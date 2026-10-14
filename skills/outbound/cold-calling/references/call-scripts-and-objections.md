# Call Scripts and Objections

Original scripts built on the opener, reason, question, ask structure. Every script uses fields ScraperCity returns, so the reason for the call is a fact the rep can see on screen: `total_score` and `reviews_count` from the Local Business Database, Maps or Yelp; title, company size and industry from the Lead Database; platform and apps from Store Leads; a domain from Tech Stack Search (`scrape_builtwith`). Edit the bracketed parts; never invent a client result.

Rules for every script:

- Sell only the offer the user named. The stake, reason, voicemails and emails stay inside it; a product the user did not mention appears nowhere.
- Write with merge fields from the list columns ({owner_first}, {business}, {rating}, {review_count}, {city}, {trigger_date}, {slot_1}, {slot_2}), not a sample record. The examples below use one record to show the shape; the plan converts them to fields.
- The first sentence says who you are and where you are from (Blount: identify yourself and why you are calling). Berman gives the opener 8 to 10 seconds before the prospect checks out.
- No "did I catch you at a bad time?" (Gong Labs measured about 40% fewer meetings).
- One reason, one question, one ask. Stop talking after each question (Blount).
- The ask names a time.
- Any "don't call me again" ends the call and goes to the internal do-not-call list the same day.

## 0. Pre-call research: 3x3

Three insights in three minutes, written down before the dial. The method is Steve Richard's (co-founder of Vorsight, later ExecVision): his X account promoted a Call Camp on "3x3 Research" on 26 April 2016, and his 2021 LinkedIn post shared "3x3 Research in 10 slides" from ExecVision. SalesIntel's November 2021 blog says it coined the term; Richard's 2016 post is earlier, so this skill credits him. The split into account, person and why now is this skill's adaptation.

| Insight | Question it answers | Where it comes from in under a minute | Example |
|-|-|-|-|
| Account | What is true about this company that ties to the problem? | Lead Database industry and size; Local Business Database `total_score`, `reviews_count`; Store Leads platform and apps; Tech Stack Search domain list | Reyes Air: 4.8 stars, 41 reviews; three Plano competitors above 300 |
| Person | Why does this person own it? | Title, seniority, LinkedIn headline, named contact on the listing | Luis Reyes is owner and runs dispatch |
| Why now | Why call this week? | New listing, hiring post, tech change, season, funding, a review spike | Peak AC season ends in about 6 weeks |

Rules:

- Three minutes is a cap. When no why-now turns up, use the account fact as the reason and dial.
- On owner-operated local lists the account fields arrive with the record, so the account line takes less time.
- Research the next block's records in the admin slot, never inside a calling block (Golden Hours, `references/call-blocks-and-metrics.md` section 4a).
- Write the three lines into the call notes block (section 7) before dialing. Tom Slocum's SD Lab argues for relevance over personal detail: an insight earns a place only if it explains why the problem applies to this account.

## 1. Openers

| ID | Opener | When | Basis |
|-|-|-|-|
| O1 | "Hi Dana, this is Sam with Northline. The reason I'm calling is..." | Default for every motion | Gong 2018: stating the reason 2.1x |
| O2 | "Hi Dana, Sam with Northline. I know I'm calling out of the blue. Can I take 30 seconds to tell you why, and you tell me if we should keep talking?" | Mid-market titles, people who get many calls | Gong and 30MPC 2024: permission opener 11.18%; Berman: honor the 30 seconds |
| O3 | "Hi Dana, Sam with Northline. Have you heard our name tossed around?" then straight into the reason | Teams with some brand awareness in the segment | Gong and 30MPC 2024: 11.24% |
| O4 | "Hi, is this the owner of Reyes Air?" then O1 | Local business, owner might answer | Confirms you have the decision maker before the reason |

Avoid: "How are you doing today?" read as a script, "Is now a good time?", and any opener that implies you have spoken before.

## 2. Reason, question and ask by motion

### 2a. Local business, review count angle (Local Business Database or Maps fields)

> **Reason:** "The reason I'm calling is Reyes Air has a 4.8 on Google, but 41 reviews, and the three HVAC companies ranked above you in Plano each have over 300."
>
> **Question:** "Right now, after a job's done, how do your techs ask for a review?"
>
> **Ask:** "We set that up for contractors in about a week. Can I show you on a 15 minute call, Tuesday at 10 or Wednesday at 2?"

### 2b. Local business, new listing angle (a business first seen in this week's pull with few reviews)

> **Reason:** "I'm calling because Lakeview Pediatric Dentistry just showed up on Google Maps with 3 reviews, so I'm guessing you opened in the last few months."
>
> When a permit or license record dates the opening (`references/public-records-triggers.md`), cite it instead of guessing: "I saw your sales tax permit for the Lakeview location was issued on October 2nd."
>
> **Question:** "Where are new patients finding you so far?"
>
> **Ask:** "We help new practices get to their first 50 reviews. Can I show you how in 15 minutes Thursday morning?"

### 2c. B2B title list (Lead Database fields)

> **Reason:** "The reason I'm calling is you run sales at a 120 person software company, and teams that size usually have reps building lists by hand."
>
> **Question:** "How are your reps getting their lists today?"
>
> **Ask:** "I can show you a sample list for your exact market in 20 minutes. Does Tuesday at 11 or Thursday at 3 work?"

### 2d. Ecommerce store (Store Leads fields)

> **Reason:** "I'm calling because Northpaw runs Shopify with Recharge installed, and subscription churn tends to spike in month two."
>
> **Question:** "What happens today when a subscriber skips or pauses?"
>
> **Ask:** "We built a skip-a-month flow for a pet brand your size. 15 minutes Wednesday to walk through it?"

### 2e. Technology change (Tech Stack Search domain list)

> **Reason:** "The reason I'm calling is your site still runs on Magento 1, and support for it ended in 2020."
>
> **Question:** "Is a replatform on the roadmap this year, or is it working fine as is?"
>
> **Ask:** "If it's on the list, a 20 minute call on timelines would help you plan. Monday at 1?"

### 2f. Business for sale (BizBuySell listing and broker contact)

> **Reason:** "I'm calling about the HVAC business you have listed in Mesa. We work with buyers looking for exactly that size of service business."
>
> **Question:** "Are you still taking buyer conversations, or is it under LOI?"
>
> **Ask:** "Could I send one qualified buyer profile and set 10 minutes Friday to go over fit?"

### 2g. If they engage: discovery, then sell the meeting

Ronen Pessar describes the call as four stages: pick-up, conversation, interest, meeting (Sell Better show notes). Once the opener gets a response, he says to "start the qualification with a present-tense closed-ended question" (The Sales Doctor, episode 43). His Triple Session training adds a transition that confirms you have the right person, open probing questions with a pause after each, and confirming the email and invite while the prospect is still on the line.

Tom Slocum (The SD Lab) holds that a cold call earns the next conversation and leaves the demo for the meeting. Answer narrow questions directly, skip the product tour, and when you ask, summarize the problem you heard, say what the meeting will cover, and offer one specific next step.

| Beat | Goal | Line (HVAC example) | Basis |
|-|-|-|-|
| Transition | Right person, relevant topic | "Are you the one who handles reviews and marketing, or is that someone else?" | Pessar, Triple Session |
| Qualify, closed and present tense | Current state, and that this person owns and pays for what the offer covers | "Do you sign off on the office software, and do your techs ask every customer for a review at the end of the job today?" For equipment offers to tenants: "Are the rooftop units on you or the landlord under your lease?" A no on ownership: "Who handles that?", log Not Me or Referred, do not book | Pessar, The Sales Doctor ep. 43; outcomes per Gilkey |
| Probe, open | The problem in their words | "What happens on the jobs where they forget?" then stop talking | Pessar, Triple Session; Blount |
| Summarize and sell the meeting | Earn the next step | "So reviews depend on techs remembering, and some jobs slip through. In 15 minutes I can show you how contractors automate that ask. Tuesday at 4:15 or Wednesday at 9:15?" | Slocum, SD Lab |
| Confirm | Lock it before hanging up | "What email should the invite go to? I'm sending it now. Can you see it come in?" | Pessar, Triple Session |

Slocum keeps diagnosis for the meeting, and Gong's cold calling tips found more back-and-forth and shorter prospect monologues in successful calls: a few questions, then the ask. A product question gets a one-sentence answer and a return to the ask. If they ask for a demo on the spot, book it as the meeting.

### 2h. Name the stake: their costliest equipment or risk

Name the one asset or risk the owner already worries about, in their words, in place of a generic benefit. Before writing the reason for a segment, answer one question: what is the most expensive thing that can break, sit idle or go wrong in this business this month that the seller's offer fixes? The stake depends on the seller as much as the buyer: a restaurant's walk-in cooler is the stake only for a seller who services refrigeration. Put that noun in the reason or the question, and log it as the script's stake (the Stake row in the Call Script section of the plan).

The rows below are examples to adapt, not research findings. Confirm the stake on your first conversations: if owners do not bring it up or agree with it, pick another.

| Seller and buyer (example) | Stake to name | Reason or question that uses it |
|-|-|-|
| HVAC maintenance to restaurants | A rooftop unit failing over a full dining room on a 100 degree Friday, with tables comped and covers lost | "When a rooftop unit quits on a Friday night in August, who do you call, and how long until they're on the roof?" |
| Refrigeration service to restaurants | The walk-in cooler or freezer failing overnight and the stock inside it | "When the walk-in goes down on a Saturday night, who gets the call, and what do you lose before they show up?" |
| HVAC and plumbing contractors | Trucks and techs sitting idle on a slow day while after-hours calls ring to voicemail and go to the next listing | "On a slow Tuesday, how many trucks are parked by noon, and where are those missed calls from last night going?" |
| Dental practices | An empty chair hour from a no-show or a late cancellation that nobody refilled | "When a hygiene patient cancels the morning of, how does that chair get filled today?" |

Rules: one stake per script; tie it to a fact you can see (a review complaint about a broken cooler, a listing that says "24/7" with no after-hours number, a recall gap); never invent a loss figure for the prospect.

## 3. Objection bank

Structure for every response: acknowledge in a few words, ask one question that tests whether the objection holds up, then ask again or exit. Every response below is under 45 words and contains a question. The type column follows the usual six-way split (value, timing, competition, authority, status quo, trust) plus access and stop requests; tag the type in the CRM so the weekly review counts them.

| # | Type | Objection | Response | If they hold firm, log as |
|-|-|-|-|-|
| 1 | Status quo | "Not interested." | "Fair enough. Is that because the timing's wrong, or because it doesn't fit how you run things?" | Ask which; Not Interested with the reason |
| 2 | Access | "Send me an email." | "Happy to. To make it useful, what should it cover: pricing, how it works, or results for companies like yours?" | Activated if they name an item and a callback time; else Not Now |
| 3 | Competition | "We already use someone for that." | "Good, that means it's a priority. What do you like most about them, and is there anything you'd change?" | Not Interested, competitor named |
| 4 | Timing | "I'm busy." | "Understood. I'll be quick or I'll call back. Is later today better, or tomorrow morning?" | Callback task at the time they pick |
| 5 | Trust | "How did you get my number?" | "It's listed with your business on Google. I'm Sam at Northline, calling about reviews for HVAC companies. Want me to take the number off our list?" | Removed on yes, the same day |
| 6 | Stop | "Don't call me again." | "Understood, I'll remove this number now." | Removed the same day, all channels stopped. The question rule does not apply here. |
| 7 | Value | "We don't have budget." | "Makes sense. What are you spending on getting new customers right now, roughly per month?" | Not Now with the date they give |
| 8 | Status quo | "We get plenty of business from referrals." | "That's a good spot to be in. When a referral looks you up before calling, what do they see on Google?" | Not Interested, reason referrals |
| 9 | Authority | "I'm not the right person." | "Thanks for telling me. Who handles marketing there, and is it OK if I mention you pointed me to them?" | Referred with the name, or Not Me |
| 10 | Timing | "Call me next quarter." | "Will do. What changes next quarter that makes it a better time?" | Not Now, task on the date with their reason |
| 11 | Value | "What does it cost?" | "It depends on locations, usually $200 to $400 a month. Can I take 15 minutes to show you whether it would pay for itself?" | Activated; give the range only if your pricing supports one |
| 12 | Trust | "Is this a sales call?" | "Yes, it is. I'm calling about one specific thing, review volume. Can I take 30 seconds and you decide?" | Not Interested on a no |
| 13 | Trust | "We tried something like this, didn't work." | "That's useful to know. What did you try, and what went wrong with it?" | Not Interested, competitor and failure reason logged |
| 14 | Access | "Just email the owner." (front desk) | "Will do. What's the best address for them, and when are they usually in the office?" | Gatekeeper disposition with owner hours |

### 3a. Pre-handle the top objection

Count objections by type as conversations come in. Once one type leads, answer it before it is raised, inside the reason or the voicemail, in one clause. Examples: if "we already have someone" leads, the reason becomes "...and you probably have a company you call when something breaks; this is about the checks between those calls." If "send me an email" leads, the ask offers the email and the time together: "I'll send the one-page sample now; can we look at it together Thursday at 2:30?" Test the pre-handled version as the week's one lever.

### 3b. Delivery

Points a manager can coach from a recording: the first sentence carries full name and company; after the question, stop talking until they answer (Blount); name, company and reason fit in Berman's 8 to 10 seconds. Pessar sets warmth by role: warmer for people-facing roles, crisper for technical ones (Mixmax interview, 2023).

## 4. Voicemail

Berman's rule: under 30 seconds, name and company, one reason, the number twice, no pitch. At the 150 words a minute the National Center for Voice and Speech gives for US conversation (cited by Voices.com), 30 seconds is about 75 words, so that is the cap; the scripts below are 40 to 60. Time yours out loud once.

| ID | Use | Script |
|-|-|-|
| V1 | First attempt, any motion | "Hi Dana, it's Sam Patel with Northline, 214 555 0182. I'm calling about review volume at Reyes Air; you have a 4.8 but 41 reviews. I'll send a short email with what I mean. Again, Sam, 214 555 0182." |
| V2 | Third attempt | "Dana, Sam with Northline again, 214 555 0182. One idea on getting more Google reviews from finished jobs. If it's not a priority, reply to my email with 'no' and I'll stop. 214 555 0182." |
| V3 | Final attempt | "Hi Dana, Sam at Northline. This is my last call about reviews for Reyes Air. If it ever becomes a priority, I'm at 214 555 0182. Thanks." |

### 4a. Cadence emails

Every email a voicemail or cadence promises is written in the plan with a subject and merge fields. Shapes to adapt (the plan fills in the offer's own words):

| ID | When | Template |
|-|-|-|
| E1 | Same day as V1 | Subject: {business} {topic}. "Hi {owner_first}, I just left you a voicemail. {fact_from_record}. {one_sentence_offer}. Worth {meeting_length} on {slot_1} or {slot_2}? {rep_first}, {company}, {callback_number}" |
| E2 | Same day as V2 | Subject: question about {topic} at {business}. "{owner_first}, one question: {qualify_question} If it's you, does {slot_1} work? {rep_first}" |
| E3 | Same day as V3 | Subject: closing the file. "{owner_first}, I've tried you a few times about {topic} for {business}, so I'll close the file. If it becomes a priority, reply here and I'll send two times. {rep_first}, {callback_number}" |

Rep-left voicemails on click-to-call and power-dialer lists, so each one can cite the record's facts. Pre-recorded drops only on parallel lists (`references/dialer-and-caller-id.md` section 3).

## 5. Gatekeepers and front desks

Give your name, company and the reason in one line, then ask for help reaching the owner. Ask the gatekeeper's name ("And who am I speaking with?"), log it with the owner hours you learn, book the callback at that time, and use the name on the next call.

| Situation | Line |
|-|-|
| "What's this regarding?" | "It's Sam from Northline, about getting more Google reviews from finished jobs. Is the owner the right person for that, or is it someone else?" |
| "Are they expecting your call?" | "No, this is a first call. When is the owner usually free to take a quick call?" |
| "I can take a message." | "Thanks. Could you let them know Sam from Northline called about reviews, 214 555 0182? And what time are they usually in?" |
| "They don't take sales calls." | "Understood. Is email better? What address should I use?" |
| Owner works in the field (contractors) | "When does the owner usually check in with the office, first thing or end of day?" |
| Dental or medical office | "I'll keep it short. Who handles marketing for the practice, the doctor or the office manager?" |

Log every gatekeeper outcome with the owner hours you learned. That note lets you schedule the next attempt for a time they are in.

## 6. Local business variants

| Vertical | Who answers | Opening adjustment | Reason that works |
|-|-|-|-|
| HVAC, plumbing, roofing | Dispatcher or owner's mobile | Ask for the owner by name if `contact_first_name` exists | Review count vs local competitors, missed-call volume in peak season |
| Dental and medical | Front desk | Ask for the office manager first | New patient flow, reviews, recall |
| Restaurants | Host or manager | Ask for the owner or GM and when they are free | Online ordering fees, reviews |
| Salons and spas | Front desk, owner often behind the chair | Ask when the owner has a break | Rebooking, no-shows |
| Law, accounting, real estate offices | Receptionist | Name the partner or broker from the record | Lead flow, reviews, intake speed |

## 7. Call notes block (paste into the CRM after each conversation)

```text
3x3 account:
3x3 person:
3x3 why now:
Reached: owner | manager | gatekeeper | none
Conversation outcome: Meeting Scheduled | Activated | Not Now | Not Me | Referred | Not Interested
Problem stated in their words:
Current tool or vendor:
Objection and reason:
Owner hours learned:
Next step and date:
Asked not to be called: yes | no
```

## Sources

- https://www.gong.io/resources/labs/cold-call-opening-lines/
- https://www.gong.io/resources/labs/the-best-and-worst-cold-call-openers-backed-by-data-from-300m-calls/
- https://www.insidesales.com/secrets-of-phone-prospecting-jeb-blount/
- https://alexberman.com/cold-calling-techniques
- https://x.com/srichardv/status/724894945027436545
- https://www.linkedin.com/posts/saleskickoffspeaker_3x3-research-in-10-slides-from-execvision-activity-6785267794784067584-ajbZ
- https://salesintel.io/blog/3x3-research-a-new-success-mantra-for-a-productive-sales-call/
- https://www.thesdlab.com/resources/relevance-over-personalization
- https://www.thesdlab.com/resources/sell-the-meeting-not-the-product
- https://sellbetter.xyz/daily-show/how-to-run-a-successful-cold-call-from-opener-to-booked-meeting
- https://www.thesalesdocrx.com/podcast/episode-43-cold-calling-techniques-that-work-with-ronen-pessar
- https://triplesession.com/session/set-1-meeting-per-day-with-cold-calling
- https://www.cognism.com/cold-calling-report-2025
- https://www.mixmax.com/blog/interview-ronen-pessar
- https://www.gong.io/resources/labs/cold-calling-tips/
- https://www.voices.com/tools/words_to_time_conversion
