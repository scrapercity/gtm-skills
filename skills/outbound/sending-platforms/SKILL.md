---
name: sending-platforms
description: >-
  Chooses and configures the sequencer for cold email: Instantly, Smartlead,
  Lemlist, EmailBison, ManyReach, HubSpot sequences or Apollo sequences, with every
  feature and price taken from the vendor's own page and dated. Maps ScraperCity CSV
  columns (Lead Database, Local Business Database, Google Maps, Store Leads, Email
  Validator) to each platform's variables with fallbacks, imports without duplicates
  or suppressed contacts, sets campaign safety settings, and wires webhooks back to
  HubSpot, Pipedrive or GoHighLevel. Produces a platform plan with a column map,
  import steps, a webhook map and a monthly cost. Use when the user asks which cold
  email tool to use, Instantly vs Smartlead, how to upload a ScraperCity list to a
  sequencer, how to map custom variables, how to stop duplicates, or how to sync
  replies and unsubscribes to the CRM.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [sequencers, instantly, smartlead, lemlist, emailbison, manyreach, hubspot, apollo, csv-mapping, webhooks, crm-sync]
  related_skills: [domain-infrastructure, inbox-setup, email-deliverability, cold-email-list, cold-email-copywriting, reply-handling, scrapercity-integrations, crm-enricher]
  frameworks:
    - "Instantly - pricing, CSV import, blocklist, API v2 and webhook documentation (checked 2026-10-13)"
    - "Smartlead - pricing, CSV mapping, Global Block List, API and webhook documentation (checked 2026-10-13)"
    - "Lemlist, EmailBison and ManyReach - pricing pages and API documentation (checked 2026-10-13)"
    - "HubSpot - sequences send limits, enrollment rules, import and contacts API (checked 2026-10-13)"
    - "Apollo - sending limits, sequences and CSV import knowledge base (checked 2026-10-13)"
    - "Google and Yahoo - bulk sender one-click unsubscribe and 48-hour or 2-day processing"
    - "FTC - CAN-SPAM Act compliance guide (opt-outs within 10 business days)"
  shared_references: [deliverability-primer.md, list-quality-standard.md, scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md]
---

# Sending Platforms

## Overview

This skill picks the sequencer and turns a ScraperCity list into a running campaign without breaking anything on the way in. The deliverable is a platform plan: the requirements, the platform decision with dated vendor facts, the workspace and campaign settings, a column map from every ScraperCity source column to a platform variable with a fallback, the import procedure with dedupe and suppression, the webhook map back to the CRM, a test plan and the monthly cost.

The mistakes it prevents: buying a plan whose contact or send limit the first month already exceeds; importing with the block list or unsubscribe list overridden; merge tags that render as `{{firstName}}` or "Hi ,"; the same prospect sitting in two campaigns; an unsubscribe in one tool that another tool keeps mailing; and feature claims copied from review sites instead of the vendor's page.

## When to Use

- "Which cold email tool should we use?" or "Instantly vs Smartlead vs Lemlist".
- "How do I upload this ScraperCity CSV to Instantly?" or "map these columns to custom variables".
- "Leads are not uploading" or "why were 300 rows skipped?"
- "How do I stop duplicates across campaigns?"
- "Sync replies and unsubscribes to HubSpot" or "set up webhooks".
- "Can we just use HubSpot sequences or Apollo?"
- Moving from one sequencer to another.

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

| Input | Why | Default if unknown |
|-|-|-|
| New prospects per day, steps, sending days | Sends and contacts per month decide the plan | Required |
| Mailboxes ready (from `inbox-setup`) | Connection and caps | Required |
| Team: seats, agency or in-house, client workspaces | Pricing model and suppression scope | In-house, 1 to 3 users |
| Channels beyond email (LinkedIn, calls) | Lemlist Multichannel or a separate dialer | Email only |
| CRM | Webhook targets | HubSpot |
| Middleware | Webhook receiver | n8n or Zapier |
| ScraperCity sources | Column map | Lead Database |
| Existing suppression lists | Block list import | Export from current tools and CRM |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Vendor pricing pages and help centers (Instantly, Smartlead, Lemlist, EmailBison, ManyReach), checked 2026-10-13 | Plans, contact and send limits, CSV rules, dedupe defaults, block lists, unsubscribe settings, webhook availability and event names. Each fact is dated in `references/platform-comparison.md`. |
| HubSpot knowledge base | Sequences need a Sales or Service Hub Professional or Enterprise seat; 500 sequence emails a day per Professional seat, 1,000 per Enterprise; one sequence per contact; unenroll on reply or meeting; no warmup. |
| Apollo knowledge base | Up to 15 mailboxes per user by plan; 50 to 100 a day per mailbox suggested (stricter caps here); custom fields must exist before CSV import; contacts can be in two sequences if you override the warning. |
| scrapercity.com integrations pages | Instantly, Smartlead, Lemlist, EmailBison and ManyReach are ScraperCity integrations, each with an API push example and field names. |
| Google sender FAQ and Yahoo Sender Hub | Bulk senders need one-click unsubscribe (RFC 8058) and must process unsubscribes within 48 hours (Google) or 2 days (Yahoo). |
| FTC CAN-SPAM guide | Opt-outs honored within 10 business days; the opt-out mechanism must work. |
| `references/deliverability-primer.md` | Caps, bounce lines and validation rules every setting here enforces. |

## Workflow

### 1. Size the need

```text
sends_per_month    = new_prospects_per_day x steps x sending_days
contacts_per_month = new_prospects_per_day x sending_days
mailboxes          = from the inbox-setup roster
```

Write both numbers next to each plan's limits. A plan must cover month 2, not only month 1.

### 2. Choose the platform

Run the decision matrix in `references/platform-comparison.md` section 3. Record for each option the plan, price, why it fits, its gaps, and the date you checked the vendor page. Never cite a feature from a review site. If a pricing page does not state a feature, write "Not stated" and confirm in the app or with the vendor before buying.

### 3. Configure the workspace

Connect mailboxes by OAuth. Then set, per campaign:

| Setting | Value | Why |
|-|-|-|
| Daily limit per mailbox | Ramp row from `inbox-setup`; 30, never above 50 | Primer section 7 |
| Campaign daily limit | Mailboxes x current cap | Keeps the ramp honest |
| Schedule | Weekdays, 08:00 to 17:00 recipient local time | `inbox-setup` |
| Open tracking | Off | Apple Mail Privacy Protection inflates opens |
| Link tracking | Off unless a verified custom tracking domain exists | Fewer filter signals |
| Unsubscribe header | On (Instantly "Insert unsubscribe link header"; Smartlead "Add unsubscribe message in all emails") | Google and Yahoo one-click rules |
| Stop on reply | On | Platform default; check it |
| Bounce auto-pause | On | Instantly default pauses above 5% after 200 sends; watch the 2% house line in `email-deliverability` |
| Platform lead verification on upload | Off when the file was validated with `validate_emails` | Avoid paying twice |

### 4. Build the column map

For each source, map source column, normalized column, platform variable and fallback, using `references/csv-mapping-and-import.md` sections 1 to 3. Rename headers in the file to the platform's names before upload. Fill fallbacks in the file.

### 5. Import

Follow the 10-step procedure in `references/csv-mapping-and-import.md` section 4: normalize, dedupe, suppress, validate, split, rename, upload with duplicate checks on and every block list honored, reconcile counts, preview 10 renders, enroll into a paused campaign.

### 6. Load suppression

Before the first import, load the company suppression list into the platform's block list: unsubscribes, bounces, complaints, customer and open-deal domains, competitors. Smartlead agency accounts load it per client.

### 7. Wire webhooks to the CRM

Subscribe to replied, interested, meeting booked, unsubscribed, bounced and account error. Map each to a CRM action and a sequencer action using `references/webhooks-and-crm-sync.md` sections 1 to 4. Receivers answer 200 fast and write idempotently.

### 8. Test, then start

Send to seeds, preview renders with fallbacks, fire a test reply and a test unsubscribe, and confirm the CRM and every block list update once. Then start the campaign at the ramp row's cap.

## ScraperCity Implementation

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

**Validate** every email before import: `validate_emails(emails=[...])` at $0.0072 per email; keep `email_result`, `email_quality` and `sc_mx_provider`.

**Push** by CSV upload, or by API for daily feeds (endpoints and dedupe flags per platform in `references/csv-mapping-and-import.md` section 4). Instantly example:

```text
POST https://api.instantly.ai/api/v2/leads
Authorization: Bearer $INSTANTLY_API_KEY          (scope leads:create)
{"campaign": "<campaign uuid>", "email": "dana@northpaw.example", "first_name": "Dana",
 "company_name": "Northpaw", "website": "northpaw.example", "skip_if_in_workspace": true,
 "custom_variables": {"AppTrigger": "Klaviyo", "Category": "apparel"}}
```

**Apollo-sourced lists** (`scrape_apollo`, $0.0039 per lead) take hours to several days: register a ScraperCity webhook and let the pipeline in `references/webhooks-and-crm-sync.md` section 5 import into a paused campaign.

**Worked cost estimate** (Shopify apparel stores using Klaviyo, first month):

| Line | Count | Unit | Cost |
|-|-|-|-|
| `scrape_store_leads` | 1,500 stores | $0.0039 | $5.85 |
| `query_lead_database` people at those domains | 1,180 kept | Included on Growth | $0.00 |
| ScraperCity Growth plan | 1 | $149 a month | $149.00 |
| `validate_emails` (people plus store inboxes) | 1,676 | $0.0072 | $12.07 |
| Instantly Hypergrowth (25,000 contacts, 125,000 emails a month, webhooks) | 1 | $97 a month | $97.00 |
| Total | | | $263.92 |

Growth at $47 is ruled out: 1,587 contacts to upload is over its 1,000-contact limit, and webhooks need Hypergrowth. The paid ScraperCity lines are $17.92; show them and the plan costs before pulling.

## Output Format

One Markdown plan following `templates/output-template.md`, sections in order: Summary, Requirements, Platform Decision, Workspace Settings, Column Map, Import Procedure, Suppression and Dedupe, Webhooks to CRM, Test Plan, Cost. Every vendor fact in Platform Decision carries a checked date.

## Quality Check

- [ ] Every Platform Decision row has a vendor-page check date (YYYY-MM-DD).
- [ ] The chosen plan covers month 2 contacts and sends, with numbers shown.
- [ ] Daily limit per mailbox is 50 or less and matches the `inbox-setup` ramp.
- [ ] Column Map has an `email` row and a fallback (or "required") on every row.
- [ ] No import setting overrides the block list, unsubscribe list or bounce list.
- [ ] Webhooks cover reply, unsubscribe and bounce, each with a CRM action.
- [ ] Open tracking off; unsubscribe header on where supported.
- [ ] `python3 scripts/check-output.py plan.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Choosing on features from a comparison blog | Plans and limits change; blogs lag | Vendor page, dated, in the plan |
| Plan sized to month 1 | Contact limits block the second import | Size to month 2 |
| Ticking "ignore global block list" to get rows in | Mails people who opted out; CAN-SPAM and provider complaints | Leave every override off; find out why rows were blocked |
| Mixed header names (`First Name`, `firstname`, `first_name`) across files | Variables split; renders show blanks | Rename to the platform's names before upload |
| Fallbacks only in the template | Platforms handle them differently | Fill fallbacks in the file |
| Local `title` mapped as job title | Local Business `title` is the business name | Map it to `business_name` |
| Same contact in two campaigns | Two sequences hit one inbox | Platform duplicate checks on, local dedupe set, `excludeDelivered` on database pulls |
| Paying for platform verification after `validate_emails` | Double cost | Leave platform verification off |
| Webhook receiver that writes before answering | Timeouts trigger retries and duplicate CRM records | Answer 200 first, write idempotently |
| Unsubscribe synced to one tool only | Another tool keeps mailing | One suppression list pushed everywhere within 24 hours |
| Starting a campaign straight from an import | A bad map goes out to hundreds | Enroll paused, preview 10, then start |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Sources, conflicts between them, routing table |
| `references/platform-comparison.md` | Plans, limits, import and webhook features per platform with check dates; HubSpot and Apollo sequences; decision matrix |
| `references/csv-mapping-and-import.md` | Source columns per ScraperCity tool, platform variable names and limits, fallbacks, import procedure, API pushes, dedupe and suppression sync |
| `references/webhooks-and-crm-sync.md` | Event names per platform, event to CRM action map, HubSpot upsert, receiver design, ScraperCity run webhooks, daily pull jobs |
| `references/deliverability-primer.md` | Shared: caps, bounce lines, unsubscribe rules |
| `references/list-quality-standard.md` | Shared: normalized columns, dedupe keys, suppression lists |
| `references/scrapercity-catalog.md` | Shared: tool ids, inputs and prices |
| `references/scrapercity-platform.md` | Shared: plans, database fields, integrations list |
| `references/scrapercity-agent-patterns.md` | Shared: run lifecycle, webhooks, 48-hour downloads |
| `templates/output-template.md` | The blank platform plan |
| `examples/worked-example.md` | A filled plan: Shopify apparel stores using Klaviyo into Instantly with HubSpot sync |
| `scripts/check-output.py` | Run on the finished plan before delivery |

## Related Skills

- `domain-infrastructure` and `inbox-setup` supply the mailboxes this skill connects.
- `email-deliverability` owns bounce and complaint monitoring once campaigns run.
- `cold-email-list` builds the validated file this skill imports.
- `cold-email-copywriting` writes copy against the variable names in the column map.
- `reply-handling` works the replies the webhooks route.
- `scrapercity-integrations` covers ScraperCity's own push connectors.
- `crm-enricher` fills CRM records the webhooks create.
