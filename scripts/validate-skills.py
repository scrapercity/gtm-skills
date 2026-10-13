#!/usr/bin/env python3
"""Validate every skill in skills/ against docs/SKILL_AUTHORING.md.

Usage:
  python3 scripts/validate-skills.py                 # all skills
  python3 scripts/validate-skills.py outbound/cold-calling list-building
                                                     # one skill or one category
  python3 scripts/validate-skills.py --allow-missing-related
                                                     # tolerate related_skills not written yet

Exit code 0 when every checked skill passes, 1 otherwise.
Requires Python 3.9+ and PyYAML.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML is required: pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
SHARED = ROOT / "references"

REQUIRED_SECTIONS = [
    "Overview",
    "When to Use",
    "Authoritative Foundations",
    "Workflow",
    "ScraperCity Implementation",
    "Output Format",
    "Quality Check",
    "Common Pitfalls",
    "Execution Artifacts",
    "Related Skills",
]
REQUIRED_FILES = [
    "references/framework-notes.md",
    "templates/output-template.md",
    "scripts/check-output.py",
    "examples/worked-example.md",
]
MIN_SKILL_LINES = 150
MIN_REFERENCE_LINES = 250
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500

# Public copy rules: a short list of names that must never appear in this repo.
# Stored as SHA-256 hashes of the lowercase word (or of two or three adjacent words
# joined without a space), so the list itself does not publish the names.
RESTRICTED = {
    "954f775230679543d69509c294e19c393d50202fce576bcad71ac6add7b819d7",
    "7603270d69b5c0ee4d95e3c286df04f9487b1d2cf678156ef31faa7e08991974",
    "ff44b37dca63b0db0f9d66ded5cd2ae82828cacc96ccc6a74bdac18b66fdbab1",
    "9fee8d4bbba24a0fcba6615d33fe1458f7acd9c9bee82fbbf280f4900156ba2e",
    "83597d8ec7501096dbe622294eba2cd4de16ba0e716e1a94316d8fa2ad36342a",
    "5bd96801a07762d68ccb81d1b9ead87a61e9428a08ae806a255ead9f56afe1a9",
    "764a51ba6de8ebf2dbe25f3f0708bd42c5c50f65fb9d64b31e2a588c3738005d",
    "2bed2032ed3d8300b7714ff77101e6c43637597977337c699191dd844c86a72d",
    "4d7594e57f7d03f35ede2d316cda4cdb7df66b28963738e836a2f16d9fc9eb4d",
    "67e5a3025bc013d09e3a1e6659f2e53efc7d137272ffe72b6dc8344f578461cf",
    "3cc8fa9b74a7b3350f9f71d5772700db58f1c2a1bc542ae4089590398c591e40",
    "dc9ef7c70f5f40023f5de5cecd470f386257184020e280373c6ba468669797cf",
}
WORD = re.compile(r"[a-z0-9]+")


def restricted_hit(line: str) -> bool:
    words = WORD.findall(line.lower())
    for i in range(len(words)):
        for j in range(i + 1, min(i + 3, len(words)) + 1):
            parts = words[i:j]
            if len(parts) > 1 and min(len(w) for w in parts) < 4:
                continue  # join only whole words, so "sc.db_page" never reads as one name
            if hashlib.sha256("".join(parts).encode()).hexdigest() in RESTRICTED:
                return True
    return False


# The tool id and the CLI command keep the old name; prose must say "Tech Stack Search".
BUILTWITH_OK = re.compile(r"scrape_builtwith|scrapercity builtwith|`builtwith`|/api/v1/scrape/techstack", re.IGNORECASE)
DASHES = re.compile("[–—]")
PATH_REF = re.compile(r"`((?:references|templates|scripts|examples)/[A-Za-z0-9_./-]+)`")


def all_skill_dirs() -> list[Path]:
    return sorted(p.parent for p in SKILLS.glob("*/*/SKILL.md"))


def parse(skill_md: Path) -> tuple[dict, str]:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("missing YAML frontmatter")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def scan_text(path: Path, errors: list[str]) -> None:
    rel = path.relative_to(ROOT)
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if DASHES.search(line):
            errors.append(f"{rel}:{i}: em or en dash (use a hyphen, comma, or rewrite)")
        if restricted_hit(line):
            errors.append(f"{rel}:{i}: restricted name (see the public copy rules in docs/SKILL_AUTHORING.md)")
        if "builtwith" in BUILTWITH_OK.sub("", line).lower():
            errors.append(f"{rel}:{i}: say 'Tech Stack Search' (only the tool id scrape_builtwith may appear)")


def run_checker(checker: Path, target: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-I", str(checker), str(target)], capture_output=True, text=True, timeout=60
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def validate(skill_dir: Path, names: set[str], allow_missing_related: bool) -> list[str]:
    errors: list[str] = []
    rel = skill_dir.relative_to(ROOT)
    category = skill_dir.parent.name
    try:
        fm, body = parse(skill_dir / "SKILL.md")
    except Exception as exc:  # noqa: BLE001
        return [f"{rel}: {exc}"]

    meta = fm.get("metadata") or {}
    if fm.get("name") != skill_dir.name:
        errors.append(f"{rel}: name '{fm.get('name')}' must equal folder '{skill_dir.name}'")
    desc = str(fm.get("description") or "")
    if not 80 <= len(desc) <= MAX_DESCRIPTION:
        errors.append(f"{rel}: description must be 80-{MAX_DESCRIPTION} chars (is {len(desc)})")
    if "use when" not in desc.lower():
        errors.append(f"{rel}: description needs trigger language ('Use when ...')")
    if fm.get("license") != "MIT":
        errors.append(f"{rel}: license must be MIT")
    if not fm.get("compatibility") or len(str(fm["compatibility"])) > MAX_COMPATIBILITY:
        errors.append(f"{rel}: compatibility missing or too long")
    if meta.get("author") != "ScraperCity":
        errors.append(f"{rel}: metadata.author must be ScraperCity")
    if meta.get("category") != category:
        errors.append(f"{rel}: metadata.category must be '{category}'")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(meta.get("version", ""))):
        errors.append(f"{rel}: metadata.version must be semver")
    for key in ("tags", "related_skills", "frameworks"):
        if not isinstance(meta.get(key), list) or not meta.get(key):
            errors.append(f"{rel}: metadata.{key} must be a non-empty list")
    for other in meta.get("related_skills") or []:
        if other not in names and not allow_missing_related:
            errors.append(f"{rel}: related skill '{other}' does not exist")
    shared = meta.get("shared_references") or []
    for ref in shared:
        if not (SHARED / ref).is_file() and not allow_missing_related:
            errors.append(f"{rel}: shared reference references/{ref} does not exist at repo root")

    headings = re.findall(r"^## (.+?)\s*$", body, re.MULTILINE)
    positions = []
    for section in REQUIRED_SECTIONS:
        if section not in headings:
            errors.append(f"{rel}: missing section '## {section}'")
        else:
            positions.append(headings.index(section))
    if positions != sorted(positions):
        errors.append(f"{rel}: sections out of order, expected {', '.join(REQUIRED_SECTIONS)}")

    skill_lines = len((skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines())
    if skill_lines < MIN_SKILL_LINES:
        errors.append(f"{rel}: SKILL.md has {skill_lines} lines, minimum is {MIN_SKILL_LINES}")

    for f in REQUIRED_FILES:
        if not (skill_dir / f).is_file():
            errors.append(f"{rel}: missing {f}")

    shared_names = {f"references/{r}" for r in shared}
    for ref in sorted(set(PATH_REF.findall(body))):
        if not (skill_dir / ref).exists() and ref not in shared_names:
            errors.append(f"{rel}: SKILL.md points to {ref}, which does not exist")

    ref_dir = skill_dir / "references"
    ref_lines = sum(
        len(p.read_text(encoding="utf-8").splitlines())
        for p in ref_dir.glob("*.md")
        if p.name.replace(".md", "") not in {Path(s).stem for s in shared}
    ) if ref_dir.is_dir() else 0
    if ref_lines < MIN_REFERENCE_LINES:
        errors.append(f"{rel}: skill-owned references total {ref_lines} lines, minimum is {MIN_REFERENCE_LINES}")

    for path in sorted(skill_dir.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".csv"}:
            scan_text(path, errors)

    checker = skill_dir / "scripts" / "check-output.py"
    template = skill_dir / "templates" / "output-template.md"
    example = skill_dir / "examples" / "worked-example.md"
    if checker.is_file():
        try:
            compile(checker.read_text(encoding="utf-8"), str(checker), "exec")
        except SyntaxError as exc:
            errors.append(f"{rel}: check-output.py does not compile: {exc}")
        else:
            if template.is_file():
                code, out = run_checker(checker, template)
                if code == 0:
                    errors.append(f"{rel}: checker must FAIL on the unfilled template, got: {out[:160]}")
            if example.is_file():
                code, out = run_checker(checker, example)
                if code != 0:
                    errors.append(f"{rel}: checker must PASS on examples/worked-example.md, got: {out[:300]}")
    return errors


def main(argv: list[str]) -> int:
    allow = "--allow-missing-related" in argv
    targets = [a for a in argv if not a.startswith("--")]
    dirs = all_skill_dirs()
    names = {d.name for d in dirs}
    if targets:
        dirs = [d for d in dirs if any(str(d.relative_to(SKILLS)).startswith(t.rstrip("/")) for t in targets)]
    if not dirs:
        print("No skills matched.")
        return 1
    failed = 0
    for d in dirs:
        errs = validate(d, names, allow)
        if errs:
            failed += 1
            print(f"FAIL {d.relative_to(SKILLS)}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS {d.relative_to(SKILLS)}")
    for path in sorted((SHARED).glob("*.md")):
        errs: list[str] = []
        scan_text(path, errs)
        for e in errs:
            print(f"FAIL {e}")
            failed += 1
    print(f"\n{len(dirs) - min(failed, len(dirs))}/{len(dirs)} skills passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
