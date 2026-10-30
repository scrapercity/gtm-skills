# ScraperCity CLI Run Spec: daily VP Sales and Texas dentist feed with validation

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Scenario: Priya runs outbound for a two-offer agency on the Growth plan. Every weekday morning before 8am Central she wants two fresh files on a small Ubuntu server: 400 new VP or Head of Sales contacts at US software companies with 50-500 employees, and 100 new Texas dental practices with an email. Every email gets validated before it reaches the sequencer. Nothing pulled on an earlier day may come back.

## Environment

| Item | Value |
|---|---|
| Package | scrapercity@1.0.17, pinned, run with `npx -y` |
| Node | v20.17.0 at /usr/local/bin/node |
| Key source | `SCRAPERCITY_API_KEY` exported from `~/.config/scrapercity/env` (chmod 600), a key named "feed-server" used only by this job |
| Working folder | /home/priya/sc, output under /home/priya/sc/out/YYYYMMDD |
| Plan (from wallet) | Growth ($149 a month, $159 of credits per cycle), balance $152.40, renews 2026-11-01 |

## Commands

Every command must exist in scrapercity 1.0.17 and use only flags that command reads. REST rows start with `curl`.

| Step | Command | Maps to | Billable units | Notes |
|---|---|---|---|---|
| 1 | `npx -y scrapercity@1.0.17 wallet` | `GET /api/v1/wallet` | 0 | Guard: stop when balance is under the day's $0.85 ceiling |
| 2 | `npx -y scrapercity@1.0.17 db-leads --title "VP Sales, Vice President of Sales, Head of Sales" --not-title "Assistant, Intern, Operations" --company-country "United States" --industry "computer software" --min-employees 50 --max-employees 500 --has-email --limit 1` | Lead Database count | 0 | Printed `18940 total leads, page 1 of 18940`. Run once by hand |
| 3 | `npx -y scrapercity@1.0.17 db-local --keyword dentist --location "Texas" --has-email --limit 1` | Local Business Database count | 0 | Printed `9870 total businesses`; `Places: Texas, US`. Run once by hand |
| 4 | `curl -G https://app.scrapercity.com/api/v1/database/leads` with the step 2 filters plus `excludeDelivered=true`, `after`, `limit` | Lead Database rows | 400 new leads a day | Cursor loop from `after=0`; rows saved as JSON lines, then CSV |
| 5 | `curl -G https://app.scrapercity.com/api/v1/database/local-businesses` with `keyword=dentist`, `location=Texas`, `hasEmail=true`, `excludeDelivered=true` | Local Business Database rows | 100 new businesses a day | Same loop |
| 6 | `npx -y scrapercity@1.0.17 email-validate --file out/20261014/emails.txt` | `validate_emails` | up to 500 emails a day | Unique, lowercased emails from steps 4 and 5 |
| 7 | `npx -y scrapercity@1.0.17 poll RUN_ID --interval 30` | Status loop | 0 | Exits 1 on FAILED, CANCELLED or after 1 hour |
| 8 | `npx -y scrapercity@1.0.17 download RUN_ID -o out/20261014/validated-daily-feed-20261014-3c9e1f0a.csv` | CSV download | 0 | Named by tool, segment, date, run id |

## Cost Estimate

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Lead Database new leads, 400 a run for 22 weekday runs | 8,800 | included in Growth | $0.00 |
| Local Business Database new businesses, 100 a run for 22 runs | 2,200 | included in Growth | $0.00 |
| `email-validate` on every new email, up to 500 a run for 22 runs | 11,000 | $0.00169 | $18.59 |
| Total | | | $18.59 |

Approval: Per run the ceiling is 500 x $0.00169 = $0.85. Per month (22 weekdays) it is $18.59, 11.7% of the $159 Growth credit, leaving $140.41 for other work each cycle. Shown to Priya as a monthly figure and approved in writing on 2026-10-13. Each run uses 400 and 100 of the two databases' 100,000 a day allowances. At these rates the lead segment lasts about 47 runs (18,940 / 400, a little over 9 weeks) and the dentist segment about 99 runs (9,870 / 100, about 20 weeks); the script warns on a short day so a segment can be widened before it runs dry.

## Script

```bash
#!/usr/bin/env bash
# /home/priya/sc/daily-feed.sh - new VP Sales leads and Texas dentists, validated, once a day
set -euo pipefail
source "$HOME/.config/scrapercity/env"          # exports SCRAPERCITY_API_KEY and PATH
: "${SCRAPERCITY_API_KEY:?missing key}"
cd "$HOME/sc"
exec 9>"$HOME/sc/.daily-feed.lock"; flock -n 9 || { echo "previous run still going" >&2; exit 0; }

SC=(npx -y scrapercity@1.0.17)
API=https://app.scrapercity.com
TODAY=$(date -u +%Y%m%d)
OUT="out/$TODAY"; mkdir -p "$OUT"
LEADS_TARGET=400; DENT_TARGET=100; NEED=0.85

start_run() {
  local out id
  out=$("${SC[@]}" "$@") || return 1
  printf '%s\n' "$out" >&2
  id=$(awk '/Run ID:/ {print $3}' <<<"$out")
  [[ -n "$id" ]] || return 1
  echo "$id"
}

pull_db() {   # pull_db PATH TARGET OUTFILE [curl args]; prints rows pulled
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

jsonl_to_csv() {
  [[ -s "$1" ]] || { : > "$2"; return 0; }
  jq -rs '(.[0] | keys_unsorted) as $k | ($k | @csv),
          (.[] | [.[$k[]]] | map(if type == "array" then join(";") elif type == "object" then tojson else . end) | @csv)' \
    "$1" > "$2"
}

# 1. Wallet guard
bal=$("${SC[@]}" wallet | sed -n 's/^Balance: \$\([0-9.]*\).*/\1/p')
awk -v b="$bal" -v n="$NEED" 'BEGIN { exit !(b + 0 >= n + 0) }' \
  || { echo "wallet \$$bal is below today's \$$NEED ceiling" >&2; exit 3; }

# 2. New records only: excludeDelivered with an after cursor that starts at 0 every day
n_leads=$(pull_db /api/v1/database/leads "$LEADS_TARGET" "$OUT/leads-vp-sales-software-us-$TODAY.jsonl" \
  --data-urlencode "title=VP Sales, Vice President of Sales, Head of Sales" \
  --data-urlencode "notTitle=Assistant, Intern, Operations" \
  --data-urlencode "companyCountry=United States" --data-urlencode "industry=computer software" \
  --data-urlencode "minEmployees=50" --data-urlencode "maxEmployees=500" --data-urlencode "hasEmail=true")
n_dent=$(pull_db /api/v1/database/local-businesses "$DENT_TARGET" "$OUT/local-dentist-tx-$TODAY.jsonl" \
  --data-urlencode "keyword=dentist" --data-urlencode "location=Texas" --data-urlencode "hasEmail=true")
jsonl_to_csv "$OUT/leads-vp-sales-software-us-$TODAY.jsonl" "$OUT/leads-vp-sales-software-us-$TODAY.csv"
jsonl_to_csv "$OUT/local-dentist-tx-$TODAY.jsonl" "$OUT/local-dentist-tx-$TODAY.csv"

# 3. Unique emails for validation
grep -Eoh '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$OUT"/*.jsonl \
  | tr '[:upper:]' '[:lower:]' | sort -u > "$OUT/emails.txt" || true
n_emails=$(wc -l < "$OUT/emails.txt" | tr -d ' ')
if (( n_emails == 0 )); then
  printf '%s\tleads=%s\tdentists=%s\temails=0\trun=none\n' "$TODAY" "$n_leads" "$n_dent" >> runs.tsv
  exit 0
fi

# 4. Validate, wait, download
run=$(start_run email-validate --file "$OUT/emails.txt")
"${SC[@]}" poll "$run" --interval 30
"${SC[@]}" download "$run" -o "$OUT/validated-daily-feed-$TODAY-${run:0:8}.csv"

# 5. Run log, and a warning when a segment comes back short
printf '%s\tleads=%s\tdentists=%s\temails=%s\trun=%s\n' "$TODAY" "$n_leads" "$n_dent" "$n_emails" "$run" >> runs.tsv
(( n_leads < LEADS_TARGET )) && echo "lead segment short: $n_leads of $LEADS_TARGET" >&2
(( n_dent < DENT_TARGET )) && echo "dentist segment short: $n_dent of $DENT_TARGET" >&2
exit 0
```

## Schedule

| Item | Value |
|---|---|
| Runner | crontab on the Ubuntu server, user priya |
| Schedule | `20 11 * * 1-5 /home/priya/sc/daily-feed.sh >> /home/priya/sc/logs/daily-feed.log 2>&1` |
| Time zone | Server clock in UTC; 11:20 UTC is 6:20am Central during daylight time and 5:20am in winter, both before 8am |
| Allowance reset | 00:00 UTC per scrapercity.com/api-docs, so each run starts on a fresh 100,000 a day allowance |
| Overlap guard | `flock -n` on /home/priya/sc/.daily-feed.lock; a second copy exits 0 |

## Failure Handling

| Failure | Detection | Action |
|---|---|---|
| Balance under $0.85 | Wallet guard exits 3 with the balance in the log | Priya tops up; the next weekday run continues from `after=0`, so no day's leads are lost |
| Key missing or rejected (401) | `:?missing key` stops the script, or the CLI exits 1 with a key message | Fix `~/.config/scrapercity/env`; never put the key in the script |
| Database search took too long (503) | curl exits 22; the server message goes to the log | Narrow the segment (split by `companyState`) and rerun by hand |
| Rate limited (429) | curl exits 22 with a rate message | The 1 second sleep keeps the loop near 60 requests a minute; rerun once after 30 seconds |
| Validation run FAILED or still running after 1 hour | `poll` exits 1; `set -e` stops before download | `npx -y scrapercity@1.0.17 logs RUN_ID`, then `status` later; results stay 48 hours |
| Duplicate submit (409) on a manual rerun | CLI exits 1 with a duplicate message | `npx -y scrapercity@1.0.17 runs --hours 1`, match by time, download that run instead |
| Segment exhausted | Short-segment warning on stderr | Widen titles or size band; re-run the step 2 count |

## Verification

| Check | Result |
|---|---|
| Dry run with targets set to 5 and 5 on 2026-10-13 | 5 leads and 5 dentists written, 10 emails validated for $0.02, file `validated-daily-feed-20261013-5a1d2e7b.csv` |
| First full run 2026-10-14 | leads=400, dentists=100, emails=497 (3 duplicates removed), run 3c9e1f0a SUCCEEDED, cost 497 x $0.00169 = $0.84 |
| Second run 2026-10-15 overlap check | `comm -12` on the two days' sorted email lists returned 0 shared emails |
| Script lint | `bash -n daily-feed.sh` exits 0; `shellcheck` shows no errors |
| Key exposure | `grep -c SCRAPERCITY_API_KEY= daily-feed.sh` returns 0 |
