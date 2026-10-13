# Framework Notes: Cold Email Strategy

Which named sources shape this skill, what each one contributes, and which file to open for which decision.

## Authorities and what they contribute

| Authority | Contribution to the plan | Where it shows up | Strength of evidence |
|-|-|-|-|
| Alex Berman (alexberman.com) | 30/30/50 split: targeting, offer, deliverability before copy | Workflow order, diagnosis branch | Operator teaching, self-reported results |
| Alex Berman, "Cold Email Doesn't Fail, Your Offer Does" | Offer = niche + measured result + mechanism; list built after offer | Workflow step 1, offer worksheet | Operator teaching with worked examples |
| Alex Berman, Lean B2B interview | Segment tests of about 100 emails; scoring segments; check market size | Cell sizing, test plan | Interview, first-person account |
| Alex Berman, follow-up guide | 4 to 6 follow-ups over 2 to 3 weeks, each adding something new; stop on reply, unsubscribe, bounce | Touch map defaults | Operator teaching |
| Alex Berman, TAM breakdown on his site | One touch per 30 to 60 day cycle for very large markets | Sequence vs cycle decision | Case study on his site |
| Craig Elias, Trigger Event Selling | Window of dissatisfaction; first viable vendor wins most often | Trigger column in cells, freshness windows | Practitioner framework citing Forrester |
| Google Email sender guidelines | Bulk sender rules: SPF, DKIM, DMARC, alignment, spam rate under 0.1% and never 0.3%, one-click unsubscribe | Capacity guardrails, compliance section | Mailbox provider policy |
| Yahoo Sender best practices | Spam rate under 0.3%, unsubscribes honored within 2 days | Guardrails | Mailbox provider policy |
| Microsoft Outlook high-volume sender rules (May 5, 2025) | SPF, DKIM, DMARC for 5,000+ daily to consumer Outlook addresses; junk then rejection | Guardrails | Mailbox provider policy, via DMARC Report summary |
| FTC CAN-SPAM guide | Truthful headers, postal address, opt-out within 10 business days, no B2B exemption, penalties up to $53,088 per email | Compliance section | US regulator |
| CRTC CASL FAQ | Consent, conspicuous publication implied consent, unsubscribe within 10 business days | Exclusions for Canada | Canadian regulator |
| ICO PECR guidance | Corporate subscribers can be emailed without consent; sole traders cannot | UK cells | UK regulator |
| Hunter, State of Cold Email 2025 | 4.1% average reply across 11M emails; small campaigns reply higher; unsubscribes rise after touch 3 | Funnel targets, touch count | Vendor dataset |
| Instantly 2026 benchmarks | 3.43% average reply; about 58% of replies from email 1; opens unreliable | Funnel targets | Vendor dataset |
| Postmark on Apple MPP | Opens are logged by proxy preloading | Opens as diagnostic only | Vendor explainer |

## Routing table

| Question you are answering | Open |
|-|-|
| What did Alex Berman say about X, and where? | `references/alex-berman-cold-email.md` |
| Which email framework fits this cell? | `references/cold-email-frameworks.md` |
| How do I split cells and choose sequence vs cycle mailing? | `references/campaign-architecture-playbook.md` |
| How many inboxes for N contacts? | `references/campaign-architecture-playbook.md` (capacity tables) |
| What test runs first and when do I stop it? | `references/campaign-architecture-playbook.md` (test order, stop rules) |
| How do I write the offer sentence and contact thesis? | `references/offer-and-cell-design.md` |
| Which ScraperCity filters build this segment? | `references/offer-and-cell-design.md` (filter recipes) |
| What does a tool cost and what parameters does it take? | `references/scrapercity-catalog.md` |
| Which plan unlocks the databases? | `references/scrapercity-platform.md` |
| What are the Google, Yahoo and Microsoft rules in detail? | `references/deliverability-primer.md` |
| Can I email this country or this person? | `references/outbound-compliance-primer.md` |
| What validation status is safe to send? | `references/list-quality-standard.md` |

## Where sources disagree

| Topic | Disagreement | This skill's rule |
|-|-|-|
| Follow-up count | Berman's follow-up guide: 4 to 6. His TAM breakdown: one per cycle. Hunter: unsubscribes rise after touch 3. | 4 touches by default; cycle mailing over 50,000 contacts with deal value under $5,000. |
| Sends per inbox | Berman pages give about 15 per inbox and under 50 per inbox | Plan at 30, start new inboxes at 15, never above 50. |
| Reply benchmarks | 3.43% (Instantly) vs 4.1% (Hunter); both count all replies | Plan on positive replies, start with a 1% positive floor, replace with your data after 500 delivered. |

## Evidence rules

- A benchmark enters the plan with its source and date and is labeled a hypothesis.
- Self-reported operator results are labeled self-reported.
- A claim that cannot be traced to a URL in a `## Sources` list is cut.

## Sources

- https://alexberman.com
- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.insidesales.com/leveraging-trigger-events/
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://dmarcreport.com/blog/microsoft-outlook-dmarc-requirements-may-2025/
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://crtc.gc.ca/eng/com500/faq500.htm
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/
- https://hunter.io/the-state-of-cold-email-2025
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
