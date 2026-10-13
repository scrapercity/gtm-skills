# Unit Economics Model

The spreadsheet-ready model behind this skill: input defaults with their types, every cell and formula, a CSV block to paste into Google Sheets or Excel, and a Python reference implementation that reproduces the same numbers. The example values are the worked example's inputs (an agency booking VP Sales meetings at US software companies on the Growth plan).

## 1. How to use it

1. Paste the CSV block (section 4) into cell A1 of an empty sheet. Column A holds labels, column B holds values and formulas, row 1 is the header, so the first input lands in B2.
2. Replace every value in B2 to B27 with the user's numbers. Keep the type labels from section 2 next to the sheet so nobody mistakes an assumption for a fact.
3. Read the outputs in B28 to B56.
4. Check the sheet by running the Python block (section 5) with the same inputs. Every output must match to the cent.
5. Build the sensitivity grids from `references/break-even-and-sensitivity.md` by copying the sheet and changing B20 (reply rate) and B24 (close rate), or with the Python `run()` function in a loop.

## 2. Inputs, defaults and types

| Input | Cell | Default | Type | Source or note |
|-|-|-|-|-|
| Plan fee | B2 | 149 | catalog | Starter 49, Growth 149, Scale 649 (scrapercity.com/pricing, checked 2026-10-12) |
| Plan credits | B3 | 159 | catalog | Starter 49, Growth 159, Scale 800 |
| Bonus on purchased credits | B4 | 0.10 | catalog | Starter 0, Growth 0.10, Scale 0.30 |
| Leads pulled | B5 | 4,500 | user input | Size to capacity (B37) divided by the valid rate |
| Catalog price per lead | B6 | 0 | catalog | Lead Database and Local Business Database on Growth or Scale 0; `scrape_apollo` 0.0039; `scrape_store_leads` 0.0039; `scrape_maps` 0.0099 |
| Valid rate | B7 | 0.70 | assumption | Measure with a 200-email `validate_emails` test ($1.44) |
| Inputs to `find_mobiles` | B8 | 300 | user input | Tier A accounts or calls planned |
| Mobile hit rate | B9 | 0.40 | assumption | Measure with 100 inputs; cost per mobile stays $0.25 |
| Sending domains | B10 | 5 | user input | `domain-infrastructure` |
| Mailboxes per domain | B11 | 3 | user input | 2 to 3 per `references/deliverability-primer.md` |
| Sends per mailbox per day | B12 | 30 | assumption | House standard in `references/deliverability-primer.md`; 50 maximum on a clean record |
| Business days per month | B13 | 21 | assumption | |
| Touches per contact | B14 | 3 | user input | Sequence length |
| Mailbox seat price | B15 | 7 | user input | The user's Google Workspace or Microsoft 365 bill |
| Domain price per year | B16 | 12 | user input | The user's registrar bill |
| Sequencer per month | B17 | 97 | user input | The user's Instantly, Smartlead, Lemlist, EmailBison or ManyReach bill |
| Other tools per month | B18 | 0 | user input | Warmup, verification add-ons, dialer seats |
| People cost per month | B19 | 4,500 | user input | Share of SDR, reply handling and AE time on this program |
| Reply rate | B20 | 0.0343 | benchmark | Instantly 2026 benchmark average 3.43%; Hunter 2025 report 4.1% on 2024 sends |
| Positive share of replies | B21 | 0.35 | assumption | No published source used; measure from reply classes (`reply-handling`) |
| Meetings per positive reply | B22 | 0.50 | assumption | Measure |
| Held rate | B23 | 0.80 | assumption | Measure |
| Close rate | B24 | 0.20 | assumption | The user's CRM history for outbound-sourced deals |
| ACV | B25 | 12,000 | user input | |
| Gross margin | B26 | 0.70 | user input | |
| Lifetime months | B27 | 24 | user input | |

## 3. Cells and formulas

| Cell | Label | Value or formula | Example result |
|-|-|-|-|
| B2 | ScraperCity plan fee per month (Starter 49, Growth 149, Scale 649) | `149` | 149.00 |
| B3 | Plan credits per month (Starter 49, Growth 159, Scale 800) | `159` | 159.00 |
| B4 | Bonus on purchased credits (Starter 0, Growth 0.10, Scale 0.30) | `0.1` | 0.1 |
| B5 | Leads pulled this month | `4500` | 4,500.00 |
| B6 | Catalog price per lead (Lead Database on Growth 0, Apollo 0.0039, Maps 0.0099) | `0` | 0 |
| B7 | Share of pulled emails that validate as valid | `0.7` | 0.7 |
| B8 | Inputs sent to find_mobiles | `300` | 300.00 |
| B9 | Mobile Finder hit rate | `0.4` | 0.4 |
| B10 | Sending domains | `5` | 5.00 |
| B11 | Mailboxes per domain | `3` | 3.00 |
| B12 | Cold sends per mailbox per day | `30` | 30.00 |
| B13 | Business days per month | `21` | 21.00 |
| B14 | Touches per contact | `3` | 3.00 |
| B15 | Mailbox seat price per month (user input) | `7` | 7.00 |
| B16 | Domain price per year (user input) | `12` | 12.00 |
| B17 | Sequencer subscription per month (user input) | `97` | 97.00 |
| B18 | Other tools per month (user input) | `0` | 0 |
| B19 | People cost per month allocated to this program (user input) | `4500` | 4,500.00 |
| B20 | Reply rate | `0.0343` | 0.0343 |
| B21 | Positive share of replies | `0.35` | 0.35 |
| B22 | Meetings booked per positive reply | `0.5` | 0.5 |
| B23 | Held share of booked meetings | `0.8` | 0.8 |
| B24 | Close rate of held meetings | `0.2` | 0.2 |
| B25 | Annual contract value | `12000` | 12,000.00 |
| B26 | Gross margin | `0.7` | 0.7 |
| B27 | Customer lifetime in months | `24` | 24.00 |
| B28 | Lead cost at catalog price | `=B5*B6` | 0 |
| B29 | validate_emails cost | `=B5*0.0072` | 32.40 |
| B30 | Valid emails | `=B5*B7` | 3,150.00 |
| B31 | Mobiles found | `=B8*B9` | 120.00 |
| B32 | find_mobiles cost | `=B31*0.25` | 30.00 |
| B33 | Catalog-price spend | `=B28+B29+B32` | 62.40 |
| B34 | ScraperCity cash | `=B2+MAX(0,B33-B3)/(1+B4)` | 149.00 |
| B35 | Mailboxes | `=B10*B11` | 15.00 |
| B36 | Sends per month | `=B35*B12*B13` | 9,450.00 |
| B37 | New contacts per month at capacity | `=B36/B14` | 3,150.00 |
| B38 | Contacts emailed | `=MIN(B30,B37)` | 3,150.00 |
| B39 | Inbox, domain and tool cost | `=B35*B15+B10*B16/12+B17+B18` | 207.00 |
| B40 | Total monthly program cost | `=B34+B39+B19` | 4,856.00 |
| B41 | Replies | `=B38*B20` | 108.04 |
| B42 | Positive replies (conversations) | `=B41*B21` | 37.82 |
| B43 | Meetings booked | `=B42*B22` | 18.91 |
| B44 | Meetings held | `=B43*B23` | 15.13 |
| B45 | Deals | `=B44*B24` | 3.03 |
| B46 | Cost per lead pulled | `=B40/B5` | 1.08 |
| B47 | Data cost per verified email | `=(B28+B29)/B30` | 0.0103 |
| B48 | Cost per mobile found | `=B32/B31` | 0.25 |
| B49 | Cost per conversation | `=B40/B42` | 128.41 |
| B50 | Cost per meeting booked | `=B40/B43` | 256.82 |
| B51 | Cost per meeting held | `=B40/B44` | 321.03 |
| B52 | Cost per deal (CAC) | `=B40/B45` | 1,605.15 |
| B53 | Gross margin per deal per month | `=B25/12*B26` | 700.00 |
| B54 | CAC payback in months | `=B52/B53` | 2.29 |
| B55 | LTV to CAC | `=B53*B27/B52` | 10.47 |
| B56 | Break-even reply rate at a 12 month payback | `=B40/(B38*B21*B22*B23*B24*B53*12)` | 0.0066 |

Notes:

- B29 assumes every pulled lead has an email (`hasEmail: true` on the Lead Database). For Maps or Store Leads, multiply by the share of rows with an email.
- B34 assumes unused plan credits do not carry over; check the live pricing page.
- B38 caps contacts at mailbox capacity. If B30 is larger than B37, the extra valid emails wait for next month and need re-validation after 30 days.
- B49 counts only positive email replies. Add phone conversations from `references/break-even-and-sensitivity.md` section 6 when the program calls.

## 4. CSV to paste

```csv
Label,Value
"ScraperCity plan fee per month (Starter 49, Growth 149, Scale 649)",149
"Plan credits per month (Starter 49, Growth 159, Scale 800)",159
"Bonus on purchased credits (Starter 0, Growth 0.10, Scale 0.30)",0.1
Leads pulled this month,4500
"Catalog price per lead (Lead Database on Growth 0, Apollo 0.0039, Maps 0.0099)",0
Share of pulled emails that validate as valid,0.7
Inputs sent to find_mobiles,300
Mobile Finder hit rate,0.4
Sending domains,5
Mailboxes per domain,3
Cold sends per mailbox per day,30
Business days per month,21
Touches per contact,3
Mailbox seat price per month (user input),7
Domain price per year (user input),12
Sequencer subscription per month (user input),97
Other tools per month (user input),0
People cost per month allocated to this program (user input),4500
Reply rate,0.0343
Positive share of replies,0.35
Meetings booked per positive reply,0.5
Held share of booked meetings,0.8
Close rate of held meetings,0.2
Annual contract value,12000
Gross margin,0.7
Customer lifetime in months,24
Lead cost at catalog price,=B5*B6
validate_emails cost,=B5*0.0072
Valid emails,=B5*B7
Mobiles found,=B8*B9
find_mobiles cost,=B31*0.25
Catalog-price spend,=B28+B29+B32
ScraperCity cash,"=B2+MAX(0,B33-B3)/(1+B4)"
Mailboxes,=B10*B11
Sends per month,=B35*B12*B13
New contacts per month at capacity,=B36/B14
Contacts emailed,"=MIN(B30,B37)"
"Inbox, domain and tool cost",=B35*B15+B10*B16/12+B17+B18
Total monthly program cost,=B34+B39+B19
Replies,=B38*B20
Positive replies (conversations),=B41*B21
Meetings booked,=B42*B22
Meetings held,=B43*B23
Deals,=B44*B24
Cost per lead pulled,=B40/B5
Data cost per verified email,=(B28+B29)/B30
Cost per mobile found,=B32/B31
Cost per conversation,=B40/B42
Cost per meeting booked,=B40/B43
Cost per meeting held,=B40/B44
Cost per deal (CAC),=B40/B45
Gross margin per deal per month,=B25/12*B26
CAC payback in months,=B52/B53
LTV to CAC,=B53*B27/B52
Break-even reply rate at a 12 month payback,=B40/(B38*B21*B22*B23*B24*B53*12)
```

## 5. Python reference implementation

Standard library only. Edit `INPUTS` and run with `python3 model.py`.

```python
#!/usr/bin/env python3
"""Outbound unit economics, same formulas as the spreadsheet block. Edit INPUTS, run, compare."""

INPUTS = {
    "plan_fee": 149, "plan_credits": 159, "credit_bonus": 0.10,
    "leads_pulled": 4500, "price_per_lead": 0.0, "valid_rate": 0.70,
    "mobile_inputs": 300, "mobile_hit": 0.40,
    "domains": 5, "mb_per_domain": 3, "sends_day": 30, "biz_days": 21, "touches": 3,
    "mailbox_price": 7, "domain_year": 12, "sequencer": 97, "other_tools": 0, "people": 4500,
    "reply_rate": 0.0343, "positive_share": 0.35, "meeting_rate": 0.50, "held_rate": 0.80, "close_rate": 0.20,
    "acv": 12000, "gm": 0.70, "life": 24,
}
VALIDATE, MOBILE = 0.0072, 0.25  # catalog prices: validate_emails per email, find_mobiles per number found


def run(i):
    o = {}
    o["lead_cost"] = i["leads_pulled"] * i["price_per_lead"]
    o["validate_cost"] = i["leads_pulled"] * VALIDATE
    o["valid_emails"] = i["leads_pulled"] * i["valid_rate"]
    o["mobiles_found"] = i["mobile_inputs"] * i["mobile_hit"]
    o["mobile_cost"] = o["mobiles_found"] * MOBILE
    o["list_spend"] = o["lead_cost"] + o["validate_cost"] + o["mobile_cost"]
    o["sc_cash"] = i["plan_fee"] + max(0, o["list_spend"] - i["plan_credits"]) / (1 + i["credit_bonus"])
    o["mailboxes"] = i["domains"] * i["mb_per_domain"]
    o["sends"] = o["mailboxes"] * i["sends_day"] * i["biz_days"]
    o["capacity"] = o["sends"] / i["touches"]
    o["contacted"] = min(o["valid_emails"], o["capacity"])
    o["infra"] = o["mailboxes"] * i["mailbox_price"] + i["domains"] * i["domain_year"] / 12 + i["sequencer"] + i["other_tools"]
    o["total"] = o["sc_cash"] + o["infra"] + i["people"]
    o["replies"] = o["contacted"] * i["reply_rate"]
    o["positives"] = o["replies"] * i["positive_share"]
    o["meetings"] = o["positives"] * i["meeting_rate"]
    o["held"] = o["meetings"] * i["held_rate"]
    o["deals"] = o["held"] * i["close_rate"]
    o["cost_per_lead"] = o["total"] / i["leads_pulled"]
    o["data_cost_per_verified_email"] = (o["lead_cost"] + o["validate_cost"]) / o["valid_emails"]
    o["cost_per_mobile"] = o["mobile_cost"] / o["mobiles_found"] if o["mobiles_found"] else 0.0
    o["cost_per_conversation"] = o["total"] / o["positives"]
    o["cost_per_meeting"] = o["total"] / o["meetings"]
    o["cost_per_held"] = o["total"] / o["held"]
    o["cac"] = o["total"] / o["deals"]
    o["gm_month"] = i["acv"] / 12 * i["gm"]
    o["payback_months"] = o["cac"] / o["gm_month"]
    o["ltv_to_cac"] = o["gm_month"] * i["life"] / o["cac"]
    o["breakeven_reply_12m"] = o["total"] / (
        o["contacted"] * i["positive_share"] * i["meeting_rate"] * i["held_rate"] * i["close_rate"] * o["gm_month"] * 12)
    return o


if __name__ == "__main__":
    for k, v in run(INPUTS).items():
        print(f"{k:30s} {v:12,.4f}")
```

Expected output for the defaults (rounded): total 4,856.00; meetings 18.91; deals 3.03; cost per conversation 128.41; cost per meeting 256.82; cost per held meeting 321.03; CAC 1,605.15; payback 2.29 months; LTV to CAC 10.47; break-even reply rate 0.66%.

## Sources

- https://scrapercity.com/pricing
- https://www.forentrepreneurs.com/saas-metrics-2/
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email-2025
