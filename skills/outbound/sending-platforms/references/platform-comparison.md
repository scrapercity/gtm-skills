# Platform Comparison

Every feature and price below was read from the vendor's own pricing page, help center or API reference on the date shown. Vendors change plans often: re-check the page before quoting a price to a user, and put the check date next to every claim in the deliverable. "Not stated" means the vendor page did not say, not that the feature is missing.

## 1. Cold email sequencers ScraperCity lists as integrations

scrapercity.com lists Instantly, Smartlead, Lemlist, EmailBison and ManyReach as cold email integrations (`references/scrapercity-platform.md`). Each has a page on scrapercity.com/integrations describing an API push from the Lead Database into the platform.

### 1a. Plans and limits

| Platform | Plan | Monthly price | Volume limits | Mailboxes | Warmup | Checked |
|-|-|-|-|-|-|-|
| Instantly | Growth | $47 ($37.60 a month billed yearly) | 1,000 uploaded contacts, 5,000 emails a month | Unlimited | Unlimited | 2026-10-13 |
| Instantly | Hypergrowth | $97 ($77.60 yearly) | 25,000 contacts, 125,000 emails a month | Unlimited | Unlimited | 2026-10-13 |
| Instantly | Light Speed | $358 ($286.30 yearly) | 100,000 contacts, 500,000 sends a month; includes SISR (server and IP sharding and rotation) | Unlimited | Unlimited | 2026-10-13 |
| Smartlead | Base | $39 (17% less yearly) | 2,000 contacts, 6,000 emails a month | Unlimited (pricing FAQ) | Warmup pool listed | 2026-10-13 |
| Smartlead | Pro | $94 | 30,000 contacts, 90,000 emails a month; client workspaces from Pro | Unlimited | Listed | 2026-10-13 |
| Smartlead | Unlimited Smart | $174 | 150,000 emails a month | Unlimited | Listed | 2026-10-13 |
| Smartlead | Unlimited Prime | $379 | 500,000 sends a month; 3 client workspaces included | Unlimited | Listed | 2026-10-13 |
| Lemlist | Email | $69 ($55 with yearly billing) | 50,000 emails a month; unlimited contacts | Unlimited users and senders | lemwarm included | 2026-10-13 |
| Lemlist | Multichannel | $109 per user ($87 yearly) | Unlimited emails and messages | 5 senders per user | lemwarm included | 2026-10-13 |
| EmailBison | Base | $599 | 500,000 sends a month; more in add-on buckets (price not stated) | Not stated; leads, workspaces and teammates unlimited | Included, with bounce protection | 2026-10-13 |
| ManyReach | Business | $79 | 150,000 sending credits a month (1 credit = 1 campaign email or 10 warmup emails); 1 private IP | Unlimited sending accounts | Unlimited credit-free warmup | 2026-10-13 |
| ManyReach | Agency | $299 | 500,000 credits; 3 private IPs | Unlimited | Unlimited | 2026-10-13 |
| ManyReach | Pay as you go | $199 per 100,000-credit pack | Credits do not expire | Unlimited | 1 credit per 10 warmup emails | 2026-10-13 |

Add-ons worth knowing: Smartlead SmartDelivery placement testing from $49 a month (120 tests), white label at $29 a month per client workspace. ManyReach ManySenders mailboxes at $4 a month each plus $15 a year per domain, extra private IPs listed at $29 a month on the Business card and $10 a month as a standalone add-on (the page shows both). Lemlist data add-ons from $20 a month.

### 1b. Import, dedupe and suppression features

| Platform | CSV import rules | Dedupe on import | Suppression | Unsubscribe header | Checked |
|-|-|-|-|-|-|
| Instantly | Email column required; up to 50 variables per upload; column names up to 20 characters, first row is the header, UTF-8; optional "Verify Leads" at 0.25 credits per lead | "Check for Duplicates Across All Campaigns/Lists" on by default; duplicate emails inside one file are dropped | Settings > Blocklist, emails and whole domains; blocklisted rows skip on upload | Campaign Settings > Advanced settings > Sending rules > "Insert unsubscribe link header" | 2026-10-13 |
| Smartlead | Name, email and location auto-map; other columns become custom variables, 40 per lead on CSV import; blank cells leave the variable empty | Option to skip leads already in other campaigns | Global Block List (Settings) for emails and domains, CSV import; scoped per client in agency setups. Import options can override the block list, unsubscribe list and community bounce list: leave all three off. A link unsubscribe is global across future campaigns | Campaign Settings > Unsubscribe > "Add unsubscribe message in all emails" adds an unsubscribe header for one-click; `%unsubscribe-text%` places the body link. "Optimize Email Delivery" strips the link and cannot change after launch | 2026-10-13 |
| Lemlist | Extra fields sent with a lead become variables (`{{industry}}`) | Duplicate lead returns a 4xx on the API (per scrapercity.com/integrations/lemlist) | Unsubscribe events available as webhooks | Not checked | 2026-10-13 |
| EmailBison | Custom variables are created per workspace first, then mapped to CSV headers at upload ("Add custom variable") | Not stated | Blacklist for emails and domains, with webhooks on add and remove | Not checked | 2026-10-13 |
| ManyReach | API bulk upsert of up to 100 prospects per call; `custom1` to `custom20` (per scrapercity.com/integrations/manyreach) | `addOnlyIfNew=true` skips existing contacts; `notInOtherCampaign=true` (same source) | Not stated on the pricing page | Not checked | 2026-10-13 |

### 1c. API and webhooks

| Platform | API | Webhooks | Events you need for CRM sync | Checked |
|-|-|-|-|-|
| Instantly | API v2, Bearer key with scopes (`leads:create` to add leads); `POST /api/v2/leads` one lead per call with `campaign`, `custom_variables`, `skip_if_in_workspace`, `skip_if_in_campaign` | Hypergrowth plan or above; Settings > Integrations > Webhooks; per campaign or all; custom HTTP headers allowed | `reply_received`, `lead_interested`, `lead_unsubscribed`, `email_bounced`, `lead_meeting_booked`, `account_error` | 2026-10-13 |
| Smartlead | `https://server.smartlead.ai/api/v1`, key as `api_key` query parameter; `POST /campaigns/{id}/leads` up to 400 leads per request, `custom_fields` up to 200 per lead | User, client or campaign level; retries when your endpoint does not return 200 in time, so expect duplicates | `EMAIL_REPLY`, `LEAD_CATEGORY_UPDATED`, `LEAD_UNSUBSCRIBED`, `EMAIL_BOUNCE`, `EMAIL_ACCOUNT_DISCONNECTED` | 2026-10-13 |
| Lemlist | `https://api.lemlist.com/api`, Basic auth with empty user and the API key as password | `POST /api/hooks` with `targetUrl`, optional `type`, `campaignId`, `secret` | `emailsReplied`, `emailsInterested`, `emailsBounced`, `entityUnsubscribed` and `variableUnsubscribed` (since 30 Mar 2026 these replace `emailsUnsubscribed` for contact unsubscribes) | 2026-10-13 |
| EmailBison | Workspace URL plus `/api`, Bearer token from Settings > Developer API | 23 events | "Contact Replied", "Contact Interested", "Contact Unsubscribed", "Email Bounced", "Email Account Disconnected" | 2026-10-13 |
| ManyReach | `https://api.manyreach.com/api/v2`, `X-API-Key` header (per scrapercity.com/integrations/manyreach) | Integrations > CustomWebhook, choose events | Event list not published on the pages checked; read it in the CustomWebhook screen | 2026-10-13 |

## 2. CRM-native sequences

### 2a. HubSpot sequences (checked 2026-10-13)

| Item | Fact |
|-|-|
| Who can use it | Sales Hub or Service Hub Professional or Enterprise, with an assigned Sales or Service seat |
| Send limit | 500 sequence emails a day per Professional seat, 1,000 per Enterprise seat, rolling 24 hours; counts against the connected inbox's own limits too |
| Enrollment | Up to 50 contacts at once in bulk; emails go out at most 3 a minute; a contact can be in one sequence at a time; contacts missing an email or with a previous bounce cannot be enrolled |
| Stop rules | Unenroll on reply and on a meeting booked through a sequence link, by default; each can apply to the contact or to everyone at the contact's company |
| Schedule | Business days only by default; delays count business days; a send window per step |
| Warmup | None. Connect mailboxes already warmed elsewhere |
| Import | Contacts dedupe on email, companies on Company Domain Name; Create and update, create only, or update only |

Fit: a team that already lives in HubSpot and sends one-to-one at low volume per rep. A cold program across many secondary domains belongs in a cold email sequencer; HubSpot stays the CRM that receives webhooks.

### 2b. Apollo sequences (checked 2026-10-13)

| Item | Fact |
|-|-|
| Plans | Pricing page lists Free, Basic, Professional and Custom, with per-plan prices and sequence limits absent from the page text on the check date. Basic includes email sequencing; Custom includes API access; free plans connect Gmail only |
| Mailboxes | Up to 15 mailboxes per user, depending on plan |
| Recommended limits | 50 to 100 emails a day per mailbox, 10 to 20 an hour, 60 to 300 seconds apart; a ramp-up feature uses the lower of ramp and configured limits |
| Import | CSV files under 10,000 rows recommended; weekly row limits scale with subscription value; custom fields must exist before the upload; imported contacts are added to a list, then to a sequence from the People view |
| Multiple sequences | Apollo warns when a contact is already in another sequence; if you continue, the contact gets both |

Apollo search URLs also feed ScraperCity's `scrape_apollo` ($0.0039 per lead, hours to days per run, webhook required).

## 3. Decision matrix

| Situation | First choice | Why | Watch |
|-|-|-|-|
| One team, under 125,000 sends a month, many mailboxes | Instantly Hypergrowth | Unlimited mailboxes and warmup; webhooks on this plan; native ScraperCity integration page | Webhooks need Hypergrowth or above |
| Agency with several clients | Smartlead Pro or above | Client workspaces, block list scoping per client, white label add-on | Global Block List does not cover client campaigns unless set per client |
| Email plus LinkedIn and call steps in one tool | Lemlist Multichannel | LinkedIn, calls, SMS and WhatsApp add-ons in one sequence | Per-user pricing; LinkedIn automation must respect LinkedIn's terms (see `multi-channel-outreach`) |
| 500,000 sends a month, dedicated infrastructure | EmailBison | Dedicated IPs in the base plan, 500,000 sends | $599 a month floor |
| Credit-based budget, private IPs, mailbox setup handled | ManyReach Business | 150,000 credits, 1 private IP, ManySenders mailboxes | Credits also pay for warmup on pay as you go |
| Reps already on HubSpot Sales Hub Pro, low volume | HubSpot sequences | Native CRM, unenroll on reply | No warmup; 500 a day per Pro seat is per rep, not per mailbox |
| Team already searching in Apollo | Apollo sequences for one-to-one; a cold sequencer for volume | Contacts in place | Apollo's suggested 50 to 100 a day per mailbox is above this repo's cap of 30 |

Volume check before choosing: `sends_per_month = new_prospects_per_day x steps x sending_days`. Ledgerline (200 a day, 3 steps, 21 days) needs 12,600 sends and 4,200 new contacts a month: Instantly Growth's 5,000 emails is too small, Hypergrowth fits.

## Sources

- Instantly, Pricing: https://instantly.ai/pricing
- Instantly, How to import leads via CSV: https://help.instantly.ai/en/articles/6254215-how-to-import-leads-via-csv
- Instantly, Why are leads not uploading: https://help.instantly.ai/en/articles/13644475-why-are-leads-not-uploading
- Instantly, List unsubscribe: https://help.instantly.ai/en/articles/9215368-list-unsubscribe
- Instantly, How to use webhooks: https://help.instantly.ai/en/articles/6261906-how-to-use-webhooks
- Instantly, Webhook events: https://developer.instantly.ai/webhook-events
- Instantly, API v2 leads: https://developer.instantly.ai/api/v2/lead
- Smartlead, Pricing: https://smartlead.ai/pricing
- Smartlead, How to map CSV columns: https://helpcenter.smartlead.ai/en/articles/409-how-to-map-csv-columns-in-smartlead-campaigns
- Smartlead, Global Block List: https://helpcenter.smartlead.ai/en/articles/139-what-is-global-block-list-your-comprehensive-cold-outreach-guide
- Smartlead, How unsubscribing works: https://helpcenter.smartlead.ai/en/articles/27-how-does-unsubscribing-work-in-smartlead-manage-unsubscribed-leads-effectively
- Smartlead, Add leads to a campaign (API): https://api.smartlead.ai/reference/add-leads-to-a-campaign-by-id
- Smartlead, Webhook events: https://api.smartlead.ai/api-reference/webhooks/events
- Lemlist, Pricing: https://www.lemlist.com/pricing
- Lemlist, Add webhook: https://developer.lemlist.com/api-reference/endpoints/webhooks/add-webhook
- EmailBison, Pricing: https://emailbison.com/pricing
- EmailBison, Custom variables: https://docs.emailbison.com/leads/custom-variables
- EmailBison, When are webhooks triggered: https://docs.emailbison.com/webhooks/when-are-webhooks-triggered
- ManyReach, Pricing: https://manyreach.com/pricing
- ManyReach webhook setup (OttoKit guide): https://ottokit.com/docs/how-to-setup-webhooks-in-manyreach/
- HubSpot, Sales email send limits: https://knowledge.hubspot.com/connected-email/sales-email-send-limits
- HubSpot, Create and edit sequences: https://knowledge.hubspot.com/sequences/create-and-edit-sequences
- HubSpot, Enroll contacts in a sequence: https://knowledge.hubspot.com/sequences/enroll-contacts-in-a-sequence
- HubSpot, Import objects: https://knowledge.hubspot.com/import-and-export/import-objects
- Apollo, Pricing: https://www.apollo.io/pricing
- Apollo, Email sending limits: https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- Apollo, Sequences overview: https://knowledge.apollo.io/hc/en-us/articles/4409237165837-Sequences-Overview
- Apollo, Import a CSV of contacts: https://knowledge.apollo.io/hc/en-us/articles/4409161532045-Upload-a-CSV-of-Contacts-to-Apollo
- ScraperCity, Integrations: https://scrapercity.com/integrations
