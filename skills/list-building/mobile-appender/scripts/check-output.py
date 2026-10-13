#!/usr/bin/env python3
"""Check a mobile append report against the mobile-appender output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Input Summary",
    "Compliance Gate",
    "Cost Estimate",
    "Append Funnel",
    "Line Type and DNC",
    "Dial Rules",
    "Output Schema",
    "Sample Rows",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 40
PRICE = 0.25
E164 = re.compile(r"^\+[1-9]\d{7,14}$")
LAW = re.compile(r"TCPA|TSR|Telemarketing|47 (U\.S\.C|CFR)|DNC|Do Not Call|CASL|CRTC|PECR|TPS|GDPR|Act|Chennette", re.I)
DIAL = {"callable_manual", "callable_auto_consented", "hold_dnc", "hold_internal_dnc", "hold_line_type", "hold_shared_number"}
SCENARIOS = ["low", "expected", "high", "ceiling"]


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


def all_tables(block):
    """Return rows of every table in a block, headers removed."""
    tables, cur = [], []
    for line in block.splitlines() + [""]:
        s = line.strip()
        if s.startswith("|"):
            cur.append(s)
        elif cur:
            tables.append(table_rows("\n".join(cur)))
            cur = []
    return tables


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
    total_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if total_rows < MIN_TABLE_ROWS:
        return fail(f"only {total_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Every compliance row names a law.
    gate = table_rows(section(text, "Compliance Gate"))
    if len(gate) < 4:
        return fail("Compliance Gate needs at least 4 questions")
    for r in gate:
        if len(r) < 4 or not LAW.search(r[2]):
            return fail(f"Compliance Gate row '{r[0]}' does not name a law")

    # Hit rate and scenarios: found = inputs x rate, cost = found x $0.25.
    cost = section(text, "Cost Estimate")
    if not re.search(r"hit rate\s*\d+(\.\d+)?%", cost, re.I):
        return fail("Cost Estimate must state the pilot hit rate as a percentage")
    tables = all_tables(cost)
    scen = {r[0].strip().lower(): r for t in tables for r in t if r and r[0].strip().lower() in SCENARIOS}
    for s in SCENARIOS:
        if s not in scen:
            return fail(f"Cost Estimate missing scenario '{s}'")
        r = scen[s]
        if len(r) < 5:
            return fail(f"scenario '{s}' needs Inputs, Hit rate, Numbers found, Cost")
        inputs, rate, found, dollars = num(r[1]), num(r[2]), num(r[3]), num(r[4].replace("$", ""))
        if None in (inputs, rate, found, dollars):
            return fail(f"scenario '{s}' has a non-numeric cell")
        if abs(inputs * rate / 100 - found) > 1:
            return fail(f"scenario '{s}': {inputs:.0f} x {rate:.0f}% is not {found:.0f}")
        if abs(found * PRICE - dollars) > 0.01:
            return fail(f"scenario '{s}': {found:.0f} x $0.25 is not ${dollars:.2f}")
    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a Total row with a $ figure")

    # Funnel adds up.
    funnel = table_rows(section(text, "Append Funnel"))
    if len(funnel) < 5:
        return fail("Append Funnel needs at least 5 stages")
    prev, found_rows = None, None
    for r in funnel:
        if len(r) < 4:
            return fail("Append Funnel rows need Stage, Rows, Dropped, Reason")
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None:
            return fail(f"Append Funnel stage '{r[0]}' has non-numeric values")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"Append Funnel does not add up at '{r[0]}'")
        if "found" in r[0].lower() and found_rows is None:
            found_rows = rows
        prev = rows
    if found_rows is None:
        return fail("Append Funnel needs a 'Mobiles found' stage")

    # Dial rules use the vocabulary and sum to numbers found.
    rules = table_rows(section(text, "Dial Rules"))
    seen = 0
    for r in rules:
        if r[0].strip() not in DIAL:
            return fail(f"Dial Rules value '{r[0]}' is not in the dial_status vocabulary")
        seen += num(r[1]) or 0
    if abs(seen - found_rows) > 0.5:
        return fail(f"Dial Rules counts sum to {seen:.0f}, but {found_rows:.0f} mobiles were found")

    # Sample rows: E.164, valid dial status, callable rows are DNC clear.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if len(r) < 8:
            return fail("Sample Rows need 8 columns")
        mobile, dnc, status, sms = r[3].strip(), r[5].strip().lower(), r[6].strip(), r[7].strip().lower()
        if not E164.match(mobile):
            return fail(f"sample mobile '{mobile}' is not E.164")
        if status not in DIAL:
            return fail(f"sample dial_status '{status}' is not in the vocabulary")
        if status.startswith("callable") and dnc != "clear":
            return fail(f"sample row {r[0]} is callable but DNC status is '{dnc}'")
        if sms not in ("yes", "no"):
            return fail(f"sample row {r[0]} sms_allowed must be yes or no")

    print(f"PASS - {path.name}: {len(gate)} compliance rows name a law, scenarios price at $0.25, funnel adds up, {len(sample)} E.164 sample rows")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
