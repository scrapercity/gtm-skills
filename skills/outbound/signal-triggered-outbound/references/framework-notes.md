# Framework Notes: Signal-Triggered Outbound

Which named sources shape this skill, what each contributes, how strong the evidence is, and which file to open for each question.

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| Craig Elias, "Leveraging Trigger Events" (InsideSales, Sep 2013) | Three buying modes (status quo, window of dissatisfaction, searching for alternatives); trigger events as funnel fillers, movers and shakers; first viable vendor in the window wins, citing a 74% close ratio attributed to Forrester | Why speed and half-life exist; tier A SLA | Practitioner teaching citing third-party research |
| Alex Berman, alexberman.com | Targeting and offer before copy; a dated reason in the first line connected to the offer; a roundup on his site reports trigger-based lists out-replying bought lists (self-reported) | Angle rules, offer fit per signal | Operator teaching |
| `references/cold-email-frameworks.md` section 8 | Trigger table for ScraperCity tools; skip stale or unverifiable triggers | Signal list, max age | Shared repo reference |
| ScraperCity platform and package docs (npm `scrapercity` 1.0.17, scrapercity.com/llm-info) | `excludeDelivered`, free re-fetch of owned database records, 100,000 new records a day, Store Leads `offset` and `nextOffset`, BizBuySell `datasetName` dedupe, Distress List `maxItems` up to 500, webhooks on SUCCEEDED or FAILED | Repeat pull design and cost | Vendor documentation |
| FCC 47 CFR 64.1200 and FTC TSR | Consumer phone rules for distress outreach | S11 compliance | Federal regulation |
| CFPB Regulation O, 12 CFR 1015 | Mortgage assistance relief: no advance fees, disclosures | S11 angle limits | Federal regulation |
| n8n documentation | Schedule Trigger, HTTP Request and Webhook nodes | Recipes | Vendor documentation |

## Routing

| Question | Open |
|-|-|
| Which signals can ScraperCity show, and how is each detected? | `references/signal-catalog.md` |
| What half-life and max age for this signal? | `references/signal-catalog.md` summary table |
| How do I score and tier? What are the SLAs? | `references/scoring-and-freshness.md` |
| How do I schedule the pull and diff snapshots? | `references/repeat-pull-recipes.md` sections 1 to 5 |
| How do webhooks fit? | `references/repeat-pull-recipes.md` section 6 |
| What does each recipe cost per month? | `references/repeat-pull-recipes.md` section 7 |
| How do I write the first line for a trigger? | `references/cold-email-frameworks.md` section 8 |
| Can I call pre-foreclosure owners? | `references/outbound-compliance-primer.md` sections 3, 4 and 10 |
| Tool parameters and prices | `references/scrapercity-catalog.md` |

## Where sources differ, and house choices

| Topic | Position | Rule here |
|-|-|-|
| How fast to act | Elias: be first in the window; no source gives a day count for these signals | Tier A within 2 business days of detection; re-fit after data |
| Half-life values | No published decay rates for these signal types | House starting values per signal, dated 2026-10; re-fit by age bucket after 200 contacts |
| "New business" | `excludeDelivered` returns records new to the account and carries no opening date | New listing requires 5 or fewer reviews and absence from the prior snapshot |
| Removal signals | Detection tools miss scripts at times | Two consecutive absent pulls plus a manual site check for tier A |
| Funding, hiring, job change triggers | Common in trigger selling; not visible in ScraperCity tools | Out of scope unless the user supplies the source, labeled in the queue |

## Sources

- https://www.insidesales.com/leveraging-trigger-events/
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://alexberman.com
- https://scrapercity.com/llm-info
- https://scrapercity.com/api-docs
- https://www.npmjs.com/package/scrapercity
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
