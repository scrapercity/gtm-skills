# Decision Maker Report: US food and beverage manufacturers, 300 accounts

_Illustrative example. Companies, people, counts and run results are invented to show the format and use the reserved `.example` domain. Prices are ScraperCity catalog prices._

Prepared 2026-10-13 for Clearbatch, which sells a food-safety audit and HACCP record platform to mid-size manufacturers. ACV: $9,600. Plan: Growth ($149/mo). Wallet before run: $171.20.

## Account List

| Stage | Accounts | Dropped | Reason |
|-|-|-|-|
| Rows supplied | 318 | 0 | CRM export of target accounts |
| After domain normalization and dedupe | 311 | 7 | Same registrable domain listed twice (www and bare forms, two brand names on one domain) |
| After domain resolution | 309 | 2 | 5 name-only rows resolved by company name in the Lead Database; 2 could not be matched to a domain |
| After suppression (customers, open deals) | 300 | 9 | 6 current customers, 3 open opportunities owned by an AE |
| Accounts searched | 300 | 0 | Final account list |

Company size mix: 162 accounts at 51-200 employees, 98 at 201-500, 40 at 501-1,000.

## Role Plan

Product category: food and beverage manufacturing, food safety.

| Slot | Buying role | Lead Database title | seniority | Website Finder jobTitle | Fallback jobTitle |
|-|-|-|-|-|-|
| 1 | Economic buyer | VP Operations, COO, Chief Operating Officer, VP Supply Chain, VP Manufacturing | vp, c_suite | VP Operations | Chief Operating Officer |
| 2 | Champion | Director of Quality, Director of Food Safety, QA Manager, Quality Assurance Manager, Plant Manager | director | Director of Quality | Plant Manager |

Contacts per account agreed with the user: 2 (one per slot). Roles that joined the user's past deals of this size, mapped in the committee file: none; Clearbatch's recent deals at this size closed without procurement or security review. `notTitle` on every call: assistant, intern, former, retired, coordinator, technician.

## Waterfall Results

| Step | Tool | Input | Found | Not found | Notes |
|-|-|-|-|-|-|
| 1 Lead Database by companyDomain | Lead Database | 600 | 437 | 163 | 600 slots across 300 domains, 12 batches of 25 domains per slot; 401 people came with an email, 36 with a name only |
| 2 Website Finder, primary titles | Website Finder | 163 | 66 | 97 | Two runs: VP Operations on 59 domains (27 found), Director of Quality on 104 domains (39 found) |
| 3 Website Finder, fallback title | Website Finder | 97 | 31 | 66 | Chief Operating Officer on 32 domains (9 found), Plant Manager on 65 domains (22 found) |
| 4 Email Finder for names without email | Email Finder | 36 | 25 | 11 | First name, last name and domain per contact; found emails are validated at lookup |
| 5 Validation | Email Validator | 498 | 439 | 59 | 401 Lead Database emails plus 97 Website Finder emails in one run; found means valid |
| 6 Mobile Finder | Mobile Finder | 244 | 103 | 141 | Slot 1 contacts with a valid email only, sent as work emails |

## Coverage by Role

| Slot and role | Accounts searched | Filled (valid email) | Held (catch-all or unknown) | Empty | Fill rate |
|-|-|-|-|-|-|
| 1 Economic buyer | 300 | 244 | 21 | 35 | 81.3% |
| 2 Champion | 300 | 220 | 22 | 58 | 73.3% |

Accounts with at least one valid contact: 274. Accounts with every slot filled: 190.

Slot 1 empties: 23 domains where neither Website Finder title hit, 5 names Email Finder could not resolve, 7 invalid emails. Slot 2 empties: 43 with no Website Finder hit, 6 unresolved names, 8 invalid, 1 disposable.

## Validation Results

| Status | Lead Database and Website Finder (Email Validator) | Email Finder (validated at lookup) | Total |
|-|-|-|-|
| valid | 439 | 25 | 464 |
| catch_all | 34 | 0 | 34 |
| unknown | 9 | 0 | 9 |
| invalid | 15 | 0 | 15 |
| disposable | 1 | 0 | 1 |
| Total | 498 | 25 | 523 |

The validation run reported 498 emails received, equal to the unique count sent. Catch-all and unknown rows (43) went to the hold file, not the main file.

## Mobile Numbers

| Item | Value |
|-|-|
| Requested by user | Yes, for slot 1 only |
| Stated use | Calls by two named account executives in a call block after the second email |
| Inputs sent | 244 slot 1 work emails |
| Numbers found | 103 |
| Format | E.164 in the `mobile` column, never copied into `phone` |
| Do-not-contact check | Numbers checked against Clearbatch's do-not-contact list (shared by the dialer, sequencer and CRM) before each block; anyone who replied "remove me" by email dropped |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Lead Database pass and domain resolution | 437 leads | Included in Growth plan | $0.00 |
| Website Finder, primary titles | 66 contacts found | $0.0499 | $3.29 |
| Website Finder, fallback titles | 31 contacts found | $0.0499 | $1.55 |
| Email Finder | 25 emails found (11 free misses) | $0.05 | $1.25 |
| Email Validator | 498 emails | $0.00169 | $0.84 |
| Mobile Finder | 103 numbers found (141 free misses) | $0.25 | $25.75 |
| Total paid usage | | | $32.68 |

Total without mobiles: $6.93, or $0.015 per valid contact (464). Wallet after run: $138.52.

Approval: the user approved the waterfall ceiling of $12.34 on 2026-10-13 after seeing the 600-slot plan, then approved a separate Mobile Finder ceiling of $61.00 (244 inputs x $0.25) once the slot 1 count was known.

## Sample Contacts

| account_domain | first_name | last_name | title | buying_role | found_by | email_status | mobile |
|-|-|-|-|-|-|-|-|
| northbayfoods.example | Lena | Okafor | VP Operations | Economic buyer | lead_db | valid | +14155550142 |
| northbayfoods.example | Grant | Feeney | Director of Quality | Champion | lead_db | valid | not requested |
| pinecrestmfg.example | Rafael | Quintero | Chief Operating Officer | Economic buyer | website_finder | valid | none found |
| harvestlanebakery.example | Mei | Takahashi | QA Manager | Champion | email_finder | valid | not requested |
| ridgefieldpackaging.example | Darnell | Briggs | VP Supply Chain | Economic buyer | lead_db | valid | +16145550178 |
| ridgefieldpackaging.example | Ines | Kowalczyk | Plant Manager | Champion | website_finder | valid | not requested |

Output files: `decision-makers-food-mfg-2026-10-13.csv` (464 rows, valid only), `decision-makers-food-mfg-2026-10-13-hold.csv` (43 rows), `decision-makers-food-mfg-2026-10-13-gaps.csv` (110 accounts with at least one empty or held slot).

## Gaps and Next Steps

| Gap | Accounts | Next action |
|-|-|-|
| Slot 1 empty | 35 | Read each company's leadership page for a named COO or VP Operations, then send the names to Email Finder ($0.05 per email found) |
| Slot 2 empty | 58 | Run Website Finder once more with "Food Safety Manager" on these domains, estimated ceiling 58 x $0.0499 = $2.89 |
| Held catch-all or unknown | 43 | Re-validate the 9 unknown rows on 2026-10-16; send catch-all rows as their own 100-contact cell once the first cell stays under 2% bounces |
| 501-1,000 employee accounts with slot 1 empty | 6 | Build an Apollo.io people search for these domains and run Apollo Scraper (500 minimum, $1.95), with a webhook, since runs take hours to days |

| # | Step | Owner | Date | Done when |
|-|-|-|-|-|
| 1 | Load the 464 valid rows into the sequencer with cross-campaign duplicate checking on; email slot 1 first and slot 2 one to two weeks later if slot 1 has not replied, never both at once | SDR lead | 2026-10-14 | 464 rows imported, slot 1 sequence live |
| 2 | Give the 103 mobile numbers to the two AEs as a call block after the second email, with the do-not-contact check date on each row | AEs | 2026-10-21 | Call block booked |
| 3 | At 50 connected calls (Clearbatch's review count), count wrong-person answers by title and swap any slot title above Clearbatch's 20% share | Sales manager | 2026-11-04 | Slot titles kept or swapped |
