# Sending Infrastructure Plan: Ledgerline

Prepared 2026-10-12 for the Ledgerline sales team (fictional company used as an example; ledgerline.com is their main domain). Prices checked 2026-10-12.

## Summary

Ledgerline sells revenue-forecasting software and wants to email 200 new VP Sales and Head of Sales prospects at US SaaS companies with 50 to 200 employees each sending day, on a 3-step sequence in Instantly. At steady state that is 600 cold sends a day. The plan builds 9 secondary `.com` domains on Porkbun (7 active, 2 reserve) with 27 Google Workspace Business Starter mailboxes on the Flexible plan, 3 per domain, capped at 30 cold sends each. Every domain redirects to ledgerline.com and publishes MX, SPF, DKIM (2048-bit), DMARC `p=none` with `rua`, and an Instantly tracking CNAME. Domains are bought 2026-10-13, warmup runs 14 days, the first cold send is Thursday 2026-10-29 at 10 a mailbox, and full volume arrives the week of 2026-11-12. Monthly cost for mailboxes, domains, sequencer, data and validation is $511.35.

## Inputs

| Input | Value | Source |
|-|-|-|
| Main domain | ledgerline.com, never sends cold email | Ledgerline |
| New prospects per sending day | 200 | Ledgerline sales plan |
| Steps per sequence | 3 | `cold-email-strategy` plan |
| Sending days per month | 21 | Weekdays |
| Sequencer | Instantly Hypergrowth | Already licensed |
| Reachable market (pagination.total x valid share) | 11,400 x 86.2% = 9,827 | `query_lead_database` total, 500-address validation sample |
| Recipient provider mix | Google 62.4%, Microsoft 31.6%, other 6.0% | `sc_mx_provider` counts from the sample (312 / 158 / 30 of 500) |

Validation sample results (500 addresses, $3.60): `valid` 431, `valid_catch_all` 41, `unknown` 9, `invalid` 17, `disposable` 2. Total 500.

## Capacity Plan

| Line | Formula | Result |
|-|-|-|
| Daily sends at steady state | 200 prospects x 3 steps | 600 |
| Cap per mailbox | House standard | 30 |
| Active mailboxes | ceil(600 / 30) | 20 |
| Mailboxes per domain | Alex Berman 2 to 3 | 3 |
| Active domains | ceil(20 / 3) | 7 |
| Reserve domains | max(1, ceil(7 x 0.2)) | 2 |
| Total domains | 7 + 2 | 9 |
| Total mailboxes | 9 x 3 | 27 |
| Per-domain sends a day | 3 x 30 | 90 (1.8% of Google's 5,000 bulk line) |
| Days of list at this pace | 9,827 / 200 | 49 sending days |

Active capacity is 7 domains x 3 mailboxes = 21 mailboxes x 30 = 630 sends a day, 30 above the 600 needed. The extra mailbox absorbs a paused mailbox without touching reserves.

## Mailbox Provider Decision

| Option | Fit | Reason |
|-|-|-|
| Google Workspace | Chosen | 62.4% of sampled recipients are on Google; Flexible plan lets seats drop any month; Instantly connects by OAuth |
| Microsoft 365 | Test later | 31.6% Microsoft recipients justify a split test after week 4: move 1 reserve domain to Exchange Online Plan 1 ($4.00 a seat, annual) and compare reply rate per recipient provider |
| Other | Rejected | 6% other recipients; no reason to add a third admin console |

Decision: Google Workspace Business Starter, Flexible, one Workspace account with 9 secondary domains.

## Sending Domains

| Domain | Role | Registrar | Redirect target | Provider | Mailboxes |
|-|-|-|-|-|-|
| getledgerline.com | Active | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| tryledgerline.com | Active | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| ledgerlinehq.com | Active | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| meetledgerline.com | Active | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| withledgerline.com | Active | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| useledgerline.com | Active | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| ledgerline-team.com | Active | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| goledgerline.com | Reserve | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |
| ledgerlineapp.com | Reserve | Porkbun | https://ledgerline.com (301) | Google Workspace Starter, Flexible | 3 |

## DNS Records

Main domain addition (once): `_dmarc.ledgerline.com` already had `v=DMARC1; p=quarantine; rua=mailto:dmarc@ledgerline.com`, kept as is.

| Domain | Record | Type | Host | Value |
|-|-|-|-|-|
| getledgerline.com | MX | MX | @ | smtp.google.com, priority 1 |
| getledgerline.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| getledgerline.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| getledgerline.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| getledgerline.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| getledgerline.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| tryledgerline.com | MX | MX | @ | smtp.google.com, priority 1 |
| tryledgerline.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| tryledgerline.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| tryledgerline.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| tryledgerline.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| tryledgerline.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| ledgerlinehq.com | MX | MX | @ | smtp.google.com, priority 1 |
| ledgerlinehq.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| ledgerlinehq.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| ledgerlinehq.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| ledgerlinehq.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| ledgerlinehq.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| meetledgerline.com | MX | MX | @ | smtp.google.com, priority 1 |
| meetledgerline.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| meetledgerline.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| meetledgerline.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| meetledgerline.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| meetledgerline.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| withledgerline.com | MX | MX | @ | smtp.google.com, priority 1 |
| withledgerline.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| withledgerline.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| withledgerline.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| withledgerline.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| withledgerline.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| useledgerline.com | MX | MX | @ | smtp.google.com, priority 1 |
| useledgerline.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| useledgerline.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| useledgerline.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| useledgerline.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| useledgerline.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| ledgerline-team.com | MX | MX | @ | smtp.google.com, priority 1 |
| ledgerline-team.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| ledgerline-team.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| ledgerline-team.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| ledgerline-team.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| ledgerline-team.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| goledgerline.com | MX | MX | @ | smtp.google.com, priority 1 |
| goledgerline.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| goledgerline.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| goledgerline.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| goledgerline.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| goledgerline.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| ledgerlineapp.com | MX | MX | @ | smtp.google.com, priority 1 |
| ledgerlineapp.com | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all |
| ledgerlineapp.com | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console for this domain) |
| ledgerlineapp.com | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.com |
| ledgerlineapp.com | Tracking | CNAME | inst | prox.itrackly.com, DNS-only |
| ledgerlineapp.com | Redirect | URL forward | @ and www | 301 to https://ledgerline.com |
| ledgerline.com | DMARC report authorization | TXT | getledgerline.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | tryledgerline.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | ledgerlinehq.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | meetledgerline.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | withledgerline.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | useledgerline.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | ledgerline-team.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | goledgerline.com._report._dmarc | v=DMARC1 |
| ledgerline.com | DMARC report authorization | TXT | ledgerlineapp.com._report._dmarc | v=DMARC1 |

## Cost Estimate

| Item | Numbers | Monthly |
|-|-|-|
| Google Workspace Business Starter, Flexible | 27 seats x $8.40 | $226.80 |
| Domains, Porkbun `.com` | 9 x $11.08 a year = $99.72, / 12 | $8.31 |
| Instantly Hypergrowth, monthly billing | 125,000 emails and 25,000 contacts a month; need 12,600 sends and 4,200 contacts | $97.00 |
| ScraperCity Growth plan | Lead Database, 100,000 new leads a day allowance | $149.00 |
| List validation, `validate_emails` | 200 x 21 = 4,200 new prospects x $0.0072 | $30.24 |
| Total | $226.80 + $8.31 + $97.00 + $149.00 + $30.24 | $511.35 |

One-time: provider-mix sample 500 x $0.0072 = $3.60. Infrastructure share (seats plus domains) is $235.11 a month, $18.66 per 1,000 cold sends at 12,600 sends a month.

## Launch Checklist

| Step | Owner | Date | Done when |
|-|-|-|-|
| Register 9 domains, privacy and auto-renew on | Ops lead | 2026-10-13 | Porkbun shows 9 active domains |
| URL forwarding 301 to ledgerline.com on `@` and `www` | Ops lead | 2026-10-13 | `curl -sI` returns `location: https://ledgerline.com/` for all 9 |
| Add 9 secondary domains to Workspace, verify TXT, MX | Workspace admin | 2026-10-13 | Admin console shows each domain verified, test inbound mail received |
| Create 27 users, 2-Step Verification on | Workspace admin | 2026-10-14 | 27 users active |
| SPF and DMARC records, report authorization on ledgerline.com | Ops lead | 2026-10-14 | `dig` returns one SPF and one DMARC per domain |
| DKIM 2048-bit per domain, Start authentication | Workspace admin | 2026-10-15 | Console shows "Authenticating email" for all 9 |
| Header test from all 27 mailboxes to Gmail and Outlook.com | SDR manager | 2026-10-15 | 27 of 27 show spf=pass, dkim=pass, dmarc=pass |
| Spamhaus check for all 9 domains | Ops lead | 2026-10-15 | No listings |
| Instantly tracking CNAME `inst` and warmup on | SDR manager | 2026-10-15 | 27 accounts show CNAME Verified and warmup running |
| First cold sends, 10 per mailbox on 20 active mailboxes | SDR manager | 2026-10-29 | Instantly health score above 90% on each account |
| Raise to 20 per mailbox | SDR manager | 2026-11-05 | Bounces under 2%, no complaints |
| Raise to 30 per mailbox, full 600 a day | SDR manager | 2026-11-12 | Same, plus 14 days of DMARC reports with 100% aligned |
| Move DMARC to `p=quarantine` on all 9 | Ops lead | 2026-11-16 | 30 days of aligned reports |
