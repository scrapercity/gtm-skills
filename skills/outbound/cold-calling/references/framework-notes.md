# Framework Notes: Cold Calling

Which named sources shape this skill, what each one contributes, how strong the evidence is, and which file to open for each question.

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| Gong Labs, "cold call opening lines" (90,380 first-interaction calls, published April 2018, page updated March 2026) | Baseline success about 1.5%; "the reason for my call" 2.1x; "how are you?" 3.4x; "how have you been?" 6.6x; "did I catch you at a bad time?" about 40% lower | Opener rules, script | Vendor dataset, AI-analyzed recordings |
| Gong Labs with 30 Minutes to President's Club (300M+ calls, July 2024) | Updated opener table: "heard the name tossed around?" 11.24%, tailored permission opener 11.18%, "how's your day going?" 7.6%, "bad time?" 2.15% | Opener variants | Vendor dataset; success not defined on the page |
| Gong Labs, cold calling tips | Successful calls run about twice as long; prospect monologues 3.5 seconds in successful calls vs 8 in unsuccessful; more speaker switches | Question design, pacing | Vendor dataset, method not stated |
| Jeb Blount, telephone prospecting framework (InsideSales interview, August 2017) | Use the name, identify yourself and the reason, give a reason to keep talking, ask, then stop talking | Script structure | Practitioner teaching |
| Armand Farrokh and Nick Cegelski, 30 Minutes to President's Club | Co-authors of the 2024 Gong opener study; the permission opener and "heard the name" opener | Opener variants | Practitioner teaching plus vendor data |
| Alex Berman, cold calling techniques (page dated Aug 2026) | Script the structure; voicemail under 30 seconds with the number twice; five attempts over about two weeks then move on; mobile over switchboard (can double connects); read rates over 50+ dials; avoid 12 to 2pm, 4 to 5pm picks up better, heavy blocks Tuesday to Thursday; 8 to 10 seconds before the prospect checks out; "timing or fit?" for not interested | Script, voicemail, attempts, windows, objections | Operator teaching |
| Readymode, "avoid being flagged as spam" (June 2025) | Recommends limiting outbound volume to 75 calls per day per number (a recommendation, not a dialer limit); hold enough numbers to spread volume; monitor caller ID reputation | Dials per number, numbers per rep | Dialer vendor documentation |
| Kixie, "avoid showing up as Scam Likely" (June 2023) | Do not call the same person several times a day; rotate numbers through the day | Attempt cap per day | Dialer vendor documentation |
| National Center for Voice and Speech, via Voices.com | US conversational speech runs about 150 words a minute | 75-word voicemail cap (30 seconds) | Research center figure cited by a vendor |
| Cognism with WHAM, State of Cold Calling 2025 | 41,936 connected calls and 27,513 conversations in 2025; 4.82% conversation-to-meeting in 2024; 93% of conversations by attempt 3, 98.6% by attempt 5; average call about 93 seconds | Attempt cadence, meeting rate hypothesis | Agency dataset |
| Belkins, B2B cold calling benchmarks (175,000+ dials in 2025) | 9.9% per-dial connect, 24.5% per-prospect connect, 58% connect-to-conversation, 4.6% conversation-to-meeting; gatekeepers 13.4% of non-bookings | Funnel hypotheses, gatekeeper planning | Agency dataset |
| HubSpot calls API | Default call outcomes: Busy, Connected, Left live message, Left voicemail, No answer, Wrong number | CRM logging | Vendor documentation |
| Jeb Blount, *Fanatical Prospecting* (Wiley, 2015) and Sales Gravy podcast | "Protect the Golden Hours" (chapter 8) and the Law of Replacement (chapter 5): selling hours go to prospecting, and pipeline that leaves must be refilled | Block policy | Practitioner book |
| Joey Gilkey, TitanX founder (The B2B Playbook ep. 192, Sept 2025) and TitanX newsletter (April 2026) | Completed conversations as the outbound metric; six outcomes per conversation; labels Activated, Not Now, Not Me, Referred; activation read by title | Conversation outcomes, diagnosis | Founder interview, vendor newsletter |
| Ryan Reisert, "Buckets" (GTMnow, Nov 2021) | Four buckets worked from Scheduled back to Uncontacted; confirm a week out by phone, 12 to 24 hours by email, 2 to 3 hours by phone; no-shows return to Priority | Work order, no-show runbook | Practitioner article |
| Ronen Pessar (Sell Better, The Sales Doctor ep. 43, Triple Session, Mixmax interview 2023) | Pick-up, conversation, interest, meeting; qualify with a present-tense closed question; confirm the invite on the call; set tone to the role | If-they-engage beats, tonality | Practitioner podcasts and training |
| Tom Slocum, The SD Lab | A cold call earns the next conversation; summarize the problem, say what the meeting covers, ask for one step; relevance over personal detail | Selling the meeting, 3x3 rules | Practitioner articles |
| Steve Richard (Vorsight, ExecVision) | 3x3 Research: three insights in three minutes (Call Camp, April 2016) | Pre-call research | Practitioner training |
| ATIS-1000074 | Attestation levels A, B, C | Caller ID reputation | Industry standard |
| State and local open data portals (Texas Open Data Portal, Texas Comptroller, state license files, City of Austin, Dallas Central Appraisal District) | Permit, license, inspection, tax and appraisal records that date openings and changes | Public records triggers, fresh-opening list | Government publishers (not ScraperCity data) |
| Free Caller Registry (First Orion, Hiya, TNS) and Hiya blog (Aug 2023) | Free number registration for the analytics engines behind AT&T, Verizon and T-Mobile; no guarantee against labels | Caller ID reputation | Vendor documentation |

## Routing

| Question | Open |
|-|-|
| What do I look up before dialing? | `references/call-scripts-and-objections.md` section 0 (3x3) |
| What do I say in the first 20 seconds? | `references/call-scripts-and-objections.md` section 1 |
| They engaged. What next? | `references/call-scripts-and-objections.md` section 2g |
| How do I answer "send me an email" or "we're all set"? | `references/call-scripts-and-objections.md` section 3 |
| What do I leave on voicemail, what do I tell the front desk? | `references/call-scripts-and-objections.md` sections 4 and 5 |
| Which numbers do I dial first, and when? Which dialer settings? How many dials per number? | `references/dialer-and-caller-id.md` sections 1 to 3 |
| How many dials for N meetings? What rates should I expect? | `references/call-blocks-and-metrics.md` sections 1 and 2 |
| How do I protect call blocks and order the day's work? | `references/call-blocks-and-metrics.md` sections 4a and 4b |
| Which hours get the most connects? When are local owners reachable? | `references/call-blocks-and-metrics.md` sections 4 and 5 |
| Which dispositions, outcomes and CRM fields? | `references/call-blocks-and-metrics.md` sections 6 to 8 |
| How do I score reps, stop no-shows, decide whether to hire? | `references/call-blocks-and-metrics.md` sections 9 to 11 |
| Our numbers show "Spam Likely". What now? | `references/dialer-and-caller-id.md` section 4 |
| Where do I find new openings, permits, inspections, building age? | `references/public-records-triggers.md` |
| What stake should the offer name for this vertical? | `references/call-scripts-and-objections.md` section 2h |
| How do I set up the 2-week pilot and its decision rules? | `references/call-blocks-and-metrics.md` section 7d |
| Which days and blocks get attempts 1 to 5? How big should Working be? | `references/call-blocks-and-metrics.md` sections 4b and 4c |
| What target and first fix for each metric? | `references/call-blocks-and-metrics.md` section 9a |
| How should a manager review calls each week? | `references/call-blocks-and-metrics.md` section 13 |
| How do I type objections and pre-handle the top one? | `references/call-scripts-and-objections.md` sections 3 and 3a |
| `find_mobiles` and database parameters, prices | `references/scrapercity-catalog.md`, `references/scrapercity-platform.md` |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Openers | Gong 2018 favored "how have you been?"; Gong 2024 favored "heard the name tossed around?" and a permission opener | Use the permission opener or a direct "reason I'm calling". "How have you been?" implies a past relationship that does not exist, so this skill does not use it. |
| Attempts | Berman: five or more then move on; Cognism and WHAM: 93% of conversations by attempt 3 | Up to 5 attempts over about two weeks (Berman), one a day at most (Kixie) |
| Best time | Berman's page: late afternoon, avoid 12 to 2pm; Cognism and WHAM: 10 to 11am longest calls; Belkins: 3 to 4pm and 6pm best positive outcome per dial | Test two of these windows per segment and keep the one with the higher connect rate |
| Funnel rates | Belkins 4.6% conversation-to-meeting; Cognism and WHAM 4.82% (2024); Gong baseline success 1.5% (definition differs) | Plan with Belkins' 2025 rates; replace each with your measured rate |
| Sample size | Berman: read rates over 50+ dials; no source gives a conversation count for outcome mix | The plan sets its sample per test, never under Berman's 50 dials |
| Reachability scoring | Vendor phone-intent products claim connect rates far above blind lists; no independent study was found | Rank by number type, past connects and fresh triggers from your own data; measure connect rate per number type |
| Questions per call | Some playbooks call for 11 to 14 discovery questions; Gong found shorter prospect monologues and more back-and-forth in successful calls, and Slocum keeps diagnosis for the meeting | Two or three questions, then the ask |
| Metric bands | Weak, average and strong bands circulate without a dataset behind them | Dated benchmarks or measured rates; the plan sets each action floor (section 9a of the metrics file) |
| Calls per number | Readymode recommends 75 a day; no other dialer page found gives a figure | The plan's cap at or under 75 a day per number, cited as Readymode's recommendation |
| Owner hours by vertical | No dataset found | Logged per record from the front desk |

## Sources

- https://www.gong.io/resources/labs/cold-call-opening-lines/
- https://www.gong.io/resources/labs/the-best-and-worst-cold-call-openers-backed-by-data-from-300m-calls/
- https://www.gong.io/resources/labs/cold-calling-tips/
- https://www.insidesales.com/secrets-of-phone-prospecting-jeb-blount/
- https://alexberman.com/cold-calling-techniques
- https://www.cognism.com/cold-calling-report-2025
- https://belkins.io/blog/cold-calling-benchmarks
- https://developers.hubspot.com/docs/api-reference/latest/crm/activities/calls/guide
- https://scrapercity.com/mobile-finder
- https://www.oreilly.com/library/view/fanatical-prospecting-the/9781119144755/
- https://gtmnow.com/buckets-lead-generation-method/
- https://theb2bplaybook.com/outbound-sales-strategy-b2b
- https://titanx.beehiiv.com/p/cold-call-dispositions-cannot-be-ignored
- https://sellbetter.xyz/daily-show/how-to-run-a-successful-cold-call-from-opener-to-booked-meeting
- https://www.mixmax.com/blog/interview-ronen-pessar
- https://www.thesdlab.com/cold-calling
- https://x.com/srichardv/status/724894945027436545
- https://www.freecallerregistry.com/
- https://readymode.com/avoid-being-flagged-as-spam-in-outbound-calls
- https://www.kixie.com/sales-blog/how-to-avoid-showing-up-as-scam-likely-in-outbound-sales/
- https://www.voices.com/tools/words_to_time_conversion
- https://comptroller.texas.gov/transparency/open-data/recent-sales-tax-permits
- https://www.tdlr.texas.gov/LicenseSearch/licfile.asp
