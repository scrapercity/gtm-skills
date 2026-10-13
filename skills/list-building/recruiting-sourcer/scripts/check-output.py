#!/usr/bin/env python3
"""Check a candidate shortlist report against the recruiting-sourcer output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Role Brief",
    "Search Strings",
    "Count Check",
    "Sourcing Funnel",
    "Contact Coverage",
    "Cost Estimate",
    "Compliance Check",
    "Shortlist Sample",
    "Outreach Plan",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 40
E164 = re.compile(r"^\+[1-9]\d{7,14}$")
LAW = re.compile(r"CAN-SPAM|CASL|GDPR|PECR|TCPA|47 (U\.S\.C|CFR)|EEOC|ADEA|Title VII|Local Law 144|FCRA|contract|non-solicit", re.I)
DOMAIN = re.compile(r"\b([a-z0-9-]+(?:\.[a-z0-9-]+)+)\b", re.I)


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

    # Excluded employers are named as domains.
    brief = {r[0].strip().lower(): r[1] for r in table_rows(section(text, "Role Brief")) if len(r) > 1}
    excl_row = next((v for k, v in brief.items() if k.startswith("excluded employer")), None)
    if not excl_row:
        return fail("Role Brief needs an 'Excluded employer domains' row")
    excluded = {d.lower() for d in DOMAIN.findall(excl_row)}
    dnp = next((v for k, v in brief.items() if k.startswith("do-not-poach")), "")
    excluded |= {d.lower() for d in DOMAIN.findall(dnp)}
    if not excluded:
        return fail("Excluded employer domains must list at least one domain")

    # Search strings include title and notTitle.
    params = {r[0].strip().lower() for r in table_rows(section(text, "Search Strings"))}
    for p in ("title", "nottitle"):
        if p not in params:
            return fail(f"Search Strings must include {p}")

    # Funnel adds up and names the employer exclusion.
    funnel = table_rows(section(text, "Sourcing Funnel"))
    if len(funnel) < 4:
        return fail("Sourcing Funnel needs at least 4 stages")
    prev = None
    for r in funnel:
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None or len(r) < 4 or not r[3]:
            return fail(f"Sourcing Funnel stage '{r[0]}' needs rows, dropped and a reason")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"Sourcing Funnel does not add up at '{r[0]}'")
        prev = rows
    if not any("hiring company" in r[0].lower() or "employer" in r[0].lower() for r in funnel):
        return fail("Sourcing Funnel must show the hiring-company exclusion as its own stage")

    # Contact coverage reconciles to the shortlist; mobiles only for the A tier.
    cov = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Contact Coverage")) if len(r) > 1}
    need = ["shortlisted candidates (a and b)", "valid email from the lead database", "valid email from email finder",
            "catch-all email, held", "no usable email", "a-tier candidates", "a-tier mobiles found"]
    for k in need:
        if cov.get(k) is None:
            return fail(f"Contact Coverage missing '{k}'")
    parts = cov[need[1]] + cov[need[2]] + cov[need[3]] + cov[need[4]]
    if abs(parts - cov[need[0]]) > 0.5:
        return fail("Contact Coverage email rows do not sum to the shortlist")
    if cov[need[6]] > cov[need[5]] or cov[need[5]] > cov[need[0]]:
        return fail("A-tier mobiles cannot exceed A-tier candidates, nor A tier the shortlist")

    # Apollo lines respect the 500 to 50,000 range and $0.0039 price.
    for r in table_rows(section(text, "Cost Estimate")):
        if "scrape_apollo" in r[0].lower():
            units, cost = num(r[1]), num(r[3].replace("$", "")) if len(r) > 3 else None
            if units is None or not (500 <= units <= 50000):
                return fail("scrape_apollo count must be 500 to 50,000")
            if cost is None or abs(units * 0.0039 - cost) > 0.01:
                return fail("scrape_apollo cost must equal count x $0.0039")
    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a Total row with a $ figure")

    # Every compliance row names a law or rule.
    comp = table_rows(section(text, "Compliance Check"))
    if len(comp) < 5:
        return fail("Compliance Check needs at least 5 rows")
    for r in comp:
        if len(r) < 4 or not LAW.search(r[2]):
            return fail(f"Compliance Check row '{r[0]}' does not name a law or rule")

    # Shortlist sample: no excluded employer, tier fits score, mobiles only on A tier.
    sample = table_rows(section(text, "Shortlist Sample"))
    if len(sample) < 3:
        return fail("Shortlist Sample needs at least 3 rows")
    for r in sample:
        if len(r) < 8:
            return fail("Shortlist Sample rows need 8 columns")
        dom = r[2].strip().lower()
        if dom in excluded:
            return fail(f"candidate {r[0]} works at excluded employer {dom}")
        tier, score = r[4].strip().upper(), num(r[5])
        if tier not in ("A", "B") or score is None:
            return fail(f"candidate {r[0]} needs tier A or B and a numeric rank score")
        if (tier == "A" and score < 80) or (tier == "B" and not 60 <= score < 80):
            return fail(f"candidate {r[0]}: score {score:.0f} does not fit tier {tier}")
        if r[6].strip().lower() not in ("valid", "catch_all", "none"):
            return fail(f"candidate {r[0]}: email_status '{r[6]}' not allowed on the shortlist")
        mob = r[7].strip()
        if E164.match(mob):
            if tier != "A":
                return fail(f"candidate {r[0]} has a mobile but is not A tier")
        elif mob.lower() not in ("none found", "not run"):
            return fail(f"candidate {r[0]}: mobile must be E.164, 'none found' or 'not run'")

    print(f"PASS - {path.name}: {len(excluded)} excluded domains absent from the sample, funnel and coverage reconcile, {len(comp)} compliance rows name a rule")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
