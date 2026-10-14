# Local Pull Plan: Dentists in the Austin, TX metro

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

## Request Summary

| Item | Value |
|---|---|
| Business type | General and family dental practices, for a cold email offer of a patient-reactivation service |
| Places | Austin, Round Rock, Cedar Park, Pflugerville, Georgetown, Leander (Texas) |
| Contact needs | Email required; a named contact preferred for the first send |
| Plan confirmed by check_wallet | Growth, $149/mo, wallet balance $96.10 |
| Tool chosen and why | `query_local_business_database`: included in Growth, returns in seconds, and has rating and review filters and named contacts that `scrape_maps` does not |

## Search Spec

Every parameter must exist in `query_local_business_database`.

| Parameter | Value | Reason |
|---|---|---|
| keyword | ["dentist"] | What a patient types into Google Maps. Matches names and categories |
| location | ["Austin TX", "Round Rock TX", "Cedar Park TX", "Pflugerville TX", "Georgetown TX", "Leander TX"] | The six cities the service covers, any match |
| notCategory | ["Dental laboratory", "Dental supply store"] | `searched_as` showed both categories matched "dentist"; neither treats patients |
| country | ["US"] | Two-letter code; guards against a same-named place abroad |
| hasEmail | true | Cold email campaign |
| limit | 1 for the count, 100 for the pull | Count check first |

## Count Check

| Item | Value |
|---|---|
| Call used | MCP `query_local_business_database` with the search spec and `limit: 1` |
| pagination.total | 1,146 |
| searched_as keywords | "dentist" matched Dentist, Cosmetic dentist, Pediatric dentist, Dental clinic, Dental laboratory, Dental supply store. The last two are excluded |
| searched_as places | All six read as cities in Texas, US. None not_found |
| lead_database block | Not present (the search found businesses) |
| Decision | 1,146 is inside one day's 100,000 allowance. Segment, then pull |

## Segments

| Segment | Rating band | Review band | Count | Opening angle |
|---|---|---|---:|---|
| A. Leaders | minRating 4.5 | minReviews 20 | 388 | Reactivation of lapsed patients at the practices with the most reviews |
| B. Solid | minRating 4.0, maxRating 4.4 | minReviews 20 | 241 | Reactivation, plus the 4.5-star line that 31% of consumers apply (BrightLocal 2026) |
| C. Thin | minRating 4.0 | maxReviews 19 | 197 | Under the 20-review line that 47% of consumers use (BrightLocal 2026) |
| D. At risk | maxRating 3.9 | minReviews 1 | 154 | Held back from the first send; reputation offer is a separate campaign |
| E. No reviews | none | maxReviews 0 | 166 | Held back; a separate test later |

388 + 241 + 197 + 154 + 166 = 1,146. The bands do not overlap, and a dedupe on business id confirmed it. 412 of the 1,146 have a named contact (`contact_first_name` present).

## Pull Plan

| Item | Value |
|---|---|
| Paging method | Cursor per segment: `after: "0"`, then `pagination.next_after` until null |
| excludeDelivered | true, so re-runs and the weekly refresh return only new practices |
| page | 1 (never raised) |
| Tiles or location list | Location list of six cities. Tiling not needed at this count |
| Calls needed | 4 for A, 3 for B, 2 for C (only A, B and C pulled now) |
| Daily new businesses | 826 on day one (A, B and C), then a weekly refresh of new practices |
| Days needed | 1 |

## Cost Estimate

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Local Business Database pull, segments A, B, C | 826 | included in Growth | $0.00 |
| validate_emails (826 businesses, 1,001 emails) | 1,001 | $0.0072 | $7.21 |
| find_emails for the dentist named on the website of 200 practices without a contact, ceiling if every lookup finds one | 200 | $0.05 | $10.00 |
| Total paid, ceiling | | | $17.21 |

Email Finder bills only emails found, so its line lands at found emails x $0.05. For comparison, `scrape_maps` for the same 1,146 practices would cost 1,146 x $0.0099 = $11.35 without a rating filter or named contacts. The user approved the $17.21 ceiling before validation.

## Sample QA

| Check | Result |
|---|---|
| Category fits | 20 of 20 dental practices (Dentist, Cosmetic dentist, Dental clinic) |
| Address inside the places | 20 of 20 in the six cities |
| Rating and reviews inside segment | 20 of 20 for segment A (4.5 to 5.0, 24 to 1,210 reviews) |
| Email or phone present as required | 20 of 20 have at least one email |
| On-target rows | 19 / 20 (one row is a dental support office that manages several practices, kept for a separate DSO list; no shared miss pattern, so the search stands) |

## Next Steps

1. Validate the 1,001 emails ($7.21) and drop invalid addresses before any send.
2. Write one first line per segment (A, B, C) and hand the three files to `cold-email-list`; personalize with `contact_first_name` where present.
3. Schedule a weekly refresh: same search, `excludeDelivered: true`, `after: "0"`, so only new practices come back.
