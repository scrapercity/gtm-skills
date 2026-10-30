# Store List Report: US Shopify apparel stores using Klaviyo

Illustrative example. Prepared 2026-10-13 for Flowhouse, an email marketing agency that builds and runs Klaviyo flows. Offer: $2,500 a month retainer for T1 and T2, a $3,000 one-time flow build for T3. Plan: Starter ($49/mo). Wallet before run: $52.10. Store names use the reserved `.example` domain; counts are illustrative.

## Target Definition

| Item | Value |
|-|-|
| Platform | Shopify |
| Category | Apparel |
| Qualifying app or technology | Klaviyo (Shopify app) |
| Excluded technologies | None; Recharge flagged, not excluded |
| Geography | United States |
| Tier basis | Estimated monthly sales; Flowhouse's affordability ratio is 20x, set from its current clients ($2,500 x 20 = $50,000 for the retainer; the $3,000 project spread over 3 months = $1,000 a month, so $20,000 for T3) |
| Target send-ready stores | 1,150 |

## Filters Used

| Parameter | Value | Why |
|-|-|-|
| platform | shopify | apps filter is Shopify only |
| category | apparel | Agency's case studies are apparel brands |
| apps | Klaviyo | The retainer manages Klaviyo flows; value copied from the probe |
| countryCode | US | One country per campaign |
| emails | true | Email campaign; only stores with an address are returned |
| minEstimatedMonthlySales | 250000 / 50000 / 20000 | Tier floors, server-side |
| maxEstimatedMonthlySales | none / 249999 / 49999 | Tier ceilings, server-side, no overlap |
| totalLeads | 300 / 600 / 700 | Target per tier plus about 35% headroom, the validation and dedupe loss on Flowhouse's last apparel pull |
| offset | 0 | First page of each tier; nextOffset saved for the next pull |
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

App Store review flag: 61 US stores left a 1 or 2 star Klaviyo review in the last 12 months (complaints: setup time, flows breaking, cost). 23 matched the pull on store name key plus country and carry `unhappy_with_klaviyo = true` with a `review_note`; they go first, with "we run the flows for you" as the opener.

## Pull Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Pulled across 3 tier runs | 1,512 | 0 | T1 212, T2 600, T3 700 (probe rows excluded) |
| After normalization | 1,498 | 14 | 9 email syntax failures, 5 support@ helpdesk addresses |
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
| Total validated | 1,461 | One Email Validator run |

## Named Contacts

| Tier | Method | Stores | With a named valid email | Note |
|-|-|-|-|-|
| T1 | Website Finder, title "Founder", then Email Validator | 171 | 91 | 98 founders found, 91 valid; the role inbox moves to the hold file for these 91 |
| T2 | Website Finder, title "Founder", queued, paid from the remaining wallet | 470 | 0 | Ceiling 470 x $0.0499 = $23.45 plus $0.79 validation; wallet after at the ceiling $9.34 |
| T3 | Role inbox | 542 | 0 | Founder-run stores; `hello@` and `team@` reach the founder |

## Cost Estimate

| Line | Units | Unit price | Cost |
|-|-|-|-|
| Store Leads value probe | 25 leads | $0.0039 | $0.10 |
| Store Leads T1 | 212 leads | $0.0039 | $0.83 |
| Store Leads T2 | 600 leads | $0.0039 | $2.34 |
| Store Leads T3 | 700 leads | $0.0039 | $2.73 |
| Tech Stack Search, Recharge | 1 technology | $4.99 | $4.99 |
| Email Validator, store emails | 1,461 emails | $0.00169 | $2.47 |
| Website Finder, T1 founders | 98 contacts found | $0.0499 | $4.89 |
| Email Validator, founder emails | 98 emails | $0.00169 | $0.17 |
| Total | | | $18.52 |

Ceiling shown before the run: Store Leads 1,625 requested leads x $0.0039 = $6.34, Tech Stack Search $4.99, store email validation up to $2.75, Website Finder on 171 T1 domains up to $8.53 with $0.29 validation; $22.90 in total. Agency owner approved in chat on 2026-10-13; wallet after the run $33.58.

## Sample Rows

| Domain | Platform | Category | Apps | Tier | Email | email_status | Est. monthly sales |
|-|-|-|-|-|-|-|-|
| northloomapparel.example | shopify | Apparel | Klaviyo, Recharge, Gorgias | T1 | maren@northloomapparel.example | valid | $410,000 |
| saltwaterthreads.example | shopify | Apparel | Klaviyo, Judge.me | T2 | team@saltwaterthreads.example | valid | $96,000 |
| kestrelactive.example | shopify | Apparel | Klaviyo, Recharge | T2 | founders@kestrelactive.example | valid | $142,000 |
| plainstitch.example | shopify | Apparel | Klaviyo | T3 | info@plainstitch.example | valid | $31,000 |
| juniperandoak.example | shopify | Apparel | Klaviyo, Loox | T3 | hello@juniperandoak.example | valid | $24,500 |

QA sample (20 random rows, 2026-10-13): store live 20 of 20, category fit 19 of 20 (one children's shoe store), Klaviyo visible on the site 19 of 20, sales band plausible 18 of 20.

## Next Steps

1. Load three campaigns, one per tier, with store_name, category, the uses_recharge and unhappy_with_klaviyo flags and first name as custom variables; role inboxes read "Hi {store name} team". Send the 23 unhappy_with_klaviyo stores and the 91 named T1 founders first; T1 copy cites one missing flow found on their site, T3 copy leads with the fixed-price package.
2. Run Website Finder for T2 founders from the remaining wallet (ceiling $23.45 plus $0.79 validation, leaving at least $9.34) before the T2 campaign starts.
3. Re-validate the 31 unknown addresses on 2026-10-16; send catch-all stores from a separate low-volume campaign once the main campaigns show bounces under 2%.
4. On 2026-11-13, continue T2 from the saved nextOffset, dedupe on domain against this file, and re-validate any row validated more than 30 days before its send date.
