# Bulk Enrichment Pipeline: a CSV In, Send-Ready Rows and a CRM Update Out

How to run a file the user already has (a CRM export, an event list, a purchased list, last year's leads) through ScraperCity in batches: what to check before paying, which tool fills which gap in what order, how big each run should be, what to do with every result status, and what goes back into the CRM. Prices come from `references/scrapercity-catalog.md`. Hit rates are not published for any finder, so every count below that depends on one is labeled a planning assumption.

## 1. Stage map

```
INTAKE -> CLEAN -> SUPPRESS -> FILTER -> ROUTE BY GAP -> BATCH RUNS -> ROUTE BY RESULT -> QA SAMPLE -> EXPORT -> LEDGER AND METRICS
```

Every stage writes a file named `{stage}-{segment}-{YYYYMMDD}.csv` (`clean-crm-export-20261013.csv`), so a failure restarts from the last good file instead of from the top, and no paid step runs twice on the same rows.

## 2. Intake: which columns unlock which tool

| Column | Needed for | If missing |
|---|---|---|
| `email` | `validate_emails` | Route to the email gap (section 6) |
| `first_name`, `last_name` | `find_emails` | Lead Database lookup by domain and title, or `scrape_website_finder` with a role |
| `domain` (company website, not a free-mail domain) | `find_emails`, `scrape_website_finder`, Lead Database `companyDomain` | Take it from a work email or the website column; rows with neither go to a manual queue |
| `linkedin_url` | `find_mobiles`, Lead Database `socialUrl` | Use a work email for `find_mobiles` instead |
| `crm_id` | Idempotent write-back | Match on lowercase email, then on first + last + domain |
| `segment`, `source` | Tracing every row to the pull that produced it | Add constants before the first paid step |

Reject at intake, with a reason code in a `rejected` file: rows with no email and no domain, rows whose only domain is a free-mail provider when the goal is a work address, and exact duplicates.

## 3. Clean

| Step | Rule |
|---|---|
| Trim and lowercase | Every email and domain |
| Domain | Strip scheme, `www.` and path: `https://www.acme.example/about` becomes `acme.example` |
| Dedupe | First by lowercase email, then by `linkedin_url`, then by first + last + domain. Keep the row with the most filled fields and the newest `last_activity` |
| Phone | To E.164 if it will be loaded anywhere |
| Split names | A single `name` column into `first_name` and `last_name`; leave both empty when the split is unclear rather than guessing |

## 4. Suppress before paying

Remove these rows before any paid step. Every removed row is money not spent and a complaint that never happens.

| Remove | Source of the list |
|---|---|
| Current customers and open opportunities | CRM (route them to their owner instead) |
| Anyone who unsubscribed, bounced hard or complained | Sender suppression exports, merged into one list across every sending tool |
| People who asked not to be contacted, by any channel | The internal do-not-contact list kept with the CRM |
| Competitors and partners | A domain list the team maintains |
| Contacted inside your re-contact window | Sequencer history (set the window per campaign) |

## 5. Filter to the ICP before paying

If the rows include companies outside the target, cut them first. On Growth and Scale, a Lead Database call by `companyDomain` with `limit: 1` returns company fields (`company_industry`, `company_size`, `employees_count`, `company_annual_revenue`, `company_country`) at no wallet cost; filter on those, then pay for enrichment only on rows that pass. On Starter, filter on whatever firmographics the file already carries.

The saving is plain arithmetic: every row cut before `find_emails` saves up to $0.05, before `find_mobiles` up to $0.25.

## 6. Route each row by its gap, cheapest source first

| Row has | Row needs | Order | Price |
|---|---|---|---|
| Email from outside ScraperCity, or last validated before your re-check window | Deliverability | `validate_emails` | $0.00169 per email |
| Email from a `find_emails` run inside your re-check window | Nothing | Skip validation: Email Finder results are validated when found | $0 |
| First, last and domain, no email | Work email | 1. Lead Database by `companyDomain` (Growth plan), match first + last in your own code. 2. `find_emails` for the rest | 1. $0 wallet. 2. $0.05 per email found, free if not found |
| Domain and a target role, no person | The person and email | 1. Lead Database by `companyDomain` + `title` or `seniority` (Growth). 2. `scrape_website_finder` with `jobTitle` for domains with no match | 1. $0 wallet. 2. $0.0499 per contact found |
| Work email or LinkedIn URL | Mobile | `find_mobiles` | $0.25 per number found, free if not found |
| Name and street address (consumer or property owner) | Phone, email | `find_people` with `max_results: 1` | $0.0199 per result, a 0-match search billed as 1 |

A row that misses at every step is written as `not_found` with the steps tried. It is never filled with a constructed address (`first.last@domain`), which bounces and burns the sending domain.

## 7. Batch runs

| Rule | Value |
|---|---|
| One run per tool per batch | All of a batch's emails in one `validate_emails` call, all of its contacts in one `find_emails` call |
| Batch size | No per-run input cap is published. Size batches to what you can afford to rerun and check by hand; the ledger example uses 1,000 |
| Runs in flight | 10 at most (scrapercity.com/api-docs) |
| Status checks | Every 15 s (the npm client's interval); alert at the top of the tool's published delivery time; see `references/errors-and-retries.md` |
| Download | Within 48 hours of finishing; results are not kept longer |
| Rerun | Only the batch whose run ended `FAILED`, after reading its logs. Never resubmit a batch whose start got no response until `/api/v1/runs` shows no matching run |

### Batch ledger

One row per run, appended as each run starts and updated when it ends. It is the only way to replay a failure without paying twice.

| Column | Example |
|---|---|
| `batch_id` | `crm-export-20261013-b03` |
| `input_file` | `route-email-gap-20261013.csv` rows 2001-3000 |
| `tool` | `find_emails` |
| `run_id` | full id from the start response |
| `rows_in` | 1000 |
| `started_at`, `finished_at` | UTC timestamps |
| `status` | RUNNING, SUCCEEDED, FAILED, CANCELLED |
| `rows_found` | from the CSV, not from the start response |
| `cost` | rows billed x catalog price |
| `output_file` | `find-emails-crm-export-20261013-a1b2c3d4.csv` |
| `retry_of` | the `batch_id` this one replaces, if any |

## 8. Route by result

Column names in the validator CSV have differed between ScraperCity guides, so read the header of the first download and map these meanings onto whatever it uses.

| Result | Route | Note |
|---|---|---|
| Valid | Send-ready file and CRM `email_status = valid` | |
| Catch-all (server accepts any address) | Separate campaign | Track its bounce rate apart from the valid file |
| Unknown (timeout, greylisting) | Hold; re-validate once before any send | |
| Invalid | Remove from every send file, add to bounce suppression | Try `find_emails` for a replacement only for people on a named account or opportunity |
| Finder not found | `not_found`, no charge | Next step in section 6, or stop |
| Run `FAILED` | Read `statusMessage` and logs, fix the input, rerun that batch | Never rerun unchanged |

## 9. QA sample before export

Pull a random sample of send-ready rows and check each against the person's company website or public profile: right person, right company, plausible email format. Set the sample size and pass mark before you look. Below the mark, find the step that produced the bad rows (one finder, one segment, one source file) and fix it before exporting anything.

## 10. Export

### Sender file

Valid rows only, suppression applied a second time on the final file (lists change while runs finish), one email per row, segment and source columns kept for reporting. Field names per sender: the `scrapercity-integrations` skill.

### CRM write-back rules

Enrichment writes into the CRM in one direction. Do not set up a two-way sync between the enrichment file and the CRM: the CRM's older values would overwrite fresh results on the next sync.

| Field | Rule |
|---|---|
| `email_status`, `email_validated_at`, `enrichment_source`, `enriched_at` | Always write |
| `email` | Write only if the CRM field is empty or its status is invalid |
| `phone`, `mobile`, `title`, `linkedin_url` | Write only if empty. Otherwise put the new value in an `enriched_*` review column |
| Company differs from the CRM's company | Do not overwrite. Flag as a possible job change for review (see the job-change recipe in the `scrapercity-integrations` skill) |
| Owner, lifecycle stage, deal and opportunity fields | Never write |

Upsert on `crm_id`; without it, on lowercase email. Run a few records end to end and look at them in the CRM before the full batch.

## 11. Metrics after every batch

| Metric | Formula | Use |
|---|---|---|
| Found rate per tool | rows found / rows sent to that tool | Replace the planning assumption with this number for the next batch of the same segment |
| Valid rate | valid / validated | A falling valid rate on one source means the source is aging |
| Cost per send-ready row | total spend / send-ready rows | The number to compare against other sources |
| Failed-run rate | runs ending `FAILED` / runs started, per tool | Above zero, read the logs before the next batch; a repeat failure on the same input file means a bad column, not bad luck |
| Hard bounce rate on the first send | hard bounces / delivered | Instantly auto-pauses a campaign above 5% by default (Instantly help center, checked 2026-10-13). A rising rate on one source means re-check the routing in section 8 |
| Spam complaint rate | from Google Postmaster Tools | Keep it under 0.1% and never let it reach 0.3% (Google sender guidelines FAQ) |

## 12. Illustrative example

_Illustrative example. Counts and hit rates are invented to show the arithmetic; prices are catalog prices._

A 5,000-row CRM export on Growth. 3,800 rows have an email from outside ScraperCity; 1,200 have a name and domain but no email.

| Stage | Rows | Tool | Billable units | Unit price | Cost |
|---|---:|---|---:|---:|---:|
| Suppression removes customers, unsubscribes and recent contacts | 5,000 to 4,550 | none | 0 | | $0.00 |
| Validate existing emails (3,800 minus 300 suppressed) | 3,500 | `validate_emails` | 3,500 | $0.00169 | $5.92 |
| Lead Database by domain for the 1,050 missing emails left after suppression; 40% matched by name (assumption) | 1,050 | `query_lead_database` | 0 | included | $0.00 |
| Email Finder on the 630 still missing; 55% found (assumption) | 630 | `find_emails` | 347 | $0.05 | $17.35 |
| **Expected total** | | | | | **$23.27** |

Ceiling if every Email Finder lookup hits: 630 x $0.05 = $31.50, so 5.92 + 31.50 = $37.42. Both figures go to the user before the first run. The 347 found emails skip validation because Email Finder validated them. Lead Database calls: one per unique domain at 1 a second, well inside 100 a minute.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/api-docs
- https://scrapercity.com/pricing
- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
