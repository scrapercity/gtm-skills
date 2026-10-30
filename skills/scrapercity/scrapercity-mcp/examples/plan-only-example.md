# ScraperCity MCP Setup and Run Plan: 300 marketing leaders at US Series B cybersecurity companies

_Illustrative example. Domains and the user are invented to show the format. Prices are ScraperCity catalog prices._

Scenario: Dana asks Claude Code (macOS, home folder `/Users/dana`) to set up the ScraperCity MCP server and use it to find 300 VPs of Marketing and Heads of Marketing at US cybersecurity companies that raised a Series B, with verified emails and the total cost. She has a Growth plan and a list of Series B cybersecurity domains from her funding data source.

Plan only: nothing below has run yet. Run the steps in order; counts, runIds and validation results come from those runs.

## Answer

- Source: the Lead Database through `query_lead_database`, included in Growth. It has no funding-stage filter, so Series B comes from your domain list, passed as `companyDomain`. Step 4 tests whether a people-search URL can carry the stage instead.
- Cost: $0.51 to validate 300 emails, plus $0.00169 for each top-up email if fewer than 300 come back `valid`. The database pull costs $0 on Growth.
- Every paid call waits for your go-ahead. Time to file: database pages return in seconds, validation in 1 to 10 minutes.

## Client Setup

| Item | Value |
|---|---|
| Client | Claude Code on macOS, Node 18 or newer |
| Scope | user (stored in `~/.claude.json`, loads in every project) |
| Args | -y --package scrapercity scrapercity-mcp |
| Key handling | A dedicated key from app.scrapercity.com/dashboard/api-docs, passed with `--env` |
| Version | Unpinned (npm latest is 1.0.17) |

1. Check Node and add the server. Options go before the server name; everything after `--` is the server command.

```bash
node --version   # v18 or higher
claude mcp add --env SCRAPERCITY_API_KEY=YOUR_SCRAPERCITY_API_KEY --transport stdio --scope user \
  scrapercity -- npx -y --package scrapercity scrapercity-mcp
claude mcp list  # expect: scrapercity ... Connected
```

2. Start a new `claude` session and run `/mcp`: it lists 25 `scrapercity` tools. Step 2 below proves the key.

## Agent Rules

Add to `~/.claude/settings.json`. The three free reads run without a prompt; every scrape_*, find_*, validation, database and download call asks first.

```json
{
  "permissions": {
    "allow": [
      "mcp__scrapercity__check_wallet",
      "mcp__scrapercity__list_runs",
      "mcp__scrapercity__check_run_status"
    ],
    "ask": [
      "mcp__scrapercity__scrape_*",
      "mcp__scrapercity__find_*",
      "mcp__scrapercity__validate_emails",
      "mcp__scrapercity__search_criminal_records",
      "mcp__scrapercity__query_lead_database",
      "mcp__scrapercity__query_local_business_database",
      "mcp__scrapercity__download_results",
      "mcp__scrapercity__cancel_run"
    ]
  }
}
```

## Run Plan

Your input: `domains.txt` in `/Users/dana/Leads/cyber-b/`, one company domain per line (for example `examplesec.example`), exported from your funding data with Series B, US HQ and cybersecurity applied there.

**Step 1: clean and batch the domains (Bash).** Batches of 200 keep each call well under the 16KB query limit.

```bash
mkdir -p "$HOME/Leads/cyber-b" && cd "$HOME/Leads/cyber-b"
tr -d '\r' < domains.txt | tr 'A-Z' 'a-z' | sed -E 's#^https?://##; s#^www\.##; s#/.*$##' | grep -v '^$' | sort -u > domains.clean.txt
split -l 200 domains.clean.txt batch_
for f in batch_??; do paste -sd, "$f" > "$f.csv"; done
ls batch_??.csv
```

**Step 2: wallet (free).** `plan.name` must be Growth or Scale.

```json
{"tool": "check_wallet", "arguments": {}}
```

**Step 3: count, then a 10-row sample, per batch (free).** Claude pastes the contents of `batch_aa.csv` as `companyDomain`, reads `pagination.total`, repeats for each batch file and adds the totals. Then the same arguments with `"limit": 10`: check title, US HQ and company against your list, and note the keys that hold the email, title and company website (step 6 reads them).

```json
{"tool": "query_lead_database", "arguments": {"title": "VP Marketing, VP of Marketing, Vice President of Marketing, Vice President Marketing, Head of Marketing", "notTitle": "Assistant, Intern", "companyCountry": ["United States"], "companyDomain": "CONTENTS_OF_batch_aa.csv", "hasEmail": true, "limit": 1}}
```

**Step 4: can a people-search URL carry the stage? (free).** In Apollo, build a people search with the same titles, company location United States, industry Computer & Network Security and funding Series B, and copy the URL from the address bar.

```json
{"tool": "query_lead_database", "arguments": {"url": "APOLLO_PEOPLE_SEARCH_URL", "limit": 1}}
```

Read `search_translation`. Funding stage under `applied`: this URL can replace the domain list in steps 3 and 5. Under `approximated` or `not_supported`: the count ignores the stage, so keep the domain list.

**Step 5: pull every match through MCP (free).** Start each batch at `"after": "0"`, then send each response's `pagination.next_after` until it is null.

```json
{"tool": "query_lead_database", "arguments": {"title": "VP Marketing, VP of Marketing, Vice President of Marketing, Vice President Marketing, Head of Marketing", "notTitle": "Assistant, Intern", "companyCountry": ["United States"], "companyDomain": "CONTENTS_OF_batch_aa.csv", "hasEmail": true, "limit": 100, "after": "0"}}
```

Where the rows go: Claude Code saves a tool result over 25,000 tokens (the default `MAX_MCP_OUTPUT_TOKENS`) or 50,000 characters to a file and hands Claude the path (Claude Code MCP docs, checked 2026-10-13); Claude appends that page's `data` rows to `leads.jsonl`. A smaller page lands in the conversation and Claude writes its rows to `leads.jsonl`. If page 1 lands in the conversation with Claude Code's 10,000-token warning, finish with this loop instead, so the remaining pages stay out of the chat (100 requests a minute per key, scrapercity.com/api-docs):

```bash
cd "$HOME/Leads/cyber-b"
: > leads.jsonl
for b in batch_??.csv; do
  after=0
  while [ -n "$after" ]; do
    resp=$(curl -sS --fail-with-body -G "https://app.scrapercity.com/api/v1/database/leads" \
      -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
      --data-urlencode "title=VP Marketing, VP of Marketing, Vice President of Marketing, Vice President Marketing, Head of Marketing" \
      --data-urlencode "notTitle=Assistant, Intern" \
      --data-urlencode "companyCountry=United States" \
      --data-urlencode "companyDomain=$(cat "$b")" \
      --data-urlencode "hasEmail=true" --data-urlencode "limit=100" \
      --data-urlencode "after=$after") || { printf '%s\n' "$resp" >&2; break 2; }
    jq -c '.data[]' <<<"$resp" >> leads.jsonl
    [ "$(jq '.data | length' <<<"$resp")" -eq 0 ] && break
    after=$(jq -r '.pagination.next_after // empty' <<<"$resp")
    sleep 0.7
  done
done
wc -l < leads.jsonl
```

**Step 6: dedupe, rank and cap per company (Bash).** Set the three keys from the step 3 sample. VP titles rank first, as the request lists them first; each company keeps one VP and one Head of Marketing at most.

```bash
cd "$HOME/Leads/cyber-b"
EMAIL=email TITLE=title SITE=company_website
jq -sc --arg e "$EMAIL" --arg t "$TITLE" --arg s "$SITE" '
  map(select((.[$e] // "") != ""))
  | map(. + {_email: (.[$e] | ascii_downcase)})
  | map(. + {_domain: (((.[$s] // "") | ascii_downcase | sub("^https?://"; "") | sub("^www\\."; "") | sub("/.*$"; "")) as $d
                       | if $d == "" then (._email | split("@")[1]) else $d end),
             _rank: (if ((.[$t] // "") | test("vice president|\\bvp\\b"; "i")) then 1 else 2 end)})
  | unique_by(._email)
  | group_by([._domain, ._rank]) | map(.[0])
  | sort_by(._rank, ._domain) | .[]' leads.jsonl > ranked.jsonl
head -n 300 ranked.jsonl | jq -r '._email' > validate_1.txt
wc -l < ranked.jsonl
```

**Step 7: validate the top 300 in one run (paid).** Claude reads `validate_1.txt` and passes its lines as `emails`. Database emails are validated before sending because Alex Berman's B2B lead generation guide says to verify the list and calls a 95%+ valid rate the minimum (alexberman.com/b2b-lead-generation).

```json
{"tool": "validate_emails", "arguments": {"emails": ["LINES_OF_validate_1.txt"]}}
```

**Step 8: status once per turn, then download.**

```json
{"tool": "check_run_status", "arguments": {"runId": "RUN_ID_FROM_STEP_7"}}
{"tool": "download_results", "arguments": {"runId": "RUN_ID_FROM_STEP_7", "outputPath": "/Users/dana/Leads/cyber-b/validated_1.csv"}}
```

**Step 9: cut to 300 and size any top-up (Bash).** Writes `final.csv` (the top 300 `valid` rows in rank order, with `email_status` and `stage_source`), `spares.csv`, `catch_all.csv`, and `next_validate.txt` holding exactly the shortfall from the ranked list.

```bash
cd "$HOME/Leads/cyber-b"
python3 - 300 <<'PY'
import csv, glob, json, sys
from collections import Counter
target = int(sys.argv[1])
status = {}
for f in sorted(glob.glob("validated_*.csv")):
    with open(f, newline="") as fh:
        rows = csv.DictReader(fh)
        col = next((c for c in rows.fieldnames if c.strip().lower() == "email"), None)
        if col is None or "email_result" not in rows.fieldnames:
            sys.exit(f"{f}: header is {rows.fieldnames}; name its email and email_result columns here")
        for r in rows:
            status[r[col].strip().lower()] = r["email_result"].strip()
ranked = [json.loads(line) for line in open("ranked.jsonl")]
fields = []
for r in ranked:
    fields += [k for k in r if not k.startswith("_") and k not in fields]
fields += ["email_status", "stage_source"]
def flat(v):
    return ";".join(map(str, v)) if isinstance(v, list) else json.dumps(v) if isinstance(v, dict) else v
def write(name, rows):
    with open(name, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**{k: flat(v) for k, v in r.items()},
                        "email_status": status[r["_email"]], "stage_source": "your Series B list (domains.txt)"})
checked = [r for r in ranked if r["_email"] in status]
valid = [r for r in checked if status[r["_email"]] == "valid"]
write("final.csv", valid[:target])
write("spares.csv", valid[target:])
write("catch_all.csv", [r for r in checked if status[r["_email"]] == "valid_catch_all"])
print("checked by result:", dict(Counter(status[r["_email"]] for r in checked)))
short = target - min(len(valid), target)
todo = [r["_email"] for r in ranked if r["_email"] not in status][:short]
with open("next_validate.txt", "w") as fh:
    fh.write("".join(e + "\n" for e in todo))
print(f"final.csv: {min(len(valid), target)} of {target}; next_validate.txt: {len(todo)} emails")
PY
```

If `next_validate.txt` is not empty, run steps 7 and 8 on it (saving as `validated_2.csv`) and step 9 again. Each top-up email costs $0.00169, so 40 more is $0.07.

| Step | Tool | Key parameters | Units | Unit price | Cost |
|---|---|---|---:|---:|---:|
| 2 | check_wallet | none | 1 | $0.00 | $0.00 |
| 3-5 | query_lead_database | titles, notTitle, companyCountry, companyDomain batches, hasEmail; count, sample, pull | every match | $0.00 | $0.00 |
| 7 | validate_emails | top 300 ranked emails, one run | 300 | $0.00169 | $0.51 |
| Total | | | | | $0.51 |

Approval: the $0.51 validation waits for your go-ahead after the count, and each top-up batch is shown with its cost and waits for a go-ahead too.

## Issues and Fixes

| Symptom | Cause | Fix |
|---|---|---|
| `claude mcp list` shows Failed to connect; npm 404 for `scrapercity-mcp` | Args missing `--package scrapercity` | `claude mcp remove scrapercity`, then the add command above |
| Every tool returns `Error: No API key` | The entry has no `--env`, or the key was exported after the session started | Add again with `--env SCRAPERCITY_API_KEY=...` and start a new session |
| A database call returns 503 | The search ran too long | Smaller domain batches (`split -l 100`), then retry |

## Next Steps

1. Load `final.csv` into your sequencer; keep `catch_all.csv` in its own campaign so its bounces stay out of the main one.
2. For the next 300, rerun steps 3 to 5 with `"excludeDelivered": true` so leads you already have do not come back, then steps 6 to 9.
