# Framework Notes: Email Deliverability

Which sources shape this skill, what each contributes, and which file to open for which question. This skill builds on the shared `references/deliverability-primer.md` (authentication, provider rules, thresholds, validation buckets, warmup) and does not repeat it. Its own files add the operating layer: the pre-send gate, monitoring, testing, incident response and stop rules. Checked 2026-10-13.

## Sources and what they contribute

| Source | Type | Contribution | Where it shows up |
|-|-|-|-|
| Google Email sender guidelines (support.google.com/a/answer/81126, Gmail help copy at support.google.com/mail/answer/81126) | Mailbox provider rule | Requirements for all senders and for 5,000+ a day senders; keep spam rate under 0.10% and never reach 0.30%; ramp slowly, since doubling volume at once can cause rate limiting or reputation drops; pause 10 minutes on `4.7.28` | Pre-send gate, stop rules, recovery calendar, R2, R7 |
| Google Workspace Recommended DMARC rollout, checked 2026-10-13 | Mailbox provider doc | One week at `p=none` with daily reports, then `quarantine` on a small percentage | Six-month audit check 3 |
| Google Workspace Gmail SMTP errors and codes, checked 2026-10-13 | Mailbox provider doc | `421 4.7.28` texts report an unusual rate of (unsolicited) email; `550 5.7.28` is the blocked form; read as a reputation warning | R7, stop rules |
| Google Workspace Set up DKIM, checked 2026-10-13 | Vendor doc | Admin console > Apps > Google Workspace > Gmail > Authenticate email; 2048-bit recommended; selector `google`; Start authentication | R6 recovery records |
| Google sender guidelines FAQ (support.google.com/a/answer/14229414) | Mailbox provider rule | Spam rate calculated daily, keep under 0.1%, never 0.3%; mitigation after 7 consecutive days under 0.3%; guidelines do not apply to mail sent to Workspace accounts; 48-hour unsubscribe; SMTP codes 4.7.23 to 4.7.32 and 5.7.25 to 5.7.30; November 2025 enforcement ramp with rejections | Stop rules, R3, R6 |
| Google Postmaster Tools help (support.google.com/mail/answer/14668346) | Mailbox provider doc | Compliance status per requirement (Compliant, Needs work, No data found), rolling average up to 7 days, primary domains only, low-volume days may lack data | Monitoring section 4 |
| Yahoo Sender Hub best practices | Mailbox provider rule | Spam rate under 0.3% measured on inbox-delivered mail; CFL required for all DKIM domains; one-click unsubscribe with RFC 8058 POST highly recommended; process unsubscribes within 2 days; remove invalid addresses promptly; silent connection closes | Monitoring, R3, R7 |
| Microsoft Outlook high-volume sender announcement (2 Apr 2025, enforced 5 May 2025) | Mailbox provider rule | SPF, DKIM, DMARC `p=none` or stronger with alignment for 5,000+ a day to Outlook.com, Hotmail and Live; `550; 5.7.515`; recommended reply-capable sender addresses, visible unsubscribe, list hygiene | R6, pre-send gate |
| Microsoft delist portal documentation | Mailbox provider doc | `5.7.606-649` banned IP delisting at sender.office.com, up to 24 hours or longer; `5.7.511` goes to delist@microsoft.com | R5 |
| RFC 8058 | Standard | One-click unsubscribe headers, HTTPS POST without cookies or redirects, DKIM must cover both headers | Pre-send gate check 3 |
| RFC 7208, RFC 6376, RFC 7489 and RFC 9989 | Standards | One SPF record and 10-lookup limit; DKIM signing; one DMARC record, alignment, `rua` | Pre-send gate checks 1 and 2, R6 |
| Spamhaus (DBL, checker) | Blocklist operator | Domain listings; check domains in headers and body (URLs); free delisting through the checker; unknown reputations begin as poor; snowshoeing defined as many domains and IPs that change often | R4, incident command, blocklist checks |
| SURBL and URIBL | Blocklist operators | Domain lists matched against links in message bodies; free lookups | Linked-domain blocklist checks, monitoring section 5 |
| Barracuda Central, SpamCop | Blocklist operators | IP listings and removal timing (12 hours typical for Barracuda with a valid explanation; SpamCop auto-expires after 24 hours) | R5 |
| M3AAWG Sender BCP v4.0 (Aug 2026) | Industry body | Ramp and monitoring discipline; volume jumps as a warning sign | R2, R7 |
| Instantly, Smartlead, EmailBison docs | Sequencer docs | Instantly auto-pause at 5% after 200 sends; Instantly readiness after 2 weeks of warmup and a health score above 90%; list-unsubscribe header setting; account error webhooks | R1, R4, R8, recovery plans section 6, pre-send gate |
| Smartlead and GlockApps pricing pages; GlockApps seed list testing guide | Vendor pricing and docs | Placement test tools and prices; GlockApps Smart Test takes one proxy address | Monitoring section 3, incident checks |
| M3AAWG DKIM Key Rotation BCP (rev. March 2019) | Industry body | Rotate DKIM keys at least every six months; 1024-bit minimum, 2048-bit preferred | Six-month audit and its check 2 |
| Microsoft Learn, Rotate DKIM keys; Google Workspace, Set up DKIM | Vendor docs | Microsoft rotation takes 96 hours to switch keys; Google allows a different selector prefix and 2048-bit keys | Six-month audit check 2 |
| Postmark DMARC, dmarcian, Valimail Monitor, EasyDMARC pages (checked 2026-10-13) | Vendor pricing | Free and paid DMARC report parsing, domain limits, history | Monitoring section 8 |
| Apple, Mail Privacy Protection & Privacy, checked 2026-10-13 | Mailbox client doc | Remote content downloads in the background on arrival, whether or not the recipient engages | Recovery plans section 3, step 8a |
| Microsoft Support, automatic picture downloads, checked 2026-10-13 | Mailbox client doc | Outlook blocks automatic picture downloads by default | Recovery plans section 3 |
| lemlist help, legitimate clicks and opens, checked 2026-10-13 | Sequencer doc | Security filters (Proofpoint, Barracuda named) open and click within seconds | Recovery plans section 3 |
| Microsoft Learn, NDR 550 5.1.10 | Mailbox provider doc | Recipient address not found at Exchange Online | Recovery plans section 2b |
| Alex Berman (alexberman.com, cold email templates and TAM strategy breakdown, checked 2026-10-13) | Operator | Keep bounces under 2%; start new domains at 10 to 20 a day and ramp over 2 to 4 weeks; 2 to 3 inboxes per domain; under 50 a day per inbox; verify the list before sending | Stop rules, domain status, recovery calendar |
| ScraperCity catalog and Email Validator page | Tool facts | `validate_emails` at $0.00169; `email_result`, `email_quality`, `sc_is_catch_all`, `sc_mx_provider`, `sc_mx_security_gateway`; `find_emails` at $0.05 per email found | ScraperCity Implementation, monitoring section 2 |

## Where sources differ, and the rule this skill uses

| Topic | Sources | Rule here |
|-|-|-|
| Spam rate line | Google: under 0.1%, never 0.3%. Yahoo: under 0.3% | Act at 0.1% on any day, stop at 0.3% |
| Bounce line | Instantly default auto-pause above 5% after 200 sends; Berman under 2% | Pause a campaign or mailbox at 2% over its last 200 sends |
| Unsubscribe time | Yahoo 2 days; Google 48 hours | Same day, in every tool |
| Which rules apply to B2B cold email | Google's rules exclude mail to Workspace accounts; Microsoft's cover consumer Outlook domains | Build to every rule anyway; judge B2B placement by seeds and reply rate per recipient provider |
| Opt-out rate | No provider publishes a line | No threshold: report it per campaign against the program's own baseline |
| DKIM rotation | M3AAWG: at least every six months. Microsoft and Google offer rotation but set no schedule | Rotate every six months, checked in the six-month audit |
| Postmaster data | Google documents dashboards; low volume may show no data; spam rate counts inbox-delivered mail only | Use it when data shows; never treat "No data found" or a low spam rate as proof of inbox placement |
| Open rate | Sequencers report it; Apple MPP, Outlook image blocking and security filters distort it | Never a decision metric; seeds, replies per 1,000 sends and bounce codes decide |
| Restart volume after an incident | Berman: new domains start at 10 to 20 a day and ramp over 2 to 4 weeks. Google: no sudden doubling | Incident plans restart every inbox at 10 and step up weekly, never more than double, back to the previous cap |
| Validation re-check window, catch-all share of volume | No source publishes either | User settings, read from their own bounce data |

## Routing table

| Question | Open |
|-|-|
| What must pass before a campaign launches? | `references/monitoring-and-testing.md` section 1 |
| What do I do with catch-all, low quality or gateway rows? | `references/monitoring-and-testing.md` section 2 |
| How do I run a seed test? | `references/monitoring-and-testing.md` section 3 |
| What do Postmaster, CFL and SNDS tell me? | `references/monitoring-and-testing.md` section 4 |
| How do I check blocklists? | `references/monitoring-and-testing.md` section 5 |
| Opens collapsed and bounces jumped; give me a plan | `references/recovery-plans.md` |
| Bounces jumped; what now? | `references/incident-runbooks.md` R1 |
| Mail goes to spam | `references/incident-runbooks.md` R2 |
| Complaint rate is up | `references/incident-runbooks.md` R3 |
| Domain or IP blocklisted | `references/incident-runbooks.md` R4 and R5 |
| Opens dropped but replies did not | `references/incident-runbooks.md` R9 |
| Who can pause a domain; can we buy new domains now? | `references/incident-runbooks.md` Incident command |
| What does this SMTP code mean? | `references/incident-runbooks.md` R6 and R7 |
| Provider rules, thresholds, validation buckets | `references/deliverability-primer.md` |
| Required columns, freshness, suppression | `references/list-quality-standard.md` |
| What goes in the six-month audit? | `references/monitoring-and-testing.md` section 7 |
| Which DMARC report service? | `references/monitoring-and-testing.md` section 8 |
| Is this opt-out rate too high? | `references/monitoring-and-testing.md` section 9 |

## What this skill does not claim

- No inbox placement percentage is promised for any setup, tool or copy.
- Seed tests are samples; a seed result does not predict placement for every recipient.
- "Warmup fixes spam placement" is not claimed. Warmup builds history; it does not cancel complaints, bad lists or broken authentication.

## Sources

- https://support.google.com/a/answer/81126
- https://support.google.com/mail/answer/81126
- https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout
- https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
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
- https://www.spamhaus.org/news/article/650/
- https://knowledge.workspace.google.com/admin/support/troubleshooting/gmail-smtp-errors-and-codes
- https://knowledge.workspace.google.com/admin/security/set-up-dkim
- https://www.surbl.org/
- https://uribl.com/
- https://www.barracudacentral.org/rbl/removal-request
- https://www.spamcop.net/fom-serve/cache/298.html
- https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://alexberman.com/cold-email-templates
- https://scrapercity.com/email-validator
- https://www.m3aawg.org/DKIMKeyRotation
- https://dmarc.postmarkapp.com/
- https://dmarcian.com/pricing/
- https://www.valimail.com/products/monitor/
- https://easydmarc.com/pricing
- https://www.apple.com/legal/privacy/data/en/mail-privacy-protection/
- https://support.microsoft.com/en-us/office/block-or-unblock-automatic-picture-downloads-in-email-messages-15e08854-6808-49b1-9a0a-50b81f2d617a
- https://help.lemlist.com/en/articles/9140285-identifying-legitimate-clicks-and-opens
- https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/non-delivery-reports-in-exchange-online/fix-error-code-550-5-1-10-in-exchange-online
