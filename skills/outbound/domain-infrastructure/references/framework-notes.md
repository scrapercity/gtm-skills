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
| RFC 7489, RFC 9989 and RFC 9990 | Standard | One DMARC record, relaxed alignment, `rua`, `pct` removed; RFC 7489 section 7.1 and RFC 9990 section 4 allow one wildcard `*._report._dmarc` authorization for any domain | DMARC section, Main Domain Changes line |
| Google Workspace admin help | Vendor doc | MX `smtp.google.com`, SPF `include:_spf.google.com ~all`, DKIM `google._domainkey` 2048-bit, 2,000 a day cap, Flexible vs Annual prices | Records checklist, provider matrix |
| Microsoft 365 docs | Vendor doc | MX token format, `spf.protection.outlook.com`, DKIM CNAME formats (new from May 2025), 10,000 recipients a day, `onmicrosoft.com` 100-recipient cap | Records checklist, provider matrix |
| Cloudflare Registrar and Redirect Rules docs | Vendor doc | At-cost pricing, Cloudflare nameservers required, redirect rules need a proxied record | Registrar choice, redirect steps |
| Instantly and Smartlead help centers | Vendor doc | Exact tracking CNAME hosts and targets; Instantly's host must be exactly `inst` to `prox.itrackly.com` (checked 2026-10-13) | Tracking section, record template |
| Cloudflare API and Porkbun API v3 docs, checked 2026-10-13 | Vendor doc | Create-record endpoints, Bearer token and API-key auth, Cloudflare batch limits, Porkbun per-domain API opt-in and `warnings` | Bulk DNS path, `dns-records-checklist.md` section 13 |
| Spamhaus Domain Blocklist | Blocklist operator | Unknown reputations begin as poor (domain age is the launch risk); snowshoeing is a technique using many domains and IPs that change often, and domains acting like it get treated like it | Domain count discipline, keep domains long term, launch risk |
| Alex Berman, alexberman.com | Operator | 3 to 5 domains, 2 to 3 inboxes per domain, under 50 a day, 2 to 4 weeks warmup (October 2026); new domains start at 10 to 20 a day and ramp up over 2 to 4 weeks (cold email templates); open tracking off on first touches, bounces above 2% hurt and above 5% are critical (May 2026) | Capacity defaults, the 50 ceiling, the cold ramp and the wide build cap, bounce thresholds |
| Managed inbox vendors' pricing pages (ScaledMail, Hypertide, Mailforge, Infraforge, Primeforge, Maildoso), checked 2026-10-13 | Vendor pricing | What done-for-you vendors provide, per-mailbox and per-domain prices, stated sending guidance | `mailbox-provider-matrix.md` sections 6 to 8 |
| Microsoft Learn: outbound spam protection and Exchange Online limits (TERRL) | Vendor doc | User and organization thresholds, tenant-wide external recipient cap tied to licenses, one customer's spam can affect others | High-density tenant verdict, section 7 |
| Growth Engine X methodology page (coldoutbound.com, Eric Nowoslawski's agency), checked 2026-10-13 | Operator | Backup domains always warming; capacity for 1,500 a day when the goal is 1,000 | Where sources differ: reserve capacity |
| Cloudflare DNSSEC docs; ICANN DNSSEC explainer; ICANN Expired Registration Recovery Policy | Vendor doc, standards body | DNSSEC must be off at the old host before a nameserver change; expired names lose DNS resolution; renewal reminders a month and a week out | Domain inventory columns, `dns-records-checklist.md` section 12 |
| Microsoft 365 Message Center MC1454397 (rollout mid-September to end of November 2026) and MC786329 | Vendor notice | New tenants get 10% of the external recipient quota for 30 days and 25% until day 60; trials 500 a day; Basic SMTP AUTH off by default after December 2026 | Create Microsoft tenants on day 0, tenant settings in `mailbox-provider-matrix.md` section 10, launch dates |
| Microsoft Learn, Configure outbound spam policies | Vendor doc | Per-user hourly and daily recipient limits (0 to 10,000), restriction on breach, automatic forwarding control | Outbound policy row in section 10 |
| Google Postmaster Tools help (dashboards; set up and verify a domain) | Mailbox provider doc | Verify each domain with a TXT or CNAME; data covers personal Gmail only and is hidden on low-volume days | Monitoring section, Postmaster TXT row in the record template |
| Instantly, account readiness | Sequencer doc | 2 weeks of warmup minimum, 3 weeks for its own AirMail accounts, health score above 90% | 21-day standard path and 14-day soft start |
| Instantly, account and campaign limits; warmup settings | Sequencer doc | 30 campaign emails per account a day; for new accounts increase 1 a day, daily warmup limit 10, reply rate 30 | Cap per mailbox, warmup settings line, tenant quota check |
| Puzzle Inbox, cold email inbox naming conventions (May 18, 2026) | Vendor blog | `first.last@` most trusted, `first@` personal, no digits, no role addresses | Mailbox address rule |
| Instantly, ESP matching | Sequencer doc | Sends from the account that matches the lead's provider; asks for accounts on several providers; no data on the gain | Provider split sized to the measured mix |
| Instantly and Smartlead, secondary sending domain articles | Sequencer doc | 2 to 3 inboxes per domain; no hyphens or numbers; `.com` or country TLDs; Smartlead caps an address at 50 a day | Naming rules, mailboxes per domain |
| Instantly, high bounce auto-pause | Sequencer doc | Campaigns pause at 5% bounces after 200 sends by default | Bounce stop line |
| Google, Top 10 Gmail sender issues; Recommended DMARC rollout | Mailbox provider doc | Keep spam rate below 0.1%; `p=none` for at least a week, then quarantine | Monitoring thresholds, DMARC progression |
| Apollo, email sending limits | Sequencer doc | 10 to 20 sends an hour per mailbox | Hourly limit in the Microsoft outbound policy |
| ScraperCity catalog and platform files | Tool facts | `query_lead_database` totals, `validate_emails` at $0.0072 with `sc_mx_provider` for provider mix | ScraperCity Implementation |

## Where sources differ

| Topic | Sources | Rule here |
|-|-|-|
| Reserve capacity | Growth Engine X's methodology page: "If your goal is to send 1,000 emails per day, we set up capacity for 1,500", with backup domains always warming (50% headroom); its podcast summary describes backup inboxes equal to sending capacity | The reserve share is a user input with at least 1 reserve domain. For the 1,500 a day build, 50% means 2,250 a day of capacity: 76 mailboxes on 38 domains instead of 60 on 30 at 20%, 16 more seats, $134.40 a month more on Google Flexible plus $88.64 a year of domains. A 1:1 backup doubles the seat bill |
| Mailboxes per domain | Alex Berman, Instantly, Smartlead and Mailforge's calculator: 2 to 3. ScaledMail's Outlook option and Hypertide's Entra Domains: 25 | 2 or 3, the user's choice after the side-by-side in `capacity-and-costs.md` section 2a; high-density domains only as a test pod (`mailbox-provider-matrix.md` section 7) |
| Warmup length | Instantly: 2 weeks minimum, 3 for its own AirMail accounts. Alex Berman: 2 to 4 weeks. M3AAWG: about 6 weeks for permission mail | 21 days standard; 14-day soft start as the named alternative (`launch-and-monitoring.md` section 2) |
| When to add Microsoft mailboxes | Instantly's ESP Matching claims matching helps but publishes no data | Split by the measured mix from day one, so replies per 1,000 sends by provider are comparable from the first send instead of about 6 weeks later |
| Per-mailbox daily volume | Instantly: 30 recommended. Alex Berman: under 50. Smartlead: max 50 per address. Mailforge: 30 recommended, 100 maximum. ScaledMail: up to 25 on Google, up to 10 on Outlook. Maildoso: up to 15. Apollo: 50 to 100 | 30 on Google and Microsoft 365 seats you administer, never above 50; the vendor's lower figure when it is lower |
| Who builds the mailboxes | Vendors price Google inboxes at $3.30 to $4.50 against Google's $7.00 to $8.40 list price | Cost favors done-for-you; control favors DIY. Decide with the breakeven in `mailbox-provider-matrix.md` section 8 |

## Routing table

| Question | Open |
|-|-|
| What exact value goes in this DNS record? | `references/dns-records-checklist.md` sections 2 and 3 |
| How do I write records for many domains at once? | `references/dns-records-checklist.md` section 13 |
| One tenant or several? | `references/mailbox-provider-matrix.md` section 9 |
| When do we add capacity? | `references/capacity-and-costs.md` section 8 |
| How should DMARC change over time? | `references/dns-records-checklist.md` section 4 |
| How do I redirect the domain? | `references/dns-records-checklist.md` section 7 |
| Should I set up BIMI? | `references/dns-records-checklist.md` section 8 |
| Google or Microsoft? | `references/mailbox-provider-matrix.md` sections 1 and 2 |
| Should a vendor build the mailboxes for us? | `references/mailbox-provider-matrix.md` sections 6 and 8 |
| Is 25 Microsoft mailboxes per domain safe? | `references/mailbox-provider-matrix.md` section 7 |
| What do we set in a new Microsoft 365 tenant or Workspace account? | `references/mailbox-provider-matrix.md` sections 10 and 11 |
| When is the first cold send, honestly? Soft start or standard? | `references/launch-and-monitoring.md` sections 2 and 3 |
| What do we monitor and at what thresholds? | `references/launch-and-monitoring.md` sections 5 and 6 |
| Two or three mailboxes per domain? | `references/capacity-and-costs.md` section 2a |
| What goes in the nameservers, DNSSEC and renewal columns? | `references/dns-records-checklist.md` section 12 |
| How many domains and mailboxes for X a day? | `references/capacity-and-costs.md` sections 2 and 3 |
| What will it cost per month? | `references/capacity-and-costs.md` sections 4 and 5 |
| Is the list big enough for this build? (agent check, not a plan section) | `references/capacity-and-costs.md` section 6 |
| What are the provider rules and thresholds? | `references/deliverability-primer.md` |
| How do I read validation results for the provider sample? | `references/deliverability-primer.md` section 5 |
| Which ScraperCity tool and price? | `references/scrapercity-catalog.md` |

## What this skill does not claim

- Matching the sender's mailbox provider to the recipient's is an operator belief. No provider documents it. The skill treats it as a split test.
- Domain age thresholds ("wait 30 days after registering") are not published by Google, Yahoo or Microsoft. The skill uses 21 days of warmup as its standard and 14 days as the floor, from Instantly's readiness rule, Alex Berman's 2 to 4 weeks and Spamhaus's statement that new domains start with poor reputation. Microsoft's tenant-age quota is the one published age rule, and it applies to the tenant, not the domain.
- Reserve share, tenant size, setup time per domain and the pass lines for any volume or provider test are user inputs; no source cited here publishes them for cold email.
- No inbox placement percentages are promised for any setup.

## Sources

- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- https://www.rfc-editor.org/rfc/rfc7208
- https://www.rfc-editor.org/rfc/rfc6376
- https://www.rfc-editor.org/rfc/rfc9989.html
- https://www.rfc-editor.org/rfc/rfc9990.html
- https://www.rfc-editor.org/rfc/rfc7489#section-7.1
- https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/create/
- https://porkbun.com/llms/dns
- https://www.spamhaus.org/blocklists/domain-blocklist/
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://alexberman.com/custom-tracking-domain-gmail
- https://coldoutbound.com/
- https://scaledmail.com/pricing
- https://www.hypertide.io/pricing
- https://www.mailforge.ai/pricing
- https://maildoso.ai/pricing
- https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-protection-about
- https://developers.cloudflare.com/dns/dnssec/
- https://www.icann.org/resources/pages/errp-2013-02-28-en
- https://mc.merill.net/message/MC1454397
- https://mc.merill.net/message/MC786329
- https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-policies-configure
- https://support.google.com/mail/answer/9981691
- https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- https://thegtmengineer.substack.com/p/the-winning-cold-outbound-formula
- https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- https://help.instantly.ai/en/articles/9214350-warmup-settings
- https://alexberman.com/cold-email-templates
- https://puzzleinbox.com/blog/cold-email-inbox-naming-conventions
- https://help.instantly.ai/en/articles/7044069-email-service-providers-matching
- https://help.instantly.ai/en/articles/6502027-scale-your-cold-email-campaigns-with-secondary-sending-domains-the-strategy-how-to-implement-it
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://helpcenter.smartlead.ai/en/articles/147-all-you-need-to-know-about-secondary-sending-domains-for-cold-email-campaigns
- https://support.google.com/mail/answer/15256272
- https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout
- https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
