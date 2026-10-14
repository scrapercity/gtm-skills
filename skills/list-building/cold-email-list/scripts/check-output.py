#!/usr/bin/env python3
"""Check a cold email list report against the cold-email-list output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import math
import re
import sys
from pathlib import Path

REQUIRED = [
    "Campaign Brief",
    "Sourcing Plan",
    "Count Check",
    "Pipeline Funnel",
    "Validation Results",
    "Send Capacity",
    "Sequencer Import",
    "Cost Estimate",
    "Sample Rows",
    "Launch Checklist",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 50
STATUSES = ["valid", "valid_catch_all", "unknown", "invalid", "disposable"]
# Alex Berman's beginner setup keeps each inbox under 50 cold emails a day
# (alexberman.com/cold-email-tam-strategy-skip-followups-breakdown).
MAX_PER_MAILBOX = 50
# Instantly import rule: headers of 20 characters or fewer (help.instantly.ai, upload leads with a CSV).
MAX_HEADER = 20
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

    # Count check shows a numeric total.
    counts = [num(r[1]) for r in table_rows(section(text, "Count Check")) if len(r) > 1]
    if not any(c for c in counts if c):
        return fail("Count Check has no numeric pagination.total")

    # Funnel: each stage = previous + change, every change has a reason.
    funnel = table_rows(section(text, "Pipeline Funnel"))
    if len(funnel) < 6:
        return fail("Pipeline Funnel needs at least 6 stages")
    prev = None
    for r in funnel:
        if len(r) < 4 or not r[3]:
            return fail(f"Pipeline Funnel stage '{r[0]}' needs Rows, Change and a Reason")
        rows, change = num(r[1]), num(r[2])
        if rows is None or change is None:
            return fail(f"Pipeline Funnel stage '{r[0]}' has non-numeric values")
        if prev is not None and abs(prev + change - rows) > 0.5:
            return fail(f"Pipeline Funnel does not add up at '{r[0]}'")
        prev = rows
    send_ready = prev

    # Validation: sums to total; total = rows entering validation; valid = rows kept by it.
    found = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Validation Results")) if len(r) > 1}
    for st in STATUSES:
        if found.get(st) is None:
            return fail(f"Validation Results missing status '{st}'")
    vtotal = next((v for k, v in found.items() if k.startswith("total")), None)
    if vtotal is None or abs(sum(found[s] for s in STATUSES) - vtotal) > 0.5:
        return fail("validation statuses do not sum to Total validated")
    vidx = next((i for i, r in enumerate(funnel) if re.search(r"\bvalid\b", r[0], re.I)), None)
    if vidx is None or vidx == 0:
        return fail("Pipeline Funnel needs a 'Keep valid' stage after earlier stages")
    if abs(num(funnel[vidx - 1][1]) - vtotal) > 0.5:
        return fail("Total validated must equal the rows entering the validation stage")
    if abs(num(funnel[vidx][1]) - found["valid"]) > 0.5:
        return fail("rows after the validation stage must equal the valid count")

    # Send capacity arithmetic.
    cap = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Send Capacity")) if len(r) > 1}
    need = ["send-ready rows", "mailboxes", "sends per mailbox per day", "daily send capacity",
            "steps per prospect", "total sends", "sending days"]
    for k in need:
        if cap.get(k) is None:
            return fail(f"Send Capacity missing numeric '{k}'")
    if abs(cap["send-ready rows"] - send_ready) > 0.5:
        return fail("Send-ready rows must equal the last Pipeline Funnel stage")
    if cap["sends per mailbox per day"] >= MAX_PER_MAILBOX:
        return fail(f"sends per mailbox per day must stay under {MAX_PER_MAILBOX} (Alex Berman)")
    if abs(cap["mailboxes"] * cap["sends per mailbox per day"] - cap["daily send capacity"]) > 0.5:
        return fail("mailboxes x sends per mailbox != daily send capacity")
    if abs(cap["send-ready rows"] * cap["steps per prospect"] - cap["total sends"]) > 0.5:
        return fail("send-ready rows x steps != total sends")
    if math.ceil(cap["total sends"] / cap["daily send capacity"]) != int(cap["sending days"]):
        return fail("sending days must be total sends / daily capacity, rounded up")

    # Import headers: unique, no spaces, 20 characters or fewer, an email header present.
    imp = table_rows(section(text, "Sequencer Import"))
    headers = [r[1] for r in imp if len(r) > 1]
    if not headers:
        return fail("Sequencer Import has no headers")
    if len({h.lower() for h in headers}) != len(headers):
        return fail("Sequencer Import headers must be unique")
    for h in headers:
        if len(h) > MAX_HEADER or " " in h or not h:
            return fail(f"import header '{h}' must be 1-{MAX_HEADER} characters with no spaces")
    if not any(h.lower() == "email" for h in headers):
        return fail("Sequencer Import needs an Email header")

    # Sample rows: every cell filled, valid status, an address in the first column.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if any(not c for c in r):
            return fail(f"sample row for '{r[0]}' has a blank personalization cell")
        if "@" not in r[0]:
            return fail(f"sample row '{r[0]}' has no email in the first column")
        if r[-1].lower() != "valid":
            return fail(f"sample row '{r[0]}' is not email_status valid")

    # Launch checklist: every check marked done.
    checks = table_rows(section(text, "Launch Checklist"))
    if len(checks) < 6:
        return fail("Launch Checklist needs at least 6 checks")
    for r in checks:
        if len(r) < 3 or r[1].lower() not in {"done", "pass", "yes"}:
            return fail(f"launch check '{r[0]}' is not done")

    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: {send_ready:.0f} send-ready rows, funnel and capacity reconcile, {len(headers)} import headers valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
