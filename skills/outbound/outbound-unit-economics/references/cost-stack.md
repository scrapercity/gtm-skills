# Cost Stack: People, Tools and One-Time Costs

Every dollar an outbound program spends in a month, split by how it behaves: fixed, one-time spread over months, or variable with meetings. ScraperCity prices live in `references/scrapercity-catalog.md`; this file covers the rest. Prices below are list prices checked on 2026-10-13. Use the user's own bills when they have them, and label any list price as a list price with its date.

## 1. SDR loaded cost

An SDR's salary is the smallest part of what the seat costs. Build it in four lines.

| Line | Formula | Default | Source |
|-|-|-|-|
| Pay | base + variable x share of variable paid | $55,000 + $25,000 x 1.0 | Bridge Group 2025 SDR report: $80K median OTE, split 68:32 ($55K base, $25K variable), unchanged since 2022 |
| Employer cost on pay | pay x 19% | $15,200 a year | BLS Employer Costs for Employee Compensation, June 2026, sales and related occupations (derivation below) |
| Manager share | manager OTE x 1.19 / 6.4 | $27,146.88 a year | Bridge Group 2025: SDR manager OTE $146K, 6.4 SDRs per first-line leader |
| Ramp | x tenure / (tenure - ramp / 2) | x 1.0704 | Bridge Group 2025: 3.0 month ramp, 1.9 year (22.8 month) tenure; linear ramp is a planning assumption |

Worked number per productive FTE per month:

```
pay with employer cost   ($55,000 + $25,000) x 1.19 / 12  = $7,933.33
manager share            $146,000 x 1.19 / 12 / 6.4       = $2,262.24
before ramp                                                 $10,195.57
after ramp               $10,195.57 x 22.8 / 21.3          = $10,913.57
```

So a full SDR costs about $10,900 a month before tools, and the salary line alone ($4,583.33) understates it by more than half. Recruiting fees, a signing bonus or a contractor margin go in "other people cost" spread over tenure.

**The 19% derivation.** BLS reports, for private industry sales and related occupations in June 2026, $26.99 an hour in wages and salaries, $2.11 paid leave, $1.05 supplemental pay, $2.16 insurance, $0.85 retirement and savings, and $2.69 payroll taxes (Social Security, Medicare, unemployment and workers' compensation). An annual salary already includes paid leave and supplemental pay, so the cost on top of pay is (2.16 + 0.85 + 2.69) / (26.99 + 2.11 + 1.05) = 5.70 / 30.15 = 18.9%, rounded to 19%. Total benefits over wages alone ($8.86 / $26.99) is 32.8%, and private industry across all occupations runs higher still (benefits were 30.0% of total compensation), but those ratios count paid leave and supplemental pay as cost on top of wages, which an annual salary or OTE already pays. Use 19% on salary or OTE over 2,080 paid hours, show the derivation in the Inputs row, and use the user's payroll data when they have it.

**What Bridge's other numbers do to the model.**

| Bridge Group 2025 figure | Model use |
|-|-|
| 60% of SDRs at quota | Lower "share of variable paid" below 1.0 when the team misses; it lowers cost and signals fewer meetings |
| Monthly quota of 10 held meetings (median, "Stage 0 held"), 6 converted ("Stage 1 converted") | Capacity check for SDRs who prospect by hand; 6 of 10 is the default opportunity rate (a ratio of two quota medians, not a measured conversion). Quotas are counted in held and converted meetings, so set the SDR's quota and variable pay on those, not on bookings |
| 40% median annual attrition | Each departure restarts a 3.0 month ramp. Put the team's own average tenure in the ramp factor; 1 / 0.40 gives 2.5 years, longer than Bridge's 1.9 year average, so the 22.8 month default is the safer figure when tenure is unknown |
| 1 SDR to 2.4 AEs | Check the AE hours the meetings will need (section 2) |
| Email-centric teams log 3.4 quality conversations a day (4.1 overall) | Context only. A quality conversation is not a positive email reply, so this does not size an SDR's reply capacity; take utilization from the SDR's logged hours |
| $3.78M raw pipeline per SDR a year | Compare to the model's pipeline created per SDR FTE x 12 |

Sample: 351 B2B companies, median revenue $47M and median ASP $50K, published February 2025. A small agency or a $5K ACV product sits far from that median, which is why every figure here is a default to replace.

## 2. AE time as a variable cost

First meetings and opportunities consume AE or founder hours, and those hours rise with every extra meeting. Leaving them out understates CAC most at high reply rates.

```
AE loaded hour            AE OTE x 1.19 / 2,080 paid hours
AE cost per held meeting  AE loaded hour x hours per held meeting      (prep, call, notes)
AE cost per opportunity   AE loaded hour x hours per opportunity       (proposal, follow-ups, close)
AE cost per deal          AE cost per held meeting / (opportunity rate x win rate) + AE cost per opportunity / win rate
```

Worked: $150,000 x 1.19 / 2,080 = $85.82 an hour. At 1 hour per held meeting and 4 per opportunity, with 60% of held meetings becoming opportunities and 30% of opportunities closing, AE time costs $85.82 / 0.18 + $343.27 / 0.30 = $1,620.99 per deal. That is a CAC floor: more replies spread the fixed costs thinner but never touch it. If it is above the CAC ceiling, no reply rate pays back.

Measure hours from the AE's calendar: count first meetings and opportunity calls, and add the prep and notes time logged around each.

## 3. Tool stack prices (list, checked 2026-10-13)

| Tool | Tier | Monthly billing | Annual billing (per month) | Limits that size the tier | Source |
|-|-|-|-|-|-|
| Google Workspace | Business Starter | $8.40 per user | $7.00 per user | Google's pricing page says annual saves 16%; dollar figures from a June 2026 pricing summary | workspace.google.com/pricing; emailvendorselection.com |
| Microsoft 365 | Business Basic | Not listed | $7.00 per user, paid yearly | Annual subscription | microsoft.com business plan comparison |
| Instantly | Growth | $47 | $37.60 | 5,000 emails and 1,000 uploaded contacts a month | instantly.ai/pricing |
| Instantly | Hypergrowth | $97 | $77.60 | 125,000 emails and 25,000 contacts a month | Same |
| Smartlead | Base | $39 | $32 | 6,000 emails and 2,000 active leads a month | smartlead.ai/pricing |
| Smartlead | Pro | $94 | $78 | 90,000 emails and 30,000 active leads a month | Same |
| LinkedIn Sales Navigator | Core | $119.99 | $89.99 ($1,079.88 a year) | Per license | business.linkedin.com compare plans |
| Domain | .com | User's registrar bill, often about $10 to $15 a year | | | User input |

Every sequencer listed above includes unlimited sending accounts, so the tier is set by emails and contacts a month. The model's sends per month (mailboxes x sends per day x business days) and contacts emailed must both fit. The worked example's 9,450 sends and 3,150 contacts fit Instantly Hypergrowth and Smartlead Pro. Instantly Growth binds on contacts first: 1,000 uploaded contacts of 3,150 is 31.7% of mailbox capacity (its 5,000 emails alone would allow 52.9%). Smartlead Base's 2,000 active leads and 6,000 emails both cap it at 63.5%.

**Monthly or annual.** Annual billing saves 16% (Workspace), 17% (Smartlead), 20% (Instantly) and 25% (Sales Navigator Core) and commits a year of cash. Price the program on monthly billing until measured cost per meeting holds, then switch the tools it keeps to annual.

## 4. Fixed, one-time and variable

| Behavior | Lines | How the model treats it |
|-|-|-|
| Fixed per month | ScraperCity plan, mailbox seats, domains (annual fee / 12), sequencer, Sales Navigator, SDR share, manager share | In the total whatever the reply rate |
| One-time | Warmup months (mailbox seats and sequencer paid before the first cold send), setup hours, extra domains bought ahead | Month 0 of the cash curve; spread over 12 months in unit costs |
| Variable with meetings | AE or founder hours per held meeting and per opportunity | Scales with the funnel; sets the CAC floor |
| Variable with volume | Catalog spend past plan credits (validation, mobiles, Apollo pulls) | Through the plan cash formula; zero extra cash while inside credits |

Warmup cost: Instantly's help center asks for at least 2 weeks of warmup before an account sends campaigns (3 weeks for its AirMail accounts), so the first month of mailbox and sequencer fees buys few or no meetings. The model counts warmup months as an input (1 here). For 15 mailboxes at $7.00 and a $97 sequencer that is $202.00, spread at $16.83 a month over a year.

Domain replacement: a domain that gets listed on a blocklist or loses inbox placement stops producing replies. Budget spare domains with warmed mailboxes at the rate the user has had to replace domains; move each to fixed cost when it goes live.

## 5. Allocating shared people and tools

Charge the program only what it uses, and say how the share was set.

| Shared item | Allocation key | Example |
|-|-|-|
| SDR who also works inbound | Hours on outbound replies and booking / total hours | 20 of 40 hours = 0.5 FTE |
| AE or founder | Hours per held meeting and per opportunity (section 2) | Never a flat share; it moves with meetings |
| CRM seats | Seats used by the outbound team x seat price | 1 SDR seat on a 10-seat plan |
| Sales Navigator, dialer | Licenses used for this program | 1 license |
| ScraperCity plan | Whole fee when the program is the main user; otherwise by catalog usage share | |

Keep company overhead (rent, finance, leadership) out of program CAC. Include it only when the user asks for a fully loaded company CAC, and then label it.

## 6. Ratios worth reporting

| Ratio | Formula | Worked example |
|-|-|-|
| Tools and data share of cost | (ScraperCity cash + tool stack + one-time per month) / total | ($149.00 + $326.99 + $16.83) / $10,363.14 = 4.8% |
| Tool cost per SDR FTE | Tool stack / SDR FTE | $326.99 / 0.5 = $653.98 |
| People share of cost | (SDR + AE time + other people) / total | ($5,456.79 + $4,413.53) / $10,363.14 = 95.2% |
| New CAC ratio | Total / new ARR from the month's deals | $10,363.14 / (2.72 x $12,000) = $0.32 |

Benchmarkit's 2025 report (2024 data, 583 B2B SaaS respondents) put the median New CAC ratio at $2.00 of sales and marketing spend per $1.00 of new customer ARR, across all channels and fully loaded. An outbound program modeled at $0.32 is either efficient or missing costs: check people and AE time first.

## Sources

- https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group
- https://www.bls.gov/news.release/ecec.t04.htm
- https://www.bls.gov/news.release/ecec.nr0.htm
- https://workspace.google.com/pricing
- https://www.emailvendorselection.com/google-workspace-pricing/
- https://www.microsoft.com/en-us/microsoft-365/business/compare-all-microsoft-365-business-products
- https://instantly.ai/pricing
- https://www.smartlead.ai/pricing
- https://business.linkedin.com/sales-solutions/compare-plans
- https://www.hibob.com/wp-content/uploads/2025-SaaS-Performance-Metrics-Benchmarks.pdf
- https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
