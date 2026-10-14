# Channel Operating Rules

Checks to run before a contact enters a phone, LinkedIn, mail or text touch. Each rule states the result it protects: replies, pickups, inbox placement, account restrictions or list health.

## 1. Phone check, per number

Run per number, in order. Stop at the first "drop".

| Step | Question | If yes | If no | Reason |
|-|-|-|-|-|
| 1 | Is the number on your internal do-not-call list, or has the contact opted out on any channel? | Drop | Go to 2 | Remove anyone who asked to be removed the same day, in every tool |
| 2 | Has this person had 3 calls this cadence? | Stop | Go to 3 | Three calls is Berman's sequence; past five attempts with no engagement, he spends the time on fresh names |
| 3 | Is the recipient's local time inside Berman's windows, 08:00 to 10:00 or 16:00 to 17:00, and not 12:00 to 14:00? | Go to 4 | Reschedule | Berman: late afternoon local time shows better pickup rates, early morning works, lunch is weakest |
| 4 | Is the caller ID the rep dials from labeled spam on carrier apps? | Swap or fix the number first | Call | Pickups collapse once a number is labeled |

Heavy dial blocks run Tuesday to Thursday; Wednesday and Thursday book the most meetings, Monday is for research and Friday for email follow-ups (alexberman.com cold calling article). The opener says the rep's name and company first: Berman gives a prospect 8 to 10 seconds before they check out.

## 2. Caller ID numbers

| Check | Rule |
|-|-|
| Label | Look up each rep's number on the carrier spam-label apps before a dial block and after any drop in pickups |
| Labeled | Swap the number or have it fixed before the next block; pickups collapse while the label shows |
| Name | The caller name matches the rep who owns the account (section 3c) |

## 3. LinkedIn account restrictions

LinkedIn's User Agreement (section 8.2) and its help page "Prohibited software and extensions" bar third-party software, including bots, browser plug-ins and extensions, that scrapes LinkedIn or automates activity on it, and LinkedIn may restrict accounts that use it. A restricted seat loses every connection request in flight, so this skill plans manual activity only. LinkedIn's pages refuse automated readers; on 2026-10-13 this summary was matched against two write-ups of the same pages (Contentin and Gatling, 2026). Open the pages in a browser before relying on the wording.

| Check | Rule | Source |
|-|-|-|
| All views, connection requests, messages and voice notes are sent by the rep in LinkedIn's own web or mobile app | No bots or automated methods on the site | LinkedIn User Agreement 8.2; "Prohibited software and extensions" |
| No browser extension or cloud tool performs LinkedIn actions on the account | Extensions and third-party software that automate activity are named on the prohibited software page | Same |
| A sequencer's LinkedIn step is a task reminder only: the tool creates the task, the rep does the action | Keeps the action manual | Tool risk table, section 3a |
| Connection volume stays under the community estimate of about 100 per seat per rolling 7 days, sent 10 to 25 a day in small batches; invitations older than 3 to 4 weeks with no response are withdrawn | LinkedIn keeps its invitation limit unpublished and restricts accounts that send many invitations quickly or get marked as spam; a large pending pile is a known restriction trigger; a withdrawn invitation cannot be resent to that person for up to 3 weeks | Contentin glossary and Overloop, July 2026 (secondary) |
| InMail only from a Sales Navigator seat, one per person per cadence | Core includes 50 InMail credits a month; a credit returns when the recipient responds within 90 days | Valley (31 August 2026); LinkedIn Sales Solutions blog |
| Personalized notes fit the seat's allowance | Free accounts get a small monthly allowance of invitations with a note (three a month per July and September 2026 write-ups of LinkedIn Help); Premium or Sales Navigator for notes at volume, or send without a note | LinkedIn Help, "Personalize invitations to connect" (via Contentin and EmailAnalytics) |
| Stop on reply anywhere | One stop rule across channels | Berman's follow-up guide: halt the sequence on a reply |

### 3a. Multichannel tools and their LinkedIn account risk

Risk rating (this skill's scale, read against LinkedIn's terms above):

- **Low**: the tool never acts on LinkedIn. It creates a task and the rep acts in LinkedIn, or it connects through LinkedIn's Sales Navigator Application Platform.
- **Medium**: the tool can automate LinkedIn actions but lets each LinkedIn step be set to manual. Low only if every LinkedIn step is manual.
- **High**: automated LinkedIn actions run by the vendor on your account are the product.

| Tool | Channels (vendor page, 2026-10-13) | How LinkedIn steps run (vendor page or help center) | Price (2026-10-13) | LinkedIn risk |
|-|-|-|-|-|
| lemlist Multichannel | Email; LinkedIn visits, invites, messages, voice messages, InMail; calls with a power dialer; SMS; WhatsApp as an add-on | lemlist sends LinkedIn steps unless the step is marked manual before launch; a manual step creates a task; lemlist's help article does not say whether the rep then acts in LinkedIn itself or through lemlist's extension | $109 per user a month, $87 billed yearly | Medium; Low only if reps complete every LinkedIn task by hand inside LinkedIn |
| Reply.io Multichannel | Email, LinkedIn, calls and SMS, semi-automated WhatsApp | LinkedIn steps "can be either manual or automatic" | $99 per user a month, $89 billed annually | Medium; Low with manual LinkedIn steps only |
| Smartlead | Email; LinkedIn steps in the same sequence | LinkedIn steps run through the HeyReach integration, with non-responders moved into email follow-ups automatically (changelog, 5 January 2026) | Base $39, Pro $94 a month ($32 and $78 billed yearly) | High for LinkedIn steps; use it for email only and do LinkedIn by hand |
| La Growth Machine | LinkedIn and email on every plan, LinkedIn voice messages, calls on Pro, X on Ultimate | "100% cloud-based (no detectable extensions)" with dedicated mobile proxies | Basic €60, Pro €120 per identity a month | High |
| HeyReach | LinkedIn: connection requests, messages, follow-ups, voice notes, profile views, per sender | Automated actions with a residential proxy per sender on Growth | $79 per sender a month, $63 billed yearly | High |
| Expandi | LinkedIn connection requests, messages, InMails, event invites; email follow-ups | "Cloud-based software" with a dedicated country IP | Business $99 a month, $79 billed annually | High |
| Outreach | Email, calls, LinkedIn tasks | The rep completes LinkedIn tasks (view profile, connection request, message) in LinkedIn by hand | "Request pricing" | Low |
| Salesloft | Email, calls, LinkedIn steps | Integrates with Sales Navigator "as a member of the Sales Navigator Application Platform" | Not published | Low |

Plans built with this skill use Low-risk LinkedIn touches only. A team that picks a Medium tool sets every LinkedIn step to manual before launch. This skill does not plan touches for High-risk tools; a team that runs one anyway accepts the account restriction risk LinkedIn's terms describe.

### 3b. LinkedIn voice notes (manual touch)

LinkedIn lets members record voice messages in its mobile app (LinkedIn help: "Recording Voice Messages Sent on the LinkedIn Mobile App"). In a cadence this is a manual touch:

| Rule | Value |
|-|-|
| Who | The rep who owns the account (section 3c), from their own profile, in the LinkedIn mobile app |
| When | Only after the connection request is accepted; skip the touch if it is not |
| Script | Like voicemail V1: name and company, one reason, the question from the last email; under 30 seconds, Berman's voicemail length |
| Never | Audio pushed by a tool: that is the automation LinkedIn's terms bar (section 3) |

### 3c. One rep owns every channel for an account

| Rule | Why |
|-|-|
| One named rep per account: the sending mailbox carries the rep's name, the rep makes the calls, the LinkedIn touches come from the rep's profile, the mail piece is signed by the rep, any text comes from the rep's own number | A reply on any channel reaches the person who can stop the other channels |
| Replies on any channel route to that rep | The stop rule depends on one person seeing every reply |
| CRM account owner = sequencer sender identity = LinkedIn profile = caller name | Reporting by channel stays tied to one owner |

## 4. Direct mail

| Check | Rule |
|-|-|
| Address is a business address (Local Business Database `address`, Maps listing, company HQ) | Mail it; anyone who asks to stop joins the suppression list the same day |
| Address is a residence (property owners from `scrape_property_lookup` or `scrape_distress_list`) | Mail the owner by the name on the record |
| Contact opted out on email or phone | Do not mail: one opt-out covers every channel |
| Mail piece names a person | Use the name from the record; do not guess |

## 5. Email inside a multichannel cadence

Email touches carry a one-click unsubscribe. Google's and Yahoo's bulk-sender rules ask for one-click unsubscribe, processing within 2 days and a spam complaint rate under 0.3%, and inbox placement depends on them; this skill removes every unsubscribe the same day, on every channel. An email unsubscribe stops calls, LinkedIn and mail as well.

## 6. Suppression record per contact

| Field | Example |
|-|-|
| Contact | Tom Reyes, Reyes Air, Plano TX |
| Number type | Mobile (Mobile Finder) |
| Internal do-not-call list | Clear, checked 2026-10-13 |
| Opt-outs on any channel | None |
| Caller ID | 214-555-0137, no spam label (checked 2026-10-13) |
| Window | 08:00 to 10:00 and 16:00 to 17:00 Central |
| Calls this cadence | 0 |
| Result | Callable |

## 7. SMS and WhatsApp

Neither is a first touch. SMS confirms or moves a meeting after the prospect asks to text; plans built with this skill do not use WhatsApp. "STOP" or any opt-out wording ends texts and every other channel the same day.

Cell to write in a cadence row: "After the prospect asks to text: S1 confirmation, then one reminder the day before".

## 8. Sequencer setup (HubSpot sequences as the documented case)

Write the setup for the user's own sequencer. When the user names none, write it for HubSpot sequences, whose settings are documented below, and name the three settings to look for in any other tool: a company-level stop on reply, LinkedIn and call steps as manual tasks, and an end to the sequence when a call reaches a conversation.

| Plan rule | HubSpot setting (knowledge base, checked 2026-10-13) |
|-|-|
| A reply from anyone at the company stops everyone there | Sequence settings: the reply and meeting switches set to "All contacts at the company" (the dropdown offers "The contact" or "All contacts at the company"), plus "Unenroll contacts from the same company" |
| A booked meeting stops the cadence | The meeting switch: "When a contact books a meeting", unenroll |
| LinkedIn rows stay manual | "Sales Navigator - Connection request task" and "Sales Navigator - InMail task" steps (they need HubSpot's Sales Navigator integration); profile views and voice notes as a "General task". The rep completes each one in LinkedIn |
| Calls as cadence rows | "Call task" steps on the call days |
| A call that reaches a conversation ends the sequence | The rep unenrolls the contact while logging the call; Sales Hub or Service Hub Enterprise can unenroll through a workflow instead |
| Opt-out and bounce | HubSpot unenrolls on its unsubscribe link and on a bounce; the rep adds call and LinkedIn opt-outs to the same suppression list by hand |

## Sources

- Alex Berman, cold calling techniques: https://alexberman.com/cold-calling-techniques
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo, Sender best practices: https://senders.yahooinc.com/best-practices/
- LinkedIn, User Agreement (section 8.2): https://www.linkedin.com/legal/user-agreement
- LinkedIn Help, Prohibited software and extensions: https://www.linkedin.com/help/linkedin/answer/a1341387
- LinkedIn Help, Automated activity on LinkedIn: https://www.linkedin.com/help/linkedin/answer/a1340567
- LinkedIn Help, Recording voice messages sent on the LinkedIn mobile app: https://www.linkedin.com/help/linkedin/answer/a548233
- LinkedIn Help, Personalize invitations to connect: https://www.linkedin.com/help/linkedin/answer/a563153
- LinkedIn Sales Navigator, compare plans (checked 2026-10-13): https://business.linkedin.com/sales-solutions/compare-plans
- LinkedIn Sales Solutions, InMail policy change: https://business.linkedin.com/sales-solutions/blog/l/linkedin-changes-inmail-policy-to-improve-quality-of-messages-and-response-rates
- Contentin, LinkedIn and automation terms: https://contentin.io/blog/linkedin-mcp-terms-of-service/
- Contentin, Weekly invitation limit: https://contentin.io/glossary/weekly-invitation-limit/
- Contentin, Connection request: https://contentin.io/glossary/connection-request/
- EmailAnalytics, LinkedIn connection request templates and limits: https://emailanalytics.com/linkedin-connection-request-message-templates/
- Overloop, LinkedIn limits and safety (July 2026): https://overloop.com/blog/linkedin-limits
- Gatling, LinkedIn automation rules (secondary summary of LinkedIn's pages): https://gatling.chat/blog/linkedin-automation-rules
- lemlist, Pricing (checked 2026-10-13): https://www.lemlist.com/pricing
- lemlist Help, Mark steps as manual: https://help.lemlist.com/en/articles/10301600-mark-steps-as-manual
- Reply.io, Pricing (checked 2026-10-13): https://reply.io/pricing/
- Reply.io Help, LinkedIn step in a sequence: https://support.reply.io/en/articles/4318890-linkedin-step-in-a-sequence-manual-connections
- Smartlead changelog, Smartlead x HeyReach (5 January 2026): https://updates.smartlead.ai/changelog/smartlead-x-heyreach-run-multichannel-outreach
- Smartlead, Pricing (checked 2026-10-13): https://www.smartlead.ai/pricing
- La Growth Machine, Pricing (checked 2026-10-13): https://lagrowthmachine.com/pricing/
- HeyReach, Pricing (checked 2026-10-13): https://www.heyreach.io/pricing
- Expandi, Pricing (checked 2026-10-13): https://expandi.io/pricing/
- Outreach Support, How to manage Outreach LinkedIn tasks: https://support.outreach.io/hc/en-us/articles/360008328033-How-To-Manage-Outreach-LinkedIn-Tasks
- Salesloft, LinkedIn Sales Navigator with Salesloft: https://salesloft.com/linkedin
- HubSpot Knowledge Base, Unenroll contacts from a sequence (checked 2026-10-13): https://knowledge.hubspot.com/sequences/unenroll-from-sequence
- HubSpot Knowledge Base, Create and edit sequences (checked 2026-10-13): https://knowledge.hubspot.com/sequences/create-and-edit-sequences
- Valley, LinkedIn Sales Navigator cost explained (31 August 2026): https://www.joinvalley.co/blog/linkedin-sales-navigator-cost-explained-2026
