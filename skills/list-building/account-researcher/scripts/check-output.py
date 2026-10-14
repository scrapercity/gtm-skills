#!/usr/bin/env python3
"""Check an account brief against the account-researcher output contract.

Usage: check-output.py path/to/brief.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import hashlib
import re
import sys
from pathlib import Path

REQUIRED = [
    "Account Snapshot",
    "Why Now",
    "Tech Stack",
    "Key People",
    "Hypothesis and Talking Points",
    "Contact Plan",
    "Sources",
    "Cost Estimate",
    "Open Questions and Next Steps",
]
MIN_CHARS = 2500
MIN_TABLE_ROWS = 25
STATUSES = {"valid", "catch_all", "unknown", "invalid", "disposable", "none"}
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
BANNED = re.compile(r"references/|SKILL\.md|query_lead_database|validate_emails|find_emails|find_mobiles|scrape_[a-z_]+|check_wallet|check_run_status|download_results", re.I)

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
FOUND_BY = {"lead_db", "website_finder", "email_finder", "user_upload", "apollo"}
TECH_STATUS = {"confirmed", "likely", "not detected"}
SRC = re.compile(r"\bS(\d+)\b")
DATE = re.compile(r"\d{4}-\d{2}(-\d{2})?")


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
        print("usage: check-output.py path/to/brief.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/brief.md (file not found)")
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
    steps_problem = dated_steps_problem(section(text, "Open Questions and Next Steps"))
    if steps_problem:
        return fail("Open Questions and Next Steps " + steps_problem)
    if len(text) < MIN_CHARS:
        return fail(f"brief too short ({len(text)} chars, need {MIN_CHARS})")
    all_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if all_rows < MIN_TABLE_ROWS:
        return fail(f"only {all_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Sources: S-numbered, each with a URL and a date checked.
    sources = {}
    for r in table_rows(section(text, "Sources")):
        m = re.fullmatch(r"S(\d+)", r[0]) if r else None
        if not m or len(r) < 4:
            return fail("Sources rows need ID (S1, S2...), Source, URL, Date checked")
        if not re.search(r"https?://", r[2]):
            return fail(f"source {r[0]} has no URL")
        if not DATE.search(r[3]):
            return fail(f"source {r[0]} has no date checked")
        sources[m.group(1)] = r
    if len(sources) < 3:
        return fail("Sources needs at least 3 entries")

    def cited(cell, where):
        ids = SRC.findall(cell)
        if not ids:
            return f"{where} cites no source ID"
        bad = [i for i in ids if i not in sources]
        if bad:
            return f"{where} cites S{bad[0]}, which is not in Sources"
        return None

    # Why Now: each signal is dated, typed with an Elias category, and cited.
    why = table_rows(section(text, "Why Now"))
    if len(why) < 2:
        return fail("Why Now needs at least 2 dated signals")
    for r in why:
        if len(r) < 5 or not DATE.search(r[1]):
            return fail(f"Why Now signal '{r[0]}' has no date")
        if not re.search(r"transition|bad experience|awareness", r[2], re.I):
            return fail(f"Why Now signal '{r[0]}' needs an Elias category (transition, bad experience, awareness)")
        err = cited(r[4], f"Why Now signal '{r[0]}'")
        if err:
            return fail(err)

    # Tech stack: status vocabulary, a yes/no pitch flag, a cited source.
    stack = table_rows(section(text, "Tech Stack"))
    if not stack:
        return fail("Tech Stack is empty")
    paid = False
    for r in stack:
        if len(r) < 5:
            return fail("Tech Stack rows need Technology, Status, Evidence, Changes pitch?, Source")
        if r[1].lower() not in TECH_STATUS:
            return fail(f"Tech Stack '{r[0]}' status must be confirmed, likely or not detected")
        if r[3].lower() not in {"yes", "no"}:
            return fail(f"Tech Stack '{r[0]}' needs yes or no under Changes pitch?")
        ev = r[2].lower()
        if "tech stack search" in ev and not re.search(r"\bnot\b[^.]*tech stack search", ev):
            paid = True
            if r[3].lower() != "yes":
                return fail(f"Tech Stack Search was paid for '{r[0]}', which does not change the pitch")
        err = cited(r[4], f"Tech Stack '{r[0]}'")
        if err:
            return fail(err)
    cost = section(text, "Cost Estimate")
    if paid and "$4.99" not in cost:
        return fail("Tech Stack Search used but Cost Estimate has no $4.99 per technology line")

    # Key people: 2+, each with a role, a known status and a known tool.
    people = table_rows(section(text, "Key People"))
    if len(people) < 2:
        return fail("Key People needs at least 2 people")
    for r in people:
        if len(r) < 7 or not r[2]:
            return fail(f"person '{r[0]}' has no buying role")
        if r[4].lower() not in STATUSES:
            return fail(f"person '{r[0]}' has email_status '{r[4]}'")
        if r[5].lower() not in FOUND_BY:
            return fail(f"person '{r[0]}' has found_by '{r[5]}'")

    # Talking points: every one cites a listed source.
    tps = table_rows(section(text, "Hypothesis and Talking Points"))
    if len(tps) < 3:
        return fail("need at least 3 talking points")
    for r in tps:
        err = cited(" ".join(r[1:]), f"talking point {r[0]}")
        if err:
            return fail(err)

    # Contact plan: a warm path check, and never two people on the same day.
    if not re.search(r"warm path", section(text, "Contact Plan"), re.I):
        return fail("Contact Plan needs a 'Warm path check' line (introduction available or not)")
    days = [r[3].strip().lower() for r in table_rows(section(text, "Contact Plan")) if len(r) > 3]
    if not days:
        return fail("Contact Plan is empty")
    if len(days) != len(set(days)):
        return fail("Contact Plan puts two touches at the account on the same day")

    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: {len(sources)} sources, {len(tps)} cited talking points, {len(people)} people, contact days unique")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
