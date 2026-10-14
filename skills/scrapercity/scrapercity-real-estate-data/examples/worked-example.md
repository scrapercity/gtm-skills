# Real Estate Data Plan: Pre-foreclosure owners in north Tampa, FL

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

## Objective

| Item | Value |
|---|---|
| Persona | Residential wholesaler and buy-and-hold investor, two-person team, Hillsborough County |
| Market | Six north Tampa ZIP codes: 33604, 33610, 33612, 33613, 33614, 33617 |
| Outcome wanted | 30 owner conversations a month with owners in pre-foreclosure or facing auction, for cash purchase offers |
| Channels planned | Direct mail to every owner in the buy box, manual live calls to confirmed and probable owner matches. No texting, no dialer automation |
| Wallet balance from check_wallet | $140.00 on the Growth plan |

## Tool Plan

| Step | Tool | Key parameters | Units |
|---|---|---|---:|
| 1 | scrape_distress_list | search per ZIP (6 runs), distressTypes ["preForeclosure", "auction"], maxItems 200 | 1,200 |
| 2 | (CSV filter) | Keep single-family, value estimate $150,000 to $450,000; 1,200 rows became 640 | 0 |
| 3 | find_people | street_citystatezip = each kept property address, max_results 1 | 640 |
| 4 | scrape_property_lookup | includeOwnerContact false, top 60 by value estimate, for price history | 60 |
| 5 | (match and suppress) | Match class per row from address and name after USPS normalization; team suppression list removed | 0 |

## Cost Estimate

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| scrape_distress_list | 1,200 | $0.05 | $60.00 |
| find_people (0 matches still billed as 1 result) | 640 | $0.0199 | $12.74 |
| scrape_property_lookup without owner contact | 60 | $0.15 | $9.00 |
| Total | | | $81.74 |

Approval: Shown to the user before step 1, approved in chat. $81.74 is under the $140.00 balance. The alternative of Property Lookup with owner contact on all 640 would cost 640 x $0.25 = $160.00 and exceed the balance.

## Contact Hygiene

| Channel | Recipients | Rule | Operating reason |
|---|---|---|---|
| Direct mail | All 640 owners in the buy box | Cash purchase offer, signed by name with the team's phone; suppression list applied before each drop | Reaches every owner, including the 252 with no phone found |
| Manual calls | 241 confirmed and probable matches not on the suppression list | Live manual dial, outcome logged per attempt, list checked before each block; after two weeks the attempt cap is set at the attempt where connects stop; caller IDs checked for spam labels weekly | Calls reach the person on the deed; wrong-number replies are caught on the first attempt and suppressed; a labeled number is swapped before pickups drop |
| Email | 96 confirmed owners with a personal email | Validated first; separate campaign from agent email; one-click unsubscribe; removals within 2 days; pause above 2% hard bounces | Inbox placement holds while spam complaints stay under Google's 0.1% and bounces under Hunter's 2% |

Match test: People Finder's returned address must equal the property address after USPS Publication 28 normalization, and the returned name must match the owner on the distress record (confirmed) or share the surname (probable). Of 388 results with a phone, 241 passed; 147 failed and get mail only.

Suppression list: one sheet owned by the team lead, merged from past "stop" replies, wrong numbers and sold properties (63 rows), loaded into the mail house file and the dialer view before step 5; new "stop" requests from any channel are added the same day.

## Outreach Routing

| Record group | Count | Channel | Notes |
|---|---:|---|---|
| All kept owners | 640 | Direct mail, two letters 21 days apart (the team's schedule) | Purchase offer, named sender |
| Confirmed and probable matches with a phone | 241 | Manual live calls, attempts capped from outcome data | 388 numbers found; 147 failed the match test and stay mail only |
| Owners with no phone found | 252 | Mail only | 640 searches minus 388 with a phone |
| Top 60 by value with price history | 60 | Mail plus calls, offer letter cites last sale price | From scrape_property_lookup |

## Next Steps

1. Run the six Distress List searches, then filter to the 640 kept rows and send them to People Finder with max_results 1.
2. Classify the 388 phone results by match class, remove the suppression list, and load only the 241 confirmed and probable matches into a manual dialer view.
3. Rerun the Distress List monthly for the same ZIPs, dedupe on normalized address against last month's file and the suppression list, and log every call outcome so the next block starts from it.
