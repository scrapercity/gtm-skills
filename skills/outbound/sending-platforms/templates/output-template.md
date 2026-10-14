# Sending Platform Plan: [fill company]

Prepared [fill date] for [fill team or client]. Vendor pages checked [fill date]. [fill: one line on what is assumed, if anything]

## Summary

[fill: at most 110 words: the platform and plan, its monthly price, the all-in total, and the one reason it wins. No comparisons or cap dates here]

## Assumptions and Open Questions

| Question | Answer | Answered by user or assumed |
|-|-|-|
| HubSpot portals: one, or one per client | [fill] | [fill] |
| Client logins needed | [fill] | [fill] |
| Inbox mix (Google, Microsoft, other) | [fill] | [fill] |
| Current sending tool | [fill: a named tool, or "None"] | [fill] |
| Monthly budget ceiling, all-in | [fill] | [fill] |

## Requirements

| Input | Value | Source |
|-|-|-|
| New prospects per day | [fill] | [fill] |
| Steps per sequence | [fill] | [fill] |
| Contacts per month (month 1 and month 2) | [fill] | [fill] |
| Sends per month (month 1 and month 2) | [fill] | [fill] |
| Mailboxes connected | [fill] | [fill] |
| Seats and workspaces | [fill] | [fill] |
| Client workspaces | [fill: 0 for in-house, else the number of clients] | [fill] |
| CRM and middleware | [fill] | [fill] |

## Platform Decision

| Option | Plan and price | Fits because | Gaps | Checked |
|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] |

Decision: [fill: platform, plan, billing period, and the price gap to the runner-up with the dearer plan named. The only place the gap appears]

Revisit if: [fill: the measurable trigger that changes the choice, such as stored contacts passing a number; the cost of the next plan stays in Cost]

## Workspace Settings

| Setting | Value | Source |
|-|-|-|
| Daily limit per mailbox | [fill] | [fill] |
| Gap between emails | [fill] | [fill] |
| Campaign daily limit | [fill] | [fill] |
| Schedule | [fill] | [fill] |
| Plain text | [fill] | [fill] |
| Open tracking | [fill: Off] | [fill] |
| Link tracking | [fill] | [fill] |
| Unsubscribe header | [fill] | [fill] |
| Stop on reply | [fill: lead and company] | [fill] |
| Out-of-office replies | [fill] | [fill] |
| Bounce auto-pause | [fill: the value to type] | [fill] |
| Client assignment (agency only) | [fill] | [fill] |

## Column Map

| Source | Source column | Platform variable | Merge tag | Fallback |
|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] |

## Import Procedure

Each action is a vendor screen or a REST call a person runs. When the user already sends and named no tool, include: load the old tool's unsubscribes and bounces first; mid-sequence prospects finish on the old tool; warmup on in one tool at a time.

| Step | Action | Owner | Due | Pass when |
|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill: YYYY-MM-DD] | [fill] |

## Suppression and Dedupe

| List | Match on | Where it lives | Sync |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

## Webhooks to CRM

Writer per event: [fill: native integration or webhook flow, never both for one event]

| Business event | Platform event | Writer | CRM action | Sequencer action |
|-|-|-|-|-|
| [fill: Replied, Interested, Unsubscribed, Bounced] | [fill] | [fill] | [fill] | [fill] |
| Meeting booked | [fill: the calendar booking, never a reply label] | [fill] | [fill] | [fill] |
| Meeting held or No-show | [fill: the meeting outcome] | [fill] | [fill] | [fill] |

Positive replies: [fill: who answers every Interested reply, from where, and how reply-to-answer time is measured]

## Test Plan

| Test | Pass when | Owner | Due |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill: YYYY-MM-DD] |
| Weekly reconciliation | [fill: the week's Interested leads in the sequencer each have a deal in the CRM] | [fill] | [fill: YYYY-MM-DD] |

## Migration Plan

Include this section only when the user named a current tool. With no named tool, delete this section.

Old tool: [fill]

| Step | Action | Date | Done when |
|-|-|-|-|
| Pre-commitment trial | [fill] | [fill] | [fill] |
| Export from old tool | [fill] | [fill] | [fill] |
| Mid-sequence prospects finish on old tool | [fill] | [fill] | [fill] |
| Rebuild sequences | [fill] | [fill] | [fill] |
| Reconnect the same mailboxes | [fill] | [fill] | [fill] |
| Re-point tracking CNAME | [fill] | [fill] | [fill] |
| Parallel run | [fill] | [fill] | [fill] |
| Decommission old tool | [fill] | [fill] | [fill] |

## Cost

Total: sequencer, client workspaces, mailboxes, domains and automation. Mailboxes and domains already sending are labeled existing (reconnected, no purchase). The Total equals the sum of the lines.

| Line | Count | Unit price | Monthly |
|-|-|-|-|
| Sequencer plan | [fill] | [fill] | [fill] |
| Client workspaces (agency only) | [fill] | [fill] | [fill] |
| Mailboxes | [fill: existing reconnected, plus any new] | [fill] | [fill] |
| Domains | [fill] | [fill] | [fill] |
| Automation (middleware) | [fill] | [fill] | [fill] |
| Total | [fill] | [fill] | [fill] |

[fill: the cap step once: the month, the next plan and the new total]

Optional, not in the total unless the request includes building the list: [fill: data and validation lines]
