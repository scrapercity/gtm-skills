# Enrichment Waterfalls with ScraperCity

A waterfall asks several sources in a fixed order, runs each one only on the rows the step before it missed, and stops at the first usable result. This file sets the order for ScraperCity's tools by cost per found record, gives the per-row spending ceiling, shows the same waterfall as Clay columns and as an n8n flow, and says where providers the team already pays for fit. Prices come from `references/scrapercity-catalog.md`. ScraperCity does not publish hit rates for any finder, so every hit rate below is a planning assumption to replace with a measured one.

## 1. One waterfall per data type

| Waterfall | Steps in order | Stops when |
|---|---|---|
| Company firmographics | Lead Database by `companyDomain`, `limit: 1` (company fields on the record) | Any record returns |
| Person at an account | Lead Database by `companyDomain` + `title` or `seniority`, then `scrape_website_finder` with one `jobTitle` | A named person with the role is found |
| Work email | Email on the Lead Database record, then `find_emails` (first, last, domain), then `scrape_website_finder` when there is a role but no name | An address is found; then validation decides if it is usable |
| Mobile | Phone on the database record (`hasPhone`, or `contact_mobile` in the Local Business Database), then `find_mobiles` with the LinkedIn URL or work email | A number is found |
| Local business contact | Local Business Database with `hasContact: true`, then `scrape_maps` or `scrape_yelp` for the business line | A named contact or a business phone |

Mixing types in one chain (asking an email finder for a phone, or a phone tool for an email) pays twice for a weaker answer.

## 2. Order steps by cost per found record

```
cost per found = price per billed unit x billed units / records found
```

| Step | Billing | Cost per found |
|---|---|---|
| Lead Database, Local Business Database (Growth and Scale) | No wallet charge; new records count toward 100,000 a day | $0 |
| `find_emails` | $0.05 per email found, nothing on a miss | $0.05 at any hit rate |
| `scrape_website_finder` | $0.0499 per contact found | $0.0499 at any hit rate |
| `find_mobiles` | $0.25 per number found, nothing on a miss | $0.25 at any hit rate |
| `find_people` | $0.0199 per result, a 0-match search billed as 1 | $0.0199 / hit rate: $0.0398 at a 50% hit rate (assumption) |
| A provider that bills per lookup | Price per lookup whether or not it finds | price / hit rate: a $0.03 lookup at a 40% hit rate is $0.075 per found |

Pay-on-find steps cost the same per found record at any hit rate, so they go after the free database and before anything billed per lookup. A per-lookup provider with a low hit rate is the most expensive step per result even when its sticker price is the lowest.

## 3. Per-row ceiling

The most one row can cost in the work email waterfall:

| Path | Billed | Cost |
|---|---|---:|
| Database has the email, then validate it before sending | `validate_emails` | $0.0072 |
| Database misses, Email Finder finds (validated when found, no second check) | `find_emails` | $0.05 |
| Both miss, Website Finder finds the role holder, then validate | `scrape_website_finder` + `validate_emails` | $0.0571 |
| Every step misses | nothing | $0.00 |

So the ceiling is $0.0571 per row, plus $0.25 when a mobile is requested and found. For 2,000 rows the email ceiling is 2,000 x $0.0571 = $114.20; show that next to the expected cost before the first run. Rows that reach the end with nothing are written as `not_found` and never get a constructed `first.last@` address.

## 4. Validation gate

| Source of the address | Validate before sending? |
|---|---|
| `find_emails`, found inside your re-check window | No. The catalog says every email it finds is validated |
| Lead Database or Local Business Database record | Yes, $0.0072 each |
| `scrape_website_finder` | Yes, or send `autoValidateEmails: true` with the run (the catalog does not list a separate price for that flag; check the run cost in `/api/v1/runs` on a small test) |
| Another provider, a CRM, a purchased list | Yes |
| Any address last validated before your re-check window | Yes |

Route the validator's results the same way everywhere: valid to the sender; catch-all to its own campaign with its bounce rate tracked apart; unknown held and re-checked once before any send; invalid to bounce suppression.

## 5. Clay: the waterfall as columns

Clay's HTTP API column is synchronous, so only the database steps run per row. The pay-on-find steps run as one batched run per table, outside the per-row columns.

| Order | Column | Type | Run condition |
|---|---|---|---|
| 1 | `icp_pass` | Formula on firmographic columns | Always |
| 2 | `sc_person` | HTTP API, GET `/api/v1/database/leads`, `companyDomain` = Domain, `title` = the role, `hasEmail` = true, `limit` = 3; ScraperCity header account; 1 request per 1,000 ms | `icp_pass` is true and Domain is not empty |
| 3 | `db_email`, `db_first`, `db_last` | Field extraction from `sc_person.data` | `sc_person` has data |
| 4 | `finder_email` | Written back by a Clay webhook source after one batched `find_emails` run (n8n or code sends every row where `db_email` is empty and a name exists) | Filled by the webhook, not run per row |
| 5 | `other_email` | A provider the team already pays for, if any | `db_email` and `finder_email` both empty |
| 6 | `best_email`, `email_source` | Formula: first non-empty of `db_email`, `finder_email`, `other_email`, plus which column it came from | Always |
| 7 | `email_status` | Written back after one batched `validate_emails` run on every `best_email` whose source is not `finder_email` | Filled by the webhook |
| 8 | `send_ok` | Formula: `email_status` is valid and the row is not on the suppression list | Always |

Clay formulas are JavaScript expressions with columns inserted as `{{Column}}` (Clay University, formula generator), so the three formula columns are one line each:

| Column | Formula |
|---|---|
| `best_email` | `{{db_email}} \|\| {{finder_email}} \|\| {{other_email}} \|\| ""` |
| `email_source` | `{{db_email}} ? "lead_database" : {{finder_email}} ? "email_finder" : {{other_email}} ? "other_provider" : "not_found"` |
| `send_ok` | `{{email_status}} === "valid" && !{{suppressed}}` |

Run condition on `sc_person`: `{{icp_pass}} && !!{{Domain}}`. `suppressed` is a true or false column from a lookup of `best_email` against the team's suppression table. Check the validator's exact status word on the first download (it has differed between ScraperCity guides) and match it in `send_ok`. A row whose `email_source` is `not_found` stays empty; no formula ever builds an address from a name pattern.

Push to the sender only rows where `send_ok` is true. If the team already runs Clay's built-in provider waterfall, put the ScraperCity database column in front of it (free on Growth) and send only that waterfall's misses to the batched Email Finder run.

## 6. n8n: the same waterfall without Clay

1. Read the account or contact rows (sheet, CRM, database).
2. HTTP Request per row, batched 1 item per 1,000 ms: Lead Database by `companyDomain` (+ role). Split rows into found and missing.
3. One HTTP Request: `POST /api/v1/scrape/email-finder` with every missing row's `first_name`, `last_name`, `domain` in `contacts`. Store the `runId`.
4. Webhook node: on the ScraperCity notification for that `runId`, confirm `SUCCEEDED`, download, parse the CSV, merge on lowercase name + domain.
5. One `POST /api/v1/scrape/email-validator` with every address that did not come from Email Finder. Same webhook pattern.
6. Route by result (section 4) and load. Recipes for each node: `references/automation-recipes.md`.

## 7. Measure, then re-order

1. Pilot 50 rows per segment through every step, even after a hit, and record found per step.
2. Compute cost per found with section 2's formula. Re-order steps that bill per lookup by that number.
3. Rerun the pilot each quarter, and whenever the segment changes (new country, new company size, new role); hit rates differ by segment and drift over time.
4. Keep `email_source` on every row so bounces can be traced to the step that produced them.

## 8. Illustrative example

_Illustrative example. Hit rates are invented to show the arithmetic; prices are catalog prices._

1,000 target accounts on Growth, one VP of Marketing wanted per account.

| Step | Inputs | Found (assumption) | Billed units | Unit price | Cost |
|---|---:|---:|---:|---:|---:|
| Lead Database by domain + title | 1,000 | 620 people, 590 with email | 0 | included | $0.00 |
| `scrape_website_finder`, `jobTitle: "VP Marketing"`, on 380 domains with no match | 380 | 150 | 150 | $0.0499 | $7.49 |
| `find_emails` on 30 database people with no email | 30 | 18 | 18 | $0.05 | $0.90 |
| `validate_emails` on 590 database emails + 150 Website Finder emails | 740 | | 740 | $0.0072 | $5.33 |
| **Expected total** | | | | | **$13.72** |

Ceiling if every pay-on-find step hits: 380 x $0.0499 + 30 x $0.05 + (590 + 380) x $0.0072 = $18.96 + $1.50 + $6.98 = $27.44. Both figures go to the user before the first paid step. Coverage: 590 + 150 + 18 = 758 of 1,000 accounts with an address before validation.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/pricing
- https://scrapercity.com/api-docs
- https://scrapercity.com/integrations
- https://university.clay.com/docs/webhook-integration-guide
- https://university.clay.com/docs/http-api-integration-overview
- https://university.clay.com/docs/formula-generator
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
