---
name: crm-enricher
description: >-
  Fills missing emails, mobiles, job titles and company fields in a HubSpot,
  Pipedrive, GoHighLevel or Salesforce export using ScraperCity Lead Database
  lookups (by companyDomain, companyName or socialUrl), Email Finder, Mobile
  Finder and Website Finder, with one cost-ordered ladder per field and Tech
  Stack Search flags for technographics. Applies a field-level fill precedence
  that never overwrites owner-entered data without a stated rule, scores every
  match, flags each unfillable field with a reason code, adds write-back audit
  columns, maps the file back to the CRM's import format and sets a refresh
  schedule. Use when the user says
  "enrich my CRM", "this export is half empty", "fill in missing emails and
  phones", "append titles and company size", or "update our HubSpot records".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags:
    - crm
    - enrichment
    - hubspot
    - pipedrive
    - gohighlevel
    - salesforce
    - data-quality
    - email-finder
    - mobile-finder
  related_skills:
    - email-list-cleaner
    - mobile-appender
    - decision-maker-finder
    - icp-list-builder
    - cold-email-list
    - scrapercity-lead-database
    - scrapercity-integrations
  frameworks:
    - "DAMA UK - six data quality dimensions (as adopted by the UK Government Data Quality Hub, 2021)"
    - "HubSpot, Pipedrive, HighLevel and Salesforce - import, dedupe and overwrite documentation"
    - "Salesforce - upsert by external ID (REST API)"
    - "ZeroBounce - verification frequency FAQ and Email List Decay Report 2026"
    - "US Bureau of Labor Statistics - Employee Tenure (January 2026)"
    - "Alex Berman - keep bounces under 2%"
    - "Instantly - high bounce auto-pause, checked after 200 sends"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
    - scrapercity-agent-patterns.md
---

# CRM Enricher

## Overview

This skill takes a CRM export with holes in it and returns the same rows with gaps filled under written rules, an update file and a create file mapped to the user's CRM, and a report that accounts for every field it touched or could not fill and dates the next refresh.

The mistake it prevents is the "enrich everything, overwrite everything" import. A rep typed a direct dial and a nickname into a record last month; an enrichment job replaces both with a switchboard and a legal name, the import runs, and the team cannot tell which values changed. This skill treats every CRM value as owner-entered until proven stale, writes found values to empty fields only unless a field rule says otherwise, keeps the prior value in an audit column whenever it does replace one, and refuses to auto-write a low-confidence match.

It also prevents paying twice. The Lead Database lookup runs first because it is included on Growth and Scale plans; Email Finder ($0.05 per email found) and Mobile Finder ($0.25 per number found) run only on the rows the database could not fill.

## When to Use

- "Here's our HubSpot export, 40% of contacts have no email. Fill what you can."
- "Append job titles and company size to these Pipedrive people."
- "Add mobiles for our open opportunities before the call blitz."
- "Our Salesforce leads are stale. Which ones changed jobs?"
- "Clean up this GoHighLevel import before we load it."

Use a different skill when:

| The user wants | Use |
|-|-|
| Only to validate the emails already in a list | `email-list-cleaner` |
| Only mobiles for a call list (no CRM write-back) | `mobile-appender` |
| New contacts at accounts that have none, by buying role | `decision-maker-finder` |
| A brand-new list from an ICP | `icp-list-builder` |
| A send-ready cold email file from these records | `cold-email-list` |
| Lead Database parameters in depth | `scrapercity-lead-database` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| CRM name and object (contacts, leads, people, companies) | Picks the import identifier and column map | Ask |
| The export CSV with the CRM record ID column | Updates must match on ID, not on name | Ask for a re-export that includes the ID |
| Fields to fill, in priority order | Sets scope and cost | email, job title, seniority, department, company size, industry; mobiles only if asked |
| Scope for mobiles: accounts or stages, plus the seniority levels and departments reps will dial | Mobiles cost $0.25 each when found; every number bought for someone reps will not call is wasted | Ask. The seniority and department filter runs on the Lead Database's refreshed `seniority` and `department` values, so mobiles run after the title refresh |
| Value of one email and one mobile to the user | Decides whether a lower-yield pass (Email Finder retry, Website Finder) is worth running | Ask; a pass stays only when its cost per usable result is at or under this value |
| Who owns which fields | Decides overwrite policy | Every non-empty CRM value is owner-entered |
| Plan level | Lead Database needs Growth ($149/mo) or Scale | Run `check_wallet` and read `plan.name` |
| Suppression flags | Rows that skip every paid lookup | Any opt-out, DND or unsubscribed field in the export marks the row suppressed |
| Freshness windows for titles and company size | A CRM value older than the window can be staged for replacement | Ask; until set, every differing value is staged |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| DAMA UK data quality dimensions (UK Government Data Quality Hub, 2021) | Accuracy, completeness, uniqueness, consistency, timeliness and validity. The report measures completeness before and after, validity (E.164, email status), and timeliness (`enriched_at`, validation date). |
| HubSpot import docs | Record ID overrides other identifiers; contacts match on email, companies on Company Domain Name; three modes (create and update, create only, update only); a per-property "Don't overwrite" checkbox. |
| Pipedrive import docs | People merge when name plus organization, phone or email matches; organizations merge on address; merge step can be bypassed. |
| HighLevel import docs | Update or Create and Update; matching order Contact ID, then email, then phone; a "Don't update Empty Values" checkbox. |
| Salesforce Data Import Wizard and Data Loader docs | Add, update, or add and update; match by Salesforce ID, name or email; account values are filled only when empty unless "Overwrite existing account values" is ticked; Data Loader's "Insert null values" blanks fields; REST upsert by external ID refuses multiple matches with HTTP 300. |
| ZeroBounce verification FAQ | Verify an email list at least once per quarter; the send gate and the refresh schedule use 90 days. |
| BLS Employee Tenure (January 2026) and ZeroBounce Email List Decay Report 2026 | Median tenure 4.1 years and at least 23% of an email list decaying in a year bracket a planning decay of 1.3% to 2.3% a month. |
| Alex Berman (alexberman.com, cold email templates) and Instantly's bounce auto-pause help page | Keep bounces under 2% (Berman); Instantly runs its bounce check once a campaign has sent 200 emails. Together they set when the catch-all lane opens and when it stops. |
| `references/list-quality-standard.md` | Column names, E.164, domain normalization, dedupe keys, validation buckets. |

Details and the routing table for this skill's files: `references/framework-notes.md`.

## Workflow

### 1. Profile the export

Read the header and count, per field: present, blank, malformed. Also count the identifiers each row carries, because they decide which tool can fill it:

| Identifier inventory | Count it as |
|-|-|
| Valid-looking work email | `has_email` |
| LinkedIn or other social profile URL | `has_social` |
| First name + last name + company domain | `has_name_domain` |
| First name + last name + company name, no domain | `has_name_company` |
| Company domain only, no person | `account_only` |
| None of the above | `no_identifier` |

Derive `company_domain` from the website field, or from the email when the email is not a freemail address (gmail.com, outlook.com, yahoo.com, icloud.com, hotmail.com, aol.com, proton.me). Normalize per `references/list-quality-standard.md` section 3. Do not merge duplicate CRM records; flag them `DUPLICATE_IN_CRM` and let the CRM's own merge tool handle them. Skip test and placeholder records (`JUNK_RECORD`) and the user's own employees (`INTERNAL_RECORD`) before counting gaps, so fill rates describe prospects only.

### 2. Write the field rule sheet

Every field gets a fill precedence, one overwrite policy from this vocabulary, and the segments allowed into each paid step (that list is the per-row spend cap). Show the sheet to the user and get a yes before any paid step.

| Policy | Meaning |
|-|-|
| `fill_blank_only` | Write only when the CRM value is empty. Default for every field. |
| `replace_if_invalid` | Replace only when validation proves the current value bad (email `invalid`, phone fails E.164). Old value goes to `prior_<field>`. |
| `stage_for_review` | Never write to the CRM field; write to `enriched_<field>` for a human to accept. |
| `never_overwrite` | Owner, lifecycle stage, lead status, notes, subscription status and opt-out fields. Read only. |
| `append_new` | Add as an additional value (second phone, secondary email) without touching the primary. |

Default precedence per field, and the full conflict matrix, are in `references/field-precedence-and-overwrite-rules.md`.

### 3. Route each row by its strongest identifier

| Row has | First call (included in plan) | Paid fallback for the gap |
|-|-|-|
| Social URL | `query_lead_database` with `socialUrl` | `find_mobiles` with the URL for a mobile; `find_emails` once the domain is known |
| First + last + domain | `query_lead_database` with `companyDomain`, match the name locally | `find_emails` with `{first_name, last_name, domain}` |
| First + last + company name | `query_lead_database` with `companyName`, read the company website to get a domain | `find_emails` with `{first_name, last_name, company_name}` (domain preferred when you have it) |
| Work email only | `query_lead_database` with `companyDomain` from the email, match on email | `find_mobiles` with the email |
| Company domain, no person | `query_lead_database` with `companyDomain` and a `title` for the buyer | `scrape_website_finder` with `domains` and `jobTitle` |
| Nothing usable | None | Flag `NO_IDENTIFIER` |

### 4. Count, estimate, confirm

Compute the expected cost and the ceiling (every paid lookup hits). Use the formulas in ScraperCity Implementation below. Run `check_wallet`. Show the table and wait for a go-ahead. Mobiles are the expensive line: count them only for people in the accounts or stages the user named and at the seniority levels and departments reps will dial, read from the Lead Database's `seniority` and `department` on the refreshed record. Contacts with no high match have no refreshed seniority, so they stay out of mobile scope unless the CRM title already names a buyer role the user listed.

### 5. Run lookups, cheapest first

Each field family runs its own ladder and a row leaves it at the first step that meets the stop condition, so no row pays twice for one field. Order: Lead Database (included on Growth and Scale) by `socialUrl`, then by `companyDomain`, then by `companyName`; then `validate_emails` on existing emails that have no validation date in the last 90 days; then `find_emails` for remaining blanks and for emails that came back invalid; then `find_mobiles` with LinkedIn URLs for in-scope rows, and a second run with the work email for the URL misses only; then `scrape_website_finder` for account-only rows. Email Finder, Mobile Finder and Website Finder bill only when they find something, so the price per hit is the list price at any hit rate; order is set by price per usable result after validation (`references/waterfall-and-cost-control.md`). The batch sizes, paging limits and REST loop are in `references/enrichment-runbook.md`. A call that fails is `LOOKUP_ERROR` in the retry file, never `NOT_FOUND`.

Two passes widen email coverage at no cost on a miss. First, Email Finder misses get one retry with a different input: `company_name` in place of a domain that came from the website field (the mail domain can differ from the web domain), and `full_name` for names that did not split. Only misses enter, so one person bills at most once; give the retry its own cost line. Second, when every validated address on a domain returns no mail exchanger (`sc_mx_record` empty), flag the domain `DOMAIN_NO_MAIL`, skip Email Finder there, and look the company up by `companyName` in the Lead Database: a different current domain means the company moved or was acquired, and its contacts rerun on the new domain.

### 6. Score each match and apply the rules

| Tier | Rule | Action |
|-|-|-|
| High | `socialUrl` exact match, or email exact match, or first + last + domain with exactly one candidate | Write per the field policy |
| Medium | Nickname or initial match plus domain (Bob vs Robert), or name + company name with one candidate and no domain | `stage_for_review` for every field |
| Low | Two or more candidates, last name only, or the company name differs | Do not write; flag `AMBIGUOUS_MATCH` |
| None | No candidate | Flag `NOT_FOUND` |

Company size is compared by band (1-10, 11-50, 51-200, 201-500, 501-1,000, 1,001-5,000, 5,001+): same band keeps the CRM value, a different band is staged as `SIZE_BAND_CHANGE`; the user's freshness window decides whether an older CRM value is replaced after review.

A High match whose Lead Database company differs from the CRM company is a job change. Do not overwrite the company. Flag `JOB_CHANGE`, put the new company and title in `enriched_company` and `enriched_title`, and keep the old record out of sends at the old address. Then do two things: create the person at the new company (email from the Lead Database match, validated, or from Email Finder) and put every one who validates into the main campaign as its own "new role" segment, so the copy can name the move; and find a replacement at the old account from the Lead Database people at that domain with the departed person's title.

High matches also fill `seniority` and `department` when the CRM has them blank. Write them as properties so the campaign can be segmented by them and the mobile scope can be filtered on them.

### 7. Build the update and create files

Write the CRM-ready file with the CRM's record ID as the first column, only the fields being updated, and the audit columns. New contacts (job changes at the new company, buyers at account-only companies) go in a separate create file, deduped against the full CRM export on email, LinkedIn URL, then name plus domain (`references/api-pipeline-and-sync.md` section 6). Map column names with `references/crm-import-mapping.md`. Write every unfilled field's reason code to `enrich_flags`.

### 8. Test import, then full import

Import 10 rows in update-only mode, open 3 of them in the CRM, confirm nothing owner-entered changed and the audit columns are filled. Then import the rest. Keep the untouched original export as the rollback file.

### 9. Set the refresh schedule and the send gate

Contact data decays at roughly 1.3% to 2.3% of a list a month (planning range from BLS tenure data and the ZeroBounce 2026 decay report; measure your own). Schedule by segment: validation before any send when the last check is older than 90 days (ZeroBounce: verify at least once per quarter), a job-change sweep for open opportunities and customer champions, a title and company refresh for active accounts on the cadence the user sets, nothing paid for the rest until they enter a sequence. Build the send-gate view (valid email, validated within 90 days, no opt-out or `JOB_CHANGE` flag) as the only source for sequence enrollment. Catch-all addresses go to a separate lane that opens once the main campaign's first 200 sends bounce under 2% and pauses past 2% (Berman's bounce line; Instantly checks bounces after 200 sends). Dates, owners and costs go in the report's Refresh Schedule; the view definitions per CRM are in `references/api-pipeline-and-sync.md` sections 8 and 10. Then fill in `templates/output-template.md` and run `scripts/check-output.py` on it.

## ScraperCity Implementation

### Tools and prices (from `references/scrapercity-catalog.md`)

| Step | Tool | Price |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Person and company lookup | `query_lead_database` (`socialUrl`, `companyDomain`, `companyName`, `title`, `limit`, `after`) | Included on Growth and Scale; 100,000 new leads a day; records you already have are free to fetch again |
| Missing or invalid email | `find_emails` with `contacts[]` of `{first_name, last_name, domain}` or `company_name` | $0.05 per email found, free if not found |
| Mobile | `find_mobiles` with `inputs[]` (social URLs or emails) | $0.25 per number found, free if not found |
| Contact for an account-only record | `scrape_website_finder` with `domains[]`, `jobTitle` | $0.0499 per contact found |
| Existing emails, and company fields on Starter (the validator returns company name, industry, size, founded and location per domain) | `validate_emails` with `emails[]` | $0.0072 per email |
| Technographic flags | `scrape_builtwith` (Tech Stack Search), one run per technology, joined on domain | $4.99 per technology, whatever the CRM size |

### Calls

```json
{"tool": "query_lead_database", "args": {"socialUrl": "https://www.linkedin.com/in/dana-okafor", "limit": 5}}
{"tool": "query_lead_database", "args": {"companyDomain": "ledgerline.example", "limit": 100, "after": "0"}}
{"tool": "query_lead_database", "args": {"companyDomain": "ledgerline.example", "limit": 1}}
{"tool": "query_lead_database", "args": {"companyName": "Ledgerline", "limit": 25}}
{"tool": "find_emails", "args": {"contacts": [{"first_name": "Dana", "last_name": "Okafor", "domain": "ledgerline.example"}]}}
{"tool": "find_mobiles", "args": {"inputs": ["https://www.linkedin.com/in/dana-okafor", "sam.reyes@quotientlabs.example"]}}
{"tool": "scrape_website_finder", "args": {"domains": ["brightpathhr.example", "shipwise.example"], "jobTitle": "Head of People"}}
{"tool": "validate_emails", "args": {"emails": ["dana@ledgerline.example"]}}
```

The `limit: 1` company call is enough to read company fields (industry, size, revenue, HQ) for a domain. The `limit: 100` call lists people at the domain so you can match first and last name locally; the Lead Database has no name filter. Page with `after` only while the person is not yet found, and stop at 5 pages for one domain (large companies go to `find_emails` instead). `companyDomain` accepts several domains comma separated, but the 100 rows per call are then shared across them. Batch domains only when each company is small (under about 20 people), and send one domain per call otherwise.

Leave `autoValidateEmails` and `autoFindMobiles` off on `scrape_website_finder`. The catalog does not list a price for those flags; running `validate_emails` and `find_mobiles` separately keeps every charge at a known catalog price.

REST for loops over hundreds of domains: `GET https://app.scrapercity.com/api/v1/database/leads?companyDomain=ledgerline.example&limit=100&after=0` with `Authorization: Bearer $SCRAPERCITY_API_KEY`; scrapers are `POST /api/v1/scrape/email-finder`, `/mobile-finder`, `/website-finder`, `/email-validator`, then `GET /api/v1/scrape/status/{runId}` and `GET /api/downloads/{runId}`.

### Cost formulas

```text
find_emails     expected = lookups x expected hit rate x $0.05     ceiling = lookups x $0.05
find_mobiles    expected = inputs x expected hit rate x $0.25      ceiling = inputs x $0.25
website_finder  ceiling  = domains x $0.0499 (one contact per domain per title)
validate_emails exact    = unique emails x $0.0072
Lead Database   $0 on Growth and Scale (counts against 100,000 new leads a day)
```

Hit rates depend on the list. Use the pilot method from `references/enrichment-runbook.md`: run 50 rows, measure, then extrapolate. Show both the expected cost and the ceiling.

### Worked cost estimate

A 2,400-contact HubSpot export (the full run is in `examples/worked-example.md`): the Lead Database filled 211 missing emails for free, which left 479 first-pass Email Finder lookups (blanks it could not fill, invalid replacements, job changers) and a 120-row company-name retry; 2,112 emails to validate; 290 mobile inputs once the scope was cut to Director and above in Finance, HR and People on open deals; 38 account-only domains the database could not cover.

| Line | Units | Unit price | Actual | Ceiling |
|-|-:|-:|-:|-:|
| `query_lead_database` lookups | 2,162 calls | Included | $0.00 | $0.00 |
| `validate_emails` (existing, Lead Database, retries, new contacts) | 2,112 emails | $0.0072 | $15.21 | $15.21 |
| `find_emails` pass 1 | 479 lookups, 292 found | $0.05 per found | $14.60 | $23.95 |
| `find_emails` pass 2, company-name retry | 120 lookups, 18 found | $0.05 per found | $0.90 | $6.00 |
| `find_mobiles` pass 1 | 290 inputs, 87 found | $0.25 per found | $21.75 | $72.50 |
| `find_mobiles` pass 2, URL misses with an email | 95 inputs, 12 found | $0.25 per found | $3.00 | $0.00 extra |
| `scrape_website_finder` | 38 domains, 27 found | $0.0499 per found | $1.35 | $1.90 |
| Total | | | $56.81 | $119.56 |

The table goes to the user before any paid call. Mobiles are 61% of the ceiling; if the user balks, narrow the seniority or department list first. In the report, these lines carry product names (Lead Database, Email Validator, Email Finder, Mobile Finder, Website Finder), never the tool ids.

Plan choice: Growth's $159 of monthly credits exceed its $149 price, so once a month's paid tool use reaches $159 the Lead Database comes at no extra cost over Starter. Below that, the $100 difference pays for itself when the database fills 2,000 or more emails a month that would otherwise go to Email Finder at $0.05. Funding, hiring, intent and SIC or NAICS codes are not in the catalog; flag them `OUT_OF_CATALOG` rather than filling them.

### Build vs buy: how to run recurring enrichment

ScraperCity prices are the same in every mode; what changes is who runs the job and what breaks. Two inputs pick the mode: whether one person can review every staged row each month, and whether enrichment must run when a record is created. Count the records that need enrichment each month; total CRM size does not set the mode.

| Situation | Run it as | Write-back | Choose it when |
|-|-|-|-|
| One person can review every staged row each month | Buy as-is: dashboard runs at app.scrapercity.com with CSV download, or MCP tool calls in an agent session | CRM CSV import in update-only mode | No code to maintain |
| Batches outgrow one reviewer, but a scheduled batch is fast enough | Light build: CLI or a REST script on cron, or an n8n workflow | CSV import, or the CRM's API from the same workflow | Large batches belong in REST (`references/enrichment-runbook.md` section 3) |
| Enrichment must run when a record is created, or volume rules out a person in the loop | Build API-first: CRM webhook to n8n or your own service, REST lookups, CRM API update with audit columns | CRM API, field by field, with `prior_<field>` written first | Needs retry, logging, an owner for failures and the overwrite rules in code |

Limits that shape the API-first build: scrapercity.com/api-docs lists 100 API requests a minute per key and 10 concurrent scrapes, so 20,000 Lead Database lookups take at least 200 minutes at full speed. The Lead Database adds at most 100,000 new leads a day to the account; spread larger backfills across days. Stay with the cheaper mode until the review queue (`stage_for_review` rows) is the bottleneck, since an automated write-back cannot accept or reject a staged title.

### Errors

| Code | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, offer to drop mobile scope. |
| 403 on a database call | Plan lacks the Lead Database. Skip to the paid finders and say so in the report. |
| 409 | Same batch submitted moments ago; reuse the earlier `runId` from `list_runs`. |
| 429 | Wait 30 seconds, retry once. |
| 503 on a database call | Narrow: one domain per call, `limit` 25. |

## Output Format

1. `crm-writeback-[crm]-[date].csv`: record ID first, only fields being written, audit columns, ready for update-only import.
2. `crm-review-[crm]-[date].csv`: Medium matches, job changes, title conflicts and size-band changes with `enriched_*` columns for a human to accept or reject.
3. `crm-create-[crm]-[date].csv` when new contacts were found: deduped against the full export, for a create-only import.
4. A report from `templates/output-template.md`, written for the team that will run it. Sections, in this order:

| Section | What it holds |
|-|-|
| Status line, under the title | One line: run completed with actual counts, or a plan whose counts are planning estimates until the export is profiled. The only place "not run" or "projected" appears. |
| Summary | Answer first: what happens; the fields the user will have after the run, requested fields first and new properties marked; campaign-ready emails (catch-all counted apart); cost as expected, ceiling, cash out of pocket, cost per campaign-ready email and per dial-ready mobile; time; approvals needed with a date. |
| Decisions Needed (plan only) | Decision, default, due date. Leave out after a run. |
| Input Profile | Counts only. The mobile scope row names the accounts or stages, seniority levels and departments. |
| Field Rules | Field, precedence, policy, then one line: `Approval: name or role, YYYY-MM-DD` (a due date when not yet approved). |
| Routing Plan | Gap, identifier class, rows, first step, paid fallback, in product names; then one sentence: `Match tiers: high N, medium N, low N, none N, of T attempted.` |
| Cost Estimate | Line, units, unit price, Expected (Actual after a run), Ceiling, Total; then the pilot line and the plan line, once each. |
| Fill Results | Every field except email: missing before, filled, staged, unfilled, source. |
| Email Position After the Run | The only email table: groups before and after, then one sentence on where the valid count came from. |
| Write-back Mapping | Import settings per column; the audit columns listed in one row. |
| Unfilled Flags | At most 8 codes that need a person to act. Plain misses (`NOT_FOUND`), suppressed rows and retries are already in Fill Results; one "Not checked:" line for fields no tool supplies. |
| How to Run It | What the team runs: the Lead Database script (the compact version in `references/api-pipeline-and-sync.md` section 5) with the endpoint and `Authorization: Bearer` header, and the `npx scrapercity` commands for the paid steps with their file formats. |
| Refresh Schedule | Segment, check, date, cadence, owner, cost. Every decay, bounce or validation-age number names its source on the same line (BLS, ZeroBounce, Berman, Instantly) or says the user set it or the pilot measured it. |
| Next Steps | Numbered, each with a date, an owner and the action. Downstream checks are written out, never handed to another skill by name: for mobiles, hold numbers found on two or more contacts, drop numbers already in a phone field, remove anyone on the suppression list, and keep only carrier-confirmed mobiles when a power dialer will dial them; for email, enroll only from the send-gate view. |

Small jobs (25 records or fewer, or a single "find this person's email"): skip the report. Return one table with record, field, value found or `NOT_FOUND`, source, confidence and email status, then one line with the cost and one line with what to do next.

- Each fact appears once. The email outcome lives in Email Position only; the field list lives in Summary only; the audit columns live in one Write-back Mapping row.
- Never in the report: tool ids (`check_wallet`, `query_lead_database`, `find_emails` and the rest), JSON tool calls, run IDs or wallet asides, skill names, file paths, sample-row tables, match-confidence tables, audit-column tables, framework lists, self-grading checklists, and sections the user did not ask for.

## Quality Check

- [ ] Every field in scope has a policy from the five-value vocabulary and the user approved the sheet.
- [ ] No owner-entered value changed unless its policy is `replace_if_invalid`, and every replaced value sits in `prior_<field>`.
- [ ] For each field: filled + staged + unfilled equals the number missing before.
- [ ] Match tiers sum to the lookups attempted; no Low or None match wrote anything.
- [ ] Every unfilled field carries a reason code in `enrich_flags`.
- [ ] Every mobile is E.164 and sits in the mobile field, never the main phone field.
- [ ] The write-back file has the CRM record ID in every row and imports in update-only mode.
- [ ] A 10-row test import was checked in the CRM before the full import.
- [ ] New contacts sit in a separate create file with 0 matches against the full CRM export.
- [ ] No failed call is counted as `NOT_FOUND`; failures are `LOOKUP_ERROR` rows in the retry file.
- [ ] The Refresh Schedule gives each segment a date, an owner and a cost, and names the send-gate view.
- [ ] Mobiles were bought only for the accounts, seniority levels and departments the user named.
- [ ] Job changers with a valid email at the new company sit in the main campaign as a "new role" segment.
- [ ] Every decay, bounce or validation-age number in the report names its source on the same line.
- [ ] The Summary lists the fields after the run; every Next Step has a date and an owner.
- [ ] `check_wallet` ran and any paid step over $5 had a go-ahead.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Importing in create-and-update mode keyed on email | Rows whose email was blank create duplicate contacts | Update-only, keyed on the CRM record ID |
| Blank cells in the write-back file for fields you did not fill | HighLevel and Data Loader (with "Insert null values") can blank existing values | Drop untouched columns; tick "Don't update Empty Values"; keep "Insert null values" off |
| Overwriting a rep's title with the database title | Reps often store the title the buyer uses, and database titles lag | `stage_for_review` for titles that differ |
| Treating a different company in the Lead Database as a typo | It is usually a job change | Flag `JOB_CHANGE`, keep the CRM company, list for re-engagement |
| Running `find_emails` before the Lead Database | Paying $0.05 for emails the plan already includes | Database first, finders for the gap |
| Sending LinkedIn URL and email for the same person to `find_mobiles` in one run | Two hits on one person bill $0.50 | URL in the first run; email in a second run for URL misses only |
| Writing a found mobile into the main phone field | Dialers and texting tools cannot gate wireless numbers they cannot see | Separate `mobile` field, E.164 |
| Using freemail domains for `find_emails` | A gmail.com address names no employer, so the lookup searches the wrong company | Derive the domain from the website or company; else flag `FREEMAIL_DOMAIN` |
| Enriching records marked unsubscribed or DND | Paid lookups on rows that can never be contacted; a refilled email can slip back into a sequence and draw a spam complaint | Skip; flag `SUPPRESSED` |
| Counting a 429 or a failed run as "not found" | The row waits for the next scheduled refresh when it needed a retry tomorrow, and fill rates look worse than they are | `LOOKUP_ERROR`, retry file, next run |
| New contacts in the update file, or imported without a dedupe against the full CRM | Update-only mode drops them; create mode without a dedupe duplicates existing people | Separate create file, deduped on email, LinkedIn URL, then name plus domain |
| The sequencer's CRM sync and the enrichment job both writing title or email | Each sync overwrites the other | One writer per field group; switch the sequencer mapping off or to fill-blank-only |
| Averaging two employee counts | Produces a number neither source reported and can move the account across a routing band | Compare by size band; stage a band change |
| Buying mobiles for every contact at a target account | Money goes on numbers for people reps will not call | Filter on refreshed seniority and department to the buyers the user names |
| Parking job changers in a separate file | Validated people at their new company never get a send | Create them and enroll the valid ones as a "new role" segment of the main campaign |
| Tool ids, JSON calls or skill names in the report | The team cannot run an agent tool call or a skill name | Product names, the script and `npx scrapercity` commands, and the checks written out |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule, or which file to open next. |
| `references/field-precedence-and-overwrite-rules.md` | Writing the field rule sheet, resolving a conflict, scoring a match, handling job changes. |
| `references/crm-import-mapping.md` | Mapping columns and choosing import settings for HubSpot, Pipedrive, GoHighLevel or Salesforce. |
| `references/enrichment-runbook.md` | Routing rows, batch sizes, paging limits, MCP versus REST, the REST loop, pilot hit-rate method, reason codes. Pair section 3 with the build-vs-buy table above. |
| `references/waterfall-and-cost-control.md` | Ordering lookups by price per usable result, the ladder per field family, per-row and monthly caps, the step contribution review, plan choice by volume, Tech Stack Search flags, email lookup details. |
| `references/api-pipeline-and-sync.md` | Event triggers, sync versus async calls, safe re-runs, error states, the reference lookup script and its compact version for the report's How to Run It, create-file dedupe, one writer per field, send-gate view, monitoring, refresh schedule and decay figures. |
| `references/list-quality-standard.md` | Normalization, E.164, validation buckets (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database allowances (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling, safe retries (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished report for a 2,400-contact HubSpot export, in the report format above. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `email-list-cleaner` to validate a list without enriching it.
- `mobile-appender` when the job is a call list, with line-type, shared-number and suppression checks.
- `decision-maker-finder` to add buyers at accounts with no contacts.
- `icp-list-builder` to build net-new lists in the same schema.
- `cold-email-list` to turn enriched records into a send-ready file.
- `scrapercity-lead-database` for every Lead Database filter.
- `scrapercity-integrations` for HubSpot, Pipedrive, GoHighLevel, Zapier and n8n hookups.
