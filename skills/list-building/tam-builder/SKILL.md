---
name: tam-builder
description: >-
  Builds a total addressable market file: defines the market, counts it in the
  Lead Database and Local Business Database, pulls every account with cursor
  paging, fills coverage gaps with Google Maps or Store Leads scrapes, dedupes by
  domain then normalized business name keeping the most complete record, and
  delivers one company-level CSV with a source column, a coverage estimate and
  TAM/SAM/SOM in accounts and dollars. Use when the user asks "how big is my
  market", "build our TAM", "every X in Y", or "account universe".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [tam, market-sizing, account-universe, local-business-database, lead-database, dedupe]
  related_skills: [icp-list-builder, local-business-list, ecommerce-by-techstack, decision-maker-finder, crm-enricher, scrapercity-local-business-database, scrapercity-lead-database]
  frameworks:
    - "US Census Bureau - County Business Patterns and NAICS as an outside benchmark"
    - "Lincoln-Petersen and Chapman capture-recapture estimators for coverage"
    - "April Dunford - best-fit segment before market size"
    - "Public Suffix List - registrable domain as the company key"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md]
---

# TAM Builder

## Overview

This skill produces an account universe: one row per real company in a defined market, pulled from every ScraperCity source that covers it, deduped, with a `source` column showing where each row came from. It adds a coverage estimate (how much of the real market the file holds) and a TAM, SAM and SOM in accounts and dollars.

It prevents two failures. The first is quoting a market size from one database count, which double counts people as companies and misses businesses the source does not hold. The second is merging three sources without a dedupe key, which inflates the market by 20-40% and sends the same business three emails.

## When to Use

- "How many HVAC contractors are there in Texas, and can I get all of them?"
- "Build our TAM for the board deck."
- "Every Shopify store selling pet supplies in the US."
- "Account universe for territory planning."
- "Which metros have the most targets per rep?"

Use a different skill when:

| The user wants | Use |
|-|-|
| A send-ready contact list for a campaign now | `icp-list-builder` or `cold-email-list` |
| Local businesses in one city with emails | `local-business-list` |
| Stores filtered by installed apps or tech | `ecommerce-by-techstack` |
| Buyers at the accounts this file produces | `decision-maker-finder` |
| The TAM loaded into a CRM | `crm-enricher` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Market definition in one sentence (who, where, size) | Drives every filter | Ask; refuse to size "SMBs" |
| Market type: B2B companies, local businesses, or online stores | Picks sources | Infer from the definition, confirm |
| Geography | Location filters, metro splits | Ask |
| Annual contract value (ACV) | Dollar TAM | Ask; report accounts only if unknown |
| Territories or metros the team can serve | SAM | Same as TAM geography |
| Plan | Databases need Growth or Scale | `check_wallet` |

## Authoritative Foundations

| Source | Contribution |
|-|-|
| US Census Bureau, County Business Patterns (CBP) and NAICS | CBP publishes establishment counts by industry code and geography each year. Use it as an outside check: if your deduped file holds far fewer accounts than CBP lists for the NAICS code, coverage is low; far more means the definition is too loose. CBP counts establishments with paid employees, so owner-only shops are missing from it. |
| Lincoln-Petersen and Chapman capture-recapture estimators | With two independent samples of one population, total size is about n1 times n2 divided by the overlap. Applied to two sources in one metro it estimates how many businesses neither source has. |
| April Dunford, best-fit customers | TAM is only useful when sized for the segment that values the product most. Define the market from the best-fit customer traits, then size it. |
| Public Suffix List | The registrable domain is the most stable company key across sources; `shop.acme.co.uk` and `acme.co.uk` are one company. |
| `references/list-quality-standard.md` | Company schema, business name key, dedupe precedence, completeness score, `source` vocabulary. |

Detail in `references/framework-notes.md`.

## Workflow

### 1. Write the market definition

One sentence with all four parts: business type, geography, size band, exclusions. Example: "Residential and light commercial HVAC contractors in Texas, any size, excluding supply houses and manufacturers." Map it to a NAICS code for the CBP benchmark (238220 Plumbing, Heating, and Air-Conditioning Contractors in this example). Recipes for common markets are in `references/market-definition-recipes.md`.

### 2. Pick sources by market type

| Market type | Primary source | Second source | Gap fill |
|-|-|-|-|
| Local or storefront businesses | `query_local_business_database` | `query_lead_database` owners, deduped to companies | `scrape_maps`, then `scrape_yelp` or `scrape_angi` for trades |
| B2B companies with staff | `query_lead_database`, one leader title per company | `query_local_business_database` for companies with a physical presence | Tech Stack Search (`scrape_builtwith`) for technology-defined markets |
| Online stores | `scrape_store_leads` | Ecommerce Database (REST) | Tech Stack Search for a platform or app |

### 3. Count every source before pulling

- Local Business Database: one call with `limit: 1`, read `pagination.total`. That is a business count.
- Lead Database: `pagination.total` counts people, not companies. Use a one-per-company title set (Owner, Founder, CEO, President, General Manager), pull a 500-row sample, compute unique domains divided by rows, and multiply the total by that ratio for an estimated company count.
- Store Leads: there is no free count. Run a `totalLeads: 100` probe with the filters ($0.0039 per lead, $0.39) and read the rows to confirm the filters fit before a large job.
- Maps: there is no count call. Estimate from metro size (see `references/coverage-and-dedupe-playbook.md`) and cap with `maxCrawledPlacesPerSearch`.

Put the counts in one table with the projected cost and show it to the user. Stop for a go-ahead if paid steps exceed $5.

### 4. Pull the databases with cursors

`check_wallet`, then page each database with `after: "0"` and `limit: 100`, passing `pagination.next_after` until null. Pulls above 100,000 new records per database per day split across days (by state or metro). Save each page to disk with `source` and `source_detail`.

### 5. Fill gaps

Decide where to scrape by comparing database counts per metro against population or against CBP per county. Metros where the database count per 100k residents is under half the state average are gap candidates. For each:

- `scrape_maps` with `searchStringsArray` set to 2-4 keyword variants and `locationQuery` set to each sub-city (metros split into sub-cities; lists in `references/coverage-and-dedupe-playbook.md`).
- Before paying, read the `local_business_database` block a Maps run can return: it reports matches already in the database that the account does not have yet. Pull those from the database first.
- Poll `check_run_status` every 60 seconds, then `download_results`.

### 6. Normalize and dedupe

Normalize every row to the business schema (`references/list-quality-standard.md` section 2b). Then dedupe in two passes:

1. Registrable `domain` (blank for social-only websites).
2. `business_name_key` plus `postal_code`, then `business_name_key` plus `street`, for rows with no domain.
3. Phone in E.164 as a final catch for rows that share neither.

When rows match, keep the most complete record by completeness score, fill empty fields from the other rows, and join every contributing source into `source` (for example `local_db|maps`).

### 7. Estimate coverage

Pick 1-3 metros covered by two sources. Run Chapman's estimator on the overlap (formula and caveats in `references/coverage-and-dedupe-playbook.md`). Report observed accounts, estimated true count, and coverage percentage. Compare the statewide deduped count against the CBP establishment count for the NAICS code when the user can supply it.

### 8. Size TAM, SAM, SOM

| Layer | Definition used here |
|-|-|
| TAM | Every deduped account in the market definition times ACV |
| SAM | Accounts the team can serve (territories, languages, size band) times ACV |
| SOM | A 12-month share of SAM the user commits to, stated as an assumption |

Deliver the CSV and the report in `templates/output-template.md`. Run `scripts/check-output.py`.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Local business count and pull | `query_local_business_database` | Included on Growth and Scale, 100,000 new businesses a day |
| B2B count and pull | `query_lead_database` | Included on Growth and Scale, 100,000 new leads a day |
| Maps gap fill | `scrape_maps` | $0.0099 per business |
| Yelp gap fill | `scrape_yelp` | $0.0099 per result |
| Home services gap fill | `scrape_angi` | $0.0099 per listing |
| Online stores | `scrape_store_leads` | $0.0039 per lead |
| Technology-defined markets | `scrape_builtwith` (Tech Stack Search) | $4.99 per technology |
| Runs | `check_run_status`, `download_results`, `list_runs` | Free |

### Calls for the HVAC example

Local Business Database count:

```json
{"keyword": ["hvac contractor", "air conditioning contractor", "heating contractor"],
 "location": ["Texas"], "notCategory": ["Appliance store", "HVAC supply store"], "limit": 1}
```

Pull: same body with `"limit": 100, "after": "0"`, then each `pagination.next_after`. Read `searched_as` in the first response to confirm Texas was read as the state.

Lead Database company proxy:

```json
{"title": "Owner, President, CEO, Founder, General Manager",
 "notTitle": "assistant, former, sales, technician",
 "keywords": ["hvac"], "companyState": ["Texas"], "limit": 100, "after": "0"}
```

Maps gap fill for one metro:

```json
{"searchStringsArray": ["hvac contractor", "air conditioning repair", "heating contractor"],
 "locationQuery": "Pasadena, TX", "maxCrawledPlacesPerSearch": 50}
```

`maxCrawledPlacesPerSearch` applies per search term, so this call can return up to 150 businesses (3 terms x 50) and cost up to $1.49. Each sub-city is a separate run; keep a list of run ids. Store Leads for an ecommerce TAM: `{"platform": "shopify", "countryCode": "US", "category": "pet supplies", "totalLeads": 1000, "offset": 0}`, then raise `offset` by `totalLeads` each call or send back `nextOffset`.

### Worked cost estimate

| Item | Units | Unit price | Cost |
|-|-:|-:|-:|
| Local Business Database pull | 9,840 businesses | Included in Growth | $0.00 |
| Lead Database pull | 6,215 leads | Included in Growth | $0.00 |
| Google Maps gap fill, 30 sub-cities x 3 terms x 50 cap (4,500 max, $44.55 ceiling) | 3,600 businesses returned | $0.0099 | $35.64 |
| Total paid usage | | | $35.64 |

The two database pulls use 9.8% and 6.2% of their daily allowances. $35.64 exceeds $5, so show the table and wait for approval before the Maps runs.

## Output Format

1. `tam-[market]-[date].csv`: one row per account, business schema from the quality standard plus `source`, `source_detail`, `completeness_score`, `metro`, `in_sam` (true or false).
2. A report from `templates/output-template.md`: market definition, source counts, pull and dedupe funnel, source mix, coverage estimate, TAM/SAM/SOM, metro breakdown, cost, next steps.

## Quality Check

- [ ] Market definition names business type, geography, size band and exclusions.
- [ ] Every source was counted before pulling; counts and cost shown before paid runs.
- [ ] Lead Database totals converted from people to companies with a sampled ratio.
- [ ] Funnel adds up from raw rows to final accounts with a reason on each drop.
- [ ] Source mix rows sum to the final account count.
- [ ] Every row has a `source` value from the controlled vocabulary.
- [ ] Coverage estimate shows observed, estimated and percentage, with its caveat.
- [ ] TAM, SAM and SOM each show accounts, ACV and dollars, and SOM states its assumption.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Quoting `pagination.total` from the Lead Database as a company count | It counts people; a 40-person firm can appear 40 times | One leader title per company, sample the domain ratio, dedupe by domain. |
| Deduping only by name | "ABC Heating" and "ABC Heating & Air LLC" survive as two | Domain first, then name key plus ZIP, then phone. |
| Deduping only by domain | Franchise locations sharing one domain collapse into one row | For local markets keep one row per location; use phone as the location key. |
| One Maps search for a whole metro | Maps searches return a limited set per query; outer suburbs vanish | Split into sub-cities and keyword variants. |
| Paying for Maps rows the database already has | Double spend | Pull the database first; read the `local_business_database` block in the Maps response. |
| Treating capture-recapture as exact | Both sources favor businesses with an online presence, so the estimate is a floor | Say so in the report; cross-check with CBP. |
| A TAM in dollars with no ACV source | Board decks repeat it | State ACV and where it came from. |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the reasoning or source behind a rule, or the routing table. |
| `references/market-definition-recipes.md` | Writing the market definition and the per-source filters (24 markets). |
| `references/coverage-and-dedupe-playbook.md` | Gap-fill decisions, metro sub-city splits, capture-recapture, dedupe passes, merge rules. |
| `references/list-quality-standard.md` | Schema, normalization, dedupe precedence, source vocabulary (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Database rules and daily allowances (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished TAM for HVAC contractors in Texas. |
| `scripts/check-output.py` | Final gate on the report. |

## Related Skills

- `icp-list-builder` for a contact list from one slice of this TAM.
- `local-business-list` for one city with validated emails.
- `ecommerce-by-techstack` for online store markets by app or technology.
- `decision-maker-finder` to add buyers to the accounts.
- `crm-enricher` to load the account universe into HubSpot or Pipedrive.
- `scrapercity-local-business-database` and `scrapercity-lead-database` for every parameter.
