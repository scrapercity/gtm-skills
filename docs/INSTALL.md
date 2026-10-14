# Install

Five ways to get the skills into an agent, from most to least automated:

1. The Claude Code plugin, for Claude Code only.
2. `install.sh`, for the eleven agent targets in the table below or any folder you name.
3. Zip files for the Claude apps (claude.ai and Claude Desktop), built by `install.sh --zip`.
4. `gh skill install`, from the GitHub CLI.
5. Copying a folder by hand.

Every skill folder is self-contained. Shared references are copied into each skill that uses them, so any subset you install works without the rest of the repo.

## Claude Code plugin

```text
/plugin marketplace add scrapercity/gtm-skills
/plugin install gtm-skills@scrapercity
```

From a shell: `claude plugin marketplace add scrapercity/gtm-skills` then `claude plugin install gtm-skills@scrapercity`. Skills load as `gtm-skills:<name>`. Updates arrive through `/plugin` when the version in `.claude-plugin/plugin.json` changes.

The manifest lists the three category folders in its `skills` key because Claude Code reads each listed folder as a directory of `<name>/SKILL.md` folders ([plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)); pointing it at `skills/` alone would find category folders, not skills.

## install.sh

Clone the repo, then run the installer from the clone:

```bash
git clone https://github.com/scrapercity/gtm-skills.git
cd gtm-skills
./install.sh
```

Run with no flags in a terminal, it asks three questions (which agents, as a comma list of numbers; user or project scope; every skill, or any mix of bundles and categories), shows each destination folder with how many of the selected skills are already there, and asks for a yes before it writes. Run with no flags outside a terminal (a pipe, CI), it installs every skill into `~/.claude/skills`.

### Flags

| Flag | What it does |
|-|-|
| `--target <name>` | `claude`, `codex`, `copilot`, `cursor`, `gemini`, `opencode`, `windsurf`, `goose`, `cline`, `hermes`, `agents` or `all`. Comma list or repeat. Default `claude`. |
| `--scope user\|project` | User scope writes under your home folder. Project scope writes under the project folder. Default `user`. |
| `--project-dir <dir>` | The project root for `--scope project`. Default: the current folder. |
| `--dest <dir>` | Any folder an agent reads skills from. Overrides `--target` and `--scope`. |
| `--bundle <name>` | A named group of skills (table below). Comma list or repeat. |
| `--category <name>` | `scrapercity`, `list-building` or `outbound`. Comma list or repeat. |
| `--skill <name>` | One skill. Comma list or repeat. Bundles, categories and skills add together. |
| `--update` | Replace installed skills whose files differ from this checkout, install missing ones, leave identical ones alone. The safe way to upgrade. |
| `--force` | Replace every selected skill folder that already exists. Without `--update` or `--force`, existing folders are skipped. |
| `--uninstall` | Remove the selected skills from the destination folders. Only folders whose `SKILL.md` carries the matching `name:` are removed. |
| `--zip <dir>` | Write one `<skill>.zip` per selected skill into `<dir>`, for upload to the Claude apps. Nothing is installed. |
| `--dry-run` | Print every folder it would write or remove. Writes nothing. |
| `--yes`, `-y` | Skip the confirmation prompt. |
| `--no-verify` | Skip the `skills.lock` check after installing. |
| `--list`, `--search <word>` | Print every skill with its first sentence, or only those whose name or description contains the word. |
| `--list-bundles`, `--list-targets` | Print the bundles, or each target's folders, then exit. |

After a real install or update, the installer checks every skill it wrote against `skills.lock` (when `python3` is on PATH and the checkout's lock is current) and prints `Verified:` per folder, or `MISMATCH:` and exits 1. It prints installed, replaced, current, skipped and failed totals and exits 1 when any skill failed to copy. Each skill is copied to a temporary folder beside the destination and renamed into place, so an interrupted run never leaves a half-written skill under its real name; `__pycache__` and `.DS_Store` are left out.

It runs on bash 3.2 (the macOS default) and later, with `cp`, `mv`, `rm`, `find`, `diff`, `sed`, `awk` and `tr`. `--zip` uses `zip`, or `python3` when `zip` is missing.

### Examples

```bash
./install.sh --target cursor --dry-run                          # see the plan first
./install.sh --target all --yes                                 # every agent, user scope
./install.sh --target codex,gemini --bundle email-from-zero     # two agents, one bundle
./install.sh --target copilot --scope project --project-dir ~/code/acme --bundle calling
./install.sh --dest ~/my-agent/skills --skill cold-calling      # an agent not in the table
./install.sh --target all --update --yes                        # upgrade after git pull
./install.sh --target claude --skill tam-builder --uninstall    # remove one skill
./install.sh --search caller                                    # find a skill by keyword
./install.sh --zip ~/Downloads/gtm-skills --bundle local-outbound
```

### Bundles

| Bundle | For | Skills |
|-|-|-|
| `local-outbound` | Local businesses by email | local-business-list, cold-email-strategy, cold-email-copywriting, reply-handling |
| `b2b-outbound` | B2B contacts like your best customers | icp-list-builder, cold-email-list, cold-email-strategy, cold-email-copywriting, reply-handling |
| `account-based` | Buyers at named accounts | account-researcher, decision-maker-finder, signal-triggered-outbound, multi-channel-outreach |
| `email-from-zero` | A cold email sending setup from zero | domain-infrastructure, inbox-setup, email-deliverability, sending-platforms |
| `calling` | A calling program | mobile-appender, cold-calling, multi-channel-outreach |
| `property-owners` | Property owner lists with phones | scrapercity-real-estate-data, skip-tracer, mobile-appender, multi-channel-outreach |
| `list-core` | B2B list building and list hygiene | icp-list-builder, tam-builder, cold-email-list, email-list-cleaner |
| `platform` | The ScraperCity platform | the 8 skills in `skills/scrapercity/`, including the `using-scrapercity-skills` router |

Add the router to any bundle with `--skill using-scrapercity-skills`.

## Target folders

Each path below was checked against the agent's own documentation on 2026-10-13. Project paths are relative to `--project-dir`.

| Target | User scope | Project scope | Source |
|-|-|-|-|
| `claude` (Claude Code) | `~/.claude/skills` | `.claude/skills` | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| `codex` (OpenAI Codex) | `~/.agents/skills` | `.agents/skills` | [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills) |
| `copilot` (GitHub Copilot) | `~/.copilot/skills` | `.github/skills` | [docs.github.com: About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| `cursor` | `~/.cursor/skills` | `.cursor/skills` | [cursor.com/docs/context/skills](https://cursor.com/docs/context/skills) |
| `gemini` (Gemini CLI) | `~/.gemini/skills` | `.gemini/skills` | [geminicli.com/docs/cli/skills](https://geminicli.com/docs/cli/skills/) |
| `opencode` | `~/.config/opencode/skills` | `.opencode/skills` | [opencode.ai/docs/skills](https://opencode.ai/docs/skills/) |
| `windsurf` | `~/.codeium/windsurf/skills` | `.windsurf/skills` | [docs.windsurf.com: Cascade skills](https://docs.windsurf.com/windsurf/cascade/skills) |
| `goose` | `~/.agents/skills` | `.agents/skills` | [goose-docs.ai: Using skills](https://goose-docs.ai/docs/guides/context-engineering/using-skills) |
| `cline` | `~/.cline/skills` | `.cline/skills` | [docs.cline.bot: Skills](https://docs.cline.bot/customization/skills) |
| `hermes` (Hermes Agent) | `~/.hermes/skills` | `.hermes/skills` | [hermes-agent.nousresearch.com: Skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) |
| `agents` (shared folder) | `~/.agents/skills` | `.agents/skills` | The cross-agent folder the Codex, goose, Copilot, Cursor, Gemini CLI, OpenCode and Hermes pages above list |

Notes from the same pages:

- **Codex** reads `.agents/skills` in every folder from the working directory up to the repository root. The Codex skills URL now redirects to an OpenAI help page with the same paths.
- **Copilot** also reads `.claude/skills` and `.agents/skills` in a project, and `~/.agents/skills` at user scope.
- **Cursor** also reads `.agents/skills`, `~/.agents/skills`, and the Claude and Codex folders.
- **Gemini CLI** accepts `.agents/skills` and `~/.agents/skills` as aliases. When both exist, `.agents/skills` wins within the same scope.
- **OpenCode** also reads `.claude/skills`, `.agents/skills` and their home-folder versions.
- **Windsurf** documentation now redirects to Devin Desktop docs. Those pages list `.devin/skills` as the preferred project folder and still read `.windsurf/skills`, which older Windsurf builds also read, so the installer uses `.windsurf/skills`. The user folder `~/.codeium/windsurf/skills` is unchanged.
- **goose** recommends `~/.agents/skills` and `.agents/skills`, and also reads `.goose/skills` and the Claude folders.
- **Cline** also reads `.clinerules/skills` and `.claude/skills` in a project. Skills are on by default and can be switched off in its Skills menu.
- **Hermes Agent** treats `~/.hermes/skills` as its main folder. It loads project skills from `.hermes/skills` and `.agents/skills` only after you run `hermes skills trust` in that repository, and `~/.agents/skills` only when added under `skills.external_dirs` in `~/.hermes/config.yaml`.
- `codex`, `goose` and `agents` share a folder. With `--target all` the installer writes it once and labels it `codex,goose,agents`.

Because several agents read `~/.claude/skills` or `.agents/skills` too, installing into those folders can make a skill show up in more than one agent. That is expected.

Agents not in the table work with `--dest <folder>` pointed at the folder their own documentation names. Built-in targets exist only for agents whose skills folder appears in their own official documentation.

## Claude apps (claude.ai and Claude Desktop)

The Claude apps take custom skills as uploaded zip files, one skill per zip with the skill folder at the root of the zip ([Claude help center: How to create custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)). Anthropic's skills overview lists the upload on Pro, Max, Team and Enterprise plans with code execution turned on, and notes that a skill uploaded to the apps does not sync to Claude Code or the API ([Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)).

```bash
./install.sh --zip ~/Downloads/gtm-skills                    # every skill
./install.sh --zip ~/Downloads/gtm-skills --bundle calling   # a bundle
```

Upload each zip in the app's skills settings and turn the skill on. The help center article lists 200 characters as the description limit for an uploaded skill; the installer counts how many selected skills run longer so you know which to shorten if an upload is refused. Connect the ScraperCity MCP server in the app as well (README, "Connect ScraperCity").

## gh skill install

GitHub CLI 2.90.0 and later include `gh skill` ([GitHub changelog, 2026-04-16](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/), [manual](https://cli.github.com/manual/gh_skill_install)). GitHub labels it a public preview, so flags may change. It finds the skills in this repo by their `skills/<category>/<skill>/SKILL.md` paths:

```bash
gh skill preview scrapercity/gtm-skills cold-calling                # read it before installing
gh skill install scrapercity/gtm-skills                              # pick skills interactively
gh skill install scrapercity/gtm-skills cold-calling --agent claude-code --scope user
gh skill install scrapercity/gtm-skills skills/outbound/cold-calling # exact path, skips discovery
gh skill install scrapercity/gtm-skills --all --agent cursor --scope project
gh skill install scrapercity/gtm-skills cold-calling --pin v1.0.0    # a release tag
gh skill update --all
```

`--dir <folder>` installs into any folder. Run `gh skill install --help` for the agent names your version accepts. `gh skill` writes `metadata.github-*` tracking lines into each installed `SKILL.md`; `generate-lock.py --verify` sets those lines aside before comparing, so a `gh`-installed skill verifies like any other.

## By hand

Copy any folder under `skills/<category>/` into your agent's skills folder. Do not copy the category folder itself: agents look one level down for `<skill>/SKILL.md`.

## After installing

1. Connect ScraperCity: README, "Connect ScraperCity".
2. Restart the agent or start a new session so it rescans its skills folder.
3. Ask it to load `using-scrapercity-skills`.
4. Optional: check any copy against the lock with `python3 scripts/generate-lock.py --verify <skills folder>`. See [INTEGRITY.md](INTEGRITY.md).

Skills include small Python checker scripts. Read them before you install, as with any skill from the internet.
