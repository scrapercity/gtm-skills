# Skip Trace Runbook

Pricing, piloting, batching, the Distress List feed, Property Lookup escalation and the output schema.

## 1. Price list (from `references/scrapercity-catalog.md`)

| Tool | Billable unit | Price | Notes |
|-|-|-|-|
| `find_people` | Result | $0.0199 | A search with 0 matches is billed as 1 result |
| `scrape_property_lookup` | Property | $0.15 | +$0.10 with `includeOwnerContact: true`, so $0.25 |
| `scrape_distress_list` | Property | $0.05 | `maxItems` 1 to 500 per run |
| `validate_emails` | Email | $0.0072 | Only if an email channel is planned |

## 2. Cost formulas

```text
find_people ceiling     = searches x max(max_results, 1) x $0.0199
find_people actual      = billed results x $0.0199          (from the run's row count; 0-match searches count 1)
property_lookup         = properties x ($0.15 + $0.10 if includeOwnerContact)
distress_list           = properties returned x $0.05
cost per callable owner = total cost / owners with at least one callable phone
```

### Price comparison per address

| Path | Cost per address | When it wins |
|-|-:|-|
| `find_people` by address, `max_results: 1` | $0.0199 | Owner name known; owner likely lives there |
| `find_people` by address, then name rescue at 3 for 25% of rows | about $0.0199 + 0.25 x $0.0597 = $0.0348 | Same, with some movers |
| `scrape_property_lookup` without owner contact | $0.15 | Valuation and property facts only |
| `scrape_property_lookup` with owner contact | $0.25 | Owner unknown, absentee or multi-unit; one call returns owner name, phone and email |

## 3. Pilot

| Step | Rule |
|-|-|
| Sample | 25 random rows per identifier class |
| Measure | Share of rows reaching probable or better; average billed results per search |
| Decide | If A1 rows reach probable or better on 70% or more, keep People Finder first; if under 40%, the input names or addresses are stale and Property Lookup with owner contact may be cheaper per usable owner |
| Cost | 25 x $0.0199 = $0.50 per People Finder class; 25 x $0.25 = $6.25 for a Property Lookup class |

The 70% and 40% cutoffs are house starting points (October 2026). Replace them with your own pilot history.

## 4. Distress List as the feed

```json
{"search": "Columbus, OH", "distressTypes": ["preForeclosure", "auction"], "maxItems": 150}
```

| Choice | Rule |
|-|-|
| `search` | City and state, or one ZIP. A metro larger than 500 properties runs as several ZIP searches |
| `distressTypes` | `preForeclosure` and `auction` for owner outreach. `foreclosure` for timing research. Skip `bankOwned` for owners: the lender owns it |
| `maxItems` | 1 to 500 |
| Next step | Rows carry the property address and distress type. The tool description says to pair it with People Finder to reach the owner. With no owner name in hand, run Property Lookup with owner contact, or People Finder capped at the probable band |

## 5. Batching and polling

| Step | Batch | Poll |
|-|-|-|
| `find_people` | Up to 500 searches per run | First check after 2 minutes, then every 2 minutes, report status between checks |
| `scrape_property_lookup` | Up to 500 addresses per run | Same |
| `scrape_distress_list` | One market per run | Same |

Name each run with `fileName` where the tool accepts it (Property Lookup does). Download within 48 hours. Keep a run log: date, tool, class, inputs, runId, billed results, cost.

## 6. Merging results back to inputs

1. Keep an `input_id` for every input row and attach it to the search value before the run (a side table keyed on the normalized address, phone or email).
2. After download, join results on the normalized search value. One input can return several candidates; score each and keep the best.
3. Two inputs with the same search value (two filings on one property) share one search. Dedupe search values before the run to avoid paying twice.
4. Write `matched_by` as class plus tool, for example `A1:find_people:address`.

## 7. Output schema

| Column | Example | Rule |
|-|-|-|
| `input_id` | `cty-0193` | From the input file |
| `property_address` or input identifier | `2217 Elmwood Ave, Columbus, OH 43211` | USPS format |
| `owner_type` | `person` | person, llc, trust, bank, estate |
| `matched_name` | `Darnell Hughes` | As returned |
| `match_score` | `92` | 0 to 100 |
| `match_band` | `confirmed` | confirmed, probable, weak, no_match |
| `matched_by` | `A1:find_people:address` | Class and tool |
| `current_address` | `2217 Elmwood Ave, Columbus, OH 43211` | USPS format |
| `phone_1` to `phone_3` | `+16145550173` | E.164, best first |
| `phone_n_type` | `mobile` | From the result or a lookup; `unknown` if absent |
| `phone_n_dnc` | `clear` | clear, national, state, internal |
| `phone_n_status` | `callable_manual` | callable_manual, hold_dnc, hold_internal_dnc, do_not_call_deceased, mail_only |
| `email_1`, `email_2` | `dhughes@mail.example` | Lowercase |
| `flags` | `ABSENTEE;CO_OWNER` | Semicolon list |
| `source` | `county_filing|people_finder` | Controlled vocabulary plus the user's source |
| `pulled_at` | `2026-10-13` | ISO date |

## 8. Funnel template

```text
Input rows                                  N0
After normalization (fixable rows fixed)    N1
Searched (first pass)                       N1
Confirmed or probable after first pass      N2
Rescued or escalated                        N3
Confirmed or probable after rescue          N4
With at least one phone                     N5
With at least one callable phone            N6
```

## 9. Failure modes

| Symptom | Cause | Fix |
|-|-|-|
| Most address searches return a different surname | Owner does not live there (rentals) | Property Lookup with owner contact for that segment |
| Many results per name search | Common names, no city in scoring | Add city and state to scoring; drop to mail |
| Run `FAILED` | Malformed addresses | Normalize, require ZIP |
| Cost higher than the estimate | `max_results` larger than planned, or duplicate search values | Check the run inputs; dedupe search values |
| Phones mostly on the Registry | Normal for homeowner lists | Mail-first campaign; calls only to clear numbers |

## Sources

- ScraperCity tool catalog: references/scrapercity-catalog.md
- ScraperCity agent patterns (polling, run log, 48-hour downloads): references/scrapercity-agent-patterns.md
- ScraperCity platform facts (public-records boundary): references/scrapercity-platform.md
- USPS Publication 28: https://pe.usps.com/text/pub28/welcome.htm
- https://scrapercity.com/api-docs
