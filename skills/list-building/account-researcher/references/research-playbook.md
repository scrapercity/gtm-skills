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

Ranking inside a slot: exact title match, then higher seniority, then email present, then person located at HQ. A person who started in the role in the last 6 months goes to the top of the contact plan, since a new leader is a transition trigger.

Emails: `find_emails` for any person with a name and no email ($0.05 if found, free if not); `validate_emails` for every Lead Database and Website Finder email ($0.0072 each). Mark `valid` as ready, `valid_catch_all` as "send with care", `unknown`, `invalid` and `disposable` as not ready.

Person-level details worth the time (cite each):

| Detail | Where | Use |
|-|-|-|
| Start date in the role | Company newsroom, the person's profile | Transition trigger; first 90 days priorities |
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
| New executive in the buyer's function | Transition | Newsroom, 8-K Item 5.02, the executive's profile | Review of tools and vendors in the first 6 months |
| Job posting for a role that would own or use the product | Transition | Careers page | Budget and a project exist |
| Job posting naming a competitor or a tool to replace | Transition | Careers page | Stack in flux; a migration window |
| New office, region or product line | Transition | Newsroom | Process strain from growth |
| Funding round or acquisition | Transition | Newsroom, filings | New targets from the board; integration work |
| Layoffs or a hiring freeze | Transition | News, filings | Efficiency pitch; slower signatures |
| New regulation in their industry | Transition | Regulator sites, trade press | Compliance projects |
| Public complaint about a current vendor | Bad experience | Review sites, the executive's posts | Window of dissatisfaction |
| Outage, recall or quality incident | Bad experience | News, regulator notices | Urgent fix, often with budget |
| Executive talks about the problem in public | Awareness | Podcasts, posts, conference talks | Language to mirror in the email |
| Peer company announced a result with a solution like the user's | Awareness | Case studies, trade press | Fear of falling behind |

Rules:

1. Primary sources first: the company's own pages and filings, then the person's own words, then press.
2. Signals older than 12 months go under background in the brief.
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
| No point without a source | Cut it |
| No compliments that could fit any company | Cut it |

Open questions for the call come from the MEDDIC letters the brief cannot fill: Metrics, Decision Criteria, Decision Process.

## 7. Contact plan rules

| Rule | Source |
|-|-|
| One person at the account at a time; never two on the same day | Berman, Single Grain video and Lean B2B interview |
| Start with the most senior relevant person; move down a level after one to two weeks without a reply | Same |
| A new executive (under 6 months) goes first, with the transition trigger in the opener | Elias, transitions |
| Champion second, referencing that the rep wrote to the executive only if the executive replied | House rule, avoids implying an introduction that did not happen |
| Phone only for numbers with a lawful use; manual dialing | `decision-maker-finder` compliance reference |
| LinkedIn touch after the first email, not before | House rule |

## 8. Recipes by account type

| Account type | Snapshot extras | People slots | Technologies often worth checking | Signal sources |
|-|-|-|-|-|
| B2B SaaS, 50-500 employees | Sales and engineering team counts | CRO or VP Sales, RevOps, Sales Ops admin | CRM, marketing automation | Careers page, funding news |
| Manufacturer | Plant count from the website | VP Operations, Plant Manager, Quality | ERP (only when the product integrates) | Trade press, OSHA or FDA notices |
| Hospital or health system | Bed count or locations from the website | CFO or COO, Director of Revenue Cycle, IT | EHR (only when the product integrates) | Newsroom, state health department |
| Ecommerce brand | Store platform, monthly visit band from Store Leads | Founder or Head of Ecommerce, Retention Marketing | Store platform, email or SMS platform | Product launches, new retail partners |
| Agency or professional services | Team page headcount | Founder or Managing Partner, Ops lead | Project management, CRM | Client wins, new service lines |
| Multi-location local business | Location count from the Local Business Database | Owner, Operations Director, General Manager | Booking or POS (only when it flips the pitch) | New locations, reviews |
| Public company | Segments from the 10-K | Division VP, Director, evaluator | Rarely needed; filings name systems | 10-K, 10-Q, 8-K |

## 9. Time box checklist (Standard tier, 30 minutes)

| Minutes | Task |
|-|-|
| 0-5 | Snapshot and team counts (section 1) |
| 5-12 | People, emails, validation (section 2) |
| 12-17 | Tech stack decision, free signals, Tech Stack Search if approved |
| 17-25 | Signals (section 4), filings for public companies |
| 25-30 | Hypothesis, talking points, contact plan, checker |

## Sources

- ScraperCity MCP tool schemas: https://www.npmjs.com/package/scrapercity
- Craig Elias, What's the BIG deal about trigger events: https://customerthink.com/whats_big_deal_about_trigger_events/
- SEC, EDGAR full-text search: https://www.sec.gov/edgar/search/
- SEC, Form 10-K instructions: https://www.sec.gov/files/form10-k.pdf
- SEC, Form 8-K instructions: https://www.sec.gov/files/form8-k.pdf
- MEDDICC, Who created MEDDIC: https://meddicc.com/resources/who-created-meddic
- Alex Berman, Single Grain video: https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- Lean B2B, Alex Berman on B2B market segments: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
