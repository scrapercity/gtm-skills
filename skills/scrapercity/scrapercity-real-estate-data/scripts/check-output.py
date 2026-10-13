#!/usr/bin/env python3
"""Check a real estate data plan built from templates/output-template.md.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Objective",
    "Tool Plan",
    "Cost Estimate",
    "Compliance Check",
    "Outreach Routing",
    "Next Steps",
]
# Catalog prices (references/scrapercity-catalog.md). Property lookup allows 0.15 or 0.25 (with owner contact).
PRICES = {
    "scrape_zillow_agents": {0.029},
    "scrape_property_lookup": {0.15, 0.25, 0.10},
    "scrape_distress_list": {0.05},
    "scrape_crexi": {0.029},
    "scrape_bizbuysell": {0.0099},
    "find_people": {0.0199},
    "validate_emails": {0.0072},
    "find_emails": {0.05},
    "find_mobiles": {0.25},
}
LAWS = re.compile(
    r"TCPA|47 U\.?S\.?C|47 CFR|Telemarketing Sales Rule|\bTSR\b|CAN-SPAM|FCRA|Regulation O|12 CFR 1015|"
    r"Do Not Call|Civil Code|Act 52|SB 155|Senate Bill 155|License Act|501\.059|Wholesaler Prohibition",
    re.IGNORECASE,
)
DISTRESS_TYPES = {"preforeclosure", "foreclosure", "auction", "bankowned"}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 1800


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def table_rows(block):
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows[1:]


def money(s):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", s)
    return float(m.group(1).replace(",", "")) if m else None


def number(s):
    m = re.search(r"[\d,]+(?:\.\d+)?", s)
    return float(m.group(0).replace(",", "")) if m else None


def fail(msg):
    print("FAIL - " + msg)
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/plan.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/plan.md (file not found)")
        return 2
    text = path.read_text(encoding="utf-8")

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    for name in REQUIRED:
        if not re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M | re.I):
            return fail(f"missing heading '## {name}'")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")

    tools = table_rows(section(text, "Tool Plan"))
    if len(tools) < 2:
        return fail("Tool Plan needs at least 2 rows")
    for row in tools:
        params = " ".join(row)
        for v in re.findall(r"distressTypes\s*\[([^\]]*)\]", params):
            for t in re.findall(r"[A-Za-z]+", v):
                if t.lower() not in DISTRESS_TYPES:
                    return fail(f"distressTypes value '{t}' is not one of preForeclosure, foreclosure, auction, bankOwned")
        for lim in re.findall(r"(?:maxItems|searchLimit)\s*:?\s*(\d+)", params):
            if int(lim) > 500:
                return fail(f"maxItems or searchLimit {lim} is over the 500 limit")

    cost_rows = table_rows(section(text, "Cost Estimate"))
    if len(cost_rows) < 2:
        return fail("Cost Estimate needs line items and a total")
    total_line = None
    summed = 0.0
    for row in cost_rows:
        if len(row) < 4:
            return fail("each Cost Estimate row needs line, units, unit price and cost")
        if row[0].lower().startswith("total"):
            total_line = money(row[3])
            continue
        tool = next((t for t in PRICES if t in row[0]), None)
        units, price, cost = number(row[1]), money(row[2]), money(row[3])
        if None in (units, price, cost):
            return fail(f"cost row '{row[0]}' needs numeric units, $ unit price and $ cost")
        if tool and not any(abs(price - p) < 1e-9 for p in PRICES[tool]):
            return fail(f"{tool} unit price ${price} does not match the catalog")
        if abs(units * price - cost) > 0.02:
            return fail(f"cost row '{row[0]}': {units:g} x ${price} is not ${cost}")
        summed += cost
    if total_line is None:
        return fail("Cost Estimate needs a Total row with a $ figure")
    if abs(summed - total_line) > 0.02:
        return fail(f"line items sum to ${summed:.2f} but Total says ${total_line:.2f}")

    comp = table_rows(section(text, "Compliance Check"))
    if len(comp) < 2:
        return fail("Compliance Check needs a row per channel (at least 2)")
    for row in comp:
        law = row[2] if len(row) > 2 else ""
        if not LAWS.search(law):
            return fail(f"compliance row '{row[0]}' must name the law that governs it")
    sec = section(text, "Compliance Check")
    if not re.search(r"FCRA", sec):
        return fail("Compliance Check must state the FCRA boundary")
    if not re.search(r"state rule", sec, re.I):
        return fail("Compliance Check must state the state rule")

    if len(table_rows(section(text, "Outreach Routing"))) < 2:
        return fail("Outreach Routing needs at least 2 record groups")

    print(f"PASS - real estate plan: {len(tools)} tool steps, total ${total_line:.2f}, {len(comp)} compliance rows")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
