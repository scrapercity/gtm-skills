# DNS Records Checklist for Cold Email Sending Domains

Every record a secondary sending domain needs, with exact hosts and values for Google Workspace and Microsoft 365, plus tracking, redirect and BIMI. Values were checked against the provider documentation listed under Sources on 2026-10-12. Provider consoles generate some values per tenant (Microsoft MX token, DKIM keys); copy those from the console and never type them from memory.

Notation: `@` means the domain itself (for example `getacme.com`). TTL 600 (10 minutes) while building, so a wrong value clears fast; raise to 3600 once every record verifies, or leave it where the DNS host forces "Auto". Every example below uses 600.

## 1. Records per domain at a glance

| # | Record | Type | Host | Required | Source of the value |
|-|-|-|-|-|-|
| 1 | Provider verification | TXT | `@` | Yes | Admin console (Google: `google-site-verification=...`; Microsoft: `MS=ms...`) |
| 2 | MX | MX | `@` | Yes | Fixed (Google) or tenant token (Microsoft) |
| 3 | SPF | TXT | `@` | Yes | Fixed include per provider |
| 4 | DKIM | TXT (Google) or 2 x CNAME (Microsoft) | `google._domainkey` or `selector1/2._domainkey` | Yes | Admin console |
| 5 | DMARC | TXT | `_dmarc` | Yes | You write it |
| 6 | DMARC report authorization | TXT | `*._report._dmarc` on the report domain, once for all sending domains | Only when `rua` points to another domain you own | You write it |
| 7 | Custom tracking domain | CNAME | The sequencer's documented host: Instantly exactly `inst`; Smartlead any host, `emailtracking` by convention | Only if open or click tracking is on | Sequencer help page |
| 8 | Redirect to main site | A or ALIAS (proxied) plus a redirect rule, or registrar URL forwarding | `@` and `www` | Yes | Registrar or Cloudflare |
| 9 | Autodiscover | CNAME | `autodiscover` | Microsoft 365 only | Fixed |
| 10 | BIMI | TXT | `default._bimi` | Optional, usually skipped for cold domains | You write it |
| 11 | Postmaster Tools verification | TXT (or CNAME) | `@` | Yes, on every sending domain | Postmaster Tools > Add new domain > Verify domain; a token separate from the Workspace verification token |

## 2. Google Workspace values

| Record | Host | Value | Notes |
|-|-|-|-|
| MX | `@` | `smtp.google.com` priority `1` | Single MX for accounts created since 2023. Older accounts may use the `aspmx` set, still supported. |
| SPF | `@` | `v=spf1 include:_spf.google.com ~all` | Google recommends `~all`. Add the sequencer's include only if the sequencer sends through its own SMTP servers (OAuth and Workspace SMTP sending go out through Google already). |
| DKIM | `google._domainkey` | `v=DKIM1; k=rsa; p=<key from Admin console>` | Choose 2048-bit if the DNS host accepts long TXT values. The key is available 24 to 72 hours after Gmail is turned on; after publishing, allow up to 48 hours, then click Start authentication in Admin console > Apps > Google Workspace > Gmail > Authenticate email. |
| DMARC | `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@acme.com` | See section 4. |

Long TXT values: some DNS hosts cap a single string at 255 characters. A 2048-bit DKIM key is longer, so it must be split into two quoted strings in one record (`"v=DKIM1; k=rsa; p=MIIBIjAN..." "...IDAQAB"`). Cloudflare and Porkbun accept the full value in one field and split it themselves.

## 3. Microsoft 365 (Exchange Online) values

| Record | Host | Value | Notes |
|-|-|-|-|
| Verification | `@` | `MS=ms12345678` | From Admin center > Settings > Domains > Add domain. |
| MX | `@` | `<MX token>.mail.protection.outlook.com` priority `1` (or the lowest number the host allows) | The token is tenant-specific; copy it from Admin center > Domains > your domain > DNS records. |
| SPF | `@` | `v=spf1 include:spf.protection.outlook.com -all` | Microsoft's documented record. |
| Autodiscover | `autodiscover` | CNAME `autodiscover.outlook.com` | |
| DKIM selector 1 | `selector1._domainkey` | CNAME `selector1-getacme-com._domainkey.<initialprefix>.n-v1.dkim.mail.microsoft` | New-format target for custom domains added from May 2025; the partition letter (`n`, `r`, ...) is assigned by Microsoft. Older domains use `selector1-getacme-com._domainkey.<initialprefix>.onmicrosoft.com`. Copy both values from the Defender portal (Email authentication settings > DKIM) or `Get-DkimSigningConfig`. |
| DKIM selector 2 | `selector2._domainkey` | CNAME `selector2-getacme-com._domainkey.<initialprefix>.n-v1.dkim.mail.microsoft` | Then enable signing for the domain. Default key size is 1024-bit; rotate with `-KeySize 2048`. |
| DMARC | `_dmarc` | `v=DMARC1; p=none; rua=mailto:dmarc@acme.com` | |

Do not send from the tenant's default `*.onmicrosoft.com` address. Microsoft limits outbound mail from those default domains to 100 external recipients per organization per 24 hours (error `550 5.7.236`).

## 4. DMARC: the record and how it changes

Day 1 record for every sending domain:

```text
_dmarc.getacme.com.  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@acme.com"
```

Because the reports go to a different domain (`acme.com`), the report domain has to authorize them. Publish one wildcard record on the main domain:

```text
*._report._dmarc.acme.com.  TXT  "v=DMARC1"
```

RFC 7489 section 7.1 and RFC 9990 section 4 (May 2026) both say a receiver willing to take reports for any domain can use a wildcard record, and both give this form as the example. It replaces one record per sending domain (`getacme.com._report._dmarc.acme.com`), so the main domain's zone changes once, and adding sending domains later needs no change there. The trade-off: any domain on the internet can now send reports to `dmarc@acme.com`. Filter the mailbox, or the report service, by the sending-domain list.

Or point `rua` at a hosted DMARC report service address, which handles authorization for you.

Progression, from Google's recommended DMARC rollout (checked 2026-10-13):

| Stage | Policy | Condition to move on |
|-|-|-|
| First week at least | `p=none` | Set up SPF and DKIM at least 48 hours before DMARC; read the aggregate reports daily until they show your mailboxes' mail passing aligned |
| After that | `p=quarantine` | Google's page moves to quarantine after at least a week of monitoring with no outgoing-mail issues |
| Optional | `p=reject` | Google lists it as an alternative to quarantine; BIMI needs quarantine or reject |

RFC 9989 (May 2026) removed the `pct` tag; leave it out. One record only: two TXT records at `_dmarc` means receivers apply no DMARC.

## 5. SPF rules

1. One TXT record starting `v=spf1` per domain. Merge, never add a second.
2. Count DNS-querying terms (`include`, `a`, `mx`, `ptr`, `exists`, `redirect`) including those nested inside includes. RFC 7208 caps the total at 10; over 10 returns `permerror`.
3. Never use `ptr` (RFC 7208 says it should not be published).
4. A sending domain that only sends from Google or Microsoft needs exactly one include.
5. Keep the record under 450 characters so the DNS answer fits a UDP packet (RFC 7208 guidance).

## 6. Custom tracking domain

Open tracking and click tracking rewrite links and add a pixel on the sequencer's shared domain unless you set your own. A custom tracking domain puts those on a subdomain of the sending domain.

| Sequencer | Host | CNAME target | Where to enable | Checked |
|-|-|-|-|-|
| Instantly | `inst`, exactly (the help page says a wrong host such as `ins` will not verify) | `prox.itrackly.com` | Email account > Settings > Custom tracking domain, then Check Status | 2026-10-13, help.instantly.ai/en/articles/6984188 |
| Smartlead | `emailtracking` (any host works) | `open.sleadtrack.com` | Email account > Custom tracking domain, enter `http://emailtracking.getacme.com`, Verify CNAME | 2026-10-12, helpcenter.smartlead.ai/en/articles/50 |
| Lemlist, EmailBison, ManyReach, Apollo, HubSpot | Per the vendor screen | Copy from the vendor's tracking-domain setting | Vendor docs | Not verified here; read the setting screen |

On Cloudflare, set the CNAME to DNS-only (gray cloud). A proxied record breaks verification. Instantly allows 24 to 72 hours for propagation; Smartlead says 30 minutes to 24 hours.

Open tracking: Alex Berman's May 2026 piece on tracking domains suggests turning it off on first-touch emails and enabling it only on follow-ups, and notes that Apple Mail Privacy Protection preloads images, so opens are a relative signal at best.

## 7. Redirect to the main site

Every sending domain sends visitors to the main site with a 301.

**Cloudflare:**
1. DNS: add `A @ 192.0.2.1` proxied (orange cloud) and `CNAME www @` proxied. The IP is a placeholder; Cloudflare answers the request before it reaches it.
2. Rules > Redirect Rules > Create > Wildcard pattern. Request URL `http*://*getacme.com/*`, target `https://acme.com/`, status 301.
3. Leave MX, DKIM, DMARC and the tracking CNAME DNS-only.

**Porkbun or Namecheap:** use the registrar's URL forwarding for `@` and `www`, permanent (301), target `https://acme.com`. Confirm forwarding does not overwrite MX records.

Test: `curl -sI https://getacme.com | grep -i location` should print `location: https://acme.com/`.

## 8. BIMI (optional)

Gmail shows a brand logo only when all of these hold (support.google.com/a/answer/10911320): DMARC `p=quarantine` or `p=reject` (with `pct=100` if `pct` is present), a Verified Mark Certificate from DigiCert or Entrust for a trademarked logo, and an SVG Tiny PS logo served over HTTPS.

```text
default._bimi.acme.com.  TXT  "v=BIMI1; l=https://acme.com/bimi/logo.svg; a=https://acme.com/bimi/vmc.pem"
```

For cold sending domains, skip BIMI unless the company already holds a VMC for the main brand. It costs the certificate fee per year and does not change whether a cold email reaches the inbox.

## 9. Domain naming rules

| Rule | Good | Bad | Why |
|-|-|-|-|
| Brand stays recognizable | `getacme.com`, `tryacme.com`, `acmehq.com`, `acmeteam.com`, `meetacme.com` | Names unrelated to the brand | Instantly's examples for Shrimp.com are Getshrimp.com and Tryshrimp.com; Smartlead says to pick names closely related to the primary domain |
| `.com` first, or the country TLD of the market | `acmehq.com`, `acme.de` | `acme.biz`, `acme.online` | Instantly says `.com` and country extensions work best and reports weaker reply rates on `.biz` and `.online` from its analysis of 32M cold emails; Smartlead says to avoid `.biz` and `.online` |
| No hyphens, no digits | `acmeteam.com` | `acme-team.com`, `acme2.com`, `get-acme.com` | Instantly: letters only; Smartlead: never buy secondary domains with numbers or hyphens |
| One brand per set | Agency client A gets its own domains | Mixing clients on one domain | One client's complaints hit another's domain reputation |
| Mailbox addresses: `first@` or `first.last@`, real team members, two different people per domain | `priya@`, `marcus.bell@` | `jordanl@`, `samp@`, `sarah123@`, `sales@` | Puzzle Inbox (May 18, 2026): first.last is the most common and most trusted pattern, first@ looks personal, numbers look like a bot, role addresses are flagged |

## 10. Verification commands

```bash
dig +short MX getacme.com
dig +short TXT getacme.com                       # SPF and verification
dig +short TXT google._domainkey.getacme.com     # Google DKIM
dig +short CNAME selector1._domainkey.getacme.com  # Microsoft DKIM
dig +short TXT _dmarc.getacme.com
dig +short CNAME inst.getacme.com                # Instantly tracking
curl -sI https://getacme.com | grep -i location   # redirect
```

Then send one plain message from each mailbox to a personal Gmail and an Outlook.com test address and open "Show original" (Gmail) or the message source (Outlook). Required: `spf=pass`, `dkim=pass header.d=getacme.com`, `dmarc=pass`.

## 11. Launch checklist per domain

- [ ] Registered with privacy and auto-renew on; nameservers, DNSSEC state and renewal date written in the inventory
- [ ] Redirect returns 301 to the main site
- [ ] Verification TXT added and confirmed in the admin console
- [ ] MX record live, test inbound message received
- [ ] One SPF record, provider include present, under 10 lookups
- [ ] DKIM published and signing turned on in the console
- [ ] DMARC `p=none` with `rua`; report authorization on the main domain if needed
- [ ] Tracking CNAME DNS-only and verified in the sequencer (if tracking is on)
- [ ] Header test shows SPF, DKIM and DMARC pass at Gmail and Outlook.com
- [ ] Domain added and verified in Google Postmaster Tools
- [ ] Domain checked at check.spamhaus.org before the first send
- [ ] Mailboxes handed to `inbox-setup`

## 12. Domain inventory: nameservers, DNSSEC, renewal date

Every plan's Sending Domains table carries three registrar columns. They answer the questions that break a domain months after launch: who answers its DNS, whether a nameserver move will take it offline, and when it lapses.

| Column | What to record | Why | Rule |
|-|-|-|-|
| Nameservers | The hostnames from `dig +short NS getacme.com`, for example `curitiba.ns.porkbun.com` plus the other three Porkbun defaults, or the two Cloudflare names assigned to the account | Records only take effect at the DNS host the nameservers point to; a record added at the registrar while Cloudflare answers DNS does nothing | Keep every domain in a set on the same DNS host |
| DNSSEC | On or Off, and where the DS record lives | DNSSEC signs records so resolvers can reject forged answers (ICANN). Cloudflare's docs warn that changing nameservers with DNSSEC still active at the registrar causes connectivity errors, and cached DS records make validating resolvers return SERVFAIL | Off is acceptable for cold domains. If On: disable it at the registrar, wait out the DS TTL, then change nameservers, then re-enable at the new host |
| Renewal date | Registration expiry as YYYY-MM-DD, plus auto-renew on or off | ICANN's Expired Registration Recovery Policy has the registrar interrupt DNS resolution for at least the last 8 days a lapsed name can still be renewed; MX stops resolving, replies bounce, the tracking domain breaks | Auto-renew on, and the card on file checked when the first renewal reminder arrives |

Registrars must send renewal reminders about a month and about a week before expiry under the same ICANN policy. Send them to a shared ops inbox on the main domain, never to a person's mailbox on a sending domain.

Commands:

```bash
dig +short NS getacme.com               # nameservers
dig +short DS getacme.com               # empty = no DNSSEC delegation
whois getacme.com | grep -i expir       # renewal date (registrar format varies)
```

## 13. Bulk DNS by API

Typing 7 records into 10 dashboards is 70 chances for a typo. When the set is large enough that typing is the slower path, write the records with the DNS host's API from one script, then run the section 10 checks in a loop. Endpoints checked 2026-10-13.

| DNS host | Endpoint | Auth | Notes |
|-|-|-|-|
| Cloudflare | `POST https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records` | `Authorization: Bearer <API token>` (preferred over the legacy global key) | `POST .../dns_records/batch` applies deletes, patches, puts and posts in one call: 200 changes per call on Free, 3,500 on Pro and up. MX takes `priority`. Set `"proxied": false` on MX, TXT and tracking CNAMEs |
| Porkbun | `POST https://api.porkbun.com/api/json/v3/dns/create/{domain}` | `apikey` and `secretapikey` in the JSON body, or `X-API-Key` and `X-Secret-API-Key` headers | API access is opt-in per domain or for all domains in account settings. `name` is the host without the domain; MX takes `prio`. Writes succeed even when the domain is not on Porkbun nameservers, and the response says so in `warnings`. `"dryRun": true` validates without writing |
| Other registrars | Check the registrar's API docs | | If there is no API, move DNS to Cloudflare first (section 12 for DNSSEC) |

Porkbun loop for a mixed Google Workspace and Microsoft 365 set. It writes every DNS row of both provider blocks; the 301 forward is set with the registrar's URL forwarding. Put this script, filled in for the build, in the plan itself.

```bash
#!/usr/bin/env bash
# domains.csv: one line per sending domain: domain,google or domain,microsoft
# tokens/DOMAIN.env, copied from the admin consoles: VERIFY and POSTMASTER (TXT values),
#   plus DKIM for Google, or MX_HOST, MX_PRIO, DKIM1, DKIM2 for Microsoft.
# Usage: ./add-records.sh (dry run, nothing written), then DRY_RUN=false ./add-records.sh
set -euo pipefail
API="https://api.porkbun.com/api/json/v3/dns/create"
MAIN="acme.com"
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

The Google DKIM key exists only 24 to 72 hours after Gmail is turned on, so a Google domain whose key is not ready yet runs again with only its DKIM line once the key appears.

Cloudflare, one record (repeat per record or send them in one batch call):

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"type":"TXT","name":"_dmarc.getacme.com","content":"v=DMARC1; p=none; rua=mailto:dmarc@acme.com","ttl":600,"proxied":false}'
```

Read every response: Cloudflare returns `"success": true`; Porkbun returns `"status": "SUCCESS"`, a dry run returns `wouldSucceed` without writing, and either may add `warnings`. Then run `dig` from section 10 against every domain before adding mailboxes.


## Sources

- Google Workspace, Set up MX records: https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace
- Google Workspace, Set up SPF: https://knowledge.workspace.google.com/admin/security/set-up-spf
- Google Workspace, Set up DKIM: https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Google, BIMI requirements: https://support.google.com/a/answer/10911320
- Microsoft, External DNS records for Microsoft 365: https://learn.microsoft.com/en-us/microsoft-365/enterprise/external-domain-name-system-records
- Microsoft, Configure DKIM: https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
- Microsoft, Exchange Online limits: https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- RFC 7208, SPF: https://www.rfc-editor.org/rfc/rfc7208
- RFC 6376, DKIM: https://www.rfc-editor.org/rfc/rfc6376
- RFC 7489, DMARC: https://www.rfc-editor.org/rfc/rfc7489
- RFC 9989, DMARC (May 2026): https://www.rfc-editor.org/rfc/rfc9989.html
- RFC 7489 section 7.1, Verifying External Destinations (wildcard example): https://www.rfc-editor.org/rfc/rfc7489#section-7.1
- RFC 9990, DMARC Aggregate Reporting, section 4 (May 2026, checked 2026-10-13): https://www.rfc-editor.org/rfc/rfc9990.html
- Cloudflare API, Create DNS record (checked 2026-10-13): https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/create/
- Cloudflare API, Batch DNS records (checked 2026-10-13): https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/batch/
- Cloudflare, Batch record changes and per-plan limits: https://developers.cloudflare.com/dns/manage-dns-records/how-to/batch-record-changes/
- Cloudflare, Make API calls (base URL, Bearer token): https://developers.cloudflare.com/fundamentals/api/how-to/make-api-calls/
- Porkbun API v3, DNS guide (checked 2026-10-13): https://porkbun.com/llms/dns
- Porkbun API v3 documentation: https://porkbun.com/api/json/v3/documentation
- Instantly, Custom tracking domain: https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- Smartlead, Custom tracking domain: https://helpcenter.smartlead.ai/en/articles/50-setting-up-smartlead-custom-tracking-domain-for-better-email-engagement
- Cloudflare, Create a redirect rule: https://developers.cloudflare.com/rules/url-forwarding/single-redirects/create-dashboard/
- Cloudflare Registrar FAQ: https://developers.cloudflare.com/registrar/faq/
- Alex Berman, custom tracking domains and Gmail (May 11, 2026): https://alexberman.com/custom-tracking-domain-gmail
- Google Workspace, Recommended DMARC rollout (checked 2026-10-13): https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout
- Instantly, Secondary sending domains (naming, TLDs; checked 2026-10-13): https://help.instantly.ai/en/articles/6502027-scale-your-cold-email-campaigns-with-secondary-sending-domains-the-strategy-how-to-implement-it
- Puzzle Inbox, Cold email inbox naming conventions (Tom Harris, May 18, 2026): https://puzzleinbox.com/blog/cold-email-inbox-naming-conventions
- Smartlead, Secondary sending domains (no numbers or hyphens; checked 2026-10-13): https://helpcenter.smartlead.ai/en/articles/147-all-you-need-to-know-about-secondary-sending-domains-for-cold-email-campaigns
- Cloudflare, DNSSEC (checked 2026-10-13): https://developers.cloudflare.com/dns/dnssec/
- ICANN, DNSSEC: what it is and why it is important: https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en
- ICANN, Expired Registration Recovery Policy (checked 2026-10-13): https://www.icann.org/resources/pages/errp-2013-02-28-en
- Porkbun, How to switch to Porkbun's nameservers (checked 2026-10-13): https://kb.porkbun.com/article/63-how-to-switch-to-porkbuns-nameservers
- Google, Set up Postmaster Tools (verify a domain; checked 2026-10-13): https://support.google.com/mail/answer/9981691
