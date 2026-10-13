#!/usr/bin/env python3
"""Regenerate the catalog and inventory sections of README.md from the skill folders.

  python3 scripts/generate-readme.py          # rewrite the generated blocks
  python3 scripts/generate-readme.py --check  # exit 1 if README.md is stale
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
ORDER = ["scrapercity", "list-building", "outbound"]
TITLES = {
    "scrapercity": "ScraperCity platform",
    "list-building": "List building",
    "outbound": "Outbound",
}


def load():
    out = {}
    for skill_md in sorted(ROOT.glob("skills/*/*/SKILL.md")):
        m = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.DOTALL)
        fm = yaml.safe_load(m.group(1))
        desc = " ".join(fm["description"].split())
        first = re.split(r"(?<=[.!?])\s", desc, maxsplit=1)[0]
        out.setdefault(skill_md.parent.parent.name, []).append((fm["name"], first, skill_md.relative_to(ROOT)))
    return out


def catalog(skills) -> str:
    lines = []
    for cat in ORDER:
        rows = skills.get(cat, [])
        lines.append(f"### {TITLES[cat]} ({len(rows)})")
        lines.append("")
        lines.append("| Skill | What it does |")
        lines.append("|-|-|")
        for name, first, path in rows:
            lines.append(f"| [{name}]({path.as_posix()}) | {first} |")
        lines.append("")
    return "\n".join(lines).rstrip()


def inventory(skills) -> str:
    dirs = [ROOT / p.parent for rows in skills.values() for _, _, p in rows]
    def count(sub):
        return sum(1 for d in dirs for f in (d / sub).rglob("*") if f.is_file()) if sub else 0
    shared = sorted(p.name for p in (ROOT / "references").glob("*.md"))
    owned_refs = sum(
        1 for d in dirs for f in (d / "references").glob("*.md") if f.name not in shared
    )
    total_files = sum(1 for d in dirs for f in d.rglob("*") if f.is_file())
    lines_md = sum(
        len(f.read_text(encoding="utf-8").splitlines())
        for d in dirs for f in d.rglob("*.md")
        if not (f.parent.name == "references" and f.name in shared)
    ) + sum(len((ROOT / "references" / n).read_text(encoding="utf-8").splitlines()) for n in shared)
    rows = [
        ("Skills", len(dirs)),
        ("Categories", len(skills)),
        ("Skill-owned reference files", owned_refs),
        ("Shared reference files (repo root, copied into each skill that uses them)", len(shared)),
        ("Output templates", count("templates")),
        ("Worked examples", count("examples")),
        ("Deliverable checkers", count("scripts")),
        ("Total packaged files", total_files),
        ("Lines of Markdown (shared references counted once)", lines_md),
    ]
    out = ["| Inventory | Count |", "|-|-:|"]
    out += [f"| {k} | {v:,} |" for k, v in rows]
    return "\n".join(out)


def replace(text: str, tag: str, body: str) -> str:
    start, end = f"<!-- GENERATED:{tag}:start -->", f"<!-- GENERATED:{tag}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"README.md is missing the {tag} markers")
    return pattern.sub(lambda _: f"{start}\n{body}\n{end}", text)


def main(argv):
    skills = load()
    text = README.read_text(encoding="utf-8")
    new = replace(text, "catalog", catalog(skills))
    new = replace(new, "inventory", inventory(skills))
    new = re.sub(r"\*\*\d+ skills\*\*", f"**{sum(len(v) for v in skills.values())} skills**", new)
    if "--check" in argv:
        if new != text:
            print("FAIL - README.md is stale (run scripts/generate-readme.py)")
            return 1
        print("PASS - README.md catalog and inventory are current")
        return 0
    README.write_text(new, encoding="utf-8")
    print("Wrote README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
