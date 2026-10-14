# Client Setup: ScraperCity MCP in Every Supported Client

Every client starts the same local process: `npx -y --package scrapercity scrapercity-mcp`, with `SCRAPERCITY_API_KEY` in the process environment. scrapercity.com/mcp puts it this way: the config JSON is the same across clients and only the file path changes. The differences below come from each client's own documentation, checked 2026-10-13. The server is local only: scrapercity.com/mcp lists no hosted MCP URL, so web-only chat apps reach ScraperCity another way (ChatGPT section below). Claude on the web, the Claude mobile apps and Cowork add connectors by remote MCP server URL only, and servers in `claude_desktop_config.json` are not available there (Claude Help Center, custom connectors), so on a Claude account run ScraperCity from Claude Desktop or Claude Code.

Replace `YOUR_SCRAPERCITY_API_KEY` with the key from app.scrapercity.com/dashboard/api-docs. Never commit a file that holds the key itself.

## Quick matrix

| Client | Config location | Top-level key | Key without hardcoding | Reload |
|---|---|---|---|---|
| Claude Code | `~/.claude.json` (local and user scope) or `.mcp.json` (project scope) | `mcpServers` | `${SCRAPERCITY_API_KEY}` in `.mcp.json` | New session; `/mcp` to reconnect |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS), `%APPDATA%\Claude\claude_desktop_config.json` (Windows) | `mcpServers` | Not documented; put the key in `env` | Quit fully, reopen |
| Cursor | `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project) | `mcpServers` | `${env:SCRAPERCITY_API_KEY}` or `envFile` | Toggle in Customize, or restart Cursor |
| Windsurf (Devin Desktop) | Open from the Cascade panel: `...` menu, MCPs, Open MCP config file | `mcpServers` | `${env:SCRAPERCITY_API_KEY}` | Toggle the server, or restart |
| Cline | `cline_mcp_settings.json` via MCP Servers icon, Configure, Configure MCP Servers | `mcpServers` | Put the key in `env` | Restart from MCP settings |
| Gemini CLI | `~/.gemini/settings.json` (user) or `.gemini/settings.json` (project) | `mcpServers` | `"$SCRAPERCITY_API_KEY"` in `env` | New session; `/mcp` to check |
| GitHub Copilot in VS Code | `.vscode/mcp.json` (workspace) or user `mcp.json` via "MCP: Open User Configuration" | `servers` | `inputs` with `promptString` and `password: true` | "MCP: List Servers", restart; "MCP: Reset Cached Tools" |
| GitHub Copilot CLI | `~/.copilot/mcp-config.json` | Added with `/mcp add` | Entered in the `/mcp add` form | New session |
| OpenAI Codex (CLI, IDE extension, desktop app) | `~/.codex/config.toml`, or `.codex/config.toml` in a trusted project | `[mcp_servers.scrapercity]` TOML table | `env_vars = ["SCRAPERCITY_API_KEY"]` forwards it from the shell | New session; `/mcp` in the composer |
| OpenCode | `~/.config/opencode/opencode.json`, or `opencode.json` at the project root | `mcp`, with `"type": "local"` | `"{env:SCRAPERCITY_API_KEY}"` | Restart OpenCode |
| Goose | `~/.config/goose/config.yaml`, or `goose configure`, Add Extension, Command-Line Extension | `extensions` | `envs` map | New session |
| Zed | `settings.json` (`zed: open settings file`), or Settings, AI, MCP Servers, Add Local Server | `context_servers` | Put the key in `env` | Green dot next to the server in Settings, AI, MCP Servers |
| Hermes Agent | `~/.hermes/config.yaml` | `mcp_servers` | Put the key in `env`; Hermes passes only the listed variables to stdio servers | `/reload-mcp`; `hermes mcp test scrapercity` |
| Perplexity (Mac app) | Settings, Connectors, Add Connector, Simple tab | Connector form | Reads `SCRAPERCITY_API_KEY` from the shell profile | Save; wait for Running |
| ChatGPT | Custom GPT with an Action, not MCP | OpenAPI schema | Action authentication, API key, Bearer | Save the GPT |
| Claude web, Claude mobile, Cowork | Not supported: remote connectors by URL only | | | Use Claude Desktop or Claude Code |

## Claude Code

Per the Claude Code docs, options (`--transport`, `--env`, `--scope`) go before the server name, and `--` separates them from the server command. Do not put the server name directly after an `--env` pair; the CLI would read the name as another pair.

User scope (every project, stored in `~/.claude.json`):

```bash
claude mcp add --env SCRAPERCITY_API_KEY=YOUR_SCRAPERCITY_API_KEY --transport stdio --scope user \
  scrapercity -- npx -y --package scrapercity scrapercity-mcp
```

Project scope for a team repo, with the key read from each person's shell (`.mcp.json` at the repo root):

```json
{
  "mcpServers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "${SCRAPERCITY_API_KEY}" }
    }
  }
}
```

Claude Code expands `${VAR}` and `${VAR:-default}` in `.mcp.json`. Project servers ask for approval the first time; `claude mcp list` shows them as pending until approved.

Check and manage:

| Command | What it shows or does |
|---|---|
| `claude mcp list` | Every server and its state (Connected, Failed to connect, Pending approval) |
| `claude mcp get scrapercity` | The stored command, args, env and scope |
| `claude mcp remove scrapercity` | Deletes the entry (add `--scope` if it lives in more than one) |
| `/mcp` (inside a session) | Status and a Reconnect action |

Output limits (Claude Code MCP docs, checked 2026-10-13): Claude Code warns when one MCP result passes 10,000 tokens, and the default maximum is 25,000 (`MAX_MCP_OUTPUT_TOKENS` changes it). A successful text result over that maximum, or over 50,000 characters, is saved to a file in the session's `tool-results` folder and the conversation gets the file path instead. So a 100-row database page either lands in the chat (warned past 10,000 tokens) or arrives as a file Claude can read; count with `limit: 1`, inspect with `limit: 10`, and see where page 1 of a pull lands before paging on.

## Claude Desktop

1. Claude menu (the system menu bar, not the chat window), Settings, Developer, Edit Config. This creates the file if it does not exist.
2. Paste:

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

3. If the file already has other servers, add `"scrapercity": {...}` inside the existing `mcpServers` object. Two top-level `mcpServers` keys break the file.
4. Quit Claude Desktop completely and reopen it. The MCP guide says the app has to restart to load the config.
5. Open the "Add files, connectors, and more" control at the bottom left of the input box, then Connectors, Manage connectors, and select `scrapercity` to see its tools.

The desktop app starts the server itself, so variables exported in a terminal profile are not a reliable way to pass the key. Put it in `env`.

Logs: `~/Library/Logs/Claude/mcp.log` and `mcp-server-scrapercity.log` on macOS, `%APPDATA%\Claude\logs` on Windows. `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log` follows them.

Windows: if the log mentions `${APPDATA}` in a path with ENOENT, add `"APPDATA": "C:\\Users\\you\\AppData\\Roaming\\"` to the `env` block, and make sure npm is installed globally (`%APPDATA%\npm` exists), per the MCP guide.

## Cursor

Global file `~/.cursor/mcp.json`, or `.cursor/mcp.json` in a project:

```json
{
  "mcpServers": {
    "scrapercity": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "${env:SCRAPERCITY_API_KEY}" }
    }
  }
}
```

Cursor resolves `${env:NAME}` in `command`, `args`, `env`, `url` and `headers`, and supports `envFile` for stdio servers. Enable or disable the server with its toggle under Customize; a disabled server does not load. Cursor asks for approval before running MCP tools by default. To pick up a new npm release, the Cursor docs describe removing the server, clearing the npm cache and adding it again.

## Windsurf (Devin Desktop)

Windsurf became Devin Desktop on June 2, 2026, per its FAQ, and the MCP page now lives under docs.devin.ai. Open the file from the app so the path is always right: Cascade panel, `...` menu, MCPs section, Open MCP config file. The current docs list `~/.config/devin/mcp_config.json` on macOS and Linux and `%APPDATA%\devin\mcp_config.json` on Windows; scrapercity.com/mcp lists the older Windsurf path `~/.codeium/windsurf/mcp_config.json`.

```json
{
  "mcpServers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "${env:SCRAPERCITY_API_KEY}" }
    }
  }
}
```

Cascade can use at most 100 tools at a time across all servers. ScraperCity adds 25. If tools go missing after adding servers, turn off servers you are not using with the toggle next to each one.

## Cline

In the Cline panel: MCP Servers icon (stacked servers in the top toolbar), Configure tab, Configure MCP Servers. That opens `cline_mcp_settings.json`. The Cline CLI keeps it at `~/.cline/data/settings/cline_mcp_settings.json` (override with `CLINE_MCP_SETTINGS_PATH`).

```json
{
  "mcpServers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "YOUR_SCRAPERCITY_API_KEY" },
      "disabled": false,
      "autoApprove": ["check_wallet", "list_runs", "check_run_status"]
    }
  }
}
```

Only auto-approve free, read-only tools. Paid tools (`scrape_*`, `find_*`, `validate_emails`, `search_criminal_records`) should always ask. Restart an unresponsive server from MCP settings.

## Gemini CLI

User scope `~/.gemini/settings.json`, project scope `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "$SCRAPERCITY_API_KEY" },
      "trust": false
    }
  }
}
```

Gemini CLI redacts inherited variables whose names match patterns such as `*KEY*`, `*TOKEN*` and `*SECRET*`. `SCRAPERCITY_API_KEY` matches, so it reaches the server only when listed in the server's `env` block as above. Keep `trust: false` so paid calls still ask. `includeTools` can limit the server to a subset, for example only the free utility tools on a shared machine. The default request timeout is 10 minutes. `gemini mcp list` shows connection state; stdio servers show Disconnected in an untrusted folder until `gemini trust` is run there. `/mcp` inside a session lists the tools.

## GitHub Copilot in VS Code

VS Code uses a top-level `servers` key, not `mcpServers`. Workspace file `.vscode/mcp.json`:

```json
{
  "inputs": [
    { "type": "promptString", "id": "scrapercity-key", "description": "ScraperCity API key", "password": true }
  ],
  "servers": {
    "scrapercity": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "${input:scrapercity-key}" }
    }
  }
}
```

VS Code prompts for the input the first time the server starts, so the file can be committed without the key. For a user-wide setup, run "MCP: Open User Configuration". Manage the server with "MCP: List Servers" (start, stop, logs). After a ScraperCity release, run "MCP: Reset Cached Tools", which clears the cached tool list when a server's tools change.

## GitHub Copilot CLI

Start an interactive session, run `/mcp add`, fill in the fields (name `scrapercity`, command `npx`, arguments `-y --package scrapercity scrapercity-mcp`, environment `SCRAPERCITY_API_KEY`), Tab between fields, Ctrl+S to save. The entry is stored in `~/.copilot/mcp-config.json` (the folder moves with `COPILOT_HOME`).

## OpenAI Codex

Codex reads MCP servers from `~/.codex/config.toml`; the CLI, the IDE extension and the ChatGPT desktop app share that file, and a trusted project can add `.codex/config.toml` (OpenAI Codex MCP docs). One command writes the entry:

```bash
codex mcp add scrapercity --env SCRAPERCITY_API_KEY=YOUR_SCRAPERCITY_API_KEY -- npx -y --package scrapercity scrapercity-mcp
codex mcp list
```

Or edit the file. `env_vars` forwards the key from the shell, so the file never holds it:

```toml
[mcp_servers.scrapercity]
command = "npx"
args = ["-y", "--package", "scrapercity", "scrapercity-mcp"]
env_vars = ["SCRAPERCITY_API_KEY"]
startup_timeout_sec = 30
disabled_tools = ["search_criminal_records"]
```

`startup_timeout_sec` defaults to 10 seconds; the first `npx` start downloads the package, so 30 gives it room. `tool_timeout_sec` defaults to 60, which covers every ScraperCity call because scrapers return a `runId` at once and a database search that runs long comes back as a 503. `enabled_tools` and `disabled_tools` trim the tool list for a narrow agent; the example hides a tool that agent never needs. Type `/mcp` in the composer to see the server.

## OpenCode

Global `~/.config/opencode/opencode.json`, or `opencode.json` at the project root (project overrides global):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "scrapercity": {
      "type": "local",
      "command": ["npx", "-y", "--package", "scrapercity", "scrapercity-mcp"],
      "enabled": true,
      "timeout": 30000,
      "environment": { "SCRAPERCITY_API_KEY": "{env:SCRAPERCITY_API_KEY}" }
    }
  }
}
```

`command` is one array, not `command` plus `args`. `timeout` is how long OpenCode waits to fetch the tool list and defaults to 5,000 ms, which a first `npx` download can exceed, so set 30,000. An unset `{env:...}` variable becomes an empty string, which shows up as `Error: No API key`.

## Goose

Run `goose configure`, choose Add Extension, then Command-Line Extension, and answer the prompts (name `scrapercity`, command `npx -y --package scrapercity scrapercity-mcp`, environment variable `SCRAPERCITY_API_KEY`). The result in `~/.config/goose/config.yaml`:

```yaml
extensions:
  scrapercity:
    name: scrapercity
    type: stdio
    cmd: npx
    args: [-y, --package, scrapercity, scrapercity-mcp]
    envs: { "SCRAPERCITY_API_KEY": "YOUR_SCRAPERCITY_API_KEY" }
    enabled: true
    timeout: 300
```

## Zed

Open the settings file with the command palette (`zed: open settings file`), or use Settings, AI, MCP Servers, Add Local Server, which writes the same entry:

```json
{
  "context_servers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "YOUR_SCRAPERCITY_API_KEY" }
    }
  },
  "agent": {
    "tool_permissions": {
      "tools": {
        "mcp:scrapercity:check_wallet": { "default": "allow" },
        "mcp:scrapercity:list_runs": { "default": "allow" },
        "mcp:scrapercity:check_run_status": { "default": "allow" }
      }
    }
  }
}
```

A green dot next to `scrapercity` in Settings, AI, MCP Servers means the server is running. The agent's default tool permission is `confirm` (Zed 0.224.0 and later), so every tool not listed above, paid tools included, asks before it runs. MCP tools accept only the tool-level `default` value, keyed `mcp:<server>:<tool>`.

## Hermes Agent

Hermes reads MCP servers from `~/.hermes/config.yaml` under `mcp_servers`. It passes a stdio server only the variables listed in its `env` plus a small baseline, not your shell profile, so the key has to be in the entry:

```yaml
mcp_servers:
  scrapercity:
    command: "npx"
    args: ["-y", "--package", "scrapercity", "scrapercity-mcp"]
    env:
      SCRAPERCITY_API_KEY: "YOUR_SCRAPERCITY_API_KEY"
    connect_timeout: 30
    tools:
      exclude: [search_criminal_records]
```

`connect_timeout` bounds the first handshake, which includes the first `npx` download, so give it room. `tools.include` or `tools.exclude` (glob patterns allowed; `include` wins when both are set) trims the tool list for a narrow agent. After editing, run `/reload-mcp` in the session, then `hermes mcp test scrapercity` to see what the server answered; a server that failed to register is named in `agent.log`.

## Perplexity (Mac app)

Local connectors need the Perplexity Mac app on a Pro plan (scrapercity.com/integrations/perplexity).

1. Settings, Connectors. Install the PerplexityXPC helper when asked; the Mac sandbox needs it to start local servers.
2. Put the key in the shell profile: `echo 'export SCRAPERCITY_API_KEY="YOUR_SCRAPERCITY_API_KEY"' >> ~/.zshrc`, then open a new terminal. The connector form has no environment field.
3. Add Connector, Simple tab: Server Name `ScraperCity`, Command `npx -y --package scrapercity scrapercity-mcp`. Save and wait for Running.
4. On the home screen, turn the connector on under Sources and ask it to check the wallet. Approve the call.

ScraperCity's Perplexity guide says the Lead Database needs the $649 plan; the pricing page and `references/scrapercity-platform.md` say Growth ($149/mo) and up. Go by the platform reference.

## ChatGPT (custom GPT, no MCP)

ChatGPT web cannot start a local server, so ScraperCity's ChatGPT guide builds a custom GPT whose Action calls the REST API (scrapercity.com/integrations/chatgpt):

1. chatgpt.com/create, Configure tab. Creating a GPT needs a paid ChatGPT plan.
2. Actions, Create new action, paste the OpenAPI schema from the guide. It points at `https://app.scrapercity.com/api/v1` and defines `searchLeads` (`/database/leads`) and `searchLocalBusinesses` (`/database/local-businesses`).
3. Authentication: API Key, auth type Bearer, paste a key made only for this GPT.
4. Test, then save as Only me. "Anyone with the link" or the GPT Store lets other people spend this wallet.

Limits: database search only (Growth plan and up), one call per message, default page size 50, no scrapers, no CSV export. For scrapers or bulk files, use Claude Desktop, Codex or the CLI.

## Verify, in every client

1. The tool list shows 25 tools. Spot-check `check_wallet`, `query_lead_database`, `scrape_distress_list`, `find_mobiles`.
2. Ask the agent to call `check_wallet`. Expect `plan.name` and `wallet.total_balance_dollars`. (ChatGPT custom GPT: run the Action's test with `limit: 1` instead.)
3. If the reply starts `Error: No API key`, the env block never reached the process. Recheck the key name, the file, and that the client was fully restarted.

## Pinning a version

`"args": ["-y", "--package", "scrapercity@1.0.17", "scrapercity-mcp"]` pins the release. Pin in shared or production setups so a release never changes tool behavior mid-campaign; unpin (or bump the pin) on purpose after reading the release notes on npm.

## Sources

- https://scrapercity.com/mcp
- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://code.claude.com/docs/en/mcp
- https://modelcontextprotocol.io/docs/develop/connect-local-servers
- https://cursor.com/docs/context/mcp
- https://docs.devin.ai/desktop/cascade/mcp
- https://docs.devin.ai/desktop/devin-desktop-faq
- https://docs.cline.bot/mcp/configuring-mcp-servers
- https://geminicli.com/docs/tools/mcp-server/
- https://code.visualstudio.com/docs/copilot/customization/mcp-servers
- https://code.visualstudio.com/docs/copilot/reference/mcp-configuration
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli
- https://developers.openai.com/codex/mcp
- https://opencode.ai/docs/mcp-servers/
- https://opencode.ai/docs/config/
- https://block.github.io/goose/docs/getting-started/using-extensions/
- https://zed.dev/docs/ai/mcp
- https://zed.dev/docs/ai/tool-permissions
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://support.claude.com/en/articles/11175166
- https://scrapercity.com/integrations/perplexity
- https://scrapercity.com/integrations/chatgpt
