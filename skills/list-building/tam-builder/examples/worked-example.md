# TAM Report: HVAC contractors in Texas

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Prepared 2026-10-12 for DispatchDesk, a field-service scheduling app priced at $300 a month with an 80% gross margin, sold by 4 account executives and 2 SDRs. Plan: Growth ($149/mo). Wallet before run: $158.90.

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
| local_db | Local Business Database keyword hvac contractor, air conditioning contractor, heating contractor; location Texas; notCategory supply and appliance; limit 1 | 9,840 | businesses | $0.00, included in Growth |
| lead_db | Lead Database title Owner, President, CEO, Founder, General Manager; keywords hvac; companyState Texas; limit 1 | 6,215 | people | $0.00, included in Growth |
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

## Source Overlap

`found_in` counts list sources plus outside imports per account. Enrichment lookups do not count.

| Found in N sources | Confidence | Accounts | Share of TAM |
|-|-|-|-|
| 1 | Low | 3,184 | 27.4% |
| 2 | Medium | 4,678 | 40.3% |
| 3 | High | 2,900 | 25.0% |
| 4 | High | 820 | 7.1% |
| 5 | High | 40 | 0.3% |

| Outside source | Rows after own dedupe | Dedupe key | Matched to file | New accounts added | Held for review |
|-|-|-|-|-|-|
| TDLR Air Conditioning Contractors license file, active licenses with a business name and Texas business address | 9,412 | Phone, then name key + ZIP | 7,830 | 0 | 1,582 |
| ACCA contractor locator, five SAM metros | 702 | Domain, then phone | 640 | 0 | 62 |

Reading: the imports ran after the funnel was frozen for the board deck, so they confirm accounts and add none this cycle. 7,830 of 9,412 active licensees (83.2%) are already in the file, a registry-based coverage check that sits below the 94.1% capture-recapture figure. The 1,582 unmatched licensees and 62 unmatched ACCA listings are in `tam-review-hvac-tx-2026-10-12.csv` for a Maps probe. The 3,184 Low accounts (27.4%) get a website or Maps existence check before any paid enrichment.

## Source Yield

| Source | Accounts contributed | Unique accounts | Cost | Cost per unique account | Next refresh |
|-|-|-|-|-|-|
| local_db | 8,965 | 4,980 | $0.00 | $0.000 | Keep |
| lead_db | 4,095 | 1,042 | $0.00 | $0.000 | Keep |
| maps | 3,190 | 1,427 | $35.64 | $0.025 | Keep, limited to the 30 gap sub-cities |
| TDLR license file | 7,830 | 0 | $0.00 | none added | Keep as the registry coverage check |

Maps found 1,427 accounts no database held at $0.025 each, under the $14.40 Tier 3 ceiling, so it stays for next month's gap sub-cities.

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

Caveat: both sources favor contractors with a website and reviews, so 1,496 is a floor and 94.1% is a ceiling; the license-file match (83.2%) is the lower check. Applying the Houston rate statewide gives an estimated market of about 12,350 HVAC contractors (11,622 / 0.941), as a planning figure only.

## TAM SAM SOM

| Layer | Definition | Accounts | ACV | Dollars |
|-|-|-|-|-|
| TAM | Every deduped account in the definition | 11,622 | $3,600 | $41,839,200 |
| SAM | In Houston, DFW, Austin, San Antonio or El Paso, 20+ reviews | 6,940 | $3,600 | $24,984,000 |
| SOM | 2% of SAM in 12 months, the user's stated target | 139 | $3,600 | $500,400 |

## Account Tiers

| Tier | Rule | Accounts | Motion | Contacts per account | Spend ceiling per account |
|-|-|-|-|-|-|
| 1 | Score 14 or more, top 120 by score | 120 | Account brief, email plus manual calls by an AE, person-level opener | 3 | $144.00 |
| 2 | Next 1,200 by score (score 8 to 13) | 1,200 | SDR sequence with an account-level opener (new location, hiring, reviews) | 2 | $48.00 |
| 3 | Score 3 to 7 | 4,100 | Segment-level sequence, one contact | 1 | $14.40 |
| Not worked | Score under 3 | 1,462 | Monthly re-score only | 0 | $0.00 |
| Excluded | Current customers (46) and open opportunities (12) | 58 | Account owners | 0 | $0.00 |

Scored on: 50+ Google reviews 6 points, confidence High 5, named owner on file 3, rating 4.0 or higher 2 (weights from win-rate lift on 112 closed deals, 38 won); website and size columns not scored because they are filled on under 80% of SAM rows, the user's minimum fill.
Deal inputs (from you): ACV $3,600, gross margin 80%, so $2,880 first-year gross profit; win rates of 1 in 20, 1 in 60 and 1 in 200 worked accounts by tier, from last year's CRM.
Capacity: 4 AEs x 30 researched accounts a quarter = 120; 2 SDRs x 46 new accounts a week x 13 weeks = 1,196, rounded to 1,200.
Backtest: 31 of 46 current customers score into Tier 1 or 2 (67.4%) against 19.0% of SAM, concentration 3.5x.
Movers applied: none this cycle; the user's CRM had no web engagement export and no Sales Navigator seat, so every account sits at its fit tier.
Quarter-end read: 2027-01-12, meetings per 100 accounts worked by tier; Tier 1 must book more meetings per 100 than Tier 2 or the weights change.

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
| Google Maps scraper, 30 runs | 3,600 businesses | $0.0099 | $35.64 |
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
| completeness_score | 8 | Email 3, valid email 2, named contact 2, phone 1, website 1, street 1, rating 1 |
| import_sources | tdlr_ac_2026-10;acca_2026-10 | Outside lists that matched this account, `;` separated |
| found_in | 4 | Count of list sources plus import lists |
| confidence | High | 3+ High, 2 Medium, 1 Low |
| metro | Houston | Metro assignment |
| in_sam | true | 20+ reviews and in a served metro |

## Next Steps

| # | Step | Owner | Date | Done when |
|-|-|-|-|-|
| 1 | Add the County Business Patterns 2023 establishment count for NAICS 238220 in Texas (data.census.gov) as a benchmark row; it should exceed this file because it includes plumbers | Agent | 2026-10-14 | Benchmark row added |
| 2 | Run a Maps probe on the 1,582 held license-file rows by metro and add the ones that pass to next month's refresh | Agent | 2026-10-16 | Held rows resolved |
| 3 | Find the buyers at the 120 Tier 1 and 1,200 Tier 2 accounts, then write a one-page brief on each Tier 1 account | Agent | 2026-10-21 | Tier 1 briefs and contacts delivered to the AEs |
