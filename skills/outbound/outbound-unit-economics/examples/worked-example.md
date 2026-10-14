# Outbound Unit Economics: Pipeline Partners, VP Sales at US Software Companies

Illustrative example. Pipeline Partners (pipelinepartners.example, an invented agency) sells done-for-you outbound on a $1,000 a month retainer ($12,000 ACV) and asked: what will 20 booked meetings a month cost, does it pay back, and Starter or Growth? Target: VP Sales at 50 to 200 employee US software companies. Channel: cold email, plus mobiles for the top 300 accounts. Plan: Growth. Period: one steady-state month after a one-month warmup, October 2026.

**Answer.** Run it. At benchmark rates the program costs $10,363.14 a month, books 18.91 meetings at $548.09 each and wins 2.72 deals, so CAC is $3,806.15 and pays back in 5.44 months, inside a 6 month target. The reply rate to beat is 2.91% for that target and 1.11% for a 12 month ceiling. People are 95.2% of cost, so win rate and held rate matter more than data price. Fund $44,037.46 of cash on monthly billing, or offer annual prepay and the low point falls to $20,894.62.

Every rate below is a typed input; assumptions are replaced with measured rates as the first month's sends come in.

## Inputs

| Input | Value | Type | Source |
|-|-|-|-|
| Plan fee and credits | Growth, $149 fee, $159 credits, 10% bonus on purchased credits | catalog | scrapercity.com/pricing, checked 2026-10-12 |
| Leads pulled | 4,500 from the Lead Database, email on file | user input | Sized to capacity: 3,150 contacts / 0.70 valid |
| Valid rate | 70% | assumption | Replace with a 200-email validation test ($1.44) |
| Mobile Finder inputs, hit rate | 300 work emails, 40% found | user input, assumption | Top accounts by fit; measure the hit rate on the first batch |
| Domains and mailboxes | 5 domains, 3 mailboxes each | user input | Current setup |
| Cold sends per mailbox per day | 30 | benchmark | Instantly help center, checked 2026-10-13: 30 campaign emails per account per day |
| Business days, touches per contact | 21 days, 3 touches | user input | Sequence design |
| Mailbox seat, domain | $7.00 a month; $12.00 a year | user input | Workspace bill; registrar bill |
| Sequencer | $97.00 a month | user input | Instantly Hypergrowth: 125,000 emails and 25,000 uploaded contacts a month |
| Sales Navigator Core | $119.99 a month | user input | LinkedIn list price, checked 2026-10-13 |
| Warmup before the first cold send | 1 month of mailbox and sequencer fees | benchmark | Instantly help center, 2026: at least 2 weeks of warmup before campaigns |
| SDR time and pay | 0.5 FTE; $55,000 base + $25,000 variable | benchmark | Bridge Group 2025 SDR report (6 Feb 2025): $80K median OTE, 68:32 |
| SDR manager, ramp, tenure | $146,000 OTE over 6.4 SDRs; 3.0 month ramp; 22.8 month tenure | benchmark | Bridge Group 2025 SDR report |
| Employer cost on top of pay | 19% | benchmark | BLS ECEC, June 2026, sales and related: ($2.16 insurance + $0.85 retirement + $2.69 payroll taxes) / ($26.99 wages + $2.11 paid leave + $1.05 supplemental) = 18.9%. Benefits over wages alone is 32.8%, but that counts paid leave, which a salary already pays |
| AE (founder) pay and hours | $150,000 OTE over 2,080 paid hours; 1.0 hour per held meeting, 4.0 per opportunity | user input, assumption | Agency P&L; measure hours from the calendar |
| Reply rate | 3.43% | benchmark | Instantly, Email Sequence Benchmarks 2026 (30 Mar 2026) |
| Positive share, meetings per positive reply | 35%, 50% | assumption | Measure from reply classes |
| Held rate | 80% | assumption | Measure |
| Opportunities per held meeting | 60% | benchmark | Bridge Group 2025: median monthly quotas of 10 held and 6 converted |
| Win rate | 30% | assumption | Agency's outbound-sourced deals, until measured |
| ACV, gross margin, lifetime | $12,000, 70%, 24 months | user input | Agency history |
| Billing and sales cycle | Monthly; 1 month from held meeting to signature | user input | Agency history |

## ScraperCity Cost

| Line | Tool | Count | Unit price | Cost |
|-|-|-|-|-|
| Plan fee and credits | Growth plan: $149 fee, $159 credits | 1 | $149.00 | $149.00 |
| Lead pull, VP Sales at 50 to 200 employee US software companies | Lead Database | 4,500 | Included in Growth | $0.00 |
| Email validation | Email validation | 4,500 | $0.0072 | $32.40 |
| Mobiles found | Mobile Finder | 120 | $0.25 | $30.00 |
| Mobile inputs with no number | Mobile Finder, no number found | 180 | $0.00 | $0.00 |
| ScraperCity cash for the month | $149 + max(0, $62.40 - $159.00) / 1.10 | | | $149.00 |

## Cost Stack

| Line | Basis | Count | Unit cost | Monthly cost |
|-|-|-|-|-|
| ScraperCity plan cash | fixed | 1 | $149.00 | $149.00 |
| Mailbox seats | fixed | 15 | $7.00 | $105.00 |
| Domains at $12.00 a year | fixed | 5 | $1.00 | $5.00 |
| Sequencer, Instantly Hypergrowth | fixed | 1 | $97.00 | $97.00 |
| Sales Navigator Core | fixed | 1 | $119.99 | $119.99 |
| Warmup month ($202.00) over 12 months | amortized | 1 | $16.83 | $16.83 |
| SDR, loaded | fixed | 0.5 | $10,913.57 | $5,456.79 |
| AE time on held meetings | per held meeting | 15.13 | $85.82 | $1,298.10 |
| AE time on opportunities | per opportunity | 9.08 | $343.27 | $3,115.44 |
| Total monthly program cost | | | | $10,363.14 |

SDR per FTE: ($55,000 + $25,000) x 1.19 / 12 plus the manager share $146,000 x 1.19 / 12 / 6.4 is $10,195.57; times 22.8 / 21.3 for half the ramp lost over tenure, $10,913.57. AE hour: $150,000 x 1.19 / 2,080 = $85.82.

## Capacity

| Item | Value |
|-|-|
| Mailboxes | 5 x 3 = 15 |
| Sends per month | 15 x 30 x 21 = 9,450 |
| New contacts per month at 3 touches | 9,450 / 3 = 3,150 |
| Valid emails available | 4,500 x 0.70 = 3,150 |
| Sequencer fit | Hypergrowth covers 9,450 sends and 3,150 contacts. Instantly Growth ($47) caps at 5,000 emails and 1,000 uploaded contacts, so it would use 1,000 / 3,150 = 31.7% of the mailboxes |
| Held meetings per SDR FTE | 15.13 / 0.5 = 30.26, against a Bridge 2025 median quota of 10 for SDRs who also prospect by hand |

## Funnel

| Stage | Rate | Count | Basis |
|-|-|-|-|
| Contacts emailed | 100% of capacity | 3,150 | Capacity |
| Replies | 3.43% | 108.05 | Instantly 2026 average; Hunter 2026 reports 2.4% for sequences over 500 recipients |
| Positive replies | 35% of replies | 37.82 | Assumption |
| Meetings booked | 50% of positive replies | 18.91 | Assumption |
| Meetings held | 80% of booked | 15.13 | Assumption |
| Opportunities | 60% of held | 9.08 | Bridge Group 2025 quota medians |
| Deals | 30% of opportunities | 2.72 | Assumption |

## Unit Costs

| Metric | Formula | Value |
|-|-|-|
| Total monthly program cost | Cost Stack total | $10,363.14 |
| Loaded cost per lead | $10,363.14 / 4,500 | $2.30 |
| Data cost per verified email | $32.40 / 3,150 | $0.0103 |
| Cost per mobile found | $30.00 / 120 | $0.25 |
| Cost per conversation (positive reply) | $10,363.14 / 37.82 | $274.04 |
| Cost per meeting booked | $10,363.14 / 18.91 | $548.09 |
| Cost per meeting held | $10,363.14 / 15.13 | $685.11 |
| Cost per opportunity | $10,363.14 / 9.08 | $1,141.85 |
| Cost per deal (CAC) | $10,363.14 / 2.72 | $3,806.15 |
| New CAC ratio (cost per $1 of new ARR) | $10,363.14 / (2.72 x $12,000) | $0.32 |
| Tools and data share of cost | ($149.00 + $326.99 + $16.83) / $10,363.14 | 4.8% |

Figures come from unrounded counts. Instantly's targets count software, data and rep time only: under $150 a meeting below $25K ACV (Email Sequence Benchmarks 2026, 30 Mar 2026), and $50 to $100 for B2B outbound in its cost per meeting calculator post (13 Nov 2025). On that definition this program is ($149.00 + $326.99 + $16.83 + $5,456.79) / 18.91 = $314.65 a meeting; the $548.09 above adds manager, ramp and AE time. The New CAC ratio compares with Benchmarkit's 2025 median of $2.00, an all-channel company figure.

## Break-even

| Measure | Value | Basis |
|-|-|-|
| Monthly gross margin per deal | $12,000 / 12 x 0.70 = $700.00 | Inputs |
| CAC target (6 month payback) | $700.00 x 6 = $4,200.00 | Skok, SaaS Metrics 2.0: the best recover CAC in 5 to 7 months |
| CAC ceiling (12 month payback) | $700.00 x 12 = $8,400.00 | Skok: past 12 months is weak |
| CAC payback | $3,806.15 / $700.00 = 5.44 months | Inside the 6 month target |
| LTV to CAC | $700.00 x 24 / $3,806.15 = 4.41 | Skok: above 3 |
| AE cost per deal, a CAC floor no reply rate removes | $85.82 / (0.60 x 0.30) + $343.27 / 0.30 = $1,620.99 | AE time divided by meeting to deal yield |
| Highest cost per booked meeting at 12 month payback | $8,400.00 x 0.80 x 0.60 x 0.30 = $1,209.60 | CAC ceiling x held x opportunity x win |
| Break-even reply rate, 12 month ceiling | 1.11% | Fixed cost $5,949.61 a month; AE time rises with meetings |
| Break-even reply rate, 6 month target | 2.91% | Same formula at $4,200.00 |
| Deals a quarter | 2.72 x 3 = 8.17 | One deal fewer or more moves quarterly CAC to $4,337.11 or $3,391.00, so judge CAC on a full quarter |
| Program cash break-even, monthly billing | Month 14; low point -$44,037.46 in month 7 | First deals sign in month 2 and pay $700.00 a month from month 3 |
| Program cash break-even, annual prepay | Month 4; low point -$20,894.62 in month 2 | Each deal pays $8,400.00 of margin up front |

## Sensitivity

Cost per deal by reply rate and win rate; each cell is recomputed with its own AE time.

| Reply rate | Win 15% | Win 20% | Win 30% | Win 40% |
|-|-|-|-|-|
| 1.5% | $13,235.45 | $9,926.59 | $6,617.73 | $4,963.29 |
| 2.5% | $9,238.07 | $6,928.55 | $4,619.03 | $3,464.27 |
| 3.43% | $7,612.31 | $5,709.23 | $3,806.15 | $2,854.62 |
| 4.5% | $6,573.14 | $4,929.86 | $3,286.57 | $2,464.93 |
| 5.5% | $5,967.48 | $4,475.61 | $2,983.74 | $2,237.80 |

| Scenario, one lever at a time | Total cost | Meetings booked | Deals | Cost per meeting | CAC | Payback |
|-|-|-|-|-|-|-|
| Today | $10,363.14 | 18.91 | 2.723 | $548.09 | $3,806.15 | 5.44 months |
| Reply rate 3.43% to 2.5% | $9,166.47 | 13.78 | 1.984 | $665.14 | $4,619.03 | 6.60 months |
| Held rate 80% to 70% | $9,811.45 | 18.91 | 2.382 | $518.91 | $4,118.32 | 5.88 months |
| Opportunity rate 60% to 40% | $9,324.66 | 18.91 | 1.815 | $493.16 | $5,137.11 | 7.34 months |
| Win rate 30% to 20% | $10,363.14 | 18.91 | 1.815 | $548.09 | $5,709.23 | 8.16 months |
| 2x domains and leads, SDR to 1.0 FTE | $20,352.21 | 37.82 | 5.445 | $538.19 | $3,737.46 | 5.34 months |

Win rate and opportunity rate move CAC most; doubling volume with the SDR barely moves it, because people scale with meetings.

## Recommendation

| Decision | Value | Why | Owner | Due |
|-|-|-|-|-|
| Run the program | Yes; review at day 60 | Payback 5.44 months at benchmark rates | Founder | 21 Dec 2026 |
| Reply rate to beat | 2.91% for a 6 month payback; 1.11% floor | Break-even table | SDR | 30 Nov 2026 |
| Win rate to protect | 30% or better | At 20%, payback is 8.16 months | Founder | 31 Jan 2027 |
| Reach 20 booked meetings | Add 1 domain (3 mailboxes) and pull 4,760 leads | 3,332 contacts at these rates; cost rises $278.76 and cost per meeting falls to $532.09 | SDR | 23 Oct 2026 |
| Protect the 80% held rate | Confirmation call about a week out, reminder email 12 to 24 hours before, call 2 to 3 hours before if no reply; every no-show goes back on the call list with two new times offered | Reisert, Buckets (GTMnow, Nov 2021). At 70% held, CAC rises to $4,118.32 | SDR | 20 Oct 2026 |
| SDR quota | Count held meetings and converted opportunities, not bookings | Bridge Group 2025 quotas are 10 held and 6 converted a month | Founder | 20 Oct 2026 |
| Cash and billing | Fund $44,037.46; offer annual prepay | Prepay moves cash break-even from month 14 to month 4 | Founder | 23 Oct 2026 |
| ScraperCity plan | Growth | Starter on the Apollo route is $79.95, $69.05 less (0.7% of cost); Growth gives same-day database pulls with no repeats | Founder | 16 Oct 2026 |
| First measurements | Valid rate from 200 emails; reply, positive and meeting rates on the first 3,150 contacts; win rate as those opportunities close | Replace each assumption and re-run | SDR | 30 Nov 2026 |

**Confirmation** (sent with the invite):

> Thanks {{first_name}}. You're set for Thursday, October 22 at 11:00am Central, and the invite is on its way. We'll look at where your SDR team's meetings come from and what 20 more a month would take. Anyone else who should join?

**Reminder** (12 to 24 hours before, in the invite thread):

> Looking forward to tomorrow at 11am Central. If anything's changed on your side, reply here. The link is in the invite.

**No-show** (after the start time passes and one call):

> Hi {{first_name}}, looks like today got away from you. No problem. Would Monday at 10am or Tuesday at 2pm Central work instead?

## Sources

- Instantly, Email Sequence Benchmarks 2026: https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- Instantly, cost per meeting calculator: https://instantly.ai/blog/cold-outbound-cost-per-meeting-calculator/
- Instantly limits and warmup: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits ; https://instantly.ai/pricing
- Hunter, State of Cold Email 2026: https://hunter.io/the-state-of-cold-email
- Bridge Group, 2025 SDR Metrics: https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group
- BLS ECEC, June 2026: https://www.bls.gov/news.release/ecec.t04.htm
- Skok, SaaS Metrics 2.0: https://www.forentrepreneurs.com/saas-metrics-2/
- Benchmarkit 2025: https://www.hibob.com/wp-content/uploads/2025-SaaS-Performance-Metrics-Benchmarks.pdf
- Reisert, Buckets: https://gtmnow.com/buckets-lead-generation-method/
