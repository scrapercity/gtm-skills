# Monitoring and Testing

How to check that mail is authenticated, lands in the inbox and stays there: the pre-send gate, list validation handling beyond the basic buckets, seed and placement tests, the provider dashboards, blocklist checks and the weekly review. Provider rules and the standing thresholds live in `references/deliverability-primer.md`; this file is the operating procedure that sits on top of them. Checked 2026-10-13.

## 1. Pre-send gate (run before every new campaign and every re-launch)

| # | Check | How | Pass when | Fail action |
|-|-|-|-|-|
| 1 | SPF, DKIM, DMARC pass and align | Send one message from each mailbox to a personal Gmail and an Outlook.com seed; open "Show original" in Gmail, "View message source" in Outlook | `spf=pass`, `dkim=pass header.d=<sending domain>`, `dmarc=pass` on every mailbox | Hold the mailbox; fix DNS with `domain-infrastructure` |
| 2 | One SPF record, one DMARC record per domain | `dig +short TXT <domain>` and `dig +short TXT _dmarc.<domain>` | Exactly one `v=spf1` and one `v=DMARC1` | Merge duplicates (RFC 7208 `permerror`; RFC 7489 ignores DMARC when two records exist) |
| 3 | Unsubscribe header, if the sequencer supports it | Instantly: campaign Settings, Advanced settings, Sending rules, "Insert unsubscribe link header". Then check the raw headers of a test message | `List-Unsubscribe` present; `List-Unsubscribe-Post: List-Unsubscribe=One-Click` present for RFC 8058 one-click | Turn it on, or rely on the body opt-out line and same-day suppression (house standard) |
| 4 | Body opt-out line and postal address | Read the rendered test email | Both present (CAN-SPAM) | Fix the signature (`inbox-setup`) |
| 5 | Every address validated within 30 days | `email_validated_at` column | 100% of rows | Run `validate_emails` on the stale rows |
| 6 | Send file is 100% `valid` | `email_status` column | No `invalid`, `disposable`, `unknown` or `catch_all` rows in the main file | Split files per section 2 |
| 7 | Suppression applied | Match against unsubscribes, bounces, complaints, customers, open deals | 0 matches | Remove matches; see `references/list-quality-standard.md` section 7 |
| 8 | Seed placement | Section 3 | Inbox at 4 of 5 seed providers or better | Run the spam-folder runbook in `references/incident-runbooks.md` before launch |
| 9 | Mailbox ramp row | `inbox-setup` roster | Campaign daily limit is at or under mailboxes x current cap | Lower the campaign limit |
| 10 | Tracking | Campaign settings | Open tracking off; link tracking off unless a custom tracking domain is set and verified | Turn off |

A campaign launches only when all 10 pass. Record the date and result of each check in the health report.

## 2. Validation results beyond the buckets

`validate_emails` ($0.0072 per email) returns `email_result`, `email_quality` and enrichment columns including `sc_is_catch_all`, `sc_mx_provider` and `sc_mx_security_gateway` (per scrapercity.com/email-validator, checked 2026-10-12). The bucket actions are in `references/deliverability-primer.md` section 5. These are the extra rules this skill runs on top.

### 2a. Send order inside the valid file

| `email_quality` | Send order | Reason |
|-|-|-|
| high | First days of the campaign, newest mailboxes get these rows | Lowest bounce risk while a mailbox builds history |
| medium | After high | |
| low | Last, from mailboxes with 30+ days of history and bounces under 1% | Highest bounce risk inside the valid bucket |

### 2b. Catch-all handling

| Rule | Value | Why |
|-|-|-|
| Separate campaign | Catch-all rows never share a campaign with valid rows | The sequencer's bounce auto-pause then trips on the risky campaign only |
| Volume share | 10% or less of a day's sends (house standard, primer section 7) | Caps the damage of a bad catch-all domain |
| Sending mailboxes | Mailboxes past ramp row 3 with bounces under 1% | New mailboxes get only `valid` rows |
| Contacts per catch-all domain | 1 per company per day, 3 per campaign | A catch-all company that rejects later bounces every contact you sent |
| Do not re-validate | A catch-all domain accepts every address at SMTP, so a second run usually returns the same result and costs $0.0072 again | Spend on `find_emails` for a second address instead when the account is worth it |
| Stop | Catch-all campaign hard bounces over 3% across 200 sends | Primer section 5 |
| Learn | After 200 catch-all sends, list the company domains that bounced and suppress them at domain level | Those domains accept at SMTP then bounce |

### 2c. Security gateways

`sc_mx_security_gateway` names the filtering service in front of a recipient domain when one is detected. Mail through a gateway is filtered by that company's rules, not by Google's or Microsoft's consumer rules.

| Use | How |
|-|-|
| Placement testing | If more than 15% of a list sits behind gateways, add a seed mailbox behind the most common gateway if you have access to one; otherwise watch reply rate for that segment separately |
| Copy | Plain text, no attachments, no link in touch 1; gateways weigh links and attachments heavily |
| Reporting | Report reply rate by `sc_mx_provider` and gateway; a segment with zero replies after 300 sends behind one gateway is a placement problem until shown otherwise |

### 2d. Re-validation calendar

| Situation | Re-validate | Cost per 1,000 |
|-|-|-|
| First send more than 30 days after validation | Yes, the unsent rows | $7.20 |
| `unknown` result | Once, after 72 hours | $7.20 |
| Bounce spike on a campaign | The unsent rows of that campaign, before resuming | $7.20 |
| Re-launch to non-responders after 60 days | Yes | $7.20 |
| `catch_all` result | No (section 2b) | |

## 3. Seed and placement testing

A seed test sends a real campaign email to mailboxes you control at each major provider and records the folder it lands in. It is a sample of one message at one moment. Repeat weekly, and before every launch.

### 3a. Seed list design (house standard)

| Seed | Count | Why |
|-|-|-|
| Personal Gmail (`@gmail.com`) | 2 | Google's consumer filtering, where Postmaster data comes from |
| Google Workspace on a domain you own (not a sending domain) | 2 | Most B2B recipients; filtering differs from consumer Gmail and admins can add rules |
| Outlook.com or Hotmail | 1 | Microsoft consumer filtering, the scope of the May 2025 rules |
| Microsoft 365 tenant you own | 2 | B2B recipients on Exchange Online Protection |
| Yahoo Mail | 1 | Yahoo consumer filtering |
| Mailbox behind a security gateway | 1 if available | Only if a meaningful share of the list sits behind one (section 2c) |

Keep seeds quiet: no auto-forwarding, no rules, no warmup pool participation. Open and move a message out of spam only after the folder is recorded, then delete it, so the seeds do not train themselves.

### 3b. Test protocol

1. Pick 1 mailbox per sending domain under review (the one with the most sends that week).
2. Send the live touch 1 copy with merge fields filled from a real row, through the sequencer, to all seeds at once.
3. After 15 minutes, record the folder per seed: Inbox, Promotions or Other tab, Spam or Junk, Missing.
4. Read the headers on the Gmail seed: authentication results, and whether the message came through the sequencer's tracking domain.
5. Score: Inbox and tabs count as delivered; Spam and Missing count as failed.

| Result | Meaning | Action |
|-|-|-|
| Inbox at all providers | Healthy | Continue |
| Spam at 1 provider | Watch | Repeat in 48 hours with a second mailbox on the same domain |
| Spam at 2 or more providers, or every Microsoft seed | Placement problem | Run the spam-folder runbook |
| Missing at a provider | Rejection or delay | Read the sequencer's bounce log for the SMTP code |

Paid placement tools run the same idea on larger seed lists. Smartlead's SmartDelivery is a separate add-on starting at $49 a month for 120 tests (Smartlead pricing page, checked 2026-10-13). GlockApps lists a free plan with 2 spam test credits and paid plans from $59 a month for 360 credits (GlockApps pricing page, checked 2026-10-13). Their seed lists lean toward consumer mailboxes; keep your own Workspace and Microsoft 365 seeds for B2B.

## 4. Provider dashboards

| Dashboard | Setup | What to read weekly | Limits to remember |
|-|-|-|-|
| Google Postmaster Tools | Add each sending domain, verify with a DNS TXT record | Compliance status (each requirement shows Compliant, Needs work or No data found), spam rate, authentication, delivery errors | Covers mail to personal Gmail only; Google says low-volume days might not include all data; compliance status is a rolling average that can take up to 7 days to change; data typically updates within 24 hours |
| Yahoo Complaint Feedback Loop (Sender Hub) | Enroll every DKIM domain after DKIM signing starts | Complaint reports per domain | Yahoo computes spam rate on mail delivered to the inbox |
| Microsoft SNDS and JMRP | Request access for IPs you control | Per-IP data and junk reports for Outlook.com | IP based; only useful for senders on dedicated IPs (for example EmailBison or ManyReach private IPs), not for Workspace or Microsoft 365 mailboxes |
| DMARC aggregate reports (`rua`) | Set by `domain-infrastructure` | Share of mail passing DMARC per source; unknown sources sending as your domain | Arrive daily from each receiver that sends reports |
| Sequencer analytics | Built in | Hard bounce rate per mailbox over the last 200 sends; health score; auto-paused campaigns | Bounce rates are only as good as the sequencer's bounce classification |

Postmaster reality check for cold email: a domain sending 90 messages a day, mostly to Workspace and Microsoft 365, may send only 10 to 20 a day to personal Gmail. Expect "No data found" on many days. Seed tests and reply rate by recipient provider carry more signal for B2B programs.

## 5. Blocklist checks

| List | Lookup | Covers | Removal |
|-|-|-|-|
| Spamhaus Domain Blocklist (DBL) and IP lists | check.spamhaus.org | Domains (DBL) and IPs | Free, only through the checker; fix the cause first |
| Barracuda Reputation Block List | barracudacentral.org/lookups | IPs | Removal request form; Barracuda says requests with a valid explanation are typically processed within 12 hours |
| SpamCop Blocking List | spamcop.net lookup | IPs | Automatic after 24 hours with no new spam reports; mirrors can take up to 4 hours more |
| Microsoft 365 banned sending IP | Shows in the NDR as `5.7.606-649` | IPs sending to Microsoft 365 tenants | sender.office.com delist portal; Microsoft says it might take up to 24 hours or longer |

Workspace and Microsoft 365 mailboxes send from the provider's shared IPs. An IP listing on those is the provider's problem, and your action is to check your own domain on the Spamhaus DBL. IP lists apply directly when you send through dedicated or private IPs.

Weekly: check every sending domain and every dedicated IP. Daily during an incident.

## 6. Weekly review (30 minutes)

| Step | Source | Record |
|-|-|-|
| 1 | Sequencer account table, sorted by bounce rate over the last 200 sends | Mailboxes at 1% or more |
| 2 | Sequencer campaign table | Auto-paused campaigns and why |
| 3 | Postmaster compliance status and spam rate per domain | Any "Needs work"; any spam rate at 0.1% or more |
| 4 | Yahoo CFL reports | Complaint count per domain |
| 5 | DMARC aggregate reports | Pass share per domain; unknown senders |
| 6 | Blocklist checks (section 5) | Listings |
| 7 | Seed test (section 3) | Folder per provider per domain |
| 8 | Reply rate by `sc_mx_provider` | Segments with zero replies after 300 sends |
| 9 | Opt-out log | Opt-outs suppressed within 24 hours, count |
| 10 | Domain status | Green, yellow or red per the rules in the SKILL.md stop rules table |

## Sources

- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Google, Postmaster Tools dashboards: https://support.google.com/mail/answer/14668346
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders (Apr 2025): https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Microsoft, Use the delist portal to unblock yourself: https://learn.microsoft.com/en-us/defender-office-365/external-senders-use-the-delist-portal-to-unblock-yourself
- Microsoft, SNDS: https://sendersupport.olc.protection.outlook.com/snds/
- RFC 8058, One-click unsubscribe: https://www.rfc-editor.org/rfc/rfc8058
- RFC 7208, SPF: https://www.rfc-editor.org/rfc/rfc7208
- RFC 7489, DMARC: https://www.rfc-editor.org/rfc/rfc7489
- Spamhaus, IP and Domain Reputation Checker: https://check.spamhaus.org/
- Barracuda Central, Removal request: https://www.barracudacentral.org/rbl/removal-request
- SpamCop, How long do listings last: https://www.spamcop.net/fom-serve/cache/298.html
- Instantly, List unsubscribe: https://help.instantly.ai/en/articles/9215368-list-unsubscribe
- Smartlead, Pricing: https://smartlead.ai/pricing
- GlockApps, Pricing: https://glockapps.com/pricing/
- ScraperCity, Email Validator: https://scrapercity.com/email-validator
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
