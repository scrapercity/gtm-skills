# Multi-Channel Outreach Plan: HVAC contractors in Dallas-Fort Worth

Prepared 2026-10-13 for Northbeam Dispatch (fictional company used as an example), which sells an after-hours call answering and booking service to HVAC contractors at $650 a month. Average customer stays 12 months, so one closed deal is worth about $7,800. Prices checked 2026-10-13.

## Summary

The list is 1,140 HVAC contractors across nine Dallas-Fort Worth cities, pulled from the Local Business Database with a phone, an email and at least 20 Google reviews. Tier A (280 contractors with 150+ reviews and a named contact) gets a 14 business day cadence of 4 emails, 3 calls and 1 postcard. Tier B (520 with 40 to 149 reviews) gets 4 emails and 2 calls to the business line. Tier C (340 with 20 to 39 reviews) gets email only. LinkedIn is left out: the Local Business Database returns no LinkedIn URL for these owners, and few trade owners work from LinkedIn. After the phone gate, 144 tier A owners have a callable mobile; the other 136 get business-line calls. ScraperCity data costs $27.21 (validation $8.21, Mobile Finder $19.00 for 76 numbers found). Cash cost for the program is $611.06, or $2,804.39 with rep time. The user approved the $19.00 Mobile Finder run and the $336.00 postcard order on 2026-10-13.

## Channel Roles

| Channel | Role in this plan | Used for tiers | Not used because |
|-|-|-|-|
| Email | Carries the offer and the proof: "a Plano contractor booked 31 after-hours jobs in September that used to go to voicemail" | A, B, C | Used everywhere |
| Phone | Converts owners who will not answer email; mobiles for tier A, business line for tier A without a callable mobile and for tier B | A, B | Tier C deal value per contact cannot carry rep time |
| LinkedIn | None | None | No LinkedIn URLs in the data; trade owners rarely work from LinkedIn |
| Direct mail | Pattern break that lands on the owner's desk at the shop address | A | Postcard at $1.20 is over the tier B break-even per contact |

## Contact Tiers

| Tier | Rule | Contacts | Channels |
|-|-|-|-|
| A | `reviews_count` 150 or more and `contact_first_name` present | 280 | Email, mobile or business-line call, postcard |
| B | `reviews_count` 40 to 149 | 520 | Email, business-line call |
| C | `reviews_count` 20 to 39 | 340 | Email only |
| Total | | 1,140 | |

Break-even per contact at a 25% close rate: tier A at a 3% meeting rate carries $7,800 x 25% x 3% = $58.50, far above its $9.31 cost per contact (`references/channel-cost-model.md` section 5). Meeting rates are hypotheses to replace after the first 300 contacts finish.

## Cadence

| Tier | Day | Channel | Touch | Owner | Gate |
|-|-|-|-|-|-|
| A | 1 | Email | Touch 1: review count fact, Plano proof, question | Sequencer (Instantly) | CAN-SPAM: postal address and opt-out line in the footer |
| A | 2 | Phone | Call 1, live rep, click-to-call, voicemail V1 | Jordan Pike (SDR) | TCPA 47 CFR 64.1200 and National DNC scrub passed; internal DNC clear; 09:00 to 20:00 Central (strictest state window applied everywhere) |
| A | 3 | Direct mail | Postcard M1 mailed to the shop `address`, lands about day 8 | Ops, print vendor | Business address; email or phone opt-out checked; opt-out line printed |
| A | 4 | Email | Touch 2 in thread: second proof (missed-call count) | Sequencer | CAN-SPAM footer |
| A | 6 | Phone | Call 2 at the other window, no voicemail | Jordan Pike | TCPA and DNC as day 2; 1 call per day, 3 per cadence (Florida FTSA cap of 3 per 24 hours is stricter than needed) |
| A | 9 | Email | Touch 3: references the postcard headline | Sequencer | CAN-SPAM footer |
| A | 12 | Phone | Call 3, voicemail V3 (breakup) | Jordan Pike | TCPA and DNC as day 2 |
| A | 14 | Email | Touch 4: breakup | Sequencer | CAN-SPAM footer |
| B | 1 | Email | Touch 1 | Sequencer | CAN-SPAM footer |
| B | 3 | Phone | Business line, front desk F1, ask for the owner by name | Sam Okafor (SDR) | Business landline per TSR B2B exemption; internal DNC clear; 09:00 to 20:00 Central |
| B | 4 | Email | Touch 2 | Sequencer | CAN-SPAM footer |
| B | 9 | Phone | Business line, F1 at the other window | Sam Okafor | TSR B2B exemption, internal DNC clear, TCPA calling window |
| B | 11 | Email | Touch 3 | Sequencer | CAN-SPAM footer |
| B | 15 | Email | Touch 4: breakup | Sequencer | CAN-SPAM footer |
| C | 1, 4, 9, 15 | Email | Touches 1 to 4 | Sequencer | CAN-SPAM footer |

Stop rule: a reply on any channel, a booked meeting, or an opt-out on any channel stops every channel for that contact and for every other contact at the same business (`domain` or `phone` match). A rep logs the stop in Instantly (lead status) and in the call sheet the same day.

Cohorts: 70 tier A and 130 tier B contacts start each week for 4 weeks, so two SDRs at 2 hours of calling a day cover the 62.7 hours of dialing.

## Compliance Gates

| Gate | Applies to | Rule and law | Result for this list |
|-|-|-|-|
| Dialing method | All calls | TCPA 47 CFR 64.1200(a)(1)(iii): no autodialer, prerecorded or AI voice calls to cell phones without prior express consent. Plan uses live reps on click-to-call only | Pass for all calls; no voicemail drops, no AI voice |
| Internal DNC and cross-channel opt-outs | All calls and mail | 47 CFR 64.1200(d) company-specific DNC list; any email unsubscribe also stops calls and mail | 2 tier A mobiles removed |
| National DNC Registry | Mobiles (Mobile Finder and `contact_mobile`) | 47 CFR 64.1200(c)(2) and (e); FTC TSR Q&A: registry refreshed every 31 days. Business-to-business exemption not relied on for mobiles | Registry file for 7 DFW area codes dated 2026-10-02; 26 mobiles removed |
| Calling window | All calls | 47 CFR 64.1200(c)(1) 08:00 to 21:00; Texas Bus. & Com. Code 301.051 09:00 start and Florida FTSA 20:00 stop applied as the house window | 09:00 to 20:00 Central, all contacts are in Texas |
| Call frequency | All calls | Florida FTSA 3 calls per 24 hours; house cap 1 a day, 3 per cadence | Enforced in the call sheet |
| Email content | All email touches | CAN-SPAM: accurate headers, non-deceptive subject, postal address, opt-out honored within 10 business days (house: 24 hours) | Footer set in Instantly |
| Mail | Tier A postcards | CAN-SPAM does not cover mail; house rule: business address only, opt-out line, no imitation of official mail | 280 business addresses, 0 residential |
| Data use | All ScraperCity data | ScraperCity terms; FCRA purposes excluded (prospecting only) | Prospecting only |

## Channel Copy

| Code | Channel | Copy or reference |
|-|-|-|
| E1 to E4 | Email | Written in `cold-email-copywriting`. E1 subject "after-hours calls at {{business_name}}", first line "{{business_name}} has {{reviews_count}} reviews, which usually means the phone rings after 6pm too." Body under 90 words, ends with a question |
| V1 | Phone voicemail | "Hi Ray, Jordan with Northbeam. I emailed you about after-hours calls at Reyes Air, the one with the Plano numbers. 214-555-0137, again 214-555-0137." (under 30 seconds) |
| V3 | Phone voicemail | "Hi Ray, Jordan with Northbeam, last call from me. If nights are covered, I'll close the file. If not, Tuesday's email has the Plano numbers. 214-555-0137, 214-555-0137." |
| F1 | Business line | "Hi, this is Sam with Northbeam. Is Ray in today? I emailed him about the after-hours line." |
| M1 | Postcard, 6 x 9 | Front: "31 after-hours jobs booked in September for one Plano contractor." Back: two lines on how the line answers and books, `northbeam.co/dfw` and 214-555-0137, sender name, return address, "Prefer no mail? Call or email and we'll remove you." |

## Data and Cost

`check_wallet` on 2026-10-13: $284.40 balance, Growth plan. Counts came from `query_local_business_database(keyword=["hvac contractor","air conditioning contractor"], location=["Dallas TX","Fort Worth TX","Plano TX","Arlington TX","Irving TX","Frisco TX","McKinney TX","Garland TX","Denton TX"], hasPhone=true, hasEmail=true, minReviews=20, limit=1)`, `pagination.total` 1,140.

| Line | Channel | Count | Unit price | Cost |
|-|-|-|-|-|
| Local Business Database pull | All | 1,140 | Included on Growth ($149 a month, already paid) | $0.00 |
| `validate_emails` | Email | 1,140 | $0.0072 | $8.21 |
| `find_mobiles` test on tier A `contact_email` | Phone | 50 inputs, 21 found (42%) | $0.25 per number found | $5.25 |
| `find_mobiles` remaining tier A without `contact_mobile` | Phone | 134 inputs, 55 found | $0.25 per number found | $13.75 |
| DNC Registry access, 7 DFW area codes (5 free) | Phone | 2 paid area codes | $85 a year | $170.00 |
| Postcards, all-in | Direct mail | 280 | $1.20 | $336.00 |
| Cold email sends on existing infrastructure | Email | 4,172 sends (1,043 valid and catch-all contacts x 4) | $0.01866 | $77.85 |
| Rep dialing time (assumption: 30 dials an hour, $35 an hour loaded) | Phone | 1,880 dials = 62.7 hours | $35 an hour | $2,193.33 |
| Total | All | | | $2,804.39 |

ScraperCity subtotal: $8.21 + $5.25 + $13.75 = $27.21. Cash outside payroll: $27.21 + $170.00 + $336.00 + $77.85 = $611.06.

Validation results: `valid` 912, `valid_catch_all` 131, `unknown` 22, `invalid` 70, `disposable` 5 (total 1,140). Catch-alls run in a separate Instantly campaign capped at 10% of daily volume. Invalid and unknown tier A contacts still get calls and the postcard.

Mobile funnel for tier A: 96 already had `contact_mobile`, 76 found by Mobile Finder, 172 total; 26 on the National DNC Registry and 2 on the internal list removed; 144 callable mobiles. The other 136 tier A owners get business-line calls.

## Tracking

| Metric | Per channel | Target or decision rule |
|-|-|-|
| Positive replies and meetings | Email, phone, mail (mail has its own URL `northbeam.co/dfw` and its own number) | Credit the meeting to the channel of the first positive response |
| Meetings per 100 contacts | Tier A, B, C | Hypotheses: A 3, B 1.5, C 0.8. Below half of target after 300 contacts: change the offer before adding volume |
| Cost per meeting | Per tier | Tier A target under $150. Over $300 after 300 contacts: drop the postcard first, then call 3 |
| Connect rate | Mobile vs business line | If mobile connects are under 2x business-line connects after 200 dials each, stop buying mobiles |
| Hard bounce rate | Email | Under 2% per campaign; pause at 2% |
| Opt-outs | All channels | Suppressed on every channel the same day; log count weekly |
