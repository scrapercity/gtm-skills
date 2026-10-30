# Framework Notes: ScraperCity Lead Database

This file lists the sources behind the skill, what each one contributes, and which reference file to open for which job.

## Routing table

| You need | Open |
|---|---|
| A ready filter set for a role, industry, size band or geography | `references/filter-cookbook.md` |
| Exact behavior of a filter (partial match, whole word, OR vs AND) | `references/filter-semantics.md` |
| Seniority and department values, and how to verify a value before a big pull | `references/filter-semantics.md` |
| Person location vs company HQ location | `references/filter-semantics.md` |
| An error code, an empty result, a sample that looks wrong | `references/troubleshooting.md` |
| Prices for tools chained after the pull | `references/scrapercity-catalog.md` (shared) |
| Plan names, allowance, paging rules shared by all databases | `references/scrapercity-platform.md` (shared) |
| The acceptance bar for a finished list | `references/list-quality-standard.md` (shared) |
| Wallet checks, confirmation before spend, webhook vs polling | `references/scrapercity-agent-patterns.md` (shared) |

## Sources and what each contributes

### ScraperCity Lead Database API (primary)

The published `scrapercity` npm package (version 1.0.17) is the behavior source, in these files:

- `bin/mcp.mjs` defines `query_lead_database` and the description of every parameter: title is partial match with commas for several, keywords are company tags with any match, `companyCountry`/`companyState`/`companyCity` are company HQ and not the person, `excludeDelivered` needs `page` kept at 1 or the `after` cursor, `limit` maxes at 100 and defaults to 50.
- `bin/cli.mjs` defines `db-leads`, its flag names, which flags take comma lists, and that it prints the total, the next cursor and the first 3 rows.
- `lib/client.mjs` sends GET with repeated keys for arrays and switches to POST with a JSON body when the query string passes 6,000 characters.
- `AGENT_DOCS.txt` documents `search_translation`, the 400 for a URL with nothing usable, the 409 `filters_not_applied_yet`, the 503 rule, the ~16KB query string limit, and the field list on returned leads.

Contribution: every parameter name, every matching rule and every error branch in the skill.

### ScraperCity platform facts and catalog

`references/scrapercity-platform.md` (checked against scrapercity.com, /pricing and /llm-info on 2026-10-12) gives the plans (Starter $49, Growth $149, Scale $649 a month), that the Lead Database is Growth and up, the 100,000 new leads a day allowance, and that re-fetching a lead the account owns is free. `references/scrapercity-catalog.md` gives the prices used in cost tables: `scrape_apollo` $0.0039 per lead, `validate_emails` $0.00169 per email, `find_emails` $0.05 per email found, `find_mobiles` $0.25 per number found.

scrapercity.com/api-docs adds two operating limits used in the daily pull design: 100 API requests a minute per key and a daily database reset at midnight UTC.

### Apollo.io People API documentation

People-search URLs that users paste often come from Apollo.io. Apollo's People API docs list the seniority vocabulary (`owner`, `founder`, `c_suite`, `partner`, `vp`, `head`, `director`, `manager`, `senior`, `entry`, `intern`) and say a person needs to match one listed seniority. They also say Apollo's own title search includes similar titles unless told otherwise. That explains why a URL count in Apollo and the database count can differ, and it is why the skill reads `search_translation` before trusting a number.

### US Bureau of Labor Statistics, Employee Tenure (January 2026)

Median tenure with the current employer was 4.1 years. Spread evenly, that is roughly 1.4% of a contact list changing employer each month (a planning estimate; replace it with your measured rate). It is why the skill dates every pull and re-checks named people by `socialUrl` before an important send; recurring champion checks are the job-change recipe in the `scrapercity-integrations` skill.

### Alex Berman (ScraperCity founder)

His companies send millions of cold emails a month and have booked 500k+ meetings. The working rule used here: one narrow segment, one offer, one message. A pull plan splits a broad ICP into segments (by size band, region or title family) so each segment gets its own copy. That is also how the skill stays under the 503 limit.

## How the sources combine

1. ScraperCity docs decide what the API does.
2. Costs come from the catalog.
3. Apollo docs explain URL translation gaps.
4. Tenure data sets how long a pulled record stays usable before a re-check.
5. Segment-per-offer decides how big each pull should be.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/pricing
- https://scrapercity.com/llm-info
- https://scrapercity.com/api-docs
- https://docs.apollo.io/reference/people-api-search
- https://www.bls.gov/news.release/tenure.nr0.htm
