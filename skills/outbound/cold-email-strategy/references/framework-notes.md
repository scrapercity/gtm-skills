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
| April Dunford, podcast episode 82 on stfo.io (June 3, 2019) | Positioning starts from the competitive alternative | Offer worksheet: current alternative row | Practitioner framework, first-person |
| Jordan Crawford, The Transaction episode 55 (May 16, 2025) | Pain-Qualified Segments built from the situation past buyers were in | Cells from recent won deals | Practitioner interview |
| Craig Elias, Trigger Event Selling | Window of dissatisfaction; first viable vendor wins most often | Trigger column in cells, freshness windows | Practitioner framework citing Forrester |
| Lars Nilsson, SaaStr Annual 2016 transcript; SalesSource post (2020) | Account-based sales development: personas per account, three email arc, use-case library of 10 to 15 per vertical, calls to engaged non-repliers, net-new vs known contact campaigns | Playbook section 8, deal-shape gate | Practitioner talk; Cloudera figures are point in time |
| Google Email sender guidelines | Bulk sender rules: SPF, DKIM, DMARC, alignment, spam rate under 0.1% and never 0.3%, one-click unsubscribe | Capacity guardrails, List and Sender Rules | Mailbox provider policy |
| Yahoo Sender best practices | Spam rate under 0.3%, unsubscribes honored within 2 days | Guardrails | Mailbox provider policy |
| Microsoft Outlook high-volume sender rules (May 5, 2025) | SPF, DKIM, DMARC for 5,000+ daily to consumer Outlook addresses; junk then rejection | Guardrails | Mailbox provider policy, via DMARC Report summary |
| Hunter, State of Email Outreach 2026 | 4.5% average sequence reply rate across 31M emails sent in 2025; three messages 6.8% vs one 3.3%, three the best balance; 21 to 50 recipient sequences 6.2% vs 2.4% over 500 | Default of 3 touches, funnel targets | Vendor dataset |
| Hunter, State of Cold Email 2025 | 4.1% average reply across 11M emails; unsubscribes rise after touch 3 | Touch count ceiling | Vendor dataset |
| Instantly 2026 benchmarks | 3.43% average reply; about 58% of replies from email 1; opens unreliable | Funnel targets | Vendor dataset |
| Postmark on Apple MPP | Opens are logged by proxy preloading | Opens as diagnostic only | Vendor explainer |
| Hunter, Set Up Your Outreach Ops for Scale (December 29, 2023) | 50 a day safe for warmed accounts; 15 or fewer for new senders; fewer than five accounts per domain; 21 sending days a month | Capacity, ramp, domains | Vendor guide from its outreach team |
| Instantly help center, account and campaign limits (checked 2026-10-13) | 30 campaign emails per account per day; Campaign Slow Ramp adds 2 a day up to the limit | Sends per inbox, the ramp, scaling a winner | Vendor documentation |
| Instantly help center, campaign options and high bounce auto-pause (checked 2026-10-13) | Option names for the Sequencer Settings table; bounce auto-pause on by default at 5% after 200 sends, threshold adjustable | Sequencer Settings | Vendor documentation |
| Alex Berman, follow-up guide and templates page (reply handling) | Interested replies within 5 minutes (follow-up guide), 2 to 4 business hours at the outside (templates page); info replies get 2 to 3 sentences, one case study and a proposed time; "not interested" gets one timing-or-fit question; a competitor user is asked what made them choose it | Reply texts in the routing table | Operator teaching |
| Instantly pricing page (checked 2026-10-13) | Growth $47 a month (1,000 uploaded contacts, 5,000 emails); Hypergrowth $97 (25,000 uploaded contacts) | Sending stack cost lines, tier choice | Vendor pricing page |
| Instantly and Smartlead secondary-domain articles; Puzzle Inbox (May 18, 2026); Google Workspace MX, SPF and DKIM pages | Domain naming, inbox addresses, record values for a new sending domain | New sending domain rows | Vendor documentation and a practitioner guide |
| Two-proportion sample size (standard formula) | About 1,530 delivered per variant to separate 1.5% from 3% at 95% confidence and 80% power | Small-volume reads, playbook section 6 | Statistics |
| The user's own figures | Funnel rates (positive per 100, booked, held), trigger windows, deal-value cutoffs for personalization depth, routing SLAs other than Berman's 2 to 4 hours | Gate, back-solve, cells, routing | No published source sets these; the plan lists them as assumptions until measured |

## Routing table

| Question you are answering | Open |
|-|-|
| What did Alex Berman say about X, and where? | `references/alex-berman-cold-email.md` |
| Which email framework fits this cell? | `references/cold-email-frameworks.md` |
| How do I split cells and choose sequence vs cycle mailing? | `references/campaign-architecture-playbook.md` |
| How many inboxes for N contacts, or for a meeting goal? | `references/campaign-architecture-playbook.md` section 4 (capacity, goal back-solve, runway) |
| Who answers which reply, and how fast? | `references/campaign-architecture-playbook.md` section 3 (reply routing) |
| Which sequencer settings, with which values? | `references/campaign-architecture-playbook.md` section 4 (Instantly option names) |
| What happens on which date before launch? | `references/campaign-architecture-playbook.md` section 10 (launch calendar) |
| What test runs first and when do I stop it? | `references/campaign-architecture-playbook.md` (test order, stop rules) |
| How do I write the offer sentence and contact thesis? | `references/offer-and-cell-design.md` |
| Which first line fits this trigger, and does ScraperCity cover it? | `references/offer-and-cell-design.md` section 6 |
| A short list of high-value accounts with several buyers each | `references/campaign-architecture-playbook.md` section 8 (ABSD) |
| When can a contact be emailed again? | `references/campaign-architecture-playbook.md` section 2, the rest rule |
| Only 3 to 4 inboxes: how many cells, and how to judge tests? | `references/campaign-architecture-playbook.md` sections 1 and 6 |
| Adding a phone touch | `references/campaign-architecture-playbook.md` section 9, then `cold-calling` |
| Hiring as a trigger | `references/offer-and-cell-design.md` section 7 |
| Should this campaign run at all? | SKILL.md Prerequisites gate, then `outbound-unit-economics` |
| Which ScraperCity filters build this segment? | `references/offer-and-cell-design.md` (filter recipes) |
| What does a tool cost and what parameters does it take? | `references/scrapercity-catalog.md` |
| Which plan unlocks the databases? | `references/scrapercity-platform.md` |
| What are the Google, Yahoo and Microsoft rules in detail? | `references/deliverability-primer.md` |
| What validation status is safe to send? | `references/list-quality-standard.md` |

## Where sources disagree

| Topic | Disagreement | This skill's rule |
|-|-|-|
| Follow-up count | Berman's follow-up guide: 4 to 6. His TAM breakdown: one per cycle. Hunter 2025: unsubscribes rise after touch 3; Hunter 2026: three messages the best balance. | 3 touches by default, a fourth only when no new contacts are waiting; cycle mailing when validated contacts reach daily capacity x 42 sending days. |
| Re-mail spacing | Berman's TAM breakdown: a new cycle every 30 to 60 days. Earlier drafts of this skill used 60 days for standard sequences and 90 for account-based ones | One rest rule: 60 days after a sequence ends with no reply and between cycle emails; new angle only |
| Sends per inbox | Berman: under 50. Instantly: 30. Hunter: 15 or fewer for new senders, 50 safe once warmed | Plan at Instantly's 30, start new senders at Hunter's 15 or fewer, stay under Berman's 50. |
| Reply benchmarks | 3.43% (Instantly 2026) vs 4.5% (Hunter 2026); both count all replies | Plan on positive replies at the user's own floor and target; no published source sets them; replace with measured rates at the first read. |

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
- https://hunter.io/the-state-of-cold-email-2025
- https://hunter.io/the-state-of-cold-email
- https://hunter.io/cold-email-guide/outreach-ops
- https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- https://help.instantly.ai/en/articles/6222396-campaign-options
- https://instantly.ai/pricing
- https://alexberman.com/cold-email-templates
- https://knowledge.workspace.google.com/admin/security/set-up-spf
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://stfo.io/podcast/april-dunford-product-positioning
- https://thetransactionpod.com/episodes/inverting-your-go-to-market-strategy-thinking-with-jordan-crawford-ep-55/transcript
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- https://www.saastr.com/lars-nilsson-vp-global-inside-sales-cloudera-targeting-the-big-guys-account-based-sales-development-video-transcript/
- https://salessource.com/blog/the-ultimate-absd-tech-stack/
