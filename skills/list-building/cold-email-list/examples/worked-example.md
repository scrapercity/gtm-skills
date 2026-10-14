# Cold Email List Report: finance leaders at US construction firms, 50-500 employees

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Prepared 2026-10-13 for Ledgerpath (ledgerpath.example), an accounts payable automation tool for contractors. Plan: Growth ($149/mo). Wallet before run: $166.75. Company and person names are fictional and use the reserved `.example` domain.

## Campaign Brief

| Field | Value |
|-|-|
| Offer | Cut invoice approval time for job-site purchases; case study: a 180-person general contractor went from 11 days to 3 days per invoice |
| Segment | CFO, Controller, VP Finance and Director of Finance at US construction firms with 50-500 employees, plus 140 priority accounts from the CRM |
| Sequencer | Instantly, 6 mailboxes on 3 warmed domains |
| Launch date | 2026-10-20 |
| Personalization variables in the copy | FirstName, CompanyName, City, CaseStudy (commercial or residential version) |
| Recipient countries | United States only |
| Suppression files supplied | HubSpot customers and open deals, Instantly unsubscribes and bounces, contacts emailed inside Ledgerpath's 60-day re-contact window |

## Sourcing Plan

| Path | Input | Tool | Why |
|-|-|-|-|
| ICP pull | Title, industry, size, country filters | Lead Database with after cursors | Included in the plan; count first |
| Priority domains | 140 domains from the CRM | Lead Database with companyDomain in batches of 25 | The AE team named these accounts |
| Empty priority domains | 44 domains with no finance leader in the database | Website Finder, jobTitle Controller | One title per run, paid only on hits |
| Names without email | 15 people from the priority-domain pass | Email Finder | Free when not found; validated at lookup |

## Count Check

| Call | pagination.total | Decision |
|-|-|-|
| ICP filters without notTitle | 3,204 | 25-row read showed accounts payable clerks and assistants matching "Controller" partials |
| ICP filters with notTitle | 2,861 | Target 1,200 send-ready; pull 1,600 (1,200 / 0.75, the yield Ledgerpath measured on its last construction list) |
| Priority domains, 6 batches with finance titles | 96 | One best person per domain for 96 of 140 domains; 44 domains go to Website Finder |

User go-ahead: approved in chat on 2026-10-13 after seeing the counts and the $15.30 ceiling.

## Pipeline Funnel

| Stage | Rows | Change | Reason |
|-|-|-|-|
| ICP pull from the Lead Database | 1,600 | 0 | 16 pages of 100 with after cursors |
| Add priority-domain people | 1,696 | +96 | 81 with an email, 15 name only |
| Add Website Finder contacts | 1,715 | +19 | 19 of 44 empty domains returned a Controller |
| Drop names Email Finder could not resolve | 1,710 | -5 | 15 sent, 10 found |
| Normalization drops | 1,688 | -22 | 14 rows with no first name, 8 broken email syntax |
| Dedupe | 1,647 | -41 | Priority-domain people already in the ICP pull, matched on email and name plus domain |
| Suppression | 1,562 | -85 | 18 customers, 9 open deals, 52 emailed inside the 60-day re-contact window, 6 unsubscribes |
| Keep valid only | 1,278 | -284 | 187 catch-all to their own file, 39 unknown held, 54 invalid and 4 disposable removed |
| Per-company cap and wave split | 1,247 | -31 | Fourth and later contacts per company removed; 214 second and third contacts sit in the wave 2 file inside this count |

## Validation Results

| Status | Count | Share | Action |
|-|-|-|-|
| valid | 1,278 | 81.8% | 1,268 from Email Validator plus 10 Email Finder results validated at lookup; send file |
| valid_catch_all | 187 | 12.0% | Separate Instantly campaign at 18 sends a day (Ledgerpath's setting), started once the main campaign's first 200 sends stay under 2% bounces |
| unknown | 39 | 2.5% | Re-validate once on 2026-10-16 |
| invalid | 54 | 3.5% | Removed and added to the Instantly blocklist |
| disposable | 4 | 0.3% | Removed and added to the blocklist |
| Total validated | 1,562 | 100% | 1,552 addresses in one Email Validator run (`emailCount` 1,552) plus 10 Email Finder results |

## Send Capacity

| Item | Value |
|-|-|
| Send-ready rows | 1,247 |
| Mailboxes | 6 |
| Sends per mailbox per day | 30 |
| Daily send capacity | 180 |
| Steps per prospect | 3 |
| Total sends | 3,741 |
| Sending days | 21 |

Wave 1 holds 1,033 first contacts per company and starts 2026-10-20; wave 2 (214 rows) starts once each company's first contact finishes the sequence without a reply. Rows validated on 2026-10-13 stay inside the four-week window through 2026-11-10. Rows still unsent that day (about 250, mostly wave 2) are re-validated before their first step, about $1.80.

## Sequencer Import

| Source column | Import header | Maps to | Example |
|-|-|-|-|
| email | Email | Email (required) | dana.whitfield@ridgelinebuilders.example |
| first_name | FirstName | First Name | Dana |
| last_name | LastName | Last Name | Whitfield |
| company_name | CompanyName | Company Name | Ridgeline Builders |
| title | Title | Custom variable | Controller |
| company_city | City | Custom variable | Denver |
| case_study | CaseStudy | Custom variable | a 180-person commercial GC |
| company_domain | Website | Custom variable | ridgelinebuilders.example |
| company_contact_order | ContactOrder | Custom variable (filter only, not used in copy) | 1 |

Upload settings: CSV saved as UTF-8 with the header row first; "Check for duplicates across all campaigns" left on; 1,434 blocklist rows imported before the leads; verification at upload turned off since every row was validated on 2026-10-13.

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Lead Database ICP pull and priority domains | 1,696 leads | Included in Growth plan | $0.00 |
| Website Finder | 19 contacts found | $0.0499 | $0.95 |
| Email Finder | 10 emails found (5 free misses) | $0.05 | $0.50 |
| Email Validator | 1,552 emails | $0.0072 | $11.17 |
| Total paid usage | | | $12.62 |

Cost per send-ready row: $12.62 / 1,247 = $0.010. Wallet after run: $154.13. The 1,696 leads used under 2% of the 100,000 daily allowance.

## Sample Rows

| Email | FirstName | CompanyName | Title | City | CaseStudy | email_status |
|-|-|-|-|-|-|-|
| dana.whitfield@ridgelinebuilders.example | Dana | Ridgeline Builders | Controller | Denver | a 180-person commercial GC | valid |
| marcus.oyelaran@coppercreekcontracting.example | Marcus | Copper Creek Contracting | CFO | Phoenix | a 180-person commercial GC | valid |
| priya.raman@tallgrasshomes.example | Priya | Tallgrass Homes | VP Finance | Omaha | a 240-person residential builder | valid |
| lena.ortiz@graniteforge.example | Lena | Granite Forge Construction | Director of Finance | Charlotte | a 180-person commercial GC | valid |
| owen.castellano@bayshoreelectric.example | Owen | Bayshore Electric | Controller | Tampa | a 180-person commercial GC | valid |

## Launch Checklist

| Check | Status | Evidence |
|-|-|-|
| SPF, DKIM and DMARC pass on all 3 sending domains | done | Test message headers show dkim=pass and dmarc=pass on 2026-10-12 |
| Each mailbox warmed 14+ days | done | Mailboxes created 2026-09-15, warmup on since |
| Daily limit 30 per mailbox in Instantly | done | Campaign settings |
| Bounce auto-pause on | done | Instantly default auto-pause kept on |
| Blocklist imported before leads | done | 1,434 rows on 2026-10-13 |
| Cross-campaign duplicate check on at upload | done | Upload dialog |
| Unsubscribe in every step, removals blocklisted the same day | done | Instantly unsubscribe link on in the campaign settings |
| Every send row validated within four weeks of its send date | done | Validated 2026-10-13; re-validation of unsent rows scheduled for 2026-11-10 |
| Catch-all rows in their own campaign | done | 187 rows, 18 a day, starts once the main campaign's first 200 sends stay under 2% bounces |
| No more than one contact per company in wave 1 | done | ContactOrder = 1 for all 1,033 wave 1 rows |
| 20-row QA sample against the brief | done | 19 of 20 title fit, 20 of 20 company fit, 18 of 20 still at the company, 20 of 20 domains open the company site |
