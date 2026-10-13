---
name: skip-tracer
description: >-
  Turns names, phone numbers, emails or property addresses into current phones,
  emails and addresses with ScraperCity People Finder ($0.0199 per result; a
  search with 0 matches is billed as 1 result) and Property Lookup ($0.15 per
  property, plus $0.10 for owner contact), with Distress List as a lead feed.
  Searches the strongest identifier first, scores every match 0 to 100,
  escalates only weak or ownerless rows to the pricier tool, holds the FCRA
  line (no tenant, employment, credit or insurance decisions), and scrubs
  phones against Do Not Call before any call. Use when the user says "skip
  trace these owners", "find the owner's phone number", "here are property
  addresses, get me contacts", "find current contact info for these names", or
  "skip trace my pre-foreclosure list".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [skip-tracing, people-finder, property-owner, real-estate, fcra, dnc, public-records]
  related_skills: [scrapercity-real-estate-data, mobile-appender, cold-calling, crm-enricher, email-list-cleaner, scrapercity-mcp]
  frameworks:
    - "Fair Credit Reporting Act, 15 U.S.C. 1681 (FTC guidance on consumer reports and permissible purpose)"
    - "FTC enforcement - Spokeo (2012) and Instant Checkmate and TruthFinder (2023)"
    - "CFPB - Regulation F, 12 CFR 1006.10 location communications"
    - "FCC - TCPA, 47 U.S.C. 227 and 47 CFR 64.1200"
    - "FTC - Telemarketing Sales Rule and National Do Not Call Registry"
    - "CFPB - Regulation O, 12 CFR 1015 (mortgage assistance relief)"
    - "USPS - Publication 28 address standards"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, scrapercity-agent-patterns.md, outbound-compliance-primer.md]
---

# Skip Tracer

## Overview

This skill takes a list of people or properties and returns, for each row, the best current phones, emails and mailing address it can find, a match score from 0 to 100 with a band, the tool and identifier that produced the match, a DNC status for every phone, and a report that prices each step before it runs.

It prevents four mistakes:

1. Searching the weakest identifier. A name alone matches many people and People Finder bills every result. An address with a ZIP or a phone number usually returns one person.
2. Paying $0.25 a row for Property Lookup with owner contact on every address when a $0.0199 People Finder search answers most of them. This skill runs the cheap search first and escalates only weak matches and rows with no known owner.
3. Calling the wrong person. An address search returns the people tied to that address, which can be a tenant or a former owner. Every match is scored against what the input already knows before anyone dials.
4. Crossing the FCRA line. People Finder and Property Lookup results are prospecting and contact data. They are never the basis for a tenant, employment, credit or insurance decision.

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
| A tenant, employment or credit screen | No skill here. Use a consumer reporting agency that complies with the FCRA |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Purpose of the search, in one sentence | FCRA gate | Ask. Do not run without it |
| Who the user is (investor, agent, collector, law firm, business re-engaging customers) | Collectors follow Regulation F; investors follow foreclosure and state wholesaling rules | Ask |
| The input file and which identifiers each row has | Picks the search order | Profile it |
| Expected name for address rows (owner of record) | Needed to score an address match | Unknown; plan Property Lookup with owner contact for those rows |
| Outreach channel: mail, manual call, automated call, text, email | Compliance and whether a skip trace is even needed | Mail and manual calls |
| DNC access (Registry SAN) and internal do-not-call list | Scrub before calls | Ask; without it phones stay on hold |

## Authoritative Foundations

| Source | What it contributes here |
|-|-|
| FCRA, 15 U.S.C. 1681, and FTC guidance | A consumer report used for credit, insurance, employment or housing eligibility triggers permissible purpose, accuracy and adverse action duties. This skill's output is never used for those decisions. |
| FTC v. Spokeo (2012, $800,000) | A people-search site that marketed profiles to HR and recruiters for screening was treated as a consumer reporting agency. Selling or using people data for screening pulls it into the FCRA. |
| FTC v. Instant Checkmate and TruthFinder (2023, $5.8 million) | Background report sites were charged with acting as consumer reporting agencies without accuracy procedures and with giving reports to users who had no permissible purpose. |
| CFPB Regulation F, 12 CFR 1006.10 | Debt collectors contacting third parties for location information must identify themselves, say they are confirming or correcting location information, not mention the debt, and generally contact each third party once. |
| TCPA, 47 U.S.C. 227, and 47 CFR 64.1200 | Autodialed, prerecorded or AI-voice calls and texts to wireless numbers need consent; calling hours 8 a.m. to 9 p.m. local; internal DNC lists; $500 per violation in private actions, up to triple if willful. |
| FTC Telemarketing Sales Rule | Scrub against the National DNC Registry at least every 31 days. A skip-traced homeowner has no established business relationship with the caller. |
| CFPB Regulation O, 12 CFR 1015 | Offers to stop a foreclosure or modify a loan are mortgage assistance relief services; no advance fees and required disclosures. Purchase offers stay outside it. |
| USPS Publication 28 | Standard address format (street suffix and unit abbreviations, ZIP) so searches match. |

Details and routing: `references/framework-notes.md`. Compliance detail: `references/fcra-and-contact-compliance.md`. Nothing here is legal advice.

## Workflow

### 1. Purpose gate

Write the purpose in the report's first section. Stop if any answer below is yes:

| Question | If yes |
|-|-|
| Will the result help decide whether to rent to, hire, lend to, insure or extend credit to this person? | Stop. FCRA use. Send the user to a consumer reporting agency |
| Is the person someone the user knows personally and who has cut off contact? | Stop. Not a prospecting or business purpose |
| Is the user a debt collector locating a consumer? | Proceed under Regulation F location rules; no debt mention to third parties |
| Will numbers be autodialed, sent prerecorded or AI voice, or texted? | Proceed only for numbers with documented consent; everything else is manual calls or mail |

Also ask whether a skip trace is needed at all. For mail to property owners, the property address (and the owner mailing address from Property Lookup) may be enough.

### 2. Profile and normalize identifiers

Normalize addresses to USPS format ("4410 W Linda Ln, Tampa, FL 33629": number, directional, street, suffix, unit, city, two-letter state, ZIP), phones to E.164, emails to lowercase. Then class each row by its strongest identifier:

| Class | Identifier | Tool and parameter | `max_results` |
|-|-|-|-|
| A1 | Full address with ZIP and an expected name | `find_people` `street_citystatezip` | 1 |
| A2 | Full address with ZIP, owner unknown | `scrape_property_lookup` `includeOwnerContact: true` | n/a |
| P | Phone number | `find_people` `phone_number` | 1 |
| E | Personal email | `find_people` `email` | 1 |
| N1 | Name plus last known address | `find_people` `street_citystatezip` with that address, then a `name` search if the person moved | 1, then 3 |
| N2 | Name plus city and state only | `find_people` `name` | 3 |
| X | Name only, or address without ZIP | Fix the input first; skip the search |

Each array entry is its own search. The catalog does not document pairing a name and an address in one search, so search the stronger identifier and use the other to score.

### 3. Price it and pilot

```text
find_people ceiling   = searches x max(max_results, 1) x $0.0199
property lookup       = properties x $0.15, or x $0.25 with includeOwnerContact
distress list         = maxItems x $0.05
```

Pilot 25 rows per class to measure match rates. Run `check_wallet`. Over $5, show the estimate and wait for a go-ahead.

### 4. Run the strong searches

Batch up to 500 searches per run. Poll `check_run_status` every 2 minutes (these runs take minutes), then `download_results`. Keep the run log.

### 5. Score every match

Points (see `references/identifier-strategy-and-match-scoring.md` for edge cases):

| Evidence | Points |
|-|-|
| Name match to the expected person: exact first and last 40; last plus nickname or initial 30; last only 15 | up to 40 |
| Address: result's current address equals the input address 25; same city and state 10 | up to 25 |
| Corroboration: an input phone or email appears in the result | 20 |
| Recency: the result marks a phone or address as current or recent | 10 |
| Age or life-status fields consistent with the input (no deceased flag) | 5 |

Score only with fields present in the downloaded CSV header. If a field is absent, its points are unavailable: score = points earned / points available x 100. Rows with no expected name (A2 before lookup) cannot exceed the probable band.

| Band | Score | Use |
|-|-|-|
| `confirmed` | 80 to 100 | Call and mail |
| `probable` | 60 to 79 | Call with an identity check in the first sentence; mail |
| `weak` | 40 to 59 | Mail only; rescue search if budget allows |
| `no_match` | 0 to 39 | Rescue search or drop |

### 6. Rescue and escalate

| Row state | Next step | Cost |
|-|-|-|
| A1 weak or no match | `name` search, `max_results: 3`, scored against the city | up to 3 x $0.0199 |
| A2 or any address row needing an owner name | `scrape_property_lookup` with `includeOwnerContact: true` | $0.25 |
| Owner is an LLC, trust or bank | Do not skip trace the entity as a person; research the registered agent with the state, or mail the owner address | $0 |
| Deceased flag | Stop calling; mail to the estate at the property or the probate address | $0 |

### 7. Phone hygiene and DNC

Normalize every phone to E.164, keep line type where the data gives it, scrub the internal do-not-call list, then the National DNC Registry (within 31 days) and state lists. Homeowner calls are telephone solicitations; Registry numbers are removed unless the user holds written consent. Mark each phone `callable_manual`, `hold_dnc`, `hold_internal_dnc`, `do_not_call_deceased`, or `mail_only` when the row's band is below probable.

### 8. Deliver

CSV with one row per input and up to 3 phones and 2 emails ranked, plus the report from `templates/output-template.md`. Run `scripts/check-output.py`.

## ScraperCity Implementation

### Tools and prices (from `references/scrapercity-catalog.md`)

| Step | Tool | Price |
|-|-|-|
| Balance | `check_wallet` | Free |
| Lead feed | `scrape_distress_list` (`search`, `distressTypes`, `maxItems` 1 to 500) | $0.05 per property |
| Person search | `find_people` (`name`, `email`, `phone_number`, `street_citystatezip`, `max_results`) | $0.0199 per result; a search with 0 matches is billed as 1 result |
| Owner of record and contact | `scrape_property_lookup` (`addresses`, `includeOwnerContact`, `fileName`) | $0.15 per property, +$0.10 for owner contact |
| Email check for an email channel | `validate_emails` | $0.0072 per email |

Per scrapercity.com, People Finder searches 10B+ public records. That is coverage, not a match rate for any list.

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

1. `skiptrace-[segment]-[date].csv`: input columns, `match_score`, `match_band`, `matched_by` (class and tool), `matched_name`, `current_address`, `phone_1` to `phone_3` (E.164), `phone_n_dnc`, `phone_n_status`, `email_1`, `email_2`, `owner_type` (person, llc, trust, bank, estate), `flags`, `source`, `pulled_at`.
2. A report from `templates/output-template.md`: purpose and permissible use, input profile, identifier plan, cost, match scoring, funnel, contact results, compliance check, sample rows, next steps.

## Quality Check

- [ ] Purpose written, and the report states the results are not used for tenant, employment, credit or insurance decisions.
- [ ] Every search used the strongest identifier the row had, and `max_results` is 1 for address, phone and email searches.
- [ ] Cost lines equal billed results x $0.0199 for People Finder and properties x $0.15 or $0.25 for Property Lookup.
- [ ] Every row has a score and a band; the bands sum to the rows searched.
- [ ] No `weak` or `no_match` row has a phone marked callable.
- [ ] Every callable phone is E.164, off the internal list, and Registry-scrubbed within 31 days.
- [ ] Entities (LLC, trust, bank) and deceased flags are routed away from person outreach.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Name-only searches with `max_results: 10` | Bills up to 10 results per search for people you cannot tell apart | Strongest identifier first; names at 3 and scored |
| Address without ZIP | Weak matches and failed runs | USPS format with ZIP |
| Treating the first person at the address as the owner | Tenants and relatives live there | Score against the owner name; use Property Lookup with owner contact when the owner is unknown |
| Property Lookup with owner contact on every row | $0.25 versus $0.0199 | People Finder first, escalate only weak or ownerless rows |
| Skip tracing bank-owned properties | The owner is the lender | Drop `bankOwned` for owner outreach |
| Screening a tenant "just to check" | FCRA use with non-consumer-report data | Consumer reporting agency only |
| A collector telling a relative about the debt | Regulation F violation | Location script only; no debt mention |
| Texting skip-traced numbers | TCPA consent required | Manual calls and mail |
| Calling a Registry number because "it's public" | TSR and FCC DNC rules apply to homeowners | Scrub and remove |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or which file to open. |
| `references/identifier-strategy-and-match-scoring.md` | Choosing the search per row, setting `max_results`, scoring, rescue rules, entities and deceased owners. |
| `references/fcra-and-contact-compliance.md` | The purpose gate, FCRA boundary, collector rules, DNC and TCPA for homeowners, foreclosure offers. |
| `references/skip-trace-runbook.md` | Pricing, piloting, batching, the Distress List feed, Property Lookup escalation, output schema. |
| `references/outbound-compliance-primer.md` | Shared TCPA, DNC and email rules. |
| `references/list-quality-standard.md` | E.164 and normalization (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | The compliance boundary for public-records tools (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet, polling, retries (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished report for a Columbus, OH home-buying investor. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `scrapercity-real-estate-data` for distress lists, valuations, agent lists and state wholesaling rules.
- `mobile-appender` for B2B mobiles from LinkedIn URLs or work emails.
- `cold-calling` for scripts, identity checks and cadence.
- `crm-enricher` to write results back to a CRM with audit columns.
- `email-list-cleaner` to validate found emails before any email step.
- `scrapercity-mcp` for MCP setup.
