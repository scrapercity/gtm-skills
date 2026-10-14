# Reply Taxonomy and Routing

Fifteen reply classes, how to detect each, what happens next, and which of those steps automation may take alone. Priority order for replies that fit two classes: Hostile > Unsubscribe > Bounce > Interested > Referral > Objection > Not now > Wrong person > Other. Hostile sits first so an opt-out written in anger never gets the automated removal line meant for a polite one.

## 1. Classes

| # | Class | Typical wording | Detect | Next action |
|-|-|-|-|-|
| 1 | Interested: meeting | "Sure, Tuesday works", "Send times" | Agreement plus time words | Reply with two slots or booking link inside 5 minutes |
| 2 | Interested: info first | "Send more info", "What does it cost?" | Request for material or price | Short answer plus a proposed call inside 5 minutes (no PDF, no price sheet) |
| 3 | Interested: question | "Does it work with Dentrix?" | A product question with no objection | Answer in one line, then ask for the call |
| 4 | Referral: named | "Talk to Sarah Kim, she runs ops" | A person's name, often with a role | `find_emails` (found addresses come back already validated), enroll; thank referrer |
| 5 | Referral: role only | "Our marketing team handles that" | A team or title, no name | `query_lead_database` by domain and title, then enroll |
| 6 | Objection: no need | "We're fine", "Not a problem for us" | Denial of the problem | Accept and stop in one or two lines (R13), no question |
| 7 | Objection: competitor | "We use Birdeye" | Vendor name | Acknowledge; name one industry problem the offer takes over; nurture (R14) |
| 8 | Objection: price or budget | "No budget", "Too expensive" | Money words | Offer smaller start or pilot; ask timing |
| 9 | Objection: timing | "Busy until January" | Date or season without a no | Becomes Not now with that date |
| 10 | Not now | "Reach out next quarter" | Future date, polite | Nurture; task on the date |
| 11 | Wrong person | "I don't handle that" | Role mismatch, no name | Ask who does, one line |
| 12 | Left company | "No longer with Acme" (human or auto) | Departure words | Suppress address; find replacement with Lead Database |
| 13 | Unsubscribe | "Remove me", "Stop", "Unsubscribe" | Opt-out words, any tone | Suppress; no sales reply |
| 14 | Hostile (needs review) | "This is spam", "I'm reporting you", "my lawyer", profanity, "how did you get my email" | Any trigger word in section 1b | Suppress now; a person decides the reply (R26 or none); never automated |
| 15 | Automatic | OOO, auto-ack, ticket created, bounce | Headers and wording rules in section 2 | Pause or suppress; never reply |

### Edge cases

| Reply | Class | Why |
|-|-|-|
| "Not interested, but try Sarah" | Referral: named | The referral is actionable; record the objection as a note |
| "Interested, but take me off the list" | Unsubscribe | Opt-out wins; ask nothing further by email |
| "What's this about?" | Interested: question | Curious; answer in two lines |
| "Who gave you my email?" | Hostile (complaint group) | A person answers in one line that the address came from a business contact database (R26); suppress |
| A single "?" or "." | Other | Treat as Interested: question; restate the offer in one line |
| Calendar invite accepted with no text | Interested: meeting | Confirm day, date, time and time zone with R29 inside 5 minutes |
| Reply from a different person at the company | Use their words to classify; link to the original contact | Same company stop rule applies |

### 1b. Needs-review trigger words

Any of these words or phrases, in any class, moves the reply to Hostile. Automation may suppress the address; it may not send anything, including the polite unsubscribe line. Match on whole words, case-insensitive, in the reply body only (not the quoted thread below it), so your own email's footer can't trigger it.

| Group | Trigger words and phrases | What a person does | Within |
|-|-|-|-|
| Complaint | spam, spamming, report, reported, reporting, junk, blacklist, block, abuse, harass, harassment, unsolicited, how did you get my email, where did you get my email | Confirms suppression; sends R26 (which answers where the address came from) or nothing | Same day |
| Threat | lawyer, attorney, sue, lawsuit, cease and desist | No reply from sales; forwards to the escalation owner the user names | Same day |
| Data request | delete my data, erase my data, what data do you have, what information do you hold | Confirms suppression; sends R26 or nothing | Same day |
| Profanity or threat | Any profanity, threats, all-caps demands | Confirms suppression; sends R26 or nothing | Same day |

"Report" and "block" also appear in friendly replies ("I'll report back", "block out an hour"). The trigger still routes them to a person; a person reclassifies in seconds, while a template sent to a real complaint can't be taken back.

## 2. Automatic reply detection

Check in this order. The first match wins.

| Check | Rule | Class |
|-|-|-|
| Return path is empty (`<>`) | RFC 3834 says responders must not reply to a null return path | Bounce or system |
| `Content-Type: multipart/report` with `report-type=delivery-status` | Delivery status notification | Bounce |
| Status code `5.1.1`, `5.1.10`, `5.2.1`, `5.4.1`, "user unknown", "mailbox unavailable", "does not exist" | Permanent failure | Hard bounce: suppress |
| Status code `4.x.x`, "mailbox full", "try again later" | Temporary failure; platforms retry over 24 to 72 hours (alexberman.com bounce guide) | Soft bounce: let the platform retry; after two or three consecutive mailbox-full bounces, suppress as a hard bounce |
| Status code `5.7.1` or text naming spam, policy or reputation | Block of the sender; the address itself may be fine (per alexberman.com bounce guide) | Do not suppress the contact; pause the sending domain and route to `email-deliverability` |
| `Auto-Submitted: auto-replied` or `auto-generated` | RFC 3834 values other than `no` mark automatic mail | Automatic |
| `X-Autoreply: yes`, `X-Autorespond`, `Precedence: auto_reply`, `Precedence: bulk` or `junk` | Common auto-responder headers | Automatic |
| Subject begins "Automatic reply", "Auto-Reply", "Out of Office", "OOO", "Autoreply", "Abwesenheit", "Absence", "Réponse automatique", "Respuesta automática" | Client defaults | OOO |
| Body: "I am out of the office", "on leave", "parental leave", "returning on", "back on" + date | OOO language | OOO with return date |
| Body: "no longer with", "has left the company", "this inbox is no longer monitored" | Departure | Left company |
| Body: "your ticket", "we received your request", "case number" | Help desk | Automatic: suppress the address from outbound |

### OOO return date parsing

| Wording | Example | Resume on |
|-|-|-|
| "back on [date]" | back on Monday, October 19 | The return date (Instantly's OOO resume pauses the lead until then) |
| "returning [date]" | returning 10/20 | Same |
| "until [date]" | out until the 24th | The day after |
| Leave with no date | on parental leave | A pause length the user sets; neither Instantly nor Smartlead documents a default |
| No date at all | out of office | Same: the user's setting |

If the OOO names an alternate contact ("for anything urgent, contact Jen at jen@acme.example"), log it as a role-only referral; do not email the alternate until the original contact's sequence ends.

## 3. CRM state map

| Class | Lead status | Lifecycle | Sequence action | Task | Deal |
|-|-|-|-|-|-|
| Interested: meeting | Interested | Sales qualified lead | Stop for every contact at the company | Reply in 5 minutes | Create, "Meeting requested" |
| Meeting booked | Meeting booked | Sales qualified lead | Stopped | Prep note | "Meeting scheduled" |
| Interested: info | Interested | Marketing qualified lead | Stop at company | Reply in 5 minutes | Create, "Engaged" |
| Interested: question | Interested | Marketing qualified lead | Stop at company | Reply or holding reply in 5 minutes | None until meeting |
| Referral: named | Referred | Lead | Stop for referrer | Enroll referral when the Email Finder returns | Note on new contact |
| Referral: role only | Referred | Lead | Stop for referrer | Lead Database lookup | None |
| Objection: no need | Not interested | Other | Stop | None | None |
| Objection: competitor | Competitor: [name] | Other | Stop; nurture | First nurture touch 6 weeks out, then every 4 to 6 weeks (Berman's nurture cadence), or the renewal date if they gave one | None |
| Objection: price | Objection: budget | Lead | Stop | Re-engage next budget cycle | None |
| Not now / timing | Nurture | Lead | Stop | Task on stated date | None |
| Wrong person | Wrong person | Other | Stop | Ask who owns it | None |
| Left company | Left company | Other | Stop; suppress address | Find replacement | None |
| Unsubscribe | Do not contact | Other | Stop everywhere | Suppress | None |
| Hostile | Do not contact | Other | Stop everywhere | Suppress; person decides reply; threat replies forwarded | None |
| OOO | Paused | Unchanged | Pause to resume date | None | None |
| Hard bounce | Bounced | Other | Stop; suppress | Check list source | None |

## 4. Platform setup notes

Each rule the replies trigger, with the menu path in the two sequencers this skill covers (help centers checked 2026-10-13). A deliverable gives the line for the platform the user named, or both lines when none was named; it never assumes one.

| Rule | Instantly | Smartlead |
|-|-|-|
| Stop on reply, whole company | Campaign, Settings, Advanced settings: "Stop sending emails on reply" on (Basic deliverability) and "Stop Campaign for Company on Reply" on (Sending rules); other leads at the domain are marked Completed | Email Campaigns, the campaign, gear icon, Setup, Campaign Settings: tick "Company Level Auto-Pause" (free mail domains such as gmail.com are excluded) |
| Out of office pauses, then resumes | Campaign, Settings, Advanced settings, Sending rules: "Stop on auto-reply" off; Settings, Preferences, AI Automations: "Automatically tag lead status in replies" on. The lead pauses until the return date ("Pause Until" in Unibox lead info) | Campaign settings, General: "Intelli-categorize replies using Smartlead's AI" with Out-of-Office selected, then "Automatically restart ai-categorized OOO when lead returns", Save General Settings (beta) |
| One suppression list | Settings, Blocklist: block an email address or a whole domain (bare domain, no @) | Settings, Global Block List: an email or a domain; with client sub-accounts, add the entry for each client, because an unassigned entry covers only campaigns with no client |
| AI reply labels | Settings, Preferences, AI Automations (see section 6) | Campaign settings, General, AI categorization (see section 6) |
| Hostile trigger words (section 1b) | No keyword setting in the help center; run the word match in your reply webhook or CRM workflow and set the lead to Do not contact | Same |
| CRM (HubSpot, Pipedrive, GoHighLevel) | One "Outbound status" property with the class values; one "Do not contact" boolean every tool reads | Same |

Lemlist, EmailBison and ManyReach: map their reply labels to the classes above and to one blocklist, from the platform's own docs.

## 5. Daily triage loop

| Time | Action |
|-|-|
| On arrival, business hours | Interested, price and accepted-meeting replies answered within 5 minutes (phone alert) |
| Within 2 to 4 business hours | Referrals logged; objections and not-now answered |
| End of day | Unsubscribes, hostile replies and bounces confirmed in global suppression; referral batch sent to `find_emails` |
| Weekly | Class counts per cell; bounce rate and complaint review |

## 6. Automation boundaries

Sequencers now label replies with AI: a model reads each reply, picks one of the workspace's labels, and the label can change the lead status, stop the sequence or start a subsequence. Two implementations, checked in the vendors' help docs on 2026-10-13:

| Platform | Feature | What the docs say | Confidence score exposed |
|-|-|-|-|
| Instantly | AI Custom Reply Labels | Turned on under Settings, Preferences, AI Automations with "Automatically tag lead status in replies". Interested, Not interested and Out of Office are on by default; custom labels (Hyper Growth and Light Speed plans) are classified from each label's description. A Test AI tab runs a sample reply; thumbs up or down sends feedback. API: `POST /api/v2/lead-labels/ai-reply-label` returns the predicted label. | None in the help article or the API response |
| Smartlead | Intelligent AI Lead Categorization | Turned on per campaign under settings, General; you choose the categories. Up to 5 categories on Pro, up to 10 on Custom (more than 5 needs your own GPT-4 API key); not on Base. | None in the help article |

Neither documents a confidence score, so the threshold has to come from your own layer: the header and keyword rules in section 2, plus your own classifier (an LLM prompt or a CRM workflow) that returns a class and a confidence.

### 6a. Threshold and queue (the user's settings)

No vendor or study publishes a confidence threshold, a queue interval or a sample size for reply labels, so the playbook asks the user for each and states it.

| Rule | Setting |
|-|-|
| Confidence threshold | Automation acts alone only when the class is on the auto list below and either a section 2 header rule matched or your classifier scores at or above the threshold the user sets |
| Vendor label disagrees with your rules | Human queue |
| Human-review queue | Every reply below the threshold or on the never list; the AI label shows as a suggestion only |
| Queue check | At the interval the user sets, with an alert to the reply owner's manager when an item waits longer than the user's limit; hot replies still follow the 5 minute rule |
| Unsure between Unsubscribe and anything else | Suppress first and queue for review |

### 6b. What automation may and may not do

| Class | Automation | Allowed action | Condition |
|-|-|-|-|
| Out of office | Auto | Pause until the return date; the user's pause length if no date | Header or subject rule matched, or confidence at or above the threshold |
| Hard bounce, help desk auto-ack | Auto | Suppress the address | 5.1.x status code or `Auto-Submitted` header |
| Unsubscribe, polite | Auto | Suppress everywhere; R24 removal line only if the user chose to send one | Opt-out words at or above the threshold and no section 1b trigger word; below that, suppress and queue |
| Referral: named | Partial | Run `find_emails` (validated on return; `validate_emails` only for an address the referrer typed); a human sends R10 and approves enrollment | Any confidence |
| Not now with a date | Partial | Set status and the dated task; a human sends R19 | At or above the threshold |
| Interested, non-target account | Partial | Label, alert, AI-drafted reply allowed; a human sends it | Any confidence |
| Interested at a target account | Never | Human only, escalate to the AE (SKILL.md step 3) | Always |
| Hostile (any section 1b trigger word, even inside an unsubscribe) | Never sends | Suppress allowed; any reply is written and sent by a person; threat replies go to the escalation owner the user names | Always |
| Other, unclear, two intents, unfamiliar language | Never | Human queue | Always |
| `5.7.1` reputation block | Never auto-suppress | Pause the sending domain and alert | Always |

### 6c. Weekly misclassification sample

1. Every Monday, pull the number of auto-handled replies the user set from the last 7 days (all of them if fewer), spread across classes.
2. A person labels each one without seeing the AI label.
3. Misclassification rate = disagreements / sample size. Log it per class.
4. Over the error rate the user set for a class: turn off auto for that class, rewrite the label description or category, and re-test with the vendor's test tool (Instantly's Test AI tab) before turning it back on.
5. Any Unsubscribe or Hostile reply labelled as Interested or Out of office, or any automated message sent to a reply containing a section 1b trigger word: turn off automation for that class the same day and check every reply that label touched that week.

## Sources

- https://www.rfc-editor.org/rfc/rfc3834
- https://help.instantly.ai/en/articles/9713093-ooo-resume-ai-smart-pause-for-out-of-office
- https://helpcenter.smartlead.ai/en/articles/51-lead-categories
- https://help.instantly.ai/en/articles/9712488-ai-custom-reply-labels
- https://developer.instantly.ai/api-reference/leadlabel/test-ai-reply-label-prediction
- https://helpcenter.smartlead.ai/en/articles/150-what-is-ai-categorization-and-how-does-it-work-with-smartlead
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/soft-vs-hard-bounce-email
- https://help.instantly.ai/en/articles/9214908-campaign-options
- https://help.instantly.ai/en/articles/6192983-global-blocklist
- https://helpcenter.smartlead.ai/en/articles/199-how-to-set-up-company-level-auto-pause
- https://helpcenter.smartlead.ai/en/articles/209-auto-restart-ooo-based-on-email-copy
- https://helpcenter.smartlead.ai/en/articles/139-what-is-global-block-list-your-comprehensive-cold-outreach-guide
