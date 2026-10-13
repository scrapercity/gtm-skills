# Real Estate Data Plan: Pre-foreclosure owners in north Tampa, FL

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

## Objective

| Item | Value |
|---|---|
| Persona | Residential wholesaler and buy-and-hold investor, two-person team, Hillsborough County |
| Market | Six north Tampa ZIP codes: 33604, 33610, 33612, 33613, 33614, 33617 |
| Outcome wanted | 30 owner conversations a month with owners in pre-foreclosure or facing auction, for cash purchase offers |
| Channels planned | Direct mail to every owner, manual live calls to numbers that pass the DNC scrub. No texting, no autodialer |
| Wallet balance from check_wallet | $140.00 on the Growth plan |

## Tool Plan

| Step | Tool | Key parameters | Units |
|---|---|---|---:|
| 1 | scrape_distress_list | search per ZIP (6 runs), distressTypes ["preForeclosure", "auction"], maxItems 200 | 1,200 |
| 2 | (CSV filter) | Keep single-family, value estimate $150,000 to $450,000; 1,200 rows became 640 | 0 |
| 3 | find_people | street_citystatezip = each kept property address, max_results 1 | 640 |
| 4 | scrape_property_lookup | includeOwnerContact false, top 60 by value estimate, for price history | 60 |
| 5 | (scrub) | National DNC Registry and Florida state list, mobile flag, internal DNC list | 0 |

## Cost Estimate

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| scrape_distress_list | 1,200 | $0.05 | $60.00 |
| find_people (0 matches still billed as 1 result) | 640 | $0.0199 | $12.74 |
| scrape_property_lookup without owner contact | 60 | $0.15 | $9.00 |
| Total | | | $81.74 |

Approval: Shown to the user before step 1, approved in chat. $81.74 is under the $140.00 balance. The alternative of Property Lookup with owner contact on all 640 would cost 640 x $0.25 = $160.00 and exceed the balance.

## Compliance Check

| Channel | Recipients | Law | Action |
|---|---|---|---|
| Direct mail | All 640 owners | CFPB Regulation O (12 CFR 1015) on content | Letter makes a cash purchase offer only. No promise to stop the foreclosure or modify the loan |
| Manual calls | Owners whose numbers pass the scrub | TCPA (47 U.S.C. 227), 47 CFR 64.1200, FTC Telemarketing Sales Rule | Scrub against the National DNC Registry at least every 31 days, live manual dial only, 8 a.m. to 9 p.m. Eastern, internal do-not-call list honored at once |
| Texting | None | TCPA and Florida Telephone Solicitation Act (Fla. Stat. 501.059) | Not used. No prior express written consent on file |
| Email | Owners with a personal email from People Finder | CAN-SPAM | Postal address, clear opt-out, removals within 10 business days |

State rule: Florida is not one of the states with a wholesaling licensing or disclosure statute covered in `references/compliance-guide.md` (IL, OK, PA, OH, SC). The team confirms current Florida rules with a local real estate attorney before assigning any contract, and discloses in writing that it may assign the contract.

FCRA boundary: Results are used only to find owners and make purchase offers. No result is used for tenant screening, lending or any other eligibility decision.

## Outreach Routing

| Record group | Count | Channel | Notes |
|---|---:|---|---|
| All kept owners | 640 | Direct mail, two letters 21 days apart | Mail needs no DNC scrub; content follows Regulation O |
| Owners with a phone that passed the DNC scrub | 212 | Manual live calls, up to 3 attempts | 388 numbers found; 176 removed by the Registry and state list scrub |
| Owners with no phone found | 252 | Mail only | 640 searches minus 388 with a phone |
| Top 60 by value with price history | 60 | Mail plus calls, offer letter cites last sale price | From scrape_property_lookup |

## Next Steps

1. Run the six Distress List searches, then filter to the 640 kept rows and send them to People Finder with max_results 1.
2. Scrub the 388 numbers against the National DNC Registry and the Florida list, record the scrub date, and load only the 212 that pass into a manual dialer view.
3. Rerun the Distress List monthly for the same ZIPs, dedupe on address, and scrub again within 31 days of each calling block.
