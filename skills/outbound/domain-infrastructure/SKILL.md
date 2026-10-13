---
name: domain-infrastructure
description: >-
  Plans and specifies the sending infrastructure for cold email: how many
  secondary domains and mailboxes a volume target needs, what to name them,
  where to register them, how they redirect to the main site, the exact SPF,
  DKIM, DMARC (with rua), MX, tracking-domain and optional BIMI records, and
  whether to run Google Workspace, Microsoft 365 or another mailbox provider.
  Produces a capacity table, a records checklist and a cost estimate. Use when
  the user asks how many domains or inboxes they need, wants to buy sending
  domains, set up DNS for cold email, protect their main domain, or choose
  between Google and Microsoft mailboxes.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [domains, dns, spf, dkim, dmarc, mailboxes, google-workspace, microsoft-365, cold-email-infrastructure]
  related_skills: [inbox-setup, email-deliverability, sending-platforms, cold-email-strategy, outbound-unit-economics, cold-email-list]
  frameworks:
    - "Google - Email sender guidelines and FAQ (2024, enforcement ramp Nov 2025)"
    - "Yahoo - Sender Hub best practices (2024)"
    - "Microsoft - Outlook requirements for high-volume senders (May 2025)"
    - "IETF - RFC 7208 SPF, RFC 6376 DKIM, RFC 7489 and RFC 9989 DMARC"
    - "Google Workspace and Microsoft 365 admin documentation (DNS records, sending limits)"
    - "Spamhaus - Domain Blocklist listing criteria"
    - "Alex Berman - domain and inbox counts for a starting setup"
  shared_references: [deliverability-primer.md, scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md]
---

# Domain Infrastructure

## Overview

This skill turns a sending goal ("we want to email 200 new prospects a day") into a buildable spec: the number of mailboxes and secondary domains, the domain names, the registrar, the redirect to the main site, every DNS record with its exact host and value, the mailbox provider, and the monthly cost. The output is a plan a person or an agent can execute line by line in a registrar and an admin console.

The mistake it prevents is sending cold email from the company's main domain, or from a pile of hastily bought domains with missing DMARC, a broken SPF record and no `rua` reports. A complaint spike on the main domain hits invoices, password resets and the CEO's inbox at once. A domain missing DMARC fails the Google, Yahoo and Microsoft bulk sender rules on day one.

## When to Use

- "How many domains and inboxes do I need for X emails a day?"
- "Set up sending domains for cold email" or "buy secondary domains".
- "What DNS records do I need?" or "is my SPF/DKIM/DMARC right?"
- "Google Workspace or Microsoft 365 for outbound?"
- "Should I send cold email from our main domain?" (no, and this skill shows the alternative)
- Scaling an existing setup: adding domains for a new market or a new client.

Use a different skill for nearby jobs:

| Job | Skill |
|-|-|
| Per-mailbox setup after the domains exist (names, signatures, warmup ramp, sending windows) | `inbox-setup` |
| Running health: bounce and complaint monitoring, blocklists, incidents | `email-deliverability` |
| Choosing and wiring the sequencer, CSV mapping, webhooks | `sending-platforms` |
| Campaign plan, offer and sequence | `cold-email-strategy` |
| Cost per meeting and whether the volume pays | `outbound-unit-economics` |

## Prerequisites

Collect these before sizing. Mark anything unknown and use the default shown.

| Input | Why | Default if unknown |
|-|-|-|
| Main (primary) domain | Redirect target; must never send cold mail | Required |
| New prospects to contact per sending day | Drives capacity | Required |
| Steps per sequence | Each step is a send | 3 |
| Sending days per month | Monthly volume | 21 (weekdays) |
| Recipient mix: Google vs Microsoft vs other | Mailbox provider choice | Measure with a 500-address validation sample (below) |
| Sequencer | Tracking CNAME format, mailbox limits | Instantly |
| DNS host access | Who adds records | Registrar DNS |
| Budget per month | Caps domain and seat count | None |

## Authoritative Foundations

| Source | Principle it contributes |
|-|-|
| Google Email sender guidelines and FAQ (support.google.com/a/answer/81126, /14229414) | All senders need SPF or DKIM, PTR, TLS and a spam rate under 0.3%. Senders of about 5,000+ a day to personal Gmail need SPF and DKIM, DMARC (`p=none` allowed) aligned with the From domain, and one-click unsubscribe. The 5,000 count is per primary domain, subdomains included, and bulk status never expires. |
| Yahoo Sender Hub | Same authentication bar for bulk senders, DMARC must pass, `rua` strongly recommended, unsubscribes honored within 2 days. |
| Microsoft Outlook high-volume sender requirements (announced April 2025, enforced 5 May 2025) | Domains sending over 5,000 a day to Outlook.com, Hotmail and Live need SPF, DKIM and DMARC `p=none` or stronger with alignment; failures get `550; 5.7.515`. |
| RFC 7208 (SPF) | One SPF record per domain, at most 10 DNS-querying terms or the result is `permerror`. |
| RFC 6376 (DKIM) | Keys at `selector._domainkey`; signers use at least 1024-bit RSA. |
| RFC 7489, replaced by RFC 9989 (May 2026) | One DMARC record at `_dmarc`; relaxed alignment by default; no aggregate reports without `rua`; `pct` removed in RFC 9989. |
| Google Workspace and Microsoft 365 admin docs | Exact MX, SPF, DKIM values; Workspace 2,000 messages per user per day (500 on trial); Exchange Online 10,000 recipients a day and 30 messages a minute. |
| Spamhaus Domain Blocklist | New domains start with a poor reputation by default; rapidly rotating many domains is treated as snowshoe spam. Keep the domain count proportional and the domains stable. |
| Alex Berman (alexberman.com) | A starting setup of 3 to 5 sending domains, 2 to 3 inboxes per domain, under 50 emails per inbox per day, 2 to 4 weeks of warmup. |

Full detail and links: `references/deliverability-primer.md`.

## Workflow

### 1. Lock the main domain out of cold email

Write the primary domain at the top of the plan with the line "never sends cold email". Its SPF, DKIM and DMARC stay as they are. If the main domain has no DMARC record, add `v=DMARC1; p=none; rua=mailto:dmarc@<main domain>` so the sending domains' reports have a home.

### 2. Size capacity from the volume target

Use the house formulas (worked table in `references/capacity-and-costs.md`):

```text
daily_sends        = new_prospects_per_day x steps_per_sequence   (steady state, follow-ups included)
active_mailboxes   = ceil(daily_sends / cap_per_mailbox)          cap = 30, never above 50
active_domains     = ceil(active_mailboxes / mailboxes_per_domain) mailboxes_per_domain = 3 (Google) or 2 to 3
reserve_domains    = max(1, ceil(active_domains x 0.2))           warmed spares, same setup
total_mailboxes    = (active_domains + reserve_domains) x mailboxes_per_domain
```

Steady state means every sequence step is running. In week one only step 1 sends, so the full capacity is needed from the third week of a 3-step sequence onward.

Check each domain stays far below Google's 5,000 per day bulk line: at 3 mailboxes x 30 sends, a domain sends 90 a day.

### 3. Choose the mailbox provider

Run the matrix in `references/mailbox-provider-matrix.md`. Default rules:

- Recipients mostly on Google (per a validation sample's `sc_mx_provider`): Google Workspace Business Starter.
- Recipients mostly on Microsoft 365 or behind a Microsoft gateway: test a split, half Microsoft 365 Exchange Online Plan 1, half Google. Matching sender and recipient provider is an operator belief, not a provider rule; treat it as a hypothesis and compare reply rates per provider after 2 weeks.
- Agencies needing dozens of domains fast, or senders above roughly 2,000 sends a day: consider a sequencer's bundled mailboxes or private IPs (ManyReach ManySenders, EmailBison dedicated IPs) and read `sending-platforms`.

### 4. Name the domains

Rules (house standard, details in `references/dns-records-checklist.md`):

1. `.com` first; the brand stays recognizable: `getacme.com`, `tryacme.com`, `acmehq.com`, `meetacme.com`, `acme-team.com`.
2. No misspellings of other brands, no words like "mail", "promo", "outreach" or "deals" in the name.
3. One brand per domain set. An agency builds a separate set per client.
4. Register them all at once in one registrar account, privacy on, auto-renew on.
5. Keep domains for the long run. Replacing burned domains every month is the snowshoe pattern Spamhaus lists.

### 5. Pick the registrar and the redirect

| Registrar | Why pick it | Watch |
|-|-|-|
| Cloudflare Registrar | Registry price with no markup, free WHOIS redaction, fast DNS, Redirect Rules | Domains must use Cloudflare nameservers; a redirect rule needs a proxied DNS record; tracking CNAMEs must be DNS-only (gray cloud) |
| Porkbun | $11.08 a year for `.com` (registration and renewal, checked 2026-10-12), free WHOIS privacy and free URL forwarding listed | Use its URL forwarding for the redirect |
| Namecheap, GoDaddy, Squarespace | Fine if the team already uses one | Price renewals before buying 10+ domains |

Every sending domain redirects with a 301 to the main site's homepage. A person who types `getacme.com` should land on `acme.com`.

### 6. Write every DNS record

Fill the records table per domain from `references/dns-records-checklist.md`: MX, SPF, DKIM, DMARC with `rua`, provider verification TXT, tracking CNAME, redirect. BIMI is optional and needs DMARC at `quarantine` or `reject`, a trademarked logo and a VMC certificate, so skip it for cold domains unless the brand already has a VMC.

### 7. Verify, then hand off

For each domain: look up the records with `dig` or the admin console's check, send one message from each mailbox to a Gmail and an Outlook.com test address, and read the headers for `spf=pass`, `dkim=pass header.d=<domain>` and `dmarc=pass`. Then hand the mailboxes to `inbox-setup` for warmup. No cold send before day 15.

## ScraperCity Implementation

ScraperCity does not sell domains or mailboxes. It supplies the two numbers this plan depends on: how many prospects the market holds (so capacity is not overbuilt) and which mail provider those prospects use.

**Step A. Check the wallet.**

```text
check_wallet()
```

**Step B. Size the market before buying domains.** On the Growth plan ($149/mo) and up, a Lead Database query returns `pagination.total` without pulling every row:

```text
query_lead_database(title="VP Sales, Head of Sales", country=["United States"],
                    minEmployees=50, maxEmployees=200, keywords=["saas"], hasEmail=true, limit=1)
```

If `total` is 9,000 and the plan contacts 200 new prospects a day, the market lasts 45 sending days. Size infrastructure to the list you have, not to an ambition.

**Step C. Measure the recipient provider mix.** Pull 500 sample addresses (Lead Database rows count against the 100,000 a day allowance, no per-row charge) and validate them:

```text
validate_emails(emails=[...500 addresses...])     # 500 x $0.0072 = $3.60
check_run_status(runId) -> download_results(runId)
```

Count `sc_mx_provider` values (Google, Microsoft, other) and `sc_mx_security_gateway` values. A sample that comes back 62% Google, 31% Microsoft and 7% other supports a Google-first build with a Microsoft test pod.

**Worked cost estimate** (catalog and vendor prices, checked 2026-10-12), target 200 new prospects a day, 3 steps:

| Item | Numbers | Cost |
|-|-|-|
| Steady-state sends a day | 200 x 3 = 600 | |
| Active mailboxes | 600 / 30 = 20 | |
| Active domains | ceil(20 / 3) = 7 | |
| Reserve domains | max(1, ceil(7 x 0.2)) = 2 | |
| Total mailboxes | 9 x 3 = 27 | |
| Domains, Porkbun `.com` | 9 x $11.08 | $99.72 a year |
| Google Workspace Business Starter, Flexible | 27 x $8.40 | $226.80 a month |
| Provider-mix sample | 500 x $0.0072 | $3.60 once |
| Monthly list validation | 200 x 21 = 4,200 new prospects x $0.0072 | $30.24 a month |
| ScraperCity Growth plan (Lead Database) | flat | $149 a month |

Infrastructure alone: $226.80 a month plus $8.31 a month of domain cost ($99.72 / 12). Show this table to the user before buying anything.

## Output Format

One Markdown document following `templates/output-template.md`:

1. Summary: volume target, mailbox and domain counts, provider, monthly cost.
2. Inputs table.
3. Capacity plan table with every formula result.
4. Mailbox provider decision with the reason.
5. Sending domains table: domain, registrar, redirect target, provider, mailboxes, role (active or reserve).
6. DNS records table: one row per record per domain, exact host and value.
7. Cost estimate table.
8. Launch checklist with owners and dates.

## Quality Check

- [ ] The main domain appears only as a redirect target and in `rua` addresses, never as a sending domain.
- [ ] Cap per mailbox is 50 or less; the plan uses 30 unless the user has a 14-day clean record.
- [ ] Every sending domain has MX, SPF, DKIM and DMARC rows; every DMARC value contains `rua=mailto:`.
- [ ] Exactly one SPF record per domain, under 10 DNS-querying terms.
- [ ] Every domain redirects (301) to the main site.
- [ ] Each domain's daily volume is under 300, far below the 5,000 bulk line.
- [ ] Reserve domains exist (at least 1).
- [ ] Cost table has dollar figures from current vendor pages with the check date.
- [ ] `python3 scripts/check-output.py plan.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Cold email from the main domain | A complaint spike hurts invoices and customer mail too; Google counts subdomains toward the same primary domain | Separate secondary domains |
| Cold email from a subdomain of the main domain (`go.acme.com`) | Same organizational domain: DMARC policy, Gmail bulk counts and Spamhaus DBL listings apply to the parent | Use separate registered domains |
| Two SPF records after adding a sequencer | RFC 7208 gives `permerror`; SPF fails everywhere | Merge into one record |
| DMARC without `rua` | No reports, so alignment failures go unseen; Yahoo strongly recommends `rua` | Add `rua=mailto:` on day one |
| `rua` pointing to another domain with no authorization record | Receivers drop the reports | Publish `<sendingdomain>._report._dmarc.<reportdomain>` TXT `v=DMARC1`, or use a DMARC report service address |
| Tracking CNAME proxied through Cloudflare (orange cloud) | Verification fails | Set DNS-only |
| Buying 30 domains for a 4,000-row market | Idle seats cost money and domains age without history | Size with Step B first |
| Annual Workspace plan for cold seats | Users can be removed only at renewal on the annual plan | Flexible plan until the setup proves itself |
| Microsoft 365 sending from the `onmicrosoft.com` domain | Limited to 100 external recipients a day | Add and verify the custom domain first |
| Lookalike names (`acrne.com` for `acme.com`) | Reads as phishing to filters and people | Brand prefix or suffix only |

## Execution Artifacts

| File | When to open it |
|-|-|
| `references/framework-notes.md` | Which source backs which rule, and which file to open for which question |
| `references/dns-records-checklist.md` | Exact record values for Google Workspace and Microsoft 365, tracking CNAMEs, redirects, BIMI, naming rules, verification commands |
| `references/mailbox-provider-matrix.md` | Google vs Microsoft vs other providers, limits, prices, decision rules |
| `references/capacity-and-costs.md` | The capacity formulas, a worked table from 50 to 1,000 prospects a day, cost lines |
| `references/deliverability-primer.md` | Shared: authentication, provider rules, thresholds |
| `references/list-quality-standard.md` | Shared: validation buckets for the provider-mix sample |
| `references/scrapercity-catalog.md` | Shared: tool ids and prices |
| `references/scrapercity-platform.md` | Shared: plans and database allowances |
| `templates/output-template.md` | The blank plan to fill |
| `examples/worked-example.md` | A complete plan for a US SaaS VP Sales campaign |
| `scripts/check-output.py` | Run on the finished plan before delivery |

## Related Skills

- `inbox-setup` takes the mailboxes from this plan and sets names, signatures, warmup and caps.
- `email-deliverability` monitors the domains once they send.
- `sending-platforms` connects the mailboxes to a sequencer and maps ScraperCity CSVs.
- `cold-email-strategy` sets the volume target this plan sizes.
- `outbound-unit-economics` checks the infrastructure cost against meetings booked.
- `cold-email-list` builds the validated list the domains will send to.
