#!/usr/bin/env python3
"""Check a finished sending infrastructure plan.

Usage: check-output.py path/to/plan.md
Prints PASS - ... and exits 0, or FAIL - reason and exits 1. Exit 2 on usage error.
"""

import hashlib
import re
import sys
from datetime import date
from pathlib import Path

REQUIRED = [
    "Summary",
    "Inputs",
    "Capacity Plan",
    "Mailbox Provider Decision",
    "Sending Domains and Mailboxes",
    "Tenant Settings",
    "DNS Record Template",
    "Launch Timeline",
    "Monitoring",
    "Cost Estimate",
    "Launch Risks and Scaling Triggers",
    "Launch Checklist",
    "Sources",
]
# Calendar dates belong only in these sections (and the top line); elsewhere they repeat the timeline.
DATED_SECTIONS = {"sending domains and mailboxes", "tenant settings", "launch timeline", "launch checklist", "sources"}
SUMMARY_MAX_WORDS = 160
OFF_SPEC = re.compile(
    r"reachable market|days of list|list runway|(cost|\$[\d.,]+) per 1,000|contact limit|archiv|tenant ownership|"
    r"security team|questionnaire|lead data|lead database|growth plan",
    re.IGNORECASE,
)
NO_PATH = re.compile(r"\bno (path|way|option|build)\b[^.\n]{0,100}\b(reach|reaches|hit|hits|meet|meets)\b", re.IGNORECASE)
DISCLAIMER = re.compile(r"\bnot (yet )?(run|measured)\b|#\s*assumed|assumed (response|output)", re.IGNORECASE)
LOCAL_PART = re.compile(r"^[a-z]+(\.[a-z]+)?$")
ROLE_WORDS = {"info", "sales", "contact", "hello", "team", "support", "admin", "marketing", "outreach", "mail", "office", "noreply"}
MAX_TEMPLATE_ROWS_PER_PROVIDER = 12
INTERNAL_REF = re.compile(
    r"references/|\.md\b|SKILL\.md|scripts/check-output|\bsection \d|\b(inbox-setup|email-deliverability|sending-platforms|"
    r"cold-email-strategy|outbound-unit-economics|cold-email-list|domain-infrastructure)\b|\bskills?\b|\bphase \d|frameworks applied",
    re.IGNORECASE,
)
TOOL_ID = re.compile(
    r"\b(check_wallet|query_lead_database|query_local_business_database|validate_emails|find_emails|check_run_status|"
    r"download_results|scrape_[a-z_]+|sc_mx_[a-z_]+|pagination\.total|run_?id)\b",
    re.IGNORECASE,
)
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)[^\]]*\]|<[a-z][a-z _-]*>", re.IGNORECASE)
MIN_CHARS = 3500
MAX_CAP = 50  # Alex Berman: under 50 a day per inbox; Smartlead: max 50 per address
MAX_PER_DOMAIN = 3  # Alex Berman, Instantly and Smartlead: 2 to 3 inboxes per domain
STANDARD_WARMUP = 21  # Instantly: 3 weeks of warmup for its own AirMail accounts
MIN_WARMUP = 14  # Instantly: at least 2 weeks of warmup before campaigns
DATE = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
HOST = re.compile(r"\b[a-z0-9-]+(\.[a-z0-9-]+)+\b", re.IGNORECASE)
ADDR = re.compile(r"[a-z0-9._+-]+@([a-z0-9.-]+\.[a-z]{2,})", re.IGNORECASE)


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


def table_rows(block):
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def header_of(block):
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("|"):
            return [c.strip().lower() for c in s.strip("|").split("|")]
    return []


def col(header, name):
    for i, h in enumerate(header):
        if name in h:
            return i
    return -1


def to_date(s):
    m = DATE.search(s)
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def first_word(s):
    words = re.findall(r"[a-z]+", s.lower())
    return words[0] if words else ""


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
    if legal_word(text):
        return fail("deliverable carries legal content; remove it (owner rule)")
    if len(text) < MIN_CHARS:
        return fail(f"too short ({len(text)} chars, need {MIN_CHARS})")
    sec = sections(text)
    for name in REQUIRED:
        if name.lower() not in sec:
            return fail(f"missing section '## {name}'")
    allowed = {n.lower() for n in REQUIRED}
    for name in sec:
        if name not in allowed:
            return fail(f"extra section '## {name}'; the plan has only the template's sections")
    for name, body in sec.items():
        if name not in DATED_SECTIONS and DATE.search(body):
            return fail(f"calendar date in '{name}'; dates live only in the timeline, checklist, tenant settings and the All domains line")
    words = len(re.findall(r"\S+", sec["summary"]))
    if words > SUMMARY_MAX_WORDS:
        return fail(f"Summary is {words} words; answer in {SUMMARY_MAX_WORDS} or fewer")
    for name in ("summary", "inputs", "capacity plan", "cost estimate", "launch risks and scaling triggers"):
        hit = OFF_SPEC.search(sec[name])
        if hit:
            return fail(f"off-spec content in '{name}': {hit.group(0)}; the plan covers infrastructure and the sequencer only")
    hit = NO_PATH.search(text)
    if hit:
        return fail(f"'{hit.group(0)}': price the wide build instead of saying the date cannot be met")
    if len(DISCLAIMER.findall(text)) > 1:
        return fail("repeated not-run or assumed-output disclaimers; one line at the top is enough")
    urls = re.findall(r"https://[^\s)>\]]+", sec["sources"])
    if len(urls) < 5:
        return fail("Sources needs a URL for every vendor price, limit and rule the plan uses (at least 5)")

    hit = TOOL_ID.search(text)
    if hit:
        return fail(f"agent tool id in the deliverable: {hit.group(0)}; say what was checked in plain words")
    hit = INTERNAL_REF.search(text)
    if hit:
        return fail(f"deliverable cites an internal file or skill: {hit.group(0)}")

    # Inputs
    main_domain = ""
    has_volume = False
    for row in table_rows(sec["inputs"]):
        label = row[0].lower() if row else ""
        if label.startswith("main domain") and len(row) > 1:
            m = re.search(r"([a-z0-9-]+\.[a-z.]+)", row[1].lower())
            main_domain = m.group(1) if m else ""
        if "volume" in label:
            has_volume = True
    if not main_domain:
        return fail("Inputs table needs a 'Main domain' row with a domain")
    if not has_volume:
        return fail("Inputs table needs the volume as requested and the reading used")

    # Capacity
    cap_rows = table_rows(sec["capacity plan"])
    if len(cap_rows) < 6:
        return fail("Capacity Plan table needs at least 6 rows")
    cap = [r for r in cap_rows if r and "cap per mailbox" in r[0].lower()]
    if not cap:
        return fail("Capacity Plan needs a 'Cap per mailbox' row")
    nums = re.findall(r"\d+", cap[0][-1])
    if not nums or int(nums[0]) > MAX_CAP:
        return fail(f"cap per mailbox must be {MAX_CAP} or less")
    mpd = [r for r in cap_rows if r and "mailboxes per domain" in r[0].lower()]
    if not mpd or not (re.search(r"\b2 per domain\b", " ".join(mpd[0])) and re.search(r"\b3 per domain\b", " ".join(mpd[0]))):
        return fail("Capacity Plan needs a 'Mailboxes per domain' row comparing '2 per domain' and '3 per domain'")

    # Provider decision
    mix = sec["mailbox provider decision"]
    for prov in ("google", "microsoft"):
        if not re.search(prov + r"[^|\n]{0,40}?\d+(\.\d+)?\s*%", mix, re.IGNORECASE):
            return fail(f"Mailbox Provider Decision needs the recipient mix with a {prov.title()} share in %")
    opts = table_rows(mix)
    if len(opts) < 3 or sum(1 for r in opts if "$" in " ".join(r)) < 3:
        return fail("Mailbox Provider Decision needs an option table with a dollar cost on at least 3 options")
    if not any("resold" in " ".join(r).lower() or "reseller" in " ".join(r).lower() for r in opts):
        return fail("option table needs a resold-inbox option with its cost")
    bp = re.search(r"^build path:(.+)$", mix, re.IGNORECASE | re.MULTILINE)
    if not bp or "tenant" not in bp.group(1).lower() or "dkim" not in bp.group(1).lower():
        return fail("Mailbox Provider Decision needs a 'Build path:' line stating the tenant and DKIM-key trade-off")

    # Inventory
    inv = sec["sending domains and mailboxes"]
    ih = header_of(inv)
    di, ri, pi_, mi = col(ih, "domain"), col(ih, "role"), col(ih, "provider"), col(ih, "mailbox")
    if min(di, ri, pi_, mi) < 0:
        return fail("Sending Domains and Mailboxes needs Domain, Role, Provider and Mailboxes columns")
    pm = re.search(r"prepared\D{0,20}(20\d{2}-\d{2}-\d{2})", text, re.IGNORECASE)
    plan_date = to_date(pm.group(1)) if pm else None
    all_line = next((l for l in inv.splitlines() if l.lower().startswith("all domains:")), "")
    if not all_line:
        return fail("Sending Domains and Mailboxes needs one 'All domains:' line with the shared registrar facts")
    if not re.search(r"nameserver", all_line, re.IGNORECASE) or not HOST.search(all_line.split(":", 1)[1]):
        return fail("'All domains:' line needs the nameserver hostnames")
    if not re.search(r"dnssec\W{0,3}(on|off)\b", all_line, re.IGNORECASE):
        return fail("'All domains:' line needs DNSSEC On or Off")
    rd = re.search(r"renew\D{0,40}(20\d{2}-\d{2}-\d{2})", all_line, re.IGNORECASE)
    if not rd:
        return fail("'All domains:' line needs a renewal date as YYYY-MM-DD")
    if plan_date and to_date(rd.group(1)) <= plan_date:
        return fail("renewal date must be after the plan date")
    sending, provider_of, roles, all_locals = [], {}, set(), []
    for row in table_rows(inv):
        if len(row) <= max(di, ri, pi_, mi):
            return fail(f"inventory row is missing cells: {' | '.join(row)[:60]}")
        d = row[di].lower().strip("` ")
        if d == main_domain:
            return fail(f"main domain {main_domain} listed as a sending domain")
        label = d.split(".")[0]
        if "-" in label or re.search(r"\d", label):  # Instantly and Smartlead: no hyphens or numbers
            return fail(f"{d}: no hyphens or digits in sending domain names")
        addrs = ADDR.findall(row[mi])
        if not addrs:
            return fail(f"{d} lists no mailbox addresses")
        if any(a.lower() != d for a in addrs):
            return fail(f"{d} lists an address on another domain")
        locals_ = [m.group(1).lower() for m in re.finditer(r"([a-z0-9._+-]+)@", row[mi], re.IGNORECASE)]
        for lp in locals_:
            if not LOCAL_PART.match(lp) or lp.split(".")[0] in ROLE_WORDS:
                return fail(f"{lp}@{d}: addresses are first@ or first.last@ of a real person, no digits or role words")
        firsts = [lp.split(".")[0] for lp in locals_]
        if len(set(firsts)) < len(firsts):
            return fail(f"{d}: two mailboxes for the same first name; put two different people on each domain")
        all_locals.extend(locals_)
        role = row[ri].lower()
        if len(addrs) > MAX_PER_DOMAIN and "test" not in role:
            return fail(f"{d} has {len(addrs)} mailboxes; more than {MAX_PER_DOMAIN} per domain only as a labeled test pod")
        sending.append(d)
        provider_of[d] = row[pi_].lower()
        roles.add(role)
    if len(sending) < 2:
        return fail("Sending Domains and Mailboxes needs at least 2 domains")
    known_first = {lp.split(".")[0] for lp in all_locals if "." in lp}
    for lp in all_locals:
        if "." not in lp and lp not in known_first:
            return fail(f"{lp}@ is not the first name of any first.last@ sender; truncated or initial forms read as generated")
    if not any("reserve" in r for r in roles):
        return fail("Sending Domains and Mailboxes needs at least one Reserve domain")
    uses_ms = any("microsoft" in p or "exchange" in p for p in provider_of.values())

    # Domain list written once
    inv_lines = set(inv.splitlines())
    for line in text.splitlines():
        if line in inv_lines:
            continue
        named = {d for d in sending if re.search(r"(?<![a-z0-9.@-])" + re.escape(d) + r"(?![a-z0-9-])", line.lower())}
        if len(named) > 3:
            return fail("the domain list is written out again outside Sending Domains and Mailboxes; refer to it by provider and count")

    # Tenant settings
    ts = sec["tenant settings"]
    if len(table_rows(ts)) < 3:
        return fail("Tenant Settings needs at least 3 setting rows")
    if uses_ms:
        low = ts.lower()
        if "outbound spam" not in low or not re.search(r"quota|external recipient", low) or "trial" not in low:
            return fail("Microsoft tenants need the outbound spam policy, the age-based external recipient quota and a no-trial row in Tenant Settings")

    # DNS record template
    tpl = sec["dns record template"]
    th = header_of(tpl)
    trows = [r for r in table_rows(tpl) if len(r) >= 5]
    pi, ki, hi, vi = col(th, "provider"), col(th, "record"), col(th, "host"), col(th, "value")
    if min(pi, ki, hi, vi) < 0:
        return fail("DNS Record Template needs Provider, Record, Host and Value columns")
    trows = [r for r in trows if r[pi].strip().lower() != "provider"]
    by_provider = {}
    for r in trows:
        by_provider.setdefault(r[pi].lower(), []).append(r)
    if not by_provider:
        return fail("DNS Record Template has no rows")
    for prov, recs in by_provider.items():
        if len(recs) > MAX_TEMPLATE_ROWS_PER_PROVIDER:
            return fail(f"{prov}: {len(recs)} template rows; show one template per provider, not one row set per domain")
        kinds = [r[ki].upper() for r in recs]
        for need in ("MX", "SPF", "DKIM", "DMARC"):
            if need not in kinds:
                return fail(f"{prov} template has no {need} row")
        if kinds.count("SPF") != 1:
            return fail(f"{prov} template must have exactly one SPF row")
        if not any("POSTMASTER" in k for k in kinds):
            return fail(f"{prov} template needs a Postmaster Tools verification row")
        seen = set()
        for r in recs:
            kind, value, host = r[ki].upper(), r[vi].lower(), r[hi].lower()
            if kind == "DMARC" and "rua=mailto:" not in value:
                return fail(f"{prov} DMARC value has no rua=mailto:")
            if kind == "SPF" and not value.startswith("v=spf1"):
                return fail(f"{prov} SPF value must start with v=spf1")
            if "itrackly" in value and host.strip("` ") != "inst":
                return fail("Instantly tracking CNAME host must be exactly 'inst'")
            if kind == "TRACKING" and "instantly" in text.lower() and "itrackly" not in value and "sleadtrack" not in value:
                return fail("tracking row must use the sequencer's documented target (Instantly: inst to prox.itrackly.com)")
            key = (kind.lower(), host)
            if key in seen:
                return fail(f"{prov}: '{r[ki]}' at host '{r[hi]}' appears twice; one template row per record")
            seen.add(key)
        named = {d for d in sending for r in recs if d in " ".join(r).lower()}
        if len(named) > 1:
            return fail(f"{prov} template rows name {len(named)} sending domains; fill it in for one domain")
    filled = [m.group(1).lower() for m in re.finditer(r"filled in for\W{0,3}([a-z0-9.-]+\.[a-z]{2,})", tpl, re.IGNORECASE)]
    if len(filled) < len(by_provider):
        return fail("each provider block must say which sending domain it is 'filled in for'")
    for f in filled:
        if f not in sending:
            return fail(f"template is filled in for {f}, which is not a sending domain")
    stray = {d for d in sending for r in trows if d in " ".join(r).lower()} - set(filled)
    if stray:
        return fail(f"template rows name {', '.join(sorted(stray))}; per-domain rows repeat the template")
    for line in tpl.splitlines():
        m = re.search(r"filled in for\W{0,3}([a-z0-9.-]+\.[a-z]{2,})", line, re.IGNORECASE)
        if not m:
            continue
        if not re.search(r"applies to", line, re.IGNORECASE):
            return fail("each 'filled in for' line needs 'Applies to' with the other domains by provider and count")
        word = first_word(provider_of[m.group(1).lower()])
        same = [d for d in sending if first_word(provider_of[d]) == word]
        counts = [int(n) for n in re.findall(r"\b(\d+)\b", line.split("pplies to", 1)[1])]
        listed = [d for d in same if d in line.lower()]
        if len(listed) < len(same) and len(same) - 1 not in counts and len(same) not in counts:
            return fail(f"'Applies to' for {m.group(1)} must cover the {len(same)} {word} domains by count or by name")
    if re.search(r"\bapi\b", tpl, re.IGNORECASE):
        code = "\n".join(re.findall(r"```[a-z]*\n(.*?)```", tpl, re.DOTALL))
        if "curl" not in code or not re.search(r"\b(while|for)\b", code):
            return fail("records go in by API: write the script (a loop over the domain file with the curl call) in DNS Record Template")
    if re.search(r"[a-z0-9-]+\.[a-z]{2,}\._report\._dmarc", text, re.IGNORECASE):
        return fail("use one wildcard *._report._dmarc record on the report domain, not one per sending domain")
    if f"@{main_domain}" in tpl.lower() and "*._report._dmarc" not in text:
        return fail(f"rua points at {main_domain}: add the wildcard *._report._dmarc.{main_domain} record")

    # Launch timeline
    lt = sec["launch timeline"]
    if not re.search(r"^requested:", lt, re.IGNORECASE | re.MULTILINE):
        return fail("Launch Timeline needs a 'Requested:' line")
    lh = header_of(lt)
    wi, fi, vi2 = col(lh, "warmup start"), col(lh, "first cold"), col(lh, "full volume")
    if min(wi, fi, vi2) < 0:
        return fail("Launch Timeline needs Warmup start, First cold send and Full volume columns")
    paths = {}
    for r in table_rows(lt):
        name = r[0].lower()
        key = "standard" if "standard" in name else "soft" if "soft" in name else None
        if key and len(r) > max(wi, fi, vi2):
            paths[key] = (to_date(r[wi]), to_date(r[fi]), to_date(r[vi2]))
    if set(paths) != {"standard", "soft"} or any(None in v for v in paths.values()):
        return fail("Launch Timeline needs dated Standard and Soft start rows")
    if (paths["standard"][1] - paths["standard"][0]).days < STANDARD_WARMUP:
        return fail(f"standard path must warm at least {STANDARD_WARMUP} days")
    if (paths["soft"][1] - paths["soft"][0]).days < MIN_WARMUP:
        return fail(f"soft start must warm at least {MIN_WARMUP} days")
    req_line = next(l for l in lt.splitlines() if l.lower().startswith("requested:"))
    req = to_date(req_line)
    if req and req < paths["standard"][2] and not re.search(r"\bdays? (late|after|later)\b|\bslip", lt, re.IGNORECASE):
        return fail("full volume lands after the requested date: state the slip in days")
    wl = next((l for l in lt.splitlines() if l.lower().startswith("warmup settings")), "")
    if not wl or "limit" not in wl.lower() or "reply" not in wl.lower() or len(re.findall(r"\d+", wl)) < 3:
        return fail("Launch Timeline needs a 'Warmup settings' line with single values for increase, daily limit and reply rate")
    if req and req < paths["standard"][2]:
        wide = [r for r in table_rows(lt) if r and "wide" in r[0].lower()]
        if not wide or not re.search(r"\d[\d,]* mailboxes", " ".join(wide[0])) or to_date(" ".join(wide[0])) is None:
            return fail("standard path misses the requested date: add a dated 'Wide build' row with its mailbox count")
        if not any("wide" in r[0].lower() for r in table_rows(sec["capacity plan"])):
            return fail("Capacity Plan needs the wide build row (mailboxes = daily sends / wide cap)")
        if not re.search(r"wide[^\n]*\$\d", sec["cost estimate"], re.IGNORECASE):
            return fail("Cost Estimate needs the wide build's monthly total")

    # Monitoring
    mon = sec["monitoring"].lower()
    if "postmaster" not in mon:
        return fail("Monitoring needs Google Postmaster Tools on every sending domain")
    if "snds" not in mon or not re.search(r"dedicated|shared|does not apply|not apply", mon):
        return fail("Monitoring needs the SNDS note (it covers IPs you control, so shared-IP mailboxes are out of scope)")
    if len(table_rows(sec["monitoring"])) < 3 or "0.3%" not in mon or "bounce" not in mon:
        return fail("Monitoring needs a thresholds table with the 0.3% spam line and a bounce threshold")

    # Cost, risks, checklist
    cost = sec["cost estimate"]
    if "$" not in cost or not re.search(r"^\|\s*total", cost, re.IGNORECASE | re.MULTILINE):
        return fail("Cost Estimate needs dollar figures and a Total row")
    for r in table_rows(cost):
        if r and r[0].lower().startswith("total"):
            break
        if re.search(r"validat|lead|data", r[0], re.IGNORECASE):
            return fail(f"cost row '{r[0]}' is outside the infrastructure; put it on one line under the total")
    risks = sec["launch risks and scaling triggers"]
    if not re.search(r"domain age", risks, re.IGNORECASE):
        return fail("Launch Risks and Scaling Triggers must state the domain age risk")
    if not re.search(r"blast radius", risks + mix, re.IGNORECASE):
        return fail("state the tenant blast radius")
    if len(table_rows(risks)) < 3:
        return fail("Launch Risks and Scaling Triggers needs at least 3 trigger rows")
    cl = table_rows(sec["launch checklist"])
    if len(cl) < 4:
        return fail("Launch Checklist needs at least 4 steps")
    cl_dates = [to_date(" ".join(r)) for r in cl if to_date(" ".join(r))]
    if plan_date and (not cl_dates or min(cl_dates) != plan_date):
        return fail("Day 0 is the plan date: the first checklist step is dated the prepared date")

    print(
        f"PASS - {len(sending)} sending domains with every address, {len(by_provider)} record template(s) with Postmaster rows, "
        f"standard and soft-start dates, monitoring thresholds, main domain {main_domain} excluded"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
