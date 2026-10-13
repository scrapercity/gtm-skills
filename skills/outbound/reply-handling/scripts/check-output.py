#!/usr/bin/env python3
"""Check a reply handling playbook produced with the reply-handling skill.

Usage: check-output.py path/to/playbook.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import re
import sys

REQUIRED = [
    "Inbox Setup",
    "Reply Taxonomy",
    "Response Library",
    "SLAs",
    "CRM State Map",
    "Suppression Rules",
    "Auto-Reply Detection",
    "Referral Capture",
    "Weekly Review",
]
MUST_HAVE_CLASSES = ["interested", "referral", "objection", "not now", "unsubscribe", "out of office", "bounce", "wrong person", "angry"]
NO_REPLY_CLASSES = ["unsubscribe", "bounce", "angry"]
MAX_RESPONSE_WORDS = 79
MIN_WORDS = 700
MIN_TABLE_ROWS = 40
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
LAW = re.compile(r"can-spam|casl|pecr|gdpr|yahoo|google", re.IGNORECASE)
DEADLINE = re.compile(r"\d+\s*(business\s+)?(day|days|hour|hours)", re.IGNORECASE)


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


def covers(rows, key, cls):
    return [r for r in rows if cls in r.get(key, "").lower()]


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/playbook.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the playbook: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    words = len(text.split())
    if words < MIN_WORDS:
        fail(f"playbook has {words} words, minimum is {MIN_WORDS}")
    all_rows = table_rows(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"playbook has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    taxonomy = table_rows(secs["reply taxonomy"])
    slas = table_rows(secs["slas"])
    crm = table_rows(secs["crm state map"])
    for cls in MUST_HAVE_CLASSES:
        if not covers(taxonomy, "class", cls):
            fail(f"Reply Taxonomy has no '{cls}' class")
        if not covers(slas, "class", cls):
            fail(f"SLAs has no row for '{cls}'")
        if not covers(crm, "class", cls):
            fail(f"CRM State Map has no row for '{cls}'")

    # Skill check: every CRM row states a suppression decision; no-reply classes are suppressed.
    for r in crm:
        if not r.get("suppress"):
            fail(f"CRM row '{r.get('class')}' has no suppression decision")
    for cls in NO_REPLY_CLASSES:
        for r in covers(crm, "class", cls):
            if not r["suppress"].lower().startswith("yes"):
                fail(f"'{r['class']}' must be suppressed")
        for r in covers(slas, "class", cls):
            if "no sales reply" not in r.get("first response", "").lower() and "no reply" not in r.get("first response", "").lower():
                fail(f"'{r['class']}' must get no sales reply in SLAs")

    # Skill check: every response body is under 80 words.
    bodies = re.findall(r"```[a-z]*\n(.*?)```", secs["response library"], re.DOTALL)
    if len(bodies) < 8:
        fail(f"Response Library has {len(bodies)} responses, minimum is 8")
    for b in bodies:
        n = len(b.split())
        if n > MAX_RESPONSE_WORDS:
            fail(f"a response has {n} words; keep every response under 80: '{b.strip()[:50]}...'")

    # Skill check: referral capture uses find_emails; suppression names a law and a deadline.
    if "find_emails" not in secs["referral capture"]:
        fail("Referral Capture must use find_emails on the referred person")
    sup = table_rows(secs["suppression rules"])
    if not sup:
        fail("Suppression Rules has no rows")
    for r in sup:
        if not LAW.search(r.get("law or policy", "")) and "internal" not in r.get("law or policy", "").lower():
            fail(f"suppression row '{r.get('event')}' names no law or policy")
    if not any(DEADLINE.search(r.get("deadline", "")) for r in sup):
        fail("Suppression Rules needs at least one deadline in days or hours")

    print(f"PASS - {len(taxonomy)} classes, {len(bodies)} responses under 80 words, {len(all_rows)} table rows")
    sys.exit(0)


if __name__ == "__main__":
    main()
