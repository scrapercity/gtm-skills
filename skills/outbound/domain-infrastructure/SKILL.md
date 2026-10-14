---
name: domain-infrastructure
description: >-
  Plans and specifies the sending infrastructure for cold email: how many
  secondary domains and mailboxes a volume target needs, 2 or 3 per domain,
  Google Workspace and Microsoft 365 split by the measured recipient mix, your
  own tenants or resold inboxes, tenant settings, domain names, the exact SPF,
  DKIM, DMARC (with rua), MX, tracking and Postmaster records, warmup settings,
  dated launch paths including a wide build that meets the requested date,
  monitoring thresholds and a cost estimate. Use when the
  user asks how many domains or inboxes they need, wants to buy sending
  domains, set up DNS for cold email, protect their main domain, choose
  between Google and Microsoft mailboxes or between building and buying
  inboxes, or asks when a new setup can start sending.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.1.0"
  author: ScraperCity
  category: outbound
  tags:
    - domains
    - dns
    - spf
    - dkim
    - dmarc
    - mailboxes
    - google-workspace
    - microsoft-365
    - cold-email-infrastructure
  related_skills:
    - inbox-setup
    - email-deliverability
    - sending-platforms
    - cold-email-strategy
    - outbound-unit-economics
    - cold-email-list
  frameworks:
    - "Google - Email sender guidelines and FAQ (2024, enforcement ramp Nov 2025); Postmaster Tools help"
    - "Yahoo - Sender Hub best practices (2024)"
    - "Microsoft - Outlook requirements for high-volume senders (May 2025); Message Center MC1454397 new-tenant quotas (2026)"
    - "IETF - RFC 7208 SPF, RFC 6376 DKIM, RFC 7489 and RFC 9989 DMARC"
    - "Google Workspace and Microsoft 365 admin documentation (DNS records, sending limits, outbound spam policies)"
    - "Spamhaus - Domain Blocklist listing criteria"
    - "Alex Berman - domain and inbox counts for a starting setup; first cold volume for new domains"
    - "Instantly - per-account limits, warmup settings, ESP matching and secondary domain naming"
    - "Puzzle Inbox - cold email inbox naming conventions (May 2026)"
  shared_references:
    - deliverability-primer.md
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
---

# Domain Infrastructure

## Overview

This skill turns a sending goal ("1,500 cold emails a day, starting in three weeks") into a buildable spec: mailboxes and secondary domains, 2 or 3 per domain, the provider split, whether the team owns its tenants or rents inboxes, the settings in each tenant, the domain names, every DNS record, the first cold send date on two paths, the monitoring thresholds and the monthly cost. A person or an agent can execute it line by line in a registrar and an admin console.

It prevents four mistakes: cold email from the company's main domain; a launch date that new domains cannot meet, or one that rests on a vendor's unconfirmed delivery window; Microsoft tenants created late and then throttled by their age; and a build with no monitoring until replies stop.

## When to Use

- "How many domains and inboxes do I need for X emails a day?"
- "Set up sending domains for cold email" or "buy secondary domains".
- "What DNS records do I need?" or "is my SPF/DKIM/DMARC right?"
- "Google Workspace or Microsoft 365 for outbound?" or "should we buy inboxes from a reseller?"
- "We need to start sending in N weeks. Is that possible?"
- Scaling an existing setup: adding domains for a new market or a new client.

Use a different skill for nearby jobs:

| Job | Skill |
|-|-|
| Per-mailbox setup after the domains exist (names, signatures, warmup settings, sending windows) | `inbox-setup` |
| Running health: incidents, blocklist removal, spam-folder diagnosis | `email-deliverability` |
| Choosing and wiring the sequencer, CSV mapping, webhooks | `sending-platforms` |
| Campaign plan, offer and sequence | `cold-email-strategy` |
| Cost per meeting and whether the volume pays | `outbound-unit-economics` |

## Prerequisites

Collect these before sizing. Mark anything unknown and use the default shown.

| Input | Why | Default if unknown |
|-|-|-|
| Main (primary) domain | Redirect target; must never send cold mail | Required |
| Volume, as the user said it | Drives capacity | Required. "X emails a day" is read as X total sends including follow-ups; state the reading |
| Requested start date | The launch paths are dated against it | "As soon as possible" |
| Steps per sequence | Each step is a send | Required |
| Sending days per month | Monthly volume | Required; 21 on a weekday schedule |
| Mailboxes per domain | Domain count | Required: 2 or 3 after the side-by-side in step 3 |
| Senders: the team members whose names go on the mailboxes | Mailbox addresses | Required; stand-in names are marked ASSUMED |
| Wide-build cap | Per-mailbox volume when the date is worth more than the extra seats (step 11) | Required when the standard path misses the date: a number from Alex Berman's 10 to 20 a day for new domains |
| Reserve share of domains | Reserve count | Required; at least 1 reserve domain |
| Tenant size | Blast radius | Required for builds with more than one tenant's worth of mailboxes |
| Recipient mix: Google vs Microsoft vs other | Provider split | Required: measure it in step 4 |
| Existing sending domains, with registration dates and incidents | Aged domains shorten the ramp; burned ones are not reused | None |
| Sequencer | Tracking CNAME format, warmup | Instantly |
| Budget per month | Caps domain and seat count | None |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Google Email sender guidelines and FAQ (support.google.com/a/answer/81126, /14229414) | All senders need SPF or DKIM, PTR, TLS and a spam rate under 0.3%. Senders of about 5,000+ a day to personal Gmail need SPF and DKIM, aligned DMARC (`p=none` allowed) and one-click unsubscribe. The count is per primary domain, subdomains included, and bulk status never expires. |
| Google Postmaster Tools help (support.google.com/mail/answer/9981691, /14668346) | Each domain is verified with a TXT or CNAME; dashboards cover mail to personal Gmail only and hide low-volume days. |
| Yahoo Sender Hub | Same authentication bar for bulk senders, DMARC must pass, `rua` strongly recommended, unsubscribes honored within 2 days. |
| Microsoft Outlook high-volume sender requirements (enforced 5 May 2025) | Domains sending over 5,000 a day to Outlook.com, Hotmail and Live need SPF, DKIM and DMARC `p=none` or stronger with alignment; failures get `550; 5.7.515`. |
| Microsoft 365 Message Center MC1454397 (rollout mid-September to end of November 2026) and MC786329 | New tenants get 10% of the tenant external recipient quota (500 x licenses^0.7 + 9,500 a day) for 30 days and 25% until day 60; trial tenants 500 a day. Basic auth for SMTP AUTH turns off by default at the end of December 2026. |
| RFC 7208, RFC 6376, RFC 7489 replaced by RFC 9989 and RFC 9990 (May 2026) | One SPF record under 10 lookups; DKIM keys at `selector._domainkey`, 1024-bit minimum; one DMARC record, `rua` for reports, `pct` removed; one wildcard `*._report._dmarc` authorization covers every sending domain. |
| Google Workspace and Microsoft 365 admin docs | Exact MX, SPF, DKIM values; Workspace 2,000 messages per user per day (500 on trial); Exchange Online 10,000 recipients a day, 30 messages a minute; outbound spam policy limits of 0 to 10,000. |
| Spamhaus Domain Blocklist | Unknown reputations start as poor, so domain age at launch is the first risk; spreading volume over ever-changing domains is snowshoeing. Keep domains stable and proportional to volume. |
| Alex Berman (alexberman.com) | A starting setup of 3 to 5 sending domains, 2 to 3 inboxes per domain, under 50 emails per inbox per day, 2 to 4 weeks of warmup (October 2026); new domains start at 10 to 20 emails a day and ramp up over 2 to 4 weeks (cold email templates page); bounces above 2% hurt domain reputation and above 5% are critical (May 2026). |
| Instantly help center | 30 campaign emails per account a day; ready after 2 weeks of warmup and a health score above 90%, 3 weeks for its own AirMail accounts; warmup settings for new accounts: increase 1 a day, daily warmup limit 10, reply rate 30%; 2 to 3 inboxes per domain, no hyphens or numbers in names; ESP Matching sends from the account matching the lead's provider. |
| Puzzle Inbox, cold email inbox naming conventions (Tom Harris, May 18, 2026) | `first.last@` is the most common and most trusted pattern, `first@` looks personal (one per first name per domain), numbers in addresses look like a bot, role addresses (`sales@`, `info@`) are flagged. |
| Growth Engine X (coldoutbound.com) | Backup domains always warming; 1,500 a day of capacity for a 1,000 a day goal. |

Full detail and links: `references/deliverability-primer.md` and `references/framework-notes.md`.

## Workflow

### 1. Lock the main domain out of cold email

Write the primary domain at the top of the plan with the line "never sends cold email". Check it at check.spamhaus.org and confirm it has one DMARC record; if it has none, add `v=DMARC1; p=none; rua=mailto:dmarc@<main domain>` so the sending domains' reports have a home. Its SPF and DKIM stay as they are.

### 2. Read the request: volume and date

Write the reading in the Inputs table. "1,500 emails a day" means 1,500 sends at steady state, so 500 new prospects a day on a 3-step sequence; give the other reading's size in one line ("1,500 first touches a day would need 4,500 sends and 150 mailboxes"). Write the requested start date; step 11 checks it. Day 0 is the plan date: purchases start the day the plan is delivered, and every later date counts from it.

### 3. Size capacity

Formulas and worked tables: `references/capacity-and-costs.md`.

```text
daily_sends        = new_prospects_per_day x steps_per_sequence
active_mailboxes   = ceil(daily_sends / 30)                     Instantly's 30; never above Alex Berman's 50
mailboxes_per_dom  = 2 or 3                                     Alex Berman, Instantly, Smartlead
active_domains     = ceil(active_mailboxes / mailboxes_per_dom)
reserve_domains    = max(1, ceil(active_domains x reserve_share))   user input; Growth Engine X runs 0.5
total_mailboxes    = (active_domains + reserve_domains) x mailboxes_per_dom
wide_mailboxes     = ceil(daily_sends / wide_cap)                  wide_cap from Alex Berman's 10 to 20 for new domains
wide_domains       = ceil(wide_mailboxes / mailboxes_per_dom)       no reserve: every mailbox can rise to 30 to cover a paused domain
```

Show both layouts in the Capacity Plan and let the user choose. At 1,500 a day with a 20% reserve: 3 per domain needs 21 domains and 63 mailboxes; 2 per domain needs 30 domains and 60 mailboxes, costs $16.89 a month less, and one domain incident pauses 4% of volume instead of 6%, for 9 more domains to set up and renew (section 2a).

### 4. Measure the recipient mix (required)

| Method | How | Cost |
|-|-|-|
| Validation sample | 500 addresses through ScraperCity's Email Validator; count the mail provider and security gateway columns (ScraperCity Implementation, Step B) | $3.60 |
| MX lookup | Company domains from a 500-row sample: `dig +short MX <domain>`. `google.com` or `googlemail.com` = Google; `mail.protection.outlook.com` = Microsoft 365 | Free, slower |

Write the shares (Google %, Microsoft %, other %) with the sample size as the source.

### 5. Split providers by the measured mix from day one

```text
microsoft_active_domains  = floor(active_domains x microsoft_share)     0 means Google Workspace only
microsoft_reserve_domains = round(reserve_domains x microsoft_share)
google domains            = the rest
```

Instantly's ESP Matching sends each lead from an account on the lead's own provider and asks for accounts on more than one provider; Instantly publishes no data on the gain, so the plan compares replies per 1,000 sends by provider. Two providers also keep one provider's account problem from stopping every mailbox. A Microsoft pod added after launch needs its own 21 days of warmup and 15 sending days of ramp, about 6 weeks. When a large share of the sample sits behind one security gateway, a seed address behind it joins every placement test. Decision rules: `references/mailbox-provider-matrix.md` section 2.

### 6. Choose the build path: your own tenants or resold inboxes

Put both in the option table with monthly cost, then state the trade-off in one line:

- **Own tenants (DIY):** you hold the admin console, the DKIM keys, the tenant boundary and the exit. Seats at list price ($8.40 Google Starter Flexible, $4.00 Exchange Online Plan 1 annual, checked 2026-10-13) plus the team's own setup time per domain.
- **Resold inboxes:** $3.30 to $4.50 a Google inbox (Hypertide, ScaledMail, Primeforge pages, 2026-10-13), built in hours to days. The vendor's account holds the seats, so its standing with Google or Microsoft decides yours, and other senders may share the tenant or IPs.

Rules: DIY when the user says the company must own the tenant, or when the launch date cannot move. A vendor's delivery window goes in the plan only after the vendor confirms it in writing for this order, with a DIY fallback next to it, dated in the Launch Checklist. Breakeven and vendor questions: `references/mailbox-provider-matrix.md` sections 6a and 8.

Tenant size is the user's input; agency clients each get their own, and reserves are spread across tenants. Write how many mailboxes one tenant problem would pause. Tenant ownership is not an Inputs row; it only changes the build path when the user raises it.

### 7. Configure the tenants, Microsoft first

Create every Microsoft 365 tenant on day 0: its quota is cut by age (10% for 30 days, 25% to day 60), so age gained before cold mail is free. Never send from a trial (500 a day on either provider). Write the settings into the plan's Tenant Settings table:

| Provider | Settings the plan names |
|-|-|
| Microsoft 365 | Paid tenant, custom domains verified (never `onmicrosoft.com`), DKIM enabled per domain, an outbound spam policy for the cold mailboxes (20 external recipients an hour, the top of Apollo's 10 to 20; 50 a day, Alex Berman's per-inbox ceiling; forwarding off), OAuth connection to the sequencer, MFA, the tenant's quota at its age with the day it rises |
| Google Workspace | Paid account, secondary domains (not aliases), a cold email organizational unit, 2048-bit DKIM per domain, 2-Step Verification enforced, Flexible seats |

Paths and reasons: `references/mailbox-provider-matrix.md` sections 10 and 11.

### 8. Name the domains

1. `.com` or the market's country TLD; Instantly reports weaker reply rates on `.biz` and `.online`.
2. The brand stays recognizable: `getacme.com`, `tryacme.com`, `acmehq.com`, `meetacme.com` (Instantly's own examples follow this pattern).
3. No hyphens and no digits (Instantly and Smartlead).
4. One brand per domain set; an agency builds a separate set per client.
5. Register them all at once in the company's own registrar account, privacy on, auto-renew on, and keep them for the long run (Spamhaus treats ever-changing domains as snowshoeing). Details: `references/dns-records-checklist.md` section 9.
6. Mailbox addresses: `first@` and `first.last@` only, from real team members' names, two different people on each domain (Puzzle Inbox). No truncated or initial-only forms (`jordanl@`, `samp@`), no digits, no role addresses. Every `first@` name also appears somewhere as `first.last@`, so each address reads as one person.

### 9. Pick the registrar and the redirect

| Registrar | Why pick it | Watch |
|-|-|-|
| Cloudflare Registrar | At-cost pricing with no markup (Cloudflare page; a price tracker showed $10.46 for `.com` on 2026-10-13, confirm at checkout), Redirect Rules, a DNS API with batch writes | Cloudflare nameservers required; tracking CNAMEs DNS-only |
| Porkbun | $11.08 a year for `.com` registration and renewal, free WHOIS privacy and URL forwarding (porkbun.com, 2026-10-13), a JSON DNS API | API access is opt-in in account settings |
| Namecheap, GoDaddy, Squarespace | Fine if the team already uses one | Price renewals before buying the set |

Every sending domain 301-redirects to the main site. Record the nameservers, DNSSEC state and renewal date once for the domain set (`references/dns-records-checklist.md` section 12).

### 10. Write the records once, as a template

One record block per provider, filled in for one real domain, with an "Applies to" line. Rows: verification TXT, MX, SPF, DKIM, DMARC with `rua`, Postmaster Tools verification TXT, tracking CNAME (Instantly: exactly `inst` to `prox.itrackly.com`), redirect; Microsoft adds `autodiscover` and two DKIM CNAMEs. When `rua` points at the main domain, publish one `*._report._dmarc.<main domain>` TXT `v=DMARC1`. For a large set, write records by API with a dry run first (Porkbun `"dryRun":true` returns `wouldSucceed` without writing), TTL 600 while building, and put the script itself in the plan: the loop over the domain file that writes every record of each provider block, filled in for this build (`references/dns-records-checklist.md` section 13). A described script that the reader has to write is not a deliverable.

### 11. Date the launch: three paths and the warmup settings

Day 0 is the plan date. Warmup starts the day the header test passes (Google's DKIM key appears 24 to 72 hours after Gmail is on, so usually day 2). Rules and the worked calendar: `references/launch-and-monitoring.md` sections 2 to 4.

Warmup settings, one value each, for every mailbox (Instantly's suggested values for new accounts): increase 1 a day, daily warmup limit 10, reply rate 30%, left on at those values while cold mail sends. Campaign daily limit 0 until the first cold day. The tenant quota check uses cold cap + 10.

Cold ramp: 10 a mailbox for the first 5 sending days, 20 for the next 5, then the cap (30) from sending day 11. It starts at the low end of Alex Berman's 10 to 20 a day for new domains and reaches the cap in 2 weeks, the short end of his 2 to 4. Every mailbox, reserves included, sends during the ramp; reserves go back to warmup only once the active mailboxes reach the cap. Each raise waits for the weekly review to pass (step 12).

| Path | Warmup | Mailboxes | Target reached |
|-|-|-|-|
| Standard | 21 days (Instantly's warmup for its own new AirMail accounts, inside Alex Berman's 2 to 4 weeks) | The sized build | Sending day 11 of the ramp |
| Soft start | 14 days, never shorter (Instantly's minimum); only mailboxes with an Instantly health score above 90% and a send file of `valid` addresses | The sized build | 7 calendar days earlier |
| Wide build | 21 days, or 14 on the soft start | `wide_mailboxes` from step 3 | Its first cold day, at `wide_cap` with no ramp |

Compare each path with the requested date and write the slip in days. When the standard path reaches the target after the requested date, the wide build row is required, with its mailbox count, and the Cost Estimate prices it; the user chooses on day 0. Never write that no path meets the date when the wide build meets it. Never close a gap by skipping warmup or by sending from the main domain. A Microsoft tenant under 31 days old runs on 10% of its quota: check mailboxes x (cold cap + 10) per tenant on the first cold day.

### 12. Set up monitoring before the first warmup email

Every sending domain verified in Google Postmaster Tools; Microsoft SNDS left out because it covers IPs you control and Workspace and Microsoft 365 send from shared provider IPs; each Microsoft tenant's external recipient report watched against its age quota; Spamhaus checks and seed tests at Gmail, Workspace, Outlook.com and Microsoft 365 on a fixed review day. Thresholds: spam rate below Google's 0.1%, stop at 0.3%; bounces act at 2% and stop at 5% (Alex Berman, Instantly's auto-pause); health score above Instantly's 90%. Table: `references/launch-and-monitoring.md` section 6.

### 13. Verify, hand off, name the triggers

Per domain: `dig` the records, send from each mailbox to Gmail and Outlook.com test addresses, read `spf=pass`, `dkim=pass header.d=<domain>` and `dmarc=pass`. Hand the mailboxes on for roster setup (display names, signatures); the warmup settings are already in the plan. Write the scaling triggers: a reserve promoted, a higher daily target, a new market or client, the replies per 1,000 sends gap between providers (`references/capacity-and-costs.md` section 8).

## ScraperCity Implementation

ScraperCity does not sell domains or mailboxes. It supplies the one number the provider split depends on: which mail provider the prospects use.

**Step A. Check the wallet.** `check_wallet()`

**Step B. Measure the recipient provider mix.** Take 500 addresses from the user's target list (or 500 Lead Database rows on the Growth plan, which count against the 100,000 a day allowance with no per-row charge) and validate them:

```text
validate_emails(emails=[...500 addresses...])     # 500 x $0.0072 = $3.60
check_run_status(runId) -> download_results(runId)
```

Count `sc_mx_provider` (Google, Microsoft, other) and `sc_mx_security_gateway`. In the plan, write the result in plain words: "Email validation sample of 500: 54.2% Google, 38.6% Microsoft".

**Worked cost estimate** (vendor prices checked 2026-10-13), 1,500 sends a day, 3 steps, 38.6% Microsoft recipients:

| Item | Numbers | Cost |
|-|-|-|
| Steady-state sends a day | 500 x 3 = 1,500 | |
| Active mailboxes, layout | 1,500 / 30 = 50; 2 per domain = 25 active domains; 20% reserve share chosen = 5 reserve | |
| Provider split | Microsoft floor(25 x 0.386) = 9 active + 2 reserve; Google 16 + 3 | |
| Google Workspace Business Starter, Flexible | 19 domains x 2 = 38 x $8.40 | $319.20 a month |
| Exchange Online Plan 1, annual | 11 domains x 2 = 22 x $4.00 | $88.00 a month |
| Domains, Porkbun `.com` | 30 x $11.08 = $332.40 a year | $27.70 a month |
| Instantly Hypergrowth | flat, 125,000 emails a month | $97.00 a month |
| Total | | $531.90 a month |
| Provider-mix sample, outside the total | 500 x $0.0072 | $3.60 once |

Show this table to the user before buying anything. The plan's Total covers mailboxes, domains and the sequencer only; validation of the sending list is one line under it, marked as outside the total.

## Output Format

One Markdown document following `templates/output-template.md`. The top line carries the prepared date (Day 0) and the price check date; when any value is a stand-in, one more sentence says values marked ASSUMED are replaced at the first checklist row. Nothing else comes before the Summary, and no disclaimer about what was not run appears anywhere else.

1. **Summary**, at most 160 words, answer first: which path meets the requested date and the slip in days for the others (no calendar dates here), domain and mailbox counts, provider split, build path, monthly total and the wide build's extra cost, and the other volume reading in one clause.
2. **Inputs**: only the template's rows. The requested date lives in the Launch Timeline and the recipient mix in the Provider Decision. No market size, list runway or tenant-ownership rows.
3. **Capacity Plan**: every formula result, the 2-versus-3 layout row and the wide build row. No list runway or cost per 1,000 sends.
4. **Mailbox Provider Decision**: the recipient mix with its source; the option table with a monthly cost per option (Google only, Microsoft only, the mix, resold inboxes); the decision; the build path in one line; tenants and blast radius.
5. **Sending Domains and Mailboxes**: one row per domain with role, provider and tenant, and every `first@` or `first.last@` address. Shared facts (registrar, redirect, nameservers, DNSSEC, renewal date) appear once, in the "All domains:" line.
6. **Tenant Settings**: one table, one row per setting per provider in use.
7. **DNS Record Template**: one block per provider filled in for one named domain, an "Applies to" line by count, the Main Domain Changes line, and, when records go in by API, the script itself.
8. **Launch Timeline**: the Requested line, the Warmup settings line (single values), the ramp line, the Standard, Soft start and (when the standard path misses the date) Wide build rows, and the recommendation.
9. **Monitoring**: setup line and thresholds table.
10. **Cost Estimate**: mailboxes, domains and sequencer rows with a Total row; one line with the wide build's total; one line for costs outside the infrastructure (list validation), marked as outside the total. Lead data plans, cost per 1,000 sends and contact-limit notes stay out.
11. **Launch Risks and Scaling Triggers**: domain age in one sentence and blast radius in one sentence, no dates; the triggers table.
12. **Launch Checklist** with owners and dates; Day 0 rows carry the plan date.
13. **Sources**: one line per vendor or source whose number the plan uses, with its URL.

Each fact appears once. Calendar dates appear only in the top line, the "All domains:" line, Tenant Settings, the Launch Timeline, the Launch Checklist and Sources. No other sections (no assumptions list, frameworks, quality checklist). Sources are named once, without commentary on who said what. No repo file paths, section numbers, skill names or agent tool ids; say what was checked in plain words. The domain list appears once. One TTL value throughout.

## Quality Check

- [ ] The main domain appears only as a redirect target, in `rua` addresses and in the Main Domain Changes line.
- [ ] The volume reading is stated (total sends or first touches) with the other reading's mailbox count.
- [ ] Recipient mix measured before the provider decision; the provider split follows the measured Microsoft share from day one.
- [ ] The option table carries a monthly cost per option, including resold inboxes, and the own-tenant trade-off is stated.
- [ ] No date depends on a vendor delivery window that is not confirmed in writing; a fallback is named.
- [ ] Capacity Plan shows the 2-per-domain and 3-per-domain layouts and the wide build; core domains carry 3 mailboxes or fewer.
- [ ] Cap per mailbox is 30 (Instantly) unless the user set another, never above 50 (Alex Berman).
- [ ] Every Microsoft tenant is paid, created on day 0, and its age quota and outbound spam policy are in Tenant Settings.
- [ ] Domain names have no hyphens or digits; addresses are `first@` or `first.last@` with two people per domain.
- [ ] Every domain row has its addresses; nameservers, DNSSEC and a renewal date after the plan date are stated once for the set.
- [ ] Record template per provider with MX, SPF (one row, under 10 lookups), DKIM, DMARC with `rua=mailto:` and a Postmaster verification row; Instantly tracking is `inst` to `prox.itrackly.com`; the API script is written out when records go in by API.
- [ ] One wildcard `*._report._dmarc` record on the main domain when `rua` lives there.
- [ ] Launch Timeline has the warmup settings, the ramp, the standard and soft-start rows and, when the standard path misses the date, the wide build row; slips in days.
- [ ] Day 0 is the plan date: the first checklist row is dated the prepared date.
- [ ] Monitoring has a thresholds table, Postmaster Tools on every domain, and the SNDS note.
- [ ] Cost total covers mailboxes, domains and sequencer only, with the wide build's total on one line.
- [ ] Sources section lists a URL for every vendor price, limit and rule used.
- [ ] `python3 scripts/check-output.py plan.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Cold email from the main domain or a subdomain of it | Complaints hit invoices and customer mail; Google counts subdomains toward the primary domain | Separate registered domains |
| Promising full volume on day 21 from domains bought today | Unknown domains start at a poor reputation (Spamhaus); the ramp needs 10 more sending days to reach 30 | Dated paths with the slip in days |
| Saying no path meets the requested date | More mailboxes at Alex Berman's 10 to 20 a day reach the target on the first cold day | A wide build row with its mailbox count and cost |
| Starting the cold ramp at 2 a mailbox after 21 days of warmup | Full volume lands 3 weeks after the first send | Start at 10 a mailbox, Alex Berman's low end, every mailbox including reserves |
| Truncated addresses (`jordanl@`, `samp@`) | They read as generated, not as a person | `first@` and `first.last@` only |
| Lead data, list runway or cost per 1,000 sends in an infrastructure plan | Off the question asked; the total stops matching the build | Infrastructure and sequencer in the total, anything else one line below it |
| Launch date resting on a reseller's "24 to 72 hours" | A window on a pricing page is not a commitment | Confirmed in writing, with a dated DIY fallback |
| Microsoft tenant created the week cold mail starts | Under 31 days old it gets 10% of its external recipient quota, warmup included | Create tenants on day 0; check the quota report before each ramp step |
| Sending from a trial tenant or trial Workspace | 500 a day on either provider | Pay on day 0 |
| Registering every domain in SNDS | SNDS covers IPs you control; Workspace and Microsoft 365 IPs are shared | Postmaster Tools on every domain, seed tests for Microsoft |
| Microsoft pod "after week 4" | Its own 21-day warmup and 15-day ramp push the comparison out about 6 weeks | Split by the measured mix from day one |
| Hyphenated or numbered names (`acme-team.com`, `acme2.com`) | Instantly and Smartlead both say to avoid hyphens and numbers | Brand plus one short word |
| Two SPF records after adding a sequencer | RFC 7208 `permerror`; SPF fails everywhere | Merge into one |
| DMARC without `rua`, or `rua` to another domain with no authorization | No reports, or reports dropped | `rua` on day one; one wildcard `*._report._dmarc` record |
| A 400-row DNS sheet identical except for the domain | Reviewers miss the one wrong row | One template per provider; API loop for a large set |
| Tracking CNAME on an undocumented host or proxied | Verification fails | Sequencer's documented host, DNS-only |
| Buying 30 domains for a 4,000-row market | Idle seats, domains aging without history | Ask the user how many prospects the list holds before sizing; `references/capacity-and-costs.md` section 6 |
| Annual seats for an unproven build | Seats removable only at renewal | Google Flexible; Microsoft annual only for the pod size you will keep |
| 25-per-domain Microsoft mailboxes as core capacity | One domain or tenant problem pauses 25 | Test pod only, judged against the standard pods |
| Changing nameservers with DNSSEC on | Validating resolvers return SERVFAIL, mail stops | DNSSEC off, wait out the DS TTL, move, re-enable |
| Untracked renewal dates | An expired domain loses DNS mid-sequence | Renewal date in the plan, auto-renew on, card checked at the first renewal reminder |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Which source backs which rule, where sources differ, routing table |
| `references/capacity-and-costs.md` | Capacity formulas, 2 versus 3 per domain, worked tables, cost lines, ramp, scaling and retiring triggers |
| `references/mailbox-provider-matrix.md` | Google vs Microsoft vs others, prices, decision rules, resold inbox vendors and risks, breakeven, tenant size, Microsoft 365 and Workspace tenant settings |
| `references/launch-and-monitoring.md` | Why new builds wait, standard and soft-start paths, the honest-date formula, vendor lead times, monitoring setup and thresholds |
| `references/dns-records-checklist.md` | Exact record values, Postmaster verification, tracking, redirects, BIMI, naming rules, verification commands, inventory rules, bulk DNS by API |
| `references/deliverability-primer.md` | Shared: authentication, provider rules, thresholds |
| `references/list-quality-standard.md` | Shared: validation buckets for the provider-mix sample |
| `references/scrapercity-catalog.md` | Shared: tool ids and prices |
| `references/scrapercity-platform.md` | Shared: plans and database allowances |
| `templates/output-template.md` | The blank plan to fill |
| `examples/worked-example.md` | Illustrative example: 1,500 sends a day in three weeks, Google and Microsoft from day one |
| `scripts/check-output.py` | Run on the finished plan before delivery |

## Related Skills

- `inbox-setup` takes the mailboxes from this plan and sets names, signatures, warmup and caps.
- `email-deliverability` runs incidents once the domains send.
- `sending-platforms` connects the mailboxes to a sequencer and maps ScraperCity CSVs.
- `cold-email-strategy` sets the volume target this plan sizes.
- `outbound-unit-economics` checks the infrastructure cost against meetings booked.
- `cold-email-list` builds the validated list the domains will send to.
