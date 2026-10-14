---
name: recruiting-sourcer
description: >-
  Sources candidates by role, seniority, location and target companies from the
  ScraperCity Lead Database (title, notTitle, seniority, department,
  companyName, companyDomain and location filters) or from an Apollo
  people-search URL (scrape_apollo, 500 to 50,000 leads at $0.0039 each,
  delivered over hours to days through a webhook), removes people at the
  hiring company and do-not-poach accounts, tiers the shortlist, then adds
  verified emails (find_emails, validate_emails) and mobiles for the top tier
  (find_mobiles), with first messages for candidates. Use when the user says
  "source senior React engineers in Austin", "find candidates at these
  companies", "build a recruiting shortlist", "get emails and mobiles for these
  candidates", or "map the VPs of Engineering at fintechs".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags:
    - recruiting
    - sourcing
    - talent
    - boolean-search
    - candidates
    - lead-database
    - apollo
    - email-finder
    - mobile-finder
  related_skills:
    - icp-list-builder
    - decision-maker-finder
    - mobile-appender
    - email-list-cleaner
    - cold-email-copywriting
    - multi-channel-outreach
    - scrapercity-lead-database
  frameworks:
    - "Glen Cathey (Boolean Black Belt) - sourcing as information retrieval and title expansion"
    - "LinkedIn Talent Solutions - InMail response data by length, send mode, day and reply timing (2021-2022)"
    - "Greenhouse - bulk prospect import with source mapping"
    - "US Bureau of Labor Statistics - Employee Tenure (January 2026)"
    - "GitHub Docs - user search qualifiers and search API limits"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
    - scrapercity-agent-patterns.md
---

# Recruiting Sourcer

## Overview

This skill produces a tiered candidate shortlist for one role: people whose current title and seniority fit, at the companies and in the locations the search asked for, with people at the hiring company and do-not-poach accounts removed, each with a validated email where one exists and a mobile for the top tier. The report shows the search strings, the counts, the exclusions, the contact coverage, the cost and the outreach plan.

It prevents four sourcing mistakes:

1. One title string. "Senior React Engineer" misses "Frontend Engineer II", "UI Engineer" and "Software Engineer, Web". Titles expand into a family with exclusions, as sourcers have done in Boolean strings for years.
2. Sending the hiring manager's own team a recruiting email. The Lead Database has no "not this company" filter, so the skill removes the client's domains, subsidiaries and do-not-poach accounts after the pull and reports the count.
3. Paying for mobiles on 300 people when the recruiter will call 40. Mobile Finder ($0.25 per number found) runs on the A tier only.
4. One source tag for every candidate. The agency cannot tell which search produced the replies and hires, so the next search repeats the weak one. Each search gets its own source in the ATS import.

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

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Role title as the client writes it, plus 2-3 example profiles of people they would hire | Title family and seniority | Ask |
| Seniority (individual contributor level or management level) | `seniority` and `notTitle` | Ask |
| Location: city, state, country, or remote with a time zone | Person location filters | Ask |
| Target companies (poach list), or company traits (industry, size, keywords) | `companyDomain`, `companyName`, `keywords`, size bands | Market-wide search with company traits |
| Hiring company domains, subsidiaries, and do-not-poach accounts (the agency's current clients) | Exclusion | Ask; never skip |
| Shortlist size and how many the recruiter will call | Sets mobile scope | Ask |
| ATS export of people already in process or recently rejected, with the client's look-back window | Exclusion | Ask |
| Pay band and two selling points (team, scope, schedule, equity) | First message content | Ask; a message without a pay band waits until the client gives one |
| The hiring team's past employers | `alumni` target companies with a warm first line | Ask |
| Plan level | Lead Database needs Growth or Scale; Starter uses `scrape_apollo` | `check_wallet` |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| Glen Cathey, Boolean Black Belt | Search is information retrieval: every concept (title, skill, level) has several ways people write it, and narrow exact phrases miss qualified people. The title family and `notTitle` sets in `references/title-expansion-library.md` apply that to Lead Database filters. |
| LinkedIn InMail analysis (May 2021 to April 2022) | Messages under 400 characters drew 22% more responses than average; one-by-one sends about 15% more than bulk; Friday and Saturday ran 4% and 8% below; 65% of replies came within 24 hours and 90% within a week. Sets the first-message length, send days and the follow-up after day 7. |
| LinkedIn salary-range survey | 91% of US respondents said a salary range in a job post affects whether they apply. The first message states the pay band. |
| Greenhouse bulk prospect import | First and last name required, source mapped at import, no more than 8,000 prospects per import recommended. Sets the ATS handoff. |
| US Bureau of Labor Statistics, Employee Tenure | Median tenure with the current employer was 4.1 years in January 2026, so a share of any shortlist moves every month it waits. Sets the re-check before outreach. |
| GitHub Docs, user search | `location:`, `language:` and `repos:` qualifiers; up to 1,000 results per search. A free second source for thin engineering markets. |

Details and routing: `references/framework-notes.md`.

## Workflow

### 1. Write the role brief

Fill the Role Brief table: title as written, title family, seniority, location, pay band, two selling points, target companies, company traits, must-haves that the data can filter (title and level) and must-haves it cannot (skills, years of experience, visa status, and for sales roles quota attainment and deal size; those are screened by a human). List the excluded employer domains.

Build the target-company list by reason and tag each company: `ahead` (one or two stages or size bands ahead of the client), `competitor`, `alumni` (the hiring team's past employers), `adjacent` (same buyer, different product). Reasons and why each replies: `references/candidate-messages-and-handoff.md` section 1.

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

Run two searches when there is a poach list: one with `companyDomain` (target companies, comma-separated) and one market-wide with location and company traits. Count both. For engineering roles where the market-wide count is thin, add a GitHub user search (`location:`, `language:`, `repos:`) as a free second source and match profiles back by name and company (`references/sourcing-runbook.md` section 9).

### 4. Pull

Database: page with `after: "0"` then `pagination.next_after`, `limit: 100`, until the planned rows. Apollo: register the webhook at app.scrapercity.com/dashboard/webhooks, start the run, save the `runId`, and stop the session; the webhook (or an hourly check at most) tells you when it reaches SUCCEEDED. Runs take hours to several days.

### 5. Exclude, dedupe, QA

1. Union the searches; dedupe on LinkedIn URL, then email, then first name + last name + company domain.
2. Remove the hiring company: every row whose `company_domain` is a client domain or subsidiary. Report the count.
3. Remove do-not-poach accounts (the agency's current clients and partners).
4. Remove titles that slipped through: read a random sample (the size is the recruiter's call; the example reads 20) and record title fit, level fit and location as "N of M", plus a few LinkedIn URLs opened to confirm the person. When misfits share a pattern (one drag-in title, one wrong level), fix `notTitle` or the company filters and re-pull rather than hand-deleting.
5. Remove people the client already has in its ATS or rejected within the client's look-back window, if the client supplies the list.

### 6. Tier

Tier each candidate by the evidence the row holds, and write it to `fit`:

| Fit | Meaning | Tier |
|-|-|-|
| `core+level+target` | Title in the core family, seniority matches the brief, current company on the target list | A |
| `core+level` | Core title and seniority, found market-wide | B |
| `adjacent+level+target` | Adjacent title (for example Full Stack for a frontend role) at a target company, seniority matches | B |
| Anything else | Adjacent title market-wide, or level off | C (long list, no paid enrichment) |

Location, company size and keywords are filters, so every pulled row already meets them.

### 7. Add contact data

1. Validate Lead Database emails with `validate_emails`.
2. For A and B candidates with no email, `find_emails` with `{first_name, last_name, domain}` ($0.05 per email found).
3. For A candidates only, `find_mobiles` with the LinkedIn URL, else the work email ($0.25 per number found). One input per person.
4. Normalize mobiles to E.164.

### 8. Draft the messages, hand off, read the replies

1. Write the first email (under 400 characters: one specific line about the candidate's work, the role in one line, the pay band and setup, one selling point, a 15-minute ask), a follow-up after day 7, a LinkedIn connection note, and a closing email that asks for a referral. Send Sunday to Thursday. The LinkedIn note and the close go out on days the recruiter sets. Templates and the data behind each rule: `references/candidate-messages-and-handoff.md` sections 2 and 3.
2. Import the shortlist into the ATS as prospects with the source set per search (target companies by reason, market-wide), so replies and hires count per search. Greenhouse mapping is in section 5.
3. Tag replies `interested`, `not_now`, `not_looking`, `wrong_fit`, `referred`, `opt_out`. An `opt_out` goes on the agency suppression list the same day, every channel. After the first wave, compare `wrong_fit` share by title term and reply rate by target reason: the title term that draws the most `wrong_fit` moves to `notTitle`, and the next pull shifts toward the reasons that reply (section 4).
4. Before sending a shortlist that has waited, re-check title and employer; set how long it may wait from the share of candidates who had moved at your last re-check. Write the shortlist CSV, the long list CSV and the report from `templates/output-template.md`; run `scripts/check-output.py`.

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

Ceiling before the run: $1.81 + 69 x $0.05 ($3.45) + 84 x $0.25 ($21.00) = $26.26. Show it and wait for a go-ahead. If the user were on Starter and used an Apollo URL instead, a 1,000-lead run would add 1,000 x $0.0039 = $3.90 and one to several days.

### Errors

| Code | Action |
|-|-|
| 402 | `check_wallet`; cut mobile scope first. |
| 403 on a database call | Plan lacks the Lead Database; offer the Apollo path. |
| 409 | Same Apollo URL submitted moments ago; reuse the earlier `runId`. |
| 503 on a database call | Narrow: fewer title terms, add a state, or split target companies into smaller domain batches. |
| Apollo `FAILED` | Check the URL uses Filters 1.0; read the run logs. |

## Output Format

1. `shortlist-[role]-[date].csv`: A and B candidates with `first_name`, `last_name`, `title`, `seniority`, `company_name`, `company_domain`, `person_city`, `person_state`, `linkedin_url`, `tier`, `fit`, `email`, `email_status`, `mobile` (A tier, E.164), `source`, `pulled_at`.
2. `longlist-[role]-[date].csv`: C tier, no paid enrichment.
3. Report from `templates/output-template.md`: role brief with pay band and selling points, search strings, count check with the QA line, sourcing funnel, contact coverage, cost, shortlist sample, outreach plan, message drafts, next steps with the ATS import and reply tags.

What the reader receives is the deliverable only: product names (Lead Database, Apollo Scraper, Email Finder, Email Validator, Mobile Finder), never tool ids, internal file paths or reference section numbers; filter parameter names appear only in the Search Strings table; another skill is named only in a handoff line; no tables of checks that were not run (one "Not checked:" line instead); no repeated identical rows.

## Quality Check

- [ ] The title family and `notTitle` set are written out, and the QA line reports title fit, level fit and location as "N of M".
- [ ] No candidate's company domain matches the hiring company, a subsidiary or a do-not-poach account, and the removed count is reported.
- [ ] Every shortlisted row's tier matches its `fit` evidence.
- [ ] Apollo runs, if any, had a webhook registered and a `count` between 500 and 50,000.
- [ ] Every email in the shortlist was validated or came from Email Finder; catch-all emails are marked.
- [ ] Mobiles exist only for A-tier rows and are E.164.
- [ ] The Role Brief states a pay band in dollars, and the first message carries it.
- [ ] Message Drafts holds at least the first email and the closing email, each under 400 characters, with no bracketed placeholders left for the candidate to see.
- [ ] Next Steps names the ATS import with the source per search and the six reply tags.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| `title: "Senior React Engineer"` | Partial match on one phrasing misses most of the market | Title family plus `seniority` |
| No `notTitle` | "React" also matches React Native mobile engineers, engineering managers and recruiters hiring React engineers | Exclusion set per family |
| Forgetting the client's own staff | The client's engineers get a recruiting email from the client's agency | Remove client domains and subsidiaries after every pull |
| Polling an Apollo run every few minutes | Runs take hours to days | Webhook; hourly at most |
| Mobiles for the long list | $0.25 per hit on people the recruiter will not call | A tier only |
| Guessing `firstname@company.com` when Email Finder returns nothing | Pattern guesses bounce, and bounces hurt the recruiter's domain for every other send | Mark "no usable email"; reach the person by LinkedIn or a call |
| A 1,200-character first message with the job description pasted in | LinkedIn's InMail data puts messages over 1,200 characters 11% below average and under 400 characters 22% above | Under 400 characters; the description goes out after the reply |
| No pay band until the call | Candidates weigh the band before they reply; the survey puts 91% as saying a range affects whether they apply | Band in the first message |
| One source tag for every candidate | The agency cannot tell which search produced the hires | Source per search in the ATS import |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/title-expansion-library.md` | Building `title`, `notTitle`, `seniority` and `department` for a role family. |
| `references/sourcing-runbook.md` | Choosing Lead Database or Apollo, target-company batching, exclusions, tiering, contact enrichment, webhooks, GitHub search. |
| `references/candidate-messages-and-handoff.md` | Target companies by reason, first-message rules with the LinkedIn data, four message drafts, reply tags and what they change, Greenhouse import mapping, refresh before outreach. |
| `references/list-quality-standard.md` | Normalization, dedupe keys, validation buckets (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database allowances (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet, webhooks, polling (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished shortlist for senior React engineers in Austin. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `icp-list-builder` and `decision-maker-finder` for the same filters aimed at buyers.
- `mobile-appender` for mobiles on an existing list of profiles.
- `email-list-cleaner` to re-validate a candidate list before a new search.
- `cold-email-copywriting` for candidate outreach copy.
- `multi-channel-outreach` to combine email, calls and LinkedIn.
- `scrapercity-lead-database` for every Lead Database filter in depth.
