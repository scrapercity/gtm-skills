#!/usr/bin/env python3
"""Write skills.lock: a SHA-256, size and kind for every packaged skill file.

  python3 scripts/generate-lock.py                       # write skills.lock
  python3 scripts/generate-lock.py --check               # exit 1 if skills.lock does not match the files
  python3 scripts/generate-lock.py --verify ~/.claude/skills
                                                         # check an installed copy against skills.lock
                                                         # (SKILL.md frontmatter lines that gh skill install
                                                         # adds under metadata, github-*, are set aside)
  python3 scripts/generate-lock.py --verify ~/.claude/skills --only cold-calling,inbox-setup
                                                         # check only the named skills

What the lock records (see docs/INTEGRITY.md for what it proves and what it does not):

  schemaVersion   format version of this file
  generatedFrom   the git commit checked out when the lock was written (omitted outside git).
                  It is the parent of the commit that carries the lock, so --check ignores it.
  totals          skills, files and bytes
  kinds           file count per kind: skill entrypoint, reference, template, example, script
  entries         per skill, per file: sha256, size_bytes, kind, and shared=true for a copy
                  of a repo-root shared reference

The file holds no timestamp, so the same tree always produces the same lock.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "skills.lock"
SHARED = ROOT / "references"
SCHEMA_VERSION = 2
KINDS = {
    "references": "reference",
    "templates": "template",
    "examples": "example",
    "scripts": "script",
}


def kind_of(rel: Path) -> str:
    if rel.as_posix() == "SKILL.md":
        return "skill entrypoint"
    return KINDS.get(rel.parts[0], "other") if len(rel.parts) > 1 else "other"


def git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    return out if len(out) == 40 else None


def build() -> dict:
    shared = {p.name for p in SHARED.glob("*.md")}
    entries: dict[str, dict] = {}
    kinds: dict[str, int] = {}
    total_bytes = 0
    for skill_md in sorted(ROOT.glob("skills/*/*/SKILL.md")):
        d = skill_md.parent
        files = {}
        for p in sorted(d.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or p.name == ".DS_Store":
                continue
            rel = p.relative_to(d)
            body = p.read_bytes()
            kind = kind_of(rel)
            item = {"kind": kind, "sha256": hashlib.sha256(body).hexdigest(), "size_bytes": len(body)}
            if kind == "reference" and len(rel.parts) == 2 and rel.name in shared:
                item["shared"] = True
            files[rel.as_posix()] = item
            kinds[kind] = kinds.get(kind, 0) + 1
            total_bytes += len(body)
        entries[f"{d.parent.name}/{d.name}"] = files
    data = {
        "schemaVersion": SCHEMA_VERSION,
        "totals": {
            "skills": len(entries),
            "files": sum(len(v) for v in entries.values()),
            "bytes": total_bytes,
        },
        "kinds": dict(sorted(kinds.items())),
        "entries": entries,
    }
    commit = git_commit()
    if commit:
        data["generatedFrom"] = commit
    return data


def dump(data: dict) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def comparable(data: dict) -> dict:
    return {k: v for k, v in data.items() if k != "generatedFrom"}


def load_lock() -> dict | None:
    if not LOCK.is_file():
        return None
    try:
        return json.loads(LOCK.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def lock_digests(lock: dict) -> dict[str, dict[str, str]]:
    """skill folder name -> {relative path: sha256}, for schema 1 and schema 2 locks."""
    out: dict[str, dict[str, str]] = {}
    for key, files in lock.get("entries", {}).items():
        name = key.split("/", 1)[1]
        out[name] = {rel: (v["sha256"] if isinstance(v, dict) else v) for rel, v in files.items()}
    return out


GH_INSTALL_LINE = re.compile(rb"^[ \t]+github-[A-Za-z0-9-]+:.*\n", re.MULTILINE)


def strip_install_metadata(body: bytes) -> bytes:
    """Remove the metadata.github-* lines `gh skill install` writes into SKILL.md frontmatter."""
    end = body.find(b"\n---\n", 4)
    if not body.startswith(b"---\n") or end == -1:
        return body
    return GH_INSTALL_LINE.sub(b"", body[:end + 1]) + body[end + 1:]


def verify(target: Path, only: set[str] | None = None) -> int:
    lock = load_lock()
    if lock is None:
        print("FAIL - skills.lock is missing or not valid JSON")
        return 1
    if not target.is_dir():
        print(f"FAIL - {target} is not a folder")
        return 1
    checked = bad = missing = 0
    for name, files in lock_digests(lock).items():
        if only is not None and name not in only:
            continue
        skill_dir = target / name
        if not skill_dir.is_dir():
            continue  # not installed here, which is fine (bundles install a subset)
        checked += 1
        for rel, digest in files.items():
            p = skill_dir / rel
            if not p.is_file():
                print(f"MISSING  {name}/{rel}")
                missing += 1
            elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
                if rel == "SKILL.md" and hashlib.sha256(strip_install_metadata(p.read_bytes())).hexdigest() == digest:
                    print(f"OK       {name}/{rel} (matches once gh skill install's metadata.github-* lines are set aside)")
                    continue
                print(f"MISMATCH {name}/{rel}")
                bad += 1
        for p in sorted(skill_dir.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts and p.relative_to(skill_dir).as_posix() not in files:
                print(f"EXTRA    {name}/{p.relative_to(skill_dir).as_posix()} (not in the lock)")
    if checked == 0:
        print(f"FAIL - no skills from skills.lock are installed in {target}")
        return 1
    if bad or missing:
        print(f"FAIL - {checked} skills checked: {bad} files differ, {missing} missing")
        return 1
    print(f"PASS - {checked} installed skills match skills.lock")
    return 0


def main(argv: list[str]) -> int:
    if "--verify" in argv:
        i = argv.index("--verify")
        if i + 1 >= len(argv):
            print("usage: generate-lock.py --verify <skills folder>")
            return 2
        only = None
        if "--only" in argv:
            j = argv.index("--only")
            if j + 1 >= len(argv):
                print("usage: generate-lock.py --verify <skills folder> [--only name,name]")
                return 2
            only = {n for n in argv[j + 1].split(",") if n}
        return verify(Path(argv[i + 1]).expanduser(), only)

    data = build()
    current = load_lock()
    if "--check" in argv:
        # generatedFrom is left out of the comparison: committing the lock moves HEAD past it.
        if (
            current is None
            or comparable(current) != comparable(data)
            or LOCK.read_text(encoding="utf-8") != dump(current)
        ):
            print("FAIL - skills.lock is stale (run scripts/generate-lock.py)")
            return 1
        t = data["totals"]
        print(f"PASS - skills.lock matches {t['skills']} skills, {t['files']} files")
        return 0

    if current is not None and comparable(current) == comparable(data):
        print(f"skills.lock already current: {data['totals']['skills']} skills, {data['totals']['files']} files")
        return 0
    LOCK.write_text(dump(data), encoding="utf-8")
    t = data["totals"]
    print(f"Wrote skills.lock: {t['skills']} skills, {t['files']} files, {t['bytes']:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
