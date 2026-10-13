#!/usr/bin/env python3
"""Check a finished mailbox roster and ramp plan.

Usage: check-output.py path/to/roster.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import re
import sys
from datetime import date
from pathlib import Path

REQUIRED = [
    "Summary",
    "Sender Identities",
    "Mailbox Roster",
    "Signature Block",
    "Warmup and Ramp Schedule",
    "Sending Rules",
    "Reply Monitoring",
    "Rotation and Retirement",
    "List Feed and Cost",
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 3500
MAX_CAP = 50
MIN_WARMUP_DAYS = 14
OPT_OUT = re.compile(r"unsubscribe|opt[ -]?out|no thanks|won't follow up|will not follow up|remove", re.IGNORECASE)
POSTAL = re.compile(r"\b\d{5}(?:-\d{4})?\b|\bP\.?O\.? Box\b|\b[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}\b", re.IGNORECASE)


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


def table(block):
    """Return (header, rows) for the first markdown table in block."""
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    if not rows:
        return [], []
    return [h.lower() for h in rows[0]], rows[1:]


def col(header, *names):
    for i, h in enumerate(header):
        if any(n in h for n in names):
            return i
    return -1


def first_int(s):
    m = re.search(r"\d+", s)
    return int(m.group(0)) if m else None


def parse_date(s):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def fail(msg):
    print(f"FAIL - {msg}")
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/roster.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"usage: file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    sec = sections(text)
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")

    header, rows = table(sec["mailbox roster"])
    if len(rows) < 2:
        return fail("Mailbox Roster needs at least 2 mailbox rows")
    idx = {
        "mailbox": col(header, "mailbox"),
        "owner": col(header, "owner"),
        "role": col(header, "role"),
        "warm": col(header, "warmup start"),
        "first": col(header, "first cold send"),
        "cap": col(header, "cap"),
        "routing": col(header, "routing"),
    }
    missing = [k for k, v in idx.items() if v < 0]
    if missing:
        return fail(f"Mailbox Roster is missing columns: {', '.join(missing)}")
    active = reserve = 0
    for r in rows:
        if len(r) < len(header):
            return fail(f"roster row has too few cells: {' | '.join(r)[:80]}")
        box = r[idx["mailbox"]]
        if "@" not in box:
            return fail(f"roster row without a mailbox address: {box}")
        owner = r[idx["owner"]].lower()
        if not owner or owner in {"none", "n/a", "-", "unassigned"}:
            return fail(f"{box} has no owner; every mailbox needs a real person")
        cap = first_int(r[idx["cap"]])
        if cap is None or cap > MAX_CAP:
            return fail(f"{box} cold cap must be a number of {MAX_CAP} or less")
        if "reply-to" in r[idx["routing"]].lower():
            return fail(f"{box} routes replies with a Reply-To header; keep replies on the sending mailbox")
        if "reserve" in r[idx["role"]].lower():
            reserve += 1
            if cap != 0:
                return fail(f"{box} is a reserve mailbox and must have a cold cap of 0")
            continue
        active += 1
        warm, first = parse_date(r[idx["warm"]]), parse_date(r[idx["first"]])
        if not warm or not first:
            return fail(f"{box} needs a warmup start and first cold send date (YYYY-MM-DD)")
        if (first - warm).days < MIN_WARMUP_DAYS:
            return fail(f"{box} first cold send is {(first - warm).days} days after warmup start; minimum {MIN_WARMUP_DAYS}")
    if active == 0:
        return fail("roster has no active mailboxes")

    sig = sec["signature block"]
    if not POSTAL.search(sig):
        return fail("Signature Block needs a postal address (ZIP, postcode or PO Box)")
    if not OPT_OUT.search(sig):
        return fail("Signature Block needs an opt-out line")

    rh, rrows = table(sec["warmup and ramp schedule"])
    ci = col(rh, "cold cap")
    if ci < 0 or len(rrows) < 3:
        return fail("Warmup and Ramp Schedule needs a 'Cold cap' column and at least 3 rows")
    caps = [first_int(r[ci]) for r in rrows if len(r) > ci and first_int(r[ci]) is not None]
    positive = [c for c in caps if c > 0]
    if not positive or positive[0] > 10:
        return fail("ramp must start cold sends at 10 or fewer per mailbox")
    if max(caps) > MAX_CAP:
        return fail(f"ramp cap above {MAX_CAP}")
    if caps[0] != 0:
        return fail("first ramp row must be warmup only (cold cap 0)")

    if not re.search(r"\d{1,2}:\d{2}", sec["sending rules"]):
        return fail("Sending Rules needs an hour window like 08:00 to 17:00")
    _, ret = table(sec["rotation and retirement"])
    if len(ret) < 3 or "%" not in sec["rotation and retirement"]:
        return fail("Rotation and Retirement needs pause, rest and retire rows with numeric (%) triggers")
    cost = sec["list feed and cost"]
    if "$" not in cost or "0.0072" not in cost:
        return fail("List Feed and Cost needs validation priced at $0.0072 per email")

    print(f"PASS - {active} active and {reserve} reserve mailboxes, all owned, caps <= {MAX_CAP}, {MIN_WARMUP_DAYS}+ day warmup, signature has address and opt-out")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
