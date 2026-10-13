---
name: inbox-setup
description: >-
  Sets up each cold email mailbox after the domains exist: sender identity tied
  to a real person, address format, display name, signature with opt-out and
  postal address, profile photo, reply routing and forwarding, warmup settings
  and a day-by-day ramp, sending windows, daily caps, reply monitoring, inbox
  rotation and retirement. Produces a mailbox roster with every setting and a
  dated ramp. Use when the user has new mailboxes to configure, asks how to
  warm up inboxes, how many emails a mailbox can send, what signature or sender
  name to use, how to rotate inboxes, or when to retire one.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [mailboxes, warmup, inbox-rotation, signatures, sending-limits, cold-email-infrastructure]
  related_skills: [domain-infrastructure, email-deliverability, sending-platforms, reply-handling, cold-email-copywriting, cold-email-strategy]
  frameworks:
    - "FTC - CAN-SPAM Act compliance guide (accurate headers, postal address, opt-out)"
    - "Google - Email sender guidelines (ramp volume gradually, avoid spikes)"
    - "M3AAWG - Sender Best Common Practices v4.0 (Aug 2026), ramp and monitoring"
    - "Instantly - warmup settings and campaign readiness rules"
    - "Apollo - mailbox sending limit recommendations"
    - "Google Workspace and Microsoft 365 - per-user sending limits"
    - "Alex Berman - warmup length and per-inbox daily volume"
  shared_references: [deliverability-primer.md, outbound-compliance-primer.md, scrapercity-catalog.md, scrapercity-platform.md]
---

# Inbox Setup

## Overview

This skill configures every mailbox that will send cold email and schedules its first six weeks. The deliverable is a roster: one row per mailbox with the address, the real person behind it, display name, signature, photo status, reply routing, warmup settings, first cold send date, daily cap, sending window and rotation group, plus a dated ramp and the rules for retiring a mailbox.

It prevents three common failures. Brand-new mailboxes sending 50 cold emails on day two. Mailboxes under invented names with no human reading replies, which breaks CAN-SPAM's accurate-header rule and loses the positive replies. And a roster nobody can audit, where one bad mailbox drags its domain down before anyone notices.

## When to Use

- "I just created 15 mailboxes, what now?"
- "How long do I warm up?" or "what warmup settings?"
- "How many emails per day per inbox?"
- "What name and signature should the sender use?"
- "Should replies forward to my main inbox?"
- "How does inbox rotation work?" or "when do I retire an inbox?"

Use a different skill for nearby jobs:

| Job | Skill |
|-|-|
| Domains, DNS records, mailbox count and provider | `domain-infrastructure` |
| Ongoing bounce, complaint and blocklist monitoring | `email-deliverability` |
| Sequencer choice, CSV import, webhooks | `sending-platforms` |
| Categorizing and answering replies | `reply-handling` |
| Writing the emails | `cold-email-copywriting` |

## Prerequisites

| Input | Default if unknown |
|-|-|
| Mailbox list from `domain-infrastructure` (address, domain, active or reserve) | Required |
| Real people who will send and read replies, with title and photo consent | Required; at least 1 |
| Company postal address for the signature | Required for US commercial email (CAN-SPAM) |
| Sequencer | Instantly |
| Recipient time zones | From the list's `state` or `country` columns |
| Mailbox creation date | Today |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| FTC CAN-SPAM compliance guide | From, To, Reply-To and routing must identify the person or business who sent the message; commercial email needs a valid postal address (a registered PO box is fine) and a clear opt-out honored within 10 business days; the law has no B2B exception; up to $53,088 per violating email. |
| Google Email sender guidelines | Raise volume slowly; sudden spikes such as doubling at once can trigger rate limits; on error 4.7.28 pause at least 10 minutes. |
| M3AAWG Sender BCP v4.0 (Aug 2026) | Start low and ramp, about six weeks on average; spread sends through the day; watch for volume jumps above 40%. |
| Instantly help center | Account ready for campaigns after at least 2 weeks of warmup and a health score above 90%; new-account warmup defaults: +1 a day, limit 10, reply rate 30%. |
| Apollo knowledge base | Recommends 50 to 100 emails a day per mailbox, 10 to 20 an hour, 60 to 300 seconds between emails, start at 50. This skill runs stricter. |
| Google Workspace and Microsoft 365 limits | Workspace 2,000 messages per user per day (500 on trial); Exchange Online 10,000 recipients a day, 30 messages a minute. Far above cold caps, so reputation sets the limit. |
| Alex Berman (alexberman.com) | Warm up 2 to 4 weeks, start new domains at 10 to 20 a day, keep under 50 a day per inbox. |

## Workflow

### 1. Assign a real person to every mailbox

Each mailbox maps to a person on the team who agrees to send under their name and who reads (or has a teammate read) the replies. One person can own several mailboxes across domains: `dana@getacme.com`, `dana.ortiz@tryacme.com`. Invented personas with stock photos fail CAN-SPAM's accurate-header test and fall apart the moment a prospect looks them up. Details: `references/mailbox-setup-runbook.md` section 1.

### 2. Set address and display name

Address formats, rotated across domains for the same person: `first@`, `first.last@`, `firstl@`. Display name is the person's real name, `Dana Ortiz`, with the company name, titles and emojis left out.

### 3. Write the signature

Plain text, 3 to 5 lines: name, title, company, postal address line, opt-out line. No images, no tracking links, at most one link (the main site, as plain text), and none in step 1 if link tracking is on. Template in `references/mailbox-setup-runbook.md` section 3.

### 4. Profile photo and account hygiene

Upload the person's real headshot to the Google or Microsoft account so it shows in Gmail and Outlook. Turn on 2-Step Verification, record the recovery email (an address on the main domain the ops lead controls), and store credentials in the team password manager.

### 5. Reply routing

Replies land in the sending mailbox. The sequencer's unified inbox reads all mailboxes in one place and stops the sequence on reply. Do not set a Reply-To on the main domain (house standard: keeps the cold domain and the main domain separate in headers). If the rep wants copies in their main inbox, add a Gmail forwarding rule for replies only. Routing options: `references/mailbox-setup-runbook.md` section 5.

### 6. Warmup and ramp

Turn on sequencer warmup the day the mailbox connects. Day 1 to 14 warmup only. Then cold sends of 10, 20, 30 a day in weekly steps, gated on bounce and complaint numbers. Schedules and per-sequencer settings: `references/warmup-and-ramp.md`.

### 7. Sending window and caps

Weekdays, 8:00 to 17:00 in the recipient's time zone (house standard), randomized gaps of 2 to 6 minutes between sends from one mailbox, at most 15 cold sends an hour per mailbox. Daily cap 30, raised to 50 only after 14 days with bounces under 1% and complaints under 0.1%.

### 8. Rotation groups

Group mailboxes by domain into rotation groups so each campaign spreads first touches across many mailboxes; follow-ups stay with the mailbox that sent step 1 so the thread holds together. Reserve mailboxes stay in warmup only. Rules: `references/rotation-and-retirement.md`.

### 9. Reply monitoring

Name the person who checks the unified inbox and the hours they check it (at least twice a sending day). Positive replies get a human answer within 4 business hours (house standard). Hand categorization to `reply-handling`.

### 10. Retirement rules

Write the conditions that pause or retire a mailbox before anything goes wrong: 3% hard bounces on a mailbox over its last 200 sends, any spam complaint spike on its domain, a provider suspension, or the person leaving the company. Steps: `references/rotation-and-retirement.md` section 4.

## ScraperCity Implementation

ScraperCity does not host mailboxes. It feeds the ramp with validated lists, so a new mailbox's first 200 sends carry close to zero bounces.

**Step A.** `check_wallet()` before any paid call.

**Step B. Pull only what the ramp can send.** During ramp week 1 (10 a mailbox on 20 mailboxes), the campaign needs 200 first touches a day, so pull 1,000 prospects for the first week, not 20,000:

```text
query_lead_database(title="VP Sales, Head of Sales", country=["United States"],
                    minEmployees=50, maxEmployees=200, keywords=["saas"],
                    hasEmail=true, excludeDelivered=true, limit=100, after="0")
```

Page with `pagination.next_after` until 1,000 rows. Lead Database rows count against the Growth plan's 100,000 new leads a day; no per-row charge.

**Step C. Validate before the first send.**

```text
validate_emails(emails=[...1,000 addresses...])   # 1,000 x $0.0072 = $7.20
```

Send only `valid`. During ramp weeks 1 and 2, keep `valid_catch_all` out entirely (house standard: new mailboxes get the safest rows). Treatment of every result: `references/deliverability-primer.md` section 5.

**Step D. Seed the roster's timezone column.** Lead Database rows carry `state` and `country`; Local Business Database rows carry `state`, `postal_code` and `country_code`. Group prospects by time zone so each mailbox's window matches its recipients.

**Worked cost estimate** for a 20-active-mailbox ramp (catalog price $0.0072 per validated email):

| Week | Cold sends a day | First touches a day (steps 2 and 3 take the rest) | New prospects that week | Validation cost |
|-|-|-|-|-|
| Ramp week 1 (10 a mailbox) | 200 | 200 | 1,000 | $7.20 |
| Ramp week 2 (20 a mailbox) | 400 | about 200 (follow-ups start) | 1,000 | $7.20 |
| Ramp week 3 (30 a mailbox) | 600 | 200 | 1,000 | $7.20 |
| Total | | | 3,000 | $21.60 |

First touches stay at 200 a day because steps 2 and 3 of earlier prospects fill the extra capacity. Show this before validating.

## Output Format

A Markdown roster following `templates/output-template.md`:

1. Summary.
2. Sender identities: person, title, mailboxes owned, photo consent.
3. Mailbox roster: one row per mailbox with every setting.
4. Signature block, exact text.
5. Warmup and ramp schedule with dates.
6. Sending rules: window, gaps, hourly and daily caps, time zones.
7. Reply monitoring: owner, check times, SLA, routing.
8. Rotation and retirement rules.
9. List feed and validation cost for the ramp weeks.

## Quality Check

- [ ] Every mailbox row names a real person who owns it.
- [ ] Every daily cap is 50 or less; ramp starts at 10.
- [ ] Every first cold send date is at least 14 days after the warmup start date.
- [ ] Signature includes a postal address and an opt-out line; no images.
- [ ] No Reply-To on the main domain.
- [ ] Sending window is in the recipient's time zone, weekdays only.
- [ ] Reserve mailboxes show cap 0 for cold sends and warmup on.
- [ ] Retirement triggers are numeric.
- [ ] `python3 scripts/check-output.py roster.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Invented personas and AI headshots | CAN-SPAM requires headers that identify the sender; prospects who check LinkedIn find nobody | Real team members, real photos |
| Warmup turned off the day campaigns start | Volume drops by the warmup amount and history thins | Keep warmup running at a lower rate (house standard: 10 a day) |
| Same cap for a 3-day-old mailbox and a 60-day-old one | New mailboxes have no history | Cap by mailbox age per the ramp table |
| HTML signature with logo and 4 links | Images and links add spam signals and tracked redirects | Plain text, one plain link at most |
| Reply-To set to `sales@maincompany.com` | Ties the cold domain to the main domain in every header | Replies stay on the sending mailbox; forward copies if needed |
| Sending 9:00 to 9:05 in one burst | Spikes look automated; Google warns against sudden volume jumps | Spread with 2 to 6 minute random gaps |
| Follow-up sent from a different mailbox than step 1 | The thread breaks and the prospect sees a stranger | Pin each lead to its first-touch mailbox |
| Nobody reads the unified inbox on Friday | Positive replies go cold | Named owner and check times |
| Recovery email on a personal Gmail of a rep who leaves | Lost account access | Recovery to an ops-controlled address on the main domain |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Which source backs which rule, routing table |
| `references/mailbox-setup-runbook.md` | Identity, address formats, signature templates, photo, security, reply routing, Google and Microsoft click paths |
| `references/warmup-and-ramp.md` | Ramp tables, per-sequencer warmup settings, gates between steps |
| `references/rotation-and-retirement.md` | Rotation groups, lead pinning, pause and retire steps, replacement timing |
| `references/deliverability-primer.md` | Shared: thresholds, validation results, warmup sources |
| `references/outbound-compliance-primer.md` | Shared: CAN-SPAM, CASL, GDPR and PECR rules for signatures and opt-outs |
| `references/scrapercity-catalog.md` | Shared: tool ids and prices |
| `references/scrapercity-platform.md` | Shared: database allowances |
| `templates/output-template.md` | Blank roster |
| `examples/worked-example.md` | Filled roster for 27 mailboxes across 9 domains |
| `scripts/check-output.py` | Run on the roster before delivery |

## Related Skills

- `domain-infrastructure` decides how many mailboxes exist and on which domains.
- `email-deliverability` watches the mailboxes once they send and triggers retirements.
- `sending-platforms` connects the mailboxes and sets the campaign schedule in the sequencer.
- `reply-handling` turns replies into meetings.
- `cold-email-copywriting` writes the messages these mailboxes send.
- `cold-email-strategy` sets the daily volume the ramp grows into.
