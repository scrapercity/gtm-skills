#!/usr/bin/env python3
"""Write skills.lock: a SHA-256 for every packaged skill file, so installs can be verified.

  python3 scripts/generate-lock.py          # write skills.lock
  python3 scripts/generate-lock.py --check  # exit 1 if skills.lock does not match the files

Verify an installed copy against the lock with:
  python3 scripts/generate-lock.py --verify ~/.claude/skills
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "skills.lock"


def build() -> dict:
    skills = {}
    for skill_md in sorted(ROOT.glob("skills/*/*/SKILL.md")):
        d = skill_md.parent
        files = {
            str(p.relative_to(d)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(d.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts
        }
        skills[f"{d.parent.name}/{d.name}"] = files
    return {
        "lockfileVersion": 1,
        "skills": len(skills),
        "files": sum(len(v) for v in skills.values()),
        "entries": skills,
    }


def main(argv: list[str]) -> int:
    data = build()
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if "--verify" in argv:
        target = Path(argv[argv.index("--verify") + 1]).expanduser()
        bad = 0
        for key, files in data["entries"].items():
            name = key.split("/", 1)[1]
            for rel, digest in files.items():
                p = target / name / rel
                if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() != digest:
                    print(f"MISMATCH {name}/{rel}")
                    bad += 1
        print("PASS - installed files match the lock" if not bad else f"FAIL - {bad} files differ")
        return 1 if bad else 0
    if "--check" in argv:
        if not LOCK.is_file() or LOCK.read_text() != text:
            print("FAIL - skills.lock is stale (run scripts/generate-lock.py)")
            return 1
        print(f"PASS - skills.lock matches {data['skills']} skills, {data['files']} files")
        return 0
    LOCK.write_text(text)
    print(f"Wrote skills.lock: {data['skills']} skills, {data['files']} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
