# Deliverability Primer

Shared reference for every outbound skill in this repo. It covers authentication, mailbox provider rules with dates, bounce and complaint numbers, how to treat each email validation result, warmup, and the standing thresholds every skill uses. Facts were checked against the primary sources listed at the end on 2026-10-12. Thresholds marked "house standard" are ScraperCity operating defaults: starting points to test against your own bounce and reply data, never guarantees.

Skills that load this file: `domain-infrastructure`, `inbox-setup`, `email-deliverability`, `sending-platforms`, `cold-email-strategy`, `cold-email-list`, `email-list-cleaner`.

## 1. Authentication

Three DNS-published checks tell a receiving server that a message from `you@yourdomain.com` was sent with your permission.

| Check | Standard | What it proves | Record lives at | Failure mode to know |
|-|-|-|-|-|
| SPF | RFC 7208 (2014) | The connecting server's IP is allowed to send for the envelope sender (Return-Path) domain | TXT on the domain, starts `v=spf1` | More than 10 DNS-querying terms (`include`, `a`, `mx`, `ptr`, `exists`, `redirect`) returns `permerror` (RFC 7208 section 4.6.4). Only one SPF record per domain. |
| DKIM | RFC 6376 (2011) | The message was signed by a key the `d=` domain publishes and was not altered in transit | TXT at `<selector>._domainkey.<domain>` (Google) or CNAME to the provider (Microsoft 365) | RFC 6376 requires signers to use RSA keys of at least 1024 bits for long-lived keys. Google recommends 2048-bit when the DNS host supports it. Microsoft 365 defaults to 1024 and can rotate to 2048. |
| DMARC | RFC 7489 (2015), replaced by RFC 9989 (May 2026) | The visible From domain aligns with a domain that passed SPF or DKIM, and tells receivers what to do on failure | TXT at `_dmarc.<domain>`, starts `v=DMARC1` | Two DMARC records at the same name means receivers apply no DMARC at all (RFC 7489 section 6.6.3). |

### Alignment

DMARC passes when at least one of these is true:

- **DKIM alignment:** the DKIM `d=` domain matches the From domain. Relaxed mode (`adkim=r`, the default) accepts any domain under the same organizational domain, so `d=mail.acme-hq.com` aligns with `From: jo@acme-hq.com`. Strict (`adkim=s`) needs an exact match.
- **SPF alignment:** the Return-Path domain that passed SPF matches the From domain, relaxed by default (`aspf=r`).

Cold email sent from Google Workspace or Microsoft 365 mailboxes through a sequencer that connects by OAuth or SMTP is signed by the mailbox provider with your domain's key, so DKIM alignment passes once the DKIM record is published and signing is turned on. Check one sent message's headers for `dkim=pass header.d=<your domain>` and `dmarc=pass` before any campaign starts.

### DMARC tags you will use

| Tag | Meaning | Value for a new cold email domain |
|-|-|-|
| `v` | Version, first tag | `DMARC1` |
| `p` | Policy for the domain | `none` for the first 30 days while reports confirm alignment, then `quarantine` (house standard) |
| `sp` | Policy for subdomains | Omit; inherits `p` |
| `rua` | Where aggregate reports go | Required by house standard. Yahoo strongly recommends it. Under RFC 9989 receivers send no aggregate reports when `rua` is absent. |
| `adkim`, `aspf` | Alignment mode | Omit (relaxed default) |
| `pct` | Percent of mail the policy applies to | Omit. RFC 9989 removed `pct`; Gmail BIMI still asks for `pct=100` if present. |

Example: `v=DMARC1; p=none; rua=mailto:dmarc-reports@yourmaindomain.com`

When the `rua` address sits on a different domain from the one publishing the record, the receiving domain must publish an authorization record (`<sendingdomain>._report._dmarc.<reportdomain>` TXT `v=DMARC1`) or reports are dropped. A hosted DMARC report service gives you an address that already has this set up.

## 2. Mailbox provider requirements, with dates

| Provider | Applies to | Requirement | In force since | Source |
|-|-|-|-|-|
| Google | All senders to personal Gmail accounts | SPF or DKIM; valid forward and reverse DNS (PTR) for sending IPs; TLS; RFC 5322 format; spam rate in Postmaster Tools below 0.3%; no impersonation of Gmail From headers | 1 Feb 2024 | support.google.com/a/answer/81126 |
| Google | Senders of about 5,000+ messages a day to personal Gmail accounts ("bulk senders") | All of the above plus SPF and DKIM; DMARC record (policy may be `none`); From domain aligned with SPF or DKIM; one-click unsubscribe (RFC 8058) plus a visible unsubscribe link for marketing and subscribed messages | 1 Feb 2024; one-click deadline 1 Jun 2024 | support.google.com/a/answer/81126, FAQ answer/14229414 |
| Google | Enforcement | Spam rate at or above 0.3% makes a bulk sender ineligible for mitigation until it stays below 0.3% for 7 consecutive days. From November 2025 Gmail ramps up enforcement, including temporary and permanent rejections of non-compliant traffic. | Jun 2024; Nov 2025 | FAQ answer/14229414 |
| Yahoo | All senders | SPF or DKIM; spam rate below 0.3%; valid forward and reverse DNS; RFC 5321 and 5322 | Feb 2024 | senders.yahooinc.com/best-practices |
| Yahoo | Bulk senders (Yahoo publishes no volume number) | SPF and DKIM; DMARC at least `p=none` that passes; From aligned with SPF or DKIM; one-click unsubscribe (RFC 8058 POST highly recommended, mailto acceptable) plus a visible body link; honor unsubscribes within 2 days | Feb 2024; unsubscribe Jun 2024 | senders.yahooinc.com/best-practices, /faqs |
| Microsoft (Outlook.com, Hotmail.com, Live.com consumer) | Domains sending more than 5,000 messages a day to those consumer domains | SPF pass, DKIM pass, DMARC at least `p=none` aligned with SPF or DKIM (ideally both) | 5 May 2025 | techcommunity.microsoft.com announcement (2 Apr 2025, updated late Apr 2025); Outlook.com sender policies |
| Microsoft | Enforcement | Non-compliant mail goes to Junk or is rejected with `550; 5.7.515 Access denied, sending domain [SendingDomain] does not meet the required authentication level.` The announcement's 29 April update moved to rejection; the Outlook.com policy page still describes Junk first. Plan for rejection. | 5 May 2025 | Same |

### What this means for B2B cold email

1. **Google's bulk rules count by primary domain.** Mail from `acme-hq.com` and `go.acme-hq.com` adds up to one total. Once a domain qualifies as a bulk sender, the status does not expire (FAQ answer/14229414). A cold email setup spread across separate sending domains, each sending a few hundred messages a day, stays far under 5,000 per domain. Build to the bulk sender rules anyway: SPF, DKIM and DMARC on every domain cost nothing.
2. **Google's sender guidelines do not apply to messages sent to Google Workspace accounts** (FAQ answer/14229414). Most B2B recipients sit on Workspace or Microsoft 365, where the receiving organization's own filters and admins decide. Postmaster Tools reports traffic to personal Gmail, so a pure B2B program may see little data there. Seed tests and reply rates per recipient provider carry more signal.
3. **Microsoft's rules cover consumer Outlook domains,** not Microsoft 365 business tenants. Business recipients behind Exchange Online Protection or a security gateway (Mimecast, Proofpoint, Barracuda) apply their own filtering. ScraperCity's Email Validator returns `sc_mx_provider` and `sc_mx_security_gateway`, which lets you see which provider and gateway each recipient sits behind before you send.
4. **Unsubscribe:** Google and Yahoo require one-click unsubscribe for marketing and subscribed messages from bulk senders. Neither provider's FAQ addresses one-to-one cold outreach directly. CAN-SPAM covers B2B commercial email in the US and requires a working opt-out honored within 10 business days (FTC compliance guide). House standard for cold email: every message carries a plain opt-out line, every opt-out is suppressed workspace-wide within 24 hours, and the sequencer's unsubscribe header is on when the platform supports it. See `references/outbound-compliance-primer.md` for the law by country.

## 3. One-click unsubscribe (RFC 8058)

RFC 8058 (January 2017) defines two headers that let a mailbox provider show its own unsubscribe button and send the opt-out for the recipient:

```text
List-Unsubscribe: <https://u.yourdomain.com/u/8f3k2>, <mailto:unsub@yourdomain.com?subject=8f3k2>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

Sender rules from the RFC: an HTTPS URI must be present; the POST must succeed without cookies, login or a redirect; the DKIM signature must cover both headers. Sequencers that support the header add it per campaign. Check one test message's raw headers before launch.

## 4. Bounce and complaint numbers

| Metric | Formula | Window | Who measures it |
|-|-|-|-|
| Hard bounce rate | permanent failures (5xx: no such user, domain has no MX) / messages sent | Per campaign, per mailbox, rolling 200 sends | Your sequencer |
| Soft bounce rate | temporary failures (4xx: mailbox full, rate limited, greylisted) / messages sent | Same | Your sequencer |
| Spam (complaint) rate | spam reports / messages delivered to the inbox | Daily | Google Postmaster Tools (personal Gmail only), Yahoo CFL, Microsoft JMRP |
| Reply rate | replies (excluding auto-replies) / prospects contacted | Per campaign | Your sequencer |

Worked numbers:

- **Complaint ceiling at small volume.** A domain sending 300 messages a day to personal Gmail that draws 1 spam report is at 1 / 300 = 0.33%, over Google's 0.3% line. At 1,000 a day, 1 report is 0.1%. Low per-domain volume makes the rate swing hard, so judge complaints over 7 days and act on the trend.
- **Bounce budget.** A campaign of 2,000 sends at a 2% hard bounce ceiling allows 40 bounces. A list of 2,000 addresses that are all `valid` per the validator usually bounces well under that; a list with 10% `invalid` rows would produce about 200 bounces, 10%, and trip every sequencer auto-pause.
- **Validation pays for itself.** Validating 2,000 addresses with `validate_emails` costs 2,000 x $0.0072 = $14.40. One burned domain costs the domain fee, 2 to 3 mailbox seats for the months left on the plan, and 2 to 4 weeks of warmup time.

## 5. Email validation results and what to do with each

ScraperCity's Email Validator (`validate_emails`, $0.0072 per email) returns `email_result` with one of five values, a quality rating in `email_quality` (high, medium or low), and enrichment columns including `sc_is_catch_all`, `sc_mx_provider` and `sc_mx_security_gateway` (per scrapercity.com/email-validator, checked 2026-10-12). Read the header row of the downloaded CSV before mapping, since columns can change between versions. The buckets below match `references/list-quality-standard.md`.

| `email_result` | Bucket | Cold email action (house standard) | Suppression |
|-|-|-|-|
| `valid` | valid | Send-ready file. Low `email_quality` rows go last in the send order. | None |
| `valid_catch_all` | catch_all | Separate file and separate campaign, capped at 10% of a day's volume, from mailboxes with the most warmup history. Pause that campaign if its hard bounces pass 3% over 200 sends. | Suppress any address that bounces |
| `unknown` | unknown | Hold. Re-validate once after 72 hours. Still `unknown`: treat as catch_all or drop. | None until it bounces |
| `invalid` | invalid | Remove from every send file. Try `find_emails` ($0.05 per email found, free if none) with name and domain for a replacement. | Add to the workspace blocklist |
| `disposable` | disposable | Remove. | Add to the workspace blocklist |

Re-validate anything older than 30 days before a send (house standard; mailboxes close when people change jobs).

## 6. Warmup

Warmup is a period of low, rising volume that builds a sending history for a new domain and mailbox before cold campaigns start.

| Source | What it says |
|-|-|
| M3AAWG Sender Best Common Practices v4.0 (Aug 2026) | Begin with low volume and increase gradually; about six weeks is an average warm-up period. Spread sends through the day. Artificial warming is not recommended. |
| Google Email sender guidelines | Increase volume slowly; sudden spikes, such as doubling previous volume at once, can trigger rate limits or reputation drops. On SMTP error 4.7.28, pause at least 10 minutes. |
| Instantly help center | An account is ready for campaigns after at least 2 weeks of warmup and a health score above 90% over the last 7 days. New-account defaults: 1 extra warmup email a day, daily warmup limit 10, reply rate 30%. |
| Alex Berman, alexberman.com | Start new domains at roughly 10 to 20 emails a day and increase over 2 to 4 weeks. A beginner setup of 3 to 5 domains, 2 to 3 inboxes per domain, under 50 emails per inbox per day. |

M3AAWG's guidance is written for permission-based mail and treats cold email as abusive; quote it for ramp shape and monitoring only. Sequencer warmup pools (automated sends between participating mailboxes) are the "artificial warming" M3AAWG does not recommend. Operators use them anyway to build early history; the house standard runs pool warmup for 14 days, then keeps it on at a low rate while real campaigns ramp, and treats real replies from real prospects as the signal that counts.

House ramp for a new mailbox (cold sends, on top of warmup):

| Days since mailbox created | Cold sends per mailbox per day |
|-|-|
| 1 to 14 | 0 (warmup only) |
| 15 to 21 | 10 |
| 22 to 28 | 20 |
| 29 onward | 30, raise to a maximum of 50 only while bounces stay under 2% and complaints under 0.1% |

## 7. Standing thresholds

Every outbound skill in this repo uses these numbers.

| Metric | Target | Act at | Stop at | Basis |
|-|-|-|-|-|
| Spam complaint rate (Postmaster Tools, Yahoo CFL) | Under 0.1% | 0.1% for 2 days: cut volume 50% on that domain | 0.3%: stop the domain | Google sender guidelines and FAQ; Yahoo best practices |
| Hard bounce rate (per campaign, rolling 200 sends) | Under 1% | 2%: pause the campaign, re-validate the remaining list | 3% on a mailbox: pause the mailbox | alexberman.com (under 2%); house standard. Instantly's default auto-pause is 5% after 200 sends; set yours lower. |
| Email validation status in the send file | 100% `valid` | Any `invalid` or `disposable`: remove before upload | A source with over 15% `invalid`: stop and check the source | `references/list-quality-standard.md` |
| Catch-all share of daily volume | 10% or less | Over 10%: move excess to the next day | Catch-all campaign bounces over 3%: stop catch-alls | House standard |
| Cold sends per mailbox per day | 30 | Raise to 50 only on a clean 14-day record | Over 50: not allowed | alexberman.com (under 50); Apollo recommends 50 to 100 per mailbox with 10 to 20 an hour; house standard is stricter |
| Mailboxes per sending domain | 2 to 3 | 4 or more: spread to a new domain | | alexberman.com |
| Warmup before first cold send | 14 days minimum | | Any cold send before day 15 | Instantly readiness rule; alexberman.com 2 to 4 weeks |
| Messages per sending domain per day to personal Gmail | Well under 5,000 | | 5,000 makes the primary domain a permanent bulk sender | Google FAQ |
| DMARC | `p=none` with `rua` from day 1 | Move to `quarantine` after 30 days of aligned reports | Missing or duplicate DMARC record: do not send | Google, Yahoo, Microsoft requirements; RFC 7489, RFC 9989 |
| Opt-out handling | Suppressed within 24 hours | | Any opt-out mailed again | Google 48 hours, Yahoo 2 days, CAN-SPAM 10 business days; house standard is faster |

## 8. Monitoring tools

| Tool | What it shows | Setup | Limits |
|-|-|-|-|
| Google Postmaster Tools | Compliance status, spam rate, authentication, encryption, delivery errors, feedback loop; Google's help page also lists IP and domain reputation dashboards | Add the sending domain and verify it with a DNS TXT record | Traffic to personal Gmail only. Low-volume days may show no data. Postmastery reported in 2025 that the v1 interface retired on 30 Sep 2025 and the reputation dashboards were dropped; read whatever your account shows. |
| Microsoft SNDS and JMRP | Per-IP data for mail to Outlook.com; JMRP sends a report when a recipient marks your mail as junk | Sign in with a Microsoft account and request access to IPs you control | IP-based. Workspace and Microsoft 365 senders do not own their sending IPs, so SNDS helps only dedicated-IP senders (for example EmailBison or ManyReach private IPs). |
| Yahoo Complaint Feedback Loop | Complaint reports for DKIM domains you enroll | Enroll each DKIM `d=` domain in Yahoo Sender Hub | Domain-based since 2024; IP-based reporting retired |
| Spamhaus IP and Domain Reputation Checker (check.spamhaus.org) | Whether a domain is on the Domain Blocklist (DBL) or an IP is listed | None | Spamhaus says new domains start with a poor reputation by default and that rapidly rotating many domains is treated as snowshoe spamming. Delisting is free and only through the checker. |
| Seed or placement test | Inbox vs spam vs missing per provider for one message | A seed list of mailboxes at Gmail, Workspace, Outlook.com and Microsoft 365 | A sample, not a census; repeat weekly |

## Sources

- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Google, Postmaster Tools dashboards: https://support.google.com/mail/answer/14668346
- Google Workspace, Set up SPF: https://knowledge.workspace.google.com/admin/security/set-up-spf
- Google Workspace, Set up DKIM: https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Google Workspace, Set up MX records: https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Yahoo Sender Hub, FAQs: https://senders.yahooinc.com/faqs/
- Microsoft, Strengthening email ecosystem: Outlook's new requirements for high-volume senders (Apr 2025): https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Microsoft, Outlook.com sender policies: https://substrate.office.com/ip-domain-management-snds/postmaster/Policies
- Microsoft, SNDS: https://sendersupport.olc.protection.outlook.com/snds/
- Microsoft, Configure DKIM for Microsoft 365: https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
- RFC 7208, SPF: https://www.rfc-editor.org/rfc/rfc7208
- RFC 6376, DKIM Signatures: https://www.rfc-editor.org/rfc/rfc6376
- RFC 7489, DMARC: https://www.rfc-editor.org/rfc/rfc7489
- RFC 9989, DMARC (May 2026): https://www.rfc-editor.org/rfc/rfc9989.html
- RFC 9990, DMARC Aggregate Reporting (May 2026): https://www.rfc-editor.org/rfc/rfc9990.html
- RFC 8058, One-click unsubscribe: https://www.rfc-editor.org/rfc/rfc8058
- M3AAWG Sender Best Common Practices v4.0 (Aug 2026): https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- Spamhaus, Domain Blocklist: https://www.spamhaus.org/blocklists/domain-blocklist/
- Postmastery, Gmail Postmaster Tools v1 is retiring: https://www.postmastery.com/gmail-postmaster-tools-v1-is-retiring-what-you-need-to-know/
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, Warmup settings: https://help.instantly.ai/en/articles/7988514-warmup-settings
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Apollo, Configure email sending limits: https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- Alex Berman, cold email templates (warmup and bounce guidance): https://alexberman.com/cold-email-templates
- Alex Berman, TAM strategy breakdown (domain and inbox setup): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- ScraperCity, Email Validator: https://scrapercity.com/email-validator
