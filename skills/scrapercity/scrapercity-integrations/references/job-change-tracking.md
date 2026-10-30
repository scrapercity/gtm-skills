# Job-Change Tracking with Lead Database Re-Pulls

ScraperCity has no job-change alert or monitoring endpoint. What it does have is the Lead Database's `socialUrl` filter, which matches a person by their social profile URL, and a billing rule that makes re-checking people free: fetching a lead the account already has costs nothing and does not count toward the 100,000 a day allowance (package `AGENT_DOCS.txt`). Together those make a scheduled re-pull: look up every person on a watch list, compare the company on the record with the one stored in the CRM, and route the differences. Growth plan and up.

ScraperCity does not publish how often a person's employer is refreshed in the database, so treat a mismatch as a candidate and confirm it on the person's public profile or the new company's site before anyone reaches out.

## 1. Build the watch list

| Column | Why |
|---|---|
| `crm_id` | Write-back and task creation |
| `linkedin_url` | The `socialUrl` lookup key. Rows without one can only be checked by `companyDomain` (section 4) |
| `stored_company_domain`, `stored_title` | What the comparison runs against |
| `relationship` | One of the segments in section 2; decides the route |
| `owner` | Who gets the alert |
| `last_checked_at` | Spacing between checks |

## 2. Segments and cadence

| Segment | Why it is watched |
|---|---|
| Champions and power users at current customers | Their departure puts the renewal at risk; their next company is a warm new account |
| Stakeholders on open opportunities | A departure changes the deal |
| Champions at former customers | A warm path into their next company |
| Stakeholders on closed-lost deals | A new person in the seat reopens the account; the old one may buy at the next company |
| Contacts at target accounts | A promotion into budget changes the message |

For planning volume: the US Bureau of Labor Statistics reported a median employee tenure of 4.1 years in January 2026. If departures were spread evenly, about 1.4% of a contact list changes employer each month. Re-checking a record the account already has costs $0, so the recipe below checks every segment monthly; set each segment's interval from its measured change rate (section 8) once you have a few months of data.

## 3. The lookup

| Path | Call |
|---|---|
| MCP | `query_lead_database` with `{"socialUrl": "https://www.linkedin.com/in/dana-ruiz-example", "limit": 1}` |
| REST | `GET https://app.scrapercity.com/api/v1/database/leads?socialUrl=<url-encoded profile URL>&limit=1` with the Bearer header |
| CLI | No `--social-url` flag in 1.0.17; use REST or MCP |

One call per person, paced at one a second (100 requests a minute per key). A 600-person watch list takes about 10 minutes and costs $0 in wallet. Map the record's company and title keys from your own first response; the package documents `company_website` among the company fields, and the n8n guide on scrapercity.com shows `company_domain` and `title` on person records.

## 4. Compare and classify

Normalize both domains (lowercase, no scheme, no `www.`) before comparing.

| Record shows | Classification | Next |
|---|---|---|
| Same company, same title | No change | Update `last_checked_at` only |
| Same company, more senior title | Promotion | Route per section 5; the message angle changes |
| Same company, different function | Role change | Owner decides whether the person still belongs on the deal |
| Different company | Job-change candidate | Confirm on the public profile, then route |
| No record returned | Unknown | Not evidence that the person left. Recheck next cycle; after two empty cycles, check by hand |

Replacement at the old account: `query_lead_database` with `companyDomain` set to the old domain and the departed person's `title` or `seniority` returns who holds the role now, free on Growth.

Contact at the new company: if the record carries an email, validate it ($0.00169). If not, `find_emails` with first name, last name and the new domain ($0.05 if found, nothing if not), batched into one run for that month's movers.

## 5. Routing

| Relationship | Event | Goes to | Action |
|---|---|---|---|
| Champion at a current customer | Left | CSM and account executive | Risk review, map the replacement (section 4), multi-thread the account |
| Champion at a current or former customer | Joined an account that fits the ICP | Account owner for the new company | Warm note from whoever knows them best |
| Open opportunity stakeholder | Left | Opportunity owner and manager | Deal review; find who now holds the seat |
| Closed-lost stakeholder | Left, and the seat has someone new | SDR on that account | New-logo outreach to the replacement |
| Target account contact | Promoted | Account owner | Adjust the angle to the new scope |
| Anyone | Moved to a company outside the ICP | Nobody | Log it, update the CRM, no outreach |

Write each route as a CRM task (or a Slack message) that carries the old company, the new company, the title, the relationship and the evidence link. Never enroll a mover into an automated sequence from this flow; a person writes the first note.

## 6. Writing to a mover

The note itself is written with the `cold-email-copywriting` skill. Sample for a former champion:

> Subject: Congrats on Northwind
>
> Hi Dana, congrats on the new role at Northwind. When we rolled out the reporting project at Acme, your team cut month-end close from nine days to four. If Northwind's finance team is wrestling with the same close, I'd be glad to share what we changed and what we'd skip next time. Worth 15 minutes in the next couple of weeks?

## 7. Running it every month

n8n, monthly Schedule Trigger:

1. Read the watch list rows due for a check (CRM search or a sheet).
2. HTTP Request per row: the `socialUrl` lookup, Batching 1 item per 1,000 ms, Retry On Fail on (GET only).
3. Code node: normalize and classify per section 4.
4. IF on classification: job-change candidates and promotions go on; the rest only update `last_checked_at`.
5. CRM node: create the task for the owner in section 5, with the evidence fields.
6. Once a month, collect every confirmed mover with no email into one `find_emails` run and every database email into one `validate_emails` run (the webhook pattern in `references/automation-recipes.md`).

### The same loop in a Clay table

One row per watched person, imported from the CRM with the section 1 columns. Rerun the lookup column once a month; database re-fetches cost $0 in wallet.

| Order | Column | Type and setting | Run condition |
|---|---|---|---|
| 1 | `sc_lookup` | HTTP API, GET `https://app.scrapercity.com/api/v1/database/leads`, query `socialUrl` = `{{linkedin_url}}`, `limit` = `1`; ScraperCity header account; request limit 1 per 1,000 ms | `!!{{linkedin_url}}` |
| 2 | `db_domain`, `db_title` | Field extraction from `sc_lookup.data`, using the company and title keys seen in the first response | `sc_lookup` has data |
| 3 | `change_class` | Formula: `!{{db_domain}} ? "unknown" : {{db_domain}}.toLowerCase().replace("www.", "") !== {{stored_company_domain}}.toLowerCase().replace("www.", "") ? "candidate" : {{db_title}} !== {{stored_title}} ? "title_change" : "no_change"` | Always |
| 4 | `alert` | The CRM's Clay action, or an HTTP API column to an n8n webhook, that creates the section 5 task with old and new company, title and relationship | `change_class` is `candidate` or `title_change` |

A `title_change` row is a promotion or a function change; the owner reads the two titles and decides which (section 4). Movers still go into the one monthly `find_emails` and `validate_emails` runs, outside the per-row columns.

## 8. Measure

| Metric | Formula |
|---|---|
| Change rate | candidates / people checked, per segment per month |
| Confirmation rate | confirmed moves / candidates (shows how far the database lags) |
| Response time | median hours from task created to task completed, per route |
| Meetings and pipeline | meetings and opportunity value sourced from mover tasks |
| Risk cases opened | customer accounts flagged after a champion left |
| Replacements mapped | old accounts with a named person in the departed seat / departures |
| Cost | `find_emails` and `validate_emails` spend for the month |

## 9. Illustrative example

_Illustrative example. Counts are invented to show the arithmetic; prices are catalog prices._

A SaaS company on Growth watches 600 champions and power users monthly.

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| `query_lead_database` by `socialUrl`, 600 people | 600 | included | $0.00 |
| Candidates at about 1.4% a month (BLS-based estimate, section 2) | 8 | | |
| `validate_emails` on movers whose record carries an email (assume 5) | 5 | $0.00169 | $0.01 |
| `find_emails` on the other 3 | 3 | $0.05 | $0.15 |
| Replacement lookups at the 8 old accounts by `companyDomain` + title | 8 | included | $0.00 |
| **Monthly total** | | | **$0.16** |

600 lookups at one a second take 10 minutes of a single n8n run. Most of the cost is owner time on about 16 tasks a month (8 movers, 8 replacement checks), so keep the out-of-ICP rule in section 5 strict.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/api-docs
- https://scrapercity.com/integrations/n8n
- https://www.bls.gov/news.release/tenure.nr0.htm
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- https://university.clay.com/docs/formula-generator
