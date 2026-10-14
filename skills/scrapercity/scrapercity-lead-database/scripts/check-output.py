#!/usr/bin/env python3
"""Check a Lead Database pull plan built from templates/output-template.md.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Request Summary",
    "Filter Spec",
    "Count Check",
    "Pull Plan",
    "Cost and Allowance",
    "Sample QA",
    "Next Steps",
]
PARAMS = {
    "url", "title", "industry", "country", "state", "city", "companyname", "companydomain",
    "seniority", "department", "minemployees", "maxemployees", "keywords", "revenuemin",
    "revenuemax", "companycountry", "companystate", "companycity", "nottitle", "notkeywords",
    "notindustry", "socialurl", "hasemail", "hasphone", "page", "limit", "excludedelivered", "after",
}
GEO = {"country", "state", "city", "companycountry", "companystate", "companycity"}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 1800
DAILY_CAP = 100000
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
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows[1:]  # drop header


def kv(block):
    return {r[0].lower(): r[1] for r in table_rows(block) if len(r) >= 2}


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

    filters = table_rows(section(text, "Filter Spec"))
    if len(filters) < 3:
        return fail("Filter Spec needs at least 3 filter rows")
    for row in filters:
        param = row[0].strip("` ").lower()
        if param not in PARAMS:
            return fail(f"Filter Spec uses '{row[0]}', which is not a query_lead_database parameter")
        if param in GEO and len(row) >= 3:
            why = row[2].lower()
            if "person" not in why and "company" not in why and "hq" not in why:
                return fail(f"geography filter '{row[0]}' must say whether it is person or company location")

    count = kv(section(text, "Count Check"))
    total = count.get("pagination.total", "")
    if not re.search(r"\d", total):
        return fail("Count Check must show pagination.total from a limit 1 call")

    plan = kv(section(text, "Pull Plan"))
    excl = plan.get("excludedelivered", "").lower()
    page = plan.get("page", "")
    page_num = re.match(r"\s*(\d+)", page)
    if excl.startswith("true") and page_num and int(page_num.group(1)) > 1:
        return fail("excludeDelivered true with page above 1 skips records; use page 1 or after")
    daily = plan.get("daily new leads", "")
    nums = [int(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", daily)]
    if not nums:
        return fail("Pull Plan must state daily new leads as a number")
    if max(nums) > DAILY_CAP:
        return fail(f"daily new leads {max(nums)} exceeds the 100,000 a day allowance")

    cost = section(text, "Cost and Allowance")
    if len(table_rows(cost)) < 2 or not re.search(r"\$\d", cost):
        return fail("Cost and Allowance needs a table with $ figures")
    if not re.search(r"total", cost, re.I):
        return fail("Cost and Allowance needs a total line")

    qa = section(text, "Sample QA")
    m = re.search(r"On-target rows\s*\|\s*(\d+)\s*/\s*(\d+)", qa, re.I)
    if not m:
        return fail("Sample QA must report on-target rows as N / sample size")
    mark = re.search(r"Pass mark[^|]*\|\s*(\d+)\s*/\s*(\d+)", qa, re.I)
    if not mark:
        return fail("Sample QA must state the pass mark set before the sample, as N / sample size")
    on, size = int(m.group(1)), int(m.group(2))
    need, mark_size = int(mark.group(1)), int(mark.group(2))
    if size != mark_size or on > size:
        return fail("Sample QA on-target rows and pass mark must use the same sample size")
    if on < need:
        return fail(f"Sample QA shows {on} / {size} on target, under the pass mark of {need}; fix filters before pulling")

    legal = LEGAL.search(text)
    if legal:
        return fail(f"legal commentary in the plan ('{legal.group(0)}'); remove it")

    print(f"PASS - lead pull plan: {len(filters)} filters, total {total}, QA {on}/{size}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
