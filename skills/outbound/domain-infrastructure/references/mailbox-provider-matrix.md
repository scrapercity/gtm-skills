# Mailbox Provider Decision Matrix

Which provider hosts the cold email mailboxes. Prices and limits were read from each vendor's own page on 2026-10-12 and change often; re-check before a purchase over $100 and put the check date in the plan.

## 1. Side by side

| Factor | Google Workspace | Microsoft 365 / Exchange Online | Sequencer-bundled mailboxes (ManyReach ManySenders) | Private SMTP or dedicated IPs (EmailBison, ManyReach private IPs) |
|-|-|-|-|-|
| Entry price | Business Starter $8.40 per user a month Flexible, $7.00 Annual (Google billing help, 2026-10-12) | Exchange Online Plan 1 $4.00 per user a month paid yearly; Business Basic $7.00 paid yearly (microsoft.com, 2026-10-12) | $4 a month per Google or Microsoft mailbox plus $15 a year per domain (manyreach.com/pricing, 2026-10-12) | EmailBison Base Plan $599 a month with dedicated IPs and a monthly allowance of 500,000 sends; ManyReach Business $79 a month with 1 private IP, extra IPs $29 a month |
| Commitment | Flexible: add or remove any month. Annual: remove users only at renewal | Plan 1 and Business Basic as listed are annual; monthly billing exists at a higher price in the admin center | Monthly | Monthly |
| Provider daily cap | 2,000 messages per user per day; 500 on trial accounts; rolling 24 hours | 10,000 recipients per day per mailbox; 30 messages a minute; trial tenants 5,000 external recipients a day | Inherits Google or Microsoft caps | Set by the platform and IP warmup |
| DKIM | TXT `google._domainkey`, 2048-bit available | 2 CNAMEs, default 1024-bit, rotate to 2048 | Configured by the vendor | Configured by the vendor; you add their records |
| Admin effort per domain | Add domain alias or secondary domain, verify, MX, DKIM | Add domain, verify, MX token, DKIM CNAMEs, enable signing | Lowest: vendor provisions | Medium: IP warmup is on you |
| Works with Instantly, Smartlead, Lemlist, EmailBison, ManyReach | Yes (OAuth or app password) | Yes (OAuth) | ManyReach only | The platform that owns the IPs |
| Postmaster visibility | Postmaster Tools covers the domain whatever the mailbox provider | Same; SNDS only if you own the IPs (you do not on Microsoft 365) | Same as underlying | SNDS for the dedicated IPs |
| Best for | Default for most B2B senders | Testing against Microsoft-heavy recipient lists; lowest per-seat price | Agencies that want mailboxes provisioned inside the sequencer | Senders above several thousand a day who will manage IP reputation |
| Main risk | Seat cost adds up past 50 mailboxes | Newer tenants and domains face stricter outbound spam policy; M365 security defaults can block SMTP auth | Vendor lock-in; check where mailboxes live if you leave | IP reputation is entirely yours; a bad week burns the IP |

Caps above are provider maximums, far above the 30 to 50 cold sends a day this repo allows per mailbox. The cap that limits you is reputation, never the provider's number.

## 2. Decision rules

Work down the list and stop at the first match.

| # | Condition | Choose | Reason |
|-|-|-|-|
| 1 | The company already runs its main domain on one provider and the team will administer the cold domains themselves | Same provider, separate tenant or separate secondary domains | One admin skill set; keep cold domains out of the main tenant's sending policies if possible |
| 2 | Validation sample (`sc_mx_provider`) shows 60%+ of recipients on Google | Google Workspace | Default |
| 3 | Sample shows 60%+ on Microsoft, or many recipients behind Microsoft-centric gateways | Split test: half Microsoft 365, half Google, compare reply rate and bounce per provider for 2 weeks | Provider matching is an operator hypothesis, not a documented provider rule |
| 4 | Agency with 5+ clients, each needing 5 to 10 domains | Google Workspace per client, or sequencer-bundled mailboxes if the agency already uses ManyReach | Per-client isolation |
| 5 | Target over 3,000 sends a day and a team member who can watch IP reputation daily | Dedicated-IP platform for part of the volume, Workspace for the rest | Seat count above 100 mailboxes gets costly; IPs need active care |
| 6 | Budget under $100 a month | 1 to 2 domains, 3 to 6 Google Starter seats Flexible | Small and stable beats many cheap mailboxes |

## 3. Cost per 1,000 cold sends a month

At 30 cold sends per mailbox per day and 21 sending days, one mailbox sends 630 cold emails a month.

| Provider | Seat price used | Sends a month per seat | Cost per 1,000 sends |
|-|-|-|-|
| Google Workspace Starter, Flexible | $8.40 | 630 | $8.40 / 0.63 = $13.33 |
| Google Workspace Starter, Annual | $7.00 | 630 | $11.11 |
| Exchange Online Plan 1, annual | $4.00 | 630 | $6.35 |
| ManyReach ManySenders | $4.00 plus domain fee | 630 | about $6.35 plus domain |

Add domain cost: one `.com` at $11.08 a year shared by 3 mailboxes is $0.31 a month per mailbox, about $0.49 per 1,000 sends.

These are seat costs only. The sequencer, the data and the validation come on top; see `capacity-and-costs.md`.

## 4. Provider-specific setup notes

**Google Workspace**
- One Workspace account can hold several sending domains as secondary domains, each with its own users. Each domain still needs its own MX, SPF, DKIM key and DMARC.
- Turn on 2-Step Verification for every user; sequencers connect by OAuth.
- Admin console > Apps > Google Workspace > Gmail > Authenticate email > generate a 2048-bit key per domain.
- Keep trial accounts out of cold sending: the 500 a day trial cap is low, and new accounts on trial are still building history.

**Microsoft 365**
- Add each sending domain in Admin center > Settings > Domains; never send from `*.onmicrosoft.com` (100 external recipients a day per organization).
- Enable DKIM per domain in the Defender portal after the CNAMEs resolve.
- Sequencers connect by OAuth; if a platform needs SMTP AUTH, it must be enabled per mailbox, and Security Defaults can block it.
- Microsoft's documentation says Exchange Online is not built for bulk mail and points high-volume senders to a bulk provider. Keep per-mailbox volume low.

**Other mailbox hosts (Zoho Mail and similar)**
- Zoho lists Mail Lite and Mail Premium as annual-only plans. The live page did not show USD prices on 2026-10-12, so price it at checkout.
- Fewer sequencers document native connection for these hosts; check the sequencer's supported providers before buying.

## 5. What not to do

| Pattern | Problem |
|-|-|
| Free Gmail or Outlook.com accounts for cold email | Consumer terms; low caps (HubSpot lists free Gmail at 350 a day for one-to-one sends); no domain identity |
| Buying "aged" mailboxes from a stranger | Unknown history, unknown recovery email, credentials you do not control |
| Running cold email from the same tenant and domain as the CEO and billing | One incident takes down company mail |
| More than 3 mailboxes per sending domain to save on domains | One domain carries more volume and more risk; reserve capacity shrinks |

## Sources

- Google Workspace, Compare Flexible and Annual plans (prices): https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans
- Google Workspace, Gmail sending limits: https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace
- Microsoft, Compare Exchange Online plans: https://www.microsoft.com/en-us/microsoft-365/exchange/compare-microsoft-exchange-online-plans
- Microsoft, Compare Microsoft 365 business plans: https://www.microsoft.com/en-us/microsoft-365/business/compare-all-microsoft-365-business-products
- Microsoft, Exchange Online limits: https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- Microsoft, Configure DKIM: https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
- ManyReach, Pricing: https://manyreach.com/pricing
- EmailBison, Pricing: https://emailbison.com/pricing
- Zoho Mail, Pricing: https://www.zoho.com/mail/zohomail-pricing.html
- HubSpot, Sales email send limits: https://knowledge.hubspot.com/connected-email/sales-email-send-limits
- Porkbun, Domain pricing: https://porkbun.com/products/domains
