---
name: reply-handling
description: >-
  Classifies and answers cold email replies: interested, price questions,
  referrals, objections (too expensive, competitor, our system already does it,
  in-house, no need), not now, unsubscribe, hostile, out of office and
  bounce. Produces a reply-by-reply triage with sendable drafts, or a full inbox
  playbook with SLAs, CRM states, suppression and automation limits, and finds a
  referred person's email with ScraperCity's Email Finder. Use when the user
  pastes replies to answer, wants a reply playbook or objection lines, or asks
  how to handle OOO, unsubscribes and angry replies.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags:
    - cold-email
    - reply-handling
    - objection-handling
    - inbox-management
    - suppression
    - crm
  related_skills:
    - cold-email-strategy
    - cold-email-copywriting
    - multi-channel-outreach
    - email-deliverability
    - sending-platforms
    - crm-enricher
    - email-list-cleaner
    - decision-maker-finder
  frameworks:
    - "Alex Berman - reply handling rules from his follow-up guide (reply within 5 minutes)"
    - "Alex Berman - soft vs hard bounce guide"
    - "Alex Berman - 'we already have a vendor' means the market buys (Lean B2B interview)"
    - "IETF RFC 3834 - Auto-Submitted header and auto-responder rules"
    - "Yahoo - Sender best practices, unsubscribe within 2 days"
    - "Google - Email sender guidelines (2024)"
    - "Instantly AI Custom Reply Labels and Smartlead AI Lead Categorization (vendor docs, checked 2026-10-13)"
    - "Instantly campaign options and Smartlead company-level auto-pause, OOO restart and global block list (vendor docs, checked 2026-10-13)"
    - "Toast - restaurant peak hours by service type (June 2026)"
    - "Ryan Reisert - meeting confirmation sequence (Buckets)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - alex-berman-cold-email.md
    - cold-email-frameworks.md
    - deliverability-primer.md
---

# Reply Handling

## Overview

This skill turns a cold email inbox into a set of states with rules. Every reply gets one class from a fixed taxonomy, a response from the library (or a deliberate non-response), a deadline, a CRM state change and, when needed, a suppression entry. Referrals become new contacts: the named person's email is found with `find_emails` (it returns validated addresses), and their first email names the referrer in the subject and gives a reason to care written for their industry and job.

The mistakes it prevents: answering a positive reply the next day, an automated template sent to someone who wrote "this is spam, I'm reporting you", re-emailing someone who said "remove me", and a "talk to Sarah" referral that gets a thin note pointing at someone else's thread. These cost meetings that the list and the copy already paid for.

## When to Use

- "How should I respond to these replies?" (one or more pasted replies: use the triage format).
- "Build a reply playbook", "write objection responses", "set up inbox rules".
- "What do we do with out-of-office and bounces?"
- Configuring lead statuses in Instantly, Smartlead, Lemlist, EmailBison or ManyReach and their CRM sync.
- An SDR or agency needs a response library and SLAs.

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Writing the first emails and follow-ups | `cold-email-copywriting` |
| Fixing bounce rate or spam placement | `email-deliverability` |
| Planning the sequence and its branches | `cold-email-strategy` |
| Calling a positive reply who went quiet | `multi-channel-outreach` |
| Cleaning a CRM after the campaign | `crm-enricher`, `email-list-cleaner` |

## Prerequisites

1. The offer and the meeting link or two proposed time slots.
2. The sending platform and CRM, and whether replies sync between them.
3. Who owns replies, their working hours and time zone.
4. A suppression list location that every sending tool reads (platform blocklist plus CRM field).
5. ScraperCity API key for referral capture (`find_emails`).
6. For pasted replies: each reply's text, the prospect's signature or location (for time zone), and the brief's offer and proof.
7. For a playbook, the settings no source publishes, which the user sets and the deliverable states: escalation owners and their time limits, the AI-label confidence threshold, how often the review queue is checked, the weekly sample size and the error rate that turns a class off, and how long to pause an out-of-office with no return date.

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, follow-up guide | Get back to an interested reply within 5 minutes. Send the calendar invite immediately after they agree. Info request: a 2 to 3 sentence summary and a proposed time, no PDF. Price question: no pricing in email, move it to a call. A competitor reply is good news: they are in the market. "Not right now": nurture with something useful every 4 to 6 weeks; a named date: confirm it and follow up then. Not interested or "remove me": acknowledge and remove at once. Stop the sequence on reply, unsubscribe or hard bounce. Unsubscribes above 0.5% of prospects mean the follow-ups are too aggressive or not relevant enough. |
| Alex Berman, templates page | Respond within 2 to 4 hours during business hours; no case studies, proposals or pricing over email. Price question: "Pricing depends on [Variable 1] and [Variable 2], so it varies", then a 15 minute walkthrough. Cold emails stay under 75 words, subjects under 50 characters. |
| Alex Berman, soft vs hard bounce guide | Remove a hard bounce immediately. Platforms retry soft bounces over 24 to 72 hours; after two or three consecutive mailbox-full bounces, treat the address as a hard bounce. A 5.7.1 block is a sender reputation problem, not a bad address. Keep bounces under 2%. |
| Alex Berman, Lean B2B interview | "We already have a vendor" means the market buys. He also suggests asking "not interested" replies for feedback; this skill doesn't, because the reply has just promised no follow-up (step 4). |
| RFC 3834 | Messages with an `Auto-Submitted` value other than `no` are automatic; responders should not answer them, and must not reply to a null return path. |
| Yahoo sender best practices | Honor unsubscribes within 2 days; keep spam rate under 0.3%. |
| Google sender guidelines | Keep user-reported spam under 0.1% and never reach 0.3%; process unsubscribes within 48 hours. |
| Hunter, State of Cold Email 2025 | Referral requests were the most effective follow-up type in its data. |
| Instantly and Smartlead help docs (checked 2026-10-13) | Both sequencers can label replies with AI automatically; neither documents a confidence score, so the threshold and review queue are the user's own. |
| Instantly and Smartlead help docs, campaign settings (checked 2026-10-13) | Menu paths for company-level stop on reply, OOO pause and resume, and the global blocklist (`references/reply-taxonomy-and-routing.md` section 4). |
| Toast, "Best opening hours for different types of restaurants" (June 2026) | Restaurant peak hours: 11am to 2pm and 5pm to 8pm for quick service, 5pm to 10pm for casual dining. Proposed meeting times for restaurants avoid them. |
| Ryan Reisert, "Buckets" (GTMnow, Nov 2021) | Confirm booked meetings a week out by phone, 12 to 24 hours out by email, 2 to 3 hours out by phone; no-shows go back to the Priority bucket. |

## Workflow

### 1. Detect automatic replies before a human reads them

Check headers first, then text. Full rules in `references/reply-taxonomy-and-routing.md`.

| Signal | Class |
|-|-|
| `Auto-Submitted: auto-replied` or `auto-generated` (RFC 3834) | Automatic: OOO, auto-ack, or bounce |
| Null return path, `Content-Type: multipart/report; report-type=delivery-status`, or a `5.x.x` status code | Bounce |
| Subject starts with "Automatic reply", "Out of Office", "Abwesenheitsnotiz", "Respuesta automática" | OOO |
| `X-Autoreply`, `X-Autorespond`, or `Precedence: auto_reply` / `bulk` | Automatic |
| Body names a return date | OOO with date |
| Body says "no longer with", "has left", "this mailbox is not monitored" | Left company |

Never send a sales reply to an automatic message.

Automation boundary: AI reply labels in Instantly or Smartlead may act alone only on Out of office (pause), hard bounce and help desk auto-acks (suppress) and polite Unsubscribe (suppress, optional removal line), and only when a header rule matched or your own classifier scores at or above the confidence threshold the user sets (neither vendor publishes a score). Hostile replies, unclear or two-intent replies, and Interested replies from target accounts always go to a person. Everything below the threshold goes to a human-review queue checked at an interval the user sets, and a weekly sample of auto-handled replies, sized by the user, measures misclassification. Rules: `references/reply-taxonomy-and-routing.md` section 6.

### 2. Classify every human reply into one class

Use the 15 classes in the taxonomy reference. When a reply fits two classes, take the one higher in this priority order: Hostile > Unsubscribe > Bounce > Interested > Referral > Objection > Not now > Wrong person > Other. An "interested, but talk to Sarah too" reply is Interested, with a referral note.

Hostile is a needs-review class set by trigger words, whatever else the reply says. Automation may suppress the address but never sends anything, not even the polite removal line:

| Trigger group | Words (whole word, reply body only) | Who acts |
|-|-|-|
| Complaint | spam, report, reported, junk, blacklist, block, abuse, harass, unsolicited, "how did you get my email" | A person: suppress, then R26 or nothing |
| Threat | lawyer, attorney, sue, cease and desist | A person: no reply from sales; forwarded to the escalation owner the user names |
| Data request | "delete my data", "what data do you have" | A person: suppress, then R26 or nothing |
| Profanity or threat | profanity, threats | A person: suppress, then R26 or nothing |

"I'll report back" or "block out an hour" also trips it; a person clears a false alarm in seconds, and a template sent to a real complaint can't be recalled. Full list: `references/reply-taxonomy-and-routing.md` section 1b.

### 3. Respond within the SLA

Response times come from Berman: an interested reply within 5 minutes (follow-up guide), every other human reply within 2 to 4 business hours (templates page). Removals happen the same day in every tool. Escalation owners and their time limits are the user's settings; the deliverable states them in the Escalate to column.

| Class | First response | Who | Escalate to |
|-|-|-|-|
| Interested, target account or VP+ title | 5 minutes | AE | AE, within the time the user sets; SDR covers if the AE has not replied by then |
| Interested, any other account (meeting request, accepted time, send info) | 5 minutes | SDR | SDR; AE added when the meeting is booked |
| Interested: price question, any account | 5 minutes: what the price depends on, then a short walkthrough call (R6) | SDR | AE, within the time the user sets, if they ask for a quote or contract terms |
| Interested: technical question the brief can't answer | 5 minutes (holding reply R8b) | SDR | Solutions engineer, within the time the user sets |
| Referral | 2 to 4 business hours (thank the referrer); new contact enrolled when the Email Finder returns | SDR, then automation | AE if the referred person is VP+ at a target account |
| Objection | 2 to 4 business hours | SDR | Manager for a competitor or procurement objection at a target account |
| Not now | 2 to 4 business hours, short | SDR or template | None |
| Unsubscribe, polite | No reply, or Removal line (R24); the deliverable picks one; suppress the same day | Automation, SDR checks | Ops if any entry is not suppressed the same day |
| Hostile: complaint, profanity | Removal line (R26), sent by a person, or No reply; suppress now | SDR | Sales manager |
| Hostile: threat or data request | No reply; suppress now | SDR forwards | The escalation owner the user names |
| OOO | No reply; pause until the return date | Automation | None |
| Bounce | No reply; suppress immediately | Automation | Deliverability owner if bounces pass 2% in a cell |

In a triage, escalation rides the reply's own window: the AE or manager is alerted when the reply arrives and acts inside the same 5 minutes or 2 to 4 business hours, so the deliverable needs no new number. Hot replies (a meeting request, an accepted time, a price question) get 5 minutes during business hours for every account tier. Replies that arrive after hours are answered first thing the next business day in the prospect's time zone. Target account means a named account list agreed with sales (for example multi-location dental groups).

The Send value is the same word everywhere: "No reply" means nothing goes out; "Removal line (R24)" or "Removal line (R26), sent by a person" means exactly one line goes out. Never write "no sales reply" next to a draft.

### 4. Write the response from the library

Pick the response in `references/response-library.md`. Every draft you hand over must be sendable as written:

- No brackets and no blanks. The only variables allowed are the recipient's name and company as merge fields with a fallback, such as `{{first_name|there}}` and `{{company|your team}}`.
- Use only facts in the user's brief: their offer, prices, results, integrations. If the brief has no proof point, write the reply without one. Never leave "[client result]" for a rep to fill; a rushed rep sends it broken or makes one up.
- Two to three sentences (Berman's follow-up guide), never over 75 words, one ask at most, contractions, plain words. Interested replies get two specific times with a time zone, or the brief's booking link. No decks, PDFs, proposals or price sheets (Berman's templates page).
- Proposed times fall outside the prospect's busy hours. Restaurants: Toast's peak hours are 11am to 2pm and 5pm to 8pm (quick service) and 5pm to 10pm (casual dining), so offer 2:30pm to 4:30pm their time. Other industries: outside the business's posted rush, or the hours the user gives.

Class rules the drafts follow:

| Reply | Draft does | Draft never does |
|-|-|-|
| Not interested, no need | Accepts and stops in one or two lines (R25, R13) | Asks a feedback question after saying "I won't follow up" |
| Maybe next quarter, not now | Confirms the date you'll follow up, then stops (R19, R20) | Adds extra questions such as "is this still the best address?" |
| Happy with a competitor ("we use ADP and we're happy") | Acknowledges, names the hardest part of the job in their industry that the offer takes over as a condition ("if tips and tip credits ever start eating someone's week, reply here"), goes to nurture with an exact first-touch date 6 weeks out (R14) | Argues, knocks the competitor, claims what it lacks or what "most" buyers find, or ends with "I'll leave you be" |
| Too expensive | Says plainly it may not pay for them, offers a 15 minute comparison against what they spend now (R34) | Argues value, invents ROI, quotes a competitor's or a salary cost the brief lacks |
| "Our system already does that" (POS, practice software or bank bundles it) | Separates "the feature exists" from "someone does the work", names the job the brief says you take over, easy out (R35) | Claims the bundled tool falls short without the brief saying so |
| "We do it in-house" | Offers to take one named part off the in-house person, so it isn't either-or, easy out (R27) | Implies the in-house person does it badly |
| Price question | Answers first with what the price depends on (Berman's templates page: "Pricing depends on [Variable 1] and [Variable 2]"), using the brief's variables, then a 15 minute walkthrough with two times, inside 5 minutes (R6) | Skips the question and only asks for a meeting, sends a price sheet, or guesses a number |
| Accepted a meeting time | Restates day, date and time, says the invite is on its way, invites them to forward it (R3, R29); the invite goes out at once (Berman), in the zone from the reply, signature, lead-record address or area code | Holds the invite to ask the time zone when any of those shows it, assumes the sender's zone, re-pitches, or adds a question |
| Unsubscribe, hostile | Suppresses; one removal line at most (R24, R26; a person sends R26) | Explains, argues, asks why, or goes out from automation when a trigger word is present |
| Threat or data request | Nothing from sales; forwarded the same day | Any reply from the rep |

Every objection the user's brief or request names gets its own ready line in the deliverable, in this shape: acknowledge in under 10 words, one fact from the brief, an easy out or one ask.

### 5. Update the CRM state

Map each class to a lead status and a deal action. Full map in `references/reply-taxonomy-and-routing.md`.

| Class | Lead status | Sequence | Deal |
|-|-|-|-|
| Interested | Interested | Stop for everyone at the company | Create, stage "Meeting requested" |
| Meeting booked | Meeting booked | Stopped | Stage "Meeting scheduled" |
| Referral | Referred | Stop for referrer | Note referrer on new contact |
| Objection | Objection: [type] | Stop | None, or "Nurture" |
| Not now | Nurture until [date] | Stop; task on date | None |
| Unsubscribe | Do not contact | Stop everywhere | None |
| Bounce | Bounced | Stop | None |
| Hostile | Do not contact | Stop everywhere | None; flag for review |

### 6. Suppress

Add unsubscribe, hostile and hard-bounce addresses to the global suppression list in every sending tool and the CRM the same day they arrive (Berman: remove them immediately). That stays inside the 2 day unsubscribe limit in Yahoo's and Google's sender rules, which inbox placement depends on. A not-interested reply is suppressed from every sequence permanently, because the reply promised no follow-up. When someone says "take our company off", suppress the domain. In the deliverable, state only the rules the replies trigger (`references/suppression-and-compliance.md`).

### 7. Capture referrals

For "talk to Sarah Kim, she runs ops" or "I've left; try David":

1. Parse first name, last name, the job the referrer said they own, and the company domain (from the referrer's email domain if not given).
2. `find_emails` with `contacts: [{"first_name": "Sarah", "last_name": "Kim", "domain": "acme.example"}]`. Charged $0.05 only if found, and found addresses come back already validated. Run `validate_emails` ($0.00169) only on an address the referrer typed out.
3. Thank the referrer in one line (R10) and stop their sequence.
4. Send the referred person R11 as a new thread, not a forward:
   - Subject names the referrer ("Tom suggested I reach out").
   - Line 1: the referrer's name and the job they said this person owns.
   - Line 2: the problem the offer removes, in the terms of their industry and seat (for restaurant payroll, tip reporting across shifts; for a dental practice, front desk time). Name a problem, never a result or number the brief doesn't give.
   - Line 3: one proof or the price, from the brief.
   - Line 4: two times in their time zone or the booking link.
   - Never paste the original email underneath or quote the referrer's reply. Under 75 words, subject under 50 characters (Berman's limits for a cold email). Use "suggested" only if the referrer named this person.

If the person is not named ("talk to our marketing team"), run `query_lead_database` with `companyDomain` and a `title` filter to find the role holder, then `find_emails` if no email returns.

In a triage, the lookup is one clause in the referral's row: a full address from the referrer is used as given; a missing or cut-off one gets "address from ScraperCity Email Finder (name plus the company domain)". No call blocks, parameters or prices.

### 8. Review weekly

Count replies by class per campaign cell. Mostly "not interested" points at targeting (Berman's diagnosis table); many "already have a vendor" means the market buys and the offer needs sharpening (Lean B2B interview); unsubscribes above 0.5% of prospects mean the follow-ups are too aggressive or not relevant (follow-up guide). Pause the cell when spam complaints near Google's 0.1% or bounces pass 2%.

## ScraperCity Implementation

| Step | Tool | Parameters | Price |
|-|-|-|-|
| Find the referred person's email | `find_emails` (Email Finder) | `contacts: [{first_name, last_name, domain}]` or `full_name` + `company_name` | $0.05 per email found, free if not found; found emails are already validated |
| Check an address the referrer typed out | `validate_emails` (Email Validator) | `emails: [...]` | $0.00169 per email |
| Find the role holder when only a team is named | `query_lead_database` | `companyDomain`, `title`, `seniority`, `hasEmail: true`, `limit: 10` | Included on Growth ($149/mo) and Scale |
| Mobile for a hot referral that prefers calls | `find_mobiles` (Mobile Finder) | `inputs: ["sarah.kim@acmedental.example"]` | $0.25 per number found, free if not found |

MCP call for a batch of referrals collected over a week:

```json
{
  "tool": "find_emails",
  "contacts": [
    {"first_name": "Sarah", "last_name": "Kim", "domain": "acmedental.example"},
    {"first_name": "David", "last_name": "Ruiz", "domain": "lonestarortho.example"},
    {"full_name": "Priya Shah", "company_name": "Northpaw Coffee"}
  ]
}
```

CLI: `npx scrapercity email-find`. REST: `POST /api/v1/scrape/email-finder`, then poll `GET /api/v1/scrape/status/{runId}` and download.

### Worked cost estimate (one month, 2,600 contact campaign)

Both finders bill only on a hit, so the estimate is a ceiling: every lookup found.

| Line | Count | Unit price | Ceiling |
|-|-|-|-|
| `find_emails` on referral and wrong-person replies with a named person | 24 | $0.05 per email found | $1.20 |
| `validate_emails` on 2 addresses referrers typed out | 2 | $0.00169 | $0.00 |
| `find_mobiles` for 5 referrals who asked for a call | 5 | $0.25 per number found | $1.25 |
| "Talk to the team" replies resolved with Lead Database | 9 | included on Growth | $0.00 |
| Total | | | $2.45 |

Under $5, so no separate approval is needed; call `check_wallet` once a week.

## Output Format

Pick the format by what the user asked for.

**A. Pasted replies (one to about 25): a reply triage** from `templates/triage-template.md`. Answer first, each fact once. Sections in order, nothing else:

1. One or two lines: the brief facts the drafts use (offer, price, proof) and the assumptions (platform, time zones). No notes about the process or what was or wasn't run.
2. `## Reply Triage`: one table, one row per reply: `| # | Reply | Class | Send | Within | CRM status | Suppress |`. Send is "Draft N", "No reply", "Removal line (draft N), sent by a person" or "No reply; forwarded to" plus the owner's role. Within is the response window (5 minutes for hot replies, 2 to 4 business hours for other human replies). Pause, resume and nurture dates are exact, with the weekday. A referral row says where the referred person's address comes from in one clause.
3. `## Drafts`: one `### N. Name, class` heading per reply that gets one, the draft in a fenced `text` block. A new thread (the referred person) starts with a `Subject:` line naming the referrer.
4. `## Routing and SLAs`, only when the user asked for routing, SLAs, inbox rules or setup: one table `| Class | Owner | Escalate to | Automation |`, one row per class the replies used (the response window already sits in the triage table). Then one line per platform setting the replies trigger, each a rule plus its menu path in Instantly and in Smartlead from `references/reply-taxonomy-and-routing.md` section 4, or only the platform the user named.
5. `## Open Items`: at most 5 bullets: facts missing from the brief that a draft needed (no price, no proof), and one "Confirm:" line naming the settings the user owns (escalation owners, target-account list) without restating values from the tables. Write "None" if empty.

Leave out a Reason column and any rationale after a setting. Taxonomy, bounce or help-desk rules, OOO parsing, meeting reminders, weekly review and referral lookups appear only when a pasted reply or the request needs them.

**B. A reply playbook** ("build our reply process"): one Markdown file from `templates/output-template.md`, `##` sections in order: Inbox Setup, Reply Taxonomy, Response Library, SLAs, CRM State Map, Suppression Rules, Auto-Reply Detection, Automation Boundaries, Referral Capture, Weekly Review. The SLAs table carries an Escalate to column; Automation Boundaries lists each class as auto, partial or never, the confidence threshold, the review queue, the hostile trigger words and the weekly misclassification sample. Response Library drafts sit in fenced `text` blocks under `###` headings that name the class: one contains "Not interested", at least three name an objection, and the referral first email has a subject naming the referrer.

Rules for both formats:

- Send says the same thing in every table: "No reply" never sits next to a draft, and a removal line is listed as a removal line.
- State only the rules the replies trigger, as plain settings. No justification after a setting ("because...", "keeps the promise", "looks automated"); a playbook's Suppression Rules may give one operating reason per row.
- Every number is either from a named source, named in a few words ("5 minutes, Alex Berman"), or a value the user gave. A setting nobody published and the user did not give goes on the "Confirm:" line by name, with no invented default.
- No legal content: no laws, regulators, penalties or legal deadlines in any deliverable.
- No tool ids, JSON call blocks, per-call prices, file paths, skill names or source page names in the deliverable. Name a lookup in words ("ScraperCity Email Finder") once.
- No claim about what buyers "usually" or "most" do, and no cost, price or result for any vendor, competitor or tool unless the brief or ScraperCity's catalog states it.
- Response ids (R1, R25) may label drafts in a playbook; they never appear inside a draft.

## Quality Check

`python3 scripts/check-output.py deliverable.md` reads either format. For a triage it enforces:

- Only the sections in Output Format A, and at most 5 Open Items bullets.
- Every row's Send matches the drafts: a draft exists for every "Draft N" and removal line, and none exists for a "No reply" row.
- Any reply containing a hostile trigger word (spam, report, lawyer, attorney, sue) is classed Hostile, never sent by automation.
- Hot rows (interested, price, accepted time) are answered within 5 minutes; a price draft says what the price depends on; an accepted-time draft says the invite is on its way.
- A referral draft opens with a `Subject:` line that names the referrer.
- No Reason column, no "because" outside the drafts, no JSON blocks, tool ids or per-lookup prices, no process notes, and no bounce or help-desk text unless a row needs it; no law names, source page names or file paths.

For a playbook it enforces:

- Every class has an SLA, a CRM state and a suppression decision; hostile, unsubscribe and bounce are suppressed.
- Every SLA row has an Escalate to value; every Interested row escalates to a named role with a time limit; hot replies are answered in 5 minutes or less.
- Unsubscribe and hostile rows say "No reply" or "Removal line", never "no sales reply", and a removal line has a draft.
- Automation Boundaries lets automation handle out of office and unsubscribe, keeps hostile and target-account interested replies with a person, lists hostile trigger words including spam and lawyer, states a confidence threshold, and names a weekly misclassification sample.
- At least 8 drafts, each 75 words or fewer, no "[" outside a `{{merge|fallback}}` field; the Not interested draft has no question; at least three objection drafts; the referral first email has a subject naming the referrer.
- Referral capture names the Email Finder; every suppression row has a deadline and an operating reason, and no deliverable names a law.

Also check by reading:

- Interested replies get two specific times in the prospect's time zone or a booking link.
- Every fact in a draft (price, result, integration, competitor gap) appears in the user's brief.
- No response sends a deck, PDF or price sheet; a price question gets what the price depends on, then a short walkthrough call with two times outside the prospect's busy hours.
- OOO replies pause rather than stop, and resume after the return date.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Answering positive replies the next morning | Berman: replying within 5 minutes lifts the meeting book rate; waiting 48 hours drops it | 5 minute SLA in business hours for every hot reply, mobile alerts on Interested |
| Drafts with "[client result]" or "[their problem]" slots | A rushed rep sends the bracket or invents a claim to fill it | Sendable drafts; facts only from the brief; drop the proof if the brief has none |
| Sequence keeps running after a reply | The next touch lands mid-conversation and can draw a spam report | Stop on any reply at company level |
| Unsubscribe handled in one tool only | Another campaign emails them next week and they report it as spam | One global suppression list synced to every tool |
| Replying to an OOO with a pitch | Wasted touch; can loop with auto-responders | Detect via headers, pause to return date |
| Referral email that says "Tom said to talk to you, see below" | The referred person has no reason to read someone else's thread | Subject names the referrer; one industry-specific reason, one proof, one ask; no forwarded original |
| Arguing with "not interested", or asking for feedback after promising no follow-up | Berman: acknowledge and remove, don't push | Accept and stop in one line, no question |
| "Happy with ADP" answered with a rebuttal, or with "I'll leave you be" | A rebuttal ends the thread; a bare goodbye leaves no reason to come back | Acknowledge, one industry problem as a condition, nurture date 6 weeks out |
| No ready line for "too expensive", "our POS does that" or "we do it in-house" | Reps improvise, argue, or invent ROI | R34, R35 and R27, written from the brief |
| Emailing a price sheet after "how much?", or ignoring the question and only asking for a call | Berman: pricing over email rarely leads to deals; a dodged question reads as a dodge | R6: what the price depends on, then a 15 minute walkthrough with two times |
| Restaurant slots at 11am or 1pm | Toast's peak hours: 11am to 2pm and 5pm onward | Offer 2:30pm to 4:30pm their time |
| "Which time zone? I'll send the invite once I know" | A round trip before a meeting two days out | Zone from signature, lead-record address or area code; invite now (Berman) |
| An automated removal line sent to "this is spam, I'm reporting you" | A template that misreads a furious reply turns a complaint into a report | Trigger words route to a person; automation only suppresses |
| Triage says "No sales reply" and then lists a confirmation | The rep can't tell whether anything goes out | One Send value per row: "No reply" or "Removal line" |
| Bounce codes and help-desk rules in a triage of eight human replies | Padding the reader skips, and it buries the drafts | Only the rules the pasted replies trigger |
| A Reason column, JSON tool calls or a lookup section with prices in a triage | Unsourced claims and internal ids the reader can't act on | Settings only; a lookup is one clause in the referral row |
| Letting AI labels send replies on their own | A misread "remove me" gets a sales reply; a target account gets a template | Auto only for OOO, bounce and polite unsubscribe above the user's threshold; human queue for the rest; weekly sample |
| VP at a target account waits for the SDR's next inbox pass | The AE hears about it the next day | Escalate to column: the AE, with the time limit the user sets |
| Booked meetings with no confirmation | No-shows | R29 to R33 confirmation and no-show copy |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/reply-taxonomy-and-routing.md` | Classifying a reply, hostile trigger words, auto-reply header rules, CRM state map, platform status names, automation boundaries for AI reply labels |
| `references/response-library.md` | Writing the response for any class: referral first emails, ready objection lines (too expensive, bundled feature, in-house, competitor, procurement), meeting confirmation and no-show copy |
| `references/suppression-and-compliance.md` | Suppression speed, scope, which rules a deliverable needs, suppression lag log |
| `templates/output-template.md` | Starting a reply playbook |
| `templates/triage-template.md` | Starting a reply triage of pasted replies |
| `examples/worked-example.md` | A full playbook for a dental review-software campaign with sample replies |
| `examples/triage-example.md` | A reply triage of eight pasted replies for a vet-clinic bookkeeping campaign |
| `scripts/check-output.py` | Validating a triage or a playbook |
| `references/alex-berman-cold-email.md` | Berman's reply guidance with sources (shared) |
| `references/cold-email-frameworks.md` | Framework context for follow-up copy (shared) |
| `references/scrapercity-catalog.md` | Prices and parameters for `find_emails`, `validate_emails`, `find_mobiles` (shared) |
| `references/scrapercity-platform.md` | Lead Database access by plan (shared) |
| `references/deliverability-primer.md` | Complaint thresholds and bounce handling (shared) |

## Related Skills

- `cold-email-strategy` defines the branches this skill executes.
- `cold-email-copywriting` writes the referral sequence and re-engagement copy.
- `multi-channel-outreach` calls interested contacts who go quiet.
- `email-deliverability` investigates bounce and complaint spikes this skill reports.
- `sending-platforms` configures statuses, stop rules and blocklists.
- `crm-enricher`, `email-list-cleaner` and `decision-maker-finder` keep contacts and referrals accurate.
