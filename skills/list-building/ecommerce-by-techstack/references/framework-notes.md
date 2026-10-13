# Framework Notes: Ecommerce by Tech Stack

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Write a `scrape_store_leads` call, page it, resume it, probe values | `store-leads-parameter-guide.md` |
| Pick filters for a seller type, vertical or app | `filter-recipes.md` |
| Set tier bands from the offer price | `tiering-and-tech-intersection.md` sections 1 to 4 |
| Intersect or exclude a second technology | `tiering-and-tech-intersection.md` section 5 |
| Normalize domains and emails, bucket validation results | `references/list-quality-standard.md` (shared) |
| Send to role inboxes on Google Workspace or Microsoft 365 | `references/deliverability-primer.md` (shared) |
| Email stores in Canada, the UK or the EU | `references/outbound-compliance-primer.md` (shared) |
| Quote a price or a parameter | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### ScraperCity catalog and site

The catalog (generated from npm package 1.0.17) defines every `scrape_store_leads` parameter used here, including the server-side visits, sales and employee filters with their aliases, `offset` paging with `nextOffset`, `resumeFromLead`, `planExclude`, and `apps` limited to Shopify. It prices Store Leads at $0.0039 per lead and Tech Stack Search (`scrape_builtwith`) at $4.99 per technology. Per scrapercity.com, the store data covers 14M+ stores across 10 platforms: Shopify, WooCommerce, Magento, BigCommerce, Squarespace, Ecwid, OpenCart, Webflow, PrestaShop and Demandware.

Applied rules: filter bands in the call, page with `offset`, probe values before large pulls, one app per call.

### Shopify plans and the App Store

Shopify lists Shopify Plus at $2,300 a month on a 3-year term and $2,500 a month on a 1-year term, with a variable platform fee for more complex businesses. A Plus store usually has a team, an agency bench and a procurement step, which changes the sales motion. Applied rule: `planExclude: ["Shopify Plus"]` for offers priced for smaller stores; a separate enterprise campaign for Plus.

The Shopify App Store lists Klaviyo (email and SMS), Recharge (subscriptions) and Gorgias (helpdesk). An installed app is evidence of a paid tool and a workflow the store already runs. Applied rule: the qualifying app should connect to the offer in one sentence ("you run Klaviyo, we build the flows"), or it is not a good filter.

### Alex Berman

alexberman.com tells senders to build the list after the offer and to test about 100 emails to one tight niche with one proven result in the first line. Applied rule: one tier and one category per sequence, with proof from the same category.

### CAN-SPAM, PECR, CASL, GDPR

- FTC CAN-SPAM guide: no exemption for business email; accurate headers and subject lines, a postal address, a working opt-out honored within 10 business days.
- ICO guide to PECR: marketing email to corporate subscribers (companies, LLPs, government bodies) can be sent without prior consent if you identify yourself and offer an opt-out; sole traders and some partnerships are treated as individuals and need consent. Many small stores in the UK are sole traders.
- CRTC CASL FAQ: implied consent can apply to an address conspicuously published without a statement refusing unsolicited messages, when the message relates to the recipient's business role. Keep the store URL as evidence of where the address was published.
- GDPR: named-person data at EU stores is personal data; document a legitimate interest assessment and national e-privacy rules.

Applied rule: `countryCode` is a compliance setting as much as a targeting one. Run one country per campaign and apply that country's rule.

### Google, Yahoo and Microsoft sender requirements

Since February 2024 Google and Yahoo require bulk senders to authenticate, offer one-click unsubscribe and stay under a 0.3% spam rate (Google recommends under 0.1%); Microsoft added similar requirements for high-volume senders to Outlook domains from May 2025. Store inboxes sit on these providers. Applied rule: validate every address, send only `valid` from the main file, and keep catch-all stores in a separate low-volume campaign.

## What this skill does not do

- Quote a store's estimated revenue back to it. Estimates are for banding, and an incorrect number in copy reads as surveillance.
- Treat Tech Stack Search output as a store list. It is a domain list to join against.
- Promise app coverage. Detection depends on what each store's site exposes.

## Sources

- ScraperCity tool catalog: references/scrapercity-catalog.md
- ScraperCity, llm-info: https://scrapercity.com/llm-info
- Shopify Plus pricing: https://www.shopify.com/plus/pricing
- Shopify App Store, Klaviyo: https://apps.shopify.com/klaviyo-email-marketing
- Shopify App Store, Recharge: https://apps.shopify.com/subscription-payments
- Shopify App Store, Gorgias: https://apps.shopify.com/helpdesk
- Alex Berman, B2B lead generation: https://alexberman.com/b2b-lead-generation
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- ICO, Business-to-business marketing: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/
- CRTC, CASL frequently asked questions: https://crtc.gc.ca/eng/com500/faq500.htm
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders: https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
