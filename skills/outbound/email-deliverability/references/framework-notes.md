# Framework Notes: Email Deliverability

Which sources shape this skill, what each contributes, and which file to open for which question. This skill builds on the shared `references/deliverability-primer.md` (authentication, provider rules, thresholds, validation buckets, warmup) and does not repeat it. Its own files add the operating layer: the pre-send gate, monitoring, testing, incident response and stop rules. Checked 2026-10-13.

## Sources and what they contribute

| Source | Type | Contribution | Where it shows up |
|-|-|-|-|
| Google Email sender guidelines (support.google.com/a/answer/81126) | Mailbox provider rule | Requirements for all senders and for 5,000+ a day senders; ramp slowly; pause 10 minutes on `4.7.28` | Pre-send gate, R7 |
| Google sender guidelines FAQ (support.google.com/a/answer/14229414) | Mailbox provider rule | Spam rate calculated daily, keep under 0.1%, never 0.3%; mitigation after 7 consecutive days under 0.3%; guidelines do not apply to mail sent to Workspace accounts; 48-hour unsubscribe; SMTP codes 4.7.23 to 4.7.32 and 5.7.25 to 5.7.30; November 2025 enforcement ramp with rejections | Stop rules, R3, R6 |
| Google Postmaster Tools help (support.google.com/mail/answer/14668346) | Mailbox provider doc | Compliance status per requirement (Compliant, Needs work, No data found), rolling average up to 7 days, primary domains only, low-volume days may lack data | Monitoring section 4 |
| Yahoo Sender Hub best practices | Mailbox provider rule | Spam rate under 0.3% measured on inbox-delivered mail; CFL required for all DKIM domains; one-click unsubscribe with RFC 8058 POST highly recommended; process unsubscribes within 2 days; remove invalid addresses promptly; silent connection closes | Monitoring, R3, R7 |
| Microsoft Outlook high-volume sender announcement (2 Apr 2025, enforced 5 May 2025) | Mailbox provider rule | SPF, DKIM, DMARC `p=none` or stronger with alignment for 5,000+ a day to Outlook.com, Hotmail and Live; `550; 5.7.515`; recommended reply-capable sender addresses, visible unsubscribe, list hygiene | R6, pre-send gate |
| Microsoft delist portal documentation | Mailbox provider doc | `5.7.606-649` banned IP delisting at sender.office.com, up to 24 hours or longer; `5.7.511` goes to delist@microsoft.com | R5 |
| RFC 8058 | Standard | One-click unsubscribe headers, HTTPS POST without cookies or redirects, DKIM must cover both headers | Pre-send gate check 3 |
| RFC 7208, RFC 6376, RFC 7489 and RFC 9989 | Standards | One SPF record and 10-lookup limit; DKIM signing; one DMARC record, alignment, `rua` | Pre-send gate checks 1 and 2, R6 |
| Spamhaus (DBL, checker) | Blocklist operator | Domain listings; free delisting through the checker; new domains start poor; snowshoeing | R4 |
| Barracuda Central, SpamCop | Blocklist operators | IP listings and removal timing (12 hours typical for Barracuda with a valid explanation; SpamCop auto-expires after 24 hours) | R5 |
| M3AAWG Sender BCP v4.0 (Aug 2026) | Industry body | Ramp and monitoring discipline; volume jumps as a warning sign | R2, R7 |
| Instantly, Smartlead, EmailBison docs | Sequencer docs | Auto-pause defaults, list-unsubscribe header setting, account error webhooks | R1, R8, pre-send gate |
| Smartlead and GlockApps pricing pages | Vendor pricing | Placement test tools and prices | Monitoring section 3 |
| Alex Berman (alexberman.com) | Operator | Keep bounces under 2% | Stop rules |
| ScraperCity catalog and Email Validator page | Tool facts | `validate_emails` at $0.0072; `email_result`, `email_quality`, `sc_is_catch_all`, `sc_mx_provider`, `sc_mx_security_gateway`; `find_emails` at $0.05 per email found | ScraperCity Implementation, monitoring section 2 |

## Where sources differ, and the rule this skill uses

| Topic | Sources | Rule here |
|-|-|-|
| Spam rate line | Google: under 0.1%, never 0.3%. Yahoo: under 0.3% | Act at 0.1% for 2 days, stop at 0.3% |
| Bounce line | Instantly default auto-pause above 5% after 200 sends; Berman under 2% | Pause a campaign at 2%, a mailbox at 3% |
| Unsubscribe time | CAN-SPAM 10 business days; Yahoo 2 days; Google 48 hours | Same day, 24 hours at most |
| Which rules apply to B2B cold email | Google's rules exclude mail to Workspace accounts; Microsoft's cover consumer Outlook domains | Build to every rule anyway; judge B2B placement by seeds and reply rate per recipient provider |
| Postmaster data | Google documents dashboards; low volume may show no data | Use it when data shows; never treat "No data found" as healthy |

## Routing table

| Question | Open |
|-|-|
| What must pass before a campaign launches? | `references/monitoring-and-testing.md` section 1 |
| What do I do with catch-all, low quality or gateway rows? | `references/monitoring-and-testing.md` section 2 |
| How do I run a seed test? | `references/monitoring-and-testing.md` section 3 |
| What do Postmaster, CFL and SNDS tell me? | `references/monitoring-and-testing.md` section 4 |
| How do I check blocklists? | `references/monitoring-and-testing.md` section 5 |
| Bounces jumped; what now? | `references/incident-runbooks.md` R1 |
| Mail goes to spam | `references/incident-runbooks.md` R2 |
| Complaint rate is up | `references/incident-runbooks.md` R3 |
| Domain or IP blocklisted | `references/incident-runbooks.md` R4 and R5 |
| What does this SMTP code mean? | `references/incident-runbooks.md` R6 and R7 |
| Provider rules, thresholds, validation buckets | `references/deliverability-primer.md` |
| Required columns, freshness, suppression | `references/list-quality-standard.md` |
| Opt-out law by country | `references/outbound-compliance-primer.md` |

## What this skill does not claim

- No inbox placement percentage is promised for any setup, tool or copy.
- Seed tests are samples; a seed result does not predict placement for every recipient.
- "Warmup fixes spam placement" is not claimed. Warmup builds history; it does not cancel complaints, bad lists or broken authentication.

## Sources

- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://support.google.com/mail/answer/14668346
- https://senders.yahooinc.com/best-practices/
- https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- https://learn.microsoft.com/en-us/defender-office-365/external-senders-use-the-delist-portal-to-unblock-yourself
- https://www.rfc-editor.org/rfc/rfc8058
- https://www.rfc-editor.org/rfc/rfc7208
- https://www.rfc-editor.org/rfc/rfc6376
- https://www.rfc-editor.org/rfc/rfc7489
- https://www.rfc-editor.org/rfc/rfc9989.html
- https://www.spamhaus.org/blocklists/domain-blocklist/
- https://www.barracudacentral.org/rbl/removal-request
- https://www.spamcop.net/fom-serve/cache/298.html
- https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://alexberman.com/cold-email-templates
- https://scrapercity.com/email-validator
