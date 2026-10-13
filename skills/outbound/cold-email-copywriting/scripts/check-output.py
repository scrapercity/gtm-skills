#!/usr/bin/env python3
"""Check a cold email sequence produced with the cold-email-copywriting skill.

Usage: check-output.py path/to/sequence.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.

Expected shape: '## Sequence' holds '### Touch N' blocks, each with a 'Subject:'
line, a 'Send day:' line and the body in a fenced code block.
"""

import re
import sys

REQUIRED = [
    "Campaign Inputs",
    "Merge Fields and Fallbacks",
    "Sequence",
    "Subject Line Tests",
    "Footer and Compliance",
    "QA Results",
]
MAX_BODY_WORDS = 89  # every body must be under 90 words
MAX_SUBJECT_CHARS = 49
MIN_TOUCHES = 3
MIN_WORDS = 400
MIN_TABLE_ROWS = 10
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
TAG = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*(\|[^}]*)?\}\}")
LINK = re.compile(r"https?://|www\.|\b[a-z0-9-]+\.(?:com|io|co|net|org|ai)\b", re.IGNORECASE)
ADDRESS = re.compile(r"\b\d{2,6}\s+\w+.*\b(st|street|ave|avenue|rd|road|blvd|suite|ste|dr|drive|lane|ln|way|pkwy)\b|\bp\.?o\.? box\b", re.IGNORECASE)


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
                cells = [c.strip() for c in lines[j].strip("|").split("|")]
                rows.append(dict(zip(head, cells)))
                j += 1
    return rows


def body_words(body):
    # Merge tags count as one word each.
    flat = TAG.sub("X", body)
    return len(re.findall(r"[A-Za-z0-9$%][A-Za-z0-9$%'.,:/-]*", flat))


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/sequence.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the sequence: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    if len(text.split()) < MIN_WORDS:
        fail(f"document has {len(text.split())} words, minimum is {MIN_WORDS}")
    if len(table_rows(text)) < MIN_TABLE_ROWS:
        fail(f"document has {len(table_rows(text))} table rows, minimum is {MIN_TABLE_ROWS}")

    fields = {}
    for r in table_rows(secs["merge fields and fallbacks"]):
        tag = r.get("tag", "").strip("`{} ")
        if tag:
            fields[tag] = r.get("fallback", "")
    if not fields:
        fail("Merge Fields and Fallbacks has no rows")

    touches = re.split(r"^###\s+Touch\s+(\d+)\s*$", secs["sequence"], flags=re.MULTILINE)
    blocks = list(zip(touches[1::2], touches[2::2]))
    if len(blocks) < MIN_TOUCHES:
        fail(f"Sequence has {len(blocks)} touches, minimum is {MIN_TOUCHES}")

    longest = 0
    for num, block in blocks:
        subj = re.search(r"^Subject:\s*(.+)$", block, re.MULTILINE)
        if not subj:
            fail(f"touch {num} has no Subject line")
        subject = subj.group(1).strip()
        if subject.lower() != "(same thread)":
            visible = TAG.sub(lambda m: m.group(1), subject)
            if len(visible) > MAX_SUBJECT_CHARS:
                fail(f"touch {num} subject is {len(visible)} characters, keep it under 50")
            if re.match(r"(re|fwd?):", subject, re.IGNORECASE):
                fail(f"touch {num} subject fakes a reply or forward")
        if not re.search(r"^Send day:\s*\S", block, re.MULTILINE):
            fail(f"touch {num} has no Send day")
        fence = re.search(r"```[a-z]*\n(.*?)```", block, re.DOTALL)
        if not fence:
            fail(f"touch {num} body must be in a fenced code block")
        body = fence.group(1).strip()
        words = body_words(body)
        longest = max(longest, words)
        if words > MAX_BODY_WORDS:
            fail(f"touch {num} body has {words} words; every body must be under 90")
        last = [l for l in body.splitlines() if l.strip()][-1].strip()
        if not last.endswith("?"):
            fail(f"touch {num} must end with a single question; last line is '{last[:60]}'")
        if body.count("?") > 2:
            fail(f"touch {num} has {body.count('?')} question marks; keep one ask")
        links = len(LINK.findall(TAG.sub("", body)))
        if num == "1" and links:
            fail("touch 1 must not contain a link")
        if links > 1:
            fail(f"touch {num} has {links} links; one maximum")
        for m in TAG.finditer(body + "\n" + subject):
            name = m.group(1)
            if name.upper() == "RANDOM":
                continue
            if name not in fields:
                fail(f"touch {num} uses {{{{{name}}}}} which is not listed in Merge Fields and Fallbacks")
            if not fields[name] or fields[name].lower() in ("none", "-", "n/a"):
                fail(f"merge field '{name}' has no fallback")

    footer = secs["footer and compliance"]
    if not re.search(r"unsubscribe|opt[- ]?out|reply .*no|won't follow up|will not follow up", footer, re.IGNORECASE):
        fail("Footer and Compliance needs an opt-out line")
    if not ADDRESS.search(footer):
        fail("Footer and Compliance needs a postal address (CAN-SPAM)")

    print(f"PASS - {len(blocks)} touches, longest body {longest} words, {len(fields)} merge fields with fallbacks")
    sys.exit(0)


if __name__ == "__main__":
    main()
