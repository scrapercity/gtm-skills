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

## Skill Chain

| Step | Skill | Produces | Done when |
|-:|-|-|-|
| 1 | `local-business-list` | `dfw_hvac_plumbing_sendready.csv` with owner name, business phone, website, rating, reviews and a validated email | Its checker passes and every row has a validation status |
| 2 | `cold-email-strategy` | Two campaign cells split by review count (under 50 reviews, 50 or more) with one offer each | Touch map has a branch for every reply type |
| 3 | `cold-email-copywriting` | Four-touch sequence per cell, each body under 90 words | Copy checker passes |
| 4 | `sending-platforms` | Instantly import mapping, suppression list, webhook to the CRM | Test import of 20 rows maps every merge field |
| 5 | `cold-calling` | Call script and blocks for owners who opened or clicked twice | DNC and Texas calling-hours gate written into the dialer settings |
| 6 | `outbound-unit-economics` | Cost per booked call at the measured reply rate | Model reconciles with the cost table below |

## Tool Calls and Cost

| Step | Tool | Units | Unit price | Cost | Basis for units |
|-:|-|-:|-:|-:|-|
| 1 | `query_local_business_database` | 2,400 | $0.00 | $0.00 | Count call with `keyword: ["hvac contractor", "plumber"]`, `location: ["Dallas TX", "Fort Worth TX", "Plano TX", "Arlington TX"]`, `hasWebsite: true`, `hasEmail: true` returned 2,400 |
| 1 | `scrape_maps` | 600 | $0.0099 | $5.94 | Gap fill for 6 suburbs the database returned fewer than 40 businesses for, capped at 100 each |
| 1 | `validate_emails` | 3,000 | $0.0072 | $21.60 | Every email from both sources, before dedupe credit |
| 5 | `find_mobiles` | 0 | $0.25 | $0.00 | Not used; calls go to the business line, which avoids the wireless-number consent question |
| | **Total** | | | **$27.54** | |

Why: the Local Business Database is included on Growth and covered the four core cities, so it ran first. Maps ran only for suburbs under 40 results. Mobile Finder was left out because the business line reaches owners of small trade companies during office hours and carries no extra cost.

## Gates

| Gate | Rule applied | Status |
|-|-|-|
| Wallet | `check_wallet` before the first paid call; $142.30 covers $27.54 | Passed |
| Count | 2,400 database rows and a $27.54 estimate shown to the user before the pull | Approved by user |
| Compliance | Email: CAN-SPAM opt-out line and the agency's postal address in every message. Phone: business lines only, scrubbed against the National DNC Registry and the internal DNC list, calls 9am to 8pm Central on weekdays per Texas Business and Commerce Code 301.051 | Written into sequence and dialer settings |
| Quality | Only `valid` emails send; catch-all rows go to a separate low-volume cell; list meets the shared list quality standard | Passed on validation report |
| Deliverability | 6 warmed inboxes on 3 secondary domains with SPF, DKIM and DMARC; 30 sends per inbox per day | Passed |

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
- Whether the agency already holds a do-not-contact list from past campaigns, to load as suppression before import.
