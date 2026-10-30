---
name: inbox-setup
description: >-
  Sets up each cold email mailbox after the domains exist: sender identity tied
  to a person on the team, address format, display name, plain-text signature
  with an opt-out line, profile photo, account security, Google Workspace and
  Microsoft 365 connection settings, reply routing, warmup on a 21-day standard
  path or a 14-day soft start, sending windows, daily caps, tenant quota checks,
  reply monitoring, rotation and retirement. Produces a compact mailbox roster
  with dated warmup waves. Use when the user has new mailboxes to configure,
  asks how to warm up inboxes, how many emails a mailbox can send, what
  signature or sender name to use, how to rotate inboxes, when to retire one,
  or what to set on mailboxes bought from a reseller.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.1.0"
  author: ScraperCity
  category: outbound
  tags:
    - mailboxes
    - warmup
    - inbox-rotation
    - signatures
    - sending-limits
    - cold-email-infrastructure
  related_skills:
    - domain-infrastructure
    - email-deliverability
    - sending-platforms
    - reply-handling
    - cold-email-copywriting
    - cold-email-strategy
  frameworks:
    - "Google - Email sender guidelines (ramp volume gradually, avoid spikes)"
    - "M3AAWG - Sender Best Common Practices v4.0 (Aug 2026), ramp and monitoring"
    - "Instantly - warmup settings and campaign readiness rules"
    - "Microsoft - Message Center MC1454397 new-tenant quotas and MC786329 SMTP AUTH (2026)"
    - "Google Workspace and Microsoft 365 - per-user sending limits and outbound spam policies"
    - "Alex Berman - warmup length, per-inbox daily volume and bounce lines"
    - "Instantly - account limits and campaign slow ramp"
    - "Apollo - hourly sending limits and gaps"
  shared_references:
    - deliverability-primer.md
    - scrapercity-catalog.md
    - scrapercity-platform.md
---

# Inbox Setup

## Overview

This skill configures every mailbox that will send cold email and schedules its first six weeks. The deliverable is a compact roster: one short row per mailbox (address, owner, provider, role, rotation group, warmup wave), one row per wave with its dates, and one block each for identity, signature, account settings, sending rules, reply monitoring and retirement.

It prevents four failures: brand-new mailboxes sending 50 cold emails in their first week; mailboxes with no named person reading replies, which loses the positive replies; a Microsoft 365 tenant that hits its new-tenant recipient quota mid-ramp; and an unaudited roster, where one bad mailbox drags its domain down before anyone notices.

## When to Use

- "I just created 15 mailboxes, what now?"
- "How long do I warm up?" or "can we start sooner?"
- "How many emails per day per inbox?"
- "What name and signature should the sender use?"
- "Should replies forward to my main inbox?"
- "How does inbox rotation work?" or "when do I retire an inbox?"
- "We bought inboxes from a vendor. What do we still need to set?"

Use a different skill for nearby jobs:

| Job | Skill |
|-|-|
| Domains, DNS records, mailbox count, provider split, tenant settings | `domain-infrastructure` |
| Ongoing bounce, complaint and blocklist incidents | `email-deliverability` |
| Sequencer choice, CSV import, webhooks | `sending-platforms` |
| Categorizing and answering replies | `reply-handling` |
| Writing the emails | `cold-email-copywriting` |

## Prerequisites

| Input | Default if unknown |
|-|-|
| Mailbox list from the sending plan (address, domain, provider, tenant, active or reserve) | Required |
| Domain registration dates and Microsoft tenant creation dates | Required; decide the path in step 6 |
| Team members who will send and read replies, with title | Required; at least 1 |
| Sending days and hours, reply check times, reply response target | Required; the team's own |
| Reserve share of domains | From the sending plan; at least 1 domain |
| Sequencer | Instantly |
| Recipient time zones | From the list's `state` or `country` columns |
| Who built the mailboxes: your admin or a vendor | Your admin |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Google and Yahoo sender requirements | Spam rate under 0.3% (Google asks for under 0.1%); unsubscribe requests processed within 2 days (Yahoo) and 48 hours (Google), so every signature carries a plain opt-out line and opt-outs are suppressed the same day. |
| Google Email sender guidelines | Raise volume slowly; sudden spikes such as doubling at once can trigger rate limits; on error 4.7.28 pause at least 10 minutes. |
| M3AAWG Sender BCP v4.0 (Aug 2026) | Start low and ramp, about six weeks on average; spread sends through the day; watch for volume jumps above 40%. |
| Instantly help center | Account ready after at least 2 weeks of warmup and a health score above 90% (readiness guide), 3 weeks for Instantly's own AirMail accounts; new-account warmup defaults: +1 a day, limit 10, reply rate 30%, and "Disable slow warmup" only for accounts already warmed (warmup settings); 30 campaign emails per account a day; Campaign Slow Ramp from 2 a day, +2 a day, 30 on day 15; campaigns auto-pause at 5% bounces after 200 sends; Inbox Placement tests cover Gmail and Microsoft, with two free one-time tests (Email Accounts > Deliverability Tests). |
| Smartlead help center | Keep warmup at 10 to 20 a day while campaigns run. |
| Google Workspace admin help | MX `smtp.google.com` priority 1; SPF `v=spf1 include:_spf.google.com ~all`; DKIM selector `google`, 2048-bit, available 24 to 72 hours after Gmail is turned on; DMARC starts at `p=none` with a `rua` report address; Postmaster Tools shows data only after the domain is verified by a TXT or CNAME record. |
| Microsoft Learn (SPF and DKIM for Microsoft 365) | SPF `v=spf1 include:spf.protection.outlook.com -all`; DKIM CNAMEs `selector1._domainkey` and `selector2._domainkey`, targets copied from the Defender portal. |
| Apollo, Email Sending Limits | 10 to 20 sends an hour per mailbox, 60 to 300 seconds apart. |
| Microsoft 365 Message Center MC1454397 and MC786329 (2026) | New tenants get 10% of the external recipient quota (500 x licenses^0.7 + 9,500 a day) for 30 days and 25% to day 60; trial tenants 500. Basic SMTP AUTH turns off by default after December 2026, so mailboxes connect by OAuth. |
| Google Workspace and Microsoft 365 limits | Workspace 2,000 messages per user per day (500 on trial); Exchange Online 10,000 recipients a day, 30 messages a minute; outbound spam policies take per-user hourly and daily limits. |
| Alex Berman (alexberman.com) | Warm up 2 to 4 weeks, start new domains at 10 to 20 a day, keep under 50 a day per inbox; bounces above 2% hurt reputation and above 5% are critical. |

## Workflow

### 1. Assign a named person to every mailbox

Each mailbox maps to a person on the team who reads (or has a teammate read) its replies; unread replies are lost meetings. One person can own several mailboxes across domains: `dana@getacme.com`, `dana.ortiz@tryacme.com`. How many depends on how fast they answer replies. Details: `references/mailbox-setup-runbook.md` section 1.

### 2. Set address and display name

Address formats, rotated across domains for the same person: `first@`, `first.last@`, `firstl@`. Display name is the person's own name, `Dana Ortiz`. State the display-name rule once in the roster, not on every row.

### 3. Write the signature

Plain text: name, title, company, opt-out line. Use at most one link (the main site, as plain text), and none in step 1 if link tracking is on, since click tracking wraps every link in a redirect (Alex Berman). Template in `references/mailbox-setup-runbook.md` section 3.

### 4. Account settings per provider

| Setting | Google Workspace | Microsoft 365 |
|-|-|-|
| Sign-in security | 2-Step Verification enforced on a cold email OU | MFA through security defaults or Conditional Access |
| Sequencer connection | OAuth, no app passwords | OAuth; Basic SMTP AUTH turns off by default after December 2026 |
| Volume guard | Sequencer caps | Outbound spam policy on the cold mailboxes: 20 external recipients an hour (Apollo's top hourly figure), 50 a day (Alex Berman's ceiling), forwarding off |
| Tenant-wide limit | None to plan for after the trial | External recipient quota by tenant age: check before each ramp step (step 6) |
| Photo and recovery | Owner's headshot; recovery to an ops address on the main domain | Same |

DNS: the deliverable lists every record with its exact value (MX, SPF, DKIM host and key length, DMARC with a report address), from the provider pages in Authoritative Foundations; for Microsoft MX and DKIM targets, name the admin page that shows them. Schedule DKIM generation 24 to 72 hours after Gmail is on, and a dated step that registers and verifies every sending domain in Google Postmaster Tools whenever its spam rate is a gate.

Click paths and record values: `references/mailbox-setup-runbook.md` sections 4 and 4a. Mailboxes a vendor built: section 8 of the same file.

### 5. Reply routing

Replies arrive in the sending mailbox. The sequencer's unified inbox reads all mailboxes in one place and stops the sequence on reply. Do not set a Reply-To on another address: the sequencer never sees those replies, so stop-on-reply fails. If the rep wants copies in their main inbox, add a forwarding rule for replies only. Options: `references/mailbox-setup-runbook.md` section 5.

### 6. Choose the warmup path and group mailboxes into waves

| Path | Warmup | Cold sends a mailbox | Gate |
|-|-|-|-|
| Standard | 21 days (Instantly's warmup for its own AirMail accounts, inside Alex Berman's 2 to 4 weeks) | Instantly's slow ramp from day 22: 2 on the first sending day, +2 each sending day, 30 on sending day 15 | Health score above 90% (Instantly readiness guide), a passing header test, and an inbox placement test that lands in the inbox at Gmail and Microsoft (Instantly Inbox Placement; name the tool) |
| Soft start | 14 days, never shorter (Instantly's minimum) | Same ramp from day 15 | The same gates plus a send file of `valid` addresses only; a domain that misses any gate stays on the standard dates. Raise the daily warmup limit from 10 to 20 at the mid-warmup check if every account is above 90%, so mailboxes carry 20 warmup a day into launch (top of Smartlead's 10 to 20 while campaigns run) |

A Microsoft tenant under 31 days old runs on 10% of its quota, so name the tenant's age when choosing the path. Mailboxes that start warmup the same day form a wave; the roster lists each wave's dates once. Reserves start warmup the same day as the first active wave, so a warmed reserve exists on the first cold send. For every Microsoft tenant, check before each ramp step that mailboxes x (cold cap + warmup) stays under the tenant's quota at its age. Tables, sequencer settings and the quota example: `references/warmup-and-ramp.md` sections 2 and 4. Raises above 30 follow the escalation test (section 8); a burned mailbox is retired and replaced from reserve, never re-warmed (section 9).

### 7. Sending window and caps

Sending days and hours are the team's choice, set in the recipient's time zone. Randomized gaps of 60 to 300 seconds between sends from one mailbox and 10 to 20 sends an hour per mailbox (Apollo). Daily cap 30 (Instantly), raised toward 50 (Alex Berman) only through the escalation test.

### 8. Rotation groups and reserves

Group mailboxes so each campaign spreads first touches across several domains; follow-ups stay with the mailbox that sent step 1. Reserve mailboxes stay in warmup with a cold cap of 0 from the first wave's start. Reserves: the sending plan's reserve share, at least one domain per rotation group so a promotion never leaves a group short (Growth Engine X keeps backup domains always warming and runs 50%); state the added seat cost in one line. A 1:1 backup doubles the seat bill. Rules: `references/rotation-and-retirement.md`.

### 9. Reply monitoring

Name the person who checks the unified inbox, the times they check it and the team's response-time target for positive replies, then measure time to first human answer. Opt-outs go to the workspace blocklist the same day, across every tool. Hand categorization to `reply-handling`.

### 10. Retirement rules

Write the conditions that pause or retire a mailbox before anything goes wrong: hard bounces over 5% after 200 sends (Alex Berman's critical line, Instantly's default auto-pause), with list re-validation from 2%; a 0.3% spam rate on its domain (Google); a provider suspension; or the person leaving the company. Steps: `references/rotation-and-retirement.md` section 4.

## ScraperCity Implementation

ScraperCity does not host mailboxes. It feeds the ramp with validated lists, so a new mailbox's first 200 sends carry close to zero bounces.

**Step A.** `check_wallet()` before any paid call.

**Step B. Pull only what the ramp can send.** In the first ramp week (2 rising to 10 a mailbox on 12 mailboxes, Monday to Friday) the campaign sends at most 360 emails, so pull 360 prospects for that week:

```text
query_lead_database(title="Head of Operations, VP Operations", country=["United States"],
                    minEmployees=20, maxEmployees=200, keywords=["logistics"],
                    hasEmail=true, excludeDelivered=true, limit=100, after="0")
```

Page with `pagination.next_after` until 360 rows. Lead Database rows count against the Growth plan's 100,000 new leads a day; no per-row charge.

**Step C. Validate before the first send.**

```text
validate_emails(emails=[...360 addresses...])   # 360 x $0.00169 = $0.61
```

Send only `valid`; bounces above 2% hurt a new domain's reputation (Alex Berman). Treatment of every result: `references/deliverability-primer.md` section 5.

**Step D. Seed the time zone split.** Lead Database rows carry `state` and `country`; Local Business Database rows carry `state`, `postal_code` and `country_code`. Group prospects by time zone so each campaign's window matches its recipients.

**Worked cost estimate** for a 12-active-mailbox ramp (catalog price $0.00169 per validated email):

| Ramp week | Cap per mailbox | Cold sends that week | New prospects that week | Validation cost |
|-|-|-|-|-|
| 1 | 2 rising to 10 | 12 x (2 + 4 + 6 + 8 + 10) = 360 | 360 | $0.61 |
| 2 | 12 rising to 20 | 12 x 80 = 960 | 600 | $1.01 |
| 3 | 22 rising to 30 | 12 x 130 = 1,560 | 600 | $1.01 |
| Total | | 2,880 | 1,560 | $2.63 |

Week 1 sends are almost all first touches, so one prospect per send is the most it can use. From week 2 new prospects hold at 120 a day (the steady-state 360 sends / 3 steps) and the rest of the capacity carries follow-ups; rows not sent carry into the next week. Show this before validating.

## Output Format

A Markdown roster following `templates/output-template.md`. Answer first: the title, then one line with the date and any stand-in names, then the Summary.

1. **Summary:** at most three sentences (the path chosen and its one reason), then the key-facts table (main domain, sequencer, active and reserve mailboxes, path, first cold send, full volume, steady-state sends). The path decision is written here only.
2. **Sender Identities:** person, title, mailboxes owned, reply backup; the address and display-name rules once.
3. **Mailbox Roster:** one row per mailbox with Mailbox, Owner, Provider, Role, Group and Wave only.
4. **Account Settings:** one row per setting, one column per provider in use, then the DNS record table with exact values.
5. **Signature Block**, exact text.
6. **Warmup and Ramp Schedule:** the wave table (dates once per wave), the ramp rows with campaign limits and gates, the dated setup steps (DNS, Postmaster Tools registration, warmup on, list loaded with `valid` rows only, gate check with the named placement test, first send), the warmup settings with Instantly's exact setting names, and the tenant quota check only when a mailbox is on Microsoft 365.
7. **Sending Rules:** the team's window, gaps, hourly and daily caps, time zones, tracking, each with its source.
8. **Reply Monitoring:** owner, check times, response-time target, opt-outs, routing.
9. **Rotation and Retirement** with numeric triggers and reserves.
10. **List Feed and Cost** only when the user asked for the list or its cost; otherwise the list is one dated setup step.

Economy rules (the checker enforces most):

- Each fact once. A date, gate or rationale that a table holds is not repeated in prose; no paragraph restates another.
- Every number names its source in the same line, by vendor and page: "above 90% (Instantly readiness guide)", "10 to 20 an hour (Apollo, Email Sending Limits)". A team choice says so.
- Each rule is written as a setting with its number. Leave out justification sentences, checks that came out "not needed", capacity arithmetic and warnings about things the plan does not do.
- Leave out legal content, vendor pitches, internal file paths, section numbers, skill names, agent tool ids and self-graded checklists. If nothing was run, say so once in the top line.

## Quality Check

- [ ] Every mailbox row names the team member who owns it and a wave.
- [ ] Every wave has a warmup start and a first cold send at least 21 days later on the standard path, or at least 14 days later when the soft start is named with its gates.
- [ ] The go-live gate includes a named inbox placement test; reserves start warmup with the first wave.
- [ ] DNS records carry exact values; Postmaster Tools registration is a dated step.
- [ ] Instantly settings use the exact names: "Disable slow warmup" off for new accounts.
- [ ] Every daily cap is 50 or less (Alex Berman); cold sends start at 20 a mailbox or fewer (Alex Berman's 10 to 20; Instantly's slow ramp starts at 2).
- [ ] Reserve mailboxes show cap 0 for cold sends and warmup on.
- [ ] Account Settings name the connection method (OAuth) for each provider; Microsoft rows include the outbound spam policy and the tenant quota check with numbers.
- [ ] Signature is plain text with an opt-out line; no images.
- [ ] No Reply-To on the main domain.
- [ ] Sending window is set in the recipient's time zone.
- [ ] Retirement triggers are numeric and name their source.
- [ ] No agent tool ids, file paths or skill names in the roster; no fact stated twice; no justification sentences.
- [ ] `python3 scripts/check-output.py roster.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Mailboxes with no named owner | Replies wait and positive ones go unanswered | A named team member reads each mailbox's replies |
| Cold sends on day 15 from domains bought that month, with no gate | Unknown domains start at a poor reputation | Standard 21-day path; soft start only with its gates passed |
| Microsoft tenant ramped without checking its quota | Under 31 days old it gets 10% of the standard external recipient quota, warmup included | Tenant quota check before each ramp step |
| Connecting Microsoft mailboxes with an app password or Basic SMTP AUTH | Off by default after December 2026 | OAuth |
| Warmup turned off the day campaigns start | Volume drops by the warmup amount and history thins | Keep warmup at 10 to 20 a day while campaigns run (Smartlead) |
| Same cap for a 3-day-old mailbox and a 60-day-old one | New mailboxes have no history | Cap by wave and ramp row |
| HTML signature with logo and 4 links | Click tracking wraps every link in a redirect | Plain text, one plain link at most |
| Reply-To set to `sales@maincompany.com` | The sequencer never sees those replies, so stop-on-reply fails, and every header names the main domain | Replies stay on the sending mailbox; forward copies if needed |
| Sending 9:00 to 9:05 in one burst | Google warns against sudden volume spikes | Random 60 to 300 second gaps, 10 to 20 an hour (Apollo) |
| Follow-up sent from a different mailbox than step 1 | The thread breaks and the prospect sees a stranger | Pin each lead to its first-touch mailbox |
| Resold mailboxes treated as fully yours | The vendor holds the admin account, DKIM and the tenant | Ask the reseller questions in `references/mailbox-setup-runbook.md` section 8; export replies before cancelling |
| Recovery email on a personal Gmail of a rep who leaves | Lost account access | Recovery to an ops-controlled address on the main domain |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Which source backs which rule, routing table |
| `references/mailbox-setup-runbook.md` | Identity, address formats, signature templates, photo, security, Microsoft connection and outbound policy, reply routing, resold mailboxes |
| `references/warmup-and-ramp.md` | Standard and soft-start ramps, waves, the Microsoft tenant quota check, per-sequencer warmup settings, escalation and burned-mailbox rules |
| `references/rotation-and-retirement.md` | Rotation groups, lead pinning, pause and retire steps, reserves and replacement timing |
| `references/deliverability-primer.md` | Shared: thresholds, validation results, warmup sources |
| `references/scrapercity-catalog.md` | Shared: tool ids and prices |
| `references/scrapercity-platform.md` | Shared: database allowances |
| `templates/output-template.md` | Blank roster |
| `examples/worked-example.md` | Illustrative example: 18 mailboxes on Google and Microsoft 365 across 6 domains |
| `scripts/check-output.py` | Run on the roster before delivery |

## Related Skills

- `domain-infrastructure` decides how many mailboxes exist, on which domains and tenants.
- `email-deliverability` runs incidents once the mailboxes send and triggers retirements.
- `sending-platforms` connects the mailboxes and sets the campaign schedule in the sequencer.
- `reply-handling` turns replies into meetings.
- `cold-email-copywriting` writes the messages these mailboxes send.
- `cold-email-strategy` sets the daily volume the ramp grows into.
