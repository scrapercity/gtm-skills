# Real Estate Workflow Playbooks

One playbook per persona. Each gives the tool chain, the exact calls, a priced example from catalog prices, the channel routing and the compliance flags. Run `check_wallet` before each and get approval for spend over $5.

## 1. Selling to real estate agents (vendors, brokerage recruiters, lenders seeking referral partners)

Goal: a list of active agents in a market, segmented by production.

| Step | Call | Notes |
|---|---|---|
| 1 | `scrape_zillow_agents` `{"location":"Denver, CO","searchLimit":300}` | One run per city or ZIP; 500 max per run |
| 2 | Repeat for suburbs: Aurora, Lakewood, Littleton, Arvada | Dedupe on profile URL |
| 3 | Optional `specialty` runs (for example `buyer`) for a niche offer | Probe codes with `searchLimit: 5` first |
| 4 | `validate_emails` on the agent emails | $0.0072 each |
| 5 | Segment by recent sales count and active listings | See `references/tool-reference.md` |

Priced example: 5 cities x 300 agents = 1,500 x $0.029 = $43.50. Validation on 1,350 emails = $9.72. Total $53.22.

Routing: agents are licensed professionals contacted at their business; email is the main channel and follows CAN-SPAM. Many agents list a personal mobile as the business number, so treat it as a wireless number: manual calls only, inside 8 a.m. to 9 p.m. local time, DNC-scrubbed, and no autodialer or texts without consent.

## 2. Wholesalers and residential investors (motivated sellers)

Goal: distressed properties plus owner contact, routed to compliant channels.

| Step | Call | Notes |
|---|---|---|
| 1 | Confirm the state's wholesaling rules | `references/compliance-guide.md` |
| 2 | `scrape_distress_list` `{"search":"33612","distressTypes":["preForeclosure"],"maxItems":200}` per target ZIP | Pre-foreclosure gives the most time to work a deal |
| 3 | Filter rows: value estimate inside the buy box, property type single-family | Done on the CSV |
| 4 | `find_people` `{"street_citystatezip":[...],"max_results":1}` on kept rows | $0.0199 per search, misses billed |
| 5 | `scrape_property_lookup` without owner contact on the top 10% for price history | $0.15 each |
| 6 | DNC scrub, flag mobiles, route | Mail first, manual calls second |

Priced example: 6 ZIPs x 200 = 1,200 x $0.05 = $60.00. Keep 700 inside the buy box, `find_people` 700 x $0.0199 = $13.93. Lookups on 70 = $10.50. Total $84.43.

Routing: direct mail to every owner (no DNC rule on mail). Manual live calls to numbers that pass the DNC scrub, inside 8 a.m. to 9 p.m. local time. Texts and autodialed calls wait until prior express written consent is on file. Scripts make purchase offers; any "save your home" or loan modification pitch falls under Regulation O.

## 3. Listing agents prospecting pre-foreclosures and REO

Goal: homeowners who may need to sell, and bank-owned inventory.

| Step | Call | Notes |
|---|---|---|
| 1 | `scrape_distress_list` `{"search":"Phoenix, AZ","distressTypes":["preForeclosure"],"maxItems":300}` | Homeowners who may list |
| 2 | `scrape_distress_list` `{"search":"Phoenix, AZ","distressTypes":["bankOwned"],"maxItems":200}` | REO: the lender is the seller, so the outreach target is the asset manager, not the former owner |
| 3 | `scrape_property_lookup` with owner contact on pre-foreclosures with value above a threshold | $0.25 each |
| 4 | Letter with a CMA-style value range | From the lookup's estimated value |

Priced example: 300 + 200 = 500 x $0.05 = $25.00. Owner lookups on 120 = $30.00. Total $55.00.

Routing: mail first; manual calls only after DNC scrub. Some states regulate solicitations to owners in foreclosure (California Civil Code 1695 governs equity purchases from them). An agent who also buys directly must follow those rules.

## 4. Lenders and loan officers

Goal: referral partners (agents), investor borrowers, and commercial or SBA deal flow.

| Need | Tool chain | Example cost |
|---|---|---|
| Agent referral partners | `scrape_zillow_agents` by city, segment by recent sales | 400 agents = $11.60 |
| Investors buying distressed property | `scrape_distress_list` for `auction` and `bankOwned` to see where investors are active; pair with `scrapercity-lead-database` for investors by title | 300 properties = $15.00 |
| Commercial borrowers and brokers | `scrape_crexi` on multifamily or retail searches in the lending footprint | 600 listings = $17.40 |
| SBA acquisition loans | `scrape_bizbuysell` on state searches; reach the listing brokers | 800 listings = $7.92 |

Routing: agents and CRE or business brokers are B2B contacts; email and calls to their business lines follow CAN-SPAM, and most B2B calls are exempt from the TSR's DNC provisions. A lender reaching homeowners about refinancing or relief is in consumer territory: TCPA, DNC and, for relief offers, Regulation O.

## 5. Commercial real estate brokers

Goal: listings by type and market, and the competing brokers who hold them.

| Step | Call | Notes |
|---|---|---|
| 1 | On Crexi, choose the city or market in the search bar, set type (for example Industrial), price and cap rate | A panned map with no location returns 400 |
| 2 | `scrape_crexi` `{"startUrls":["<copied URL>"]}` | Replace the angle-bracket text with the copied address |
| 3 | Broker directory run for the same market | `https://www.crexi.com/resources/find-a-broker/...` URL |
| 4 | Group listings by broker firm; count listings per broker | Top holders are co-brokerage or recruiting targets |
| 5 | Track asking price and days listed across weekly runs | Price cuts signal motivated sellers |

Priced example: 3 markets x 350 listings = 1,050 x $0.029 = $30.45. Broker directory 300 brokers = $8.70. Total $39.15.

Routing: brokers are B2B; email and phone to business lines. Owners of the properties are a separate list: run `scrape_property_lookup` on the address (commercial owners are often LLCs) and treat individual owners with consumer rules.

## 6. Business brokers and acquirers

Goal: businesses for sale in a niche, with financials and the listing broker.

| Step | Call | Notes |
|---|---|---|
| 1 | Build the search on BizBuySell (state + industry, for example Texas HVAC) | Copy the URL |
| 2 | `scrape_bizbuysell` `{"startUrls":["https://www.bizbuysell.com/texas/hvac-businesses-for-sale/"],"maxItems":200,"datasetName":"tx-hvac"}` | Same `datasetName` on reruns dedupes |
| 3 | Filter by cash flow and asking price multiple | Price / cash flow on each row |
| 4 | Reach listing brokers for deal flow; for acquirers, request the CIM | Broker name, phone, firm per row |
| 5 | Find owners of similar businesses not for sale | `scrapercity-local-business-database` with `keyword: ["hvac contractor"]` in the same state |

Priced example: 4 states x 200 = 800 x $0.0099 = $7.92. Local Business Database pull of 2,000 HVAC companies: included in Growth.

Routing: brokers are B2B. Owners of businesses not for sale are B2B contacts at their business; CAN-SPAM for email, and manual calls to business lines.

## 7. Property managers and investors tracking a portfolio

Goal: values and history for a list of owned or target addresses.

| Step | Call | Notes |
|---|---|---|
| 1 | Normalize addresses with ZIP | Required |
| 2 | `scrape_property_lookup` `{"addresses":[...],"fileName":"portfolio-q4"}` | No owner contact needed for owned property |
| 3 | Compare estimated value to purchase price | Equity per property |

Priced example: 80 properties x $0.15 = $12.00.

## Choosing between paths, quick table

| Want | Cheapest route | Cost per record |
|---|---|---:|
| Agent contact | `scrape_zillow_agents` | $0.029 |
| Distressed property list | `scrape_distress_list` | $0.05 |
| Owner contact from an address | `find_people` with `max_results: 1` | $0.0199 |
| Value, history and owner in one row | `scrape_property_lookup` with owner contact | $0.25 |
| CRE listing with broker | `scrape_crexi` | $0.029 |
| Business for sale with broker | `scrape_bizbuysell` | $0.0099 |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/zillow-agents-scraper
- https://scrapercity.com/crexi-scraper
- https://scrapercity.com/bizbuysell-scraper
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- https://california.public.law/codes/civil_code_section_1695.4
