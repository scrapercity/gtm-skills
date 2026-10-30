# Webhooks and CRM Sync

How sequencer events get back to the CRM, and how ScraperCity run completions feed the import pipeline. Event names were read from each vendor's docs on 2026-10-13. CRM targets named here (HubSpot, Pipedrive, GoHighLevel) are the CRMs scrapercity.com lists as integrations.

## 1. Events to subscribe to

Subscribe only to the events the CRM acts on. Opens are left out: Apple Mail Privacy Protection preloads images and logs opens that never happened.

| Business event | Instantly | Smartlead | Lemlist | EmailBison |
|-|-|-|-|-|
| Prospect replied | `reply_received` | `EMAIL_REPLY` | `emailsReplied` | Contact Replied |
| Out-of-office | `auto_reply_received`, `lead_out_of_office` | Handled by OOO detection settings; no CRM write | n/a | n/a |
| Marked interested | `lead_interested` | `LEAD_CATEGORY_UPDATED` filtered with `category_id_map` to Interested | `emailsInterested`, `interested` | Contact Interested |
| Marked not interested or wrong person | `lead_not_interested`, `lead_wrong_person` | `LEAD_CATEGORY_UPDATED` filtered to Not Interested or Do Not Contact | `emailsNotInterested`, `notInterested` | Tag Attached (if you tag them) |
| Asked for a meeting (a reply label, not a booking) | `lead_meeting_booked` | `LEAD_CATEGORY_UPDATED` filtered to Meeting Request | No webhook event listed (lemcal bookings log as a HubSpot Note) | Tag Attached (if you tag meetings) |
| Unsubscribed | `lead_unsubscribed` | `LEAD_UNSUBSCRIBED` | `entityUnsubscribed`, `variableUnsubscribed` and the older `emailsUnsubscribed` (since 30 Mar 2026 the first two replace it for contact unsubscribes) | Contact Unsubscribed |
| Hard bounce | `email_bounced` | `EMAIL_BOUNCE` | `emailsBounced` | Email Bounced |
| Sending account problem | `account_error` | `EMAIL_ACCOUNT_DISCONNECTED`, set per user (`notify_on_disconnect`), outside campaign webhooks | `connectionIssue`, `sendLimitReached`, `lemwarmPaused` | Email Account Disconnected |
| Reply outside a campaign | n/a | `UNTRACKED_REPLIES` | n/a | Untracked Reply Received |
| Custom reply labels | Arrive as `event_type` equal to the label name; subscribe with `all_events` | Custom categories through `LEAD_CATEGORY_UPDATED` | n/a | n/a |

Instantly webhooks need the Hypergrowth plan or above. ManyReach webhooks are set up under Integrations > CustomWebhook; its event list was not published on the pages checked. Creation calls for Instantly, Smartlead and Lemlist, with scopes and limits: `references/platform-runbooks.md` sections 2c, 3b and 4.

## 2. Event to CRM action

| Event | CRM action (HubSpot calls in section 3) | Sequencer action | Owner |
|-|-|-|-|
| Replied | Upsert contact by email; log the reply as an incoming email engagement; set lead status "Replied" | Sequence stops for that lead (platform default); stop the company (Instantly `stop_for_company`, Smartlead `auto_pause_domain_leads_on_reply`) | Ops automation |
| Interested | Upsert contact; create a deal in the first pipeline stage; assign the mailbox owner. Skip both writes when a native integration already creates the deal (section 3a) | None | Ops automation, rep follows up |
| Not interested, wrong person | Set lead status; no deal; a wrong-person reply naming a colleague becomes a task for the rep | None; the platform stops the lead | Ops automation |
| Asked for a meeting (reply label) | Keep the deal at Positive reply; alert the reply owner to send the booking link | Stop every campaign for that company | Reply owner |
| Meeting booked (calendar booking, section 2a) | Move the deal to "Meeting booked"; set the meeting date | None | Ops automation |
| Meeting held or no-show (meeting outcome, section 2a) | Move the deal to "Meeting held" or "No-show" | None | Rep sets the outcome; automation moves the deal |
| Unsubscribed | Unsubscribe the contact from all email through the communication preferences API; add to the company suppression list | Add to every sequencer's block list the same day | Ops automation |
| Bounced | Set a custom contact property `cold_email_status` to "bounced"; never retry that address | Add to every sequencer's block list | Ops automation |
| Account error | No CRM action; alert the ops channel | Reconnect the mailbox; follow `email-deliverability` R8 | Ops |

### 2a. Pipeline stages come from the calendar, not the reply label

A sequencer's "Meeting Request" or "meeting booked" label records a reply asking for a meeting; nothing has been booked yet. Per-meeting billing and show rates need the booking and the outcome, which live on the calendar.

| Stage | Set by | Source |
|-|-|-|
| Positive reply | Sequencer webhook: Interested or Meeting Request label creates the deal here | Sequencer webhook events (section 1) |
| Meeting booked | The booking itself: a meeting booked through a HubSpot scheduling page (all plans; a new email address creates a contact), read with the meetings API (`/crm/v3/objects/meetings`), or the scheduler's own booking webhook | HubSpot scheduling pages article and meetings API guide, checked 2026-10-13 |
| Meeting held, No-show | The meeting outcome the rep sets after the call: `hs_meeting_outcome` takes scheduled, completed, rescheduled, no show and canceled. Completed moves the deal to Meeting held; no show to No-show; rescheduled keeps Meeting booked | HubSpot meetings API guide, checked 2026-10-13. On Professional or Enterprise, a meeting-based workflow can make the move instead of the middleware (HubSpot knowledge base, checked 2026-10-13) |
| Closed lost | Not interested after a meeting, or the client rejects the meeting | Rep |

In an agency, the client goes on the deal (a single-value deal property), so the pipeline is the billing record per client.

Positive replies: name one owner per client who answers every Interested and Meeting Request reply from the sequencer's master inbox. The middleware posts each such event to the team channel with its timestamp, and the weekly review reports the median time from reply to first answer, so the team sets and tracks its own response target.

Attribution on the contact: write the campaign name and the step that drew the reply (Smartlead `EMAIL_REPLY` carries `campaign_name`, `campaign_id`, `client_id` and `sequence_number`; webhook integration guide, checked 2026-10-13). Name campaigns `{ClientCode}_{Segment}_{ListSource}_{YYYYMM}` so the middleware can split segment and list source out of the name into their own properties.

Weekly reconciliation: export the week's Interested and Meeting Request leads from the sequencer and compare them with the deals created in HubSpot that week. Any lead without a deal is a lost event: replay it from the sequencer (Smartlead's Retrigger Webhooks endpoint) and find the cause.

## 3. CRM write patterns

| CRM | Pattern | Notes |
|-|-|-|
| HubSpot | Batch upsert contacts by email: `POST /crm/objects/2026-09/contacts/batch/upsert`, each input with `idProperty: "email"` and the email as `id` (HubSpot API reference, checked 2026-10-13) | Up to 100 records per batch; partial upserts are not supported when email is the id property. Contacts dedupe on email and companies on Company Domain Name in imports |
| HubSpot, reply as an email engagement | `POST /crm/objects/2026-09/emails` with `hs_timestamp` (required), `hs_email_direction: INCOMING_EMAIL`, `hs_email_subject`, `hs_email_text`, and an association to the contact with `associationTypeId` 198 (`HUBSPOT_DEFINED`) | Sent steps can be logged the same way with `hs_email_direction: EMAIL` and `hs_email_status: SENT`; log replies only unless reps want every step on the timeline |
| HubSpot, opt-out | `POST /communication-preferences/v4/statuses/{email}/unsubscribe-all?channel=EMAIL`, scope `communication_preferences.write` | HubSpot's documented route to unsubscribe a contact from all email. The batch version (`/statuses/batch/unsubscribe-all`) needs Marketing Hub Enterprise, so call the single endpoint per address |
| HubSpot, bounce | Create a custom dropdown property `cold_email_status` (active, replied, bounced, unsubscribed) and set it on the event | Keeps the sequencer's verdict visible to reps and to list filters |
| HubSpot, marketing contact status | Leave contacts the flow creates as non-marketing: "Any integration or API sets contacts as non-marketing by default", and only marketing contacts count toward the contact tier (HubSpot knowledge base, checked 2026-10-13) | Thousands of cold contacts a month cost nothing extra on the HubSpot bill |
| HubSpot limits | Private app: 100 requests per 10 seconds on Free and Starter, 190 on Professional and Enterprise; per account per day 250,000, 625,000 and 1,000,000 | Estimate: each reply or bounce costs 2 to 3 calls, so a 1,000-a-day program stays far below these limits; use batch upserts for backfills |
| Pipedrive | Search person by email, then create or update the person and add a deal | Keep the search-then-write in one workflow step so retries do not create two persons |
| GoHighLevel | Create or update the contact by email, then trigger the workflow that owns the pipeline stage | scrapercity.com lists GoHighLevel workflows for nurture sequences and pipeline stages |

Middleware: Zapier, n8n and Pipedream are all integrations scrapercity.com lists. Any of them can receive the webhook, transform it and call the CRM.

### 3a. Native CRM integration or webhooks: one writer per event

Some sequencers write to HubSpot on their own. Use the native integration for the events it covers, and webhooks for everything else. Never let both write the same event.

What Smartlead's native HubSpot integration does (Smartlead help center, checked 2026-10-13):

| Item | What it does |
|-|-|
| Plan | Smartlead's pricing page names Pro ($94 a month) as the first tier with CRM access, API and webhooks |
| Sent and replied emails | Logged on the HubSpot record as Email activities |
| Opens, clicks, unsubscribes, bounces | Logged as Note activities |
| Deals | Auto-creates a deal at a HubSpot stage you pick, triggered by the lead category you choose (for example "Interested"). It does not move deals between stages afterward |
| Leads | Activity tracking needs the lead to exist in HubSpot; for CSV campaigns, pick a HubSpot list to push the leads to |
| Setup | HubSpot: a property group named "Smartlead" with prefixed properties. Smartlead: Integrations, native integrations, HubSpot, pick the HubSpot instance, choose the deal category and stage, turn on activity tracking |

Split the work like this when Smartlead and HubSpot are both in the plan:

| Event | Writer | Why |
|-|-|-|
| Sent email, reply | Native integration (Email activity) | Covered; a webhook note on top would log the reply twice |
| Lead categorised Interested | Native integration (deal at the chosen stage) | Covered; a webhook "create deal" would make a second deal |
| Meeting booked, held, no-show | The calendar booking and the meeting outcome (section 2a) move the existing deal | The native integration does not move stages, and a reply label is not a booking |
| Unsubscribe | Webhook calls HubSpot's unsubscribe-all endpoint and pushes the address to every other tool's block list. It writes no note | The native integration logs a Note; the help page does not say it changes the contact's subscription status or reaches other tools |
| Hard bounce | Webhook sets `cold_email_status` to bounced and pushes the address to every block list. No note | Same reason |
| Account disconnected | Webhook to the ops alert channel only | Not a CRM event |

The failure to test for: duplicate notes and duplicate deals. Both appear when someone turns on the native integration after the webhook flow already logs replies, or the other way round. Before launch, fire one test reply and one Interested categorisation and count the HubSpot records: one Email activity, one deal, zero extra notes.

Instantly writes to HubSpot only through Automations built on the "New HubSpot" connector (help center, checked 2026-10-13): Instantly triggers such as reply, interest status changed, unsubscribed and bounced, mapped to HubSpot actions such as create or update contact and create note. Nothing writes until you build and switch on a workflow, so the split is yours: either an Automation or the webhook flow owns each event, never both. Deal creation and stage moves are not named Automation actions; keep those in the webhook flow.

Lemlist's HubSpot integration (help center, checked 2026-10-13) syncs two ways per field, logs sent and replied emails as Emails and opens, clicks, bounces and unsubscribes as Notes, and creates deals from per-campaign triggers. Unsubscribes added by hand in lemlist are not pushed, so the webhook flow owns opt-outs.

### 3b. Agencies: one HubSpot portal per client

When each client has its own HubSpot portal (HubSpot calls it an account):

| Rule | How |
|-|-|
| One token per client portal | Create a private app inside each client's portal with scopes `crm.objects.contacts.write`, `crm.objects.deals.write` and `communication_preferences.write`. A private app reads and writes only the account it was created in, needs a super admin, and each account allows up to 20 (HubSpot developer docs, checked 2026-10-13). HubSpot now labels private apps "legacy" but still supports them; rotate each token every six months ("Rotate and expire later" keeps the old one for 7 days). Store tokens in the middleware's credential store, one per client, named by client |
| Alternative for many portals | An app on HubSpot's new developer platform with OAuth and private distribution installs in up to 10 accounts, so one app can serve up to 10 client portals; you host the OAuth flow. Static auth on that platform serves a single account only | Worth it from about 5 client portals; below that, one legacy private app per portal is less work |
| Route by client | The receiver reads the client from the event and picks that client's token: Smartlead client-level webhooks (one per `client_id`, no user-level webhook for the same events, since a user-level one overrides them), Instantly payloads carry `workspace`, and a per-client path or header works for any tool. An event with no known client goes to an error queue, never to a default portal |
| Native integration per client | Smartlead asks you to pick the HubSpot instance when you connect. Whether one Smartlead account can hold a different portal per client is not stated on the help page; confirm in the app before relying on it |
| Optional mirror to the agency portal | For billing and reporting, write a thin record to the agency's own portal: company, client served, meeting booked date, deal stage. Email bodies and reply text stay in the client's portal, which remains the system of record |
| Shared agency portal instead | When clients share the agency's portal, add a "Client" property of type Multiple checkboxes, so one contact can carry several clients without one overwriting another (HubSpot property field types, checked 2026-10-13) |

## 4. Receiver design

| Rule | Why | Source |
|-|-|-|
| Answer 200 at once, then process in the background | Smartlead expects 200 within 30 seconds; its webhooks reference retries after 1 minute, 5 minutes, 15 minutes, 1 hour and 6 hours and disables the webhook after 5 failed attempts, and its integration guide retries after 1, 5 and 30 minutes and then marks the event failed | Smartlead webhooks reference and webhook integration guide, checked 2026-10-13 |
| Make every write idempotent: key on the delivery id (Smartlead `X-Request-Id`) or, where none is sent, event type + lead email + campaign id + timestamp | Retries produce duplicate deliveries | Smartlead webhook integration guide |
| Authenticate the sender | Instantly: a custom header you set on the webhook. Lemlist: the `secret` you set comes back in every payload body. Smartlead: verify `X-Smartlead-Signature` (HMAC SHA256 of the raw body with your signing secret) and keep a long random path segment | Instantly API, Lemlist API, Smartlead webhook integration guide |
| Check webhook health daily | Instantly marks a failing hook `status` -1 (resume it by API); Smartlead's webhooks reference disables a webhook after 5 failed attempts and its integration guide marks failed events; Lemlist disables on 404, 410 or an unresolvable host | Vendor API references |
| Log raw payloads for a retention period you set, longer than any outage you would replay | Replays after an outage | User setting |
| Alert on a silent day | Zero webhook calls on a sending day points at a disabled or broken subscription (see the row above) | Vendor API references |
| Treat unknown event types as data | Instantly sends custom label names as `event_type`; route unknown types to a review queue, never to an error that blocks the flow | Instantly webhook events |

Instantly payloads always include `timestamp`, `event_type`, `workspace`, `campaign_id` and `campaign_name`, plus lead fields such as `lead_email` when available.

## 5. ScraperCity run webhooks into the import pipeline

ScraperCity sends a POST when a run reaches SUCCEEDED or FAILED; register the URL at app.scrapercity.com/dashboard/webhooks. The payload includes `runId`, `fileName` and `leadsCount` (`references/scrapercity-agent-patterns.md`). Apollo runs take hours to several days, so a webhook is the trigger to use for them.

```text
ScraperCity webhook (runId)
  -> GET /api/v1/scrape/status/{runId}          confirm SUCCEEDED (no signature scheme is documented)
  -> GET /api/downloads/{runId}                 CSV, within 48 hours
  -> normalize, dedupe, suppress                 csv-mapping-and-import.md sections 4 to 6
  -> POST /api/v1/scrape/email-validator         validate_emails, $0.00169 per email
  -> poll status, download validated CSV
  -> split files, push valid rows to a PAUSED campaign
  -> notify the owner to review counts and start the campaign
```

Key the pipeline on `runId` so a repeated webhook does not import the same file twice. Never auto-start a campaign from a webhook: a person checks the counts and the preview first.

## 6. Daily database pulls on a schedule

For the Lead Database and Local Business Database there is no run to wait for. A daily job calls the database with the saved filters and `excludeDelivered: true`, pages with `after`, validates the new rows and pushes them. New records count toward the 100,000 a day allowance; records the account already has are free to fetch again.

| Job step | Setting |
|-|-|
| Schedule | On sending days, before the sending window opens |
| Pull size | The ramp's first touches for the day (for example 200) |
| Validation | Every new row |
| Push | Into the running campaign, after the dedupe and suppression checks |
| Report | Rows pulled, valid, pushed, skipped as duplicates, cost |

## 7. Test before relying on it

1. Send the platform's test event where it offers one, or reply to a campaign email from a seed mailbox.
2. Confirm the CRM record changed exactly once.
3. Unsubscribe from a seed and confirm, before the next send, that the address is on every sequencer's block list and that HubSpot shows the contact unsubscribed from all email.
4. Stop the receiver for longer than the first retry interval (Smartlead's first retry comes after 1 minute) during a test send, bring it back, and confirm retries arrive and are de-duplicated.

## Sources

- Instantly, How to use webhooks: https://help.instantly.ai/en/articles/6261906-how-to-use-webhooks
- Instantly, Webhook events: https://developer.instantly.ai/webhook-events
- Smartlead, Webhook events: https://api.smartlead.ai/api-reference/webhooks/events
- Lemlist, Add webhook: https://developer.lemlist.com/api-reference/endpoints/webhooks/add-webhook
- EmailBison, When are webhooks triggered: https://docs.emailbison.com/webhooks/when-are-webhooks-triggered
- ManyReach webhook setup (OttoKit guide): https://ottokit.com/docs/how-to-setup-webhooks-in-manyreach/
- HubSpot, Contacts API guide: https://developers.hubspot.com/docs/api-reference/latest/crm/objects/contacts/guide
- HubSpot, Import objects: https://knowledge.hubspot.com/import-and-export/import-objects
- Smartlead, How to set up the HubSpot integration (checked 2026-10-13): https://helpcenter.smartlead.ai/en/articles/127-how-to-set-up-hubspot-integration-with-smartlead
- Smartlead, Pricing (Pro is the first tier with CRM access, checked 2026-10-13): https://www.smartlead.ai/pricing.md
- Instantly, HubSpot marketplace page (checked 2026-10-13): https://instantly.ai/marketplace/hubspot
- HubSpot, Legacy private apps overview (checked 2026-10-13): https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview
- HubSpot, Property field types (checked 2026-10-13): https://knowledge.hubspot.com/properties/property-field-types-in-hubspot
- HubSpot, Emails API guide (checked 2026-10-13): https://developers.hubspot.com/docs/api-reference/latest/crm/activities/emails/guide
- HubSpot, Communication preferences v4, unsubscribe a contact from all (checked 2026-10-13): https://developers.hubspot.com/docs/api-reference/legacy/communication-preferences/status/unsubscribe-contact
- HubSpot, Communication preferences guide: https://developers.hubspot.com/docs/api-reference/legacy/communication-preferences/guide
- HubSpot, Developer platform authentication (static auth, OAuth, private distribution): https://developers.hubspot.com/docs/apps/developer-platform/build-apps/authentication/overview
- Smartlead, Create webhook: https://api.smartlead.ai/api-reference/webhooks/create
- Smartlead, Webhooks guide (retry schedule): https://api.smartlead.ai/core/webhooks
- Smartlead, Webhook integration guide (retries, `X-Smartlead-Signature`, `X-Request-Id`, payload fields; checked 2026-10-13): https://api.smartlead.ai/guides/webhook-integration
- HubSpot, Meetings API guide (`hs_meeting_outcome` values; checked 2026-10-13): https://developers.hubspot.com/docs/api-reference/crm-meetings-v3/guide
- HubSpot, Create and edit scheduling pages (all plans; checked 2026-10-13): https://knowledge.hubspot.com/meetings-tool/create-and-edit-scheduling-pages
- HubSpot, Create meeting-based workflows (checked 2026-10-13): https://knowledge.hubspot.com/workflows/create-meeting-based-workflows
- HubSpot, Default marketing statuses for created contacts (checked 2026-10-13): https://knowledge.hubspot.com/records/default-marketing-statuses-for-created-contacts
- HubSpot, Marketing contacts (only marketing contacts count toward the tier; checked 2026-10-13): https://knowledge.hubspot.com/records/marketing-contacts
- Instantly, Create webhook: https://developer.instantly.ai/api-reference/webhook/create-webhook
- lemlist, Map lemlist activities to HubSpot: https://help.lemlist.com/en/articles/8735296-map-lemlist-activities-to-hubspot
- ScraperCity, Integrations: https://scrapercity.com/integrations
- ScraperCity agent patterns (webhooks, 48-hour downloads): `references/scrapercity-agent-patterns.md`
- Postmark, Apple Mail Privacy Protection and open tracking: https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
