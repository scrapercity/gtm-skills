# Framework Notes: scrapercity-mcp

Which sources shape this skill, what each one contributes, and which file to open for what.

## Sources and what they contribute

| Source | Type | What it contributes | Where it shows up |
|---|---|---|---|
| `scrapercity` npm package 1.0.17 (`bin/mcp.mjs`, `lib/client.mjs`, generated tool catalog) | Vendor code, primary | The 25 tool names and schemas, the `--package` requirement (the binary is `scrapercity-mcp`, the package is `scrapercity`), the key lookup order, the `Error:` text format, the `download_results` default of `{runId}.csv`, `list_runs` caps (168 hours, 100 runs) | SKILL.md steps 3-8, `references/tool-reference.md`, `references/troubleshooting.md` |
| `references/scrapercity-catalog.md` | Generated from the package | Every per-result price and input schema | Every cost line |
| `references/scrapercity-agent-patterns.md` | Shared house rules | Wallet first, count first, $5 approval line, start-poll-download, webhook for Apollo, polling cadence, error and retry tables, CSV naming | SKILL.md step 7, every run plan |
| `references/scrapercity-platform.md` | Vendor facts | Plans, database access from Growth ($149/mo), 100,000 new records a day, integrations list naming the seven MCP clients | Prerequisites, decision table |
| scrapercity.com/mcp | Vendor docs | Same JSON in every client, fully quit and relaunch, key from the dashboard, a separate key for agents, duplicate protection | Client setup, prerequisites |
| Model Context Protocol, "Connect to local MCP servers" | Protocol docs | Claude Desktop config path, Developer settings route, full restart, log files, Windows `${APPDATA}` fix | `references/client-setup.md`, troubleshooting |
| Anthropic, Claude Code MCP docs | Client docs | `claude mcp add` option order and `--`, scopes and where each is stored, `.mcp.json` `${VAR}` expansion, `claude mcp list/get/remove`, `/mcp`, output token warning and cap | Client setup, pitfalls |
| Cursor MCP docs | Client docs | `~/.cursor/mcp.json` and project file, `${env:NAME}`, `envFile`, Customize toggle, approval by default | Client setup |
| Devin Desktop (formerly Windsurf) Cascade MCP docs and FAQ | Client docs | Rename date, config path, `${env:VAR}`, 100-tool cap, toggles | Client setup, troubleshooting |
| Cline MCP docs | Client docs | `cline_mcp_settings.json` route, `disabled` and `autoApprove` | Client setup |
| Gemini CLI MCP docs | Client docs | `settings.json` scopes, `$VAR` expansion, redaction of `*KEY*` variables, `trust`, `includeTools`, folder trust | Client setup, pitfalls |
| VS Code GitHub Copilot MCP docs | Client docs | `servers` key, `type: stdio`, `inputs` with `password: true`, "MCP: List Servers", "MCP: Reset Cached Tools" | Client setup, stale-version fix |
| GitHub Copilot CLI docs | Client docs | `/mcp add`, `~/.copilot/mcp-config.json` | Client setup |
| npm docs (npx, config cache) | Tool docs | `--package` to run a binary from a differently named package, `-y` to skip the install prompt, npm cache location | Config args, cache clearing |
| AWS Architecture Blog, "Exponential Backoff and Jitter" | Engineering reference | Backoff with jitter for safe retries on 429 and 503 | Error handling (via agent patterns) |
| FTC (FCRA) and FCC (TCPA) | Regulators | Public-record and phone data limits | Compliance boundary in `references/tool-reference.md` |

## Routing table

| You need to | Open |
|---|---|
| Write the config for one client, with its path and reload steps | `references/client-setup.md` |
| Pick a tool for a request, fill its arguments, find its price and polling cadence | `references/tool-reference.md` |
| Fix a missing key, a missing tool, a stale tool set, a second extension, or a tool error | `references/troubleshooting.md` |
| Look up an exact price or input field | `references/scrapercity-catalog.md` |
| Apply the wallet, count, approve, poll and retry rules | `references/scrapercity-agent-patterns.md` |
| Check plan access or database allowances | `references/scrapercity-platform.md` |
| Produce the report | `templates/output-template.md`, then `scripts/check-output.py` |
| See a finished report | `examples/worked-example.md` |

## Decisions this skill makes, and why

| Decision | Reason |
|---|---|
| Always `npx -y --package scrapercity scrapercity-mcp` | There is no `scrapercity-mcp` package on npm (404 on 2026-10-13); `-y` avoids a hidden install prompt in a desktop app |
| Unpinned by default, pinned for teams | Unpinned picks up fixes on the next restart; pinned keeps a shared setup stable |
| Key in the client's variable syntax where the client supports it | Keeps keys out of committed files |
| `check_wallet` as the verification call | It is free and proves the key, the network path and the plan in one call |
| One status check per turn | A conversation is not a scheduler; repeated checks burn context and tool calls |
| Absolute `outputPath` on every download | The default writes relative to the server process, which a desktop user may not be able to find |
| Remove the old desktop extension instead of trying to update it | No npm release reaches it |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/mcp
- https://scrapercity.com/agents
- https://modelcontextprotocol.io/docs/develop/connect-local-servers
- https://code.claude.com/docs/en/mcp
- https://cursor.com/docs/context/mcp
- https://docs.devin.ai/desktop/cascade/mcp
- https://docs.cline.bot/mcp/configuring-mcp-servers
- https://geminicli.com/docs/tools/mcp-server/
- https://code.visualstudio.com/docs/copilot/reference/mcp-configuration
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli
- https://docs.npmjs.com/cli/v10/commands/npx
- https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
