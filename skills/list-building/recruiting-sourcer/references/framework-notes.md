# Framework Notes: Recruiting Sourcer

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Turn a job title into `title`, `notTitle`, `seniority`, `department` | `title-expansion-library.md` |
| Decide between the Lead Database and an Apollo run | `sourcing-runbook.md` section 1 |
| Batch target companies, run market-wide searches | `sourcing-runbook.md` sections 2 and 3 |
| Start and track an Apollo run with a webhook | `sourcing-runbook.md` section 4 |
| Remove the hiring company and do-not-poach accounts | `sourcing-runbook.md` section 5 |
| Tier candidates | `sourcing-runbook.md` section 7 |
| Add GitHub user search for engineers | `sourcing-runbook.md` section 9 |
| Pick target companies by reason, draft the four messages, tag replies, import to the ATS | `candidate-messages-and-handoff.md` |
| Validate emails, normalize phones | `references/list-quality-standard.md` (shared) |
| Quote a price | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### Glen Cathey, Boolean Black Belt

Cathey's long-running sourcing blog treats search as information retrieval: the sourcer's job is to anticipate the many ways qualified people describe themselves, and narrow exact-phrase keywords cut out good candidates. Applied here as the title-family method: a core noun, specialty words, spelling variants, and an exclusion set for drag-ins, with level handled by the `seniority` filter where possible.

### LinkedIn InMail and salary-range data

LinkedIn's Talent Blog analyzed tens of millions of recruiter InMails sent from May 2021 to April 2022: messages under 400 characters drew responses 22% above average, messages over 1,200 characters 11% below; one-by-one sends ran about 15% above bulk sends; Friday and Saturday ran 4% and 8% below average; 65% of responses arrived within 24 hours and 90% within a week. A separate LinkedIn survey reported that 91% of US respondents said a salary range in a job post affects whether they apply. Applied rules: first message under 400 characters with the pay band, sent Sunday to Thursday, follow-up after day 7. The LinkedIn note and the closing email go out on days the recruiter sets.

### Greenhouse bulk prospect import

Greenhouse's help center documents the bulk prospect import: a template spreadsheet with first and last name required, source and credit mapped during import, pool and stage names matched to the CRM settings, and a recommended maximum of 8,000 prospects per import. Applied rule: import the shortlist with a source per search so replies and hires can be counted by search.

### US Bureau of Labor Statistics, Employee Tenure

The BLS reported a median of 4.1 years with the current employer for wage and salary workers in January 2026. Applied rule: a shortlist that waits loses people to job moves, so title and employer are re-checked before outreach; the recruiter sets the wait from the share who had moved at the last re-check.

### GitHub Docs, user search

GitHub documents user-search qualifiers (`location:`, `language:`, `repos:`, `followers:`, `created:`, `type:user`), and its REST search returns up to 100 users per page and 1,000 results per search, with authenticated search limited to 30 requests a minute. Applied rule: a free second source for engineering roles when the market-wide count is thin.

### ScraperCity catalog and platform facts

The catalog defines `scrape_apollo` (Apollo.io people-search URLs in Filters 1.0 format, `count` 500 to 50,000, $0.0039 per lead), `find_emails`, `find_mobiles` and `validate_emails` with their prices. The platform facts file and the MCP tool description define the Lead Database filters used here (`title`, `notTitle`, `seniority`, `department`, `companyName`, `companyDomain`, person and company location, size and keyword filters) and the `url` parameter with `search_translation`. Apollo runs usually take 15 to 30 minutes, so they run behind a webhook.

## Inputs this skill asks for instead of assuming

| Setting | Where it comes from |
|-|-|
| Shortlist size and how many candidates get mobiles | How many the recruiter will call |
| QA sample size | The recruiter's choice; the example reads 20 rows |
| ATS look-back window for rejected candidates | The client |
| When a title term moves to `notTitle`, and how the next pull splits by target reason | `wrong_fit` share by title term and reply rate by reason after the first wave |
| How long a shortlist may wait before a re-check | Share of candidates who had moved at the last re-check |
| LinkedIn note and closing email days | The recruiter |

## What this skill does not do

- Screen candidates for skills, years of experience, visa status or compensation; the data does not hold those reliably and a recruiter screens them.
- Find personal emails or home addresses.

## Sources

- Glen Cathey, Boolean Black Belt: https://booleanblackbelt.com/
- LinkedIn Talent Blog, InMail response data: https://business.linkedin.com/talent-solutions/blog/trends-and-research/2021/these-inmails-get-best-response-rates
- LinkedIn, salary ranges in job posts: https://www.linkedin.com/business/talent/blog/talent-acquisition/why-you-should-include-salary-ranges-in-job-posts
- Greenhouse Support, Bulk import prospects: https://support.greenhouse.io/hc/en-us/articles/203871039-Bulk-import-prospects-from-spreadsheet
- US Bureau of Labor Statistics, Employee Tenure (January 2026, checked 2026-10-13): https://www.bls.gov/news.release/tenure.nr0.htm
- GitHub Docs, Searching users: https://docs.github.com/en/search-github/searching-on-github/searching-users
- GitHub Docs, REST API search endpoints: https://docs.github.com/en/rest/search/search
- ScraperCity tool catalog: references/scrapercity-catalog.md
