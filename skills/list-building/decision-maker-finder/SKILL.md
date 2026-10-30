---
name: decision-maker-finder
description: >-
  Finds the people who own a buying decision at a given list of companies or
  domains, maps each to a buying role (economic buyer, champion, technical
  evaluator), sizes the committee to the deal, and returns verified work emails
  and, on request, mobile numbers for reps who call. Runs a
  cost-ordered waterfall: Lead Database by companyDomain with seniority and
  department, Website Finder by job title for misses, Email Finder for names
  without emails, Mobile Finder last. Use when the user has accounts and asks
  "who should I contact at these companies", "find the decision makers", "map
  the buying committee", or "get me the CFO and VP Ops at these 300 domains".
  When the user describes a market (industry, size, geography) instead of
  naming accounts, use icp-list-builder.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.1.0"
  author: ScraperCity
  category: list-building
  tags:
    - decision-makers
    - buying-committee
    - contact-discovery
    - email-finder
    - mobile-finder
    - account-based
  related_skills:
    - icp-list-builder
    - account-researcher
    - cold-email-list
    - mobile-appender
    - crm-enricher
    - tam-builder
    - multi-channel-outreach
    - cold-calling
  frameworks:
    - "Gartner B2B Buying Report - buying groups of five to 11 stakeholders across five functions"
    - "MEDDIC (Dick Dunkel, Jack Napoli, John McMahon, PTC 1996) - economic buyer and champion"
    - "Alex Berman - start at the top of the account, move down a level after one to two weeks"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
---

# Decision Maker Finder

## Overview

Input: a list of companies (domains preferred, names accepted). Output: a contact file with the number of people per account the user sets, each tagged with a buying role, a verified work email, an email status, and a mobile number only when the user asked for one for a planned call block. When the user's past deals pulled in procurement, security or finance, it also produces a committee file: the procurement, security and finance names the AE will meet later, mapped from the Lead Database at no wallet cost and never sequenced. The report shows coverage per account and per role, which tool found each contact, and what it cost.

The mistake it prevents: emailing whoever has the biggest title. At a 2,000-person company, the VP Operations buys a scheduling tool and the operations manager uses it. The skill picks roles from what the product is and the deal size, then searches for those roles at each domain, cheapest source first.

## When to Use

- "Here are 300 target accounts, find who I should email."
- "Get the CFO and Controller at these domains."
- "Who runs IT at these hospitals?"
- "Map the buying committee for our 40 enterprise accounts."
- After `tam-builder` tiered the account list, or a CRM export produced it.

Use a different skill when:

| The user wants | Use |
|-|-|
| Decision-makers across a market defined by industry, size and geography (no account list yet), with company and contact counts, tiers and cost | `icp-list-builder` |
| Company counts, a TAM or a tiered account universe | `tam-builder` |
| A one-page brief on a few accounts before a call | `account-researcher` |
| Mobiles appended to contacts they already have | `mobile-appender` |
| The finished contact file validated and ready for a sequencer | `cold-email-list` |
| Owners of local businesses by category and city | `local-business-list` |
| Call scripts and call blocks for the mobiles | `cold-calling` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Account list with domains | Every tool keys on domain | Names only: resolve domains first (`references/waterfall-runbook.md` section 1) |
| What the product does | Picks the buying roles | Ask |
| Contacts per account | Sets cost and how many slots get sequenced | Ask |
| Which roles joined the user's last deals of this size (procurement, IT security, finance)? | Decides whether a committee file is built | Ask; no committee file if unknown |
| Mobiles wanted? Who calls, and when? | Mobile Finder costs $0.25 per number found | No mobiles |
| Suppression: customers, open deals, past sends, people who asked to be removed | One suppression list keeps owned accounts and removals out of every tool | Ask for the CRM export and the list |

## Authoritative Foundations

| Source | Contribution |
|-|-|
| Gartner B2B Buying Report (2022 survey) | The average enterprise buying group has five to 11 stakeholders from about five functions. Outbound reaches the number the user sets, in order; when the user's past deals pulled in more roles, the rest are mapped by name so the AE knows who joins later. |
| MEDDIC, created at PTC in 1996 by Dick Dunkel with Jack Napoli under John McMahon | Two letters drive the slots: the Economic Buyer (who can approve the spend) and the Champion (who wants the change and sells it inside). `references/buying-role-map.md` names both for 22 product categories. |
| Alex Berman (500,000+ meetings booked by his companies) | Start with the most senior relevant person and move down a level after one to two weeks without a reply; do not email several people at one company at once, since that can get the sender blocked company wide (Single Grain video, Lean B2B interview). Test one variable at a time (alexberman.com, cold email templates). The slot order is the send order. |
| `references/list-quality-standard.md` | Columns, normalization, dedupe, validation buckets, per-domain cap, the shared suppression list. |

Details in `references/framework-notes.md`.

## Workflow

### 1. Clean the account list

Normalize every domain to its registrable form, drop duplicates and platform hosts, and remove suppressed accounts (customers, open deals). Accounts with only a name need a domain: `query_lead_database` with `companyName` and `limit: 5`, accept the domain only when name, state and size agree with the source row; mark the rest unresolved and continue without them.

### 2. Size the committee and choose roles

Pick the product category in `references/buying-role-map.md` and set the slots from two user inputs:

| User input | Contact (sequenced, in this order) | Map only (named in the committee file, not emailed) |
|-|-|-|
| Contacts per account | Slots 1, 2, 3 in order, up to that number (MEDDIC: economic buyer, then champion, then evaluator) | Slots past that number |
| Roles that joined the user's last deals of this size | None | Those roles (procurement, IT security, finance from the map's committee table) |

Adjust by size with the map's size table: at the smallest companies slot 1 is the founder or owner and slot 2 is often the same person; at the largest, slot 1 moves to the SVP or business-unit head with a region in the title.

### 3. Lead Database pass (included in plan)

Batch domains in `companyDomain` (halve the batch on a 503), one call per slot, with the slot's `seniority`, `title` and `notTitle`. Count with `limit: 1`, then page with `after` until `next_after` is null. Rank people per slot (title match, seniority, email present, HQ country) and keep the best as primary and the next as backup. Map-only roles use the same pass and cost nothing from the wallet.

| Account state after this pass | Next step |
|-|-|
| Slot filled with an email | Validation (step 6) |
| Slot filled, no email | Email Finder (step 5) |
| Slot empty | Website Finder for that title (step 4) |
| Domain returned no people, over 1,000 employees | Apollo.io search URL through the Lead Database `url` first, then `scrape_apollo` |

### 4. Website Finder pass (pay per contact found)

`scrape_website_finder` takes many `domains` but one `jobTitle` per request. Group empty-slot domains by the title needed and send one run per title; misses get one more run with the fallback title. Leave `autoValidateEmails` and `autoFindMobiles` off so every email goes through one validation run and mobiles are bought only for the slots the user asked for.

### 5. Email Finder pass (pay per email found)

For people with a name and domain but no email, send `find_emails` with `contacts: [{first_name, last_name, domain}]` (or `full_name`). Found emails are validated at lookup per the tool description; record them with `email_status = valid` and `found_by = email_finder`.

### 6. Validate the rest

Every Lead Database and Website Finder email goes through `validate_emails` in one run after dedupe and suppression. Map `email_result` into the standard's buckets (`valid_catch_all` becomes `catch_all`). Only `valid` rows reach the main file; `invalid` names go back to Email Finder once.

### 7. Mobiles (only if asked)

Run the decision table in `references/mobile-and-phone-handling.md`: a named rep and a dated call block exist, and one do-not-contact list is shared across tools. Send valid work emails or profile URLs for the agreed slots to `find_mobiles`. Store results in `mobile` as E.164, never in `phone`.

### 8. Assemble and report

One row per person with `account_domain`, `slot`, `buying_role`, `found_by`, `email_status`, plus the person schema. Cap at the agreed contacts per account; the committee file holds map-only names. Fill the report from `templates/output-template.md` and run `scripts/check-output.py`.

### 9. After launch: role audit

Before launch, the user sets the number of replies or connected calls to review and the wrong-person share that triggers a title change. At that count, sort answers into wrong person, referred, not now, not interested and meeting. Count wrong-person and referral answers per slot title; "not now" is timing and never counts against the title. A slot over the user's threshold means the role map picked the wrong title for this product: promote the referred-to title into the slot and re-run step 3 for accounts not yet contacted. Change the slot title or the copy, never both in the same round (Berman: test one variable at a time), so the next review shows which change worked.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Balance | `check_wallet` | Free |
| Database pass and committee map | `query_lead_database` | Included on Growth and Scale, 100,000 new leads a day |
| Title search on domains | `scrape_website_finder` | $0.0499 per contact found |
| Email from name and domain | `find_emails` | $0.05 per email found, free if not found |
| Validation | `validate_emails` | $0.00169 per email |
| Mobiles | `find_mobiles` | $0.25 per number found, free if not found |
| Large-company search by URL | `scrape_apollo` | $0.0039 per lead, 500 minimum, usually 15 to 30 minutes, use a webhook |
| Runs | `check_run_status`, `download_results`, `list_runs` | Free |

### Lead Database pass

```json
{"companyDomain": "northbayfoods.example, pinecrestmfg.example, harborlinelogistics.example",
 "seniority": ["vp", "c_suite"],
 "title": "VP Operations, COO, Chief Operating Officer, VP Supply Chain, Director of Operations, Plant Manager",
 "notTitle": "assistant, intern, former, coordinator",
 "limit": 100, "after": "0"}
```

Run a second call for slot 2 with `"seniority": ["director"]` and the champion titles. The tool documents `vp`, `director`, `c_suite` for seniority and `sales`, `engineering` for department; test other values with a `limit: 1` call.

Committee map when the user's past deals pulled in procurement and security (same batch):

```json
{"companyDomain": "northbayfoods.example, pinecrestmfg.example",
 "title": "Procurement, Purchasing, Sourcing, Information Security, IT Security, Controller",
 "notTitle": "assistant, intern, former, clerk, analyst i",
 "limit": 100, "after": "0"}
```

### Website Finder pass

```json
{"domains": ["pinecrestmfg.example", "ridgefieldpackaging.example"],
 "jobTitle": "VP Operations",
 "autoValidateEmails": false,
 "autoFindMobiles": false}
```

### Email Finder pass

```json
{"contacts": [
  {"first_name": "Lena", "last_name": "Okafor", "domain": "northbayfoods.example"},
  {"full_name": "Tomas Ruiz", "domain": "harborlinelogistics.example"}
]}
```

Use `company_name` only when no domain exists; the tool's schema marks domain as preferred.

### Mobile Finder pass

```json
{"inputs": ["lena.okafor@northbayfoods.example", "https://www.linkedin.com/in/tomas-ruiz-ops"]}
```

### Apollo for large accounts

Build the people search on Apollo.io (Filters 1.0 URL) for the large accounts the database pass missed. First try it free: `query_lead_database` with `url` set to that search and `limit: 1`; read `search_translation` and `pagination.total`. Only if that falls short:

```json
{"url": "https://app.apollo.io/#/people?organizationDomains[]=bigco.example&personSeniorities[]=vp", "count": 500, "fileName": "dmf-large-accounts"}
```

Apollo runs usually take 15 to 30 minutes; register a webhook at app.scrapercity.com/dashboard/webhooks or poll every few minutes.

### Worked cost estimate (ceiling)

300 accounts, 2 contact slots each (the user's input), 600 slots, plus slot 3 mapped because evaluators joined the user's past deals. Prices are per result found, so the table is the ceiling if every lookup hits.

| Item | Max units | Unit price | Ceiling |
|-|-:|-:|-:|
| Lead Database pass (contact slots and slot 3 map) | 900 slots | Included in Growth | $0.00 |
| Website Finder for slots the database left empty (planned 150) | 150 contacts | $0.0499 | $7.49 |
| Email Finder for names without email (planned 80) | 80 emails | $0.05 | $4.00 |
| Validation of database and Website Finder emails (planned 500) | 500 emails | $0.00169 | $0.85 |
| Mobile Finder, slot 1 only, if asked | 300 numbers | $0.25 | $75.00 |
| Total without mobiles | | | $12.34 |
| Total with mobiles | | | $87.34 |

Run a test batch of each paid step, at a size the user picks, to turn the ceiling into an expected cost (hit rates are unknown until measured). Show this table, run `check_wallet`, and get approval before any paid step.

## Output Format

1. `decision-makers-[list]-[date].csv`: one row per contact, valid emails only, with `account_domain`, `slot`, `buying_role`, `found_by`, `email_status`, `email_validated_at`, `mobile` (if requested), plus the person schema from the quality standard.
2. `decision-makers-[list]-[date]-committee.csv` (when map-only roles exist): map-only names with `buying_role`, never loaded into a sequencer.
3. `decision-makers-[list]-[date]-gaps.csv`: accounts with an empty slot, the titles tried, and the tools tried.
4. A report from `templates/output-template.md`: account list funnel, role plan, waterfall results by step, coverage by role, validation, mobiles, cost, sample rows, gaps and next steps.

What the reader receives is the deliverable only: no internal file paths, reference section numbers, tool ids or skill names (name the product, such as Lead Database, Email Validator or Website Finder, and describe the next action instead of naming a skill); no sales-framework acronyms (keep the content: who signs, who champions); each figure stated once; every outside number with its source and date on first mention; no value left as "you set" when a sourced default or a dated step can carry it; no table of checks that were not run (one "Not checked:" line instead); no repeated identical rows where one template plus a list will do. Next steps are a table with Step, Owner, Date and Done when.

## Quality Check

- [ ] Role plan written before any search, tied to the product category, the contacts per account and the roles from the user's past deals.
- [ ] Every contact row has a buying role, an email status and a `found_by` tool.
- [ ] Main file is 100% `email_status = valid`; map-only names are in the committee file, not the main file.
- [ ] No account exceeds the agreed contacts per account.
- [ ] Waterfall table shows input and found counts per step, and found never exceeds input.
- [ ] Coverage by role adds up to the accounts searched.
- [ ] Mobile numbers only appear if requested, in E.164, with the call block and the do-not-contact check.
- [ ] Cost table uses catalog prices and states the total.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Pulling only C-suite | CEOs of mid-size companies ignore tools they will not use | Economic buyer at VP level for most categories, plus a champion. |
| Same committee for every deal size | Small deals pay for contacts nobody needs; big deals meet procurement late | Map the roles that joined the user's past deals of this size (step 2). |
| Emailing the map-only roles | Procurement and security do not own the budget, so the email reaches no economic buyer | Committee file only, for the AE. |
| Website Finder with a comma list of titles | The tool takes one `jobTitle` per request | Group domains by title, one run per title. |
| Email Finder on names with no domain | Lower match rates | Resolve domains first; `company_name` only as a fallback. |
| Validating Email Finder results again | They are validated at lookup | Validate only database and Website Finder emails. |
| Mobile Finder on every contact | $0.25 each adds up for numbers nobody dials | Slot 1 only, only for a planned call block. |
| Polling an Apollo run every few seconds | Burns the 100 a minute budget on a run that usually takes 15 to 30 minutes | Webhook, or polling every few minutes. |
| Six contacts at one account at once | Berman: several people at one company at once can get the sender blocked company wide | Cap at the agreed number; send in slot order. |
| Keeping a slot title after referrals pile up | Every new account repeats the miss | Role audit at the count the user set (step 9). |
| Swapping titles after a run of "not now" answers | Timing replies come from the right person; the swap throws away a working slot | Count only wrong-person and referral answers against a title. |
| Guessing the committee | Map-only rows nobody meets cost research time | Ask which roles joined the user's last deals of this size. |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source or reasoning behind a rule, or the routing table. |
| `references/buying-role-map.md` | Choosing roles, title families and committee roles for 22 product categories. |
| `references/waterfall-runbook.md` | Running the steps: batching, domain resolution, ranking candidates, branch logic, failure handling, cost formulas. |
| `references/mobile-and-phone-handling.md` | Before requesting mobiles: who gets one, storage, call blocks, the do-not-contact list, reading dispositions. |
| `references/list-quality-standard.md` | Columns, normalization, validation buckets, suppression (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database rules (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished run for 300 food manufacturers. |
| `scripts/check-output.py` | Final gate on the report. |

## Related Skills

- `account-researcher` for a brief on the top accounts before outreach.
- `cold-email-list` to take this file to a sequencer.
- `cold-calling` for scripts and call blocks once mobiles are in hand.
- `mobile-appender` to add mobiles to an existing contact file.
- `icp-list-builder` when there is no account list yet.
- `tam-builder` to produce and tier the account list.
- `crm-enricher` to write contacts and the committee file back to the CRM.
- `multi-channel-outreach` to sequence email, phone and LinkedIn across the roles.
