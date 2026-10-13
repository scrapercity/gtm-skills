#!/usr/bin/env python3
"""Check a store list report against the ecommerce-by-techstack output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Target Definition",
    "Filters Used",
    "Value Probe",
    "Tier Bands",
    "Tech Stack Search",
    "Pull Funnel",
    "Validation Results",
    "Cost Estimate",
    "Sample Rows",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 35
# scrape_store_leads parameters and aliases from references/scrapercity-catalog.md
PARAMS = {
    "platform", "totalleads", "resumefromlead", "countrycode", "emails", "phones", "category", "city",
    "technologies", "apps", "instagram", "facebook", "tiktok", "youtube", "linkedin", "twitter", "pinterest",
    "planexclude", "offset", "minestimatedmonthlyvisits", "maxestimatedmonthlyvisits",
    "minestimatedmonthlysales", "maxestimatedmonthlysales", "minemployeecount", "maxemployeecount",
    "state", "filename", "visitsmin", "visitsmax", "salesmin", "salesmax", "employeesmin", "employeesmax",
}
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
    total_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if total_rows < MIN_TABLE_ROWS:
        return fail(f"only {total_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Every filter is a real scrape_store_leads parameter; emails is true; apps only on Shopify.
    filters = {}
    for r in table_rows(section(text, "Filters Used")):
        key = r[0].strip().strip("`")
        if key.lower() not in PARAMS:
            return fail(f"Filters Used names '{key}', which is not a scrape_store_leads parameter")
        filters[key.lower()] = r[1].strip().lower() if len(r) > 1 else ""
    if filters.get("emails") != "true":
        return fail("Filters Used must set emails to true for an email list")
    if "apps" in filters and "shopify" not in filters.get("platform", ""):
        return fail("apps is Shopify only; set platform to shopify or use technologies")

    # Tier bands: non-overlapping, and counts tie to the funnel.
    tiers = table_rows(section(text, "Tier Bands"))
    if not tiers:
        return fail("Tier Bands needs at least one tier")
    bands, pulled_sum, ready_sum, names = [], 0, 0, set()
    for r in tiers:
        if len(r) < 6:
            return fail("Tier Bands rows need Tier, min, max, Pulled, Send-ready, Sequence")
        lo = num(r[1])
        hi = num(r[2]) if num(r[2]) is not None else float("inf")
        if lo is None or lo > hi:
            return fail(f"tier {r[0]} has an invalid band")
        bands.append((lo, hi, r[0]))
        pulled_sum += num(r[3]) or 0
        ready_sum += num(r[4]) or 0
        names.add(r[0].strip().lower())
        if not r[5]:
            return fail(f"tier {r[0]} has no sequence")
    bands.sort()
    for (lo1, hi1, n1), (lo2, hi2, n2) in zip(bands, bands[1:]):
        if lo2 <= hi1:
            return fail(f"tier bands {n1} and {n2} overlap")

    funnel = table_rows(section(text, "Pull Funnel"))
    if len(funnel) < 4:
        return fail("Pull Funnel needs at least 4 stages")
    prev = None
    for r in funnel:
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None or len(r) < 4 or not r[3]:
            return fail(f"Pull Funnel stage '{r[0]}' needs rows, dropped and a reason")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"Pull Funnel does not add up at '{r[0]}'")
        prev = rows
    if abs(num(funnel[0][1]) - pulled_sum) > 0.5:
        return fail("tier Pulled counts do not sum to the first funnel stage")
    if abs(num(funnel[-1][1]) - ready_sum) > 0.5:
        return fail("tier Send-ready counts do not sum to the last funnel stage")

    # Tech Stack Search is priced at $4.99 per technology.
    for r in table_rows(section(text, "Tech Stack Search")):
        if r[0].strip().lower() in ("none", "not used"):
            continue
        if len(r) < 2 or "4.99" not in r[1]:
            return fail(f"Tech Stack Search row '{r[0]}' must show the $4.99 per technology price")

    # Validation buckets sum to total.
    vals = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Validation Results")) if len(r) > 1}
    for b in BUCKETS:
        if vals.get(b) is None:
            return fail(f"Validation Results missing bucket '{b}'")
    total = next((v for k, v in vals.items() if k.startswith("total")), None)
    if total is None or abs(sum(vals[b] for b in BUCKETS) - total) > 0.5:
        return fail("validation buckets do not sum to Total validated")

    # Sample rows: valid email, known tier.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if len(r) < 7:
            return fail("Sample Rows need Domain through email_status columns")
        if r[4].strip().lower() not in names:
            return fail(f"sample {r[0]} has tier '{r[4]}' not in Tier Bands")
        if r[6].strip().lower() != "valid":
            return fail(f"sample {r[0]} email_status must be valid")

    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a Total row with a $ figure")

    print(f"PASS - {path.name}: {len(filters)} valid store-leads filters, {len(tiers)} non-overlapping tiers tie to the funnel, buckets sum to {total:.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
