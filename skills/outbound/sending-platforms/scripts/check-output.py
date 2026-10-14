#!/usr/bin/env python3
"""Check a finished sending platform plan.

Fails on legal content (owner rule), on a daily limit per mailbox of 50 or
more (Alex Berman: keep it under 50 per inbox), on agent tool calls or
mailbox-provider rule citations the reader cannot use, on repeated figures and
extra sections, on a Meeting booked stage driven by a reply label, and on a
Cost total that does not add up.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import hashlib
import re
import sys
from pathlib import Path

REQUIRED = [
    "Summary",
    "Assumptions and Open Questions",
    "Requirements",
    "Platform Decision",
    "Workspace Settings",
    "Column Map",
    "Import Procedure",
    "Suppression and Dedupe",
    "Webhooks to CRM",
    "Test Plan",
    "Cost",
]
ASSUMPTION_TOPICS = {
    "HubSpot portals": re.compile(r"portal", re.IGNORECASE),
    "client logins": re.compile(r"login", re.IGNORECASE),
    "inbox mix": re.compile(r"inbox|mailbox", re.IGNORECASE),
    "current tool": re.compile(r"current (sending )?tool", re.IGNORECASE),
    "budget": re.compile(r"budget", re.IGNORECASE),
}
NO_TOOL = re.compile(r"^\s*(none|no\b|not |unknown|n/a|-)", re.IGNORECASE)
COST_LINES = {
    "mailboxes": re.compile(r"mailbox|inbox|seat", re.IGNORECASE),
    "domains": re.compile(r"domain", re.IGNORECASE),
    "automation": re.compile(r"automation|middleware|n8n|zapier|make\.com|pipedream", re.IGNORECASE),
}
ALLOWED_SECTIONS = {s.lower() for s in (
    "Summary", "Assumptions and Open Questions", "Requirements", "Platform Decision", "Workspace Settings",
    "Column Map", "Import Procedure", "Suppression and Dedupe", "Webhooks to CRM", "Test Plan",
    "Migration Plan", "Cost")}
SUMMARY_MAX_WORDS = 110
# Agent tool names and call syntax: the reader is a person with a vendor UI or a REST client.
AGENT_TOOLS = re.compile(
    r"\b(check_wallet|list_runs|check_run_status|download_results|cancel_run|query_lead_database|"
    r"query_local_business_database|validate_emails|find_emails|find_mobiles|find_people|"
    r"search_criminal_records|scrape_[a-z_]+)\b|\b[a-z][a-z_]+\(\)|\b[a-z]+_[a-z_]+\(\w+=",
)
DB_PARAM = re.compile(r"\bexcludeDelivered\b")
RULE_CITATION = re.compile(
    r"\b(Google|Yahoo|Gmail|Microsoft|Outlook)\b[^|\n.]{0,40}\b(rules?|requirements?|guidelines?|mandates?)\b",
    re.IGNORECASE,
)
ASSUMED_NOTE = re.compile(r"assumed until (run|checked)|results? (are )?assumed|\(assumed\)", re.IGNORECASE)
WHY_PARA = re.compile(r"^\**why\b[^\n]{0,80}\bover\b", re.IGNORECASE | re.MULTILINE)
GAP = re.compile(r"\$(\d[\d,]*(?:\.\d+)?)\s+(?:a (?:month|year)\s+)?(more|less|cheaper|dearer|higher|lower)\b", re.IGNORECASE)
CENTS = re.compile(r"\$(\d[\d,]*\.\d{2})\b")
REPLY_LABEL = re.compile(r"LEAD_CATEGORY_UPDATED|meeting request|lead_meeting_booked|interest status|label|category", re.IGNORECASE)
ALREADY = re.compile(r"already (send|warm)|existing|sending (about|around)?\s*[\d,]+ a day today|at the \d+-send cap", re.IGNORECASE)
MONEY = re.compile(r"\$(\d[\d,]*(?:\.\d+)?)")
SKILL_SLUGS = (
    "cold-email-strategy|cold-email-copywriting|reply-handling|multi-channel-outreach|domain-infrastructure|"
    "inbox-setup|email-deliverability|sending-platforms|cold-calling|signal-triggered-outbound|"
    "outbound-unit-economics|icp-list-builder|tam-builder|decision-maker-finder|account-researcher|"
    "local-business-list|cold-email-list|email-list-cleaner|crm-enricher|mobile-appender|"
    "ecommerce-by-techstack|skip-tracer|recruiting-sourcer|using-scrapercity-skills|scrapercity-mcp|"
    "scrapercity-cli|scrapercity-api|scrapercity-integrations|scrapercity-lead-database|"
    "scrapercity-local-business-database|scrapercity-real-estate-data"
)
INTERNAL = re.compile(
    r"\b(references|templates|scripts|examples)/|SKILL\.md|[\w-]+\.md\b|(?<![\w-])(" + SKILL_SLUGS + r")(?![\w-])",
    re.IGNORECASE,
)
PRICE_CMP = re.compile(
    r"\(\$(\d[\d,]*(?:\.\d+)?)\)[^.()]{0,40}?\$(\d[\d,]*(?:\.\d+)?) (more|less|cheaper|dearer|higher|lower)"
    r"[^.()]{0,30}? than [^.()]{0,40}?\(\$(\d[\d,]*(?:\.\d+)?)\)",
    re.IGNORECASE,
)


def num(x):
    return float(x.replace(",", ""))
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 4000
CAP_LIMIT = 50  # Alex Berman: under 50 cold emails a day per inbox
DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
OVERRIDE = re.compile(
    r"(ignore_global_block_list|ignore_unsubscribe_list|ignore_community_bounce_list)\W{0,4}(true|on|yes)",
    re.IGNORECASE,
)
MIGRATION_STEPS = {
    "pre-commitment trial": re.compile(r"trial", re.IGNORECASE),
    "export from the old tool": re.compile(r"export", re.IGNORECASE),
    "mid-sequence prospects finish on the old tool": re.compile(r"mid-sequence|finish", re.IGNORECASE),
    "rebuild sequences": re.compile(r"rebuild", re.IGNORECASE),
    "reconnect the same mailboxes": re.compile(r"reconnect|mailbox", re.IGNORECASE),
    "re-point tracking CNAME": re.compile(r"tracking|cname", re.IGNORECASE),
    "parallel run": re.compile(r"parallel", re.IGNORECASE),
    "decommission": re.compile(r"decommission", re.IGNORECASE),
}
PADDING = re.compile(r"^##+\s*(quality check|frameworks?( applied)?|framework basis|self[- ]assessment)\b", re.IGNORECASE | re.MULTILINE)
CLIENT_ROUTING = re.compile(r"client[- ]level|per client|each client|one per client|client's portal|workspace", re.IGNORECASE)
NEEDED_EVENTS = {
    "reply": re.compile(r"repl", re.IGNORECASE),
    "unsubscribe": re.compile(r"unsubscri", re.IGNORECASE),
    "bounce": re.compile(r"bounce", re.IGNORECASE),
}


# Owner rule: deliverables carry no legal content. The terms (laws, regulators, legal
# advice, consent) are stored as SHA-256 hashes of lowercased words and word pairs so
# this file itself names none of them.
LEGAL_HASHES = {
    "9d8be820823bd8b1ceecaef063aea4c28da6f22fc8565985b17f05a49e04620c",
    "f63dd214824a68974443cba568eb6ef8af02ef2b3aa5848cb567b2a9b7b33eee",
    "df679e72d63dc69befbe502d5e155258ca356fa1ac5ab7b47aab9c990f9586c1",
    "8d53e0154b79535cda4bda2c9ad960af9bf320002ce8d8365c7a0a56f4f897f9",
    "8b16477e3abe1de345a6e82f360db77b5e238983ad685cec9fef0d0bc009aed3",
    "0c89db9e0a961c3939fb277192805c817fdf6b611e353477970af73ad9b54236",
    "ca30ed14f4d400b853d9b111688395db1d75a5583539d9841b2209d0b9d8400c",
    "fa193c8cc820b3b216502909af65a353a26b670c77833006d7dca1144bfb6950",
    "9f6bbaad419acd37b0d06e775bb1d28533a0cefdef0c245d769af00a80eef975",
    "7ffc2a17340af2828c78218d1f933dd37bc8203c6843d675a1da0c6210bbb8fc",
    "c818cdccc0a062a8aafff7af570b2a10e62600ab4ef7dea12e8566ec16015148",
    "06e901d0ba7b90b8ab9466a114c93dc1830a9bb83845a732b92bf90d91da7e3e",
    "31eab555f64988513f62d41c77252e07836b01303b7b38e42bb71c5be5be3904",
    "88b1fe38cf4efddeccb0a6b068134a319c9bcd5bd5fefb53b1addebd8481bf8b",
    "0d4bf5b068aa598c06488809d6c39af7d3f9e2c8dcbd5324cd8fdd26b3135a19",
    "b0c50e9b35b69e48852157aa642adbf411eb3239fc49d5d0f90b38739ee38789",
    "c51052ef06b65a956d9edade6297b03388457a6521544a6d11e1c0507173b2f3",
    "523c1b730b9c9b9f5aff9435a0953988bc08f8626bb8902cd9a1afa9be9ba9db",
    "467f0ea7dd59072ccaa8dcd5901728a463e3d9a9e13d2c676fd2dc80c891124f",
    "83a70052504733134861af25c442ffd741935da314c948f2e015a93b2d0af6ed",
    "6c0a579f38b0e548486f32f9e6d1585102d1050e2d50293a324405735e2f7d78",
    "5561ba03cac2c86f883ddbe7966f05c12375f0ce18fe8a0938733d170887fe76",
    "1244377974aeb11cf1b66db5a33bb15b58ec15d72a6e807157d50e62b642de25",
    "ff9a0c76596a5d3c658f760c483cc2b927d118bc84c52d8ea2146a0cf2a4c9f6",
    "503acf004b50b4f97beae09309f837a2ba47afacc83800fce9a1066813c7a97d",
    "c1818e804aa575636570432284eb15ef692087ef09f6542c1b302bd6f7bb4419",
    "fe98a4b07a9f4ee4ec6638054f073defc31b0f216a4e38f46361c1e62bc788a2",
    "4ad92a45689299fb31cec0c4d2912f4f98218da1f61c632567362818645161d5",
    "383b6630e8241d34d54bfd689decc0cab88770d935667989a3a1de8397f5520f",
    "b3466e5f75eb27dabd63b94b3fee826acd9de192d400569b894d7685e814dd8a",
    "0b7b13bc416f7216aeca837585dc4bccc6fd9e4bb8e00e41cf608fe9253e60c6",
    "114ece8d992faac0dbffa9f93988ea242de90980817208ac293e8f4b576cf886",
    "12423e0482f3e81cb1d23230664e95bb3d11b9f34f06fc199e588d4cdab6e4d4",
    "e068496fb44ea938edba82e057fdd593dbe2620e68aa5c4a75b7aa31aa67c591",
    "62ae4ff47444a8465b7923c659ebe4f24549a314307a2f30f33cb99b5d5c422a",
    "1b0dd42b70a0535277095734c5a850f07308022b7fda34d958a42d0989190834",
    "0ecce90493ca388227361a7231c2e9bb07a8f6528c9ffb5062b80ddbe153e9d8",
}


def legal_term(text):
    words = re.findall(r"[a-z][a-z-]*", text.lower())
    for i, w in enumerate(words):
        for cand in (w, " ".join(words[i:i + 2])):
            if hashlib.sha256(cand.encode()).hexdigest() in LEGAL_HASHES:
                return cand
    return None


def sections(text):
    out, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip().lower()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def table(block):
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    if not rows:
        return [], []
    return [h.lower() for h in rows[0]], rows[1:]


def col(header, name):
    for i, h in enumerate(header):
        if name in h:
            return i
    return -1


def fail(msg):
    print(f"FAIL - {msg}")
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/plan.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"usage: file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    if legal_term(text):
        return fail("plan carries legal content; remove it (owner rule)")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    sec = sections(text)
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")

    for name in sec:
        if name not in ALLOWED_SECTIONS:
            return fail(f"section '## {name}' is not part of the plan; fold it into a listed section or cut it")
    words = len(re.findall(r"\S+", sec["summary"]))
    if words > SUMMARY_MAX_WORDS:
        return fail(f"Summary is {words} words; keep it to {SUMMARY_MAX_WORDS}: platform, price, total, one reason")

    hit = AGENT_TOOLS.search(text)
    if hit:
        return fail(f"agent tool call in the plan: {hit.group(0)} (write the dashboard step or the REST call a person runs)")
    for line in text.splitlines():
        if DB_PARAM.search(line) and "/api/" not in line:
            return fail("excludeDelivered named outside a REST call; describe the step, or show the call")
    hit = RULE_CITATION.search(text)
    if hit:
        return fail(f"mailbox-provider rule cited: '{hit.group(0)}'; give the setting and its vendor page")
    if len(ASSUMED_NOTE.findall(text)) > 1:
        return fail("'assumed' notes repeated; say it once under the title and in the Assumptions table")
    hit = WHY_PARA.search(text)
    if hit:
        return fail(f"separate argument paragraph '{hit.group(0)}'; the table and the Decision line carry the choice")
    counts = {}
    for m in CENTS.finditer(text):
        v = m.group(1)
        if num(v) >= 100:
            counts[v] = counts.get(v, 0) + 1
    rep = [v for v, c in counts.items() if c > 2]
    if rep:
        return fail(f"${rep[0]} appears {counts[rep[0]]} times; state each figure once (twice at most)")

    pad = PADDING.search(text)
    if pad:
        return fail(f"padding section in the deliverable: '{pad.group(0).strip()}' (the reader gets the plan, not the checklist)")

    leak = INTERNAL.search(text)
    if leak:
        return fail(f"internal file path or skill name shown to the reader: {leak.group(0)}")

    for m in PRICE_CMP.finditer(text):
        a, d, word, b = num(m.group(1)), num(m.group(2)), m.group(3).lower(), num(m.group(4))
        dearer = word in {"more", "dearer", "higher"}
        if (dearer and a <= b) or (not dearer and a >= b) or abs(abs(a - b) - d) > 0.01:
            return fail(f"price comparison has the wrong direction or gap: {m.group(0)}")

    _, arows = table(sec["assumptions and open questions"])
    current_tool = None
    for topic, rx in ASSUMPTION_TOPICS.items():
        hits = [r for r in arows if r and rx.search(r[0])]
        if not hits or len(hits[0]) < 3 or not hits[0][1].strip() or not hits[0][2].strip():
            return fail(f"Assumptions and Open Questions needs an answered or assumed row for {topic}")
        if topic == "current tool":
            current_tool = hits[0][1]
    has_tool = not NO_TOOL.match(current_tool or "")
    if has_tool and "migration plan" not in sec:
        return fail(f"current tool '{current_tool}' is named, so a '## Migration Plan' section is required")
    if not has_tool and "migration plan" in sec:
        return fail("no current tool is named, so leave out Migration Plan (never invent a migration)")

    ph, prows = table(sec["platform decision"])
    ci = col(ph, "checked")
    if ci < 0 or len(prows) < 2:
        return fail("Platform Decision needs a Checked column and at least 2 options")
    for r in prows:
        if ci >= len(r) or not DATE.search(r[ci]):
            return fail(f"platform option without a vendor-page check date: {r[0]}")
    if not re.search(r"^decision:", sec["platform decision"], re.IGNORECASE | re.MULTILINE):
        return fail("Platform Decision needs a 'Decision:' line")
    if not re.search(r"^revisit if:", sec["platform decision"], re.IGNORECASE | re.MULTILINE):
        return fail("Platform Decision needs a 'Revisit if:' line naming the trigger that changes the choice")
    dline = re.search(r"^decision:.*$", sec["platform decision"], re.IGNORECASE | re.MULTILINE).group(0)
    for m in GAP.finditer(dline):
        gap = m.group(1)
        n = len(re.findall(r"\$" + re.escape(gap) + r"(?![\d.,]*\d)", text))
        if n > 1:
            return fail(f"the ${gap} price gap appears {n} times; state it once, in the Decision line")

    _, wrows = table(sec["workspace settings"])
    caps = [r for r in wrows if r and "per mailbox" in r[0].lower()]
    if not caps:
        return fail("Workspace Settings needs a 'Daily limit per mailbox' row")
    m = re.search(r"\d+", caps[0][1] if len(caps[0]) > 1 else "")
    if not m or int(m.group(0)) >= CAP_LIMIT:
        return fail(f"daily limit per mailbox must be under {CAP_LIMIT} (Alex Berman)")
    if not any(r and "unsubscribe" in r[0].lower() for r in wrows):
        return fail("Workspace Settings needs an unsubscribe header row")
    bounce = [r for r in wrows if r and "bounce" in r[0].lower()]
    if not bounce or len(bounce[0]) < 2 or not re.search(r"\d", bounce[0][1]):
        return fail("Workspace Settings needs a 'Bounce auto-pause' row with the value to type")
    opens = [r for r in wrows if r and "open tracking" in r[0].lower()]
    if not opens or len(opens[0]) < 2 or not re.match(r"\s*off\b", opens[0][1], re.IGNORECASE):
        return fail("Workspace Settings needs an 'Open tracking' row set to Off")

    mh, mrows = table(sec["column map"])
    fi, vi, si = col(mh, "fallback"), col(mh, "platform variable"), col(mh, "source column")
    if min(fi, vi, si) < 0:
        return fail("Column Map needs Source column, Platform variable and Fallback columns")
    if len(mrows) < 4:
        return fail("Column Map needs at least 4 rows")
    has_email = False
    for r in mrows:
        if max(fi, vi, si) >= len(r):
            return fail(f"column map row has too few cells: {' | '.join(r)[:80]}")
        if "email" in r[si].lower() and "email" in r[vi].lower():
            has_email = True
        if not r[fi].strip():
            return fail(f"column map row without a fallback: {r[si]}")
        joined = " ".join(r)
        if joined.count("{{") != joined.count("}}"):
            return fail(f"malformed merge tag in column map row: {r[si]}")
    if not has_email:
        return fail("Column Map needs an email row")

    if OVERRIDE.search(text):
        return fail("an import setting overrides the block list, unsubscribe list or bounce list")

    wh, whrows = table(sec["webhooks to crm"])
    ai = col(wh, "crm action")
    if ai < 0:
        return fail("Webhooks to CRM needs a CRM action column")
    wi = col(wh, "writer")
    if wi < 0:
        return fail("Webhooks to CRM needs a Writer column (native integration or webhook flow, one per event)")
    for r in whrows:
        if wi >= len(r) or not r[wi].strip():
            return fail(f"webhook row without a writer: {r[0]}")
        if re.search(r"\bboth\b", r[wi], re.IGNORECASE):
            return fail(f"event '{r[0]}' has two writers; duplicate notes follow")
    covered = set()
    for r in whrows:
        joined = " ".join(r[: ai])
        for key, rx in NEEDED_EVENTS.items():
            if rx.search(joined):
                covered.add(key)
                if ai >= len(r) or not r[ai].strip() or r[ai].strip().lower() in {"none", "-"}:
                    return fail(f"{key} webhook row has no CRM action")
    missing = set(NEEDED_EVENTS) - covered
    if missing:
        return fail(f"Webhooks to CRM must cover: {', '.join(sorted(missing))}")
    pi = col(wh, "platform event")
    booked = [r for r in whrows if r and re.search(r"meeting booked", r[0], re.IGNORECASE)]
    if not booked:
        return fail("Webhooks to CRM needs a 'Meeting booked' row driven by the calendar booking")
    for r in booked:
        if 0 <= pi < len(r) and REPLY_LABEL.search(r[pi]):
            return fail("Meeting booked is driven by a reply label; a label is a reply, so take the booking from the calendar")
    wtext = sec["webhooks to crm"]
    if not (re.search(r"\bheld\b", wtext, re.IGNORECASE) and re.search(r"no[- ]show", wtext, re.IGNORECASE)):
        return fail("Webhooks to CRM needs Meeting held and No-show from the meeting outcome")
    if not re.search(r"^positive replies:", wtext, re.IGNORECASE | re.MULTILINE):
        return fail("Webhooks to CRM needs a 'Positive replies:' line naming who answers Interested replies")

    mig = sec.get("migration plan", "")
    mh2, migrows = table(mig)
    mdi = col(mh2, "date")
    if has_tool and mdi < 0:
        return fail("Migration Plan table needs a Date column")
    needed = list(MIGRATION_STEPS) if has_tool else []
    for step in needed:
        rows = [r for r in migrows if r and MIGRATION_STEPS[step].search(r[0])]
        if not rows:
            return fail(f"Migration Plan is missing the '{step}' step")
        if mdi >= len(rows[0]) or not DATE.search(rows[0][mdi]):
            return fail(f"Migration Plan '{step}' step needs a date (YYYY-MM-DD) in the Date column")
        if step == "reconnect the same mailboxes" and not re.search(r"same[^.;|]{0,40}mailbox", " ".join(rows[0][1:]), re.IGNORECASE):
            return fail("Migration Plan must reconnect the same mailboxes, not new ones")
        if step == "pre-commitment trial" and not re.search(r"seed|placement", " ".join(rows[0][1:]), re.IGNORECASE):
            return fail("Migration Plan trial must include a placement (seed) test")

    for name, minimum in (("test plan", 4), ("import procedure", 5)):
        th, trows = table(sec[name])
        if len(trows) < minimum:
            return fail(f"{name.title()} needs at least {minimum} rows")
        oi, di = col(th, "owner"), col(th, "due")
        if oi < 0 or di < 0:
            return fail(f"{name.title()} needs Owner and Due columns")
        for r in trows:
            if max(oi, di) >= len(r) or not r[oi].strip():
                return fail(f"{name.title()} row without an owner: {r[0]}")
            if not DATE.search(r[di]):
                return fail(f"{name.title()} row without a due date (YYYY-MM-DD): {r[0]}")
    _, tprows = table(sec["test plan"])
    if not any(r and re.search(r"reconcil", r[0], re.IGNORECASE)
               and re.search(r"deal|crm|hubspot|pipedrive|gohighlevel", " ".join(r), re.IGNORECASE) for r in tprows):
        return fail("Test Plan needs a weekly reconciliation row (sequencer positive replies against CRM deals)")
    if len(table(sec["suppression and dedupe"])[1]) < 3:
        return fail("Suppression and Dedupe needs at least 3 lists")
    cost = sec["cost"]
    if "$" not in cost or not re.search(r"^\|\s*total", cost, re.IGNORECASE | re.MULTILINE):
        return fail("Cost needs dollar figures and a Total row")
    ch, crows = table(cost)
    for name, rx in COST_LINES.items():
        if not any(r and rx.search(r[0]) for r in crows):
            return fail(f"Cost must include a {name} line (full monthly cost, not only the sequencer)")
    mi = col(ch, "monthly")
    total_rows = [r for r in crows if r and r[0].lower().startswith("total")]
    if mi >= 0 and total_rows:
        def money(cell):
            m = MONEY.search(cell)
            return num(m.group(1)) if m else 0.0
        lines = sum(money(r[mi]) for r in crows if r and not r[0].lower().startswith("total") and mi < len(r))
        stated = money(total_rows[0][mi]) if mi < len(total_rows[0]) else 0.0
        if abs(lines - stated) > 0.05:
            return fail(f"Cost Total ${stated:,.2f} does not equal the sum of its lines ${lines:,.2f}")
    inbox_rows = [r for r in arows if r and ASSUMPTION_TOPICS["inbox mix"].search(r[0])]
    already = bool(inbox_rows) and len(inbox_rows[0]) > 1 and ALREADY.search(inbox_rows[0][1])
    if already:
        mrow = [r for r in crows if r and COST_LINES["mailboxes"].search(r[0])]
        if not re.search(r"existing|reconnect", " ".join(mrow[0]), re.IGNORECASE):
            return fail("the user already sends: label the mailbox line existing (reconnected, no purchase)")
        if not has_tool:
            ip = sec["import procedure"]
            for label, rx in (("old tool's unsubscribes and bounces loaded first", r"unsubscri"),
                              ("mid-sequence prospects finish on the old tool", r"mid-sequence|finish"),
                              ("warmup on in one tool at a time", r"warmup")):
                if not re.search(rx, ip, re.IGNORECASE):
                    return fail(f"the user already sends from an unnamed tool: Import Procedure needs the switch step '{label}'")
    _, rrows = table(sec["requirements"])
    cw = [r for r in rrows if r and "client workspace" in r[0].lower()]
    if not cw:
        return fail("Requirements needs a 'Client workspaces' row (0 for in-house)")
    m = re.search(r"\d+", cw[0][1] if len(cw[0]) > 1 else "")
    if m is None:
        return fail("Client workspaces row needs a number")
    clients = int(m.group(0))
    if clients > 0:
        rows = [" ".join(r) for r in crows if r and "workspace" in r[0].lower()]
        if not any(re.search(r"\d+\s*x\s*\$?\d", r) for r in rows):
            return fail("agency plan: Cost needs a workspace line priced as workspaces x clients")
        if "per client" not in sec["suppression and dedupe"].lower():
            return fail("agency plan: Suppression and Dedupe needs per client block lists")
        if not CLIENT_ROUTING.search(sec["webhooks to crm"]):
            return fail("agency plan: Webhooks to CRM must say how each event reaches the right client (client-level webhook or one workspace per client)")

    print(f"PASS - {len(prows)} dated platform options, {len(mrows)} mapped columns with fallbacks, one writer per webhook event, owners and dates on every step, full monthly cost, {'agency with ' + str(clients) + ' clients, ' if clients else ''}{'migration steps dated' if has_tool else 'no migration (no current tool)'}, no internal paths or padding")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
