# Mobile Append Report: IT leaders at US hospitals, 100 to 1,000 employees

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Prepared 2026-10-13 for Sentrygate (sentrygate.example), a cybersecurity vendor whose SDR team runs a manual call blitz the week of 2026-10-19. Plan: Starter ($49/mo). Wallet before run: $96.40. Dialing method: click-to-call from the sales engagement tool, one call at a time, live reps only. Names and companies are fictional and use the reserved `.example` domain; phone numbers use the reserved 555-01XX range.

## Input Summary

| Input type | Rows | Notes |
|-|-|-|
| LinkedIn URLs | 300 | Saved lead list of IT Directors, CIOs and IT Managers |
| Work emails | 40 | Webinar registrants with no LinkedIn URL |
| Dropped before append | 14 | 8 duplicate people, 4 company pages, 2 Sales Navigator links |
| Sent to Mobile Finder | 326 | 286 URLs and 40 emails, one input per person |

## Call Plan

| Question | Answer | Action |
|-|-|-|
| Dialing method | Click-to-call from the sales engagement tool, one call at a time, live reps | Line-type lookup on every number so reps only see mobiles |
| Suppression list | One list synced from the sequencer, the dialer and the CRM, 1,240 rows | Matched before the pilot and again on every found number |
| Countries | United States only | `+1` country code; tz from each person's city and state |
| Line-type lookups | All 119 found numbers, on the team's own carrier lookup account | Landline, VoIP and unknown go to hold_line_type |
| Destination | Sales engagement tool for the blitz; CRM mobile field afterwards | Only line_type = mobile rows go to the CRM field |

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
| Mobile Finder pilot | 50 inputs, 18 found | $0.25 per number found | $4.50 |
| Mobile Finder main run | 276 inputs, 101 found | $0.25 per number found | $25.25 |
| Email Validator on the 40 email inputs, for the follow-up email step | 40 emails | $0.0072 | $0.29 |
| Total actual | | | $30.04 |

User go-ahead: SDR manager approved the $69.00 ceiling in chat on 2026-10-13 after a wallet check showed $91.90 left after the pilot, enough to cover the ceiling. Billed separately and not in the total: 119 line-type lookups on the team's own carrier lookup account. Cost per dial-ready mobile: $30.04 / 102 = $0.29.

## Append Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Rows received | 340 | 0 | Starting point |
| After dedupe | 332 | 8 | Same person on two rows; kept the LinkedIn URL |
| After input normalization | 326 | 6 | 4 company pages and 2 Sales Navigator links |
| Mobiles found | 119 | 207 | No number found; not billed |
| After E.164 and shared-number check | 117 | 2 | One number listed on two people, an office line |
| After line-type check | 104 | 13 | 6 nonFixedVoip, 3 fixedVoip, 2 landline, 2 unknown |
| After suppression list | 102 | 2 | Earlier removal requests |
| Dial-ready, callable | 102 | 0 | Final calling list |

## Line Type and Suppression

| Check | Count | Result |
|-|-|-|
| mobile | 104 | Kept |
| voip_nonfixed | 6 | hold_line_type, review by hand |
| voip_fixed | 3 | hold_line_type, likely desk direct dials |
| landline | 2 | hold_line_type |
| unknown | 2 | hold_line_type |
| Shared number | 2 | hold_shared_number |
| Suppression list matches | 2 | hold_suppressed, permanent, checked 2026-10-13 |

## Dial Rules

| dial_status | Count | Allowed use |
|-|-|-|
| callable | 102 | Click-to-call inside the team's call window, prospect's local time |
| hold_suppressed | 2 | Never dialed |
| hold_line_type | 13 | Rep reviews; may move desk lines to the phone column |
| hold_shared_number | 2 | Moved to company phone; not a personal mobile |

## Output Schema

| Column | Example | Rule |
|-|-|-|
| mobile | +15125550142 | E.164, stored as text |
| input_used | linkedin_url | Identifier that found the number |
| line_type | mobile | From the carrier lookup |
| suppressed | no | yes, no, unchecked |
| suppression_checked_at | 2026-10-13 | Date of the last match against the suppression list |
| tz | America/Chicago | From person location, not area code |
| dial_status | callable | Four-value vocabulary |
| source | mobile_finder | Controlled vocabulary |

## Sample Rows

| Name | Company | Input used | Mobile | Line type | Suppressed | dial_status |
|-|-|-|-|-|-|-|
| Priya Natarajan | Coastal Health (coastalhealth.example) | linkedin_url | +15125550142 | mobile | no | callable |
| Marcus Bell | Riverbend Medical (riverbend.example) | linkedin_url | +13035550117 | mobile | no | callable |
| Jorge Alvarez | Coastal Health (coastalhealth.example) | email | +13055550188 | mobile | no | callable |
| Helen Sato | Prairie Regional (prairieregional.example) | linkedin_url | +16125550163 | mobile | yes | hold_suppressed |
| Owen Fitch | Lakeside Clinics (lakeside.example) | linkedin_url | +14145550109 | voip_fixed | no | hold_line_type |

## Next Steps

1. Load the 102 callable rows into the sales engagement tool with tz mapped and the dialer set to click-to-call.
2. SDRs review the 13 hold_line_type rows; desk direct dials move to the phone column.
3. Move the 2 shared numbers to the company phone column and run a decision-maker search on those accounts.
4. Add anyone who asks not to be called to the suppression list the same day and sync it to the sequencer and CRM.
5. After the first week of dials, compare connect rate by local hour and move the call window to the best hours.
