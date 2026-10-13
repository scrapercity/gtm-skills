---
name: cold-calling
description: >-
  Builds a B2B or local-business cold calling program: a call list from
  ScraperCity phone fields and find_mobiles, a per-number DNC and TCPA gate
  (B2B vs consumer lines, wireless numbers, AI-voice ban, state calling hours),
  call blocks with a dials-to-meetings funnel, an opener-reason-question-ask
  script, an objection bank, voicemail and gatekeeper scripts, and CRM logging.
  Use when the user asks for a cold call script, a calling plan, phone numbers
  for a list, connect-rate fixes, objection handling, or whether it is legal to
  call these numbers.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [cold-calling, phone, tcpa, do-not-call, objection-handling, voicemail, sdr, local-business]
  related_skills: [multi-channel-outreach, reply-handling, cold-email-strategy, signal-triggered-outbound, outbound-unit-economics, mobile-appender, local-business-list, decision-maker-finder, scrapercity-lead-database, scrapercity-local-business-database]
  frameworks:
    - "Gong Labs - cold call opening lines (90,380 calls, 2018)"
    - "Gong Labs with 30 Minutes to President's Club (Armand Farrokh, Nick Cegelski) - opener study of 300M+ calls (2024)"
    - "Jeb Blount - telephone prospecting framework (Fanatical Prospecting)"
    - "Alex Berman - cold calling techniques"
    - "Cognism and WHAM - State of Cold Calling report 2025"
    - "Belkins - B2B cold calling benchmarks 2026 (175,000+ dials)"
    - "FCC - TCPA rules 47 CFR 64.1200 and the 2024 AI-generated voice ruling"
    - "FTC - Telemarketing Sales Rule B2B exemption, 16 CFR 310.6(b)(7)"
    - "State telephone solicitation laws (Florida, Oklahoma, Maryland, Texas)"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md, outbound-compliance-primer.md, list-quality-standard.md, alex-berman-cold-email.md]
---

# Cold Calling

## Overview

This skill produces a cold calling plan a rep can run on Monday: a gated call list with every number typed (business line, direct dial, mobile), call blocks sized to a meeting target, a short script built on opener, reason, question and ask, an objection bank, voicemail and gatekeeper scripts, and the CRM fields that make the funnel measurable.

The mistakes it prevents: dialing a sole proprietor's mobile that sits on the National Do Not Call Registry, running a parallel dialer or an AI voice on cold numbers, calling a Texas plumber at 8:15am, judging a script on 40 dials, and logging calls so loosely that nobody can tell whether the list, the opener or the rep is the problem.

## When to Use

- "Write me a cold call script", "how do I handle 'send me an email'", "what do I say to the gatekeeper".
- "Get phone numbers for this list", "find mobiles for these VPs", "build a call list of roofers in Tampa".
- "Is it legal to call these numbers?", "can we use an AI dialer?", "what hours can we call?".
- "How many dials do we need for 20 meetings?", "our connect rate is 3%".
- Setting up dispositions and call logging in HubSpot, Pipedrive or GoHighLevel.

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Phone as one step in an email, LinkedIn and mail cadence | `multi-channel-outreach` |
| Appending mobiles to a large CRM file | `mobile-appender` |
| Building a local business list without calling it | `local-business-list` |
| Finding the right person at each account | `decision-maker-finder` |
| Picking which accounts to call this week from fresh events | `signal-triggered-outbound` |
| Cost per meeting across channels | `outbound-unit-economics` |
| Answering an email reply that asks for a call | `reply-handling` |

## Prerequisites

1. Market: B2B title list or local business category and geography.
2. Offer and the meeting you are booking (length, who attends).
3. Dialer and how it dials: manual, click-to-call, one-line power dialer. Parallel, predictive, ringless voicemail and AI voice are out for cold numbers (see the gate).
4. Reps, hours available per day, time zones they cover.
5. CRM and whether the dialer logs calls to it.
6. Access to the National Do Not Call Registry (telemarketing.donotcall.gov) or a scrub service, and the company DNC list.
7. ScraperCity plan: Growth ($149/mo) or Scale for the Lead Database and Local Business Database; any plan for `find_mobiles` and the scrapers.

## Authoritative Foundations

| Source | What this skill takes from it |
|-|-|
| Gong Labs, cold call opening lines (90,380 calls, published April 2018) | Baseline success about 1.5%; "the reason for my call is" lifted success 2.1x; "did I catch you at a bad time?" cut it about 40%. |
| Gong Labs with 30 Minutes to President's Club (300M+ calls, July 2024) | "Heard the name tossed around?" 11.24% and a tailored permission opener 11.18% success, against 2.15% for "bad time". Success is not defined on the page; treat as relative. |
| Jeb Blount, telephone prospecting framework (InsideSales interview, Aug 2017) | Name to get attention, identify yourself and why you are calling, give a reason to keep talking, ask, then stop talking. |
| Alex Berman, cold calling techniques | Script the structure and keep the wording flexible; voicemail under 30 seconds with the number said twice; up to five attempts, then move on; mobiles over switchboards; judge on 50+ dials. |
| Cognism and WHAM, State of Cold Calling 2025 | 4.82% conversation-to-meeting in 2024; 93% of conversations happen by the third attempt, 98.6% by the fifth; calls average about 93 seconds. |
| Belkins, B2B cold calling benchmarks (175,000+ dials, 2025) | 9.9% per-dial connect, 58% of connects become conversations, 4.6% of conversations become meetings, about one meeting per 370 dials. |
| FCC, 47 CFR 64.1200 and Declaratory Ruling FCC 24-17 (Feb 2024) | 8am to 9pm window, National DNC with a 31-day scrub, company DNC honored within 10 business days, consent for autodialed or artificial-voice calls to wireless numbers, AI voices count as artificial. |
| FTC, 16 CFR 310.6(b)(7) | Most B2B sales calls are exempt from the Telemarketing Sales Rule, including its DNC provisions. |
| Florida, Oklahoma, Maryland, Texas statutes | Tighter hours (Texas 9am start; Florida, Oklahoma, Maryland 8pm stop), 3 calls per 24 hours caps, broader "automated system" definitions. |

Detail and links: `references/framework-notes.md` and `references/outbound-compliance-primer.md`.

## Workflow

### 1. Choose the motion

| Motion | Who answers | Numbers to use | Booking target |
|-|-|-|-|
| Local business (owner-operated) | Front desk or the owner | Listing `phone`, then `contact_mobile` or a found mobile for the named owner | 15 minute demo or on-site visit |
| SMB B2B (under 50 staff) | Founder or GM | Direct dial or mobile | 20 minute call |
| Mid-market B2B title list | The title holder on mobile; switchboard routes to voicemail | Mobile from `find_mobiles`, then direct dial | 30 minute discovery |

### 2. Build the call list

1. Pull the list (Lead Database, Local Business Database, Google Maps or Yelp) with `hasPhone: true`. Count first with `limit: 1`.
2. Normalize every number to E.164 and keep `phone` (main line) and `mobile` in separate columns (`references/list-quality-standard.md` section 3c).
3. For named contacts with a work email or a LinkedIn URL and no mobile, run `find_mobiles`. You pay $0.25 only when a number is found.
4. Dedupe on E.164 number, then on business name plus postal code. One row per location for local lists.
5. Suppress: company DNC list, open opportunities, customers, anyone who opted out of any channel.

### 3. Gate every number before it reaches a dialer

Run `references/dialing-compliance-gate.md` per number. Short form:

| Check | Pass | Fail |
|-|-|-|
| Dialing method | Rep dials by hand or click-to-call, one line | Parallel, predictive, ringless voicemail, prerecorded or AI voice: block the list |
| Line type | Business landline or VoIP main line | Wireless or unknown: treat as consumer, run the next two checks |
| National DNC (consumer numbers) | Not on a registry copy pulled within 31 days | On the registry: drop unless counsel confirms the B2B exemption for this number |
| Company DNC | Not on your list | On it: drop for 5 years |
| Calling window | 9am to 8pm recipient local time, Monday to Friday (meets federal, Texas, Florida, Oklahoma, Maryland) | Outside: reschedule |
| Attempts | Under 3 to this number in 24 hours, under 6 total | Cap reached: stop |
| Country | US, or Canada with DNCL rules, or UK after TPS and CTPS screening | EU: counsel first |

### 4. Size the call blocks from the meeting target

Work backward from meetings with the funnel in `references/call-blocks-and-metrics.md`:

```
dials needed = meetings / (connect rate x conversation rate x meeting rate)
```

With Belkins' 2025 rates (9.9%, 58%, 4.6%) one meeting needs about 379 dials (1 / (0.099 x 0.58 x 0.046) = 378.6). Treat those rates as the starting hypothesis and replace them with your own after 300 dials per segment.

Default block: 90 minutes, phone only, no email or CRM cleanup inside the block. Two blocks a day for a full-time rep, three for a dedicated SDR. Berman's page puts a trained rep at 40 to 60 targeted calls a day; the funnel decides whether that is enough.

### 5. Write the script

Structure (from Blount and Berman, tuned with Gong's data):

| Part | Length | Job | Rule |
|-|-|-|-|
| Opener | 1 sentence | Name, your name, company | No "bad time?" (Gong: about 40% worse). A permission line is fine. |
| Reason for the call | 1 to 2 sentences | Why them, why now | Start "The reason I'm calling is"; cite one fact from the data (rating, review count, tech, hiring) |
| Question | 1 question | Get them talking about the problem | Open question; avoid "would you be interested" |
| Ask | 1 sentence | Book the meeting | One specific time pair or a 15 minute slot today or tomorrow |

Library and variants: `references/call-scripts-and-objections.md`.

### 6. Handle objections, voicemail and gatekeepers

Use the bank in `references/call-scripts-and-objections.md`: acknowledge, ask one question, then ask again or exit. Voicemail under 30 seconds with the callback number said twice. Gatekeepers get the truth: your name, company, and the reason in one line.

### 7. Run attempts and log every call

Default cadence per number: up to 5 attempts over 10 business days, at different times of day, never more than 2 a day and never 3 in 24 hours. Cognism and WHAM found 93% of conversations by attempt 3 and 98.6% by attempt 5. Log every dial with the disposition list in `references/call-blocks-and-metrics.md`, and move any "don't call me" to the company DNC list the same day.

### 8. Review weekly

Compare each stage rate against the hypothesis. Low connects point at the list or number type, low conversations at the opener, low meetings at the reason or the ask. Change one thing per 300 dials.

## ScraperCity Implementation

| Step | Tool | Parameters | Price |
|-|-|-|-|
| Wallet check | `check_wallet` | none | Free |
| Count and pull B2B contacts with phones | `query_lead_database` | `title`, `seniority`, `minEmployees`, `maxEmployees`, `companyCountry`, `hasPhone: true`, `limit: 100`, `after` | Included in Growth and Scale |
| Count and pull local businesses | `query_local_business_database` | `keyword`, `location`, `category`, `hasPhone: true`, `hasContact: true`, `minReviews`, `limit: 100`, `after` | Included in Growth and Scale |
| Fresh listings outside the database | `scrape_maps` | `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch` | $0.0099 per business |
| Yelp listings | `scrape_yelp` | `searchTerms`, `locations`, `searchLimit` | $0.0099 per result |
| Find mobiles | `find_mobiles` | `inputs`: LinkedIn profile URLs or work emails | $0.25 per number found, free if none |
| Named contact plus mobile at a list of domains | `scrape_website_finder` | `domains`, `jobTitle`, `autoFindMobiles: true` | $0.0499 per contact found; read the run's cost estimate for the added mobile lookups |

MCP calls:

```json
{"tool": "query_local_business_database",
 "keyword": ["roofing contractor"], "location": ["Tampa FL", "St. Petersburg FL", "Clearwater FL"],
 "hasPhone": true, "hasContact": true, "minReviews": 15, "limit": 1}
```

```json
{"tool": "find_mobiles",
 "inputs": ["https://www.linkedin.com/in/example-owner", "owner@exampleroofing.com"]}
```

CLI: `npx scrapercity db-local --keyword "roofing contractor" --location "Tampa FL; Clearwater FL" --has-phone --has-contact --limit 100`, then `npx scrapercity mobile-find --file inputs.txt`, `npx scrapercity poll <runId>`, `npx scrapercity download <runId> -o mobiles-roofers-tampa-20261013.csv`. REST: `POST /api/v1/scrape/mobile-finder` with `{"inputs": [...]}`, then `GET /api/v1/scrape/status/{runId}` and `GET /api/downloads/{runId}`.

Mobile Finder returns `mobile_number`, `status` and `message` per input (scrapercity.com/mobile-finder); read the header row before mapping.

### Worked cost estimate (B2B title list)

Growth plan. Target: VP Sales and Head of Sales at 50 to 200 employee US software companies.

| Line | Count | Unit price | Cost |
|-|-|-|-|
| `query_lead_database` pull with `hasPhone: true` | 600 contacts | Included in Growth | $0.00 |
| `find_mobiles` on 600 work emails (planning assumption: 40% found) | 240 found | $0.25 | $60.00 |
| `find_mobiles` not found | 360 | $0.00 | $0.00 |
| National DNC registry, 5 area codes or fewer | | First five free (FTC FY2027) | $0.00 |
| ScraperCity total | | | $60.00 |

$60.00 is over $5: call `check_wallet`, show this table, and wait for a yes. Ceiling if every input hits: 600 x $0.25 = $150.00. Run 100 inputs first and re-estimate from the real hit rate.

### Worked cost estimate (local business list)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| `query_local_business_database`, roofers in 3 cities, `hasPhone` | 900 businesses | Included in Growth | $0.00 |
| Rows with a named contact and `contact_email` but no `contact_mobile` | 260 | | |
| `find_mobiles` on those emails (planning assumption: 35% found) | 91 found | $0.25 | $22.75 |
| Starter-plan alternative: `scrape_maps` for the same 900 | 900 | $0.0099 | $8.91 |

## Output Format

One Markdown call plan from `templates/output-template.md` with these sections in order: Program Summary, Call List Build, Compliance Gate, Call Blocks, Funnel Targets, Call Script, Objection Bank, Voicemail and Gatekeeper, CRM Logging, Cost Estimate. Every rate in Funnel Targets carries its basis (a named source with date, or "assumption, replace after 300 dials"). When the user asks only for a script, return the Call Script, Objection Bank and Voicemail and Gatekeeper sections.

## Quality Check

`python3 scripts/check-output.py call-plan.md` enforces:

- All ten sections present, no `[fill]` left, at least 30 table rows.
- Every Compliance Gate row names a rule (TCPA, 47 CFR, TSR, DNC, a state, CASL, PECR or internal policy).
- The dialing method is manual or click-to-call, and no plan row allows predictive dialing, prerecorded messages, ringless voicemail or AI voice on cold numbers.
- A calling window with hours is stated.
- The funnel has dials, connects, conversations and meetings, each with a number and a basis.
- At least 8 objections, each response 45 words or fewer and containing a question.
- Every voicemail script is 75 words or fewer (about 30 seconds).
- The cost estimate names `find_mobiles` at $0.25 or states why no mobiles were bought, and has a dollar total.

Also check by reading: the reason for the call cites a real fact from the data; the ask names a time; the B2B vs consumer decision is made for each number separately.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Treating every number on a B2B list as exempt | Owner and personal mobiles are consumer numbers under the DNC rules | Type every number; scrub wireless numbers against the registry |
| Parallel dialer or AI agent on cold mobiles | Autodialer and artificial-voice consent rules; FCC 24-17 covers AI voices | Hand dial or click-to-call, one line per rep |
| Calling Texas at 8am | Texas starts at 9am, Sunday at noon | 9am to 8pm local, weekdays |
| "Did I catch you at a bad time?" | Gong measured about 40% fewer meetings | Name, company, "the reason I'm calling is" |
| Pitching for 60 seconds | The prospect checks out; Blount warns to stop and let them talk | One reason, one question |
| Calling the switchboard for VPs | Routes to voicemail or a gatekeeper | `find_mobiles` on work emails; direct dials |
| Judging a script on a day of dials | 40 dials is noise | 300 dials per segment before changing the opener |
| Logging "called" with no outcome | No way to diagnose list vs opener vs ask | Disposition on every dial, required in the CRM |
| Ignoring "take me off your list" | Company DNC must be honored within 10 business days and kept 5 years | Same-day DNC entry across every tool |
| Calling restaurants at noon | Owners are on the line during service | Use the owner-hours table in `references/call-blocks-and-metrics.md` |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/call-scripts-and-objections.md` | Writing openers, reasons, questions and asks; the objection bank; voicemail and gatekeeper scripts; local business variants |
| `references/dialing-compliance-gate.md` | Gating each number: line type, DNC, hours by state, attempts, dialer settings, gate record |
| `references/call-blocks-and-metrics.md` | Funnel formulas, benchmarks with dates, block schedule, owner hours by vertical, dispositions and CRM fields |
| `templates/output-template.md` | Starting a call plan |
| `examples/worked-example.md` | A full plan for HVAC and plumbing contractors in Dallas-Fort Worth |
| `scripts/check-output.py` | Validating a call plan before handing it over |
| `references/outbound-compliance-primer.md` | TCPA, DNC, state laws, CASL, PECR in full (shared) |
| `references/scrapercity-catalog.md` | Prices and parameters for `find_mobiles`, `scrape_maps`, `scrape_yelp` (shared) |
| `references/scrapercity-platform.md` | Database access by plan, daily allowances (shared) |
| `references/scrapercity-agent-patterns.md` | Wallet check, count first, run lifecycle, CSV naming (shared) |
| `references/list-quality-standard.md` | E.164 phone format, `phone` vs `mobile` columns, dedupe keys (shared) |
| `references/alex-berman-cold-email.md` | Berman's phone and multichannel guidance with sources (shared) |

## Related Skills

- `multi-channel-outreach` places calls inside an email and LinkedIn cadence.
- `mobile-appender` runs `find_mobiles` at CRM scale.
- `local-business-list` and `scrapercity-local-business-database` build the local call list.
- `decision-maker-finder` and `scrapercity-lead-database` find the title holder to call.
- `signal-triggered-outbound` ranks which accounts get called first.
- `outbound-unit-economics` turns the call funnel into cost per meeting.
- `reply-handling` and `cold-email-strategy` cover the email side of the same accounts.
