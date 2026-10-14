# Public Records Triggers

Free state and local open data that tells a calling team who just opened, who just changed hands, who failed an inspection and whose building is old. None of these sources are ScraperCity tools. Use them three ways:

1. Add brand-new businesses that a review-count filter leaves out.
2. Give the reason for the call a dated public fact ("your TABC permit was issued on the 3rd").
3. Rank who gets dialed first: a fresh trigger goes to the Priority bucket ahead of the Working records (`references/call-blocks-and-metrics.md` section 4b).

Every record from these sources gets typed and ordered like the rest (`references/dialer-and-caller-id.md`). A new owner-operated business often lists the owner's cell as its number, so type the line before the first dial.

## 1. Review-count filters drop new openings

A `minReviews` filter on `query_local_business_database`, or a review floor applied to `scrape_maps` or `scrape_yelp` results, removes every business that opened in the last few months, because it has not collected reviews yet. A new business still has to set up POS, payroll, insurance, signage, marketing, linen, pest control and reviews. Run two lists:

| List | Filter | Why |
|-|-|-|
| Main list | Your usual `minReviews` floor | Established businesses with a visible review gap |
| Fresh-opening list | No `minReviews`; `maxReviews: 10` | Businesses too new to clear the floor |
| Permit match | Fresh-opening rows matched to a permit or license record from section 2 by address or phone | Confirms the business is new and dates the opening |

Use the 2b script in `references/call-scripts-and-objections.md` (new listing angle) for the fresh-opening list, and cite the permit date instead of guessing "you opened in the last few months".

## 2. Source types and the trigger each one implies (any state)

Every state names these agencies differently. Search "[state] open data portal", "[state] comptroller" or "[state] revenue department", "[state] alcohol commission", and "[county] appraisal district" or "[county] assessor".

| Source type | Usual publisher | Fields to pull | Trigger it implies | Offers that fit the trigger (examples) |
|-|-|-|-|-|
| Liquor or alcohol permits, including pending applications | State alcohol agency | License type, status, original issue date, location address, owner or managing entity | A pending or new on-premise permit means a bar or restaurant is about to open; a new permit at an existing address can mean new ownership | POS, payroll, insurance, linen, music licensing, staffing, signage |
| Alcohol sales tax receipts (states that tax drinks sold separately) | State tax agency | Taxpayer, location, reporting period, receipts | Monthly sales by location: steady growth points to a second location, a falling trend to cost pressure | Financing, equipment, cost-cutting offers |
| Restaurant and food health inspections | City or county health department | Score, inspection date, violations | A low score or repeat violations is a fresh, specific pain | Pest control, refrigeration repair, deep cleaning, food safety training |
| Sales tax permits | State comptroller or revenue department | Permit issue date, first sales date, NAICS code, outlet address | A new business location this week | Anything a new business buys while setting up |
| Contractor and trade licenses | State licensing board | License type, license number, issue and expiration dates, business name, county | A new license is a new shop; a license type names the trade; an expiring license is a renewal date | Insurance, fleet, software, supplier accounts, continuing education |
| County appraisal or property records | County appraisal district or assessor | Owner, year built, building class, improvement value, square footage | Building age points at roofs, HVAC, plumbing and electrical near the end of their life; the owner record says who to address | Roofing, HVAC replacement, energy retrofits, commercial insurance, property management |
| New business filings | Secretary of state or business registry | Entity name, formation date, registered agent, entity type | A new legal entity, often weeks before a storefront exists | Banking, bookkeeping, payroll, insurance, web design |

Freshness: log the trigger's age at the first dial and compare meeting rate by age; once a trigger is old enough that it stops converting better than the main list, use it only as an account fact in the reason.

## 3. Worked set: Texas (checked 2026-10-13)

These are examples for one state. Field lists come from the publisher pages; open each dataset's column list before you build a filter on it.

| Source | Where | What the publisher says it holds | Trigger use |
|-|-|-|-|
| TABC License Information | Texas Open Data Portal, data.texas.gov dataset `7hf9-qc9f` | Each primary license the Texas Alcoholic Beverage Commission issues, about 28 license types, with effective dates, managing entities and contact information | New on-premise licenses by county and effective date: bars and restaurants that just opened |
| TABC pending original license applications | data.texas.gov dataset `mxm5-tdpj` | New alcohol license applications marked Received or In Review; renewals excluded | Businesses that have not opened yet: the earliest trigger on this list |
| Mixed Beverage Gross Receipts | data.texas.gov dataset `naix-2893`, Texas Comptroller | Taxpayers who file mixed beverage gross receipts reports, with amounts reported | Size and trend of drink sales per location |
| Recent sales tax permits | comptroller.texas.gov, Transparency, Open Data, Recent Sales Tax Permits | Permits issued in the week before the last update, with outlet address, NAICS code, permit issue date and first sales date | New locations by NAICS code and county every week |
| TDLR license files | tdlr.texas.gov License Search download page; also data.texas.gov dataset `7358-krk7` (TDLR All Licenses) | CSV files updated every day, by license type: air conditioning contractors and technicians, electricians and electrical contractors, tow companies, barbering and cosmetology establishments and more | New licenses by trade and county; plumbers are licensed by a separate state board |
| Austin Food Establishment Inspection Scores | data.austintexas.gov dataset `ecmv-9xxi` | Austin Public Health inspection scores from the last 3 years | Low or falling scores for food safety, pest and refrigeration offers |
| City of Dallas restaurant food scores | dallascityhall.com Consumer Health page, linking a search tool (no bulk file found on 2026-10-13) | Inspection scores per establishment, weighted toward critical violations; the city notes scores are a snapshot and some places are missing after an ownership change or remodel | Look up each restaurant on the list before the call; a recent low score is a dated fact for food safety, pest and refrigeration offers |
| Dallas Central Appraisal District data products | dallascad.org, Data Products | Current ownership and certified appraisal data files, each with reference documents that explain the fields | Owner names, and building age where the field reference shows a year-built field |

Example recipe (an HVAC replacement offer in Dallas County): pull commercial accounts from the appraisal file, keep buildings at the age your offer targets, match owner or tenant business names to `query_local_business_database` with `hasPhone: true`, then type and order the numbers like any other row. The reason for the call cites the building's year from the appraisal record.

## 4. Cost and handling

| Check | Rule |
|-|-|
| Portal limits | Check each portal's API rate limits before you script a pull. Some registries charge per search or per record. |
| Source field | Store `source` (portal and dataset id), `source_detail` (record id) and `pulled_at` on every row, as `references/list-quality-standard.md` requires. |
| Matching | Match on phone in E.164 first, then normalized street address plus postal code, then business name plus city. Keep unmatched permit rows in a separate tab; do not guess a phone number. |
| Cost | The portals in section 3 are free to view and download. ScraperCity spend starts when you look up phones or contacts for the matched rows (`find_mobiles` at $0.25 per number found). |

## Sources

- Texas Open Data Portal, TABC License Information: https://data.texas.gov/d/7hf9-qc9f
- Data.gov listing, TABC License Information: https://catalog.data.gov/dataset/tabc-license-information
- Data.gov listing, Pending Original New Primary and Subordinate License Applications: https://catalog.data.gov/dataset/pending-original-new-primary-and-subordinate-license-applications
- Texas Open Data Portal, Mixed Beverage Gross Receipts: https://data.texas.gov/d/naix-2893
- Data.gov listing, Mixed Beverage Gross Receipts: https://catalog.data.gov/dataset/mixed-beverage-gross-receipts
- Texas Comptroller, Recent Sales Tax Permits: https://comptroller.texas.gov/transparency/open-data/recent-sales-tax-permits
- TDLR, License data files: https://www.tdlr.texas.gov/LicenseSearch/licfile.asp
- Texas Open Data Portal, TDLR All Licenses: https://data.texas.gov/d/7358-krk7
- Data.gov listing, Food Establishment Inspection Scores (City of Austin): https://catalog.data.gov/dataset/food-establishment-inspection-scores
- Dallas Central Appraisal District, Data Products: https://dallascad.org/DataProducts.aspx
- City of Dallas, Restaurant Food Scores: https://dallascityhall.com/departments/codecompliance/consumer-health/Pages/restaurant_food_scores.aspx
