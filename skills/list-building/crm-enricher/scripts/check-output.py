#!/usr/bin/env python3
"""Check a CRM enrichment report against the crm-enricher output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Input Profile",
    "Field Rules",
    "Routing Plan",
    "Cost Estimate",
    "Fill Results",
    "Match Confidence",
    "Write-back Mapping",
    "Audit Columns",
    "Unfilled Flags",
    "Sample Rows",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 40
POLICIES = {"fill_blank_only", "replace_if_invalid", "stage_for_review", "never_overwrite", "append_new"}
TIERS = ["high", "medium", "low", "none"]
AUDIT_REQUIRED = ["enriched_at", "enrich_source", "enrich_confidence", "enrich_status", "enrich_flags"]


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

    # Every field rule uses a policy from the controlled vocabulary.
    rules = table_rows(section(text, "Field Rules"))
    if len(rules) < 4:
        return fail("Field Rules needs at least 4 fields")
    for r in rules:
        if len(r) < 3 or r[2].strip().lower() not in POLICIES:
            return fail(f"Field Rules row '{r[0]}' has policy '{r[2] if len(r) > 2 else ''}', not one of {sorted(POLICIES)}")
    if not any(r[2].strip().lower() == "never_overwrite" for r in rules):
        return fail("Field Rules must name at least one never_overwrite field (owner, stage, consent)")

    # Fill results: filled + staged + unfilled == missing before.
    fills = table_rows(section(text, "Fill Results"))
    if len(fills) < 3:
        return fail("Fill Results needs at least 3 fields")
    for r in fills:
        if len(r) < 6:
            return fail("Fill Results rows need Field, Missing before, Filled, Staged, Unfilled, Filled by")
        vals = [num(c) for c in r[1:5]]
        if any(v is None for v in vals):
            return fail(f"Fill Results row '{r[0]}' has a non-numeric count")
        missing_n, filled, staged, unfilled = vals
        if abs(filled + staged + unfilled - missing_n) > 0.5:
            return fail(f"Fill Results row '{r[0]}': {filled:.0f} + {staged:.0f} + {unfilled:.0f} != {missing_n:.0f}")
        if not r[5]:
            return fail(f"Fill Results row '{r[0]}' does not say which source filled it")

    # Match tiers sum to total attempted.
    tiers = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Match Confidence")) if len(r) > 1}
    for t in TIERS:
        if tiers.get(t) is None:
            return fail(f"Match Confidence missing tier '{t}'")
    total = next((v for k, v in tiers.items() if k.startswith("total")), None)
    if total is None:
        return fail("Match Confidence needs a Total attempted row")
    if abs(sum(tiers[t] for t in TIERS) - total) > 0.5:
        return fail("Match Confidence tiers do not sum to Total attempted")

    # Audit columns present.
    audit = section(text, "Audit Columns").lower()
    absent = [c for c in AUDIT_REQUIRED if c not in audit]
    if absent:
        return fail("Audit Columns missing: " + ", ".join(absent))
    if "prior_" not in audit:
        return fail("Audit Columns needs a prior_<field> column for replaced values")

    # Write-back mapping rows all state an import setting.
    for r in table_rows(section(text, "Write-back Mapping")):
        if len(r) < 3 or not r[2]:
            return fail(f"Write-back Mapping row '{r[0]}' has no import setting")

    # Sample rows: low or none confidence never shows status filled.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if len(r) < 7:
            return fail("Sample Rows need 7 columns ending in Confidence and Status")
        conf, status = r[5].strip().lower(), r[6].strip().lower()
        if conf not in TIERS:
            return fail(f"Sample row {r[0]} has confidence '{r[5]}'")
        if conf in ("low", "none") and status == "filled":
            return fail(f"Sample row {r[0]} wrote a {conf}-confidence value")

    cost = section(text, "Cost Estimate")
    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a Total row with a $ figure")

    print(f"PASS - {path.name}: {len(rules)} field rules, {len(fills)} fill rows balance, {total:.0f} matches tiered, audit columns present")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
