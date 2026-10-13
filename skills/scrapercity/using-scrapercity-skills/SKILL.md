---
name: using-scrapercity-skills
description: >-
  Routes any lead generation, list building or outbound request to the right
  ScraperCity skills in the right order, picks the cheapest tool path, prices
  it from the live catalog, and sets the wallet, count and compliance gates
  before anything is spent. Produces a routing plan: the skill chain, tool
  calls with a cost estimate, gates and handoffs. Use when a request spans
  more than one skill ("find dentists in Austin and email them", "build a
  pipeline for my agency"), when it is unclear which skill fits, or at the
  start of any ScraperCity session.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags: [router, index, lead-generation, outbound, scrapercity, mcp]
  related_skills: [scrapercity-mcp, scrapercity-cli, scrapercity-api, scrapercity-integrations, scrapercity-lead-database, scrapercity-local-business-database, scrapercity-real-estate-data, icp-list-builder, tam-builder, local-business-list, cold-email-list, cold-email-strategy, outbound-unit-economics]
  frameworks:
    - "ScraperCity - tool catalog and pricing (scrapercity npm package 1.0.17, scrapercity.com/pricing)"
    - "Agent Skills specification - progressive disclosure (agentskills.io)"
    - "Alex Berman - targeting and offer before copy"
    - "FTC - CAN-SPAM Act compliance guide for business"
    - "FCC - TCPA rules, 47 CFR 64.1200"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md, outbound-compliance-primer.md, list-quality-standard.md, alex-berman-cold-email.md]
---

# Using ScraperCity Skills

## Overview

This repo holds 30 skills in three categories. This one is the entry point. It reads a request, decides which skills run and in what order, chooses the cheapest ScraperCity tool path for each data step, prices the job from `references/scrapercity-catalog.md`, and writes down the gates that must pass before money is spent or a message is sent.

The mistakes it prevents:

- Running a paid scrape when the same records sit in a database the user's plan already includes. A Google Maps scrape of 2,000 dentists costs $19.80; the same pull from the Local Business Database costs nothing extra on Growth and up.
- Writing copy before anyone has sized the market or picked the offer.
- Sending to a list that was never validated, or calling mobiles that were never checked against Do Not Call.
- Loading eight skills when two would do. Each skill is loaded only when its step starts.

## When to Use

- The request names an outcome rather than a tool: "get me meetings with HVAC owners in Texas", "build a list and a sequence for my agency".
- The request crosses categories: data plus copy, data plus calling, data plus CRM.
- It is unclear whether a job is a database pull, a scrape or an enrichment.
- At the start of a session, to confirm setup (MCP, CLI or API) and the plan tier.

Go straight to a single skill when the request is narrow and named: "clean this CSV" is `email-list-cleaner`, "write three follow-ups" is `cold-email-copywriting`.

## Prerequisites

Collect, or mark unknown:

- Who the user sells to, and what they sell (one sentence each).
- How they will reach people: email, phone, LinkedIn, mail, or a mix.
- The access path in use: MCP server, CLI, REST API, or the dashboard.
- Plan tier. Starter ($49) has no database access; Growth ($149) and Scale ($649) include the Lead, Local Business and Ecommerce databases.
- Budget ceiling for this job, and the wallet balance from `check_wallet`.
- Countries in scope, because they change the compliance gate.

## Authoritative Foundations

| Source | What it sets in this skill |
|-|-|
| ScraperCity catalog (npm package 1.0.17) and scrapercity.com/pricing | Every tool id, input and per-result price used in routing and cost estimates. Generated into `references/scrapercity-catalog.md`. |
| ScraperCity platform facts | Plan tiers, database allowances (100,000 new records a day), `excludeDelivered` and cursor paging. See `references/scrapercity-platform.md`. |
| Agent Skills specification (agentskills.io) | Progressive disclosure: metadata first, SKILL.md on activation, references only when a step needs them. The router loads skills step by step for this reason. |
| Alex Berman, alexberman.com | Targeting and offer decide most of the result, so the chain sizes the market and fixes the offer before any copy. See `references/alex-berman-cold-email.md`. |
| FTC CAN-SPAM guide, FCC 47 CFR 64.1200, FTC FCRA guidance | The compliance gates the router attaches to email, phone and public-records steps. See `references/outbound-compliance-primer.md`. |

## Workflow

### 1. Restate the job as an outcome

Write one line: who, how many, by when, through which channel, toward what result (meetings, a TAM file, an enriched CRM). If the user gave a tool ("scrape Google Maps"), keep it as a preference, not a rule; step 3 may find a cheaper path.

### 2. Match intents to skills

Use `references/routing-matrix.md`. Most requests match two to four intents. Typical chains:

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
| Count | Show a count or a cost estimate and get a go-ahead before any pull over about $5. |
| Compliance | Email: CAN-SPAM opt-out and postal address, plus CASL or PECR when those countries are in scope. Phone: TCPA and DNC scrub. People Finder, Property Lookup and Criminal Records: never for employment, tenant, credit or insurance decisions (FCRA). |
| Quality | Every send-ready email validated. Lists meet `references/list-quality-standard.md`. |
| Deliverability | No new campaign on a domain without SPF, DKIM, DMARC and a warmed inbox. |

### 6. Hand off

Load the first skill in the chain and follow it. When its deliverable passes its own `scripts/check-output.py`, move to the next skill and pass the output file along. Do not preload later skills.

## ScraperCity Implementation

Confirm the access path first:

| Path | Check | Skill |
|-|-|-|
| MCP | `check_wallet` returns a balance | `scrapercity-mcp` |
| CLI | `npx scrapercity wallet` prints a plan and balance | `scrapercity-cli` |
| REST | `GET /api/v1/wallet` with `Authorization: Bearer $SCRAPERCITY_API_KEY` returns 200 | `scrapercity-api` |
| No-code | Clay, n8n, Zapier or a sequencer | `scrapercity-integrations` |

Then run the shared operating rules in `references/scrapercity-agent-patterns.md`: wallet first, count before pull, start-poll-download, Apollo by webhook, `excludeDelivered=true` with `after` cursors for repeat pulls.

Worked routing estimate: "Email 1,500 dentists in Austin and Houston, Growth plan."

| Step | Tool | Units | Unit price | Cost |
|-|-|-:|-:|-:|
| Pull businesses with a website and email | `query_local_business_database` | 1,500 | $0.00 (included) | $0.00 |
| Fill gaps where the database is thin | `scrape_maps` | 300 | $0.0099 | $2.97 |
| Validate every email before sending | `validate_emails` | 1,800 | $0.0072 | $12.96 |
| **Total** | | | | **$15.93** |

The same job on Starter, with Maps for all 1,800 businesses: 1,800 x $0.0099 = $17.82, plus $12.96 validation = $30.78. Show both and let the user choose.

## Output Format

A routing plan in Markdown, built from `templates/output-template.md`:

1. **Request** - the one-line outcome, channel, plan tier, access path, budget.
2. **Skill Chain** - ordered table: step, skill, what it produces, done-when.
3. **Tool Calls and Cost** - one row per paid tool with units, unit price and cost, and a total.
4. **Gates** - wallet, count, compliance, quality, deliverability, each with its status.
5. **Handoffs** - which file moves from each skill to the next.
6. **Open Questions** - anything marked unknown in Prerequisites.

## Quality Check

- Every skill named in the chain exists in this repo.
- Every paid tool row multiplies out, and the rows sum to the total.
- Unit prices match `references/scrapercity-catalog.md`.
- A database path was considered before any scraper, and the plan says why a scraper was still needed.
- A compliance gate exists for every channel in the plan, and an FCRA line exists whenever People Finder, Property Lookup or Criminal Records appears.
- No copy or sending step comes before the list and offer steps.

Run `scripts/check-output.py routing-plan.md`.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Scraping Maps on a Growth account without checking the Local Business Database | Pays $0.0099 a row for records already included | Count the database first; scrape only the gap |
| Polling an Apollo run every minute | Runs take hours to days; the polls waste rate limit | Webhook, or check once an hour |
| Loading every skill up front | Floods context, and later skills' rules get cut off | Load each skill when its step starts |
| Writing the sequence before the list exists | Copy cannot use fields nobody pulled | List and offer first, then copy |
| Treating People Finder output as a screening report | FCRA exposure | Prospecting and research only, stated in the plan |
| Skipping validation because the source "has verified emails" | Bounce rates still rise on old or catch-all addresses | Validate every address that will be sent |

## Execution Artifacts

- `references/framework-notes.md` - which sources shape the routing, and which file to open for what.
- `references/routing-matrix.md` - intent to skill table with trigger phrases, first tool and typical cost driver.
- `references/chains.md` - nine end-to-end playbooks with skill order, files passed between skills and worked costs.
- `references/scrapercity-catalog.md` - shared; every tool, endpoint and price.
- `references/scrapercity-platform.md` - shared; plans, databases, integrations.
- `references/scrapercity-agent-patterns.md` - shared; the operating rules for every call.
- `references/outbound-compliance-primer.md` - shared; channel and country rules.
- `references/list-quality-standard.md` - shared; what makes a list send-ready.
- `references/alex-berman-cold-email.md` - shared; the targeting-and-offer-first principle behind chain order.
- `templates/output-template.md` - the routing plan shell.
- `examples/worked-example.md` - a full routing plan for an HVAC agency's outbound program.
- `scripts/check-output.py` - checks a routing plan: known skills, cost arithmetic, catalog prices, gates.

## Related Skills

- `scrapercity-mcp`, `scrapercity-cli`, `scrapercity-api`, `scrapercity-integrations` - access paths.
- `scrapercity-lead-database`, `scrapercity-local-business-database`, `scrapercity-real-estate-data` - the data products.
- `icp-list-builder`, `tam-builder`, `local-business-list`, `cold-email-list` - the most common first steps.
- `cold-email-strategy`, `outbound-unit-economics` - the most common second steps.
