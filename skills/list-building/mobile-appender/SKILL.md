---
name: mobile-appender
description: >-
  Turns LinkedIn profile URLs or work emails into a dialer-ready calling list
  with ScraperCity Mobile Finder ($0.25 per number found, nothing when none is
  found). Gates the job on TCPA and Do Not Call rules before spending,
  estimates cost from a measured hit rate, sends one input per person,
  normalizes every number to E.164, checks line type, scrubs internal and
  national DNC lists, and tags each row with a dial status and an SMS flag.
  Use when the user says "find mobiles for these LinkedIn profiles", "append
  cell numbers", "my SDRs need direct dials", "build a call list", or "add
  phone numbers before the call blitz".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [mobile, cold-calling, tcpa, dnc, e164, mobile-finder, sdr]
  related_skills: [cold-calling, crm-enricher, multi-channel-outreach, decision-maker-finder, skip-tracer, email-list-cleaner, scrapercity-mcp]
  frameworks:
    - "FCC - TCPA, 47 U.S.C. 227 and 47 CFR 64.1200"
    - "FTC - Telemarketing Sales Rule and the National Do Not Call Registry"
    - "FCC - Reassigned Numbers Database and safe harbor, 47 CFR 64.1200(m)"
    - "US Supreme Court - Facebook v. Duguid (2021)"
    - "Ninth Circuit - Chennette v. Porch.com (2022)"
    - "Eleventh Circuit - Insurance Marketing Coalition v. FCC (2025)"
    - "ITU-T Recommendation E.164"
    - "CRTC - Unsolicited Telecommunications Rules; ICO - PECR telephone marketing"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, scrapercity-agent-patterns.md, outbound-compliance-primer.md]
---

# Mobile Appender

## Overview

This skill produces a calling list: one row per person with a mobile number in E.164, its line type, its Do Not Call status, a `dial_status` that says how the number may be dialed, and an `sms_allowed` flag. A short report shows the compliance answers, the measured hit rate, the cost, and a funnel from inputs to dial-ready numbers.

It prevents three expensive mistakes:

1. Loading appended mobiles into an autodialer, a prerecorded or AI-voice campaign, or a texting tool without consent. Under the TCPA that is $500 per call or text in private suits, up to triple if willful.
2. Paying twice for one person. Mobile Finder bills $0.25 for every number it finds; send a LinkedIn URL and an email for the same person and two hits cost $0.50 for one human.
3. Dialing numbers labeled "mobile" that are office lines, VoIP numbers or shared numbers, or that sit on the National Do Not Call Registry, because nobody checked after the append.

## When to Use

- "Find mobile numbers for these 300 LinkedIn profiles so my SDRs can dial them."
- "Append cell phones to this list of emails."
- "We need direct dials for the call blitz next week."
- "Add mobiles to our open opportunities."

Use a different skill when:

| The user wants | Use |
|-|-|
| Mobiles written back into HubSpot, Pipedrive, GoHighLevel or Salesforce with audit columns | `crm-enricher` (then run this skill's gate on the result) |
| Phones for homeowners or consumers from names or addresses | `skip-tracer` |
| The call script, cadence and objection handling | `cold-calling` |
| Who to call at a list of accounts | `decision-maker-finder` |
| Email plus phone plus LinkedIn sequencing | `multi-channel-outreach` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| LinkedIn URLs or work emails, one row per person | Mobile Finder inputs | Ask |
| How numbers will be dialed: manual, click-to-call, power or predictive dialer, prerecorded or AI voice, SMS | Decides consent needs | Manual live calls only; no SMS |
| Who the recipients are and where they sit | TSR B2B exemption, state rules, Canada and UK rules | B2B contacts in the US |
| Consent records, if any | Required for automated calls and texts | None |
| Internal do-not-call list and the user's National DNC Registry access (SAN) | Scrubbing | Ask; without a scrub, numbers stay on hold |
| Budget ceiling | Mobiles are the most expensive per-row enrichment | Show the estimate and ask |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| TCPA, 47 U.S.C. 227 | Autodialed or artificial or prerecorded voice calls to wireless numbers need prior express consent. Private damages $500 per violation, up to triple if willful or knowing. |
| 47 CFR 64.1200 | Prior express written consent for telemarketing robocalls; no telephone solicitation before 8 a.m. or after 9 p.m. local time; internal do-not-call lists with opt-outs honored within 10 business days and kept 5 years; wireless numbers covered by the DNC rules; 15-day safe harbor for numbers just ported from wireline to wireless; reassigned-number safe harbor in paragraph (m). |
| FTC Telemarketing Sales Rule | Scrub against the National DNC Registry at least every 31 days. Most calls to a business to sell to that business are exempt from the TSR's DNC provisions. Civil penalties up to $53,088 per violation (the 2025 figure, unchanged for 2026). |
| Facebook v. Duguid (2021) | An autodialer under the TCPA is equipment that stores or produces numbers with a random or sequential number generator. Prerecorded and artificial voice rules apply regardless of equipment. |
| FCC declaratory ruling (February 2024) | AI-generated voices count as artificial voices under the TCPA, so AI voice calls need the same consent as prerecorded calls. |
| Chennette v. Porch.com (9th Cir. 2022) | A registered cell phone used for both personal and business purposes is presumptively residential for DNC purposes. A B2B caller cannot assume a business person's personal mobile on the Registry is exempt. |
| Insurance Marketing Coalition v. FCC (11th Cir. 2025) | Vacated the FCC's one-to-one consent rule. Consent can still be obtained for several sellers; prior express written consent itself remains. |
| ITU-T E.164 | `+`, country code, national number, 15 digits maximum. |
| CRTC and ICO | Canada's DNCL rules do not apply to calls to businesses but an internal list is still required; UK live marketing calls are screened against TPS and CTPS. |

Details and the routing table: `references/framework-notes.md`. Shared rules: `references/outbound-compliance-primer.md`. Nothing here is legal advice.

## Workflow

### 1. Run the compliance gate first

Before any paid call, answer these and write the answers into the report's Compliance Gate table:

| Question | Answer leads to |
|-|-|
| How will numbers be dialed? | Manual or click-to-call by a human, live voice: proceed. Power, predictive or any dialer that might fall under the autodialer definition, prerecorded voice, AI voice, or ringless voicemail: only for numbers with documented prior express written consent (telemarketing) or prior express consent (informational). |
| Will anyone text these numbers? | Default `sms_allowed = no`. Texts are treated as calls under the TCPA rules. |
| Who is called, and in what role? | B2B sales calls are mostly exempt from the TSR's DNC provisions, but registered mobiles can still be "residential" under the FCC rules (Chennette). Default: scrub and hold registered mobiles unless the user's counsel approves calling them. |
| Where are they? | US: Registry plus state lists and state calling laws (for example Florida's Telephone Solicitation Act). Canada: internal list required; DNCL does not apply to calls to businesses. UK: TPS and CTPS screening for live calls; recorded calls need specific consent. EU: national rules; ask counsel. |
| Is any number for a consumer, not a business contact? | Use `skip-tracer` and its consumer gate instead. |

If the user wants automated calls or texts and has no consent records, the job continues only as a manual-call list. Say so plainly before spending.

### 2. Normalize and dedupe inputs

- One row per person. If a person has a LinkedIn URL and an email, send the URL only.
- LinkedIn URLs: lowercase, `https://www.linkedin.com/in/<slug>`, strip query strings, locale suffixes and trailing slashes. Drop company pages (`/company/`), Sales Navigator links (`/sales/`) and post links; they do not identify a person.
- Emails: trim, lowercase, reject syntax failures. Work emails only; Mobile Finder's catalog description names social profile URLs or work email addresses.
- Remove people already holding a mobile in the source, and anyone on the internal do-not-call list.

Details: `references/phone-normalization-and-line-type.md`.

### 3. Pilot 50 and measure the hit rate

Run `find_mobiles` on 50 random inputs. Cost is at most 50 x $0.25 = $12.50. Hit rate = numbers found / 50. ScraperCity does not publish a hit rate, so this pilot is the planning number. The method and confidence range are in `references/cost-and-hit-rate-model.md`.

### 4. Estimate and confirm

```text
expected cost = remaining inputs x hit rate x $0.25
ceiling       = remaining inputs x $0.25
```

Show low, expected, high and ceiling scenarios. Run `check_wallet`. Over $5, wait for a go-ahead.

### 5. Run the append

Batches of up to 500 inputs. Poll `check_run_status` (first check after 30 seconds, then every 30 seconds within the session as the user waits), then `download_results`. Keep the `runId` per batch in the run log.

### 6. Post-process every number

1. Normalize to E.164. US and Canada: `+1` and 10 digits, area code and exchange not starting with 0 or 1.
2. Flag shared numbers: one number on two or more people is an office line or a reception desk. Hold.
3. Line type: number portability means the prefix does not prove a mobile. If any automated dialing or SMS is planned, or the user wants certainty, run the numbers through a carrier lookup the user holds (for example Twilio Lookup Line Type Intelligence returns mobile, landline, fixedVoip, nonFixedVoip and others). Keep `line_type`.
4. Scrub: internal do-not-call list, then the National DNC Registry through the user's access (within the last 31 days), then any state list the user subscribes to. Record `dnc_checked_at`.
5. Reassigned numbers: for any number with consent on file, query the FCC Reassigned Numbers Database with the consent date before automated contact.
6. Time zone: from the person's location, not the area code (mobiles travel). Store `tz` so the dialer enforces 8 a.m. to 9 p.m. local.

### 7. Assign dial status and deliver

| `dial_status` | Rule |
|-|-|
| `callable_manual` | Mobile line type or unchecked, not on any DNC list, live manual dialing only |
| `callable_auto_consented` | Consent record on file, scrubbed, reassigned check passed |
| `hold_dnc` | On the National or a state Registry, no consent, counsel has not cleared B2B calls to registered mobiles |
| `hold_internal_dnc` | On the user's own do-not-call list. Never call |
| `hold_line_type` | Landline, VoIP or unknown when the plan needs a mobile; review by hand |
| `hold_shared_number` | Same number on two or more people |

`sms_allowed = yes` only with consent on file for texts. Deliver the CSV and the report from `templates/output-template.md`; run `scripts/check-output.py`.

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

ScraperCity's site states Mobile Finder covers 250M+ people (per scrapercity.com). Coverage is not a hit-rate promise for any one list.

### Worked cost estimate

340 rows received; after dedupe and dropping 6 company or Sales Navigator links, 326 inputs. Pilot 50: 18 found (36%).

| Scenario | Inputs | Hit rate | Numbers found | Cost |
|-|-:|-:|-:|-:|
| Pilot (done) | 50 | 36% | 18 | $4.50 |
| Low | 276 | 20% | 55 | $13.75 |
| Expected | 276 | 36% | 99 | $24.75 |
| High | 276 | 50% | 138 | $34.50 |
| Ceiling | 276 | 100% | 276 | $69.00 |

Ask for a go-ahead on the $69.00 ceiling (the expected spend is $24.75). If 99 numbers are found and about 70% survive the DNC and line-type checks, the cost per dial-ready number is about $0.36 ($24.75 / 69, rounded). Carrier lookups and Registry access are billed by those providers, not ScraperCity.

### Errors

| Code | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, offer a smaller batch. |
| 409 | Same inputs submitted moments ago; reuse the earlier `runId`. |
| 429 | Wait 30 seconds, retry once. |
| Run `FAILED` | Read `statusMessage` and logs; check for malformed URLs before resubmitting. |

## Output Format

1. `mobiles-[segment]-[date].csv`: one row per person with `first_name`, `last_name`, `company_name`, `input_used`, `mobile` (E.164), `line_type`, `dnc_status`, `dnc_checked_at`, `tz`, `dial_status`, `sms_allowed`, `source = mobile_finder`, `pulled_at`.
2. `mobiles-[segment]-[date]-hold.csv`: every `hold_*` row with its reason.
3. A report from `templates/output-template.md`: input summary, compliance gate, cost estimate with the hit-rate scenarios, append funnel, line type and DNC results, dial rules, output schema, sample rows, next steps.

## Quality Check

- [ ] The compliance gate was answered before the pilot, and every row names the law it applies.
- [ ] One input per person; no person was sent twice.
- [ ] The pilot hit rate and the low, expected, high and ceiling scenarios appear, and the user approved the ceiling if over $5.
- [ ] Every delivered mobile matches E.164 (`+` then 8 to 15 digits, first digit not 0).
- [ ] No `callable_manual` row is on the internal list or an unwaived Registry hit, and `dnc_checked_at` is within 31 days.
- [ ] `sms_allowed = yes` only where consent is on file.
- [ ] Shared numbers are held.
- [ ] The funnel adds up from inputs to dial-ready.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Sending URL and email for the same person | Two hits bill $0.50 for one person | One input per person, URL first |
| Loading appended mobiles into a predictive dialer | Possible autodialer use; prerecorded or AI voice always needs consent | Manual or click-to-call only without consent |
| Texting the list "just once" | Texts are calls under the TCPA rules; $500 per text in private suits | `sms_allowed = no` without consent |
| Treating B2B as exempt from every DNC rule | The TSR exemption does not settle the FCC rule; Chennette presumes registered mixed-use mobiles residential | Scrub; hold registered mobiles unless counsel clears them |
| Time zone from area code | Mobiles keep their area code when people move | Use the person's location |
| Trusting "mobile" without a line-type check | Ported numbers and VoIP break prefix rules | Carrier lookup before automated or SMS use |
| Skipping the pilot | Budget swings 2x between a 20% and a 50% hit rate | Pilot 50 first |
| Using Mobile Finder on consumers | Consumer contact has stricter rules and a different purpose test | Use `skip-tracer` |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/tcpa-dnc-gate.md` | Answering the compliance gate, scrubbing, choosing dial status, Canada and UK rules. |
| `references/phone-normalization-and-line-type.md` | Normalizing inputs and outputs, E.164 by country, line types, shared numbers, time zones. |
| `references/cost-and-hit-rate-model.md` | Running the pilot, building scenarios, cost per dial-ready number. |
| `references/outbound-compliance-primer.md` | Shared TCPA, DNC, CASL and PECR basics. |
| `references/list-quality-standard.md` | Column names and E.164 rule (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet, polling, retries (shared). |
| `references/scrapercity-platform.md` | Plans and the compliance boundary (shared). |
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
