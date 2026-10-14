# Framework Notes: Ecommerce by Tech Stack

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Write a `scrape_store_leads` call, page it, resume it, probe values | `store-leads-parameter-guide.md` |
| Pick filters for a seller type, vertical or app | `filter-recipes.md` |
| Set tier bands from the offer price | `tiering-and-tech-intersection.md` sections 1 to 4 |
| Intersect or exclude a second technology | `tiering-and-tech-intersection.md` section 5 |
| Flag stores that reviewed a competitor app at 1 or 2 stars | `tiering-and-tech-intersection.md` section 6 |
| Add a named founder or ecommerce lead by tier | `tiering-and-tech-intersection.md` section 7 |
| Normalize domains and emails, bucket validation results | `references/list-quality-standard.md` (shared) |
| Send to role inboxes on Google Workspace or Microsoft 365 | `references/deliverability-primer.md` (shared) |
| Quote a price or a parameter | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### ScraperCity catalog and site

The catalog (generated from npm package 1.0.17) defines every `scrape_store_leads` parameter used here, including the server-side visits, sales and employee filters with their aliases, `offset` paging with `nextOffset`, `resumeFromLead`, `planExclude`, and `apps` limited to Shopify. It prices Store Leads at $0.0039 per lead and Tech Stack Search (`scrape_builtwith`) at $4.99 per technology. Per scrapercity.com, the store data covers 14M+ stores across 10 platforms: Shopify, WooCommerce, Magento, BigCommerce, Squarespace, Ecwid, OpenCart, Webflow, PrestaShop and Demandware.

Applied rules: filter bands in the call, page with `offset`, probe values before large pulls, one app per call.

### Shopify plans and the App Store

Shopify lists Shopify Plus at $2,300 a month on a 3-year term and $2,500 a month on a 1-year term, with a variable platform fee for more complex businesses. A Plus store usually has a team, an agency bench and a procurement step, which changes the sales motion. Applied rule: `planExclude: ["Shopify Plus"]` for offers priced for smaller stores; a separate enterprise campaign for Plus.

The Shopify App Store lists Klaviyo (email and SMS), Recharge (subscriptions) and Gorgias (helpdesk). An installed app is evidence of a paid tool and a workflow the store already runs. Applied rule: the qualifying app should connect to the offer in one sentence ("you run Klaviyo, we build the flows"), or it is not a good filter.

Each App Store review shows the store name, country, time using the app and date, and the reviews page filters by star rating (checked 2026-10-13). Applied rule: 1 and 2 star reviewers of the app the user replaces, matched to a Store Leads pull of that app's users, are the first campaign.

### Alex Berman

alexberman.com tells senders to build the list after the offer and to test about 100 emails to one tight niche with one proven result in the first line. Applied rule: one tier and one category per sequence, with proof from the same category.

### Google, Yahoo and Microsoft sender requirements

Since February 2024 Google and Yahoo require bulk senders to authenticate, offer one-click unsubscribe and stay under a 0.3% spam rate (Google recommends under 0.1%); Microsoft added similar requirements for high-volume senders to Outlook domains from May 2025. Store inboxes sit on these providers. Applied rule: validate every address, send only `valid` from the main file, and keep catch-all stores in a separate campaign that pauses at 2% hard bounces over 200 sends (Alex Berman's 2% line, Instantly's 200-send window, per `references/deliverability-primer.md`).

## What this skill does not do

- Quote a store's estimated revenue back to it. Estimates are modeled and used for banding; a wrong number in line one tells the founder the email came from a tool.
- Treat Tech Stack Search output as a store list. It is a domain list to join against.
- Promise app coverage. Detection depends on what each store's site exposes.

## Sources

- ScraperCity tool catalog: references/scrapercity-catalog.md
- ScraperCity, llm-info: https://scrapercity.com/llm-info
- Shopify Plus pricing: https://www.shopify.com/plus/pricing
- Shopify App Store, Klaviyo: https://apps.shopify.com/klaviyo-email-marketing
- Shopify App Store, Recharge: https://apps.shopify.com/subscription-payments
- Shopify App Store, Gorgias: https://apps.shopify.com/helpdesk
- Shopify App Store, Klaviyo reviews filtered by rating: https://apps.shopify.com/klaviyo-email-marketing/reviews?ratings%5B%5D=1
- Alex Berman, B2B lead generation: https://alexberman.com/b2b-lead-generation
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders: https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
