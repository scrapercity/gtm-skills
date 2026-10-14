---
name: signal-triggered-outbound
description: >-
  Builds outbound that fires on dated events: new local listings, review and
  rating changes, tech installs and removals (Tech Stack Search), store apps
  and traffic bands, businesses for sale, pre-foreclosures, agents new to a
  market and new-to-account records from ScraperCity pulls; plus website
  visitors, job changes, new leaders, funding and Form D filings, job posts,
  earnings and SEC filings, competitor and account launches, events, webinars,
  third-party category intent and social engagement from public feeds or the
  user's tools. Gives each signal a detection method, decay, stacking and
  negative score, touch window, routing, a merge-field first email, the repeat
  pull (cron, CLI or REST, n8n, webhooks) and a dated launch plan. Use when the user
  asks for trigger-based or signal-based outbound, a funding, hiring, job
  change, earnings, launch or event play, visitor follow-up, social listening,
  "why now" lists, tech install alerts, or a weekly fresh-lead feed.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.1.0"
  author: ScraperCity
  category: outbound
  tags:
    - signals
    - trigger-events
    - intent
    - repeat-pull
    - automation
    - n8n
    - cron
    - webhooks
    - tech-stack
    - new-business
    - funding
    - hiring
    - job-change
    - earnings
    - events
    - website-visitors
  related_skills:
    - cold-email-strategy
    - cold-email-copywriting
    - cold-calling
    - multi-channel-outreach
    - outbound-unit-economics
    - ecommerce-by-techstack
    - local-business-list
    - decision-maker-finder
    - scrapercity-integrations
    - scrapercity-cli
    - scrapercity-api
    - scrapercity-real-estate-data
  frameworks:
    - "Craig Elias - Trigger Event Selling and the window of dissatisfaction"
    - "Alex Berman - trigger-based relevance and segment-first targeting"
    - "Jordan Crawford - Pain-Qualified Segments (Blueprint GTM)"
    - "UserGems - signal taxonomy and the first-90-days window for new executives"
    - "SEC EDGAR - full-text search for Form D, 8-K and 10-K/10-Q filings as a signal feed"
    - "Instantly - email sequence benchmarks 2026 (reply rates, touch spacing, re-engagement pause)"
    - "Hunter - The State of Cold Email (2025 reply rates, 3% for sales outreach)"
    - "G2 - Buyer Intent documentation (signal types and delivery)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
    - cold-email-frameworks.md
    - list-quality-standard.md
---

# Signal-Triggered Outbound

## Overview

This skill turns repeat ScraperCity pulls and free outside feeds into a queue of accounts with a dated reason to reach out this week. Each signal has a detection rule (what changed between two pulls or feeds), a date anchor, a half-life after which its score halves, a maximum age after which it is dropped, a touch window, a score, and a play: who gets it, the touch plan, and a first email that names the event in the first line.

The mistakes it prevents: calling a list "intent" when it is a static filter, emailing about a "new" listing that opened a year ago, attributing funding rounds or job posts to a tool that does not show them, opening with "congrats on the raise" instead of what the money is for, re-paying for the same records every week, and letting a hot signal sit in a spreadsheet until it is stale.

Signals S1 to S13 come from ScraperCity tools. S14 to S28 start outside ScraperCity: website visits (RB2B, Vector, Warmly), job changes and new leaders (also found by re-pulling the Lead Database), funding (Crunchbase, Form D on EDGAR), job posts (Greenhouse, Lever and Ashby public job boards), earnings and filings (EDGAR), competitor and account launches (page monitors, press feeds), events (exhibitor and speaker lists), social engagement (Octolens, F5Bot), third-party category intent (G2 Buyer Intent) and webinar or content engagement (the user's own webinar and marketing tools). Negative signals (layoffs, a hiring freeze, a competitor just signed) lower a score and pause the account. All of them score on the same formula and carry `other source: <feed>` unless a Lead Database re-pull found them. ScraperCity then finds and validates the buyer at each account, and for a competitor change pulls the competitor's install base with Tech Stack Search.

## When to Use

- "Find businesses that just opened", "alert me to new dentists in Phoenix every week".
- "Who just installed Klaviyo", "stores that started using Recharge", "sites that dropped HubSpot".
- "Which restaurants' ratings dropped", "contractors whose reviews stalled".
- "Businesses for sale in my area", "new pre-foreclosures in Tampa every Monday".
- "Set up a daily feed of new leads", "only give me records I don't already have".
- "Make our outbound trigger-based", "why-now lists", "signal scoring", "stack signals".
- "Reach companies that just raised", "Form D alerts", "companies hiring SDRs", "new VP Sales outreach".
- "A champion changed jobs", "our main contact left a customer".
- "Use their 10-K or earnings call in outreach", "competitor raised prices, who uses them", "they just launched a product".
- "Conference prospecting", "follow up after the trade show", "RB2B visitor follow-up", "social listening for buying signals".
- "Use our G2 intent data", "follow up with webinar attendees", "who downloaded the guide".

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| A one-time list with no change detection | `local-business-list`, `ecommerce-by-techstack`, `icp-list-builder` |
| Writing the emails once the angle is chosen | `cold-email-copywriting` |
| Calling tier A accounts | `cold-calling` |
| Sequencing email, phone and LinkedIn around a signal | `multi-channel-outreach` |
| Wiring n8n, Zapier or Clay in depth | `scrapercity-integrations` |
| Real estate data in depth (owners, comps) | `scrapercity-real-estate-data` |
| Cost per meeting of the signal program vs a static list | `outbound-unit-economics` |

## Prerequisites

1. ICP: category or platform, geography, size band.
2. Which events plausibly create a buying window for this offer (step 1).
3. Where snapshots live: a folder of CSVs, SQLite, Postgres, Google Sheets or Airtable.
4. Scheduler: cron on a server, n8n, Zapier, or a person running the pull every Monday.
5. Destination: sequencer (Instantly, Smartlead, Lemlist, EmailBison, ManyReach), CRM (HubSpot, Pipedrive, GoHighLevel), or a dialer.
6. ScraperCity plan. Growth ($149/mo) for the Local Business Database, Lead Database and Ecommerce Database; any plan for the scrapers.
7. Outside tools the user already pays for (visitor ID, G2, webinar platform, Crunchbase). Where none is named, the program picks one per feed and prices it from the vendor's page, for example RB2B: Free with 150 monthly resolutions, Starter $79 a month with 300, Pro from $149 (pricing page, checked 2026-10-13).
8. Owner roles for the build, tier A and tier B work; the Launch Plan dates start from today.

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Craig Elias, Trigger Event Selling (InsideSales, 2013) | A trigger event opens a "window of dissatisfaction" before the buyer starts shopping; the first viable vendor in that window wins far more often (he cites a 74% close ratio attributed to Forrester). |
| Alex Berman, alexberman.com | Targeting and offer drive results ahead of copy; a dated reason belongs in the first line, and the offer must connect to it. A roundup on his site reports trigger-based lists replying above bought lists (self-reported). |
| `references/cold-email-frameworks.md` section 8 | Trigger-based relevance: skip a trigger you cannot verify; never invent a trigger. |
| ScraperCity platform facts | `excludeDelivered=true` returns only records the account does not have; re-fetching an owned database record is free; new records count toward 100,000 a day. |
| Jordan Crawford, Blueprint GTM | A Pain-Qualified Segment groups prospects by a specific, data-detectable problem they have now. Each signal here must name the problem it detects. |
| UserGems, signals page (checked 2026-10-13) | Lists job changes, new hires, departures from customers, funding, hiring, earnings, product launches and event attendees as signal types, and says new executives re-evaluate the stack in their first 90 days (vendor claim). |
| EDGAR full-text search and investor.gov | Form D, 8-K (Item 2.02 results, Item 5.02 officer changes) and 10-K or 10-Q filings arrive as free JSON by state, form and company; Item 1A risk factors are generally ordered by importance and Item 7 holds management's own view, which is the language to quote. |
| RB2B and Vector FAQs; RB2B past-customer guide (May 2026) | Person-level visitor ID is US-only; RB2B's own sample messages open with the visit, so naming the visit is a split test, not a rule. |
| Instantly, email sequence benchmarks (March 2026); Hunter, The State of Cold Email (2025 data) | Instantly: 3.43% average reply rate; 4 to 7 emails over 14 to 21 days, first follow-up 2 to 3 days later, later ones 4 to 7 days apart; pause two to three months before re-engaging. Hunter: 4.5% across all uses, 3% for sales outreach sequences, the baseline for a sales program. |
| G2 Buyer Intent documentation (checked 2026-10-13) | Company-level signals when a buyer views your G2 profile, pricing, category, alternatives or compare pages, or a competitor's pages in a shared category; buying stage and activity level updated daily; CSV export, email alerts and integrations; signals depend on the G2 plan. |
| NAMM Show suitcasing and solicitation policy (checked 2026-10-13) | An example of show rules that bar selling to exhibitors on the floor: exhibitors may not solicit in aisles or other exhibitors' booths, and non-exhibitors may not solicit at all. Event plays ask for a meeting after the show. |

## Workflow

### 1. Pick signals that create a buying window for this offer

| Offer | Signals to track |
|-|-|
| Reviews, local SEO, websites for local businesses | New listing with few reviews; rating drop; review velocity stall |
| Email and SMS retention for Shopify stores | New Klaviyo or Recharge detection; traffic band crossing; app removed |
| Replatforming or development agencies | Domain on a legacy technology; technology removed or added |
| M&A advisors, SBA lenders, exit services, buyers | New BizBuySell listing in a category and region |
| Real estate investors, cash buyers, foreclosure attorneys | New pre-foreclosure or auction in a ZIP |
| Services sold to real estate agents (photography, CRM, leads) | Agents new to a market pull |
| Any database-backed ICP | Daily or weekly new records with `excludeDelivered=true` |
| B2B software and services | Funding or Form D stacked with a job post on the team you serve (S17, S22, S18); new leader in your buyer's function (S20) |
| Anything sold to past users | Champion moved (S16); champion left a customer (S21, account owner) |
| Enterprise accounts | Earnings release, 10-K or 10-Q priorities (S23); 8-K officer changes (S20) |
| Displacement offers | Competitor price change, sunset or launch plus its install base from Tech Stack Search (S24) |
| Services tied to a launch or expansion | Account launched a product, market or location (S25) |
| Teams that exhibit or attend shows | Exhibitors, sponsors and speakers at the event (S26) |
| Any offer, when the user has the tools | Identified website visits (S14, S15), social engagement (S19), G2 category intent (S27), webinar or content engagement (S28) |
| Every offer | Negative signals: layoffs, a hiring freeze in the buyer's team, a competitor signed (lower the score, pause the account) |

When the user asks for "anything else that works", include every signal family above that fits the offer and the tools the user has or can buy, priced; list the rest in one "Not used" line with a reason each. Do not defer a fitting family to "next quarter" without a reason the user would accept.

Full detection rules, false positives, touch windows, angles and negative signals: `references/signal-catalog.md`. Who to contact, touch plans and a full first email per outside signal: `references/signal-plays.md`.

### 2. Define each signal precisely

For each signal write: tool or feed and parameters, the diff key (domain, phone, place, listing URL, property address, accession number, posting id), the change that counts (appeared, disappeared, field crossed a threshold), the date anchor, the half-life, the max age, the touch window and the angle.

The date anchor is the date your pull first saw the change unless the source row carries its own date. A weekly pull dates every event to within 7 days; say "in the last week", never "yesterday".

### 3. Take a baseline, then pull on a schedule

The first pull is a baseline and produces no signals. Every later pull is diffed against the stored snapshot. Default cadence:

| Signal | Cadence used in the recipes | What the cost of a pull depends on |
|-|-|-|
| New local listing, review movement | Weekly | Database re-fetch of owned records is free; Maps and Yelp bill $0.0099 per row |
| Tech Stack Search adoption or removal | Weekly | $4.99 per technology per pull, flat |
| Store Leads apps, platform, traffic band | Monthly universe, weekly for apps | Store Leads bills $0.0039 per lead on every pull |
| BizBuySell | Weekly | $0.0099 per listing |
| Distress List | Weekly | $0.05 per property |
| Zillow Agents | Monthly | $0.029 per agent |
| Database `excludeDelivered` feed | Daily | Allowance resets daily |
| EDGAR Form D and 8-K, job boards | Daily or weekly | Free public endpoints |
| Lead Database re-pull for job changes and new leaders | Quarterly for champions, monthly for watched accounts | Owned records re-fetch free |
| Page monitors on competitors and accounts | Daily | Self-hosted, free |
| Visitor and social feeds | Webhook, real time | The vendor's own plan |

The cadence sets the age resolution of every signal, so pick it per signal against its cost.

### 4. Score, tier and route

Run the exclusion check first: competitors, vendors, partners, agencies, customers, open deals and do-not-contact domains get tier X and no score (`references/scoring-and-freshness.md` section 5a). Then score.

Score = fit + signal strength decayed by age + reachability, minus negative points, out of 100. Signal strength = base points x 0.5^(age in days / half-life); each further live signal adds a bonus. A negative signal (catalog section "Negative signals") subtracts its points and pauses the account for the days the program sets; at least one negative row goes in every Scoring Model. No published study gives weights, base points, half-lives or tier cut-offs for these signals, so the program sets each one, writes them in its Scoring Model and Signal Catalog, and re-fits them from its own meeting rate by age bucket. Formula, decay lookup and a worked example: `references/scoring-and-freshness.md`.

| Tier | Action | Touch window |
|-|-|-|
| A | Find the decision maker, call plus first email | Set in the program; Elias says the first viable vendor in the window of dissatisfaction wins, so measure meeting rate by days to first touch |
| B | First email in a signal-specific campaign | Set in the program |
| C | Hold; re-score next pull; drop at max age | None |

Webhook signals (S14 visits, S19 social) can be worked in minutes; weekly pulls cannot. No benchmark exists for minutes-to-touch, so log it and compare buckets.

Routing settings every program writes down: an owner per tier, what the workflow does when the owner misses the SLA (reassign, or move to the next day's batch), and who gets each signal. An identified visitor below the buyer (a rep, SDR or coordinator) is routed to the buyer at that domain with the fit-based email, which does not mention the visit; a second visitor from an account already in sequence adds to the score and goes to the second thread.

### 5. Enrich only what you will contact

Enrich after scoring, so money goes to tier A and B. Order: Lead Database by `companyDomain` (included on Growth), then `scrape_website_finder` for a named role, `find_emails` for a known name, `validate_emails` on everything, `find_mobiles` for tier A calls.

### 6. Write the angle into the first line

Name the event and its date range in plain words, connect it to the offer, ask one question (Berman: a dated reason in the first line, connected to the offer). For funding, open with what the money is for. For filings, quote management's phrase with its section. Angles per signal are in `references/signal-catalog.md`; full first emails in `references/signal-plays.md`. State the number you saw and ask about it; never claim a cause the data does not show.

Copy rules for every first email:

- Write it as a sequencer template: the event fact is a merge field (`{{open_sales_roles}}`, `{{round}}`, `{{start_month}}`), and a "Fields:" line under the email names each field's source column and one example value.
- A claim about the prospect's world ("managers hear one or two calls a month", "teams usually...") is either asked as a question or comes from the sender's own data in a field. Never state it as fact.
- Product capabilities restate what the user said about the product. Any other capability, and every proof result, goes in one "Claims to confirm" line for the user to sign off; proof results are a `{{proof_result}}` field from the user's results sheet.
- Events: shows such as NAMM bar non-exhibitors from soliciting exhibitors on the floor, and booth staff are working their own prospects. Pre-event emails go to the sales leader not on booth duty and ask for a meeting in the week after the show; a booth visit is an optional drop-by.

### 7. Suppress and cool down

One account gets one signal-triggered sequence per 90 days, whatever new signals fire; Instantly (March 2026) advises pausing two to three months before re-engaging a contact. Signals on customers, open opportunities and opted-out contacts are logged and not contacted. Stop the sequence on any reply, and remove anyone who asks the same day, across every tool.

### 8. Measure per signal

Track reply, positive reply and meeting rate by signal type and by age bucket. Once a signal reaches the contact count the program sets, retire it if it does not beat your static-list baseline from the same ICP and weeks; shorten a half-life when old signals convert at the static rate. Without a static baseline yet, compare with Hunter's 3% average reply rate for sales outreach sequences (2025 data) and Instantly's 3.43% across all sequences (2026).

## ScraperCity Implementation

| Signal | Tool | Key parameters | Diff key | Price per run |
|-|-|-|-|-|
| New local listing, few reviews | `query_local_business_database` | `keyword`, `location`, `maxReviews` (the program's cap), `excludeDelivered: true` | phone, then name plus postal code | Included in Growth; new records count toward 100,000 a day |
| New listing outside the database, fresh review counts | `scrape_maps` | `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch` | phone or place URL | $0.0099 per business |
| Rating or review change on a watched set | `scrape_yelp` | `directUrls` (the watched businesses) | Yelp URL | $0.0099 per result |
| Technology adoption or removal | `scrape_builtwith` (Tech Stack Search) | `technology`, `fileName` | domain | $4.99 per technology |
| Store app, platform, traffic band | `scrape_store_leads` | `platform`, `countryCode`, `apps`, `technologies`, `minEstimatedMonthlyVisits`, `maxEstimatedMonthlyVisits`, `planExclude`, `totalLeads`, `offset` | domain | $0.0039 per lead |
| Business listed for sale | `scrape_bizbuysell` | `startUrls`, `maxItems`, `datasetName` | listing URL | $0.0099 per listing |
| Pre-foreclosure, foreclosure, auction | `scrape_distress_list` | `search`, `distressTypes`, `maxItems` (max 500) | property address | $0.05 per property |
| Agents in a market | `scrape_zillow_agents` | `location`, `specialty`, `searchLimit` (max 500) | profile URL or name plus brokerage | $0.029 per agent |
| New-to-account records | `query_lead_database`, `query_local_business_database`, Ecommerce Database REST | `excludeDelivered: true`, `after` cursor | record id | Included in Growth |
| Contacts for scored accounts | `query_lead_database`, `scrape_website_finder`, `find_emails`, `validate_emails`, `find_mobiles` | `companyDomain`; `domains` plus `jobTitle`; names plus domain | email | $0, $0.0499 per contact found, $0.05 per email found, $0.0072 per email, $0.25 per mobile found |
| Job change, champion left (S16, S21) | `query_lead_database` | `socialUrl` per CRM champion or customer contact | LinkedIn URL plus `company_domain` | Included in Growth |
| New leader at a watched account (S20) | `query_lead_database` | `companyDomain` (several, comma separated), `seniority: ["vp", "c_suite"]`, `department` | LinkedIn URL per domain | Included in Growth |
| Competitor install base (S24) | `scrape_builtwith` (Tech Stack Search) | `technology` set to the competitor's product | domain | $4.99 per technology |
| Form D company to domain (S22) | `query_lead_database` | `companyName`, `companyState`, `limit: 5` | domain | Included in Growth |
| Event exhibitors and speakers (S26) | `query_lead_database`, `scrape_website_finder` | `companyDomain` list plus `title`; `domains` plus `jobTitle` for gaps | email | $0; $0.0499 per contact found |
| G2 intent account, webinar registrant (S27, S28) | `query_lead_database`, `validate_emails` | `companyDomain` plus buyer `title` for S27; the registrant's email or `socialUrl` for S28 | domain; email | $0; $0.0072 per email |

Three things about repeat pulls that change cost:

1. Re-fetching a Local Business Database or Lead Database record the account already owns is free, so a weekly re-pull of the same segment costs nothing on Growth. The database's refresh schedule is not published: re-pull a sample of known records on a later cycle and count changed `reviews_count` values before relying on it for review movement. If none changed, measure reviews with `scrape_maps` or `scrape_yelp`.
2. Store Leads, Maps, Yelp, BizBuySell, Distress List and Zillow Agents bill per row on every pull, including rows you saw last week. Keep those pulls narrow.
3. `excludeDelivered=true` returns records new to your account, which says nothing about when the business opened. Pair it with `maxReviews` to approximate new businesses; never call a record "just opened" from that flag alone.

MCP calls (these ids, parameters and file names stay in the agent's calls; the deliverable describes each pull in plain words):

```json
{"tool": "query_local_business_database",
 "keyword": ["med spa"], "location": ["Scottsdale AZ", "Phoenix AZ", "Tempe AZ"],
 "maxReviews": 5, "hasPhone": true, "excludeDelivered": true, "limit": 100, "page": 1}
```

```json
{"tool": "scrape_builtwith", "technology": "Klaviyo", "fileName": "techstack-klaviyo-20261019"}
```

Cron with the CLI and REST, n8n workflows, webhook handling and a stdlib diff script: `references/repeat-pull-recipes.md`. The CLI `db-local` and `db-leads` commands print only the first three rows, so scheduled database pulls use REST (`GET /api/v1/database/local-businesses`) and scrapers use the CLI or REST start, poll, download.

### Worked cost estimate (4-week cycle, Shopify retention agency)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Store Leads ICP universe, monthly (Shopify, US, 20,000 to 150,000 visits, `emails: true`) | 9,800 stores | $0.0039 | $38.22 |
| Tech Stack Search "Klaviyo", weekly | 4 pulls | $4.99 | $19.96 |
| `scrape_website_finder` founder at domains with no Lead Database contact, weekly | 7 found x 4 | $0.0499 | $1.40 |
| `validate_emails` on contacts, weekly | 36 x 4 | $0.0072 | $1.04 |
| `find_mobiles` for tier A calls, weekly | 4 found x 4 | $0.25 | $4.00 |
| Lead Database contacts by `companyDomain` | 29 x 4 | Included in Growth | $0.00 |
| Total for the cycle | | | $64.62 |

Over $5: run `check_wallet`, show this table, wait for a yes. Test the universe with `totalLeads: 100` ($0.39) first and confirm the visits filter behaves as expected. Rounding: per-line costs are rounded to the cent; the unrounded total is $64.614.

## Output Format

One Markdown signal program from `templates/output-template.md`, answer first. A title, then one paragraph: offer, ICP, buyer, the stack with one named tool per outside feed, and a single line saying which numbers are the program's starting settings and that no pulls have run (said once, nowhere else). Then these sections in order:

1. **Signal Catalog**: one row per signal with source, detection rule, date anchor, half-life, max age, base points and touch window; one "Not used" line with a reason per signal family left out.
2. **Scoring Model**: fit, strength, reachability, at least one "Negative:" row with minus points and a pause in days, the tier cut-offs, and one example line of arithmetic for one account.
3. **Exclusions**: class, match rule, list source (competitors, vendors, partners, agencies, customers and open opportunities, do not contact).
4. **Routing and SLAs**: owner, SLA and missed-SLA action per tier; first contact and second thread per signal; the visitor-below-the-buyer rule when S14 is tracked; the cadence and cool-down in one line.
5. **First Emails**: one "Claims to confirm" line, then per signal an "Angle:" line, a template (subject plus a body of 90 words or fewer, first sentence 30 words or fewer, the event fact as a merge field) and a "Fields:" line with each field's source column and an example value.
6. **Pulls and Cost**: each pull described in plain words (for example "Lead Database: VP and C-level sales contacts at watched domains"), its frequency, cost per run and cost per 4 weeks, outside tools at their checked price or "your plan", and a total row.
7. **Launch Plan**: dated weeks starting from today, each with a step and an owner role: tool sign-up, baseline pulls, first cycle, first review.

- Each fact appears once. The catalog is the only signal list and the emails carry their own angle lines, so leave out summary tables, angle tables, queues of invented accounts and score-check arithmetic. A **Signal Queue** goes in only when real pulls were run or the user supplied accounts.
- The reader gets plain words only: no tool ids, parameter names, JSON or code blocks, file names, repo paths or skill names. Another skill is named only in a closing handoff line.
- Fit the request: a user who asks for one play (funding, hiring, events) gets that signal and its stack partners only.

## Quality Check

`python3 scripts/check-output.py signal-program.md` enforces:

- All seven sections present, no `[fill]` left, no Program Summary, Message Angles or other repeating section, no 10-word sentence stated twice, "assumed" and "illustrative" at most twice each.
- No tool ids, backticked parameters, code blocks, repo paths or skill names; no legal content.
- Every catalog signal names a ScraperCity product or is labeled `other source`; funding, hiring, filing, launch, event, visit, intent, webinar and social signals carry the label; a job change or new leader row carries it or the Lead Database.
- Every catalog signal has a touch window with a number and a unit, a numeric half-life and a max age at least as long.
- The Scoring Model states the A and B cut-offs and at least one negative row with minus points and a pause in days.
- Exclusions cover competitors, vendors, partners and agencies, each with a match rule.
- Routing states the missed-SLA action, and routes a visitor below the buyer when S14 is tracked.
- Every catalog signal has a first email with an Angle line, a subject, a 15 to 90 word body, a first sentence of 30 words or fewer, an event merge field, a Fields line covering every field, no generalization stated as fact ("usually", "typically", "most teams") and no booth meeting ask; the section has a Claims to confirm line.
- Every pull has a frequency and a dollar cost, with a total row; the Launch Plan has at least three dated rows with owners.
- A Signal Queue, when present, has ISO dates, ages within max age, scores from 0 to 100 and tiers that match the cut-offs.

Also check by reading: the baseline pull produced no signals; each angle names an event the data shows; funding emails name what the money is for; filing emails quote the filing with its section.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Calling a filter a signal | "Uses Shopify" describes a state; nothing changed between pulls | Diff two pulls; only appeared, disappeared or crossed counts |
| Treating `excludeDelivered` as "new business" | It means new to your account | Pair with `maxReviews` and a first-seen date; word the angle carefully |
| Alerting on the baseline | Every record looks new on the first pull | Store pull 1 as baseline, signal from pull 2 |
| Re-buying the same rows weekly | Scrapers bill every row every time | Narrow filters; monthly universe plus weekly Tech Stack Search |
| Stale signals | A 90-day-old listing reads as research to the prospect | Max age per signal; drop or downgrade |
| Overclaiming cause | "Your customers are unhappy" from a 0.2 rating dip | State the number, ask a question |
| Tech removal taken at face value | Detection gaps produce false removals | Check the site by hand before a tier A touch |
| Funding or job-post triggers attributed to ScraperCity | These tools do not show them | Score them as S14 to S28 with `other source: <feed>` |
| One visit line for every S14 row | No study compares a visit line with a fit line, and RB2B's own samples use the visit | Split S14 rows between the two and keep the winner |
| Scoring competitors and agencies | Their visits and tech installs come from research on you, so the queue fills with accounts that will never buy | Exclusion check before scoring, tier X |
| Hot signal waits a week | Elias: the first viable vendor in the window wins | Tier A touch window set in the program, owner notified by the workflow |
| "Congrats on the raise" as the opener | Other vendors on the same funding feed open the same way, and the line says nothing about the offer | Name the stated use of the money and ask how they will do it |
| Matching every Form D filing | A national query for 2026-10-01 to 2026-10-09 returned 2,054 filings, the first page angel fund series | Filter by state, drop funds by name and Item 4, stack with S18 or S20 |
| Quoting an earnings recap instead of the filing | Other vendors read the same recap | Quote Item 7, Item 1A or the call Q&A, with the section |
| Building S19 on Trigify | Its standalone platform and API stop on 22 October 2026 | Octolens or F5Bot; export Trigify history first |
| Emailing a job post that closed | The angle is about a seat already filled | Re-load the posting before a tier A touch; a closed post becomes S20 next month |
| No negative signals | A hiring freeze or a just-signed competitor still scores as hiring or funding | A "Negative:" row per event with minus points and a pause |
| Asking an exhibitor for a booth meeting | Booth staff sell to their own prospects, and shows such as NAMM bar non-exhibitors from soliciting on the floor | Email the sales leader not on booth duty; ask for a meeting the week after the show |
| "Teams usually..." in the email body | An industry figure with no source reads as a guess and invites a "not us" | Ask it as a question, or use the sender's own data in a field |
| Worked emails for fictional accounts | A sequencer cannot load them | Templates with merge fields and a Fields line naming each source column |
| Pitching an SDR who visited pricing | The visitor cannot buy | Route to the buyer at that domain with the fit-based email; do not mention the visit |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/signal-catalog.md` | Detection rule, diff key, date anchor, false positives and angle for each signal; outside signals S14 to S28 with visitor coverage by country; negative signals |
| `references/scoring-and-freshness.md` | Score formula, decay lookup (days and hours), exclusion tier, tiers and touch spacing, cool-down and per-signal measurement |
| `references/signal-plays.md` | Who to contact, touch plan and a complete first email for each outside signal (visits, funding and Form D, hiring and new leaders, job changes, earnings, competitor changes, launches, events, social, G2 intent, webinars) |
| `references/repeat-pull-recipes.md` | Snapshot schema, diff script, cron jobs, n8n workflow, webhooks, monthly run costs, social engagement types, owner alert payload, free EDGAR, job board and page monitor feeds |
| `templates/output-template.md` | Starting a signal program |
| `examples/worked-example.md` | A full program for a Shopify retention agency using Store Leads and Tech Stack Search |
| `scripts/check-output.py` | Validating a signal program |
| `references/scrapercity-catalog.md` | Prices and parameters for every tool above (shared) |
| `references/scrapercity-platform.md` | Database allowances, `excludeDelivered`, plan access (shared) |
| `references/scrapercity-agent-patterns.md` | Wallet check, run lifecycle, webhooks, safe retry, CSV naming (shared) |
| `references/cold-email-frameworks.md` | Trigger-based relevance framework and example emails (shared) |
| `references/list-quality-standard.md` | Dedupe keys, normalization, validation buckets (shared) |

## Related Skills

- `cold-email-strategy` and `cold-email-copywriting` build the signal-specific campaigns.
- `cold-calling` and `multi-channel-outreach` work tier A accounts.
- `ecommerce-by-techstack` and `local-business-list` build the universes that signals are diffed against.
- `decision-maker-finder` finds the person at each scored account.
- `scrapercity-integrations`, `scrapercity-cli` and `scrapercity-api` cover scheduling and automation detail.
- `scrapercity-real-estate-data` covers distress and owner data.
- `outbound-unit-economics` compares cost per meeting of signal programs with static lists.
