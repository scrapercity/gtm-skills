# ICP List Plan: Maintenance software buyers at US food and beverage manufacturers, 200-2,000 employees

_Illustrative example of a plan report. The seller, Plantline Software (CMMS for food plants), is invented. Government and survey figures are real and cited; prices are ScraperCity catalog prices._

Status: Plan, prepared 2026-10-13. No ScraperCity call has run in this session; the free counts at step 2 replace the Census estimates with database figures.

## Answer

| Question | Answer |
|-|-|
| How many companies? | Up to 1,228 US firms with 200-1,999 employees run at least one food or beverage plant (Census SUSB 2022). The deduped database count at step 3 replaces this. |
| How many contacts? | 6,140 to 13,508 people sit in those buying groups (1,228 firms x 5 to 11 people per group, Gartner B2B Buying Report, 2022 survey). The plan validates the 3,118 its tier caps select. |
| How to tier them? | Three tiers by firm size, 4, 3 and 2 contacts per account (table under Account Tiers). A new plant, a new plant leader or maintenance hiring lifts an account one tier for the next send cycle. |
| What does it cost? | $149 for one month of Growth. Paid usage is at most $44.74 and fits inside the plan's $159 monthly credit. |
| How do you get verified emails? | Validate only the tier-selected contacts, send only `valid`, hold catch-all and unknown, then release through a 100-contact test cell that must stay under 2% bounces. Steps, owners and dates are under Next Steps. |

## ICP Definition

ICP statement: Plant operations, maintenance and reliability, IT and executive leaders at US food and beverage manufacturers with 200-2,000 employees that run their own plants, excluding distributors, brokers, restaurant groups and brands that use co-manufacturers for all production.

Evidence: none supplied. Send 3-5 best-fit and 2-5 lost account domains; I will look each one up in the Lead Database and confirm the size band, the plant types and the title that signed.

## Filters Used

Shared by the four role-family queries:

| Parameter | Value | Why |
|-|-|-|
| keywords | food manufacturing, food processing, beverage manufacturing, bakery, meat processing, dairy, co-packer | Plant operators; co-packers run plants for brands |
| notKeywords | food distribution, foodservice distributor, food broker, restaurant, grocery, catering, software | Business types with no plant to maintain |
| minEmployees / maxEmployees | 200 / 2,000 | Your band; the edge pass at step 4 adds firms the database lists low |
| companyCountry | United States | US headquarters |
| hasEmail | true | Email campaign; Tier 1 slots with a name and no email go to Email Finder |
| industry | Added after the evidence lookups | The label is copied from a customer's record, never typed |

Per role family:

| Family | title | notTitle |
|-|-|-|
| Economic buyer | CEO, Chief Executive Officer, President, Owner, Co-Owner, Founder, Co-Founder, Managing Partner, COO, Chief Operating Officer, CFO, Chief Financial Officer | vice, assistant, coordinator, product owner, process owner, former, board, investor, advisor, division, regional, sales |
| Operations | VP Operations, SVP Operations, Director of Operations, VP Manufacturing, Director of Manufacturing, Plant Manager, General Manager | assistant, intern, former, sales, supervisor, coordinator, lead |
| Maintenance and reliability | Director of Maintenance, Maintenance Director, Maintenance Manager, Reliability Manager, Director of Reliability, Director of Engineering, Engineering Manager, Plant Engineer, Director of Facilities | technician, mechanic, electrician, planner, scheduler, intern, former, sales, software |
| IT | CIO, Chief Information Officer, VP IT, VP Information Technology, Director of IT, IT Director, Director of Applications | help desk, support, technician, analyst, intern, former |

Owner, Founder and Managing Partner are in the economic-buyer family because family-owned and founder-led firms use those titles for the person who signs. "vice" stops "President" from matching every Vice President, and "coordinator" stops "COO" from matching Coordinators.

## Count Check

| Call | Result | Decision |
|-|-|-|
| Census SUSB 2022, firms with 200-1,999 employees and a plant in NAICS 311 (food) or 3121 (beverage) | 1,095 food + 133 beverage = 1,228 firms; a firm with both plant types counts in each, so 1,228 is a ceiling | Benchmark for the database company count |
| Lead Database, one `limit: 1` count per role family | Step 2 | Read the first 100 rows of each; add the word behind any wrong title to notTitle and recount |
| Companies across the four pulls, deduped on company_domain | Step 3 | Below the Census figure by more than the excluded business types: widen keywords one at a time |

Employee counts in B2B data read low for plant-heavy firms, because few hourly workers keep an online professional profile: Pew Research Center (January 2024) found 10% of US adults with a high school education or less use LinkedIn, against 53% of college graduates. Step 4 adds the 100-199 band firms whose own site or press states 200-2,000 employees.

## Account Tiers

| Tier | Rule | Accounts | Contacts per account | Motion |
|-|-|-|-|-|
| 1 | 1,000-2,000 employees | 171 | 4: one per role family | Account research, a first line per person, email and LinkedIn |
| 2 | 500-999 employees | 320 | 3: operations, maintenance, economic buyer | First line per account: plant count, a trigger or news item |
| 3 | 200-499 employees | 737 | 2: maintenance, operations | Copy per plant type (bakery, meat, dairy, beverage) |
| Total | | 1,228 | | |

Accounts per tier are the SUSB size classes until the step 3 pull recuts them on database headcount.

Movers: a new plant or line announced, a new plant or operations leader (Sales Navigator "changed jobs"), or open maintenance or reliability engineering roles. Each lifts an account one tier for the next send cycle; two movers still lift one tier.

Capacity: Tier 1 is sized by headcount band. Send your AE and SDR headcount and I will cut Tier 1 to the accounts your AEs can research this quarter.

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Growth plan, includes the Lead Database and a $159 monthly credit | 1 month | $149/mo | $149.00 |
| Lead Database counts and pulls, four role families | Up to 13,508 people, inside one day's 100,000-lead allowance | Included in Growth | $0.00 |
| Email Validator, primary contact per slot | 3,118 emails (171 x 4 + 320 x 3 + 737 x 2) | $0.00169 | $5.27 |
| Email Validator, second pass per slot (backup for an invalid, or one re-check of an unknown), ceiling | 3,118 emails | $0.00169 | $5.27 |
| Email Finder, Tier 1 slots with a named person and no email, ceiling | 684 lookups | $0.05 per email found, free if none | $34.20 |
| Total paid usage, ceiling | | | $44.74 |

Prices: ScraperCity pricing page and tool catalog, checked 2026-10-13. The paid usage ceiling sits inside the $159 credit, so the cash cost is the $149 plan fee.

## Output Schema

The send file (valid only) and the hold file (catch-all and still-unknown) share these columns, joined to an account file on `company_domain`.

| Column | Example | Rule |
|-|-|-|
| first_name, last_name | Dana, Okafor | Normalized case, credentials moved out |
| title | Director of Maintenance | As returned |
| role_family | maintenance_reliability | economic_buyer, operations, maintenance_reliability, it |
| email | dana.okafor@northfieldfoods.example | Lowercased |
| email_status | valid | valid in the send file; catch_all or unknown in the hold file |
| email_validated_at | 2026-10-19 | ISO date |
| linkedin_url | https://www.linkedin.com/in/danaokafor | Lowercase, no query string |
| company_name, company_domain | Northfield Foods, northfieldfoods.example | Registrable domain |
| company_employees | 640 | From the database, or the site figure that admitted the account at step 4 |
| plant_check_url | https://northfieldfoods.example/facilities | The page that shows the company runs a plant |
| tier, tier_reason | 2, 500-999 employees; new line announced | Plain words |
| source | lead_db | lead_db, or lead_db plus email_finder |

## Next Steps

| # | Step | Owner | Date | Done when |
|-|-|-|-|-|
| 1 | Send best-fit and lost domains, suppression files (customers, open deals, past sends with dates, unsubscribes, competitor domains) and AE and SDR headcount | You | 2026-10-14 | Files received |
| 2 | Wallet and plan check; run the four free role-family counts and read the first 100 rows of each | Agent | 2026-10-14 | Four totals posted, notTitle tightened |
| 3 | Pull all four families with cursor paging; dedupe company_domain; post the company count next to the Census ceiling | Agent | 2026-10-15 | Company count posted |
| 4 | Read each company's site: keep firms with a plant or facility page (URL recorded), drop distributors, brokers and brands that use co-manufacturers. Same pass on the 100-199 band: firms whose site, press or job posts state 200-2,000 employees join | Agent | 2026-10-16 | Every account has plant_check_url and a yes or no |
| 5 | Score, tier, pick a primary and a backup per slot, apply suppression | Agent | 2026-10-16 | Slot file of 3,118 primaries |
| 6 | Approve paid usage up to $44.74 | You | 2026-10-19 | Approved |
| 7 | Validate primaries; an invalid slot gets its backup validated, an unknown gets one re-check on 2026-10-20; Tier 1 named slots with no email go to Email Finder | Agent | 2026-10-19 | Send file and hold file written, bucket counts posted |
| 8 | Fit sample: 60 random send-file rows per tier against LinkedIn or the team page (title, company, location, domain, still employed). Zero misses caps misfits under 5% at 95% confidence (3/n, Eypasch et al., BMJ 1995). A miss a filter word would have stopped means fix the filter and re-pull | SDR lead | 2026-10-20 | Counts per dimension posted |
| 9 | Test cell of 100 valid Tier 3 contacts, the size Alex Berman tests a niche with (Lean B2B interview, December 2020) | SDR lead | 2026-10-21 | Bounces under 2% (alexberman.com cold email templates): release the send file by tier |
| 10 | Hold file as its own 100-contact cell | SDR lead | 2026-10-26 | Same 2% line: release or drop |
| 11 | Next cycle: re-pull new people only, re-validate, one email per person; Alex Berman spaces cycles 30 to 60 days apart (alexberman.com TAM breakdown, October 2026) | Agent | 2026-12-18 | Cycle 2 loaded |
