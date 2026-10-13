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
| `absent_runs` | Consecutive pulls it was missing (removal needs 2) |
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

Every recipe over $5 a run gets one approval for the schedule, with the monthly total shown, and a `check_wallet` call inside the job that stops the run when the balance is under 2x the run cost.

## Sources

- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
