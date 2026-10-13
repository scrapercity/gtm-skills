# ScraperCity REST Endpoint Reference

Every endpoint the published `scrapercity` npm package (version 1.0.17) calls, with request and response shapes. HTTP behavior is taken from `lib/client.mjs`; request bodies from the generated tool schemas in `references/scrapercity-catalog.md`; response fields from `AGENT_DOCS.txt` and the fields the CLI reads. Prices come only from `references/scrapercity-catalog.md`. When a field is not listed here, treat it as optional and read it defensively.

## Conventions

| Item | Value |
|---|---|
| Host | `https://app.scrapercity.com` |
| API prefix | `/api/v1` for everything except downloads |
| Download prefix | `/api/downloads/{runId}` (no `/v1`) |
| Auth header | `Authorization: Bearer <api key>` on every call, downloads included |
| Body | `Content-Type: application/json` on POST |
| Responses | JSON, except downloads (CSV bytes) |
| Error body | JSON with `error` or `message`; the package shows `error` first, then `message`, then `HTTP <code>` |
| Key location | app.scrapercity.com/dashboard/api-docs |
| Rate limits | 100 requests a minute per key, 10 scrapes running at once (scrapercity.com/api-docs) |
| Result storage | 48 hours after a run finishes (scrapercity.com/api-docs) |
| Database cap | 100,000 new records a day per database, resets midnight UTC |

## Account

### `GET /api/v1/wallet`

No parameters. Response fields the package reads:

```json
{
  "email": "you@company.com",
  "wallet": { "total_balance_dollars": 120.5, "balance_dollars": 100, "purchased_credits_dollars": 20.5 },
  "plan": { "name": "Growth", "limit_dollars": 159, "used_dollars": 38.6, "usage_percent": 24 },
  "billing": { "next_billing_date": "2026-11-01" }
}
```

`total_balance_dollars` is what a run can spend now. `plan.name` tells you whether the database endpoints are open (Growth and Scale).

### `GET /api/v1/runs?hours=24&limit=50`

`hours` up to 168, `limit` up to 100. Response: `{ "runs": [ { "run_id", "status", "handled", "url", "file_name", "created_at", "price_per_lead_micro" } ] }`. The CLI computes a run's cost as `handled x price_per_lead_micro / 1,000,000`. Use this list to find an earlier run after a 409, a 429 or a lost POST response, and for the hourly sweep that backs up webhooks.

### `GET /api/v1/apollo-status`

Response: `{ "status": "url-based" | "legacy", "message", "timestamp" }`. `url-based` means the Apollo URL endpoint is available. Call it before a large `scrape_apollo` batch.

## Run lifecycle

| Step | Method and path | Response |
|---|---|---|
| Start | `POST /api/v1/scrape/{slug}` | `{ runId, ... }` plus tool-specific fields below |
| Status | `GET /api/v1/scrape/status/{runId}` | `{ status, statusMessage, handled, requested, outputUrl }` |
| Download | `GET /api/downloads/{runId}` | CSV bytes |
| Cancel | `POST /api/v1/scrape/cancel/{runId}` | JSON message |
| Logs | `GET /api/v1/scrape/logs/{runId}` | JSON with the run log (the CLI prints `log` or `logs`) |

Status values: `RUNNING`, then exactly one of `SUCCEEDED`, `FAILED`, `CANCELLED`.

| Status | `outputUrl` | Next call |
|---|---|---|
| `RUNNING` | absent or null | Check again on the schedule for that tool |
| `SUCCEEDED` | `/api/downloads/{runId}` | Download now; results are stored for 48 hours |
| `FAILED` | absent | Read `statusMessage`, then the logs, before changing inputs |
| `CANCELLED` | absent | Nothing to download. A cancelled `scrape_store_leads` job can be continued with `resumeFromLead` |

`handled / requested` is the progress figure to show the user. The download only works on `SUCCEEDED`; any other state returns a non-2xx code.

## Scraper start endpoints

All are `POST /api/v1/scrape/{slug}` with a JSON body. Required fields are marked. The tool id is what the MCP server calls the same endpoint.

| Slug | Tool id | Body (required in bold) | Price |
|---|---|---|---|
| `apollo` | `scrape_apollo` | **`url`** (Apollo people search, Filters 1.0), `count` (500 to 50,000), `fileName` (max 50 chars) | $0.0039 per lead |
| `maps` | `scrape_maps` | `searchStringsArray`, `locationQuery`, `customGeolocation`, `maxCrawledPlacesPerSearch`, or `url` (a Google Maps search link) | $0.0099 per business |
| `email-validator` | `validate_emails` | **`emails`** (string array) | $0.0072 per email |
| `email-finder` | `find_emails` | **`contacts`** (objects with `first_name`, `last_name`, `domain`, optional `full_name`, `company_name`); the package also sends `autoValidateEmails`, `autoFindMobiles` | $0.05 per email found, free if not found |
| `mobile-finder` | `find_mobiles` | **`inputs`** (social profile URLs or work emails) | $0.25 per number found, free if not found |
| `skip-trace` | `find_people` | `name`, `email`, `phone_number`, `street_citystatezip` (all string arrays), `max_results` | $0.0199 per result, 0 matches billed as 1 |
| `website-finder` | `scrape_website_finder` | **`domains`**, **`jobTitle`** (one title), `autoValidateEmails`, `autoFindMobiles` | $0.0499 per contact found |
| `store-leads` | `scrape_store_leads` | `platform`, `totalLeads`, `offset`, `countryCode`, `state`, `city`, `category`, `technologies`, `apps`, `emails`, `phones`, social flags, `planExclude`, visit, sales and employee bounds, `resumeFromLead`, `fileName` | $0.0039 per lead |
| `techstack` | `scrape_builtwith` (Tech Stack Search) | **`technology`**, `fileName` (max 50 chars) | $4.99 per technology |
| `yelp-scraper` | `scrape_yelp` | `searchTerms`, `locations`, `searchLimit`, or `directUrls` | $0.0099 per result |
| `angi-angies-list-scraper` | `scrape_angi` | **`keyword`** (Angi slug, see catalog), `zipCodes`, `maxItems` | $0.0099 per listing |
| `zillow-agents` | `scrape_zillow_agents` | **`location`**, `specialty`, `language`, `searchLimit` (1 to 500) | $0.029 per agent |
| `property-lookup` | `scrape_property_lookup` | **`addresses`** (full street, city, state, ZIP), `includeOwnerContact`, `fileName` | $0.15 per property, +$0.10 with owner contact |
| `distress-list` | `scrape_distress_list` | **`search`** (city and state, or ZIP), `distressTypes`, `maxItems` (1 to 500) | $0.05 per property |
| `crexi-scraper` | `scrape_crexi` | **`startUrls`** (Crexi property search, city or market search, or broker directory URL) | $0.029 per property |
| `bizbuysell-scraper` | `scrape_bizbuysell` | **`startUrls`**, `maxItems`, `datasetName` | $0.0099 per listing |
| `airbnb-email` | `scrape_airbnb` | `mode` (`city`, `single`, `bulk`), `city` ("City, Country", Europe only), `listingUrl`, `bulkListings`, `maxPages`, `checkin`, `checkout`, `onlyProHosts`, `onlyUniqueEmails` | $0.019 per result |
| `criminal-records` | `search_criminal_records` | **`name`** (one per request), `state`, `dob` | $1.00 per search with records found, free when none |

Note the two slugs that differ from their tool names: Tech Stack Search posts to `/api/v1/scrape/techstack`, and People Finder posts to `/api/v1/scrape/skip-trace`.

### Start response fields

Every start returns `runId`. Extra fields the package documents or reads:

| Slug | Extra fields |
|---|---|
| `apollo` | `message`; `lead_database: { matches, url, api }` when the Lead Database already holds leads for the same filters that the account does not have |
| `maps` | `datasetId`, `priceMicro`; `local_business_database: { matches, url, api }` when the Local Business Database has the same search |
| `email-validator` | `emailCount`, `estimatedCost` |
| `email-finder` | `contactCount`, `priceMicro` |
| `mobile-finder` | `inputCount`, `priceMicro` |
| `skip-trace` | `totalSearches`, `estimatedCost` |
| `store-leads` | `totalLeads`, `estimatedCost`; the catalog says responses also return `nextOffset` for paging |
| `techstack` | `technology`, `estimatedCost` |
| `criminal-records` | `name`, `state` |

When `lead_database` or `local_business_database` comes back, compare `matches` with the requested count before letting a paid run continue. On Growth or Scale, the database call in `api` returns those records with no wallet charge.

### Example bodies

```json
{ "url": "https://app.apollo.io/#/people?personTitles[]=vp%20sales&personLocations[]=United%20States", "count": 2000, "fileName": "apollo-vp-sales-us-20261013" }
```

```json
{ "searchStringsArray": ["roofing contractor"], "locationQuery": "Denver, CO", "maxCrawledPlacesPerSearch": 200 }
```

```json
{ "contacts": [ { "first_name": "Dana", "last_name": "Ruiz", "domain": "example.com" } ], "autoValidateEmails": true, "autoFindMobiles": false }
```

```json
{ "platform": "shopify", "countryCode": "US", "emails": true, "totalLeads": 100, "offset": 0, "minEstimatedMonthlyVisits": 10000 }
```

## Databases (Growth plan and up)

| Database | Endpoint | Methods |
|---|---|---|
| Lead Database | `/api/v1/database/leads` | GET with query string, or POST with JSON body |
| Local Business Database | `/api/v1/database/local-businesses` | GET with query string, or POST with JSON body |
| Ecommerce Database | `/api/v1/database/ecommerce` | GET with query string (the package has no POST path for it) |

### Shared parameters

| Parameter | Meaning |
|---|---|
| `limit` | Records per call, max 100 |
| `page` | Page number, starts at 1 |
| `after` | Cursor: send `0` first, then each response's `pagination.next_after` until it is null |
| `excludeDelivered=true` | Only records this account does not already have. Keep `page=1` or use `after` |
| `url` | A saved search URL whose filters become the search. The response adds `search_translation: { applied, approximated, not_supported }`. A URL with nothing usable returns 400 |

GET arrays use repeated keys (`?seniority=vp&seniority=director`). In a POST body, arrays are JSON arrays. Booleans go as the string `"true"`, the way the package sends them.

### Lead Database filters

`title`, `industry`, `country`, `state`, `city`, `companyName`, `companyDomain`, `seniority`, `department`, `hasEmail`, `hasPhone`, `minEmployees`, `maxEmployees`, `socialUrl`; company filters `keywords`, `revenueMin`, `revenueMax`, `companyCountry`, `companyState`, `companyCity`; exclusions `notTitle`, `notKeywords`, `notIndustry`. Country takes full names ("United States"); US, USA, UK and UAE also work. Full semantics: the `scrapercity-lead-database` skill.

### Local Business Database filters

`keyword` and `location` (repeat each; location up to 2,000 places), `category`, `notCategory`, `country` (two-letter codes), `state`, `city`, `postalCode`, `box` (`minLat,minLng,maxLat,maxLng`), `query`, `title` (business name), `minRating`, `maxRating`, `minReviews`, `maxReviews`, `hasEmail`, `hasPhone`, `hasWebsite`, `hasContact`. Full semantics: the `scrapercity-local-business-database` skill.

### Database response

```json
{
  "data": [ { "...": "one record per element" } ],
  "pagination": { "page": 1, "limit": 100, "total": 18420, "totalPages": 185, "has_more": true, "next_after": "8812345" },
  "rate_limit": { },
  "search_translation": { "applied": [], "approximated": [], "not_supported": [] }
}
```

Local Business responses can add `searched_as` (how each keyword and place was read) and, on an empty search, `lead_database: { count, read_as, filters, dashboard_url }` when the Lead Database has 100+ people for it. Log `rate_limit` as returned; its fields are not documented.

Record fields documented in the package:

| Database | Fields |
|---|---|
| Lead Database | Person fields (name, title, seniority, department, email, phone, location) plus `company_industry`, `company_size`, `employees_count`, `company_website`, `company_annual_revenue`, `company_city`, `company_state`, `company_country`, `keywords`. Run one `limit=1` call and map from the keys you see before building a pipeline |
| Local Business Database | `title`, `category_name`, `address`, `city`, `state`, `postal_code`, `country_code`, `phone`, `website`, `emails`, `total_score`, `reviews_count`, `lat`, `lng`, and for named contacts `contact_first_name`, `contact_last_name`, `contact_job_title`, `contact_email`, `contact_mobile` |

### Long requests

A query string over about 16KB is refused before the search runs. The package sends a database read as POST with a JSON body once the encoded query passes 6,000 characters. Do the same: long saved-search URLs, long title lists, and location lists in the hundreds all go in a body. The response is identical.

### Database error branches

| Response | Meaning | Action |
|---|---|---|
| 400 | A `url` with no usable filters, or a `box` that cannot be read | Fix the input |
| 409 with `filters_not_applied_yet` (Lead Database) | Some company filters cannot be used yet; nothing is returned or counted | Drop those filters or retry later |
| 503 | The search ran too long | Narrow it: add a location, a size band or a category, or use fewer titles. Retrying the same search unchanged rarely helps |

## Webhooks

| Item | Value |
|---|---|
| Where | app.scrapercity.com/dashboard/webhooks (a dashboard setting, there is no API call to register one) |
| When | A run reaches `SUCCEEDED` or `FAILED` |
| Method | POST with a JSON body |
| Payload fields documented | `runId`, `fileName`, `leadsCount` (scrapercity-cli `SKILL.md`). Neither scrapercity.com/how-to-use nor /api-docs lists further fields, a signature header or a retry schedule |
| Receiver contract | Answer 200 fast. Then call the status endpoint with `runId` to learn the outcome and confirm the notification is real, and download only on `SUCCEEDED` |
| Idempotency | Key work on `runId` so a repeated delivery does not import twice |
| Backstop | An hourly sweep of `GET /api/v1/runs?hours=48` for `SUCCEEDED` runs not yet handled |
| Security | Use HTTPS and a long random path. Since no signature is documented, the status call is the authenticity check |

`CANCELLED` runs are not listed as a webhook trigger. If your code cancels a run, it already knows.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://scrapercity.com/llm-info
