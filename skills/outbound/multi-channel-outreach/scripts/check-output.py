#!/usr/bin/env python3
"""Check a finished multi-channel outreach plan.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import re
import sys
from pathlib import Path

REQUIRED = [
    "Summary",
    "Channel Roles",
    "Contact Tiers",
    "Cadence",
    "Compliance Gates",
    "Channel Copy",
    "Data and Cost",
    "Tracking",
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 4000
PHONE_LAW = re.compile(r"tcpa|dnc|do not call|64\.1200|tsr|telemarketing|florida|ftsa|state law|tps|crtc", re.IGNORECASE)
AUTOMATED = re.compile(r"autodial|auto-dial|prerecorded|pre-recorded|ringless|voicemail drop|ai voice|ai-generated|robocall", re.IGNORECASE)
LAW_NAMES = re.compile(r"tcpa|dnc|64\.1200|tsr|can-spam|florida|ftsa|casl|pecr|gdpr|fcra|linkedin|user agreement|terms|house rule", re.IGNORECASE)
CHANNELS = {
    "email": re.compile(r"\bemail\b", re.IGNORECASE),
    "phone": re.compile(r"\bphone\b|\bcall\b|\bsms\b|\btext\b", re.IGNORECASE),
    "linkedin": re.compile(r"linkedin", re.IGNORECASE),
    "mail": re.compile(r"direct mail|postcard|letter|\bmail\b", re.IGNORECASE),
}


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


def col(header, name):
    for i, h in enumerate(header):
        if name in h:
            return i
    return -1


def channel_of(cell):
    c = cell.lower()
    if "linkedin" in c:
        return "linkedin"
    if any(w in c for w in ("phone", "call", "sms", "text")):
        return "phone"
    if any(w in c for w in ("mail", "postcard", "letter")) and "email" not in c:
        return "mail"
    if "email" in c:
        return "email"
    return c


def fail(msg):
    print(f"FAIL - {msg}")
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/plan.md")
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

    header, rows = table(sec["cadence"])
    ci, ti, gi = col(header, "channel"), col(header, "touch"), col(header, "gate")
    if min(ci, ti, gi) < 0:
        return fail("Cadence table needs Channel, Touch and Gate columns")
    if len(rows) < 6:
        return fail("Cadence needs at least 6 touch rows")
    used = set()
    phone_rows = 0
    for r in rows:
        if len(r) <= max(ci, ti, gi):
            return fail(f"cadence row has too few cells: {' | '.join(r)[:80]}")
        ch = channel_of(r[ci])
        used.add(ch)
        touch, gate = r[ti], r[gi]
        if not gate or gate.lower() in {"none", "-", "n/a"}:
            return fail(f"cadence row without a gate: {' | '.join(r)[:80]}")
        if ch == "phone":
            phone_rows += 1
            if not PHONE_LAW.search(gate):
                return fail(f"phone touch gate must cite TCPA, DNC or a state law: {gate[:80]}")
        if AUTOMATED.search(touch) and "consent" not in gate.lower():
            return fail(f"automated or prerecorded touch without documented consent in its gate: {touch[:80]}")
        if ch == "linkedin" and "manual" not in (touch + " " + gate).lower():
            return fail(f"LinkedIn touch must be marked manual: {touch[:80]}")
    known = used & set(CHANNELS)
    if len(known) < 3:
        return fail(f"cadence uses {len(known)} channels ({', '.join(sorted(known))}); need at least 3")
    if not re.search(r"stop rule", sec["cadence"], re.IGNORECASE):
        return fail("Cadence needs a written stop rule")

    gh, grows = table(sec["compliance gates"])
    if len(grows) < 3:
        return fail("Compliance Gates needs at least 3 rows")
    for r in grows:
        if not LAW_NAMES.search(" ".join(r)):
            return fail(f"compliance gate row names no law or rule: {' | '.join(r)[:80]}")

    cost = sec["data and cost"]
    if "$" not in cost or not re.search(r"^\|\s*total", cost, re.IGNORECASE | re.MULTILINE):
        return fail("Data and Cost needs dollar figures and a Total row")
    if re.search(r"find_mobiles|mobile finder", cost, re.IGNORECASE) and "0.25" not in cost:
        return fail("Mobile Finder must be priced at $0.25 per number found")
    priced = {name for name, rx in CHANNELS.items() if rx.search(cost)}
    if len(priced) < 2:
        return fail("Data and Cost needs per-channel lines for at least 2 channels")
    if len(table(sec["tracking"])[1]) < 3:
        return fail("Tracking needs at least 3 metric rows")

    print(f"PASS - {len(rows)} touches across {len(known)} channels, {phone_rows} phone touches gated by law, stop rule and cost total present")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
