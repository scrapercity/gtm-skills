# Sending Platform Plan: Corvid Lane (4 clients)

Illustrative example: Corvid Lane, its four clients and every domain below are invented. Prepared 2026-10-13 for Corvid Lane, a three-person outbound agency. Vendor pages checked 2026-10-13. Assumed: the current tool's name and the recipient time zone split; everything else was answered on the kickoff call on 2026-10-12.

## Summary

Use Smartlead Pro with four client workspaces: $94 + 4 x $29 = $210 a month on monthly billing, inside Corvid's $250 sequencer budget. It is the cheapest option checked that gives each client its own campaigns, mailboxes, block list, webhook and login inside one agency account. Corvid's 36 warmed Google mailboxes are reconnected, not replaced, and carry 1,000 sends a day at 30 each. Four client-level webhooks feed one n8n flow that writes replies, deals, meetings, opt-outs and bounces into each client's own HubSpot portal. The sending stack costs $523.48 a month, about $130.87 per client.

## Assumptions and Open Questions

| Question | Answer | Answered by user or assumed |
|-|-|-|
| HubSpot portals: one, or one per client | One per client (4), plus Corvid's own portal for billing | Answered |
| Client logins needed | Palisade HR and Quillmark Legal want read-only access to their campaigns and positive replies | Answered |
| Inbox mix (Google, Microsoft, other) | 36 Google Workspace mailboxes on 12 domains, already sending about 1,000 a day; no Microsoft senders | Answered |
| Current sending tool | Not named; Corvid sends from it today and leaves it once Smartlead is live | Assumed: none named, so the switch steps sit in the Import Procedure |
| Monthly budget ceiling, all-in | $250 a month for the sequencer; each client pays its own mailboxes and domains | Answered |
| Recipient time zones | Eastern and Central to an East campaign, Mountain and Pacific to a West campaign | Assumed from the first pull |
| Data source | ScraperCity Lead Database on the Growth plan Corvid already pays for | Answered |

## Requirements

| Input | Value | Source |
|-|-|-|
| New prospects per day | 333 (83 per client) | 1,000 sends a day / 3 steps at steady state |
| Steps per sequence | 3 (day 0, day 3, day 7, business days) | Client copy plans |
| Contacts per month (month 1 and month 2) | About 7,000 each; 14,000 stored after month 2 | 333 x 21 sending days, cumulative |
| Sends per month (month 1 and month 2) | Up to 21,000 each | 1,000 x 21 |
| Mailboxes connected | 36 existing on 12 domains; per client 9 x 30 = 270 a day against 250 needed | Corvid's roster |
| Seats and workspaces | 3 Corvid staff: Priya Nand (founder), Jules Okafor (client lead), Rafa Ibarra (ops). No seat limit stated on Smartlead's pricing page, which says pricing is "not per seat"; confirmed in the app trial on 2026-10-13 | Smartlead pricing page |
| Client workspaces | 4 (Ferrous Labs, Quillmark Legal, Palisade HR, Ostrava Freight) | Signed clients |
| CRM and middleware | 4 client HubSpot portals; n8n self-hosted on Corvid's server | Corvid |

## Platform Decision

| Option | Plan and price | Fits because | Gaps | Checked |
|-|-|-|-|-|
| Smartlead Pro + 4 client workspaces | $94 + 4 x $29 = $210 a month: 30,000 stored contacts, 90,000 emails, unlimited mailboxes, API and webhooks | Client workspaces with logins, client-scoped block lists and client-level webhooks; inside budget | 30,000 stored contacts is cumulative across clients | 2026-10-13 |
| Smartlead Unlimited Smart + 4 client workspaces | $174 + 4 x $29 = $290 a month: unlimited contacts, 150,000 emails | Removes the contact cap | Over today's sequencer budget | 2026-10-13 |
| Instantly, 4 Hypergrowth workspaces | 4 x $97 = $388 a month (each workspace is its own subscription) | Fully separate workspaces; webhooks and staff invites from Hypergrowth | Over budget | 2026-10-13 |
| Instantly, 4 Growth workspaces | 4 x $47 = $188 a month | Cheapest | 1,000 contacts per workspace against 1,750 per client in month 1; no webhooks; no staff invites | 2026-10-13 |
| Lemlist Email | $69 per user a month | CRM integrations on every plan | No client workspaces: one block list and one webhook set for all four clients; one account per client is 4 x $69 = $276 a month at one user each | 2026-10-13 |
| EmailBison Base | $599 a month, 500,000 sends, dedicated IPs | Built for agency volume | 24 times the volume needed, over budget | 2026-10-13 |
| HubSpot sequences in each client portal | Sales Hub Professional seats; seat price not checked | No sync to build | 500 sequence emails a day per Professional seat; no warmup; one sequence per contact at a time | 2026-10-13 |

Decision: Smartlead Pro with 4 client workspaces on monthly billing. Instantly on 4 Hypergrowth workspaces ($388) costs $178 more than Smartlead Pro with 4 client workspaces ($210) for the same sending.

Revisit if: stored contacts pass 25,000 (the step is costed under Cost), or a client demands a fully separate account, which favors an Instantly workspace for that client alone.

## Workspace Settings

Applied to all 8 campaigns (one East and one West campaign per client).

| Setting | Value | Source |
|-|-|-|
| Daily limit per mailbox | 30 cold sends; account `max_email_per_day` 40, because Smartlead counts warmup (10 a day) and campaign mail together | Alex Berman: under 50 a day per inbox; Smartlead API reference |
| Gap between emails | `time_to_wait_in_mins` 18 per mailbox | 540-minute window / 30 |
| Campaign daily limit | East 170 and West 80 per client; max 56 new leads a day East, 27 West | 68% of the first pull is Eastern or Central |
| Schedule | Monday to Friday, 08:00 to 17:00; East in America/New_York, West in America/Denver | Recipient time zones |
| Plain text | On (`send_as_plain_text`) | No images or links in step 1 |
| Open tracking | Off (`DONT_TRACK_EMAIL_OPEN`) | Apple Mail Privacy Protection records opens nobody made |
| Link tracking | Off (`DONT_TRACK_LINK_CLICK`) | No tracking domains set up |
| Unsubscribe header | On: Campaign Settings > Unsubscribe > "Add unsubscribe message in all emails", plus a plain opt-out line in each step | Smartlead help article 27: adds the one-click header |
| Stop on reply | On for the lead; other leads at the same domain paused (`auto_pause_domain_leads_on_reply`) | Smartlead settings |
| Out-of-office replies | Not counted as replies; lead reactivated after the return date (`ignoreOOOasReply`, `autoReactivateOOO`) | Smartlead settings |
| Provider matching | Off: all senders are Google. The week-1 validator `sc_mx_provider` mix is reported per client, and Corvid decides per client whether to add Microsoft 365 senders | Corvid |
| Bounce auto-pause | 2%: campaign SETUP > "High Bounce Rate Auto Protection", type 2. Account settings > Warning Notifications sends the pause to n8n, which alerts Rafa | Alex Berman: hard bounces under 2%; Smartlead help articles 274 and 210 |
| Client assignment (agency only) | `client_id` on every campaign and on each client's 9 mailboxes | Smartlead agency view |
| Campaign names | `{ClientCode}_{Segment}_{ListSource}_{YYYYMM}`, for example `FRX_OpsLeaders_LeadDB_202610`; n8n splits them into HubSpot properties | Corvid |
| Platform verification | Off; files validated before upload | Avoids paying twice |

## Column Map

| Source | Source column | Platform variable | Merge tag | Fallback |
|-|-|-|-|-|
| Lead Database | `email` | `email` | none | Required; rows without one are dropped |
| Lead Database | `first_name` | `first_name` | `{{first_name}}` | "there" |
| Lead Database | `last_name` | `last_name` | none | Not used in copy |
| Lead Database | `company_name` | `company_name` | `{{company_name}}` | "your team" |
| Lead Database | `company_domain` | `website` | none | Not used in copy |
| Lead Database | `title` | custom field `title_short` | `{{title_short}}` | "your role" |
| Lead Database | `linkedin_url` | `linkedin_profile` | none | Not used in copy |
| Lead Database | `company_industry` | custom field `industry_plain` | `{{industry_plain}}` | Rows without it get the variant without the industry line |
| Lead Database | `state` | custom field `prospect_state` | none | Blank rows go to the East campaign |
| Email Validator | `email_quality` | custom field `email_quality` | none | Send order only |

## Import Procedure

Steps 1 to 7 run once; steps 8 to 13 run per client every Monday.

| Step | Action | Owner | Due | Pass when |
|-|-|-|-|-|
| 1 | Smartlead: Client Access Dashboard > Add Client, once per client; logins only for Palisade HR and Quillmark Legal, showing the Interested and Meeting Request categories | Priya Nand | 2026-10-14 | 4 clients listed with their ids |
| 2 | Export the old tool's unsubscribes, bounces and every contacted prospect. Load unsubscribes and bounces into every client's block list and the no-client list (`POST /api/v1/leads/add-domain-block-list` with `client_id`, bare domains); contacted prospects go into Corvid's master contacted list | Rafa Ibarra | 2026-10-14 | Entry count per client equals the export |
| 3 | Load each client's customers, open deals and competitors into its own block list | Jules Okafor | 2026-10-15 | Entry count per client equals its file |
| 4 | From 2026-10-15 no new prospect enters the old tool; mid-sequence prospects finish their remaining steps there at 10 a day per mailbox | Rafa Ibarra | 2026-10-15 | Old tool shows 0 active prospects by 2026-10-24 |
| 5 | Reconnect the 36 existing mailboxes to Smartlead by OAuth (Email Accounts > account > Management: client, `max_email_per_day` 40 from 2026-10-25, 30 during the overlap). Turn warmup off in the old tool, then on in Smartlead the same day, 10 a day | Rafa Ibarra | 2026-10-15 | Every account read back with its client, cap and warmup |
| 6 | In each client's HubSpot: a private app (scopes `crm.objects.contacts.write`, `crm.objects.deals.write`, `communication_preferences.write`), token stored in n8n under the client's name; properties `cold_email_status`, `cold_campaign`, `cold_sequence_step`, `cold_segment`, `cold_list_source`; pipeline "Outbound" with Positive reply, Meeting booked, Meeting held, No-show, Closed lost; deal property `corvid_client` | Jules Okafor | 2026-10-16 | Test upsert returns 200 in each portal |
| 7 | Create 8 campaigns with the settings above, paused; create the 4 client-level webhooks | Rafa Ibarra | 2026-10-16 | Each campaign read back with its client, settings and mailboxes |
| 8 | Pull new prospects per client: `GET https://app.scrapercity.com/api/v1/database/leads` with the client's saved title and industry filters, `excludeDelivered=true`, 100 per page, paged with `after` | Rafa Ibarra | 2026-10-19 | About 460 rows per client for week 1 |
| 9 | Dedupe on lowercased email against Corvid's master contacted list across all four clients | Rafa Ibarra | 2026-10-19 | 0 duplicates; an overlap goes to the client that signed first |
| 10 | Validate every row: ScraperCity Email Validator, `POST https://app.scrapercity.com/api/v1/scrape/email-validator` with the file's emails | Rafa Ibarra | 2026-10-20 | Main files 100% `valid`; catch-alls in their own campaign at 10% of daily volume or less (Corvid's setting) |
| 11 | Upload 100 leads per call (`POST /api/v1/campaigns/{id}/leads`) with all four `ignore_*` settings false | Rafa Ibarra | 2026-10-20 | `added_count` + `skipped_count` = rows sent; every skip explained |
| 12 | Preview 10 renders per campaign, 2 with fallbacks | Jules Okafor | 2026-10-20 | No raw tags, no "Hi ," |
| 13 | Start all 8 campaigns (`POST /api/v1/campaigns/{id}/status`, `ACTIVE`) after the Test Plan passes | Priya Nand | 2026-10-22 | Day-1 sends match the overlap caps |

## Suppression and Dedupe

| List | Match on | Where it lives | Sync |
|-|-|-|-|
| Client customers and open deals | Domain | Smartlead block list per client (`client_id`) | Re-exported from each client's HubSpot every Monday before import |
| Client competitors | Domain | Smartlead block list per client | Kept by Jules with each client |
| Link unsubscribes | Email | Smartlead marks the lead unsubscribed across all future campaigns, every client (help article 27) | n8n on `LEAD_UNSUBSCRIBED` updates that client's portal the same day |
| Opt-outs by reply | Email, or domain if asked | That client's block list; a "remove me from everything" reply or one naming Corvid goes onto every client's list and the no-client list | Same-day manual add by Jules |
| Hard bounces and spam complaints | Email | Every client's block list and the no-client list | n8n on `EMAIL_BOUNCE`, same day |
| Old tool's history | Email | Unsubscribes and bounces in every block list; contacted prospects in the master list | Loaded once in step 2 |
| Cross-client overlap | Email | Corvid's master contacted list | Checked before every upload; a prospect in one client's active sequence is skipped for the others until 60 days after it ends (the top of Alex Berman's 30 to 60 days) |

## Webhooks to CRM

Four client-level Smartlead webhooks (one per `client_id`, no user-level webhook, since a user-level one overrides them) post to one n8n URL. n8n answers 200 at once (Smartlead's webhooks reference retries after 1 minute, 5 minutes, 15 minutes, 1 hour and 6 hours and disables a webhook after 5 failed attempts; checked 2026-10-13), verifies `X-Smartlead-Signature`, dedupes on `X-Request-Id`, and writes with that client's token only; an unknown client goes to an error queue. Contacts it creates stay non-marketing, HubSpot's default for API-created contacts, so they do not count toward any client's contact tier.

Writer per event: the n8n webhook flow for every event. Smartlead's native HubSpot integration stays off, because its help page does not say one Smartlead account can connect a different portal per client.

| Business event | Platform event | Writer | CRM action | Sequencer action |
|-|-|-|-|-|
| Replied | `EMAIL_REPLY` | n8n webhook flow | Upsert the contact by email in the client's portal; log the reply as an incoming email engagement; set `cold_campaign`, `cold_sequence_step` (from `sequence_number`), `cold_segment` and `cold_list_source` | Lead stops; other leads at the domain paused |
| Interested or asked for a meeting | `LEAD_CATEGORY_UPDATED`, filtered to Interested and Meeting Request | n8n webhook flow | Create a deal at Positive reply with `corvid_client`, owned by the client's AE; skip if one is open | None |
| Meeting booked | Booking on the client AE's HubSpot scheduling page, read by n8n from the meetings API | n8n flow | Move the deal to Meeting booked with the meeting date; write a thin record (company, client, date, stage) to Corvid's portal | Remove other leads at the domain from the client's campaigns |
| Meeting held or No-show | Meeting outcome the AE sets after the call (`hs_meeting_outcome` completed or no show) | n8n flow | Move the deal to Meeting held or No-show in both portals; Meeting held is the billable meeting | None |
| Unsubscribed | `LEAD_UNSUBSCRIBED` | n8n webhook flow | Unsubscribe the contact from all email in the client's portal through the communication preferences API | Already unsubscribed in Smartlead for every client |
| Bounced | `EMAIL_BOUNCE` | n8n webhook flow | Set `cold_email_status` to bounced in the client's portal | Add to every client's block list and the no-client list |
| Mailbox disconnected or campaign paused | Per-user disconnect alert; bounce threshold webhook | n8n webhook flow | None: no CRM write | Alert Rafa in Slack |

Positive replies: Jules Okafor answers every Interested and Meeting Request reply from Smartlead's Master Inbox with the client AE's booking link. n8n posts each one to #replies with its reply time, and the Monday review reports the median reply-to-answer time per client.

## Test Plan

| Test | Pass when | Owner | Due |
|-|-|-|-|
| Seed send from one mailbox per domain (12 sends) | Inbox at Gmail, Workspace, Outlook.com and Microsoft 365 seeds | Rafa Ibarra | 2026-10-20 |
| Raw headers of a test message per client | `List-Unsubscribe` present; `dkim=pass` for the sending domain | Rafa Ibarra | 2026-10-20 |
| Test reply into each client's campaign | One contact and one incoming email in that client's portal, with campaign, step, segment and list source set; nothing in the other three portals | Rafa Ibarra | 2026-10-21 |
| Interested, then a booking on Ferrous Labs' scheduling page, then outcome No show | One deal: Positive reply, then Meeting booked, then No-show; no second deal | Jules Okafor | 2026-10-21 |
| Test unsubscribe through the Smartlead link | Contact unsubscribed from all email in that client's portal within 1 hour | Rafa Ibarra | 2026-10-21 |
| Client-scoped block | A seed address blocked for Ferrous Labs only is skipped by Ferrous Labs and accepted by Quillmark Legal | Rafa Ibarra | 2026-10-21 |
| Receiver stopped for 10 minutes during a test reply | Retries arrive and the contact is written once | Rafa Ibarra | 2026-10-21 |
| Client logins | Palisade HR and Quillmark Legal each see only their own campaigns and the two categories | Jules Okafor | 2026-10-21 |
| Weekly reconciliation | Every Interested and Meeting Request lead Smartlead shows for the week has a deal in its client's portal; gaps replayed and explained | Rafa Ibarra | 2026-10-30 |

## Cost

Mailbox price from Google's Workspace billing help (Business Starter, Flexible plan) and domain price from porkbun.com, both checked 2026-10-13.

| Line | Count | Unit price | Monthly |
|-|-|-|-|
| Sequencer: Smartlead Pro | 1 | $94 a month | $94.00 |
| Client workspaces | 4 x $29 | $29 a month | $116.00 |
| Mailboxes: Google Workspace Business Starter, existing, reconnected | 36 | $8.40 a month | $302.40 |
| Domains: `.com`, existing | 12 | $11.08 a year | $11.08 |
| Automation: n8n self-hosted on an existing server | 1 | $0 extra | $0.00 |
| Total | | | $523.48 |

At 7,000 new contacts a month the stored total passes Pro's 30,000 in month 5 (about February 2027), unless Smartlead confirms that each client workspace has its own allowance or that deleting finished leads frees the cap. From that month Unlimited Smart with 4 workspaces is $290, and the total becomes $603.48.

Optional, outside the total: the ScraperCity Growth plan Corvid already pays ($149 a month) and validation of about 7,700 rows a month at $0.00169 ($13.01).
