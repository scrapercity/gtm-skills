# Skip Trace Report: Columbus, OH pre-foreclosure owners

Prepared 2026-10-13 for Brickline Homebuyers, a cash home buyer in Columbus, OH. Plan: Starter ($49/mo). Wallet before run: $88.40. People, addresses and numbers are fictional; phone numbers use the reserved 555-01XX range and emails the `.example` domain.

## Purpose and Permissible Use

| Item | Answer |
|-|-|
| Purpose | Reach owners of homes in pre-foreclosure or scheduled for auction to make cash purchase offers |
| User type | Real estate investor buying for its own account |
| Channels | Direct mail to every owner and manual live calls by two acquisition reps. Texts, dialer automation and email are off |
| FCRA statement | Results are prospecting and contact data under the FCRA boundary. They are not used for any tenant, employment, credit or insurance decision and are not stored in a screening system |

## Input Profile

| Class | Identifier | Rows |
|-|-|-|
| A1 | Full property address with ZIP plus owner name, from Franklin County pre-foreclosure filings the user supplied | 300 |
| A2 | Full property address with ZIP, owner unknown, from scrape_distress_list | 150 |
| P, E, N | Phone, email or name-only inputs | 0 |

Six county rows lacked a ZIP; fixed from the USPS ZIP lookup before any search. Pilot: 25 random A1 rows, 19 reached probable or better (76%), so People Finder stays first for A1.

## Identifier Plan

| Class | Tool | Parameter | max_results | Rows |
|-|-|-|-|-|
| Feed | scrape_distress_list | search Columbus, OH; distressTypes preForeclosure, auction; maxItems 150 | none | 150 |
| A1 | find_people | street_citystatezip | 1 | 300 |
| A1 rescue | find_people | name, scored against Columbus, OH | 3 | 71 |
| A2 | scrape_property_lookup | addresses, includeOwnerContact true | none | 150 |

## Cost Estimate

| Line | Units | Unit price | Cost |
|-|-|-|-|
| scrape_distress_list, preForeclosure and auction | 150 properties | $0.05 | $7.50 |
| find_people by address, A1 | 300 billed results | $0.0199 | $5.97 |
| find_people name rescue, 71 rows at max_results 3 | 189 billed results | $0.0199 | $3.76 |
| scrape_property_lookup with owner contact, A2 | 150 properties | $0.25 | $37.50 |
| Total | | | $54.73 |

User go-ahead: owner approved the $55.21 ceiling in chat on 2026-10-13 (rescue capped at 213 results). Property Lookup with owner contact on all 450 addresses would have cost $112.50 before the Distress List. Cost per owner with a callable phone: $54.73 / 241 = $0.23.

## Match Scoring

| Band | Score range | Count | Use |
|-|-|-|-|
| confirmed | 80 to 100 | 290 | Mail and manual calls after DNC scrub |
| probable | 60 to 79 | 96 | Mail; calls open with an identity check |
| weak | 40 to 59 | 26 | Mail only (12 A1 rows after rescue, 14 A2 rows owned by an LLC or a lender) |
| no_match | 0 to 39 | 38 | Mail to "Current Owner" at the property; no calls |
| Total searched | | 450 | 300 A1 and 150 A2 |

First pass on A1: 171 confirmed, 58 probable, 33 weak, 38 no match. Rescue on those 71 rows: 22 confirmed, 17 probable, 12 weak, 20 no match. A2 via Property Lookup: 97 confirmed, 21 probable, 14 weak, 18 no match.

## Results Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Input rows | 450 | 0 | 300 county filings and 150 Distress List properties |
| Confirmed or probable after rescue and lookup | 386 | 64 | 26 weak and 38 no match go to mail only |
| With at least one phone | 352 | 34 | No phone in the result |
| With at least one callable phone | 241 | 111 | Every phone on the National DNC Registry or the internal list |

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
| On the National DNC Registry (scrubbed 2026-10-13) | 233 |
| On the internal do-not-call list | 4 |
| Callable phone numbers | 367 |
| Records with at least one callable phone | 241 |
| Emails returned (not used) | 268 |

## Compliance Check

| Item | Answer | Law | Action |
|-|-|-|-|
| Purpose | Purchase offers to owners in pre-foreclosure | FCRA, 15 U.S.C. 1681b | No tenant, employment, credit or insurance use |
| Calls | Two reps dialing by hand, live voice | TCPA, 47 U.S.C. 227(b) | No autodialer, prerecorded or AI voice; no texts |
| DNC | Registry and internal list scrubbed 2026-10-13 | FTC TSR; 47 CFR 64.1200(c) and (d) | 237 numbers removed; re-scrub by 2026-11-12 |
| Calling hours | Eastern time | 47 CFR 64.1200(c)(1) | 8 a.m. to 9 p.m. |
| Offer content | Cash purchase offers only | Regulation O, 12 CFR 1015 | No claims about stopping the foreclosure |
| State | Ohio | Ohio SB 155 | Wholesaler disclosure form before any assignable contract |
| Entities and estates | 9 LLC owners, 5 lender-owned, 3 deceased flags | FCRA and TSR scope | Entities mailed at the registered address; estates contacted through probate only |

## Sample Rows

| input_id | matched_name | match_score | match_band | matched_by | phone_1 | phone_1_dnc | phone_1_status |
|-|-|-|-|-|-|-|-|
| cty-0193 | Darnell Hughes | 100 | confirmed | A1:find_people:address | +16145550173 | clear | callable_manual |
| cty-0412 | Patricia Moore | 76 | probable | A1:find_people:address | +16145550129 | clear | callable_manual |
| cty-0088 | Robert Kline | 64 | probable | A1 rescue:find_people:name | +16145550151 | national | hold_dnc |
| dl-0031 | Ellen Park | 88 | confirmed | A2:property_lookup:owner | +16145550190 | clear | callable_manual |
| cty-0270 | Luis Ortega | 52 | weak | A1:find_people:address | +16145550144 | clear | mail_only |

## Next Steps

1. Mail all 450 properties this week; confirmed and probable owners by name, the rest to "Current Owner".
2. Load the 367 callable numbers (241 owners) into the reps' click-to-call queue with the identity-check opener for probable rows.
3. Log every "stop calling" to the internal list the same day; re-scrub any number not dialed by 2026-11-12.
4. Look up registered agents for the 9 LLC owners in the Ohio business registry and mail them.
5. Run next month's Distress List by ZIP to stay under 500 properties per run.
