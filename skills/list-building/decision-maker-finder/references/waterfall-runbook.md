# Waterfall Runbook

The step-by-step mechanics behind the decision maker waterfall: cleaning the account list, batching Lead Database calls, ranking candidates into slots, choosing the next tool for each empty slot, building the Website Finder, Email Finder and Mobile Finder payloads, and recovering from failures. Prices and run rules (start, poll, download, error codes) come from `references/scrapercity-catalog.md`.

## 1. Account list preparation

| Input problem | Fix | Tool |
|-|-|-|
| `https://www.acme.com/about` style values | Lowercase, strip scheme, `www.`, path and query, reduce to the registrable domain with the Public Suffix List | Local script |
| Two rows with one domain | Keep one; merge any owner or tier columns | Local script |
| Platform hosts (`facebook.com`, `linkedin.com`, `business.site`, `wixsite.com` subdomains) | Blank the domain; treat the row as name-only | Local script |
| Name only, no domain | `query_lead_database` with `companyName` and `limit: 5`; read `company_website` or the email domain from returned rows | Lead Database, included in plan |
| Name matches several companies | Add `companyState` or `companyCity` from the source row and recount | Lead Database |
| Still unresolved | Keep in the gaps file with reason `no_domain`; do not guess a domain | None |
| Current customers, open deals, competitors | Drop by domain before any search | CRM export |

Domain resolution call:

```json
{"companyName": "Pinecrest Manufacturing", "companyState": ["Ohio"], "limit": 5}
```

Accept the domain only when the returned company name, state and size agree with the source row. Two disagreeing domains means unresolved.

## 2. Lead Database pass

### Batching

`companyDomain` takes a comma-separated list. Pick a batch size and halve it when a call returns 503, which means the search ran too long (`references/scrapercity-platform.md`). Run one call per slot so `seniority` and `title` stay specific to the role. Calls per slot = accounts / batch size, rounded up; multiply by the number of slots.

When the body gets long (many domains plus a long title list), send `POST /api/v1/database/leads` with a JSON body. The package switches to POST past about 6,000 characters and a query string over about 16KB is refused.

### Count first, then page

1. First call per batch: same filters with `limit: 1`. Read `pagination.total`.
2. If `total` is 100 or less, one call with `limit: 100` returns everything.
3. If `total` is over 100, page with `after: "0"`, then each `pagination.next_after` until it is null.
4. Large accounts can return dozens of directors. Tighten with `seniority` or a shorter `title` list before paging through rows you will not rank into a slot.

```json
{"companyDomain": "northbayfoods.example, pinecrestmfg.example, ridgefieldpackaging.example",
 "title": "Director of Quality, Director of Food Safety, QA Manager, Quality Assurance Manager, Plant Manager",
 "notTitle": "assistant, intern, former, retired, coordinator, technician",
 "seniority": ["director"],
 "limit": 100, "after": "0"}
```

Leave `hasEmail` off on the slot calls. Email Finder can still find an email for a person with the right title, at $0.05 per hit, and the miss is free. Turn `hasEmail` on only when the user wants email-ready rows and nothing else.

### Daily allowance

Every record returned is saved to the account; only new records count toward the 100,000 a day allowance. Read `pagination.total` from the count calls; when the sum passes the allowance, split the pull across days by state.

## 3. Ranking candidates into slots

For each domain, group returned people by slot, then rank them by these signals in order (the first difference decides):

1. Title matches the slot's first title exactly (after normalization), then another title in the slot list.
2. Seniority equals the slot's top seniority.
3. Email present.
4. Title names a region or business unit that matches the user's territory.
5. Person country equals company HQ country.
6. Title does not contain "interim", "acting" or "fractional".

Keep the top person as primary and the second as backup. Send to the primary only. Remaining ties go to the newer `pulled_at`.

One person can fit two slots (a COO who also runs quality at a 60-person company). Assign them to slot 1 and leave slot 2 for someone else at the account; never put one person in two rows.

## 4. Branch table for every slot after the database pass

| Slot state | Company size | Next tool | Notes |
|-|-|-|-|
| Person with email | Any | Validation (step 6 of SKILL.md) | Done unless the email fails |
| Person, no email | Any | `find_emails` | Free when not found |
| Empty | Under 50 employees | `scrape_website_finder` with "Owner", then "President" | Small company sites list the owner |
| Empty | 50-1,000 | `scrape_website_finder` with the slot's primary title, then the fallback title | One title per run |
| Empty | Over 1,000 | `scrape_apollo` with an Apollo.io people search for those domains, or Website Finder with a region-specific title | Apollo takes hours to days; use a webhook |
| Email came back `invalid` | Any | `find_emails` with the same name and domain | A replacement often exists when the person still works there |
| Email came back `catch_all` (raw `valid_catch_all`) | Any | Hold file | Do not spend on a second source; the domain accepts everything |
| Still empty after two titles | Any | Gaps file | Stop spending on this slot |

## 5. Website Finder runs

`scrape_website_finder` takes `domains` (array) and one `jobTitle`. It bills $0.0499 per contact found.

Grouping procedure:

1. Collect empty slots after the database pass.
2. Group domains by the jobTitle each slot needs (slot 1 domains with "VP Operations", slot 2 domains with "Director of Quality").
3. One run per group. Record the run id, title and domain count in the run log.
4. After download, match rows back by domain. Domains with no row are misses.
5. Second round: the fallback title on the misses only.

```json
{"domains": ["pinecrestmfg.example", "ridgefieldpackaging.example", "harvestlanebakery.example"],
 "jobTitle": "Director of Quality",
 "autoValidateEmails": false,
 "autoFindMobiles": false}
```

Leave both auto options off. Validation runs once for every source through `validate_emails` at $0.0072 per email, and mobiles go through `find_mobiles` only for the slots the user asked for.

Ceiling per run: domains x $0.0499. A 104-domain run costs at most $5.19.

### Title ladder for second rounds

| Slot 1 primary | Fallback | Slot 2 primary | Fallback |
|-|-|-|-|
| VP Operations | Chief Operating Officer | Director of Quality | Plant Manager |
| VP Sales | Chief Revenue Officer | Director of Sales | Sales Manager |
| VP Marketing | Chief Marketing Officer | Director of Marketing | Marketing Manager |
| CFO | Controller | Controller | Accounting Manager |
| CTO | VP Engineering | Director of Engineering | Engineering Manager |
| IT Director | CIO | IT Manager | Systems Administrator |
| Owner | President | Office Manager | General Manager |
| Managing Partner | Founding Partner | Firm Administrator | Office Manager |

## 6. Email Finder

`find_emails` takes `contacts`, an array of objects with `first_name`, `last_name`, `full_name`, `domain` and `company_name`. It bills $0.05 per email found and nothing on a miss. Found emails are validated at lookup per the tool description, so they skip `validate_emails`.

| Input you have | Send |
|-|-|
| First and last name, domain | `{"first_name": "Lena", "last_name": "Okafor", "domain": "northbayfoods.example"}` |
| One name field | `{"full_name": "Tomas Ruiz", "domain": "harborlinelogistics.example"}` |
| Name and company, no domain | `{"first_name": "Mei", "last_name": "Takahashi", "company_name": "Harvest Lane Bakery"}` (lower match rate; resolve the domain first when you can) |
| Initial only for first name | Skip; find the full name on the company site first |

Split large lists into several runs so a failure only costs one batch's retry. Ceiling: contacts x $0.05.

## 7. Validation

Collect every email from the Lead Database and Website Finder, dedupe on the lowercased address, apply suppression, then send one `validate_emails` run with the array. Map `email_result` into the quality standard's buckets: `valid` to the main file, `valid_catch_all` (bucket `catch_all`) and `unknown` to the hold file, `invalid` and `disposable` removed. For `invalid` rows, the branch table sends the name back to Email Finder.

## 8. Mobile Finder

`find_mobiles` takes `inputs`: work emails or social profile URLs, auto-detected. It bills $0.25 per number found and nothing on a miss.

1. Confirm the call block with the user and run the decision table in `mobile-and-phone-handling.md` before the run.
2. Send only the slots the user asked for, and only rows with a valid email or a profile URL.
3. Store results in `mobile` as E.164. A number that comes back on a business main line stays in `phone`.

Ceiling: inputs x $0.25. For 244 slot 1 contacts that is $61.00; show it and wait for a yes.

## 9. Apollo side path for large accounts

Use when an account has over 1,000 employees and the database returned zero people for a slot.

1. Build a people search on Apollo.io with Filters 1.0 for those domains and the slot's seniority and titles; copy the URL.
2. Before paying, run `query_lead_database` with `url` set to that search and `limit: 1`. If `search_translation` shows the filters applied and `pagination.total` covers the need, pull from the database instead.
3. Otherwise `scrape_apollo` with `url`, `count` (500 minimum, 50,000 maximum) and a `fileName` under 50 characters. Cost: count x $0.0039, so $1.95 at the minimum.
4. The start response can carry a `lead_database` block with matches already in the Lead Database. Pull those first.
5. Register a webhook at app.scrapercity.com/dashboard/webhooks before starting. Without one, check status at most once an hour.

## 10. Output CSV columns

One row per contact. Person columns follow `references/list-quality-standard.md` section 2a; these columns are added for this skill:

| Column | Example | Rule |
|-|-|-|
| `account_domain` | northbayfoods.example | The account the row belongs to; equals `company_domain` unless the person sits at a parent company |
| `slot` | 1 | 1, 2 or 3 from the role plan |
| `buying_role` | Economic buyer | Economic buyer, Champion, Evaluator |
| `found_by` | lead_db | lead_db, website_finder, email_finder, apollo, user_upload |
| `email_status` | valid | Section 5 bucket |
| `email_validated_at` | 2026-10-13 | ISO date |
| `mobile` | +14155550142 | E.164, only when requested |
| `mobile_found_at` | 2026-10-13 | ISO date |
| `backup_contact` | grant.feeney@northbayfoods.example | Second-ranked candidate for the slot, not sent to |

Dedupe keys, in order: lowercased `email`, normalized `linkedin_url`, then `first_name + last_name + account_domain`. The gaps file has one row per account with `slot`, `titles_tried`, `tools_tried` and `reason`.

## 11. Run log and failure handling

Keep one row per run: date, tool, slot, title, input count, run id, status, found, cost, file path.

| Failure | What happened | Action |
|-|-|-|
| 503 on a Lead Database batch | The search ran too long | Halve the batch, shorten the title list, retry |
| 409 `filters_not_applied_yet` | Some company filters cannot be used yet | Drop those filters or retry later |
| 0 rows for a domain the user knows has staff | Domain mismatch (subsidiary, rebrand, regional site) | Search `companyName`; try the parent domain; note the alias |
| Website Finder run FAILED | Read `statusMessage` and logs | Resubmit once; on a second failure split the domain list in half |
| Website Finder returns people with the wrong title | Title matched loosely | Filter rows by title family locally; misses go to the fallback title |
| 402 mid-waterfall | Wallet ran out | `check_wallet`, report the shortfall and which step stopped, resume from the run log |
| 409 on a start | Same request seconds ago | `list_runs` with `hours: 1`; reuse the earlier run id |
| Apollo run still RUNNING after a day | Normal for large counts | Wait for the webhook; do not resubmit |

## 12. Recipe library

Each recipe is the slot 1 Lead Database call; swap `seniority` and `title` for slot 2 from `buying-role-map.md`.

| # | Job | Key filters |
|-|-|-|
| 1 | VP Sales and CRO at SaaS accounts | `"title": "VP Sales, Chief Revenue Officer, CRO, SVP Sales, Head of Sales"`, `"seniority": ["vp", "c_suite"]` |
| 2 | CFO and Controller at mid-market accounts | `"title": "CFO, Chief Financial Officer, VP Finance, Controller"`, `"seniority": ["c_suite", "vp", "director"]` |
| 3 | IT leader at hospitals | `"title": "CIO, Chief Information Officer, VP IT, Director of IT"`, `"notTitle": "assistant, nurse, clinical"` |
| 4 | Owner at small service firms | `"title": "Owner, President, Founder, CEO"`, `"maxEmployees": 50` |
| 5 | Head of People at 200-2,000 employee accounts | `"title": "CHRO, VP People, VP Human Resources, Head of People"` |
| 6 | Engineering leader at developer-tool targets | `"title": "CTO, VP Engineering, Head of Engineering"`, `"department": ["engineering"]` |
| 7 | Plant leadership at manufacturers | `"title": "VP Operations, VP Manufacturing, Plant Manager"`, `"seniority": ["vp", "director"]` |
| 8 | Managing partner at law and accounting firms | `"title": "Managing Partner, Founding Partner, Firm Administrator"` |
| 9 | Ecommerce lead at consumer brands | `"title": "Founder, Head of Ecommerce, Director of Ecommerce, VP Digital"` |
| 10 | Territory owner at enterprises | Slot title plus region, for example `"title": "VP Operations North America"`, with `"state": ["Texas"]` for the person |

Every recipe also carries `companyDomain` (the batch), the universal `notTitle` set and `limit: 1` for the count.

## 13. Cost formulas

```text
lead_db       = 0 wallet (plan allowance)
website_find  = contacts found x 0.0499        ceiling: domains sent x 0.0499
email_find    = emails found x 0.05            ceiling: contacts sent x 0.05
validate      = unique emails x 0.0072
mobiles       = numbers found x 0.25           ceiling: inputs x 0.25
apollo        = count x 0.0039                 minimum count 500
```

Hit rates vary by industry, company size and title, and this repo publishes no fixed rate for any tool. To turn a ceiling into an expected cost, run a test batch first at a size the user picks, take the test's hit rate, and multiply: expected = full input x test hit rate x price. Quote the ceiling to the user with the expected cost next to it, and keep your own hit rates per list type in the run log.

## 14. Committee file (when map-only roles exist)

Map-only roles are found in the same Lead Database pass and cost nothing from the wallet. They go to `decision-makers-[list]-[date]-committee.csv`, never to the sequencer.

| Roles that joined the user's past deals | Map-only roles | `title` for the batch call |
|-|-|-|
| Evaluator only | Slot 3 evaluator from the role map, when the user contacts fewer than 3 slots | The category's slot 3 titles |
| Procurement, IT security, finance | Slot 3 plus the roles named | `Procurement, Purchasing, Sourcing, Information Security, IT Security, Controller, Finance Director` |

Columns: `account_domain`, `first_name`, `last_name`, `title`, `buying_role` (Evaluator, Procurement, Security review, Finance), `email` if returned (not validated, since nobody emails these rows yet), `found_by = lead_db`. When the AE books a meeting, validate the committee emails for that one account ($0.0072 each) before the first send to them.

## 15. Role audit after launch

The user sets the review count and both thresholds before launch.

| Count at the review | Threshold | Action |
|-|-|-|
| Wrong-person answers for one slot title (not-now answers excluded; they are timing) | The user's wrong-person share | Replace the title in the slot; re-run section 2 for accounts not yet contacted |
| Referrals naming another title | The user's referral count | Add that title to the slot's list ahead of the current one |
| Bounces on Website Finder emails versus Lead Database emails | Website Finder bounce rate clearly above the database rate | Validate Website Finder results again before the next send; check the title match rule |

Log the counts in the run log so the next list for the same product starts from the corrected role map.

## Sources

- ScraperCity MCP tool schemas (`query_lead_database`, `scrape_website_finder`, `find_emails`, `find_mobiles`, `scrape_apollo`): https://www.npmjs.com/package/scrapercity
- ScraperCity CLI repository: https://github.com/scrapercity/scrapercity-cli
- ScraperCity, How to use: https://scrapercity.com/how-to-use
- Public Suffix List: https://publicsuffix.org/
- Gartner, B2B Buying Report: https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
