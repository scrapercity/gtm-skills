#!/usr/bin/env python3
"""Check a TAM report against the tam-builder output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Market Definition",
    "Source Counts",
    "Pull and Dedupe Funnel",
    "Source Mix",
    "Coverage Estimate",
    "TAM SAM SOM",
    "Metro Breakdown",
    "Cost Estimate",
    "Output Schema",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 35
SOURCES = {"lead_db", "local_db", "ecom_db", "apollo", "maps", "yelp", "angi", "store_leads",
           "techstack", "website_finder", "email_finder", "mobile_finder", "people_finder", "user_upload"}


def num(text):
    m = re.search(r"-?\d[\d,]*\.?\d*", (text or "").replace("$", ""))
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
        s = s.replace("\\|", "\x00")
        rows.append([c.strip().replace("\x00", "|") for c in s.strip("|").split("|")])
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
        return fail(f"only {total_rows} table rows, need {MIN_TABLE_ROWS}")

    # Funnel adds up.
    funnel = table_rows(section(text, "Pull and Dedupe Funnel"))
    if len(funnel) < 4:
        return fail("funnel needs at least 4 stages")
    prev = None
    for r in funnel:
        if len(r) < 4 or not r[3]:
            return fail(f"funnel stage '{r[0]}' needs rows, dropped and a reason")
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None:
            return fail(f"funnel stage '{r[0]}' is not numeric")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"funnel does not add up at '{r[0]}'")
        prev = rows
    final_accounts = prev

    # Source mix uses the controlled vocabulary and sums to final accounts.
    mix = table_rows(section(text, "Source Mix"))
    mix_sum = 0.0
    for r in mix:
        if r[0].lower().startswith("total"):
            continue
        for part in r[0].strip("`").split("|"):
            if part.strip() not in SOURCES:
                return fail(f"source value '{part.strip()}' is not in the controlled vocabulary")
        mix_sum += num(r[1]) or 0
    if abs(mix_sum - final_accounts) > 0.5:
        return fail(f"Source Mix sums to {mix_sum:.0f}, final accounts are {final_accounts:.0f}")

    # Coverage estimate: observed, estimate and a percentage.
    cov = {r[0].lower(): r[1] for r in table_rows(section(text, "Coverage Estimate")) if len(r) > 1}
    for key in ("observed", "chapman estimate", "coverage"):
        if key not in cov or num(cov[key]) is None:
            return fail(f"Coverage Estimate needs a numeric '{key}' row")
    if "%" not in cov["coverage"]:
        return fail("Coverage row must be a percentage")
    if not re.search(r"caveat", section(text, "Coverage Estimate"), re.I):
        return fail("Coverage Estimate needs a caveat line")

    # TAM SAM SOM: accounts x ACV = dollars, and SOM <= SAM <= TAM.
    layers = {}
    for r in table_rows(section(text, "TAM SAM SOM")):
        if len(r) < 5:
            return fail("TAM SAM SOM rows need Layer, Definition, Accounts, ACV, Dollars")
        acc, acv, dol = num(r[2]), num(r[3]), num(r[4])
        if None in (acc, acv, dol) or "$" not in r[4]:
            return fail(f"TAM SAM SOM row '{r[0]}' needs numeric accounts, ACV and a $ dollars value")
        if abs(acc * acv - dol) > max(1.0, dol * 0.005):
            return fail(f"{r[0]}: {acc:.0f} x {acv:.0f} does not equal {dol:.0f}")
        layers[r[0].strip().upper()] = acc
    if not {"TAM", "SAM", "SOM"} <= set(layers):
        return fail("TAM SAM SOM needs TAM, SAM and SOM rows")
    if not layers["SOM"] <= layers["SAM"] <= layers["TAM"]:
        return fail("expected SOM <= SAM <= TAM in accounts")

    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: funnel adds up to {final_accounts:.0f} accounts, source mix matches, TAM/SAM/SOM consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
