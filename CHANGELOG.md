# Changelog

## Unreleased

### Owner rules

Two rules from the repo owner (October 13, 2026) now govern every skill and every author doc:

- **No legal content.** No laws, regulations, regulators, fines, registries, consent or registration requirements, disclaimers or advice to get legal review in any skill, even when correct. Legal texts no longer count as sources.
- **No moralizing.** Skills say what to do to get more replies, meetings and revenue at lower cost; each rule is a setting tied to results.

The author docs (SKILL_AUTHORING, QUALITY_BAR, SOURCE_STANDARDS, RELEASE_PROCESS, CONTRIBUTING, GOVERNANCE, SUPPORT, README, the issue and pull request templates) state both rules and no longer ask for legal sources or compliance sections. `references/glossary.md` dropped its laws section, and `references/experts.md` cites no regulator.

### Added

- `validate-skills.py --check-legal` (off by default) fails any skill file or root reference that names a law, regulation or regulator, cites a CFR section, sends the reader to legal counsel, or adds a legal checkpoint. Reply-classification words stay allowed in `reply-handling`, and law firms stay a prospecting vertical.
- `validate-skills.py --strict`: Agent Skills name rules, no reserved words or XML tags, only spec frontmatter keys, block-style lists (the `skills-ref` validator rejects flow lists), SKILL.md under 500 lines, unique names, each section once, at least 3 distinct frameworks, no filler phrases, every file named in Execution Artifacts, every Markdown link resolving inside the skill, no symlinks, empty files or junk, a checker that exits 2 with no argument and repeats its result, and the "Illustrative example" label.
- `scripts/check-repo.py`: required files, version agreement across plugin.json, marketplace.json, CITATION.cff and CHANGELOG, plugin skill paths, installer bundles and docs, SHA-pinned actions, the owner rules in author docs, dashes, restricted names, secrets and junk in every file git would publish.
- `scripts/check-all.sh` (every check in CI order, with `--offline`, `--strict`, `--check-legal`, `--fast`), `scripts/regenerate.sh` (every writer, lock last) and a `.githooks/pre-commit` hook.
- `materialize-shared-references.py` reports orphan copies of shared references a skill no longer lists (`--prune` deletes them, `--check --strict` fails on them); `scripts/regenerate.sh --prune` runs it.
- `scripts/new-skill.py` scaffolds a skill that meets the layout and checker contract; `scripts/normalize-frontmatter.py` rewrites flow-style frontmatter lists as block lists without changing values.
- Installer: `cline`, `hermes` and `agents` (the shared `.agents/skills` folder) targets; multi-agent selection in the interactive mode; per-folder counts of skills already installed; `--update` (replace only changed skills), `--uninstall`, `--zip` (one zip per skill for the Claude apps), `--search`, descriptions in `--list`, comma lists for `--skill` and `--category`; a `skills.lock` check of every folder it writes; bundles `b2b-outbound`, `account-based` and `property-owners`.
- `generate-lock.py --verify --only <skills>`, and `--verify` now sets aside the `metadata.github-*` lines `gh skill install` writes, so gh installs verify.
- README: badges, a generated authorities table and a pitfalls count. AGENTS.md: a generated skill index. `taxonomy.csv`: version, description, related skills and shared references columns.
- Plugin manifests: `documentationUrl`, `supportUrl`, marketplace `category`, `tags` and `displayName`; skill counts in both descriptions are generated.
- CI: `claude plugin validate --strict`, `gh skill publish --dry-run` when the runner's GitHub CLI has it, `check-repo.py`, every installer target, bundle, update, uninstall and zip path on Linux and on macOS (bash 3.2), and a `regenerated-files` patch uploaded when a generated file is stale.
- `docs/REPO_TOPICS.md` with the 20 GitHub topics and the command to set them.

## 1.0.0 - 2026-10-13

First release. 31 skills in three categories.

- **scrapercity (8):** using-scrapercity-skills (router), scrapercity-mcp, scrapercity-cli, scrapercity-api, scrapercity-integrations, scrapercity-lead-database, scrapercity-local-business-database, scrapercity-real-estate-data.
- **list-building (12):** icp-list-builder, tam-builder, decision-maker-finder, account-researcher, local-business-list, cold-email-list, email-list-cleaner, crm-enricher, mobile-appender, ecommerce-by-techstack, skip-tracer, recruiting-sourcer. Full versions of the 12 short skills on scrapercity.com/skills.
- **outbound (11):** cold-email-strategy, cold-email-copywriting, reply-handling, multi-channel-outreach, domain-infrastructure, inbox-setup, email-deliverability, sending-platforms, cold-calling, signal-triggered-outbound, outbound-unit-economics.
- Shared references: tool and price catalog generated from the `scrapercity` npm package 1.0.17, platform facts, agent operating patterns, list quality standard, deliverability primer, outbound compliance primer, cold email frameworks, Alex Berman's cold email teachings.
- Tooling: skill validator, catalog sync with a check that the catalog matches the package, shared-reference materializer, README generator, `skills.lock` with SHA-256 per file, installer, Claude Code plugin and marketplace manifests, CI.
