# Store Leads Parameter Guide

Every `scrape_store_leads` parameter in the published catalog (`references/scrapercity-catalog.md`, npm package 1.0.17), what it does, and how to use it without wasting spend. Endpoint: `POST /api/v1/scrape/store-leads`. Price: $0.0039 per lead returned.

## 1. Parameter table

| Parameter | Type | What it does | Operating notes |
|-|-|-|-|
| `platform` | string | E-commerce platform, case-insensitive. Omit for all platforms | Platforms per scrapercity.com: Shopify, WooCommerce, Magento, BigCommerce, Squarespace, Ecwid, OpenCart, Webflow, PrestaShop, Demandware. Use the plain lowercase name |
| `totalLeads` | number | Total leads to fetch in this run | The run's cost ceiling: `totalLeads` x $0.0039 |
| `resumeFromLead` | number | Resume from this lead number | Restart a cancelled run without paying for the rows you already have |
| `countryCode` | string | Two-letter country code | ISO 3166-1 alpha-2: `US`, `GB`, `DE`, `CA`, `AU` |
| `emails` | boolean | Only stores with email addresses | Always `true` for an email list |
| `phones` | boolean | Only stores with phone numbers | `true` for a call list; combine with `emails` for multi-channel |
| `category` | string | Store category, case-insensitive | Values are not listed in the catalog. Probe with 25 rows and copy what the data shows |
| `city` | string | City filter | Pair with `countryCode` to avoid same-name cities |
| `state` | string | State or region, case-insensitive | Probe whether the data uses `California` or `CA` |
| `technologies` | string | Filter by technologies used | Any platform. One technology per call |
| `apps` | string | Filter by installed apps, Shopify only | Use with `platform: "shopify"`. One app per call |
| `instagram`, `facebook`, `tiktok`, `youtube`, `linkedin`, `twitter`, `pinterest` | boolean | Store has that social profile | Signals a content or ads budget; also a second outreach channel |
| `planExclude` | string[] | Exclude stores on these plan tiers, case-insensitive, several allowed | `["Shopify Plus"]` removes enterprise Shopify stores |
| `offset` | number | Leads to skip before returning results | Send `0` first, then the response's `nextOffset` (or previous offset + `totalLeads`). Without it, repeat calls return the same first page |
| `minEstimatedMonthlyVisits` (alias `visitsMin`) | number | At least this many estimated monthly visits | Server-side: stores below are never returned or billed |
| `maxEstimatedMonthlyVisits` (alias `visitsMax`) | number | At most this many | Server-side |
| `minEstimatedMonthlySales` (alias `salesMin`) | number | Minimum estimated monthly sales, USD | Server-side |
| `maxEstimatedMonthlySales` (alias `salesMax`) | number | Maximum estimated monthly sales, USD | Server-side |
| `minEmployeeCount` (alias `employeesMin`) | number | Minimum employee count | Server-side |
| `maxEmployeeCount` (alias `employeesMax`) | number | Maximum employee count | Server-side |
| `fileName` | string | Custom filename for export | Name per tier: `shopify-apparel-klaviyo-us-t2` |

Estimated visits and sales are model estimates, not reported figures. Use them to band and rank, never to quote a store's revenue back to it in copy.

## 2. Value probing

The catalog gives no enumerated values for `category`, `apps`, `technologies` or `state`. Before any large pull:

1. Run the draft filters with `totalLeads: 25` (cost $0.0975).
2. Open the CSV. Read the category, apps, technologies and state columns.
3. Copy the exact string the data uses into the filter. Case does not matter for `platform` and `category` per the catalog; treat everything else as exact until a probe shows otherwise.
4. If the probe returns 0 rows, remove the newest filter and probe again. The last filter removed is the one spelled differently.
5. If the probe returns fewer than 25 rows, the universe for those filters is that size. Widen (drop `category`, widen the band, add countries) or accept the small list.

## 3. Paging and resuming

| Situation | What to send |
|-|-|
| First page | `offset: 0`, `totalLeads: N` |
| Next page | `offset: nextOffset` from the previous response |
| No `nextOffset` in the response | `offset: previous offset + N` |
| Run was cancelled at lead 340 | Same filters, `resumeFromLead: 340` |
| Re-running last month's tier for new stores only | New run with the same filters; dedupe locally on domain against last month's file |

Store Leads has no `excludeDelivered`. Keep each tier's prior CSV and dedupe on normalized domain before validation, so you never validate the same store twice.

## 4. Single-value filters and combinations

`apps` and `technologies` are single strings in the schema, and the catalog does not document comma lists. Treat them as one value per call:

| Need | Approach |
|-|-|
| Stores with app A | `apps: "A"` |
| Stores with app A or app B | Two runs, union on domain |
| Stores with app A and app B | Run the smaller app, then intersect with a Tech Stack Search list for the other ($4.99) |
| Stores with app A and not app B | Run app A, subtract a Tech Stack Search list for B |
| Stores with technology T on WooCommerce | `platform: "woocommerce"`, `technologies: "T"` |

## 5. Band filter patterns

| Goal | Parameters |
|-|-|
| Exclude tiny stores | `minEstimatedMonthlySales: 10000` or `minEstimatedMonthlyVisits: 5000` |
| One tier | `minEstimatedMonthlySales` and `maxEstimatedMonthlySales` with the upper bound one dollar below the next tier's floor |
| Team size for a service that needs a marketing hire | `minEmployeeCount: 5` |
| Founder-run stores | `maxEmployeeCount: 10` |
| Enterprise only | `minEstimatedMonthlySales: 1000000`; there is no plan include filter, so read the plan column if the data has one |
| SMB only on Shopify | `planExclude: ["Shopify Plus"]` plus a sales ceiling |

## 6. Cost table

| Leads requested | Cost |
|-:|-:|
| 25 (probe) | $0.10 |
| 100 | $0.39 |
| 500 | $1.95 |
| 1,000 | $3.90 |
| 5,000 | $19.50 |
| 10,000 | $39.00 |
| 50,000 | $195.00 |

Add $0.0072 per email for validation: 1,000 stores pulled and validated cost $3.90 + $7.20 = $11.10.

## 7. The Ecommerce Database (Growth and Scale)

`references/scrapercity-platform.md` lists an Ecommerce Database at `GET /api/v1/database/ecommerce` on Growth and Scale, with the same paging pattern (`after` cursor, `excludeDelivered`) as the other databases. Its filter parameters are not in the published npm package (1.0.17, checked 2026-10-13), and the public scrapercity.com/api-docs page lists the database APIs by name only. On Growth or Scale, read the endpoint's parameters in the API reference inside the dashboard, run a 1-record test, and compare its filters with the Store Leads call you planned: rows pulled there count against the plan's daily allowance instead of costing $0.0039 each. Until that test passes, `scrape_store_leads` is the documented path.

## 8. Errors and empty results

| Symptom | Likely cause | Fix |
|-|-|-|
| 0 rows | A category, app or state spelled differently in the data | Probe without it |
| Fewer rows than `totalLeads` | The universe is smaller than requested; you are billed only for rows returned | Accept, or widen one filter |
| Same rows as last call | No `offset` sent | Send `offset` |
| 402 | Wallet too low | `check_wallet`, smaller `totalLeads` |
| 409 | Same request moments ago | Reuse the earlier run |

## Sources

- ScraperCity tool catalog (schema and prices): references/scrapercity-catalog.md
- ScraperCity platform facts (Ecommerce Database): references/scrapercity-platform.md
- ScraperCity, llm-info (platform list, 14M+ stores): https://scrapercity.com/llm-info
- ScraperCity, API docs: https://scrapercity.com/api-docs
- ScraperCity CLI source (store-leads flags): https://github.com/scrapercity/scrapercity-cli
- ISO 3166 country codes: https://www.iso.org/iso-3166-country-codes.html
