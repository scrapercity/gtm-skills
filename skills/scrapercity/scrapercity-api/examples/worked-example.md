# ScraperCity API Integration Spec: Daily VP Sales feed for a SaaS outbound agency

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

## Request Summary

| Item | Value |
|---|---|
| Goal | Every weekday at 06:00 UTC, pull 500 new VP Sales and Head of Sales contacts at US SaaS companies with 50-200 employees, validate the emails, and drop a send-ready CSV in the agency's S3 bucket. Once a month, pull one extra segment from an Apollo search URL whose technology filter the Lead Database cannot apply |
| Runtime and language | Python 3.11 on a small Linux VM, cron for the schedule, `scrapercity_client.py`, `daily_feed.py`, `webhook_receiver.py` and `sweep.py` from `references/code-samples.md` |
| Plan confirmed by GET /api/v1/wallet | Growth (`plan.name` = Growth, `plan.limit_dollars` = 159) |
| Wallet balance at spec time | $142.60 (`wallet.total_balance_dollars`) |
| Volume and schedule | 500 new leads a weekday (22 weekdays = 11,000 a month) plus one Apollo run of 2,000 leads a month |
| Output destination | `validated-vp-sales-saas-us-YYYYMMDD-{runId first 8}.csv` in S3; the agency's sender imports from there |

## Endpoints

One row per call the integration makes. Paths come from `references/endpoint-reference.md`.

| Step | Method | Path | Body or key params | Response fields used |
|---|---|---|---|---|
| 1. Balance check | GET | `/api/v1/wallet` | none | `plan.name`, `wallet.total_balance_dollars` |
| 2. Count check | GET | `/api/v1/database/leads` | `title=VP Sales, Head of Sales`, `country=United States`, `minEmployees=50`, `maxEmployees=200`, `keywords=saas`, `hasEmail=true`, `limit=1` | `pagination.total` |
| 3. Daily pull | GET | `/api/v1/database/leads` | same filters, `excludeDelivered=true`, `limit=100`, `after=0` then `pagination.next_after` | `data[]`, `pagination.next_after` |
| 4. Validate | POST | `/api/v1/scrape/email-validator` | `{"emails": [500 unique lowercased emails]}` | `runId`, `emailCount`, `estimatedCost` |
| 5. Poll | GET | `/api/v1/scrape/status/{runId}` | none | `status`, `handled`, `requested`, `statusMessage` |
| 6. Download | GET | `/api/downloads/{runId}` | none | CSV bytes |
| 7. Apollo health | GET | `/api/v1/apollo-status` | none | `status` must be `url-based` |
| 8. Monthly Apollo start | POST | `/api/v1/scrape/apollo` | `{"url": "https://app.apollo.io/#/people?personTitles[]=vp%20sales&organizationNumEmployeesRanges[]=51%2C200&currentlyUsingAnyOfTechnologyUids[]=hubspot", "count": 2000, "fileName": "apollo-vp-sales-hubspot-us-202611"}` | `runId`, `lead_database.matches` |
| 9. Sweep and 409 lookup | GET | `/api/v1/runs?hours=48&limit=100` | none | `run_id`, `status`, `file_name` |

## Auth and Keys

| Item | Value |
|---|---|
| Header | `Authorization: Bearer` plus the key, `Content-Type: application/json` on POST |
| Key storage | `SCRAPERCITY_API_KEY` in the VM's systemd environment file, mode 600, never in the repo |
| Keys per automation | One key named "vm-daily-feed" for this job only, so spend and 429s are attributable |
| Rotation | New key in the dashboard on any suspected exposure; update the environment file, restart, revoke the old key |

## Run Handling

| Tool | Completion signal | Poll interval | Give up after |
|---|---|---|---|
| `validate_emails` | Poll status | First check at 30 s, then every 30 s | 30 min, then alert with the runId |
| `scrape_apollo` | Webhook to `https://feeds.example-agency.com/hooks/sc-7f3a9c2e41b8`, plus the hourly `sweep.py` | No polling; the sweep runs every 60 min | 5 days, then alert with the runId |

## Database Paging

| Item | Value |
|---|---|
| Endpoint | `/api/v1/database/leads` |
| Method rule | GET while the encoded query is under 6,000 characters; this one is about 180, so GET |
| limit | 100 |
| Paging | `after` cursor: `0`, then `pagination.next_after` until null or 500 rows |
| excludeDelivered | true |
| page | not sent |
| Count check total | 18,420 matching leads |
| New records per day | 500 (0.5% of the 100,000 daily allowance) |

18,420 / 500 = about 37 weekdays before the segment runs dry. The job logs `pagination.total` daily so the drop is visible.

## Error Handling

| Code | Action | Retry |
|---|---|---|
| 401 | Stop the job, alert "key invalid", check the environment file for quotes | No |
| 402 | Stop before the validator POST, alert with balance and estimate | No, until the wallet is topped up |
| 409 on a start | Look up `/runs?hours=1` by `file_name` and reuse that runId | No, reuse the earlier run |
| 429 | Reads: wait 30 s, then backoff. Starts: check `/runs` first, then wait 30 s and retry once | Yes, reads up to 5 tries; starts once |
| 503 on the database | Log the filters, alert; next run splits the search by `companyState` | No, narrow first |
| Timeout on a POST start | Wait 10 s, look in `/runs`, resubmit only if no matching run exists | Only after the lookup |

## Rate Budget

| Item | Value |
|---|---|
| Peak requests per minute | 8 (wallet, count, 5 database pages at 1 a second, validator start) |
| Concurrent scrapes | 2 at most (validator plus a running Apollo job) |
| Pacing | Database pages 1 a second; status checks every 30 s; the sweep makes 1 call an hour plus 1 download per new run |

## Cost Estimate

Prices from `references/scrapercity-catalog.md`. Lead Database rows are included in Growth.

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Lead Database rows, 22 weekdays x 500 | 11,000 | $0.00 (Growth) | $0.00 |
| `validate_emails`, 22 x 500 unique emails | 11,000 | $0.0072 | $79.20 |
| `scrape_apollo`, one run a month | 2,000 | $0.0039 | $7.80 |
| `validate_emails` on the Apollo leads | 2,000 | $0.0072 | $14.40 |
| Total per month | | | $101.40 |

$101.40 is under the $159 of monthly Growth credits. The first daily run costs $3.60 and the Apollo run plus its validation $22.20, both shown to the agency owner before go-live because each is close to or over the $5 approval line. If the Apollo start response shows `lead_database.matches` of 640, those 640 come from the database at no wallet charge and the Apollo `count` drops to 1,360, saving 640 x $0.0039 = $2.50.

## Test Plan

| Check | Result |
|---|---|
| `GET /api/v1/wallet` with the new key | 200, plan Growth, balance $142.60 |
| Count with `limit=1` | `pagination.total` 18,420 |
| Cursor pull capped at 250 rows on a test day | 250 rows, 3 calls, no repeated ids |
| Validator on 3 known addresses | `SUCCEEDED` in under 2 min, CSV downloaded, cost $0.02 |
| Fake webhook post with an existing runId, sent twice | One download, second post ignored by the `runId` log |
| Same filters sent as a POST JSON body | Same `pagination.total` as the GET |
| `python3 -m py_compile` and a cron dry run | Pass |

## Next Steps

1. Register `https://feeds.example-agency.com/hooks/sc-7f3a9c2e41b8` at app.scrapercity.com/dashboard/webhooks and post one test notification.
2. Turn on the 06:00 UTC weekday cron for `daily_feed.py` and the hourly cron for `sweep.py`.
3. Review the first week: rows delivered, validator pass rate, wallet spend against the $101.40 monthly estimate.
