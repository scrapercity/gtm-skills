# Reply Taxonomy and Routing

Fifteen reply classes, how to detect each, and what happens next. Priority order for replies that fit two classes: Unsubscribe > Angry > Bounce > Interested > Referral > Objection > Not now > Wrong person > Other.

## 1. Classes

| # | Class | Typical wording | Detect | Next action |
|-|-|-|-|-|
| 1 | Interested: meeting | "Sure, Tuesday works", "Send times" | Agreement plus time words | Reply with two slots or booking link inside 1 business hour |
| 2 | Interested: info first | "Send more info", "What does it cost?" | Request for material or price | Short answer plus a proposed call (no PDF) |
| 3 | Interested: question | "Does it work with Dentrix?" | A product question with no objection | Answer in one line, then ask for the call |
| 4 | Referral: named | "Talk to Sarah Kim, she runs ops" | A person's name, often with a role | `find_emails`, validate, enroll; thank referrer |
| 5 | Referral: role only | "Our marketing team handles that" | A team or title, no name | `query_lead_database` by domain and title, then enroll |
| 6 | Objection: no need | "We're fine", "Not a problem for us" | Denial of the problem | One feedback question, then close |
| 7 | Objection: competitor | "We use Birdeye" | Vendor name | Ask what made them choose it; position as complement |
| 8 | Objection: price or budget | "No budget", "Too expensive" | Money words | Offer smaller start or pilot; ask timing |
| 9 | Objection: timing | "Busy until January" | Date or season without a no | Becomes Not now with that date |
| 10 | Not now | "Reach out next quarter" | Future date, polite | Nurture; task on the date |
| 11 | Wrong person | "I don't handle that" | Role mismatch, no name | Ask who does, one line |
| 12 | Left company | "No longer with Acme" (human or auto) | Departure words | Suppress address; find replacement with Lead Database |
| 13 | Unsubscribe | "Remove me", "Stop", "Unsubscribe" | Opt-out words, any tone | Suppress; no sales reply |
| 14 | Angry or complaint | Profanity, "How did you get my email", "Reported as spam" | Hostility, data questions, threats | Suppress; optional one-line apology and data source answer; review cell |
| 15 | Automatic | OOO, auto-ack, ticket created, bounce | Headers and patterns in section 2 | Pause or suppress; never reply |

### Edge cases

| Reply | Class | Why |
|-|-|-|
| "Not interested, but try Sarah" | Referral: named | The referral is actionable; record the objection as a note |
| "Interested, but take me off the list" | Unsubscribe | Opt-out wins; ask nothing further by email |
| "What's this about?" | Interested: question | Curious, not hostile; answer in two lines |
| "Who gave you my email?" | Angry or complaint | Answer honestly in one line that the address came from a business database, then suppress if asked |
| A single "?" or "." | Other | Treat as Interested: question; restate the offer in one line |
| Calendar invite accepted with no text | Interested: meeting | Confirm and send agenda |
| Reply from a different person at the company | Use their words to classify; link to the original contact | Same company stop rule applies |

## 2. Automatic reply detection

Check in this order. The first match wins.

| Check | Rule | Class |
|-|-|-|
| Return path is empty (`<>`) | RFC 3834 says responders must not reply to a null return path | Bounce or system |
| `Content-Type: multipart/report` with `report-type=delivery-status` | Delivery status notification | Bounce |
| Status code `5.1.1`, `5.1.10`, `5.2.1`, `5.4.1`, "user unknown", "mailbox unavailable", "does not exist" | Permanent failure | Hard bounce: suppress |
| Status code `4.x.x`, "mailbox full", "try again later" | Temporary failure | Soft bounce: retry once after 72 hours, suppress after 3 soft bounces |
| Status code `5.7.1` or text naming spam, policy or reputation | Block of the sender, not a bad address (per alexberman.com bounce guide) | Do not suppress the contact; pause the sending domain and route to `email-deliverability` |
| `Auto-Submitted: auto-replied` or `auto-generated` | RFC 3834 values other than `no` mark automatic mail | Automatic |
| `X-Autoreply: yes`, `X-Autorespond`, `Precedence: auto_reply`, `Precedence: bulk` or `junk` | Common auto-responder headers | Automatic |
| Subject begins "Automatic reply", "Auto-Reply", "Out of Office", "OOO", "Autoreply", "Abwesenheit", "Absence", "Réponse automatique", "Respuesta automática" | Client defaults | OOO |
| Body: "I am out of the office", "on leave", "parental leave", "returning on", "back on" + date | OOO language | OOO with return date |
| Body: "no longer with", "has left the company", "this inbox is no longer monitored" | Departure | Left company |
| Body: "your ticket", "we received your request", "case number" | Help desk | Automatic: suppress the address from outbound |

### OOO return date parsing

| Pattern | Example | Resume on |
|-|-|-|
| "back on [date]" | back on Monday, October 20 | Return date plus 1 business day |
| "returning [date]" | returning 10/20 | Same |
| "until [date]" | out until the 24th | Day after, plus 1 business day |
| Leave with no date | on parental leave | Pause 60 days, then resume |
| No date at all | out of office | Pause 7 days |

If the OOO names an alternate contact ("for anything urgent, contact Jen at jen@acme.com"), log it as a role-only referral; do not email the alternate until the original contact's sequence ends.

## 3. CRM state map

| Class | Lead status | Lifecycle | Sequence action | Task | Deal |
|-|-|-|-|-|-|
| Interested: meeting | Interested | Sales qualified lead | Stop for every contact at the company | Reply in 1 hour | Create, "Meeting requested" |
| Meeting booked | Meeting booked | Sales qualified lead | Stopped | Prep note | "Meeting scheduled" |
| Interested: info | Interested | Marketing qualified lead | Stop at company | Reply in 2 hours | Create, "Engaged" |
| Interested: question | Interested | Marketing qualified lead | Stop at company | Reply in 2 hours | None until meeting |
| Referral: named | Referred | Lead | Stop for referrer | Enroll referral within 1 day | Note on new contact |
| Referral: role only | Referred | Lead | Stop for referrer | Lead Database lookup | None |
| Objection: no need | Not interested | Other | Stop | None | None |
| Objection: competitor | Competitor: [name] | Other | Stop | Re-engage in 6 months | None |
| Objection: price | Objection: budget | Lead | Stop | Re-engage next budget cycle | None |
| Not now / timing | Nurture | Lead | Stop | Task on stated date | None |
| Wrong person | Wrong person | Other | Stop | Ask who owns it | None |
| Left company | Left company | Other | Stop; suppress address | Find replacement | None |
| Unsubscribe | Do not contact | Other | Stop everywhere | Suppress | None |
| Angry | Do not contact | Other | Stop everywhere | Suppress; manager review | None |
| OOO | Paused | Unchanged | Pause to resume date | None | None |
| Hard bounce | Bounced | Other | Stop; suppress | Check list source | None |

## 4. Platform setup notes

| Platform | What to configure | Source |
|-|-|-|
| Instantly | Lead statuses for Interested, Meeting booked, Not interested, Wrong person, OOO. For OOO auto-resume, turn off "Stop on auto-reply" in sending rules and enable automatic status tagging. | Instantly help center |
| Smartlead | Lead categories in the master inbox; categories such as "Requested info" can trigger a subsequence. | Smartlead help center |
| Lemlist, EmailBison, ManyReach | Map their reply labels to the classes above and to one blocklist | Platform docs |
| CRM (HubSpot, Pipedrive, GoHighLevel) | One "Outbound status" property with the class values; one "Do not contact" boolean read by every tool | Internal policy |

Stop on reply must work at company (domain) level, so a positive reply from one person stops touches to their colleagues.

## 5. Daily triage loop

| Time | Action |
|-|-|
| Every hour in business hours | Interested and Interested: info replies answered |
| Twice a day | Referrals logged; objections and not-now answered |
| End of day | Unsubscribes, angry and bounces confirmed in global suppression; referral batch sent to `find_emails` |
| Weekly | Class counts per cell; bounce rate and complaint review |

## Sources

- https://www.rfc-editor.org/rfc/rfc3834
- https://help.instantly.ai/en/articles/9713093-ooo-resume-ai-smart-pause-for-out-of-office
- https://helpcenter.smartlead.ai/en/articles/51-lead-categories
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/soft-vs-hard-bounce-email
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
