# Framework Notes: scrapercity-mcp

Which sources shape this skill, what each one contributes, and which file to open for what.

## Sources and what they contribute

| Source | Type | What it contributes | Where it shows up |
|---|---|---|---|
| `scrapercity` npm package 1.0.17 (`bin/mcp.mjs`, `lib/client.mjs`, generated tool catalog) | Vendor code, primary | The 25 tool names and schemas, the `--package` requirement (the binary is `scrapercity-mcp`, the package is `scrapercity`), the key lookup order, the `Error:` text format, the `download_results` default of `{runId}.csv`, `list_runs` caps (168 hours, 100 runs) | SKILL.md steps 3-8, `references/tool-reference.md`, `references/troubleshooting.md` |
| `references/scrapercity-catalog.md` | Generated from the package | Every per-result price and input schema | Every cost line |
| `references/scrapercity-agent-patterns.md` | Shared operating rules | Wallet first, count first, a go-ahead before every paid run, the rank-and-cap cut, start-poll-download, webhook for Apollo, polling cadence, error and retry tables, CSV naming | SKILL.md step 7, every run plan |
| `references/scrapercity-platform.md` | Vendor facts | Plans, database access from Growth ($149/mo), 100,000 new records a day, integrations list naming the seven MCP clients | Prerequisites, decision table |
| scrapercity.com/mcp | Vendor docs | Same JSON in every client, fully quit and relaunch, key from the dashboard, a separate key for agents, duplicate protection | Client setup, prerequisites |
| Model Context Protocol, "Connect to local MCP servers" | Protocol docs | Claude Desktop config path, Developer settings route, full restart, log files, Windows `${APPDATA}` fix | `references/client-setup.md`, troubleshooting |
| Anthropic, Claude Code MCP docs | Client docs | `claude mcp add` option order and `--`, scopes and where each is stored, `.mcp.json` `${VAR}` expansion, `claude mcp list/get/remove`, `/mcp`, the 10,000-token output warning, the 25,000-token default cap and the save-to-file behavior past it or past 50,000 characters | Client setup, step 8 (where a database page lands), pitfalls |
| Cursor MCP docs | Client docs | `~/.cursor/mcp.json` and project file, `${env:NAME}`, `envFile`, Customize toggle, approval by default | Client setup |
| Devin Desktop (formerly Windsurf) Cascade MCP docs and FAQ | Client docs | Rename date, config path, `${env:VAR}`, 100-tool cap, toggles | Client setup, troubleshooting |
| Cline MCP docs | Client docs | `cline_mcp_settings.json` route, `disabled` and `autoApprove` | Client setup |
| Gemini CLI MCP docs | Client docs | `settings.json` scopes, `$VAR` expansion, redaction of `*KEY*` variables, `trust`, `includeTools`, folder trust | Client setup, pitfalls |
| VS Code GitHub Copilot MCP docs | Client docs | `servers` key, `type: stdio`, `inputs` with `password: true`, "MCP: List Servers", "MCP: Reset Cached Tools" | Client setup, stale-version fix |
| GitHub Copilot CLI docs | Client docs | `/mcp add`, `~/.copilot/mcp-config.json` | Client setup |
| OpenAI Codex MCP docs | Client docs | `~/.codex/config.toml`, `[mcp_servers.<name>]`, `env_vars` forwarding, `startup_timeout_sec` (10 s) and `tool_timeout_sec` (60 s) defaults, `enabled_tools` and `disabled_tools`, `codex mcp add ... --env ... --` | Client setup |
| OpenCode MCP and config docs | Client docs | `mcp` key, `type: local`, single `command` array, `{env:VAR}`, 5,000 ms tool-fetch timeout | Client setup |
| Goose extensions docs | Client docs | `goose configure` flow, `extensions` YAML with `cmd`, `args`, `envs`, `type: stdio` | Client setup |
| Zed MCP and tool permissions docs | Client docs | `context_servers` entry with `command`, `args`, `env`; status dot; `confirm` default and `mcp:<server>:<tool>` rules | Client setup |
| Hermes Agent MCP docs | Client docs | `~/.hermes/config.yaml` `mcp_servers`, env passed only when listed, `connect_timeout`, `tools.include` and `exclude`, `/reload-mcp`, `hermes mcp test` | Client setup |
| Claude Help Center, custom connectors | Client docs | Claude web, mobile and Cowork take remote MCP servers by URL only; local config servers are not available there | Client setup, When to Use |
| scrapercity.com/integrations/chatgpt and /perplexity | Vendor docs | The custom GPT Action path for ChatGPT (database search only) and the Perplexity Mac local connector with its helper app | Client setup |
| Anthropic, "Writing effective tools for agents" | Engineering guidance | Tools should return meaningful errors and agents should be evaluated on realistic tasks; basis for the agent test matrix | SKILL.md step 4 and Agent Rules |
| npm docs (npx, config cache) | Tool docs | `--package` to run a binary from a differently named package, `-y` to skip the install prompt, npm cache location | Config args, cache clearing |
| scrapercity.com/email-validator | Vendor docs | The `email` and `email_result` columns and their five values, read by the join script | `references/tool-reference.md` bulk pull scripts |
| Alex Berman, B2B lead generation guide (alexberman.com) | Operator's published work | Verify the list before sending; a 95%+ valid rate is the minimum. The reason database emails are validated, cited inline when a report uses it | Plan example, validation step |
| AWS Architecture Blog, "Exponential Backoff and Jitter" | Engineering reference | Backoff with jitter for safe retries on 429 and 503 | Error handling (via agent patterns) |

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
| See a finished report or plan | `examples/worked-example.md` (run report), `examples/plan-only-example.md` (plan) |

## Decisions this skill makes, and why

| Decision | Reason |
|---|---|
| Always `npx -y --package scrapercity scrapercity-mcp` | There is no `scrapercity-mcp` package on npm (404 on 2026-10-13); `-y` avoids a hidden install prompt in a desktop app |
| Tool tiers set in the client (auto-approve free tools only) | A paid tool should always show the user an approval prompt, whatever the agent's own rules say |
| Every paid run waits for a go-ahead, with no dollar threshold | Scrapers draw from the wallet per result as they deliver (scrapercity.com/llm-info); no source sets a safe amount, so the user sets one or approves each run |
| A plan states itself once and carries no results | A reader cannot tell an assumed count or runId from a real one; one `Plan only:` line is enough |
| Cut people pulls by title rank and a per-company cap | Cursor order is id order; the user's title order and cap are the only stated priorities |
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
- https://developers.openai.com/codex/mcp
- https://opencode.ai/docs/mcp-servers/
- https://block.github.io/goose/docs/getting-started/using-extensions/
- https://zed.dev/docs/ai/mcp
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://support.claude.com/en/articles/11175166
- https://scrapercity.com/integrations/chatgpt
- https://scrapercity.com/integrations/perplexity
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://scrapercity.com/email-validator
- https://scrapercity.com/llm-info
- https://alexberman.com/b2b-lead-generation
- https://docs.npmjs.com/cli/v10/commands/npx
- https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
