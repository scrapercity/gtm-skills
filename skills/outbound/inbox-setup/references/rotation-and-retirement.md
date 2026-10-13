# Rotation and Retirement

How mailboxes share a campaign's volume, how leads stay pinned to one sender, and when a mailbox is paused, rested or retired. Thresholds are house standards built on the provider rules in `references/deliverability-primer.md`.

## 1. Rotation groups

A rotation group is the set of mailboxes attached to one campaign. The sequencer picks the next mailbox for each new lead (Instantly, Smartlead, EmailBison and ManyReach all rotate sender accounts within a campaign).

| Rule | Value | Reason |
|-|-|-|
| Group size | 6 to 12 mailboxes across at least 3 domains | A bad domain carries a third or less of the campaign |
| Domains per group | Every mailbox on a domain in the same group | Keeps a domain's volume predictable and its incidents contained |
| Mailboxes per person per group | 4 or fewer | One person can read replies for 4 mailboxes in a unified inbox; beyond that, replies wait |
| Reserve mailboxes | Not in any active group; warmup only | Ready replacements |
| Campaign daily limit | Group size x per-mailbox cap | Instantly recommends accounts x 30 |
| New mailboxes added to a running group | Only when their ramp row allows; never mix a day-15 mailbox at cap 30 | Caps follow mailbox age |

Example: 21 active mailboxes on 7 domains split into 2 groups. Group A: 4 domains, 12 mailboxes. Group B: 3 domains, 9 mailboxes. Each group runs its own campaign for one segment or time zone.

## 2. Lead pinning

| Rule | How |
|-|-|
| Every step of a sequence goes from the mailbox that sent step 1 | Default in Instantly, Smartlead and Lemlist; check the "send follow-ups from the same account" style setting in others |
| A paused mailbox's in-flight leads | Hold their follow-ups up to 7 days. If the mailbox does not return, end the sequence for those leads rather than switching senders mid-thread |
| A lead who replied | Removed from all campaigns workspace-wide (sequencer stop-on-reply plus blocklist where the lead asked to stop) |
| One company, several contacts | No more than 3 contacts per company domain per campaign (`references/list-quality-standard.md`), spread across different days |

## 3. Health signals per mailbox

| Signal | Where | Green | Watch | Pause |
|-|-|-|-|-|
| Hard bounce rate, last 200 sends | Sequencer analytics per account | Under 1% | 1% to 3% | 3% or more |
| Sequencer warmup health score | Instantly and Smartlead account view | Above 90% | 80% to 90% | Under 80% for 3 days |
| Domain spam rate | Postmaster Tools (personal Gmail traffic only) | Under 0.1% | 0.1% to 0.3% | 0.3% or more: pause every mailbox on the domain |
| Replies | Unified inbox | At least one human reply a week across the domain | No human reply in 2 weeks of full volume | Review copy and list with `email-deliverability` |
| Provider status | Admin console, sequencer connection | Connected | Reconnect needed | Suspended or sending disabled |
| Seed placement | Weekly seed test | Inbox at Gmail and Outlook | Promotions or mixed | Spam at 2 or more seed providers |

## 4. Pause, rest, retire

| Action | Trigger | Steps | Back in service |
|-|-|-|-|
| Pause | Any "Pause" column hit in section 3 | Set the mailbox's daily campaign limit to 0; keep warmup on; log date and reason; promote a reserve mailbox to the group | When the cause is fixed (list re-validated, DNS fixed), restart at ramp row 1 (10 a day) |
| Rest | 2 pauses in 30 days, or a domain-level complaint spike | All mailboxes on the domain to cap 0 for 14 days, warmup on | Full ramp from row 1 after 14 days and a seed test that lands in the inbox at every seed provider |
| Retire | Domain on the Spamhaus DBL and relisted after removal, provider suspension that does not lift, 3 pauses in 60 days, or owner left and 30 days passed | Remove from sequencer, cancel the seat at the next Flexible billing date, keep the domain registered and redirecting for 12 months (mail from prospects may still arrive), delete the user only after exporting replies | Not reused for cold email |

Keep retired domains registered: if a burned domain lapses, someone else can register it and receive mail meant for your former reps.

## 5. Replacement timing

A reserve must be fully warmed when it is needed, so the number of warmed reserves is the real safety margin.

| Item | Value |
|-|-|
| Lead time for a new reserve | 14 days warmup plus 1 to 3 days of DNS and setup = 15 to 17 days |
| Reserves on hand | At least 20% of active domains, minimum 1 (`domain-infrastructure`) |
| Reorder point | When warmed reserves fall to 1 domain, buy and set up a new one that week |

Example: 7 active domains, 2 reserves. A domain gets retired in week 6; one reserve goes active the same day, leaving 1. Reorder point hit: buy one domain, set up 3 mailboxes, warmup starts within 2 days, ready 14 days later.

## 6. Weekly review agenda (20 minutes)

1. Sequencer account table sorted by bounce rate: any mailbox at 1% or more over its last 200 sends.
2. Health scores under 90%.
3. Postmaster Tools spam rate per domain where data shows.
4. Seed test results.
5. Human replies per domain.
6. Ramp moves due this week (mailboxes moving rows).
7. Reserves on hand vs reorder point.
8. Log every pause, rest and retirement with date and cause.

## Sources

- Instantly, Account and campaign limits: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Smartlead, High bounce rate auto protection: https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Spamhaus, Domain Blocklist: https://www.spamhaus.org/blocklists/domain-blocklist/
- Google Workspace, Compare Flexible and Annual plans: https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans
- M3AAWG, Sender Best Common Practices v4.0: https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
