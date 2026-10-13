#!/usr/bin/env python3
"""Check an ICP list report against the icp-list-builder output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "ICP Definition",
    "Filters Used",
    "Count Check",
    "Pull Funnel",
    "Validation Results",
    "Cost Estimate",
    "Output Schema",
    "Sample Rows",
    "Next Steps",
]
MIN_CHARS = 2500
MIN_TABLE_ROWS = 30
BUCKETS = ["valid", "catch_all", "unknown", "invalid", "disposable"]


def num(text):
    m = re.search(r"-?\d[\d,]*\.?\d*", text or "")
    return float(m.group(0).replace(",", "")) if m else None


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def table_rows(block):
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|") or re.match(r"^\|[\s:|-]+\|$", s):
            continue
        rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows[1:] if rows else []


def fail(msg):
    print("FAIL - " + msg)
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/report.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/report.md (file not found)")
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")

    headings = {h.strip().lower() for h in re.findall(r"^## (.+?)\s*$", text, re.M)}
    missing = [h for h in REQUIRED if h.lower() not in headings]
    if missing:
        return fail("missing sections: " + ", ".join(missing))
    hit = re.search(r"\[(fill|todo|tbd)[^\]]*\]", text, re.I)
    if hit:
        return fail("placeholder left in: " + hit.group(0))
    angle = re.search(r"<[A-Za-z][^>\n]{0,60}>", text)
    if angle:
        return fail("angle-bracket placeholder left in: " + angle.group(0))
    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    all_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if all_rows < MIN_TABLE_ROWS:
        return fail(f"only {all_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # ICP evidence: at least 3 example customers.
    if len(table_rows(section(text, "ICP Definition"))) < 3:
        return fail("ICP Definition needs at least 3 example customers")

    # Count check must show a numeric pagination total.
    counts = [num(r[1]) for r in table_rows(section(text, "Count Check")) if len(r) > 1]
    if not any(c is not None and c > 0 for c in counts):
        return fail("Count Check has no numeric pagination.total")

    # Funnel must decrease and each row must equal previous minus dropped.
    funnel = table_rows(section(text, "Pull Funnel"))
    if len(funnel) < 5:
        return fail("Pull Funnel needs at least 5 stages")
    prev = None
    for r in funnel:
        if len(r) < 4:
            return fail("Pull Funnel rows need Stage, Rows, Dropped, Reason")
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None:
            return fail(f"Pull Funnel stage '{r[0]}' has non-numeric rows or dropped")
        if not r[3]:
            return fail(f"Pull Funnel stage '{r[0]}' has no reason")
        if prev is not None:
            if rows > prev:
                return fail(f"Pull Funnel grows at '{r[0]}'")
            if abs(prev - dropped - rows) > 0.5:
                return fail(f"Pull Funnel does not add up at '{r[0]}': {prev:.0f} - {dropped:.0f} != {rows:.0f}")
        prev = rows

    # Validation buckets present and summing to the total.
    vrows = table_rows(section(text, "Validation Results"))
    found = {r[0].strip().lower(): num(r[1]) for r in vrows if len(r) > 1}
    for b in BUCKETS:
        if b not in found or found[b] is None:
            return fail(f"Validation Results missing bucket '{b}'")
    total = next((v for k, v in found.items() if k.startswith("total")), None)
    if total is None:
        return fail("Validation Results needs a Total validated row")
    if abs(sum(found[b] for b in BUCKETS) - total) > 0.5:
        return fail("validation buckets do not sum to Total validated")

    # Every sample row carries an email status, and it is valid.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if "valid" not in [c.lower() for c in r]:
            return fail("every sample row must show email_status valid")

    # Cost estimate shows a dollar total.
    cost = section(text, "Cost Estimate")
    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: {len(funnel)} funnel stages add up, validation buckets sum to {total:.0f}, cost total present")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
