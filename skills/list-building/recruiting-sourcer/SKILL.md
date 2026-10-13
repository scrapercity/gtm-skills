---
name: recruiting-sourcer
description: >-
  Sources candidates by role, seniority, location and target companies from the
  ScraperCity Lead Database (title, notTitle, seniority, department,
  companyName, companyDomain and location filters) or from an Apollo
  people-search URL (scrape_apollo, 500 to 50,000 leads at $0.0039 each,
  delivered over hours to days through a webhook), removes people at the
  hiring company and do-not-poach accounts, ranks the shortlist, then adds
  verified emails (find_emails, validate_emails) and mobiles for the top tier
  (find_mobiles), with outreach rules for candidates. Use when the user says
  "source senior React engineers in Austin", "find candidates at these
  companies", "build a recruiting shortlist", "get emails and mobiles for these
  candidates", or "map the VPs of Engineering at fintechs".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [recruiting, sourcing, talent, boolean-search, candidates, lead-database, apollo, email-finder, mobile-finder]
  related_skills: [icp-list-builder, decision-maker-finder, mobile-appender, email-list-cleaner, cold-email-copywriting, multi-channel-outreach, scrapercity-lead-database]
  frameworks:
    - "Glen Cathey (Boolean Black Belt) - sourcing as information retrieval and title expansion"
    - "EEOC - prohibited recruitment and job advertising practices; ADEA"
    - "NYC Local Law 144 - automated employment decision tools (2023)"
    - "FTC v. Spokeo (2012) - the FCRA line for candidate data"
    - "EU GDPR - Article 14 notice for data not obtained from the candidate"
    - "FTC - CAN-SPAM Act; CRTC - CASL"
    - "FCC - TCPA, 47 CFR 64.1200 for calls and texts to candidate mobiles"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, scrapercity-agent-patterns.md, outbound-compliance-primer.md]
---

# Recruiting Sourcer

## Overview

This skill produces a ranked candidate shortlist for one role: people whose current title and seniority fit, at the companies and in the locations the search asked for, with nobody from the hiring company or a do-not-poach account, each with a validated email where one exists and a mobile for the top tier. The report shows the search strings, the counts, the exclusions, the contact coverage, the cost and the outreach rules.

It prevents four sourcing mistakes:

1. One title string. "Senior React Engineer" misses "Frontend Engineer II", "UI Engineer" and "Software Engineer, Web". Titles expand into a family with exclusions, as sourcers have done in Boolean strings for years.
2. Sending the hiring manager's own team a recruiting email. The Lead Database has no "not this company" filter, so the skill removes the client's domains, subsidiaries and do-not-poach accounts after the pull and reports the count.
3. Paying for mobiles on 300 people when the recruiter will call 40. Mobile Finder ($0.25 per number found) runs on the A tier only.
4. Turning sourcing data into a background check. Running People Finder or Criminal Records on candidates moves the work into FCRA territory; this skill uses business contact tools only.

## When to Use

- "Source senior React engineers in Austin and give me their emails and mobiles."
- "Find VPs of Engineering at Series B fintechs on the East Coast."
- "Map the account executives at these 20 competitors."
- "Here's my Apollo search for data engineers; turn it into a contactable shortlist."
- "Build a pipeline of controllers for a client in Chicago."

Use a different skill when:

| The user wants | Use |
|-|-|
| Buyers at companies for a sales campaign | `icp-list-builder` or `decision-maker-finder` |
| Mobiles for an existing list of profiles | `mobile-appender` |
| Validation of an existing candidate email list | `email-list-cleaner` |
| The outreach copy | `cold-email-copywriting` |
| Email plus phone plus LinkedIn sequencing | `multi-channel-outreach` |
| A background check on a candidate | No skill here. Use an FCRA-compliant consumer reporting agency with the candidate's written authorization |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Role title as the client writes it, plus 2-3 example profiles of people they would hire | Title family and seniority | Ask |
| Seniority (individual contributor level or management level) | `seniority` and `notTitle` | Ask |
| Location: city, state, country, or remote with a time zone | Person location filters | Ask |
| Target companies (poach list), or company traits (industry, size, keywords) | `companyDomain`, `companyName`, `keywords`, size bands | Market-wide search with company traits |
| Hiring company domains, subsidiaries, and do-not-poach accounts (agency clients under non-solicit) | Exclusion | Ask; never skip |
| Shortlist size and how many the recruiter will call | Sets mobile scope | 300 shortlist, top 50 for mobiles |
| Plan level | Lead Database needs Growth or Scale; Starter uses `scrape_apollo` | `check_wallet` |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| Glen Cathey, Boolean Black Belt | Search is information retrieval: every concept (title, skill, level) has several ways people write it, and narrow exact phrases miss qualified people. The title family and `notTitle` sets in `references/title-expansion-library.md` apply that to Lead Database filters. |
| EEOC prohibited practices; ADEA | Job ads and recruiting methods may not show a preference or discourage applicants by race, sex, national origin, age 40 and up, disability or genetic information; word-of-mouth-only recruiting can be discriminatory when it reproduces a homogeneous workforce. Filters stay job-related: title, seniority, company, location. |
| NYC Local Law 144 (enforced from July 5, 2023) | An automated tool that substantially assists hiring decisions needs a bias audit within the past year and notice to candidates at least 10 days before use. A manual ranking rubric is outside it; automated scoring for NYC roles needs review. |
| FTC v. Spokeo (2012) | A people-data company that marketed profiles to HR and recruiters for screening was treated as a consumer reporting agency. Candidate evaluation with people-search data is an FCRA use. |
| GDPR Article 14 | When personal data comes from a source other than the person, the controller tells them, among other things, the source, at the latest at the first communication or within one month. |
| FTC CAN-SPAM; CRTC CASL | Whether a job email is "commercial" depends on its primary purpose; this skill applies CAN-SPAM mechanics (accurate sender, opt-out, postal address) to all candidate email, and treats Canadian candidate email as subject to CASL until counsel says otherwise. |
| TCPA, 47 CFR 64.1200 | Autodialed, prerecorded or AI-voice calls and texts to wireless numbers need consent whatever the content. Recruiters dial by hand and do not mass-text without consent. |

Details and routing: `references/framework-notes.md`. Nothing here is legal advice.

## Workflow

### 1. Write the role brief

Fill the Role Brief table: title as written, title family, seniority, location, target companies, company traits, must-haves that the data can filter (title and level) and must-haves it cannot (skills, years of experience, visa status; those are screened by a human). List the excluded employer domains.

### 2. Expand the title into a family

From `references/title-expansion-library.md`, build:

- `title`: comma-separated synonyms. The Lead Database matches each term partially, so "Frontend" also matches "Senior Frontend Engineer".
- `notTitle`: terms that partial matches drag in (Native for a web React role, Manager and Director for an individual contributor role, Recruiter, Intern, Instructor, Contract).
- `seniority` and `department` arrays. The tool documents `vp`, `director` and `c_suite` as seniority values and `sales` and `engineering` as departments; probe any other value with `limit: 1` and read the returned rows before relying on it.

### 3. Pick the source and count

| Situation | Source |
|-|-|
| Growth or Scale plan | `query_lead_database` with the filters, `limit: 1`, read `pagination.total` |
| User has an Apollo people-search URL | First pass it as `url` to `query_lead_database`; read `search_translation` for applied, approximated and unsupported filters |
| Starter plan, or the Lead Database count is too small and the Apollo URL's filters are what the client signed off | `scrape_apollo` with the URL, `count` 500 to 50,000 at $0.0039 per lead, webhook registered first |

Run two searches when there is a poach list: one with `companyDomain` (target companies, comma-separated) and one market-wide with location and company traits. Count both.

### 4. Pull

Database: page with `after: "0"` then `pagination.next_after`, `limit: 100`, until the planned rows. Apollo: register the webhook at app.scrapercity.com/dashboard/webhooks, start the run, save the `runId`, and stop the session; the webhook (or an hourly check at most) tells you when it reaches SUCCEEDED. Runs take hours to several days.

### 5. Exclude, dedupe, QA

1. Union the searches; dedupe on LinkedIn URL, then email, then first name + last name + company domain.
2. Remove the hiring company: every row whose `company_domain` is a client domain or subsidiary. Report the count.
3. Remove do-not-poach accounts (the agency's current clients, partners under non-solicit).
4. Remove titles that slipped through (read 20 random rows; 2 or more misfits means fix `notTitle` and re-pull).
5. Remove people the client already has in its ATS or rejected in the last 6 months if the client supplies the list.

### 6. Rank

| Points | Evidence |
|-|-|
| 40 | Title in the core family (not an adjacent title) |
| 20 | Seniority matches the brief |
| 20 | Current company on the target list |
| 10 | Person location in the target metro or time zone |
| 10 | Company size or stage matches the brief |

A tier: 80 and up. B: 60 to 79. C: under 60 (kept in the long list, not the shortlist). Do not add points for anything that proxies a protected trait (graduation year, name, photo, school as a stand-in for age).

### 7. Add contact data

1. Validate Lead Database emails with `validate_emails`.
2. For A and B candidates with no email, `find_emails` with `{first_name, last_name, domain}` ($0.05 per email found).
3. For A candidates only, `find_mobiles` with the LinkedIn URL, else the work email ($0.25 per number found). One input per person.
4. Normalize mobiles to E.164. Recruiters call by hand; no texts without consent.

### 8. Deliver and set outreach rules

Shortlist CSV, long list CSV, and the report from `templates/output-template.md` with the compliance table. Run `scripts/check-output.py`.

## ScraperCity Implementation

### Tools and prices (from `references/scrapercity-catalog.md`)

| Step | Tool | Price |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Search and count | `query_lead_database` | Included on Growth and Scale; 100,000 new leads a day |
| Apollo URL pull | `scrape_apollo` (`url`, `count` 500 to 50,000, `fileName`) | $0.0039 per lead |
| Email for candidates without one | `find_emails` (`contacts[]` of `{first_name, last_name, domain}`) | $0.05 per email found, free if not found |
| Email validation | `validate_emails` | $0.0072 per email |
| Mobile for A tier | `find_mobiles` (`inputs[]`) | $0.25 per number found, free if not found |

### Calls

```json
{"tool": "query_lead_database", "args": {
  "title": "React, Frontend, Front End, Front-End, UI Engineer, JavaScript Engineer, Web Engineer",
  "notTitle": "Native, Manager, Director, Head of, VP, Recruiter, Intern, Instructor, Designer, QA, Contract",
  "seniority": ["senior"],
  "city": "Austin", "state": ["Texas"], "country": ["United States"],
  "keywords": ["fintech", "saas"],
  "hasEmail": false, "limit": 1}}
{"tool": "query_lead_database", "args": {
  "companyDomain": "pinecrestpay.example,tallyworks.example,orbitfin.example",
  "title": "React, Frontend, Front End, Front-End, UI Engineer, JavaScript Engineer",
  "notTitle": "Native, Manager, Director, Head of, VP, Recruiter, Intern", "limit": 100, "after": "0"}}
{"tool": "query_lead_database", "args": {"url": "PASTE_APOLLO_PEOPLE_SEARCH_URL", "limit": 1}}
{"tool": "scrape_apollo", "args": {"url": "PASTE_APOLLO_PEOPLE_SEARCH_URL", "count": 1000, "fileName": "data-eng-chicago-20261013"}}
{"tool": "find_emails", "args": {"contacts": [{"first_name": "Maya", "last_name": "Chen", "domain": "tallyworks.example"}]}}
{"tool": "find_mobiles", "args": {"inputs": ["https://www.linkedin.com/in/maya-chen-frontend"]}}
```

`hasEmail: false` on the count keeps candidates without an email in the pool; Email Finder fills them later. Set it to `true` only when the budget rules out Email Finder. Replace each PASTE value with the URL copied from the browser.

Apollo through the CLI: `npx scrapercity apollo "<url>"` with a count; the CLI prints that Apollo takes up to 4 days and points to the webhook page. Apollo URLs must use Filters 1.0 format per the catalog.

### Worked cost estimate

Senior React engineers in Austin for a fintech client, Growth plan, shortlist of 320 (A 84, B 236).

| Line | Units | Unit price | Cost |
|-|-:|-:|-:|
| `query_lead_database` count and pulls | 814 rows (214 target-company, 600 market-wide) | Included | $0.00 |
| `validate_emails` on Lead Database emails for A and B | 251 emails | $0.0072 | $1.81 |
| `find_emails` for A and B without an email | 69 lookups, 41 found | $0.05 per found | $2.05 |
| `find_mobiles` for A tier | 84 inputs, 29 found | $0.25 per found | $7.25 |
| Total | | | $11.11 |

Ceiling before the run: $1.81 + 69 x $0.05 ($3.45) + 84 x $0.25 ($21.00) = $26.26. Over $5, so show it and wait. If the user were on Starter and used an Apollo URL instead, a 1,000-lead run would add 1,000 x $0.0039 = $3.90 and one to several days.

### Errors

| Code | Action |
|-|-|
| 402 | `check_wallet`; cut mobile scope first. |
| 403 on a database call | Plan lacks the Lead Database; offer the Apollo path. |
| 409 | Same Apollo URL submitted moments ago; reuse the earlier `runId`. |
| 503 on a database call | Narrow: fewer title terms, add a state, or split target companies into batches of 10 domains. |
| Apollo `FAILED` | Check the URL uses Filters 1.0; read the run logs. |

## Output Format

1. `shortlist-[role]-[date].csv`: A and B candidates with `first_name`, `last_name`, `title`, `seniority`, `company_name`, `company_domain`, `person_city`, `person_state`, `linkedin_url`, `tier`, `rank_score`, `email`, `email_status`, `mobile` (A tier, E.164), `source`, `pulled_at`.
2. `longlist-[role]-[date].csv`: C tier, no paid enrichment.
3. Report from `templates/output-template.md`: role brief, search strings, count check, sourcing funnel, contact coverage, cost, compliance check, shortlist sample, outreach plan, next steps.

## Quality Check

- [ ] The title family and `notTitle` set are written out, and a 20-row QA sample had fewer than 2 misfits.
- [ ] No candidate's company domain matches the hiring company, a subsidiary or a do-not-poach account, and the removed count is reported.
- [ ] Ranking uses only job-related evidence; nothing proxies age, sex, race, national origin or disability.
- [ ] Apollo runs, if any, had a webhook registered and a `count` between 500 and 50,000.
- [ ] Every email in the shortlist was validated or came from Email Finder; catch-all emails are marked.
- [ ] Mobiles exist only for A-tier rows, are E.164, and the outreach plan has no texts without consent.
- [ ] The compliance table names a law or rule on every row, including Article 14 for EU and UK candidates.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| `title: "Senior React Engineer"` | Partial match on one phrasing misses most of the market | Title family plus `seniority` |
| No `notTitle` | "React" also matches React Native mobile engineers, engineering managers and recruiters hiring React engineers | Exclusion set per family |
| Forgetting the client's own staff | The client's engineers get a recruiting email from the client's agency | Remove client domains and subsidiaries after every pull |
| Polling an Apollo run every few minutes | Runs take hours to days | Webhook; hourly at most |
| Mobiles for the long list | $0.25 per hit on people nobody will call | A tier only |
| Texting candidates from a platform | TCPA consent applies to automated texts whatever the content | Manual calls and email |
| Ranking by graduation year or "years since degree" | Age proxy; ADEA and EEOC risk | Rank on title, level, company, location |
| Running People Finder or Criminal Records on finalists | Background screening is an FCRA use | Use a consumer reporting agency with the candidate's authorization |
| EU candidates emailed with no source notice | GDPR Article 14 | Say where you found them and how to opt out in the first email |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/title-expansion-library.md` | Building `title`, `notTitle`, `seniority` and `department` for a role family. |
| `references/sourcing-runbook.md` | Choosing Lead Database or Apollo, target-company batching, exclusions, ranking, contact enrichment, webhooks. |
| `references/candidate-outreach-compliance.md` | Writing the compliance table and outreach rules: email, calls, texts, EEOC, LL144, GDPR, FCRA. |
| `references/outbound-compliance-primer.md` | Shared CAN-SPAM, CASL, PECR and TCPA rules. |
| `references/list-quality-standard.md` | Normalization, dedupe keys, validation buckets (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database allowances (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet, webhooks, polling (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished shortlist for senior React engineers in Austin. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `icp-list-builder` and `decision-maker-finder` for the same filters aimed at buyers.
- `mobile-appender` for the TCPA gate on any mobile list.
- `email-list-cleaner` to re-validate a candidate list before a new search.
- `cold-email-copywriting` for candidate outreach copy.
- `multi-channel-outreach` to combine email, calls and LinkedIn.
- `scrapercity-lead-database` for every Lead Database filter in depth.
