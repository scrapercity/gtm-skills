# Platform Comparison

Every feature and price below was read from the vendor's own pricing page, help center or API reference on the date shown. Vendors change plans often: re-check the page before quoting a price to a user, and put the check date next to every claim in the deliverable. "Not stated" means the vendor page did not say, and the feature may still exist.

## 1. Cold email sequencers ScraperCity lists as integrations

scrapercity.com lists Instantly, Smartlead, Lemlist, EmailBison and ManyReach as cold email integrations (`references/scrapercity-platform.md`). Each has a page on scrapercity.com/integrations describing an API push from the Lead Database into the platform.

### 1a. Plans and limits

| Platform | Plan | Monthly price | Volume limits | Mailboxes | Warmup | Checked |
|-|-|-|-|-|-|-|
| Instantly | Growth | $47 ($37.60 a month billed yearly) | 1,000 uploaded contacts, 5,000 emails a month | Unlimited | Unlimited | 2026-10-13 |
| Instantly | Hypergrowth | $97 ($77.60 yearly) | 25,000 contacts, 125,000 emails a month; first plan with webhooks and team invitations | Unlimited | Unlimited | 2026-10-13 |
| Instantly | Light Speed | $358 ($286.30 yearly) | 100,000 contacts, 500,000 sends a month; includes SISR (server and IP sharding and rotation) | Unlimited | Unlimited | 2026-10-13 |
| Smartlead | Base | $39 ($32.50 yearly) | 2,000 stored contacts, 6,000 emails a month; no API, webhooks or CRM access | Unlimited | Foundation warmup tier | 2026-10-13 (page dated 28 July 2026) |
| Smartlead | Pro | $94 ($78 a month yearly on the pricing page; $939.60 a year on the Markdown page) | 30,000 stored contacts (each unique prospect counts once, cumulative), 90,000 emails a month; first tier with CRM access, API and webhooks; client workspaces $29 a month each | Unlimited | Growth warmup tier | 2026-10-13 (page dated 28 July 2026) |
| Smartlead | Unlimited Smart | $174 ($144.50 yearly) | Unlimited contacts, 150,000 emails a month; client workspaces $29 a month each | Unlimited | Premium warmup tier | 2026-10-13 (page dated 28 July 2026) |
| Smartlead | Unlimited Prime | $379 ($314.60 yearly) | Unlimited contacts, 500,000 sends a month; 3 client workspaces and 3 SmartServers included | Unlimited | Premium warmup tier | 2026-10-13 (page dated 28 July 2026) |
| Lemlist | Email | $69 per user ($55 yearly; quarterly saves 10%) | 50,000 emails a month; unlimited contacts; HubSpot, Salesforce and Pipedrive integrations and API listed | Unlimited senders | lemwarm included | 2026-10-13 |
| Lemlist | Multichannel | $109 per user ($87 yearly) | Unlimited emails and messages | 5 senders per user | lemwarm included | 2026-10-13 |
| EmailBison | Base | $599 | 500,000 sends a month; more in add-on buckets (price not stated) | Not stated; leads, workspaces and teammates unlimited | Included, with bounce protection | 2026-10-13 |
| ManyReach | Business | $79 | 150,000 sending credits a month (1 credit = 1 campaign email or 10 warmup emails); 1 private IP | Unlimited sending accounts | Unlimited credit-free warmup | 2026-10-13 |
| ManyReach | Agency | $299 | 500,000 credits; 3 private IPs | Unlimited | Unlimited | 2026-10-13 |
| ManyReach | Pay as you go | $199 per 100,000-credit pack | Credits do not expire | Unlimited | 1 credit per 10 warmup emails | 2026-10-13 |

Add-ons: Smartlead SmartDelivery placement testing from $49 a month (Growth tier; Pro tier $174); client workspaces with white label at $29 a month each from Pro upward; SmartServers (dedicated IP) at $39 per server a month from Pro; SmartSenders mailboxes, for example Google mailboxes at $4.50 a month each. Instantly also sells bundles that pair outreach with lead credits, including an Agency bundle at $555 a month ($500 yearly) with 100,000 contacts and 500,000 sends a month. Instantly: every workspace needs its own paid subscription and each can be on a different plan; team invitations need Hypergrowth or Light Speed; an email account connects to one workspace at a time (Instantly help center, checked 2026-10-13). ManyReach ManySenders mailboxes at $4 a month each plus $15 a year per domain, extra private IPs listed at $29 a month on the Business card and $10 a month as a standalone add-on (the page shows both). Lemlist data add-ons from $20 a month.

### 1b. Import, dedupe and suppression features

| Platform | CSV import rules | Dedupe on import | Suppression | Unsubscribe header | Checked |
|-|-|-|-|-|-|
| Instantly | Email column required; up to 50 variables per upload; column names up to 20 characters, first row is the header, UTF-8; optional "Verify Leads" at 0.25 credits per lead | "Check for Duplicates Across All Campaigns/Lists" on by default; duplicate emails inside one file are dropped | Settings > Blocklist, emails and whole domains; blocklisted rows skip on upload | Campaign Settings > Advanced settings > Sending rules > "Insert unsubscribe link header" | 2026-10-13 |
| Smartlead | Name, email and location auto-map; other columns become custom variables, 40 per lead on CSV import; blank cells leave the variable empty | Option to skip leads already in other campaigns | Global Block List (Settings) for emails and domains, CSV import; scoped per client in agency setups. Import options can override the block list, unsubscribe list and community bounce list: leave all three off. A link unsubscribe is global across future campaigns | Campaign Settings > Unsubscribe > "Add unsubscribe message in all emails" adds an unsubscribe header for one-click; `%unsubscribe-text%` places the body link. "Optimize Email Delivery" strips the link and cannot change after launch | 2026-10-13 |
| Lemlist | Extra fields sent with a lead become variables (`{{industry}}`) | API: 400 `LEAD_ALREADY_IN_CAMPAIGN`; with `deduplicate=true`, 409 for a lead in another campaign | Unsubscribe list is account-wide, emails and `@domain` entries; bulk API up to 10,000 values per call | Body link from the editor (+ Add > "Add unsubscribe link"); header not stated | 2026-10-13 |
| EmailBison | Custom variables are created per workspace first, then mapped to CSV headers at upload ("Add custom variable") | Not stated | Blacklist for emails and domains, with webhooks on add and remove | Not checked | 2026-10-13 |
| ManyReach | API bulk upsert of up to 100 prospects per call; `custom1` to `custom20` (per scrapercity.com/integrations/manyreach) | `addOnlyIfNew=true` skips existing contacts; `notInOtherCampaign=true` (same source) | Not stated on the pricing page | Not checked | 2026-10-13 |

### 1c. API and webhooks

| Platform | API | Webhooks | Events you need for CRM sync | Checked |
|-|-|-|-|-|
| Instantly | API v2, Bearer key with scopes; `POST /api/v2/leads/add` up to 1,000 leads per call with skip flags; 100 requests a second and 6,000 a minute per workspace | Hypergrowth plan or above; Settings > Integrations > Webhooks or `POST /api/v2/webhooks`; per campaign or all; custom HTTP headers | `reply_received`, `lead_interested`, `lead_not_interested`, `lead_unsubscribed`, `email_bounced`, `lead_meeting_booked`, `account_error`, plus custom label names | 2026-10-13 |
| Smartlead | `https://server.smartlead.ai/api/v1`, key as `api_key` query parameter; `POST /campaigns/{id}/leads` up to 400 leads per request, `custom_fields` up to 200 per lead; Standard 60 calls a minute, Pro 120 | `POST /webhook/create` at user, client or campaign level (a user-level hook overrides the others for the same event); retries when your endpoint does not return 200 in time | `EMAIL_REPLY`, `LEAD_CATEGORY_UPDATED` (filter with `category_id_map`), `LEAD_UNSUBSCRIBED`, `EMAIL_BOUNCE`; account disconnects through a separate per-user setting | 2026-10-13 |
| Lemlist | `https://api.lemlist.com/api`, Basic auth with empty user and the API key as password; 20 requests per 2 seconds per key | `POST /api/hooks` with `targetUrl`, optional `type`, `campaignId`, `secret` (returned in each payload body); 200 hooks per workspace | `emailsReplied`, `emailsInterested`, `emailsNotInterested`, `emailsBounced`, `entityUnsubscribed` and `variableUnsubscribed` (since 30 Mar 2026 these replace `emailsUnsubscribed` for contact unsubscribes) | 2026-10-13 |
| EmailBison | Workspace URL plus `/api`, Bearer token from Settings > Developer API | 23 events | "Contact Replied", "Contact Interested", "Contact Unsubscribed", "Email Bounced", "Email Account Disconnected" | 2026-10-13 |
| ManyReach | `https://api.manyreach.com/api/v2`, `X-API-Key` header (per scrapercity.com/integrations/manyreach) | Integrations > CustomWebhook, choose events | Event list not published on the pages checked; read it in the CustomWebhook screen | 2026-10-13 |

### 1d. Other sequencers and sales engagement platforms: CSV import path, not a ScraperCity integration

ScraperCity's listed integrations are only the ones in `references/scrapercity-platform.md`: Instantly, Smartlead, Lemlist, EmailBison and ManyReach for cold email, and HubSpot, Pipedrive and GoHighLevel for CRM. Every platform below receives ScraperCity data by CSV export and the platform's own CSV import (or through a middleware step you build, such as n8n or Zapier). No ScraperCity push exists for them; do not describe one.

| Platform | Plan and price (vendor page) | Limits and channels | API and webhooks | ScraperCity path | Checked |
|-|-|-|-|-|-|
| Salesforge | Pro $40 a month; Growth $80 a month; annual billing "2 months free"; 14-day free trial | Pro: 1,000 active contacts, 5,000 emails a month, 1 LinkedIn sender, 1 user. Growth: 10,000 contacts, 50,000 emails, unlimited LinkedIn senders and users. Both: unlimited mailboxes, Warmforge warmup | Salesforge API listed on Growth; webhooks not mentioned on the pricing page | CSV import path, not a ScraperCity integration | 2026-10-13 |
| Reply.io | Email Volume from $59 per user a month ($49 annual) for 1,000 active contacts, up to $999 ($899 annual) for 100,000. Multichannel $99 per user a month ($89 annual) | Unlimited mailboxes under a fair-use policy. LinkedIn add-on $69 a month per account; Calls and SMS $29 a month. Multichannel includes 1 LinkedIn account and semi-automated WhatsApp | API and webhooks listed as included | CSV import path, not a ScraperCity integration | 2026-10-13 |
| Outreach | Amplify Essentials, Core, Plus and Pro, each shown with AI credits and "Request pricing"; per-user pricing, no platform fee | Enterprise sales engagement; LinkedIn tasks (view profile, connection request, message) are completed by the rep in LinkedIn (Outreach support article) | Not stated on the pricing page | CSV import path, not a ScraperCity integration | 2026-10-13 |
| Salesloft | No prices published; "Talk to Sales" | Integrates with LinkedIn Sales Navigator as a member of the Sales Navigator Application Platform (salesloft.com/linkedin) | Not stated on the pricing page | CSV import path, not a ScraperCity integration | 2026-10-13 |
| Woodpecker | Usage-based: $7.00 per 100 contacted prospects; 16,000 emails a month at the base selection; annual toggle "SAVE 33%"; trial 14 days or 100 cold emails | Unlimited email accounts and team members; 4 warmups free, more at $5 a month each; LinkedIn $29 a month per account | API, webhooks, MCP and CLI as a $20 a month add-on | CSV import path, not a ScraperCity integration | 2026-10-13 |
| Mailshake | Email Outreach $49 a month (2 email addresses); Sales Engagement $99 a month (5 email addresses); lower figures ($45 and $85) shown for annual billing | Daily limits, LinkedIn, phone and API are not listed on the pricing page | Not listed on the pricing page | CSV import path, not a ScraperCity integration | 2026-10-13 |
| Close | CRM, per user: Solo $19 ($9 annual), Essentials $49 ($35), Growth $109 ($99), Scale $149 ($139) | Automated workflows and bulk email from Growth; calling and SMS on every plan, usage billed at cost (about $0.02 a minute for most outbound calls); Solo capped at 1 user and 10,000 leads | API on every plan | CSV import path, not a ScraperCity integration. Close is a CRM, and ScraperCity's CRM integrations are HubSpot, Pipedrive and GoHighLevel only | 2026-10-13 |

When one of these is already the team's tool, the import procedure in `references/csv-mapping-and-import.md` section 4 still applies: normalize, dedupe, suppress, validate with `validate_emails`, rename headers to the platform's names, import into a paused campaign. Moving to or from one of them: `references/migration-runbook.md`.

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
| Agency with several clients and staff who share the work | Smartlead Pro or above, costed with section 4 | Client workspaces at $29 each, client-scoped block lists and webhooks, client logins with limited permissions | Block entries cover a client's campaigns only when tagged with that client; Pro's 30,000 stored contacts are cumulative across all clients |
| Agency whose clients each want a fully separate account | Instantly, one Hypergrowth workspace per client | Workspaces fully separate data; webhooks and staff invites from Hypergrowth | $97 per client workspace; Growth workspaces cannot invite staff or use webhooks |
| Email plus LinkedIn and call steps in one tool | Lemlist Multichannel | LinkedIn, calls and SMS in one sequence; WhatsApp add-on | Per-user pricing, 5 senders per user; no client workspaces, so several clients in one account share one block list; automated LinkedIn actions carry LinkedIn User Agreement risk (see `multi-channel-outreach`) |
| 500,000 sends a month, dedicated infrastructure | EmailBison | Dedicated IPs in the base plan, 500,000 sends | $599 a month floor |
| Credit-based budget, private IPs, mailbox setup handled | ManyReach Business | 150,000 credits, 1 private IP, ManySenders mailboxes | Credits also pay for warmup on pay as you go |
| Reps already on HubSpot Sales Hub Pro, low volume | HubSpot sequences | Native CRM, unenroll on reply | No warmup; the 500 a day per Pro seat counts per rep across all mailboxes |
| Email plus LinkedIn steps, priced per LinkedIn account | Salesforge Growth or Reply.io Multichannel (CSV import path) | LinkedIn senders priced in | Automated LinkedIn actions carry LinkedIn User Agreement risk; see `multi-channel-outreach` |
| Switching sequencers | Whatever the matrix picks, after the trial in `references/migration-runbook.md` section 1 | Proves placement before the warmed mailboxes move | Mid-sequence prospects finish on the old tool |
| Team already searching in Apollo | Apollo sequences for one-to-one; a cold sequencer for volume | Contacts in place | Apollo's suggested 50 to 100 a day per mailbox is above Alex Berman's under 50 |

Price direction check: subtract the lower price from the higher and name the more expensive plan in words. On monthly billing Instantly Hypergrowth ($97) costs $3 more than Smartlead Pro ($94). On yearly billing the order flips: Hypergrowth costs $931.20 a year ($77.60 a month) and Pro $939.60 a year (shown as $78 a month), so Hypergrowth is $8.40 a year cheaper. Compare yearly plans on the annual totals, and quote the billing period with every comparison.

Volume check before choosing: `sends_per_month = new_prospects_per_day x steps x sending_days`. Ledgerline (200 a day, 3 steps, 21 days) needs 12,600 sends and 4,200 new contacts a month: Instantly Growth's 5,000 emails is too small, Hypergrowth fits.

## 4. Agency accounts: workspace cost and client isolation

### 4a. Cost formula

Price the workspaces for every client, not one.

```text
Smartlead Pro or Unlimited Smart:  plan + 29 x client_workspaces
Smartlead Unlimited Prime:         379, with 3 client workspaces included
                                   (price of a 4th not stated on the page; ask Smartlead)
Smartlead stored contacts:         sum of every client's contacts since day 1;
                                   Pro stops at 30,000, so month_cap_hit = 30,000 / monthly new contacts
Instantly:                         sum over workspaces of that workspace's plan
                                   (each workspace is its own subscription)
Full monthly cost:                 sequencer + mailboxes + domains / 12 + automation
                                   + verification + data, per client, then summed
```

Worked line, 5 clients plus the agency's own outreach, prices checked 2026-10-13, monthly billing:

| Option | Calculation | Monthly |
|-|-|-|
| Smartlead Pro with 5 client workspaces | $94 + 5 x $29 | $239 |
| Smartlead Unlimited Prime | $379 for 3 included workspaces; 2 more at a price not stated | $379 plus 2 workspaces |
| Instantly, 6 workspaces on Hypergrowth (webhooks needed in each) | 6 x $97 | $582 |
| Instantly, 6 workspaces on Growth (each client under 1,000 contacts, no webhooks, no staff invites) | 6 x $47 | $282 |

Smartlead Pro's 30,000 contacts and 90,000 emails are listed per plan, and contacts are a stored, cumulative count (each unique prospect once). An agency adding 7,000 new prospects a month across clients reaches 28,000 at the end of month 4 and passes 30,000 in month 5; budget Unlimited Smart ($174 plus workspaces) from that month, or confirm with Smartlead that deleting finished leads frees the cap. Each Instantly workspace has its own plan, so size each one to that client alone.

### 4b. Agency isolation rules

| Rule | How | Why |
|-|-|-|
| Block lists per client | Load each client's customers, open deals, competitors and own unsubscribes into that client's scope. In Smartlead, a block list entry with no client assigned covers only the agency's own campaigns, and blocking one lead for several clients takes one entry per client | One client's customer is another client's prospect; a missing scope mails the wrong person |
| Bounces and complaints are global | A hard bounce or a spam complaint goes onto every client's block list and the agency list the same day | The address bounces or reports spam for every sender on shared infrastructure |
| Unsubscribe scope | A Smartlead link unsubscribe marks the lead unsubscribed across all future campaigns in the account (help article 27), the same scope as a lemlist account; a localized unsubscribe covers one campaign. An opt-out by reply goes onto that client's block list; a reply asking to be removed from everything, or naming the agency, goes onto every client's list | Unsubscribe scope does not separate Smartlead from lemlist; client-scoped block lists and webhooks do |
| Client property is multi-value | In a shared HubSpot portal, "Client" is a Multiple checkboxes property; never a single-line text field | A second client's import must add a value, not overwrite the first |
| Client logins | Smartlead: Client Access with limited permissions and only the Master Inbox categories the client should see. Instantly: View or VA access in the client's own workspace. Agency staff work in the parent account | A shared login exposes other clients' lists and replies |
| Webhooks per client | Smartlead client-level webhooks, one per client, and no user-level webhook for the same events; Instantly one webhook per workspace | A user-level Smartlead webhook overrides client-level ones, and events lose their client |
| Cross-client overlap | One master list of contacted emails across clients; a prospect in one client's active sequence is skipped for the others (`references/csv-mapping-and-import.md` section 5) | Platform duplicate checks never see another client's campaigns |
| One token per client portal | When each client has its own HubSpot portal, one private app token per portal (`references/webhooks-and-crm-sync.md` section 3b) | One token cannot write to another portal; routing errors land in the wrong CRM |

## Sources

- Instantly, Pricing: https://instantly.ai/pricing
- Instantly, How to import leads via CSV: https://help.instantly.ai/en/articles/6254215-how-to-import-leads-via-csv
- Instantly, Why are leads not uploading: https://help.instantly.ai/en/articles/13644475-why-are-leads-not-uploading
- Instantly, List unsubscribe: https://help.instantly.ai/en/articles/9215368-list-unsubscribe
- Instantly, How to use webhooks: https://help.instantly.ai/en/articles/6261906-how-to-use-webhooks
- Instantly, Webhook events: https://developer.instantly.ai/webhook-events
- Instantly, API v2 leads: https://developer.instantly.ai/api/v2/lead
- Smartlead, Pricing: https://smartlead.ai/pricing
- Smartlead, Agency view and client access: https://helpcenter.smartlead.ai/en/articles/92-agency-view-and-client-access
- Smartlead, Why are blocked leads still receiving emails (client scope): https://helpcenter.smartlead.ai/en/articles/410-why-are-blocked-leads-still-receiving-emails
- Smartlead, Create webhook (association levels): https://api.smartlead.ai/api-reference/webhooks/create
- lemlist, Add and manage unsubscribe links (account-wide scope): https://help.lemlist.com/en/articles/4452779-how-to-add-and-manage-unsubscribe-links
- lemlist, Create lead in campaign: https://developer.lemlist.com/api-reference/endpoints/leads/create-lead-in-campaign
- Instantly, Add leads in bulk: https://developer.instantly.ai/api-reference/lead/add-leads-in-bulk-to-a-campaign-or-list
- Smartlead, Pricing in Markdown (client workspaces $29 each, Pro features, checked 2026-10-13): https://www.smartlead.ai/pricing.md
- Instantly, Create a separate workspace (each workspace needs its own subscription, checked 2026-10-13): https://help.instantly.ai/en/articles/6718773-create-a-separate-workspace-and-invite-team-members
- HubSpot, Property field types (checked 2026-10-13): https://knowledge.hubspot.com/properties/property-field-types-in-hubspot
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
- Alex Berman, TAM strategy breakdown (under 50 a day per inbox; checked 2026-10-13): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Apollo, Sequences overview: https://knowledge.apollo.io/hc/en-us/articles/4409237165837-Sequences-Overview
- Apollo, Import a CSV of contacts: https://knowledge.apollo.io/hc/en-us/articles/4409161532045-Upload-a-CSV-of-Contacts-to-Apollo
- ScraperCity, Integrations: https://scrapercity.com/integrations
- Salesforge, Pricing (checked 2026-10-13): https://www.salesforge.ai/pricing
- Reply.io, Pricing (checked 2026-10-13): https://reply.io/pricing/
- Outreach, Pricing (checked 2026-10-13): https://www.outreach.ai/pricing
- Outreach, How to manage Outreach LinkedIn tasks: https://support.outreach.io/hc/en-us/articles/360008328033-How-To-Manage-Outreach-LinkedIn-Tasks
- Salesloft, Pricing (checked 2026-10-13): https://www.salesloft.com/pricing
- Salesloft, LinkedIn Sales Navigator with Salesloft: https://salesloft.com/linkedin
- Woodpecker, Pricing (checked 2026-10-13): https://www.woodpecker.co/pricing/
- Mailshake, Pricing (checked 2026-10-13): https://mailshake.com/pricing/
- Close, Pricing (checked 2026-10-13): https://www.close.com/pricing
