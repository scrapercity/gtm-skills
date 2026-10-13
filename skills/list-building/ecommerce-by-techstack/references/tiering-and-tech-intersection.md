# Tiering and Tech Intersection

How to set size tiers from the offer, pull them with server-side band filters, and combine Store Leads with Tech Stack Search lists.

## 1. From offer price to tier floor

House rule (a starting point to test, October 2026): a store should be able to pay for the offer with no more than 5% of its estimated monthly sales. That gives a floor of 20 times the monthly price.

| Offer monthly price | Core tier floor (sales per month) | Stretch tier (below floor, smaller ask) |
|-:|-:|-:|
| $300 (app subscription) | $6,000 | none; the app is self-serve |
| $1,000 | $20,000 | $10,000 to $19,999 with a lighter package |
| $2,500 | $50,000 | $20,000 to $49,999 with a project, not a retainer |
| $5,000 | $100,000 | $50,000 to $99,999 |
| $10,000 | $200,000 | $100,000 to $199,999 |

One-time projects: divide the project fee by 3 and treat it as a monthly price. Usage-priced software: use the price at the store's expected volume.

## 2. Tier band presets

Bands are inclusive on the floor and exclusive above it, written as max = next floor minus 1, so no store lands in two tiers.

### By estimated monthly sales (USD)

| Tier | `minEstimatedMonthlySales` | `maxEstimatedMonthlySales` | Typical use |
|-|-:|-:|-|
| T1 | 250,000 | (none) | Founder plus a team; agencies on retainer; custom proof |
| T2 | 50,000 | 249,999 | Core SMB retainer tier |
| T3 | 20,000 | 49,999 | Projects, productized offers |
| T4 | 5,000 | 19,999 | Self-serve software only |

### By estimated monthly visits

| Tier | `minEstimatedMonthlyVisits` | `maxEstimatedMonthlyVisits` | Use when |
|-|-:|-:|-|
| V1 | 500,000 | (none) | The offer scales with traffic (CRO, onsite search, chat) |
| V2 | 100,000 | 499,999 | |
| V3 | 20,000 | 99,999 | |
| V4 | 5,000 | 19,999 | |

### By employees

| Tier | `minEmployeeCount` | `maxEmployeeCount` | Use when |
|-|-:|-:|-|
| E1 | 51 | (none) | The buyer is a department head |
| E2 | 11 | 50 | A marketing or ops hire exists |
| E3 | 1 | 10 | Founder is the buyer |

Combine one band family with the others only when needed; every extra band filter shrinks the pool.

## 3. Sizing each tier's pull

```text
pull_n(tier) = ceil(target_send_ready(tier) / expected_survival)
expected_survival = 0.75 as a first guess (validation, dedupe and suppression losses); replace with measured values
cost(tier) = pull_n(tier) x $0.0039
```

If a tier returns fewer rows than requested, that is the universe for those filters. You pay only for the rows returned.

## 4. Sequencing by tier

| Tier | Proof to cite | Ask |
|-|-|-|
| T1 | A named result at a store of similar size, or a teardown of their current flows | 20-minute call |
| T2 | A case study from the same category | Short call or a free audit |
| T3 | A productized package and price | Reply to get the one-pager |
| T4 | Self-serve signup or a free trial | Link |

Keep one sequence per tier; the tier is written in the CSV so the sequencer can split.

## 5. Tech Stack Search: what it returns and how to join it

`scrape_builtwith` (Tech Stack Search) takes one `technology` string and returns the domains detected using it, for $4.99 per technology. The list covers every kind of site, not only stores.

### Join procedure

1. Download the Tech Stack Search CSV and the Store Leads CSVs.
2. Normalize every domain on both sides: lowercase; strip scheme, `www.`, path, query, port; reduce to the registrable domain with the Public Suffix List (`shop.brand.co.uk` to `brand.co.uk`).
3. For Store Leads rows on a `*.myshopify.com` host with a custom domain also present, use the custom domain.
4. Build a set from the Tech Stack Search domains.
5. Intersect (keep rows whose domain is in the set), subtract (keep rows not in it), or flag (`uses_<tech> = true`).
6. Report: technology, cost, domains returned, matches in the store list, rows kept.

### When Tech Stack Search beats a second Store Leads pull

| Situation | Better choice |
|-|-|
| The second technology is common (thousands of stores) | Tech Stack Search: $4.99 flat versus $0.0039 per row for a pull of the same size, which passes $4.99 at about 1,280 rows |
| You need to exclude a technology | Tech Stack Search (Store Leads cannot exclude apps) |
| You need the second app's stores with emails and bands | A second Store Leads pull, then union or intersect |
| The second technology is rare (under about 1,000 stores) | Either; a banded Store Leads pull also gives emails |

### Caveats

- Detection lists lag installs and removals. A store that removed an app recently can still appear; one that added it yesterday can be missing.
- Some technologies run on checkout or app subdomains; registrable-domain normalization catches most of these.
- Tech Stack Search names follow the technology's public name. Probe a new name with the cheapest possible check: run it, read the row count, and compare against expectations before building a campaign on it.

## 6. Tier report table

Each report includes this table; the checker confirms bands do not overlap and the send-ready counts add up.

| Tier | minEstimatedMonthlySales | maxEstimatedMonthlySales | Pulled | Send-ready | Sequence |
|-|-|-|-|-|-|
| T1 | 250,000 | none | 212 | 171 | T1 teardown |
| T2 | 50,000 | 249,999 | 600 | 470 | T2 case study |
| T3 | 20,000 | 49,999 | 700 | 542 | T3 package |

## Sources

- ScraperCity tool catalog (band filters, Tech Stack Search price): references/scrapercity-catalog.md
- Shopify Plus pricing: https://www.shopify.com/plus/pricing
- Public Suffix List: https://publicsuffix.org/
- Alex Berman, cold email list and offer guidance: references/alex-berman-cold-email.md
