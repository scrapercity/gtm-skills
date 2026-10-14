#!/usr/bin/env python3
"""Regenerate every generated block outside the skill folders from the skills on disk.

  python3 scripts/generate-readme.py          # rewrite the generated blocks
  python3 scripts/generate-readme.py --check  # exit 1 if any of them is stale

What it writes:

  README.md      the catalog, inventory and authorities blocks between GENERATED markers,
                 the bold skill count, and the skills badge
  AGENTS.md      the skill index block between GENERATED markers (name, category, when to use)
  .claude-plugin/plugin.json, .claude-plugin/marketplace.json
                 the "N go-to-market agent skills" count in each description

Prose outside the markers is hand-written and never touched.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
AGENTS = ROOT / "AGENTS.md"
EXPERTS = ROOT / "references" / "experts.md"
MANIFESTS = [ROOT / ".claude-plugin" / "plugin.json", ROOT / ".claude-plugin" / "marketplace.json"]
ORDER = ["scrapercity", "list-building", "outbound"]
TITLES = {
    "scrapercity": "ScraperCity platform",
    "list-building": "List building",
    "outbound": "Outbound",
}
COUNT_PHRASE = re.compile(r"\b\d+ go-to-market agent skills\b")


def frontmatter(skill_md: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.DOTALL)
    return yaml.safe_load(m.group(1)) or {}


def load():
    out = {}
    for skill_md in sorted(ROOT.glob("skills/*/*/SKILL.md")):
        fm = frontmatter(skill_md)
        desc = " ".join(fm["description"].split())
        first = re.split(r"(?<=[.!?])\s", desc, maxsplit=1)[0]
        use = re.search(r"\bUse (?:it )?when\b(.*?)(?:(?<=[.!?])\s|$)", desc)
        when = ("Use when" + use.group(1)).strip() if use else first
        out.setdefault(skill_md.parent.parent.name, []).append(
            {"name": fm["name"], "first": first, "when": when, "path": skill_md.relative_to(ROOT), "fm": fm}
        )
    return out


def ordered(skills):
    return [c for c in ORDER if c in skills] + sorted(set(skills) - set(ORDER))


def catalog(skills) -> str:
    lines = []
    for cat in ordered(skills):
        rows = skills[cat]
        lines += [f"### {TITLES.get(cat, cat)} ({len(rows)})", "", "| Skill | What it does |", "|-|-|"]
        lines += [f"| [{s['name']}]({s['path'].as_posix()}) | {s['first']} |" for s in rows]
        lines.append("")
    return "\n".join(lines).rstrip()


def inventory(skills) -> str:
    entries = [s for rows in skills.values() for s in rows]
    dirs = [ROOT / s["path"].parent for s in entries]

    def count(sub):
        return sum(1 for d in dirs for f in (d / sub).rglob("*") if f.is_file())

    # Root files that no skill lists in shared_references (the generated pitfalls index,
    # for one) are repo-level reading, not packaged copies, so they are not counted here.
    listed = {n for s in entries for n in ((s["fm"].get("metadata") or {}).get("shared_references") or [])}
    shared = sorted(p.name for p in (ROOT / "references").glob("*.md") if p.name in listed)
    owned_refs = sum(1 for d in dirs for f in (d / "references").glob("*.md") if f.name not in shared)
    total_files = sum(1 for d in dirs for f in d.rglob("*") if f.is_file() and "__pycache__" not in f.parts)
    lines_md = sum(
        len(f.read_text(encoding="utf-8").splitlines())
        for d in dirs for f in d.rglob("*.md")
        if not (f.parent.name == "references" and f.name in shared)
    ) + sum(len((ROOT / "references" / n).read_text(encoding="utf-8").splitlines()) for n in shared)
    pitfalls = ROOT / "references" / "pitfalls-index.md"
    m = re.search(r"^(\d+) pitfalls across", pitfalls.read_text(encoding="utf-8"), re.M) if pitfalls.is_file() else None
    rows = [
        ("Skills", len(dirs)),
        ("Categories", len(skills)),
        ("Skill-owned reference files", owned_refs),
        ("Shared reference files (repo root, copied into each skill that uses them)", len(shared)),
        ("Output templates", count("templates")),
        ("Worked examples", count("examples")),
        ("Deliverable checkers", count("scripts")),
        ("Common Pitfalls rows (references/pitfalls-index.md)", int(m.group(1)) if m else 0),
        ("Total packaged files", total_files),
        ("Lines of Markdown (shared references counted once)", lines_md),
    ]
    out = ["| Inventory | Count |", "|-|-:|"]
    out += [f"| {k} | {v:,} |" for k, v in rows]
    return "\n".join(out)


def authorities(skills) -> str:
    """Experts index names, counted by how many skills credit them in metadata.frameworks.

    Only the attribution before " - " in each framework entry counts, so "Google Maps" in a
    method name is not read as a citation of Google's sender guidelines.
    """
    names = []
    if EXPERTS.is_file():
        index = EXPERTS.read_text(encoding="utf-8").split("## Index", 1)[-1].split("\n## ", 1)[0]
        names = [m.group(1).strip() for m in re.finditer(r"^\| ([^|]+?) \|", index, re.M)]
        names = [n for n in names if n not in {"Authority", "-"} and not n.startswith("-")]
    entries = [s for rows in skills.values() for s in rows]
    counted = []
    for name in names:
        parts = [p.strip() for p in re.split(r"\band\b", name) if p.strip()]
        pattern = re.compile("|".join(rf"(?<![A-Za-z]){re.escape(p)}(?![A-Za-z])" for p in parts))
        cited = [
            s["name"] for s in entries
            if any(pattern.search(str(f).split(" - ")[0]) for f in (s["fm"].get("metadata") or {}).get("frameworks") or [])
        ]
        if cited:
            counted.append((name, len(cited)))
    counted.sort(key=lambda x: (-x[1], x[0]))
    out = ["| Authority | Skills that name them in `frameworks` |", "|-|-:|"]
    out += [f"| {n} | {c} |" for n, c in counted]
    return "\n".join(out)


def agents_index(skills) -> str:
    out = ["| Skill | Category | Use when |", "|-|-|-|"]
    for cat in ordered(skills):
        for s in skills[cat]:
            when = re.sub(r"^Use when\s*", "", s["when"]).rstrip(".")
            out.append(f"| `{s['name']}` | {cat} | {when} |")
    return "\n".join(out)


def replace(text: str, tag: str, body: str, where: str) -> str:
    start, end = f"<!-- GENERATED:{tag}:start -->", f"<!-- GENERATED:{tag}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"{where} is missing the {tag} markers")
    return pattern.sub(lambda _: f"{start}\n{body}\n{end}", text)


def build(skills) -> dict[Path, str]:
    total = sum(len(v) for v in skills.values())
    readme = README.read_text(encoding="utf-8")
    new = replace(readme, "catalog", catalog(skills), "README.md")
    new = replace(new, "inventory", inventory(skills), "README.md")
    new = replace(new, "authorities", authorities(skills), "README.md")
    new = re.sub(r"\*\*\d+ skills\*\*", f"**{total} skills**", new)
    new = re.sub(r"badge/skills-\d+-", f"badge/skills-{total}-", new)
    outputs = {README: new}
    outputs[AGENTS] = replace(AGENTS.read_text(encoding="utf-8"), "skills", agents_index(skills), "AGENTS.md")
    for manifest in MANIFESTS:
        text = manifest.read_text(encoding="utf-8")
        json.loads(text)  # fail loudly on a broken manifest
        outputs[manifest] = COUNT_PHRASE.sub(f"{total} go-to-market agent skills", text)
    return outputs


def main(argv):
    outputs = build(load())
    if "--check" in argv:
        stale = [p for p, text in outputs.items() if p.read_text(encoding="utf-8") != text]
        for p in stale:
            print(f"FAIL - {p.relative_to(ROOT)} is stale (run scripts/generate-readme.py)")
        if stale:
            return 1
        print("PASS - README.md, AGENTS.md and the plugin manifests are current")
        return 0
    for p, text in outputs.items():
        if p.read_text(encoding="utf-8") != text:
            p.write_text(text, encoding="utf-8")
            print(f"Wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
