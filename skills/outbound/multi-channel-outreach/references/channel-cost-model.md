# Channel Cost Model

What each channel costs per contact and per touch, built from ScraperCity catalog prices and dated vendor and regulator figures. Use it to decide which tier gets which channel and to show the user an estimate before any paid pull. ScraperCity prices come from `references/scrapercity-catalog.md`; every other figure carries its source and check date. Rates marked "assumption" are inputs to replace with your own numbers after the first two weeks.

## 1. Unit prices

### 1a. ScraperCity data and enrichment

| Need | Tool | Billable unit | Price | Notes |
|-|-|-|-|-|
| Mobile number from a work email or LinkedIn URL | `find_mobiles` | Number found | $0.25 | Free when nothing is found |
| Email validation before every email touch | `validate_emails` | Email | $0.0072 | Returns `email_result`, `email_quality`, `sc_mx_provider` |
| Work email from name and domain | `find_emails` | Email found | $0.05 | Free when not found; results are validated at lookup |
| Contact plus email (and optional mobile) at a domain for one title | `scrape_website_finder` | Contact found | $0.0499 | `autoFindMobiles: true` adds Mobile Finder lookups at $0.25 per number found |
| Local businesses with phone and address | `scrape_maps` | Business | $0.0099 | Business line, street address for mail |
| Local businesses, named contact, `contact_mobile` | `query_local_business_database` | Record | Included on Growth ($149/mo) and Scale | 100,000 new records a day |
| B2B contacts with phone, `linkedin_url` | `query_lead_database` | Record | Included on Growth and Scale | 100,000 new leads a day |
| Property details and owner contact for owner mail | `scrape_property_lookup` | Property | $0.15, +$0.10 with `includeOwnerContact` | Residential addresses: see the mail gate |
| Distressed properties | `scrape_distress_list` | Property | $0.05 | `maxItems` up to 500 |
| Person lookup by name, phone or address | `find_people` | Result | $0.0199 | A search with 0 matches is billed as 1 result |

### 1b. Channel costs outside ScraperCity

| Item | Price | Source and date |
|-|-|-|
| National Do Not Call Registry access, per area code per year | $85 (first 5 area codes free; $43 for an added area code in the second half of the year; $23,425 for every area code) | FTC press release, Aug 2026, effective 1 Oct 2026 |
| USPS domestic postcard stamp | $0.65 | USPS price change of 12 Jul 2026, via UMass Lowell notice (May 2026) |
| USPS First-Class letter stamp | $0.82 | Same |
| Printed postcard, all-in (print, postage, mailing), under 5,000 pieces a month | $0.85 to $1.50 each | directmail.io pricing guide, Apr 2026 |
| LinkedIn Sales Navigator Core | $99.99 a month, or $959.88 a year, per seat | LinkedIn compare-plans page, checked 2026-10-13 |
| LinkedIn Sales Navigator Advanced | $179.99 a month, or $1,679.88 a year, per seat | Same |
| Rep time | Loaded hourly cost (salary, taxes, tools) | Your payroll number (assumption until supplied) |
| Dialer seat | Vendor price | Your dialer contract; click-to-call or manual dialing only on cold mobiles (`references/channel-compliance-gates.md` section 3) |

## 2. Cost per touch formulas

```text
email_touch      = (mailbox seats + domains + sequencer + data) per month / cold sends per month
validation_share = $0.0072 per contact, paid once per contact per 30 days
mobile_per_found = $0.25
mobile_per_input = hit_rate x $0.25                     # hit_rate measured on a 50-input test
call_attempt     = rep_hourly_cost / dials_per_hour
linkedin_touch   = (seat price per month + rep minutes x rep_minute_cost) / touches per month
mail_piece       = print + postage (all-in vendor price) + list cost per address
dnc_access       = paid area codes x $85 / contacts called per year
```

Measure `hit_rate` before a large Mobile Finder run. Send 50 inputs from the real list; the run bills only numbers found, so the test costs at most 50 x $0.25 = $12.50. Divide numbers found by 50 and use that rate for the estimate.

## 3. Reference rates (assumptions to replace)

| Input | Starting assumption | Basis |
|-|-|-|
| Dials per rep hour, manual or click-to-call | 30 | alexberman.com cold calling article recommends 40 to 60 targeted calls a day; 2 hours of calling a day (roundup on alexberman.com) gives 20 to 30 an hour |
| Rep loaded cost | $35 an hour | Assumption; use payroll |
| LinkedIn manual touches per rep hour | 40 profile views or 20 personalized connection requests | Assumption; time a rep for one hour |
| Mobile Finder hit rate on owner emails | Measure with the 50-input test | No published rate; never estimate from memory |
| Cold email infrastructure cost per 1,000 sends | $18.66 (seats and domains only) | `domain-infrastructure` worked example: $235.11 a month over 12,600 sends |

## 4. Cost per touch at the reference rates

| Channel | Touch | Cost per touch | How |
|-|-|-|-|
| Email | One cold send | About $0.019 plus sequencer | $18.66 / 1,000 sends |
| Email | Validation per contact | $0.0072 | Once per contact per 30 days |
| Phone | One dial attempt | $1.17 | $35 / 30 dials |
| Phone | Mobile number for a tier A contact | $0.25 per number found | Free when not found |
| LinkedIn | Profile view | $0.88 rep time plus seat share | $35 / 40 views |
| LinkedIn | Personalized connection request | $1.75 rep time plus seat share | $35 / 20 requests |
| Direct mail | Postcard, all-in | $0.85 to $1.50 | directmail.io range |
| Direct mail | Letter with first-class stamp, printed in-house | $0.82 postage plus paper, envelope and labor | USPS rate |

Seat share for Sales Navigator Core: $99.99 a month over 400 touches a month is $0.25 a touch.

## 5. Cost per contact by tier

Using the default cadences in `references/channel-scripts-and-cadences.md` section 1 and the reference rates above.

| Tier | Touches | Data | Touch cost | Total per contact |
|-|-|-|-|-|
| A (email 4, calls 3, LinkedIn 3, postcard 1) | 11 | Validation $0.0072 + mobile $0.25 if found | Email 4 x $0.019 = $0.08; calls 3 x $1.17 = $3.51; LinkedIn view $0.88 + request $1.75 + message $0.88 + seat share 3 x $0.25 = $4.26; postcard $1.20 | About $9.31 |
| B (email 4, calls 2 on business line, LinkedIn 2) | 8 | Validation $0.0072 | Email $0.08; calls 2 x $1.17 = $2.34; LinkedIn view $0.88 + request $1.75 + seat share $0.50 = $3.13 | About $5.56 |
| C (email only, 4 touches) | 4 | Validation $0.0072 | $0.08 | About $0.09 plus sequencer |

Tier A costs about 100 times tier C per contact. That is why tiering comes before any mobile lookup or mail order.

## 6. Break-even spend per contact

```text
max_spend_per_contact = deal_value x close_rate x meeting_rate_for_that_tier
```

| Deal value | Close rate from meeting | Meeting rate per contact (assumption to test) | Break-even per contact |
|-|-|-|-|
| $3,000 | 20% | 2% | $12.00 |
| $8,000 | 25% | 3% | $60.00 |
| $1,000 | 20% | 1% | $2.00 |

A $1,000 deal with a 1% meeting rate cannot carry a $9.31 tier A cadence; it gets tier C. Meeting rates are hypotheses until the first 300 contacts per tier finish the cadence. Hand the measured rates to `outbound-unit-economics`.

## 7. DNC registry cost by market

The registry charges per area code per year; the first five are free (FTC, effective 1 Oct 2026).

| Market | Area codes | Paid area codes | Annual registry cost |
|-|-|-|-|
| Dallas-Fort Worth | 214, 469, 972, 945, 817, 682, 940 | 2 | $170 |
| Austin | 512, 737 | 0 | $0 |
| One state with 12 area codes | 12 | 7 | $595 |
| Every US area code | All | All | $23,425 |

The registry list must be refreshed at least every 31 days (FTC TSR Q&A). Buying access does not by itself make a call lawful; the gate in `references/channel-compliance-gates.md` still applies.

## 8. Cost estimate checklist before any paid step

1. `check_wallet` and record `wallet.total_balance_dollars`.
2. Count the list (`query_local_business_database` or `query_lead_database` with `limit: 1`, read `pagination.total`).
3. Tier the list and count each tier.
4. Run the phone gate on tier A and B; count numbers already present (`contact_mobile`, `phone`).
5. Run the 50-input Mobile Finder test; record the hit rate.
6. Price each line: validation, Mobile Finder at the measured rate, mail pieces, registry access.
7. Show the table with a ceiling (every input hits) and an expected figure (measured hit rate). Wait for a yes on anything over about $5.

## Sources

- ScraperCity tool catalog: `references/scrapercity-catalog.md`
- ScraperCity platform facts: `references/scrapercity-platform.md`
- FTC, FTC announces 2027 telemarketer fees to access the National Do Not Call Registry (Aug 2026): https://www.ftc.gov/news-events/news/press-releases/2026/08/ftc-announces-2027-telemarketer-fees-access-national-do-not-call-registry
- FTC, Q&A for telemarketers and sellers about DNC provisions in the TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr
- UMass Lowell, USPS July 2026 rate increases: https://www.uml.edu/myuml/submissions/2026/2026-05-29-15-11-43-usps-july-2026-rate-increases.aspx
- directmail.io, Direct mail cost and pricing 2026: https://directmail.io/blog/direct-mail-cost-pricing-2026/
- LinkedIn, Sales Navigator compare plans: https://business.linkedin.com/sales-solutions/compare-plans
- Alex Berman, cold calling techniques: https://alexberman.com/cold-calling-techniques
- Roundup on alexberman.com, manual outbound: https://alexberman.com/manual-outbound-beats-ai-cold-email
