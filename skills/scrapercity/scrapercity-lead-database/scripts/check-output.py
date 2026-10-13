#!/usr/bin/env python3
"""Check a Lead Database pull plan built from templates/output-template.md.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Request Summary",
    "Filter Spec",
    "Count Check",
    "Pull Plan",
    "Cost and Allowance",
    "Sample QA",
    "Next Steps",
]
PARAMS = {
    "url", "title", "industry", "country", "state", "city", "companyname", "companydomain",
    "seniority", "department", "minemployees", "maxemployees", "keywords", "revenuemin",
    "revenuemax", "companycountry", "companystate", "companycity", "nottitle", "notkeywords",
    "notindustry", "socialurl", "hasemail", "hasphone", "page", "limit", "excludedelivered", "after",
}
GEO = {"country", "state", "city", "companycountry", "companystate", "companycity"}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 1800
DAILY_CAP = 100000


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def table_rows(block):
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows[1:]  # drop header


def kv(block):
    return {r[0].lower(): r[1] for r in table_rows(block) if len(r) >= 2}


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

    filters = table_rows(section(text, "Filter Spec"))
    if len(filters) < 3:
        return fail("Filter Spec needs at least 3 filter rows")
    for row in filters:
        param = row[0].strip("` ").lower()
        if param not in PARAMS:
            return fail(f"Filter Spec uses '{row[0]}', which is not a query_lead_database parameter")
        if param in GEO and len(row) >= 3:
            why = row[2].lower()
            if "person" not in why and "company" not in why and "hq" not in why:
                return fail(f"geography filter '{row[0]}' must say whether it is person or company location")

    count = kv(section(text, "Count Check"))
    total = count.get("pagination.total", "")
    if not re.search(r"\d", total):
        return fail("Count Check must show pagination.total from a limit 1 call")

    plan = kv(section(text, "Pull Plan"))
    excl = plan.get("excludedelivered", "").lower()
    page = plan.get("page", "")
    page_num = re.match(r"\s*(\d+)", page)
    if excl.startswith("true") and page_num and int(page_num.group(1)) > 1:
        return fail("excludeDelivered true with page above 1 skips records; use page 1 or after")
    daily = plan.get("daily new leads", "")
    nums = [int(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", daily)]
    if not nums:
        return fail("Pull Plan must state daily new leads as a number")
    if max(nums) > DAILY_CAP:
        return fail(f"daily new leads {max(nums)} exceeds the 100,000 a day allowance")

    cost = section(text, "Cost and Allowance")
    if len(table_rows(cost)) < 2 or not re.search(r"\$\d", cost):
        return fail("Cost and Allowance needs a table with $ figures")
    if not re.search(r"total", cost, re.I):
        return fail("Cost and Allowance needs a total line")

    qa = section(text, "Sample QA")
    m = re.search(r"(\d+)\s*/\s*20", qa)
    if not m:
        return fail("Sample QA must report on-target rows as N / 20")
    if int(m.group(1)) < 18:
        return fail(f"Sample QA shows {m.group(1)} / 20 on target; fix filters before pulling (need 18+)")

    print(f"PASS - lead pull plan: {len(filters)} filters, total {total}, QA {m.group(1)}/20")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
