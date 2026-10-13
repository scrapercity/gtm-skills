#!/usr/bin/env python3
"""Copy shared references into every skill that lists them.

Each skill names the repo-root files it depends on in `metadata.shared_references`.
This script copies those files into the skill's own `references/` folder, so a skill
installed by itself (copied into ~/.claude/skills, say) still has every file it points to.
The repo-root copy in `references/` is the source of truth. Never edit a skill's copy.

  python3 scripts/materialize-shared-references.py          # write the copies
  python3 scripts/materialize-shared-references.py --check  # exit 1 if any copy is missing or stale
"""

from __future__ import annotations

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


def main(argv: list[str]) -> int:
    check = "--check" in argv
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
