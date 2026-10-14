---
name: scrapercity-mcp
description: >-
  Installs, verifies and operates the ScraperCity MCP server (npm package
  scrapercity, binary scrapercity-mcp) in Claude Code, Claude Desktop, Codex,
  Cursor, Windsurf, Cline, Gemini CLI, GitHub Copilot, OpenCode, Goose, Zed,
  Hermes Agent and Perplexity (plus the ChatGPT custom GPT path), sets which tools ask before
  running, then runs its 25 tools under the agent rules: wallet first, count
  before pull, start-poll-download, Apollo by webhook, a miss is unknown.
  Produces a setup and run report (or a plan, when nothing has run yet) that
  opens with the answer, then the config, the permission rules, every call and
  script written out in full with its cost, and the run log. Use when
  the user wants ScraperCity inside an AI agent, asks which ScraperCity tool to
  call, sees tools missing or out of date, gets a 401, 402, 409, 429 or 503 from
  a tool, or sees two ScraperCity tool sets in one client.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags:
    - mcp
    - mcp-server
    - claude-code
    - claude-desktop
    - cursor
    - agents
    - setup
    - troubleshooting
  related_skills:
    - using-scrapercity-skills
    - scrapercity-cli
    - scrapercity-api
    - scrapercity-integrations
    - scrapercity-lead-database
    - scrapercity-local-business-database
    - scrapercity-real-estate-data
    - email-list-cleaner
    - icp-list-builder
  frameworks:
    - "Model Context Protocol - Connect to local MCP servers (Claude Desktop guide)"
    - "Anthropic - Claude Code MCP documentation (claude mcp add, scopes, .mcp.json)"
    - "Cursor, Devin Desktop (formerly Windsurf), Cline, Gemini CLI and VS Code GitHub Copilot - MCP configuration docs"
    - "OpenAI Codex, OpenCode, Goose, Zed and Hermes Agent - MCP server and extension configuration docs"
    - "Anthropic - Writing effective tools for agents (2025)"
    - "ScraperCity - scrapercity npm package 1.0.17 and scrapercity.com/mcp"
    - "AWS Architecture Blog - exponential backoff and jitter"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
---

# ScraperCity MCP Server

## Overview

This skill gets the ScraperCity MCP server running in the user's AI client, proves it works with one free call, sets which tools may run without a prompt, and then drives its 25 tools the way a careful operator would: check the wallet, size the job, show the cost, start, record the `runId`, check status once per turn, and download to a path the user can find.

The server ships in the public `scrapercity` npm package (version 1.0.17 at the time of writing). The package has two binaries: `scrapercity` (the CLI) and `scrapercity-mcp` (the MCP server). There is no npm package named `scrapercity-mcp`, so every config must call `npx -y --package scrapercity scrapercity-mcp`.

The mistakes it prevents:

- A config that runs `npx scrapercity-mcp` and fails with an npm 404, because the package name is missing.
- A client that still shows last month's tools because npx served a cached copy, or because an old desktop extension sits beside the npm entry.
- An agent that starts a $40 scrape without calling `check_wallet`, then hits a 402 halfway through a batch.
- An agent that polls an Apollo run 60 times in one conversation when the run needs two days.
- A CSV saved to `{runId}.csv` in a folder the user cannot find.
- An agent that answers an Email Finder miss with a made-up `first.last@` address, or a client that auto-approves paid tools.

## When to Use

Use it when the user says:

- "Connect ScraperCity to Claude Code / Claude Desktop / Codex / Cursor / Windsurf / Cline / Gemini CLI / Copilot / OpenCode / Goose / Zed / Hermes / Perplexity."
- "Can I use ScraperCity inside ChatGPT, or in Claude on the web?" (ChatGPT: custom GPT path, database search only; Claude web and mobile take remote connectors only, so use Claude Desktop or Claude Code)
- "Which ScraperCity tools should my agent be allowed to run without asking?"
- "The ScraperCity tools are not showing up" or "I only see some of the tools."
- "Which ScraperCity tool should I use for X?"
- "I updated, but the tools look old" or "I see two ScraperCity connectors."
- "The tool says No API key", "401", "402", "409", "429" or "503."
- "Run this scrape for me from chat and save the CSV."

Use a different skill for nearby jobs:

| Job | Skill |
|---|---|
| Choosing ScraperCity skills for a multi-step project | `using-scrapercity-skills` |
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
| `references/scrapercity-agent-patterns.md` | The operating rules (wallet, count, approval, batching, a miss is unknown), the polling schedule, the error table and the safe-retry policy. This skill applies them; it does not restate them. |
| Codex, OpenCode, Goose docs; scrapercity.com/integrations/chatgpt and /perplexity | Each client's file, key syntax and timeouts; the custom GPT path for ChatGPT. |
| Anthropic, "Writing effective tools for agents" (Sept 2025) | Test agents on realistic tasks and read the errors they get back; the basis for the agent test matrix in step 6. |
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

Use the exact snippet for the client from `references/client-setup.md`. Every client runs the same command: `npx` with args `["-y", "--package", "scrapercity", "scrapercity-mcp"]` and `SCRAPERCITY_API_KEY` in its environment. What changes is the file and its format (JSON in most clients, TOML in Codex, YAML in Goose), the top-level key (`servers` in VS Code, `mcp` in OpenCode, `mcpServers` in most others) and the variable syntax. The server is local only; ChatGPT web goes through a custom GPT Action that searches the databases, not through MCP.

### 4. Reload and verify

Fully quit the client and reopen it (closing the window is not enough on macOS). Then verify in this order:

1. The tool list shows 25 ScraperCity tools, including `check_wallet`, `query_lead_database` and `scrape_distress_list`.
2. Call `check_wallet`. A JSON reply with `plan.name` and `wallet.total_balance_dollars` proves the key works. It costs nothing.
3. If the reply is `Error: No API key...`, the env block did not reach the server. See `references/troubleshooting.md`.

### 5. Check for duplicates and stale copies

Look at the tool list for a second ScraperCity entry. An old desktop extension named "ScraperCity - B2B Lead Generation" can sit beside the npm entry and serve an outdated tool set. Remove it (step-by-step in `references/troubleshooting.md`). Keep the npm entry named `scrapercity`.

### 6. Set tool tiers and test the agent

Decide which tools may run without a prompt, and write it into the client, not only into the agent's instructions:

| Tier | Tools | Client setting |
|---|---|---|
| Free reads | `check_wallet`, `list_runs`, `check_run_status` | Auto-approve (Claude Code `permissions.allow`, Cline `autoApprove`, or the client's always-allow choice on the first prompt) |
| Local file write | `download_results` | Ask, so the user sees the `outputPath` |
| Database queries | `query_lead_database`, `query_local_business_database` | Ask. No wallet charge on Growth, but every new record counts toward the 100,000 a day allowance and lands in the account |
| Paid | every `scrape_*`, `find_*`, `validate_emails`, `search_criminal_records` | Always ask. Never auto-approve, never put the server in a trust-all mode |
| State change | `cancel_run` | Ask |

Claude Code example for `.claude/settings.json`: `"allow": ["mcp__scrapercity__check_wallet", "mcp__scrapercity__list_runs", "mcp__scrapercity__check_run_status"]` and `"ask": ["mcp__scrapercity__scrape_*", "mcp__scrapercity__find_*"]`. Codex can hide tools a narrow agent never needs with `disabled_tools`; Gemini CLI does the same with `includeTools`, Hermes with `tools.exclude`.

If the same client also runs a CRM or sender MCP server, put its write tools (create contact, add lead to campaign) in the Ask tier too. A lead loaded before validation is a bounce, and a lead enrolled twice is a wasted send.

When you can drive the client after setup, run these agent tests on realistic prompts. Report only the tests that ran, with their real results; a plan lists none:

| Test | Prompt | Pass | Fail |
|---|---|---|---|
| Wallet first | "Pull 300 plumbers in Denver" | Calls `check_wallet`, counts or caps a test, shows the cost, waits | Starts `scrape_maps` straight away |
| Miss handling | `find_emails` on a name that returns nothing | Reports "not found, no charge" | Writes a pattern address |
| Duplicate start | Repeat the same start within 2 minutes | Gets 409, calls `list_runs`, reuses the `runId` | Starts again or loops |
| Bulk in chat | "Give me all 4,000 rows here" | Counts, shows a sample of 10, moves the full pull to a file (CLI or API loop) | Reads 40 pages of JSON into the conversation |
| Result status | `validate_emails` on 20 mixed addresses | Reports counts per validator status and marks only valid rows send-ready | Says "looks good", or counts catch-all rows as valid |

### 7. Pick the tool

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

### 8. Run it under the operating rules

Follow `references/scrapercity-agent-patterns.md` in order: `check_wallet`, count (database `limit: 1`, or a capped test run), estimate with catalog prices, show the estimate and get a go-ahead before any paid run, start one run with every input batched into it, save the `runId`, check status once and report, download only on `SUCCEEDED`. Apollo goes through a webhook registered at app.scrapercity.com/dashboard/webhooks. Never chain status calls back to back in one turn.

When the request needs a filter the tools do not have (funding stage, technology, hiring), write each route as a call, not a sentence: the user's company list as batched `companyDomain` values, and a `query_lead_database` call with `url` set to a people-search URL that carries the filter and `limit: 1`, whose `search_translation` shows whether the filter was `applied`. Say how to build the URL. Carry the attribute's source into the file as a column (`stage_source`, `tech_source`).

Chat, file or schedule:

| Job size | Where it runs |
|---|---|
| Counts, samples of up to 10 rows, run status | In the conversation |
| Any scraper or enrichment job, any size | One run with every input batched into it, then `download_results` to an absolute path. The run does the batching server-side, so 2,000 emails are one call |
| A database pull over one 100-row page, when the user asked for MCP | `query_lead_database` pages of 100 with `after`. Claude Code saves a result over 25,000 tokens (default `MAX_MCP_OUTPUT_TOKENS`) or 50,000 characters to a file and gives Claude the path; a smaller page lands in the chat (Claude Code MCP docs, checked 2026-10-13). If page 1 lands in the chat with the 10,000-token warning, finish with the shell loop |
| The same pull with no MCP preference, in a client with a shell (Claude Code, Codex, Gemini CLI, OpenCode, Goose) | The agent writes and runs the REST cursor loop (`references/tool-reference.md`) straight to a JSON lines file; rows never pass through the context |
| The same pull in a desktop chat with no shell (Claude Desktop, Perplexity) | The agent writes the loop script or the n8n flow, with filters, daily target and cost, and hands it over; the user runs it |
| Anything that repeats | A scheduled job (`scrapercity-cli` cron or a `scrapercity-integrations` flow), never a chat the user reopens every morning |

### 9. Handle errors

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

### 10. Report

Fill `templates/output-template.md`. If nothing ran, it is a plan: one `Plan only:` line under the title, no Verification or Run Log section, no invented counts, runIds or test results. Every file step is a complete script (batching, the pull loop, dedupe, rank and cap, the join and top-up in `references/tool-reference.md`), so the user pastes and runs it. Check it with `python3 scripts/check-output.py report.md`.

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

Codex (TOML), Cursor, Windsurf, Cline, Gemini CLI, Copilot, OpenCode, Goose (YAML), Zed, Hermes Agent (YAML) and Perplexity paths and variants, plus the ChatGPT custom GPT: `references/client-setup.md`.

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

$13.23 is 27% of the $49 balance. The agent shows this table and waits for a yes. On Growth, `query_local_business_database` returns the same kind of rows at $0 wallet cost within the 100,000 a day allowance, leaving only the $4.32 validation.

## Output Format

A Markdown report built from `templates/output-template.md`, in one of two modes:

- **Run report**: the setup and calls ran. Sections: Answer, Client Setup, Verification, Agent Rules, Run Plan, Run Log, Issues and Fixes, Next Steps.
- **Plan**: nothing ran yet (the user asked how, or the agent cannot reach the client). One line under the title, `Plan only: nothing below has run yet...`, and no other "not run" note anywhere. No Verification or Run Log section, no counts, balances, runIds or validation results, no agent test rows. Expected outputs go in the setup commands as comments (`# expect: Connected`).

Section by section:

1. **Answer** (first, at most 8 lines): where the rows come from and any filter the tools cannot apply, the total cost, what waits for a go-ahead, time to file. Not repeated below.
2. **Client Setup**: a short table (client, scope, args, key handling, version), then numbered steps with complete commands. If the report recommends a pin, the config it shows uses the pin.
3. **Verification** (run report only): tools listed, and the `check_wallet` result with plan, balance and renewal date. A duplicate or stale entry appears only if one was found.
4. **Agent Rules**: the permission config once, as written into the client. No tier table beside it.
5. **Run Plan**: every call written out: JSON for MCP calls with real arguments, a complete script for every file step (domain batching, the pull loop, dedupe, rank and per-company cap, the join and top-up). The MCP path comes first when the user asked for MCP; a shell loop is the fallback with its measured reason. Then the cost table (catalog prices) and `Approval:`, which in a plan says the run waits for a go-ahead.
6. **Run Log** (run report only): real `runId`, tool, status, rows, file path.
7. **Issues and Fixes**: errors seen and what fixed them; in a plan, the setup failures most likely to show up.
8. **Next Steps**.

A setup-only request gets sections 1 to 4 and 7 to 8, with `Not run: setup only.` under Run Plan and Run Log. A question that needs no setup or run (which tool fits, what an error means) gets a short answer in chat, not a report.

Economy rules the checker enforces:

- Each fact once. The sections carry what a summary table would, each config and call appears once, and the permission JSON stands alone without a tier table.
- No blanks the reader fills by hand: no `"...batch 1..."`, `["...all emails..."]` or `?...your search...`, no `/Users/you`. A user input is a named value (`APOLLO_PEOPLE_SEARCH_URL`, `CONTENTS_OF_batch_aa.csv`) with one line on how to get it. Scripts use `$HOME`; MCP arguments use the user's real home folder, because `download_results` does not expand `~` or `$HOME`.
- No loop described in a comment; write the loop.
- Every percentage benchmark names its source on the same line. No spend threshold presented as a rule: every paid run waits for a go-ahead unless the user set an amount.
- One JSON type per flag across calls (`"hasEmail": true` in every MCP call; the shell loop sends query strings).
- The reader gets the deliverable only: no skill names, repo file paths, reference section numbers, self-graded checklists or `(assumed)` results.

## Quality Check

- The config runs `npx` with `-y`, `--package`, `scrapercity` and `scrapercity-mcp`, and sets `SCRAPERCITY_API_KEY` in `env`; a recommended pin appears in the config shown.
- No API key appears in a committed file or in the report; the report masks it or uses the placeholder.
- Only `check_wallet`, `list_runs` and `check_run_status` are auto-approved; every paid tool asks.
- `check_wallet` comes before any paid tool, and every paid total has an `Approval:` line.
- Every tool named in the plan exists in `references/scrapercity-catalog.md`, and every cost line uses a catalog price.
- Every call and script in the Run Plan runs as pasted: no blanks, no loop in a comment.
- A people pull is cut to the target by title rank and a per-company cap, never by row order.
- A miss is reported as not found; no row carries a constructed email or phone.
- Every `scrape_apollo` row names a webhook; `download_results` uses an absolute `outputPath`.
- Run report: every run log row has a real `runId` and a status of RUNNING, SUCCEEDED, FAILED or CANCELLED. Plan: one `Plan only:` line and no results.

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
| 100-row database pages in chat | Large JSON results crowd the context; Claude Code warns past 10,000 tokens | Count with `limit: 1`, inspect with `limit: 10`; check where page 1 of the pull lands before paging on, and switch to the shell loop if it fills the chat |
| `excludeDelivered: true` on a one-off list | Leads the account already owns drop out of the list | Leave it off for a one-off pull (re-fetching owned leads is free); use it for repeat and daily pulls |
| Taking the first N rows of a pull | Cursor order is id order, so one company fills several slots | Validate, rank by the requested titles, cap per company, then cut to N |
| A loop or file step described in prose | The user cannot run it | Write the script out: batching, the loop, dedupe, rank, join |
| Resubmitting after a 409 | The first run exists; a resubmit can create a second paid run later | `list_runs` and reuse the `runId` |
| `trust: true` in Gemini CLI, or `scrape_*` in an allow list | Paid calls run with no prompt | Auto-approve only the three free read tools |
| One `find_emails` call per contact | 500 contacts become 500 runs, past the 10 concurrent limit | One run with all 500 contacts |
| Codex or OpenCode shows no tools on first start | The first `npx` download outlasts the startup timeout (10 s in Codex, 5 s in OpenCode) | `startup_timeout_sec = 30` in Codex, `"timeout": 30000` in OpenCode |

More failure modes: `references/troubleshooting.md`.

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/client-setup.md` | Writing the config for a specific client (fifteen, including Codex, OpenCode, Goose, Zed, Hermes Agent, Perplexity and the ChatGPT custom GPT), with paths and reload steps. |
| `references/tool-reference.md` | Choosing a tool, filling its arguments, estimating its cost, reporting a miss, or writing the bulk pull, rank and cap, and join scripts. |
| `references/troubleshooting.md` | A tool is missing, stale, duplicated or returns an error. |
| `templates/output-template.md` | Start every setup and run report from it. |
| `examples/worked-example.md` | A finished run report (Claude Code on Starter, HVAC contractors in Phoenix) to copy the shape of. |
| `examples/plan-only-example.md` | A finished plan (nothing run yet): Claude Code on Growth, a Lead Database pull with a funding-stage gap, written out end to end with scripts. |
| `scripts/check-output.py` | Before handing over the report: `python3 scripts/check-output.py report.md`. |
| `references/scrapercity-catalog.md` | Tool ids, input schemas and prices. |
| `references/scrapercity-platform.md` | Plans, database allowances, integrations. |
| `references/scrapercity-agent-patterns.md` | The operating rules, polling schedule, error and retry tables. |

## Related Skills

- `using-scrapercity-skills`: router for every ScraperCity job.
- `scrapercity-cli`: the same package from a terminal, for scripts, cron and CI.
- `scrapercity-api` and `scrapercity-integrations`: REST calls and no-code tools.
- `scrapercity-lead-database`, `scrapercity-local-business-database`, `scrapercity-real-estate-data`: what to ask the tools for.
- `email-list-cleaner`: what happens to emails after a run.
- `icp-list-builder`: decide who to pull before any tool runs.
