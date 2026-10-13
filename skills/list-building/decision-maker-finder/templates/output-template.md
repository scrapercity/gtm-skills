# Decision Maker Report: [fill account list name]

Prepared [fill date] for [fill company or user]. Product being sold: [fill one line]. Plan: [fill plan]. Wallet before run: [fill $ balance].

## Account List

| Stage | Accounts | Dropped | Reason |
|-|-|-|-|
| Rows supplied | [fill] | [fill] | [fill] |
| After domain normalization and dedupe | [fill] | [fill] | [fill] |
| After domain resolution | [fill] | [fill] | [fill] |
| After suppression (customers, open deals) | [fill] | [fill] | [fill] |
| Accounts searched | [fill] | [fill] | [fill] |

Company size mix: [fill employee bands and account counts]

## Role Plan

Product category from `references/buying-role-map.md`: [fill]

| Slot | Buying role | Lead Database title | seniority | Website Finder jobTitle | Fallback jobTitle |
|-|-|-|-|-|-|
| 1 | [fill] | [fill] | [fill] | [fill] | [fill] |
| 2 | [fill] | [fill] | [fill] | [fill] | [fill] |

Contacts per account agreed with the user: [fill]

## Waterfall Results

| Step | Tool | Input | Found | Not found | Notes |
|-|-|-|-|-|-|
| 1 Lead Database by companyDomain | query_lead_database | [fill] | [fill] | [fill] | [fill] |
| 2 Website Finder, primary titles | scrape_website_finder | [fill] | [fill] | [fill] | [fill] |
| 3 Website Finder, fallback title | scrape_website_finder | [fill] | [fill] | [fill] | [fill] |
| 4 Email Finder for names without email | find_emails | [fill] | [fill] | [fill] | [fill] |
| 5 Validation | validate_emails | [fill] | [fill] | [fill] | [fill] |
| 6 Mobile Finder | find_mobiles | [fill] | [fill] | [fill] | [fill] |

## Coverage by Role

| Slot and role | Accounts searched | Filled (valid email) | Held (catch-all or unknown) | Empty | Fill rate |
|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

Accounts with at least one valid contact: [fill]. Accounts with every slot filled: [fill].

## Validation Results

| Status | Lead Database and Website Finder (validate_emails) | Email Finder (validated at lookup) | Total |
|-|-|-|-|
| valid | [fill] | [fill] | [fill] |
| valid_catch_all | [fill] | [fill] | [fill] |
| unknown | [fill] | [fill] | [fill] |
| invalid | [fill] | [fill] | [fill] |
| disposable | [fill] | [fill] | [fill] |
| Total | [fill] | [fill] | [fill] |

## Mobile Numbers

| Item | Value |
|-|-|
| Requested by user | [fill yes or no] |
| Stated use | [fill] |
| Inputs sent | [fill] |
| Numbers found | [fill] |
| Format | [fill] |
| Compliance check | [fill] |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |
| Total paid usage | | | [fill] |

Approval: [fill who approved which estimate and when]

## Sample Contacts

| account_domain | first_name | last_name | title | buying_role | found_by | email_status | mobile |
|-|-|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

## Gaps and Next Steps

| Gap | Accounts | Next action |
|-|-|-|
| [fill] | [fill] | [fill] |

1. [fill]
2. [fill]
