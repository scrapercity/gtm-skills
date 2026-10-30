---
name: email-list-cleaner
description: >-
  Cleans an old or inherited email list before anyone sends to it: repairs
  syntax, dedupes, applies suppression, flags role and free-provider
  addresses, validates every unique address with ScraperCity's Email
  Validator, and splits the result into send-ready, catch-all, hold and
  removed files with a reason on every dropped row. Use when the user says
  "clean this list", "verify these emails", "this list is 2 years old",
  "my bounce rate spiked", "is this list safe to send", or hands over a CSV
  export before a campaign or re-launch.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags:
    - email-validation
    - list-hygiene
    - bounce-rate
    - catch-all
    - suppression
    - deliverability
  related_skills:
    - cold-email-list
    - crm-enricher
    - icp-list-builder
    - email-deliverability
    - sending-platforms
    - scrapercity-cli
  frameworks:
    - "Google - Email sender guidelines (Feb 2024)"
    - "Yahoo - Sender best practices (Feb 2024)"
    - "Microsoft - Outlook high-volume sender requirements (May 2025)"
    - "M3AAWG - Sender Best Common Practices"
    - "IETF RFC 2142 - mailbox names for common services"
    - "Hunter - Email verification guide, email data decay (Nov 2025)"
    - "Alex Berman - verify every email, keep bounces under 2%"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
    - deliverability-primer.md
---

# Email List Cleaner

## Overview

This skill turns a list of unknown quality into five files and a report: `send_ready.csv` (valid addresses only), `catch_all.csv`, `hold_unknown.csv`, `role_review.csv` and `removed.csv`, plus the suppression rows to add to the sending platform. Every input row ends up in exactly one file, and every removed row carries a reason code.

The mistake it prevents: validating the raw export as-is and sending to everything marked "valid" or "catch-all" in one campaign. Paying to validate duplicates and already-suppressed rows wastes money, and mixing catch-all addresses into the main send is how a list that "passed validation" still bounces at 6% and trips the sequencer's auto-pause. The order of operations here (repair, dedupe, suppress, then validate) is what keeps the bill and the bounce rate low.

## When to Use

- "Clean this list before we send." "Verify these 20,000 emails."
- A list more than four weeks past its last validation, or one that has never been validated.
- A bounce spike on a live campaign (pause first, then clean the remaining rows).
- An inherited list: a former employee's export, an event list, an acquired company's CRM.
- A re-launch to a list that was last mailed months ago.

Use a different skill when:

| The user wants | Use |
|-|-|
| New contacts, not a cleaned old list | `icp-list-builder` or `cold-email-list` |
| Missing emails or mobiles filled into a CRM export | `crm-enricher` |
| Domain, DNS or warmup problems behind the bounces | `email-deliverability` |
| Help choosing or configuring a sequencer | `sending-platforms` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| The file (CSV or XLSX) and which column holds the email | Everything starts here | Ask; detect columns containing `@` |
| Where the list came from and when it was last mailed | Sets risk tier and catch-all policy | "Unknown source, last mailed a year or more ago" (tier C) |
| Intended use (cold email, newsletter, CRM import, ads audience) | Role and catch-all rules differ by use | Cold email |
| List type (named B2B contacts, local businesses, ecommerce stores) | Role address policy | Named B2B contacts |
| Suppression exports (unsubscribes, bounces, complaints, customers) | Must be applied before validation | None supplied; say so in the report |
| Previous bounce rate on this list, if mailed | Calibrates the bounce projection | Unknown |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Google Email sender guidelines (Feb 2024) | Keep spam rate under 0.3%, target under 0.1%. Bounces and complaints from a dirty list feed both. |
| Yahoo Sender best practices | Remove invalid recipients promptly and track bounces and inactive recipients. |
| Microsoft Outlook high-volume sender requirements (5 May 2025) | Lists list hygiene and bounce monitoring as expected practice for senders over 5,000 a day. |
| M3AAWG Sender Best Common Practices | Suppress an address after it bounces consecutively at least two times over two weeks or more; not mailing a list for a year or more is a sign of a dirty list. |
| IETF RFC 2142 (May 1997) | Defines role mailboxes (info, sales, support, abuse, noc, security, postmaster, webmaster). Basis for the role flag. |
| Hunter, Email verification guide (4 Nov 2025) | Verify shortly before the campaign. In Hunter's test, over 2% of a list went invalid within four weeks and 5.5% within eight. Basis for the four-week re-validation window. |
| Alex Berman (alexberman.com, cold email templates) | Verify every email before sending and keep bounces under 2%. The stop line for every send plan here. |
| Instantly, High bounce auto-pause | Pauses a campaign at 5% bounces by default (adjustable) once it has sent 200. Sets the size of the first read on a test batch. |
| `references/list-quality-standard.md` | Normalization, dedupe keys, validation buckets. |
| `references/deliverability-primer.md` | What each validator status means for sending. |

Source details and a routing table for this skill's files: `references/framework-notes.md`.

## Workflow

### 1. Profile the file

Count rows, find the email column (or columns: some exports carry `email`, `email_2`, `work_email`), and record blank emails, cells with more than one address, and the source and last-mailed date. Assign a risk tier:

| Tier | Signal | Effect |
|-|-|-|
| A | Validated within four weeks (Hunter), last send bounced under 2% (Berman) | Re-validate only rows older than four weeks |
| B | Mailed within the last year, not validated in the last four weeks | Full clean, catch-all rows in their own campaign |
| C | Not mailed for a year or more (M3AAWG's dirty-list marker), or source or last-mailed date unknown | Full clean, catch-all rows held out of cold campaigns, first send is a test batch of a size the user sets |

### 2. Repair syntax

Apply the rules in `references/syntax-repair-and-role-rules.md`: trim, strip `mailto:` and display names (`Dana Ruiz <dana@acme.com>`), split multi-address cells into separate rows, remove zero-width characters, fix known consumer-domain typos (`gmial.com` to `gmail.com`). Never rewrite a corporate domain. Log every change in `fix_applied`. Rows that still fail syntax go to `removed.csv` with reason `syntax`; they are not sent to the validator.

### 3. Dedupe

Build `email_key`: lowercase the full address; for consumer `gmail.com` and `googlemail.com` addresses only, also drop dots and any `+tag` in the local part. Keep one row per key using the survivorship order in `references/list-quality-standard.md` section 4b. Record how many rows each key collapsed.

### 4. Suppress before you pay

Match the deduped rows against unsubscribes, hard bounces, complaints, current customers, open opportunities and competitor domains, in that order (exact email first, then domain). Suppressed rows go to `removed.csv` with the list name as the reason. RFC 2142 network-operations mailboxes (`abuse@`, `postmaster@`, `hostmaster@`, `noc@`, `security@`) are removed here too: RFC 2142 routes them to the people who handle abuse reports, not buyers.

### 5. Flag role and free-provider addresses

Set `is_role = true` for the local parts listed in the reference file. On a named-contact B2B list, role rows are validated but routed to `role_review.csv`; on local business and ecommerce lists they stay in the main flow. Set `is_free = true` for consumer providers; on a B2B list keep them only when the person is a sole proprietor or the business uses that address publicly.

### 6. Show the count and cost, then validate

Unique addresses to validate x $0.00169 is the cost. Call `check_wallet`, show the funnel so far and the cost, and wait for a go-ahead before submitting. Then submit:

- A list short enough to fit in one tool argument: MCP `validate_emails` with the array.
- Larger files: one-column text files, submitted through the CLI or REST, one run per file; split into chunks of a size the user picks only so a failed run is cheap to retry. The runbook is `references/batching-and-revalidation-runbook.md`.

Poll `check_run_status`; a typical run finishes in minutes. `download_results` when SUCCEEDED.

### 7. Map results and route every row

Read the downloaded header row first; the documented columns are `email`, `email_result`, `email_quality`, `subresult`, `free`, plus `sc_` enrichment columns such as `sc_is_catch_all`, `sc_mx_provider` and `sc_mx_security_gateway`. Route with `references/status-handling-matrix.md`:

| `email_result` | File | Suppress? |
|-|-|-|
| `valid` (not role on a B2B list) | `send_ready.csv`, ordered high, medium, low `email_quality` | No |
| `valid` and role on a B2B list | `role_review.csv` | No |
| `valid_catch_all` | `catch_all.csv`, ordered by evidence score (quality, address format, person confirmed, no gateway) | Only if it later bounces |
| `unknown` | `hold_unknown.csv`, re-validate once on a later date (greylisting servers defer first attempts, RFC 6647) | No |
| `invalid` | `removed.csv`, reason `invalid` | Yes, add to the platform blocklist |
| `disposable` | `removed.csv`, reason `disposable` | Yes |

### 8. Check the projection and hand off

Hard bounces on `send_ready.csv` should stay under 2% (Berman; Instantly's default auto-pause is 5% once a campaign has sent 200). Report the `invalid` rate per source: a source far above the others is stale or mis-mapped and should not be reused. When the list lives in a CRM, write `email_status` and `email_validated_at` back to every record and enroll sequences only from a view filtered on valid status validated within four weeks, so the next campaign cannot pull an unchecked row. Write the report from `templates/output-template.md`, run `scripts/check-output.py` on it, and set the re-validation dates: four weeks after validation for unsent rows, the retry date for unknowns, and at once for unsent rows at any domain that hard-bounces during the send.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Validate | `validate_emails` (`POST /api/v1/scrape/email-validator`, body `{"emails": [...]}`) | $0.00169 per email |
| Poll, fetch | `check_run_status`, `download_results` | Free |
| Replace an invalid address for a high-value contact | `find_emails` with `contacts: [{first_name, last_name, domain}]` | $0.05 per email found, free if not found |

ScraperCity's validator dedupes the submitted array and bills unique addresses. Dedupe on your side anyway: the `email_key` rule in step 3 catches Gmail dot and case variants an exact match misses, and the count you quote the user should equal the count on the bill. The start response returns `emailCount` and an `estimatedCost`; compare `emailCount` with your unique count before letting a large run continue, and `cancel_run` if they disagree.

MCP call for a small list:

```json
{ "emails": ["dana.ruiz@ledgerline.example", "ops@harborclinic.example", "sam@brightpath.example"] }
```

CLI for a large file (the file must hold one address per line; the CLI keeps any line containing `@`, so a multi-column CSV would send whole lines):

```bash
npx scrapercity email-validate --file chunk_01.txt
npx scrapercity poll <runId>
npx scrapercity download <runId> -o chunk_01_results.csv
```

### Worked cost estimate

A 12,400-row event and webinar list, last mailed 14 months ago (tier C):

| Stage | Rows |
|-|-:|
| Raw rows | 12,400 |
| After splitting 31 two-address cells | 12,431 |
| After removing blank emails (212) and unrepairable syntax (61) | 12,158 |
| After dedupe (1,388 duplicates) | 10,770 |
| After suppression (402 matches) and network-role removal (17) | 10,351 |

| Item | Units | Unit price | Cost |
|-|-:|-:|-:|
| Validation | 10,351 | $0.00169 | $17.49 |
| Optional replacements for 40 invalid VIP contacts, 20 found | 20 found | $0.05 | $1.00 |
| Total | | | $18.49 |

Validating before suppression would have billed at least 480 more addresses (402 suppressed, 17 network-role, 61 broken), $0.81, plus up to 1,388 near-duplicates that the validator's own dedupe may not merge (case variants, Gmail dots and `+tags`), up to $2.35 more. Show this table and wait for a yes before submitting.

### Error handling

| Response | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, stop. |
| 409 | The same batch was submitted moments ago. Find the earlier run with `list_runs` and use it. |
| 429 | Rate limited: back off, then retry once. |
| Run FAILED | Resubmit that chunk once; if it fails again, split it in half and record both run ids. |

## Output Format

1. `send_ready.csv`: `valid` only, columns per `references/list-quality-standard.md` section 2 plus `email_status`, `email_status_raw`, `email_quality`, `email_validated_at`, `is_role`, `is_free`, `fix_applied`.
2. `catch_all.csv`, `hold_unknown.csv`, `role_review.csv`: same columns.
3. `removed.csv`: every dropped row with `removed_reason` (`no_email`, `syntax`, `duplicate`, `unsubscribed`, `bounced`, `complained`, `customer`, `competitor`, `network_role`, `invalid`, `disposable`).
4. `suppression_additions.csv`: `invalid` and `disposable` addresses formatted for the sequencer's blocklist import.
5. The report from `templates/output-template.md`: list profile, cleaning funnel, validation results, segment files, suppression additions, cost, re-validation schedule, next steps.

Small jobs (a handful of addresses, "are these 12 safe to send"): skip the files and the report. Return one table with each address, its `email_result`, `email_quality` and the action (send, separate catch-all campaign, retry on a date, remove), then one line with the cost.

- What the reader receives is the deliverable only, in product names (Lead Database, Email Validator, Email Finder, Mobile Finder, Website Finder): no tool ids, JSON tool calls, run IDs, skill names, file paths, reference section numbers or runbook IDs; a downstream step is written out as the checks or commands the team runs, never handed to another skill by name; no tables of checks that were not run (one "Not checked:" line instead); and no repeated identical rows where one template plus a list will do. `scripts/check-output.py` fails a report that carries a tool id, skill name or path.

## Quality Check

- [ ] Every input row appears in exactly one output file; file row counts sum to the raw row count plus rows created by splitting multi-address cells.
- [ ] No row reached the validator before dedupe and suppression.
- [ ] Validation buckets sum to the number validated, and the billed count equals the unique count.
- [ ] `send_ready.csv` is 100% `valid`, validated within four weeks, with 0 duplicates and 0 suppression matches.
- [ ] No `abuse@`, `postmaster@`, `noc@`, `security@` or `hostmaster@` address in any send file.
- [ ] Catch-all rows sit in their own file, ordered by evidence, with the user's daily volume and the 2% bounce stop written in the report.
- [ ] `check_wallet` ran and the user approved the cost before the run.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Validating the raw export | Pays for duplicates and suppressed rows | Repair, dedupe, suppress, then validate. |
| Passing a multi-column CSV to the CLI `--file` flag | The CLI sends every line containing `@` as an address | Export a one-column text file per chunk. |
| Treating `valid_catch_all` as valid | The server accepts everything at validation time and bounces later | Separate file, separate campaign at the user's daily volume, stopped past 2% bounces. |
| Auto-fixing corporate domains | `acme.co` may be the company's own domain | Fix only the known consumer-domain typos and log each fix. |
| Deleting removed rows | You lose the reason and re-import them next quarter | Keep `removed.csv` and push invalids to the blocklist. |
| Re-validating `unknown` rows in a loop | Each pass bills again | One retry on a later date, then route by the catch-all rule or drop. |
| Sending every valid row on day one from a tier C list | Stale mailboxes surface only on send | First send a test batch; continue only if bounces stay under 2% after 200 sends. |
| Sending catch-all rows in file order | The weakest rows can use up the first 200 sends and stop the catch-all campaign | Order by quality, address format, recent confirmation and gateway; send the best first. |
| Sending more catch-alls at a domain after one hard-bounced | That server rejects at delivery what it accepted at validation | Pause the domain's unsent catch-all rows; re-validate its unsent valid rows. |
| Validation status kept only in the CSV | The next campaign pulls the same contacts from the CRM unchecked | Write status and date back; enroll only from the four-week valid view. |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a threshold or the routing table for this skill. |
| `references/status-handling-matrix.md` | Mapping validator columns to files, combining result, quality and flags. |
| `references/syntax-repair-and-role-rules.md` | Repairing addresses, the typo map, role and free-provider lists. |
| `references/batching-and-revalidation-runbook.md` | Files over 1,000 rows, chunking, run tracking, failures, re-validation cadence. |
| `references/list-quality-standard.md` | Columns, dedupe keys, buckets (shared). |
| `references/deliverability-primer.md` | Mailbox provider sender rules and bounce monitoring (shared). |
| `references/scrapercity-catalog.md` | Tool ids, parameters and prices (shared). |
| `references/scrapercity-platform.md` | Plans and billing rules (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished report for a 12,400-row event list. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `cold-email-list` to rebuild a list when this one comes back mostly invalid.
- `crm-enricher` to find replacement emails and write results back to the CRM.
- `icp-list-builder` for new contacts that match the same profile.
- `email-deliverability` when bounces persist on a cleaned list.
- `sending-platforms` for blocklist import and auto-pause settings.
- `scrapercity-cli` for every CLI command and flag.
