#!/usr/bin/env python3
"""Check a finished multi-channel outreach plan.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED = [
    "Summary",
    "Channel Roles",
    "Contact Tiers",
    "Cadence",
    "Tool Setup",
    "Reply Branches",
    "Channel Copy",
    "Launch and Cost",
    "Tracking",
]
# "Tool Choice" only when the user asked which multichannel tool to use.
OPTIONAL = ["Tool Choice"]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 4000
PHONE_CHECK = re.compile(r"do-not-call|do not call list|opt-?out|suppression", re.IGNORECASE)
# Deliverables carry no legal content (owner rule, 2026-10-13). Same terms as the repo's
# validate-skills.py --check-legal list, plus texting registration; one letter of each term
# sits in brackets so this file does not itself name a law, regulator or registry.
LEGAL_TERMS = [
    r"c[a]n[- ]?spam", r"\bt[c]pa\b", r"telephone consumer pro[t]ection", r"\bc[a]sl\b", r"anti-spam legi[s]lation",
    r"\bg[d]pr\b", r"general data pro[t]ection", r"\bepri[v]acy\b", r"lawful bas[i]s", r"legitimate interests? asse[s]sment",
    r"\bc[c]pa\b", r"\bc[p]ra\b", r"california consumer pri[v]acy", r"\bp[e]cr\b", r"privacy and electronic com[m]unications",
    r"\bf[c]ra\b", r"fair credit rep[o]rting", r"\bt[s]r\b", r"telemarketing sales r[u]le", r"\b(?:4[7]|1[6])\s*c\.?f\.?r\b",
    r"\b(?:f[t]c|f[c]c|c[r]tc|i[c]o)\b", r"federal trade com[m]ission", r"federal communications com[m]ission",
    r"information com[m]issioner", r"att[o]rneys? gen[e]ral", r"legal ad[v]ice", r"\bnot le[g]al\b",
    r"(?:consult|check with|speak with|talk to) (?:a|an|your) (?:\w+ )?(?:law[y]er|att[o]rney|coun[s]el)",
    r"do[- ]not[- ]call reg[i]stry", r"nati[o]nal do[- ]not[- ]call", r"donotcall\.g[o]v", r"\bdnc reg[i]stry",
    r"compliance ga[t]es?", r"\bsta[t]ute", r"\bpenalt[i]", r"prior exp[r]ess",
    r"\b1[0]dlc\b", r"campaign reg[i]stry", r"regi[s]tered (?:number|brand|campaign)",
]
LEGAL = re.compile("|".join(LEGAL_TERMS), re.IGNORECASE)
BAD_OPENER = re.compile(r"bad time", re.IGNORECASE)
CONFIRM = re.compile(r"confirm|reminder", re.IGNORECASE)
CONFIRM_TIMES = {
    "a week before": re.compile(r"week|7 days|5 business days", re.IGNORECASE),
    "24 hours before": re.compile(r"24 hours|24h|day before", re.IGNORECASE),
    "2 to 3 hours before": re.compile(r"2 to 3 hours|2-3 hours", re.IGNORECASE),
}
MESSAGING = re.compile(r"\bsms\b|\btext(s|ing)?\b|whatsapp", re.IGNORECASE)
ASKED_TO_TEXT = re.compile(r"asks? to text|asked to text|request to text|requests? a text", re.IGNORECASE)
NO_SKIP = {"", "-", "n/a"}
CHANNELS = {
    "email": re.compile(r"\bemail\b", re.IGNORECASE),
    "phone": re.compile(r"\bphone\b|\bcall\b|\bsms\b|\btext\b|\bdial", re.IGNORECASE),
    "linkedin": re.compile(r"linkedin", re.IGNORECASE),
    "mail": re.compile(r"direct mail|postcard|letter|\bmail\b", re.IGNORECASE),
}
CODE = re.compile(r"\b([A-Z]{1,2}\d{1,2}[a-z]?)\b")
NO_CODE_OK = re.compile(r"profile view|view profile", re.IGNORECASE)
PLACEHOLDER_BRACKET = re.compile(r"\[[^\]\n]{1,60}\]")
MAX_EMAIL_WORDS = 75  # Berman's templates page: cut any cold email over 75 words
RELATED_SKILLS = (
    "cold-calling|cold-email-strategy|cold-email-copywriting|reply-handling|signal-triggered-outbound|"
    "outbound-unit-economics|mobile-appender|local-business-list|scrapercity-real-estate-data|skip-tracer"
)
INTERNAL = [
    (re.compile(r"\b(references|scripts|templates|examples)/|\.md\b|\.py\b|SKILL\.md"), "an internal file path"),
    (re.compile(r"\bsection \d", re.IGNORECASE), "a reference section number"),
    (re.compile(r"\b(find_mobiles|find_emails|find_people|validate_emails|check_wallet|list_runs|download_results|check_run_status|query_lead_database|query_local_business_database|search_criminal_records|scrape_[a-z_]+)\b"), "a tool id (name the product instead, such as Mobile Finder)"),
    (re.compile(r"^\s*[-*] \[[ xX]\]", re.MULTILINE), "a checkbox list (self-grading)"),
    (re.compile(r"^#+\s*quality check", re.IGNORECASE | re.MULTILINE), "a quality check section (self-grading)"),
    (re.compile(r"\b(" + RELATED_SKILLS + r")\b|\bskill\b", re.IGNORECASE), "a skill name or skill reference (state the recommendation directly)"),
    (re.compile(r"^Next:", re.MULTILINE), "a 'Next:' handoff line"),
    # Plans use Low-risk LinkedIn touches only, so tools that automate LinkedIn are never used.
    (re.compile(r"heyreach|expandi|la growth machine", re.IGNORECASE), "a LinkedIn automation tool the plan does not use"),
    (re.compile(r"linkedin risk|\((?:low|medium|high)\)", re.IGNORECASE), "a tool risk rating (name only the tools the plan uses)"),
]
MONTH = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
DATE = re.compile(r"\b\d{1,2} " + MONTH + r"\b|\b" + MONTH + r" \d{1,2}\b|\b20\d\d-\d\d-\d\d\b")
ALTERNATIVE_COPY = re.compile(r"\b(?:has|is|was|are)\b[^.|\"]{0,80}, or (?:is|has|was|are)\b", re.IGNORECASE)
MERGE = re.compile(r"\{\{\s*([a-z_]+)")
BASIC_MERGE = {"first_name", "last_name", "company"}
REPEAT_MIN_CHARS = 40
REPEAT_MAX = 3
DISCLAIMER = re.compile(r"\bassumed\b|until the (?:data )?pull runs|nothing was run|not yet (?:run|pulled)", re.IGNORECASE)
DISCLAIMER_MAX = 4
REPLY_CLASSES = {
    "interested or asks for a time": re.compile(r"interested|asks for a time|meeting request", re.IGNORECASE),
    "price question": re.compile(r"price|cost", re.IGNORECASE),
    "referral": re.compile(r"referr", re.IGNORECASE),
    "forwarded internally": re.compile(r"forward", re.IGNORECASE),
    "wrong person or left the company": re.compile(r"wrong person|left the company|no longer", re.IGNORECASE),
    "not now": re.compile(r"not now|timing", re.IGNORECASE),
    "uses a competitor": re.compile(r"competitor|current vendor|already use", re.IGNORECASE),
    "not interested": re.compile(r"not interested", re.IGNORECASE),
    "opt-out": re.compile(r"opt-?out|unsubscribe", re.IGNORECASE),
    "angry or threatening": re.compile(r"angry|threat|hostile", re.IGNORECASE),
    "out of office": re.compile(r"out of office|\booo\b|auto-?reply", re.IGNORECASE),
    "bounce": re.compile(r"bounce", re.IGNORECASE),
}
PHONE_OUTCOMES = {
    "voicemail": re.compile(r"voicemail", re.IGNORECASE),
    "front desk": re.compile(r"front desk|gatekeeper|assistant", re.IGNORECASE),
    "wrong number": re.compile(r"wrong number|disconnected|bad number", re.IGNORECASE),
    "returned call": re.compile(r"returns? (?:a |the )?call|calls? back|callback", re.IGNORECASE),
}


def word_count(s):
    return len(re.findall(r"[A-Za-z0-9{}'$%.,|-]+", s))


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
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", s.strip().strip("|"))]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    if not rows:
        return [], []
    return [h.lower() for h in rows[0]], rows[1:]


def all_cells(text):
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|"):
            for c in re.split(r"(?<!\\)\|", s.strip("|")):
                c = c.strip()
                if c and not re.fullmatch(r":?-+:?", c):
                    yield c


def col(header, name):
    for i, h in enumerate(header):
        if name in h:
            return i
    return -1


def channel_of(cell):
    c = cell.lower()
    if "linkedin" in c:
        return "linkedin"
    if any(w in c for w in ("phone", "call", "sms", "text")):
        return "phone"
    if any(w in c for w in ("mail", "postcard", "letter")) and "email" not in c:
        return "mail"
    if "email" in c:
        return "email"
    return c


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
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    hit = BAD_OPENER.search(text)
    if hit:
        return fail("plan uses the 'did I catch you at a bad time' opener; Gong measured it about 40% less likely to book. Use 'The reason I'm calling is...'")
    sec = sections(text)
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")
    allowed = {n.lower() for n in REQUIRED + OPTIONAL}
    for name in sec:
        if name not in allowed:
            return fail(f"section '## {name}' is not part of the plan format; fold it into a required section or cut it")

    # Economy: one disclaimer line at the top, no long cell repeated across rows.
    head = text.split("## ", 1)[0]
    if not re.search(r"^Not checked:", head, re.IGNORECASE | re.MULTILINE):
        return fail("put one 'Not checked:' line above '## Summary' naming what was assumed or not verified (or 'Not checked: nothing')")
    if len(re.findall(r"^Not checked:", text, re.IGNORECASE | re.MULTILINE)) > 1:
        return fail("state 'Not checked:' once, at the top")
    n = len(DISCLAIMER.findall(text))
    if n > DISCLAIMER_MAX:
        return fail(f"'assumed' or a not-run disclaimer appears {n} times; say it once in the 'Not checked:' line (at most {DISCLAIMER_MAX})")
    counts = Counter(c for c in all_cells(text) if len(c) >= REPEAT_MIN_CHARS)
    for cell, k in counts.items():
        if k > REPEAT_MAX:
            return fail(f"the same cell appears {k} times: '{cell[:70]}'; state it once above the table")

    header, rows = table(sec["cadence"])
    ci, ti = col(header, "channel"), col(header, "touch")
    ski, oi, tri = col(header, "skip"), col(header, "owner"), col(header, "tier")
    if min(ci, ti) < 0:
        return fail("Cadence table needs Channel and Touch columns")
    if col(header, "check") >= 0:
        return fail("Cadence has a Check column; state the standing checks once in a 'Checks:' line above the table")
    if ski < 0:
        return fail("Cadence table needs a 'Skip when' column (a skip branch per touch)")
    if oi < 0:
        return fail("Cadence table needs an Owner column")
    tmi, dyi = col(header, "time"), col(header, "day")
    if tmi < 0 or dyi < 0:
        return fail("Cadence table needs Day and Time columns (day offset and recipient local time per touch)")
    cadence_head = sec["cadence"].split("|", 1)[0]
    checks = re.search(r"^Checks:(.*)$", cadence_head, re.IGNORECASE | re.MULTILINE)
    if not checks:
        return fail("Cadence needs one 'Checks:' line above the table with the standing checks (unsubscribe footer, do-not-call list and opt-outs)")
    checks_line = checks.group(1)
    hit = DATE.search(sec["cadence"])
    if hit:
        return fail(f"Cadence carries a calendar date ({hit.group(0)}); the cadence is day offsets, and dates go in Launch and Cost")
    copy_header, copy_rows = table(sec["channel copy"])
    codes = set()
    for r in copy_rows:
        if r:
            codes.update(CODE.findall(r[0]))
    if not codes:
        return fail("Channel Copy needs a code (E1, V1, L1...) in the first column of each row")
    owners = {}
    if len(rows) < 6:
        return fail("Cadence needs at least 6 touch rows")
    used = set()
    phone_rows = 0
    for r in rows:
        if len(r) <= max(ci, ti, ski, oi, tmi, dyi):
            return fail(f"cadence row has too few cells: {' | '.join(r)[:80]}")
        if r[ski].strip().lower() in NO_SKIP:
            return fail(f"cadence row without a skip branch: {' | '.join(r)[:80]}")
        if not re.search(r"\d", r[tmi]) or not r[dyi].strip():
            return fail(f"cadence row needs a day and a clock time: {' | '.join(r)[:80]}")
        row_codes = set(CODE.findall(r[ti]))
        if not row_codes and not NO_CODE_OK.search(r[ti]):
            return fail(f"cadence touch names no copy code from Channel Copy: {r[ti][:80]}")
        missing_codes = row_codes - codes
        if missing_codes:
            return fail(f"cadence touch uses copy code(s) {', '.join(sorted(missing_codes))} that Channel Copy does not contain")
        tier = r[tri].strip().lower() if tri >= 0 else "all"
        owner = re.sub(r"\(.*?\)", "", r[oi]).strip().lower()
        if not owner:
            return fail(f"cadence row without an owner: {' | '.join(r)[:80]}")
        owners.setdefault(tier, set()).add(owner)
        ch = channel_of(r[ci])
        used.add(ch)
        if MESSAGING.search(r[ci]) and not ASKED_TO_TEXT.search(" ".join(r)):
            return fail(f"SMS touch must run only after the prospect asks to text: {' | '.join(r)[:80]}")
        if ch == "phone":
            phone_rows += 1
        if ch == "linkedin":
            if "manual" not in (r[ti] + " " + checks_line).lower():
                return fail(f"LinkedIn touch must be marked manual (in the row or the 'Checks:' line): {r[ti][:80]}")
            if re.search(r"connection request|\bL1\b", r[ti]) and re.search(r"signal|no post|dormant|inactive", r[ski], re.IGNORECASE):
                return fail(f"connection request skipped for lack of a LinkedIn signal: {r[ski][:80]}; send L1 to every contact with a LinkedIn URL and use signals only to order the day's requests")
    if phone_rows and not PHONE_CHECK.search(checks_line):
        return fail("plan has phone touches; the 'Checks:' line must name the internal do-not-call list and opt-outs")
    if "email" in used and not re.search(r"unsubscribe", checks_line, re.IGNORECASE):
        return fail("plan has email touches; the 'Checks:' line must name the one-click unsubscribe")
    for tier, names in owners.items():
        if len(names) > 1:
            return fail(f"tier {tier} has several owners ({', '.join(sorted(names))}); one rep owns every channel for an account")
    known = used & set(CHANNELS)
    if len(known) < 3:
        return fail(f"cadence uses {len(known)} channels ({', '.join(sorted(known))}); need at least 3")
    if not re.search(r"stop rule", sec["cadence"], re.IGNORECASE):
        return fail("Cadence needs a written stop rule")
    if phone_rows and not re.search(r"caller id", sec["cadence"], re.IGNORECASE):
        return fail("Cadence needs one line on checking each rep's caller ID for a spam label")

    confirm_text = " ".join(" ".join(r) for r in rows if CONFIRM.search(r[ti]))
    for label, rx in CONFIRM_TIMES.items():
        if not rx.search(confirm_text):
            return fail(f"Cadence needs a meeting confirmation row {label} (week out, 24 hours, 2 to 3 hours)")
    if not re.search(r"operational owner|bring the", confirm_text, re.IGNORECASE):
        return fail("a confirmation row must ask the buyer to bring the operational owner to the meeting")
    if any(channel_of(r[ci]) == "linkedin" and re.search(r"connection request|\bL1\b", r[ti]) for r in rows):
        if not re.search(r"accept", sec["cadence"], re.IGNORECASE):
            return fail("plan sends LinkedIn connection requests but states no accept-skips-email branch")
        m = re.search(r"LinkedIn volume:[^\n]*?(\d+)", text)
        if not m:
            return fail("plan sends LinkedIn connection requests but has no 'LinkedIn volume:' line with requests per seat per week")
        if int(m.group(1)) > 100:
            return fail(f"LinkedIn volume of {m.group(1)} requests a week per seat is over the community estimate of about 100 a week (Overloop, July 2026); cap it lower")

    ts = sec["tool setup"]
    if not (re.search(r"compan", ts, re.IGNORECASE) and re.search(r"repl", ts, re.IGNORECASE)):
        return fail("Tool Setup must name the sequencer setting that stops everyone at the company on a reply")
    if "linkedin" in used and not re.search(r"task", ts, re.IGNORECASE):
        return fail("Tool Setup must say how LinkedIn rows become manual tasks")

    rh, rrows = table(sec["reply branches"])
    if len(rrows) < 12:
        return fail(f"Reply Branches needs a row for every reply type and call outcome (at least 12, found {len(rrows)})")
    texti = max(col(rh, "text"), col(rh, "send"), col(rh, "reply text"))
    if col(rh, "action") < 0 or col(rh, "owner") < 0 or texti < 0:
        return fail("Reply Branches needs Action, Owner and Text to send columns")
    for r in rrows:
        if len(r) <= texti or not r[texti].strip():
            return fail(f"reply branch without text to send (write None when nothing is sent): {' | '.join(r)[:80]}")
    reply_text = sec["reply branches"]
    for label, rx in REPLY_CLASSES.items():
        if not rx.search(reply_text):
            return fail(f"Reply Branches has no row for: {label}")
    price_rows = [r for r in rrows if re.search(r"price|cost", r[0], re.IGNORECASE)]
    if price_rows and not re.search(r"\$|\{\{\s*price", price_rows[0][texti]):
        return fail("the price question row must answer with the price or range ($ figure or {{price_range}}) and what moves it, then offer the call")
    if phone_rows:
        for label, rx in PHONE_OUTCOMES.items():
            if not rx.search(reply_text):
                return fail(f"Reply Branches has no call outcome row for: {label}")
    if "linkedin" in used and not re.search(r"accept", reply_text, re.IGNORECASE):
        return fail("Reply Branches needs a row for a LinkedIn connection accepted without a message")

    for name in ("channel copy", "reply branches"):
        hit = PLACEHOLDER_BRACKET.search(sec[name])
        if hit:
            return fail(f"bracket placeholder in {name}: {hit.group(0)}; write sendable text (merge fields like {{{{first_name|there}}}} are fine)")
    hit = ALTERNATIVE_COPY.search(sec["channel copy"])
    if hit:
        return fail(f"copy covers two cases in one body ('{hit.group(0)[:60]}'); write one copy code per trigger or persona")
    if re.search(r"trigger", sec["contact tiers"], re.IGNORECASE):
        fields = set(MERGE.findall(sec["channel copy"])) - BASIC_MERGE
        if not fields:
            return fail("tiers use a trigger, but no copy names it; add the trigger's own merge fields (such as {{award_project}}) to the trigger variants")
    chi = col(copy_header, "channel")
    for r in copy_rows:
        if not r or not CODE.search(r[0]) or not r[0].strip().upper().startswith("E"):
            continue
        if chi >= 0 and len(r) > chi and "email" not in r[chi].lower():
            continue
        body_cell = " ".join(r[1:])
        if not re.search(r"subject", body_cell, re.IGNORECASE):
            return fail(f"email {r[0]} has no subject line")
        m = re.search(r"body:(.*)", body_cell, re.IGNORECASE | re.DOTALL)
        if not m:
            return fail(f"email {r[0]} needs its full body after 'Body:'")
        if word_count(m.group(1)) > MAX_EMAIL_WORDS:
            return fail(f"email {r[0]} body is {word_count(m.group(1))} words; keep it to {MAX_EMAIL_WORDS} or fewer")

    hit = LEGAL.search(text)
    if hit:
        return fail(f"deliverable contains legal or registration content ({hit.group(0)}); state the operating rule only")
    for rx, label in INTERNAL:
        hit = rx.search(text)
        if hit:
            return fail(f"deliverable contains {label}: {hit.group(0).strip()}")

    cost = sec["launch and cost"]
    if "$" not in cost or not re.search(r"^\|\s*total", cost, re.IGNORECASE | re.MULTILINE):
        return fail("Launch and Cost needs dollar figures and a Total row")
    if not DATE.search(cost):
        return fail("Launch and Cost needs the dated launch calendar (cohort start dates)")
    if re.search(r"mobile finder", cost, re.IGNORECASE) and "0.25" not in cost:
        return fail("Mobile Finder must be priced at $0.25 per number found")
    if re.search(r"sales navigator", cost, re.IGNORECASE) and not re.search(r"119\.99|1,079\.88", cost):
        return fail("Sales Navigator Core is $119.99 a month or $1,079.88 a year (LinkedIn compare-plans page, checked 2026-10-13)")
    priced = {name for name, rx in CHANNELS.items() if rx.search(cost)}
    if len(priced) < 2:
        return fail("Launch and Cost needs per-channel lines for at least 2 channels")
    if len(table(sec["tracking"])[1]) < 3:
        return fail("Tracking needs at least 3 metric rows")

    print(f"PASS - {len(rows)} touches across {len(known)} channels with day, time and copy code on each, standing checks stated once, no legal content, {len(rrows)} reply branches, one owner per tier, confirmations at a week, 24 hours and 2 to 3 hours, no internal paths, skill names or tool ids, no repeated cells, cost total present")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
