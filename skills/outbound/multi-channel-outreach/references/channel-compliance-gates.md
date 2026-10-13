# Channel Compliance Gates

Checks to run before a contact enters a phone, LinkedIn or mail touch. Each gate cites the rule it comes from. This is an operating checklist, not legal advice; the full legal background is in `references/outbound-compliance-primer.md`, and anything uncertain goes to counsel.

## 1. Phone gate (US)

Run per number, in order. Stop at the first "drop".

| Step | Question | If yes | If no | Rule |
|-|-|-|-|-|
| 1 | Will the call use an autodialer, a prerecorded message, a ringless voicemail drop or an AI-generated voice? | Drop unless you hold prior express consent for this number | Go to 2 | 47 CFR 64.1200(a)(1)(iii); FCC 2024 ruling on AI voices |
| 2 | Is the number on your internal Do Not Call list, or has the contact opted out on any channel? | Drop | Go to 3 | 47 CFR 64.1200(d) company-specific DNC; internal policy |
| 3 | Is it a mobile or residential number (Mobile Finder results, `contact_mobile`, skip-trace results)? | Go to 4 | Business landline: go to 5 | 47 CFR 64.1200(e) |
| 4 | Is the number on the National DNC Registry (list refreshed within 31 days)? | Drop unless counsel confirms the business-to-business exemption applies to this number and call | Go to 5 | 47 CFR 64.1200(c)(2); FTC TSR Q&A (31 day refresh) |
| 5 | Is the recipient's local time between 9am and 8pm on a weekday? | Go to 6 | Reschedule | 47 CFR 64.1200(c)(1) (8am to 9pm); Florida (8am to 8pm); Texas Bus. & Com. Code 301.051 (9am start) |
| 6 | Has this person had 3 calls about this offer in the last 24 hours? | Reschedule | Call | Florida Telephone Solicitation Act |
| 7 | Does the rep identify themselves and the company at the start, and honor a "don't call me" on the spot? | Call | Train first | TSR disclosure practice; company DNC rule |

Notes:

- The FTC's TSR Q&A says most calls to a business to solicit sales from that business are exempt from the DNC provisions. A mobile found by Mobile Finder may be the owner's personal phone, so this skill scrubs mobiles anyway.
- Penalties are per call: the FTC cites up to $53,088 per violation.
- Texts follow the same consent rules as calls under the TCPA and are covered by Florida's law. This skill does not send cold SMS.
- State rules beyond Florida exist (for example Oklahoma adopted a similar law in 2022). Check the states on your list in the compliance primer.

## 2. Phone gate outside the US

| Country | Rule summary | Default here |
|-|-|-|
| Canada | National DNCL and CRTC telemarketing rules apply to calls; CASL governs email | Scrub the DNCL; email under CASL consent rules |
| UK | Live B2B calls are allowed unless the number is on the TPS or CTPS, or the business objected | Screen TPS and CTPS before calling |
| EU | Varies by country; many require opt-in for calls to individuals | Email only unless counsel approves |

## 3. Dialing method matrix

| Method | Allowed on cold mobiles without consent? | Why |
|-|-|-|
| Rep dials by hand or click-to-call, one line at a time | Generally yes, after the gate | Live, non-automated call |
| Power dialer that dials the next number when the rep is ready | Ask counsel; keep it rep-initiated and one line at a time | Autodialer definitions vary by state |
| Parallel or predictive dialer | No | Higher autodialer risk; abandoned calls |
| Prerecorded voicemail drop | No | Artificial or prerecorded voice |
| AI voice agent | No | FCC treats AI voices as artificial |

## 4. LinkedIn gate

| Check | Rule | Source |
|-|-|-|
| All views, connection requests and messages are sent by a person in the LinkedIn interface | LinkedIn's User Agreement bars bots and unauthorized automated methods, including automated messages | LinkedIn User Agreement 8.2, as quoted by Contentin (2026) |
| No browser extension or cloud tool automates actions | LinkedIn's prohibited software page names extensions that automate activity and warns of account restriction | Same |
| Connection volume stays modest and steady | LinkedIn keeps its weekly invitation limit unpublished; community estimates sit near 100 a week | Contentin glossary, July 2026 |
| Connection note has no pitch and no link | Recipients ignore or report pitch-first requests | Practice |
| Stop on reply anywhere | One stop rule across channels | Internal policy |

## 5. Direct mail gate

| Check | Rule |
|-|-|
| Address is a business address (Local Business Database `address`, Maps listing) | Mail freely; include a way to opt out |
| Address is a residence (property owners from `scrape_property_lookup` or `scrape_distress_list`) | Mail only a relevant, respectful offer; never reference financial distress in a way that shames; follow state rules for real estate solicitations; offer opt-out |
| Contact opted out on email or phone | Do not mail |
| Mail piece names a person | Use the name from the record; do not guess |
| Offer and claims | Same truth standards as email; no fake checks or official-looking envelopes |

Public-record and skip-trace data is for prospecting and research. Never use it for employment, tenant, credit or insurance decisions, which fall under the FCRA (see `references/scrapercity-platform.md`).

## 6. Email inside a multichannel cadence

Email touches keep every CAN-SPAM element: accurate headers, non-deceptive subject, postal address, working opt-out honored within 10 business days. An email opt-out stops calls and mail as well.

## 7. Gate record per contact

| Field | Example |
|-|-|
| Contact | Tom Reyes, Reyes Air, Plano TX |
| Number type | Mobile (Mobile Finder) |
| Internal DNC | Clear, checked 2026-10-13 |
| National DNC | Clear, registry file dated 2026-10-01 |
| Dialing method | Click-to-call, live rep |
| Window | 9am to 8pm Central (Texas 9am start) |
| Calls in last 24h | 0 |
| Gate result | Pass |

## Sources

- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr
- https://cooley.com/news/insight/2024/2024-02-15-fcc-ai-generated-robocalls-illegal-under-the-tcpa
- https://www.jonesday.com/en/insights/2021/07/florida-makes-significant-changes-to-telemarketing-laws
- https://contentin.io/blog/linkedin-mcp-terms-of-service/
- https://contentin.io/glossary/weekly-invitation-limit/
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://crtc.gc.ca/eng/com500/faq500.htm
- https://scrapercity.com/terms
