# Cold Calling Plan: Northline Reviews, HVAC and Plumbing in Dallas-Fort Worth

Illustrative example.

Company and offer, in the user's words: Northline Reviews (a fictional company for this example) sells review-request texts that go out from the contractor's own job-completion workflow, $249 a month per location. Market: HVAC and plumbing contractors in Dallas-Fort Worth. Reps: 2 SDRs (Sam Patel and Ana Ruiz), Central time, managed by the founder, Dana Cole. Dialer: HubSpot calling, click-to-call, one line per rep. CRM: HubSpot Sales Hub Professional. Plan period: 20 business days, Monday 2026-10-19 to Friday 2026-11-13.

## Program Summary

| Item | Value |
|-|-|
| Motion | Local business, owner-operated contractors; a dispatcher or the owner answers |
| Meeting being booked | 15 minute screen-share demo with the owner |
| Meetings target for the period | 12 booked, 9 held |
| Reps and hours per day | 2 SDRs, 3 blocks of 90 minutes each (4.5 hours of dialing) |
| Calling window | 9:00am to 10:30am, 2:00pm to 3:30pm and 4:00pm to 5:30pm Central, Monday to Friday; nothing from 12 to 2pm |
| ScraperCity plan | Growth, $149 a month with $159 in credits |

Estimates: connect, conversation and meeting rates are Belkins' 2025 B2B figures (no local-business benchmark found) until Northline's own rates replace them; dials per hour come from the 2026-10-14 dialer trial, show rate from Northline's inbound demos, and row counts from the 2026-10-15 pull.

## Launch Checklist

| Task | Owner | Date |
|-|-|-|
| Export demos booked since 2026-04-01 that did not buy | Dana Cole | 2026-10-14 |
| Pull, format, dedupe, suppress and type the list; hand-check 25 random records | Ana Ruiz | 2026-10-15 |
| Register the five numbers with the Free Caller Registry, confirm A attestation with HubSpot calling, test-call AT&T, Verizon and T-Mobile phones | Sam Patel | 2026-10-15 |
| HubSpot call outcomes, required properties and the weekly funnel report | Dana Cole | 2026-10-15 |
| Map the removed-numbers property into the call queue and test that a removed number is skipped | Ana Ruiz | 2026-10-16 |
| Recurring block events on both calendars; 30 minute script and objection role-play per rep | Sam Patel | 2026-10-16 |

## Call List Build

| Step | Source or action | Filters in plain words | Rows |
|-|-|-|-|
| 0 Own records | HubSpot | Demos booked since 2026-04-01 with no purchase; not a current customer | 64; dialed first, the reason cites their demo date |
| 1 Count, then pull | Local Business Database | Keywords "hvac contractor", "air conditioning contractor", "heating contractor", "plumber" and "plumbing contractor"; Dallas, Fort Worth, Arlington, Plano, Irving and Garland TX; has a phone; 10 to 150 reviews, because the offer sells review volume and under 10 goes to step 8 | 1,384 businesses, included in Growth |
| 2 Format phones | +1 and 10 digits (E.164); main line and mobile in separate columns | Drop numbers that fail the US format | 1,362 (22 dropped) |
| 3 Dedupe | Phone, then name plus postal code | Same company listed twice | 1,321 (41 merged) |
| 4 Suppress | HubSpot customers, step 0 records, removed numbers | Domain and phone match | 1,297 |
| 5 Owner mobiles on file | Named contact with a mobile on the record | | 210 |
| 6 Find owner mobiles | Mobile Finder, $0.25 per number found, nothing when none is found | 380 owner emails on rows with no mobile; first 100, then the rest at the measured hit rate | 133 found (35%), $33.25 from the plan credits |
| 7 Line type on main lines | Northline's carrier lookup account | 1,297 main lines | 827 landline or VoIP, 470 wireless |
| 8 Fresh openings (free public data) | TDLR air conditioning contractor license file: numbers in the 2026-10-13 file and absent from the 2026-09-14 file | Matched by phone or address to listings with 10 reviews or fewer in the same 6 cities | 24 matched; list v2, the reason cites the license date |

Dial order: step 0 records, then owner mobiles (343) and wireless main lines (470) in Block 1, then landline and VoIP main lines (827) in Blocks 2 and 3.

Rep split: Sam Patel takes Dallas, Plano, Irving and Garland (about 710 businesses, 214 caller IDs); Ana Ruiz takes Fort Worth and Arlington (about 590, 817 caller IDs). Step 0 records go to the rep whose city they sit in.

Spot-check on 2026-10-15: 25 random records, 4 or more failures (closed, wrong owner, dead number) send the filter back. Result: 2 failures.

## Dialer Setup

| Setting | Value |
|-|-|
| Dial mode | Click-to-call, one line per rep: the owner opener carries the call, and 1,297 businesses fit two reps over 20 days |
| Voicemail | Rep-left V1 to V3 on attempts 1, 3 and 5 |
| Caller ID | Sam: two 214 numbers; Ana: two 817 numbers; one shared 214 backup. Test calls to AT&T, Verizon and T-Mobile phones every Monday before Block 1, and any day one number's connect rate halves |
| Calls per number per day | 59 (117 per rep over two numbers), under the 75 a day per number Readymode recommends (June 2025) |
| Window | 9:00am to 10:30am, 2:00pm to 3:30pm and 4:00pm to 5:30pm Central; logged owner hours override per record |
| Attempts | One dial per number per day, 5 at most over two weeks |
| Removed numbers | The call queue skips any record with `removed` = true; new requests set it the same day and stop every channel |

## Call Blocks

| Block | Local time | Length | Focus |
|-|-|-|-|
| Prep | 8:30 to 9:00 | 30 min | Confirm booked demos, load the day's records, read callbacks due |
| Block 1 | 9:00 to 10:30 | 90 min | Step 0 records, owner mobiles, first attempts |
| Admin | 10:30 to 11:00 | 30 min | Pre-call notes for the afternoon, HubSpot notes |
| Block 2 | 2:00 to 3:30 | 90 min | Main lines, gatekeeper callbacks at logged owner hours |
| Block 3 | 4:00 to 5:30 | 90 min | Third and fifth attempts; owners back from jobs |

Blocks are recurring busy events and stay at three a day after a good week. Work order each day: confirm booked demos, then callbacks that are due (Activated, Not Now, no-shows), then records in cadence, then new records.

| Attempt | Business day | Block | Voicemail | Email the same day |
|-|-|-|-|-|
| 1 | 1 | Block 1 | V1 | E1 |
| 2 | 2 | Block 3 | None | None |
| 3 | 4 | Block 2 | V2 | E2 |
| 4 | 7 | Block 1 | None | None |
| 5 | 10 | Block 3 | V3 | E3 |

Volume: 26 dials per rep hour (2026-10-14 trial) x 4.5 hours x 20 days x 2 reps = 4,680 dials, about 3.6 attempts per business. No conversation after attempt 5: the record closes for this cycle.

## Funnel Targets

| Stage | Rate | Basis | Count | Act if |
|-|-|-|-|-|
| Dials | 26 per rep hour | Measured, 2026-10-14 trial | 4,680 | Under 21 per rep hour: move email and notes out of the blocks |
| Connects | 9.9% of dials | Belkins 2025, B2B | 463 | Under 5% after 300 dials: more owner mobiles; run test calls for spam labels |
| Conversations | 58% of connects | Belkins 2025 | 269 | Under 40% after 50 connects: shorten the opener to name, company, reason |
| Meetings | 4.6% of conversations | Belkins 2025 | 12 | Under 3% after 50 conversations: test the reason or the ask; Not Me plus Referred over a third of conversations: ask for the owner by name and add referrals to list v2 |
| Held | 75% of meetings | Measured, Northline's inbound demos | 9 | Under 65% after 20 booked: check that C1 and C2 went out and the week-of and 2 hour calls happened |
| Cost per held meeting | (SDR cost + data + seats) / held | Measured | 9 held | Above Northline's cold email cost per held meeting at day 20: keep email primary and use the phone for callbacks |

Act-if floors are Northline's settings, written before the first dial.

## Call Script

| Part | Script | Source of the fact |
|-|-|-|
| Opener | "Hi, is this {owner_first}? {owner_first}, it's {rep_first} with Northline Reviews." | Named contact on the listing |
| Reason for the call | "The reason I'm calling is {business} has a {rating} on Google but {review_count} reviews, and {top_competitor} in {city} has {competitor_reviews}." | Listing rating and review count; top competitor is the highest review count for the same keyword and city in the pull |
| Stake (inside the offer's scope) | "When a homeowner's AC dies in August, they call whoever has the most reviews, and that replacement job goes to {top_competitor}." | The job lost at the comparison step, which more reviews address |
| Question | "After a job's done today, how do your techs ask for a review?" | Open question about the current process |
| Ask | "We set this up in about a week. Can I show you in 15 minutes, {slot_1} or {slot_2}?" | Two open slots inside the blocks |

Step 0 records use this reason instead: "The reason I'm calling is we spoke on {demo_date} about reviews for {business}, and you're at {review_count} today."

| Beat | Line |
|-|-|
| Transition | "Are you the one who handles reviews and marketing, or is that someone else?" |
| Qualify | "Do you sign off on the office software, and do your techs close jobs out in an app today?" A no on either: ask who does, log Not Me or Referred |
| Probe | "What happens on the jobs where they forget?" then stop talking |
| Sell the meeting | "So reviews depend on techs remembering, and some jobs slip through. In 15 minutes I'll show how the text goes out when the job closes. {slot_1} or {slot_2}?" |
| Confirm | "What's the best email for the invite? Sending it now, can you see it?" then send C1 |

## Objection Bank

| # | Type | Objection | Response | If they hold firm, log as |
|-|-|-|-|-|
| 1 | Status quo | "Not interested." | "Fair enough. Is that because the timing's wrong, or because it doesn't fit how you run jobs?" | Not Interested with the reason |
| 2 | Access | "Send me an email." | "Will do. To make it useful, should it show pricing, how it works, or results for a {city} HVAC company?" | Activated; send that one item and book a follow-up call |
| 3 | Competition | "We already use a review tool." | "Good, so you already ask for reviews. What do you like about it, and what would you change?" | Not Interested, tool logged, 6 month hold |
| 4 | Timing | "I'm on a job." | "Understood, I'll call back. Is after 4 today better, or tomorrow at 9?" | Callback task at the time they pick |
| 5 | Trust | "How'd you get this number?" | "It's listed on your Google Business Profile. I'm {rep_first} at Northline, calling about reviews. Want me to take it off our list?" | Removed on yes, the same day |
| 6 | Stop | "Don't call me again." | "Understood, I'll remove this number now." | Removed the same day, all channels stopped |
| 7 | Value | "No budget." | "Makes sense. What do you spend now to get a new customer, roughly?" | Not Now, 90 days |
| 8 | Status quo | "We get our work from referrals." | "That's a strong spot. When a referral looks you up before calling, what do they see on Google?" | Not Interested, reason referrals |
| 9 | Authority | "Talk to my office manager." | "Thanks. What's their name, and is it OK if I say you sent me?" | Referred; call them in the same block |
| 10 | Value | "What does it cost?" | "$249 a month per location, no contract. Can I take 15 minutes to show you whether it pays for itself?" | Activated; follow-up booked |

Once one type leads the weekly count, answer it inside the reason or V2 and test that as one lever.

## Voicemail, Gatekeeper and Email

| ID | Use | Script |
|-|-|-|
| V1 | Attempt 1 | "Hi {owner_first}, it's {rep_first} with Northline Reviews, {callback_number}. I'm calling about {business}'s Google reviews: you have a {rating} but {review_count} reviews. I'll send a short email with what I mean. Again, {rep_first}, {callback_number}." |
| V2 | Attempt 3 | "{owner_first}, {rep_first} with Northline again, {callback_number}. One idea on getting more reviews from finished jobs. If it's not a priority, reply 'no' to my email and I'll stop. {callback_number}." |
| V3 | Attempt 5 | "Hi {owner_first}, {rep_first} at Northline. Last call from me about reviews. If it ever becomes a priority, I'm at {callback_number}. Thanks." |
| G1 | Dispatcher asks what it's about | "It's {rep_first} from Northline, about getting more Google reviews from finished jobs. Is {owner_first} the right person? And who am I speaking with?" Log the dispatcher's name |
| G2 | Owner in the field | "When does {owner_first} usually check in with the office, first thing or end of day?" Callback task at that time |
| G3 | Offer to take a message | "Thanks, {gatekeeper_first}. Please tell {owner_first} that {rep_first} from Northline called about reviews, {callback_number}. What time is best to try back?" |
| E1 | Same day as V1 | Subject: {business} reviews. "Hi {owner_first}, I just left you a voicemail. {business} has a {rating} on Google with {review_count} reviews; {top_competitor} has {competitor_reviews}. Northline sends a review request by text when a job closes, so every finished job gets asked. Worth 15 minutes on {slot_1} or {slot_2}? {rep_first}, Northline Reviews, {callback_number}" |
| E2 | Same day as V2 | Subject: who closes jobs at {business}? "{owner_first}, one question: who closes jobs out in your system today? That is the step our text hangs off, so nobody has to remember to ask. If it's you, does {slot_1} work for 15 minutes? {rep_first}" |
| E3 | Same day as V3 | Subject: closing the file. "{owner_first}, I've tried you a few times about reviews for {business} and haven't reached you, so I'll close the file. If it becomes a priority, reply here and I'll send two times. {rep_first}, {callback_number}" |
| C1 | Text while they are on the line | "{owner_first}, it's {rep_first} from Northline. Confirmed: {meeting_day} at {meeting_time}, 15 minutes on screen share. The invite went to {email}. Reply here if the time stops working." |
| C2 | Email 12 to 24 hours before | Subject: tomorrow at {meeting_time}. "{owner_first}, see you tomorrow at {meeting_time}. I'll show how the review text goes out from {business}'s job-close step and what it costs. The link is in the invite. {rep_first}" |

Confirmation calls: one about a week out (or right after booking when the demo is sooner), and one 2 to 3 hours before if C2 got no reply. A no-show gets one call and two new times.

## CRM Logging

| Disposition | Counts as connect | Counts as conversation | Next action |
|-|-|-|-|
| No answer | No | No | Next attempt per cadence |
| Busy | No | No | Next business day |
| Left voicemail | No | No | Send the email the cadence names |
| Gatekeeper, message left | Yes | No | Log owner hours and gatekeeper name, retry in that window |
| Wrong number | Yes | No | Mark bad; run Mobile Finder on the owner email |
| Connected, not owner | Yes | No | Ask for the owner by name |
| Conversation, not interested | Yes | Yes | Log objection number and reason |
| Conversation, follow-up requested | Yes | Yes | Task with date and requested item |
| Meeting booked | Yes | Yes | Invite and C1 sent on the call |
| Asked not to be called | Yes | No | `removed` = true the same day, all channels stopped |

HubSpot setup: add the six dispositions that HubSpot's defaults (Busy, Connected, Left live message, Left voicemail, No answer, Wrong number) do not cover as custom call outcomes under Settings, Calling, Call Configurations, Track call outcomes. Required call properties: `call_disposition`, `number_type` (owner mobile, wireless main line, landline main line), `attempt_number`, `test_id`, `objection`, `owner_hours`, `gatekeeper_name`, `next_action_date`, `removed`, and `conversation_outcome` (Meeting Scheduled, Activated, Not Now, Not Me, Referred, Not Interested) on every conversation. Referred names go through Mobile Finder into list v2 with `referred_by` set.

## Pilot Plan

Pilot dates: 2026-10-19 to 2026-10-30. Segment: HVAC and plumbing, 10 to 150 reviews. Decision day: 2026-10-30, after Block 3.

| Week | Dates | Lever changed | Version run | Volume | Decision rule |
|-|-|-|-|-|-|
| 1 (baseline) | 2026-10-19 to 2026-10-23 | None | Script as written: review-gap reason with the stake, process question, two named times | 1,170 dials, about 67 conversations | Connect rate under 5% after 300 dials: fix the list or number type before week 2 |
| 2 (test) | 2026-10-26 to 2026-10-30 | Ask | Same list, opener, reason, stake and question; the ask offers one 15 minute slot today or tomorrow | 1,170 dials, about 67 conversations | Keep the single-slot ask if conversation-to-meeting is at least 1.5 points above week 1 with 50+ conversations each; otherwise keep two times |

Both weeks use the same reps and segment; calls carry `test_id` hvac-dfw-ask-a or hvac-dfw-ask-b. A week short of 50 conversations runs on until it gets there. Weeks 3 and 4 run the winner.

## Rep Scorecard

Actuals, filled each Friday and cut by number type, block and `test_id`; targets are in Funnel Targets. Reps are compared once each has 50 conversations in the segment.

| Rep | Days | Dials | Dials/day | Connects | Connect rate | Conversations | Conversations per 100 dials | Meetings | Conversation-to-meeting | Dials per meeting | Held | Show rate |
|-|-|-|-|-|-|-|-|-|-|-|-|-|
| Sam Patel | | | | | | | | | | | | |
| Ana Ruiz | | | | | | | | | | | | |

Call review: every Friday Dana scores 3 recorded calls per rep (one booked, one Not Interested, one random) on 8 yes or no items, gives one keep and one fix with timestamps, and the rep role-plays the fix before Monday's Block 1. Dana listens live to both reps' Block 1 on 2026-10-19.
