# Repeat Pull Recipes

How to run the same pull on a schedule, keep snapshots, diff them, and push the signals to a sequencer or CRM. Three ways to schedule: cron with REST or the CLI, n8n, and ScraperCity webhooks for runs that finish later. Endpoints, run lifecycle and error handling follow `references/scrapercity-agent-patterns.md`.

## 1. Snapshot layout

One folder (or table) per signal. Keep every raw download and a small state file.

```text
signals/
  s5-techstack-klaviyo/
    raw/techstack-klaviyo-20261012-9f8e7d6c.csv
    raw/techstack-klaviyo-20261019-1a2b3c4d.csv
    state.csv          # key, first_seen, last_seen, absent_runs, metric fields
    events-20261019.csv  # appeared, disappeared, changed rows from this run
  s1-local-new/
    raw/local-medspa-phx-20261019.jsonl
    state.csv
```

| State column | Meaning |
|-|-|
| `key` | Diff key: domain, E.164 phone, listing URL or normalized address |
| `first_seen` | Pull date the key first appeared (the date anchor) |
| `last_seen` | Most recent pull that returned it |
| `absent_runs` | Consecutive pulls it was missing (the script below reports a removal on the second miss; change the constant to suit your checks) |
| metric columns | `reviews_count`, `total_score`, estimated visits, distress type: whatever the signal compares |

## 2. Diff script (Python standard library)

Save as `diff_snapshot.py` in your own tools folder, outside the downloads folder. It compares a new download with `state.csv`, writes the events file and updates state.

```python
#!/usr/bin/env python3
"""Usage: diff_snapshot.py state.csv new.csv KEY_COLUMN RUN_DATE [METRIC:THRESHOLD ...]
Example: diff_snapshot.py state.csv maps-20261019.csv phone 2026-10-19 reviews_count:10 total_score:-0.2
"""
import csv, os, sys

state_path, new_path, key_col, run_date = sys.argv[1:5]
metrics = [m.split(":") for m in sys.argv[5:]]

def norm(v):
    return (v or "").strip().lower()

state = {}
if os.path.exists(state_path):
    with open(state_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            state[row["key"]] = row

baseline = not state
seen, events = set(), []
with open(new_path, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        k = norm(row.get(key_col))
        if not k or k in seen:
            continue
        seen.add(k)
        old = state.get(k)
        if old is None:
            state[k] = {"key": k, "first_seen": run_date, "last_seen": run_date, "absent_runs": "0"}
            if not baseline:
                events.append({"key": k, "event": "appeared", "detail": "", "signal_date": run_date})
        else:
            old["last_seen"], old["absent_runs"] = run_date, "0"
            for name, thr in metrics:
                try:
                    before, after, t = float(old.get(name) or "nan"), float(row.get(name) or "nan"), float(thr)
                except ValueError:
                    continue
                delta = after - before
                if (t > 0 and delta >= t) or (t < 0 and delta <= t):
                    events.append({"key": k, "event": f"{name}_changed", "detail": f"{before}->{after}", "signal_date": run_date})
        for name, _ in metrics:
            state[k][name] = row.get(name, "")

for k, row in state.items():
    if k not in seen:
        row["absent_runs"] = str(int(row.get("absent_runs") or 0) + 1)
        if row["absent_runs"] == "2" and not baseline:
            events.append({"key": k, "event": "disappeared", "detail": "absent 2 runs", "signal_date": run_date})

cols = ["key", "first_seen", "last_seen", "absent_runs"] + [m[0] for m in metrics]
with open(state_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    w.writerows(state.values())
out = os.path.join(os.path.dirname(state_path) or ".", f"events-{run_date.replace('-', '')}.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["key", "event", "detail", "signal_date"])
    w.writeheader()
    w.writerows(events)
print(f"{'baseline' if baseline else 'diff'}: {len(seen)} rows, {len(events)} events -> {out}")
```

Normalize keys before diffing (lowercase domains without `www.`, E.164 phones), per `references/list-quality-standard.md` section 3. Run the script with Python's isolated flag (`python3 -I`) when the CSVs came from the internet.

## 3. Cron with REST (databases)

The CLI `db-local` and `db-leads` commands print only the first three rows, so scheduled database pulls call REST directly.

```bash
#!/usr/bin/env bash
# pull-local-new.sh: weekly new med spa listings with 5 or fewer reviews, new to this account
set -euo pipefail
DAY=$(date +%Y%m%d)
OUT="$HOME/signals/s1-local-new/raw/local-medspa-phx-$DAY.jsonl"
after=0
while [ -n "$after" ] && [ "$after" != "null" ]; do
  resp=$(curl -sS -G "https://app.scrapercity.com/api/v1/database/local-businesses" \
    -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
    --data-urlencode "keyword=med spa" \
    --data-urlencode "location=Phoenix AZ" --data-urlencode "location=Scottsdale AZ" \
    --data-urlencode "maxReviews=5" --data-urlencode "hasPhone=true" \
    --data-urlencode "excludeDelivered=true" --data-urlencode "limit=100" \
    --data-urlencode "after=$after")
  echo "$resp" | jq -c '.data[]' >> "$OUT"
  after=$(echo "$resp" | jq -r '.pagination.next_after')
  sleep 1
done
```

## 4. Cron with REST (scrapers: start, poll, download)

```bash
#!/usr/bin/env bash
# pull-techstack.sh: weekly Tech Stack Search for one technology ($4.99 per run)
set -euo pipefail
DAY=$(date +%Y%m%d)
API="https://app.scrapercity.com"
AUTH="Authorization: Bearer $SCRAPERCITY_API_KEY"
run=$(curl -sS -X POST "$API/api/v1/scrape/techstack" -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"technology\":\"Klaviyo\",\"fileName\":\"techstack-klaviyo-$DAY\"}" | jq -r '.runId')
echo "$DAY $run" >> "$HOME/signals/runs.log"
for i in $(seq 1 60); do            # 30 s x 60 = 30 min, the give-up point for this tool group
  st=$(curl -sS "$API/api/v1/scrape/status/$run" -H "$AUTH" | jq -r '.status')
  [ "$st" = "SUCCEEDED" ] && break
  if [ "$st" = "FAILED" ] || [ "$st" = "CANCELLED" ]; then echo "run $run $st" >&2; exit 1; fi
  sleep 30
done
[ "$st" = "SUCCEEDED" ] || { echo "run $run still $st" >&2; exit 1; }
curl -sS "$API/api/downloads/$run" -H "$AUTH" -o "$HOME/signals/s5-techstack-klaviyo/raw/techstack-klaviyo-$DAY-${run:0:8}.csv"
python3 -I "$HOME/tools/diff_snapshot.py" "$HOME/signals/s5-techstack-klaviyo/state.csv" \
  "$HOME/signals/s5-techstack-klaviyo/raw/techstack-klaviyo-$DAY-${run:0:8}.csv" domain "$(date +%F)"
```

Check the domain column name in the first download and change `domain` in the last line if it differs. If the POST gets no response (timeout), do not resubmit blind: call `GET /api/v1/runs?hours=1` and look for the same `fileName` first.

Manual equivalent with the CLI: `npx scrapercity builtwith "Klaviyo" --name techstack-klaviyo-20261019`, then `npx scrapercity poll <runId>` and `npx scrapercity download <runId> -o techstack-klaviyo-20261019.csv`. Other scrapers: `npx scrapercity maps --query "med spa" --location "Phoenix, AZ" --limit 200`, `npx scrapercity yelp --urls <yelp-urls>`, `npx scrapercity bizbuysell "<url>" --limit 150`, `npx scrapercity distress-list "Tampa, FL" --types preForeclosure,auction --max 300`, `npx scrapercity zillow-agents -l "Scottsdale, AZ" --limit 200`.

Crontab (server time; set `CRON_TZ` if your cron supports it):

```text
15 6 * * 1   $HOME/signals/bin/pull-techstack.sh   >> $HOME/signals/logs/techstack.log 2>&1
30 6 * * 1   $HOME/signals/bin/pull-local-new.sh   >> $HOME/signals/logs/local.log 2>&1
0  7 1 * *   $HOME/signals/bin/pull-store-universe.sh >> $HOME/signals/logs/stores.log 2>&1
```

Keep the API key in the environment of the cron user or in `~/.scrapercityrc`, never in the script.

## 5. n8n workflow

| # | Node | Settings |
|-|-|-|
| 1 | Schedule Trigger | Weekly, Monday 06:15, workflow time zone set |
| 2 | HTTP Request | POST `https://app.scrapercity.com/api/v1/scrape/techstack`, header auth credential with the API key, JSON body `{"technology": "Klaviyo", "fileName": "techstack-klaviyo-{{$now.toFormat('yyyyLLdd')}}"}` |
| 3 | Wait | 1 minute |
| 4 | HTTP Request | GET `/api/v1/scrape/status/{{$json.runId}}` |
| 5 | If | `status` equals SUCCEEDED: go to 6. RUNNING: back to 3, with a counter that stops after 30 loops. FAILED or CANCELLED: Slack alert |
| 6 | HTTP Request | GET `/api/downloads/{{runId}}`, response format File |
| 7 | Extract from File | CSV to items |
| 8 | Postgres or Google Sheets | Read the previous state for this signal |
| 9 | Code | Diff (same logic as section 2), add `signal_date`, compute score (`references/scoring-and-freshness.md`) |
| 10 | Postgres or Google Sheets | Write state and events |
| 11 | Switch | Tier A, B, C |
| 12a | HubSpot | Create or update company, create task for the owner (tier A) |
| 12b | HTTP Request | Add lead to the sequencer campaign through its API (tier B) |
| 12c | Slack | Post tier A accounts with the signal line |

For database signals, replace nodes 2 to 7 with one HTTP Request node in a loop on `pagination.next_after`.

## 6. Webhooks for runs that finish later

Register the receiving URL at app.scrapercity.com/dashboard/webhooks. ScraperCity posts when a run reaches SUCCEEDED or FAILED, with `runId`, `fileName` and `leadsCount` in the payload.

| Step | Receiver action |
|-|-|
| 1 | n8n Webhook node (or your endpoint) answers 200 at once |
| 2 | Look up `runId` in your run log; if already imported, stop (duplicate delivery) |
| 3 | `GET /api/v1/scrape/status/{runId}` to confirm SUCCEEDED (no signature scheme is documented, so the status call is the authenticity check) |
| 4 | Download, then route by `fileName` prefix to the right signal's diff |
| 5 | Mark `runId` imported |

Use webhooks for Apollo runs (hours to days) and for any large scraper run you do not want a cron job waiting on. Download within 48 hours; results are stored for 48 hours per scrapercity.com/api-docs.

## 7. Run cost per recipe

| Recipe | Tool | Size per run | Frequency | Cost per run | Cost per 4 weeks |
|-|-|-|-|-|-|
| New local listings | `query_local_business_database` | All new matches | Weekly | $0.00 on Growth | $0.00 |
| Maps re-run for review counts | `scrape_maps` | 3 terms x 200 places | Weekly | $5.94 | $23.76 |
| Yelp watched set | `scrape_yelp` `directUrls` | 300 businesses | Weekly | $2.97 | $11.88 |
| Tech adoption | `scrape_builtwith` | 1 technology | Weekly | $4.99 | $19.96 |
| Store apps | `scrape_store_leads` | 500 stores | Weekly | $1.95 | $7.80 |
| Store universe | `scrape_store_leads` | 9,800 stores | Monthly | $38.22 | $38.22 |
| Businesses for sale | `scrape_bizbuysell` | 150 listings | Weekly | $1.49 | $5.94 |
| Pre-foreclosure and auction | `scrape_distress_list` | 300 properties | Weekly | $15.00 | $60.00 |
| Agents in a market | `scrape_zillow_agents` | 200 agents | Monthly | $5.80 | $5.80 |

Every recipe over $5 a run gets one approval for the schedule, with the monthly total shown, and a `check_wallet` call inside the job that stops the run when the balance is under a floor the job sets (at least the run cost).

## 8. Social engagement types

For S19 rows imported from a social listening tool. No published benchmark ranks these engagement types, so log the type on every S19 row, set base points and touch windows per type in the program, and compare meeting rate by type.

| Engagement type | Example | Channel | First-line rule |
|-|-|-|-|
| Person posts asking for tool or vendor recommendations in your category | "Anyone using something better than X for SDR lists?" | Comment with a useful answer first, then email | Name their post; answer the question before any pitch |
| Comment on a competitor's post or launch | A question under a competitor's pricing change | Email | Name the topic; leave the competitor post out |
| Comment on a post about the problem you solve | "We hit this every quarter" under a post on list decay | Email, then call for tier A | Name the problem in their words; leave the comment out |
| Reaction (like) on a post about the problem | A like on a post about bounce rates | Email in the tier B campaign | Fit-based line |
| Reaction or comment on your own company's post | A like on your founder's post | Email or a connection request | Fit-based line; the person already knows who you are |
| New follow of your company page | Follow event from the page's admin view | Tier B campaign | Fit-based line |

Rules that hold for every row: score only people at accounts that pass fit and the exclusion list, one S19 touch per person inside the cool-down, and drop the row if the post was deleted before the first touch.

## 9. Alert payload

Every tier A row, and every hot first-party row, posts one alert to the owner. Build it once in the workflow (n8n Code node or the diff script) and send the same JSON to Slack, the CRM task and the run log, so the three always match.

```json
{
  "account": "[fill company name]",
  "domain": "[fill registrable domain]",
  "signal_id": "[fill S-number]",
  "signal_label": "[fill label]",
  "signal_date": "[fill YYYY-MM-DD or ISO timestamp for S14]",
  "source": "[fill tool id, or other:<feed> for S14 to S28]",
  "score": "[fill 0 to 100]",
  "tier": "[fill A or A-hot]",
  "owner": "[fill CRM owner]",
  "sla_due": "[fill ISO timestamp]",
  "contact": "[fill name, title, validated email, mobile if on file]",
  "first_line": "[fill under 30 words]",
  "checks": "[fill exclusion list, opt-outs, cool-down: all pass]",
  "crm_url": "[fill link to the record]"
}
```

| Field | Rule |
|-|-|
| `account`, `domain` | Domain is the dedupe key; the alert is dropped if the domain is on the exclusion list |
| `signal_id`, `signal_label`, `signal_date` | Date for weekly pulls, timestamp for S14 and S19 |
| `source` | The ScraperCity tool id, or `other:<vendor>` for outside signals, so a visit is never reported as ScraperCity data |
| `score`, `tier` | From `references/scoring-and-freshness.md`, rounded to one decimal |
| `owner`, `sla_due` | Owner from CRM territory rules; `sla_due` from the program's touch window for the tier |
| `first_line` | The angle from `references/signal-catalog.md` |
| `checks` | Written by the workflow, so a person cannot skip a check |

Filled example, as posted to Slack:

```text
[A] kestrelcoffee.example  |  Kestrel Coffee
Signal: S5 Klaviyo adopted (2026-10-12) + S8 traffic band crossed  |  source: scrape_builtwith, scrape_store_leads
Score 86.4  |  Owner: Dana R.  |  Due: 2026-10-21 17:00 CT
Contact: Priya Nair, Founder, priya@kestrelcoffee.example (valid), mobile on file
First line: "Saw Kestrel started running Klaviyo in the last couple of weeks; the first 90 days are when flows get built or stall."
Checks: not excluded, no opt-out, no sequence in 90 days  |  HubSpot task created
```

For an S14 alert the second line reads `Signal: S14 pricing page, 2026-10-19T14:07 CT | source: other:rb2b`, and `Due` follows the program's S14 touch window.

## 10. Free outside feeds on the same schedule

Three outside signals come from public endpoints with no key, so they run in the same cron or n8n workflow as the ScraperCity pulls and feed the same diff script (section 2).

### EDGAR: Form D, earnings and officer changes (S22, S23, S20)

```bash
#!/usr/bin/env bash
# pull-edgar.sh: last 7 days of Form D filings in one state, and 8-Ks for watched public companies
set -euo pipefail
UA="Acme Growth ops@acme.example"            # SEC asks for a company name and a contact email
END=$(date +%F); START=$(date -d '7 days ago' +%F)   # GNU date; on macOS use: date -v-7d +%F
DAY=$(date +%Y%m%d); Q="dateRange=custom&startdt=$START&enddt=$END"
{ echo "adsh,file_date,name,detail"
  curl -sS -A "$UA" "https://efts.sec.gov/LATEST/search-index?forms=D&$Q&locationCodes=TX" \
  | jq -r '.hits.hits[]._source | [.adsh, .file_date, .display_names[0], (.biz_locations[0] // "")] | @csv'
} > "$HOME/signals/s22-formd/raw/formd-tx-$DAY.csv"
{ echo "adsh,file_date,name,detail"
  while read -r cik; do                       # one 10-digit CIK per line
    curl -sS -A "$UA" "https://efts.sec.gov/LATEST/search-index?forms=8-K&ciks=$cik&$Q" \
    | jq -r '.hits.hits[]._source | [.adsh, .file_date, .display_names[0], (.items | join(" "))] | @csv'
    sleep 0.2                                 # stays under 10 requests a second
  done < "$HOME/signals/watched-ciks.txt"
} > "$HOME/signals/s23-8k/raw/8k-watched-$DAY.csv"
```

Diff each file on `adsh` (the accession number). Route 8-K rows by `detail`: `2.02` is S23, `5.02` is S20. The SEC webmaster FAQ sets 10 requests a second as the maximum. Page past the first 100 hits with `&from=100` when a state's Form D list is longer.

### Job boards (S18)

| ATS | Call | Date field | Diff key |
|-|-|-|-|
| Greenhouse | `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs` | `updated_at` in the list; `first_published` on `GET .../jobs/{job_id}` | `id` |
| Ashby | `GET https://api.ashbyhq.com/posting-api/job-board/{JOB_BOARD_NAME}` | `publishedAt` | `id` |
| Lever | `GET https://api.lever.co/v0/postings/{site}` | None documented; use first-seen pull date | `id` |

Keep a `boards.csv` of watched domains with their ATS and token (read it off the careers page link). A weekly loop fetches each board, keeps titles that match your role list, writes one row per posting, and runs the diff with `id` as the key. A posting that disappears from the board is closed once the URL no longer loads: run the S20 re-pull for that domain the following month.

### Page monitors (S24, S25)

Run changedetection.io (self-hosted with Docker) on competitor pricing, changelog and status pages, and on watched accounts' newsroom pages. Point its webhook notification at an n8n Webhook node; the workflow adds `signal_id` (S24 or S25), the page URL and the change date, then for S24 starts one Tech Stack Search run for the competitor's technology and diffs the result against the last install-base pull.

| Feed | Cost |
|-|-|
| EDGAR, job board APIs, changedetection.io self-hosted | $0 plus server time |
| Install base per competitor change, `scrape_builtwith` | $4.99 per run |
| Buyers at matched domains, `query_lead_database` | Included in Growth |
| Validation of found emails, `validate_emails` | $0.00169 each |

## Sources

- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/about/webmaster-frequently-asked-questions
- https://developers.greenhouse.io/job-board.html
- https://developers.ashbyhq.com/docs/public-job-posting-api
- https://github.com/lever/postings-api
- https://github.com/dgtlmoon/changedetection.io
