# Waterfall and Cost Control

How to order lookups per field, what each usable result costs, where to cap spend, when to cut a step, and which plan to run the job on. Prices come from `references/scrapercity-catalog.md` and plans from `references/scrapercity-platform.md`. Every hit rate, valid share and survival rate below is a planning assumption until the 50-row pilot in `enrichment-runbook.md` section 4 replaces it.

## 1. Order steps by price per usable result

Three of the paid tools bill only when they find something:

| Tool | Billing (catalog) | Price per hit |
|-|-|-|
| `find_emails` | $0.05 per email found, free if not found | $0.05 at any hit rate |
| `find_mobiles` | $0.25 per number found, free if not found | $0.25 at any hit rate |
| `scrape_website_finder` | $0.0499 per contact found | $0.0499 at any hit rate |

The usual waterfall formula, price per attempt divided by hit rate, applies to tools that bill every attempt. For these three, a miss costs nothing, so the price per hit is the list price and the hit rate only changes total spend and how many rows fall through to the next step. Order by what a usable result costs once validation and post-checks are included:

| Step | What you pay | Cost per usable result |
|-|-|-|
| Lead Database email, then `validate_emails` | $0 wallet on Growth and Scale, plus $0.00169 per address checked | $0.00169 / valid share |
| `find_emails` (validated at lookup per its tool description) | $0.05 per email found | $0.05 |
| `scrape_website_finder` contact, then `validate_emails` | $0.0499 per contact found plus $0.00169 | ($0.0499 + $0.00169) / valid share |
| `find_mobiles` number, then line-type, shared-number and suppression checks | $0.25 per number found | $0.25 / survival share |

Rule: included steps first, then the cheapest usable result, then steps that need a different input (Website Finder for accounts with no named person). No published figure gives the valid share or the survival share; measure both on the first batch and use them for the rest of the run.

## 2. One ladder per field family

Run each family as its own ladder. A row leaves a ladder at the first step that meets the stop condition, so it never pays for a second source of the same field.

| Field family | Step 1 (included on Growth and Scale) | Step 2 | Step 3 | Stop when | Never |
|-|-|-|-|-|-|
| Work email | CRM value if not `invalid`; else Lead Database by `socialUrl`, or by `companyDomain` with a local name match | `validate_emails` on the Lead Database email | `find_emails` with `domain` (or `company_name` when no domain, `full_name` when the name will not split); its misses get one retry with `company_name` in place of a website-derived domain, on its own cost line | A `valid` email; a `catch_all` result is staged and the ladder stops | A pattern-built address (`first.last@`) written as found |
| Mobile (only people at the seniority levels and departments the user will dial, read from the refreshed Lead Database record) | CRM mobile | `find_mobiles` with the LinkedIn URL | `find_mobiles` with the work email, only for the URL misses, in a second run | One number found | Copying a main line into `mobile` |
| Main or direct phone | CRM phone | Lead Database phone (`hasPhone: true` narrows the people call) | Website Finder phone for account-only rows | One number that passes E.164 | Writing a mobile into the main phone field |
| Title, seniority, department, LinkedIn URL | CRM value | Lead Database on a High match | Website Finder title for account-only rows | High match found | Writing a Medium match; it is staged |
| Firmographics: industry, size, revenue, HQ | CRM value | Lead Database `companyDomain` with `limit: 1` (`company_industry`, `company_size`, `employees_count`, `company_annual_revenue`, `company_city`, `company_state`, `company_country`) | The company columns `validate_emails` returns for the domain (`sc_company_name`, `industry`, `size`, `founded`, `location`) when the database has no row or the plan is Starter | All requested company fields filled | Averaging two different sizes; see the size-band rule in `field-precedence-and-overwrite-rules.md` |
| Technographics | CRM value | Tech Stack Search per technology, joined on domain (section 6) | | Each requested technology checked once | Reading "not on the list" as "does not use it" |

The mobile ladder's second run cannot bill one person twice: it only receives people whose URL found nothing, and a miss is free.

## 3. Spend caps

| Cap | How to set it | Where it is enforced |
|-|-|-|
| Per row | The sum of the paid steps a row may enter. A contact allowed into every step costs at most $0.05 (email) + $0.25 (mobile) + $0.00338 (two validations) = $0.30. Mobiles are the lever: keep them to the accounts or stages the user named and, within those, to the seniority levels and departments reps will dial. | Field rule sheet: list which segments enter which paid step |
| Per page | 5 pages of 100 per domain on the Lead Database | Runbook REST loop |
| Per run | Ceiling = every paid lookup hits. Shown before any paid step; over $5 waits for a go-ahead | `check_wallet`, then the user |
| Per month (scheduled jobs) | Records expected per month x per-row cap, agreed with the user | Sum the run log before each batch; `list_runs` only covers the last 168 hours, so keep your own log for the month. Pause the job at 80% of the cap |
| Per key | One API key per automation, so one job's spend can be read and revoked alone | `references/scrapercity-agent-patterns.md` section 10 |

## 4. Step contribution review

After each run, score every step on what it added that earlier steps had not:

| Step | Rows entered | Incremental fills | Cost | Cost per incremental fill |
|-|-:|-:|-:|-:|
| Lead Database by `socialUrl`, `companyDomain` and `companyName` | 611 | 211 emails | $0.00 | $0.00 |
| `validate_emails` | 2,112 | 103 bad existing emails caught | $3.57 | $0.03 per bad address caught |
| `find_emails` pass 1 | 479 | 219 blanks filled, 71 invalid replaced, 2 job changers | $14.60 | $0.05 |
| `find_emails` pass 2, company-name retry | 120 | 18 blanks filled | $0.90 | $0.05 |
| `find_mobiles`, two passes | 385 (290 + 95) | 99 mobiles | $24.75 | $0.25 |
| `scrape_website_finder` | 38 | 27 contacts | $1.35 | $0.05 |

Numbers from the illustrative 2,400-contact run in `examples/worked-example.md`.

Cut or move a step later when its cost per incremental fill is above what the field is worth for the segment. Set that value in the rule sheet as a user input, for example "a mobile is worth $2 on an open opportunity and $0 on nurture", so mobiles never run on nurture. A step that fills almost none of the rows that enter it usually means the rows are wrong for that step (old domains, freemail-only, company pages); check the inputs before the next run.

## 5. Plan choice by volume

| Plan | Price | Monthly credits | What it adds for enrichment |
|-|-:|-:|-|
| Starter | $49 | $49 | Pay-per-result tools only; no Lead Database |
| Growth | $149 | $159 | Lead Database, Local Business Database and Ecommerce Database; 10% bonus on purchased credits |
| Scale | $649 | $800 | Everything in Growth, higher rate limits; 30% bonus on purchased credits |

- When a month's paid tool use reaches $159, Growth's credits cover it, so the databases come at no extra cost over buying the same credits on Starter.
- Below that, the $100 price difference pays for itself when the Lead Database fills 2,000 or more emails a month that would otherwise go to Email Finder ($100 / $0.05 = 2,000), before counting titles, phones and company fields it fills for $0.
- On Starter, fill company fields from the `validate_emails` company columns ($0.00169 per address) instead of buying a database plan for firmographics alone.
- Scale's credits exceed its price by $151. Compare it with Growth plus purchased credits once monthly spend passes about $800, or when the 100 requests a minute limit stretches a backfill across too many hours.

## 6. Technographics with Tech Stack Search

`scrape_builtwith` takes one `technology` and returns the domains detected using it, at $4.99 per technology. To enrich accounts:

1. Pick the technologies the pitch depends on (a competitor, a complementary tool, the platform the integration needs).
2. One run per technology. Normalize each returned domain to the registrable domain.
3. Join to CRM accounts on `company_domain`. Write `uses_<technology> = yes` and `tech_checked_at`. Leave non-matches blank, never `no`: detection misses tools that leave no trace on the public site.
4. Cost does not depend on CRM size: 5 technologies cost $24.95 whether the CRM holds 500 accounts or 50,000.
5. Refresh before each campaign that uses the technology as its trigger.

## 7. Email lookups in detail

| Input the row has | Call | Note |
|-|-|-|
| First name, last name, domain | `find_emails` `{first_name, last_name, domain}` | Best input |
| LinkedIn URL only | Lead Database `socialUrl` first; on a High match take the domain, then `find_emails` | The database row may already carry the email |
| Name and company name, no domain | Lead Database `companyName` to resolve the domain, then `find_emails`; `company_name` in `find_emails` only when no domain resolves | Domain is preferred per the tool schema |
| A full name that will not split into first and last | `find_emails` `{full_name, domain}` | The schema accepts `full_name` in place of first and last |

- CLI batch files: `npx scrapercity email-find --file contacts.csv` needs a header row containing "first" and reads columns by position as first name, last name, domain, company name. It splits on every comma with no quote handling, so "Acme, Inc." or "Smith, Jr." shifts the columns. Strip commas from those fields or send the batch as JSON through MCP or REST.
- A miss is recorded as `NOT_FOUND`. No address is built from a naming pattern and written as found.
- Format check, for ranking only: at a domain with several `valid` addresses, note the dominant local-part format (`first.last`, `flast`, `first`). A `catch_all` result that matches it goes to the front of the catch-all send order; one that breaks it goes to the back.
- One person or a handful of names: send them in one `find_emails` call and return the short-form answer from the SKILL.md Output Format; no report.

## 8. Fields this catalog does not supply

Funding stage and amount, hiring counts, intent topics, SIC or NAICS codes, and web traffic rank are not returned by any tool in the catalog (the Lead Database returns an industry label, not a code). Leave them blank, flag `OUT_OF_CATALOG`, and say so in one line of the report. Never fill them from memory.

## Sources

- ScraperCity tool catalog (prices, billing on found results, `find_emails` and `scrape_builtwith` inputs): references/scrapercity-catalog.md
- ScraperCity platform facts (plans, credits, purchase bonuses, database allowance): references/scrapercity-platform.md
- ScraperCity npm package 1.0.17, `AGENT_DOCS.txt` (Lead Database response fields) and `bin/cli.mjs` (`email-find --file` parsing): https://www.npmjs.com/package/scrapercity
- ScraperCity, Email Validator (company enrichment columns): https://scrapercity.com/email-validator
- ScraperCity, pricing: https://scrapercity.com/pricing
