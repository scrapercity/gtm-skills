---
name: scrapercity-mcp
description: >-
  Installs, verifies and operates the ScraperCity MCP server (npm package
  scrapercity, binary scrapercity-mcp) in Claude Code, Claude Desktop, Cursor,
  Windsurf, Cline, Gemini CLI and GitHub Copilot, then runs its 25 tools under
  the agent rules: wallet first, count before pull, start-poll-download, Apollo
  by webhook. Produces a setup and run report with the config used, a
  verification check, the wallet check, a cost estimate and a run log. Use when
  the user wants ScraperCity inside an AI agent, asks which ScraperCity tool to
  call, sees tools missing or out of date, gets a 401, 402, 409, 429 or 503 from
  a tool, or sees two ScraperCity tool sets in one client.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags: [mcp, mcp-server, claude-code, claude-desktop, cursor, agents, setup, troubleshooting]
  related_skills: [using-scrapercity-skills, scrapercity-cli, scrapercity-api, scrapercity-integrations, scrapercity-lead-database, scrapercity-local-business-database, scrapercity-real-estate-data, email-list-cleaner, icp-list-builder]
  frameworks:
    - "Model Context Protocol - Connect to local MCP servers (Claude Desktop guide)"
    - "Anthropic - Claude Code MCP documentation (claude mcp add, scopes, .mcp.json)"
    - "Cursor, Devin Desktop (formerly Windsurf), Cline, Gemini CLI and VS Code GitHub Copilot - MCP configuration docs"
    - "ScraperCity - scrapercity npm package 1.0.17 and scrapercity.com/mcp"
    - "AWS Architecture Blog - exponential backoff and jitter"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md]
---

# ScraperCity MCP Server

## Overview

This skill gets the ScraperCity MCP server running in the user's AI client, proves it works with one free call, and then drives its 25 tools the way a careful operator would: check the wallet, size the job, show the cost, start, record the `runId`, check status once per turn, and download to a path the user can find.

The server ships in the public `scrapercity` npm package (version 1.0.17 at the time of writing). The package has two binaries: `scrapercity` (the CLI) and `scrapercity-mcp` (the MCP server). There is no npm package named `scrapercity-mcp`, so every config must call `npx -y --package scrapercity scrapercity-mcp`.

The mistakes it prevents:

- A config that runs `npx scrapercity-mcp` and fails with an npm 404, because the package name is missing.
- A client that still shows last month's tools because npx served a cached copy, or because an old desktop extension sits beside the npm entry.
- An agent that starts a $40 scrape without calling `check_wallet`, then hits a 402 halfway through a batch.
- An agent that polls an Apollo run 60 times in one conversation when the run needs two days.
- A CSV saved to `{runId}.csv` in a folder the user cannot find.

## When to Use

Use it when the user says:

- "Connect ScraperCity to Claude Code / Claude Desktop / Cursor / Windsurf / Cline / Gemini CLI / Copilot."
- "The ScraperCity tools are not showing up" or "I only see some of the tools."
- "Which ScraperCity tool should I use for X?"
- "I updated, but the tools look old" or "I see two ScraperCity connectors."
- "The tool says No API key", "401", "402", "409", "429" or "503."
- "Run this scrape for me from chat and save the CSV."

Use a different skill for nearby jobs:

| Job | Skill |
|---|---|
| Choosing a ScraperCity skill for a whole project | `using-scrapercity-skills` |
| Terminal commands, shell scripts, cron, CI | `scrapercity-cli` |
| HTTP calls from code, Clay, n8n or Zapier | `scrapercity-api`, `scrapercity-integrations` |
| Filter design for B2B people | `scrapercity-lead-database` |
| Filter design for local businesses | `scrapercity-local-business-database` |
| Property, agent and distress data | `scrapercity-real-estate-data` |
| Cleaning the emails a run returned | `email-list-cleaner` |

## Prerequisites

- Node.js 18 or newer (`node --version`). The package declares `"node": ">=18"`.
- A ScraperCity API key from app.scrapercity.com/dashboard/api-docs. Use a separate key per agent so spend can be tracked and revoked on its own (scrapercity.com/mcp suggests a dedicated key for agent use).
- The client name, the OS, and whether the server should load in every project or one project only.
- For the Lead Database and Local Business Database tools: the Growth plan ($149/mo) or Scale. `check_wallet` shows `plan.name`.

## Authoritative Foundations

| Source | What it contributes here |
|---|---|
| `scrapercity` npm package 1.0.17 (`bin/mcp.mjs`, `lib/client.mjs`) | The 25 tool names, input schemas, the key lookup order (env var, then `~/.scrapercityrc`), the error text format and the `download_results` default path. Tested on 2026-10-13 by starting the server and calling `tools/list`. |
| `references/scrapercity-catalog.md` | Every tool id and per-result price. The only price source. |
| `references/scrapercity-agent-patterns.md` | The ten operating rules, the polling schedule, the error table and the safe-retry policy. This skill applies them; it does not restate them. |
| Model Context Protocol docs (modelcontextprotocol.io) | Claude Desktop config path, full quit and restart, log locations, the Windows `${APPDATA}` fix. |
| Claude Code docs (code.claude.com/docs/en/mcp) | `claude mcp add` option order, the `--` separator, scopes, `.mcp.json` env expansion, `claude mcp list`, `/mcp`, `MAX_MCP_OUTPUT_TOKENS`. |
| Cursor, Devin Desktop (Windsurf), Cline, Gemini CLI, VS Code docs | Each client's file path, JSON shape, variable syntax and reload method. |
| scrapercity.com/mcp | Same JSON for every client, only the path changes; fully quit and relaunch after install; duplicate protection on identical requests. |

Details and routing: `references/framework-notes.md`.

## Workflow

### 1. Check the machine

Run `node --version`. Under 18, stop and have the user install the Node LTS. Run `npx --version` to confirm npx is on the PATH. On macOS with a desktop client, note the output of `which npx`; a GUI app may not see the same PATH as the terminal.

### 2. Get the key and pick the scope

Ask for the key or confirm `SCRAPERCITY_API_KEY` is set. Decide the scope:

| Situation | Scope |
|---|---|
| One person, every project | User scope (Claude Code `--scope user`, Cursor `~/.cursor/mcp.json`, Gemini `~/.gemini/settings.json`) |
| A team repo where everyone has their own key | Project file with variable expansion, so no key is committed |
| A shared machine or demo | Local scope with a dedicated low-balance key |

### 3. Write the config

Use the exact snippet for the client from `references/client-setup.md`. Every client runs the same command: `npx` with args `["-y", "--package", "scrapercity", "scrapercity-mcp"]` and `SCRAPERCITY_API_KEY` in `env`. The only differences are the file path, the top-level key (`servers` in VS Code, `mcpServers` everywhere else) and the variable syntax.

### 4. Reload and verify

Fully quit the client and reopen it (closing the window is not enough on macOS). Then verify in this order:

1. The tool list shows 25 ScraperCity tools, including `check_wallet`, `query_lead_database` and `scrape_distress_list`.
2. Call `check_wallet`. A JSON reply with `plan.name` and `wallet.total_balance_dollars` proves the key works. It costs nothing.
3. If the reply is `Error: No API key...`, the env block did not reach the server. See `references/troubleshooting.md`.

### 5. Check for duplicates and stale copies

Look at the tool list for a second ScraperCity entry. An old desktop extension named "ScraperCity - B2B Lead Generation" can sit beside the npm entry and serve an outdated tool set. Remove it (step-by-step in `references/troubleshooting.md`). Keep the npm entry named `scrapercity`.

### 6. Pick the tool

Map the request to one tool with the decision table in `references/tool-reference.md`. Short form:

| The user has or wants | Tool |
|---|---|
| Balance, plan, renewal date | `check_wallet` |
| B2B people by title, industry, size, location (Growth plan) | `query_lead_database` |
| Local businesses by keyword and place (Growth plan) | `query_local_business_database` |
| An Apollo people-search URL on Starter, or filters the database cannot apply | `scrape_apollo` |
| Local businesses on Starter | `scrape_maps`, `scrape_yelp`, `scrape_angi` |
| Names plus domains, need emails | `find_emails` |
| Domains plus one job title, need the person | `scrape_website_finder` |
| A list of emails to clean | `validate_emails` |
| LinkedIn URLs or work emails, need mobiles | `find_mobiles` |
| Stores by platform, country, traffic | `scrape_store_leads` |
| Every site using one technology | `scrape_builtwith` (Tech Stack Search) |
| Real estate agents, properties, distressed homes, commercial listings | `scrape_zillow_agents`, `scrape_property_lookup`, `scrape_distress_list`, `scrape_crexi` |
| Businesses for sale, Airbnb hosts in Europe | `scrape_bizbuysell`, `scrape_airbnb` |
| A person's contact data from name, phone, email or address | `find_people` |
| Criminal record search on a named person | `search_criminal_records` |

### 7. Run it under the operating rules

Follow `references/scrapercity-agent-patterns.md` in order: `check_wallet`, count (database `limit: 1`, or a capped test run), estimate with catalog prices, get a go-ahead over $5, start, save the `runId`, check status once and report, download only on `SUCCEEDED`. Apollo goes through a webhook registered at app.scrapercity.com/dashboard/webhooks. Never chain status calls back to back in one turn.

### 8. Handle errors

Tool failures come back as text starting `Error:` followed by the server's message, with the call flagged as an error. The message may not include the HTTP number, so match on meaning:

| Message is about | Code | Do this |
|---|---|---|
| No API key / invalid key | 401 | Stop. Fix the env block, quit and reopen. |
| Balance too low | 402 | `check_wallet`, report the shortfall in dollars, offer a smaller run. |
| Account cancelled or charge processing | 403 | Stop and tell the user. |
| Same search submitted moments ago | 409 | `list_runs` with `hours: 1`, reuse that `runId`. Do not resubmit. |
| `filters_not_applied_yet` (Lead Database) | 409 | Drop the named company filters or retry later. |
| Rate limited | 429 | Wait at least 30 seconds, retry once. |
| Unavailable or search took too long | 503 | Database: narrow the search. Scraper: retry later. |

### 9. Report

Fill `templates/output-template.md`: setup, verification, wallet, run plan with cost, run log, issues fixed, next steps. Check it with `python3 scripts/check-output.py report.md`.

## ScraperCity Implementation

### Claude Code

```bash
claude mcp add --env SCRAPERCITY_API_KEY=YOUR_SCRAPERCITY_API_KEY --transport stdio --scope user \
  scrapercity -- npx -y --package scrapercity scrapercity-mcp
claude mcp list            # expect: scrapercity ... Connected
```

Options go before the server name and everything after `--` is the server command (Claude Code docs). Inside a session, `/mcp` shows status and offers Reconnect.

### Claude Desktop (and the JSON every other client reuses)

File: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows). Open it from the Claude menu: Settings, Developer, Edit Config.

```json
{
  "mcpServers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "YOUR_SCRAPERCITY_API_KEY" }
    }
  }
}
```

Cursor, Windsurf, Cline, Gemini CLI and Copilot paths and variants: `references/client-setup.md`.

### Call sequence for a database job (Growth plan)

```json
{"tool": "check_wallet", "arguments": {}}
{"tool": "query_local_business_database", "arguments": {"keyword": ["roofing contractor"], "location": ["Dallas TX", "Fort Worth TX"], "hasEmail": true, "limit": 1}}
{"tool": "query_local_business_database", "arguments": {"keyword": ["roofing contractor"], "location": ["Dallas TX", "Fort Worth TX"], "hasEmail": true, "limit": 100, "after": "0"}}
```

Read `pagination.total` from the `limit: 1` call, report it, then loop `after` on `pagination.next_after` until it is null.

### Call sequence for a scraper job

```json
{"tool": "check_wallet", "arguments": {}}
{"tool": "scrape_maps", "arguments": {"searchStringsArray": ["roofing contractor"], "locationQuery": "Dallas, TX", "maxCrawledPlacesPerSearch": 300}}
{"tool": "check_run_status", "arguments": {"runId": "RUN_ID_FROM_START"}}
{"tool": "download_results", "arguments": {"runId": "RUN_ID_FROM_START", "outputPath": "/Users/sam/Leads/maps-roofing-dallas-tx-20261013.csv"}}
```

If the `scrape_maps` start response includes `local_business_database` with `matches`, those businesses are already in the database. On Growth, pull them there first.

### Worked cost estimate

Request: roofing contractors in Dallas, Fort Worth and Austin with validated emails. Account on Starter with a $49 balance, so the database is not available.

| Step | Units (ceiling) | Unit price | Ceiling cost |
|---|---:|---:|---:|
| `scrape_maps`, 3 runs (one per city), `maxCrawledPlacesPerSearch: 300` | 900 businesses | $0.0099 | $8.91 |
| `validate_emails` on the emails returned (assume 600) | 600 emails | $0.0072 | $4.32 |
| **Total ceiling** | | | **$13.23** |

$13.23 is 27% of the $49 balance and over the $5 line, so the agent shows this table and waits for a yes. On Growth, `query_local_business_database` returns the same kind of rows at $0 wallet cost within the 100,000 a day allowance, leaving only the $4.32 validation.

## Output Format

A Markdown report built from `templates/output-template.md`:

1. **Client Setup**: client, OS, scope, config file path, the config with the key masked.
2. **Verification**: tool count seen, `check_wallet` result, duplicate or stale entries found.
3. **Wallet Check**: plan, balance, renewal date.
4. **Run Plan**: one row per tool call with parameters, billable units, unit price and cost, plus the approval line.
5. **Run Log**: `runId`, tool, status, rows, file path.
6. **Issues and Fixes**: each error seen and what fixed it.
7. **Next Steps**.

## Quality Check

- The config runs `npx` with `-y`, `--package`, `scrapercity` and `scrapercity-mcp`, and sets `SCRAPERCITY_API_KEY` in `env`.
- No API key appears in a committed file or in the report; the report masks it.
- `check_wallet` was called and succeeded before any paid tool.
- Every tool named in the plan exists in `references/scrapercity-catalog.md`.
- Every cost line uses a catalog price; a plan over $5 shows an approval line.
- Every `scrape_apollo` row names a webhook.
- Every run log row has a `runId` and a status of RUNNING, SUCCEEDED, FAILED or CANCELLED.
- `download_results` used an absolute `outputPath`.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| `"args": ["-y", "scrapercity-mcp"]` | npm looks for a package named `scrapercity-mcp`, which does not exist (404) | `["-y", "--package", "scrapercity", "scrapercity-mcp"]` |
| Closing the window instead of quitting | The client keeps the old server process and config | Quit from the menu (Cmd+Q on macOS), reopen |
| Tools still old after a new release | npx reuses its cached copy | Quit, delete `~/.npm/_npx`, reopen; or pin `scrapercity@1.0.17` |
| Two ScraperCity tool sets | An old desktop extension serves a frozen tool list | Remove "ScraperCity - B2B Lead Generation" in Claude Desktop Settings, Extensions |
| Key in a committed `.mcp.json` | Anyone with repo access can spend the wallet | `${SCRAPERCITY_API_KEY}` expansion, key in the shell |
| Gemini CLI without the key in `env` | Gemini CLI redacts inherited variables matching `*KEY*` | List `SCRAPERCITY_API_KEY` in the server's `env` block |
| Polling Apollo every minute | Apollo runs take hours to days; each poll burns a tool call | Webhook, or one check an hour at most |
| `download_results` without `outputPath` | Saves `{runId}.csv` in the server's working directory | Pass an absolute path in a folder the user named |
| 100-row database pages in chat | Large JSON results crowd the context; Claude Code warns past 10,000 tokens | Use `limit: 1` to count and `limit: 10` to inspect; bulk pulls go to the CLI or API |
| Resubmitting after a 409 | The first run exists; a resubmit can create a second paid run later | `list_runs` and reuse the `runId` |

More failure modes: `references/troubleshooting.md`.

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/client-setup.md` | Writing the config for a specific client, with paths and reload steps. |
| `references/tool-reference.md` | Choosing a tool, filling its arguments, or estimating its cost. |
| `references/troubleshooting.md` | A tool is missing, stale, duplicated or returns an error. |
| `templates/output-template.md` | Start every setup and run report from it. |
| `examples/worked-example.md` | A finished report (Claude Code on Starter, HVAC contractors in Phoenix) to copy the shape of. |
| `scripts/check-output.py` | Before handing over the report: `python3 scripts/check-output.py report.md`. |
| `references/scrapercity-catalog.md` | Tool ids, input schemas and prices. |
| `references/scrapercity-platform.md` | Plans, database allowances, integrations. |
| `references/scrapercity-agent-patterns.md` | The ten operating rules, polling schedule, error and retry tables. |

## Related Skills

- `using-scrapercity-skills`: router for every ScraperCity job.
- `scrapercity-cli`: the same package from a terminal, for scripts, cron and CI.
- `scrapercity-api` and `scrapercity-integrations`: REST calls and no-code tools.
- `scrapercity-lead-database`, `scrapercity-local-business-database`, `scrapercity-real-estate-data`: what to ask the tools for.
- `email-list-cleaner`: what happens to emails after a run.
- `icp-list-builder`: decide who to pull before any tool runs.
