#!/usr/bin/env python3
"""Check a local business list report against the local-business-list output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Search Definition",
    "Geography Split",
    "Count Check",
    "Source Results",
    "Cleaning Funnel",
    "Validation Results",
    "Cost Estimate",
    "Output Schema",
    "Sample Rows",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 45
STATUSES = ["valid", "valid_catch_all", "unknown", "invalid", "disposable"]
E164 = re.compile(r"\+\d{8,15}")


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
    angle = re.search(r"<[A-Za-z][^>@\n]{0,60}>", text)
    if angle:
        return fail("angle-bracket placeholder left in: " + angle.group(0))
    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    all_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if all_rows < MIN_TABLE_ROWS:
        return fail(f"only {all_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Geography: sub-area counts sum to the Total row in both count columns.
    geo = table_rows(section(text, "Geography Split"))
    total = next((r for r in geo if r[0].lower().startswith("total")), None)
    subs = [r for r in geo if r is not total]
    if total is None or len(subs) < 2:
        return fail("Geography Split needs 2+ sub-areas and a Total row")
    for col, label in ((1, "A"), (2, "C")):
        vals = [num(r[col]) if len(r) > col else None for r in subs]
        if None in vals or num(total[col]) is None:
            return fail(f"Geography Split column {label} has a non-numeric cell")
        if abs(sum(vals) - num(total[col])) > 0.5:
            return fail(f"Geography Split column {label} does not sum to its Total")
        if col == 2:
            for r, c in zip(subs, vals):
                if c > num(r[1]):
                    return fail(f"sub-area '{r[0]}' has more website-and-email rows than businesses")
    pulled_c = num(total[2])

    # Count check: four calls with numeric totals that never grow as filters are added.
    counts = [num(r[2]) for r in table_rows(section(text, "Count Check")) if len(r) > 2]
    if len(counts) < 3 or None in counts:
        return fail("Count Check needs calls A to C (or D) with numeric pagination.total")
    if any(b > a for a, b in zip(counts, counts[1:])):
        return fail("Count Check totals grow as filters are added")

    # Source results: new rows never exceed returned rows.
    for r in table_rows(section(text, "Source Results")):
        if len(r) < 5:
            return fail("Source Results rows need Source, Inputs, Returned, New after dedupe, Cost")
        ret, new = num(r[2]), num(r[3])
        if ret is None or new is None:
            return fail(f"Source Results '{r[0]}' has non-numeric counts")
        if new > ret:
            return fail(f"Source Results '{r[0]}' added more rows than it returned")

    # Funnel: starts at the database pull, each stage = previous + change.
    funnel = table_rows(section(text, "Cleaning Funnel"))
    if len(funnel) < 6:
        return fail("Cleaning Funnel needs at least 6 stages")
    prev = None
    for r in funnel:
        if len(r) < 4 or not r[3]:
            return fail(f"Cleaning Funnel stage '{r[0]}' needs Rows, Change and a Reason")
        rows, change = num(r[1]), num(r[2])
        if rows is None or change is None:
            return fail(f"Cleaning Funnel stage '{r[0]}' has non-numeric values")
        if prev is not None and abs(prev + change - rows) > 0.5:
            return fail(f"Cleaning Funnel does not add up at '{r[0]}'")
        prev = rows
    if abs(num(funnel[0][1]) - pulled_c) > 0.5:
        return fail("Cleaning Funnel must start from the database pull (Geography Total, column C)")

    # Validation: statuses sum to total; total equals the stage before validation; valid equals send-ready.
    found = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Validation Results")) if len(r) > 1}
    for st in STATUSES:
        if found.get(st) is None:
            return fail(f"Validation Results missing status '{st}'")
    vtotal = next((v for k, v in found.items() if k.startswith("total")), None)
    if vtotal is None or abs(sum(found[s] for s in STATUSES) - vtotal) > 0.5:
        return fail("validation statuses do not sum to Total validated")
    if abs(vtotal - num(funnel[-2][1])) > 0.5:
        return fail("Total validated must equal the funnel stage just before validation")
    if abs(found["valid"] - num(funnel[-1][1])) > 0.5:
        return fail("send-ready rows (last funnel stage) must equal the valid count")

    # Sample rows: website domain, email, valid status, E.164 phone.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if len(r) < 7:
            return fail("Sample Rows need 7 columns")
        if not r[1] or "." not in r[1]:
            return fail(f"sample '{r[0]}' has no domain")
        if "@" not in r[2]:
            return fail(f"sample '{r[0]}' has no email")
        if r[3].lower() != "valid":
            return fail(f"sample '{r[0]}' is not email_status valid")
        if not E164.fullmatch(r[4]):
            return fail(f"sample '{r[0]}' phone '{r[4]}' is not E.164")

    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: {len(subs)} sub-areas sum, funnel reconciles to {found['valid']:.0f} send-ready, samples have website, valid email and E.164 phone")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
