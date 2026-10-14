#!/usr/bin/env python3
"""Check a CRM enrichment report against the crm-enricher output contract.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Summary",
    "Input Profile",
    "Field Rules",
    "Routing Plan",
    "Cost Estimate",
    "Fill Results",
    "Email Position After the Run",
    "Write-back Mapping",
    "Unfilled Flags",
    "How to Run It",
    "Refresh Schedule",
    "Next Steps",
]
# Sections that restate other sections or show plumbing; they cost the reader time.
BANNED_SECTIONS = re.compile(
    r"sample rows|match confidence|audit columns|fields you end up with|calls i would make"
    r"|quality check|frameworks?( applied)?$|methodology|sources used",
    re.I,
)
MIN_CHARS = 2500
MIN_TABLE_ROWS = 30
MAX_FLAG_ROWS = 8
POLICIES = {"fill_blank_only", "replace_if_invalid", "stage_for_review", "never_overwrite", "append_new"}
AUDIT_REQUIRED = ["enrich_run_id", "enriched_at", "enrich_source", "enrich_confidence", "enrich_status", "enrich_flags"]
NO_ACTION_CODES = {"NOT_FOUND", "SUPPRESSED", "LOOKUP_ERROR", "OUT_OF_CATALOG"}
ISO_DATE = re.compile(r"\b20\d\d-\d\d-\d\d\b")

# Deliverables carry no legal content. Same terms as scripts/validate-skills.py
# --check-legal; the bracketed letters keep this file from matching its own terms.
LEGAL = re.compile(
    r"\b(?:CAN[- ]?SP[A]M|T[C]PA|T[S]R|C[A]SL|G[D]PR|C[C]PA|C[P]RA|P[E]CR|F[C]RA|F[T]C|F[C]C|C[R]TC|I[C]O|D[N]C)\b"
    r"|\b(?:47|16)\s*C\.?F\.?R\b|U\.S\.C|Do[- ]Not[- ]Call|Att[o]rneys? Gen[e]ral|leg[a]l advi[c]e|\bnot leg[a]l\b"
    r"|\bcompliance\b|\bconsent\b|lawful bas[i]s"
    r"|\b(?:consult|ask|check with|speak (?:to|with)|talk (?:to|with))\s+(?:a|an|your)\s+(?:\w+\s+)?(?:lawy[e]r|attorn[e]y|couns[e]l)",
    re.I,
)
# The reader gets product names (Lead Database, Email Finder, Mobile Finder, Email
# Validator, Website Finder), never agent tool ids, skill names, repo paths or run plumbing.
INTERNAL = re.compile(
    r"\b(?:check_wallet|list_runs|check_run_status|download_results|cancel_run|query_lead_database"
    r"|query_local_business_database|find_emails|find_mobiles|find_people|validate_emails|scrape_[a-z_]+)\b"
    r"|\b(?:crm-enricher|email-list-cleaner|mobile-appender|cold-email-list|icp-list-builder"
    r"|decision-maker-finder|scrapercity-lead-database|scrapercity-integrations|skip-tracer|cold-calling)\b"
    r"|\b(?:references|templates|examples)/|SKILL\.md|check-output\.py|^Run ID:|\bRun ID:|\"tool\"\s*:",
    re.M,
)
# One status line at the top is enough; repeated "not run" asides are padding.
DISCLAIMER = re.compile(
    r"\bnot (?:yet )?run\b|has not been run|none (?:has|have) been run|nothing (?:has been |was )?(?:run|spent)"
    r"|assumed in this plan|^projected\b",
    re.I | re.M,
)
# A decay, bounce or validation-age number names where it came from.
NEEDS_SOURCE = re.compile(
    r"(?:\d[\d.]*%[^|\n]{0,80}(?:decay|stale|bounce|change (?:jobs|employer)|go(?:es)? bad))"
    r"|(?:(?:decay|stale|bounce|change (?:jobs|employer))[^|\n]{0,80}\d[\d.]*%)"
    r"|(?:within (?:the last )?\d+ days)",
    re.I,
)
SOURCE_TOKENS = re.compile(
    r"BLS|Bureau of Labor|ZeroBounce|Berman|Instantly|Hunter|Google|Yahoo|pilot|measured|your own|you set|you chose"
    r"|planning assumption",
    re.I,
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

    hit = re.search(r"\[(fill|todo|tbd)[^\]]*\]", text, re.I)
    if hit:
        return fail("placeholder left in: " + hit.group(0))
    angle = re.search(r"<[A-Za-z][^>\n]{0,60}>", text)
    if angle:
        return fail("angle-bracket placeholder left in: " + angle.group(0))

    for i, line in enumerate(text.splitlines(), 1):
        m = LEGAL.search(line)
        if m:
            return fail(f"line {i}: legal content '{m.group(0)}'; deliverables carry none")
        m = INTERNAL.search(line)
        if m:
            return fail(f"line {i}: internal id or path '{m.group(0)}'; use product names and plain steps")
        m = NEEDS_SOURCE.search(line)
        if m and not SOURCE_TOKENS.search(line):
            return fail(f"line {i}: '{m.group(0).strip()}' needs its source on the same line (or say it is measured or set by you)")
    disclaimers = DISCLAIMER.findall(text)
    if len(disclaimers) > 1:
        return fail(f"{len(disclaimers)} 'not run' or 'projected' asides; state the plan status once at the top")

    headings = [h.strip() for h in re.findall(r"^## (.+?)\s*$", text, re.M)]
    lower = [h.lower() for h in headings]
    missing = [h for h in REQUIRED if h.lower() not in lower]
    if missing:
        return fail("missing sections: " + ", ".join(missing))
    if lower[0] != "summary":
        return fail("Summary must be the first section: answer first")
    banned = [h for h in headings if BANNED_SECTIONS.search(h)]
    if banned:
        return fail("section restates other sections or shows plumbing: " + ", ".join(banned))
    if len(text) < MIN_CHARS:
        return fail(f"report too short ({len(text)} chars, need {MIN_CHARS})")
    total_rows = sum(len(table_rows(section(text, h))) for h in REQUIRED)
    if total_rows < MIN_TABLE_ROWS:
        return fail(f"only {total_rows} table rows across sections, need {MIN_TABLE_ROWS}")

    # Each fact once: no table row repeated anywhere in the report.
    seen = set()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", s):
            if s in seen:
                return fail("table row repeated: " + s[:80])
            seen.add(s)

    # Summary: the field list the user asked for and the money, up front.
    summary = table_rows(section(text, "Summary"))
    fields_row = next((r for r in summary if r and r[0].lower().startswith("fields")), None)
    if not fields_row or len(fields_row) < 2 or fields_row[1].count(",") < 3:
        return fail("Summary needs a 'Fields ...' row listing at least 4 fields")
    if not any("$" in " ".join(r) for r in summary):
        return fail("Summary needs the cost")

    # Field rules: controlled vocabulary, one never_overwrite, one dated approval line.
    block = section(text, "Field Rules")
    rules = table_rows(block)
    if len(rules) < 4:
        return fail("Field Rules needs at least 4 fields")
    for r in rules:
        if len(r) < 3 or r[2].strip().lower() not in POLICIES:
            return fail(f"Field Rules row '{r[0]}' has policy '{r[2] if len(r) > 2 else ''}', not one of {sorted(POLICIES)}")
    if not any(r[2].strip().lower() == "never_overwrite" for r in rules):
        return fail("Field Rules must name at least one never_overwrite field (owner, stage, subscription status)")
    approval = re.search(r"^Approv[a-z]*[^\n]*", block, re.M | re.I)
    if not approval or not ISO_DATE.search(approval.group(0)):
        return fail("Field Rules needs one 'Approval: who, YYYY-MM-DD' line")

    # Routing: match tiers in one sentence that sums.
    tiers = re.search(
        r"high ([\d,]+), medium ([\d,]+), low ([\d,]+), none ([\d,]+),? of ([\d,]+)", section(text, "Routing Plan"), re.I
    )
    if not tiers:
        return fail("Routing Plan needs 'Match tiers: high N, medium N, low N, none N, of T attempted'")
    h, m_, lo, no, tot = (num(g) for g in tiers.groups())
    if abs(h + m_ + lo + no - tot) > 0.5:
        return fail("match tiers do not sum to the lookups attempted")

    # Fill results balance; email lives only in Email Position.
    fills = table_rows(section(text, "Fill Results"))
    if len(fills) < 3:
        return fail("Fill Results needs at least 3 fields")
    for r in fills:
        if len(r) < 6:
            return fail("Fill Results rows need Field, Missing before, Filled, Staged, Unfilled, Filled by")
        if r[0].lower().startswith("email"):
            return fail("email belongs in Email Position After the Run only; state it once")
        vals = [num(c) for c in r[1:5]]
        if any(v is None for v in vals):
            return fail(f"Fill Results row '{r[0]}' has a non-numeric count")
        missing_n, filled, staged, unfilled = vals
        if abs(filled + staged + unfilled - missing_n) > 0.5:
            return fail(f"Fill Results row '{r[0]}': {filled:.0f} + {staged:.0f} + {unfilled:.0f} != {missing_n:.0f}")
        if not r[5]:
            return fail(f"Fill Results row '{r[0]}' does not say which source filled it")

    if len(table_rows(section(text, "Email Position After the Run"))) < 3:
        return fail("Email Position After the Run needs at least 3 groups")

    # Write-back mapping: every row has an import setting; audit columns named here.
    wb = section(text, "Write-back Mapping")
    for r in table_rows(wb):
        if len(r) < 3 or not r[2]:
            return fail(f"Write-back Mapping row '{r[0]}' has no import setting")
    absent = [c for c in AUDIT_REQUIRED if c not in wb]
    if absent or "prior_" not in wb:
        return fail("Write-back Mapping must name the audit columns: " + ", ".join(absent or ["prior_<field>"]))

    # Unfilled flags: only what a person has to act on.
    flags = table_rows(section(text, "Unfilled Flags"))
    if not flags or len(flags) > MAX_FLAG_ROWS:
        return fail(f"Unfilled Flags lists 1 to {MAX_FLAG_ROWS} codes that need a person; it has {len(flags)}")
    for r in flags:
        if r[0].strip().strip("`").upper() in NO_ACTION_CODES:
            return fail(f"Unfilled Flags row '{r[0]}' needs no person; it is already counted in Fill Results")
        if len(r) < 4 or not r[-1]:
            return fail(f"Unfilled Flags row '{r[0]}' has no next action")

    run = section(text, "How to Run It")
    if "npx scrapercity" not in run and "Authorization: Bearer" not in run:
        return fail("How to Run It needs the commands or REST calls a team can run")

    refresh = table_rows(section(text, "Refresh Schedule"))
    if len(refresh) < 2:
        return fail("Refresh Schedule needs at least 2 segments")
    for r in refresh:
        joined = " | ".join(r)
        if not ISO_DATE.search(joined):
            return fail(f"Refresh Schedule row '{r[0]}' has no YYYY-MM-DD date")
        if "$" not in joined:
            return fail(f"Refresh Schedule row '{r[0]}' has no cost")

    steps = re.findall(r"^\d+\.\s+(.+)$", section(text, "Next Steps"), re.M)
    if not steps:
        return fail("Next Steps needs numbered steps")
    for s in steps:
        if not ISO_DATE.search(s):
            return fail("every Next Step needs a YYYY-MM-DD date: " + s[:60])

    cost = section(text, "Cost Estimate")
    if not re.search(r"total[^\n]*\$\d", cost, re.I):
        return fail("Cost Estimate needs a Total row with a $ figure")

    print(f"PASS - {path.name}: {len(rules)} field rules, {len(fills)} fill rows balance, {tot:.0f} matches tiered, {len(flags)} flags need a person")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
