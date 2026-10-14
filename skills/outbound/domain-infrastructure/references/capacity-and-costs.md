# Capacity and Cost Planning

How to turn a volume target into mailboxes, domains and a monthly bill. Each default below names its source; the rest are inputs the user sets. Prices were checked on 2026-10-13.

## 1. Inputs and defaults

| Symbol | Meaning | Default | Source of default |
|-|-|-|-|
| P | New prospects contacted per sending day | Required. A request for "X emails a day" is read as X total sends (P = X / S); write that reading in the plan and the mailbox count for the other reading (X first touches) in one line | User |
| S | Steps (emails) per sequence | Required | The user's sequence (`cold-email-strategy`) |
| C | Cold sends per mailbox per day | 30, never above 50 | Instantly recommends 30 campaign emails per account a day (account and campaign limits article, checked 2026-10-13); Alex Berman keeps each inbox under 50 a day (October 2026) and Smartlead's secondary-domain article sets a maximum of 50 per address |
| M | Mailboxes per sending domain | 2 or 3, the user's choice after section 2a | Alex Berman, Instantly and Smartlead each give 2 to 3 inboxes per domain |
| R | Reserve share of domains | Required, at least 1 reserve domain | User. Growth Engine X keeps backup domains warming and builds 1,500 a day of capacity for a 1,000 a day goal (coldoutbound.com, checked 2026-10-13), which is R = 50% |
| D | Sending days per month | Required | The user's sending schedule; 21 for a weekday schedule |

## 2. Formulas

```text
daily_sends       = P x S
active_mailboxes  = ceil(daily_sends / C)
active_domains    = ceil(active_mailboxes / M)
reserve_domains   = max(1, ceil(active_domains x R))
total_domains     = active_domains + reserve_domains
total_mailboxes   = total_domains x M
per_domain_daily  = M x C
monthly_new_prospects = P x D
```

Why steady state: on day 1 of a 3-step sequence only step 1 goes out. Once the last step starts, every day carries step 1 for today's prospects and the later steps for earlier prospects. Size for that.

Reserve domains are set up, warmed and kept sending warmup only. When an active domain is paused by `email-deliverability`, a reserve takes its place the same day.

## 2a. Two or three mailboxes per domain

Same volume, two layouts. Worked for 1,500 sends a day with these example inputs: P = 500, S = 3, C = 30, R = 20%; all seats Google Workspace Starter Flexible at $8.40, domains at Porkbun's $11.08 (both checked 2026-10-13):

| Line | 3 per domain | 2 per domain |
|-|-|-|
| Active mailboxes | 50 | 50 |
| Active domains | ceil(50 / 3) = 17 (51 mailboxes) | 25 |
| Reserve domains | ceil(17 x 0.2) = 4 | 25 x 0.2 = 5 |
| Total domains, total mailboxes | 21, 63 | 30, 60 |
| Sends a day per domain | 90 | 60 |
| One domain incident pauses | 3 mailboxes, 6% of daily volume | 2 mailboxes, 4% |
| Seats a month | 63 x $8.40 = $529.20 | 60 x $8.40 = $504.00 |
| Domains a month | 21 x $11.08 / 12 = $19.39 | 30 x $11.08 / 12 = $27.70 |
| Infrastructure a month | $548.59 | $531.70 |
| Domains to set up and renew | 21 | 30 |

At this size 2 per domain costs less a month (reserve rounding needs fewer seats) and pauses less per incident, for 9 more domains to set up and renew. The user picks the layout; write the chosen layout and the other one's numbers in the plan.

## 3. Worked capacity table (example inputs C = 30, M = 3, S = 3, R = 20%)

| New prospects a day (P) | Sends a day | Active mailboxes | Active domains | Reserve domains | Total domains | Total mailboxes | Per-domain sends a day |
|-|-|-|-|-|-|-|-|
| 50 | 150 | 5 | 2 | 1 | 3 | 9 | 90 |
| 100 | 300 | 10 | 4 | 1 | 5 | 15 | 90 |
| 200 | 600 | 20 | 7 | 2 | 9 | 27 | 90 |
| 300 | 900 | 30 | 10 | 2 | 12 | 36 | 90 |
| 500 | 1,500 | 50 | 17 | 4 | 21 | 63 | 90 |
| 1,000 | 3,000 | 100 | 34 | 7 | 41 | 123 | 90 |

Check row 3: 200 x 3 = 600; 600 / 30 = 20; ceil(20 / 3) = 7; ceil(7 x 0.2) = ceil(1.4) = 2; 7 + 2 = 9; 9 x 3 = 27.

Per-domain volume stays at 90 a day in every row, about 1.8% of Google's 5,000 bulk line. At M = 2 the same rows need more domains and fewer reserve seats; section 2a works P = 500.

## 4. Monthly cost table (Google Workspace Starter Flexible, Porkbun `.com`, D = 21)

Seat $8.40 a month; domain $11.08 a year = $0.92 a month.

| P | Total mailboxes | Seats a month | Total domains | Domains a month | Infrastructure a month | Cold sends a month (P x S x D) | Cost per 1,000 sends |
|-|-|-|-|-|-|-|-|
| 50 | 9 | $75.60 | 3 | $2.77 | $78.37 | 3,150 | $24.88 |
| 100 | 15 | $126.00 | 5 | $4.62 | $130.62 | 6,300 | $20.73 |
| 200 | 27 | $226.80 | 9 | $8.31 | $235.11 | 12,600 | $18.66 |
| 500 | 63 | $529.20 | 21 | $19.39 | $548.59 | 31,500 | $17.42 |
| 1,000 | 123 | $1,033.20 | 41 | $37.86 | $1,071.06 | 63,000 | $17.00 |

Reserve mailboxes cost money and send nothing, which is why cost per 1,000 drops as volume grows.

## 5. The full monthly bill (P = 200 example)

| Line | Numbers | Monthly |
|-|-|-|
| Mailboxes | 27 x $8.40 | $226.80 |
| Domains | 9 x $11.08 / 12 | $8.31 |
| Sequencer, Instantly Hypergrowth (monthly billing) | 125,000 emails a month, 25,000 uploaded contacts | $97.00 |
| Total, infrastructure and sequencer | | $332.11 |
| Outside the total: lead data and validation, when the team buys them here | Growth plan $149.00; 4,200 new prospects x $0.0072 = $30.24 | $179.24 |

Sequencer headroom check: 12,600 sends a month is far under Instantly Hypergrowth's 125,000; 4,200 new contacts a month is under 25,000 uploaded contacts. Instantly's Growth plan ($47, 5,000 emails, 1,000 contacts) would be too small.

The plan's Total covers what the build needs to send: mailboxes, domains and the sequencer. Lead data and validation sit on one line under it. Hand the full bill to `outbound-unit-economics`, which divides it by the meetings booked after the first full month of sending.

## 6. Market size versus capacity

Capacity should not outrun the list.

```text
days_of_list = total_reachable_prospects / P
```

| Reachable prospects (from `pagination.total`) | P | Days of list |
|-|-|-|
| 3,000 | 200 | 15 |
| 9,000 | 200 | 45 |
| 40,000 | 200 | 200 |

Compare days of list with how long the user plans to run the campaign. When the list runs out first, lower P and buy fewer domains. A new domain needs 21 days of warmup before it sends (section 7), so a list shorter than that is spent before a replacement domain is ready.

Reachable means after dedupe, suppression and validation: multiply the raw total by the share of `valid` results in a 500-address validation sample.

## 7. Ramp timeline for a new build

Warmup: 21 days on the standard path, 14 on the soft start. Instantly asks for at least 2 weeks of warmup and a health score above 90%, and 3 weeks for its own AirMail accounts; Alex Berman warms for 2 to 4 weeks (both checked 2026-10-13). Warmup settings: Instantly's suggested increase of 1 a day, daily limit 10 and reply rate 30% for new accounts. Full rules, the date formula and a worked calendar: `launch-and-monitoring.md` sections 2 and 3.

Cold sends start at 10 a mailbox, the low end of Alex Berman's "start with 10-20 emails per day and ramp up over 2-4 weeks" for new domains, and step to 20 after 5 sending days and to the cap (30) after 10, so the cap is reached in 2 weeks. Every mailbox, reserves included, sends during the ramp.

| Cold sending day | Cap per mailbox | 27 mailboxes (P = 200 build) send |
|-|-|-|
| 1 to 5 | 10 | 270 |
| 6 to 10 | 20 | 540 |
| 11 onward | 30 on the 20 active, reserves back to warmup | 600 |

The first cold sending day is warmup day 22 on the standard path and day 15 on the soft start. On a Monday-to-Friday schedule, sending day 11 falls 14 calendar days after the first send. During the first days of cold mail only step 1 goes out, so the P = 200 build reaches 200 new prospects a day before it reaches 600 sends.

**Wide build.** When the date is worth more than the extra seats: `wide_mailboxes = ceil(daily_sends / wide_cap)` with `wide_cap` from Alex Berman's 10 to 20, `wide_domains = ceil(wide_mailboxes / M)`, no reserve domains (each mailbox can rise to 30 to cover a paused domain). At P = 500, S = 3 and `wide_cap` = 15: 100 mailboxes on 50 domains, 1,500 a day from the first cold day.

## 8. Launch risk, scaling triggers and retiring

**Domain age at launch is the biggest risk.** Spamhaus says unknown reputations begin as poor, and a domain bought this week has no sending history with Google, Microsoft or Yahoo. Time and low, clean volume build a reputation: 21 days of warmup on the standard path (14 at the least, on the soft start), cold sends on the ramp from 10 a mailbox, and reserves bought early enough to finish warmup before they are needed.

**Tenant blast radius.** One Google Workspace or Microsoft 365 account holding every mailbox means one account-level problem (billing lapse, admin lockout, tenant-wide sending restriction) stops all of them. Smaller tenants cap that loss for the cost of more consoles and bills. The user sets the tenant size; the plan states how many mailboxes one tenant problem would pause (`mailbox-provider-matrix.md` section 9).

Scaling triggers (each one goes in the plan with its action):

| Trigger | Action |
|-|-|
| A reserve is promoted | Buy and warm a replacement reserve the same week (about 24 days to readiness on the standard path: setup plus 21 days of warmup) |
| The daily send target rises | Add 1 domain per M x C extra sends a day; start it in warmup now |
| A new market, product line or agency client | A separate domain set for it |
| Replies per 1,000 sends differ by mailbox provider | Compare on each review; the user decides any shift of reserves between providers from the measured gap |
| Raising C above 30 | Run it as a test against the current replies per 1,000 sends and bounces, never above 50 |

Retiring:

| Event | Action |
|-|-|
| A domain's spam rate reaches Google's 0.3% or Spamhaus lists it on the DBL | Pause it, promote a reserve, run the `email-deliverability` incident runbook. Do not buy a replacement until the cause is found; Spamhaus treats volume spread across ever-changing domains as snowshoeing |
| A market is exhausted | Stop new prospects; keep domains warm at warmup volume or cancel seats at the Flexible billing date |

## Sources

- Alex Berman, TAM strategy breakdown (3 to 5 domains, 2 to 3 inboxes per domain, under 50 a day, 2 to 4 weeks of warmup; October 9, 2026): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Instantly, Account and campaign limits (30 campaign emails per account a day, checked 2026-10-13): https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Alex Berman, cold email templates (new domains start at 10 to 20 a day and ramp up over 2 to 4 weeks; checked 2026-10-13): https://alexberman.com/cold-email-templates
- Instantly, Warmup settings (increase 1, limit 10, reply rate 30 for new accounts; checked 2026-10-13): https://help.instantly.ai/en/articles/9214350-warmup-settings
- Instantly, Secondary sending domains (2 to 3 inboxes per domain, checked 2026-10-13): https://help.instantly.ai/en/articles/6502027-scale-your-cold-email-campaigns-with-secondary-sending-domains-the-strategy-how-to-implement-it
- Smartlead, Secondary sending domains (2 to 3 addresses per domain, max 50 emails per address; checked 2026-10-13): https://helpcenter.smartlead.ai/en/articles/147-all-you-need-to-know-about-secondary-sending-domains-for-cold-email-campaigns
- Google, Email sender guidelines FAQ (5,000 a day per primary domain): https://support.google.com/a/answer/14229414
- Google Workspace, Compare Flexible and Annual plans: https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans
- Porkbun, Domain pricing: https://porkbun.com/products/domains
- Instantly, Pricing: https://instantly.ai/pricing
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- ScraperCity, Pricing: https://scrapercity.com/pricing
- Spamhaus, Domain Blocklist (reputations begin as poor; snowshoeing), checked 2026-10-13: https://www.spamhaus.org/blocklists/domain-blocklist/
- Microsoft, Outbound spam protection (user and organization thresholds): https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-protection-about
- Growth Engine X, methodology (backup domains warming, 1,500 of capacity for a 1,000 goal; checked 2026-10-13): https://coldoutbound.com/
- Microsoft 365 Message Center MC1454397, new-tenant quotas (mirror, checked 2026-10-13): https://mc.merill.net/message/MC1454397
