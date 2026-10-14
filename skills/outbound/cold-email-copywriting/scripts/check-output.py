#!/usr/bin/env python3
"""Check a cold email sequence produced with the cold-email-copywriting skill.

Usage: check-output.py path/to/sequence.md [path/to/sequence-worksheet.md]
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.

Two files. The sequence is what the client reads; the worksheet holds the inputs the
checker needs and the client does not (it defaults to '<sequence stem>-worksheet.md'
next to the sequence; run on a worksheet, the checker checks its sequence).

Sequence, answer first: a one-line header, then '## Copy Audit' (audit mode only),
'## Sequence' (a sending line, then '### Touch N' blocks with 'Thread:', 'Subject:',
'Subject B:', 'Send day:' and a fenced body ending with one ask and a sign-off),
'## Variants' ('### Variant ...' blocks with 'Kind:', 'For:', 'Gate:', 'Subject:' and a
fenced body), '## Footer' (fenced, no table), '## Merge Fields and Fallbacks' (Tag,
List column, Fallback), '## Test Plan' (table plus a 'Decide:' line) and
'## Confirm Before Launch'.

Worksheet: '## Campaign Inputs' (Mode, Segment markers, Their words, Facts from the brief,
Reply offer with a delivery time, Likely objection rows), '## Fill Rates' (Tag, Fill rate
in sample) and '## Touch Map' (Touch, Type, Adds).
"""

import re
import sys
from pathlib import Path

SEQUENCE_SECTIONS = ["Sequence", "Variants", "Footer", "Merge Fields and Fallbacks", "Test Plan", "Confirm Before Launch"]
WORKSHEET_SECTIONS = ["Campaign Inputs", "Fill Rates", "Touch Map"]
# Internal working material that belongs in the worksheet, not in the client's document.
WORKSHEET_ONLY = ["campaign inputs", "fill rates", "touch map"]
REQUIRED_INPUT_ROWS = ["mode", "segment markers", "their words", "facts from the brief", "reply offer", "likely objection"]
MAX_BODY_WORDS = 99  # every body under 100 words (Jason Bay, Gong blog, July 2025)
MAX_SUBJECT_CHARS = 49  # under 50 characters (Alex Berman, templates page)
MIN_PER_ARM = 100  # 100 to 200+ emails per variation (Alex Berman, templates page)
MIN_TOUCHES = 3
MIN_AUDIT_ROWS = 3
MAX_SIGNOFF_WORDS = 4
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
TAG = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*(\|[^}]*)?\}\}")
LINK = re.compile(r"https?://|www\.|\b[a-z0-9-]+\.(?:com|io|co|net|org|ai)\b", re.IGNORECASE)
GREETING = re.compile(r"^(hi|hello|hey|dear)\b", re.IGNORECASE)
SELLER_OPENING = re.compile(r"^(i|i'm|i've|i'd|we|we're|we've|our|my)\b", re.IGNORECASE)
NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")
# Ratios written as words are claims too: "half as many", "twice the", "a third".
WORD_RATIO = re.compile(r"\b(half|halved|twice|double[sd]?|triple[sd]?|a third|two thirds|a quarter|three quarters|(?:two|three|four|five|ten) times)\b", re.IGNORECASE)
CALL_LENGTH = re.compile(r"^\s*(?:-|to\s+\d+\s*)?\s*(minute|minutes|min)\b", re.IGNORECASE)
GENERIC_ADDS = re.compile(r"\b(follow(ing)?[- ]up|checking in|check in|bump|reminder|circle back|touch base|nothing new|same as)\b", re.IGNORECASE)
# Owner rule: no legal content. Laws, regulators, legal citations and disclaimers fail.
LEGAL = re.compile(
    r"\b(can.?spam|tc[p]a|casl|gd[p]r|ccpa|cpra|pecr|fcra|hipaa|tsr|telemarketing sales rule|"
    r"ftc|fcc|crtc|ico|cfpb|attorn[e]ys? general|\d+\s*c\.?f\.?r|u\.s\.c|lawful\s+basis|legal\s+advice|not\s+legal|"
    r"lawy[e]rs?|attorn[e]ys?|counsel|do.?not.?call\s+registry|compliance|regulat\w*|statute|consent|penalt\w+)\b",
    re.IGNORECASE,
)
LEAK = re.compile(r"references/|scripts/|check-output|SKILL\.md|`(?:scrape_\w+|query_\w+|find_emails|find_people|find_mobiles|validate_emails|check_wallet)`")
BRACKET_BLANK = re.compile(r"\[[A-Za-z][^\]\n]{0,60}\](?!\()")
UNLINKED_SOURCE = re.compile(
    r"\b(berman|venetz|nowoslawski|josh braun|jason bay|schwartz|craig elias|jordan crawford|"
    r"sender rules|follow-up guide|templates page)\b",
    re.IGNORECASE,
)
UNMEASURED_FILL = re.compile(r"assumed|unknown|unmeasured|not measured|not sampled|\blow\b", re.IGNORECASE)
DELIVERY_TIME = re.compile(r"\b(within|by|same day|next day|\d+\s*(business\s+)?(hours?|days?|weeks?))\b", re.IGNORECASE)
TIME_ZONE = re.compile(r"time zone|\b(MT|ET|CT|PT|UTC|GMT|CET)\b|mountain|eastern|central|pacific|local time", re.IGNORECASE)
INTERNAL_LINE = re.compile(r"^(Type|Adds|Framework|Word count|Rationale):", re.MULTILINE)
QA_LEFTOVER = re.compile(r"fill rate|rendered on a row|empty-row render", re.IGNORECASE)


def fail(msg):
    print(f"FAIL - {msg}")
    sys.exit(1)


def sections(text, level="##"):
    out, current = {}, None
    pat = re.compile(r"^" + level + r"\s+(.+?)\s*$")
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else pat.match(line)
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
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", lines[j].strip("|"))]
                rows.append(dict(zip(head, cells)))
                j += 1
    return rows


def inputs_row(block, name):
    for r in table_rows(block):
        if r.get("field", "").strip().lower() == name:
            return r.get("value", "").strip()
    return ""


def body_words(body):
    flat = TAG.sub("X", body)
    return len(re.findall(r"[A-Za-z0-9$%][A-Za-z0-9$%'.,:/-]*", flat))


def content_lines(body):
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    if lines and GREETING.match(lines[0]):
        lines = lines[1:]
    return lines


def sentences(body):
    return [x for x in re.split(r"(?<=[.?!])\s+", " ".join(content_lines(body))) if x]


def fenced(block):
    m = re.search(r"```[a-z]*\n(.*?)```", block, re.DOTALL)
    return m.group(1).strip() if m else None


def voice_check(label, body):
    """Leslie Venetz (1-10-100 post): do not open with I, we or our (greeting excluded)."""
    lines = content_lines(body)
    if not lines:
        fail(f"{label} has no body after the greeting")
    if SELLER_OPENING.match(lines[0]):
        fail(f"{label} opens with a seller word ('{lines[0][:40]}'); lead with the reader or the proof")


def unsupported_claims(body, inputs):
    flat = TAG.sub(" ", body)
    known = inputs.replace(",", "")
    out = []
    for m in NUMBER.finditer(flat):
        if CALL_LENGTH.match(flat[m.end():]):
            continue
        digits = m.group(0).strip("$%").replace(",", "").rstrip(".")
        if not re.search(r"(?<![\d.])" + re.escape(digits) + r"(?![\d])", known):
            out.append(m.group(0))
    for m in WORD_RATIO.finditer(flat):
        if not re.search(r"\b" + re.escape(m.group(0)) + r"\b", inputs, re.IGNORECASE):
            out.append(m.group(0))
    return out


def numbers_in(body):
    return {m.group(0).strip("$%").replace(",", "").rstrip(".") for m in NUMBER.finditer(TAG.sub(" ", body))}


def check_subject(label, s_):
    visible = TAG.sub(lambda m: m.group(1), s_)
    if len(visible) > MAX_SUBJECT_CHARS:
        fail(f"{label} subject '{s_}' is {len(visible)} characters, keep it under 50")


def check_tags(label, text, fields):
    for m in TAG.finditer(text):
        name = m.group(1)
        if name.upper() == "RANDOM":
            continue
        if name not in fields:
            fail(f"{label} uses {{{{{name}}}}} which is not listed in Merge Fields and Fallbacks")
        if not fields[name] or fields[name].lower() in ("none", "-", "n/a"):
            fail(f"merge field '{name}' has no fallback")


def split_signoff(label, body):
    """Every body ends with the ask and then a short sign-off line."""
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    sign = lines[-1] if lines else ""
    if len(lines) < 3 or "?" in sign or len(TAG.sub("X", sign).split()) > MAX_SIGNOFF_WORDS:
        fail(f"{label} must end with a sign-off line (the sender's first name or {{{{sender_first_name}}}}) after the ask; last line is '{sign[:60]}'")
    return lines[:-1]


def check_ask(label, body):
    """One ask (Venetz, one low-effort ask): exactly one question mark, on the line before the sign-off."""
    last = split_signoff(label, body)[-1]
    if not last.endswith("?"):
        fail(f"{label} must end with its one question before the sign-off; that line is '{last[:60]}'")
    if body.count("?") != 1:
        fail(f"{label} has {body.count('?')} question marks; one ask only, so the opener is a statement")


def check_opening(label, body, markers):
    """First-touch rule: the proof (a number) or a segment marker within the first two sentences."""
    opening = " ".join(sentences(body)[:2]).lower()
    if not (re.search(r"\d", TAG.sub(" ", opening)) or any(m in opening for m in markers)):
        fail(f"{label} must show the proof (a number) or the segment within its first two sentences")


def check_markers(label, body, markers):
    """Name every segment marker the user gave, as the slice you serve, never as a label on the reader's property."""
    flat = TAG.sub(" ", body).lower()
    missing = [m for m in markers if m not in flat]
    if missing:
        fail(f"{label} does not name the segment marker(s) {', '.join(missing)}; say the slice you serve ('we clean Class B office buildings in Denver')")
    for m in markers:
        hit = re.search(r"\byour\s+(?:[\w-]+\s+)?" + re.escape(m) + r"\b", flat)
        if hit:
            fail(f"{label} labels the reader's own business with the segment marker ('{hit.group(0)}'); name the slice you serve instead")


def check_body(label, body, inputs, markers):
    made_up = unsupported_claims(body, inputs)
    if made_up:
        fail(f"{label} uses {', '.join(made_up)}, which is not in the worksheet's Campaign Inputs; facts come from the brief only")
    words = body_words(body)
    if words > MAX_BODY_WORDS:
        fail(f"{label} body has {words} words; every body must be under 100")
    voice_check(label, body)
    for m in markers:
        hit = re.search(r"\byour\s+(?:[\w-]+\s+)?" + re.escape(m) + r"\b", TAG.sub(" ", body).lower())
        if hit:
            fail(f"{label} labels the reader's own business with the segment marker ('{hit.group(0)}'); name the slice you serve instead")
    return words


def check_audit(secs, markers):
    if "copy audit" not in secs:
        fail("Mode is audit but '## Copy Audit' is missing")
    audit = secs["copy audit"]
    named = sections(audit, "###")
    for need in ("original", "rewrite"):
        if need not in named or fenced(named[need]) is None:
            fail(f"Copy Audit needs '### {need.title()}' with the email in a fenced block")
    rows = table_rows(audit)
    if len(rows) < MIN_AUDIT_ROWS:
        fail(f"Copy Audit has {len(rows)} issue rows, minimum is {MIN_AUDIT_ROWS}")
    for r in rows:
        for col in ("line", "issue", "fix"):
            if not r.get(col):
                fail(f"Copy Audit row '{r.get('line', '?')[:30]}' has no {col}")
    rewrite = fenced(named["rewrite"])
    if body_words(rewrite) > MAX_BODY_WORDS:
        fail(f"Copy Audit rewrite has {body_words(rewrite)} words; keep it under 100")
    check_ask("Copy Audit rewrite", rewrite)
    voice_check("Copy Audit rewrite", rewrite)
    return len(rows)


def resolve_paths(argv):
    first = Path(argv[1])
    if len(argv) == 3:
        return first, Path(argv[2])
    if first.stem.endswith("-worksheet"):
        return first.with_name(first.stem[: -len("-worksheet")] + first.suffix), first
    return first, first.with_name(first.stem + "-worksheet" + first.suffix)


def main():
    if len(sys.argv) not in (2, 3):
        print("usage: check-output.py path/to/sequence.md [path/to/sequence-worksheet.md]")
        sys.exit(2)
    seq_path, ws_path = resolve_paths(sys.argv)
    try:
        text = seq_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"usage: cannot read {seq_path}: {exc}")
        sys.exit(2)
    try:
        sheet = ws_path.read_text(encoding="utf-8")
    except OSError:
        fail(f"worksheet {ws_path.name} not found; keep the inputs, fill rates and touch map there, not in the client's document")

    for label, doc in (("sequence", text), ("worksheet", sheet)):
        hit = PLACEHOLDER.search(doc)
        if hit:
            fail(f"placeholder left in the {label}: {hit.group(0)}")
        legal = LEGAL.search(doc)
        if legal:
            fail(f"{label} contains legal content ('{legal.group(0)}'); state the setting and the result it protects instead")

    # The client's document.
    blank = BRACKET_BLANK.search(text)
    if blank:
        fail(f"blank left in the sequence: {blank.group(0)}; use a merge tag with a fallback or a Confirm Before Launch item")
    leak = LEAK.search(text)
    if leak:
        fail(f"working note '{leak.group(0)}' left in the sequence; the client reads emails, not file paths or tool ids")
    for line in text.splitlines():
        src = UNLINKED_SOURCE.search(line)
        if src and not re.search(r"https?://", line):
            fail(f"'{src.group(0)}' is cited without a link ('{line.strip()[:60]}'); state the choice as a choice or link the page")
    internal = INTERNAL_LINE.search(text)
    if internal:
        fail(f"'{internal.group(0)}' lines describe the email under them; keep them in the worksheet's Touch Map")
    secs = sections(text)
    for name in WORKSHEET_ONLY:
        if name in secs:
            fail(f"'## {name.title()}' belongs in the worksheet; the client's document holds emails and decisions")
    qa = QA_LEFTOVER.search(text)
    if qa:
        fail(f"'{qa.group(0)}' is internal QA; keep it in the worksheet")
    first = next(iter(secs), "")
    if first not in ("copy audit", "sequence"):
        fail(f"the first section is '## {first}'; answer first: start with '## Sequence' (or '## Copy Audit' in audit mode)")
    header = text.split("\n## ", 1)[0]
    header_lines = [l for l in header.splitlines()[1:] if l.strip()]
    if len(header_lines) > 1:
        fail("the header holds more than one line under the title; open questions go once, in Confirm Before Launch")
    for name in SEQUENCE_SECTIONS:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")

    # The worksheet.
    wsecs = sections(sheet)
    for name in WORKSHEET_SECTIONS:
        if name.lower() not in wsecs:
            fail(f"worksheet is missing '## {name}'")
    inputs = wsecs["campaign inputs"]
    for row in REQUIRED_INPUT_ROWS:
        if not inputs_row(inputs, row):
            fail(f"worksheet Campaign Inputs needs a filled '{row.capitalize()}' row")
    offer = inputs_row(inputs, "reply offer")
    if not DELIVERY_TIME.search(offer):
        fail("Reply offer row must say when the reader gets it (for example 'within 3 business days')")
    confirm = secs["confirm before launch"]
    if offer.lower().startswith("proposed") and "offer" not in confirm.lower() and "walkthrough" not in confirm.lower():
        fail("the reply offer is proposed, so Confirm Before Launch must ask the user to confirm it")
    if not confirm.strip():
        fail("Confirm Before Launch is empty; list each open question once, or write 'Nothing open.'")
    mode = inputs_row(inputs, "mode").lower()
    if not mode.startswith(("write", "audit")):
        fail("Campaign Inputs needs a Mode row set to 'write' or 'audit'")
    terms = [t.strip().lower() for t in re.split(r"[,;]", inputs_row(inputs, "their words")) if t.strip()]
    markers = [t.strip().lower() for t in re.split(r"[,;]", inputs_row(inputs, "segment markers")) if t.strip()]
    if not terms or not markers:
        fail("Campaign Inputs needs comma-separated 'Their words' and 'Segment markers'")
    audit_rows = check_audit(secs, markers) if mode.startswith("audit") else 0

    fill = {r.get("tag", "").strip("`{} "): r.get("fill rate in sample", "") for r in table_rows(wsecs["fill rates"])}
    unmeasured = {t for t, f in fill.items() if UNMEASURED_FILL.search(f)}
    touch_map = {r.get("touch", "").strip(): r for r in table_rows(wsecs["touch map"])}

    fields = {}
    for r in table_rows(secs["merge fields and fallbacks"]):
        tag = r.get("tag", "").strip("`{} ")
        if tag:
            fields[tag] = r.get("fallback", "")
            if tag not in fill:
                fail(f"merge field '{tag}' has no row in the worksheet's Fill Rates")
    if not fields:
        fail("Merge Fields and Fallbacks has no rows")

    def check_default_subject(label, subject):
        for m in TAG.finditer(subject):
            if m.group(1) in unmeasured:
                fail(f"{label} default Subject depends on '{m.group(1)}', whose fill rate is not measured; make the tag-free subject the default and test the tagged one as Subject B")

    seq = secs["sequence"]
    sending = seq.split("\n### ", 1)[0]
    if not TIME_ZONE.search(sending) or "per inbox" not in sending.lower():
        fail("the Sequence opens with a sending line: send days, window in the recipient's time zone, cap per inbox per day, threading")
    touches = re.split(r"^###\s+Touch\s+(\d+)\s*$", seq, flags=re.MULTILINE)
    blocks = list(zip(touches[1::2], touches[2::2]))
    if len(blocks) < MIN_TOUCHES:
        fail(f"Sequence has {len(blocks)} touches, minimum is {MIN_TOUCHES}")

    longest = no_ask = objection = 0
    subjects, adds_seen, touch_numbers, all_bodies = {}, {}, {}, []
    for num, block in blocks:
        label = f"touch {num}"
        row = touch_map.get(num) or touch_map.get(f"touch {num}") or touch_map.get(f"Touch {num}")
        if not row:
            fail(f"{label} has no row in the worksheet's Touch Map (Type, Adds)")
        kind, reason = row.get("type", ""), " ".join(row.get("adds", "").lower().split())
        if len(reason.split()) < 3:
            fail(f"{label} Touch Map 'Adds' must name the new reason to reply (3+ words)")
        if GENERIC_ADDS.search(reason):
            fail(f"{label} Touch Map 'Adds' is a bump ('{reason[:40]}'); every touch needs a new fact, offer, answer or route")
        if reason in adds_seen:
            fail(f"{label} adds the same thing as touch {adds_seen[reason]}; every touch needs a new reason to reply")
        adds_seen[reason] = num
        if "objection" in kind.lower():
            objection += 1
        subj = re.search(r"^Subject:\s*(.+)$", block, re.MULTILINE)
        alt = re.search(r"^Subject B:\s*(.+)$", block, re.MULTILINE)
        thread = re.search(r"^Thread:\s*(.+)$", block, re.MULTILINE)
        if not subj or not alt:
            fail(f"{label} needs 'Subject:' and 'Subject B:'")
        if not thread:
            fail(f"{label} has no Thread line (new, or reply to touch N)")
        subject, subject_b, how = subj.group(1).strip(), alt.group(1).strip(), thread.group(1).strip().lower()
        subjects[num] = (subject, subject_b)
        for s_ in (subject, subject_b):
            check_subject(label, s_)
        parent = re.match(r"reply to touch\s+(\d+)", how)
        if num == "1" and not how.startswith("new"):
            fail("touch 1 must start a new thread")
        if parent:
            if parent.group(1) not in subjects:
                fail(f"{label} replies to touch {parent.group(1)}, which does not come before it")
            for mine, theirs in zip((subject, subject_b), subjects[parent.group(1)]):
                if " ".join(mine.lower().split()) != " ".join(("re: " + theirs).lower().split()):
                    fail(f"{label} is a reply, so its subject should be 'Re: {theirs}', got '{mine}'")
        elif how.startswith("new"):
            for s_ in (subject, subject_b):
                if re.match(r"(re|fwd?):", s_, re.IGNORECASE):
                    fail(f"{label} starts a new thread but its subject fakes a reply or forward")
        else:
            fail(f"{label} Thread must be 'new' or 'reply to touch N', got '{how}'")
        if not re.search(r"^Send day:\s*\S", block, re.MULTILINE):
            fail(f"{label} has no Send day")
        body = fenced(block)
        if body is None:
            fail(f"{label} body must be in a fenced code block")
        all_bodies.append(body)
        longest = max(longest, check_body(label, body, inputs, markers))
        touch_numbers[num] = numbers_in(body)
        if num == "1":
            check_default_subject(label, subject)
            check_opening(label, body, markers)
            check_markers(label, body, markers)
        if "no ask" in kind.lower():
            no_ask += 1
            if num == "1":
                fail("touch 1 cannot be a no-ask touch")
            if "?" in body:
                fail(f"{label} is marked no ask but contains a question mark")
            split_signoff(label, body)
        else:
            check_ask(label, body)
        links = len(LINK.findall(TAG.sub("", body)))
        if num == "1" and links:
            fail("touch 1 must not contain a link")
        if links > 1:
            fail(f"{label} has {links} links; one maximum")
        check_tags(label, body + "\n" + subject + "\n" + subject_b, fields)

    if no_ask > 1:
        fail(f"{no_ask} touches are marked no ask; one maximum per sequence")
    if not objection:
        fail("no touch answers the Likely objection; mark one Touch Map Type 'objection ...' and answer it head-on")
    proof = touch_numbers.get("1", set())
    if proof and not any(proof & nums for n, nums in touch_numbers.items() if n != "1"):
        fail("touch 1's proof number appears in no follow-up; restate it in one line in a later touch")

    variants = re.split(r"^###\s+Variant\b[^\n]*$", secs["variants"], flags=re.MULTILINE)[1:]
    if not variants:
        fail("Variants needs at least one '### Variant' block (persona or signal)")
    for i, block in enumerate(variants, 1):
        label = f"variant {i}"
        kind = re.search(r"^Kind:\s*(persona|signal)\b", block, re.MULTILINE | re.IGNORECASE)
        who = re.search(r"^For:\s*(.+)$", block, re.MULTILINE)
        gate = re.search(r"^Gate:\s*(.+)$", block, re.MULTILINE)
        subj = re.search(r"^Subject:\s*(.+)$", block, re.MULTILINE)
        if not kind:
            fail(f"{label} needs 'Kind: persona' or 'Kind: signal'")
        if not who or not gate or not subj:
            fail(f"{label} needs For:, Gate: and Subject: lines")
        if kind.group(1).lower() == "signal" and not re.search(r"`[a-z_]+`", gate.group(1)):
            fail(f"{label} is a signal variant; its Gate must name the list field that verifies the signal, in backticks")
        if len(gate.group(1).split()) < 4:
            fail(f"{label} Gate must say which rows get it and what the rest get")
        subject = subj.group(1).strip()
        check_subject(label, subject)
        check_default_subject(label, subject)
        if re.match(r"(re|fwd?):", subject, re.IGNORECASE):
            fail(f"{label} subject fakes a reply or forward")
        body = fenced(block)
        if body is None:
            fail(f"{label} body must be in a fenced code block")
        all_bodies.append(body)
        longest = max(longest, check_body(label, body, inputs, markers))
        check_opening(label, body, markers)
        check_markers(label, body, markers)
        check_ask(label, body)
        if LINK.findall(TAG.sub("", body)):
            fail(f"{label} replaces touch 1, so it must not contain a link")
        check_tags(label, body + "\n" + subject, fields)

    copy = " ".join(all_bodies).lower()
    used = [t for t in terms if t in copy or (t.endswith("s") and t[:-1] in copy)]
    if not used:
        fail("none of the segment's own terms (Their words) appear in the bodies")

    test = secs["test plan"]
    rows = table_rows(test)
    if not rows:
        fail("Test Plan needs a table with at least one test")
    for r in rows:
        n = re.search(r"\d[\d,]*", r.get("per variant", ""))
        if not n or int(n.group(0).replace(",", "")) < MIN_PER_ARM:
            fail(f"Test Plan row '{r.get('test', '?')[:30]}' needs at least {MIN_PER_ARM} delivered per variant")
    if not re.search(r"^Decide:", test, re.MULTILINE):
        fail("Test Plan needs a 'Decide:' line saying when a gap between arms is large enough to act on")

    footer = secs["footer"]
    if table_rows(footer):
        fail("Footer holds a table; the footer is the sender line and the opt-out line, nothing else")
    if fenced(footer) is None:
        fail("Footer must be the sender line and opt-out line in a fenced block")
    if not re.search(r"unsubscribe|opt[- ]?out|reply .*no|won't follow up|will not follow up", footer, re.IGNORECASE):
        fail("Footer needs an opt-out line")

    audit_note = f", audit with {audit_rows} line-level issues" if audit_rows else ""
    print(f"PASS - {'audit' if mode.startswith('audit') else 'write'} mode, {len(blocks)} touches with A/B subjects and a new reason each, {len(variants)} gated variants, objection answered, longest body {longest} words, {len(used)} segment terms used, {len(fields)} merge fields with fallbacks{audit_note}")
    sys.exit(0)


if __name__ == "__main__":
    main()
