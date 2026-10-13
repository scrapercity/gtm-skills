# DNS Records Checklist for Cold Email Sending Domains

Every record a secondary sending domain needs, with exact hosts and values for Google Workspace and Microsoft 365, plus tracking, redirect and BIMI. Values were checked against the provider documentation listed under Sources on 2026-10-12. Provider consoles generate some values per tenant (Microsoft MX token, DKIM keys); copy those from the console and never type them from memory.

Notation: `@` means the domain itself (for example `getacme.com`). TTL 3600 unless the DNS host forces "Auto".

## 1. Records per domain at a glance

| # | Record | Type | Host | Required | Source of the value |
|-|-|-|-|-|-|
| 1 | Provider verification | TXT | `@` | Yes | Admin console (Google: `google-site-verification=...`; Microsoft: `MS=ms...`) |
| 2 | MX | MX | `@` | Yes | Fixed (Google) or tenant token (Microsoft) |
| 3 | SPF | TXT | `@` | Yes | Fixed include per provider |
| 4 | DKIM | TXT (Google) or 2 x CNAME (Microsoft) | `google._domainkey` or `selector1/2._domainkey` | Yes | Admin console |
| 5 | DMARC | TXT | `_dmarc` | Yes | You write it |
| 6 | DMARC report authorization | TXT | `<sendingdomain>._report._dmarc` on the report domain | Only when `rua` points to another domain you own | You write it |
| 7 | Custom tracking domain | CNAME | Sequencer-specific (`inst`, `emailtracking`, ...) | Only if open or click tracking is on | Sequencer help page |
| 8 | Redirect to main site | A or ALIAS (proxied) plus a redirect rule, or registrar URL forwarding | `@` and `www` | Yes | Registrar or Cloudflare |
| 9 | Autodiscover | CNAME | `autodiscover` | Microsoft 365 only | Fixed |
| 10 | BIMI | TXT | `default._bimi` | Optional, rarely worth it for cold domains | You write it |

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

Because the reports go to a different domain (`acme.com`), publish this authorization on the main domain once per sending domain:

```text
getacme.com._report._dmarc.acme.com.  TXT  "v=DMARC1"
```

Or point `rua` at a hosted DMARC report service address, which handles authorization for you.

Progression (house standard):

| Day | Policy | Condition to move on |
|-|-|-|
| 1 to 30 | `p=none` | Aggregate reports show 100% of your mailboxes' mail passing DKIM aligned |
| 31 onward | `p=quarantine` | No legitimate source failing alignment for 14 days |
| Optional | `p=reject` | Only if the team wants BIMI or spoofing protection; cold domains gain little |

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
| Instantly | `inst` (must be exactly this) | `prox.itrackly.com` | Email account > Settings > Custom tracking domain, then Check Status | 2026-10-12, help.instantly.ai/en/articles/6984188 |
| Smartlead | `emailtracking` (any host works) | `open.sleadtrack.com` | Email account > Custom tracking domain, enter `http://emailtracking.getacme.com`, Verify CNAME | 2026-10-12, helpcenter.smartlead.ai/en/articles/50 |
| Lemlist, EmailBison, ManyReach, Apollo, HubSpot | Per the vendor screen | Copy from the vendor's tracking-domain setting | Vendor docs | Not verified here; read the setting screen |

On Cloudflare, set the CNAME to DNS-only (gray cloud). A proxied record breaks verification. Instantly allows 24 to 72 hours for propagation; Smartlead says 30 minutes to 24 hours.

House standard: open tracking off on step 1 of cold sequences, on for later steps only when testing subject lines. Alex Berman's May 2026 piece on tracking domains makes the same call and notes that Apple Mail Privacy Protection inflates opens.

## 7. Redirect to the main site

Every sending domain sends visitors to the main site with a 301.

**Cloudflare:**
1. DNS: add `A @ 192.0.2.1` proxied (orange cloud) and `CNAME www @` proxied. The IP is a placeholder; Cloudflare answers the request before it reaches it.
2. Rules > Redirect Rules > Create > Wildcard pattern. Request URL `http*://*getacme.com/*`, target `https://acme.com/`, status 301.
3. Leave MX, DKIM, DMARC and the tracking CNAME DNS-only.

**Porkbun or Namecheap:** use the registrar's URL forwarding for `@` and `www`, permanent (301), target `https://acme.com`. Confirm forwarding does not overwrite MX records.

Test: `curl -sI https://getacme.com | grep -i location` should print `location: https://acme.com/`.

## 8. BIMI (optional)

Gmail shows a brand logo only when all of these hold (support.google.com/a/answer/10911320): DMARC `p=quarantine` or `p=reject` (with `pct=100` if `pct` is present), a Verified Mark Certificate from DigiCert or Entrust for a trademarked logo, and an SVG Tiny PS logo served over HTTPS. Trademark registration can take 6 months to over a year.

```text
default._bimi.acme.com.  TXT  "v=BIMI1; l=https://acme.com/bimi/logo.svg; a=https://acme.com/bimi/vmc.pem"
```

For cold sending domains, skip BIMI unless the company already holds a VMC for the main brand. It costs the certificate fee per year and does not change whether a cold email reaches the inbox.

## 9. Domain naming rules

| Rule | Good | Bad | Why |
|-|-|-|-|
| Brand stays recognizable | `getacme.com`, `tryacme.com`, `acmehq.com`, `acme-team.com`, `meetacme.com` | `a-c-m-e-sales.net` | A recipient who checks the domain should see the brand |
| `.com` first, then `.co` or `.io` | `acmehq.com` | `acme.xyz`, `acme.top` | Cheap new TLDs carry more abuse history with filters |
| No spam words | `withacme.com` | `acmepromo.com`, `acmedeals.com`, `acmemail.com` | Words like these are flagged by content filters and by people |
| No lookalikes of other brands | | `acrne.com`, `g00gle-acme.com` | Reads as phishing |
| Hyphens at most one | `acme-team.com` | `acme-sales-team-hq.com` | Long hyphenated names look disposable |
| One brand per set | Agency client A gets its own 6 domains | Mixing clients on one domain | One client's complaints hit another |

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

- [ ] Registered with privacy and auto-renew on
- [ ] Redirect returns 301 to the main site
- [ ] Verification TXT added and confirmed in the admin console
- [ ] MX record live, test inbound message received
- [ ] One SPF record, provider include present, under 10 lookups
- [ ] DKIM published and signing turned on in the console
- [ ] DMARC `p=none` with `rua`; report authorization on the main domain if needed
- [ ] Tracking CNAME DNS-only and verified in the sequencer (if tracking is on)
- [ ] Header test shows SPF, DKIM and DMARC pass at Gmail and Outlook.com
- [ ] Domain checked at check.spamhaus.org before the first send
- [ ] Mailboxes handed to `inbox-setup`

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
- Instantly, Custom tracking domain: https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- Smartlead, Custom tracking domain: https://helpcenter.smartlead.ai/en/articles/50-setting-up-smartlead-custom-tracking-domain-for-better-email-engagement
- Cloudflare, Create a redirect rule: https://developers.cloudflare.com/rules/url-forwarding/single-redirects/create-dashboard/
- Cloudflare Registrar FAQ: https://developers.cloudflare.com/registrar/faq/
- Alex Berman, custom tracking domains and Gmail: https://alexberman.com/custom-tracking-domain-gmail
