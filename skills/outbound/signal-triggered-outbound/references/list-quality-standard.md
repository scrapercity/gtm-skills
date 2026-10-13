# List Quality Standard

The shared bar for every list a skill in this repo hands to a user: B2B contact lists, company lists, local business lists and send-ready cold email files. Each list-building skill points here instead of restating these rules. When a skill's own reference is stricter, the stricter rule wins.

Thresholds marked "house standard" are ScraperCity's operating defaults. They are starting points to test against your own bounce and reply data, dated 2026-10. Thresholds attributed to a mailbox provider or a law come from the source named next to them.

## 1. How to use this file

| Moment | Section to apply |
|-|-|
| Designing the output CSV before the first pull | 2 Required columns |
| Right after each download or database page | 3 Normalization |
| Before merging sources or appending to an old list | 4 Dedupe keys and precedence |
| After `validate_emails` finishes | 5 Validation statuses |
| Before any campaign launch or re-launch | 6 Freshness, 7 Suppression |
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
| `mobile` | If present | E.164. Keep separate from `phone`; mobiles carry TCPA consent rules for calls and texts in the US. |
| `linkedin_url` | Recommended | `https://www.linkedin.com/in/<slug>` lowercase, no query string, no trailing slash. |
| `company_name` | Yes | Display name as the source gave it, trimmed. |
| `company_domain` | Yes | Registrable domain per 3e, for example `acme.com`. |
| `company_industry` | Recommended | Source value, unmodified. |
| `company_employees` | Recommended | Integer. |
| `company_revenue` | Optional | Integer USD. |
| `company_city`, `company_state`, `company_country` | Recommended | HQ location; state as USPS 2-letter code for US; country as ISO 3166-1 alpha-2. |
| `person_city`, `person_state`, `person_country` | Recommended | Where the person sits, which can differ from HQ. Drives time zone and law (CASL, PECR, GDPR). |
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
2. Lowercase for the dedupe key. RFC 5321 section 2.4 allows a case-sensitive local-part, but Gmail, Microsoft 365 and nearly every corporate server treat it case-insensitively, so lowercasing the full address for matching is safe; send to the lowercased form.
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

Dedupe inside each source first, then across sources. Run it before validation so you never pay $0.0072 twice for the same address.

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

When a skill must keep one whole record (for example TAM builds that keep the most complete record per business), score each candidate: email 3, `email_status = valid` 2, named contact 2, phone 1, website 1, full street address 1, rating and reviews 1. Keep the highest score; break ties by newer `pulled_at`.

## 5. Validation statuses and what to do with each

Run `validate_emails` ($0.0072 per email) on every address that did not come from `find_emails` within the last 30 days (Email Finder results are validated at lookup time per its tool description). Validator outputs vary by tool version; read the header row of the downloaded CSV and map each raw result into these buckets. Keep the raw value in `email_status_raw`.

| Bucket (`email_status`) | Typical raw meanings | Cold email action | Other uses |
|-|-|-|-|
| `valid` | Deliverable, mailbox confirmed, SMTP accepted | Send-ready file | CRM import |
| `catch_all` | Accept-all domain, server accepts any address, mailbox not confirmable | Separate catch-all file. Send only from a separate campaign at no more than 10% of a day's volume, watch bounces daily (house standard) | Fine for direct mail matching or ads audiences |
| `unknown` | Timeout, greylisting, server did not answer | Hold. Re-validate once after 72 hours; still unknown after that goes to the catch-all file rules or is dropped | Keep for phone outreach |
| `invalid` | Mailbox does not exist, domain has no MX, syntax error | Remove from every send file. Add to the bounce suppression list | Try `find_emails` with name and domain for a replacement |
| `disposable` | Temporary inbox provider | Remove and suppress | None |
| `spamtrap` or `abuse` (if the validator reports it) | Known trap or complainer | Remove and suppress permanently | None |

`is_role = true` is a flag on top of a bucket, not a bucket. A valid `info@` on a dentist list is sendable; on a named-VP list it is a fallback only.

If more than 15% of a source's emails come back `invalid`, stop and check the source before validating more of it; a bad batch usually means an old export, a wrong domain column or a scraped page of support addresses (house standard).

## 6. Freshness

| Field | Max age before re-check (house standard) | Why |
|-|-|-|
| `email_status` before the first send of a campaign | 30 days | Mailboxes close when people leave; a 30-day window keeps the bounce estimate close to the validation result. |
| `email_status` for a re-launch to the same list | Re-validate if older than 30 days | Same reason. Cost is $7.20 per 1,000. |
| `title` and `company_name` | 90 days | Job changes. |
| Local business phone, website, hours | 180 days | Closures and moves. |

A rough decay model: the US Bureau of Labor Statistics reported median employee tenure of 4.1 years in January 2026. If departures were spread evenly, that implies roughly 1.4% of a contact list changing employer each month, about 15% a year. Treat this as a floor for planning; promotions, title changes and company closures add to it. Measure your own bounce rate per list age and replace this estimate.

Use `excludeDelivered=true` on `query_lead_database` and `query_local_business_database` for daily or weekly incremental pulls, so a scheduled job only returns records the account does not already have.

## 7. Suppression lists

Apply suppression after dedupe and before validation (no point paying to validate a row you will drop). Match in this order: exact email, then domain, then `business_name_key`.

| List | Match on | Source of truth | Rule |
|-|-|-|-|
| Unsubscribes and opt-outs | email, and domain if the person asked to block their company | Sequencer export plus reply inbox | Permanent. CAN-SPAM requires honoring opt-outs within 10 business days and keeping the mechanism working for 30 days after a send (FTC). Gmail and Yahoo expect bulk senders to process one-click unsubscribes within 2 days. CASL sets 10 business days. |
| Hard bounces | email | Sequencer bounce log, `invalid` validator results | Permanent for that address. |
| Spam complaints | email and domain | Sequencer, feedback loops | Permanent. |
| Current customers | domain | CRM | Exclude from prospecting lists unless the campaign is an expansion play. |
| Open opportunities | domain | CRM | Exclude; the account owner works them. |
| Competitors and partners | domain | Maintained by the user | Exclude. |
| Do-not-contact accounts | domain | Legal or leadership | Exclude. |
| Contacted in the last N days | email | Sequencer | House standard: 90 days between cold sequences to the same person. |
| Jurisdiction rules | `person_country` | Section 7a | Route or exclude per law. |

### 7a. Jurisdiction routing

| Recipient | Rule of thumb | Source |
|-|-|-|
| US business address | CAN-SPAM: no B2B exemption; truthful headers and subject, physical address, working opt-out. | FTC CAN-SPAM guide |
| Canada | CASL: needs consent. Implied consent can apply to a conspicuously published business address when the message relates to the person's role and the posting does not refuse unsolicited mail. Keep where you found the address. | CRTC CASL FAQ |
| UK corporate subscriber (company, LLP, government body) | PECR allows B2B marketing email without prior consent; identify yourself and give an opt-out. Sole traders and some partnerships are treated as individuals and need consent. | ICO guide to PECR |
| EU | GDPR applies to named business addresses; document a legitimate interest assessment and national e-privacy rules before sending. | Outbound compliance primer |

See `references/outbound-compliance-primer.md` for the full treatment. Nothing here is legal advice.

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
| `email_status` in the send file | 100% `valid` | House standard; catch-all and unknown live in their own files. |
| Invalid, disposable, spamtrap rows | 0 | Yahoo asks senders to remove invalid recipients promptly; Microsoft's May 2025 high-volume sender rules list removing invalid addresses as list hygiene. |
| `email_validated_at` within 30 days of first send | 100% of rows | House standard (section 6). |
| Duplicate emails | 0 | Section 4. |
| Suppression matches | 0 | Section 7. |
| Rows missing `first_name` in a personalized campaign | 2% or less | House standard; the rest go to a non-personalized variant. |
| Role addresses on a named-contact B2B list | 5% or less | House standard. Local business lists are exempt. |
| Contacts per company domain per campaign | 3 or fewer for B2B; 1 per location for local | House standard; more than that reads as spam to the company's admin and raises complaint risk. |
| Required columns (section 2) populated | 100% for required fields | This file. |
| Projected hard bounce rate | Under 2% | House target. Instantly auto-pauses a campaign above 5% bounces after 200 sends by default; Smartlead lets you set the pause threshold. Stay well below the pause line. |
| Spam complaint rate after launch | Under 0.1%, never 0.3% | Google sender guidelines; Yahoo uses 0.3%. |

## 10. QA sample before delivery

Pull 20 random rows (or 2% of the file, whichever is larger, up to 50) and check by hand:

1. Name and title belong together and match the company (open the LinkedIn URL or company team page for 5 of them).
2. Domain resolves to the company's real site, not a parked page or a platform host.
3. Title fits the ICP; no assistant, intern, former, retired or "to the" titles slipped through.
4. Location fits the filter.
5. Phone formatted as E.164.

Two or more misses in a 20-row sample means the filter or mapping is wrong. Fix the query and re-pull rather than hand-patching rows.

## 11. Delivery report block

Every list skill ends its deliverable with this funnel, numbers that add up from top to bottom:

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

- FTC, CAN-SPAM Act: A Compliance Guide for Business: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FTC, Complying with the Telemarketing Sales Rule (B2B call exemption): https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Gmail security and spam protection announcement (Oct 2023): https://blog.google/products/gmail/gmail-security-authentication-spam-protection/
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders (2025): https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Instantly, High bounce auto-pause feature: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Smartlead, High bounce rate auto protection: https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- ICO, Guide to PECR, electronic mail marketing: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/
- CRTC, CASL frequently asked questions: https://crtc.gc.ca/eng/com500/faq500.htm
- IETF RFC 5321, Simple Mail Transfer Protocol, section 2.4: https://datatracker.ietf.org/doc/html/rfc5321#section-2.4
- Twilio, What is E.164: https://www.twilio.com/docs/glossary/what-e164
- Public Suffix List: https://publicsuffix.org/
- US Bureau of Labor Statistics, Employee Tenure (January 2026): https://www.bls.gov/news.release/tenure.nr0.htm
- ScraperCity tool catalog: references/scrapercity-catalog.md
