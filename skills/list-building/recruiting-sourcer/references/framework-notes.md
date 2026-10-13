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
| Rank candidates | `sourcing-runbook.md` section 7 |
| Write outreach rules and the compliance table | `candidate-outreach-compliance.md` |
| Validate emails, normalize phones | `references/list-quality-standard.md` (shared) |
| Quote a price | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### Glen Cathey, Boolean Black Belt

Cathey's long-running sourcing blog treats search as information retrieval: the sourcer's job is to anticipate the many ways qualified people describe themselves, and narrow exact-phrase keywords cut out good candidates. Applied here as the title-family method: a core noun, specialty words, spelling variants, and an exclusion set for drag-ins, with level handled by the `seniority` filter where possible.

### EEOC and the ADEA

The EEOC states that job advertisements and recruitment practices may not show a preference for or discourage people based on race, color, religion, sex, national origin, age (40 or older), disability or genetic information, and gives "recent college graduates" as an ad example that can deter older applicants. It also notes that word-of-mouth recruiting can be discriminatory when it produces a workforce of mostly one group. Applied rules: filters and ranking use job-related evidence only; target-company searches are paired with market-wide searches.

### New York City Local Law 144

Enforced from July 5, 2023, under rules adopted April 6, 2023. An automated employment decision tool (a machine learning, statistical or AI process producing a score or ranking that substantially assists or replaces discretionary hiring decisions) needs a bias audit within one year before use, a public summary, and at least 10 days' notice to candidates. Fines run from $500 to $1,500 per violation. Applied rule: the ranking rubric here is a manual sort a recruiter reviews; automated screening for NYC roles gets a legal review first.

### FTC v. Spokeo and the FCRA

In 2012 the FTC settled with Spokeo for $800,000, saying it acted as a consumer reporting agency by marketing people profiles to human resources, recruiters and background screeners without FCRA procedures. Applied rule: candidate sourcing uses business contact tools; people-search and criminal record tools stay out of candidate workflows, and any background check runs through a consumer reporting agency with the candidate's authorization.

### GDPR Article 14

When data comes from a third party, the controller gives the person its identity, purposes, legal basis, legitimate interests, data categories, source, retention, rights, and the right to complain, at the latest within one month or at first contact. Applied rule: the first email to an EU or UK candidate carries a short source and privacy line.

### CAN-SPAM and CASL

The FTC guide ties CAN-SPAM coverage to a message's primary purpose. PeopleScout's compliance note says these laws also apply to talent acquisition teams that email candidates, without settling which candidate emails are commercial. CRTC's CASL FAQ covers implied consent for conspicuously published addresses. Applied rule: CAN-SPAM mechanics on every candidate email; CASL treatment for Canadian candidates unless counsel decides otherwise.

### TCPA and 47 CFR 64.1200

Autodialed, prerecorded or artificial-voice calls and texts to wireless numbers need consent regardless of content; AI voices count as artificial (FCC, February 2024); consent can be revoked by any reasonable means (rules effective April 11, 2025). Applied rule: recruiters dial by hand; no mass texting without consent.

### ScraperCity catalog and platform facts

The catalog defines `scrape_apollo` (Apollo.io people-search URLs in Filters 1.0 format, `count` 500 to 50,000, $0.0039 per lead), `find_emails`, `find_mobiles` and `validate_emails` with their prices. The platform facts file and the MCP tool description define the Lead Database filters used here (`title`, `notTitle`, `seniority`, `department`, `companyName`, `companyDomain`, person and company location, size and keyword filters) and the `url` parameter with `search_translation`. Apollo runs take hours to several days, so they run behind a webhook.

## What this skill does not do

- Screen candidates for skills, years of experience, visa status or compensation; the data does not hold those reliably and a recruiter screens them.
- Find personal emails or home addresses.
- Make or support hiring decisions with automated scores.

## Sources

- Glen Cathey, Boolean Black Belt: https://booleanblackbelt.com/
- EEOC, Prohibited employment policies and practices: https://www.eeoc.gov/prohibited-employment-policiespractices
- NYC Local Law 144 final rules (summary): https://perkinscoie.com/en/news-insights/nyc-adopts-final-rules-for-law-governing-automated-employment-decision-tools.html
- FTC Spokeo settlement (summary): https://www.hunton.com/privacy-and-cybersecurity-law-blog/ftc-fines-data-broker-800000-alleged-fcra-violations
- GDPR Article 14: https://gdpr-info.eu/art-14-gdpr/
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- PeopleScout, Compliance corner: https://www.peoplescout.com/insights/compliance-corner-can-spam-casl/
- CRTC, CASL FAQ: https://crtc.gc.ca/eng/com500/faq500.htm
- 47 U.S.C. 227: https://www.law.cornell.edu/uscode/text/47/227
- ScraperCity tool catalog: references/scrapercity-catalog.md
