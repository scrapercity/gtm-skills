# Local Business List: dentists in the Austin, TX metro

Illustrative example. Prepared 2026-10-13 for Brightchair Marketing, an agency selling patient-acquisition campaigns to independent dental practices. Use: cold email. Plan: Growth ($149/mo). Business names, domains and emails are invented and use the reserved `.example` domain; counts are illustrative.

**Status: Delivered.** Every count below comes from the run on 2026-10-13.

## Short Answer

| Question | Answer |
|-|-|
| How many you can email | 545 independent practices with a validated email, 337 of them with a named contact |
| How big the market is | 1,214 dental listings in the Local Business Database across 10 sub-cities; every sub-city now matches 88% or more of its NPI Registry practices |
| What is held back | 100 catch-all addresses in their own file; 20 unknown, re-validated on 2026-10-16 |
| What it cost | $8.71 in usage, inside the Growth plan's $159 monthly credit: $0.016 per send-ready practice |
| What to send first | 100 emails to named_contact practices tagged few_reviews, starting 2026-10-14 |

## Search Definition

| Field | Value |
|-|-|
| Category words | dentist, dental clinic, cosmetic dentist, pediatric dentist |
| Excluded categories | Dental laboratory, Dental supply store, Dental school |
| Area | 10 sub-cities across Travis, Williamson and Hays counties |
| Must have | Website on its own domain, an email that validates |
| Scope | Specialists kept and tagged in `subtype` (Brightchair's choice) |
| Independence | Brands on 5 or more locations (Brightchair's chain line), Brightchair's list of 9 Texas groups, and homepage text naming a group |
| Suppression | 11 current clients (domain and phone), practices Brightchair emailed in the last 90 days |
| Chain policy | One row per email: practices that share one inbox across locations collapse to one row |

## Coverage

Gap line: email coverage under 58.3%, 5 points below the metro average of 63.3% (Brightchair's setting). NPI target: 85% of the sub-area's NPI organization dentists matched (Brightchair's setting).

| Sub-area | Database (A) | With website and email (C) | NPI matched, before and after | Action |
|-|-|-|-|-|
| Other 5 sub-areas (Austin, Round Rock, Cedar Park, Georgetown, Lakeway) | 1,045 | 675 | 91% to 94% | None |
| Pflugerville | 47 | 27 | 66% to 89% | Maps, 2 terms |
| Leander | 34 | 19 | 64% to 88% | Maps, 2 terms |
| Kyle | 31 | 16 | 71% to 90% | Maps, 2 terms |
| Buda | 18 | 9 | 68% to 88% | Maps, 2 terms |
| San Marcos | 39 | 22 | 79% to 86% | Yelp (dense listings near the university) |
| Total | 1,214 | 768 | | |

## Funnel

| Stage | Rows | Change | Reason |
|-|-|-|-|
| Database rows with a website and an email | 768 | 0 | Start of the email file |
| Add Maps businesses | 805 | +37 | 228 returned, 191 already in the pool by phone, domain or name plus ZIP |
| Add Yelp businesses | 810 | +5 | 58 returned, 53 already in the pool |
| Drop rows with no website | 802 | -8 | Facebook page or no site |
| Drop wrong category or closed | 793 | -9 | 6 labs or supply stores, 3 permanently closed |
| Drop group-run locations | 771 | -22 | 14 on Brightchair's group list, 8 whose homepage says "supported by" a group |
| Drop rows still without an email | 760 | -11 | Website Finder found no contact on 11 of 26 domains |
| Dedupe on email | 747 | -13 | Practices sharing one inbox across locations |
| Suppression | 713 | -34 | 11 clients, 23 emailed in the last 90 days |
| Send-ready after validation | 545 | -168 | Only valid addresses stay; the split is below |

## Validation Results

| Status | Count | Share | Action |
|-|-|-|-|
| valid | 545 | 76.4% | Main file; 208 role addresses (info@, office@) stay, since the owner often reads them |
| catch_all | 100 | 14.0% | Own file and campaign |
| unknown | 20 | 2.8% | Re-validate once on 2026-10-16 |
| invalid | 45 | 6.3% | Removed and blocklisted |
| disposable | 3 | 0.4% | Removed and blocklisted |
| Total validated | 713 | 100% | One Email Validator run |

## Segments

| Segment | Rule | Rows | Send order |
|-|-|-|-|
| named_contact | Personal address with a contact name | 337 | 1: first-name copy |
| role_inbox | info@, office@, frontdesk@ | 208 | 2: copy addressed to the practice |
| few_reviews | Under 20 Google reviews (Brightchair's cutoff) | 72 | First inside each base segment |
| multi_location | Same domain on 2 to 4 locations | 17 | One email per owner |

## Cost

| Item | Units | Unit price | Cost | New rows | Cost per new |
|-|-|-|-|-|-|
| Local Business Database counts and pull | 768 businesses | Included in Growth | $0.00 | 768 | $0.00 |
| Google Maps, 4 sub-cities x 2 terms, cap 40 | 228 businesses | $0.0099 | $2.26 | 37 | $0.061 |
| Yelp, San Marcos and Georgetown, 30 each | 58 results | $0.0099 | $0.57 | 5 | $0.114 |
| Website Finder, "Office Manager" on 26 domains | 15 contacts found | $0.0499 | $0.75 | 15 | $0.050 |
| Email Validator | 713 emails | $0.0072 | $5.13 | - | - |
| Total usage | | | $8.71 | | |

The approved ceiling was $9.59. Yelp cost about twice as much per new practice as Maps, so the next refresh skips Yelp for dentists. Wallet after the run: $150.19.

## Checks

| Check | Pass line | Result |
|-|-|-|
| Count reconciliation | Pulled rows equal the count; sub-areas sum to the total | 768 pulled, 768 counted |
| NPI coverage | 85% per sub-area (Brightchair's setting) | Every sub-area 86% or more after gap fills |
| Maps cap | No term returns at its cap of 40 | Highest term returned 34 |
| Dedupe | No duplicate domain, phone or email | 0 duplicates |
| QA sample, 20 random rows | 18 of 20 per check (Brightchair's setting) | Category fit 20 of 20, open at the listed address 19 of 20 (one suite change, fixed), own-domain website 20 of 20, phone E.164 20 of 20 |
| Catch-all start | Main file hard bounces under 2% over its first 200 sends (Alex Berman's 2% line, Instantly's 200-send window) | Measured after the first 200 sends |

## Output Columns

| Column | Example | Rule |
|-|-|-|
| business_name | Barton Creek Family Dentistry | As listed |
| business_name_key | barton creek family dentistry | Lowercase, punctuation and legal suffix removed |
| domain | bartoncreekdental.example | Registrable domain; blank for platform hosts |
| email | info@bartoncreekdental.example | Lowercased |
| email_status | valid | Only valid in the main file |
| is_role | true | Role addresses kept on this local list |
| phone | +15125550143 | E.164 |
| contact_name, contact_title | Dr. Alicia Moreno, Owner | Database contact or Website Finder |
| subtype | general | general, or the NPI specialty |
| street, city, state, postal_code | 3801 Bee Caves Rd, Austin, TX, 78746 | ZIP stored as text |
| rating, reviews | 4.8, 312 | From the source |
| segment | role_inbox;few_reviews | Base segment plus tags |
| source | local_db | local_db, maps, yelp, website_finder, joined with a pipe |

Files: `local-dentists-austin-tx-2026-10-13.csv` (main) and `local-dentists-austin-tx-2026-10-13-catch-all.csv`.

## Next Steps

1. 2026-10-14: import the main file to the sequencer with email, first name from contact_name ("Dr." removed; a blank name reads "Hi there"), business_name, city and segment. One campaign per base segment. The first 100 sends go to named_contact practices tagged few_reviews, Alex Berman's first-test size for one segment.
2. 2026-10-16: re-validate the 20 unknown rows.
3. After the first 200 sends: open role_inbox, then the catch-all campaign, if hard bounces stay under 2% (Berman's line).
4. 2026-11-13: re-run the same database search for new practices only, and re-validate any row older than 90 days before it is sent (ZeroBounce recommends verifying at least quarterly).
