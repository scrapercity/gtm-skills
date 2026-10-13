# Real Estate Tool Reference

Inputs, outputs, limits, prices and CLI flags for the six ScraperCity tools this skill uses. Prices come from `references/scrapercity-catalog.md`. Output fields marked "per scrapercity.com" come from the product page samples and may not be the complete column list.

All six are runs: the start call returns `runId`; poll `check_run_status` (or `GET /api/v1/scrape/status/{runId}`) until `SUCCEEDED`; then `download_results` (or `GET /api/downloads/{runId}`) for the CSV. These finish in minutes. Run `check_wallet` first.

## 1. Zillow Agents (`scrape_zillow_agents`)

| Item | Value |
|---|---|
| Endpoint | `POST /api/v1/scrape/zillow-agents` |
| Price | $0.029 per agent |
| Required | `location`: city and state, or ZIP |
| Optional | `specialty` (code string), `language`, `searchLimit` (1-500) |
| CLI | `npx scrapercity zillow-agents -l "Denver, CO" --specialty buyer --language English --limit 100` (CLI default limit is 10) |
| Output (per scrapercity.com) | Name, phone, email, screen name, profile URL, specialties, languages, active listings count, recent sales count, rating, review count, license number; sample also shows location and years of experience |

Specialty codes: the ScraperCity page describes 40+ specialties (buyer's agent, listing agent, relocation, foreclosure, short sale among them) without publishing the codes. The CLI usage example is `buyer`. Probe a new code with `searchLimit: 5` ($0.145) and read the specialties column before a full run.

Cost examples: 100 agents = $2.90. 500 agents = $14.50. Five suburbs at 200 each = 1,000 x $0.029 = $29.00.

Segmenting agents after the pull:

| Segment | Rule on the CSV | Why |
|---|---|---|
| Producers | Recent sales count in the top quartile | Most likely to buy tools, leads, ISA services |
| Listing-heavy | Active listings count high | Photography, staging, marketing offers |
| New agents | Few reviews, few sales | Brokerage recruiting, coaching |
| Bilingual | Languages includes a second language | Language-specific offers |

## 2. Property Lookup (`scrape_property_lookup`)

| Item | Value |
|---|---|
| Endpoint | `POST /api/v1/scrape/property-lookup` |
| Price | $0.15 per property; +$0.10 per property with `includeOwnerContact: true` ($0.25 total) |
| Required | `addresses`: array of full US addresses with city, state and ZIP |
| Optional | `includeOwnerContact` (adds owner name, phone and email), `fileName` |
| CLI | None in package 1.0.17. Use MCP or REST |
| Output | Property details, estimated home value, price history; owner name, phone and email when requested |

Address hygiene before a run:

| Problem | Fix |
|---|---|
| Missing ZIP | Add it; required |
| Unit numbers | Keep them: "123 Main St Apt 4, Denver, CO 80202" |
| Rural routes, PO boxes | Use the physical address |
| Duplicates | Dedupe; each row is billed |

Cost examples: 50 addresses = $7.50; with owner contact = $12.50. 1,000 with owner contact = $250.00.

## 3. Distress List (`scrape_distress_list`)

| Item | Value |
|---|---|
| Endpoint | `POST /api/v1/scrape/distress-list` |
| Price | $0.05 per property |
| Required | `search`: city + state, or ZIP |
| Optional | `distressTypes`: any of `preForeclosure`, `foreclosure`, `auction`, `bankOwned`; `maxItems`: 1-500 |
| CLI | `npx scrapercity distress-list "Tampa, FL" --types preForeclosure,auction --max 300` |
| Output (per catalog) | Full address, distress type, value estimates, property details |

Distress type to persona:

| Type | Stage | Who works it |
|---|---|---|
| `preForeclosure` | Owner in default, before sale | Wholesalers, investors, listing agents, short sale specialists |
| `foreclosure` | In foreclosure proceedings | Investors, agents |
| `auction` | Scheduled for sale | Auction buyers, investors |
| `bankOwned` | REO, lender owns it | Agents who list REO, investors buying from banks |

Covering a metro past 500: run one search per ZIP. 12 ZIPs at 200 each = 2,400 x $0.05 = $120.00. Dedupe on address across ZIP runs.

## 4. Crexi (`scrape_crexi`)

| Item | Value |
|---|---|
| Endpoint | `POST /api/v1/scrape/crexi-scraper` |
| Price | $0.029 per property |
| Required | `startUrls`: array of Crexi URLs |
| URL forms | Property search or list (`https://www.crexi.com/properties?...`); city or market search from the Crexi search bar (`https://www.crexi.com/search?...`), scoped to that location; broker directory (`https://www.crexi.com/resources/find-a-broker/...`) |
| Not supported | A map view with no city or market set. Returns 400 |
| CLI | `npx scrapercity crexi "<url>"` |
| Output (per scrapercity.com) | Property name, address, type, asking price, square footage, broker name, broker phone, broker firm, status, investment highlights, cap rate, NOI, year built, building class, zoning, lot size, image count |

Property types on Crexi per scrapercity.com: office, retail, industrial, multifamily, land, hospitality, special purpose.

Cost examples: 400 industrial listings = $11.60. 1,500 across three markets = $43.50.

## 5. BizBuySell (`scrape_bizbuysell`)

| Item | Value |
|---|---|
| Endpoint | `POST /api/v1/scrape/bizbuysell-scraper` |
| Price | $0.0099 per listing |
| Required | `startUrls`: BizBuySell search pages or individual listings |
| Optional | `maxItems`, `datasetName` (dedupe across runs) |
| CLI | `npx scrapercity bizbuysell "<url>" --limit 150` (CLI default 100) |
| Output (per scrapercity.com) | Title, location, price, EBITDA, revenue, cash flow, broker name, broker phone, broker firm, year established, employees, reason for selling, date listed, real estate, building square feet, seller type |

URL pattern for state and industry searches: `https://www.bizbuysell.com/texas/hvac-businesses-for-sale/`; county pages follow `https://www.bizbuysell.com/texas/dallas-county/hvac-businesses-for-sale/`. Build the search on the site, then copy the address bar.

Cost examples: 150 listings = $1.49. 2,000 listings across 10 states = $19.80.

## 6. People Finder (`find_people`)

| Item | Value |
|---|---|
| Endpoint | `POST /api/v1/scrape/skip-trace` |
| Price | $0.0199 per result; a search with 0 matches is billed as 1 result |
| Inputs | Any of `name`, `email`, `phone_number`, `street_citystatezip` (arrays); `max_results` per search |
| CLI | `npx scrapercity people-find --address "123 Main St, City, ST 12345"` (several addresses separated by `|`), `--name`, `--email`, `--phone` (commas for several), `--max-results` (default 1) |
| Output | Contact information and addresses for the matched person |

Spend control: every search costs at least $0.0199. With `max_results: 1`, 300 owner searches cost exactly 300 x $0.0199 = $5.97 whether or not each finds a match. With `max_results: 3`, the same 300 can cost up to $17.91.

Owner contact options compared, per property:

| Route | Cost | Gives |
|---|---:|---|
| `find_people` by property address, `max_results: 1` | $0.0199 | Contact info for the matched person |
| `scrape_property_lookup` with owner contact | $0.25 | Valuation, history, owner name, phone, email |
| Distress List then `find_people` | $0.05 + $0.0199 = $0.0699 | Distress type, value estimate, owner contact |

## Run and poll pattern (any tool)

```bash
RUN=$(curl -s -X POST https://app.scrapercity.com/api/v1/scrape/distress-list \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"search":"Tampa, FL","distressTypes":["preForeclosure","auction"],"maxItems":300}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['runId'])")
npx scrapercity poll "$RUN" --interval 20
npx scrapercity download "$RUN" -o tampa-distress.csv
```

Error handling: 402 means the wallet is short (run `check_wallet`, report the gap); 409 means the same request went in moments ago (use the earlier run); 429 means back off and retry once.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/zillow-agents-scraper
- https://scrapercity.com/crexi-scraper
- https://scrapercity.com/bizbuysell-scraper
- https://www.bizbuysell.com/texas/hvac-businesses-for-sale
