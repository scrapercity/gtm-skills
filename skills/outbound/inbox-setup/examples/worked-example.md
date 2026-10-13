# Mailbox Roster and Ramp: Ledgerline

Prepared 2026-10-15 for the Ledgerline sales team (fictional company; ledgerline.com is the main domain). Mailboxes from the `domain-infrastructure` plan dated 2026-10-12.

## Summary

Ledgerline has 27 Google Workspace mailboxes on 9 secondary domains: 21 active on 7 domains and 6 reserve on 2 domains. Three people own them, one mailbox per person per domain, so each person owns 9. All 27 connect to Instantly Hypergrowth by OAuth and start pool warmup on Thursday 2026-10-15. Cold sends start Thursday 2026-10-29 at 10 a mailbox, step to 20 on 2026-11-05 and 30 on 2026-11-12. At 30 a mailbox the 21 active mailboxes can send 630 a day; the campaigns are capped at 600 (200 new prospects a day on a 3-step sequence). Reserves stay in warmup with a cold cap of 0. The list feed for the three ramp weeks is 3,000 prospects validated for $21.60.

| Item | Value |
|-|-|
| Main domain (never sends cold email) | ledgerline.com |
| Sequencer | Instantly Hypergrowth ($97 a month) |
| Active mailboxes | 21 on 7 domains |
| Reserve mailboxes | 6 on 2 domains |
| Warmup start | 2026-10-15 |
| First cold send | 2026-10-29 |
| Full volume date | 2026-11-12 |
| Steady-state cold sends a day | 600 (630 capacity) |

## Sender Identities

| Person | Title | Consent recorded | Photo uploaded | Mailboxes owned | Reply backup |
|-|-|-|-|-|-|
| Priya Natarajan | Head of Sales | Signed sender consent form, 2026-10-13 | Yes, LinkedIn headshot, 2026-10-14 | 9 (one per domain) | Elena Ruiz |
| Marcus Bell | Account Executive | Signed sender consent form, 2026-10-13 | Yes, 2026-10-14 | 9 (one per domain) | Priya Natarajan |
| Elena Ruiz | Account Executive | Signed sender consent form, 2026-10-13 | Yes, 2026-10-14 | 9 (one per domain) | Marcus Bell |

Address formats rotate by domain so no person repeats a pattern on neighboring domains: `first@`, `first.last@`, `firstl@`. Display names are the plain full name. Recovery email on every account is `it-ops@ledgerline.com`; 2-Step Verification is enforced on the "Cold Email" organizational unit; passwords live in the team password manager.

## Mailbox Roster

| Mailbox | Domain | Owner | Display name | Role | Rotation group | Warmup start | First cold send | Cold cap at full volume | Window (recipient TZ) | Reply routing |
|-|-|-|-|-|-|-|-|-|-|-|
| priya@getledgerline.com | getledgerline.com | Priya Natarajan | Priya Natarajan | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| marcus.bell@getledgerline.com | getledgerline.com | Marcus Bell | Marcus Bell | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elenar@getledgerline.com | getledgerline.com | Elena Ruiz | Elena Ruiz | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| priya.natarajan@tryledgerline.com | tryledgerline.com | Priya Natarajan | Priya Natarajan | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| marcusb@tryledgerline.com | tryledgerline.com | Marcus Bell | Marcus Bell | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elena@tryledgerline.com | tryledgerline.com | Elena Ruiz | Elena Ruiz | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| priyan@ledgerlinehq.com | ledgerlinehq.com | Priya Natarajan | Priya Natarajan | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| marcus@ledgerlinehq.com | ledgerlinehq.com | Marcus Bell | Marcus Bell | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elena.ruiz@ledgerlinehq.com | ledgerlinehq.com | Elena Ruiz | Elena Ruiz | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| priya@meetledgerline.com | meetledgerline.com | Priya Natarajan | Priya Natarajan | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| marcus.bell@meetledgerline.com | meetledgerline.com | Marcus Bell | Marcus Bell | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elenar@meetledgerline.com | meetledgerline.com | Elena Ruiz | Elena Ruiz | Active | Group A | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 ET and CT, Mon to Fri | Instantly Unibox |
| priya.natarajan@withledgerline.com | withledgerline.com | Priya Natarajan | Priya Natarajan | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox |
| marcusb@withledgerline.com | withledgerline.com | Marcus Bell | Marcus Bell | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elena@withledgerline.com | withledgerline.com | Elena Ruiz | Elena Ruiz | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox |
| priyan@useledgerline.com | useledgerline.com | Priya Natarajan | Priya Natarajan | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox |
| marcus@useledgerline.com | useledgerline.com | Marcus Bell | Marcus Bell | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elena.ruiz@useledgerline.com | useledgerline.com | Elena Ruiz | Elena Ruiz | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox |
| priya@ledgerline-team.com | ledgerline-team.com | Priya Natarajan | Priya Natarajan | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox |
| marcus.bell@ledgerline-team.com | ledgerline-team.com | Marcus Bell | Marcus Bell | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elenar@ledgerline-team.com | ledgerline-team.com | Elena Ruiz | Elena Ruiz | Active | Group B | 2026-10-15 | 2026-10-29 | 30 | 08:00 to 17:00 MT and PT, Mon to Fri | Instantly Unibox |
| priya.natarajan@goledgerline.com | goledgerline.com | Priya Natarajan | Priya Natarajan | Reserve | Reserve | 2026-10-15 | None (reserve) | 0 | Warmup only | Instantly Unibox |
| marcusb@goledgerline.com | goledgerline.com | Marcus Bell | Marcus Bell | Reserve | Reserve | 2026-10-15 | None (reserve) | 0 | Warmup only | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elena@goledgerline.com | goledgerline.com | Elena Ruiz | Elena Ruiz | Reserve | Reserve | 2026-10-15 | None (reserve) | 0 | Warmup only | Instantly Unibox |
| priyan@ledgerlineapp.com | ledgerlineapp.com | Priya Natarajan | Priya Natarajan | Reserve | Reserve | 2026-10-15 | None (reserve) | 0 | Warmup only | Instantly Unibox |
| marcus@ledgerlineapp.com | ledgerlineapp.com | Marcus Bell | Marcus Bell | Reserve | Reserve | 2026-10-15 | None (reserve) | 0 | Warmup only | Instantly Unibox plus Gmail filter forwarding reply copies to marcus@ledgerline.com |
| elena.ruiz@ledgerlineapp.com | ledgerlineapp.com | Elena Ruiz | Elena Ruiz | Reserve | Reserve | 2026-10-15 | None (reserve) | 0 | Warmup only | Instantly Unibox |
Group A: 4 domains, 12 mailboxes, prospects in Eastern and Central time. Group B: 3 domains, 9 mailboxes, prospects in Mountain and Pacific time. Each person owns 4 mailboxes in Group A and 3 in Group B.

## Signature Block

```text
Priya Natarajan
Head of Sales, Ledgerline
2100 Ledger Ave, Suite 300, Denver, CO 80202
Not the right person? Reply "no thanks" and I won't follow up.
```

Marcus Bell and Elena Ruiz use the same block with their own name and title ("Account Executive, Ledgerline"). Set in: Instantly per-account signature for all 27 accounts, and matched in each Gmail account under Settings > General > Signature for manual replies. Plain text, no logo, no links. Instantly open tracking and link tracking are off, so the `inst` tracking CNAME is set but unused until a later test.

## Warmup and Ramp Schedule

| Dates | Row | Cold cap per mailbox | Warmup per day | Campaign daily limit | Gate to move on |
|-|-|-|-|-|-|
| 2026-10-15 to 2026-10-28 | Warmup only | 0 | 1 rising to 10 | 0 | Instantly health score above 90% over 7 days on each account; header test shows spf=pass, dkim=pass, dmarc=pass |
| 2026-10-29 to 2026-11-04 | Ramp 1 | 10 | 10 | 200 (A 115, B 85) | Hard bounces under 2% per mailbox; no complaint showing in Postmaster Tools |
| 2026-11-05 to 2026-11-11 | Ramp 2 | 20 | 10 | 400 (A 230, B 170) | Same, plus at least 1 human reply across each domain's mailboxes |
| 2026-11-12 to 2026-12-09 | Ramp 3 | 30 | 10 | 600 (A 345, B 255) | Same |
| 2026-12-10 onward | Steady, review | 30, raise to 35 only after 14 days with bounces under 1% and complaints under 0.1% | 10 | 600 | Weekly review |

The A and B split follows the list: 57.5% of the first 1,000 prospects sit in Eastern and Central time, 42.5% in Mountain and Pacific. Reserve mailboxes on goledgerline.com and ledgerlineapp.com stay on the warmup-only row with cap 0 until promoted.

Warmup settings entered in Instantly for all 27 accounts: warmup on, increase per day 1, daily warmup limit 10, reply rate 30%, slow warmup on, weekdays only off for the first 14 days, warm custom tracking domain on. Account daily campaign limit 0 until 2026-10-29, then 10, 20, 30 by row. Minimum wait time 3 minutes. Campaign Slow Ramp off (the per-account limit already does the ramp).

## Sending Rules

| Rule | Value | Source |
|-|-|-|
| Days | Monday to Friday | House standard |
| Hours | 08:00 to 17:00 recipient local time. Group A runs 09:00 to 17:00 America/New_York, so Central recipients get mail 08:00 to 16:00. Group B runs 09:00 to 17:00 America/Denver, so Pacific recipients get mail 08:00 to 16:00 | House standard |
| Gap between sends | Random 3 to 6 minutes per mailbox | Apollo knowledge base (60 to 300 seconds); house standard |
| Max per hour per mailbox | 15 | Apollo knowledge base (10 to 20 an hour) |
| Max per day per mailbox | Ramp row, ceiling 50 | alexberman.com (under 50); house cap 30 |
| Time zone handling | One campaign per rotation group, prospects split by `company_state` into the two groups before upload | `references/warmup-and-ramp.md` section 5 |
| Tracking | Opens off, clicks off | Apple Mail Privacy Protection makes opens unreliable; fewer tracked links |

At a 4.5-minute average gap, a 9-hour window gives each mailbox room for about 120 sends; a cap of 30 uses a quarter of it.

## Reply Monitoring

| Item | Value |
|-|-|
| Owner per rotation group | Group A: Priya Natarajan, backup Elena Ruiz. Group B: Marcus Bell, backup Priya Natarajan |
| Check times | 10:00 and 15:00 Central on sending days, plus 09:00 Monday for weekend replies |
| Positive reply SLA | Human answer within 4 business hours, from the mailbox that received the reply |
| Opt-out handling | Any "no thanks", "remove me" or unsubscribe goes to the Instantly blocklist the same day; domain-level block if the person asks for the company |
| Routing option | Option A (Unibox) for Priya and Elena; Option B (Unibox plus forwarded copies) for Marcus, who answers in Unibox only |

Categories and response templates come from `reply-handling`.

## Rotation and Retirement

| Action | Trigger | Steps | Back in service |
|-|-|-|-|
| Pause | Hard bounces 3% or more over the mailbox's last 200 sends; health score under 80% for 3 days; spam rate 0.3% on the domain | Account daily campaign limit to 0, warmup stays on, log date and cause, promote a reserve mailbox into the group | Cause fixed and list re-validated; restart at Ramp 1 (10 a day) |
| Rest | 2 pauses in 30 days on one domain, or spam rate 0.1% for 2 days on the domain | All 3 mailboxes on the domain to cap 0 for 14 days, warmup on | Full ramp from Ramp 1 after 14 days and a seed test that lands in the inbox at Gmail and Outlook |
| Retire | Domain listed on the Spamhaus DBL again after removal; provider suspension that does not lift in 7 days; 3 pauses in 60 days; owner leaves and 30 days pass | Remove from Instantly, cancel seats at the next Flexible billing date, keep the domain registered and redirecting for 12 months, export replies before deleting users | Not reused for cold email |

Reserves on hand: 2 warmed domains (6 mailboxes), 28.6% of the 7 active domains. Reorder point: when warmed reserves fall to 1 domain, buy and set up one new domain that week (15 to 17 days to ready).

## List Feed and Cost

| Week | Cold sends a day | New prospects | Validation cost |
|-|-|-|-|
| Ramp 1 (2026-10-29 to 2026-11-04) | 200 | 1,000 | 1,000 x $0.0072 = $7.20 |
| Ramp 2 (2026-11-05 to 2026-11-11) | 400 | 1,000 | 1,000 x $0.0072 = $7.20 |
| Ramp 3 (2026-11-12 to 2026-11-18) | 600 | 1,000 | 1,000 x $0.0072 = $7.20 |
| Total | | 3,000 | $21.60 |

Prospects come from `query_lead_database` (VP Sales and Head of Sales, US, 50 to 200 employees, `keywords: ["saas"]`, `hasEmail: true`, `excludeDelivered: true`), included in the ScraperCity Growth plan with no per-row charge. Only `valid` results go to the ramp campaigns; `valid_catch_all` rows wait until 2026-11-12 and then go to a separate catch-all campaign capped at 10% of a day's volume. `check_wallet` showed $412.50 on 2026-10-15, so the $21.60 needed no extra approval step beyond this table.
