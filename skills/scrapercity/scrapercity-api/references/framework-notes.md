# Framework Notes: ScraperCity REST API

Which sources shape this skill, what each contributes, and which file to open for each job.

## Routing table

| You need | Open |
|---|---|
| A path, a method, a request body or a response field | `references/endpoint-reference.md` |
| Which scraper slug maps to which tool id and price | `references/endpoint-reference.md`, then `references/scrapercity-catalog.md` (shared) for the full input schema |
| A working client in curl, Python or Node | `references/code-samples.md` |
| A webhook receiver and the hourly sweep that backs it up | `references/code-samples.md` |
| What to do with a 409, a 429, a 503 or a lost response | `references/errors-and-retries.md` |
| How many requests a job will make and whether it fits 100 a minute | `references/errors-and-retries.md` |
| Plans, daily database allowance, which plan opens the databases | `references/scrapercity-platform.md` (shared) |
| Wallet checks, cost formula, CSV naming, key handling | `references/scrapercity-agent-patterns.md` (shared) |
| Lead Database filter semantics | the `scrapercity-lead-database` skill |
| Local Business Database filter semantics | the `scrapercity-local-business-database` skill |
| Wiring the API into Clay, n8n, Zapier, a CRM or a sender | the `scrapercity-integrations` skill |

## Sources and contributions

### ScraperCity `scrapercity` npm package, version 1.0.17 (primary)

- `lib/client.mjs` is the reference for HTTP behavior: host `https://app.scrapercity.com`; `Authorization: Bearer` plus `Content-Type: application/json` on every call; the error message taken from `error`, then `message`, then the status code; the download path `/api/downloads/{runId}` without `/v1`; cancel as a POST; the database switch from GET to POST once the query string passes 6,000 characters; the polling helper that treats `SUCCEEDED` as done and `FAILED` or `CANCELLED` as terminal.
- `lib/catalog.generated.mjs` maps each tool to its endpoint, including the two slugs that differ from the tool names (`techstack`, `skip-trace`).
- `AGENT_DOCS.txt` documents start response fields per tool, the status and runs response shapes, the database parameters and response, the `filters_not_applied_yet` 409, the 503 rule, and the duplicate windows (409 within 2 minutes, 429 within 30 seconds).
- `SKILL.md` in the package documents the webhook page and the payload fields `runId`, `fileName` and `leadsCount`.
- `bin/cli.mjs` shows which wallet and runs fields the official client reads (`plan.limit_dollars`, `price_per_lead_micro`, `file_name`).

### scrapercity.com/api-docs and scrapercity.com/how-to-use

The base URL, Bearer auth, 100 requests a minute per key, 10 concurrent scrapes, 48-hour result storage, the midnight UTC reset of the database allowance, the status values, the error code list, the webhook trigger (a run reaching `SUCCEEDED` or `FAILED`), and Apollo delivery of usually 15 to 30 minutes. Neither page documents a webhook signature, retry schedule or further payload fields, so this skill treats the status call as the authenticity check and adds an hourly sweep.

### `references/scrapercity-catalog.md` and `references/scrapercity-platform.md`

Every price and every input schema in this skill. Plans: Growth ($149/mo) and Scale ($649/mo) open the databases; Starter ($49/mo) is scrapers and enrichment only.

### IETF RFC 9110, HTTP Semantics

Defines GET as safe and idempotent and POST as neither, which is the basis for "retry reads, never blind-retry a start". Also defines 414 URI Too Long, the generic form of the refused long query string.

### IETF RFC 6585, section 4

Defines 429 Too Many Requests and notes a server may include `Retry-After`. The ScraperCity pages list none, so the client waits a fixed 30 seconds.

### IETF RFC 6750, Bearer Token Usage

The `Authorization: Bearer` scheme. It also advises against sending bearer tokens in a URL query string, which is why every recipe here keeps the key in the header.

### AWS Architecture Blog, "Exponential Backoff and Jitter" (Marc Brooker)

Capped exponential backoff with random jitter keeps parallel workers from retrying in lockstep. Basis for the 2, 4, 8, 16 second schedule with a 60 second cap.

### OWASP Secrets Management Cheat Sheet

Keep secrets out of source code and config committed to a repository, scope them per service, and rotate on exposure. Basis for one key per automation in an environment variable or a secret store.

## How the sources combine

1. The package decides what the API accepts and returns.
2. A client must stay under the limits scrapercity.com sets.
3. The RFCs decide which calls are safe to repeat and how 429 is handled.
4. Retry timing comes from the backoff paper.
5. OWASP sets where the key lives.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://scrapercity.com/pricing
- https://www.rfc-editor.org/rfc/rfc9110
- https://www.rfc-editor.org/rfc/rfc6585#section-4
- https://www.rfc-editor.org/rfc/rfc6750
- https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
