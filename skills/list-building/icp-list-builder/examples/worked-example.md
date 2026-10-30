# ICP List Report: US SaaS VP Sales, 50-200 employees

_Illustrative example of a run report. Companies, people, counts and run results are invented to show the format and use the reserved `.example` domain. Prices are ScraperCity catalog prices._

Status: Ran 2026-10-12 for Pipeline Coaching Co., a sales-coaching firm selling a 12-week program to sales leaders. Counts, pull and validation below are live results. Plan: Growth. Wallet: $163.40 before, $160.36 after.

## Answer

| Question | Answer |
|-|-|
| How many send-ready contacts? | 1,480 VP Sales, Head of Sales and CRO contacts at US B2B SaaS companies with 50-200 employees, every email validated `valid`, at most 3 per company |
| What is held back? | 216 catch-all and unknown addresses in a hold file, released only after the test cell passes |
| What did it cost? | $3.04 of paid usage, $0.0021 per send-ready contact |

## ICP Definition

ICP statement: VP Sales and CRO at US B2B SaaS companies with 50-200 employees, excluding agencies and staffing firms.

| Evidence account | Domain | Outcome | Industry | Employees | HQ | Buyer title | Why it counts |
|-|-|-|-|-|-|-|-|
| Ledgerline | ledgerline.example | won | Computer Software | 85 | Austin, TX | VP Sales | Signed in 9 days, renewed for a second cohort |
| Shipwise | shipwise.example | won | Computer Software | 140 | Denver, CO | Chief Revenue Officer | Referred two other customers |
| Clinicflow | clinicflow.example | won | Hospital and Health Care software | 62 | Nashville, TN | VP Sales | Team quota attainment cited in their case study |
| Brightpath HR | brightpathhr.example | won | Human Resources software | 190 | Chicago, IL | Head of Sales | Expanded from 6 to 14 reps in the program |
| Quotient Labs | quotientlabs.example | won | Computer Software | 110 | Raleigh, NC | VP Sales | Bought after one call, no discount |
| Brandloop | brandloop.example | churned | Marketing and Advertising | 70 | Miami, FL | Founder | Agency; reps sell client retainers, program did not fit, left after 4 months |
| Talentrail | talentrail.example | lost | Staffing and Recruiting | 120 | Phoenix, AZ | VP Sales | Recruiter desks, not a sales team; lost on fit in discovery |

Shared traits used as filters: B2B SaaS business model (5 of 5 won), 62-190 employees (5 of 5, banded to 50-200), US person location (5 of 5), sales leader title at VP or CRO level (5 of 5).

Exclusions: agency and staffing, shared by the churned and the lost account and absent from all 5 won. Left out after you agreed: healthcare vertical (1 of 5), HR vertical (1 of 5), Series B funding (2 of 5), Texas HQ (1 of 5).

## Filters Used

| Parameter | Value | Evidence |
|-|-|-|
| title | VP Sales, Vice President of Sales, VP of Sales, Head of Sales, Chief Revenue Officer, CRO | Buyer titles at all 5 won accounts plus synonyms |
| notTitle | assistant, intern, former, retired, advisor, board, investor, operations, enablement, engineer | Sales leader exclusion set plus the two stray families found at the first count |
| keywords | saas, b2b | Tags present on 5 of 5 won accounts |
| notKeywords | agency, staffing | The fit losses |
| minEmployees / maxEmployees | 50 / 200 | Won accounts span 62-190 |
| country | United States | All 5 buyers sit in the US |
| hasEmail | true | Email campaign |

## Count Check

| Call | pagination.total | Decision |
|-|-|-|
| Title, keywords, notKeywords, size, country, hasEmail | 4,388 | 2.9x the 1,500 target; of the first 100 rows, 16 were sales operations or sales engineers, so their words went into notTitle |
| Recount with notTitle added | 3,412 | Pull 2,000 (1,500 / 0.75 yield) |

You approved the pull and the $3.04 validation spend in chat on 2026-10-12.

## Pull Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Matched | 3,412 | 0 | Starting point |
| Pulled | 2,000 | 1,412 | Planned pull, 20 pages of 100 with cursor paging |
| After normalization | 1,974 | 26 | 19 broken email syntax, 7 rows with no first name |
| After dedupe | 1,936 | 38 | Same email listed twice under two title variants |
| After suppression | 1,800 | 136 | 41 current customers, 88 inside your 60-day re-contact window, 7 unsubscribes |
| Valid after validation | 1,512 | 288 | 216 catch-all and unknown to the hold file, 72 invalid and disposable removed |
| Send-ready after per-company cap | 1,480 | 32 | Fourth and later contacts at one company (your cap is 3) |

## Validation Results

| Bucket | Count | Share | Action |
|-|-|-|-|
| valid | 1,512 | 84.0% | Send file |
| catch_all | 171 | 9.5% | Hold file; its own 100-contact cell after the test cell passes |
| unknown | 45 | 2.5% | Re-validate once on 2026-10-15 |
| invalid | 68 | 3.8% | Removed, added to bounce suppression |
| disposable | 4 | 0.2% | Removed and suppressed |
| Total validated | 1,800 | 100% | One Email Validator run |

Fit sample: 60 random send-file rows checked by hand on 2026-10-12: title 60 of 60, company 59 of 60 (one company had grown to 240 employees; kept, size data lags), location 60 of 60, domain resolves 60 of 60, person still there 60 of 60. No miss traces to a filter word, so the filters stand.

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Lead Database counts and pull | 2,002 leads, 2% of the 100,000 daily allowance | Included in Growth | $0.00 |
| Email Validator | 1,800 emails | $0.00169 | $3.04 |
| Total paid usage | | | $3.04 |

Prices: ScraperCity pricing page and tool catalog, checked 2026-10-12, matching the wallet change.

## Output Schema

| Column | Example | Rule |
|-|-|-|
| first_name, last_name | Dana, Whitfield | Normalized case, suffixes moved out |
| title | VP of Sales | As returned |
| title_normalized | vice president of sales | Lowercase, abbreviations expanded |
| seniority | vp | Derived from title |
| email | dana.whitfield@ledgerline.example | Lowercased |
| email_status | valid | valid only in the send file |
| email_validated_at | 2026-10-12 | ISO date |
| company_name, company_domain | Ledgerline, ledgerline.example | Registrable domain |
| company_employees | 85 | Integer |
| person_state | TX | USPS code; sets send time |
| source, source_detail | lead_db; title=VP Sales...;keywords=saas,b2b;emp=50-200;country=US | Query fingerprint for a rerun |
| segment | saas-50-200-vp-sales | Campaign slice |

Files: `icp-list-saas-vp-sales-2026-10-12.csv` (1,480 rows, sorted by company_domain) and `icp-list-saas-vp-sales-2026-10-12-hold.csv` (216 rows).

## Next Steps

| # | Step | Owner | Date | Done when |
|-|-|-|-|-|
| 1 | Import the send file to the sequencer with cross-campaign duplicate checking on and the shared suppression list connected | SDR lead | 2026-10-13 | 1,480 rows imported, 0 flagged as duplicates |
| 2 | Send a 100-contact test cell, the size Alex Berman tests a niche with (Lean B2B interview, December 2020) | SDR lead | 2026-10-13 | Bounces under 2% (alexberman.com cold email templates): release the rest |
| 3 | Re-validate the 45 unknown rows | Agent | 2026-10-15 | Each one moved to valid, catch-all or removed |
| 4 | Hold file as its own 100-contact cell | SDR lead | 2026-10-20 | Same 2% line: release or drop |
| 5 | Sort replies by title; when referral replies from Head of Sales keep naming one other title, swap that title in on the next pull | SDR lead | 2026-11-10 | Title list for cycle 2 set |
