#!/usr/bin/env bash
# Install ScraperCity GTM skills into an agent's skills folder.
#
#   ./install.sh                                interactive in a terminal; otherwise every skill into ~/.claude/skills
#   ./install.sh --target codex                 one agent: claude codex copilot cursor gemini opencode windsurf goose cline hermes agents
#   ./install.sh --target all --yes             every agent above, no confirmation prompt
#   ./install.sh --target cursor,gemini         a comma list, or repeat --target
#   ./install.sh --scope project                the project folder instead of your home folder
#   ./install.sh --project-dir ~/code/app       project root for --scope project (default: current directory)
#   ./install.sh --dest ~/my-agent/skills       any folder an agent reads skills from (overrides --target)
#   ./install.sh --bundle email-from-zero       a named bundle (comma list or repeat; see --list-bundles)
#   ./install.sh --category outbound            a category (outbound, list-building, scrapercity; comma list or repeat)
#   ./install.sh --skill cold-calling           a skill (comma list or repeat)
#   ./install.sh --update                       replace installed skills that differ from this checkout, add missing ones
#   ./install.sh --force                        replace every selected skill folder that already exists
#   ./install.sh --uninstall                    remove the selected skills from the destination folders
#   ./install.sh --zip ~/Downloads/skills       write one .zip per skill for upload to the Claude apps
#   ./install.sh --dry-run                      print the plan, write nothing
#   ./install.sh --yes                          skip the confirmation prompt
#   ./install.sh --no-verify                    skip the skills.lock check after installing
#   ./install.sh --list                         list every skill with what it does, then exit
#   ./install.sh --search <word>                list skills whose name or description contains a word, then exit
#   ./install.sh --list-bundles                 list every bundle and exit
#   ./install.sh --list-targets                 print each target's user and project folders and exit
#
# Folders per target are documented, with the official source for each, in docs/INSTALL.md.
# Written for bash 3.2 (the macOS default) and later.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ALL_TARGETS="claude codex copilot cursor gemini opencode windsurf goose cline hermes agents"
BUNDLES="local-outbound b2b-outbound account-based email-from-zero calling property-owners list-core platform"
HELP_LINES=27

SCOPE="user"
SCOPE_SET=0
DEST=""
ZIP_DIR=""
PROJECT_DIR="$PWD"
CATEGORIES=""
TARGETS=""
SKILLS=""
BUNDLE_LIST=""
MODE="install"   # install | update | uninstall | zip
DRY=0
FORCE=0
YES=0
VERIFY=1

usage() { sed -n "2,${HELP_LINES}p" "$0" | sed 's/^# \{0,1\}//'; }
die() { echo "$*" >&2; exit 2; }

bundle_skills() {
  case "$1" in
    local-outbound) echo "local-business-list cold-email-strategy cold-email-copywriting reply-handling" ;;
    b2b-outbound) echo "icp-list-builder cold-email-list cold-email-strategy cold-email-copywriting reply-handling" ;;
    account-based) echo "account-researcher decision-maker-finder signal-triggered-outbound multi-channel-outreach" ;;
    email-from-zero) echo "domain-infrastructure inbox-setup email-deliverability sending-platforms" ;;
    calling) echo "mobile-appender cold-calling multi-channel-outreach" ;;
    property-owners) echo "scrapercity-real-estate-data skip-tracer mobile-appender multi-channel-outreach" ;;
    list-core) echo "icp-list-builder tam-builder cold-email-list email-list-cleaner" ;;
    platform)
      local out="" d
      for d in "$REPO"/skills/scrapercity/*/; do [ -f "$d/SKILL.md" ] && out="$out $(basename "$d")"; done
      echo "${out# }" ;;
    *) return 1 ;;
  esac
}

bundle_about() {
  case "$1" in
    local-outbound) echo "local business list to replies" ;;
    b2b-outbound) echo "B2B contacts like your best customers, to replies" ;;
    account-based) echo "buyers at named accounts, triggers and multichannel touches" ;;
    email-from-zero) echo "a cold email sending setup from zero" ;;
    calling) echo "mobile numbers and a calling program" ;;
    property-owners) echo "property owner lists with phones and outreach" ;;
    list-core) echo "B2B list building and list hygiene" ;;
    platform) echo "the ScraperCity platform skills and the router" ;;
  esac
}

target_dir() { # target scope -> folder
  local base="$HOME"
  [ "$2" = "project" ] && base="$PROJECT_DIR"
  case "$1:$2" in
    claude:*) echo "$base/.claude/skills" ;;
    codex:*|goose:*|agents:*) echo "$base/.agents/skills" ;;
    copilot:user) echo "$base/.copilot/skills" ;;
    copilot:project) echo "$base/.github/skills" ;;
    cursor:*) echo "$base/.cursor/skills" ;;
    gemini:*) echo "$base/.gemini/skills" ;;
    opencode:user) echo "$base/.config/opencode/skills" ;;
    opencode:project) echo "$base/.opencode/skills" ;;
    windsurf:user) echo "$base/.codeium/windsurf/skills" ;;
    windsurf:project) echo "$base/.windsurf/skills" ;;
    cline:*) echo "$base/.cline/skills" ;;
    hermes:*) echo "$base/.hermes/skills" ;;
    *) return 1 ;;
  esac
}

in_list() { # word list
  local w
  for w in $2; do [ "$w" = "$1" ] && return 0; done
  return 1
}

add_targets() {
  local t
  for t in $(echo "$1" | tr ',' ' '); do
    if [ "$t" = "all" ]; then
      TARGETS="$ALL_TARGETS"
    elif in_list "$t" "$ALL_TARGETS"; then
      in_list "$t" "$TARGETS" || TARGETS="$TARGETS $t"
    else
      die "Unknown target: $t. Targets: $ALL_TARGETS all"
    fi
  done
}

# Prints the description from a SKILL.md frontmatter on one line (folded or plain scalar).
describe() {
  awk '
    NR == 1 && $0 != "---" { exit }
    NR > 1 && $0 == "---" { exit }
    folded { if ($0 ~ /^[ \t]+/) { sub(/^[ \t]+/, ""); printf "%s ", $0; next } else exit }
    /^description:/ {
      sub(/^description:[ \t]*/, "")
      if ($0 ~ /^[>|][-+]?$/) { folded = 1; next }
      gsub(/^["\047]|["\047]$/, ""); print; exit
    }' "$1" | sed 's/[[:space:]]*$//'
}

first_sentence() { sed 's/\([.!?]\) .*/\1/'; }

list_skills() { # [word] -> category, name, first sentence
  local d word="${1:-}" desc hay
  for d in "$REPO"/skills/*/*/; do
    d="${d%/}"
    [ -f "$d/SKILL.md" ] || continue
    desc="$(describe "$d/SKILL.md")"
    if [ -n "$word" ]; then
      hay="$(printf '%s %s' "$(basename "$d")" "$desc" | tr '[:upper:]' '[:lower:]')"
      case "$hay" in *"$(printf '%s' "$word" | tr '[:upper:]' '[:lower:]')"*) ;; *) continue ;; esac
    fi
    printf '%-13s %-36s %s\n' "$(basename "$(dirname "$d")")" "$(basename "$d")" "$(printf '%s' "$desc" | first_sentence | cut -c1-110)"
  done
  return 0
}

skill_count() { list_skills | wc -l | tr -d ' '; }

# ---------------------------------------------------------------- interactive mode
tty_read() { # prompt default -> REPLY_VAL
  local ans=""
  printf '%s' "$1" > /dev/tty
  IFS= read -r ans < /dev/tty || ans=""
  [ -z "$ans" ] && ans="$2"
  REPLY_VAL="$ans"
}

# pick title default multi option... -> PICKED (space-separated first words of the chosen options)
pick() {
  local title="$1" def="$2" multi="$3" i n ok choice
  shift 3
  n=$#
  while :; do
    printf '\n%s\n' "$title" > /dev/tty
    i=1
    for opt in "$@"; do printf '  %2d) %s\n' "$i" "$opt" > /dev/tty; i=$((i + 1)); done
    if [ "$multi" = 1 ]; then
      tty_read "Choose one or more, for example 1,3 [$def]: " "$def"
    else
      tty_read "Choose 1-$n [$def]: " "$def"
    fi
    PICKED=""; ok=1
    for choice in $(echo "$REPLY_VAL" | tr ',' ' '); do
      case "$choice" in ''|*[!0-9]*) ok=0; break ;; esac
      if [ "$choice" -lt 1 ] || [ "$choice" -gt "$n" ]; then ok=0; break; fi
      i=1
      for opt in "$@"; do
        [ "$i" -eq "$choice" ] && PICKED="$PICKED ${opt%% *}"
        i=$((i + 1))
      done
    done
    if [ "$ok" = 1 ] && [ -n "$PICKED" ] && { [ "$multi" = 1 ] || [ "$(echo "$PICKED" | wc -w | tr -d ' ')" = 1 ]; }; then
      PICKED="${PICKED# }"
      return 0
    fi
    printf 'Enter %s from 1 to %d.\n' "$([ "$multi" = 1 ] && echo 'numbers' || echo 'a number')" "$n" > /dev/tty
  done
}

interactive() {
  printf 'ScraperCity GTM skills installer\n' > /dev/tty
  local t b c
  set --
  for t in $ALL_TARGETS; do
    set -- "$@" "$(printf '%-9s %-28s %s' "$t" "$(target_dir "$t" user | sed "s#^$HOME#~#")" "$(target_dir "$t" project | sed "s#^$PROJECT_DIR/##")")"
  done
  set -- "$@" "$(printf '%-9s %s' all 'every agent above')"
  pick "Which agents?            user folder                  project folder" 1 1 "$@"
  add_targets "$(echo "$PICKED" | tr ' ' ',')"
  pick "Which scope?" 1 0 "$(printf '%-9s %s' user 'your home folder, every project on this machine')" "$(printf '%-9s %s' project "$PROJECT_DIR")"
  SCOPE="$PICKED"
  set -- "$(printf '%-16s %s' all "every skill ($(skill_count))")"
  for b in $BUNDLES; do set -- "$@" "$(printf '%-16s %s: %s' "$b" "$(bundle_about "$b")" "$(bundle_skills "$b")")"; done
  for c in "$REPO"/skills/*/; do
    c="$(basename "$c")"
    set -- "$@" "$(printf '%-16s category: %s skills' "$c" "$(find "$REPO/skills/$c" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')")"
  done
  pick "Which skills? Bundles and categories combine." 1 1 "$@"
  in_list all "$PICKED" && return 0
  for b in $PICKED; do
    if [ -d "$REPO/skills/$b" ]; then CATEGORIES="$CATEGORIES $b"; else BUNDLE_LIST="$BUNDLE_LIST $b"; fi
  done
  return 0
}

# ---------------------------------------------------------------- arguments
NARGS=$#
while [ $# -gt 0 ]; do
  case "$1" in
    --target) add_targets "${2:?--target needs a name}"; shift 2 ;;
    --target=*) add_targets "${1#*=}"; shift ;;
    --scope) SCOPE="${2:?--scope needs user or project}"; SCOPE_SET=1; shift 2 ;;
    --scope=*) SCOPE="${1#*=}"; SCOPE_SET=1; shift ;;
    --project-dir) PROJECT_DIR="${2:?--project-dir needs a folder}"; shift 2 ;;
    --project-dir=*) PROJECT_DIR="${1#*=}"; shift ;;
    --dest) DEST="${2:?--dest needs a folder}"; shift 2 ;;
    --dest=*) DEST="${1#*=}"; shift ;;
    --category) CATEGORIES="$CATEGORIES $(echo "${2:?--category needs a name}" | tr ',' ' ')"; shift 2 ;;
    --category=*) CATEGORIES="$CATEGORIES $(echo "${1#*=}" | tr ',' ' ')"; shift ;;
    --skill) SKILLS="$SKILLS $(echo "${2:?--skill needs a name}" | tr ',' ' ')"; shift 2 ;;
    --skill=*) SKILLS="$SKILLS $(echo "${1#*=}" | tr ',' ' ')"; shift ;;
    --bundle) BUNDLE_LIST="$BUNDLE_LIST $(echo "${2:?--bundle needs a name}" | tr ',' ' ')"; shift 2 ;;
    --bundle=*) BUNDLE_LIST="$BUNDLE_LIST $(echo "${1#*=}" | tr ',' ' ')"; shift ;;
    --update) MODE="update"; shift ;;
    --uninstall) MODE="uninstall"; shift ;;
    --zip) MODE="zip"; ZIP_DIR="${2:?--zip needs a folder}"; shift 2 ;;
    --zip=*) MODE="zip"; ZIP_DIR="${1#*=}"; shift ;;
    --dry-run) DRY=1; shift ;;
    --force) FORCE=1; shift ;;
    --no-verify) VERIFY=0; shift ;;
    -y|--yes) YES=1; shift ;;
    --list) list_skills; exit 0 ;;
    --search) list_skills "${2:?--search needs a word}"; exit 0 ;;
    --search=*) list_skills "${1#*=}"; exit 0 ;;
    --list-bundles)
      for b in $BUNDLES; do printf '%-16s %s\n%-16s %s\n' "$b" "$(bundle_about "$b")" "" "$(bundle_skills "$b")"; done
      exit 0 ;;
    --list-targets)
      printf '%-9s %-34s %s\n' target user project
      for t in $ALL_TARGETS; do printf '%-9s %-34s %s\n' "$t" "$(target_dir "$t" user | sed "s#^$HOME#~#")" "$(target_dir "$t" project | sed "s#^$PROJECT_DIR/##")"; done
      exit 0 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$SCOPE" in user|project) ;; *) die "--scope must be user or project" ;; esac
[ "$MODE" = "update" ] && [ "$FORCE" -eq 1 ] && die "--update and --force do different things; pick one."
[ "$SCOPE" = "project" ] && { [ -d "$PROJECT_DIR" ] || die "Project folder not found: $PROJECT_DIR"; PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"; }

if [ "$NARGS" -eq 0 ] && [ -t 0 ] && [ -t 1 ] && [ -r /dev/tty ]; then
  interactive
fi

if [ -n "$DEST" ] && [ -n "$TARGETS" ]; then
  echo "Note: --dest overrides --target; using only $DEST" >&2
fi
if [ -n "$DEST" ] && [ "$SCOPE_SET" -eq 1 ]; then
  echo "Note: --dest overrides --scope" >&2
fi
[ -z "$TARGETS" ] && TARGETS="claude"

for c in $CATEGORIES; do
  # shellcheck disable=SC2012  # category folder names are plain words
  [ -d "$REPO/skills/$c" ] || die "No category named $c. Categories: $(ls "$REPO/skills" | tr "\n" " " | sed "s/ $//")"
done

for b in $BUNDLE_LIST; do
  bs="$(bundle_skills "$b")" || die "No bundle named $b. Bundles: $BUNDLES"
  SKILLS="$SKILLS $bs"
done

# ---------------------------------------------------------------- select skills
# A skill is selected when it matches a named skill or bundle, or sits in a named category.
# With none of the three, every skill is selected.
SELECTED=""   # newline-separated skill folders
COUNT=0
for d in "$REPO"/skills/*/*/; do
  d="${d%/}"
  name="$(basename "$d")"
  cat="$(basename "$(dirname "$d")")"
  [ -f "$d/SKILL.md" ] || continue
  if [ -n "$SKILLS$CATEGORIES" ] && ! in_list "$name" "$SKILLS" && ! in_list "$cat" "$CATEGORIES"; then continue; fi
  SELECTED="$SELECTED$d
"
  COUNT=$((COUNT + 1))
done

for s in $SKILLS; do
  printf '%s' "$SELECTED" | grep -q "/$s\$" || die "No skill named $s (run ./install.sh --list or --search <word>)"
done

[ "$COUNT" -eq 0 ] && die "Nothing selected."

# ---------------------------------------------------------------- zip mode
if [ "$MODE" = "zip" ]; then
  echo "Skills:       $COUNT"
  echo "Zip folder:   $ZIP_DIR"
  [ "$DRY" -eq 1 ] && echo "Dry run: nothing will be written."
  if [ "$DRY" -eq 0 ]; then
    mkdir -p "$ZIP_DIR"
    ZIP_DIR="$(cd "$ZIP_DIR" && pwd)"
    command -v zip >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1 || die "--zip needs zip or python3 on PATH."
  fi
  made=0; long=0
  OLDIFS="$IFS"; IFS='
'
  for d in $SELECTED; do
    IFS="$OLDIFS"
    name="$(basename "$d")"
    out="$ZIP_DIR/$name.zip"
    len="$(describe "$d/SKILL.md" | wc -c | tr -d ' ')"
    [ "$len" -gt 201 ] && long=$((long + 1))
    if [ "$DRY" -eq 0 ]; then
      rm -f -- "$out"
      if command -v zip >/dev/null 2>&1; then
        (cd "$(dirname "$d")" && zip -qr -X "$out" "$name" -x "*/__pycache__/*" "*.pyc" "*/.DS_Store")
      else
        (cd "$(dirname "$d")" && python3 - "$out" "$name" <<'PY'
import os, sys, zipfile
out, name = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(name):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for f in sorted(files):
            if f.endswith(".pyc") or f == ".DS_Store":
                continue
            z.write(os.path.join(root, f))
PY
        )
      fi
    fi
    echo "  zip      $name.zip"
    made=$((made + 1))
    IFS='
'
  done
  IFS="$OLDIFS"
  echo "Done: $made zip files$([ "$DRY" -eq 1 ] && echo ' would be written')."
  if [ "$long" -gt 0 ]; then
    echo "Note: $long of $made skills have descriptions over 200 characters. Claude's help article on custom skills lists 200 as the upload maximum; if an upload is refused, shorten that skill's description in the zip."
  fi
  [ "$DRY" -eq 1 ] || echo "Next: upload each zip in the Claude app's skills settings, then turn the skill on. Connect ScraperCity first (README, 'Connect ScraperCity')."
  exit 0
fi

# ---------------------------------------------------------------- destinations
DESTS=""   # newline-separated "folder|label"
if [ -n "$DEST" ]; then
  DESTS="$DEST|--dest
"
else
  # Several agents share a folder (codex, goose and agents all read ~/.agents/skills),
  # so each folder is written once and labelled with every agent that reads it.
  for t in $TARGETS; do
    dir="$(target_dir "$t" "$SCOPE")"
    merged=""; found=0
    OLDIFS="$IFS"; IFS='
'
    for entry in $DESTS; do
      if [ "${entry%|*}" = "$dir" ]; then entry="$entry,$t"; found=1; fi
      merged="$merged$entry
"
    done
    IFS="$OLDIFS"
    [ "$found" -eq 0 ] && merged="$merged$dir|$t
"
    DESTS="$merged"
  done
fi

existing_in() { # folder -> how many selected skills already have a folder there
  local n=0 d
  OLDIFS2="$IFS"; IFS='
'
  for d in $SELECTED; do [ -e "$1/$(basename "$d")" ] && n=$((n + 1)); done
  IFS="$OLDIFS2"
  echo "$n"
}

echo "Skills:       $COUNT"
echo "Action:       $MODE"
echo "Scope:        $([ -n "$DEST" ] && echo custom || echo "$SCOPE")"
echo "Destinations:"
printf '%s' "$DESTS" | while IFS='|' read -r dir label; do
  [ -n "$dir" ] && printf '  %-22s %s  (%s of %s already there)\n' "$label" "$dir" "$(existing_in "$dir")" "$COUNT"
done
[ "$FORCE" -eq 1 ] && echo "Existing skill folders will be replaced (--force)."
[ "$MODE" = "install" ] && [ "$FORCE" -eq 0 ] && echo "Existing skill folders are skipped. --update replaces the ones that changed; --force replaces all."

if [ "$DRY" -eq 1 ]; then
  echo "Dry run: nothing will be written."
elif [ "$YES" -eq 0 ] && [ -t 0 ] && [ -r /dev/tty ]; then
  tty_read "$([ "$MODE" = uninstall ] && echo Remove || echo Install)? [y/N]: " "n"
  case "$REPLY_VAL" in y|Y|yes|YES|Yes) ;; *) echo "Cancelled. Nothing was written."; exit 1 ;; esac
fi

# ---------------------------------------------------------------- copy, update or remove
same_tree() { # a b -> 0 when the two folders hold the same files with the same bytes
  diff -rq -x __pycache__ -x '*.pyc' -x .DS_Store "$1" "$2" >/dev/null 2>&1
}

installed=0; updated=0; current=0; skipped=0; removed=0; failed=0
DONE_NAMES=""
set -f   # folder names are data, never glob patterns
OLDIFS="$IFS"
IFS='
'
for entry in $DESTS; do
  dir="${entry%|*}"
  label="${entry##*|}"
  echo "[$label] $dir"
  for d in $SELECTED; do
    name="$(basename "$d")"
    target="$dir/$name"
    if [ "$MODE" = "uninstall" ]; then
      if [ ! -f "$target/SKILL.md" ] || ! grep -q "^name: $name\$" "$target/SKILL.md"; then
        echo "  absent   $name"
        skipped=$((skipped + 1))
        continue
      fi
      if [ "$DRY" -eq 0 ] && ! rm -rf -- "$target"; then
        echo "  FAILED   $name (could not remove $target)" >&2
        failed=$((failed + 1))
        continue
      fi
      echo "  remove   $name"
      removed=$((removed + 1))
      continue
    fi
    verb="install"
    if [ -e "$target" ]; then
      if [ "$MODE" = "update" ]; then
        if same_tree "$d" "$target"; then
          echo "  current  $name"
          current=$((current + 1))
          continue
        fi
        verb="update"
      elif [ "$FORCE" -eq 0 ]; then
        echo "  skip     $name (exists; --update or --force to replace)"
        skipped=$((skipped + 1))
        continue
      else
        verb="replace"
      fi
    fi
    if [ "$DRY" -eq 1 ]; then
      echo "  $(printf '%-8s' "$verb") $name"
      if [ "$verb" = "install" ]; then installed=$((installed + 1)); else updated=$((updated + 1)); fi
      continue
    fi
    tmp="$dir/.$name.installing.$$"
    if mkdir -p "$dir" 2>/dev/null && rm -rf -- "$tmp" && cp -R "$d" "$tmp" 2>/dev/null \
       && find "$tmp" \( -name '__pycache__' -o -name '.DS_Store' \) -prune -exec rm -rf {} + 2>/dev/null \
       && rm -rf -- "$target" && mv "$tmp" "$target"; then
      echo "  $(printf '%-8s' "$verb") $name"
      if [ "$verb" = "install" ]; then installed=$((installed + 1)); else updated=$((updated + 1)); fi
      in_list "$name" "$DONE_NAMES" || DONE_NAMES="$DONE_NAMES $name"
    else
      rm -rf -- "$tmp" 2>/dev/null || true
      echo "  FAILED   $name (could not write $target)" >&2
      failed=$((failed + 1))
    fi
  done
done
IFS="$OLDIFS"
set +f

if [ "$MODE" = "uninstall" ]; then
  echo "$([ "$DRY" -eq 1 ] && echo 'Dry run done' || echo Done): $removed removed, $skipped not installed, $failed failed."
  [ "$failed" -gt 0 ] && exit 1
  exit 0
fi

if [ "$DRY" -eq 1 ]; then
  echo "Dry run done: $installed would be installed, $updated replaced, $current current, $skipped skipped, $failed failed."
  exit 0
fi
echo "Done: $installed installed, $updated replaced, $current already current, $skipped skipped, $failed failed."

# ---------------------------------------------------------------- verify against skills.lock
verify_failed=0
if [ "$VERIFY" -eq 1 ] && [ -n "$DONE_NAMES" ] && ! command -v python3 >/dev/null 2>&1; then
  echo "Skipped the skills.lock check: python3 is not on PATH."
elif [ "$VERIFY" -eq 1 ] && [ -n "$DONE_NAMES" ] && ! python3 "$REPO/scripts/generate-lock.py" --check >/dev/null 2>&1; then
  echo "Skipped the skills.lock check: this checkout has edits the lock does not cover yet."
elif [ "$VERIFY" -eq 1 ] && [ -n "$DONE_NAMES" ]; then
  only="$(echo "$DONE_NAMES" | sed 's/^ //' | tr ' ' ',')"
  OLDIFS="$IFS"; IFS='
'
  for entry in $DESTS; do
    dir="${entry%|*}"
    if python3 "$REPO/scripts/generate-lock.py" --verify "$dir" --only "$only" >/dev/null 2>&1; then
      echo "Verified:     $dir matches skills.lock"
    else
      echo "MISMATCH:     $dir differs from skills.lock; run: python3 scripts/generate-lock.py --verify $dir --only $only" >&2
      verify_failed=1
    fi
  done
  IFS="$OLDIFS"
fi

[ "$failed" -gt 0 ] && exit 1
[ "$verify_failed" -gt 0 ] && exit 1
echo "Next: connect ScraperCity (README, 'Connect ScraperCity'), restart your agent, then ask it to load using-scrapercity-skills."
exit 0
