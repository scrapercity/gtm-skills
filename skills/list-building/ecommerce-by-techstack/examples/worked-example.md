# Store List Report: US Shopify apparel stores using Klaviyo

Prepared 2026-10-13 for Flowhouse, an email marketing agency that builds and runs Klaviyo flows. Offer: $2,500 a month retainer for T1 and T2, a $3,000 one-time flow build for T3. Plan: Starter ($49/mo). Wallet before run: $52.10. Store names use the reserved `.example` domain; counts are illustrative.

## Target Definition

| Item | Value |
|-|-|
| Platform | Shopify |
| Category | Apparel |
| Qualifying app or technology | Klaviyo (Shopify app) |
| Excluded technologies | None; Recharge flagged, not excluded |
| Geography | United States |
| Tier basis | Estimated monthly sales; floor is 20 times the monthly price ($2,500 x 20 = $50,000 for the retainer; $3,000 project / 3 = $1,000 a month, so $20,000 for T3) |
| Target send-ready stores | 1,150 |

## Filters Used

| Parameter | Value | Why |
|-|-|-|
| platform | shopify | apps filter is Shopify only |
| category | apparel | Agency's case studies are apparel brands |
| apps | Klaviyo | The retainer manages Klaviyo flows; value copied from the probe |
| countryCode | US | One country per campaign; CAN-SPAM applies |
| emails | true | Email campaign; only stores with an address are returned |
| minEstimatedMonthlySales | 250000 / 50000 / 20000 | Tier floors, server-side |
| maxEstimatedMonthlySales | none / 249999 / 49999 | Tier ceilings, server-side, no overlap |
| totalLeads | 300 / 600 / 700 | Target per tier plus about 35% headroom |
| offset | 0 | First page of each tier; nextOffset kept for the next pull |
| fileName | shopify-apparel-klaviyo-us-t1, -t2, -t3 | Matches the run log and dashboard |

## Value Probe

| Probe | Rows returned | Values seen | Decision |
|-|-|-|-|
| platform shopify, category apparel, apps Klaviyo, countryCode US, emails true, totalLeads 25 | 25 | Category column read Apparel on all 25; apps column listed Klaviyo on all 25 | Keep values; universe is larger than 25 |

## Tier Bands

| Tier | minEstimatedMonthlySales | maxEstimatedMonthlySales | Pulled | Send-ready | Sequence |
|-|-|-|-|-|-|
| T1 | 250,000 | none | 212 | 171 | Flow teardown of their store plus a 20-minute call |
| T2 | 50,000 | 249,999 | 600 | 470 | Apparel case study, retainer offer |
| T3 | 20,000 | 49,999 | 700 | 542 | $3,000 flow build package |

T1 returned 212 of the 300 requested: that is the full universe for these filters, and only returned rows were billed.

## Tech Stack Search

| Technology | Cost | Domains returned | Matched in store list | Use |
|-|-|-|-|-|
| Recharge | $4.99 | 41,906 | 164 | Flag uses_recharge = true; T1 and T2 subscription stores get a replenishment-flow angle |

## Pull Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Pulled across 3 tier runs | 1,512 | 0 | T1 212, T2 600, T3 700 (probe rows excluded) |
| After normalization | 1,498 | 14 | 9 email syntax failures, 5 platform support addresses |
| After dedupe on domain then email | 1,490 | 8 | Two storefronts sharing one inbox |
| After suppression | 1,461 | 29 | 22 current agency clients, 7 past unsubscribes |
| Valid after validation | 1,183 | 278 | 176 catch_all and 31 unknown to the hold file, 66 invalid and 5 disposable removed |

## Validation Results

| Bucket | Count | Action |
|-|-|-|
| valid | 1,183 | Main CSV, split by tier |
| catch_all | 176 | Hold file; separate campaign at no more than 10% of daily volume |
| unknown | 31 | Re-validate after 72 hours |
| invalid | 66 | Removed and added to bounce suppression |
| disposable | 5 | Removed and suppressed |
| Total validated | 1,461 | One validate_emails run |

## Cost Estimate

| Line | Units | Unit price | Cost |
|-|-|-|-|
| scrape_store_leads value probe | 25 leads | $0.0039 | $0.10 |
| scrape_store_leads T1 | 212 leads | $0.0039 | $0.83 |
| scrape_store_leads T2 | 600 leads | $0.0039 | $2.34 |
| scrape_store_leads T3 | 700 leads | $0.0039 | $2.73 |
| scrape_builtwith (Tech Stack Search), Recharge | 1 technology | $4.99 | $4.99 |
| validate_emails | 1,461 emails | $0.0072 | $10.52 |
| Total | | | $21.51 |

Ceiling shown before the run: 1,625 requested leads x $0.0039 = $6.34, plus $4.99, plus up to 1,625 x $0.0072 = $11.70 validation, $23.03 in total. Agency owner approved in chat on 2026-10-13; wallet covered it with $29.07 to spare.

## Sample Rows

| Domain | Platform | Category | Apps | Tier | Email | email_status | Est. monthly sales |
|-|-|-|-|-|-|-|-|
| northloomapparel.example | shopify | Apparel | Klaviyo, Recharge, Gorgias | T1 | hello@northloomapparel.example | valid | $410,000 |
| saltwaterthreads.example | shopify | Apparel | Klaviyo, Judge.me | T2 | team@saltwaterthreads.example | valid | $96,000 |
| kestrelactive.example | shopify | Apparel | Klaviyo, Recharge | T2 | founders@kestrelactive.example | valid | $142,000 |
| plainstitch.example | shopify | Apparel | Klaviyo | T3 | info@plainstitch.example | valid | $31,000 |
| juniperandoak.example | shopify | Apparel | Klaviyo, Loox | T3 | hello@juniperandoak.example | valid | $24,500 |

## Next Steps

1. Load the three tier files into separate campaigns; T1 copy cites a specific missing flow found on their site, T3 copy leads with the fixed-price package.
2. Use the 164 uses_recharge stores as a sub-segment in T1 and T2 with replenishment and subscription-churn flows as the hook.
3. Find the founder or head of ecommerce for the 171 T1 stores with scrape_website_finder (jobTitle Founder), ceiling 171 x $0.0499 = $8.53, and validate those emails.
4. Re-validate the 31 unknown addresses on 2026-10-16; send catch-all stores from a separate low-volume campaign.
5. Next month, pull T2 with offset set to the saved nextOffset to reach stores not yet contacted, and dedupe on domain against this file.
