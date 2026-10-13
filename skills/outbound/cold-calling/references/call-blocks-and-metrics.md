# Call Blocks and Metrics

Funnel formulas, dated benchmarks, block schedules, owner hours for local businesses, and the CRM fields that make the program measurable. Every benchmark here is a starting hypothesis with its source and date. Replace each rate with your own after 300 dials in a segment.

## 1. The funnel

| Stage | Definition used in this skill | Formula |
|-|-|-|
| Dial | Any outbound attempt, any outcome | count |
| Connect | A live human picked up (includes gatekeepers, wrong person, not interested) | connects / dials |
| Decision maker reached | The connect was the person you want (local lists only) | DM reached / connects |
| Conversation | The person engaged past the opener | conversations / connects (or / DM reached) |
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
| Conversation to meeting | 4.6% | Belkins 2025 | About 1 meeting per 370 dials |
| Conversation to meeting | 4.82% | Cognism with WHAM, 2024 figures in the 2025 report | 2025 rate described as almost half of 2024 |
| Conversations by attempt | 93% by attempt 3, 98.6% by attempt 5 | Cognism with WHAM 2025 | Drives the 5 attempt cap |
| Average call length | About 93 seconds | Cognism with WHAM 2025 | Meeting-booking calls averaged 3.7 minutes in Belkins 2025 |
| Opener baseline success | About 1.5% | Gong Labs, 90,380 calls, April 2018 | "Success" implied as a booked meeting |
| Gatekeepers among non-bookings | 13.4% | Belkins 2025 | Wrong person or number 13.5% |
| Targeted calls per rep per day | 40 to 60 | alexberman.com/cold-calling-techniques | Berman says this beats 100 generic dials |

No benchmark in this table covers owner-operated local businesses specifically. For local lists, start with the planning assumptions in section 3 and label them as assumptions in the plan.

## 3. Planning assumptions for local business lists

These are not benchmarks. They are the starting numbers this skill uses when no data exists yet, chosen to be conservative, and each must be replaced after 300 dials.

| Stage | Starting assumption | Replace with |
|-|-|-|
| Connect (someone answers the listed number) | 25% | Your connects / dials |
| Decision maker reached, of connects | 40% | Your DM reached / connects |
| Conversation, of DM reached | 58% (Belkins B2B figure) | Your conversations / DM reached |
| Meeting, of conversations | 6% | Your meetings / conversations |
| Held, of meetings | 75% | Your held / booked |

## 4. Call blocks

Default schedule for one full-time rep, times in the prospect's local time:

| Block | Time | Length | Focus |
|-|-|-|-|
| Prep | 8:30 to 9:00 | 30 min | Load the gated list, read the first 10 records, check callbacks due |
| Block 1 | 9:00 to 10:30 | 90 min | First attempts on new records |
| Admin | 10:30 to 11:00 | 30 min | Follow-up emails promised on calls, CRM notes |
| Block 2 | 2:00 to 3:30 | 90 min | Second and third attempts, callbacks |
| Block 3 (dedicated SDR) | 4:00 to 5:30 | 90 min | Late-day window; Berman's page and Belkins both report late afternoon working |

Dials per hour depend on the dialer: hand dialing with notes is slower than click-to-call. Measure your own rate in week one and size blocks from it.

Rules inside a block: phone only, no inbox; one list segment per block so the reason for the call stays the same; log the disposition before the next dial.

## 5. Owner hours for local businesses

House starting points from operating practice, with no measured data behind them. Log the hours a front desk gives you (section 7 of the scripts file) and override these per record.

| Vertical | Call | Avoid | Why |
|-|-|-|-|
| HVAC, plumbing, electrical, roofing | 9:00 to 10:00, 4:00 to 6:00 | 10:00 to 3:00 (owners on job sites) | Owners dispatch early and close out late |
| Dental, medical, veterinary | 12:00 to 1:30 if the practice closes for lunch; 4:30 to 5:30 | First hour of patient schedule | Front desk is buried at open |
| Restaurants | 2:00 to 4:00 | 11:00 to 1:30, 5:00 onward | Between lunch and dinner service |
| Salons, spas, barbers | 9:00 to 10:00 before first appointment | Saturdays | Owner is often working a chair |
| Law, accounting, insurance | 9:00 to 11:00, 3:00 to 5:00 | Tax season deadlines for accountants | Office hours |
| Auto repair | 9:30 to 11:00, 2:00 to 3:30 | Opening and closing rush | Drop-off and pickup |

Every window still sits inside the gate's 9am to 8pm weekday window.

## 6. Dispositions

Map these to your CRM's call outcomes. HubSpot's defaults are Busy, Connected, Left live message, Left voicemail, No answer and Wrong number; add custom outcomes for the rest.

| Disposition | Counts as connect | Counts as conversation | Next action |
|-|-|-|-|
| No answer | No | No | Next attempt per cadence |
| Busy | No | No | Retry later the same day if under the cap |
| Left voicemail | No | No | Email the same day referencing the voicemail |
| Gatekeeper, message left | Yes | No | Log owner hours; retry in that window |
| Wrong number | Yes | No | Mark number bad; try `find_mobiles` or another source |
| Bad number (disconnected) | No | No | Mark bad; suppress |
| Connected, not decision maker | Yes | No | Ask for the right person; log referral |
| Conversation, not interested | Yes | Yes | Log reason; nurture or close |
| Conversation, follow-up requested | Yes | Yes | Task with date and what they asked for |
| Meeting booked | Yes | Yes | Calendar invite within 5 minutes |
| DNC requested | Yes | No | Company DNC entry the same day; stop all channels |

## 7. CRM fields

| Field | Type | Example |
|-|-|-|
| `call_disposition` | Picklist (section 6) | Gatekeeper, message left |
| `call_timestamp` | Datetime, recipient local | 2026-10-14 09:42 CT |
| `call_duration_sec` | Integer | 74 |
| `number_dialed` | E.164 | +12145550182 |
| `number_class` | business, consumer | consumer |
| `gate_result` | pass, drop, reschedule | pass |
| `attempt_number` | Integer | 2 |
| `opener_id` | Text | O2 |
| `segment` | Text | hvac-dfw-41-150-reviews |
| `objection` | Picklist (objection bank numbers) | 2 Send me an email |
| `owner_hours` | Text | in office after 4pm |
| `next_action_date` | Date | 2026-10-16 |
| `dnc` | Boolean | false |

HubSpot's calls API stores the outcome in `hs_call_disposition` as a GUID, duration in `hs_call_duration` in milliseconds, and the dialed number in `hs_call_to_number`.

## 8. Weekly review

| Symptom after 300 dials in a segment | Likely cause | Change |
|-|-|-|
| Connect rate under half the assumption | Number type (switchboards, dead lines) | Add mobiles via `find_mobiles`; re-pull with `hasContact: true` |
| Many gatekeeper dispositions | Calling main lines in busy hours | Use logged owner hours; ask the gatekeeper for the best time |
| Conversations under 40% of DM reached | Opener | Switch to the permission opener (O2) or a sharper reason |
| Meetings under 3% of conversations | Reason or ask | Tie the reason to a visible fact; offer two times |
| Held under 60% of booked | Booking quality | Confirm by email the same day; book within 5 business days |
| DNC requests over 2% of connects | Wrong list or tone | Review the segment and the first 10 seconds of recordings |

## Sources

- https://belkins.io/blog/cold-calling-benchmarks
- https://www.cognism.com/cold-calling-report-2025
- https://www.gong.io/resources/labs/cold-call-opening-lines/
- https://www.gong.io/resources/labs/cold-calling-tips/
- https://alexberman.com/cold-calling-techniques
- https://developers.hubspot.com/docs/api-reference/latest/crm/activities/calls/guide
