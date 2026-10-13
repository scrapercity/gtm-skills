# Call Scripts and Objections

Original scripts built on the opener, reason, question, ask structure. Every script uses fields ScraperCity returns, so the reason for the call is a fact the rep can see on screen: `total_score` and `reviews_count` from the Local Business Database, Maps or Yelp; title, company size and industry from the Lead Database; platform and apps from Store Leads; a domain from Tech Stack Search (`scrape_builtwith`). Edit the bracketed parts; never invent a client result.

Rules for every script:

- The first sentence says who you are and where you are from. No disguised identity (47 CFR 64.1200(d)(4) requires the caller's name, the company and a contact number or address for telemarketing).
- No "did I catch you at a bad time?" (Gong Labs measured about 40% fewer meetings).
- One reason, one question, one ask. Stop talking after each question (Blount).
- The ask names a time.
- Any "don't call me again" ends the call politely and goes to the company DNC list the same day.

## 1. Openers

| ID | Opener | When | Basis |
|-|-|-|-|
| O1 | "Hi Dana, this is Sam with Northline. The reason I'm calling is..." | Default for every motion | Gong 2018: stating the reason 2.1x |
| O2 | "Hi Dana, Sam with Northline. I know I'm calling out of the blue. Can I take 30 seconds to tell you why, and you tell me if it's worth a conversation?" | Mid-market titles, people who get many calls | Gong and 30MPC 2024: permission opener 11.18%; Berman: honor the 30 seconds |
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
> **Question:** "Where are new patients finding you so far?"
>
> **Ask:** "We help new practices get to their first 50 reviews. Worth 15 minutes Thursday morning?"

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

## 3. Objection bank

Pattern for every response: acknowledge in a few words, ask one question that tests whether the objection is real, then ask again or exit. Two objections in a row with no opening: thank them and end the call. Every response below is under 45 words and contains a question.

| # | Objection | Response | If they hold firm |
|-|-|-|-|
| 1 | "Not interested." | "Fair enough. Is that because the timing's wrong, or because it doesn't fit how you run things?" | Ask which; if fit, thank and log Not interested with the reason |
| 2 | "Send me an email." | "Happy to. So it's worth opening, what should it cover: pricing, how it works, or results for companies like yours?" | Send that one thing; book a follow-up call time before hanging up |
| 3 | "We already use someone for that." | "Good, that means it's a priority. What do you like most about them, and is there anything you'd change?" | If nothing to change, log competitor name and set a 6 month nurture |
| 4 | "I'm busy." | "Understood. I'll be quick or I'll call back. Is later today better, or tomorrow morning?" | Book the callback in the CRM with a time |
| 5 | "How did you get my number?" | "It's listed with your business on Google. I'm Sam at Northline, calling about reviews for HVAC companies. Want me to take the number off our list?" | If yes, DNC entry the same day |
| 6 | "Don't call me again." | "Understood, I'll remove this number now. Sorry for the interruption. Have a good afternoon." | DNC entry, no further call or text. The question rule does not apply here. |
| 7 | "We don't have budget." | "Makes sense. What are you spending on getting new customers right now, roughly per month?" | If nothing, log Not now with a 90 day date |
| 8 | "We get plenty of business from referrals." | "That's a good spot to be in. When a referral looks you up before calling, what do they see on Google?" | Log Not interested, reason referrals |
| 9 | "I'm not the right person." | "Thanks for telling me. Who handles marketing there, and is it OK if I mention you pointed me to them?" | Capture name; `find_mobiles` or `find_emails` for the referral |
| 10 | "Call me next quarter." | "Will do. What changes next quarter that makes it a better time?" | Task on the date with their reason in the note |
| 11 | "What does it cost?" | "It depends on locations, usually $200 to $400 a month. Worth 15 minutes to see if it would pay for itself for you?" | Give the range only if you have a real one |
| 12 | "Is this a sales call?" | "Yes, it is. I'm calling about one specific thing, review volume. Can I take 30 seconds and you decide?" | Respect a no immediately |
| 13 | "We tried something like this, didn't work." | "That's useful to know. What did you try, and what went wrong with it?" | Log the competitor and the failure reason |
| 14 | "Just email the owner." (front desk) | "Will do. What's the best address for them, and when are they usually in the office?" | Log the owner hours on the record |

## 4. Voicemail

Berman's rule: under 30 seconds, name and company, one reason, the number twice, no pitch. This skill caps a voicemail script at 75 words; the scripts below are 40 to 60. Time yours out loud once.

| ID | Use | Script |
|-|-|-|
| V1 | First attempt, any motion | "Hi Dana, it's Sam Patel with Northline, 214 555 0182. I'm calling about review volume at Reyes Air; you have a 4.8 but 41 reviews. I'll send a short email with what I mean. Again, Sam, 214 555 0182." |
| V2 | Third attempt | "Dana, Sam with Northline again, 214 555 0182. One idea on getting more Google reviews from finished jobs. If it's not a priority, reply to my email with 'no' and I'll stop. 214 555 0182." |
| V3 | Final attempt | "Hi Dana, Sam at Northline. This is my last call about reviews for Reyes Air. If it ever becomes a priority, I'm at 214 555 0182. Thanks." |

Live, rep-left voicemails only. Prerecorded voicemail drops and ringless voicemail are artificial or prerecorded messages and need consent on wireless numbers (see `references/dialing-compliance-gate.md`).

## 5. Gatekeepers and front desks

The front desk is doing its job. Tell the truth, be brief, and ask for help.

| Situation | Line |
|-|-|
| "What's this regarding?" | "It's Sam from Northline, about getting more Google reviews from finished jobs. Is the owner the right person for that, or is it someone else?" |
| "Are they expecting your call?" | "No, this is a first call. When is the owner usually free to take a quick call?" |
| "I can take a message." | "Thanks. Could you let them know Sam from Northline called about reviews, 214 555 0182? And what time are they usually in?" |
| "They don't take sales calls." | "Understood. Is email better? What address should I use?" |
| Owner works in the field (contractors) | "When does the owner usually check in with the office, first thing or end of day?" |
| Dental or medical office | "I'll keep it short. Who handles marketing for the practice, the doctor or the office manager?" |

Log every gatekeeper outcome with the owner hours you learned. That note turns the next attempt into a scheduled call.

## 6. Local business variants

| Vertical | Who answers | Opening adjustment | Reason that lands |
|-|-|-|-|
| HVAC, plumbing, roofing | Dispatcher or owner's mobile | Ask for the owner by name if `contact_first_name` exists | Review count vs local competitors, missed-call volume in peak season |
| Dental and medical | Front desk | Ask for the office manager first | New patient flow, reviews, recall |
| Restaurants | Host or manager | Never during service; ask for the owner or GM | Online ordering fees, reviews |
| Salons and spas | Front desk, owner often behind the chair | Ask when the owner has a break | Rebooking, no-shows |
| Law, accounting, real estate offices | Receptionist | Name the partner or broker from the record | Lead flow, reviews, intake speed |

## 7. Call notes block (paste into the CRM after each conversation)

```text
Reached: owner | manager | gatekeeper | none
Problem stated in their words:
Current tool or vendor:
Objection and reason:
Owner hours learned:
Next step and date:
DNC requested: yes | no
```

## Sources

- https://www.gong.io/resources/labs/cold-call-opening-lines/
- https://www.gong.io/resources/labs/the-best-and-worst-cold-call-openers-backed-by-data-from-300m-calls/
- https://www.insidesales.com/secrets-of-phone-prospecting-jeb-blount/
- https://alexberman.com/cold-calling-techniques
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf
- https://www.cognism.com/cold-calling-report-2025
