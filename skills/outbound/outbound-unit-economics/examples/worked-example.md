# Outbound Unit Economics: Pipeline Partners, VP Sales at US Software Companies

Company and offer: Pipeline Partners (a fictional agency for this example) sells done-for-you outbound to software companies, $1,000 a month retainer, so ACV is $12,000. Target: VP Sales and Head of Sales at 50 to 200 employee US software companies. Channel mix: cold email, with mobiles bought for the top 300 accounts so the account executive can call positive replies who go quiet. ScraperCity plan: Growth. Period: one month at steady state (mailboxes warmed).

## Inputs

| Input | Value | Type | Source |
|-|-|-|-|
| Plan fee and credits | Growth, $149 fee, $159 credits, 10% bonus on purchased credits | catalog | scrapercity.com/pricing, checked 2026-10-12 |
| Leads pulled | 4,500 from the Lead Database with `hasEmail: true` | user input | Sized to mailbox capacity / valid rate (3,150 / 0.70) |
| Price per lead | $0 (included in Growth) | catalog | `references/scrapercity-platform.md` |
| Valid rate | 70% | assumption | Replace with the 200-email validation test |
| `find_mobiles` inputs | 300 work emails | user input | Top accounts by fit |
| Mobile hit rate | 40% | assumption | Replace after the first 100 inputs |
| Sending domains | 5 | user input | Current setup |
| Mailboxes per domain | 3 | user input | `references/deliverability-primer.md` (2 to 3) |
| Sends per mailbox per day | 30 | assumption | House standard in `references/deliverability-primer.md` |
| Business days | 21 | assumption | |
| Touches per contact | 3 | user input | Sequence design |
| Mailbox seat | $7.00 a month | user input | User's Google Workspace bill |
| Domain | $12.00 a year | user input | User's registrar bill |
| Sequencer | $97.00 a month | user input | User's Instantly bill |
| People cost | $4,500.00 a month | user input | Half an SDR plus AE time on first meetings |
| Reply rate | 3.43% | benchmark | Instantly 2026 benchmark report average |
| Positive share of replies | 35% | assumption | Measure from reply classes |
| Meetings per positive reply | 50% | assumption | Measure |
| Held rate | 80% | assumption | Measure |
| Close rate | 20% | assumption | Agency's last 12 months of outbound-sourced deals pending |
| ACV | $12,000 | user input | Retainer pricing |
| Gross margin | 70% | user input | Agency P&L |
| Customer lifetime | 24 months | user input | Agency history |

## ScraperCity Cost

| Line | Tool | Count | Unit price | Cost |
|-|-|-|-|-|
| Plan fee and credits | Growth plan: $149 fee, $159 credits | 1 | $149.00 | $149.00 |
| Lead Database pull | `query_lead_database` | 4,500 | Included in Growth | $0.00 |
| Email validation | `validate_emails` | 4,500 | $0.0072 | $32.40 |
| Mobiles found | `find_mobiles` | 120 | $0.25 | $30.00 |
| Mobile inputs with no number | `find_mobiles` misses | 180 | $0.00 | $0.00 |
| Catalog spend inside credits | | | | $62.40 of $159.00 credits |
| ScraperCity cash for the month | $149 + max(0, $62.40 - $159.00) / 1.10 | | | $149.00 |

`check_wallet` was called and the $62.40 of runs approved before any pull; the mobile run was estimated on its ceiling, 300 x $0.25 = $75.00.

## Capacity

| Item | Value |
|-|-|
| Mailboxes | 5 domains x 3 = 15 |
| Sends per month | 15 x 30 x 21 = 9,450 |
| New contacts per month at 3 touches | 9,450 / 3 = 3,150 |
| Valid emails available | 4,500 x 0.70 = 3,150 |
| Contacts emailed | min(3,150, 3,150) = 3,150 |
| Inbox, domain and tool cost | 15 x $7.00 + 5 x $12.00 / 12 + $97.00 = $207.00 |

## Funnel

| Stage | Rate | Count | Basis |
|-|-|-|-|
| Contacts emailed | 100% of capacity | 3,150 | Capacity |
| Replies | 3.43% | 108.05 | Instantly 2026 benchmark average; Hunter 2025 reports 4.1% |
| Positive replies | 35% of replies | 37.82 | Assumption |
| Meetings booked | 50% of positive replies | 18.91 | Assumption |
| Meetings held | 80% of booked | 15.13 | Assumption |
| Deals | 20% of held | 3.03 | Assumption |

## Unit Costs

| Metric | Formula | Value |
|-|-|-|
| Total monthly program cost | $149.00 ScraperCity + $207.00 inbox and tools + $4,500.00 people | $4,856.00 |
| Data cost per lead | $0 / 4,500 | $0.00 |
| Loaded cost per lead | $4,856.00 / 4,500 | $1.08 |
| Data cost per verified email | $32.40 / 3,150 | $0.0103 |
| Cost per mobile found | $30.00 / 120 | $0.25 |
| Cost per conversation (positive reply) | $4,856.00 / 37.82 | $128.41 |
| Cost per meeting booked | $4,856.00 / 18.91 | $256.82 |
| Cost per meeting held | $4,856.00 / 15.13 | $321.03 |
| Cost per deal | $4,856.00 / 3.03 | $1,605.15 |

Figures are computed from unrounded counts with the Python reference implementation in `references/unit-economics-model.md`.

## Break-even

| Measure | Value | Basis |
|-|-|-|
| Monthly gross margin per deal | $12,000 / 12 x 0.70 = $700.00 | Inputs |
| CAC target (6 month payback) | $4,200.00 | Skok: recover CAC in 5 to 7 months |
| CAC ceiling (12 month payback) | $8,400.00 | Skok: over 12 months is weak |
| CAC payback on this plan | $1,605.15 / $700.00 = 2.29 months | Under target |
| LTV to CAC | $700.00 x 24 / $1,605.15 = 10.47 | Skok: above 3 |
| Break-even reply rate (12 month ceiling) | 0.66% | $4,856.00 / (3,150 x 0.35 x 0.50 x 0.80 x 0.20 x $8,400.00) |
| Break-even reply rate (6 month target) | 1.31% | Same formula with $4,200.00 |
| Plan comparison at this usage | Starter $79.95 vs Growth $149.00 | Starter: Apollo 4,500 x $0.0039 = $17.55 plus $32.40 validation plus $30.00 mobiles = $79.95 of usage, above the $49 credits |
| Plan break-even | Starter and Growth tie at $149.00 of monthly catalog usage | `references/break-even-and-sensitivity.md` section 1 |

## Sensitivity

Cost per deal by reply rate and close rate, everything else unchanged.

| Reply rate | Close 10% | Close 15% | Close 20% | Close 30% |
|-|-|-|-|-|
| 1.5% | $7,340.89 | $4,893.93 | $3,670.45 | $2,446.96 |
| 2.5% | $4,404.54 | $2,936.36 | $2,202.27 | $1,468.18 |
| 3.43% | $3,210.30 | $2,140.20 | $1,605.15 | $1,070.10 |
| 4.1% | $2,685.69 | $1,790.46 | $1,342.85 | $895.23 |
| 5.5% | $2,002.06 | $1,334.71 | $1,001.03 | $667.35 |

Cost per meeting booked by positive share (rows) and reply rate (columns):

| Positive share | 1.5% | 2.5% | 3.43% | 4.1% | 5.5% |
|-|-|-|-|-|-|
| 20% | $1,027.72 | $616.63 | $449.44 | $376.00 | $280.29 |
| 35% | $587.27 | $352.36 | $256.82 | $214.86 | $160.16 |
| 50% | $411.09 | $246.65 | $179.78 | $150.40 | $112.12 |

Three cells land over the 6 month target ($4,200.00): 1.5% replies at a 10% or 15% close rate, and 2.5% replies at 10%. None passes the 12 month ceiling ($8,400.00).

## Recommendation

| Decision | Value | Why |
|-|-|-|
| Run the program | Yes, at 15 mailboxes | Payback 2.29 months at benchmark rates; every sensitivity cell stays under the $8,400.00 ceiling |
| Reply rate to beat | 1.31% (6 month target), 0.66% floor | Break-even table |
| ScraperCity plan | Growth for month 1, review at month 3 | Starter is $69.05 cheaper at this usage, but Growth gives same-day Lead Database pulls and `excludeDelivered` dedupe with no Apollo account or multi-day wait |
| Unused credits | $96.60 a month ($159.00 - $62.40) | Spend on validation of month 2's pull early or on `find_mobiles` for more accounts |
| Leads per month | 4,500 | Matches 3,150 contacts of capacity at a 70% valid rate |
| First measurements | Valid rate after 200 emails; reply, positive share and meeting rate after 1,000 contacts | Replace assumptions, re-run the model |
| Scale trigger | Measured cost per meeting under $250 for 2 months | Add 5 domains (15 mailboxes) and 4,500 leads; ScraperCity cost stays inside Growth credits until catalog usage passes $159 |
