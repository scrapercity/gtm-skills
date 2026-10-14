#!/usr/bin/env python3
"""Check a decision maker report against the decision-maker-finder output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import hashlib
import re
import sys
from pathlib import Path

REQUIRED = [
    "Account List",
    "Role Plan",
    "Waterfall Results",
    "Coverage by Role",
    "Validation Results",
    "Mobile Numbers",
    "Cost Estimate",
    "Sample Contacts",
    "Gaps and Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 35
STATUSES = ["valid", "catch_all", "unknown", "invalid", "disposable"]
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
# Also rejected: these hashed words (kept from the earlier check). Stored as SHA-256 hashes of lowercase words so the
# checker itself names no law or regulation (owner rule, 2026-10-13).
LEGAL_WORDS = {
    "9d8be820823bd8b1ceecaef063aea4c28da6f22fc8565985b17f05a49e04620c",
    "8d53e0154b79535cda4bda2c9ad960af9bf320002ce8d8365c7a0a56f4f897f9",
    "8b16477e3abe1de345a6e82f360db77b5e238983ad685cec9fef0d0bc009aed3",
    "fa193c8cc820b3b216502909af65a353a26b670c77833006d7dca1144bfb6950",
    "df679e72d63dc69befbe502d5e155258ca356fa1ac5ab7b47aab9c990f9586c1",
    "0c89db9e0a961c3939fb277192805c817fdf6b611e353477970af73ad9b54236",
    "9f6bbaad419acd37b0d06e775bb1d28533a0cefdef0c245d769af00a80eef975",
    "114ece8d992faac0dbffa9f93988ea242de90980817208ac293e8f4b576cf886",
    "503acf004b50b4f97beae09309f837a2ba47afacc83800fce9a1066813c7a97d",
}
# Deliverables carry no internal paths or tool ids (docs/SKILL_AUTHORING.md, Economy).
BANNED = re.compile(r"references/|SKILL\.md|query_lead_database|query_local_business_database|validate_emails|find_emails|find_mobiles|scrape_[a-z_]+|check_wallet|check_run_status|download_results", re.I)

# Deliverables name no skills: they describe the next action instead.
SKILL_NAMES = re.compile(
    r"\b(account-researcher|cold-email-list|crm-enricher|decision-maker-finder|ecommerce-by-techstack|"
    r"email-list-cleaner|icp-list-builder|local-business-list|mobile-appender|recruiting-sourcer|skip-tracer|"
    r"tam-builder|cold-calling|cold-email-copywriting|cold-email-strategy|domain-infrastructure|"
    r"email-deliverability|inbox-setup|multi-channel-outreach|outbound-unit-economics|reply-handling|"
    r"sending-platforms|signal-triggered-outbound|scrapercity-[a-z-]+|using-scrapercity-skills)\b")
# Sales-framework names are padding in a deliverable: keep the content, drop the acronym.
FRAMEWORK_NAMES = re.compile(r"\b(MEDDICC?|MEDDPICC|BANT|SPICED|GPCTBA|PQS|PVP|DAMA-DMBOK)\b")
DATE_CELL = re.compile(r"\d{4}-\d{2}-\d{2}|\b\d{1,2}/\d{1,2}\b|\bDay \d+\b|\bWeek \d+\b", re.I)


def headed_tables(block):
    """Each markdown table in the block as (header cells, body rows)."""
    out, cur = [], []
    for line in block.splitlines() + [""]:
        t = line.strip()
        if t.startswith("|"):
            if not re.match(r"^\|[\s:|-]+\|$", t):
                cur.append([c.strip() for c in t.strip("|").split("|")])
        elif cur:
            out.append((cur[0], cur[1:]))
            cur = []
    return out


def dated_steps_problem(block):
    """None when the block holds a steps table whose every row has an owner and a date."""
    for hdr, rows in headed_tables(block):
        cols = [c.lower() for c in hdr]
        if "owner" in cols and "date" in cols:
            oi, di = cols.index("owner"), cols.index("date")
            if not rows:
                return "the steps table is empty"
            for r in rows:
                if len(r) <= max(oi, di) or not r[oi].strip():
                    return f"step '{r[0]}' has no owner"
                if not DATE_CELL.search(r[di]):
                    return f"step '{r[0]}' has no date"
            return None
    return "needs a table with Step, Owner, Date and Done when columns"
FOUND_BY = {"lead_db", "website_finder", "email_finder", "apollo", "user_upload"}
NO_MOBILE = {"none found", "not requested"}


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
    for word in re.findall(r"[a-z][a-z-]+", text.lower()):
        if hashlib.sha256(word.encode()).hexdigest() in LEGAL_WORDS:
            return fail("deliverable carries legal commentary; remove it (owner rule)")
    legal = LEGAL.search(text)
    if legal:
        return fail(f"deliverable carries legal content ('{legal.group(0)}'); remove it (owner rule)")
    banned = BANNED.search(text)
    if banned:
        return fail("deliverable carries an internal path or a tool id: " + banned.group(0))
    skill = SKILL_NAMES.search(text)
    if skill:
        return fail("deliverable names a skill: " + skill.group(0) + " (describe the action instead)")
    framework = FRAMEWORK_NAMES.search(text)
    if framework:
        return fail("deliverable name-drops a sales framework: " + framework.group(0) + " (keep the content, drop the name)")
    steps_problem = dated_steps_problem(section(text, "Gaps and Next Steps"))
    if steps_problem:
        return fail("Gaps and Next Steps " + steps_problem)
    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    all_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if all_rows < MIN_TABLE_ROWS:
        return fail(f"only {all_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Account list funnel: each stage equals the previous minus dropped.
    prev = None
    for r in table_rows(section(text, "Account List")):
        if len(r) < 4:
            return fail("Account List rows need Stage, Accounts, Dropped, Reason")
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None:
            return fail(f"Account List stage '{r[0]}' has non-numeric values")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"Account List does not add up at '{r[0]}'")
        prev = rows
    searched = prev
    if not searched:
        return fail("Account List must end with a positive accounts-searched count")

    # Role plan: at least one slot, each with a role and a Website Finder title.
    plan = table_rows(section(text, "Role Plan"))
    if not plan or any(len(r) < 5 or not r[1] or not r[4] for r in plan):
        return fail("Role Plan needs a buying role and a Website Finder jobTitle on every slot")

    # Waterfall: found + not found = input, and found never exceeds input.
    wf = table_rows(section(text, "Waterfall Results"))
    if len(wf) < 4:
        return fail("Waterfall Results needs at least 4 steps")
    for r in wf:
        if len(r) < 5:
            return fail("Waterfall rows need Step, Tool, Input, Found, Not found")
        i, f, n = num(r[2]), num(r[3]), num(r[4])
        if None in (i, f, n):
            return fail(f"Waterfall step '{r[0]}' has non-numeric counts")
        if f > i:
            return fail(f"Waterfall step '{r[0]}' found more than its input")
        if abs(f + n - i) > 0.5:
            return fail(f"Waterfall step '{r[0]}': found + not found != input")

    # Coverage: filled + held + empty = accounts searched, for every slot.
    cov = table_rows(section(text, "Coverage by Role"))
    if not cov:
        return fail("Coverage by Role is empty")
    for r in cov:
        vals = [num(c) for c in r[1:5]]
        if len(r) < 6 or None in vals:
            return fail(f"Coverage row '{r[0]}' needs numeric searched, filled, held, empty")
        s, f, h, e = vals
        if abs(f + h + e - s) > 0.5:
            return fail(f"Coverage row '{r[0]}': filled + held + empty != searched")
        if abs(s - searched) > 0.5:
            return fail(f"Coverage row '{r[0]}' searched {s:.0f} accounts, Account List says {searched:.0f}")

    # Validation: every status present; each column sums to its Total row.
    vrows = table_rows(section(text, "Validation Results"))
    by = {r[0].strip().lower(): r for r in vrows}
    for st in STATUSES:
        if st not in by:
            return fail(f"Validation Results missing status '{st}'")
    if "total" not in by:
        return fail("Validation Results needs a Total row")
    for col in range(1, len(by["total"])):
        tot = num(by["total"][col])
        parts = [num(by[st][col]) if len(by[st]) > col else None for st in STATUSES]
        if tot is None or None in parts:
            return fail("Validation Results has a non-numeric cell")
        if abs(sum(parts) - tot) > 0.5:
            return fail(f"Validation Results column {col} does not sum to its Total")

    # Sample contacts: role, tool, valid status, and an E.164 mobile or an explicit none.
    sample = table_rows(section(text, "Sample Contacts"))
    if len(sample) < 3:
        return fail("Sample Contacts needs at least 3 rows")
    any_mobile = False
    for r in sample:
        if len(r) < 8:
            return fail("Sample Contacts rows need 8 columns")
        if not r[4]:
            return fail(f"sample contact {r[1]} {r[2]} has no buying_role")
        if r[5].lower() not in FOUND_BY:
            return fail(f"sample contact {r[1]} {r[2]} has found_by '{r[5]}', expected one of {sorted(FOUND_BY)}")
        if r[6].lower() != "valid":
            return fail(f"sample contact {r[1]} {r[2]} is not email_status valid")
        mob = r[7].strip()
        if mob.lower() in NO_MOBILE:
            continue
        if not re.fullmatch(r"\+\d{8,15}", mob):
            return fail(f"mobile '{mob}' is not E.164 (or 'none found' / 'not requested')")
        any_mobile = True

    # Mobiles carry a call block and a check against the one do-not-contact list.
    mob = {r[0].lower(): r[1] for r in table_rows(section(text, "Mobile Numbers")) if len(r) > 1}
    found = num(mob.get("numbers found", ""))
    if (found and found > 0) or any_mobile:
        if not mob.get("stated use", "").strip():
            return fail("mobiles delivered without a stated use (who calls, in which call block)")
        dnc = mob.get("do-not-contact check", "")
        if not re.search(r"do-not-contact|do not contact", dnc, re.I):
            return fail("mobiles delivered without a check against the do-not-contact list")

    cost = section(text, "Cost Estimate")
    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: {searched:.0f} accounts, {len(wf)} waterfall steps reconcile, coverage and validation add up")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
