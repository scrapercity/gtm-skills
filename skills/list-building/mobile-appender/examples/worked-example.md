# Mobile Append Report: IT leaders at US hospitals, 100 to 1,000 employees

Prepared 2026-10-13 for Sentrygate, a cybersecurity vendor whose SDR team runs a manual call blitz the week of 2026-10-19. Plan: Starter ($49/mo). Wallet before run: $96.40. Dialing method: click-to-call from the sales engagement tool, one call at a time, live reps only. Names and companies are fictional and use the reserved `.example` domain; phone numbers use the reserved 555-01XX range.

## Input Summary

| Input type | Rows | Notes |
|-|-|-|
| LinkedIn URLs | 300 | Saved lead list of IT Directors, CIOs and IT Managers |
| Work emails | 40 | Webinar registrants with no LinkedIn URL |
| Dropped before append | 14 | 8 duplicate people, 4 company pages, 2 Sales Navigator links |
| Sent to find_mobiles | 326 | 286 URLs and 40 emails, one input per person |

## Compliance Gate

| Question | Answer | Law | Action |
|-|-|-|-|
| Dialing method | Click-to-call, human dials each number, live voice | TCPA, 47 U.S.C. 227(b) | Live reps on click-to-call only; prerecorded voice, AI voice, ringless voicemail and predictive dialing are switched off |
| Texts | None planned, no text consent on file | TCPA, 47 CFR 64.1200 | sms_allowed = no on every row |
| Recipients | IT leaders called about their employer's security program; numbers are personal mobiles | TSR B2B exemption; 47 CFR 64.1200(c) and (e); Chennette v. Porch.com | Scrub against the National DNC Registry; hold registered numbers, counsel has not cleared them |
| Calling hours | 8 a.m. to 9 p.m. in each person's local time | 47 CFR 64.1200(c)(1) | tz set from person city and state |
| Internal do-not-call list | Kept in the sales engagement tool | 47 CFR 64.1200(d) | Scrubbed after append; same-day adds during the blitz |
| State law | 9 callable contacts in Florida | Florida Telephone Solicitation Act | Manual calls only, no texts |

## Cost Estimate

Pilot: 50 inputs, 18 found, hit rate 36%.

| Scenario | Inputs | Hit rate | Numbers found | Cost |
|-|-|-|-|-|
| Low | 276 | 20% | 55 | $13.75 |
| Expected | 276 | 36% | 99 | $24.75 |
| High | 276 | 50% | 138 | $34.50 |
| Ceiling | 276 | 100% | 276 | $69.00 |

| Line | Units | Unit price | Cost |
|-|-|-|-|
| find_mobiles pilot | 50 inputs, 18 found | $0.25 per number found | $4.50 |
| find_mobiles main run | 276 inputs, 101 found | $0.25 per number found | $25.25 |
| validate_emails on the 40 email inputs, for the follow-up email step | 40 emails | $0.0072 | $0.29 |
| Total actual | | | $30.04 |

User go-ahead: SDR manager approved the $69.00 ceiling in chat on 2026-10-13 after a wallet check showed $91.90 left after the pilot, enough to cover the ceiling. Billed separately and not in the total: Registry access (the team's 4 target area codes fall inside the free five) and 119 line-type lookups on the team's own carrier lookup account. Cost per dial-ready mobile: $30.04 / 73 = $0.41.

## Append Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Rows received | 340 | 0 | Starting point |
| After dedupe | 332 | 8 | Same person on two rows; kept the LinkedIn URL |
| After input normalization | 326 | 6 | 4 company pages and 2 Sales Navigator links |
| Mobiles found | 119 | 207 | No number found; not billed |
| After E.164 and shared-number check | 117 | 2 | One number listed on two people, an office line |
| After line-type check | 104 | 13 | 6 nonFixedVoip, 3 fixedVoip, 2 landline, 2 unknown |
| After internal do-not-call list | 102 | 2 | Earlier opt-outs |
| After National DNC Registry scrub | 73 | 29 | Registered numbers held |
| Dial-ready, callable_manual | 73 | 0 | Final calling list |

## Line Type and DNC

| Check | Count | Result |
|-|-|-|
| mobile | 104 | Kept |
| voip_nonfixed | 6 | hold_line_type, review by hand |
| voip_fixed | 3 | hold_line_type, likely desk direct dials |
| landline | 2 | hold_line_type |
| unknown | 2 | hold_line_type |
| Shared number | 2 | hold_shared_number |
| Internal do-not-call matches | 2 | hold_internal_dnc, permanent |
| National DNC Registry matches | 29 | hold_dnc, checked 2026-10-13 |

## Dial Rules

| dial_status | Count | Allowed use |
|-|-|-|
| callable_manual | 73 | Live manual or click-to-call, 8 a.m. to 9 p.m. local |
| callable_auto_consented | 0 | No consent records |
| hold_dnc | 29 | Not dialed unless counsel clears B2B calls to registered mobiles |
| hold_internal_dnc | 2 | Never dialed |
| hold_line_type | 13 | Rep reviews; may move desk lines to the phone column |
| hold_shared_number | 2 | Moved to company phone; not a personal mobile |

## Output Schema

| Column | Example | Rule |
|-|-|-|
| mobile | +15125550142 | E.164, stored as text |
| input_used | linkedin_url | Identifier that found the number |
| line_type | mobile | From the carrier lookup |
| dnc_status | clear | clear, national, state, internal |
| dnc_checked_at | 2026-10-13 | Must be within 31 days of the first dial |
| tz | America/Chicago | From person location, not area code |
| dial_status | callable_manual | Six-value vocabulary |
| sms_allowed | no | yes only with text consent |
| source | mobile_finder | Controlled vocabulary |

## Sample Rows

| Name | Company | Input used | Mobile | Line type | DNC status | dial_status | sms_allowed |
|-|-|-|-|-|-|-|-|
| Priya Natarajan | Coastal Health (coastalhealth.example) | linkedin_url | +15125550142 | mobile | clear | callable_manual | no |
| Marcus Bell | Riverbend Medical (riverbend.example) | linkedin_url | +13035550117 | mobile | clear | callable_manual | no |
| Jorge Alvarez | Coastal Health (coastalhealth.example) | email | +13055550188 | mobile | clear | callable_manual | no |
| Helen Sato | Prairie Regional (prairieregional.example) | linkedin_url | +16125550163 | mobile | national | hold_dnc | no |
| Owen Fitch | Lakeside Clinics (lakeside.example) | linkedin_url | +14145550109 | voip_fixed | clear | hold_line_type | no |

## Next Steps

1. Load the 73 callable_manual rows into the sales engagement tool with tz mapped, call windows enforced, and the dialer set to click-to-call only.
2. Send the 29 hold_dnc rows to counsel with the Chennette summary; until cleared, those contacts get email and LinkedIn touches only.
3. SDRs review the 13 hold_line_type rows; desk direct dials move to the phone column.
4. Re-scrub any number not dialed by 2026-11-12 (31 days after the scrub).
5. Log every opt-out to the internal list the same day and keep it for 5 years.
