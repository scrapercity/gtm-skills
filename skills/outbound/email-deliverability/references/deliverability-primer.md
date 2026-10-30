# Deliverability Primer

Shared reference for every outbound skill in this repo. It covers authentication, mailbox provider rules with dates, bounce and complaint numbers, how to treat each email validation result, warmup, and the standing thresholds every skill uses. Facts were checked against the primary sources listed at the end on 2026-10-12, and sections 6 to 9 again on 2026-10-13. Every threshold names its source; where no source publishes a number, the table says it is the user's own setting.

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
| `p` | Policy for the domain | `none` while reports confirm alignment, then `quarantine`. Google's DMARC rollout guide says one week of daily reports is usually enough before quarantine, applied to a small percentage first |
| `sp` | Policy for subdomains | Omit; inherits `p` |
| `rua` | Where aggregate reports go | Set it. Yahoo strongly recommends it, and under RFC 9989 receivers send no aggregate reports when `rua` is absent. |
| `adkim`, `aspf` | Alignment mode | Omit (relaxed default) |
| `pct` | Percent of mail the policy applies to | Omit. RFC 9989 removed `pct`; Gmail BIMI still asks for `pct=100` if present. |

Example: `v=DMARC1; p=none; rua=mailto:dmarc-reports@yourmaindomain.com`

When the `rua` address sits on a different domain from the one publishing the record, the receiving domain must publish an authorization record or reports are dropped. RFC 7489 section 7.1 and RFC 9990 section 4 allow one wildcard for every sending domain: `*._report._dmarc.<reportdomain>` TXT `v=DMARC1`. That is one change to the main domain instead of one per sending domain (`<sendingdomain>._report._dmarc.<reportdomain>`); the trade-off is that any domain can then send reports to that address. A hosted DMARC report service gives you an address that already has this set up.

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
2. **Google's sender guidelines do not apply to messages sent to Google Workspace accounts** (FAQ answer/14229414). B2B recipients often sit on Workspace or Microsoft 365, where the receiving organization's own filters and admins decide. Postmaster Tools reports traffic to personal Gmail, so a pure B2B program may see little data there. Seed tests and reply rates per recipient provider carry more signal.
3. **Microsoft's rules cover consumer Outlook domains,** not Microsoft 365 business tenants. Business recipients behind Exchange Online Protection or a security gateway (Mimecast, Proofpoint, Barracuda) apply their own filtering. ScraperCity's Email Validator returns `sc_mx_provider` and `sc_mx_security_gateway`, which lets you see which provider and gateway each recipient sits behind before you send.
4. **Unsubscribe:** Google and Yahoo require one-click unsubscribe for marketing and subscribed messages from bulk senders. Neither provider's FAQ addresses one-to-one cold outreach directly. Settings for cold email: every message carries a plain opt-out line, every opt-out is suppressed the same day across every tool, and the sequencer's unsubscribe header is on when the platform supports it. Google processes, and asks bulk senders to process, unsubscribes within 48 hours; Yahoo within 2 days.

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

- **Complaint ceiling at small volume.** A domain sending 300 messages a day to personal Gmail that draws 1 spam report is at 1 / 300 = 0.33%, over Google's 0.3% line. At 1,000 a day, 1 report is 0.1%. At low per-domain volume one report moves the rate by a tenth of a point or more, so read the trend across days, as Google's own mitigation rule does (7 consecutive days under 0.3%).
- **Bounce budget.** A campaign of 2,000 sends at Alex Berman's 2% hard bounce line allows 40 bounces. A list with 10% `invalid` rows would produce about 200 bounces, 10%, past Instantly's default 5% auto-pause.
- **Validation cost against a burned domain.** Validating 2,000 addresses with `validate_emails` costs 2,000 x $0.00169 = $3.38. A replacement domain costs the domain fee, its 2 to 3 mailbox seats (Berman's inboxes per domain), and 2 to 4 weeks of warmup (Berman) before it sends.

## 5. Email validation results and what to do with each

ScraperCity's Email Validator (`validate_emails`, $0.00169 per email) returns `email_result` with one of five values, a quality rating in `email_quality` (high, medium or low), and enrichment columns including `sc_is_catch_all`, `sc_mx_provider` and `sc_mx_security_gateway` (per scrapercity.com/email-validator, checked 2026-10-12). Read the header row of the downloaded CSV before mapping, since columns can change between versions. The buckets below match `references/list-quality-standard.md`.

| `email_result` | Bucket | Cold email action | Suppression |
|-|-|-|-|
| `valid` | valid | Send-ready file. Low `email_quality` rows go last in the send order. | None |
| `valid_catch_all` | catch_all | Separate file and separate campaign, so the sequencer's bounce auto-pause trips on that campaign only. Its share of daily volume is your setting. Pause it when its hard bounces pass 2% over 200 sends (Berman's line, Instantly's 200-send window). | Suppress any address that bounces |
| `unknown` | unknown | Hold. Re-validate once. Still `unknown`: treat as catch_all or drop. | None until it bounces |
| `invalid` | invalid | Remove from every send file. Try `find_emails` ($0.05 per email found, free if none) with name and domain for a replacement. | Add to the workspace blocklist |
| `disposable` | disposable | Remove. | Add to the workspace blocklist |

Re-validate any row whose last check is older than your re-check window before it is sent. Set the window from your own data: the bounce rate of re-sent rows by age since validation.

## 6. Warmup

Warmup is a period of low, rising volume that builds a sending history for a new domain and mailbox before cold campaigns start.

| Source | What it says |
|-|-|
| M3AAWG Sender Best Common Practices v4.0 (Aug 2026) | Begin with low volume and increase gradually; about six weeks is an average warm-up period. Spread sends through the day. Artificial warming is not recommended. |
| Google Email sender guidelines | Increase volume slowly; sudden spikes, such as doubling previous volume at once, can trigger rate limits or reputation drops. On SMTP error 4.7.28, pause at least 10 minutes. Gmail's 4.7.28 texts report an unusual rate of unsolicited email from your IP or domain, so treat it as a reputation warning as well as a deferral (Gmail SMTP error reference, checked 2026-10-13). |
| Instantly help center | An account is ready for campaigns after at least 2 weeks of warmup and a health score above 90% over the last 7 days. New-account defaults: 1 extra warmup email a day, daily warmup limit 10, reply rate 30%. |
| Alex Berman, alexberman.com | Start new domains at roughly 10 to 20 emails a day and increase over 2 to 4 weeks. A beginner setup of 3 to 5 domains, 2 to 3 inboxes per domain, under 50 emails per inbox per day. |

M3AAWG's guidance is written for permission-based mail; quote it for ramp shape and monitoring only. Sequencer warmup pools (automated sends between participating mailboxes) are the "artificial warming" M3AAWG does not recommend. Operators use them to build early history; Instantly's readiness rule is at least 2 weeks of warmup and a health score above 90%.

Ramp for a new mailbox (cold sends, on top of warmup):

| Stage | Cold sends per mailbox per day | Source |
|-|-|-|
| Warmup | 0 until at least 2 weeks of warmup and a health score above 90% | Instantly help center |
| First cold sends | 10 to 20 | Alex Berman, alexberman.com |
| Ramp | Raise over 2 to 4 weeks to your cap; no single step doubles the previous day's volume | Berman; Google sender guidelines (doubling volume at once can cause rate limiting or reputation drops) |
| Cap | Under 50, while bounces stay under 2% and the spam rate under 0.1% | Berman (under 50 per inbox, bounces under 2%); Google (spam rate under 0.1%) |

## 7. Standing thresholds

Every outbound skill in this repo uses these numbers.

| Metric | Target | Act at | Stop at | Basis |
|-|-|-|-|-|
| Spam complaint rate (Postmaster Tools, Yahoo CFL) | Under 0.1% | 0.1% or more: lower that domain's volume and run the complaint checks | 0.3%: stop the domain | Google sender guidelines (keep under 0.10%, never reach 0.30%); Yahoo best practices (under 0.3%) |
| Hard bounce rate (per campaign or mailbox, rolling 200 sends) | Under 2% | 2% or more: pause the campaign or mailbox, re-validate the remaining list | | alexberman.com (under 2%). Instantly's default auto-pause is 5% after 200 sends; set yours to 2%. |
| Email validation status in the send file | 100% `valid` | Any `invalid` or `disposable`: remove before upload | | Berman (verify before sending); section 5 |
| Catch-all campaign | Its own campaign | | Hard bounces 2% or more over 200 sends: pause it | Berman (under 2%); Instantly (200-send window) |
| Cold sends per mailbox per day | Your cap, reached by the section 6 ramp | | 50 or more | alexberman.com (under 50). Apollo suggests 50 to 100 per mailbox with 10 to 20 an hour; Berman's line is lower |
| Mailboxes per sending domain | 2 to 3 | 4 or more: spread to a new domain | | alexberman.com |
| Warmup before first cold send | 14 days minimum | | Any cold send before day 15 | Instantly readiness rule; alexberman.com 2 to 4 weeks |
| Messages per sending domain per day to personal Gmail | Well under 5,000 | | 5,000 makes the primary domain a permanent bulk sender | Google FAQ |
| DMARC | `p=none` with `rua` from day 1 | Move to `quarantine` once at least a week of daily reports shows only your own sources passing | Missing or duplicate DMARC record: do not send | Google, Yahoo, Microsoft requirements; Google DMARC rollout guide; RFC 7489, RFC 9989 |
| Opt-out handling | Suppressed the same day, in every tool | | Any opt-out mailed again | Google 48 hours, Yahoo 2 days are the outer limits |

## 8. Monitoring tools

| Tool | What it shows | Setup | Limits |
|-|-|-|-|
| Google Postmaster Tools | Compliance status, spam rate, authentication, encryption, delivery errors, feedback loop; Google's help page also lists IP and domain reputation dashboards | Add the sending domain and verify it with a DNS TXT record | Traffic to personal Gmail only. Low-volume days may show no data. The spam rate counts DKIM-authenticated mail that reached the inbox, so Google notes it can look low when much of the mail is filtered to spam; a low rate never proves inbox placement. Google's deprecation notice says the Domain and IP Reputation dashboards are being retired (checked 2026-10-13), so a keep or retire decision rests on seed tests, bounces and spam rate, not on a reputation label. |
| Microsoft SNDS and JMRP | Per-IP data for mail to Outlook.com; JMRP sends a report when a recipient marks your mail as junk | Sign in with a Microsoft account and request access to IPs you control | IP-based. Workspace and Microsoft 365 senders do not own their sending IPs, so SNDS helps only dedicated-IP senders (for example EmailBison or ManyReach private IPs). |
| Yahoo Complaint Feedback Loop | Complaint reports for DKIM domains you enroll | Enroll each DKIM `d=` domain in Yahoo Sender Hub | Domain-based since 2024; IP-based reporting retired |
| Spamhaus IP and Domain Reputation Checker (check.spamhaus.org) | Whether a domain is on the Domain Blocklist (DBL) or an IP is listed | None | Spamhaus says unknown reputations begin as poor by default. It describes snowshoeing as a technique that uses many domains and IP addresses which change frequently, and says domains that act like they are snowshoeing get treated like snowshoers. Spamhaus also recommends checking domains in message bodies (links), so check linked and tracking domains too, along with SURBL and URIBL. Delisting is free and only through the checker. |
| Seed or placement test | Inbox vs spam vs missing per provider for one message | A seed list of mailboxes at Gmail, Workspace, Outlook.com and Microsoft 365 you own, or a GlockApps test: its Smart Test takes one proxy address and distributes the message to its seed mailboxes | A sample, not a census; repeat weekly. GlockApps weights its coverage toward US consumer providers, so keep your own Workspace and Microsoft 365 seeds for B2B |
| Multi-list blocklist checkers | Many lists at once | None | Weight Spamhaus first. SORBS closed in June 2024, so a checker still showing it is out of date |

## 9. What opens, clicks and provider limits can tell you

| Signal | What distorts it | Use it for |
|-|-|-|
| Open rate | Apple Mail Privacy Protection downloads remote content in the background when a message arrives, whether or not the recipient engages. Outlook blocks automatic picture downloads by default. Security filters open messages and click links within seconds of delivery. Mail in spam is seldom opened | Nothing that decides placement. A sudden drop says something changed; seeds, replies and bounce codes say what. Keep open tracking off for cold email |
| Click rate | The same security filters click links; gateways rewrite or strip tracked links | Not a placement signal |
| Human replies per 1,000 sends | Auto-replies, if not excluded | The main engagement signal. Compare against the 4-week average |
| Seed placement | Small sample, one moment | The direct placement reading, per provider |
| Hard bounce rate with SMTP codes | Sequencers that count `4.x.x` deferrals as bounces | List quality (`5.1.1`, `5.1.10`) vs authentication or policy (`5.7.x`) |

Provider sending limits sit far above cold email caps. Google Workspace allows 2,000 messages a day per user (500 on a trial account) and suspends sending for up to 24 hours when a user exceeds a limit (Gmail sending limits in Google Workspace, checked 2026-10-13). Berman's under-50 cap is a reputation limit, not a provider limit; a Workspace mailbox suspended well under 50 a day points at something other than volume (security alert, unusual activity, or a second campaign sending from it).

## Sources

- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Google, Postmaster Tools dashboards: https://support.google.com/mail/answer/14668346
- Google Workspace, Set up SPF: https://knowledge.workspace.google.com/admin/security/set-up-spf
- Google Workspace, Set up DKIM: https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Google Workspace, Recommended DMARC rollout (one week at `p=none`, then quarantine a small percentage; checked 2026-10-13): https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout
- Google, Email sender guidelines, Gmail help copy (keep spam rate below 0.10%, never 0.30%; doubling volume at once can cause rate limiting; checked 2026-10-13): https://support.google.com/mail/answer/81126
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
- Spamhaus, Domain Blocklist (snowshoeing, body URL checks; checked 2026-10-13): https://www.spamhaus.org/blocklists/domain-blocklist/
- Google Workspace, Gmail SMTP errors and codes (checked 2026-10-13): https://knowledge.workspace.google.com/admin/support/troubleshooting/gmail-smtp-errors-and-codes
- RFC 7489 section 7.1, Verifying External Destinations: https://www.rfc-editor.org/rfc/rfc7489#section-7.1
- SURBL: https://www.surbl.org/
- URIBL: https://uribl.com/
- Google, Learn about the deprecation of the old Postmaster Tools interface (Domain and IP Reputation dashboards being retired; checked 2026-10-13): https://support.google.com/mail/answer/16594218
- GlockApps, Email seed list testing (Manual Test sends to the seed list; Smart Test sends to one proxy address that GlockApps distributes; 40 mailbox providers; checked 2026-10-13): https://glockapps.com/blog/email-seed-list-testing-get-the-best-results-with-glockapps/
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, Warmup settings: https://help.instantly.ai/en/articles/7988514-warmup-settings
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Apollo, Configure email sending limits: https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- Alex Berman, cold email templates (start at 10 to 20 a day and ramp over 2 to 4 weeks; bounces under 2%; verify before sending; checked 2026-10-13): https://alexberman.com/cold-email-templates
- Alex Berman, TAM strategy breakdown (3 to 5 domains, 2 to 3 inboxes per domain, under 50 a day per inbox, 2 to 4 weeks of warmup; checked 2026-10-13): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- ScraperCity, Email Validator: https://scrapercity.com/email-validator
- Apple, Mail Privacy Protection & Privacy (checked 2026-10-13): https://www.apple.com/legal/privacy/data/en/mail-privacy-protection/
- Microsoft Support, Block or unblock automatic picture downloads in email messages (checked 2026-10-13): https://support.microsoft.com/en-us/office/block-or-unblock-automatic-picture-downloads-in-email-messages-15e08854-6808-49b1-9a0a-50b81f2d617a
- lemlist help, Identifying legitimate clicks and opens (checked 2026-10-13): https://help.lemlist.com/en/articles/9140285-identifying-legitimate-clicks-and-opens
- Google Workspace, Gmail sending limits in Google Workspace (checked 2026-10-13): https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace
- The Register, SORBS closed (2024-06-07): https://www.theregister.com/2024/06/07/sorbs_closed/
- Microsoft Learn, Fix NDR error 550 5.1.10 in Exchange Online: https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/non-delivery-reports-in-exchange-online/fix-error-code-550-5-1-10-in-exchange-online
