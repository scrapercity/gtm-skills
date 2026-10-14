#!/usr/bin/env python3
"""Check a TAM report against the tam-builder output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import hashlib
import importlib.util
import re
import sys
from pathlib import Path

REQUIRED = [
    "Market Definition",
    "Source Counts",
    "Pull and Dedupe Funnel",
    "Source Mix",
    "Source Overlap",
    "Source Yield",
    "Coverage Estimate",
    "TAM SAM SOM",
    "Metro Breakdown",
    "Cost Estimate",
    "Output Schema",
    "Next Steps",
]
MIN_CHARS = 3000
MIN_TABLE_ROWS = 35
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
# Deliverables carry no internal paths or tool ids (docs/SKILL_AUTHORING.md, Economy).
BANNED = re.compile(r"references/|SKILL\.md|query_lead_database|query_local_business_database|validate_emails|find_emails|find_mobiles|scrape_[a-z_]+|check_wallet|check_run_status|download_results|playbook section", re.I)

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
SOURCES = {"lead_db", "local_db", "ecom_db", "apollo", "maps", "yelp", "angi", "store_leads",
           "techstack", "website_finder", "email_finder", "mobile_finder", "people_finder", "user_upload"}


def num(text):
    m = re.search(r"-?\d[\d,]*\.?\d*", (text or "").replace("$", ""))
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
        s = s.replace("\\|", "\x00")
        rows.append([c.strip().replace("\x00", "|") for c in s.strip("|").split("|")])
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
    legal = legal_hit(text)
    if legal:
        return fail(f"deliverable carries legal content: {legal}; remove it (owner rule)")
    banned = BANNED.search(text)
    if banned:
        return fail("deliverable carries an internal path or a tool id: " + banned.group(0))
    skill = SKILL_NAMES.search(text)
    if skill:
        return fail("deliverable names a skill: " + skill.group(0) + " (describe the action instead)")
    framework = FRAMEWORK_NAMES.search(text)
    if framework:
        return fail("deliverable name-drops a sales framework: " + framework.group(0) + " (keep the content, drop the name)")
    steps_problem = dated_steps_problem(section(text, "Next Steps"))
    if steps_problem:
        return fail("Next Steps " + steps_problem)
    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    total_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if total_rows < MIN_TABLE_ROWS:
        return fail(f"only {total_rows} table rows, need {MIN_TABLE_ROWS}")

    # Funnel adds up.
    funnel = table_rows(section(text, "Pull and Dedupe Funnel"))
    if len(funnel) < 4:
        return fail("funnel needs at least 4 stages")
    prev = None
    for r in funnel:
        if len(r) < 4 or not r[3]:
            return fail(f"funnel stage '{r[0]}' needs rows, dropped and a reason")
        rows, dropped = num(r[1]), num(r[2])
        if rows is None or dropped is None:
            return fail(f"funnel stage '{r[0]}' is not numeric")
        if prev is not None and abs(prev - dropped - rows) > 0.5:
            return fail(f"funnel does not add up at '{r[0]}'")
        prev = rows
    final_accounts = prev

    # Source mix uses the controlled vocabulary and sums to final accounts.
    mix = table_rows(section(text, "Source Mix"))
    mix_sum = 0.0
    for r in mix:
        if r[0].lower().startswith("total"):
            continue
        for part in r[0].strip("`").split("|"):
            if part.strip() not in SOURCES:
                return fail(f"source value '{part.strip()}' is not in the controlled vocabulary")
        mix_sum += num(r[1]) or 0
    if abs(mix_sum - final_accounts) > 0.5:
        return fail(f"Source Mix sums to {mix_sum:.0f}, final accounts are {final_accounts:.0f}")

    # Source overlap: found-in-N rows sum to final accounts, labels match N, imports reconcile.
    overlap = section(text, "Source Overlap")
    n_rows, imports = [], []
    for line_block in re.split(r"\n\s*\n", overlap):
        rows = table_rows(line_block)
        if not rows:
            continue
        header = line_block.strip().splitlines()[0].lower()
        if "found in" in header:
            n_rows = rows
        elif "outside source" in header:
            imports = rows
    if len(n_rows) < 3:
        return fail("Source Overlap needs a found-in-N table with at least 3 rows")
    n_sum = 0.0
    for r in n_rows:
        if len(r) < 4:
            return fail("found-in-N rows need N, Confidence, Accounts, Share")
        n, acc = num(r[0]), num(r[2])
        if n is None or acc is None or "%" not in r[3]:
            return fail(f"found-in-N row '{r[0]}' needs numeric N, accounts and a % share")
        expected = "high" if n >= 3 else "medium" if n == 2 else "low"
        if r[1].strip().lower() != expected:
            return fail(f"found in {r[0]} sources should be '{expected.title()}' confidence, not '{r[1]}'")
        if final_accounts and abs(acc / final_accounts * 100 - num(r[3])) > 0.11:
            return fail(f"share for found in {r[0]} does not match {acc:.0f} / {final_accounts:.0f}")
        n_sum += acc
    if abs(n_sum - final_accounts) > 0.5:
        return fail(f"found-in-N accounts sum to {n_sum:.0f}, final accounts are {final_accounts:.0f}")
    for r in imports:
        if len(r) < 6:
            return fail("outside source rows need rows, dedupe key, matched, new and held")
        vals = [num(r[1]), num(r[3]), num(r[4]), num(r[5])]
        if None in vals:
            return fail(f"outside source '{r[0]}' needs numeric rows, matched, new and held")
        if not r[2].strip():
            return fail(f"outside source '{r[0]}' needs a dedupe key")
        if abs(vals[0] - vals[1] - vals[2] - vals[3]) > 0.5:
            return fail(f"outside source '{r[0]}' does not reconcile: rows must equal matched + new + held")

    # Coverage estimate: observed, estimate and a percentage.
    cov = {r[0].lower(): r[1] for r in table_rows(section(text, "Coverage Estimate")) if len(r) > 1}
    for key in ("observed", "chapman estimate", "coverage"):
        if key not in cov or num(cov[key]) is None:
            return fail(f"Coverage Estimate needs a numeric '{key}' row")
    if "%" not in cov["coverage"]:
        return fail("Coverage row must be a percentage")
    if not re.search(r"caveat", section(text, "Coverage Estimate"), re.I):
        return fail("Coverage Estimate needs a caveat line")

    # TAM SAM SOM: accounts x ACV = dollars, and SOM <= SAM <= TAM.
    layers = {}
    for r in table_rows(section(text, "TAM SAM SOM")):
        if len(r) < 5:
            return fail("TAM SAM SOM rows need Layer, Definition, Accounts, ACV, Dollars")
        acc, acv, dol = num(r[2]), num(r[3]), num(r[4])
        if None in (acc, acv, dol) or "$" not in r[4]:
            return fail(f"TAM SAM SOM row '{r[0]}' needs numeric accounts, ACV and a $ dollars value")
        if abs(acc * acv - dol) > max(1.0, dol * 0.005):
            return fail(f"{r[0]}: {acc:.0f} x {acv:.0f} does not equal {dol:.0f}")
        layers[r[0].strip().upper()] = acc
    if not {"TAM", "SAM", "SOM"} <= set(layers):
        return fail("TAM SAM SOM needs TAM, SAM and SOM rows")
    if not layers["SOM"] <= layers["SAM"] <= layers["TAM"]:
        return fail("expected SOM <= SAM <= TAM in accounts")

    # Source yield: unique accounts never exceed accounts contributed; every row has a decision.
    for r in table_rows(section(text, "Source Yield")):
        if len(r) < 6:
            return fail("Source Yield rows need Source, Contributed, Unique, Cost, Cost per unique, Next refresh")
        contributed, unique = num(r[1]), num(r[2])
        if contributed is None or unique is None:
            return fail(f"Source Yield '{r[0]}' needs numeric contributed and unique accounts")
        if unique > contributed:
            return fail(f"Source Yield '{r[0]}' has more unique accounts than it contributed")
        if not r[5].strip():
            return fail(f"Source Yield '{r[0]}' needs a next-refresh decision")

    # Account tiers (optional): tiers sum to SAM, capacity and a backtest above 1.0x (better than chance).
    tiers_block = section(text, "Account Tiers")
    if tiers_block.strip():
        tiers = table_rows(tiers_block)
        if len(tiers) < 3:
            return fail("Account Tiers needs at least 3 rows")
        tsum = 0.0
        for r in tiers:
            if len(r) < 5 or num(r[2]) is None:
                return fail(f"Account Tiers row '{r[0]}' needs Rule, numeric Accounts, Motion, Contacts")
            tsum += num(r[2])
        if abs(tsum - layers["SAM"]) > 0.5:
            return fail(f"Account Tiers sum to {tsum:.0f}, SAM is {layers['SAM']:.0f}")
        if re.search(r"spend ceiling", tiers_block, re.I) and not re.search(r"^Deal inputs \(from you\):\s*\S", tiers_block, re.M):
            return fail("spend ceilings need the user's ACV, margin and win rates on a 'Deal inputs (from you):' line; otherwise drop the column")
        if not re.search(r"^Capacity:\s*\S", tiers_block, re.M):
            return fail("Account Tiers needs a 'Capacity:' line")
        bt = re.search(r"^Backtest:[^\n]*?(\d+(?:\.\d+)?)x", tiers_block, re.M)
        if not bt:
            return fail("Account Tiers needs a 'Backtest:' line ending in a concentration like 3.5x")
        if float(bt.group(1)) <= 1.0:
            return fail(f"Backtest concentration {bt.group(1)}x is no better than chance (1.0x); re-weight the score")

    if not re.search(r"total[^\n]*\$\d", section(text, "Cost Estimate"), re.I):
        return fail("Cost Estimate needs a total with a $ figure")

    print(f"PASS - {path.name}: funnel adds up to {final_accounts:.0f} accounts, source mix matches, {len(n_rows)} overlap tiers and {len(imports)} imports reconcile, TAM/SAM/SOM consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
