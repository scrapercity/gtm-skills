# Tech Stack Decision Guide

When to pay for Tech Stack Search, which technologies change which pitch, the free signals to check first, and how to read and reuse the results. Tech Stack Search is ScraperCity's `scrape_builtwith` tool: it takes one `technology` and returns the domains detected using it, at $4.99 per technology (`references/scrapercity-catalog.md`).

## 1. The decision

A technology earns a place in the brief only if knowing it changes one of these: whether to contact the account at all, which case study to lead with, the opening line, or who to contact.

| Situation | Check with | Cost |
|-|-|-|
| The product only works with a given platform (a Shopify app, a Salesforce add-on) | Tech Stack Search, unless a free signal confirms it | $4.99 per technology, once |
| The pitch differs by which competitor they run (displacement vs greenfield) | Tech Stack Search for each competitor that has a separate pitch | $4.99 each |
| Integration is a selling point but not a requirement | Free signals only; mark "likely" | $0 |
| Curiosity, or "good to know" | Do not check | $0 |
| The same technology decides the pitch for 5+ accounts this month | One Tech Stack Search, reused for every account | $4.99 total |
| Mail platform and security gateway (for deliverability notes) | `validate_emails` columns `sc_mx_provider`, `sc_mx_security_gateway` | $0.0072 per email |

Show the user the technologies and the $4.99 each before running, and call `check_wallet` first when the total passes $5.

## 2. Technologies that commonly change the pitch

| User sells | Technology to check | Present means | Absent means |
|-|-|-|-|
| CRM services, RevOps consulting | Salesforce, HubSpot | Pitch the platform they run; both present means a sync and routing angle | Greenfield or a smaller CRM; pitch selection and setup |
| Shopify apps, Shopify agencies | Shopify, Shopify Plus | Qualified | Disqualify, or pitch a migration only if the user does migrations |
| Email and SMS retention for ecommerce | Klaviyo, Attentive, Postscript | Displacement pitch or an add-on pitch | Greenfield pitch with a revenue estimate |
| WordPress maintenance or hosting | WordPress, WooCommerce | Qualified | Different offer or skip |
| Marketing automation consulting | Marketo, Pardot, HubSpot | Platform-specific case study | Selection pitch |
| Support platforms | Zendesk, Intercom, Gorgias | Displacement with a migration offer | Greenfield |
| Analytics and data tools | Segment, Snowflake, Google Analytics 4 | Integration story | Data foundation pitch |
| Payments and checkout | The user's direct competitors by name | Displacement | Greenfield |
| Website agencies | Wix, Squarespace, Webflow | Rebuild or migration pitch | Different angle |

Name the technology the way the user's market names it (for example "HubSpot", "Shopify", "WordPress", the forms the tool description itself uses). A misspelled or vague name returns a thin or empty list and still costs $4.99.

## 3. Free signals to check first

| Signal | How to read it | Strength |
|-|-|-|
| Page source of the homepage | Script hosts such as `js.hs-scripts.com` (HubSpot tracking), `cdn.shopify.com` (Shopify), `static.klaviyo.com` (Klaviyo), `munchkin.marketo.net` (Marketo), `pi.pardot.com` (Pardot), `widget.intercom.io` (Intercom), `static.zdassets.com` (Zendesk), `cdn.segment.com` (Segment), `static.hotjar.com` (Hotjar), `googletagmanager.com` (Google Tag Manager) | Strong for front-end tools; silent for back-office tools such as CRMs and ERPs |
| Careers page postings | "Salesforce administrator", "experience with NetSuite", "migrating to HubSpot" | Strong for back-office tools; also shows migrations in progress |
| Login or portal links | `company.my.salesforce.com`, `company.zendesk.com`, `help.company.com` hosted by a support platform | Strong |
| `sc_mx_provider` from `validate_emails` | Google Workspace or Microsoft 365 | Strong for the mail platform |
| `sc_mx_security_gateway` from `validate_emails` | A gateway such as Mimecast, Proofpoint or Barracuda | Strong; plan plain-text, low-link email |
| Lead Database `keywords` | Tags that sometimes name platforms | Weak; confirm elsewhere |
| Case studies and partner directories | The vendor lists the account as a customer | Strong, but may be old; check the date |
| Employee profiles | Titles like "HubSpot Admin" | Medium |

Record the signal, where it was seen and the date. A free signal marks the row "likely"; Tech Stack Search or two independent strong signals mark it "confirmed".

## 4. Running Tech Stack Search

MCP:

```json
{"technology": "Salesforce", "fileName": "techstack-salesforce-20261013"}
```

CLI: `npx scrapercity builtwith "Salesforce"`. REST: `POST /api/v1/scrape/techstack` with the same body. The start response returns a `runId` and `estimatedCost`. Check `check_run_status` after 30 seconds, then every 30 seconds; runs usually finish in minutes. Download with `download_results` and an absolute `outputPath`, within 48 hours.

Reading the CSV:

1. Read the header row; find the domain column.
2. Normalize every domain to its registrable form (`shop.acme.example` to `acme.example`).
3. Look up each researched account's registrable domain and its known aliases.
4. Present: "confirmed". Absent: "not detected". Never write "not used" from an absence.
5. Keep the file under `techstack-[technology]-[date].csv` with the run id in the run log.

## 5. Cost amortization

| Accounts researched this month | Technologies that change the pitch | Tech Stack Search cost | Per account |
|-|-:|-:|-:|
| 1 | 2 | $9.98 | $9.98 |
| 10 | 2 | $9.98 | $1.00 |
| 25 | 2 | $9.98 | $0.40 |
| 25 | 4 | $19.96 | $0.80 |

The same CSV also gives a target list: every domain running the technology. Hand it to `ecommerce-by-techstack` (stores) or filter it through the Lead Database with `companyDomain` batches to find people at lookalike accounts.

## 6. Reading results with care

| Result | What to write | Why |
|-|-|-|
| Domain present | Confirmed, with run id and date | Detection found a footprint |
| Domain absent, free signal says present | Likely, cite the free signal | Detection can miss a tool used on a subdomain or a different domain |
| Domain absent, no free signal | Not detected | Absence of a footprint is weak evidence for back-office tools |
| Present on a subsidiary's domain only | Note which entity | The parent may run something else |
| Two competing tools both present | Note both; ask on the call | Migrations and team-by-team choices are common |

## 7. How the stack shows up in the brief

| Column | Rule |
|-|-|
| Technology | As named in the search |
| Status | confirmed, likely or not detected |
| Evidence | The signal and where it came from |
| Changes pitch? | yes or no; rows with "no" are allowed only for free signals that inform deliverability (mail platform, gateway) |
| Source | Source ID from the brief's Sources table |

## Sources

- ScraperCity tool catalog and `scrape_builtwith` schema: https://www.npmjs.com/package/scrapercity
- ScraperCity, How to use: https://scrapercity.com/how-to-use
- ScraperCity, Email Validator (MX provider and security gateway columns): https://scrapercity.com/email-validator
- HubSpot, Install the HubSpot tracking code: https://knowledge.hubspot.com/reports/install-the-hubspot-tracking-code
- Public Suffix List: https://publicsuffix.org/
