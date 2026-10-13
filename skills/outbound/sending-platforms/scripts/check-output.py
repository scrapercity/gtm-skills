#!/usr/bin/env python3
"""Check a finished sending platform plan.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import re
import sys
from pathlib import Path

REQUIRED = [
    "Summary",
    "Requirements",
    "Platform Decision",
    "Workspace Settings",
    "Column Map",
    "Import Procedure",
    "Suppression and Dedupe",
    "Webhooks to CRM",
    "Test Plan",
    "Cost",
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 4000
MAX_CAP = 50
DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
OVERRIDE = re.compile(
    r"(ignore_global_block_list|ignore_unsubscribe_list|ignore_community_bounce_list)\W{0,4}(true|on|yes)",
    re.IGNORECASE,
)
NEEDED_EVENTS = {
    "reply": re.compile(r"repl", re.IGNORECASE),
    "unsubscribe": re.compile(r"unsubscri", re.IGNORECASE),
    "bounce": re.compile(r"bounce", re.IGNORECASE),
}


def sections(text):
    out, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip().lower()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def table(block):
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    if not rows:
        return [], []
    return [h.lower() for h in rows[0]], rows[1:]


def col(header, name):
    for i, h in enumerate(header):
        if name in h:
            return i
    return -1


def fail(msg):
    print(f"FAIL - {msg}")
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/plan.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"usage: file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    sec = sections(text)
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")

    ph, prows = table(sec["platform decision"])
    ci = col(ph, "checked")
    if ci < 0 or len(prows) < 2:
        return fail("Platform Decision needs a Checked column and at least 2 options")
    for r in prows:
        if ci >= len(r) or not DATE.search(r[ci]):
            return fail(f"platform option without a vendor-page check date: {r[0]}")
    if not re.search(r"^decision:", sec["platform decision"], re.IGNORECASE | re.MULTILINE):
        return fail("Platform Decision needs a 'Decision:' line")

    _, wrows = table(sec["workspace settings"])
    caps = [r for r in wrows if r and "per mailbox" in r[0].lower()]
    if not caps:
        return fail("Workspace Settings needs a 'Daily limit per mailbox' row")
    m = re.search(r"\d+", caps[0][1] if len(caps[0]) > 1 else "")
    if not m or int(m.group(0)) > MAX_CAP:
        return fail(f"daily limit per mailbox must be {MAX_CAP} or less")
    if not any(r and "unsubscribe" in r[0].lower() for r in wrows):
        return fail("Workspace Settings needs an unsubscribe header row")

    mh, mrows = table(sec["column map"])
    fi, vi, si = col(mh, "fallback"), col(mh, "platform variable"), col(mh, "source column")
    if min(fi, vi, si) < 0:
        return fail("Column Map needs Source column, Platform variable and Fallback columns")
    if len(mrows) < 4:
        return fail("Column Map needs at least 4 rows")
    has_email = False
    for r in mrows:
        if max(fi, vi, si) >= len(r):
            return fail(f"column map row has too few cells: {' | '.join(r)[:80]}")
        if "email" in r[si].lower() and "email" in r[vi].lower():
            has_email = True
        if not r[fi].strip():
            return fail(f"column map row without a fallback: {r[si]}")
        joined = " ".join(r)
        if joined.count("{{") != joined.count("}}"):
            return fail(f"malformed merge tag in column map row: {r[si]}")
    if not has_email:
        return fail("Column Map needs an email row")

    if OVERRIDE.search(text):
        return fail("an import setting overrides the block list, unsubscribe list or bounce list")

    wh, whrows = table(sec["webhooks to crm"])
    ai = col(wh, "crm action")
    if ai < 0:
        return fail("Webhooks to CRM needs a CRM action column")
    covered = set()
    for r in whrows:
        joined = " ".join(r[: ai])
        for key, rx in NEEDED_EVENTS.items():
            if rx.search(joined):
                covered.add(key)
                if ai >= len(r) or not r[ai].strip() or r[ai].strip().lower() in {"none", "-"}:
                    return fail(f"{key} webhook row has no CRM action")
    missing = set(NEEDED_EVENTS) - covered
    if missing:
        return fail(f"Webhooks to CRM must cover: {', '.join(sorted(missing))}")

    if len(table(sec["test plan"])[1]) < 4:
        return fail("Test Plan needs at least 4 tests")
    if len(table(sec["import procedure"])[1]) < 5:
        return fail("Import Procedure needs at least 5 steps")
    if len(table(sec["suppression and dedupe"])[1]) < 3:
        return fail("Suppression and Dedupe needs at least 3 lists")
    cost = sec["cost"]
    if "$" not in cost or not re.search(r"^\|\s*total", cost, re.IGNORECASE | re.MULTILINE):
        return fail("Cost needs dollar figures and a Total row")

    print(f"PASS - {len(prows)} dated platform options, {len(mrows)} mapped columns with fallbacks, reply/unsubscribe/bounce webhooks mapped, no block list overrides")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
