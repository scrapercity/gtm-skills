# Break-even and Sensitivity

Every table here was computed with `scripts/unit-economics-model.py` using the default inputs (the worked example) unless a row says otherwise. Re-run it with the user's inputs before quoting any number.

## 1. Plan break-even on catalog usage

Monthly cash cost of each plan at a given catalog-price usage (the sum of billable results times catalog prices). Formula: fee + max(0, usage - credits) / (1 + bonus). Database access is not valued here; Growth and Scale include the Lead Database and Local Business Database on top.

| Monthly catalog usage | Starter ($49, $49 credits) | Growth ($149, $159 credits, 10% bonus) | Scale ($649, $800 credits, 30% bonus) | Cheapest |
|-|-|-|-|-|
| $49 | $49.00 | $149.00 | $649.00 | Starter |
| $100 | $100.00 | $149.00 | $649.00 | Starter |
| $149 | $149.00 | $149.00 | $649.00 | Starter and Growth tie |
| $159 | $159.00 | $149.00 | $649.00 | Growth |
| $300 | $300.00 | $277.18 | $649.00 | Growth |
| $500 | $500.00 | $459.00 | $649.00 | Growth |
| $709 | $709.00 | $649.00 | $649.00 | Growth and Scale tie |
| $800 | $800.00 | $731.73 | $649.00 | Scale |
| $1,000 | $1,000.00 | $913.55 | $802.85 | Scale |
| $2,000 | $2,000.00 | $1,822.64 | $1,572.08 | Scale |

Crossovers: Starter to Growth at $149 of usage; Growth to Scale at $709 (149 + (709 - 159) / 1.10 = 649).

What changes the answer:

- A team that would otherwise pay $0.0039 per lead for Apollo pulls gets Lead Database records at $0 on Growth. 10,000 leads a month is $39.00 of Apollo usage that disappears.
- Scale's higher rate limits help automation and do not change this table.
- Large, steady usage favors buying extra credits on Scale (30% bonus) over stacking Growth purchases (10%).
- The plan is a small line next to people: in the worked example the Starter route saves $69.05 a month, 0.7% of program cost.

## 2. CAC limits and the most a meeting can cost, by deal size

Monthly gross margin per deal = ACV / 12 x gross margin (70% in every row). Skok: the best businesses recover CAC in 5 to 7 months (6 used as the target); past 12 months is weak (the ceiling). The last column multiplies the ceiling by the default meeting-to-deal yield, held 80% x opportunity 60% x win 30% = 14.4%.

| ACV | Monthly gross margin per deal | CAC target (6 months) | CAC ceiling (12 months) | Highest cost per booked meeting at the ceiling |
|-|-|-|-|-|
| $3,000 | $175.00 | $1,050.00 | $2,100.00 | $302.40 |
| $6,000 | $350.00 | $2,100.00 | $4,200.00 | $604.80 |
| $12,000 | $700.00 | $4,200.00 | $8,400.00 | $1,209.60 |
| $24,000 | $1,400.00 | $8,400.00 | $16,800.00 | $2,419.20 |
| $60,000 | $3,500.00 | $21,000.00 | $42,000.00 | $6,048.00 |

The default AE time costs $1,620.99 per deal no matter how many replies come in. At $3,000 ACV that alone is above the $1,050 target, so the program needs fewer AE hours per opportunity, a higher win rate or a higher price before volume can help.

For one-time sales (services, real estate), use gross profit per deal as the ceiling and skip payback.

## 3. Break-even reply rate

Fixed costs stay flat as replies rise, while AE time grows with every meeting. Solving CAC = limit for the reply rate:

```
held yield per reply rate   k_held = positive share x meeting rate x held rate
opportunity yield           k_opp  = k_held x opportunity rate
deal yield                  k_deal = k_opp x win rate
break-even reply rate = fixed monthly cost / (contacts x (k_deal x CAC limit - k_held x AE cost per held meeting - k_opp x AE cost per opportunity))
```

When the bracket is zero or negative, no reply rate pays back. Defaults: fixed $5,949.61, 3,150 contacts, 35% positive, 50% meeting, 80% held, 60% opportunity, 30% win, AE $85.82 per held meeting and $343.27 per opportunity.

| ACV | Break-even reply rate, 12 month ceiling | Break-even reply rate, 6 month target |
|-|-|-|
| $6,000 | 2.91% | 15.65% |
| $12,000 | 1.11% | 2.91% |
| $24,000 | 0.49% | 1.11% |

The default plan at 3.43% replies clears the 6 month target at $12,000 ACV with 0.52 points to spare. At $6,000 ACV it clears only the 12 month ceiling.

## 4. Sensitivity: cost per deal by reply rate and win rate

Everything else at defaults. AE time moves with meetings, so each row has its own total.

| Reply rate | Total cost | Meetings booked | Win 15% | Win 20% | Win 30% | Win 40% | Payback at 30% |
|-|-|-|-|-|-|-|-|
| 1.5% | $7,879.73 | 8.27 | $13,235.45 | $9,926.59 | $6,617.73 | $4,963.29 | 9.45 months |
| 2.5% | $9,166.47 | 13.78 | $9,238.07 | $6,928.55 | $4,619.03 | $3,464.27 | 6.60 months |
| 3.43% (Instantly 2026 average) | $10,363.14 | 18.91 | $7,612.31 | $5,709.23 | $3,806.15 | $2,854.62 | 5.44 months |
| 4.5% (Hunter 2026 average) | $11,739.96 | 24.81 | $6,573.14 | $4,929.86 | $3,286.57 | $2,464.93 | 4.70 months |
| 5.5% (Instantly top quartile) | $13,026.70 | 30.32 | $5,967.48 | $4,475.61 | $2,983.74 | $2,237.80 | 4.26 months |

Across these ranges win rate moves CAC further than reply rate: going from 15% to 40% wins cuts CAC 2.7x at 3.43% replies, while going from 1.5% to 5.5% replies cuts it 2.2x at a 30% win rate.

## 5. Sensitivity: cost per meeting by positive share and reply rate

| Positive share | 1.5% | 2.5% | 3.43% | 4.5% | 5.5% |
|-|-|-|-|-|-|
| 20% | $1,492.60 | $988.93 | $784.08 | $653.15 | $576.83 |
| 35% | $952.95 | $665.14 | $548.09 | $473.27 | $429.66 |
| 50% | $737.09 | $535.63 | $453.69 | $401.31 | $370.79 |

Instantly's Email Sequence Benchmarks 2026 post (30 Mar 2026) sets cost per meeting targets of under $150 (SMB, ACV under $25K), $250 (mid-market) and $350 (enterprise), counting software, data and rep time; it does not describe how the targets were set. Its cost per meeting calculator post (13 Nov 2025) calls $50 to $100 strong for B2B outbound on the same kind of cost base. Name the post and date when quoting either. The default model comes out at $548.09 because it also counts the SDR manager, ramp and AE time. Compare like with like: drop those lines when matching Instantly's definition, and keep them when deciding whether to fund the program.

## 6. Scale: 1x, 2x and 3x volume

Domains, leads, mobile inputs and SDR FTE scale together; the sequencer tier and Sales Navigator license stay; ScraperCity cash stays $149.00 while catalog usage is inside Growth credits.

| Volume | Total cost | Meetings booked | Cost per meeting | CAC |
|-|-|-|-|-|
| 1x | $10,363.14 | 18.91 | $548.09 | $3,806.15 |
| 2x | $20,352.21 | 37.82 | $538.19 | $3,737.46 |
| 3x | $30,366.92 | 56.72 | $535.35 | $3,717.70 |

Volume barely moves unit cost because people are 95% of it and scale with meetings. Rates move it: one more point of reply rate does more than tripling volume.

## 7. Program cash curve

Month 0 is warmup (one-time $202.00). Sends start in month 1, the first deals sign in month 2 (one month sales cycle) and pay from month 3. Monthly cash out is $10,346.31 (the total less the amortized one-time line).

| Month | Margin in, monthly billing | Cumulative, monthly billing | Margin in, annual prepay | Cumulative, annual prepay |
|-|-|-|-|-|
| 0 | $0.00 | -$202.00 | $0.00 | -$202.00 |
| 1 | $0.00 | -$10,548.31 | $0.00 | -$10,548.31 |
| 2 | $0.00 | -$20,894.62 | $0.00 | -$20,894.62 |
| 3 | $1,905.91 | -$29,335.02 | $22,870.97 | -$8,369.96 |
| 4 | $3,811.83 | -$35,869.50 | $22,870.97 | $4,154.69 |
| 5 | $5,717.74 | -$40,498.07 | $22,870.97 | $16,679.35 |
| 6 | $7,623.66 | -$43,220.72 | $22,870.97 | $29,204.00 |
| 7 | $9,529.57 | -$44,037.46 | $22,870.97 | $41,728.66 |
| 8 | $11,435.48 | -$42,948.29 | $22,870.97 | $54,253.31 |
| 10 | $15,247.31 | -$35,052.20 | $22,870.97 | $79,302.63 |
| 12 | $19,059.14 | -$19,532.46 | $22,870.97 | $104,351.94 |
| 13 | $20,965.05 | -$8,913.72 | $22,870.97 | $116,876.59 |
| 14 | $22,870.97 | $3,610.94 | $22,870.97 | $129,401.25 |

Each deal pays back in 5.44 months, yet the program needs $44,037.46 of cash and 14 months to break even on monthly billing, because every month adds a new cohort that pays back in installments. Annual prepay cuts the low point to $20,894.62 and break-even to month 4. Quote both numbers whenever a founder asks whether outbound "pays back".

## 8. Reverse sizing: what a meeting target takes

At default rates one contact yields 3.43% x 35% x 50% = 0.60% meetings booked. People are held at 0.5 SDR FTE; check reply volume against SDR hours before trusting the larger rows.

| Booked meetings a month | Contacts | Leads to pull at 70% valid | Mailboxes needed | Domains (3 mailboxes each) | Total cost | Cost per meeting |
|-|-|-|-|-|-|-|
| 20 | 3,332 | 4,760 | 16 | 6 | $10,641.90 | $532.09 |
| 25 | 4,165 | 5,950 | 20 | 7 | $11,832.78 | $473.30 |
| 30 | 4,998 | 7,140 | 24 | 8 | $13,023.67 | $434.12 |

New mailboxes need at least 2 weeks of warmup before campaigns (Instantly help center), so plan the extra meetings for the month after they are bought.

## 9. Plan versus actual: which stage explains the gap

Cost per meeting = total / (contacts x reply rate x positive share x meeting rate). Taking logs, the gap between plan and actual splits into one share per term, and the shares add to 100%. `scripts/unit-economics-model.py variance actual.json` prints them.

Worked: plan $548.09 per meeting. After the first 1,000 contacts the measured rates are 2.5% replies, 30% positive and 45% meeting rate, and actual cost per meeting is $793.06.

| Term | Share of the gap |
|-|-|
| Reply rate (3.43% to 2.5%) | 85.6% |
| Positive share (35% to 30%) | 41.7% |
| Meeting rate (50% to 45%) | 28.5% |
| Total cost (fewer meetings, less AE time) | -55.8% |
| Contacts emailed | 0.0% |

Reply rate explains most of the gap, so the fix starts with targeting and offer (`cold-email-strategy`), then reply handling for the positive share and meeting rate (`reply-handling`). Re-forecast after any month where cost per meeting runs over plan by more than the margin the user sets.

## 10. Phone add-on

Cold calling costs are mostly people. From the `cold-calling` worked example (2 SDRs, 20 business days, local contractors in Dallas-Fort Worth):

| Line | Value |
|-|-|
| Dials | 4,680 |
| Conversations (owner engaged past the opener) | 271 |
| Meetings booked | 16 |
| Total cash (plan, `find_mobiles` from credits, dialer, SDRs) | $10,789.00 |
| Cost per conversation | $39.81 |
| Cost per meeting booked | $674.31 |

Formulas:

```
conversations = dials x connect rate x (DM reached rate) x conversation rate
cost per conversation = (people + dialer + plan + mobiles) / conversations
```

`find_mobiles` costs $0.25 per number found and nothing on a miss, so 1,000 inputs at a 35% hit rate cost $87.50, and at 50% cost $125.00. Budget the ceiling (1,000 x $0.25 = $250.00) and approve on it.

## 11. Reading the grids

| If | Then |
|-|-|
| Cost per deal at your measured rates is under the 6 month target | Scale: more domains and mailboxes, then more leads, then SDR hours |
| Between the target and the ceiling | Fix the weakest stage first (section 9) before adding volume |
| Over the ceiling | Stop scaling; revisit targeting and offer (`cold-email-strategy`) |
| AE cost per deal above the 6 month target | Cut AE hours per opportunity or raise the win rate; replies will not fix it |
| Meeting rate per positive reply below the plan's rate | Reply handling speed and the ask (`reply-handling`) |
| Held rate below the plan's rate | Confirmation sequence and no-show rebooking (section 12) |
| Opportunity rate below the plan's rate | A qualifying question before the calendar link (section 12) |
| Cash low point larger than the user can fund | Offer annual prepay or start with fewer mailboxes |

## 12. Stage fixes with sendable copy

Every fix the deliverable names is written out in full, with an owner on the user's team and a calendar date. Fill the bracketed parts with the user's offer and times; the deliverable carries finished text.

| Stage that misses | Fix | Source |
|-|-|-|
| Held rate | Confirm by phone about a week out, by email 12 to 24 hours before, and by phone 2 to 3 hours before if the email got no reply. A no-show or cancellation goes back on the call list until a new time is booked | Ryan Reisert, Buckets (GTMnow, 29 Nov 2021) |
| Opportunity rate | Before sending times, ask one present-tense closed question about today's process and confirm the person owns it | Ronen Pessar, The Sales Doctor ep. 43 and Triple Session |
| Held and opportunity rates together | Count the SDR's quota in held meetings and converted opportunities, not bookings | Bridge Group 2025 SDR report: quota medians of 10 held and 6 converted a month |

Copy (the confirmation, reminder and no-show texts follow the response library used for reply handling):

**Confirmation**, sent with the invite:

> Thanks {{first_name}}. You're set for [day, date and time with time zone], and the invite is on its way. We'll look at [the problem they named] and what fixing it would take. Anyone else who should join?

**Reminder**, 12 to 24 hours before, in the invite thread:

> Looking forward to tomorrow at [time]. If anything's changed on your side, reply here. The link is in the invite.

**No-show**, once the start time has passed and one call went unanswered:

> Hi {{first_name}}, looks like today got away from you. No problem. Would [day and time] or [day and time] work instead?

**Qualifying question**, in the reply that would carry the calendar link:

> Before I send times: do you [the process the offer fixes] in-house today, and are you the one who decides whether to change it?

The deliverable states the measured lift only once the user's own held and opportunity rates come in; until then the scenario table shows what each rate is worth.

## Sources

- https://www.forentrepreneurs.com/saas-metrics-2/
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email
- https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group
- https://belkins.io/blog/cold-calling-benchmarks
- https://scrapercity.com/pricing
- https://instantly.ai/blog/cold-outbound-cost-per-meeting-calculator/
- https://gtmnow.com/buckets-lead-generation-method/
- https://www.thesalesdocrx.com/podcast/episode-43-cold-calling-techniques-that-work-with-ronen-pessar
- https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
