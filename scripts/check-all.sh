#!/usr/bin/env bash
# Run every check CI runs, in the same order, and report each one.
#
#   scripts/check-all.sh                 every check, including --strict and the legal-terms check
#   scripts/check-all.sh --offline       skip the catalog check that reads the npm registry
#   (--strict and --check-legal are accepted for compatibility; both are on by default)
#   scripts/check-all.sh --fast          skip the checker runs (frontmatter, files and copy rules only)
#
# Tools that are not installed (node, shellcheck, claude, agentskills) are reported as
# skipped, never as passed. Exit 1 when any check fails.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 2
OFFLINE=0; STRICT=1; LEGAL="--check-legal"; FAST=0
for a in "$@"; do
  case "$a" in
    --offline) OFFLINE=1 ;;
    --strict) STRICT=1 ;;
    --check-legal) LEGAL="--check-legal" ;;
    --fast) FAST=1 ;;
    -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $a" >&2; exit 2 ;;
  esac
done

failed=0; skipped=""
step() { # label command...
  local label="$1"; shift
  local out
  if out="$("$@" 2>&1)"; then
    printf 'PASS  %s\n' "$label"
  else
    printf 'FAIL  %s\n' "$label"
    printf '%s\n' "$out" | grep -vE '^PASS ' | sed 's/^/      /' | head -40
    failed=$((failed + 1))
  fi
}
skip() { printf 'SKIP  %s (%s)\n' "$1" "$2"; skipped="$skipped $1"; }

step "Python files compile" python3 - <<'PY'
import pathlib, py_compile, sys, tempfile
root = pathlib.Path(".")
bad = 0
with tempfile.TemporaryDirectory() as tmp:
    for p in sorted(root.rglob("*.py")):
        if ".git" in p.parts:
            continue
        try:
            py_compile.compile(str(p), cfile=str(pathlib.Path(tmp) / "x.pyc"), doraise=True)
        except py_compile.PyCompileError as exc:
            print(exc); bad += 1
sys.exit(1 if bad else 0)
PY
if command -v node >/dev/null 2>&1; then
  step "Node modules parse" node --check scripts/sync-catalog.mjs
else
  skip "Node modules parse" "node not installed"
fi

if [ "$FAST" -eq 1 ]; then
  skip "Skill validator" "--fast"
else
  if [ "$STRICT" -eq 1 ]; then
    # shellcheck disable=SC2086  # LEGAL is one flag or empty
    step "Skill validator (--strict)" python3 scripts/validate-skills.py --strict $LEGAL
  else
    # shellcheck disable=SC2086
    step "Skill validator" python3 scripts/validate-skills.py $LEGAL
  fi
fi
# shellcheck disable=SC2086
step "Repo checks" python3 scripts/check-repo.py $LEGAL
step "Shared reference copies current" python3 scripts/materialize-shared-references.py --check
step "Pitfalls index and taxonomy current" python3 scripts/generate-indexes.py --check
step "README, AGENTS.md and manifests current" python3 scripts/generate-readme.py --check
step "skills.lock current" python3 scripts/generate-lock.py --check

if [ "$OFFLINE" -eq 1 ]; then
  skip "Catalog matches the npm package" "--offline"
elif command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
  step "Catalog matches the npm package" node scripts/sync-catalog.mjs --check
else
  skip "Catalog matches the npm package" "node or npm not installed"
fi

if command -v shellcheck >/dev/null 2>&1; then
  step "Shell scripts pass shellcheck" shellcheck install.sh scripts/check-all.sh scripts/regenerate.sh .githooks/pre-commit
else
  skip "Shell scripts pass shellcheck" "shellcheck not installed"
fi

if command -v claude >/dev/null 2>&1; then
  step "Plugin and marketplace manifests (claude plugin validate --strict)" claude plugin validate . --strict
else
  skip "Plugin and marketplace manifests" "claude not installed"
fi

if [ "$STRICT" -eq 1 ]; then
  if command -v agentskills >/dev/null 2>&1; then
    spec_check() { local d rc=0; for d in skills/*/*/; do agentskills validate "$d" >/dev/null 2>&1 || { echo "invalid: $d"; rc=1; }; done; return "$rc"; }
    step "Agent Skills reference validator (skills-ref)" spec_check
  else
    skip "Agent Skills reference validator" "pip install skills-ref"
  fi
fi

echo
if [ "$failed" -gt 0 ]; then
  echo "$failed check(s) failed.${skipped:+ Skipped:$skipped.}"
  exit 1
fi
echo "All checks passed.${skipped:+ Skipped:$skipped.}"
