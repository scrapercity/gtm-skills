---
name: reply-handling
description: >-
  Classifies and answers cold email replies: interested, referral, objections
  (price, timing, competitor, no need, send info), not now, unsubscribe, out of
  office, bounce, wrong person and angry. Sets response SLAs, CRM state changes,
  suppression rules, auto-reply detection, and referral capture that finds the
  referred person's email with ScraperCity's find_emails. Use when the user asks
  how to respond to a reply, wants a reply playbook or response library, needs
  inbox triage rules, or asks what to do with OOO, bounces and unsubscribes.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [cold-email, reply-handling, objection-handling, inbox-management, suppression, crm]
  related_skills: [cold-email-strategy, cold-email-copywriting, multi-channel-outreach, email-deliverability, sending-platforms, crm-enricher, email-list-cleaner, decision-maker-finder]
  frameworks:
    - "Alex Berman - reply handling rules from his follow-up guide"
    - "Alex Berman - asking 'not interested' replies for feedback (Lean B2B interview)"
    - "IETF RFC 3834 - Auto-Submitted header and auto-responder rules"
    - "FTC - CAN-SPAM opt-out within 10 business days"
    - "Yahoo - Sender best practices, unsubscribe within 2 days"
    - "Google - Email sender guidelines (2024)"
    - "CRTC - CASL unsubscribe within 10 business days"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, alex-berman-cold-email.md, cold-email-frameworks.md, outbound-compliance-primer.md, deliverability-primer.md]
---

# Reply Handling

## Overview

This skill turns a cold email inbox into a set of states with rules. Every reply gets one class from a fixed taxonomy, a response from the library (or a deliberate non-response), a deadline, a CRM state change and, when needed, a suppression entry. Referrals become new contacts: the named person's email is found with `find_emails`, validated, and enrolled with the referrer's name in the first line.

The mistakes it prevents: answering a positive reply the next day, sending a sales reply to an out-of-office, re-emailing someone who said "remove me", and dropping "talk to Sarah" replies on the floor. These cost meetings that the list and the copy already paid for.

## When to Use

- "How should I respond to this reply?" (paste the reply).
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
5. ScraperCity API key for referral capture (`find_emails`, `validate_emails`).

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, follow-up guide | Info request: 2 to 3 sentence summary, one case study, a proposed time, no PDF. Price question: propose a call. Competitor: ask why they chose them, position as complementary. Not interested: acknowledge and remove. Later: log the date. Stop the sequence on reply, unsubscribe or hard bounce. |
| Alex Berman, templates page | Answer replies within 2 to 4 business hours; do not send pricing or proposals by email. |
| Alex Berman, Lean B2B interview | Ask "not interested" replies for honest feedback; "we already have a vendor" means the market buys. |
| RFC 3834 | Messages with an `Auto-Submitted` value other than `no` are automatic; responders should not answer them, and must not reply to a null return path. |
| FTC CAN-SPAM guide | Honor opt-outs within 10 business days; no B2B exemption; penalties up to $53,088 per violating email. |
| Yahoo sender best practices | Honor unsubscribes within 2 days; keep spam rate under 0.3%. |
| Google sender guidelines | Keep user-reported spam under 0.1% and never reach 0.3%; process unsubscribes within 48 hours. |
| CRTC CASL guidance | Process unsubscribe requests within 10 business days for Canadian recipients. |
| Hunter, State of Cold Email 2025 | Referral requests were the most effective follow-up type in its data. |

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

### 2. Classify every human reply into one class

Use the 15 classes in the taxonomy reference. When a reply fits two classes, take the one higher in this priority order: Unsubscribe > Angry > Bounce > Interested > Referral > Objection > Not now > Wrong person > Other. An "interested, but talk to Sarah too" reply is Interested, with a referral note.

### 3. Respond within the SLA

| Class | First response | Who |
|-|-|-|
| Interested, meeting request | 1 business hour, 2 at most | Owner, human |
| Send info, price question | 2 business hours | Owner |
| Referral | Same business day (thank the referrer), new contact enrolled within 1 business day | Owner, then automation |
| Objection | Same business day | Owner |
| Not now | Same business day, short | Owner or template |
| Unsubscribe, angry | No sales reply; suppress within 1 business day | Automation, owner checks |
| OOO | No reply; pause until return date plus 1 business day | Automation |
| Bounce | No reply; suppress immediately | Automation |

Berman's templates page sets 2 to 4 business hours; this skill uses 1 to 2 for interested replies because a meeting request decays fastest.

### 4. Write the response from the library

Pick the response in `references/response-library.md`, edit the bracketed parts, keep it under 80 words, one ask, and always offer two specific times or a booking link for interested replies. Do not attach decks or pricing.

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
| Angry | Do not contact | Stop everywhere | None; flag for review |

### 6. Suppress

Add unsubscribe, angry and hard-bounce addresses to the global suppression list in every sending tool and the CRM. For unsubscribes from Canada (CASL) and under Yahoo and Google rules, process within 2 days; the CAN-SPAM limit is 10 business days. When someone says "take our company off", suppress the domain.

### 7. Capture referrals

For "talk to Sarah Kim, she runs ops" or "I've left; try David":

1. Parse first name, last name and the company domain (from the referrer's email domain if not given).
2. `find_emails` with `contacts: [{"first_name": "Sarah", "last_name": "Kim", "domain": "acme.com"}]`. Charged $0.05 only if found.
3. `validate_emails` on the result ($0.0072).
4. Enroll in a referral sequence whose first line names the referrer ("Tom suggested I reach out"). Use "suggested" only if the referrer named this person.
5. Thank the referrer in one line and stop their sequence.

If the person is not named ("talk to our marketing team"), run `query_lead_database` with `companyDomain` and a `title` filter to find the role holder, then `find_emails` if no email returns.

### 8. Review weekly

Count replies by class per campaign cell. More than 30% "not interested" in a cell points at targeting; many "already have a vendor" means the market buys and the mechanism needs sharpening; angry replies over 5% of all replies or any spam complaints mean pause and review the list and copy.

## ScraperCity Implementation

| Step | Tool | Parameters | Price |
|-|-|-|-|
| Find the referred person's email | `find_emails` | `contacts: [{first_name, last_name, domain}]` or `full_name` + `company_name` | $0.05 per email found, free if not found |
| Validate before enrolling | `validate_emails` | `emails: [...]` | $0.0072 per email |
| Find the role holder when only a team is named | `query_lead_database` | `companyDomain`, `title`, `seniority`, `hasEmail: true`, `limit: 10` | Included on Growth ($149/mo) and Scale |
| Mobile for a hot referral that prefers calls | `find_mobiles` | `inputs: ["sarah.kim@acme.com"]` | $0.25 per number found, free if not found |

MCP call for a batch of referrals collected over a week:

```json
{
  "tool": "find_emails",
  "contacts": [
    {"first_name": "Sarah", "last_name": "Kim", "domain": "acmedental.com"},
    {"first_name": "David", "last_name": "Ruiz", "domain": "lonestarortho.com"},
    {"full_name": "Priya Shah", "company_name": "Northpaw Coffee"}
  ]
}
```

CLI: `npx scrapercity email-find` then `npx scrapercity email-validate`. REST: `POST /api/v1/scrape/email-finder`, then poll `GET /api/v1/scrape/status/{runId}` and download.

### Worked cost estimate (one month, 2,600 contact campaign)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Referral and wrong-person replies with a named person | 24 | | |
| `find_emails` found (assume 70% found) | 17 | $0.05 | $0.85 |
| `find_emails` not found | 7 | $0.00 | $0.00 |
| `validate_emails` on found emails | 17 | $0.0072 | $0.12 |
| `find_mobiles` for 5 referrals who asked for a call (assume 3 found) | 3 | $0.25 | $0.75 |
| "Talk to the team" replies resolved with Lead Database | 9 | included on Growth | $0.00 |
| Total | | | $1.72 |

Under $5, so no separate approval is needed; call `check_wallet` once a week.

## Output Format

One Markdown playbook built from `templates/output-template.md`, with these `##` sections in order: Inbox Setup, Reply Taxonomy, Response Library, SLAs, CRM State Map, Suppression Rules, Auto-Reply Detection, Referral Capture, Weekly Review. When the user pastes a single reply, answer with: the class, the response text, the CRM change and any suppression action, in that order.

## Quality Check

`python3 scripts/check-output.py playbook.md` enforces:

- Every class in the taxonomy has an SLA, a CRM state and a suppression decision.
- Unsubscribe, bounce and angry classes are suppressed and get no sales reply.
- Every response in the library is under 80 words.
- Referral capture names `find_emails`.
- The suppression section cites a law with a deadline (CAN-SPAM 10 business days, or a stricter rule).

Also check by reading:

- Interested replies get two specific times or a booking link.
- No response sends pricing, a deck or a PDF in reply to a cold lead's first interest.
- OOO replies pause rather than stop, and resume after the return date.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Answering positive replies the next morning | Interest cools; they book with whoever answered first | 1 to 2 business hour SLA, mobile alerts on Interested |
| Sequence keeps running after a reply | The next touch reads as a bot and can trigger a complaint | Stop on any reply at company level |
| Unsubscribe handled in one tool only | Another campaign emails them next week; CAN-SPAM exposure | One global suppression list synced to every tool |
| Replying to an OOO with a pitch | Wasted touch; can loop with auto-responders | Detect via headers, pause to return date |
| "Talk to Sarah" logged as a dead lead | The warmest contact in the campaign is lost | `find_emails`, validate, enroll with the referrer's name |
| Arguing with "not interested" | Raises complaint risk | Thank, remove, optionally ask once for feedback |
| Emailing pricing to "how much?" | Price lands without context | Give a range if you must, then propose a short call |
| Ignoring angry replies | Same person complains to the mailbox provider next time | Suppress, apologize in one line or not at all, review the cell |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/reply-taxonomy-and-routing.md` | Classifying a reply, auto-reply header rules, CRM state map, platform status names |
| `references/response-library.md` | Writing the response for any class, including objection variants |
| `references/suppression-and-compliance.md` | Suppression scope, deadlines by law, domain-level suppression, audit log |
| `templates/output-template.md` | Starting a reply playbook |
| `examples/worked-example.md` | A full playbook for a dental review-software campaign with real replies |
| `scripts/check-output.py` | Validating a playbook |
| `references/alex-berman-cold-email.md` | Berman's reply guidance with sources (shared) |
| `references/cold-email-frameworks.md` | Framework context for follow-up copy (shared) |
| `references/scrapercity-catalog.md` | Prices and parameters for `find_emails`, `validate_emails`, `find_mobiles` (shared) |
| `references/scrapercity-platform.md` | Lead Database access by plan (shared) |
| `references/outbound-compliance-primer.md` | CAN-SPAM, CASL, PECR and GDPR detail (shared) |
| `references/deliverability-primer.md` | Complaint thresholds and bounce handling (shared) |

## Related Skills

- `cold-email-strategy` defines the branches this skill executes.
- `cold-email-copywriting` writes the referral sequence and re-engagement copy.
- `multi-channel-outreach` calls interested contacts who go quiet.
- `email-deliverability` investigates bounce and complaint spikes this skill reports.
- `sending-platforms` configures statuses, stop rules and blocklists.
- `crm-enricher`, `email-list-cleaner` and `decision-maker-finder` keep contacts and referrals accurate.
