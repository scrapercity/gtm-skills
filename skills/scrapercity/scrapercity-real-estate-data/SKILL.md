---
name: scrapercity-real-estate-data
description: >-
  Plans and runs ScraperCity real estate pulls: Zillow agent lists, property
  lookups with owner contact, distressed property lists (pre-foreclosure,
  foreclosure, auction, bank-owned), Crexi commercial listings, BizBuySell
  businesses for sale, and People Finder for owner contact. Produces a
  real estate data plan with tool calls, a cost table, match-confidence
  routing and a contact hygiene row per channel. Use when the user is an agent, wholesaler, investor, lender,
  commercial broker or business broker who wants agent lists, motivated
  seller lists, owner phone numbers, property values, CRE broker contacts or
  business-for-sale listings.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags:
    - real-estate
    - zillow
    - foreclosure
    - skip-tracing
    - crexi
    - bizbuysell
    - wholesaling
  related_skills:
    - using-scrapercity-skills
    - scrapercity-mcp
    - scrapercity-api
    - skip-tracer
    - mobile-appender
    - cold-calling
    - local-business-list
    - scrapercity-local-business-database
    - scrapercity-lead-database
  frameworks:
    - "ScraperCity - scrapercity npm package 1.0.17 and the Zillow Agents, Crexi and BizBuySell product pages"
    - "USPS - Publication 28, Postal Addressing Standards"
    - "Google - Email sender guidelines and FAQ (2024)"
    - "Yahoo - Sender Hub best practices (2024)"
    - "Hunter - Cold Email Guide, bounce rate (2023)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
---

# ScraperCity Real Estate Data

## Overview

This skill picks the right ScraperCity real estate tool for the job, builds the exact call, prices it from the catalog before anything runs, and routes every contact by who the recipient is and how sure the match is.

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

- Calling a People Finder result as if it were the owner when the returned address or name does not match the property record.
- Calling or mailing an owner who already said "stop" because that request sat in one dialer and never reached the mail house or the sender.
- Calling the same owner past the point where attempts still connect, while the caller ID picks up a spam label.
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

- Who the user is (agent, wholesaler, investor, lender, CRE broker, business broker) and the market they work.
- The outreach channel: mail, email, phone call. Each needs different fields and a different match bar.
- The suppression list the team already holds (past "stop" requests, wrong numbers, sold properties).
- For property work: full addresses with city, state and ZIP.
- For Crexi and BizBuySell: search URLs built on those sites with the filters set.
- Wallet balance: run `check_wallet` first. All tools here are pay per result on any plan.

## Authoritative Foundations

| Source | Contribution |
|---|---|
| ScraperCity catalog (`references/scrapercity-catalog.md`) and npm package 1.0.17 | Tool ids, inputs, prices, the Crexi URL forms and the 400 on a map view with no location, the property lookup requirement for a full address |
| USPS Publication 28 | Address normalization (suffixes, units, five-digit ZIP) for lookups, dedupe across ZIP runs and the match test |
| Google Email sender guidelines and FAQ; Yahoo Sender Hub | One-click unsubscribe, removals within 2 days, spam rate under 0.1% and never 0.3%: the email rows of every plan |
| Hunter Cold Email Guide (October 2023) | Bounces should not exceed 2% of emails sent: the hard bounce pause on every email row |

Details and the full source list: `references/framework-notes.md` and `references/contact-routing-guide.md`.

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

### 2. Set the contact plan before any pull that feeds phone or email

Answer four questions and write the answers in the plan:

1. Who is the recipient: a homeowner, an agent or broker at their business, a commercial owner entity, a lender's REO desk?
2. Which channels, in what order? Owners: mail, then calls, then email. Agents and brokers: email, then calls.
3. How will owner matches be confirmed? Address and name compared after USPS normalization; only confirmed and probable matches get calls.
4. Where does the suppression list live, and how does a "stop" from any channel reach every other tool the same day?

The channel table, match classes and reply triage are in `references/contact-routing-guide.md`.

### 3. Build the call and price it

Use the catalog prices only. Write units times price for each line. Show the table and wait for a go-ahead before any paid run. Run `check_wallet` and compare the balance to the total.

### 4. Run, poll, download

Every tool here is a run: start returns `runId`, then `check_run_status` until SUCCEEDED, then `download_results`. These finish in minutes; inside a conversation, check once per turn and report the status. CLI: `npx scrapercity poll <runId>` then `npx scrapercity download <runId> -o <file>.csv`.

### 5. Chain owner contact

Distress List rows carry the property address and distress type. To reach the owner, send the property address to `find_people` as `street_citystatezip`. Set `max_results: 1` to cap spend: a search with no match is still billed as one result ($0.0199). For a full valuation plus owner name, phone and email in one call, `scrape_property_lookup` with `includeOwnerContact: true` costs $0.25 per property.

### 6. Classify, suppress and route

Before a call list goes to anyone: give every owner row a `match_class` (confirmed, probable, unconfirmed), remove everything on the suppression list, and send unconfirmed rows to mail only. Validate every email; personal addresses from People Finder go to a separate campaign so their bounce and complaint rates are read on their own.

### 7. Hand off

Agent lists go to email sequencing. Owner lists go to mail first, then manual calls to confirmed matches. Crexi and BizBuySell broker lists are business contacts and go to email and calls to the firm line.

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

The alternative of `scrape_property_lookup` with owner contact on all 300 would cost 300 x $0.25 = $75.00. Mail goes to all 300 property addresses; calls go only to the People Finder results that pass the match test.

## Output Format

A real estate data plan in Markdown from `templates/output-template.md`:

1. **Objective**: persona, market, outcome.
2. **Tool Plan**: one row per tool call with tool id, key parameters, units.
3. **Cost Estimate**: units x catalog price per line and a total.
4. **Contact Hygiene**: one row per channel with the rule and its operating reason, plus the match test and where the suppression list lives.
5. **Outreach Routing**: which records go to which channel, by match class.
6. **Next Steps**.

Run `python3 scripts/check-output.py plan.md` before handing it over.

- Each fact once; every call and script written out in full (no `"..."` values, no loop described in a comment); no counts or results marked assumed. If nothing has run, say so once at the top.
- What the reader receives is the deliverable only: no internal file paths, reference section numbers or runbook IDs; another skill is named only in a handoff line that tells the user what to run next; no tables of checks that were not run (one "Not checked:" line instead); and no repeated identical rows where one template plus a list will do.

## Quality Check

- Every tool id is one of the six above, and every unit price matches the catalog.
- Every Property Lookup and People Finder address has a ZIP code.
- Every `distressTypes` value is one of `preForeclosure`, `foreclosure`, `auction`, `bankOwned`.
- `maxItems` and `searchLimit` are 500 or less.
- The cost total equals the sum of the lines, and the user approved it before running.
- Every outreach channel has a Contact Hygiene row with a rule and its operating reason.
- Calls go only to confirmed or probable matches; unconfirmed rows are mail only.
- The suppression list is named, applied before each drop and call block, and fed by every channel.
- The plan contains no legal commentary.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| Address without ZIP in Property Lookup | Full address required | Normalize to "street, city, ST ZIP" |
| `distressTypes: ["REO"]` | Not a value the tool takes | Use `bankOwned` |
| `maxItems: 2000` for a metro | Max is 500 | Split by ZIP |
| Crexi map URL after panning | Returns 400 | Choose a city or market in the Crexi search bar first |
| `find_people` with `max_results: 5` on every owner | Pays up to 5 results per search | Use 1, then rerun only the misses |
| Calling every People Finder result | Some results are a former resident or a relative, so the dial and the dialer minutes go to someone who cannot sell | Match test first; unconfirmed rows get mail only |
| Redialing a number with no connects | Dialer time spent with no conversations, and the caller ID can pick up a spam label | Cap attempts from your outcome data; swap a labeled number |
| Suppression kept in the dialer only | The same owner keeps getting letters and emails after saying stop | One list, synced to the mail house, dialer and sender before each drop |
| Re-mailing last month's list after a fresh distress pull | Owners who said no or sold get the same letter again | Dedupe the new pull against the suppression list and last month's file on normalized address |
| Zillow Agents with the CLI default | CLI default `--limit` is 10 | Set `--limit` |

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule, or which reference to open. |
| `references/tool-reference.md` | You need inputs, output fields, limits and CLI flags for each of the six tools. |
| `references/workflow-playbooks.md` | You are planning for an agent, wholesaler, investor, lender, CRE broker or business broker. |
| `references/contact-routing-guide.md` | Any list will feed mail, calls or email: channel order, match test, suppression list, message rules, reply triage, the Contact Hygiene table. |
| `templates/output-template.md` | Start every real estate data plan here. |
| `examples/worked-example.md` | A finished plan for a Tampa wholesaler. |
| `scripts/check-output.py` | Run on the finished plan. |
| `references/scrapercity-catalog.md` | Prices and schemas. |
| `references/scrapercity-platform.md` | Plans, databases and integrations. |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling and confirmation patterns. |

## Related Skills

- `skip-tracer`: owner contact at volume from a list you already have.
- `mobile-appender`: mobiles for B2B contacts.
- `cold-calling`: scripts and cadence once the list is matched and suppressed.
- `scrapercity-local-business-database`: brokerages, title companies and property managers as local businesses.
- `scrapercity-lead-database`: executives at real estate and lending firms.
- `local-business-list`, `scrapercity-mcp`, `scrapercity-api`, `using-scrapercity-skills`.
