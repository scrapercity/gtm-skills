# Release Process

A release is a git tag on `main` that people and the Claude Code plugin can pin to. This page lists the steps in order. Do not skip one because the previous release went fine.

## Owner rules gate every release

Two rules from the repo owner (October 13, 2026) apply to everything a release ships:

- **No legal content.** No law, regulation, regulator, fine, registry, consent or registration requirement, disclaimer or advice to get legal review in any skill. Run `python3 scripts/validate-skills.py --check-legal` before tagging; it must print no legal-term lines.
- **No moralizing.** Every rule in a skill is a setting tied to replies, meetings, revenue or cost. Read the diff for "reason" columns, brand or respect framing, and gates justified as good behavior, and cut them before tagging.

## Version numbers

Releases follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html): `MAJOR.MINOR.PATCH`.

| Bump | When | Examples |
|-|-|-|
| MAJOR | A change that can break an existing install or a script that depends on the repo | A skill removed or renamed, a category renamed, an `install.sh` flag removed or its meaning changed, a target folder changed, a `skills.lock` schema change that drops a key, a checker's PASS rule tightened so a deliverable that used to pass now fails |
| MINOR | New capability that leaves existing installs working | A new skill, a new bundle or target, a new section or reference in a skill, a new optional flag, a new key in `skills.lock` or a new column in `taxonomy.csv` |
| PATCH | Corrections only | A wrong fact fixed, a stale price resynced from the catalog, a copy edit, a checker bug fixed without changing what passes |

Each skill also carries `metadata.version`. Bump it by the same rule when that skill's content changes. The repo version moves at least as far as the largest skill bump in the release.

## Steps

### 1. Start from a green `main`

```bash
git switch main && git pull --ff-only
git status            # nothing uncommitted
```

The latest `validate` workflow run on `main` must be green, including the weekly scheduled run that checks the catalog against the npm package.

### 2. Run every check locally

```bash
scripts/check-all.sh --strict --check-legal
```

That one command runs, in CI order: Python and Node syntax, the skill validator with the strict and legal checks, `check-repo.py` (versions, manifests, installer docs, workflow pins, owner rules, copy rules, secrets), the shared-reference, index, README and lock checks, the catalog check against npm, shellcheck, `claude plugin validate . --strict` and the `skills-ref` validator. A check whose tool is missing prints SKIP; install the tool and rerun until nothing is skipped. Fix any failure on `main` before going further.

### 3. Bump the version in four places

- `.claude-plugin/plugin.json`: `version`. Claude Code keeps plugin users on this version until it changes.
- `.claude-plugin/marketplace.json`: the plugin entry's `version`.
- `CITATION.cff`: `version` and `date-released`.
- `CHANGELOG.md`: rename `## Unreleased` to `## X.Y.Z - YYYY-MM-DD`, listing added, changed, fixed and removed items and naming each skill touched.

`scripts/check-repo.py` fails until all four agree. Then regenerate and commit as `Release X.Y.Z`:

```bash
scripts/regenerate.sh
scripts/check-all.sh
```

### 4. Tag the release commit

After the release commit is on `main` and its CI run is green:

```bash
git switch main && git pull --ff-only
git tag -a vX.Y.Z -m "gtm-skills X.Y.Z"
git push origin vX.Y.Z
```

Then publish a GitHub release from the tag and paste that version's CHANGELOG section as the notes. Attach the per-skill zips for Claude app users:

```bash
./install.sh --zip "dist/gtm-skills-X.Y.Z"
```

### 5. Verify from a fresh clone

In a new temporary folder, clone the tag and repeat the checks and an install:

```bash
git clone --depth 1 --branch vX.Y.Z https://github.com/scrapercity/gtm-skills.git
cd gtm-skills
scripts/check-all.sh --offline
tmp="$(mktemp -d)" && ./install.sh --target all --scope project --project-dir "$tmp" --yes
```

The installer verifies every folder it wrote against `skills.lock` and prints `Verified:` per folder. Then, in Claude Code, run `/plugin marketplace update scrapercity` and confirm `gtm-skills` shows the new version and one skill loads as `gtm-skills:<name>`.

If any step fails, fix it on `main` and cut a new PATCH release. Never move or delete a published tag.

## Hotfixes

A wrong price, a wrong tool id, or any legal or moralizing text found in a released skill ships as a PATCH release the same day, with the CHANGELOG entry naming the file, the wrong text and the source for the fix.
