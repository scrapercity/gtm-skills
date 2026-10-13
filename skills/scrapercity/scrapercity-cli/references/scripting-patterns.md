# Scripting Patterns: scrapercity CLI in Bash, Cron and CI

Tested against `scrapercity` 1.0.17 with the network stubbed (2026-10-13). Every pattern follows `references/scrapercity-agent-patterns.md`: wallet first, count first, capture the `runId`, poll at a sane interval, name the file, never loop on Apollo.

## 0. Script header

```bash
#!/usr/bin/env bash
set -euo pipefail
SC=(npx -y scrapercity@1.0.17)        # pinned; -y skips the npx install prompt
API=https://app.scrapercity.com
: "${SCRAPERCITY_API_KEY:?set SCRAPERCITY_API_KEY or source your key file}"
TODAY=$(date -u +%Y%m%d)
```

`set -e` stops the script on the first command that exits non-zero, which every CLI failure does. `-u` catches a missing key variable before any request. The array form keeps `npx -y scrapercity@1.0.17` as separate words.

## 1. Capture the run id

```bash
start_run() {              # usage: start_run maps -q "dentist" -l "Austin, TX" --limit 200
  local out id
  out=$("${SC[@]}" "$@") || return 1
  printf '%s\n' "$out" >&2           # keep the human output in the log
  id=$(awk '/Run ID:/ {print $3}' <<<"$out")
  [[ -n "$id" ]] || return 1
  echo "$id"
}
```

The start output has a line `Run ID: ...` (indented). The third field is the id. The explicit `|| return 1` lines are needed: bash does not apply `set -e` inside a command substitution, so without them a failed start returns an empty id and the script carries on. Do not take ids from `runs`, which shows only the first 12 characters.

## 2. Start, poll, download

```bash
run=$(start_run maps -q "roofing contractor" -l "Dallas, TX" --limit 300)
"${SC[@]}" poll "$run" --interval 30
"${SC[@]}" download "$run" -o "out/maps-roofing-contractor-dallas-tx-${TODAY}-${run:0:8}.csv"
```

`poll` exits 1 on FAILED, CANCELLED or after one hour, so `set -e` stops the script before a download that would fail. For a run that can pass one hour (large `apollo`, big `crexi` searches), replace `poll` with a status loop:

```bash
wait_run() {               # usage: wait_run RUN_ID SECONDS_BETWEEN MAX_CHECKS
  local run=$1 gap=$2 max=$3 i s
  for ((i = 1; i <= max; i++)); do
    s=$("${SC[@]}" status "$run" | awk '/^Status:/ {print $2}')
    case "$s" in
      SUCCEEDED) return 0 ;;
      FAILED|CANCELLED) "${SC[@]}" logs "$run" >&2; return 1 ;;
    esac
    sleep "$gap"
  done
  echo "run $run still $s after $max checks" >&2; return 2
}
wait_run "$run" 120 90      # 2 minutes apart, up to 3 hours
```

Apollo: do not script a wait at all in an interactive session. Start it, store the id, and let the webhook registered at app.scrapercity.com/dashboard/webhooks trigger the download job. If there is no webhook, `wait_run "$run" 3600 96` checks hourly for up to 4 days.

## 3. Loop over segments

```bash
for city in "Dallas, TX" "Fort Worth, TX" "Austin, TX"; do
  slug=$(tr '[:upper:]' '[:lower:]' <<<"$city" | tr -cs 'a-z0-9' '-' | sed 's/-$//')
  run=$(start_run maps -q "roofing contractor" -l "$city" --limit 300)
  printf '%s\tmaps\troofing contractor\t%s\t%s\n' "$(date -u +%FT%TZ)" "$city" "$run" >> runs.tsv
  sleep 31                   # different searches, but stay clear of the 30 second repeat window
done
while IFS=$'\t' read -r ts tool term city run; do
  "${SC[@]}" poll "$run" --interval 30
  slug=$(tr '[:upper:]' '[:lower:]' <<<"$city" | tr -cs 'a-z0-9' '-' | sed 's/-$//')
  "${SC[@]}" download "$run" -o "out/maps-roofing-contractor-${slug}-${TODAY}-${run:0:8}.csv"
done < runs.tsv
```

Starting all runs first and polling after keeps total time near the slowest run. Stay under 10 concurrent scrapes and 100 API requests a minute per key (scrapercity.com/api-docs). Three runs at `--limit 300` have a ceiling of 900 x $0.0099 = $8.91: show that before the loop runs.

## 4. Wallet guard

```bash
need=10.00
bal=$("${SC[@]}" wallet | sed -n 's/^Balance: \$\([0-9.]*\).*/\1/p')
awk -v b="$bal" -v n="$need" 'BEGIN { exit !(b + 0 >= n + 0) }' \
  || { echo "wallet \$$bal is below the \$$need this job can spend" >&2; exit 3; }
```

Set `need` to the job's ceiling. Exit code 3 separates "not enough money" from a CLI error (1) in cron mail and CI logs.

## 5. Daily new records with the CLI only

This loop delivers new leads into the account each day and keeps a log. It does not write the rows to a file, because `db-leads` prints only the first 3 rows of each page.

```bash
after=0; pulled=0; target=400
while (( pulled < target )); do
  out=$("${SC[@]}" db-leads --title "VP Sales, Head of Sales" --company-country "United States" \
        --min-employees 50 --max-employees 200 --keywords saas --has-email \
        --exclude-delivered --after "$after" --limit 100)
  more=$(sed -n 's/^\.\.\. and \([0-9]*\) more$/\1/p' <<<"$out")
  pulled=$(( pulled + 3 + ${more:-0} ))      # 3 shown plus the rest; overcounts a page of 1-2 rows
  next=$(sed -n 's/^Next page: --after //p' <<<"$out")
  [[ -z "$next" ]] && break
  after=$next
  sleep 1
done
echo "$(date -u +%F) db-leads new=$pulled last_after=$after" >> db-leads.log
```

`db-local` works the same way with its own flags (`--keyword dentist --location "Austin, TX" --has-email`) and prints `N total businesses`.

## 6. Daily new records written to a file (REST loop)

```bash
pull_db() {   # usage: pull_db PATH TARGET OUTFILE [--data-urlencode k=v ...]; prints rows pulled
  local path=$1 target=$2 out=$3; shift 3
  local after=0 got=0 lim resp n
  : > "$out"
  while (( got < target )); do
    lim=$(( target - got < 100 ? target - got : 100 ))
    resp=$(curl -sS --fail-with-body -G "$API$path" \
      -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
      --data-urlencode "excludeDelivered=true" --data-urlencode "limit=$lim" \
      --data-urlencode "after=$after" "$@") || { printf '%s\n' "$resp" >&2; return 1; }
    n=$(jq '.data | length' <<<"$resp")
    jq -c '.data[]' <<<"$resp" >> "$out"
    got=$(( got + n ))
    after=$(jq -r '.pagination.next_after // empty' <<<"$resp")
    if (( n == 0 )) || [[ -z "$after" ]]; then break; fi
    sleep 1
  done
  echo "$got"
}

n_leads=$(pull_db /api/v1/database/leads 400 "out/leads-vp-sales-saas-us-${TODAY}.jsonl" \
  --data-urlencode "title=VP Sales, Head of Sales" --data-urlencode "companyCountry=United States" \
  --data-urlencode "minEmployees=50" --data-urlencode "maxEmployees=200" \
  --data-urlencode "keywords=saas" --data-urlencode "hasEmail=true")
n_dent=$(pull_db /api/v1/database/local-businesses 100 "out/local-dentist-austin-tx-${TODAY}.jsonl" \
  --data-urlencode "keyword=dentist" --data-urlencode "location=Austin, TX" --data-urlencode "hasEmail=true")
```

Array filters repeat the key (`--data-urlencode "seniority=vp" --data-urlencode "seniority=director"`). `--fail-with-body` needs curl 7.76 or newer; it makes curl exit non-zero on HTTP errors while keeping the message, and the `|| { ...; return 1; }` passes that failure out of the function (a command substitution does not inherit `set -e`). A 503 here means the search ran too long: narrow it.

JSON lines to CSV, with arrays joined by `;`:

```bash
jsonl_to_csv() {   # usage: jsonl_to_csv in.jsonl out.csv
  [[ -s "$1" ]] || { : > "$2"; return 0; }
  jq -rs '(.[0] | keys_unsorted) as $k | ($k | @csv),
          (.[] | [.[$k[]]] | map(if type == "array" then join(";") elif type == "object" then tojson else . end) | @csv)' \
    "$1" > "$2"
}
```

## 7. Pipe a CSV into enrichment

Pull a clean, deduplicated email list out of any CSV, whatever the column is called:

```bash
grep -Eoh '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' out/*-"${TODAY}".jsonl \
  | tr '[:upper:]' '[:lower:]' | sort -u > "out/emails-${TODAY}.txt"
wc -l < "out/emails-${TODAY}.txt"     # units for the estimate: lines x $0.0072
run=$(start_run email-validate --file "out/emails-${TODAY}.txt")
"${SC[@]}" poll "$run" --interval 30
"${SC[@]}" download "$run" -o "out/validated-daily-feed-${TODAY}-${run:0:8}.csv"
```

`email-validate --file` reads every line that contains `@`, so a one-column file or a raw grep result both work.

Build an `email-find` input file safely (the CLI splits on plain commas and expects the header to contain `first`):

```bash
python3 -I - "$IN" > contacts.csv <<'PY'
import csv, sys
r = csv.DictReader(open(sys.argv[1], newline=""))
print("first_name,last_name,domain,company_name")
for row in r:
    vals = [(row.get(k) or "").replace(",", " ").strip() for k in ("first_name", "last_name", "domain", "company_name")]
    if vals[0] and vals[2]:
        print(",".join(vals))
PY
"${SC[@]}" email-find --file contacts.csv
```

## 8. Cron

Cron starts jobs with a minimal environment: no shell profile, a short `PATH`, no `SCRAPERCITY_API_KEY`. Put both in the script.

```bash
# ~/.config/scrapercity/env  (chmod 600)
export SCRAPERCITY_API_KEY=YOUR_SCRAPERCITY_API_KEY
export PATH=/usr/local/bin:/usr/bin:/bin      # the folder that holds node and npx (check: dirname "$(command -v node)")
```

```bash
# top of daily-feed.sh
source "$HOME/.config/scrapercity/env"
cd "$HOME/sc"
exec 9>"$HOME/sc/.daily-feed.lock"; flock -n 9 || { echo "previous run still going" >&2; exit 0; }
```

```cron
# m  h  dom mon dow   command  (machine clock in UTC)
20   0  *   *   *     $HOME/sc/daily-feed.sh >> $HOME/sc/logs/daily-feed.log 2>&1
```

Run after 00:00 UTC, when the database allowance resets (scrapercity.com/api-docs). If the machine clock is local time, convert. `flock` (Linux util-linux) stops a slow run from overlapping the next one.

## 9. CI (GitHub Actions)

```yaml
name: scrapercity-daily-feed
on:
  schedule:
    - cron: "20 0 * * *"        # UTC
  workflow_dispatch: {}
jobs:
  feed:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Pull and validate
        run: bash scripts/daily-feed.sh
        env:
          SCRAPERCITY_API_KEY: ${{ secrets.SCRAPERCITY_API_KEY }}
      - uses: actions/upload-artifact@v4
        with:
          name: daily-feed-${{ github.run_id }}
          path: out/
          retention-days: 7
```

GitHub runs scheduled workflows in UTC, only on the default branch, may delay them under load, and disables them in public repositories after 60 days without repository activity. Store the key as an encrypted secret; never print it. Uploaded artifacts hold lead data, so keep retention short and the repository private.

## 10. Exit codes and error text for scripts

| Exit | Source | Meaning |
|---|---|---|
| 0 | CLI | Success |
| 1 | CLI | Any failure; stderr has `✗ ` plus the server message |
| 2 | `wait_run` above | Still running after the allowed checks |
| 3 | Wallet guard above | Balance below the job's ceiling |
| 22 | curl `--fail-with-body` | HTTP error from a REST call |

Branch on stderr text when a failure needs its own handling: a message about balance means top up (402); about a duplicate means look up the earlier run with `runs --hours 1` (409); about rate limits means wait 30 seconds and retry once (429); about a search taking too long means narrow the filters (503).

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://docs.npmjs.com/cli/v10/commands/npx
- https://pubs.opengroup.org/onlinepubs/9799919799/utilities/crontab.html
- https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
- https://man7.org/linux/man-pages/man1/flock.1.html
- https://curl.se/docs/manpage.html
- https://jqlang.org/manual/
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
