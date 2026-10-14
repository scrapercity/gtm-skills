# Field Precedence and Overwrite Rules

The rule sheet the enricher applies field by field. Copy the defaults, change only what the user explicitly decides, and print the final sheet in the report's Field Rules section.

## 1. The five policies

| Policy | Writes to the CRM field? | Keeps the old value? | Typical fields |
|-|-|-|-|
| `fill_blank_only` | Only when the CRM value is empty | Nothing to keep | Email, mobile, title, industry, employees, revenue, HQ location, LinkedIn URL |
| `replace_if_invalid` | Only when validation proves the current value bad | Yes, in `prior_<field>` | Email (validator `invalid`), phone (fails E.164 or wrong digit count) |
| `stage_for_review` | Never; writes `enriched_<field>` | The CRM value is untouched | Title that differs, company that differs, any Medium-confidence value |
| `never_overwrite` | Never | Untouched | Owner, lifecycle stage, lead status, deal fields, notes, subscription status, opt-out, DND, original source |
| `append_new` | Adds a second value | Primary untouched | Second phone, secondary email (HubSpot additional emails, Pipedrive extra email or phone entries) |

A value counts as owner-entered when it is non-empty in the export. The enricher cannot see who typed it, so every non-empty value gets owner protection unless the user names a field as "system-filled, safe to refresh" (for example a field a previous enrichment vendor wrote).

## 2. Default precedence per field

Read left to right: the first source that yields a value at the required confidence wins. "CRM" means the current non-empty CRM value.

| Field | 1st | 2nd | 3rd | 4th | Default policy |
|-|-|-|-|-|-|
| `email` | CRM, if not `invalid` | `find_emails` (validated at lookup) | Lead Database email after `validate_emails` returns valid or catch_all | `scrape_website_finder` email after validation | `fill_blank_only`, plus `replace_if_invalid` |
| `email_status` | New validation result | Prior status if validated within 90 days | | | System field; always write |
| `mobile` | CRM | `find_mobiles` | | | `fill_blank_only` |
| `phone` (main) | CRM | Lead Database phone | Website Finder phone | | `fill_blank_only`; never copy a mobile here |
| `job_title` | CRM, if updated inside the title freshness window | Lead Database title on a High match | Website Finder title | | `fill_blank_only`; differing values `stage_for_review` |
| `linkedin_url` | CRM | Lead Database profile URL on a High match | | | `fill_blank_only` |
| `company_name` | CRM | Lead Database company on a High match | | | `stage_for_review` when different (job change test) |
| `company_domain` / website | CRM website | Domain from a non-freemail email | Lead Database company website | | `fill_blank_only` |
| `industry` | CRM | Lead Database `company_industry` | `validate_emails` company `industry` column | | `fill_blank_only` |
| `employees` | CRM | Lead Database `employees_count` or `company_size` | `validate_emails` company `size` column | | `fill_blank_only`; a different size band is staged (section 6a) |
| `annual_revenue` | CRM | Lead Database `company_annual_revenue` | | | `fill_blank_only` |
| HQ city, state, country | CRM | Lead Database company HQ | | | `fill_blank_only` |
| `uses_<technology>` | Tech Stack Search domain list for that technology | | | | System field; write `yes` on a match, leave blank otherwise |
| Funding, hiring, intent, SIC or NAICS code | Not supplied by any catalog tool | | | | Leave blank; flag `OUT_OF_CATALOG` |
| Person city, state, country | CRM | Lead Database person location | | | `fill_blank_only` |

Why the Lead Database email goes through `validate_emails` and the Email Finder email does not: the Email Finder tool description says every email found is validated for deliverability. Every other source is validated before it is written, because the send gate needs a validation inside 90 days (ZeroBounce recommends verifying at least once per quarter).

## 3. Conflict matrix

When the CRM has a value and the lookup returns a different one:

| Field | CRM value state | Lookup result | Action | Flag |
|-|-|-|-|-|
| Email | Validated `valid` | Different email | Keep CRM. Put the new one in `enriched_email` | `EMAIL_CONFLICT` |
| Email | Validated `invalid` | `find_emails` found a different address | Replace; old goes to `prior_email` | `EMAIL_REPLACED` |
| Email | Validated `invalid` | Nothing found | Keep CRM value with `email_status = invalid`; never delete owner data | `EMAIL_INVALID` |
| Email | `catch_all` | Different `valid` address from `find_emails` | Stage; the catch-all may be the right inbox | `EMAIL_CONFLICT` |
| Phone | Fails E.164 rules | Lead Database phone passes | Replace; old to `prior_phone` | `PHONE_REPLACED` |
| Phone | Passes | Different phone | `append_new` if the CRM supports a second phone, else stage | `PHONE_ADDED` |
| Title | Updated inside the title freshness window | Different | Keep CRM | none |
| Title | Older than the window, or age unknown | Different, High match | Stage | `TITLE_CONFLICT` |
| Company | Any | Different company on a High match | Keep CRM; stage new company and title | `JOB_CHANGE` |
| Employees | Same size band as the lookup (section 6a) | Different number | Keep CRM; no flag | none |
| Employees | Different size band, CRM value older than the size freshness window or of unknown age | Different band | Stage the new value; size bands drive routing and territory | `SIZE_BAND_CHANGE` |
| Revenue | Any | Different | Keep CRM; report the count of differences only | none |
| Owner, stage, subscription status | Any | Anything | Never touch | none |

## 4. Match scoring for Lead Database results

The Lead Database has no first-name or last-name filter. You fetch people by `socialUrl`, `companyDomain` or `companyName` and match locally.

### Name comparison

1. Normalize both sides per the quality standard (case, particles, suffixes moved out, accents stripped for comparison only).
2. Last names must match exactly after normalization, or match on the first token of a hyphenated name (`Garcia-Lopez` vs `Garcia`).
3. First names match when equal, when one is a known nickname of the other, or when one is the initial of the other.

Common nickname pairs to accept: Robert/Bob/Rob, William/Bill/Will, Richard/Rick/Dick, Elizabeth/Liz/Beth, Katherine/Kate/Katie, Michael/Mike, James/Jim/Jamie, Jennifer/Jen, Christopher/Chris, Alexander/Alex, Alexandra/Alex, Daniel/Dan/Danny, Margaret/Maggie/Peggy, Anthony/Tony, Joseph/Joe, Thomas/Tom, Stephen/Steve, Steven/Steve, Patricia/Pat/Trish, Rebecca/Becky, Samuel/Sam, Samantha/Sam, Nicholas/Nick, Andrew/Andy/Drew, Edward/Ed/Ted, Theodore/Ted/Theo, Susan/Sue, Benjamin/Ben, Jonathan/Jon, Matthew/Matt, Gregory/Greg, Kimberly/Kim, Victoria/Vicky/Tori, Charles/Chuck/Charlie.

### Tiering

| Evidence | Tier |
|-|-|
| `socialUrl` returned exactly one person | High |
| CRM email equals a returned email | High |
| Exact first + last name, same domain, one candidate | High |
| Nickname or initial match, same domain, one candidate | Medium |
| Exact name, matched through `companyName` (no domain), one candidate | Medium |
| Two or more candidates pass the name test at the same domain | Low |
| Only the last name matches | Low |
| Nothing passes | None |

Break a Low tie only with a second field the CRM already has: a matching phone, a matching city, or a title in the same department. If the tie survives, flag `AMBIGUOUS_MATCH` and write nothing.

### What each tier may write

| Tier | `fill_blank_only` fields | `stage_for_review` fields |
|-|-|-|
| High | Written | Staged |
| Medium | Staged, never written | Staged |
| Low, None | Nothing | Nothing |

## 5. Job changes

A High match (`socialUrl` or email) that lists a different company than the CRM is the strongest job-change signal in the run.

1. Do not overwrite `company_name`, `email` or `job_title`.
2. Write `enriched_company`, `enriched_title`, and the new company domain to the review file.
3. Flag `JOB_CHANGE` and count these rows in the report.
4. Create the person at the new company: email from the Lead Database match after validation, else Email Finder with the new domain. Every one who validates goes into the main campaign as its own "new role" segment, so the copy can name the move. Then find a replacement contact at the old account with `query_lead_database` by `companyDomain` and the old title.
5. Keep the old record out of sends at the old address: the send gate excludes `JOB_CHANGE`.
6. If the CRM email is at the old company's domain, validate it. An `invalid` result confirms the job change.

## 6. Freshness windows

| Field | Refresh when older than | Source or input |
|-|-|-|
| `email_status` | 90 days, checked before any send | ZeroBounce recommends verifying a list at least once per quarter |
| `job_title`, `company_name` | The title freshness window in the rule sheet | User input; set it from the share of re-checked titles that changed on the last refresh |
| Company size, revenue | The size freshness window in the rule sheet ($0 lookups on Growth and Scale); write only on a size-band change | User input |
| `uses_<technology>` | Before each campaign that uses the technology as its trigger | Tech Stack Search is $4.99 per technology per pull, whatever the list size |
| Mobile | When reps mark a number wrong | Re-run `find_mobiles` for those people only |

### 6a. Size bands

Compare employee counts by band, never by averaging two sources: 1-10, 11-50, 51-200, 201-500, 501-1,000, 1,001-5,000, 5,001+. Two values in the same band are the same answer for segmentation. Different bands change which sequence, territory or price tier the account gets, so the new value is staged for the account owner.

## 7. Fields the enricher never writes

Record owner, lifecycle stage, lead status, deal stage and amount, notes and activity, original source, subscription status, unsubscribe, opt-out, DND flags, and any field the user lists as "rep-managed". If a lookup returns a value for one of these, drop it.

## Sources

- ZeroBounce, How often should I verify my email list: https://zerobounce.net/docs/frequently-asked-questions/account/how-often-should-I-verify-my-email-list
- UK Government Data Quality Hub, data quality dimensions: https://www.gov.uk/government/news/meet-the-data-quality-dimensions
- HubSpot, Import records for a single object (Don't overwrite checkbox): https://knowledge.hubspot.com/import-and-export/import-records-for-a-single-object
- Salesforce, Import cheat sheet (overwrite existing account values): https://resources.docs.salesforce.com/206/latest/en-us/sfdc/pdf/salesforce_import_cheatsheet.pdf
- ScraperCity tool catalog (Email Finder validation at lookup): references/scrapercity-catalog.md
- ScraperCity npm package 1.0.17, `AGENT_DOCS.txt` (Lead Database company field names): https://www.npmjs.com/package/scrapercity
- ScraperCity, Email Validator (company enrichment columns): https://scrapercity.com/email-validator
- US Bureau of Labor Statistics, Employee Tenure: https://www.bls.gov/news.release/tenure.nr0.htm
