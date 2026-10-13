# Suppression and Compliance

What gets suppressed, how fast, at what scope, and how to prove it later. Nothing here is legal advice; see `references/outbound-compliance-primer.md` and ask counsel for your jurisdiction.

## 1. Deadlines by rule

| Rule | Applies to | Opt-out deadline | Notes | Source |
|-|-|-|-|-|
| CAN-SPAM | Commercial email to US recipients, including B2B | 10 business days | Opt-out must work for at least 30 days after sending; no fee or extra info to opt out; penalties up to $53,088 per email | FTC |
| Yahoo sender requirements | Mail to Yahoo and AOL addresses | 2 days | One-click unsubscribe header (RFC 8058 POST recommended) plus a visible body link for marketing mail | Yahoo |
| Google sender guidelines | Bulk senders to Gmail | 48 hours (recommended) | One-click unsubscribe for marketing messages; spam rate under 0.1%, never 0.3% | Google |
| CASL | Commercial electronic messages to Canadian addresses | 10 business days | Unsubscribe mechanism valid for 60 days after sending; consent required | CRTC |
| PECR | UK marketing email | Promptly; keep a do-not-email list | Corporate subscribers can be emailed without consent; sole traders cannot | ICO |
| GDPR (EU, UK GDPR) | Personal data of EU and UK individuals, including work emails | Right to object to direct marketing is absolute | Keep the minimum data needed to honor the objection | See shared compliance primer |

Internal rule that meets all of them: suppress within 1 business day, everywhere.

## 2. What to suppress, and at what scope

| Event | Scope | Duration | Re-contact allowed |
|-|-|-|-|
| Unsubscribe link clicked | Address | Permanent | Only if they opt in later |
| "Remove me" or "stop" reply | Address | Permanent | Same |
| "Take our company off your list" | Domain | Permanent | Same |
| Angry reply or threat | Address; domain if they speak for the company | Permanent | No |
| Spam complaint (feedback loop) | Address | Permanent | No |
| Hard bounce (5.1.x) | Address | Permanent | Only after a fresh validation and a new source |
| Domain does not accept mail (556 or no MX) | Domain | Permanent | No |
| Reputation block (5.7.1) | None for the contact | Pause the sending domain | After `email-deliverability` clears it |
| Soft bounce 3 times | Address | 90 days | After re-validation |
| Not interested | Address, this offer | 180 days | New offer only |
| Competitor customer | Address | 180 days | With a complementary angle |
| Left company | Address | Permanent | Not applicable |
| Help desk or ticket system address | Address | Permanent | No |

## 3. One suppression list, many tools

| Tool | Where suppression lives | Sync |
|-|-|-|
| Sending platform (Instantly, Smartlead, Lemlist, EmailBison, ManyReach) | Global blocklist, workspace level, not campaign level | Webhook or Zapier, n8n on each new entry |
| CRM (HubSpot, Pipedrive, GoHighLevel) | "Do not contact" boolean and "Outbound status" | Two-way sync with the sending platform |
| ScraperCity pulls | Remove suppressed emails and domains before upload | Filter the CSV against the master list before `validate_emails` |
| Dialer and LinkedIn tools | Same "Do not contact" field | Read from CRM |

ScraperCity's `excludeDelivered: true` skips records your account already received from the databases. It does not know your suppression list, so filter every pull against it before sending.

## 4. Audit log

Keep one row per suppression for at least as long as you send cold email.

| Field | Example |
|-|-|
| Email or domain | jsmith@acmedental.com |
| Scope | Address |
| Reason class | Unsubscribe |
| Source message id | Platform message id of the reply |
| Received at | 2026-10-21 14:02 CT |
| Suppressed at | 2026-10-21 16:40 CT |
| Tools updated | Instantly blocklist, HubSpot DNC |
| Operator | Name or automation id |

The gap between "Received at" and "Suppressed at" is the number to watch. Anything over 2 days breaks the Yahoo rule.

## 5. Complaint prevention through reply handling

| Practice | Effect |
|-|-|
| Stop every touch at a company on any reply | Removes the "they ignored my reply" complaint |
| Plain opt-out line in every touch ("Reply 'no' and I won't follow up") | Gives a softer exit than the spam button |
| Answer "how did you get my email" honestly and briefly | Lowers hostility |
| Never reply to an auto-responder | Prevents loops |
| Pause a cell when angry replies pass 5% of all replies | Caught before Gmail's 0.1% threshold is reached |

## 6. Referral capture and data minimization

When enrolling a referred person, store only what the outreach needs: name, work email, company, title, the referrer's name, and the date. Do not store personal mobile numbers unless you plan a phone touch that has passed the TCPA and DNC checks in `multi-channel-outreach`.

## Sources

- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://senders.yahooinc.com/best-practices/
- https://support.google.com/a/answer/14229414
- https://crtc.gc.ca/eng/com500/faq500.htm
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/
- https://alexberman.com/soft-vs-hard-bounce-email
- https://www.rfc-editor.org/rfc/rfc8058
