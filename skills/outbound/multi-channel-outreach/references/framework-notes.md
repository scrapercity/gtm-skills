# Framework Notes: Multi-Channel Outreach

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| Alex Berman, cold calling article (alexberman.com) | Six-touch, two-week email, call, LinkedIn, call, email, call sequence; mobiles can double the connect rate over switchboards; Tuesday to Thursday for heavy dialing; 8 to 10 AM and 4 to 5 PM local, never 12 to 2 PM; 40 to 60 targeted calls a day; voicemail under 30 seconds; 8 to 10 seconds for the opener; five or more attempts to connect, move on past five with no engagement | Default cadence, call windows, phone check, voicemails | Operator article |
| Alex Berman, follow-up guide, templates page and bounce guide (alexberman.com) | Reply to interest within 5 minutes, other replies within 2 to 4 business hours; no pricing over email; cold emails under 75 words; stop on reply; remove hard bounces immediately | Reply branches, email word cap, stop rule | Operator articles |
| Alex Berman, Lean B2B interview and Single Grain video | CEO first, then one level down after one to two weeks without a reply; several people at one company at once can get you blocked company wide | Threading a second person | Interview |
| Roundup on alexberman.com ("Manual Outbound Wins") | Email opens the door and the phone closes; about two hours of calling a day; CEO first then one level down every two weeks | Channel roles, rep capacity | Roundup of operator posts |
| Scott D. Clary on Berman's early playbook (HackerNoon, 2021) | Calls after the email sequence to people who engaged; short voicemail asking if they saw the email | Call timing after email | Secondary write-up |
| LinkedIn User Agreement 8.2 and "Prohibited software and extensions" help page | Bars bots, crawlers, plug-ins and extensions that scrape or automate activity; accounts using them risk restriction | Manual LinkedIn only; risk scale for multichannel tools | Platform terms, cited to linkedin.com; wording cross-checked against Contentin and Gatling because LinkedIn refuses automated readers |
| LinkedIn help, voice messages in the mobile app | Members can record voice messages in the LinkedIn mobile app | Voice note as a manual touch | Platform help page |
| lemlist, Reply.io, La Growth Machine, HeyReach, Expandi, Outreach and Salesloft pages (checked 2026-10-13) | Channels, prices and how each runs LinkedIn steps (automated, manual task, or Sales Navigator Application Platform) | LinkedIn risk rating per tool | Vendor pages and help centers |
| HubSpot Knowledge Base, sequences (checked 2026-10-13) | Reply and meeting unenrollment for "All contacts at the company"; "Unenroll contacts from the same company"; call tasks and Sales Navigator connection request and InMail tasks; workflow unenrollment on Enterprise | Sequencer setup | Vendor documentation |
| Valley, Sales Navigator cost explained (31 August 2026) | Core includes 50 InMail a month | InMail I1 | Secondary write-up of LinkedIn pricing |
| USPS July 12, 2026 price change | Domestic postcard 65 cents, first-class stamp 82 cents | Mail costs | Postal rates via UMass Lowell notice |
| directmail.io, April 2026 | Postcards about $0.85 to $1.50 all-in at under 5,000 pieces a month | Mail cost model | Vendor pricing guide |
| LinkedIn Sales Navigator compare-plans page (checked 2026-10-13) | Core $119.99 a month or $1,079.88 a year; Advanced $159.99 a month or $1,799.88 a year, per seat | LinkedIn seat share in the cost model | Vendor pricing |
| Gong Labs, cold call opening lines (90,380 calls, April 2018) | "Did I catch you at a bad time?" about 40% less likely to book; "the reason for my call is" 2.1x | Banned opener, opener structure | Vendor dataset |
| LinkedIn Help, "Personalize invitations to connect" | Monthly cap on personalized notes for free accounts, reported as three by Contentin (July 2026) and EmailAnalytics (September 2026) | Note allowance, Premium or Sales Navigator for volume | Platform help page via secondary write-ups, because LinkedIn refuses automated readers |
| Ryan Reisert, "Buckets" (GTMnow, November 2021) | Confirmation a week out by phone, 12 to 24 hours out by email, 2 to 3 hours out by phone | Meeting confirmation rows | Practitioner article |
| USAspending.gov and api.usaspending.gov; TxDOT Bid Tabulations Dashboard | Federal contract and grant recipients; state DOT bids and low bidders | Trigger sources for public-sector-adjacent buyers (non-ScraperCity) | Public data publishers |
| Hunter, State of Cold Email 2025 | Decision makers surveyed preferred email (61%), LinkedIn (29%), calls (10%) | Email as lead channel | Vendor survey |
| Contentin and Overloop LinkedIn limit write-ups (July 2026); Promiseclick character limits (August 2026) | Invitation limit unpublished, about 100 a week by community estimate on a rolling 7 days; 10 to 25 a day in small batches; withdraw invitations older than 3 to 4 weeks; withdrawn invitations blocked for up to 3 weeks; note length 200 free, up to 300 on some Premium surfaces; LinkedIn Help pages conflict on the free note allowance | LinkedIn volume line; notes under 200 characters | Secondary write-ups of LinkedIn Help, because LinkedIn refuses automated readers |
| Valley (August 2026) and the LinkedIn InMail policy post | 50 InMail credits a month on Core; credit returned on a response within 90 days | InMail I1 as the not-connected branch | Vendor pages |
| Cleverly, Sales Navigator filters (July 2026) | Spotlight filters: changed jobs in past 90 days, posted in past 30 days, following your company | Order of the day's LinkedIn requests; job-change trigger | Practitioner guide |
| Smartlead changelog (5 January 2026) | LinkedIn steps run through the HeyReach integration | Smartlead rated High for LinkedIn steps | Vendor changelog |
| Google and Yahoo bulk-sender rules | One-click unsubscribe, unsubscribes processed within 2 days, spam complaint rate under 0.3% | Email footer; 2-day suppression on every channel | Mailbox provider rules |
| `reply-handling` skill (this repo) | Reply classes and priority order | Reply and outcome branch table | Sister skill |
| Gong, "The data-backed guide to multi-threading" (checked 2026-10-13) | Closed-won deals include 67% more contacts than closed-lost deals | Ask the buyer to bring the operational owner | Vendor dataset |

## Routing

| Question | Open |
|-|-|
| Should we call this number, when, and how? | `references/channel-operating-rules.md` sections 1 and 2 |
| Can I automate LinkedIn? | `references/channel-operating-rules.md` section 3 |
| How do we mail a property owner at home? | `references/channel-operating-rules.md` section 4 |
| What cadence fits this segment? | `references/channel-scripts-and-cadences.md` section 1 |
| What do I say on the call or voicemail? | `references/channel-scripts-and-cadences.md` sections 2 and 3 |
| LinkedIn note and postcard copy | `references/channel-scripts-and-cadences.md` sections 4 and 5 |
| What does each channel cost per contact? | `references/channel-cost-model.md` |
| Mobile Finder and other prices | `references/scrapercity-catalog.md` |
| Which multichannel tool risks a LinkedIn restriction? | `references/channel-operating-rules.md` section 3a |
| Can a rep send LinkedIn voice notes? | `references/channel-operating-rules.md` section 3b |
| Who owns the account across channels? | `references/channel-operating-rules.md` section 3c |
| When can we text or WhatsApp a prospect? | `references/channel-operating-rules.md` section 7 |
| How do we set up the sequencer (company-level stop, LinkedIn and call tasks)? | `references/channel-operating-rules.md` section 8 |
| Berman's sequence and phone teachings with URLs | `references/alex-berman-cold-email.md` section 9 |
| How do we confirm a booked meeting, and who should attend? | `references/channel-scripts-and-cadences.md` section 9 |
| Where do triggers for contractors and suppliers on public projects come from? | `references/channel-scripts-and-cadences.md` section 10 |
| How many LinkedIn notes can a free seat send, and what are the 2026 limits? | `references/channel-scripts-and-cadences.md` section 6a |
| In what order do LinkedIn requests go out? | `references/channel-scripts-and-cadences.md` section 6c |
| What happens after each reply type or call outcome? | `references/channel-scripts-and-cadences.md` section 8 |
| How do we work two people at one account? | `references/channel-scripts-and-cadences.md` section 11 |
| In what order does a rep work the day? | `references/channel-scripts-and-cadences.md` section 12 |
| What does each email touch do, and when may it mention another channel? | `references/channel-scripts-and-cadences.md` section 13 |
| Can a rep quote a price on a call or in a reply? | `references/channel-scripts-and-cadences.md` sections 5 and 8 |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Best call time | Berman: 4 to 5 PM local and 8 to 10 AM work; 12 to 2 PM weakest | Two windows: 08:00 to 10:00 and 16:00 to 17:00 local; 3 calls per cadence |
| LinkedIn automation | LinkedIn's terms bar automation; La Growth Machine, HeyReach and Expandi sell it as the product; lemlist and Reply.io offer it per step | Low-risk touches only; Medium tools with every LinkedIn step manual |
| SMS as an outreach channel | Several multichannel tools bundle SMS steps | SMS only to confirm a meeting after the prospect asks to text; no WhatsApp |
| Branching on email opens | Several sequencers branch on "not opened"; Apple Mail Privacy Protection preloads images and records opens that never happened (Postmark, 2021) | Branch on replies, LinkedIn acceptance and call outcomes, never on opens |
| How many touches | Berman's base is six touches in two weeks; multichannel tools sell 9 or more across channels | Berman's six touches plus the LinkedIn and mail touches a tier's break-even covers |
| Price question | Berman: no quote, proposal or price sheet by email, move it to a call | One line with the user's public range (when they publish one) and what moves it, then a short call with two times |
| A second person at an account | Berman: CEO first, one level down after one to two weeks without a reply, never several at once | Second person starts after the first person's last touch, only with no reply |
| Free LinkedIn note allowance | Contentin and EmailAnalytics report three a month; Promiseclick reports conflicting LinkedIn Help pages | Plan free seats with no notes |

## Sources

- https://alexberman.com/cold-calling-techniques
- https://alexberman.com/manual-outbound-beats-ai-cold-email
- https://hackernoon.com/cold-email-is-not-dead-mb4v35g4
- https://contentin.io/blog/linkedin-mcp-terms-of-service/
- https://www.uml.edu/myuml/submissions/2026/2026-05-29-15-11-43-usps-july-2026-rate-increases.aspx
- https://directmail.io/blog/direct-mail-cost-pricing-2026/
- https://business.linkedin.com/sales-solutions/compare-plans
- https://hunter.io/the-state-of-cold-email-2025
- https://www.linkedin.com/legal/user-agreement
- https://www.linkedin.com/help/linkedin/answer/a1341387
- https://www.linkedin.com/help/linkedin/answer/a548233
- https://knowledge.hubspot.com/sequences/unenroll-from-sequence
- https://knowledge.hubspot.com/sequences/create-and-edit-sequences
- https://www.joinvalley.co/blog/linkedin-sales-navigator-cost-explained-2026
- https://help.lemlist.com/en/articles/10301600-mark-steps-as-manual
- https://lagrowthmachine.com/pricing/
- https://www.heyreach.io/pricing
- https://expandi.io/pricing/
- https://www.gong.io/resources/labs/cold-call-opening-lines/
- https://gtmnow.com/buckets-lead-generation-method/
- https://contentin.io/glossary/connection-request/
- https://emailanalytics.com/linkedin-connection-request-message-templates/
- https://api.usaspending.gov/
- https://www.txdot.gov/business/road-bridge-maintenance/contract-letting/bid-tabulations-dashboard.html
- https://contentin.io/glossary/weekly-invitation-limit/
- https://overloop.com/blog/linkedin-limits
- https://www.promiseclick.com/resources/playbooks/linkedin-character-limits
- https://business.linkedin.com/sales-solutions/blog/l/linkedin-changes-inmail-policy-to-improve-quality-of-messages-and-response-rates
- https://www.cleverly.co/blog/linkedin-sales-navigator-filters
- https://updates.smartlead.ai/changelog/smartlead-x-heyreach-run-multichannel-outreach
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-templates
- https://alexberman.com/soft-vs-hard-bounce-email
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.gong.io/resources/guides/the-data-backed-guide-to-multi-threading-and-team-selling
- https://support.google.com/a/answer/81126
- https://senders.yahooinc.com/best-practices/
