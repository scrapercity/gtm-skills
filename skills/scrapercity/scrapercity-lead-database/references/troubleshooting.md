# Lead Database Troubleshooting

Runbook for every way a `query_lead_database` call goes wrong. Find the symptom, run the check, apply the fix.

## Error codes

| Code | Meaning on this endpoint | Fix |
|---|---|---|
| 400 | The `url` had no filters the database can use, or a parameter could not be read | Rebuild the search with explicit filters. Check the URL is a people search, not a company or saved-list page |
| 401 | Missing or invalid API key | Stop. Ask for a valid key. Check `SCRAPERCITY_API_KEY` or `~/.scrapercityrc` |
| 402 | Wallet balance too low | Run `check_wallet`, report the shortfall, wait for the user |
| 403 | Account cancelled or a charge is processing | Stop and tell the user. Also run `check_wallet`: if `plan.name` is Starter, the database needs Growth ($149/mo) |
| 409 `filters_not_applied_yet` | The company filters named in the response cannot be used yet | Nothing was returned or counted. Retry later, or drop the listed filters and filter the rows yourself |
| 429 | Rate limited (scrapercity.com/api-docs: 100 requests a minute per key) | Wait at least 30 seconds (AGENT_DOCS: a repeat within 30 s is a 429), retry once. Keep paging loops under 100 calls a minute |
| 503 | The search ran too long | Narrow: add a location or a size band, cut the title list, cut keywords. Retry |
| Query refused, no JSON | Query string over about 16KB | Send the same parameters as `POST /api/v1/database/leads` with a JSON body |

## Empty or tiny results

| Symptom | Check | Fix |
|---|---|---|
| `total: 0` | Run the same call without `hasPhone`, then without `revenueMin/Max`, then without `keywords` | Drop the filter that zeroes it. Revenue is missing on some companies |
| `total: 0` with a country | Spelling. Use "United States", "United Kingdom", "Germany". US, USA, UK, UAE also work | Fix the name |
| `total: 0` with `seniority` | The value may not exist in the data | Probe with the loop in `references/filter-semantics.md` |
| `total: 0` with `industry` | Industry string spelling | Read `company_industry` from a sample row for a known company and copy it, or switch to `keywords` |
| Count far below a people-search URL count | `search_translation.not_supported` or `approximated` lists something | Report it. Add explicit filters, or use `scrape_apollo` for that URL |
| Count far above expectation | Person vs company location mix-up, or a short title stem | Swap `country` for `companyCountry`, lengthen title stems, add `notTitle` |

## Sample looks wrong

Pull the sample (for example `limit: 20`) and tally:

| Off-target pattern | Cause | Fix |
|---|---|---|
| Assistants, coordinators, interns | Partial title match | `notTitle: "Assistant, Coordinator, Intern"` |
| Right title, wrong function ("VP Product" in a VP Sales pull) | Stem too short ("VP") | Pair the function word in every stem |
| Agencies in a SaaS pull | Agencies tag themselves "saas" | `notKeywords: ["agency", "consulting"]` |
| People in other countries | Filtered on `companyCountry` only | Add `country` if the person must be local |
| Companies outside the size band | Employee count differs from what the user saw elsewhere | Widen or narrow the band by one step and compare |
| Missing emails | `hasEmail` not set | Set `hasEmail: true` |

Acceptance: the pass mark agreed with the user before the sample, on title, size and geography. Below it, fix and re-run the count.

## Paging problems

| Symptom | Cause | Fix |
|---|---|---|
| Duplicates across pages | Mixed `page` and `after` in one loop | Use one method per loop |
| Missing rows with `excludeDelivered` | Paged with `page=2..N` | Keep `page=1` and loop, or use `after` |
| Loop never ends | Not reading `next_after` | Stop when `next_after` is null or `has_more` is false |
| Daily feed returns 0 new leads | Every match already delivered to this account | The segment is exhausted. Widen geography or size, or add a new segment |
| Feed stops mid-day | Hit 100,000 new leads | Resumes after midnight UTC (per scrapercity.com/api-docs). Save the last cursor |

## Cursor loop template (Python, stdlib)

```python
import json, os, urllib.parse, urllib.request, time

KEY = os.environ["SCRAPERCITY_API_KEY"]
BASE = "https://app.scrapercity.com/api/v1/database/leads"

def fetch(params):
    req = urllib.request.Request(BASE, data=json.dumps(params).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)

params = {"title": "VP Sales, Head of Sales", "companyCountry": ["United States"],
          "minEmployees": 50, "maxEmployees": 200, "hasEmail": "true",
          "excludeDelivered": "true", "limit": 100, "after": "0"}
rows, target = [], 2000
while len(rows) < target:
    page = fetch(params)
    rows += page.get("data", [])
    nxt = page.get("pagination", {}).get("next_after")
    if not nxt:
        break
    params["after"] = str(nxt)
    time.sleep(0.7)  # stays under 100 calls a minute
print(len(rows), "new leads; last cursor", params["after"])
```

On a 503, the loop should catch the HTTP error, narrow the filters, and restart from `after: "0"`. With `excludeDelivered` on, rows already taken are skipped, so restarting costs nothing.

## Lead Database vs Apollo Scraper decisions

| Situation | Choose |
|---|---|
| Growth or Scale plan, filters expressible here | Lead Database |
| Starter plan | `scrape_apollo` at $0.0039 per lead, 500 minimum per run |
| URL depends on a filter in `not_supported` and the user insists on it | `scrape_apollo` with a webhook |
| `scrape_apollo` response shows a `lead_database` block with `matches` | Pull those matches now through the database `api` call, then size the Apollo run to the rest |
| Need results right now | Lead Database. Apollo runs usually take 15 to 30 minutes |

Never poll an Apollo run in a tight loop: start after 15 minutes and check every few minutes. Register a webhook at app.scrapercity.com/dashboard/webhooks.

## Before you report a count to the user

1. The count came from a call with the final filters.
2. The person vs company location choice is written next to each geography filter.
3. Any `search_translation` gaps are listed.
4. The sample QA result and its pass mark are stated.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://docs.apollo.io/reference/people-api-search
