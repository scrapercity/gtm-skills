# Local Business List Report: dentists in the Austin, TX metro

Prepared 2026-10-13 for Brightchair Marketing, an agency selling patient-acquisition campaigns to independent dental practices. Use: cold email, first test to one sub-segment. Plan: Growth ($149/mo). Wallet before run: $158.90. Business names, domains and emails are fictional and use the reserved `.example` domain.

## Search Definition

| Field | Value |
|-|-|
| keyword | dentist, dental clinic, cosmetic dentist, pediatric dentist |
| notCategory | Dental laboratory, Dental supply store |
| Area | Austin, TX metro split into 10 sub-cities (Travis, Williamson and Hays counties) |
| Must have | Website with a real domain, an email that validates |
| Nice to have | Named contact (`hasContact`), used for personalization when present |
| Exclusions and suppression | 11 current agency clients (domain and phone), dental schools, practices emailed by the agency in the last 90 days |
| Chain policy | One row per email: group practices that share one inbox across locations collapse to one row |

## Geography Split

| Sub-area | All businesses (A) | With website and email (C) | Email coverage | Action |
|-|-|-|-|-|
| Austin | 761 | 498 | 65.4% | Database only |
| Round Rock | 118 | 74 | 62.7% | Database only |
| Cedar Park | 83 | 52 | 62.7% | Database only |
| Georgetown | 66 | 41 | 62.1% | Database, plus a Yelp spot check |
| Pflugerville | 47 | 27 | 57.4% | Maps gap fill |
| Leander | 34 | 19 | 55.9% | Maps gap fill |
| Kyle | 31 | 16 | 51.6% | Maps gap fill |
| Buda | 18 | 9 | 50.0% | Maps gap fill |
| San Marcos | 39 | 22 | 56.4% | Yelp gap fill (dense Yelp listings near the university) |
| Lakeway | 17 | 10 | 58.8% | Database only |
| Total | 1,214 | 768 | 63.3% | Gap threshold: under 58.3% (5 points below the metro average) |

`searched_as` read all 10 places as cities in Texas; no keyword came back `matches_nothing`.

## Count Check

| Call | Filters | pagination.total | Decision |
|-|-|-|-|
| A | keyword, location, notCategory | 1,214 | Market size for the metro |
| B | plus hasWebsite | 1,093 | 325 businesses have a website but no email in the database |
| C | plus hasEmail | 768 | Pull all 768 (8 pages of 100 with after cursors) |
| D | plus hasContact | 402 | 402 of the 768 carry a named contact; used for the first-name variant of the email |

User go-ahead: approved in chat on 2026-10-13 after seeing the table above and the $9.59 ceiling for scrapes and validation.

## Source Results

| Source | Inputs | Returned | New after dedupe | Cost |
|-|-|-|-|-|
| Local Business Database (call C) | 10 sub-cities, 4 keywords | 768 | 768 | $0.00 |
| scrape_maps | Pflugerville, Leander, Kyle, Buda; "dentist", "dental clinic"; cap 40 per term | 228 | 37 | $2.26 |
| scrape_yelp | "dentist" in San Marcos and Georgetown; searchLimit 30 | 58 | 5 | $0.57 |
| scrape_website_finder | 26 new domains with no email; jobTitle "Office Manager" | 15 | 15 | $0.75 |

Maps returned under its cap of 40 for every term in every sub-city, so no further split was needed. The Maps start responses reported no extra `local_business_database` matches the account did not already have.

## Cleaning Funnel

| Stage | Rows | Change | Reason |
|-|-|-|-|
| Local Business Database pull | 768 | 0 | Call C, every row has a website and an email |
| Add Maps businesses | 805 | +37 | 228 returned, 191 already in the pool by phone, domain or name plus ZIP |
| Add Yelp businesses | 810 | +5 | 58 returned, 53 already in the pool |
| Drop rows with no website | 802 | -8 | 7 Maps and 1 Yelp listings with only a Facebook page or no site |
| Drop rows still without an email | 791 | -11 | Website Finder found no contact on 11 of the 26 domains |
| Drop wrong category or closed | 782 | -9 | 6 dental labs or supply stores that matched "dental", 3 marked permanently closed |
| Dedupe on email | 768 | -14 | Group practices using one inbox for several locations |
| Suppression | 734 | -34 | 11 agency clients, 23 practices emailed in the last 90 days |
| Send-ready after validation | 561 | -173 | 103 catch-all to their own file, 21 unknown held, 46 invalid and 3 disposable removed |

## Validation Results

| Status | Count | Share | Action |
|-|-|-|-|
| valid | 561 | 76.4% | Main CSV; 214 of them are role addresses (info@, office@), kept on a local list |
| valid_catch_all | 103 | 14.0% | Catch-all file, sent at no more than 10% of daily volume after the main file shows bounces under 2% |
| unknown | 21 | 2.9% | Re-validate once on 2026-10-16 |
| invalid | 46 | 6.3% | Removed, added to the sequencer blocklist |
| disposable | 3 | 0.4% | Removed, added to the blocklist |
| Total validated | 734 | 100% | One `validate_emails` run, `emailCount` 734 |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Local Business Database counts and pull | 768 businesses | Included in Growth plan | $0.00 |
| scrape_maps | 228 businesses | $0.0099 | $2.26 |
| scrape_yelp | 58 results | $0.0099 | $0.57 |
| scrape_website_finder | 15 contacts found | $0.0499 | $0.75 |
| validate_emails | 734 emails | $0.0072 | $5.28 |
| Total paid usage | | | $8.86 |

Cost per send-ready practice: $8.86 / 561 = $0.016. Wallet after run: $150.04.

## Output Schema

| Column | Example | Rule |
|-|-|-|
| business_name | Barton Creek Family Dentistry | As listed |
| business_name_key | barton creek family dentistry | Lowercase, punctuation and legal suffix removed |
| category | Dentist | Primary category from the source |
| website | https://www.bartoncreekdental.example/ | As listed |
| domain | bartoncreekdental.example | Registrable domain; blank for platform hosts |
| email | info@bartoncreekdental.example | Lowercased |
| email_status | valid | Only valid in the main file |
| email_validated_at | 2026-10-13 | ISO date |
| is_role | true | Role addresses kept on this local list |
| phone | +15125550143 | E.164 |
| contact_name | Dr. Alicia Moreno | From the database contact fields or Website Finder |
| street, city, state, postal_code | 3801 Bee Caves Rd, Austin, TX, 78746 | ZIP stored as text |
| rating, reviews | 4.8, 312 | From the source |
| sub_area | Austin | Sub-city from the geography split |
| source | local_db | local_db, maps, yelp, joined with a pipe when merged |
| source_detail | local_db:keyword=dentist...;location=10 sub-cities;hasEmail | Query fingerprint or run id |

## Sample Rows

| business_name | domain | email | email_status | phone | city | source |
|-|-|-|-|-|-|-|
| Barton Creek Family Dentistry | bartoncreekdental.example | info@bartoncreekdental.example | valid | +15125550143 | Austin | local_db |
| Round Rock Smiles | roundrocksmiles.example | amorales@roundrocksmiles.example | valid | +15125550188 | Round Rock | local_db |
| Plum Creek Dental | plumcreekdental.example | office@plumcreekdental.example | valid | +15125550121 | Kyle | maps |
| Pflugerville Pediatric Dentistry | pflugervillekidsdds.example | frontdesk@pflugervillekidsdds.example | valid | +15125550167 | Pflugerville | local_db |
| Riverside Dental San Marcos | riversidedentalsm.example | kim.tran@riversidedentalsm.example | valid | +15125550109 | San Marcos | yelp |

QA sample: 20 random rows opened on 2026-10-13; 19 were independent practices matching the listing, 1 was a practice that had moved to a new suite in the same building (kept, address updated).

## Next Steps

1. Start with one sub-segment: the send-ready practices with a named contact (402 before cleaning), first-name personalization, about 100 sends a day; widen to role addresses only after the first 300 sends show bounces under 2%.
2. Re-validate the 21 unknown rows on 2026-10-16 and schedule a monthly `excludeDelivered: true` pull for new practices in the same 10 sub-cities.
