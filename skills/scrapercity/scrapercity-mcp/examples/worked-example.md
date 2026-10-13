# ScraperCity MCP Setup and Run Report: HVAC contractors in Phoenix, AZ

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Scenario: Sam runs a small HVAC marketing agency on the Starter plan and works in Claude Code on a MacBook. He wants HVAC contractors in Phoenix with checked emails in a CSV in `~/Leads`, and he wants ScraperCity available in every project.

## Client Setup

| Item | Value |
|---|---|
| Client | Claude Code 2.x on macOS |
| OS | macOS 15, Node v22.11.0 |
| Scope | user (stored in `~/.claude.json`, loads in every project) |
| Config file | `~/.claude.json` |
| Command | npx |
| Args | -y --package scrapercity scrapercity-mcp |
| Key handling | Masked: added with `--env SCRAPERCITY_API_KEY=****8f2a`; a dedicated key named "claude-code-sam" |
| Version | Unpinned (npm latest was 1.0.17 on 2026-10-13) |

```json
{
  "scrapercity": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
    "env": { "SCRAPERCITY_API_KEY": "****8f2a" }
  }
}
```

Install command used (key masked here):

```bash
claude mcp add --env SCRAPERCITY_API_KEY=****8f2a --transport stdio --scope user \
  scrapercity -- npx -y --package scrapercity scrapercity-mcp
```

## Verification

| Check | Result |
|---|---|
| Tools listed | 25 tools under `scrapercity` in `/mcp`; `claude mcp list` shows Connected |
| check_wallet call | Succeeded: plan Starter, total_balance_dollars 46.20 |
| Duplicate or old ScraperCity entries | None. One earlier entry from a teammate's snippet removed (see Issues) |
| Current tool set (scrape_distress_list present, after and excludeDelivered on query_lead_database) | Yes, both present |

## Wallet Check

| Item | Value |
|---|---|
| Plan | Starter ($49/mo, $49 monthly credit) |
| Balance | $46.20 |
| Renews | 2026-11-01 |
| Database access | No. Lead Database and Local Business Database need Growth ($149/mo) |

## Run Plan

Every tool must exist in `references/scrapercity-catalog.md`. Units are the billable ceiling. A `scrape_apollo` row names its webhook.

| Step | Tool | Key parameters | Units | Unit price | Cost |
|---|---|---|---:|---:|---:|
| 1 | scrape_maps | searchStringsArray ["hvac contractor"], locationQuery "Phoenix, AZ", maxCrawledPlacesPerSearch 400 | 400 | $0.0099 | $3.96 |
| 2 | validate_emails | Unique emails from the step 1 CSV (estimate 70% of 400 businesses carry one) | 280 | $0.0072 | $2.02 |
| Total | | | | | $5.98 |

Approval: Total ceiling $5.98 is over the $5 line and 13% of the $46.20 balance. Shown to Sam, approved in chat ("go ahead") before step 1.

Polling plan: step 1 first check after 2 minutes, then one check per turn; step 2 first check after 30 seconds. No status calls chained in one turn.

## Run Log

| runId | Tool | Status | Rows | File |
|---|---|---|---:|---|
| 7f3a91c2-5b0e-4d7a-9c11-2e8f6a4b3d90 | scrape_maps | SUCCEEDED | 372 | /Users/sam/Leads/maps-hvac-contractor-phoenix-az-20261013-7f3a91c2.csv |
| c41d0e88-2a6f-4b19-8e3d-91f7b0c5a2e4 | validate_emails | SUCCEEDED | 251 | /Users/sam/Leads/validated-hvac-contractor-phoenix-az-20261013-c41d0e88.csv |

Actual spend: 372 businesses x $0.0099 = $3.68, plus 251 emails x $0.0072 = $1.81, total $5.49. Balance after: $40.71.

The `scrape_maps` start response carried a `local_business_database` block with 1,180 matches for the same search. On Growth those rows come from `query_local_business_database` at $0 wallet cost, which left Sam with a pricing question for next month (see Next Steps).

## Issues and Fixes

| Symptom | Cause | Fix |
|---|---|---|
| First install showed `Failed to connect`; server output had `npm error 404 'scrapercity-mcp@*' is not in this registry` | A teammate's snippet ran `npx -y scrapercity-mcp` without `--package` | `claude mcp remove scrapercity`, then added again with `-y --package scrapercity scrapercity-mcp` |
| Every tool returned `Error: No API key` on the second try | The key was exported in `~/.zshrc` after the session started, and the entry had no `--env` | Re-added with `--env SCRAPERCITY_API_KEY=...`, started a new session, `check_wallet` succeeded |
| Agent proposed checking the maps run status every 15 seconds | Default loop habit from the CLI `poll` command | Applied the agent rule: one `check_run_status` per turn; the run reported 210 / 400 on the first check and SUCCEEDED on the second |

## Next Steps

1. Load the 251 validated rows (status valid only) into Sam's sequencer; handle the catch-all rows with `email-list-cleaner` rules before sending.
2. For the next city, compare costs: on Starter each 400-business city costs up to $3.96 plus validation; on Growth ($149/mo) the 1,180 database matches cost $0 and only validation is paid.
3. Pin `scrapercity@1.0.17` in the shared team `.mcp.json` with `${SCRAPERCITY_API_KEY}` so teammates get the same tool set without committing a key.
