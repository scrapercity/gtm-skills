# Channel Scripts and Cadences

Cadences by segment, email jobs per touch, call openers, voicemails, front-desk lines, objection answers, LinkedIn limits and notes, direct mail copy, reply branches, confirmations, threading and the daily run order. Every script uses fields ScraperCity returns, so a rep can fill it from the row in front of them. The plan writes every email in full (section 13) using the `cold-email-copywriting` rules; deeper call coaching belongs to `cold-calling`. Every phone touch below runs only on a number that passed the phone check in `references/channel-operating-rules.md`.

## 1. Cadences by segment

### 1a. Tier A local business owner (14 business days)

Adapted from the six-touch, two-week email, call and LinkedIn sequence on alexberman.com, with a mail piece added and LinkedIn dropped where the owner has no profile.

| Day | Channel | Touch | Notes |
|-|-|-|-|
| 1 | Email | Touch 1: one fact from the row (`total_score`, `reviews_count`, `category_name`), one proof line, one question | From `cold-email-copywriting` |
| 2 | Phone | Call 1 to `contact_mobile` or the Mobile Finder number, voicemail V1 | Tuesday to Thursday preferred |
| 3 | Mail | Postcard mailed to `address` (arrives about day 8) | One offer, one number or URL |
| 4 | Email | Touch 2 in thread: a second proof point | |
| 6 | Phone | Call 2 at the other time window, no voicemail | If morning on day 2, late afternoon now |
| 8 | Mail | Postcard arrives | |
| 9 | Email | Touch 3: references the postcard by its headline | |
| 12 | Phone | Call 3, voicemail V3 (breakup) | |
| 14 | Email | Touch 4: breakup, one line | |

### 1b. Tier A B2B title (CFO, controller, VP, director) with a LinkedIn profile

Day 1 is a Tuesday, so every call lands Tuesday to Thursday. Days are business days; times are the recipient's local time. The email send window is the user's setting; test it against reply rates.

| Day | Time | Channel | Touch | Skip or branch |
|-|-|-|-|-|
| 1 (Tue) | Send window | Email | E1 | Email not `valid` or `valid_catch_all`: skip every email row |
| 1 (Tue) | Rep's LinkedIn block | LinkedIn | Profile view (manual) | No LinkedIn URL: skip every LinkedIn row |
| 3 (Thu) | 08:00 to 10:00 | Phone | Call 1, voicemail V1 | No number passed the phone check: skip every call |
| 4 (Fri) | Send window | Email | E2 in thread | Hard bounce on E1: skip the rest of email |
| 5 (Mon) | Rep's LinkedIn block | LinkedIn | Connection request L1 (manual), under 200 characters, no link | Already connected: skip to day 9 |
| 7 (Wed) | 16:00 to 17:00 | Phone | Call 2, no voicemail | Reached on call 1 and asked for email: skip |
| 9 (Fri) | Send window | Email | E3, new proof | Connection accepted: send L2 in LinkedIn on this day instead (accept-skips-email) |
| 11 (Tue) | Rep's LinkedIn block | LinkedIn | Connected and L2 already sent: voice note scripted like V1. Connected after day 9: L2. Not connected and the seat is Sales Navigator: InMail I1 | Not connected on a free or Premium seat: skip |
| 12 (Wed) | 08:00 to 10:00 | Phone | Call 3, voicemail V3 | Spoke on an earlier call: skip the voicemail |
| 14 (Fri) | Send window | Email | E4 breakup | None; last touch |

A second person at the same account (the controller after the CFO, for example) runs the same rows starting day 16, the Tuesday after the first person's last touch, and only if the first person has not replied. Rules in section 11.

### 1c. Tier B (business line, no mobile purchase)

| Day | Channel | Touch |
|-|-|-|
| 1 | Email | Touch 1 |
| 3 | Phone | Business line: front-desk script F1, ask for the contact by name |
| 4 | Email | Touch 2 |
| 7 | LinkedIn | Connection request L1 (manual), B2B titles only |
| 9 | Phone | Business line, F1 again at another time |
| 11 | Email | Touch 3 |
| 15 | Email | Touch 4, breakup |

### 1d. Property owners at a residential address

Mail leads; calls follow the letter and stop at the first "no".

| Day | Channel | Touch |
|-|-|-|
| 1 | Mail | Letter M2 to the owner by name, first-class stamp |
| 10 | Phone | Call 1 if the number passed the phone check, voicemail V-P |
| 14 | Mail | Postcard M1 follow-up |
| 21 | Phone | Call 2, no voicemail |
| 30 | Mail | Final postcard |

### 1e. Engaged-on-email fast lane

A prospect who replies with a question, or replies "not now, but..." without a meeting, moves to a call if a callable number exists. Opens are not a trigger: Apple Mail Privacy Protection preloads images and logs opens that never happened (Postmark, 2021).

### 1f. Timing rules

| Rule | Value | Source |
|-|-|-|
| Call days | Tuesday to Thursday for heavy dialing (Wednesday and Thursday book best); Monday for research, Friday for email | alexberman.com cold calling article |
| Call windows | 08:00 to 10:00 and 16:00 to 17:00 recipient local time; skip 12:00 to 14:00 | Same article |
| Attempts | 3 calls per 14-day cadence | Berman's sequence has three calls; past five attempts with no engagement he moves to fresh names |
| Order on one day | Email first, call after it has gone out | The voicemail can reference an email that has arrived |
| Cohort start day | Tuesday | Puts calls 1 to 3 on Thursday, Wednesday, Wednesday |
| Stop rule | Any reply on any channel stops every channel for that person and their company | Berman's follow-up guide: halt the sequence on a reply |

## 2. Call openers

Structure from Berman's article: name and company, a specific trigger, a permission check, one question. He gives the opener 8 to 10 seconds before the prospect checks out.

Banned opener: "Did I catch you at a bad time?" Gong Labs (90,380 calls, April 2018) found it made a booked meeting about 40% less likely than its baseline, while "the reason for my call is" lifted success 2.1x. Say who you are, then "The reason I'm calling is...". A permission check, if you want one, comes after the reason and asks for 30 seconds.

| Segment | Opener | Fields used |
|-|-|-|
| Local owner with a strong rating | "Hi Maria, this is Dana with Brightline. The reason I'm calling is the note I sent about Lakeline Family Dental's 212 reviews. Can I take 30 seconds on why, and you tell me if it's worth a conversation?" | `contact_first_name`, `title`, `reviews_count` |
| Local owner with few reviews | "Hi Tom, Dana with Brightline. Hill Country Plumbing came up when I searched plumbers in Austin, and you're at 31 reviews against 150-plus for the top three. Quick question: do you ask for reviews after each job today?" | `title`, `city`, `reviews_count` |
| B2B title, hiring trigger | "Hi Priya, Dana with Brightline. I emailed you Tuesday about SDR ramp at Corvane. Is getting new reps to their first meeting faster something you're working on this quarter?" | `first_name`, `company_name` |
| Ecommerce store with an app trigger | "Hi Ava, Dana with Brightline. I saw Lumen Tea added Recharge. Do you have a skip-a-month email running yet?" | Store Leads `apps` |

Rules: say your name and company first; if the person says "don't call me", say "understood, I'll take you off our list", and add the number to the internal do-not-call list before the next dial.

## 3. Voicemails

Berman's structure: under 30 seconds; name and company in about 5 seconds, one reason in about 10, the callback number twice. One reason only, no full pitch.

| Code | Use | Script |
|-|-|-|
| V1 | First call, after touch 1 | "Hi Maria, Dana Ortiz with Brightline. I sent you an email about new-patient forms at Lakeline Family Dental. It's the one with the Round Rock numbers in it. My number is 512-555-0148, again 512-555-0148." |
| V3 | Breakup, last call | "Hi Maria, Dana with Brightline, last call from me on this. If new-patient forms are handled, I'll close the file. If not, the email from Tuesday has everything. 512-555-0148, that's 512-555-0148." |
| V-P | Property owner | "Hi Mr. Alvarez, this is Dana with Cedar Home Buyers, about the property on Elm Street. I mailed you a letter last week. If you've thought about selling, I'm at 214-555-0190, 214-555-0190. If not, tell me and I won't call again." |

## 4. Front desk and business lines

| Code | Situation | Line |
|-|-|-|
| F1 | Reaching the front desk | "Hi, this is Dana with Brightline. Is Maria in today? She's expecting a note from me about the website." Only say "expecting" if an email went out first. |
| F2 | "What's it regarding?" | "I emailed her about the new-patient form on the website. Is there a better time to catch her, or should I leave a message with you?" |
| F3 | "She doesn't take sales calls" | "Thanks for telling me. What's the best email for her, so I stop calling the front desk?" |
| F4 | "Send it to info@" | Thank them, log the address, run it through `validate_emails` before using it |

## 5. Objection answers

Paraphrased from the objection examples in Berman's cold calling article, with a next step for each.

| Objection | Answer pattern | Next step |
|-|-|-|
| "Not interested" | Ask if timing is the issue, or if the topic is off their radar | Timing: set a follow-up date. Fit: close the file |
| "Send me an email" | Ask what the email should cover so they will open it | Send a 3-line email that day referencing their answer |
| "We already use [competitor]" | Ask what works well about it today | Log the competitor; offer one comparison point only if asked |
| "No time" | Ask the one qualifying question now, or ask for a better five minutes this week | Book the time on the call |
| "No budget" | Ask what they spend on the problem today | Price against the current cost, or close the file |
| "What does it cost?" | Answer in one line: the user's public price or range when they publish one, and what moves it (seats, volume, modules), then the 20 minute meeting with two times. No quote, proposal or price sheet by email (Berman's templates page) | Book the meeting; log the price objection if they balk |
| "Take me off your list" | Agree immediately, no pitch | Internal do-not-call list, email blocklist and mail suppression the same day |

## 6. LinkedIn: limits, notes, InMail and who gets LinkedIn touches (manual only)

Connection notes stay under 200 characters so they fit a free seat (Promiseclick, August 2026), sent by the person whose name is on the email.

### 6a. Limits to plan around (checked 2026-10-13)

LinkedIn's help pages refuse automated readers, so the rows below name the page and the dated write-up that read it. Open the LinkedIn page in a browser before you commit to volume.

| Limit | Value | Status and source |
|-|-|-|
| Connection invitations | LinkedIn publishes no number; it restricts accounts that send many invitations in a short time or whose invitations recipients mark as spam. Community estimate about 100 a week on a rolling 7 days | Official wording via Contentin (July 2026); the 100 figure is an estimate (Contentin, Overloop, July 2026) |
| Daily pace | 10 to 25 invitations a day in small batches | Overloop (July 2026) |
| Withdrawn invitation | The same person cannot be invited again for up to 3 weeks | LinkedIn Help as cited by Contentin (July 2026) |
| Pending invitations | No published cap; a large pile of unanswered invitations is a known restriction trigger; withdraw invitations older than 3 to 4 weeks with no response | Overloop (July 2026) |
| Notes on a free account | A small monthly allowance; Contentin and EmailAnalytics read it as three a month in July and September 2026, while Promiseclick (August 2026) found LinkedIn Help pages that conflict | Plan free seats with no notes |
| Note length | 200 characters on free accounts; up to 300 on some Premium surfaces | Promiseclick (August 2026). Plan under 200 so the note fits every seat |
| Sales Navigator InMail | 50 credits a month on Core, Advanced and Advanced Plus | LinkedIn compare-plans page, checked 2026-10-13 |
| InMail credit back | A credit returns when the recipient responds within 90 days | LinkedIn Sales Solutions blog on the InMail policy |

### 6b. Seat plan

| Seat | Notes | Plan |
|-|-|-|
| Free account | A few a month | Send requests without a note; the email carries the message. Spend the free notes on tier A accounts |
| Premium or Sales Navigator (Core $119.99 a month or $1,079.88 a year, LinkedIn compare-plans page checked 2026-10-13) | Personalized notes at volume, inside the invitation limits | Note L1 on every tier A and B request; Sales Navigator also covers one InMail I1 per unconnected tier A contact |

### 6c. Who gets LinkedIn touches, and in what order

Every contact with a LinkedIn URL gets L1. Sales Navigator lead filters (Spotlights) only set the order: Cleverly's July 2026 filter guide lists "Changed jobs in past 90 days", "Posted on LinkedIn in past 30 days" and "Following your company on LinkedIn". Contacts with one of these go first in the day's 10 to 25 requests; everyone else follows inside the same weekly volume.

| Signal | Use |
|-|-|
| Posted in the past 30 days | First in the day's batch. Optional: comment on the post with one specific point and one question, then send L1 one or two business days later, referencing the post |
| Changed jobs in the past 90 days | First in the day's batch; L1 congratulates on the role |
| Follows your company | First in the day's batch; L2 can ask what prompted the follow |
| None of these | L1 in the same week, after the signal contacts |
| No LinkedIn URL | Skip every LinkedIn row for that person |

### 6d. Copy

Branch: when a connection is accepted, the next scheduled email is skipped and L2 goes out in LinkedIn on that email's day (accept-skips-email).

| Code | Use | Note |
|-|-|-|
| L1 | Connection request after email touch 1 | "Hi Priya, I sent you a note about SDR ramp at Corvane. Connecting here as well, I post about outbound for 50 to 200 person SaaS teams." (134 characters) |
| L1-local | Owner with a profile | "Hi Maria, I work with dental practices around Austin on new-patient forms. Would be glad to connect." (100 characters) |
| L2 | Message once connected | "Thanks for connecting, Priya. Is SDR ramp time on your list this quarter, or is it handled?" |
| I1 | InMail when not connected by day 11 (Sales Navigator seat) | Subject "SDR ramp at Corvane". Body: three sentences, the one fact from email 1, one proof line, one question. No attachment, no link |

## 7. Direct mail copy

| Code | Piece | Front | Back |
|-|-|-|-|
| M1 | 6 x 9 postcard to a business | Headline with one number: "26 new-patient forms a month for a 3-chair practice in Round Rock" | Two lines on the result, one call to action (a short URL or a phone number), the sender's name, company and return address |
| M2 | Letter to a tier A owner or property owner | Plain envelope, handwritten-style address, first-class stamp | One page: who you are, why you are writing to this owner, one offer, one way to respond, your signature |

Rules for mail:

- One offer and one response path per piece.
- One piece per trigger or persona (M1p for a public award, M1h for a hiring post), each naming its trigger with the trigger fields; never one letter that says "X, or Y" to cover both.
- The name on the piece comes from the record (`contact_first_name`, owner name from `scrape_property_lookup`); never guess a name.
- Track the piece with its own URL or phone number so replies can be credited to mail.

## 8. Reply and outcome branches, every channel

Every reply, call outcome and LinkedIn event maps to one row. The row says what stops, who answers, how fast, and the text to send. Response times come from Berman: a hot reply within 5 minutes in business hours (follow-up guide), every other human reply within 2 to 4 business hours (templates page); after-hours replies are answered first thing the next business day. A reply that fits two rows takes the higher one in this order: opt-out, angry, bounce, interested, referral, objection, not now, wrong person.

| Reply or outcome | Channel | Action across channels | Owner and SLA | Text to send |
|-|-|-|-|-|
| Interested, asks for a time | Any | Stop prospecting touches for everyone at the company; offer two times | Account rep, 5 minutes | "Glad to. Thursday at 10:00 or Friday at 14:00 Central, 20 minutes? I'll bring the numbers from the email." |
| Accepts a time | Any | Calendar invite within 5 minutes; start the confirmation rows (section 9) | Account rep, 5 minutes | "Booked for Thursday 10:00 Central. Invite on its way. Anyone else who should join, such as whoever runs the process day to day?" |
| Price question | Any | Treat as interested; answer in one line, then offer the call (Berman: no quote or price sheet by email) | Account rep, 5 minutes | "It runs {{price_range}} depending on invoice volume and how many entities you run. Easiest to size on a call: Thursday at 10:00 or Friday at 14:00 Central, 20 minutes?" ({{price_range}} is the user's public range; without one, name only what moves the price) |
| "Send me info" | Any | Treat as interested; stop the cadence | Account rep, 5 minutes | Two or three sentences in the original thread (Berman): the one result that fits their row and a proposed time |
| Forwarded internally ("I've passed this to our controller") | Any | Stop the forwarder; start the named person as a warm thread that names the forwarder in line one | Account rep, 2 to 4 business hours | "Thanks for passing it along. I'll write to Sam directly so it doesn't sit in your inbox." |
| Referral to a named colleague | Any | Stop the referrer; enroll the named person with a first line naming the referrer | Account rep, 2 to 4 business hours | To the referrer: "Thanks, I'll reach out to Sam and mention you sent me." To Sam, line one: "Jordan suggested I get in touch about..." |
| Wrong person or left the company | Any | Stop that person; look up the role holder at the company and enroll them | Account rep, 2 to 4 business hours | No reply to an auto-message. To a human: "Thanks for letting me know. Who runs that now?" |
| Not now, with or without a date | Any | Stop; task on the date given, or the re-contact date the user set | Account rep, 2 to 4 business hours | "Understood. I'll check back the first week of March. Nothing before then." |
| Uses a competitor, happy | Any | Stop; note the vendor and any renewal date | Account rep, 2 to 4 business hours | "Makes sense. If renewal comes up, I can show where we differ in 15 minutes. I won't follow up before then." |
| Not interested | Any | Stop all channels; suppress from every sequence, since the reply promises no follow-up | Account rep, 2 to 4 business hours | "Understood, thanks for telling me. I'll close the file." |
| Opt-out: unsubscribe, "stop", "don't call", "remove me" | Any | Suppress email, phone, LinkedIn and mail the same day; add the number to the internal do-not-call list | Ops, same day | Email: no reply, or "Done, you won't hear from us again." Phone: "Understood, I'll take you off our list." |
| Angry or threatening | Any | Suppress everywhere the same day; a manager decides any reply | Manager, same day | None |
| Out of office | Email | Pause that person until the return date; do not email the delegate named in the message | Sequencer | None |
| Hard bounce | Email | Stop email for that person; calls and LinkedIn continue; one Email Finder lookup for a new address | Ops, immediately (Berman's bounce guide) | None |
| Connection accepted, no message | LinkedIn | Skip the next email; send L2 on that day (accept-skips-email) | Account rep, that day | L2 |
| Reply inside LinkedIn | LinkedIn | Classify with the rows above; answer in LinkedIn | Account rep, same SLA as the row | As the matching row |
| Call: conversation, meeting booked | Phone | Send the invite while still on the call; stop the cadence | Account rep, on the call | "Sending the invite now so it's on your calendar before we hang up." |
| Call: prospect returns a call or a voicemail | Phone | Treat as interested; call back while they are still at their desk | Account rep, 5 minutes (Berman's response time for interest) | "Thanks for calling back. You'd asked about..." then the two times |
| Call: "call me back at 3" | Phone | Book the callback; it counts as one of the 3 calls | Account rep, the time given | None |
| Call: front desk | Phone | Use F1 to F4; log the best time and direct line | Account rep | Section 4 |
| Call: voicemail | Phone | V1 on call 1, none on call 2, V3 on call 3 | Account rep | Section 3 |
| Call: wrong or disconnected number | Phone | Mark the number bad; no more calls to it; email and LinkedIn continue | Account rep, that day | None |
| Asks to text | Any | SMS confirmation from the rep's own number | Account rep, 5 minutes | "Sure. Texting you from 214-555-0137 now. Reply STOP any time." |
| Mail returned undeliverable | Mail | Remove the address; do not re-mail | Ops | None |

## 9. Meeting confirmations

Ryan Reisert's "Buckets" method (GTMnow, November 2021) confirms every booked meeting three times: by phone about a week out, by email 12 to 24 hours before, and by phone 2 to 3 hours before when the email got no reply. In a multichannel plan these are cadence rows owned by the same rep:

| Touch | When | Channel | What it says | Skip when |
|-|-|-|-|-|
| Invite | Within 5 minutes of booking | Calendar invite plus a two-line email | The problem they described, in their words; the agenda in one line | Never |
| Week-out confirmation | About 5 business days before | Phone (callable number), email if no answer | Confirms the time and asks them to bring the operational owner: the person who runs the process day to day, such as the dispatcher, office manager or ops lead | Meeting booked less than a week out: ask about the operational owner on the booking call |
| 24 hours | 12 to 24 hours before | Email in the invite thread | One line: time, link, who is joining from each side | Rescheduled: move it to the new date |
| 2 to 3 hours | Only if the 24 hour email got no reply | Phone; a text only after the prospect asked to text (section 7 of the operating rules) | "Still good for 2pm? I'll have the numbers on your Plano calls ready." | They replied to the 24 hour email |

Why the operational owner: Gong's multithreading guide (checked 2026-10-13) found closed-won deals include 67% more contacts than closed-lost deals. No-shows go back to the Priority bucket until a new time is booked (Reisert).

## 10. Trigger sources for public-sector-adjacent B2B buyers

These sources are not ScraperCity tools. They tell you which companies to move into tier A this week; ScraperCity then finds the people and numbers at those companies (`query_lead_database`, `scrape_website_finder` with `jobTitle`, `find_mobiles`).

| Source (non-ScraperCity) | What it shows | Trigger | First line it supports |
|-|-|-|-|
| USAspending.gov, Advanced Search or the free API at api.usaspending.gov | Federal spending data, including who received federal contracts and grants and from which agency | A new award: the recipient is about to hire, subcontract, buy equipment and take on reporting work | "Saw the new Army Corps award to Ridgeway Civil last week" |
| State DOT bid tabulations (example: TxDOT's Bid Tabulations Dashboard, which shows every bid and TxDOT's estimate for projects let in the past 24 months; also the "Bid Tabulations" dataset on data.texas.gov) | Who bid on each letting and who came in low | The low bidder is about to mobilize; repeat losing bidders feel price pressure | "You came in low on the I-35 frontage job in Hays County" |
| Job postings for a role that signals the pain (company careers pages, job boards) | A company hiring the role your product supports or replaces | Hiring a dispatcher (answering service), an estimator (takeoff software), a safety manager (safety training) | "Saw you're hiring a second dispatcher in Fort Worth" |
| Sales Navigator "Changed jobs in past 90 days" on the buyer title (Cleverly, July 2026) | A new person in the buying seat | New CFO, controller or ops lead at a target account | "Congratulations on the CFO role at Ridgeway Civil" |

Rules: date every trigger; carry the trigger's own fields onto the contact row (`award_agency`, `award_project`, `bid_project`, `posted_role`) and name them in the first line of email 1, the letter and the call reason, one copy code per trigger type, so the email reads "congratulations on the {{award_project}} award from {{award_agency}}", never "the new public work"; read each portal's terms and rate limits before scripting a pull; public-entity buyers themselves (agencies, school districts) often run formal procurement, so sell to the contractors and suppliers around the award unless you know the agency's purchasing rules.

## 11. A second person at one account (threading)

Berman starts with the CEO and goes one level down only when there is no reply in one to two weeks, and warns that emailing several people at one company at once can get you blocked company wide (Lean B2B interview, Single Grain video).

| Rule | Value |
|-|-|
| Order | The senior person (CFO, owner) first; the person who runs the process (controller, ops manager) second |
| Start | The second person starts on day 16, the Tuesday after the first person's last touch, so the threads never overlap |
| Condition | Only if the first person has not replied on any channel |
| Angle | Senior person: cost, risk and the price. Process owner: hours, errors and close time. Never the same email body to both |
| Mention the other thread | The second person's first email may say the rep wrote to the colleague by role ("I wrote to your CFO last month about..."), never quoting or forwarding it |
| Any reply | A reply from either person stops both; the reply row in section 8 decides what happens next |
| Referral inside the account | "Talk to our controller" from the CFO turns the controller thread into a warm thread: stop the cold copy and open with the CFO's name |
| Owner | One rep owns both threads and every channel for the account |

## 12. Daily run order for a rep

Adapted from Ryan Reisert's "Buckets" method (GTMnow, November 2021): work the most valuable task first, from booked meetings backwards to new names.

| Order | Work | Time block (recipient local time for calls) |
|-|-|-|
| 1 | Confirmation calls and emails for booked meetings | Start of day |
| 2 | Replies and callbacks from the day before, in the section 8 SLAs | Before 08:00 local for the first time zone called |
| 3 | Today's cadence calls | 08:00 to 10:00 and 16:00 to 17:00 |
| 4 | Today's LinkedIn tasks: views, requests, messages, voice notes | Midday, 10 to 25 invitations a day |
| 5 | Load tomorrow's new contacts and run the phone check | End of day |

## 13. Email touches inside a multichannel plan

Each email in the plan is written out in full: subject, body, sign-off. A touch that says "see the copywriting skill" cannot be sent. Rules: body under 75 words (Berman's templates page), one question, no link in email 1, merge fields for name and company with a fallback (`{{first_name|there}}`) plus the trigger fields from the trigger row on trigger variants, one copy code per trigger or persona (never "X, or Y" in one body), and no reference to a touch that may not have happened.

| Touch | Job | Mentions another channel only when |
|-|-|-|
| E1 | One fact about their company, one proof line, one question | Never |
| E2 | A second proof point, in the same thread | The voicemail on call 1 was left: "I left you a short voicemail Thursday." |
| E3 | References the letter or postcard by its headline; without mail, a third proof | The mail piece was sent |
| E4 | Breakup: one line, the open question restated, permission to close the file | Never |

## Sources

- Alex Berman, cold calling techniques: https://alexberman.com/cold-calling-techniques
- Roundup on alexberman.com, manual outbound: https://alexberman.com/manual-outbound-beats-ai-cold-email
- Scott D. Clary on Berman's early playbook (HackerNoon, 2021): https://hackernoon.com/cold-email-is-not-dead-mb4v35g4
- Postmark, Apple Mail Privacy Protection and open tracking: https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- Gong Labs, cold call opening lines (April 2018): https://www.gong.io/resources/labs/cold-call-opening-lines/
- Ryan Reisert, Buckets (GTMnow, November 2021): https://gtmnow.com/buckets-lead-generation-method/
- LinkedIn Help, Personalize invitations to connect: https://www.linkedin.com/help/linkedin/answer/a563153
- Contentin, What is a LinkedIn connection request (checked the LinkedIn page July 2026): https://contentin.io/glossary/connection-request/
- EmailAnalytics, LinkedIn connection request templates and limits (checked the LinkedIn page September 2026): https://emailanalytics.com/linkedin-connection-request-message-templates/
- LinkedIn Sales Navigator, compare plans: https://business.linkedin.com/sales-solutions/compare-plans
- USAspending API: https://api.usaspending.gov/
- USAspending.gov: https://www.usaspending.gov/
- TxDOT, Bid Tabulations Dashboard: https://www.txdot.gov/business/road-bridge-maintenance/contract-letting/bid-tabulations-dashboard.html
- Texas Open Data Portal, Bid Tabulations: https://data.texas.gov/dataset/Bid-Tabulations/de7b-7dna
- Contentin, LinkedIn weekly invitation limit (updated July 2026): https://contentin.io/glossary/weekly-invitation-limit/
- Overloop, LinkedIn limits and safety (July 2026): https://overloop.com/blog/linkedin-limits
- Promiseclick, LinkedIn character limits (August 2026): https://www.promiseclick.com/resources/playbooks/linkedin-character-limits
- LinkedIn Sales Solutions, InMail policy change (response within 90 days): https://business.linkedin.com/sales-solutions/blog/l/linkedin-changes-inmail-policy-to-improve-quality-of-messages-and-response-rates
- LinkedIn Help, Understand InMail credits in Sales Navigator: https://www.linkedin.com/help/linkedin/answer/57013
- Cleverly, Sales Navigator filters (July 2026): https://www.cleverly.co/blog/linkedin-sales-navigator-filters
- Gong, The data-backed guide to multi-threading (checked 2026-10-13): https://www.gong.io/resources/guides/the-data-backed-guide-to-multi-threading-and-team-selling
- Alex Berman, cold email follow-up guide: https://alexberman.com/cold-email-follow-up
- Alex Berman, cold email templates: https://alexberman.com/cold-email-templates
- Alex Berman, soft vs hard bounce: https://alexberman.com/soft-vs-hard-bounce-email
- Lean B2B, Alex Berman interview: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
