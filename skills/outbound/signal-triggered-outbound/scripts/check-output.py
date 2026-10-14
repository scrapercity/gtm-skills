#!/usr/bin/env python3
"""Check a signal program produced with the signal-triggered-outbound skill.

Usage: check-output.py path/to/signal-program.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.
"""

import hashlib
import re
import sys
from datetime import date

REQUIRED = [
    "Signal Catalog",
    "Scoring Model",
    "Exclusions",
    "Routing and SLAs",
    "First Emails",
    "Pulls and Cost",
    "Launch Plan",
]
# Sections that repeat other sections; the deliverable leaves them out.
DUPLICATE_SECTIONS = ["Program Summary", "Message Angles", "Frameworks Applied", "Quality Check"]
# ScraperCity products by the names a reader sees (never tool ids).
PRODUCTS = [
    "local business database", "lead database", "ecommerce database", "maps", "yelp", "angi",
    "tech stack search", "store leads", "bizbuysell", "distress list", "zillow agents", "crexi",
    "property lookup",
]
OUTSIDE = re.compile(
    r"funding|form d|job post|hiring|job change|new leader|left a customer|departure|intent|press|\bvisit"
    r"|social|engagement|earnings|filing|10-k|10-q|8-k|launch|\bevent|conference|exhibit|sponsor|webinar",
    re.IGNORECASE,
)
PEOPLE = re.compile(r"job change|new leader|left a customer|departure|champion", re.IGNORECASE)
OUTSIDE_LABEL = re.compile(r"other source", re.IGNORECASE)
TOUCH = re.compile(r"\d+\s*(business\s+)?(minute|hour|day|week)s?\b|\bday\s+\d+|\bsame day\b", re.IGNORECASE)
MAX_EMAIL_WORDS = 90
MIN_EMAIL_WORDS = 15
MAX_FIRST_SENTENCE_WORDS = 30
EXCLUSION_CLASSES = {"competitor": "competitors", "vendor": "vendors", "partner": "partners", "agenc": "agencies"}
MIN_WORDS = 600
MIN_TABLE_ROWS = 15
MIN_SIGNALS = 3
MIN_LAUNCH_ROWS = 3
DUP_SENTENCE_WORDS = 10
MAX_DISCLAIMER_WORDS = {"assumed": 2, "illustrative": 2}
TIER_A_RX = re.compile(r"\bA\s+(?:at\s+)?(\d+(?:\.\d+)?)")
TIER_B_RX = re.compile(r"\bB\s+(?:at\s+)?(\d+(?:\.\d+)?)")
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
SIG_ID = re.compile(r"\bS\d+\b")
ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
DOLLAR = re.compile(r"\$\s?\d")
FIELD = re.compile(r"\{\{\s*([a-z0-9_]+)\s*\}\}")
# Internal identifiers the reader cannot use: tool ids, parameters in backticks, code blocks,
# repo paths and skill names.
TOOL_ID = re.compile(
    r"\b(query_[a-z_]+|scrape_[a-z_]+|find_(?:emails|mobiles|people)|validate_emails|check_wallet"
    r"|list_runs|check_run_status|download_results|cancel_run|search_criminal_records)\b"
)
INTERNAL = [
    (re.compile(r"```"), "a code block"),
    (re.compile("built" "with", re.IGNORECASE), "a supplier name; say Tech Stack Search"),
    (re.compile(r"`[a-z]+[A-Z][A-Za-z0-9]*`"), "an API parameter name in backticks"),
    (re.compile(r"\b(references|scripts|templates|examples)/[\w.-]+"), "a repo file path"),
    (re.compile(r"`[a-z0-9]+(?:-[a-z0-9]+)+`"), "a skill or file name in backticks"),
    (re.compile(r"SKILL\.md|check-output"), "a repo file name"),
]
# A generalization about the prospect's world stated as fact. Ask it as a question, or use the
# sender's own measured data in a merge field.
GENERALIZATION = re.compile(
    r"\b(usually|typically|tends? to|on average|in our experience|most (?:teams|companies|leaders|reps"
    r"|managers|stores|brands|founders|buyers))\b",
    re.IGNORECASE,
)
BOOTH_ASK = re.compile(
    r"at (?:your|the) booth[^.?!]*(?:\bminutes?\b|\d{1,2}:\d{2}|\bmeet)|(?:\bminutes?\b|\bmeet\w*)[^.?!]*at (?:your|the) booth",
    re.IGNORECASE,
)
JUNIOR_ROUTE = re.compile(r"junior|below the buyer|individual contributor|\bAE or SDR\b|\brep or SDR\b", re.IGNORECASE)
MISSED_SLA = re.compile(r"\bmiss", re.IGNORECASE)
NEGATIVE_POINTS = re.compile(r"(?:^|[\s(])[-−]\s?\d+")
PAUSE = re.compile(r"pause[^|]*?\d+\s*days?|\d+\s*-?days?[^|]*pause", re.IGNORECASE)
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


def col(row, *prefixes):
    for prefix in prefixes:
        for k, v in row.items():
            if k.startswith(prefix):
                return v
    return ""


def num(s):
    m = re.search(r"-?\d+(\.\d+)?", s.replace(",", ""))
    return float(m.group(0)) if m else None


def to_date(s):
    m = ISO.search(s)
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def check_internal(text):
    m = TOOL_ID.search(text)
    if m:
        fail(f"tool id '{m.group(0)}' in the program; describe the pull in plain words (for example 'Lead Database: VP and C-level sales contacts by domain')")
    for rx, what in INTERNAL:
        m = rx.search(text)
        if m:
            fail(f"'{m.group(0)}' is {what}; the reader gets plain words only")
    for name in DUPLICATE_SECTIONS:
        if re.search(rf"^##\s+{re.escape(name)}\s*$", text, re.MULTILINE | re.IGNORECASE):
            fail(f"section '## {name}' repeats other sections; cut it")
    for word, cap in MAX_DISCLAIMER_WORDS.items():
        n = len(re.findall(rf"\b{word}\b", text, re.IGNORECASE))
        if n > cap:
            fail(f"'{word}' appears {n} times; say it once in the opening lines")


def check_duplicates(text):
    seen = {}
    cleaned = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    for part in re.split(r"[.?!|\n]", cleaned):
        words = re.findall(r"[a-z0-9{}_']+", part.lower())
        if len(words) < DUP_SENTENCE_WORDS:
            continue
        key = " ".join(words)
        if key in seen:
            fail(f"sentence stated twice: '{part.strip()[:80]}'; state each fact once")
        seen[key] = True


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/signal-program.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the program: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    if len(text.split()) < MIN_WORDS:
        fail(f"program has {len(text.split())} words, minimum is {MIN_WORDS}")
    all_rows = table_rows(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"program has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")
    if legal_hit(text):
        fail("program contains legal content; remove it (owner rule) and keep only settings that change results")
    check_internal(text)
    check_duplicates(text)

    # Scoring Model: tier cut-offs and at least one negative signal with points and a pause.
    scoring = table_rows(secs["scoring model"])
    tier_rows = [r for r in scoring if "tier" in r.get("component", "").lower()]
    tier_text = " ".join(" ".join(r.values()) for r in tier_rows)
    ma_, mb_ = TIER_A_RX.search(tier_text), TIER_B_RX.search(tier_text)
    if not (ma_ and mb_):
        fail("Scoring Model needs a Tiers row with the A and B cut-offs, for example 'A 70 and up, B 40 to 69'")
    tier_a, tier_b = float(ma_.group(1)), float(mb_.group(1))
    if not 0 < tier_b < tier_a <= 100:
        fail(f"tier cut-offs must satisfy 0 < B < A <= 100 (got A {tier_a:g}, B {tier_b:g})")
    negatives = [r for r in scoring if "negative" in r.get("component", "").lower()]
    if not negatives:
        fail("Scoring Model needs at least one 'Negative:' row (an event that lowers the score, such as a hiring freeze or a competitor signed)")
    for r in negatives:
        joined = " | ".join(r.values())
        if not NEGATIVE_POINTS.search(joined):
            fail(f"negative row '{r.get('component')}' needs minus points, for example '-25'")
        if not PAUSE.search(joined):
            fail(f"negative row '{r.get('component')}' needs a pause in days, for example 'pause 60 days'")

    # Signal Catalog: each signal names a ScraperCity product or is labeled as outside data,
    # has a touch window, a half-life and a max age at least as long.
    catalog = table_rows(secs["signal catalog"])
    if len(catalog) < MIN_SIGNALS:
        fail(f"Signal Catalog has {len(catalog)} signals, minimum is {MIN_SIGNALS}")
    max_age = {}
    for r in catalog:
        name = r.get("signal", "")
        ids = SIG_ID.findall(name)
        if not ids:
            fail(f"catalog signal '{name}' needs an ID such as S5")
        source = col(r, "source", "tool").lower()
        labeled = bool(OUTSIDE_LABEL.search(source))
        if not any(p in source for p in PRODUCTS) and not labeled:
            fail(f"signal '{name}' names no ScraperCity product and is not labeled 'other source'")
        if OUTSIDE.search(name) and not labeled:
            if not (PEOPLE.search(name) and "lead database" in source):
                fail(f"signal '{name}' is not something ScraperCity tools show; label it 'other source'")
        if not TOUCH.search(col(r, "touch")):
            fail(f"signal '{name}' needs a touch window with a number and a unit (for example '2 business days')")
        hl, ma = num(col(r, "half-life")), num(col(r, "max age"))
        if hl is None or ma is None or hl <= 0:
            fail(f"signal '{name}' needs a numeric half-life and max age")
        if ma < hl:
            fail(f"signal '{name}' max age {ma:g} is shorter than its half-life {hl:g}")
        max_age[ids[0]] = ma

    # Exclusions: competitors, vendors, partners and agencies, each with a match rule.
    found = set()
    for r in table_rows(secs["exclusions"]):
        cls = r.get("class", "").lower()
        if not cls:
            fail("Exclusions row has no class")
        if not r.get("match rule", "").strip():
            fail(f"exclusion class '{cls}' needs a match rule")
        for key, label in EXCLUSION_CLASSES.items():
            if key in cls:
                found.add(label)
    missing = [v for v in EXCLUSION_CLASSES.values() if v not in found]
    if missing:
        fail("Exclusions must list " + ", ".join(missing))

    # Routing: what happens on a missed SLA; a visitor below the buyer goes to the buyer.
    routing = secs["routing and slas"]
    if not table_rows(routing):
        fail("Routing and SLAs needs a table with tier, first touch, SLA and owner")
    prose = "\n".join(l for l in routing.splitlines() if not l.strip().startswith("|"))
    missed_cells = [col(r, "missed") for r in table_rows(routing)]
    if not (MISSED_SLA.search(prose) or any(c and c.lower() not in ("none", "-", "n/a") for c in missed_cells)):
        fail("Routing and SLAs must say what happens when an owner misses the SLA (a 'Missed SLA' column or a sentence)")
    if "S14" in max_age and not JUNIOR_ROUTE.search(routing):
        fail("S14 is tracked, so Routing must send a visitor below the buyer (a rep or SDR) to their buyer")

    # First Emails: one per signal, with an angle line, a merge-field template and field sources.
    emails_sec = secs["first emails"]
    if not re.search(r"^\s*\**claims to confirm", emails_sec, re.IGNORECASE | re.MULTILINE):
        fail("First Emails needs one 'Claims to confirm:' line listing every product capability and proof result the emails use")
    emails = {}
    for block in re.split(r"^###\s+", emails_sec, flags=re.MULTILINE)[1:]:
        head, _, rest = block.partition("\n")
        raw = rest.splitlines()
        quoted = [re.sub(r"^>\s?", "", l).strip() for l in raw if l.strip().startswith(">")]
        plain = [l.strip() for l in raw if l.strip() and not l.strip().startswith(">")]
        subj = [l for l in quoted if l.lower().startswith("subject:")]
        body_lines = [l for l in quoted if l and not l.lower().startswith("subject:")]
        angle = [l for l in plain if re.match(r"\**angle:?\**", l, re.IGNORECASE)]
        fields_line = " ".join(l for l in plain if re.match(r"\**fields:?\**", l, re.IGNORECASE))
        for sid in SIG_ID.findall(head):
            emails[sid] = (subj[0] if subj else "", body_lines, angle, fields_line)
    for sid in max_age:
        if sid not in emails:
            fail(f"signal {sid} has no email under '## First Emails' (a '### {sid} ...' heading)")
        subj, body_lines, angle, fields_line = emails[sid]
        if not angle:
            fail(f"first email for {sid} needs an 'Angle:' line above it")
        if len(subj.split()) < 2:
            fail(f"first email for {sid} needs a 'Subject:' line")
        body = " ".join(body_lines)
        n = len(body.split())
        if not MIN_EMAIL_WORDS <= n <= MAX_EMAIL_WORDS:
            fail(f"first email for {sid} has {n} words in the body; keep it between {MIN_EMAIL_WORDS} and {MAX_EMAIL_WORDS}")
        first = re.split(r"(?<=[.?!])\s", body, maxsplit=1)[0]
        if len(first.split()) > MAX_FIRST_SENTENCE_WORDS:
            fail(f"first sentence of the {sid} email has {len(first.split())} words; keep it at or under {MAX_FIRST_SENTENCE_WORDS}")
        g = GENERALIZATION.search(body)
        if g:
            fail(f"{sid} email states a generalization as fact ('{g.group(0)}'); ask it as a question or use the sender's own data")
        if BOOTH_ASK.search(body):
            fail(f"{sid} email asks an exhibitor for a meeting at their booth; ask the sales leader for a meeting after the show")
        fields = set(FIELD.findall(subj + " " + body))
        if not fields - {"first_name", "company"}:
            fail(f"{sid} email needs a merge field for the event fact (for example {{{{round}}}}), not only name and company")
        if not fields_line:
            fail(f"{sid} email needs a 'Fields:' line naming the source column of each merge field")
        named = set(FIELD.findall(fields_line))
        for f in sorted(fields - named):
            fail(f"{sid} email uses {{{{{f}}}}} but the Fields line does not say where it comes from")

    # Pulls and Cost: frequency and a dollar cost per row, plus a total.
    pulls = table_rows(secs["pulls and cost"])
    if not pulls:
        fail("Pulls and Cost has no rows")
    total = False
    for r in pulls:
        label = " ".join(r.values()).lower()
        if "total" in label:
            total = bool(DOLLAR.search(label))
            continue
        if not col(r, "frequency"):
            fail(f"pull '{col(r, 'pull')}' has no frequency")
        if not DOLLAR.search(" ".join(v for k, v in r.items() if "cost" in k)):
            fail(f"pull '{col(r, 'pull')}' has no dollar cost")
    if not total:
        fail("Pulls and Cost needs a total row with a dollar figure")

    # Launch Plan: dated steps, each with an owner role.
    launch = table_rows(secs["launch plan"])
    if len(launch) < MIN_LAUNCH_ROWS:
        fail(f"Launch Plan has {len(launch)} rows; give at least {MIN_LAUNCH_ROWS} dated steps with owners")
    cycle = None
    for r in launch:
        if not ISO.search(" ".join(r.values())):
            fail(f"Launch Plan row '{col(r, 'step')}' needs an ISO date (YYYY-MM-DD)")
        if not col(r, "owner").strip():
            fail(f"Launch Plan row '{col(r, 'step')}' needs an owner")
        if "first cycle" in " ".join(r.values()).lower():
            cycle = to_date(" ".join(r.values()))

    # Optional Signal Queue (only when real pulls were run): dated, fresh, scored, tiered.
    queue = table_rows(secs.get("signal queue", ""))
    for r in queue:
        acct = r.get("account", "")
        ids = SIG_ID.findall(r.get("signal", ""))
        if not ids:
            fail(f"queue row '{acct}' has no signal ID")
        for sid in ids:
            if sid not in max_age:
                fail(f"queue row '{acct}' uses {sid}, which is not in the Signal Catalog")
        sdate = to_date(r.get("signal date", ""))
        if not sdate:
            fail(f"queue row '{acct}' needs an ISO signal date (YYYY-MM-DD)")
        age = num(col(r, "age"))
        if age is None:
            fail(f"queue row '{acct}' has no age")
        if cycle and int(age) != (cycle - sdate).days:
            fail(f"queue row '{acct}' age {age:g} does not match first cycle date minus signal date ({(cycle - sdate).days})")
        if age > max(max_age[s] for s in ids):
            fail(f"queue row '{acct}' is {age:g} days old, past the signal's max age")
        score = num(r.get("score", ""))
        if score is None or not 0 <= score <= 100:
            fail(f"queue row '{acct}' needs a score from 0 to 100")
        tier = r.get("tier", "").strip().upper()[:1]
        expected = "A" if score >= tier_a else "B" if score >= tier_b else "C"
        if tier != expected:
            fail(f"queue row '{acct}' score {score:g} should be tier {expected}, not {tier or 'blank'}")

    print(f"PASS - {len(catalog)} signals, {len(emails)} first emails, {len(negatives)} negative signals, "
          f"{len(launch)} launch steps, tiers A {tier_a:g} and B {tier_b:g}, {len(all_rows)} table rows")
    sys.exit(0)


if __name__ == "__main__":
    main()
