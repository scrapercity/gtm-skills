#!/usr/bin/env python3
"""Check a cold email campaign plan produced with the cold-email-strategy skill.

Usage: check-output.py path/to/plan.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import re
import sys

REQUIRED = [
    "Campaign Summary",
    "Offer",
    "Campaign Cells",
    "Contact Thesis",
    "List Sources and Cost",
    "Touch Map",
    "Volume and Capacity",
    "Test Plan",
    "Measurement Funnel",
    "Compliance and Suppression",
    "Handoff",
]
MIN_WORDS = 600
MIN_TABLE_ROWS = 25
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)


def sections(text):
    out = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip().lower()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def tables(block):
    """Return a list of tables; each table is a list of dicts keyed by lowercased header."""
    result, rows = [], []
    for line in block.splitlines() + [""]:
        if line.strip().startswith("|"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif rows:
            if len(rows) >= 2 and all(re.fullmatch(r":?-+:?", c) for c in rows[1] if c):
                head = [h.lower() for h in rows[0]]
                result.append([dict(zip(head, r)) for r in rows[2:]])
            rows = []
    return result


def fail(msg):
    print(f"FAIL - {msg}")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/plan.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the plan: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    words = len(text.split())
    if words < MIN_WORDS:
        fail(f"plan has {words} words, minimum is {MIN_WORDS}")
    all_rows = [r for t in tables(text) for r in t]
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"plan has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    # Skill check 1: every campaign cell has a segment, an offer and a trigger.
    cell_rows = [r for t in tables(secs["campaign cells"]) for r in t]
    if not cell_rows:
        fail("Campaign Cells has no table rows")
    for r in cell_rows:
        for col in ("segment", "offer", "trigger"):
            if not r.get(col):
                fail(f"campaign cell '{r.get('cell', '?')}' has no {col}")

    # Skill check 2: every touch row has a branch.
    touch_rows = [r for t in tables(secs["touch map"]) for r in t]
    if len(touch_rows) < 3:
        fail("Touch Map needs at least 3 touch rows")
    for r in touch_rows:
        if "branch" not in r or len(r["branch"]) < 5:
            fail(f"touch '{r.get('touch', '?')}' has no branch")

    # Skill check 3: cost section carries a dollar total.
    cost = secs["list sources and cost"]
    if not re.search(r"total[^\n]*\$\d", cost, re.IGNORECASE):
        fail("List Sources and Cost needs a Total row with a $ figure")

    # Skill check 4: funnel measures positive replies and meetings; tests never decide on opens.
    funnel = secs["measurement funnel"].lower()
    if "positive" not in funnel or "meeting" not in funnel:
        fail("Measurement Funnel must track positive replies and meetings")
    for r in [r for t in tables(secs["test plan"]) for r in t]:
        metric = r.get("decision metric", "").lower()
        if not metric:
            fail("every test needs a decision metric")
        if "open" in metric:
            fail(f"test '{r.get('test', '?')}' decides on opens; use positive replies per 100 delivered")

    # Skill check 5: capacity shows its inputs.
    cap = secs["volume and capacity"].lower()
    for needed in ("inbox", "per day", "total sends"):
        if needed not in cap:
            fail(f"Volume and Capacity is missing '{needed}'")

    print(f"PASS - {len(cell_rows)} cells, {len(touch_rows)} touches with branches, {len(all_rows)} table rows, {words} words")
    sys.exit(0)


if __name__ == "__main__":
    main()
