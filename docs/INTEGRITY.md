# Integrity

`skills.lock` records every file in every skill folder, so you can check that an installed copy matches what this repo published. This page explains the format, how to verify, and the limits of what a match tells you.

## Format

`skills.lock` is JSON, written by `scripts/generate-lock.py` with sorted keys and two-space indents.

| Key | Meaning |
|-|-|
| `schemaVersion` | Format version. `2` adds sizes, kinds and totals to the plain hashes of version 1. |
| `generatedFrom` | The git commit checked out when the lock was written. It is the parent of the commit that carries the lock. Omitted when the lock is written outside a git checkout. |
| `totals` | `skills`, `files` and `bytes` across every skill folder. |
| `kinds` | File count per kind: `skill entrypoint` (SKILL.md), `reference`, `template`, `example`, `script`. |
| `entries` | `<category>/<skill>` mapped to each file's relative path, with `sha256`, `size_bytes`, `kind`, and `shared: true` on a materialized copy of a repo-root shared reference. |

The lock holds no timestamp. The same tree always produces the same file, which is what lets `--check` run in CI. `--check` compares everything except `generatedFrom`, because committing the lock moves `HEAD` one commit past the one it names.

`__pycache__` folders and `.DS_Store` files are skipped.

## Verify an install

```bash
python3 scripts/generate-lock.py --verify ~/.claude/skills
python3 scripts/generate-lock.py --verify ./.agents/skills
python3 scripts/generate-lock.py --verify ~/.cursor/skills --only cold-calling,inbox-setup
```

`install.sh` runs the same check on every folder it writes, limited to the skills it just wrote, and prints `Verified:` or `MISMATCH:` per folder. It skips the check, and says so, when `python3` is missing or the checkout has edits the lock does not cover yet.

`--verify` reads `skills.lock` from your clone and checks each skill it finds in the folder. Skills not installed there are skipped, so a bundle install verifies too; `--only` narrows the check to named skills. It prints:

- `MISMATCH <skill>/<file>` when the file's SHA-256 differs from the lock.
- `MISSING <skill>/<file>` when a file in the lock is absent.
- `EXTRA <skill>/<file>` when a file is present that the lock does not list. This is informational and does not fail the run.

It exits 0 when every installed skill matches and 1 otherwise. Use a clone checked out at the same tag or commit you installed from; a newer clone has a newer lock.

## What a match proves

- Every file the lock lists for an installed skill is present and byte-for-byte identical to the file this repo hashed.
- No file was edited, truncated or swapped after it left the repo, by an installer, a sync tool or a person.
- The shared-reference copies inside a skill are the same bytes as the repo-root originals they were made from, as of that commit.

## What a match does not prove

- **Who wrote the lock.** The lock is unsigned. Anyone who can change the repo can change the files and the lock together. Trust comes from the repo itself: install from `github.com/scrapercity/gtm-skills` at a release tag, and check the tag's commit on GitHub.
- **That the content is correct.** A hash says the bytes are unchanged. It says nothing about whether a price or a sender rule is still current. That is the job of the validators, the catalog sync and [SOURCE_STANDARDS.md](SOURCE_STANDARDS.md).
- **That the checker scripts are safe to run.** Read `scripts/check-output.py` in any skill before you run it, as with any code. The checkers use only the Python standard library and make no network calls, which a reviewer can confirm in a few minutes.
- **That extra files are harmless.** `EXTRA` lines are reported and left alone. Delete files you did not expect.
- **That your agent loads the skill.** Placement and discovery are covered in [INSTALL.md](INSTALL.md).

## Known benign differences

- `gh skill install` adds `metadata.github-*` tracking lines to the frontmatter of each `SKILL.md` it installs. `--verify` sets those lines aside and compares the rest, printing `OK ... (matches once gh skill install's metadata.github-* lines are set aside)`. Any other change to the file still reports `MISMATCH`.
- Line-ending conversion (for example `core.autocrlf` on Windows) changes every text file's hash. Clone with `git -c core.autocrlf=false clone ...` before installing if you plan to verify.

## For maintainers

- Run `python3 scripts/generate-lock.py` last, after every other generator, because it hashes their output. It leaves `skills.lock` untouched when nothing but the commit has changed.
- CI runs `generate-lock.py --check` on every push and pull request, then installs every skill for every target into a temporary project on Linux and macOS, and the installer runs `--verify` against each folder.
- `scripts/regenerate.sh` runs every generator in order with the lock last; `scripts/check-all.sh` runs every check.
- Never edit `skills.lock` by hand.
