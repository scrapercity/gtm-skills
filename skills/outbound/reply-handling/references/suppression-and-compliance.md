# Suppression Rules

What gets suppressed, how fast, at what scope, and how to measure the lag. Every rule here has an operating reason: keep complaint and bounce rates under the mailbox providers' limits, which inbox placement depends on, and keep a promise made in a reply.

## 1. Speed: the mailbox providers' sender requirements

| Provider | Applies to | Unsubscribe processing | Other limits | Source |
|-|-|-|-|-|
| Yahoo sender requirements | Mail to Yahoo and AOL addresses | Within 2 days | One-click unsubscribe header (RFC 8058 POST) plus a visible body link for marketing mail; spam rate under 0.3% | Yahoo |
| Google sender guidelines | Bulk senders to Gmail | Within 48 hours | One-click unsubscribe for marketing messages; spam rate under 0.1%, never 0.3% | Google |

Setting: suppress every opt-out and hostile reply the same day it arrives, in every tool. Berman's follow-up guide says to respect "remove me" immediately, and the same day sits inside both providers' 2 day limit.

### Which rows a deliverable needs

A reply triage or playbook names only the rules its replies trigger: same-day suppression for opt-outs and hostile replies, inside the providers' 2 day limit. Bounce and help-desk rows appear only when the request covers automatic replies or a pasted reply is one.

## 2. What to suppress, and at what scope

| Event | Scope | Duration | Re-contact allowed |
|-|-|-|-|
| Unsubscribe link clicked | Address | Permanent | Only if they write in first |
| "Remove me" or "stop" reply | Address | Permanent | Same |
| "Take our company off your list" | Domain | Permanent | Same |
| Hostile reply or threat | Address; domain if they speak for the company | Permanent | No |
| Spam complaint (feedback loop) | Address | Permanent | No |
| Hard bounce (5.1.x) | Address | Permanent, removed immediately (alexberman.com bounce guide) | Only after a fresh validation and a new source |
| Domain does not accept mail (556 or no MX) | Domain | Permanent | No |
| Reputation block (5.7.1) | None for the contact | Pause the sending domain | After `email-deliverability` clears it |
| Two or three consecutive mailbox-full soft bounces | Address | Permanent: treat as a hard bounce (alexberman.com bounce guide) | Only after a fresh validation |
| Not interested | Address, every sequence from this sender | Permanent | Only if they write in first |
| Competitor customer | Address | Until the renewal date they gave, or a hold the user sets | With a new angle |
| Left company | Address | Permanent | Not applicable |
| Help desk or ticket system address | Address | Permanent | No |

## 3. One suppression list, many tools

| Tool | Where suppression lives | Sync |
|-|-|-|
| Sending platform (Instantly, Smartlead, Lemlist, EmailBison, ManyReach) | Global blocklist at workspace level | Webhook or Zapier, n8n on each new entry |
| CRM (HubSpot, Pipedrive, GoHighLevel) | "Do not contact" boolean and "Outbound status" | Two-way sync with the sending platform |
| ScraperCity pulls | Remove suppressed emails and domains before upload | Filter every CSV against the master list before enrolling |
| Dialer and LinkedIn tools | Same "Do not contact" field | Read from CRM |

ScraperCity's `excludeDelivered: true` skips records your account already received from the databases. It does not know your suppression list, so filter every pull against it before sending.

## 4. Suppression lag log

Keep one row per suppression so the lag can be measured.

| Field | Example |
|-|-|
| Email or domain | jsmith@acmedental.example |
| Scope | Address |
| Reason class | Unsubscribe |
| Source message id | Platform message id of the reply |
| Received at | 2026-10-21 14:02 CT |
| Suppressed at | 2026-10-21 16:40 CT |
| Tools updated | Instantly blocklist, HubSpot DNC |
| Operator | Name or automation id |

Watch the time from "Received at" to "Suppressed at". Anything not suppressed the same day breaks the setting; anything over 2 days misses the Yahoo and Google limit.

## 5. Complaint prevention through reply handling

| Practice | Effect |
|-|-|
| Stop every touch at a company on any reply | No scheduled touch lands in the middle of a conversation (Berman: stop the sequence on a reply) |
| One-click unsubscribe header on every campaign the sequencer supports it for | Google and Yahoo bulk-sender requirement, processed within 2 days |
| Never reply to an auto-responder | RFC 3834; prevents loops |
| Watch unsubscribes per cell | Above 0.5% of prospects, Berman reads the follow-ups as too aggressive or not relevant enough |
| Pause a cell as spam complaints approach Google's 0.1% | Google's line is 0.1%, never 0.3% |

## Sources

- https://senders.yahooinc.com/best-practices/
- https://support.google.com/a/answer/14229414
- https://alexberman.com/soft-vs-hard-bounce-email
- https://alexberman.com/cold-email-follow-up
- https://www.rfc-editor.org/rfc/rfc3834
- https://www.rfc-editor.org/rfc/rfc8058
