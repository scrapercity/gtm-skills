#!/usr/bin/env python3
"""Check a ScraperCity MCP setup and run report built from templates/output-template.md.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.

Two modes:
- Run report: the setup and calls were run. Verification and Run Log carry real results.
- Plan: nothing was run yet. One "Plan only:" line under the title says so, and the report
  has no Verification or Run Log section, no invented runIds and no agent test results.
"""
import re
import sys
from pathlib import Path

RUN_REQUIRED = [
    "Answer", "Client Setup", "Verification", "Agent Rules",
    "Run Plan", "Run Log", "Issues and Fixes", "Next Steps",
]
PLAN_REQUIRED = ["Answer", "Client Setup", "Agent Rules", "Run Plan", "Next Steps"]
TOOLS = {
    "check_wallet", "list_runs", "check_run_status", "download_results", "cancel_run",
    "query_lead_database", "query_local_business_database",
    "scrape_apollo", "scrape_website_finder", "find_people", "scrape_distress_list",
    "validate_emails", "scrape_maps", "scrape_airbnb", "scrape_bizbuysell", "scrape_crexi",
    "scrape_angi", "scrape_yelp", "scrape_zillow_agents", "scrape_property_lookup",
    "search_criminal_records", "scrape_store_leads", "scrape_builtwith", "find_emails",
    "find_mobiles",
}
FREE_READS = {"check_wallet", "list_runs", "check_run_status"}
STATUSES = {"RUNNING", "SUCCEEDED", "FAILED", "CANCELLED"}
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
# Blanks a reader would have to fill by hand: "...batch 1 domains...", ["...all emails..."],
# ?...your search..., /Users/you/...
BLANK = re.compile(
    r"[\"'\[(?=,]\s*\.\.\.\s*[A-Za-z]|[A-Za-z]\s*\.\.\.\s*[\"'\])]|\.\.\.\s*your\b|"
    r"/Users/you\b|/home/you\b|\\Users\\you\b",
    re.IGNORECASE,
)
# A loop described in a comment instead of written out.
COMMENT_LOOP = re.compile(r"^\s*#\s*(?:then\s+)?(?:loop|repeat|paginate|page through)\b", re.M | re.I)
# Results presented as real when they were not, and self-graded checks.
ASSUMED = re.compile(r"\(assumed\)|pass \(assumed|^\s*-\s*\[x\]", re.I | re.M)
# Internal names the reader has no use for: skill ids, repo paths, the checker.
INTERNAL = re.compile(
    r"\b(?:scrapercity-(?:cli|api|integrations|lead-database|local-business-database|real-estate-data)|"
    r"using-scrapercity-skills|email-list-cleaner|icp-list-builder)\b|"
    r"(?<![\w/.])(?:references|templates|examples|scripts)/[\w.-]+\.(?:md|py)|check-output\.py|SKILL\.md"
)
# An approval threshold presented as a rule; the go-ahead applies to every paid run.
APPROVAL_LINE_RX = re.compile(r"\$\d+(?:\.\d+)? approval line|approval line of \$|(?:under|over) the \$\d+(?:\.\d+)? (?:line|approval)|over about \$\d+|since it is over \$\d+", re.I)
# A benchmark percentage needs its source on the same line.
BENCHMARK = re.compile(r"(?:aim(?:s)? for|target of|minimum of|benchmark)[^.\n]*\d+%|\d+%\+?\s*(?:or more|is the minimum|minimum)", re.I)
SOURCE_HINT = re.compile(r"https?://|\b[\w-]+\.(?:com|io|org|ai|dev)\b|\bper [A-Z]", re.I)
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
PLAN_LINE = re.compile(r"^Plan only:\s*\S", re.M)
NOT_RUN_PHRASE = re.compile(r"\bnothing (?:here |below |in this report )?(?:has been|was|is) (?:actually )?run\b|\bnot (?:actually )?run\b", re.I)
# Reports carry no legal content (owner rule). Letters are bracketed so the
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
# A key value is fine when it is masked, a variable reference, or the documented placeholder.
SAFE_KEY = re.compile(r"^(\*+\w{0,6}|\.{3}|\$\{?[A-Za-z_:]+\}?|\$\{input:[\w-]+\}|YOUR_SCRAPERCITY_API_KEY)$")
KEY_VALUE = re.compile(r"SCRAPERCITY_API_KEY[\"']?\s*[:=]\s*[\"']?([^\s\"'`,}]+)")
MIN_CHARS = 1800
MAX_ANSWER_LINES = 8
NOT_RUN = re.compile(r"^\s*Not run:\s*\S", re.M | re.I)
PEOPLE_TOOLS = ("query_lead_database", "scrape_apollo", "scrape_website_finder")


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def has_heading(text, name):
    return bool(re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M | re.I))


def table_rows(block):
    rows = []
    in_code = False
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows[1:]


def kv(block):
    return {r[0].lower(): r[1] for r in table_rows(block) if len(r) >= 2}


def code_blocks(text):
    return re.findall(r"^```[^\n]*\n(.*?)^```", text, re.M | re.S)


def money(cell):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def number(cell):
    m = re.search(r"\d[\d,]*(?:\.\d+)?", cell)
    return float(m.group(0).replace(",", "")) if m else None


def fail(msg):
    print("FAIL - " + msg)
    return 1


def check_common(text, plan_mode):
    """Rules for every report. Returns an error string or None."""
    hit = PLACEHOLDER.search(text)
    if hit:
        return f"placeholder left in: {hit.group(0)}"
    legal = LEGAL.search(text)
    if legal:
        return f"legal commentary in the report ('{legal.group(0)}'); remove it"
    blank = BLANK.search(text)
    if blank:
        return f"a blank the reader has to fill by hand ('{blank.group(0)}'); write the real value, a named input with how to get it, or $HOME paths"
    if COMMENT_LOOP.search(text):
        return "a loop is described in a comment; write the loop out so it runs as pasted"
    assumed = ASSUMED.search(text)
    if assumed:
        return f"'{assumed.group(0).strip()}' presents an unrun result or a self-graded check; a plan states the plan once and leaves results out"
    extra = re.search(r"^## (?:Quality Check|Framework[^\n]*|Context|Summary)\s*$|\bSkills used\b", text, re.M | re.I)
    if extra:
        return f"'{extra.group(0).strip()}' is a section the user did not ask for; the Answer covers the summary"
    if plan_mode and re.search(r"ScraperCity - B2B Lead Generation|[Ss]tale (?:extension|copy)", text):
        return "a plan mentions a stale extension nobody has seen; report one only when it is found"
    internal = INTERNAL.search(text)
    if internal:
        return f"internal name in the report ('{internal.group(0)}'); the reader gets the deliverable only"
    line = APPROVAL_LINE_RX.search(text)
    if line:
        return f"'{line.group(0)}' presents a spend threshold as a rule; show the estimate and wait for the go-ahead"
    for ln in text.splitlines():
        if BENCHMARK.search(ln) and not SOURCE_HINT.search(ln):
            return f"benchmark with no source on its line: '{ln.strip()[:80]}'"

    blocks = code_blocks(text)
    seen = set()
    for b in blocks:
        key = b.strip()
        if len(key) > 40 and key in seen:
            return "the same code block appears twice; show each config or call once"
        seen.add(key)
    joined = "\n".join(blocks)

    # One JSON type per flag across every JSON block.
    for flag in ("hasEmail", "hasPhone", "hasWebsite", "hasContact", "excludeDelivered"):
        as_bool = re.search(r'"' + flag + r'"\s*:\s*(?:true|false)\b', joined)
        as_str = re.search(r'"' + flag + r'"\s*:\s*"(?:true|false)"', joined)
        if as_bool and as_str:
            return f"'{flag}' is a boolean in one call and a string in another; use one form"

    # A recommended pin must be the pin the shown config uses.
    pin = re.search(r"\bpin(?:ned|ning)?\b[^\n]*?scrapercity@(\d+\.\d+\.\d+)", text, re.I)
    if pin and ("scrapercity@" + pin.group(1)) not in joined:
        return f"the report recommends pinning scrapercity@{pin.group(1)} but no config shown uses it"

    # Agent rules: free reads only in any allow list; paid tools ask.
    rules = section(text, "Agent Rules")
    for m in re.finditer(r'"(?:allow|autoApprove|alwaysAllow)"\s*:\s*\[(.*?)\]', joined, re.S):
        for item in re.findall(r'"([^"]+)"', m.group(1)):
            tool = item.split("__")[-1]
            if tool not in FREE_READS:
                return f"'{item}' is auto-approved; only check_wallet, list_runs and check_run_status may run without a prompt"
    if not re.search(r"scrape_", rules) or not re.search(r"\bask\b|prompt", rules, re.I):
        return "Agent Rules must show that scrape_* and other paid tools ask before running"
    if re.search(r"^\|\s*Tier\s*\|", rules, re.M | re.I) and re.search(r'"permissions"|autoApprove|alwaysAllow', rules):
        return "Agent Rules shows the tiers twice (a tier table and the config); keep the config"
    tests = [r for r in table_rows(rules) if len(r) >= 2 and re.match(r"^(pass|fail|fixed)\b", r[1], re.I)]
    if plan_mode and tests:
        return "a plan reports no agent test results; tests are reported after they run"

    # Paging the database to a file: the MCP path comes first when the report uses a shell loop.
    if re.search(r"/api/v1/database/", joined) and re.search(r"\bcurl\b", joined):
        if not re.search(r'"tool"\s*:\s*"query_(?:lead|local_business)_database"[^\n]*"after"', text):
            return "the bulk pull bypasses MCP; write the query pages as MCP calls with 'after' and keep the shell loop as the fallback"

    # Cutting a people pull to the requested number: rank and cap, not row order.
    if any(t in text for t in PEOPLE_TOOLS) and re.search(r"\bspares?\b|first \d[\d,]* (?:rows|valid)", text, re.I):
        if not re.search(r"per[- ]company|per company domain|each company", text, re.I):
            return "the final cut takes rows in arrival order; rank by the requested titles and cap per company before cutting"
    return None


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/report.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/report.md (file not found)")
        return 2
    text = path.read_text(encoding="utf-8")

    head = text.split("\n## ", 1)[0]
    plan_mode = bool(PLAN_LINE.search(head))

    err = check_common(text, plan_mode)
    if err:
        return fail(err)

    required = PLAN_REQUIRED if plan_mode else RUN_REQUIRED
    for name in required:
        if not has_heading(text, name):
            return fail(f"missing heading '## {name}'")
    first = re.search(r"^## (.+?)\s*$", text, re.M)
    if not first or first.group(1).strip().lower() != "answer":
        return fail("the report opens with '## Answer'")
    answer_lines = [ln for ln in section(text, "Answer").splitlines() if ln.strip()]
    if len(answer_lines) > MAX_ANSWER_LINES:
        return fail(f"Answer runs {len(answer_lines)} lines; keep it to {MAX_ANSWER_LINES} or fewer")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")

    if plan_mode:
        if len(PLAN_LINE.findall(text)) != 1:
            return fail("a plan carries exactly one 'Plan only:' line, under the title")
        rest = PLAN_LINE.sub("", text, count=1)
        if NOT_RUN_PHRASE.search(rest):
            return fail("the 'not run' note repeats; the one 'Plan only:' line covers the whole report")
        for name in ("Verification", "Run Log"):
            if has_heading(text, name):
                return fail(f"a plan has no '## {name}' section; results go in after the run")
        if UUID.search(text):
            return fail("a plan carries no runId; runIds come from real runs")

    # 1. The config runs the right package and binary.
    setup = kv(section(text, "Client Setup"))
    args = setup.get("args", "")
    for part in ("-y", "--package", "scrapercity", "scrapercity-mcp"):
        if part not in args:
            return fail(f"Client Setup Args must include '{part}' (npx -y --package scrapercity scrapercity-mcp)")
    if not setup.get("key handling"):
        return fail("Client Setup needs a Key handling row")

    # 2. No unmasked API key anywhere in the report.
    for m in KEY_VALUE.finditer(text):
        if not SAFE_KEY.match(m.group(1)):
            return fail(f"API key value '{m.group(1)[:6]}...' is not masked or a variable reference")

    # 3. Run report: verification proves the server and the key; the wallet sets the ceiling.
    balance = None
    if not plan_mode:
        ver = kv(section(text, "Verification"))
        if "25" not in ver.get("tools listed", ""):
            return fail("Verification must report the 25 tools the server lists")
        wallet_call = ver.get("check_wallet call", "")
        if not re.search(r"succeed|plan", wallet_call, re.I):
            return fail("Verification must show a successful check_wallet call")
        balance = money(wallet_call)
        if balance is None:
            return fail("Verification's check_wallet row must show the balance as a $ figure")

    # 4. Run plan: known tools, arithmetic that adds up, webhook for Apollo, approval for any spend.
    plan_block = section(text, "Run Plan")
    log_block = section(text, "Run Log")
    setup_only = (not plan_mode) and bool(NOT_RUN.search(plan_block)) and not table_rows(plan_block)
    if setup_only:
        if not NOT_RUN.search(log_block) or table_rows(log_block):
            return fail("a setup-only report writes 'Not run:' under both Run Plan and Run Log")
        issues = section(text, "Issues and Fixes")
        if not table_rows(issues) and not re.search(r"^\s*None\b", issues, re.M | re.I):
            return fail("Issues and Fixes needs a table row or the word None")
        print("PASS - MCP setup report: client verified, no runs")
        return 0
    rows = table_rows(plan_block)
    steps = [r for r in rows if r and r[0].lower() != "total"]
    total_rows = [r for r in rows if r and r[0].lower() == "total"]
    if not steps:
        return fail("Run Plan needs at least one tool row")
    if not total_rows or money(total_rows[0][-1]) is None:
        return fail("Run Plan needs a Total row with a $ figure")
    total = money(total_rows[0][-1])
    running = 0.0
    for r in steps:
        if len(r) < 6:
            return fail(f"Run Plan row '{r[0]}' needs 6 columns")
        tool = r[1].strip("` ")
        if tool not in TOOLS:
            return fail(f"Run Plan tool '{r[1]}' is not a ScraperCity MCP tool")
        if tool == "scrape_apollo" and "webhook" not in " ".join(r).lower():
            return fail("a scrape_apollo row must name its webhook")
        units, price, cost = number(r[3]), money(r[4]), money(r[5])
        if cost is None:
            return fail(f"Run Plan row '{r[0]}' needs a $ cost")
        if units is not None and price is not None and abs(units * price - cost) > 0.011:
            return fail(f"Run Plan row '{r[0]}': {units:g} x ${price} is not ${cost}")
        running += cost
    if abs(running - total) > 0.011:
        return fail(f"Run Plan rows add to ${running:.2f}, Total says ${total:.2f}")
    if balance is not None and total > balance:
        return fail(f"Run Plan total ${total:.2f} exceeds the ${balance:.2f} balance; do not start")
    if total > 0:
        approval = re.search(r"^Approval:(.*)$", plan_block, re.M | re.I)
        if not approval or not re.search(r"approved|yes|go[- ]ahead", approval.group(1), re.I):
            return fail(f"Run Plan total ${total:.2f} is paid and has no Approval line (approved, or waits for a go-ahead)")
        if plan_mode and re.search(r"\bapproved\b", approval.group(1), re.I) and not re.search(r"go[- ]ahead|yes", approval.group(1), re.I):
            return fail("a plan cannot record an approval that has not happened; say the run waits for a go-ahead")

    if plan_mode:
        print(f"PASS - MCP plan: {len(steps)} planned calls, total ${total:.2f}, nothing run")
        return 0

    # 5. Run log: every run has an id, a known status, and SUCCEEDED rows an absolute file path.
    log = table_rows(log_block)
    if not log:
        return fail("Run Log needs at least one run row")
    for r in log:
        if len(r) < 5 or len(r[0]) < 8:
            return fail(f"Run Log row '{r[0]}' needs a full runId and 5 columns")
        status = r[2].upper().strip("` ")
        if status not in STATUSES:
            return fail(f"Run Log status '{r[2]}' must be one of {', '.join(sorted(STATUSES))}")
        if status == "SUCCEEDED" and not re.match(r"^`?(/|~/|\$HOME/|[A-Za-z]:\\)", r[4]):
            return fail(f"Run Log row '{r[0][:8]}' SUCCEEDED but its file path is not absolute")

    issues = section(text, "Issues and Fixes")
    if not table_rows(issues) and not re.search(r"^\s*None\b", issues, re.M | re.I):
        return fail("Issues and Fixes needs a table row or the word None")

    print(f"PASS - MCP report: {len(steps)} planned calls, total ${total:.2f}, {len(log)} runs logged")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
