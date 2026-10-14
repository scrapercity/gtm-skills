---
name: mobile-appender
description: >-
  Turns LinkedIn profile URLs or work emails into a dialer-ready calling list
  with ScraperCity Mobile Finder ($0.25 per number found, nothing when none is
  found). Estimates cost from a measured pilot hit rate, sends one input per
  person, normalizes every number to E.164, checks line type, removes shared
  numbers and anyone on the suppression list, and tags each row with a dial
  status. Use when the user says "find mobiles for these LinkedIn profiles",
  "append cell numbers", "my SDRs need direct dials", "build a call list", or
  "add phone numbers before the call blitz".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags:
    - mobile
    - cold-calling
    - suppression
    - line-type
    - e164
    - mobile-finder
    - sdr
  related_skills:
    - cold-calling
    - crm-enricher
    - multi-channel-outreach
    - decision-maker-finder
    - skip-tracer
    - email-list-cleaner
    - scrapercity-mcp
  frameworks:
    - "ITU-T Recommendation E.164"
    - "Twilio - Lookup Line Type Intelligence"
    - "Service Objects - number portability and line type (2015)"
    - "NIST/SEMATECH e-Handbook - confidence limits for a proportion"
    - "IANA Time Zone Database"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
    - scrapercity-agent-patterns.md
---

# Mobile Appender

## Overview

This skill produces a calling list: one row per person with a mobile number in E.164, its line type, a suppression check, a time zone and a `dial_status` that says whether a rep dials it now or a person reviews it first. A short report shows the measured hit rate, the cost, and a funnel from inputs to dial-ready numbers.

It prevents three expensive mistakes:

1. Paying twice for one person. Mobile Finder bills $0.25 for every number it finds; send a LinkedIn URL and an email for the same person and two hits cost $0.50 for one human.
2. Budgeting blind. ScraperCity does not publish a hit rate, so a list run without a pilot can cost anywhere from a few dollars to the full ceiling of $0.25 per input.
3. Loading numbers labeled "mobile" that are office lines, VoIP numbers or shared reception numbers, so reps burn dials on the wrong line.

## When to Use

- "Find mobile numbers for these 300 LinkedIn profiles so my SDRs can dial them."
- "Append cell phones to this list of emails."
- "We need direct dials for the call blitz next week."
- "Add mobiles to our open opportunities."

Use a different skill when:

| The user wants | Use |
|-|-|
| Mobiles written back into HubSpot, Pipedrive, GoHighLevel or Salesforce with audit columns | `crm-enricher` (then run this skill's post-processing on the result) |
| Phones for homeowners or consumers from names or addresses | `skip-tracer` |
| The call script, cadence and objection handling | `cold-calling` |
| Who to call at a list of accounts | `decision-maker-finder` |
| Email plus phone plus LinkedIn sequencing | `multi-channel-outreach` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| LinkedIn URLs or work emails, one row per person | Mobile Finder inputs | Ask |
| Who reps will dial: seniority levels and departments | Every number found bills $0.25, so the input list is cut to these people before the pilot | Ask; filter on the seniority and department columns (Lead Database records carry both) |
| How numbers will be dialed: manual, click-to-call, power dialer | Decides whether every number needs a line-type lookup | Manual click-to-call |
| The suppression list (everyone who asked not to be contacted, from every tool) | Removed before the pilot and after the append | Ask; without it, the list ships with `suppressed = unchecked` |
| Where the people sit | E.164 country code and time zone | From the person's location column |
| Budget ceiling | Sets the batch size | Show the estimate and ask |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| ScraperCity catalog | `find_mobiles` takes social profile URLs or email addresses and bills $0.25 per number found, nothing on a miss. |
| ITU-T E.164 | `+`, country code, national number, 15 digits maximum. |
| Service Objects, "The Benefits and Uses of Local Number Portability" (September 10, 2015) | A number can move between switches and carriers, so its prefix no longer tells you the line type. |
| Twilio Lookup Line Type Intelligence | Returns mobile, landline, fixedVoip, nonFixedVoip, tollFree and other line types for a number. |
| NIST/SEMATECH e-Handbook | Confidence limits for a proportion, used to size the pilot and the low and high scenarios. |
| IANA Time Zone Database | The zone names stored in `tz`. |

Details and the routing table: `references/framework-notes.md`.

## Workflow

### 1. Scope the job

Before any paid call, record in the report's Call Plan table: the dialing method, the suppression list used and its row count, the countries in the list, and whether line-type lookups will run on every number. Any automated or power dialer that drops calls on non-mobile lines needs a lookup on every number; a click-to-call team can skip it and let reps mark wrong lines.

### 2. Normalize and dedupe inputs

- One row per person, one input per person per run. If a person has a LinkedIn URL and a work email, the first run gets the URL; a second run sends the work email only for people whose URL found nothing. Misses are free, so the second pass adds coverage and cannot bill anyone twice.
- LinkedIn URLs: lowercase, `https://www.linkedin.com/in/<slug>`, strip query strings, locale suffixes and trailing slashes. Drop company pages (`/company/`), Sales Navigator links (`/sales/`) and post links; they do not identify a person.
- Emails: trim, lowercase, reject syntax failures. Work emails only; Mobile Finder's catalog description names social profile URLs or work email addresses.
- Remove people already holding a mobile in the source, and anyone on the suppression list.

Details: `references/phone-normalization-and-line-type.md`.

### 3. Pilot 50 and measure the hit rate

Run `find_mobiles` on 50 random inputs. Cost is at most 50 x $0.25 = $12.50. Hit rate = numbers found / 50. ScraperCity does not publish a hit rate, so this pilot is the planning number. At 50 inputs the standard error near a 50% rate is about 7 points (NIST/SEMATECH formula), so set the low and high scenarios at least 14 points either side. The method is in `references/cost-and-hit-rate-model.md`.

### 4. Estimate and confirm

```text
expected cost = remaining inputs x hit rate x $0.25
ceiling       = remaining inputs x $0.25
```

Show low, expected, high and ceiling scenarios. Run `check_wallet`. Wait for a go-ahead on the ceiling before the main run.

### 5. Run the append

Phone ladder, cheapest first: the mobile already in the source; on Growth and Scale, a Lead Database people call with `hasPhone: true` for a direct or company line at $0 wallet (written to `phone`, never to `mobile`); then `find_mobiles` with URLs; then the work-email second pass for URL misses.

Send many inputs per run, never one run per row. Split the list into batches when the user wants to stop early: after each batch, compare its hit rate with the pilot's low scenario, and if it falls below, stop and look at the inputs (old export, wrong country, company pages). Poll `check_run_status`, report, and check again later instead of looping (the CLI `poll` command defaults to every 15 seconds); then `download_results`. Keep the `runId` per batch in the run log.

### 6. Post-process every number

1. Normalize to E.164. US and Canada: `+1` and 10 digits, area code and exchange not starting with 0 or 1.
2. Flag shared numbers: one number on two or more people is an office line or a reception desk. Hold.
3. Line type: a number's prefix does not prove a mobile once it has been ported. When the plan calls for lookups, run each number through a carrier lookup the user holds (for example Twilio Lookup Line Type Intelligence). Keep `line_type`.
4. Suppression: match every number and email against the one suppression list. Record `suppression_checked_at`.
5. Time zone: from the person's location, not the area code (mobiles travel). Store `tz` so the dialer places each call inside the window the team sets in the prospect's local time.

### 7. Assign dial status and deliver

| `dial_status` | Rule |
|-|-|
| `callable` | Mobile line type or unchecked, not shared, not suppressed |
| `hold_suppressed` | On the suppression list. Never dialed |
| `hold_line_type` | Landline, VoIP or unknown when the plan needs a mobile; review by hand |
| `hold_shared_number` | Same number on two or more people |

Deliver the CSV and the report from `templates/output-template.md`; run `scripts/check-output.py`.

## ScraperCity Implementation

### Tools and prices (from `references/scrapercity-catalog.md`)

| Step | Tool | Price |
|-|-|-|
| Balance | `check_wallet` | Free |
| Mobile append | `find_mobiles` with `inputs[]` (social profile URLs or email addresses, auto-detected) | $0.25 per number found, free if not found |
| Optional email check for the multi-channel file | `validate_emails` with `emails[]` | $0.0072 per email |
| Poll and fetch | `check_run_status`, `download_results` | Free |
| Inputs from accounts | `query_lead_database` with `companyDomain`, `title`, `hasPhone` (Growth and Scale) | Included |

### Calls

```json
{"tool": "find_mobiles", "args": {"inputs": [
  "https://www.linkedin.com/in/priya-natarajan",
  "https://www.linkedin.com/in/marcus-bell-it",
  "j.alvarez@coastalhealth.example"
]}}
```

CLI: `npx scrapercity mobile-find https://www.linkedin.com/in/priya-natarajan j.alvarez@coastalhealth.example`, then `npx scrapercity poll <runId>` and `npx scrapercity download <runId>`. REST: `POST https://app.scrapercity.com/api/v1/scrape/mobile-finder` with `{"inputs": [...]}`, then `GET /api/v1/scrape/status/{runId}` and `GET /api/downloads/{runId}`.

Mobile Finder is also reachable through `scrape_website_finder` with `autoFindMobiles` and through `find_emails` options in the CLI, but the catalog prices only the standalone tool. Use `find_mobiles` directly so every charge is $0.25 per number found.

### Worked cost estimate

340 rows received; after dedupe and dropping 6 company or Sales Navigator links, 326 inputs. Pilot 50: 18 found (36%).

| Scenario | Inputs | Hit rate | Numbers found | Cost |
|-|-:|-:|-:|-:|
| Pilot (done) | 50 | 36% | 18 | $4.50 |
| Low | 276 | 20% | 55 | $13.75 |
| Expected | 276 | 36% | 99 | $24.75 |
| High | 276 | 50% | 138 | $34.50 |
| Ceiling | 276 | 100% | 276 | $69.00 |

Ask for a go-ahead on the $69.00 ceiling (the expected spend is $24.75). Cost per dial-ready number is total spend divided by the numbers that pass the shared-number, line-type and suppression checks; report it from the run's own counts. Carrier lookups are billed by the lookup provider, not ScraperCity.

### Errors

| Code | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, offer a smaller batch. |
| 409 | Same inputs submitted moments ago; reuse the earlier `runId`. |
| 429 | Wait 30 seconds, retry once. |
| Run `FAILED` | Read `statusMessage` and logs; check for malformed URLs before resubmitting. |

## Output Format

1. `mobiles-[segment]-[date].csv`: one row per person with `first_name`, `last_name`, `company_name`, `input_used`, `mobile` (E.164), `line_type`, `suppressed`, `suppression_checked_at`, `tz`, `dial_status`, `source = mobile_finder`, `pulled_at`.
2. `mobiles-[segment]-[date]-hold.csv`: every `hold_*` row with its reason.
3. A report from `templates/output-template.md`: input summary, call plan, cost estimate with the hit-rate scenarios, append funnel, line type and suppression results, dial rules, output schema, sample rows, next steps.

- What the reader receives is the deliverable only, in product names (Lead Database, Email Validator, Email Finder, Mobile Finder, Website Finder): no tool ids, JSON tool calls, run IDs, skill names, file paths, reference section numbers or runbook IDs; a downstream step is written out as the checks or commands the team runs, never handed to another skill by name; no tables of checks that were not run (one "Not checked:" line instead); and no repeated identical rows where one template plus a list will do. `scripts/check-output.py` fails a report that carries a tool id, skill name or path.

## Quality Check

- [ ] The call plan was recorded before the pilot.
- [ ] One input per person per run; the email pass held only people whose URL missed.
- [ ] The pilot hit rate and the low, expected, high and ceiling scenarios appear, and the user approved the ceiling.
- [ ] Every delivered mobile matches E.164 (`+` then 8 to 15 digits, first digit not 0).
- [ ] No `callable` row is on the suppression list or shared by two people.
- [ ] The funnel adds up from inputs to dial-ready, and the dial rules sum to the numbers found.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Sending URL and email for the same person in one run | Two hits bill $0.50 for one person | URL in run 1; email in run 2 for URL misses only |
| Time zone from area code | Mobiles keep their area code when people move | Use the person's location |
| Trusting "mobile" without a line-type check | Ported numbers break prefix rules | Carrier lookup when the dialer needs true mobiles |
| Skipping the pilot | Budget swings 2.5x between a 20% and a 50% hit rate | Pilot 50 first |
| Loading shared numbers as mobiles | Reps reach a reception desk, not the person | Hold any number on two or more people |
| Suppression list kept in one tool only | A person who asked to be removed in email gets a call | One suppression list, checked before the pilot and after the append |
| Using Mobile Finder on consumers | Its inputs are work identities | Use `skip-tracer` |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/dial-status-and-suppression.md` | Running the suppression check, choosing dial status, handling removal requests during the campaign. |
| `references/phone-normalization-and-line-type.md` | Normalizing inputs and outputs, E.164 by country, line types, shared numbers, time zones. |
| `references/cost-and-hit-rate-model.md` | Running the pilot, building scenarios, cost per dial-ready number. |
| `references/list-quality-standard.md` | Column names and E.164 rule (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet, polling, retries (shared). |
| `references/scrapercity-platform.md` | Plans and databases (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished report for 340 IT leaders at US hospitals. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `cold-calling` for scripts, cadence and call windows.
- `crm-enricher` to write the numbers back to the CRM with audit columns.
- `multi-channel-outreach` to combine calls with email and LinkedIn touches.
- `decision-maker-finder` to pick whom to call at each account.
- `skip-tracer` for consumer or property-owner phones.
- `email-list-cleaner` for the email side of the same list.
- `scrapercity-mcp` for MCP setup.
