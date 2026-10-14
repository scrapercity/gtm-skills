# Monitoring and Testing

How to check that mail is authenticated, reaches the inbox and stays there: the pre-send gate, list validation handling beyond the basic buckets, seed and placement tests, the provider dashboards, blocklist checks and the weekly review. Provider rules and the standing thresholds live in `references/deliverability-primer.md`; this file is the operating procedure that sits on top of them. Checked 2026-10-13.

## 1. Pre-send gate (run before every new campaign and every re-launch)

| # | Check | How | Pass when | Fail action |
|-|-|-|-|-|
| 1 | SPF, DKIM, DMARC pass and align | Send one message from each mailbox to a personal Gmail and an Outlook.com seed; open "Show original" in Gmail, "View message source" in Outlook | `spf=pass`, `dkim=pass header.d=<sending domain>`, `dmarc=pass` on every mailbox | Hold the mailbox; fix DNS with `domain-infrastructure` |
| 2 | One SPF record, one DMARC record per domain | `dig +short TXT <domain>` and `dig +short TXT _dmarc.<domain>` | Exactly one `v=spf1` and one `v=DMARC1` | Merge duplicates (RFC 7208 `permerror`; RFC 7489 ignores DMARC when two records exist) |
| 3 | Unsubscribe header, if the sequencer supports it | Instantly: campaign Settings, Advanced settings, Sending rules, "Insert unsubscribe link header". Then check the raw headers of a test message | `List-Unsubscribe` present; `List-Unsubscribe-Post: List-Unsubscribe=One-Click` present for RFC 8058 one-click | Turn it on, or rely on the body opt-out line and same-day suppression |
| 4 | Body opt-out line | Read the rendered test email | Present and readable | Fix the signature (`inbox-setup`) |
| 5 | Every address validated inside the re-check window | `email_validated_at` column | 100% of rows | Run `validate_emails` on the stale rows |
| 6 | Send file is 100% `valid` | `email_status` column | No `invalid`, `disposable`, `unknown` or `catch_all` rows in the main file | Split files per section 2 |
| 7 | Suppression applied | Match against unsubscribes, bounces, complaints, customers, open deals | 0 matches | Remove matches; see `references/list-quality-standard.md` section 7 |
| 8 | Seed placement | Section 3 | Inbox at every seed provider | Run the spam-folder runbook in `references/incident-runbooks.md` before launch |
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
| low | Last, from the mailboxes with the longest sending history and bounces under 2% | Highest bounce risk inside the valid bucket |

### 2b. Catch-all handling

| Rule | Value | Why |
|-|-|-|
| Separate campaign | Catch-all rows never share a campaign with valid rows | The sequencer's bounce auto-pause then trips on the risky campaign only |
| Volume share | Your setting; raise or lower it from the catch-all campaign's own bounce rate | No source publishes a share |
| Sending mailboxes | Mailboxes at their full cap with bounces under 2% | New mailboxes get only `valid` rows |
| Do not re-validate | A catch-all domain accepts every address at SMTP, so a second run usually returns the same result and costs $0.0072 again | Spend on `find_emails` for a second address instead when the account is high value |
| Stop | Catch-all campaign hard bounces 2% or more across 200 sends | Berman's line; Instantly's 200-send window |
| Learn | After every 200 catch-all sends, list the company domains that bounced and suppress them at domain level | Those domains accept at SMTP then bounce |

### 2c. Security gateways

`sc_mx_security_gateway` names the filtering service in front of a recipient domain when one is detected. Mail through a gateway is filtered by that company's own rules instead of Google's or Microsoft's consumer rules.

| Use | How |
|-|-|
| Placement testing | If a large share of the list sits behind one gateway, add a seed mailbox behind it if you have access to one; otherwise watch reply rate for that segment separately |
| Reporting | Report reply rate by `sc_mx_provider` and gateway; a gateway segment with no replies while the others reply gets a placement check first |

### 2d. Re-validation calendar

| Situation | Re-validate | Cost per 1,000 |
|-|-|-|
| First send after the re-check window | Yes, the unsent rows | $7.20 |
| `unknown` result | Once | $7.20 |
| Bounce spike on a campaign | The unsent rows of that campaign, before resuming | $7.20 |
| Re-launch to non-responders past the re-check window | Yes | $7.20 |
| `catch_all` result | No (section 2b) | |

## 3. Seed and placement testing

A seed test sends a live campaign email to mailboxes you control at each major provider and records the folder it arrives in. It is a sample of one message at one moment. Repeat weekly, and before every launch.

### 3a. Seed list design

One seed or more at each provider the list uses (read the mix from `sc_mx_provider`).

| Seed | Count | Why |
|-|-|-|
| Personal Gmail (`@gmail.com`) | 1 or more | Google's consumer filtering, where Postmaster data comes from |
| Google Workspace on a domain you own (not a sending domain) | 1 or more | Many B2B recipients; filtering differs from consumer Gmail and admins can add rules |
| Outlook.com or Hotmail | 1 or more | Microsoft consumer filtering, the scope of the May 2025 rules |
| Microsoft 365 tenant you own | 1 or more | B2B recipients on Exchange Online Protection |
| Yahoo Mail | 1 or more | Yahoo consumer filtering |
| Mailbox behind a security gateway | 1 if available | Only if a meaningful share of the list sits behind one (section 2c) |

Keep seeds quiet: turn off auto-forwarding and rules, and keep them out of warmup pools. Open and move a message out of spam only after the folder is recorded, then delete it, so the seeds do not train themselves.

### 3b. Test protocol

1. Pick 1 mailbox per sending domain under review (the one with the most sends that week).
2. Send the live touch 1 copy with merge fields filled from a list row, through the sequencer, to all seeds at once.
3. Once the message has reached every seed, record the folder per seed: Inbox, Promotions or Other tab, Spam or Junk, Missing.
4. Read the headers on the Gmail seed: authentication results, and whether the message came through the sequencer's tracking domain.
5. Score: Inbox and tabs count as delivered; Spam and Missing count as failed.
6. Split test when tracking or links are suspects: send the same touch twice to the seeds, once as live and once with open tracking off and every link removed. Only the live version in spam points at the tracking host or a linked domain; both in spam points at the sending domain, the list history or the copy.

| Result | Meaning | Action |
|-|-|-|
| Inbox at all providers | Healthy | Continue |
| Spam at one provider | Placement problem at that provider | Repeat with a second mailbox on the same domain, then run the spam-folder runbook for that provider |
| Spam at several providers | Placement problem on the domain | Run the spam-folder runbook |
| Missing at a provider | Rejection or delay | Read the sequencer's bounce log for the SMTP code |

Paid placement tools run the same idea on larger seed lists. Smartlead's SmartDelivery is a separate add-on starting at $49 a month for 120 tests (Smartlead pricing page, checked 2026-10-13). GlockApps lists a free plan with 2 spam test credits and paid plans from $59 a month for 360 credits (GlockApps pricing page, checked 2026-10-13). GlockApps runs a Manual Test (you send to its seed list) or a Smart Test (you send to one proxy address and it distributes the message to its seed mailboxes), covers 40 mailbox providers and weights coverage toward US consumer providers (GlockApps seed list testing guide, checked 2026-10-13). Keep your own Workspace and Microsoft 365 seeds for B2B.

## 4. Provider dashboards

| Dashboard | Setup | What to read weekly | Limits to remember |
|-|-|-|-|
| Google Postmaster Tools | Add each sending domain, verify with a DNS TXT record | Compliance status (each requirement shows Compliant, Needs work or No data found), spam rate, authentication, delivery errors | Covers mail to personal Gmail only; Google says low-volume days might not include all data; compliance status is a rolling average that can take up to 7 days to change; data typically updates within 24 hours |
| Yahoo Complaint Feedback Loop (Sender Hub) | Enroll every DKIM domain after DKIM signing starts | Complaint reports per domain | Yahoo computes spam rate on mail delivered to the inbox |
| Microsoft SNDS and JMRP | Request access for IPs you control | Per-IP data and junk reports for Outlook.com | IP based; only useful for senders on dedicated IPs (for example EmailBison or ManyReach private IPs), not for Workspace or Microsoft 365 mailboxes |
| DMARC aggregate reports (`rua`) | Set by `domain-infrastructure` | Share of mail passing DMARC per source; unknown sources sending as your domain | Arrive daily from each receiver that sends reports |
| Sequencer analytics | Built in | Hard bounce rate per mailbox over the last 200 sends; health score; auto-paused campaigns | Bounce rates are only as good as the sequencer's bounce classification |

Postmaster reality check for cold email: a domain whose recipients sit mostly on Workspace and Microsoft 365 sends little to personal Gmail (read the share from `sc_mx_provider`). Expect "No data found" on many days. Seed tests and reply rate by recipient provider carry more signal for B2B programs.

## 5. Blocklist checks

| List | Lookup | Covers | Removal |
|-|-|-|-|
| Spamhaus Domain Blocklist (DBL) and IP lists | check.spamhaus.org | Domains (DBL) and IPs | Free, only through the checker; fix the cause first |
| Barracuda Reputation Block List | barracudacentral.org/lookups | IPs | Removal request form; Barracuda says requests with a valid explanation are typically processed within 12 hours |
| SpamCop Blocking List | spamcop.net lookup | IPs | Automatic after 24 hours with no new spam reports; mirrors can take up to 4 hours more |
| SURBL (Multi) | surbl.org/surbl-analysis | Domains of abused or malicious sites, used to filter mail by the links in the body | Lookup page does not describe removal; fix the cause and contact SURBL from its site |
| URIBL | admin.uribl.com (up to 15 URIs per lookup) | Domains found in message content; enabled by default in SpamAssassin | Lookup page does not describe removal; fix the cause, then follow the site's own instructions |
| Microsoft 365 banned sending IP | Shows in the NDR as `5.7.606-649` | IPs sending to Microsoft 365 tenants | sender.office.com delist portal; Microsoft says it might take up to 24 hours or longer |

Workspace and Microsoft 365 mailboxes send from the provider's shared IPs. An IP listing on those is the provider's problem, and your action is to check your own domain on the Spamhaus DBL. IP lists apply directly when you send through dedicated or private IPs.

Domains to check, every week:

| Domain | Why | Lists |
|-|-|-|
| Every sending domain | Its reputation decides placement for its mailboxes | Spamhaus DBL; SURBL and URIBL because the custom tracking host (`inst.<domain>` on Instantly) puts it in every tracked link |
| The sequencer's shared tracking domain, if custom tracking is off | Every tracked link points there, shared with other senders | Spamhaus DBL, SURBL, URIBL |
| The main site linked in the signature | It appears in every message body | Spamhaus DBL, SURBL, URIBL |
| Booking or calendar link domains and any other linked domain | Filters look up every domain in the body (Spamhaus recommends checking URLs in headers and body) | Spamhaus DBL, SURBL, URIBL |

When a linked shared host is listed, every message carrying the link is affected. Remove the link until it clears.

SORBS closed in June 2024 (The Register, 2024-06-07); ignore multi-list checkers that still report it.

Weekly: every domain above and every dedicated IP. Daily during an incident, with a seed test before each ramp step. Report what was not checked in one line, not as table rows.

## 6. Weekly review

| Step | Source | Record |
|-|-|-|
| 1 | Sequencer account table, sorted by bounce rate over the last 200 sends | Mailboxes at 2% or more |
| 2 | Sequencer campaign table | Auto-paused campaigns and why |
| 3 | Postmaster compliance status and spam rate per domain | Any "Needs work"; any spam rate at 0.1% or more |
| 4 | Yahoo CFL reports | Complaint count per domain |
| 5 | DMARC aggregate reports | Pass share per domain; unknown senders |
| 6 | Blocklist checks (section 5): sending and linked domains on DBL, SURBL, URIBL | Listings |
| 7 | Seed test (section 3) | Folder per provider per domain |
| 8 | Reply rate by `sc_mx_provider` | Segments with no replies while the others reply |
| 9 | Opt-out log | Opt-outs suppressed the same day in every tool, count |
| 10 | Domain status | Green, yellow or red per the rules in the SKILL.md stop rules table |

## 7. Six-month audit

The weekly review catches incidents. The six-month audit catches slow changes: an unlogged DNS edit, a DKIM key past its rotation date, an unapproved tool sending as your domain, caps that crept up while volume moved. Run it every six months, the DKIM rotation interval M3AAWG sets, and in the first month after any sequencer migration. Every row goes into the report's Six-Month Audit table with the date run and the next due date.

| # | Check | How | Pass when | Fail action |
|-|-|-|-|-|
| 1 | DNS records vs plan | Compare live records to the `domain-infrastructure` plan for every sending domain: `dig +short TXT <domain>`, `dig +short TXT _dmarc.<domain>`, `dig +short MX <domain>`, the DKIM selector, the tracking CNAME, `dig +short NS <domain>` | Every record matches the plan; one SPF and one DMARC per domain; nameservers unchanged | Restore the planned value, log who changed it; check renewal dates while in the registrar |
| 2 | DKIM key rotation | Key age per domain from the plan's launch date or the last rotation log; selector in a live message's `DKIM-Signature` `s=` tag | Key younger than 6 months (M3AAWG: rotate at least every six months); 2048-bit where the provider allows it | Rotate: Microsoft 365 "Rotate DKIM keys" in the Defender portal or `Rotate-DkimSigningConfig -KeySize 2048` (the new key signs after 96 hours); Google Workspace: generate a new 2048-bit key in the Admin console with a different selector prefix (the setup page allows one), publish it, then start authentication. Header test after |
| 3 | DMARC `rua` review for unknown senders | Read the aggregate reports since the last audit in the report service (section 8); list every sending source per domain | Every source is a known one: the mailbox provider, the sequencer's warmup, nothing else | Unknown source passing DMARC: find the tool and remove it or document it. Unknown source failing: spoofing or a forgotten tool. A source failing SPF while passing DKIM is usually forwarding by the recipient, not spoofing. Once at least a week of daily reports shows only known sources, move toward `p=quarantine` (Google's DMARC rollout guide) |
| 4 | Placement across Google, Microsoft and Yahoo | Seed test (section 3) from one mailbox per domain, live copy, seeds at personal Gmail, Google Workspace, Outlook.com, Microsoft 365 and Yahoo | Inbox at every seed provider on every domain | Spam-folder runbook R2 in `references/incident-runbooks.md` |
| 5 | Caps against volume | Sequencer account table: per-mailbox daily limit, campaign daily limits, actual sends per mailbox since the last audit; `inbox-setup` roster | Every mailbox at or under its roster cap (under 50, Berman); campaign limits at or under mailboxes x cap; no mailbox sending above cap through a second campaign | Lower the limits; any raise goes through the escalation rule in `inbox-setup` (`warmup-and-ramp.md` section 8) |
| 6 | Suppression sync (optional) | Pick a sample of recent opt-outs and confirm each is blocked in every tool and the CRM | Every one blocked everywhere | Fix the sync before the next launch |
| 7 | Renewal dates (optional) | Registrar inventory | Every sending domain has auto-renew on and its renewal date logged | Turn on auto-renew |

## 8. DMARC report services

Raw `rua` reports are XML files from every receiver, every day. A report service parses them into a list of sending sources per domain, which is what check 3 needs. Prices read from each vendor's page on 2026-10-13.

| Service | What it offers (per its page) | Price (2026-10-13) | Fit for a cold sending set |
|-|-|-|-|
| Postmark DMARC | Free tier: weekly email digest, top 10 mail sources with 5 IPs each, 7 days of history, no dashboard. Paid "DMARC Digests": all sources and IPs, 60 days of history, web dashboard, 14-day free trial | Free; paid $14 a month per domain | Free tier covers a small set when the sources are few; 9 domains on paid is $126 a month |
| dmarcian | Personal plan free for non-business use only (2 domains, 1,250 messages a month). Paid plans include a 30-day trial | Basic $19.99 a month billed yearly ($24 monthly), up to 2 domains, 100,000 DMARC-capable messages a month; Plus $199 a month yearly ($240 monthly), up to 8 domains; Enterprise $499 a month yearly, up to 15 domains | Plus covers 8 domains; the free plan is off-limits for a business |
| Valimail Monitor | Free DMARC monitoring: identifies sending services, shows DMARC pass or fail with aligned SPF and DKIM, flags suspicious IPs sending as your domain, checks Google, Microsoft and Yahoo requirements; "No trial offers, credit cards, or obligations" | Free (usage caps and retention not stated) | Good default for the unknown-sender check across many domains |
| EasyDMARC | DMARC Plus: 2 domains, from 100,000 emails a month, 3 months of history. DMARC Premium: 4 domains, 1 year of history. Free trial, no credit card; no free plan listed | Plus $35.99 a month billed yearly ($44.99 monthly); Premium $71.99 a month yearly ($89.99 monthly) | Priced per small domain block; check the domain count before choosing |

Point every sending domain's `rua` at the service's address, or keep `rua` at your own mailbox and forward. Reports sent to an address on another domain need the authorization record from `domain-infrastructure` (`<sendingdomain>._report._dmarc.<reportdomain>`) unless the service publishes it for you.

## 9. Opt-out rate

```text
opt_out_rate = (unsubscribe clicks + "remove me" or "stop" replies) / delivered sends, per campaign
```

No mailbox provider publishes an opt-out rate limit, so this skill sets no threshold. Report the rate per campaign against the program's own baseline, and read the replies behind any campaign running above it: they name the segment or touch to fix. Opt-outs are suppressed the same day in every tool whatever the rate.

## Sources

- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Google, Postmaster Tools dashboards: https://support.google.com/mail/answer/14668346
- Google Workspace, Recommended DMARC rollout (one week at `p=none` before quarantine; checked 2026-10-13): https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout
- Alex Berman, cold email templates (bounces under 2%): https://alexberman.com/cold-email-templates
- Alex Berman, TAM strategy breakdown (under 50 a day per inbox): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Instantly, High bounce auto-pause (200-send window): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders (Apr 2025): https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Microsoft, Use the delist portal to unblock yourself: https://learn.microsoft.com/en-us/defender-office-365/external-senders-use-the-delist-portal-to-unblock-yourself
- Microsoft, SNDS: https://sendersupport.olc.protection.outlook.com/snds/
- RFC 8058, One-click unsubscribe: https://www.rfc-editor.org/rfc/rfc8058
- RFC 7208, SPF: https://www.rfc-editor.org/rfc/rfc7208
- RFC 7489, DMARC: https://www.rfc-editor.org/rfc/rfc7489
- Spamhaus, IP and Domain Reputation Checker: https://check.spamhaus.org/
- Spamhaus, Domain Blocklist (check domains in headers and body, e.g. URLs; checked 2026-10-13): https://www.spamhaus.org/blocklists/domain-blocklist/
- SURBL, home and lookup (checked 2026-10-13): https://www.surbl.org/ and https://www.surbl.org/surbl-analysis
- URIBL, home and lookup (checked 2026-10-13): https://uribl.com/ and https://admin.uribl.com/
- Instantly, Custom tracking domain (host `inst`, checked 2026-10-13): https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- Barracuda Central, Removal request: https://www.barracudacentral.org/rbl/removal-request
- SpamCop, How long do listings last: https://www.spamcop.net/fom-serve/cache/298.html
- Instantly, List unsubscribe: https://help.instantly.ai/en/articles/9215368-list-unsubscribe
- Smartlead, Pricing: https://smartlead.ai/pricing
- GlockApps, Pricing: https://glockapps.com/pricing/
- GlockApps, Email seed list testing (Manual and Smart Test, 40 providers, consumer weighting; checked 2026-10-13): https://glockapps.com/blog/email-seed-list-testing-get-the-best-results-with-glockapps/
- ScraperCity, Email Validator: https://scrapercity.com/email-validator
- M3AAWG, DKIM Key Rotation Best Common Practices (rev. March 2019): https://www.m3aawg.org/DKIMKeyRotation
- Microsoft, Configure DKIM, Rotate DKIM keys (checked 2026-10-13): https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
- Postmark, DMARC monitoring (checked 2026-10-13): https://dmarc.postmarkapp.com/
- dmarcian, Pricing (checked 2026-10-13): https://dmarcian.com/pricing/
- Valimail, Monitor (checked 2026-10-13): https://www.valimail.com/products/monitor/
- EasyDMARC, Pricing (checked 2026-10-13): https://easydmarc.com/pricing
- Google Workspace, Set up DKIM (selector prefix, 2048-bit keys; checked 2026-10-13): https://knowledge.workspace.google.com/admin/security/set-up-dkim
- The Register, SORBS closed (2024-06-07): https://www.theregister.com/2024/06/07/sorbs_closed/
