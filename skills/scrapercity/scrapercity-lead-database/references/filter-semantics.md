# Lead Database Filter Semantics

Exact behavior of every `query_lead_database` parameter, taken from the `scrapercity` npm package (1.0.17): `bin/mcp.mjs`, `bin/cli.mjs`, `lib/client.mjs` and `AGENT_DOCS.txt`. Where the source gives examples rather than a full list, this file says so and shows how to check a value with a 1-row call.

## Combining rules

- Values inside one array filter are OR: `industry: ["computer software", "internet"]` matches either.
- Different filters are AND: `industry` plus `seniority` plus `minEmployees` must all hold.
- Exclusions (`notTitle`, `notKeywords`, `notIndustry`) remove rows after the include filters.
- With `url`, the URL's filters are the base and any filter you also send overrides the matching one.

## Parameter reference

| Parameter | Type | Applies to | Matching | CLI flag |
|---|---|---|---|---|
| `url` | string | whole search | A people-search URL. Its filters become the search. Response adds `search_translation` | `--url` |
| `title` | string | person | Partial match. Comma separated for several: `"CEO, Founder"` | `--title` |
| `notTitle` | string | person | Excludes titles containing any listed term, comma separated | `--not-title` |
| `seniority` | string[] | person | Any match. Source examples: `vp`, `director`, `c_suite` | `--seniority` (commas) |
| `department` | string[] | person | Any match. Source examples: `sales`, `engineering` | `--department` (commas) |
| `country` | string[] | person location | Full names like "United States". US, USA, UK, UAE also work | `--country` (commas) |
| `state` | string[] | person location | Any match | `--state` (commas) |
| `city` | string | person location | Comma separated for several | `--city` |
| `socialUrl` | string | person | Match a social profile URL | none (MCP and REST) |
| `hasEmail` | boolean | person | Only contacts with an email | `--has-email` |
| `hasPhone` | boolean | person | Only contacts with a phone | `--has-phone` |
| `companyName` | string | company | Company name | `--company` |
| `companyDomain` | string | company | Domain or domains, comma separated | `--domain` |
| `industry` | string[] | company | Any match. Docs example: `computer software` | `--industry` (commas) |
| `notIndustry` | string[] | company | Excludes these industries | `--not-industry` (commas) |
| `keywords` | string[] | company | Company keywords and tags. Whole word, any match | `--keywords` |
| `notKeywords` | string[] | company | Excludes companies with any of these keywords | `--not-keywords` |
| `minEmployees` | number | company | Minimum employee count | `--min-employees` |
| `maxEmployees` | number | company | Maximum employee count | `--max-employees` |
| `revenueMin` | number | company | Minimum annual revenue, USD | `--revenue-min` |
| `revenueMax` | number | company | Maximum annual revenue, USD | `--revenue-max` |
| `companyCountry` | string[] | company HQ | HQ country, not where the person is | `--company-country` (commas) |
| `companyState` | string[] | company HQ | HQ state | `--company-state` (commas) |
| `companyCity` | string | company HQ | HQ city | `--company-city` |
| `page` | number | paging | Default 1. Keep at 1 when `excludeDelivered` is on | `--page` |
| `limit` | number | paging | Max 100. MCP default 50 | `--limit` |
| `excludeDelivered` | boolean | paging | Skip leads this account already has, from the API or unlocked in the dashboard | `--exclude-delivered` |
| `after` | string | paging | Cursor in id order. Send `"0"` first, then `pagination.next_after` | `--after` |

On REST, booleans go as the string `true`. The MCP and CLI convert for you.

## Person location vs company HQ

| User says | Filter |
|---|---|
| "US companies", "companies headquartered in Germany" | `companyCountry` |
| "Companies in Texas" | `companyState` |
| "Companies based in Austin" | `companyCity` |
| "People in the US", "reps located in the UK" | `country` |
| "People who live in California" | `state` |
| "People in Chicago" | `city` |
| "US-based people at US companies" | `country` and `companyCountry` both |
| "Remote reps in the US at any company" | `country` only |

A company with HQ in New York and sales reps in Denver: `companyState: ["New York"]` returns the Denver reps. `state: ["Colorado"]` also returns them. Pick the one the user means, and when in doubt, ask.

## Title matching

- Partial match means `"CEO"` also matches longer titles that contain it, such as "CEO and Co-Founder".
- Short stems pull unrelated titles. `"VP"` matches every VP in every function. Pair a function word: `"VP Sales, VP of Sales, Vice President Sales, Vice President of Sales"`.
- `"Owner"` matches "Product Owner". Add `notTitle: "Product Owner"` for small-business owner pulls.
- `"Director"` matches "Art Director" and "Director of First Impressions". Use `department` or a function word.
- `notTitle` is the cleanup tool. A standard exclusion list for sales leadership pulls: `"Assistant, Intern, Coordinator, Executive Assistant, Operations"`.
- Keep the title list under about 25 stems. Long lists slow the search and invite a 503.

## Keyword matching

- `keywords` match company tags as whole words, any match. `["saas"]` does not match "saasy".
- Use 2-6 keywords that describe the business model, not the buyer's pain. `["saas", "b2b"]`, `["ecommerce", "dtc"]`, `["fintech", "payments"]`.
- `notKeywords` removes adjacent categories: a SaaS pull with `notKeywords: ["agency", "consulting", "staffing"]` drops service firms that tag themselves with software words.
- The CLI `--keywords` flag passes the string as typed; REST also accepts commas (`keywords=saas,fintech`).

## Seniority values

Confirmed in the ScraperCity source as examples: `vp`, `director`, `c_suite`.

People-search URLs from Apollo.io carry this vocabulary (Apollo People API docs): `owner`, `founder`, `c_suite`, `partner`, `vp`, `head`, `director`, `manager`, `senior`, `entry`, `intern`.

The ScraperCity source does not publish a complete list. Before using any value outside the three confirmed examples in a big pull, verify it:

```bash
for s in owner founder c_suite partner vp head director manager senior entry intern; do
  printf "%s " "$s"
  curl -s -G "https://app.scrapercity.com/api/v1/database/leads" \
    -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
    --data-urlencode "seniority=$s" --data-urlencode "companyCountry=United States" \
    --data-urlencode "minEmployees=50" --data-urlencode "maxEmployees=200" \
    --data-urlencode "limit=1" | python3 -c "import sys,json; print(json.load(sys.stdin).get('pagination',{}).get('total'))"
done
```

A value that returns 0 on a broad US search is not a value the database uses. Each probe returns one lead, which the account then owns; 11 probes add at most 11 leads.

## Department values

Confirmed in the ScraperCity source as examples: `sales`, `engineering`.

No complete list is published in the package. Probe candidate values the same way as seniority (swap `seniority=$s` for `department=$d`) before relying on them. Probe these candidates first: `marketing`, `finance`, `human_resources`, `operations`, `information_technology`, `legal`, `product_management`, `customer_success`. Keep only the ones that return a non-zero total, and record them in the pull plan.

When a department value cannot be confirmed, use title stems instead. `title: "Marketing"` with `notTitle: "Assistant, Intern, Coordinator"` covers the marketing department without depending on a department label.

## Industry values

The docs example is `computer software`. Industry strings must match what the data holds. The fastest way to learn the spelling: run a `limit: 5` call with `companyDomain` set to two or three known companies in the target industry, and read `company_industry` on the returned rows. Use those exact strings.

## Size and revenue

- `minEmployees` and `maxEmployees` are inclusive bands on company employee count. Bands used in the cookbook: 1-10, 11-50, 51-200, 201-1,000, 1,001-5,000, 5,001+.
- `revenueMin` and `revenueMax` are annual revenue in USD: `revenueMin: 10000000` is $10M.
- Revenue is missing on some companies. Adding a revenue filter drops companies with no revenue value. If the count falls sharply, try employees alone.

## search_translation

Sent when `url` is used:

```json
"search_translation": {
  "applied": ["person titles", "person locations"],
  "approximated": ["organization employee ranges"],
  "not_supported": ["technologies"]
}
```

The list items above are an illustration of the shape. Read each list in the live response:

- `applied`: no action.
- `approximated`: tell the user what the closest match was and check the sample.
- `not_supported`: the count ignores these. If one defines the ICP, add the closest explicit filter yourself (for example `keywords`) or use `scrape_apollo` for that URL.

A URL with nothing usable returns 400.

## Response pagination block

| Field | Meaning |
|---|---|
| `page`, `limit` | What was sent |
| `total` | Matching leads for the filters (use for the count check) |
| `totalPages` | `total / limit` rounded up |
| `has_more` | More rows after this page |
| `next_after` | Cursor to send as `after`. Null when there is nothing left |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://docs.apollo.io/reference/people-api-search
