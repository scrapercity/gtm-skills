# Call Blocks and Metrics

Funnel formulas, dated benchmarks, calling windows by source, block policy, work order and attempt cadence, dispositions and conversation outcomes, CRM fields, the rep scorecard with targets, the no-show runbook, the comparison for proving calling before hiring, and the weekly call review. Every benchmark here is a dated hypothesis to test. Replace each one with your measured rate once a segment reaches the sample size the plan sets; Berman reads connect, meeting and show rate over 50+ dials at minimum.

## 1. The funnel

| Stage | Definition used in this skill | Formula |
|-|-|-|
| Dial | Any outbound attempt, any outcome | count |
| Connect | A live human picked up (includes gatekeepers, wrong person, not interested) | connects / dials |
| Decision maker reached | The connect was the person you want (local lists only) | DM reached / connects |
| Conversation | The person engaged past the opener | conversations / connects |
| Meeting | A meeting booked with a date and time | meetings / conversations |
| Held | The meeting happened | held / meetings |

Definitions follow Belkins' 2025 benchmark page (dial, connect, conversation, meeting). Keep them fixed so weeks compare.

Planning formula:

```
dials needed = meetings target / (connect rate x conversation rate x meeting rate)
rep hours    = dials needed / dials per hour
```

## 2. Benchmarks to test against

| Metric | Figure | Source and date | Notes |
|-|-|-|-|
| Per-dial connect rate, B2B | 9.9% (campaign exports about 9.2%) | Belkins, 175,000+ dials in 2025 | US 9.0%, UK 14.7% |
| Per-prospect connect rate | 24.5% at about 3 dials per prospect | Belkins 2025 | |
| Connect to conversation | 58% | Belkins 2025 | |
| Conversation to meeting | 4.6% | Belkins 2025 | About 1 meeting per 370 dials (Belkins' own rounded figure; the rates in this table multiply out to about 379) |
| Conversation to meeting | 4.82% | Cognism with WHAM, 2024 figures in the 2025 report | 2025 rate described as almost half of 2024 |
| Conversations by attempt | 93% by attempt 3, 98.6% by attempt 5 | Cognism with WHAM 2025 | Supports Berman's five-attempt cap |
| Average call length | About 93 seconds | Cognism with WHAM 2025 | Meeting-booking calls averaged 3.7 minutes in Belkins 2025 |
| Opener baseline success | About 1.5% | Gong Labs, 90,380 calls, April 2018 | "Success" implied as a booked meeting |
| Gatekeepers among non-bookings | 13.4% | Belkins 2025 | Wrong person or number 13.5% |
| Targeted calls per rep per day | 40 to 60 | alexberman.com/cold-calling-techniques | Berman says this beats 100 generic dials |
| Calls per number per day | 75, recommended | Readymode, June 2025 | A recommendation in Readymode's blog, not a dialer limit; spread volume across enough numbers |

## 3. Local business lists

No benchmark in section 2 covers owner-operated local businesses. Plan a local list with Belkins' B2B rates, labeled in the plan as B2B figures, and replace each with your measured rate. Track decision maker reached as a measured rate from week 1; no published figure was found to start from.

## 4. Call blocks and windows

| Window | Source |
|-|-|
| Avoid 12 to 2pm | Berman: "the one window almost everyone agrees to avoid" |
| Late afternoon, about 4 to 5pm prospect time | Berman: meaningfully better pickup rates |
| 8 to 10am, depending on industry and role; a 9 to 11am block as his example | Berman |
| Heavy dial blocks Tuesday to Thursday; Monday for list building and research | Berman |
| 10 to 11am for the longest calls | Cognism with WHAM 2025 |
| 3 to 4pm and 6pm for the best positive outcome per dial | Belkins 2025 |

Block length and count come from the reps' available hours. Dials per hour depend on the dialer: hand dialing with notes is slower than click-to-call. Measure your own rate in week 1 and size blocks from it.

Rules inside a block: phone only, no inbox; one list segment per block so the reason for the call stays the same; log the disposition before the next dial.

### 4a. Block policy: protect the Golden Hours

Jeb Blount's *Fanatical Prospecting* (Wiley, 2015) gives a section of its time chapter to protecting the "Golden Hours": the part of the day when buyers can be reached belongs to selling, and admin, CRM cleanup and internal meetings go around it. On his Sales Gravy podcast page he puts the selling window at 6 to 8 hours a day. The book's Law of Replacement (chapter 5) says every opportunity that closes or is lost leaves the pipeline and has to be replaced, so prospecting continues after a good week.

| Rule | Setting in this skill |
|-|-|
| Blocks on the calendar | Recurring events marked busy, same times every day, set before the week starts |
| Inside a block | Dialer, script and CRM disposition only; email, chat and internal meetings wait for the admin slot |
| Missed block | Made up the same day or logged as missed in the scorecard |
| After a big week or a closed deal | Same number of blocks next week (Law of Replacement) |
| Replacement target | Meetings needed next week = opportunities that left the pipeline last week / your meeting-to-opportunity rate |

### 4b. Work order inside the day: Reisert's buckets

Ryan Reisert ("Buckets", GTMnow, November 2021) sorts every record into four buckets and works them from the one closest to a meeting backward. He writes: "Getting a meeting scheduled is your only priority in Bucket 3." His buckets, mapped to the CRM fields in section 8:

| Order | Bucket | What is in it | Work | CRM filter |
|-|-|-|-|-|
| 1 | Scheduled (confirm) | Booked meetings | Confirmation touches (section 10) | Meeting date in the next 7 days |
| 2 | Priority (engaged) | People you reached who need a nudge, in-segment inbound, deals lost in the last 2 to 3 quarters | Callback at the agreed time, opening with what they told you | Outcome Activated, Not Now with a date due, or a no-show |
| 3 | Working (in cadence) | In-segment records attempted at least once | Next attempt per the cadence | `attempt_number` 1 to 4, `ready_to_dial` yes |
| 4 | Uncontacted (new) | Typed records never dialed | Check the record and number, then the first dial | `attempt_number` 0 |

Reisert wants Working to be the largest bucket. In practice: confirmations before the first block, Priority callbacks at the start of the block they were promised for, then Working, then new records with what is left.

Sizing: keep enough records in Working for every attempt to land on schedule. Working size per rep = dials per day x business days between attempts. Below one day of dials, load new records before the next block.

### 4c. Attempt cadence per number

Berman: "beyond five attempts on a single prospect with zero engagement, your time is almost always better invested in fresh targets", and his sample sequence runs six touches over about two weeks with calls on day 2, day 5 and day 12. Kixie (June 2023): do not call the same person several times a day. Cognism and WHAM found 93% of conversations by attempt 3. The plan writes its own days into this table:

| Attempt | Business day | Block | Voicemail | Email the same day |
|-|-|-|-|-|
| 1 | Set in the plan | Morning or afternoon | V1 | Refers to the voicemail |
| 2 | Set in the plan, a different block | | None | None |
| 3 | Set in the plan | | V2 | One line and the reason |
| 4 | Set in the plan | | None | None |
| 5 | Inside about two weeks of attempt 1 | | V3 | Short close-the-file email |

After attempt 5 with no conversation, close the record for the cycle, or move it to an email-only sequence whose emails the plan writes out. Never name another routine in the plan without its steps. Rotate blocks so each record gets morning and afternoon attempts; for owner-operated lists, use the logged owner hours.

## 5. Owner hours for local businesses

No published dataset gives owner availability by vertical. Ask the front desk when the owner is in (gatekeeper lines in the scripts file, section 5), log it in `owner_hours`, and dial that record in that window. Until a record has logged hours, use Berman's windows from section 4.

## 6. Dispositions

Map these to your CRM's call outcomes. HubSpot's defaults are Busy, Connected, Left live message, Left voicemail, No answer and Wrong number; add custom outcomes for the rest under Settings, Calling, Call Configurations, Track call outcomes (up to 30, Sales Hub or Service Hub Professional and Enterprise; HubSpot Knowledge Base, checked 2026-10-13). In the plan, name the property for every required field and where it is set in the named CRM.

| Disposition | Counts as connect | Counts as conversation | Next action |
|-|-|-|-|
| No answer | No | No | Next attempt per cadence |
| Busy | No | No | Next business day (one attempt a day) |
| Left voicemail | No | No | Email the same day referencing the voicemail |
| Gatekeeper, message left | Yes | No | Log owner hours; retry in that window |
| Wrong number | Yes | No | Mark number bad; try `find_mobiles` or another source |
| Bad number (disconnected) | No | No | Mark bad; suppress |
| Connected, not decision maker | Yes | No | Ask for the right person; log referral |
| Conversation, not interested | Yes | Yes | Log reason; nurture or close |
| Conversation, follow-up requested | Yes | Yes | Task with date and what they asked for |
| Meeting booked | Yes | Yes | Calendar invite confirmed while they are on the line |
| Asked not to be called | Yes | No | Internal do-not-call entry the same day; stop all channels |

## 7. Conversation outcomes

A disposition records what happened to the dial. An outcome records what the conversation produced. Every dial logged as a conversation gets exactly one outcome, so you can tell a list problem from a script problem.

Joey Gilkey, founder of TitanX, measures outbound on completed conversations rather than meetings booked, with every conversation ending in one of six outcomes (The B2B Playbook, episode 192, September 2025). TitanX's newsletter (April 2026) reports results with the labels Activated, Not Now, Not Me and Referred, and reads activation rates by title to find where the message misses. This skill uses six outcomes built on those labels:

| Outcome | Definition | Next action | Bucket (section 4b) |
|-|-|-|-|
| Meeting Scheduled | Date and time agreed, invite sent during the call | Confirmation runbook (section 10) | Scheduled |
| Activated | Showed intent, intrigue or interest (TitanX's "three I's") but did not book | Callback on the date agreed on the call, opening with what they said | Priority |
| Not Now | Gave a specific later date or event | Task on that date with their reason | Priority, dated |
| Not Me | Does not own the problem and gave no name | Ask once who owns it; flag the title for list review | Working, title flagged |
| Referred | Named the person who owns it | `find_mobiles` or `find_emails` on the referral; add to list v2 with the referrer noted | Uncontacted (new record) |
| Not Interested | Heard the reason and declined | Log the reason and objection number | Closed |

Log a request not to be called as a disposition with no outcome; it ends the record on every channel.

### 7a. Sample size and testing

- The plan sets the conversation count a segment needs before its outcome mix and meeting rate are read. Convert it to dials with the funnel: at Belkins' 2025 rates (9.9% connect, 58% of connects become conversations), N conversations take about N / (0.099 x 0.58) dials, so 50 conversations take about 871.
- Change one lever per test: the list (title, segment, number type), the opener, the reason, or the ask. Log a `test_id` on every call so results stay separate.
- Keep the losing version's numbers so a later test can be compared with it.

### 7b. Reading the mix

| Outcome mix | Read it as | Change |
|-|-|-|
| Not Me plus Referred a large share | List or title problem: the people answering do not own the problem | Change the `title` or `seniority` filter in `query_lead_database`; promote referred titles into list v2 |
| Not Interested high with few Activated | The reason does not fit this segment | New reason, same list |
| Many Activated, few Meeting Scheduled | The ask is weak or too big | Smaller ask, two named times, sell the meeting (`references/call-scripts-and-objections.md` section 2g) |
| Not Now high | No timing trigger in the list | Add a signal filter (`signal-triggered-outbound`) |
| Meetings booked but show rate falling | Booking quality | Section 10 |

TitanX's April 2026 issue gives one example: in the Director-level example, Not Me and Referred made up about 32% of calls (the issue does not make clear whether that is Director calls or all calls), which TitanX read as a pitch aimed at a title that does not own the problem. Fix it either by changing the title on the list or by writing a reason for that title.

### 7c. Referrals feed list v2

1. Each Friday, export the week's Referred outcomes: referred name, title, company, referrer.
2. Run `find_mobiles` (work email or LinkedIn URL) and `find_emails` for the missing fields. $0.25 per mobile found, $0.05 per email found.
3. Count titles across referrals. A title that keeps coming up joins the `title` filter for the next pull.
4. Load the referrals as new records with `referred_by` set, and open the call with the referrer's name.

### 7d. The dated 2-week pilot

Every call plan opens with a 2-week pilot on calendar dates: a baseline week, then a week with one lever changed.

| Week | What runs | Lever changed | Read at the end of the week |
|-|-|-|-|
| 1 (baseline) | The script, list and ask as written | None | Connect rate against the planning rate; conversations so far |
| 2 (one test) | Same list and reps, one lever swapped | Exactly one: the list (title, segment or number type), the opener, the reason or stake, the ask, or the calling window | Conversation-to-meeting and outcome mix against week 1 |

Decision rules the plan writes down before day 1:

| Rule | What the plan sets |
|-|-|
| Connect rate far below the planning rate | The connect floor below which the list or number type gets fixed before any script verdict |
| Sample | The conversation count each week needs before a verdict; extend the week until it gets there |
| Keep the variant | The lift in conversation-to-meeting over baseline that keeps it; the variant becomes the new baseline |
| No clear winner | Keep the baseline (simpler to train); test a different lever next |

Run the two weeks back to back with the same reps and list segment, and tag every call with `test_id` so the halves stay separate. A team too small to reach its sample in a week runs each half for as long as it takes and keeps the dates in the plan.

## 8. CRM fields

| Field | Type | Example |
|-|-|-|
| `call_disposition` | Picklist (section 6) | Gatekeeper, message left |
| `conversation_outcome` | Picklist (section 7), required when the disposition is a conversation | Activated |
| `call_timestamp` | Datetime, recipient local | 2026-10-14 09:42 CT |
| `call_duration_sec` | Integer | 74 |
| `number_dialed` | E.164 | +12145550182 |
| `caller_id_number` | E.164, the number shown to the prospect | +12145550199 |
| `number_type` | owner mobile, direct dial, main line | owner mobile |
| `ready_to_dial` | yes, no | yes |
| `attempt_number` | Integer | 2 |
| `opener_id` | Text | O2 |
| `test_id` | Text, one per test | hvac-dfw-reason-b |
| `segment` | Text | hvac-dfw-41-150-reviews |
| `objection` | Picklist (objection bank numbers) | 2 Send me an email |
| `referred_by` | Contact lookup | Luis Reyes |
| `owner_hours` | Text | in office after 4pm |
| `next_action_date` | Date | 2026-10-16 |
| `removed` | Boolean, set when they asked not to be called | false |

HubSpot's calls API stores the outcome in `hs_call_disposition` as a GUID, duration in `hs_call_duration` in milliseconds, and the dialed number in `hs_call_to_number`.

## 9. Rep scorecard

One row per rep per week, same segment where possible. Every rate is computed from the counts in the same row, so a reader can check it. In a plan written before launch the rows are blank actuals; targets appear once, in Funnel Targets, and are not split by rep.

| Metric | Formula | Starting hypothesis (dated source or measured) |
|-|-|-|
| Dials per day | dials / days worked | Measured dials per hour x block hours; Berman: 40 to 60 targeted calls a day |
| Connect rate | connects / dials | Belkins 2025: 9.9% per dial for B2B |
| Conversations per 100 dials | conversations / dials x 100 | About 5.7 at Belkins 2025 rates (9.9% x 58%) |
| Conversation-to-meeting | meetings / conversations | Belkins 2025: 4.6%; Cognism and WHAM: 4.82% (2024) |
| Dials per meeting | dials / meetings | About 379 at Belkins 2025 rates |
| Show rate | held / meetings whose date has passed | Your own measured show rate on booked demos |

Consistency check: dials per meeting should equal 100 / (conversations per 100 dials x conversation-to-meeting). If a row fails that check, a count is wrong. Compare reps only after each reaches the plan's sample in the same segment; before that, the scorecard is for coaching on dials and dispositions.

### 9a. Targets and first fixes

Targets are the dated benchmarks above or your measured rates. The plan sets the floor for each metric that triggers the first fix.

| Metric | Formula | Starting target | First fix when it falls short |
|-|-|-|-|
| Dials per rep hour | dials / dialing hours | Measured in week 1 | Research or email happening inside blocks |
| Connect rate | connects / dials | B2B 9.9% (Belkins 2025) | Number type, caller ID label, calling window |
| Decision maker reached (local lists) | DM reached / connects | Measured from week 1 | Logged owner hours, ask by name, mobiles first |
| Held past the opener | conversations / connects | 58% (Belkins 2025) | Opener and first 8 to 10 seconds (Berman) |
| Conversation-to-meeting | meetings / conversations | 4.6% (Belkins 2025); 4.82% (Cognism and WHAM, 2024) | Reason, stake or ask |
| Show rate | held / booked, past dates | Your measured show rate | Section 10 runbook |
| Not Me plus Referred | share of conversations | Trend down after a title change | Title filter (section 7b) |
| Working bucket | records with attempts 1 to 4 due | Section 4b sizing | Load new typed records |

Cut every metric by segment, rep, number type (owner mobile, direct dial, main line), block and `test_id`. A blended rate hides the block or number type that fails.

## 10. No-show runbook

Reisert's Scheduled bucket confirms every meeting three times: by phone about a week out, by email 12 to 24 hours before, and, if that email gets no reply, by phone 2 to 3 hours before. A no-show or cancellation goes back to Priority (GTMnow, November 2021). Pessar confirms the email and invite while the prospect is still on the line (Triple Session).

| Touch | When | Channel | Copy |
|-|-|-|-|
| Invite | On the call | Calendar invite plus C1 | C1 below |
| Week-of | About a week before, or right after booking when the meeting is sooner | Phone call | Call |
| 24 hours | 12 to 24 hours before | Email in the invite thread | C2 below |
| 2 to 3 hours | Only when C2 got no reply | Phone call | Call |
| No-show | After the start time passes | One call, then C3 with two new times | C3 below |

The plan writes C1 to C3 in full with merge fields, in the Voicemail, Gatekeeper and Email table:

| ID | Template |
|-|-|
| C1 | "{owner_first}, it's {rep_first} from {company}. Confirmed: {meeting_day} at {meeting_time}, {meeting_length} with {attendee}. The invite went to {email}. Reply here if the time stops working." |
| C2 | Subject: tomorrow at {meeting_time}. "{owner_first}, see you tomorrow at {meeting_time}. We'll cover {problem_they_named} and you'll leave with {meeting_output}. Details are in the invite. {rep_first}" |
| C3 | Subject: new time for {business}? "{owner_first}, we missed each other today. Does {slot_1} or {slot_2} work instead? {rep_first}, {callback_number}" |

Held-meeting rate for the scorecard: held / booked, counting a no-show that reschedules and is held as held.

## 11. Prove calling works before hiring

Before hiring an SDR or buying dialer seats for a team, the founder or first seller runs the motion on one ICP and records outcomes, meetings, show rate, hours spent and cash cost.

Cost per held meeting = (hours spent x loaded hourly cost + data + dialer) / held meetings. Compare it with the same figure for cold email (`outbound-unit-economics`).

| Result | Decision | Hand-over |
|-|-|-|
| Conversation-to-meeting at or above Belkins' 4.6% and cost per held meeting at or below email's | Hire an SDR | Script, list recipe, dialer settings and this scorecard as the ramp target |
| Same result, but no SDR manager and no founder time for daily blocks | Outsource a pilot to a calling agency | Same list recipe and scorecard; agency reports outcomes weekly |
| Below Belkins' rate | Run another test with one lever changed | Decide after the second test |
| Still below after two lever tests, or Not Me plus Referred stays high after a list change | Keep email primary | Phone for Priority callbacks, Activated follow-ups and email replies that ask for a call |

## 12. Weekly review

In the plan, each row below becomes the change half of a Funnel Targets "Act if" cell; the plan carries no second symptom table.

| Symptom | Likely cause | Change |
|-|-|-|
| Connect rate far under the planning rate | Number type (switchboards, dead lines) | Add mobiles via `find_mobiles`; re-pull with `hasContact: true` |
| Connect rate collapses within days on a list that was connecting | Caller ID labelled "Spam Likely" or similar | Check labels and attestation per `references/dialer-and-caller-id.md` section 4; do not swap in fresh numbers |
| Many gatekeeper dispositions | Calling main lines in busy hours | Use logged owner hours; ask the gatekeeper for the best time |
| Conversations far under 58% of connects | Opener | Switch to the permission opener (O2) or a sharper reason |
| Not Me plus Referred a large share of conversations | List or title | Section 7b; feed referrals into list v2 |
| Meetings under 4.6% of conversations | Reason or ask | Tie the reason to a visible fact; offer two times |
| Show rate falling | Booking quality or missing confirmations | Section 10 |
| Many requests not to be called in one segment | Wrong list or opener | Review the segment and the first 10 seconds of recordings |
| One rep far below the others on the same segment | Rep skill or block discipline | Listen to their conversations; check missed blocks |

## 13. Call review and coaching

For a manager with SDRs on recorded, announced calls:

| Item | Setting |
|-|-|
| Launch day | The manager listens live to each rep's first block and gives notes at the break |
| Weekly sample | A set number of recorded conversations per rep each Friday, mixing booked, Not Interested and random calls |
| Score each call yes or no | Name and company in the first sentence; reason cites a fact from the record; stake named; stopped talking after the question; objection answered with a question, then re-ask or exit; ask named two times; next step dated and the invite confirmed on the call; disposition and outcome logged correctly |
| Feedback | One thing to keep and one fix, each tied to a timestamp |
| Practice | Role-play of the fix before Monday's first block; next Friday's sample checks the same item |
| Escalate | The same fix missed week after week, or one rep far under the team's conversation-to-meeting in the same segment: listen to more calls and review block discipline |

## Sources

- https://belkins.io/blog/cold-calling-benchmarks
- https://www.cognism.com/cold-calling-report-2025
- https://www.gong.io/resources/labs/cold-call-opening-lines/
- https://www.gong.io/resources/labs/cold-calling-tips/
- https://alexberman.com/cold-calling-techniques
- https://readymode.com/avoid-being-flagged-as-spam-in-outbound-calls
- https://www.kixie.com/sales-blog/how-to-avoid-showing-up-as-scam-likely-in-outbound-sales/
- https://developers.hubspot.com/docs/api-reference/latest/crm/activities/calls/guide
- https://knowledge.hubspot.com/calling/create-custom-call-and-meeting-outcomes
- https://knowledge.hubspot.com/records/manually-log-activities-on-records
- https://www.oreilly.com/library/view/fanatical-prospecting-the/9781119144755/16_chapter08.html
- https://www.oreilly.com/library/view/fanatical-prospecting-the/9781119144755/13_chapter05.html
- https://salesgravy.com/?p=13248
- https://gtmnow.com/buckets-lead-generation-method/
- https://theb2bplaybook.com/outbound-sales-strategy-b2b
- https://titanx.beehiiv.com/p/cold-call-dispositions-cannot-be-ignored
- https://triplesession.com/session/set-1-meeting-per-day-with-cold-calling
