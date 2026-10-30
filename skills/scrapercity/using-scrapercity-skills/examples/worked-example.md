# Routing Plan: HVAC agency outbound program

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

## Request

| Field | Value |
|-|-|
| Outcome | 20 booked calls a month with owners of HVAC and plumbing companies in Dallas-Fort Worth, for a marketing agency that sells paid search management |
| Buyer | Owner or general manager of a residential HVAC or plumbing company with a website |
| Channels | Cold email first, then a phone call to the business line for engaged owners |
| Plan tier | Growth ($149 a month, $159 of credits) |
| Access path | MCP server in Claude Code; `check_wallet` returned a balance |
| Budget ceiling | $60 for data this month |
| Wallet balance | $142.30 |
| Countries | United States (Texas) |
| Ready by | Send-ready file the same day: the database pull returns in seconds a page, and the Maps and validation runs finish in minutes. No Apollo run, so nothing waits on one |

## Skill Chain

| Step | Skill | Produces | Done when |
|-:|-|-|-|
| 1 | `local-business-list` | `dfw_hvac_plumbing_sendready.csv` with owner name, business phone, website, rating, reviews and a validated email | Its checker passes and every row has a validation status |
| 2 | `cold-email-strategy` | Two campaign cells split by review count (under 50 reviews, 50 or more) with one offer each | Touch map has a branch for every reply type |
| 3 | `cold-email-copywriting` | Four-touch sequence per cell, each body under 90 words | Copy checker passes |
| 4 | `sending-platforms` | Instantly import mapping, suppression list, webhook to the CRM | Test import of 20 rows maps every merge field |
| 5 | `cold-calling` | Call script and blocks for owners who opened or clicked twice | Do-not-contact list and call-block schedule written into the dialer settings |
| 6 | `outbound-unit-economics` | Cost per booked call at the measured reply rate | Model reconciles with the cost table below |

## Tool Calls and Cost

| Step | Tool | Units | Unit price | Cost | Basis for units |
|-:|-|-:|-:|-:|-|
| 1 | `query_local_business_database` | 2,400 | $0.00 | $0.00 | Count call with `keyword: ["hvac contractor", "plumber"]`, `location: ["Dallas TX", "Fort Worth TX", "Plano TX", "Arlington TX"]`, `hasWebsite: true`, `hasEmail: true` returned 2,400 |
| 1 | `scrape_maps` | 600 | $0.0099 | $5.94 | Gap fill for 6 suburbs the database returned fewer than 40 businesses for, capped at 100 each |
| 1 | `validate_emails` | 3,000 | $0.00169 | $5.07 | Every email from both sources, before dedupe credit |
| 5 | `find_mobiles` | 0 | $0.25 | $0.00 | Not used in month one; the business line is dialed first and costs nothing extra |
| | **Total** | | | **$11.01** | |

Why: the Local Business Database is included on Growth and covered the four core cities, so it ran first. Maps ran only for suburbs under 40 results. Mobile Finder was left out of month one because the business line carries no extra cost; it gets priced if the business-line connect rate from the first call blocks is too low to book the target.

## Gates

| Gate | Rule applied | Status |
|-|-|-|
| Wallet | `check_wallet` before the first paid call; $142.30 covers $11.01 | Passed |
| Count | 2,400 database rows and a $11.01 estimate shown to the user before the pull | Approved by user |
| Suppression | One list merged from the agency's past unsubscribes, hard bounces, complaints and do-not-contact requests, plus current clients, loaded into Instantly and the dialer before import. Email: one-click unsubscribe header on and removals processed daily (inside the 2-day window Google and Yahoo set). Phone: do-not-contact list checked before each call block | Written into sequence and dialer settings |
| Quality | Only `valid` emails send; catch-all rows go to a separate cell with its own bounce tracking; list meets the shared list quality standard | Passed on validation report |
| Deliverability | 6 warmed inboxes on 3 secondary domains with SPF, DKIM and DMARC; the agency's current setting of 30 sends per inbox per day; spam rate watched in Postmaster Tools and kept under 0.1% | Passed |

## Handoffs

| From skill | File | To skill |
|-|-|-|
| `local-business-list` | `dfw_hvac_plumbing_sendready.csv` | `cold-email-strategy` |
| `cold-email-strategy` | `dfw_campaign_cells.md` | `cold-email-copywriting` |
| `cold-email-copywriting` | `dfw_sequences.md` | `sending-platforms` |
| `sending-platforms` | `instantly_import_map.csv` | `cold-calling` |
| `cold-calling` | `call_blocks.md` | `outbound-unit-economics` |

## Open Questions

- The agency's average deal size and close rate, needed for the cost-per-deal line in `outbound-unit-economics`.
- Where each past campaign's unsubscribes live today (old sender accounts, CRM, spreadsheets), so the merged suppression list is complete before import.
