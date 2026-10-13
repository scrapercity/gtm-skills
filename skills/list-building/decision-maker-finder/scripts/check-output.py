#!/usr/bin/env python3
"""Check a decision maker report against the decision-maker-finder output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Account List",
    "Role Plan",
    "Waterfall Results",
    "Coverage by Role",
    "Validation Results",
    "Mobile Numbers",
    "Cost Estimate",
    "Sample Contacts",
    "Gaps and Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 35
STATUSES = ["valid", "valid_catch_all", "unknown", "invalid", "disposable"]
FOUND_BY = {"lead_db", "website_finder", "email_finder", "apollo", "user_upload"}
NO_MOBILE = {"none found", "not requested"}


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

    # Account list funnel: each stage equals the previous minus dropped.
    prev = None
    for r in table_rows(section(text, "Account List")):
        if len(r) < 4:
            return fail("Account List rows need Stage, Accounts, Dropped, Reason")
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None:
            return fail(f"Account List stage '{r[0]}' has non-numeric values")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"Account List does not add up at '{r[0]}'")
        prev = rows
    searched = prev
    if not searched:
        return fail("Account List must end with a positive accounts-searched count")

    # Role plan: at least one slot, each with a role and a Website Finder title.
    plan = table_rows(section(text, "Role Plan"))
    if not plan or any(len(r) < 5 or not r[1] or not r[4] for r in plan):
        return fail("Role Plan needs a buying role and a Website Finder jobTitle on every slot")

    # Waterfall: found + not found = input, and found never exceeds input.
    wf = table_rows(section(text, "Waterfall Results"))
    if len(wf) < 4:
        return fail("Waterfall Results needs at least 4 steps")
    for r in wf:
        if len(r) < 5:
            return fail("Waterfall rows need Step, Tool, Input, Found, Not found")
        i, f, n = num(r[2]), num(r[3]), num(r[4])
        if None in (i, f, n):
            return fail(f"Waterfall step '{r[0]}' has non-numeric counts")
        if f > i:
            return fail(f"Waterfall step '{r[0]}' found more than its input")
        if abs(f + n - i) > 0.5:
            return fail(f"Waterfall step '{r[0]}': found + not found != input")

    # Coverage: filled + held + empty = accounts searched, for every slot.
    cov = table_rows(section(text, "Coverage by Role"))
    if not cov:
        return fail("Coverage by Role is empty")
    for r in cov:
        vals = [num(c) for c in r[1:5]]
        if len(r) < 6 or None in vals:
            return fail(f"Coverage row '{r[0]}' needs numeric searched, filled, held, empty")
        s, f, h, e = vals
        if abs(f + h + e - s) > 0.5:
            return fail(f"Coverage row '{r[0]}': filled + held + empty != searched")
        if abs(s - searched) > 0.5:
            return fail(f"Coverage row '{r[0]}' searched {s:.0f} accounts, Account List says {searched:.0f}")

    # Validation: every status present; each column sums to its Total row.
    vrows = table_rows(section(text, "Validation Results"))
    by = {r[0].strip().lower(): r for r in vrows}
    for st in STATUSES:
        if st not in by:
            return fail(f"Validation Results missing status '{st}'")
    if "total" not in by:
        return fail("Validation Results needs a Total row")
    for col in range(1, len(by["total"])):
        tot = num(by["total"][col])
        parts = [num(by[st][col]) if len(by[st]) > col else None for st in STATUSES]
        if tot is None or None in parts:
            return fail("Validation Results has a non-numeric cell")
        if abs(sum(parts) - tot) > 0.5:
            return fail(f"Validation Results column {col} does not sum to its Total")

    # Sample contacts: role, tool, valid status, and an E.164 mobile or an explicit none.
    sample = table_rows(section(text, "Sample Contacts"))
    if len(sample) < 3:
        return fail("Sample Contacts needs at least 3 rows")
    any_mobile = False
    for r in sample:
        if len(r) < 8:
            return fail("Sample Contacts rows need 8 columns")
        if not r[4]:
            return fail(f"sample contact {r[1]} {r[2]} has no buying_role")
        if r[5].lower() not in FOUND_BY:
            return fail(f"sample contact {r[1]} {r[2]} has found_by '{r[5]}', expected one of {sorted(FOUND_BY)}")
        if r[6].lower() != "valid":
            return fail(f"sample contact {r[1]} {r[2]} is not email_status valid")
        mob = r[7].strip()
        if mob.lower() in NO_MOBILE:
            continue
        if not re.fullmatch(r"\+\d{8,15}", mob):
            return fail(f"mobile '{mob}' is not E.164 (or 'none found' / 'not requested')")
        any_mobile = True

    # Mobiles carry a stated use and a compliance note.
    mob = {r[0].lower(): r[1] for r in table_rows(section(text, "Mobile Numbers")) if len(r) > 1}
    found = num(mob.get("numbers found", ""))
    if (found and found > 0) or any_mobile:
        use = mob.get("stated use", "")
        comp = mob.get("compliance check", "")
        if not use or not re.search(r"tcpa|consent|dnc|do not call", comp, re.I):
            return fail("mobiles delivered without a stated use and a TCPA or consent compliance note")

    cost = section(text, "Cost Estimate")
    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: {searched:.0f} accounts, {len(wf)} waterfall steps reconcile, coverage and validation add up")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
