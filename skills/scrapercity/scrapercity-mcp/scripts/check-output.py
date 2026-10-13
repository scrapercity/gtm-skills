#!/usr/bin/env python3
"""Check a ScraperCity MCP setup and run report built from templates/output-template.md.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Client Setup",
    "Verification",
    "Wallet Check",
    "Run Plan",
    "Run Log",
    "Issues and Fixes",
    "Next Steps",
]
TOOLS = {
    "check_wallet", "list_runs", "check_run_status", "download_results", "cancel_run",
    "query_lead_database", "query_local_business_database",
    "scrape_apollo", "scrape_website_finder", "find_people", "scrape_distress_list",
    "validate_emails", "scrape_maps", "scrape_airbnb", "scrape_bizbuysell", "scrape_crexi",
    "scrape_angi", "scrape_yelp", "scrape_zillow_agents", "scrape_property_lookup",
    "search_criminal_records", "scrape_store_leads", "scrape_builtwith", "find_emails",
    "find_mobiles",
}
STATUSES = {"RUNNING", "SUCCEEDED", "FAILED", "CANCELLED"}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
# A key value is fine when it is masked, a variable reference, or the documented placeholder.
SAFE_KEY = re.compile(r"^(\*+\w{0,6}|\.{3}|\$\{?[A-Za-z_:]+\}?|\$\{input:[\w-]+\}|YOUR_SCRAPERCITY_API_KEY)$")
KEY_VALUE = re.compile(r"SCRAPERCITY_API_KEY[\"']?\s*[:=]\s*[\"']?([^\s\"'`,}]+)")
MIN_CHARS = 1800
APPROVAL_LINE = 5.00


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


def money(cell):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def number(cell):
    m = re.search(r"\d[\d,]*(?:\.\d+)?", cell)
    return float(m.group(0).replace(",", "")) if m else None


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
    text = path.read_text(encoding="utf-8")

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    for name in REQUIRED:
        if not re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M | re.I):
            return fail(f"missing heading '## {name}'")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")

    # 1. The config runs the right package and binary.
    setup = kv(section(text, "Client Setup"))
    args = setup.get("args", "")
    for part in ("-y", "--package", "scrapercity", "scrapercity-mcp"):
        if part not in args:
            return fail(f"Client Setup Args must include '{part}' (npx -y --package scrapercity scrapercity-mcp)")
    if not setup.get("key handling"):
        return fail("Client Setup needs a Key handling row")

    # 2. No unmasked API key anywhere in the report.
    for m in KEY_VALUE.finditer(text):
        if not SAFE_KEY.match(m.group(1)):
            return fail(f"API key value '{m.group(1)[:6]}...' is not masked or a variable reference")

    # 3. Verification proves the server and the key.
    ver = kv(section(text, "Verification"))
    if "25" not in ver.get("tools listed", ""):
        return fail("Verification must report the 25 tools the server lists")
    wallet_call = ver.get("check_wallet call", "").lower()
    if "succeed" not in wallet_call and "plan" not in wallet_call:
        return fail("Verification must show a successful check_wallet call")

    wallet = kv(section(text, "Wallet Check"))
    balance = money(wallet.get("balance", ""))
    if balance is None:
        return fail("Wallet Check must show the balance as a $ figure")

    # 4. Run plan: known tools, arithmetic that adds up, webhook for Apollo, approval over $5.
    plan_block = section(text, "Run Plan")
    rows = table_rows(plan_block)
    steps = [r for r in rows if r and r[0].lower() != "total"]
    total_rows = [r for r in rows if r and r[0].lower() == "total"]
    if not steps:
        return fail("Run Plan needs at least one tool row")
    if not total_rows or money(total_rows[0][-1]) is None:
        return fail("Run Plan needs a Total row with a $ figure")
    total = money(total_rows[0][-1])
    running = 0.0
    for r in steps:
        if len(r) < 6:
            return fail(f"Run Plan row '{r[0]}' needs 6 columns")
        tool = r[1].strip("` ")
        if tool not in TOOLS:
            return fail(f"Run Plan tool '{r[1]}' is not a ScraperCity MCP tool")
        if tool == "scrape_apollo" and "webhook" not in " ".join(r).lower():
            return fail("a scrape_apollo row must name its webhook")
        units, price, cost = number(r[3]), money(r[4]), money(r[5])
        if cost is None:
            return fail(f"Run Plan row '{r[0]}' needs a $ cost")
        if units is not None and price is not None and abs(units * price - cost) > 0.011:
            return fail(f"Run Plan row '{r[0]}': {units:g} x ${price} is not ${cost}")
        running += cost
    if abs(running - total) > 0.011:
        return fail(f"Run Plan rows add to ${running:.2f}, Total says ${total:.2f}")
    if total > balance:
        return fail(f"Run Plan total ${total:.2f} exceeds the ${balance:.2f} balance; do not start")
    if total > APPROVAL_LINE:
        approval = re.search(r"^Approval:(.*)$", plan_block, re.M | re.I)
        if not approval or not re.search(r"approved|yes|go ahead", approval.group(1), re.I):
            return fail(f"Run Plan total ${total:.2f} is over $5 and has no recorded approval")

    # 5. Run log: every run has an id, a known status, and SUCCEEDED rows an absolute file path.
    log = table_rows(section(text, "Run Log"))
    if not log:
        return fail("Run Log needs at least one run row")
    for r in log:
        if len(r) < 5 or len(r[0]) < 8:
            return fail(f"Run Log row '{r[0]}' needs a full runId and 5 columns")
        status = r[2].upper().strip("` ")
        if status not in STATUSES:
            return fail(f"Run Log status '{r[2]}' must be one of {', '.join(sorted(STATUSES))}")
        if status == "SUCCEEDED" and not re.match(r"^`?(/|~/|[A-Za-z]:\\)", r[4]):
            return fail(f"Run Log row '{r[0][:8]}' SUCCEEDED but its file path is not absolute")

    if not table_rows(section(text, "Issues and Fixes")):
        return fail("Issues and Fixes needs a table row (write 'None' rows if nothing broke)")

    print(f"PASS - MCP report: {len(steps)} planned calls, total ${total:.2f}, {len(log)} runs logged")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
