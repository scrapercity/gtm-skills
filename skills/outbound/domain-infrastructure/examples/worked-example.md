# Sending Infrastructure Plan: Ledgerline

Illustrative example. Ledgerline is a fictional company; every domain uses the reserved `.example` suffix where a live build would use `.com`. Prepared 2026-10-13 (Day 0) for the Ledgerline sales team. Prices checked 2026-10-13.

## Summary

Only the wide build reaches 1,500 sends a day by the requested date. Read as 1,500 sends including follow-ups (500 new prospects on a 3-step sequence), the standard build is 30 secondary domains with 2 mailboxes each: 19 domains on Google Workspace and 11 on Microsoft 365, matching the 38.6% of sampled prospects on Microsoft, all in Ledgerline's own tenants, for $531.90 a month with Instantly. It sends its first cold emails 2 days after the requested date and reaches 1,500 a day 16 days after it (9 days on the 14-day soft start). The wide build, 100 mailboxes at 15 a day on 50 domains, costs $284.07 a month more and sends 1,500 a day from its first cold day: 2 days late, or 5 days early on the soft start. Read as 1,500 first touches, the target is 4,500 sends and 150 mailboxes.

## Inputs

| Input | Value | Source |
|-|-|-|
| Main domain | ledgerline.example, never sends cold email; Spamhaus check clean, DMARC `p=quarantine` with rua | Ledgerline, checked on the plan date |
| Volume as requested, and the reading used | "1,500 new cold emails a day": 1,500 sends a day at steady state = 500 new prospects x 3 steps | Head of Sales |
| Steps per sequence | 3 | Campaign plan |
| Sending days per month | 21, Monday to Friday | Weekday schedule |
| Mailboxes per domain | 2 | Ledgerline's choice after the side-by-side below |
| Reserve share of domains | 20%, at least 1 domain | Ledgerline's choice |
| Tenant size | About 10 users per tenant | Ledgerline's choice |
| Senders | Priya Natarajan, Marcus Bell, Elena Ruiz, Tom Okafor, Sara Lindqvist, Dev Mehta, Hannah Cole | Sales team |
| Wide-build cap | 15 a mailbox, inside Alex Berman's 10 to 20 a day for new domains | Head of Sales |
| Sequencer | Instantly Hypergrowth | Already licensed |
| Existing sending domains | None | Ledgerline |

## Capacity Plan

| Line | Formula | Result |
|-|-|-|
| Daily sends at steady state | 500 new prospects x 3 steps | 1,500 |
| Cap per mailbox | Instantly's recommended campaign emails per account a day | 30 |
| Active mailboxes | ceil(1,500 / 30) | 50 |
| Mailboxes per domain (2 versus 3) | 2 per domain: 30 domains, 60 mailboxes, $531.70 a month at Google prices, one domain incident pauses 4% of volume. 3 per domain: 21 domains, 63 mailboxes, $548.59 a month, 6% per incident, 9 fewer domains to set up and renew | 2 per domain (Ledgerline's choice) |
| Active domains | 50 / 2 | 25 (16 Google, 9 Microsoft) |
| Reserve domains | max(1, ceil(25 x 0.2)) | 5 (3 Google, 2 Microsoft) |
| Total domains | 25 + 5 | 30 |
| Total mailboxes | 30 x 2 | 60 |
| Wide build | ceil(1,500 / 15) mailboxes, 2 per domain, no reserve because each mailbox can rise to 30 to cover a paused domain; Microsoft floor(50 x 0.386) = 19 domains | 100 mailboxes on 50 domains (31 Google, 19 Microsoft) in 7 Workspace accounts and 5 Microsoft tenants |

Active capacity equals the 1,500 target with no slack; a paused mailbox is covered by promoting a reserve the same day.

## Mailbox Provider Decision

Recipient mix: Google 54.2%, Microsoft 38.6%, other 7.2% (source: 500-address validation sample of the target list, 271 / 193 / 36, taken on the plan date). Proofpoint fronts 9.4% of the sample, so a Proofpoint-protected seed joins every placement test.

| Option | Monthly cost | Fit | Reason |
|-|-|-|-|
| Google Workspace only | 60 x $8.40 = $504.00 | Rejected | 38.6% Microsoft recipients would get no Microsoft-sent comparison, and one provider problem would stop all 60 mailboxes |
| Microsoft 365 only | 60 x $4.00 = $240.00, annual commitment $2,880 | Rejected | Cheapest seats, but every tenant starts at 10% of its quota and the Google majority gets no Google-sent comparison |
| Google and Microsoft from day one | 38 x $8.40 + 22 x $4.00 = $407.20 | Chosen | Microsoft domains = floor(25 x 0.386) = 9 active, round(5 x 0.386) = 2 reserve; Instantly's ESP Matching sends each lead from its own provider where it can, and replies per 1,000 sends are compared by provider from the first week |
| Resold inboxes | 60 x $3.30 = $198.00 (Hypertide Google), 60 x $3.50 = $210.00 (ScaledMail Google) | Rejected | Cheaper and faster when delivered, but the vendor's account holds the seats and setup windows on their pages are not commitments |

Decision: Google Workspace Business Starter (Flexible) on 19 domains and Exchange Online Plan 1 (annual) on 11 domains, built in Ledgerline's own tenants.

Build path: own tenants, $209.20 a month more than resold Google inboxes ($407.20 against $198.00); Ledgerline holds the admin console, the DKIM keys and the tenant boundary, can leave with its mailboxes, and no launch date depends on a vendor's delivery window.

Tenants: 4 Google Workspace accounts (G1 to G3 with 10 users, G4 with 8) and 3 Microsoft 365 tenants (M1 and M2 with 8 users, M3 with 6). Blast radius: one tenant problem pauses at most 10 mailboxes; reserves sit in 5 different tenants.

## Sending Domains and Mailboxes

| Domain | Role | Provider and tenant | Mailboxes |
|-|-|-|-|
| getledgerline.example | Active | Google, G1 | priya@getledgerline.example, marcus.bell@getledgerline.example |
| tryledgerline.example | Active | Google, G1 | elena@tryledgerline.example, tom.okafor@tryledgerline.example |
| ledgerlinehq.example | Active | Google, G1 | sara@ledgerlinehq.example, dev.mehta@ledgerlinehq.example |
| meetledgerline.example | Active | Google, G1 | hannah@meetledgerline.example, priya.natarajan@meetledgerline.example |
| withledgerline.example | Active | Google, G1 | marcus@withledgerline.example, elena.ruiz@withledgerline.example |
| useledgerline.example | Active | Google, G2 | tom@useledgerline.example, sara.lindqvist@useledgerline.example |
| goledgerline.example | Active | Google, G2 | dev@goledgerline.example, hannah.cole@goledgerline.example |
| ledgerlineapp.example | Active | Google, G2 | priya@ledgerlineapp.example, marcus.bell@ledgerlineapp.example |
| joinledgerline.example | Active | Google, G2 | elena@joinledgerline.example, tom.okafor@joinledgerline.example |
| hiledgerline.example | Reserve | Google, G2 | sara@hiledgerline.example, dev.mehta@hiledgerline.example |
| ledgerlineteam.example | Active | Google, G3 | hannah@ledgerlineteam.example, priya.natarajan@ledgerlineteam.example |
| teamledgerline.example | Active | Google, G3 | marcus@teamledgerline.example, elena.ruiz@teamledgerline.example |
| myledgerline.example | Active | Google, G3 | tom@myledgerline.example, sara.lindqvist@myledgerline.example |
| ledgerlinelabs.example | Active | Google, G3 | dev@ledgerlinelabs.example, hannah.cole@ledgerlinelabs.example |
| ledgerlinegroup.example | Reserve | Google, G3 | priya@ledgerlinegroup.example, marcus.bell@ledgerlinegroup.example |
| ledgerlinehub.example | Active | Google, G4 | elena@ledgerlinehub.example, tom.okafor@ledgerlinehub.example |
| askledgerline.example | Active | Google, G4 | sara@askledgerline.example, dev.mehta@askledgerline.example |
| seeledgerline.example | Active | Google, G4 | hannah@seeledgerline.example, priya.natarajan@seeledgerline.example |
| ledgerlinenow.example | Reserve | Google, G4 | marcus@ledgerlinenow.example, elena.ruiz@ledgerlinenow.example |
| ledgerlinecloud.example | Active | Microsoft, M1 | tom@ledgerlinecloud.example, sara.lindqvist@ledgerlinecloud.example |
| ledgerlinedata.example | Active | Microsoft, M1 | dev@ledgerlinedata.example, hannah.cole@ledgerlinedata.example |
| ledgerlineinc.example | Active | Microsoft, M1 | priya@ledgerlineinc.example, marcus.bell@ledgerlineinc.example |
| ledgerlinecorp.example | Active | Microsoft, M1 | elena@ledgerlinecorp.example, tom.okafor@ledgerlinecorp.example |
| theledgerline.example | Active | Microsoft, M2 | sara@theledgerline.example, dev.mehta@theledgerline.example |
| ledgerlineco.example | Active | Microsoft, M2 | hannah@ledgerlineco.example, priya.natarajan@ledgerlineco.example |
| ledgerlinerev.example | Active | Microsoft, M2 | marcus@ledgerlinerev.example, elena.ruiz@ledgerlinerev.example |
| ledgerlinepro.example | Reserve | Microsoft, M2 | tom@ledgerlinepro.example, sara.lindqvist@ledgerlinepro.example |
| ledgerlinesuite.example | Active | Microsoft, M3 | dev@ledgerlinesuite.example, hannah.cole@ledgerlinesuite.example |
| ledgerlineforecast.example | Active | Microsoft, M3 | priya@ledgerlineforecast.example, marcus.bell@ledgerlineforecast.example |
| ledgerlinesoftware.example | Reserve | Microsoft, M3 | elena@ledgerlinesoftware.example, tom.okafor@ledgerlinesoftware.example |

All domains: registered 2026-10-13 at Porkbun, WHOIS privacy on; 301 to https://ledgerline.example on `@` and `www`; nameservers curitiba.ns.porkbun.com, fortaleza.ns.porkbun.com, maceio.ns.porkbun.com, salvador.ns.porkbun.com; DNSSEC Off (no DS record, so a later move to Cloudflare cannot strand them); renewal 2027-10-13 with auto-renew on, renewal notices to ops@ledgerline.example.

## Tenant Settings

| Provider | Setting | Value | Why |
|-|-|-|-|
| Microsoft 365 (M1 to M3) | Subscription | Exchange Online Plan 1, paid and annual, bought 2026-10-13 before any domain work; no trial | Trial tenants are capped at 500 external recipients a day; the age clock starts at creation |
| Microsoft 365 | Tenant age quota | M1 and M2 (8 licenses): 1,164 external recipients a day through 2026-11-12, 2,911 through 2026-12-12, 11,644 after. M3 (6 licenses): 1,125, 2,813, then 11,253. Peak use 8 x (30 cold + 10 warmup) = 320 a day; wide build 8 x (15 + 10) = 200 | New tenants get 10% of the standard quota for 30 days and 25% to day 60; warmup mail counts |
| Microsoft 365 | Custom domains | All 11 Microsoft domains verified; each tenant's default domain set to one of them | Mail from onmicrosoft.com is limited to 100 external recipients a day |
| Microsoft 365 | DKIM | Enabled per domain in the Defender portal once both CNAMEs resolve, rotated to 2048-bit | Without it, mail is signed with the tenant's default domain and DKIM does not align |
| Microsoft 365 | Outbound spam policy "Cold email" | Applied to all 22 users: 20 external recipients an hour (the top of Apollo's 10 to 20), 50 a day (Alex Berman's per-inbox ceiling), restrict until the following day, automatic forwarding Off | A runaway sequence or a stolen password stops at 50 instead of 10,000 |
| Microsoft 365 | Sequencer connection and sign-in | Instantly by Sign in with Microsoft (OAuth); SMTP AUTH left off; MFA through security defaults | Basic SMTP AUTH turns off by default at the end of December 2026 |
| Google Workspace (G1 to G4) | Subscription | Business Starter, Flexible, paid from 2026-10-13; no trial | Trial users are capped at 500 messages a day; Flexible seats can be removed any month |
| Google Workspace | Domains and OU | Each sending domain added as a secondary domain (not an alias); all users in a "Cold email" OU with 2-Step Verification enforced | Each mailbox gets its own identity and policy |
| Google Workspace | DKIM | 2048-bit key per domain, Start authentication once the TXT resolves | DKIM aligned with the From domain |

## DNS Record Template

Google Workspace block, filled in for getledgerline.example. Applies to: the other 18 Google domains in Sending Domains and Mailboxes.

| Provider | Record | Type | Host | Value | Differs per domain |
|-|-|-|-|-|-|
| Google Workspace | Verification | TXT | @ | google-site-verification=(token from Admin console) | Yes, token |
| Google Workspace | MX | MX | @ | smtp.google.com, priority 1 | No |
| Google Workspace | SPF | TXT | @ | v=spf1 include:_spf.google.com ~all | No |
| Google Workspace | DKIM | TXT | google._domainkey | v=DKIM1; k=rsa; p=(2048-bit key from Admin console) | Yes, key |
| Google Workspace | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.example | No |
| Google Workspace | Postmaster | TXT | @ | google-site-verification=(token from Postmaster Tools) | Yes, token |
| Google Workspace | Tracking | CNAME | inst | prox.itrackly.com, DNS-only | No |
| Google Workspace | Redirect | URL forward | @ and www | 301 to https://ledgerline.example | No |

Microsoft 365 block, filled in for ledgerlinecloud.example. Applies to: the other 10 Microsoft domains in Sending Domains and Mailboxes.

| Provider | Record | Type | Host | Value | Differs per domain |
|-|-|-|-|-|-|
| Microsoft 365 | Verification | TXT | @ | MS=ms(number from admin center) | Yes |
| Microsoft 365 | MX | MX | @ | (tenant token).mail.protection.outlook.com, priority as shown in the admin center | Yes, token |
| Microsoft 365 | SPF | TXT | @ | v=spf1 include:spf.protection.outlook.com -all | No |
| Microsoft 365 | Autodiscover | CNAME | autodiscover | autodiscover.outlook.com | No |
| Microsoft 365 | DKIM | CNAME | selector1._domainkey | selector1 target copied from the Defender portal (new format ends in dkim.mail.microsoft) | Yes |
| Microsoft 365 | DKIM | CNAME | selector2._domainkey | selector2 target copied from the Defender portal | Yes |
| Microsoft 365 | DMARC | TXT | _dmarc | v=DMARC1; p=none; rua=mailto:dmarc@ledgerline.example | No |
| Microsoft 365 | Postmaster | TXT | @ | google-site-verification=(token from Postmaster Tools) | Yes, token |
| Microsoft 365 | Tracking | CNAME | inst | prox.itrackly.com, DNS-only | No |
| Microsoft 365 | Redirect | URL forward | @ and www | 301 to https://ledgerline.example | No |

Main domain changes: one record on ledgerline.example, `*._report._dmarc.ledgerline.example` TXT `v=DMARC1`, so all 30 sending domains, and any added later, can send aggregate reports to dmarc@ledgerline.example. The main domain's own DMARC record stays as it is.

How the records get written: Porkbun API, with API access on for all domains, TTL 600. `domains.csv` holds one `domain,google` or `domain,microsoft` line per sending domain; `tokens/DOMAIN.env` holds the values copied from the admin consoles. Run it once as is (dry run, each response shows `wouldSucceed`), then with `DRY_RUN=false`; every live response must show `"status": "SUCCESS"`. A Google domain whose DKIM key appears later is run again with only its DKIM line.

```bash
#!/usr/bin/env bash
# tokens/DOMAIN.env: VERIFY, POSTMASTER, and DKIM (Google) or MX_HOST, MX_PRIO, DKIM1, DKIM2 (Microsoft)
set -euo pipefail
API="https://api.porkbun.com/api/json/v3/dns/create"
MAIN="ledgerline.example"
DRY_RUN="${DRY_RUN:-true}"
add() {  # domain type name content [prio]
  body=$(printf '{"apikey":"%s","secretapikey":"%s","type":"%s","name":"%s","content":"%s","ttl":600,"prio":%s,"dryRun":%s}' \
    "$PB_KEY" "$PB_SECRET" "$2" "$3" "$4" "${5:-0}" "$DRY_RUN")
  curl -s -X POST "$API/$1" -H "Content-Type: application/json" -d "$body"; echo
}
while IFS=, read -r d provider; do
  source "tokens/$d.env"
  add "$d" TXT   ""                     "$VERIFY"
  add "$d" TXT   ""                     "$POSTMASTER"
  add "$d" TXT   "_dmarc"               "v=DMARC1; p=none; rua=mailto:dmarc@$MAIN"
  add "$d" CNAME "inst"                 "prox.itrackly.com"
  if [ "$provider" = "google" ]; then
    add "$d" MX    ""                   "smtp.google.com" 1
    add "$d" TXT   ""                   "v=spf1 include:_spf.google.com ~all"
    add "$d" TXT   "google._domainkey"  "$DKIM"
  else
    add "$d" MX    ""                   "$MX_HOST" "$MX_PRIO"
    add "$d" TXT   ""                   "v=spf1 include:spf.protection.outlook.com -all"
    add "$d" CNAME "autodiscover"       "autodiscover.outlook.com"
    add "$d" CNAME "selector1._domainkey" "$DKIM1"
    add "$d" CNAME "selector2._domainkey" "$DKIM2"
  fi
done < domains.csv
```

## Launch Timeline

Requested: 1,500 sends a day from Tuesday 2026-11-03.

Warmup settings, every mailbox in Instantly: increase 1 a day, daily warmup limit 10, reply rate 30%, left on at those values once cold mail starts; campaign daily limit 0 until the first cold day.

Ramp: 10 a mailbox on all 60 mailboxes for 5 sending days, 20 for the next 5, then 30 on the 50 active mailboxes while the 10 reserves go back to warmup only. Each raise waits for the Wednesday review to pass.

| Path | Warmup start | First cold send | Full volume | Against the request |
|-|-|-|-|-|
| Standard (21 days), recommended for the 60-mailbox build | 2026-10-15 | 2026-11-05, 600 a day; 1,200 from 2026-11-12 | 2026-11-19, 1,500 a day | First sends 2 days late; full volume 16 days late |
| Soft start (14 days) | 2026-10-15 | 2026-10-29, 600 a day; 1,200 from 2026-11-05 | 2026-11-12, 1,500 a day | First sends 5 days early; full volume 9 days late |
| Wide build, 100 mailboxes at 15, 21-day warmup | 2026-10-15 | 2026-11-05, 1,500 a day | 2026-11-05 | 2 days late; on the 14-day warmup, 1,500 a day from 2026-10-29, 5 days early |

Recommendation: the standard path on the 60-mailbox build if 1,500 a day in late November is acceptable; the wide build if the date is worth $284.07 a month more. The Head of Sales picks the build on 2026-10-13, before anything is bought. The soft start is chosen on 2026-10-28 only for mailboxes showing an Instantly health score above 90% with a send file of valid addresses; the Microsoft tenants are 16 days old on 2026-10-29 and still inside their 10% quota window, which the planned use fits.

## Monitoring

Setup: all 30 domains added and verified in Google Postmaster Tools (the Postmaster row in each template). Postmaster reports only mail to personal Gmail and hides low-volume days, so a B2B list will show thin data there; seed tests carry the Microsoft side. Microsoft SNDS is not set up: it reports on IP addresses you control, and Workspace and Microsoft 365 send from shared provider IPs, so it does not apply here. Each Microsoft tenant's outbound external recipients report is read every Monday against the quota in Tenant Settings. All 30 DKIM domains are enrolled in Yahoo's complaint feedback loop. The seed list covers Gmail, Google Workspace, Outlook.com, Microsoft 365 and one Proofpoint-protected mailbox.

| Signal | Where | Act at | Stop at |
|-|-|-|-|
| Spam rate, personal Gmail | Postmaster Tools, per domain, daily | 0.1%, Google's line: hold that domain's volume and find the cause | 0.3%: stop the domain, promote a reserve |
| Hard bounces | Instantly, per campaign, after 200 sends | 2% (Alex Berman): pause the campaign, re-validate the list | 5%: Instantly's default auto-pause |
| Blocklist | Spamhaus checker, every Monday, all domains and tracking hosts | Any listing: pause the domain, request removal | Relisted after removal: retire the domain |
| Seed placement | Seed test every Wednesday, before each ramp raise | Spam at any provider: hold the raise, check copy, links, authentication | |
| Instantly health score | Per account, daily | Under 90%: hold that mailbox's cold cap until it recovers | |
| Microsoft tenant quota | Exchange admin center report, Mondays | Before each ramp step: planned use against the quota at the tenant's age | 100%: external mail blocked until the 24-hour window clears |
| Replies per 1,000 sends by recipient provider | Instantly, Fridays from the first full-volume week | The Head of Sales reviews the gap and decides any shift of reserves | |

## Cost Estimate

| Item | Numbers | Monthly |
|-|-|-|
| Google Workspace Business Starter, Flexible | 38 seats x $8.40 | $319.20 |
| Exchange Online Plan 1, annual | 22 seats x $4.00 (commits $1,056 for 12 months) | $88.00 |
| Domains, Porkbun `.com` | 30 x $11.08 = $332.40 a year, / 12 | $27.70 |
| Instantly Hypergrowth, monthly billing | 125,000 emails a month; the build sends 31,500 | $97.00 |
| Total | $319.20 + $88.00 + $27.70 + $97.00 | $531.90 |

Wide build instead: 62 x $8.40 + 38 x $4.00 + 50 x $11.08 / 12 + $97.00 = $815.97 a month, $284.07 more.

Not in the total: list validation, if the send file is not validated elsewhere, 10,500 new prospects a month x $0.00169 = $17.75; the provider-mix sample already run cost $0.85.

## Launch Risks and Scaling Triggers

Domain age: every domain is new and Spamhaus starts unknown domains at a poor reputation, so none sends cold mail before 14 days of warmup and none sends 30 a day before the ramp's 11th sending day.

Blast radius: one domain problem pauses 2 mailboxes (4% of volume), covered by 5 reserves; one tenant problem pauses at most 10 mailboxes, and no tenant holds more than one reserve.

| Trigger | Action |
|-|-|
| A reserve is promoted | Register and warm 1 new domain with 2 mailboxes that week in the tenant with the fewest users (ready about 24 days later) |
| The daily target rises above 1,500 sends | Add 1 domain and 2 mailboxes per 60 extra sends a day, warmed 21 days before use |
| Replies per 1,000 sends differ between the Google and Microsoft pods after the first full month at full volume | The Head of Sales decides any move of reserves; annual Microsoft seats stay in warmup until renewal |
| A domain is paused for complaints or a Spamhaus listing | Promote a reserve; buy no replacement until the cause is found |

## Launch Checklist

| Step | Owner | Date | Done when |
|-|-|-|-|
| Choose the 60-mailbox build or the wide build | Head of Sales | 2026-10-13 | Build named in writing |
| Buy 3 Microsoft 365 tenants with 22 Exchange Online Plan 1 seats, paid | IT admin | 2026-10-13 | Tenants show paid subscriptions; creation date recorded |
| Register 30 domains, privacy, auto-renew and 301 forwarding on | Ops lead | 2026-10-13 | 30 active at Porkbun; `curl -sI` returns the ledgerline.example location for all 30 |
| Open 4 Workspace accounts, Business Starter Flexible, secondary domains added | IT admin | 2026-10-13 | 19 domains verified across G1 to G4 |
| Records by the script above, dry run then live; wildcard record on the main domain | Ops lead | 2026-10-13 | `dig` returns one SPF and one DMARC per domain; `*._report._dmarc.ledgerline.example` resolves |
| Create 60 users; 2-Step Verification and MFA; outbound spam policy on the 22 Microsoft users | IT admin | 2026-10-14 | 60 users active, policy applied |
| Verify 30 domains in Postmaster Tools; enroll them in Yahoo's feedback loop | Ops lead | 2026-10-14 | 30 of 30 show Verified |
| DKIM signing on for all 30; header test from all 60 mailboxes to Gmail and Outlook.com | IT admin | 2026-10-15 | 60 of 60 show spf=pass, dkim=pass, dmarc=pass |
| Instantly connected by OAuth, warmup settings above, campaign limit 0, tracking domain verified; Spamhaus check | SDR manager | 2026-10-15 | 60 accounts warming; no listings |
| Move DMARC to `p=quarantine` on all 30 | Ops lead | 2026-10-22 | A week of daily report reads with every mailbox aligned |
| Choose standard or soft start per mailbox | Head of Sales | 2026-10-28 | Health scores read for all 60 mailboxes |
| First cold sends, 10 a mailbox on all 60 | SDR manager | 2026-11-05 (soft start 2026-10-29) | 600 sent; bounces under 2% |
| Raise to 20 a mailbox | SDR manager | 2026-11-12 (soft start 2026-11-05) | Wednesday review passed |
| 30 a mailbox on the 50 active; reserves back to warmup only | SDR manager | 2026-11-19 (soft start 2026-11-12) | 1,500 a day, bounces under 2%, spam rate under 0.1% |

## Sources

- Instantly help center, checked 2026-10-13: account limits (30 a day) https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits; warmup settings (1, 10, 30%) https://help.instantly.ai/en/articles/9214350-warmup-settings; account readiness (2 weeks, 3 for AirMail, health above 90%) https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns; tracking domain (`inst`) https://help.instantly.ai/en/articles/6984188-custom-tracking-domain; bounce auto-pause (5%) https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature; pricing https://instantly.ai/pricing
- Alex Berman: new domains at 10 to 20 a day, ramp over 2 to 4 weeks, bounces under 2% https://alexberman.com/cold-email-templates; under 50 a day per inbox https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Spamhaus Domain Blocklist FAQ (unknown reputations begin as poor) https://www.spamhaus.org/blocklists/domain-blocklist/
- Microsoft: new-tenant quota MC1454397 https://mc.merill.net/message/MC1454397; outbound spam policies https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-policies-configure; Exchange Online plans https://www.microsoft.com/en-us/microsoft-365/exchange/compare-microsoft-exchange-online-plans
- Google: spam rate 0.1% https://support.google.com/mail/answer/15256272 and 0.3% https://support.google.com/a/answer/14229414; Workspace plan prices https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans
- Apollo, 10 to 20 an hour per mailbox https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- Porkbun: pricing https://porkbun.com/products/domains; DNS API https://porkbun.com/llms/dns
- Resold inboxes: Hypertide https://www.hypertide.io/pricing; ScaledMail https://scaledmail.com/pricing
- Mailbox naming, Puzzle Inbox (May 18, 2026) https://puzzleinbox.com/blog/cold-email-inbox-naming-conventions
