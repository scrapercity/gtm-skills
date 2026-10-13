---
name: icp-list-builder
description: >-
  Turns 3-5 example customers into Lead Database filters, shows the match count
  before pulling, pages the results with after cursors, normalizes, dedupes,
  suppresses and validates every email, and delivers a CSV of send-ready
  contacts with a funnel that accounts for every dropped row. Use when the user
  says "build me a list like these customers", "find more companies like X",
  "pull VP Sales at 50-200 person SaaS", "lookalike list", or "ICP list".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [icp, lookalike, lead-database, list-building, email-validation, b2b]
  related_skills: [tam-builder, decision-maker-finder, cold-email-list, email-list-cleaner, crm-enricher, scrapercity-lead-database, cold-email-strategy]
  frameworks:
    - "April Dunford - best-fit customers as the source of targeting"
    - "Gartner - B2B buying groups of 6 to 10 decision makers"
    - "Alex Berman - narrow, case-study-shaped cold email lists"
    - "Google, Yahoo and Microsoft - bulk sender requirements (2024-2025)"
    - "FTC - CAN-SPAM Act compliance guide"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, outbound-compliance-primer.md]
---

# ICP List Builder

## Overview

This skill produces one file: a CSV of contacts who look like the user's best customers, every email validated, plus a short report with the filters used, the match count, the funnel from matched to send-ready, and the cost.

It prevents the most expensive list mistake: describing an ICP in adjectives ("mid-market tech companies, decision makers") and pulling whatever the database returns. That list bounces, reaches assistants and interns, and burns domains. This skill derives filters from evidence (the 3-5 customers who bought fastest and got the most value), checks the count before spending, and refuses to hand over a row that has not passed `references/list-quality-standard.md`.

## When to Use

- "Here are 5 of our best customers, build me a list of more like them."
- "Pull VP Sales at 50-200 employee SaaS companies in the US."
- "I need 2,000 leads for a campaign, here's who we sell to."
- "Lookalike list", "ICP list", "target account contacts".
- A cold email plan exists and needs its list.

Use a different skill when:

| The user wants | Use |
|-|-|
| Every company in a market, sized, with no contact pull yet | `tam-builder` |
| The right buyers at a named list of companies or domains | `decision-maker-finder` |
| Local businesses by category and city (dentists, roofers) | `local-business-list` |
| A send-ready file from domains or an existing ICP, through to sequencer import | `cold-email-list` |
| To clean a list they already have | `email-list-cleaner` |
| Shopify or WooCommerce stores filtered by apps or tech | `ecommerce-by-techstack` |

## Prerequisites

Collect these before the first call. Mark anything missing as "unknown" and say which default you used.

| Input | Why | Default if unknown |
|-|-|-|
| 3-5 best-fit customer domains | Source of every filter | Ask; do not proceed on adjectives alone |
| What the product does, in one line | Picks the department and titles | Ask |
| Target row count | Sets pages and cost | 1,000 send-ready |
| Geography | Person country and law | United States |
| Suppression files (customers, open deals, past sends, unsubscribes) | Section 7 of the quality standard | None supplied; say so in the report |
| Plan level | Lead Database needs Growth ($149/mo) or Scale | Run `check_wallet` and read the plan |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| April Dunford, positioning work on best-fit customers | Start from the customers who understood the product fastest and got the most value, then find the traits they share. The filters come from those accounts, not from every customer on the books. |
| Gartner B2B buying research | A complex purchase involves a buying group of roughly 6 to 10 people. Pull 2-3 roles per account (economic buyer, operator, user lead), not one title. |
| Alex Berman (X27, ScraperCity) | Narrow lists shaped like a case study outperform broad ones. His early university campaign targeted about 50 accounts that resembled one result. Prefer 1,500 tight contacts over 15,000 loose ones. |
| Google, Yahoo, Microsoft sender requirements (Feb 2024, May 2025) | Remove invalid recipients, keep complaints under 0.3% (Google targets under 0.1%). A list is only send-ready after validation. |
| FTC CAN-SPAM guide | No B2B exemption; honor opt-outs within 10 business days. Suppression runs before every pull is delivered. |
| `references/list-quality-standard.md` | Required columns, normalization, dedupe keys, validation buckets, acceptance thresholds. |

Details and when to open each file: `references/framework-notes.md`.

## Workflow

### 1. Profile the example customers

For each of the 3-5 domains, call `query_lead_database` with `companyDomain` and `limit: 5` to read firmographics from returned rows (industry, employee count, revenue, HQ location, keywords). Record them in the ICP table. Look for the shared traits:

| Trait | Rule for turning it into a filter |
|-|-|
| Employee count | Take min and max of the examples, widen each side by about 30%, round to a standard band (1-10, 11-50, 51-200, 201-500, 501-1,000, 1,001-5,000). |
| Industry | Use the label that 3 or more examples share. If they disagree, use `keywords` instead. |
| Keywords | Pick 2-4 tags that appear on 3+ examples and describe the business model (saas, b2b, marketplace, fintech). |
| Revenue | Only if the user sells by revenue tier; revenue fields are sparser than headcount. |
| HQ location | `companyCountry` when the seller can only serve some countries; `country` for where the person sits. |
| Buyer titles | Ask who signed and who used it at each example; map to a title family in `references/title-synonyms-and-exclusions.md`. |

If fewer than 3 examples share a trait, leave it out. One outlier customer should not shape the list.

### 2. Draft filters and pick a recipe

Start from the closest recipe in `references/icp-filter-recipes.md` (36 recipes by vertical and buyer), then swap in the traits from step 1. Always add:

- `hasEmail: true` for email campaigns.
- `notTitle` from the exclusion set for the title family (assistant, intern, former, etc.).
- `notIndustry` or `notKeywords` for segments the user cannot serve (agencies, staffing, government).

### 3. Count before pulling

Run the draft with `limit: 1`. Read `pagination.total`. Decide with this table:

| `pagination.total` vs target send-ready rows | Action |
|-|-|
| Under 50% of target | Widen: add title synonyms, widen headcount one band, drop the weakest keyword, add a neighboring country. Recount. |
| 50% to 150% of target | Show the user the count and cost, then pull everything. |
| 150% to 1,000% of target | Pull the target plus 40% headroom for drops (validation, dedupe, suppression), or tighten. |
| Over 10x target | Tighten: add seniority, narrow headcount, add `keywords`, split by state. Recount. |
| 0 | Remove one filter at a time until the count returns; the last removed filter is spelled differently in the database. Check `search_translation` if you used `url`. |
| 503 error | The search ran too long. Add a location, a size band, or fewer titles, then retry. |

Show the user: filters, total, rows you plan to pull, and estimated validation cost. Wait for a go-ahead when the paid part exceeds $5.

### 4. Pull with cursor paging

Call `check_wallet`. Then page with `after`: first call `after: "0"`, `limit: 100`, then pass each response's `pagination.next_after` until it is null or you have the planned rows. Add `excludeDelivered: true` if the account has pulled this ICP before and only new people are wanted. Keep the filters identical across pages. The full loop and failure handling are in `references/count-and-paging-runbook.md`.

### 5. Normalize, dedupe, suppress

Map each returned field to the person schema in `references/list-quality-standard.md` section 2a. Normalize names, emails, phones (E.164), titles and domains per section 3. Dedupe on email, then LinkedIn URL, then first + last + domain. Apply suppression in this order: unsubscribes, bounces, complaints, current customers, open opportunities, competitors, contacted in the last 90 days. Count every drop by reason.

### 6. Validate

Send every remaining email to `validate_emails`. Poll `check_run_status` every 30-60 seconds (validation finishes in minutes), then `download_results`. Map raw results into the buckets: valid, catch_all, unknown, invalid, disposable. Only `valid` goes into the main CSV; catch-all and unknown go into a side file with the rules from the standard.

### 7. Cap per account and deliver

Keep at most 3 contacts per `company_domain`, preferring the highest seniority, then the closest title match. Write the CSV, the side file, and the report from `templates/output-template.md`. Run `scripts/check-output.py` on the report.

## ScraperCity Implementation

### Tools used

| Step | Tool | Price (catalog) |
|-|-|-|
| Plan and balance | `check_wallet` | Free |
| Profile examples, count, pull | `query_lead_database` | Included on Growth ($149/mo) and Scale; 100,000 new leads a day; re-fetching leads you already have is free |
| Validate | `validate_emails` | $0.0072 per email |
| Poll and fetch | `check_run_status`, `download_results` | Free |
| Fill a missing email for a high-value contact | `find_emails` | $0.05 per email found, free if not found |

### Count call (MCP)

```json
{
  "title": "VP Sales, Vice President of Sales, VP of Sales, Head of Sales, Chief Revenue Officer, CRO",
  "notTitle": "assistant, intern, former, retired, advisor, board, investor, operations, enablement, engineer",
  "keywords": ["saas", "b2b"],
  "minEmployees": 50,
  "maxEmployees": 200,
  "country": ["United States"],
  "hasEmail": true,
  "limit": 1
}
```

Read `pagination.total` from the response. Seniority can replace part of the title list: `"seniority": ["vp", "c_suite"]` with `"department": ["sales"]`. The tool documents `vp`, `director` and `c_suite` as seniority values and `sales` and `engineering` as departments; confirm any other value with a `limit: 1` call and read the returned rows before relying on it.

### Pull loop (MCP)

```text
after = "0"
while rows < planned:
    r = query_lead_database({...same filters..., "limit": 100, "after": after})
    rows += r.data
    after = r.pagination.next_after
    if after is null: break
```

### REST equivalents (Clay, n8n, scripts)

```bash
curl -s -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
  "https://app.scrapercity.com/api/v1/database/leads?title=VP%20Sales,Head%20of%20Sales,CRO&keywords=saas&minEmployees=50&maxEmployees=200&country=United%20States&hasEmail=true&limit=100&after=0"
curl -s -X POST -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"emails":["dana@ledgerline.example"]}' https://app.scrapercity.com/api/v1/scrape/email-validator
```

Then `GET /api/v1/scrape/status/{runId}` until SUCCEEDED and `GET /api/downloads/{runId}` for the CSV. Use `POST /api/v1/database/leads` with a JSON body for long title lists or a long `url`. The CLI commands are `db-leads`, `email-validate`, `poll` and `download`; flags are listed in the `scrapercity-cli` skill.

### Worked cost estimate

Target: 1,500 send-ready VP Sales contacts. Count returned 3,412. Plan to pull 2,000 (target plus about 33% headroom).

| Item | Units | Unit price | Cost |
|-|-:|-:|-:|
| Lead Database pull, 20 pages of 100 | 2,000 leads | Included in Growth plan | $0.00 |
| Validation after dedupe and suppression | 1,800 emails | $0.0072 | $12.96 |
| Total paid usage | | | $12.96 |

2,000 new leads uses 2% of the 100,000 daily allowance. At an expected 1,480 send-ready rows the paid cost is under $0.01 per contact. Because $12.96 exceeds $5, show this table and wait for a yes.

### Error handling

| Code | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, stop. |
| 403 on a database call | The plan may not include databases; tell the user the Lead Database needs Growth or Scale. |
| 409 | Same validation submitted moments ago; use the earlier `runId` from `list_runs`. |
| 429 | Back off 30 seconds, retry once. |
| 503 | Narrow the search (state, size band, fewer titles) and retry. |

## Output Format

The user receives:

1. `icp-list-[segment]-[date].csv`: valid emails only, columns per `references/list-quality-standard.md` section 2a, sorted by `company_domain`.
2. `icp-list-[segment]-[date]-hold.csv`: catch_all and unknown rows with `email_status` filled.
3. A markdown report following `templates/output-template.md`: ICP definition with evidence, filters, count check, pull funnel, validation results, cost, output schema, 5 sample rows, next steps.

## Quality Check

- [ ] Every filter traces to 3+ example customers or to an explicit user instruction.
- [ ] A `limit: 1` count ran and its total appears in the report before any pull.
- [ ] `check_wallet` ran; any paid step over $5 had a user go-ahead.
- [ ] Funnel rows decrease or stay equal at each step and every drop has a reason.
- [ ] Validation buckets sum to the number validated.
- [ ] Main CSV is 100% `email_status = valid`, validated within 30 days.
- [ ] 0 duplicate emails, 0 suppression matches, 3 or fewer contacts per domain.
- [ ] 20-row QA sample checked per section 10 of the quality standard, with misses recorded.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Filters from adjectives ("tech companies") | Returns hundreds of thousands of mixed rows | Profile the example domains first (step 1). |
| One title string, no synonyms | Misses half the buyers ("Head of Sales", "CRO", "VP Revenue") | Use the title family list. |
| No `notTitle` | Assistants to the VP, former VPs, and sales engineers match "VP Sales" partial matches | Apply the exclusion set for the family. |
| Paging with `page` while `excludeDelivered` is on | Pages shift as records get delivered and you skip rows | Use `after` cursors, or keep `page: 1`. |
| Validating before dedupe | Paying twice for the same address | Dedupe and suppress first. |
| Shipping catch-all rows in the main file | Bounces you could not see coming | Hold file, separate campaign, 10% volume cap. |
| 10 contacts at one company | Admins flag the sender; complaints climb | Cap at 3 per domain. |
| `industry` label typed from memory returns 0 | Database labels differ | Recount without it and lean on `keywords`. |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or the routing table for this skill's files. |
| `references/icp-filter-recipes.md` | Drafting filters (step 2). 36 recipes by vertical with ready JSON. |
| `references/title-synonyms-and-exclusions.md` | Building `title` and `notTitle` strings for any buyer family. |
| `references/count-and-paging-runbook.md` | Counting, widening or tightening, the cursor loop, 503s, daily allowance planning. |
| `references/list-quality-standard.md` | Columns, normalization, dedupe, validation buckets, thresholds (shared). |
| `references/scrapercity-catalog.md` | Prices and tool parameters (shared). |
| `references/scrapercity-platform.md` | Plans, database rules, daily allowances (shared). |
| `references/outbound-compliance-primer.md` | Country rules before sending (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | Seeing a finished report for VP Sales at 50-200 employee US SaaS. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `tam-builder` to size the full market before choosing a slice.
- `decision-maker-finder` when the user already has the account list.
- `cold-email-list` to carry this file through to sequencer import.
- `email-list-cleaner` to re-validate an older export of this list.
- `crm-enricher` to push the result into HubSpot or Pipedrive.
- `scrapercity-lead-database` for every Lead Database parameter in depth.
- `cold-email-strategy` for what to send once the list is ready.
