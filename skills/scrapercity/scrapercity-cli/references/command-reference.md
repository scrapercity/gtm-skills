# Command Reference: scrapercity CLI 1.0.17

Every command and flag below was read from `bin/cli.mjs` and `lib/client.mjs` in the published `scrapercity` 1.0.17 package, and the request each command sends was captured with the network stubbed out (2026-10-13). Prices come from `references/scrapercity-catalog.md` only.

Invoke as `npx -y scrapercity@1.0.17 <command>` or, after `npm i -g scrapercity@1.0.17`, as `scrapercity <command>`. `scrapercity help`, `--help`, `-h` or no command prints the built-in help.

## Parsing rules that apply to every command

| Rule | Effect |
|---|---|
| Value flags are `--flag value` with a space | `--limit=100` is not read; the flag is ignored |
| A value flag given last with no value | Reads as `true`; commands that convert it to a number send 1 (`maps --limit` with no value asks for 1 place) |
| Positional arguments | Read before flags are removed in several commands; see `references/gaps-and-quirks.md` |
| Key lookup | `SCRAPERCITY_API_KEY` first, then `~/.scrapercityrc` (`{"apiKey": "..."}`) |
| Success | Exit 0, human-readable text on stdout |
| Any failure | Exit 1, `✗ ` plus the message on stderr. The message is the server's `error` or `message` field, or `HTTP N` when there is none |
| Unknown command | `✗ Unknown command: X. Run: scrapercity help`, exit 1 |
| No key | `✗ No API key. Run: scrapercity login  OR  export SCRAPERCITY_API_KEY=...`, exit 1 |

## Account and run commands (free)

| Command | Flags (default) | Calls | Prints |
|---|---|---|---|
| `login [key]` | none; prompts `API key:` when no key is given | Writes `~/.scrapercityrc` with owner-only permissions on creation | `✓ Saved to ~/.scrapercityrc` |
| `wallet` | none | `GET /api/v1/wallet` | `Plan: NAME ($LIMIT/cycle)`, `Balance: $X (subscription: $A + purchased: $B)`, `Used: $U (P%)`, `Renews: DATE` |
| `runs` | `--hours` (24), `--limit` (20) | `GET /api/v1/runs?hours=&limit=` | One line per run: status, first 12 characters of the run id, rows handled, cost, file name or URL |
| `status <runId>` | none | `GET /api/v1/scrape/status/{runId}` | `Status:`, `Message:`, `Handled: X / Y`, and a download hint when output exists |
| `poll <runId>` | `--interval` seconds (15); timeout fixed at 1 hour | Repeats `status` | Progress line, then `✓ Done: N leads`; exit 1 on FAILED, CANCELLED or timeout |
| `download <runId>` | `--output` or `-o` (`{runId}.csv` in the current folder) | `GET /api/downloads/{runId}` | `✓ PATH (N KB)`; on error `Download failed: HTTP N` |
| `cancel <runId>` | none | `POST /api/v1/scrape/cancel/{runId}` | `✓` plus the server message |
| `logs <runId>` | none | `GET /api/v1/scrape/logs/{runId}` | The run log text |

## Scraper and enrichment commands (paid)

Ceiling = what the command can bill at its defaults if every unit is billable.

| Command | Syntax and flags (default) | Sends to | Price | Ceiling at defaults |
|---|---|---|---|---|
| `apollo` | `apollo URL [--count N] [--name TEXT]`; URL must be the first argument; `--count` (1000) is 500-50,000 | `scrape_apollo`: `url`, `count`, `fileName` | $0.0039 per lead | $3.90 |
| `maps` | `maps -q TEXT -l PLACE [--limit N]`; long forms `--query`, `--location`; `--limit` (500) | `scrape_maps`: one `searchStringsArray` term, `locationQuery`, `maxCrawledPlacesPerSearch` | $0.0099 per business | $4.95 |
| `email-validate` | `email-validate a@x.com b@y.com` or `--file FILE` (every line containing `@`) | `validate_emails`: `emails` | $0.0072 per email | emails x $0.0072 |
| `email-find` | `--first --last --domain [--company] [--full-name]` for one person, or `--file CSV`; `--validate`, `--mobiles` | `find_emails`: `contacts`, plus `autoValidateEmails` and `autoFindMobiles` | $0.05 per email found, free if not found | contacts x $0.05 |
| `mobile-find` | `mobile-find INPUT...` or `--file FILE` (one LinkedIn URL or work email per line) | `find_mobiles`: `inputs` | $0.25 per number found, free if not found | inputs x $0.25 |
| `people-find` | `--name`, `--email`, `--phone` (comma lists), `--address` (list separated by `\|`), `--max-results` (1) | `find_people`: `name`, `email`, `phone_number`, `street_citystatezip`, `max_results` | $0.0199 per result, 0 matches billed as 1 | searches x $0.0199 |
| `store-leads` | `--platform`, `--country` (two-letter, sent as `countryCode`), `--category`, `--city`, `--technologies`, `--apps`, `--total-leads` (1000), `--name`; switches `--emails`, `--phones`, `--instagram`, `--facebook`, `--tiktok`, `--youtube`, `--linkedin` | `scrape_store_leads` | $0.0039 per lead | $3.90 |
| `builtwith` | `scrapercity builtwith TECHNOLOGY` (Tech Stack Search); `--tech`, `--name` exist but see quirks | `scrape_builtwith`: `technology`, `fileName` | $4.99 per technology | $4.99 |
| `criminal` | `--name "First Last"` (always use the flag), `--state`, `--dob MM/DD/YYYY` | `search_criminal_records` | $1.00 per search with records found, free when none | $1.00 |
| `airbnb` | `--city` (comma list), or `--url LISTING` for single mode; `--max-results` or `--limit` (100), `--checkin`, `--checkout` | `scrape_airbnb`: `mode`, `city`, `listingUrl`, `maxResults` | $0.019 per result | $1.90 if 100 results |
| `website-finder` | `website-finder DOMAIN...` or `--file FILE`; `--title` | `scrape_website_finder`: `domains`, `jobTitle` | $0.0499 per contact found | domains x $0.0499 |
| `yelp` | `-q` terms (comma list), `-l` locations (comma list), or `--urls` (comma list); `--limit` (10) | `scrape_yelp`: `searchTerms`, `locations`, `directUrls`, `searchLimit` | $0.0099 per result | terms x locations x 10 x $0.0099 |
| `angi` | `-q SLUG` (a service slug from the catalog, such as `plumbing`, `roofing`, `hvac`), `--zips` (comma list), `--limit` (100) | `scrape_angi`: `keyword`, `zipCodes`, `maxItems` | $0.0099 per listing | $0.99 |
| `zillow-agents` | `-l PLACE`, `--specialty`, `--language`, `--limit` (10, max 500) | `scrape_zillow_agents`: `location`, `specialty`, `language`, `searchLimit` | $0.029 per agent | $0.29 |
| `bizbuysell` | `bizbuysell URL...`; `--limit` (100) | `scrape_bizbuysell`: `startUrls`, `maxItems` | $0.0099 per listing | $0.99 |
| `crexi` | `crexi URL...` (property search, city or market search, or broker directory URL) | `scrape_crexi`: `startUrls` | $0.029 per property | Not capped; test one URL |
| `distress-list` | `distress-list "City, ST"` first, then `--types` (comma list of `preForeclosure`, `foreclosure`, `auction`, `bankOwned`), `--max` (1-500) | `scrape_distress_list`: `search`, `distressTypes`, `maxItems` | $0.05 per property | `--max` x $0.05; always pass `--max` |

Every start command prints `Run ID: ...` on its own line (Apollo adds a webhook reminder; some add `Est. cost:` from the server). Capture it with `awk '/Run ID:/ {print $3}'`.

## db-leads (Growth plan and up, $0 wallet)

`GET /api/v1/database/leads`, switching to `POST` with a JSON body when the query string passes 6,000 characters.

| Flag | API parameter | Type in the CLI |
|---|---|---|
| `--title` | `title` | text, commas inside for several (partial match) |
| `--not-title` | `notTitle` | text, commas inside |
| `--seniority` | `seniority` | comma list (`vp,director,c_suite`) |
| `--department` | `department` | comma list |
| `--industry`, `--not-industry` | `industry`, `notIndustry` | comma list |
| `--keywords`, `--not-keywords` | `keywords`, `notKeywords` | text; the server splits on commas |
| `--country`, `--state` | `country`, `state` (where the person is) | comma list |
| `--city` | `city` (person) | text |
| `--company-country`, `--company-state` | `companyCountry`, `companyState` (HQ) | comma list |
| `--company-city` | `companyCity` (HQ) | text |
| `--company`, `--domain` | `companyName`, `companyDomain` | text |
| `--min-employees`, `--max-employees` | `minEmployees`, `maxEmployees` | number |
| `--revenue-min`, `--revenue-max` | `revenueMin`, `revenueMax` (USD) | number |
| `--url` | `url` (a people-search URL) | text |
| `--apollo-url` | `apolloUrl` | older name for a search URL; prefer `--url` |
| `--has-email`, `--has-phone` | `hasEmail`, `hasPhone` | switch |
| `--exclude-delivered` | `excludeDelivered` | switch |
| `--after` | `after` (cursor; start with `0`) | text |
| `--page`, `--limit` | `page`, `limit` (max 100) | number |

Output: `N total leads, page P of T`, then `Next page: --after ID` when there is more, then `Not supported from the search URL: ...` when a URL filter was dropped, then the first 3 rows as JSON and `... and K more`.

## db-local (Growth plan and up, $0 wallet)

`GET /api/v1/database/local-businesses`, POST past 6,000 characters.

| Flag | API parameter | Type in the CLI |
|---|---|---|
| `--keyword` | `keyword` | text as typed; the server splits a list on commas and keeps "plumbers in Austin, TX" whole |
| `--location` | `location` | list separated by `;` (cities, states, countries, postal codes) |
| `--category`, `--not-category` | `category`, `notCategory` | comma list |
| `--country` | `country` | comma list of two-letter codes |
| `--state`, `--city`, `--postal-code` | `state`, `city`, `postalCode` | text |
| `--query` | `query` (name and description) | text |
| `--title` | `title` (business name) | text |
| `--box` | `box` as `minLat,minLng,maxLat,maxLng` | text |
| `--min-rating`, `--max-rating`, `--min-reviews`, `--max-reviews` | same names in camelCase | number |
| `--url` | `url` (a Google Maps search URL) | text |
| `--has-email`, `--has-phone`, `--has-website`, `--has-contact` | `hasEmail`, `hasPhone`, `hasWebsite`, `hasContact` | switch |
| `--exclude-delivered` | `excludeDelivered` | switch |
| `--after`, `--page`, `--limit` | `after`, `page`, `limit` | text, number, number |

Output adds `Places: ...` (how each location was read, with `(not found)` markers), `Keywords no business name or category has: ...`, and, when nothing matched but the Lead Database has people for the search, `Nothing here, but the Lead Database has N people for this search by ...: URL`.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/agents
- https://scrapercity.com/api-docs
- https://scrapercity.com/pricing
