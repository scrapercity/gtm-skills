#!/usr/bin/env python3
"""Check a reply handling deliverable produced with the reply-handling skill.

Two formats: a reply triage (has a '## Reply Triage' section) for pasted replies,
or a full playbook (has '## Inbox Setup').

Usage: check-output.py path/to/deliverable.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import re
import sys

REQUIRED = [
    "Inbox Setup",
    "Reply Taxonomy",
    "Response Library",
    "SLAs",
    "CRM State Map",
    "Suppression Rules",
    "Auto-Reply Detection",
    "Automation Boundaries",
    "Referral Capture",
    "Weekly Review",
]
MUST_HAVE_CLASSES = ["interested", "referral", "objection", "not now", "unsubscribe", "out of office", "bounce", "wrong person", "hostile"]
NO_REPLY_CLASSES = ["unsubscribe", "bounce", "hostile"]
HOSTILE_WORDS = re.compile(r"\b(spam|spamming|report|reported|reporting|lawyer|attorney|sue|lawsuit|cease and desist|harass\w*)\b", re.IGNORECASE)
HOSTILE_CLASS = re.compile(r"hostile|needs review", re.IGNORECASE)
# Deliverables carry no legal content (owner rule, 2026-10-13). Same terms as the repo's
# validate-skills.py --check-legal list; one letter of each term sits in brackets so this
# file does not itself name a law or regulator. Reply-classification words (lawyer,
# attorney, sue) stay allowed: they are hostile trigger words this skill routes.
LEGAL_TERMS = [
    r"c[a]n[- ]?spam", r"\bt[c]pa\b", r"telephone consumer pro[t]ection", r"\bc[a]sl\b", r"anti-spam legi[s]lation",
    r"\bg[d]pr\b", r"general data pro[t]ection", r"\bepri[v]acy\b", r"lawful bas[i]s", r"legitimate interests? asse[s]sment",
    r"\bc[c]pa\b", r"\bc[p]ra\b", r"california consumer pri[v]acy", r"\bp[e]cr\b", r"privacy and electronic com[m]unications",
    r"\bf[c]ra\b", r"fair credit rep[o]rting", r"\bt[s]r\b", r"telemarketing sales r[u]le", r"\b(?:4[7]|1[6])\s*c\.?f\.?r\b",
    r"\b(?:f[t]c|f[c]c|c[r]tc|i[c]o)\b", r"federal trade com[m]ission", r"federal communications com[m]ission",
    r"information com[m]issioner", r"att[o]rneys? gen[e]ral", r"legal ad[v]ice", r"\bnot le[g]al\b",
    r"(?:consult|check with|speak with|talk to) (?:a|an|your) (?:\w+ )?(?:law[y]er|att[o]rney|coun[s]el)",
    r"do[- ]not[- ]call reg[i]stry", r"nati[o]nal do[- ]not[- ]call", r"donotcall\.g[o]v", r"compliance ga[t]es?",
    r"\bsta[t]ute", r"\bpenalt[i]", r"legal lim[i]t",
]
LEGAL = re.compile("|".join(LEGAL_TERMS), re.IGNORECASE)
PADDING = re.compile(r"templates page|references/|SKILL\.md|check-output|framework-notes", re.IGNORECASE)
SUBJECT = re.compile(r"^\s*subject:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
MAX_RESPONSE_WORDS = 75  # Berman's templates page: cut any cold email over 75 words
MIN_WORDS = 700
MIN_TABLE_ROWS = 40
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
TIME_LIMIT = re.compile(r"\d+\s*(business\s+)?(minute|minutes|hour|hours|day|days)\b|same\s+(business\s+)?day", re.IGNORECASE)
THRESHOLD = re.compile(r"\b0\.\d{1,2}\b|\b\d{2}\s*%")
AUTO_ALLOWED = ["out of office", "unsubscribe"]
DEADLINE = re.compile(r"\d+\s*(business\s+)?(day|days|hour|hours)", re.IGNORECASE)
MERGE = re.compile(r"\{\{([^{}]*)\}\}")
DURATION = re.compile(r"(\d+)\s*(?:business\s+)?(minute|minutes|min|hour|hours|day|days)\b", re.IGNORECASE)
HOT_SLA_MINUTES = 5  # Berman's follow-up guide: get back to an interested reply within 5 minutes
TRIAGE_SECTIONS = {"reply triage", "drafts", "routing and slas", "open items"}
MAX_OPEN_ITEMS = 5  # format rule: Open Items carries only missing inputs and one Confirm line
FENCE = re.compile(r"```.*?```", re.DOTALL)
TOOL_ID = re.compile(r"\b(?:find_emails|validate_emails|query_lead_database|find_mobiles|check_wallet|[a-z]+_[a-z]+_[a-z_]+)\b|```json", re.IGNORECASE)
LOOKUP_PRICE = re.compile(r"\bunder a cent\b|\ba few cents\b|\bper (?:email|lookup|number|search) found\b|\$\d+(?:\.\d+)? per (?:email|lookup|number)", re.IGNORECASE)
PROCESS_TALK = re.compile(r"no tools were|nothing was run|not yet returned|marked assumed|assumed result|the skill(?:'s)? |intake asks|quality check", re.IGNORECASE)
RATIONALE = re.compile(r"\bbecause\b|looks automated|draws complaints|gets reported|annoy", re.IGNORECASE)


def is_hot(cls):
    c = cls.lower()
    return bool(re.search(r"(?<!not )interested", c)) or "accepted" in c or "price question" in c


def minutes(cell):
    """Longest duration named in an SLA cell, in minutes; None if no number is given."""
    found = DURATION.findall(cell)
    if not found or re.search(r"same\s+(business\s+)?day|next\s+(business\s+)?day", cell, re.IGNORECASE):
        return None if not found else float("inf")
    unit = {"min": 1, "minute": 1, "minutes": 1, "hour": 60, "hours": 60, "day": 1440, "days": 1440}
    return max(int(n) * unit[u.lower()] for n, u in found)


def drafts(block):
    """(heading, body) for every fenced draft under a ### heading in the Response Library."""
    out = []
    for part in re.split(r"^###\s+", block, flags=re.MULTILINE)[1:]:
        head, _, rest = part.partition("\n")
        for body in re.findall(r"```[a-z]*\n(.*?)```", rest, re.DOTALL):
            out.append((head.strip(), body))
    return out


def fail(msg):
    print(f"FAIL - {msg}")
    sys.exit(1)


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


def table_rows(block):
    rows = []
    lines = [l.strip() for l in block.splitlines()]
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", lines[i + 1]):
            head = [h.strip().lower() for h in line.strip("|").split("|")]
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(dict(zip(head, [c.strip() for c in lines[j].strip("|").split("|")])))
                j += 1
    return rows


def covers(rows, key, cls):
    return [r for r in rows if cls in r.get(key, "").lower()]


def body_words(body):
    """Words in a draft, not counting a Subject line."""
    return len(SUBJECT.sub("", body).split())


def check_draft(body):
    n = body_words(body)
    if n > MAX_RESPONSE_WORDS:
        fail(f"a response has {n} words; keep every response to {MAX_RESPONSE_WORDS} or fewer: '{body.strip()[:50]}...'")
    for field in MERGE.findall(body):
        name, _, fallback = field.partition("|")
        if not fallback.strip():
            fail(f"merge field '{{{{{name.strip()}}}}}' in a draft has no fallback: '{body.strip()[:50]}...'")
    if "[" in MERGE.sub("", body):
        fail(f"a draft contains a '[' placeholder; drafts must be sendable as written: '{body.strip()[:50]}...'")


def check_referral_subject(found):
    """found: list of (heading, body) for referral first emails."""
    for head, body in found:
        m = SUBJECT.search(body)
        if not m:
            fail(f"referral first email '{head}' needs a Subject line that names the referrer")
        subj = m.group(1)
        if not (re.search(r"\{\{referrer", subj) or re.search(r"suggest|pointed|referr|sent me|asked me|told me", subj, re.IGNORECASE)):
            fail(f"referral subject '{subj.strip()}' should name the referrer, for example 'Tom suggested I reach out'")


def triage(text, secs):
    for name in ["Reply Triage", "Drafts", "Open Items"]:
        if name.lower() not in secs:
            fail(f"triage is missing section '## {name}'")
    extra = [k for k in secs if k not in TRIAGE_SECTIONS]
    if extra:
        fail(f"triage has a section the format does not allow: '## {extra[0]}'; keep Reply Triage, Drafts, Routing and SLAs (if asked) and Open Items")
    prose = FENCE.sub("", MERGE.sub("", text))
    for pattern, why in [(TOOL_ID, "a tool id or JSON call block"), (LOOKUP_PRICE, "a per-lookup price"),
                         (PROCESS_TALK, "a note about the process"), (RATIONALE, "a justification after a setting")]:
        hit = pattern.search(prose)
        if hit:
            fail(f"triage contains {why} ('{hit.group(0)}'); state the setting only")
    for row in table_rows(text):
        if "reason" in row or "why" in row:
            fail("triage has a Reason column; state settings without their rationale")
    bullets = [l for l in secs["open items"].splitlines() if re.match(r"\s*[-*]\s", l)]
    if len(bullets) > MAX_OPEN_ITEMS:
        fail(f"Open Items has {len(bullets)} bullets; keep it to {MAX_OPEN_ITEMS}: missing facts and one 'Confirm:' line")
    rows = table_rows(secs["reply triage"])
    if not rows:
        fail("Reply Triage has no table rows")
    need = ["#", "reply", "class", "send", "within", "crm status", "suppress"]
    missing = [c for c in need if c not in rows[0]]
    if missing:
        fail(f"Reply Triage table is missing columns: {', '.join(missing)}")
    found = {}
    for part in re.split(r"^###\s+", secs["drafts"], flags=re.MULTILINE)[1:]:
        head, _, rest = part.partition("\n")
        num = re.match(r"(\d+)", head.strip())
        bodies = re.findall(r"```[a-z]*\n(.*?)```", rest, re.DOTALL)
        if num and bodies:
            found.setdefault(num.group(1), []).append((head.strip(), bodies[0]))
    referral = []
    has_bounce = False
    for r in rows:
        n, cls, send, within = r["#"].strip(), r["class"], r["send"].lower(), r["within"].lower()
        has_bounce = has_bounce or "bounce" in cls.lower()
        sends_draft = "draft" in send or "removal line" in send
        if send.startswith("no reply") and n in found:
            fail(f"row {n} says No reply but a draft exists for it; pick one")
        if sends_draft and n not in found:
            fail(f"row {n} sends a draft but '## Drafts' has no '### {n}.' draft")
        if "no sales reply" in send:
            fail(f"row {n} says 'no sales reply'; write 'No reply' or 'Removal line (draft {n})'")
        if HOSTILE_WORDS.search(r["reply"]) and not HOSTILE_CLASS.search(cls) and "reviewed" not in cls.lower():
            fail(f"row {n} contains a hostile trigger word; class it Hostile so no automation replies")
        if HOSTILE_CLASS.search(cls) and re.search(r"(?<!not )(?<!never )(?<!no )automat", send + " " + within):
            fail(f"row {n} is hostile; a person acts, never automation")
        if HOSTILE_CLASS.search(cls) or "unsubscribe" in cls.lower():
            if not r["suppress"].lower().startswith("yes"):
                fail(f"row {n} ({cls}) must be suppressed")
        if is_hot(cls):
            took = minutes(r["within"])
            if took is None or took > HOT_SLA_MINUTES:
                fail(f"hot row {n} ({cls}) must be answered within {HOT_SLA_MINUTES} minutes")
        if "referr" in cls.lower():
            new_thread = [d for d in found.get(n, []) if SUBJECT.search(d[1]) or "referred" in d[0].lower()]
            if not new_thread:
                fail(f"row {n} is a referral; add the first email to the referred person ('### {n}b. Name, referred') with a Subject line")
            referral.extend(new_thread)
        if "price" in cls.lower() and not any(re.search(r"depend|\$\d", b, re.IGNORECASE) for _, b in found.get(n, [])):
            fail(f"row {n} asks the price; the draft must answer what it depends on before the call ask")
        if "accepted" in cls.lower() and not any(re.search(r"invite (?:is )?on its way|invite (?:is )?(?:sent|attached)", b, re.IGNORECASE) for _, b in found.get(n, [])):
            fail(f"row {n} accepted a time; the draft says the invite is on its way (send it now)")
        if re.search(r"not interested", cls, re.IGNORECASE) and any("?" in b for _, b in found.get(n, [])):
            fail(f"row {n} is Not interested; its draft asks a question")
    for items in found.values():
        for head, body in items:
            check_draft(body)
    check_referral_subject(referral)
    if not has_bounce and re.search(r"\bbounce", text, re.IGNORECASE):
        fail("triage mentions bounces but no pasted reply is a bounce; cut it")
    if re.search(r"help.?desk|ticket system", text, re.IGNORECASE) and not any("automatic" in r["class"].lower() for r in rows):
        fail("triage mentions help-desk rules but no pasted reply is automatic; cut it")
    print(f"PASS - triage of {len(rows)} replies, {sum(len(v) for v in found.values())} drafts, send column matches drafts, hostile replies kept with a person")
    sys.exit(0)


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/playbook.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the deliverable: {hit.group(0)}")
    hit = LEGAL.search(text)
    if hit:
        fail(f"deliverable contains legal content ('{hit.group(0)}'); state operating rules and their reasons instead")
    hit = TOOL_ID.search(FENCE.sub("", MERGE.sub("", text))) or re.search(r"```json", text)
    if hit:
        fail(f"deliverable contains a tool id or JSON call block ('{hit.group(0)}'); name the lookup in words")
    hit = PADDING.search(text)
    if hit:
        fail(f"deliverable cites a source page or file path the reader can't use: '{hit.group(0)}'")
    secs = sections(text)
    if "reply triage" in secs and "inbox setup" not in secs:
        triage(text, secs)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    words = len(text.split())
    if words < MIN_WORDS:
        fail(f"playbook has {words} words, minimum is {MIN_WORDS}")
    all_rows = table_rows(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"playbook has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    taxonomy = table_rows(secs["reply taxonomy"])
    slas = table_rows(secs["slas"])
    crm = table_rows(secs["crm state map"])
    for cls in MUST_HAVE_CLASSES:
        if not covers(taxonomy, "class", cls):
            fail(f"Reply Taxonomy has no '{cls}' class")
        if not covers(slas, "class", cls):
            fail(f"SLAs has no row for '{cls}'")
        if not covers(crm, "class", cls):
            fail(f"CRM State Map has no row for '{cls}'")

    # Skill check: every SLA row names who it escalates to; interested rows give a role and a time limit.
    if slas and "escalate to" not in slas[0]:
        fail("SLAs table needs an 'Escalate to' column")
    for r in slas:
        esc = r.get("escalate to", "").strip()
        if not esc:
            fail(f"SLA row '{r.get('class')}' has an empty 'Escalate to' cell (write 'None' if nobody)")
        if is_hot(r.get("class", "")):
            if esc.lower().startswith("none") or not TIME_LIMIT.search(esc):
                fail(f"SLA row '{r.get('class')}' must escalate to a named role with a time limit")
            took = minutes(r.get("first response", ""))
            if took is None:
                fail(f"hot SLA row '{r.get('class')}' needs a first response time in minutes")
            if took > HOT_SLA_MINUTES:
                fail(f"hot SLA row '{r.get('class')}' allows more than {HOT_SLA_MINUTES} minutes; hot replies get {HOT_SLA_MINUTES} minutes at every account tier")

    # Skill check: the automation boundary is stated.
    auto_text = secs["automation boundaries"]
    auto_rows = table_rows(auto_text)
    if not auto_rows or "automation" not in auto_rows[0]:
        fail("Automation Boundaries needs a table with an 'Automation' column (auto, partial or never)")
    for cls in AUTO_ALLOWED:
        rows = covers(auto_rows, "class", cls)
        if not rows:
            fail(f"Automation Boundaries has no row for '{cls}'")
        if not rows[0].get("automation", "").lower().startswith(("auto", "partial")):
            fail(f"Automation Boundaries should let automation handle '{cls}'")
    hostile = covers(auto_rows, "class", "hostile")
    if not hostile or not hostile[0].get("automation", "").lower().startswith(("never", "human")):
        fail("Automation Boundaries must keep 'hostile' replies with a person (Automation: never)")
    if not re.search(r"\bspam\b", auto_text, re.IGNORECASE) or not re.search(r"lawyer|attorney", auto_text, re.IGNORECASE):
        fail("Automation Boundaries must list hostile trigger words, including spam and lawyer or attorney")
    target = [r for r in auto_rows
              if re.search(r"(?<!non-)(?<!non )target", r.get("class", ""), re.IGNORECASE) and "interested" in r.get("class", "").lower()]
    if not target or not target[0].get("automation", "").lower().startswith(("never", "human")):
        fail("Automation Boundaries must keep target-account interested replies with a person (Automation: never)")
    if not any("confidence" in line.lower() and THRESHOLD.search(line) for line in auto_text.splitlines()):
        fail("Automation Boundaries must state the confidence threshold the user set, as a number")
    if "queue" not in auto_text.lower():
        fail("Automation Boundaries must name the human-review queue")
    if not re.search(r"misclassif", auto_text, re.IGNORECASE) or not re.search(r"week", auto_text, re.IGNORECASE):
        fail("Automation Boundaries must set a weekly misclassification sample")

    # Skill check: every CRM row states a suppression decision; no-reply classes are suppressed.
    for r in crm:
        if not r.get("suppress"):
            fail(f"CRM row '{r.get('class')}' has no suppression decision")
    for cls in NO_REPLY_CLASSES:
        for r in covers(crm, "class", cls):
            if not r["suppress"].lower().startswith("yes"):
                fail(f"'{r['class']}' must be suppressed")
        for r in covers(slas, "class", cls):
            first = r.get("first response", "").lower()
            if "no sales reply" in first:
                fail(f"'{r['class']}' says 'no sales reply'; write 'No reply' or 'Removal line' so the reader knows what goes out")
            if "no reply" not in first and "removal line" not in first:
                fail(f"'{r['class']}' must say 'No reply' or 'Removal line' in SLAs")
            if "removal line" in first and not [h for h, _ in drafts(secs["response library"]) if cls in h.lower()]:
                fail(f"'{r['class']}' sends a removal line but the Response Library has no draft for it")

    # Skill check: every response body is under 80 words.
    bodies = re.findall(r"```[a-z]*\n(.*?)```", secs["response library"], re.DOTALL)
    if len(bodies) < 8:
        fail(f"Response Library has {len(bodies)} responses, minimum is 8")
    for b in bodies:
        check_draft(b)
    library = drafts(secs["response library"])
    objections = [h for h, _ in library if "objection" in h.lower()]
    if len(objections) < 3:
        fail(f"Response Library has {len(objections)} objection drafts; give ready lines for at least three objections")
    referral = [(h, b) for h, b in library if "referred" in h.lower() or ("referral" in h.lower() and "first email" in h.lower())]
    if not referral:
        fail("Response Library needs the first email to the referred person under a heading containing 'referred'")
    check_referral_subject(referral)

    # Skill check: the not-interested draft accepts and stops, with no question.
    ni = [body for head, body in drafts(secs["response library"]) if "not interested" in head.lower()]
    if not ni:
        fail("Response Library needs a draft under a '### ... Not interested' heading")
    for body in ni:
        if "?" in body:
            fail("the Not interested draft asks a question; accept and stop")

    # Skill check: referral capture uses find_emails; every suppression row gives an operating reason and a deadline.
    if "find_emails" not in secs["referral capture"] and "email finder" not in secs["referral capture"].lower():
        fail("Referral Capture must use ScraperCity's Email Finder (find_emails) on the referred person")
    sup = table_rows(secs["suppression rules"])
    if not sup:
        fail("Suppression Rules has no rows")
    for r in sup:
        if len(r.get("reason", "").split()) < 3:
            fail(f"suppression row '{r.get('event')}' needs a Reason column stating why (complaint rate, bounce rate, a promise kept)")
    if not any(DEADLINE.search(r.get("deadline", "")) for r in sup):
        fail("Suppression Rules needs at least one deadline in days or hours")

    hot = sum(1 for r in slas if is_hot(r.get("class", "")))
    print(f"PASS - {len(taxonomy)} classes, {len(bodies)} bracket-free responses of {MAX_RESPONSE_WORDS} words or fewer, {hot} hot SLAs at {HOT_SLA_MINUTES} minutes or less, {len(auto_rows)} automation rows, {len(all_rows)} table rows")
    sys.exit(0)


if __name__ == "__main__":
    main()
