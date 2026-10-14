# Framework Notes: ScraperCity Real Estate Data

Which sources shape this skill, what each contributes, and which file to open for each job.

## Routing table

| You need | Open |
|---|---|
| Inputs, outputs, limits and CLI flags for a tool | `references/tool-reference.md` |
| A plan for a specific persona (agent, wholesaler, investor, lender, CRE broker, business broker) | `references/workflow-playbooks.md` |
| Channel order, match confidence, the suppression list, message rules, reply triage, the Contact Hygiene table | `references/contact-routing-guide.md` |
| Catalog prices and schemas | `references/scrapercity-catalog.md` (shared) |
| Plans and database access | `references/scrapercity-platform.md` (shared) |
| Wallet checks, polling, approvals | `references/scrapercity-agent-patterns.md` (shared) |

## Sources and contributions

### ScraperCity tools (primary for behavior and price)

- `references/scrapercity-catalog.md`, generated from npm `scrapercity` 1.0.17, gives the six tools, their inputs and prices: Zillow Agents $0.029 per agent; Property Lookup $0.15 per property plus $0.10 for owner contact; Distress List $0.05 per property; Crexi $0.029 per property; BizBuySell $0.0099 per listing; People Finder $0.0199 per result with zero-match searches billed as one result.
- `bin/cli.mjs` gives the CLI commands `zillow-agents`, `distress-list`, `crexi`, `bizbuysell` and `people-find`, and their flags. The CLI has no property lookup command in this version.
- `AGENT_DOCS.txt` says Property Lookup needs a full address with city, state and ZIP.
- The catalog entry for Crexi lists the three URL forms and the 400 for a map view with no location.
- ScraperCity product pages list the Zillow Agents output fields (name, phone, email, screen name, profile URL, specialties, languages, active listings, recent sales, rating, reviews, license number), the Crexi sample fields (property, address, type, price, square footage, broker name, phone and firm, cap rate, NOI and others) and the BizBuySell sample fields (title, location, price, EBITDA, revenue, cash flow, broker name, phone and firm, year established, employees, reason for selling and others).

### USPS Publication 28, Postal Addressing Standards

Standard street suffix and unit abbreviations and the ZIP format. Contribution: the address normalization used before Property Lookup and People Finder runs, before dedupe across ZIP runs, and in the match-confidence test.

### Google Email sender guidelines and FAQ; Yahoo Sender Hub best practices

Bulk senders need a one-click unsubscribe, removals within 2 days (Google asks for 48 hours), and a spam complaint rate under 0.3% (Google asks for under 0.1%). Contribution: the email rows in the Contact Hygiene table.

### Hunter, Cold Email Guide (October 2023)

Hunter's guide to bounce rates says bounces should not exceed 2% of the emails sent. Contribution: the hard bounce pause in `references/contact-routing-guide.md`.

### Settings this skill measures instead of assuming

| Setting | Where it comes from |
|---|---|
| Call attempts per number | The attempt after which your outcome data shows no further connects |
| Call block hours | The hours with the best connect rate in your outcome data |
| Which rows get Property Lookup for price history | The rows the user will make offers on |

## How the sources combine

1. The catalog decides which tool and what it costs.
2. Address standards decide whether two records are the same property and the same person.
3. The recipient type decides the channel order; match confidence decides who gets a call.
4. Mailbox provider rules decide the email settings; the suppression list decides who hears from anyone at all.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/zillow-agents-scraper
- https://scrapercity.com/crexi-scraper
- https://scrapercity.com/bizbuysell-scraper
- https://pe.usps.com/text/pub28/welcome.htm
- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://hunter.io/cold-email-guide/email-bounce-rate
