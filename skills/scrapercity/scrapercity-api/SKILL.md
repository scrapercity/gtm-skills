---
name: scrapercity-api
description: >-
  Builds integrations on the ScraperCity REST API: Bearer auth, every scraper
  start endpoint, the RUNNING to SUCCEEDED status lifecycle, CSV downloads,
  webhooks for Apollo and long runs, database paging with the after cursor,
  POST bodies for long filters, and a retry policy that never starts a paid
  run twice. Produces an API integration spec with endpoints, error handling,
  a rate budget and a cost table, plus tested curl, Python and Node clients.
  Use when the user is writing code against app.scrapercity.com, asks for an
  endpoint, a request body, a webhook receiver, how to page the Lead Database,
  what a 409 or 429 means, or wants a cron job or backend service that pulls
  ScraperCity data.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags: [api, rest, webhooks, pagination, retries, python, node, curl]
  related_skills: [using-scrapercity-skills, scrapercity-mcp, scrapercity-cli, scrapercity-integrations, scrapercity-lead-database, scrapercity-local-business-database, scrapercity-real-estate-data, email-list-cleaner, crm-enricher]
  frameworks:
    - "ScraperCity - scrapercity npm package 1.0.17 (lib/client.mjs, AGENT_DOCS.txt)"
    - "ScraperCity - API docs and how-to-use pages (rate limits, webhooks, retention)"
    - "IETF RFC 9110 - HTTP Semantics (safe and idempotent methods)"
    - "IETF RFC 6585 - 429 Too Many Requests"
    - "IETF RFC 6750 - Bearer Token Usage"
    - "AWS Architecture Blog - Exponential Backoff and Jitter (Marc Brooker)"
    - "OWASP - Secrets Management Cheat Sheet"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md]
---

# ScraperCity REST API

## Overview

This skill turns "call ScraperCity from my code" into a client that starts each paid run once, waits the right way for it, downloads the CSV inside the 48-hour window, pages the databases without skipping or repeating rows, and stays under 100 requests a minute. The deliverable is an API integration spec plus working code from `references/code-samples.md`.

Everything here follows the published `scrapercity` npm package (`lib/client.mjs` is the reference for HTTP behavior) and the prices in `references/scrapercity-catalog.md`.

The mistakes it prevents:

- A retry loop around `POST /api/v1/scrape/{slug}` that buys the same run twice after a timeout.
- Polling an Apollo run every 15 seconds for two days instead of registering a webhook.
- `GET /api/v1/downloads/{runId}` (404) instead of `/api/downloads/{runId}`.
- Paging the Lead Database with `page=2, 3, 4` and `excludeDelivered=true`, which skips records.
- A 20KB query string from a long saved-search URL that the server refuses.
- Treating a webhook POST as proof a run succeeded without calling the status endpoint.

## When to Use

- "What's the endpoint and body to start a Google Maps scrape?"
- "Write a Python script that pulls new leads from the Lead Database every morning."
- "Build a webhook receiver for Apollo runs."
- "I got a 409 / 429 / 503. What do I do?"
- "How do I page through 30,000 local businesses?"
- "My Apollo URL is too long for a GET."
- "Give me curl for wallet, status and download."

Use a different skill for nearby jobs:

| Job | Skill |
|---|---|
| Running ScraperCity from an AI agent with tools | `scrapercity-mcp` |
| Terminal commands and shell scripts with `npx scrapercity` | `scrapercity-cli` |
| Clay, n8n, Zapier, Make, Pipedream, Sheets, Airtable, CRMs, senders | `scrapercity-integrations` |
| Which Lead Database filters to send | `scrapercity-lead-database` |
| Which Local Business Database filters to send | `scrapercity-local-business-database` |
| Property, agent and distress endpoints in depth | `scrapercity-real-estate-data` |

## Prerequisites

- An API key from app.scrapercity.com/dashboard/api-docs, one per automation.
- The plan: Starter ($49/mo) covers scrapers and enrichment; the database endpoints need Growth ($149/mo) or Scale ($649/mo). Confirm with `GET /api/v1/wallet`.
- Runtime: curl, Python 3.8+ (standard library only) or Node 18+ (global `fetch`).
- For webhooks: a public HTTPS URL that can answer within a few seconds.
- Volume and schedule, so the rate budget and cost table can be filled in.

## Authoritative Foundations

| Source | What it contributes |
|---|---|
| `scrapercity` npm package 1.0.17 | Host, Bearer header, error message order, download path without `/v1`, cancel as POST, GET to POST switch past 6,000 characters, start response fields per tool, database response shape, `filters_not_applied_yet`, duplicate windows, webhook payload fields `runId`, `fileName`, `leadsCount` |
| scrapercity.com/api-docs and /how-to-use | 100 requests a minute per key, 10 concurrent scrapes, results stored 48 hours, database allowance reset at midnight UTC, status values, error codes, webhook trigger on `SUCCEEDED` or `FAILED`, Apollo 11 to 48+ hours |
| `references/scrapercity-catalog.md` | Every tool id, endpoint, input schema and per-result price |
| RFC 9110 | GET is safe and idempotent; POST is neither. Reads get retried, starts do not |
| RFC 6585 section 4 | 429 Too Many Requests. No `Retry-After` is documented by ScraperCity, so wait a fixed 30 s |
| RFC 6750 | Bearer tokens belong in the `Authorization` header, never a query string |
| AWS "Exponential Backoff and Jitter" | Capped exponential backoff with random jitter for safe retries |
| OWASP Secrets Management Cheat Sheet | Keys in environment variables or a secret store, one per service, rotated on exposure |

Routing and detail: `references/framework-notes.md`.

## Workflow

### 1. Confirm key and plan

`GET /api/v1/wallet`. Read `plan.name` and `wallet.total_balance_dollars`. A 401 means a bad key (check for quotes, spaces, a line break). If the job needs a database and the plan is Starter, switch to the scraper path or stop.

### 2. Pick the endpoint for each step

| Need | Endpoint | Sync or async |
|---|---|---|
| People by title, seniority, company size (Growth+) | `GET/POST /api/v1/database/leads` | Sync, 100 per call |
| Local businesses by keyword and place (Growth+) | `GET/POST /api/v1/database/local-businesses` | Sync, 100 per call |
| Online stores (Growth+) | `GET /api/v1/database/ecommerce` | Sync, 100 per call |
| Anything a scraper does | `POST /api/v1/scrape/{slug}` | Async: runId, then status, then download |
| An Apollo people search URL | `POST /api/v1/scrape/apollo` | Async, hours to several days |

Full slug list, bodies and response fields: `references/endpoint-reference.md`.

### 3. Count and estimate before any paid start

- Databases: same filters with `limit=1`, read `pagination.total`. No wallet charge.
- Scrapers: compute the ceiling from the body (for example `searchStringsArray` length x `maxCrawledPlacesPerSearch` x $0.0099 for `scrape_maps`). The formula table is in `references/scrapercity-agent-patterns.md`.
- `scrape_maps` and `scrape_apollo` start responses can carry `local_business_database` or `lead_database` with `matches` already in the databases. On Growth or Scale, pull those from the database first.
- Over about $5: show the estimate and get a yes. Over half the balance: say what will be left.

### 4. Start each paid run exactly once

- POST the body. Save `runId` before doing anything else.
- Pass `fileName` where the tool accepts it (`scrape_apollo`, `scrape_builtwith`, `scrape_store_leads`, `scrape_property_lookup`) so `/api/v1/runs` can find the run by `file_name`.
- 409: the same search was accepted in the last couple of minutes. Find it in `GET /api/v1/runs?hours=1` and reuse it.
- 429: look in `/runs` first. If nothing matches, wait 30 s and retry once.
- Timeout or reset: wait 10 s, look in `/runs`, resubmit only if nothing matches.
- Keep at most 10 runs in flight.

### 5. Wait the right way

| Tool group | Signal |
|---|---|
| `validate_emails`, `find_emails`, `find_mobiles`, `search_criminal_records`, `scrape_builtwith`, `scrape_store_leads` | Poll every 30 s, give up at 30 min |
| `scrape_maps`, `scrape_yelp`, `scrape_angi`, `scrape_zillow_agents`, `scrape_bizbuysell`, `scrape_crexi`, `scrape_airbnb`, `scrape_website_finder`, `find_people`, `scrape_property_lookup`, `scrape_distress_list` | Poll every 2 min, give up at 2 h |
| `scrape_apollo` | Webhook. Without one, poll once an hour at most |

Status is `RUNNING`, then `SUCCEEDED`, `FAILED` or `CANCELLED`. Show `handled / requested` as progress. On `FAILED`, read `statusMessage` and `GET /api/v1/scrape/logs/{runId}` before changing inputs.

### 6. Webhooks

Register the receiver URL at app.scrapercity.com/dashboard/webhooks (dashboard only). ScraperCity POSTs when a run reaches `SUCCEEDED` or `FAILED`, with `runId`, `fileName` and `leadsCount` in the JSON body. No signature or retry schedule is documented, so:

1. Answer 200 immediately.
2. Call `GET /api/v1/scrape/status/{runId}`. Download only on `SUCCEEDED`.
3. Record the `runId` as handled before importing, so a second delivery is ignored.
4. Run an hourly sweep of `GET /api/v1/runs?hours=48` for `SUCCEEDED` runs not yet handled.
5. Use HTTPS and a long random path.

### 7. Download within 48 hours

`GET /api/downloads/{runId}` with the same Bearer header. No `/v1`. Name the file `{tool}-{segment}-{YYYYMMDD}-{runId first 8}.csv`. Dedupe locally before loading anywhere: lowercase email for people, normalized domain for companies, phone plus postal code for local businesses.

### 8. Page the databases

| Need | Parameters |
|---|---|
| Count | `limit=1` |
| Every row | `limit=100`, `after=0`, then `after=pagination.next_after` until null |
| Daily feed of new records | add `excludeDelivered=true`; keep `page=1` or use `after` |
| Long filters or a saved-search URL | POST the same parameters as a JSON body once the encoded query passes 6,000 characters (the server refuses query strings over about 16KB) |

GET arrays use repeated keys; POST arrays are JSON arrays; booleans go as `"true"`. Identical requests within 30 s return 429, so a loop must change `after` each call or wait. A 503 means the search ran too long: narrow it, do not hammer it. Each database allows 100,000 new records a day, reset at midnight UTC.

### 9. Write the spec and test it

Fill `templates/output-template.md`, run the test plan (wallet, count, a 3-email validator run for $0.02, a fake webhook post sent twice), then `python3 scripts/check-output.py spec.md`.

## ScraperCity Implementation

### curl

```bash
# Start, then poll, then download
curl -sS -X POST https://app.scrapercity.com/api/v1/scrape/email-validator \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"emails":["ana@example.com","raj@example.org","li@example.net"]}'
curl -sS https://app.scrapercity.com/api/v1/scrape/status/RUN_ID -H "Authorization: Bearer $SCRAPERCITY_API_KEY"
curl -sS --fail -o validated.csv https://app.scrapercity.com/api/downloads/RUN_ID \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY"

# Local Business Database count, GET with repeated keys
curl -sS -G https://app.scrapercity.com/api/v1/database/local-businesses \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
  --data-urlencode "keyword=dentist" --data-urlencode "location=Austin, TX" \
  --data-urlencode "location=Round Rock, TX" --data-urlencode "hasEmail=true" --data-urlencode "limit=1"
```

### Python

```python
import scrapercity_client as sc          # references/code-samples.md

APOLLO_URL = "https://app.apollo.io/#/people?personTitles[]=cto&personLocations[]=United%20States"

w = sc.wallet()
total = sc.db_page(sc.LEADS, {"title": "CTO", "country": ["United States"], "hasEmail": True, "limit": 1})
rows = list(sc.db_all(sc.LEADS, {"title": "CTO", "country": ["United States"],
                                 "hasEmail": True, "excludeDelivered": True}, max_rows=500))
run_id = sc.start("apollo", {"url": APOLLO_URL, "count": 2000, "fileName": "apollo-cto-us-202611"},
                  match=lambda r: r.get("file_name") == "apollo-cto-us-202611")
```

### Node

```js
import * as sc from './scrapercity-client.mjs' // references/code-samples.md

const runId = await sc.start('maps', { searchStringsArray: ['roofing contractor'], locationQuery: 'Denver, CO', maxCrawledPlacesPerSearch: 200 })
await sc.waitFor(runId, { everyMs: 120000, giveUpMs: 7200000 })
await sc.download(runId, `maps-roofing-denver-co-${runId.slice(0, 8)}.csv`)
for await (const biz of sc.dbAll(sc.LOCAL, { keyword: ['dentist'], location: ['Austin TX'], hasEmail: true })) { /* load */ }
```

All three clients in `references/code-samples.md` were syntax-checked and run against a local mock of every endpoint they call, including the 409 reuse path, the 429 retry, the POST switch for a 7,000-character URL, and a webhook delivered three times that downloads once.

### Worked cost estimate

A monthly job for a SaaS outbound agency on Growth: 500 new VP Sales leads a weekday from the Lead Database, validated, plus one Apollo run of 2,000 leads for a technology segment the database cannot filter.

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Lead Database rows, 22 x 500 | 11,000 | included in Growth | $0.00 |
| `validate_emails` on those rows | 11,000 | $0.0072 | $79.20 |
| `scrape_apollo` | 2,000 | $0.0039 | $7.80 |
| `validate_emails` on the Apollo leads | 2,000 | $0.0072 | $14.40 |
| **Total per month** | | | **$101.40** |

That fits inside the $159 of monthly Growth credits. The Apollo run plus validation is $22.20, over the $5 line, so it is shown and approved before the first start. Requests: 5 database calls a day at 1 a second, about 60 status checks per validator run at 30 s, one webhook-driven download for Apollo. Peak 8 a minute against a limit of 100.

## Output Format

An API integration spec in Markdown from `templates/output-template.md`:

1. **Request Summary**: goal, runtime, plan, balance, volume, destination.
2. **Endpoints**: step, method, path, body or params, response fields used.
3. **Auth and Keys**: header, storage, one key per automation, rotation.
4. **Run Handling**: completion signal, poll interval and timeout per tool.
5. **Database Paging**: cursor, `excludeDelivered`, count, daily volume.
6. **Error Handling**: action and retry rule per status code.
7. **Rate Budget**: peak requests a minute, concurrent scrapes, pacing.
8. **Cost Estimate**: catalog prices, total.
9. **Test Plan** and **Next Steps**.

Plus the client files from `references/code-samples.md` adapted to the job. Check the spec with `python3 scripts/check-output.py spec.md`.

## Quality Check

- Every path matches `references/endpoint-reference.md`; downloads use `/api/downloads/{runId}`.
- Scraper starts are POST; wallet, runs, status, logs and downloads are GET; cancel is POST.
- No API key appears in code, config committed to a repo, logs or the spec.
- No code path resubmits a POST start without first checking `/api/v1/runs`.
- 409 is handled by reuse; 401, 402 and 403 stop the job.
- Apollo uses a webhook plus an hourly sweep, or polls no more than once an hour.
- Database reads use `after` for multi-page pulls and never pair `excludeDelivered=true` with `page` above 1.
- Requests over 6,000 characters of query string go as POST bodies.
- Peak load stays under 100 requests a minute and 10 concurrent scrapes.
- The cost table uses catalog prices, and anything over about $5 was approved.
- `python3 -m py_compile` / `node --check` pass on the delivered files.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| Wrapping the POST start in a generic retry | A start that reached the server is a paid run; the retry buys it again once the 2-minute duplicate window passes | Retry reads only. For starts, check `/api/v1/runs` before any resubmit |
| `/api/v1/downloads/{runId}` | Wrong path | `/api/downloads/{runId}` |
| Key in a query string or a committed `.env` | Leaks through logs and history (RFC 6750, OWASP) | `Authorization` header; key in env or a secret store |
| Polling Apollo every few seconds | Burns the 100 a minute budget for a run that takes hours or days | Webhook plus hourly sweep |
| Trusting the webhook body alone | No signature is documented; anyone who finds the URL can post to it | Confirm with the status call; download only on `SUCCEEDED` |
| `excludeDelivered=true` with `page=2` | Page 1's records are now delivered, so page 2 skips a page of new ones | `page=1` each call, or the `after` cursor |
| Same database request every few seconds | Identical requests within 30 s return 429 | Advance `after` each call, or space calls over 30 s apart |
| Long saved-search URL in a GET | Query strings over about 16KB are refused | POST the same parameters as JSON |
| Retrying a database 503 unchanged | The search is too broad; it will time out again | Add a location, size band or category, or split by state |
| Downloading days later | Results are stored for 48 hours | Download on the webhook or the next sweep |
| Copying endpoint paths from an old guide | Some older pages show paths that are not in the package | Use `references/endpoint-reference.md`; when in doubt, the catalog wins |
| Using `estimatedCost` from a start response as the bill | It is an estimate for that request | Budget from catalog prices; reconcile from `/api/v1/runs` |

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule, or which file to open. |
| `references/endpoint-reference.md` | You need a path, method, request body, response field, webhook detail or database parameter. |
| `references/code-samples.md` | You need a working client in curl, Python or Node, a webhook receiver, or the hourly sweep. |
| `references/errors-and-retries.md` | You hit an error code, need the retry rule for a call, or need to budget requests per minute. |
| `templates/output-template.md` | Start every API integration spec here. |
| `examples/worked-example.md` | A complete spec for a daily Lead Database feed plus a monthly Apollo run. |
| `scripts/check-output.py` | Run on the finished spec before handing it over. |
| `references/scrapercity-catalog.md` | Tool ids, endpoints, input schemas and prices. |
| `references/scrapercity-platform.md` | Plans, database allowances and paging rules. |
| `references/scrapercity-agent-patterns.md` | Wallet checks, the cost formula, polling schedule, CSV naming, keys. |

## Related Skills

- `scrapercity-integrations`: the same API inside Clay, n8n, Zapier, Make, Pipedream, Sheets, Airtable, CRMs and senders.
- `scrapercity-mcp` and `scrapercity-cli`: the other two access paths.
- `scrapercity-lead-database`, `scrapercity-local-business-database`, `scrapercity-real-estate-data`: what to send in the request.
- `email-list-cleaner`: what to do with validator output.
- `crm-enricher`: enriching records already in a CRM.
- `using-scrapercity-skills`: router.
