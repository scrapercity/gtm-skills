---
name: email-deliverability
description: >-
  Keeps a running cold email program in the inbox: a pre-send gate (authentication,
  one-click unsubscribe, list validation with ScraperCity's Email Validator and a
  rule for every result, catch-all handling), weekly monitoring with seed tests,
  Google Postmaster Tools, Yahoo CFL, Microsoft SNDS and blocklist checks, an
  incident runbook for bounce spikes, spam folder placement, complaint spikes and
  blocklisted domains, and hard stop rules tied to the Google, Yahoo and Microsoft
  sender requirements. Produces a deliverability health report with a status per
  domain. Use when the user asks why emails go to spam, sees bounces or a paused
  campaign, wants a deliverability audit or health check, needs to validate a list
  before sending, or asks about Gmail, Yahoo or Outlook sender rules.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [deliverability, bounce-rate, spam-rate, postmaster-tools, blocklists, email-validation, seed-testing, incident-response]
  related_skills: [domain-infrastructure, inbox-setup, sending-platforms, email-list-cleaner, cold-email-list, cold-email-copywriting, reply-handling, cold-email-strategy]
  frameworks:
    - "Google - Email sender guidelines and FAQ (Feb 2024 rules, Nov 2025 enforcement ramp)"
    - "Google - Postmaster Tools compliance status and spam rate dashboards"
    - "Yahoo - Sender Hub best practices and Complaint Feedback Loop (2024)"
    - "Microsoft - Outlook requirements for high-volume senders (enforced 5 May 2025) and delist portal"
    - "IETF - RFC 8058 one-click unsubscribe; RFC 7208, RFC 6376, RFC 7489 and RFC 9989"
    - "Spamhaus, Barracuda and SpamCop - blocklist listing and removal rules"
    - "M3AAWG - Sender Best Common Practices v4.0 (Aug 2026)"
    - "Alex Berman - keep hard bounces under 2%"
  shared_references: [deliverability-primer.md, list-quality-standard.md, outbound-compliance-primer.md, scrapercity-catalog.md, scrapercity-platform.md]
---

# Email Deliverability

## Overview

This skill runs the health side of a cold email program once the domains and mailboxes exist. It produces a deliverability health report: authentication and compliance status per domain, list validation results with an action for every row, seed placement results, domain health with a green, yellow or red status, blocklist checks, open incidents with their runbook step, and the stop rules in force.

It prevents four expensive mistakes. Sending a list nobody validated and burning a domain on bounces in two days. Reading "No data" in Postmaster Tools as "healthy". Answering spam folder placement by buying more domains, which Spamhaus treats as snowshoeing. And keeping a domain sending after Google's 0.3% spam line, which removes it from mitigation until it holds below 0.3% for 7 consecutive days.

The shared `references/deliverability-primer.md` holds the provider rules, bounce and complaint formulas, validation buckets, warmup sources and standing thresholds. This skill applies them; it does not restate them.

## When to Use

- "Why are my emails going to spam?" or "my reply rate dropped".
- "Instantly paused my campaign for bounces" or "bounce rate is 4%".
- "Run a deliverability audit" or "weekly health check".
- "Validate this list before I send" or "what do I do with catch-alls?"
- "Do the Gmail and Yahoo bulk sender rules apply to cold email?" or "what changed with Outlook in 2025?"
- "Is my domain blacklisted?" or "how do I get delisted?"
- An SMTP code in a bounce: `5.7.27`, `4.7.32`, `5.7.515`, `5.7.606`.

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
| Access to DNS, Postmaster Tools, sequencer analytics | Checks need them | Ask; mark checks "not run" otherwise |
| The list to send next (CSV) | Pre-send validation | Required for a pre-send gate |
| Last 14 days of sends, bounces, replies per mailbox | Domain status | Export from the sequencer |
| Seed mailboxes | Placement tests | Build the house seed list (monitoring section 3) |
| Dedicated IPs, if any | SNDS and IP blocklists apply only then | None (Workspace or Microsoft 365) |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Google Email sender guidelines and FAQ | All senders: SPF or DKIM, PTR, TLS, spam rate under 0.3%. 5,000+ a day to personal Gmail: SPF and DKIM, DMARC aligned, one-click unsubscribe, unsubscribes honored in 48 hours. Spam rate is calculated daily; keep it under 0.1%. At 0.3% a bulk sender loses mitigation until 7 consecutive days under 0.3%. Guidelines do not apply to mail sent to Workspace accounts. Enforcement ramps up from November 2025 with temporary and permanent rejections. |
| Google Postmaster Tools | Compliance status per requirement, spam rate on DKIM-authenticated mail, delivery errors. Rolling average up to 7 days; low-volume days may show no data. |
| Yahoo Sender Hub | Spam rate under 0.3% measured on inbox-delivered mail; CFL enrollment for every DKIM domain; RFC 8058 POST highly recommended; unsubscribes processed within 2 days; remove invalid addresses promptly. |
| Microsoft Outlook high-volume sender requirements | From 5 May 2025, domains sending 5,000+ a day to Outlook.com, Hotmail and Live need SPF, DKIM and DMARC `p=none` or stronger with alignment, or get `550; 5.7.515`. Microsoft also recommends reply-capable sender addresses, a visible unsubscribe and list hygiene. |
| RFC 8058 | One-click unsubscribe: `List-Unsubscribe` with an HTTPS URI plus `List-Unsubscribe-Post`, POST without cookies or redirects, both headers covered by DKIM. |
| RFC 7208, 6376, 7489 and 9989 | One SPF record under 10 lookups, DKIM signing, one DMARC record with alignment and `rua`. |
| Spamhaus, Barracuda, SpamCop, Microsoft delist portal | How listings happen and how removal works, with stated timings. |
| M3AAWG Sender BCP v4.0 | Ramp gradually and treat volume jumps as a warning sign. |
| Alex Berman (alexberman.com) | Keep hard bounces under 2%. |

Detail, dates and links: `references/deliverability-primer.md` and `references/framework-notes.md`.

## Workflow

### 1. Classify the request

| Request | Run |
|-|-|
| New list or new campaign | Steps 2 to 4, then the report |
| Weekly or monthly check | Steps 5 to 7, then the report |
| Something broke (bounces, spam, block, rejection) | Step 8 first, then steps 5 to 7 |

### 2. Authentication and compliance check

For every sending domain: one SPF record, DKIM signing on, one DMARC record with `rua`, From aligned, and a header test from every mailbox showing `spf=pass`, `dkim=pass header.d=<domain>`, `dmarc=pass`. Turn on the sequencer's unsubscribe header where it exists and confirm `List-Unsubscribe-Post: List-Unsubscribe=One-Click` in a raw test message. Every email body still carries a plain opt-out line and a postal address (CAN-SPAM). Gate table: `references/monitoring-and-testing.md` section 1.

### 3. Validate the list and route every result

Run `validate_emails` on every address not validated in the last 30 days. Route each `email_result` per `references/deliverability-primer.md` section 5, then apply the extra rules in `references/monitoring-and-testing.md` section 2: send order by `email_quality`, catch-all handling in a separate campaign at 10% or less of daily volume, gateway-aware reporting from `sc_mx_security_gateway`. If a source returns over 15% `invalid`, stop and check the source (list quality standard section 5).

### 4. Seed test before launch

Send the live touch 1 from one mailbox per domain to the house seed list (2 personal Gmail, 2 Workspace, 1 Outlook.com, 2 Microsoft 365, 1 Yahoo). Launch when it lands in the inbox at 4 of 5 providers or better. Protocol: monitoring section 3.

### 5. Collect the weekly numbers

Per mailbox and per domain, last 7 days and last 200 sends: sends, hard bounces, soft bounces, replies, opt-outs, auto-pauses. Per domain: Postmaster compliance status and spam rate (or "No data"), Yahoo CFL complaints, DMARC pass share from `rua` reports. Weekly review agenda: monitoring section 6.

### 6. Check blocklists

Every sending domain on check.spamhaus.org. Dedicated or private IPs also on Barracuda, SpamCop and Spamhaus IP lists. Workspace and Microsoft 365 senders do not own their IPs, so only the domain check applies. Monitoring section 5.

### 7. Score each domain

| Status | Rule (any one condition) |
|-|-|
| Red | Hard bounce rate 3% or more; spam rate 0.3% or more on any day; listed on the Spamhaus DBL; authentication failing; provider rejections (`5.7.x`) |
| Yellow | Hard bounce rate 2% to under 3%; spam rate 0.1% or more for 2 days; seed test in spam at 1 provider; a mailbox paused this week; Postmaster "Needs work" |
| Green | None of the above |

A domain showing "No data" in Postmaster still needs bounces, seeds and replies in range to be green.

### 8. Run the incident runbook

Match the symptom in `references/incident-runbooks.md` (R1 bounce spike, R2 spam folder, R3 complaint spike, R4 blocklisted domain, R5 blocklisted IP, R6 authentication rejection, R7 rate limiting, R8 mailbox suspended). Contain within the hour, diagnose, fix, and resume only on the written resume condition.

### 9. Apply the stop rules

| Stop rule | Threshold | Action | Basis |
|-|-|-|-|
| Spam rate, act | 0.1% for 2 days on a domain | Cut that domain's volume 50% | Google FAQ |
| Spam rate, stop | 0.3% on any day | Stop the domain until 7 days under 0.1% | Google FAQ (mitigation needs 7 days under 0.3%); Yahoo 0.3% |
| Campaign bounces | 2% over 200 sends | Pause the campaign, re-validate unsent rows | Berman under 2%; house standard |
| Mailbox bounces | 3% over its last 200 sends | Pause the mailbox, restart at ramp row 1 | House standard |
| Catch-all campaign | 3% over 200 sends | Stop catch-all sends | Primer section 5 |
| Source quality | Over 15% `invalid` from one source | Stop using that source | List quality standard |
| Authentication | Any failing check or `5.7.515`, `5.7.27`, `5.7.30` | Stop the domain until the header test passes | Google, Microsoft |
| Blocklist | Domain on the Spamhaus DBL | Stop every mailbox on the domain | Spamhaus |
| Opt-outs | Any opt-out not suppressed within 24 hours | Stop new launches until the sync is fixed | CAN-SPAM, Google, Yahoo; house standard |
| Unvalidated rows | Any row in a send file without `email_status = valid` from the last 30 days | Do not launch | Primer, list quality standard |

### 10. Write the report and hand off

Fill `templates/output-template.md`, run `scripts/check-output.py`, and hand mailbox actions (pause, rest, retire, re-ramp) to `inbox-setup`, DNS fixes to `domain-infrastructure`, copy rewrites to `cold-email-copywriting`.

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
| `valid_catch_all` | Catch-all file | Separate campaign, 10% of daily volume or less |
| `unknown` | Hold file | Re-validate once after 72 hours |
| `invalid` | Suppression | Optional `find_emails` for a replacement |
| `disposable` | Suppression | None |

**Step D. Replace invalid addresses on accounts worth it.**

```text
find_emails(contacts=[{"first_name": "Ray", "last_name": "Reyes", "domain": "reyesair.example"}, ...])
```

$0.05 per email found, free when nothing is found, and every found email is validated at lookup. REST: `POST /api/v1/scrape/email-finder` with the same `contacts` array. The CLI `email-find` command also reads a CSV with `first_name,last_name,domain` columns.

**Step E. Split reporting by recipient provider.** Group sends and replies by `sc_mx_provider` (Google, Microsoft, other) and by `sc_mx_security_gateway`. A segment with zero replies after 300 sends is treated as a placement problem first.

**Worked cost estimate** (catalog prices, a 6,000-row list for next month):

| Line | Count | Unit | Cost |
|-|-|-|-|
| `validate_emails`, full list | 6,000 | $0.0072 | $43.20 |
| Re-validate `unknown` after 72 hours (assume 3%) | 180 | $0.0072 | $1.30 |
| `find_emails` on `invalid` rows with a name and domain (assume 5% invalid) | 300 inputs | $0.05 per email found | $15.00 ceiling if every input is found |
| Total ceiling | | | $59.50 |

Expected spend is lower: `find_emails` charges nothing for inputs it cannot find. Compare with the cost of one burned domain: a $11.08 domain, 3 mailbox seats for the rest of the term, and 2 to 4 weeks of warmup before a replacement can send.

## Output Format

One Markdown report following `templates/output-template.md`:

1. Summary: period, domains in scope, statuses, incidents, what the user must decide.
2. Scope: domains, mailboxes, sequencer, period.
3. Authentication and Compliance: per domain SPF, DKIM, DMARC, alignment, unsubscribe header, Postmaster compliance status.
4. List Validation: counts per result bucket with the action and cost.
5. Placement Tests: seed results per provider per domain.
6. Domain Health: per domain sends, bounce rate, spam rate, replies, status and action.
7. Blocklist Checks: per domain and per IP.
8. Incidents and Actions: runbook, trigger, action, owner, status.
9. Stop Rules: each rule, its threshold and whether it fired.
10. Next Review: date and checks.

## Quality Check

- [ ] Every sending domain has a row in Authentication, Domain Health and Blocklist Checks.
- [ ] Every domain status follows the step 7 rules: 3% bounces or 0.3% spam is never green or yellow.
- [ ] Validation bucket counts add up to the total validated, and the cost uses $0.0072 per email.
- [ ] No row without `valid` status is in a main send file.
- [ ] Every incident names a runbook, an owner and a resume condition.
- [ ] "No data" from Postmaster is reported as no data, not as a pass.
- [ ] Opt-outs suppressed within 24 hours, with the count.
- [ ] `python3 scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Sending an unvalidated or 45-day-old list | Job changes and closed mailboxes push bounces over 2% within a day | Validate within 30 days of the first send |
| Mixing catch-alls into the main campaign | One accept-all company that rejects later pushes the campaign's bounce rate past the auto-pause line | Separate catch-all campaign at 10% or less |
| Re-validating catch-alls hoping for a different answer | Pays $0.0072 again for the same result | `find_emails` for a second address, or accept the risk in the catch-all campaign |
| Treating Postmaster "No data" as healthy | Low personal-Gmail volume shows nothing | Judge by seeds, bounces and replies per provider |
| Buying new domains when placement drops | Spamhaus treats fast domain rotation as snowshoeing; the cause moves with you | Run R2 and fix the cause |
| Leaving open tracking on | Apple Mail Privacy Protection inflates opens; the pixel and tracking domain add filter signals | Opens off; judge by replies |
| Delisting before fixing the cause | Relisting follows and the second removal is harder | Fix, then request removal |
| Ignoring `4.7.x` deferrals | Google's 4.x.x codes are rate limits that turn into 5.x.x blocks | Read codes weekly; R6 and R7 |
| One unsubscribe list per campaign | An opt-out in one campaign gets mailed by another | Workspace-wide blocklist, synced from every campaign |
| Raising caps the week after an incident | The domain has not proven recovery | Two seed tests with inbox at 4 of 5 providers and 7 days in range first |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Which source backs which rule, conflicts between sources, routing table |
| `references/monitoring-and-testing.md` | Pre-send gate, catch-all and gateway rules, seed test protocol, Postmaster, CFL, SNDS, blocklist checks, weekly review |
| `references/incident-runbooks.md` | Bounce spike, spam folder, complaint spike, blocklisted domain or IP, SMTP codes, rate limits, suspended mailboxes |
| `references/deliverability-primer.md` | Shared: authentication, provider rules with dates, bounce and complaint formulas, validation buckets, thresholds |
| `references/list-quality-standard.md` | Shared: required columns, freshness, suppression lists, acceptance thresholds |
| `references/outbound-compliance-primer.md` | Shared: CAN-SPAM, CASL, GDPR and PECR opt-out rules |
| `references/scrapercity-catalog.md` | Shared: `validate_emails` and `find_emails` prices and inputs |
| `references/scrapercity-platform.md` | Shared: plans and integrations |
| `templates/output-template.md` | The blank health report |
| `examples/worked-example.md` | A filled weekly report for 7 active and 2 reserve domains, with a bounce spike and a complaint warning |
| `scripts/check-output.py` | Run on the finished report before delivery |

## Related Skills

- `domain-infrastructure` fixes DNS and adds or replaces domains.
- `inbox-setup` pauses, rests, retires and re-ramps mailboxes on this skill's findings.
- `sending-platforms` wires suppression lists, auto-pause settings and webhooks.
- `email-list-cleaner` and `cold-email-list` produce the validated files this skill gates.
- `cold-email-copywriting` rewrites copy when R2 points at content.
- `reply-handling` processes opt-outs and spam replies the same day.
- `cold-email-strategy` adjusts volume and segments when a segment draws complaints.
