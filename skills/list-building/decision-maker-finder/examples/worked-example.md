# Decision Maker Report: US food and beverage manufacturers, 300 accounts

Prepared 2026-10-13 for Clearbatch, which sells a food-safety audit and HACCP record platform to mid-size manufacturers. Plan: Growth ($149/mo). Wallet before run: $171.20. Company and person names are fictional and use the reserved `.example` domain.

## Account List

| Stage | Accounts | Dropped | Reason |
|-|-|-|-|
| Rows supplied | 318 | 0 | CRM export of target accounts built with `tam-builder` |
| After domain normalization and dedupe | 311 | 7 | Same registrable domain listed twice (www and bare forms, two brand names on one domain) |
| After domain resolution | 309 | 2 | 5 name-only rows resolved through `query_lead_database` with `companyName`; 2 could not be matched to a domain |
| After suppression (customers, open deals) | 300 | 9 | 6 current customers, 3 open opportunities owned by an AE |
| Accounts searched | 300 | 0 | Final account list |

Company size mix: 162 accounts at 51-200 employees, 98 at 201-500, 40 at 501-1,000.

## Role Plan

Product category from `references/buying-role-map.md`: 17, food and beverage manufacturing (food safety).

| Slot | Buying role | Lead Database title | seniority | Website Finder jobTitle | Fallback jobTitle |
|-|-|-|-|-|-|
| 1 | Economic buyer | VP Operations, COO, Chief Operating Officer, VP Supply Chain, VP Manufacturing | vp, c_suite | VP Operations | Chief Operating Officer |
| 2 | Champion | Director of Quality, Director of Food Safety, QA Manager, Quality Assurance Manager, Plant Manager | director | Director of Quality | Plant Manager |

Contacts per account agreed with the user: 2 (one per slot). `notTitle` on every call: assistant, intern, former, retired, coordinator, technician.

## Waterfall Results

| Step | Tool | Input | Found | Not found | Notes |
|-|-|-|-|-|-|
| 1 Lead Database by companyDomain | query_lead_database | 600 | 437 | 163 | 600 slots across 300 domains, 12 batches of 25 domains per slot; 401 people came with an email, 36 with a name only |
| 2 Website Finder, primary titles | scrape_website_finder | 163 | 66 | 97 | Two runs: VP Operations on 59 domains (27 found), Director of Quality on 104 domains (39 found) |
| 3 Website Finder, fallback title | scrape_website_finder | 97 | 31 | 66 | Chief Operating Officer on 32 domains (9 found), Plant Manager on 65 domains (22 found) |
| 4 Email Finder for names without email | find_emails | 36 | 25 | 11 | First name, last name and domain per contact; found emails are validated at lookup |
| 5 Validation | validate_emails | 498 | 439 | 59 | 401 Lead Database emails plus 97 Website Finder emails in one run; found means valid |
| 6 Mobile Finder | find_mobiles | 244 | 103 | 141 | Slot 1 contacts with a valid email only, sent as work emails |

## Coverage by Role

| Slot and role | Accounts searched | Filled (valid email) | Held (catch-all or unknown) | Empty | Fill rate |
|-|-|-|-|-|-|
| 1 Economic buyer | 300 | 244 | 21 | 35 | 81.3% |
| 2 Champion | 300 | 220 | 22 | 58 | 73.3% |

Accounts with at least one valid contact: 274. Accounts with every slot filled: 190.

Slot 1 empties: 23 domains where neither Website Finder title hit, 5 names Email Finder could not resolve, 7 invalid emails. Slot 2 empties: 43 with no Website Finder hit, 6 unresolved names, 8 invalid, 1 disposable.

## Validation Results

| Status | Lead Database and Website Finder (validate_emails) | Email Finder (validated at lookup) | Total |
|-|-|-|-|
| valid | 439 | 25 | 464 |
| valid_catch_all | 34 | 0 | 34 |
| unknown | 9 | 0 | 9 |
| invalid | 15 | 0 | 15 |
| disposable | 1 | 0 | 1 |
| Total | 498 | 25 | 523 |

The `validate_emails` start response reported `emailCount` 498, equal to the unique count sent. Catch-all and unknown rows (43) went to the hold file, not the main file.

## Mobile Numbers

| Item | Value |
|-|-|
| Requested by user | Yes, for slot 1 only |
| Stated use | Manual one-to-one calls by two account executives after the second email, no dialer, no texts |
| Inputs sent | 244 slot 1 work emails |
| Numbers found | 103 |
| Format | E.164 in the `mobile` column, never copied into `phone` |
| Compliance check | TCPA: manual dialing only, no prerecorded messages; numbers scrubbed against the National Do Not Call Registry and the internal do-not-call list before the call block; calls between 8 a.m. and 9 p.m. recipient local time |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Lead Database pass and domain resolution | 437 leads | Included in Growth plan | $0.00 |
| Website Finder, primary titles | 66 contacts found | $0.0499 | $3.29 |
| Website Finder, fallback titles | 31 contacts found | $0.0499 | $1.55 |
| Email Finder | 25 emails found (11 free misses) | $0.05 | $1.25 |
| validate_emails | 498 emails | $0.0072 | $3.59 |
| Mobile Finder | 103 numbers found (141 free misses) | $0.25 | $25.75 |
| Total paid usage | | | $35.43 |

Total without mobiles: $9.68, or $0.021 per valid contact (464). Wallet after run: $135.77.

Approval: the user approved the waterfall ceiling of $15.09 on 2026-10-13 after seeing the 600-slot plan, then approved a separate Mobile Finder ceiling of $61.00 (244 inputs x $0.25) once the slot 1 count was known.

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
| Slot 1 empty | 35 | Read each company's leadership page for a named COO or VP Operations, then send the names to `find_emails` ($0.05 per email found) |
| Slot 2 empty | 58 | Run Website Finder once more with "Food Safety Manager" on these domains, estimated ceiling 58 x $0.0499 = $2.89 |
| Held catch-all or unknown | 43 | Re-validate the 9 unknown rows on 2026-10-16; send catch-all rows only from a separate capped campaign |
| 501-1,000 employee accounts with slot 1 empty | 6 | Build an Apollo.io people search for these domains and run `scrape_apollo` (500 minimum, $1.95), with a webhook, since runs take hours to days |

1. Load the 464 valid rows into the sequencer with cross-campaign duplicate checking on; email slot 1 first and slot 2 one week later, never both on the same day (see `cold-email-list`).
2. Give the 103 mobile numbers to the two AEs as a manual call block after the second email, with the DNC scrub date recorded on each row.
