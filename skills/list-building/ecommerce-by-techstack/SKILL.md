---
name: ecommerce-by-techstack
description: >-
  Builds a list of online stores filtered by platform, category, installed
  Shopify apps, technologies, location, social presence and estimated
  traffic, sales or headcount bands with ScraperCity Store Leads ($0.0039 per
  lead, band filters applied server-side), intersects or excludes a second
  technology with Tech Stack Search ($4.99 per technology), keeps only stores
  with an email, validates them, tiers them by size and exports a CSV. Use when
  the user asks for "Shopify apparel stores using Klaviyo", "stores with
  Recharge", "WooCommerce stores in Germany", "ecommerce leads by tech stack",
  "DTC brands doing $50k a month", or "Shopify stores without Gorgias".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [ecommerce, shopify, woocommerce, technographics, store-leads, tech-stack, klaviyo, dtc]
  related_skills: [icp-list-builder, cold-email-list, email-list-cleaner, decision-maker-finder, tam-builder, cold-email-copywriting, scrapercity-api]
  frameworks:
    - "Shopify - plan tiers and Shopify Plus pricing"
    - "Shopify App Store - app listings used as filters (Klaviyo, Recharge, Gorgias)"
    - "Alex Berman - narrow lists tied to one offer and one proof point"
    - "FTC - CAN-SPAM Act compliance guide"
    - "Google, Yahoo and Microsoft - bulk sender requirements (2024-2025)"
    - "ICO - PECR rules for corporate subscribers and sole traders"
    - "CRTC - CASL implied consent for conspicuously published addresses"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, scrapercity-agent-patterns.md, deliverability-primer.md, outbound-compliance-primer.md]
---

# Ecommerce by Tech Stack

## Overview

This skill produces a CSV of online stores that match a platform, a category and a tech stack, each with a validated email and a size tier, plus a report that shows the filters, the test pull, the tier bands, any Tech Stack Search intersection, the funnel and the cost.

It prevents three common failures with ecommerce lists:

1. Pulling every Shopify store and filtering locally. Store Leads bills $0.0039 per lead returned; the visits, sales and employee band filters run server-side, so stores outside the band are never returned or billed. Filter in the call.
2. Paying for the same page twice. Without `offset`, repeat calls with the same filters return the same first page. Page with `offset` or the returned `nextOffset`.
3. Targeting on "has Klaviyo" and nothing else. A store with Klaviyo and $8,000 a month in sales cannot pay a $3,000 retainer. Tier by estimated sales or traffic so the offer and the store size match.

## When to Use

- "Give me Shopify apparel stores that use Klaviyo and have an email, as a CSV."
- "Find subscription brands on Recharge doing over $100k a month."
- "WooCommerce stores in Germany with a phone number."
- "Shopify stores on Gorgias with an Instagram presence."
- "Stores that use Klaviyo but not Attentive" (exclusion).

Use a different skill when:

| The user wants | Use |
|-|-|
| People at ecommerce companies by title (VP Ecommerce, Head of Growth) across the Lead Database | `icp-list-builder` |
| The founder or marketing lead at a list of store domains | `decision-maker-finder` |
| The full market size before choosing a slice | `tam-builder` |
| A send-ready file carried through to the sequencer | `cold-email-list` |
| Validation of a store list they already have | `email-list-cleaner` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| The offer and its monthly price | Sets the tier floor | Ask |
| Platform | `platform` filter; `apps` works on Shopify only | Shopify |
| Category | `category` filter | Ask; probe values with a 25-row test |
| Apps or technologies that qualify a store | `apps` (Shopify) or `technologies` | Ask |
| Apps or technologies that disqualify a store | Tech Stack Search exclusion | None |
| Country, state, city | `countryCode`, `state`, `city` | US |
| Target send-ready count | Sets `totalLeads` per tier | 1,000 |
| Suppression files | Current clients, past unsubscribes | None supplied; say so |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| ScraperCity catalog (`references/scrapercity-catalog.md`) | Every `scrape_store_leads` parameter, the server-side band filters and their aliases, `offset` paging, `apps` being Shopify only, prices for Store Leads and Tech Stack Search. |
| scrapercity.com (per scrapercity.com) | 14M+ stores across 10 platforms: Shopify, WooCommerce, Magento, BigCommerce, Squarespace, Ecwid, OpenCart, Webflow, PrestaShop, Demandware. |
| Shopify plan pricing | Shopify Plus starts at $2,300 a month on a 3-year term or $2,500 on a 1-year term. A Plus store has budget; `planExclude: ["Shopify Plus"]` removes it when the offer is built for smaller stores. |
| Shopify App Store listings | Klaviyo (email and SMS), Recharge (subscriptions), Gorgias (helpdesk) are listed apps. An installed app tells you what the store already pays for and what problem it already has. |
| Alex Berman (alexberman.com) | Build the list after the offer, and test about 100 emails to one tight niche with one proven result. "Shopify apparel on Klaviyo at $50k to $250k a month" is a niche; "ecommerce" is a market. |
| FTC CAN-SPAM, ICO PECR, CRTC CASL | US: no B2B exemption, opt-out within 10 business days. UK: corporate subscribers may receive B2B email without prior consent, sole traders need consent. Canada: implied consent can apply to a conspicuously published address when the message relates to the recipient's role. |
| Google, Yahoo, Microsoft sender rules | Store inboxes are often role addresses on Google Workspace or Microsoft 365. Validate before sending and keep complaints under 0.3%. |

Details and the routing table: `references/framework-notes.md`.

## Workflow

### 1. Turn the offer into a tier floor

Ask what the offer costs per month. House starting point (test it): the store's estimated monthly sales should be at least 20 times the offer's monthly price, so the offer is 5% of sales or less. A $2,500 a month retainer implies a $50,000 a month sales floor for the core tier. Write the tiers as non-overlapping bands of `minEstimatedMonthlySales` and `maxEstimatedMonthlySales` (or visits, or employees). Band presets are in `references/tiering-and-tech-intersection.md`.

### 2. Pick a recipe and build the filters

Start from `references/filter-recipes.md` (recipes by seller type and by app). Always set `emails: true` for an email list and `phones: true` for a call list. Use `apps` only with `platform: "shopify"`; for other platforms use `technologies`. Every parameter, its type and its behavior is in `references/store-leads-parameter-guide.md`.

### 3. Probe values with a 25-row test

The catalog documents `platform` and `category` as case-insensitive strings and `apps` and `technologies` as strings, with no list of allowed values. Run the draft with `totalLeads: 25` ($0.0975). Read the returned category, apps and technologies columns, and copy the exact app or technology name you see into the filter. A 25-row result under 25 rows means the universe for those filters is that small; widen.

### 4. Size each tier and confirm the cost

There is no count endpoint for Store Leads. Plan each tier's `totalLeads` from the target, adding 35% headroom for validation and dedupe losses. Cost ceiling = sum of `totalLeads` x $0.0039, plus $4.99 per Tech Stack Search technology, plus validation at $0.0072 per email. Run `check_wallet`; over $5, show the table and wait for a go-ahead.

### 5. Pull each tier with offset paging

One run per tier, same filters, different band. For a tier larger than one run, page: `offset: 0`, then the `nextOffset` the response returns (or the previous offset plus `totalLeads`). If a run is cancelled, restart with `resumeFromLead`. Set `fileName` per tier so `list_runs` and the dashboard show it.

### 6. Intersect or exclude with Tech Stack Search

Store Leads takes one `apps` and one `technologies` string per call, and has no "not installed" filter. For a second required technology, or to exclude stores using a competitor, run `scrape_builtwith` once per technology ($4.99 flat), normalize the returned domains, and join on domain:

| Goal | Join |
|-|-|
| Stores with app A and technology B | Store Leads `apps: A` rows whose domain is in the B domain list |
| Stores with app A but not B (for example Klaviyo without Attentive) | Store Leads `apps: A` rows whose domain is not in the B list |
| Flag a signal without filtering (subscription brands) | Add `uses_<tech> = true` for domains in the list |

Procedure and domain normalization: `references/tiering-and-tech-intersection.md`.

### 7. Normalize, dedupe, suppress, validate

Normalize domains and emails per `references/list-quality-standard.md`. Drop platform-host domains (`*.myshopify.com` when a custom domain exists). Dedupe on domain, then on email (one brand can run several storefronts with one inbox). Apply suppression. Validate every email with `validate_emails`. Store emails are often role addresses (`hello@`, `support@`); for store lists those are acceptable, as on local business lists, but keep `is_role` so copy can say "your team".

### 8. Optional: add a named contact

For Tier 1, find the founder or head of ecommerce: `scrape_website_finder` with the domains and `jobTitle: "Founder"` ($0.0499 per contact found), or `query_lead_database` with `companyDomain` on Growth and Scale. Validate those emails too.

### 9. Deliver

One CSV with a `tier` column, a hold file for catch-all and unknown, and the report from `templates/output-template.md`. Run `scripts/check-output.py`.

## ScraperCity Implementation

### Tools and prices (from `references/scrapercity-catalog.md`)

| Step | Tool | Price |
|-|-|-|
| Balance | `check_wallet` | Free |
| Store pull | `scrape_store_leads` | $0.0039 per lead |
| Second technology, exclusion | `scrape_builtwith` (Tech Stack Search) | $4.99 per technology |
| Validation | `validate_emails` | $0.0072 per email |
| Named contact | `scrape_website_finder` | $0.0499 per contact found |
| Named contact (Growth plan) | `query_lead_database` with `companyDomain` | Included |

### Store Leads call with every filter family

```json
{
  "platform": "shopify",
  "category": "apparel",
  "apps": "Klaviyo",
  "countryCode": "US",
  "state": "California",
  "emails": true,
  "phones": false,
  "instagram": true,
  "tiktok": true,
  "planExclude": ["Shopify Plus"],
  "minEstimatedMonthlySales": 50000,
  "maxEstimatedMonthlySales": 249999,
  "minEstimatedMonthlyVisits": 20000,
  "minEmployeeCount": 2,
  "maxEmployeeCount": 50,
  "totalLeads": 500,
  "offset": 0,
  "fileName": "shopify-apparel-klaviyo-ca-t2"
}
```

Not every call needs every filter; each one narrows the result. `technologies` takes a technology name string for non-Shopify platforms (for example `"platform": "woocommerce", "technologies": "Klaviyo"`). `city`, `facebook`, `youtube`, `linkedin`, `twitter` and `pinterest` work the same way as their siblings above. Aliases: `visitsMin`, `visitsMax`, `salesMin`, `salesMax`, `employeesMin`, `employeesMax`.

CLI: `npx scrapercity store-leads` takes platform, country, category, city, technologies, apps, total-leads, name and the emails, phones, instagram, facebook, tiktok, youtube and linkedin switches in package 1.0.17. The band filters, `state`, `planExclude`, `offset`, `twitter` and `pinterest` are MCP and REST only: `POST https://app.scrapercity.com/api/v1/scrape/store-leads` with the JSON body above.

### Tech Stack Search call

```json
{"technology": "Recharge", "fileName": "techstack-recharge-20261013"}
```

Returns the domains detected using that technology, for $4.99 per technology. The list covers all websites, not only stores, so always join it to a Store Leads pull.

### Worked cost estimate

Shopify apparel stores in the US using Klaviyo with an email, three sales tiers, target about 1,150 send-ready, Recharge flagged.

| Line | Units | Unit price | Cost |
|-|-:|-:|-:|
| 25-row value probe | 25 leads | $0.0039 | $0.10 |
| Tier 1 pull, sales $250,000 and up | 212 leads (universe smaller than the 300 requested) | $0.0039 | $0.83 |
| Tier 2 pull, $50,000 to $249,999 | 600 leads | $0.0039 | $2.34 |
| Tier 3 pull, $20,000 to $49,999 | 700 leads | $0.0039 | $2.73 |
| Tech Stack Search, Recharge | 1 technology | $4.99 | $4.99 |
| Validation after dedupe and suppression | 1,461 emails | $0.0072 | $10.52 |
| Total | | | $21.51 |

Show the ceiling first (requested 1,625 leads x $0.0039 = $6.34, plus $4.99, plus up to 1,625 x $0.0072 = $11.70 validation, $23.03). Over $5, so wait for a go-ahead.

### Errors

| Code | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, offer fewer tiers. |
| 409 | Same filters submitted moments ago; reuse the earlier run. |
| 429 | Wait 30 seconds, retry once. |
| Run returns 0 rows | A filter value is spelled differently in the data. Remove `apps` or `category`, rerun 25 rows, read the values. |

## Output Format

1. `stores-[segment]-[date].csv`: `domain`, `store_name`, `platform`, `category`, `apps`, `technologies`, `country`, `state`, `city`, `est_monthly_visits`, `est_monthly_sales`, `employees`, social flags, `email`, `is_role`, `email_status`, `email_validated_at`, `tier`, `uses_<tech>` flags, `source = store_leads`, `source_detail`, `pulled_at`. Valid emails only.
2. `stores-[segment]-[date]-hold.csv`: catch-all and unknown.
3. Report from `templates/output-template.md`: target, filters, value probe, tier bands, Tech Stack Search, funnel, validation, cost, sample rows, next steps.

## Quality Check

- [ ] Every filter name exists in the `scrape_store_leads` schema, and `emails: true` is set for an email list.
- [ ] `apps` appears only with `platform: "shopify"`.
- [ ] A 25-row probe ran and the app and category values match what the data returned.
- [ ] Tier bands do not overlap and each tier was pulled with server-side band filters.
- [ ] Every multi-page tier used `offset` or `nextOffset`; no page was bought twice.
- [ ] Tech Stack Search lists were joined on normalized domains and each technology cost $4.99.
- [ ] Main CSV is 100% `email_status = valid`; 0 duplicate domains; suppression applied.
- [ ] Funnel adds up and the tier counts sum to the send-ready total.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Filtering size after the pull | Billed for every store outside the band | Band filters in the call; they run server-side |
| Repeating a call without `offset` | Same first page returned and billed again | `offset` 0, then `nextOffset` |
| `apps` on WooCommerce | `apps` is Shopify only | `technologies` for other platforms |
| Guessing app names ("klaviyo-email") | 0 rows or partial matches | 25-row probe, copy the name from the data |
| Two apps in one `apps` string | Behavior with several values is not documented | One app per call; intersect with Tech Stack Search |
| Using Tech Stack Search alone as the list | Returns every website using the tech, stores or not, with no email | Join to Store Leads on domain |
| No `planExclude` for an SMB offer | Plus stores have procurement and agencies on retainer | `planExclude: ["Shopify Plus"]` |
| Sending to `support@` with a sales pitch | Lands with a support team that tags it spam | Prefer `hello@`, `info@` or a founder; tailor copy to "your team" |
| One sequence for all tiers | A $20k a month store and a $500k store need different proof | Sequence per tier |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/store-leads-parameter-guide.md` | Writing any `scrape_store_leads` call: every parameter, alias, paging, value probing. |
| `references/filter-recipes.md` | Choosing filters by seller type, vertical or app. |
| `references/tiering-and-tech-intersection.md` | Setting tier bands from the offer, joining Tech Stack Search lists, exclusions. |
| `references/list-quality-standard.md` | Normalization, dedupe, validation buckets (shared). |
| `references/deliverability-primer.md` | Sending to role inboxes on Google Workspace and Microsoft 365 (shared). |
| `references/outbound-compliance-primer.md` | CAN-SPAM, CASL, PECR, GDPR before sending (shared). |
| `references/scrapercity-catalog.md` | Prices and schemas (shared). |
| `references/scrapercity-platform.md` | Plans and the Ecommerce Database (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet, polling, retries (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished report for Shopify apparel stores using Klaviyo. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `icp-list-builder` for people-first lists at ecommerce companies.
- `decision-maker-finder` for founders and marketing leads at the store domains.
- `tam-builder` to size every store in a category before choosing tiers.
- `cold-email-list` and `email-list-cleaner` to carry the file to a sequencer.
- `cold-email-copywriting` for tier-specific copy that cites the installed app.
- `scrapercity-api` for REST loops over many tiers or countries.
