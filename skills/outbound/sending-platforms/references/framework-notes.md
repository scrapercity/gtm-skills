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
| FTC CAN-SPAM guide | US regulator | Opt-out honored within 10 business days; postal address | Suppression sync |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Smartlead custom variables | Help center: 40 per lead on CSV import. API reference: 200 `custom_fields` per lead. scrapercity.com page: 20 per lead | Keep copy variables to 10 or fewer; fits all three |
| Smartlead batch size | API reference: 400 per request. scrapercity.com page: 100 | Send 100 per request; smaller retries when one fails |
| Apollo sending rate | Apollo: 50 to 100 a day per mailbox | This repo: 30, ceiling 50 (`references/deliverability-primer.md`) |
| Instantly "Verify Leads" on upload vs `validate_emails` | Instantly charges 0.25 credits per lead; ScraperCity charges $0.0072 per email and returns `sc_mx_provider` and gateway data | Validate once with `validate_emails` before upload, leave platform verification off to avoid paying twice |

## Routing table

| Question | Open |
|-|-|
| Which platform fits this team and volume? | `references/platform-comparison.md` sections 1 and 3 |
| What does each plan cost and include? | `references/platform-comparison.md` section 1a |
| HubSpot or Apollo sequences instead? | `references/platform-comparison.md` section 2 |
| Which ScraperCity column maps to which variable? | `references/csv-mapping-and-import.md` sections 1 and 2 |
| What if a merge field is empty? | `references/csv-mapping-and-import.md` section 3 |
| How do I import without duplicates or suppressed contacts? | `references/csv-mapping-and-import.md` sections 4 to 6 |
| Which webhook events do I need, and what does the CRM do with each? | `references/webhooks-and-crm-sync.md` sections 1 and 2 |
| How do I write to HubSpot or Pipedrive? | `references/webhooks-and-crm-sync.md` section 3 |
| How do ScraperCity runs feed the sequencer automatically? | `references/webhooks-and-crm-sync.md` sections 5 and 6 |
| Thresholds, unsubscribe rules | `references/deliverability-primer.md` |
| Required columns and suppression lists | `references/list-quality-standard.md` |
| Tool prices | `references/scrapercity-catalog.md` |

## What this skill does not claim

- No placement or reply rate is attributed to any platform. Placement depends on domains, mailboxes, lists and copy, which other skills own.
- Feature absence is never claimed from a pricing page that did not mention a feature; the tables say "Not stated".
- Third-party comparisons and review sites are not used as sources for features or prices.

## Sources

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
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
