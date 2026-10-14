---
name: using-scrapercity-skills
description: >-
  Routes any lead generation, list building or outbound request to the right
  ScraperCity skills in the right order, picks the cheapest tool path, prices
  it from the live catalog, and sets the wallet, count, suppression, quality
  and deliverability gates before anything is spent or sent. Produces a
  routing plan: the skill chain with one owner skill, tool calls with a cost
  estimate, gates and handoffs. Use when a request spans more than one skill
  ("find dentists in Austin and email them", "build a pipeline for my
  agency"), when it is unclear which skill fits, when a job needs a waterfall,
  a bulk CSV enrichment or job-change tracking, when installing or checking
  these skills, or at the start of any ScraperCity session.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags:
    - router
    - index
    - lead-generation
    - outbound
    - scrapercity
    - mcp
  related_skills:
    - scrapercity-mcp
    - scrapercity-cli
    - scrapercity-api
    - scrapercity-integrations
    - scrapercity-lead-database
    - scrapercity-local-business-database
    - scrapercity-real-estate-data
    - icp-list-builder
    - tam-builder
    - local-business-list
    - cold-email-list
    - cold-email-strategy
    - outbound-unit-economics
  frameworks:
    - "ScraperCity - tool catalog and pricing (scrapercity npm package 1.0.17, scrapercity.com/pricing)"
    - "Agent Skills specification - progressive disclosure (agentskills.io)"
    - "Alex Berman - targeting and offer before copy"
    - "Google - Email sender guidelines and FAQ (2024)"
    - "Yahoo - Sender Hub best practices (2024)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
    - list-quality-standard.md
    - alex-berman-cold-email.md
    - experts.md
    - glossary.md
---

# Using ScraperCity Skills

## Overview

This repo holds 31 skills in three categories. This one is the entry point. It reads a request, decides which skills run and in what order, chooses the cheapest ScraperCity tool path for each data step, prices the job from `references/scrapercity-catalog.md`, and writes down the gates that must pass before money is spent or a message is sent.

The mistakes it prevents:

- Running a paid scrape when the same records sit in a database the user's plan already includes. A Google Maps scrape of 2,000 dentists costs $19.80; the same pull from the Local Business Database costs nothing extra on Growth and up.
- Writing copy before anyone has sized the market or picked the offer.
- Sending to a list that was never validated, or calling people who already asked not to be contacted because the suppression list lived in one tool only.
- Loading eight skills when two would do. Each skill is loaded only when its step starts.

## When to Use

- The request names an outcome rather than a tool: "get me meetings with HVAC owners in Texas", "build a list and a sequence for my agency".
- The request crosses categories: data plus copy, data plus calling, data plus CRM.
- It is unclear whether a job is a database pull, a scrape or an enrichment.
- At the start of a session, to confirm setup (MCP, CLI or API) and the plan tier.
- The user wants these skills installed in an agent, or wants to check an install.

Go straight to a single skill when the request is narrow and named: "clean this CSV" is `email-list-cleaner`, "write three follow-ups" is `cold-email-copywriting`.

## Prerequisites

Collect, or mark unknown:

- Who the user sells to, and what they sell (one sentence each).
- How they will reach people: email, phone, LinkedIn, mail, or a mix.
- The access path in use: MCP server, CLI, REST API, or the dashboard.
- Plan tier. Starter ($49) has no database access; Growth ($149) and Scale ($649) include the Lead, Local Business and Ecommerce databases.
- Budget ceiling for this job, and the wallet balance from `check_wallet`.
- Countries in scope, because they change the database filters (person vs company country).
- Lists the team already keeps: customers, open opportunities, unsubscribes, bounces, do-not-contact requests. They become the suppression gate.

## Authoritative Foundations

| Source | What it sets in this skill |
|-|-|
| ScraperCity catalog (npm package 1.0.17) and scrapercity.com/pricing | Every tool id, input and per-result price used in routing and cost estimates. Generated into `references/scrapercity-catalog.md`. |
| ScraperCity platform facts | Plan tiers, database allowances (100,000 new records a day), `excludeDelivered` and cursor paging. See `references/scrapercity-platform.md`. |
| Agent Skills specification (agentskills.io) | Progressive disclosure: metadata first, SKILL.md on activation, references only when a step needs them. The router loads skills step by step for this reason. |
| Alex Berman, alexberman.com | Targeting and offer decide most of the result, so the chain sizes the market and fixes the offer before any copy. See `references/alex-berman-cold-email.md`. |
| Google Email sender guidelines and FAQ; Yahoo Sender Hub | The operational send gate: one-click unsubscribe for bulk mail, removals inside 2 days (Google asks for 48 hours), spam rate kept under 0.1% and never at 0.3%. These are mailbox provider rules that decide inbox placement. |

## Workflow

### 1. Restate the job as an outcome

Write one line: who, how many, by when, through which channel, toward what result (meetings, a TAM file, an enriched CRM). If the user gave a tool ("scrape Google Maps"), keep it as a preference, not a rule; step 3 may find a cheaper path.

### 2. Match intents to skills

Use `references/routing-matrix.md`. A typical request matches two to four intents. Typical chains:

| Request shape | Chain |
|-|-|
| "Find X in city Y and email them" | `local-business-list` then `cold-email-strategy`, `cold-email-copywriting`, `sending-platforms` |
| "Build a list like my best customers" | `icp-list-builder` then `cold-email-list` |
| "Who should I talk to at these accounts?" | `decision-maker-finder`, then `account-researcher` for the top tier |
| "How big is my market?" | `tam-builder`, then `outbound-unit-economics` |
| "Fix the data in our CRM" | `crm-enricher`, then `email-list-cleaner` |
| "Call list for my SDRs" | list skill, then `mobile-appender`, then `cold-calling` |
| "Reach property owners" | `scrapercity-real-estate-data`, then `skip-tracer`, then `multi-channel-outreach` |
| "New cold email setup from zero" | `domain-infrastructure`, `inbox-setup`, `email-deliverability`, `sending-platforms` |
| "Enrich this CSV / CRM export in bulk" | `scrapercity-api` (bulk pipeline) or `crm-enricher`, then `email-list-cleaner` |
| "Try the database, then the finders, only pay when needed" | `scrapercity-integrations` (waterfall recipes), then `email-list-cleaner` |
| "Tell us when champions change jobs" | `scrapercity-integrations` (job-change tracking), then `cold-email-copywriting` for the note |

One skill owns the final deliverable; every other skill in the chain must hand it a concrete input or act as a check. If a skill adds neither, drop it.

Full end-to-end playbooks are in `references/chains.md`.

### 3. Pick the cheapest data path

For every data step, walk this order and stop at the first source that covers the need:

1. **A database the plan includes.** Lead Database for people at companies, Local Business Database for storefront businesses, Ecommerce Database for online stores. Records the account already has are free to fetch again.
2. **A scraper priced per result.** Store Leads ($0.0039 per lead), Google Maps ($0.0099 per business), Yelp and Angi ($0.0099), Apollo URLs ($0.0039 per lead, hours to days).
3. **Pay-on-find enrichment.** Email Finder ($0.05 per email found), Mobile Finder ($0.25 per number found). Nothing is charged when nothing is found.
4. **Per-search lookups.** People Finder ($0.0199 per result, a 0-match search billed as 1), Property Lookup ($0.15, plus $0.10 for owner contact), Tech Stack Search ($4.99 per technology).

On Starter, step 1 is unavailable. Price the scraper path, and show the Growth upgrade as an option when the database would cover the job.

### 4. Price the job

For each paid tool: units times unit price, with units estimated from a count call or a stated hit-rate assumption. Add validation for every email that will be sent ($0.0072 each). Sum it. Compare the total with the wallet balance and the user's ceiling.

### 5. Set the gates

Every plan carries these gates, in this order:

| Gate | Rule |
|-|-|
| Wallet | `check_wallet` before the first paid call. On 402, stop and report the shortfall. |
| Count | Show a count and a cost estimate, and get a go-ahead before any paid run. |
| Suppression | One suppression list across every sending tool and dialer (unsubscribes, hard bounces, complaints, do-not-contact requests, customers, open opportunities), applied before every send and every call block. Email: a one-click unsubscribe header and removals inside 2 days (Google and Yahoo bulk sender rules). Phone: the internal do-not-contact list checked before each block. |
| Quality | Every send-ready email validated. Lists meet `references/list-quality-standard.md`. People Finder and Property Lookup contacts used only where the returned name and address match the input. |
| Deliverability | No new campaign on a domain without SPF, DKIM, DMARC and a warmed inbox. |

### 6. Hand off

Load the first skill in the chain and follow it. When its deliverable passes its own `scripts/check-output.py`, move to the next skill and pass the output file along. Do not preload later skills.

## ScraperCity Implementation

Pick the access path by how the job runs, then confirm it works:

| Path | Use it when | Check | Skill |
|-|-|-|-|
| MCP | A person works the job in an AI client: counts, samples, one-off runs, setup | `check_wallet` returns a balance | `scrapercity-mcp` |
| CLI | Shell scripts, cron or CI on a machine the team controls | `npx scrapercity wallet` prints a plan and balance | `scrapercity-cli` |
| REST | A backend service, a bulk file pipeline, or a webhook receiver in code | `GET /api/v1/wallet` with `Authorization: Bearer $SCRAPERCITY_API_KEY` returns 200 | `scrapercity-api` |
| No-code | The flow lives in Clay, n8n, Zapier, Make, a sheet, a CRM or a sender | The platform's HTTP step returns the wallet JSON | `scrapercity-integrations` |

A recurring job never runs from a chat: it moves to CLI cron, a REST service or a no-code schedule, and the chat keeps the count, the estimate and the check.

Then run the shared operating rules in `references/scrapercity-agent-patterns.md`: wallet first, count before pull, start-poll-download, Apollo by webhook, `excludeDelivered=true` with `after` cursors for repeat pulls.

Worked routing estimate: "Email 1,500 dentists in Austin and Houston, Growth plan."

| Step | Tool | Units | Unit price | Cost |
|-|-|-:|-:|-:|
| Pull businesses with a website and email | `query_local_business_database` | 1,500 | $0.00 (included) | $0.00 |
| Fill gaps where the database is thin | `scrape_maps` | 300 | $0.0099 | $2.97 |
| Validate every email before sending | `validate_emails` | 1,800 | $0.0072 | $12.96 |
| **Total** | | | | **$15.93** |

The same job on Starter, with Maps for all 1,800 businesses: 1,800 x $0.0099 = $17.82, plus $12.96 validation = $30.78. Show both and let the user choose.

### Install and verify these skills

| Agent | Install |
|-|-|
| Claude Code | `/plugin marketplace add scrapercity/gtm-skills`, then `/plugin install gtm-skills@scrapercity` |
| Codex, Copilot, Cursor, Gemini CLI, OpenCode, Windsurf, goose | Clone `https://github.com/scrapercity/gtm-skills` and check out a release tag, then `./install.sh --target <agent> --scope project --bundle platform` (the bundle includes this router; add `--dry-run` first to see the folders) |
| GitHub CLI 2.90 and later | `gh skill install scrapercity/gtm-skills using-scrapercity-skills --pin <release tag>` (public preview; flags may change) |
| Any other agent | `./install.sh --dest <its skills folder> --skill <name>`, or copy a skill folder by hand; each folder carries its own shared references |

Project scope by default: skills include small Python checker scripts, so read them and install where they are needed rather than in every project. Pin a release tag so a later change to a skill never alters a running campaign mid-month. Verify in three steps:

1. Files: `python3 scripts/generate-lock.py --verify <skills folder>` from a clone at the same tag reports no `MISMATCH` or `MISSING` lines (a `gh`-installed `SKILL.md` shows one expected mismatch for its tracking fields).
2. Checker: `python3 scripts/check-output.py examples/worked-example.md` in any installed skill prints PASS.
3. Routing: in a new session ask "email 200 dentists in Austin, Growth plan". The agent should load this router, name `local-business-list` as the first skill, and price validation at $0.0072 an email before anything runs.

Every flag, bundle and agent folder is in the repo's `docs/INSTALL.md`; the lock format is in `docs/INTEGRITY.md`.

## Output Format

A routing plan in Markdown, built from `templates/output-template.md`:

1. **Request** - the one-line outcome, channel, plan tier, access path, budget, and when the first file is ready (database pages in seconds, most runs in minutes, Apollo in hours to days).
2. **Skill Chain** - ordered table: step, skill, what it produces, done-when.
3. **Tool Calls and Cost** - one row per paid tool with units, unit price and cost, and a total.
4. **Gates** - wallet, count, suppression, quality, deliverability, each with its status.
5. **Handoffs** - which file moves from each skill to the next.
6. **Open Questions** - anything marked unknown in Prerequisites.

- Each fact once; every call and script written out in full (no `"..."` values, no loop described in a comment); no counts or results marked assumed. If nothing has run, say so once at the top.
- What the reader receives is the deliverable only: no internal file paths, reference section numbers or runbook IDs; another skill is named only in a handoff line that tells the user what to run next; no tables of checks that were not run (one "Not checked:" line instead); and no repeated identical rows where one template plus a list will do.

## Quality Check

- Every skill named in the chain exists in this repo.
- Every paid tool row multiplies out, and the rows sum to the total.
- Unit prices match `references/scrapercity-catalog.md`.
- A database path was considered before any scraper, and the plan says why a scraper was still needed.
- A suppression gate covers every channel in the plan: unsubscribe handling for email, the do-not-contact list for phone, and a match check whenever People Finder or Property Lookup appears.
- Exactly one skill owns the final deliverable, and every other skill in the chain hands it an input or checks it.
- The plan contains no legal commentary; every rule in it is a setting tied to cost, replies or inbox placement.
- No copy or sending step comes before the list and offer steps.

Run `scripts/check-output.py routing-plan.md`.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Scraping Maps on a Growth account without checking the Local Business Database | Pays $0.0099 a row for records already included | Count the database first; scrape only the gap |
| Polling an Apollo run every minute | Runs take hours to days; the polls waste rate limit | Webhook, or check once an hour |
| Loading every skill up front | Floods context, and later skills' rules get cut off | Load each skill when its step starts |
| Writing the sequence before the list exists | Copy cannot use fields that were never pulled | List and offer first, then copy |
| Using a People Finder result without checking the match | A wrong-person match wastes the dial and the $0.0199 lookup | Keep only results whose name and address match the input; send the rest to review |
| Suppression lists kept separately in each tool | Someone who unsubscribed in one sender gets mailed from another, and complaints rise | One list, synced into every sender and dialer before each send |
| Skipping validation because the source "has verified emails" | Bounce rates still rise on old or catch-all addresses | Validate every address that will be sent |

## Execution Artifacts

- `references/framework-notes.md` - which sources shape the routing, and which file to open for what.
- `references/routing-matrix.md` - intent to skill table with trigger phrases, first tool and typical cost driver.
- `references/chains.md` - nine end-to-end playbooks with skill order, files passed between skills and worked costs.
- `references/scrapercity-catalog.md` - shared; every tool, endpoint and price.
- `references/scrapercity-platform.md` - shared; plans, databases, integrations.
- `references/scrapercity-agent-patterns.md` - shared; the operating rules for every call.
- `references/list-quality-standard.md` - shared; what makes a list send-ready.
- `references/alex-berman-cold-email.md` - shared; the targeting-and-offer-first principle behind chain order.
- `references/experts.md` - shared; who each cited authority is, their primary links, and which skills cite them.
- `references/glossary.md` - shared; one-line definitions of repo and data terms, with primary links.
- `templates/output-template.md` - the routing plan shell.
- `examples/worked-example.md` - a full routing plan for an HVAC agency's outbound program.
- `scripts/check-output.py` - checks a routing plan: known skills, cost arithmetic, catalog prices, gates, and that no legal commentary appears.

## Related Skills

- `scrapercity-mcp`, `scrapercity-cli`, `scrapercity-api`, `scrapercity-integrations` - access paths.
- `scrapercity-lead-database`, `scrapercity-local-business-database`, `scrapercity-real-estate-data` - the data products.
- `icp-list-builder`, `tam-builder`, `local-business-list`, `cold-email-list` - the most common first steps.
- `cold-email-strategy`, `outbound-unit-economics` - the most common second steps.
