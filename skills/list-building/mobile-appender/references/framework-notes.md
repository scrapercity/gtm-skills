# Framework Notes: Mobile Appender

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Record the call plan before the pilot | `dial-status-and-suppression.md` section 1 |
| Run the suppression check | `dial-status-and-suppression.md` section 2 |
| Assign dial status | `dial-status-and-suppression.md` section 3 |
| Normalize LinkedIn URLs and emails before the append | `phone-normalization-and-line-type.md` section 1 |
| Convert found numbers to E.164 and check line type | `phone-normalization-and-line-type.md` sections 2 to 4 |
| Run the pilot and build the cost scenarios | `cost-and-hit-rate-model.md` |
| Quote a price | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### ScraperCity catalog and platform files

`find_mobiles` takes an array of social profile URLs or email addresses, auto-detected, and bills $0.25 per number found, nothing when no number is found. The platform file confirms Mobile Finder charges only when it finds something. Applied rule: misses are free, so a second pass with the work email for URL misses adds coverage at no risk of double billing, while sending both identifiers in one run can bill two hits for one person.

### ITU-T E.164

E.164 numbers are a plus sign, a country code and the national significant number, at most 15 digits. Applied rule: every delivered mobile matches `^\+[1-9]\d{7,14}$`, stored as text.

### Service Objects on number portability (September 10, 2015)

Service Objects, a phone data vendor, explains that a number can move from switch to switch and carrier to carrier, so the prefix is no longer an effective way to determine line type. Applied rule: line type comes from a carrier lookup, not from the area code or exchange.

### Twilio Lookup Line Type Intelligence

Twilio's Lookup v2 line type package returns a `type` for each number: landline, mobile, fixedVoip, nonFixedVoip, personal, tollFree, premium, sharedCost, uan, voicemail, pager or unknown. Applied rule: map these to the skill's `line_type` values in `phone-normalization-and-line-type.md` section 3.

### NIST/SEMATECH e-Handbook, confidence limits for a proportion

The standard error of a proportion is the square root of p x (1 - p) / n. At n = 50 and p = 0.5 that is about 0.07. Applied rule: a 50-input pilot is cheap (at most $12.50) and still separates a 20% list from a 50% list; the low and high scenarios sit at least 14 points either side of the pilot rate.

### IANA Time Zone Database

The `tz` column uses IANA zone names such as `America/Chicago`, which every major dialer and CRM accepts. Applied rule: the zone comes from the person's location, because a mobile keeps its area code when the owner moves.

## What this skill does not do

- Buy carrier lookups. The user holds that account.
- Append phones for consumers. That runs through `skip-tracer`.
- Write the call script or cadence. That runs through `cold-calling`.

## Sources

- ScraperCity tool catalog: references/scrapercity-catalog.md
- ITU-T E.164 (Twilio glossary summary): https://www.twilio.com/docs/glossary/what-e164
- Service Objects, The Benefits and Uses of Local Number Portability (2015-09-10): https://www.serviceobjects.com/blog/the-benefits-and-uses-of-local-number-portability/
- Twilio, Lookup Line Type Intelligence: https://www.twilio.com/docs/lookup/v2-api/line-type-intelligence
- NIST/SEMATECH e-Handbook, confidence limits for a proportion: https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
- IANA Time Zone Database: https://www.iana.org/time-zones
