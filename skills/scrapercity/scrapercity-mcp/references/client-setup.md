# Client Setup: ScraperCity MCP in Seven Clients

Every client starts the same local process: `npx -y --package scrapercity scrapercity-mcp`, with `SCRAPERCITY_API_KEY` in the process environment. scrapercity.com/mcp puts it this way: the config JSON is the same across clients and only the file path changes. The differences below come from each client's own documentation, checked 2026-10-13.

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

Limits worth knowing: Claude Code warns when one MCP result passes 10,000 tokens and caps output at 25,000 by default (`MAX_MCP_OUTPUT_TOKENS` raises it). A 100-row database page can come close, so count with `limit: 1` and inspect with small limits.

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

## Verify, in every client

1. The tool list shows 25 tools. Spot-check `check_wallet`, `query_lead_database`, `scrape_distress_list`, `find_mobiles`.
2. Ask the agent to call `check_wallet`. Expect `plan.name` and `wallet.total_balance_dollars`.
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
