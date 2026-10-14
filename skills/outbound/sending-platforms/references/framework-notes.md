# Framework Notes: Sending Platforms

Which sources shape this skill, what each contributes, and which file to open for which question. The rule that runs through the skill: every platform feature or price in a deliverable carries the vendor page it came from and the date it was checked. Vendor pages were read on 2026-10-13.

## Sources and what they contribute

| Source | Type | Contribution | Where it shows up |
|-|-|-|-|
| Instantly pricing, help center and developer docs | Vendor docs | Plans and limits; CSV rules (50 variables, 20-character headers); duplicate check default; blocklist; unsubscribe header setting; webhooks on Hypergrowth and above; API v2 lead fields and dedupe flags; webhook event names | Platform comparison, column map, webhooks |
| Smartlead pricing, help center and API reference | Vendor docs | Plans; CSV mapping (40 custom variables); import override flags; Global Block List scope per client; unsubscribe setting; API batch of 400 and 200 custom fields; webhook events and retry behavior | Same |
| Lemlist pricing and API reference | Vendor docs | Email and Multichannel plans; lemwarm included; add-webhook endpoint with `secret`; event names, including the March 2026 unsubscribe event change | Same |
| EmailBison pricing and docs | Vendor docs | $599 base plan with 500,000 sends and dedicated IPs; custom variables per workspace; 23 webhook events | Same |
| ManyReach pricing | Vendor docs | Credit model, private IPs, ManySenders mailboxes | Platform comparison |
| HubSpot knowledge base and API reference | Vendor docs | Sequence seat requirement and send limits; enrollment rules; unenroll triggers; import dedupe keys; batch upsert by email | CRM-native option, CRM sync |
| Apollo knowledge base and pricing page | Vendor docs | Mailbox limits and recommended sending rates; CSV import rules; sequence overlap warning | CRM-native option |
| scrapercity.com integrations pages | ScraperCity docs | Which sequencers are integrations; API push examples and field names per platform | Column map, API pushes |
| ScraperCity npm package and catalog | Tool facts | Database output fields; tool prices; run webhooks and 48-hour downloads | Column map, pipeline |
| Google sender guidelines and FAQ, Yahoo Sender Hub | Mailbox provider rules | One-click unsubscribe for bulk senders; unsubscribes processed within 48 hours (Google) or 2 days (Yahoo) | Unsubscribe header settings, suppression sync timing |
| Alex Berman, alexberman.com (cold email templates; TAM strategy breakdown; checked 2026-10-13) | Operator | Under 50 cold emails a day per inbox; hard bounces under 2%; 2 to 3 inboxes per domain; 2 to 4 weeks of warmup | Daily limit per mailbox, bounce auto-pause, migration trial and fallback |
| Instantly help center, account readiness and high bounce auto-pause (checked 2026-10-13) | Vendor docs | Ready for campaigns after at least 2 weeks of warmup and a health score above 90%; auto-pause at 5% after 200 sends | Migration trial, bounce auto-pause, parallel-run fallback |
| Salesforge, Reply.io, Outreach, Salesloft, Woodpecker, Mailshake and Close pricing pages (checked 2026-10-13) | Vendor pricing | Plans, limits, channels and API notes for platforms outside ScraperCity's integration list | `platform-comparison.md` section 1d |
| Instantly, Woodpecker and Mailshake export documentation (checked 2026-10-13) | Vendor docs | What each tool exports (prospects, block lists, stats) and what it does not (sequences, replies) | `migration-runbook.md` section 2 |
| Smartlead HubSpot integration article and pricing Markdown page (checked 2026-10-13) | Vendor docs | Native sync: Email activities for sent and replied mail, Note activities for opens, clicks, unsubscribes and bounces, a deal created from a chosen lead category; CRM access from Pro; client workspaces $29 a month each | `webhooks-and-crm-sync.md` section 3a; `platform-comparison.md` section 4 |
| Instantly help center, separate workspaces (checked 2026-10-13) | Vendor docs | Each workspace needs its own paid subscription and can sit on a different plan | `platform-comparison.md` section 4 |
| HubSpot private apps overview and property field types (checked 2026-10-13) | Vendor docs | A private app lives in one account, super admin only, up to 20 per account; Multiple checkboxes holds several values | `webhooks-and-crm-sync.md` section 3b |
| Google Workspace billing help and porkbun.com `.com` page (checked 2026-10-13) | Vendor pricing | Business Starter $8.40 a user a month Flexible, $7.00 Annual; `.com` $11.08 a year | Full monthly cost in SKILL.md and both examples |
| Instantly API v2 reference (checked 2026-10-13) | Vendor API docs | Bulk add of 1,000 leads with skip flags and reconciliation counters; campaign setting fields; account `daily_limit` and `sending_gap`; webhook create, status and resume; block list bulk create; 100 a second and 6,000 a minute per workspace | `platform-runbooks.md` section 2, `csv-mapping-and-import.md` section 4 |
| Smartlead API reference, guides and help center (checked 2026-10-13) | Vendor docs | Client create and scoping, client-matched block lists, user-level webhook override, category filters, account cap that counts warmup, rate limits per key, webhook retry schedule | `platform-runbooks.md` section 3 |
| lemlist API reference and help center (checked 2026-10-13) | Vendor docs | Add-lead errors and `deduplicate`, unsubscribe variables API and account-wide scope, webhook secret in the body, lemwarm launch gate, conditions, two-way HubSpot sync and what it does not push | `platform-runbooks.md` section 4 |
| HubSpot developer docs: emails API, communication preferences v4, developer platform auth (checked 2026-10-13) | Vendor API docs | Reply logged as an incoming email engagement with association 198; opt-out through unsubscribe-all; private apps labeled legacy with rate limits; OAuth private distribution to up to 10 accounts | `webhooks-and-crm-sync.md` sections 2, 3 and 3b |
| Instantly help center, HubSpot connectors and Automations (checked 2026-10-13) | Vendor docs | Old connector imports, new connector powers Automations with named HubSpot actions; no deal actions named | `webhooks-and-crm-sync.md` section 3a |
| Smartlead webhook integration guide, help articles 27, 210 and 274 (checked 2026-10-13) | Vendor docs | Retries after 1, 5 and 30 minutes, 200 within 30 seconds, `X-Smartlead-Signature` and `X-Request-Id`, `EMAIL_REPLY` fields including `sequence_number`; a link unsubscribe covers all future campaigns; High Bounce Rate Auto Protection takes a percentage; Warning Notifications webhook on a bounce pause | `platform-runbooks.md` sections 1 and 3c; `webhooks-and-crm-sync.md` sections 2a and 4 |
| HubSpot meetings API guide, scheduling pages, meeting-based workflows, default marketing contact statuses (checked 2026-10-13) | Vendor docs | `hs_meeting_outcome` values (scheduled, completed, rescheduled, no show, canceled); scheduling pages on all plans; API-created contacts non-marketing by default, and only marketing contacts count toward the tier | `webhooks-and-crm-sync.md` sections 2a and 3 |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Smartlead custom variables | Help center: 40 per lead on CSV import. API reference: 200 `custom_fields` per lead. scrapercity.com page: 20 per lead | Keep custom variables to 20 or fewer, the lowest stated limit (also ManyReach's `custom1` to `custom20`) |
| Smartlead batch size | API reference: 400 per request. scrapercity.com page: 100 | Send 100 per request; smaller retries when one fails |
| Apollo sending rate | Apollo: 50 to 100 a day per mailbox. Alex Berman: under 50 per inbox | Under 50 (`references/deliverability-primer.md`) |
| Smartlead Pro yearly price | smartlead.ai/pricing shows $78 a month billed yearly (checked 2026-10-13); the Markdown page, dated 28 July 2026, shows $78.30 a month and $939.60 a year | Quote $78 as the pricing page shows it and compare yearly plans on annual totals: Instantly Hypergrowth $931.20 a year is $8.40 cheaper than Pro's $939.60 |
| Smartlead webhook retries | The webhooks reference (api.smartlead.ai/core/webhooks): retries after 1 minute, 5 minutes, 15 minutes, 1 hour and 6 hours, then the webhook is disabled after 5 failed attempts. The webhook integration guide (api.smartlead.ai/guides/webhook-integration): retries after 1, 5 and 30 minutes, then the event is marked failed; return 200 within 30 seconds; 4xx is not retried. Both checked 2026-10-13 | Answer 200 at once, dedupe on `X-Request-Id`, and run the daily health check that catches both a disabled webhook and failed events |
| Smartlead seats | Neither pricing page states a seat limit; the Markdown page says pricing is "not per seat and not per mailbox" | Write "no seat limit stated on the pricing page; confirm in the trial" |
| Smartlead webhook event names | The API reference lists `EMAIL_REPLY`, `EMAIL_BOUNCE`, `LEAD_UNSUBSCRIBED`, `LEAD_CATEGORY_UPDATED`; a separate webhooks guide uses `EMAIL_REPLIED`, `EMAIL_BOUNCED`, `EMAIL_UNSUBSCRIBED` | Use the API reference names, then confirm with a test event before going live |
| Smartlead settings and schedule fields | The setup guide, settings reference and schedule reference name stop conditions, days and new-lead caps differently | Set in the UI or API, then read the campaign back |
| Smartlead account daily cap | API reference: `max_email_per_day` counts warmup and campaign mail together | Set it to cold cap plus warmup per day; watch the account's sent count |
| Warmup length before launch | Instantly: at least 2 weeks and a health score above 90%. Berman: 2 to 4 weeks. lemlist's lemwarm guide: about 54 days with a Warmup Score of 90 or more | On lemlist, wait for the lemwarm score; elsewhere Instantly's readiness rule. The stricter gate wins |
| lemlist advanced conditions plan | Help article: Multichannel Expert or Enterprise. Pricing page: Email, Multichannel, Enterprise | Confirm in the app before a sequence depends on conditions |
| HubSpot private apps | Labeled legacy, still supported and creatable | One per client portal; with many portals, a developer-platform OAuth app with private distribution installs in up to 10 accounts |
| Instantly "Verify Leads" on upload vs `validate_emails` | Instantly charges 0.25 credits per lead; ScraperCity charges $0.0072 per email and returns `sc_mx_provider` and gateway data | Validate once with `validate_emails` before upload, leave platform verification off to avoid paying twice |

## Routing table

| Question | Open |
|-|-|
| Which platform fits this team and volume? | `references/platform-comparison.md` sections 1 and 3 |
| Exact settings, API calls and rate limits for Instantly, Smartlead or Lemlist | `references/platform-runbooks.md` sections 1 to 4 |
| Setting up one client at a time in an agency | `references/platform-runbooks.md` section 5, then `examples/agency-example.md` |
| What does each plan cost and include? | `references/platform-comparison.md` section 1a |
| HubSpot or Apollo sequences instead? | `references/platform-comparison.md` section 2 |
| We use Salesforge, Reply.io, Outreach, Salesloft, Woodpecker, Mailshake or Close | `references/platform-comparison.md` section 1d (CSV import path, not a ScraperCity integration) |
| How do we switch sequencers? | `references/migration-runbook.md` |
| Which ScraperCity column maps to which variable? | `references/csv-mapping-and-import.md` sections 1 and 2 |
| What if a merge field is empty? | `references/csv-mapping-and-import.md` section 3 |
| How do I import without duplicates or suppressed contacts? | `references/csv-mapping-and-import.md` sections 4 to 6 |
| Which webhook events do I need, and what does the CRM do with each? | `references/webhooks-and-crm-sync.md` sections 1 and 2 |
| How do I write to HubSpot or Pipedrive? | `references/webhooks-and-crm-sync.md` section 3 |
| Native integration or webhooks, and how to avoid duplicate notes | `references/webhooks-and-crm-sync.md` section 3a |
| Each client has its own HubSpot portal | `references/webhooks-and-crm-sync.md` section 3b |
| What does an agency with N clients pay, and how do we keep clients apart? | `references/platform-comparison.md` section 4 |
| How do ScraperCity runs feed the sequencer automatically? | `references/webhooks-and-crm-sync.md` sections 5 and 6 |
| Thresholds, unsubscribe rules | `references/deliverability-primer.md` |
| Required columns and suppression lists | `references/list-quality-standard.md` |
| Tool prices | `references/scrapercity-catalog.md` |

## What this skill does not claim

- No placement or reply rate is attributed to any platform. Placement depends on domains, mailboxes, lists and copy, which other skills own.
- Feature absence is never claimed from a pricing page that did not mention a feature; the tables say "Not stated".
- Third-party comparisons and review sites are not used as sources for features or prices.

## Sources

- Alex Berman, cold email templates (bounces under 2%; checked 2026-10-13): https://alexberman.com/cold-email-templates
- Alex Berman, TAM strategy breakdown (under 50 a day per inbox, 2 to 3 inboxes per domain, 2 to 4 weeks of warmup; checked 2026-10-13): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Instantly, When your email account is ready for campaigns (checked 2026-10-13): https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, High bounce auto-pause (checked 2026-10-13): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://instantly.ai/pricing
- https://help.instantly.ai/en/articles/6254215-how-to-import-leads-via-csv
- https://help.instantly.ai/en/articles/6261906-how-to-use-webhooks
- https://developer.instantly.ai/api/v2/lead
- https://smartlead.ai/pricing
- https://helpcenter.smartlead.ai/en/articles/409-how-to-map-csv-columns-in-smartlead-campaigns
- https://api.smartlead.ai/reference/add-leads-to-a-campaign-by-id
- https://www.lemlist.com/pricing
- https://developer.lemlist.com/api-reference/endpoints/webhooks/add-webhook
- https://emailbison.com/pricing
- https://docs.emailbison.com/webhooks/when-are-webhooks-triggered
- https://manyreach.com/pricing
- https://knowledge.hubspot.com/connected-email/sales-email-send-limits
- https://developers.hubspot.com/docs/api-reference/latest/crm/objects/contacts/guide
- https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- https://scrapercity.com/integrations
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://www.salesforge.ai/pricing
- https://reply.io/pricing/
- https://woodpecker.co/help-center/en/articles/5241827-exporting-data-from-woodpecker
- https://help.instantly.ai/en/articles/13924078-how-to-export-data-from-your-instantly-account
- https://helpcenter.smartlead.ai/en/articles/127-how-to-set-up-hubspot-integration-with-smartlead
- https://www.smartlead.ai/pricing.md
- https://help.instantly.ai/en/articles/6718773-create-a-separate-workspace-and-invite-team-members
- https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview
- https://knowledge.hubspot.com/properties/property-field-types-in-hubspot
- https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans
- https://porkbun.com/tld/com
- https://developer.instantly.ai/api-reference/lead/add-leads-in-bulk-to-a-campaign-or-list
- https://developer.instantly.ai/getting-started/rate-limit
- https://api.smartlead.ai/api-reference/webhooks/create
- https://api.smartlead.ai/guides/rate-limits
- https://helpcenter.smartlead.ai/en/articles/410-why-are-blocked-leads-still-receiving-emails
- https://developer.lemlist.com/api-reference/endpoints/webhooks/add-webhook
- https://help.lemlist.com/en/articles/14653207-how-to-set-up-and-use-lemwarm
- https://developers.hubspot.com/docs/api-reference/latest/crm/activities/emails/guide
- https://developers.hubspot.com/docs/api-reference/legacy/communication-preferences/status/unsubscribe-contact
- https://help.instantly.ai/en/articles/13342530-hubspot-integration-in-automations
