# Platform Runbooks: Instantly, Smartlead, Lemlist

The exact setup for each sequencer ScraperCity integrates with most often: the screen or API field for every setting, the calls that create campaigns, leads, block list entries and webhooks, the rate limits, the native HubSpot connector, and how each platform separates agency clients. Everything here was read from the vendor's help center or API reference on 2026-10-13. Vendor docs sometimes disagree with themselves; those spots are flagged, and the rule is the same each time: set it in the app, then read the campaign or account back (UI or GET call) and confirm the value stuck.

Plans and prices live in `references/platform-comparison.md`; event-to-CRM mapping lives in `references/webhooks-and-crm-sync.md`. This file is the how-to.

## 1. Settings every cold campaign gets, by platform

Values come from `references/deliverability-primer.md`, which names the source of each number; settings no source fixes are the user's.

| Setting | Value | Instantly (API v2 field) | Smartlead (API v1 field) | Lemlist |
|-|-|-|-|-|
| Cold sends per mailbox per day | Current ramp step from `inbox-setup`, under 50 (Alex Berman) | Account `daily_limit` (`PATCH /api/v2/accounts/{email}`) | Account `max_email_per_day` (`POST /api/v1/email-accounts/{id}`). The API reference says it counts warmup and campaign mail together, so set cold cap plus warmup per day (for example 30 cold + 10 warmup = 40) | lemlist's lemwarm guide: 30 a day at launch with lemwarm cut to 10, 40 after a clean month |
| Minimum gap between sends from one mailbox | Sending window minutes / cap, rounded down (a 540-minute window at 30 a day: 18) | Account `sending_gap` (minutes, 0 to 1440); campaign `email_gap` plus `random_wait_max` | Account `time_to_wait_in_mins`; schedule `min_time_btw_emails` | Not checked on 2026-10-13; read the sending settings screen |
| Campaign caps | Mailboxes x cap; new leads a day = daily sends / steps at steady state | `daily_limit`, `daily_max_leads` | Max new leads per day in the campaign schedule screen (the API pages name it differently; confirm in the UI) | Not checked |
| Schedule | The user's sending days and hours, in the recipient's time zone | `campaign_schedule.schedules[]`: `timing.from` and `timing.to` ("HH:MM"), `days` set true for each sending day, `timezone` | `POST /campaigns/{id}/schedule` with `{"schedule": {"timezone", "days": [1,2,3,4,5], "start_hour", "end_hour", "min_time_btw_emails"}}` | Campaign schedule |
| Plain text | On | `text_only: true` | `send_as_plain_text: true` | Write steps without images or links |
| Open tracking | Off (Apple Mail Privacy Protection fires opens nobody made) | `open_tracking: false` | `track_settings` includes `DONT_TRACK_EMAIL_OPEN` | Turn off in campaign settings |
| Link tracking | Off unless a verified custom tracking domain exists | `link_tracking: false` | `track_settings` includes `DONT_TRACK_LINK_CLICK` | Turn off, or use a custom tracking domain |
| Stop on reply | On | `stop_on_reply: true` | Stop the lead on reply (campaign settings) | Default lead stop on reply; check it |
| Stop the company on reply | On | `stop_for_company: true` | `auto_pause_domain_leads_on_reply: true` | Not checked |
| Out-of-office replies | Do not end the sequence; resume after the return date | `stop_on_auto_reply: false` | `out_of_office_detection_settings`: `ignoreOOOasReply: true`, `autoReactivateOOO: true` | Not checked |
| Unsubscribe | Header on where offered, plus a plain opt-out line in the body | `insert_unsubscribe_header: true` (UI: Campaign Settings > Advanced settings > Sending rules > "Insert unsubscribe link header") | UI: Campaign Settings > Unsubscribe > "Add unsubscribe message in all emails"; API `add_unsubscribe_tag`; body link `%unsubscribe-text%` | Editor: highlight text, + Add > "Add unsubscribe link". Header not stated in the help article |
| Provider matching | On only when the sender pool mixes Google and Microsoft and the validator's `sc_mx_provider` shows both among recipients | `match_lead_esp` | `enable_ai_esp_matching` | n/a |
| Bounce protection | Never relax it | `allow_risky_contacts: false`, `disable_bounce_protect: false` | Campaign SETUP > "High Bounce Rate Auto Protection": enable it and type the bounce-rate percentage (help article 274; the API field `bounce_autopause_threshold` has no documented values, so set it in the UI). Account settings > Warning Notifications takes a webhook URL that receives `campaign_bounce_threshold` when a campaign pauses (help article 210) | lemlist pauses on its own deliverability alerts; watch Berman's 2% line yourself |
| Platform email verification | Off when the file passed `validate_emails` | `verify_leads_on_import: false` | Not used | `verifyEmail=false` on the add-lead call |
| A/B variants | Judge on positive replies per 1,000 sends once each variant reaches the sample size the user sets | Up to 26 variants per step; "Auto optimize A/Z Testing" (Sending rules) off, or set to reply rate, never open rate | Sequence `variants` with `variant_distribution` | Not checked |

## 2. Instantly

### 2a. Workspaces, team and clients

| Fact (Instantly help center, 2026-10-13) | What to do with it |
|-|-|
| Each workspace needs its own subscription, and workspaces can sit on different plans | Cost every client workspace (`references/platform-comparison.md` section 4) |
| Team invitations need Hypergrowth or Light Speed (or a CRM plan) | A Growth workspace cannot take your staff as members; an agency with staff needs Hypergrowth per client workspace |
| Roles: Owner, Admin, Editor, View or VA access (replies in Unibox, edits email account settings) | Staff as Editor; a client who wants to watch replies gets View or VA access in its own workspace only |
| Members with campaign access see every campaign in the workspace; access cannot be limited per campaign | One workspace per client. Never put two clients in one workspace |
| An email account connects to one workspace at a time | Buy and connect each client's mailboxes inside that client's workspace |
| All workspaces sit under one login; switch from the logo menu | Name workspaces after the client so webhook payloads (`workspace`) name the client |

### 2b. Setup order

| Step | Where | Done when |
|-|-|-|
| 1. Create the workspace and subscribe | Logo menu > Create Workspace | Plan shows on the workspace |
| 2. Connect mailboxes by OAuth; set `daily_limit` and `sending_gap`; warmup per `inbox-setup` | Email Accounts | Each account shows warmup on and the ramp cap |
| 3. Tracking domain only if link tracking is on: CNAME host `inst` to `prox.itrackly.com`, DNS-only | Account settings, then "Check Status" | Verified on every account that uses it |
| 4. Load the block list (emails and whole domains) | Settings > Blocklist, or `POST /api/v2/block-lists-entries/bulk-create` with `bl_values` (1 to 1,000 per call) | `valid_count` matches the file; `invalid_count` 0 |
| 5. Create the campaign with section 1 settings and leave it paused | UI, or `POST /api/v2/campaigns` | Read the campaign back; every field matches |
| 6. Add leads | CSV with "Check for Duplicates Across All Campaigns/Lists" on, or `POST /api/v2/leads/add` (below) | Counts reconcile |
| 7. Labels for replies | Lead labels (interest statuses); custom labels arrive in webhooks as `event_type` equal to the label name | Every label maps to a CRM action or to "no write" |
| 8. Webhook | `POST /api/v2/webhooks` (below), Hypergrowth or above | Test delivery returns 200 |
| 9. Start | `POST /api/v2/campaigns/{id}/activate`; pause with the stop endpoint | Sends match the campaign cap on day 1 |

### 2c. API v2 calls

Base `https://api.instantly.ai/api/v2`, header `Authorization: Bearer <key>`. Keys carry scopes; grant only what the job needs (`leads:create`, `block_list_entries:create`, `webhooks:create`, `campaigns:read`). Limits: 100 requests a second and 6,000 a minute per workspace, shared by every key and by API v1, so a second key does not add capacity. 429 means back off; 402 means the workspace has no paid plan.

Bulk add, up to 1,000 leads per call, into a campaign or a list (not both):

```text
POST /api/v2/leads/add
{"campaign_id": "<uuid>", "skip_if_in_workspace": true, "verify_leads_on_import": false,
 "leads": [{"email": "dana@northpaw.example", "first_name": "Dana", "last_name": "Reyes",
            "company_name": "Northpaw", "job_title": "Founder", "website": "northpaw.example",
            "custom_variables": {"AppTrigger": "Klaviyo"}}]}
```

`skip_if_in_workspace` overrides the other two skip flags and skips anyone already in any campaign or list. Extra properties on a lead are rejected, so custom fields go in `custom_variables`. Leave `blocklist_id` out to use the workspace block list. Reconcile every response: `leads_uploaded` plus the skip counters (`in_blocklist`, `skipped_count`, `invalid_email_count`, `duplicate_email_count`, `duplicated_leads`) should account for every row in `total_sent`; chase any gap before the next batch. `created_leads[].index` maps each created lead back to its input row; `remaining_in_plan` warns before the contact limit stops an import.

Webhook:

```text
POST /api/v2/webhooks
{"target_hook_url": "https://hooks.yourco.example/instantly/acme",
 "event_type": "all_events", "campaign": null, "name": "acme to hubspot",
 "headers": {"X-Hook-Token": "<long random value>"}}
```

`all_events` includes custom label events. A webhook object with `status` -1 was disabled after delivery failures (`timestamp_error` says when); fix the receiver, then call "Resume a webhook". A daily job that lists webhooks and alerts on any -1 catches this.

### 2d. HubSpot from Instantly

Instantly has two HubSpot connectors (help center, 2026-10-13): "Old HubSpot" imports HubSpot leads into Instantly; "New HubSpot" exports SuperSearch leads and powers Automations. Automations pair Instantly triggers (interest status changed, unsubscribed, positive or negative label, reply, email bounced, email account error, campaign finished for a lead) with HubSpot actions: create or update contact, create note, create task, create message, send event, create or update record, find contact. Deal creation and stage moves are not named actions, and no plan requirement is stated. Use Automations for contact upserts and notes if you prefer no middleware; keep deals in the webhook flow. Either way, one writer per event (`references/webhooks-and-crm-sync.md` section 3a).

## 3. Smartlead

### 3a. Clients, block lists and webhooks for agencies

| Fact (Smartlead help center and API reference, 2026-10-13) | What to do with it |
|-|-|
| Client workspaces cost $29 a month each from Pro upward; Unlimited Prime includes 3 | Cost workspaces x clients |
| Add a client in the Client Access Dashboard > Add Client: name, company, email, password, permissions, which Master Inbox categories the client sees, email and lead credits. API: `POST /api/v1/client/save` returns the client `id` and its own `api_key` | Give clients limited permissions and hide categories you do not want them working (for example Not Interested) |
| Clients see only the campaigns and email accounts tied to them | Tie each campaign (General Settings, or the campaign's 3-dot menu; API `client_id`) and each mailbox (Email Accounts > account > Management; API `client_id`) to its client |
| A block list entry blocks only when the entry and the campaign share the same client; entries with no client cover campaigns with no client; blocking one address for three clients takes three entries | Load each client's suppression with its `client_id`; load global bounces and complaints once per client plus once with no client |
| Domain entries must be the bare domain (no `www`, no protocol) | Strip before upload |
| Deleting a lead from the Global Block List also deletes that lead's email thread | Never "clean up" the block list; it is history |
| A block applies to sends queued after the entry; mail already queued still goes | Load block lists before leads, never after |
| Webhooks attach at user, client or campaign level; a user-level webhook for an event overrides client and campaign webhooks for the same event | Agencies: one client-level webhook per client and no user-level webhook for those events, so every payload is tied to one client |
| Pro stores up to 30,000 contacts; each unique prospect counts once and sends are a separate counter; Unlimited Smart and Prime have no contact cap (pricing page, as of 28 July 2026) | Sum every client's cumulative contacts, not monthly ones; plan the move to Unlimited Smart before the month the total passes 30,000 |

### 3b. Setup order

| Step | Call or screen | Done when |
|-|-|-|
| 1. Connect mailboxes; set `max_email_per_day`, `time_to_wait_in_mins`, `client_id` | `POST /api/v1/email-accounts/{id}` | Read back each account |
| 2. Warmup | `POST /api/v1/email-accounts/{id}/warmup`: `warmup_enabled`, `total_warmup_per_day` (1 to 50), `daily_rampup` (5 to 20), `reply_rate_percentage` (20 to 100) | Values match the `inbox-setup` plan |
| 3. Block list | Settings > Global Block List, or `POST /api/v1/leads/add-domain-block-list` with `{"domain_block_list": [...], "client_id": 123}` (emails and domains) | Count per client matches the file |
| 4. Campaign | `POST /api/v1/campaigns/create`, then `POST /campaigns/{id}/sequences`, `POST /campaigns/{id}/email-accounts` with `email_account_ids`, `POST /campaigns/{id}/schedule`, `POST /campaigns/{id}/settings` | Campaign shows the client, mailboxes and section 1 settings |
| 5. Leads | `POST /api/v1/campaigns/{id}/leads`, up to 400 per call (send 100), `settings` with `ignore_global_block_list`, `ignore_unsubscribe_list`, `ignore_community_bounce_list` and `ignore_duplicate_leads_in_other_campaign` all false | `added_count` + `skipped_count` = rows sent; read `skipped_leads` |
| 6. Categories | `GET /api/v1/leads/fetch-categories`; defaults include Interested, Meeting Request, Not Interested, Do Not Contact, Information Request | Category ids noted for the webhook filter |
| 7. Webhook | `POST /api/v1/webhook/create` (below) | Test reply arrives once |
| 8. Disconnect alerts | Per-user setting (`notify_on_disconnect.webhookUrl`), separate from campaign webhooks | Alert reaches the ops channel |
| 9. Start | `POST /api/v1/campaigns/{id}/status` with `{"status": "ACTIVE"}`; `"PAUSED"` to pause | Sends begin at the schedule start |

```text
POST https://server.smartlead.ai/api/v1/webhook/create?api_key=$SMARTLEAD_API_KEY
{"name": "acme to hubspot", "webhook_url": "https://hooks.yourco.example/smartlead/acme",
 "association_type": "client", "client_id": 123,
 "event_type_map": {"EMAIL_REPLY": true, "LEAD_CATEGORY_UPDATED": true,
                    "LEAD_UNSUBSCRIBED": true, "EMAIL_BOUNCE": true},
 "category_id_map": {"<Interested id>": true, "<Meeting Request id>": true}}
```

The reference page describes `association_type` as `user`, `client` or `campaign` in one place and as numbers in another; its examples use the strings. `category_id_map` filters only `LEAD_CATEGORY_UPDATED`.

### 3c. API facts and doc conflicts

| Item | Fact |
|-|-|
| Auth | `api_key` query parameter on every call; a client's own key (from client/save) acts inside that client |
| Rate limits | Per key, all endpoints combined: Standard 60 a minute, 1,000 an hour, 10 a second burst; Pro 120 a minute, 3,000 an hour, 20 a second. Three analytics endpoints allow 10 calls a minute each. Plan-limit 429s carry `Retry-After`; throttle to about 80% of the limit |
| Webhook retries | Two Smartlead pages, both checked 2026-10-13. Webhooks reference (api.smartlead.ai/core/webhooks): retries after 1 minute, 5 minutes, 15 minutes, 1 hour and 6 hours, and the webhook is disabled after 5 failed attempts. Webhook integration guide (api.smartlead.ai/guides/webhook-integration): retries after 1, 5 and 30 minutes, then the event is marked failed; return 200 within 30 seconds; a 4xx is not retried; failed events can be resent with the Retrigger Webhooks endpoint. Design for duplicates and check webhook status daily |
| Webhook signing | The integration guide names `X-Smartlead-Signature` (HMAC SHA256 of the raw body with your signing secret, prefixed `sha256=`), `X-Request-Id` (unique per delivery, for dedupe) and `X-Webhook-Level` (user, client or campaign). Verify the signature, dedupe on `X-Request-Id`, and keep a long random path segment as a second check |
| Field names | The campaign-setup guide, the settings reference and the schedule reference name some fields differently (`stop_lead_settings` values, `days` vs `days_of_the_week`, new-lead caps). After any API write, read the campaign back and check the UI |
| Settings changes | Apply to future sends; leads already in progress keep the old settings |

### 3d. HubSpot from Smartlead

Native integration from Pro: sent and replied emails become Email activities, opens, clicks, unsubscribes and bounces become Notes, and a deal is created at a chosen stage when a lead gets a chosen category; it does not move deal stages. Whether one Smartlead account can connect a different HubSpot portal per client is not stated on the help page, so agencies whose clients each have a portal use the webhook flow (`references/webhooks-and-crm-sync.md` sections 3a and 3b).

## 4. Lemlist

| Area | Fact (lemlist help center and API reference, 2026-10-13) | What to do with it |
|-|-|-|
| Plans | Email and Multichannel priced per user; HubSpot, Salesforce and Pipedrive integrations and the API are listed on every plan; lemwarm included | See `references/platform-comparison.md` |
| Unsubscribes | Account-wide: a lead who clicks the link is unsubscribed across the lemlist account; whole domains go in as `@company.com` (Settings > Unsubscribe > Unsubscribe variables) | Same scope as a Smartlead link unsubscribe (across all future campaigns). What lemlist lacks for agencies is client workspaces with their own block lists and webhooks: run one lemlist account per client |
| Unsubscribe API | `POST /api/v2/unsubscribes/variables` with `{"values": [...]}`: emails, `@domain`, phone numbers or LinkedIn URLs, up to 10,000 per call. The old `POST /api/unsubscribes/{email}` is deprecated | Push every other tool's opt-outs here daily |
| Add a lead | `POST /api/campaigns/{campaignId}/leads/` with the email in the body. `deduplicate=true` returns 409 `LEAD_ALREADY_IN_OTHER_CAMPAIGN`; a lead already in this campaign returns 400 `LEAD_ALREADY_IN_CAMPAIGN`; the call never updates. Extra keys become variables, and characters other than letters, digits, `_`, `-`, space and `#` become `_`. Company fields update the shared company record | Send `deduplicate=true` and `verifyEmail=false`; use `updateStrategy=fillEmptyOnly` so an import does not overwrite company data another campaign set |
| Rate limit | 20 requests per 2 seconds per API key; `Retry-After` on every response | Queue calls; at most 10 a second |
| Auth | HTTP Basic, empty user, API key as password; base `https://api.lemlist.com/api` | Key in an environment variable |
| Webhooks | `POST /api/hooks` with `targetUrl`, optional `type` and `secret`; `campaignId` is a query parameter in the spec and a body field in the examples. 200 webhooks per workspace, each URL once. The secret comes back as a `secret` field in every payload body, not a header, and cannot be changed without recreating the hook. A hook is disabled when your endpoint returns 404 or 410 or its host does not resolve | Compare the body `secret` before acting; monitor for disabled hooks |
| Unsubscribe events | Since 30 March 2026 a contact unsubscribe emits `entityUnsubscribed` or `variableUnsubscribed` in place of `emailsUnsubscribed` | Subscribe to all three |
| Warmup | lemlist's lemwarm guide: about 40 days of ramp then 14 days of stabilization, Warmup Score 90 or higher with inbox rate above 90%; below 65 pause and investigate | Stricter than Instantly's 2-week readiness minimum; on lemlist, the lemwarm score is the launch gate |
| Conditions | Yes/No branches on lead data (has email, has LinkedIn URL, custom variable) and actions (opened, clicked, unsubscribed, booked a meeting, accepted invite). A "within" condition needs at least a 1-day delay. The help article ties advanced conditions to "Multichannel Expert or Enterprise", names the current pricing page does not use | Never branch on opens; branch on clicked, accepted invite or booked a meeting. Confirm the plan before relying on conditions |
| HubSpot | Two-way sync with a direction per field (bi-sync, HubSpot priority, lemlist priority, off), usually 2 to 10 minutes; creates contacts after matching by email and companies by domain or name; field mapping is not retroactive; sent and replied emails log as Emails, opens, clicks, bounces and unsubscribes as Notes; deal triggers set per campaign | Map fields before the first import. Unsubscribes you add by hand in lemlist are not pushed to HubSpot, so send those through the webhook flow |

## 5. Agency client checklist (any platform)

Run once per client before its first send.

| Step | Instantly | Smartlead | Done when |
|-|-|-|-|
| Client container | Own workspace, own subscription (Hypergrowth for staff invites and webhooks) | Client in Client Access, `client_id` on every campaign and mailbox | Container named after the client |
| Mailboxes | Bought and connected inside that workspace | Tied to the client under Management | No mailbox serves two clients |
| Suppression | Client's customers, open deals, competitors and own unsubscribes in that workspace's block list | Same, each entry with the client's `client_id` | Count matches the client's export |
| Global suppression | Bounces and complaints pushed to every workspace | One entry per client plus one with no client | Test address blocked in every container |
| Webhook | One webhook per workspace, header token naming the client | One client-level webhook per client, no user-level webhook for the same events | Test reply carries the right client |
| CRM credentials | That client's HubSpot token in the credential store under the client's name (`references/webhooks-and-crm-sync.md` section 3b) | Same | Test reply lands only in that client's portal |
| Client login | View or VA access in the client's own workspace | Limited permissions, chosen Master Inbox categories | Client sees only its own campaigns |

## Sources

- Alex Berman, TAM strategy breakdown (under 50 a day per inbox; checked 2026-10-13): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Alex Berman, cold email templates (bounces under 2%; checked 2026-10-13): https://alexberman.com/cold-email-templates
- Instantly, When your email account is ready for campaigns (2 weeks of warmup; checked 2026-10-13): https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, API v2 leads: https://developer.instantly.ai/api/v2/lead
- Instantly, Add leads in bulk: https://developer.instantly.ai/api-reference/lead/add-leads-in-bulk-to-a-campaign-or-list
- Instantly, Create campaign: https://developer.instantly.ai/api-reference/campaign/create-campaign
- Instantly, Patch account: https://developer.instantly.ai/api-reference/account/patch-account
- Instantly, Create webhook: https://developer.instantly.ai/api-reference/webhook/create-webhook
- Instantly, Bulk create block list entries: https://developer.instantly.ai/api-reference/blocklistentry/bulk-create-block-list-entry
- Instantly, Rate limit: https://developer.instantly.ai/getting-started/rate-limit
- Instantly, Webhook events: https://developer.instantly.ai/webhook-events
- Instantly, A/Z testing: https://help.instantly.ai/en/articles/6661549-a-z-testing
- Instantly, Separate workspaces and team members: https://help.instantly.ai/en/articles/6718773-create-a-separate-workspace-and-invite-team-members
- Instantly, How to use webhooks: https://help.instantly.ai/en/articles/6261906-how-to-use-webhooks
- Instantly, How to connect HubSpot: https://help.instantly.ai/articles/8848886-how-to-connect-hubspot-to-instantly
- Instantly, HubSpot integration in Automations: https://help.instantly.ai/en/articles/13342530-hubspot-integration-in-automations
- Instantly, Custom tracking domain: https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- Smartlead, Pricing (Markdown, as of 28 July 2026): https://www.smartlead.ai/pricing.md
- Smartlead, Rate limits: https://api.smartlead.ai/guides/rate-limits
- Smartlead, Campaign setup guide: https://api.smartlead.ai/guides/campaign-setup
- Smartlead, Update campaign settings: https://api.smartlead.ai/api-reference/campaigns/update-settings
- Smartlead, Update campaign schedule: https://api.smartlead.ai/api-reference/campaigns/update-schedule
- Smartlead, Add leads to a campaign: https://api.smartlead.ai/reference/add-leads-to-a-campaign-by-id
- Smartlead, Update email account: https://api.smartlead.ai/api-reference/email-accounts/update
- Smartlead, Warmup settings: https://api.smartlead.ai/api-reference/email-accounts/warmup-settings
- Smartlead, Domain block list: https://api.smartlead.ai/api-reference/utilities/domain-block-list
- Smartlead, Create client: https://api.smartlead.ai/api-reference/clients/create
- Smartlead, Create webhook: https://api.smartlead.ai/api-reference/webhooks/create
- Smartlead, Webhook events: https://api.smartlead.ai/api-reference/webhooks/events
- Smartlead, Webhooks guide: https://api.smartlead.ai/core/webhooks
- Smartlead, Webhook integration guide (retries, signature and request id headers; checked 2026-10-13): https://api.smartlead.ai/guides/webhook-integration
- Smartlead, High bounce rate auto protection (checked 2026-10-13): https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- Smartlead, Bounce autopause and webhook (checked 2026-10-13): https://helpcenter.smartlead.ai/en/articles/210-bounce-autopause-and-webhook
- Smartlead, How unsubscribing works (link unsubscribe across all future campaigns; checked 2026-10-13): https://helpcenter.smartlead.ai/en/articles/27-how-does-unsubscribing-work-in-smartlead-manage-unsubscribed-leads-effectively
- Smartlead, Leads and categories: https://api.smartlead.ai/core/leads
- Smartlead, How to add a new client: https://helpcenter.smartlead.ai/en/articles/25-how-to-add-a-new-client-in-smartlead
- Smartlead, Agency view and client access: https://helpcenter.smartlead.ai/en/articles/92-agency-view-and-client-access
- Smartlead, Why are blocked leads still receiving emails: https://helpcenter.smartlead.ai/en/articles/410-why-are-blocked-leads-still-receiving-emails
- Smartlead, HubSpot integration: https://helpcenter.smartlead.ai/en/articles/127-how-to-set-up-hubspot-integration-with-smartlead
- lemlist, Pricing: https://www.lemlist.com/pricing
- lemlist, Create lead in campaign: https://developer.lemlist.com/api-reference/endpoints/leads/create-lead-in-campaign
- lemlist, Rate limits: https://developer.lemlist.com/api-reference/getting-started/rate-limits
- lemlist, Bulk unsubscribe variables: https://developer.lemlist.com/api-reference/endpoints/unsubscribes/bulk-unsubscribe-variables
- lemlist, Add unsubscribe email or domain (deprecated): https://developer.lemlist.com/api-reference/endpoints/unsubscribes/add-unsubscribe-email-or-domain
- lemlist, Add webhook: https://developer.lemlist.com/api-reference/endpoints/webhooks/add-webhook
- lemlist, Add and manage unsubscribe links: https://help.lemlist.com/en/articles/4452779-how-to-add-and-manage-unsubscribe-links
- lemlist, Set up and use lemwarm: https://help.lemlist.com/en/articles/14653207-how-to-set-up-and-use-lemwarm
- lemlist, Conditions in a campaign sequence: https://help.lemlist.com/en/articles/8290177-how-to-use-conditions-in-your-campaign-sequence
- lemlist, New HubSpot integration: https://help.lemlist.com/en/articles/10308771-new-hubspot-integration
- lemlist, Map lemlist activities to HubSpot: https://help.lemlist.com/en/articles/8735296-map-lemlist-activities-to-hubspot
