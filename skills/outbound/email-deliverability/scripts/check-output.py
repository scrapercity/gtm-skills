#!/usr/bin/env python3
"""Check a finished deliverability deliverable.

Two kinds of deliverable are checked:
- Incident recovery plan (has "## Verdict" and "## Recovery Plan"): ranked
  diagnosis with a confirming check per cause, a dated day-by-day calendar whose
  totals equal inboxes x sends per inbox, stop-now list, re-validation priced at
  $0.0072, the open-rate caveat, and a length cap.
- Weekly health report (everything else): statuses match the sourced thresholds
  (Berman 2% bounces, Google 0.1% and 0.3% spam rate), validation buckets add up,
  linked domains on DBL, SURBL and URIBL, six-month audit dated.
Both fail on legal content (owner rule).

Usage: check-output.py path/to/deliverable.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import hashlib
import re
import sys
from pathlib import Path

REQUIRED = [
    "Summary",
    "Scope",
    "Authentication and Unsubscribe",
    "List Validation",
    "Placement Tests",
    "Domain Health",
    "Blocklist Checks",
    "Incidents and Actions",
    "Stop Rules",
    "Six-Month Audit",
    "Next Review",
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 4000
BUCKETS = ["valid", "catch_all", "unknown", "invalid", "disposable"]
RED_BOUNCE = 2.0  # Alex Berman: keep hard bounces under 2%
RED_SPAM, YELLOW_SPAM = 0.3, 0.1  # Google sender guidelines: under 0.10%, never 0.30%
RESTART_MAX = 20  # Alex Berman: new domains start at 10 to 20 a day
CAP_LIMIT = 50  # Alex Berman: under 50 a day per inbox
AUDIT_CHECKS = {
    "DNS records vs plan": re.compile(r"dns", re.IGNORECASE),
    "DKIM key rotation": re.compile(r"dkim", re.IGNORECASE),
    "DMARC rua review": re.compile(r"dmarc|rua", re.IGNORECASE),
    "placement test": re.compile(r"placement|seed", re.IGNORECASE),
    "caps vs volume": re.compile(r"\bcaps?\b|volume", re.IGNORECASE),
}
INCIDENT_TYPES = re.compile(
    r"bounce spike|spam folder|complaint spike|blocklisted domain|blocklisted ip|authentication rejection|"
    r"reputation deferral|rate limit|mailbox suspended|measurement problem",
    re.IGNORECASE,
)
INTERNAL = re.compile(
    r"\bR[1-9]\b|references/|scripts/|\b[\w-]+\.md\b|\b(domain-infrastructure|inbox-setup|email-deliverability|"
    r"sending-platforms|email-list-cleaner|cold-email-list|cold-email-copywriting|reply-handling|cold-email-strategy)\b|"
    r"\b(validate_emails|find_emails|check_wallet|check_run_status|download_results|scrape_[a-z_]+)\b"
)
INCIDENT_REQUIRED = [
    "Verdict",
    "Stop Now",
    "Diagnosis",
    "Measurement",
    "List Re-validation",
    "Recovery Plan",
    "Resume and Retire Rules",
    "Next Check-in",
]
INCIDENT_MIN, INCIDENT_MAX = 3000, 12000
PADDING_HEADINGS = ("six-month audit", "quarterly audit", "quality check", "frameworks applied", "framework basis")
EMPTY_CELL = re.compile(r"^\s*(not run|not checked|not applicable|n/?a)\b", re.IGNORECASE)
ISO_DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
# A bare "(Google)" hides which document the number came from; name the document.
BARE_SOURCE = re.compile(r"\((Google|Yahoo|Microsoft|Instantly|Berman|Spamhaus)\)")
# Spamhaus defines snowshoeing as many domains and IPs that change frequently; a plan
# should not stretch that term onto a sender buying a few replacement domains.
STRETCHED = re.compile(r"snowsho", re.IGNORECASE)
AUTH_CAUSE = re.compile(r"authenticat|\bspf\b|\bdkim\b|\bdmarc\b|\bdns\b", re.IGNORECASE)
DOMAIN = re.compile(r"\b([a-z0-9-]+\.)+[a-z]{2,}\b", re.IGNORECASE)


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


def pct(cell):
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", cell)
    return float(m.group(1)) if m else None


def num(cell):
    m = re.fullmatch(r"\s*(\d{1,3}(?:,\d{3})*|\d+)\s*", cell)
    return int(m.group(1).replace(",", "")) if m else None


def domain_of(cell):
    m = DOMAIN.search(cell)
    return m.group(0).lower() if m else ""


def fail(msg):
    print(f"FAIL - {msg}")
    return 1


def first_int(cell):
    m = re.search(r"\d{1,3}(?:,\d{3})+|\d+", cell)
    return int(m.group(0).replace(",", "")) if m else None


def common_checks(text, sec):
    for name, block in sec.items():
        for line in block.splitlines():
            if line.strip().startswith("|"):
                for cell in line.strip().strip("|").split("|"):
                    if EMPTY_CELL.match(cell):
                        return f"'{cell.strip()[:30]}' table cell in {name}; list what was not checked in one line instead"
    hit = INTERNAL.search(text)
    if hit:
        return f"deliverable cites an internal reference or tool id the reader cannot use: {hit.group(0)}"
    if re.search(r"^\s*[-*] \[[xX ]\]", text, re.MULTILINE):
        return "self-grading checklist in the deliverable; the reader gets the plan, not the review"
    hit = BARE_SOURCE.search(text)
    if hit:
        return f"bare source {hit.group(0)}; name the document once (\"Google's sender guidelines\", \"Instantly help\")"
    if STRETCHED.search(text):
        return "'snowshoeing' stretches Spamhaus's term; say new domains would get the same list and copy and burn the same way"
    seen = {}
    prose = "\n".join(l for l in text.splitlines() if not l.strip().startswith("|"))
    for sent in re.split(r"(?<=[.!?])\s+|\n", prose):
        key = re.sub(r"\s+", " ", sent.strip().lower())
        if len(key) >= 60:
            if key in seen:
                return f"sentence repeated; state each fact once: '{sent.strip()[:60]}'"
            seen[key] = True
    return None


def check_incident(text, sec):
    if not INCIDENT_MIN <= len(text) <= INCIDENT_MAX:
        return fail(f"incident plan is {len(text)} chars; keep it between {INCIDENT_MIN} and {INCIDENT_MAX}")
    for name in INCIDENT_REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")
    for pad in PADDING_HEADINGS:
        if pad in sec:
            return fail(f"'## {pad.title()}' does not belong in an incident plan")
    err = common_checks(text, sec)
    if err:
        return fail(err)

    m = re.search(r"(\d+)\s+(?:[A-Za-z0-9-]+\s+){0,3}inboxes", text)
    if not m:
        return fail("state the inbox count in the setup line (for example '12 Google Workspace inboxes')")
    inboxes = int(m.group(1))

    verdict = sec["verdict"]
    if not ISO_DATE.search(verdict) or not re.search(r"restart|resume", verdict, re.IGNORECASE):
        return fail("Verdict needs the earliest restart date (YYYY-MM-DD)")

    stop = sec["stop now"]
    bullets = [l for l in stop.splitlines() if re.match(r"^\s*[-*] ", l)]
    if len(bullets) < 4:
        return fail("Stop Now needs at least 4 bullet actions")
    for word, why in (("warmup", "say what happens to warmup"), ("opt-out", "keep the opt-out line and same-day suppression")):
        if word not in stop.lower():
            return fail(f"Stop Now must {why}")

    dh, drows = table(sec["diagnosis"])
    rk, cf, cl = col(dh, "rank"), col(dh, "confirm"), col(dh, "clear")
    if min(rk, cf, cl) < 0:
        return fail("Diagnosis table needs Rank, Confirm with and Clears it columns")
    if len(drows) < 3:
        return fail("Diagnosis needs at least 3 ranked causes")
    for i, r in enumerate(drows, 1):
        if first_int(r[rk]) != i:
            return fail(f"Diagnosis ranks must run 1, 2, 3 in order; row {i} says '{r[rk]}'")
        if len(r[cf]) < 15 or len(r[cl]) < 10:
            return fail(f"Diagnosis rank {i} needs a specific confirming check and a result that clears it")

    diag = sec["diagnosis"]
    steps = re.findall(r"^\s*\d+\.\s+\S", diag, re.MULTILINE)
    if len(steps) < 3 or "dig " not in diag:
        return fail("Diagnosis needs the checks once, as at least 3 numbered commands including the dig lines")
    if AUTH_CAUSE.search(" ".join(" ".join(r) for r in drows)):
        for need, what in (("v=spf1", "the SPF record"), ("v=dmarc1", "the DMARC record"), ("authenticate email", "the Admin console DKIM path")):
            if need not in text.lower():
                return fail(f"authentication is a ranked cause, so write its fix out: {what} ready to paste")
    if not re.search(r"glockapps|seed (account|mailbox)|test account|seed you own", text, re.IGNORECASE):
        return fail("name how the seed test runs: a tool (for example GlockApps) or seed accounts you own at each provider")
    if re.search(r"auto-?pause", text, re.IGNORECASE) and not re.search(r"preferences|settings", text, re.IGNORECASE):
        return fail("the bounce auto-pause change needs its menu path")
    if "instantly" in text.lower() and not re.search(r"(another|other|any other) sequencer", text, re.IGNORECASE):
        return fail("an assumed sequencer needs one line on the same settings in any other sequencer")
    if len(re.findall(r"last 200 sends", text, re.IGNORECASE)) > 2:
        return fail("the bounce gate is restated; define it once as the standard gate and refer to it")
    if re.search(r"would change", sec["next check-in"], re.IGNORECASE):
        return fail("Next Check-in repeats what would change the ranking; the Diagnosis 'Clears it' column already says it")

    meas = sec["measurement"].lower()
    for pat, what in ((r"apple", "Apple Mail Privacy Protection"), (r"repl", "reply rate"), (r"seed|placement", "seed placement")):
        if not re.search(pat, meas):
            return fail(f"Measurement must cover {what}")

    rv = sec["list re-validation"]
    if "0.0072" not in rv or "$" not in rv:
        return fail("List Re-validation needs the cost at $0.0072 per email")
    for qty, total in re.findall(r"(\d[\d,]*)\s*x\s*\$0\.0072\s*=\s*\$(\d[\d,]*\.\d{2})", rv):
        want = round(int(qty.replace(",", "")) * 0.0072, 2)
        if abs(want - float(total.replace(",", ""))) > 0.01:
            return fail(f"re-validation cost {qty} x $0.0072 should be ${want:.2f}, not ${total}")

    ph, prows = table(sec["recovery plan"])
    dc, pi, tc, gc = col(ph, "date"), col(ph, "per inbox"), col(ph, "total"), col(ph, "gate")
    if min(dc, pi, tc, gc) < 0:
        return fail("Recovery Plan table needs Date, Sends per inbox, Total sends a day and Gate columns")
    if len(prows) < 5:
        return fail("Recovery Plan needs at least 5 dated rows")
    last_date, prev = "", 0
    first_send = None
    for r in prows:
        dm = ISO_DATE.search(r[dc])
        if not dm:
            return fail(f"Recovery Plan row without a YYYY-MM-DD date: {r[dc][:30]}")
        if dm.group(0) < last_date:
            return fail("Recovery Plan dates must run forward")
        last_date = dm.group(0)
        per, tot = first_int(r[pi]), first_int(r[tc])
        if per is None or tot is None:
            return fail(f"Recovery Plan row {last_date} needs numeric sends per inbox and total")
        if per * inboxes != tot:
            return fail(f"Recovery Plan {last_date}: {per} x {inboxes} inboxes = {per * inboxes}, table says {tot}")
        if per >= CAP_LIMIT:
            return fail(f"Recovery Plan {last_date}: {per} a day per inbox; keep it under {CAP_LIMIT} (Berman)")
        if per and first_send is None:
            first_send = per
            if per > RESTART_MAX:
                return fail(f"restart at {per} a day per inbox; restart at 10 to {RESTART_MAX} (Berman's new-domain start)")
        if per and prev and per > 2 * prev:
            return fail(f"Recovery Plan {last_date}: {prev} to {per} more than doubles in one step (Google warns against doubling volume at once)")
        if per:
            prev = per
        if per and not re.search(r"\d|standard gate", r[gc], re.IGNORECASE):
            return fail(f"Recovery Plan {last_date}: the gate needs a number or the standard gate")
    if first_send is None:
        return fail("Recovery Plan never restarts sending")
    if re.search(r"standard gate", sec["recovery plan"], re.IGNORECASE):
        m = re.search(r"standard gate:[^\n]*", text, re.IGNORECASE)
        if not m or not re.search(r"\d%", m.group(0)):
            return fail("rows cite the standard gate; define it once with its numbers ('Standard gate: ...')")

    rh, rrows = table(sec["resume and retire rules"])
    if len(rrows) < 3 or "retire" not in sec["resume and retire rules"].lower():
        return fail("Resume and Retire Rules needs at least 3 rules including when to retire a domain")
    if not ISO_DATE.search(sec["next check-in"]):
        return fail("Next Check-in needs a date (YYYY-MM-DD)")

    print(f"PASS - incident plan: {len(drows)} ranked causes with confirming checks, {len(prows)} dated calendar rows "
          f"for {inboxes} inboxes (restart at {first_send} a day, totals match), stop list, re-validation priced, "
          f"open-rate caveat, {len(text)} chars")
    return 0


def main(argv):
    if len(argv) != 2:
        print("usage: check-output.py path/to/report.md")
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"usage: file not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")

    hit = PLACEHOLDER.search(text)
    if hit:
        return fail(f"placeholder left in: {hit.group(0)}")
    term = legal_term(text)
    if term:
        return fail("deliverable carries legal content; remove it (owner rule)")
    sec = sections(text)
    if "verdict" in sec and "recovery plan" in sec:
        return check_incident(text, sec)
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")

    # Authentication: every row has pass or fail for SPF, DKIM, DMARC.
    ah, arows = table(sec["authentication and unsubscribe"])
    auth = {}
    for key in ("spf", "dkim", "dmarc"):
        if col(ah, key) < 0:
            return fail(f"Authentication table needs a {key.upper()} column")
    for r in arows:
        d = domain_of(r[0])
        if not d:
            return fail(f"authentication row without a domain: {r[0]}")
        results = []
        for key in ("spf", "dkim", "dmarc"):
            cell = r[col(ah, key)].lower()
            if "fail" in cell:
                results.append("fail")
            elif "pass" in cell:
                results.append("pass")
            else:
                return fail(f"{d} {key.upper()} must read pass or fail, got '{cell[:30]}'")
        auth[d] = "fail" not in results

    # Domain health: status consistent with thresholds.
    hh, hrows = table(sec["domain health"])
    bi, si, st = col(hh, "bounce"), col(hh, "spam"), col(hh, "status")
    if min(bi, si, st) < 0:
        return fail("Domain Health needs bounce, spam rate and status columns")
    if not hrows:
        return fail("Domain Health has no rows")
    counts = {"green": 0, "yellow": 0, "red": 0}
    health_domains = set()
    for r in hrows:
        d = domain_of(r[0])
        if not d:
            return fail(f"domain health row without a domain: {r[0]}")
        health_domains.add(d)
        status = r[st].strip().lower().split()[0] if r[st].strip() else ""
        if status not in counts:
            return fail(f"{d} status must be Green, Yellow or Red")
        counts[status] += 1
        bounce = pct(r[bi])
        if bounce is None:
            return fail(f"{d} needs a hard bounce percentage")
        spam = pct(r[si])
        must_red = bounce >= RED_BOUNCE or (spam is not None and spam >= RED_SPAM) or not auth.get(d, True)
        not_green = spam is not None and spam >= YELLOW_SPAM
        if must_red and status != "red":
            return fail(f"{d} must be Red (bounce {bounce}%, spam {spam}, auth ok {auth.get(d, True)})")
        if not_green and status == "green":
            return fail(f"{d} cannot be Green at bounce {bounce}% and spam {spam}%")
    missing_auth = health_domains - set(auth)
    if missing_auth:
        return fail(f"no authentication row for: {', '.join(sorted(missing_auth))}")
    block = sec["blocklist checks"].lower()
    for d in health_domains:
        if d not in block:
            return fail(f"no blocklist check for {d}")
    bh, brows = table(sec["blocklist checks"])
    for lst in ("spamhaus", "surbl", "uribl"):
        if col(bh, lst) < 0:
            return fail(f"Blocklist Checks needs a {lst.upper()} column")
    linked = [r for r in brows if r and domain_of(r[0]) and domain_of(r[0]) not in health_domains]
    if not linked:
        return fail("Blocklist Checks must include the linked domains (tracking host, main site, booking link), not only sending domains")

    # List validation: every bucket present, columns add up, priced at $0.0072.
    vh, vrows = table(sec["list validation"])
    found = {}
    total_row = None
    for r in vrows:
        label = r[0].lower().replace(" ", "_")
        if label.startswith("total"):
            total_row = r
            continue
        for b in BUCKETS:
            if b in label and not (b == "valid" and "catch" in label) and not (b == "valid" and "invalid" in label):
                found[b] = r
    for b in BUCKETS:
        if b not in found:
            return fail(f"List Validation is missing the '{b}' bucket")
    if total_row is None:
        return fail("List Validation needs a Total row")
    for ci in range(1, len(vh)):
        if ci >= len(total_row):
            continue
        tot = num(total_row[ci])
        if tot is None:
            continue
        vals = [num(found[b][ci]) if ci < len(found[b]) else None for b in BUCKETS]
        if any(v is None for v in vals):
            return fail(f"List Validation column '{vh[ci]}' has a non-numeric bucket count")
        if sum(vals) != tot:
            return fail(f"List Validation column '{vh[ci]}' buckets sum to {sum(vals)}, Total says {tot}")
    if "0.0072" not in sec["list validation"] or "$" not in sec["list validation"]:
        return fail("List Validation needs the cost at $0.0072 per email")

    # Incidents: a named incident type and an owner on every row.
    ih, irows = table(sec["incidents and actions"])
    ri, oi = col(ih, "type"), col(ih, "owner")
    if min(ri, oi) < 0:
        return fail("Incidents and Actions needs Type and Owner columns")
    for r in irows:
        if r[0].lower() in {"none", "no incidents"}:
            continue
        if not INCIDENT_TYPES.search(r[ri]):
            return fail(f"incident type must name the problem (Bounce spike, Complaint spike, ...): {r[ri][:40]}")
        if not r[oi] or r[oi].lower() in {"none", "-", "tbd"}:
            return fail("incident without an owner")

    # Scope: one owner with pause authority and a backup capacity plan.
    scope_rows = table(sec["scope"])[1]
    pause = [r for r in scope_rows if r and "pause" in r[0].lower()]
    if not pause or len(pause[0]) < 2 or not re.search(r"[A-Z][a-z]+ [A-Z][a-z]+", pause[0][1]):
        return fail("Scope needs a 'Pause authority' row naming one person")
    backup = [r for r in scope_rows if r and "backup capacity" in r[0].lower()]
    if not backup or len(backup[0]) < 2 or not re.search(r"\d", backup[0][1]):
        return fail("Scope needs a 'Backup capacity' row with the reserve sends a day")

    # Authentication failures need the records to publish.
    if not all(auth.values()) and not re.search(r"v=spf1|v=dkim1|v=dmarc1", sec["authentication and unsubscribe"], re.IGNORECASE):
        return fail("a failing authentication check needs the exact records to publish")

    # Economy and audience.
    err = common_checks(text, sec)
    if err:
        return fail(err)
    srows = table(sec["stop rules"])[1]
    if len(srows) < 5:
        return fail("Stop Rules needs at least 5 rules")
    sh = table(sec["stop rules"])[0]
    if col(sh, "source") < 0:
        return fail("Stop Rules needs a Source column naming where each threshold comes from")

    qh, qrows = table(sec["six-month audit"])
    for name, rx in AUDIT_CHECKS.items():
        match = [r for r in qrows if r and rx.search(r[0])]
        if not match:
            return fail(f"Six-Month Audit is missing the '{name}' check")
        row = match[0]
        if not ISO_DATE.search(" ".join(row[1:])):
            return fail(f"Six-Month Audit '{name}' row needs a run date and next due date (YYYY-MM-DD)")
        if name == "placement test":
            joined = " ".join(row).lower()
            for prov, pat in (("Google", r"google|gmail"), ("Microsoft", r"microsoft|outlook"), ("Yahoo", r"yahoo")):
                if not re.search(pat, joined):
                    return fail(f"Six-Month Audit placement row must cover {prov}")
    if len(table(sec["placement tests"])[1]) < 1:
        return fail("Placement Tests needs at least 1 row")

    print(f"PASS - {len(health_domains)} domains ({counts['green']} green, {counts['yellow']} yellow, {counts['red']} red), statuses match thresholds, validation buckets add up, stop rules sourced, linked domains on DBL, SURBL and URIBL, pause owner and backup capacity named, six-month audit complete")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
