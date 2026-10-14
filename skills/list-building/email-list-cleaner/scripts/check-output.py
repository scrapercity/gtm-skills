#!/usr/bin/env python3
"""Check an email list cleaning report against the email-list-cleaner output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "List Profile",
    "Cleaning Funnel",
    "Validation Results",
    "Output Files",
    "Suppression Additions",
    "Cost Estimate",
    "Re-validation Schedule",
    "Next Steps",
]
MIN_CHARS = 2500
MIN_TABLE_ROWS = 35
STATUSES = ["valid", "valid_catch_all", "unknown", "invalid", "disposable"]
FILES = ["send_ready", "catch_all", "hold_unknown", "removed"]
PRICE = 0.0072
# Deliverables carry no legal content (owner rule, 2026-10-13): the same terms that
# scripts/validate-skills.py --check-legal rejects. Bracketed letters keep this file
# from matching its own patterns; acronyms are case-sensitive like the validator's.
LEGAL = re.compile("|".join([
    r"\bCAN[- ]?SP[A]M\b", r"\bT[C]PA\b", r"Telephone Consumer Prot[e]ction",
    r"(?-i:\bC[A]SL\b)", r"(?-i:Anti-Spam Legisl[a]tion)",
    r"\bG[D]PR\b", r"General Data Protection Reg[u]lation", r"\beP[r]ivacy\b",
    r"lawful b[a]sis", r"legitimate interests? assess[m]ent",
    r"(?-i:\bC[C]PA\b|\bC[P]RA\b|California Consumer Priv[a]cy)",
    r"(?-i:\bP[E]CR\b|Privacy and Electronic Comm[u]nications)",
    r"(?-i:\bF[C]RA\b|Fair Credit Rep[o]rting)", r"(?-i:\bT[S]R\b|Telemarketing Sales R[u]le)",
    r"\b(?:47|16)\s*C[.]?F[.]?R\b",
    r"(?-i:\b(?:F[T]C|F[C]C|C[R]TC|I[C]O)\b|Federal (?:Trade|Communications) Comm[i]ssion"
    r"|Information Comm[i]ssioner|Att[o]rneys? Gen[e]ral)",
    r"\bleg[a]l adv[i]ce\b", r"\bnot leg[a]l\b",
    r"\b(?:consult|ask|check with|speak (?:to|with)|talk (?:to|with))\s+(?:with\s+)?(?:a|an|your)\s+"
    r"(?:\w+\s+)?(?:l[a]wyer|att[o]rney|couns[e]l|solic[i]tor|leg[a]l (?:team|advis[eo]r))",
    r"Do[- ]Not[- ]Call Reg[i]stry|National Do[- ]Not[- ]Call|donotc[a]ll\.gov", r"\bcompliance g[a]tes?\b",
]), re.I)



# The reader gets product names (Lead Database, Email Finder, Mobile Finder, Email
# Validator, Website Finder), never agent tool ids, skill names, repo paths or run plumbing.
INTERNAL = re.compile(
    r"\b(?:check_wallet|list_runs|check_run_status|download_results|cancel_run|query_lead_database"
    r"|query_local_business_database|find_emails|find_mobiles|find_people|validate_emails|scrape_[a-z_]+)\b"
    r"|\b(?:crm-enricher|email-list-cleaner|mobile-appender|cold-email-list|icp-list-builder"
    r"|decision-maker-finder|scrapercity-lead-database|scrapercity-integrations|skip-tracer|cold-calling)\b"
    r"|\b(?:references|templates|examples)/|SKILL\.md|check-output\.py|\bRun ID:|\"tool\"\s*:",
)

def num(text):
    m = re.search(r"-?\d[\d,]*\.?\d*", text or "")
    return float(m.group(0).replace(",", "")) if m else None


def money(text):
    m = re.search(r"\$\s*(\d[\d,]*\.?\d*)", text or "")
    return float(m.group(1).replace(",", "")) if m else None


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
        print("usage: check-output.py path/to/report.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/report.md (file not found)")
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
    legal = LEGAL.search(text)
    if legal:
        return fail(f"deliverable carries legal content ('{legal.group(0)}'); remove it (owner rule)")
    for i, line in enumerate(text.splitlines(), 1):
        m = INTERNAL.search(line)
        if m:
            return fail(f"line {i}: internal id or path '{m.group(0)}'; use product names and plain steps")
    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    all_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if all_rows < MIN_TABLE_ROWS:
        return fail(f"only {all_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Funnel: each stage equals the previous stage plus its signed change.
    funnel = table_rows(section(text, "Cleaning Funnel"))
    if len(funnel) < 5:
        return fail("Cleaning Funnel needs at least 5 stages")
    prev, added = None, 0.0
    for r in funnel:
        if len(r) < 4 or not r[3]:
            return fail(f"Cleaning Funnel stage '{r[0]}' needs Rows, Change and a Reason")
        rows, change = num(r[1]), num(r[2])
        if rows is None or change is None:
            return fail(f"Cleaning Funnel stage '{r[0]}' has non-numeric rows or change")
        if prev is None:
            raw = rows
        else:
            if abs(prev + change - rows) > 0.5:
                return fail(f"Cleaning Funnel does not add up at '{r[0]}': {prev:.0f} + {change:.0f} != {rows:.0f}")
            if change > 0:
                added += change
        prev = rows
    sent = prev

    # Validation: statuses sum to the total, and the total equals rows sent to the validator.
    found = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Validation Results")) if len(r) > 1}
    for st in STATUSES:
        if found.get(st) is None:
            return fail(f"Validation Results missing status '{st}'")
    total = next((v for k, v in found.items() if k.startswith("total")), None)
    if total is None:
        return fail("Validation Results needs a Total validated row")
    if abs(sum(found[s] for s in STATUSES) - total) > 0.5:
        return fail("validation statuses do not sum to Total validated")
    if abs(total - sent) > 0.5:
        return fail(f"Total validated {total:.0f} != rows sent to the validator {sent:.0f} (last funnel stage)")

    # Output files: required files present, and every input row lands in exactly one file.
    files = {r[0].lower(): num(r[1]) for r in table_rows(section(text, "Output Files")) if len(r) > 1}
    for f in FILES:
        if not any(k.startswith(f) for k in files):
            return fail(f"Output Files missing {f}.csv")
    ftotal = files.pop("total", None)
    if ftotal is None or None in files.values():
        return fail("Output Files needs numeric rows and a Total row")
    if abs(sum(files.values()) - ftotal) > 0.5:
        return fail("Output Files rows do not sum to Total")
    if abs(ftotal - (raw + added)) > 0.5:
        return fail(f"Output Files total {ftotal:.0f} != raw rows plus split rows {raw + added:.0f}")
    send_ready = next(v for k, v in files.items() if k.startswith("send_ready"))
    if send_ready > found["valid"] + 0.5:
        return fail("send_ready.csv has more rows than valid results; catch-all or unknown rows leaked in")

    # Cost: the Email Validator units equal the validated total and the dollar figure equals units x $0.0072.
    cost_rows = table_rows(section(text, "Cost Estimate"))
    vrow = next((r for r in cost_rows if r[0].lower().startswith("email validator")), None)
    if not vrow or len(vrow) < 4:
        return fail("Cost Estimate needs an Email Validator row")
    units, dollars = num(vrow[1]), money(vrow[3])
    if units is None or dollars is None:
        return fail("Email Validator cost row needs units and a $ cost")
    if abs(units - total) > 0.5:
        return fail(f"Email Validator units {units:.0f} != Total validated {total:.0f}")
    if abs(units * PRICE - dollars) > 0.01:
        return fail(f"Email Validator cost ${dollars:.2f} != {units:.0f} x $0.0072 = ${units * PRICE:.2f}")
    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    # Every re-validation row carries an ISO date.
    sched = table_rows(section(text, "Re-validation Schedule"))
    if len(sched) < 2:
        return fail("Re-validation Schedule needs at least 2 rows")
    for r in sched:
        if not re.search(r"\d{4}-\d{2}-\d{2}", " ".join(r)):
            return fail(f"Re-validation row '{r[0]}' has no YYYY-MM-DD date")

    print(f"PASS - {path.name}: funnel reconciles to {sent:.0f} validated, {ftotal:.0f} rows routed, cost matches $0.0072 per email")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
