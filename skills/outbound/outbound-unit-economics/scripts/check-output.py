#!/usr/bin/env python3
"""Check an outbound unit economics model produced with the outbound-unit-economics skill.

Usage: check-output.py path/to/model.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import re
import sys

REQUIRED = [
    "Inputs",
    "ScraperCity Cost",
    "Capacity",
    "Funnel",
    "Unit Costs",
    "Break-even",
    "Sensitivity",
    "Recommendation",
]
# Catalog prices from references/scrapercity-catalog.md (npm scrapercity 1.0.17).
PRICES = {
    "scrape_apollo": 0.0039,
    "scrape_website_finder": 0.0499,
    "find_people": 0.0199,
    "scrape_distress_list": 0.05,
    "validate_emails": 0.0072,
    "scrape_maps": 0.0099,
    "scrape_airbnb": 0.019,
    "scrape_bizbuysell": 0.0099,
    "scrape_crexi": 0.029,
    "scrape_angi": 0.0099,
    "scrape_yelp": 0.0099,
    "scrape_zillow_agents": 0.029,
    "scrape_property_lookup": 0.15,
    "search_criminal_records": 1.00,
    "scrape_store_leads": 0.0039,
    "scrape_builtwith": 4.99,
    "find_emails": 0.05,
    "find_mobiles": 0.25,
}
PLANS = {"starter": (49, 49), "growth": (149, 159), "scale": (649, 800)}
INPUT_TYPES = ("user input", "catalog", "benchmark", "assumption", "measured")
MIN_WORDS = 600
MIN_TABLE_ROWS = 30
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
MONEY = re.compile(r"\$\s?(-?[\d,]+(?:\.\d+)?)")


def fail(msg):
    print(f"FAIL - {msg}")
    sys.exit(1)


def sections(text):
    out, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip().lower()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def tables(block):
    found = []
    lines = [l.strip() for l in block.splitlines()]
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", lines[i + 1]):
            head = [h.strip().lower() for h in line.strip("|").split("|")]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(dict(zip(head, [c.strip() for c in lines[j].strip("|").split("|")])))
                j += 1
            found.append((head, rows))
    return found


def rows_of(block):
    return [r for _, rows in tables(block) for r in rows]


def money(s):
    vals = [float(v.replace(",", "")) for v in MONEY.findall(s)]
    return vals[-1] if vals else None


def number(s):
    m = re.search(r"-?[\d,]+(?:\.\d+)?", s)
    return float(m.group(0).replace(",", "")) if m else None


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/model.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the model: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    if len(text.split()) < MIN_WORDS:
        fail(f"model has {len(text.split())} words, minimum is {MIN_WORDS}")
    all_rows = rows_of(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"model has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    # Skill check 1: every input is typed, and benchmarks carry a year.
    inputs = rows_of(secs["inputs"])
    if len(inputs) < 10:
        fail(f"Inputs has {len(inputs)} rows, minimum is 10")
    for r in inputs:
        t = r.get("type", "").lower()
        if not any(t.startswith(x) for x in INPUT_TYPES):
            fail(f"input '{r.get('input')}' needs a type: {', '.join(INPUT_TYPES)}")
        if t.startswith("benchmark") and not re.search(r"20\d\d", r.get("source", "")):
            fail(f"benchmark input '{r.get('input')}' needs a dated source")

    # Skill check 2: catalog prices and line arithmetic; plan fee and credits.
    cost_rows = rows_of(secs["scrapercity cost"])
    plan_ok = False
    for r in cost_rows:
        line = " | ".join(r.values()).lower()
        for plan, (fee, credits) in PLANS.items():
            if f"{plan} plan" in line or (plan in line and "plan" in r.get("line", "").lower()):
                if f"${fee}" not in line or f"${credits}" not in line:
                    fail(f"{plan.title()} plan row must show the ${fee} fee and ${credits} credits")
                plan_ok = True
        tool = r.get("tool", "")
        for tid, price in PRICES.items():
            if re.search(rf"`{tid}`", tool) and "miss" not in tool.lower():
                unit = money(r.get("unit price", ""))
                if unit is None or abs(unit - price) > 1e-9:
                    fail(f"{tid} must be priced at ${price} per result, found '{r.get('unit price')}'")
                count, cost = number(r.get("count", "")), money(r.get("cost", ""))
                if count is None or cost is None:
                    fail(f"{tid} row needs a count and a dollar cost")
                if abs(count * price - cost) > 0.01:
                    fail(f"{tid} row: {count:g} x ${price} = ${count * price:.2f}, not ${cost:.2f}")
    if not plan_ok:
        fail("ScraperCity Cost needs a plan row naming Starter, Growth or Scale with its fee and credits")

    # Skill check 3: cost per meeting and per deal match total / count.
    funnel = {r.get("stage", "").lower(): r for r in rows_of(secs["funnel"])}
    unit = {r.get("metric", "").lower(): r for r in rows_of(secs["unit costs"])}
    total_row = next((v for k, v in unit.items() if k.startswith("total monthly")), None)
    if not total_row:
        fail("Unit Costs needs a 'Total monthly program cost' row")
    total = money(total_row.get("value", ""))
    for stage, metric in (("meetings booked", "cost per meeting booked"), ("deals", "cost per deal")):
        f = next((v for k, v in funnel.items() if k.startswith(stage)), None)
        u = next((v for k, v in unit.items() if k.startswith(metric)), None)
        if not f or not u:
            fail(f"need Funnel '{stage}' and Unit Costs '{metric}' rows")
        count, value = number(f.get("count", "")), money(u.get("value", ""))
        if not count or value is None:
            fail(f"'{stage}' count or '{metric}' value missing")
        expected = total / count
        if abs(expected - value) / expected > 0.01:
            fail(f"{metric} should be about ${expected:,.2f} (total / {stage}), found ${value:,.2f}")

    # Skill check 4: sensitivity grid size, and break-even states CAC and payback.
    grid = [rows for head, rows in tables(secs["sensitivity"]) if len(head) >= 4]
    if not grid or max(len(rows) for rows in grid) < 3:
        fail("Sensitivity needs a grid with at least 3 reply rates and 3 close rates")
    be = secs["break-even"].lower()
    if "cac" not in be or "payback" not in be or not re.search(r"\d+(\.\d+)?\s*months", be):
        fail("Break-even must state a CAC limit and a payback in months")

    print(f"PASS - {len(inputs)} typed inputs, prices and arithmetic consistent, {len(all_rows)} table rows")
    sys.exit(0)


if __name__ == "__main__":
    main()
