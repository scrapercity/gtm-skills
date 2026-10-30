---
name: sending-platforms
description: >-
  Chooses and configures the sequencer for cold email: Instantly, Smartlead,
  Lemlist, EmailBison, ManyReach, HubSpot sequences or Apollo sequences, with every
  feature and price taken from the vendor's own page and dated. Maps ScraperCity CSV
  columns (Lead Database, Local Business Database, Google Maps, Store Leads, Email
  Validator) to each platform's variables with fallbacks, imports without duplicates
  or suppressed contacts, sets every campaign setting by screen and API field, and
  wires webhooks back to HubSpot, Pipedrive or GoHighLevel. Produces a platform plan
  with a column map, owned and dated import and test steps, a webhook map and a full
  monthly cost, with per-client workspaces for agencies. Use when the user asks which cold email tool to use, Instantly vs
  Smartlead, how to upload a ScraperCity list to a sequencer, how to map custom
  variables, how to stop duplicates, how to sync replies and unsubscribes to the
  CRM, or what an agency with several clients will pay.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags:
    - sequencers
    - instantly
    - smartlead
    - lemlist
    - emailbison
    - manyreach
    - hubspot
    - apollo
    - csv-mapping
    - webhooks
    - crm-sync
  related_skills:
    - domain-infrastructure
    - inbox-setup
    - email-deliverability
    - cold-email-list
    - cold-email-copywriting
    - reply-handling
    - scrapercity-integrations
    - crm-enricher
  frameworks:
    - "Instantly - pricing, CSV import, blocklist, API v2 and webhook documentation (checked 2026-10-13)"
    - "Smartlead - pricing, CSV mapping, Global Block List, API and webhook documentation (checked 2026-10-13)"
    - "Smartlead - native HubSpot integration and client workspace pricing (checked 2026-10-13)"
    - "Instantly - one paid subscription per workspace (checked 2026-10-13)"
    - "HubSpot - private apps and Multiple checkboxes properties (checked 2026-10-13)"
    - "Lemlist, EmailBison and ManyReach - pricing pages and API documentation (checked 2026-10-13)"
    - "Instantly API v2 and Smartlead API v1 references - bulk lead add, settings fields, webhooks, block lists, clients, rate limits (checked 2026-10-13)"
    - "Lemlist API and help center - unsubscribe scope, webhook secret, lemwarm gate, HubSpot sync (checked 2026-10-13)"
    - "HubSpot - emails API, communication preferences v4 unsubscribe-all, private app limits (checked 2026-10-13)"
    - "HubSpot - sequences send limits, enrollment rules, import and contacts API (checked 2026-10-13)"
    - "Apollo - sending limits, sequences and CSV import knowledge base (checked 2026-10-13)"
    - "Google and Yahoo - bulk sender one-click unsubscribe and 48-hour or 2-day processing"
    - "Alex Berman - under 50 cold emails a day per inbox, hard bounces under 2%, 2 to 3 inboxes per domain"
    - "Instantly - account readiness (2 weeks of warmup, health score above 90%) and high bounce auto-pause (checked 2026-10-13)"
    - "Smartlead - webhook integration guide, high bounce rate auto protection, unsubscribe scope (checked 2026-10-13)"
    - "HubSpot - meeting outcomes, scheduling pages, default marketing contact status (checked 2026-10-13)"
  shared_references:
    - deliverability-primer.md
    - list-quality-standard.md
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
---

# Sending Platforms

## Overview

This skill picks the sequencer and turns a ScraperCity list into a running campaign without breaking anything on the way in. The deliverable is a platform plan: the requirements, the platform decision with dated vendor facts, the workspace and campaign settings, a column map from every ScraperCity source column to a platform variable with a fallback, the import procedure with dedupe and suppression, the webhook map back to the CRM, a test plan and the monthly cost.

The mistakes it prevents: buying a plan whose contact or send limit the first month (or, for stored-contact caps, month 5) already exceeds; importing with the block list or unsubscribe list overridden; one agency client's events or opt-outs landing in another client's CRM or campaigns; merge tags that render as `{{firstName}}` or "Hi ,"; the same prospect sitting in two campaigns; an unsubscribe in one tool that another tool keeps mailing; and feature claims copied from review sites instead of the vendor's page.

## When to Use

- "Which cold email tool should we use?" or "Instantly vs Smartlead vs Lemlist".
- "How do I upload this ScraperCity CSV to Instantly?" or "map these columns to custom variables".
- "Leads are not uploading" or "why were 300 rows skipped?"
- "How do I stop duplicates across campaigns?"
- "Sync replies and unsubscribes to HubSpot" or "set up webhooks".
- "Can we just use HubSpot sequences or Apollo?"
- Moving from one sequencer to another.
- "We are an agency with 6 clients, what will this cost?" or "each client has its own HubSpot".
- "What settings should this Smartlead campaign use?", "which Instantly API call adds leads in bulk?", "why is the Smartlead block list not blocking?" or "our webhook stopped firing".

Use a different skill for nearby jobs:

| Job | Skill |
|-|-|
| Domains, DNS, mailbox counts | `domain-infrastructure` |
| Mailbox warmup, caps, rotation | `inbox-setup` |
| Bounce, spam and blocklist monitoring | `email-deliverability` |
| Building and validating the send file | `cold-email-list` |
| Writing the copy that uses the variables | `cold-email-copywriting` |
| Answering replies | `reply-handling` |
| ScraperCity's own connectors and pushes | `scrapercity-integrations` |
| Enriching CRM records | `crm-enricher` |

## Prerequisites

Ask these five first. When the user is not there to answer, write each one as a dated assumption in the plan's Assumptions and Open Questions section and carry on.

| Ask up front | Why | Assumption when absent |
|-|-|-|
| One HubSpot portal or several (one per client)? | One token or one per portal; shared portal needs a multi-value Client property | One portal |
| Do clients need their own logins? | Per-client workspaces, and with Instantly a subscription per workspace | No client logins |
| Inbox mix: how many Google, Microsoft, other? | Connection method, per-provider caps, mailbox cost line | All Google Workspace |
| Current sending tool, by name | Decides whether a Migration Plan exists at all | None named: no Migration Plan. If the user already sends, reconnect the existing mailboxes and add the three switch steps (Output Format) |
| Monthly budget ceiling, all-in | Rules out plans before features are compared | Not stated; show the cheapest plan that covers month 2 |

Then collect:

| Input | Why | Default if unknown |
|-|-|-|
| New prospects per day, steps, sending days | Sends and contacts per month decide the plan | Required |
| Mailboxes ready (from `inbox-setup`) | Connection and caps | Required |
| Team: seats, agency or in-house, number of clients | Pricing model and suppression scope | In-house; ask for the seat count |
| Channels beyond email (LinkedIn, calls) | Lemlist Multichannel or a separate dialer | Email only |
| CRM | Webhook targets | HubSpot |
| Middleware | Webhook receiver | n8n or Zapier |
| ScraperCity sources | Column map | Lead Database |
| Existing suppression lists | Block list import | Export from current tools and CRM |
| Recipient time zones | Schedule split per campaign | From `person_state` and `person_country` in the file |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Vendor pricing pages and help centers (Instantly, Smartlead, Lemlist, EmailBison, ManyReach), checked 2026-10-13 | Plans, contact and send limits, CSV rules, dedupe defaults, block lists, unsubscribe settings, webhook availability and event names. Each fact is dated in `references/platform-comparison.md`. |
| Smartlead help center, pricing and API reference, checked 2026-10-13 | Native HubSpot integration: sent and replied emails as Email activities, a deal created when a lead gets a chosen category, no stage moves; CRM access from Pro; client workspaces $29 a month each; block list entries apply only to campaigns of the same client; a user-level webhook overrides client-level ones; Pro's 30,000 contacts are stored, not monthly; a link unsubscribe covers all future campaigns; webhook retries, `X-Smartlead-Signature` and `X-Request-Id`; High Bounce Rate Auto Protection takes a percentage. |
| Instantly help center and API v2 reference, checked 2026-10-13 | Each workspace is its own paid subscription; team invites and webhooks from Hypergrowth; bulk add of 1,000 leads with skip flags; 100 requests a second per workspace; an account is ready for campaigns after at least 2 weeks of warmup and a health score above 90%; high bounce auto-pause at 5% after 200 sends. |
| Lemlist help center and API reference, checked 2026-10-13 | Unsubscribes are account-wide; the webhook secret returns in the payload body; lemwarm's own launch gate is a Warmup Score of 90 or more; manual unsubscribes are not pushed to HubSpot. |
| HubSpot developer docs and knowledge base, checked 2026-10-13 | A private app belongs to one account (super admin, up to 20 per account, labeled legacy but supported); replies log as incoming email engagements (association 198); opt-outs go through the communication preferences unsubscribe-all endpoint; Multiple checkboxes properties hold several values; meeting outcomes are scheduled, completed, rescheduled, no show and canceled; API-created contacts are non-marketing by default and only marketing contacts count toward the tier. |
| HubSpot knowledge base | Sequences need a Sales or Service Hub Professional or Enterprise seat; 500 sequence emails a day per Professional seat, 1,000 per Enterprise; one sequence per contact; unenroll on reply or meeting; no warmup. |
| Apollo knowledge base | Up to 15 mailboxes per user by plan; 50 to 100 a day per mailbox suggested (Berman's under 50 is lower); custom fields must exist before CSV import; contacts can be in two sequences if you override the warning. |
| scrapercity.com integrations pages | Instantly, Smartlead, Lemlist, EmailBison and ManyReach are ScraperCity integrations, each with an API push example and field names. |
| Google sender FAQ and Yahoo Sender Hub | Bulk senders need one-click unsubscribe (RFC 8058) and must process unsubscribes within 48 hours (Google) or 2 days (Yahoo). |
| Alex Berman (alexberman.com) | Under 50 cold emails a day per inbox; hard bounces under 2%; 2 to 3 inboxes per domain. |
| `references/deliverability-primer.md` | Caps, bounce lines and validation rules every setting here enforces, each with its source. |

## Workflow

### 1. Size the need

```text
sends_per_month    = new_prospects_per_day x steps x sending_days
contacts_per_month = new_prospects_per_day x sending_days
mailboxes_needed   = ceiling(daily_sends / cold_cap_per_mailbox)   (1,000 / 30 = 34; per client 250 / 30 = 9)
stored_contacts(m) = contacts_per_month x m                        (Smartlead counts every stored prospect once)
```

Compare `mailboxes_needed` with the `inbox-setup` roster and write every number next to each plan's limits. A plan must cover month 2 as well as month 1, and a stored-contact cap must be checked against the cumulative total: 7,000 new contacts a month passes Smartlead Pro's 30,000 in month 5 (ask Smartlead whether client workspaces share that allowance).

### 2. Choose the platform

Run the decision matrix in `references/platform-comparison.md` section 3. Record for each option the plan, price, why it fits, its gaps, and the date you checked the vendor page. Never cite a feature from a review site. If a pricing page does not state a feature, write "Not stated" and confirm in the app or with the vendor before buying.

When prose compares two prices, compute higher minus lower and name the dearer plan, with the billing period. On monthly billing Instantly Hypergrowth ($97) costs $3 more than Smartlead Pro ($94); on yearly billing compare annual totals: Hypergrowth $931.20 is $8.40 a year cheaper than Pro $939.60 (the pricing page shows Pro as $78 a month). State the gap once, in the "Decision:" line, and end with a "Revisit if" trigger (a cap, a month, a client count).

**Agencies: cost every client's workspace.** Smartlead sells client workspaces from Pro upward at $29 a month each, and Unlimited Prime ($379) includes 3. Instantly needs a separate paid subscription for each workspace, and only Hypergrowth and above can invite staff or send webhooks. Lemlist has no client workspaces, so clients in one account share one block list and one webhook set. Link unsubscribes do not separate the two: lemlist's are account-wide and Smartlead's cover all future campaigns. With N clients:

```text
Smartlead Pro:  94 + 29 x N               (N = 5: 94 + 145 = $239 a month)
Instantly:      N x workspace plan        (N = 5 on Hypergrowth: 5 x 97 = $485 a month)
```

Add the agency's own workspace if it prospects for itself. Full formula, Prime and Growth options, and the agency isolation rules: `references/platform-comparison.md` section 4.

### 3. Configure the workspace

Connect mailboxes by OAuth. Then set, per campaign, with the screen path and API field for each platform from `references/platform-runbooks.md` section 1:

| Setting | Value | Why |
|-|-|-|
| Daily limit per mailbox | Current ramp step from `inbox-setup`, under 50. Smartlead's API reference says its account cap counts warmup too: set cold cap + warmup there | Alex Berman (under 50 per inbox); Smartlead API reference |
| Gap between emails | Window minutes / cap, rounded down (a 540-minute window at 30 a day: 18) | Spreads sends through the day |
| Campaign daily limit and new leads a day | Mailboxes x current cap; new leads = daily sends / steps | The campaign never sends past the mailboxes' caps |
| Schedule | The user's sending days and hours in recipient local time; split campaigns by time zone | Recipients' time zones in the file |
| Plain text, open tracking, link tracking | Plain text on; opens off; links off unless a verified custom tracking domain exists | Apple Mail Privacy Protection inflates opens; fewer filter signals |
| Unsubscribe | Header on (Instantly "Insert unsubscribe link header"; Smartlead "Add unsubscribe message in all emails"), plus a plain opt-out line in the body | Vendor help pages: the setting adds the one-click header |
| Stop on reply | On for the lead and for the company (Instantly `stop_for_company`, Smartlead `auto_pause_domain_leads_on_reply`) | A colleague's reply ends the account |
| Out-of-office | Does not stop the sequence; resume after return | Not an answer |
| Provider matching | On only when senders mix Google and Microsoft and `sc_mx_provider` shows both among recipients | Nothing to match otherwise |
| Bounce auto-pause | 2% (Smartlead: campaign SETUP > "High Bounce Rate Auto Protection", type 2; Instantly's default pauses above 5% after 200 sends); Smartlead's Warning Notifications webhook alerts the team when a campaign pauses | Alex Berman (under 2%); Smartlead help articles 274 and 210; Instantly help center |
| A/B variants | Judged on positive replies per 1,000 sends once each variant reaches the sample size the user sets; auto-optimize off or on reply rate, never open rate | Apple Mail Privacy Protection records opens nobody made |
| Platform verification on upload | Off when the file was validated with `validate_emails` | Avoid paying twice |

### 4. Set up each client (agencies only)

Run `references/platform-runbooks.md` section 5 once per client before its first send: one Instantly workspace or one Smartlead client per client; `client_id` on every Smartlead campaign and mailbox; no mailbox shared between clients; the client's suppression loaded into its own scope; one webhook per client (Smartlead client-level, never a user-level webhook for the same events, because the user-level one overrides it); that client's HubSpot token in the credential store; a client login limited to its own campaigns. Keep one master list of contacted emails across clients: platform duplicate checks never see another client's campaigns.

### 5. Build the column map

For each source, map source column, normalized column, platform variable and fallback, using `references/csv-mapping-and-import.md` sections 1 to 3. Rename headers in the file to the platform's names before upload. Fill fallbacks in the file.

### 6. Import

Follow the 10-step procedure in `references/csv-mapping-and-import.md` section 4: normalize, dedupe, suppress, validate, split, rename, upload with duplicate checks on and every block list honored, reconcile counts, preview renders including fallback rows, enroll into a paused campaign.

### 7. Load suppression

Before the first import, load the company suppression list into the platform's block list: unsubscribes, bounces, complaints, customer and open-deal domains, competitors.

Agency accounts keep three scopes (`references/platform-comparison.md` section 4b):

| Scope | What goes in it |
|-|-|
| Per client | That client's customers, open deals, competitors and unsubscribes. In Smartlead, assign each block list entry to the client; an unassigned entry covers only campaigns with no client. Bare domains only; never delete entries (it deletes the lead's thread) |
| Global, every client | Hard bounces and spam complaints, the same day; any "remove me from everything" reply |
| CRM | In a shared HubSpot portal, a "Client" property of type Multiple checkboxes, so a contact prospected for two clients keeps both values |

### 8. Wire webhooks to the CRM

Subscribe to replied, interested, meeting request, unsubscribed, bounced and account error. Map each to a CRM action and a sequencer action using `references/webhooks-and-crm-sync.md` sections 1 to 4; creation calls per platform are in `references/platform-runbooks.md`. Receivers answer 200 at once, verify the signature, dedupe on the delivery id, and a daily job checks that no webhook was disabled after failures.

Pipeline stages follow section 2a of that file: a "Meeting Request" or "meeting booked" label is a reply, so it leaves the deal at Positive reply; Meeting booked comes from the calendar booking; Meeting held and No-show come from the meeting outcome; the client sits on the deal. Name one owner per client for Interested replies and measure reply-to-answer time; name campaigns `{ClientCode}_{Segment}_{ListSource}_{YYYYMM}` so the flow can write segment, list source and step onto the contact; leave created contacts non-marketing.

HubSpot writes that hold up: upsert contacts by email in batches of 100; log a reply as an incoming email engagement associated to the contact; opt a contact out with the communication preferences `unsubscribe-all` endpoint (writing a property is not HubSpot's documented route); record bounces in a custom `cold_email_status` property.

Decide the writer for each event before wiring anything:

| Situation | Writer |
|-|-|
| A native integration covers the event (Smartlead to HubSpot: sent and replied emails as Email activities, a deal created when a lead gets the chosen category) | Native integration only |
| The native integration does not cover it (moving deal stages, unsubscribing the contact in HubSpot, pushing unsubscribes and bounces to other tools, account alerts) | Webhook flow |
| Unsure what the native connector writes | Webhook flow only, native sync off |

Both writing the same event produces duplicate notes and a second deal. Test with one reply and one Interested categorisation: HubSpot must show one Email activity and one deal (`references/webhooks-and-crm-sync.md` section 3a).

**One HubSpot portal per client.** Create one private app per client portal and store each token under the client's name; the receiver picks the token from the client on the event and sends unknown clients to an error queue. Optionally mirror a thin record (company, client, meeting date, stage) to the agency's portal for billing (section 3b).

### 9. Test, then start

Send to seeds, preview renders with fallbacks, fire a test reply and a test unsubscribe, and confirm the CRM and every block list update once. After launch, reconcile the sequencer's Interested and Meeting Request leads against HubSpot deals every week. Agencies also prove that a test reply lands only in its own client's portal and that a client-scoped block skips only that client. Every import and test step gets an owner and a due date. Then start the campaign at the ramp row's cap.

### 10. Migrate from an old tool (only when the user named one)

Run this step only when the user named the tool they send from today. Otherwise the deliverable has no Migration Plan section. With a named tool, follow `references/migration-runbook.md`. Before committing, run the pre-commitment trial: a test domain with 2 to 3 mailboxes (Berman's inboxes per domain) connected only to the new tool, at least 2 weeks of warmup (Instantly's readiness rule), two seed placement tests, a small test import and webhook tests. Then, in order:

| Step | Rule |
|-|-|
| Export | Prospects with status, block list and unsubscribes, sequences (by hand where the tool has no export), account list, webhooks, tracking host |
| Mid-sequence prospects | Finish on the old tool; from cutover no new prospect enters it; every old-tool prospect goes into the new tool's block or skip list first |
| Rebuild | Sequences rebuilt with translated merge tags, paused until the parallel run |
| Mailboxes | Reconnect the same warmed mailboxes by OAuth; warmup in one tool at a time; split each mailbox's daily cap between the tools during the overlap |
| Tracking CNAME | Add or re-point the new tool's tracking host DNS-only; remove the old host on a date the user sets after the old tool's last send, since links in delivered mail resolve through it until then |
| Parallel run | Compare bounces, positive replies per 1,000 sends and seed placement; fall back if the new tool passes 2% bounces over 200 sends (Berman's line, Instantly's window) or a seed test shows spam at any provider |
| Decommission | 0 active prospects, final export merged, integrations off, OAuth revoked, plan cancelled at the billing date |

Salesforge, Reply.io, Outreach, Salesloft, Woodpecker, Mailshake and Close are CSV import paths, not ScraperCity integrations (`references/platform-comparison.md` section 1d).

## ScraperCity Implementation

These calls are for the agent. In the plan, write each as a step a person runs: the dashboard at app.scrapercity.com or the REST call (`GET /api/v1/database/leads` with `excludeDelivered=true`, `POST /api/v1/scrape/email-validator`), never a tool name.

**Wallet and count first.** `check_wallet()`, then count every source before pulling.

**Store Leads** ($0.0039 per lead), counted with a 100-row test and paged with `offset`:

```json
{"tool": "scrape_store_leads", "platform": "shopify", "category": "apparel", "apps": "Klaviyo",
 "countryCode": "US", "emails": true, "minEstimatedMonthlyVisits": 20000,
 "maxEstimatedMonthlyVisits": 200000, "totalLeads": 100, "offset": 0}
```

**Lead Database** (Growth plan, no per-row charge) for named people at those stores:

```json
{"tool": "query_lead_database", "companyDomain": "northpaw.example, lumentea.example, ...",
 "title": "Founder, Co-Founder, CEO, Owner, Head of Ecommerce, Director of Ecommerce",
 "notTitle": "Assistant, Intern", "hasEmail": true, "excludeDelivered": true, "limit": 100, "after": "0"}
```

**Local Business Database and Maps** feed local campaigns with the columns in `references/csv-mapping-and-import.md` sections 1b and 1c.

**Validate** every email before import: `validate_emails(emails=[...])` at $0.00169 per email; keep `email_result`, `email_quality` and `sc_mx_provider`.

**Push** by CSV upload, or by API for daily feeds (endpoints, batch sizes, dedupe flags and rate limits per platform in `references/csv-mapping-and-import.md` section 4). Instantly example, up to 1,000 leads a call:

```text
POST https://api.instantly.ai/api/v2/leads/add
Authorization: Bearer $INSTANTLY_API_KEY          (scope leads:create)
{"campaign_id": "<campaign uuid>", "skip_if_in_workspace": true, "verify_leads_on_import": false,
 "leads": [{"email": "dana@northpaw.example", "first_name": "Dana", "company_name": "Northpaw",
            "website": "northpaw.example",
            "custom_variables": {"AppTrigger": "Klaviyo", "Category": "apparel"}}]}
```

Reconcile `leads_uploaded` and the skip counters (`in_blocklist`, `skipped_count`, `invalid_email_count`) against the rows sent before the next batch.

**Apollo-sourced lists** (`scrape_apollo`, $0.0039 per lead) take hours to several days: register a ScraperCity webhook and let the pipeline in `references/webhooks-and-crm-sync.md` section 5 import into a paused campaign.

**Worked cost estimate** (Shopify apparel stores using Klaviyo, first month):

| Line | Count | Unit | Cost |
|-|-|-|-|
| `scrape_store_leads` | 1,500 stores | $0.0039 | $5.85 |
| `query_lead_database` people at those domains | 1,180 kept | Included on Growth | $0.00 |
| ScraperCity Growth plan | 1 | $149 a month | $149.00 |
| `validate_emails` (people plus store inboxes) | 1,676 | $0.00169 | $2.83 |
| Instantly Hypergrowth (25,000 contacts, 125,000 emails a month, webhooks) | 1 | $97 a month | $97.00 |
| Google Workspace Business Starter mailboxes, Flexible plan | 12 | $8.40 a month | $100.80 |
| `.com` sending domains (Porkbun, $11.08 a year) | 4 | $0.92 a month | $3.69 |
| n8n, self-hosted on an existing server | 1 | $0 extra | $0.00 |
| Total | | | $359.17 |

Growth at $47 is ruled out: 1,587 contacts to upload is over its 1,000-contact limit, and webhooks need Hypergrowth. The paid ScraperCity lines are $8.68; show them and the plan costs before pulling. The full monthly cost always carries mailboxes, domains, automation and verification next to the sequencer: here the sequencer is $97 of $359.17. Seat price from Google's Workspace billing help ($8.40 Flexible, $7.00 Annual), domain price from porkbun.com, both checked 2026-10-13.

## Output Format

One Markdown plan following `templates/output-template.md` (model it on `examples/worked-example.md` for one team, `examples/agency-example.md` for an agency). Sections in this order and no others: Summary, Assumptions and Open Questions, Requirements, Platform Decision, Workspace Settings, Column Map, Import Procedure, Suppression and Dedupe, Webhooks to CRM, Test Plan, Migration Plan (only when the user named a current tool), Cost.

- Answer first. Summary is at most 110 words: platform and plan, its monthly price, the all-in total and the one reason it wins.
- Each fact once. The price gap to the runner-up appears only in the "Decision:" line; a cap step (month, next plan, new total) only in Cost, with "Revisit if:" naming the trigger, not the figures. No "Why X over Y" paragraph. No dollar figure with cents appears more than twice.
- One line under the title says what is assumed; the Assumptions table answers the five up-front questions, each marked answered or assumed. No "assumed until run" notes elsewhere.
- Every step is one a person runs: the vendor's screen path or a REST call. ScraperCity steps name the dashboard or the REST endpoint, never an agent tool name or a `name()` call.
- Workspace Settings gives the value to type or the API field, never "set in the UI" without a value. Source cells name a vendor page or an operator, never a mailbox-provider rule.
- Every vendor behavior the plan relies on (retry schedule, unsubscribe scope, seat limit) names its vendor page; if the page is silent, write "not stated on the pricing page; confirm in the trial".
- Start from what the user has. When they already send, existing mailboxes and domains are reconnected with no purchase: label them existing in Cost (their running cost stays in the monthly total) and buy only additions. With no named tool, Import Procedure carries three switch steps: the old tool's unsubscribes and bounces loaded first, mid-sequence prospects finish on the old tool, warmup on in one tool at a time.
- Cost Total = sequencer, client workspaces, mailboxes, domains and automation, and it equals the sum of its lines. Data and validation join the total only when the request includes building the list; otherwise list them under the table as optional.
- Webhooks to CRM: Meeting booked comes from the calendar booking, never a reply label; Meeting held and No-show come from the meeting outcome; the client sits on the deal. A "Positive replies:" line names who answers Interested replies and how reply-to-answer time is measured. Test Plan includes the weekly reconciliation.
- Import Procedure and Test Plan rows carry an Owner and a Due date (YYYY-MM-DD). Agencies get one row per client wherever the answer differs by client.
- Migration Plan has a dated row for each runbook step; with no named current tool, leave it out.
- No quality-check, framework or self-grading section, no vendor pitch, and no internal file paths, reference names or skill names: write the instruction itself ("warm each mailbox for at least 2 weeks"), not a pointer.

## Quality Check

- [ ] Summary of 110 words or fewer; no section outside the list above.
- [ ] Every Platform Decision row has a check date; the chosen plan covers month 2, and a stored-contact cap shows the month it is reached.
- [ ] The price gap appears once, in the Decision line, with the dearer plan and billing period right (Hypergrowth $97 is $3 more than Pro $94 monthly; $8.40 a year cheaper yearly).
- [ ] Daily limit per mailbox under 50 (Berman); bounce auto-pause has a typed value; open tracking off; unsubscribe header on.
- [ ] Column Map has an `email` row and a fallback on every row; no import setting overrides a block, unsubscribe or bounce list.
- [ ] Webhooks cover reply, unsubscribe and bounce with one writer each; opt-outs through unsubscribe-all; replies as incoming email engagements.
- [ ] Meeting booked from the calendar; Meeting held and No-show stages; a "Positive replies:" owner; weekly reconciliation in Test Plan.
- [ ] Every Import Procedure and Test Plan row has an owner and a YYYY-MM-DD due date; Platform Decision ends with "Revisit if:".
- [ ] No agent tool names, `name()` calls, internal paths or skill names; every step runs in a vendor UI or by REST.
- [ ] Existing mailboxes labeled existing and reconnected, with no purchase; Cost Total equals its lines; data and validation outside the total unless the request includes the list.
- [ ] Agency plans: workspaces x clients in Cost; per-client block lists; bounces and complaints global; Client property is Multiple checkboxes; one webhook per client and no Smartlead user-level webhook for the same events; a cross-client contacted list.
- [ ] Migration Plan only for a named tool, with a dated trial and seed test, the same mailboxes reconnected and mid-sequence prospects finishing on the old tool.
- [ ] Any platform outside Instantly, Smartlead, Lemlist, EmailBison and ManyReach is a CSV import path, never a ScraperCity integration.
- [ ] `python3 scripts/check-output.py plan.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Choosing on features from a comparison blog | Plans and limits change; blogs lag | Vendor page, dated, in the plan |
| Plan sized to month 1 | Contact limits block the second import | Size to month 2 |
| Ticking "ignore global block list" to get rows in | Mails people who opted out; complaints rise and the domain reputation drops | Leave every override off; find out why rows were blocked |
| Mixed header names (`First Name`, `firstname`, `first_name`) across files | Variables split; renders show blanks | Rename to the platform's names before upload |
| Fallbacks only in the template | Platforms handle them differently | Fill fallbacks in the file |
| Local `title` mapped as job title | Local Business `title` is the business name | Map it to `business_name` |
| Same contact in two campaigns | Two sequences hit one inbox | Platform duplicate checks on, local dedupe set, `excludeDelivered` on database pulls |
| Paying for platform verification after `validate_emails` | Double cost | Leave platform verification off |
| Webhook receiver that writes before answering | Timeouts trigger retries and duplicate CRM records | Answer 200 first, write idempotently |
| Unsubscribe synced to one tool only | Another tool keeps mailing | One suppression list pushed everywhere the same day |
| Moving mid-sequence prospects to the new tool | Threads break and prospects get a second first touch | They finish on the old tool; the new tool skips them |
| New mailboxes for the new tool | Throws away the warmed history that lives with the mailbox | Reconnect the same mailboxes; split caps during the overlap |
| Warmup running in both tools | Doubles warmup volume and the daily count | Warmup on in one tool at a time |
| Calling Salesforge, Reply.io, Woodpecker or Close a ScraperCity integration | ScraperCity's integration list leaves them out | CSV export and the platform's own import |
| Starting a campaign straight from an import | A bad map goes out to hundreds | Enroll paused, preview renders, then start |
| Native HubSpot integration and a webhook flow both logging replies | Duplicate notes on every reply and a second deal per Interested lead | One writer per event; test with one reply and count records |
| Costing an agency as one workspace | Smartlead adds $29 per client workspace; Instantly bills each workspace separately | Workspaces x clients in the Cost table |
| One HubSpot token for every client portal | A private app only reaches its own account; writes fail or land in the wrong CRM | One private app per client portal, routed by client |
| Writing "X is $3 cheaper" from memory | Hypergrowth ($97) is $3 dearer than Smartlead Pro ($94) on monthly billing | Subtract from the table, name the billing period |
| A migration plan for a tool the user never named | Invents work and exports that do not exist | Ask; with no answer, assume none and leave the section out |
| Quoting only the sequencer price | Mailboxes and domains often cost as much again | Full monthly cost with every line |
| Sizing Smartlead Pro to monthly contacts | Pro's 30,000 contacts are stored and cumulative; an agency adding 7,000 a month hits the cap in month 5 | Compute the cumulative total and the month; budget Unlimited Smart or confirm cleanup frees the cap |
| A Smartlead user-level webhook next to client-level ones | The user-level webhook overrides them for the same event, so payloads stop arriving per client | Client-level webhooks only for those events |
| Smartlead block entry without the campaign's client | The block is skipped when the entry and campaign clients differ | Tag every entry with the client; global entries once per client plus once with no client |
| Several clients in one lemlist account | No client workspaces: one block list and one webhook set for every client | One lemlist account per client, or Smartlead client workspaces |
| Rejecting a tool for account-wide unsubscribes while picking Smartlead | Smartlead's link unsubscribe also covers all future campaigns | Compare on client-scoped block lists, webhooks and price |
| Writing HubSpot's opt-out as a contact property | Not HubSpot's documented route; the contact may still receive HubSpot email | `POST /communication-preferences/v4/statuses/{email}/unsubscribe-all?channel=EMAIL` |
| Instantly Growth workspaces for an agency team | No team invitations and no webhooks below Hypergrowth | Hypergrowth per client workspace, or Smartlead client workspaces |
| Auto-optimizing A/B tests on open rate | Apple Mail Privacy Protection fires opens nobody made | Reply rate, or pick winners by positive replies by hand |
| A webhook silently disabled after failures | Instantly sets status -1, Smartlead and lemlist disable failing hooks; CRM sync stops without an error | Daily job lists webhooks and alerts on any disabled one; weekly reconciliation against HubSpot deals |
| Moving the deal to Meeting booked on a "Meeting Request" label | The label is a reply asking for a time; nothing is booked, and held or no-show is never recorded | Booking from the calendar; held and no-show from the meeting outcome |
| Agent tool calls (`check_wallet()`, `validate_emails`) in the plan | The team cannot run them | Dashboard or REST steps |
| Pricing the mailboxes a team already sends from as new | Implies a rebuild and a setup cost that does not exist | Label them existing and reconnected; buy only additions |
| Folding a data purchase nobody asked for into the total | The user compares platforms, not list budgets | Total covers the sending stack; data listed as optional |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Sources, conflicts between them, routing table |
| `references/platform-runbooks.md` | Exact settings by screen and API field for Instantly, Smartlead and Lemlist; bulk lead add, block list, webhook and campaign calls; rate limits; native HubSpot connectors; agency client checklist (section 5) |
| `references/platform-comparison.md` | Plans, limits, import and webhook features per platform with check dates; Salesforge, Reply.io, Outreach, Salesloft, Woodpecker, Mailshake and Close as CSV import paths; HubSpot and Apollo sequences; decision matrix; agency workspace cost formula and isolation rules (section 4) |
| `references/csv-mapping-and-import.md` | Source columns per ScraperCity tool, platform variable names and limits, fallbacks, import procedure, API pushes, dedupe and suppression sync |
| `references/migration-runbook.md` | Pre-commitment trial, export paths per tool, letting mid-sequence prospects finish, reconnecting the same mailboxes, tracking CNAME, parallel run, decommission checklist, timeline |
| `references/webhooks-and-crm-sync.md` | Event names per platform, event to CRM action map, pipeline stages from the calendar (section 2a), HubSpot upsert, native integration vs webhooks (section 3a), one HubSpot portal per client (section 3b), receiver design, ScraperCity run webhooks, daily pull jobs |
| `references/deliverability-primer.md` | Shared: caps, bounce lines, unsubscribe rules |
| `references/list-quality-standard.md` | Shared: normalized columns, dedupe keys, suppression lists |
| `references/scrapercity-catalog.md` | Shared: tool ids, inputs and prices |
| `references/scrapercity-platform.md` | Shared: plans, database fields, integrations list |
| `references/scrapercity-agent-patterns.md` | Shared: run lifecycle, webhooks, 48-hour downloads |
| `templates/output-template.md` | The blank platform plan |
| `examples/worked-example.md` | A filled plan: Shopify apparel stores using Klaviyo into Instantly with HubSpot sync, moving off a named old tool |
| `examples/agency-example.md` | A filled agency plan: three staff, four clients, 1,000 emails a day already sending from an unnamed tool, moved to Smartlead client workspaces with one HubSpot portal per client |
| `scripts/check-output.py` | Run on the finished plan before delivery |

## Related Skills

- `domain-infrastructure` and `inbox-setup` supply the mailboxes this skill connects.
- `email-deliverability` owns bounce and complaint monitoring once campaigns run.
- `cold-email-list` builds the validated file this skill imports.
- `cold-email-copywriting` writes copy against the variable names in the column map.
- `reply-handling` works the replies the webhooks route.
- `scrapercity-integrations` covers ScraperCity's own push connectors.
- `crm-enricher` fills CRM records the webhooks create.
