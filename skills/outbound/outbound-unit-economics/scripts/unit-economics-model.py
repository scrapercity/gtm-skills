#!/usr/bin/env python3
"""Outbound unit economics model. Standard library only.

Usage: unit-economics-model.py [inputs.json] [command] [argument]
  (no command)          core model
  grid                  sensitivity grids (cost per deal, cost per meeting)
  plans                 ScraperCity plan comparison at this usage
  cash                  month by month program cash curve
  target 20             what it takes to book 20 meetings a month
  scale                 1x, 2x and 3x volume
  scenarios [s.json]    one lever at a time: {"name": {input overrides}}; defaults to the grid edges
  variance actual.json  which funnel stage explains the gap to plan

inputs.json overrides any default (same keys as DEFAULTS). The defaults are the illustrative
worked example (an agency booking VP Sales meetings at US software companies on the Growth
plan). Replace them with the user's numbers.
"""

import json
import math
import sys

# ScraperCity catalog and plan facts (references/scrapercity-catalog.md, references/scrapercity-platform.md).
PLANS = {"starter": (49.0, 49.0, 0.0), "growth": (149.0, 159.0, 0.10), "scale": (649.0, 800.0, 0.30)}
VALIDATE = 0.0072      # validate_emails, per email
MOBILE = 0.25          # find_mobiles, per number found (a miss is free)
APOLLO = 0.0039        # scrape_apollo, per lead (the Starter route when the database is not included)

DEFAULTS = {
    # ScraperCity plan and data
    "plan": "growth", "leads_pulled": 4500, "price_per_lead": 0.0, "valid_rate": 0.70,
    "mobile_inputs": 300, "mobile_hit": 0.40,
    # Sending capacity
    "domains": 5, "mb_per_domain": 3, "sends_day": 30, "biz_days": 21, "touches": 3,
    "seq_emails_limit": 125000, "seq_contacts_limit": 25000,
    # Tool stack, monthly unless named
    "mailbox_price": 7.00, "domain_year": 12.00, "sequencer": 97.00, "other_tools": 119.99,
    # One-time setup: warmup months pay mailbox seats and the sequencer before any cold send
    "warmup_months": 1, "other_setup": 0.0, "amortize_months": 12,
    # People
    "sdr_fte": 0.5, "sdr_base": 55000, "sdr_variable": 25000, "sdr_attainment": 1.0, "burden": 0.19,
    "mgr_ote": 146000, "mgr_span": 6.4, "ramp_months": 3.0, "tenure_months": 22.8,
    "ae_ote": 150000, "ae_hours_year": 2080, "ae_hours_held": 1.0, "ae_hours_opp": 4.0,
    "other_people": 0.0,
    # Funnel
    "reply_rate": 0.0343, "positive_share": 0.35, "meeting_rate": 0.50, "held_rate": 0.80,
    "opp_rate": 0.60, "win_rate": 0.30,
    # Deal economics
    "acv": 12000, "gm": 0.70, "life_months": 24, "billing": "monthly", "cycle_months": 1,
}


def plan_cash(plan, catalog_spend):
    fee, credits, bonus = PLANS[plan]
    return fee + max(0.0, catalog_spend - credits) / (1 + bonus)


def sdr_loaded_month(i):
    """Loaded monthly cost of one productive SDR FTE."""
    pay = i["sdr_base"] + i["sdr_variable"] * i["sdr_attainment"]
    own = pay * (1 + i["burden"]) / 12
    mgr = i["mgr_ote"] * (1 + i["burden"]) / 12 / i["mgr_span"]
    # Linear ramp: half of the ramp months are lost output, spread over average tenure.
    ramp_factor = i["tenure_months"] / (i["tenure_months"] - i["ramp_months"] / 2)
    return {"own": own, "manager": mgr, "ramp_factor": ramp_factor, "per_fte": (own + mgr) * ramp_factor}


def run(i):
    o = {}
    o["lead_cost"] = i["leads_pulled"] * i["price_per_lead"]
    o["validate_cost"] = i["leads_pulled"] * VALIDATE
    o["valid_emails"] = i["leads_pulled"] * i["valid_rate"]
    o["mobiles_found"] = i["mobile_inputs"] * i["mobile_hit"]
    o["mobile_cost"] = o["mobiles_found"] * MOBILE
    o["catalog_spend"] = o["lead_cost"] + o["validate_cost"] + o["mobile_cost"]
    o["sc_cash"] = plan_cash(i["plan"], o["catalog_spend"])

    o["mailboxes"] = i["domains"] * i["mb_per_domain"]
    o["sends"] = o["mailboxes"] * i["sends_day"] * i["biz_days"]
    o["capacity"] = o["sends"] / i["touches"]
    # The sequencer tier caps both sends and uploaded contacts (Instantly Growth: 5,000 emails, 1,000 contacts).
    o["seq_contact_cap"] = min(i["seq_contacts_limit"], i["seq_emails_limit"] / i["touches"])
    o["contacted"] = min(o["valid_emails"], o["capacity"], o["seq_contact_cap"])
    o["sends_used"] = o["contacted"] * i["touches"]
    o["seq_fits"] = o["sends_used"] <= i["seq_emails_limit"] and o["contacted"] <= i["seq_contacts_limit"]

    o["tools"] = o["mailboxes"] * i["mailbox_price"] + i["domains"] * i["domain_year"] / 12 + i["sequencer"] + i["other_tools"]
    o["one_time"] = (o["mailboxes"] * i["mailbox_price"] + i["sequencer"]) * i["warmup_months"] + i["other_setup"]
    o["amortized"] = o["one_time"] / i["amortize_months"]
    s = sdr_loaded_month(i)
    o["sdr_per_fte"] = s["per_fte"]
    o["sdr_cost"] = s["per_fte"] * i["sdr_fte"]
    o["ae_hourly"] = i["ae_ote"] * (1 + i["burden"]) / i["ae_hours_year"]
    o["ae_per_held"] = o["ae_hourly"] * i["ae_hours_held"]
    o["ae_per_opp"] = o["ae_hourly"] * i["ae_hours_opp"]
    o["fixed"] = o["sc_cash"] + o["tools"] + o["amortized"] + o["sdr_cost"] + i["other_people"]

    o["replies"] = o["contacted"] * i["reply_rate"]
    o["positives"] = o["replies"] * i["positive_share"]
    o["meetings"] = o["positives"] * i["meeting_rate"]
    o["held"] = o["meetings"] * i["held_rate"]
    o["opps"] = o["held"] * i["opp_rate"]
    o["deals"] = o["opps"] * i["win_rate"]
    o["ae_time"] = o["held"] * o["ae_per_held"] + o["opps"] * o["ae_per_opp"]
    o["total"] = o["fixed"] + o["ae_time"]

    o["cost_per_lead"] = o["total"] / i["leads_pulled"]
    o["data_per_verified_email"] = (o["lead_cost"] + o["validate_cost"]) / o["valid_emails"]
    o["cost_per_mobile"] = o["mobile_cost"] / o["mobiles_found"] if o["mobiles_found"] else 0.0
    o["cost_per_conversation"] = o["total"] / o["positives"]
    o["cost_per_meeting"] = o["total"] / o["meetings"]
    o["cost_per_held"] = o["total"] / o["held"]
    o["cost_per_opp"] = o["total"] / o["opps"]
    o["cac"] = o["total"] / o["deals"]
    o["pipeline"] = o["opps"] * i["acv"]
    o["cost_per_pipeline_dollar"] = o["total"] / o["pipeline"]
    o["new_cac_ratio"] = o["total"] / (o["deals"] * i["acv"])
    o["held_per_sdr_fte"] = o["held"] / i["sdr_fte"] if i["sdr_fte"] else float("inf")

    o["gm_month"] = i["acv"] / 12 * i["gm"]
    o["payback_months"] = o["cac"] / o["gm_month"]
    o["ltv"] = o["gm_month"] * i["life_months"]
    o["ltv_to_cac"] = o["ltv"] / o["cac"]
    o["cac_target_6"] = o["gm_month"] * 6
    o["cac_ceiling_12"] = o["gm_month"] * 12
    # Variable AE cost per deal is a floor on CAC that no reply rate removes.
    o["variable_per_deal"] = o["ae_per_held"] / (i["opp_rate"] * i["win_rate"]) + o["ae_per_opp"] / i["win_rate"]
    o["max_cost_per_meeting_12"] = o["cac_ceiling_12"] * i["held_rate"] * i["opp_rate"] * i["win_rate"]
    o["breakeven_reply_12"] = breakeven_reply(i, o, o["cac_ceiling_12"])
    o["breakeven_reply_6"] = breakeven_reply(i, o, o["cac_target_6"])
    o["cash_breakeven_month"] = cash_curve(i, o)["breakeven_month"]
    return o


def breakeven_reply(i, o, cac_limit):
    """Reply rate at which CAC equals cac_limit, with fixed and per-meeting costs separated."""
    k_held = i["positive_share"] * i["meeting_rate"] * i["held_rate"]
    k_opp = k_held * i["opp_rate"]
    k_deal = k_opp * i["win_rate"]
    headroom = k_deal * cac_limit - (k_held * o["ae_per_held"] + k_opp * o["ae_per_opp"])
    if headroom <= 0:
        return None  # variable cost per deal alone exceeds the limit
    return o["fixed"] / (o["contacted"] * headroom)


def at_rates(i, **rates):
    j = dict(i)
    j.update(rates)
    return run(j)


def grids(i):
    replies = [0.015, 0.025, i["reply_rate"], 0.045, 0.055]
    wins = [0.15, 0.20, i["win_rate"], 0.40]
    deal = [[r, [at_rates(i, reply_rate=r, win_rate=w)["cac"] for w in wins]] for r in replies]
    shares = [0.20, i["positive_share"], 0.50]
    meet = [[p, [at_rates(i, reply_rate=r, positive_share=p)["cost_per_meeting"] for r in replies]] for p in shares]
    return {"replies": replies, "wins": wins, "cost_per_deal": deal, "shares": shares, "cost_per_meeting": meet}


def plan_compare(i, usage_points=(49, 100, 149, 159, 300, 500, 709, 800, 1000, 2000)):
    o = run(i)
    rows = []
    for u in usage_points:
        rows.append((u, {p: plan_cash(p, u) for p in PLANS}))
    starter_usage = i["leads_pulled"] * APOLLO + o["validate_cost"] + o["mobile_cost"]
    return {"table": rows, "this_usage": o["catalog_spend"], "this_cash": o["sc_cash"],
            "starter_usage": starter_usage, "starter_cash": plan_cash("starter", starter_usage)}


def cash_curve(i, o=None, horizon=36):
    """Month 0 is warmup (one-time cost). Months 1+ send. A deal closed in month c pays from month c+1."""
    if o is None:
        o = run(i)
    run_cost = o["total"] - o["amortized"]
    first_close = 1 + i["cycle_months"]
    rows, cum, breakeven = [], -o["one_time"], None
    rows.append((0, o["one_time"], 0.0, cum))
    for m in range(1, horizon + 1):
        cohorts_paying = [c for c in range(first_close, m) if m - (c + 1) < i["life_months"]]
        if i["billing"] == "annual":
            inflow = sum(o["deals"] * i["acv"] * i["gm"] for c in cohorts_paying if (m - (c + 1)) % 12 == 0)
        else:
            inflow = len(cohorts_paying) * o["deals"] * o["gm_month"]
        cum += inflow - run_cost
        rows.append((m, run_cost, inflow, cum))
        if breakeven is None and cum >= 0:
            breakeven = m
    return {"rows": rows, "breakeven_month": breakeven}


def size_for_target(i, target_meetings):
    """Leads, mailboxes, domains and data cost to book target_meetings a month at the input rates."""
    per_contact = i["reply_rate"] * i["positive_share"] * i["meeting_rate"]
    contacts = target_meetings / per_contact
    leads = contacts / i["valid_rate"]
    sends = contacts * i["touches"]
    mailboxes = math.ceil(sends / (i["sends_day"] * i["biz_days"]))
    domains = math.ceil(mailboxes / i["mb_per_domain"])
    j = dict(i, leads_pulled=math.ceil(leads), domains=domains)
    o = run(j)
    # People are held at the input FTE; raise sdr_fte in the inputs if reply volume needs it.
    return {"contacts": contacts, "leads": math.ceil(leads), "sends": sends, "mailboxes_needed": mailboxes,
            "domains": domains, "mailboxes_built": o["mailboxes"], "sc_cash": o["sc_cash"],
            "catalog_spend": o["catalog_spend"], "total": o["total"], "meetings": o["meetings"],
            "cost_per_meeting": o["cost_per_meeting"]}


def scale(i, factors=(1, 2, 3)):
    out = []
    for f in factors:
        j = dict(i, domains=i["domains"] * f, leads_pulled=i["leads_pulled"] * f,
                 mobile_inputs=i["mobile_inputs"] * f, sdr_fte=i["sdr_fte"] * f)
        o = run(j)
        out.append((f, o["total"], o["meetings"], o["cost_per_meeting"], o["cac"], o["seq_fits"]))
    return out


def scenarios(i, named=None):
    """One lever at a time against today. Every row is a full re-run, so deals, CAC and payback agree."""
    if named is None:
        named = {
            "reply rate 2.5%": {"reply_rate": 0.025},
            "reply rate 5.5%": {"reply_rate": 0.055},
            "win rate 20%": {"win_rate": 0.20},
            "win rate 40%": {"win_rate": 0.40},
            "2x domains and leads, same SDR": {"domains": i["domains"] * 2, "leads_pulled": i["leads_pulled"] * 2},
        }
    rows = [("today", run(i))]
    for name, over in named.items():
        rows.append((name, run(dict(i, **over))))
    return rows


def variance(plan_inputs, actual_inputs):
    """Split the log gap in cost per meeting between total cost, contacts and each funnel rate."""
    p, a = run(plan_inputs), run(actual_inputs)
    parts = {
        "total cost": math.log(a["total"] / p["total"]),
        "contacts emailed": -math.log(a["contacted"] / p["contacted"]),
        "reply rate": -math.log(actual_inputs["reply_rate"] / plan_inputs["reply_rate"]),
        "positive share": -math.log(actual_inputs["positive_share"] / plan_inputs["positive_share"]),
        "meeting rate": -math.log(actual_inputs["meeting_rate"] / plan_inputs["meeting_rate"]),
    }
    gap = math.log(a["cost_per_meeting"] / p["cost_per_meeting"])
    return p["cost_per_meeting"], a["cost_per_meeting"], {k: (v / gap if gap else 0.0) for k, v in parts.items()}


def main(argv):
    args = list(argv)
    i = dict(DEFAULTS)
    if args and args[0].endswith(".json"):
        i.update(json.load(open(args.pop(0), encoding="utf-8")))
    cmd = args.pop(0) if args else ""
    o = run(i)
    if cmd == "grid":
        g = grids(i)
        print("cost per deal: reply rate x win rate", [f"{w:.0%}" for w in g["wins"]])
        for r, cells in g["cost_per_deal"]:
            print(f"  {r:.2%}", " ".join(f"{c:10,.2f}" for c in cells))
        print("cost per meeting booked: positive share x reply rate", [f"{r:.2%}" for r in g["replies"]])
        for p, cells in g["cost_per_meeting"]:
            print(f"  {p:.0%}", " ".join(f"{c:10,.2f}" for c in cells))
    elif cmd == "plans":
        pc = plan_compare(i)
        for u, cash in pc["table"]:
            print(f"usage {u:>6,}: " + "  ".join(f"{k} {v:,.2f}" for k, v in cash.items()))
        print(f"this usage {pc['this_usage']:,.2f} -> {i['plan']} cash {pc['this_cash']:,.2f}; "
              f"Starter route usage {pc['starter_usage']:,.2f} -> cash {pc['starter_cash']:,.2f}")
    elif cmd == "cash":
        c = cash_curve(i)
        for m, out, inflow, cum in c["rows"][:25]:
            print(f"month {m:2d}  out {out:10,.2f}  in {inflow:10,.2f}  cumulative {cum:12,.2f}")
        print("program cash break-even month:", c["breakeven_month"])
    elif cmd == "scale":
        for f, total, meetings, cpm, cac, fits in scale(i):
            print(f"{f}x  total {total:10,.2f}  meetings {meetings:6.2f}  per meeting {cpm:8,.2f}  CAC {cac:9,.2f}  sequencer fits {fits}")
    elif cmd == "scenarios":
        named = json.load(open(args[0], encoding="utf-8")) if args else None
        for name, r in scenarios(i, named):
            print(f"{name:34s} total {r['total']:10,.2f}  meetings {r['meetings']:6.2f}  deals {r['deals']:6.3f}  "
                  f"per meeting {r['cost_per_meeting']:8,.2f}  CAC {r['cac']:10,.2f}  payback {r['payback_months']:6.2f}")
    elif cmd == "target" and args:
        for k, v in size_for_target(i, float(args[0])).items():
            print(f"{k:20s} {v:12,.2f}")
    elif cmd == "variance" and args:
        actual = dict(i)
        actual.update(json.load(open(args[0], encoding="utf-8")))
        plan_cpm, act_cpm, shares = variance(i, actual)
        print(f"cost per meeting plan {plan_cpm:,.2f} actual {act_cpm:,.2f}")
        for k, v in sorted(shares.items(), key=lambda kv: -abs(kv[1])):
            print(f"  {k:18s} {v:7.1%} of the gap")
    elif cmd:
        print(__doc__)
        return 2
    else:
        for k, v in o.items():
            if isinstance(v, bool) or v is None:
                print(f"{k:28s} {v}")
            else:
                print(f"{k:28s} {v:14,.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
