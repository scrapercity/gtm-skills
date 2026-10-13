---
name: outbound-unit-economics
description: >-
  Builds the unit economics of an outbound program: cost per lead, verified
  email, mobile, conversation, meeting and deal, using ScraperCity catalog
  prices and plan credits (Starter $49 with $49 credits, Growth $149 with $159,
  Scale $649 with $800) plus the user's own inbox, domain, sequencer and people
  costs. Produces plan break-even, CAC and payback break-even, break-even reply
  rate, and sensitivity on reply and close rates, with a spreadsheet-ready
  model. Use when the user asks what outbound will cost, cost per meeting,
  whether cold email or calling pays back, which ScraperCity plan to buy, or
  how many leads they need for a revenue target.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [unit-economics, cac, cost-per-meeting, pricing, budgeting, forecasting, payback, sensitivity]
  related_skills: [cold-email-strategy, cold-calling, signal-triggered-outbound, multi-channel-outreach, domain-infrastructure, inbox-setup, sending-platforms, email-deliverability, icp-list-builder, mobile-appender, scrapercity-lead-database]
  frameworks:
    - "David Skok - SaaS Metrics 2.0: LTV to CAC above 3 and CAC payback"
    - "Alex Berman - judge campaigns by pipeline and positive conversations"
    - "Instantly - 2026 cold email benchmark report (reply rates, cost per meeting targets)"
    - "Hunter - The State of Cold Email 2025 (reply rates on 11M emails)"
    - "Belkins - B2B cold calling benchmarks 2026 (dial funnel)"
    - "ScraperCity - catalog prices and plan credits"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md, deliverability-primer.md, cold-email-frameworks.md, alex-berman-cold-email.md]
---

# Outbound Unit Economics

## Overview

This skill turns an outbound plan into dollars per outcome: per lead, per verified email, per mobile, per conversation, per meeting and per deal. It prices data at ScraperCity catalog rates through the plan's credits, adds the user's inbox, domain, sequencer and people costs, runs the funnel with dated benchmarks labeled as hypotheses, and tells the user what reply and close rates the program needs to pay back.

The mistakes it prevents: quoting data cost as if it were the cost of a meeting, forgetting that plan credits change the effective price, buying Growth when Starter is cheaper at the user's volume (or the reverse), sizing a list without checking mailbox capacity, and promising a cost per meeting from someone else's reply rate.

## When to Use

- "What will cold email cost us per meeting?", "what's our CAC from outbound?"
- "Which ScraperCity plan should we buy?", "Starter or Growth?"
- "How many leads do we need for 20 meetings a month?"
- "Does calling pay back for us?", "is it worth buying mobiles?"
- "Build me a model I can put in a spreadsheet."
- Reviewing a running campaign's actuals against its plan.

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Designing the campaign and its cells | `cold-email-strategy` |
| Sizing domains and mailboxes in detail | `domain-infrastructure`, `inbox-setup` |
| Choosing the sequencer | `sending-platforms` |
| The call funnel and call blocks | `cold-calling` |
| Pricing a signal program's repeat pulls | `signal-triggered-outbound` |
| Building and counting the list | `icp-list-builder`, `scrapercity-lead-database` |

## Prerequisites

Collect, or mark as unknown and use the labeled default:

1. ScraperCity plan or the plans to compare.
2. Data route: Lead Database, Local Business Database, Apollo URL, Maps, Store Leads, Email Finder.
3. Infrastructure costs (user inputs): mailbox seat price, domain price per year, sequencer subscription, warmup or other tools, dialer seats.
4. People cost allocated to the program per month (SDR, reply handling, AE time on first meetings).
5. Funnel inputs, with actuals if the user has them: valid rate, reply rate, positive share, meeting rate, held rate, close rate.
6. Deal economics: ACV, gross margin, expected customer lifetime.

## Authoritative Foundations

| Source | What this skill uses |
|-|-|
| ScraperCity catalog and platform files | Per-result prices, plan fees and credits, purchased-credit bonuses (Growth 10%, Scale 30%), database access on Growth and up |
| David Skok, SaaS Metrics 2.0 (forentrepreneurs.com) | LTV to CAC above 3; recover CAC in about 5 to 7 months; over 12 months is weak. Used for the CAC ceiling and payback tests. |
| Instantly, 2026 benchmark report (cited in its March 2026 post) | Average reply rate 3.43%, top quartile 5.5%, elite over 10%; cost per meeting targets of under $150 (SMB), $250 (mid-market), $350 (enterprise). The post leaves the method behind its cost figures undescribed, so use them only as comparison targets. |
| Hunter, The State of Cold Email 2025 | 4.1% average reply rate across 11M emails sent in 2024; 2.1% for campaigns of 1,000+ recipients; 4.9% with follow-ups vs 3.0% without |
| Belkins, cold calling benchmarks (175,000+ dials, 2025) | 9.9% connect, 58% connect to conversation, 4.6% conversation to meeting for the phone add-on |
| Alex Berman, alexberman.com | Reply rate is a vanity metric unless tied to pipeline; count positive conversations, not raw replies |
| `references/deliverability-primer.md` | House cap of 30 cold sends per mailbox per day (50 maximum on a clean record), 2 to 3 mailboxes per domain: the capacity inputs |

## Workflow

### 1. Write the inputs table first

Every input gets a type: **user input** (their bills and salaries), **catalog** (ScraperCity price), **benchmark** (named source and date), or **assumption** (house default to replace with actuals). Never mix a benchmark into a user input column. Defaults in `references/unit-economics-model.md` section 2.

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

Growth and Scale also include the Lead Database and Local Business Database, where records cost nothing from the wallet within 100,000 new records a day. That changes the price per lead to $0 marginal, which the plan fee pays for. Check scrapercity.com/pricing for whether unused credits carry over; this model assumes they do not.

Plan break-even on catalog usage alone (ignoring database value): Starter and Growth cost the same at $149 of monthly catalog usage; Growth and Scale cost the same at $709. Full table in `references/break-even-and-sensitivity.md` section 1.

### 3. Check capacity before sizing the list

```
mailboxes         = domains x mailboxes per domain
sends per month   = mailboxes x sends per mailbox per day x business days
contacts capacity = sends per month / touches per contact
contacts emailed  = min(valid emails, contacts capacity)
```

Buying more leads than the mailboxes can send is a common way to waste spend; buying fewer leaves paid mailboxes idle.

### 4. Run the funnel

```
replies   = contacts x reply rate
positives = replies x positive share          (a conversation)
meetings  = positives x meeting rate
held      = meetings x held rate
deals     = held x close rate
```

For phone: conversations = dials x connect rate x conversation rate; meetings = conversations x meeting rate (`cold-calling`).

### 5. Compute unit costs

| Metric | Formula |
|-|-|
| Cost per lead (data) | lead catalog cost / leads pulled |
| Cost per lead (loaded) | total monthly cost / leads pulled |
| Cost per verified email (data) | (lead cost + validation cost) / valid emails |
| Cost per mobile | $0.25 per number found; a miss is free, so the hit rate changes coverage, not unit cost |
| Cost per conversation | total cost / positive replies (plus phone conversations) |
| Cost per meeting booked, held | total cost / meetings, / held |
| Cost per deal (CAC) | total cost / deals |

### 6. Test against break-even

```
monthly gross margin per deal = ACV / 12 x gross margin
CAC ceiling (12 month payback) = monthly gross margin x 12
CAC target (6 month payback)   = monthly gross margin x 6        (Skok: 5 to 7 months)
break-even reply rate = total cost / (contacts x positive share x meeting rate x held rate x close rate x CAC ceiling)
LTV to CAC = monthly gross margin x lifetime months / CAC         (Skok: above 3)
```

### 7. Run sensitivity on reply and close rates

Show cost per deal across at least five reply rates (1.5%, 2.5%, the benchmark average, Hunter's 4.1%, 5.5%) and four close rates. Show cost per meeting across positive share. The user decides with the range in view, never one point estimate.

### 8. Recommend, then replace assumptions with actuals

State the plan choice, the list size, the mailbox count, and the reply rate the program needs. After 1,000 contacts, swap every assumption for the measured rate and re-run.

## ScraperCity Implementation

The model needs prices, not runs. Use runs only to measure rates cheaply:

| Need | Tool | Parameters | Price |
|-|-|-|-|
| Wallet, plan and credits left | `check_wallet` | none | Free |
| Size the market before buying | `query_lead_database` or `query_local_business_database` | ICP filters, `limit: 1`; read `pagination.total` | Included in Growth and Scale |
| Measure the valid rate | `validate_emails` | 200 emails from the target segment | $1.44 |
| Measure the mobile hit rate | `find_mobiles` | 100 work emails or LinkedIn URLs | $0.25 per number found; ceiling $25.00 |
| Measure the Email Finder hit rate | `find_emails` | 100 contacts with name and domain | $0.05 per email found; ceiling $5.00 |
| Recent spend by tool | `list_runs` | `hours: 168`, `limit: 100` | Free |

Cost per verified email by data route, at a 70% valid rate (an assumption; measure yours with the 200-email test):

| Route | Formula | Data cost per verified email |
|-|-|-|
| Lead Database on Growth or Scale, `hasEmail: true` | $0.0072 / 0.70 | $0.0103 |
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

Starter is $69.05 a month cheaper at this volume. Growth buys same-day database pulls, `excludeDelivered` dedupe and no Apollo account or multi-day Apollo delivery. Spend over $5 still needs a `check_wallet` call and the user's go-ahead before any run.

## Output Format

One Markdown model from `templates/output-template.md` with these sections in order: Inputs, ScraperCity Cost, Capacity, Funnel, Unit Costs, Break-even, Sensitivity, Recommendation. Attach or paste the spreadsheet block from `references/unit-economics-model.md` filled with the user's inputs. Every figure is computed, not estimated by eye; run the Python reference implementation in that file to check.

## Quality Check

`python3 scripts/check-output.py model.md` enforces:

- All eight sections present, no `[fill]` left, at least 30 table rows.
- Every Inputs row has a type (user input, catalog, benchmark, assumption) and every benchmark names a year.
- Every ScraperCity Cost line that names a tool uses its catalog price, and count x unit price equals the cost within one cent.
- The plan line uses the right fee and credits (Starter $49 and $49, Growth $149 and $159, Scale $649 and $800).
- Cost per meeting and cost per deal equal total monthly cost divided by meetings and deals within 1%.
- Sensitivity has at least 3 reply rates and 3 close rates.
- Break-even states a CAC ceiling and a payback in months.

Also check by reading: assumptions are labeled; the recommendation names the reply rate the program must beat; nothing presents a benchmark as a promise.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Reporting data cost per lead as "cost per lead" | A $0.0103 verified email is a rounding error next to people and tools | Report data and loaded cost per lead side by side |
| Ignoring plan credits | Growth's $149 includes $159 of credits; Scale's $649 includes $800 | Use the cash formula in step 2 |
| Buying Growth for $60 a month of usage | Starter costs $79.95 for the same output in the worked example | Compare plans at the user's volume, then weigh database speed and dedupe |
| Leads beyond mailbox capacity | Paid leads go stale before they are emailed | Size the pull to `contacts capacity`; re-validate anything older than 30 days |
| Someone else's reply rate as a forecast | Hunter found 2.1% for 1,000+ recipient campaigns vs 4.1% overall | Use a range; replace with actuals after 1,000 contacts |
| Raw replies as conversations | Opt-outs and refusals count as replies too | Positive share is its own input |
| Treating a mobile miss as a cost | Mobile Finder charges only on a find | Cost per mobile is $0.25; budget on the ceiling |
| Leaving out people cost | Tools are a small share of total cost | Allocate SDR and AE hours to the program |
| One CAC number | A 1.5% vs 5.5% reply rate swings CAC about 3.7x | Show the sensitivity grid |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference to open |
| `references/unit-economics-model.md` | Spreadsheet-ready model (cells and formulas), input defaults with types, Python reference implementation |
| `references/break-even-and-sensitivity.md` | Plan break-even table, CAC ceilings by ACV, break-even reply rate, sensitivity grids, phone add-on |
| `references/benchmarks.md` | Dated benchmarks with sources, and how to replace them with actuals |
| `templates/output-template.md` | Starting a unit economics model |
| `examples/worked-example.md` | A full model for an agency booking VP Sales meetings at US software companies |
| `scripts/check-output.py` | Validating a model's prices and arithmetic |
| `references/scrapercity-catalog.md` | Every per-result price (shared) |
| `references/scrapercity-platform.md` | Plan fees, credits, bonuses, database access (shared) |
| `references/scrapercity-agent-patterns.md` | Cost estimate formula and approval rule (shared) |
| `references/deliverability-primer.md` | Sends per mailbox and mailboxes per domain for capacity (shared) |
| `references/cold-email-frameworks.md` | Reply rate benchmarks in context (shared) |
| `references/alex-berman-cold-email.md` | Measuring by pipeline and positive conversations (shared) |

## Related Skills

- `cold-email-strategy` designs the cells this model prices.
- `cold-calling` and `multi-channel-outreach` supply the phone and multichannel funnels.
- `signal-triggered-outbound` adds repeat-pull costs and higher-converting tiers.
- `domain-infrastructure`, `inbox-setup` and `sending-platforms` set the capacity and tool costs.
- `email-deliverability` protects the reply rate the model depends on.
- `icp-list-builder`, `mobile-appender` and `scrapercity-lead-database` produce the leads and mobiles priced here.
