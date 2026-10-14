---
name: outbound-unit-economics
description: >-
  Builds the unit economics of an outbound program: cost per lead, verified
  email, mobile, conversation, meeting, opportunity and deal, using ScraperCity
  catalog prices and plan credits (Starter $49 with $49 credits, Growth $149
  with $159, Scale $649 with $800), a dated tool stack, a loaded SDR cost and
  AE time per meeting. Produces CAC, payback, program cash break-even, the
  break-even reply rate, the most a meeting can cost, sensitivity grids and a
  reverse sizing of leads and mailboxes, with a spreadsheet, a runnable model
  and a checker that recomputes every number. Use when the user asks what
  outbound will cost, cost per meeting or opportunity, what an SDR costs,
  whether cold email or calling pays back, which ScraperCity plan to buy, how
  many leads they need for a meeting target, or why actuals miss the plan.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "2.0.0"
  author: ScraperCity
  category: outbound
  tags:
    - unit-economics
    - cac
    - cost-per-meeting
    - cost-per-opportunity
    - sdr-cost
    - tool-stack
    - payback
    - sensitivity
    - forecasting
  related_skills:
    - cold-email-strategy
    - cold-calling
    - signal-triggered-outbound
    - multi-channel-outreach
    - domain-infrastructure
    - inbox-setup
    - sending-platforms
    - email-deliverability
    - reply-handling
    - icp-list-builder
    - mobile-appender
    - scrapercity-lead-database
  frameworks:
    - "David Skok - SaaS Metrics 2.0: LTV to CAC above 3 and CAC payback"
    - "The Bridge Group - 2025 SDR Models and Metrics report (OTE, ramp, tenure, quotas)"
    - "U.S. Bureau of Labor Statistics - Employer Costs for Employee Compensation, June 2026"
    - "Benchmarkit - 2025 B2B SaaS Performance Metrics (New CAC ratio)"
    - "Instantly - 2026 cold email benchmark report (reply rates, cost per meeting targets)"
    - "Instantly - cold outbound cost per meeting calculator (November 2025)"
    - "Ryan Reisert - Buckets (GTMnow, November 2021): meeting confirmations and no-shows"
    - "Ronen Pessar - qualify with a present-tense closed question"
    - "Hunter - The State of Email Outreach 2026 (31M emails sent in 2025)"
    - "Alex Berman - judge campaigns by pipeline and positive conversations"
    - "ScraperCity - catalog prices and plan credits"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
    - deliverability-primer.md
    - cold-email-frameworks.md
    - alex-berman-cold-email.md
---

# Outbound Unit Economics

## Overview

This skill turns an outbound plan into dollars per outcome: per lead, verified email, mobile, conversation, meeting booked and held, opportunity and deal. It prices data at ScraperCity catalog rates through the plan's credits, adds a dated tool stack, a loaded SDR cost built from published medians and the AE hours each meeting consumes, then runs the funnel with labeled benchmarks and tells the user what reply rate, win rate and cash the program needs.

The mistakes it prevents:

- Quoting data cost as the cost of a meeting. In the worked example data and tools are 4.8% of program cost; people are the rest.
- Pricing an SDR at salary. A $55K base SDR costs about $10,900 a month loaded once variable pay, employer cost, a manager share and ramp are in.
- Leaving AE time out of CAC, which hides a cost floor that no reply rate removes.
- Treating a 5-month CAC payback as a program that pays back in 5 months. Monthly cohorts keep the program cash negative far longer.
- Buying leads the mailboxes cannot send, or a sequencer tier that caps sends below mailbox capacity.
- Promising a cost per meeting from someone else's reply rate.

## When to Use

- "What will cold email cost us per meeting?", "what's our CAC from outbound?", "cost per opportunity?"
- "What does an SDR really cost?", "is a half-time SDR enough?"
- "Which ScraperCity plan should we buy?", "Starter or Growth?"
- "How many leads and mailboxes do we need for 20 meetings a month?"
- "Does calling pay back for us?", "should we buy mobiles?"
- "How long until outbound pays for itself?", "how much cash do we need?"
- "Our actuals are below plan; where is the problem?"
- "Build me a model I can put in a spreadsheet."

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Designing the campaign and its cells | `cold-email-strategy` |
| Sizing domains and mailboxes in detail | `domain-infrastructure`, `inbox-setup` |
| Choosing the sequencer | `sending-platforms` |
| The call funnel and call blocks | `cold-calling` |
| Pricing a signal program's repeat pulls | `signal-triggered-outbound` |
| Building and counting the list | `icp-list-builder`, `scrapercity-lead-database` |
| Lifting positive share and meeting rate | `reply-handling` |

## Prerequisites

Collect, or mark unknown and use the labeled default from `references/unit-economics-model.md` section 2:

1. Goal: meetings, opportunities or deals a month, and the decision the model must settle.
2. ScraperCity plan or plans to compare, and the data route (Lead Database, Local Business Database, Apollo URL, Maps, Store Leads, Email Finder).
3. Tool bills: mailbox seat, domain per year, sequencer tier, Sales Navigator, dialer, CRM seat share.
4. People: SDR share of time and pay, who takes first meetings and their pay, hours per held meeting and per opportunity.
5. Funnel actuals if any: valid, reply, positive share, meeting, held, opportunity and win rates.
6. Deal economics: ACV, gross margin, lifetime or monthly churn, billing (monthly or annual prepay), sales cycle.
7. Who on the team can own each action (founder, SDR, AE), so every recommendation gets an owner and a date.

When the user gives a total (for example "$7,000 a month for the SDR, tools and data") without the split, keep the total as the user input. Any split is an assumption, and no headline may rest on it: write the decision as a branch on the number they can look up ("if the SDR line is above $X loaded, cut hours; if below, keep the seat and add volume"), with both outcomes' CAC.
## Authoritative Foundations

| Source | What this skill uses |
|-|-|
| ScraperCity catalog and platform files | Per-result prices, plan fees and credits, purchased-credit bonuses (Growth 10%, Scale 30%), database access on Growth and up |
| David Skok, SaaS Metrics 2.0 | LTV to CAC above 3; the best recover CAC in 5 to 7 months; past 12 months is weak. Sets the 6 month target and 12 month ceiling. |
| The Bridge Group, 2025 SDR report (351 companies, 6 Feb 2025) | $80K median SDR OTE split 68:32; 3.0 month ramp; 1.9 year tenure; 40% attrition; manager OTE $146K over 6.4 SDRs; quotas counted in held meetings (median 10 a month) and converted opportunities (median 6) |
| BLS Employer Costs for Employee Compensation, June 2026 | Sales and related: insurance $2.16, retirement $0.85 and payroll taxes $2.69 an hour on $30.15 of pay (wages $26.99, paid leave $2.11, supplemental $1.05) = 18.9%, used as 19% on top of an annual salary. Benefits over wages alone is 32.8%, but that counts paid leave, which a salary already pays; show this derivation in the Inputs row |
| Benchmarkit, 2025 B2B SaaS Performance Metrics | Median New CAC ratio $2.00 of S&M per $1.00 of new ARR (2024 data): the market line to compare the program against |
| Instantly, Email Sequence Benchmarks 2026 (30 Mar 2026) and cost per meeting calculator (13 Nov 2025) | Reply rate 3.43% average, 5.5% top quartile; cost per meeting under $150, $250 and $350 by ACV segment (software, data and rep time); the calculator post calls $50 to $100 strong for B2B outbound. Quote the one you use with its post and date |
| Ryan Reisert, Buckets (GTMnow, Nov 2021) | Confirm each booked meeting by phone about a week out, by email 12 to 24 hours before, by phone 2 to 3 hours before if the email got no reply; a no-show goes back to the Priority bucket for a new time |
| Ronen Pessar (The Sales Doctor ep. 43; Triple Session) | Qualify with a present-tense closed question and confirm the right person before booking |
| Hunter, State of Email Outreach 2026 | 4.5% average reply per sequence on 31M emails sent in 2025; 2.4% for sequences over 500 recipients |
| Alex Berman, alexberman.com | Reply rate means little unless tied to pipeline; count positive conversations, opportunities and pipeline |
| Instantly help center (checked 2026-10-13); Alex Berman, alexberman.com | Instantly recommends 30 campaign emails per account per day and at least 2 weeks of warmup before campaigns; Berman's setup uses 2 to 3 inboxes per domain. These set the capacity and warmup inputs |

## Workflow

### 1. Write the inputs table first

Every input gets a type: **user input** (their bills and salaries), **catalog** (ScraperCity price), **benchmark** (named source and year), **assumption** (a planning number the user replaces with a measured rate) or **measured** (their own data with a date range). Never put a benchmark in a user input row. A benchmark row names the report and its date; when the figure is computed from the source (a ratio of two medians, the 19% employer cost), the row shows that arithmetic so a reader can check it against the page. A figure built from several medians (a loaded SDR) is labeled as built, never as a reported number.

### 2. Price the data through the plan

```
catalog spend    = sum of (billable results x catalog price)
ScraperCity cash = plan fee + max(0, catalog spend - plan credits) / (1 + purchased-credit bonus)
```

| Plan | Fee | Credits | Bonus on purchased credits | Cash per $1 of catalog usage when credits are fully used |
|-|-|-|-|-|
| Starter | $49 | $49 | 0% | $1.00 |
| Growth | $149 | $159 | 10% | $0.94 inside credits, $0.91 for purchased |
| Scale | $649 | $800 | 30% | $0.81 inside credits, $0.77 for purchased |

Growth and Scale include the Lead Database and Local Business Database, where records cost nothing from the wallet within 100,000 new records a day. Starter and Growth tie at $149 of monthly catalog usage; Growth and Scale at $709. This model assumes unused credits do not carry over; check scrapercity.com/pricing.

### 3. Build the cost stack

List every monthly line with its basis, so the model knows what moves with meetings:

```
fixed      ScraperCity cash, mailbox seats, domains / 12, sequencer, Sales Navigator, SDR share
amortized  warmup months of mailbox and sequencer fees + setup, spread over 12 months
variable   AE hours per held meeting and per opportunity x AE loaded hour
SDR loaded per productive FTE = ((base + variable x share paid) x 1.19 / 12 + manager OTE x 1.19 / 12 / SDRs per manager)
                                x tenure / (tenure - ramp / 2)
AE loaded hour = AE OTE x 1.19 / 2,080
```

Defaults and dated tool prices are in `references/cost-stack.md`. Allocate shared people by hours and shared seats by use.

### 4. Check capacity before sizing the list

```
mailboxes         = domains x mailboxes per domain
sends per month   = mailboxes x sends per mailbox per day x business days
contacts capacity = sends per month / touches per contact
contacts emailed  = min(valid emails, contacts capacity)
```

The sequencer tier caps both: Instantly Growth ($47) allows 5,000 emails and 1,000 uploaded contacts a month, Hypergrowth ($97) 125,000 and 25,000 (instantly.ai/pricing, checked 2026-10-13). So contacts emailed = min(valid emails, contacts capacity, tier contact cap, tier email cap / touches). Compare held meetings per SDR FTE with Bridge's median quota of 10.

When the user knows meetings booked but not contacts emailed, start from their counts. The top of the funnel is then a diagnostic with two branches (full capacity and an implied low reply rate, or a capped list and idle mailboxes), each with its implied reply rate and its fix, and the first measurement that picks the branch. Neither branch is the base case, and no headline rests on one. SDR utilization comes from the SDR's logged hours, never from a benchmark activity rate.

### 5. Run the funnel

```
replies = contacts x reply rate            positives = replies x positive share
meetings = positives x meeting rate        held = meetings x held rate
opportunities = held x opportunity rate    deals = opportunities x win rate
```

For phone: conversations = dials x connect rate x conversation rate; meetings = conversations x meeting rate (`cold-calling`).

### 6. Compute unit costs

| Metric | Formula |
|-|-|
| Total monthly program cost | fixed + amortized + AE cost per held meeting x held + AE cost per opportunity x opportunities |
| Cost per lead, data and loaded | lead catalog cost / leads; total / leads |
| Cost per verified email | (lead cost + validation cost) / valid emails |
| Cost per mobile | $0.25 per number found; a miss is free |
| Cost per conversation, meeting booked, meeting held, opportunity, deal (CAC) | total / that count |
| Cost per $1 of pipeline | total / (opportunities x ACV) |
| New CAC ratio | total / (deals x ACV); Benchmarkit's 2025 median is $2.00 |

### 7. Test against break-even

```
monthly gross margin per deal = ACV / 12 x gross margin
CAC target  = margin x 6     CAC ceiling = margin x 12     payback = CAC / margin
LTV to CAC  = margin x lifetime months / CAC        (lifetime = 1 / monthly churn when churn is known)
AE cost per deal (CAC floor) = AE per held / (opportunity rate x win rate) + AE per opportunity / win rate
highest cost per booked meeting = CAC limit x held rate x opportunity rate x win rate
break-even reply rate = fixed / (contacts x (k_deal x CAC limit - k_held x AE per held - k_opp x AE per opportunity))
   where k_held = positive share x meeting rate x held rate, k_opp = k_held x opportunity rate, k_deal = k_opp x win rate
```

Then run the cash curve (`references/unit-economics-model.md` section 6): month 0 warmup, deals sign after the sales cycle and pay monthly or a year up front. Report the break-even month and the lowest cumulative cash.

### 8. Run sensitivity

One grid: cost per deal across at least five reply rates (1.5%, 2.5%, the benchmark, Hunter's 4.5%, 5.5%) by four win rates, every cell with its own total, since AE time moves with meetings. One scenario table: one lever at a time against today, each row a full re-run (`unit-economics-model.py scenarios levers.json`) so total, meetings, deals, cost per meeting, CAC and payback agree. Name the stage that moves CAC most. No second grid.

### 9. Size to the goal and recommend

Reverse the funnel for the user's target: contacts = target meetings / (reply x positive share x meeting rate), leads = contacts / valid rate, mailboxes = contacts x touches / (sends per day x business days), domains rounded up. State the plan, list size, mailboxes, reply and win rates to beat, cash to fund and the first measurements. `scripts/unit-economics-model.py target N` does the arithmetic.

### 10. Write the fixes, with owners and copy

Each fix the recommendation names comes with a named source for the tactic, an owner who exists on the user's team, a calendar date and every message it involves written out in full. Stage fixes and their copy are in `references/break-even-and-sensitivity.md` section 12: Reisert's confirmation sequence and no-show rebooking for the held rate, a Pessar-style qualifying question before the calendar link for the opportunity rate, and an SDR quota counted in held meetings and converted opportunities as Bridge reports them. When deals a month are few, show deals a quarter and the quarterly CAC at one deal fewer and one more, so the user judges CAC on enough deals.

### 11. Replace assumptions with actuals

As each stage produces measured counts, swap its assumption for the measured rate, with the sample size and date range beside it, and re-run. When actuals miss plan, split the gap by stage (`unit-economics-model.py variance actual.json`) and fix the stage with the largest share first.

## ScraperCity Implementation

The model runs on catalog prices; use tool runs only to measure rates cheaply:

| Need | Tool | Parameters | Price |
|-|-|-|-|
| Wallet, plan and credits left | `check_wallet` | none | Free |
| Size the market before buying | `query_lead_database` or `query_local_business_database` | ICP filters, `limit: 1`; read `pagination.total` | Included in Growth and Scale |
| Measure the valid rate | `validate_emails` | 200 emails from the target segment | $1.44 |
| Measure the mobile hit rate | `find_mobiles` | 100 work emails or LinkedIn URLs | $0.25 per number found; ceiling $25.00 |
| Measure the Email Finder hit rate | `find_emails` | 100 contacts with name and domain | $0.05 per email found; ceiling $5.00 |
| Recent spend by tool | `list_runs` | `hours: 168`, `limit: 100` | Free |

Data cost per verified email by route, at a 70% valid rate (an assumption; measure yours with the 200-email test):

| Route | Formula | Data cost per verified email |
|-|-|-|
| Lead Database on Growth or Scale, email on file | $0.0072 / 0.70 | $0.0103 |
| Apollo URL (`scrape_apollo`) then validate | ($0.0039 + $0.0072) / 0.70 | $0.0159 |
| Google Maps (`scrape_maps`), 40% of businesses with an email (assumption), then validate | ($0.0099 / 0.40 + $0.0072) / 0.70 | $0.0456 |
| Website Finder (`scrape_website_finder`) per contact found, then validate | ($0.0499 + $0.0072) / 0.70 | $0.0816 |
| Email Finder (`find_emails`), validated at lookup | $0.05 per email found | $0.0500 |

### Worked cost estimate (data line only)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Lead Database pull, VP Sales at 50 to 200 employee US software companies, `hasEmail: true` | 4,500 | Included in Growth | $0.00 |
| `validate_emails` | 4,500 | $0.0072 | $32.40 |
| `find_mobiles` on 300 top accounts (assume 40% found) | 120 found | $0.25 | $30.00 |
| Catalog spend | | | $62.40 |
| Growth cash: $149 + max(0, $62.40 - $159) / 1.10 | | | $149.00 |
| Starter alternative: Apollo 4,500 x $0.0039 = $17.55 plus the same validation and mobiles | | | $79.95 |

Starter is $69.05 a month cheaper at this volume, 0.7% of the worked example's $10,363.14 program cost. Growth buys same-day database pulls, `excludeDelivered` dedupe and no multi-day Apollo delivery. Spend over $5 still needs a `check_wallet` call and the user's go-ahead before any run.

## Output Format

One Markdown model from `templates/output-template.md`: a one-line context, the answer, then Inputs, ScraperCity Cost, Cost Stack, Capacity, Funnel, Unit Costs, Break-even, Sensitivity, Recommendation and Sources, and no other sections. Show arithmetic in cells as `a x b = c`. Compute every figure with `scripts/unit-economics-model.py` (or the spreadsheet checked against it) and run the checker before sending.

- **Answer first.** After the context line, at most five sentences: the decision, CAC and payback, the levers that move them, each number once. Anything that rests on an assumption is an if/then with both numbers. One line then says which figures are the user's; a "nothing was run" note appears there once or not at all.
- **Each fact once.** No second Cost Stack table (the SDR and AE derivation is one line under it), one grid plus one scenario table, and no row that repeats a figure another section states. At most 2,000 words.
- **Only what was asked.** ScraperCity Cost carries the plan row, the catalog lines and the cash row. Plan comparisons, unused-credit ideas and route tables appear only when the user asked which plan to buy; otherwise one line ("data line at $149 on Growth; anything you pay above that is a direct cut"). No frameworks, scores or ratios the user cannot act on.
- **Plain words.** Write "a count of matching leads" and "validate 200 current emails" in place of tool ids, parameter names, code spans, file paths, skill or script names. Leave out handoff lines to other skills, disclaimers and self-graded checklists.
- **Recommendation table** columns: Decision, Value, Why, Owner, Due. It answers the question first, then names the reply rate and win rate to beat, the cash to fund and the first measurements. Owners are roles the user has; due dates are calendar dates.
- **Every message the plan names is written out** below the table as a quote block, ready to send: confirmation, reminder, no-show, qualifying question.
- **Sources** lists each external figure's source name, date and URL, one line each.
- When the user asks a narrow question (only "Starter or Growth?", only "what does an SDR cost?"), answer it in a few lines with the formula and number and offer the full model.

## Quality Check

`python3 scripts/check-output.py model.md` enforces:

- The nine sections in order plus Sources and nothing else, every `[fill]` replaced, 500 to 2,000 words, at least 30 table rows; legal content, dashes, file paths, code spans, tool ids and parameters, skill names, disclaimers and a repeated "nothing was run" note fail.
- Every Inputs row is typed and every benchmark names a year; benchmarks require a Sources section with URLs.
- ScraperCity lines use catalog prices by product name with count x price = cost; the plan row shows its fee and credits; the cash line equals fee + max(0, spend - credits) / (1 + bonus).
- One Cost Stack table whose rows are count x unit cost and sum to the total, carrying the ScraperCity cash; per-meeting and per-opportunity lines use the Funnel's counts.
- Each Funnel count equals the previous count times its rate; cost per meeting booked, held, opportunity and deal each equal total / count within 1%.
- Every `a x b = c` cell and Formula and Value pair computes, with at least 15 shown.
- Payback = CAC / monthly margin; the ceiling is 12 months of margin; the 12 month break-even reply rate is recomputed.
- Every cost per deal grid cell is recomputed; every scenario row has CAC = total / deals, cost per meeting = total / meetings and payback = CAC / margin.
- Any line sizing Instantly Growth states its 1,000 contact cap.
- The Recommendation has Owner and Due (a calendar date) on every row, names the reply rate to beat, and writes out as many messages as it names.

Also check by reading: no headline rests on an assumed split or volume; the cash curve and CAC payback are both stated when the user asks about payback; nothing presents a benchmark as a promise.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Reporting data cost per lead as "cost per lead" | A $0.0103 verified email is a rounding error next to people | Report data and loaded cost per lead side by side |
| SDR priced at base salary | $4,583 a month of base becomes about $10,900 loaded | Build pay, 19% employer cost, manager share and ramp |
| No AE time in CAC | First meetings and proposals cost $1,620.99 a deal in the worked example | Count AE hours per held meeting and per opportunity as variable cost |
| CAC payback read as program payback | 5.44 month payback, yet monthly billing breaks even in month 14 and needs $44K | Run the cash curve; offer annual prepay when cash is tight |
| Ignoring plan credits | Growth's $149 includes $159 of credits; Scale's $649 includes $800 | Use the cash formula in step 2 |
| Leads beyond mailbox capacity, or a sequencer tier below it | Paid leads go stale; Instantly Growth's 1,000 uploaded contacts caps 15 mailboxes (3,150 contacts) at 31.7% | Size the pull to contacts capacity and the tier to both sends and contacts |
| A headline built on an assumed split or volume | The user's $7,000 total says nothing about which line is idle | Branch the decision on the number they can look up, with both CACs |
| A fix named but not written | "Add a reminder" leaves the work undone | Write the message in full, with an owner and a date |
| Someone else's reply rate as a forecast | Hunter found 2.4% for 500+ recipient sequences vs 4.5% overall | Use a range; replace it with the measured rate as sends come in |
| Raw replies as conversations | Opt-outs and refusals count as replies too | Positive share is its own input |
| Fixing volume when rates are the problem | 3x volume lowers cost per meeting by 2.3% in the worked example | Fix the stage with the largest share of the gap first |
| Cost month matched to another month's deals | Mixing periods makes CAC meaningless | Price one month of sends against the outcomes of that cohort |
| Annualizing churn by multiplying by 12 | 2% a month is 21.5% a year | Use 1 - (1 - monthly churn)^12 |
| One blended model for several segments | A strong segment hides a losing one | Run the model per campaign cell |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/unit-economics-model.md` | Inputs with types, every spreadsheet cell and formula, the CSV to paste, the cash curve tab |
| `references/cost-stack.md` | SDR loaded cost build, AE time, dated tool prices and tier limits, fixed vs one-time vs variable, allocation of shared seats |
| `references/break-even-and-sensitivity.md` | Plan break-even, CAC limits by ACV, break-even reply rate, grids, scale, cash curve, reverse sizing, plan versus actual, phone add-on, stage fixes with sendable copy |
| `references/benchmarks.md` | Dated benchmarks with samples and limits, and how to replace them with actuals |
| `templates/output-template.md` | Starting a unit economics model |
| `examples/worked-example.md` | A full model for an illustrative agency booking VP Sales meetings at US software companies |
| `scripts/unit-economics-model.py` | Computing the model, grid, one-lever scenarios, plan comparison, cash curve, target sizing, scale and variance |
| `scripts/check-output.py` | Recomputing a finished model's prices and arithmetic |
| `references/scrapercity-catalog.md` | Every per-result price (shared) |
| `references/scrapercity-platform.md` | Plan fees, credits, bonuses, database access (shared) |
| `references/scrapercity-agent-patterns.md` | Cost estimate formula and approval rule (shared) |
| `references/deliverability-primer.md` | Sends per mailbox, mailboxes per domain and the warmup ramp (shared) |
| `references/cold-email-frameworks.md` | Reply rate benchmarks in context (shared) |
| `references/alex-berman-cold-email.md` | Measuring by pipeline and positive conversations (shared) |

## Related Skills

- `cold-email-strategy` designs the cells this model prices.
- `cold-calling` and `multi-channel-outreach` supply the phone and multichannel funnels.
- `signal-triggered-outbound` adds repeat-pull costs and higher-converting tiers.
- `domain-infrastructure`, `inbox-setup` and `sending-platforms` set the capacity and tool costs.
- `email-deliverability` protects the reply rate the model depends on.
- `reply-handling` lifts the positive share and meeting rate.
- `icp-list-builder`, `mobile-appender` and `scrapercity-lead-database` produce the leads and mobiles priced here.
