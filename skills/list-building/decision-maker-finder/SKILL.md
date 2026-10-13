---
name: decision-maker-finder
description: >-
  Finds the people who own a buying decision at a given list of companies or
  domains, maps each to a buying role (economic buyer, owner, champion,
  technical evaluator), and returns verified work emails and, on request, mobile
  numbers. Runs a cost-ordered waterfall: Lead Database by companyDomain with
  seniority and department, Website Finder by job title for misses, Email Finder
  for names without emails, Mobile Finder last. Use when the user has accounts
  and asks "who should I contact at these companies", "find the decision makers",
  or "get me the CFO and VP Ops at these 300 domains".
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags: [decision-makers, buying-committee, contact-discovery, email-finder, mobile-finder, account-based]
  related_skills: [icp-list-builder, account-researcher, cold-email-list, mobile-appender, crm-enricher, tam-builder, multi-channel-outreach]
  frameworks:
    - "Gartner - B2B buying groups of 6 to 10 decision makers"
    - "MEDDIC (Dick Dunkel, Jack Napoli, John McMahon, PTC 1996) - economic buyer and champion"
    - "FCC - TCPA rules for calls and texts to mobile numbers"
    - "FTC - CAN-SPAM Act compliance guide"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, list-quality-standard.md, outbound-compliance-primer.md]
---

# Decision Maker Finder

## Overview

Input: a list of companies (domains preferred, names accepted). Output: a contact file with 1-3 people per account, each tagged with a buying role, a verified work email, an email status, and a mobile number only when the user asked for one and the use is lawful. The report shows coverage per account and per role, which tool found each contact, and what it cost.

The mistake it prevents: emailing whoever has the biggest title. A CEO of a 2,000-person company does not buy a scheduling tool; the VP Operations does, and the operations manager uses it. The skill picks roles from what the product is, then searches for those roles at each domain, cheapest source first.

## When to Use

- "Here are 300 target accounts, find who I should email."
- "Get the CFO and Controller at these domains."
- "Who runs IT at these hospitals?"
- "Find decision makers for our ABM list."
- After `tam-builder` or a CRM export produced the account list.

Use a different skill when:

| The user wants | Use |
|-|-|
| Accounts and people from an ICP, no account list yet | `icp-list-builder` |
| A one-page brief on a few accounts before a call | `account-researcher` |
| Mobiles appended to contacts they already have | `mobile-appender` |
| The finished contact file validated and ready for a sequencer | `cold-email-list` |
| Owners of local businesses by category and city | `local-business-list` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Account list with domains | Every tool keys on domain | Names only: resolve domains first (see `references/waterfall-runbook.md` section 1) |
| What the product does | Picks the buying roles | Ask |
| Contacts per account | Cost and complaint risk | 2 (economic buyer plus owner or champion) |
| Mobiles wanted? For what use? | Mobile Finder costs $0.25 per number found; calls and texts to mobiles carry TCPA rules | No mobiles |
| Suppression: customers, open deals, past sends | Avoid contacting owned accounts | Ask for CRM export |

## Authoritative Foundations

| Source | Contribution |
|-|-|
| Gartner B2B buying research | Complex purchases involve buying groups of roughly 6 to 10 people. One contact per account under-covers the decision; 2-3 targeted roles is a practical floor for outbound. |
| MEDDIC, created at PTC in 1996 by Dick Dunkel with Jack Napoli under John McMahon | Two letters drive this skill: the Economic Buyer (who can approve the spend) and the Champion (who wants the change and sells it inside). The role map in `references/buying-role-map.md` names both per product category. |
| FCC, Telephone Consumer Protection Act | Autodialed or prerecorded calls and texts to mobile numbers need prior express consent, with business-to-business calls not exempt from the mobile rules. Mobiles are for manual, one-to-one calling unless consent exists. |
| FTC CAN-SPAM guide | Covers B2B email with no exemption; identify yourself, include a physical address, honor opt-outs within 10 business days. |
| `references/list-quality-standard.md` | Columns, normalization, dedupe, validation buckets, per-domain cap. |

Details in `references/framework-notes.md`.

## Workflow

### 1. Clean the account list

Normalize every domain to its registrable form, drop duplicates, drop platform hosts, and remove suppressed accounts (customers, open deals). Accounts with only a name need a domain: try `query_lead_database` with `companyName` and `limit: 5` and read `company_domain` from the rows; mark unresolved accounts and continue without them.

### 2. Choose roles

From `references/buying-role-map.md`, pick the product category and write the role plan:

| Slot | Role | Seniority | Department | Title family |
|-|-|-|-|-|
| 1 | Economic buyer | vp, c_suite | from the map | from the map |
| 2 | Owner or champion | director, manager | same | from the map |
| 3 (optional) | Technical evaluator or user lead | manager, senior | from the map | from the map |

Adjust by company size: under 50 employees, slot 1 is the founder or owner and slot 2 is often empty; over 1,000, slot 1 moves up to SVP and slot 2 is a director.

### 3. Lead Database pass (included in plan)

Batch domains, 25-50 per call, comma separated in `companyDomain`, with the role's `seniority`, `department` and `title`, plus `hasEmail: true`. Page with `after` until `next_after` is null. For each domain, rank returned people by role fit (title family match, then seniority, then email present) and keep the best person per slot.

Coverage after this pass decides the next step:

| Account state | Next step |
|-|-|
| All slots filled with an email | Done for this account |
| Slot filled, no email | Email Finder (step 5) |
| Slot empty | Website Finder for that title (step 4) |
| Domain returned no people at all | Website Finder for slot 1 title; for very large companies, an Apollo.io search URL through `scrape_apollo` |

### 4. Website Finder pass (pay per contact found)

`scrape_website_finder` takes many `domains` but one `jobTitle` per request. Group the empty-slot domains by the title you need and send one run per title. Leave `autoValidateEmails` and `autoFindMobiles` off: the catalog prices validation at $0.0072 through `validate_emails`, so every found email goes through that one step (step 6) and lands in one results file. Poll `check_run_status` every 60 seconds, then `download_results`.

### 5. Email Finder pass (pay per email found)

For people with a name and domain but no email, send `find_emails` with `contacts: [{first_name, last_name, domain}]`. Found emails are validated at lookup time per the tool description; record them with `email_status = valid` and `source` ending in `email_finder`.

### 6. Validate the rest

Every email from the Lead Database and from Website Finder goes through `validate_emails` in one run after dedupe. Bucket per the quality standard. Only `valid` rows reach the main file.

### 7. Mobiles (only if asked)

Confirm the use: one-to-one manual calls or texts with consent. Then send work emails or LinkedIn URLs of slot 1 and slot 2 contacts to `find_mobiles` as `inputs`. Store results in `mobile` in E.164, never in `phone`.

### 8. Assemble and report

One row per person with `account_domain`, `buying_role`, `found_by`, `email_status`, plus the person schema. Cap at the agreed contacts per account. Fill the report from `templates/output-template.md` and run `scripts/check-output.py`.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Balance | `check_wallet` | Free |
| Database pass | `query_lead_database` | Included on Growth and Scale, 100,000 new leads a day |
| Title search on domains | `scrape_website_finder` | $0.0499 per contact found |
| Email from name and domain | `find_emails` | $0.05 per email found, free if not found |
| Validation | `validate_emails` | $0.0072 per email |
| Mobiles | `find_mobiles` | $0.25 per number found, free if not found |
| Large-company search by URL | `scrape_apollo` | $0.0039 per lead, 500 minimum, hours to days, use a webhook |
| Runs | `check_run_status`, `download_results`, `list_runs` | Free |

### Lead Database pass

```json
{"companyDomain": "northbayfoods.example, pinecrestmfg.example, harborlinelogistics.example",
 "seniority": ["vp", "c_suite"],
 "title": "VP Operations, COO, Chief Operating Officer, VP Supply Chain, Director of Operations, Plant Manager",
 "notTitle": "assistant, intern, former, coordinator",
 "hasEmail": true, "limit": 100, "after": "0"}
```

Run a second call for slot 2 with `"seniority": ["director"]` and the champion titles. The tool documents `vp`, `director`, `c_suite` for seniority and `sales`, `engineering` for department; test other department values with a `limit: 1` call.

### Website Finder pass

```json
{"domains": ["pinecrestmfg.example", "ridgefieldpackaging.example"],
 "jobTitle": "VP Operations",
 "autoValidateEmails": false}
```

### Email Finder pass

```json
{"contacts": [
  {"first_name": "Lena", "last_name": "Okafor", "domain": "northbayfoods.example"},
  {"full_name": "Tomas Ruiz", "domain": "harborlinelogistics.example"}
]}
```

Use `company_name` only when no domain exists; domains give better matches per the tool's own schema note.

### Mobile Finder pass

```json
{"inputs": ["lena.okafor@northbayfoods.example", "https://www.linkedin.com/in/tomas-ruiz-ops"]}
```

### Apollo for large accounts

Build the people search on Apollo.io (Filters 1.0 URL) for the large accounts that the database pass missed, then:

```json
{"url": "https://app.apollo.io/#/people?organizationDomains[]=bigco.example&personSeniorities[]=vp", "count": 500, "fileName": "dmf-large-accounts"}
```

The response may include a `lead_database` block with matching leads already available in the Lead Database; pull those first. Apollo runs take hours to several days, so register a webhook at app.scrapercity.com/dashboard/webhooks or poll at most hourly.

### Worked cost estimate (ceiling)

300 accounts, 2 slots each, 600 slots. Prices are per result found, so the table shows the ceiling if every lookup hits; real cost is lower.

| Item | Max units | Unit price | Ceiling |
|-|-:|-:|-:|
| Lead Database pass | 600 slots | Included in Growth | $0.00 |
| Website Finder for slots the database left empty (planned 150) | 150 contacts | $0.0499 | $7.49 |
| Email Finder for names without email (planned 80) | 80 emails | $0.05 | $4.00 |
| Validation of database and Website Finder emails (planned 500) | 500 emails | $0.0072 | $3.60 |
| Mobile Finder, slot 1 only, if asked | 300 numbers | $0.25 | $75.00 |
| Total without mobiles | | | $15.09 |
| Total with mobiles | | | $90.09 |

Show this table, run `check_wallet`, and get approval before Website Finder, Email Finder or Mobile Finder runs above $5.

## Output Format

1. `decision-makers-[list]-[date].csv`: one row per contact, valid emails only, with `account_domain`, `buying_role`, `found_by`, `email_status`, `email_validated_at`, `mobile` (if requested), plus the person schema from the quality standard.
2. `decision-makers-[list]-[date]-gaps.csv`: accounts with an empty slot, the titles tried, and the tools tried.
3. A report from `templates/output-template.md`: role plan, waterfall results by step, coverage by role, validation, mobiles, cost, sample rows, gaps and next steps.

## Quality Check

- [ ] Role plan written before any search, tied to the product category.
- [ ] Every contact row has a buying role, an email status and a `found_by` tool.
- [ ] Main file is 100% `email_status = valid`.
- [ ] No account exceeds the agreed contacts per account.
- [ ] Waterfall table shows input and found counts per step, and found never exceeds input.
- [ ] Coverage by role adds up to the accounts searched.
- [ ] Mobile numbers only appear if requested, in E.164, with the stated use.
- [ ] Cost table uses catalog prices and states the total.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Pulling only C-suite | CEOs of mid-size companies ignore tools they will not use | Role map: economic buyer at VP level for most categories, plus an owner. |
| Website Finder with a comma list of titles | The tool takes one `jobTitle` per request | Group domains by title, one run per title. |
| Email Finder on names with no domain | Lower match rates | Resolve domains first; use `company_name` only as a fallback. |
| Validating Email Finder results again | They are validated at lookup | Validate only database and Website Finder emails. |
| Mobile Finder on every contact | $0.25 each adds up; mobiles carry TCPA rules | Slot 1 only, only when the user calls by hand. |
| Polling an Apollo run every minute | Runs take hours to days | Webhook, or hourly polling. |
| Six contacts at one account | Looks like a blast; complaints rise | Cap at the agreed number, 3 maximum. |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source or reasoning behind a rule, or the routing table. |
| `references/buying-role-map.md` | Choosing roles and title families for 22 product categories. |
| `references/waterfall-runbook.md` | Running the steps: batching, domain resolution, ranking candidates, branch logic, failure handling. |
| `references/mobile-and-contact-compliance.md` | Before requesting mobiles, or contacting people in Canada, the UK or the EU. |
| `references/list-quality-standard.md` | Columns, normalization, validation buckets (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database rules (shared). |
| `references/outbound-compliance-primer.md` | Full compliance rules (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished run for 300 food manufacturers. |
| `scripts/check-output.py` | Final gate on the report. |

## Related Skills

- `account-researcher` for a brief on the top accounts before outreach.
- `cold-email-list` to take this file to a sequencer.
- `mobile-appender` to add mobiles to an existing contact file.
- `icp-list-builder` when there is no account list yet.
- `tam-builder` to produce the account list.
- `crm-enricher` to write contacts back to the CRM.
- `multi-channel-outreach` to sequence email, phone and LinkedIn across the roles.
