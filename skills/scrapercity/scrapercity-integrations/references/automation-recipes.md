# Automation Platform Recipes

How to connect ScraperCity to Clay, n8n, Zapier, Make, Pipedream, Google Sheets and Airtable. Each recipe gives the mechanism, where the ScraperCity key goes, the field mapping, and the rate and cost guardrails. The ScraperCity side always follows `references/scrapercity-catalog.md` and the `scrapercity-api` skill; the third-party side was checked in each vendor's own documentation on 2026-10-13 (links per section and in Sources).

## ScraperCity rules every recipe obeys

| Rule | Value | Source |
|---|---|---|
| Auth | `Authorization: Bearer <key>` header. Never a query string | scrapercity.com/api-docs, RFC 6750 |
| Key | app.scrapercity.com/dashboard/api-docs, one key per automation | scrapercity.com/agents |
| Requests | 100 a minute per key, 10 scrapes running at once | scrapercity.com/api-docs |
| Duplicates | Identical request within 30 s returns 429; same search within about 2 min returns 409 | package `AGENT_DOCS.txt` |
| Databases | Growth plan and up; 100 per call; 100,000 new records a day per database, reset midnight UTC | `references/scrapercity-platform.md`, scrapercity.com/api-docs |
| Daily feeds | `excludeDelivered=true` plus the `after` cursor, so each call differs and nothing repeats | package `AGENT_DOCS.txt` |
| Scrapers | Async: POST returns `runId`; status until `SUCCEEDED`; CSV from `/api/downloads/{runId}` within 48 hours | package `lib/client.mjs`, scrapercity.com/api-docs |
| Webhooks | Set at app.scrapercity.com/dashboard/webhooks; POST on `SUCCEEDED` or `FAILED` with `runId`, `fileName`, `leadsCount` | scrapercity.com/how-to-use, package `SKILL.md` |
| Paths | Use the paths in `references/scrapercity-catalog.md`. If a guide shows a different path (for example a GET to a scraper), the catalog wins | `references/scrapercity-catalog.md` |

Sync vs async decides the design on every platform:

| ScraperCity call | Returns | Fits a per-row step? |
|---|---|---|
| Lead Database, Local Business Database, Ecommerce Database | Records in the response | Yes |
| Wallet, runs, status | JSON in the response | Yes |
| Any scraper (`find_emails`, `validate_emails`, `scrape_maps`, ...) | Only a `runId` | No. Batch many rows into one run, then finish on the webhook |

A per-row scraper call turns 2,000 rows into 2,000 runs: past the 10 concurrent limit, past 100 requests a minute, and 2,000 CSVs to stitch back together. One `validate_emails` run with 2,000 addresses costs the same 2,000 x $0.0072 = $14.40 and returns one file.

## Clay

**Mechanism.** HTTP API enrichment column (Add enrichment, then HTTP API, Configure tab). Method, endpoint, query parameters, headers, JSON body and field paths are set per column; column values are inserted by name (Clay University, HTTP API integration overview).

**Where the key goes.** Save `Authorization: Bearer <key>` as an "HTTP API (Headers)" account (Select header account, then Add account). Clay stores it encrypted at the workspace level and reuses it across columns. Headers typed straight into the column are visible in plain text to anyone with access to the column.

**Recipe: find the decision maker for each company row (sync).**

| Setting | Value |
|---|---|
| Method | GET |
| Endpoint | `https://app.scrapercity.com/api/v1/database/leads` |
| Query params | `companyDomain` = the Domain column, `title` = `VP Sales, Head of Sales`, `hasEmail` = `true`, `limit` = `3` |
| Header account | the ScraperCity header account |
| Field paths | `data`, `pagination.total` (then extract the person fields from `data`) |
| Rate limit | Request limit `1`, Duration `1000` ms (60 a minute) |
| Conditional run | only when the Domain column is not empty |

**Recipe: push a finished Clay table into one ScraperCity run (async).** Export the table or send it from an n8n or code step as one `POST /api/v1/scrape/email-validator` with all addresses; bring results back into Clay through a Clay webhook source (Add, then Webhooks, then Monitor webhook). Clay caps each webhook source at 50,000 submissions, and the cap persists after rows are deleted (Clay University, webhook integration guide).

**Guardrails.**

| Risk | Guardrail |
|---|---|
| ScraperCity's own Clay guide shows 10 requests per 1,000 ms | That is 600 a minute against a documented 100 a minute per key. Use 1 per 1,000 ms; drop further on 429 |
| One run per row on a scraper | Never put `/api/v1/scrape/*` in a per-row column. Batch it |
| Whole-table reruns | Use conditional runs so filled rows do not call again. Database re-fetches are free, but they still spend requests |
| Lead Database on Starter | Database calls need Growth. Check the plan with `GET /api/v1/wallet` before building |

## n8n

**Mechanism.** HTTP Request node with a Header Auth credential; Webhook node for ScraperCity notifications (n8n docs: HTTP Request node, Webhook node).

**Where the key goes.** Credentials, Header Auth: Name `Authorization`, Value `Bearer <key>`. In the HTTP Request node choose Generic Credential Type, then Header Auth.

**Recipe: daily feed from a database.**

1. Schedule Trigger, daily.
2. HTTP Request: GET `https://app.scrapercity.com/api/v1/database/local-businesses`, Send Query Parameters with the filters, `excludeDelivered=true`, `limit=100`.
3. Options, Pagination: mode Update a Parameter in Each Request, Type Query, Name `after`, Value `{{ $pageCount === 0 ? "0" : $response.body.pagination.next_after }}`. `$pageCount` starts at zero and `$response` carries the previous body (n8n pagination cookbook). Stop when `next_after` is null and cap the page count at your daily volume / 100.
4. Split Out on `data`.
5. Destination nodes.

**Recipe: scraper run finished.**

1. Webhook node, POST, a long random path. The production URL registers when the workflow is published; the test URL only listens while you click "Listen for test event". Respond Immediately.
2. IF node: is `{{$json.body.runId}}` one this workflow started? (Store started runIds in a Data table or a sheet.) ScraperCity notifies on every run on the account.
3. HTTP Request: GET `/api/v1/scrape/status/{{$json.body.runId}}`; continue only on `SUCCEEDED`.
4. HTTP Request: GET `/api/downloads/{{$json.body.runId}}`, Response Format File.
5. Extract From File, operation Extract From CSV, input binary field `data`.
6. Destination nodes.

**Guardrails.**

| Risk | Guardrail |
|---|---|
| 100 a minute per key | HTTP Request Options, Batching: Items per Batch `1`, Batch Interval `1000` ms for per-item calls |
| 429 | Settings, Retry On Fail, Max Tries `3`, Wait Between Tries `30000` ms, on GET nodes only |
| Duplicate paid starts | Never enable Retry On Fail on a POST to `/api/v1/scrape/*` |
| Pagination re-sending the same request | Identical calls within 30 s return 429; the cursor changes each call, a fixed `page=1` does not |
| Testing burns the daily allowance | Test with `limit=5` and a Manual Trigger before publishing |

## Zapier

**Mechanism.** Webhooks by Zapier action, event Custom Request, for calls with a Bearer header; Catch Hook trigger for ScraperCity notifications. Both are on Professional, Team and Enterprise plans, not Free (Zapier help: Send webhooks in Zaps; Trigger Zaps from webhooks).

**Where the key goes.** Custom Request, Headers: key `Authorization`, value `Bearer <key>`. Zapier's Basic Auth field does not fit a Bearer token. Name the Zap without the key.

**Recipe: hourly feed.**

| Step | Setting |
|---|---|
| Trigger | Schedule by Zapier, Every Hour |
| Action | Webhooks by Zapier, Custom Request, GET `https://app.scrapercity.com/api/v1/database/leads?title=VP%20Sales&country=United%20States&hasEmail=true&excludeDelivered=true&page=1&limit=100` |
| Split | Code by Zapier (JavaScript) returning `data` as an array of objects; later steps run once per object |
| Destination | HubSpot, Google Sheets, Airtable, or a sender |

One call an hour keeps identical requests far outside the 30-second window, and `excludeDelivered=true` with `page=1` returns the next 100 new records each hour, up to 2,400 a day.

**Recipe: scraper run finished.** Catch Hook trigger, then a Filter on `runId`, then Custom Request GET to `/api/v1/scrape/status/{{runId}}`, then a Code by Zapier step that fetches `/api/downloads/{{runId}}` with the Bearer header and returns the parsed rows. Code steps include `fetch`; returning an array runs later steps once per item, and nesting it under `line_items` passes it as one unit (Zapier help: Use JavaScript code in Zaps).

**Guardrails.**

| Risk | Guardrail |
|---|---|
| Task usage | Every object returned by the Code step is a separate run of later steps. 100 records an hour into two actions is 200 tasks an hour |
| Webhooks by Zapier limit | 20,000 requests per 5 minutes per user, 429 above it (Zapier help: Webhooks by Zapier rate limits) |
| No native pagination | Use the hourly `excludeDelivered` pattern, or move bulk pulls to n8n, Pipedream or code |
| URL encoding | Encode spaces and commas in query values (`%20`, `%2C`) |

## Make

**Mechanism.** HTTP app, module Make a request; Webhooks app, Custom webhook; CSV app, Parse CSV (Make apps docs: HTTP, CSV; Make help: Webhooks).

**Where the key goes.** Authentication type API key, stored in a keychain, header name `Authorization`, value `Bearer <key>`. Make's HTTP docs say credentials belong in the Credentials field, not in Headers.

**Recipe: scheduled feed.** Schedule the scenario At regular intervals, for example every 30 minutes. Make a request: GET the database endpoint with Query parameters including `excludeDelivered=true`, `page=1`, `limit=100`; Parse response Yes. Iterator over `data`, then the destination module. Forty-eight runs a day move up to 4,800 new records without any loop logic.

**Recipe: scraper run finished.** Custom webhook trigger, filter on `runId`, Make a request GET status, Make a request GET `/api/downloads/{runId}` (Parse response No), `toString()` on the data, Parse CSV with CSV contains headers on, then the destination.

**Guardrails.**

| Risk | Guardrail |
|---|---|
| Webhook intake | 300 incoming requests per 10 seconds; over that returns 429; a full queue returns 400 (Make help: Webhooks) |
| Idle webhook | A webhook not attached to a scenario for 5 days is deactivated and returns 410 |
| Slow responses | Make a request Timeout accepts 1 to 300 seconds; database calls with `limit=100` return well inside 60 |
| Operations cost | Each module run counts toward the Make plan. Iterating 100 records into 2 modules is 200 operations per page |

## Pipedream

**Mechanism.** Workflows with a Schedule or HTTP / Webhook trigger and Node.js or Python code steps (Pipedream docs: Triggers, Environment variables, Limits).

**Where the key goes.** Settings, Environment Variables: `SCRAPERCITY_API_KEY`, marked Secret (the default for new variables). Read it with `process.env.SCRAPERCITY_API_KEY` in Node or `os.environ["SCRAPERCITY_API_KEY"]` in Python. Do not `console.log` it.

**Recipe.** Paste the client from the `scrapercity-api` skill (`references/code-samples.md`) into a Node code step, or call `fetch` directly. For webhooks, the HTTP trigger URL (`*.m.pipedream.net`) goes in the ScraperCity dashboard; it answers 200 by default, and `$.respond({ immediate: true, status: 200 })` answers before the rest of the workflow runs.

**Guardrails.**

| Risk | Guardrail |
|---|---|
| Timeouts | Default 30 s for HTTP-triggered and 60 s for scheduled workflows; up to 300 s on free tiers and 750 s on paid. A 1,000-row database pull at 1 call a second needs about 10 s plus destination time |
| HTTP trigger intake | About 10 requests a second on average |
| Body size | 512KB default request body on the HTTP trigger |
| Credits | Credits scale with memory and run time; keep loops paced, not idle-polling |

## Google Sheets

**Mechanism.** Google Apps Script bound to the sheet, using `UrlFetchApp`, with the key in Script properties. Sheets formulas such as `IMPORTDATA` cannot send an Authorization header, so they cannot call ScraperCity. Zapier, Make and n8n Sheets actions work too; use them when one of those already runs the flow.

**Where the key goes.** Apps Script editor, Project Settings, Script properties: `SCRAPERCITY_API_KEY`. Script properties are shared by every user of the script, so keep the sheet's editors to people allowed to spend the wallet.

```js
// file: scrapercity-sheet.js
// Google Apps Script. Project Settings > Script properties: SCRAPERCITY_API_KEY.
// Database calls go as POST bodies because Apps Script caps a fetch URL at 2KB.
const SC_BASE = 'https://app.scrapercity.com'
const COLS = ['title', 'category_name', 'phone', 'website', 'emails', 'address', 'city', 'state',
  'postal_code', 'total_score', 'reviews_count', 'contact_first_name', 'contact_last_name', 'contact_email']

function scCall_ (method, path, body) {
  const key = PropertiesService.getScriptProperties().getProperty('SCRAPERCITY_API_KEY')
  const opts = { method, headers: { Authorization: 'Bearer ' + key }, muteHttpExceptions: true }
  if (body) {
    opts.contentType = 'application/json'
    opts.payload = JSON.stringify(body)
  }
  const res = UrlFetchApp.fetch(SC_BASE + path, opts)
  const code = res.getResponseCode()
  const data = JSON.parse(res.getContentText() || '{}')
  if (code >= 300) throw new Error('ScraperCity ' + code + ': ' + (data.error || data.message || ''))
  return data
}

function pullNewBusinesses () {
  const book = SpreadsheetApp.getActive()
  const sheet = book.getSheetByName('Leads') || book.insertSheet('Leads')
  if (sheet.getLastRow() === 0) sheet.appendRow(COLS)
  const params = {
    keyword: ['HVAC contractor'], state: 'TX', country: ['US'], hasEmail: 'true',
    excludeDelivered: 'true', limit: 100, after: '0'
  }
  let added = 0
  for (let i = 0; i < 5; i++) { // 5 pages, 500 records, well inside the 6 minute run limit
    const page = scCall_('post', '/api/v1/database/local-businesses', params)
    const rows = (page.data || []).map((r) => COLS.map((c) => {
      const v = r[c]
      if (Array.isArray(v)) return v.join('; ')
      return v === undefined || v === null ? '' : v
    }))
    if (rows.length) {
      sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, COLS.length).setValues(rows)
      added += rows.length
    }
    const next = page.pagination && page.pagination.next_after
    if (!next) break
    params.after = String(next)
    Utilities.sleep(1000)
  }
  console.log(added + ' rows added')
}
```

Add a time-driven trigger (Triggers, Add Trigger, Time-driven, Day timer) to run `pullNewBusinesses` daily.

**Guardrails.**

| Risk | Guardrail |
|---|---|
| URL length | 2KB per fetch URL in Apps Script. Always POST database filters as JSON |
| Run time | 6 minutes per execution; triggers total 90 min a day on consumer accounts, 6 h on Workspace |
| Fetch quota | 20,000 URL Fetch calls a day on consumer accounts, 100,000 on Workspace |
| Sheet size | A sheet is a working list, not a CRM. Move to Airtable or a CRM past tens of thousands of rows |

## Airtable

**Mechanism.** Airtable Web API, `POST https://api.airtable.com/v0/{baseId}/{tableIdOrName}` to create records, or `PATCH` with `performUpsert` and `fieldsToMergeOn` to create-or-update by a key field. Called from n8n, Make, Zapier, Pipedream or code (Airtable Web API: Create records, Update multiple records, Rate limits).

**Where the keys go.** ScraperCity key in the automation tool's secret store, as in its recipe above. Airtable personal access token with `data.records:write` scope in the same store, sent as `Authorization: Bearer`.

**Recipe.** Database page (100 records) to 10 Airtable requests of 10 records each, `PATCH` with `performUpsert: { fieldsToMergeOn: ["Email"] }` for people or `["Website"]` for businesses, and `typecast: true` so number and select fields accept strings.

**Guardrails.**

| Risk | Guardrail |
|---|---|
| Records per request | 10 (Airtable support: Managing API call limits) |
| Rate | 5 requests a second per base; 50 a second per token; a 429 means wait 30 s |
| Monthly calls | Free 1,000 API calls a month, Team 100,000; Business and Enterprise Scale have no fixed monthly cap. 2,000 records a day at 10 per call is 6,000 calls a month, over the Free cap |
| Upsert keys | `fieldsToMergeOn` takes 1 to 3 fields, not formulas or lookups; more than one match fails the request |

## Sources

- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://scrapercity.com/integrations
- https://www.npmjs.com/package/scrapercity
- https://university.clay.com/docs/http-api-integration-overview
- https://university.clay.com/docs/webhook-integration-guide
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- https://docs.n8n.io/code/cookbook/http-node/pagination/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/common-issues/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.extractfromfile/
- https://help.zapier.com/hc/en-us/articles/8496326446989-Send-webhooks-in-Zaps
- https://help.zapier.com/hc/en-us/articles/8496288690317-Trigger-Zaps-from-webhooks
- https://help.zapier.com/hc/en-us/articles/29972220283789
- https://help.zapier.com/hc/en-us/articles/8496310939021-Use-JavaScript-code-in-Zaps
- https://help.zapier.com/hc/en-us/articles/8496288648461
- https://apps.make.com/http
- https://apps.make.com/csv
- https://help.make.com/webhooks
- https://help.make.com/schedule-a-scenario
- https://pipedream.com/docs/workflows/building-workflows/triggers
- https://pipedream.com/docs/workflows/environment-variables
- https://pipedream.com/docs/workflows/limits
- https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app
- https://developers.google.com/apps-script/guides/services/quotas
- https://developers.google.com/apps-script/guides/properties
- https://airtable.com/developers/web/api/create-records
- https://airtable.com/developers/web/api/update-multiple-records
- https://airtable.com/developers/web/api/rate-limits
- https://support.airtable.com/docs/managing-api-call-limits-in-airtable
