# Field Mapping: ScraperCity to Destinations

Source field names, destination field names and the transforms between them. Destination names come from each vendor's API docs (see `references/crm-and-sender-recipes.md` and `references/automation-recipes.md`). Before you build a mapping, run one `limit=1` database call or a 3-row test run and map from the keys you see; the lists below are where to start, not a promise that every record carries every field.

## Source fields

### Local Business Database

Documented in the `scrapercity` npm package (`AGENT_DOCS.txt`):

| Field | Holds | Note |
|---|---|---|
| `title` | Business name | This is the company name, not a job title |
| `category_name` | Google Maps style category | Good merge field for the opener |
| `address`, `city`, `state`, `postal_code`, `country_code` | Location | `country_code` is two letters |
| `phone` | Main business phone | Normalize to E.164 before loading |
| `website` | Website URL | Normalize to a bare domain for dedupe |
| `emails` | Business email addresses | Can hold more than one. Pick one per record |
| `total_score` | Rating, 1 to 5 | |
| `reviews_count` | Review count | |
| `lat`, `lng` | Coordinates | |
| `contact_first_name`, `contact_last_name`, `contact_job_title`, `contact_email`, `contact_mobile` | Named contact, when there is one | Filter with `hasContact=true` when the destination needs a person's name |

### Lead Database

Company fields documented in the package: `company_industry`, `company_size`, `employees_count`, `company_website`, `company_annual_revenue`, `company_city`, `company_state`, `company_country`, `keywords`.

Person keys shown in ScraperCity's n8n integration guide (scrapercity.com/integrations/n8n): `first_name`, `last_name`, `full_name`, `email`, `personal_email`, `mobile_number`, `title`, `headline`, `seniority`, `department`, `company_name`, `company_domain`, `company_linkedin`, `linkedin_url`, `city`, `state`, `country`. ScraperCity's other guides show the phone under different keys (`phone_number`, `phone`), so read the key from your own `limit=1` response before mapping phones.

### Scraper CSVs

Columns depend on the tool. Run a small capped test (for example `maxCrawledPlacesPerSearch: 10` on `scrape_maps`, 10 x $0.0099 = $0.10) and map from the header row. For `validate_emails`, ScraperCity's integrations page lists `email`, `status`, `quality`, `is_catch_all` and `mx_found`; filter on `status` before loading anything into a sender.

## Transforms

| Transform | Rule |
|---|---|
| Pick one email | Local business: `contact_email` if present, else the first entry of `emails`. People: `email`; never load `personal_email` into a cold campaign |
| Lowercase and trim emails | Always, before dedupe and before load |
| Validate | Only rows whose validator `status` is valid go to a sender |
| Domain from website | Strip scheme, `www.` and path: `https://www.lonestarhvac.example/contact` becomes `lonestarhvac.example` |
| Phone to E.164 | `(214) 555-0199` with country US becomes `+12145550199`. Pipedrive, HubSpot and GoHighLevel all store what you send, so normalize first |
| Full name | Pipedrive needs `name`: join first and last. With no named contact, use the business `title` only in a CRM, never as a sender first name |
| Missing first name in a sender | Filter `hasContact=true`, or leave `first_name` empty and write copy that does not use it. EmailBison requires `first_name` and `last_name`, so send only named contacts there |
| Rating and reviews | `total_score` and `reviews_count` into custom fields, as text in senders (`"4.7"`, `"212"`) |
| Segment tag | A constant per flow (`hvac-tx-4star`) in a tag or custom field, so every record can be traced to its pull |
| Source tag | `ScraperCity` plus the database or tool name, in HubSpot `lead_source` style properties or GoHighLevel `source` |

## People (Lead Database) to each destination

| ScraperCity | HubSpot | Pipedrive | GoHighLevel | Instantly | Smartlead | Lemlist | EmailBison | ManyReach | Airtable |
|---|---|---|---|---|---|---|---|---|---|
| `email` | `email` (also the upsert `id`) | `emails[0].value` | `email` | `email` | `email` | `email` | `email` | `email` | Email |
| `first_name` | `firstname` | part of `name` | `firstName` | `first_name` | `first_name` | `firstName` | `first_name` | `firstName` | First name |
| `last_name` | `lastname` | part of `name` | `lastName` | `last_name` | `last_name` | `lastName` | `last_name` | `lastName` | Last name |
| `title` | `jobtitle` | custom field (or `job_title` with contact sync) | custom field | `job_title` | `custom_fields.title` | `jobTitle` | `title` | `jobPosition` | Title |
| `company_name` | `company` | organization `name`, then `org_id` | `companyName` | `company_name` | `company_name` | `companyName` | `company` | `company` | Company |
| `company_domain` | `website` | organization field | `website` | `website` | `website` | `companyDomain` | custom variable | `website` | Domain |
| `linkedin_url` | custom property | custom field | custom field | `custom_variables.linkedin` | `linkedin_profile` | `linkedinUrl` | custom variable | custom slot | LinkedIn |
| phone key from your sample | `phone` | `phones[0].value` | `phone` | `phone` | `phone_number` | `phone` | custom variable | `phone` | Phone |
| `city`, `state`, `country` | `city`, `state`, `country` | custom fields | custom fields | `custom_variables` | `location` (joined) | custom variables | custom variables | `city`, `state`, `country` | City, State, Country |
| segment constant | custom property | `label_ids` | `tags` | `custom_variables.segment` | `custom_fields.segment` | `segment` (custom variable) | custom variable | custom slot | Segment |

## Local businesses (Local Business Database) to each destination

| ScraperCity | HubSpot | Pipedrive | GoHighLevel | Instantly | Smartlead | Lemlist | EmailBison | ManyReach | Airtable |
|---|---|---|---|---|---|---|---|---|---|
| chosen email | `email` | `emails[0].value` | `email` | `email` | `email` | `email` | `email` | `email` | Email |
| `contact_first_name` | `firstname` | part of `name` | `firstName` | `first_name` | `first_name` | `firstName` | `first_name` | `firstName` | First name |
| `contact_last_name` | `lastname` | part of `name` | `lastName` | `last_name` | `last_name` | `lastName` | `last_name` | `lastName` | Last name |
| `title` (business name) | `company` | organization `name` | `companyName` | `company_name` | `company_name` | `companyName` | `company` | `company` | Business |
| `website` as domain | `website` | organization field | `website` | `website` | `website` | `companyDomain` | custom variable | `website` | Website |
| `phone` as E.164 | `phone` | `phones[0].value` | `phone` | `phone` | `phone_number` | `phone` | custom variable | `phone` | Phone |
| `category_name` | custom property | custom field | custom field | `custom_variables.category` | `custom_fields.category` | `category` | custom variable | custom slot | Category |
| `total_score`, `reviews_count` | custom properties | custom fields | custom fields | `custom_variables` | `custom_fields` | custom variables | custom variables | custom slots | Rating, Reviews |
| `city`, `state`, `postal_code` | `city`, `state`, `zip` | custom fields | custom fields | `custom_variables` | `location` (joined) | custom variables | custom variables | `city`, `state` | City, State, ZIP |

## Mapping QA

| Check | Pass |
|---|---|
| Every row has a lowercase, validated email before a sender load | 100% |
| No `personal_email` in a cold campaign | 0 rows |
| First name present wherever the copy uses it | 100% of rows in that campaign |
| Phones in E.164 | 100% of loaded phones |
| Each record carries a segment and source tag | 100% |
| 20 records spot-checked in the destination UI | Fields land in the intended columns |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/integrations
- https://scrapercity.com/integrations/n8n
- https://knowledge.hubspot.com/properties/hubspots-default-contact-properties
- https://developers.pipedrive.com/docs/api/v1/Persons#addPerson
- https://marketplace.gohighlevel.com/docs/ghl/contacts/upsert-contact
- https://developer.instantly.ai/api-reference/lead/add-leads-in-bulk-to-a-campaign-or-list
- https://api.smartlead.ai/api-reference/leads/add-to-campaign
- https://developer.lemlist.com/api-reference/endpoints/leads/create-lead-in-campaign
- https://docs.emailbison.com/leads/creating-a-lead
- https://scrapercity.com/integrations/manyreach
- https://airtable.com/developers/web/api/create-records
- https://www.itu.int/rec/T-REC-E.164
