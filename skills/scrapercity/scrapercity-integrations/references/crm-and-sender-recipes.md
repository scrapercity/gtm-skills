# CRM and Sending Platform Recipes

How to load ScraperCity records into HubSpot, Salesforce, Attio, Pipedrive and GoHighLevel, and into Instantly, Smartlead, Lemlist, EmailBison and ManyReach. Every destination call below was checked in that vendor's own API documentation on 2026-10-13. Run these calls from n8n, Make, Zapier, Pipedream or your own code; the ScraperCity side of each flow is in `references/automation-recipes.md`.

## Before any load

1. Validate first. Send the emails to `validate_emails` ($0.0072 per email) and load only the ones that come back valid. A sender that imports unvalidated addresses pays for it in bounces. See the `email-list-cleaner` skill.
2. Dedupe on a stable key before the load: lowercase email for people, normalized domain for companies, phone plus postal code for local businesses.
3. Run one record end to end before the batch.
4. Keep every destination token in the automation tool's secret store, never in a node name, a sheet cell or a committed file.

## Destination limits at a glance

| Destination | Endpoint used | Auth | Records per call | Rate limit | Source |
|---|---|---|---:|---|---|
| HubSpot | `POST /crm/v3/objects/contacts/batch/upsert` | Private app token, `Authorization: Bearer` | 100 | Private apps: 100 per 10 s on Free and Starter, 190 per 10 s on Professional and Enterprise; 250,000 to 1,000,000 a day by tier | HubSpot developer docs |
| Salesforce | `PATCH /services/data/vXX.X/composite/sobjects/Lead/Email_Key__c` (or `Contact`) | OAuth access token from a connected app, `Authorization: Bearer` | 200 | Daily API requests: 100,000 plus a per-license amount (1,000 per Salesforce license on Enterprise), shared by every integration in the org | Salesforce developer docs |
| Attio | `PUT https://api.attio.com/v2/objects/people/records?matching_attribute=email_addresses` | Access token, `Authorization: Bearer` | 1 | 25 writes a second, 100 reads a second; 429 carries `Retry-After` | Attio API docs |
| Pipedrive | `POST /api/v2/persons` | `x-api-token` header | 1 | Burst per 2 s by plan (API token: Lite 20, Growth 40, Premium 100, Ultimate 120); daily token budget 30,000 x plan multiplier x seats | Pipedrive developer docs |
| GoHighLevel | `POST https://services.leadconnectorhq.com/contacts/upsert` | Private Integration token, `Authorization: Bearer`, `Version` header | 1 | 100 per 10 s burst, 200,000 a day per app per location | HighLevel API docs |
| Instantly | `POST https://api.instantly.ai/api/v2/leads/add` | API key, `Authorization: Bearer` | 1,000 | 100 a second and 6,000 a minute per workspace | Instantly API v2 docs |
| Smartlead | `POST https://server.smartlead.ai/api/v1/campaigns/{campaign_id}/leads` | `api_key` query parameter | 400 | 10 requests per 2 s (plan dependent) | Smartlead API docs |
| Lemlist | `POST https://api.lemlist.com/api/campaigns/{campaignId}/leads/` | Basic auth, empty username, API key as password | 1 | 20 requests per 2 s per key | Lemlist developer docs |
| EmailBison | `POST {your instance}/api/leads`, then attach to a campaign | API token, `Authorization: Bearer` | 1 (JSON) or a CSV of up to 50,000 | Not published | EmailBison docs |
| ManyReach | Bulk prospect add (see the ManyReach section) | API key | see section | Not published as a number in ManyReach help | ManyReach help center |

## HubSpot

**Mechanism.** CRM v3 batch upsert with `idProperty: "email"`. Existing contacts with that email are updated, the rest are created. Batches are capped at 100 records. Partial upserts are not supported when `email` is the id property (HubSpot API reference, batch upsert contacts).

**Where the token goes.** A private app (super admin: Development, Legacy apps, the app, Auth tab, Show token) with `crm.objects.contacts.write`. Send `Authorization: Bearer <token>`.

**Body.**

```json
{
  "inputs": [
    {
      "idProperty": "email",
      "id": "dana.ruiz@example.com",
      "properties": {
        "email": "dana.ruiz@example.com",
        "firstname": "Dana",
        "lastname": "Ruiz",
        "jobtitle": "VP Sales",
        "company": "Example Analytics",
        "website": "example.com",
        "city": "Austin",
        "state": "TX",
        "country": "United States"
      }
    }
  ]
}
```

These are HubSpot's default contact property internal names; confirm any custom ones under Settings, Properties, where each property shows its internal name (HubSpot knowledge base, default contact properties).

**Guardrails.** 100 per batch. A 2,000-record daily load is 20 calls, far under 100 per 10 seconds. The daily API budget is shared by every app in the HubSpot account, so check what else is calling before scheduling a large backfill. Set a custom property such as `lead_source = ScraperCity` and the segment name so sales can filter and so a later cleanup is one view.

## Salesforce

**Mechanism.** sObject Collections upsert: `PATCH /services/data/vXX.X/composite/sobjects/{object}/{externalIdField}` with up to 200 records per request. It matches on an External ID field only, never on record ids, and every record carries an `attributes` map with its `type`. With `allOrNone: false`, each record succeeds or fails on its own (Salesforce REST API, Upsert Records Using sObject Collections).

**One-time setup.** The standard `Email` field cannot be the match key, so add a custom Email field such as `Email_Key__c`, marked External ID and Unique, and fill it with the lowercase address on every load. Cold prospects usually load as Leads, which need `LastName` and `Company`; a Contact sits under an Account, so it suits people at accounts already in the org.

**Where the token goes.** An OAuth access token from a connected app with API access, sent as `Authorization: Bearer <token>`. In n8n, the Salesforce OAuth2 credential holds it; in code, refresh the token rather than storing a long-lived one in a file.

**Body.**

```json
{
  "allOrNone": false,
  "records": [
    {
      "attributes": { "type": "Lead" },
      "Email_Key__c": "dana.ruiz@example.com",
      "Email": "dana.ruiz@example.com",
      "FirstName": "Dana",
      "LastName": "Ruiz",
      "Company": "Example Analytics",
      "Title": "VP Sales",
      "Website": "example.com",
      "LeadSource": "ScraperCity"
    }
  ]
}
```

`LeadSource` is a picklist: add `ScraperCity` as a value first, or write the source into a custom text field. Leave `OwnerId`, `Status` and every opportunity field out of the body so assignment rules and reps keep control of them.

**Guardrails.** Read the per-record results: an active duplicate rule or a validation rule can reject a record while the rest of the batch loads. A 2,000-lead day is 10 requests. The daily allocation is shared by every integration in the org, so check Setup, System Overview ("API Requests, Last 24 Hours") or the `Sforce-Limit-Info` response header before scheduling a large backfill.

## Attio

**Mechanism.** Assert a person record: `PUT https://api.attio.com/v2/objects/people/records?matching_attribute=email_addresses`. It creates the person or updates the one whose email matches; the matching attribute must be unique (Attio API reference, Assert a person record).

**Where the token goes.** An Attio access token with `record_permission:read-write` and `object_configuration:read`, sent as `Authorization: Bearer <token>`.

**Body.**

```json
{
  "data": {
    "values": {
      "email_addresses": ["dana.ruiz@example.com"],
      "name": [{ "first_name": "Dana", "last_name": "Ruiz", "full_name": "Dana Ruiz" }]
    }
  }
}
```

Add title, company and segment as attributes that exist on the People object in that workspace; read their slugs from the object settings before mapping.

**Guardrails.** 25 write requests a second; a 429 carries `Retry-After` (usually the next second) and the request can be retried after it. Pace at 5 a second, so 2,000 people take about 7 minutes.

## Pipedrive

**Mechanism.** API v2 `POST /api/v2/persons`, one person per call, on your company domain (`https://yourcompany.pipedrive.com/api/v2/persons`). Create or find the organization first and pass `org_id` (Pipedrive API reference, Persons).

**Where the token goes.** Personal preferences, API (app.pipedrive.com/settings/api). Send it in the `x-api-token` header (Pipedrive docs, Authentication).

**Body.**

```json
{
  "name": "Dana Ruiz",
  "org_id": 4821,
  "emails": [{ "value": "dana.ruiz@example.com", "primary": true, "label": "work" }],
  "phones": [{ "value": "+15125550142", "primary": true, "label": "work" }],
  "label_ids": [7]
}
```

`job_title`, `postal_address` and `notes` are accepted only when contact sync is enabled; otherwise the request fails with 403. Put the title in a custom field (its key is a 40-character hash) if contact sync is off.

**Guardrails.** Searching for an existing person costs 40 tokens and is limited to 10 requests per 2 seconds on every plan, so dedupe in the automation before loading instead of searching Pipedrive per record. Pace creates at the plan's burst limit or lower; admins get emails at 75% and 100% of the daily budget, and continued traffic after 429s can turn into 403s for `api_token` integrations (Pipedrive docs, Rate limiting).

## GoHighLevel

**Mechanism.** `POST https://services.leadconnectorhq.com/contacts/upsert`. Required body field `locationId`. Matching follows the location's Allow Duplicate Contact setting (email, phone or both, in its priority order). The response says whether the contact was new (HighLevel API docs, Upsert Contact).

**Where the token goes.** A Private Integration token (agency or sub-account settings, Private Integrations, Create new Integration, only the scopes needed: `contacts.write`). Copy it once; it is not shown again. Send `Authorization: Bearer <token>` and the `Version` header shown on the endpoint's page (`v3` on the upsert page when checked; older examples show `2021-07-28`).

**Body.**

```json
{
  "locationId": "ve9EPM428h8vShlRW1KT",
  "firstName": "Marco",
  "lastName": "Diaz",
  "email": "marco@lonestarhvac.example",
  "phone": "+12145550199",
  "companyName": "Lone Star HVAC",
  "website": "lonestarhvac.example",
  "source": "ScraperCity Local Business Database",
  "tags": ["scrapercity", "hvac-tx"]
}
```

`tags` overwrites every tag on an existing contact. For contacts that may already exist with other tags, add tags with the Add Tag endpoint instead.

**Guardrails.** 100 requests per 10 seconds and 200,000 a day per app per location; read `X-RateLimit-Remaining` on each response. One contact per call, so 300 contacts at 5 a second takes a minute. Upserts can trigger GoHighLevel workflows; turn those off or filter on the tag until the test batch looks right.

## Instantly

**Mechanism.** `POST https://api.instantly.ai/api/v2/leads/add` with `campaign_id` (or `list_id`) and a `leads` array of 1 to 1,000. With `campaign_id`, every lead needs `email` (Instantly API v2, Add leads in bulk).

**Where the key goes.** An Instantly API v2 key with a `leads:create` (or broader) scope, sent as `Authorization: Bearer <key>`.

**Body.**

```json
{
  "campaign_id": "0193a3c2-7d4e-7a51-9f0b-3c2e1d4a5b6c",
  "skip_if_in_workspace": true,
  "verify_leads_on_import": false,
  "leads": [
    {
      "email": "dana.ruiz@example.com",
      "first_name": "Dana",
      "last_name": "Ruiz",
      "company_name": "Example Analytics",
      "job_title": "VP Sales",
      "website": "example.com",
      "personalization": "Saw Example Analytics just opened a Denver office.",
      "custom_variables": { "segment": "vp-sales-saas-50-200" }
    }
  ]
}
```

`skip_if_in_workspace` skips any lead already anywhere in the workspace and overrides the other skip flags. Leave `verify_leads_on_import` off when the list already went through `validate_emails`, so you do not pay to verify twice.

**Guardrails.** 100 requests a second and 6,000 a minute, shared by every key in the workspace. Instantly's docs suggest batches of about 100 with a short pause between them for large jobs. A 2,000-lead day is 2 calls at 1,000 or 20 at 100.

## Smartlead

**Mechanism.** `POST https://server.smartlead.ai/api/v1/campaigns/{campaign_id}/leads?api_key=<key>` with `lead_list` (up to 400 leads) and `settings` (Smartlead API docs, Add leads to campaign).

**Where the key goes.** Settings, Activate API. Smartlead takes the key as the `api_key` query parameter and has no Bearer option, so make sure the automation tool does not log full request URLs.

**Body.**

```json
{
  "lead_list": [
    {
      "email": "marco@lonestarhvac.example",
      "first_name": "Marco",
      "last_name": "Diaz",
      "company_name": "Lone Star HVAC",
      "phone_number": "+12145550199",
      "website": "lonestarhvac.example",
      "location": "Dallas, TX",
      "custom_fields": { "rating": "4.7", "reviews": "212", "category": "HVAC contractor" }
    }
  ],
  "settings": {
    "ignore_global_block_list": false,
    "ignore_unsubscribe_list": false,
    "ignore_duplicate_leads_in_other_campaign": false
  }
}
```

Keep the three `ignore_*` settings false so Smartlead's block list, unsubscribes and cross-campaign duplicates are respected. `custom_fields` holds up to 200 keys per lead.

**Guardrails.** 10 requests per 2 seconds; on 429 wait at least 2 seconds. 400 leads per call means a 2,000-lead day is 5 calls.

## Lemlist

**Mechanism.** `POST https://api.lemlist.com/api/campaigns/{campaignId}/leads/`, one lead per call. It never updates: a contact already in the campaign returns 400 `LEAD_ALREADY_IN_CAMPAIGN`. Query parameter `deduplicate=true` refuses the lead (409) if it is in another campaign (Lemlist developer docs, Create lead in campaign).

**Where the key goes.** The Lemlist API key, sent with HTTP Basic auth with an empty username and the key as password (`--user ":KEY"` in curl, or `Authorization: Basic` of `:KEY` base64).

**Body.**

```json
{
  "email": "dana.ruiz@example.com",
  "firstName": "Dana",
  "lastName": "Ruiz",
  "companyName": "Example Analytics",
  "companyDomain": "example.com",
  "jobTitle": "VP Sales",
  "linkedinUrl": "https://www.linkedin.com/in/example-dana-ruiz",
  "icebreaker": "Saw Example Analytics just opened a Denver office.",
  "segment": "vp-sales-saas-50-200"
}
```

Any key that is not a standard field becomes a custom variable (`{{segment}}`). Company fields update the shared company record, not just this lead. Leave `verifyEmail` and `findEmail` false when ScraperCity already found and validated the address.

**Guardrails.** 20 requests per 2 seconds per key, with `Retry-After` on 429. One lead per call, so 2,000 leads take at least 200 seconds; pace at 8 a second.

## EmailBison

**Mechanism.** Create leads, then attach them to a campaign. Base URL is your EmailBison instance (the docs use `https://dedi.emailbison.com`; white-label workspaces use their own domain). `POST /api/leads` creates one lead with required `first_name`, `last_name`, `email` and optional `title`, `company`, `notes`, `custom_variables` (an array of `{ "name", "value" }`; each variable must exist in the workspace first). `POST /api/leads/bulk/csv` uploads a CSV (multipart, up to 50,000 leads per file in the UI) into a new lead list. Attach with `POST /api/campaigns/{campaign_id}/leads/attach-leads` (`lead_ids`) or `/attach-lead-list` (`lead_list_id`). Leads added to an active campaign take up to 5 minutes to sync (EmailBison docs: Adding leads, Adding leads to a campaign).

**Where the key goes.** Settings, Developer API, New API Token, type api-user (scoped to the workspace it was created in). Send `Authorization: Bearer <token>`.

**Body (single lead).**

```json
{
  "first_name": "Dana",
  "last_name": "Ruiz",
  "email": "dana.ruiz@example.com",
  "title": "VP Sales",
  "company": "Example Analytics",
  "custom_variables": [{ "name": "segment", "value": "vp-sales-saas-50-200" }]
}
```

**Guardrails.** No rate limit is published; pace single-lead creates at 2 a second and prefer the CSV upload for anything over a few hundred. Leads already in sequence in another campaign are skipped by default when imported to a campaign (EmailBison docs, Clay import enrichment), which is the behavior you want for cold lists.

## ManyReach

**Mechanism.** Bulk prospect add into a ManyReach list, optionally enrolled in a campaign. ManyReach's help center documents `POST https://app.manyreach.com/api/prospects/crm/add/bulk?apikey=<key>` with the prospects in a JSON body, `GET https://app.manyreach.com/api/lists?apikey=<key>` to find list ids, and a Swagger reference at `app.manyreach.com/swagger/docs` (ManyReach help: How to connect n8n to ManyReach). ScraperCity's ManyReach guide describes a newer bulk endpoint, `POST https://api.manyreach.com/api/v2/prospects/bulk?listId=...` with an `X-API-Key` header, up to 100 prospects per call, fields `email`, `firstName`, `lastName`, `company`, `website`, `jobPosition`, `phone`, `city`, `state`, `country`, `custom1` to `custom20`, and 60 calls a minute per key (per scrapercity.com/integrations/manyreach). Open the Swagger page in your account and use whichever version it lists.

**Where the key goes.** ManyReach Settings, API (`app.manyreach.com/e/account/api`). Reset it there if exposed.

**Body (v2 form, per the ScraperCity guide).**

```json
{
  "prospects": [
    {
      "email": "marco@lonestarhvac.example",
      "firstName": "Marco",
      "lastName": "Diaz",
      "company": "Lone Star HVAC",
      "website": "lonestarhvac.example",
      "phone": "+12145550199",
      "city": "Dallas",
      "state": "TX",
      "country": "US",
      "custom1": "4.7 stars, 212 reviews"
    }
  ]
}
```

**Guardrails.** ManyReach's own help says the API is rate limited without a number and recommends delays between requests; the ScraperCity guide gives 60 calls a minute. Pace at 1 call a second with 100 prospects per call and back off on 429.

## Sources

- https://developers.hubspot.com/docs/api-reference/crm-contacts-v3/batch/post-crm-v3-objects-contacts-batch-upsert
- https://developers.hubspot.com/docs/developer-tooling/platform/usage-guidelines
- https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview
- https://knowledge.hubspot.com/properties/hubspots-default-contact-properties
- https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_composite_sobjects_collections_upsert.htm
- https://developer.salesforce.com/docs/platform/salesforce-app-limits-cheatsheet/guide/salesforce-app-limits-platform-api.html
- https://docs.attio.com/api-reference/people/assert-a-person-record
- https://docs.attio.com/rest-api/guides/rate-limiting
- https://pipedrive.readme.io/docs/core-api-concepts-authentication
- https://pipedrive.readme.io/docs/core-api-concepts-rate-limiting
- https://pipedrive.readme.io/docs/how-to-find-the-api-token
- https://developers.pipedrive.com/docs/api/v1/Persons#addPerson
- https://marketplace.gohighlevel.com/docs/ghl/contacts/upsert-contact
- https://marketplace.gohighlevel.com/docs/other/rate-limits
- https://help.gohighlevel.com/support/solutions/articles/155000003054-private-integrations-everything-you-need-to-know
- https://developer.instantly.ai/api-reference/lead/add-leads-in-bulk-to-a-campaign-or-list
- https://developer.instantly.ai/getting-started/rate-limit
- https://api.smartlead.ai/api-reference/leads/add-to-campaign
- https://helpcenter.smartlead.ai/en/articles/125-full-api-documentation
- https://developer.lemlist.com/api-reference/endpoints/leads/create-lead-in-campaign
- https://docs.emailbison.com/get-started/authentication
- https://docs.emailbison.com/leads/creating-a-lead
- https://docs.emailbison.com/campaigns/adding-leads-to-a-campaign
- https://docs.emailbison.com/low-code-tools/clay/enrichments/import-leads-to-campaign
- https://help.manyreach.com/en/articles/60-how-to-connect-n8n-to-manyreach-using-api-integration
- https://scrapercity.com/integrations/manyreach
- https://scrapercity.com/integrations
