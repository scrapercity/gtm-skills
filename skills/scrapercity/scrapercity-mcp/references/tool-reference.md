# Tool Reference: All 25 ScraperCity MCP Tools

The server in `scrapercity` 1.0.17 lists 25 tools: 7 utility and database tools and 18 scrapers. Names, arguments and prices below come from `references/scrapercity-catalog.md` and the package's tool schemas. When the catalog and scrapercity.com/pricing disagree, the live site wins.

## Utility and database tools

| Tool | Arguments | Cost | Use it when | Do not use it when |
|---|---|---|---|---|
| `check_wallet` | none | Free | First call of every session and before every paid run | Never skip it |
| `list_runs` | `hours` (default 24, max 168), `limit` (default 20, max 100) | Free | Finding a `runId` after a 409, a timeout, or a lost conversation | You already hold the `runId` |
| `check_run_status` | `runId` | Free | Once per turn while a run is RUNNING | Back to back in one turn; Apollo more than once an hour |
| `download_results` | `runId`, `outputPath` (absolute) | Free | The status is SUCCEEDED | Status is RUNNING, FAILED or CANCELLED |
| `cancel_run` | `runId` | Free | Wrong inputs spotted after start, or the user wants to stop spend | The run already finished |
| `query_lead_database` | filters, `url`, `page`, `limit` (max 100, default 50), `after`, `excludeDelivered` | $0 wallet on Growth and Scale, 100,000 new leads a day | B2B people by title, seniority, department, industry, size, revenue, location | Starter plan; or you need one person at a named account (use `find_emails` or `scrape_website_finder`) |
| `query_local_business_database` | `keyword`, `location`, `url`, `category`, `country`, `state`, `city`, `postalCode`, `box`, `query`, `title`, rating and review bounds, `has*` flags, `page`, `limit`, `after`, `excludeDelivered` | $0 wallet on Growth and Scale, 100,000 new businesses a day | Local businesses by what they do and where | Starter plan; or the target is a person by title (use the Lead Database) |

Database rules that trip agents:

- Count with `limit: 1` and read `pagination.total`. Inspect with `limit: 10`. Pull with `limit: 100` and `after`.
- `excludeDelivered: true` goes with `after` or `page: 1`, never with `page` above 1.
- `query_lead_database`: `country`, `state`, `city` are where the person lives; `companyCountry`, `companyState`, `companyCity` are the company HQ.
- `query_local_business_database`: `country` takes two-letter codes (`["US"]`), unlike the Lead Database's full names.
- A `url` (people-search URL or Google Maps search URL) becomes the search; read `search_translation` for what was applied, approximated or not supported.

Full filter semantics live in `scrapercity-lead-database` and `scrapercity-local-business-database`.

## Scraper and enrichment tools

| Tool | Required arguments | Price (catalog) | Billable ceiling | Published delivery time |
|---|---|---|---|---|
| `scrape_apollo` | `url` (Apollo people search, Filters 1.0); `count` 500-50,000 | $0.0039 per lead | `count` x $0.0039 | Up to 4 days; webhook, or check at most hourly |
| `scrape_website_finder` | `domains[]`, `jobTitle` (one per request) | $0.0499 per contact found | domains x $0.0499 | 5-15 min |
| `find_people` | one of `name[]`, `email[]`, `phone_number[]`, `street_citystatezip[]`; `max_results` | $0.0199 per result (0 matches billed as 1) | searches x max(`max_results`, 1) x $0.0199 | 2-10 min |
| `scrape_distress_list` | `search` (city + state or ZIP); `distressTypes[]`, `maxItems` 1-500 | $0.05 per property | `maxItems` x $0.05 | 1-30 min (README range) |
| `validate_emails` | `emails[]` | $0.0072 per email | unique emails x $0.0072 | 1-10 min |
| `scrape_maps` | `searchStringsArray[]` + `locationQuery`, or `url`; `maxCrawledPlacesPerSearch` | $0.0099 per business | terms x max places x $0.0099 | 5-30 min |
| `scrape_airbnb` | `mode` and `city[]` ("City, Country", Europe only) or `listingUrl` or `bulkListings[]` | $0.019 per result | Test a small `maxPages` first | 10-30 min |
| `scrape_bizbuysell` | `startUrls[]`; `maxItems` | $0.0099 per listing | `maxItems` x $0.0099 | 5-15 min |
| `scrape_crexi` | `startUrls[]` (property search, city or market search, or broker directory) | $0.029 per property | Not capped by a parameter; test one URL | 5-15 min |
| `scrape_angi` | `keyword` (a service slug such as `roofing`, `hvac`, `plumbing`); `zipCodes[]`, `maxItems` | $0.0099 per listing | `maxItems` x $0.0099 | 5-15 min |
| `scrape_yelp` | `searchTerms[]` + `locations[]`, or `directUrls[]`; `searchLimit` | $0.0099 per result | terms x locations x `searchLimit` x $0.0099 | 5-15 min |
| `scrape_zillow_agents` | `location`; `specialty`, `language`, `searchLimit` 1-500 | $0.029 per agent | `searchLimit` x $0.029 | 5-15 min |
| `scrape_property_lookup` | `addresses[]`; `includeOwnerContact` | $0.15 per property, +$0.10 with owner contact | addresses x $0.15 (or $0.25) | 2-10 min |
| `search_criminal_records` | `name` (one per request); `state`, `dob` | $1.00 per search with records found, free when none | searches x $1.00 | 2-5 min |
| `scrape_store_leads` | filters; `totalLeads`, `offset` | $0.0039 per lead | `totalLeads` x $0.0039 | Instant |
| `scrape_builtwith` (Tech Stack Search) | `technology` | $4.99 per technology | technologies x $4.99 | 1-5 min |
| `find_emails` | `contacts[]` of `first_name`, `last_name` or `full_name`, plus `domain` or `company_name` | $0.05 per email found, free if not found | contacts x $0.05 | 1-10 min |
| `find_mobiles` | `inputs[]` (social profile URLs or work emails) | $0.25 per number found, free if not found | inputs x $0.25 | 1-5 min |

Delivery times come from the package's AGENT_DOCS. In a conversation, check status once per turn and report a run still `RUNNING` past the top of its range. See the polling schedule in `references/scrapercity-agent-patterns.md`.

## Decision table: request to tool

| The user says | Plan on Growth or Scale | Plan on Starter |
|---|---|---|
| "VP Sales at US SaaS, 50-200 employees" | `query_lead_database` | `scrape_apollo` with the user's Apollo URL |
| "Here is my Apollo search URL" | `query_lead_database` with `url`, check `search_translation`; `scrape_apollo` only for `not_supported` filters the ICP needs | `scrape_apollo` |
| "Dentists in Austin with emails" | `query_local_business_database` `keyword: ["dentist"], location: ["Austin TX"], hasEmail: true` | `scrape_maps`, then `validate_emails` |
| "Plumbers in these ZIP codes" | `query_local_business_database` with `location` set to the ZIPs | `scrape_angi` `keyword: "plumbing"`, `zipCodes` |
| "Restaurants with Yelp ratings" | `query_local_business_database` with `minRating` | `scrape_yelp` |
| "Find the CEO at these 300 domains" | `query_lead_database` `companyDomain` + `seniority: ["c_suite"]` first, then `scrape_website_finder` for misses | `scrape_website_finder` `jobTitle: "CEO"` |
| "I have names and companies, need emails" | `find_emails` | `find_emails` |
| "Clean this list before I send" | `validate_emails` | `validate_emails` |
| "Mobile numbers for these LinkedIn profiles" | `find_mobiles` | `find_mobiles` |
| "Shopify stores in the US doing over 50k visits a month" | `scrape_store_leads` `platform: "shopify"`, `countryCode: "US"`, `minEstimatedMonthlyVisits: 50000` | same |
| "Every site running Klaviyo" | `scrape_builtwith` `technology: "Klaviyo"` ($4.99) | same |
| "Realtors in Denver" | `scrape_zillow_agents` `location: "Denver, CO"` | same |
| "Who owns 123 Main St and what is it worth" | `scrape_property_lookup` with `includeOwnerContact: true` ($0.25) | same |
| "Pre-foreclosures in Tampa" | `scrape_distress_list` `search: "Tampa, FL"`, `distressTypes: ["preForeclosure"]` | same |
| "Businesses for sale in Texas" | `scrape_bizbuysell` with a BizBuySell search URL | same |
| "Airbnb hosts in Lisbon" | `scrape_airbnb` `mode: "city"`, `city: ["Lisbon, Portugal"]` | same |
| "Find this person's phone and address" | `find_people` with `max_results: 1`; confirm the returned name and address match before using the contact | same |
| "Does this person have a record" | `search_criminal_records` with `state` and `dob` to narrow the match ($1.00 only when records are found) | same |

## Argument recipes

```json
{"tool": "query_lead_database", "arguments": {"title": "VP Sales, Head of Sales", "notTitle": "Assistant, Intern", "companyCountry": ["United States"], "minEmployees": 50, "maxEmployees": 200, "keywords": ["saas"], "hasEmail": true, "limit": 1}}
{"tool": "query_local_business_database", "arguments": {"keyword": ["hvac contractor"], "location": ["Phoenix AZ"], "hasEmail": true, "excludeDelivered": true, "after": "0", "limit": 100}}
{"tool": "scrape_apollo", "arguments": {"url": "https://app.apollo.io/#/people?...", "count": 2000, "fileName": "apollo-vp-sales-us-20261013"}}
{"tool": "find_emails", "arguments": {"contacts": [{"first_name": "Dana", "last_name": "Lee", "domain": "acme.com"}]}}
{"tool": "find_mobiles", "arguments": {"inputs": ["linkedin.com/in/danalee", "dana@acme.com"]}}
{"tool": "scrape_website_finder", "arguments": {"domains": ["acme.com", "globex.com"], "jobTitle": "Head of Marketing", "autoValidateEmails": true}}
{"tool": "scrape_store_leads", "arguments": {"platform": "shopify", "countryCode": "US", "emails": true, "minEstimatedMonthlyVisits": 50000, "totalLeads": 100, "offset": 0}}
{"tool": "scrape_property_lookup", "arguments": {"addresses": ["123 Main St, Denver, CO 80202"], "includeOwnerContact": true}}
{"tool": "search_criminal_records", "arguments": {"name": "John Smith", "state": "CA", "dob": "02/07/1992"}}
```

## Start responses that save money

| Tool | Field in the start response | What to do |
|---|---|---|
| `scrape_apollo` | `lead_database: { matches, url, api }` | Leads with the same filters already in the Lead Database that the account does not have. On Growth, pull those first and size the Apollo run to the remainder. |
| `scrape_maps` | `local_business_database: { matches, url, api }` | Same idea for local businesses. |
| `scrape_store_leads` | `nextOffset` | Send it back as `offset` for the next page, so repeat calls do not return the same first page. |

## Results the agent did not get

| Result | What the agent reports | What it never does |
|---|---|---|
| `find_emails` returns no email for a contact | "Not found", no charge | Builds `first.last@domain` or any other pattern address |
| `find_mobiles` returns no number | "Not found", no charge | Uses the business line as if it were the person's mobile |
| `find_people` returns a different name or address than the input | "Possible match, unconfirmed" with both values side by side | Treats it as the person |
| A database query returns `pagination.total` 0 | The count and the filters used, then one widening suggestion | Silently drops a filter and pulls a broader list |
| A run ends `FAILED` | `statusMessage` and the first lines of the logs | Resubmits the same inputs |

## Bulk people pull: the scripts a report writes out

A report that pulls more than one database page carries these steps in full, adapted to the job (titles, folder, target, the attribute column). Every step was run against sample data; the shell parts need `jq` and Python 3, and the loop needs curl 7.76 or newer for `--fail-with-body`.

**Company list into batches.** A company list the user supplies (funding stage, a named-account list) becomes `companyDomain`, comma separated. Batches of 200 keep each request far under the 16KB query limit.

```bash
mkdir -p "$HOME/Leads/JOB" && cd "$HOME/Leads/JOB"
tr -d '\r' < domains.txt | tr 'A-Z' 'a-z' | sed -E 's#^https?://##; s#^www\.##; s#/.*$##' | grep -v '^$' | sort -u > domains.clean.txt
split -l 200 domains.clean.txt batch_
for f in batch_??; do paste -sd, "$f" > "$f.csv"; done
```

**The pull through MCP.** One `query_lead_database` call per page: `limit: 100`, `after: "0"` first, then each `pagination.next_after` until it is null, per batch. In Claude Code a page over 25,000 tokens or 50,000 characters arrives as a saved file the agent reads; a smaller page lands in the chat, and the agent appends each page's `data` rows to `leads.jsonl`. If page 1 lands in the chat with the 10,000-token warning, the rest goes through the loop below. Leave `excludeDelivered` off for a one-off list, since re-fetching leads the account owns is free and dropping them shrinks the list; turn it on for repeat pulls.

**The shell fallback.** Same filters as query strings, so there is no JSON type to mismatch. `sleep 0.7` keeps one key under 100 requests a minute (scrapercity.com/api-docs).

```bash
cd "$HOME/Leads/JOB"
: > leads.jsonl
for b in batch_??.csv; do
  after=0
  while [ -n "$after" ]; do
    resp=$(curl -sS --fail-with-body -G "https://app.scrapercity.com/api/v1/database/leads" \
      -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
      --data-urlencode "title=VP Sales, Head of Sales" --data-urlencode "notTitle=Assistant, Intern" \
      --data-urlencode "companyCountry=United States" --data-urlencode "companyDomain=$(cat "$b")" \
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

Without a company list, drop the `for` loop and the `companyDomain` line.

**Dedupe, rank, cap.** Set the three keys from the 10-row sample. `_rank` follows the order the request names the roles in (here VP first); the per-company cap is the user's, and when they gave none it is one contact per role named. The email's domain stands in when the website field is blank.

```bash
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
head -n TARGET ranked.jsonl | jq -r '._email' > validate_1.txt
```

Replace `TARGET` with the number the user asked for. The agent then reads `validate_1.txt` and passes its lines as `emails` in one `validate_emails` call, and downloads the result to `validated_1.csv` in the same folder by its absolute path.

**Join, cut, top up.** The validator's result column is `email_result` (scrapercity.com/email-validator); the script stops and prints the header if the columns differ. It writes the target count of `valid` rows in rank order, the spares, the catch-all rows, and `next_validate.txt` holding exactly the shortfall from the ranked list. The `stage_source` value names where the attribute the database could not filter on came from.

```bash
python3 - TARGET <<'PY'
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
                        "email_status": status[r["_email"]], "stage_source": "user's company list"})
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

A non-empty `next_validate.txt` goes through one more `validate_emails` run (saved as `validated_2.csv`), then the script runs again. The cost of a top-up is its line count x $0.0072, shown before it starts. This replaces a guessed over-pull buffer: the plan prices the target count, and each top-up is priced from the real shortfall.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/pricing
- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://scrapercity.com/email-validator
- https://code.claude.com/docs/en/mcp
