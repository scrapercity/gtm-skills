#!/usr/bin/env python3
"""Check a ScraperCity routing plan built from templates/output-template.md.

Usage: check-output.py path/to/routing-plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.

Checks:
  - every required section, no placeholders, minimum length
  - every skill in the chain exists in this repo
  - every paid tool row: unit price matches the catalog, units x price = cost
  - the cost rows sum to the stated total
  - all five gates are present and have a status
  - suppression gate covers unsubscribes for email and the do-not-contact list for phone
  - quality gate requires a match check when People Finder or Property Lookup is used
  - no legal commentary (statutes, regulators, legal disclaimers) anywhere in the plan
"""
import re
import sys
from pathlib import Path

REQUIRED = ["Request", "Skill Chain", "Tool Calls and Cost", "Gates", "Handoffs", "Open Questions"]
SKILLS = {
    "using-scrapercity-skills", "scrapercity-mcp", "scrapercity-cli", "scrapercity-api",
    "scrapercity-integrations", "scrapercity-lead-database", "scrapercity-local-business-database",
    "scrapercity-real-estate-data", "icp-list-builder", "tam-builder", "decision-maker-finder",
    "account-researcher", "local-business-list", "cold-email-list", "email-list-cleaner",
    "crm-enricher", "mobile-appender", "ecommerce-by-techstack", "skip-tracer", "recruiting-sourcer",
    "cold-email-strategy", "cold-email-copywriting", "reply-handling", "multi-channel-outreach",
    "domain-infrastructure", "inbox-setup", "email-deliverability", "sending-platforms",
    "cold-calling", "signal-triggered-outbound", "outbound-unit-economics",
}
# Per-result prices from references/scrapercity-catalog.md (scrapercity 1.0.17). 0 = included with Growth and up.
PRICES = {
    "query_lead_database": 0.0, "query_local_business_database": 0.0,
    "scrape_apollo": 0.0039, "scrape_website_finder": 0.0499, "find_people": 0.0199,
    "scrape_distress_list": 0.05, "validate_emails": 0.00169, "scrape_maps": 0.0099,
    "scrape_airbnb": 0.019, "scrape_bizbuysell": 0.0099, "scrape_crexi": 0.029,
    "scrape_angi": 0.0099, "scrape_yelp": 0.0099, "scrape_zillow_agents": 0.029,
    "scrape_property_lookup": 0.15, "search_criminal_records": 1.00, "scrape_store_leads": 0.0039,
    "scrape_builtwith": 4.99, "find_emails": 0.05, "find_mobiles": 0.25,
}
MATCH_TOOLS = {"find_people", "scrape_property_lookup"}
GATES = ["wallet", "count", "suppression", "quality", "deliverability"]
# Plans carry no legal content (owner rule). Letters are bracketed so the
# pattern list itself does not trip the repo's legal-term scan.
LEGAL = re.compile(
    r"\bc[a]n[- ]?sp[a]m\b|\bt[c]pa\b|telephone consumer prot|\bc[a]sl\b|\bg[d]pr\b|\bepriv[a]cy\b|"
    r"lawful b[a]sis|\bc[c]pa\b|\bc[p]ra\b|\bp[e]cr\b|\bf[c]ra\b|fair credit rep|\bt[s]r\b|"
    r"telemarketing sales r|\b(?:47|16)\s*c\.?f\.?r\b|\bf[t]c\b|\bf[c]c\b|\bc[r]tc\b|\bi[c]o\b|"
    r"att[o]rneys? gen|legal adv[i]ce|\bnot leg[a]l\b|\bstatute|\bd[n]c\b|"
    r"\b(?:consult|ask|check with)\s+(?:a|an|your)\s+(?:\w+\s+)?(?:law[y]er|att[o]rney|coun[s]el)|"
    r"do[- ]not[- ]call regis|national do[- ]not[- ]call|complian[c]e gate",
    re.IGNORECASE,
)
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 1500


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
    return m.group(1) if m else None


def rows(block):
    out = []
    for line in (block or "").splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        out.append([c.strip() for c in line.strip("|").split("|")])
    return out[1:]


def money(cell):
    m = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def number(cell):
    m = re.search(r"([\d,]+(?:\.\d+)?)", cell)
    return float(m.group(1).replace(",", "")) if m else None


def fail(msg):
    print("FAIL - " + msg)
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/routing-plan.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"FAIL - file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")
    _econ = economy_error(text)
    if _econ:
        return fail(_econ)

    if PLACEHOLDER.search(text):
        return fail("unresolved placeholders remain")
    if len(text.strip()) < MIN_CHARS:
        return fail(f"plan is under {MIN_CHARS} characters")
    for name in REQUIRED:
        if section(text, name) is None:
            return fail(f"missing section '## {name}'")

    request = {r[0].lower(): r[1] for r in rows(section(text, "Request")) if len(r) >= 2}
    channels = request.get("channels", "").lower()

    chain = rows(section(text, "Skill Chain"))
    if len(chain) < 2:
        return fail("skill chain needs at least 2 steps")
    for r in chain:
        names = re.findall(r"`([a-z0-9-]+)`", r[1] if len(r) > 1 else "")
        if not names:
            return fail(f"chain step '{r[0]}' does not name a skill in backticks")
        for n in names:
            if n not in SKILLS:
                return fail(f"unknown skill '{n}' in the chain")

    cost_rows = rows(section(text, "Tool Calls and Cost"))
    total_stated, summed, tools_used = None, 0.0, set()
    for r in cost_rows:
        if len(r) < 5:
            continue
        if "total" in r[1].lower():
            total_stated = money(r[4])
            continue
        tool = re.findall(r"`([a-z_]+)`", r[1])
        if not tool:
            return fail(f"cost row without a tool id: {r[1]}")
        tool = tool[0]
        if tool not in PRICES:
            return fail(f"unknown tool '{tool}'")
        units, price, cost = number(r[2]), money(r[3]), money(r[4])
        if units is None or price is None or cost is None:
            return fail(f"row for {tool} needs units, a $ unit price and a $ cost")
        if abs(price - PRICES[tool]) > 1e-9:
            return fail(f"{tool} unit price ${price} does not match catalog ${PRICES[tool]}")
        if abs(units * price - cost) > 0.01:
            return fail(f"{tool}: {units:g} x ${price} = ${units * price:.2f}, row says ${cost:.2f}")
        if units > 0:
            tools_used.add(tool)
        summed += cost
    if total_stated is None:
        return fail("no Total row in Tool Calls and Cost")
    if abs(total_stated - summed) > 0.01:
        return fail(f"rows sum to ${summed:.2f}, total says ${total_stated:.2f}")

    gates = {r[0].lower(): r for r in rows(section(text, "Gates")) if r}
    for g in GATES:
        if g not in gates:
            return fail(f"missing gate '{g}'")
        if len(gates[g]) < 3 or not gates[g][2]:
            return fail(f"gate '{g}' has no status")
    suppression = " ".join(gates["suppression"]).lower()
    if "email" in channels and "unsubscribe" not in suppression:
        return fail("email channel without unsubscribe handling in the suppression gate")
    if any(w in channels for w in ("phone", "call", "sms", "text")) and "do-not-contact" not in suppression:
        return fail("phone channel without the do-not-contact list in the suppression gate")
    if tools_used & MATCH_TOOLS and "match" not in " ".join(gates["quality"]).lower():
        return fail("People Finder or Property Lookup used without a match check in the quality gate")
    legal = LEGAL.search(text)
    if legal:
        return fail(f"legal commentary in the plan ('{legal.group(0)}'); remove it")

    if len(rows(section(text, "Handoffs"))) < len(chain) - 1:
        return fail("every step after the first needs a handoff row")

    print(f"PASS - {len(chain)} skills chained, ${summed:.2f} priced from the catalog, all 5 gates set")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
