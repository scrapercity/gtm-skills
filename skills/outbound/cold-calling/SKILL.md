---
name: cold-calling
description: >-
  Builds a B2B or local-business cold calling program: a call list from
  ScraperCity phone fields and find_mobiles, dial order by number type, dialer
  and caller ID setup that keeps pickups high, call blocks with a dials-to-meetings funnel, an opener-reason-question-ask
  script, an objection bank, voicemail and gatekeeper scripts, and CRM logging.
  Use when the user asks for a cold call script, a calling plan, phone numbers
  for a list, connect-rate fixes, "Spam Likely" labels, or objection handling.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.2.0"
  author: ScraperCity
  category: outbound
  tags:
    - cold-calling
    - phone
    - caller-id
    - dialer
    - objection-handling
    - voicemail
    - sdr
    - local-business
  related_skills:
    - multi-channel-outreach
    - reply-handling
    - cold-email-strategy
    - signal-triggered-outbound
    - outbound-unit-economics
    - mobile-appender
    - local-business-list
    - decision-maker-finder
    - scrapercity-lead-database
    - scrapercity-local-business-database
  frameworks:
    - "Gong Labs - cold call opening lines (90,380 calls, 2018)"
    - "Gong Labs with 30 Minutes to President's Club (Armand Farrokh, Nick Cegelski) - opener study of 300M+ calls (2024)"
    - "Jeb Blount - telephone prospecting framework, Golden Hours and Law of Replacement (Fanatical Prospecting)"
    - "Joey Gilkey and TitanX - completed conversations and conversation outcomes"
    - "Ryan Reisert - Buckets work order and meeting confirmations"
    - "Ronen Pessar - cold call stages and discovery questions"
    - "Tom Slocum (The SD Lab) - selling the meeting"
    - "Steve Richard - 3x3 Research"
    - "ATIS-1000074 - STIR/SHAKEN caller ID attestation; Free Caller Registry; Hiya on call labels"
    - "Alex Berman - cold calling techniques"
    - "Cognism and WHAM - State of Cold Calling report 2025"
    - "Belkins - B2B cold calling benchmarks 2026 (175,000+ dials)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
    - list-quality-standard.md
    - alex-berman-cold-email.md
---

# Cold Calling

## Overview

This skill produces a cold calling plan a team can run on Monday: a dated launch checklist with owners, a call list with every number typed (business line, direct dial, mobile), call blocks and an attempt cadence sized to a meeting target, a short script built on opener, reason, stake, question and ask, a typed objection bank, voicemail and gatekeeper scripts, CRM fields, and a scorecard where every metric has a target and an action threshold.

The mistakes it prevents: calling the switchboard when the owner's mobile was on file, dialing all week from a number that shows "Spam Likely", dialing between 12 and 2pm (the window Berman says almost everyone avoids), pitching something outside the offer, booking meetings with people who do not own the decision, promising emails nobody wrote, judging a script on 40 dials, and logging calls so loosely that you cannot tell whether the list, the opener or the rep is the problem.

## When to Use

- "Write me a cold call script", "how do I handle 'send me an email'", "what do I say to the gatekeeper".
- "Get phone numbers for this list", "find mobiles for these VPs", "build a call list of roofers in Tampa".
- "Click-to-call or a parallel dialer?", "what hours get the most connects?", "our number shows as Spam Likely".
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
2. Offer, in the user's words: what is sold and what is not. The plan never adds a product line the user did not name.
3. The meeting you are booking (length, who attends).
4. Dialer and CRM by product name, and how the dialer dials: click-to-call, one-line power dialer or a parallel dialer (step 3). If the user names none, ask; the plan names the product it is written for.
5. Reps, hours available per day, time zones they cover.
6. The company's own records: past one-time customers, lapsed customers, lost deals and quotes, demos that did not buy.
7. The company's internal do-not-call list (everyone who ever asked not to be called).
8. ScraperCity plan: Growth ($149/mo) or Scale for the Lead Database and Local Business Database; any plan for `find_mobiles` and the scrapers.

## Authoritative Foundations

| Source | What this skill takes from it |
|-|-|
| Gong Labs, cold call opening lines (90,380 calls, published April 2018) | Baseline success about 1.5%; "the reason for my call is" lifted success 2.1x; "did I catch you at a bad time?" cut it about 40%. |
| Gong Labs with 30 Minutes to President's Club (300M+ calls, July 2024) | "Heard the name tossed around?" 11.24% and a tailored permission opener 11.18% success, against 2.15% for "bad time". Success is not defined on the page; treat as relative. |
| Jeb Blount, telephone prospecting framework (InsideSales interview, Aug 2017) | Name to get attention, identify yourself and why you are calling, give a reason to keep talking, ask, then stop talking. |
| Jeb Blount, *Fanatical Prospecting* (Wiley, 2015) | Protect the Golden Hours for prospecting; the Law of Replacement: pipeline that closes or is lost must be refilled. |
| Joey Gilkey, TitanX (B2B Playbook ep. 192, Sept 2025; TitanX newsletter, Apr 2026) | Measure completed conversations; every conversation ends in one outcome; Not Me and Referred by title show where the message or list misses. |
| Ryan Reisert, "Buckets" (GTMnow, Nov 2021) | Work Scheduled, then Priority, then Working, then Uncontacted; confirm meetings a week out, 12 to 24 hours out, and 2 to 3 hours out. |
| Ronen Pessar (Sell Better; The Sales Doctor ep. 43; Triple Session) | Pick-up, conversation, interest, meeting; qualify with a present-tense closed question; confirm the invite before hanging up. |
| Tom Slocum, The SD Lab | The cold call earns the meeting; summarize the problem, say what the meeting covers, ask for one step. |
| Steve Richard, 3x3 Research (Call Camp, Apr 2016) | Three insights in three minutes before the dial. |
| ATIS-1000074; Free Caller Registry; Hiya (Aug 2023) | STIR/SHAKEN attestation levels, free number registration with the carrier analytics engines, labels follow calling behavior. |
| Readymode, avoiding spam flags (June 2025); Kixie, avoiding "Scam Likely" (June 2023) | Readymode recommends limiting outbound volume to 75 calls per day per number and holding enough numbers to spread it; it is a recommendation, so the plan sets its own cap in whatever dialer it names. Kixie: do not call the same person several times a day. |
| HubSpot Knowledge Base (checked 2026-10-13) | Default call outcomes (Busy, Connected, Left live message, Left voicemail, No answer, Wrong number); up to 30 custom outcomes under Settings, Calling, Call Configurations, Track call outcomes, on Sales Hub or Service Hub Professional and Enterprise. |
| Alex Berman, cold calling techniques (page dated Aug 2026) | Script the structure and keep the wording flexible; voicemail under 30 seconds with the number said twice; up to five attempts over about two weeks, then move on; mobiles over switchboards; read rates over 50+ dials; avoid 12 to 2pm, late afternoon (4 to 5pm) picks up better. |
| Cognism and WHAM, State of Cold Calling 2025 | 4.82% conversation-to-meeting in 2024; 93% of conversations happen by the third attempt, 98.6% by the fifth; calls average about 93 seconds. |
| Belkins, B2B cold calling benchmarks (175,000+ dials, 2025) | 9.9% per-dial connect, 58% of connects become conversations, 4.6% of conversations become meetings, about one meeting per 370 dials. |

Detail and links: `references/framework-notes.md`.

## Workflow

### 1. Choose the motion

| Motion | Who answers | Numbers to use | Booking target |
|-|-|-|-|
| Local business (owner-operated) | Front desk or the owner | Listing `phone`, then `contact_mobile` or a found mobile for the named owner | 15 minute demo or on-site visit |
| SMB B2B (under 50 staff) | Founder or GM | Direct dial or mobile | 20 minute call |
| Mid-market B2B title list | The title holder on mobile; switchboard routes to voicemail | Mobile from `find_mobiles`, then direct dial | 30 minute discovery |

### 2. Build the call list

0. Start with the company's own records: past one-time customers, lapsed customers, lost deals or quotes, demos that did not buy. They are Reisert's Priority bucket (he puts deals lost in the last 2 to 3 quarters there), get dialed first, and the reason line cites their own date ("we fixed your unit on March 3rd").
1. Pull the list (Lead Database, Local Business Database, Google Maps or Yelp) with `hasPhone: true`. Count first with `limit: 1`. Keywords cover every category of the market the user named (for "independent restaurants": full-service, bar and grill, cafe, each cuisine), not a sample. Add a filter the user did not ask for (a review band, a size band) only when the plan states in one clause what it changes for this offer.
2. Normalize every number to E.164 and keep `phone` (main line) and `mobile` in separate columns (`references/list-quality-standard.md` section 3c).
3. For named contacts with a work email or a LinkedIn URL and no mobile, run `find_mobiles`. You pay $0.25 only when a number is found.
4. Dedupe on E.164 number, then on business name plus postal code. One row per location for local lists.
5. Suppress: internal do-not-call list, open opportunities, customers, anyone who opted out of any channel.
6. Find the warmest public signal for this offer. When the offer fixes something customers complain about, pull review text (Maps and Yelp scrapes return reviews; read the header row first), match complaint words to the stake (for HVAC: "hot inside", "AC was out"), move those records to Priority and put the review date in the reason line. When the offer depends on who owns the asset (a tenant vs the landlord, a franchisee vs the franchisor), add that as the Qualify question in the script (Workflow step 5) and as a filter wherever the data carries it.
7. Add fresh openings. A `minReviews` floor drops businesses that opened in the last few months, and new owners are buying now. Pull a second list with `maxReviews: 10`, match it to free state and local permit, license, inspection, sales-tax or appraisal records, and cite the record's date in the reason for the call. These are non-ScraperCity sources. Source types, the trigger each implies and a verified Texas set: `references/public-records-triggers.md`.
8. Set the dial order by reachability: owner mobile, then direct dial, then main line (Berman: moving from switchboard to mobile can double the connect rate), and inside each, records with a fresh trigger or a past connect first.
9. With two or more reps, split the list so each rep owns their records: by territory (and the matching local caller IDs) or by tier. Write a "Rep split:" line with the counts.
10. Before the first block, hand-check a random sample of records: the number reaches the business, the named contact matches, the business is open. Write the sample size and the failure count that sends the filter back for a fix into the plan.

### 3. Set up the dialer and caller ID

Settings in `references/dialer-and-caller-id.md`. Short form:

| Setting | Value |
|-|-|
| Dial mode | Click-to-call or a one-line power dialer for tier A accounts and mid-market titles. A parallel dialer for large local lists where conversations per hour decide the result; it dials several lines at once, so it needs more numbers |
| Voicemail | Rep-left and specific to the record (V1 to V3); drops recorded once are reused only on parallel lists |
| Caller ID | Local numbers you own that ring back to the rep, registered with the Free Caller Registry, A attestation, test calls to AT&T, Verizon and T-Mobile phones on a schedule the plan sets |
| Number volume | Planned dials per number per day, at or under the 75 a day per number Readymode recommends (June 2025); numbers per rep = planned daily dials / 75, rounded up. In the plan, cite it as Readymode's recommendation, never as a limit of the user's dialer |
| Window | Berman's windows: 9 to 11am blocks, late afternoon (4 to 5pm) for better pickups, nothing from 12 to 2pm; for local owners, the hours the front desk gives you |
| Attempts | Up to 5 over about two weeks (Berman), one a day per person at most (Kixie) |
| Removed numbers | Anyone who said "don't call" or "remove me" comes off every list the same day |

Write each setting as a value the rep types into the named dialer (calls per number per day, attempts per number per day, maximum attempts, voicemail mode, which numbers each rep holds), not as a description.

### 4. Size the call blocks from the meeting target

Work backward from meetings with the funnel in `references/call-blocks-and-metrics.md`:

```
dials needed = meetings / (connect rate x conversation rate x meeting rate)
```

With Belkins' 2025 rates (9.9%, 58%, 4.6%) one meeting needs about 379 dials (1 / (0.099 x 0.58 x 0.046) = 378.6). Treat those rates as the starting hypothesis and replace each with your measured rate once the segment has the sample the plan sets (Berman reads rates over 50+ dials at minimum).

Blocks: phone only, no email or CRM cleanup inside the block; block length and count come from the reps' available hours. Berman's page puts a trained rep at 40 to 60 targeted calls a day; the funnel decides whether that is enough, and dials per hour are measured in week 1.

Block policy (Blount, *Fanatical Prospecting*): blocks sit in the Golden Hours when buyers answer, go on the calendar as busy, and survive a good week. Under his Law of Replacement every opportunity that closes or is lost has to be replaced, so next week's block count does not drop after a win. Research, email and CRM cleanup go in the admin slots.

Work order inside the day (Reisert's buckets): confirm Scheduled meetings first, then Priority callbacks (Activated, Not Now due, no-shows), then Working records in cadence, then new records. Detail and CRM filters: `references/call-blocks-and-metrics.md` sections 4a and 4b.

### 5. Write the script

Structure (from Blount and Berman, tuned with Gong's data):

| Part | Length | Job | Rule |
|-|-|-|-|
| Opener | 1 sentence | Name, your name, company | No "bad time?" (Gong: about 40% worse). A permission line is fine. |
| Stake | Inside the reason or question | The costliest equipment or risk in their business | One noun the owner already worries about; logged in the plan |
| Reason for the call | 1 to 2 sentences | Why them, why now | Start "The reason I'm calling is"; cite one fact from the data (rating, review count, tech, hiring) |
| Question | 1 question | Get them talking about the problem | Open question; avoid "would you be interested" |
| Ask | 1 sentence | Book the meeting | One specific time pair or a 15 minute slot today or tomorrow |

Name the stake. Before writing the reason for a segment, decide what the most expensive thing is that can break, sit idle or go wrong for this buyer this month that the seller's offer fixes, and put it in the reason or the question. The stake comes from inside the offer as the user stated it: an HVAC maintenance seller calling restaurants names a rooftop unit failing over a full dining room on a 100 degree Friday, not the walk-in cooler, unless the user said they service refrigeration. Confirm it on the first 10 conversations. Examples by seller and buyer: `references/call-scripts-and-objections.md` section 2h.

Write every script line, voicemail and email with merge fields from the list columns ({owner_first}, {business}, {rating}, {review_count}, {city}, {trigger_date}), so reps never rewrite a sample record. Name the column each field comes from in the "Source of the fact" cell.

Before each dial, 3x3 research (Steve Richard): three insights in three minutes covering the account, the person and why now, written into the call notes. On local lists the record already carries the account facts.

If they engage, follow Pessar's beats: confirm the right person, then a Qualify line: a present-tense closed question that confirms this person owns and pays for what the offer covers ("Are the rooftop units on you or the landlord under your lease?", "Do you sign off on the office software?"); a no gets "who does?" and a Not Me or Referred log, not a booking. Then one or two open questions with a pause after each, then sell the meeting the way Slocum describes it: repeat the problem in their words, say what 15 minutes will show, offer two times, and confirm the invite while they are on the line.

Tonality: Pessar sets tone by role, warm for people-facing roles and confident and crisp for technical ones (Mixmax interview, 2023). Berman gives the opener 8 to 10 seconds before the prospect checks out, so name, company and reason come first.

Library and variants: `references/call-scripts-and-objections.md` (section 0 for 3x3, section 2g for discovery).

### 6. Handle objections, voicemail and gatekeepers

Use the bank in `references/call-scripts-and-objections.md`: acknowledge, ask one question, then ask again or exit. Each objection carries a type (value, timing, competition, authority, status quo, trust, access, stop) and the outcome to log if they hold firm, so the weekly review can count them. Once one objection type leads the count, answer it inside the reason or the voicemail and test that as one lever. Voicemail under 30 seconds with the callback number said twice (Berman). Gatekeepers get your name, company and the reason in one line; the rep asks the gatekeeper's name and when the owner is in, logs both, and books the callback at that time.

Every email, text and confirmation the plan mentions is written out in full with a subject and merge fields (E1 to E3 for the cadence, C1 and C2 for confirmations), in the same table as the voicemails. A cadence cell names the message ID; it never says "send an email" without the copy. Templates: `references/call-scripts-and-objections.md` section 4a and `references/call-blocks-and-metrics.md` section 10.

### 7. Run attempts and log every call

Cadence per number: up to 5 attempts over about two weeks (Berman), one attempt a day per person at most (Kixie, June 2023), rotated across morning and afternoon blocks, rep-left voicemail on some attempts with a same-day email. Write the attempt days into the plan (`references/call-blocks-and-metrics.md` section 4c). Cognism and WHAM found 93% of conversations by attempt 3 and 98.6% by attempt 5. Log every dial with the disposition list in `references/call-blocks-and-metrics.md`, and move any "don't call me" to the internal do-not-call list the same day.

Every conversation also gets one outcome, using the labels from Gilkey's and TitanX's framing: Meeting Scheduled, Activated, Not Now, Not Me, Referred, Not Interested. Referred names go through `find_mobiles` or `find_emails` and into list v2. Every Meeting Scheduled gets the invite confirmed while the prospect is on the line (Pessar), then Reisert's confirmations: a call about a week out, an email 12 to 24 hours before, and a call 2 to 3 hours before if the email got no reply. The plan writes the confirmation text and email (C1, C2) in full. After attempt 5 with no conversation, the record closes for the cycle (Berman: past five attempts, fresh targets pay better); if the user wants an email-only follow-up, the plan writes those emails too.

### 8. Run the dated 2-week pilot

Every plan starts with a 2-week pilot on calendar dates. Week 1 runs the plan as written as the baseline. Week 2 changes exactly one lever (list, opener, reason or stake, ask, or calling window). Before day 1, the plan writes down the conversation count each week needs before a verdict and the lift in conversation-to-meeting that keeps the variant. On the last day, apply those rules (`references/call-blocks-and-metrics.md` section 7d); if connects run far below the Belkins 9.9% planning rate, fix the list or number type before judging any script change.

### 9. Review weekly

Compare each stage rate against the hypothesis. Low connects point at the list, the number type or a caller ID label; low conversations at the opener; low meetings at the reason or the ask. Change one lever per test. A large share of Not Me plus Referred is a list or title problem (TitanX read about 32% in one Director-level example that way, April 2026): change the title filter and feed referrals into list v2. Fill the Rep Scorecard every Friday against the targets in `references/call-blocks-and-metrics.md` section 9a, cut by segment, rep, number type and block. The same Friday, the manager scores a sample of recorded calls per rep, gives one keep and one fix, and the rep role-plays the fix before Monday (section 13).

### 10. Prove calling works before hiring

Before hiring an SDR, the founder or first seller runs the motion and measures cost per held meeting = (hours x loaded hourly cost + data + dialer) / held meetings. Hire when conversation-to-meeting is at or above the Belkins 4.6% planning rate and cost per held meeting is at or below cold email's (`outbound-unit-economics`). Below that, keep email primary and use the phone for Priority callbacks and replies that ask for a call. Detail: `references/call-blocks-and-metrics.md` section 11.

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
| `find_mobiles` on 600 work emails, ceiling if every input returns a number | up to 600 found | $0.25 | up to $150.00 |
| `find_mobiles` inputs with no number | rest of the 600 | $0.00 | $0.00 |
| ScraperCity total | | | up to $150.00 |

Over $5: call `check_wallet`, show this table, and wait for a yes (an agent step before the run; it stays out of the plan). The hit rate is not published, so run a first batch, measure found / inputs, and re-estimate the rest as remaining inputs x hit rate x $0.25.

### Worked cost estimate (local business list)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| `query_local_business_database`, roofers in 3 cities, `hasPhone` | 900 businesses | Included in Growth | $0.00 |
| Rows with a named contact and `contact_email` but no `contact_mobile` | 260 | | |
| `find_mobiles` on those emails, ceiling | up to 260 found | $0.25 | up to $65.00 |
| Starter-plan alternative: `scrape_maps` for the same 900 | 900 | $0.0099 | $8.91 |

## Output Format

One Markdown call plan from `templates/output-template.md`. It opens with one header line (company and offer in the user's words, market, reps, dialer and CRM by name, plan period) and the Program Summary, so the answer comes first. Sections in this order:

| Section | What it holds |
|-|-|
| Program Summary | Motion, the meeting and who runs it, meeting target, reps and dialing hours, calling window with hours, then one "Estimates:" line naming which counts are estimates |
| Launch Checklist | Every task before the first dial with an owner and a YYYY-MM-DD date: own-records export, list pull, removed-numbers list loaded in the dialer, caller ID registration and test calls, CRM fields, calendar blocks, script role-play |
| Call List Build | Step 0 own records, then source, filters in plain words and rows after each step; paid steps priced inline (Mobile Finder at $0.25 per number found); dial order, "Rep split:" line, spot-check |
| Dialer Setup | Dial mode, voicemail, caller ID numbers per rep and their test schedule, calls per number per day, window, attempts, removed numbers, each as a value |
| Call Blocks | Block times, work order, the attempt cadence table whose email column names message IDs |
| Funnel Targets | One table: dials, connects, conversations, meetings, held and cost per held meeting, each with rate, basis (dataset name and year, "measured" or "assumption"), count, and an "Act if" cell holding both the threshold and the change |
| Call Script | Opener, reason, stake, question and ask with merge fields, then the if-they-engage beats including Qualify |
| Objection Bank | 8 to 15 rows: type, objection, a response of 45 words or fewer that asks a question, and what to log if they hold firm |
| Voicemail, Gatekeeper and Email | V1 to V3 at 75 words or fewer, gatekeeper lines that capture the gatekeeper's name and owner hours, every cadence email (E rows with a subject) and the confirmation text and email (C rows), all in full |
| CRM Logging | Dispositions, the six conversation outcomes, required fields by property name and where they are set in the named CRM |
| Pilot Plan | Two dated weeks, one lever, decision rules with thresholds |
| Rep Scorecard | Blank actuals columns per rep, filled each Friday, and the weekly call review in one line |

Add a Cost Estimate section only when the user asked about cost, budget or cost per meeting; otherwise the paid data line is priced in Call List Build and cost per held meeting is a measured Funnel Targets row.

When the user asks only for a script, return the Call Script, Objection Bank and the Voicemail, Gatekeeper and Email sections.

What the reader receives is the deliverable only:

- The offer exactly as the user stated it. The stake, script, voicemails and emails sell only that.
- ScraperCity products by name (Local Business Database, Mobile Finder) with filters in plain words. Tool ids, API paths, CLI commands, file paths, skill names and this skill's section numbers stay out; where another routine would run, write its steps.
- Instructions without the names of trainers or frameworks (no "Berman's window", "Reisert's buckets", "3x3"). Published datasets are cited by name and year in a Basis cell (Belkins 2025, Cognism 2025); vendor recommendations as recommendations (Readymode recommends 75 calls per number per day).
- No agent process: no wallet checks, approval gates, "not run" or "not checked" lists. One "Estimates:" line covers every estimate. Absence of data is written as "none found", never "none exists".
- Each fact once: targets live in Funnel Targets only, the scorecard holds actuals, symptoms and fixes live in the "Act if" cells, no second diagnosis table, no restated dates.
- A full plan runs 900 to 4,000 words.

## Quality Check

`python3 scripts/check-output.py call-plan.md` enforces:

- All twelve sections present, no `[fill]` left, at least 30 table rows, 900 to 4,000 words.
- No tool ids, CLI commands, file paths, skill names, trainer or framework names, agent process lines (wallet, approval, "not checked"), or "no ... exists" claims; exactly one "Estimates:" line.
- Every Launch Checklist row has an owner and a YYYY-MM-DD date; a plan with two or more reps has a "Rep split:" line in Call List Build.
- Dialer Setup names the dial mode, caller ID numbers with a test schedule, the window with hours, and the attempt cap.
- The plan carries no legal content.
- Funnel Targets is one table; dials, connects, conversations and meetings each have a count and a basis, and every stage after dials has an "Act if" with a number.
- The Call Script has opener, reason, stake, question and ask rows, at least two merge fields and a Qualify beat.
- The Pilot Plan spans 7 to 16 calendar days, every row has a date, and each row changes at most one lever and carries a decision rule.
- At least 8 objections, each response 45 words or fewer and containing a question.
- Every voicemail script is 75 words or fewer: Berman's 30 seconds at the 150 words a minute the National Center for Voice and Speech gives for US conversation (cited by Voices.com).
- Every email the cadence names is a written row with a subject; a confirmation message (C row) is written.
- Mobile Finder, wherever used, is priced at $0.25 per number found; a Cost Estimate, if present, has dollar figures and a total.
- The Rep Scorecard has every required column, no "target" rows, and any filled row's rates match its counts within rounding.

Also check by reading: the stake and every message sell only the offer the user named; the reason cites a fact from the data; the keywords cover every category of the market the user named; the Qualify line tests who owns the asset or budget; the ask names a time; every number is typed before it is dialed; caller ID numbers show no label on the latest test; every price is current on the plan date.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Parallel dialer on tier A accounts | The pickup delay costs the opener on accounts you cannot replace | Click-to-call for tier A; parallel only for large local lists |
| "Did I catch you at a bad time?" | Gong measured about 40% fewer meetings | Name, company, "the reason I'm calling is" |
| Pitching for 60 seconds | The prospect checks out; Blount warns to stop and let them talk | One reason, one question |
| Calling the switchboard for VPs | Routes to voicemail or a gatekeeper | `find_mobiles` on work emails; direct dials |
| Judging a script on a day of dials | 40 dials is under Berman's 50+ dial minimum | Set the sample per segment in the plan before changing the opener |
| Logging "called" with no outcome | No way to diagnose list vs opener vs ask | Disposition on every dial, required in the CRM |
| Tool ids, CLI commands and file paths in the plan | The owner cannot act on them and the plan grows | Product names and filters in plain words |
| Filtering on `minReviews` only | New openings have no reviews yet, so the filter drops the owners who are buying now | Second pull with `maxReviews: 10`, matched to permit and license records |
| A generic benefit in the reason | Nothing ties the call to what the owner worries about | Name the stake: their costliest equipment or risk |
| No dated pilot | Changes pile up and no week can be compared with another | 2-week pilot on calendar dates, one lever in week 2 |
| Dialing from 12 to 2pm | Berman calls it the one window almost everyone agrees to avoid | Morning and late-afternoon blocks; logged owner hours for local lists |
| Rotating fresh numbers when one gets "Spam Likely" | Labels follow calling behavior, so new numbers pick them up too, and callbacks break | Register numbers, fix the behavior, dispute the label (`references/dialer-and-caller-id.md` section 4) |
| Hiring an SDR before anyone has booked from the phone | The new hire inherits an unproven list and script | Workflow step 10: founder-run calls measured against the Belkins rate and email's cost per meeting first |
| Booking and never confirming | Each no-show wastes the roughly 379 dials that booked it at Belkins' 2025 rates | Reisert's week-of call, 24 hour email, 2 to 3 hour call |
| Admin and email inside call blocks | Dialing time goes to admin | Golden Hours policy; admin slots around the blocks |
| A stake outside the offer (the walk-in cooler for an HVAC-only seller) | Every touch pitches something the company does not sell | Stake from the offer as the user stated it |
| Booking before qualifying who owns the asset | Meetings land with tenants whose landlord maintains the equipment | Qualify beat before selling the meeting; filter where the data allows |
| Script written for one sample record | Reps rewrite it on every call | Merge fields from the list columns |
| "I'll send you an email" with no email written | The rep improvises or skips it | E and C rows written in full; cadence cells name the ID |
| Skipping the company's own records | The warmest names (past one-time customers, lost deals) never get called | List step 0, dialed first |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/call-scripts-and-objections.md` | 3x3 pre-call research; openers, reasons, questions and asks; the stake by vertical; discovery beats and selling the meeting; the typed objection bank, pre-handling and delivery; voicemail and gatekeeper scripts; local business variants |
| `references/dialer-and-caller-id.md` | Typing each number and the dial order; dial mode and dialer settings; windows, dials per number and attempt caps; caller ID attestation, registration, monitoring and the label runbook; the ready-to-dial record |
| `references/call-blocks-and-metrics.md` | Funnel formulas, benchmarks with dates, calling windows by source, block policy, bucket work order and Working size, attempt cadence, dispositions, conversation outcomes, the 2-week pilot, CRM fields, rep scorecard with targets, no-show runbook, prove-before-hiring comparison, weekly call review |
| `references/public-records-triggers.md` | Finding fresh openings and dated triggers in free state and local permit, license, inspection, tax and appraisal data; the Texas worked set |
| `templates/output-template.md` | Starting a call plan |
| `examples/worked-example.md` | A full plan for HVAC and plumbing contractors in Dallas-Fort Worth |
| `scripts/check-output.py` | Validating a call plan before handing it over |
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
