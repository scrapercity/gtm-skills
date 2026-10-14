# ScraperCity Agent Operating Patterns

The rules every skill in this repo follows when it touches ScraperCity, whether through the MCP server, the CLI or the REST API. Tool ids, prices and input schemas come from `references/scrapercity-catalog.md`. Plans, databases and allowances come from `references/scrapercity-platform.md`. Behavior described here was read from the published `scrapercity` npm package (version 1.0.17: `bin/mcp.mjs`, `bin/cli.mjs`, `lib/client.mjs`, `AGENT_DOCS.txt`) and from scrapercity.com/how-to-use, scrapercity.com/mcp, scrapercity.com/agents and scrapercity.com/api-docs, checked 2026-10-12.

## The rules

| # | Rule | Why |
|-|-|-|
| 1 | Call `check_wallet` (CLI `wallet`, REST `GET /api/v1/wallet`) before any paid run. | The wallet is the spending ceiling. A run started on a thin wallet ends in a 402. |
| 2 | Count before you pull. Size the audience with a 1-row database query or a small test run first. | Keeps cost predictable; scrapercity.com/how-to-use says to check result counts before exporting. |
| 3 | Show the user the cost estimate before every paid run and wait for a go-ahead. Start without asking only under a per-run amount the user has set. | Scrapers draw from the wallet per result as they deliver (scrapercity.com/llm-info), so the go-ahead before the start is the one point where the user controls the spend. |
| 4 | Every scraper is start, poll, download. Save the `runId` the moment a run starts. | The `runId` is the only handle for status, download, cancel and logs. |
| 5 | Apollo runs go through a webhook. If you must poll, once an hour at most. | Apollo takes from hours to several days (scrapercity.com/how-to-use). |
| 6 | Never loop-poll inside a conversation. Check, report, and check again later. | Each check costs a tool call and context. A run that needs 20 minutes does not need 80 checks. |
| 7 | Page databases with the `after` cursor and use `excludeDelivered=true` for repeat pulls. | Cursor paging does not skip or repeat rows; `excludeDelivered` returns only records the account does not already have. |
| 8 | On a 409, find the earlier run instead of resubmitting. | The same search was already accepted. Resubmitting does not get a second run. |
| 9 | Retry only what is safe to retry (reads, and starts that got no response), with backoff. | A blind retry of a POST that did reach the server can start a second paid run once the duplicate window passes. |
| 10 | Name every CSV by tool, segment, date and run id, and download within 48 hours. | scrapercity.com/api-docs says results are stored for 48 hours. |
| 11 | Send many inputs in one run: one `validate_emails` call with 2,000 addresses, one `find_emails` call with 500 contacts. Never one run per row. | One run per row spends a request, a run slot and a CSV per record, and trips the 10 concurrent scrapes and 100 requests a minute limits. |
| 12 | A miss is unknown. When a tool returns no email, phone, title or match, record it as not found and never construct a pattern address or fill the gap from memory. | A guessed address bounces and lands on suppression lists; a guessed title sends the wrong message. Email Finder and Mobile Finder already charge nothing for a miss. |

## 1. Wallet check

MCP: `check_wallet` takes no arguments. CLI: `npx scrapercity wallet`. REST: `GET https://app.scrapercity.com/api/v1/wallet`.

Fields the package reads from the response:

| Field | Meaning |
|-|-|
| `plan.name` | Plan name (Starter, Growth, Scale) |
| `plan.limit_dollars`, `plan.used_dollars`, `plan.usage_percent` | Cycle allowance and how much is used |
| `wallet.total_balance_dollars` | What the agent can spend right now |
| `wallet.balance_dollars` | Subscription credit part of the balance |
| `wallet.purchased_credits_dollars` | Purchased credit part of the balance |
| `billing.next_billing_date` | When the plan renews |

Decision table:

| Situation | Action |
|-|-|
| Estimate fits within `total_balance_dollars` | Proceed after the user's go-ahead (or under the user's own per-run amount); say what will be left. |
| Estimate exceeds the balance | Do not start. Report the shortfall in dollars and offer a smaller run. |
| User asks for a database tool and `plan.name` is Starter | The Lead Database and Local Business Database need Growth ($149/mo) or higher. Offer the scraper path instead. |

## 2. Count first

| Source | How to count | Cost of counting |
|-|-|-|
| Lead Database | `query_lead_database` with the filters and `limit: 1`; read `pagination.total` | No wallet charge; at most 1 new record counts toward the 100,000 a day allowance |
| Local Business Database | `query_local_business_database` with `limit: 1`; read `pagination.total` and `searched_as` | Same as above |
| Apollo URL | The start response can include `lead_database: { matches, url, api }`, the same filters already in the Lead Database | Apollo charges per lead delivered; check `lead_database.matches` first and use the database when it covers the need |
| Google Maps | The start response can include `local_business_database: { matches, url, api }` | Same idea for local businesses |
| Every other scraper | No count endpoint. Run a small capped test (for example `maxItems: 25`, `searchLimit: 25`, `totalLeads: 100`) and extrapolate | The test is billed at catalog price |

## 3. Cost estimate formula

```
estimate = sum over steps of (expected billable results x catalog price per result)
ceiling  = sum over steps of (maximum billable results x catalog price per result)
```

Show both when they differ. Billing units, from `references/scrapercity-catalog.md`:

| Tool | Billable unit | Price | Ceiling for N inputs or requested rows |
|-|-|-|-|
| `scrape_apollo` | Lead delivered | $0.0039 | count x $0.0039 (count 500 to 50,000) |
| `scrape_maps` | Business | $0.0099 | search terms x `maxCrawledPlacesPerSearch` x $0.0099 |
| `scrape_yelp` | Result | $0.0099 | terms x locations x `searchLimit` x $0.0099 |
| `scrape_angi`, `scrape_bizbuysell` | Listing | $0.0099 | `maxItems` x $0.0099 |
| `scrape_zillow_agents` | Agent | $0.029 | `searchLimit` x $0.029 |
| `scrape_crexi` | Property | $0.029 | Not capped by a parameter; test one URL first |
| `scrape_airbnb` | Result | $0.019 | Test with a small `maxPages` first |
| `scrape_store_leads` | Lead | $0.0039 | `totalLeads` x $0.0039 |
| `scrape_builtwith` (Tech Stack Search) | Technology | $4.99 | technologies x $4.99 |
| `scrape_website_finder` | Contact found | $0.0499 | domains x $0.0499 if every domain hits |
| `find_emails` | Email found (free if not found) | $0.05 | contacts x $0.05 |
| `find_mobiles` | Number found (free if not found) | $0.25 | inputs x $0.25 |
| `validate_emails` | Email | $0.0072 | unique emails x $0.0072 |
| `find_people` | Result (0 matches billed as 1) | $0.0199 | searches x max(`max_results`, 1) x $0.0199 |
| `scrape_property_lookup` | Property | $0.15 (+$0.10 owner contact) | addresses x $0.15, or x $0.25 with `includeOwnerContact` |
| `scrape_distress_list` | Property | $0.05 | `maxItems` x $0.05 (max 500) |
| `search_criminal_records` | Search with records found | $1.00 | searches x $1.00 |
| `query_lead_database`, `query_local_business_database` | Included in Growth and Scale | $0 wallet | Daily allowance of 100,000 new records each |

Worked check: 2,000 Apollo leads plus validating them is 2,000 x $0.0039 = $7.80 plus 2,000 x $0.0072 = $14.40, a ceiling of $22.20. Show it and wait for a yes.

## 4. Start, poll, download

1. Start: MCP scraper tool, CLI scraper command, or `POST /api/v1/scrape/{slug}`. The response carries `runId`.
2. Poll: `check_run_status` / `scrapercity status <runId>` / `GET /api/v1/scrape/status/{runId}`. The response is `{ status, statusMessage, handled, requested, outputUrl }`.
3. Download: `download_results` / `scrapercity download <runId> -o file.csv` / `GET /api/downloads/{runId}` (note: this path has no `/v1`). Only works once `status` is `SUCCEEDED`.

Status lifecycle: `RUNNING` then one of `SUCCEEDED`, `FAILED` or `CANCELLED`. Treat only `SUCCEEDED` as downloadable. On `FAILED`, read `statusMessage` and the run logs (`GET /api/v1/scrape/logs/{runId}`, CLI `logs`) before changing inputs.

### Polling schedule by tool

Intervals come from the package: `pollUntilDone` in `lib/client.mjs` (and the CLI `poll` command) checks every 15 seconds with a 1-hour timeout, and AGENT_DOCS lists a delivery time per tool and says to check Apollo once per hour at most.

| Tool group | Published delivery time | Check | Report to the user when |
|-|-|-|-|
| `validate_emails`, `find_emails`, `find_mobiles`, `find_people`, `scrape_property_lookup`, `search_criminal_records`, `scrape_builtwith` | 1 to 10 minutes | Every 15 s from a script; once per turn in a chat | Still `RUNNING` after 10 minutes |
| `scrape_store_leads` | Instant (cached database) | Once | Not `SUCCEEDED` on the first check |
| `scrape_maps`, `scrape_yelp`, `scrape_angi`, `scrape_zillow_agents`, `scrape_bizbuysell`, `scrape_crexi`, `scrape_airbnb`, `scrape_website_finder`, `scrape_distress_list` | 5 to 30 minutes (the README gives 1 to 30 minutes for every scraper but Apollo) | Every 15 s from a script; once per turn in a chat | Still `RUNNING` after 30 minutes |
| `scrape_apollo` | Up to 4 days | Webhook; if you must poll, once an hour at most | Report the runId and stop the session |

Inside an agent conversation: check once, tell the user the status and `handled / requested`, and check again on the next turn or when the user asks. Do not chain status calls back to back.

## 5. Webhooks for Apollo and long runs

- Register the receiving URL at app.scrapercity.com/dashboard/webhooks before starting the run.
- ScraperCity sends a POST when a run reaches `SUCCEEDED` or `FAILED`. The payload includes `runId`, `fileName` and `leadsCount`.
- The receiver answers 200 fast, then calls the status endpoint with the `runId` to confirm `SUCCEEDED` before downloading. No signature scheme is documented, so the status call is how the receiver confirms the notification before acting on it.
- Key the work on `runId` so a repeated delivery does not import the same CSV twice.

## 6. Database paging and dedupe across runs

| Need | Parameters |
|-|-|
| One page to look at | `page: 1`, `limit: 100` |
| Every row of a large search | `after: "0"`, then `after = pagination.next_after` until it is null |
| Only records this account does not have yet | `excludeDelivered: true` with `page: 1` or with `after` |
| A saved people-search or Google Maps URL | `url: "<the url>"`; read `search_translation` for applied, approximated and not supported filters |
| Very long filters or URLs | Send `POST` with a JSON body. A query string over about 16KB is refused; the package switches to POST past 6,000 characters |

Every record returned is saved to the account. Only new records count toward the 100,000 a day allowance, and fetching a record the account already has is free. That makes `excludeDelivered=true` the dedupe tool for daily pulls: yesterday's leads never come back.

For scraper CSVs (which have no `excludeDelivered`), dedupe locally on a stable key before loading anywhere: lowercase email for people, normalized domain for companies, phone plus postal code for local businesses.

Cutting a pull to the number the user asked for: never take the first N rows in the order they arrived, because cursor order is id order and one company can fill several slots. Keep only rows whose email validated `valid`, sort by the user's title order (the order the request names the roles in), keep at most the user's per-company cap per company domain (when the user gave none, one contact per role named in the request), then take the first N. Keep the rows past N as spares in their own file.

## 7. Error handling

| Code | Meaning | Agent action | Safe to retry? |
|-|-|-|-|
| 400 | Bad input, such as a database `url` with no usable filters, an unreadable `box`, or a Crexi map view with no location | Fix the input from the message | After fixing |
| 401 | Missing or invalid API key | Stop. Ask for a valid key. Check the env block for stray quotes or spaces | No |
| 402 | Wallet balance too low | `check_wallet`, report the shortfall, wait for the user | After a top-up |
| 403 | Account cancelled or a charge is processing | Stop and tell the user | No |
| 409 | Same search submitted moments ago | `list_runs` (hours 1) and reuse the earlier `runId` | No, reuse |
| 409 `filters_not_applied_yet` (Lead Database) | Some company filters cannot be used yet; nothing returned or counted | Drop those filters or retry later | Later |
| 429 | Rate limited, or a repeat within about 30 seconds | Wait at least 30 s, then retry once | Once |
| 503 | Temporarily unavailable, or a database search ran too long | For databases, narrow (add location, size band, fewer titles); otherwise retry later | After narrowing |

MCP tools return failures as text starting with `Error:` and the server's message, with the call marked as an error. The CLI prints the message to stderr and exits 1.

## 8. Safe retry

| Call | Retry policy |
|-|-|
| Any GET (wallet, runs, status, download, database) | Retry on 429, 503 and network errors with capped exponential backoff plus full jitter (AWS Architecture Blog). After a 429 wait at least 30 s, since AGENT_DOCS defines 429 as a duplicate within 30 s. Set the cap and the number of tries from how long the job can wait |
| POST start, response received with an error code | Follow the error table; never resubmit on 409 |
| POST start, no response (timeout, connection reset) | Do not resubmit blind. Call `list_runs` for the last hour and look for a run with the same file name or inputs. Resubmit only if none exists |
| Cancel | Safe to repeat |

scrapercity.com/api-docs lists 100 API requests per minute per key and 10 concurrent scrapes. Stay under both from automations even where other pages say there is no hard limit beyond the wallet.

## 9. CSV naming and storage

Pattern: `{tool}-{segment}-{YYYYMMDD}-{runId first 8}.csv`, all lowercase, hyphens only.

Examples: `apollo-vp-sales-saas-us-20261012-a1b2c3d4.csv`, `maps-plumbers-denver-co-20261012-9f8e7d6c.csv`, `validated-vp-sales-saas-us-20261013-0a1b2c3d.csv`.

- Pass `fileName` where the tool accepts it (`scrape_apollo` and `scrape_builtwith` cap it at 50 characters; `scrape_store_leads` and `scrape_property_lookup` also take it) so the dashboard and `list_runs` show the same name.
- In MCP, give `download_results` an absolute `outputPath`. The default is `{runId}.csv` in the server's working directory, which for a desktop client may not be a folder the user can find.
- Keep a run log row per run: date, tool, inputs summary, runId, status, rows, cost, file path.

## 10. Keys

- One API key per agent or automation, so spend can be tracked and one key revoked without breaking the rest (scrapercity.com/agents).
- Keys live in `SCRAPERCITY_API_KEY` or `~/.scrapercityrc` (written by `scrapercity login` with owner-only permissions). The environment variable wins when both exist.
- Never paste a key into a shared file, a committed config, a Zap name or a sheet cell.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/how-to-use
- https://scrapercity.com/mcp
- https://scrapercity.com/agents
- https://scrapercity.com/api-docs
- https://scrapercity.com/llm-info
- https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- https://www.rfc-editor.org/rfc/rfc6585#section-4
