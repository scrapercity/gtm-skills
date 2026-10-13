# Channel Scripts and Cadences

Cadences by segment, call openers, voicemails, front-desk lines, objection answers, LinkedIn notes and direct mail copy. Every script uses fields ScraperCity returns, so a rep can fill it from the row in front of them. Email copy belongs to `cold-email-copywriting`; deeper call coaching belongs to `cold-calling`. Every phone touch below runs only on a number that passed the gate in `references/channel-compliance-gates.md`.

## 1. Cadences by segment

### 1a. Tier A local business owner (14 business days)

Adapted from the roughly 12 day email, call and LinkedIn sequence on alexberman.com, with a mail piece added and LinkedIn dropped where the owner has no profile.

| Day | Channel | Touch | Notes |
|-|-|-|-|
| 1 | Email | Touch 1: one fact from the row (`total_score`, `reviews_count`, `category_name`), one proof line, one question | From `cold-email-copywriting` |
| 2 | Phone | Call 1 to `contact_mobile` or the Mobile Finder number, voicemail V1 | Tuesday to Thursday preferred |
| 3 | Mail | Postcard mailed to `address` (arrives about day 8) | One offer, one number or URL |
| 4 | Email | Touch 2 in thread: a second proof point | |
| 6 | Phone | Call 2 at the other time window, no voicemail | If morning on day 2, late afternoon now |
| 8 | Mail | Postcard lands | |
| 9 | Email | Touch 3: references the postcard by its headline | |
| 12 | Phone | Call 3, voicemail V3 (breakup) | |
| 14 | Email | Touch 4: breakup, one line | |

### 1b. Tier A B2B title (VP, Head of, Director) with a LinkedIn profile

| Day | Channel | Touch | Notes |
|-|-|-|-|
| 1 | Email | Touch 1 | |
| 1 | LinkedIn | Profile view (manual) | Sender's own profile must match the email signature |
| 2 | Phone | Call 1, voicemail V1 | Mobile only after the gate |
| 3 | LinkedIn | Connection request with note L1 (manual) | Under 200 characters, no link |
| 5 | Phone | Call 2 at a different time, no voicemail | |
| 6 | Email | Touch 2 in thread | |
| 8 | LinkedIn | Message L2 if connected (manual) | One line, one question |
| 10 | Email | Touch 3, new angle (case study or number) | |
| 12 | Phone | Call 3, voicemail V3 | |
| 14 | Email | Touch 4, breakup | |

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

Mail leads; phone only after the full gate (residential numbers are where the DNC rules bite hardest).

| Day | Channel | Touch |
|-|-|-|
| 1 | Mail | Letter M2 to the owner by name, first-class stamp |
| 10 | Phone | Call 1 if the number passed the gate, voicemail V-P |
| 14 | Mail | Postcard M1 follow-up |
| 21 | Phone | Call 2, no voicemail |
| 30 | Mail | Final postcard with opt-out line |

### 1e. Engaged-on-email fast lane

A prospect who replies with a question, or replies "not now, but..." without a meeting, moves to a call within 1 business hour of the reply if a gated number exists. Opens are not a trigger: Apple Mail Privacy Protection preloads images and logs opens that never happened (Postmark, 2021).

### 1f. Timing rules

| Rule | Value | Source |
|-|-|-|
| Call days | Tuesday to Thursday for heavy dialing; Monday for research, Friday for email | alexberman.com cold calling article |
| Call windows | 09:00 to 10:00 and 15:30 to 17:30 recipient local time; skip 12:00 to 14:00 | Same article (late afternoon, early morning, lunch weakest), inside the 09:00 to 20:00 gate |
| Attempts | 3 calls per 14-day cadence; at most 1 a day per person | Florida caps calls at 3 per 24 hours; this skill is stricter |
| Gap between channels on one day | Email first, call at least 2 hours later | The voicemail can reference an email that has arrived |
| Stop rule | Any reply on any channel stops every channel for that person and their company | House standard |

## 2. Call openers

Structure from Berman's article: name and company, a specific trigger, a permission check, one question. Keep the opener under 20 seconds.

| Segment | Opener | Fields used |
|-|-|-|
| Local owner with a strong rating | "Hi Maria, this is Dana with Brightline. I sent you a note about Lakeline Family Dental's 212 reviews. Did I catch you at a bad time? I'll keep it to 30 seconds." | `contact_first_name`, `title`, `reviews_count` |
| Local owner with few reviews | "Hi Tom, Dana with Brightline. Hill Country Plumbing came up when I searched plumbers in Austin, and you're at 31 reviews against 150-plus for the top three. Quick question: do you ask for reviews after each job today?" | `title`, `city`, `reviews_count` |
| B2B title, hiring trigger | "Hi Priya, Dana with Brightline. I emailed you Tuesday about SDR ramp at Corvane. Is getting new reps to their first meeting faster something you're working on this quarter?" | `first_name`, `company_name` |
| Ecommerce store with an app trigger | "Hi Ava, Dana with Brightline. I saw Lumen Tea added Recharge. Do you have a skip-a-month email running yet?" | Store Leads `apps` |

Rules: say your name and company first; never claim a prior relationship that does not exist; if the person says "don't call me", say "understood, I'll take you off our list", and add the number to the internal DNC list before the next dial.

## 3. Voicemails

Berman's structure: under 30 seconds; name and company in about 5 seconds, one reason in about 10, the callback number twice. One reason only, no full pitch.

| Code | Use | Script |
|-|-|-|
| V1 | First call, after touch 1 | "Hi Maria, Dana Ortiz with Brightline. I sent you an email about new-patient forms at Lakeline Family Dental. It's the one with the Round Rock numbers in it. My number is 512-555-0148, again 512-555-0148." |
| V3 | Breakup, last call | "Hi Maria, Dana with Brightline, last call from me on this. If new-patient forms are handled, I'll close the file. If not, the email from Tuesday has everything. 512-555-0148, that's 512-555-0148." |
| V-P | Property owner | "Hi Mr. Alvarez, this is Dana with Cedar Home Buyers, about the property on Elm Street. I mailed you a letter last week. If you've thought about selling, I'm at 214-555-0190, 214-555-0190. If not, tell me and I won't call again." |

Voicemails are left by the live rep on the call. Prerecorded drops and ringless voicemail need prior express consent and are out of this skill (`references/channel-compliance-gates.md` section 3).

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
| "Send me an email" | Ask what the email should cover to be worth opening | Send a 3-line email that day referencing their answer |
| "We already use [competitor]" | Ask what works well about it today | Log the competitor; offer one comparison point only if asked |
| "No time" | Ask the one qualifying question now, or ask for a better five minutes this week | Book the time on the call |
| "No budget" | Ask what they spend on the problem today | Price against the current cost, or close the file |
| "Take me off your list" | Agree immediately, no pitch | Internal DNC, email blocklist and mail suppression the same day |

## 6. LinkedIn notes (manual only)

House standard: connection notes under 200 characters, no link, no pitch, sent by the person whose name is on the email.

| Code | Use | Note |
|-|-|-|
| L1 | Connection request after email touch 1 | "Hi Priya, I sent you a note about SDR ramp at Corvane. Connecting here as well, I post about outbound for 50 to 200 person SaaS teams." (134 characters) |
| L1-local | Owner with a profile | "Hi Maria, I work with dental practices around Austin on new-patient forms. Would be glad to connect." (100 characters) |
| L2 | Message once connected | "Thanks for connecting, Priya. Is SDR ramp time on your list this quarter, or is it handled?" |
| L3 | After a call with no answer | Skip. Three channels in one day reads as pressure |

## 7. Direct mail copy

| Code | Piece | Front | Back |
|-|-|-|-|
| M1 | 6 x 9 postcard to a business | Headline with one number: "26 new-patient forms a month for a 3-chair practice in Round Rock" | Two lines on the result, one call to action (a short URL or a phone number), the sender's name, company, return address, and "Prefer no mail? Call or email and we'll remove you." |
| M2 | Letter to a tier A owner or property owner | Plain envelope, handwritten-style address, first-class stamp | One page: who you are, why you are writing to this owner, one offer, one way to respond, your signature, an opt-out line |

Rules for mail:

- One offer and one response path per piece.
- The name on the piece comes from the record (`contact_first_name`, owner name from `scrape_property_lookup`); never guess a name.
- No fake checks, "final notice" language or envelopes that imitate government mail.
- Residential owners in distress: never name the distress (foreclosure, auction) on the outside of the piece.
- Track the piece with its own URL or phone number so replies can be credited to mail.

## 8. Handoffs between channels

| Event | Action | Owner |
|-|-|-|
| Email reply, positive | Stop all channels; rep replies within 4 business hours | `reply-handling` |
| Email reply, question or "not now" | Fast lane call (section 1e) if a gated number exists | Rep |
| Call connects, meeting booked | Stop email and LinkedIn; send a calendar invite and a one-line confirmation | Rep |
| Call connects, "send info" | Email within 1 hour, in the original thread | Rep |
| LinkedIn connection accepted | Message L2 two days later unless email or phone already engaged | Rep |
| Opt-out on any channel | Suppress email, phone and mail the same day | Ops |
| Mail returned undeliverable | Remove the address; do not re-mail | Ops |

## Sources

- Alex Berman, cold calling techniques: https://alexberman.com/cold-calling-techniques
- Roundup on alexberman.com, manual outbound: https://alexberman.com/manual-outbound-beats-ai-cold-email
- Scott D. Clary on Berman's early playbook (HackerNoon, 2021): https://hackernoon.com/cold-email-is-not-dead-mb4v35g4
- 47 CFR 64.1200 (TCPA rules): https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- Jones Day, Florida telemarketing law changes (2021): https://www.jonesday.com/en/insights/2021/07/florida-makes-significant-changes-to-telemarketing-laws
- Postmark, Apple Mail Privacy Protection and open tracking: https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
