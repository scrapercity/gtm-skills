# Framework Notes: Skip Tracer

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Pick the search for each row and set `max_results` | `identifier-strategy-and-match-scoring.md` sections 1 and 2 |
| Band a match from its evidence | `identifier-strategy-and-match-scoring.md` section 3 |
| Handle LLC owners, trusts, banks, deceased owners | `identifier-strategy-and-match-scoring.md` section 5 |
| Price, pilot, batch, chain from Distress List | `skip-trace-runbook.md` sections 1 to 8 |
| Order phones, flag shared lines, group portfolio owners | `identifier-strategy-and-match-scoring.md` sections 6 and 7 |
| QA against the owner of record, call outcomes, handoff files, refresh | `skip-trace-runbook.md` sections 9 to 12 |
| Quote a price | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### USPS Publication 28

The Postal Service's addressing standard (street suffix abbreviations such as AVE, LN, DR; secondary unit designators such as APT, STE, UNIT; two-letter state codes; ZIP or ZIP+4). Applied rule: addresses are normalized to this format before any search, and rows without a ZIP are fixed before they cost money.

### ITU-T Recommendation E.164

The international numbering plan: a plus sign, the country code, then the national number, 15 digits at most. Applied rule: every phone is normalized to E.164 before dedupe, shared-line detection and dialer import, so one number written three ways counts once.

### County auditor and assessor records

Counties publish the owner of record for each parcel (Franklin County, Ohio, runs a public property search on its auditor site). Applied rule: a random sample of `confirmed` rows is checked against the owner of record before the call queue opens, and an evidence type that keeps missing moves down a band.

### ScraperCity catalog and API docs

- People Finder (`find_people`): $0.0199 per result, a search with 0 matches billed as 1 result; inputs are separate `name`, `email`, `phone_number` and `street_citystatezip` arrays plus `max_results`.
- Property Lookup (`scrape_property_lookup`): $0.15 per property, +$0.10 with `includeOwnerContact` for owner name, phone and email.
- Distress List (`scrape_distress_list`): $0.05 per property, `maxItems` 1 to 500, distress types preForeclosure, foreclosure, auction and bankOwned; its description says to pair it with People Finder to reach the owner.
- The API docs say results are stored for 48 hours.

Applied rule: every plan is priced from these numbers before it runs, and every run is downloaded the same day.

## Inputs this skill asks for instead of assuming

| Setting | Where it comes from |
|-|-|
| Pilot sample size per class | The user's budget; the example uses 25 rows |
| `max_results` for name searches | How many same-name candidates the user will pay to compare; the example uses 3 |
| QA sample size | The user's choice; the example checks 20 confirmed rows |
| Whether probable rows keep their calls | Wrong-party share by band after the first call block |
| Phone order by line type | Connect rate by line type after the first call block |
| Re-trace age and Distress List cadence | Wrong-number rate on older rows; how fast new filings appear in the market |

## What this skill does not do

- Run Criminal Records searches; this skill has no reason to call `search_criminal_records`.
- Write the call script or the cadence; `cold-calling` does.

## Sources

- USPS Publication 28: https://pe.usps.com/text/pub28/welcome.htm
- ITU-T Recommendation E.164: https://www.itu.int/rec/T-REC-E.164
- Twilio, What is E.164: https://www.twilio.com/docs/glossary/what-e164
- Franklin County Auditor, Ohio (property search): https://auditor.franklincountyohio.gov/home
- ScraperCity tool catalog: references/scrapercity-catalog.md
- ScraperCity API docs (48-hour result storage): https://scrapercity.com/api-docs
