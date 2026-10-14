# Quality Bar

The minimum every skill in `skills/` meets before it merges. [SKILL_AUTHORING.md](SKILL_AUTHORING.md) explains how to write a skill; this page is the acceptance list a reviewer works through. The "Checked by" column says whether `scripts/validate-skills.py` enforces the line (by default, with `--strict`, or with `--check-legal`) or a reviewer has to.

## Owner rules

| Requirement | Checked by |
|-|-|
| **No legal content.** No law, regulation, regulator, court ruling, fine, registry, consent or registration requirement, disclaimer, or advice to get legal review, anywhere in the skill folder, even when correct | `--check-legal` (the `LEGAL_TERMS` list in `validate-skills.py`), reviewer (everything else) |
| **No moralizing.** Every rule is a setting tied to replies, meetings, revenue or cost, with its number. No "reason" columns arguing a rule is right; no brand, respect, annoyance or safety framing. A rule that cannot be tied to results is deleted | reviewer |

## Files

| Requirement | Checked by |
|-|-|
| `SKILL.md`, `references/framework-notes.md`, `templates/output-template.md`, `examples/worked-example.md`, `scripts/check-output.py` all exist | validator |
| At least one skill-owned reference beyond `framework-notes.md` | reviewer |
| Skill-owned references total 250 lines or more (shared copies do not count) | validator |
| `SKILL.md` is 150 lines or more, and under 500 | validator, `--strict` |
| Every `references/`, `templates/`, `scripts/` or `examples/` path named in backticks in `SKILL.md` exists | validator |
| Every Markdown link in the skill resolves to a file inside the skill folder | `--strict` |
| Every shared reference the skill uses is listed in `metadata.shared_references` and materialized | validator and `materialize-shared-references.py --check` |
| Only `SKILL.md` at the skill root; only `references/`, `templates/`, `examples/`, `scripts/` and `assets/` below it; no symlinks, empty files or cache and editor junk | `--strict` |
| Every file in the skill is named in Execution Artifacts, except materialized shared copies; no orphan copy of a shared reference the skill no longer lists | `--strict`, `materialize-shared-references.py --check --strict` |

## Frontmatter

| Requirement | Checked by |
|-|-|
| `name` equals the folder name; 1 to 64 characters of `a-z`, `0-9` and single hyphens; no "claude" or "anthropic"; unique across categories | validator, `--strict` |
| `description` is 80 to 1,024 characters, says what the skill produces, includes "Use when" triggers, and has no XML tags | validator (length, trigger phrase), `--strict` (tags), reviewer (content) |
| Only the Agent Skills top-level keys; lists in block style so the `skills-ref` reference validator accepts the file | `--strict` |
| `license: MIT`, `compatibility` present and under 500 characters | validator |
| `metadata.author: ScraperCity`, `metadata.category` equals the category folder, `metadata.version` is semver | validator |
| `metadata.tags`, `metadata.related_skills` and `metadata.frameworks` are non-empty lists | validator |
| Every related skill exists in this repo | validator |
| At least 3 distinct frameworks, each naming a person, company or standard, with a year where one applies | `--strict` (count), reviewer (content) |

## Body

| Requirement | Checked by |
|-|-|
| These `##` sections appear once each (`--strict`), in this order: Overview, When to Use, Authoritative Foundations, Workflow, ScraperCity Implementation, Output Format, Quality Check, Common Pitfalls, Execution Artifacts, Related Skills | validator |
| Workflow steps are numbered `###` headings an agent can follow without guessing | reviewer |
| ScraperCity Implementation names exact tool ids or commands from `references/scrapercity-catalog.md` and works one cost estimate with catalog prices | reviewer (`taxonomy.csv` lists the tools and prices each skill names) |
| Any paid pull shows the count or estimate to the user and checks the wallet first | reviewer |
| Output Format and Quality Check drive a deliverable that scores 10 on results, accuracy, actionability, fit and economy ([SKILL_AUTHORING.md](SKILL_AUTHORING.md#what-a-deliverable-must-score)) | reviewer |
| Quality Check items are pass or fail, not judgment calls | reviewer |
| Common Pitfalls is a table of mistake, why it fails, and fix. Every row appears in `references/pitfalls-index.md` | reviewer, `generate-indexes.py --check` |
| Benchmarks are labelled as planning assumptions with a source and a date | reviewer |

## Sources

Every reference file ends with a `## Sources` list. Each source meets [SOURCE_STANDARDS.md](SOURCE_STANDARDS.md): primary where one exists, dated where the fact can change. A new fact without a source does not merge.

## Public copy rules

| Requirement | Checked by |
|-|-|
| No em or en dashes in any packaged text file or repo doc | validator, `check-repo.py` |
| No restricted names (a hashed list in the validator) | validator, `check-repo.py` |
| The technology lookup is called Tech Stack Search in prose; only the tool id `scrape_builtwith` and the CLI command keep the old name | validator |
| No filler words or rhetorical constructions listed in SKILL_AUTHORING.md | `--strict` (the `SLOP` list in `SKILL.md`), reviewer |
| No invented tool, parameter, price or database size | reviewer, catalog sync |
| Worked examples carry the "Illustrative example" label and use `.example` domains for invented businesses | `--strict` (label), reviewer (domains) |

## The checker contract

`scripts/check-output.py` is the skill's own test. The validator runs it on every skill: on the unfilled template, where it must exit non-zero, and on the worked example, where it must exit 0. `--strict` also runs it with no argument (exit 2) and twice on the example (same result both times).

A checker:

1. Takes one argument, the path of a finished deliverable, and runs as `python3 -I check-output.py <file>`.
2. Imports only the Python standard library and makes no network calls.
3. Prints one line starting `PASS - ` and exits 0, or prints `FAIL - <reason>` lines and exits 1. A usage error exits 2.
4. Fails on any `[fill]`, `[todo]` or `[tbd]` marker left in the file.
5. Fails when a required `##` heading of the template is missing.
6. Fails below a minimum length and on empty tables.
7. Runs at least two checks specific to the skill, for example an email body over 90 words, a cost line where units times price does not equal the total, or a phone row with no line type.
8. Gives the same result on the same file every time. It reads the file it was given and nothing else.

A checker that only counts headings does not meet the bar. Reviewers read each checker and try one broken deliverable against it.

## Before you request review

```bash
scripts/check-all.sh --offline     # every offline check CI runs
# or one at a time:
python3 scripts/validate-skills.py <category>/<skill> --strict --check-legal
python3 scripts/materialize-shared-references.py --check
scripts/regenerate.sh              # rewrites the indexes, README blocks and skills.lock
```
