# Webhooks and CRM Sync

How sequencer events get back to the CRM, and how ScraperCity run completions feed the import pipeline. Event names were read from each vendor's docs on 2026-10-13. CRM targets named here (HubSpot, Pipedrive, GoHighLevel) are the CRMs scrapercity.com lists as integrations.

## 1. Events to subscribe to

Subscribe only to the events the CRM acts on. Opens are left out: Apple Mail Privacy Protection preloads images and logs opens that never happened.

| Business event | Instantly | Smartlead | Lemlist | EmailBison |
|-|-|-|-|-|
| Prospect replied | `reply_received` (and `auto_reply_received` for out-of-office) | `EMAIL_REPLY` | `emailsReplied` | Contact Replied |
| Marked interested | `lead_interested` | `LEAD_CATEGORY_UPDATED` (filter by category) | `emailsInterested`, `interested` | Contact Interested |
| Meeting booked | `lead_meeting_booked` | `LEAD_CATEGORY_UPDATED` | Not a separate email event | Tag Attached (if you tag meetings) |
| Unsubscribed | `lead_unsubscribed` | `LEAD_UNSUBSCRIBED` | `entityUnsubscribed`, `variableUnsubscribed` (since 30 Mar 2026) | Contact Unsubscribed |
| Hard bounce | `email_bounced` | `EMAIL_BOUNCE` | `emailsBounced` | Email Bounced |
| Sending account problem | `account_error` | `EMAIL_ACCOUNT_DISCONNECTED` (configured per user) | `connectionIssue`, `sendLimitReached` | Email Account Disconnected |
| Reply outside a campaign | n/a | `UNTRACKED_REPLIES` | n/a | Untracked Reply Received |

ManyReach webhooks are set up under Integrations > CustomWebhook; its event list is chosen in that screen and was not published on the pages checked. Instantly webhooks need the Hypergrowth plan or above.

## 2. Event to CRM action

| Event | CRM action | Sequencer action | Owner |
|-|-|-|-|
| Replied | Upsert contact by email; log the reply as an activity; set lead status "Replied" | Sequence stops for that lead (platform default); check company-level stop | Ops automation |
| Interested | Upsert contact; create a deal in the first pipeline stage; assign the mailbox owner | None | Ops automation, rep follows up |
| Meeting booked | Move the deal to "Meeting booked"; set the meeting date | Stop every campaign for that company | Rep |
| Unsubscribed | Set the CRM email opt-out property; add to the company suppression list | Add to every sequencer's block list within 24 hours | Ops automation |
| Bounced | Mark the email invalid in the CRM | Add to every sequencer's block list | Ops automation |
| Account error | No CRM action; alert the ops channel | Reconnect the mailbox; follow `email-deliverability` R8 | Ops |

## 3. CRM write patterns

| CRM | Pattern | Notes |
|-|-|-|
| HubSpot | Batch upsert contacts by email: `POST /crm/objects/2026-09/contacts/batch/upsert` with each input carrying `idProperty: "email"` and the email as `id` (HubSpot API reference, checked 2026-10-13) | Up to 100 records per batch; partial upserts are not supported when email is the id property. Contacts dedupe on email and companies on Company Domain Name in imports |
| Pipedrive | Search person by email, then create or update the person and add a deal | Keep the search-then-write in one workflow step so retries do not create two persons |
| GoHighLevel | Create or update the contact by email, then trigger the workflow that owns the pipeline stage | scrapercity.com lists GoHighLevel workflows for nurture sequences and pipeline stages |

Middleware: Zapier, n8n and Pipedream are all integrations scrapercity.com lists. Any of them can receive the webhook, transform it and call the CRM.

## 4. Receiver design

| Rule | Why | Source |
|-|-|-|
| Answer 200 within a few seconds, then process in the background | Smartlead retries when your server does not return 200 in time | Smartlead webhook docs |
| Make every write idempotent: key on event type + lead email + timestamp or event id | Retries produce duplicate deliveries | Smartlead webhook docs |
| Authenticate the sender | Instantly lets you add custom HTTP headers to the webhook; Lemlist's add-webhook call accepts a `secret`; for others, use an unguessable URL path and check the payload against the platform API before acting on it | Instantly help, Lemlist API reference |
| Log raw payloads for 30 days | Replays after an outage | House standard |
| Alert on a silent day | Zero webhook calls on a sending day usually means a broken subscription | House standard |

Instantly payloads always include `timestamp`, `event_type`, `workspace`, `campaign_id` and `campaign_name`, plus lead fields such as `lead_email` when available.

## 5. ScraperCity run webhooks into the import pipeline

ScraperCity sends a POST when a run reaches SUCCEEDED or FAILED; register the URL at app.scrapercity.com/dashboard/webhooks. The payload includes `runId`, `fileName` and `leadsCount` (`references/scrapercity-agent-patterns.md`). Apollo runs take hours to several days, so a webhook is the trigger to use for them.

```text
ScraperCity webhook (runId)
  -> GET /api/v1/scrape/status/{runId}          confirm SUCCEEDED (no signature scheme is documented)
  -> GET /api/downloads/{runId}                 CSV, within 48 hours
  -> normalize, dedupe, suppress                 csv-mapping-and-import.md sections 4 to 6
  -> POST /api/v1/scrape/email-validator         validate_emails, $0.0072 per email
  -> poll status, download validated CSV
  -> split files, push valid rows to a PAUSED campaign
  -> notify the owner to review counts and start the campaign
```

Key the pipeline on `runId` so a repeated webhook does not import the same file twice. Never auto-start a campaign from a webhook: a person checks the counts and the preview first.

## 6. Daily database pulls on a schedule

For the Lead Database and Local Business Database there is no run to wait for. A daily job calls the database with the saved filters and `excludeDelivered: true`, pages with `after`, validates the new rows and pushes them. New records count toward the 100,000 a day allowance; records the account already has are free to fetch again.

| Job step | Setting |
|-|-|
| Schedule | Weekdays, 06:00 in the sending time zone |
| Pull size | The ramp's first touches for the day (for example 200) |
| Validation | Every new row |
| Push | Into the running campaign, after the dedupe and suppression checks |
| Report | Rows pulled, valid, pushed, skipped as duplicates, cost |

## 7. Test before relying on it

1. Send the platform's test event where it offers one, or reply to a campaign email from a seed mailbox.
2. Confirm the CRM record changed once, not twice.
3. Unsubscribe from a seed and confirm the address lands on every sequencer's block list and the CRM opt-out property within the hour.
4. Kill the receiver for 10 minutes during a test send, bring it back, and confirm retries arrive and are de-duplicated.

## Sources

- Instantly, How to use webhooks: https://help.instantly.ai/en/articles/6261906-how-to-use-webhooks
- Instantly, Webhook events: https://developer.instantly.ai/webhook-events
- Smartlead, Webhook events: https://api.smartlead.ai/api-reference/webhooks/events
- Lemlist, Add webhook: https://developer.lemlist.com/api-reference/endpoints/webhooks/add-webhook
- EmailBison, When are webhooks triggered: https://docs.emailbison.com/webhooks/when-are-webhooks-triggered
- ManyReach webhook setup (OttoKit guide): https://ottokit.com/docs/how-to-setup-webhooks-in-manyreach/
- HubSpot, Contacts API guide: https://developers.hubspot.com/docs/api-reference/latest/crm/objects/contacts/guide
- HubSpot, Import objects: https://knowledge.hubspot.com/import-and-export/import-objects
- ScraperCity, Integrations: https://scrapercity.com/integrations
- ScraperCity agent patterns (webhooks, 48-hour downloads): `references/scrapercity-agent-patterns.md`
- Postmark, Apple Mail Privacy Protection and open tracking: https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
