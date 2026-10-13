# Framework Notes: Outbound Unit Economics

Which named sources shape this skill, what each contributes, how strong the evidence is, and which file to open for each question.

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| ScraperCity catalog (npm `scrapercity` 1.0.17) and platform facts (scrapercity.com/pricing, checked 2026-10-12) | Per-result prices; plan fees and credits; purchased-credit bonuses; database access on Growth and up; Email Finder and Mobile Finder charge only on a find | Every cost line, plan break-even | Vendor pricing |
| David Skok, SaaS Metrics 2.0 | LTV to CAC above 3; CAC recovery in about 5 to 7 months, over 12 weak | CAC target and ceiling, payback test | Investor framework |
| Instantly, 2026 benchmark report and March 2026 post | Average 3.43% reply rate, top quartile 5.5%; cost per meeting targets by segment | Reply rate default, targets | Vendor dataset, sample not stated |
| Hunter, The State of Cold Email 2025 | 4.1% average reply on 11M emails sent in 2024; 2.1% for 1,000+ recipient campaigns; follow-ups 4.9% vs 3.0% | Sensitivity range, pitfalls | Vendor dataset |
| Belkins, cold calling benchmarks (2025 data) | Dial funnel rates for the phone add-on | Phone section | Agency dataset |
| Cognism with WHAM, State of Cold Calling 2025 | 4.82% conversation to meeting (2024) | Phone cross-check | Agency dataset |
| Alex Berman, alexberman.com | Judge by pipeline; count positive conversations and leave raw reply counts aside | Positive share as its own input | Operator teaching |
| `references/deliverability-primer.md` | 30 cold sends per mailbox per day house cap, 2 to 3 mailboxes per domain | Capacity inputs | Repo standard |

## Routing

| Question | Open |
|-|-|
| Which cell holds which input, and what is the formula? | `references/unit-economics-model.md` section 3 |
| What default should I use, and is it a fact or an assumption? | `references/unit-economics-model.md` section 2 |
| How do I check the spreadsheet? | `references/unit-economics-model.md` section 5 |
| Which plan is cheapest at my usage? | `references/break-even-and-sensitivity.md` section 1 |
| What CAC can I afford at my ACV? | `references/break-even-and-sensitivity.md` section 2 |
| What reply rate do I need? | `references/break-even-and-sensitivity.md` section 3 |
| How does cost per deal move with reply and close rates? | `references/break-even-and-sensitivity.md` sections 4 and 5 |
| What does calling add? | `references/break-even-and-sensitivity.md` section 6 |
| Where does each benchmark come from and when to replace it? | `references/benchmarks.md` |
| Exact tool prices | `references/scrapercity-catalog.md` |

## Where sources differ, and house choices

| Topic | Sources | Rule here |
|-|-|-|
| Average reply rate | Instantly 3.43% (2026 report); Hunter 4.1% (2024 sends) | Default 3.43%, sensitivity from 1.5% to 5.5% |
| Cost per meeting | Instantly targets $150 to $350 by segment; its own cold email vs calling comparison lacks a stated method | Use targets as a comparison line only |
| Payback | Skok 5 to 7 months target, 12 months weak | 6 month target, 12 month ceiling |
| Unused credits | Not stated in the platform facts file | Assume they do not carry over; check the pricing page |
| Positive share and meeting rate | No published source used | Labeled assumptions; measure |

## Sources

- https://scrapercity.com/pricing
- https://www.npmjs.com/package/scrapercity
- https://www.forentrepreneurs.com/saas-metrics-2/
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email-2025
- https://belkins.io/blog/cold-calling-benchmarks
- https://www.cognism.com/cold-calling-report-2025
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://alexberman.com/cold-email-fewer-sends-higher-reply-rates
