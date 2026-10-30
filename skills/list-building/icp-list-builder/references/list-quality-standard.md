# List Quality Standard

The shared bar for every list a skill in this repo hands to a user: B2B contact lists, company lists, local business lists and send-ready cold email files. Each list-building skill points here instead of restating these rules. When a skill's own reference is stricter, the stricter rule wins.

Every number here names its source (a mailbox provider, a sending tool, a published dataset or a named operator). Where no published source sets a number, the rule is a setting the user fills in from their own bounce and reply data, and the deliverable records the value used.

## 1. How to use this file

| Moment | Section to apply |
|-|-|
| Designing the output CSV before the first pull | 2 Required columns |
| Right after each download or database page | 3 Normalization |
| Before merging sources or appending to an old list | 4 Dedupe keys and precedence |
| After `validate_emails` finishes | 5 Validation statuses |
| Before any campaign launch or re-launch | 6 Freshness, 7 Suppression |
| Scheduling re-pulls of a list you keep (TAM, CRM, account universe) | 6a Refresh cadence |
| Final gate before handing a file to a sequencer | 9 Acceptance thresholds, 10 QA sample |

## 2. Required columns

Column names are snake_case, lowercase, stable across runs, so a file built in March merges with one built in October without remapping. Keep the raw value columns that a source returns in a separate `raw_` file if you need an audit trail; the delivered file uses this schema.

### 2a. Person-level list (B2B contacts)

| Column | Required | Format and rule |
|-|-|-|
| `first_name` | Yes | Normalized per 3a. Blank only if the source had no name; such rows cannot go to a personalized sequence. |
| `last_name` | Yes | Normalized per 3a. |
| `title` | Yes | Raw title as the source gave it, trimmed. |
| `title_normalized` | Recommended | Lowercase, abbreviations expanded per 3d. Used for matching and QA, never in copy. |
| `seniority` | Recommended | One of: owner, founder, c_suite, partner, vp, head, director, manager, senior, entry. |
| `department` | Recommended | sales, marketing, engineering, operations, finance, hr, it, customer_success, product, legal, executive, other. |
| `email` | Yes for email lists | Trimmed, lowercased for matching (3b). |
| `email_status` | Yes for email lists | One of the buckets in section 5. Never blank on a delivered email list. |
| `email_validated_at` | Yes for email lists | ISO date `YYYY-MM-DD` of the validation run. |
| `phone` | If present | E.164 per 3c. Company or direct line. |
| `mobile` | If present | E.164. Keep separate from `phone`: a mobile is a person's own line, and call lists read it against the do-not-contact list in section 7. |
| `linkedin_url` | Recommended | `https://www.linkedin.com/in/<slug>` lowercase, no query string, no trailing slash. |
| `company_name` | Yes | Display name as the source gave it, trimmed. |
| `company_domain` | Yes | Registrable domain per 3e, for example `acme.com`. |
| `company_industry` | Recommended | Source value, unmodified. |
| `company_employees` | Recommended | Integer. |
| `company_revenue` | Optional | Integer USD. |
| `company_city`, `company_state`, `company_country` | Recommended | HQ location; state as USPS 2-letter code for US; country as ISO 3166-1 alpha-2. |
| `person_city`, `person_state`, `person_country` | Recommended | Where the person sits, which can differ from HQ. Drives send time, call windows and language. |
| `source` | Yes | Controlled vocabulary in section 8. |
| `source_detail` | Yes | Query fingerprint or run id, for example `lead_db:title=VP Sales;keywords=saas;emp=50-200` or `run:8f3a...`. |
| `pulled_at` | Yes | ISO date the record was retrieved. |
| `segment` | Recommended | The ICP slice or campaign this row belongs to, for example `saas-50-200-vp-sales`. |

### 2b. Business-level list (companies or local businesses)

| Column | Required | Format and rule |
|-|-|-|
| `business_name` | Yes | Display name, trimmed, emojis and trailing location tags like " - Downtown" kept (they help the rep), legal suffix kept. |
| `business_name_key` | Yes | Matching key per 3f. Never shown to a prospect. |
| `category` | Yes | Primary category from the source. |
| `website` | Yes for email lists | Full URL as given. |
| `domain` | Yes when a website exists | Registrable domain per 3e. Blank for social-only "websites" (facebook.com, instagram.com, linktr.ee, yelp.com, business.site); keep the URL in `website`. |
| `email` | Yes for email lists | Lowercased for matching. |
| `email_status` | Yes for email lists | Section 5 buckets. |
| `email_validated_at` | Yes for email lists | ISO date. |
| `phone` | Recommended | E.164. |
| `contact_name`, `contact_title` | If present | Named person at the business when the source has one. |
| `street`, `city`, `state`, `postal_code`, `country` | Yes for local lists | USPS state code, 5-digit ZIP as text (keep leading zeros: `02116`). |
| `rating` | If present | Decimal 1.0 to 5.0. |
| `reviews` | If present | Integer. |
| `employees` | B2B company lists | Integer. |
| `source`, `source_detail`, `pulled_at`, `segment` | Yes | As in 2a. |

Keep company rows and person rows in two files joined on `company_domain` (person) to `domain` (company). A firmographic refresh then updates one company row instead of every contact at it, and the per-domain cap and account tiers read from the company file.

Store ZIP codes, phone numbers and IDs as text. Spreadsheet apps strip leading zeros and turn long digit strings into scientific notation; open CSVs with the import wizard or in a script, never by double-click.

## 3. Normalization

Normalize every page or download as it arrives, before merging. Keep the original value in a `raw_` column only when a client asks for an audit trail.

### 3a. Person names

1. Trim, collapse internal whitespace, remove emojis, quotes and surrounding punctuation.
2. Case: change only names that arrive ALL CAPS or all lower. Title-case those, then restore known particles and prefixes: `van`, `von`, `de`, `da`, `del`, `der`, `la`, `le` stay lowercase mid-name; `Mc` and `Mac` capitalize the following letter only for `Mc` (MacDonald is ambiguous, leave as given); apostrophes capitalize the next letter (`O'Brien`, `D'Angelo`). Leave mixed-case names alone (`DeShawn`, `McKenzie`, `deMarco`).
3. Move credentials and generational suffixes out of `last_name`: `MBA`, `CPA`, `PhD`, `MD`, `DDS`, `DMD`, `Esq`, `PE`, `PMP`, `Jr`, `Sr`, `II`, `III`. Put them in a `credentials` column if the copy will use "Dr." for clinicians.
4. If `first_name` holds an initial only (`J.`) or a nickname in parentheses (`Robert (Bob)`), keep the preferred name (`Bob`) when present, otherwise flag the row for manual review before a personalized send.
5. Never invent a first name from an email local-part like `jsmith@`. Leave it blank and route the row to a non-personalized segment.

### 3b. Emails

1. Trim, strip `mailto:`, surrounding brackets and trailing punctuation.
2. Lowercase for the dedupe key. RFC 5321 section 2.4 allows a case-sensitive local-part, but Gmail, Microsoft 365 and corporate servers in common use treat it case-insensitively, so lowercasing the full address for matching is safe; send to the lowercased form.
3. Do not strip `+tags` or Gmail dots for sending. For the dedupe key only, a consumer Gmail address can drop dots and `+tag`; corporate addresses keep them.
4. Reject syntax failures (no `@`, spaces, two `@`, missing TLD) before paying to validate them; mark `email_status = invalid` with reason `syntax`.
5. Flag role accounts with `is_role = true` when the local-part is one of: info, contact, hello, admin, office, sales, support, help, team, billing, accounts, marketing, careers, jobs, hr, noreply, no-reply, webmaster, enquiries, reception, frontdesk, appointments. Role addresses are normal on local business lists and a weaker choice on named-contact B2B lists (section 9).

### 3c. Phones to E.164

E.164 (ITU-T) is `+`, country code, then the national number, 15 digits maximum.

1. Split off extensions first (`x123`, `ext. 123`, `#123`) into `phone_ext`.
2. Strip everything except digits and a leading `+`.
3. US and Canada: 10 digits becomes `+1` plus the 10; 11 digits starting with `1` becomes `+` plus the 11. Area code and exchange must not start with 0 or 1; otherwise blank the field and flag.
4. Other countries: use the row's country to add the code, drop the trunk `0` (UK `020 7946 0018` becomes `+442079460018`). If the country is unknown, leave the number as given and flag it rather than guessing.
5. More than 15 digits after the plus, or fewer than 8: blank and flag.
6. Keep `phone` (switchboard or main line) and `mobile` in separate columns. Never copy a business main line into `mobile`.

### 3d. Titles

Keep the raw title for display. Build `title_normalized` for matching:

| Raw token | Normalized |
|-|-|
| VP, V.P., Vice-President | vice president |
| SVP, Sr. VP | senior vice president |
| EVP | executive vice president |
| Dir, Dir. | director |
| Mgr, Mngr | manager |
| Sr, Sr. | senior |
| Jr, Jr. | junior |
| Head of | head of (kept as is) |
| CRO, CMO, CFO, COO, CTO, CIO, CISO, CEO, CPO | expand to the full chief title and keep the acronym in a second token |
| Ops | operations |
| BizDev, BD | business development |
| & , / , + | " and " |

Then derive `seniority` and `department` from `title_normalized` with keyword rules. A title that maps to two departments ("VP Sales and Marketing") gets the first one listed and keeps both in `title`.

### 3e. Domains

1. Lowercase. Strip scheme, `www.`, `www2.`, `m.`, port, path, query, fragment and trailing dot.
2. Reduce to the registrable domain using the Public Suffix List: `shop.acme.co.uk` becomes `acme.co.uk`, `blog.acme.com` becomes `acme.com`.
3. Blank the domain (keep the URL in `website`) when the host is a platform, not the business: facebook.com, instagram.com, linkedin.com, yelp.com, google.com, business.site, sites.google.com, linktr.ee, wixsite.com subdomains, square.site, godaddysites.com, myshopify.com when a custom domain is also known.
4. A company with several brands keeps one row per domain. Do not collapse `acme.com` and `acmehealth.com` unless the source says they are the same company.

### 3f. Business name key

For matching only: lowercase, remove punctuation, `&` to `and`, collapse whitespace, then drop trailing legal suffixes (inc, incorporated, llc, l.l.c, ltd, limited, co, corp, corporation, company, plc, gmbh, sa, srl, bv, pty, pllc, pc, pa, lp, llp) and a leading `the`. Keep location words; "Smile Dental Austin" and "Smile Dental Round Rock" are different practices.

### 3g. Locations

US states as USPS 2-letter codes. Countries as ISO 3166-1 alpha-2 (US, CA, GB, DE, AU). When calling `query_lead_database`, the `country` filter takes full names like "United States" (US, USA, UK, UAE also work per the tool description); normalize after you receive data, not in the filter.

## 4. Dedupe keys and precedence

Dedupe inside each source first, then across sources. Run it before validation so you never pay $0.00169 twice for the same address.

### 4a. Keys, in the order they are tried

| Entity | Key 1 | Key 2 | Key 3 | Key 4 |
|-|-|-|-|-|
| Person | `email` (lowercased) | `linkedin_url` (normalized) | `first_name + last_name + company_domain` (lowercased) | `first_name + last_name + business_name_key` |
| Company (B2B) | `company_domain` | `business_name_key + company_state` | | |
| Local business | `domain` | `phone` (E.164) | `business_name_key + postal_code` | `business_name_key + street` |

A row matches if any key matches a key on an existing row. Chains: two locations of one franchise share a domain but have different phones and addresses. For local lists where each location is a separate prospect, set Key 1 to `phone` and use `domain` only to cap contacts per brand (section 9).

### 4b. Survivorship when two rows match

Field by field, keep the value from the higher row in this order:

1. A value with `email_status = valid` beats any other email status, and a newer `email_validated_at` beats an older one.
2. Non-empty beats empty.
3. Source precedence for the field: user-supplied CRM data > `email_finder` / `website_finder` (found against a named person and domain) > `lead_db` / `local_db` > `apollo` > `maps` / `yelp` / `angi` / `store_leads`.
4. Newer `pulled_at` beats older.

The merged row's `source` lists every contributing source joined with `|`, for example `local_db|maps`. Report how many rows each source contributed before and after dedupe.

### 4c. Completeness score (tie-breaker)

When a skill must keep one record intact (for example TAM builds that keep the most complete record per business), score each candidate: email 3, `email_status = valid` 2, named contact 2, phone 1, website 1, full street address 1, rating and reviews 1. Keep the highest score; break ties by newer `pulled_at`.

## 5. Validation statuses and what to do with each

Run `validate_emails` ($0.00169 per email) on every address that did not come from `find_emails` in this pull (Email Finder results are validated at lookup time per its tool description). Read the header row of the downloaded CSV before mapping, since columns can change between versions, and keep the raw value in `email_status_raw`.

ScraperCity's Email Validator reports the result in `email_result` (per scrapercity.com/email-validator, checked 2026-10-12). Map it like this:

| Raw `email_result` | Bucket (`email_status`) |
|-|-|
| `valid` | `valid` |
| `valid_catch_all` | `catch_all` |
| `unknown` | `unknown` |
| `invalid` | `invalid` |
| `disposable` | `disposable` |

Other validators use other words ("accept_all", "risky", "deliverable"); map them by meaning with the table below.

| Bucket (`email_status`) | Typical raw meanings | Cold email action | Other uses |
|-|-|-|-|
| `valid` | Deliverable, mailbox confirmed, SMTP accepted | Send-ready file | CRM import |
| `catch_all` | Accept-all domain, server accepts any address, mailbox not confirmable | Hold file. After the valid file's test cell passes, send it as its own 100-contact cell and release the rest only while bounces stay under 2% (section 10) | Fine for direct mail matching or ads audiences |
| `unknown` | Timeout, greylisting, server did not answer | Hold. Re-validate once on a later day; still unknown after that goes to the catch-all file rules or is dropped | Keep for phone outreach |
| `invalid` | Mailbox does not exist, domain has no MX, syntax error | Remove from every send file. Add to the bounce suppression list | Try `find_emails` with name and domain for a replacement |
| `disposable` | Temporary inbox provider | Remove and suppress | None |
| `spamtrap` or `abuse` (if the validator reports it) | Known trap or complainer | Remove and suppress permanently | None |

`is_role = true` is a flag on top of a bucket, not a bucket. A valid `info@` on a dentist list is sendable; on a named-VP list it is a fallback only.

Alex Berman aims for 95% or more valid on a list he sends (alexberman.com, B2B lead generation). When one source's batch comes back far below that, stop and check the source before validating more of it; a bad batch usually means an old export, a wrong domain column or a scraped page of support addresses.

## 6. Freshness

| Field | When to re-check | Basis |
|-|-|-|
| `email_status` before the first send of a campaign | Validate before sending | Alex Berman: verify addresses before you send and keep bounces under 2% (alexberman.com, cold email templates). Cost is $1.69 per 1,000. |
| `email_status` for a re-launch to the same list | Re-validate before the re-launch | Same. |
| `title` and `company_name` | At the interval the user sets from the decay rate below | Job changes. |
| Local business phone, website, hours | At the interval the user sets from the change rate measured at the last refresh | Closures and moves. |

Decay rates to plan with: ZeroBounce's 2025 Email List Decay Report (its 2024 verification data) found email databases degrade by at least 28% a year, which compounds to about 2.7% a month (1 - 0.72^(1/12)). The US Bureau of Labor Statistics reported median employee tenure of 4.1 years in January 2026; if departures were spread evenly, roughly 1.4% of a contact list changes employer each month. Divide the share of stale rows the user will accept by the monthly rate to get a re-check interval, then replace the rate with the bounce rate the user measures by list age.

### 6a. Refresh cadence by data type

How often to re-pull or re-check each kind of data on a list you keep using (a TAM file, a CRM, an account universe). Where no source sets the cadence, the user sets it and the next refresh tests it.

| Data type | Fields | Refresh cadence | How | Basis |
|-|-|-|-|-|
| Firmographic | `company_industry`, `company_employees`, `company_revenue`, HQ location | The user's interval | `query_lead_database` with `companyDomain` and `limit: 1` per account; owned records re-fetch free | Set from the change rate at the last refresh |
| Technographic | Technologies, apps, ecommerce platform, plan | The user's interval | Tech Stack Search (`scrape_builtwith`, $4.99 per technology) or a narrow `scrape_store_leads` re-pull | Set from the change rate at the last refresh; see `signal-triggered-outbound` when the tech change is the trigger |
| CRM dedupe | Duplicate people (key 1 to 4 in 4a) and companies (domain) | Before each import into the CRM | Export, run section 4 keys, merge in the CRM's own tool | Duplicates mean the same person gets two sequences |
| Person role and employer | `title`, `company_name`, `company_domain` | The user's interval | Lead Database by `socialUrl` or `companyDomain` | ZeroBounce and BLS decay rates above |
| Email deliverability | `email_status`, `email_validated_at` | Before any send | `validate_emails` at $0.00169 each | Alex Berman: verify before sending |
| Local business contact | `phone`, `website`, hours, open or closed | The user's interval | `query_local_business_database` re-pull or `scrape_maps` | Set from the change rate at the last refresh |
| Suppression lists | Unsubscribes, bounces, complaints, do-not-contact requests | Before every send and every call block | Sync from the sequencer, the dialer and the reply inbox into one list | Gmail asks bulk senders to honor unsubscribes within 48 hours and to keep spam rate under 0.3% (Google sender FAQ) |

At each refresh, record the share of a field that changed across the records checked, and set the next interval for that field from it: a field that changed a lot gets a shorter interval, one that barely moved a longer one.

Use `excludeDelivered=true` on `query_lead_database` and `query_local_business_database` for daily or weekly incremental pulls, so a scheduled job only returns records the account does not already have.

## 7. Suppression lists

Apply suppression after dedupe and before validation (no point paying to validate a row you will drop). Match in this order: exact email, then domain, then `business_name_key`. Keep one suppression list that every tool reads (sequencer, dialer, CRM, the next list pull); a person who asked to be removed in one tool and then hears from another tends to click "Report spam", which counts against Google's 0.3% spam-rate line.

| List | Match on | Source of truth | Rule |
|-|-|-|-|
| Unsubscribes and "remove me" replies | email, and domain if the person asked to block their company | Sequencer export plus reply inbox | Permanent. Add the same day, in every tool. Gmail asks bulk senders to honor unsubscribes within 48 hours (Google sender FAQ); a remove request that keeps getting mail turns into a complaint. |
| Internal do-not-contact list | email, phone, mobile | Reps, reply inbox, call notes | Permanent. Anyone who asked not to be called or emailed, logged by whoever heard it. Checked before every call block and every send. |
| Hard bounces | email | Sequencer bounce log, `invalid` validator results | Permanent for that address. |
| Spam complaints | email and domain | Sequencer, feedback loops | Permanent. |
| Current customers | domain | CRM | Exclude from prospecting lists unless the campaign is an expansion play. |
| Open opportunities | domain | CRM | Exclude; the account owner works them. |
| Competitors and partners | domain | Maintained by the user | Exclude. |
| Do-not-contact accounts | domain | Leadership or account owners | Exclude. |
| Contacted in the last N days | email | Sequencer | N is the user's re-contact window. Alex Berman's TAM breakdown sends one email per person per cycle and starts the next cycle 30 to 60 days later with a refreshed message. |

## 8. Source column

`source` uses this controlled vocabulary so lists from different skills merge and report the same way:

| Value | Tool |
|-|-|
| `lead_db` | `query_lead_database` |
| `local_db` | `query_local_business_database` |
| `ecom_db` | Ecommerce Database (REST `GET /api/v1/database/ecommerce`) |
| `apollo` | `scrape_apollo` |
| `maps` | `scrape_maps` |
| `yelp` | `scrape_yelp` |
| `angi` | `scrape_angi` |
| `store_leads` | `scrape_store_leads` |
| `techstack` | `scrape_builtwith` (Tech Stack Search) |
| `website_finder` | `scrape_website_finder` |
| `email_finder` | `find_emails` |
| `mobile_finder` | `find_mobiles` |
| `people_finder` | `find_people` |
| `user_upload` | A CSV or CRM export the user supplied |

`source_detail` holds the query fingerprint (filters as `key=value` pairs separated by `;`) or the run id, so anyone can rerun or audit the pull. Enrichment tools append to `source` rather than replacing it: a Lead Database contact whose email came from Email Finder reads `lead_db|email_finder`.

## 9. Acceptance thresholds for a send-ready list

A file is send-ready only when every row below passes. Anything that fails goes back for fixing; do not "send it and see".

| Check | Threshold | Basis |
|-|-|-|
| `email_status` in the send file | 100% `valid` | Definition of the send file; catch-all and unknown live in their own files. |
| Invalid, disposable, spamtrap rows | 0 | Yahoo asks senders to remove invalid recipients promptly; Microsoft's May 2025 high-volume sender rules list removing invalid addresses as list hygiene. |
| `email_validated_at` before the first send | 100% of rows | Alex Berman: verify before sending (section 6). |
| Duplicate emails | 0 | Section 4. |
| Suppression matches | 0 | Section 7. |
| Rows missing `first_name` in a personalized campaign | 0 | Rows without a first name go to a non-personalized variant. |
| Role addresses on a named-contact B2B list | The user's cap | Local business lists are exempt. |
| Contacts per company domain per campaign | The user's cap for B2B; 1 per location for local | Gartner's B2B Buying Report (2022 survey) puts buying groups at five to 11 people; the cap sets how many of them one campaign reaches. |
| Required columns (section 2) populated | 100% for required fields | This file. |
| Projected hard bounce rate | Under 2% | Alex Berman, alexberman.com cold email templates. Instantly auto-pauses a campaign above 5% bounces after 200 sends by default; Smartlead lets you set the pause threshold. |
| Spam complaint rate after launch | Under 0.1%, never 0.3% | Google sender FAQ; Yahoo uses 0.3%. |

## 10. QA sample and fit scorecard before delivery

Pull a random sample of rows (per tier when the list is tiered) and check each by hand against the brief the list was built for, opening the LinkedIn URL or the company team page. Size the sample from the misfit ceiling: when no row in n misses, the 95% upper limit on the misfit rate is about 3/n for n over 30 (Eypasch et al., BMJ 1995). 60 rows with no misses caps misfits under 5%; 100 rows caps them under 3%. Write the sample size and what it caps in the report.

| Dimension | Pass rule per row | When a row misses |
|-|-|-|
| Title fit | Title is in the agreed title family; no assistant, intern, former, retired or "to the" titles | Add the offending words to `notTitle`, recount, re-pull |
| Company fit | Industry or keywords, business model and employee band match the ICP filters | Tighten `keywords` or `notKeywords`, or add the site check; re-read `search_translation` if a URL was used |
| Location fit | Person country and state match the filter | Check `country` versus `companyCountry`; one is the person, the other is HQ |
| Domain resolves | `company_domain` opens the company's own site, not a parked page or a platform host | Re-run domain normalization; blank platform hosts |
| Person still there | The profile or team page shows the person at the company today | Re-pull with `excludeDelivered` for newer records; re-validate |
| Formatting | Names cased, phone E.164, ZIP as text | Fix the normalizer and re-run it on every row |

The file passes when no miss traces to a filter, mapping or normalizer change; a miss that does means fix the query and re-pull rather than hand-patching rows. Report the sample as "60 of 60 title fit, 59 of 60 company fit..." in one line.

Release a new list as a test cell first. Alex Berman tests a niche with about 100 emails (Lean B2B interview, December 2020). Release the rest once the cell's bounce rate is under 2% (alexberman.com). Catch-all rows follow as their own 100-contact cell under the same line.

After launch, keep reading the list through replies. Sort them into wrong person, referred, not now, not interested and positive. When referral replies from one title family keep naming another title, move the referred-to title into slot 1 and the old title down or out. Not-now replies are timing, not a list error. Change the list or the copy between rounds, never both, so the next round of replies shows which change worked.

## 11. Delivery report block

Every list skill that ran its pulls ends its deliverable with this funnel, numbers that add up from top to bottom. A plan written before any call could run carries no projected funnel or bucket shares: it gives sourced counts, cost ceilings and the dated step that measures each stage.

```text
Matched (pagination.total or run rows)   N0
Pulled                                    N1
After normalization drops (bad rows)      N2
After dedupe                              N3
After suppression                         N4
Validated                                 N4
  valid / catch_all / unknown / invalid / disposable
Send-ready (valid, passes section 9)      N5
Cost: database pulls (plan allowance) + paid tools at catalog prices = $X
```

## Sources

- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Email sender guidelines FAQ (spam rate and 48-hour unsubscribe, checked 2026-10-13): https://support.google.com/a/answer/14229414
- ScraperCity, Email Validator (`email_result` values): https://scrapercity.com/email-validator
- Google, Gmail security and spam protection announcement (Oct 2023): https://blog.google/products/gmail/gmail-security-authentication-spam-protection/
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders (2025): https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Instantly, High bounce auto-pause feature: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Smartlead, High bounce rate auto protection: https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- IETF RFC 5321, Simple Mail Transfer Protocol, section 2.4: https://datatracker.ietf.org/doc/html/rfc5321#section-2.4
- Twilio, What is E.164: https://www.twilio.com/docs/glossary/what-e164
- Public Suffix List: https://publicsuffix.org/
- US Bureau of Labor Statistics, Employee Tenure (January 2026): https://www.bls.gov/news.release/tenure.nr0.htm
- ZeroBounce, Email List Decay Report (February 2025, 2024 data, at least 28% a year): https://www.zerobounce.net/blog/newsroom/press/zerobounce-report-email-list-decay
- Alex Berman, Cold email templates (verify before sending, bounces under 2%): https://alexberman.com/cold-email-templates
- Alex Berman, B2B lead generation (verify every email, 95%+ valid): https://alexberman.com/b2b-lead-generation
- Alex Berman, Map your market, skip the follow-ups (one email per person per cycle, 30 to 60 days between cycles): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Lean B2B, interview with Alex Berman on testing market segments (about 100 emails per niche, December 2020): https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- Eypasch E, Lefering R, Kum CK, Troidl H. Probability of adverse events that have not yet occurred: a statistical reminder. BMJ 1995;311:619 (3/n upper limit for zero events): https://www.bmj.com/content/311/7005/619
- Gartner, B2B Buying Report (buying groups of five to 11 people, 2022 survey): https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- ScraperCity tool catalog: references/scrapercity-catalog.md
