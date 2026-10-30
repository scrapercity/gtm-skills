# Channel Cost Model

What each channel costs per contact and per touch, built from ScraperCity catalog prices and dated vendor figures. Use it to decide which tier gets which channel and to show the user an estimate before any paid pull. ScraperCity prices come from `references/scrapercity-catalog.md`; every other figure carries its source and check date. Rep cost, rep speed and meeting rates have no published default: they are the user's inputs, and the worked figures below label theirs as illustrative.

## 1. Unit prices

### 1a. ScraperCity data and enrichment

| Need | Tool | Billable unit | Price | Notes |
|-|-|-|-|-|
| Mobile number from a work email or LinkedIn URL | `find_mobiles` | Number found | $0.25 | Free when nothing is found |
| Email validation before every email touch | `validate_emails` | Email | $0.00169 | Returns `email_result`, `email_quality`, `sc_mx_provider` |
| Work email from name and domain | `find_emails` | Email found | $0.05 | Free when not found; results are validated at lookup |
| Contact plus email (and optional mobile) at a domain for one title | `scrape_website_finder` | Contact found | $0.0499 | `autoFindMobiles: true` adds Mobile Finder lookups at $0.25 per number found |
| Local businesses with phone and address | `scrape_maps` | Business | $0.0099 | Business line, street address for mail |
| Local businesses, named contact, `contact_mobile` | `query_local_business_database` | Record | Included on Growth ($149/mo) and Scale | 100,000 new records a day |
| B2B contacts with phone, `linkedin_url` | `query_lead_database` | Record | Included on Growth and Scale | 100,000 new leads a day |
| Property details and owner contact for owner mail | `scrape_property_lookup` | Property | $0.15, +$0.10 with `includeOwnerContact` | Residential addresses: see the mail rules |
| Distressed properties | `scrape_distress_list` | Property | $0.05 | `maxItems` up to 500 |
| Person lookup by name, phone or address | `find_people` | Result | $0.0199 | A search with 0 matches is billed as 1 result |

### 1b. Channel costs outside ScraperCity

| Item | Price | Source and date |
|-|-|-|
| USPS domestic postcard stamp | $0.65 | USPS price change of 12 Jul 2026, via UMass Lowell notice (May 2026) |
| USPS First-Class letter stamp | $0.82 | Same |
| Printed postcard, all-in (print, postage, mailing), under 5,000 pieces a month | $0.85 to $1.50 each | directmail.io pricing guide, Apr 2026 |
| LinkedIn Sales Navigator Core | $119.99 a month, or $1,079.88 a year, per seat | LinkedIn compare-plans page, checked 2026-10-13 |
| LinkedIn Sales Navigator Advanced | $159.99 a month, or $1,799.88 a year, per seat | Same |
| Sales Navigator InMail | 50 credits a month on Core; a credit returns when the recipient responds within 90 days | Valley, Sales Navigator cost explained (31 August 2026); LinkedIn Sales Solutions blog |
| Rep time | Loaded hourly cost (salary, taxes, tools) | Your payroll number |
| Dialer seat | Vendor price | Your dialer contract |

## 2. Cost per touch formulas

```text
email_touch      = (mailbox seats + domains + sequencer + data) per month / cold sends per month
validation_share = $0.00169 per contact, paid once before the contact's first send
mobile_per_found = $0.25
mobile_per_input = hit_rate x $0.25                     # hit_rate measured on a 50-input test
call_attempt     = rep_hourly_cost / dials_per_hour
linkedin_touch   = (seat price per month + rep minutes x rep_minute_cost) / touches per month
mail_piece       = print + postage (all-in vendor price) + list cost per address
```

Measure `hit_rate` before a large Mobile Finder run. Send 50 inputs from the list you plan to run; the run bills only numbers found, so the test costs at most 50 x $0.25 = $12.50. Divide numbers found by 50 and use that rate for the estimate.

## 3. Inputs

| Input | Where it comes from |
|-|-|
| Dials per rep hour, manual or click-to-call | Berman's cold calling article recommends 40 to 60 targeted calls a day, and a roundup on his site describes about two hours of calling a day, which gives 20 to 30 an hour. Replace with your dialer's count after the first week |
| Rep loaded cost per hour | Your payroll |
| LinkedIn manual touches per rep hour | Time a rep for one hour of views and one hour of requests |
| Mobile Finder hit rate on your list | The 50-input test above; no published rate |
| Cold email infrastructure cost per 1,000 sends | Your mailbox, domain and sequencer bills divided by sends; the `domain-infrastructure` worked example comes to $18.66 ($235.11 a month over 12,600 sends) |
| Meeting rate per contact and close rate from a meeting, per tier | Your own results; until the first cohort of each tier finishes, state them as hypotheses |

## 4. Cost per touch, worked with illustrative inputs

Illustrative inputs: $35 an hour loaded rep cost, 30 dials an hour, 40 profile views or 20 personalized connection requests an hour, $18.66 per 1,000 cold sends, a Sales Navigator Core seat carrying 400 touches a month. Swap in the user's numbers.

| Channel | Touch | Cost per touch | How |
|-|-|-|-|
| Email | One cold send | About $0.019 plus sequencer | $18.66 / 1,000 sends |
| Email | Validation per contact | $0.00169 | Once per contact before the first send |
| Phone | One dial attempt | $1.17 | $35 / 30 dials |
| Phone | Mobile number for a tier A contact | $0.25 per number found | Free when not found |
| LinkedIn | Profile view | $0.88 rep time plus seat share | $35 / 40 views |
| LinkedIn | Personalized connection request | $1.75 rep time plus seat share | $35 / 20 requests |
| Direct mail | Postcard, all-in | $0.85 to $1.50; plans use $1.50, the top of the range | directmail.io range |
| Direct mail | Letter with first-class stamp, printed in-house | $0.82 postage plus paper, envelope and labor | USPS rate |
| LinkedIn | InMail from a Core seat | No added cash: one of the 50 monthly credits, returned if they respond within 90 days | Seat already counted in seat share; $119.99 / 50 = $2.40 only if the seat were bought for InMail alone |

Seat share for Sales Navigator Core: $119.99 a month over 400 touches a month is $0.30 a touch.

## 5. Cost per contact by tier

Using the default cadences in `references/channel-scripts-and-cadences.md` section 1 and the illustrative inputs above.

| Tier | Touches | Data | Touch cost | Total per contact |
|-|-|-|-|-|
| A (email 4, calls 3, LinkedIn 3, postcard 1) | 11 | Validation $0.00169 + mobile $0.25 if found | Email 4 x $0.019 = $0.08; calls 3 x $1.17 = $3.51; LinkedIn view $0.88 + request $1.75 + message $0.88 + seat share 3 x $0.30 = $4.41; postcard $1.50 | About $9.75 |
| B (email 4, calls 2 on business line, LinkedIn 2) | 8 | Validation $0.00169 | Email $0.08; calls 2 x $1.17 = $2.34; LinkedIn view $0.88 + request $1.75 + seat share $0.60 = $3.23 | About $5.65 |
| C (email only, 4 touches) | 4 | Validation $0.00169 | $0.08 | About $0.08 plus sequencer |

Tier A costs about 120 times tier C per contact. That is why tiering comes before any mobile lookup or mail order.

## 6. Break-even spend per contact

```text
max_spend_per_contact = deal_value x close_rate x meeting_rate_for_that_tier
```

Illustrative inputs, to be replaced by the user's:

| Deal value | Close rate from meeting | Meeting rate per contact | Break-even per contact |
|-|-|-|-|
| $3,000 | 20% | 2% | $12.00 |
| $8,000 | 25% | 3% | $60.00 |
| $1,000 | 20% | 1% | $2.00 |

A $1,000 deal with a 1% meeting rate cannot carry a $9.75 tier A cadence; it gets tier C. Meeting rates are hypotheses until the first cohort of each tier finishes the cadence. Hand the measured rates to `outbound-unit-economics`.

## 7. Cost estimate checklist before any paid step

1. `check_wallet` and record `wallet.total_balance_dollars`.
2. Count the list (`query_local_business_database` or `query_lead_database` with `limit: 1`, read `pagination.total`).
3. Tier the list and count each tier.
4. Run the phone check on tier A and B; count numbers already present (`contact_mobile`, `phone`).
5. Run the 50-input Mobile Finder test; record the hit rate.
6. Price each line: validation, Mobile Finder at the measured rate, mail pieces, seats.
7. Show the table with a ceiling (every input hits) and an expected figure (measured hit rate). Wait for a yes on anything over about $5.

## Sources

- ScraperCity tool catalog: `references/scrapercity-catalog.md`
- ScraperCity platform facts: `references/scrapercity-platform.md`
- UMass Lowell, USPS July 2026 rate increases: https://www.uml.edu/myuml/submissions/2026/2026-05-29-15-11-43-usps-july-2026-rate-increases.aspx
- directmail.io, Direct mail cost and pricing 2026: https://directmail.io/blog/direct-mail-cost-pricing-2026/
- LinkedIn, Sales Navigator compare plans (checked 2026-10-13: Core $119.99 a month or $1,079.88 a year): https://business.linkedin.com/sales-solutions/compare-plans
- Valley, LinkedIn Sales Navigator cost explained (31 August 2026; Core includes 50 InMail a month): https://www.joinvalley.co/blog/linkedin-sales-navigator-cost-explained-2026
- Alex Berman, cold calling techniques: https://alexberman.com/cold-calling-techniques
- Roundup on alexberman.com, manual outbound: https://alexberman.com/manual-outbound-beats-ai-cold-email
