---
name: local-business-list
description: >-
  Builds a send-ready list of local businesses for a category and area. Counts
  and pulls the Local Business Database first (keyword, location, hasWebsite,
  hasEmail, hasContact), splits big metros into sub-cities or map boxes, fills
  gaps with Google Maps and Yelp scrapes, finds missing emails on the business
  website, keeps only rows with a website and an email, dedupes by phone,
  domain and name plus postal code, validates every email, and exports a CSV.
  Use when the user asks for "dentists in Austin", "every roofer in Florida
  with an email", "local business leads", "scrape Google Maps for plumbers",
  or a list of shops, clinics, contractors or restaurants by city.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: list-building
  tags:
    - local-business
    - google-maps
    - yelp
    - local-business-database
    - smb
    - email-validation
  related_skills:
    - tam-builder
    - scrapercity-local-business-database
    - email-list-cleaner
    - cold-email-list
    - decision-maker-finder
    - mobile-appender
    - cold-email-copywriting
  frameworks:
    - "US Census Bureau - County Business Patterns as an establishment count benchmark"
    - "Google - Places Text Search returns at most 60 results per query"
    - "Google, Yahoo and Microsoft - bulk sender requirements (2024-2025)"
    - "Alex Berman - one niche, one result, small test batches"
    - "CMS - NPPES NPI Registry as a coverage list for health practices"
    - "State licensing boards - licensee download files (Florida DBPR) as a coverage list for trades"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - scrapercity-agent-patterns.md
    - list-quality-standard.md
    - deliverability-primer.md
---

# Local Business List

## Overview

This skill produces a CSV of local businesses in one category and area where every row has a website, an email that passed validation, a phone in E.164, a full address, and a named contact or owner where one exists, plus a call file when the user phones. A short report answers first (how many, what it cost, what to send first), then shows coverage, the funnel and the checks. When the tools are not connected or the user has not approved spend, the same skill delivers a Plan: measured free counts, decisions, a usage ceiling and a dated run schedule, with no invented counts.

The mistake it prevents is running one Google Maps scrape for "dentists in Houston", getting a slice of the city, paying for hundreds of rows with no email, and mailing `info@` addresses that bounce. Here the database goes first because it is included in the plan and can be counted before anything is spent. Scrapes fill only the sub-areas where the database is thin, and nothing ships until it has a website, an email, a dedupe pass and a `valid` result.

## When to Use

- "Get me every dentist in the Austin area with an email."
- "Roofers in Florida, owner name if possible."
- "Scrape Google Maps for HVAC companies in Phoenix."
- "Med spas in Miami, Fort Lauderdale and West Palm."
- An agency or SaaS selling to small businesses needs its first list in a new city.

Use a different skill when:

| The user wants | Use |
|-|-|
| A count of every business in a market, with TAM in dollars | `tam-builder` |
| Every Local Business Database parameter in depth | `scrapercity-local-business-database` |
| The owner's mobile number appended to an existing list | `mobile-appender` |
| Named managers at multi-location chains or franchises | `decision-maker-finder` |
| A send-ready file through to sequencer import with copy columns | `cold-email-list` (can start from this skill's CSV) |
| An old local list cleaned before sending | `email-list-cleaner` |

## Prerequisites

| Input | Why | Default if unknown |
|-|-|-|
| Category, in the words a customer would type on Google Maps | Becomes `keyword` and Maps search terms | Ask for 2-4 variants |
| Area: city, metro, state or list of ZIP codes | Becomes `location`, sub-city splits or map boxes | Ask |
| Use: cold email, cold calls, direct mail | Email required or not; phone rules | Cold email: website and email required |
| Named contact wanted? | Adds `hasContact` and Website Finder runs | Nice to have, not required |
| Exclusions: chains, franchises, current customers | `notCategory`, suppression | Exclude current customers by domain and phone |
| Target count | Pull size and cost | Everything that matches |
| Plan level | The Local Business Database needs Growth ($149/mo) or Scale | Run `check_wallet` and read the plan; Starter goes scrape-only. A user with no plan sees the all-in cost: the plan price plus any usage above its credit |
| Scope words | "Every", "all" and "independent" decide what stays | "Every" keeps sub-types (specialists, niches) tagged in `subtype`, and excluding them is offered as a decision; "independent" turns on the independence screen |
| Owner name wanted? | Turns on the owner sources in step 7 | Ask when the use includes calls or first-name email |
| Chain line, coverage target, QA sample size and pass line | User settings; no published benchmark exists | Ask; the plan lists them as decisions |

## Authoritative Foundations

| Source | What it contributes |
|-|-|
| US Census Bureau, County Business Patterns (CBP) | Establishment counts by NAICS code and county. Used as an outside benchmark: a database count far below the CBP count for the same county says the sub-area needs a scrape. |
| Google Maps Platform, Places Text Search | Google documents that a text search returns at most 60 results across all pages. A single Maps search over a large metro returns a capped slice, which is why this skill splits areas and treats a run that hits its cap as a sign to split further. |
| Google, Yahoo, Microsoft sender requirements (Feb 2024, May 2025) | Remove invalid recipients and keep complaints low. Local lists carry many small-host and catch-all domains, so validation and a catch-all cap are required before sending. |
| Alex Berman | Tight niches beat broad lists: one vertical, one result, about 100 emails per segment as a first test before scaling (Lean B2B interview). A list of every business in a city is the input; the campaign starts with one sub-segment. |
| CMS NPI Registry; state licensing board files | Lists built for billing and licensing, so they hold businesses that never filled in a Maps profile. Matching them against the pool gives a coverage percentage per sub-area and a `new_license` segment from the licensure date. The NPI API pages 200 records at a time and `skip` stops at 1,000, so one query returns at most 1,200 records (tested 2026-10-13). |
| State entity registries; group announcements | Arizona's eCorp search reaches an entity's principals from its legal name; Colorado files no officers or managers. Heartland Dental lists newly supported offices under their own practice names, so location counts alone miss group-run offices. |
| `references/list-quality-standard.md` | Business columns (section 2b), dedupe keys for local businesses (section 4a), role-address policy for local lists, validation buckets, the QA sample. |

Details and the file routing table: `references/framework-notes.md`.

## Workflow

### 0. Pick the report mode

| Situation | Mode | Template |
|-|-|-|
| ScraperCity tools connected and the user approved the spend | Delivered | `templates/output-template.md` |
| Tools not connected, no go-ahead yet, or the user asked for a plan or quote | Plan | `templates/plan-template.md` |

In Plan mode, run the free public counts now when web access is available (NPI Registry for health practices, a state license file for trades) and use the measured count as the planning number. Never write a per-sub-area count, a match rate, a validation split or a hit rate that was not measured: those cells wait for the run, and the Run Schedule says when they arrive. The cost is a ceiling (units on the measured base x catalog price), never an expected spend built on a guessed hit rate.

### 1. Define the search

Write the search card before any call:

| Field | Example |
|-|-|
| `keyword` | ["dentist", "dental clinic", "cosmetic dentist", "pediatric dentist"] |
| `notCategory` | ["Dental laboratory", "Dental supply store"] |
| Area | Austin, TX metro |
| Must have | website, email |
| Nice to have | named contact (`hasContact`) |
| Exclude | current customers (domain and phone), dental schools |
| Scope | sub-types kept and tagged unless the user excludes them |

Keyword recipes for 30 verticals, with exclusions and the Website Finder title for each, are in `references/local-category-recipes.md`.

### 2. Split the geography

A metro becomes a list of sub-cities; a state becomes its cities or counties; a dense city core becomes map boxes. Lists for 15 large metros and the box-grid method are in `references/metro-split-and-geo-recipes.md`. The Local Business Database accepts up to 2,000 entries in `location`, so one call can carry every sub-city; scrapes run one sub-city per run.

Read `searched_as` in the first database response. Every place should show a `read_as` value; a place marked `not_found` needs a different spelling or a ZIP code.

### 3. Count before pulling

Run `query_local_business_database` with `limit: 1` four times, adding one filter each time, and read `pagination.total`:

| Call | Filters added | Tells you |
|-|-|-|
| A | keyword, location, notCategory | All businesses that match |
| B | plus `hasWebsite: true` | How many can be researched or emailed at a domain |
| C | plus `hasEmail: true` | Rows ready to validate now |
| D | plus `hasContact: true` | Rows with a named contact (contact name, title, email, mobile when present) |

Then run call C once per sub-city to build the coverage table: sub-city, all (A), with website and email (C), email coverage C / A.

| Situation | Decision |
|-|-|
| C meets the target | Pull C; skip scrapes |
| C is short and B minus C is large | Pull C, then find emails for B minus C rows at their websites (step 7) |
| A sub-city's coverage is below the gap line the user sets against the metro average, or its A count is far below CBP for the county | Scrape that sub-city with Maps (step 5), lowest coverage first |
| A is 0 for a keyword | `searched_as` shows `matches_nothing`; reword the keyword |
| 503 | Narrow: fewer keywords, add a category, split the location list |

For health practices (NPI Registry, free) and licensed trades in states that publish licensee files, also match the outside list against the pool per sub-area against a coverage target the user sets: at or above it needs no scrape, below it gets one Maps run, and a sub-area still below after that gets a ZIP-level Maps split. Query the NPI Registry one city at a time (200 per page, at most 1,200 per query) and count only records whose practice address is in the sub-area. The procedure and match keys are in `references/coverage-segments-and-handoff.md` section 1.

Show the user the gap sub-areas, the planned pull and the ceiling for each paid step (scrapes, lookups, validation). Wait for a go-ahead before any paid step.

### 4. Pull with cursor paging

`check_wallet`, then page call C (or B if you will find emails) with `limit: 100`, `after: "0"`, then each `pagination.next_after` until null. Add `excludeDelivered: true` when the account has pulled this search before and only new businesses are wanted. Save each page with `source = local_db` and the query fingerprint in `source_detail`.

### 5. Fill gaps with Maps and Yelp

For each gap sub-city, run `scrape_maps` with 2-3 `searchStringsArray` terms, `locationQuery` set to the sub-city, and `maxCrawledPlacesPerSearch` capped at 60 or less, since Google documents 60 results as the most one text search returns (the worked example uses 40). The ceiling is terms x cap x $0.0099. The start response can include a `local_business_database` block with matches already in the database that the account does not have; pull those first. If a term returns at its cap, the sub-city holds more: split it (neighborhoods, ZIP codes) before raising the cap. When the sub-city's outside-list or database count is already above the per-term cap, run it by ZIP from the start, using the ZIPs on the outside list's practice addresses.

Use `scrape_yelp` (`searchTerms`, `locations`, `searchLimit`) for verticals where Yelp listings are dense (restaurants, beauty, home services, auto) and for any sub-city where Maps still looks thin. Ceiling: terms x locations x `searchLimit` x $0.0099. Use `scrape_angi` for home services by ZIP code when the category has an Angi slug.

Dedupe scrape rows against the pulled pool before paying for anything downstream.

### 6. Screen out chains and groups

When the user wants independents, run the screen before any paid lookup: brands over the user's chain line, a group list built at run time (the national groups' location pages for the state, the groups' own announcements of supported offices, names the user sends), homepage text naming a group ("supported by", "affiliated with") when web access is available, and NPI officials with corporate titles. Every dropped row records its signal in `independence`. A `corporate` call outcome adds the parent to the list. Signals and sources: `references/coverage-segments-and-handoff.md` section 1c.

### 7. Find owners and missing emails

When owner names are wanted, try the sources in order: the state entity registry where it lists principals (search the legal name from the NPI record or license file), the NPI authorized official titled Owner, President or DDS/DMD, then a database or Website Finder contact titled Owner. For health practices, confirm the name against that person's own NPI individual record. A registered agent or office manager never goes in `owner_name`. Conflict rule and the `owner_key` that sends one email per owner while the call file keeps every location: `references/coverage-segments-and-handoff.md` section 1b.

Then fill missing emails:

| Row has | Tool | Price |
|-|-|-|
| Website only, without an email or contact name | `scrape_website_finder` with the domains and one `jobTitle` from the category recipe ("Owner", "Office Manager", "Practice Manager") | $0.0499 per contact found |
| Website and a contact name, no email | `find_emails` with `first_name`, `last_name`, `domain` | $0.05 per email found, free if not found |
| No website | Drop from an email list; keep in a phone-only file if the user calls | $0 |

Leave `autoValidateEmails` off; every email is validated once in step 9.

### 8. Filter, normalize, dedupe, suppress

Keep rows with a website and an email. Normalize per `references/list-quality-standard.md` section 3: phone to E.164, domain to registrable form (blank for facebook.com, yelp.com and other platform hosts), ZIP as text, `business_name_key`. Dedupe with the local-business keys: domain, then phone, then name key plus postal code, then name key plus street. Decide the chain policy with the user: one row per location (key on phone) or one row per brand (key on domain). Two locations that share one email always collapse to one row for email. Apply suppression: current customers, open deals, unsubscribes, past bounces, and anyone contacted inside the cool-off window the user sets.

### 9. Validate and route

Send every unique email to `validate_emails`. `valid` rows form the main CSV. Role addresses (`info@`, `office@`, `contact@`) stay in the main file on a local list, since the owner often reads them. The validator's `valid_catch_all` result maps to the `catch_all` bucket: a separate file in its own campaign, paused when its hard bounces pass 2% over 200 sends (Alex Berman's 2% line, Instantly's 200-send window). `unknown` is re-validated once. `invalid` and `disposable` are removed and added to the blocklist.

### 10. Segment, sample and hand off

1. Tag every row with `segment` from fields already pulled: `named_contact` or `role_inbox`, plus a situation tag that matches the offer (`low_rating`, `few_reviews`, `high_rated_busy`, `new_license`, `multi_location`). Rules and the offer each tag fits: `references/coverage-segments-and-handoff.md` section 2. The first campaign sends `named_contact` rows in the offer's segment first.
2. Open a random sample of main-file rows (size and pass line are the user's settings; the worked example uses 20) and record the result in the Checks table: category fit, open at the listed address, website is the business's own domain, phone E.164, owner name confirmed when owners were wanted, each as "N of M". Misses that repeat on one check mean the filter or normalizer is wrong: fix it and re-run, rather than patching rows.
3. Map columns for the sequencer and, when the user calls, the dialer with the outcome field set up before the first call block (section 3 and 4 of the same reference). Outcomes feed back: the sub-area with the highest `wrong_number` plus `closed` share gets a fresh Maps pull.
4. Write the CSV with the columns in Output Format, the catch-all file, the call file if the user phones, and the report from the template for the mode. Run `scripts/check-output.py`.

## ScraperCity Implementation

| Step | Tool | Price (catalog) |
|-|-|-|
| Balance and plan | `check_wallet` | Free |
| Count and pull | `query_local_business_database` | Included on Growth and Scale; 100,000 new businesses a day |
| Maps gap fill | `scrape_maps` | $0.0099 per business |
| Yelp gap fill | `scrape_yelp` | $0.0099 per result |
| Home services by ZIP | `scrape_angi` | $0.0099 per listing |
| Email at the business website | `scrape_website_finder` | $0.0499 per contact found |
| Email from a contact name | `find_emails` | $0.05 per email found, free if not found |
| Validation | `validate_emails` | $0.00169 per email |
| Owner mobile, if asked | `find_mobiles` (Mobile Finder) | $0.25 per number found, free if not found |

### Calls

Count (call C):

```json
{"keyword": ["dentist", "dental clinic", "cosmetic dentist", "pediatric dentist"],
 "location": ["Austin TX", "Round Rock TX", "Cedar Park TX", "Georgetown TX", "Pflugerville TX",
              "Leander TX", "Kyle TX", "Buda TX", "San Marcos TX", "Lakeway TX"],
 "notCategory": ["Dental laboratory", "Dental supply store"],
 "hasWebsite": true, "hasEmail": true, "limit": 1}
```

Pull: the same body with `"limit": 100, "after": "0"`, then `pagination.next_after`. CLI: `npx scrapercity db-local` with the keyword, location (semicolon separated), has-website and has-email flags. REST: `GET` or `POST /api/v1/database/local-businesses`; use POST for long location lists.

Maps for one gap sub-city:

```json
{"searchStringsArray": ["dentist", "dental clinic"], "locationQuery": "Kyle, TX", "maxCrawledPlacesPerSearch": 40}
```

Yelp:

```json
{"searchTerms": ["dentist"], "locations": ["San Marcos, TX", "Georgetown, TX"], "searchLimit": 30}
```

Website Finder for Maps rows with a website and no email:

```json
{"domains": ["kylefamilydental.example", "budasmiles.example"], "jobTitle": "Office Manager", "autoValidateEmails": false}
```

### Worked cost estimate

Dentists in the Austin metro, 10 sub-cities, database first, Maps in 4 thin sub-cities, Yelp in 2:

| Item | Units | Unit price | Cost |
|-|-:|-:|-:|
| Local Business Database counts and pull | 768 businesses | Included in Growth | $0.00 |
| scrape_maps, 4 sub-cities x 2 terms x 40 cap (ceiling 320) | 228 returned | $0.0099 | $2.26 |
| scrape_yelp, 1 term x 2 locations x 30 (ceiling 60) | 58 returned | $0.0099 | $0.57 |
| Website Finder on 26 domains with no email | 15 contacts found | $0.0499 | $0.75 |
| validate_emails after screening, dedupe and suppression | 713 emails | $0.00169 | $1.20 |
| Total | | | $4.78 |

The ceiling shown before the scrapes was $3.17 (Maps) + $0.59 (Yelp) + $1.37 (validation of up to 810 emails) = $5.13, shown before any paid step, so it waited for a yes. The Website Finder ceiling ($1.30 for 26 domains) was shown and approved after the scrapes, once the domain count was known. Cost per send-ready business in the example: $4.78 / 545 = $0.009.

### Error handling

| Response | Action |
|-|-|
| 403 or a plan error on the database | The Local Business Database needs Growth or Scale; offer the scrape-only path (Maps and Yelp per sub-city) with its ceiling |
| `searched_as` place `not_found` | Respell the place, add the state, or use ZIP codes |
| `searched_as` keyword `matches_nothing` | Use the category name customers use on Maps; try `category` instead |
| Empty search with a `lead_database` block | The Lead Database has 100+ people for that search; consider it for professional firms |
| 400 on `box` | Use `minLat,minLng,maxLat,maxLng` with min below max |
| Maps run returns at its cap for a term | Split the sub-city into ZIP codes before raising the cap |
| 503 | Fewer keywords, smaller location list, or add a category |

## Output Format

Files:

1. `local-[category]-[area]-[date].csv`: valid emails only, one row per owner when owners were found (per inbox otherwise), with the business columns from `references/list-quality-standard.md` section 2b plus `subtype`, `independence`, and `owner_name`, `owner_check`, `owner_key` when owners were wanted.
2. `-catch-all.csv`, and `-call-file.csv` when the user phones: one row per location phone, same columns plus an empty `call_outcome`.
3. The report, from `templates/output-template.md` (Delivered) or `templates/plan-template.md` (Plan).

Report sections, in order:

| Delivered | Plan |
|-|-|
| Short Answer, Search Definition, Coverage, Funnel, Validation Results, Segments, Cost, Checks, Output Columns, Next Steps | Short Answer, Decisions, Search Definition, Coverage, Segments, Cost, Checks, Run Schedule, Output Columns |

Rules for what the reader gets:

- **Answer first.** Short Answer is the first section: how many, what it costs, how it is checked, what to send first. Cost leads with the all-in figure for the user's plan status (plan price plus usage above its credit), then the usage ceiling, then per-run prices for gap scrapes. Hand work is listed with its row counts, never with invented hours.
- **One status line.** "Status: Plan" or "Status: Delivered" once under the title says what ran and when. It is not repeated in sections, table titles or notes.
- **Each fact once.** Coverage shows one row per gap sub-area plus one row for the rest; the funnel is the only place counts flow; Cost carries the source results (new rows and cost per new); Output Columns carries the example values, so there is no sample-row table; the hand-check results sit in the Checks table.
- **Inputs a person chooses, not API detail.** Category words, areas, exclusions and filters in plain words. No tool ids, parameter names, endpoints, request bodies, internal file paths or names of other builds. A handoff names the product and the step ("Mobile Finder on owner emails, $0.25 per number found").
- **Every threshold carries its source or says it is the user's setting.** Example: "pause at 2% hard bounces over 200 sends (Alex Berman's line, Instantly's 200-send window)"; "coverage target: yours". Segment cutoffs are the user's.
- **Plan mode has no invented numbers.** Only measured counts (with the date and source), catalog prices and arithmetic on them. No decimal shares, no projected funnel or validation split.
- **Every date the user acts on is written.** Plan: a Run Schedule with dates and who approves each paid step. Delivered: dated Next Steps with the sequencer and dialer import columns and the call outcome values.
- **Only the job.** Legal commentary, a frameworks list, a self-grading checklist and vendor pitches all stay out.

## Quality Check

- [ ] The mode matches what ran: Delivered only after the tools ran and the user approved; otherwise Plan.
- [ ] Plan: every count is measured (source and date) or left to a dated step; the cost is a ceiling on catalog prices; decisions list every user setting.
- [ ] Delivered: count calls A to D ran before any pull or scrape, coverage rows sum to the total, and scrapes ran only in gap sub-areas with a stated cap.
- [ ] NPI queries ran one city at a time, none at the 1,200-record limit; sub-areas above the per-term Maps cap ran by ZIP.
- [ ] The independence screen ran before any paid lookup, and every dropped row names its signal.
- [ ] Every `owner_name` comes from a source that names the owner; conflicts are marked.
- [ ] Every main-file row has a website, a domain (or a noted platform host), `email_status = valid` and an E.164 phone; the funnel and validation buckets reconcile; catch-all rows are in their own file.
- [ ] Segments list each tag with its rule and send order (and counts when Delivered).
- [ ] Every threshold in the report names its source or the user.
- [ ] `check_wallet` ran and every paid step had a go-ahead.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| One Maps search across a metro | Results are capped per search; suburbs go missing | Split into sub-cities; split again when a run hits its cap |
| Scraping before counting the database | Pays for rows already included in the plan | Database first, scrapes only for gaps |
| Raising `maxCrawledPlacesPerSearch` to 500 on 4 terms | Ceiling of 2,000 places, $19.80, mostly duplicates | Cap at 60 or less per term and split the area instead |
| Keeping Facebook pages as websites | No domain to search or validate against | Blank the domain for platform hosts; keep the URL |
| Deduping only on name | "Smile Dental" exists in five suburbs | Keys in order: domain, phone, name key plus postal code |
| Dropping `info@` addresses | On local lists the owner often reads them | Keep role addresses on local lists; validate them |
| Sending catch-all rows with the valid file | Small-business hosting often accepts all mail, then bounces | Separate file and campaign; pause at 2% hard bounces over 200 sends |
| Writing projected counts per sub-area in a plan | Invented numbers read as measured data, and the plan loses trust when the run differs | Measure the free counts (NPI Registry, license files) or leave the cell to a dated run step |
| One NPI query for a whole state or metro | `skip` stops at 1,000, so the query silently stops at 1,200 records | One query per city; split by ZIP any city that reaches 1,200 |
| Calling a brand independent because it has few locations | Groups can keep the original practice name (Heartland Dental lists supported offices under their own names) | Group lists, homepage text and the `corporate` call outcome in the independence screen |
| Writing the office manager or registered agent as the owner | First-name copy and calls go to the wrong person | `owner_name` only from a source that names the owner; others go to `contact_name` |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or the routing table. |
| `references/metro-split-and-geo-recipes.md` | Splitting a metro or state, building map boxes, deciding where to scrape, cursor paging and dedupe for local rows. |
| `references/local-category-recipes.md` | Keywords, exclusions, Website Finder titles and Yelp or Angi terms for 30 verticals. |
| `references/coverage-segments-and-handoff.md` | NPI Registry and license-file coverage checks, owner-name sources, the independence screen, situation segments, call outcomes, sequencer and dialer mapping, refresh cadence. |
| `references/list-quality-standard.md` | Business columns, normalization, dedupe keys, validation buckets (shared). |
| `references/deliverability-primer.md` | Catch-all routing and bounce stop lines (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling, retries (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database rules (shared). |
| `templates/output-template.md` | Writing a Delivered report. |
| `templates/plan-template.md` | Writing a Plan when the tools are not connected or spend is not approved. |
| `examples/worked-example.md` | A Delivered list of dentists in the Austin metro. |
| `examples/plan-example.md` | A Plan for independent dentists in the Denver metro, built on measured NPI counts. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `tam-builder` to size every business in the market first.
- `scrapercity-local-business-database` for every database parameter.
- `cold-email-list` to carry this CSV into a sequencer with copy columns.
- `email-list-cleaner` to re-validate the list before a later re-launch.
- `decision-maker-finder` for named managers at multi-location groups.
- `mobile-appender` for owner mobiles with line-type and suppression checks.
- `cold-email-copywriting` for the first email to one sub-segment.
