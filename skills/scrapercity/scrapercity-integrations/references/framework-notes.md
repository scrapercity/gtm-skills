# Framework Notes: ScraperCity Integrations

Which sources shape this skill, what each contributes, and which file to open for each job.

## Routing table

| You need | Open |
|---|---|
| Clay, n8n, Zapier, Make, Pipedream, Google Sheets or Airtable setup | `references/automation-recipes.md` |
| HubSpot, Pipedrive, GoHighLevel, Instantly, Smartlead, Lemlist, EmailBison or ManyReach setup | `references/crm-and-sender-recipes.md` |
| Which ScraperCity field goes to which destination field, and the transforms | `references/field-mapping.md` |
| A vendor's rate limit or batch size | the "Destination limits at a glance" table in `references/crm-and-sender-recipes.md`, and each recipe's Guardrails table |
| A ScraperCity endpoint, body or error code | the `scrapercity-api` skill, `references/endpoint-reference.md` there |
| Tool prices | `references/scrapercity-catalog.md` (shared) |
| Plans, database allowances | `references/scrapercity-platform.md` (shared) |
| Wallet checks, polling schedule, webhook handling, key rules | `references/scrapercity-agent-patterns.md` (shared) |
| Email validation before a sender load | the `email-list-cleaner` skill |
| Sender choice and setup | the `sending-platforms` skill |

## Sources and contributions

### ScraperCity (primary for the ScraperCity side)

- `scrapercity` npm package 1.0.17: endpoints, Bearer auth, the database switch to POST past 6,000 characters, database fields, webhook payload `runId`, `fileName`, `leadsCount`, duplicate windows (429 within 30 s, 409 within about 2 min).
- scrapercity.com/api-docs: 100 requests a minute per key, 10 concurrent scrapes, 48-hour result storage, midnight UTC allowance reset.
- scrapercity.com/how-to-use: webhook page and trigger on `SUCCEEDED` or `FAILED`.
- scrapercity.com/integrations and its per-tool pages: which integrations ScraperCity supports, the Lead Database person keys in the n8n guide, validator CSV columns, and the ManyReach v2 bulk details. Where a guide's path or rate setting conflicts with the package or the API docs (for example scraper paths shown as GET, or Clay at 10 requests a second), this skill follows the package and the API docs and says so.

### Automation platforms

| Vendor doc | Contribution |
|---|---|
| Clay University: HTTP API integration overview; webhook integration guide | HTTP API column settings, header accounts stored encrypted per workspace, request limit and duration, conditional runs, webhook source and its 50,000-submission cap |
| n8n docs: HTTP Request node, pagination cookbook, common issues, Webhook node, Extract From File | Header Auth credential, pagination with `$pageCount` and `$response`, Batching and Retry On Fail, test vs production webhook URLs, Respond Immediately, CSV extraction from binary |
| Zapier help: Send webhooks, Trigger Zaps from webhooks, Webhooks by Zapier rate limits, JavaScript code, Schedule by Zapier | Custom Request for Bearer headers, Catch Hook, Professional plan requirement, 20,000 requests per 5 minutes per user, Code steps with `fetch` returning arrays, hourly schedule |
| Make apps and help: HTTP, CSV, Webhooks, scheduling | Make a request with keychain credentials and Parse response, 1 to 300 s timeout, Custom webhook queue, 300 requests per 10 s, 410 after 5 idle days, Parse CSV, At regular intervals scheduling |
| Pipedream docs: Triggers, Environment variables, Limits | HTTP trigger URL and `$.respond`, secret environment variables, 30 s and 60 s default timeouts, 300 s and 750 s maximums, 10 requests a second on HTTP triggers, 512KB bodies |
| Google Apps Script: UrlFetchApp, quotas, Properties | Fetch with headers and JSON payloads, 2KB URL cap, 6-minute executions, daily fetch and trigger quotas, Script properties for the key |
| Airtable Web API and support | Create and upsert records, 10 per request, 5 requests a second per base, 30-second wait after 429, monthly call caps by plan |

### CRMs and senders

| Vendor doc | Contribution |
|---|---|
| HubSpot developer docs | Batch upsert by email, 100 per batch, private app tokens as Bearer, burst and daily limits by tier |
| Pipedrive developer docs | `x-api-token` header, API v2 persons body, contact-sync 403 on some fields, token-based daily budget and burst limits, 40-token search cost |
| HighLevel API docs and help center | Contacts upsert body and dedupe behavior, Private Integration tokens, `Version` header, 100 per 10 s and 200,000 a day |
| Instantly API v2 docs | Bulk add of up to 1,000 leads, skip flags, scopes, 100 a second and 6,000 a minute per workspace |
| Smartlead API docs and help center | Add up to 400 leads per call, `api_key` query auth, `settings` flags, 10 requests per 2 s |
| Lemlist developer docs | Create lead in campaign, Basic auth, deduplicate and verify flags, custom variables, 20 requests per 2 s |
| EmailBison docs | Instance base URL, api-user tokens, single and CSV lead creation, attach endpoints, 5-minute sync |
| ManyReach help center | Bulk prospect endpoint, list lookup, Swagger location, key location; no published numeric rate limit |

### Standards

- IETF RFC 6750: bearer tokens in the `Authorization` header, not the URL.
- ITU-T E.164: the international phone number format used for every phone transform.
- OWASP Secrets Management Cheat Sheet: one secret per service, stored in a secret manager, never in code or shared documents.

## How the sources combine

1. ScraperCity's package and API docs decide the request, the limits and the async pattern.
2. Each platform's docs decide where the key lives and how loops, schedules and webhooks are built.
3. Each destination's docs decide the body, batch size and pacing.
4. The field mapping joins the two sides, and validation sits between the pull and any sender.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://scrapercity.com/integrations
- https://university.clay.com/docs/http-api-integration-overview
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- https://help.zapier.com/hc/en-us/articles/8496326446989-Send-webhooks-in-Zaps
- https://apps.make.com/http
- https://pipedream.com/docs/workflows/limits
- https://developers.google.com/apps-script/guides/services/quotas
- https://airtable.com/developers/web/api/rate-limits
- https://developers.hubspot.com/docs/developer-tooling/platform/usage-guidelines
- https://pipedrive.readme.io/docs/core-api-concepts-rate-limiting
- https://marketplace.gohighlevel.com/docs/other/rate-limits
- https://developer.instantly.ai/getting-started/rate-limit
- https://helpcenter.smartlead.ai/en/articles/125-full-api-documentation
- https://developer.lemlist.com/api-reference/endpoints/leads/create-lead-in-campaign
- https://docs.emailbison.com/get-started/authentication
- https://help.manyreach.com/en/articles/60-how-to-connect-n8n-to-manyreach-using-api-integration
- https://www.rfc-editor.org/rfc/rfc6750
- https://www.itu.int/rec/T-REC-E.164
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
