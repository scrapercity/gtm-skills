#!/usr/bin/env python3
"""Check a skip trace report against the skip-tracer output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Purpose and Permissible Use",
    "Input Profile",
    "Identifier Plan",
    "Cost Estimate",
    "Match Scoring",
    "Results Funnel",
    "Contact Results",
    "Compliance Check",
    "Sample Rows",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 35
BANDS = [("confirmed", 80, 100), ("probable", 60, 79), ("weak", 40, 59), ("no_match", 0, 39)]
STATUSES = {"callable_manual", "hold_dnc", "hold_internal_dnc", "do_not_call_deceased", "mail_only"}
E164 = re.compile(r"^\+[1-9]\d{7,14}$")
LAW = re.compile(r"FCRA|TCPA|TSR|47 (U\.S\.C|CFR)|Regulation [FO]|12 CFR|15 U\.S\.C|CAN-SPAM|SB \d+|Act|Code", re.I)
PRICES = {"find_people": 0.0199, "distress": 0.05}


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
    total_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if total_rows < MIN_TABLE_ROWS:
        return fail(f"only {total_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # FCRA boundary stated.
    purpose = section(text, "Purpose and Permissible Use").lower()
    if "fcra" not in purpose:
        return fail("Purpose and Permissible Use must cite the FCRA")
    for word in ("tenant", "employment", "credit"):
        if word not in purpose:
            return fail(f"Purpose and Permissible Use must rule out {word} decisions")

    # Cost lines priced at catalog rates.
    for r in table_rows(section(text, "Cost Estimate")):
        if len(r) < 4 or r[0].lower().startswith("total"):
            continue
        line, units, cost = r[0].lower(), num(r[1]), num(r[3].replace("$", ""))
        if units is None or cost is None:
            continue
        if "find_people" in line:
            price = PRICES["find_people"]
        elif "property_lookup" in line:
            price = 0.25 if "owner" in line else 0.15
        elif "distress" in line:
            price = PRICES["distress"]
        else:
            continue
        if abs(units * price - cost) > 0.01:
            return fail(f"cost line '{r[0]}': {units:.0f} x ${price} is not ${cost:.2f}")
    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a Total row with a $ figure")

    # Bands present and summing to total searched.
    counts = {r[0].strip().lower(): num(r[2]) for r in table_rows(section(text, "Match Scoring")) if len(r) > 2}
    for name, _, _ in BANDS:
        if counts.get(name) is None:
            return fail(f"Match Scoring missing band '{name}'")
    total = next((v for k, v in counts.items() if k.startswith("total")), None)
    if total is None or abs(sum(counts[b[0]] for b in BANDS) - total) > 0.5:
        return fail("Match Scoring bands do not sum to Total searched")

    # Funnel adds up and never grows.
    funnel = table_rows(section(text, "Results Funnel"))
    if len(funnel) < 3:
        return fail("Results Funnel needs at least 3 stages")
    prev = None
    for r in funnel:
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None or len(r) < 4 or not r[3]:
            return fail(f"Results Funnel stage '{r[0]}' needs rows, dropped and a reason")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"Results Funnel does not add up at '{r[0]}'")
        prev = rows

    # Every compliance row names a law.
    comp = table_rows(section(text, "Compliance Check"))
    if len(comp) < 4:
        return fail("Compliance Check needs at least 4 rows")
    for r in comp:
        if len(r) < 4 or not LAW.search(r[2]):
            return fail(f"Compliance Check row '{r[0]}' does not name a law")

    # Sample rows: score fits band, phones E.164, only strong DNC-clear rows callable.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if len(r) < 8:
            return fail("Sample Rows need 8 columns")
        score, band = num(r[2]), r[3].strip().lower()
        rng = next((b for b in BANDS if b[0] == band), None)
        if score is None or rng is None or not (rng[1] <= score <= rng[2]):
            return fail(f"sample {r[0]}: score {r[2]} does not fit band '{r[3]}'")
        if r[5] and not E164.match(r[5].strip()):
            return fail(f"sample {r[0]}: phone '{r[5]}' is not E.164")
        status = r[7].strip()
        if status not in STATUSES:
            return fail(f"sample {r[0]}: status '{status}' not in the vocabulary")
        if status == "callable_manual" and (band not in ("confirmed", "probable") or r[6].strip().lower() != "clear"):
            return fail(f"sample {r[0]} is callable but is {band} or not DNC clear")

    print(f"PASS - {path.name}: FCRA boundary stated, cost lines at catalog prices, {total:.0f} rows banded, {len(comp)} compliance rows name a law")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
