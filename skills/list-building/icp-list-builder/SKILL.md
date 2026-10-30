---
name: icp-list-builder
description: >-
  Builds a list of the people who decide on a purchase at companies that fit
  an ICP, and answers how many companies and contacts exist, how to tier them,
  what it costs and how to get verified emails. Delivers a validated send file
  with a funnel, or a dated plan when no call can run yet. Use when the user
  asks for decision-makers, buyers or contacts by industry, size and geography
  ("people who decide on warehouse automation at US 3PLs with 200-2,000
  employees", "pull VP Sales at 50-200 person SaaS"), says "build me a list
  like these customers", "lookalike list", "ICP list", or "turn my Sales Nav
  search into emails". Starts from best-fit customers when given, counts before
  pulling, validates every email. For a company-only market count use
  tam-builder; for buyers at a named list of accounts use decision-maker-finder.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.2.0"
  author: ScraperCity
  category: list-building
  tags:
    - icp
    - lookalike
    - lead-database
    - list-building
    - email-validation
    - sales-navigator
    - buying-group
    - b2b
  related_skills:
    - tam-builder
    - decision-maker-finder
    - account-researcher
    - cold-email-list
    - email-list-cleaner
    - crm-enricher
    - scrapercity-lead-database
    - cold-email-strategy
    - signal-triggered-outbound
  frameworks:
    - "April Dunford - best-fit customers as the source of targeting"
    - "Gartner B2B Buying Report (2022 survey) - buying groups of five to 11 stakeholders across five functions"
    - "US Census Bureau - Statistics of U.S. Businesses (2022 data), firm counts by industry and employment size"
    - "Pew Research Center (January 2024) - LinkedIn use by education level"
    - "Eypasch, Lefering, Kum and Troidl, BMJ (1995) - zero events in n puts the 95% upper limit at 3/n"
    - "Alex Berman - narrow lists, 100-email test cells, 30 to 60 day market cycles"
    - "Google, Yahoo and Microsoft - bulk sender requirements (2024-2025)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
---

# ICP List Builder

## Overview

This skill answers the questions people ask when they want a contact list: how many companies fit, how many decision-makers sit in them, how to tier them, what it costs, and how to end up with verified emails. It then builds the list: a send file where every email validated `valid`, a hold file for catch-all and unknown addresses, and a report whose funnel accounts for every dropped row.

When ScraperCity is reachable, the counts are free, so the skill runs them before answering and delivers a **run report** with live numbers. When no call can run (no API key or MCP server in the session), it delivers a **plan report**: company counts from Census firm data, contact counts from published buying-group sizes, costs as ceilings, and dated steps that replace each estimate.

It prevents three expensive mistakes: describing an ICP in adjectives and pulling whatever the database returns; quoting invented counts and rates as if they were measured; and paying to validate thousands of contacts the tiers will never email.

## When to Use

- "Build me a list of the people who decide on X at Y companies with 200-2,000 employees. How many exist, how would you tier them, what does it cost?"
- "Here are 5 of our best customers, build me a list of more like them."
- "Pull VP Sales at 50-200 employee SaaS companies in the US."
- "Here's my Sales Navigator search, get me emails for these people."
- "Lookalike list", "ICP list", "target account contacts", "buying committee at companies like these".

Use a different skill when:

| The user wants | Use |
|-|-|
| Companies only: market size, TAM/SAM/SOM, every account in a market, no people yet | `tam-builder` |
| The buyers at a list of companies or domains they already have | `decision-maker-finder` |
| A one-page brief on 1-10 named accounts before a call | `account-researcher` |
| Local businesses by category and city (dentists, roofers) | `local-business-list` |
| A list built from events (funding, hiring, job changes) across many companies | `signal-triggered-outbound` |
| A finished file formatted for one sequencer's import | `cold-email-list` |
| To clean a list they already have | `email-list-cleaner` |
| Shopify or WooCommerce stores filtered by apps or tech | `ecommerce-by-techstack` |

## Prerequisites

Collect these before the first call. A missing input never blocks the work: use the sourced default in the table and ask for the input once, as a Next Steps row.

| Input | Why | When missing |
|-|-|-|
| 3-5 best-fit customer domains, 2-5 lost or churned with the reason | Source of filters and exclusions | Build from the user's instruction; one "Evidence:" line asks for them |
| What the product does, in one line | Picks the role families | Ask |
| Target send-ready rows | Sets pages and cost | Every account the tiers select |
| Geography | Location filters, send times | United States |
| A Sales Navigator search | Becomes the filter draft | None |
| Suppression files (customers, open deals, past sends, unsubscribes, competitors) | Removed before validation | Ask in Next Steps |
| Re-contact window | Suppresses recent sends | The 30 to 60 days Alex Berman puts between cycles (alexberman.com, October 2026), cited as such |
| Per-company contact cap | Contacts per account | Set per tier, never above Gartner's 5-11 buying group |
| AE and SDR headcount | Cuts Tier 1 to capacity | One line asking for it |
| Deal size, margin, win rates | Spend ceilings per tier | Leave ceilings out |
| Plan level | The Lead Database needs Growth or Scale | `check_wallet` reads it |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| April Dunford, best-fit customers | Filters come from the customers who understood the product fastest and got the most value, and exclusions from accounts lost on fit. One unusual logo never sets a filter. |
| Gartner B2B Buying Report (2022 survey) | Buying groups hold five to 11 people from about five functions. Each role family is its own query, contacts per account stay at or under that size, and companies x 5-11 bounds a plan's contact estimate. |
| US Census Bureau, Statistics of U.S. Businesses (SUSB, 2022 data, released April 2025) | Counts US firms by industry and enterprise employment size (200-299 up to 1,500-1,999 and beyond). It is the company count in a plan report and the benchmark for the database count in a run report. |
| Pew Research Center, Americans' Social Media Use (January 2024) | 10% of US adults with a high school education or less use LinkedIn, against 53% of college graduates. Employee counts in B2B data read low for firms with mostly hourly staff, so the band edges get checked against the company's own site. |
| Eypasch et al., BMJ 1995 | With zero events in n checks (n over 30), the 95% upper limit on the rate is 3/n. A fit sample of 60 rows with no misses caps misfits under 5%. |
| Alex Berman (X27, ScraperCity) | Narrow lists shaped like a case study beat broad ones; test a niche with about 100 emails (Lean B2B interview, December 2020); keep bounces under 2% (alexberman.com); send one email per person per cycle, 30 to 60 days apart (alexberman.com TAM breakdown, October 2026). |
| Google, Yahoo, Microsoft sender requirements (2024-2025) | Remove invalid recipients, keep spam rate under 0.3%, honor unsubscribes within 48 hours. Only validated rows and one shared suppression list reach a sequencer. |

Details and when to open each file: `references/framework-notes.md`.

## Workflow

### 1. Decide run or plan

Call `check_wallet`. If it answers, every count below is free: run them and write a run report. If ScraperCity is not reachable in the session, write a plan report: size companies from SUSB (step 4), contacts as companies x 5-11 (Gartner), costs as ceilings, and put every call in Next Steps with an owner and a date. Never fill a plan with invented counts, valid shares or catch-all shares; a figure is sourced, computed from sourced figures, or left to the step that measures it.

### 2. Build the evidence worksheet, or ask for it once

For each best-fit and lost domain, call `query_lead_database` with `companyDomain` and `limit: 5`; record industry as the database spells it, employees, keywords, HQ, the signer's title and the trigger at purchase. Trait rules are in `references/icp-evidence-worksheet.md`: a trait every best-fit account shares becomes a filter; a trait on fit losses only becomes an exclusion the user approves; competitor, price and timing losses never exclude. With no evidence, write the ICP statement from the instruction and one "Evidence:" line asking for domains; never a table of empty rows. Get the user's yes on the statement before pulling.

### 3. Map the buying group into role families

One query per role family, so a long title list in one family cannot leak rows into another. Most B2B purchases need four: the economic buyer, the day-to-day owner of the problem, the technical evaluator, and IT or systems when the product touches their stack. Title and `notTitle` strings are in `references/title-synonyms-and-exclusions.md` (section "Buying-group families"). The economic-buyer family always carries Owner, Co-Owner, Founder, Co-Founder and Managing Partner next to CEO and President: family-owned and founder-led companies use those titles for the person who signs. Guard the partial matches: "vice" stops "President" from matching every Vice President, "coordinator" stops "COO", "product owner" and "process owner" stop "Owner".

Start the shared filters from the closest recipe in `references/icp-filter-recipes.md`, or translate a Sales Navigator search with `references/sales-navigator-filter-map.md`. Add `hasEmail: true`, the anti-ICP `notKeywords`, and `industry` only once a customer lookup shows the database's label.

### 4. Count companies and people

- **People:** one `limit: 1` count per family; read `pagination.total`. Read the first 100 rows of each and put the word behind every wrong title into `notTitle`, then recount. Widen or tighten with the table in `references/count-and-paging-runbook.md`.
- **Companies:** the Lead Database counts people. Pull the families (included in the plan) and dedupe on `company_domain`; that is the company count. Do not multiply a title proxy by an assumed ratio.
- **Benchmark:** SUSB firm counts for the NAICS codes and employment classes of the band (`references/count-and-paging-runbook.md` section 9). A database count far below SUSB after exclusions means widen keywords, then look up the domains on the industry's association member directory or trade-show exhibitor list with `companyDomain`; far above means the keywords admit other industries.
- **Band edges:** in industries with mostly hourly staff (warehousing, manufacturing, retail, healthcare delivery, construction, hospitality), count the band just below the floor as its own query. Step 6 admits those companies one by one.

| `pagination.total` vs target | Action |
|-|-|
| Below target | Widen one filter, recount |
| At or a little above | Show the count and cost; pull |
| Many times the target | Tighten (Berman: the list closest to the case study converts best); recount |
| 0 | Remove one filter at a time; the last one removed is spelled differently in the database |
| 503 | Split by state or size band; retry |

Wait for a go-ahead when the paid part exceeds $5.

### 5. Pull with cursor paging

Page each family with `after: "0"`, `limit: 100`, then each `pagination.next_after` until null. Keep filters identical across pages and save each page as it arrives. Add `excludeDelivered: true` on later cycles. Loop and failures: `references/count-and-paging-runbook.md`.

### 6. Check the business model and the band edges

When keywords cannot separate companies that run the operation the product serves from look-alikes (a 3PL that runs warehouses versus a freight broker; a food plant versus a brand that uses a co-manufacturer; a clinic versus a billing company), read each account's own site before scoring: record yes or no and the URL that shows it (`plant_check_url`, `site_check_url`). Drop the no's before any paid step. In the same pass, a company from the below-floor band joins only when its site, a press release or a job posting states a headcount inside the band; a company inside the band whose site states one above the ceiling leaves. No ScraperCity charge; it costs reading time, so it runs after dedupe and exclusions.

### 7. Tier the accounts (when asked, or when the list exceeds what the team can work)

Fit sets the tier, using only columns every account has (size band, segment, role families present); a column filled for some accounts stays out of the score. Tier rows add up to the account total. Contacts per account fall by tier and never exceed the buying group. Movers (a dated trigger such as a new site, a new leader in the buyer's seat, hiring for the role the product serves, or a past reply in the CRM) lift an account one tier for the next send cycle; two movers still lift one tier. Tier 1 size comes from the user's AE headcount; without it, one Capacity line asks for it. Spend ceilings appear only on a "Deal inputs (from you):" line with the user's deal size, margin and win rates. Weighted lift scores across a whole market belong to `tam-builder`.

### 8. Normalize, dedupe, suppress

Map fields to the person schema in the quality standard (section 2a), normalize (section 3), dedupe on email, then LinkedIn URL, then first + last + domain. Suppress in this order: unsubscribes and remove requests, the do-not-contact list, bounces, complaints, current customers, open opportunities, competitors, anyone contacted inside the re-contact window. Count every drop by reason.

### 9. Validate only the selected slots

Pick a primary and one backup per slot under each tier's cap. Validate the primaries with `validate_emails`; an `invalid` slot gets its backup validated, an `unknown` gets one re-check on a later day, so each slot is validated at most twice. Top-tier slots still empty take a named person from the same family query with `hasEmail` removed, then `find_emails` ($0.05 per email found, free if none). Poll `check_run_status` until SUCCEEDED, `download_results`, map `email_result` (`valid_catch_all` becomes `catch_all`). Only `valid` goes into the send file; catch-all and still-unknown go to the hold file.

### 10. Fit sample, deliver, test cell

Check a random sample per tier by hand on title, company, location, domain and still-employed. Size it as n = 3 / the misfit ceiling, n over 30 (Eypasch 1995): 60 rows caps misfits under 5% when none miss. A miss a filter word would have stopped means fix the filter and re-pull, never hand-patch rows. Write the report from `templates/output-template.md` and run `scripts/check-output.py` on it. Release a 100-contact test cell first (Berman, Lean B2B 2020) and the rest only while bounces stay under 2% (alexberman.com); the hold file follows as its own 100-contact cell under the same line. Sort replies by title family; when referral replies keep naming another title, move it up on the next pull. Change the list or the copy per cycle, never both.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Plan and balance | `check_wallet` | Free |
| Evidence lookups, counts, pulls | `query_lead_database` | Included on Growth ($149/mo) and Scale; 100,000 new leads a day; re-fetching leads you already have is free |
| Validate | `validate_emails` | $0.00169 per email |
| Poll and fetch | `check_run_status`, `download_results` | Free |
| Email for a named top-tier contact | `find_emails` | $0.05 per email found, free if not found |
| Technology-defined segment | `scrape_builtwith` (Tech Stack Search) | $4.99 per technology |

### Count call (MCP), one per role family

```json
{
  "title": "VP Sales, Vice President of Sales, VP of Sales, Head of Sales, Chief Revenue Officer, CRO",
  "notTitle": "assistant, intern, former, retired, advisor, board, investor, operations, enablement, engineer",
  "keywords": ["saas", "b2b"],
  "notKeywords": ["agency", "staffing"],
  "minEmployees": 50,
  "maxEmployees": 200,
  "country": ["United States"],
  "hasEmail": true,
  "limit": 1
}
```

Seniority can replace part of a title list: `"seniority": ["vp", "c_suite"]` with `"department": ["sales"]`. The tool documents `vp`, `director` and `c_suite` as seniority values; confirm any other value (such as `owner`) with a `limit: 1` call and read the rows, or put the titles in `title`.

### Pull loop (MCP)

```text
after = "0"
while after:
    r = query_lead_database({...same filters..., "limit": 100, "after": after})
    save(r.data)
    after = r.pagination.next_after
```

### REST and CLI

```bash
curl -s -X POST -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"title":"VP Sales, Head of Sales, CRO","keywords":["saas"],"minEmployees":50,"maxEmployees":200,"country":["United States"],"hasEmail":true,"limit":100,"after":"0"}' \
  https://app.scrapercity.com/api/v1/database/leads
curl -s -X POST -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d '{"emails":["dana@ledgerline.example"]}' https://app.scrapercity.com/api/v1/scrape/email-validator
```

Then `GET /api/v1/scrape/status/{runId}` until SUCCEEDED and `GET /api/downloads/{runId}`. CLI: `db-leads`, `email-validate`, `poll`, `download`.

### Worked cost estimate (plan report)

Food and beverage manufacturers, 200-2,000 employees: 1,228 firms in SUSB 2022, tiered 171 / 320 / 737 with 4 / 3 / 2 contacts.

| Item | Units | Unit price | Cost |
|-|-:|-:|-:|
| Counts and pulls, four families | Up to 13,508 people | Included in Growth | $0.00 |
| Validator, primaries | 3,118 | $0.00169 | $5.27 |
| Validator, second pass ceiling | 3,118 | $0.00169 | $5.27 |
| Email Finder ceiling, Tier 1 slots | 684 | $0.05 per email found | $34.20 |
| Total paid usage, ceiling | | | $44.74 |

$44.74 sits inside Growth's $159 monthly credit, so the cash cost is the $149 plan fee. It exceeds $5, so show this table and wait for a yes before step 9.

### Error handling

| Code | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, stop. |
| 403 on a database call | The plan may not include databases; the Lead Database needs Growth or Scale. |
| 409 | Same validation submitted moments ago; reuse the earlier `runId` from `list_runs`. |
| 429 | Back off, then retry once. |
| 503 | Narrow the search (state, size band, fewer titles) and retry. |

## Output Format

The user receives the send file and hold file (run report only) and one markdown report from `templates/output-template.md`:

1. Title, then one `Status:` line: "Ran YYYY-MM-DD" with plan and wallet, or "Plan, prepared YYYY-MM-DD" with the one sentence saying nothing ran and which step replaces the estimates. That sentence appears nowhere else in the report.
2. `## Answer` first: a table with one row per question the user asked, in their words. In a plan, counts are sourced ranges or ceilings.
3. `## ICP Definition`: the statement; the evidence table only when accounts were supplied, otherwise one "Evidence:" line asking for them.
4. `## Filters Used`: shared filters, then one row per role family with `title` and `notTitle`.
5. `## Count Check`: one table holding every count and benchmark (Call, Result, Decision). No separate market-size table.
6. `## Account Tiers` when tiering was asked for: rows summing to a Total row, then Movers and Capacity lines.
7. `## Pull Funnel` and `## Validation Results` with the Fit sample line, run report only. A plan carries no projected funnel or bucket shares.
8. `## Cost Estimate` ending in a "Prices: ... checked YYYY-MM-DD" line.
9. `## Output Schema`: columns with one example each. No sample-rows section.
10. `## Next Steps`: a table with Step, Owner (You, Agent, a named role), Date and Done when. In a plan this table is the run plan.

Economy rules: each figure appears once (the Answer points to a section instead of repeating its numbers); every outside number names its source and date on first mention; assumed rates carry no causal story; no internal tool ids, file paths or skill names (describe the action: "import to the sequencer with cross-campaign duplicate checking on"); file names only in a run report; no value left as "you set" when a sourced default or a Next Steps row can carry it; no framework lists, self-graded checklists or legal commentary.

## Quality Check

- [ ] `## Answer` is the first section and answers every question the user asked.
- [ ] The Status line is the only place that says nothing ran.
- [ ] Every number is a live result, a sourced figure with its date, or arithmetic on those.
- [ ] Companies are counted by deduping `company_domain` (run) or from SUSB (plan), never title proxy x assumed ratio.
- [ ] The economic-buyer family includes Owner, Founder and Managing Partner with their `notTitle` guards.
- [ ] Hourly-workforce industries: the below-floor band was counted and admitted only by site-stated headcount.
- [ ] Look-alike business models were checked on each company's site, with the URL recorded.
- [ ] Tier rows sum to the Total; no spend ceiling without a "Deal inputs (from you):" line.
- [ ] Run report: funnel rows add up, buckets sum to the total validated, the send file is 100% `valid`.
- [ ] Every Next Steps row has an owner and a date.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Filters from adjectives ("tech companies") | Returns hundreds of thousands of mixed rows | Evidence worksheet first, or one Evidence line and the user's instruction. |
| Company count from a CEO title proxy times a guessed ratio | Companies with no CEO record vanish; the figure looks precise and is not | Dedupe `company_domain` across the family pulls; benchmark against SUSB. |
| Invented counts, valid shares or catch-all shares in a plan | The user budgets on numbers nobody measured | Sourced ranges and cost ceilings; the measuring step goes in Next Steps. |
| Database headcount taken as exact in hourly-workforce industries | Real in-band companies show as smaller and drop out | Count the below-floor band; admit companies whose site states an in-band headcount. |
| Keyword filters alone for business model | Brokers and resellers that mention the activity pass | Site check per account, URL recorded, before scoring. |
| Economic buyer titles without Owner or Founder | Misses the signer at family-owned and founder-led firms | Add them with `product owner, process owner` in `notTitle`. |
| One query for every title | Long title lists leak rows across families | One count and pull per role family. |
| Validating every pulled contact | Pays for contacts the tiers will never email | Validate tier-selected slots; backups only for invalid slots. |
| Shipping catch-all rows in the send file | Bounces you could not see coming | Hold file, released as its own 100-contact cell under the 2% line. |
| Spend ceilings from assumed deal size and win rates | A budget answer nobody asked for, built on invented data | Only with the user's deal inputs. |
| Sending every row on day one | A filter error shows up only after every row is sent | 100-contact test cell; release while bounces stay under 2%. |
| Tool ids, skill names and repeated tables in the report | The reader has to translate and re-read | Product names, actions, each figure once. |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or the routing table for this skill's files. |
| `references/icp-evidence-worksheet.md` | Step 2: evidence accounts, trait rules, losses by reason, the lift check, size bands, situation segments, the ICP statement. |
| `references/icp-filter-recipes.md` | Step 3: 37 recipes by vertical with ready JSON. |
| `references/sales-navigator-filter-map.md` | The user has a Sales Navigator search or seat. |
| `references/title-synonyms-and-exclusions.md` | Step 3: `title` and `notTitle` strings, including the buying-group families. |
| `references/count-and-paging-runbook.md` | Steps 4-5 and 9: counting, SUSB benchmarks, band edges, widening, the cursor loop, 503s, validation runs. |
| `references/list-quality-standard.md` | Columns, normalization, dedupe, validation buckets, suppression, fit sample (shared). |
| `references/scrapercity-catalog.md` | Prices and tool parameters (shared). |
| `references/scrapercity-platform.md` | Plans, database rules, daily allowances (shared). |
| `templates/output-template.md` | Writing the report, run or plan. |
| `examples/worked-example.md` | A run report: VP Sales at 50-200 employee US SaaS, from five customers. |
| `examples/plan-example.md` | A plan report: maintenance software buyers at US food and beverage manufacturers, no customers supplied, no call run. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `tam-builder` to size and score a whole market at company level.
- `decision-maker-finder` when the user already has the account list.
- `account-researcher` for briefs on the Tier 1 accounts.
- `signal-triggered-outbound` for the movers: new sites, new leaders, hiring.
- `cold-email-list` to format the send file for one sequencer's import.
- `email-list-cleaner` to re-validate an older export of this list.
- `crm-enricher` to push the result into HubSpot or Pipedrive.
- `scrapercity-lead-database` for every Lead Database parameter in depth.
- `cold-email-strategy` for what to send once the list is ready.
