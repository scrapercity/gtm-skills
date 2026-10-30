# Pipeline Runbook

Stage-by-stage mechanics for turning domains or an ICP into a send-ready file: capacity sizing, sourcing recipes, gap fill, dedupe, suppression, per-company waves and personalization columns. Prices from `references/scrapercity-catalog.md`; run rules from `references/scrapercity-agent-patterns.md`.

## 1. Capacity sizing

| Input | Symbol | Default |
|-|-|-|
| Mailboxes connected to the sequencer | M | Ask |
| Cold sends per mailbox per day | S | 30, Instantly's recommendation for campaign emails; always under 50 (Alex Berman) |
| Steps per prospect | K | Ask; Berman's follow-up guide plans 4 to 6 follow-ups over 2 to 3 weeks |
| Sending days in the campaign window | D | Ask |
| Yield: send-ready rows / rows pulled | Y | Measured on the user's last list for this segment, or on a first wave |

```text
daily_sends       = M x S
new_prospects_day = daily_sends / K           (steady state once follow-ups overlap)
send_ready_target = daily_sends x D / K
pull_rows         = ceil(send_ready_target / Y / 100) x 100
sending_days      = ceil(send_ready_rows x K / daily_sends)
```

| Mailboxes | Daily sends at 30 | Send-ready rows for 20 days, 3 steps |
|-:|-:|-:|
| 3 | 90 | 600 |
| 6 | 180 | 1,200 |
| 10 | 300 | 2,000 |
| 20 | 600 | 4,000 |

The 20 days and 3 steps in the table are example inputs. When the user asks for more rows than the window can send, build the first wave only and schedule the next pull with `excludeDelivered: true`. Rows validated more than four weeks before their send date need a second validation pass ($1.69 per 1,000): Hunter's 2025 decay test found over 2% of a list invalid after four weeks, which alone reaches Berman's 2% bounce line.

## 2. Sourcing recipes

### A. From target domains

1. Normalize domains, drop duplicates and suppressed accounts.
2. Batch domains in `companyDomain` (halve the batch on a 503, which means the search ran too long), with the role `title` list, `notTitle`, and `seniority` when the role map gives one. `limit: 1` per batch to count, then `limit: 100` with `after` paging.
3. Rank per domain: exact title, seniority, email present, person at HQ. Keep up to the contacts per company the user agreed.
4. Domains with zero people go to Website Finder (section 3).

### B. From an ICP

1. Filters from the ICP: `title` or `seniority` plus `department`, `industry` or `keywords`, `minEmployees` and `maxEmployees`, `country`, `hasEmail: true`, `notTitle`.
2. Count with `limit: 1`. Read a page of rows and check titles before pulling; tighten `notTitle` when partial matches slip in.
3. Pull `pull_rows` with `after` cursors.

### C. From a people-search URL

1. `query_lead_database` with `url` and `limit: 1`. Read `search_translation`: applied, approximated, not supported.
2. Re-add unsupported filters as native parameters, then pull.
3. Only when the database cannot express the search, run `scrape_apollo` with `url`, `count` (500 to 50,000) and `fileName`. Cost: count x $0.0039. Register a webhook first; runs usually take 15 to 30 minutes.

### D. From a CRM export

1. Map columns to the person schema.
2. Rows with a name and domain but no email go to Email Finder.
3. Rows with an email go straight to dedupe, suppression and validation; treat them like `email-list-cleaner` input.

### E. Local businesses

Build with `local-business-list` (database first, scrapes for gaps), then join this runbook at section 4.

## 3. Gap fill

| Gap | Call | Billing | Ceiling |
|-|-|-|-|
| Domain returned zero people for the role | `scrape_website_finder` with `domains` and one `jobTitle`; second run with a fallback title on the misses | $0.0499 per contact found | domains x $0.0499 |
| Person with no email | `find_emails` with `contacts: [{first_name, last_name, domain}]` | $0.05 per email found, free if not | contacts x $0.05 |
| Person with only a company name | Resolve the domain with `query_lead_database` `companyName` first; `company_name` in `find_emails` is the fallback | Same | Same |

Run a test batch (size set by the user) before a large Website Finder or Email Finder batch, then multiply the test's hit rate by the full input count to quote an expected cost next to the ceiling. Both tools bill only on a find, so the hit rate changes total spend and how many rows reach the gaps file, never the price of each hit.

| Source of the email | Paid per usable address | At an 80% valid share (example input; measure on your first batch) |
|-|-|-|
| Lead Database, then `validate_emails` | $0.00169 / valid share | $0.0021 |
| `find_emails` (validated at lookup per its tool description) | $0.05 | $0.05 |
| `scrape_website_finder`, then `validate_emails` | ($0.0499 + $0.00169) / valid share | $0.064 |

Email Finder batches from the CLI: `npx scrapercity email-find --file contacts.csv` wants a header row containing "first" and reads columns by position (first name, last name, domain, company name), splitting on every comma with no quote handling. Strip commas from names and company names, or send the batch as JSON through MCP or REST. A person whose name will not split into first and last can be sent as `full_name` with the domain.

A miss is recorded in the gaps file. No address is built from a naming pattern; on a catch-all domain a built address passes validation and then bounces.

## 4. Dedupe

| Order | Key | Notes |
|-|-|-|
| 1 | Lowercased `email` | Collapse Gmail dots and `+tags` only for consumer Gmail addresses |
| 2 | Normalized `linkedin_url` | Catches a person with two work emails |
| 3 | `first_name + last_name + company_domain` | Catches the same person from two sources |

Survivorship: valid status beats any other; non-empty beats empty; user CRM data beats Email Finder and Website Finder, which beat the Lead Database, which beats Apollo; newer `pulled_at` wins ties. The merged `source` joins contributors with a pipe (`lead_db|email_finder`).

Dedupe before validation; the validator bills unique addresses per run, and local dedupe also removes near-duplicates and rows you would suppress anyway.

## 5. Suppression order

| # | List | Match on | Permanent? |
|-|-|-|-|
| 1 | Unsubscribes and removal requests, added the same day in every tool | Email, and domain when the person asked for the company | Yes |
| 2 | Hard bounces | Email | Yes |
| 3 | Spam complaints | Email and domain | Yes |
| 4 | Current customers | Domain | While a customer |
| 5 | Open opportunities | Domain | While open |
| 6 | Competitors and partners | Domain | Yes |
| 7 | Leads in another active campaign | Email | Until that campaign ends |
| 8 | Contacted inside the user's re-contact window | Email | Until the window ends (Berman's cycle model restarts every 30 to 60 days) |

Keep one suppression list and export every list from the sequencer and CRM on the day of the build, not from last month's file.

## 6. Per-company cap and waves

1. Sort each company's rows by buying role priority (economic buyer, champion, evaluator), then title match.
2. Keep the top rows per `company_domain`, up to the number the user agreed; remove the rest with reason `per_company_cap`.
3. Write `company_contact_order` 1, 2, 3 and so on.
4. Wave 1 file: every `company_contact_order = 1`. Wave 2 file: the later orders, loaded only after the company's first contact finishes the sequence with no reply.
5. When contact 1 replies, remove that company's wave 2 rows.

Why waves instead of one campaign with a delay: sequencers schedule each lead independently, so two people at one company in one campaign can receive the same step on the same morning, and Berman warns that emailing several people at a company at once can get the sender blocked company wide. Separate files keep the order under the user's control.

## 7. Personalization columns

| Level (Berman) | Column | Source | Fill rule |
|-|-|-|-|
| Segment | `industry`, `employee_band`, `city` | Lead Database fields | Always filled; drop rows missing a used column |
| Segment | `case_study` | Chosen by the user per segment (for example commercial vs residential) | Mapped from `keywords` or `industry` with a lookup table |
| Account | `trigger` | `account-researcher`, a signal list, a job posting | Only for tier 1 rows; blank elsewhere and the copy has a fallback |
| Person | `first_line` | The person's own post or talk, written by a human or reviewed | Only when sourced; never generated from guesses |

Column rules:

- Every column used in the copy is filled on every row, or the copy carries a fallback, or the rows go to a variant without that variable (Smartlead's import guide: a blank cell means the value does not appear in the email).
- No column holds an invented fact. A wrong fact in the first line costs the reply.
- Keep values short; they are pasted into sentences. "a 180-person commercial GC" works; a paragraph does not.

## 8. Output CSV columns (master file)

| Column | Example | Rule |
|-|-|-|
| `email` | dana.whitfield@ridgelinebuilders.example | Lowercased, valid |
| `first_name`, `last_name` | Dana, Whitfield | Normalized |
| `title` | Controller | As returned |
| `company_name` | Ridgeline Builders | As returned |
| `company_domain` | ridgelinebuilders.example | Registrable domain |
| `company_city`, `company_state` | Denver, CO | HQ |
| `industry`, `employee_band` | construction, 51-200 | From the database |
| `case_study`, `trigger`, `first_line` | per section 7 | Only sourced values |
| `email_status`, `email_validated_at` | valid, 2026-10-13 | Required |
| `company_contact_order` | 1 | 1 up to the agreed cap |
| `source`, `source_detail`, `pulled_at` | lead_db, lead_db:title=CFO...;emp=50-500, 2026-10-13 | Required |
| `segment`, `wave` | construction-finance-50-500, 1 | Campaign slice and wave |

The import file is a projection of this master file with headers renamed per `sequencer-import-specs.md`.

## 9. Failure handling

| Failure | Action |
|-|-|
| Count far below target | Widen per `icp-list-builder` (title synonyms, size band, neighboring states) and recount |
| Count far above target | Tighten (seniority, size, keywords) or take the first wave only |
| One source's `invalid` share far above the others | Stop using that source for this campaign; check its age and column mapping |
| Large catch-all share | Expect a large catch-all file; set its separate campaign volume or drop it |
| 402 mid-pipeline | Stop before validation; never import unvalidated rows |
| A personalization column blank on some rows | Fix the mapping or move those rows to a variant |
| QA sample shows the same miss repeating on one check | Fix the filter or mapping and re-pull; do not hand-patch rows |

## Sources

- ScraperCity MCP tool schemas and CLI source (`email-find --file` parsing): https://www.npmjs.com/package/scrapercity
- ScraperCity, How to use: https://scrapercity.com/how-to-use
- Alex Berman, Cold email templates (personalization levels): https://alexberman.com/cold-email-templates
- Alex Berman, Cold email follow-up guide (4 to 6 follow-ups over 2 to 3 weeks): https://alexberman.com/cold-email-follow-up
- Alex Berman, TAM strategy breakdown (inbox limits, 30 to 60 day cycles): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Lean B2B, Alex Berman on B2B market segments: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- Instantly, Account and campaign limits (30 campaign emails per account per day): https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Hunter, Email verification guide, email data decay (4 Nov 2025): https://hunter.io/email-verification-guide/email-data-decay
- Smartlead, How to map CSV columns (blank cells): https://helpcenter.smartlead.ai/en/articles/409-how-to-map-csv-columns-in-smartlead-campaigns
