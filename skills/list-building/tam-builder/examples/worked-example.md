# TAM Report: HVAC contractors in Texas

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Prepared 2026-10-12 for DispatchDesk, a field-service scheduling app priced at $300 a month. Plan: Growth ($149/mo). Wallet before run: $158.90.

## Market Definition

| Part | Value |
|-|-|
| Business type | Residential and light commercial heating and air conditioning contractors |
| Geography | Texas |
| Size band | Any size; SAM limited to businesses with 20+ Google reviews in the five metros the sales team covers |
| Exclusions | HVAC supply houses, appliance stores, equipment manufacturers |
| NAICS benchmark code | 238220 Plumbing, Heating, and Air-Conditioning Contractors (mixes plumbers in, so it overstates the HVAC-only market) |
| ACV used for dollars | $3,600 ($300 a month list price, from the user's pricing page) |

## Source Counts

| Source | Call or run | Count | Unit | Projected cost |
|-|-|-|-|-|
| local_db | `query_local_business_database` keyword hvac contractor, air conditioning contractor, heating contractor; location Texas; notCategory supply and appliance; limit 1 | 9,840 | businesses | $0.00, included in Growth |
| lead_db | `query_lead_database` title Owner, President, CEO, Founder, General Manager; keywords hvac; companyState Texas; limit 1 | 6,215 | people | $0.00, included in Growth |
| lead_db company proxy | 500-row sample had 347 unique domains, ratio 0.694 | 4,313 | estimated companies | Not billed |
| maps | 30 sub-cities in 5 metros x 3 terms x 50 cap | 4,500 maximum | businesses | $44.55 ceiling at $0.0099 |

User go-ahead: approved in chat on 2026-10-12 for the database pulls and up to $44.55 of Maps runs.

## Pull and Dedupe Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Raw rows, all sources | 19,655 | 0 | 9,840 local_db + 6,215 lead_db + 3,600 maps returned |
| After normalization | 19,412 | 243 | Out-of-state addresses and rows with no name |
| After people-to-company collapse | 17,507 | 1,905 | Lead Database rows sharing a company domain |
| After pass 1 domain | 13,020 | 4,487 | Same company across sources |
| After pass 2 name and ZIP | 12,180 | 840 | No-domain rows with the same name key and ZIP |
| After pass 3 name and street | 12,045 | 135 | Same name key and street, ZIP missing or mistyped |
| After pass 4 phone | 11,890 | 155 | Name variants sharing one E.164 phone |
| Final accounts | 11,622 | 268 | Excluded supply houses and manufacturers found in a category review |

## Source Mix

| source | Accounts |
|-|-|
| local_db | 4,980 |
| local_db\|lead_db | 2,410 |
| local_db\|maps | 1,120 |
| local_db\|lead_db\|maps | 455 |
| lead_db | 1,042 |
| lead_db\|maps | 188 |
| maps | 1,427 |
| Total | 11,622 |

## Coverage Estimate

| Metric | Value |
|-|-|
| Sample area | Houston metro, 8 sub-cities |
| n1 | 1,240 local_db accounts |
| n2 | 980 maps accounts |
| m (overlap) | 812 |
| Observed | 1,408 |
| Chapman estimate | 1,496 |
| Coverage | 94.1% |

Caveat: both sources favor contractors with a website and reviews, so 1,496 is a floor and true coverage is lower than 94.1%. Applying the Houston rate statewide gives an estimated market of about 12,350 HVAC contractors (11,622 / 0.941), as a planning figure only.

## TAM SAM SOM

| Layer | Definition | Accounts | ACV | Dollars |
|-|-|-|-|-|
| TAM | Every deduped account in the definition | 11,622 | $3,600 | $41,839,200 |
| SAM | In Houston, DFW, Austin, San Antonio or El Paso, 20+ reviews | 6,940 | $3,600 | $24,984,000 |
| SOM | 2% of SAM in 12 months, the user's stated target | 139 | $3,600 | $500,400 |

## Metro Breakdown

| Metro | Accounts | Maps-only accounts added | Share of TAM |
|-|-|-|-|
| Dallas-Fort Worth | 3,105 | 452 | 26.7% |
| Houston | 2,964 | 410 | 25.5% |
| San Antonio | 1,288 | 236 | 11.1% |
| Austin | 1,140 | 198 | 9.8% |
| El Paso | 402 | 131 | 3.5% |
| Rest of Texas | 2,723 | 0 | 23.4% |
| Total | 11,622 | 1,427 | 100.0% |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Local Business Database pull, 99 pages via after cursors | 9,840 businesses | Included in Growth, 9.8% of the daily allowance | $0.00 |
| Lead Database pull, 63 pages | 6,215 leads | Included in Growth, 6.2% of the daily allowance | $0.00 |
| scrape_maps, 30 runs | 3,600 businesses | $0.0099 | $35.64 |
| Total paid usage | | | $35.64 |

Cost per account in the final file: $35.64 / 11,622 = $0.0031. Wallet after run: $123.26.

## Output Schema

| Column | Example | Rule |
|-|-|-|
| business_name | Lone Star Comfort Air | As returned by the base record |
| business_name_key | lone star comfort air | Matching only |
| category | HVAC contractor | Primary category |
| domain | lonestarcomfort.example | Registrable domain, blank for social hosts |
| phone | +17135550142 | E.164 |
| street, city, state, postal_code | 1200 Main St, Pasadena, TX, 77502 | USPS state, ZIP as text |
| rating, reviews | 4.7, 213 | From local_db or maps |
| source | local_db\|maps | Every contributing source |
| source_detail | local_db:keyword=hvac contractor;location=Texas | Base row query |
| completeness_score | 8 | Quality standard section 4c |
| metro | Houston | Metro assignment |
| in_sam | true | 20+ reviews and in a served metro |

## Next Steps

1. Pull the County Business Patterns 2023 establishment count for NAICS 238220 in Texas from data.census.gov and add it as a benchmark row; expect it to exceed this file because it includes plumbers.
2. Run `decision-maker-finder` on the 6,940 SAM accounts, starting with Dallas-Fort Worth, then `cold-email-list` for the first 1,500.
