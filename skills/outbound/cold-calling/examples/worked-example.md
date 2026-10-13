# Cold Calling Plan: Northline Reviews, HVAC and Plumbing in Dallas-Fort Worth

Company and offer: Northline Reviews (a fictional company for this example) sells review-request texts that go out from the contractor's own job-completion workflow, $249 a month per location. Market: HVAC and plumbing contractors in Dallas-Fort Worth with 10 to 150 Google reviews. Reps: 2 SDRs, Central time. Dialer: click-to-call dialer with a built-in line type lookup, one line per rep, logs to HubSpot. CRM: HubSpot. Plan period: 20 business days starting Monday 2026-10-19.

## Program Summary

| Item | Value |
|-|-|
| Motion | Local business, owner-operated contractors |
| Meeting being booked | 15 minute screen-share demo with the owner |
| Meetings target for the period | 16 booked, 12 held |
| Reps and hours per day | 2 SDRs, 3 blocks of 90 minutes each (4.5 hours of dialing) |
| Calling window | 9am to 8pm Central, Monday to Friday; blocks inside 9:00 to 10:30, 2:00 to 3:30, 4:00 to 5:30 |
| ScraperCity plan | Growth, $149 a month with $159 in credits |

## Call List Build

| Step | Tool or action | Parameters | Rows |
|-|-|-|-|
| 1 Wallet check | `check_wallet` | none | Balance $171.40, Growth plan |
| 2 Count | `query_local_business_database` | `keyword: ["hvac contractor", "plumber"]`, `location: ["Dallas TX", "Fort Worth TX", "Arlington TX", "Plano TX", "Irving TX", "Garland TX"]`, `hasPhone: true`, `minReviews: 10`, `maxReviews: 150`, `limit: 1` | `pagination.total` 1,384 |
| 3 Pull | `query_local_business_database` | Same filters, `limit: 100`, `after: "0"` then `next_after` (14 pages) | 1,384 businesses, included in Growth |
| 4 Normalize phones to E.164 | Script per `references/list-quality-standard.md` 3c | Drop numbers that fail the US format | 1,362 (22 dropped) |
| 5 Dedupe | Key: `phone`, then name plus postal code | Same company listed twice | 1,321 (41 merged) |
| 6 Suppress | HubSpot customers, company DNC list | Domain and phone match | 1,297 (18 customers, 6 DNC) |
| 7 Owner mobiles on file | `contact_mobile` present | Named contact rows | 210 |
| 8 Find owner mobiles | `find_mobiles` | `inputs`: 380 `contact_email` values with no `contact_mobile` | 133 found (35%), $33.25 |
| 9 Line type on main lines | Dialer lookup | 1,297 `phone` values | 827 landline or VoIP, 470 wireless |

## Compliance Gate

| Check | Rule | Setting or result |
|-|-|-|
| Dialing method | 47 U.S.C. 227(b); FCC 24-17 AI-voice ruling | Click-to-call, one line per rep. Predictive dialing, prerecorded voicemail drops, ringless voicemail and AI voice are off for this list. |
| Line type | 47 CFR 64.1200(e) wireless numbers | 470 wireless main lines plus 343 owner mobiles treated as consumer; 827 landline or VoIP main lines treated as business |
| National DNC | 47 CFR 64.1200(c)(2), registry copy within 31 days | 813 consumer numbers scrubbed against the 2026-10-16 download: 162 listed, dropped |
| Texas no-call list | Texas Business and Commerce Code chapters 301 and 304 | 9 more listed, dropped |
| B2B landlines | TSR 16 CFR 310.6(b)(7) exemption | 827 business lines callable after the company DNC check |
| Company DNC | 47 CFR 64.1200(d), honored within 10 business days, kept 5 years | Dialer reads the HubSpot DNC property before each dial; house standard same day |
| Calling window | 47 CFR 64.1200(c)(1); Texas 301.051 (9am start) | 9am to 8pm Central, Monday to Friday, no weekend calls |
| Attempts cap | Florida-style 3 per 24 hours (house rule everywhere); internal policy | Max 2 dials per number per day, max 5 attempts over 10 business days |
| Caller identification | 47 CFR 64.1200(d)(4) | Rep name, Northline Reviews, callback number that rings to the rep |
| Result | Internal policy | 1,220 businesses with at least one passing number; 77 businesses go to email only |

## Call Blocks

| Block | Local time | Length | Focus |
|-|-|-|-|
| Prep | 8:30 to 9:00 | 30 min | Load the day's gated records, check callbacks due |
| Block 1 | 9:00 to 10:30 | 90 min | First attempts, owner mobiles first (owners dispatch early) |
| Admin | 10:30 to 11:00 | 30 min | Promised emails, HubSpot notes |
| Block 2 | 2:00 to 3:30 | 90 min | Second attempts on main lines, gatekeeper callbacks |
| Block 3 | 4:00 to 5:30 | 90 min | Owners back from job sites; third attempts |

Measured in a 2-day pilot: 26 dials per hour per rep with notes. 2 reps x 20 days x 4.5 hours x 26 = 4,680 dials, about 3.8 attempts per callable business, under the 5 attempt cap.

## Funnel Targets

| Stage | Rate | Basis | Count |
|-|-|-|-|
| Dials | 26 per rep hour | Measured in the 2-day pilot, 2026-10 | 4,680 |
| Connects | 25% of dials | Assumption for local lists, replace after 300 dials | 1,170 |
| Owner reached | 40% of connects | Assumption for local lists, replace after 300 dials | 468 |
| Conversations | 58% of owner reached | Belkins B2B benchmark, 2025 data | 271 |
| Meetings | 6% of conversations | Assumption, above Belkins 4.6% (2025) and Cognism/WHAM 4.82% (2024) because the reason uses a visible review gap; replace after 300 dials | 16 |
| Held | 75% of meetings | Assumption, replace after 30 meetings | 12 |
| Cross-check | 9.9% x 58% x 4.6% per dial | Belkins 2025 end-to-end | 12 meetings at B2B benchmark rates |

## Call Script

| Part | Script | Source of the fact |
|-|-|-|
| Opener | "Hi, is this Luis? Luis, it's Sam with Northline Reviews." | `contact_first_name` |
| Reason for the call | "The reason I'm calling is Reyes Air has a 4.8 on Google but 41 reviews, and the three HVAC companies above you in Plano each have over 300." | `total_score`, `reviews_count`, competitors from the same pull |
| Question | "After a job's done today, how do your techs ask for a review?" | Open question about the current process |
| Ask | "We set this up in about a week. Can I show you in 15 minutes, Tuesday at 4:15 or Wednesday at 9:15?" | Times inside the owner-hours windows |

## Objection Bank

| # | Objection | Response | If they hold firm |
|-|-|-|-|
| 1 | "Not interested." | "Fair enough. Is that because the timing's wrong, or because it doesn't fit how you run jobs?" | Log reason, close the record |
| 2 | "Send me an email." | "Will do. So it's worth opening, should it show pricing, how it works, or results for a Plano HVAC company?" | Send that one item, book a follow-up call |
| 3 | "We already use Podium." | "Good, so reviews matter to you. What do you like about it, and what would you change?" | Log competitor, nurture 6 months |
| 4 | "I'm on a job." | "Understood, I'll call back. Is after 4 today better, or tomorrow at 9?" | Callback task with the time |
| 5 | "How'd you get this number?" | "It's listed on your Google Business Profile. I'm Sam at Northline, calling about reviews. Want me to take it off our list?" | DNC on yes |
| 6 | "Don't call me again." | "Understood, I'll remove this number now. Sorry to interrupt your day." | Company DNC same day, all channels stopped |
| 7 | "No budget." | "Makes sense. What do you spend now to get a new customer, roughly?" | Not now, 90 days |
| 8 | "We get our work from referrals." | "That's a strong spot. When a referral looks you up before calling, what do they see on Google?" | Not interested, reason referrals |
| 9 | "Talk to my office manager." | "Thanks. What's their name, and is it OK if I say you sent me?" | Log referral, call within the same block |
| 10 | "What does it cost?" | "$249 a month per location, no contract. Worth 15 minutes to see if it pays for itself for you?" | Send pricing email if asked, book follow-up |

## Voicemail and Gatekeeper

| ID | Use | Script |
|-|-|-|
| V1 | First attempt | "Hi Luis, it's Sam Patel with Northline Reviews, 214 555 0182. I'm calling about Reyes Air's Google reviews; you have a 4.8 but 41 reviews. I'll send a short email with what I mean. Again, Sam, 214 555 0182." |
| V2 | Third attempt | "Luis, Sam with Northline again, 214 555 0182. One idea on getting more reviews from finished jobs. If it's not a priority, reply 'no' to my email and I'll stop. 214 555 0182." |
| V3 | Fifth attempt | "Hi Luis, Sam at Northline. Last call from me about reviews. If it ever becomes a priority, I'm at 214 555 0182. Thanks." |
| G1 | Dispatcher asks what it's about | "It's Sam from Northline, about getting more Google reviews from finished jobs. Is Luis the right person, or someone else?" |
| G2 | Owner in the field | "When does Luis usually check in with the office, first thing or end of day?" |
| G3 | Offer to take a message | "Thanks. Please tell him Sam from Northline called about reviews, 214 555 0182. What time is he usually back?" |

## CRM Logging

| Disposition | Counts as connect | Counts as conversation | Next action |
|-|-|-|-|
| No answer | No | No | Next attempt per cadence |
| Busy | No | No | Retry in the next block if under the daily cap |
| Left voicemail | No | No | Same-day email referencing the voicemail |
| Gatekeeper, message left | Yes | No | Log owner hours, retry in that window |
| Wrong number | Yes | No | Mark bad; try `find_mobiles` on `contact_email` |
| Connected, not owner | Yes | No | Ask for the owner by name |
| Conversation, not interested | Yes | Yes | Log objection number and reason |
| Conversation, follow-up requested | Yes | Yes | Task with date and requested item |
| Meeting booked | Yes | Yes | HubSpot meeting and invite within 5 minutes |
| DNC requested | Yes | No | Company DNC same day, all channels stopped |

HubSpot setup: custom call outcomes for the six dispositions HubSpot does not ship by default, required `call_disposition`, `number_class`, `gate_result`, `opener_id` and `owner_hours` properties on every logged call, and a weekly report of each funnel rate by segment and rep.

## Cost Estimate

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Local Business Database pull | 1,384 businesses | Included in Growth | $0.00 |
| `find_mobiles` numbers found | 133 | $0.25 | $33.25 (paid from the $159 plan credits) |
| `find_mobiles` inputs with no number | 247 | $0.00 | $0.00 |
| ScraperCity Growth plan | 1 month | $149.00 | $149.00 |
| National DNC registry, 6 area codes (214, 469, 972, 945, 817, 682) | 1 paid area code | $85 at the FY2027 rate (from 1 Oct 2026), first five free | $85.00 |
| Dialer seats (user input) | 2 | $120.00 | $240.00 |
| SDR loaded cost (user input) | 2 | $5,200.00 | $10,400.00 |
| Total cash for the period | | | $10,874.00 |
| Cost per booked meeting | 16 meetings | | $679.63 |
| Cost per held meeting | 12 held | | $906.17 |

`find_mobiles` at $33.25 is over $5, so the estimate (ceiling 380 x $0.25 = $95.00) was shown to the user with the `check_wallet` balance and approved before the run.
