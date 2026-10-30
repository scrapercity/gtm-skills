# Local Business List Plan: independent dental practices in the Denver, CO metro

Illustrative example. Prepared 2026-10-13 for Peakline Growth, an agency selling new-patient campaigns. Use: cold email and calls. Plan: none yet (new account). The agency, sample names and `.example` domains are invented; the NPI Registry counts are real.

**Status: Plan.** The ScraperCity tools were not connected in this session, so nothing paid has run. The NPI Registry counts were measured on 2026-10-13 from the free public API; every other count arrives on the date named in Run Schedule.

## Short Answer

| Question | Answer |
|-|-|
| How many practices | 1,151 dental organizations with a practice address in the 14 sub-cities, per the NPI Registry: 874 general practices and 277 specialists. Group-run offices come out in the independence screen on 2026-10-14, before any paid step |
| How many you can email and call | Counted on 2026-10-14 from the Local Business Database pull and sent to you with a resized ceiling. The call file holds every independent location with a phone; the email file holds those with a validated address, one row per owner |
| What it costs | All-in for a new account: $149 for one month of Growth, which carries $159 of usage credit. Usage ceiling: $116.93, sized on the 1,151 practices, plus $1.19 per Google Maps run in a sub-area under your coverage target. Website Finder and Email Finder charge only per contact found, so spend lands below the ceiling |
| Your time | Review of rows the independence screen flags, owner-name conflicts, and the hand check of a random sample; the row counts come with the 2026-10-14 report |
| How it is checked | NPI coverage per sub-area, an independence screen before any paid lookup, one validation pass, a hand check of a random sample, and a 100-email test cell |

## Decisions

1. Specialists: kept and tagged by NPI taxonomy (orthodontics, oral surgery, pediatric, periodontics, endodontics), since you asked for every practice. Say "general only" and the 277 come out before enrichment.
2. Chain line: how many locations make a brand a group. Groups found on a group's own office list or named on the homepage come out either way. Send any group names you already know.
3. Coverage target: the share of each sub-area's NPI practices the list must match before Maps spend stops.
4. Hand check: sample size and the pass line per check.
5. Suppression: current clients, open deals and past contacts, matched on domain and phone.
6. Your offer: it decides which segment gets the first 100 emails.
7. Owner mobiles: not included. Mobile Finder on owner emails costs $0.25 per number found, nothing when not found.

## Search Definition

| Field | Value |
|-|-|
| Category words | dentist, dental clinic, cosmetic dentist, pediatric dentist |
| Excluded categories | Dental laboratory, Dental supply store, Dental school |
| Area | The 14 sub-cities under Coverage |
| Email file | Own-domain website and a validated email; one row per owner |
| Call file | Phone and full address; one row per location, with an empty `call_outcome` |
| Independence | Group list built on 2026-10-14 from the national groups' Colorado location pages, Heartland Dental's supported-office announcements (it lists new offices under their own practice names) and names you send; homepage text naming a group; NPI official with a corporate title |
| Owner name | NPI authorized official titled Owner, President or DDS/DMD, confirmed against that dentist's own NPI license record; then a database or Website Finder contact titled Owner. Colorado's business register files no officers or managers (Topograph's Colorado register notes), so it is not an owner source here |

## Coverage

Measured 2026-10-13: NPI Registry organization records with a dentist taxonomy and a practice address in the sub-city. Maps runs only where the database matches fewer of these than your coverage target. A sub-area with more practices than one Maps term returns (60, Google's text search maximum) runs by ZIP from the start.

| Sub-area | NPI practices | General | Specialist | Maps method if under target |
|-|-|-|-|-|
| Denver | 302 | 244 | 58 | By ZIP, 32 ZIPs |
| Aurora | 176 | 139 | 37 | By ZIP, 11 ZIPs |
| Lakewood | 104 | 81 | 23 | By ZIP, 9 ZIPs |
| Littleton | 89 | 62 | 27 | By ZIP, 6 ZIPs |
| Centennial | 75 | 51 | 24 | By ZIP, 6 ZIPs |
| Westminster | 67 | 50 | 17 | By ZIP, 8 ZIPs |
| Parker | 60 | 39 | 21 | One run |
| Arvada | 54 | 40 | 14 | One run |
| Castle Rock | 49 | 35 | 14 | One run |
| Thornton | 48 | 33 | 15 | One run |
| Highlands Ranch | 37 | 25 | 12 | One run |
| Broomfield | 37 | 29 | 8 | One run |
| Englewood | 30 | 27 | 3 | One run |
| Golden | 23 | 19 | 4 | One run |
| Total | 1,151 | 874 | 277 | At most 80 runs |

## Segments

Counts arrive with the 2026-10-14 report. Cutoffs are yours; the ones shown are starting values to change.

| Segment | Rule | Send order |
|-|-|-|
| named_contact | Personal address of a named person | 1: first-name copy |
| role_inbox | info@, office@, frontdesk@ | 2: copy addressed to the practice |
| few_reviews | Under 20 Google reviews | First if the offer is reviews or local SEO |
| high_rated_busy | Rating 4.6 or higher with 200 or more reviews | First if the offer is capacity: hiring, scheduling, financing |
| new_practice | NPI enumeration date in the last 12 months | First if the offer is a launch: website, equipment, marketing setup |
| multi_location | Same owner on 2 or more locations | One email per owner; the call file keeps every location |

## Cost

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Local Business Database counts and pull | Every match | Included in Growth | $0.00 |
| NPI Registry matching | 14 sub-cities | Free | $0.00 |
| Website Finder, "Office Manager", domains with no email | up to 1,151 domains | $0.0499 per contact found | $57.43 |
| Email Finder, owner name plus domain where only a role inbox exists | up to 1,151 lookups | $0.05 per email found | $57.55 |
| Email Validator, every unique email once | up to 1,151 emails | $0.00169 | $1.95 |
| Usage ceiling before Maps | | | $116.93 |
| Google Maps, one run of 2 terms at 60 each | 120 places | $0.0099 | $1.19 |

The ceiling is resized on 2026-10-14 from the database count. The $159 credit leaves $42.07 after the ceiling, enough for 35 Maps runs before any extra credit is bought.

## Checks

| Check | When | Pass line | If it fails |
|-|-|-|-|
| NPI coverage per sub-area | 2026-10-14, after the pull | Your coverage target | Maps by the method in Coverage |
| Maps cap | Each Maps run | No term returns at 60 (Google's text search maximum) | Split that area by ZIP |
| Independence screen | Before any paid lookup | Every dropped row names its signal | Add the brand and re-run the screen |
| Owner check | After owner lookups | Owner name matches a licensed dentist's NPI record | Mark the row as a conflict for hand review |
| Dedupe | Before validation | No repeated domain, phone or email in the email file; no repeated phone in the call file | Fix the key order and re-run |
| Hand check | Before handoff | Your sample size and pass line, reported as N of M per check | Fix the filter and re-run on every row |
| Test cell | First send | 100 emails to one segment (Alex Berman's first-test size); pause at 2% hard bounces over 200 sends (Berman's line, Instantly's 200-send window) | Pause, re-validate, trace the bounced rows to their source |

## Run Schedule

| Date | Step | Cost | Who approves |
|-|-|-|-|
| 2026-10-14 | Plan and wallet check, database counts per sub-area, full pull, NPI match, independence screen; report back with real counts and a resized ceiling | $0 | Nothing to approve |
| 2026-10-15 | Website Finder, Email Finder and Email Validator | Up to the resized ceiling | You approve the 2026-10-14 report |
| 2026-10-15 | Google Maps in sub-areas under your target | $1.19 per run | You approve the run list |
| 2026-10-16 | Owner check, dedupe, hand check, three files delivered | $0 | Nothing to approve |
| 2026-10-19 | First 100 emails; first call blocks with the outcome field set up | Your sending tools | You approve the segment and copy |

## Output Columns

| Column | Example | Rule |
|-|-|-|
| business_name | Sloan's Lake Family Dental | As listed |
| owner_name | Dr. Dana Whitfield | Only from a source that names the owner; blank otherwise |
| owner_check | confirmed | confirmed (NPI license match), conflict, or blank |
| owner_key | dana whitfield, sloans lake dental pllc | One per owner; the email file holds one row per key |
| email | dana@sloanslakedental.example | Owner's address when found and valid, else the practice inbox |
| email_status | valid | Only valid in the main file |
| phone | +13035550142 | Main line, E.164 |
| subtype | general | general, or the NPI specialty |
| independence | pass | pass, or the signal that removed the row |
| segment | named_contact;few_reviews | Base segment plus tags |
| npi | 1234567893 | Organization NPI, stored as text |
| call_outcome | owner_reached | owner_reached, gatekeeper, referred, corporate, wrong_number, closed, not_interested, remove_request |

Sequencer import: email, first name from owner_name or contact_name ("Dr." and credentials removed; a blank name reads "Hi there"), business_name, city, segment. Dialer import: phone, business_name, owner_name, segment, rating, reviews and call_outcome, on Mountain time. A `corporate` outcome adds the parent group to the independence screen; a remove request is suppressed in every tool the same day.
