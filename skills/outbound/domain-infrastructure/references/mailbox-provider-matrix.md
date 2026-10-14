# Mailbox Provider Decision Matrix

Which provider hosts the cold email mailboxes, who owns the tenant, and how each tenant is configured. Prices and limits were re-read from each vendor's own page on 2026-10-13 and change often; re-check before a purchase over $100 and put the check date in the plan.

## 1. Side by side

| Factor | Google Workspace | Microsoft 365 / Exchange Online | Sequencer-bundled mailboxes (ManyReach ManySenders) | Private SMTP or dedicated IPs (EmailBison, ManyReach private IPs) |
|-|-|-|-|-|
| Entry price | Business Starter $8.40 per user a month Flexible, $7.00 Annual (Google billing help, 2026-10-13) | Exchange Online Plan 1 $4.00 per user a month paid yearly; Business Basic $7.00 with Teams or $5.40 without, paid yearly (microsoft.com, 2026-10-13) | $4 a month per Google or Microsoft mailbox plus $15 a year per domain (manyreach.com/pricing, 2026-10-13) | EmailBison Base Plan $599 a month with dedicated IPs and 500,000 sends a month; ManyReach Business $79 a month, extra IPs $29 a month (vendor pages, 2026-10-13) |
| Commitment | Flexible: add or remove any month. Annual: remove users only at renewal | Plan 1 and Business Basic as listed are annual; monthly billing exists at a higher price in the admin center | Monthly | Monthly |
| Provider daily cap | 2,000 messages per user per day; 500 on trial accounts; rolling 24 hours | 10,000 recipients per day per mailbox; 30 messages a minute; a tenant-wide external recipient quota (TERRL) that new tenants get only 10% of for 30 days and 25% of until day 60; trial tenants 500 a day (section 10) | Inherits Google or Microsoft caps | Set by the platform and IP warmup |
| DKIM | TXT `google._domainkey`, 2048-bit available | 2 CNAMEs, default 1024-bit, rotate to 2048 | Configured by the vendor | Configured by the vendor; you add their records |
| Admin effort per domain | Add domain alias or secondary domain, verify, MX, DKIM | Add domain, verify, MX token, DKIM CNAMEs, enable signing | Lowest: vendor provisions | Medium: IP warmup is on you |
| Works with Instantly, Smartlead, Lemlist, EmailBison, ManyReach | Yes (OAuth or app password) | Yes (OAuth) | ManyReach only | The platform that owns the IPs |
| Postmaster visibility | Postmaster Tools covers the domain whatever the mailbox provider | Same; SNDS only if you own the IPs (you do not on Microsoft 365) | Same as underlying | SNDS for the dedicated IPs |
| Best for | Default for B2B senders | Testing against Microsoft-heavy recipient lists; lowest per-seat price | Agencies that want mailboxes provisioned inside the sequencer | Senders above several thousand a day who will manage IP reputation |
| Main risk | Seat cost grows with every mailbox | A tenant under 61 days old runs on a cut quota; annual seats cannot be removed before renewal; Basic SMTP AUTH turns off by default at the end of December 2026 | Vendor lock-in; check where mailboxes live if you leave | IP reputation is entirely yours; a bad week burns the IP |

Caps above are provider maximums, far above Instantly's recommended 30 campaign emails per account a day and Alex Berman's ceiling of 50 per inbox.

## 2. Decision rules

Measure the recipient mix first; it is a required input, never a default. Work down the list and stop at the first match.

| # | Condition | Choose | Reason |
|-|-|-|-|
| 1 | The company already runs its main domain on one provider | Cold domains still go in separate tenants (section 9), never in the main tenant; apply rule 2 for the provider split | The main tenant's billing, admin and outbound policies stay out of cold email's blast radius |
| 2 | Recipient mix measured (validation sample or MX lookup) | Split by the mix from day one: Microsoft active domains = floor(active domains x Microsoft share), the rest Google; Microsoft reserves = round(reserve domains x Microsoft share). When the floor is 0, Google Workspace only | Instantly's ESP Matching sends from the account that matches the lead's provider and asks for sending accounts on more than one provider; Instantly offers no data on the gain, so the plan compares replies per 1,000 sends by provider. A pod added after launch needs its own 21 days of warmup and 15 sending days of ramp, about 6 weeks before it can be compared |
| 2b | A large share of the sample behind one security gateway | Same build; add a seed address behind that gateway to every placement test | Gateways filter on their own rules |
| 3 | Agency with several clients | A separate domain set and Google Workspace account per client, or sequencer-bundled mailboxes if the agency already uses ManyReach | Per-client isolation |
| 4 | A team member who can watch IP reputation daily and a volume the seat bill makes costly | Dedicated-IP platform for part of the volume, Workspace for the rest | IPs need active care |

## 3. Cost per 1,000 cold sends a month

At 30 cold sends per mailbox per day (Instantly's recommendation) and 21 sending days, one mailbox sends 630 cold emails a month.

| Provider | Seat price used | Sends a month per seat | Cost per 1,000 sends |
|-|-|-|-|
| Google Workspace Starter, Flexible | $8.40 | 630 | $8.40 / 0.63 = $13.33 |
| Google Workspace Starter, Annual | $7.00 | 630 | $11.11 |
| Exchange Online Plan 1, annual | $4.00 | 630 | $6.35 |
| ManyReach ManySenders | $4.00 plus domain fee | 630 | about $6.35 plus domain |

Add domain cost: one `.com` at $11.08 a year shared by 3 mailboxes is $0.31 a month per mailbox, about $0.49 per 1,000 sends.

These are seat costs only. The sequencer, the data and the validation come on top; see `capacity-and-costs.md`. Exchange Online Plan 1 at $4.00 is an annual commitment: 22 seats commit $1,056 for the year even if the Microsoft pod is cut after 4 weeks. Google's Flexible plan lets seats go any month.

## 4. Provider-specific setup notes

**Google Workspace** and **Microsoft 365**: the account and tenant settings for cold sending are in sections 10 and 11, in build order.

**Other mailbox hosts (Zoho Mail and similar)**
- Zoho lists Mail Lite and Mail Premium as annual-only plans. The live page did not show USD prices on 2026-10-13, so price it at checkout.
- Fewer sequencers document native connection for these hosts; check the sequencer's supported providers before buying.

## 5. What not to do

| Pattern | Problem |
|-|-|
| Free Gmail or Outlook.com accounts for cold email | Consumer terms; low caps (HubSpot lists free Gmail at 350 a day for one-to-one sends); no domain identity |
| Running cold email from the same tenant and domain as the CEO and billing | One incident takes down company mail |
| More than 3 mailboxes per sending domain to save on domains | Alex Berman, Instantly and Smartlead all give 2 to 3 per domain; one domain incident pauses more mailboxes |

## 6. Managed ("done-for-you") inbox providers

These vendors register or connect the domains, publish the DNS records, create the mailboxes and load them into the sequencer. Every row was read from the vendor's own pricing page on 2026-10-13. Re-check before buying; these pages change often.

| Vendor | What the page says it provides | Pricing model (2026-10-13) | Sending guidance on the page | Terms on the page |
|-|-|-|-|-|
| ScaledMail | Domain registration or connection, SPF, DKIM and DMARC, mailbox provisioning, deliverability monitoring, a Slack support channel; setup in 24 to 72 hours | Google Workspace $3.50 per mailbox a month, 2 to 3 per domain. Microsoft Outlook $50 per domain a month for 25 mailboxes. SMTP server $3.75 per domain a month for 4 mailboxes. Optional reporting $2 per mailbox or $5 per domain a month | Up to 25 a day per Google mailbox; up to 10 a day per Outlook or SMTP mailbox | Minimum and contract question listed, answer not shown on the page |
| Hypertide | Automated setup, DNS, OAuth or SMTP upload to the sequencer, domain-level analytics, API, unlimited seats | Google inboxes $3.30 per inbox a month, "no minimums". Entra Domains $25 per domain a month with 25 inboxes ($1 per inbox), listed with tenant separation | 6,000+ monthly sending capacity per Entra domain | Contract length not stated |
| Mailforge | Mailboxes on a shared IP pool, automated DNS, hosting; billed per mailbox slot, used or not | $3 per slot a month on monthly billing (25 slots: $75 a month, or $60 a month billed yearly); minimum 10 slots; `.com` domains $14 a year; SSL and domain masking $2 per domain a month | 30 a day per mailbox recommended, 100 maximum; 2 to 3 mailboxes per domain | No contract, cancel anytime, no free trial |
| Infraforge | Dedicated sending servers (a sibling product named on the Mailforge page), automated DNS, API | $4 per slot a month billed quarterly; minimum 10 slots; dedicated IP $99 a month each; `.com` $14 a year | Same 30 a day and 2 to 3 per domain guidance | No contract |
| Primeforge | Google Workspace and Microsoft 365 mailboxes on US IPs (sibling product) | $4.50 per slot a month (25 slots: $113 a month monthly, $94 a month yearly); minimum 10 slots; bring your own domains by changing nameservers | Same 30 a day and 2 to 3 per domain guidance | No contract |
| Maildoso | Mailboxes with IP rotation, "self-healing mailboxes", reputation measurement, API; 30-day money-back guarantee | Monthly: 30 mailboxes $75, 300 mailboxes $225, 1,000 mailboxes $499. Legacy quarterly plans work out to 4 mailboxes per domain | Up to 15 emails a day per mailbox | Page does not say which mail platform hosts the mailboxes |

ManyReach ManySenders (section 1) is the sequencer-bundled version of the same idea.

### 6a. Risks to clear before buying

| Risk | Question to put to the vendor in writing | What to do |
|-|-|-|
| You do not hold the tenant | Who is the Google Workspace or Microsoft 365 admin? Do we get admin access? Can the mailboxes move to our own tenant if we leave? | Treat mailboxes you cannot administer as rented. Keep the domains in your own registrar account |
| Domain ownership | Whose name is on the registration? | Register in your company's name, or bring your own domains |
| Shared infrastructure | Which other senders share our IPs or tenant? | Mailforge's own page says its mailboxes sit on a shared IP pool. Seed test before scaling (`email-deliverability`) |
| Cancellation | What happens to the mailboxes, the domains and the warmup history when we cancel? | Export the suppression list and reply history before cancelling |
| Seats priced under the provider's list price | Under whose Google or Microsoft account are the seats licensed? | Google lists Business Starter at $7.00 to $8.40 a user (section 1); vendors sell Google inboxes at $3.30 to $4.50. A vendor-owned account means the vendor's standing with Google or Microsoft decides your mailboxes' fate |
| Higher per-domain density | How many mailboxes per domain, and how many sends per mailbox? | Section 7 |
| Delivery time | How many hours from order to mailboxes connected in our sequencer, for this order size, in writing? | Pages state setup windows (ScaledMail 24 to 72 hours, Hypertide "live in hours") without a guarantee. Never date the launch from a window the vendor has not confirmed; write the fallback build date next to it (`launch-and-monitoring.md` section 4) |

## 7. The high-density Microsoft tenant pattern

Several vendors sell Microsoft mailboxes in blocks of 25 on one domain and keep each mailbox at low volume: ScaledMail's Outlook option (25 mailboxes per domain, up to 10 a day each) and Hypertide's Entra Domains (25 inboxes per domain). The pitch: many mailboxes at a low per-mailbox count look gentle, and the per-mailbox price drops to $1 to $2.

Compared with the standard layout:

| Standard layout | High-density pattern | Result |
|-|-|-|
| 2 to 3 mailboxes per sending domain (Alex Berman, Instantly, Smartlead) | 25 per domain | Outside every operator figure cited here |
| 3 x 30 = 90 sends a day per domain at Instantly's 30 | 25 x 10 = 250 a day | 2.8 times the per-domain load |
| One domain problem pauses 3 mailboxes | One domain problem pauses 25 | Eight times the blast radius |
| Reputation is judged per domain by Google, Spamhaus and DMARC | Same, so 25 mailboxes share one domain's reputation | Low per-mailbox volume does not lower per-domain volume |

**The shared-tenant risk.** Microsoft documents separate outbound spam thresholds for each user and for the organization overall. It also caps external recipients per tenant per day with the Tenant External Recipient Rate Limit, which depends on the tenant's license count, and it states that spam from one customer can affect delivery for other customers (Microsoft Learn, checked 2026-10-13). When many domains, or many customers, sit in one tenant, a single restriction can stop every mailbox in it at once. Hypertide lists "tenant separation" for Entra Domains; get the tenant boundary confirmed in writing for any vendor before counting on it.

**Use.** Keep high-density Microsoft out of core capacity. It can run as a test pod with its own campaign and Microsoft 365 plus Outlook.com seeds in every placement test. Before it starts, the user writes the test length and the pass line for bounces and replies per 1,000 sends against the standard pods; promote it only if it passes.

## 8. DIY or done-for-you: the breakeven

```text
DIY first year  = setup_hours x rate + 12 x admin_hours_month x rate + 12 x mailboxes x seat_price + domains x domain_price
DFY first year  = onboarding_hours x rate + 12 x admin_hours_month_dfy x rate + 12 x vendor_monthly_fee + domains x domain_price
Breakeven rate  = (DFY cash - DIY cash) / (DIY hours - DFY hours)      DIY pays off only at a positive rate above zero
```

Time inputs come from the user: time the first domain (register, redirect, add to the admin console, verify, MX, SPF, DKIM, DMARC, tracking CNAME) and the first mailbox (user, 2-Step Verification, signature, photo, sequencer connection), and use the team's own hourly rate. The table below uses these example inputs: 45 minutes a domain, 10 minutes a mailbox, 15 minutes per domain a month of DIY admin, 2 hours of done-for-you onboarding and 1 hour a month, $50 an hour.

Worked for the 9-domain, 27-mailbox build in `capacity-and-costs.md` (prices checked 2026-10-13):

| Line | DIY Google Workspace Starter, Flexible | DIY Exchange Online Plan 1, annual | Done-for-you Google, Hypertide $3.30 | Done-for-you Google, ScaledMail $3.50 |
|-|-|-|-|-|
| Setup or onboarding | 9 x 0.75 h + 27 x 1/6 h = 11.25 h = $562.50 | $562.50 | 2 h = $100.00 | $100.00 |
| Seats or fees, 12 months | 27 x $8.40 x 12 = $2,721.60 | 27 x $4.00 x 12 = $1,296.00 | 27 x $3.30 x 12 = $1,069.20 | 27 x $3.50 x 12 = $1,134.00 |
| Admin, 12 months | 2.25 h x $50 x 12 = $1,350.00 | $1,350.00 | 1 h x $50 x 12 = $600.00 | $600.00 |
| Domains, own Porkbun account | 9 x $11.08 = $99.72 | $99.72 | $99.72 | $99.72 |
| First-year total | $4,733.82 | $3,308.22 | $1,868.92 | $1,933.72 |

Own tenants or resold mailboxes, stated plainly: resold mailboxes cost less and arrive faster when the vendor delivers; your own tenants cost more and keep the admin console, the DKIM keys, the tenant boundary and the exit with you. At these list prices and example inputs there is no positive breakeven rate: the DIY Google build costs $2,821.32 in cash before any hours, against $1,168.92 for the Hypertide build, so DIY is the dearer path even at $0 an hour. The case for DIY is control: you hold the tenant, the admin console, the DKIM keys and the exit. The price of that control here is $2,864.90 a year ($4,733.82 minus $1,868.92), about $106 per mailbox.

Decision rule:

| Situation | Choose |
|-|-|
| A security review, client contract or investor diligence requires the company to own the mail tenant | DIY |
| A small build, and an in-house admin already runs Workspace or Microsoft 365 | DIY |
| Agency building mailboxes for several clients every month | Done-for-you, after section 6a answers come back in writing, with each client's domains in that client's registrar account |
| The launch date cannot move | DIY in your own tenants, or a vendor only with delivery confirmed in writing and a dated DIY fallback |
| Any build | Seed test 1 domain from the vendor before ordering the rest |

## 9. Tenant size and blast radius

A tenant here means one Google Workspace account or one Microsoft 365 organization. Every mailbox in it shares the admin console, the billing account and, on Microsoft, the organization-level outbound thresholds and the Tenant External Recipient Rate Limit (section 7). A problem at that level stops every mailbox at once.

| Build | One tenant | Tenants of 9 users |
|-|-|-|
| 27 mailboxes (9 domains x 3) | 1 console; one account problem pauses 27 mailboxes | 3 tenants (3 domains each); one problem pauses 9 |
| 63 mailboxes (21 domains x 3) | 1 console; one problem pauses 63 | 7 tenants; one problem pauses 9 |
| Seat price | Same | Same |
| Extra work | None | One more admin login, bill, DKIM setup and 2-Step Verification policy per tenant |

The user sets the tenant size. Spread active and reserve domains across tenants so a tenant problem does not take the reserves with it, and agency clients each get their own. Write the chosen size and its blast radius in the plan.

## 10. Microsoft 365 tenant settings for cold sending, in build order

Create Microsoft tenants first, on day 0, before the domains finish DNS: the quota cut for new tenants runs on tenant age, so every day of age before cold mail helps.

| # | Setting | Where | Value | Why |
|-|-|-|-|-|
| 1 | Paid tenant, never a trial | Microsoft 365 admin center, buy Exchange Online Plan 1 (or Business Basic) | Paid from day 0 | Trial tenants are capped at 500 external recipients a day under MC1454397 (rollout mid-September to end of November 2026) |
| 2 | Tenant age quota | Exchange admin center > Reports > Mail flow > Tenant outbound external recipients | Plan for 10% of the standard quota until day 30, 25% until day 60 | Microsoft's standard quota is 500 x (purchased email licenses ^ 0.7) + 9,500 external recipients a day. An 8-license tenant: 500 x 8^0.7 + 9,500 = 11,644; 10% = 1,164 a day for its first 30 days, 25% = 2,911 until day 60. Warmup mail to outside mailboxes counts toward it |
| 3 | Custom domain added and verified | Admin center > Settings > Domains | Every sending domain; default domain set to one of them | Mail from `*.onmicrosoft.com` is limited to 100 external recipients a day per organization (`550 5.7.236`) |
| 4 | DKIM signing on | Defender portal > Email authentication settings > DKIM, after both CNAMEs resolve | Enabled per domain; rotate to 2048-bit | Microsoft signs custom domains with the tenant's default key until you enable it, which does not align with the From domain |
| 5 | Outbound spam policy for the cold mailboxes | Defender portal > Policies & rules > Threat policies > Anti-spam > Create policy > Outbound (`New-HostedOutboundSpamFilterPolicy`) | External limit 20 an hour (the top of Apollo's 10 to 20 an hour per mailbox), daily limit 50 recipients (Alex Berman's per-inbox ceiling); restriction "until the following day" (the default); automatic forwarding Off | A runaway sequence or a stolen password stops at 50 instead of the 10,000 service default; the limits accept 0 to 10,000. Raise the daily limit if cold cap plus warmup ever needs more |
| 6 | Sequencer connection | Sequencer > add account > Sign in with Microsoft | OAuth | Basic auth for SMTP AUTH is unchanged through December 2026, then off by default for existing tenants and unavailable for tenants created after December 2026 (MC786329). OAuth avoids the cut-over |
| 7 | SMTP AUTH per mailbox, only if a tool cannot use OAuth | Admin center > Users > user > Mail > Manage email apps > Authenticated SMTP | Off unless needed | Security defaults block legacy authentication |
| 8 | MFA | Entra admin center, security defaults or Conditional Access | On for every user | Account takeover is the fastest way to lose a tenant |
| 9 | Seat term | Admin center > Billing | Annual at $4.00 a seat, or a monthly term at a higher price for a test pod | Annual seats cannot be cut before renewal |

## 11. Google Workspace account settings for cold sending

| # | Setting | Where | Value | Why |
|-|-|-|-|-|
| 1 | Paid account, not a trial | Billing | Pay on day 0 | Trial users are capped at 500 messages a day; raised limits can take up to 75 days after the account has paid $100 (Google Workspace sending limits page) |
| 2 | Secondary domains, not domain aliases | Admin console > Account > Domains > Manage domains > Add a domain | Secondary domain per sending domain | An alias gives existing users a second address; a secondary domain gets its own users, so each mailbox has its own identity |
| 3 | Cold email organizational unit | Admin console > Directory > Organizational units | All cold mailboxes in one OU | Policies (2-Step Verification, forwarding) differ from staff mailboxes |
| 4 | DKIM | Admin console > Apps > Google Workspace > Gmail > Authenticate email | 2048-bit key per domain, then Start authentication | The key appears 24 to 72 hours after Gmail is turned on for the domain |
| 5 | 2-Step Verification | Admin console > Security > Authentication | Enforced for the cold OU | Sequencers connect by OAuth, so no app passwords are needed |
| 6 | Seat term | Billing | Flexible ($8.40) until the seat count is settled; Annual ($7.00) after | Annual seats can be removed only at renewal |

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
- ScaledMail, Pricing (checked 2026-10-13): https://scaledmail.com/pricing
- Hypertide, Pricing (checked 2026-10-13): https://www.hypertide.io/pricing
- Mailforge, Pricing (checked 2026-10-13): https://www.mailforge.ai/pricing
- Infraforge, Pricing (checked 2026-10-13): https://www.infraforge.ai/pricing
- Primeforge, Pricing (checked 2026-10-13): https://www.primeforge.ai/pricing
- Maildoso, Pricing (checked 2026-10-13): https://maildoso.ai/pricing
- Microsoft, Outbound spam protection (checked 2026-10-13): https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-protection-about
- Microsoft, Exchange Online limits, Tenant External Recipient Rate Limit (checked 2026-10-13): https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- Microsoft 365 Message Center MC1454397, TERRL quotas for new, trial and education tenants (mirror, checked 2026-10-13): https://mc.merill.net/message/MC1454397
- Microsoft 365 Message Center MC786329, Basic auth for SMTP AUTH (mirror, checked 2026-10-13): https://mc.merill.net/message/MC786329
- Instantly, Email service providers matching (checked 2026-10-13): https://help.instantly.ai/en/articles/7044069-email-service-providers-matching
- Instantly, Account and campaign limits (30 a day per account): https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Instantly, Secondary sending domains (2 to 3 inboxes per domain): https://help.instantly.ai/en/articles/6502027-scale-your-cold-email-campaigns-with-secondary-sending-domains-the-strategy-how-to-implement-it
- Smartlead, Secondary sending domains (2 to 3 addresses per domain): https://helpcenter.smartlead.ai/en/articles/147-all-you-need-to-know-about-secondary-sending-domains-for-cold-email-campaigns
- Apollo, Email sending limits (10 to 20 an hour per mailbox): https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- Alex Berman, TAM strategy breakdown (under 50 a day per inbox, 2 to 3 per domain): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Microsoft, Configure outbound spam policies (checked 2026-10-13): https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-policies-configure
- Google Workspace, Gmail sending limits (trial cap and paid threshold, checked 2026-10-13): https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace
