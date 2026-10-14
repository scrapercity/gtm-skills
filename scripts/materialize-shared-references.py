#!/usr/bin/env python3
"""Copy shared references into every skill that lists them.

Each skill names the repo-root files it depends on in `metadata.shared_references`.
This script copies those files into the skill's own `references/` folder, so a skill
installed by itself (copied into ~/.claude/skills, say) still has every file it points to.
The repo-root copy in `references/` is the source of truth. Never edit a skill's copy.

  python3 scripts/materialize-shared-references.py          # write the copies
  python3 scripts/materialize-shared-references.py --check  # exit 1 if any copy is missing or stale
  python3 scripts/materialize-shared-references.py --prune  # also delete orphan copies
  python3 scripts/materialize-shared-references.py --check --strict
                                                            # also exit 1 on orphan copies

An orphan is a file in a skill's references/ folder that has the name of a repo-root
shared reference the skill no longer lists in shared_references: a copy left behind when
a skill dropped a reference, or when the root file was deleted. --check reports orphans
as warnings; --prune deletes them; --strict makes them fail the check.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "references"


def shared_refs(skill_md: Path) -> list[str]:
    m = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.DOTALL)
    meta = (yaml.safe_load(m.group(1)) or {}).get("metadata") or {} if m else {}
    return list(meta.get("shared_references") or [])


def locked_shared_names() -> set[str]:
    """Names skills.lock marked shared, so copies of a deleted root reference still count."""
    lock = ROOT / "skills.lock"
    try:
        entries = json.loads(lock.read_text(encoding="utf-8")).get("entries", {})
    except (OSError, ValueError):
        return set()
    return {
        Path(rel).name
        for files in entries.values()
        for rel, item in files.items()
        if isinstance(item, dict) and item.get("shared")
    }


def orphans(skill_md: Path, root_names: set[str]) -> list[Path]:
    listed = set(shared_refs(skill_md))
    ref_dir = skill_md.parent / "references"
    if not ref_dir.is_dir():
        return []
    return sorted(p for p in ref_dir.glob("*.md") if p.name not in listed and p.name in root_names)


def main(argv: list[str]) -> int:
    check = "--check" in argv
    prune = "--prune" in argv
    strict = "--strict" in argv
    root_names = {p.name for p in SHARED.glob("*.md")} | locked_shared_names()
    orphan_files = [o for s in sorted(ROOT.glob("skills/*/*/SKILL.md")) for o in orphans(s, root_names)]
    for o in orphan_files:
        rel = o.relative_to(ROOT)
        if prune and not check:
            o.unlink()
            print(f"Removed orphan copy {rel}")
        else:
            print(f"{'FAIL' if strict else 'WARN'} - orphan copy {rel} (the skill no longer lists it; --prune deletes it)")
    if check and strict and orphan_files:
        return 1
    stale, written = [], 0
    for skill_md in sorted(ROOT.glob("skills/*/*/SKILL.md")):
        for name in shared_refs(skill_md):
            src = SHARED / name
            if not src.is_file():
                print(f"FAIL - {skill_md.parent.relative_to(ROOT)} lists missing shared reference {name}")
                return 1
            dst = skill_md.parent / "references" / name
            body = src.read_bytes()
            if dst.is_file() and dst.read_bytes() == body:
                continue
            if check:
                stale.append(str(dst.relative_to(ROOT)))
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(body)
                written += 1
    if check:
        if stale:
            print("FAIL - stale shared reference copies (run scripts/materialize-shared-references.py):")
            for s in stale:
                print("  " + s)
            return 1
        print("PASS - every shared reference copy matches references/")
        return 0
    print(f"Wrote {written} shared reference copies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
