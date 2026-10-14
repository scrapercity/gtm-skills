# CSV Mapping and Import

How a ScraperCity file becomes a sequencer campaign: the source columns per tool, the normalized columns this repo uses, the variable names each platform expects, fallbacks for empty cells, and the import procedure with dedupe and suppression. Normalized column names follow `references/list-quality-standard.md` section 2. Platform limits were read from vendor docs on 2026-10-13.

Rule one: open the header row of every downloaded CSV or the first JSON record before mapping. Field names below come from the `scrapercity` npm package docs and the integration pages on scrapercity.com; a tool version can add or rename a column.

## 1. Source columns by ScraperCity tool

### 1a. Lead Database (`query_lead_database`, Growth plan and up)

Company fields per the package docs: `company_industry`, `company_size`, `employees_count`, `company_website`, `company_annual_revenue`, `company_city`, `company_state`, `company_country`, `keywords`. Person fields as used on the scrapercity.com integration pages: `first_name`, `last_name`, `email`, `title`, `company_name`, `company_domain`, `linkedin_url`, `mobile_number`, `city`, `state`, `country`, `seniority`, `department`, `company_linkedin`.

| Source column | Normalized column | Notes |
|-|-|-|
| `first_name` | `first_name` | Title-case only if ALL CAPS or all lower |
| `last_name` | `last_name` | Move credentials (MBA, CPA) out |
| `email` | `email` | Lowercase for matching |
| `title` | `title` | Keep raw; shorten for copy in a separate `title_short` |
| `company_name` | `company_name` | Strip legal suffixes in a `company_short` column for copy |
| `company_domain` | `company_domain` | Registrable domain |
| `linkedin_url` | `linkedin_url` | No query string |
| `mobile_number` | `mobile` | E.164; keep out of the sequencer unless calls are a step |
| `city`, `state`, `country` | `person_city`, `person_state`, `person_country` | Drives time zone |
| `company_industry` | `company_industry` | Plain words for copy: "software" not "computer software" |
| `employees_count` | `company_employees` | Integer; band word for copy |

### 1b. Local Business Database (`query_local_business_database`)

Fields per the package docs: `title` (business name), `category_name`, `address`, `city`, `state`, `postal_code`, `country_code`, `phone`, `website`, `emails`, `total_score`, `reviews_count`, `lat`, `lng`, and when a named contact exists `contact_first_name`, `contact_last_name`, `contact_job_title`, `contact_email`, `contact_mobile`.

| Source column | Normalized column | Notes |
|-|-|-|
| `contact_first_name` | `first_name` | Fallback "there" when blank |
| `contact_last_name` | `last_name` | |
| `contact_email`, else first address in `emails` | `email` | One row per business unless several named contacts are wanted |
| `title` | `business_name` | Watch the name clash: Local `title` is the business, Lead Database `title` is the job |
| `contact_job_title` | `title` | |
| `category_name` | `category` | Lowercase singular for copy |
| `city`, `state`, `postal_code` | `city`, `state`, `postal_code` | ZIP as text |
| `phone` | `phone` | E.164 |
| `website` | `website`, `domain` | Blank `domain` for social-only sites |
| `total_score` | `rating` | One decimal |
| `reviews_count` | `reviews` | Integer |

### 1c. Google Maps scraper (`scrape_maps`, $0.0099 per business)

The listing fields match the Local Business Database set used throughout this repo (business name, category, address, phone, website, rating, review count). Scraper CSV headers can differ in case or naming from the database JSON, so map from the downloaded header row. Maps listings carry no named contact: route rows to a non-personalized variant or enrich first (`scrape_website_finder` with `domains` and one `jobTitle`, $0.0499 per contact found).

### 1d. Store Leads (`scrape_store_leads`, $0.0039 per lead)

The tool filters by `platform`, `category`, `apps`, `technologies`, location, estimated monthly visits and sales, and employee count, and can require `emails` or `phones`. The CSV carries store-level fields along those lines (store name, domain, platform, category, apps, technologies, contact emails and phones, location). Read the header row and map:

| Store Leads field | Normalized column | Notes |
|-|-|-|
| Store name | `company_name` | Strip ".com" duplicates |
| Domain | `company_domain` | Key for joining people from the Lead Database (`companyDomain` filter) |
| Platform | `platform` | "Shopify", "WooCommerce" |
| Apps | `app_trigger` | The one installed app that matches the offer |
| Store email | `email` | Often a role address (info@, hello@); run as its own variant |
| Category | `category` | Lowercase plural for copy |

### 1e. Email Validator output (`validate_emails`)

Join back on `email`. Keep `email_result` as `email_status_raw`, map to `email_status`, and keep `email_quality`, `sc_mx_provider` and `sc_mx_security_gateway`. Only `email_status = valid` rows go to the main campaign; catch-alls go to their own campaign (`email-deliverability`).

## 2. Normalized column to platform variable

Upload the normalized file with headers already renamed to what the platform expects. That removes manual mapping errors at upload.

| Normalized column | Instantly | Smartlead | Lemlist | EmailBison | ManyReach |
|-|-|-|-|-|-|
| `email` | Email (required) | `email` | `email` | `email` | `email` |
| `first_name` | First Name, merge `{{firstName}}` | `first_name` | `firstName` | `first_name` | `firstName`, merge `{{FIRST_NAME}}` |
| `last_name` | Last Name | `last_name` | `lastName` | `last_name` | `lastName` |
| `company_name` or `business_name` | Company Name, merge `{{companyName}}` | `company_name` | `companyName` | `company` (per scrapercity.com/integrations/emailbison) | `company`, `{{COMPANY}}` |
| `company_domain` or `website` | Website | `website` | custom variable | custom variable | `domain`, `{{DOMAIN}}` |
| `phone` | Phone | `phone_number` | `phone` | custom variable | `phone`, `{{PHONE}}` |
| `linkedin_url` | custom variable `linkedin` | `linkedin_profile` | `linkedinUrl` | custom variable | `personalSocial` |
| `title` | `job_title` on the bulk API; custom variable `title` on CSV | custom field | `jobTitle` | custom variable `title` | `jobPosition`, `{{JOB_POSITION}}` |
| Copy variables (`category`, `rating`, `reviews`, `app_trigger`, `industry_plain`) | Custom variables | Custom fields | Extra fields become variables | Custom variables created first | `custom1` to `custom20`, merge `{{CUSTOM_1}}` |

Platform limits that shape the file:

| Platform | Limit | Source |
|-|-|-|
| Instantly | 50 variables per upload; column names up to 20 characters; first row must be headers; UTF-8 | Instantly help, CSV import |
| Smartlead | 40 custom variables per lead on CSV import; API `custom_fields` up to 200 per lead; up to 400 leads per API request | Smartlead help and API reference |
| EmailBison | Custom variables must exist in the workspace before they can be attached | EmailBison docs |
| ManyReach | `custom1` to `custom20`; `{{CUSTOM_1}}` works, `{{CUSTOM1}}` is rejected; `companySize` up to 32 characters | scrapercity.com/integrations/manyreach |
| Lemlist | 20 requests per 2 seconds per key on the API; custom variable values are text, and characters other than letters, digits, `_`, `-`, space and `#` become `_` | lemlist API reference |

Keep custom variables to 20 or fewer (ManyReach's `custom1` to `custom20` and the scrapercity.com Smartlead page's 20 per lead are the lowest limits above) and column names to 20 characters or fewer (Instantly's limit). That fits every platform above.

## 3. Fallbacks

Fill fallbacks in the file so every platform renders the same.

| Column | Fallback | When no fallback reads naturally |
|-|-|-|
| `first_name` | "there" | Never guess from the email local part |
| `company_short` | "your team" (B2B), "your practice" or "your shop" (local) | |
| `category` | "business" | |
| `rating` | none | Route rows without a rating to a variant without the rating line |
| `reviews` | none | Under 10 reviews: route to the non-count variant |
| `app_trigger` | none | Route to the platform line variant |
| `title_short` | "your role" | |

Check: zero empty cells in any column used in copy, and no `{{` in a rendered preview.

## 4. Import procedure

| Step | Action | Pass when |
|-|-|-|
| 1 | Normalize every file (list quality standard section 3) | Required columns filled |
| 2 | Dedupe inside the file and against the sequencer workspace on lowercased email | 0 duplicates |
| 3 | Suppress: unsubscribes, bounces, complaints, customers, open deals, competitors, anyone contacted inside the user's re-contact gap (Alex Berman waits 30 to 60 days between cycles) | 0 matches |
| 4 | Validate with `validate_emails` ($0.0072 per email) any row last checked before the user's re-check window | 100% of main-file rows `valid` |
| 5 | Split files: main (valid), catch-all, role-address variant, non-personalized variant | Each file maps to one campaign or variant |
| 6 | Rename headers to the platform's names (section 2) | Header row matches the table |
| 7 | Upload with duplicate checks on and every block list honored | Instantly "Check for Duplicates" checked; Smartlead `ignore_global_block_list`, `ignore_unsubscribe_list` and `ignore_community_bounce_list` all false; ManyReach `addOnlyIfNew=true` |
| 8 | Reconcile counts | rows sent = rows imported + reported duplicates + reported blocklisted + reported invalid |
| 9 | Preview rendered emails, including rows that use fallbacks | No raw tags; names and numbers read right |
| 10 | Enroll into a paused campaign, then start | Sends match the ramp row from `inbox-setup` |

### API pushes

| Platform | Call | Batch | Dedupe flags | Read back |
|-|-|-|-|-|
| Instantly | `POST https://api.instantly.ai/api/v2/leads/add` with `campaign_id` (or `list_id`) and a `leads` array; custom fields inside `custom_variables` | Up to 1,000 per call | `skip_if_in_workspace` (overrides the other two), `skip_if_in_campaign`, `skip_if_in_list`; `verify_leads_on_import: false` after `validate_emails` | `leads_uploaded`, `in_blocklist`, `skipped_count`, `invalid_email_count`, `duplicate_email_count`, `remaining_in_plan` |
| Smartlead | `POST https://server.smartlead.ai/api/v1/campaigns/{id}/leads?api_key=...` with `lead_list` and `settings` | Up to 400 per request; send 100 (scrapercity.com integration page) | The four `ignore_*` settings all false | `added_count`, `skipped_count`, `skipped_leads` |
| Lemlist | `POST https://api.lemlist.com/api/campaigns/{campaignId}/leads/?deduplicate=true&verifyEmail=false` | One lead per call | `deduplicate=true` returns 409 for a lead in another campaign; 400 `LEAD_ALREADY_IN_CAMPAIGN` for this one | Count 200s, 409s and 400s per batch |
| EmailBison | `POST {workspace}/api/leads`, then `POST {workspace}/api/campaigns/{id}/leads` with `lead_ids` | One create per lead, attach many | Dedupe locally first | Lead ids returned |
| ManyReach | `POST https://api.manyreach.com/api/v2/prospects/bulk?listId=...&campaignId=...` | 100 per call | `addOnlyIfNew=true`, `notInOtherCampaign=true` | Response counts |

Rate limits that set the push speed (vendor docs, checked 2026-10-13):

| Platform | Limit | Scope | Practical pace |
|-|-|-|-|
| Instantly | 100 requests a second, 6,000 a minute | Per workspace, shared by every key and API v1 | Bulk add makes this a non-issue for imports |
| Smartlead | Standard 60 a minute and 1,000 an hour; Pro 120 a minute and 3,000 an hour | Per API key | 100 leads per call, about 50 calls a minute on Standard |
| Lemlist | 20 requests per 2 seconds | Per API key | 10 a second, one lead each |
| HubSpot private app | 100 (Free, Starter) or 190 (Professional, Enterprise) per 10 seconds | Per app | Batch upserts of 100 |

Store every API key in an environment variable. On 429, wait for `Retry-After` when the response carries it, otherwise back off exponentially (1, 2, 4, 8, 16 seconds) with one retry per batch, and log every response so a partial batch resumes without double-adding.

## 5. Dedupe across ScraperCity pulls

| Source | Tool | Method |
|-|-|-|
| Lead Database and Local Business Database | `excludeDelivered: true` with `page: 1` or the `after` cursor | Returns only records this account does not already have |
| Scrapers (Maps, Store Leads, Apollo) | None built in | Keep a local set of lowercased emails and domains already pushed; check before each push |
| Sequencer | Platform duplicate check | Catches what the local set missed |
| Agency, several clients | One master set of lowercased emails across all clients | Sequencer duplicate checks stop at the workspace or client, so they never see another client's campaigns. A prospect in one client's active sequence is skipped for every other client until the re-contact gap after that sequence ends (Alex Berman waits 30 to 60 days between cycles) |

## 6. Suppression sync

One suppression list per company, pushed to every sequencer and the CRM.

| Event | Source | Push to |
|-|-|-|
| Unsubscribe or "remove me" reply | Sequencer webhook or reply handling | Every sequencer's block list (email), CRM opt-out property |
| Company asks to stop | Reply | Every sequencer's block list (domain) |
| Hard bounce | Sequencer webhook | Every sequencer's block list (email) |
| Customer or open deal | CRM | Block list (domain) before each import |

Timing: the same day, in every tool. Google's 48 hours and Yahoo's 2 days are the outer limits.

## Sources

- ScraperCity tool catalog: `references/scrapercity-catalog.md`
- Alex Berman, TAM strategy breakdown (30 to 60 days between cycles; checked 2026-10-13): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- ScraperCity platform facts: `references/scrapercity-platform.md`
- scrapercity npm package (AGENT_DOCS field lists): https://www.npmjs.com/package/scrapercity
- ScraperCity, Instantly integration: https://scrapercity.com/integrations/instantly
- ScraperCity, Smartlead integration: https://scrapercity.com/integrations/smartlead
- ScraperCity, Lemlist integration: https://scrapercity.com/integrations/lemlist
- ScraperCity, EmailBison integration: https://scrapercity.com/integrations/emailbison
- ScraperCity, ManyReach integration: https://scrapercity.com/integrations/manyreach
- Instantly, How to import leads via CSV: https://help.instantly.ai/en/articles/6254215-how-to-import-leads-via-csv
- Instantly, API v2 leads: https://developer.instantly.ai/api/v2/lead
- Instantly, Add leads in bulk: https://developer.instantly.ai/api-reference/lead/add-leads-in-bulk-to-a-campaign-or-list
- Instantly, Rate limit: https://developer.instantly.ai/getting-started/rate-limit
- Smartlead, Rate limits: https://api.smartlead.ai/guides/rate-limits
- lemlist, Create lead in campaign: https://developer.lemlist.com/api-reference/endpoints/leads/create-lead-in-campaign
- lemlist, Rate limits: https://developer.lemlist.com/api-reference/getting-started/rate-limits
- HubSpot, Legacy private apps (rate limits): https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview
- Smartlead, How to map CSV columns: https://helpcenter.smartlead.ai/en/articles/409-how-to-map-csv-columns-in-smartlead-campaigns
- Smartlead, Add leads to a campaign (API): https://api.smartlead.ai/reference/add-leads-to-a-campaign-by-id
- EmailBison, Custom variables: https://docs.emailbison.com/leads/custom-variables
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
