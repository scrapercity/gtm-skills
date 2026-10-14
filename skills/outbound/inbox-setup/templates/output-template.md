# Mailbox Roster and Ramp: [fill company]

[fill: one line with the date and, only if the brief left them out, the stand-in names used]

## Summary

[fill: at most three sentences: the warmup path chosen and the one reason, and anything the table cannot say. No date or count that the table below already gives]

| Item | Value |
|-|-|
| Main domain (never sends cold email) | [fill] |
| Sequencer | [fill] |
| Active mailboxes | [fill] |
| Reserve mailboxes | [fill] |
| Warmup path | [fill] |
| First cold send | [fill] |
| Full volume date | [fill] |
| Steady-state cold sends a day | [fill] |

## Sender Identities

| Person | Title | Mailboxes owned | Reply backup |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

[fill: the address format rotation and the display-name rule, stated once]

## Mailbox Roster

| Mailbox | Owner | Provider | Role | Group | Wave |
|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

## Account Settings

| Setting | [fill provider] | [fill provider] |
|-|-|-|
| Sign-in security | [fill] | [fill] |
| Sequencer connection | [fill] | [fill] |
| Volume guard | [fill] | [fill] |
| Tenant-wide limit | [fill] | [fill] |
| Photo and recovery | [fill] | [fill] |

DNS records on each sending domain:

| Record | [fill provider] | [fill provider] |
|-|-|-|
| MX | [fill exact value and priority] | [fill] |
| SPF (TXT on @) | [fill exact v=spf1 value] | [fill] |
| DKIM | [fill host, e.g. google._domainkey, and key length] | [fill] |
| DMARC (TXT on `_dmarc`) | [fill exact v=DMARC1 value with a report address] | [fill] |

## Signature Block

```text
[fill name]
[fill title], [fill company]
[fill opt-out line]
```

Set in: [fill sequencer and mail client]

## Warmup and Ramp Schedule

| Wave | Mailboxes | Warmup start | First cold send | Cold cap at full volume |
|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] |

| Dates | Row | Cold cap per mailbox | Warmup per day | Campaign daily limit | Gate to move on |
|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

| Date | Step | Done when |
|-|-|-|
| [fill] | [fill: DNS, users, security, photos] | [fill] |
| [fill] | [fill: register and verify every sending domain in Google Postmaster Tools] | [fill] |
| [fill] | [fill: header test, OAuth connection, warmup on (reserves the same day)] | [fill] |
| [fill] | [fill: list validated, only `valid` rows loaded] | [fill] |
| [fill] | [fill: gate check with the named inbox placement test] | [fill] |
| [fill] | [fill: first cold send] | [fill] |

Tenant quota check: [fill only when a mailbox is on Microsoft 365; otherwise delete this line]

Warmup settings entered: [fill, with the exact setting names]

## Sending Rules

| Rule | Value | Source |
|-|-|-|
| Days | [fill] | [fill] |
| Hours | [fill] | [fill] |
| Gap between sends | [fill] | [fill] |
| Max per hour per mailbox | [fill] | [fill] |
| Max per day per mailbox | [fill] | [fill] |
| Time zone handling | [fill] | [fill] |
| Tracking | [fill] | [fill] |

## Reply Monitoring

| Item | Value |
|-|-|
| Owner per rotation group | [fill] |
| Check times | [fill] |
| Positive reply response target | [fill the team's target and how it is measured] |
| Opt-out handling | [fill] |
| Routing | [fill] |

## Rotation and Retirement

| Action | Trigger | Steps | Back in service |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

Reserves on hand: [fill]. Reorder point: [fill].
