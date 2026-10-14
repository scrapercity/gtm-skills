#!/usr/bin/env python3
"""Repo-level checks for everything outside the skill folders.

  python3 scripts/check-repo.py                # every check below
  python3 scripts/check-repo.py --check-legal  # also fail repo docs that name a law or regulator

Checks:
  files       the community, docs and metadata files exist; no root CLAUDE.md (the Claude
              Code plugin validator warns on one)
  versions    plugin.json, the marketplace entry and CITATION.cff carry the same version,
              and CHANGELOG.md's newest release heading matches it
  manifests   plugin.json lists every category folder that holds skills, and only those
  installer   every install.sh bundle names existing skills; docs/INSTALL.md documents every
              target and bundle install.sh accepts
  workflows   least-privilege permissions; every action pinned to a full commit SHA
  rules       the author docs state both owner rules ("No legal content", "No moralizing")
  copy        no em or en dashes and no restricted names in repo docs, scripts and templates
  secrets     no private keys, cloud or API keys, or literal ScraperCity keys in any file
              git would publish (values are never printed)
  junk        no editor, OS or merge leftovers anywhere in the repo

Exit 0 when every check passes, 1 otherwise. Requires Python 3.9+ and PyYAML.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "README.md", "LICENSE", "AGENTS.md", "CHANGELOG.md", "CITATION.cff", "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md", "GOVERNANCE.md", "SECURITY.md", "SUPPORT.md", "install.sh", "skills.lock",
    "taxonomy.csv", "references/pitfalls-index.md", "references/scrapercity-catalog.md",
    ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".github/workflows/validate.yml",
    ".github/dependabot.yml", ".github/pull_request_template.md", ".githooks/pre-commit",
    "docs/ARCHITECTURE.md", "docs/INSTALL.md", "docs/INTEGRITY.md", "docs/QUALITY_BAR.md",
    "docs/RELEASE_PROCESS.md", "docs/REPO_TOPICS.md", "docs/SKILL_AUTHORING.md", "docs/SOURCE_STANDARDS.md",
    "scripts/check-all.sh", "scripts/regenerate.sh",
]
# Files where authors read the rules. Each must state both owner rules (Oct 13 2026).
RULE_DOCS = [
    "docs/SKILL_AUTHORING.md", "docs/QUALITY_BAR.md", "docs/SOURCE_STANDARDS.md", "docs/RELEASE_PROCESS.md",
    "CONTRIBUTING.md", "GOVERNANCE.md", "SUPPORT.md", "README.md", "CHANGELOG.md",
    ".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/improvement.yml",
    ".github/ISSUE_TEMPLATE/skill-request.yml",
]
RULE_MARKERS = ["No legal content", "No moralizing"]
SECRET_PATTERNS = {
    "private key": r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----",
    "AWS key": r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
    "GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b",
    "Slack token": r"\bxox[abpr]-[A-Za-z0-9-]{10,}",
    "OpenAI-style key": r"\bsk-[A-Za-z0-9_-]{32,}",
    "Anthropic key": r"\bsk-ant-[A-Za-z0-9_-]{20,}",
    "Google API key": r"\bAIza[0-9A-Za-z_-]{35}\b",
    "payment processor live key": r"\b(?:sk|rk)_live_[A-Za-z0-9]{24,}\b",
    "ScraperCity key": r"SCRAPERCITY_API_KEY\s*[=:]\s*[\"']?[A-Za-z0-9]{20,}",
}
JUNK = re.compile(r"(?:^|/)(?:\.DS_Store|Thumbs\.db)$|\.(?:orig|rej|swp|swo|bak)$|~$")
DASHES = re.compile("[\u2013\u2014]")
TEXT_SUFFIXES = {".md", ".py", ".mjs", ".sh", ".yml", ".yaml", ".json", ".cff", ".csv", ".txt", ""}


def load_validator():
    sys.dont_write_bytecode = True  # keep scripts/__pycache__ out of the checkout
    spec = importlib.util.spec_from_file_location("validate_skills", ROOT / "scripts" / "validate-skills.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def git_files() -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            capture_output=True, text=True, check=True, timeout=30,
        ).stdout
        names = [n for n in out.split("\0") if n]
    except (OSError, subprocess.SubprocessError):
        names = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if ".git" not in p.parts]
    return [ROOT / n for n in sorted(set(names)) if (ROOT / n).is_file() and not (ROOT / n).is_symlink()]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def check_files(errors: list[str]) -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"files: missing {rel}")
    if (ROOT / "CLAUDE.md").exists():
        errors.append("files: root CLAUDE.md (claude plugin validate warns; put agent notes in AGENTS.md)")


def check_versions(errors: list[str]) -> str:
    plugin = json.loads(read(".claude-plugin/plugin.json"))
    market = json.loads(read(".claude-plugin/marketplace.json"))
    version = str(plugin.get("version", ""))
    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")]
    if not entries:
        errors.append(f"versions: marketplace.json has no entry named {plugin.get('name')}")
    for entry in entries:
        if str(entry.get("version", version)) != version:
            errors.append(f"versions: marketplace entry {entry.get('version')} != plugin.json {version}")
    m = re.search(r"^version:\s*\"?([^\"\n]+)\"?", read("CITATION.cff"), re.M)
    if not m or m.group(1).strip() != version:
        errors.append(f"versions: CITATION.cff version {m.group(1) if m else 'missing'} != plugin.json {version}")
    releases = re.findall(r"^## (\d+\.\d+\.\d+)\b", read("CHANGELOG.md"), re.M)
    if not releases or releases[0] != version:
        errors.append(f"versions: newest CHANGELOG release {releases[0] if releases else 'missing'} != plugin.json {version}")
    return version


def check_manifests(errors: list[str]) -> None:
    plugin = json.loads(read(".claude-plugin/plugin.json"))
    listed = {str(p).strip("./").rstrip("/") for p in plugin.get("skills", [])}
    on_disk = {f"skills/{p.parent.parent.name}" for p in ROOT.glob("skills/*/*/SKILL.md")}
    for missing in sorted(on_disk - listed):
        errors.append(f"manifests: plugin.json skills does not list {missing}/")
    for extra in sorted(listed - on_disk):
        errors.append(f"manifests: plugin.json skills lists {extra}/, which holds no skills")


def check_installer(errors: list[str]) -> None:
    text = read("install.sh")
    skills = {p.parent.name for p in ROOT.glob("skills/*/*/SKILL.md")}
    targets = re.search(r'^ALL_TARGETS="([^"]+)"', text, re.M)
    bundles = re.search(r'^BUNDLES="([^"]+)"', text, re.M)
    if not targets or not bundles:
        errors.append("installer: ALL_TARGETS or BUNDLES not found in install.sh")
        return
    body = re.search(r"^bundle_skills\(\) \{(.*?)^\}", text, re.M | re.S)
    for name, members in re.findall(r'^\s+([a-z0-9-]+)\) echo "([^"]+)"', body.group(1) if body else "", re.M):
        for skill in members.split():
            if skill not in skills:
                errors.append(f"installer: bundle {name} names missing skill {skill}")
    install_doc = read("docs/INSTALL.md")
    for word in targets.group(1).split() + bundles.group(1).split():
        if f"`{word}`" not in install_doc:
            errors.append(f"installer: docs/INSTALL.md does not document `{word}`")


def check_workflows(errors: list[str]) -> None:
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        text = wf.read_text(encoding="utf-8")
        rel = wf.relative_to(ROOT)
        if not re.search(r"^permissions:\s*\n\s+contents: read\s*$", text, re.M):
            errors.append(f"workflows: {rel} must set top-level permissions to contents: read")
        for use in re.findall(r"uses:\s*([^\s#]+)", text):
            if use.startswith("./"):
                continue
            if not re.search(r"@[0-9a-f]{40}$", use):
                errors.append(f"workflows: {rel} uses {use} without a full commit SHA")


def check_rules(errors: list[str]) -> None:
    for rel in RULE_DOCS:
        if not (ROOT / rel).is_file():
            continue
        text = read(rel)
        for marker in RULE_MARKERS:
            if marker.lower() not in text.lower():
                errors.append(f"rules: {rel} does not state the owner rule '{marker}'")


def check_text(files: list[Path], validator, legal: bool, errors: list[str]) -> None:
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("skills/") or rel in {"skills.lock"}:
            continue  # validate-skills.py owns the skill folders
        if rel.startswith("references/") and path.suffix == ".md":
            continue  # validate-skills.py scans the root references
        if path.suffix not in TEXT_SUFFIXES:
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        for i, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
            if DASHES.search(line):
                errors.append(f"copy: {rel}:{i}: em or en dash")
            if validator.restricted_hit(line):
                errors.append(f"copy: {rel}:{i}: restricted name")
            if legal and rel not in {"scripts/validate-skills.py", "taxonomy.csv"}:
                for hit in validator.legal_hits(line, rel):
                    errors.append(f"legal: {rel}:{i}: {hit}")


def check_secrets(files: list[Path], errors: list[str]) -> None:
    compiled = {k: re.compile(v) for k, v in SECRET_PATTERNS.items()}
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if rel == "scripts/check-repo.py":
            continue  # holds the patterns themselves
        if path.name == ".env" or (path.name.startswith(".env.") and path.name not in {".env.example", ".env.sample"}):
            errors.append(f"secrets: {rel} is an environment file and must not be committed")
        data = path.read_bytes()
        if b"\0" in data:
            continue
        for i, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
            for label, pattern in compiled.items():
                if pattern.search(line):
                    errors.append(f"secrets: {rel}:{i}: possible {label} (value not printed); remove it and rotate the key")


def check_junk(files: list[Path], errors: list[str]) -> None:
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if JUNK.search(rel):
            errors.append(f"junk: {rel}")


def main(argv: list[str]) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    legal = "--check-legal" in argv
    validator = load_validator()
    files = git_files()
    errors: list[str] = []
    check_files(errors)
    version = check_versions(errors)
    check_manifests(errors)
    check_installer(errors)
    check_workflows(errors)
    check_rules(errors)
    check_text(files, validator, legal, errors)
    check_secrets(files, errors)
    check_junk(files, errors)
    for e in errors:
        print(f"FAIL - {e}")
    if errors:
        print(f"\n{len(errors)} repo check(s) failed")
        return 1
    print(f"PASS - repo checks: version {version}, {len(files)} files scanned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
