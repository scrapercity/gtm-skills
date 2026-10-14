# ScraperCity Integration Plan: Texas HVAC contractors into Smartlead and GoHighLevel via n8n

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

## Request Summary

| Item | Value |
|---|---|
| Goal | A home-services marketing agency wants 300 new Texas HVAC contractors rated 4 stars and up every weekday: every business into its GoHighLevel sub-account as a contact for the call team, and every business with a valid email into a Smartlead cold campaign |
| Automation platform | n8n Cloud, two workflows: "HVAC TX daily pull" and "ScraperCity run finished" |
| Destinations | Smartlead campaign "HVAC TX - review offer"; GoHighLevel sub-account "Agency Prospects" |
| ScraperCity plan and balance | Growth, $131.40 `wallet.total_balance_dollars` on 2026-10-13 |
| Volume and cadence | 300 new businesses a weekday, about 6,600 a month |

## Data Flow

| Step | Tool | Action | Trigger |
|---|---|---|---|
| 1 | n8n | Schedule Trigger, weekdays 07:00 | Schedule |
| 2 | ScraperCity | `GET /api/v1/wallet`; stop and alert if `plan.name` is not Growth or Scale, or balance is under $10 | Step 1 |
| 3 | ScraperCity | `GET /api/v1/database/local-businesses` with `keyword=HVAC contractor`, `state=TX`, `country=US`, `minRating=4`, `hasEmail=true`, `excludeDelivered=true`, `limit=100`, cursor `after` for 3 pages | Step 2 |
| 4 | n8n Code node | Pick one email per business (`contact_email`, else first of `emails`), lowercase, dedupe by email and by domain, phone to E.164, website to bare domain | Step 3 |
| 5 | GoHighLevel | `POST /contacts/upsert` for all 300, tag `scrapercity` and `hvac-tx-4star` | Step 4 |
| 6 | ScraperCity | `POST /api/v1/scrape/email-validator` with the 300 emails; save the `runId` and the date in an n8n Data table | Step 4 |
| 7 | n8n Webhook node | Receives the ScraperCity notification; continue only if `runId` is in the Data table and not yet handled | ScraperCity webhook |
| 8 | ScraperCity | `GET /api/v1/scrape/status/{runId}`, then `GET /api/downloads/{runId}` as a file, then Extract From CSV | Step 7, only on `SUCCEEDED` |
| 9 | Smartlead | `POST /api/v1/campaigns/{campaign_id}/leads` with the valid rows in one call | Step 8 |
| 10 | n8n | Mark the `runId` handled in the Data table | Step 9 |

## Connection Setup

No key values in this document. Name the credential and where it is stored.

| Tool | Credential | Where it goes | Secret store |
|---|---|---|---|
| ScraperCity | API key "n8n-hvac-tx", created for this automation only | `Authorization` header as `Bearer` plus the key, through a Header Auth credential on every ScraperCity HTTP Request node | n8n Credentials (encrypted), named "ScraperCity HVAC TX" |
| Smartlead | Smartlead API key | `api_key` query parameter, the only method Smartlead offers; the node pulls it from a credential, and the workflow is set not to save successful executions so URLs with the key are not kept | n8n Credentials |
| GoHighLevel | Private Integration token with `contacts.write` only, on the "Agency Prospects" sub-account | `Authorization` header as `Bearer` plus the token, and `Version` header as shown on the upsert page | n8n Header Auth credential "GHL Agency Prospects" |
| ScraperCity webhook | n8n production webhook URL with a 24-character random path | Pasted at app.scrapercity.com/dashboard/webhooks | ScraperCity dashboard |

## Field Mapping

| ScraperCity field | Destination | Destination field | Transform |
|---|---|---|---|
| `contact_email`, else first of `emails` | Smartlead and GoHighLevel | `email` | Lowercase, trim; Smartlead gets only validator `status` valid |
| `contact_first_name` | Smartlead / GoHighLevel | `first_name` / `firstName` | As is; blank when no named contact (copy does not use the name) |
| `contact_last_name` | Smartlead / GoHighLevel | `last_name` / `lastName` | As is |
| `title` (business name) | Smartlead / GoHighLevel | `company_name` / `companyName` | As is |
| `website` | Smartlead / GoHighLevel | `website` | Bare domain: strip scheme, `www.` and path |
| `phone` | Smartlead / GoHighLevel | `phone_number` / `phone` | E.164, `+1` prefix |
| `city`, `state` | Smartlead | `location` | Joined as "Dallas, TX" |
| `total_score` | Smartlead | `custom_fields.rating` | Text, one decimal |
| `reviews_count` | Smartlead | `custom_fields.reviews` | Text |
| `category_name` | GoHighLevel | custom field "Category" | As is |
| constant | GoHighLevel | `tags`, `source` | `["scrapercity", "hvac-tx-4star"]`, "ScraperCity Local Business Database" |

## Schedule and Triggers

| Item | Value |
|---|---|
| Pull schedule | Weekdays 07:00, Schedule Trigger in the "HVAC TX daily pull" workflow |
| Run-finished signal | ScraperCity webhook to the n8n Webhook node, Respond Immediately, production URL (workflow published) |
| Backstop for missed notifications | A third small workflow every 60 min reads Data table rows older than 30 min and not handled, calls `GET /api/v1/scrape/status/{runId}`, and runs steps 8 to 10 for any `SUCCEEDED` run |
| Time zone | America/Chicago set in the workflow settings |

## Rate Guardrails

| Hop | Vendor limit | Planned rate | Batch size | Source |
|---|---|---|---|---|
| ScraperCity API | 100 requests a minute per key; 10 concurrent scrapes | 5 a minute peak (wallet, 3 pages at 1 per 1,000 ms, 1 validator start) | 100 records per database call | https://scrapercity.com/api-docs |
| GoHighLevel | 100 requests per 10 s; 200,000 a day per app per location | 50 per 10 s (Batching: 5 items per 1,000 ms) | 1 contact per call | https://marketplace.gohighlevel.com/docs/other/rate-limits |
| Smartlead | 10 requests per 2 s | 1 a day | 240 leads in one call (max 400) | https://helpcenter.smartlead.ai/en/articles/125-full-api-documentation |

## Cost Estimate

Prices from `references/scrapercity-catalog.md`. Smartlead, GoHighLevel and n8n are billed on their own plans and are not in this table.

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Local Business Database rows, 22 weekdays x 300 | 6,600 | included in Growth | $0.00 |
| `validate_emails`, one email per business | 6,600 | $0.0072 | $47.52 |
| Test batch before go-live (50 emails) | 50 | $0.0072 | $0.36 |
| Total for the first month | | | $47.88 |

Each weekday run spends 300 x $0.0072 = $2.16. The monthly total of $47.88 was shown to the agency owner and approved before the schedule went live. It leaves about $83 of the current balance for other work.

## Dedupe and Idempotency

| Item | Value |
|---|---|
| Across pulls | `excludeDelivered=true` with the `after` cursor: businesses delivered on earlier days never come back, and each call differs so the 30-second duplicate window never triggers |
| Within a batch | Code node drops repeat emails and repeat domains (franchise locations sharing one inbox) |
| Repeated notifications | The Data table keys on `runId`; a second notification for a handled `runId` stops at step 7 |
| In the destination | GoHighLevel upsert matches on email then phone per the sub-account's duplicate setting; Smartlead `ignore_duplicate_leads_in_other_campaign` stays false so Smartlead skips leads already in another campaign |

## Test Run

| Check | Result |
|---|---|
| `GET /api/v1/wallet` with the new credential | 200, Growth, $131.40 |
| Count with `limit=1` and the full filter set | `pagination.total` 3,960, so about 13 weekdays at 300 before widening to `minRating=3.5` or adding Oklahoma |
| One page with `limit=5` through the Code node | 5 rows, emails lowercased, phones in E.164, domains bare |
| Validator on 50 emails | `SUCCEEDED` in 3 minutes, 40 valid, $0.36 |
| Webhook from that run | Arrived at the production URL, matched the Data table, handled once; a manual re-post was ignored |
| Smartlead load of the 40 valid | 40 added, 0 skipped, merge fields `{{rating}}` and `{{reviews}}` render in the preview |
| GoHighLevel upsert of the 50 | 50 contacts with both tags; no workflow fired because the tag-based workflow was paused for the test |
| 20 records checked in both UIs | 20 of 20 in the right fields |

## Next Steps

1. Publish both n8n workflows and the hourly backstop, then confirm the first 07:00 run in the Executions list.
2. Turn the GoHighLevel tag workflow back on after the first live day looks right.
3. Review after 10 weekdays: `pagination.total` remaining, validator pass rate, Smartlead bounce rate, wallet spend against the $47.88 estimate.
