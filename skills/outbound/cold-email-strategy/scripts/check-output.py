#!/usr/bin/env python3
"""Check a cold email campaign plan produced with the cold-email-strategy skill.

Usage: check-output.py path/to/plan.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import datetime
import re
import sys

REQUIRED = [
    "Campaign Summary",
    "Offer",
    "Campaign Cells",
    "Contact Thesis",
    "List Sources and Cost",
    "Touch Map",
    "Email Copy",
    "Sequencer Settings",
    "Volume and Funnel",
    "Test Plan",
    "List and Sender Rules",
    "Owners and Controls",
    "Launch Calendar",
    "Assumptions and Open Questions",
    "Sources",
]
# Sections that pad the plan instead of running it.
BANNED_SECTIONS = ("handoff", "quality check", "frameworks", "sources and frameworks", "measurement funnel")
MIN_WORDS = 600
MIN_TABLE_ROWS = 25
MAX_CELLS = 3  # cells that launch inside the calendar; later cells get one "Next cells" line
MAX_CALENDAR_DAYS = 92  # the calendar covers the first 90 days
MAX_BODY_WORDS = 100  # Alex Berman's B2B lead generation page: under 100 words, one observation, one question
MAX_ASSUMED_TAGS = 2  # assumptions live in one list, not as "(assumed)" on every row
MAX_ANSWER_WORDS = 45  # the Answer row is one sentence; the numbers live in the funnel table
MAX_GATE_WORDS = 35  # the go/no-go row is the verdict and the break-even; its inputs sit under the funnel
# A trigger with a freshness window goes stale in a queue, so it launches with the first cell.
DATED_TRIGGER = re.compile(r"\bwithin (?:the last )?\d+ days|\blast \d+ days|\b\d+-day window|\bposted\b|\bposting\b", re.IGNORECASE)
# The positive reply asks for a time only; documents and uploads come after the call is booked.
ASKS_FOR_WORK = re.compile(r"\bupload|\battach|\bsend (?:us|me|over)\b|\bstatements?\b|\breports?\b", re.IGNORECASE)
# Phrases that state a rest, cooldown or re-enrollment period. Every match must carry the same number.
COOLDOWN = [
    re.compile(r"\brests?\s+(?:for\s+)?(\d+)\s*days", re.IGNORECASE),
    re.compile(r"\bsuppress(?:ed|es)?\s+(?:for\s+)?(\d+)\s*days", re.IGNORECASE),
    re.compile(r"\b(\d+)[- ]day\s+(?:rest|cooldown|cool-down|suppression)", re.IGNORECASE),
    re.compile(r"\b(?:cooldown|cool-down)\D{0,20}?(\d+)\s*days", re.IGNORECASE),
    re.compile(
        r"\b(?:re-?enrol\w*|re-?enter\w*|re-?mail\w*|re-?sequenc\w*|new sequence|next cycle)"
        r"[^.;|\n]{0,40}?\b(?:after|every|at least|wait(?:ing)?)\s+(\d+)\s*days",
        re.IGNORECASE,
    ),
    re.compile(r"\bevery\s+(\d+)\s*(?:to\s+\d+\s*)?days?\s*(?:with\s+)?(?:fresh|new)\s+copy", re.IGNORECASE),
]
DATE = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b")
# Owner rule: a plan carries no legal content. Laws, regulators, legal citations and
# legal disclaimers fail the plan (same list as validate-skills.py --check-legal).
LEGAL = re.compile(
    r"\b(can.?spam|tc[p]a|casl|gd[p]r|ccpa|cpra|pecr|fcra|hipaa|ferpa|glba|dppa|tsr|telemarketing sales rule|"
    r"ftc|fcc|crtc|ico|cfpb|attorn[e]ys? general|\d+\s*c\.?f\.?r|u\.s\.c|lawful\s+basis|legal\s+advice|not\s+legal|"
    r"lawy[e]rs?|attorn[e]ys?|counsel|do.?not.?call\s+registry|compliance|regulat\w*|statute|consent|penalt\w+|"
    r"business associate|baa)\b",
    re.IGNORECASE,
)
# The reader gets the plan, not the agent's plumbing: no tool ids, no skill ids, no code blocks.
TOOL_ID = re.compile(r"\b(check_wallet|query_\w+|scrape_\w+|find_(?:emails|mobiles|people)|validate_emails|pagination\.\w+|excludeDelivered|limit=1)\b")
SKILL_ID = re.compile(
    r"\b(cold-email-copywriting|cold-email-strategy|reply-handling|sending-platforms|domain-infrastructure|inbox-setup|"
    r"email-deliverability|multi-channel-outreach|outbound-unit-economics|signal-triggered-outbound|icp-list-builder|"
    r"local-business-list|ecommerce-by-techstack|email-list-cleaner)\b|\brun cold-calling\b",
    re.IGNORECASE,
)
# Rules are stated directly; trainer and framework name-drops are padding to a buyer.
NAME_DROP = re.compile(
    r"\b(Berman|Nowoslawski|Venetz|Becc Holland|Crawford|Dunford|Craig Elias|Nilsson|SPIN (?:Problem|Implication|Need)|"
    r"Earn the Right|Pain-Qualified|PQS|PVP)\b"
)
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)


def sections(text):
    out = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = m.group(1).strip().lower()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def tables(block):
    """Return a list of tables; each table is a list of dicts keyed by lowercased header."""
    result, rows = [], []
    for line in block.splitlines() + [""]:
        if line.strip().startswith("|"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif rows:
            if len(rows) >= 2 and all(re.fullmatch(r":?-+:?", c) for c in rows[1] if c):
                head = [h.lower() for h in rows[0]]
                result.append([dict(zip(head, r)) for r in rows[2:]])
            rows = []
    return result


def headers(block):
    """Lowercased header cells of every table in a block."""
    out = []
    lines = block.splitlines()
    for i, line in enumerate(lines[:-1]):
        if line.strip().startswith("|") and re.fullmatch(r"\|?(\s*:?-+:?\s*\|)+\s*:?-*:?\s*\|?", lines[i + 1].strip()):
            if i == 0 or not lines[i - 1].strip().startswith("|"):
                out.append([c.strip().lower() for c in line.strip().strip("|").split("|")])
    return out


def first_number(value):
    """Number after the first '=' if present, else the first number in the cell."""
    part = value.split("=", 1)[1] if "=" in value else value
    m = re.search(r"\d[\d,]*(?:\.\d+)?", part)
    return float(m.group(0).replace(",", "")) if m else None


def emails(block):
    """Each email in Email Copy: a 'Subject:' line, then its body as '>' quote lines."""
    out, lines = [], block.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s*subject:", line, re.IGNORECASE):
            body = []
            for nxt in lines[i + 1:]:
                if nxt.strip().startswith(">"):
                    body.append(nxt.strip().lstrip(">").strip())
                elif nxt.strip() == "" and not body:
                    continue
                elif nxt.strip() == "" and body:
                    continue
                else:
                    break
            out.append((line.strip(), [b for b in body if b]))
    return out


def fail(msg):
    print(f"FAIL - {msg}")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/plan.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the plan: {hit.group(0)}")
    legal = LEGAL.search(text)
    if legal:
        fail(f"plan contains legal content ('{legal.group(0)}'); state the setting and the result it protects instead")

    # Economy: the reader gets the plan only.
    if "```" in text:
        fail("plan contains a code block; write list pulls as plain steps or calendar rows")
    for rx, label in ((TOOL_ID, "a tool id or API syntax"), (SKILL_ID, "an internal skill id"), (NAME_DROP, "a trainer or framework name-drop")):
        m = rx.search(text)
        if m:
            fail(f"plan contains {label} ('{m.group(0)}'); state the step or rule in plain words")
    heads = [h.strip().lower() for h in re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
    for h in heads:
        if h in BANNED_SECTIONS:
            fail(f"section '## {h}' is padding; copy, reply text and settings belong in the plan itself")
    dupes = sorted({h for h in heads if heads.count(h) > 1})
    if dupes:
        fail(f"duplicate section heading(s): {', '.join(dupes)}")
    not_checked = [i for i, line in enumerate(text.splitlines()) if re.search(r"\bnot checked\b|\bnothing was run\b|\bnone were run\b", line, re.IGNORECASE)]
    if len(not_checked) > 1:
        fail("say what was not checked once, in one line at the top")
    if not_checked and not_checked[0] > 8:
        fail("the one 'Not checked:' line goes at the top of the plan, before the first section")
    for rx, label in (
        (re.compile(r"offer strength score|score \(0 to \d\)", re.IGNORECASE), "a self-scoring row"),
        (re.compile(r"\ballows?\s+\d+\s+(?:business\s+)?days\b", re.IGNORECASE), "a looser outside limit next to the plan's own setting"),
    ):
        m = rx.search(text)
        if m:
            fail(f"plan contains {label} ('{m.group(0)}'); cut it")
    assumed = len(re.findall(r"\(assumed\b|\bassumed\)", text, re.IGNORECASE))
    if assumed > MAX_ASSUMED_TAGS:
        fail(f"'(assumed)' appears {assumed} times; list each assumption once under Assumptions and Open Questions")

    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    words = len(text.split())
    if words < MIN_WORDS:
        fail(f"plan has {words} words, minimum is {MIN_WORDS}")
    all_rows = [r for t in tables(text) for r in t]
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"plan has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    # Skill check 1: every campaign cell has a segment, an offer and a trigger; only cells inside the calendar.
    cell_rows = [r for t in tables(secs["campaign cells"]) for r in t]
    if not cell_rows:
        fail("Campaign Cells has no table rows")
    if len(cell_rows) > MAX_CELLS:
        fail(f"Campaign Cells has {len(cell_rows)} rows; keep the cells that launch inside the 90-day calendar (at most {MAX_CELLS}) and give later ones one 'Next cells' line")
    for r in cell_rows:
        for col in ("segment", "offer", "trigger"):
            if not r.get(col):
                fail(f"campaign cell '{r.get('cell', '?')}' has no {col}")
    launches = {}
    for r in cell_rows:
        m = DATE.search(r.get("launch", ""))
        if m:
            launches[r.get("cell", "?")] = m.group(0)
    if launches:
        first_launch = min(launches.values())
        for r in cell_rows:
            if DATED_TRIGGER.search(r.get("trigger", "")) and launches.get(r.get("cell", "?"), first_launch) != first_launch:
                fail(f"cell '{r.get('cell', '?')}' has a dated trigger but launches after the first cell; launch it on {first_launch} sharing the inboxes")

    # Skill check 2: every touch row has a branch; every reply routing row has an owner, an SLA and, for replies a person answers, the reply text.
    touch_rows, route_rows = [], []
    for t in tables(secs["touch map"]):
        if t and "event" in t[0]:
            route_rows.extend(t)
        else:
            touch_rows.extend(t)
    if len(touch_rows) < 3:
        fail("Touch Map needs at least 3 touch rows")
    for r in touch_rows:
        if "branch" not in r or len(r["branch"]) < 5:
            fail(f"touch '{r.get('touch', '?')}' has no branch")
    call_rows = [r for r in touch_rows if "call" in r.get("touch", "").lower()]
    cell_ids = {r.get("cell", "").strip() for r in cell_rows if r.get("cell", "").strip()}
    for r in call_rows:
        covered = {c.strip() for c in re.split(r"[,;]|\band\b", r.get("cell", "")) if c.strip()}
        if "all" not in r.get("cell", "").lower() and not cell_ids <= covered:
            fail(f"the call touch covers cells {sorted(covered)} but the plan has {sorted(cell_ids)}; call every cell with a listed main number")
    if len(route_rows) < 4:
        fail("Touch Map needs a reply routing table (Event, Action, Owner, SLA) with at least 4 events")
    for r in route_rows:
        if not r.get("owner", "").strip() or not r.get("sla", "").strip():
            fail(f"reply routing row '{r.get('event', '?')}' needs an owner and an SLA")
        if re.search(r"positive|info|price|not interested|referral|vendor|competitor", r.get("event", ""), re.IGNORECASE):
            if '"' not in r.get("action", ""):
                fail(f"reply routing row '{r.get('event', '?')}' needs the reply text written out in quotes")
        if "positive" in r.get("event", "").lower():
            if ASKS_FOR_WORK.search(r.get("action", "")):
                fail("the positive reply asks the prospect for work before the call; ask for a time only and request anything else after it is booked")
            if not re.search(r"\bminutes?\b", r.get("sla", ""), re.IGNORECASE):
                fail("the positive reply SLA must be in minutes during business hours (alexberman.com follow-up guide: within 5 minutes)")

    # Skill check 3: every email touch is written out: subject, body under the word cap, ending on a question; one opt-out line.
    email_touches = [r for r in touch_rows if re.fullmatch(r"\d+", r.get("touch", "").strip())]
    copy = secs["email copy"]
    mails = emails(copy)
    if len(mails) < len(email_touches):
        fail(f"Email Copy has {len(mails)} emails for {len(email_touches)} email touches; write every touch in full ('Subject:' line, then the body as '>' lines)")
    for subject, body in mails:
        if not body:
            fail(f"'{subject}' has no body ('>' lines under the subject)")
        n = len(" ".join(body).split())
        if n > MAX_BODY_WORDS:
            fail(f"'{subject}' body has {n} words; keep it under {MAX_BODY_WORDS}")
        if not body[-1].rstrip().endswith("?"):
            fail(f"'{subject}' must end on one question")
    if not re.search(r"opt-?out|unsubscribe|no thanks", copy, re.IGNORECASE):
        fail("Email Copy must state the opt-out line every email carries")
    if not re.search(r"^\s*(?:\*\*)?signature(?:\*\*)?:", copy, re.IGNORECASE | re.MULTILINE):
        fail("Email Copy must write out the signature block ('Signature: ...')")

    # Skill check 4: one sequencer, with its exact settings.
    seq_rows = [r for t in tables(secs["sequencer settings"]) for r in t]
    seq = secs["sequencer settings"].lower()
    if len(seq_rows) < 6:
        fail("Sequencer Settings needs at least 6 settings rows for the one platform the plan uses")
    for needed, label in (("limit", "the daily limit"), ("ramp", "the ramp"), ("reply", "stop on reply"), ("unsubscribe", "the unsubscribe header"), ("bounce", "the bounce auto-pause")):
        if needed not in seq:
            fail(f"Sequencer Settings needs {label}")
    if not re.search(r"another sequencer|already (?:uses?|pays? for|on)|other sequencer", seq):
        fail("Sequencer Settings needs one line for a team already on another sequencer (same values, that tool's option names)")
    if not re.search(r"limits? by hand|manual(?:ly)? (?:raise|set)", seq):
        fail("Sequencer Settings needs a by-hand fallback for the ramp if the option label differs")

    # Skill check 5: the offer sentence is concrete (carries a number).
    offer_line = re.search(r"^offer sentence:(.*)$", secs["offer"], re.IGNORECASE | re.MULTILINE)
    if not offer_line:
        fail("Offer needs an 'Offer sentence:' line")
    result = re.search(r"\bget\b(.+?)\bby\b", offer_line.group(1), re.IGNORECASE)
    if not re.search(r"\d", result.group(1) if result else offer_line.group(1)):
        fail("the offer's result ('get ... by') needs a number, from a measured client result")

    # Skill check 6: cost section carries a dollar total and a dated price source.
    cost = secs["list sources and cost"]
    if not re.search(r"total[^\n]*\$\d", cost, re.IGNORECASE):
        fail("List Sources and Cost needs a Total row with a $ figure")
    if not re.search(r"(checked|as of)\s+20\d\d-\d\d-\d\d", cost, re.IGNORECASE):
        fail("List Sources and Cost needs one line naming where the prices come from and the date they were checked")
    if re.search(r"sending stack", cost, re.IGNORECASE) or not re.search(r"\bseats?\b", cost, re.IGNORECASE):
        fail("List Sources and Cost must itemize the sending stack: sequencer plan, inbox seats and domains, each priced")

    # Skill check 7: tests never decide on opens; every test has a read date.
    for r in [r for t in tables(secs["test plan"]) for r in t]:
        metric = r.get("decision metric", "").lower()
        if not metric:
            fail("every test needs a decision metric")
        if "open" in metric:
            fail(f"test '{r.get('test', '?')}' decides on opens; use positive replies per 100 delivered")
        if not DATE.search(r.get("read on", "")):
            fail(f"test '{r.get('test', '?')}' needs a 'Read on' date (YYYY-MM-DD)")

    # Skill check 8: a unit economics go/no-go row with a decision and a number.
    gate = None
    for r in [r for t in tables(secs["campaign summary"]) for r in t]:
        vals = list(r.values())
        if vals and "go/no-go" in vals[0].lower():
            gate = vals[1] if len(vals) > 1 else ""
    if gate is None:
        fail("Campaign Summary needs a 'Unit economics go/no-go' row")
    if not re.match(r"\s*(go|test|no-go)\b", gate, re.IGNORECASE) or not re.search(r"\d", gate):
        fail("the go/no-go row must start with Go, Test or No-go and show the break-even number")
    if len(gate.split()) > MAX_GATE_WORDS:
        fail(f"the go/no-go row has {len(gate.split())} words; give the verdict and break-even in {MAX_GATE_WORDS} or fewer and put the inputs under the funnel")
    answer = next((list(r.values())[1] for r in [r for t in tables(secs["campaign summary"]) for r in t] if list(r.values())[0].lower().startswith("answer") and len(r) > 1), None)
    if answer is None:
        fail("Campaign Summary needs an 'Answer' row first")
    if len(answer.split()) > MAX_ANSWER_WORDS or len(re.findall(r"[.!?](?:\s|$)", answer.strip())) > 1:
        fail(f"the Answer row must be one sentence of {MAX_ANSWER_WORDS} words or fewer")

    # Skill check 9: one rest/cooldown value across the whole plan.
    found = []
    for rx in COOLDOWN:
        for m in rx.finditer(text):
            found.append((int(m.group(1)), m.group(0).strip()))
    rules = secs["list and sender rules"]
    if not any(rx.search(rules) for rx in COOLDOWN):
        fail("List and Sender Rules must state the rest rule with a number of days (for example 'rest 60 days')")
    values = sorted({v for v, _ in found})
    if len(values) > 1:
        first = {}
        for v, p in found:
            first.setdefault(v, p)
        examples = "; ".join(f"{v}: '{p}'" for v, p in sorted(first.items()))
        fail(f"rest/cooldown periods disagree ({', '.join(map(str, values))} days): {examples}")

    # Skill check 10: list and sender rules: tracker, new angle, unsubscribe, one suppression list, authentication; no Source column.
    low = rules.lower()
    for needed, label in (
        ("not-yet-reached", "a not-yet-reached tracker"),
        ("new angle", "re-enrollment only with a new angle"),
        ("unsubscribe", "unsubscribe handling"),
        ("suppression", "the one suppression list"),
        ("dkim", "authentication (SPF, DKIM, DMARC)"),
    ):
        if needed not in low:
            fail(f"List and Sender Rules needs {label}")
    for head in headers(rules):
        if "source" in head:
            fail("List and Sender Rules has a Source column; state each rule as a setting, with a source in parentheses only for a number")

    # Skill check 10b: a new sending domain comes with its record values.
    cal_text = secs["launch calendar"].lower()
    if re.search(r"\bregister\b", cal_text) and not ("v=spf1" in low and "v=dmarc1" in low):
        fail("the plan registers a domain; List and Sender Rules must give the record values (v=spf1 ..., v=DMARC1 ...)")

    # Skill check 11: owners, backup and pause rights are named; personalization check stated.
    own_rows = [r for t in tables(secs["owners and controls"]) for r in t]
    for role in ("campaign owner", "backup", "pause"):
        hit = [r for r in own_rows if role in list(r.values())[0].lower()]
        if not hit or not hit[0].get("name", "").strip():
            fail(f"Owners and Controls needs a named '{role}' row")
    own = secs["owners and controls"].lower()
    # About 10 hand-written examples before any AI output (Eric Nowoslawski, via alexberman.com).
    if not re.search(r"\b10\b[^.\n]{0,60}hand-?writ|hand-?writ[^.\n]{0,60}\b10\b", own) or not re.search(r"\bai\b[^.\n]{0,40}(dry run|line)|(read|review)\w*[^.\n]{0,40}\bai\b", own):
        fail("Owners and Controls must say who hand-writes the first 10 lines and who reviews the AI-written lines")

    # Skill check 12: capacity shows its inputs, the ramp and the goal result in one funnel table.
    vol = secs["volume and funnel"]
    cap = vol.lower()
    for needed in ("inbox", "per day", "total sends"):
        if needed not in cap:
            fail(f"Volume and Funnel is missing '{needed}'")
    cap_rows = {}
    for r in [r for t in tables(vol) for r in t]:
        vals = list(r.values())
        if len(vals) >= 2:
            cap_rows[vals[0].lower()] = vals[1:]
    daily = next((first_number(v[0]) for k, v in cap_rows.items() if "daily capacity" in k), None)
    cells = next((first_number(v[0]) for k, v in cap_rows.items() if "cells launched" in k), None)
    if daily is None or cells is None:
        fail("Volume and Funnel needs 'Daily capacity' and 'Cells launched at once' rows with numbers")
    if cells < 1:
        fail("Volume and Funnel must launch at least one cell")
    if not any("ramp" in k for k in cap_rows):
        fail("Volume and Funnel needs a 'Ramp' row: first cold sends per inbox and how they climb to the steady limit")
    if not any(k.startswith("goal") for k in cap_rows) or not any("held" in k for k in cap_rows) or not any("positive" in k for k in cap_rows):
        fail("Volume and Funnel needs one funnel table with positive replies, meetings held and a 'Goal' row")
    if "goal met" not in cap and "shortfall" not in cap:
        fail("Volume and Funnel must say 'goal met' or name the shortfall and its fix")

    # Skill check 13: launch calendar rows carry a date and an owner, inside the first 90 days.
    cal_rows = [r for t in tables(secs["launch calendar"]) for r in t]
    if len(cal_rows) < 5:
        fail("Launch Calendar needs at least 5 dated tasks")
    days = []
    for r in cal_rows:
        m = DATE.search(r.get("date", ""))
        if not m or not r.get("owner", "").strip():
            fail(f"launch task '{r.get('task', '?')}' needs a YYYY-MM-DD date and an owner")
        days.append(datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    span = (max(days) - min(days)).days
    if span > MAX_CALENDAR_DAYS:
        fail(f"Launch Calendar spans {span} days; cover the first 90 days and put later steps in one 'Next cells' line")

    if re.search(r"\{\{\s*\w*link\w*\s*\}\}", text, re.IGNORECASE) and "link" not in cal_text:
        fail("the copy uses a link merge tag; the Launch Calendar needs the row that sets up that link")

    # Skill check 14: assumptions are listed.
    assum = secs["assumptions and open questions"]
    items = len(re.findall(r"^\s*[-*]\s+\S", assum, re.MULTILINE)) + len([r for t in tables(assum) for r in t])
    if items < 2:
        fail("Assumptions and Open Questions needs at least 2 items")

    # Skill check 15: every outside source is listed once with its URL.
    if len(re.findall(r"https?://\S+", secs["sources"])) < 2:
        fail("Sources must list each outside source once with its URL")

    rest = f"rest {values[0]} days" if values else "rest rule"
    print(f"PASS - {len(cell_rows)} cells, {len(touch_rows)} touches with branches, {len(mails)} emails written, {len(route_rows)} routing rows, {len(seq_rows)} sequencer settings, {rest} consistent, capacity {daily:g} a day with {cells:g} cell(s) live, {len(cal_rows)} dated tasks over {span} days, {len(all_rows)} table rows, {words} words")
    sys.exit(0)


if __name__ == "__main__":
    main()
