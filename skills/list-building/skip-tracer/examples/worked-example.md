# Skip Trace Report: Columbus, OH pre-foreclosure owners

Illustrative example. Prepared 2026-10-13 for Brickline Homebuyers, a cash home buyer in Columbus, OH. Plan: Starter ($49/mo). Wallet before run: $88.40. People, addresses and numbers are fictional; phone numbers use the reserved 555-01XX range and emails the `.example` domain.

## Purpose and Channels

| Item | Answer |
|-|-|
| Purpose | Reach owners of homes in pre-foreclosure or scheduled for auction to make cash purchase offers |
| User type | Real estate investor buying for its own account |
| Channels | Direct mail to every owner and live calls by two acquisition reps. Texts and email are off |
| Suppression list | One sheet owned by the acquisitions lead: 4 numbers from past remove requests, loaded into the dialer and the mail file; new requests from any channel added the same day |

## Input Profile

| Class | Identifier | Rows |
|-|-|-|
| A1 | Full property address with ZIP plus owner name, from Franklin County pre-foreclosure filings the user supplied | 300 |
| A2 | Full property address with ZIP, owner unknown, from the Distress List | 150 |
| P, E, N | Phone, email or name-only inputs | 0 |

Six county rows lacked a ZIP; fixed from the USPS ZIP lookup before any search. Pilot: 25 random A1 rows, 19 reached probable or better (76%), so People Finder costs $0.0199 / 0.76 = $0.026 per usable owner against at least $0.25 for Property Lookup with owner contact; People Finder stays first for A1.

## Identifier Plan

| Class | Tool | Parameter | max_results | Rows |
|-|-|-|-|-|
| Feed | Distress List | search Columbus, OH; distressTypes preForeclosure, auction; maxItems 150 | none | 150 |
| A1 | People Finder | street_citystatezip | 1 | 300 |
| A1 rescue | People Finder | name, scored against Columbus, OH | 3 | 71 |
| A2 | Property Lookup | addresses, includeOwnerContact true | none | 150 |

## Cost Estimate

| Line | Units | Unit price | Cost |
|-|-|-|-|
| Distress List, preForeclosure and auction | 150 properties | $0.05 | $7.50 |
| People Finder by address, A1 | 300 billed results | $0.0199 | $5.97 |
| People Finder name rescue, 71 rows at max_results 3 | 189 billed results | $0.0199 | $3.76 |
| Property Lookup with owner contact, A2 | 150 properties | $0.25 | $37.50 |
| Total | | | $54.73 |

User go-ahead: owner approved the $55.21 ceiling in chat on 2026-10-13 (rescue capped at 213 results). Property Lookup with owner contact on all 450 addresses would have cost $112.50 before the Distress List. Cost per owner with a callable phone: $54.73 / 350 = $0.16.

## Match Bands

| Band | Evidence | Count | Use |
|-|-|-|-|
| confirmed | name+address, name+contact, owner_record | 311 | Mail and calls |
| probable | name+city, surname+address, address_only | 75 | Mail; calls open with an identity check |
| weak | name_only, surname+city, tie, entity | 26 | Mail only (12 A1 rows after rescue, 14 A2 rows owned by an LLC or a lender) |
| no_match | none, deceased | 38 | Mail to "Current Owner" at the property; no calls |
| Total searched | | 450 | 300 A1 and 150 A2 |

QA sample (20 confirmed rows against the Franklin County Auditor owner of record, 2026-10-13): owner 19 of 20, address 19 of 20, phone format 20 of 20. The one miss was a co-owner listed under a maiden name (name+address evidence); no evidence type repeated across misses, so the bands hold.

First pass on A1: 171 confirmed, 58 probable, 33 weak, 38 no match. Rescue on those 71 rows: 22 confirmed, 17 probable, 12 weak, 20 no match. A2 via Property Lookup: 118 confirmed (a person returned as owner of record), 14 weak (LLC or lender owner), 18 no match (no owner returned).

## Results Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Input rows | 450 | 0 | 300 county filings and 150 Distress List properties |
| Confirmed or probable after rescue and lookup | 386 | 64 | 26 weak and 38 no match go to mail only |
| With at least one phone | 352 | 34 | No phone in the result |
| With at least one callable phone | 350 | 2 | Every phone on the suppression list |

## Contact Results

| Measure | Count |
|-|-|
| Records confirmed or probable | 386 |
| Records with at least one phone | 352 |
| Phone numbers returned | 611 |
| After E.164 normalization | 604 |
| Line type mobile | 371 |
| Line type landline | 188 |
| Line type VoIP or unknown | 45 |
| On the suppression list | 4 |
| Callable phone numbers | 600 |
| Records with at least one callable phone | 350 |
| Portfolio owners (2 or more input properties) | 11 owners, 26 properties |
| Phones shared by 2 or more unrelated owners, dialed last | 6 |
| Emails returned (not used) | 268 |

## Sample Rows

| input_id | matched_name | match_evidence | match_band | matched_by | phone_1 | phone_1_status |
|-|-|-|-|-|-|-|
| cty-0193 | Darnell Hughes | name+address+contact | confirmed | A1:people_finder:address | +16145550173 | callable |
| cty-0412 | Patricia Moore | name+city | probable | A1:people_finder:address | +16145550129 | callable |
| cty-0088 | Robert Kline | name+city | probable | A1 rescue:people_finder:name | +16145550151 | suppressed |
| dl-0031 | Ellen Park | owner_record | confirmed | A2:property_lookup:owner | +16145550190 | callable |
| cty-0270 | Luis Ortega | surname+city | weak | A1:people_finder:address | +16145550144 | mail_only |
| dl-0107 | Maple Row Holdings LLC | entity | weak | A2:property_lookup:owner | +16145550162 | mail_only |

## Next Steps

1. Mail all 450 properties this week; confirmed and probable owners by name, the rest to "Current Owner".
2. Load the call queue: 600 callable numbers for 350 owners, the 11 portfolio owners first with every address on one call, then confirmed, then probable rows with the identity-check opener. Phones run newest first; the 6 shared lines go last.
3. Set the dialer outcomes before the first block (right party, relative or tenant, wrong number, disconnected, no answer, remove request). After the first block, compare the wrong-party share of probable rows with confirmed rows and of each evidence type, and move any evidence type that carries most wrong parties down a band for next month's run.
4. Log every remove request to the suppression list the same day, every number on the row, in the dialer and the mail file.
5. Look up registered agents for the 9 LLC owners in the Ohio business registry and mail them; mail the 3 estates at the probate address.
6. Run the Distress List every two weeks by ZIP (under 500 properties per run, the team's chosen cadence), new addresses only.
