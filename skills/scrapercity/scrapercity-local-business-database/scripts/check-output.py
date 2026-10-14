#!/usr/bin/env python3
"""Check a Local Business Database pull plan built from templates/output-template.md.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Request Summary",
    "Search Spec",
    "Count Check",
    "Segments",
    "Pull Plan",
    "Cost Estimate",
    "Sample QA",
    "Next Steps",
]
PARAMS = {
    "keyword", "location", "url", "category", "country", "state", "city", "postalcode", "box",
    "query", "title", "notcategory", "minrating", "maxrating", "minreviews", "maxreviews",
    "hasemail", "hasphone", "haswebsite", "hascontact", "page", "limit", "excludedelivered", "after",
}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 1800
DAILY_CAP = 100000

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


def kv(block):
    return {r[0].lower(): r[1] for r in table_rows(block) if len(r) >= 2}


def fail(msg):
    print("FAIL - " + msg)
    return 1


def check_box(value):
    nums = re.findall(r"-?\d+(?:\.\d+)?", value)
    if len(nums) != 4:
        return "box must be four numbers minLat,minLng,maxLat,maxLng"
    a, b, c, d = map(float, nums)
    if not (a < c and b < d):
        return "box min values must be below max values"
    if not (-90 <= a <= 90 and -90 <= c <= 90 and -180 <= b <= 180 and -180 <= d <= 180):
        return "box coordinates out of range"
    return ""


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
    legal = legal_hit(text)
    if legal:
        return fail(f"legal content in the plan ('{legal}'); state the setting and the result it changes instead")

    spec = table_rows(section(text, "Search Spec"))
    if len(spec) < 3:
        return fail("Search Spec needs at least 3 rows")
    for row in spec:
        param = row[0].strip("` ").lower()
        if param not in PARAMS:
            return fail(f"Search Spec uses '{row[0]}', which is not a query_local_business_database parameter")
        value = row[1] if len(row) > 1 else ""
        if param == "country":
            codes = re.findall(r"[A-Za-z]+", value)
            if not codes or any(len(c) != 2 for c in codes):
                return fail(f"country must be two-letter codes, got '{value}'")
        if param == "box":
            err = check_box(value)
            if err:
                return fail(err)

    count = kv(section(text, "Count Check"))
    if not re.search(r"\d", count.get("pagination.total", "")):
        return fail("Count Check must show pagination.total from a limit 1 call")

    segs = table_rows(section(text, "Segments"))
    if len(segs) < 2:
        return fail("Segments needs at least 2 rating or review segments")
    for row in segs:
        if len(row) < 4:
            return fail("each segment row needs segment, rating band, review band and count")
        if not re.search(r"\d", row[1] + row[2]):
            return fail(f"segment '{row[0]}' must state a numeric rating or review band")
        if not re.search(r"\d", row[3]):
            return fail(f"segment '{row[0]}' must state a count")

    plan = kv(section(text, "Pull Plan"))
    excl = plan.get("excludedelivered", "").lower()
    pg = re.match(r"\s*(\d+)", plan.get("page", ""))
    if excl.startswith("true") and pg and int(pg.group(1)) > 1:
        return fail("excludeDelivered true with page above 1 skips records; use page 1 or after")
    nums = [int(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", plan.get("daily new businesses", ""))]
    if not nums:
        return fail("Pull Plan must state daily new businesses as a number")
    if max(nums) > DAILY_CAP:
        return fail(f"daily new businesses {max(nums)} exceeds the 100,000 a day allowance")

    cost = section(text, "Cost Estimate")
    if len(table_rows(cost)) < 2 or not re.search(r"\$\d", cost) or not re.search(r"total", cost, re.I):
        return fail("Cost Estimate needs a table with $ figures and a total line")

    m = re.search(r"(\d+)\s*/\s*(\d+)", section(text, "Sample QA"))
    if not m:
        return fail("Sample QA must report on-target rows as N / M")
    if int(m.group(2)) == 0 or int(m.group(1)) > int(m.group(2)):
        return fail(f"Sample QA count {m.group(1)} / {m.group(2)} is not a valid count")

    print(f"PASS - local pull plan: {len(spec)} search rows, {len(segs)} segments, QA {m.group(1)}/{m.group(2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
