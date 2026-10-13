# Capacity and Cost Planning

How to turn "new prospects per day" into mailboxes, domains and a monthly bill. Formulas are the house standard used by every outbound skill in this repo. Prices were checked on 2026-10-12.

## 1. Inputs and defaults

| Symbol | Meaning | Default | Source of default |
|-|-|-|-|
| P | New prospects contacted per sending day | Required | User |
| S | Steps (emails) per sequence | 3 | House standard; see `cold-email-strategy` |
| C | Cold sends per mailbox per day | 30 | House standard, inside Alex Berman's "under 50 per inbox" |
| M | Mailboxes per sending domain | 3 | Alex Berman: 2 to 3 inboxes per domain |
| R | Reserve share of domains | 20%, minimum 1 domain | House standard |
| D | Sending days per month | 21 | Weekdays |

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

Why steady state: on day 1 of a 3-step sequence only step 1 goes out. By the time step 3 starts (day 7 to 10 in a typical cadence) every day carries step 1 for today's prospects, step 2 for last week's and step 3 for the week before. Size for that.

Reserve domains are set up, warmed and kept sending warmup only. When an active domain is paused by `email-deliverability`, a reserve takes its place the same day.

## 3. Worked capacity table (C = 30, M = 3, S = 3)

| New prospects a day (P) | Sends a day | Active mailboxes | Active domains | Reserve domains | Total domains | Total mailboxes | Per-domain sends a day |
|-|-|-|-|-|-|-|-|
| 50 | 150 | 5 | 2 | 1 | 3 | 9 | 90 |
| 100 | 300 | 10 | 4 | 1 | 5 | 15 | 90 |
| 200 | 600 | 20 | 7 | 2 | 9 | 27 | 90 |
| 300 | 900 | 30 | 10 | 2 | 12 | 36 | 90 |
| 500 | 1,500 | 50 | 17 | 4 | 21 | 63 | 90 |
| 1,000 | 3,000 | 100 | 34 | 7 | 41 | 123 | 90 |

Check row 3: 200 x 3 = 600; 600 / 30 = 20; ceil(20 / 3) = 7; ceil(7 x 0.2) = ceil(1.4) = 2; 7 + 2 = 9; 9 x 3 = 27.

Per-domain volume stays at 90 a day in every row, about 1.8% of Google's 5,000 bulk line.

## 4. Monthly cost table (Google Workspace Starter Flexible, Porkbun `.com`)

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
| Lead data, ScraperCity Growth plan | Lead Database included, 100,000 new leads a day allowance | $149.00 |
| Validation | 4,200 new prospects x $0.0072 | $30.24 |
| Total | | $511.35 |

Sequencer headroom check: 12,600 sends a month is far under Instantly Hypergrowth's 125,000; 4,200 new contacts a month is under 25,000 uploaded contacts. Instantly's Growth plan ($47, 5,000 emails, 1,000 contacts) would be too small.

Hand this bill to `outbound-unit-economics` to compare against meetings. Example check: if 4,200 prospects a month yield 1% positive replies (42) and half book (21 meetings), cost per meeting from infrastructure, data and validation is $511.35 / 21 = $24.35. The 1% is a planning hypothesis to replace with your own reply data.

## 6. Market size versus capacity

Capacity should not outrun the list.

```text
days_of_list = total_reachable_prospects / P
```

| Reachable prospects (from `pagination.total`) | P | Days of list | Verdict |
|-|-|-|-|
| 3,000 | 200 | 15 | Overbuilt. Drop to P = 50 (60 days) and 3 domains |
| 9,000 | 200 | 45 | Fine for a 2-month test |
| 40,000 | 200 | 200 | Room to scale after the test |

Reachable means after dedupe, suppression and validation: multiply the raw total by the share of `valid` results in a 500-address validation sample.

## 7. Ramp timeline for a new build

| Day | What happens | Cold sends a day (P = 200 build) |
|-|-|-|
| 0 | Domains registered, DNS written | 0 |
| 1 to 3 | Mailboxes created, DKIM signing on, header tests pass, warmup starts | 0 |
| 4 to 14 | Warmup only | 0 |
| 15 to 21 | 10 a mailbox on 20 active mailboxes | 200 |
| 22 to 28 | 20 a mailbox | 400 |
| 29 onward | 30 a mailbox | 600 |

New prospects per day during ramp: 200 sends on days 15 to 21 is about 67 new prospects a day once follow-ups start. Full P = 200 arrives in week 5.

## 8. Scaling and retiring

| Event | Action |
|-|-|
| A domain's complaint rate crosses 0.3% or it lands on the Spamhaus DBL | Pause it, promote a reserve, run the `email-deliverability` incident runbook |
| Reserve count drops to 0 | Buy and warm a new reserve the same week (14 days to readiness) |
| Reply rate per mailbox stays healthy for 30 days with bounces under 1% | Raise C toward 40, never above 50 |
| A market is exhausted | Stop new prospects; keep domains warm at warmup volume or cancel seats at the Flexible billing date |

## Sources

- Alex Berman, TAM strategy breakdown (3 to 5 domains, 2 to 3 inboxes per domain, under 50 a day): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Google, Email sender guidelines FAQ (5,000 a day per primary domain): https://support.google.com/a/answer/14229414
- Google Workspace, Compare Flexible and Annual plans: https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans
- Porkbun, Domain pricing: https://porkbun.com/products/domains
- Instantly, Pricing: https://instantly.ai/pricing
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- ScraperCity, Pricing: https://scrapercity.com/pricing
