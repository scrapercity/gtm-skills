#!/usr/bin/env python3
"""Rewrite flow-style YAML lists in SKILL.md frontmatter as block lists.

The Agent Skills reference validator (skills-ref, command `agentskills validate`)
parses frontmatter with strict YAML and rejects flow-style lists such as
`tags: [cold-email, sequences]`. This script rewrites each such line as a block list
and leaves every other byte of the file alone. It then parses the old and new
frontmatter and refuses to write when the values differ.

  python3 scripts/normalize-frontmatter.py                  # every skill
  python3 scripts/normalize-frontmatter.py outbound/cold-calling
  python3 scripts/normalize-frontmatter.py --check          # exit 1 if any file would change

Requires Python 3.9+ and PyYAML.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FLOW = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z_][\w-]*):\s*\[(?P<items>.*)\]\s*$")
PLAIN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._/+()-]*$")
AMBIGUOUS = {"true", "false", "yes", "no", "on", "off", "null", "~"}


def scalar(item: object) -> str:
    text = str(item)
    if PLAIN.match(text) and text.lower() not in AMBIGUOUS and not re.fullmatch(r"[\d.]+", text):
        return text
    return json.dumps(text, ensure_ascii=False)


def normalize(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return text
    out = []
    for line in m.group(1).split("\n"):
        f = FLOW.match(line)
        if not f:
            out.append(line)
            continue
        items = yaml.safe_load(f"[{f.group('items')}]") or []
        if not items:
            out.append(line)
            continue
        out.append(f"{f.group('indent')}{f.group('key')}:")
        out.extend(f"{f.group('indent')}  - {scalar(i)}" for i in items)
    new_fm = "\n".join(out)
    if yaml.safe_load(new_fm) != yaml.safe_load(m.group(1)):
        raise ValueError("rewritten frontmatter parses to different values")
    return f"---\n{new_fm}\n---\n" + text[m.end():]


def main(argv: list[str]) -> int:
    check = "--check" in argv
    targets = [a.rstrip("/") for a in argv if not a.startswith("--")]
    files = sorted(SKILLS.glob("*/*/SKILL.md"))
    if targets:
        files = [f for f in files if any(str(f.parent.relative_to(SKILLS)).startswith(t) for t in targets)]
    changed = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        try:
            new = normalize(text)
        except ValueError as exc:
            print(f"FAIL - {f.relative_to(ROOT)}: {exc}")
            return 1
        if new != text:
            changed += 1
            if check:
                print(f"would rewrite {f.relative_to(ROOT)}")
            else:
                f.write_text(new, encoding="utf-8")
                print(f"rewrote {f.relative_to(ROOT)}")
    if check and changed:
        print(f"FAIL - {changed} SKILL.md files use flow-style lists (run scripts/normalize-frontmatter.py)")
        return 1
    print(f"PASS - {len(files) - changed if check else len(files)} SKILL.md files use block lists" if check
          else f"{changed} of {len(files)} SKILL.md files rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
