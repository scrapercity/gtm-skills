#!/usr/bin/env python3
"""Check a finished sending infrastructure plan.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import re
import sys
from pathlib import Path

REQUIRED = [
    "Summary",
    "Inputs",
    "Capacity Plan",
    "Mailbox Provider Decision",
    "Sending Domains",
    "DNS Records",
    "Cost Estimate",
    "Launch Checklist",
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 2500
MAX_CAP = 50


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


def table_rows(block):
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


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

    inputs = table_rows(sec["inputs"])
    main_domain = ""
    for row in inputs:
        if row and row[0].lower().startswith("main domain") and len(row) > 1:
            m = re.search(r"([a-z0-9-]+\.[a-z.]+)", row[1].lower())
            main_domain = m.group(1) if m else ""
    if not main_domain:
        return fail("Inputs table needs a 'Main domain' row with a domain")

    cap_rows = [r for r in table_rows(sec["capacity plan"]) if r and "cap per mailbox" in r[0].lower()]
    if not cap_rows:
        return fail("Capacity Plan needs a 'Cap per mailbox' row")
    nums = re.findall(r"\d+", cap_rows[0][-1])
    if not nums or int(nums[0]) > MAX_CAP:
        return fail(f"cap per mailbox must be {MAX_CAP} or less")
    if len(table_rows(sec["capacity plan"])) < 6:
        return fail("Capacity Plan table needs at least 6 rows")

    domain_rows = table_rows(sec["sending domains"])
    if len(domain_rows) < 2:
        return fail("Sending Domains table needs at least 2 domains")
    sending = []
    roles = set()
    for row in domain_rows:
        d = row[0].lower()
        if d == main_domain:
            return fail(f"main domain {main_domain} listed as a sending domain")
        sending.append(d)
        if len(row) > 1:
            roles.add(row[1].lower())
    if "reserve" not in roles:
        return fail("Sending Domains needs at least one Reserve domain")

    dns = table_rows(sec["dns records"])
    by_domain = {}
    for row in dns:
        if len(row) < 5:
            continue
        by_domain.setdefault(row[0].lower(), []).append(row)
    for d in sending:
        recs = by_domain.get(d, [])
        kinds = [r[1].upper() for r in recs]
        for need in ("MX", "SPF", "DKIM", "DMARC"):
            if need not in kinds:
                return fail(f"{d} has no {need} row in DNS Records")
        if kinds.count("SPF") != 1:
            return fail(f"{d} must have exactly one SPF row")
        for r in recs:
            if r[1].upper() == "DMARC" and "rua=mailto:" not in r[4].lower():
                return fail(f"{d} DMARC value has no rua=mailto:")
            if r[1].upper() == "SPF" and not r[4].lower().startswith("v=spf1"):
                return fail(f"{d} SPF value must start with v=spf1")

    cost = sec["cost estimate"]
    if "$" not in cost or not re.search(r"^\|\s*total", cost, re.IGNORECASE | re.MULTILINE):
        return fail("Cost Estimate needs dollar figures and a Total row")
    if len(table_rows(sec["launch checklist"])) < 4:
        return fail("Launch Checklist needs at least 4 steps")

    print(f"PASS - {len(sending)} sending domains, all with MX, SPF, DKIM and DMARC (rua); main domain {main_domain} excluded")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
