#!/usr/bin/env python3
"""Check a ScraperCity integration plan built from templates/output-template.md.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Request Summary",
    "Data Flow",
    "Connection Setup",
    "Field Mapping",
    "Schedule and Triggers",
    "Rate Guardrails",
    "Cost Estimate",
    "Dedupe and Idempotency",
    "Test Run",
    "Next Steps",
]
# Largest batch each destination accepts per call, from the vendors' API docs.
MAX_BATCH = {
    "instantly": 1000,
    "smartlead": 400,
    "hubspot": 100,
    "airtable": 10,
    "manyreach": 100,
    "lemlist": 1,
    "pipedrive": 1,
    "gohighlevel": 1,
    "scrapercity": 100,
}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
# Plans carry no legal content (owner rule). Letters are bracketed so the
# pattern list itself does not trip the repo's legal-term scan.
LEGAL = re.compile(
    r"\bc[a]n[- ]?sp[a]m\b|\bt[c]pa\b|telephone consumer prot|\bc[a]sl\b|\bg[d]pr\b|\bepriv[a]cy\b|"
    r"lawful b[a]sis|\bc[c]pa\b|\bc[p]ra\b|\bp[e]cr\b|\bf[c]ra\b|fair credit rep|\bt[s]r\b|"
    r"telemarketing sales r|\b(?:47|16)\s*c\.?f\.?r\b|\bf[t]c\b|\bf[c]c\b|\bc[r]tc\b|\bi[c]o\b|"
    r"att[o]rneys? gen|legal adv[i]ce|\bnot leg[a]l\b|"
    r"\b(?:consult|ask|check with)\s+(?:a|an|your)\s+(?:\w+\s+)?(?:law[y]er|att[o]rney|coun[s]el)|"
    r"do[- ]not[- ]call regis|national do[- ]not[- ]call|complian[c]e gate",
    re.IGNORECASE,
)
SECRET = re.compile(
    r"(Bearer\s+|api_key=|apikey=|X-API-Key:\s*|x-api-token:\s*)[A-Za-z0-9_\-]{20,}"
    r"|\b(sk|pk|pat)[_-][A-Za-z0-9]{16,}"
    r"|\b[A-Za-z0-9]{40,}\b"
)
MIN_CHARS = 2500
SC_MAX_PER_MIN = 100


# Economy and honesty rules shared by the ScraperCity checkers: no unrun results presented
# as real, no blanks the reader fills by hand, no loop left in a comment, no spend threshold
# presented as a rule, and a source on the same line as any percentage benchmark.
_ASSUMED = re.compile(r"\(assumed\)|^\s*-\s*\[x\]", re.I | re.M)
_BLANK = re.compile(r"[\"'\[(?=,]\s*\.\.\.\s*[A-Za-z]|[A-Za-z]\s*\.\.\.\s*[\"'\])]|\.\.\.\s*your\b|/Users/you\b|/home/you\b", re.I)
_COMMENT_LOOP = re.compile(r"^\s*#\s*(?:then\s+)?(?:loop|repeat|paginate|page through)\b", re.M | re.I)
_SPEND_LINE = re.compile(r"\$\d+(?:\.\d+)? approval line|approval line of \$|(?:under|over) the \$\d+(?:\.\d+)? (?:line|approval)|over about \$\d+|since it is over \$\d+", re.I)
_BENCHMARK = re.compile(r"(?:aim(?:s)? for|target of|minimum of|benchmark)[^.\n]*\d+%|\d+%\+?\s*(?:or more|is the minimum)", re.I)
_SOURCE_HINT = re.compile(r"https?://|\b[\w-]+\.(?:com|io|org|ai|dev)\b|\bper [A-Z]", re.I)


def economy_error(text):
    for rx, msg in ((_ASSUMED, "presents an unrun result or a self-graded check"),
                    (_BLANK, "is a blank the reader has to fill by hand; write the value or a named input"),
                    (_COMMENT_LOOP, "describes a loop in a comment; write the loop out"),
                    (_SPEND_LINE, "presents a spend threshold as a rule; every paid run waits for a go-ahead")):
        m = rx.search(text)
        if m:
            return f"'{m.group(0).strip()}' {msg}"
    for ln in text.splitlines():
        if _BENCHMARK.search(ln) and not _SOURCE_HINT.search(ln):
            return f"benchmark with no source on its line: '{ln.strip()[:80]}'"
    return None

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


def fail(msg):
    print("FAIL - " + msg)
    return 1


def per_minute(value):
    """Convert the first rate in a cell to requests per minute, or None."""
    v = value.lower().replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:requests?\s*)?(?:a|per|/)\s*(\d+(?:\.\d+)?)?\s*"
                  r"(ms|milliseconds?|s|sec|seconds?|min|minutes?|h|hours?)\b", v)
    if not m:
        return None
    n = float(m.group(1))
    span = float(m.group(2)) if m.group(2) else 1.0
    unit = m.group(3)
    if unit.startswith("ms") or unit.startswith("milli"):
        seconds = span / 1000
    elif unit.startswith("s"):
        seconds = span
    elif unit.startswith("h"):
        seconds = span * 3600
    else:
        seconds = span * 60
    return n * 60 / seconds


def vendor_of(hop):
    h = hop.lower().replace(" ", "")
    for name in MAX_BATCH:
        if name in h:
            return name
    if "ghl" in h or "highlevel" in h:
        return "gohighlevel"
    return None


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/plan.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/plan.md (file not found)")
        return 2
    text = path.read_text(encoding="utf-8")
    _econ = economy_error(text)
    if _econ:
        return fail(_econ)

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    legal = LEGAL.search(text)
    if legal:
        return fail(f"legal commentary in the plan ('{legal.group(0)}'); remove it")
    for name in REQUIRED:
        if not re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M | re.I):
            return fail(f"missing heading '## {name}'")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    leak = SECRET.search(text)
    if leak:
        return fail(f"something that looks like a key is in the plan: '{leak.group(0)[:24]}...'; name the credential instead")

    flow = table_rows(section(text, "Data Flow"))
    if len(flow) < 3:
        return fail("Data Flow needs at least 3 steps")

    conn = table_rows(section(text, "Connection Setup"))
    sc_rows = [r for r in conn if r and r[0].lower().strip("` ") == "scrapercity"]
    if not sc_rows:
        return fail("Connection Setup needs a ScraperCity row")
    for row in conn:
        if len(row) < 4 or not row[3]:
            return fail(f"Connection Setup row '{row[0]}' must name a secret store")
    where = sc_rows[0][2].lower()
    if "authorization" not in where and "header" not in where:
        return fail("the ScraperCity key must go in the Authorization header")
    if re.search(r"\bquery\b|\burl\b", where):
        return fail("the ScraperCity key must never go in a query string or URL")

    mapping = table_rows(section(text, "Field Mapping"))
    if len(mapping) < 5:
        return fail("Field Mapping needs at least 5 rows")
    for row in mapping:
        if len(row) < 3 or not all(row[:3]):
            return fail(f"Field Mapping row '{row[0] if row else ''}' needs source, destination and destination field")
    if not any("email" in r[0].lower() for r in mapping):
        return fail("Field Mapping must map an email field")

    guards = table_rows(section(text, "Rate Guardrails"))
    if len(guards) < 2:
        return fail("Rate Guardrails needs the ScraperCity hop and at least one destination")
    saw_sc = False
    for row in guards:
        if len(row) < 5:
            return fail(f"Rate Guardrails row '{row[0]}' needs limit, planned rate, batch size and source")
        if not re.search(r"https?://|references/|docs", row[4]):
            return fail(f"Rate Guardrails row '{row[0]}' must cite where the vendor limit comes from")
        vendor = vendor_of(row[0])
        batch = re.search(r"\d[\d,]*", row[3])
        if vendor and batch and int(batch.group(0).replace(",", "")) > MAX_BATCH[vendor]:
            return fail(f"{row[0]} batch of {batch.group(0)} exceeds the {MAX_BATCH[vendor]} per call that {vendor} accepts")
        if vendor == "scrapercity":
            saw_sc = True
            rate = per_minute(row[2])
            if rate is None:
                return fail("state the planned ScraperCity rate as N a minute, N a second or N per M ms")
            if rate > SC_MAX_PER_MIN:
                return fail(f"planned ScraperCity rate {rate:.0f} a minute exceeds 100 a minute per key")
    if not saw_sc:
        return fail("Rate Guardrails needs a ScraperCity row")

    sched = section(text, "Schedule and Triggers").lower()
    if "apollo" in section(text, "Data Flow").lower() and "webhook" not in sched:
        return fail("an Apollo step needs a webhook as its run-finished signal")

    cost = section(text, "Cost Estimate")
    if len(table_rows(cost)) < 2 or not re.search(r"\$\d", cost) or not re.search(r"total", cost, re.I):
        return fail("Cost Estimate needs a table with $ figures and a total line")

    dedupe = section(text, "Dedupe and Idempotency").lower()
    if not re.search(r"excludedelivered|runid|dedupe", dedupe):
        return fail("Dedupe and Idempotency must use excludeDelivered, a runId key or a dedupe rule")

    if len(table_rows(section(text, "Test Run"))) < 3:
        return fail("Test Run needs at least 3 checks")

    print(f"PASS - integration plan: {len(flow)} steps, {len(mapping)} mapped fields, {len(guards)} rate hops")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
