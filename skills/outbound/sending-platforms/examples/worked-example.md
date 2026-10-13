# Sending Platform Plan: Kestrel Studio

Prepared 2026-10-13 for Kestrel Studio (fictional agency used as an example), which builds Klaviyo email flows for Shopify apparel brands. Vendor pages checked 2026-10-13.

## Summary

Kestrel will run its own outbound to US Shopify apparel stores that have Klaviyo installed and 20,000 to 200,000 estimated monthly visits. ScraperCity Store Leads supplies 1,500 stores, the Lead Database supplies founders and ecommerce leads at 990 of them, and the other 496 stores get a variant sent to the store inbox. After suppression and validation, 1,587 contacts go into three Instantly campaigns: named people (1,002 valid), store inboxes (401 valid) and catch-alls (184). Instantly Hypergrowth ($97 a month) is the pick: 1,587 contacts is over the Growth plan's 1,000-contact limit, and webhooks, which feed HubSpot through n8n, need Hypergrowth or above. Twelve warmed mailboxes on 4 domains send at 30 a day each, 360 a day in total. First month cost is $263.92, of which $17.92 is pay-per-result ScraperCity data.

## Requirements

| Input | Value | Source |
|-|-|-|
| New prospects per day | 76 (1,587 over 21 sending days) | This plan |
| Steps per sequence | 3 | `cold-email-strategy` plan |
| Contacts per month (month 1 and month 2) | 1,587 and about 1,600 | Store Leads count and next month's pull |
| Sends per month (month 1 and month 2) | 4,761 (1,587 x 3) and about 4,800 | Contacts x steps |
| Mailboxes connected | 12 on 4 domains, warmed, cap 30 | `inbox-setup` roster |
| Seats and workspaces | 2 users, 1 workspace | Kestrel |
| CRM and middleware | HubSpot (existing), n8n self-hosted (existing server) | Kestrel |

## Platform Decision

| Option | Plan and price | Fits because | Gaps | Checked |
|-|-|-|-|-|
| Instantly | Hypergrowth, $97 a month: 25,000 contacts, 125,000 emails, unlimited mailboxes and warmup | Covers month 2 with room; webhooks available on Hypergrowth or above; duplicate check across campaigns on by default; blocklist for emails and domains; unsubscribe header setting; ScraperCity integration page | API adds one lead per call | 2026-10-13 |
| Instantly | Growth, $47 a month: 1,000 contacts, 5,000 emails | Price | 1,587 contacts is over the limit; no webhooks below Hypergrowth | 2026-10-13 |
| Smartlead | Pro, $94 a month: 30,000 contacts, 90,000 emails | Client workspaces if Kestrel later runs client campaigns; API up to 400 leads per request | Per-plan webhook availability not legible in the pricing page text; would need confirming in the app | 2026-10-13 |
| Lemlist | Email, $69 a month: 50,000 emails, unlimited senders, lemwarm | Variables from any extra field | Multichannel not needed; webhook plan availability not stated | 2026-10-13 |
| ManyReach | Business, $79 a month: 150,000 credits, 1 private IP | Credit model, private IP | Webhook event list not published on the pages checked | 2026-10-13 |
| EmailBison | Base, $599 a month: 500,000 sends, dedicated IPs | Built for high volume | Six times the volume needed, over budget | 2026-10-13 |
| HubSpot sequences | Needs Sales Hub Professional or Enterprise seats | Native CRM | No warmup; Kestrel's HubSpot has no Sales Hub Professional seats | 2026-10-13 |

Decision: Instantly Hypergrowth, monthly billing until the campaign proves out, then yearly ($77.60 a month).

## Workspace Settings

| Setting | Value | Source |
|-|-|-|
| Daily limit per mailbox | 30 | `inbox-setup` ramp, steady row; primer cap |
| Campaign daily limit | People 240, Store inbox 84, Catch-all 36 (10% of 360) | 12 mailboxes x 30 = 360 |
| Schedule | Monday to Friday, 08:00 to 17:00; two schedules, America/New_York and America/Denver, split by store state | `inbox-setup` sending rules |
| Open tracking | Off | Apple Mail Privacy Protection inflates opens |
| Link tracking | Off; no links in touch 1 | `cold-email-copywriting` |
| Unsubscribe header | On: Settings, Advanced settings, Sending rules, "Insert unsubscribe link header"; confirmed `List-Unsubscribe` in a raw test message | Instantly help, checked 2026-10-13 |
| Stop on reply | On | Instantly campaign default, checked |
| Bounce auto-pause | On (Instantly default above 5% after 200 sends); 2% house line watched weekly | `email-deliverability` |
| Verify Leads on upload | Off; file already validated with `validate_emails` | Avoids 0.25 credits per lead on top |

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

| Step | Action | Result |
|-|-|-|
| 1 | `check_wallet`: $212.40 balance, Growth plan | Approved spend of $17.92 |
| 2 | `scrape_store_leads` test, `totalLeads` 100, `offset` 0 | 100 stores, $0.39; filters confirmed on 10 sampled rows |
| 3 | `scrape_store_leads` remaining 1,400 with `offset` 100 to 1,400 in steps of 100 | 1,500 stores in total, $5.85 including the test |
| 4 | Suppress 14 HubSpot customer domains | 1,486 stores |
| 5 | `query_lead_database` with `companyDomain` in 15 batches of up to 100 domains, founder and ecommerce titles, `hasEmail` true, `excludeDelivered` true | 1,236 people at 990 stores; capped at 2 per domain: 1,180 kept |
| 6 | Store inbox file for the 496 stores with no person | 496 rows, all role addresses, own campaign |
| 7 | Dedupe on lowercased email across both files and against the Instantly workspace | 0 duplicates (new workspace) |
| 8 | `validate_emails` on 1,676 addresses | People: 1,002 valid, 121 catch-all, 19 unknown, 36 invalid, 2 disposable. Store inboxes: 401 valid, 63 catch-all, 9 unknown, 22 invalid, 1 disposable. $12.07 |
| 9 | Split: People (1,002), Store inbox (401), Catch-all (184), Hold unknown (28), Suppress (61) | 1,587 rows to upload |
| 10 | Upload three CSVs into paused campaigns, "Check for Duplicates Across All Campaigns/Lists" on | Instantly reported 0 existing, 0 invalid, 0 blocklisted; 1,587 imported |
| 11 | Preview 10 renders per campaign, including 2 with fallbacks | No raw `{{`, no "Hi ," |
| 12 | Start on Wednesday 2026-10-14 at the campaign limits above | Sends logged |

## Suppression and Dedupe

| List | Match on | Where it lives | Sync |
|-|-|-|-|
| Customers | Domain (14) | Instantly Blocklist, HubSpot lifecycle stage "Customer" | Re-exported from HubSpot before each import |
| Past unsubscribes from the previous tool | Email (37) | Instantly Blocklist | Loaded once on 2026-10-13 |
| Competitor agencies | Domain (22) | Instantly Blocklist | Kept by the founder |
| New unsubscribes and "remove me" replies | Email, or domain if asked | Instantly Blocklist and HubSpot email opt-out | n8n flow on `lead_unsubscribed` plus same-day manual add for reply opt-outs |
| Hard bounces | Email | Instantly Blocklist | n8n flow on `email_bounced` |
| Already pulled from ScraperCity | Lead Database records | `excludeDelivered` on every database call | Automatic |

## Webhooks to CRM

One Instantly webhook (all campaigns) posts to n8n with a custom header `X-Kestrel-Token`; n8n answers 200 at once, then writes to HubSpot with a batch upsert keyed on email.

| Business event | Platform event | CRM action | Sequencer action |
|-|-|-|-|
| Replied | `reply_received` | Upsert contact by email; log the reply as a note; lead status "Replied" | Stops for that lead (default); rep removes the second contact at the same store by hand |
| Interested | `lead_interested` | Create a deal in "Discovery", owner Mara Lind | None |
| Meeting booked | `lead_meeting_booked` | Move the deal to "Meeting booked" | Remove other contacts at the domain from all campaigns |
| Unsubscribed | `lead_unsubscribed` | Set email opt-out on the contact | Add email to the Instantly Blocklist (already unsubscribed in Instantly; the flow keeps HubSpot in step) |
| Bounced | `email_bounced` | Mark the email invalid on the contact | Add to the Instantly Blocklist |
| Account error | `account_error` | None | Slack alert to ops; reconnect the mailbox |

## Test Plan

| Test | Pass when | Result |
|-|-|-|
| Seed send from 4 mailboxes (one per domain) | Inbox at Gmail, Workspace, Outlook.com and Microsoft 365 seeds | Pass, 2026-10-13 |
| Render preview with an empty `first_name` row | Reads "Hi there," with no raw tags | Pass |
| Test reply from a seed | HubSpot contact created once, note logged, status "Replied" | Pass, one record |
| Test unsubscribe from a seed | Instantly Blocklist and HubSpot opt-out within 1 hour | Pass, 3 minutes |
| Receiver stopped for 10 minutes during a test reply | Gap visible in the n8n execution log; status reconciled from Instantly lead status the same day | Pass |
| Raw headers of a test message | `List-Unsubscribe` present; `dkim=pass` for the sending domain | Pass |

## Cost

| Line | Count | Unit price | Monthly |
|-|-|-|-|
| Instantly Hypergrowth | 1 workspace | $97 a month | $97.00 |
| ScraperCity Growth plan (Lead Database) | 1 | $149 a month | $149.00 |
| `scrape_store_leads` | 1,500 stores | $0.0039 | $5.85 |
| `validate_emails` | 1,676 | $0.0072 | $12.07 |
| n8n and HubSpot | Existing | $0 | $0.00 |
| Total | | | $263.92 |
