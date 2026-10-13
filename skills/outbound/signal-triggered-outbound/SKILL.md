---
name: signal-triggered-outbound
description: >-
  Builds outbound that fires on dated events ScraperCity data can show: a new
  Google Maps or Yelp listing with few reviews, rating or review-count changes
  across repeat pulls, a domain newly found on a technology via Tech Stack
  Search, a store's platform, apps or traffic band from Store Leads, a business
  listed on BizBuySell, a pre-foreclosure or auction from the Distress List,
  agents new to a Zillow market, and daily new records with excludeDelivered.
  Covers signal half-life, freshness rules, scoring, the message angle per
  signal, and the repeat pull (cron and CLI or REST, n8n, webhooks). Use when
  the user asks for trigger-based or signal-based outbound, "why now" lists,
  new business alerts, tech install alerts, or a weekly fresh-lead feed.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [signals, trigger-events, intent, repeat-pull, automation, n8n, cron, webhooks, tech-stack, new-business]
  related_skills: [cold-email-strategy, cold-email-copywriting, cold-calling, multi-channel-outreach, outbound-unit-economics, ecommerce-by-techstack, local-business-list, decision-maker-finder, scrapercity-integrations, scrapercity-cli, scrapercity-api, scrapercity-real-estate-data]
  frameworks:
    - "Craig Elias - Trigger Event Selling and the window of dissatisfaction"
    - "Alex Berman - trigger-based relevance and segment-first targeting"
    - "FCC and FTC - TCPA and Do Not Call rules for consumer-owned numbers (distress outreach)"
    - "CFPB - Regulation O, Mortgage Assistance Relief Services"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md, cold-email-frameworks.md, outbound-compliance-primer.md, list-quality-standard.md]
---

# Signal-Triggered Outbound

## Overview

This skill turns repeat ScraperCity pulls into a queue of accounts with a dated reason to reach out this week. Each signal has a detection rule (what changed between two pulls), a date anchor, a half-life after which it is worth half as much, a maximum age after which it is dropped, a score, and a message angle that names the event in the first line.

The mistakes it prevents: calling a list "intent" when it is a static filter, emailing about a "new" listing that opened a year ago, using a signal the tools cannot see (funding rounds, job posts) as if they could, re-paying for the same records every week, and letting a hot signal sit in a spreadsheet until it is stale.

Only signals these tools can show are in scope. Funding rounds, job postings, leadership changes and web visits come from other sources; if the user brings them, label the source in the queue and do not attribute them to ScraperCity.

## When to Use

- "Find businesses that just opened", "alert me to new dentists in Phoenix every week".
- "Who just installed Klaviyo", "stores that started using Recharge", "sites that dropped HubSpot".
- "Which restaurants' ratings dropped", "contractors whose reviews stalled".
- "Businesses for sale in my area", "new pre-foreclosures in Tampa every Monday".
- "Set up a daily feed of new leads", "only give me records I don't already have".
- "Make our outbound trigger-based", "why-now lists", "signal scoring".

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

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Craig Elias, Trigger Event Selling (InsideSales, 2013) | A trigger event opens a "window of dissatisfaction" before the buyer starts shopping; the first viable vendor in that window wins far more often (he cites a 74% close ratio attributed to Forrester). Speed and timing are the point. |
| Alex Berman, alexberman.com | Targeting and offer drive results ahead of copy; a dated reason belongs in the first line, and the offer must connect to it. A roundup on his site reports trigger-based lists replying above bought lists (self-reported). |
| `references/cold-email-frameworks.md` section 8 | Trigger-based relevance: skip a trigger older than its half-life or one you cannot verify; never invent a trigger. |
| ScraperCity platform facts | `excludeDelivered=true` returns only records the account does not have; re-fetching an owned database record is free; new records count toward 100,000 a day. |
| FCC 47 CFR 64.1200 and FTC TSR | Owners in pre-foreclosure are consumers: DNC scrub, hand dial, no texts. |
| CFPB Regulation O (12 CFR 1015) | Offers to help a homeowner avoid foreclosure are mortgage assistance relief services: no advance fees, required disclosures. |

## Workflow

### 1. Pick signals that create a buying window for this offer

| Offer | Signals worth tracking |
|-|-|
| Reviews, local SEO, websites for local businesses | New listing with few reviews; rating drop; review velocity stall |
| Email and SMS retention for Shopify stores | New Klaviyo or Recharge detection; traffic band crossing; app removed |
| Replatforming or development agencies | Domain on a legacy technology; technology removed or added |
| M&A advisors, SBA lenders, exit services, buyers | New BizBuySell listing in a category and region |
| Real estate investors, cash buyers, foreclosure attorneys | New pre-foreclosure or auction in a ZIP |
| Services sold to real estate agents (photography, CRM, leads) | Agents new to a market pull |
| Any database-backed ICP | Daily or weekly new records with `excludeDelivered=true` |

Full detection rules, false positives and angles: `references/signal-catalog.md`.

### 2. Define each signal precisely

For each signal write: tool and parameters, the diff key (domain, phone, place, listing URL, property address), the change that counts (appeared, disappeared, field crossed a threshold), the date anchor, the half-life, the max age and the angle.

The date anchor is the date your pull first saw the change unless the source row carries its own date. A weekly pull dates every event to within 7 days; say "in the last week", never "yesterday".

### 3. Take a baseline, then pull on a schedule

The first pull is a baseline and produces no signals. Every later pull is diffed against the stored snapshot. Default cadence:

| Signal | Cadence | Why |
|-|-|-|
| New local listing, review movement | Weekly | Reviews accumulate in days to weeks |
| Tech Stack Search adoption or removal | Weekly | $4.99 per technology per pull, flat |
| Store Leads apps, platform, traffic band | Monthly universe, weekly for apps | Store Leads bills per lead on every pull |
| BizBuySell | Weekly | Listings move |
| Distress List | Weekly | Notices and auction dates are time-boxed |
| Zillow Agents | Monthly | Rosters change slowly |
| Database `excludeDelivered` feed | Daily | Allowance resets daily |

### 4. Score, tier and route

Score = fit (0 to 40) + signal strength decayed by age (0 to 40) + reachability (0 to 20). Signal strength = base points x 0.5^(age in days / half-life). Tiers: A at 70 and up, B 40 to 69, C below 40. Formula, decay table and examples: `references/scoring-and-freshness.md`.

| Tier | Action | SLA from detection |
|-|-|-|
| A | Find the decision maker, call plus first email | 2 business days |
| B | First email in a signal-specific campaign | 5 business days |
| C | Hold; re-score next pull; drop at max age | none |

### 5. Enrich only what you will contact

Enrich after scoring, so money goes to tier A and B. Order: Lead Database by `companyDomain` (included on Growth), then `scrape_website_finder` for a named role, `find_emails` for a known name, `validate_emails` on everything, `find_mobiles` for tier A calls.

### 6. Write the angle into the first line

Name the event and its date range in plain words, connect it to the offer, ask one question. Angles per signal are in `references/signal-catalog.md`. Rules: never imply surveillance ("we track your reviews"), never shame (distress, bad ratings), and never state a cause you cannot see, such as calling a rating drop "unhappy customers".

### 7. Suppress and cool down

One account gets one signal-triggered sequence per 90 days, whatever new signals fire. Signals on customers, open opportunities and opted-out contacts are logged and not contacted.

### 8. Measure per signal

Track reply, positive reply and meeting rate by signal type and by age bucket (0 to 7, 8 to 30, 31+ days). Retire a signal that does not beat your static-list baseline after 200 contacts; shorten a half-life when old signals convert at the static rate.

## ScraperCity Implementation

| Signal | Tool | Key parameters | Diff key | Price per run |
|-|-|-|-|-|
| New local listing, few reviews | `query_local_business_database` | `keyword`, `location`, `maxReviews: 5`, `excludeDelivered: true` | phone, then name plus postal code | Included in Growth; new records count toward 100,000 a day |
| New listing outside the database, fresh review counts | `scrape_maps` | `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch` | phone or place URL | $0.0099 per business |
| Rating or review change on a watched set | `scrape_yelp` | `directUrls` (the watched businesses) | Yelp URL | $0.0099 per result |
| Technology adoption or removal | `scrape_builtwith` (Tech Stack Search) | `technology`, `fileName` | domain | $4.99 per technology |
| Store app, platform, traffic band | `scrape_store_leads` | `platform`, `countryCode`, `apps`, `technologies`, `minEstimatedMonthlyVisits`, `maxEstimatedMonthlyVisits`, `planExclude`, `totalLeads`, `offset` | domain | $0.0039 per lead |
| Business listed for sale | `scrape_bizbuysell` | `startUrls`, `maxItems`, `datasetName` | listing URL | $0.0099 per listing |
| Pre-foreclosure, foreclosure, auction | `scrape_distress_list` | `search`, `distressTypes`, `maxItems` (max 500) | property address | $0.05 per property |
| Agents in a market | `scrape_zillow_agents` | `location`, `specialty`, `searchLimit` (max 500) | profile URL or name plus brokerage | $0.029 per agent |
| New-to-account records | `query_lead_database`, `query_local_business_database`, Ecommerce Database REST | `excludeDelivered: true`, `after` cursor | record id | Included in Growth |
| Contacts for scored accounts | `query_lead_database`, `scrape_website_finder`, `find_emails`, `validate_emails`, `find_mobiles` | `companyDomain`; `domains` plus `jobTitle`; names plus domain | email | $0, $0.0499 per contact found, $0.05 per email found, $0.0072 per email, $0.25 per mobile found |

Three things about repeat pulls that change cost:

1. Re-fetching a Local Business Database or Lead Database record the account already owns is free, so a weekly re-pull of the same segment costs nothing on Growth. The database's refresh schedule is not published: re-pull 100 known records after 30 days and count changed `reviews_count` values before relying on it for review movement. If none changed, measure reviews with `scrape_maps` or `scrape_yelp`.
2. Store Leads, Maps, Yelp, BizBuySell, Distress List and Zillow Agents bill per row on every pull, including rows you saw last week. Keep those pulls narrow.
3. `excludeDelivered=true` returns records new to your account, which says nothing about when the business opened. Pair it with `maxReviews` to approximate new businesses; never call a record "just opened" from that flag alone.

MCP calls:

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

One Markdown signal program from `templates/output-template.md` with these sections in order: Program Summary, Signal Catalog, Scoring Model, Repeat Pull Schedule, Message Angles, Signal Queue, Routing and SLAs, Cost Estimate. The Signal Queue shows this cycle's scored accounts with signal date, age, score, tier and action.

## Quality Check

`python3 scripts/check-output.py signal-program.md` enforces:

- All eight sections present, no `[fill]` left, at least 25 table rows.
- Every catalog signal uses a ScraperCity tool id, or is labeled as coming from another source.
- Every signal has a numeric half-life and a max age at least as long as the half-life.
- Every signal in the catalog has a message angle, and every first line is 30 words or fewer.
- Every Signal Queue row has an ISO signal date, an age within the signal's max age, a score from 0 to 100, and a tier that matches the 70 and 40 thresholds.
- Every repeat pull has a frequency and a dollar cost per run; the cost estimate has a total.

Also check by reading: the baseline pull produced no signals; each angle names an event the data shows; the distress row (if any) carries the consumer phone rules.

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
| Distress outreach like B2B | Owners are consumers; Regulation O and state laws apply | Consumer phone gate, respectful mail, no advance-fee offers |
| Funding or job-post triggers attributed to ScraperCity | These tools do not show them | Label any outside source in the queue |
| Hot signal waits a week | The window closes | Tier A SLA of 2 business days, owner notified by the workflow |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/signal-catalog.md` | Detection rule, diff key, date anchor, half-life, false positives, angle and compliance note for each signal |
| `references/scoring-and-freshness.md` | Score formula, decay table, tiers, SLAs, cool-down and per-signal measurement |
| `references/repeat-pull-recipes.md` | Snapshot schema, diff script, cron jobs, n8n workflow, webhooks, monthly run costs |
| `templates/output-template.md` | Starting a signal program |
| `examples/worked-example.md` | A full program for a Shopify retention agency using Store Leads and Tech Stack Search |
| `scripts/check-output.py` | Validating a signal program |
| `references/scrapercity-catalog.md` | Prices and parameters for every tool above (shared) |
| `references/scrapercity-platform.md` | Database allowances, `excludeDelivered`, plan access (shared) |
| `references/scrapercity-agent-patterns.md` | Wallet check, run lifecycle, webhooks, safe retry, CSV naming (shared) |
| `references/cold-email-frameworks.md` | Trigger-based relevance framework and example emails (shared) |
| `references/outbound-compliance-primer.md` | Consumer phone rules, Regulation O, CASL and GDPR for signals outside the US (shared) |
| `references/list-quality-standard.md` | Dedupe keys, normalization, validation buckets (shared) |

## Related Skills

- `cold-email-strategy` and `cold-email-copywriting` build the signal-specific campaigns.
- `cold-calling` and `multi-channel-outreach` work tier A accounts.
- `ecommerce-by-techstack` and `local-business-list` build the universes that signals are diffed against.
- `decision-maker-finder` finds the person at each scored account.
- `scrapercity-integrations`, `scrapercity-cli` and `scrapercity-api` cover scheduling and automation detail.
- `scrapercity-real-estate-data` covers distress and owner data.
- `outbound-unit-economics` compares cost per meeting of signal programs with static lists.
