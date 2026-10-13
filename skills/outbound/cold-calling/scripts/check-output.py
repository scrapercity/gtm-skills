#!/usr/bin/env python3
"""Check a cold calling plan produced with the cold-calling skill.

Usage: check-output.py path/to/call-plan.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import re
import sys

REQUIRED = [
    "Program Summary",
    "Call List Build",
    "Compliance Gate",
    "Call Blocks",
    "Funnel Targets",
    "Call Script",
    "Objection Bank",
    "Voicemail and Gatekeeper",
    "CRM Logging",
    "Cost Estimate",
]
FUNNEL_STAGES = ["dial", "connect", "conversation", "meeting"]
SCRIPT_PARTS = ["opener", "reason", "question", "ask"]
MIN_WORDS = 900
MIN_TABLE_ROWS = 30
MIN_OBJECTIONS = 8
MAX_OBJECTION_WORDS = 45
MAX_VOICEMAIL_WORDS = 75
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
RULE = re.compile(
    r"tcpa|47 u\.?s\.?c|47 cfr|cfr|tsr|telemarketing sales rule|dnc|do not call|fcc|ftc|texas|florida|oklahoma|"
    r"maryland|casl|crtc|pecr|ico|tps|internal|house|policy|statute|law",
    re.IGNORECASE,
)
RISKY = re.compile(r"predictive|parallel dial|prerecorded|pre-recorded|ringless|ai voice|voice clon|robocall", re.IGNORECASE)
NEGATED = re.compile(r"\b(off|no|not|never|block|blocked|drop|dropped|banned|disabled|without consent)\b", re.IGNORECASE)
HOURS = re.compile(r"\d{1,2}(:\d\d)?\s*(am|pm).{0,20}\d{1,2}(:\d\d)?\s*(am|pm)", re.IGNORECASE)
DOLLAR = re.compile(r"\$\s?\d")
STOP_WORDS = re.compile(r"don.?t call|remove me|take me off|stop calling", re.IGNORECASE)


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


def words(s):
    return len(re.findall(r"[A-Za-z0-9$'%.,-]+", s))


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/call-plan.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the plan: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    n_words = len(text.split())
    if n_words < MIN_WORDS:
        fail(f"plan has {n_words} words, minimum is {MIN_WORDS}")
    all_rows = table_rows(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"plan has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    # Skill check 1: every compliance row names a rule; dialing method is manual; a calling window with hours.
    gate = table_rows(secs["compliance gate"])
    if len(gate) < 6:
        fail(f"Compliance Gate has {len(gate)} rows, minimum is 6")
    for r in gate:
        if not RULE.search(r.get("rule", "")):
            fail(f"Compliance Gate row '{r.get('check')}' names no law, rule or policy")
    method = [r for r in gate if "dialing method" in r.get("check", "").lower()]
    if not method:
        fail("Compliance Gate needs a 'Dialing method' row")
    if not re.search(r"manual|click-to-call|click to call|hand dial|by hand", method[0].get("setting or result", ""), re.IGNORECASE):
        fail("dialing method must be manual or click-to-call for cold numbers")
    if not HOURS.search(secs["compliance gate"]) and not HOURS.search(secs["program summary"]):
        fail("state the calling window with hours, for example 9am to 8pm")

    # Skill check 2: no automated or artificial voice method is allowed anywhere in the plan.
    for line in text.splitlines():
        if RISKY.search(line) and not NEGATED.search(line):
            fail(f"plan mentions an automated or artificial-voice method without ruling it out: '{line.strip()[:80]}'")

    # Skill check 3: funnel stages with numbers and a basis.
    funnel = table_rows(secs["funnel targets"])
    for stage in FUNNEL_STAGES:
        rows = [r for r in funnel if r.get("stage", "").lower().startswith(stage)]
        if not rows:
            fail(f"Funnel Targets has no '{stage}' row")
        r = rows[0]
        if not re.search(r"\d", r.get("count", "")):
            fail(f"Funnel '{r.get('stage')}' row has no count")
        basis = r.get("basis", "")
        if not (re.search(r"20\d\d", basis) or "assumption" in basis.lower() or "measured" in basis.lower()):
            fail(f"Funnel '{r.get('stage')}' row needs a dated source, 'measured', or 'assumption'")

    # Skill check 4: script has all four parts.
    script = table_rows(secs["call script"])
    parts = " ".join(r.get("part", "").lower() for r in script)
    for p in SCRIPT_PARTS:
        if p not in parts:
            fail(f"Call Script is missing the '{p}' part")

    # Skill check 5: objection bank size, length and a question in each response.
    objections = table_rows(secs["objection bank"])
    if len(objections) < MIN_OBJECTIONS:
        fail(f"Objection Bank has {len(objections)} rows, minimum is {MIN_OBJECTIONS}")
    for r in objections:
        resp = r.get("response", "")
        if words(resp) > MAX_OBJECTION_WORDS:
            fail(f"objection response over {MAX_OBJECTION_WORDS} words: '{resp[:50]}...'")
        if STOP_WORDS.search(r.get("objection", "")):
            if "remove" not in resp.lower():
                fail("a stop or don't-call objection must be answered with removal")
            continue
        if "?" not in resp:
            fail(f"objection response has no question: '{resp[:50]}...'")

    # Skill check 6: voicemail scripts stay near 30 seconds.
    vm = [r for r in table_rows(secs["voicemail and gatekeeper"]) if r.get("id", "").upper().startswith("V")]
    if not vm:
        fail("Voicemail and Gatekeeper needs at least one voicemail row with an ID starting V")
    for r in vm:
        n = words(r.get("script", ""))
        if n > MAX_VOICEMAIL_WORDS:
            fail(f"voicemail {r.get('id')} has {n} words; keep it to {MAX_VOICEMAIL_WORDS} or fewer")

    # Skill check 7: cost estimate prices mobiles at catalog price and has dollar figures.
    cost = secs["cost estimate"]
    if not DOLLAR.search(cost):
        fail("Cost Estimate has no dollar figure")
    if "find_mobiles" in cost and "$0.25" not in cost:
        fail("find_mobiles must be priced at $0.25 per number found")
    if "find_mobiles" not in cost and "no mobiles" not in cost.lower():
        fail("Cost Estimate must price find_mobiles or say 'no mobiles' were bought")
    if not re.search(r"total", cost, re.IGNORECASE):
        fail("Cost Estimate needs a total row")

    print(f"PASS - {len(gate)} gate rows, {len(objections)} objections, {len(vm)} voicemails, {len(all_rows)} table rows")
    sys.exit(0)


if __name__ == "__main__":
    main()
