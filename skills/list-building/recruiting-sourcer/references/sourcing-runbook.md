# Sourcing Runbook

Operational steps from role brief to contactable shortlist: source choice, target-company batching, Apollo runs with webhooks, exclusions, ranking and contact enrichment.

## 1. Choosing the source

| Condition | Use | Why |
|-|-|-|
| Growth or Scale plan | `query_lead_database` | Included in the plan; count first with `limit: 1`; cursor paging |
| The client sent an Apollo people-search URL | `query_lead_database` with `url` first | Uses the URL's filters at no wallet cost; `search_translation` lists applied, approximated and unsupported filters |
| Starter plan | `scrape_apollo` | Pay per lead ($0.0039); no database access |
| Lead Database `search_translation` dropped a filter the client insists on | `scrape_apollo` with the same URL | Apollo applies its own filters |
| Fewer than 500 candidates wanted from Apollo | Lead Database, or accept the 500 minimum ($1.95) | `count` ranges 500 to 50,000 |

## 2. Target-company searches

1. Collect the poach list as domains. Use `companyName` only when the domain is unknown, then read the company website from results and switch to the domain.
2. `companyDomain` takes several domains comma-separated. Batch about 10 domains per call so the 100-row page is not dominated by one large company; page with `after` per batch.
3. Keep the same `title`, `notTitle` and `seniority` across batches.
4. Count per batch and record which companies return 0 for the title family (often a naming difference: "Software Engineer, Web" at one company, "UI Engineer" at another).

## 3. Market-wide searches

Add company traits that describe the client's world: `keywords` (fintech, saas, payments), `industry`, `minEmployees` and `maxEmployees`, `revenueMin`, and `notKeywords` or `notIndustry` for segments the client will not hire from (agencies, staffing firms, consultancies if the client wants product experience). Count, then pull with `after` cursors.

| `pagination.total` vs planned long list | Action |
|-|-|
| Under half | Widen: more title terms, drop `keywords`, add nearby cities or remote states |
| Half to 3x | Pull |
| Over 3x | Tighten: seniority, company size, keywords |
| 0 | Remove the newest filter; probe seniority or department values |
| 503 | Fewer title terms, add a state, smaller domain batches |

## 4. Apollo runs

```text
1. Confirm the URL is a people search in Filters 1.0 format.
2. Register a webhook at app.scrapercity.com/dashboard/webhooks.
3. check_wallet; show count x $0.0039; wait for a go-ahead if over $5.
4. scrape_apollo {url, count, fileName}; save the runId.
5. Tell the user the run can take hours to several days; end the session.
6. On the webhook (runId, fileName, leadsCount), call check_run_status to confirm SUCCEEDED, then download_results.
7. If there is no webhook, check at most once an hour.
```

Cost examples: 500 leads $1.95; 1,000 $3.90; 5,000 $19.50; 50,000 $195.00.

## 5. Exclusions, in order

| Step | Match on | Source of truth |
|-|-|-|
| Hiring company and subsidiaries | Registrable `company_domain` and known brand domains | Client |
| Do-not-poach accounts | `company_domain` | Agency's client list and non-solicit agreements |
| Already in the client's ATS or rejected in the last 6 months | Email, LinkedIn URL | Client export |
| Contacted by the agency for another role in the last 90 days | Email | Agency CRM |
| Opted out of contact | Email, LinkedIn URL, phone | Agency suppression list |

Report each count. A domain match also catches people who list a subsidiary brand as their employer only if the subsidiary domain is on the list, so ask for brand domains explicitly.

## 6. QA sample

Read 20 random rows (or 2%, up to 50):

1. Title fits the family and level.
2. Company is plausible for the brief (not an agency when the client wants product experience).
3. Location matches.
4. LinkedIn URL opens to the same person (check 5).

Two or more misfits: fix `notTitle` or the company filters and re-pull, rather than hand-deleting.

## 7. Ranking rubric

| Points | Evidence | Notes |
|-|-|-|
| 40 | Core title family | Adjacent titles (for example Full Stack for a frontend role) get 20 |
| 20 | Seniority matches | One level off gets 10 |
| 20 | Company on the target list | Same industry but not on the list gets 10 |
| 10 | Person in the target metro or time zone | Neighboring metro gets 5 |
| 10 | Company size or stage matches | |

A: 80 to 100. B: 60 to 79. C: under 60. The rubric is applied by the agent and checked by the recruiter; it is a manual sort, not an automated hiring decision. If the client wants an automated score to screen candidates for New York City roles, review Local Law 144 first.

## 8. Contact enrichment

| Step | Who | Tool | Cost |
|-|-|-|-|
| Validate Lead Database emails | A and B | `validate_emails` | $0.0072 each |
| Find missing work emails | A and B | `find_emails` with first name, last name, domain | $0.05 per found |
| Mobiles | A only | `find_mobiles`, LinkedIn URL first, else work email, one input per person | $0.25 per found |

Personal emails are out of scope: Email Finder returns work addresses, and People Finder is a public-records tool that does not belong in candidate workflows.

## 9. Outputs

| File | Contents |
|-|-|
| Shortlist CSV | A and B tiers with contact data |
| Long list CSV | C tier, no paid enrichment |
| Exclusion log | Counts and reasons, no personal data needed |
| Run log | Date, tool, filters or URL, runId, rows, cost |

## Sources

- ScraperCity tool catalog (Apollo count range, prices): references/scrapercity-catalog.md
- ScraperCity platform facts (Lead Database, url parameter, search_translation): references/scrapercity-platform.md
- ScraperCity agent patterns (webhooks, polling): references/scrapercity-agent-patterns.md
- ScraperCity, how to use: https://scrapercity.com/how-to-use
- NYC DCWP final rules summary for Local Law 144: https://perkinscoie.com/en/news-insights/nyc-adopts-final-rules-for-law-governing-automated-employment-decision-tools.html
