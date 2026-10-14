# Research Playbook

The procedures behind each brief section: Lead Database calls for the snapshot and team counts, finding the people, the signal catalog, reading public filings, writing talking points, planning contact order, and recipes by account type. Prices from `references/scrapercity-catalog.md`.

## 1. Snapshot calls

Run these in order. Each is a `query_lead_database` call that costs nothing from the wallet; returned records count toward the 100,000 a day allowance only if the account does not have them yet.

| # | Call | Read |
|-|-|-|
| 1 | `{"companyDomain": "acme.example", "limit": 1}` | Company fields on the row; `pagination.total` = people the database holds for the domain |
| 2 | Same plus the buyer's department titles, `limit: 1` | Size of the team the product serves |
| 3 | Same plus `seniority: ["vp", "c_suite"]`, `limit: 25` | The leadership layer, to spot new names |
| 4 | If 0 results: `{"companyName": "Acme", "limit": 5}` | Alias domains, parent company, regional sites |

Team-size count recipes (title strings for call 2):

| Product sells to | `title` |
|-|-|
| Sales teams | Account Executive, Sales Representative, Business Development, Sales Manager, SDR, BDR |
| Marketing teams | Marketing Manager, Demand Generation, Content, Growth, Marketing Operations |
| Engineering | Software Engineer, Developer, DevOps, Site Reliability, Engineering Manager |
| Finance | Accountant, Controller, Accounts Payable, FP&A, Financial Analyst |
| Customer support | Customer Support, Customer Success, Support Specialist, Customer Service |
| HR and recruiting | Recruiter, Talent Acquisition, HR Generalist, People Operations |
| Operations and plants | Plant Manager, Production Supervisor, Operations Manager, Quality |

Write the count into the brief as a number with its basis: "41 people with sales titles in the Lead Database, 2026-10-13". Database counts are a floor; say so.

## 2. Finding the people

| Slot | MEDDIC role | How to find | Fallback |
|-|-|-|-|
| 1 | Economic buyer | `query_lead_database` with the role map titles and `seniority: ["vp", "c_suite"]` | `scrape_website_finder` with the top title |
| 2 | Champion | Same, `seniority: ["director"]` or manager titles | Website Finder with the champion title |
| 3 | Evaluator or technical owner | Title list only (admin, architect, operations) | Website Finder |
| 4 | Backup | Second-ranked candidate in slot 1 or 2 | None |

Ranking inside a slot: exact title match, then higher seniority, then email present, then person located at HQ. A person new in the role goes to the top of the contact plan, since a new leader is a transition trigger (Elias).

Emails: `find_emails` for any person with a name and no email ($0.05 if found, free if not); `validate_emails` for every Lead Database and Website Finder email ($0.0072 each). Mark `valid` as ready, `valid_catch_all` as "send with care", `unknown`, `invalid` and `disposable` as not ready.

Person-level details to look for (cite each):

| Detail | Where | Use |
|-|-|-|
| Start date in the role | Company newsroom, the person's profile | Transition trigger |
| A recent post or talk on the problem | The person's posts, conference agendas, podcasts | Opening line in their words |
| Previous company used the user's product or a competitor | Profile history | Case study choice |
| Team they inherited or are building | Job postings that report to them | Size of the problem |

## 3. Reading the Lead Database row

| Field | Caution |
|-|-|
| `company_industry` | Broad labels; confirm against the website's own description |
| `employees_count`, `company_size` | Lags hiring; cross-check with the careers page if the company is growing fast |
| `company_annual_revenue` | Estimate for private companies; quote as "about" |
| `keywords` | Useful for the one-line description and for finding lookalikes later |
| `company_website` | Confirms the domain; a different domain here means an alias or parent |

## 4. Signal catalog

Each signal gets a date, an Elias category, a source ID and a line on what it suggests.

| Signal | Elias category | Where to look | What it suggests |
|-|-|-|-|
| A champion at one of the seller's customers now works here | Transition | CRM contact history; a Sales Navigator lead list of customer champions filtered by Changed jobs | Warm opener from a known user; contact them before anyone else |
| Closed-lost on timing, or a past demo | Transition | CRM opportunity history | The reason they gave last time is the first question this time |
| New executive in the buyer's function | Transition | Newsroom, 8-K Item 5.02, the executive's profile | A new buyer, one of Elias's transitions |
| Job posting for a role that would own or use the product | Transition | Careers page | Budget and a project exist |
| Job posting naming a competitor or a tool to replace | Transition | Careers page | Stack in flux; a migration window |
| New office, region or product line | Transition | Newsroom | Process strain from growth |
| Funding round or acquisition | Transition | Newsroom, filings | New targets from the board; integration work |
| Layoffs or a hiring freeze | Transition | News, filings | Efficiency pitch; slower signatures |
| New industry standard or rule with a deadline | Transition | Trade press, industry association news | A project with a fixed date and a budget |
| Public complaint about a current vendor | Bad experience | Review sites, the executive's posts | Window of dissatisfaction |
| Outage, recall or quality incident | Bad experience | News, recall listings, the company's own notices | Urgent fix, often with budget |
| Executive talks about the problem in public | Awareness | Podcasts, posts, conference talks | Language to mirror in the email |
| Peer company announced a result with a solution like the user's | Awareness | Case studies, trade press | Fear of falling behind |

Rules:

1. Primary sources first: the company's own pages and filings, then the person's own words, then press.
2. Signals older than the cutoff the user sets go under background in the brief.
3. Two signals of the same kind (two job postings) count as one signal with two sources.
4. No signal found within the time box: say so. The brief leads with the segment-level angle and the contact plan stays.

## 5. Public company filings

| Filing | Section | What it gives the brief |
|-|-|-|
| Form 10-K | Item 1, Business | How the company describes itself, segments, customers |
| Form 10-K | Item 1A, Risk Factors | Problems the company names in its own words |
| Form 10-K | Item 7, MD&A | Results, cost pressure, priorities by segment |
| Form 10-Q | MD&A | Changes since the annual report |
| Form 8-K | Item 5.02 | Departures and appointments of certain officers |
| Form 8-K | Items 1.01, 2.01 | Material agreements, acquisitions |
| DEF 14A (proxy) | Executive compensation | Metrics leaders are paid on |

Search: EDGAR full-text search for the company name and a topic word ("customer churn", "ERP implementation"). Quote at most one short phrase per filing in the brief; paraphrase the rest and cite the filing.

## 6. Hypothesis and talking points

Hypothesis, two sentences: "[Company] likely [pain] because [signal]. The [role] is judged on [metric], so [what changes this quarter]."

Talking point rules:

| Rule | Example |
|-|-|
| One fact, one implication, one source | "Posted a Revenue Operations Manager role on 2026-09-22 that names Salesforce and HubSpot [S3]: the two systems are being reconciled by hand." |
| Phrase it as a question the rep can ask | "How are leads routed between HubSpot and Salesforce today?" |
| Tie at least one point to the economic buyer's metric | "Forecast accuracy for a new CRO's first board meeting" |
| A point without a source | Cut it |
| A compliment that could fit any company | Cut it |

Open questions for the call come from the MEDDIC letters the brief cannot fill: Metrics, Decision Criteria, Decision Process.

Language bank: collect the phrases the buyer or the company used for the problem (a podcast line, a post, the wording of their own job posting) with the source ID. Talking points and the first email use those words; a phrase from the seller's website is not a substitute.


## 7. Contact plan rules

| Rule | Source |
|-|-|
| One person at the account at a time; never two at once, since that can get the sender blocked company wide | Berman, Single Grain video and Lean B2B interview |
| Start with the most senior relevant person; move down a level after one to two weeks without a reply | Same |
| A new executive goes first, with the transition trigger in the opener | Elias, transitions |
| Email first, then a call, then a LinkedIn connection | Berman, cold calling techniques article (his roughly 12 day sequence) |
| Phone only for a planned call, after the do-not-contact check | One do-not-contact list across every tool |
| Warm path before cold email: a colleague connected to the economic buyer (Sales Navigator TeamLink or "Connections of") asks for an introduction on Day 1 | LinkedIn Sales Solutions blog (2018): buyers are five times more likely to engage through a mutual connection |

## 8. Recipes by account type

| Account type | Snapshot extras | People slots | Technologies often checked | Signal sources |
|-|-|-|-|-|
| B2B SaaS, 50-500 employees | Sales and engineering team counts | CRO or VP Sales, RevOps, Sales Ops admin | CRM, marketing automation | Careers page, funding news |
| Manufacturer | Plant count from the website | VP Operations, Plant Manager, Quality | ERP (only when the product integrates) | Trade press, recall listings, plant expansion news |
| Hospital or health system | Bed count or locations from the website | CFO or COO, Director of Revenue Cycle, IT | EHR (only when the product integrates) | Newsroom, local news, new-facility announcements |
| Ecommerce brand | Store platform, monthly visit band from Store Leads | Founder or Head of Ecommerce, Retention Marketing | Store platform, email or SMS platform | Product launches, new retail partners |
| Agency or professional services | Team page headcount | Founder or Managing Partner, Ops lead | Project management, CRM | Client wins, new service lines |
| Multi-location local business | Location count from the Local Business Database | Owner, Operations Director, General Manager | Booking or POS (only when it flips the pitch) | New locations, reviews |
| Public company | Segments from the 10-K | Division VP, Director, evaluator | Rarely needed; filings name systems | 10-K, 10-Q, 8-K |

## 9. Time box checklist (Standard tier)

Split the user's time box across these tasks, in this order:

| Order | Task |
|-|-|
| 1 | Snapshot and team counts (section 1) |
| 2 | People, emails, validation (section 2) |
| 3 | Tech stack decision, free signals, Tech Stack Search if approved |
| 4 | Signals (section 4), filings for public companies |
| 5 | Hypothesis, talking points, contact plan, checker |

## Sources

- ScraperCity MCP tool schemas: https://www.npmjs.com/package/scrapercity
- Craig Elias, What's the BIG deal about trigger events: https://customerthink.com/whats_big_deal_about_trigger_events/
- SEC, EDGAR full-text search: https://www.sec.gov/edgar/search/
- SEC, Form 10-K instructions: https://www.sec.gov/files/form10-k.pdf
- SEC, Form 8-K instructions: https://www.sec.gov/files/form8-k.pdf
- MEDDICC, Who created MEDDIC: https://meddicc.com/resources/who-created-meddic
- Alex Berman, Single Grain video: https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- Lean B2B, Alex Berman on B2B market segments: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- LinkedIn, Sales Navigator compare plans (TeamLink, Relationship Explorer): https://business.linkedin.com/sales-solutions/compare-plans
- LinkedIn Sales Solutions blog, TeamLink (2018): https://business.linkedin.com/sales-solutions/blog/sales-tools/2018/vast-networks--how-to-connect-your-sales-circles-with-teamlink
- Alex Berman, Cold calling techniques: https://alexberman.com/cold-calling-techniques
