# Signal Program: Tidewater Retention, Shopify Stores Adopting or Leaving Klaviyo

Company and offer: Tidewater Retention (a fictional agency for this example) builds Klaviyo email and SMS flows for Shopify stores, $3,500 setup plus $1,800 a month. ICP: US Shopify stores with 20,000 to 150,000 estimated monthly visits, a public email, in apparel, pets, food and beverage, and home goods. Snapshot store: Postgres, one table per signal. Scheduler: n8n on a small server. Destinations: HubSpot (tasks and companies), Instantly (tier B campaign), Slack channel #signals for tier A. Store domains below use the reserved `.example` suffix because the stores are fictional.

## Program Summary

| Item | Value |
|-|-|
| Cycle date | 2026-10-19 |
| Baseline pull date | Tech Stack Search 2026-10-05; Store Leads universe 2026-09-01 |
| Signals tracked | S5 Klaviyo adopted, S6 Klaviyo removed, S8 traffic band crossed |
| Accounts with a live signal this cycle | 73 accounts, 76 signals (3 accounts carry two) |
| Tier A, B, C counts | 14 A, 30 B, 29 C |
| ScraperCity plan | Growth, $149 a month with $159 in credits |

## Signal Catalog

| Signal | Tool | Detection rule | Date anchor | Half-life (days) | Max age (days) | Base points |
|-|-|-|-|-|-|-|
| S5 Klaviyo adopted | `scrape_builtwith` (Tech Stack Search, technology "Klaviyo") intersected with the `scrape_store_leads` universe | Domain in this week's Klaviyo list, absent last week, and inside the ICP universe | First-seen pull date | 45 | 90 | 35 |
| S6 Klaviyo removed | `scrape_builtwith` intersected with the universe | Domain on the list two weeks ago, absent on the last two weekly pulls, and a manual site check finds no Klaviyo script | Second consecutive absent pull | 30 | 60 | 30 |
| S8 traffic band crossed | `scrape_store_leads` monthly universe | Estimated monthly visits crossed 50,000 upward between the 2026-09-01 and 2026-10-01 universes | Universe pull date | 60 | 120 | 20 |

Signals deliberately not used: funding and hiring (no ScraperCity source), and `excludeDelivered` new records (the Ecommerce Database feed adds untouched stores but no event).

## Scoring Model

| Component | Rule | Points |
|-|-|-|
| Fit: category | Apparel, pets, food and beverage, home goods 15; adjacent (beauty, outdoor) 7 | 0 to 15 |
| Fit: visits band | 30,000 to 100,000 visits 10; 20,000 to 30,000 or 100,000 to 150,000 visits 5 | 0 to 10 |
| Fit: geography | US store with a US address 10 | 0 to 10 |
| Fit: not on Shopify Plus | `planExclude: ["Shopify Plus"]` in the universe pull 5 | 0 to 5 |
| Signal strength | base points x 0.5 ** (age / half-life); second live signal adds 5; cap 40 | 0 to 40 |
| Reachability | Named founder or ecommerce lead 6, valid email 6, gated mobile 5, website 3 | 0 to 20 |
| Tiers | A 70 and up, B 40 to 69, C under 40 | 0 to 100 |

## Repeat Pull Schedule

| Pull | Tool | Parameters | Frequency | Cost per run |
|-|-|-|-|-|
| ICP universe | `scrape_store_leads` | `platform: "shopify"`, `countryCode: "US"`, `minEstimatedMonthlyVisits: 20000`, `maxEstimatedMonthlyVisits: 150000`, `emails: true`, `planExclude: ["Shopify Plus"]`, `totalLeads: 10000`, `offset` paging | Monthly, 1st at 07:00 CT | $38.22 (9,800 stores x $0.0039) |
| Klaviyo detections | `scrape_builtwith` | `technology: "Klaviyo"`, `fileName: "techstack-klaviyo-YYYYMMDD"` | Weekly, Monday 06:15 CT | $4.99 |
| Decision makers | `query_lead_database` | `companyDomain` (tier A and B domains), `title: "Founder, Owner, CEO, Head of Ecommerce, Ecommerce Manager, Head of Growth"`, `limit: 10` | Weekly after scoring | $0.00 (included in Growth) |
| Founder at uncovered domains | `scrape_website_finder` | `domains` (no Lead Database contact), `jobTitle: "Founder"`, `autoValidateEmails: true` | Weekly after scoring | about $0.35 (7 found x $0.0499) |
| Email validation | `validate_emails` | Contacts not validated in the last 30 days | Weekly | about $0.26 (36 x $0.0072) |
| Mobiles for tier A calls | `find_mobiles` | Founder work emails, tier A only | Weekly | about $1.00 (4 found x $0.25) |

n8n runs the Klaviyo pull, waits on status, downloads, diffs against the `s5_klaviyo_state` table, joins to the universe table, scores, and routes. A `check_wallet` node stops the workflow if the balance is under $20.

## Message Angles

| Signal | Angle | First line |
|-|-|-|
| S5 Klaviyo adopted | The first 90 days decide whether flows get built; offer the flow map | "Saw Northpaw started running Klaviyo in the last couple of weeks; the first 90 days are when flows get built or stall." |
| S6 Klaviyo removed | Displacement window; ask, do not assert | "Looks like Fernway moved off Klaviyo recently. What are you running email and SMS on now?" |
| S8 traffic band crossed | Growth outpacing retention; use "looks to" since visits are estimates | "Coastal Threads' traffic looks to have passed 50,000 visits a month since summer, which usually means repeat-purchase flows lag behind." |

Each campaign: 4 touches over 10 business days for tier A (call plus email), 3 over 2 weeks for tier B, opt-out line in every email, stop on any reply.

## Signal Queue

Ten of the 73 accounts this cycle. Score = fit + signal strength + reachability.

| Account | Signal | Signal date | Age (days) | Score | Tier | Action |
|-|-|-|-|-|-|-|
| kestrelcoffee.example | S5 + S8 | 2026-10-12 | 7 | 86.4 | A | Call founder, email touch 1, Slack alert |
| northpaw.example | S5 | 2026-10-12 | 7 | 81.4 | A | Call founder, email touch 1 |
| fernway.example | S6 | 2026-10-19 | 0 | 79.0 | A | Manual site check done (no Klaviyo script), call and email |
| lumentea.example | S5 | 2026-10-19 | 0 | 76.0 | A | Email touch 1, call tomorrow 10am |
| coastalthreads.example | S8 | 2026-10-01 | 18 | 63.2 | B | Instantly tier B campaign |
| brightbark.example | S5 | 2026-10-12 | 7 | 62.4 | B | Instantly tier B campaign |
| hollowpine.example | S5 | 2026-10-12 | 7 | 49.4 | B | Find contact with Website Finder, then tier B |
| saltandstem.example | S8 | 2026-10-01 | 18 | 44.2 | B | Instantly tier B campaign |
| merrowknit.example | S6 | 2026-10-19 | 0 | 39.0 | C | Hold, re-score next pull |
| driftwoodpets.example | S8 | 2026-10-01 | 18 | 34.2 | C | Hold, re-score next pull |

Score check for the first row: fit 35 + strength min(40, 35 x 0.5 ** (7 / 45) + 5) = 36.4 + reachability 15 = 86.4.

## Routing and SLAs

| Tier | Score | First touch | SLA | Owner |
|-|-|-|-|-|
| A | 70 to 100 | Call (gate passed) and email the same day | 2 business days from detection | Account executive, HubSpot task |
| B | 40 to 69 | Email touch 1 in the signal campaign | 5 business days | SDR, Instantly campaign |
| C | 0 to 39 | None | Re-score each pull, drop at max age | Workflow |
| Any | Customer, open opportunity, or contacted in the last 90 days | No outreach; signal logged on the HubSpot record | Same day | Account owner |

## Cost Estimate

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Store Leads ICP universe, 1 monthly pull | 9,800 stores | $0.0039 | $38.22 |
| Tech Stack Search "Klaviyo", weekly | 4 pulls | $4.99 | $19.96 |
| `scrape_website_finder` founders found | 28 (7 a week) | $0.0499 | $1.40 |
| `validate_emails` | 144 (36 a week) | $0.0072 | $1.04 |
| `find_mobiles` numbers found | 16 (4 a week) | $0.25 | $4.00 |
| `query_lead_database` contacts by domain | 116 (29 a week) | Included in Growth | $0.00 |
| Total ScraperCity spend for the 4-week cycle | | | $64.62 |

The $64.62 comes out of the $159 in Growth plan credits. The universe pull ($38.22) and the monthly schedule were approved once after a `check_wallet` call and a `totalLeads: 100` test ($0.39).
