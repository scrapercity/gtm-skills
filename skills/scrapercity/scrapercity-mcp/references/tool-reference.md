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

| Tool | Required arguments | Price (catalog) | Billable ceiling | Status check cadence |
|---|---|---|---|---|
| `scrape_apollo` | `url` (Apollo people search, Filters 1.0); `count` 500-50,000 | $0.0039 per lead | `count` x $0.0039 | Webhook; at most hourly |
| `scrape_website_finder` | `domains[]`, `jobTitle` (one per request) | $0.0499 per contact found | domains x $0.0499 | 2 min |
| `find_people` | one of `name[]`, `email[]`, `phone_number[]`, `street_citystatezip[]`; `max_results` | $0.0199 per result (0 matches billed as 1) | searches x max(`max_results`, 1) x $0.0199 | 2 min |
| `scrape_distress_list` | `search` (city + state or ZIP); `distressTypes[]`, `maxItems` 1-500 | $0.05 per property | `maxItems` x $0.05 | 2 min |
| `validate_emails` | `emails[]` | $0.0072 per email | unique emails x $0.0072 | 30 s |
| `scrape_maps` | `searchStringsArray[]` + `locationQuery`, or `url`; `maxCrawledPlacesPerSearch` | $0.0099 per business | terms x max places x $0.0099 | 2 min |
| `scrape_airbnb` | `mode` and `city[]` ("City, Country", Europe only) or `listingUrl` or `bulkListings[]` | $0.019 per result | Test a small `maxPages` first | 2 min |
| `scrape_bizbuysell` | `startUrls[]`; `maxItems` | $0.0099 per listing | `maxItems` x $0.0099 | 2 min |
| `scrape_crexi` | `startUrls[]` (property search, city or market search, or broker directory) | $0.029 per property | Not capped by a parameter; test one URL | 2 min |
| `scrape_angi` | `keyword` (a service slug such as `roofing`, `hvac`, `plumbing`); `zipCodes[]`, `maxItems` | $0.0099 per listing | `maxItems` x $0.0099 | 2 min |
| `scrape_yelp` | `searchTerms[]` + `locations[]`, or `directUrls[]`; `searchLimit` | $0.0099 per result | terms x locations x `searchLimit` x $0.0099 | 2 min |
| `scrape_zillow_agents` | `location`; `specialty`, `language`, `searchLimit` 1-500 | $0.029 per agent | `searchLimit` x $0.029 | 2 min |
| `scrape_property_lookup` | `addresses[]`; `includeOwnerContact` | $0.15 per property, +$0.10 with owner contact | addresses x $0.15 (or $0.25) | 2 min |
| `search_criminal_records` | `name` (one per request); `state`, `dob` | $1.00 per search with records found, free when none | searches x $1.00 | 30 s |
| `scrape_store_leads` | filters; `totalLeads`, `offset` | $0.0039 per lead | `totalLeads` x $0.0039 | 30 s |
| `scrape_builtwith` (Tech Stack Search) | `technology` | $4.99 per technology | technologies x $4.99 | 30 s |
| `find_emails` | `contacts[]` of `first_name`, `last_name` or `full_name`, plus `domain` or `company_name` | $0.05 per email found, free if not found | contacts x $0.05 | 30 s |
| `find_mobiles` | `inputs[]` (social profile URLs or work emails) | $0.25 per number found, free if not found | inputs x $0.25 | 30 s |

Cadence column: first status check after that interval, then the same interval, one check per conversation turn. See the polling schedule in `references/scrapercity-agent-patterns.md`.

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
| "Find this person's phone and address" | `find_people` (public records; see compliance below) | same |
| "Does this person have a record" | `search_criminal_records` (never for hiring, tenant, credit or insurance decisions) | same |

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

## Compliance boundary

`find_people`, `scrape_property_lookup` and `search_criminal_records` return public-record data. Use them for prospecting and research only. Decisions on employment, tenancy, credit or insurance fall under the FCRA in the US and are out of scope. Calling or texting numbers from `find_mobiles` falls under the TCPA and Do Not Call rules. See `references/scrapercity-platform.md` and `references/outbound-compliance-primer.md` at the repo root.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/pricing
- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act
- https://www.fcc.gov/general/telemarketing-and-robocalls
