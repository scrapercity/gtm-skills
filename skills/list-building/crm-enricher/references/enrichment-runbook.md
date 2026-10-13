# Enrichment Runbook

Operational detail for running the lookups: routing, batch sizes, paging limits, the REST loop for large files, the pilot hit-rate method, and the reason codes the report uses.

## 1. Profiling script logic

For each row compute, in this order:

1. `company_domain`: website field normalized to the registrable domain; else the email's domain if not freemail; else blank.
2. `freemail`: true when the email domain is one of gmail.com, googlemail.com, outlook.com, hotmail.com, live.com, yahoo.com, icloud.com, me.com, aol.com, proton.me, protonmail.com, gmx.com, mail.com, zoho.com, yandex.com.
3. `identifier_class`: the first that applies of `social`, `name_domain`, `name_company`, `email_only`, `account_only`, `no_identifier`.
4. `needs`: the list of in-scope fields that are blank or invalid.
5. `suppressed`: true when an unsubscribe, opt-out, DND or "do not contact" field is set. Suppressed rows skip every step.

Report the counts of each class and of each need before spending anything.

## 2. Routing and batch sizes

| Step | Tool | Batch | Notes |
|-|-|-|-|
| Social lookups | `query_lead_database` `socialUrl` | 1 URL per call, `limit: 5` | Normalize URL: lowercase, `https://www.linkedin.com/in/<slug>`, no query string or trailing slash |
| People at a domain | `query_lead_database` `companyDomain` | 1 domain per call, `limit: 100`, `after` paging | Stop paging when every person you need at that domain is matched, or after 5 pages |
| Company fields | `query_lead_database` `companyDomain` | 1 domain per call, `limit: 1` | Reads industry, size, revenue, HQ from the returned row |
| Name-only companies | `query_lead_database` `companyName` | 1 name per call, `limit: 25` | Read the website from results; if two companies share the name, use HQ state to pick, else flag `AMBIGUOUS_COMPANY` |
| Account-only buyer | `query_lead_database` `companyDomain` + `title` | 1 domain per call, `limit: 10` | Then `scrape_website_finder` for domains with no hit |
| Email validation | `validate_emails` | Up to a few thousand per run | Dedupe first; never pay twice for one address |
| Email Finder | `find_emails` `contacts[]` | 500 contacts per run is easy to track | Domain preferred over company_name |
| Mobile Finder | `find_mobiles` `inputs[]` | 500 per run | One input per person |
| Website Finder | `scrape_website_finder` `domains[]`, `jobTitle` | 100 domains per run, one title | Run again per title if you need two roles |

Each Lead Database row returned is saved to the account and new rows count against 100,000 a day. A 2,000-row export rarely reaches 20,000 rows of lookups, but a run that pages 5 pages at 300 large domains can: 300 x 5 x 100 = 150,000. Cap pages per domain and spread big runs across days.

## 3. MCP versus REST

| Lookups planned | Use |
|-|-|
| Under about 200 database calls | MCP tool calls inside the agent session |
| 200 or more | A script against the REST API, run by the user or the agent's shell |

REST loop shape (pseudocode):

```text
for domain in domains_needing_people:
    after = "0"; pages = 0
    while pages < 5:
        r = GET /api/v1/database/leads?companyDomain={domain}&limit=100&after={after}
        match r.data against the CRM rows for this domain on normalized names and emails
        if every CRM row for the domain is matched: break
        after = r.pagination.next_after
        if after is null: break
        pages += 1
    sleep 0.7 s between calls   (stays under 100 requests a minute)
```

On 429 wait 30 seconds and retry once. On 503 retry once with `limit=25`. Write every response to disk keyed by domain so a crash does not repeat calls.

## 4. Pilot hit-rate method

Email Finder and Mobile Finder charge only on a hit, so the ceiling (every lookup hits) is the worst case and the expected cost depends on the hit rate. ScraperCity does not publish hit rates, and they vary by industry, seniority and region. Measure them:

1. Take a random 50 rows from each paid step's input (stratify by segment if the export mixes very different segments).
2. Run them. Cost is at most 50 x $0.05 = $2.50 for emails and 50 x $0.25 = $12.50 for mobiles.
3. Hit rate = hits / 50. With 50 rows the estimate is rough; give the user a range of plus or minus 14 percentage points (about two standard errors at a 50% rate).
4. Expected cost for the rest = remaining inputs x hit rate x price. Show the ceiling beside it.

## 5. Ordering to avoid paying twice

1. Lead Database before any paid finder.
2. Validate existing emails before `find_emails`, so invalid ones join the finder batch in one run.
3. Remove rows whose email the Lead Database filled (and validation confirmed) from the finder batch.
4. For mobiles, send the LinkedIn URL when you have it, otherwise the email. Never both.
5. Dedupe each paid batch on its input key.

## 6. Reason codes

| Code | Meaning | Next action for the user |
|-|-|-|
| `NO_IDENTIFIER` | No email, social URL, or name plus company | Research by hand or drop |
| `NO_DOMAIN` | Name present, company unknown or freemail only | Add the company, or run `find_people` only if the use is lawful and not outreach-gated |
| `FREEMAIL_DOMAIN` | Only a personal email; employer unknown | Ask the rep, or try the Lead Database by `socialUrl` |
| `NOT_FOUND` | Lookups ran and returned nothing | Retry in 90 days |
| `AMBIGUOUS_MATCH` | Two or more candidates; nothing written | Rep picks from the review file |
| `AMBIGUOUS_COMPANY` | Company name matches several companies | Add domain or state |
| `LOW_CONFIDENCE` | Last-name-only or company mismatch | Review file |
| `RULE_BLOCKED` | A value was found but the field policy kept the CRM value | None, by design |
| `EMAIL_INVALID` | Existing email invalid and no replacement found | Do not email; phone or LinkedIn instead |
| `EMAIL_REPLACED` | Invalid email replaced; old in `prior_email` | None |
| `EMAIL_CONFLICT`, `TITLE_CONFLICT` | Different value found; staged | Rep accepts or rejects |
| `JOB_CHANGE` | Person now at another company | New contact at new company; replacement at old account |
| `OUT_OF_SCOPE` | Field not requested for this segment (often mobiles) | None |
| `SUPPRESSED` | Opt-out, unsubscribe or DND set | Never enrich for outreach |
| `DUPLICATE_IN_CRM` | Another CRM record shares the email or name plus domain | Merge in the CRM |

## 7. Run log

Keep one line per tool run: date, tool, input count, runId, status, hits, cost, output file. The report's cost table is built from this log, not from estimates.

## Sources

- ScraperCity tool catalog: references/scrapercity-catalog.md
- ScraperCity platform facts (daily allowance, saved records): references/scrapercity-platform.md
- ScraperCity agent patterns (rate limits, safe retry): references/scrapercity-agent-patterns.md
- https://scrapercity.com/api-docs
- NIST/SEMATECH e-Handbook, confidence limits for a proportion: https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
