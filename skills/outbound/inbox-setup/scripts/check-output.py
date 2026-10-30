#!/usr/bin/env python3
"""Check a finished mailbox roster and ramp plan.

Usage: check-output.py path/to/roster.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import hashlib
import re
import sys
from datetime import date
from pathlib import Path

REQUIRED = [
    "Summary",
    "Sender Identities",
    "Mailbox Roster",
    "Account Settings",
    "Signature Block",
    "Warmup and Ramp Schedule",
    "Sending Rules",
    "Reply Monitoring",
    "Rotation and Retirement",
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
TOOL_ID = re.compile(
    r"\b(check_wallet|query_lead_database|query_local_business_database|validate_emails|find_emails|check_run_status|"
    r"download_results|scrape_[a-z_]+|sc_mx_[a-z_]+|pagination\.[a-z_]+|run_?id)\b",
    re.IGNORECASE,
)
INTERNAL_REF = re.compile(
    r"references/|\.md\b|SKILL\.md|scripts/check-output|\bsection \d|\b(domain-infrastructure|email-deliverability|"
    r"sending-platforms|reply-handling|cold-email-copywriting|cold-email-strategy|inbox-setup)\b",
    re.IGNORECASE,
)
MIN_CHARS = 3500
MAX_CAP = 50  # Alex Berman: under 50 a day per inbox
MAX_START = 20  # Alex Berman: start new domains at 10 to 20 a day (Instantly's slow ramp starts at 2)
MIN_WARMUP_DAYS = 14  # Instantly: at least 2 weeks of warmup before campaigns
STANDARD_WARMUP_DAYS = 21  # Instantly: 3 weeks for its own AirMail accounts
OPT_OUT = re.compile(r"unsubscribe|opt[ -]?out|no thanks|won't follow up|will not follow up|remove", re.IGNORECASE)
IMAGE = re.compile(r"!\[|<img|https?://\S+\.(png|jpe?g|gif)", re.IGNORECASE)
# Economy: filler a reader cannot act on, and justifications for a rule the roster already states.
FILLER = re.compile(
    r"capacity check|tenant quota check: not needed|well (inside|within)|invented name|made-up|no personas|fake persona|"
    r"not run yet|nothing was run|results? (below )?(is|are) assumed|frameworks applied|quality check",
    re.IGNORECASE,
)
# Instantly's warmup settings page: slow warmup is skipped only for already-warmed accounts.
SLOW_WARMUP_WRONG = re.compile(r"\bslow warmup (on|enabled)\b|disable slow warmup:? (on|yes|enabled)", re.IGNORECASE)
SHINGLE = 10  # words; the same 10-word run in two prose paragraphs means a fact is stated twice


def prose_paragraphs(text):
    """Paragraphs outside tables, headings and code blocks."""
    out, buf, code = [], [], False
    for line in text.splitlines() + [""]:
        s = line.strip()
        if s.startswith("```"):
            code = not code
            continue
        if code or s.startswith("|") or s.startswith("#") or not s:
            if buf:
                out.append(" ".join(buf))
                buf = []
            continue
        buf.append(s)
    return out


def repeated_run(text):
    seen = {}
    for i, para in enumerate(prose_paragraphs(text)):
        words = re.findall(r"[a-z0-9%$.,:-]+", para.lower())
        for j in range(len(words) - SHINGLE + 1):
            run = " ".join(words[j:j + SHINGLE])
            if run in seen and seen[run] != i:
                return run
            seen.setdefault(run, i)
    return None


# Deliverables carry no legal content (owner rule, 2026-10-13). Stored as SHA-256 hashes of
# lowercase words so the checker itself names no law, regulator or legal term.
LEGAL_WORDS = {
    "9d8be820823bd8b1ceecaef063aea4c28da6f22fc8565985b17f05a49e04620c",
    "f63dd214824a68974443cba568eb6ef8af02ef2b3aa5848cb567b2a9b7b33eee",
    "df679e72d63dc69befbe502d5e155258ca356fa1ac5ab7b47aab9c990f9586c1",
    "8d53e0154b79535cda4bda2c9ad960af9bf320002ce8d8365c7a0a56f4f897f9",
    "8b16477e3abe1de345a6e82f360db77b5e238983ad685cec9fef0d0bc009aed3",
    "467f0ea7dd59072ccaa8dcd5901728a463e3d9a9e13d2c676fd2dc80c891124f",
    "0c89db9e0a961c3939fb277192805c817fdf6b611e353477970af73ad9b54236",
    "ca30ed14f4d400b853d9b111688395db1d75a5583539d9841b2209d0b9d8400c",
    "fa193c8cc820b3b216502909af65a353a26b670c77833006d7dca1144bfb6950",
    "9f6bbaad419acd37b0d06e775bb1d28533a0cefdef0c245d769af00a80eef975",
    "88b1fe38cf4efddeccb0a6b068134a319c9bcd5bd5fefb53b1addebd8481bf8b",
    "0d4bf5b068aa598c06488809d6c39af7d3f9e2c8dcbd5324cd8fdd26b3135a19",
    "b0c50e9b35b69e48852157aa642adbf411eb3239fc49d5d0f90b38739ee38789",
    "83a70052504733134861af25c442ffd741935da314c948f2e015a93b2d0af6ed",
    "6c0a579f38b0e548486f32f9e6d1585102d1050e2d50293a324405735e2f7d78",
    "5561ba03cac2c86f883ddbe7966f05c12375f0ce18fe8a0938733d170887fe76",
    "1244377974aeb11cf1b66db5a33bb15b58ec15d72a6e807157d50e62b642de25",
    "ff9a0c76596a5d3c658f760c483cc2b927d118bc84c52d8ea2146a0cf2a4c9f6",
    "503acf004b50b4f97beae09309f837a2ba47afacc83800fce9a1066813c7a97d",
    "c1818e804aa575636570432284eb15ef692087ef09f6542c1b302bd6f7bb4419",
    "383b6630e8241d34d54bfd689decc0cab88770d935667989a3a1de8397f5520f",
    "b3466e5f75eb27dabd63b94b3fee826acd9de192d400569b894d7685e814dd8a",
    "fe98a4b07a9f4ee4ec6638054f073defc31b0f216a4e38f46361c1e62bc788a2",
    "4ad92a45689299fb31cec0c4d2912f4f98218da1f61c632567362818645161d5",
    "a708df92c9e46229e8f1cd50d8b7d172bda33fc24c8d96d7e9dabf6eba73baa2",
    "56b018aa31b599aff57344518c93e4043dc226dfca697f070cad6fc7efe5fd32",
    "114ece8d992faac0dbffa9f93988ea242de90980817208ac293e8f4b576cf886",
    "32c7e7f733686af37e445a31fb5a1b1162aeec85e4767cb7c236f8e6713014f5",
    "4e73ff840ac8644a388365f8b5cff0b016219096686f4e6f552523dc9bb61c0c",
    "12423e0482f3e81cb1d23230664e95bb3d11b9f34f06fc199e588d4cdab6e4d4",
    "debfc54303301ee216c165f277f4094db60962efc92a3e24d74dddabeac6cf51",
    "12a695850d2cc58a6d0f266fff22d9bd4a85508157105ebdfce247cd1e89870e",
    "1dfb1d06942d61e4bb81e92075ddc5808aa30e3f2dfca4ed99180c56ecee79ac",
    "b85b91c53558d46dfdbd0c469e03525ecc57106fbea8cbea5fd38884d3a26eec",
    "34a9415adb8a8e59cde74cd06c19257660caf41123a6c6f2829aa13d3070836e",
    "bcd3a888401fba8a4b040456cbc53acfab3c7e1de94a1a4d55ba5a8f852a4ea6",
}


def legal_word(text):
    for word in re.findall(r"[a-z][a-z-]+", text.lower()):
        if hashlib.sha256(word.encode()).hexdigest() in LEGAL_WORDS:
            return True
    return False


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


def tables(block):
    """Return a list of (header, rows) for every markdown table in block."""
    found, rows = [], []
    for line in block.splitlines() + [""]:
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                rows.append(cells)
            continue
        if rows:
            found.append(([h.lower() for h in rows[0]], rows[1:]))
            rows = []
    return found


def table(block):
    t = tables(block)
    return t[0] if t else ([], [])


def col(header, *names):
    for i, h in enumerate(header):
        if any(n in h for n in names):
            return i
    return -1


def first_int(s):
    m = re.search(r"\d+", s)
    return int(m.group(0)) if m else None


def parse_date(s):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def fail(msg):
    print(f"FAIL - {msg}")
    return 1


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/roster.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"usage: file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    if legal_word(text):
        return fail("deliverable carries legal content; remove it (owner rule)")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    sec = sections(text)
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")
    hit = TOOL_ID.search(text)
    if hit:
        return fail(f"agent tool id in the roster: {hit.group(0)}; say what was checked in plain words")
    hit = INTERNAL_REF.search(text)
    if hit:
        return fail(f"roster cites an internal file or skill: {hit.group(0)}")
    if re.search(r"reply-to[^\n|]{0,60}@", text, re.IGNORECASE):
        return fail("a Reply-To header points at another address; keep replies on the sending mailbox")
    hit = FILLER.search(text)
    if hit:
        return fail(f"filler or justification the reader cannot act on: '{hit.group(0)}'; state the setting only")
    if SLOW_WARMUP_WRONG.search(text):
        return fail("slow warmup must stay on for new accounts: write 'Disable slow warmup: off' (Instantly warmup settings)")
    run = repeated_run(text)
    if run:
        return fail(f"the same fact is written in two paragraphs ('{run}'); state it once")
    for line in text.splitlines():
        if re.search(r"health", line, re.IGNORECASE) and "90%" in line and not re.search(r"readiness", line, re.IGNORECASE):
            return fail("each health-score line names its source: 'above 90% (Instantly readiness guide)'")
        if "Apollo" in line and not re.search(r"sending limits", line, re.IGNORECASE):
            return fail("each Apollo figure names its article: 'Apollo, Email Sending Limits'")
    for needle, why in (("v=spf1", "SPF value"), ("_domainkey", "DKIM host"), ("v=DMARC1", "DMARC value")):
        if needle.lower() not in text.lower():
            return fail(f"DNS records need their exact values; missing the {why} ({needle})")
    if "postmaster" in text.lower() and not re.search(
        r"(register|verify|add)[^\n]{0,80}postmaster|postmaster[^\n]{0,80}(register|verif)", text, re.IGNORECASE
    ):
        return fail("Postmaster Tools data is used, so a dated step must register and verify every sending domain there")

    # Waves
    ramp = sec["warmup and ramp schedule"]
    ramp_tables = tables(ramp)
    if len(ramp_tables) < 2:
        return fail("Warmup and Ramp Schedule needs a wave table and a ramp table")
    wh, wrows = ramp_tables[0]
    wi, ws, wf, wc = col(wh, "wave"), col(wh, "warmup start"), col(wh, "first cold"), col(wh, "cap")
    if min(wi, ws, wf, wc) < 0:
        return fail("wave table needs Wave, Warmup start, First cold send and Cold cap columns")
    waves, soft_used = {}, False
    active_starts, active_firsts, reserve_starts = [], [], []
    for r in wrows:
        if len(r) <= max(wi, ws, wf, wc):
            return fail("wave row has too few cells")
        name = r[wi].lower()
        cap = first_int(r[wc])
        if cap is None or cap > MAX_CAP:
            return fail(f"wave {r[wi]}: cold cap must be a number of {MAX_CAP} or less")
        reserve = "reserve" in name or "none" in r[wf].lower()
        if reserve:
            if cap != 0:
                return fail(f"wave {r[wi]} is a reserve wave and must have a cold cap of 0")
            if parse_date(r[ws]):
                reserve_starts.append(parse_date(r[ws]))
        else:
            warm, first = parse_date(r[ws]), parse_date(r[wf])
            if not warm or not first:
                return fail(f"wave {r[wi]} needs a warmup start and first cold send (YYYY-MM-DD)")
            days = (first - warm).days
            if days < MIN_WARMUP_DAYS:
                return fail(f"wave {r[wi]} sends cold {days} days after warmup start; minimum {MIN_WARMUP_DAYS}")
            if days < STANDARD_WARMUP_DAYS:
                soft_used = True
            active_starts.append(warm)
            active_firsts.append(first)
        waves[name] = reserve
    if not any(not v for v in waves.values()):
        return fail("wave table has no active wave")
    if reserve_starts and active_starts and min(reserve_starts) > min(active_starts):
        return fail("reserve warmup starts after the first active wave; start it the same day so a warmed reserve exists on the first cold send")
    if not re.search(r"soft start", text, re.IGNORECASE):
        return fail("state once (in the Summary) whether the soft start was chosen")
    if soft_used and not (re.search(r"health", ramp, re.IGNORECASE) and re.search(r"\bvalid\b", ramp, re.IGNORECASE)):
        return fail("a wave on the soft start needs its gates stated (health score and a valid-only send file)")
    if not re.search(r"placement test|seed test", ramp, re.IGNORECASE):
        return fail("the go-live gate needs an inbox placement (seed) test with its tool named")

    rh, rrows = ramp_tables[1]
    ci = col(rh, "cold cap")
    if ci < 0 or len(rrows) < 3:
        return fail("ramp table needs a 'Cold cap' column and at least 3 rows")
    caps = [first_int(r[ci]) for r in rrows if len(r) > ci and first_int(r[ci]) is not None]
    positive = [c for c in caps if c > 0]
    if not caps or caps[0] != 0:
        return fail("first ramp row must be warmup only (cold cap 0)")
    if not positive or positive[0] > MAX_START:
        return fail(f"ramp must start cold sends at {MAX_START} or fewer per mailbox")
    if max(caps) > MAX_CAP:
        return fail(f"ramp cap above {MAX_CAP}")

    # Roster
    header, rows = table(sec["mailbox roster"])
    if len(rows) < 2:
        return fail("Mailbox Roster needs at least 2 mailbox rows")
    mi, oi, ri, vi, pi = col(header, "mailbox"), col(header, "owner"), col(header, "role"), col(header, "wave"), col(header, "provider")
    if min(mi, oi, ri, vi, pi) < 0:
        return fail("Mailbox Roster needs Mailbox, Owner, Provider, Role and Wave columns")
    active = reserve = 0
    uses_ms = False
    for r in rows:
        if len(r) < len(header):
            return fail(f"roster row has too few cells: {' | '.join(r)[:80]}")
        box = r[mi]
        if "@" not in box:
            return fail(f"roster row without a mailbox address: {box}")
        owner = r[oi].lower()
        if not owner or owner in {"none", "n/a", "-", "unassigned"}:
            return fail(f"{box} has no owner; every mailbox needs a real person")
        wave = r[vi].lower()
        if wave not in waves:
            return fail(f"{box} is on wave '{r[vi]}', which is not in the wave table")
        if "reserve" in r[ri].lower():
            reserve += 1
            if not waves[wave]:
                return fail(f"{box} is a reserve mailbox on an active wave; reserves stay at cold cap 0")
        else:
            active += 1
            if waves[wave]:
                return fail(f"{box} is active but on a reserve wave")
        if re.search(r"microsoft|exchange|outlook", r[pi], re.IGNORECASE):
            uses_ms = True
    if active == 0:
        return fail("roster has no active mailboxes")

    acct = sec["account settings"]
    if len(table(acct)[1]) < 3 or "oauth" not in acct.lower():
        return fail("Account Settings needs at least 3 rows and the OAuth connection method")
    if uses_ms:
        if "outbound spam" not in acct.lower() or "quota" not in acct.lower():
            return fail("Microsoft mailboxes need the outbound spam policy and the tenant quota in Account Settings")
        qline = next((l for l in ramp.splitlines() if l.lower().startswith("tenant quota check")), "")
        if not re.search(r"\d", qline):
            return fail("Microsoft mailboxes need a 'Tenant quota check:' line with numbers in the ramp schedule")
    elif re.search(r"tenant quota", text, re.IGNORECASE):
        return fail("no Microsoft mailboxes, so leave out the tenant quota check")
    if "smtp.google.com" not in text and re.search(r"google workspace", text, re.IGNORECASE):
        return fail("Google Workspace mailboxes need the MX value smtp.google.com in the DNS records")

    sig = sec["signature block"]
    if IMAGE.search(sig):
        return fail("Signature Block must be plain text with no images")
    if not OPT_OUT.search(sig):
        return fail("Signature Block needs an opt-out line")
    if not re.search(r"\d{1,2}:\d{2}", sec["sending rules"]):
        return fail("Sending Rules needs an hour window like 08:00 to 17:00")
    _, ret = table(sec["rotation and retirement"])
    if len(ret) < 3 or "%" not in sec["rotation and retirement"]:
        return fail("Rotation and Retirement needs pause, rest and retire rows with numeric (%) triggers")
    cost = sec.get("list feed and cost")
    if cost is not None and ("$" not in cost or "0.00169" not in cost):
        return fail("List Feed and Cost needs validation priced at $0.00169 per email")
    if not re.search(r"only `?valid`? (rows|addresses)|`?valid`? (rows|addresses) only", text, re.IGNORECASE):
        return fail("state the list rule once: load only valid rows")

    print(
        f"PASS - {active} active and {reserve} reserve mailboxes, all owned, {len(waves)} wave(s) dated once, "
        f"caps <= {MAX_CAP}, {MIN_WARMUP_DAYS}+ day warmup, plain-text signature with opt-out"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
