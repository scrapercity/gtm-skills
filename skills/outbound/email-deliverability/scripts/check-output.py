#!/usr/bin/env python3
"""Check a finished deliverability health report.

Usage: check-output.py path/to/report.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import re
import sys
from pathlib import Path

REQUIRED = [
    "Summary",
    "Scope",
    "Authentication and Compliance",
    "List Validation",
    "Placement Tests",
    "Domain Health",
    "Blocklist Checks",
    "Incidents and Actions",
    "Stop Rules",
    "Next Review",
]
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 4000
BUCKETS = ["valid", "catch_all", "unknown", "invalid", "disposable"]
RED_BOUNCE, YELLOW_BOUNCE = 3.0, 2.0
RED_SPAM, YELLOW_SPAM = 0.3, 0.1
DOMAIN = re.compile(r"\b([a-z0-9-]+\.)+[a-z]{2,}\b", re.IGNORECASE)


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
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    sec = sections(text)
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")

    # Authentication: every row has pass or fail for SPF, DKIM, DMARC.
    ah, arows = table(sec["authentication and compliance"])
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
        not_green = bounce >= YELLOW_BOUNCE or (spam is not None and spam >= YELLOW_SPAM)
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
    if "spamhaus" not in block:
        return fail("Blocklist Checks must include Spamhaus")

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

    # Incidents: runbook and owner on every row.
    ih, irows = table(sec["incidents and actions"])
    ri, oi = col(ih, "runbook"), col(ih, "owner")
    if min(ri, oi) < 0:
        return fail("Incidents and Actions needs Runbook and Owner columns")
    for r in irows:
        if r[0].lower() in {"none", "no incidents"}:
            continue
        if not re.search(r"\bR[1-8]\b", r[ri]):
            return fail(f"incident without a runbook reference (R1 to R8): {r[ri][:40]}")
        if not r[oi] or r[oi].lower() in {"none", "-", "tbd"}:
            return fail("incident without an owner")
    if len(table(sec["stop rules"])[1]) < 5:
        return fail("Stop Rules needs at least 5 rules")
    if len(table(sec["placement tests"])[1]) < 1:
        return fail("Placement Tests needs at least 1 row")

    print(f"PASS - {len(health_domains)} domains ({counts['green']} green, {counts['yellow']} yellow, {counts['red']} red), statuses match thresholds, validation buckets add up")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
