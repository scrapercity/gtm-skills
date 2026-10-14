#!/usr/bin/env python3
"""Validate every skill in skills/ against docs/SKILL_AUTHORING.md.

Usage:
  python3 scripts/validate-skills.py                 # all skills
  python3 scripts/validate-skills.py outbound/cold-calling list-building
                                                     # one skill or one category
  python3 scripts/validate-skills.py --allow-missing-related
                                                     # tolerate related_skills not written yet
  python3 scripts/validate-skills.py --strict        # add the spec and hygiene checks below
  python3 scripts/validate-skills.py --check-legal   # fail on legal terms (owner rule 1)

Default checks: frontmatter, section order, required files, lengths, backticked paths,
public copy rules, and the checker contract (fails the template, passes the example).

--strict adds checks that mirror the Agent Skills reference validator (skills-ref) and
Claude's skill rules, plus package hygiene:
  name: 1-64 chars, a-z 0-9 and single hyphens, no "claude" or "anthropic"
  name and description: no XML tags; frontmatter: only spec keys, no flow-style [lists]
  SKILL.md under 500 lines; no duplicate skill names across categories; each section once
  at least 3 distinct frameworks; no filler phrases (SLOP below) in SKILL.md
  every file in the skill named in Execution Artifacts (materialized shared copies excepted)
  every Markdown link in the skill resolves inside the skill folder
  no symlinks, empty files, editor or cache junk, or files outside the standard folders
  the checker exits 2 with no argument and gives the same result on two runs
  the worked example carries the "Illustrative example" label

--check-legal fails any skill file or root reference that names a law, regulation or
regulator, tells the reader to consult a lawyer, or adds a compliance gate. The term list
is LEGAL_TERMS below; reply-classification words such as "lawyer" are allowed only in
skills/outbound/reply-handling.

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
DASHES = re.compile("[\u2013\u2014]")
PATH_REF = re.compile(r"`((?:references|templates|scripts|examples)/[A-Za-z0-9_./-]+)`")

# Owner rule 1 (Oct 13 2026): skills carry no legal content. Each entry is
# (label, pattern, path prefixes where the pattern is allowed, a pattern that
# excuses the line). Acronyms are case-sensitive so ordinary words never match.
# Law firms are a normal prospecting vertical, so "attorney" in a targeting line
# (a title filter, a category or NAICS row, "personal injury lawyers") passes.
_I = re.IGNORECASE
TARGETING_LINE = re.compile(
    r"law firms?|legal services|offices of lawyers|naics|\"title\"|managing partner|practice area|"
    r"(?:personal injury|estate planning|foreclosure|divorce|immigration|bankruptcy|real estate|criminal defense|"
    r"family|dui|tax|patent|trademark|employment|business|corporate|principal)\s+(?:lawyers?|attorneys?)",
    _I,
)
LEGAL_TERMS = [
    ("CAN-SPAM", re.compile(r"\bCAN[- ]?SPAM\b", _I), (), None),
    ("TCPA", re.compile(r"\bTCPA\b|Telephone Consumer Protection", _I), (), None),
    ("CASL", re.compile(r"\bCASL\b|Anti-Spam Legislation"), (), None),
    ("GDPR", re.compile(r"\bGDPR\b|General Data Protection Regulation|\bePrivacy\b|lawful basis|legitimate interests? assessment", _I), (), None),
    ("CCPA", re.compile(r"\bCCPA\b|\bCPRA\b|California Consumer Privacy"), (), None),
    ("PECR", re.compile(r"\bPECR\b|Privacy and Electronic Communications"), (), None),
    ("FCRA", re.compile(r"\bFCRA\b|Fair Credit Reporting"), (), None),
    ("TSR", re.compile(r"\bTSR\b|Telemarketing Sales Rule"), (), None),
    ("CFR citation", re.compile(r"\b(?:47|16)\s*C\.?F\.?R\b", _I), (), None),
    ("regulator", re.compile(r"\b(?:FTC|FCC|CRTC|ICO)\b|Federal Trade Commission|Federal Communications Commission|Information Commissioner|Attorneys? General"), (), None),
    ("legal advice", re.compile(r"\blegal advice\b|\bnot legal\b", _I), (), None),
    ("consult a lawyer", re.compile(r"\b(?:consult|ask|check with|speak (?:to|with)|talk (?:to|with))\s+(?:with\s+)?(?:a|an|your)\s+(?:\w+\s+)?(?:lawyer|attorney|counsel|solicitor|legal (?:team|adviser|advisor))", _I), (), None),
    ("lawyer or attorney", re.compile(r"\b(?:lawyers?|attorneys?)\b", _I), ("skills/outbound/reply-handling/",), TARGETING_LINE),
    ("Do Not Call Registry", re.compile(r"Do[- ]Not[- ]Call Registry|National Do[- ]Not[- ]Call|donotcall\.gov", _I), (), None),
    ("compliance gate", re.compile(r"\bcompliance gates?\b", _I), (), None),
]


def legal_hits(line: str, rel_posix: str) -> list[str]:
    hits = []
    for label, pattern, allowed, excuse in LEGAL_TERMS:
        if any(rel_posix.startswith(prefix) for prefix in allowed):
            continue
        if excuse is not None and excuse.search(line) and not re.search(r"Attorneys? General", line):
            continue
        m = pattern.search(line)
        if m:
            hits.append(f"{label} ('{m.group(0)}')")
    return hits


SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SPEC_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
XML_TAG = re.compile(r"<[A-Za-z/][^>]*>")
FLOW_LIST = re.compile(r"^\s*[A-Za-z_][\w-]*:\s*\[")
MD_LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
STANDARD_DIRS = {"references", "templates", "examples", "scripts", "assets"}
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
JUNK_SUFFIXES = (".pyc", ".orig", ".rej", ".swp", ".swo", ".tmp", ".bak", "~")
MAX_SKILL_LINES = 500
SLOP = ["actually", "genuinely", "quietly", "cleanly", "crazy", "in today's fast-paced", "game-changing",
        "game changer", "unlock your", "supercharge", "seamless", "best-in-class", "cutting-edge", "delve"]


def all_skill_dirs() -> list[Path]:
    return sorted(p.parent for p in SKILLS.glob("*/*/SKILL.md"))


def parse(skill_md: Path) -> tuple[dict, str]:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("missing YAML frontmatter")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def scan_text(path: Path, errors: list[str], legal: bool = False) -> None:
    rel = path.relative_to(ROOT)
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if legal:
            for hit in legal_hits(line, rel.as_posix()):
                errors.append(f"{rel}:{i}: legal term {hit}; owner rule: no legal content")
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


def link_target_ok(target: str, md_file: Path, skill_dir: Path) -> bool:
    """A relative link resolves from the file that holds it or from the skill root, inside the skill."""
    root = skill_dir.resolve()
    for base in (md_file.parent, skill_dir):
        candidate = (base / target).resolve()
        if candidate.exists() and (candidate == root or root in candidate.parents):
            return True
    return False


def strict_checks(skill_dir: Path, fm: dict, errors: list[str]) -> None:
    rel = skill_dir.relative_to(ROOT)
    name = str(fm.get("name") or "")
    desc = str(fm.get("description") or "")
    if not (1 <= len(name) <= 64 and SPEC_NAME.match(name)):
        errors.append(f"{rel}: name must be 1-64 chars of a-z, 0-9 and single hyphens (Agent Skills spec)")
    if re.search(r"claude|anthropic", name):
        errors.append(f"{rel}: name contains a reserved word (claude, anthropic)")
    for key, value in (("name", name), ("description", desc)):
        if XML_TAG.search(value):
            errors.append(f"{rel}: {key} contains an XML tag")
    unknown = sorted(set(fm) - SPEC_KEYS)
    if unknown:
        errors.append(f"{rel}: frontmatter keys outside the Agent Skills spec: {', '.join(unknown)} (move them under metadata)")
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    fm_text = text.split("\n---\n", 1)[0]
    flow = [line.strip().split(":")[0] for line in fm_text.splitlines() if FLOW_LIST.match(line)]
    if flow:
        errors.append(
            f"{rel}: flow-style [lists] in frontmatter ({', '.join(flow)}); the skills-ref validator rejects them. "
            "Run scripts/normalize-frontmatter.py"
        )
    meta = fm.get("metadata") or {}
    frameworks = [str(f) for f in meta.get("frameworks") or []]
    if len(set(frameworks)) < 3:
        errors.append(f"{rel}: metadata.frameworks needs at least 3 distinct named sources (has {len(set(frameworks))})")
    if len(set(frameworks)) != len(frameworks):
        errors.append(f"{rel}: metadata.frameworks repeats an entry")
    body = text.split("\n---\n", 1)[1] if "\n---\n" in text else text
    headings = re.findall(r"^## (.+?)\s*$", body, re.MULTILINE)
    for heading in sorted({h for h in headings if headings.count(h) > 1}):
        errors.append(f"{rel}: section '## {heading}' appears {headings.count(heading)} times")
    for phrase in SLOP:
        if re.search(rf"\b{re.escape(phrase)}", text, re.IGNORECASE):
            errors.append(f"{rel}: SKILL.md uses the filler phrase '{phrase}' (docs/SKILL_AUTHORING.md copy rules)")
    shared = {str(s) for s in meta.get("shared_references") or []}
    artifacts = body.split("## Execution Artifacts", 1)[1].split("\n## ", 1)[0] if "## Execution Artifacts" in body else ""
    for path in sorted(skill_dir.rglob("*")):
        prel = path.relative_to(skill_dir).as_posix()
        if not path.is_file() or prel == "SKILL.md" or "__pycache__" in path.parts:
            continue
        if prel.startswith("references/") and path.name in shared:
            continue
        if prel not in artifacts:
            orphan = prel.startswith("references/") and (SHARED / path.name).is_file()
            errors.append(
                f"{rel}: {prel} is a stale copy of a shared reference the skill no longer lists (run scripts/materialize-shared-references.py --prune)"
                if orphan else f"{rel}: {prel} is not named in Execution Artifacts"
            )
    lines = len(text.splitlines())
    if lines > MAX_SKILL_LINES:
        errors.append(f"{rel}: SKILL.md has {lines} lines; the Agent Skills spec recommends under {MAX_SKILL_LINES}")

    for path in sorted(skill_dir.rglob("*")):
        prel = path.relative_to(skill_dir)
        if path.is_symlink():
            errors.append(f"{rel}/{prel}: symlink (installers copy folders; use a real file)")
            continue
        if path.is_dir():
            if path.name == "__pycache__":
                errors.append(f"{rel}/{prel}: cache folder")
            continue
        if path.name in JUNK_NAMES or path.name.endswith(JUNK_SUFFIXES):
            errors.append(f"{rel}/{prel}: editor, OS or cache junk file")
        elif path.stat().st_size == 0:
            errors.append(f"{rel}/{prel}: empty file")
        if len(prel.parts) == 1 and prel.name != "SKILL.md":
            errors.append(f"{rel}/{prel}: file at the skill root; put it in references/, templates/, examples/, scripts/ or assets/")
        elif len(prel.parts) > 1 and prel.parts[0] not in STANDARD_DIRS:
            errors.append(f"{rel}/{prel}: folder '{prel.parts[0]}' is not one of {', '.join(sorted(STANDARD_DIRS))}")
        if path.suffix == ".md":
            body = path.read_text(encoding="utf-8", errors="replace")
            body = re.sub(r"^(```|~~~).*?^\1", "", body, flags=re.MULTILINE | re.DOTALL)
            body = re.sub(r"`[^`\n]*`", "", body)
            for target in MD_LINK.findall(body):
                if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#)", target, re.IGNORECASE):
                    continue
                clean = target.split("#", 1)[0]
                if clean and not link_target_ok(clean, path, skill_dir):
                    errors.append(f"{rel}/{prel}: link ({target}) does not resolve inside the skill folder")

    checker = skill_dir / "scripts" / "check-output.py"
    example = skill_dir / "examples" / "worked-example.md"
    if checker.is_file():
        proc = subprocess.run([sys.executable, "-I", str(checker)], capture_output=True, text=True, timeout=60)
        if proc.returncode != 2:
            errors.append(f"{rel}: checker with no argument must exit 2 (usage error), exited {proc.returncode}")
        if example.is_file():
            first, second = run_checker(checker, example), run_checker(checker, example)
            if first != second:
                errors.append(f"{rel}: checker gave different results on two runs of the worked example")
    if example.is_file() and "illustrative example" not in example.read_text(encoding="utf-8").lower():
        errors.append(f"{rel}: examples/worked-example.md must carry the label 'Illustrative example'")


def validate(skill_dir: Path, names: set[str], allow_missing_related: bool,
             strict: bool = False, legal: bool = False) -> list[str]:
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
            scan_text(path, errors, legal)

    if strict:
        strict_checks(skill_dir, fm, errors)

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
    known = {"--allow-missing-related", "--strict", "--check-legal", "-h", "--help"}
    unknown = [a for a in argv if a.startswith("-") and a not in known]
    if unknown or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 2 if unknown else 0
    allow = "--allow-missing-related" in argv
    strict = "--strict" in argv
    legal = "--check-legal" in argv
    targets = [a for a in argv if not a.startswith("--")]
    dirs = all_skill_dirs()
    names = {d.name for d in dirs}
    duplicates: dict[str, list[str]] = {}
    for d in dirs:
        duplicates.setdefault(d.name, []).append(str(d.relative_to(SKILLS)))
    if targets:
        dirs = [d for d in dirs if any(str(d.relative_to(SKILLS)).startswith(t.rstrip("/")) for t in targets)]
    if not dirs:
        print("No skills matched.")
        return 1
    failed = 0
    for d in dirs:
        errs = validate(d, names, allow, strict, legal)
        if strict and len(duplicates[d.name]) > 1:
            errs.append(f"{d.relative_to(ROOT)}: skill name also used by {', '.join(x for x in duplicates[d.name] if x != str(d.relative_to(SKILLS)))}")
        if errs:
            failed += 1
            print(f"FAIL {d.relative_to(SKILLS)}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS {d.relative_to(SKILLS)}")
    for path in sorted((SHARED).glob("*.md")):
        errs: list[str] = []
        scan_text(path, errs, legal)
        for e in errs:
            print(f"FAIL {e}")
            failed += 1
    print(f"\n{len(dirs) - min(failed, len(dirs))}/{len(dirs)} skills passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
