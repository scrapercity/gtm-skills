# Candidate Messages, Reply Outcomes and Handoff

What happens after the shortlist exists: which companies to source from first, the first messages, how replies feed the next pull, and how the file lands in the ATS.

## 1. Choosing target companies

The poach list decides who answers. Build it from these sources, in this order, and tag each company with the reason so replies can be read by reason later:

| Reason tag | Companies | Why candidates there answer |
|-|-|-|
| `ahead` | One or two funding stages or size bands ahead of the client, same product category | They have done the job at the next scale; the client's role is a step up in scope |
| `competitor` | Direct competitors | Same customers, same vocabulary; shortest ramp |
| `alumni` | The hiring manager's and the team's past employers | Warm path: the first message names someone they worked with |
| `adjacent` | Companies selling to the same buyer with a different product | Same buyer knowledge, fresh product |
| `stalled` | Companies with a hiring freeze, a reorg or flat headcount the user knows about | People are already looking; confirm with the user rather than guessing |

The reply-rate reading in section 4 shows which reasons answer for this client; the "why" column is the hypothesis it tests. Batch the domains in small groups with the same `title`, `notTitle` and `seniority` (see `sourcing-runbook.md` section 2) and keep the reason tag in a `target_reason` column.

## 2. What the first message carries

LinkedIn's analysis of tens of millions of recruiter InMails (May 2021 to April 2022) gives the closest public data on candidate replies:

| Finding | Number | Rule it sets |
|-|-|-|
| Messages under 400 characters | Response rate 22% above average; over 1,200 characters, 11% below | First message under 400 characters |
| Sent one by one versus in bulk | About 15% higher response one by one | Personalize the first line per candidate; no mail-merge-only openers |
| Day of week | Friday 4% below average, Saturday 8% below; Sunday to Thursday within about 1% | Send Sunday to Thursday |
| Reply timing | 65% of responses within 24 hours, 90% within a week | Follow up after day 7 |

LinkedIn also reported that 91% of US respondents in its survey said a salary range in a job post affects whether they apply. Applied rule: the first message states the pay band.

Every first message has five parts, in this order: the candidate's name and one specific line about their work (their company's product, a talk, a repo, a launch); the role in one line (level, team, what they would own); the pay band and work setup; one selling point from the brief; a 15-minute ask. No job description attached and no link wall.

## 3. Message drafts

Character counts below exclude the signature. Replace the bracketed parts with real details from the candidate's row; nothing in brackets ships.

### Email 1 (day 1, under 400 characters)

> Hi [first name], your work on [product or team at their company] is why I'm writing. A payments software company in Austin is hiring senior frontend engineers to own its merchant dashboard: React and TypeScript, hybrid two days a week, $165k to $195k base plus equity. The team ships weekly with no on-call. Open to a 15-minute call this week?

### LinkedIn connection note (day set by the recruiter)

> Hi [first name], I emailed about a senior frontend role at an Austin payments company ($165k to $195k, hybrid). Happy to send details here if easier.

### Email 2 (day 8, under 400 characters)

> [first name], one more detail: the team is six engineers, interviews are three steps over one week, and the role reports to the VP of Engineering. Worth 15 minutes?

### Email 3 (day set by the recruiter, closes the loop and asks for a referral)

> [first name], I'll stop here. If someone you've worked with would want this role ($165k to $195k, hybrid Austin), I'd be glad to hear their name. If timing changes for you, reply anytime.

For `alumni` candidates, the first line names the shared employer or the person who suggested them, with that person's permission.

## 4. Reply outcomes and what they change

Tag every reply with one outcome:

| Outcome | Meaning | Action |
|-|-|-|
| `interested` | Wants the call | Book the call; move to the ATS as an active candidate |
| `not_now` | Interested later; gives a time | Set a follow-up date; keep in the prospect pool |
| `not_looking` | Declines | Suppress for this role; the agency decides when a different role may reach them |
| `wrong_fit` | Says the level, stack or location is off | Note which; this is a filter problem |
| `referred` | Names someone else | Source the referred person; their first message names the referrer |
| `opt_out` | Asks not to be contacted | Agency suppression list, every channel, same day |

Read the outcomes after the first wave of each search:

| Signal | Fix for the next pull |
|-|-|
| One title term draws most of the `wrong_fit` replies | Move that term to `notTitle` or tighten `seniority` |
| One `target_reason` replies well below the others | Shift the next pull toward the reasons that reply |
| `referred` names cluster on one title | Add that title to the family |
| Low reply rate with few `wrong_fit` replies | The list fits and the message or the offer does not: rewrite the first message and take the reply data to the client as a pay band question before pulling more people |

## 5. ATS handoff

Greenhouse's bulk prospect import takes a spreadsheet from its template: first and last name are required, sources and "who gets credit" are mapped during the import, prospect pool and stage names must match the CRM settings exactly, and Greenhouse recommends no more than 8,000 prospects per import. A prospect imported with Referral or an agency as the source is not auto-merged with an existing record; both get a Duplicate tag for review.

| ATS field | Column |
|-|-|
| First name, last name | `first_name`, `last_name` |
| Email | `email` (valid only; catch-all in a separate pool) |
| Phone | `mobile` (A tier) |
| Current company, title | `company_name`, `title` |
| LinkedIn or website | `linkedin_url` |
| Source | The search name, for example `ScraperCity, target companies, ahead` or `ScraperCity, market-wide`, so replies and hires can be counted per search |
| Prospect pool and stage | The role's pool; stage `sourced` |
| Tags or custom field | `tier`, `target_reason` |

Other ATS products take CSV imports with similar fields; map the same columns and keep the source per search.

## 6. Refresh before outreach

People change jobs. The US Bureau of Labor Statistics reported median employee tenure of 4.1 years in January 2026. A shortlist that waits loses people to moves, so before a shortlist goes out after a wait:

| Step | Action |
|-|-|
| Emails | Re-validate any email validated before the wait |
| Title and employer | Re-check with a Lead Database lookup by LinkedIn URL; drop anyone who moved to an excluded employer |
| Next time | Record the share who had moved, and set the next shortlist's allowed wait from it |

## Sources

- LinkedIn Talent Blog, InMail response rate data, May 2021 to April 2022 (checked 2026-10-13): https://business.linkedin.com/talent-solutions/blog/trends-and-research/2021/these-inmails-get-best-response-rates
- LinkedIn, Why you should include salary ranges in job posts: https://www.linkedin.com/business/talent/blog/talent-acquisition/why-you-should-include-salary-ranges-in-job-posts
- Search Engine Journal, summary of the LinkedIn salary-range survey (Feb 2023): https://www.searchenginejournal.com/linkedin-data-91-of-applicants-want-salary-range-in-job-posting/479267/
- Greenhouse Support, Bulk import prospects from spreadsheet (checked 2026-10-13): https://support.greenhouse.io/hc/en-us/articles/203871039-Bulk-import-prospects-from-spreadsheet
- US Bureau of Labor Statistics, Employee Tenure (January 2026): https://www.bls.gov/news.release/tenure.nr0.htm
- Glen Cathey, Boolean Black Belt (sourcing from where qualified people describe their work): https://booleanblackbelt.com/
