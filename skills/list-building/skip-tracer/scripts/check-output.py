#!/usr/bin/env python3
"""Check a skip trace report against the skip-tracer output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Purpose and Channels",
    "Input Profile",
    "Identifier Plan",
    "Cost Estimate",
    "Match Bands",
    "Results Funnel",
    "Contact Results",
    "Sample Rows",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 30
BANDS = ["confirmed", "probable", "weak", "no_match"]
# Evidence tokens and the band each combination earns (SKILL.md workflow step 5).
EVIDENCE_BAND = {
    "name+address": "confirmed", "name+contact": "confirmed", "name+address+contact": "confirmed",
    "owner_record": "confirmed",
    "name+city": "probable", "surname+address": "probable", "address_only": "probable",
    "name_only": "weak", "surname+city": "weak", "tie": "weak", "entity": "weak",
    "none": "no_match", "deceased": "no_match",
}
STATUSES = {"callable", "suppressed", "estate_mail", "mail_only"}
E164 = re.compile(r"^\+[1-9]\d{7,14}$")
PRICES = {"find_people": 0.0199, "distress": 0.05}
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


def legal_hit(text):
    m = LEGAL_ACRONYMS.search(text) or LEGAL_PHRASES.search(text)
    return m.group(0) if m else None


# Deliverables name products, never tool ids or internal paths (SKILL.md Output Format).
BANNED = re.compile(r"references/|SKILL\.md|query_lead_database|query_local_business_database|validate_emails|find_emails|find_mobiles|find_people|scrape_[a-z_]+|check_wallet|check_run_status|download_results", re.I)


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
    angle = re.search(r"<[A-Za-z][^>\n]{0,60}>", text)
    if angle:
        return fail("angle-bracket placeholder left in: " + angle.group(0))
    legal = legal_hit(text)
    if legal:
        return fail("deliverable carries legal content: " + legal)
    banned = BANNED.search(text)
    if banned:
        return fail("deliverable carries an internal path or a tool id: " + banned.group(0))
    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    total_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if total_rows < MIN_TABLE_ROWS:
        return fail(f"only {total_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Purpose, channels and the suppression list stated.
    purpose = section(text, "Purpose and Channels").lower()
    for word in ("purpose", "channels", "suppression"):
        if word not in purpose:
            return fail(f"Purpose and Channels must state the {word}")

    # Cost lines priced at catalog rates.
    for r in table_rows(section(text, "Cost Estimate")):
        if len(r) < 4 or r[0].lower().startswith("total"):
            continue
        line, units, cost = r[0].lower(), num(r[1]), num(r[3].replace("$", ""))
        if units is None or cost is None:
            continue
        if "people finder" in line or "find_people" in line:
            price = PRICES["find_people"]
        elif "property lookup" in line or "property_lookup" in line:
            price = 0.25 if "owner" in line else 0.15
        elif "distress" in line:
            price = PRICES["distress"]
        else:
            continue
        if abs(units * price - cost) > 0.01:
            return fail(f"cost line '{r[0]}': {units:.0f} x ${price} is not ${cost:.2f}")
    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a Total row with a $ figure")

    # Bands present and summing to total searched.
    counts = {r[0].strip().lower(): num(r[2]) for r in table_rows(section(text, "Match Bands")) if len(r) > 2}
    for name in BANDS:
        if counts.get(name) is None:
            return fail(f"Match Bands missing band '{name}'")
    total = next((v for k, v in counts.items() if k.startswith("total")), None)
    if total is None or abs(sum(counts[b] for b in BANDS) - total) > 0.5:
        return fail("Match Bands do not sum to Total searched")

    # QA sample: confirmed rows checked against the owner of record, reported as counts.
    qa = re.search(r"QA sample[^\n]*", text, re.I)
    checks = re.findall(r"(\d+) of (\d+)", qa.group(0)) if qa else []
    if len(checks) < 2:
        return fail("add a QA sample line: confirmed rows checked against the owner of record, as 'n of m'")
    for n, m in checks:
        if int(m) == 0 or int(n) > int(m):
            return fail(f"QA sample check '{n} of {m}' is not a valid count")

    # Funnel adds up and never grows.
    funnel = table_rows(section(text, "Results Funnel"))
    if len(funnel) < 3:
        return fail("Results Funnel needs at least 3 stages")
    prev = None
    for r in funnel:
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None or len(r) < 4 or not r[3]:
            return fail(f"Results Funnel stage '{r[0]}' needs rows, dropped and a reason")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"Results Funnel does not add up at '{r[0]}'")
        prev = rows

    # Sample rows: band matches evidence, phones E.164, only confirmed or probable rows callable.
    sample = table_rows(section(text, "Sample Rows"))
    if len(sample) < 3:
        return fail("Sample Rows needs at least 3 rows")
    for r in sample:
        if len(r) < 7:
            return fail("Sample Rows need 7 columns")
        evidence, band = r[2].strip().lower(), r[3].strip().lower()
        if evidence not in EVIDENCE_BAND:
            return fail(f"sample {r[0]}: evidence '{r[2]}' not in the vocabulary")
        if EVIDENCE_BAND[evidence] != band:
            return fail(f"sample {r[0]}: evidence '{evidence}' earns {EVIDENCE_BAND[evidence]}, not '{r[3]}'")
        if r[5] and not E164.match(r[5].strip()):
            return fail(f"sample {r[0]}: phone '{r[5]}' is not E.164")
        status = r[6].strip()
        if status not in STATUSES:
            return fail(f"sample {r[0]}: status '{status}' not in the vocabulary")
        if status == "callable" and band not in ("confirmed", "probable"):
            return fail(f"sample {r[0]} is callable but is {band}")

    print(f"PASS - {path.name}: cost lines at catalog prices, {total:.0f} rows banded, {len(sample)} sample rows banded by evidence")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
