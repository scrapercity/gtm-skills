#!/usr/bin/env python3
"""Scaffold a new skill folder that already meets the layout and the checker contract.

  python3 scripts/new-skill.py outbound linkedin-voice-notes
  python3 scripts/new-skill.py list-building dentist-list --dry-run

Writes skills/<category>/<name>/ with SKILL.md (every required section, in order),
references/framework-notes.md, templates/output-template.md, examples/worked-example.md
and scripts/check-output.py. Every field to write is marked [fill], so the new skill
fails scripts/validate-skills.py until it is finished: the checker fails the template
and the unfinished example, and SKILL.md is under the minimum length.

Refuses to overwrite an existing folder. Read docs/SKILL_AUTHORING.md before filling it in.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SKILL = """---
name: {name}
description: >-
  [fill] What the skill produces, deliverable first, in one sentence that stands
  on its own. Use when [fill] the phrases a user types and the situations.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "0.1.0"
  author: ScraperCity
  category: {category}
  tags:
    - "[fill]"
  related_skills:
    - using-scrapercity-skills
  frameworks:
    - "[fill] Person or company - the method, with a year"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
---

# {title}

## Overview

[fill] What the user gets and the mistake this skill prevents. Results only: replies,
meetings, revenue, cost. No legal content and no moralizing (docs/SKILL_AUTHORING.md).

## When to Use

- [fill] trigger phrase
- Use another skill instead for [fill].

## Authoritative Foundations

- **[fill] Named source** - the principle it contributes and where in the workflow it applies.

## Workflow

### 1. [fill] First step

[fill]

## ScraperCity Implementation

[fill] Exact tool ids from `references/scrapercity-catalog.md`, the count check before any
paid pull, and one worked cost estimate (units x catalog price = total).

## Output Format

[fill] Exactly what the user receives. Point to `templates/output-template.md`.

## Quality Check

- [ ] [fill] A pass or fail test the deliverable must meet.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| [fill] | [fill] | [fill] |

## Execution Artifacts

- `references/framework-notes.md` - which sources shape the skill and when to open each file.
- `templates/output-template.md` - the deliverable shell.
- `examples/worked-example.md` - a finished deliverable that passes the checker.
- `scripts/check-output.py` - run `python3 scripts/check-output.py <file>` on the deliverable.

## Related Skills

- `using-scrapercity-skills` - routes requests to this skill.
"""

NOTES = """# Framework Notes: {name}

[fill] One short section per named source: what it says (paraphrased, with a link) and which
workflow step uses it. Then a table of the files in `references/` and when to open each.

## Sources

- [fill] Publisher, title: https://
"""

TEMPLATE = """# [fill] Deliverable title

## Summary

[fill] Two or three sentences: what to do, for whom, and the number that decides success.

## Plan

| Step | Owner | Due | Setting or copy |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

## Cost

| Item | Units | Price | Total |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |
"""

EXAMPLE = """# [fill] Deliverable title

Illustrative example. [fill] Write a complete deliverable for an invented business on a
`.example` domain, with catalog prices worked through. Replace every [fill]; the checker
fails until you do.

## Summary

[fill]

## Plan

| Step | Owner | Due | Setting or copy |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

## Cost

| Item | Units | Price | Total |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |
"""

CHECKER = '''#!/usr/bin/env python3
"""Check a finished {name} deliverable.

  python3 scripts/check-output.py <deliverable.md>

Prints PASS and exits 0, or FAIL lines and exits 1. No argument: usage, exit 2.
Standard library only, no network.
"""

import re
import sys

REQUIRED = ["## Summary", "## Plan", "## Cost"]
PLACEHOLDER = re.compile(r"\\[(?:fill|todo|tbd)[^\\]]*\\]", re.IGNORECASE)
MIN_CHARS = 600


def table_rows(text, heading):
    section = text.split(heading, 1)[1].split("\\n## ", 1)[0] if heading in text else ""
    rows = [l for l in section.splitlines() if l.startswith("|")]
    return [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]


def money(cell):
    m = re.search(r"\\$?([\\d,]+(?:\\.\\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py <deliverable.md>")
        return 2
    text = open(argv[1], encoding="utf-8").read()
    fails = []
    if PLACEHOLDER.search(text):
        fails.append("unfilled [fill], [todo] or [tbd] marker")
    for heading in REQUIRED:
        if heading not in text:
            fails.append(f"missing section {{heading}}")
    if len(text) < MIN_CHARS:
        fails.append(f"under {{MIN_CHARS}} characters")
    # Skill-specific check 1: every plan row names an owner and a due date.
    plan = table_rows(text, "## Plan")
    if not plan:
        fails.append("Plan table has no rows")
    for row in plan:
        if len(row) < 3 or not row[1] or not re.search(r"\\d{{4}}-\\d{{2}}-\\d{{2}}", row[2]):
            fails.append(f"plan row without an owner and an ISO due date: {{row}}")
    # Skill-specific check 2: units x price equals total on every cost row (1 cent tolerance).
    for row in table_rows(text, "## Cost"):
        if len(row) >= 4:
            units, price, total = money(row[1]), money(row[2]), money(row[3])
            if None in (units, price, total) or abs(units * price - total) > 0.01:
                fails.append(f"cost row where units x price != total: {{row}}")
    # [fill] Replace or extend the two checks above with ones specific to this skill.
    for f in fails:
        print(f"FAIL - {{f}}")
    if fails:
        return 1
    print("PASS - {name} deliverable meets the checker")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
'''


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2 or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 2
    category, name = args
    if not NAME.match(name) or len(name) > 64 or re.search(r"claude|anthropic", name):
        print(f"FAIL - '{name}' must be 1-64 chars of a-z, 0-9 and single hyphens, without claude or anthropic")
        return 2
    if not (ROOT / "skills" / category).is_dir():
        print(f"FAIL - no category folder skills/{category}")
        return 2
    if any(p.parent.name == name for p in ROOT.glob("skills/*/*/SKILL.md")):
        print(f"FAIL - a skill named {name} already exists")
        return 1
    dest = ROOT / "skills" / category / name
    title = name.replace("-", " ").title()
    files = {
        "SKILL.md": SKILL.format(name=name, category=category, title=title),
        "references/framework-notes.md": NOTES.format(name=name),
        "templates/output-template.md": TEMPLATE,
        "examples/worked-example.md": EXAMPLE,
        "scripts/check-output.py": CHECKER.format(name=name),
    }
    for rel, body in files.items():
        print(f"{'would write' if '--dry-run' in argv else 'wrote'} {dest.relative_to(ROOT)}/{rel}")
        if "--dry-run" not in argv:
            path = dest / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            if rel.endswith(".py"):
                path.chmod(0o755)
    if "--dry-run" not in argv:
        print("Next: fill every [fill], add a deeper reference, add the skill to the router's routing matrix, "
              "then run python3 scripts/validate-skills.py " + f"{category}/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
