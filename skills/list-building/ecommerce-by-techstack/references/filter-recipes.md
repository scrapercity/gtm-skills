# Filter Recipes

Starting filters by what the user sells and by the app or technology that qualifies a store. Every recipe uses only `scrape_store_leads` parameters from the catalog. App, category and technology names below are the public product names; the data may spell them differently, so run the 25-row probe from `store-leads-parameter-guide.md` section 2 before any pull and copy the value the data uses.

Bands below assume the worked example's 20x affordability ratio from `tiering-and-tech-intersection.md` section 1. Recompute them from the user's offer price and ratio before a pull.

## 1. Recipes by what the user sells

| # | Seller | Core filters | Bands | Extra flags | Why these stores |
|-|-|-|-|-|-|
| 1 | Klaviyo or email marketing agency | `platform: shopify`, `apps: Klaviyo` | sales $50,000 to $499,999 | `emails: true`, `planExclude: ["Shopify Plus"]` for SMB retainers | Already pays for Klaviyo; flows and campaigns are missing, and those are the agency's work |
| 2 | Email agency, platform switch pitch | `platform: shopify`, `apps: Mailchimp` | sales $30,000 and up | `emails: true` | Store on a general email tool at a size where ecommerce flows pay back |
| 3 | SMS platform or SMS agency | `platform: shopify`, `apps: Klaviyo` then exclude Attentive and Postscript domains via Tech Stack Search | sales $40,000 and up | `emails: true`, `instagram: true` | Email is running, SMS is not |
| 4 | Subscription app or agency | `platform: shopify`, `apps: Recharge` | sales $20,000 and up | `emails: true` | Subscription revenue in place; pitch retention, churn or migration |
| 5 | Subscription launch for consumables | `platform: shopify`, `category: health` or `food`, then exclude Recharge domains | sales $30,000 and up | `emails: true` | Consumable products with no subscription app yet |
| 6 | CX outsourcing, support agency | `platform: shopify`, `apps: Gorgias` | sales $100,000 and up, `minEmployeeCount: 5` | `emails: true`, `phones: true` | Has ticket volume and a helpdesk; may need people |
| 7 | Helpdesk vendor competing with Gorgias | `platform: shopify`, category of choice, exclude Gorgias domains | sales $50,000 and up | `emails: true` | No Gorgias yet |
| 8 | Reviews and UGC tool | `platform: shopify`, `apps: Judge.me` | sales $30,000 to $300,000 | `instagram: true` | Upgrade pitch from a lighter reviews app |
| 9 | Reviews competitor displacement | `platform: shopify`, `apps: Yotpo` | sales $100,000 and up | `emails: true` | Paying for a premium reviews suite; price or feature switch |
| 10 | Loyalty program vendor | `platform: shopify`, `apps: Smile.io` or `LoyaltyLion` | sales $50,000 and up | `emails: true` | Loyalty in place; upgrade or switch |
| 11 | Upsell and AOV tool | `platform: shopify`, `apps: Klaviyo`, then exclude Rebuy domains via Tech Stack Search | sales $50,000 and up | `emails: true` | Store large enough for AOV gains, no upsell engine yet |
| 12 | Returns software | `platform: shopify`, `category: apparel`, exclude Loop Returns domains | sales $100,000 and up | `emails: true` | Apparel has high return rates and no returns portal yet |
| 13 | 3PL or fulfillment | `platform: shopify`, any category | sales $60,000 to $600,000, `maxEmployeeCount: 25` | `phones: true`, `emails: true` | Big enough to outgrow self-fulfillment, small enough to lack a warehouse |
| 14 | Shipping protection or tracking | `platform: shopify`, `apps: AfterShip` or exclude Route domains | sales $40,000 and up | `emails: true` | Order volume with tracking questions |
| 15 | Paid social creative agency | `platform: shopify`, `category: beauty` or `apparel` | sales $50,000 to $1,000,000 | `instagram: true`, `tiktok: true`, `facebook: true` | Active social presence, likely running ads |
| 16 | TikTok Shop agency | `platform: shopify`, `category: beauty` | sales $30,000 and up | `tiktok: true`, `emails: true` | Already on TikTok; Shop is the next channel |
| 17 | Influencer platform | `platform: shopify` | sales $50,000 and up, visits 50,000 and up | `instagram: true`, `youtube: true` | Audience-led brands |
| 18 | Pinterest ads agency | `platform: shopify`, `category: home` | sales $40,000 and up | `pinterest: true` | Visual home categories with a Pinterest profile |
| 19 | B2B wholesale portal | `platform: shopify`, `category: apparel` or `home` | sales $100,000 and up | `linkedin: true` | Brands with a company page often sell wholesale |
| 20 | Magento to Shopify migration agency | `platform: magento` | sales $100,000 and up | `emails: true`, `phones: true` | Platform migration pitch; band filters keep only budgets that can pay for it |
| 21 | WooCommerce to Shopify migration | `platform: woocommerce`, `technologies: Klaviyo` | visits 20,000 and up | `emails: true` | Serious marketing stack on WooCommerce |
| 22 | WooCommerce plugin or host | `platform: woocommerce`, `countryCode: DE` or `GB` | visits 10,000 and up | `emails: true` | Country-specific campaigns, one language per sequence |
| 23 | BigCommerce partner | `platform: bigcommerce` | sales $50,000 and up | `emails: true`, `phones: true` | Smaller platform ecosystem, fewer agencies chasing it |
| 24 | Squarespace or Webflow store designer | `platform: squarespace` or `webflow` | `maxEstimatedMonthlySales: 30000` | `instagram: true` | Small creative brands that hire designers |
| 25 | Packaging supplier | `platform: shopify`, `category: food` or `beauty` | sales $20,000 to $250,000 | `phones: true` | Physical product volume, still buying from small suppliers |
| 26 | Product photography studio | `platform: shopify`, `category: jewelry` | sales $15,000 to $150,000, `maxEmployeeCount: 10` | `instagram: true`, `city` near the studio | Local, image-heavy category |
| 27 | Local-market agency | `platform: shopify`, `countryCode: US`, `state`, `city` | sales $20,000 and up | `emails: true`, `phones: true` | Meet-in-person pitch |
| 28 | Enterprise ecommerce consultancy | `platform: shopify` | `minEstimatedMonthlySales: 1000000`, `minEmployeeCount: 50` | `linkedin: true` | Plus-scale budgets and procurement |

## 2. Recipes by vertical (category probes)

Run the probe with the plain word first; the data's category labels decide the final string.

| Vertical | First probe value | Typical apps to test as qualifiers | Notes |
|-|-|-|-|
| Apparel | `apparel` | Klaviyo, Loop Returns, Gorgias | High return rates; returns and CX offers fit |
| Beauty and cosmetics | `beauty` | Klaviyo, Yotpo, Recharge | Replenishment and reviews drive revenue |
| Supplements and wellness | `health` | Recharge, Klaviyo | Subscriptions; check claims rules before copy |
| Pet | `pet` | Recharge, Klaviyo | Consumables, subscription-friendly |
| Coffee and tea | `food` | Recharge | Subscription heavy |
| Home and furniture | `home` | Klaviyo, Rebuy | High AOV, long consideration |
| Jewelry | `jewelry` | Judge.me, Klaviyo | Image-driven, gift seasons |
| Sports and outdoors | `sports` | Klaviyo, AfterShip | Seasonal peaks |
| Baby and kids | `baby` | Recharge, Klaviyo | Life-stage flows |
| Electronics accessories | `electronics` | AfterShip, Gorgias | Support volume |

## 3. Exclusion recipes with Tech Stack Search

Store Leads has no "not installed" filter. Use one Tech Stack Search run per excluded technology ($4.99 each) and subtract on domain.

| Pitch | Pull | Exclude | Cost of exclusion |
|-|-|-|-|
| SMS for Klaviyo stores without SMS | `apps: Klaviyo` | Attentive, Postscript | $9.98 |
| Helpdesk for stores without one | category pull | Gorgias, Zendesk | $9.98 |
| Reviews for stores without a reviews app | category pull | Yotpo, Judge.me, Okendo, Loox | $19.96 |
| Subscriptions for consumables without one | `category: health` | Recharge | $4.99 |
| Returns portal | `category: apparel` | Loop Returns | $4.99 |

Exclusions are only as complete as the technology lists. A store that removed an app last month can still appear in the list, and a store that installed one yesterday can be missing from it. Say so in the report.

## 4. Social flag combinations

| Flags | Signal |
|-|-|
| `instagram` + `tiktok` | Content-led brand, likely runs paid social |
| `youtube` | Long-form content or tutorials; influencer budget |
| `pinterest` | Visual categories, often home, wedding, fashion |
| `linkedin` | Company page; often wholesale, B2B or a larger team |
| `facebook` only | Older or local store |
| None | Founder-run or early store; pair with low bands |

## 5. Per-tier filter template

```json
{"platform": "shopify", "category": "apparel", "apps": "Klaviyo", "countryCode": "US",
 "emails": true, "minEstimatedMonthlySales": 50000, "maxEstimatedMonthlySales": 249999,
 "totalLeads": 600, "offset": 0, "fileName": "shopify-apparel-klaviyo-us-t2"}
```

Copy it once per tier and change only the band, `totalLeads` and `fileName`.

## Sources

- ScraperCity tool catalog (parameters): references/scrapercity-catalog.md
- Shopify App Store, Klaviyo: https://apps.shopify.com/klaviyo-email-marketing
- Shopify App Store, Recharge: https://apps.shopify.com/subscription-payments
- Shopify App Store, Gorgias: https://apps.shopify.com/helpdesk
- Shopify App Store: https://apps.shopify.com/
- Shopify Plus pricing: https://www.shopify.com/plus/pricing
- ScraperCity, llm-info (platform list): https://scrapercity.com/llm-info
