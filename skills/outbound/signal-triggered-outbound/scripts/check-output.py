#!/usr/bin/env python3
"""Check a signal program produced with the signal-triggered-outbound skill.

Usage: check-output.py path/to/signal-program.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import re
import sys
from datetime import date

REQUIRED = [
    "Program Summary",
    "Signal Catalog",
    "Scoring Model",
    "Repeat Pull Schedule",
    "Message Angles",
    "Signal Queue",
    "Routing and SLAs",
    "Cost Estimate",
]
TOOLS = [
    "query_local_business_database", "query_lead_database", "scrape_maps", "scrape_yelp", "scrape_angi",
    "scrape_builtwith", "scrape_store_leads", "scrape_bizbuysell", "scrape_distress_list",
    "scrape_zillow_agents", "scrape_crexi", "scrape_property_lookup", "ecommerce database",
]
OUTSIDE = re.compile(r"funding|job post|hiring|job change|intent data|press", re.IGNORECASE)
MIN_WORDS = 600
MIN_TABLE_ROWS = 25
MIN_SIGNALS = 3
MAX_FIRST_LINE_WORDS = 30
TIER_A, TIER_B = 70, 40
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
SIG_ID = re.compile(r"\bS\d+\b")
ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
DOLLAR = re.compile(r"\$\s?\d")


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


def table_rows(block):
    rows = []
    lines = [l.strip() for l in block.splitlines()]
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", lines[i + 1]):
            head = [h.strip().lower() for h in line.strip("|").split("|")]
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(dict(zip(head, [c.strip() for c in lines[j].strip("|").split("|")])))
                j += 1
    return rows


def col(row, prefix):
    for k, v in row.items():
        if k.startswith(prefix):
            return v
    return ""


def num(s):
    m = re.search(r"-?\d+(\.\d+)?", s.replace(",", ""))
    return float(m.group(0)) if m else None


def to_date(s):
    m = ISO.search(s)
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/signal-program.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the program: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    if len(text.split()) < MIN_WORDS:
        fail(f"program has {len(text.split())} words, minimum is {MIN_WORDS}")
    all_rows = table_rows(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"program has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    # Skill check 1: each signal uses a ScraperCity tool (or is labeled as outside data) and has half-life and max age.
    catalog = table_rows(secs["signal catalog"])
    if len(catalog) < MIN_SIGNALS:
        fail(f"Signal Catalog has {len(catalog)} signals, minimum is {MIN_SIGNALS}")
    max_age = {}
    for r in catalog:
        name = r.get("signal", "")
        ids = SIG_ID.findall(name)
        if not ids:
            fail(f"catalog signal '{name}' needs an ID such as S5")
        tool = r.get("tool", "").lower()
        if not any(t in tool for t in TOOLS):
            if "other source" not in tool:
                fail(f"signal '{name}' names no ScraperCity tool and is not labeled 'other source'")
        if OUTSIDE.search(name) and "other source" not in tool:
            fail(f"signal '{name}' is not something ScraperCity tools show; label it 'other source'")
        hl, ma = num(col(r, "half-life")), num(col(r, "max age"))
        if hl is None or ma is None or hl <= 0:
            fail(f"signal '{name}' needs a numeric half-life and max age")
        if ma < hl:
            fail(f"signal '{name}' max age {ma:g} is shorter than its half-life {hl:g}")
        max_age[ids[0]] = ma

    # Skill check 2: every signal has an angle, and first lines stay short.
    angles = table_rows(secs["message angles"])
    covered = {i for r in angles for i in SIG_ID.findall(r.get("signal", ""))}
    for sid in max_age:
        if sid not in covered:
            fail(f"signal {sid} has no row in Message Angles")
    for r in angles:
        n = len(r.get("first line", "").split())
        if n == 0 or n > MAX_FIRST_LINE_WORDS:
            fail(f"first line for {r.get('signal')} has {n} words; keep it between 1 and {MAX_FIRST_LINE_WORDS}")

    # Skill check 3: queue rows are dated, fresh, scored and tiered consistently.
    cycle = None
    for r in table_rows(secs["program summary"]):
        if "cycle date" in r.get("item", "").lower():
            cycle = to_date(r.get("value", ""))
    queue = table_rows(secs["signal queue"])
    if not queue:
        fail("Signal Queue has no rows")
    for r in queue:
        acct = r.get("account", "")
        ids = SIG_ID.findall(r.get("signal", ""))
        if not ids:
            fail(f"queue row '{acct}' has no signal ID")
        for sid in ids:
            if sid not in max_age:
                fail(f"queue row '{acct}' uses {sid}, which is not in the Signal Catalog")
        sdate = to_date(r.get("signal date", ""))
        if not sdate:
            fail(f"queue row '{acct}' needs an ISO signal date (YYYY-MM-DD)")
        age = num(col(r, "age"))
        if age is None:
            fail(f"queue row '{acct}' has no age")
        if cycle and int(age) != (cycle - sdate).days:
            fail(f"queue row '{acct}' age {age:g} does not match cycle date minus signal date ({(cycle - sdate).days})")
        if age > max(max_age[s] for s in ids):
            fail(f"queue row '{acct}' is {age:g} days old, past the signal's max age")
        score = num(r.get("score", ""))
        if score is None or not 0 <= score <= 100:
            fail(f"queue row '{acct}' needs a score from 0 to 100")
        tier = r.get("tier", "").strip().upper()[:1]
        expected = "A" if score >= TIER_A else "B" if score >= TIER_B else "C"
        if tier != expected:
            fail(f"queue row '{acct}' score {score:g} should be tier {expected}, not {tier or 'blank'}")

    # Skill check 4: every repeat pull has a frequency and a dollar cost; the estimate has a total.
    pulls = table_rows(secs["repeat pull schedule"])
    if not pulls:
        fail("Repeat Pull Schedule has no rows")
    for r in pulls:
        if not r.get("frequency"):
            fail(f"pull '{r.get('pull')}' has no frequency")
        if not DOLLAR.search(r.get("cost per run", "")):
            fail(f"pull '{r.get('pull')}' has no dollar cost per run")
    cost = secs["cost estimate"]
    if not DOLLAR.search(cost) or not re.search(r"total", cost, re.IGNORECASE):
        fail("Cost Estimate needs dollar figures and a total row")

    print(f"PASS - {len(catalog)} signals, {len(queue)} queue rows tiered, {len(all_rows)} table rows")
    sys.exit(0)


if __name__ == "__main__":
    main()
