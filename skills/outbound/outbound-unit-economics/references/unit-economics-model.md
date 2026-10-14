# Unit Economics Model

The spreadsheet-ready model behind this skill: every input with its default and type, every cell and formula, a CSV block to paste into Google Sheets or Excel, a cash curve tab, and how to check the sheet against `scripts/unit-economics-model.py`. The defaults are the worked example's inputs (an illustrative agency booking VP Sales meetings at US software companies on the Growth plan).

## 1. How to use it

1. Paste the CSV block (section 5) into cell A1 of an empty tab named `Model`. Column A holds labels, column B values and formulas, so the first input sits in B2.
2. Replace every value in B2 to B45 with the user's numbers. Keep the type labels from section 2 beside the sheet so an assumption is never read as a fact.
3. Read the outputs in B46 to B90.
4. Add the `Cash` tab from section 6 for the month-by-month curve.
5. Check the sheet: save the same inputs as JSON and run `python3 scripts/unit-economics-model.py my.json`. Every output must match to the cent. Add a command after the file for the grids (`grid`), plan comparison (`plans`), cash curve (`cash`), target sizing (`target 20`), scale scenarios (`scale`) or the plan versus actual split (`variance actual.json`).

## 2. Inputs, defaults and types

| Input | Cell | Default | Type | Source or note |
|-|-|-|-|-|
| Plan fee | B2 | 149 | catalog | Starter 49, Growth 149, Scale 649 (scrapercity.com/pricing, checked 2026-10-12) |
| Plan credits | B3 | 159 | catalog | Starter 49, Growth 159, Scale 800 |
| Bonus on purchased credits | B4 | 0.10 | catalog | Starter 0, Growth 0.10, Scale 0.30 |
| Leads pulled | B5 | 4,500 | user input | Size to capacity (B55) divided by the valid rate |
| Catalog price per lead | B6 | 0 | catalog | Lead Database and Local Business Database on Growth or Scale 0; `scrape_apollo` 0.0039; `scrape_store_leads` 0.0039; `scrape_maps` 0.0099 |
| Valid rate | B7 | 0.70 | assumption | Measure with a 200-email `validate_emails` test ($1.44) |
| Inputs to `find_mobiles` | B8 | 300 | user input | Tier A accounts or calls planned |
| Mobile hit rate | B9 | 0.40 | assumption | Measure on 100 inputs; cost per mobile stays $0.25 |
| Sending domains | B10 | 5 | user input | `domain-infrastructure` |
| Mailboxes per domain | B11 | 3 | user input | 2 to 3 per the deliverability primer |
| Cold sends per mailbox per day | B12 | 30 | benchmark | Instantly help center: 30 campaign emails per account per day (checked 2026-10-13); Smartlead's September 2026 guide caps a mailbox at 50 |
| Business days per month | B13 | 21 | assumption | |
| Touches per contact | B14 | 3 | user input | Sequence length |
| Mailbox seat per month | B15 | 7 | user input | The user's Workspace or Microsoft 365 bill (`references/cost-stack.md` section 3) |
| Domain per year | B16 | 12 | user input | Registrar bill |
| Sequencer per month | B17 | 97 | user input | The tier that covers B54 sends and B56 contacts |
| Other tools per month | B18 | 119.99 | user input | Sales Navigator, dialer, warmup add-ons, CRM seat share |
| Warmup months | B19 | 1 | assumption | Mailbox and sequencer fees paid before the first cold send; Instantly asks for at least 2 weeks of warmup |
| Other one-time setup | B20 | 0 | user input | Setup hours, a consultant, extra domains bought ahead |
| Months to spread one-time costs | B21 | 12 | assumption | |
| SDR FTE on this program | B22 | 0.5 | user input | Share of a seat; split shared SDRs by hours |
| SDR base | B23 | 55,000 | benchmark | Bridge Group 2025 median; replace with the offer letter |
| SDR variable at target | B24 | 25,000 | benchmark | Same |
| Share of variable paid | B25 | 1.0 | assumption | Bridge 2025 reports 60% of SDRs at quota |
| Employer cost on pay | B26 | 0.19 | benchmark | BLS ECEC June 2026, derived in `references/cost-stack.md` section 1 |
| SDR manager OTE | B27 | 146,000 | benchmark | Bridge Group 2025 |
| SDRs per manager | B28 | 6.4 | benchmark | Bridge Group 2025 |
| SDR ramp months | B29 | 3.0 | benchmark | Bridge Group 2025 |
| SDR tenure months | B30 | 22.8 | benchmark | Bridge Group 2025 (1.9 years) |
| AE OTE | B31 | 150,000 | user input | Founder or AE taking first meetings |
| AE paid hours per year | B32 | 2,080 | assumption | 40 x 52 |
| AE hours per held meeting | B33 | 1.0 | assumption | Prep, call and notes; measure from the calendar |
| AE hours per opportunity | B34 | 4.0 | assumption | Proposal, follow-up calls and close |
| Other people cost per month | B35 | 0 | user input | Recruiting fees spread over tenure, a copywriter, an agency retainer |
| Reply rate | B36 | 0.0343 | benchmark | Instantly 2026 benchmark average; Hunter 2026 reports 4.5% |
| Positive share of replies | B37 | 0.35 | assumption | No published figure used; classify replies and measure |
| Meetings per positive reply | B38 | 0.50 | assumption | Measure |
| Held rate | B39 | 0.80 | assumption | Measure |
| Opportunities per held meeting | B40 | 0.60 | benchmark | Bridge Group 2025 medians, 6 converted per 10 held |
| Win rate | B41 | 0.30 | assumption | The user's CRM history for outbound-sourced opportunities |
| ACV | B42 | 12,000 | user input | |
| Gross margin | B43 | 0.70 | user input | |
| Customer lifetime in months | B44 | 24 | user input | Or 1 / monthly logo churn (section 4) |
| Sales cycle in months | B45 | 1 | user input | Held meeting to signature |

## 3. Cells and formulas

| Cell | Label | Formula | Example result |
|-|-|-|-|
| B46 | Lead cost at catalog price | `=B5*B6` | 0.00 |
| B47 | validate_emails cost | `=B5*0.0072` | 32.40 |
| B48 | Valid emails | `=B5*B7` | 3,150.00 |
| B49 | Mobiles found | `=B8*B9` | 120.00 |
| B50 | find_mobiles cost | `=B49*0.25` | 30.00 |
| B51 | Catalog-price spend | `=B46+B47+B50` | 62.40 |
| B52 | ScraperCity cash | `=B2+MAX(0,B51-B3)/(1+B4)` | 149.00 |
| B53 | Mailboxes | `=B10*B11` | 15.00 |
| B54 | Sends per month | `=B53*B12*B13` | 9,450.00 |
| B55 | New contacts per month at capacity | `=B54/B14` | 3,150.00 |
| B56 | Contacts emailed | `=MIN(B48,B55)` | 3,150.00 |
| B57 | Tool stack per month | `=B53*B15+B10*B16/12+B17+B18` | 326.99 |
| B58 | One-time setup | `=(B53*B15+B17)*B19+B20` | 202.00 |
| B59 | One-time, per month | `=B58/B21` | 16.83 |
| B60 | Loaded cost per productive SDR FTE | `=((B23+B24*B25)*(1+B26)/12+B27*(1+B26)/12/B28)*B30/(B30-B29/2)` | 10,913.57 |
| B61 | SDR cost on this program | `=B60*B22` | 5,456.79 |
| B62 | AE loaded hour | `=B31*(1+B26)/B32` | 85.82 |
| B63 | AE cost per held meeting | `=B62*B33` | 85.82 |
| B64 | AE cost per opportunity | `=B62*B34` | 343.27 |
| B65 | Fixed monthly cost | `=B52+B57+B59+B61+B35` | 5,949.61 |
| B66 | Replies | `=B56*B36` | 108.05 |
| B67 | Positive replies (conversations) | `=B66*B37` | 37.82 |
| B68 | Meetings booked | `=B67*B38` | 18.91 |
| B69 | Meetings held | `=B68*B39` | 15.13 |
| B70 | Opportunities | `=B69*B40` | 9.08 |
| B71 | Deals | `=B70*B41` | 2.72 |
| B72 | AE time cost | `=B69*B63+B70*B64` | 4,413.53 |
| B73 | Total monthly program cost | `=B65+B72` | 10,363.14 |
| B74 | Loaded cost per lead pulled | `=B73/B5` | 2.30 |
| B75 | Data cost per verified email | `=(B46+B47)/B48` | 0.0103 |
| B76 | Cost per conversation | `=B73/B67` | 274.04 |
| B77 | Cost per meeting booked | `=B73/B68` | 548.09 |
| B78 | Cost per meeting held | `=B73/B69` | 685.11 |
| B79 | Cost per opportunity | `=B73/B70` | 1,141.85 |
| B80 | Cost per deal (CAC) | `=B73/B71` | 3,806.15 |
| B81 | Pipeline created | `=B70*B42` | 108,909.36 |
| B82 | Cost per $1 of pipeline | `=B73/B81` | 0.095 |
| B83 | New CAC ratio | `=B73/(B71*B42)` | 0.32 |
| B84 | Gross margin per deal per month | `=B42/12*B43` | 700.00 |
| B85 | CAC payback in months | `=B80/B84` | 5.44 |
| B86 | LTV to CAC | `=B84*B44/B80` | 4.41 |
| B87 | AE cost per deal (CAC floor) | `=B63/(B40*B41)+B64/B41` | 1,620.99 |
| B88 | Highest cost per booked meeting at a 12 month payback | `=B84*12*B39*B40*B41` | 1,209.60 |
| B89 | Break-even reply rate, 12 month payback | `=B65/(B56*(B37*B38*B39*B40*B41*B84*12-B37*B38*B39*B63-B37*B38*B39*B40*B64))` | 0.0111 |
| B90 | Break-even reply rate, 6 month payback | `=B65/(B56*(B37*B38*B39*B40*B41*B84*6-B37*B38*B39*B63-B37*B38*B39*B40*B64))` | 0.0291 |

Notes:

- B47 assumes every pulled lead has an email (`hasEmail: true` on the Lead Database). For Maps or Store Leads, multiply by the share of rows with an email.
- B52 assumes unused plan credits do not carry over; check the live pricing page.
- B56 caps contacts at mailbox capacity. If B48 is larger than B55, the extra valid emails wait for next month and are re-validated before they are sent. The sequencer tier caps it too: on Instantly Growth (5,000 emails and 1,000 uploaded contacts a month, instantly.ai/pricing) use `=MIN(B48,B55,1000,5000/B14)`; Hypergrowth allows 125,000 and 25,000.
- B60 treats the ramp as linear, so half the ramp months are lost output, spread over average tenure. Recruiting fees go in B35.
- B89 and B90 return a negative number or an error when the denominator is zero or below. That means AE cost per deal (B87) alone is above the CAC limit and no reply rate pays back: cut AE hours per opportunity, raise the win rate or raise ACV.
- B76 counts only positive email replies. Add phone conversations from `references/break-even-and-sensitivity.md` section 10 when the program calls.

## 4. Formulas that sit outside the sheet

```
Lifetime from churn:        lifetime months = 1 / monthly logo churn
Annual churn from monthly:  1 - (1 - monthly churn)^12      (2% a month compounds to 21.5% a year; 2% x 12 = 24% overstates it)
LTV:                        gross margin per deal per month x lifetime months
Pipeline velocity:          opportunities x ACV x win rate / sales cycle in days   (dollars of new ARR a day)
Max affordable cost per meeting booked = CAC limit x held rate x opportunity rate x win rate
Reverse sizing:             contacts needed = target meetings / (reply rate x positive share x meeting rate)
                            leads to pull = contacts / valid rate
                            mailboxes = contacts x touches / (sends per mailbox per day x business days), rounded up
                            domains = mailboxes / mailboxes per domain, rounded up
```

Steady state: the model prices one month of sends against the meetings, opportunities and deals those sends produce. Match the cost month to the cohort it contacted, never this month's cost to last month's deals.

## 5. CSV to paste

```csv
Label,Value
ScraperCity plan fee per month,149
Plan credits per month,159
Bonus on purchased credits,0.1
Leads pulled this month,4500
Catalog price per lead,0
Valid rate,0.7
Inputs sent to find_mobiles,300
Mobile Finder hit rate,0.4
Sending domains,5
Mailboxes per domain,3
Cold sends per mailbox per day,30
Business days per month,21
Touches per contact,3
Mailbox seat per month,7
Domain per year,12
Sequencer per month,97
Other tools per month,119.99
Warmup months,1
Other one-time setup,0
Months to spread one-time costs,12
SDR FTE on this program,0.5
SDR base,55000
SDR variable at target,25000
Share of variable paid,1
Employer cost on pay,0.19
SDR manager OTE,146000
SDRs per manager,6.4
SDR ramp months,3
SDR tenure months,22.8
AE OTE,150000
AE paid hours per year,2080
AE hours per held meeting,1
AE hours per opportunity,4
Other people cost per month,0
Reply rate,0.0343
Positive share of replies,0.35
Meetings per positive reply,0.5
Held rate,0.8
Opportunities per held meeting,0.6
Win rate,0.3
ACV,12000
Gross margin,0.7
Customer lifetime in months,24
Sales cycle in months,1
Lead cost at catalog price,=B5*B6
validate_emails cost,=B5*0.0072
Valid emails,=B5*B7
Mobiles found,=B8*B9
find_mobiles cost,=B49*0.25
Catalog-price spend,=B46+B47+B50
ScraperCity cash,"=B2+MAX(0,B51-B3)/(1+B4)"
Mailboxes,=B10*B11
Sends per month,=B53*B12*B13
New contacts per month at capacity,=B54/B14
Contacts emailed,"=MIN(B48,B55)"
Tool stack per month,=B53*B15+B10*B16/12+B17+B18
One-time setup,=(B53*B15+B17)*B19+B20
"One-time, per month",=B58/B21
Loaded cost per productive SDR FTE,=((B23+B24*B25)*(1+B26)/12+B27*(1+B26)/12/B28)*B30/(B30-B29/2)
SDR cost on this program,=B60*B22
AE loaded hour,=B31*(1+B26)/B32
AE cost per held meeting,=B62*B33
AE cost per opportunity,=B62*B34
Fixed monthly cost,=B52+B57+B59+B61+B35
Replies,=B56*B36
Positive replies (conversations),=B66*B37
Meetings booked,=B67*B38
Meetings held,=B68*B39
Opportunities,=B69*B40
Deals,=B70*B41
AE time cost,=B69*B63+B70*B64
Total monthly program cost,=B65+B72
Loaded cost per lead pulled,=B73/B5
Data cost per verified email,=(B46+B47)/B48
Cost per conversation,=B73/B67
Cost per meeting booked,=B73/B68
Cost per meeting held,=B73/B69
Cost per opportunity,=B73/B70
Cost per deal (CAC),=B73/B71
Pipeline created,=B70*B42
Cost per $1 of pipeline,=B73/B81
New CAC ratio,=B73/(B71*B42)
Gross margin per deal per month,=B42/12*B43
CAC payback in months,=B80/B84
LTV to CAC,=B84*B44/B80
AE cost per deal (CAC floor),=B63/(B40*B41)+B64/B41
Highest cost per booked meeting at a 12 month payback,=B84*12*B39*B40*B41
"Break-even reply rate, 12 month payback",=B65/(B56*(B37*B38*B39*B40*B41*B84*12-B37*B38*B39*B63-B37*B38*B39*B40*B64))
"Break-even reply rate, 6 month payback",=B65/(B56*(B37*B38*B39*B40*B41*B84*6-B37*B38*B39*B63-B37*B38*B39*B40*B64))
```

## 6. Cash tab (monthly billing)

Make a tab named `Cash` with headers in row 1: Month, Cash out, Margin in, Cumulative. Put `0` in A2 and `=A2+1` in A3 down to A38 (month 36).

| Column | Row 2 (month 0, warmup) | Row 3 and down |
|-|-|-|
| B, cash out | `=Model!B58` | `=Model!B73-Model!B59` |
| C, margin in | `0` | `=MAX(0,(A3-1)-MAX(1+Model!B45,A3-Model!B44)+1)*Model!B71*Model!B84` |
| D, cumulative | `=C2-B2` | `=D2+C3-B3` |

Column C counts the monthly cohorts already paying: a deal closed in month c pays from month c+1 for the lifetime in B44, and the first deals close in month 1 plus the sales cycle. Program cash break-even is the first month where column D turns positive; the lowest value in column D is the cash the program needs before then. For annual prepay, run `scripts/unit-economics-model.py my.json cash` with `"billing": "annual"` in the file: each deal then pays a year of margin up front.

Default results: monthly billing breaks even in month 14 with a low point of -$44,037.46 in month 7; annual prepay breaks even in month 4 with a low point of -$20,894.62 in month 2. The CAC payback of 5.44 months describes one deal. The cash curve describes the program, which keeps paying for new cohorts while each earlier one pays back in monthly installments.

## Sources

- https://scrapercity.com/pricing
- https://www.forentrepreneurs.com/saas-metrics-2/
- https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group
- https://www.bls.gov/news.release/ecec.t04.htm
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email
- https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- https://www.smartlead.ai/blog/how-many-cold-emails-per-day
