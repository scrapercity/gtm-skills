---
name: multi-channel-outreach
description: >-
  Builds outbound sequences that combine cold email with phone calls (mobile
  numbers from ScraperCity's Mobile Finder), manual LinkedIn touches and direct
  mail to business or property addresses. Assigns each channel a role, sets the
  weekday and clock time of every touch, writes every touch in full, maps every
  reply type to an action, checks every number against the internal do-not-call
  list and opt-outs, and prices each channel from the ScraperCity catalog. Use when the user asks for a multichannel
  or omnichannel cadence, wants to add calls or LinkedIn to cold email, asks how to
  find mobile numbers for outreach, wants postcards or letters in a sequence, or
  asks which multichannel tool risks a LinkedIn restriction or when to use SMS and WhatsApp.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags:
    - multichannel
    - cold-calling
    - linkedin
    - direct-mail
    - sequences
    - reply-branches
  related_skills:
    - cold-email-strategy
    - cold-email-copywriting
    - reply-handling
    - cold-calling
    - signal-triggered-outbound
    - outbound-unit-economics
    - mobile-appender
    - local-business-list
    - scrapercity-real-estate-data
  frameworks:
    - "Alex Berman - email opens the door, phone closes; six-touch email, call and LinkedIn sequence; call windows"
    - "Alex Berman - CEO first, then one level down (Lean B2B interview)"
    - "LinkedIn - User Agreement and prohibited software policy"
    - "LinkedIn - Sales Navigator plans and InMail credit policy"
    - "Overloop - LinkedIn invitation pacing (July 2026)"
    - "Google and Yahoo - bulk sender requirements (one-click unsubscribe, 2-day processing, 0.3% spam rate)"
    - "HubSpot - sequence unenrollment settings and task steps"
    - "Gong Labs - cold call opening lines (90,380 calls, 2018) and multithreading"
    - "Ryan Reisert - Buckets method, daily run order and meeting confirmations"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - cold-email-frameworks.md
    - alex-berman-cold-email.md
---

# Multi-Channel Outreach

## Overview

This skill produces a day-by-day cadence where each channel has a job: email carries the offer and the proof, the phone call turns interest into a meeting, LinkedIn makes the sender's name familiar, and a postcard or letter reaches a physical desk. Every touch has a day offset and weekday, a clock time in the recipient's zone, copy written out in full, a skip branch and a cost; the standing checks are stated once. Every reply type and call outcome has a row that says what stops, who answers, how fast and the words to send. The sequencer setup is written as settings a team can turn on today.

The mistakes it prevents: buying and calling every mobile number Mobile Finder returns before tiering; calling someone who already said no on another channel; dialing from a caller ID that carriers have labeled spam; LinkedIn automation or invitation volume that gets the seat restricted; handing reps touches that say "see the copy doc"; and spending $0.25 per mobile number on contacts who will never be called.

## When to Use

- "Add calls and LinkedIn to this cold email sequence."
- "Build a multichannel cadence for [segment]."
- "Find mobile numbers for these leads so my SDRs can call them."
- "Should we send postcards to these [dentists, roofers, property owners]?"
- "Which of these numbers should we call, and when?" (run the phone check, then hand off to `cold-calling`).

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Email-only campaign plan | `cold-email-strategy` |
| Email copy | `cold-email-copywriting` |
| Call scripts, objection handling on the phone, dialer setup | `cold-calling` |
| Appending mobiles to a CRM at scale | `mobile-appender` |
| Property owner lists and skip tracing | `scrapercity-real-estate-data`, `skip-tracer` |
| Cost per meeting across channels | `outbound-unit-economics` |

## Prerequisites

1. The email campaign plan (cells, offer, touch map) or enough to write one.
2. Who will call: in-house reps, hours available per day, dialer, and the caller ID numbers each rep dials from.
3. LinkedIn: which seats send, Sales Navigator or not, and a commitment to manual sending.
4. Direct mail: budget per piece, a print and mail vendor, and whether the address is a business or a residence.
5. The sequencer and CRM the team uses, so the stop rule and LinkedIn and call steps are written as that tool's settings.
6. Recipient time zones, so every call lands in Berman's call windows in the recipient's local time.
7. Deal value, close rate from a meeting, and the meeting rate per contact the user expects for each tier, so the break-even per contact decides which channels each tier gets.
8. The offer's public price or price range and what moves it, and one true proof point, so every touch can be written in full. With no price, the price answer uses `{{price_range}}` and the top note asks for it; with no proof point, the copy goes without one; never invent a result.
9. The user's own settings: list size and start date (without them, the dated launch is a labelled worked example), the email send window and the re-contact date for "not now" replies that give no date.

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, cold calling article on alexberman.com | A six-touch sequence over two weeks: email day 1, call with voicemail day 2, LinkedIn day 3, call day 5, email day 8, final call with a breakup day 12. Stack dials Tuesday to Thursday (Wednesday and Thursday book best); call 8 to 10 AM or 4 to 5 PM local, never 12 to 2 PM. 40 to 60 targeted calls a day. Voicemail under 30 seconds; the opener has 8 to 10 seconds. A mobile can double the connect rate over a switchboard. Most prospects take five or more attempts; past five with no engagement, move on. Meeting ask: a 20 minute call with two slots. |
| Roundup on alexberman.com ("Manual Outbound Wins") | Email opens the door and the phone closes; about two hours of calling a day. |
| Alex Berman, Lean B2B interview and Single Grain video | Start with the CEO; if there is no reply in one to two weeks, go one level down. Emailing several people at one company at once can get you blocked company wide. |
| Alex Berman, follow-up and templates pages | Reply to interest within 5 minutes; other replies within 2 to 4 business hours; no quote, proposal or price sheet by email, move pricing to a call; cold emails under 75 words; keep hard bounces under 2%; stop the sequence on a reply. |
| Scott D. Clary on Berman's early agency playbook (HackerNoon, 2021) | Calls after the email sequence, to people who engaged without replying, with a short voicemail asking whether they saw the email. |
| LinkedIn User Agreement section 8.2 and the "Prohibited software and extensions" help page | LinkedIn bars third-party software, bots and extensions that scrape or automate activity on the site, and may restrict accounts that use them. It keeps the weekly invitation limit unpublished. |
| Overloop, LinkedIn limits (July 2026) | About 100 invitations a week on a rolling 7 days (community estimate); 10 to 25 a day in small batches; withdraw invitations older than 3 to 4 weeks with no response, since a large pending pile is a known restriction trigger. |
| Google and Yahoo bulk-sender rules | One-click unsubscribe, unsubscribes processed within 2 days, spam complaint rate under 0.3%; inbox placement depends on them. |
| Gong Labs, cold call opening lines (90,380 calls, April 2018) | "Did I catch you at a bad time?" made a booked meeting about 40% less likely; "the reason for my call is" lifted success 2.1x. |
| Gong, "The data-backed guide to multi-threading" (checked 2026-10-13) | Closed-won deals include 67% more contacts than closed-lost deals. |
| LinkedIn Help, read through dated write-ups (Contentin, EmailAnalytics, Promiseclick; July to September 2026) | A withdrawn invitation blocks a re-invite for up to 3 weeks; free accounts get a few notes a month (reported as three, though LinkedIn's pages conflict); notes run 200 characters, up to 300 on some Premium surfaces. |
| LinkedIn Sales Navigator compare-plans page (checked 2026-10-13), Valley (31 August 2026) and the InMail policy post | Core $119.99 a month or $1,079.88 a year per seat; Core includes 50 InMail credits a month; a credit returns when the recipient responds within 90 days. |
| HubSpot Knowledge Base, sequences (checked 2026-10-13) | Reply and meeting unenrollment for "All contacts at the company" and "Unenroll contacts from the same company"; call task and Sales Navigator connection request and InMail task steps; workflow unenrollment on Enterprise. |
| Ryan Reisert, "Buckets" (GTMnow, November 2021) | Work the day backwards from booked meetings to new names; confirm each booked meeting a week out by phone, 12 to 24 hours out by email, and 2 to 3 hours out by phone when the email got no reply; no-shows go back to the Priority bucket. |
| Hunter, State of Cold Email 2025 | Decision makers surveyed preferred cold email (61%) over LinkedIn (29%) and calls (10%), so email stays the lead channel. |

## Workflow

### 1. Assign channel roles

| Channel | Role | Best for | Weak for |
|-|-|-|-|
| Email | Carries the offer, proof and the first ask | Every segment | Owners who do not read the inbox on file |
| Phone (mobile or direct dial) | Converts engaged or high-value contacts into meetings; a mobile can double the connect rate (Berman) | Owners, founders, finance and ops leaders in tiers whose break-even covers the calls | Large enterprises reached only through a switchboard |
| Phone (main line) | Reaches the front desk; asks for the person by name | Local businesses and smaller companies | Reaching a named executive at scale |
| LinkedIn (manual) | Familiarity: profile view, connection, short note, InMail when not connected | Every contact with a LinkedIn URL | Contacts with no LinkedIn URL |
| Direct mail | Pattern break that reaches a physical desk | Local owners, property owners, the signer at high-value accounts | Remote teams, tiers whose break-even does not cover a piece |
| SMS | Meeting confirmation and reminders after the prospect asks to text; no WhatsApp | Prospects who reply "text me" | Any first touch |

One rep owns every channel for an account, so the stop rule works: a reply on any channel reaches the person who stops the other channels. Rules: `references/channel-operating-rules.md` section 3c.

Tools that run several channels, rated against LinkedIn's terms (vendor pages and help centers, 2026-10-13; detail in `references/channel-operating-rules.md` section 3a):

| Tool | Price | LinkedIn steps | LinkedIn risk |
|-|-|-|-|
| lemlist Multichannel | $109 per user a month ($87 yearly) | Sent by lemlist unless each step is marked manual before launch | Medium; Low only if reps do every LinkedIn task by hand in LinkedIn |
| Reply.io Multichannel | $99 per user a month ($89 annual) | Manual or automatic per step | Medium; Low if all manual |
| Smartlead | $39 to $94 a month for email plans | Through the HeyReach integration (January 2026) | High for LinkedIn; fine as the email sender |
| La Growth Machine | €60 to €120 per identity a month | Cloud automation with mobile proxies | High |
| HeyReach | $79 per sender a month ($63 yearly) | Automated, proxy per sender | High |
| Expandi | $99 a month ($79 annual) | Cloud automation | High |
| Outreach or Salesloft | Not published | Rep completes LinkedIn tasks (Outreach); Sales Navigator Application Platform member (Salesloft) | Low |

Plans from this skill use Low-risk LinkedIn touches only. The deliverable names only the tools the plan uses; this comparison goes into a "Tool Choice" section only when the user asked which tool to pick.

### 2. Decide which contacts get which channels, and thread the account

Spend on the expensive channels only where the deal value pays for it. Break-even per contact = deal value x close rate from a meeting x meeting rate per contact, from the user's numbers; a tier gets a channel only when its cost per contact (`references/channel-cost-model.md` section 5) stays under that break-even.

| Tier | Rule | Channels |
|-|-|-|
| A | Break-even covers email, calls, LinkedIn and a mail piece; top accounts by fit, or engaged on email (replied with a question) | Email, mobile or direct-dial call, LinkedIn, letter |
| B | Break-even covers email, calls and LinkedIn | Email, direct-dial or main-line call, LinkedIn |
| C | Break-even covers email only | Email only |

Promote to tier A on a dated trigger. For buyers around public money (contractors, engineering firms, suppliers), free non-ScraperCity sources supply the trigger: new federal awards on USAspending.gov, state DOT bid tabulations, and job postings for the role your product supports; for any segment, Sales Navigator's "Changed jobs in past 90 days" on the buyer title. Carry the trigger's own fields onto the row (`award_agency`, `award_project`, `posted_role`) so the copy names the award or the role, and write one copy code per trigger type. Recipes: `references/channel-scripts-and-cadences.md` section 10.

Every contact with a LinkedIn URL gets the connection request. Sales Navigator signals (posted in the past 30 days, changed jobs in the past 90 days, follows your company) only set the order: those contacts go first in the day's 10 to 25 requests (section 6c of the scripts reference).

Thread the account the way Berman does: start with the senior person (CFO, owner) and go one level down (controller, ops manager) only when the senior person has not replied in one to two weeks; he warns that emailing several people at one company at once can get you blocked company wide. In the default cadence the second person starts on day 16, the Tuesday after the senior person's last touch, so the two threads never overlap, and a reply from either stops both. Rules: `references/channel-scripts-and-cadences.md` section 11.

### 3. Run the phone check before buying or dialing numbers

For every number, in order. Any "no" removes the phone touch for that contact. Full checklist: `references/channel-operating-rules.md` section 1.

1. Is the number on your internal do-not-call list, or has the person opted out on any channel? Drop it. An email unsubscribe also stops calls and mail, the same day.
2. Has the person had 3 calls this cadence (the three calls in Berman's sequence)? Stop. Past five attempts with no engagement, Berman moves on to fresh names.
3. Is it inside Berman's call windows in the recipient's local time: 08:00 to 10:00 or 16:00 to 17:00, Tuesday to Thursday for the heavy blocks, never 12:00 to 14:00? Otherwise reschedule.
4. Is the caller ID the rep dials from labeled spam on carrier apps? Swap or fix the number first; pickups collapse once it is labeled.

### 4. Build the day-by-day cadence

Default 14 business day cadence for tier A, adapted from the six-touch sequence on Berman's cold calling page with a mail piece and more LinkedIn touches added. Day 1 is a Tuesday so every call lands Tuesday to Thursday; times are the recipient's local time. The email send window is the user's setting; test it against reply rates. The cadence is day offsets; dates belong to the launch calendar.

Checks, stated once above the table: one-click unsubscribe on every email; the phone check (step 3) before every call block; every LinkedIn touch done by hand in LinkedIn.

| Day | Time | Channel | Touch | Skip when |
|-|-|-|-|-|
| 1 (Tue) | Send window | Email | E1: fact, proof, question | Email not `valid` or `valid_catch_all`: skip every email touch |
| 1 (Tue) | Rep's LinkedIn block | LinkedIn | View profile | No LinkedIn URL: skip every LinkedIn touch |
| 3 (Thu) | 08:00 to 10:00 | Phone | Call 1, voicemail V1 referencing the email | No number passed the check: main line with the front-desk script, or skip every call |
| 4 (Fri) | Send window | Email | E2 in thread: new proof | Hard bounce on E1: skip the rest of email |
| 5 (Mon) | Rep's LinkedIn block | LinkedIn | L1 connection request, note under 200 characters; free seat sends it without a note | Already connected: skip to day 9 |
| 7 (Wed) | 16:00 to 17:00 | Phone | Call 2 at the other window, no voicemail | Reached on call 1 and asked for email: skip |
| 8 (Thu) | Arrives (mailed day 3) | Direct mail | Postcard or letter, one code per trigger or persona | Tier B or C, or no deliverable address: skip |
| 9 (Fri) | Send window | Email | E3: references the mail piece | Connection accepted since day 5: send L2 in LinkedIn on this day instead (accept-skips-email). No mail piece: second proof |
| 11 (Tue) | Rep's LinkedIn block | LinkedIn | Connected and L2 sent: voice note VN1. Connected after day 9: L2. Not connected and a Sales Navigator seat: one InMail I1 | Not connected on a free or Premium seat: skip |
| 12 (Wed) | 08:00 to 10:00 | Phone | Call 3 with breakup voicemail | Spoke on an earlier call: skip the voicemail |
| 14 (Fri) | Send window | Email | E4: breakup | None; last touch |
| Meeting minus 5 business days | 08:00 to 10:00 | Phone | Confirmation call; ask the buyer to bring the operational owner | Meeting booked under a week out: ask on the booking call |
| Meeting minus 24 hours | Send window | Email | One-line confirmation in the invite thread | Rescheduled: move to the new date |
| Meeting minus 2 to 3 hours | Meeting time minus 2 hours | Phone | Reminder call | They replied to the 24 hour email: skip |

LinkedIn volume per seat stays under the community estimate of about 100 invitations a week on a rolling 7 days, sent 10 to 25 a day in small batches; invitations pending 3 to 4 weeks are withdrawn (Overloop, July 2026). One InMail per person: I1 is a single touch.

Stop rules: any reply on any channel stops every prospecting touch for that person and their company (Berman: stop the sequence on a reply; confirmation touches for a booked meeting still run); an opt-out on one channel is an opt-out on all, the same day. A contact who finishes with no reply re-enters only with a new dated trigger and new copy, never the same sequence again. Every touch has a skip branch so a contact missing a LinkedIn URL, a callable number or an address moves forward instead of stalling. SMS enters only after a reply that asks to text, as a confirmation touch; plans do not use WhatsApp.

### 4b. Write the sequencer setup

Write the stop rule, the LinkedIn rows and the call rows as settings in the user's sequencer. With no tool named, use HubSpot sequences, whose settings are documented in `references/channel-operating-rules.md` section 8: reply and meeting unenrollment set to "All contacts at the company" plus "Unenroll contacts from the same company"; "Sales Navigator - Connection request task" and "InMail task" steps for LinkedIn; "Call task" steps for calls; the rep unenrolls the contact when a call reaches a conversation (a workflow can do it on Enterprise).

### 5. Write every touch in full

A rep should be able to send every row without opening another document.

- Email: subject and full body for every email, under 75 words (Berman's templates page), one question, merge fields for name and company with a fallback (`{{first_name|there}}`) plus the trigger's own fields on trigger variants ("congratulations on the {{award_project}} award from {{award_agency}}", never "the new public work"). An email mentions another channel only when that touch happened (section 13 of the scripts reference).
- One copy code per trigger and persona (E1p and M1p for a public award, E1h and M1h for a hiring post). Never one body that says "X, or Y" to cover two cases.
- Calls and voicemails: opener, voicemail per call and front-desk line, from `references/channel-scripts-and-cadences.md`; hand dialer setup and coaching to `cold-calling`.
- Openers: never "Did I catch you at a bad time?" (Gong: about 40% less likely to book). Name and company, then "The reason I'm calling is...".
- LinkedIn: L1 under 200 characters so it fits every seat, L2 one line and one question, the InMail and the voice note written out word for word. Free seats get a few notes a month, so plan them with no note; notes at volume need Premium or Sales Navigator (Core $119.99 a month, 50 InMail credits).
- Pricing questions in a reply: one line with the user's public price or range and what moves it (or `{{price_range}}` when the user has not given one), then a 20 minute call with two times. No quote, proposal or price sheet by email (Berman's templates page).
- Mail: the full letter or postcard text, one offer, one URL or phone number and the rep's signature.

### 6. Map every reply and call outcome

Build the branch table from `references/channel-scripts-and-cadences.md` section 8: interested, accepts a time, price question, "send me something", forwarded internally, referral, wrong person or left, not now, uses a competitor, not interested, opt-out, angry, out of office, hard bounce, LinkedIn accepted and LinkedIn reply, and each call outcome (meeting agreed, prospect returns a call or voicemail, callback request, front desk, voicemail, wrong number), plus a request to text. Each row names the action on every channel, the owner and response time (5 minutes for hot replies and 2 to 4 business hours for the rest, from Berman's follow-up guide and templates page), and the text to send. Branch on replies, acceptances and call outcomes; never on email opens, which Apple Mail Privacy Protection inflates.

### 7. Confirm every booked meeting and set the daily run order

A booked meeting gets three confirmation touches from the same rep (Reisert): a call about a week out, an email 24 hours before, and a call 2 to 3 hours before when the email got no reply. The week-out call asks the buyer to bring the operational owner, the person who runs the process day to day; Gong found closed-won deals include 67% more contacts than closed-lost deals. Each rep works the day in this order: confirmations, replies and callbacks, cadence calls in the two call windows, LinkedIn tasks, then the phone check on tomorrow's contacts. Scripts: `references/channel-scripts-and-cadences.md` sections 9 and 12.

### 8. Price every channel, show the estimate and track

Use the cost model below. Get approval before any pull over about $5, and run `check_wallet` first. Record which channel produced each first positive response; report meetings, cost per meeting and connect or acceptance rate per channel, with a decision rule for each, and feed the numbers to `outbound-unit-economics`.

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
| Validate emails before the email touches | `validate_emails` | `emails` | $0.00169 per email |

Order of operations to avoid wasted spend: pull the list, validate emails, tier the contacts, run the phone check on tier A and B, then call `find_mobiles` only for contacts who passed it and have no `contact_mobile` already.

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

Mobile Finder bills only on a hit, so the table shows the ceiling (every lookup found). Replace it with the expected cost after a 50-input Mobile Finder test (at most $12.50) measures the hit rate on this list.

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Local Business Database pull with `hasPhone`, `hasEmail` | 400 | included on Growth | $0.00 |
| `validate_emails` | 400 | $0.00169 | $0.68 |
| Owners already carrying `contact_mobile` | 120 | included | $0.00 |
| `find_mobiles` on the other 280, ceiling | 280 | $0.25 per number found | $70.00 |
| Postcards to 400 business addresses, all-in print and postage | 400 | $1.50 (top of directmail.io's $0.85 to $1.50 small-volume range, April 2026) | $600.00 |
| ScraperCity data subtotal | | | $70.68 |
| Total including mail | | | $670.68 |

Callable mobiles after the check = 120 + numbers found - matches on the internal do-not-call list and opt-outs. Owners without a callable mobile get business-line calls asking for them by name. Show this table and get approval before `find_mobiles` (it passes $5) and before the mail order.

## Output Format

One Markdown plan built from `templates/output-template.md`, with these `##` sections in order and no others: Summary, Channel Roles, Contact Tiers, Cadence, Tool Setup, Reply Branches, Channel Copy, Launch and Cost, Tracking. Add "Tool Choice" only when the user asked which multichannel tool to use.

- Top: the title, one sentence naming stand-ins to replace (product, reps, numbers, `{{price_range}}`), and one "Not checked:" line with everything assumed or not verified. Say it there once; nowhere else repeats "assumed".
- Summary: four sentences at most. The sequence first (tiers, channels, length, threading), then the launch it was sized for, the cost, and the spend to approve.
- Channel Roles: one row per channel used. Claims about how the segment behaves (who opens mail, who answers the phone) appear only as what a Tracking metric tests.
- Cadence: day offsets, not dates. One "Checks:" line above the table holds the standing checks once; the table has Tier, Day, Time, Channel, Touch (with its copy code), Owner and Skip when, plus the three confirmation rows. Under it: account owner per tier, stop rule, LinkedIn branch, a "LinkedIn volume:" line, and the daily run order ending with one line on the caller ID spam-label check.
- Tool Setup: three to five lines of settings in the named sequencer.
- Reply Branches: a row for every reply type and call outcome with the action on every channel, owner and response time, and the text to send ("None" when nothing is sent). The price row answers with a figure or `{{price_range}}`.
- Channel Copy: every code used in the cadence, written word for word, one code per trigger or persona. Emails as "Subject: ... Body: ..." under 75 words; no brackets or blanks.
- Launch and Cost: the dated cohort calendar, the data pull in two or three sentences, and the cost table with product names (Mobile Finder, Email Validator, B2B Lead Database), counts, unit prices and a total; rep-time lines name the user's inputs. Without a user list size or start date, the first line labels it a worked launch for the stated test size.
- Tracking: each metric with the decision it triggers; bounce and complaint limits live here only.

The reader receives the deliverable only, with each fact or check stated once. Leave out internal file paths, reference section numbers, tool ids, skill names, "Next:" handoff lines, checklists, self-scores, quality check sections, tools the plan does not use, tool risk ratings, and any law, regulator, registration or consent requirement.

## Quality Check

`python3 scripts/check-output.py plan.md` enforces:

- The nine sections in order and no others (Tool Choice optional); one "Not checked:" line above Summary; "assumed" at most four times; no table cell of 40 or more characters repeated more than three times.
- A "Checks:" line above the cadence table naming the unsubscribe and the do-not-call list and opt-outs, and no Check column; no calendar dates inside Cadence; a caller ID line.
- Every cadence row has a day, a clock time, a copy code found in Channel Copy (profile views excepted), an owner and a skip branch; no connection request skipped for lack of a LinkedIn signal.
- Every email copy row has a subject and a body of 75 words or fewer (Berman's cap); no bracket placeholders; no copy that covers two cases with "X, or Y"; trigger tiers have copy with trigger merge fields.
- Reply Branches has at least 12 rows covering interested, price, referral, forwarded, wrong person, not now, competitor, not interested, opt-out, angry, out of office and bounce; with phone rows, also voicemail, front desk, wrong number and a returned call; the price row carries a figure or `{{price_range}}`.
- SMS rows run only after the prospect asks to text; LinkedIn touches are manual; a plan with connection requests states the accept-skips-email branch and a LinkedIn volume of 100 or fewer per seat per week.
- Tool Setup names the company-level stop on reply and, with LinkedIn rows, the task steps.
- One owner per tier across every channel; at least three channels; a stop rule; confirmation rows at a week, 24 hours and 2 to 3 hours, one asking for the operational owner.
- Launch and Cost has cohort dates, per-channel lines, a total, Mobile Finder at $0.25 per number found and Sales Navigator Core at $119.99 a month.
- No "bad time" opener, legal or registration term, internal path, section number, tool id, skill name, "Next:" line, LinkedIn automation tool, risk rating, checkbox list or quality check section.

Also confirm by reading:

- Calls fall in Berman's windows, 08:00 to 10:00 and 16:00 to 17:00 recipient local time, Tuesday to Thursday where the cohort calendar allows.
- No more than 3 calls per cadence to one person.
- The second person at an account starts only after the first person's touches end, and only if the first has not replied.
- Every number and rate is from the catalog, a dated source or the user's own inputs; rates not yet measured are stated as the user's hypotheses.
- Mobile Finder runs only after tiering and the phone check.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Buying mobiles for every contact | $0.25 per found number on contacts who never get called | Tier first; mobiles for tier A and B only |
| Dialing from a caller ID carriers label as spam | Pickups collapse once the label shows | Check each number's label; swap or fix it as soon as it is labeled |
| Calling someone who said no on another channel | The dials are wasted and the account is lost | One suppression list and internal do-not-call list across every channel, applied the same day |
| Calling at lunch | Berman: 12 to 2 PM local is the weakest window | 08:00 to 10:00 and 16:00 to 17:00 recipient local time |
| LinkedIn automation tools | LinkedIn prohibits third-party automation and restricts accounts that use it | Manual views, requests and messages; Medium-risk tools with every LinkedIn step set to manual |
| 50 connection requests in one morning from one seat | LinkedIn restricts accounts that send many invitations quickly; Overloop paces 10 to 25 a day | 10 to 25 a day, under about 100 a week per seat; withdraw requests pending 3 to 4 weeks |
| Connection requests only to profiles with a LinkedIn signal | Contacts without a signal never get L1, L2 or the voice note, though the weekly volume had room | L1 to every contact with a URL; signals only set the order |
| "Congratulations on the new public work" | The trigger email reads as generic because it never names the trigger | Merge the trigger's own fields: "the {{award_project}} award from {{award_agency}}" |
| One letter or email that says "X, or Y" | A rep has to rewrite it before sending | One copy code per trigger and persona |
| "I'd rather walk you through it than send a sheet" | A buyer who asked a direct question gets no answer | One line with the public range and what moves it, then two times |
| The same check repeated in every row, a separate limits table, a "Next:" line | The plan is longer than the work it describes | Checks once above the table; limits in Tracking only; no handoffs to other skills |
| SDR calls, AE emails, marketing mails the postcard | A reply on one channel never reaches the person running the others, so the stop rule fails | One rep owns every channel for the account |
| CFO and controller emailed the same week | Berman: several people at one company at once can get you blocked company wide | Senior person first; one level down only after that thread ends with no reply |
| Branching on "email not opened" | Apple Mail Privacy Protection records opens that never happened | Branch on replies, LinkedIn acceptance and call outcomes |
| Touches that say "see copy doc" | The rep improvises or skips the touch | Every code written in full in Channel Copy |
| Reply handling left as "route to the reply team" | Hot replies wait past Berman's 5 minutes; opt-outs miss a channel | A branch row per reply type with action, owner, response time and text |
| Cadence without skip branches | A contact missing a LinkedIn URL or a phone number waits on a touch that cannot fire | A skip rule on every row |
| Channel keeps going after a reply elsewhere | The next touch lands mid-conversation | One stop rule across every channel, set as the sequencer's company-level unenrollment |
| "Did I catch you at a bad time?" | Gong measured about 40% fewer booked meetings | "The reason I'm calling is...", then ask for 30 seconds |
| Notes on every request from a free seat | Free accounts get only a few personalized notes a month | Premium or Sales Navigator for notes at volume, or no note |
| Emailing a price sheet after "what does it cost?" | Berman: no quote, proposal or price sheet by email | One line with the range, then a short call with two times |
| Booking and never confirming | No-shows erase the dials and emails that booked them | Week-out call, 24 hour email, 2 to 3 hour call (Reisert) |
| Meeting with only the executive | Gong: closed-won deals include 67% more contacts than closed-lost deals | Ask the buyer to bring the operational owner |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/channel-operating-rules.md` | The phone check and caller ID labels, LinkedIn volume and tool risk ratings, voice notes, one rep per account, mail rules, email footer, suppression record, SMS rules, sequencer setup (HubSpot settings) |
| `references/channel-scripts-and-cadences.md` | Cadences with weekdays and times, openers and voicemails, pricing answers, 2026 LinkedIn limits and the order of requests, InMail, mail copy, the reply and outcome branch table, confirmations, threading a second person at an account, the daily run order, email jobs per touch, trigger sources |
| `references/channel-cost-model.md` | Per-channel cost tables and cost per touch from catalog prices |
| `templates/output-template.md` | Starting a multichannel plan |
| `examples/worked-example.md` | A full plan for CFOs and controllers at Texas trucking carriers, CFO first and the controller after |
| `scripts/check-output.py` | Validating a plan |
| `references/cold-email-frameworks.md` | Email framework per cell (shared) |
| `references/alex-berman-cold-email.md` | Berman's phone and sequence guidance with sources (shared) |
| `references/scrapercity-catalog.md` | Tool ids and prices (shared) |
| `references/scrapercity-platform.md` | Plans and database fields (shared) |

## Related Skills

- `cold-email-strategy` and `cold-email-copywriting` set the email strategy and copy rules this skill writes to.
- `cold-calling` owns scripts, dialer setup and call coaching.
- `reply-handling` owns reply classification, response times and the full response library once someone engages.
- `mobile-appender` appends mobiles at CRM scale with the same phone check.
- `local-business-list` and `scrapercity-real-estate-data` supply addresses for mail.
- `signal-triggered-outbound` decides which contacts deserve tier A.
- `outbound-unit-economics` compares cost per meeting by channel.
