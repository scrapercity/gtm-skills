# ICP List Report: US SaaS VP Sales, 50-200 employees

Prepared 2026-10-12 for Pipeline Coaching Co., a sales-coaching firm selling a 12-week program to sales leaders. Plan: Growth ($149/mo). Wallet before run: $163.40. Company and person names below are fictional and use the reserved `.example` domain.

## ICP Definition

| Example customer | Domain | Industry | Employees | HQ | Buyer title | Why best-fit |
|-|-|-|-|-|-|-|
| Ledgerline | ledgerline.example | Computer Software | 85 | Austin, TX | VP Sales | Signed in 9 days, renewed for a second cohort |
| Shipwise | shipwise.example | Computer Software | 140 | Denver, CO | Chief Revenue Officer | Referred two other customers |
| Clinicflow | clinicflow.example | Hospital and Health Care software | 62 | Nashville, TN | VP Sales | Team quota attainment cited in their case study |
| Brightpath HR | brightpathhr.example | Human Resources software | 190 | Chicago, IL | Head of Sales | Expanded from 6 to 14 reps in the program |
| Quotient Labs | quotientlabs.example | Computer Software | 110 | Raleigh, NC | VP Sales | Bought after one call, no discount |

Shared traits used as filters: B2B SaaS business model (5 of 5), 62-190 employees (5 of 5, banded to 50-200), US person location (5 of 5), sales leader title at VP or CRO level (5 of 5).

Traits seen on fewer than 3 examples and left out: healthcare vertical (1 of 5), HR vertical (1 of 5), Series B funding (2 of 5), Texas HQ (1 of 5).

## Filters Used

| Parameter | Value | Evidence |
|-|-|-|
| title | VP Sales, Vice President of Sales, VP of Sales, Head of Sales, Chief Revenue Officer, CRO | Buyer titles at all 5 examples plus synonyms |
| notTitle | assistant, intern, former, retired, advisor, board, investor, operations, enablement, engineer | Sales leader exclusion set |
| keywords | saas, b2b | Tags present on 5 of 5 example companies |
| minEmployees / maxEmployees | 50 / 200 | Examples span 62-190 |
| country | United States | All 5 buyers sit in the US |
| hasEmail | true | Email campaign |

## Count Check

| Call | pagination.total | Decision |
|-|-|-|
| Count with title, keywords, size, country, hasEmail | 4,388 | 2.9x the 1,500 target; read 25 rows, 4 were sales operations or sales engineers |
| Recount with notTitle added | 3,412 | 2.3x target; pull 2,000 (target divided by 0.75) |

User go-ahead: approved by the user in chat on 2026-10-12 after seeing the 3,412 count and the $12.96 validation estimate.

## Pull Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Matched (pagination.total) | 3,412 | 0 | Starting point |
| Pulled | 2,000 | 1,412 | Planned pull of 20 pages of 100 via after cursors |
| After normalization | 1,974 | 26 | 19 broken email syntax, 7 rows with no first name |
| After dedupe | 1,936 | 38 | Same email listed twice under two title variants |
| After suppression | 1,800 | 136 | 41 current customers, 88 contacted in the last 90 days, 7 unsubscribes |
| Valid after validation | 1,512 | 288 | 171 catch_all and 45 unknown moved to the hold file, 68 invalid and 4 disposable removed |
| Send-ready after per-domain cap | 1,480 | 32 | Fourth and later contacts at the same domain |

## Validation Results

| Bucket | Count | Share | Action |
|-|-|-|-|
| valid | 1,512 | 84.0% | Main CSV |
| catch_all | 171 | 9.5% | Hold file, separate campaign capped at 10% of daily volume |
| unknown | 45 | 2.5% | Re-validate once after 72 hours |
| invalid | 68 | 3.8% | Removed, added to bounce suppression |
| disposable | 4 | 0.2% | Removed and suppressed |
| Total validated | 1,800 | 100% | Submitted in one `validate_emails` run |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Lead Database count calls | 2 records | Included in Growth plan | $0.00 |
| Lead Database pull | 2,000 leads | Included in Growth plan, 2% of the 100,000 daily allowance | $0.00 |
| validate_emails | 1,800 emails | $0.0072 | $12.96 |
| Total paid usage | | | $12.96 |

Cost per send-ready contact: $12.96 / 1,480 = $0.0088. Wallet after run: $150.44.

## Output Schema

| Column | Example | Rule |
|-|-|-|
| first_name | Dana | Normalized case, no credentials |
| last_name | Whitfield | Suffixes moved out |
| title | VP of Sales | As returned |
| title_normalized | vice president of sales | Lowercase, abbreviations expanded |
| seniority | vp | Derived from title |
| email | dana.whitfield@ledgerline.example | Lowercased |
| email_status | valid | Only valid in the main file |
| email_validated_at | 2026-10-12 | ISO date |
| company_name | Ledgerline | As returned |
| company_domain | ledgerline.example | Registrable domain |
| company_employees | 85 | Integer |
| person_state | TX | USPS code |
| source | lead_db | Controlled vocabulary |
| source_detail | lead_db:title=VP Sales...;keywords=saas,b2b;emp=50-200;country=US | Query fingerprint |
| segment | saas-50-200-vp-sales | Campaign slice |

## Sample Rows

| first_name | last_name | title | company_domain | employees | email_status | source |
|-|-|-|-|-|-|-|
| Dana | Whitfield | VP of Sales | ledgerline.example | 85 | valid | lead_db |
| Marcus | Oyelaran | Chief Revenue Officer | parcelgrid.example | 172 | valid | lead_db |
| Priya | Raman | Head of Sales | tallyroom.example | 58 | valid | lead_db |
| Owen | Castellano | Vice President of Sales | fleetnote.example | 121 | valid | lead_db |
| Hannah | Brekke | VP Sales | claimstack.example | 96 | valid | lead_db |

QA sample: 20 random rows checked by hand on 2026-10-12. 19 matched title, company and location; 1 was a VP Sales at a company that had grown to 240 employees (kept, size data lags).

## Next Steps

1. Load `icp-list-saas-vp-sales-2026-10-12.csv` (1,480 rows) into the sequencer with duplicate checking across campaigns turned on; see `cold-email-list`.
2. Re-validate the 45 unknown rows on 2026-10-15 and decide on the 171 catch_all rows after the first 500 sends show a bounce rate under 2%.
