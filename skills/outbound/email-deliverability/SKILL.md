---
name: email-deliverability
description: >-
  Keeps a running cold email program in the inbox: a pre-send gate (authentication,
  one-click unsubscribe, list validation with ScraperCity's Email Validator and a
  rule for every result, catch-all handling), weekly monitoring with seed tests,
  Google Postmaster Tools, Yahoo CFL, Microsoft SNDS and blocklist checks, an
  incident runbook for bounce spikes, spam folder placement, complaint spikes and
  blocklisted domains, and hard stop rules tied to the Google, Yahoo and Microsoft
  sender requirements. Produces either a dated incident recovery plan (ranked
  causes with the check that confirms each, a day-by-day restart calendar with
  send numbers) or a weekly health report with a status per domain. Use when the
  user asks why emails go to spam, sees open rates or replies collapse, bounces or
  a paused campaign, wants a deliverability audit or health check, needs to validate a list
  before sending, or asks about Gmail, Yahoo or Outlook sender rules.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags:
    - deliverability
    - bounce-rate
    - spam-rate
    - postmaster-tools
    - blocklists
    - email-validation
    - seed-testing
    - incident-response
  related_skills:
    - domain-infrastructure
    - inbox-setup
    - sending-platforms
    - email-list-cleaner
    - cold-email-list
    - cold-email-copywriting
    - reply-handling
    - cold-email-strategy
  frameworks:
    - "Google - Email sender guidelines and FAQ (Feb 2024 rules, Nov 2025 enforcement ramp)"
    - "Google - Postmaster Tools compliance status and spam rate dashboards"
    - "Yahoo - Sender Hub best practices and Complaint Feedback Loop (2024)"
    - "Microsoft - Outlook requirements for high-volume senders (enforced 5 May 2025) and delist portal"
    - "IETF - RFC 8058 one-click unsubscribe; RFC 7208, RFC 6376, RFC 7489 and RFC 9989"
    - "Spamhaus, Barracuda and SpamCop - blocklist listing and removal rules"
    - "M3AAWG - Sender Best Common Practices v4.0 (Aug 2026)"
    - "Apple - Mail Privacy Protection (remote content loaded on arrival) and Microsoft - Outlook image blocking default"
    - "Alex Berman - hard bounces under 2%, new mailboxes start at 10 to 20 a day and ramp over 2 to 4 weeks, under 50 a day per inbox"
    - "Instantly - high bounce auto-pause (5% after 200 sends) and account readiness (2 weeks of warmup, health score above 90%)"
    - "M3AAWG - DKIM Key Rotation BCP (rotate at least every six months)"
  shared_references:
    - deliverability-primer.md
    - list-quality-standard.md
    - scrapercity-catalog.md
    - scrapercity-platform.md
---

# Email Deliverability

## Overview

This skill runs the health side of a cold email program once the domains and mailboxes exist. It produces one of two deliverables. When something broke, an incident recovery plan: a verdict, what stops today, causes ranked with the check that confirms or clears each, why the open rate cannot decide it, list re-validation with its cost, and a dated day-by-day restart calendar with sends per inbox and a gate on every step. For routine checks, a deliverability health report: authentication and compliance status per domain, list validation results with an action for every row, seed placement results, domain health with a green, yellow or red status, blocklist checks, open incidents with their runbook step, and the stop rules in force.

It prevents five expensive mistakes: answering an incident with a long audit instead of a dated plan, sending an unvalidated list and burning a domain on bounces, reading "No data" in Postmaster Tools as "healthy", answering spam folder placement by buying more domains (the new domains get the same list and copy and burn the same way), and keeping a domain sending after Google's 0.3% spam line, which removes it from mitigation until it holds below 0.3% for 7 consecutive days.

The shared `references/deliverability-primer.md` holds the provider rules, bounce and complaint formulas, validation buckets, warmup sources and standing thresholds. This skill applies them; it does not restate them.

## When to Use

- "Why are my emails going to spam?" or "my reply rate dropped".
- "Instantly paused my campaign for bounces" or "bounce rate is 4%".
- "Run a deliverability audit" or "weekly health check".
- "Validate this list before I send" or "what do I do with catch-alls?"
- "Do the Gmail and Yahoo bulk sender rules apply to cold email?" or "what changed with Outlook in 2025?"
- "Is my domain blacklisted?" or "how do I get delisted?"
- An SMTP code in a bounce: `5.7.27`, `4.7.28`, `4.7.32`, `5.7.515`, `5.7.606`.
- "Open rates fell off a cliff" or "opens dropped and bounces jumped this week": write the incident recovery plan; check replies and seeds before trusting the open rate.

Use a different skill for nearby jobs:

| Job | Skill |
|-|-|
| Buying domains, DNS records, mailbox counts | `domain-infrastructure` |
| Warmup schedule, caps, rotation and retirement of mailboxes | `inbox-setup` |
| Sequencer choice, CSV mapping, webhooks, suppression sync | `sending-platforms` |
| Cleaning and bucketing a large list as a deliverable | `email-list-cleaner` |
| Building the send-ready file | `cold-email-list` |
| Rewriting copy that triggers filters | `cold-email-copywriting` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Sending domains and mailboxes (roster from `inbox-setup`) | Scope of the report | Required |
| Sequencer and plan | Where bounce data and auto-pause live | Instantly |
| Access to DNS, Postmaster Tools, sequencer analytics | Checks need them | Ask; list anything not checked in one line of the report |
| The list to send next (CSV) | Pre-send validation | Required for a pre-send gate |
| Re-check window for validation | Rows last validated before it are re-validated before sending | Ask; no source publishes one, so set it from the bounce rate of re-sent rows by age |
| Sends, bounces and replies per mailbox since the last review, and for the weeks before any incident | Domain status and the pre-incident baseline | Export from the sequencer |
| Seed mailboxes | Placement tests | One seed at each provider the list uses (monitoring section 3) |
| Dedicated IPs, if any | SNDS and IP blocklists apply only then | None (Workspace or Microsoft 365) |
| One owner with authority to pause any domain | Containment needs one name, not a meeting | "The outbound lead, unless you name someone else today" |
| Linked domains (main site, calendar link, tracking host) | Blocklist checks cover every domain in the message, not only senders | Read them from touch 1 |

For an incident plan only the symptom numbers are required (inboxes, domains, daily cap, the rates that moved). Everything else becomes a confirming check in the plan or a labeled assumption.

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Google Email sender guidelines and FAQ | All senders: SPF or DKIM, PTR, TLS, spam rate under 0.3%. Increase volume slowly; doubling volume at once can cause rate limiting or reputation drops; on `4.7.28` stop sending for at least 10 minutes. 5,000+ a day to personal Gmail: SPF and DKIM, DMARC aligned, one-click unsubscribe, unsubscribes honored in 48 hours. Spam rate is calculated daily; keep it under 0.1%. At 0.3% a bulk sender loses mitigation until 7 consecutive days under 0.3%. Guidelines do not apply to mail sent to Workspace accounts. Enforcement ramps up from November 2025 with temporary and permanent rejections. |
| Google Postmaster Tools | Compliance status per requirement, spam rate on DKIM-authenticated mail, delivery errors. Rolling average up to 7 days; low-volume days may show no data. |
| Yahoo Sender Hub | Spam rate under 0.3% measured on inbox-delivered mail; CFL enrollment for every DKIM domain; RFC 8058 POST highly recommended; unsubscribes processed within 2 days; remove invalid addresses promptly. |
| Microsoft Outlook high-volume sender requirements | From 5 May 2025, domains sending 5,000+ a day to Outlook.com, Hotmail and Live need SPF, DKIM and DMARC `p=none` or stronger with alignment, or get `550; 5.7.515`. Microsoft also recommends reply-capable sender addresses, a visible unsubscribe and list hygiene. |
| RFC 8058 | One-click unsubscribe: `List-Unsubscribe` with an HTTPS URI plus `List-Unsubscribe-Post`, POST without cookies or redirects, both headers covered by DKIM. |
| RFC 7208, 6376, 7489 and 9989 | One SPF record under 10 lookups, DKIM signing, one DMARC record with alignment and `rua`. |
| Spamhaus, Barracuda, SpamCop, Microsoft delist portal | How listings happen and how removal works, with stated timings. |
| M3AAWG Sender BCP v4.0; M3AAWG DKIM Key Rotation BCP | Ramp gradually and treat volume jumps as a warning sign. Rotate DKIM keys at least every six months. |
| Apple Mail Privacy Protection; Microsoft Outlook picture download default | Apple loads remote content when a message arrives, read or not; Outlook blocks automatic picture downloads by default. Opens cannot decide placement. |
| Alex Berman (alexberman.com) | Keep hard bounces under 2%. New mailboxes start at 10 to 20 a day and ramp over 2 to 4 weeks; under 50 a day per inbox. Verify the list before sending. |
| Instantly help center | High bounce auto-pause at 5% once a campaign has sent 200 emails; an account is ready for campaigns after at least 2 weeks of warmup and a health score above 90%. |

Detail, dates and links: `references/deliverability-primer.md` and `references/framework-notes.md`.

## Workflow

### 1. Classify the request

| Request | Run | Deliverable |
|-|-|-|
| Something broke (opens or replies collapsed, bounces, spam, block, rejection) | Steps 8, 8a and 8b | Incident recovery plan |
| Opens fell; the user says replies, bounces and seeds held | Step 8a | Incident recovery plan, measurement branch (short) |
| New list or new campaign | Steps 2 to 4 | Health report |
| Weekly or monthly check | Steps 5 to 7 | Health report |
| Six-month audit due, or the first month after a sequencer migration | Step 10, then steps 5 to 7 | Health report |

When the user gives symptom numbers, answer with the plan in the first reply. Restate their setup as counts (12 inboxes x 30 a day x 5 weekdays = 1,800 sends; 4% of that = 72 hard bounces), state at most 3 assumptions in one line, and put the facts that would change the ranking in the Diagnosis "Clears it" column, once. Do not open with a questionnaire.

### 2. Authentication and unsubscribe check

For every sending domain: one SPF record, DKIM signing on, one DMARC record with `rua`, From aligned, and a header test from every mailbox showing `spf=pass`, `dkim=pass header.d=<domain>`, `dmarc=pass`. Turn on the sequencer's unsubscribe header where it exists and confirm `List-Unsubscribe-Post: List-Unsubscribe=One-Click` in a raw test message. Every email body carries a plain opt-out line. Gate table: `references/monitoring-and-testing.md` section 1. When a check fails, put the exact records to publish in the report: the copy-paste SPF, DKIM and DMARC values and the Google Admin console DKIM path are in `references/incident-runbooks.md` R6.

### 3. Validate the list and route every result

Run `validate_emails` on every address last checked before the user's re-check window (ask for it; no source publishes one, so set it from the bounce rate of re-sent rows by age). Route each `email_result` per `references/deliverability-primer.md` section 5, then apply the extra rules in `references/monitoring-and-testing.md` section 2: send order by `email_quality`, catch-all rows in their own campaign, gateway-aware reporting from `sc_mx_security_gateway`.

### 4. Seed test before launch

Send the live touch 1 from one mailbox per domain to a seed at each provider the list uses (personal Gmail, Workspace, Outlook.com, Microsoft 365, Yahoo; read the mix from `sc_mx_provider`). Launch when it reaches the inbox at every seed provider; a provider in spam gets the spam-folder runbook first. Protocol: monitoring section 3.

### 5. Collect the weekly numbers

Per mailbox and per domain, last 7 days and last 200 sends: sends, hard bounces, soft bounces, replies, opt-outs, auto-pauses. Per domain: Postmaster compliance status and spam rate (or "No data"), Yahoo CFL complaints, DMARC pass share from `rua` reports. Weekly review agenda: monitoring section 6.

### 6. Check blocklists

Every sending domain on check.spamhaus.org (DBL). Then every other domain a recipient's filter sees in the message: the tracking host's domain (`inst.<sending domain>` sits on the sending domain; with no custom tracking domain, the sequencer's shared tracking domain), the main site in the signature, a calendar or booking link, and any other link. Check those on the Spamhaus DBL, SURBL (surbl.org lookup) and URIBL (admin.uribl.com), which list domains found in message bodies and links. A listed linked domain hurts every mailbox that carries the link. Dedicated or private IPs also go on Barracuda, SpamCop and Spamhaus IP lists. Workspace and Microsoft 365 senders do not own their IPs, so IP checks do not apply; say so in one line, not a table. Monitoring section 5.

### 7. Score each domain

| Status | Rule (any one condition) |
|-|-|
| Red | Hard bounce rate 2% or more (Berman's line); spam rate 0.3% or more on any day (Google, Yahoo); listed on the Spamhaus DBL; authentication failing; provider rejections (`5.7.x`) |
| Yellow | Spam rate 0.1% or more on any day (Google's target); seed test in spam at any provider; a mailbox paused this week; Postmaster "Needs work" |
| Green | No condition above applies |

A domain showing "No data" in Postmaster still needs bounces, seeds and replies in range to be green.

### 8. Diagnose the incident

Rank causes by evidence: the cause must explain every symptom given, be shared by every affected domain, and have changed inside the window. Four domains failing the same week share a cause (list, copy, tracking or linked domain, a DNS edit, a settings change). Each ranked cause carries the check that confirms it and the result that clears it, from `references/recovery-plans.md` section 2. The common combination, opens collapsing on every domain plus hard bounces at 2% or more at flat volume, ranks: bad or stale list batch; spam placement following it; tracking or linked domain flagged or broken; authentication broken by a DNS edit; Spamhaus DBL listing. A Postmaster spam rate under 0.1% does not clear spam placement: Google counts only mail that reached the inbox.

Confirm the incident owner: one named person with authority to pause any domain or campaign without asking anyone. Match the symptom in `references/incident-runbooks.md` (R1 bounce spike, R2 spam folder, R3 complaint spike, R4 blocklisted domain, R5 blocklisted IP, R6 authentication rejection, R7 Gmail `4.7.28` reputation deferral and other rate limits, R8 mailbox suspended, R9 measurement problem only). Contain first, then diagnose, fix, and resume only on the written resume condition. What stops in the first hour, and what keeps running (warmup at its current setting, the opt-out line, same-day suppression): `references/recovery-plans.md` section 4.

Keep a backup capacity plan in every health report (in an incident plan, one line inside the retire rule): which warmed reserve domains can take a paused domain's volume, and how many sends a day they cover. Never buy replacement domains during an incident before the cause is found; the new domains inherit the list and copy and burn the same way.

### 8a. Rule out a measurement problem

Opens are the weakest signal. Apple Mail Privacy Protection downloads remote content when a message arrives, whether or not anyone reads it; Outlook blocks automatic picture downloads by default; security filters open and click within seconds of delivery. A drop says something changed without saying what. Decide with seed placement, human replies per 1,000 sends against the pre-incident baseline, and hard bounces with their SMTP codes; every incident plan says so in three or four sentences.

| Opens | Human replies per 1,000 sends | Bounces and seeds | Read it as | Next step |
|-|-|-|-|-|
| Down | Steady against the pre-incident baseline | Steady | Measurement problem only: pixel blocked, tracking domain changed or broken, Apple MPP share moved, link tracking stripped | R9: check the tracking CNAME and the sequencer's tracking setting. No volume change |
| Down | Down | Seeds in spam or bounces up | Placement problem | R2, then R1 or R3 as the numbers say |
| Steady or up | Down | Steady | Copy, offer or list fit | Copy and targeting review; no deliverability action |
| Down | Down at one recipient provider only (`sc_mx_provider`) | Seeds in spam at that provider | Provider-specific placement | R2, Microsoft or Google branch |

### 8b. Write the dated recovery calendar

Build it from today's date with weekday names, following `references/recovery-plans.md` section 6:

| Day | Action | Sends per inbox |
|-|-|-|
| 0 (today) | Stop, export the bounce log with codes and per-inbox numbers for the weeks before the drop, run the confirming checks | 0 |
| 1 | Re-validate the queued rows (step 3 routing; catch-alls wait), fix the cause, seed test 1 | 0 |
| 2 | Restart if seed test 1 reached the inbox at every seed provider | 10 (low end of Berman's 10 to 20 start) |
| Before the first step up | Seed test 2 | 10 |
| Weekly, over 2 to 4 weeks | Step up in equal weekly steps to the previous cap (Berman's 2 to 4 week ramp); no step more than doubles the last (Google) | Previous cap, under 50 (Berman) |

Every row shows total sends a day (inboxes x sends per inbox). Define the numeric gate once, in a "Standard gate" line above the table: hard bounces under 2% over the last 200 sends (Berman's line, Instantly's window), zero `4.7.28`, spam rate under 0.1% (Google's sender guidelines). Rows say "standard gate" plus anything that day adds (seed test in the inbox at every provider). Add the back-off rules (one step back on a 2% bounce rate, stop a domain on `5.7.28`, 0.3% spam or a DBL listing) and the keep, rest or retire rule for each domain (`references/recovery-plans.md` section 6b). Reserve domains start warming only after the cause is written down. An incident plan restarts every inbox at 10, because placement is unproven until the seed tests pass.

### 9. Apply the stop rules

| Stop rule | Threshold | Action | Basis |
|-|-|-|-|
| Spam rate, act | 0.1% or more on any day on a domain | Lower that domain's volume and run the complaint checks | Google sender guidelines (keep under 0.10%) |
| Spam rate, stop | 0.3% on any day | Stop the domain; Google restores mitigation only after 7 consecutive days under 0.3% | Google FAQ; Yahoo 0.3% |
| Bounces | 2% or more over the last 200 sends, per campaign or mailbox | Pause it, re-validate unsent rows | Berman under 2%; Instantly's 200-send window |
| Catch-all campaign | 2% or more over 200 sends | Pause catch-all sends | Berman; Instantly |
| Authentication | Any failing check or `5.7.515`, `5.7.27`, `5.7.30` | Stop the domain until the header test passes | Google, Microsoft |
| Gmail rate limit | Any `421 4.7.28` on a domain | Stop that domain's sends for at least 10 minutes, then lower its volume and run the complaint checks; `550 5.7.28` (unusual rate of unsolicited mail, blocked) stops the domain | Google sender guidelines and SMTP error reference |
| Blocklist | Domain on the Spamhaus DBL | Stop every mailbox on the domain | Spamhaus |
| Opt-outs | Any opt-out not suppressed the same day in every tool | Stop new launches until the sync is fixed | Google 48 hours and Yahoo 2 days are the outer limits |
| Unvalidated rows | Any row in a send file without `email_status = valid` inside the re-check window | Do not launch | Berman: verify before sending |

### 10. Six-month audit

Every six months, the DKIM rotation interval M3AAWG sets, run the five audit checks in `references/monitoring-and-testing.md` section 7: DNS records against the `domain-infrastructure` plan, DKIM key age (rotate at least every six months per M3AAWG), a DMARC `rua` review since the last audit for unknown senders in a report service (dmarcian, Postmark DMARC, Valimail Monitor or EasyDMARC, compared in section 8), a placement test across Google, Microsoft and Yahoo seeds, and caps against actual volume. Each row gets a run date, a result and a next due date in the report.

### 11. Write the report and hand off

Fill `templates/incident-plan-template.md` for an incident or `templates/output-template.md` for a health report, run `scripts/check-output.py` on it, and hand mailbox actions (pause, rest, retire, re-ramp) to `inbox-setup`, DNS fixes to `domain-infrastructure`, copy rewrites to `cold-email-copywriting`. In the report itself, describe each handoff by the work to be done ("re-ramp the two mailboxes from 10 a day"), never by a skill name or runbook number.

## ScraperCity Implementation

**Step A. Wallet.** `check_wallet()` before any paid run; show the estimate and wait for a go-ahead on anything over about $5.

**Step B. Validate.**

```text
validate_emails(emails=["ray@reyesair.example", "maria@lakelinefamilydental.example", ...])
check_run_status(runId)          # first check after 30 s, then every 30 s
download_results(runId, outputPath="/abs/path/validated-ledgerline-wk49-20261207.csv")
```

CLI:

```bash
npx scrapercity email-validate ray@reyesair.example maria@lakelinefamilydental.example
npx scrapercity status <runId>
npx scrapercity download <runId> -o validated.csv
```

REST: `POST /api/v1/scrape/email-validator` with `{"emails": [...]}`, poll `GET /api/v1/scrape/status/{runId}`, download `GET /api/downloads/{runId}`.

Read the CSV header row before mapping. Columns this skill uses: `email_result`, `email_quality`, `sc_is_catch_all`, `sc_mx_provider`, `sc_mx_security_gateway`.

**Step C. Route results.**

| `email_result` | File | Next step |
|-|-|-|
| `valid` | Send file, ordered by `email_quality` | Upload via `sending-platforms` |
| `valid_catch_all` | Catch-all file | Separate campaign |
| `unknown` | Hold file | Re-validate once |
| `invalid` | Suppression | Optional `find_emails` for a replacement |
| `disposable` | Suppression | None |

**Step D. Replace invalid addresses on high-value accounts.**

```text
find_emails(contacts=[{"first_name": "Ray", "last_name": "Reyes", "domain": "reyesair.example"}, ...])
```

$0.05 per email found, free when nothing is found, and every found email is validated at lookup. REST: `POST /api/v1/scrape/email-finder` with the same `contacts` array. The CLI `email-find` command also reads a CSV with `first_name,last_name,domain` columns.

**Step E. Split reporting by recipient provider.** Group sends and replies by `sc_mx_provider` (Google, Microsoft, other) and by `sc_mx_security_gateway`. A provider or gateway segment with no replies while the others reply gets a seed test at that provider first.

**Worked cost estimate** (catalog prices, a 6,000-row list for next month):

| Line | Count | Unit | Cost |
|-|-|-|-|
| `validate_emails`, full list | 6,000 | $0.0072 | $43.20 |
| Re-validate `unknown` once (assume 3%) | 180 | $0.0072 | $1.30 |
| `find_emails` on `invalid` rows with a name and domain (assume 5% invalid) | 300 inputs | $0.05 per email found | $15.00 ceiling if every input is found |
| Total ceiling | | | $59.50 |

Expected spend is lower: `find_emails` charges nothing for inputs it cannot find. Compare with the cost of one burned domain: a $11.08 domain, its 2 to 3 mailbox seats for the rest of the term, and 2 to 4 weeks of warmup (Berman) before a replacement can send.

## Output Format

### A. Incident recovery plan (something broke)

One Markdown plan following `templates/incident-plan-template.md`, under about 1,500 words. A setup line first: owner with pause authority, inboxes, domains, cap, sends a week, and at most 3 assumptions.

Owner defaults to "the outbound lead, unless you name someone else today"; the sequencer defaults to Instantly, with one line saying which two settings to find in any other sequencer (custom tracking domain, bounce auto-pause).

1. Verdict: the likeliest cause and why the user's numbers point to it, what stops today, the earliest restart date and its gate, the one decision needed.
2. Stop Now: dated bullets (pause, suppress bounces everywhere, quarantine the batch, no new domains, open tracking off, the bounce auto-pause lowered to 2% with its menu path) and what keeps running (warmup at its current setting, the opt-out line, same-day opt-out suppression).
3. Diagnosis: at least 3 causes ranked 1, 2, 3, each with why it fits, the result that confirms it and the result that clears it. Under it, the checks once, numbered, as commands (bounce log read by its text, `dig` lines, header test, blocklist lookups, a named seed test), then the fix for each ranked cause written out in full: SPF and DMARC records ready to paste, the Google Admin DKIM path, the tracking CNAME.
4. Measurement: three or four sentences on why opens cannot decide it (Apple Mail Privacy Protection, Outlook image blocking, security filters) and the three deciding signals: seed placement, replies per 1,000 sends, hard bounces with codes.
5. List Re-validation: rows, count, cost at $0.0072, routing per result.
6. Recovery Plan: the standard gate line once with its numbers and sources, then a dated table with weekday names, sends per inbox, total sends a day, and a gate per sending row ("standard gate" plus that day's extra).
7. Resume and Retire Rules: what to do when a gate is missed (without restating the gate numbers) and the keep, rest or retire rule, decided by seeds and bounces.
8. Next Check-in: date, time, the numbers to bring, decisions pending. Not a second list of what would change the ranking.

No six-month audit, records for causes the plan does not rank, monitoring dashboards or framework lists in an incident plan. Each check, gate and fact appears once.

### B. Weekly health report

One Markdown report following `templates/output-template.md`:

1. Summary: period, domains in scope, statuses, incidents, what the user must decide.
2. Scope: domains, mailboxes, sequencer, period, the one owner with authority to pause any domain, and the backup capacity (warmed reserves and the sends a day they cover).
3. Authentication and Unsubscribe: per domain SPF, DKIM, DMARC, alignment, unsubscribe header, Postmaster compliance status. When a check fails, the exact records to publish follow the table.
4. List Validation: counts per result bucket with the action and cost.
5. Placement Tests: seed results per provider per domain.
6. Domain Health: per domain sends, bounce rate, spam rate, replies, status and action.
7. Blocklist Checks: every sending domain and every linked domain (tracking host, main site, booking link) on the Spamhaus DBL, SURBL and URIBL; dedicated IPs when there are any.
8. Incidents and Actions: incident type, trigger, action, owner, resume condition, status.
9. Stop Rules: each rule, its threshold, its source and whether it fired.
10. Six-Month Audit: the five checks, each with run date and next due date.
11. Next Review: date and checks.

### Rules for both

- What was not checked goes in one line ("Not checked: SNDS, no dedicated IPs"). Never a table of "Not run" or "Not applicable" rows.
- The reader is the sender, not this repo: no file paths, runbook numbers (R1 to R9), section numbers, skill names or tool ids. Name the incident type and the product ("Email Validator"), and say "re-ramp the two mailboxes from 10 a day" instead of naming a skill.
- Label every number the user did not give as an assumption, and name the source of each threshold once by its document ("Google's sender guidelines", "Instantly help", "Alex Berman"), never a bare "(Google)".
- Every message, record or setting the plan tells the user to change is written out (the record value, the menu path), not "fix DNS".
- No self-grading checklist in the deliverable.

## Quality Check

Incident recovery plan:

- [ ] The first reply is the plan; the user's numbers are restated as counts (sends a week, bounce count).
- [ ] At least 3 causes ranked in order, each with a confirming check and a clearing result; the rank 1 cause explains every symptom given.
- [ ] Stop Now is dated, keeps warmup at its current setting and the opt-out line, and buys no domains before the cause is written down.
- [ ] Measurement names Apple Mail Privacy Protection and says seeds, replies per 1,000 sends and bounces decide.
- [ ] Re-validation count x $0.0072 is computed right; catch-alls wait until the last step.
- [ ] Every calendar row has a date; totals equal inboxes x sends per inbox; restart at 10 to 20 a day (Berman); no step more than doubles (Google); the standard gate is defined once with its numbers.
- [ ] The checks are numbered commands; each ranked cause has its fix written out (records, Admin path, CNAME); the seed test names its tool or seed accounts.
- [ ] `python3 scripts/check-output.py plan.md` prints PASS (it also enforces the length cap).

Weekly health report:

- [ ] Every sending domain has a row in Authentication, Domain Health and Blocklist Checks.
- [ ] Every domain status follows the step 7 rules: 2% bounces or 0.3% spam is never green or yellow.
- [ ] Validation bucket counts add up to the total validated, and the cost uses $0.0072 per email.
- [ ] No row without `valid` status is in a main send file.
- [ ] Every incident names its type, an owner and a resume condition; Scope names one owner with pause authority and the backup capacity.
- [ ] Blocklist Checks cover every linked domain on the Spamhaus DBL, SURBL and URIBL, not only sending domains.
- [ ] Opens are never read alone: any open-rate drop is checked against replies first.
- [ ] "No data" from Postmaster is reported as no data, not as a pass.
- [ ] Opt-outs suppressed the same day in every tool, with the count.
- [ ] Six-Month Audit has all five checks with dates; the DKIM row shows key age under six months or a booked rotation; the placement row names Google, Microsoft and Yahoo.
- [ ] `python3 scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Answering an incident with the weekly report format | A sender with 4% bounces gets tables of unchecked rows and an audit instead of what to do today | Incident recovery plan: verdict, stop list, ranked causes with checks, dated calendar |
| Judging the recovery by open rate, with tracking left on | Apple MPP loads images on arrival and Outlook blocks them by default, so opens move without placement moving; the pixel and tracking host add filter signals | Open tracking off; seeds, replies per 1,000 sends and bounce codes decide |
| Reading a low Postmaster spam rate as proof of inbox placement | Google computes it on inbox-delivered mail only; heavy spam filtering makes it look low | Seed test the live touch 1 |
| Restarting at the old cap after the fix | The domains have not proven recovery and a second spike follows | Restart at 10 a day per inbox and step up weekly behind numeric gates, no step more than double the last |
| Sending an unvalidated or stale list | Closed mailboxes bounce and push the campaign past the 2% line | Re-validate rows older than the re-check window before the first send |
| Mixing catch-alls into the main campaign | One accept-all company that rejects later pushes the campaign's bounce rate past the auto-pause line | Separate catch-all campaign |
| Re-validating catch-alls hoping for a different answer | Pays $0.0072 again for the same result | `find_emails` for a second address, or accept the risk in the catch-all campaign |
| Treating Postmaster "No data" as healthy | Low personal-Gmail volume shows nothing | Judge by seeds, bounces and replies per provider |
| Buying new domains when placement drops | The cause (list, copy, volume) moves to the new domains and burns them too | Run R2 and fix the cause; promote an already-warmed reserve if capacity is short |
| Delisting before fixing the cause | Relisting follows and the second removal is harder | Fix, then request removal |
| Treating Gmail `4.7.28` as a harmless retry | Gmail's text says it detected an unusual rate of email and rate limited it, and `5.7.28` is the block for unsolicited mail | Send nothing from the domain for 10 minutes (Google's sender guidelines), lower its volume, run the complaint checks (R7) |
| Reading an open-rate drop as a deliverability problem | A blocked pixel or a broken tracking CNAME drops opens while replies hold | Compare replies per 1,000 sends first (step 8a) |
| Checking only the sending domains for listings | A listed booking or tracking domain in the body hurts every mailbox that carries it | DBL, SURBL and URIBL on every linked domain |
| One unsubscribe list per campaign | An opt-out in one campaign gets mailed by another | Workspace-wide blocklist, synced from every campaign |
| No DKIM rotation since launch | M3AAWG says rotate at least every six months | Six-month audit check 2; rotation booked with a new selector |
| Reading raw `rua` XML by hand, or not at all | Unknown tools sending as your domain go unseen | A DMARC report service, reviewed at each audit for unknown sources |
| Raising caps the week after an incident | The domain has not proven recovery | Two seed tests in the inbox at every provider and a week inside the gates first |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Which source backs which rule, conflicts between sources, routing table |
| `references/monitoring-and-testing.md` | Pre-send gate, catch-all and gateway rules, seed test protocol, Postmaster, CFL, SNDS, blocklist checks, weekly review, six-month audit, DMARC report services, opt-out rate |
| `references/recovery-plans.md` | Incident plan: fast intake, cause ranking with confirming checks, open-rate caveats with sources, stop-now list, re-validation, dated recovery calendar, back-off and keep, rest or retire rules |
| `references/incident-runbooks.md` | Incident command (owner, backup capacity), bounce spike, spam folder, complaint spike, blocklisted domain or IP, SMTP codes with copy-paste records, Gmail `4.7.28`, suspended mailboxes, measurement problem only |
| `references/deliverability-primer.md` | Shared: authentication, provider rules with dates, bounce and complaint formulas, validation buckets, thresholds |
| `references/list-quality-standard.md` | Shared: required columns, freshness, suppression lists, acceptance thresholds |
| `references/scrapercity-catalog.md` | Shared: `validate_emails` and `find_emails` prices and inputs |
| `references/scrapercity-platform.md` | Shared: plans and integrations |
| `templates/output-template.md` | The blank health report |
| `templates/incident-plan-template.md` | The blank incident recovery plan |
| `examples/worked-example.md` | A filled weekly report for 7 active and 2 reserve domains, with a bounce spike and a complaint warning |
| `examples/incident-example.md` | A filled recovery plan for 8 inboxes on 4 domains after opens fell to 7% and hard bounces hit 4.5% |
| `scripts/check-output.py` | Run on the finished plan or report before delivery; it detects which one it is |

## Related Skills

- `domain-infrastructure` fixes DNS and adds or replaces domains.
- `inbox-setup` pauses, rests, retires and re-ramps mailboxes on this skill's findings.
- `sending-platforms` wires suppression lists, auto-pause settings and webhooks.
- `email-list-cleaner` and `cold-email-list` produce the validated files this skill gates.
- `cold-email-copywriting` rewrites copy when R2 points at content.
- `reply-handling` processes opt-outs and spam replies the same day.
- `cold-email-strategy` adjusts volume and segments when a segment draws complaints.
