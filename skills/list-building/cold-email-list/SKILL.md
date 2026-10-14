---
name: cold-email-list
description: >-
  Takes target domains or an ICP and produces a send-ready CSV for a cold
  email sequencer. Finds the right people (Lead Database by domain or ICP
  filters, Website Finder for empty accounts), fills missing emails with
  Email Finder, dedupes, suppresses, validates every address, caps contacts
  per company, adds personalization columns, sizes the list to mailbox
  capacity, and formats headers for Instantly, Smartlead, Lemlist or
  EmailBison. Use when the user says "build a cold email list", "get this
  ready for Instantly", "turn these domains into a campaign", or "I need
  1,000 verified leads to send next week".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags:
    - cold-email
    - send-ready
    - sequencer-import
    - email-validation
    - lead-database
    - email-finder
  related_skills:
    - icp-list-builder
    - decision-maker-finder
    - email-list-cleaner
    - local-business-list
    - cold-email-strategy
    - cold-email-copywriting
    - sending-platforms
    - email-deliverability
  frameworks:
    - "Alex Berman - 30/30/50: targeting, offer, deliverability"
    - "Google, Yahoo and Microsoft - bulk sender requirements (2024-2025)"
    - "Hunter - Email verification guide, email data decay (Nov 2025)"
    - "Instantly, Smartlead and Lemlist - CSV import requirements"
    - "M3AAWG - Sender Best Common Practices"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
    - list-quality-standard.md
    - deliverability-primer.md
    - alex-berman-cold-email.md
---

# Cold Email List

## Overview

This skill delivers the file a sequencer imports on launch day: one row per prospect, every email `valid` and validated within four weeks of its send date, duplicates and suppressed contacts removed, no more people per company than the user agreed, personalization columns filled or deliberately blank, headers that the chosen platform accepts, and a row count that the user's mailboxes can send on schedule. A separate catch-all file and a short report come with it.

The mistake it prevents is the half-finished list: a database export pasted into Instantly with unvalidated emails, five people from one company in the same campaign, a `{{first_name}}` column that is blank on some rows, and 4,000 prospects for three mailboxes. Each of those costs bounces or a week. Alex Berman splits cold email results into 30% targeting, 30% offer and 50% deliverability; this skill covers the targeting share and protects the deliverability share before the first send.

## When to Use

- "Build me a cold email list for this campaign."
- "Here are 400 domains, get the right people and make it ready for Smartlead."
- "I need 1,500 verified CFOs at construction companies for Instantly."
- "Take this ICP list and make it send-ready."
- A campaign plan from `cold-email-strategy` exists and needs its file.

Use a different skill when:

| The user wants | Use |
|-|-|
| Only the ICP definition and a validated contact pull, no sequencer prep | `icp-list-builder` |
| Buying committees at named accounts, with mobiles | `decision-maker-finder` |
| An existing list cleaned, no new sourcing | `email-list-cleaner` |
| Local businesses by category and city | `local-business-list`, then this skill for import prep |
| The campaign plan, offer or sequence | `cold-email-strategy` |
| Sequencer setup, warmup or sending limits | `sending-platforms`, `email-deliverability` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Domains, an ICP, or a people-search URL | Picks the sourcing path | Ask |
| Offer and segment in one line each | Decides titles and personalization columns | Ask; see `cold-email-strategy` |
| Sequencer (Instantly, Smartlead, Lemlist, EmailBison) | Header rules differ | Instantly |
| Mailboxes, sends per mailbox per day, sequence steps | Sizes the list | Sends per mailbox: 30 (Instantly's recommendation for campaign emails); mailboxes and steps: ask |
| Launch date | Rows validated more than four weeks before their send date get re-validated | Ask |
| Suppression: customers, open deals, past sends, unsubscribes, bounces | Must run before validation | Ask for CRM and sequencer exports |
| Re-contact window | People contacted inside it are suppressed | Ask; Berman's cycle model restarts every 30 to 60 days |
| Recipient countries | Time zone of the send window | United States |

## Authoritative Foundations

| Source | What it contributes |
|-|-|
| Alex Berman (alexberman.com, Lean B2B interview) | 30/30/50 targeting, offer, deliverability. Build the list after the offer. Test about 100 emails per segment before scaling. Verify every email and keep bounces under 2%. Under 50 emails per inbox per day. Do not email several people at one company at once. |
| Google, Yahoo, Microsoft sender requirements (Feb 2024, May 2025) | Remove invalid recipients, keep complaints under 0.3% (Google targets under 0.1%), authenticate every sending domain. The list is the input those numbers depend on. |
| Hunter, Email verification guide (4 Nov 2025) | Verify shortly before the campaign; in Hunter's test, over 2% of a list went invalid within four weeks and 5.5% within eight. Sets the four-week re-validation rule against Berman's 2% bounce line. |
| Instantly, Smartlead and Lemlist docs | Email is the required column; Instantly asks for unique UTF-8 headers of 20 characters or fewer, caps an upload at 50 variables, recommends 30 campaign emails per account per day, and pauses a campaign at 5% bounces once it has sent 200; Smartlead allows up to 40 custom variables per lead; Lemlist auto-maps `firstname`, `lastname`, `companyName` and similar names. |
| M3AAWG Sender Best Common Practices | Suppress repeat bouncers and treat lists not mailed for a year as dirty. |
| `references/list-quality-standard.md` and `references/deliverability-primer.md` | Columns, dedupe keys, validation buckets. |

Details: `references/framework-notes.md`.

## Workflow

### 1. Write the campaign brief

One table: offer, segment, sequencer, mailboxes, sends per mailbox per day, steps, launch date, personalization variables the copy will use, countries. Every later number comes from it.

### 2. Size the list from capacity

```text
daily_sends     = mailboxes x sends_per_mailbox_per_day          (Instantly recommends 30; Berman: under 50)
total_sends     = send_ready_rows x steps
sending_days    = ceil(total_sends / daily_sends)
rows_for_N_days = daily_sends x N / steps
pull_rows       = target_send_ready / yield, rounded up to the next 100
```

`yield` is send-ready rows divided by rows pulled on the user's last list for this segment; with no history, pull a first wave and measure it. Six mailboxes at 30 a day send 180 emails a day; with 3 steps that is 60 new prospects a day, or about 1,200 for a 20-day campaign. A list much larger than the campaign window ages past four weeks before it is sent; build it in waves.

### 3. Pick the sourcing path and count

| Input | Path | Count call |
|-|-|-|
| Target domains | `query_lead_database` with `companyDomain` batches (halve on a 503) plus the role `title`, `seniority`, `notTitle` | `limit: 1` per batch |
| An ICP | `query_lead_database` with title, industry or keywords, size, location, `hasEmail: true` | `limit: 1`, read `pagination.total` |
| A people-search URL (Apollo.io and similar) | `query_lead_database` with `url`; read `search_translation` | `limit: 1` |
| The URL needs filters the database cannot apply | `scrape_apollo` with `url` and `count` (500 to 50,000), webhook registered | The start response may report `lead_database.matches` |
| Local businesses | Build with `local-business-list`, then continue at step 6 | Per that skill |

Show the count, the planned pull and the cost estimate. Call `check_wallet`. Wait for a go-ahead before any paid step.

### 4. Pull with cursor paging

Page with `after: "0"`, `limit: 100`, then `pagination.next_after` until null or the planned rows. Add `excludeDelivered: true` when the account has pulled this ICP before and only new people are wanted. For domain lists, rank people per domain and keep the best by role, up to the contacts per company the user agreed (role ranking in `decision-maker-finder`).

### 5. Fill gaps

| Gap | Tool | Price |
|-|-|-|
| A target domain returned zero people | `scrape_website_finder`, one `jobTitle` per run across those domains | $0.0499 per contact found |
| A person with no email | `find_emails` with `first_name`, `last_name`, `domain` (`company_name` only when no domain resolves; `full_name` when the name will not split) | $0.05 per email found, free if not found |
| Still no email | Drop from the email file; keep in a gaps file | $0 |

Leave `autoValidateEmails` off on Website Finder; validation runs once in step 7. Record a miss in the gaps file; no address is built from a naming pattern. Order follows price per usable result: a database email costs $0.0072 / valid share to validate into a usable address (about $0.009 at the example's 80% valid share) against $0.05 from Email Finder and ($0.0499 + $0.0072) / valid share from Website Finder plus validation.

### 6. Normalize, dedupe, suppress

Normalize per `references/list-quality-standard.md` section 3. Dedupe on lowercased email, then LinkedIn URL, then first name + last name + domain. Suppress in this order: unsubscribes, bounces, complaints, current customers, open opportunities, competitors, anyone in another active campaign, anyone contacted inside the user's re-contact window. Count every drop by reason. Drop rows with no first name from a personalized campaign or move them to a non-personalized variant.

### 7. Validate

Send every email that did not come from Email Finder to `validate_emails` ($0.0072 each). Route: `valid` to the send file; `valid_catch_all` to a catch-all file for a separate campaign at a daily volume the user sets, paused if its bounces pass 2% (Berman), highest-evidence rows first (high `email_quality`, an address format that matches other known addresses at the domain, no security gateway); `unknown` held for one retry on a date in the report; `invalid` and `disposable` removed and added to the blocklist.

### 8. Cap and order per company

Keep no more contacts per `company_domain` than the user agreed, highest buying role first. Write `company_contact_order` (1, 2, 3...) so the sequencer can stagger them: contact 2 starts only after contact 1's sequence ends without a reply, per Berman's one-person-at-a-time guidance. Instantly and Smartlead both run campaigns per list, so put later contacts in a second wave file.

### 9. Personalization columns

Add only columns the copy uses, and only facts with a source: `industry`, `city`, `employee_band`, `case_study` (chosen per segment), `trigger` (account level, from `account-researcher` or a signal list). Smartlead's import guide says a blank cell means the value does not appear in the email, which leaves "Hi ," in the inbox; give every variable a fallback in the copy or drop rows where it is blank. Never generate facts about a prospect to fill a column.

### 10. Format for the sequencer

Map columns to the platform's headers with `references/sequencer-import-specs.md`: UTF-8 CSV, header row first, unique headers, Instantly headers of 20 characters or fewer starting with a capital letter, no more than 50 variables (Instantly) or 40 custom variables (Smartlead). One file per campaign. Turn on the platform's duplicate check across campaigns and import the blocklist first.

### 11. Report and launch checklist

Before export, read a random sample (size set by the user) against the brief: title in the agreed family, company in the ICP band, person still at the company on their profile or the team page, domain opens the company's own site. Misses that repeat on one check mean the filter or mapping is wrong: fix the query and re-pull instead of patching rows. Record the result as one launch-checklist line ("19 of 20 title fit, 20 of 20 company fit, 18 of 20 still there").

Fill `templates/output-template.md`, run the launch checklist in the reference, and run `scripts/check-output.py`.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Count and pull | `query_lead_database` | Included on Growth and Scale; 100,000 new leads a day |
| Empty target domains | `scrape_website_finder` | $0.0499 per contact found |
| Names without emails | `find_emails` | $0.05 per email found, free if not found |
| Validation | `validate_emails` | $0.0072 per email |
| URL-based people search the database cannot cover | `scrape_apollo` | $0.0039 per lead; hours to days, use a webhook |
| Runs | `check_run_status`, `download_results`, `list_runs` | Free |

### Calls

ICP count:

```json
{"title": "CFO, Chief Financial Officer, Controller, VP Finance, Director of Finance",
 "notTitle": "assistant, intern, former, retired, advisor, board, accounts payable",
 "industry": ["construction"], "minEmployees": 50, "maxEmployees": 500,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

Pull: the same body with `"limit": 100, "after": "0"`, then each `pagination.next_after`. Confirm the `industry` label with the count; if it returns 0, use `keywords` instead.

Domain batch:

```json
{"companyDomain": "ridgelinebuilders.example, coppercreekcontracting.example",
 "title": "CFO, Chief Financial Officer, Controller, VP Finance", "notTitle": "assistant, intern, former",
 "limit": 100, "after": "0"}
```

Website Finder for empty domains: `{"domains": ["..."], "jobTitle": "Controller", "autoValidateEmails": false}`. Email Finder: `{"contacts": [{"first_name": "Lena", "last_name": "Ortiz", "domain": "graniteforge.example"}]}`. Validation: `{"emails": [...]}` for a list that fits in one tool argument; for larger files the CLI's `email-validate` command with a one-address-per-line file, or `POST /api/v1/scrape/email-validator`.

### Worked cost estimate

1,200 send-ready finance leaders at US construction firms, plus 140 priority domains from the user's CRM:

| Item | Units | Unit price | Cost |
|-|-:|-:|-:|
| Lead Database: ICP pull and priority domains | 1,696 leads | Included in Growth | $0.00 |
| Website Finder on 44 empty priority domains | 19 contacts found | $0.0499 | $0.95 |
| Email Finder for 15 names | 10 emails found | $0.05 | $0.50 |
| validate_emails after dedupe and suppression | 1,552 emails | $0.0072 | $11.17 |
| Total | | | $12.62 |

Ceiling shown before the run: $2.20 (Website Finder, 44 domains) + $0.75 (Email Finder, 15 names) + $12.35 (validation, up to 1,715 emails) = $15.30. Run `check_wallet`, show it and wait for a yes. Cost per send-ready row in the example: $12.62 / 1,247 = $0.010.

### Error handling

| Response | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, stop before validation; never import unvalidated rows |
| 409 | Same request moments ago; reuse the earlier run from `list_runs` |
| 409 `filters_not_applied_yet` | Drop the listed company filters or retry later |
| 503 on a database call | Narrow: add a state, a size band or fewer titles |
| Apollo run still RUNNING | Normal; wait for the webhook, check at most hourly |
| Sequencer rejects the CSV | Re-export as UTF-8, check header length and duplicates per the reference |

## Output Format

1. `send-ready-[segment]-[date].csv`: valid emails only, headers mapped for the chosen sequencer, plus `email_status`, `email_validated_at` and `company_contact_order` kept in a parallel master file.
2. `send-ready-[segment]-[date]-wave2.csv` for second and third contacts per company.
3. `catch-all-[segment]-[date].csv` for a separate campaign at the user's daily volume.
4. `suppression-additions-[date].csv` with invalid and disposable addresses for the blocklist.
5. The report from `templates/output-template.md`: campaign brief, sourcing plan, count check, pipeline funnel, validation, send capacity, sequencer import map, cost, sample rows, launch checklist.

- What the reader receives is the deliverable only, in product names (Lead Database, Email Validator, Email Finder, Mobile Finder, Website Finder): no tool ids, JSON tool calls, run IDs, skill names, file paths, reference section numbers or runbook IDs; a downstream step is written out as the checks or commands the team runs, never handed to another skill by name; no tables of checks that were not run (one "Not checked:" line instead); and no repeated identical rows where one template plus a list will do. `scripts/check-output.py` fails a report that carries a tool id, skill name or path.

## Quality Check

- [ ] Count calls ran and the approved estimate appears before any paid step.
- [ ] Funnel adds up stage by stage with a reason on every change.
- [ ] Every row in the send file is `valid`, validated within four weeks of its send date or given a re-validation date.
- [ ] 0 duplicate emails, 0 suppression matches, no more contacts per company than agreed, contact 1 only in wave 1.
- [ ] Every personalization column used in the copy is filled on every row, or the copy has a fallback.
- [ ] The QA sample result appears in the launch checklist, and any repeated miss led to a re-pull.
- [ ] Send capacity: mailboxes x sends per mailbox equals daily sends, sends per mailbox is under 50 (Berman), and the sending days fit the campaign window.
- [ ] Import headers are unique, under 20 characters and accepted by the platform.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Importing straight from the database | Unvalidated rows bounce; the sequencer auto-pauses | Validate every non-Email Finder address first |
| Building 5,000 rows for 3 mailboxes | Rows age past four weeks before they are sent and decay (Hunter: over 2% in four weeks) | Size from capacity; build in waves |
| Every contact at a company in one campaign | Several people get the same email at once; Berman says that can get the sender blocked company wide | Cap at the agreed number, wave file for later contacts |
| Blank `{{first_name}}` | "Hi ," in the inbox | Drop or route blank-name rows to a variant |
| Catch-all rows in the main campaign | Bounces you could not see coming | Separate campaign at the user's daily volume, paused past 2% bounces |
| Headers like `Company Name (from CRM)` | Instantly rejects headers over 20 characters | Short, unique headers from the reference map |
| Duplicate check off at upload | The same person enters two campaigns | Keep the cross-campaign duplicate check on |
| Generated "personal" facts in a column | One wrong fact kills the reply | Only sourced facts; segment-level variables otherwise |
| Filling Email Finder misses with `first.last@domain` | A built address is unverified; on a catch-all domain it passes validation and bounces on send | Keep the miss in the gaps file; try Website Finder for the domain |
| Batch Email Finder file with commas in names or company names | The CLI `--file` reader splits on every comma, so "Acme, Inc." shifts the columns | Strip commas from those fields or send JSON through MCP or REST |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or the routing table. |
| `references/pipeline-runbook.md` | Running steps 2-9: capacity sizing, sourcing recipes, gap fill, dedupe, suppression order, per-company waves, personalization columns. |
| `references/sequencer-import-specs.md` | Step 10: header rules and maps for Instantly, Smartlead, Lemlist and EmailBison, upload settings, launch checklist. |
| `references/list-quality-standard.md` | Columns, dedupe keys, validation buckets (shared). |
| `references/deliverability-primer.md` | Mailbox provider sender rules and bounce monitoring (shared). |
| `references/alex-berman-cold-email.md` | Targeting, testing and account sequencing guidance (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling, retries (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database rules (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished Instantly-ready list of finance leaders at US construction firms. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `icp-list-builder` for the ICP definition and filters behind the pull.
- `decision-maker-finder` when the user has accounts and needs buying roles.
- `email-list-cleaner` to re-validate a list that missed its launch window.
- `local-business-list` for small-business campaigns before import prep.
- `cold-email-strategy` for the offer, segment and sequence this list serves.
- `cold-email-copywriting` for the emails that use the personalization columns.
- `sending-platforms` for upload settings, blocklists and auto-pause.
- `email-deliverability` for domain and mailbox health before launch.
