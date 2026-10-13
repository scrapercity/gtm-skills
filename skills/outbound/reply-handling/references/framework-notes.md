# Framework Notes: Reply Handling

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| Alex Berman, follow-up guide | Responses for info requests, not interested, later, price, competitor; respond fast; stop on reply, unsubscribe, hard bounce | Response library, stop rules | Operator teaching |
| Alex Berman, templates page | 2 to 4 business hour reply window; no pricing, proposals or PDFs by email | SLAs, response rules | Operator teaching |
| Alex Berman, Lean B2B interview | Ask "not interested" for feedback; "already have a vendor" signals a buying market | Objection handling, weekly review | Interview |
| RFC 3834 (IETF) | `Auto-Submitted` header values; do not answer automatic messages or null return paths; one away reply per sender per several days | Auto-reply detection | Internet standard |
| FTC CAN-SPAM guide | Opt-out honored within 10 business days, no B2B exemption, up to $53,088 per email | Suppression | US regulator |
| Yahoo sender best practices | Unsubscribes within 2 days; spam rate under 0.3% | Suppression deadline | Mailbox provider |
| Google sender guidelines | Spam rate under 0.1%, never 0.3%; unsubscribe within 48 hours | Suppression, angry-reply review | Mailbox provider |
| CRTC CASL FAQ | Unsubscribe within 10 business days; sender identification | Canadian contacts | Canadian regulator |
| ICO PECR guidance | Keep a "do not email" list for corporate subscribers who object and screen new lists against it | UK suppression | UK regulator |
| Hunter, State of Cold Email 2025 | Referral requests were the most effective follow-up type in its data | Referral emphasis | Vendor dataset |
| Instantly help center (OOO resume) | Platform pauses OOO leads until the stated return date when stop-on-auto-reply is off | OOO handling | Vendor documentation |
| Smartlead help center | Lead categories assigned in the master inbox can trigger subsequences | Platform setup | Vendor documentation |

## Routing

| Question | Open |
|-|-|
| Which class is this reply? | `references/reply-taxonomy-and-routing.md` section 1 |
| Is this an auto-reply or bounce? | `references/reply-taxonomy-and-routing.md` section 2 |
| What status do I set in Instantly, Smartlead or the CRM? | `references/reply-taxonomy-and-routing.md` sections 3 and 4 |
| What do I write back? | `references/response-library.md` |
| How fast must I suppress, and what scope? | `references/suppression-and-compliance.md` |
| What exactly did Berman say about replies? | `references/alex-berman-cold-email.md` section 6 |
| `find_emails` parameters and price | `references/scrapercity-catalog.md` |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Reply speed | Berman templates page 2 to 4 hours; his follow-up guide says minutes when possible | 1 hour target, 2 hour limit for interested |
| Unsubscribe deadline | CAN-SPAM and CASL 10 business days; Yahoo 2 days; Google 48 hours | 1 business day internal rule, so every limit is met |
| Not interested | Berman: acknowledge and remove; optionally ask once for feedback | One feedback question at most, never a second pitch |

## Sources

- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-templates
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.rfc-editor.org/rfc/rfc3834
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://senders.yahooinc.com/best-practices/
- https://support.google.com/a/answer/14229414
- https://crtc.gc.ca/eng/com500/faq500.htm
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/
- https://hunter.io/the-state-of-cold-email-2025
- https://help.instantly.ai/en/articles/9713093-ooo-resume-ai-smart-pause-for-out-of-office
- https://helpcenter.smartlead.ai/en/articles/51-lead-categories
