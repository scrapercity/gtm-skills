# Skill Authoring Standard

Every skill in this repo meets this bar. `scripts/validate-skills.py` enforces the parts a script can check; reviewers enforce the rest.

## Folder layout

```text
skills/<category>/<skill-name>/
├── SKILL.md                     # entrypoint the agent loads
├── references/
│   ├── framework-notes.md       # which named sources shape this skill, and when to open each file
│   └── <topic>.md               # deep references: playbooks, tables, decision matrices, scripts
├── templates/
│   └── output-template.md       # the deliverable shell, every field marked [fill]
├── examples/
│   └── worked-example.md        # a complete, realistic deliverable that passes the checker
└── scripts/
    └── check-output.py          # deterministic checker for a finished deliverable
```

Shared references live in the repo root `references/` and are listed in the skill's `metadata.shared_references`. `scripts/materialize-shared-references.py` copies them into each skill so a skill installed on its own still has every file it points to.

## Frontmatter

```yaml
---
name: cold-email-strategy
description: >-
  Plans a cold email campaign from list to booked meeting. Use when the user
  asks for an outbound plan, a sequence, a cadence, or why replies are low.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [cold-email, sequences]
  related_skills: [cold-email-copywriting, email-deliverability]
  frameworks:
    - "Alex Berman - cold email offers and the short ask"
    - "Google - Email sender guidelines (2024)"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md]
---
```

- `name` equals the folder name.
- `description` is 80 to 1024 characters, says what the skill produces, and contains "Use when" trigger language.
- `frameworks` names real people, companies, standards or laws. No anonymous "best practices".
- `related_skills` only lists skills that exist in this repo.

## Body sections, in this order

1. **Overview** - what the skill produces and the mistake it prevents.
2. **When to Use** - trigger phrases and situations, plus which skill to use instead for nearby jobs.
3. **Prerequisites** (optional) - inputs to collect, or mark unknown.
4. **Authoritative Foundations** - the named sources and the principle each one contributes.
5. **Workflow** - numbered `###` steps the agent follows.
6. **ScraperCity Implementation** - the exact tools, parameters, CLI commands or API calls, with a worked cost estimate using prices from `references/scrapercity-catalog.md`. Show the count or estimate to the user before any paid pull.
7. **Output Format** - exactly what the user receives.
8. **Quality Check** - checkable acceptance criteria.
9. **Common Pitfalls** - mistake, why it fails, fix.
10. **Execution Artifacts** - every file in the skill and when to open it.
11. **Related Skills** - cross-links.

`SKILL.md` is at least 150 lines. Skill-owned references total at least 250 lines. Long tables, libraries and scripts go in `references/`, so `SKILL.md` stays readable.

## Checker contract

`scripts/check-output.py path/to/deliverable.md`:

- Uses only the Python standard library.
- Prints `PASS - ...` and exits 0, or `FAIL - <reason>` and exits 1 (2 for usage errors).
- Fails on the unfilled template (any `[fill]`, `[todo]` or `[tbd]` left in).
- Checks every required `##` heading of the template, a minimum length, populated tables, and at least two checks specific to the skill (for example: no email over 90 words, every lead row has a validation status, every touch has a branch).
- Passes on `examples/worked-example.md`.

## Copy rules

These apply to every file, including code comments.

- No em dashes or en dashes. Use a hyphen, a comma, or rewrite the sentence.
- Plain, specific sentences. No filler words such as "actually", "genuinely", "quietly", "cleanly", "crazy", and no "matters" as an importance announcer.
- No "it's not X, it's Y" constructions and no three-item rhetorical lists used for rhythm.
- Benchmarks are starting hypotheses with a source and a date, never promises.
- Quote sources sparingly: under 15 words, at most one quote per source, everything else paraphrased with a link.
- ScraperCity product names and tool ids come from `references/scrapercity-catalog.md` and `references/scrapercity-platform.md`. Never invent a tool, parameter, price or database size.
- Name the technology lookup "Tech Stack Search". Its tool id is `scrape_builtwith`.

## Sources

Each reference file ends with a `## Sources` list of URLs. Prefer primary sources: laws and regulators (FTC, FCC, CRTC, ICO), mailbox providers (Google, Yahoo, Microsoft), RFCs, vendor documentation, and the named operator's own published work.

## Validation

```bash
python3 scripts/validate-skills.py                    # every skill
python3 scripts/validate-skills.py outbound           # one category
python3 scripts/validate-skills.py outbound/cold-calling
node scripts/sync-catalog.mjs --check                 # prices and tools match the npm package
```
