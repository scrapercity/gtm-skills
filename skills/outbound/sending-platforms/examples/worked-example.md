# Sending Platform Plan: Kestrel Studio

Illustrative example: Kestrel Studio and every domain below are invented. Prepared 2026-10-13 for Kestrel Studio, which builds Klaviyo email flows for Shopify apparel brands. Vendor pages checked 2026-10-13. Nothing is assumed: Kestrel's founder answered every question on 2026-10-09.

## Summary

Use Instantly Hypergrowth at $97 a month on monthly billing. It covers the 1,587 contacts Kestrel will upload this month (over the Growth plan's 1,000) and is the first Instantly plan with webhooks, which feed HubSpot through n8n, and it passed Kestrel's 26-day trial. ScraperCity Store Leads and the Lead Database supply Shopify apparel stores using Klaviyo and the people who run them, validated before upload. Kestrel's 12 warmed mailboxes move over from Woodpecker. The first month costs $368.41 all-in, inside the $400 ceiling.

## Assumptions and Open Questions

| Question | Answer | Answered by user or assumed |
|-|-|-|
| HubSpot portals: one, or one per client | One portal, Kestrel's own | Answered |
| Client logins needed | None; this is Kestrel's own outbound | Answered |
| Inbox mix (Google, Microsoft, other) | 12 existing Google Workspace mailboxes on 4 domains, sending from Woodpecker today; 0 Microsoft | Answered |
| Current sending tool | Woodpecker, usage-based plan paid through 2026-10-31 | Answered |
| Monthly budget ceiling, all-in | $400 a month | Answered |

## Requirements

| Input | Value | Source |
|-|-|-|
| New prospects per day | 76 (1,587 over 21 sending days) | This plan |
| Steps per sequence | 3 | Kestrel's campaign plan |
| Contacts per month (month 1 and month 2) | 1,587 and about 1,600 | Store Leads count and next month's pull |
| Sends per month (month 1 and month 2) | 4,761 (1,587 x 3) and about 4,800 | Contacts x steps |
| Mailboxes connected | 12 on 4 domains, warmed, cap 30 | Kestrel's inbox roster |
| Seats and workspaces | 2 users (Mara Lind, founder; Theo Ruiz, ops), 1 workspace | Kestrel |
| Client workspaces | 0 (in-house outbound) | Kestrel |
| CRM and middleware | HubSpot (existing), n8n self-hosted (existing server) | Kestrel |

## Platform Decision

| Option | Plan and price | Fits because | Gaps | Checked |
|-|-|-|-|-|
| Instantly | Hypergrowth, $97 a month: 25,000 contacts, 125,000 emails, unlimited mailboxes and warmup | Covers month 2 with room; webhooks available on Hypergrowth or above; duplicate check across campaigns on by default; blocklist for emails and domains; unsubscribe header setting; ScraperCity integration page | API adds one lead per call | 2026-10-13 |
| Instantly | Growth, $47 a month: 1,000 contacts, 5,000 emails | Price | 1,587 contacts is over the limit; no webhooks below Hypergrowth | 2026-10-13 |
| Smartlead | Pro, $94 a month: 30,000 contacts, 90,000 emails; CRM access, API and webhooks from Pro | Native HubSpot integration logs replies and creates deals; client workspaces at $29 each if Kestrel later runs client campaigns; API up to 400 leads per request | Not trialled on Kestrel's domains; the 26-day trial ran on Instantly | 2026-10-13 |
| Lemlist | Email, $69 a month: 50,000 emails, unlimited senders, lemwarm | Variables from any extra field | Multichannel not needed; webhook plan availability not stated | 2026-10-13 |
| ManyReach | Business, $79 a month: 150,000 credits, 1 private IP | Credit model, private IP | Webhook event list not published on the pages checked | 2026-10-13 |
| EmailBison | Base, $599 a month: 500,000 sends, dedicated IPs | Built for high volume | Six times the volume needed, over budget | 2026-10-13 |
| HubSpot sequences | Needs Sales Hub Professional or Enterprise seats | Native CRM | No warmup; Kestrel's HubSpot has no Sales Hub Professional seats | 2026-10-13 |

Decision: Instantly Hypergrowth, monthly billing until the campaign proves out, then yearly ($77.60 a month). On monthly billing Instantly Hypergrowth ($97) costs $3 more than Smartlead Pro ($94); Kestrel pays the difference to keep the platform its trial already proved.

Revisit if: Kestrel signs its first client campaign (Smartlead's $29 client workspaces then cost less than a second Instantly subscription), or uploaded contacts pass 20,000 of Hypergrowth's 25,000.

## Workspace Settings

| Setting | Value | Source |
|-|-|-|
| Daily limit per mailbox | 30 from 2026-10-24; 20 during the Woodpecker overlap 2026-10-14 to 2026-10-23, while Woodpecker keeps 10 | Inbox ramp plan, steady row; under Alex Berman's 50 a day; cap split during the migration |
| Gap between emails | 15 minutes per mailbox (`sending_gap`) plus a random wait up to 5, so 15 to 20 minutes | 540-minute window / 30 sends = 18 on average |
| Campaign daily limit | People 240, Store inbox 84, Catch-all 36 (Kestrel's own 10% setting, of 360); during the overlap 160, 56 and 24 (240 in total) | 12 mailboxes x 30 = 360; 12 x 20 = 240 during the overlap |
| Schedule | Monday to Friday, 08:00 to 17:00; two schedules, America/New_York and America/Denver, split by store state | Inbox ramp plan sending rules |
| Plain text | On (`text_only`) | No images or tracked links in cold steps |
| Open tracking | Off | Apple Mail Privacy Protection inflates opens |
| Link tracking | Off; no links in touch 1 | Copy brief |
| Unsubscribe header | On: Settings, Advanced settings, Sending rules, "Insert unsubscribe link header"; confirmed `List-Unsubscribe` in a raw test message | Instantly help, checked 2026-10-13 |
| Stop on reply | On for the lead and for its store (`stop_for_company`), so the second contact at a store that replied gets nothing more | Instantly campaign settings, checked |
| Out-of-office replies | Do not stop the sequence (`stop_on_auto_reply` off) | An out-of-office is not an answer |
| Bounce auto-pause | On at Instantly's default, 5% after 200 sends; Theo pauses a campaign by hand above 2% over its last 200 sends | Instantly help center; Alex Berman: hard bounces under 2% |
| Verify Leads on upload | Off; file already validated with the ScraperCity Email Validator | Avoids 0.25 credits per lead on top |

## Column Map

Headers are renamed in the file before upload. Instantly column names stay at 20 characters or fewer and each upload carries at most 12 columns (7 custom variables), under the 50-variable limit.

| Source | Source column | Platform variable | Merge tag | Fallback |
|-|-|-|-|-|
| Lead Database | `email` | Email (predefined) | none | Required; rows without one are dropped |
| Lead Database | `first_name` | First Name (predefined) | `{{firstName}}` | "there" (4 rows) |
| Lead Database | `last_name` | Last Name (predefined) | `{{lastName}}` | Not used in copy |
| Lead Database | `company_name` | Company Name (predefined) | `{{companyName}}` | Store name from Store Leads |
| Lead Database | `company_domain` | Website (predefined) | `{{website}}` | Store domain from Store Leads |
| Lead Database | `title` | TitleShort (custom) | `{{TitleShort}}` | "your role" |
| Lead Database | `linkedin_url` | Linkedin (custom) | none | Not used in copy |
| Store Leads | Store name | Company Name, store inbox campaign | `{{companyName}}` | "your store" |
| Store Leads | Store email | Email, store inbox campaign | none | Required |
| Store Leads | Apps | AppTrigger (custom) | `{{AppTrigger}}` | "Klaviyo" (every row passed the `apps` filter) |
| Store Leads | Category | Category (custom) | `{{Category}}` | "apparel" |
| Store Leads | Estimated monthly visits | VisitsBand (custom) | `{{VisitsBand}}` | "20k to 200k" |
| Email Validator | `email_quality` | EmailQuality (custom) | none | Send order only |
| Email Validator | `sc_mx_provider` | MxProvider (custom) | none | "other" for reporting |

## Import Procedure

| Step | Action | Owner | Due | Result |
|-|-|-|-|-|
| 1 | ScraperCity dashboard: wallet balance $212.40 on the Growth plan | Mara Lind | 2026-10-12 | Approved spend of $17.92 |
| 2 | Store Leads test run: `POST https://app.scrapercity.com/api/v1/scrape/store-leads` with platform shopify, category apparel, apps Klaviyo, country US, 20,000 to 200,000 visits, `totalLeads` 100, `offset` 0 | Theo Ruiz | 2026-10-12 | 100 stores, $0.39; filters confirmed on 10 sampled rows |
| 3 | Same call for the remaining 1,400, `offset` 100 to 1,400 in steps of 100 | Theo Ruiz | 2026-10-12 | 1,500 stores in total, $5.85 including the test |
| 4 | Suppress 14 HubSpot customer domains | Theo Ruiz | 2026-10-12 | 1,486 stores |
| 5 | Lead Database: `GET https://app.scrapercity.com/api/v1/database/leads` with the store domains in 15 batches of up to 100, founder and ecommerce titles, people with an email, `excludeDelivered=true` | Theo Ruiz | 2026-10-12 | 1,236 people at 990 stores; capped at 2 per domain: 1,180 kept |
| 6 | Store inbox file for the 496 stores with no person | Theo Ruiz | 2026-10-12 | 496 rows, all role addresses, own campaign |
| 7 | Dedupe on lowercased email across both files and against the Instantly workspace | Theo Ruiz | 2026-10-13 | 0 duplicates (new workspace) |
| 8 | ScraperCity Email Validator (`POST https://app.scrapercity.com/api/v1/scrape/email-validator`) on 1,676 addresses | Theo Ruiz | 2026-10-13 | People: 1,002 valid, 121 catch-all, 19 unknown, 36 invalid, 2 disposable. Store inboxes: 401 valid, 63 catch-all, 9 unknown, 22 invalid, 1 disposable. $12.07 |
| 9 | Split: People (1,002), Store inbox (401), Catch-all (184), Hold unknown (28), Suppress (61) | Theo Ruiz | 2026-10-13 | 1,587 rows to upload |
| 10 | Upload three CSVs into paused campaigns, "Check for Duplicates Across All Campaigns/Lists" on | Theo Ruiz | 2026-10-13 | Instantly reported 0 existing, 0 invalid, 0 blocklisted; 1,587 imported |
| 11 | Preview 10 renders per campaign, including 2 with fallbacks | Mara Lind | 2026-10-13 | Renders show neither raw `{{` nor "Hi ," |
| 12 | Start the campaigns at the limits above | Mara Lind | 2026-10-14 | Sends logged at 160, 56 and 24 on day 1 (overlap caps) |

## Suppression and Dedupe

| List | Match on | Where it lives | Sync |
|-|-|-|-|
| Customers | Domain (14) | Instantly Blocklist, HubSpot lifecycle stage "Customer" | Re-exported from HubSpot before each import |
| Past unsubscribes from Woodpecker | Email (37) | Instantly Blocklist | Loaded once on 2026-10-13 from the Woodpecker blacklist export |
| Every Woodpecker prospect (2,140, any status) | Email | Instantly list "woodpecker-history", never enrolled, so the cross-campaign duplicate check skips them | Loaded 2026-10-12; 0 matches with this pull, since Woodpecker campaigns targeted Shopify beauty brands |
| Competitor agencies | Domain (22) | Instantly Blocklist | Kept by the founder |
| New unsubscribes and "remove me" replies | Email, or domain if asked | Instantly Blocklist and HubSpot "unsubscribed from all email" | n8n flow on `lead_unsubscribed` plus same-day manual add for reply opt-outs |
| Hard bounces | Email | Instantly Blocklist | n8n flow on `email_bounced` |
| Already pulled from ScraperCity | Lead Database records | Every database call asks for new records only | Automatic |

## Webhooks to CRM

One Instantly webhook (all campaigns) posts to n8n with a custom header `X-Kestrel-Token`; n8n answers 200 at once, then writes to HubSpot with a batch upsert keyed on email. Contacts it creates stay non-marketing, HubSpot's default for API-created contacts, so they do not raise the contact tier. The pipeline "Outbound" has Positive reply, Meeting booked, Meeting held, No-show and Closed lost.

Writer per event: the n8n webhook flow is the only writer to HubSpot. Instantly's HubSpot marketplace page (checked 2026-10-13) describes importing HubSpot lists and syncing outcomes, and lists logging sends and replies through third-party webhook tools, so Instantly's own HubSpot connector stays off. Two writers would log every reply twice.

| Business event | Platform event | Writer | CRM action | Sequencer action |
|-|-|-|-|-|
| Replied | `reply_received` | n8n webhook flow | Upsert contact by email; log the reply as an incoming email engagement associated to the contact; lead status "Replied" | Stops for that lead (default); rep removes the second contact at the same store by hand |
| Interested or asked for a meeting | `lead_interested`, `lead_meeting_booked` (a reply label) | n8n webhook flow | Create a deal at Positive reply, owner Mara Lind; skip if one is open | Remove other contacts at the domain from all campaigns |
| Meeting booked | Booking on Mara's HubSpot scheduling page, read by n8n from the meetings API | n8n flow | Move the deal to Meeting booked with the meeting date | None |
| Meeting held or No-show | Meeting outcome Mara sets after the call (`hs_meeting_outcome` completed or no show) | n8n flow | Move the deal to Meeting held or No-show | None |
| Unsubscribed | `lead_unsubscribed` | n8n webhook flow | Unsubscribe the contact from all HubSpot email through the communication preferences API | Add email to the Instantly Blocklist (already unsubscribed in Instantly; the flow keeps HubSpot in step) |
| Bounced | `email_bounced` | n8n webhook flow | Set the contact's `cold_email_status` property to bounced | Add to the Instantly Blocklist |
| Account error | `account_error` | n8n webhook flow | None | Slack alert to ops; reconnect the mailbox |

Positive replies: Mara Lind answers every Interested reply from the Instantly Unibox with her booking link. n8n posts each one to Slack with its reply time, and the Friday review reports the median reply-to-answer time.

## Test Plan

| Test | Pass when | Owner | Due | Result |
|-|-|-|-|-|
| Seed send from 4 mailboxes (one per domain) | Inbox at Gmail, Workspace, Outlook.com and Microsoft 365 seeds | Theo Ruiz | 2026-10-13 | Pass |
| Render preview with an empty `first_name` row | Reads "Hi there," with no raw tags | Mara Lind | 2026-10-13 | Pass |
| Test reply from a seed | HubSpot contact created once, one incoming email logged (no duplicate from a second writer), status "Replied" | Theo Ruiz | 2026-10-13 | Pass, one record, one email |
| Test unsubscribe from a seed | Instantly Blocklist and HubSpot "unsubscribed from all email" within 1 hour | Theo Ruiz | 2026-10-13 | Pass, 3 minutes |
| Receiver stopped for 10 minutes during a test reply | Gap visible in the n8n execution log; status reconciled from Instantly lead status the same day | Theo Ruiz | 2026-10-13 | Pass |
| Raw headers of a test message | `List-Unsubscribe` present; `dkim=pass` for the sending domain | Theo Ruiz | 2026-10-13 | Pass |
| Webhook health | Daily n8n job lists Instantly webhooks and alerts on any with status -1 | Theo Ruiz | 2026-10-14 | Scheduled |
| Weekly reconciliation | Every lead Instantly marks Interested that week has a deal in HubSpot; gaps replayed and explained | Theo Ruiz | 2026-10-23 | Scheduled |

## Migration Plan

Old tool: Woodpecker (usage-based plan, paid through 2026-10-31), 12 mailboxes on 4 domains, 318 prospects mid-sequence on 2026-10-12.

| Step | Action | Date | Done when |
|-|-|-|-|
| Pre-commitment trial | Test domain kestrelhq.example (a new reserve) with 3 mailboxes connected only to Instantly Hypergrowth, monthly billing; warmup 14 days; seed tests from Instantly on 2026-10-02 and 2026-10-06; 100-row import and webhook tests | 2026-09-14 to 2026-10-09 | Health score 96% on day 14; inbox at 5 of 5 seed providers on both tests; 100 rows reconciled; test reply, unsubscribe and bounce each reached HubSpot once. Decision to migrate 2026-10-09 |
| Export from old tool | Woodpecker prospects by status (2,140 rows, 318 Active), blacklist (37 emails), campaign stats; sequences copied by hand since Woodpecker does not export them | 2026-10-12 | Row counts logged; 37 unsubscribes in the Instantly Blocklist; 2,140 in the history list |
| Mid-sequence prospects finish on old tool | No new prospects in Woodpecker from 2026-10-14; the 318 Active prospects finish their remaining steps there, at 10 a day per mailbox | 2026-10-14 to 2026-10-23 | Woodpecker shows 0 Active prospects |
| Rebuild sequences | Three Instantly campaigns rebuilt from the copied steps, merge tags translated to `{{firstName}}` and the custom variables in the Column Map, schedules and limits re-entered, campaigns left paused | 2026-10-12 to 2026-10-13 | 10 previews per campaign render clean |
| Reconnect the same mailboxes | The same 12 Google Workspace mailboxes connected to Instantly by OAuth; Instantly warmup on and Woodpecker warmup off the same day; no new mailboxes created | 2026-10-13 | 12 accounts connected in Instantly; caps split 20 Instantly and 10 Woodpecker per mailbox |
| Re-point tracking CNAME | Instantly host `inst` CNAME to `prox.itrackly.com` added DNS-only on the 4 domains and verified (link tracking stays off for now); the Woodpecker tracking host is removed on the cut-off date Kestrel set, 30 days after its last send | 2026-10-13; removal 2026-11-23 | "Check Status" shows verified on all 12 accounts; old host deleted |
| Parallel run | Instantly ramps at the split cap while Woodpecker finishes; daily comparison of hard bounces per mailbox, positive replies per 1,000 sends and a seed test on 2026-10-20 | 2026-10-14 to 2026-10-23 | Instantly bounces under 2% over 200 sends and inbox at every seed provider; otherwise new prospects go back to Woodpecker |
| Decommission old tool | Final Woodpecker export merged into the Instantly Blocklist and HubSpot; integrations off; OAuth grants revoked in each Google account; plan cancelled at the 2026-10-31 billing date; archive kept to 2027-10-31 | 2026-10-26 | Woodpecker shows 0 active prospects, final export merged, integrations off, OAuth revoked, cancellation confirmed |

## Cost

Full monthly cost for the first month. Mailbox price from Google's Workspace billing help (Business Starter, Flexible plan); domain price from porkbun.com; both checked 2026-10-13.

| Line | Count | Unit price | Monthly |
|-|-|-|-|
| Sequencer: Instantly Hypergrowth | 1 workspace | $97 a month | $97.00 |
| Client workspaces | 0 (in-house) | n/a | $0.00 |
| Mailboxes: Google Workspace Business Starter, existing, reconnected | 12 | $8.40 a month | $100.80 |
| Domains: `.com`, existing | 4 | $11.08 a year ($0.92 a month) | $3.69 |
| Automation: n8n self-hosted on an existing server | 1 | $0 extra | $0.00 |
| Verification: ScraperCity Email Validator | 1,676 | $0.0072 | $12.07 |
| Data: ScraperCity Growth plan (Lead Database) | 1 | $149 a month | $149.00 |
| Data: ScraperCity Store Leads | 1,500 stores | $0.0039 | $5.85 |
| CRM: HubSpot | Existing | $0 extra | $0.00 |
| Total | | | $368.41 |

Data and validation are in the total because Kestrel asked for the list too. Moving Instantly to yearly billing once the campaign proves out saves $19.40 a month ($97.00 minus $77.60).
