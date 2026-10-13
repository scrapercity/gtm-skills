# Deliverability Health Report: Ledgerline

Period 2026-11-30 to 2026-12-06. Prepared 2026-12-07 by Dana Cho (RevOps) for the Ledgerline sales team (fictional company used as an example).

## Summary

Ledgerline's 7 active sending domains sent 2,435 cold emails this week from 21 Google Workspace mailboxes through Instantly; 2 reserve domains stayed in warmup. Five domains are green and two are yellow; none is red. Two incidents opened. Campaign B (Mountain and Pacific prospects) auto-paused on Tuesday when two mailboxes on useledgerline.com crossed 3% hard bounces; the cause was a 1,000-row batch validated 45 days before it was sent. The 640 unsent rows were re-validated, 41 invalid rows removed, and Campaign B resumed Thursday with the two mailboxes back at 10 a day. Separately, getledgerline.com showed a Postmaster spam rate of 0.15% and 0.13% on Monday and Tuesday; its volume is cut 50% until it holds under 0.1% for 7 days. Validation this week cost $11.81 for 1,640 addresses, plus $1.25 for 25 replacement emails. Decision for the user: approve keeping getledgerline.com at half volume through 2026-12-10 and dropping touch 4 for the "fintech" segment that drew the replies marked as spam.

## Scope

| Item | Value |
|-|-|
| Main domain (never sends cold email) | ledgerline.com |
| Sending domains | 7 active (getledgerline.com, tryledgerline.com, ledgerlinehq.com, meetledgerline.com, withledgerline.com, useledgerline.com, ledgerline-team.com), 2 reserve (goledgerline.com, ledgerlineapp.com) |
| Mailboxes | 21 active, 6 reserve, Google Workspace Business Starter |
| Sequencer | Instantly Hypergrowth, Campaign A (ET and CT), Campaign B (MT and PT), Campaign C (catch-all, all zones) |
| Cold sends in period | 2,435 |
| Dedicated IPs | None (Workspace shared IPs), so SNDS and IP blocklists do not apply |

## Authentication and Compliance

| Domain | SPF | DKIM | DMARC | Alignment | Unsubscribe header | Postmaster compliance |
|-|-|-|-|-|-|-|
| getledgerline.com | pass | pass (2048-bit, d=getledgerline.com) | pass, p=none, rua set | DKIM and SPF aligned | On, List-Unsubscribe-Post present | Compliant; spam rate 0.15% peak |
| tryledgerline.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| ledgerlinehq.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | Compliant |
| meetledgerline.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| withledgerline.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| useledgerline.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| ledgerline-team.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | On | No data found |
| goledgerline.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | Not sending cold | No data found |
| ledgerlineapp.com | pass | pass | pass, p=none, rua set | DKIM and SPF aligned | Not sending cold | No data found |

Header test 2026-12-04 from all 27 mailboxes to a personal Gmail seed: 27 of 27 show `spf=pass`, `dkim=pass` with `header.d` set to the sending domain, `dmarc=pass`. DMARC aggregate reports: 100% pass for all 9 domains; no unknown sources. Every touch carries the plain opt-out line and the Denver postal address. DMARC moves to `p=quarantine` on 2026-12-14 after 30 days of aligned reports, per the `domain-infrastructure` plan.

## List Validation

| Bucket | New batch, week 49 | Re-validated, Campaign B unsent rows | Total | Action |
|-|-|-|-|-|
| valid | 861 | 571 | 1,432 | Send file, ordered high, medium, low `email_quality` |
| valid_catch_all | 92 | 22 | 114 | Campaign C (catch-all), capped at 60 a day, 10% of 600 |
| unknown | 14 | 6 | 20 | Hold; re-validate on 2026-12-10 |
| invalid | 31 | 41 | 72 | Instantly blocklist; `find_emails` run on all 72 |
| disposable | 2 | 0 | 2 | Instantly blocklist |
| Total | 1,000 | 640 | 1,640 | |

Cost: `validate_emails` 1,640 x $0.0072 = $11.81. `find_emails` on 72 invalid rows with first name, last name and domain: 25 found x $0.05 = $1.25 (47 not found, free). The 25 replacements arrived validated and went into the send file. Total ScraperCity spend this week: $13.06. `check_wallet` before the runs showed $391.20.

Re-validation result for the Campaign B batch: 41 of 640 invalid (6.4%) after 45 days, against 1.9% invalid when the same rows were first validated on 2026-10-21. The source stays in use (under the 15% stop line); the freshness rule caused the spike.

## Placement Tests

Run 2026-12-04, 11:00 CT, one mailbox per domain, live touch 1 copy, 8 seeds.

| Domain | Gmail | Workspace | Outlook.com | Microsoft 365 | Yahoo | Result |
|-|-|-|-|-|-|-|
| getledgerline.com | 1 of 2 inbox, 1 spam | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Spam at 1 provider: watch, retest 2026-12-07 |
| tryledgerline.com | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| ledgerlinehq.com | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| meetledgerline.com | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| withledgerline.com | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| useledgerline.com | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |
| ledgerline-team.com | 2 of 2 inbox | 2 of 2 inbox | 1 of 1 inbox | 2 of 2 inbox | 1 of 1 inbox | Inbox everywhere |

## Domain Health

| Domain | Mailboxes | Sends (period) | Hard bounce % | Spam rate (Postmaster) | Human replies | Status | Action |
|-|-|-|-|-|-|-|-|
| getledgerline.com | 3 | 315 | 0.6% (2) | 0.15% peak (Mon 0.15%, Tue 0.13%) | 3 | Yellow | Volume cut 50% from 2026-12-03 (R3); retest seeds 2026-12-07 |
| tryledgerline.com | 3 | 450 | 0.4% (2) | No data | 6 | Green | None |
| ledgerlinehq.com | 3 | 450 | 0.9% (4) | 0.00% | 5 | Green | None |
| meetledgerline.com | 3 | 450 | 0.7% (3) | No data | 4 | Green | None |
| withledgerline.com | 3 | 300 | 1.0% (3) | No data | 3 | Green | Resumed with Campaign B on 2026-12-03 |
| useledgerline.com | 3 | 220 | 2.7% (6) | No data | 2 | Yellow | marcus.bell@ and elenar@ restarted at 10 a day (R1) |
| ledgerline-team.com | 3 | 250 | 1.2% (3) | No data | 2 | Green | Resumed with Campaign B on 2026-12-03 |
| goledgerline.com | 3 | 0 | 0.0% | No data | 0 | Green | Reserve, warmup only |
| ledgerlineapp.com | 3 | 0 | 0.0% | No data | 0 | Green | Reserve, warmup only |

Sends add up to 2,435: 315 + 450 + 450 + 450 + 300 + 220 + 250. Reply rate by recipient provider (from `sc_mx_provider`): Google 1.1% (17 of 1,520), Microsoft 0.8% (6 of 790), other 1.6% (2 of 125); 25 human replies in total. No provider or gateway segment sat at zero replies.

## Blocklist Checks

| Domain or IP | Spamhaus | Other lists | Checked |
|-|-|-|-|
| getledgerline.com | Not listed (DBL) | Not applicable, shared Workspace IPs | 2026-12-04 |
| tryledgerline.com | Not listed (DBL) | Not applicable | 2026-12-04 |
| ledgerlinehq.com | Not listed (DBL) | Not applicable | 2026-12-04 |
| meetledgerline.com | Not listed (DBL) | Not applicable | 2026-12-04 |
| withledgerline.com | Not listed (DBL) | Not applicable | 2026-12-04 |
| useledgerline.com | Not listed (DBL) | Not applicable | 2026-12-01 and 2026-12-04 |
| ledgerline-team.com | Not listed (DBL) | Not applicable | 2026-12-04 |
| goledgerline.com | Not listed (DBL) | Not applicable | 2026-12-04 |
| ledgerlineapp.com | Not listed (DBL) | Not applicable | 2026-12-04 |

## Incidents and Actions

| Opened | Runbook | Scope | Trigger | Action | Owner | Resume condition | Status |
|-|-|-|-|-|-|-|-|
| 2026-12-01 10:40 CT | R1 Bounce spike | Campaign B; marcus.bell@useledgerline.com and elenar@useledgerline.com | 3.4% and 3.1% hard bounces over each mailbox's last 200 sends; Instantly campaign paused 10:45 | Bounce log: `550 5.1.1` across 9 company domains; batch validated 2026-10-21, sent 45 days later. Re-validated 640 unsent rows ($4.61), removed 41 invalid, blocklisted 13 bounced addresses | Dana Cho | Send file 100% `valid`; the two mailboxes restart at 10 a day | Closed 2026-12-03 |
| 2026-12-02 09:00 CT | R3 Complaint spike | getledgerline.com, Campaign A | Postmaster spam rate 0.15% (Mon) and 0.13% (Tue); 2 replies saying "stop spamming" from the fintech segment | Volume cut 50% from 2026-12-03; both repliers blocklisted at domain level; removed 38 personal Gmail addresses from the remaining Campaign A list; proposed dropping touch 4 for the fintech segment | Priya Natarajan | 7 consecutive days under 0.1% and a seed test with inbox at all 5 providers | Open |

## Stop Rules

| Rule | Threshold | Fired this period | Action taken |
|-|-|-|-|
| Spam rate, act | 0.1% for 2 days on a domain | Yes, getledgerline.com | Volume cut 50% |
| Spam rate, stop | 0.3% on any day | No | None |
| Campaign bounces | 2% over 200 sends | Yes, Campaign B | Campaign paused, unsent rows re-validated |
| Mailbox bounces | 3% over the mailbox's last 200 sends | Yes, 2 mailboxes on useledgerline.com | Paused, restarted at 10 a day |
| Catch-all campaign | 3% over 200 sends | No (Campaign C at 1.8% over 166 sends) | None |
| Source quality | Over 15% invalid from one source | No (6.4% after 45 days) | None |
| Authentication | Any failing check or a `5.7.x` rejection | No | None |
| Blocklist | Domain on the Spamhaus DBL | No | None |
| Opt-outs | Suppressed within 24 hours | No breach: 11 opt-outs, all blocklisted the same day | None |
| Unvalidated rows | Any row in a send file not `valid` within 30 days | Yes, Campaign B batch was 45 days old | Freshness check added to the pre-send gate for every batch |

## Next Review

Monday 2026-12-14, 10:00 CT. Repeat: header test on any mailbox touched by DNS changes (DMARC moves to `p=quarantine` that day), seed test on all 7 domains, Postmaster spam rate for getledgerline.com (resume full volume only after 7 days under 0.1%), Spamhaus check on all 9 domains, re-validation of the 20 `unknown` rows on 2026-12-10. Pending decision: drop touch 4 for the fintech segment.
