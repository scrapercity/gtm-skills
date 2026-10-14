#!/usr/bin/env python3
"""Check an ICP list report against the icp-list-builder output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.

Two report modes, set by the Status line above the first heading:
  Status: Ran ...   the counts, pull and validation ran; funnel and buckets are live numbers
  Status: Plan ...  no call could run yet; estimates are sourced ranges or ceilings
"""
import hashlib
import importlib.util
import re
import sys
from pathlib import Path

BOTH = ["Answer", "ICP Definition", "Filters Used", "Count Check", "Cost Estimate", "Output Schema", "Next Steps"]
RUN_ONLY = ["Pull Funnel", "Validation Results"]
MIN_CHARS = 2500
MIN_TABLE_ROWS = 25
BUCKETS = ["valid", "catch_all", "unknown", "invalid", "disposable"]
# Deliverables carry no legal commentary. Stored as SHA-256 hashes of lowercase words so the
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
# Deliverables carry no internal paths, tool ids or skill names (docs/SKILL_AUTHORING.md, Economy).
BANNED = re.compile(r"references/|SKILL\.md|check-output|query_lead_database|query_local_business_database|validate_emails|find_emails|find_mobiles|find_people|scrape_[a-z_]+|check_wallet|check_run_status|download_results|list_runs", re.I)
SKILL_NAMES = re.compile(
    r"\b(account-researcher|cold-email-list|crm-enricher|decision-maker-finder|ecommerce-by-techstack|"
    r"email-list-cleaner|icp-list-builder|local-business-list|mobile-appender|recruiting-sourcer|skip-tracer|"
    r"tam-builder|cold-calling|cold-email-copywriting|cold-email-strategy|domain-infrastructure|"
    r"email-deliverability|inbox-setup|multi-channel-outreach|outbound-unit-economics|reply-handling|"
    r"sending-platforms|signal-triggered-outbound|scrapercity-[a-z-]+|using-scrapercity-skills)\b")
# Sales-framework names are padding in a deliverable: keep the content, drop the acronym.
FRAMEWORK_NAMES = re.compile(r"\b(MEDDICC?|MEDDPICC|BANT|SPICED|GPCTBA|PQS|PVP|DAMA-DMBOK)\b")
# A value left for the reader to pick is a step nobody can run. State the value and its source.
VAGUE = re.compile(r"\byou set\b|\bset your own\b|\byou choose\b|\bof your choosing\b|\bas you see fit\b|\bwindow you set\b", re.I)
# One status line carries the "nothing ran" message; repeating it is padding.
DISCLAIMER = re.compile(r"\bnot (been )?run\b|\bnothing (has )?run\b|\bno [a-z ]{0,30}calls? (has|have) run\b|\bbefore any [a-z ]{0,30}ran\b|\bwas not run\b", re.I)
# A named outside source needs its date or its site on the line that first names it.
NAMED = re.compile(r"\b(Berman|Gartner|Pew|Instantly|Smartlead|Eypasch|ZeroBounce|SUSB|Census|Bureau of Labor)\b")
DATED = re.compile(r"\b(19|20)\d{2}\b|\b[a-z0-9-]+\.(com|org|gov|ai|net|io)\b", re.I)
DATE_CELL = re.compile(r"\d{4}-\d{2}-\d{2}|\b\d{1,2}/\d{1,2}\b|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2}\b|\bDay \d+\b|\bWeek \d+\b", re.I)
PLACEHOLDER_CELL = re.compile(r"^(not supplied|lookup|ask|n/?a|none supplied|tbd|-)$", re.I)


def legal_hit(text):
    """First legal term, using the repo's scripts/validate-skills.py list when the checker runs in the repo."""
    for parent in Path(__file__).resolve().parents:
        validator = parent / "scripts" / "validate-skills.py"
        if validator.is_file():
            spec = importlib.util.spec_from_file_location("validate_skills", validator)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for line in text.splitlines():
                hits = module.legal_hits(line, "")
                if hits:
                    return hits[0]
            return None
    return None


def num(text):
    m = re.search(r"-?\d[\d,]*\.?\d*", text or "")
    return float(m.group(0).replace(",", "")) if m else None


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def tables(block):
    """Each markdown table in the block as (header, rows)."""
    out, cur = [], []
    for line in block.splitlines() + [""]:
        s = line.strip()
        if s.startswith("|"):
            if not re.match(r"^\|[\s:|-]+\|$", s):
                cur.append([c.strip() for c in s.strip("|").split("|")])
        elif cur:
            out.append((cur[0], cur[1:]))
            cur = []
    return out


def table_rows(block):
    return [r for _, rows in tables(block) for r in rows]


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

    hit = re.search(r"\[(fill|todo|tbd)[^\]]*\]", text, re.I)
    if hit:
        return fail("placeholder left in: " + hit.group(0))
    angle = re.search(r"<[A-Za-z][^>\n]{0,60}>", text)
    if angle:
        return fail("angle-bracket placeholder left in: " + angle.group(0))

    head = text.split("\n## ", 1)[0]
    status = re.search(r"^Status:\s*(Ran|Plan)\b", head, re.M | re.I)
    if not status:
        return fail("put one 'Status: Ran ...' or 'Status: Plan ...' line above the first section")
    plan = status.group(1).lower() == "plan"

    headings = re.findall(r"^## (.+?)\s*$", text, re.M)
    lower = [h.lower() for h in headings]
    required = BOTH + ([] if plan else RUN_ONLY)
    missing = [h for h in required if h.lower() not in lower]
    if missing:
        return fail("missing sections: " + ", ".join(missing))
    if lower[0] != "answer":
        return fail("the first section must be '## Answer': the answers come before the detail")
    if "sample rows" in lower:
        return fail("drop Sample Rows: invented people add nothing the Output Schema example column does not show")

    for word in re.findall(r"[a-z][a-z-]+", text.lower()):
        if hashlib.sha256(word.encode()).hexdigest() in LEGAL_WORDS:
            return fail("deliverable carries legal commentary; remove it (owner rule)")
    legal = legal_hit(text)
    if legal:
        return fail(f"deliverable carries legal content: {legal}; remove it (owner rule)")
    banned = BANNED.search(text)
    if banned:
        return fail("deliverable carries an internal path or a tool id: " + banned.group(0) + " (name the product or the action)")
    skill = SKILL_NAMES.search(text)
    if skill:
        return fail("deliverable names a skill: " + skill.group(0) + " (describe the action instead)")
    framework = FRAMEWORK_NAMES.search(text)
    if framework:
        return fail("deliverable name-drops a sales framework: " + framework.group(0) + " (keep the content, drop the name)")
    vague = VAGUE.search(text)
    if vague:
        return fail(f"value left to the reader ('{vague.group(0)}'): state the value and its source, or ask for it in Next Steps")
    disclaimers = DISCLAIMER.findall(text)
    if len(disclaimers) > 1:
        return fail(f"the 'nothing ran' message appears {len(disclaimers)} times; keep it once, in the Status line")
    cited = set()
    for line in text.splitlines():
        names = {m.group(1) for m in NAMED.finditer(line)} - cited
        if names and not DATED.search(line):
            return fail("first mention of a named source without its date or site on the same line: " + line.strip()[:90])
        cited |= names
    if re.search(r"spend ceiling", text, re.I) and not re.search(r"^Deal inputs \(from you\):", text, re.M):
        return fail("spend ceilings need the user's deal size, margin and win rates on a 'Deal inputs (from you):' line; otherwise leave them out")
    if plan and re.search(r"\b[\w.-]+\.csv\b", text):
        return fail("a plan names no file names; describe the send file and hold file instead")

    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    all_rows = sum(len(table_rows(section(text, h))) for h in headings)
    if all_rows < MIN_TABLE_ROWS:
        return fail(f"only {all_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Each fact once: no table row repeats another section's row of figures.
    seen = {}
    for h in headings:
        for r in table_rows(section(text, h)):
            cells = re.sub(r"\d{4}-\d{2}-\d{2}", "", " ".join(r[1:]))
            nums = tuple(n for n in (float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", cells)) if n >= 100)
            if len(nums) >= 2:
                if nums in seen and seen[nums] != h:
                    return fail(f"'{h}' repeats a row of figures already in '{seen[nums]}' ({r[0]}); state each figure once")
                seen.setdefault(nums, h)

    # Answer: one row per question, ranges or sourced figures in a plan.
    answer = table_rows(section(text, "Answer"))
    if len(answer) < 3:
        return fail("Answer needs a table with at least 3 rows, one per question the user asked")
    if plan and not re.search(r"\d[\d,]*\s?(-|to)\s?\$?\d[\d,]*", section(text, "Answer")):
        return fail("a plan gives estimated counts as sourced ranges or ceilings in Answer, not single invented figures")

    # ICP evidence: a statement, then either 3+ won accounts or one 'Evidence:' line asking for them.
    icp = section(text, "ICP Definition")
    if not re.search(r"^ICP statement:\s*\S.{20,}$", icp, re.M):
        return fail("ICP Definition needs an 'ICP statement:' line")
    evidence = table_rows(icp)
    won = [r for r in evidence if len(r) > 2 and r[2].strip().lower() == "won"]
    if len(won) < 3 and not re.search(r"^Evidence:\s*\S", icp, re.M):
        return fail("ICP Definition needs 3+ evidence accounts with outcome 'won', or one 'Evidence:' line asking for them")
    for h in headings:
        for r in table_rows(section(text, h)):
            for c in r[1:]:
                if PLACEHOLDER_CELL.match(c.strip()):
                    return fail(f"'{h}' has a placeholder cell ('{c.strip()}' in row '{r[0]}'); cut the row or fill it")

    counts = [num(r[1]) for r in table_rows(section(text, "Count Check")) if len(r) > 1]
    if not any(c is not None and c > 0 for c in counts):
        return fail("Count Check has no numeric count or benchmark")

    # Account tiers, when present: the tier rows add up to the Total row.
    tiers = section(text, "Account Tiers")
    if tiers:
        trs = table_rows(tiers)
        total_row = next((r for r in trs if r[0].lower().startswith("total")), None)
        if not total_row:
            return fail("Account Tiers needs a Total row")
        hdr = tables(tiers)[0][0]
        col = next((i for i, c in enumerate(hdr) if c.lower().startswith("accounts")), None)
        if col is None:
            return fail("Account Tiers needs an Accounts column")
        parts = [num(r[col]) for r in trs if r is not total_row and len(r) > col]
        if any(p is None for p in parts) or abs(sum(parts) - (num(total_row[col]) or -1)) > 0.5:
            return fail("Account Tiers rows do not add up to the Total row")

    if not plan:
        funnel = table_rows(section(text, "Pull Funnel"))
        if len(funnel) < 5:
            return fail("Pull Funnel needs at least 5 stages")
        prev = None
        for r in funnel:
            if len(r) < 4:
                return fail("Pull Funnel rows need Stage, Rows, Dropped, Reason")
            rows, dropped = num(r[1]), num(r[2])
            if rows is None or dropped is None:
                return fail(f"Pull Funnel stage '{r[0]}' has non-numeric rows or dropped")
            if not r[3]:
                return fail(f"Pull Funnel stage '{r[0]}' has no reason")
            if prev is not None:
                if rows > prev:
                    return fail(f"Pull Funnel grows at '{r[0]}'")
                if abs(prev - dropped - rows) > 0.5:
                    return fail(f"Pull Funnel does not add up at '{r[0]}': {prev:.0f} - {dropped:.0f} != {rows:.0f}")
            prev = rows
        vblock = section(text, "Validation Results")
        found = {r[0].strip().lower(): num(r[1]) for r in table_rows(vblock) if len(r) > 1}
        for b in BUCKETS:
            if b not in found or found[b] is None:
                return fail(f"Validation Results missing bucket '{b}'")
        total = next((v for k, v in found.items() if k.startswith("total")), None)
        if total is None:
            return fail("Validation Results needs a Total validated row")
        if abs(sum(found[b] for b in BUCKETS) - total) > 0.5:
            return fail("validation buckets do not sum to Total validated")
        fit = re.search(r"^Fit sample[^\n]*$", vblock, re.M | re.I)
        if not fit:
            return fail("Validation Results needs a 'Fit sample' line with counts per dimension")
        pairs = [(int(a), int(b)) for a, b in re.findall(r"(\d+) of (\d+)", fit.group(0))]
        if len(pairs) < 3:
            return fail("Fit sample needs at least 3 dimensions written as 'N of M'")
        for a, b in pairs:
            if b == 0 or a > b:
                return fail(f"Fit sample dimension '{a} of {b}' is not a valid count")

    cost = section(text, "Cost Estimate")
    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a total with a $ figure")
    if not re.search(r"^Prices:[^\n]*checked[^\n]*\d{4}-\d{2}-\d{2}", cost, re.M | re.I):
        return fail("Cost Estimate needs a 'Prices: ... checked YYYY-MM-DD' line naming where the prices come from")

    # Next Steps: every step has an owner and a date.
    nt = tables(section(text, "Next Steps"))
    if not nt:
        return fail("Next Steps needs a table with Step, Owner, Date and Done when columns")
    hdr, rows = nt[0]
    cols = [c.lower() for c in hdr]
    if "owner" not in cols or "date" not in cols:
        return fail("Next Steps table needs Owner and Date columns")
    oi, di = cols.index("owner"), cols.index("date")
    if len(rows) < 3:
        return fail("Next Steps needs at least 3 steps")
    for r in rows:
        if len(r) <= max(oi, di) or not r[oi].strip():
            return fail(f"Next Steps row '{r[0]}' has no owner")
        if not DATE_CELL.search(r[di]):
            return fail(f"Next Steps row '{r[0]}' has no date")

    mode = "plan" if plan else "run"
    print(f"PASS - {path.name}: {mode} report, answer first, {len(rows)} dated steps with owners, cost and prices line present")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
