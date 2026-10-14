# Framework Notes: Signal-Triggered Outbound

Which named sources shape this skill, what each contributes, how strong the evidence is, and which file to open for each question.

## Authorities

| Authority | Contribution | Used in | Evidence type |
|-|-|-|-|
| Craig Elias, "Leveraging Trigger Events" (InsideSales, Sep 2013) | Three buying modes (status quo, window of dissatisfaction, searching for alternatives); trigger events as funnel fillers, movers and shakers; first viable vendor in the window wins, citing a 74% close ratio attributed to Forrester | Why speed and half-life exist | Practitioner teaching citing third-party research |
| Instantly, email sequence benchmarks 2026 (March 2026) | 3.43% average reply rate; 58% of replies on step 1; 4 to 7 emails over 14 to 21 days, first follow-up 2 to 3 days later, later ones 4 to 7 days apart; pause two to three months before re-engaging | Touch spacing, cool-down, static baseline | Vendor dataset |
| Hunter, The State of Cold Email | 4.5% reply rate across 31 million sequence emails sent in 2025; 3% for sales outreach sequences | Static baseline (3% for a sales program) | Vendor dataset |
| G2 Buyer Intent documentation (checked 2026-10-13) | Signal types (profile, pricing, category, alternatives, compare, competitive), buying stage and activity level updated daily, CSV export, email alerts, integrations; signals depend on the G2 plan | S27 | Vendor documentation |
| NAMM Show suitcasing and unauthorized solicitation policy (checked 2026-10-13) | Exhibitors may not solicit in aisles or other exhibitors' booths; non-exhibitors may not solicit at the show | S26 exhibitor play: ask the sales leader for a meeting after the show | Event organizer rules |
| RB2B pricing page (checked 2026-10-13) | Free $0 with 150 monthly resolutions, Starter $79 a month with 300, Pro from $149, Pro+ from $199 | Pricing the S14 feed | Vendor pricing page |
| layoffs.fyi | Tracks tech startup layoffs; data free to use with attribution | Negative signal detection | Public tracker |
| Alex Berman, alexberman.com | Targeting and offer before copy; a dated reason in the first line connected to the offer; a roundup on his site reports trigger-based lists out-replying bought lists (self-reported) | Angle rules, offer fit per signal | Operator teaching |
| `references/cold-email-frameworks.md` section 8 | Trigger table for ScraperCity tools; skip stale or unverifiable triggers | Signal list, max age | Shared repo reference |
| ScraperCity platform and package docs (npm `scrapercity` 1.0.17, scrapercity.com/llm-info) | `excludeDelivered`, free re-fetch of owned database records, 100,000 new records a day, Store Leads `offset` and `nextOffset`, BizBuySell `datasetName` dedupe, Distress List `maxItems` up to 500, webhooks on SUCCEEDED or FAILED | Repeat pull design and cost | Vendor documentation |
| n8n documentation | Schedule Trigger, HTTP Request and Webhook nodes | Recipes | Vendor documentation |
| Jordan Crawford, Blueprint GTM (blueprintgtm.com) | Pain-Qualified Segment: prospects grouped by a specific, data-detectable problem they have now | Signal design: each signal must be a detectable event tied to a problem the offer fixes | Practitioner teaching |
| RB2B, Vector, Warmly, UserGems, Crunchbase, Trigify (vendor sites, checked 2026-10-13) | What each outside signal tool detects; RB2B and Vector state person-level ID is US-only; RB2B's past-customer guide (May 2026) opens sample messages with the visit; Trigify's shutdown date; UserGems' signal list (departures from customers, earnings, product launches, event attendees) and its first-90-days claim for new executives | S14 to S28 in the signal catalog | Vendor documentation |
| EDGAR full-text search and APIs (sec.gov), SEC webmaster FAQ, Form D form, investor.gov bulletins on the 8-K and 10-K | Free JSON search by form, state and CIK with `items` on 8-Ks; 10 requests a second and a User-Agent with contact email; Form D items (Industry Group, Type of Filing, Related Persons, amounts) and its 15-day filing window; 8-K Item 2.02 and 5.02 names and the four-business-day window; Item 1A order and Item 7 content | S20, S22, S23 detection and the earnings play | Primary publisher documentation |
| Greenhouse, Ashby and Lever job board API docs | Public, unauthenticated job lists and their date fields (`updated_at` and `first_published`, `publishedAt`, none for Lever) | S18 detection | Vendor documentation |
| Octolens, F5Bot, changedetection.io, GlobeNewswire RSS list, Product Hunt API docs | Social and mention monitoring sources and prices; open-source page monitoring with webhooks; press feeds by subject and industry only; Product Hunt API token and commercial-use limit | S19, S24, S25 detection | Vendor documentation |
| LinkedIn Sales Navigator how-to page | Saved leads trigger alerts when they change jobs; account pages show decision makers who joined or left | S16 and S20 fallback detection | Vendor documentation |

## Routing

| Question | Open |
|-|-|
| Which signals can ScraperCity show, and how is each detected? | `references/signal-catalog.md` |
| What half-life and max age for this signal? | `references/signal-catalog.md` summary table |
| How do I score and tier? What are the SLAs? | `references/scoring-and-freshness.md` |
| How do I schedule the pull and diff snapshots? | `references/repeat-pull-recipes.md` sections 1 to 5 |
| How do webhooks fit? | `references/repeat-pull-recipes.md` section 6 |
| How do I score website visits, job changes, funding, hiring, filings, launches, events or social engagement? | `references/signal-catalog.md` S14 to S28 |
| Who do I contact for each outside signal, on what days, with what email? | `references/signal-plays.md` |
| How do I pull Form D, 8-K, job board and page monitor feeds on a schedule? | `references/repeat-pull-recipes.md` section 10 |
| How do signals stack, and which ones cannot reach tier A alone? | `references/scoring-and-freshness.md` section 1 |
| What can I say to someone whose visit we identified? | `references/signal-catalog.md`, website visitor coverage for S14 and S15 |
| Which events lower a score? | `references/signal-catalog.md`, Negative signals |
| Which accounts never get scored? | `references/scoring-and-freshness.md` section 5a |
| How fast should each tier be worked? | `references/scoring-and-freshness.md` section 5 |
| How urgent is each kind of social engagement? | `references/repeat-pull-recipes.md` section 8 |
| What does the owner alert contain? | `references/repeat-pull-recipes.md` section 9 |
| What does each recipe cost per month? | `references/repeat-pull-recipes.md` section 7 |
| How do I write the first line for a trigger? | `references/cold-email-frameworks.md` section 8 |
| Tool parameters and prices | `references/scrapercity-catalog.md` |

## Where sources differ, and program settings

| Topic | Position | Rule here |
|-|-|-|
| How fast to act | Elias: be first in the window; no source gives a day count for these signals | The program sets each tier's touch window and measures meeting rate by days to first touch |
| Half-life values, base points, score weights, tier cut-offs | No published values for these signal types | Settings each program writes down and re-fits by age bucket from its own meeting rate |
| "New business" | `excludeDelivered` returns records new to the account and carries no opening date | New listing requires a review count at or under the program's cap and absence from the prior snapshot |
| Removal signals | One absent pull can be a detection miss | Confirm on the next pull or by loading the site before a tier A touch |
| Funding, hiring, filing, launch, event, visit, social, intent and webinar triggers | Common in trigger selling; not visible in ScraperCity tools | Scored as S14 to S28 from free feeds or the user's tools, labeled `other source`; job changes and new leaders can also come from a Lead Database re-pull |
| How fast to touch a funding or job-change signal | Windows such as 48 hours or day 14 to 21 circulate in vendor blog posts; none could be traced to a primary report with a method (checked 2026-10-13) | Program-set windows measured by age bucket; only UserGems' first-90-days claim is cited, as a vendor claim |
| Form D as a trigger | A national EDGAR query for 2026-10-01 to 2026-10-09 returned 2,054 Form D filings, the first page angel fund series | Filter by state, drop funds, and optionally cap the signal so it needs a second one for tier A |
| Naming the visit in S14 copy | RB2B's past-customer guide opens with the visit; no study compares visit and fit lines | Split test per program |
| Speed for first-party visits | No published benchmark found for minutes-to-touch on identified visits | Program-set window, measured by minutes to first touch |

## Sources

- https://www.insidesales.com/leveraging-trigger-events/
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://alexberman.com
- https://scrapercity.com/llm-info
- https://scrapercity.com/api-docs
- https://www.npmjs.com/package/scrapercity
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
- https://www.blueprintgtm.com/
- https://www.rb2b.com/
- https://learn.vector.co/articles/5062232408-faq-help-center
- https://www.warmly.ai/
- https://www.usergems.com/
- https://www.trigify.io/
- https://www.usergems.com/product/signals
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/about/webmaster-frequently-asked-questions
- https://www.sec.gov/files/formd.pdf
- https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read-8
- https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read
- https://developers.greenhouse.io/job-board.html
- https://developers.ashbyhq.com/docs/public-job-posting-api
- https://github.com/lever/postings-api
- https://octolens.com/
- https://f5bot.com/
- https://github.com/dgtlmoon/changedetection.io
- https://www.globenewswire.com/rss/list
- https://api.producthunt.com/v2/docs
- https://business.linkedin.com/sales-solutions/sales-navigator/how-to-use-linkedin-sales-navigator
- https://www.rb2b.com/learn/how-to-re-engage-past-customers-who-visit-your-website-again
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email
- https://documentation.g2.com/docs/buyer-intent
- https://www.namm.org/thenammshow/info/SuitcasingUnauthorizedSolicitation
- https://www.rb2b.com/pricing
- https://layoffs.fyi/
