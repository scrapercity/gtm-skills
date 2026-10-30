# ScraperCity MCP Setup and Run Report: HVAC contractors in Phoenix, AZ

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Scenario: Sam runs a small HVAC marketing agency on the Starter plan and works in Claude Code on a MacBook. He wants HVAC contractors in Phoenix with checked emails in a CSV in `~/Leads`, and he wants ScraperCity available in every project.

## Answer

- 229 Phoenix HVAC contractors with a `valid` email are in `/Users/sam/Leads/validated-hvac-contractor-phoenix-az-20261013-c41d0e88.csv`.
- Spent $4.10 of the $46.20 wallet (372 businesses from Google Maps, 251 emails validated); $42.10 left.
- Starter has no database access, so the rows came from a Maps scrape. The same search has 1,180 matches in the Local Business Database, which Growth returns at $0.

## Client Setup

| Item | Value |
|---|---|
| Client | Claude Code 2.x on macOS 15, Node v22.11.0 |
| Scope | user (stored in `~/.claude.json`, loads in every project) |
| Args | -y --package scrapercity scrapercity-mcp |
| Key handling | A dedicated key named "claude-code-sam", passed with `--env`; masked here as ****8f2a |
| Version | Unpinned (npm latest was 1.0.17 on 2026-10-13) |

Install command used:

```bash
claude mcp add --env SCRAPERCITY_API_KEY=****8f2a --transport stdio --scope user \
  scrapercity -- npx -y --package scrapercity scrapercity-mcp
claude mcp list   # showed: scrapercity ... Connected
```

## Verification

| Check | Result |
|---|---|
| Tools listed | 25 tools under `scrapercity` in `/mcp` |
| check_wallet call | Succeeded: plan Starter ($49/mo), balance $46.20, renews 2026-11-01 |

## Agent Rules

Written to `~/.claude/settings.json`. The three free reads run without a prompt; every scrape_*, find_*, validation, database and download call asks first.

```json
{
  "permissions": {
    "allow": [
      "mcp__scrapercity__check_wallet",
      "mcp__scrapercity__list_runs",
      "mcp__scrapercity__check_run_status"
    ],
    "ask": [
      "mcp__scrapercity__scrape_*",
      "mcp__scrapercity__find_*",
      "mcp__scrapercity__validate_emails",
      "mcp__scrapercity__search_criminal_records",
      "mcp__scrapercity__query_lead_database",
      "mcp__scrapercity__query_local_business_database",
      "mcp__scrapercity__download_results",
      "mcp__scrapercity__cancel_run"
    ]
  }
}
```

Agent tests run after setup:

| Agent test | Result | Note |
|---|---|---|
| Wallet first | Pass | Asked for "HVAC contractors in Phoenix", the agent called check_wallet, priced 400 places plus validation, and waited |
| Miss handling | Pass | find_emails on one invented contact at `desertairhvac.example` returned no email; the agent said "not found, no charge" and wrote no address |
| Duplicate start | Pass | A repeat of the same validate_emails start inside 2 minutes got 409; the agent called list_runs (hours 1) and reused c41d0e88 |

## Run Plan

**Call 1: scrape Google Maps**

```json
{"tool": "scrape_maps", "arguments": {"searchStringsArray": ["hvac contractor"], "locationQuery": "Phoenix, AZ", "maxCrawledPlacesPerSearch": 400}}
```

**Call 2: validate every email from call 1 in one run.** Claude read the `email` column of the call 1 CSV, lowercased and deduplicated it, and passed the list:

```json
{"tool": "validate_emails", "arguments": {"emails": ["service@desertairhvac.example", "office@valleycoolaz.example", "info@sonoranheating.example"]}}
```

(The real call carried all 251 unique addresses; three are shown.)

**Calls 3 and 4: status once per turn, then download to an absolute path.**

```json
{"tool": "check_run_status", "arguments": {"runId": "c41d0e88-2a6f-4b19-8e3d-91f7b0c5a2e4"}}
{"tool": "download_results", "arguments": {"runId": "c41d0e88-2a6f-4b19-8e3d-91f7b0c5a2e4", "outputPath": "/Users/sam/Leads/validated-hvac-contractor-phoenix-az-20261013-c41d0e88.csv"}}
```

| Step | Tool | Key parameters | Units | Unit price | Cost |
|---|---|---|---:|---:|---:|
| 1 | scrape_maps | searchStringsArray ["hvac contractor"], locationQuery "Phoenix, AZ", maxCrawledPlacesPerSearch 400 | 400 | $0.0099 | $3.96 |
| 2 | validate_emails | Unique emails from the step 1 CSV, ceiling of one per business | 400 | $0.00169 | $0.68 |
| Total | | | | | $4.64 |

Approval: Ceiling $4.64, 10% of the $46.20 balance. Shown to Sam, approved in chat ("go ahead") before step 1.

## Run Log

| runId | Tool | Status | Rows | File |
|---|---|---|---:|---|
| 7f3a91c2-5b0e-4d7a-9c11-2e8f6a4b3d90 | scrape_maps | SUCCEEDED | 372 | /Users/sam/Leads/maps-hvac-contractor-phoenix-az-20261013-7f3a91c2.csv |
| c41d0e88-2a6f-4b19-8e3d-91f7b0c5a2e4 | validate_emails | SUCCEEDED | 251 | /Users/sam/Leads/validated-hvac-contractor-phoenix-az-20261013-c41d0e88.csv |

Actual spend: 372 x $0.0099 = $3.68, plus 251 x $0.00169 = $0.42, total $4.10. Validation: 229 valid, 17 catch-all, 5 unknown, 0 invalid.

## Issues and Fixes

| Symptom | Cause | Fix |
|---|---|---|
| First install showed `Failed to connect`; server output had `npm error 404 'scrapercity-mcp@*' is not in this registry` | A teammate's snippet ran `npx -y scrapercity-mcp` without `--package` | `claude mcp remove scrapercity`, then added again with `-y --package scrapercity scrapercity-mcp` |
| Every tool returned `Error: No API key` on the second try | The key was exported in `~/.zshrc` after the session started, and the entry had no `--env` | Re-added with `--env SCRAPERCITY_API_KEY=...`, started a new session, `check_wallet` succeeded |
| Agent proposed checking the maps run status every 15 seconds | Habit from the CLI `poll` command | One `check_run_status` per turn; the run showed 210 / 400 on the first check and SUCCEEDED on the second |

## Next Steps

1. Load the 229 valid rows into Sam's sequencer. The 17 catch-all rows go to a separate campaign; the 5 unknown rows are re-checked once before they are sent.
2. Next city: on Starter, up to $3.96 per 400-business scrape plus validation; on Growth ($149/mo) the 1,180 database matches cost $0 and only validation is paid.
3. For teammates, commit this `.mcp.json` at the repo root. It pins the release so everyone gets the same 25 tools, and each person's key comes from their own shell:

```json
{
  "mcpServers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity@1.0.17", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "${SCRAPERCITY_API_KEY}" }
    }
  }
}
```
