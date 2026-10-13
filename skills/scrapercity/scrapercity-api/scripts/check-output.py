#!/usr/bin/env python3
"""Check a ScraperCity API integration spec built from templates/output-template.md.

Usage: check-output.py path/to/spec.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Request Summary",
    "Endpoints",
    "Auth and Keys",
    "Run Handling",
    "Database Paging",
    "Error Handling",
    "Rate Budget",
    "Cost Estimate",
    "Test Plan",
    "Next Steps",
]
SLUGS = {
    "apollo", "maps", "email-validator", "email-finder", "mobile-finder", "skip-trace", "website-finder",
    "store-leads", "techstack", "yelp-scraper", "angi-angies-list-scraper", "zillow-agents",
    "property-lookup", "distress-list", "crexi-scraper", "bizbuysell-scraper", "airbnb-email",
    "criminal-records",
}
RUN_ID = r"\{runid\}"
ROUTES = [
    (r"/api/v1/wallet", {"GET"}),
    (r"/api/v1/runs", {"GET"}),
    (r"/api/v1/apollo-status", {"GET"}),
    (r"/api/v1/scrape/status/" + RUN_ID, {"GET"}),
    (r"/api/v1/scrape/logs/" + RUN_ID, {"GET"}),
    (r"/api/v1/scrape/cancel/" + RUN_ID, {"POST"}),
    (r"/api/downloads/" + RUN_ID, {"GET"}),
    (r"/api/v1/database/(?:leads|local-businesses)", {"GET", "POST"}),
    (r"/api/v1/database/ecommerce", {"GET"}),
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 2500
MAX_RPM = 100
MAX_CONCURRENT = 10


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


def kv(block):
    return {r[0].lower(): r[1] for r in table_rows(block) if len(r) >= 2}


def fail(msg):
    print("FAIL - " + msg)
    return 1


def check_route(method, path):
    path = path.strip("` ").split("?")[0].lower()
    m = re.fullmatch(r"/api/v1/scrape/([a-z-]+)", path)
    if m and m.group(1) not in {"status", "logs", "cancel"}:
        if m.group(1) not in SLUGS:
            return f"unknown scraper slug '{m.group(1)}' (see references/endpoint-reference.md)"
        if method != "POST":
            return f"scraper start {path} must be POST"
        return ""
    if path.startswith("/api/v1/downloads"):
        return "download path is /api/downloads/{runId}, without /v1"
    for pattern, methods in ROUTES:
        if re.fullmatch(pattern, path):
            if method not in methods:
                return f"{path} must be {' or '.join(sorted(methods))}, not {method}"
            return ""
    return f"unknown path '{path}'"


def minutes(value):
    m = re.search(r"(\d+(?:\.\d+)?)\s*(s|sec|min|m|h|hour)", value.lower())
    if not m:
        return None
    n, unit = float(m.group(1)), m.group(2)
    return n / 60 if unit.startswith("s") else n * 60 if unit.startswith("h") else n


def first_int(value):
    m = re.search(r"\d[\d,]*", value)
    return int(m.group(0).replace(",", "")) if m else None


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/spec.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/spec.md (file not found)")
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

    endpoints = table_rows(section(text, "Endpoints"))
    if len(endpoints) < 3:
        return fail("Endpoints needs at least 3 rows")
    for row in endpoints:
        if len(row) < 3:
            return fail("each Endpoints row needs step, method and path")
        err = check_route(row[1].strip("` ").upper(), row[2])
        if err:
            return fail(f"Endpoints row '{row[0]}': {err}")

    auth = section(text, "Auth and Keys")
    if not re.search(r"Bearer", auth):
        return fail("Auth and Keys must name the Authorization: Bearer header")
    if re.search(r"Bearer\s+[A-Za-z0-9_\-]{20,}", text):
        return fail("a literal API key appears in the spec; reference the variable or secret store instead")

    runs = table_rows(section(text, "Run Handling"))
    if not runs:
        return fail("Run Handling needs at least one row")
    for row in runs:
        if "apollo" in row[0].lower():
            signal = " ".join(row[1:3]).lower()
            interval = minutes(row[2]) if len(row) > 2 else None
            if "webhook" not in signal and (interval is None or interval < 60):
                return fail("scrape_apollo needs a webhook or polling no more often than every 60 min")

    paging = kv(section(text, "Database Paging"))
    lim = first_int(paging.get("limit", ""))
    if lim is not None and lim > 100:
        return fail(f"database limit {lim} is over the 100 per call maximum")
    excl = paging.get("excludedelivered", "").lower()
    pg = first_int(paging.get("page", ""))
    if excl.startswith("true") and pg and pg > 1:
        return fail("excludeDelivered true with page above 1 skips records; use page 1 or the after cursor")
    daily = first_int(paging.get("new records per day", ""))
    if daily is not None and daily > 100000:
        return fail(f"{daily} new records a day exceeds the 100,000 daily allowance")

    errors = table_rows(section(text, "Error Handling"))
    codes = {r[0].split()[0]: r for r in errors if r and r[0]}
    if "409" not in codes:
        return fail("Error Handling must cover 409 (duplicate request)")
    if not re.search(r"\b(no|reuse)\b", " ".join(codes["409"][1:]).lower()):
        return fail("409 must be handled by reusing the earlier run, never by resubmitting")
    if "401" in codes and re.search(r"\byes\b", codes["401"][-1].lower()):
        return fail("401 must not be retried")

    budget = kv(section(text, "Rate Budget"))
    rpm = first_int(budget.get("peak requests per minute", ""))
    if rpm is None:
        return fail("Rate Budget must state peak requests per minute")
    if rpm > MAX_RPM:
        return fail(f"peak {rpm} requests a minute exceeds the 100 a minute per key limit")
    conc = first_int(budget.get("concurrent scrapes", ""))
    if conc is not None and conc > MAX_CONCURRENT:
        return fail(f"{conc} concurrent scrapes exceeds the limit of 10")

    cost = section(text, "Cost Estimate")
    if len(table_rows(cost)) < 2 or not re.search(r"\$\d", cost) or not re.search(r"total", cost, re.I):
        return fail("Cost Estimate needs a table with $ figures and a total line")

    if len(table_rows(section(text, "Test Plan"))) < 2:
        return fail("Test Plan needs at least 2 checks")

    print(f"PASS - API spec: {len(endpoints)} endpoints, {len(errors)} error rows, peak {rpm} req/min")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
