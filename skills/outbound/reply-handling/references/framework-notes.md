# Framework Notes: Reply Handling

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| Alex Berman, follow-up guide | Responses for info requests (2 to 3 sentence summary), not interested, later, price (no pricing in email), competitor (a sign they are in the market); calendar invite sent immediately after they agree; nurture every 4 to 6 weeks; reply to interest within 5 minutes; stop on reply, unsubscribe, hard bounce; unsubscribes above 0.5% of prospects flag the follow-ups | Hot-reply SLA, response library, stop rules, weekly review | Operator teaching |
| Alex Berman, templates page | Respond within 2 to 4 hours in business hours; no case studies, proposals or pricing by email; price reply "Pricing depends on [Variable 1] and [Variable 2]" plus a 15 minute walkthrough; cold emails under 75 words, subjects under 50 characters | SLA for non-hot replies, response rules, word cap | Operator teaching |
| Alex Berman, soft vs hard bounce guide | Remove hard bounces immediately; platforms retry soft bounces over 24 to 72 hours; two or three consecutive mailbox-full bounces count as hard; 5.7.1 is a reputation problem; bounces under 2% | Auto-reply detection, suppression | Operator teaching |
| Alex Berman, Lean B2B interview | "Already have a vendor" signals a buying market; he also suggests asking "not interested" replies for feedback, which this skill moves to the weekly class review | Objection handling, weekly review | Interview |
| RFC 3834 (IETF) | `Auto-Submitted` header values; do not answer automatic messages or null return paths; one away reply per sender per several days | Auto-reply detection | Internet standard |
| Yahoo sender best practices | Unsubscribes within 2 days; spam rate under 0.3% | Suppression deadline | Mailbox provider |
| Google sender guidelines | Spam rate under 0.1%, never 0.3%; unsubscribe within 48 hours | Suppression, hostile-reply review | Mailbox provider |
| Hunter, State of Cold Email 2025 | Referral requests were the most effective follow-up type in its data | Referral emphasis | Vendor dataset |
| Instantly help center (OOO resume) | Platform pauses OOO leads until the stated return date when stop-on-auto-reply is off | OOO handling | Vendor documentation |
| Smartlead help center | Lead categories assigned in the master inbox can trigger subsequences | Platform setup | Vendor documentation |
| Instantly help center, AI Custom Reply Labels, and API docs (checked 2026-10-13) | AI applies reply labels automatically when enabled; default labels Interested, Not interested, Out of Office; test tool; no confidence score documented | Automation boundaries | Vendor documentation |
| Smartlead help center, AI categorization (checked 2026-10-13) | Per-campaign AI lead categorization; category limits by plan; no confidence score documented | Automation boundaries | Vendor documentation |
| Instantly and Smartlead help centers, campaign settings (checked 2026-10-13) | Company-level stop on reply, OOO pause and restart, global blocklist menu paths | Platform setting lines | Vendor documentation |
| Toast, restaurant opening hours (June 2026) | Peak hours 11am to 2pm and 5pm to 8pm (quick service), 5pm to 10pm (casual dining) | Proposed meeting times for restaurants | Industry publication |
| Ryan Reisert, "Buckets" (GTMnow, Nov 2021) | Confirmation a week out by phone, 12 to 24 hours by email, 2 to 3 hours by phone; no-shows return to Priority | Confirmation and no-show copy | Practitioner article |
| The user's settings (no published source) | Escalation owners and time limits, AI-label confidence threshold, review-queue interval, weekly sample size and error rate, OOO pause with no return date. The playbook asks for each and states it | SLAs, automation boundaries | User input |

## Routing

| Question | Open |
|-|-|
| Which class is this reply? | `references/reply-taxonomy-and-routing.md` section 1 |
| Does this reply need a person (spam, report, lawyer, data request)? | `references/reply-taxonomy-and-routing.md` section 1b |
| The user pasted several replies | `SKILL.md` Output Format A, `templates/triage-template.md` and `examples/triage-example.md` |
| What do I send someone a referrer named? | `references/response-library.md` R11 |
| Ready lines for too expensive, bundled tool, in-house | `references/response-library.md` R34, R35, R27 |
| Is this an auto-reply or bounce? | `references/reply-taxonomy-and-routing.md` section 2 |
| What status do I set in Instantly, Smartlead or the CRM? | `references/reply-taxonomy-and-routing.md` sections 3 and 4 |
| What do I write back? | `references/response-library.md` |
| Which replies can AI labels handle alone? | `references/reply-taxonomy-and-routing.md` section 6 |
| Who gets escalated, and how fast? | `SKILL.md` workflow step 3 |
| How do I confirm a booked meeting or chase a no-show? | `references/response-library.md` section 12 |
| How fast must I suppress, and what scope? | `references/suppression-and-compliance.md` |
| What exactly did Berman say about replies? | `references/alex-berman-cold-email.md` section 6 |
| `find_emails` parameters and price | `references/scrapercity-catalog.md` |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Reply speed | Berman templates page 2 to 4 hours; his follow-up guide says within 5 minutes | 5 minutes in business hours for every hot reply, any account tier; 2 to 4 business hours for other human replies |
| Unsubscribe speed | Yahoo 2 days; Google 48 hours; Berman "immediately" | The same day, in every tool, hostile replies included |
| Price question | Berman: no pricing over email, move it to a call; his template names what the price depends on | R6 answers what the price depends on, then a 15 minute walkthrough with two times |
| Not interested | Berman: acknowledge and remove; optionally ask once for feedback | Accept and stop in one or two lines with no question; a feedback question right after "I won't follow up" contradicts the promise |
| Draft variables | Template libraries often use bracketed slots | No brackets in any draft; only name and company merge fields with fallbacks; facts only from the user's brief |
| Confirming an opt-out | Suppression is what stops the next email | Polite opt-out: automation may send R24 if the user chose to. Hostile opt-out: a person sends R26 or nothing. The Send column states which, in one word |
| Referral first email | A forwarded original with "see below" | New thread, subject names the referrer, one industry-specific reason, one proof, one ask |

## Sources

- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-templates
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.rfc-editor.org/rfc/rfc3834
- https://senders.yahooinc.com/best-practices/
- https://support.google.com/a/answer/14229414
- https://hunter.io/the-state-of-cold-email-2025
- https://help.instantly.ai/en/articles/9713093-ooo-resume-ai-smart-pause-for-out-of-office
- https://helpcenter.smartlead.ai/en/articles/51-lead-categories
- https://help.instantly.ai/en/articles/9712488-ai-custom-reply-labels
- https://helpcenter.smartlead.ai/en/articles/150-what-is-ai-categorization-and-how-does-it-work-with-smartlead
- https://gtmnow.com/buckets-lead-generation-method/
- https://alexberman.com/soft-vs-hard-bounce-email
- https://help.instantly.ai/en/articles/9214908-campaign-options
- https://help.instantly.ai/en/articles/6192983-global-blocklist
- https://helpcenter.smartlead.ai/en/articles/199-how-to-set-up-company-level-auto-pause
- https://helpcenter.smartlead.ai/en/articles/209-auto-restart-ooo-based-on-email-copy
- https://helpcenter.smartlead.ai/en/articles/139-what-is-global-block-list-your-comprehensive-cold-outreach-guide
- https://pos.toasttab.com/ca/blog/on-the-line/best-opening-hours-for-different-types-of-restaurants
