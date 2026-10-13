#!/usr/bin/env python3
"""Check a ScraperCity routing plan built from templates/output-template.md.

Usage: check-output.py path/to/routing-plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.

Checks:
  - every required section, no placeholders, minimum length
  - every skill in the chain exists in this repo
  - every paid tool row: unit price matches the catalog, units x price = cost
  - the cost rows sum to the stated total
  - all five gates are present and have a status
  - compliance gate names CAN-SPAM for email, DNC for phone, FCRA for public-records tools
"""
import re
import sys
from pathlib import Path

REQUIRED = ["Request", "Skill Chain", "Tool Calls and Cost", "Gates", "Handoffs", "Open Questions"]
SKILLS = {
    "using-scrapercity-skills", "scrapercity-mcp", "scrapercity-cli", "scrapercity-api",
    "scrapercity-integrations", "scrapercity-lead-database", "scrapercity-local-business-database",
    "scrapercity-real-estate-data", "icp-list-builder", "tam-builder", "decision-maker-finder",
    "account-researcher", "local-business-list", "cold-email-list", "email-list-cleaner",
    "crm-enricher", "mobile-appender", "ecommerce-by-techstack", "skip-tracer", "recruiting-sourcer",
    "cold-email-strategy", "cold-email-copywriting", "reply-handling", "multi-channel-outreach",
    "domain-infrastructure", "inbox-setup", "email-deliverability", "sending-platforms",
    "cold-calling", "signal-triggered-outbound", "outbound-unit-economics",
}
# Per-result prices from references/scrapercity-catalog.md (scrapercity 1.0.17). 0 = included with Growth and up.
PRICES = {
    "query_lead_database": 0.0, "query_local_business_database": 0.0,
    "scrape_apollo": 0.0039, "scrape_website_finder": 0.0499, "find_people": 0.0199,
    "scrape_distress_list": 0.05, "validate_emails": 0.0072, "scrape_maps": 0.0099,
    "scrape_airbnb": 0.019, "scrape_bizbuysell": 0.0099, "scrape_crexi": 0.029,
    "scrape_angi": 0.0099, "scrape_yelp": 0.0099, "scrape_zillow_agents": 0.029,
    "scrape_property_lookup": 0.15, "search_criminal_records": 1.00, "scrape_store_leads": 0.0039,
    "scrape_builtwith": 4.99, "find_emails": 0.05, "find_mobiles": 0.25,
}
PUBLIC_RECORDS = {"find_people", "scrape_property_lookup", "search_criminal_records", "scrape_distress_list"}
GATES = ["wallet", "count", "compliance", "quality", "deliverability"]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 1500


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else None


def rows(block):
    out = []
    for line in (block or "").splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        out.append([c.strip() for c in line.strip("|").split("|")])
    return out[1:]


def money(cell):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def number(cell):
    m = re.search(r"([\d,]+(?:\.\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def fail(msg):
    print("FAIL - " + msg)
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/routing-plan.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"FAIL - file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")

    if PLACEHOLDER.search(text):
        return fail("unresolved placeholders remain")
    if len(text.strip()) < MIN_CHARS:
        return fail(f"plan is under {MIN_CHARS} characters")
    for name in REQUIRED:
        if section(text, name) is None:
            return fail(f"missing section '## {name}'")

    request = {r[0].lower(): r[1] for r in rows(section(text, "Request")) if len(r) >= 2}
    channels = request.get("channels", "").lower()

    chain = rows(section(text, "Skill Chain"))
    if len(chain) < 2:
        return fail("skill chain needs at least 2 steps")
    for r in chain:
        names = re.findall(r"`([a-z0-9-]+)`", r[1] if len(r) > 1 else "")
        if not names:
            return fail(f"chain step '{r[0]}' does not name a skill in backticks")
        for n in names:
            if n not in SKILLS:
                return fail(f"unknown skill '{n}' in the chain")

    cost_rows = rows(section(text, "Tool Calls and Cost"))
    total_stated, summed, tools_used = None, 0.0, set()
    for r in cost_rows:
        if len(r) < 5:
            continue
        if "total" in r[1].lower():
            total_stated = money(r[4])
            continue
        tool = re.findall(r"`([a-z_]+)`", r[1])
        if not tool:
            return fail(f"cost row without a tool id: {r[1]}")
        tool = tool[0]
        if tool not in PRICES:
            return fail(f"unknown tool '{tool}'")
        units, price, cost = number(r[2]), money(r[3]), money(r[4])
        if units is None or price is None or cost is None:
            return fail(f"row for {tool} needs units, a $ unit price and a $ cost")
        if abs(price - PRICES[tool]) > 1e-9:
            return fail(f"{tool} unit price ${price} does not match catalog ${PRICES[tool]}")
        if abs(units * price - cost) > 0.01:
            return fail(f"{tool}: {units:g} x ${price} = ${units * price:.2f}, row says ${cost:.2f}")
        if units > 0:
            tools_used.add(tool)
        summed += cost
    if total_stated is None:
        return fail("no Total row in Tool Calls and Cost")
    if abs(total_stated - summed) > 0.01:
        return fail(f"rows sum to ${summed:.2f}, total says ${total_stated:.2f}")

    gates = {r[0].lower(): r for r in rows(section(text, "Gates")) if r}
    for g in GATES:
        if g not in gates:
            return fail(f"missing gate '{g}'")
        if len(gates[g]) < 3 or not gates[g][2]:
            return fail(f"gate '{g}' has no status")
    compliance = " ".join(gates["compliance"]).lower()
    if "email" in channels and "can-spam" not in compliance:
        return fail("email channel without a CAN-SPAM rule in the compliance gate")
    if any(w in channels for w in ("phone", "call", "sms", "text")) and "dnc" not in compliance:
        return fail("phone channel without a DNC rule in the compliance gate")
    if tools_used & PUBLIC_RECORDS and "fcra" not in compliance:
        return fail("public-records tool used without an FCRA line in the compliance gate")

    if len(rows(section(text, "Handoffs"))) < len(chain) - 1:
        return fail("every step after the first needs a handoff row")

    print(f"PASS - {len(chain)} skills chained, ${summed:.2f} priced from the catalog, all 5 gates set")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
