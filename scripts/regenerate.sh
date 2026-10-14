#!/usr/bin/env bash
# Rewrite every generated file, in dependency order. Run after changing a skill or a shared reference.
#
#   scripts/regenerate.sh             materialize shared references, indexes, README/AGENTS/manifests, lock
#   scripts/regenerate.sh --catalog   also resync references/scrapercity-catalog.md from the npm package first
#   scripts/regenerate.sh --prune     also delete orphan copies of shared references a skill no longer lists
#
# skills.lock is written last because it hashes the output of every other step.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PRUNE=""
for a in "$@"; do
  case "$a" in
    --catalog) node scripts/sync-catalog.mjs ;;
    --prune) PRUNE="--prune" ;;
    -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $a" >&2; exit 2 ;;
  esac
done
# shellcheck disable=SC2086  # PRUNE is one flag or empty
python3 scripts/materialize-shared-references.py $PRUNE
python3 scripts/generate-indexes.py
python3 scripts/generate-readme.py
python3 scripts/generate-lock.py
