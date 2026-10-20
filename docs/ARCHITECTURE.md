# Architecture

How the repo is laid out, which files a person writes and which a script writes, and the order the scripts run in.

## Layout

```text
gtm-skills/
├── skills/<category>/<skill>/     # what gets installed; one folder per skill
│   ├── SKILL.md                   # entrypoint the agent loads
│   ├── references/                # skill-owned references, plus copies of shared references
│   ├── templates/output-template.md
│   ├── examples/worked-example.md
│   └── scripts/check-output.py
├── references/                    # repo-root shared references (source of truth) and the pitfalls index
├── scripts/                       # repo tooling: validators, generators, catalog sync, scaffolder
├── docs/                          # standards and process (this folder)
├── .claude-plugin/                # Claude Code plugin and marketplace manifests
├── .github/                       # CI, Dependabot, issue and pull request templates
├── .githooks/pre-commit           # runs the offline checks before each commit (opt in once per clone)
├── install.sh                     # installs, updates, removes or zips skill folders for 11 agent targets
├── skills.lock                    # SHA-256, size and kind of every packaged file
├── taxonomy.csv                   # one row per skill: version, description, links, frameworks, tools, prices
├── AGENTS.md                      # notes for agents working in the repo, with a generated skill index
└── README.md                      # hand-written prose with three generated blocks
```

Categories are `scrapercity` (the platform and the router), `list-building` and `outbound`. The category folder exists for people browsing the repo. Agents never see it: installers copy each `<skill>` folder directly into the agent's skills folder.

Only `skills/` is packaged. Everything else is tooling, documentation or metadata for the repo.

## Hand-written and generated files

| File | Written by | Edit it by hand? |
|-|-|-|
| `skills/*/*/SKILL.md`, skill-owned references, templates, examples, checkers | People | Yes |
| `references/*.md` except the two below | People | Yes. This is the only place to edit a shared reference. |
| `references/scrapercity-catalog.md` | `scripts/sync-catalog.mjs` | No |
| `references/pitfalls-index.md` | `scripts/generate-indexes.py` | No |
| `skills/*/*/references/<shared file>` | `scripts/materialize-shared-references.py` | No. Changes are overwritten. |
| `README.md` and `AGENTS.md` between `<!-- GENERATED:... -->` markers, the skill count in both plugin manifests | `scripts/generate-readme.py` | No. Prose outside the markers is hand-written. |
| `taxonomy.csv` | `scripts/generate-indexes.py` | No |
| `skills.lock` | `scripts/generate-lock.py` | No |
| `docs/`, `install.sh`, `scripts/`, `.github/`, `.claude-plugin/` | People | Yes |

Every generator has a `--check` mode that exits 1 when its output is out of date. CI runs each one, so a pull request that edits a source without regenerating fails; the failed run uploads a `regenerated-files` patch with the fix.

## Scripts

| Script | What it does |
|-|-|
| `validate-skills.py` | Skill structure, frontmatter, section order, copy rules and the checker contract. `--strict` adds the Agent Skills spec, link and package hygiene checks; `--check-legal` adds owner rule 1. |
| `check-repo.py` | Everything outside the skill folders: required files, version agreement across the manifests, CITATION and CHANGELOG, plugin skill paths, installer bundles and docs, workflow pins, the owner rules in author docs, copy rules, secrets and junk. |
| `check-all.sh` | Every check above plus the generator checks, shellcheck, `claude plugin validate --strict` and the `skills-ref` validator, in CI order. `--offline`, `--strict`, `--check-legal`, `--fast`. |
| `regenerate.sh` | Every writer, in order, lock last. `--catalog` resyncs the catalog first; `--prune` deletes orphan shared-reference copies. |
| `sync-catalog.mjs` | Writes `references/scrapercity-catalog.md` from the published npm package. |
| `materialize-shared-references.py` | Copies each listed shared reference into its skills. `--check` also warns about orphans (copies a skill no longer lists, found by name and by the `shared` flag in `skills.lock`); `--prune` deletes them; `--check --strict` fails on them. |
| `generate-indexes.py` | Writes `references/pitfalls-index.md` and `taxonomy.csv`. |
| `generate-readme.py` | Writes the README and AGENTS.md generated blocks and the manifest skill counts. |
| `generate-lock.py` | Writes, checks and verifies `skills.lock`. |
| `normalize-frontmatter.py` | Rewrites flow-style `[lists]` in frontmatter as block lists, values unchanged. |
| `new-skill.py` | Scaffolds a skill folder that meets the layout and checker contract, every field marked `[fill]`. |

## Catalog sync

`scripts/sync-catalog.mjs` downloads the published `scrapercity` npm package (the MCP server and CLI), reads the catalog that package ships, and writes `references/scrapercity-catalog.md`: every tool id, endpoint, input schema and price, plus the CLI commands in that version. It also confirms the hand-listed utility tools still exist in the package, and it applies a short, commented list of price overrides where the package renders a price wrong.

The skills take tool names and prices only from that file. The package is published often, and most releases change no tool, price or CLI command, so the version line in the catalog is not compared: a release that changes only the version passes `--check`, and the writer leaves the file unchanged. When a release changes a tool, a price or a CLI command, the maintainers resync the catalog right after the publish; if they miss one, `node scripts/sync-catalog.mjs --check` fails in the weekly scheduled CI run and names the first line that moved. After a price change, re-read any skill that quotes the old price.

## Shared-reference materialization

A skill names the repo-root references it uses in `metadata.shared_references`. `scripts/materialize-shared-references.py` copies each of those files into the skill's own `references/` folder. That keeps every skill folder self-contained: install one folder alone and every file it points to is there.

The root copy is the source of truth. The copies inside skills are byte-identical, and the materializer's `--check` fails if any copy differs. `references/pitfalls-index.md` is a repo-level index and must never be listed in `shared_references`.

## Indexes

`scripts/generate-indexes.py` writes two files for browsing:

- `references/pitfalls-index.md` collects every row of every skill's Common Pitfalls table, grouped by category and skill, each heading linking to its skill.
- `taxonomy.csv` lists each skill with its category, path, `metadata.frameworks`, the ScraperCity tool ids its `SKILL.md` names (matched against the catalog) and the dollar amounts its `SKILL.md` quotes.

## Lock

`scripts/generate-lock.py` hashes every file in every skill folder and writes `skills.lock`. It runs last, after every other generator, because it hashes their output. See [INTEGRITY.md](INTEGRITY.md) for the format and what it proves.

## Regeneration order

After changing a skill or a shared reference:

```bash
scripts/regenerate.sh              # add --catalog when the npm package changed
scripts/check-all.sh --offline
```

`regenerate.sh` runs `materialize-shared-references.py`, `generate-indexes.py`, `generate-readme.py`, then `generate-lock.py`, which always goes last because it hashes the others' output.

## Plugin manifests

`.claude-plugin/plugin.json` declares the plugin and points `skills` at the three category folders, because Claude Code reads each listed folder as a directory of `<name>/SKILL.md` folders and our skills sit two levels under `skills/`. `check-repo.py` fails if a category folder is added without being listed. The manifest also carries `documentationUrl` and `supportUrl` for Anthropic's plugin directory listing, and the marketplace entry carries `category` and `tags` for search. `.claude-plugin/marketplace.json` lists the plugin so `/plugin marketplace add scrapercity/gtm-skills` works. Check both with `claude plugin validate . --strict` from the repo root; CI runs it on every push.

The repo has no root `CLAUDE.md`. Claude Code skips a `CLAUDE.md` at a plugin root, and its validator warns when it finds one. Notes for agents working on the repo live in `AGENTS.md`.

## Runtime behavior

No telemetry: static files and local scripts only. The checkers use the Python standard library and make no network calls. The one network call in the repo tooling is `sync-catalog.mjs` reading the public npm registry. `generate-lock.py` asks the local `git` for the current commit and nothing else.
