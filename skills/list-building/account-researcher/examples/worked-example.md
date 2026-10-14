# Account Brief: Harborline Logistics (harborlinelogistics.example)

Prepared 2026-10-13 for the account executive team at Northwind RevOps. Seller: a 90-day CRM and pipeline rebuild for sales teams of 20-100 reps. Purpose: first cold email to a tier 1 account. Depth tier: Standard.

_Illustrative example. Company, people, URLs and run results are invented to show the format and use the reserved `.example` domain. Prices are ScraperCity catalog prices._

## Account Snapshot

| Field | Value | Source |
|-|-|-|
| Description | Asset-light freight brokerage moving truckload and LTL freight for mid-size shippers, with carrier sales and shipper sales teams | S1, S7 |
| Industry | Transportation, trucking and logistics (keywords: freight brokerage, truckload, 3pl, logistics) | S1 |
| Employees | About 350 (Lead Database), careers page lists 14 open roles | S1, S3 |
| Revenue | About $140M a year (estimate for a private company) | S1 |
| HQ | Chicago, IL; second office in Dallas, TX opened May 2026 | S1, S4 |
| People in Lead Database | 64 people at the domain, 2026-10-13 | S1 |
| Team the product serves | 41 people with sales titles (account executive, carrier sales, business development, sales manager); a floor, since database counts lag hiring | S1 |

## Why Now

| Signal | Date | Elias category | What it suggests | Source |
|-|-|-|-|-|
| Renee Calloway named Chief Revenue Officer, coming from a larger 3PL | 2026-07-08 | Transition | A new buyer in the revenue seat, the transition Elias describes | S2 |
| Job posting: Revenue Operations Manager, "own Salesforce and HubSpot, rebuild lead routing and reporting" | 2026-09-22 | Transition | A rebuild has budget and an owner is being hired; a 90-day outside project can run before the hire is productive | S3 |
| Dallas office opened with 25 new sales hires planned | 2026-05-14 | Transition | Onboarding and pipeline hygiene strain as the team grows by more than half | S4 |
| VP Sales Marcus Bell on a freight sales podcast: forecast calls "take half a day" | 2026-08-30 | Bad experience | Forecasting pain stated by the person who runs the team | S5 |

Background (older than 12 months, the cutoff the team set): a 2024 trade-press profile on Harborline's switch from spreadsheets to Salesforce; useful context, not a trigger.

## Tech Stack

| Technology | Status | Evidence | Changes pitch? | Source |
|-|-|-|-|-|
| Salesforce | confirmed | Domain present in the Tech Stack Search list for Salesforce; also named in the RevOps job posting | yes | S3, S6 |
| HubSpot | confirmed | Domain present in the Tech Stack Search list for HubSpot; `js.hs-scripts.com` tracking script on the homepage | yes | S6, S7 |
| Microsoft 365 mail with Mimecast gateway | confirmed | `sc_mx_provider` and `sc_mx_security_gateway` columns from Email Validator | no | S8 |
| Gong | likely | Named once in the RevOps job posting; not checked with Tech Stack Search because it does not change the pitch | no | S3 |

Pitch consequence: both Salesforce and HubSpot are live, so the opening angle is lead routing and attribution between the two, backed by the user's case study for a 60-rep logistics team on the same pair. The first email goes out in plain text with no link.

## Key People

| Name | Title | Buying role | Email | email_status | found_by | Notes |
|-|-|-|-|-|-|-|
| Renee Calloway | Chief Revenue Officer | Economic buyer | renee.calloway@harborlinelogistics.example | valid | lead_db | Started 2026-07; previously ran sales operations at a larger 3PL (S2) |
| Priya Natarajan | Director of Sales Operations | Champion | priya.natarajan@harborlinelogistics.example | valid | email_finder | Hiring manager on the RevOps posting (S3) |
| Jordan Ames | Salesforce Administrator | Evaluator | jordan.ames@harborlinelogistics.example | valid | website_finder | Two years in role; would own the technical review |
| Marcus Bell | VP Sales | Backup economic buyer | marcus.bell@harborlinelogistics.example | valid | lead_db | Podcast guest on forecasting pain (S5); reports to the CRO |

## Hypothesis and Talking Points

Hypothesis: Harborline likely loses leads and forecast accuracy between HubSpot and Salesforce as the Dallas team ramps, and the new CRO needs a forecast she trusts before her first board review. The RevOps hire signals the budget exists, and an outside 90-day rebuild finishes before a new manager would be productive.

| # | Talking point | Question for the rep to ask | Source |
|-|-|-|-|
| 1 | The RevOps posting asks for someone to "rebuild lead routing and reporting" across Salesforce and HubSpot, so routing is being handled by hand today | How are inbound leads routed from HubSpot to the right rep in Salesforce right now? | S3, S6 |
| 2 | The CRO started in July and owns the forecast process she inherited | What does the forecast need to show at the first board review? | S2 |
| 3 | 25 new reps in Dallas means onboarding into a CRM that is being rebuilt at the same time | How long until a new Dallas rep has a usable pipeline view? | S4 |
| 4 | Marcus Bell said forecast calls take half a day; the case study cut that to under an hour for a logistics team on the same stack | What eats the time in the weekly forecast call today? | S5, S6 |

## Contact Plan

| Order | Person | Channel | Day | Angle |
|-|-|-|-|-|
| 1 | Renee Calloway | Email, plain text, no links | Day 1 | New CRO, routing between HubSpot and Salesforce, logistics case study, one question |
| 2 | Priya Natarajan | Email | Day 9 | Only if no reply from the CRO; the RevOps posting and a 90-day bridge before the hire starts |
| 3 | Marcus Bell | LinkedIn connection, then email | Day 16 | His podcast comment on forecast calls |
| 4 | Jordan Ames | Held until a conversation starts | Day 23 | Technical review only after a meeting is booked |

Warm path check: no one on the Northwind team is connected to Renee Calloway or Marcus Bell in Sales Navigator TeamLink, so Day 1 is a cold email. No mobile numbers requested for this account.

## Sources

| ID | Source | URL | Date checked |
|-|-|-|-|
| S1 | ScraperCity Lead Database, lookup by company domain plus two team-count calls | https://app.scrapercity.com/api/v1/database/leads?companyDomain=harborlinelogistics.example | 2026-10-13 |
| S2 | Harborline newsroom, CRO appointment | https://harborlinelogistics.example/news/renee-calloway-cro | 2026-10-13 |
| S3 | Harborline careers page, Revenue Operations Manager posting | https://harborlinelogistics.example/careers/revenue-operations-manager | 2026-10-13 |
| S4 | Harborline newsroom, Dallas office announcement | https://harborlinelogistics.example/news/dallas-office | 2026-10-13 |
| S5 | Freight Sales Floor podcast, episode 142 with Marcus Bell | https://freightsalesfloor.example/episodes/142 | 2026-10-13 |
| S6 | ScraperCity Tech Stack Search runs for Salesforce (run 5c2e91aa) and HubSpot (run 7b10d4ee) | https://app.scrapercity.com/api/v1/scrape/status/5c2e91aa | 2026-10-13 |
| S7 | Harborline homepage, page source | https://harborlinelogistics.example | 2026-10-13 |
| S8 | ScraperCity Email Validator run on 3 emails (run 1e8f3a02) | https://app.scrapercity.com/api/v1/scrape/status/1e8f3a02 | 2026-10-13 |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Lead Database snapshot, 2 team counts, 9 people | 12 records | Included in Growth plan | $0.00 |
| Tech Stack Search (Salesforce, HubSpot) | 2 technologies | $4.99 per technology | $9.98 |
| Website Finder, Salesforce Administrator | 1 contact found | $0.0499 | $0.05 |
| Email Finder, Director of Sales Operations | 1 email found | $0.05 | $0.05 |
| Email Validator | 3 emails | $0.0072 | $0.02 |
| Total paid usage | | | $10.10 |

The user approved the $9.98 Tech Stack Search spend on 2026-10-13. Both technology CSVs are saved as `techstack-salesforce-20261013.csv` and `techstack-hubspot-20261013.csv`; checking the other 24 tier 1 accounts against them costs nothing more, which brings the Tech Stack Search cost to $0.40 per account.

## Open Questions and Next Steps

Open questions for the first call: the metric the CRO will be judged on this year, who besides the CRO signs a services contract, and whether the RevOps hire changes the timeline.

| # | Step | Owner | Date | Done when |
|-|-|-|-|-|
| 1 | Write the Day 1 email from talking points 1 and 2 in Bell's and the posting's own words ("rebuild lead routing", forecast calls that "take half a day"), plain text, under 75 words (Berman's templates page), ending in one question | AE | 2026-10-14 | Email sent to Renee Calloway |
| 2 | Run the other 24 tier 1 domains against the saved Salesforce and HubSpot CSVs and add the results to each account's brief | Agent | 2026-10-15 | 24 briefs updated |
