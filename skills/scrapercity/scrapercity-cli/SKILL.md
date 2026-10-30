---
name: scrapercity-cli
description: >-
  Runs ScraperCity from a terminal with the scrapercity CLI (npm package
  scrapercity 1.0.17): login and key handling, all 27 commands and their flags,
  start-poll-download in shell scripts, daily cron pulls of only new records with
  db-leads and db-local using excludeDelivered and after cursors, CSV piping, and
  CI jobs. Produces a CLI run spec with exact commands, a cost estimate from
  catalog prices, the script, the schedule and failure handling. Use when the
  user wants ScraperCity in bash, cron, a Makefile or GitHub Actions, asks what a
  CLI flag does, hits a CLI error, or asks for a command the CLI may not have.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags:
    - cli
    - bash
    - cron
    - automation
    - ci
    - scripting
    - npx
  related_skills:
    - using-scrapercity-skills
    - scrapercity-mcp
    - scrapercity-api
    - scrapercity-integrations
    - scrapercity-lead-database
    - scrapercity-local-business-database
    - email-list-cleaner
    - cold-email-list
  frameworks:
    - "ScraperCity - scrapercity npm package 1.0.17 (bin/cli.mjs, lib/client.mjs)"
    - "npm - npx and package execution docs"
    - "IEEE and The Open Group - POSIX crontab and shell utilities"
    - "GitHub - Actions workflow syntax, schedule events and encrypted secrets"
    - "AWS Architecture Blog - exponential backoff and jitter"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
---

# ScraperCity CLI

## Overview

This skill turns a ScraperCity job into commands and scripts that run unattended: a count check, a cost estimate, a start command that captures the `runId`, a poll, a download to a named file, and a schedule. It covers every command and flag in `scrapercity` 1.0.17, read from `bin/cli.mjs` and `lib/client.mjs` and exercised against a stubbed network on 2026-10-13.

The mistakes it prevents:

- Scripting around a flag that does not exist, or a command the CLI does not have (there is no `property-lookup` command in 1.0.17).
- Treating `db-leads` output as an export. It prints the total, the next cursor and the first 3 rows only.
- Combining flags that the 1.0.17 parser mixes into other values, such as `scrapercity builtwith Shopify --name x`, which searches for the technology "Shopify x".
- A cron job that dies silently because cron has neither a `PATH` to `node` nor `SCRAPERCITY_API_KEY`.
- A daily pull that re-buys or re-downloads yesterday's records because it skipped `--exclude-delivered` or paged with `--page`.

## When to Use

Use it when the user says:

- "Give me the command to scrape plumbers in Denver" or "what does `--after` do?"
- "Write a script that pulls new leads every morning."
- "Run ScraperCity in GitHub Actions" or "in a Makefile."
- "Validate this CSV's emails from the terminal, then push the good ones into Instantly."
- "`scrapercity` says Unknown command" or "No API key."
- "Is there a CLI command for property lookup / the ecommerce database / webhooks?"

Use a different skill for nearby jobs:

| Job | Skill |
|---|---|
| Using ScraperCity from Claude, Cursor or another AI client | `scrapercity-mcp` |
| HTTP calls from Python, Node, Clay, n8n or Zapier | `scrapercity-api`, `scrapercity-integrations` |
| Designing Lead Database filters | `scrapercity-lead-database` |
| Designing Local Business Database searches | `scrapercity-local-business-database` |
| What to do with the emails after validation | `email-list-cleaner`, `cold-email-list` |

## Prerequisites

- Node.js 18 or newer. Run with `npx -y scrapercity@1.0.17 <command>` (pinned, no install prompt) or install once with `npm i -g scrapercity@1.0.17` and call `scrapercity <command>`.
- An API key from app.scrapercity.com/dashboard/api-docs in `SCRAPERCITY_API_KEY`, or saved by `scrapercity login`.
- `jq` for scripts that write database rows to files. `curl` for the REST calls the CLI does not cover.
- For `db-leads` and `db-local`: Growth ($149/mo) or Scale.

## Authoritative Foundations

| Source | What it contributes here |
|---|---|
| `scrapercity` 1.0.17 `bin/cli.mjs` and `lib/client.mjs` | The command list, every flag and its default, the key lookup order, what each command prints, exit codes, and the parser behavior documented in `references/gaps-and-quirks.md`. The only source for CLI behavior. The README and SKILL tables in the CLI repo carry outdated prices; this skill does not use them. |
| `references/scrapercity-catalog.md` | Every price, endpoint and input schema; the command list for 1.0.17. |
| `references/scrapercity-agent-patterns.md` | Wallet first, count first, a go-ahead before every paid run, polling cadence, error and retry tables, CSV naming. |
| `references/scrapercity-platform.md` | Plans, 100 records per database request, `excludeDelivered`, `after`, 100,000 new records a day. |
| npm docs | `npx --package`, `-y` to skip the install prompt, version pinning. |
| POSIX crontab and shell | Cron runs with a minimal environment; five time fields; `set -e` exit behavior. |
| GitHub Actions docs | `schedule` cron in UTC, encrypted secrets, artifacts. |
| scrapercity.com/api-docs | 100 API requests a minute per key, 10 concurrent scrapes, results kept 48 hours, database allowance resets at midnight UTC. |

Details and routing: `references/framework-notes.md`.

## Workflow

### 1. Set up the key once

```bash
npx -y scrapercity@1.0.17 login          # prompts for the key, writes ~/.scrapercityrc (owner-only)
export SCRAPERCITY_API_KEY=...           # or this; the variable wins over the file
npx -y scrapercity@1.0.17 wallet         # proves the key; prints plan, balance, used, renewal
```

On a shared machine or CI, skip `login` and use the environment variable from a secret store.

### 2. Map the job to commands

Use `references/command-reference.md`. If a tool has no command or a needed flag is missing (see `references/gaps-and-quirks.md`), use the REST call shown there, or the MCP tool.

### 3. Count before you pull

| Source | Count command | Cost |
|---|---|---|
| Lead Database | `db-leads <filters> --limit 1` and read the first line (`N total leads, page 1 of P`) | $0 wallet |
| Local Business Database | `db-local <filters> --limit 1` | $0 wallet |
| Any scraper | A capped test (`maps --limit 25`, `yelp --limit 5`, `store-leads --total-leads 100`) | Catalog price |

A total of 0 prints as `? total leads`. Treat `?` as zero.

### 4. Estimate and confirm

Multiply billable units by catalog price for every step, including the CLI defaults you did not override (`maps` 500 places, `apollo` 1,000 leads, `store-leads` 1,000 leads). Show the table and get a go-ahead before any paid run. For a recurring job, show the monthly total too.

### 5. Start, capture the run id, poll, download

```bash
RUN=$(npx -y scrapercity@1.0.17 maps -q "roofing contractor" -l "Dallas, TX" --limit 300 | awk '/Run ID:/ {print $3}')
npx -y scrapercity@1.0.17 poll "$RUN" --interval 30
npx -y scrapercity@1.0.17 download "$RUN" -o "maps-roofing-dallas-tx-$(date +%Y%m%d)-${RUN:0:8}.csv"
```

`poll` checks every `--interval` seconds (default 15), stops after one hour, exits 1 on FAILED, CANCELLED or timeout, and does not download. Use `--interval 30` or more. Apollo never goes through `poll`: register a webhook at app.scrapercity.com/dashboard/webhooks and check `status` every few minutes.

### 6. Schedule the recurring part

Daily new-record pulls use `--exclude-delivered` with an `--after` cursor that starts at `0` each day. The CLI prints the next cursor as `Next page: --after N`; loop until it stops printing one or the daily target is reached. To write the rows to a file, use the REST loop in `references/scripting-patterns.md`, since the CLI shows only 3 rows per call. Run cron after 00:00 UTC, when the allowance resets.

### 7. Handle failure in the script

Every failure exits 1 and prints `✗ ` plus the server's message to stderr. The HTTP code is not printed (except `HTTP N` when the server sent no message), so branch on the message text. Use the error table in `references/scrapercity-agent-patterns.md`.

### 8. Deliver the spec

Fill `templates/output-template.md` and run `python3 scripts/check-output.py spec.md`. The checker rejects commands and flags that 1.0.17 does not have.

## ScraperCity Implementation

### Commands in 1.0.17 (27 plus help)

| Group | Commands |
|---|---|
| Account and runs | `login`, `wallet`, `runs`, `status`, `poll`, `download`, `cancel`, `logs` |
| B2B people | `apollo`, `db-leads`, `website-finder` |
| Enrichment | `email-find`, `email-validate`, `mobile-find`, `people-find` |
| Local business | `maps`, `yelp`, `angi`, `db-local` |
| Ecommerce and technology | `store-leads`, `builtwith` (Tech Stack Search) |
| Real estate | `zillow-agents`, `crexi`, `distress-list` |
| Other | `bizbuysell`, `airbnb`, `criminal` |

Not in 1.0.17: a property lookup command, an ecommerce database command, webhook management, an Apollo status command, JSON output mode. Workarounds in `references/gaps-and-quirks.md`.

### Database count and cursor loop (CLI only)

```bash
npx -y scrapercity@1.0.17 db-leads --title "VP Sales, Head of Sales" --not-title "Assistant, Intern" \
  --company-country "United States" --min-employees 50 --max-employees 200 \
  --keywords saas --has-email --exclude-delivered --after 0 --limit 100
# 4812 total leads, page 1 of 49
# Next page: --after 98765
```

List flags take commas: `--industry`, `--country`, `--state`, `--seniority`, `--department`, `--company-country`, `--company-state`, `--not-industry` (db-leads) and `--category`, `--country`, `--not-category` (db-local). `db-local --location` takes semicolons because places contain commas: `--location "Houston, TX; Austin, TX; 78701"`.

### Worked cost estimate

Request: a morning job on Growth that adds 400 new VP Sales leads and 100 new Texas dentists a day, validated before they reach the sequencer, for 30 days.

| Line | Units per month | Unit price | Cost per month |
|---|---:|---:|---:|
| `db-leads` new leads (400 a day, cursor loop) | 12,000 | included in Growth | $0.00 |
| `db-local` new businesses (100 a day) | 3,000 | included in Growth | $0.00 |
| `email-validate` on every new email | 15,000 | $0.00169 | $25.35 |
| **Total** | | | **$25.35** |

Per day that is $0.85 and the month is $25.35, which is 16% of Growth's $159 monthly credit. Show the monthly figure once and get an explicit approval before turning on cron. Database pulls use 400 of the Lead Database's 100,000 a day allowance and 100 of the Local Business Database's.

## Output Format

A CLI run spec in Markdown, built from `templates/output-template.md`:

1. **Environment**: package version, Node version, key source, working folder.
2. **Commands**: one row per command with what it maps to and its billable units.
3. **Cost Estimate**: line items, total, approval line.
4. **Script**: the full bash script, ready to save.
5. **Schedule**: cron line or CI schedule, time zone, allowance reset.
6. **Failure Handling**: each failure, how the script detects it, what it does.
7. **Verification**: dry-run results.

A one-command question ("what does `--after` do?", "the command to validate this file") gets the command and two or three lines on what it bills and prints, not a spec. The spec is for scripts, schedules and multi-step jobs.

- Each fact once; every call and script written out in full (no `"..."` values, no loop described in a comment); no counts or results marked assumed. If nothing has run, say so once at the top.
- What the reader receives is the deliverable only: no internal file paths, reference section numbers or runbook IDs; another skill is named only in a handoff line that tells the user what to run next; no tables of checks that were not run (one "Not checked:" line instead); and no repeated identical rows where one template plus a list will do.

## Quality Check

- Every command exists in 1.0.17 and every flag is one that command reads.
- No API key appears in the script; it comes from `SCRAPERCITY_API_KEY` or `~/.scrapercityrc`.
- The script starts with `set -euo pipefail` and checks `wallet` before paid steps.
- `--exclude-delivered` is paired with `--after`, never with `--page` above 1.
- Every start command captures the `runId`; every download names its file with `-o`.
- No `apollo` run is polled with `poll`; a webhook is named.
- Cost lines use catalog prices, CLI defaults are counted, and any paid total (per run or per month) has an approval line.
- Version is pinned in scheduled jobs.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| `scrapercity property-lookup ...` | No such command in 1.0.17 (`Unknown command`) | MCP `scrape_property_lookup` or `POST /api/v1/scrape/property-lookup` |
| Parsing `db-leads` output as the full result | It prints 3 rows and a count of the rest | REST loop with `jq` for files |
| `scrapercity builtwith Shopify --name shopify-us` | Positional words and the `--name` value are joined: technology becomes "Shopify shopify-us" | `scrapercity builtwith Shopify` alone; set a file name through MCP or REST |
| `website-finder --file d.txt --title CEO` | The file name and the title are sent as domains too | MCP `scrape_website_finder` or REST |
| Paying Website Finder for a role at named companies on Growth | The Lead Database may already hold that person, free | `db-leads --domain acme.example --title "VP Sales" --has-email --limit 3` per domain first; Website Finder (MCP or REST) only for domains with no match |
| `bizbuysell URL --limit 50` | `50` is sent as a second start URL | Omit `--limit` (default 100) or use MCP/REST for another cap |
| `yelp -l "Denver, CO"` | Split on commas into "Denver" and "CO", doubling the location combinations | `-l "Denver CO"`; commas only between places |
| `airbnb --city "Lisbon, Portugal"` | Split into two cities; the tool needs "City, Country" | MCP `scrape_airbnb` or REST |
| `--limit=100` | The parser only reads `--flag value` | Use a space |
| Cron with no env | Cron does not load your shell profile | Source a key file and set `PATH` in the script |
| `--exclude-delivered --page 2` | Taking page 1 removes rows from the next query, so page 2 skips records | `--after 0`, then each printed cursor |
| Copying a run id from `runs` | `runs` shows only the first 12 characters | Keep the full id from the start output |
| `poll` on Apollo | Hits the 1-hour timeout and exits 1 when a run takes longer than the usual 15 to 30 minutes | Webhook, or `status` every few minutes |
| Validating `email-find` output again, or leaving the sender's import verification on | Email Finder results are validated when found; a second pass pays twice for the same answer | Skip validation on fresh `email-find` results; validate addresses from outside ScraperCity and any whose last check is older than the re-check window you set; `verify_leads_on_import: false` on the sender |
| Scripting a push command that does not exist | The CLI has no sender or CRM push in 1.0.17 | Filter valid rows, then `curl` the sender API in batches (`references/scripting-patterns.md` section 7b) |

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/command-reference.md` | You need a command's syntax, flags, defaults, API mapping, price or printed output. |
| `references/scripting-patterns.md` | Writing a loop, a poll-and-download, a cron job, a CSV pipe, a sender handoff or a CI workflow. |
| `references/gaps-and-quirks.md` | A command or flag is missing, or a flag combination behaves oddly in 1.0.17. |
| `templates/output-template.md` | Start every CLI run spec from it. |
| `examples/worked-example.md` | A finished spec (weekday VP Sales and Texas dentist feed with validation) to copy. |
| `scripts/check-output.py` | Before handing over a spec: `python3 scripts/check-output.py spec.md`. |
| `references/scrapercity-catalog.md` | Prices, endpoints and input schemas. |
| `references/scrapercity-platform.md` | Plans and database allowances. |
| `references/scrapercity-agent-patterns.md` | Wallet, count, approval, polling and retry rules. |

## Related Skills

- `using-scrapercity-skills`: router for every ScraperCity job.
- `scrapercity-mcp`: the same package as an MCP server inside AI clients.
- `scrapercity-api` and `scrapercity-integrations`: REST and no-code paths, including endpoints the CLI lacks.
- `scrapercity-lead-database` and `scrapercity-local-business-database`: filter design for `db-leads` and `db-local`.
- `email-list-cleaner` and `cold-email-list`: what happens to the files next.
