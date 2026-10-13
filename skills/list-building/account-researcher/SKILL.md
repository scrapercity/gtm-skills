---
name: account-researcher
description: >-
  Builds a one-page brief on a target company and its key people before
  outreach or a call: firmographics and team counts from the Lead Database,
  the 3-4 people who own the decision with verified emails, the technologies
  that change the pitch (checked with Tech Stack Search only when they do),
  dated trigger events, and talking points that each cite a source. Use when
  the user says "research this account", "brief me on acme.com before my
  call", "what do we know about X", "account plan", or names 1-10 priority
  companies for deep work before a sequence.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [account-research, account-based, tech-stack, trigger-events, brief, decision-makers]
  related_skills: [decision-maker-finder, icp-list-builder, ecommerce-by-techstack, signal-triggered-outbound, cold-email-copywriting, multi-channel-outreach, crm-enricher]
  frameworks:
    - "Gartner - B2B buying groups of 6 to 10 decision makers"
    - "MEDDIC (Dick Dunkel, Jack Napoli, John McMahon, PTC 1996) - economic buyer and champion"
    - "Craig Elias - trigger events and the window of dissatisfaction"
    - "US SEC - EDGAR filings (10-K, 8-K) as primary company evidence"
    - "Alex Berman - segment, account and person levels of personalization"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md, list-quality-standard.md, alex-berman-cold-email.md]
---

# Account Researcher

## Overview

This skill produces a brief of one to two pages per account: a snapshot (size, revenue, HQ, keywords, team counts), dated trigger events, the technologies that decide which pitch to use, the 3-4 people who own the decision with verified emails, a hypothesis with talking points that each cite a source, a contact plan, and the cost of the research.

The mistake it prevents is research that costs an hour and changes nothing: ten tabs of trivia, a "tech stack" pasted from a profile, and an email that opens with the company's founding year. Every item in the brief has to change who gets contacted, what gets said, or when. Paid lookups follow the same rule. Tech Stack Search costs $4.99 per technology, so it runs only for a technology whose presence or absence flips the pitch.

## When to Use

- "Brief me on harborlinelogistics.com before Thursday's call."
- "Research our 10 tier 1 accounts before the AEs start."
- "What do we know about Acme, and who should I email there?"
- "Account plan for this enterprise target."
- A reply came in from a good account and the rep wants context fast.

Use a different skill when:

| The user wants | Use |
|-|-|
| Decision makers at 50+ accounts, no per-account brief | `decision-maker-finder` |
| A list of companies that match an ICP | `icp-list-builder` |
| Every store running a given app or platform | `ecommerce-by-techstack` |
| A list built from an event (funding, hiring, leadership change) across many companies | `signal-triggered-outbound` |
| The email itself, once the brief exists | `cold-email-copywriting` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Account domain(s), 1-10 | Every lookup keys on domain | Ask; resolve names with `companyName` |
| What the user sells, in one line | Picks the roles and the technologies worth checking | Ask |
| Purpose: first cold email, discovery call, renewal, expansion | Sets depth and which sections lead | First cold email |
| Deadline and time box | Research expands to fill the time | Standard depth, 30 minutes per account |
| Budget for paid lookups | Tech Stack Search is $4.99 per technology | $15 per account; ask above that |
| Technologies that would change the pitch | Decides whether Tech Stack Search runs | Derive from the product in step 4 |

### Depth tiers

| Tier | Time box | Paid tools | Use for |
|-|-|-|-|
| Quick | 10 minutes | `validate_emails` only | A reply that needs context in the next hour |
| Standard | 30 minutes | Website Finder, Email Finder, validation; Tech Stack Search when it flips the pitch | Tier 1 accounts before a sequence |
| Deep | 60-90 minutes | Standard plus EDGAR filings for public companies | Enterprise targets, a discovery call with an exec |

## Authoritative Foundations

| Source | What it contributes |
|-|-|
| Gartner B2B buying research | Complex purchases involve 6 to 10 decision makers. The brief names 3-4 of them by role so the rep knows who else will weigh in. |
| MEDDIC, created at PTC in 1996 by Dick Dunkel with Jack Napoli under John McMahon | Economic Buyer and Champion become the first two people in the brief; Metrics and Identify Pain shape the hypothesis. |
| Craig Elias, trigger events (CustomerThink, 2008; book *SHiFT!*) | Buyers move from status quo into a "window of dissatisfaction" after a bad experience, a transition (new leader, new rules, new priorities) or new awareness. The Why Now section sorts every signal into those three types. |
| US SEC EDGAR | For public companies, the 10-K (business description, risk factors) and 8-K (Item 5.02 for officer changes) are primary evidence. Full-text search covers filings since 2001. |
| Alex Berman, personalization levels | His templates page describes segment, account (news, funding, hiring, leadership change) and person (a post, podcast or talk) personalization, with depth matched to the buyer. A tier 1 account earns account and person level; see `references/alex-berman-cold-email.md`. |
| `references/list-quality-standard.md` | Validation buckets and column names for the people table. |

Source details and the routing table: `references/framework-notes.md`.

## Workflow

### 1. Scope the brief

Write one line per account: domain, what the user sells, purpose, depth tier, budget. List the 1-3 technologies whose presence would change the pitch (step 4). If the user names more than 10 accounts, switch to `decision-maker-finder` for the people and run this skill on the top 10 only.

### 2. Snapshot from the Lead Database

Call `query_lead_database` with `companyDomain` and `limit: 1`. The returned row carries company fields (industry, employee count, revenue, website, HQ city, state and country, keywords), and `pagination.total` is the number of people the database holds for the domain. Then size the teams that matter with more `limit: 1` counts, one per department or title family (for example sales titles, engineering titles). These counts cost nothing and tell the rep how big the team they are selling into is.

| Field read | Use in the brief |
|-|-|
| `company_industry`, `keywords` | One-line description; check it matches the user's ICP |
| `employees_count` or `company_size` | Size band and which role map row applies |
| `company_annual_revenue` | Budget plausibility for the deal size |
| `company_city`, `company_state`, `company_country` | Time zone, law (CAN-SPAM, CASL, PECR) |
| `pagination.total` for the domain | Contactable footprint |
| Team-size counts | "41 people with sales titles" beats "mid-size sales team" |

### 3. Key people

Pick the roles from the product category (the role map in `decision-maker-finder` lists 22 categories). Query the Lead Database with `companyDomain`, the role's `title` list, `seniority` and the universal `notTitle` set, `limit: 25`. Rank by title match, seniority, email present. For an empty role, run `scrape_website_finder` on the domain with one `jobTitle`. For a name without an email, run `find_emails`. Validate every email that did not come from Email Finder with `validate_emails`. Keep 3-4 people: economic buyer, champion, evaluator, and a backup.

For each person, add one person-level detail if it exists within the time box: start date in role, a post, a talk, a podcast. Cite it.

### 4. Tech stack: only what changes the pitch

Run the decision table in `references/tech-stack-decision-guide.md`:

| Question | If yes | If no |
|-|-|-|
| Would knowing this technology change the opening line, the case study, or whether to contact at all? | Candidate for checking | Skip it; do not list it in the brief |
| Can a free signal settle it (the site's page source, a job posting, the validator's `sc_mx_provider`)? | Use the free signal, mark "likely" | Candidate for Tech Stack Search |
| Will the same technology be checked for 5+ accounts this month? | Run Tech Stack Search once and reuse the domain list for every account | Run it only if the deal size justifies $4.99 |

Tech Stack Search (`scrape_builtwith`) takes one `technology` and returns every domain detected using it. Search the downloaded CSV for the account's domain. Keep the file: it answers the same question for every other account at no extra cost and seeds `ecommerce-by-techstack` or a TAM build.

### 5. Why now

Collect dated signals from primary sources first: the company's newsroom and careers page, EDGAR for public companies, the executive's own posts or interviews, then press coverage. Sort each into Elias's three types (bad experience, transition, awareness). Signals older than 12 months go to background. Job postings count as transitions when they describe a new team, a new tool or a rebuild.

### 6. Hypothesis and talking points

Write a two-sentence hypothesis: the likely pain and why this quarter. Then 3-5 talking points, each tied to a cited source. A talking point that cannot cite a source is cut. Map them to MEDDIC: which metric the buyer is judged on, who signs, who champions.

### 7. Contact plan

Order the people, pick the channel and day for each, and the angle. Never email two people at the same account on the same day; Berman's guidance is to start at the top and move down a level after one to two weeks without a reply. Put mobiles only where the user has a lawful use (see `decision-maker-finder` compliance notes).

### 8. Write and check

Fill `templates/output-template.md`, list every source with a URL and the date checked, and run `scripts/check-output.py`.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Snapshot, team counts, people | `query_lead_database` | Included on Growth and Scale; 100,000 new leads a day |
| Missing role at the domain | `scrape_website_finder` | $0.0499 per contact found |
| Email from a name and domain | `find_emails` | $0.05 per email found, free if not found |
| Validate emails, read mail provider and gateway | `validate_emails` | $0.0072 per email |
| Technology presence | `scrape_builtwith` (Tech Stack Search) | $4.99 per technology |
| Mobile for a manual call, if asked | `find_mobiles` | $0.25 per number found, free if not found |
| Runs | `check_run_status`, `download_results`, `list_runs` | Free |

### Calls

Snapshot and team count:

```json
{"companyDomain": "harborlinelogistics.example", "limit": 1}
{"companyDomain": "harborlinelogistics.example", "title": "Account Executive, Sales, Carrier Sales, Business Development", "notTitle": "assistant, intern, former", "limit": 1}
```

People for one role:

```json
{"companyDomain": "harborlinelogistics.example",
 "title": "Chief Revenue Officer, CRO, VP Sales, Director of Sales Operations, Revenue Operations, Salesforce Administrator",
 "notTitle": "assistant, intern, former, retired, advisor",
 "limit": 25}
```

Missing role:

```json
{"domains": ["harborlinelogistics.example"], "jobTitle": "Salesforce Administrator", "autoValidateEmails": false}
```

Email for a known name: `{"contacts": [{"first_name": "Priya", "last_name": "Natarajan", "domain": "harborlinelogistics.example"}]}`

Tech Stack Search, MCP: `{"technology": "HubSpot", "fileName": "techstack-hubspot-20261013"}`. CLI: `npx scrapercity builtwith "HubSpot"`. REST: `POST /api/v1/scrape/techstack`. Poll `check_run_status` after 30 seconds, then `download_results`, then search the CSV for the account's registrable domain.

### Worked cost estimate

One Standard brief, two technologies that flip the pitch (Salesforce and HubSpot), four people:

| Item | Units | Unit price | Cost |
|-|-:|-:|-:|
| Lead Database snapshot, 2 team counts, 9 people | 12 records | Included in Growth | $0.00 |
| Tech Stack Search | 2 technologies | $4.99 | $9.98 |
| Website Finder for the missing evaluator | 1 contact found | $0.0499 | $0.05 |
| Email Finder for the champion | 1 email found | $0.05 | $0.05 |
| validate_emails | 3 emails | $0.0072 | $0.02 |
| Total | | | $10.10 |

Ten tier 1 accounts checked against the same two technology lists cost $9.98 for Tech Stack Search in total, not $99.80, so the per-account cost falls to about $1.12. Because the first brief exceeds $5, call `check_wallet`, show this table and wait for a yes.

### Error handling

| Response | Action |
|-|-|
| `pagination.total` is 0 for the domain | Try `companyName`, the parent company's domain, or the regional domain; note the alias |
| 503 on a people query | Shorten the title list or split it into two calls |
| Tech Stack Search CSV does not contain the domain | Record "not detected", which is weaker than "not used"; check one free signal before telling the rep |
| 402 | `check_wallet`, report the shortfall, finish the brief with free sources |
| 409 on a Tech Stack Search start | The same technology was submitted moments ago; reuse that run from `list_runs` |

## Output Format

1. `account-brief-[domain]-[date].md` following `templates/output-template.md`: Account Snapshot, Why Now, Tech Stack, Key People, Hypothesis and Talking Points, Contact Plan, Sources, Cost Estimate, Open Questions and Next Steps.
2. `account-people-[domain]-[date].csv`: the people table with the person columns from `references/list-quality-standard.md` section 2a plus `buying_role` and `found_by`.
3. Saved Tech Stack Search CSVs named `techstack-[technology]-[date].csv` for reuse.

## Quality Check

- [ ] Every talking point and every Why Now signal cites a source ID that appears in Sources with a URL and a date checked.
- [ ] Every signal has a date; anything older than 12 months is marked background.
- [ ] Every Tech Stack row says whether it changes the pitch; rows that do not were checked with free signals only.
- [ ] Tech Stack Search ran only for technologies marked as changing the pitch, and the cost table shows $4.99 per technology.
- [ ] Key People has 3-4 people, each with a buying role, an email status and a `found_by` tool; only `valid` emails are marked ready to send.
- [ ] The contact plan never puts two people at the account on the same day.
- [ ] The brief fits on two pages.
- [ ] `scripts/check-output.py brief.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Paying $4.99 for a technology that does not change the pitch | Spend with no effect on the email | Run the decision table first; list only pitch-changing technologies. |
| Reading "not detected" as "not used" | Detection misses tools without a public footprint, such as many CRMs | Say "not detected" and check one free signal. |
| One Tech Stack Search per account | Same $4.99 paid ten times for one list | Run once per technology, reuse the CSV across accounts. |
| Signals without dates | A two-year-old funding round reads as news | Date every signal; older than 12 months is background. |
| Opening with company trivia | Reads as a template; nothing for the buyer | Open with a dated trigger tied to their role. |
| Emailing the CRO and the VP Sales the same morning | Looks like a blast; they compare notes | One person at a time, move down after one to two weeks. |
| Using People Finder for a B2B brief | Public-record lookups on individuals are outside a sales brief's purpose | Stay with the Lead Database, Website Finder and Email Finder. |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or the routing table. |
| `references/research-playbook.md` | Running steps 2, 3, 5 and 6: Lead Database recipes, signal catalog, EDGAR forms, question bank, recipes by account type. |
| `references/tech-stack-decision-guide.md` | Step 4: which technologies change which pitch, free signals, cost amortization, reading results. |
| `references/list-quality-standard.md` | Column names and validation buckets for the people table (shared). |
| `references/alex-berman-cold-email.md` | Personalization levels and account sequencing (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling, retries (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database rules (shared). |
| `templates/output-template.md` | Writing the brief. |
| `examples/worked-example.md` | A finished brief for a 350-person freight brokerage. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py brief.md`. |

## Related Skills

- `decision-maker-finder` for the people at many accounts at once.
- `icp-list-builder` to find more accounts like the one researched.
- `ecommerce-by-techstack` to turn a saved Tech Stack Search CSV into a list.
- `signal-triggered-outbound` to build lists from the trigger types in Why Now.
- `cold-email-copywriting` to write the first email from the talking points.
- `multi-channel-outreach` to sequence email, phone and LinkedIn across the people.
- `crm-enricher` to write the people and brief back to the CRM.
