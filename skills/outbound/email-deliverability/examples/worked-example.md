# Deliverability Health Report: Ledgerline

Period 2026-11-30 to 2026-12-06. Illustrative example (fictional company; domains use `.example`). Prepared 2026-12-07 by Dana Cho (RevOps) for the Ledgerline sales team.

## Summary

Ledgerline's 7 active sending domains sent 2,435 cold emails this week from 21 Google Workspace mailboxes through Instantly; 2 reserve domains stayed in warmup. Five domains are green, one is yellow and one is red. Two incidents opened. Campaign B (Mountain and Pacific prospects) was paused on Tuesday when two mailboxes on useledgerline.example crossed 2% hard bounces; the cause was a 1,000-row batch validated 45 days before it was sent. The 640 unsent rows were re-validated, 41 invalid rows removed, and Campaign B resumed Thursday with the two mailboxes back at 10 a day. Separately, getledgerline.example showed a Postmaster spam rate of 0.15% and 0.13% on Monday and Tuesday, over Google's 0.1% target; its mailboxes are lowered from 30 to 15 a day until it holds under 0.1% for 7 consecutive days. Validation this week cost $2.77 for 1,640 addresses, plus $1.25 for 25 replacement emails. Decision for the user: approve keeping getledgerline.example at 15 a day per mailbox through 2026-12-10 and dropping touch 4 for the "fintech" segment that drew the replies marked as spam.

## Scope

| Item | Value |
|-|-|
| Main domain (never sends cold email) | ledgerline.example |
| Sending domains | 7 active (getledgerline.example, tryledgerline.example, ledgerlinehq.example, meetledgerline.example, withledgerline.example, useledgerline.example, ledgerline-team.example), 2 reserve (goledgerline.example, ledgerlineapp.example) |
| Mailboxes | 21 active, 6 reserve, Google Workspace Business Starter |
| Sequencer | Instantly Hypergrowth, Campaign A (ET and CT), Campaign B (MT and PT), Campaign C (catch-all, all zones) |
| Cold sends in period | 2,435 |
| Dedicated IPs | None (Google Workspace shared IPs) |
| Pause authority (one owner, plus backup) | Dana Cho (RevOps) can pause any domain, mailbox or campaign without sign-off; Priya Natarajan when Dana is out |
| Backup capacity (warmed reserves, sends a day) | goledgerline.example and ledgerlineapp.example, 6 mailboxes in warmup since 2026-10-15, 180 cold sends a day at 30 each. No new domains will be bought while an incident is open |

Not checked: SNDS and IP blocklists, because Ledgerline owns no sending IPs; Yahoo CFL reports were checked and empty.

## Authentication and Unsubscribe

| Domain | SPF | DKIM | DMARC | Alignment | Unsubscribe header | Postmaster compliance |
|-|-|-|-|-|-|-|
| getledgerline.example | pass | pass (2048-bit, d=getledgerline.example) | pass, p=none, rua set | DKIM and SPF aligned | On, List-Unsubscribe-Post present | Compliant; spam rate 0.15% peak |
| tryledgerline.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| ledgerlinehq.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | Compliant |
| meetledgerline.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| withledgerline.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| useledgerline.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| ledgerline-team.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| goledgerline.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | Not sending cold | No data found |
| ledgerlineapp.example | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | Not sending cold | No data found |

Header test 2026-12-04 from all 27 mailboxes to a personal Gmail seed: 27 of 27 show `spf=pass`, `dkim=pass` with `header.d` set to the sending domain, `dmarc=pass`. DMARC aggregate reports: 100% pass for all 9 domains; no unknown sources. Every touch carries the plain opt-out line. DMARC moves to `p=quarantine` on 2026-12-14, the date in the infrastructure plan, after well over the one week of aligned daily reports Google's rollout guide asks for.

Records to publish: none; every check passed.

## List Validation

| Bucket | New batch, week 49 | Re-validated, Campaign B unsent rows | Total | Action |
|-|-|-|-|-|
| valid | 861 | 571 | 1,432 | Send file, ordered high, medium, low quality rating |
| valid_catch_all | 92 | 22 | 114 | Campaign C (catch-all), capped at 60 a day, Ledgerline's own setting |
| unknown | 14 | 6 | 20 | Hold; re-validate on 2026-12-10 |
| invalid | 31 | 41 | 72 | Instantly blocklist; Email Finder run on all 72 |
| disposable | 2 | 0 | 2 | Instantly blocklist |
| Total | 1,000 | 640 | 1,640 | |

Cost: Email Validator 1,640 x $0.00169 = $2.77. Email Finder on 72 invalid rows with first name, last name and domain: 25 found x $0.05 = $1.25 (47 not found, free). The 25 replacements arrived validated and went into the send file. Total ScraperCity spend this week: $4.02. Wallet balance before the runs: $391.20.

Re-validation result for the Campaign B batch: 41 of 640 invalid (6.4%) after 45 days, against 1.9% invalid when the same rows were first validated on 2026-10-21. The source stays in use: its rows were 1.9% invalid when first validated, so age caused the spike. Ledgerline's re-check window is 30 days, its own setting.

## Placement Tests

Run 2026-12-04, 11:00 CT, one mailbox per domain, live touch 1 copy, 8 seeds.

| Domain | Gmail | Workspace | Outlook.com | Microsoft 365 | Yahoo | Result |
|-|-|-|-|-|-|-|
| getledgerline.example | 1 of 2 inbox, 1 spam | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Spam at 1 provider: retest from a second mailbox 2026-12-07 |
| tryledgerline.example | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| ledgerlinehq.example | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| meetledgerline.example | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| withledgerline.example | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| useledgerline.example | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| ledgerline-team.example | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |

## Domain Health

| Domain | Mailboxes | Sends (period) | Hard bounce % | Spam rate (Postmaster) | Human replies | Status | Action |
|-|-|-|-|-|-|-|-|
| getledgerline.example | 3 | 315 | 0.6% (2) | 0.15% peak (Mon 0.15%, Tue 0.13%) | 3 | Yellow | Lowered to 15 a day per mailbox from 2026-12-03 for the complaint warning; retest seeds 2026-12-07 |
| tryledgerline.example | 3 | 450 | 0.4% (2) | No data | 6 | Green | None |
| ledgerlinehq.example | 3 | 450 | 0.9% (4) | 0.00% | 5 | Green | None |
| meetledgerline.example | 3 | 450 | 0.7% (3) | No data | 4 | Green | None |
| withledgerline.example | 3 | 300 | 1.0% (3) | No data | 3 | Green | Resumed with Campaign B on 2026-12-03 |
| useledgerline.example | 3 | 220 | 2.7% (6) | No data | 2 | Red | marcus@ and elena.ruiz@ restarted at 10 a day after the bounce spike; seed test inbox at all 5 providers on 2026-12-04 |
| ledgerline-team.example | 3 | 250 | 1.2% (3) | No data | 2 | Green | Resumed with Campaign B on 2026-12-03 |
| goledgerline.example | 3 | 0 | 0.0% | No data | 0 | Green | Reserve, warmup only |
| ledgerlineapp.example | 3 | 0 | 0.0% | No data | 0 | Green | Reserve, warmup only |

Sends add up to 2,435: 315 + 450 + 450 + 450 + 300 + 220 + 250. Reply rate by recipient provider (from the validator's mail provider column): Google 1.1% (17 of 1,520), Microsoft 0.8% (6 of 790), other 1.6% (2 of 125); 25 human replies in total. No provider or gateway segment sat at zero replies.

## Blocklist Checks

| Domain | Role | Spamhaus DBL | SURBL | URIBL | Checked |
|-|-|-|-|-|-|
| getledgerline.example | Sending; hosts the inst tracking CNAME | Not listed | Not listed | Not listed | 2026-12-04 |
| tryledgerline.example | Sending; hosts the inst tracking CNAME | Not listed | Not listed | Not listed | 2026-12-04 |
| ledgerlinehq.example | Sending; hosts the inst tracking CNAME | Not listed | Not listed | Not listed | 2026-12-04 |
| meetledgerline.example | Sending; hosts the inst tracking CNAME | Not listed | Not listed | Not listed | 2026-12-04 |
| withledgerline.example | Sending; hosts the inst tracking CNAME | Not listed | Not listed | Not listed | 2026-12-04 |
| useledgerline.example | Sending; hosts the inst tracking CNAME | Not listed | Not listed | Not listed | 2026-12-01 and 2026-12-04 |
| ledgerline-team.example | Sending; hosts the inst tracking CNAME | Not listed | Not listed | Not listed | 2026-12-04 |
| goledgerline.example | Sending, reserve | Not listed | Not listed | Not listed | 2026-12-04 |
| ledgerlineapp.example | Sending, reserve | Not listed | Not listed | Not listed | 2026-12-04 |
| ledgerline.example | Linked: main site URL in every signature | Not listed | Not listed | Not listed | 2026-12-04 |

Touch 1 to 3 carry no booking link and no other URL, so these 10 domains are every domain a filter sees in the messages. Open and click tracking are off, so no tracked links went out this week.

## Incidents and Actions

| Opened | Type | Scope | Trigger | Action | Owner | Resume condition | Status |
|-|-|-|-|-|-|-|-|
| 2026-12-01 10:40 CT | Bounce spike | Campaign B; marcus@useledgerline.example and elena.ruiz@useledgerline.example | 3.4% and 3.1% hard bounces over each mailbox's last 200 sends; Instantly campaign paused 10:45 | Bounce log: `550 5.1.1` across 9 company domains; batch validated 2026-10-21, sent 45 days later. Re-validated 640 unsent rows ($1.08), removed 41 invalid, blocklisted 13 bounced addresses | Dana Cho | Send file 100% `valid`; the two mailboxes restart at 10 a day | Closed 2026-12-03 |
| 2026-12-02 09:00 CT | Complaint spike | getledgerline.example, Campaign A | Postmaster spam rate 0.15% (Mon) and 0.13% (Tue); 2 replies saying "stop spamming" from the fintech segment | Lowered to 15 a day per mailbox from 2026-12-03; both repliers blocklisted at domain level; removed 38 personal Gmail addresses from the remaining Campaign A list; proposed dropping touch 4 for the fintech segment | Priya Natarajan | 7 consecutive days under 0.1% and a seed test with inbox at all 5 providers | Open |

## Stop Rules

| Rule | Threshold | Source | Fired this period | Action taken |
|-|-|-|-|-|
| Spam rate, act | 0.1% or more on any day on a domain | Google sender guidelines | Yes, getledgerline.example | Lowered to 15 a day per mailbox |
| Spam rate, stop | 0.3% on any day | Google, Yahoo | No | None |
| Bounces, campaign or mailbox | 2% over the last 200 sends | Alex Berman; Instantly's 200-send window | Yes, Campaign B and 2 mailboxes on useledgerline.example | Campaign paused, unsent rows re-validated, mailboxes restarted at 10 a day |
| Catch-all campaign | 2% over 200 sends | Alex Berman; Instantly | No (Campaign C at 1.8% over 166 sends) | None |
| Authentication | Any failing check or a `5.7.x` rejection | Google, Microsoft | No | None |
| Blocklist | Domain on the Spamhaus DBL | Spamhaus | No | None |
| Opt-outs | Suppressed the same day in every tool | Google 48 hours and Yahoo 2 days are the outer limits | No breach: 11 opt-outs, all blocklisted the same day | None |
| Unvalidated rows | Any row in a send file not `valid` inside Ledgerline's 30-day re-check window | Alex Berman: verify before sending | Yes, Campaign B batch was 45 days old | Freshness check added to the pre-send gate for every batch |

Opt-out rate this week: Campaign A 0.54% (7 of 1,290), B 0.41% (4 of 979), C 0 of 166. All 7 Campaign A opt-out replies were read: 5 came from the fintech segment, which supports dropping its touch 4.

## Six-Month Audit

First audit, run on 2026-12-04 to set the baseline (domains live since 2026-10-15). Next full audit due 2027-06-04.

| Check | Run on | Result | Action | Next due |
|-|-|-|-|-|
| DNS records vs plan | 2026-12-04 | All 9 domains match the infrastructure plan: one SPF, one DMARC with `rua`, MX `smtp.google.com`, `google._domainkey` present, tracking CNAME `inst` DNS-only, Porkbun nameservers unchanged | None; renewal dates 2027-10-13 confirmed, auto-renew on | 2027-06-04 |
| DKIM key rotation | 2026-12-04 | Keys generated 2026-10-15, 50 days old, 2048-bit, selector `google` in live `DKIM-Signature` headers | Not due; rotation booked for 2027-04-12 with selector prefix `g2027`, inside the M3AAWG six-month line | 2027-04-12 |
| DMARC rua review, unknown senders | 2026-12-04 | 49 days of Valimail Monitor data for 9 domains: two sources only, Google Workspace and the Instantly warmup pool; no unknown IPs; 100% aligned | None; `p=quarantine` move on 2026-12-14 stays on plan | 2027-06-04 |
| Placement test, Google, Microsoft, Yahoo | 2026-12-04 | Seed test above: 6 domains inbox at all 5 providers; getledgerline.example in spam at 1 of 2 personal Gmail seeds | getledgerline.example retest 2026-12-07 with the complaint fix | 2027-06-04 |
| Caps vs volume | 2026-12-04 | 21 mailboxes at a 30 a day limit; Campaign A 360, B 270, C 60 a day (690 against 630 capacity) | Campaign B limit cut to 210 so the three campaigns total 630; no mailbox above 30 since launch | 2027-06-04 |

## Next Review

Monday 2026-12-14, 10:00 CT. Repeat: header test on any mailbox touched by DNS changes (DMARC moves to `p=quarantine` that day), seed test on all 7 domains, Postmaster spam rate for getledgerline.example (resume full volume only after 7 days under 0.1%), Spamhaus check on all 9 domains, re-validation of the 20 `unknown` rows on 2026-12-10. Pending decision: drop touch 4 for the fintech segment.
