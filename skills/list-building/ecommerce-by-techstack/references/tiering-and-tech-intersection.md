# Tiering and Tech Intersection

How to set size tiers from the offer, pull them with server-side band filters, and combine Store Leads with Tech Stack Search lists.

## 1. From offer price to tier floor

Core tier floor = offer monthly price x the affordability ratio. The ratio is the user's input: no published benchmark sets how much of a store's sales an offer may take. Set it from current clients: divide each client's estimated monthly sales by what they pay per month and use the lowest result that still renewed. The table shows the arithmetic at the worked example's 20x:

| Offer monthly price | Core tier floor at 20x (sales per month) | Stretch tier (below floor, smaller ask) |
|-:|-:|-:|
| $300 (app subscription) | $6,000 | none; the app is self-serve |
| $1,000 | $20,000 | $10,000 to $19,999 with a lighter package |
| $2,500 | $50,000 | $20,000 to $49,999 with a project, not a retainer |
| $5,000 | $100,000 | $50,000 to $99,999 |
| $10,000 | $200,000 | $100,000 to $199,999 |

One-time projects: the user states the months the fee should be spread over, and the fee divided by those months is the monthly price (the worked example spreads a $3,000 build over 3). Usage-priced software: use the price at the store's expected volume.

## 2. Tier band presets

Bands are inclusive on the floor and exclusive above it, written as max = next floor minus 1, so no store falls in two tiers.

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

## 6. Unhappy users of a competitor app (displacement flag)

The Shopify App Store reviews page for any app lists each reviewer's store name, country, time using the app and review date, and can be filtered by star rating (for example `apps.shopify.com/<app-handle>/reviews?ratings[]=1`; checked 2026-10-13 on the Klaviyo listing). A store that left a 1 or 2 star review of the app you replace in the last 12 months has told the public what it dislikes.

1. Pull the stores running the competitor app with Store Leads (`apps: "<Competitor>"`, bands and `emails: true` as usual).
2. Copy the 1 and 2 star reviewers from the last 12 months: store name, country, date, a five-word summary of the complaint.
3. Build `business_name_key` (lowercase, punctuation and legal suffix removed) for both lists and match on it plus country.
4. Flag matches `unhappy_with_<app> = true` and keep the complaint summary in a `review_note` column for the copywriter.
5. Send the flagged stores first, in their own campaign; the first line names the outcome they asked for in the review, never the review itself.

Matches are usually a small share of the pull. The flag costs nothing beyond the Store Leads rows you were buying anyway.

## 7. Named contacts by tier

Role inboxes (`hello@`, `info@`, `team@`) reach small stores, where the founder reads them. Larger stores route them to support. Add a named person where the buyer is no longer the founder.

| Tier or band | Title to look for, in order | Contacts per store | How |
|-|-|-|-|
| E3, or T3 and T4 | Founder, Owner, CEO | 1 named, plus the role inbox as a fallback row | Growth plan: Lead Database by `companyDomain` (included). Starter: skip; the role inbox is the founder's inbox |
| E2, or T2 | Founder or CEO, then Head of Ecommerce, Ecommerce Manager, Marketing Manager, Head of Growth | Up to 2 | Lead Database by `companyDomain` on Growth; Website Finder ($0.0499 per contact found) with "Founder" on Starter |
| E1, or T1 | Director or VP of Ecommerce, Head of Digital, Director of Retention or CRM, CMO | Up to 2 | Lead Database by `companyDomain`, then Website Finder for misses; Email Finder ($0.05 per email found) when a name is known but the email is not |

Rules:

- Two contacts at one store go in the same campaign, so a reply from either one stops the sequence for both.
- Validate every named email, including Website Finder results when `autoValidateEmails` was off.
- When the named contact and the role inbox are both valid, send to the named contact; keep the role inbox in a hold file for a later touch.
- The `contact_source` column records where the name came from, so the next pull can skip stores already covered.

## 8. Tier report table

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
- Alex Berman, B2B lead generation (list after the offer, test about 100 emails per niche): https://alexberman.com/b2b-lead-generation
- Shopify App Store, Klaviyo reviews filtered to 1 star (store name, country, time using the app and date shown per review; checked 2026-10-13): https://apps.shopify.com/klaviyo-email-marketing/reviews?ratings%5B%5D=1
