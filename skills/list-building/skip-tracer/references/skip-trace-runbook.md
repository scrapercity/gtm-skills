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
| `find_people` by address, then a name rescue at 3 on a share r of rows | $0.0199 + r x $0.0597 | Same, with some movers; r comes from the pilot |
| `scrape_property_lookup` without owner contact | $0.15 | Valuation and property facts only |
| `scrape_property_lookup` with owner contact | $0.25 | Owner unknown, absentee or multi-unit; one call returns owner name, phone and email |

## 3. Pilot

| Step | Rule |
|-|-|
| Sample | A random sample per identifier class; the size is the user's call (25 rows costs $0.50 at People Finder prices and $6.25 at Property Lookup with owner contact) |
| Measure | Share of rows reaching probable or better; average billed results per search |
| Decide | Cost per usable owner = cost per row / share reaching probable or better. Run the path with the lower cost per usable owner on that class |

Worked check: People Finder at $0.0199 per row, with 19 of 25 pilot rows (76%) reaching probable or better, costs $0.0199 / 0.76 = $0.026 per usable owner. Property Lookup with owner contact costs at least $0.25 per usable owner even if every row hits, so People Finder stays first for that class. The comparison flips only for a class where People Finder reaches probable on fewer than 0.0199 / 0.25 = 8% of rows and Property Lookup reaches nearly every owner.

## 4. Distress List as the feed

```json
{"search": "Columbus, OH", "distressTypes": ["preForeclosure", "auction"], "maxItems": 150}
```

| Choice | Rule |
|-|-|
| `search` | City and state, or one ZIP. A market with more than 500 properties runs as several ZIP searches, since `maxItems` stops at 500 |
| `distressTypes` | `preForeclosure` and `auction` for owner outreach. `foreclosure` for timing research. Skip `bankOwned` for owners: the lender owns it |
| `maxItems` | 1 to 500 |
| Next step | Rows carry the property address and distress type. The tool description says to pair it with People Finder to reach the owner. With no owner name in hand, run Property Lookup with owner contact, or People Finder capped at the probable band |

## 5. Batching and polling

| Step | Batch | Poll |
|-|-|-|
| `find_people` | Every search of one class in one run | Check once, report status, check again on the next turn |
| `scrape_property_lookup` | Every address of one class in one run | Same |
| `scrape_distress_list` | One market or ZIP per run | Same |

Name each run with `fileName` where the tool accepts it (Property Lookup does). Download the same day; results are stored for 48 hours. Keep a run log: date, tool, class, inputs, runId, billed results, cost.

## 6. Merging results back to inputs

1. Keep an `input_id` for every input row and attach it to the search value before the run (a side table keyed on the normalized address, phone or email).
2. After download, join results on the normalized search value. One input can return several candidates; band each and keep the one with the strongest evidence.
3. Two inputs with the same search value (two filings on one property) share one search. Dedupe search values before the run to avoid paying twice.
4. Write `matched_by` as class plus tool, for example `A1:find_people:address`.

## 7. Output schema

| Column | Example | Rule |
|-|-|-|
| `input_id` | `cty-0193` | From the input file |
| `property_address` or input identifier | `2217 Elmwood Ave, Columbus, OH 43211` | USPS format |
| `owner_type` | `person` | person, llc, trust, bank, estate |
| `matched_name` | `Darnell Hughes` | As returned |
| `match_evidence` | `name+address+contact` | Evidence tokens from the banding table |
| `match_band` | `confirmed` | confirmed, probable, weak, no_match |
| `matched_by` | `A1:find_people:address` | Class and tool |
| `current_address` | `2217 Elmwood Ave, Columbus, OH 43211` | USPS format |
| `phone_1` to `phone_3` | `+16145550173` | E.164, best first |
| `phone_n_type` | `mobile` | From the result or a lookup; `unknown` if absent |
| `phone_n_status` | `callable` | callable, suppressed, estate_mail, mail_only |
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
With at least one callable phone            N6   (off the suppression list)
```

## 9. QA sample against the owner of record

Before the call queue opens, pick a random sample of `confirmed` rows (the size is the user's call; the example checks 20) and check each against the county auditor or assessor site for that address:

| Check | Record | When rows miss |
|-|-|-|
| Matched name equals the owner of record (or a co-owner) | Matches out of rows checked | Read the missed rows' `match_evidence`; if they share one evidence type, move that type down one band and re-band the file, or send that input class to Property Lookup with owner contact |
| Matched person's current address is the property or the owner's mailing address on record | Matches out of rows checked | Absentee owners were read as residents: re-search the mailing address |
| Phone 1 is E.164 and not flagged `shared_line` | Passes out of rows checked | Fix the normalizer or the phone order |

Write it as one line in the report: "QA sample (20 confirmed rows against the Franklin County Auditor): owner of record 19 of 20, address 19 of 20, phone format 20 of 20."

## 10. Call outcomes and band review

Every dial that reaches a result gets one outcome:

| Outcome | Meaning | Row action |
|-|-|-|
| `right_party` | Spoke with the owner | Keep; log the conversation |
| `relative_or_tenant` | Reached a household member or tenant, not the owner | Ask for the best number for the owner; add it as a phone with source `call_note` |
| `wrong_number` | The number is not connected to the owner | Remove that phone; next phone in the order |
| `disconnected` | Number not in service | Remove that phone |
| `no_answer` | Voicemail or no pickup | Keep; retry on another day and time |
| `remove_request` | Asked not to be called | Suppression list, every number on the row, same day, every tool |

After the first call block, compute wrong-party share (`wrong_number` plus `relative_or_tenant` over reached results) for each band and each evidence type:

| Reading | Action |
|-|-|
| `probable` wrong-party share close to `confirmed` | Bands hold |
| `probable` well above `confirmed` | Probable rows drop to the back of the queue, or to mail only if rep time costs more than the deals they find |
| One evidence type carries most wrong parties | Move that evidence type down one band next run |
| `confirmed` wrong-party share high | Recheck the name normalization and the address comparison on the failed rows |

A number given by a relative or tenant goes first in the order for that row.

## 11. Handoff files

| File | Rows | Columns |
|-|-|-|
| Call queue | Rows with at least one `callable` phone, portfolio owners first, then confirmed, then probable | `input_id`, `matched_name`, every property address for the owner, `phone_1` to `phone_3` in order, `match_band`, `flags`, an outcome field |
| Mail file | Every input row | Owner name (or "Current Owner" below the probable band), mailing address (owner mailing address from Property Lookup when it differs from the property), property address, `input_id` |
| Email file | Only when email is a planned channel | `email_1` after validation, `matched_name`, property address |

Import the call queue into the dialer with the outcome list set up before the first call block, so section 10 has data to read.

## 12. Refresh

| Job | Cadence |
|-|-|
| Re-trace rows before a new campaign | Set the age from your wrong-number rate on rows of each `pulled_at` month |
| New distress filings in the same market | On the schedule you choose from how fast new filings appear; new properties only, deduped on the normalized address against earlier runs |

## 13. Failure modes

| Symptom | Cause | Fix |
|-|-|-|
| Most address searches return a different surname | Owner does not live there (rentals) | Property Lookup with owner contact for that segment |
| Many results per name search | Common names, no city in the banding | Band on city and state; drop to mail |
| Run `FAILED` | Malformed addresses | Normalize, require ZIP |
| Cost higher than the estimate | `max_results` larger than planned, or duplicate search values | Check the run inputs; dedupe search values |

## Sources

- ScraperCity tool catalog: references/scrapercity-catalog.md
- ScraperCity agent patterns (polling, run log): references/scrapercity-agent-patterns.md
- Franklin County Auditor, Ohio (property search; the owner of record used in the QA sample): https://auditor.franklincountyohio.gov/home
- USPS Publication 28: https://pe.usps.com/text/pub28/welcome.htm
- ScraperCity API docs (48-hour result storage): https://scrapercity.com/api-docs
