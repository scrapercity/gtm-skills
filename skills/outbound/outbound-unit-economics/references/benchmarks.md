# Benchmarks for the Model

Dated figures this skill may use as starting hypotheses, with their source, sample and limits. None of them is a forecast for a specific program. Replace each with the user's measured rate as soon as the sample in the last column is reached.

## 1. Email funnel

| Metric | Figure | Source, date | Sample and limits | Replace after |
|-|-|-|-|-|
| Average reply rate | 3.43% | Instantly 2026 Cold Email Benchmark Report, cited in Instantly's post of 30 Mar 2026 | Sample size not stated in the post | 1,000 contacts |
| Top quartile reply rate | 5.5% | Same | Same | 1,000 contacts |
| Elite reply rate | Over 10% | Same | Same | |
| Average reply rate | 4.1% | Hunter, The State of Cold Email 2025 | 11M cold emails sent in 2024 through Hunter | 1,000 contacts |
| Reply rate, campaigns of 50 or fewer recipients | 5.8% | Hunter 2025 | Same | |
| Reply rate, campaigns of 1,000+ recipients | 2.1% | Hunter 2025 | Same; large campaigns reply lower | |
| With follow-ups vs without | 4.9% vs 3.0% | Hunter 2025 | Same | |
| Positive share of replies | No published figure used | | Classify replies (`reply-handling`) and measure | 100 replies |
| Meetings per positive reply | No published figure used | | Measure | 30 positive replies |

## 2. Cost per meeting targets

| Segment | Target | Source, date | Limits |
|-|-|-|-|
| SMB (ACV under $25K) | Under $150 | Instantly post, 30 Mar 2026 | Defined as software, data and rep time divided by meetings; method behind the targets not described |
| Mid-market ($25K to $100K) | Under $250 | Same | Same |
| Enterprise (over $100K) | Under $350 | Same | Same |
| Cold email vs cold calling | $152.73 vs $2,777.78 per meeting | Same post, citing a separate Instantly article | Method not described on the page; a sequencer vendor comparing its own channel. Do not use as a forecast. |

## 3. Phone funnel

| Metric | Figure | Source, date | Limits |
|-|-|-|-|
| Per-dial connect rate | 9.9% | Belkins, 175,000+ dials in 2025 | Agency's own dialer data, B2B |
| Connect to conversation | 58% | Belkins 2025 | Same |
| Conversation to meeting | 4.6% | Belkins 2025 | Same |
| Conversation to meeting | 4.82% | Cognism with WHAM, 2024 figures | Agency data |
| Dials per meeting | About 370 to 379 | Belkins 2025 (370 stated; 379 from the three rates multiplied) | |

## 4. Payback and LTV

| Rule | Figure | Source | Use |
|-|-|-|-|
| LTV to CAC | Above 3; best businesses 7 to 8 | David Skok, SaaS Metrics 2.0 | Minimum test for recurring revenue |
| CAC payback | About 5 to 7 months; over 12 months weak | Same | 6 month target, 12 month ceiling |

## 5. ScraperCity figures (prices, not benchmarks)

| Item | Value | Source |
|-|-|-|
| `validate_emails` | $0.0072 per email | `references/scrapercity-catalog.md` |
| `find_emails` | $0.05 per email found, free if not found | Same |
| `find_mobiles` | $0.25 per number found, free if not found | Same |
| `scrape_apollo` | $0.0039 per lead | Same |
| `scrape_maps` | $0.0099 per business | Same |
| `scrape_store_leads` | $0.0039 per lead | Same |
| `scrape_website_finder` | $0.0499 per contact found | Same |
| `scrape_builtwith` (Tech Stack Search) | $4.99 per technology | Same |
| Plans | Starter $49 with $49 credits; Growth $149 with $159; Scale $649 with $800 | `references/scrapercity-platform.md` |
| Purchased credit bonus | Growth 10%, Scale 30% | Same |
| Mobile Finder coverage | 250M+ people, per scrapercity.com | Site claim; not a hit rate |

Hit rates for Email Finder and Mobile Finder vary by segment. Measure them on 100 records from the target list before budgeting more than the ceiling.

## 6. How to replace a benchmark with an actual

1. Run at least the sample in the "Replace after" column.
2. Compute the rate from the sequencer and CRM, using the same definitions as the model (reply excludes auto-replies and bounces; positive is interested, meeting request or referral).
3. Put the measured rate in the input cell, change its type to "measured" with the date range, and keep the benchmark in a note.
4. Re-run the sensitivity grid around the measured rate (half and double).

## Sources

- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email-2025
- https://belkins.io/blog/cold-calling-benchmarks
- https://www.cognism.com/cold-calling-report-2025
- https://www.forentrepreneurs.com/saas-metrics-2/
- https://scrapercity.com/pricing
- https://scrapercity.com/mobile-finder
