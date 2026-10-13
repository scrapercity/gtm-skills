# Break-even and Sensitivity

Every table here was computed with the Python reference implementation in `references/unit-economics-model.md` section 5, using the default inputs unless a row says otherwise. Re-run it with the user's inputs before quoting any number.

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
- Scale's higher rate limits matter for automation, not for this table.
- Large, steady usage favors buying extra credits on Scale (30% bonus) over stacking Growth purchases (10%).

## 2. CAC ceilings by deal size

Monthly gross margin per deal = ACV / 12 x gross margin. Skok: recover CAC in about 5 to 7 months (6 used as target), over 12 months is weak (ceiling). Gross margin 70% in every row.

| ACV | Monthly gross margin per deal | CAC target (6 month payback) | CAC ceiling (12 month payback) |
|-|-|-|-|
| $3,000 | $175.00 | $1,050.00 | $2,100.00 |
| $6,000 | $350.00 | $2,100.00 | $4,200.00 |
| $12,000 | $700.00 | $4,200.00 | $8,400.00 |
| $24,000 | $1,400.00 | $8,400.00 | $16,800.00 |
| $60,000 | $3,500.00 | $21,000.00 | $42,000.00 |

For one-time sales (services, real estate), use gross profit per deal as the ceiling and skip payback.

## 3. Break-even reply rate

```
break-even reply rate = total monthly cost / (contacts x positive share x meeting rate x held rate x close rate x CAC limit)
```

Defaults: total $4,856.00, 3,150 contacts, 35% positive, 50% meeting, 80% held, 20% close.

| CAC limit | Value at $12,000 ACV | Break-even reply rate |
|-|-|-|
| 12 month payback ceiling | $8,400.00 | 0.66% |
| 6 month payback target | $4,200.00 | 1.31% |

The default plan at 3.43% replies clears both with room. A program that only clears the ceiling at a reply rate above the user's measured rate should not scale.

## 4. Sensitivity: cost per deal by reply rate and close rate

Everything else at defaults (total $4,856.00 a month, 3,150 contacts).

| Reply rate | Meetings booked | Close 10% | Close 15% | Close 20% | Close 30% |
|-|-|-|-|-|-|
| 1.5% | 8.27 | $7,340.89 | $4,893.93 | $3,670.45 | $2,446.96 |
| 2.5% | 13.78 | $4,404.54 | $2,936.36 | $2,202.27 | $1,468.18 |
| 3.43% (Instantly 2026 average) | 18.91 | $3,210.30 | $2,140.20 | $1,605.15 | $1,070.10 |
| 4.1% (Hunter 2025) | 22.60 | $2,685.69 | $1,790.46 | $1,342.85 | $895.23 |
| 5.5% (Instantly top quartile) | 30.32 | $2,002.06 | $1,334.71 | $1,001.03 | $667.35 |

Payback at a 20% close rate: 5.24 months at 1.5% replies, 3.15 at 2.5%, 2.29 at 3.43%, 1.92 at 4.1%, 1.43 at 5.5%.

## 5. Sensitivity: cost per meeting by positive share and reply rate

| Positive share | 1.5% | 2.5% | 3.43% | 4.1% | 5.5% |
|-|-|-|-|-|-|
| 20% | $1,027.72 | $616.63 | $449.44 | $376.00 | $280.29 |
| 35% | $587.27 | $352.36 | $256.82 | $214.86 | $160.16 |
| 50% | $411.09 | $246.65 | $179.78 | $150.40 | $112.12 |

Instantly's 2026 post sets cost per meeting targets of under $150 (SMB, ACV under $25K), $250 (mid-market) and $350 (enterprise), counting software, data and rep time. The default model lands at $256.82, so it meets the enterprise target and misses the SMB one; with $4,500 of people cost in a $4,856 total, people time is the lever.

## 6. Phone add-on

Cold calling costs are mostly people. From the `cold-calling` worked example (2 SDRs, 20 business days, local contractors in Dallas-Fort Worth):

| Line | Value |
|-|-|
| Dials | 4,680 |
| Conversations (owner engaged past the opener) | 271 |
| Meetings booked | 16 |
| Total cash (plan, `find_mobiles` from credits, registry, dialer, SDRs) | $10,874.00 |
| Cost per conversation | $40.13 |
| Cost per meeting booked | $679.63 |

Formulas:

```
conversations = dials x connect rate x (DM reached rate) x conversation rate
cost per conversation = (people + dialer + plan + mobiles + registry) / conversations
```

`find_mobiles` costs $0.25 per number found and nothing on a miss, so 1,000 inputs at a 35% hit rate cost $87.50, and at 50% cost $125.00. Budget the ceiling (1,000 x $0.25 = $250.00) and approve on it.

## 7. Reading the grids

| If | Then |
|-|-|
| Cost per deal at your measured reply rate is under the 6 month target | Scale volume: more domains and mailboxes, then more leads |
| Between the target and the ceiling | Fix the weakest stage first (positive share, meeting rate) before adding volume |
| Over the ceiling | Stop scaling; revisit targeting and offer (`cold-email-strategy`) |
| Meeting rate per positive reply under 30% | Reply handling speed and the ask (`reply-handling`) |
| Held rate under 70% | Confirmation and booking window |

## Sources

- https://www.forentrepreneurs.com/saas-metrics-2/
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email-2025
- https://belkins.io/blog/cold-calling-benchmarks
- https://scrapercity.com/pricing
