#!/usr/bin/env python3
"""Check a cold calling plan produced with the cold-calling skill.

Usage: check-output.py path/to/call-plan.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import datetime
import hashlib
import re
import sys

REQUIRED = [
    "Program Summary",
    "Launch Checklist",
    "Call List Build",
    "Dialer Setup",
    "Call Blocks",
    "Funnel Targets",
    "Call Script",
    "Objection Bank",
    "Voicemail, Gatekeeper and Email",
    "CRM Logging",
    "Pilot Plan",
    "Rep Scorecard",
]
# "Cost Estimate" is optional: only when the user asked about cost or budget.
SCORECARD_COLUMNS = [
    "rep", "days", "dials", "dials/day", "connects", "connect rate", "conversations",
    "conversations per 100 dials", "meetings", "conversation-to-meeting", "dials per meeting", "held", "show rate",
]
# (column, numerator column, denominator column, multiplier)
SCORECARD_RATES = [
    ("dials/day", "dials", "days", 1),
    ("connect rate", "connects", "dials", 100),
    ("conversations per 100 dials", "conversations", "dials", 100),
    ("conversation-to-meeting", "meetings", "conversations", 100),
    ("dials per meeting", "dials", "meetings", 1),
    ("show rate", "held", "meetings", 100),
]
FUNNEL_STAGES = ["dial", "connect", "conversation", "meeting"]
SCRIPT_PARTS = ["opener", "reason", "stake", "question", "ask"]
MIN_WORDS = 900
MAX_WORDS = 4000
MIN_TABLE_ROWS = 30
MIN_OBJECTIONS = 8
MAX_OBJECTION_WORDS = 45
MAX_VOICEMAIL_WORDS = 75
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
# Deliverables carry no legal content (owner rule, 2026-10-13). The banned words and
# phrases are stored as SHA-256 hashes of lowercase words joined by single spaces, so the
# checker itself names no law, regulation or regulator.
LEGAL_HASHES = {
    "df679e72d63dc69befbe502d5e155258ca356fa1ac5ab7b47aab9c990f9586c1",
    "84381ab8e13ff5efe91ad2d189905637b3861ecd4ab351ecc5ce2cde18d24189",
    "8d53e0154b79535cda4bda2c9ad960af9bf320002ce8d8365c7a0a56f4f897f9",
    "8b16477e3abe1de345a6e82f360db77b5e238983ad685cec9fef0d0bc009aed3",
    "0c89db9e0a961c3939fb277192805c817fdf6b611e353477970af73ad9b54236",
    "ca30ed14f4d400b853d9b111688395db1d75a5583539d9841b2209d0b9d8400c",
    "fa193c8cc820b3b216502909af65a353a26b670c77833006d7dca1144bfb6950",
    "9f6bbaad419acd37b0d06e775bb1d28533a0cefdef0c245d769af00a80eef975",
    "9471848c4835a19f0bff2d3529343a8b0149e501fff60573b09f931d55a2738a",
    "44f9457e91d3f44b74db2f18a6129d8f607d9c126551a004d37c9f78c3bd7970",
    "88b1fe38cf4efddeccb0a6b068134a319c9bcd5bd5fefb53b1addebd8481bf8b",
    "0d4bf5b068aa598c06488809d6c39af7d3f9e2c8dcbd5324cd8fdd26b3135a19",
    "b0c50e9b35b69e48852157aa642adbf411eb3239fc49d5d0f90b38739ee38789",
    "c51052ef06b65a956d9edade6297b03388457a6521544a6d11e1c0507173b2f3",
    "467f0ea7dd59072ccaa8dcd5901728a463e3d9a9e13d2c676fd2dc80c891124f",
    "503acf004b50b4f97beae09309f837a2ba47afacc83800fce9a1066813c7a97d",
    "c1818e804aa575636570432284eb15ef692087ef09f6542c1b302bd6f7bb4419",
    "5561ba03cac2c86f883ddbe7966f05c12375f0ce18fe8a0938733d170887fe76",
    "1244377974aeb11cf1b66db5a33bb15b58ec15d72a6e807157d50e62b642de25",
    "83a70052504733134861af25c442ffd741935da314c948f2e015a93b2d0af6ed",
    "6c0a579f38b0e548486f32f9e6d1585102d1050e2d50293a324405735e2f7d78",
    "ff9a0c76596a5d3c658f760c483cc2b927d118bc84c52d8ea2146a0cf2a4c9f6",
    "5da94256a72d9fbd13a4afa5d27a05415c927774b6d923941ee31a31f58704b3",
    "e068496fb44ea938edba82e057fdd593dbe2620e68aa5c4a75b7aa31aa67c591",
    "62ae4ff47444a8465b7923c659ebe4f24549a314307a2f30f33cb99b5d5c422a",
    "b513716da13daea38b13e1c44276cc9a62cd9cff76519ea003d31ce57418e7d0",
    "32d80a57c154f5ba07371e03fd99dc9d86144c7eb23990f0ebcb9f541fed8670",
    "627961dee6169ac8943a35df549c893d90f8c6eb5257c0f80abefb48f1a76fe3",
    "25e5311e5de0b865f90e874755f1f67d59f460f3f27b2c21f1cbcb3440ce15cc",
    "8cd82cea8bfd564e4c17c472393806ff48d48f8d9eb45ae710f84851d47d9ff0",
    "165c98109c749b07bf006464025493b72b8445178a8c26c4d4ee029b92dc96df",
    "3d3fe9db99013800dd8f649a06272eaa764efd599b3aabd93cacc4f49517c528",
}
HOURS = re.compile(r"\d{1,2}(:\d\d)?\s*(am|pm).{0,20}\d{1,2}(:\d\d)?\s*(am|pm)", re.IGNORECASE)
DOLLAR = re.compile(r"\$\s?\d")
STOP_WORDS = re.compile(r"don.?t call|remove me|take me off|stop calling", re.IGNORECASE)
ISO_DATE = re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b")
MULTI_LEVER = re.compile(r"\band\b|,|\+|&|/", re.IGNORECASE)
PILOT_MIN_DAYS, PILOT_MAX_DAYS = 7, 16
INTERNAL = re.compile(
    r"\b(query_[a-z_]+|scrape_[a-z_]+|find_(mobiles|emails|people)|check_wallet|validate_emails)\b"
    r"|npx scrapercity|/api/v1/|references/[\w-]+\.md|SKILL\.md|templates/|scripts/check-output",
    re.IGNORECASE,
)
MOBILE = re.compile(r"mobile finder", re.IGNORECASE)
# Trainer and framework names stay in the skill's sources; the plan states the instruction.
# Published datasets (Belkins, Cognism, Gong) may be cited in a Basis column.
NAME_DROP = re.compile(
    r"\b(Berman|Blount|Reisert|Pessar|Slocum|Gilkey|TitanX|Sandler|Golden Hours|Law of Replacement"
    r"|King of the Hill|3x3)\b",
    re.IGNORECASE,
)
SKILL_NAMES = re.compile(
    r"\b(multi-channel-outreach|reply-handling|cold-email-strategy|cold-email-copywriting|signal-triggered-outbound"
    r"|outbound-unit-economics|mobile-appender|local-business-list|decision-maker-finder|email-deliverability"
    r"|domain-infrastructure|inbox-setup|sending-platforms|crm-enricher|account-researcher|icp-list-builder"
    r"|tam-builder|skip-tracer|scrapercity-[a-z-]+|using-scrapercity-skills)\b",
    re.IGNORECASE,
)
# Agent process lines are not deliverable content.
PROCESS = re.compile(
    r"\bwallet\b|not checked|over \$5\b|for a yes\b|\bnot run\b|\bnothing was run\b",
    re.IGNORECASE,
)
ABSOLUTE_GAP = re.compile(r"\bno [a-z -]{0,40}(benchmark|figure|dataset|data) exists\b", re.IGNORECASE)
MERGE_FIELD = re.compile(r"\{[a-z][a-z0-9_]*\}")
MSG_ID = re.compile(r"\b([ECV]\d+)\b")
MULTI_REP = re.compile(r"\b([2-9]|\d\d)\s+(SDRs|reps|callers)\b", re.IGNORECASE)


def legal_hit(text):
    """True when any word or run of up to three words hashes to a banned legal term."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    for i in range(len(words)):
        for n in (1, 2, 3):
            if i + n <= len(words):
                key = " ".join(words[i:i + n])
                if hashlib.sha256(key.encode()).hexdigest() in LEGAL_HASHES:
                    return True
    return False


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


def number(cell):
    """Parse '2,340', '25.0%', '$1.50' into a float; None for n/a or blank."""
    cleaned = re.sub(r"[,$%\s]", "", cell or "")
    if cleaned.lower() in ("", "n/a", "na", "-"):
        return None
    try:
        return float(cleaned)
    except ValueError:
        return "bad"


def table_count(block):
    lines = [l.strip() for l in block.splitlines()]
    return sum(
        1 for i, l in enumerate(lines)
        if l.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", lines[i + 1])
    )


def words(s):
    return len(re.findall(r"[A-Za-z0-9$'%.,-]+", s))


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/call-plan.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the plan: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    n_words = len(text.split())
    if n_words < MIN_WORDS:
        fail(f"plan has {n_words} words, minimum is {MIN_WORDS}")
    if n_words > MAX_WORDS:
        fail(f"plan has {n_words} words, maximum is {MAX_WORDS}; cut repetition and preamble")
    leak = INTERNAL.search(text)
    if leak:
        fail(f"plan shows an internal tool id, command or file path: '{leak.group(0)}'; use product names and plain filters")
    for pattern, why in (
        (NAME_DROP, "a trainer or framework name; state the instruction without the name"),
        (SKILL_NAMES, "an internal skill name; write the steps it would run instead"),
        (PROCESS, "an agent process line (wallet checks, approvals, what was not run); keep one 'Estimates:' line"),
        (ABSOLUTE_GAP, "an absolute 'no data exists' claim; write 'none found'"),
    ):
        hit = pattern.search(text)
        if hit:
            fail(f"plan contains {why}: '{hit.group(0)}'")
    if len(re.findall(r"(?im)^estimates:", text)) != 1:
        fail("state which counts are estimates in exactly one line starting 'Estimates:'")
    all_rows = table_rows(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"plan has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")

    # Skill check 0: every launch task has an owner and a date.
    launch = table_rows(secs["launch checklist"])
    if len(launch) < 4:
        fail(f"Launch Checklist has {len(launch)} rows, minimum is 4")
    for r in launch:
        if not ISO_DATE.search(r.get("date", "")):
            fail(f"Launch Checklist task '{r.get('task', '?')[:40]}' needs a date as YYYY-MM-DD")
        if not r.get("owner", "").strip():
            fail(f"Launch Checklist task '{r.get('task', '?')[:40]}' needs an owner")

    # Skill check 0b: with two or more reps, the list is split between them.
    if MULTI_REP.search(secs["program summary"]) and not re.search(r"rep split", secs["call list build"], re.IGNORECASE):
        fail("Call List Build needs a 'Rep split:' line assigning records to each rep")

    # Skill check 1: Dialer Setup names the dial mode, caller ID with a test schedule, the window with hours and attempts.
    dialer = table_rows(secs["dialer setup"])
    settings = {r.get("setting", "").lower(): r.get("value", "") for r in dialer}
    for need in ("dial mode", "caller id", "window", "attempts"):
        if not any(k.startswith(need) for k in settings):
            fail(f"Dialer Setup needs a '{need}' row")
    mode = next((v for k, v in settings.items() if k.startswith("dial mode")), "")
    if not re.search(r"click-to-call|click to call|power dialer|parallel", mode, re.IGNORECASE):
        fail("Dial mode must name click-to-call, a power dialer or a parallel dialer")
    cid = next((v for k, v in settings.items() if k.startswith("caller id")), "")
    if not re.search(r"test", cid, re.IGNORECASE):
        fail("Caller ID row needs a test schedule for spam labels")
    if not HOURS.search(secs["dialer setup"]) and not HOURS.search(secs["program summary"]):
        fail("state the calling window with hours, for example 9:00am to 10:30am")

    # Skill check 1b: the plan carries no legal content (owner rule).
    if legal_hit(text):
        fail("plan contains legal content; remove it (owner rule) and keep only settings that change results")

    # Skill check 3: funnel stages with numbers and a basis, in one table (the "Act if" column holds the fix).
    if table_count(secs["funnel targets"]) != 1:
        fail("Funnel Targets holds one table; put each symptom's fix in its 'Act if' cell instead of a second table")
    funnel = table_rows(secs["funnel targets"])
    for stage in FUNNEL_STAGES:
        rows = [r for r in funnel if r.get("stage", "").lower().startswith(stage)]
        if not rows:
            fail(f"Funnel Targets has no '{stage}' row")
        r = rows[0]
        if not re.search(r"\d", r.get("count", "")):
            fail(f"Funnel '{r.get('stage')}' row has no count")
        basis = r.get("basis", "")
        if not (re.search(r"20\d\d", basis) or "assumption" in basis.lower() or "measured" in basis.lower()):
            fail(f"Funnel '{r.get('stage')}' row needs a dated source, 'measured', or 'assumption'")
        if stage != "dial":
            act = next((v for k, v in r.items() if k.startswith("act if")), "")
            if not re.search(r"\d", act):
                fail(f"Funnel '{r.get('stage')}' row needs an 'Act if' threshold with a number")

    # Skill check 4: script has all four parts.
    script = table_rows(secs["call script"])
    parts = " ".join(r.get("part", "").lower() for r in script)
    for p in SCRIPT_PARTS:
        if p not in parts:
            fail(f"Call Script is missing the '{p}' part")
    if len(set(MERGE_FIELD.findall(secs["call script"]))) < 2:
        fail("Call Script needs merge fields from the list columns, for example {owner_first} and {business}, not one sample record")
    if not re.search(r"\bqualify", secs["call script"], re.IGNORECASE):
        fail("Call Script needs a 'Qualify' beat that confirms this person owns and pays for what the offer covers")

    # Skill check 4b: a dated 2-week pilot, one lever per row, each with a decision rule.
    pilot_text = secs["pilot plan"]
    pilot = table_rows(pilot_text)
    if len(pilot) < 2:
        fail("Pilot Plan needs a baseline week and a test week")
    dates = []
    for m in ISO_DATE.finditer(pilot_text):
        try:
            dates.append(datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            fail(f"Pilot Plan has an invalid date: {m.group(0)}")
    for r in pilot:
        if not ISO_DATE.search(r.get("dates", "")):
            fail(f"Pilot Plan row '{r.get('week')}' needs dates as YYYY-MM-DD")
        lever = r.get("lever changed", "")
        if not lever:
            fail("Pilot Plan needs a 'Lever changed' column")
        if MULTI_LEVER.search(lever):
            fail(f"Pilot Plan row '{r.get('week')}' changes more than one lever: '{lever}'")
        if not re.search(r"\d", r.get("decision rule", "")):
            fail(f"Pilot Plan row '{r.get('week')}' needs a decision rule with a threshold")
    span = (max(dates) - min(dates)).days
    if not PILOT_MIN_DAYS <= span <= PILOT_MAX_DAYS:
        fail(f"Pilot Plan dates span {span} days; a 2-week pilot spans {PILOT_MIN_DAYS} to {PILOT_MAX_DAYS}")

    # Skill check 5: objection bank size, length and a question in each response.
    objections = table_rows(secs["objection bank"])
    if len(objections) < MIN_OBJECTIONS:
        fail(f"Objection Bank has {len(objections)} rows, minimum is {MIN_OBJECTIONS}")
    for r in objections:
        resp = r.get("response", "")
        if words(resp) > MAX_OBJECTION_WORDS:
            fail(f"objection response over {MAX_OBJECTION_WORDS} words: '{resp[:50]}...'")
        if STOP_WORDS.search(r.get("objection", "")):
            if "remove" not in resp.lower():
                fail("a stop or don't-call objection must be answered with removal")
            continue
        if "?" not in resp:
            fail(f"objection response has no question: '{resp[:50]}...'")

    # Skill check 6: voicemail scripts stay near 30 seconds; every email the plan sends is written out.
    msgs = table_rows(secs["voicemail, gatekeeper and email"])
    ids = {r.get("id", "").strip().upper() for r in msgs}
    vm = [r for r in msgs if r.get("id", "").upper().startswith("V")]
    if not vm:
        fail("Voicemail, Gatekeeper and Email needs at least one voicemail row with an ID starting V")
    emails = [r for r in msgs if r.get("id", "").upper().startswith(("E", "C"))]
    for r in emails:
        if r.get("id", "").upper().startswith("E") and "subject:" not in r.get("script", "").lower():
            fail(f"email {r.get('id')} needs a 'Subject:' and a full body")
    if not any(r.get("id", "").upper().startswith("C") for r in msgs):
        fail("write the meeting confirmation message as a row with an ID starting C")
    cadence = [r for r in table_rows(secs["call blocks"]) if "email the same day" in r]
    if not cadence:
        fail("Call Blocks needs the attempt cadence table with an 'Email the same day' column")
    for r in cadence:
        cell = r.get("email the same day", "").strip()
        if cell.lower() in ("", "none", "no", "-"):
            continue
        refs = MSG_ID.findall(cell.upper())
        if not refs:
            fail(f"cadence email '{cell}' must name the written email by ID, for example E1")
        for ref in refs:
            if ref not in ids:
                fail(f"cadence names email {ref} but no row {ref} is written in Voicemail, Gatekeeper and Email")
    for r in vm:
        n = words(r.get("script", ""))
        if n > MAX_VOICEMAIL_WORDS:
            fail(f"voicemail {r.get('id')} has {n} words; keep it to {MAX_VOICEMAIL_WORDS} or fewer")

    # Skill check 7: rep scorecard has every column and internally consistent numbers.
    scorecard = table_rows(secs["rep scorecard"])
    if not scorecard:
        fail("Rep Scorecard has no rep rows")
    for col in SCORECARD_COLUMNS:
        if col not in scorecard[0]:
            fail(f"Rep Scorecard is missing the '{col}' column")
    for r in scorecard:
        rep_name = r.get("rep", "?")
        if re.search(r"target", rep_name, re.IGNORECASE):
            fail(f"Rep Scorecard row '{rep_name}' repeats targets; targets live once in Funnel Targets, the scorecard holds actuals")
        cells = [r.get(c, "").strip() for c in SCORECARD_COLUMNS[1:]]
        if all(c in ("", "-") for c in cells):
            continue  # blank actuals row, filled each Friday
        vals = {}
        for col in SCORECARD_COLUMNS[1:]:
            v = number(r.get(col, ""))
            if v == "bad":
                fail(f"Rep Scorecard '{rep_name}' has a non-numeric {col}: '{r.get(col)}'")
            vals[col] = v
        for col in ("days", "dials", "connects", "conversations", "meetings", "held"):
            if vals[col] is None:
                fail(f"Rep Scorecard '{rep_name}' needs a count for {col}")
        if not (vals["dials"] >= vals["connects"] >= vals["conversations"] >= vals["meetings"] >= vals["held"]):
            fail(f"Rep Scorecard '{rep_name}': counts must shrink dials >= connects >= conversations >= meetings >= held")
        for col, num, den, mult in SCORECARD_RATES:
            if vals[den] == 0:
                if vals[col] not in (None, 0):
                    fail(f"Rep Scorecard '{rep_name}': {col} must be n/a when {den} is 0")
                continue
            if vals[col] is None:
                fail(f"Rep Scorecard '{rep_name}' needs a value for {col}")
            expected = vals[num] / vals[den] * mult
            if abs(vals[col] - expected) > max(0.06, 0.01 * abs(expected)):
                fail(f"Rep Scorecard '{rep_name}': {col} is {vals[col]} but {num}/{den} gives {expected:.2f}")

    # Skill check 8: Mobile Finder at the catalog price wherever it is used; Cost Estimate only when asked for.
    if MOBILE.search(text) and "$0.25" not in text:
        fail("Mobile Finder must be priced at $0.25 per number found")
    cost = secs.get("cost estimate")
    if cost is not None:
        if not DOLLAR.search(cost):
            fail("Cost Estimate has no dollar figure")
        if not re.search(r"total", cost, re.IGNORECASE):
            fail("Cost Estimate needs a total row")

    print(f"PASS - {len(launch)} launch tasks, {len(dialer)} dialer rows, {len(pilot)} pilot weeks over {span} days, {len(objections)} objections, {len(vm)} voicemails, {len(emails)} emails and confirmations, {len(scorecard)} scorecard rows, {len(all_rows)} table rows")
    sys.exit(0)


if __name__ == "__main__":
    main()
