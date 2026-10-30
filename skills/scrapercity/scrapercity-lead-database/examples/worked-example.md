# Lead Pull Plan: VP Sales at US SaaS, 50-200 employees

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

## Request Summary

| Item | Value |
|---|---|
| ICP in one sentence | Sales leaders (VP or Head of Sales) at software-as-a-service companies headquartered in the United States with 50 to 200 employees, for a cold email offer of outsourced SDR capacity |
| Job type (one-off or daily feed) | One-off pull of the full segment now, then a daily feed of new matches at 7:00 UTC |
| Plan confirmed by check_wallet | Growth, $149/mo, wallet balance $212.40 |
| Target volume | Full segment (count below), then every new match each day |
| Access path (MCP, CLI or REST) | MCP `query_lead_database` for the count, REST POST loop for the export and the daily feed |

## Filter Spec

Every parameter must exist in `query_lead_database`. Every geography row says person or company.

| Parameter | Value | Reason |
|---|---|---|
| title | VP Sales, VP of Sales, Vice President Sales, Vice President of Sales, Head of Sales | Partial match, comma list. Each stem carries the function word so VP Product and VP Finance stay out |
| notTitle | Assistant, Intern, Operations, Ops, Enablement | Removes Sales Operations and Enablement roles that match "Head of Sales" stems, plus support staff |
| companyCountry | United States | Company HQ location, because the offer is priced in USD and contracts sign in the US. Person location is left open so remote US sales leaders at US companies stay in |
| keywords | saas | Company tag, whole word, any match |
| notKeywords | agency, consulting, staffing | Drops service firms that tag themselves saas |
| minEmployees | 50 | Below 50, founders run sales and there is no VP |
| maxEmployees | 200 | Above 200, an internal SDR team usually exists |
| hasEmail | true | Email campaign, so only rows with an email |

## Count Check

| Item | Value |
|---|---|
| Call used | MCP `query_lead_database` with the filter spec and `limit: 1` |
| pagination.total | 4,812 |
| Sample row title and company | "VP of Sales" at a 120-person US HR software company, company_industry computer software, company_state California |
| search_translation applied | Not used, no URL in this request |
| search_translation approximated | Not used, no URL in this request |
| search_translation not_supported | Not used, no URL in this request |
| Decision | 4,812 sits inside the 50 to 100,000 band. Pull the full segment in one day |

## Pull Plan

| Item | Value |
|---|---|
| Paging method | Cursor: `after: "0"`, then `pagination.next_after` until null |
| excludeDelivered | true, so a re-run or the daily feed never returns a lead the account already has |
| page | 1 (never raised; the cursor does the paging) |
| Calls needed | 49 calls of 100 (4,812 / 100 rounded up) |
| Daily new leads | 4,812 on day one, then the new matches each day after (expected to be a few dozen) |
| Days needed | 1 |
| Run log location | `runs/vp-sales-saas.csv` with date, segment, new leads, last cursor |

The 49 calls run at one call every 0.7 seconds, under the 100 requests a minute limit, so the export finishes in about a minute.

## Cost and Allowance

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Lead Database pull | 4,812 | included in Growth | $0.00 |
| validate_emails on every email | 4,812 | $0.00169 | $8.13 |
| find_mobiles on the 300 accounts at 100-200 employees (40% found assumed) | 120 found | $0.25 | $30.00 |
| Total paid | | | $38.13 |

Allowance share: 4,812 of 100,000 new leads, 4.8% of one day. For comparison, the same 4,812 leads through `scrape_apollo` would cost 4,812 x $0.0039 = $18.77 and take about 15 to 30 minutes. User approved the $38.13 before validation started.

## Sample QA

| Check | Result |
|---|---|
| Title matches intent | 19 of 20 are VP or Head of Sales. 1 is "VP, Sales Ops", which slips past `notTitle: Operations`, so "Ops" was added to notTitle for the full pull |
| Company size inside band | 20 of 20 between 52 and 198 employees |
| HQ or person location as specified | 20 of 20 company_country United States. 2 people located in Canada at US companies, kept on purpose |
| Email present | 20 of 20 |
| Excluded titles absent | 0 assistants, 0 interns, 0 enablement |
| Pass mark (set before the sample) | 18 / 20, the user's bar for this pull |
| On-target rows | 19 / 20 |

## Next Steps

1. Run `validate_emails` on all 4,812 emails ($8.13) and keep only valid results for the first send.
2. Split the file by employee band (50-99 and 100-200) so each band gets its own opening line, then hand off to `cold-email-list`.
3. Schedule the daily feed: same filters, `excludeDelivered: true`, `after: "0"`, loop to null, append new leads to the run log, and validate them the same day.
