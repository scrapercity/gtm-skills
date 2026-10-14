# Rotation and Retirement

How mailboxes share a campaign's volume, how leads stay pinned to one sender, and when a mailbox is paused, rested or retired. Thresholds come from the sources named in each row; the provider rules behind them are in `references/deliverability-primer.md`.

## 1. Rotation groups

A rotation group is the set of mailboxes attached to one campaign. The sequencer picks the next mailbox for each new lead (Instantly, Smartlead, EmailBison and ManyReach all rotate sender accounts within a campaign).

| Rule | Value | Reason |
|-|-|-|
| Domains per group | Every mailbox on a domain in the same group, and each group spread over several domains | A bad domain carries only its share of the campaign |
| Reserve mailboxes | Not in any active group; warmup only | Ready replacements |
| Campaign daily limit | Group size x per-mailbox cap | Instantly recommends accounts x 30 |
| New mailboxes added to a running group | Only at their own ramp row; Instantly's slow ramp is set per account | Caps follow mailbox age |
| Mailboxes per person | As many as the owner can answer replies for in the sequencer's unified inbox | Measure reply wait time and move mailboxes when it grows |

Example: 21 active mailboxes on 7 domains split into 2 groups. Group A: 4 domains, 12 mailboxes. Group B: 3 domains, 9 mailboxes. Each group runs its own campaign for one segment or time zone.

## 2. Lead pinning

| Rule | How |
|-|-|
| Every step of a sequence goes from the mailbox that sent step 1 | Default in Instantly, Smartlead and Lemlist; check the "send follow-ups from the same account" style setting in others |
| A paused mailbox's in-flight leads | Hold their follow-ups until the mailbox returns. If it does not return, end the sequence for those leads rather than switching senders mid-thread |
| A lead who replied | Removed from all campaigns workspace-wide (sequencer stop-on-reply plus blocklist where the lead asked to stop, the same day) |
| One company, several contacts | Spread across different days |

## 3. Health signals per mailbox

| Signal | Where | Green | Watch | Pause |
|-|-|-|-|-|
| Hard bounce rate | Sequencer analytics, per campaign after 200 sends | Under 2% | 2% to 5%: re-validate the list (Alex Berman's warning zone) | Over 5% (Alex Berman's critical line; Instantly's default auto-pause) |
| Sequencer warmup health score | Instantly and Smartlead account view | Above 90% (Instantly's readiness line) | | Under 90%: hold cold sends at the current cap until it recovers |
| Domain spam rate | Postmaster Tools (personal Gmail traffic only) | Under 0.1% (Google) | 0.1% to 0.3% | 0.3% or more (Google): pause every mailbox on the domain |
| Provider status | Admin console, sequencer connection | Connected | Reconnect needed | Suspended or sending disabled |
| Seed placement | Instantly Inbox Placement test (Gmail and Microsoft) | Inbox at Gmail and Microsoft | Promotions or mixed | Spam at a seed provider after copy, links and authentication were checked |

## 4. Pause, rest, retire

| Action | Trigger | Steps | Back in service |
|-|-|-|-|
| Pause | Any "Pause" column hit in section 3 | Set the mailbox's daily campaign limit to 0; keep warmup on; log date and reason; promote a reserve mailbox to the group | When the cause is fixed (list re-validated, DNS fixed); the slow ramp resumes from its last limit unless the user restarts it lower |
| Rest | A domain-level spam rate over Google's 0.1% | All mailboxes on the domain to cap 0, warmup on, for a period the user sets | After the rest and a seed test that reaches the inbox at every seed provider |
| Retire | Domain on the Spamhaus DBL and relisted after removal, a provider suspension that does not lift, or the owner left the company | Remove from sequencer, cancel the seat at the next Flexible billing date, keep the domain registered and redirecting (mail from prospects may still arrive), delete the user only after exporting replies | Not reused for cold email |

Keep retired domains registered: if a burned domain lapses, someone else can register it and receive mail meant for your former reps.

## 5. Replacement timing

A reserve must be fully warmed when it is needed, so the number of warmed reserves is the safety margin.

| Item | Value |
|-|-|
| Lead time for a new reserve | DNS and setup (Google's DKIM key appears 24 to 72 hours after Gmail is on) plus 21 days of warmup, about 22 to 24 days (15 to 17 on the soft start) |
| Reserves on hand | The user's reserve share, at least one domain per rotation group, warming from the first active wave's start so it is ready on the first cold send. Growth Engine X keeps backup domains always warming and builds 1,500 a day of capacity for a 1,000 goal, 50%. A 1:1 backup (one warmed reserve per active mailbox) doubles the seat bill: for 50 active Google mailboxes, 50 x $8.40 = $420 a month more (price checked 2026-10-13) |
| Reorder point | When a reserve is promoted, buy and set up its replacement that week |

Example: 7 active domains, 2 reserves. A domain gets retired in week 6; one reserve goes active the same day, leaving 1. Buy one domain, set up 3 mailboxes, warmup starts within 2 days, ready 21 days later.

## 6. Review agenda

1. Sequencer campaign table sorted by bounce rate: any campaign at 2% or more after 200 sends.
2. Health scores under 90%.
3. Postmaster Tools spam rate per domain where data shows.
4. Seed test results.
5. Human replies per domain.
6. Mailboxes moving ramp rows this week.
7. Reserves on hand.
8. Log every pause, rest and retirement with date and cause.

## Sources

- Instantly, Account and campaign limits: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Instantly, High bounce auto-pause (5% after 200 sends by default; checked 2026-10-13): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Instantly, Campaign slow ramp (remembers the last limit; checked 2026-10-13): https://help.instantly.ai/en/articles/10056946-campaign-slow-ramp-system
- Instantly, When your email account is ready for campaigns (health score above 90%): https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Smartlead, High bounce rate auto protection: https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- Alex Berman, custom tracking domains and Gmail (2% warning, 5% critical; May 11, 2026): https://alexberman.com/custom-tracking-domain-gmail
- Google, Top 10 Gmail sender issues (spam rate below 0.1%): https://support.google.com/mail/answer/15256272
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Google Workspace, Set up DKIM: https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Growth Engine X, methodology (checked 2026-10-13): https://coldoutbound.com/
- Spamhaus, Domain Blocklist: https://www.spamhaus.org/blocklists/domain-blocklist/
- Google Workspace, Compare Flexible and Annual plans: https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans
