#!/usr/bin/env python3
"""Check an account brief against the account-researcher output contract.

Usage: check-output.py path/to/brief.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Account Snapshot",
    "Why Now",
    "Tech Stack",
    "Key People",
    "Hypothesis and Talking Points",
    "Contact Plan",
    "Sources",
    "Cost Estimate",
    "Open Questions and Next Steps",
]
MIN_CHARS = 2500
MIN_TABLE_ROWS = 25
STATUSES = {"valid", "valid_catch_all", "unknown", "invalid", "disposable", "none"}
FOUND_BY = {"lead_db", "website_finder", "email_finder", "user_upload", "apollo"}
TECH_STATUS = {"confirmed", "likely", "not detected"}
SRC = re.compile(r"\bS(\d+)\b")
DATE = re.compile(r"\d{4}-\d{2}(-\d{2})?")


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
        print("usage: check-output.py path/to/brief.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/brief.md (file not found)")
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")

    headings = {h.strip().lower() for h in re.findall(r"^## (.+?)\s*$", text, re.M)}
    missing = [h for h in REQUIRED if h.lower() not in headings]
    if missing:
        return fail("missing sections: " + ", ".join(missing))
    hit = re.search(r"\[(fill|todo|tbd)[^\]]*\]", text, re.I)
    if hit:
        return fail("placeholder left in: " + hit.group(0))
    angle = re.search(r"<[A-Za-z][^>@\n]{0,60}>", text)
    if angle:
        return fail("angle-bracket placeholder left in: " + angle.group(0))
    if len(text) < MIN_CHARS:
        return fail(f"brief too short ({len(text)} chars, need {MIN_CHARS})")
    all_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if all_rows < MIN_TABLE_ROWS:
        return fail(f"only {all_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Sources: S-numbered, each with a URL and a date checked.
    sources = {}
    for r in table_rows(section(text, "Sources")):
        m = re.fullmatch(r"S(\d+)", r[0]) if r else None
        if not m or len(r) < 4:
            return fail("Sources rows need ID (S1, S2...), Source, URL, Date checked")
        if not re.search(r"https?://", r[2]):
            return fail(f"source {r[0]} has no URL")
        if not DATE.search(r[3]):
            return fail(f"source {r[0]} has no date checked")
        sources[m.group(1)] = r
    if len(sources) < 3:
        return fail("Sources needs at least 3 entries")

    def cited(cell, where):
        ids = SRC.findall(cell)
        if not ids:
            return f"{where} cites no source ID"
        bad = [i for i in ids if i not in sources]
        if bad:
            return f"{where} cites S{bad[0]}, which is not in Sources"
        return None

    # Why Now: each signal is dated, typed with an Elias category, and cited.
    why = table_rows(section(text, "Why Now"))
    if len(why) < 2:
        return fail("Why Now needs at least 2 dated signals")
    for r in why:
        if len(r) < 5 or not DATE.search(r[1]):
            return fail(f"Why Now signal '{r[0]}' has no date")
        if not re.search(r"transition|bad experience|awareness", r[2], re.I):
            return fail(f"Why Now signal '{r[0]}' needs an Elias category (transition, bad experience, awareness)")
        err = cited(r[4], f"Why Now signal '{r[0]}'")
        if err:
            return fail(err)

    # Tech stack: status vocabulary, a yes/no pitch flag, a cited source.
    stack = table_rows(section(text, "Tech Stack"))
    if not stack:
        return fail("Tech Stack is empty")
    paid = False
    for r in stack:
        if len(r) < 5:
            return fail("Tech Stack rows need Technology, Status, Evidence, Changes pitch?, Source")
        if r[1].lower() not in TECH_STATUS:
            return fail(f"Tech Stack '{r[0]}' status must be confirmed, likely or not detected")
        if r[3].lower() not in {"yes", "no"}:
            return fail(f"Tech Stack '{r[0]}' needs yes or no under Changes pitch?")
        ev = r[2].lower()
        if "tech stack search" in ev and not re.search(r"\bnot\b[^.]*tech stack search", ev):
            paid = True
            if r[3].lower() != "yes":
                return fail(f"Tech Stack Search was paid for '{r[0]}', which does not change the pitch")
        err = cited(r[4], f"Tech Stack '{r[0]}'")
        if err:
            return fail(err)
    cost = section(text, "Cost Estimate")
    if paid and "$4.99" not in cost:
        return fail("Tech Stack Search used but Cost Estimate has no $4.99 per technology line")

    # Key people: 2+, each with a role, a known status and a known tool.
    people = table_rows(section(text, "Key People"))
    if len(people) < 2:
        return fail("Key People needs at least 2 people")
    for r in people:
        if len(r) < 7 or not r[2]:
            return fail(f"person '{r[0]}' has no buying role")
        if r[4].lower() not in STATUSES:
            return fail(f"person '{r[0]}' has email_status '{r[4]}'")
        if r[5].lower() not in FOUND_BY:
            return fail(f"person '{r[0]}' has found_by '{r[5]}'")

    # Talking points: every one cites a listed source.
    tps = table_rows(section(text, "Hypothesis and Talking Points"))
    if len(tps) < 3:
        return fail("need at least 3 talking points")
    for r in tps:
        err = cited(" ".join(r[1:]), f"talking point {r[0]}")
        if err:
            return fail(err)

    # Contact plan: never two people on the same day.
    days = [r[3].strip().lower() for r in table_rows(section(text, "Contact Plan")) if len(r) > 3]
    if not days:
        return fail("Contact Plan is empty")
    if len(days) != len(set(days)):
        return fail("Contact Plan puts two touches at the account on the same day")

    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: {len(sources)} sources, {len(tps)} cited talking points, {len(people)} people, contact days unique")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
