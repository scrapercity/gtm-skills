# Framework Notes: Outbound Unit Economics

Which named sources shape this skill, what each contributes, how strong the evidence is, and which file to open for each question.

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| ScraperCity catalog (npm `scrapercity` 1.0.17) and platform facts (scrapercity.com/pricing, checked 2026-10-12) | Per-result prices; plan fees and credits; purchased-credit bonuses; database access on Growth and up; Email Finder and Mobile Finder charge only on a find | Every data cost line, plan break-even | Vendor pricing |
| David Skok, SaaS Metrics 2.0 | LTV to CAC above 3; CAC recovery in about 5 to 7 months for the best, past 12 weak | CAC target and ceiling, payback test | Investor framework |
| The Bridge Group, 2025 SDR Models and Metrics report | SDR OTE and split, ramp, tenure, attrition, manager span and pay, held-meeting and opportunity quotas, activity per day | SDR loaded cost, opportunity rate, capacity checks | Survey of 351 B2B companies |
| U.S. Bureau of Labor Statistics, Employer Costs for Employee Compensation (June 2026) | Insurance, retirement and payroll taxes on top of pay for sales occupations (19%, derived; not the 32.8% of benefits over wages, which counts paid leave) | SDR and AE loaded cost | Federal statistics |
| Benchmarkit, 2025 B2B SaaS Performance Metrics | Median New CAC ratio of $2.00 per $1.00 of new ARR (2024 data) | Market comparison for the program's CAC | Survey of 583 companies |
| Instantly, 2026 benchmark report and March 2026 post | Average 3.43% reply rate, top quartile 5.5%; cost per meeting targets by segment | Reply rate default, targets | Vendor dataset, sample not stated |
| Instantly, cold outbound cost per meeting calculator (13 Nov 2025) | $50 to $100 per meeting called strong for B2B outbound, counting software, domains, data and allocated labor | Cost per meeting comparison | Vendor blog |
| Ryan Reisert, Buckets (GTMnow, November 2021) | Confirm a week out by phone, 12 to 24 hours by email, 2 to 3 hours by phone if no reply; no-shows return to Priority for a new time | Held-rate fix and its copy | Practitioner article |
| Ronen Pessar (The Sales Doctor ep. 43; Triple Session) | Qualify with a present-tense closed question; confirm the right person | Opportunity-rate fix: the question before the calendar link | Practitioner podcast and training |
| Hunter, State of Email Outreach 2026 and State of Cold Email 2025 | 4.5% average per sequence on 31M emails sent in 2025; 2.4% for 500+ recipients; 3.3% vs 6.8% for one vs three messages; 4.1% on 2024 sends | Sensitivity range, pitfalls | Vendor dataset |
| Vendor pricing pages (Google Workspace, Microsoft 365, Instantly, Smartlead, LinkedIn Sales Navigator), checked 2026-10-13 | Seat and tier prices, monthly vs annual, sequencer email and contact limits | Tool stack, sequencer fit | Vendor pricing |
| Belkins, cold calling benchmarks (2025 data); Cognism with WHAM (2024) | Dial funnel rates for the phone add-on | Phone section | Agency datasets |
| Alex Berman, alexberman.com | Judge by pipeline; count positive conversations and leave raw reply counts aside; 2 to 3 inboxes per sending domain | Positive share as its own input; cost per opportunity and pipeline; mailboxes per domain | Operator teaching |
| Instantly help center (account limits; when an account is ready for campaigns), checked 2026-10-13 | 30 campaign emails per account per day; at least 2 weeks of warmup before campaigns | Sends per mailbox input, warmup cost | Vendor documentation |
| Smartlead, How many cold emails per day (September 2026) | 50 cold emails per mailbox per day as the upper bound | Sensitivity on sends per mailbox | Vendor guide |

## Routing

| Question | Open |
|-|-|
| Which cell holds which input, and what is the formula? | `references/unit-economics-model.md` sections 2 and 3 |
| How do I check the spreadsheet or run a scenario? | `scripts/unit-economics-model.py` (commands listed in its header) |
| What does an SDR really cost? What do the tools cost? | `references/cost-stack.md` sections 1 and 3 |
| How do I count AE time, warmup and shared seats? | `references/cost-stack.md` sections 2, 4 and 5 |
| Which plan is cheapest at my usage? | `references/break-even-and-sensitivity.md` section 1 |
| What CAC, and what cost per meeting, can I afford? | `references/break-even-and-sensitivity.md` section 2 |
| What reply rate do I need? | `references/break-even-and-sensitivity.md` section 3 |
| How do cost per deal and per meeting move with the rates? | `references/break-even-and-sensitivity.md` sections 4 and 5 |
| Does more volume lower cost per meeting? | `references/break-even-and-sensitivity.md` section 6 |
| When does the program pay back in cash? | `references/break-even-and-sensitivity.md` section 7; `references/unit-economics-model.md` section 6 |
| How many leads and mailboxes for N meetings? | `references/break-even-and-sensitivity.md` section 8 |
| Actuals are off plan: which stage? | `references/break-even-and-sensitivity.md` section 9 |
| What does calling add? | `references/break-even-and-sensitivity.md` section 10 |
| Which fix for which stage, with copy? | `references/break-even-and-sensitivity.md` section 12 |
| Where does each benchmark come from and when to replace it? | `references/benchmarks.md` |
| Exact tool prices | `references/scrapercity-catalog.md` |

## Where sources differ, and the rule used here

| Topic | Sources | Rule here |
|-|-|-|
| Average reply rate | Instantly 3.43% (2026 report); Hunter 4.5% per sequence on 2025 sends, 2.4% for 500+ recipients | Default 3.43%, sensitivity from 1.5% to 5.5% |
| Cost per meeting | Instantly targets under $150 to $350 by ACV segment (30 Mar 2026) and calls $50 to $100 strong (13 Nov 2025), both counting software, data and rep time; this model also counts manager, ramp and AE time | Quote the post used, with its date; compare on the same definition; decide on the full one |
| Payback | Skok 5 to 7 months for the best, 12 months weak; Benchmarkit's median New CAC ratio of $2.00 implies about 34 months at 70% gross margin | 6 month target, 12 month ceiling; the market median is a floor for comparison, never a target |
| Employer cost on pay | BLS: benefits 30.0% of total compensation for all private workers; sales and related benefits are 32.8% of wages alone, 19% on top of pay once paid leave and supplemental pay are counted as pay | 19% for SDRs and AEs on salary or OTE, derivation shown in the Inputs row, unless payroll data says otherwise |
| SDR ramp cost | Bridge: 3.0 month ramp, 1.9 year tenure | Linear ramp, half the ramp months lost, spread over tenure |
| Opportunity rate | Bridge quotas: 6 converted per 10 held | 60% default; replace with the measured rate |
| Unused credits | Not stated in the platform facts file | Assume they do not carry over; check the pricing page |
| Positive share, meeting rate, win rate | No published source used | Labeled assumptions; measure |
| How busy the SDR is | Bridge 3.4 quality conversations a day measures calls and conversations, not reply handling | The SDR's logged hours; never infer utilization from a benchmark |

## Sources

- https://scrapercity.com/pricing
- https://www.npmjs.com/package/scrapercity
- https://www.forentrepreneurs.com/saas-metrics-2/
- https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group
- https://www.bls.gov/news.release/ecec.t04.htm
- https://www.hibob.com/wp-content/uploads/2025-SaaS-Performance-Metrics-Benchmarks.pdf
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email
- https://hunter.io/the-state-of-cold-email-2025
- https://instantly.ai/pricing
- https://instantly.ai/blog/cold-outbound-cost-per-meeting-calculator/
- https://gtmnow.com/buckets-lead-generation-method/
- https://www.thesalesdocrx.com/podcast/episode-43-cold-calling-techniques-that-work-with-ronen-pessar
- https://www.smartlead.ai/pricing
- https://business.linkedin.com/sales-solutions/compare-plans
- https://belkins.io/blog/cold-calling-benchmarks
- https://www.cognism.com/cold-calling-report-2025
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://alexberman.com/cold-email-fewer-sends-higher-reply-rates
- https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- https://www.smartlead.ai/blog/how-many-cold-emails-per-day
