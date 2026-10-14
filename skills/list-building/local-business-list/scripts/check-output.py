#!/usr/bin/env python3
"""Check a local business list report against the local-business-list output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.

Two report modes, named on a "Status:" line near the top:
  Plan      - nothing paid has run; measured free counts only, a ceiling, decisions, a dated run schedule.
  Delivered - the run finished; coverage, funnel, validation, segments, cost and checks reconcile.
"""
import re
import sys
from pathlib import Path

REQUIRED = {
    "plan": ["Short Answer", "Decisions", "Search Definition", "Coverage", "Segments", "Cost",
             "Checks", "Run Schedule", "Output Columns"],
    "delivered": ["Short Answer", "Search Definition", "Coverage", "Funnel", "Validation Results",
                  "Segments", "Cost", "Checks", "Output Columns", "Next Steps"],
}
# Sections that restate other sections, self-grade, or carry internal detail.
FORBIDDEN_HEADINGS = re.compile(
    r"count check|source results|sample rows|calls i will make|quality check|framework|complian|"
    r"skills? used|appendix|output schema|geography split|cleaning funnel|methodology", re.I)
PLAN_FORBIDDEN = ["Funnel", "Validation Results"]
STATUSES = ["valid", "catch_all", "unknown", "invalid", "disposable"]
E164 = re.compile(r"\+\d{8,15}")
ISO = re.compile(r"\b20\d\d-\d\d-\d\d\b")
# Deliverables carry no legal content. Same terms as scripts/validate-skills.py
# --check-legal; the bracketed letters keep this file from matching its own terms.
LEGAL = re.compile(
    r"\b(?:CAN[- ]?SP[A]M|T[C]PA|T[S]R|C[A]SL|G[D]PR|C[C]PA|C[P]RA|P[E]CR|F[C]RA|F[T]C|F[C]C|C[R]TC|I[C]O|D[N]C)\b"
    r"|\b(?:47|16)\s*C\.?F\.?R\b|U\.S\.C|Do[- ]Not[- ]Call|Att[o]rneys? Gen[e]ral|leg[a]l advi[c]e|\bnot leg[a]l\b"
    r"|\bcompliance\b|\bconsent\b|lawful bas[i]s|\blawful\b"
    r"|\b(?:consult|ask|check with|speak (?:to|with)|talk (?:to|with))\s+(?:a|an|your)\s+(?:\w+\s+)?(?:lawy[e]r|attorn[e]y|couns[e]l)",
    re.I,
)
# The reader gets product names and the inputs a person chooses: no tool ids, API parameters,
# endpoints, request bodies, file paths or names of other builds.
INTERNAL = re.compile(
    r"references/|SKILL\.md|\.py\b|```|/api/|query_local_business_database|query_lead_database|validate_emails|"
    r"find_emails|find_mobiles|scrape_[a-z_]+|check_wallet|check_run_status|download_results|notCategory|"
    r"pagination\.total|next_after|autoValidateEmails|searchStringsArray|maxCrawledPlacesPerSearch|locationQuery|"
    r"\bhas(?:Website|Email|Contact)\b|excludeDelivered|searched[_ ]as|\bthe skill\b|\bthis skill\b|build next|"
    r"\b(?:account-researcher|cold-email-list|crm-enricher|decision-maker-finder|ecommerce-by-techstack|"
    r"email-list-cleaner|icp-list-builder|local-business-list|mobile-appender|recruiting-sourcer|skip-tracer|"
    r"tam-builder|cold-calling|cold-email-copywriting|cold-email-strategy|domain-infrastructure|"
    r"email-deliverability|inbox-setup|multi-channel-outreach|outbound-unit-economics|reply-handling|"
    r"sending-platforms|signal-triggered-outbound|scrapercity-[a-z-]+|using-scrapercity-skills)\b",
    re.I,
)
# One status line covers what has and has not run; repeating it is padding.
DISCLAIMER = re.compile(r"nothing (?:paid )?(?:has )?(?:run|ran)|not run yet|\bassumed\b|\bassumptions?\b|\bprojected\b|\bprojection\b", re.I)
# A number used as a stop or pass line names its source or says it is the user's setting.
SOURCED = re.compile(r"Berman|Google|Yahoo|Microsoft|Instantly|ZeroBounce|CMS|NPI|Census|measured|\byour\b|you set|setting|'s line", re.I)


def num(text):
    m = re.search(r"-?\d[\d,]*\.?\d*", text or "")
    return float(m.group(0).replace(",", "")) if m else None


def money(text):
    m = re.search(r"\$\s?(\d[\d,]*\.?\d*)", text or "")
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


def check_cost(text):
    """Units x unit price = cost on every priced row; a total or ceiling row carries a $ figure."""
    rows = table_rows(section(text, "Cost"))
    if len(rows) < 3:
        return "Cost needs a row per paid step and a total or ceiling row"
    for r in rows:
        if len(r) < 4:
            return f"Cost row '{r[0]}' needs Item, Units, Unit price and Cost"
        units, price, cost = num(r[1]), money(r[2]), money(r[3])
        if units is not None and price is not None and cost is not None and price < 1:
            if abs(units * price - cost) > 0.02:
                return f"Cost row '{r[0]}': {units:g} x ${price} is not {r[3]}"
    if not re.search(r"(total|ceiling)[^\n]*\$\d", section(text, "Cost"), re.I):
        return "Cost needs a total or ceiling row with a $ figure"
    return None


def check_columns(text, mode):
    cols = {r[0].strip("` ").lower(): r for r in table_rows(section(text, "Output Columns")) if len(r) >= 3}
    if len(cols) < 8:
        return "Output Columns needs 8+ rows of Column, Example, Rule"
    if "email" not in cols or "@" not in cols["email"][1]:
        return "Output Columns needs an email row whose example is an address"
    if "phone" not in cols or not E164.fullmatch(cols["phone"][1].strip("` ")):
        return "Output Columns needs a phone row whose example is E.164"
    if "email_status" not in cols or cols["email_status"][1].strip("` ").lower() != "valid":
        return "Output Columns needs an email_status row whose example is valid"
    return None


def check_thresholds(text):
    for r in table_rows(section(text, "Checks")):
        line = " | ".join(r)
        if re.search(r"\d\s*%", line) and not SOURCED.search(line):
            return f"Checks row '{r[0]}' has a % line with no source and no 'your setting'"
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"bounce", line, re.I) and re.search(r"\d\s*%", line) and not SOURCED.search(line):
            return f"line {i}: a bounce line with a % needs its source or 'your setting'"
    return None


def check_delivered(text):
    cov = table_rows(section(text, "Coverage"))
    total = next((r for r in cov if r[0].lower().startswith("total")), None)
    subs = [r for r in cov if r is not total]
    if total is None or len(subs) < 2:
        return "Coverage needs 2+ rows (gap sub-areas plus one row for the rest) and a Total row"
    for col, label in ((1, "database (A)"), (2, "with website and email (C)")):
        vals = [num(r[col]) if len(r) > col else None for r in subs]
        if None in vals or num(total[col]) is None:
            return f"Coverage column {label} has a non-numeric cell"
        if abs(sum(vals) - num(total[col])) > 0.5:
            return f"Coverage column {label} does not sum to its Total"
    for r in subs:
        if num(r[2]) > num(r[1]):
            return f"Coverage row '{r[0]}' has more website-and-email rows than businesses"

    funnel = table_rows(section(text, "Funnel"))
    if len(funnel) < 6:
        return "Funnel needs at least 6 stages"
    prev = None
    for r in funnel:
        if len(r) < 4 or not r[3]:
            return f"Funnel stage '{r[0]}' needs Rows, Change and a Reason"
        rows, change = num(r[1]), num(r[2])
        if rows is None or change is None:
            return f"Funnel stage '{r[0]}' has non-numeric values"
        if prev is not None and abs(prev + change - rows) > 0.5:
            return f"Funnel does not add up at '{r[0]}'"
        prev = rows
    if abs(num(funnel[0][1]) - num(total[2])) > 0.5:
        return "Funnel must start from the database pull (Coverage Total, with website and email)"

    found = {r[0].strip().lower(): num(r[1]) for r in table_rows(section(text, "Validation Results")) if len(r) > 1}
    for st in STATUSES:
        if found.get(st) is None:
            return f"Validation Results missing status '{st}'"
    vtotal = next((v for k, v in found.items() if k.startswith("total")), None)
    if vtotal is None or abs(sum(found[s] for s in STATUSES) - vtotal) > 0.5:
        return "validation statuses do not sum to Total validated"
    if abs(vtotal - num(funnel[-2][1])) > 0.5:
        return "Total validated must equal the funnel stage just before validation"
    if abs(found["valid"] - num(funnel[-1][1])) > 0.5:
        return "send-ready rows (last funnel stage) must equal the valid count"

    seg = {r[0].strip("` ").lower(): num(r[2]) for r in table_rows(section(text, "Segments")) if len(r) > 3}
    if seg.get("named_contact") is None or seg.get("role_inbox") is None:
        return "Segments needs named_contact and role_inbox rows with numeric counts"
    if abs(seg["named_contact"] + seg["role_inbox"] - found["valid"]) > 0.5:
        return "named_contact plus role_inbox must equal the send-ready (valid) count"
    for k, v in seg.items():
        if v is None or v > found["valid"]:
            return f"segment '{k}' needs a count no larger than the send-ready rows"

    cost_rows = table_rows(section(text, "Cost"))
    for r in cost_rows:
        if len(r) >= 6 and num(r[4]) and money(r[3]) is not None and money(r[5]) is not None:
            if abs(money(r[3]) / num(r[4]) - money(r[5])) > 0.006:
                return f"Cost row '{r[0]}': cost per new is not cost / new rows"

    qa = next((" ".join(r) for r in table_rows(section(text, "Checks")) if re.search(r"sample", r[0], re.I)), "")
    checks = re.findall(r"(\d+) of (\d+)", qa)
    if len(checks) < 3:
        return "Checks needs a QA sample row with its results written as 'N of M' (3+ checks)"
    for n, m in checks:
        if int(m) == 0 or int(n) > int(m):
            return f"QA sample check {n} of {m} is not a valid count"
    if not ISO.search(section(text, "Next Steps")):
        return "Next Steps needs dates"
    return None


def check_plan(text):
    if re.search(r"\d+\.\d+\s*%", text):
        return "a Plan carries no shares to a decimal place: measure them, or leave them to the run"
    cov = section(text, "Coverage")
    if not re.search(r"measured[^\n]*" + ISO.pattern + "|not measured", cov, re.I):
        return "Coverage needs the date the free counts were measured, or a 'Not measured' line"
    rows = table_rows(cov)
    total = next((r for r in rows if r[0].lower().startswith("total")), None)
    if total is not None:
        subs = [r for r in rows if r is not total]
        for col in range(1, len(total)):
            vals = [num(r[col]) if len(r) > col else None for r in subs]
            if num(total[col]) is not None and None not in vals and abs(sum(vals) - num(total[col])) > 0.5:
                return f"Coverage column {col + 1} does not sum to its Total"
    seg = {r[0].strip("` ").lower() for r in table_rows(section(text, "Segments"))}
    if not {"named_contact", "role_inbox"} <= seg:
        return "Segments needs named_contact and role_inbox rules"
    short = section(text, "Short Answer")
    if not re.search(r"\$\d", short) or not re.search(r"ceiling", short, re.I):
        return "Short Answer needs the all-in cost and the usage ceiling"
    if not re.search(r"^\s*1\.", section(text, "Decisions"), re.M):
        return "Decisions needs a numbered list"
    sched = section(text, "Run Schedule")
    if len(set(ISO.findall(sched))) < 3:
        return "Run Schedule needs 3+ dated steps"
    if not re.search(r"approv", sched, re.I):
        return "Run Schedule must say who approves each paid step"
    return None


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
    angle = re.search(r"<[A-Za-z][^>@\n]{0,60}>", text)
    if angle:
        return fail("angle-bracket placeholder left in: " + angle.group(0))
    status = re.search(r"^\W*Status:\W*(Plan|Delivered)\b", "\n".join(text.splitlines()[:12]), re.M | re.I)
    if not status:
        return fail("add one 'Status: Plan' or 'Status: Delivered' line near the top")
    mode = status.group(1).lower()

    headings = re.findall(r"^## (.+?)\s*$", text, re.M)
    lower = [h.lower() for h in headings]
    missing = [h for h in REQUIRED[mode] if h.lower() not in lower]
    if missing:
        return fail(f"{mode} report missing sections: " + ", ".join(missing))
    if lower[0] != "short answer":
        return fail("the first section must be Short Answer")
    for h in headings:
        if FORBIDDEN_HEADINGS.search(h) or (mode == "plan" and h in PLAN_FORBIDDEN):
            return fail(f"section '{h}' restates other sections or is not part of a {mode} report")

    for i, line in enumerate(text.splitlines(), 1):
        m = LEGAL.search(line)
        if m:
            return fail(f"line {i}: legal content '{m.group(0)}'; deliverables carry none")
        if re.search(chr(0x2013) + "|" + chr(0x2014), line):
            return fail(f"line {i}: em or en dash")
        if re.match(r"^\s*[-*] \[[ xX]\]", line):
            return fail(f"line {i}: self-grading checkbox; report the check result in Checks")
    internal = INTERNAL.search(text)
    if internal:
        return fail("internal detail the reader cannot act on: " + internal.group(0))
    disclaimers = DISCLAIMER.findall(text)
    if len(disclaimers) > 2:
        return fail(f"status disclaimer repeated {len(disclaimers)} times; state it once in the Status line")

    for err in (check_cost(text), check_columns(text, mode), check_thresholds(text),
                check_delivered(text) if mode == "delivered" else check_plan(text)):
        if err:
            return fail(err)
    if len(table_rows(section(text, "Checks"))) < 4:
        return fail("Checks needs 4+ rows with a pass line each")

    print(f"PASS - {path.name}: {mode} report, {len(headings)} sections, costs multiply out, thresholds sourced or set by the user")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
