---
name: scrapercity-lead-database
description: >-
  Plans and runs pulls from the ScraperCity B2B Lead Database: filter specs,
  count checks, people-search URL translation, cursor paging, daily pulls of
  only new leads, and the choice between the database and the Apollo Scraper.
  Produces a lead pull plan with a filter table, counts, allowance share and a
  sample QA. Use when the user asks for B2B contacts by title, seniority,
  industry, company size, revenue or location, wants a daily lead feed, pastes
  a people-search URL, or hits a 400, 409 or 503 from the Lead Database.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags: [lead-database, b2b-data, filters, prospecting, api, mcp]
  related_skills: [using-scrapercity-skills, scrapercity-mcp, scrapercity-cli, scrapercity-api, icp-list-builder, tam-builder, decision-maker-finder, email-list-cleaner, cold-email-list, scrapercity-local-business-database]
  frameworks:
    - "ScraperCity - Lead Database API reference (scrapercity npm package 1.0.17)"
    - "Apollo.io - People API search parameters (seniority values, title matching)"
    - "FTC - CAN-SPAM Act compliance guide for business"
    - "ICO - PECR guidance on electronic mail marketing to corporate subscribers"
    - "Alex Berman - narrow lists and one offer per segment"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, scrapercity-agent-patterns.md]
---

# ScraperCity Lead Database

## Overview

This skill turns "get me B2B leads for X" into a filter spec that returns the right people, a count check before anything is pulled, a paging plan that fits the 100,000 new leads a day allowance, and a short QA of the first 100 rows.

The Lead Database is included with the Growth plan ($149/mo) and up. Every lead returned is saved to the account. Only new leads count toward the daily allowance, and fetching a lead the account already has is free.

The mistakes it prevents:

- Pulling 20,000 rows on a filter that was wrong, because nobody looked at `pagination.total` and a 1-row sample first.
- Using `country` (where the person lives) when the user meant `companyCountry` (where the company is headquartered).
- Paging with `page=2, 3, 4` while `excludeDelivered=true`, which skips records.
- Paying for an Apollo Scraper run and waiting days for leads the database already returns in seconds.

## When to Use

Use it when the user says:

- "Find VPs of Sales at 50-200 person SaaS companies in the US."
- "Pull every CFO in Texas at companies over $50M revenue."
- "Here is my people-search URL, get me these leads."
- "Set up a daily feed of new leads that match our ICP."
- "The database returned 503" or "409 filters_not_applied_yet" or "400 on my URL."
- "Should I use the Apollo Scraper or the Lead Database?"

Use a different skill for nearby jobs:

| Job | Skill |
|---|---|
| Defining the ICP before any filter exists | `icp-list-builder` |
| Sizing a whole market (accounts and people) | `tam-builder` |
| Finding the 1-3 right people at named accounts | `decision-maker-finder` |
| Local businesses (dentists, plumbers, restaurants) | `scrapercity-local-business-database` |
| Validating the emails after the pull | `email-list-cleaner` |
| Building the final send-ready file for a sequencer | `cold-email-list` |
| MCP install and tool behavior in general | `scrapercity-mcp` |

## Prerequisites

- A ScraperCity account on Growth ($149/mo) or Scale ($649/mo). Starter does not include database access. Run `check_wallet` and read `plan.name`.
- An API key in `SCRAPERCITY_API_KEY` (MCP and CLI) or a Bearer header (REST).
- The ICP in words: titles, seniority, departments, industries, company size, revenue band, person or company geography, exclusions.
- The volume target and cadence: one-off (how many) or daily (how many new per day).

## Authoritative Foundations

| Source | What it contributes here |
|---|---|
| ScraperCity Lead Database API (npm `scrapercity` 1.0.17: `bin/mcp.mjs`, `bin/cli.mjs`, `AGENT_DOCS.txt`) | Every filter name, matching rule, paging rule, error code and the allowance. The only source for behavior. |
| `references/scrapercity-catalog.md` | Prices for the paid tools around the database (`scrape_apollo` $0.0039 per lead, `validate_emails` $0.0072 per email, `find_emails` $0.05 per email found, `find_mobiles` $0.25 per number found). |
| `references/scrapercity-platform.md` | Plans, the 100 records per request cap, `excludeDelivered`, `after`, and the 503 rule shared by all databases. |
| Apollo.io People API docs | The seniority vocabulary people-search URLs carry, and that title search there includes similar titles. Useful when translating a URL. |
| FTC CAN-SPAM guide | B2B email has no exemption. Every message needs accurate headers, a postal address and an opt-out honored within 10 business days. |
| ICO PECR guidance | In the UK, corporate subscribers can be emailed without prior consent; sole traders and some partnerships need consent. Filter UK pulls accordingly. |
| Alex Berman | Narrow lists with one offer each beat one broad list with a generic pitch. Split pulls by segment, never one mega-query. |

Details and routing: `references/framework-notes.md`.

## Workflow

### 1. Confirm access and the job type

Call `check_wallet`. If the plan is Starter, stop and explain that the Lead Database needs Growth or Scale, and offer `scrape_apollo` as the pay-per-lead route. Classify the job:

| Job type | Paging | excludeDelivered |
|---|---|---|
| One-off list under 5,000 | `after` cursor | optional |
| One-off list 5,000-100,000 | `after` cursor, may span days | `true` if re-running |
| Daily feed of new leads | `after=0` each day | `true` always |
| Re-export of leads already owned | `page` or `after` | `false` (re-fetch is free) |

### 2. Translate the ICP into filters

Map every ICP sentence to one filter. The full semantics are in `references/filter-semantics.md`. The rules that cause the most errors:

- **Person vs company location.** `country`, `state`, `city` are where the person is. `companyCountry`, `companyState`, `companyCity` are the company HQ. "US companies" means `companyCountry`. "People based in Texas" means `state`.
- **Titles are partial match, comma separated.** `title: "VP Sales, Head of Sales"` returns either. `"CEO"` also matches longer titles that contain it. Use `notTitle` to remove the noise (`"Assistant, Intern, Executive Assistant"`).
- **Keywords are whole-word, any match.** `keywords: ["saas", "fintech"]` returns companies tagged with either word. Use `notKeywords` to drop adjacent categories.
- **Arrays are OR inside a filter, filters are AND across.** `seniority: ["vp","director"]` plus `industry: ["computer software"]` means (VP or Director) and software.
- **Countries take full names.** "United States", "Germany". US, USA, UK and UAE also work.

If the user gave a people-search URL, pass it as `url` and read `search_translation` (step 4).

### 3. Run a count check before pulling

Call with `limit: 1`. Read `pagination.total` and look at `data[0]`. Report the total to the user with the filter table. Decision rule:

| Total | Action |
|---|---|
| 0 | Loosen: drop `hasPhone`, widen the size band, remove one exclusion, check country spelling. |
| 1-49 | Too narrow for a campaign segment. Widen titles or geography, or switch to `decision-maker-finder` at named accounts. |
| 50-100,000 | Pull. Show the user the count and the day count (total / 100,000). |
| Over 100,000 | Split into segments (by state, size band or seniority) so each segment fits a day and a message. |

A 503 here means the search ran too long: add a location or size band, or cut the title list, then retry.

### 4. Handle a people-search URL

Pass the URL as `url`. Any other filter you pass overrides the matching one from the URL. The response adds `search_translation` with three lists:

- `applied`: used as is.
- `approximated`: mapped to the closest database filter. Read each one and confirm with the user.
- `not_supported`: ignored. If a dropped filter defines the ICP (for example a technology filter), tell the user the count is broader than their URL.

A URL with nothing the database can use returns 400. Rebuild the search with explicit filters. A long URL or a long title list belongs in a POST body: the query string is refused past about 16KB, and the CLI switches to POST on its own past 6,000 characters.

### 5. Pull with the cursor

Send `after: "0"`, `limit: 100`, then each response's `pagination.next_after` until it is null or the target count is reached. Use `after` for anything over a few pages. Use `page` only for small one-off reads without `excludeDelivered`.

### 6. Design the daily pull (feeds)

Each day: `excludeDelivered: true`, `after: "0"`, `limit: 100`, loop `next_after`, stop at the daily target or when `next_after` is null. Starting from `after=0` daily catches every lead the account does not own yet. Keep each day under 100,000 new leads (the allowance resets at midnight UTC per scrapercity.com/api-docs). Per the same page, the API takes 100 requests a minute per key, so 1,000 calls of 100 take at least 10 minutes. Write the run log: date, segment, new leads, last cursor.

### 7. QA the first page

Before the full pull, open 20 rows and check: title matches intent, company size inside the band, company HQ where expected, email present when `hasEmail` was set, no excluded titles leaking. If more than 2 of 20 are off-target, fix the filter and re-run the count. The checklist is in `references/troubleshooting.md`.

### 8. Hand off

Send emails to `validate_emails` before any campaign, and route the file to `cold-email-list`. Never load an unvalidated pull into a sequencer.

## ScraperCity Implementation

### MCP (`query_lead_database`)

```json
{
  "title": "VP Sales, Vice President of Sales, Head of Sales",
  "notTitle": "Assistant, Intern, Operations",
  "companyCountry": ["United States"],
  "minEmployees": 50,
  "maxEmployees": 200,
  "keywords": ["saas"],
  "hasEmail": true,
  "limit": 1
}
```

Then the same body with `"limit": 100, "after": "0"`, looping on `pagination.next_after`.

### CLI (`db-leads`)

```bash
npx scrapercity db-leads --title "VP Sales, Head of Sales" --not-title "Assistant, Intern" \
  --company-country "United States" --min-employees 50 --max-employees 200 \
  --keywords saas --has-email --limit 1
```

The CLI prints the total, the next cursor and the first 3 leads, so it is the fastest count check. For a full export, use REST or MCP. List flags (`--industry`, `--country`, `--state`, `--seniority`, `--department`, `--company-country`, `--company-state`, `--not-industry`) take commas.

### REST

```bash
curl -s -G "https://app.scrapercity.com/api/v1/database/leads" \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
  --data-urlencode "title=VP Sales, Head of Sales" \
  --data-urlencode "companyCountry=United States" \
  --data-urlencode "keywords=saas" --data-urlencode "notTitle=Assistant, Intern" \
  --data-urlencode "minEmployees=50" --data-urlencode "maxEmployees=200" \
  --data-urlencode "hasEmail=true" --data-urlencode "limit=100" --data-urlencode "after=0"
```

Arrays repeat the key (`seniority=vp&seniority=director`), so a GET with two seniorities sends the key twice. `keywords` and `notKeywords` also accept commas. `POST /api/v1/database/leads` with a JSON body takes the same parameters with arrays as JSON arrays.

### Response fields to read

`data[]` (person fields plus `company_industry`, `company_size`, `employees_count`, `company_website`, `company_annual_revenue`, `company_city`, `company_state`, `company_country`, `keywords`), `pagination` (`page`, `limit`, `total`, `totalPages`, `has_more`, `next_after`), `rate_limit`, and `search_translation` when `url` was sent.

### Lead Database or Apollo Scraper

| Factor | Lead Database | `scrape_apollo` |
|---|---|---|
| Price | Included with Growth and up, 100,000 new leads a day | $0.0039 per lead |
| Speed | Seconds per 100 rows | Hours, up to several days. Webhook or hourly polling only |
| Input | Filters or a people-search URL | A people-search URL in Filters 1.0 format |
| Volume per request | 100 per call, cursor for more | 500-50,000 per run |
| Plan | Growth or Scale | Any plan with wallet credit |

Rule: on Growth or Scale, start with the database. Use `scrape_apollo` when the URL relies on filters listed in `not_supported` and the user needs them, or when the account is on Starter. A `scrape_apollo` response can include a `lead_database` block with `matches` (leads with the same filters in the database that the account does not have), a dashboard `url` and the `api` call that returns them now. Pull those first and size the Apollo run to the remainder.

### Worked cost estimate

ICP: VP or Head of Sales, US-headquartered SaaS, 50-200 employees, email required. The count check returns 4,812.

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Lead Database pull (49 calls of up to 100) | 4,812 | included in Growth | $0.00 |
| `validate_emails` on every email | 4,812 | $0.0072 | $34.65 |
| `find_mobiles` on the 300 top-tier accounts (assume 40% found) | 120 found | $0.25 | $30.00 |
| **Total paid** | | | **$64.65** |

The same 4,812 leads through `scrape_apollo` would cost 4,812 x $0.0039 = $18.77 plus the wait. On Growth the database costs nothing extra and finishes in minutes. The pull uses 4.8% of one day's 100,000 allowance. Show this table and get a go-ahead before the validation spend, since it is over $5.

## Output Format

A lead pull plan in Markdown, built from `templates/output-template.md`:

1. **Request Summary**: ICP in one paragraph, job type, plan confirmed.
2. **Filter Spec**: table of parameter, value, reason. Only real parameter names.
3. **Count Check**: total from the `limit: 1` call, sample row notes, `search_translation` lists if a URL was used.
4. **Pull Plan**: paging method, `excludeDelivered`, calls needed, days needed, daily new-lead count.
5. **Cost and Allowance**: table with $ figures and allowance share.
6. **Sample QA**: 20-row check results.
7. **Next Steps**: validation, segmenting, hand-off.

Run `python3 scripts/check-output.py plan.md` before sending.

## Quality Check

- Every filter row uses a parameter that exists in `query_lead_database`.
- Person vs company location is stated for every geography filter.
- A count from a `limit: 1` call is shown before any bulk pull.
- `excludeDelivered: true` is paired with `after` or `page=1`, never with `page` above 1.
- Daily new leads planned are at or below 100,000.
- Every `approximated` and `not_supported` item from `search_translation` is listed with what it means for the count.
- The cost table uses catalog prices and the paid total is shown before spend over $5.
- 20-row QA done, and fewer than 3 of 20 rows off-target.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| `country: ["United States"]` for "US companies" | Filters where the person lives. Remote staff of foreign companies slip in and US-based companies with foreign staff drop out | Use `companyCountry`; add `country` only if the person's location also has to match |
| `title: "Sales"` alone | Partial match pulls Sales Assistants, Sales Engineers, Salesforce Admins | List exact title stems and add `notTitle` |
| Paging `page=2..N` with `excludeDelivered` | Each page you take removes rows from the next query, so later pages skip leads | Keep `page=1` and loop, or use `after` |
| One 300,000-lead mega query | 503 timeouts and a list too broad for one message | Split by state, size band or seniority |
| Ignoring `search_translation` | The URL's tech or intent filters may be `not_supported`, so the count is broader than the user thinks | Report each list back and confirm |
| Treating 409 as a duplicate-request error | On this endpoint, 409 `filters_not_applied_yet` means the named company filters cannot be used yet | Retry later or drop the listed filters. Nothing was returned or counted |
| Running Apollo for leads already in the database | Pays $0.0039 per lead and waits days | Read the `lead_database` block, pull matches first |
| Skipping validation | Bounces hurt the sending domain | `validate_emails` at $0.0072 each before any send |
| Mixing `seniority` and a title list that conflicts | `seniority: ["c_suite"]` with `title: "Director"` returns almost nothing | Use one or the other, or make them agree |

More failure modes and fixes: `references/troubleshooting.md`.

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need to know which source backs a rule, or which reference to open. |
| `references/filter-cookbook.md` | You need a ready filter set for a role, industry or geography (40+ recipes). |
| `references/filter-semantics.md` | You need exact matching behavior, seniority and department values, or the person vs company field map. |
| `references/troubleshooting.md` | A call returned 0, 400, 409, 429 or 503, or the sample looks wrong. |
| `templates/output-template.md` | Start every lead pull plan from it. |
| `examples/worked-example.md` | You want a finished plan to copy the shape of (VP Sales at US SaaS, 50-200 employees). |
| `scripts/check-output.py` | Before handing the plan to the user: `python3 scripts/check-output.py plan.md`. |
| `references/scrapercity-catalog.md` | Prices and schemas for every paid tool you chain after the pull. |
| `references/scrapercity-platform.md` | Plan and allowance facts. |
| `references/list-quality-standard.md` | The acceptance bar for the finished list. |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling and confirmation patterns shared by all ScraperCity skills. |

## Related Skills

- `using-scrapercity-skills`: router for every ScraperCity job.
- `scrapercity-mcp`, `scrapercity-cli`, `scrapercity-api`: access paths and setup.
- `icp-list-builder` and `tam-builder`: decide who to pull before you pull.
- `decision-maker-finder`: named-account people search.
- `email-list-cleaner` and `cold-email-list`: what happens to the file next.
- `scrapercity-local-business-database`: when the target is a local business, not a B2B role.
