# Benchmarks for the Model

Dated figures this skill may use as starting hypotheses, with their source, sample and limits. Replace each with the user's measured rate, recording the sample size and date range beside it.

## 1. Email funnel

| Metric | Figure | Source, date | Sample and limits |
|-|-|-|-|
| Average reply rate | 3.43% | Instantly 2026 Cold Email Benchmark Report, cited in Instantly's post of 30 Mar 2026 | Sample size not stated in the post |
| Top quartile reply rate | 5.5% | Same | Same |
| Elite reply rate | Over 10% | Same | Same |
| Average reply rate per sequence | 4.5% | Hunter, State of Email Outreach 2026 | 31M emails sent through Hunter in 2025 |
| Reply rate, sequences of 21 to 50 recipients | 6.2% | Hunter 2026 | Same |
| Reply rate, sequences of 500+ recipients | 2.4% | Hunter 2026 | Same; large sequences reply lower, and the average sequence had 449 recipients |
| One message vs three | 3.3% vs 6.8% | Hunter 2026 | Same; replies fall past three follow-ups |
| Average reply rate, prior year | 4.1% | Hunter, State of Cold Email 2025 | 11M emails sent in 2024 |
| Positive share of replies | No published figure used | | Classify replies (`reply-handling`) and measure |
| Meetings per positive reply | No published figure used | | Measure |

A program that mails thousands of contacts a month is a 500+ recipient sender, so Hunter's 2.4% is the closer comparison for volume plans and Instantly's 3.43% the default. Run the sensitivity grid from 1.5% to 5.5%.

## 2. Meeting to opportunity to deal

| Metric | Figure | Source, date | Limits |
|-|-|-|-|
| Opportunities per held meeting | About 60% | Bridge Group 2025 SDR report: median monthly quota of 10 held meetings and 6 converted to stage 1 (ratio of the two medians) | Quotas, not measured outcomes; 351 companies with a $50K median ASP |
| Win rate | No published figure used | | The user's CRM history for outbound-sourced opportunities |
| Sales cycle | No published figure used | | Held meeting to signature from the CRM |

## 3. People cost

| Metric | Figure | Source, date | Limits |
|-|-|-|-|
| SDR OTE | $80K median, 68:32 base to variable | Bridge Group 2025 SDR Models and Metrics report (published 6 Feb 2025, 351 companies) | B2B companies with a $47M median revenue |
| SDR ramp | 3.0 months | Same | Lowest since 2010 |
| SDR tenure | 1.9 years | Same | |
| SDR attrition | 40% median a year | Same | 25th to 75th percentile 21% to 57% |
| SDRs at quota | 60% | Same | Lowest in the study's history |
| SDR manager OTE and span | $146K; 6.4 SDRs per leader | Same | Span is 3.6 below $5M revenue |
| SDR to AE ratio | 1 to 2.4 | Same | |
| Quality conversations per day | 4.1 overall; 3.4 on email-centric teams | Same | Not a count of positive email replies; do not size SDR reply capacity from it |
| Employer cost on pay, sales occupations | 19% (derived: $5.70 / $30.15 = 18.9%) | BLS Employer Costs for Employee Compensation, June 2026, sales and related | Insurance, retirement and payroll taxes over wages plus paid leave and supplemental pay. Benefits over wages alone is 32.8% because it counts paid leave, which a salary already pays; derivation in `references/cost-stack.md` |

## 4. Cost per meeting and market CAC

| Segment or metric | Figure | Source, date | Limits |
|-|-|-|-|
| SMB (ACV under $25K) | Under $150 per meeting | Instantly post, 30 Mar 2026 | Software, data and rep time divided by meetings; method behind the targets not described |
| Mid-market ($25K to $100K) | Under $250 | Same | Same |
| Enterprise (over $100K) | Under $350 | Same | Same |
| B2B outbound, any segment | $50 to $100 per meeting called "strong" | Instantly, cold outbound cost per meeting calculator post, 13 Nov 2025 | Counts software, domains, data and allocated SDR labor; no segment split. Quote it beside the 30 Mar 2026 targets, with each post's date, since the two differ |
| Cold email vs cold calling | $152.73 vs $2,777.78 per meeting | Same post, citing a separate Instantly article | Method not described; a sequencer vendor comparing its own channel. Do not use as a forecast. |
| New CAC ratio | $2.00 of S&M per $1.00 of new customer ARR (median) | Benchmarkit, 2025 B2B SaaS Performance Metrics Benchmarks (2024 data, 583 respondents) | All channels, fully loaded, company level |

## 5. Phone funnel

| Metric | Figure | Source, date | Limits |
|-|-|-|-|
| Per-dial connect rate | 9.9% | Belkins, 175,000+ dials in 2025 | Agency's own dialer data, B2B |
| Connect to conversation | 58% | Belkins 2025 | Same |
| Conversation to meeting | 4.6% | Belkins 2025 | Same |
| Conversation to meeting | 4.82% | Cognism with WHAM, 2024 figures | Agency data |
| Dials per meeting | About 370 to 379 | Belkins 2025 (370 stated; 379 from the three rates multiplied) | |
| Dials per day | 56 on phone-centric SDR teams, 28 on email-centric | Bridge Group 2025 | Medians |

## 6. Payback and LTV

| Rule | Figure | Source | Use |
|-|-|-|-|
| LTV to CAC | Above 3; best businesses 7 to 8 | David Skok, SaaS Metrics 2.0 | Minimum test for recurring revenue |
| CAC payback | About 5 to 7 months for the best; past 12 months weak | Same | 6 month target, 12 month ceiling |
| Monthly to annual churn | 1 - (1 - monthly)^12 | Arithmetic | 2% a month is 21.5% a year |

## 7. ScraperCity prices

| Item | Value | Source |
|-|-|-|
| `validate_emails` | $0.00169 per email | `references/scrapercity-catalog.md` |
| `find_emails` | $0.05 per email found, free if not found | Same |
| `find_mobiles` | $0.25 per number found, free if not found | Same |
| `scrape_apollo` | $0.0039 per lead | Same |
| `scrape_maps` | $0.0099 per business | Same |
| `scrape_store_leads` | $0.0039 per lead | Same |
| `scrape_website_finder` | $0.0499 per contact found | Same |
| Plans | Starter $49 with $49 credits; Growth $149 with $159; Scale $649 with $800 | `references/scrapercity-platform.md` |
| Purchased credit bonus | Growth 10%, Scale 30% | Same |
| Mobile Finder coverage | 250M+ people, per scrapercity.com | Site claim; not a hit rate |

Hit rates for Email Finder and Mobile Finder vary by segment. Measure them on a first batch from the target list before budgeting more than its ceiling.

## 8. How to replace a benchmark with an actual

1. Compute the rate from the sequencer and CRM, using the same definitions as the model (reply excludes auto-replies and bounces; positive is interested, meeting request or referral; an opportunity is a held meeting the AE accepts into the pipeline).
2. Put the measured rate in the input cell, change its type to "measured" with the sample size and date range, and keep the benchmark in a note.
3. Re-run the sensitivity grid around the measured rate (half and double) and the plan versus actual split (`references/break-even-and-sensitivity.md` section 9).

## Sources

- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://instantly.ai/blog/cold-outbound-cost-per-meeting-calculator/
- https://hunter.io/the-state-of-cold-email
- https://hunter.io/the-state-of-cold-email-2025
- https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group
- https://www.bls.gov/news.release/ecec.t04.htm
- https://www.hibob.com/wp-content/uploads/2025-SaaS-Performance-Metrics-Benchmarks.pdf
- https://belkins.io/blog/cold-calling-benchmarks
- https://www.cognism.com/cold-calling-report-2025
- https://www.forentrepreneurs.com/saas-metrics-2/
- https://scrapercity.com/pricing
- https://scrapercity.com/mobile-finder
