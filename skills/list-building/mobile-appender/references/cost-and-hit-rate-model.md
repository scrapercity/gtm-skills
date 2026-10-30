# Cost and Hit-Rate Model

Mobile Finder bills $0.25 per number found and nothing when no number is found (`references/scrapercity-catalog.md`). Cost depends on one unknown, the hit rate, so the skill measures it before committing the budget.

## 1. Formulas

```text
pilot_cost        = pilot_hits x $0.25                       (max 50 x $0.25 = $12.50)
hit_rate          = pilot_hits / pilot_inputs
expected_found    = round(remaining_inputs x hit_rate)
expected_cost     = expected_found x $0.25
ceiling           = remaining_inputs x $0.25
dial_ready        = found x survival_rate                    (after shared-number, line-type and suppression checks)
cost_per_dialable = total_cost / dial_ready
```

`survival_rate` is the share of found numbers that pass the E.164, shared-number, line-type and suppression checks. There is no published figure for it; measure it on the pilot's found numbers and update it after each batch.

## 2. Pilot design

| Choice | Rule |
|-|-|
| Size | 50 inputs. Small enough to cap the spend at $12.50, large enough to separate a 20% list from a 50% list |
| Sampling | Random across the list, not the first 50 rows (exports are often sorted by company or date) |
| Strata | If the list mixes very different groups (for example US and EMEA, or C-level and managers), pilot 25 from each and plan each group separately |
| Inputs | Same input type you will use at scale (URL if most rows have URLs) |
| Reuse | Pilot rows are part of the final list; do not rerun them |

Precision: with 50 inputs, the standard error of a hit rate near 50% is about 7 percentage points, so the plausible range is roughly plus or minus 14 points. Use low and high scenarios at least that wide.

## 3. Scenario table

Always show four rows: low, expected (the pilot rate), high, ceiling. Example for 276 remaining inputs after a 36% pilot:

| Scenario | Inputs | Hit rate | Numbers found | Cost |
|-|-:|-:|-:|-:|
| Low | 276 | 20% | 55 | $13.75 |
| Expected | 276 | 36% | 99 | $24.75 |
| High | 276 | 50% | 138 | $34.50 |
| Ceiling | 276 | 100% | 276 | $69.00 |

The approval request names the ceiling, because the wallet must cover the case where every lookup hits.

## 3a. Second pass on URL misses

When rows carry both a LinkedIn URL and a work email:

```text
pass2_inputs    = url_misses that have a work email
pass2_expected  = pass2_inputs x email_hit_rate x $0.25
pass2_ceiling   = pass2_inputs x $0.25
```

Measure `email_hit_rate` on the first 50 pass-2 inputs the same way as the pilot. Report pass 2 as its own scenario rows so the approval covers both ceilings.

## 4. Planning table by list size

Expected cost at a given hit rate, before shared-number, line-type and suppression losses:

| Inputs | 20% | 30% | 40% | 50% | Ceiling |
|-:|-:|-:|-:|-:|-:|
| 100 | $5.00 | $7.50 | $10.00 | $12.50 | $25.00 |
| 300 | $15.00 | $22.50 | $30.00 | $37.50 | $75.00 |
| 500 | $25.00 | $37.50 | $50.00 | $62.50 | $125.00 |
| 1,000 | $50.00 | $75.00 | $100.00 | $125.00 | $250.00 |
| 5,000 | $250.00 | $375.00 | $500.00 | $625.00 | $1,250.00 |

## 5. Cost controls

1. One input per person per run (URL preferred). Sending both identifiers for one person in the same run can bill two hits. A second run with the work email for the URL misses is safe: those people have no number yet, and a miss costs nothing.
2. Remove people who already have a mobile on file and people on the suppression list before the pilot.
3. Append only for the accounts reps will call in this campaign. Every hit bills $0.25 whether or not anyone dials it.
4. When the list runs in batches, check each batch's hit rate against the pilot's low scenario; if a batch falls below it, stop and look at the inputs (old exports, wrong country, many company pages).
5. Keep the found file and the hold file, and skip people already appended on the next run unless their number failed.

## 6. Where the cost goes after the append

| Line | Who bills it | Notes |
|-|-|-|
| Mobile Finder | ScraperCity wallet | $0.25 per number found |
| Email validation for the multi-channel file | ScraperCity wallet | $0.00169 per email, optional |
| Line-type lookup | The user's carrier lookup provider | Per lookup; only when the call plan needs true mobiles |

Report only the ScraperCity lines in the cost total and list the others as "billed separately".

## 7. Comparing channels before you buy

A quick check of whether mobiles pay off for a segment:

```text
value per dial-ready mobile = connect rate x meeting rate per connect x value of a meeting
buy mobiles when value per dial-ready mobile > cost_per_dialable
```

Example: if a team's own data shows 1 in 8 mobile dials connects and 1 in 6 connects books a meeting valued at $400 in pipeline, value per dial-ready mobile is 0.125 x (1/6) x $400 = about $8.33 for one dial; at $0.29 per dial-ready mobile the purchase clears the bar easily. These rates are placeholders; use the team's dialer reports.

## Sources

- ScraperCity tool catalog (Mobile Finder price): references/scrapercity-catalog.md
- ScraperCity, pricing: https://scrapercity.com/pricing
- NIST/SEMATECH e-Handbook, confidence limits for a proportion: https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
