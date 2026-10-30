---
name: skip-tracer
description: >-
  Turns names, phone numbers, emails or property addresses into current phones,
  emails and addresses with ScraperCity People Finder ($0.0199 per result; a
  search with 0 matches is billed as 1 result) and Property Lookup ($0.15 per
  property, plus $0.10 for owner contact), with Distress List as a lead feed.
  Searches the strongest identifier first, bands every match by the evidence
  that confirms it, escalates only weak or ownerless rows to the pricier tool,
  and builds a call queue and a mail file. Use when the user says "skip trace
  these owners", "find the owner's phone number", "here are property
  addresses, get me contacts", "find current contact info for these names", or
  "skip trace my pre-foreclosure list".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags:
    - skip-tracing
    - people-finder
    - property-owner
    - real-estate
    - public-records
  related_skills:
    - scrapercity-real-estate-data
    - mobile-appender
    - cold-calling
    - crm-enricher
    - email-list-cleaner
    - scrapercity-mcp
  frameworks:
    - "USPS - Publication 28 postal addressing standards"
    - "ITU-T - Recommendation E.164 international phone number format"
    - "County auditor and assessor property records - owner of record"
    - "ScraperCity - People Finder, Property Lookup and Distress List catalog"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
    - scrapercity-agent-patterns.md
---

# Skip Tracer

## Overview

This skill takes a list of people or properties and returns, for each row, the best current phones, emails and mailing address it can find, a match band with the evidence behind it, the tool and identifier that produced the match, a call status for every phone, and a report that prices each step before it runs.

It prevents four mistakes:

1. Searching the weakest identifier. A name alone matches many people and People Finder bills every result. An address with a ZIP or a phone number narrows the search to a household or a subscriber.
2. Paying $0.25 a row for Property Lookup with owner contact on every address when a $0.0199 People Finder search answers many of them. This skill runs the cheap search first, measures its match rate on a pilot, and escalates only weak matches and rows with no known owner.
3. Calling the wrong person. An address search returns the people tied to that address, which can be a tenant or a former owner. Every match is banded by what the input already knows before anyone dials.
4. Paying twice for the same search. Two filings on one property, or one owner on several properties, are deduped before the run and grouped after it.

## When to Use

- "Here is a list of property addresses. Find the owners and their phone numbers."
- "Skip trace my pre-foreclosure list."
- "We have names and old addresses for past customers; find current contact info."
- "Reverse these phone numbers to names."
- "Pull distressed properties in Columbus and get me owner contacts."

Use a different skill when:

| The user wants | Use |
|-|-|
| Agent lists, valuations, Crexi or BizBuySell, or a real estate data plan | `scrapercity-real-estate-data` |
| Mobiles for B2B contacts from LinkedIn URLs or work emails | `mobile-appender` |
| Missing fields in a B2B CRM export | `crm-enricher` |
| The call script and cadence | `cold-calling` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| The input file and which identifiers each row has | Picks the search order | Profile it |
| Expected name for address rows (owner of record) | Needed to band an address match | Unknown; plan Property Lookup with owner contact for those rows |
| Outreach channel: mail, calls, email | Mail-only campaigns may not need a skip trace at all | Ask |
| Suppression list: everyone who asked to be removed, from every tool | Those numbers never enter the call queue | Ask; start one if none exists |
| Budget for the run | Sets how many rescue searches the plan can afford | Ask |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| USPS Publication 28 | Standard address format (street suffix and unit abbreviations, two-letter state, ZIP) so address searches match and dedupe. |
| ITU-T Recommendation E.164 | The international phone format (+, country code, number, at most 15 digits) every phone is normalized to before dedupe and dialing. |
| County auditor or assessor property records | The owner of record for an address, used to spot-check confirmed matches before the call queue opens. |
| ScraperCity catalog | People Finder bills $0.0199 per result with 0-match searches billed as 1; Property Lookup is $0.15 per property, +$0.10 for owner contact; Distress List is $0.05 per property, 1 to 500 per run, and its description says to pair it with People Finder to reach the owner. |
| ScraperCity API docs | Results are stored for 48 hours, so every run is downloaded the same day. |

Details and routing: `references/framework-notes.md`.

## Workflow

### 1. Decide whether a skip trace is needed

For mail to property owners, the property address (and the owner mailing address from Property Lookup) may be enough. Run a skip trace when the plan includes calls or email, or when the owner's mailing address is unknown.

### 2. Profile and normalize identifiers

Normalize addresses to USPS format ("4410 W Linda Ln, Tampa, FL 33629": number, directional, street, suffix, unit, city, two-letter state, ZIP), phones to E.164, emails to lowercase. Dedupe search values. Then class each row by its strongest identifier:

| Class | Identifier | Tool and parameter | `max_results` |
|-|-|-|-|
| A1 | Full address with ZIP and an expected name | `find_people` `street_citystatezip` | 1 |
| A2 | Full address with ZIP, owner unknown | `scrape_property_lookup` `includeOwnerContact: true` | n/a |
| P | Phone number | `find_people` `phone_number` | 1 |
| E | Personal email | `find_people` `email` | 1 |
| N1 | Name plus last known address | `find_people` `street_citystatezip` with that address, then a `name` search if the person moved | 1, then your name setting |
| N2 | Name plus city and state | `find_people` `name` | Your name setting (the example uses 3) |
| X | Name only, or address without ZIP | Fix the input first; skip the search |

Each array entry is its own search, and every returned result is billed, so `max_results` is 1 wherever the identifier points to one household or subscriber. For name searches, set `max_results` to the number of same-name candidates you are willing to pay to compare. The catalog does not document pairing a name and an address in one search, so search the stronger identifier and use the other to band.

### 3. Price it and pilot

```text
find_people ceiling   = searches x max(max_results, 1) x $0.0199
property lookup       = properties x $0.15, or x $0.25 with includeOwnerContact
distress list         = maxItems x $0.05
```

Pilot a random sample per class (the size is your call; 25 People Finder searches cost $0.50). From the pilot, compute cost per usable owner for each path: People Finder cost per search divided by its share of rows reaching probable or better, against $0.25 divided by Property Lookup's share. The cheaper path per usable owner runs on that class. Run `check_wallet`, show the estimate, and wait for a go-ahead before the paid run.

### 4. Run the strong searches

Send every search of a class in one run. Check `check_run_status` once, report the status, and check again on the next turn; then `download_results` the same day. Keep a run log: date, tool, class, inputs, runId, billed results, cost.

### 5. Band every match by its evidence

Compare each returned candidate with what the input already knows, using only fields present in the downloaded CSV header. Record the evidence in `match_evidence` and band from it:

| Evidence | Meaning | Band |
|-|-|-|
| `name+address`, `name+contact`, `name+address+contact` | Expected first and last name (or nickname or initial) matches, plus the input address or an input phone or email other than the one searched | `confirmed` |
| `owner_record` | Property Lookup returned a person as the owner of record for the input address | `confirmed` |
| `name+city` | Name matches, same city and state, different street | `probable` |
| `address_only` | No expected name; the result lives at the input address | `probable` |
| `surname+address` | Last name only, at the input address (spouse or relative) | `probable` |
| `name_only`, `surname+city` | Name with no location agreement, or surname in the same city | `weak` |
| `tie` | Two candidates carry the same evidence | `weak` |
| `entity` | Owner is an LLC, trust or bank | `weak` |
| `none`, `deceased` | Nothing agrees, or the result carries a deceased flag | `no_match` |

| Band | Use |
|-|-|
| `confirmed` | Call and mail |
| `probable` | Call with an identity check in the first sentence ("Am I speaking with the owner of 2217 Elmwood?"); mail |
| `weak` | Mail only; rescue search if budget allows |
| `no_match` | Rescue search, Property Lookup, or mail to "Current Owner" |

Then check a random sample of `confirmed` rows against the county auditor or assessor's owner of record and write the result as one QA line. When missed rows share one evidence type, move that evidence type down one band and re-band the file (`references/skip-trace-runbook.md` section 9).

### 6. Rescue and escalate

| Row state | Next step | Cost |
|-|-|-|
| A1 weak or no match | `name` search at your name setting, banded against the city | up to max_results x $0.0199 |
| A2 or any address row needing an owner name | `scrape_property_lookup` with `includeOwnerContact: true` | $0.25 |
| Owner is an LLC, trust or bank | Do not search the entity as a person; look up the registered agent in the state business registry, or mail the owner address | $0 |
| Deceased flag | Mail the estate at the property or the probate address | $0 |

The plan budgets one rescue per row. A second pass is another billed search, so price it before adding it.

### 7. Phone order and suppression

Normalize every phone to E.164 and keep line type where the data gives it. Order each row's phones by the recency field the CSV holds, newest first; once the first call block has outcomes, order line types by the connect rate you measured for each. A phone that shows up on two or more unrelated owners is a shared line (property manager, office): flag it and dial it last. Remove every number on the suppression list. Mark each phone `callable`, `suppressed`, `estate_mail`, or `mail_only` when the row's band is below probable.

### 8. Group owners, hand off, read the outcomes

1. Group rows by matched owner. An owner on two or more input properties is flagged `PORTFOLIO`, takes the strongest match across their rows, and goes to the top of the call queue with every address in one call.
2. Write three files: the call queue (callable rows, portfolio owners first, then confirmed, then probable, phones in order, an outcome field), the mail file (every input row, owner name or "Current Owner", the owner's mailing address when it differs from the property), and an email file only when email is a planned channel. Columns: `references/skip-trace-runbook.md` section 11.
3. Set up the dialer outcomes before the first call block: `right_party`, `relative_or_tenant`, `wrong_number`, `disconnected`, `no_answer`, `remove_request`. A `remove_request` goes on the suppression list the same day, every number on the row, in every tool. After the first block, compare the wrong-party share of `probable` with `confirmed` and decide from those numbers whether probable rows keep their calls next run (section 10).
4. Set a re-trace age before each new campaign from your own wrong-number rate on older rows. Write the report from `templates/output-template.md` and run `scripts/check-output.py`.

## ScraperCity Implementation

### Tools and prices (from `references/scrapercity-catalog.md`)

| Step | Tool | Price |
|-|-|-|
| Balance | `check_wallet` | Free |
| Lead feed | `scrape_distress_list` (`search`, `distressTypes`, `maxItems` 1 to 500) | $0.05 per property |
| Person search | `find_people` (`name`, `email`, `phone_number`, `street_citystatezip`, `max_results`) | $0.0199 per result; a search with 0 matches is billed as 1 result |
| Owner of record and contact | `scrape_property_lookup` (`addresses`, `includeOwnerContact`, `fileName`) | $0.15 per property, +$0.10 for owner contact |
| Email check for an email channel | `validate_emails` | $0.00169 per email |

### Calls

```json
{"tool": "scrape_distress_list", "args": {"search": "Columbus, OH", "distressTypes": ["preForeclosure", "auction"], "maxItems": 150}}
{"tool": "find_people", "args": {"street_citystatezip": ["2217 Elmwood Ave, Columbus, OH 43211", "88 S Harding Rd, Columbus, OH 43209"], "max_results": 1}}
{"tool": "find_people", "args": {"name": ["Darnell Hughes"], "max_results": 3}}
{"tool": "find_people", "args": {"phone_number": ["+16145550173"], "max_results": 1}}
{"tool": "scrape_property_lookup", "args": {"addresses": ["1406 Oakridge Dr, Columbus, OH 43224"], "includeOwnerContact": true, "fileName": "cbus-distress-owners"}}
```

Skip `bankOwned` in `distressTypes` for owner outreach: a bank-owned (REO) property belongs to the lender, so a skip trace reaches former owners. CLI for People Finder: `npx scrapercity people-find` with the name, email, phone or address options (several addresses separated by `|`), and `npx scrapercity distress-list "Columbus, OH"`. Package 1.0.17 has no Property Lookup CLI command; use MCP or `POST /api/v1/scrape/property-lookup`.

### Worked cost estimate

300 county pre-foreclosure filings with owner name and property address, plus 150 Distress List properties with no owner name, Columbus, OH.

| Line | Units | Unit price | Cost |
|-|-:|-:|-:|
| `scrape_distress_list`, preForeclosure and auction | 150 properties | $0.05 | $7.50 |
| `find_people` by address, A1 rows, `max_results: 1` | 300 billed results | $0.0199 | $5.97 |
| `find_people` name rescue, 71 rows, `max_results: 3` | 189 billed results | $0.0199 | $3.76 |
| `scrape_property_lookup` with owner contact, A2 rows | 150 properties | $0.25 | $37.50 |
| Total | | | $54.73 |

Ceiling before the run: rescue at 71 x 3 = 213 results ($4.24), so $55.21. The alternative of Property Lookup with owner contact on all 450 addresses would cost 450 x $0.25 = $112.50 plus the Distress List.

### Errors

| Code | Action |
|-|-|
| 402 | `check_wallet`, report the shortfall, run class A1 first. |
| 409 | Same search submitted moments ago; reuse the earlier run. |
| 429 | Wait 30 seconds, retry once. |
| Run `FAILED` | Read the logs; malformed addresses (no ZIP) are the usual cause. |

## Output Format

1. `skiptrace-[segment]-[date].csv`: input columns, `match_evidence`, `match_band`, `matched_by` (class and tool), `matched_name`, `current_address`, `phone_1` to `phone_3` (E.164), `phone_n_status`, `email_1`, `email_2`, `owner_type` (person, llc, trust, bank, estate), `flags`, `source`, `pulled_at`.
2. `calls-[segment]-[date].csv` (call queue) and `mail-[segment]-[date].csv` (every input row with the mailing name and address).
3. A report from `templates/output-template.md`: purpose and channels, input profile, identifier plan, cost, match bands with the QA line, funnel, contact results with portfolio owners and shared lines, sample rows, next steps with the dialer outcome setup.

What the reader receives is the deliverable only: product names (People Finder, Property Lookup, Distress List, Email Validator), never tool ids, internal file paths or reference section numbers; another skill is named only in a handoff line that tells the user what to run next; no tables of checks that were not run (one "Not checked:" line instead); no repeated identical rows where one template plus a list will do.

## Quality Check

- [ ] Purpose and channels written in one table.
- [ ] Every search used the strongest identifier the row had, and `max_results` is 1 for address, phone and email searches.
- [ ] Cost lines equal billed results x $0.0199 for People Finder and properties x $0.15 or $0.25 for Property Lookup.
- [ ] Every row has evidence and a band; the bands sum to the rows searched; each sample row's band matches its evidence.
- [ ] No `weak` or `no_match` row has a phone marked callable.
- [ ] Every callable phone is E.164 and off the suppression list.
- [ ] Entities (LLC, trust, bank) and deceased flags are routed away from person outreach.
- [ ] The QA line shows how many sampled confirmed rows match the county owner of record.
- [ ] Portfolio owners and shared lines are counted in Contact Results, and the call queue lists portfolio owners first.
- [ ] Next Steps sets up the six call outcomes and the band review before the first call block.
- [ ] The report names products, not tool ids or file paths.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Name-only searches with `max_results: 10` | Bills up to 10 results per search for people you cannot tell apart | Strongest identifier first; name searches at your setting and banded |
| Address without ZIP | Weak matches and failed runs | USPS format with ZIP |
| Treating the first person at the address as the owner | Tenants and relatives live there | Band against the owner name; use Property Lookup with owner contact when the owner is unknown |
| Property Lookup with owner contact on every row | $0.25 versus $0.0199 | Compare cost per usable owner on the pilot; escalate only weak or ownerless rows |
| Skip tracing bank-owned properties | The owner is the lender | Drop `bankOwned` for owner outreach |
| Searching an LLC as a person | Returns unrelated people with the same words in their name | Registered agent lookup, or mail the entity |
| Calling each property of a portfolio owner separately | Several reps call one owner about several houses | Group by owner; one call with every address |
| A removal request logged in one dialer only | The next tool calls or mails the same person again | One suppression list, updated the same day, synced to every tool |
| Never reading call outcomes | A probable band that reaches the wrong person keeps getting dialed | Read wrong-party share per band after the first block |
| Downloading days later | Results are stored for 48 hours | Download the same day |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/identifier-strategy-and-match-scoring.md` | Choosing the search per row, setting `max_results`, banding, rescue rules, entities and deceased owners, phone order, shared lines, portfolio owners. |
| `references/skip-trace-runbook.md` | Pricing, piloting, batching, the Distress List feed, Property Lookup escalation, output schema, QA sample, call outcomes and band review, handoff files, refresh. |
| `references/list-quality-standard.md` | E.164 and normalization (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and tool groups (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet, polling, retries (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished report for a Columbus, OH home-buying investor. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `scrapercity-real-estate-data` for distress lists, valuations and agent lists.
- `mobile-appender` for B2B mobiles from LinkedIn URLs or work emails.
- `cold-calling` for scripts, identity checks and cadence.
- `crm-enricher` to write results back to a CRM with audit columns.
- `email-list-cleaner` to validate found emails before any email step.
- `scrapercity-mcp` for MCP setup.
