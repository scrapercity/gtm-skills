---
name: crm-enricher
description: >-
  Fills missing emails, mobiles, job titles and company fields in a HubSpot,
  Pipedrive, GoHighLevel or Salesforce export using ScraperCity Lead Database
  lookups (by companyDomain, companyName or socialUrl), Email Finder, Mobile
  Finder and Website Finder. Applies a field-level fill precedence that never
  overwrites owner-entered data without a stated rule, scores every match,
  flags each unfillable field with a reason code, adds write-back audit columns
  and maps the file back to the CRM's import format. Use when the user says
  "enrich my CRM", "this export is half empty", "fill in missing emails and
  phones", "append titles and company size", or "update our HubSpot records".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [crm, enrichment, hubspot, pipedrive, gohighlevel, salesforce, data-quality, email-finder, mobile-finder]
  related_skills: [email-list-cleaner, mobile-appender, decision-maker-finder, icp-list-builder, cold-email-list, scrapercity-lead-database, scrapercity-integrations]
  frameworks:
    - "DAMA UK - six data quality dimensions (as adopted by the UK Government Data Quality Hub, 2021)"
    - "HubSpot, Pipedrive, HighLevel and Salesforce - import, dedupe and overwrite documentation"
    - "Salesforce - upsert by external ID (REST API)"
    - "EU GDPR - Article 5(1)(d) accuracy and Article 14 notice for data not obtained from the person"
    - "FCC - TCPA and 47 CFR 64.1200 for mobile numbers written back to a CRM"
    - "FTC - CAN-SPAM Act compliance guide"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, scrapercity-agent-patterns.md, outbound-compliance-primer.md]
---

# CRM Enricher

## Overview

This skill takes a CRM export with holes in it and returns three things: the same rows with gaps filled under written rules, a re-import file mapped to the user's CRM, and a report that accounts for every field it touched or could not fill.

The mistake it prevents is the "enrich everything, overwrite everything" import. A rep typed a direct dial and a nickname into a record last month; an enrichment job replaces both with a switchboard and a legal name, the import runs, and nobody can tell which values changed. This skill treats every CRM value as owner-entered until proven stale, writes found values to empty fields only unless a field rule says otherwise, keeps the prior value in an audit column whenever it does replace one, and refuses to auto-write a low-confidence match.

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
| Fields to fill, in priority order | Sets scope and cost | email, job title, company size, industry; mobiles only if asked |
| Scope for mobiles (stages, owners, target accounts) | Mobiles cost $0.25 each when found | Open opportunities and target accounts only |
| Who owns which fields | Decides overwrite policy | Every non-empty CRM value is owner-entered |
| Plan level | Lead Database needs Growth ($149/mo) or Scale | Run `check_wallet` and read `plan.name` |
| Suppression and do-not-contact flags | Rows that must not be enriched for outreach | Respect any opt-out, DND or unsubscribed field in the export |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| DAMA UK data quality dimensions (UK Government Data Quality Hub, 2021) | Accuracy, completeness, uniqueness, consistency, timeliness and validity. The report measures completeness before and after, validity (E.164, email status), and timeliness (`enriched_at`, validation date). |
| HubSpot import docs | Record ID overrides other identifiers; contacts match on email, companies on Company Domain Name; three modes (create and update, create only, update only); a per-property "Don't overwrite" checkbox. |
| Pipedrive import docs | People merge when name plus organization, phone or email matches; organizations merge on address; merge step can be bypassed. |
| HighLevel import docs | Update or Create and Update; matching order Contact ID, then email, then phone; a "Don't update Empty Values" checkbox. |
| Salesforce Data Import Wizard and Data Loader docs | Add, update, or add and update; match by Salesforce ID, name or email; account values are filled only when empty unless "Overwrite existing account values" is ticked; Data Loader's "Insert null values" blanks fields; REST upsert by external ID refuses multiple matches with HTTP 300. |
| GDPR Article 5(1)(d) and Article 14 | Personal data must be accurate and kept up to date; when you obtain data from someone other than the person, you tell them the source within a month or at first contact. |
| TCPA, 47 CFR 64.1200 | A mobile in the CRM is a wireless number; autodialed or prerecorded calls and texts need consent. The enricher tags `mobile` separately so downstream tools can gate it. |
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

Derive `company_domain` from the website field, or from the email when the email is not a freemail address (gmail.com, outlook.com, yahoo.com, icloud.com, hotmail.com, aol.com, proton.me). Normalize per `references/list-quality-standard.md` section 3. Do not merge duplicate CRM records; flag them `DUPLICATE_IN_CRM` and let the CRM's own merge tool handle them.

### 2. Write the field rule sheet

Every field gets a fill precedence and one overwrite policy from this vocabulary. Show the sheet to the user and get a yes before any paid step.

| Policy | Meaning |
|-|-|
| `fill_blank_only` | Write only when the CRM value is empty. Default for every field. |
| `replace_if_invalid` | Replace only when validation proves the current value bad (email `invalid`, phone fails E.164). Old value goes to `prior_<field>`. |
| `stage_for_review` | Never write to the CRM field; write to `enriched_<field>` for a human to accept. |
| `never_overwrite` | Owner, lifecycle stage, lead status, notes, consent and opt-out fields. Read only. |
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

Compute the expected cost and the ceiling (every paid lookup hits). Use the formulas in ScraperCity Implementation below. Run `check_wallet`. Over $5, show the table and wait for a go-ahead. Mobiles are the expensive line; scope them to the segment the user named.

### 5. Run lookups, cheapest first

Order: Lead Database (free on plan) by `socialUrl`, then by `companyDomain`, then by `companyName`; then `validate_emails` on existing emails that have no validation date in the last 30 days; then `find_emails` for remaining blanks and for emails that came back invalid; then `find_mobiles` for in-scope rows; then `scrape_website_finder` for account-only rows. The batch sizes, paging limits and REST loop are in `references/enrichment-runbook.md`.

### 6. Score each match and apply the rules

| Tier | Rule | Action |
|-|-|-|
| High | `socialUrl` exact match, or email exact match, or first + last + domain with exactly one candidate | Write per the field policy |
| Medium | Nickname or initial match plus domain (Bob vs Robert), or name + company name with one candidate and no domain | `stage_for_review` for every field |
| Low | Two or more candidates, last name only, or the company name differs | Do not write; flag `AMBIGUOUS_MATCH` |
| None | No candidate | Flag `NOT_FOUND` |

A High match whose Lead Database company differs from the CRM company is a job change. Do not overwrite the company. Flag `JOB_CHANGE`, put the new company and title in `enriched_company` and `enriched_title`, and list these rows separately: they are a re-engagement list and a reason to create a new contact at the old account.

### 7. Build the write-back file and the report

Write the CRM-ready file with the CRM's record ID as the first column, only the fields being updated, and the audit columns. Map column names with `references/crm-import-mapping.md`. Write every unfilled field's reason code to `enrich_flags`. Fill in `templates/output-template.md` and run `scripts/check-output.py` on it.

### 8. Test import, then full import

Import 10 rows in update-only mode, open 3 of them in the CRM, confirm nothing owner-entered changed and the audit columns landed. Then import the rest. Keep the untouched original export as the rollback file.

## ScraperCity Implementation

### Tools and prices (from `references/scrapercity-catalog.md`)

| Step | Tool | Price |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Person and company lookup | `query_lead_database` (`socialUrl`, `companyDomain`, `companyName`, `title`, `limit`, `after`) | Included on Growth and Scale; 100,000 new leads a day; records you already have are free to fetch again |
| Missing or invalid email | `find_emails` with `contacts[]` of `{first_name, last_name, domain}` or `company_name` | $0.05 per email found, free if not found |
| Mobile | `find_mobiles` with `inputs[]` (social URLs or emails) | $0.25 per number found, free if not found |
| Contact for an account-only record | `scrape_website_finder` with `domains[]`, `jobTitle` | $0.0499 per contact found |
| Existing emails | `validate_emails` with `emails[]` | $0.0072 per email |

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

A 2,400-contact HubSpot export (the full run is in `examples/worked-example.md`): the Lead Database filled 211 missing emails for free, which left 480 Email Finder lookups (blanks it could not fill plus invalid replacements); 1,978 emails to validate; 490 in-scope mobile lookups; 38 account-only domains the database could not cover.

| Line | Units | Unit price | Ceiling | Actual |
|-|-:|-:|-:|-:|
| `query_lead_database` lookups | 1,490 calls | Included | $0.00 | $0.00 |
| `validate_emails` (existing plus Lead Database emails) | 1,978 emails | $0.0072 | $14.24 | $14.24 |
| `find_emails` | 480 lookups, 290 found | $0.05 per found | $24.00 | $14.50 |
| `find_mobiles` | 490 inputs, 147 found | $0.25 per found | $122.50 | $36.75 |
| `scrape_website_finder` | 38 domains, 27 found | $0.0499 per found | $1.90 | $1.35 |
| `validate_emails` on new account contacts | 49 emails | $0.0072 | $0.35 | $0.35 |
| Total | | | $162.99 | $67.19 |

The ceiling is over $5, so the table goes to the user before any paid call. Mobiles are 75% of the ceiling; if the user balks, cut mobile scope first.

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
2. `crm-review-[crm]-[date].csv`: Medium matches, job changes and title conflicts with `enriched_*` columns for a human to accept or reject.
3. A report from `templates/output-template.md`: input profile, field rules, routing, cost, fill results, match confidence, write-back mapping, audit columns, unfilled flags, sample rows and next steps.

## Quality Check

- [ ] Every field in scope has a policy from the five-value vocabulary and the user approved the sheet.
- [ ] No owner-entered value changed unless its policy is `replace_if_invalid`, and every replaced value sits in `prior_<field>`.
- [ ] For each field: filled + staged + unfilled equals the number missing before.
- [ ] Match tiers sum to the lookups attempted; no Low or None match wrote anything.
- [ ] Every unfilled field carries a reason code in `enrich_flags`.
- [ ] Every mobile is E.164 and sits in the mobile field, never the main phone field.
- [ ] The write-back file has the CRM record ID in every row and imports in update-only mode.
- [ ] A 10-row test import was checked in the CRM before the full import.
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
| Sending LinkedIn URL and email for the same person to `find_mobiles` | Two hits on one person bill $0.50 | One input per person, URL preferred |
| Writing a found mobile into the main phone field | Dialers and texting tools cannot gate wireless numbers they cannot see | Separate `mobile` field, E.164 |
| Using freemail domains for `find_emails` | gmail.com is not the employer | Derive the domain from the website or company; else flag `FREEMAIL_DOMAIN` |
| Enriching records marked unsubscribed or DND | Filling contact data for someone who opted out invites a repeat contact | Skip; flag `SUPPRESSED` |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule, or which file to open next. |
| `references/field-precedence-and-overwrite-rules.md` | Writing the field rule sheet, resolving a conflict, scoring a match, handling job changes. |
| `references/crm-import-mapping.md` | Mapping columns and choosing import settings for HubSpot, Pipedrive, GoHighLevel or Salesforce. |
| `references/enrichment-runbook.md` | Routing rows, batch sizes, paging limits, the REST loop, pilot hit-rate method, reason codes. |
| `references/list-quality-standard.md` | Normalization, E.164, validation buckets (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database allowances (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling, safe retries (shared). |
| `references/outbound-compliance-primer.md` | Rules before the enriched records feed calls, texts or email (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished report for a 2,400-contact HubSpot export. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `email-list-cleaner` to validate a list without enriching it.
- `mobile-appender` when the job is a call list, with the TCPA and DNC gate.
- `decision-maker-finder` to add buyers at accounts with no contacts.
- `icp-list-builder` to build net-new lists in the same schema.
- `cold-email-list` to turn enriched records into a send-ready file.
- `scrapercity-lead-database` for every Lead Database filter.
- `scrapercity-integrations` for HubSpot, Pipedrive, GoHighLevel, Zapier and n8n hookups.
