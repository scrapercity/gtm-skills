# Troubleshooting Runbook: ScraperCity MCP

Work top to bottom. Each block gives the symptom, the check, and the fix. Behavior notes come from running `scrapercity` 1.0.17 locally on 2026-10-13 and from each client's documentation.

## Triage order

| # | Check | Command or action | Pass looks like |
|---|---|---|---|
| 1 | Node 18 or newer | `node --version` | `v18` or higher |
| 2 | The server starts by hand | `SCRAPERCITY_API_KEY=YOUR_SCRAPERCITY_API_KEY npx -y --package scrapercity scrapercity-mcp` | No output, process waits for input (stdio). Ctrl+C to exit |
| 3 | The client sees it | Claude Code `claude mcp list`; Desktop connectors list; Cursor Customize; VS Code "MCP: List Servers"; Gemini `/mcp`; Zed status dot in Settings, AI, MCP Servers; Hermes `hermes mcp test scrapercity` | `scrapercity` connected, 25 tools |
| 4 | The key reaches it | Ask the agent to call `check_wallet` | JSON with `plan.name` |
| 5 | Only one ScraperCity entry | Look at the full tool list | One `scrapercity` set, no "ScraperCity - B2B Lead Generation" |
| 6 | Current tool set | `scrape_distress_list` present; `query_lead_database` has `after` and `excludeDelivered` | Both true |

## Key missing

**Symptom.** Every tool returns `Error: No API key. Run: scrapercity login  OR  export SCRAPERCITY_API_KEY=...`

The server starts and lists its tools without a key; the key is only read when a tool runs. It looks in `SCRAPERCITY_API_KEY` first, then in `~/.scrapercityrc` (written by `npx scrapercity login`).

| Cause | Fix |
|---|---|
| No `env` block, or the key was set in a terminal profile the desktop app never reads | Put `"env": { "SCRAPERCITY_API_KEY": "..." }` in the server entry |
| Typo in the variable name (`SCRAPER_CITY_API_KEY`, `SCRAPERCITY_KEY`) | Use exactly `SCRAPERCITY_API_KEY` |
| Gemini CLI redacted it | List it in the server's `env` block; inherited `*KEY*` variables are redacted |
| `${env:...}` or `${VAR}` points at a variable that is not set | Cursor and Windsurf resolve an unset variable to an empty string. Set it, or put the key in `env` |
| VS Code input never answered | Restart the server from "MCP: List Servers" and answer the prompt |

## Key rejected (401)

| Cause | Fix |
|---|---|
| Quotes or spaces pasted into the key | The value inside `"..."` must be the bare key |
| Key revoked or regenerated in the dashboard | Copy a fresh key from app.scrapercity.com/dashboard/api-docs |
| An old key in the environment beats a new one in `~/.scrapercityrc` | The environment variable wins. Update or remove the old one |

## Tool not showing

| Cause | How to tell | Fix |
|---|---|---|
| Client not fully restarted | Config edited but tool list unchanged | Quit from the app menu and reopen |
| JSON syntax error | The client skips the file, so other servers in it vanish too | Validate with `python3 -m json.tool < file.json`; watch for trailing commas and a second `mcpServers` key |
| Wrong file | Server never appears | Open the file from the client's own menu (see `references/client-setup.md`) |
| `npx scrapercity-mcp` without `--package` | Log shows `npm error 404 ... 'scrapercity-mcp@*' is not in this registry` | `"args": ["-y", "--package", "scrapercity", "scrapercity-mcp"]` |
| npx not found by a desktop app | Log shows `spawn npx ENOENT` | Use the absolute path from `which npx` as `command` |
| Windows `${APPDATA}` ENOENT | Log names `${APPDATA}` in a path | Add the expanded `APPDATA` path to `env`; install npm globally |
| Claude Code project server not approved | `claude mcp list` shows pending approval | Start `claude` in that folder and approve |
| Gemini CLI untrusted folder | `gemini mcp list` shows Disconnected | `gemini trust` in that folder |
| Cursor server toggled off | Greyed out under Customize | Toggle on |
| Windsurf 100-tool cap | Some ScraperCity tools missing when many servers are on | Turn off unused servers |
| VS Code cached tool list | Old tools after an update | "MCP: Reset Cached Tools" |

Log locations: Claude Desktop `~/Library/Logs/Claude/mcp*.log` (macOS) or `%APPDATA%\Claude\logs` (Windows); VS Code "MCP: List Servers", pick the server, Show Output; Claude Code `claude mcp get scrapercity` and `/mcp`.

## Stale version

**Symptom.** A tool the docs mention is missing, a tool description quotes an old plan price, or `query_lead_database` has no `after` or `excludeDelivered`.

The config runs `npx -y --package scrapercity` with no version, so the next start should fetch the newest release. npx caches packages, and a client that never restarted keeps the old process.

1. Quit the client completely and reopen it. Usually that is enough.
2. Still stale: delete the npx cache and reopen.
   - macOS and Linux: `rm -rf ~/.npm/_npx`
   - Windows (PowerShell): `Remove-Item -Recurse -Force "$env:LocalAppData\npm-cache\_npx"`
3. VS Code: also run "MCP: Reset Cached Tools".
4. Confirm the release you expect with `npm view scrapercity version`.

The server's own handshake reports a fixed version string, so check the tool list instead of the handshake to confirm what is running. Deleting `_npx` only removes cached npx installs; the next start downloads the package again.

## Two ScraperCity tool sets

**Symptom.** The client shows `scrapercity` and also "ScraperCity - B2B Lead Generation" (tool names prefixed `ScraperCity_-_B2B_Lead_Generation`). Answers disagree between the two.

The second entry is an old ScraperCity desktop extension installed separately from the npm config. It is frozen at an early release, and nothing published to npm updates it. Signs you are looking at it: its database tool description quotes a $649/mo plan requirement (the databases are included from the $149/mo Growth plan), its `query_lead_database` has no `after` or `excludeDelivered`, it lists tools that are not in the current catalog, and it has no `scrape_distress_list`.

Fix:

1. Claude Desktop: Settings, Extensions (or Connectors), find "ScraperCity - B2B Lead Generation", remove it.
2. Keep the `scrapercity` entry in `claude_desktop_config.json`.
3. Quit and reopen. Confirm one tool set of 25.
4. Never treat the old extension's descriptions or prices as current. The catalog in `references/scrapercity-catalog.md` is the reference.

## Errors from tools

The text of a failed call is `Error: ` plus the server's message. The HTTP code may not be in the text.

| Message is about | Code | Agent action | Retry |
|---|---|---|---|
| Missing or invalid key | 401 | Stop, fix config | No |
| Balance too low | 402 | `check_wallet`, report shortfall, offer a smaller run | After top-up |
| Account cancelled, charge processing | 403 | Stop, tell the user | No |
| Duplicate submission | 409 | `list_runs` `hours: 1`, reuse `runId` | No, reuse |
| `filters_not_applied_yet` | 409 | Drop listed company filters | Later |
| Rate limited, or repeat within about 30 s | 429 | Wait 30 s or more, retry once | Once |
| Unavailable or search took too long | 503 | Database: add location, size band, fewer titles. Scraper: retry later | After narrowing |
| `Download failed: HTTP ...` | varies | Check status is SUCCEEDED; results are kept 48 hours | After SUCCEEDED |
| Bad input (400), for example a Crexi map view with no city | 400 | Fix the input named in the message | After fixing |

Never loop-poll. One `check_run_status` per turn, then report `handled / requested` and stop.

## Output problems

| Symptom | Fix |
|---|---|
| CSV saved somewhere the user cannot find | Pass an absolute `outputPath` in a folder the user named |
| `download_results` write error | The folder does not exist or is not writable. Create it or choose another |
| Claude Code warns that a result is large, or truncates it | Lower `limit` for inspection; move bulk pulls to `scrapercity-cli` or `scrapercity-api`; raise `MAX_MCP_OUTPUT_TOKENS` only if needed |
| The agent reads 100 database rows into chat to "export" them | Write the file with a REST loop (`scrapercity-api`) or a script (`scrapercity-cli`) and keep chat for counts and samples |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/mcp
- https://scrapercity.com/api-docs
- https://modelcontextprotocol.io/docs/develop/connect-local-servers
- https://code.claude.com/docs/en/mcp
- https://cursor.com/docs/context/mcp
- https://docs.devin.ai/desktop/cascade/mcp
- https://geminicli.com/docs/tools/mcp-server/
- https://code.visualstudio.com/docs/copilot/reference/mcp-configuration
- https://docs.npmjs.com/cli/v10/commands/npx
- https://docs.npmjs.com/cli/v10/using-npm/config#cache
