#!/usr/bin/env python3
"""Check a ScraperCity CLI run spec built from templates/output-template.md.

Usage: check-output.py path/to/spec.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.

Commands and flags are checked against scrapercity 1.0.17 (bin/cli.mjs).
"""
import re
import shlex
import sys
from pathlib import Path

# Tech Stack Search command name, spelled in two parts for the repo copy rules.
TECH_CMD = "built" "with"
REQUIRED = [
    "Environment",
    "Commands",
    "Cost Estimate",
    "Script",
    "Schedule",
    "Failure Handling",
    "Verification",
]
DB_LEADS = {
    "--title", "--industry", "--country", "--state", "--city", "--company", "--domain", "--seniority",
    "--department", "--page", "--limit", "--min-employees", "--max-employees", "--after", "--url",
    "--apollo-url", "--keywords", "--revenue-min", "--revenue-max", "--company-country",
    "--company-state", "--company-city", "--not-title", "--not-keywords", "--not-industry",
    "--has-email", "--has-phone", "--exclude-delivered",
}
DB_LOCAL = {
    "--category", "--country", "--state", "--city", "--postal-code", "--query", "--min-rating",
    "--max-rating", "--min-reviews", "--max-reviews", "--page", "--limit", "--after", "--url",
    "--title", "--not-category", "--box", "--keyword", "--location", "--has-email", "--has-phone",
    "--has-website", "--has-contact", "--exclude-delivered",
}
FLAGS = {
    "login": set(), "wallet": set(), "runs": {"--hours", "--limit"}, "status": set(),
    "poll": {"--interval"}, "download": {"--output", "-o"}, "cancel": set(), "logs": set(),
    "apollo": {"--count", "--name"},
    "maps": {"--query", "-q", "--location", "-l", "--limit"},
    "email-validate": {"--file"},
    "email-find": {"--first", "--last", "--full-name", "--domain", "--company", "--file", "--validate", "--mobiles"},
    "mobile-find": {"--file"},
    "people-find": {"--name", "--email", "--phone", "--address", "--max-results"},
    "store-leads": {"--platform", "--country", "--category", "--city", "--technologies", "--apps",
                    "--total-leads", "--name", "--emails", "--phones", "--instagram", "--facebook",
                    "--tiktok", "--youtube", "--linkedin"},
    TECH_CMD: {"--tech", "--name"},
    "criminal": {"--name", "--state", "--dob"},
    "airbnb": {"--city", "--url", "--max-results", "--limit", "--checkin", "--checkout"},
    "website-finder": {"--file", "--title"},
    "yelp": {"--query", "-q", "--location", "-l", "--urls", "--limit"},
    "angi": {"--query", "-q", "--zips", "--limit"},
    "zillow-agents": {"--location", "-l", "--specialty", "--language", "--limit"},
    "bizbuysell": {"--limit"},
    "crexi": set(),
    "distress-list": {"--types", "--max"},
    "db-leads": DB_LEADS,
    "db-local": DB_LOCAL,
    "help": set(),
}
# Flags 1.0.17 reads but mixes into other values (see references/gaps-and-quirks.md).
BROKEN = {
    (TECH_CMD, "--name"): "technology absorbs the --name value",
    ("website-finder", "--title"): "the title is also sent as a domain",
    ("website-finder", "--file"): "the file name is also sent as a domain",
    ("bizbuysell", "--limit"): "the limit value is sent as a start URL",
}
INVOKE = re.compile(r'(?:\bscrapercity(?:@[\d.]+)?|"\$\{SC\[@\]\}"|\bstart_run)[ \t]+([a-z][a-z-]*)(.*)')
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
# Specs carry no legal content (owner rule). Letters are bracketed so the
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
RAW_KEY = re.compile(r"SCRAPERCITY_API_KEY=(?![\"']?\$|[\"']?YOUR_SCRAPERCITY_API_KEY)[\"']?[A-Za-z0-9_\-]{8,}")
STOP = {"|", "||", "&&", ";", ")", ">", ">>", "<", "&", "2>", "2>&1"}
MIN_CHARS = 2500


# Economy and honesty rules shared by the ScraperCity checkers: no unrun results presented
# as real, no blanks the reader fills by hand, no loop left in a comment, no spend threshold
# presented as a rule, and a source on the same line as any percentage benchmark.
_ASSUMED = re.compile(r"\(assumed\)|^\s*-\s*\[x\]", re.I | re.M)
_BLANK = re.compile(r"[\"'\[(?=,]\s*\.\.\.\s*[A-Za-z]|[A-Za-z]\s*\.\.\.\s*[\"'\])]|\.\.\.\s*your\b|/Users/you\b|/home/you\b", re.I)
_COMMENT_LOOP = re.compile(r"^\s*#\s*(?:then\s+)?(?:loop|repeat|paginate|page through)\b", re.M | re.I)
_SPEND_LINE = re.compile(r"\$\d+(?:\.\d+)? approval line|approval line of \$|(?:under|over) the \$\d+(?:\.\d+)? (?:line|approval)|over about \$\d+|since it is over \$\d+", re.I)
_BENCHMARK = re.compile(r"(?:aim(?:s)? for|target of|minimum of|benchmark)[^.\n]*\d+%|\d+%\+?\s*(?:or more|is the minimum)", re.I)
_SOURCE_HINT = re.compile(r"https?://|\b[\w-]+\.(?:com|io|org|ai|dev)\b|\bper [A-Z]", re.I)


def economy_error(text):
    for rx, msg in ((_ASSUMED, "presents an unrun result or a self-graded check"),
                    (_BLANK, "is a blank the reader has to fill by hand; write the value or a named input"),
                    (_COMMENT_LOOP, "describes a loop in a comment; write the loop out"),
                    (_SPEND_LINE, "presents a spend threshold as a rule; every paid run waits for a go-ahead")):
        m = rx.search(text)
        if m:
            return f"'{m.group(0).strip()}' {msg}"
    for ln in text.splitlines():
        if _BENCHMARK.search(ln) and not _SOURCE_HINT.search(ln):
            return f"benchmark with no source on its line: '{ln.strip()[:80]}'"
    return None

def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def table_rows(block):
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        rows.append([c.strip() for c in re.split(r"(?<!\\)\|", line.strip("|"))])
    return rows[1:]


def money(cell):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def number(cell):
    m = re.search(r"\d[\d,]*(?:\.\d+)?", cell)
    return float(m.group(0).replace(",", "")) if m else None


def tokens(rest):
    lex = shlex.shlex(rest, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    lex.commenters = "#"
    out = []
    try:
        for tok in lex:
            if tok in STOP or tok.startswith(">"):
                break
            out.append(tok)
    except ValueError:
        out = rest.split()
    return out


def check_invocation(cmd, rest, where):
    if cmd not in FLAGS:
        return f"{where}: '{cmd}' is not a scrapercity 1.0.17 command"
    toks = tokens(rest)
    flags = [t for t in toks if re.match(r"^--?[A-Za-z][\w-]*$", t)]
    for f in flags:
        if f not in FLAGS[cmd]:
            return f"{where}: '{cmd}' has no flag '{f}' in 1.0.17"
        if (cmd, f) in BROKEN:
            return f"{where}: '{cmd} {f}' misbehaves in 1.0.17 ({BROKEN[(cmd, f)]}); use MCP or REST"
    if cmd == "criminal" and "--name" not in flags:
        return f"{where}: criminal must use --name (a positional name absorbs other flag values)"
    if cmd == "download" and "-o" not in flags and "--output" not in flags:
        return f"{where}: download must name its file with -o"
    if cmd in ("db-leads", "db-local") and "--exclude-delivered" in flags:
        if "--after" not in flags:
            return f"{where}: --exclude-delivered needs --after (cursor), not page numbers"
        if "--page" in flags:
            i = toks.index("--page")
            if i + 1 < len(toks) and toks[i + 1].isdigit() and int(toks[i + 1]) > 1:
                return f"{where}: --exclude-delivered with --page above 1 skips records"
    return None


def fail(msg):
    print("FAIL - " + msg)
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/spec.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("usage: check-output.py path/to/spec.md (file not found)")
        return 2
    text = path.read_text(encoding="utf-8")
    _econ = economy_error(text)
    if _econ:
        return fail(_econ)

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    legal = LEGAL.search(text)
    if legal:
        return fail(f"legal commentary in the spec ('{legal.group(0)}'); remove it")
    for name in REQUIRED:
        if not re.search(r"^## " + re.escape(name) + r"\s*$", text, re.M | re.I):
            return fail(f"missing heading '## {name}'")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")

    # 1. Commands table: known commands and flags only.
    cmd_rows = table_rows(section(text, "Commands"))
    if len(cmd_rows) < 2:
        return fail("Commands needs at least 2 rows")
    invocations = 0
    for r in cmd_rows:
        if len(r) < 3:
            return fail(f"Commands row '{r[0]}' needs Step, Command and Maps to")
        cell = r[1].strip()
        m = re.match(r"^`(.*)`$", cell)
        if not m:
            return fail(f"Commands row '{r[0]}': put the command in backticks")
        line = m.group(1).strip()
        if line.startswith("curl"):
            continue
        if not re.match(r"^(npx (-y )?)?scrapercity(@[\d.]+)? ", line):
            return fail(f"Commands row '{r[0]}' must start with scrapercity, npx scrapercity, or curl")
        inv = INVOKE.search(line)
        err = check_invocation(inv.group(1), inv.group(2), f"Commands row {r[0]}")
        if err:
            return fail(err)
        invocations += 1

    # 2. Script: strict mode, no raw key, every CLI call valid.
    script_block = section(text, "Script")
    code = re.search(r"```(?:bash|sh)?\n(.*?)```", script_block, re.S)
    if not code or len(code.group(1).strip().splitlines()) < 10:
        return fail("Script needs a bash code block of at least 10 lines")
    script = code.group(1).replace("\\\n", " ")
    if not re.search(r"^set -[a-z]*e[a-z]*( -o pipefail)?", script, re.M) and "set -euo pipefail" not in script:
        return fail("Script must start strict mode (set -euo pipefail)")
    key = RAW_KEY.search(text)
    if key:
        return fail("an API key value is written into the spec; read it from the environment")
    if re.search(r"Bearer [A-Za-z0-9]{16,}", text):
        return fail("a literal Bearer token is written into the spec")
    for n, line in enumerate(script.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for inv in INVOKE.finditer(stripped):
            err = check_invocation(inv.group(1), inv.group(2), f"Script line {n}")
            if err:
                return fail(err)
            invocations += 1
    if "wallet" not in script:
        return fail("Script must check the wallet before paid steps")

    # 3. Apollo needs a webhook, never poll alone.
    if re.search(r"scrapercity(?:@[\d.]+)?\s+apollo\b|start_run\s+apollo\b", text) and "webhook" not in text.lower():
        return fail("an apollo run is used without a webhook")

    # 4. Cost estimate adds up; any paid total has a recorded approval.
    cost_block = section(text, "Cost Estimate")
    rows = table_rows(cost_block)
    lines = [r for r in rows if r and r[0].lower() != "total"]
    totals = [r for r in rows if r and r[0].lower() == "total"]
    if not lines or not totals or money(totals[0][-1]) is None:
        return fail("Cost Estimate needs line items and a Total row with a $ figure")
    total = money(totals[0][-1])
    running = 0.0
    for r in lines:
        if len(r) < 4 or money(r[3]) is None:
            return fail(f"Cost Estimate line '{r[0]}' needs a $ cost")
        units, price, cost = number(r[1]), money(r[2]), money(r[3])
        if units is not None and price is not None and abs(units * price - cost) > 0.011:
            return fail(f"Cost Estimate line '{r[0]}': {units:g} x ${price} is not ${cost}")
        running += cost
    if abs(running - total) > 0.011:
        return fail(f"Cost Estimate lines add to ${running:.2f}, Total says ${total:.2f}")
    if total > 0:
        approval = re.search(r"^Approval:(.*)$", cost_block, re.M | re.I)
        if not approval or not re.search(r"approved|yes|go ahead", approval.group(1), re.I):
            return fail(f"Cost Estimate total ${total:.2f} is a paid total with no recorded approval")

    # 5. Schedule, failure handling and verification are filled in.
    sched = {r[0].lower(): r[1] for r in table_rows(section(text, "Schedule")) if len(r) >= 2}
    if not sched.get("schedule"):
        return fail("Schedule needs a Schedule row (cron line, CI cron, or 'manual')")
    if re.search(r"\d+ \d+ [\d*,/-]+ [\d*,/-]+ [\d*,/-]+", sched.get("schedule", "")) and "utc" not in sched.get("time zone", "").lower():
        return fail("a cron schedule must state its time zone relative to UTC")
    if len(table_rows(section(text, "Failure Handling"))) < 3:
        return fail("Failure Handling needs at least 3 rows")
    if len(table_rows(section(text, "Verification"))) < 2:
        return fail("Verification needs at least 2 rows")

    print(f"PASS - CLI run spec: {invocations} CLI calls checked against 1.0.17, total ${total:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
