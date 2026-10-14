# Framework Notes: ScraperCity Local Business Database

Which sources shape this skill, what each contributes, and where to look for each job.

## Routing table

| You need | Open |
|---|---|
| Exact behavior of `keyword`, `location`, `category`, `box` or any other parameter | `references/filter-semantics.md` |
| How to read `searched_as`, `search_translation` and the `lead_database` block | `references/filter-semantics.md` |
| The list of returned fields | `references/filter-semantics.md` |
| A ready search for a vertical (dentists, HVAC, med spas, law firms, gyms, 50+ more) | `references/category-recipes.md` |
| Rating and review segments and the opening angle for each | `references/segmentation-and-tiling.md` |
| Map box tiles for a big metro | `references/segmentation-and-tiling.md` |
| Prices for `scrape_maps`, `scrape_yelp`, `scrape_angi`, `validate_emails`, `find_emails` | `references/scrapercity-catalog.md` (shared) |
| Plan, allowance and paging rules | `references/scrapercity-platform.md` (shared) |

## Sources and contributions

### ScraperCity Local Business Database API (primary)

From the published `scrapercity` npm package, version 1.0.17:

- `bin/mcp.mjs` defines `query_local_business_database`: `keyword` and `location` as arrays (location up to 2,000 places, any match), a place inside a keyword used as the location when none is given, `category` matching categories that contain the word, two-letter `country`, `state` with commas and US abbreviations, partial-match `city`, `box` as four comma-separated numbers, `title` as business name with commas, rating and review bounds, the four `has*` flags, `excludeDelivered` with `page` kept at 1 or `after`.
- `bin/cli.mjs` defines `db-local`: list flags with commas (`--category`, `--country`, `--not-category`), `--location` split on semicolons, `--keyword` passed as typed, and the printed summary of places read, keywords that match nothing, and the Lead Database fallback.
- `lib/client.mjs` switches to POST with a JSON body past 6,000 characters of query string.
- `AGENT_DOCS.txt` documents `searched_as` (`keywords[]` with `text`, `words`, `categories`, `matches_nothing`; `places[]` with `text`, `read_as`, `kind`, `not_found`), the `lead_database` block (`count`, `read_as`, `filters`, `dashboard_url`) on an empty search when the Lead Database has 100+ people, the 400 for an unreadable box or an unusable URL, the ~16KB limit, the 503 rule, and the returned fields.
- The catalog entry for `scrape_maps` says its response can include a `local_business_database` block (`matches`, `url`, `api`) with businesses for the same search that the account does not have yet.

### ScraperCity catalog and platform facts

Prices: `scrape_maps` $0.0099 per business, `scrape_yelp` $0.0099 per result, `scrape_angi` $0.0099 per listing, `validate_emails` $0.0072 per email, `find_emails` $0.05 per email found, `find_mobiles` $0.25 per number found. Plans and allowance: Growth $149/mo and Scale $649/mo include the database; 100,000 new businesses a day; re-fetching owned records is free.

### Google Business Profile category guidelines

Google asks businesses to pick the most specific category that completes "this business IS a", and adds broader parent categories automatically. Practical effect for search: the specific category ("Pediatric dentist", "Emergency veterinarian") finds a tight set, the broad word ("dentist") finds the broad set, and service words ("teeth whitening") are not categories at all. The recipes start specific and widen.

### BrightLocal Local Consumer Review Survey 2026

A panel of 1,002 US adults. Numbers used here as segment lines, treated as hypotheses to test, dated 2026:

- 68% will only use a business with 4+ stars; 31% only 4.5+.
- 47% will not use a business with fewer than 20 reviews.
- 74% look for reviews written in the last three months.
- 97% read reviews for local businesses.

These set the 4.0 and 4.5 rating lines and the 20-review line in the segments.

### USGS distance per degree

At 38 degrees north, one degree of latitude is about 69 miles and one degree of longitude is about 54.6 miles. Longitude shrinks toward the poles. The tiling table in `references/segmentation-and-tiling.md` uses these to convert a tile step to miles.

### Google Email sender guidelines

Bulk senders to Gmail need a one-click unsubscribe, removals processed within 48 hours and a spam rate kept under 0.1% (never 0.3% or higher). These set the email settings for any send from a local pull.

## How the sources combine

1. The ScraperCity API decides what a search can express.
2. Keyword and category wording follows Google's category rules.
3. BrightLocal sets where to cut the rating and review segments.
4. The USGS figures convert map box steps to miles; the tile step itself comes from counting tiles and splitting any that return 503.
5. Google's sender rules set the email settings.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/pricing
- https://support.google.com/business/answer/3038177
- https://www.brightlocal.com/research/local-consumer-review-survey/
- https://www.usgs.gov/faqs/how-much-distance-does-a-degree-minute-and-second-cover-your-maps
- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
