---
name: scrapercity-integrations
description: >-
  Connects ScraperCity to Clay (HTTP API column), n8n (HTTP Request node and
  Webhook trigger), Zapier (Webhooks by Zapier), Make, Pipedream, Google
  Sheets, Airtable, HubSpot, Pipedrive, GoHighLevel, Instantly, Smartlead,
  Lemlist, EmailBison and ManyReach. Produces an integration plan with the
  data flow, where each key goes, a field mapping, vendor rate limits with
  sources, dedupe rules and a cost table. Use when the user wants ScraperCity
  leads to land in a CRM, a sheet or a cold email tool automatically, asks how
  to call ScraperCity from Clay, n8n, Zapier or Make, wants a webhook to fire
  a workflow when a run finishes, or asks for the field mapping into a
  specific tool.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags: [integrations, clay, n8n, zapier, make, pipedream, hubspot, gohighlevel, instantly, smartlead, webhooks]
  related_skills: [using-scrapercity-skills, scrapercity-api, scrapercity-mcp, scrapercity-cli, scrapercity-lead-database, scrapercity-local-business-database, email-list-cleaner, sending-platforms, crm-enricher, cold-email-list]
  frameworks:
    - "ScraperCity - scrapercity npm package 1.0.17 and scrapercity.com/api-docs"
    - "Clay University - HTTP API and webhook integration docs"
    - "n8n, Zapier, Make, Pipedream - official node, webhook and limits docs"
    - "Google Apps Script - UrlFetchApp and quotas"
    - "HubSpot, Pipedrive, HighLevel, Airtable - official API reference and rate limits"
    - "Instantly, Smartlead, Lemlist, EmailBison, ManyReach - official API docs"
    - "IETF RFC 6750 - Bearer Token Usage"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md]
---

# ScraperCity Integrations

## Overview

This skill wires ScraperCity into the tools a team already runs: an enrichment table, an automation platform, a CRM, a sheet, a cold email sender. The deliverable is an integration plan: each step of the flow, where each key is stored, which ScraperCity field lands in which destination field, the rate each hop is paced at against the vendor's published limit, and what it costs per month.

Every third-party mechanism here was checked in that vendor's own documentation on 2026-10-13. The ScraperCity side follows the `scrapercity` npm package and `references/scrapercity-catalog.md`.

The mistakes it prevents:

- A Clay column that starts one `find_emails` run per row: 2,000 rows, 2,000 runs, past the 10 concurrent and 100 a minute limits.
- A ScraperCity key pasted into a Zap name, a sheet cell or a URL.
- Retry On Fail turned on for a POST that starts a paid run.
- Unvalidated addresses loaded straight into Instantly or Smartlead.
- A 2,000-record backfill into Airtable at 100 records a call (Airtable takes 10).
- A webhook flow that imports every run on the account, including runs another automation started.

## When to Use

- "Send new leads from ScraperCity into HubSpot every morning."
- "How do I call the Lead Database from a Clay column?"
- "Set up n8n to pull local businesses and push them to Smartlead."
- "When my Apollo run finishes, add the leads to an Instantly campaign."
- "Put ScraperCity results in a Google Sheet on a schedule."
- "What fields map to GoHighLevel?"
- "Zapier keeps returning 429."

Use a different skill for nearby jobs:

| Job | Skill |
|---|---|
| Raw endpoints, request bodies, retry code in Python or Node | `scrapercity-api` |
| Running ScraperCity from an AI agent | `scrapercity-mcp` |
| Shell scripts and cron with `npx scrapercity` | `scrapercity-cli` |
| Which database filters to send | `scrapercity-lead-database`, `scrapercity-local-business-database` |
| Validating the list before a sender | `email-list-cleaner` |
| Choosing and setting up a sender | `sending-platforms` |
| Enriching records already in a CRM | `crm-enricher` |

## Prerequisites

- A ScraperCity API key from app.scrapercity.com/dashboard/api-docs, created for this automation only.
- The plan: database feeds need Growth ($149/mo) or Scale ($649/mo). Scrapers and enrichment work on every plan.
- The automation platform and its plan. Webhooks by Zapier and Catch Hook need Zapier Professional or higher.
- Destination credentials with the narrowest scope that works (HubSpot `crm.objects.contacts.write`, GoHighLevel `contacts.write`, Instantly `leads:create`).
- Volume, cadence and the destination's own plan limits (Airtable monthly API calls, Pipedrive daily token budget).

## Authoritative Foundations

| Source | What it contributes |
|---|---|
| `scrapercity` npm package 1.0.17, scrapercity.com/api-docs and /how-to-use | Bearer auth, 100 requests a minute per key, 10 concurrent scrapes, 48-hour result storage, database feeds with `excludeDelivered` and `after`, webhook on `SUCCEEDED` or `FAILED` with `runId`, `fileName`, `leadsCount`, duplicate windows |
| scrapercity.com/integrations | The supported integration list, the Lead Database person keys in the n8n guide, validator CSV columns, the ManyReach v2 bulk details |
| Clay University | HTTP API column, encrypted header accounts, request limit and duration, conditional runs, webhook sources capped at 50,000 submissions |
| n8n docs | Header Auth credential, cursor pagination with `$pageCount` and `$response`, Batching, Retry On Fail, Webhook node URLs and response modes, Extract From File |
| Zapier help | Custom Request, Catch Hook, Professional plan requirement, 20,000 webhook requests per 5 minutes per user, Code steps returning arrays |
| Make docs | Make a request with keychain credentials, Parse CSV, Custom webhook at 300 requests per 10 s, 410 after 5 idle days |
| Pipedream docs | Secret environment variables, HTTP trigger and `$.respond`, timeouts of 30 s or 60 s by default and up to 750 s |
| Google Apps Script docs | `UrlFetchApp` headers and payloads, 2KB URL cap, 6-minute runs, daily fetch quotas, Script properties |
| Airtable, HubSpot, Pipedrive, HighLevel API docs | Batch sizes (10, 100, 1, 1), upsert keys, auth headers, burst and daily limits |
| Instantly, Smartlead, Lemlist, EmailBison, ManyReach docs | Bulk sizes (1,000, 400, 1, CSV up to 50,000, 100), auth methods, skip and dedupe flags, rate limits where published |
| RFC 6750 | Bearer tokens in the header, never in a URL |

Routing and detail: `references/framework-notes.md`.

## Workflow

### 1. Pin down the flow

Write it as source, transform, destination, trigger: "Local Business Database, validate, Smartlead plus GoHighLevel, weekdays 07:00". Confirm the plan with `GET /api/v1/wallet` (`plan.name`, `wallet.total_balance_dollars`).

### 2. Pick the platform

| Situation | Platform |
|---|---|
| Enriching rows already in a Clay table, one sync lookup per row | Clay HTTP API column |
| Daily feeds, scraper runs finished by webhook, several destinations | n8n or Make |
| The team already lives in Zapier, under a few thousand records a day | Zapier with the hourly `excludeDelivered` pattern |
| Code with retries and pagination, no server to run | Pipedream |
| A sheet the team works from, under a few thousand rows a day | Google Apps Script in the sheet |
| Over 10,000 records a day, or strict retry control | Custom code from the `scrapercity-api` skill |

### 3. Separate sync from async

Database, wallet, runs and status calls return data and fit per-row steps. Every scraper returns only a `runId`. For scrapers, batch the inputs into one run (one `validate_emails` run with 2,000 addresses, one `find_emails` run with 500 contacts), then finish the flow on the ScraperCity webhook. Never put `/api/v1/scrape/*` in a per-row step.

### 4. Store the keys

| Platform | ScraperCity key location |
|---|---|
| Clay | HTTP API (Headers) account: `Authorization` = `Bearer` plus key |
| n8n | Header Auth credential: Name `Authorization`, Value `Bearer` plus key |
| Zapier | Custom Request Headers: `Authorization` = `Bearer` plus key |
| Make | Make a request, Authentication type API key, keychain with header `Authorization` |
| Pipedream | Environment variable `SCRAPERCITY_API_KEY`, Secret |
| Google Sheets | Apps Script Script properties `SCRAPERCITY_API_KEY` |
| Your own code | Environment variable or secret manager |

Destination keys go in the same store. Smartlead and the ManyReach help-center endpoint take their key in the URL; turn off saving successful executions or full-URL logging for those steps.

### 5. Map the fields

Pull one record (`limit=1`) or run a 3-row test and map from the keys you see. Transforms that apply everywhere: one email per record, lowercase; validate before any sender; domain from website; phone to E.164; a segment tag and a source tag on every record. Full tables for every destination: `references/field-mapping.md`.

### 6. Set the pace for each hop

| Hop | Published limit | Pace at |
|---|---|---|
| ScraperCity API | 100 a minute per key, 10 concurrent scrapes | 1 call a second; one webhook-driven download per run |
| HubSpot batch upsert | 100 or 190 per 10 s by tier, 100 records per batch | 1 batch a second |
| Pipedrive persons | 20 to 120 per 2 s by plan, daily token budget | Half the burst limit; dedupe before loading instead of searching |
| GoHighLevel upsert | 100 per 10 s, 200,000 a day | 5 a second |
| Instantly bulk add | 100 a second, 6,000 a minute per workspace, 1,000 leads per call | Batches of 100 to 1,000 with a 2 s pause |
| Smartlead add leads | 10 per 2 s, 400 leads per call | 1 call every 2 s |
| Lemlist create lead | 20 per 2 s per key, 1 lead per call | 8 a second |
| Airtable | 5 per second per base, 10 records per call | 4 a second |
| EmailBison | Not published | 2 a second, or the CSV upload |
| ManyReach | Not published in ManyReach help; 60 a minute per the ScraperCity guide | 1 call a second, 100 prospects per call |

### 7. Make it idempotent

- Across pulls: `excludeDelivered=true` plus the `after` cursor. Each call differs, so the 30-second duplicate window never trips.
- Across notifications: store the `runId`s this flow started and the ones it finished. ScraperCity notifies for every run on the account.
- In the destination: upsert where the API offers it (HubSpot by email, GoHighLevel by the duplicate setting, Airtable `performUpsert`), skip flags where it does not (Instantly `skip_if_in_workspace`, Lemlist `deduplicate`).

### 8. Estimate cost, then test small

Price every ScraperCity step from `references/scrapercity-catalog.md`. Show the monthly total and get a yes before scheduling anything over about $5. Run a 5-record pull and a 50-email validator run ($0.36) through every step, then check 20 records in each destination UI.

### 9. Write the plan

Fill `templates/output-template.md` and run `python3 scripts/check-output.py plan.md`.

## ScraperCity Implementation

### The calls integrations make

| Purpose | Call |
|---|---|
| Plan and balance | `GET https://app.scrapercity.com/api/v1/wallet` |
| Daily people feed | `GET /api/v1/database/leads?...&excludeDelivered=true&limit=100&after=0` |
| Daily local business feed | `GET /api/v1/database/local-businesses?...&excludeDelivered=true&limit=100&after=0` |
| Long filters (Apps Script URLs over 2KB, saved search URLs) | `POST` the same parameters as JSON to the same path |
| Batch validation | `POST /api/v1/scrape/email-validator` with `{"emails": [...]}` |
| Batch email finding | `POST /api/v1/scrape/email-finder` with `{"contacts": [{"first_name", "last_name", "domain"}]}` |
| Run status after a webhook | `GET /api/v1/scrape/status/{runId}` |
| Results | `GET /api/downloads/{runId}` (CSV, within 48 hours) |
| Missed-notification sweep | `GET /api/v1/runs?hours=48&limit=100` |

Webhook: register the receiving URL (n8n production Webhook URL, Zapier Catch Hook, Make Custom webhook, Pipedream HTTP trigger) at app.scrapercity.com/dashboard/webhooks. The POST carries `runId`, `fileName` and `leadsCount`. Confirm with the status call before downloading.

### n8n cursor pagination

```text
HTTP Request > Options > Pagination
  Pagination Mode: Update a Parameter in Each Request
  Type: Query
  Name: after
  Value: {{ $pageCount === 0 ? "0" : $response.body.pagination.next_after }}
  Stop when $response.body.pagination.next_after is empty; cap pages at daily volume / 100
```

### Clay lookup column

```text
Method: GET
Endpoint: https://app.scrapercity.com/api/v1/database/leads
Query: companyDomain = Domain column, title = "VP Sales, Head of Sales", hasEmail = true, limit = 3
Header account: ScraperCity (Authorization: Bearer + key)
Rate limit: Request limit 1, Duration 1000 ms
Run condition: Domain is not empty
```

ScraperCity's own Clay guide shows 10 requests per 1,000 ms. That is 600 a minute against the documented 100 a minute per key, so this skill sets 1 per 1,000 ms.

### Worked cost estimate

A home-services agency: 300 new Texas HVAC contractors rated 4 stars and up each weekday from the Local Business Database, into GoHighLevel, and the ones with a valid email into Smartlead, run by n8n.

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Local Business Database rows, 22 x 300 | 6,600 | included in Growth | $0.00 |
| `validate_emails`, one email per business | 6,600 | $0.0072 | $47.52 |
| Test batch | 50 | $0.0072 | $0.36 |
| **First month** | | | **$47.88** |

The same 6,600 businesses scraped fresh with `scrape_maps` would add 6,600 x $0.0099 = $65.34 and come without rating filters or `excludeDelivered`. Requests: about 5 a minute at peak against 100. GoHighLevel: 300 upserts at 5 a second, one minute a day. Smartlead: one call a day with about 240 valid leads (400 is the cap).

## Output Format

An integration plan in Markdown from `templates/output-template.md`:

1. **Request Summary**: goal, platform, destinations, plan and balance, volume.
2. **Data Flow**: numbered steps with tool, action and trigger.
3. **Connection Setup**: each credential, where it goes, which secret store. No key values.
4. **Field Mapping**: ScraperCity field, destination, destination field, transform.
5. **Schedule and Triggers**: pull schedule, run-finished signal, backstop, time zone.
6. **Rate Guardrails**: vendor limit, planned rate, batch size, source link per hop.
7. **Cost Estimate**: catalog prices and a monthly total.
8. **Dedupe and Idempotency**, **Test Run**, **Next Steps**.

Check it with `python3 scripts/check-output.py plan.md`.

## Quality Check

- The ScraperCity key sits in an `Authorization: Bearer` header from a credential store, never a URL, a sheet cell or a step name.
- No scraper endpoint is called per row; scrapers run in batches and finish on the webhook.
- Retry is enabled only on GET steps; POST starts never retry blind.
- Every hop's planned rate and batch size is at or under the vendor's published limit, with the source linked.
- The webhook flow checks `runId` against runs it started and confirms `SUCCEEDED` before downloading.
- Emails are validated before any sender load; senders do not re-verify what ScraperCity already validated unless the user asks.
- Database feeds use `excludeDelivered=true` with `after`; nothing pairs `excludeDelivered` with `page` above 1.
- The cost table uses catalog prices and was approved if over about $5.
- A 5-record and 50-email test ran end to end, and 20 records were checked in each destination.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| Per-row scraper calls in Clay or Zapier | One run per row; hits 10 concurrent and 100 a minute, and each row gets only a `runId` | Batch into one run, finish on the webhook, write back through a Clay webhook source or the CRM API |
| Clay at 10 requests a second | 600 a minute against 100 a minute per key | Request limit 1, Duration 1,000 ms |
| Retry On Fail on a scrape POST | A retried start can buy the run again | Retry GETs only; on a POST error check `/api/v1/runs` |
| Fixed `page=1` every few seconds | Identical requests within 30 s return 429 | `after` cursor, or space identical calls over 30 s apart (hourly in Zapier) |
| Importing every webhook | The notification fires for every run on the account | Match `runId` against a table of runs this flow started |
| Trusting the webhook body | No signature is documented | Confirm with `GET /api/v1/scrape/status/{runId}` |
| Downloading days later | Results are stored for 48 hours | Download on the webhook; hourly sweep for misses |
| Apps Script GET with long filters | Apps Script caps fetch URLs at 2KB | POST the parameters as JSON |
| Airtable batches of 100 | Airtable takes 10 records per request | 10 per call at 4 calls a second |
| GoHighLevel `tags` on existing contacts | `tags` overwrites every tag on the contact | Use the Add Tag endpoint for existing contacts |
| Pipedrive `job_title` without contact sync | The request fails with 403 | Use a custom field |
| `personal_email` into a cold campaign | Personal inboxes raise complaint and legal risk | Map only the work `email` |
| Using an old guide's path | Some guides show scraper paths as GET or under other names | Use the paths in `references/scrapercity-catalog.md` |

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule, or which file to open. |
| `references/automation-recipes.md` | Setting up Clay, n8n, Zapier, Make, Pipedream, Google Sheets (tested Apps Script included) or Airtable. |
| `references/crm-and-sender-recipes.md` | Loading into HubSpot, Pipedrive, GoHighLevel, Instantly, Smartlead, Lemlist, EmailBison or ManyReach. |
| `references/field-mapping.md` | Mapping ScraperCity fields to any destination, and the transforms. |
| `templates/output-template.md` | Start every integration plan here. |
| `examples/worked-example.md` | A complete n8n plan: Texas HVAC contractors into GoHighLevel and Smartlead. |
| `scripts/check-output.py` | Run on the finished plan before handing it over. |
| `references/scrapercity-catalog.md` | Tool ids, endpoints and prices. |
| `references/scrapercity-platform.md` | Plans, database allowances, the supported integrations list. |
| `references/scrapercity-agent-patterns.md` | Wallet checks, cost formula, webhook handling, key rules. |

## Related Skills

- `scrapercity-api`: endpoints, bodies, retry logic and tested clients behind every recipe here.
- `scrapercity-mcp` and `scrapercity-cli`: the agent and terminal access paths.
- `scrapercity-lead-database` and `scrapercity-local-business-database`: what to put in the query.
- `email-list-cleaner` and `cold-email-list`: the validated, send-ready file.
- `sending-platforms`: picking and configuring the sender.
- `crm-enricher`: filling gaps in records already in a CRM.
- `using-scrapercity-skills`: router.
