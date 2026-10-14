#!/usr/bin/env python3
"""Check an outbound unit economics model produced with the outbound-unit-economics skill.

Usage: check-output.py path/to/model.md
Prints PASS or FAIL with a reason. Exit 0 on pass, 1 on fail, 2 on usage error.

Beyond structure, it recomputes the numbers: every "a x b = c" expression in a table, catalog
prices, the plan cash formula, the cost stack total, the funnel chain, every cost per outcome,
payback, the break-even reply rate, every cell of the cost per deal grid and every row of the
one-lever scenario table. It also enforces the deliverable's economy: only the nine sections plus
Sources, one Cost Stack table, one grid plus one scenario table, a word ceiling, no tool ids,
parameters, code spans, skill names, file paths or disclaimers, owners and dates on every
recommendation, and every message the recommendation names written out. It fails a model that
carries legal content, using the term list in the repo's scripts/validate-skills.py.
"""

import ast
import importlib.util
import operator
import re
import sys
from pathlib import Path

REQUIRED = [
    "Inputs", "ScraperCity Cost", "Cost Stack", "Capacity", "Funnel",
    "Unit Costs", "Break-even", "Sensitivity", "Recommendation",
]
ALLOWED = REQUIRED + ["Sources"]
# Catalog prices from references/scrapercity-catalog.md (npm scrapercity 1.0.17), keyed by the plain
# product name the deliverable uses in the ScraperCity Cost "Tool" column (tool ids never appear).
PRICES = {
    "email validat": 0.0072, "mobile finder": 0.25, "email finder": 0.05, "apollo": 0.0039,
    "google maps": 0.0099, "website finder": 0.0499, "store leads": 0.0039, "people finder": 0.0199,
    "yelp": 0.0099, "angi": 0.0099, "bizbuysell": 0.0099, "crexi": 0.029, "zillow": 0.029,
    "airbnb": 0.019, "property lookup": 0.15, "distress list": 0.05,
}
TOOL_ID = re.compile(r"\b(check_wallet|list_runs|check_run_status|download_results|query_\w+|validate_emails|"
                     r"find_mobiles|find_emails|find_people|scrape_\w+|search_\w+_records)\b")
PARAM = re.compile(r"\b(hasEmail|hasContact|hasPhone|excludeDelivered|pagination\.total|totalLeads)\b|\blimit:\s*\d")
DISCLAIMER = re.compile(r"not (financial|accounting|legal|tax|investment) advice", re.IGNORECASE)
NOT_RUN = re.compile(r"nothing (was|has been) run|(not|never) (been )?run here|no tools? (was|were) run", re.IGNORECASE)
MONTHS = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*"
DATE = re.compile(rf"\b\d{{1,2}} {MONTHS} 20\d\d\b|\b{MONTHS} \d{{1,2}},? 20\d\d\b|\b20\d\d-\d\d-\d\d\b")
MESSAGE_KINDS = ("confirmation", "reminder", "no-show", "qualifying question", "rebook", "follow-up email", "script")
PLANS = {"starter": (49, 49, 0.0), "growth": (149, 159, 0.10), "scale": (649, 800, 0.30)}
INPUT_TYPES = ("user input", "catalog", "benchmark", "assumption", "measured")
FUNNEL_ORDER = ["contacts", "replies", "positive", "meetings booked", "meetings held", "opportunit", "deals"]
MIN_WORDS = 500
MAX_WORDS = 2000  # words with a letter or digit (table pipes excluded); economy: the model, the fixes and their copy, nothing else
MIN_TABLE_ROWS = 30
TOL = 0.01  # 1% relative, rounding of displayed inputs
PLACEHOLDER = re.compile(r"\[(fill|todo|tbd)\]|<[A-Za-z][A-Za-z _-]*>", re.IGNORECASE)
INTERNAL_PATH = re.compile(r"\b(references|scripts|templates|examples)/[\w.-]+\.(md|py)\b")
MONEY = re.compile(r"\$\s?(-?[\d,]+(?:\.\d+)?)")
PCT = re.compile(r"(-?\d+(?:\.\d+)?)\s*%")
NUM = re.compile(r"-?\d[\d,]*(?:\.\d+)?")
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def legal_hit(text):
    """First legal term in the text, using validate-skills.py's list (owner rule, 2026-10-13).

    Returns None when the checker runs outside the repo and the list is not available.
    """
    for parent in Path(__file__).resolve().parents:
        validator = parent / "scripts" / "validate-skills.py"
        if validator.is_file():
            spec = importlib.util.spec_from_file_location("validate_skills", validator)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for line in text.splitlines():
                hits = module.legal_hits(line, "")
                if hits:
                    return hits[0]
            return None
    return None


def skill_names():
    """This skill's name and its related skills, read from SKILL.md next to scripts/."""
    skill_md = Path(__file__).resolve().parent.parent / "SKILL.md"
    if not skill_md.is_file():
        return []
    text = skill_md.read_text(encoding="utf-8")
    fm = text.split("---")[1] if text.startswith("---") else ""
    block = re.search(r"related_skills:\s*\n((?:\s+-\s+\S+\s*\n)+)", fm)
    names = re.findall(r"-\s+(\S+)", block.group(1)) if block else []
    own = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
    return names + ([own.group(1)] if own else [])


def fail(msg):
    print(f"FAIL - {msg}")
    sys.exit(1)


def close(a, b, rel=TOL, abs_tol=0.011):
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b)))


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
    found = []
    lines = [l.strip() for l in block.splitlines()]
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", lines[i + 1]):
            head = [h.strip().lower() for h in line.strip("|").split("|")]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(dict(zip(head, [c.strip() for c in lines[j].strip("|").split("|")])))
                j += 1
            found.append((head, rows))
    return found


def rows_of(block):
    return [r for _, rows in tables(block) for r in rows]


def money(s, last=True):
    vals = [float(v.replace(",", "")) for v in MONEY.findall(s or "")]
    return (vals[-1] if last else vals[0]) if vals else None


def number(s):
    m = NUM.search(s or "")
    return float(m.group(0).replace(",", "")) if m else None


def pct(s):
    m = PCT.search(s or "")
    return float(m.group(1)) / 100 if m else None


def evaluate(expr):
    """Evaluate pure arithmetic written in the model's style ($, thousands commas, x, %). None if not pure."""
    s = expr.replace("$", "")
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1/100)", s)
    s = re.sub(r"\s[x" + chr(0xd7) + r"]\s", " * ", s)
    if re.search(r"[^\d.+\-*/() ]", s) or not re.search(r"[+\-*/]", s.strip().lstrip("-")):
        return None
    try:
        tree = ast.parse(s.strip(), mode="eval")
    except SyntaxError:
        return None

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return float(n.value)
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -ev(n.operand)
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        raise ValueError
    try:
        return ev(tree)
    except (ValueError, ZeroDivisionError):
        return None


def stated(rhs):
    """The number a right-hand side states, as a fraction when written as a percent."""
    rhs = rhs.strip()
    m = re.match(r"^\$?\s?(-?[\d,]+(?:\.\d+)?)\s*(%?)", rhs)
    if not m:
        return None
    v = float(m.group(1).replace(",", ""))
    return v / 100 if m.group(2) else v


def check_arithmetic(text):
    """Every table cell written as 'expression = result', and every Formula/Value pair, must hold."""
    checked = 0
    for head, rows in tables(text):
        for r in rows:
            for cell in r.values():
                if "=" in cell:
                    lhs, rhs = cell.rsplit("=", 1)
                    got, want = evaluate(lhs), stated(rhs)
                    if got is not None and want is not None:
                        checked += 1
                        if not close(got, want):
                            fail(f"arithmetic: '{cell}' computes to {got:,.4f}")
            if "formula" in r and "value" in r:
                got, want = evaluate(r["formula"]), stated(r["value"])
                if got is not None and want is not None:
                    checked += 1
                    if not close(got, want):
                        fail(f"arithmetic: '{r['formula']}' computes to {got:,.4f}, row says {r['value']}")
    return checked


def find(rows, key, start):
    return next((r for r in rows if r.get(key, "").lower().startswith(start)), None)


def main():
    if len(sys.argv) != 2:
        print("usage: check-output.py path/to/model.md")
        sys.exit(2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print(f"usage: cannot read {sys.argv[1]}: {exc}")
        sys.exit(2)

    hit = PLACEHOLDER.search(text)
    if hit:
        fail(f"placeholder left in the model: {hit.group(0)}")
    secs = sections(text)
    for name in REQUIRED:
        if name.lower() not in secs:
            fail(f"missing section '## {name}'")
    words = len([w for w in text.split() if re.search(r"[A-Za-z0-9]", w)])
    if words < MIN_WORDS:
        fail(f"model has {words} words, minimum is {MIN_WORDS}")
    all_rows = rows_of(text)
    if len(all_rows) < MIN_TABLE_ROWS:
        fail(f"model has {len(all_rows)} table rows, minimum is {MIN_TABLE_ROWS}")
    if re.search("[" + chr(0x2013) + chr(0x2014) + "]", text):
        fail("em or en dash in the model")
    m = INTERNAL_PATH.search(text)
    if m:
        fail(f"internal file path in the deliverable: {m.group(0)}")
    legal = legal_hit(text)
    if legal:
        fail(f"legal content in the model: {legal}; remove it (owner rule)")

    # 0. Economy and plain language.
    if words > MAX_WORDS:
        fail(f"model has {words} words, maximum is {MAX_WORDS}; state each fact once and cut what the user did not ask for")
    heads = [h for h in re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]
    for h in heads:
        if h not in ALLOWED:
            fail(f"section '## {h}' is not part of the model; allowed: {', '.join(ALLOWED)}")
    order = [h for h in heads if h in REQUIRED]
    if order != REQUIRED:
        fail("sections must appear once each, in order: " + ", ".join(REQUIRED))
    if "`" in text:
        fail("code span in the deliverable; write tools and settings in plain words")
    m = TOOL_ID.search(text) or PARAM.search(text)
    if m:
        fail(f"internal tool id or parameter in the deliverable: '{m.group(0)}'; say what it does in plain words")
    for name in skill_names():
        if re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", text):
            fail(f"skill name '{name}' in the deliverable; describe the next step instead")
    if re.search(r"SKILL\.md|check-output|unit-economics-model\.py", text):
        fail("internal file or script named in the deliverable")
    m = DISCLAIMER.search(text)
    if m:
        fail(f"disclaimer in the deliverable: '{m.group(0)}'")
    if len(NOT_RUN.findall(text)) > 1:
        fail("the 'nothing was run' note appears more than once; say it once at the top")
    for line in text.splitlines():
        if re.search(r"instantly growth|growth \(\$47|growth at \$47", line, re.IGNORECASE) and "5,000" in line \
                and "1,000" not in line:
            fail("Instantly Growth is capped at 5,000 emails AND 1,000 uploaded contacts a month (instantly.ai/pricing); "
                 "state the contact cap wherever the tier is sized")

    # 1. Every input is typed, and benchmarks carry a year.
    inputs = rows_of(secs["inputs"])
    if len(inputs) < 12:
        fail(f"Inputs has {len(inputs)} rows, minimum is 12")
    for r in inputs:
        t = r.get("type", "").lower()
        if not any(t.startswith(x) for x in INPUT_TYPES):
            fail(f"input '{r.get('input')}' needs a type: {', '.join(INPUT_TYPES)}")
        if t.startswith("benchmark") and not re.search(r"20\d\d", r.get("source", "")):
            fail(f"benchmark input '{r.get('input')}' needs a dated source")

    # 2. Catalog prices, line arithmetic, plan fee and credits, plan cash formula.
    cost_rows = rows_of(secs["scrapercity cost"])
    plan, spend = None, 0.0
    for r in cost_rows:
        line = " | ".join(r.values()).lower()
        for name, (fee, credits, _) in PLANS.items():
            if f"{name} plan" in line or (name in line and "plan" in r.get("line", "").lower()):
                if f"${fee}" not in line or f"${credits}" not in line:
                    fail(f"{name.title()} plan row must show the ${fee} fee and ${credits} credits")
                plan = plan or name
        tool = r.get("tool", "").lower()
        for key, price in PRICES.items():
            if key in tool and "miss" not in tool and "no number" not in tool and "not found" not in tool:
                unit = money(r.get("unit price", ""))
                if unit is None or abs(unit - price) > 1e-9:
                    fail(f"{key} must be priced at ${price} per result, found '{r.get('unit price')}'")
                count, cost = number(r.get("count", "")), money(r.get("cost", ""))
                if count is None or cost is None:
                    fail(f"{key} row needs a count and a dollar cost")
                if abs(count * price - cost) > 0.01:
                    fail(f"{key} row: {count:g} x ${price} = ${count * price:.2f}, not ${cost:.2f}")
                spend += cost
                break
    if not plan:
        fail("ScraperCity Cost needs a plan row naming Starter, Growth or Scale with its fee and credits")
    fee, credits, bonus = PLANS[plan]
    cash_row = find(cost_rows, "line", "scrapercity cash")
    if not cash_row:
        fail("ScraperCity Cost needs a 'ScraperCity cash' row")
    expected_cash = fee + max(0.0, spend - credits) / (1 + bonus)
    if not close(money(cash_row.get("cost", "")) or -1, expected_cash, rel=0, abs_tol=0.02):
        fail(f"ScraperCity cash should be ${expected_cash:,.2f} on {plan.title()} for ${spend:,.2f} of catalog spend")

    # 3. Cost stack: count x unit, sum to total, variable lines tied to the funnel.
    if len(tables(secs["cost stack"])) != 1:
        fail("Cost Stack is one table; put the SDR and AE derivations in a one-line note under it, not a second table")
    stack = next((rows for head, rows in tables(secs["cost stack"]) if "basis" in head), None)
    if not stack:
        fail("Cost Stack needs a table with Line, Basis, Count, Unit cost and Monthly cost")
    total_row = find(stack, "line", "total")
    if not total_row:
        fail("Cost Stack needs a 'Total monthly program cost' row")
    total = money(total_row.get("monthly cost", ""))
    fixed, per_held, per_opp, summed, held_count, opp_count = 0.0, 0.0, 0.0, 0.0, None, None
    for r in stack:
        if r is total_row:
            continue
        basis = r.get("basis", "").lower()
        count, unit_cost, monthly = number(r.get("count", "")), money(r.get("unit cost", "")), money(r.get("monthly cost", ""))
        if None in (count, unit_cost, monthly):
            fail(f"Cost Stack row '{r.get('line')}' needs a count, a unit cost and a monthly cost")
        if not close(count * unit_cost, monthly):
            fail(f"Cost Stack row '{r.get('line')}': {count:g} x ${unit_cost:,.2f} is not ${monthly:,.2f}")
        summed += monthly
        if basis.startswith("per held"):
            per_held, held_count = per_held + unit_cost, count
        elif basis.startswith("per opportunit"):
            per_opp, opp_count = per_opp + unit_cost, count
        elif basis.startswith(("fixed", "amortized")):
            fixed += monthly
        else:
            fail(f"Cost Stack row '{r.get('line')}' basis must be fixed, amortized, per held meeting or per opportunity")
    if not close(summed, total, rel=0, abs_tol=1.0):
        fail(f"Cost Stack lines sum to ${summed:,.2f}, total says ${total:,.2f}")
    sc_line = find(stack, "line", "scrapercity")
    if not sc_line or not close(money(sc_line.get("monthly cost", "")), expected_cash, rel=0, abs_tol=0.02):
        fail("Cost Stack must carry the ScraperCity cash line at the same amount as ScraperCity Cost")
    unit_rows = rows_of(secs["unit costs"])
    ut = find(unit_rows, "metric", "total monthly")
    if not ut or not close(money(ut.get("value", "")) or -1, total, rel=0, abs_tol=0.05):
        fail("Unit Costs 'Total monthly program cost' must equal the Cost Stack total")

    # 4. Funnel chain: each count = previous count x rate.
    funnel = rows_of(secs["funnel"])
    stages = {}
    for key in FUNNEL_ORDER:
        r = next((f for f in funnel if key in f.get("stage", "").lower()), None)
        if not r:
            fail(f"Funnel needs a '{key}' stage")
        stages[key] = r
    prev = None
    rates = {}
    for key in FUNNEL_ORDER:
        r = stages[key]
        count = number(r.get("count", ""))
        if count is None:
            fail(f"Funnel '{r.get('stage')}' needs a count")
        if prev is not None:
            rate = pct(r.get("rate", ""))
            if rate is None:
                fail(f"Funnel '{r.get('stage')}' needs a rate in percent")
            rates[key] = rate
            if not close(prev * rate, count):
                fail(f"Funnel '{r.get('stage')}': {prev:,.2f} x {rate:.2%} = {prev * rate:,.2f}, not {count:,.2f}")
        prev = count
    contacts = number(stages["contacts"].get("count", ""))
    held = number(stages["meetings held"].get("count", ""))
    opps = number(stages["opportunit"].get("count", ""))
    if held_count is not None and not close(held_count, held):
        fail("AE time per held meeting must use the Funnel's held count")
    if opp_count is not None and not close(opp_count, opps):
        fail("AE time per opportunity must use the Funnel's opportunity count")

    # 5. Every cost per outcome = total / count.
    for stage, metric in (("meetings booked", "cost per meeting booked"), ("meetings held", "cost per meeting held"),
                          ("opportunit", "cost per opportunity"), ("deals", "cost per deal")):
        label = stages[stage].get("stage", stage).lower()
        u = find(unit_rows, "metric", metric)
        if not u:
            fail(f"Unit Costs needs a '{metric}' row")
        count, value = number(stages[stage].get("count", "")), money(u.get("value", ""))
        if not count or value is None or not close(total / count, value):
            fail(f"{metric} should be about ${total / count:,.2f} (total / {label})")
    cac = money(find(unit_rows, "metric", "cost per deal").get("value", ""))

    # 6. Arithmetic written anywhere in a table.
    checked = check_arithmetic(text)
    if checked < 15:
        fail(f"only {checked} computations are shown; show the arithmetic (for example '15 x 30 x 21 = 9,450')")

    # 7. Break-even: margin, payback, break-even reply rate recomputed from the stack and the funnel.
    be_rows = rows_of(secs["break-even"])
    gm_row, payback_row = find(be_rows, "measure", "monthly gross margin"), find(be_rows, "measure", "cac payback")
    ceiling_row = find(be_rows, "measure", "cac ceiling")
    if not (gm_row and payback_row and ceiling_row):
        fail("Break-even needs 'Monthly gross margin per deal', 'CAC ceiling' and 'CAC payback' rows")
    gm = money(gm_row.get("value", ""))
    ceiling = money(ceiling_row.get("value", ""))
    pm = re.search(r"(\d+(?:\.\d+)?)\s*months", payback_row.get("value", ""))
    if not gm or not pm or not close(cac / gm, float(pm.group(1))):
        fail(f"CAC payback should be {cac / gm:.2f} months (CAC / monthly gross margin)")
    if not close(ceiling, gm * 12):
        fail("CAC ceiling must be 12 months of gross margin per deal")
    k_held = rates["positive"] * rates["meetings booked"] * rates["meetings held"]
    k_opp = k_held * rates["opportunit"]
    k_deal = k_opp * rates["deals"]
    ber = find(be_rows, "measure", "break-even reply rate, 12")
    if not ber:
        fail("Break-even needs a 'Break-even reply rate, 12 month ceiling' row")
    headroom = k_deal * ceiling - k_held * per_held - k_opp * per_opp
    stated_ber = pct(ber.get("value", ""))
    if headroom <= 0:
        if stated_ber is not None:
            fail("no reply rate pays back: AE cost per deal alone exceeds the CAC ceiling; say so")
    elif stated_ber is None or not close(fixed / (contacts * headroom), stated_ber, rel=0.02, abs_tol=0.0001):
        fail(f"break-even reply rate at the 12 month ceiling should be {fixed / (contacts * headroom):.2%}")

    def total_at(r, share=None):
        s = rates["positive"] if share is None else share
        kh = s * rates["meetings booked"] * rates["meetings held"]
        return fixed + contacts * r * (kh * per_held + kh * rates["opportunit"] * per_opp), kh

    # 8. Sensitivity grids, every cell recomputed.
    grids = tables(secs["sensitivity"])
    deal_grid = next(((h, rows) for h, rows in grids if h and h[0].startswith("reply")), None)
    if not deal_grid or len(deal_grid[1]) < 3 or len(deal_grid[0]) < 4:
        fail("Sensitivity needs a cost per deal grid: at least 3 reply rates by 3 win rates")
    head, rows = deal_grid
    for r in rows:
        rr = pct(r[head[0]])
        for col in head[1:]:
            w, cell = pct(col), money(r.get(col, ""))
            if rr is None or w is None or cell is None:
                fail("Sensitivity grid needs percent row and column labels and dollar cells")
            t, kh = total_at(rr)
            want = t / (contacts * rr * kh * rates["opportunit"] * w)
            if not close(want, cell):
                fail(f"cost per deal at {rr:.2%} replies and {w:.0%} wins should be ${want:,.2f}")
    if len(grids) > 2:
        fail("Sensitivity holds one cost per deal grid and one scenario table; cut any other grid")
    others = [(h, rows) for h, rows in grids if (h, rows) != deal_grid]
    for h, rows in others:
        cols = {c: next((x for x in h if x.startswith(c)), None) for c in ("total", "meetings", "deals", "cac", "payback")}
        if not (cols["total"] and cols["deals"] and cols["cac"]):
            fail("the second Sensitivity table must be the one-lever scenario table: Total cost, Meetings booked, "
                 "Deals, CAC and Payback columns")
        for r in rows:
            t, d, c = money(r.get(cols["total"], "")), number(r.get(cols["deals"], "")), money(r.get(cols["cac"], ""))
            name = r.get(h[0], "")
            if None in (t, d, c) or not d:
                fail(f"scenario '{name}' needs a total, deals and CAC")
            if not close(t / d, c, rel=0.015):
                fail(f"scenario '{name}': ${t:,.2f} / {d:g} deals = ${t / d:,.2f}, not ${c:,.2f}; recompute the row")
            if cols["meetings"] and "cost per meeting" in " ".join(h):
                mcol = next(x for x in h if x.startswith("cost per meeting"))
                mt, cm = number(r.get(cols["meetings"], "")), money(r.get(mcol, ""))
                if mt and cm is not None and not close(t / mt, cm, rel=0.015):
                    fail(f"scenario '{name}': cost per meeting should be ${t / mt:,.2f}")
            if cols["payback"]:
                pb = re.search(r"(\d+(?:\.\d+)?)", r.get(cols["payback"], ""))
                if not pb or not close(c / gm, float(pb.group(1)), rel=0.015):
                    fail(f"scenario '{name}': payback should be {c / gm:.2f} months")

    # 9. The recommendation names the reply rate to beat.
    rec_tables = tables(secs["recommendation"])
    if not rec_tables:
        fail("Recommendation needs its decision table")
    head, rec = rec_tables[0]
    if "owner" not in head or "due" not in head:
        fail("Recommendation table needs Owner and Due columns: who on the user's team does it, and by what date")
    for r in rec:
        if not r.get("owner") or not DATE.search(r.get("due", "")):
            fail(f"Recommendation row '{r.get(head[0])}' needs an owner and a calendar date (for example 23 Oct 2026)")
    if not any("reply rate" in " ".join(r.values()).lower() and pct(" ".join(r.values())) for r in rec):
        fail("Recommendation must name the reply rate the program has to beat")
    rec_text = " ".join(" ".join(r.values()) for r in rec).lower()
    kinds = [k for k in MESSAGE_KINDS if k in rec_text]
    quotes = len(re.findall(r"(?:^|\n)(?:>[^\n]*\n?)+", secs["recommendation"]))
    if kinds and quotes < len(kinds):
        fail(f"the Recommendation names {', '.join(kinds)} but writes out {quotes} message(s); "
             "write every message it names in full as a quote block")
    has_benchmark = any(r.get("type", "").lower().startswith("benchmark") for r in inputs)
    if has_benchmark and not re.search(r"https?://", secs.get("sources", "")):
        fail("benchmarks are used, so end with '## Sources' listing the URL behind each one")

    print(f"PASS - {len(inputs)} typed inputs, {checked} computations and every cost per outcome, "
          f"payback, break-even and grid cell recomputed")
    sys.exit(0)


if __name__ == "__main__":
    main()
