# Local Business Database Filter Semantics

Exact behavior of every `query_local_business_database` parameter, from the `scrapercity` npm package 1.0.17 (`bin/mcp.mjs`, `bin/cli.mjs`, `lib/client.mjs`, `AGENT_DOCS.txt`).

## Combining rules

- Values inside `keyword`, `location`, `category` and `country` are OR (any of them).
- Different parameters are AND.
- `notCategory` removes businesses after the include filters.
- With `url`, the Google Maps search's keyword and place are the base; any parameter you also send overrides the matching part.

## Parameter reference

| Parameter | Type | Matching | CLI flag |
|---|---|---|---|
| `keyword` | string[] | What businesses do or are called, as typed on Google Maps. Matches names and categories, any keyword. A place inside a keyword is the location when `location` is empty | `--keyword` (passed as typed; the server splits on commas and keeps "plumbers in Austin, TX" whole) |
| `location` | string[] | Cities, states, countries or postal codes, as typed. Up to 2,000, any match | `--location` (semicolons between places) |
| `url` | string | A Google Maps search URL. Its keyword and place become the search. Adds `search_translation` | `--url` |
| `category` | string[] | Business categories. A word also finds categories that contain it | `--category` (commas) |
| `notCategory` | string[] | Excludes these categories | `--not-category` (commas) |
| `country` | string[] | Two-letter codes: `["US"]`, `["CA","GB"]` | `--country` (commas) |
| `state` | string | State or region, commas for several. US abbreviations work: "TX" | `--state` |
| `city` | string | Partial match | `--city` |
| `postalCode` | string | Postal or ZIP code | `--postal-code` |
| `box` | string | `"minLat,minLng,maxLat,maxLng"`. Only businesses inside. Unreadable box returns 400 | `--box` |
| `query` | string | Searches business names and descriptions | `--query` |
| `title` | string | Business name, commas for several, partial match | `--title` |
| `minRating`, `maxRating` | number | Google rating bounds, 1-5 | `--min-rating`, `--max-rating` |
| `minReviews`, `maxReviews` | number | Review count bounds | `--min-reviews`, `--max-reviews` |
| `hasEmail` | boolean | Only businesses with an email | `--has-email` |
| `hasPhone` | boolean | Only businesses with a phone | `--has-phone` |
| `hasWebsite` | boolean | Only businesses with a website | `--has-website` |
| `hasContact` | boolean | Only businesses with a named contact person | `--has-contact` |
| `page` | number | Default 1. Keep at 1 with `excludeDelivered` | `--page` |
| `limit` | number | Max 100. MCP default 50 | `--limit` |
| `excludeDelivered` | boolean | Skip businesses this account already has | `--exclude-delivered` |
| `after` | string | Cursor. `"0"` first, then `pagination.next_after` | `--after` |

## keyword vs category vs query vs title

| Want | Use | Example |
|---|---|---|
| A type of business, typed like a person would | `keyword` | `["med spa"]` |
| A Google category, including categories that contain the word | `category` | `["restaurant"]` also finds "Mexican restaurant" |
| A word in the business name or description | `query` | `"emergency"` |
| A business name or brand | `title` | `"Aspen Dental, Bright Now"` |
| Remove a category | `notCategory` | `["Dental laboratory"]` |

`keyword` is the default. Add `category` to pin one category and the categories that contain its word. Add `notCategory` to drop neighbors the keyword pulled in.

## Location fields

| Want | Use |
|---|---|
| A list of cities | `location: ["Austin TX", "Round Rock TX"]` |
| A list of ZIP codes | `location: ["78701", "78702", "78703"]` or `postalCode` for one |
| A whole state | `location: ["Texas"]` or `state: "TX"` |
| Several states | `state: "TX, OK, LA"` |
| A country | `location: ["Germany"]` or `country: ["DE"]` |
| A shape no city line follows | `box` |
| A city name shared by many states | `location: ["Springfield IL"]`, then check `searched_as.places[].read_as` |

## searched_as

```json
"searched_as": {
  "keywords": [{ "text": "ac guys", "words": ["ac","guys"], "categories": [], "matches_nothing": true }],
  "places": [{ "text": "Austin TX", "read_as": "Austin, Texas, US", "kind": "city" },
             { "text": "Austinn", "not_found": true }]
}
```

The values above illustrate the shape. Read the live response:

- A keyword with `matches_nothing: true` has no business name or category containing it. Rephrase.
- `categories` lists the categories the keyword matched. If it shows neighbors you do not want, add `notCategory`.
- A place with `not_found` was dropped. Fix it before trusting the count.
- `read_as` and `kind` show which place was used. Confirm ambiguous names.

## lead_database (fallback block)

On a search that finds nothing, the response adds `lead_database` when the Lead Database has 100+ people for the same search:

| Field | Meaning |
|---|---|
| `count` | People in the Lead Database for this search |
| `read_as` | Whether the keywords were read as job title or company keywords (whichever has more) |
| `filters` | The Lead Database filters to use |
| `dashboard_url` | A dashboard link to the same search |

Typical trigger: a B2B keyword ("saas companies", "cybersecurity firms") typed into the local search. Hand `filters` to `query_lead_database` (see `scrapercity-lead-database`).

## search_translation (with url)

`applied`, `approximated`, `not_supported`: what the database used from the Google Maps URL. Report `approximated` and `not_supported` to the user. A URL with nothing usable returns 400; rebuild with `keyword` and `location`.

## Returned fields

| Field | Content |
|---|---|
| `title` | Business name |
| `category_name` | Main category |
| `address`, `city`, `state`, `postal_code`, `country_code` | Location |
| `phone` | Business phone |
| `website` | Website |
| `emails` | Emails found for the business |
| `total_score` | Google rating |
| `reviews_count` | Number of reviews |
| `lat`, `lng` | Coordinates |
| `contact_first_name`, `contact_last_name`, `contact_job_title`, `contact_email`, `contact_mobile` | Named contact, when there is one |

## Pagination block

`page`, `limit`, `total`, `totalPages`, `has_more`, `next_after`. Use `total` for counts and `next_after` for the cursor.

## Errors

| Code | Meaning | Fix |
|---|---|---|
| 400 | Unreadable `box`, or a `url` with nothing usable | Fix the four numbers (min below max), or rebuild without the URL |
| 401 | Bad key | Ask for a valid key |
| 403 | Account cancelled or a charge is processing | Stop and tell the user |
| 429 | Rate limited | Wait, retry once. Stay under 100 calls a minute (scrapercity.com/api-docs) |
| 503 | Search took too long | Add a category, a city, a state or a postal code, or tile with `box` |
| Refused, no JSON | Query string over ~16KB | Same parameters as a POST JSON body |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://support.google.com/business/answer/3038177
