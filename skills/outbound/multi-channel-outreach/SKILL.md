---
name: multi-channel-outreach
description: >-
  Builds outbound sequences that combine cold email with phone calls (mobile
  numbers from ScraperCity's Mobile Finder), manual LinkedIn touches and direct
  mail to business or property addresses. Assigns each channel a role, sets day
  by day timing, gates every phone touch on TCPA and Do Not Call checks, and prices
  each channel from the ScraperCity catalog. Use when the user asks for a multichannel
  or omnichannel cadence, wants to add calls or LinkedIn to cold email, asks how to
  find mobile numbers for outreach, or wants postcards or letters in a sequence.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [multichannel, cold-calling, linkedin, direct-mail, sequences, tcpa]
  related_skills: [cold-email-strategy, cold-email-copywriting, reply-handling, cold-calling, signal-triggered-outbound, outbound-unit-economics, mobile-appender, local-business-list, scrapercity-real-estate-data]
  frameworks:
    - "Alex Berman - email opens the door, phone closes; 12 day email, call and LinkedIn sequence"
    - "FCC - TCPA rules, 47 CFR 64.1200"
    - "FTC - Telemarketing Sales Rule and National Do Not Call Registry"
    - "FCC - 2024 declaratory ruling on AI-generated voices in robocalls"
    - "Florida Telephone Solicitation Act (2021 amendments)"
    - "FTC - CAN-SPAM Act compliance guide"
    - "LinkedIn - User Agreement and prohibited software policy"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, cold-email-frameworks.md, alex-berman-cold-email.md, outbound-compliance-primer.md]
---

# Multi-Channel Outreach

## Overview

This skill produces a day-by-day cadence where each channel has a job: email carries the offer and the proof, the phone call turns interest into a meeting, LinkedIn makes the sender's name familiar, and a postcard or letter reaches owners who never read cold email. Every touch has a channel, a day, a script or copy reference, a compliance gate and a cost. Phone touches only run on numbers that pass a TCPA and Do Not Call check.

The mistakes it prevents: calling every mobile number Mobile Finder returns without checking the Do Not Call registry or the calling window; firing an autodialer or an AI voice at cell phones without consent; sending LinkedIn automation that breaks LinkedIn's terms; and spending $0.25 per mobile number on contacts who will never be called.

## When to Use

- "Add calls and LinkedIn to this cold email sequence."
- "Build a multichannel cadence for [segment]."
- "Find mobile numbers for these leads so my SDRs can call them."
- "Should we send postcards to these [dentists, roofers, property owners]?"
- "Is it legal to call these numbers?" (run the gate, then hand off to `cold-calling` and the compliance primer).

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Email-only campaign plan | `cold-email-strategy` |
| Email copy | `cold-email-copywriting` |
| Call scripts, objection handling on the phone, dialer setup | `cold-calling` |
| Appending mobiles to a whole CRM | `mobile-appender` |
| Property owner lists and skip tracing | `scrapercity-real-estate-data`, `skip-tracer` |
| Cost per meeting across channels | `outbound-unit-economics` |

## Prerequisites

1. The email campaign plan (cells, offer, touch map) or enough to write one.
2. Who will call: in-house reps, hours available per day, dialer (manual, power, parallel).
3. Whether any call will use an autodialer, prerecorded message or AI voice. If yes, the plan needs documented prior express consent for every cell phone, which cold lists do not have, so those touches are removed.
4. LinkedIn: which seats send, Sales Navigator or not, and a commitment to manual sending.
5. Direct mail: budget per piece, a print and mail vendor, and whether the address is a business or a residence.
6. Recipient states and countries (Florida, Oklahoma and other states add rules; Canada and the EU change the email and phone rules).

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, cold calling article on alexberman.com | A roughly 12 day sequence mixing a personalized email, a call with voicemail, a LinkedIn connection, a second call at another time, a follow-up email with new value and a final call with a breakup. Direct mobile lines reach decision makers faster than switchboards. Tuesday to Thursday are the strongest calling days. |
| Roundup on alexberman.com ("Manual Outbound Wins") | Email opens the door and the phone closes; about two hours of calling a day. |
| Scott D. Clary on Berman's early agency playbook (HackerNoon, 2021) | Calls after the email sequence, to people who engaged without replying, with a short voicemail asking whether they saw the email. |
| 47 CFR 64.1200(a)(1)(iii) (FCC, TCPA) | No autodialed or artificial or prerecorded voice calls to cell phones without prior express consent. |
| 47 CFR 64.1200(c)(1), (c)(2), (e) | No telephone solicitations to residential subscribers before 8am or after 9pm local time, or to numbers on the national DNC registry; applied to wireless numbers. |
| FTC Telemarketing Sales Rule Q&A | Most calls to a business to sell to that business are exempt from the DNC provisions; registry access must be refreshed at least every 31 days; fines up to $53,088 per violation. |
| FCC declaratory ruling, February 2024 | AI-generated voices count as "artificial" voices under the TCPA. |
| Florida Telephone Solicitation Act, 2021 amendments | Calls 8am to 8pm, no more than 3 calls per person per topic in 24 hours; texts and voicemail count. |
| Texas Business and Commerce Code 301.051 | No telephone solicitation before 9am on weekdays and Saturdays, or before noon on Sundays. |
| FTC CAN-SPAM guide | Email touches keep the opt-out and postal address. |
| LinkedIn User Agreement and prohibited software help page | LinkedIn bars third-party software that automates activity on the site, and keeps the weekly invitation limit unpublished. |
| Hunter, State of Cold Email 2025 | Decision makers surveyed preferred cold email (61%) over LinkedIn (29%) and calls (10%), so email stays the lead channel. |

## Workflow

### 1. Assign channel roles

| Channel | Role | Best for | Weak for |
|-|-|-|-|
| Email | Carries the offer, proof and the first ask | Every segment | Owners who do not read the inbox on file |
| Phone (mobile) | Converts engaged or high-value contacts into meetings | Local business owners, founders, deal values over $2,000 | Large enterprises with gatekeepers and strict policies |
| Phone (business line) | Reaches the front desk; asks for the owner | Local businesses | Reaching a named executive |
| LinkedIn (manual) | Familiarity: profile view, connection, short note | B2B titles active on LinkedIn | Local owners, trades |
| Direct mail | Pattern break that reaches a physical desk | Local owners, property owners, high-value accounts | Remote teams, low deal values |

### 2. Decide which contacts get which channels

Spend on the expensive channels only where the deal value pays for it.

| Tier | Rule | Channels |
|-|-|-|
| A | Top accounts by fit, deal value over $5,000, or engaged on email (replied with a question, clicked) | Email, mobile call, LinkedIn, letter |
| B | Good fit, deal value $1,000 to $5,000 | Email, business line or mobile call, LinkedIn |
| C | Everyone else | Email only |

### 3. Run the phone gate before buying or dialing numbers

For every number, in order. Any "no" removes the phone touch for that contact. Full checklist: `references/channel-compliance-gates.md`.

1. Will the call use an autodialer, prerecorded message or AI voice? If yes and there is no prior express consent: no call.
2. Is the number a mobile? Treat Mobile Finder results as mobile.
3. Is the call a solicitation to a business about that business's needs? Most such calls are exempt from the federal DNC provisions under the FTC rule, but a mobile can be personal. Scrub mobiles against the National DNC Registry (refreshed every 31 days) and your internal DNC list; drop matches unless your counsel has cleared a business-use exemption.
4. Is the recipient in a state with stricter rules (Florida: 8am to 8pm, 3 calls per 24 hours)? Texas starts at 9am. Apply the strictest window that covers the list: 9am to 8pm recipient local time.
5. Has the contact opted out on any channel? An email unsubscribe also stops calls and mail.

### 4. Build the day-by-day cadence

Default 14 business day cadence for tier A, adapted from the sequence on Berman's cold calling page:

| Day | Channel | Touch | Gate |
|-|-|-|-|
| 1 | Email | Touch 1: fact, proof, question | CAN-SPAM footer |
| 1 | LinkedIn | View profile (manual) | Manual only |
| 3 | Phone | Call 1, voicemail referencing the email | Phone gate passed |
| 4 | Email | Touch 2 in thread: new proof | Same |
| 5 | LinkedIn | Connection request, no pitch, under 200 characters | Manual only |
| 7 | Phone | Call 2 at a different time of day, no voicemail | Phone gate; 3 per 24h max |
| 8 | Direct mail | Postcard or letter lands (mailed day 3) | Business address or owner opt-out check |
| 9 | Email | Touch 3: references the mail piece | Same |
| 11 | LinkedIn | Message if connected: one line, one question | Manual only |
| 12 | Phone | Call 3 with breakup voicemail | Phone gate |
| 14 | Email | Touch 4: breakup | Same |

Stop rules: any reply on any channel stops every channel for that person and their company; an opt-out on one channel is an opt-out on all.

### 5. Write channel copy

- Email: from `cold-email-copywriting`.
- Calls and voicemails: scripts in `references/channel-scripts-and-cadences.md`; hand deeper call work to `cold-calling`.
- LinkedIn: connection notes under 200 characters, no link, no pitch in the request.
- Mail: one offer, one URL or phone number, a handwritten-style note for tier A.

### 6. Price every channel and show the estimate

Use the cost model below. Get approval before any pull over about $5, and run `check_wallet` first.

### 7. Track by channel

Record which channel produced each positive conversation. Report meetings per channel, cost per meeting per channel, and contacts reached only by phone or mail. Feed the numbers to `outbound-unit-economics`.

## ScraperCity Implementation

| Need | Tool | Parameters | Price |
|-|-|-|-|
| Mobile numbers from work emails or LinkedIn URLs | `find_mobiles` | `inputs: ["dana@northpaw.example", "https://www.linkedin.com/in/..."]` | $0.25 per number found, free if not found |
| Mobiles while finding contacts on company domains | `scrape_website_finder` | `domains`, `jobTitle`, `autoValidateEmails: true`, `autoFindMobiles: true` | $0.0499 per contact found, plus mobile lookups |
| Business phone and street address | `query_local_business_database` | `category`, `location`, `hasPhone: true`; returns `phone`, `address`, `city`, `state`, `postal_code`, and `contact_mobile` for many named contacts | Included on Growth ($149/mo) and Scale |
| Business listings with phone from Maps | `scrape_maps` | `searchStringsArray`, `locationQuery` | $0.0099 per business |
| B2B contacts with phone | `query_lead_database` | `hasPhone: true` plus title and company filters | Included on Growth and Scale |
| Property details and owner contact for mail to owners | `scrape_property_lookup` | `addresses`, `includeOwnerContact: true` | $0.15 per property, +$0.10 for owner contact |
| Distressed properties for owner mail | `scrape_distress_list` | `search`, `distressTypes`, `maxItems` | $0.05 per property |
| LinkedIn profile URLs for manual touches | `query_lead_database` | `socialUrl` match, or read profile fields returned | Included on Growth |
| Validate emails before the email touches | `validate_emails` | `emails` | $0.0072 per email |

Order of operations to avoid wasted spend: pull the list, validate emails, tier the contacts, run the phone gate on tier A and B, then call `find_mobiles` only for contacts who passed the gate and have no `contact_mobile` already.

```json
{
  "tool": "find_mobiles",
  "inputs": [
    "maria@lakelinefamilydental.example",
    "tom@hillcountryplumbing.example"
  ]
}
```

CLI: `npx scrapercity mobile-find`. REST: `POST /api/v1/scrape/mobile-finder`, poll `/api/v1/scrape/status/{runId}`, download the CSV.

### Worked cost estimate (400 tier A local business owners)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Local Business Database pull with `hasPhone`, `hasEmail` | 400 | included on Growth | $0.00 |
| `validate_emails` | 400 | $0.0072 | $2.88 |
| Owners already carrying `contact_mobile` | 120 | included | $0.00 |
| `find_mobiles` on the other 280 (assume 40% found) | 112 found | $0.25 | $28.00 |
| Mobiles removed by DNC scrub (assume 15% of 232) | 35 removed | $0.00 | $0.00 |
| Postcards to 400 business addresses, all-in print and postage | 400 | $1.20 (directmail.io small-volume range $0.85 to $1.50, April 2026) | $480.00 |
| ScraperCity data subtotal | | | $30.88 |
| Total including mail | | | $510.88 |

Callable mobiles after the gate: 120 + 112 - 35 = 197. The other 203 owners get business-line calls asking for them by name. Show this table and get approval before `find_mobiles` (it passes $5) and before the mail order.

## Output Format

One Markdown plan built from `templates/output-template.md`, with these `##` sections in order: Summary, Channel Roles, Contact Tiers, Cadence, Compliance Gates, Channel Copy, Data and Cost, Tracking. The Cadence table has one row per touch with day, channel, touch, owner and gate. Phone rows name the law they are gated by.

## Quality Check

`python3 scripts/check-output.py plan.md` enforces:

- Every phone or SMS touch row names a gate citing TCPA, DNC or a state law.
- No touch uses an autodialer, prerecorded message or AI voice without the word "consent" in its gate.
- Every LinkedIn touch is marked manual.
- The cost table has a per-channel line and a $ total, and Mobile Finder is priced at $0.25 per number found.
- The cadence uses at least three channels and has a stop rule.

Also confirm by reading:

- Calls fall between 9am and 8pm recipient local time on weekdays.
- No more than 3 calls to one person in 24 hours (Florida cap applied everywhere).
- Mobile Finder runs only after tiering and the gate.
- Mail to a residence (property owners) follows the owner-contact rules in `references/channel-compliance-gates.md`.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Buying mobiles for every contact | $0.25 per found number on contacts nobody calls | Tier first; mobiles for tier A and B only |
| Parallel dialer or AI voice to cell phones | Autodialed or artificial voice calls to cells need prior express consent under the TCPA; AI voices count as artificial | Manual or click-to-call dialing, a live rep, no prerecorded drops without consent |
| Skipping the DNC scrub because "it's B2B" | A mobile can be personal; the B2B exemption depends on the call and the number | Scrub mobiles every 31 days; keep an internal DNC list |
| Calling at 8:30pm in Miami | Florida's window ends at 8pm | 8am to 8pm recipient local time everywhere |
| LinkedIn automation tools | LinkedIn prohibits third-party automation; accounts get restricted | Manual views, requests and messages |
| Same message on every channel | Feels like spam from three directions | Each channel has its own job and copy |
| Channel keeps going after a reply elsewhere | Reads as a bot; complaint risk | One stop rule across every channel |
| Postcard with three offers | The reader acts on none | One offer, one URL or number |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/channel-compliance-gates.md` | Running the TCPA, DNC, state, LinkedIn and mail checks for a list |
| `references/channel-scripts-and-cadences.md` | Cadences by segment, voicemail and call openers, LinkedIn notes, mail copy |
| `references/channel-cost-model.md` | Per-channel cost tables and cost per touch from catalog prices |
| `templates/output-template.md` | Starting a multichannel plan |
| `examples/worked-example.md` | A full plan for HVAC contractors in Dallas-Fort Worth |
| `scripts/check-output.py` | Validating a plan |
| `references/cold-email-frameworks.md` | Email framework per cell (shared) |
| `references/alex-berman-cold-email.md` | Berman's phone and sequence guidance with sources (shared) |
| `references/scrapercity-catalog.md` | Tool ids and prices (shared) |
| `references/scrapercity-platform.md` | Plans, database fields and compliance boundaries (shared) |
| `references/outbound-compliance-primer.md` | Full TCPA, DNC, CAN-SPAM, CASL and GDPR detail (shared) |

## Related Skills

- `cold-email-strategy` and `cold-email-copywriting` own the email touches.
- `cold-calling` owns scripts, dialer setup and call coaching.
- `reply-handling` owns responses on every channel once someone engages.
- `mobile-appender` appends mobiles at CRM scale with the same gate.
- `local-business-list` and `scrapercity-real-estate-data` supply addresses for mail.
- `signal-triggered-outbound` decides which contacts deserve tier A.
- `outbound-unit-economics` compares cost per meeting by channel.
