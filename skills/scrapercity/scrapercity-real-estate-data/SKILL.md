---
name: scrapercity-real-estate-data
description: >-
  Plans and runs ScraperCity real estate pulls: Zillow agent lists, property
  lookups with owner contact, distressed property lists (pre-foreclosure,
  foreclosure, auction, bank-owned), Crexi commercial listings, BizBuySell
  businesses for sale, and People Finder for owner contact. Produces a
  real estate data plan with tool calls, a cost table and a compliance check
  per channel. Use when the user is an agent, wholesaler, investor, lender,
  commercial broker or business broker who wants agent lists, motivated
  seller lists, owner phone numbers, property values, CRE broker contacts or
  business-for-sale listings.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags: [real-estate, zillow, foreclosure, skip-tracing, crexi, bizbuysell, wholesaling]
  related_skills: [using-scrapercity-skills, scrapercity-mcp, scrapercity-api, skip-tracer, mobile-appender, cold-calling, local-business-list, scrapercity-local-business-database, scrapercity-lead-database]
  frameworks:
    - "FCC - TCPA, 47 U.S.C. 227 and 47 CFR 64.1200"
    - "FTC - Telemarketing Sales Rule and National Do Not Call Registry"
    - "FTC - Fair Credit Reporting Act guidance"
    - "CFPB - Regulation O, Mortgage Assistance Relief Services (12 CFR 1015)"
    - "State wholesaling laws - Illinois RELA, Oklahoma Predatory Real Estate Wholesaler Prohibition Act, Pennsylvania Act 52 of 2024, Ohio SB 155, South Carolina Real Estate Commission guidance"
    - "California Civil Code 1695 - Home Equity Sales Contracts"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, outbound-compliance-primer.md, scrapercity-agent-patterns.md]
---

# ScraperCity Real Estate Data

## Overview

This skill picks the right ScraperCity real estate tool for the job, builds the exact call, prices it from the catalog before anything runs, and attaches a compliance check to every outreach channel the data will feed.

Tools covered, with catalog prices:

| Tool | Id | Price | Input that drives it |
|---|---|---|---|
| Zillow Agents | `scrape_zillow_agents` | $0.029 per agent | `location`, optional `specialty`, `language`, `searchLimit` (1-500) |
| Property Lookup | `scrape_property_lookup` | $0.15 per property, +$0.10 for owner contact | `addresses` (full address), `includeOwnerContact`, `fileName` |
| Distress List | `scrape_distress_list` | $0.05 per property | `search` (city + state or ZIP), `distressTypes`, `maxItems` (1-500) |
| Crexi | `scrape_crexi` | $0.029 per property | `startUrls` (Crexi property search, city or market search, or broker directory) |
| BizBuySell | `scrape_bizbuysell` | $0.0099 per listing | `startUrls`, `maxItems`, `datasetName` |
| People Finder | `find_people` | $0.0199 per result (0 matches billed as 1 result) | `name`, `email`, `phone_number`, `street_citystatezip`, `max_results` |

The mistakes it prevents:

- Calling distressed homeowners' mobiles with a dialer and no consent check, which exposes the caller to TCPA statutory damages of $500 per violation, up to triple if willful.
- Using owner data to approve or deny a tenant, buyer or borrower. That is an FCRA use, and these results are not consumer reports.
- Wholesaling in Illinois, Oklahoma, Pennsylvania, Ohio or South Carolina with a script and contract built for a state without a wholesaling statute.
- Paying $0.25 a property (lookup plus owner contact) when a $0.05 distress list plus a $0.0199 People Finder search per owner covers the same need.

## When to Use

- "Get me every agent in Scottsdale who does luxury or relocation."
- "Pull pre-foreclosures and auctions in Tampa and find the owners' phones."
- "What's this house worth and who owns it?" for one or many addresses.
- "Scrape these Crexi searches for industrial listings and broker contacts."
- "Pull BizBuySell listings for HVAC businesses in Texas with the brokers."
- "Build a motivated-seller list for my wholesaling business."

Use a different skill for:

| Job | Skill |
|---|---|
| Skip tracing a list you already have, at volume | `skip-tracer` |
| Adding mobiles to B2B contacts | `mobile-appender` |
| The call script and cadence | `cold-calling` |
| Real estate brokerages and offices as local businesses | `scrapercity-local-business-database` |
| Executives at real estate firms by title | `scrapercity-lead-database` |

## Prerequisites

- Who the user is (agent, wholesaler, investor, lender, CRE broker, business broker) and the state(s) they work in.
- The outreach channel: mail, email, phone call, text. Each has different rules.
- For property work: full addresses with city, state and ZIP.
- For Crexi and BizBuySell: search URLs built on those sites with the filters set.
- Wallet balance: run `check_wallet` first. All tools here are pay per result on any plan.

## Authoritative Foundations

| Source | Contribution |
|---|---|
| ScraperCity catalog (`references/scrapercity-catalog.md`) and npm package 1.0.17 | Tool ids, inputs, prices, the Crexi URL forms and the 400 on a map view with no location, the property lookup requirement for a full address |
| TCPA, 47 U.S.C. 227 | Autodialed or prerecorded calls to wireless numbers need prior express consent; $500 per violation, up to triple if willful or knowing; a private right of action for more than one Do Not Call violation in 12 months |
| 47 CFR 64.1200 | No telephone solicitation to residential subscribers before 8 a.m. or after 9 p.m. local time; National Do Not Call Registry; the definition of prior express written consent; texts treated as calls in several provisions |
| FTC Telemarketing Sales Rule | Scrub against the Registry at least every 31 days; established business relationship lasts 18 months after a purchase or 3 months after an inquiry; most B2B calls are exempt from the DNC provisions; up to $53,088 per violation |
| FCRA (FTC guidance) | Using a consumer report for a tenant or credit decision triggers permissible purpose and adverse action duties. People Finder results are prospecting data and are never used for those decisions |
| CFPB Regulation O (12 CFR 1015) | Anyone offering to stop a foreclosure or modify a loan is a mortgage assistance relief provider: no advance fees, and required disclosures |
| State wholesaling laws | Illinois requires a license past one deal in 12 months; Oklahoma requires a license (effective Nov 1, 2021); Pennsylvania Act 52 (2024) adds licensing, written disclosures and a 30-day cancellation right; Ohio SB 155 (effective March 2, 2026) requires a wholesaler disclosure form; South Carolina treats marketing the property as brokerage |
| California Civil Code 1695 | Buying a residence in foreclosure from the owner: the seller can cancel until midnight of the fifth business day after signing |

Details and the full source list: `references/framework-notes.md` and `references/compliance-guide.md`.

## Workflow

### 1. Identify the persona and the job

| Persona | Typical job | Primary tools |
|---|---|---|
| Brokerage recruiter or vendor selling to agents | Agent lists by market and specialty | `scrape_zillow_agents` |
| Wholesaler or investor | Motivated sellers and owner contact | `scrape_distress_list`, then `find_people` |
| Agent prospecting listings | Pre-foreclosure and owner outreach, valuations for a CMA letter | `scrape_distress_list`, `scrape_property_lookup` |
| Lender or loan officer | Agent referral partners, investor borrowers, CRE and SBA deal flow | `scrape_zillow_agents`, `scrape_crexi`, `scrape_bizbuysell` |
| Commercial broker | Listings and competing broker contacts | `scrape_crexi` |
| Business broker or acquirer | Businesses for sale and their brokers | `scrape_bizbuysell` |

Playbooks for each persona: `references/workflow-playbooks.md`.

### 2. Run the compliance gate before any pull that feeds phone or text

Answer four questions and write the answers in the plan:

1. Channel: mail, email, call, text?
2. For calls or texts: manual dial or autodialer, live voice or prerecorded or AI voice? Consent on file?
3. State: does the user's state regulate wholesaling or equity purchases from owners in foreclosure?
4. Use: prospecting only? If any result could feed a tenant, credit, employment or insurance decision, stop: that is FCRA territory and these tools are not consumer reporting agencies.

If the answers are "text" or "autodialer" with no consent, the plan routes owners to mail or manual live calls only, with DNC scrubbing. Full matrix in `references/compliance-guide.md`.

### 3. Build the call and price it

Use the catalog prices only. Write units times price for each line. If the total is over $5, show the table and wait for a go-ahead. Run `check_wallet` and compare the balance to the total.

### 4. Run, poll, download

Every tool here is a run: start returns `runId`, then `check_run_status` until SUCCEEDED, then `download_results`. These finish in minutes; poll every 15 to 30 seconds. CLI: `npx scrapercity poll <runId>` then `npx scrapercity download <runId>`.

### 5. Chain owner contact

Distress List rows carry the property address and distress type. To reach the owner, send the property address to `find_people` as `street_citystatezip`. Set `max_results: 1` to cap spend: a search with no match is still billed as one result ($0.0199). For a full valuation plus owner name, phone and email in one call, `scrape_property_lookup` with `includeOwnerContact: true` costs $0.25 per property.

### 6. Scrub and route

Before a call list goes to anyone: scrub against the National DNC Registry (at least every 31 days) and the internal do-not-call list, flag mobiles, check state call-time rules, and route numbers without consent away from dialers and texting. Mail and email do not need DNC scrubbing; email to owners at personal addresses still follows CAN-SPAM.

### 7. Hand off

Agent lists go to email sequencing. Owner lists go to mail first, then manual calls. Crexi and BizBuySell broker lists are B2B contacts and go to email and calls (most B2B calls are exempt from the TSR's DNC provisions).

## ScraperCity Implementation

### Zillow Agents

```json
{"location": "Scottsdale, AZ", "specialty": "buyer", "language": "Spanish", "searchLimit": 200}
```

CLI: `npx scrapercity zillow-agents -l "Scottsdale, AZ" --specialty buyer --language Spanish --limit 200`. The CLI default limit is 10; set it. `specialty` is a code string; the CLI usage shows `buyer`, and ScraperCity's product page lists 40+ specialties such as buyer's agent, listing agent, relocation, foreclosure and short sale. Probe an unfamiliar code with `searchLimit: 5` before a full run.

### Property Lookup

```json
{"addresses": ["4410 W Linda Ln, Tampa, FL 33629"], "includeOwnerContact": true, "fileName": "tampa-owner-check"}
```

Addresses must include street, city, state and ZIP. The CLI in package 1.0.17 has no property lookup command; use the MCP tool or `POST /api/v1/scrape/property-lookup`.

### Distress List

```json
{"search": "Tampa, FL", "distressTypes": ["preForeclosure", "auction"], "maxItems": 300}
```

`distressTypes` values: `preForeclosure`, `foreclosure`, `auction`, `bankOwned`. `search` is a city and state or a ZIP. `maxItems` is 1-500, so a larger market runs as several ZIP searches. CLI: `npx scrapercity distress-list "Tampa, FL" --types preForeclosure,auction --max 300`.

### Crexi

```json
{"startUrls": ["PASTE_CREXI_PROPERTY_SEARCH_URL", "https://www.crexi.com/resources/find-a-broker/PASTE_REST_OF_BROKER_URL"]}
```

Replace the two PASTE values with URLs copied from the browser. A property search starts `https://www.crexi.com/properties?`, a city or market search starts `https://www.crexi.com/search?`. Set filters on Crexi (property type, price, cap rate) after choosing a city or market in the search bar, then copy the URL. Broker directory URLs (`https://www.crexi.com/resources/find-a-broker/...`) return brokers. A panned map with no city or market returns 400. CLI: `npx scrapercity crexi "<url>"`.

### BizBuySell

```json
{"startUrls": ["https://www.bizbuysell.com/texas/hvac-businesses-for-sale/"], "maxItems": 150, "datasetName": "tx-hvac"}
```

Use the same `datasetName` across runs to dedupe. CLI: `npx scrapercity bizbuysell "<url>" --limit 150`.

### People Finder

```json
{"street_citystatezip": ["4410 W Linda Ln, Tampa, FL 33629"], "max_results": 1}
```

CLI: `npx scrapercity people-find --address "4410 W Linda Ln, Tampa, FL 33629"`; separate several addresses with `|`.

### Worked cost estimate: wholesaler in Tampa

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| `scrape_distress_list` Tampa, preForeclosure + auction | 300 | $0.05 | $15.00 |
| `find_people` on each property address, `max_results: 1` | 300 | $0.0199 | $5.97 |
| `scrape_property_lookup` without owner contact on the 40 best leads | 40 | $0.15 | $6.00 |
| **Total** | | | **$26.97** |

The alternative of `scrape_property_lookup` with owner contact on all 300 would cost 300 x $0.25 = $75.00. Florida has no wholesaling licensing statute in the sources used here, but the Florida Telephone Solicitation Act covers autodialed calls and texts, so the plan routes owners to mail and manual calls.

## Output Format

A real estate data plan in Markdown from `templates/output-template.md`:

1. **Objective**: persona, market, outcome.
2. **Tool Plan**: one row per tool call with tool id, key parameters, units.
3. **Cost Estimate**: units x catalog price per line and a total.
4. **Compliance Check**: one row per channel with the law that governs it and the action.
5. **Outreach Routing**: which records go to which channel.
6. **Next Steps**.

Run `python3 scripts/check-output.py plan.md` before handing it over.

## Quality Check

- Every tool id is one of the six above, and every unit price matches the catalog.
- Every Property Lookup and People Finder address has a ZIP code.
- Every `distressTypes` value is one of `preForeclosure`, `foreclosure`, `auction`, `bankOwned`.
- `maxItems` and `searchLimit` are 500 or less.
- The cost total equals the sum of the lines, and over $5 was approved before running.
- Every outreach channel has a compliance row naming the law (TCPA, TSR, CAN-SPAM, FCRA, Regulation O or the state statute).
- No result is used for tenant screening, credit, employment or insurance decisions.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| Address without ZIP in Property Lookup | Full address required | Normalize to "street, city, ST ZIP" |
| `distressTypes: ["REO"]` | Not a value the tool takes | Use `bankOwned` |
| `maxItems: 2000` for a metro | Max is 500 | Split by ZIP |
| Crexi map URL after panning | Returns 400 | Choose a city or market in the Crexi search bar first |
| `find_people` with `max_results: 5` on every owner | Pays up to 5 results per search | Use 1, then rerun only the misses |
| Texting owners from a skip-traced list | TCPA consent and state mini-TCPA rules (Florida FTSA) | Mail plus manual calls, DNC scrubbed |
| "We can stop your foreclosure" scripts | Regulation O covers mortgage assistance relief offers | Make purchase offers only, or comply with 12 CFR 1015 |
| Same wholesaling contract in every state | IL, OK, PA, OH, SC have specific rules | Check `references/compliance-guide.md` and a local attorney |
| Using People Finder to screen tenants | FCRA use with a non-consumer-report source | Use a consumer reporting agency for screening |
| Zillow Agents with the CLI default | CLI default `--limit` is 10 | Set `--limit` |

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule, or which reference to open. |
| `references/tool-reference.md` | You need inputs, output fields, limits and CLI flags for each of the six tools. |
| `references/workflow-playbooks.md` | You are planning for an agent, wholesaler, investor, lender, CRE broker or business broker. |
| `references/compliance-guide.md` | Any list will feed calls, texts, mail or email to owners, or the user works in a state with a wholesaling statute. |
| `templates/output-template.md` | Start every real estate data plan here. |
| `examples/worked-example.md` | A finished plan for a Tampa wholesaler. |
| `scripts/check-output.py` | Run on the finished plan. |
| `references/scrapercity-catalog.md` | Prices and schemas. |
| `references/scrapercity-platform.md` | Plans and the compliance boundary for public-records tools. |
| `references/outbound-compliance-primer.md` | TCPA, DNC, CAN-SPAM, CASL and GDPR basics shared across skills. |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling and confirmation patterns. |

## Related Skills

- `skip-tracer`: owner contact at volume from a list you already have.
- `mobile-appender`: mobiles for B2B contacts.
- `cold-calling`: scripts and cadence once the list is compliant.
- `scrapercity-local-business-database`: brokerages, title companies and property managers as local businesses.
- `scrapercity-lead-database`: executives at real estate and lending firms.
- `local-business-list`, `scrapercity-mcp`, `scrapercity-api`, `using-scrapercity-skills`.
