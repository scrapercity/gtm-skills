# Errors, Retries and Rate Budgets

How a ScraperCity API client decides between retry, reuse, narrow and stop. The status codes and their meanings come from `references/scrapercity-catalog.md`, the package's `AGENT_DOCS.txt` and scrapercity.com/how-to-use. The retry rules agree with `references/scrapercity-agent-patterns.md` sections 7 and 8; this file adds the per-call decision tree and the budgeting for automations.

## The one question before any retry

Can repeating this call cost money or create a second run?

| Call | Repeat safe? | Why |
|---|---|---|
| `GET /api/v1/wallet`, `/runs`, `/scrape/status/*`, `/scrape/logs/*`, `/apollo-status` | Yes | Reads |
| `GET /api/downloads/{runId}` | Yes | Same file every time, within 48 hours |
| Database GET or POST | Yes | Re-fetching a record the account already has is free and does not count toward the daily allowance |
| `POST /api/v1/scrape/cancel/{runId}` | Yes | Cancelling twice is harmless |
| `POST /api/v1/scrape/{slug}` | No | A start that reached the server is a paid run. Repeat only after proving no run exists |

## Status code playbook

| Code | Meaning | Reads (GET, database, download) | Starts (POST scrape) |
|---|---|---|---|
| 400 | Bad input. Examples: a database `url` with nothing usable, an unreadable `box`, a Crexi map view with no location | Fix the input. Do not retry unchanged | Fix the input. Do not retry unchanged |
| 401 | Missing or invalid key | Stop. Check the header is `Authorization: Bearer <key>` with no quotes or trailing spaces | Stop |
| 402 | Wallet too low | n/a | Stop. Read the wallet, report the shortfall in dollars, offer a smaller run |
| 403 | Account cancelled or a charge is processing | Stop and tell the user | Stop and tell the user |
| 409 | Same search submitted within about 2 minutes | n/a | Never resubmit. `GET /api/v1/runs?hours=1` and reuse the earlier `runId` |
| 409 `filters_not_applied_yet` | Lead Database company filters not usable yet | Drop those filters or retry later | n/a |
| 429 | Rate limited, or a repeat within 30 seconds | Wait at least 30 seconds, then retry with backoff | Look in `/runs` first; if no matching run, wait 30 seconds and retry once |
| 503 | Temporarily unavailable, or a database search ran too long | Database: narrow the search. Other reads: backoff and retry | Retry later; check `/runs` first |
| Timeout, connection reset, no response | Unknown outcome | Retry with backoff | Do not resubmit blind. Check `/runs` (the samples wait 10 s first), resubmit only if no matching run exists |

## Backoff

For calls marked safe:

```
attempt n fails -> wait min(cap, base x 2^n) with random jitter, then retry
429 at any attempt -> wait at least 30 s instead (AGENT_DOCS: a repeat within 30 s is a 429)
attempt MAX_TRIES fails -> give up and report
```

Set `base`, `cap` and `MAX_TRIES` from how long the job can wait; ScraperCity publishes no values for them. The code samples use base 2 s, cap 60 s and 5 tries. Full jitter spreads retries from parallel workers so they do not hit the limit again on the same second (AWS Architecture Blog, "Exponential Backoff and Jitter"). HTTP 429 itself is defined in RFC 6585 section 4; ScraperCity does not document a `Retry-After` header, so the client cannot rely on one.

## Duplicate windows

Two windows are documented:

| Window | Response | Source |
|---|---|---|
| Identical request within 30 seconds | 429 | scrapercity.com/how-to-use, package `AGENT_DOCS.txt` |
| Same search within about 2 minutes | 409 | package `AGENT_DOCS.txt` |

Design consequences:

- A scheduled job that sends the same database request every few seconds (for example `excludeDelivered=true&page=1` in a tight loop) runs into the 30-second window. Use the `after` cursor, which changes the request each call, or space identical calls more than 30 seconds apart.
- A retry of a POST start inside 2 minutes returns 409 even when the first attempt succeeded. That is the protection working. Find the run.
- Give every start a `fileName` where the tool takes one (`scrape_apollo`, `scrape_builtwith`, `scrape_store_leads`, `scrape_property_lookup`). That name appears as `file_name` in `/runs`, which makes the lookup after a 409 or a lost response exact.

## Rate budget for automations

scrapercity.com/api-docs lists 100 requests a minute per key and 10 scrapes running at once.

| Workload | Requests | Fits in 100 a minute? |
|---|---|---|
| Database pull of 10,000 rows | 100 calls of 100 rows | Yes if paced at 1 call a second (60 a minute); 100 calls back to back would hit the limit |
| Polling 10 short runs every 15 s | 40 a minute | Yes |
| Polling 10 short runs every 5 s | 120 a minute | No. Poll every 15 s or more |
| Clay table of 5,000 rows, one database lookup per row at 10 a second | 600 a minute | No. Set the column to 1 request per 1,000 ms |
| One webhook plus one status call plus one download per finished run | 2 a run | Yes |

Pacing that follows from those limits:

1. Pace sequential calls at one a second or slower. That leaves 40 a minute of headroom for status checks and other tools on the same key.
2. One key per automation. Two automations on one key share the 100 a minute.
3. Never more than 10 starts in flight. Queue the eleventh until a run finishes.
4. Poll at the npm client's 15-second interval or slower, and alert at the top of the tool's published delivery time:

| Tool group | Check every | Alert after (AGENT_DOCS delivery time) |
|---|---|---|
| `validate_emails`, `find_emails`, `find_mobiles`, `find_people`, `scrape_property_lookup`, `search_criminal_records`, `scrape_builtwith` | 15 s | 10 min (1 to 10 min) |
| `scrape_store_leads` | One check | Not `SUCCEEDED` on the first check (instant) |
| `scrape_maps`, `scrape_yelp`, `scrape_angi`, `scrape_zillow_agents`, `scrape_bizbuysell`, `scrape_crexi`, `scrape_airbnb`, `scrape_website_finder`, `scrape_distress_list` | 15 s | 30 min (5 to 30 min) |
| `scrape_apollo` | Webhook; once an hour at most without one | 4 days (up to 4 days) |

## Daily database allowance

Each database allows 100,000 new records a day, reset at midnight UTC. Records the account already has do not count again.

| Plan | Daily new records you plan | Calls (100 per call) | Minutes at 1 call a second |
|---|---:|---:|---:|
| Daily feed | 500 | 5 | under 1 |
| Weekly backfill | 20,000 | 200 | about 3.5 |
| Ceiling | 100,000 | 1,000 | about 17 |

A pull that would pass 100,000 new records in a UTC day stops early. Split it across days and resume with `excludeDelivered=true` plus the `after` cursor.

## Failure runbook

| Symptom | Likely cause | Check | Fix |
|---|---|---|---|
| Every call 401 | Key copied with quotes, spaces or a line break | Print the key length, compare with the dashboard | Re-copy from app.scrapercity.com/dashboard/api-docs |
| Database calls rejected (403 per the Clay guide on scrapercity.com) on a key that works for scrapers | Plan is Starter | `GET /api/v1/wallet` and read `plan.name` | Upgrade to Growth or use a scraper |
| POST start 402 | Balance below the run | `wallet.total_balance_dollars` vs your estimate | Smaller run or a top-up |
| Download non-2xx | Run not `SUCCEEDED`, or older than 48 hours | `GET /api/v1/scrape/status/{runId}` | Wait, or rerun if expired |
| Status stays `RUNNING` for an Apollo run after a day | Normal; Apollo can take several days | `handled / requested` moving? | Leave it; the webhook will fire |
| Status `FAILED` | Bad input or a source-side failure | `statusMessage`, then `GET /api/v1/scrape/logs/{runId}` | Fix inputs before resubmitting |
| Database 503 | Search too broad | Count the same filters with a narrower location | Add a location, size band or category; tile by state or map box |
| Same rows every call | `page` fixed and no `after`, or `excludeDelivered` with `page` above 1 | Inspect the query string | Use `after` from `pagination.next_after` |
| 414 or a refused request on a database GET | Query string too long | Measure the encoded query | Send the same parameters as a POST JSON body |
| Webhook never arrives | URL unregistered or private, or the receiver returned non-2xx | Dashboard webhook page, receiver logs | Fix the URL; the hourly sweep downloads anything missed |
| Duplicate imports downstream | Receiver not keyed on `runId` | Look for the same `runId` twice in your log | Record handled `runId`s before importing |

## Sources

- https://scrapercity.com/api-docs
- https://scrapercity.com/how-to-use
- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- https://www.rfc-editor.org/rfc/rfc6585#section-4
- https://www.rfc-editor.org/rfc/rfc9110#section-15.5.15
