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
| Alex Berman, cold calling techniques | Script the structure; voicemail under 30 seconds with the number twice; five attempts then move on; mobile over switchboard; judge on 50+ dials; "timing or fit?" for not interested | Script, voicemail, attempts, objections | Operator teaching |
| Cognism with WHAM, State of Cold Calling 2025 | 41,936 connected calls and 27,513 conversations in 2025; 4.82% conversation-to-meeting in 2024; 93% of conversations by attempt 3, 98.6% by attempt 5; average call about 93 seconds | Attempt cadence, meeting rate hypothesis | Agency dataset |
| Belkins, B2B cold calling benchmarks (175,000+ dials in 2025) | 9.9% per-dial connect, 24.5% per-prospect connect, 58% connect-to-conversation, 4.6% conversation-to-meeting; gatekeepers 13.4% of non-bookings | Funnel hypotheses, gatekeeper planning | Agency dataset |
| FCC, 47 CFR 64.1200 | Hours, National DNC, company DNC, wireless consent, abandoned calls, revocation | Compliance gate | Federal regulation |
| FCC Declaratory Ruling FCC 24-17 (Feb 2024) | AI-generated voices are artificial voices under the TCPA | Dialing method rule | Federal ruling |
| FTC, Telemarketing Sales Rule 16 CFR 310.6(b)(7) | B2B sales calls exempt from most of the TSR, including DNC, except nondurable office and cleaning supplies | B2B vs consumer decision | Federal regulation |
| Florida 501.059 and 501.616, Oklahoma HB 3168, Maryland 2023 ch. 413, Texas 301.051 and SB 140 | Hours (8pm stop; Texas 9am start), 3 calls per 24 hours, broader automated-system rules, private suits | State hours table | State statutes |
| HubSpot calls API | Default call outcomes: Busy, Connected, Left live message, Left voicemail, No answer, Wrong number | CRM logging | Vendor documentation |

## Routing

| Question | Open |
|-|-|
| What do I say in the first 20 seconds? | `references/call-scripts-and-objections.md` section 1 |
| How do I answer "send me an email" or "we're all set"? | `references/call-scripts-and-objections.md` section 3 |
| What do I leave on voicemail, what do I tell the front desk? | `references/call-scripts-and-objections.md` sections 4 and 5 |
| Can I call this number, and when? | `references/dialing-compliance-gate.md` |
| What does the law say in full (TCPA, CASL, PECR, FCRA)? | `references/outbound-compliance-primer.md` |
| How many dials for N meetings? What rates should I expect? | `references/call-blocks-and-metrics.md` sections 1 and 2 |
| When are owners of restaurants, dental offices or contractors reachable? | `references/call-blocks-and-metrics.md` section 4 |
| Which dispositions and CRM fields? | `references/call-blocks-and-metrics.md` section 5 |
| `find_mobiles` and database parameters, prices | `references/scrapercity-catalog.md`, `references/scrapercity-platform.md` |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Openers | Gong 2018 favored "how have you been?"; Gong 2024 favored "heard the name tossed around?" and a permission opener | Use the permission opener or a direct "reason I'm calling". "How have you been?" implies a past relationship that does not exist, so this skill does not use it. |
| Attempts | Berman: five or more then move on; Cognism and WHAM: 93% of conversations by attempt 3 | Up to 5 attempts over 10 business days; judge reachability after 3 |
| Best time | Berman's page: late afternoon, avoid 12 to 2pm; Cognism and WHAM: 10 to 11am longest calls; Belkins: 3 to 4pm and 6pm best positive outcome per dial | Test two windows per segment; 6pm only where state hours allow and the recipient's local time is before 8pm |
| Funnel rates | Belkins 4.6% conversation-to-meeting; Cognism and WHAM 4.82% (2024); Gong baseline success 1.5% (definition differs) | Start at about 4.5% conversation-to-meeting, replace after 300 dials |
| B2B mobiles and DNC | TSR exempts B2B calls; FCC rules protect residential and wireless subscribers | Scrub every wireless number; treat sole-proprietor mobiles as consumer |

## Sources

- https://www.gong.io/resources/labs/cold-call-opening-lines/
- https://www.gong.io/resources/labs/the-best-and-worst-cold-call-openers-backed-by-data-from-300m-calls/
- https://www.gong.io/resources/labs/cold-calling-tips/
- https://www.insidesales.com/secrets-of-phone-prospecting-jeb-blount/
- https://alexberman.com/cold-calling-techniques
- https://www.cognism.com/cold-calling-report-2025
- https://belkins.io/blog/cold-calling-benchmarks
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf
- https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.6
- https://sll.texas.gov/faqs/how-late-can-telemarketers-call
- http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.616.html
- https://developers.hubspot.com/docs/api-reference/latest/crm/activities/calls/guide
- https://scrapercity.com/mobile-finder
