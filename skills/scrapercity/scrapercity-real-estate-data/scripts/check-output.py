#!/usr/bin/env python3
"""Check a real estate data plan built from templates/output-template.md.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Objective",
    "Tool Plan",
    "Cost Estimate",
    "Contact Hygiene",
    "Outreach Routing",
    "Next Steps",
]
# Catalog prices (references/scrapercity-catalog.md). Property lookup allows 0.15 or 0.25 (with owner contact).
PRICES = {
    "scrape_zillow_agents": {0.029},
    "scrape_property_lookup": {0.15, 0.25, 0.10},
    "scrape_distress_list": {0.05},
    "scrape_crexi": {0.029},
    "scrape_bizbuysell": {0.0099},
    "find_people": {0.0199},
    "validate_emails": {0.0072},
    "find_emails": {0.05},
    "find_mobiles": {0.25},
}
# Owner rule: deliverables carry no legal content. These patterns mirror
# scripts/validate-skills.py --check-legal; the bracketed letters keep this file
# from matching its own terms.
LEGAL_ACRONYMS = re.compile(
    r"\b(?:CAN[- ]?SP[A]M|T[C]PA|T[S]R|C[A]SL|G[D]PR|C[C]PA|C[P]RA|P[E]CR|F[C]RA|G[L]BA|H[I]PAA|F[E]RPA|D[P]PA"
    r"|F[T]C|F[C]C|C[F]PB|C[R]TC|I[C]O|D[N]C)\b|\bC\.?F\.?R\b|U\.S\.C|\bRegulation [A-Z]\b"
)
LEGAL_PHRASES = re.compile(
    r"Do[- ]Not[- ]Call|Att[o]rneys? Gen[e]ral|legal advi[c]e|\bnot leg[a]l\b|permissible (?:purpose|use)"
    r"|lawful bas[i]s|\bcompliance\b|\bconsent\b|\b(?:lawy[e]r|attorn[e]y|couns[e]l)s?\b",
    re.I,
)


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

def legal_hit(text):
    m = LEGAL_ACRONYMS.search(text) or LEGAL_PHRASES.search(text)
    return m.group(0) if m else None


DISTRESS_TYPES = {"preforeclosure", "foreclosure", "auction", "bankowned"}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 1800


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


def money(s):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", s)
    return float(m.group(1).replace(",", "")) if m else None


def number(s):
    m = re.search(r"[\d,]+(?:\.\d+)?", s)
    return float(m.group(0).replace(",", "")) if m else None


def fail(msg):
    print("FAIL - " + msg)
    return 1


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
    for name in REQUIRED:
        if not re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M | re.I):
            return fail(f"missing heading '## {name}'")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")

    tools = table_rows(section(text, "Tool Plan"))
    if len(tools) < 2:
        return fail("Tool Plan needs at least 2 rows")
    for row in tools:
        params = " ".join(row)
        for v in re.findall(r"distressTypes\s*\[([^\]]*)\]", params):
            for t in re.findall(r"[A-Za-z]+", v):
                if t.lower() not in DISTRESS_TYPES:
                    return fail(f"distressTypes value '{t}' is not one of preForeclosure, foreclosure, auction, bankOwned")
        for lim in re.findall(r"(?:maxItems|searchLimit)\s*:?\s*(\d+)", params):
            if int(lim) > 500:
                return fail(f"maxItems or searchLimit {lim} is over the 500 limit")

    cost_rows = table_rows(section(text, "Cost Estimate"))
    if len(cost_rows) < 2:
        return fail("Cost Estimate needs line items and a total")
    total_line = None
    summed = 0.0
    for row in cost_rows:
        if len(row) < 4:
            return fail("each Cost Estimate row needs line, units, unit price and cost")
        if row[0].lower().startswith("total"):
            total_line = money(row[3])
            continue
        tool = next((t for t in PRICES if t in row[0]), None)
        units, price, cost = number(row[1]), money(row[2]), money(row[3])
        if None in (units, price, cost):
            return fail(f"cost row '{row[0]}' needs numeric units, $ unit price and $ cost")
        if tool and not any(abs(price - p) < 1e-9 for p in PRICES[tool]):
            return fail(f"{tool} unit price ${price} does not match the catalog")
        if abs(units * price - cost) > 0.02:
            return fail(f"cost row '{row[0]}': {units:g} x ${price} is not ${cost}")
        summed += cost
    if total_line is None:
        return fail("Cost Estimate needs a Total row with a $ figure")
    if abs(summed - total_line) > 0.02:
        return fail(f"line items sum to ${summed:.2f} but Total says ${total_line:.2f}")

    hyg_block = section(text, "Contact Hygiene")
    hyg = table_rows(hyg_block)
    if len(hyg) < 2:
        return fail("Contact Hygiene needs a row per channel (at least 2)")
    for row in hyg:
        if len(row) < 4 or not row[2] or not row[3]:
            return fail(f"Contact Hygiene row '{row[0]}' needs a rule and its operating reason")
    if not re.search(r"^Match test:\s*\S", hyg_block, re.M):
        return fail("Contact Hygiene must state the match test for owner contacts")
    if not re.search(r"^Suppression list:\s*\S", hyg_block, re.M):
        return fail("Contact Hygiene must say where the suppression list lives and how it is applied")
    legal = legal_hit(text)
    if legal:
        return fail(f"legal content in the plan ('{legal}'); state the operating rule and its reason instead")

    if len(table_rows(section(text, "Outreach Routing"))) < 2:
        return fail("Outreach Routing needs at least 2 record groups")

    print(f"PASS - real estate plan: {len(tools)} tool steps, total ${total_line:.2f}, {len(hyg)} channel hygiene rows")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
