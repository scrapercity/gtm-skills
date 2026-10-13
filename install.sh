#!/usr/bin/env bash
# Install ScraperCity GTM skills into an agent's skills folder.
#
#   ./install.sh                              all skills into ~/.claude/skills
#   ./install.sh --scope project              into ./.claude/skills of the current directory
#   ./install.sh --dest ~/.codex/skills       any folder an agent reads skills from
#   ./install.sh --category outbound          one category (outbound, list-building, scrapercity)
#   ./install.sh --skill cold-calling         one skill (repeat the flag for more)
#   ./install.sh --dry-run                    print what would be copied, write nothing
#   ./install.sh --force                      replace skill folders that already exist
#   ./install.sh --list                       list every skill and exit
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCOPE="user"
DEST=""
CATEGORY=""
SKILLS=()
DRY=0
FORCE=0

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --scope) SCOPE="${2:?--scope needs user or project}"; shift 2 ;;
    --dest) DEST="${2:?--dest needs a folder}"; shift 2 ;;
    --category) CATEGORY="${2:?--category needs a name}"; shift 2 ;;
    --skill) SKILLS+=("${2:?--skill needs a name}"); shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --force) FORCE=1; shift ;;
    --list)
      for d in "$REPO"/skills/*/*/; do d="${d%/}"; printf '%-14s %s\n' "$(basename "$(dirname "$d")")" "$(basename "$d")"; done
      exit 0 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ -z "$DEST" ]; then
  case "$SCOPE" in
    user) DEST="$HOME/.claude/skills" ;;
    project) DEST="$PWD/.claude/skills" ;;
    *) echo "--scope must be user or project" >&2; exit 2 ;;
  esac
fi

if [ -n "$CATEGORY" ] && [ ! -d "$REPO/skills/$CATEGORY" ]; then
  echo "No category named $CATEGORY. Categories: $(ls "$REPO/skills" | tr '\n' ' ')" >&2
  exit 2
fi

selected=()
for d in "$REPO"/skills/*/*/; do
  d="${d%/}"
  name="$(basename "$d")"
  cat="$(basename "$(dirname "$d")")"
  [ -f "$d/SKILL.md" ] || continue
  [ -n "$CATEGORY" ] && [ "$cat" != "$CATEGORY" ] && continue
  if [ ${#SKILLS[@]} -gt 0 ]; then
    keep=0
    for s in "${SKILLS[@]}"; do [ "$s" = "$name" ] && keep=1; done
    [ $keep -eq 1 ] || continue
  fi
  selected+=("$d")
done

if [ ${#SKILLS[@]} -gt 0 ]; then
  for s in "${SKILLS[@]}"; do
    found=0
    for d in "${selected[@]:-}"; do [ "$(basename "$d")" = "$s" ] && found=1; done
    [ $found -eq 1 ] || { echo "No skill named $s (run ./install.sh --list)" >&2; exit 2; }
  done
fi

if [ ${#selected[@]} -eq 0 ]; then
  echo "Nothing selected." >&2
  exit 2
fi

echo "Destination: $DEST"
[ $DRY -eq 1 ] && echo "Dry run: nothing will be written."
copied=0; skipped=0
for d in "${selected[@]}"; do
  name="$(basename "$d")"
  target="$DEST/$name"
  if [ -e "$target" ] && [ $FORCE -eq 0 ]; then
    echo "  skip     $name (exists; use --force to replace)"
    skipped=$((skipped + 1))
    continue
  fi
  echo "  install  $name"
  if [ $DRY -eq 0 ]; then
    mkdir -p "$DEST"
    [ -e "$target" ] && rm -rf -- "$target"
    cp -R "$d" "$target"
  fi
  copied=$((copied + 1))
done
echo "Done: $copied installed, $skipped skipped."
echo "Next: connect ScraperCity (see README, 'Connect ScraperCity'), then ask your agent to load using-scrapercity-skills."
