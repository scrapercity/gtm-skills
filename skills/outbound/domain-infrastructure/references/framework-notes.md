# Framework Notes: Domain Infrastructure

Which sources shape this skill, what each contributes, and which file to open for which question.

## Sources and what they contribute

| Source | Type | Contribution to this skill | Where it shows up |
|-|-|-|-|
| Google Email sender guidelines (support.google.com/a/answer/81126) | Mailbox provider rule | Authentication bar for all senders and for 5,000+ a day senders, PTR and TLS, 0.3% spam ceiling | SKILL.md foundations, DMARC rows |
| Google sender guidelines FAQ (/14229414) | Mailbox provider rule | The 5,000 count is per primary domain including subdomains; bulk status never expires; guidelines do not apply to mail sent to Workspace accounts; November 2025 enforcement ramp | Why cold mail never uses a subdomain of the main domain |
| Yahoo Sender Hub best practices and FAQ | Mailbox provider rule | DMARC must pass; `rua` strongly recommended; no published bulk number | `rua` on every domain |
| Microsoft Outlook high-volume sender announcement (April 2025) and Outlook.com sender policies | Mailbox provider rule | SPF, DKIM, DMARC with alignment for 5,000+ a day to consumer Outlook; `550; 5.7.515` | Records checklist |
| RFC 7208 | Standard | One SPF record, 10-lookup limit, no `ptr` | SPF rules |
| RFC 6376 | Standard | DKIM selector location, 1024-bit minimum | DKIM rows |
| RFC 7489 and RFC 9989 | Standard | One DMARC record, relaxed alignment, `rua`, report authorization, `pct` removed | DMARC section |
| Google Workspace admin help | Vendor doc | MX `smtp.google.com`, SPF `include:_spf.google.com ~all`, DKIM `google._domainkey` 2048-bit, 2,000 a day cap, Flexible vs Annual prices | Records checklist, provider matrix |
| Microsoft 365 docs | Vendor doc | MX token format, `spf.protection.outlook.com`, DKIM CNAME formats (new from May 2025), 10,000 recipients a day, `onmicrosoft.com` 100-recipient cap | Records checklist, provider matrix |
| Cloudflare Registrar and Redirect Rules docs | Vendor doc | At-cost pricing, Cloudflare nameservers required, redirect rules need a proxied record | Registrar choice, redirect steps |
| Instantly and Smartlead help centers | Vendor doc | Exact tracking CNAME hosts and targets | Tracking section |
| Spamhaus Domain Blocklist | Blocklist operator | New domains start with poor reputation; snowshoeing (rapidly rotating many domains) gets listed | Domain count discipline, keep domains long term |
| Alex Berman, alexberman.com | Operator | 3 to 5 domains, 2 to 3 inboxes per domain, under 50 a day, 2 to 4 weeks warmup, tracking-domain advice (May 2026) | Capacity defaults |
| ScraperCity catalog and platform files | Tool facts | `query_lead_database` totals, `validate_emails` at $0.0072 with `sc_mx_provider` for provider mix | ScraperCity Implementation |

## Routing table

| Question | Open |
|-|-|
| What exact value goes in this DNS record? | `references/dns-records-checklist.md` sections 2 and 3 |
| How should DMARC change over time? | `references/dns-records-checklist.md` section 4 |
| How do I redirect the domain? | `references/dns-records-checklist.md` section 7 |
| Is BIMI worth it? | `references/dns-records-checklist.md` section 8 |
| Google or Microsoft? | `references/mailbox-provider-matrix.md` sections 1 and 2 |
| How many domains and mailboxes for X a day? | `references/capacity-and-costs.md` sections 2 and 3 |
| What will it cost per month? | `references/capacity-and-costs.md` sections 4 and 5 |
| Is the market big enough for this build? | `references/capacity-and-costs.md` section 6 |
| What are the provider rules and thresholds? | `references/deliverability-primer.md` |
| How do I read validation results for the provider sample? | `references/list-quality-standard.md` section 5 |
| Which ScraperCity tool and price? | `references/scrapercity-catalog.md` |

## What this skill does not claim

- Matching the sender's mailbox provider to the recipient's is an operator belief. No provider documents it. The skill treats it as a split test.
- Domain age thresholds ("wait 30 days after registering") are not published by Google, Yahoo or Microsoft. The skill uses a 14-day warmup minimum from Instantly's readiness rule and Alex Berman's 2 to 4 weeks, and Spamhaus's statement that new domains start with poor reputation.
- No inbox placement percentages are promised for any setup.

## Sources

- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- https://www.rfc-editor.org/rfc/rfc7208
- https://www.rfc-editor.org/rfc/rfc6376
- https://www.rfc-editor.org/rfc/rfc9989.html
- https://www.spamhaus.org/blocklists/domain-blocklist/
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://alexberman.com/custom-tracking-domain-gmail
