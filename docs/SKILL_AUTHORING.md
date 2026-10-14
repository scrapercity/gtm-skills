# Skill Authoring Standard

Every skill in this repo meets this bar. `scripts/validate-skills.py` enforces the parts a script can check; reviewers enforce the rest. [QUALITY_BAR.md](QUALITY_BAR.md) is the acceptance list a reviewer works through.

## Owner rules

These two rules come from the repo owner (October 13, 2026) and override anything else in this repo.

1. **No legal content.** Skills, references, templates, worked examples and checker messages name no law, regulation, regulator, court ruling, fine, registry, consent requirement or registration requirement. They carry no disclaimers and never send the reader to get legal review. Leave a legal point out even when you are sure it is correct. Legal texts do not count as sources here ([SOURCE_STANDARDS.md](SOURCE_STANDARDS.md)).
2. **No moralizing.** A skill tells the reader what to do to get more replies, meetings and revenue at lower cost. Write a rule that changes results as a plain setting with its number: stop the sequence on reply; remove anyone who asks to be removed the same day; keep one suppression list; keep spam complaints under Google's 0.3% and bounces under 2%, because inbox placement drops past them; swap a caller ID number once carriers label it, because pickups collapse. Delete any rule you cannot tie to results. Leave out "reason" columns that argue a rule is right, and any framing about protecting the brand, respecting the prospect, not annoying people or safety.

`python3 scripts/validate-skills.py --check-legal` fails a skill that names a law, regulation or regulator, cites a CFR section, sends the reader to legal counsel, or adds a legal checkpoint. Reply-classification words for legal threats stay allowed in `reply-handling`, and law firms stay a normal prospecting vertical. Moralizing has no reliable pattern to match, so reviewers check it by reading.

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

`assets/` is also allowed for static files a deliverable embeds. Nothing else goes in a skill folder: no files at the skill root besides `SKILL.md`, no other top-level folders, no symlinks, no empty files, no `__pycache__` (`--strict` checks all of these).

Shared references live in the repo root `references/` and are listed in the skill's `metadata.shared_references`. `scripts/materialize-shared-references.py` copies them into each skill so a skill installed on its own still has every file it points to.

Start a new skill with `python3 scripts/new-skill.py <category> <name>`. It writes this layout with every section heading in order, a template, a worked example stub and a checker that already meets the contract below, so you fill content instead of copying another skill's structure.

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
  tags:
    - cold-email
    - sequences
  related_skills:
    - cold-email-copywriting
    - email-deliverability
  frameworks:
    - "Alex Berman - cold email offers and the short ask"
    - "Google - Email sender guidelines (2024)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
---
```

- `name` equals the folder name: 1 to 64 characters of `a-z`, `0-9` and single hyphens, without the words "claude" or "anthropic" ([Agent Skills specification](https://agentskills.io/specification), [Claude skill rules](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)).
- `description` is 80 to 1,024 characters, says what the skill produces, and contains "Use when" trigger language. No XML tags. Lead with the deliverable: Claude's help center lists 200 characters as the limit for a skill uploaded to the Claude apps, so the first sentence should stand alone.
- Only the spec's top-level keys (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`). Everything else goes under `metadata`.
- Write lists as block lists, one `- item` per line. The Agent Skills reference validator (`skills-ref`) rejects flow-style `[a, b]` lists; `python3 scripts/normalize-frontmatter.py` rewrites them without changing any value.
- `frameworks` names specific people, companies or standards. No anonymous "best practices".
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
9. **Common Pitfalls** - a table of mistake, why it fails, fix.
10. **Execution Artifacts** - every file in the skill and when to open it.
11. **Related Skills** - cross-links.

`SKILL.md` is 150 to 499 lines; the Agent Skills specification asks for under 500 because the agent loads all of it on activation. Skill-owned references total at least 250 lines. Long tables, libraries and scripts go in `references/`, so `SKILL.md` stays readable.

## What a deliverable must score

Write the Output Format and Quality Check so the deliverable would score 10 out of 10 with a blind expert on each of these:

| Criterion | A 10 looks like |
|-|-|
| Results | It would book more meetings or replies than what the user had. |
| Accuracy | No invented facts. Every number is sourced or labelled a planning assumption. |
| Actionability | A team can run it today: exact settings, sendable copy, owners, dates. |
| Fit | It answers the request the user made, within their constraints. |
| Economy | Every line does work. Framework lists, self-grading, tables of checks nobody ran, tool ids, repo paths, repeated rows and legal or moralizing text are padding and come out. |

## Checker contract

`scripts/check-output.py path/to/deliverable.md`:

- Uses only the Python standard library and makes no network calls.
- Prints `PASS - ...` and exits 0, or `FAIL - <reason>` and exits 1. Run with no argument, it prints usage and exits 2.
- Fails on the unfilled template (any `[fill]`, `[todo]` or `[tbd]` left in).
- Checks every required `##` heading of the template, a minimum length, populated tables, and at least two checks specific to the skill (for example: no email over 90 words, every lead row has a validation status, every touch has a branch).
- Passes on `examples/worked-example.md`, and gives the same result every run.

## Examples and sample data

- Label every worked example "Illustrative example" near the top.
- Invented businesses use `.example` domains, the name reserved for documentation by [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606) and [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761). Invented people get invented names; never paste a real person's contact record.
- API keys in examples are placeholders such as `your_key` or `$SCRAPERCITY_API_KEY`. `scripts/check-repo.py` and CI fail on anything shaped like a live key.
- Prices in an example come from the catalog and are worked through, so a reader can check units times price.

## Copy rules

These apply to every file, including code comments.

- No em dashes or en dashes. Use a hyphen, a comma, or rewrite the sentence.
- Plain, specific sentences. Leave out filler words such as "actually", "genuinely", "quietly", "cleanly", "crazy", "math", "shifted" and "matters" used as an importance announcer.
- Avoid "it's not X, it's Y" constructions, "the real X" framings, tidy summary closers and three-item rhetorical lists used for rhythm.
- Benchmarks are starting hypotheses with a source and a date, never promises.
- Quote sources sparingly: under 15 words, at most one quote per source, everything else paraphrased with a link.
- ScraperCity product names and tool ids come from `references/scrapercity-catalog.md` and `references/scrapercity-platform.md`. Never invent a tool, parameter, price or database size.
- Never name ScraperCity's suppliers or servers, or describe where its data comes from or how its backend works.
- Name the technology lookup "Tech Stack Search". Its tool id is `scrape_builtwith`.
- Alex Berman is ScraperCity's founder; his companies have booked 500,000+ meetings and send millions of cold emails a month. The 500,000 figure always counts meetings.

## Sources

Each reference file ends with a `## Sources` list of URLs. Prefer primary sources: mailbox providers (Google, Yahoo, Microsoft), RFCs and other published standards, vendor documentation, and the named operator's own published work. [SOURCE_STANDARDS.md](SOURCE_STANDARDS.md) scores sources and lists what does not count.

## Validation

```bash
python3 scripts/validate-skills.py                    # every skill
python3 scripts/validate-skills.py outbound           # one category
python3 scripts/validate-skills.py outbound/cold-calling
python3 scripts/validate-skills.py --strict           # adds the spec, link and package hygiene checks
python3 scripts/validate-skills.py --check-legal      # adds the owner rule 1 term check
node scripts/sync-catalog.mjs --check                 # prices and tools match the npm package
scripts/check-all.sh                                  # everything CI runs, in CI order
```
