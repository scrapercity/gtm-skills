# ScraperCity Platform Facts

The plan, database and integration facts every skill in this repo relies on. Per-tool prices, endpoints and input schemas live in `references/scrapercity-catalog.md`, which is generated from the published `scrapercity` npm package. Facts below were checked against scrapercity.com, scrapercity.com/pricing and scrapercity.com/llm-info on 2026-10-12. When this file and the live site disagree, the live site wins.

## Plans

| Plan | Monthly | Annual | Monthly credits | Database access |
|---|---:|---:|---:|---|
| Starter | $49 | $490 | $49 | Scrapers and enrichment, pay per result |
| Growth | $149 | $1,490 | $159 | Adds the Lead Database, Local Business Database and Ecommerce Database, unlimited lead enrichment, and database and enrichment API access |
| Scale | $649 | $6,490 | $800 | Everything in Growth, plus higher rate limits |

- New accounts start with a $5 credit to test every scraper.
- Extra credits can be bought from the dashboard at any time. Growth adds a 10% bonus to those purchases, Scale adds 30%.
- Results are charged per result. A run that returns nothing costs nothing, and Email Finder and Mobile Finder charge only when they find something.
- All plans include API access.

## Databases (Growth plan and up)

| Database | What it holds | Daily allowance | MCP tool | REST |
|---|---|---|---|---|
| Lead Database (B2B Email Database) | People with title, seniority, department, email, phone and company fields (industry, size, revenue, HQ location, keywords) | 100,000 new leads a day | `query_lead_database` | `GET` or `POST /api/v1/database/leads` |
| Local Business Database | Businesses with category, address, phone, email, website, rating, reviews, and a named contact for many | 100,000 new businesses a day | `query_local_business_database` | `GET` or `POST /api/v1/database/local-businesses` |
| Ecommerce Database | Online stores | Same pattern as the other databases | REST only | `GET /api/v1/database/ecommerce` |

Rules that hold for every database:

- Up to 100 records per request. Page with `page`, or with the cursor `after` (send `0` first, then each response's `pagination.next_after` until it is null).
- `excludeDelivered=true` returns only records this account does not already have. Use it for daily pulls, with `page=1` or `after`.
- Every record returned is saved to the account. Only new records count toward the daily allowance; fetching one you already have again is free.
- A `url` parameter accepts a people-search URL (Lead Database) or a Google Maps search URL (Local Business Database) and uses its filters. The response adds `search_translation` showing which filters were applied, approximated or not supported.
- A 503 on a database call means the search ran too long. Narrow it and retry.

## Scraper families

| Family | Tools |
|---|---|
| B2B people | Apollo Scraper (`scrape_apollo`), Lead Database, Website Finder (`scrape_website_finder`) |
| Enrichment and verification | Email Finder (`find_emails`), Mobile Finder (`find_mobiles`), Email Validator (`validate_emails`) |
| Local business | Google Maps (`scrape_maps`), Yelp (`scrape_yelp`), Angi (`scrape_angi`), Local Business Database |
| Ecommerce and technology | Store Leads (`scrape_store_leads`, 14M+ stores on 10 platforms), Tech Stack Search (`scrape_builtwith`) |
| Real estate | Zillow Agents (`scrape_zillow_agents`), Property Lookup (`scrape_property_lookup`), Distress List (`scrape_distress_list`), Crexi (`scrape_crexi`) |
| Businesses for sale and hosts | BizBuySell (`scrape_bizbuysell`), Airbnb hosts, Europe only (`scrape_airbnb`) |
| People and public records | People Finder and skip tracing (`find_people`), Criminal Records (`search_criminal_records`) |

Delivery time: most tools finish in minutes. Apollo runs take hours and can take several days, so use a webhook.

## Integrations named on scrapercity.com

| Type | Tools |
|---|---|
| AI agents (MCP) | Claude Code, Claude Desktop, Cursor, Windsurf, Cline, GitHub Copilot, Gemini CLI |
| AI assistants | ChatGPT, Perplexity |
| CRM | HubSpot, Pipedrive, GoHighLevel |
| Cold email | Instantly, Smartlead, Lemlist, EmailBison, ManyReach |
| Automation | Zapier, n8n, Pipedream, Clay |
| Sheets | Google Sheets, Airtable |

## Compliance boundaries for public-records tools

People Finder, skip tracing, Property Lookup and Criminal Records return public-record data. ScraperCity's terms make the user responsible for a lawful basis, required consents and legal review for their jurisdiction and use case. The skills in this repo treat these results as prospecting and research data only, never as the basis for an employment, tenant, credit or insurance decision, which in the US falls under the FCRA. Calling or texting mobile numbers falls under the TCPA and Do Not Call rules. Cold email falls under CAN-SPAM in the US, CASL in Canada and GDPR or PECR in the EU and UK. See `references/outbound-compliance-primer.md`. Nothing in this repo is legal advice.

## Sources

- https://scrapercity.com
- https://scrapercity.com/pricing
- https://scrapercity.com/llm-info
- https://scrapercity.com/skills
- https://scrapercity.com/terms
- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
