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
  tags: [local-business, google-maps, yelp, local-business-database, smb, email-validation]
  related_skills: [tam-builder, scrapercity-local-business-database, email-list-cleaner, cold-email-list, decision-maker-finder, mobile-appender, cold-email-copywriting]
  frameworks:
    - "US Census Bureau - County Business Patterns as an establishment count benchmark"
    - "Google - Places Text Search returns at most 60 results per query"
    - "FTC - CAN-SPAM Act compliance guide"
    - "Google, Yahoo and Microsoft - bulk sender requirements (2024-2025)"
    - "Alex Berman - one niche, one result, small test batches"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, scrapercity-agent-patterns.md, list-quality-standard.md, deliverability-primer.md, outbound-compliance-primer.md]
---

# Local Business List

## Overview

This skill produces a CSV of local businesses in one category and area where every row has a website, an email that passed validation, a phone in E.164, a full address, and a named contact where one exists. A short report shows the geography split, the counts per sub-area, what each source added, the cleaning funnel and the cost.

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
| Plan level | The Local Business Database needs Growth ($149/mo) or Scale | Run `check_wallet` and read the plan; Starter goes scrape-only |

## Authoritative Foundations

| Source | What it contributes |
|-|-|
| US Census Bureau, County Business Patterns (CBP) | Establishment counts by NAICS code and county. Used as an outside benchmark: a database count far below the CBP count for the same county says the sub-area needs a scrape. |
| Google Maps Platform, Places Text Search | Google documents that a text search returns at most 60 results across all pages. A single Maps search over a large metro returns a capped slice, which is why this skill splits areas and treats a run that hits its cap as a sign to split further. |
| FTC CAN-SPAM guide | Covers business email with no B2B exemption: honest headers and subject, a physical address, a working opt-out honored within 10 business days. Applies to every row on this list. |
| Google, Yahoo, Microsoft sender requirements (Feb 2024, May 2025) | Remove invalid recipients and keep complaints low. Local lists carry many small-host and catch-all domains, so validation and a catch-all cap are required before sending. |
| Alex Berman | Tight niches beat broad lists: one vertical, one result, about 100 emails per segment as a first test before scaling (Lean B2B interview). A list of every business in a city is the input; the campaign starts with one sub-segment. |
| `references/list-quality-standard.md` | Business columns (section 2b), dedupe keys for local businesses (section 4a), role-address policy for local lists, validation buckets. |

Details and the file routing table: `references/framework-notes.md`.

## Workflow

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
| C is short and B minus C is large | Pull C, then find emails for B minus C rows at their websites (step 6) |
| A sub-city's coverage is under the metro average by 5+ points (house starting point, 2026-10), or its A count is far below CBP for the county | Scrape that sub-city with Maps (step 5) |
| A is 0 for a keyword | `searched_as` shows `matches_nothing`; reword the keyword |
| 503 | Narrow: fewer keywords, add a category, split the location list |

Show the user the coverage table, the planned pull, any scrape ceilings and the validation estimate. Wait for a go-ahead when paid steps exceed $5.

### 4. Pull with cursor paging

`check_wallet`, then page call C (or B if you will find emails) with `limit: 100`, `after: "0"`, then each `pagination.next_after` until null. Add `excludeDelivered: true` when the account has pulled this search before and only new businesses are wanted. Save each page with `source = local_db` and the query fingerprint in `source_detail`.

### 5. Fill gaps with Maps and Yelp

For each gap sub-city, run `scrape_maps` with 2-3 `searchStringsArray` terms, `locationQuery` set to the sub-city, and `maxCrawledPlacesPerSearch` capped (start at 40). The ceiling is terms x cap x $0.0099. The start response can include a `local_business_database` block with matches already in the database that the account does not have; pull those first. If a term returns at its cap, the sub-city holds more: split it (neighborhoods, ZIP codes) before raising the cap.

Use `scrape_yelp` (`searchTerms`, `locations`, `searchLimit`) for verticals where Yelp listings are dense (restaurants, beauty, home services, auto) and for any sub-city where Maps still looks thin. Ceiling: terms x locations x `searchLimit` x $0.0099. Use `scrape_angi` for home services by ZIP code when the category has an Angi slug.

Dedupe scrape rows against the pulled pool before paying for anything downstream.

### 6. Find missing emails

| Row has | Tool | Price |
|-|-|-|
| Website, no email, no contact name | `scrape_website_finder` with the domains and one `jobTitle` from the category recipe ("Owner", "Office Manager", "Practice Manager") | $0.0499 per contact found |
| Website and a contact name, no email | `find_emails` with `first_name`, `last_name`, `domain` | $0.05 per email found, free if not found |
| No website | Drop from an email list; keep in a phone-only file if the user calls | $0 |

Leave `autoValidateEmails` off; every email is validated once in step 8.

### 7. Filter, normalize, dedupe, suppress

Keep rows with a website and an email. Normalize per `references/list-quality-standard.md` section 3: phone to E.164, domain to registrable form (blank for facebook.com, yelp.com and other platform hosts), ZIP as text, `business_name_key`. Dedupe with the local-business keys: domain, then phone, then name key plus postal code, then name key plus street. Decide the chain policy with the user: one row per location (key on phone) or one row per brand (key on domain). Two locations that share one email always collapse to one row for email. Apply suppression: current customers, open deals, unsubscribes, past bounces, contacted in the last 90 days.

### 8. Validate and route

Send every unique email to `validate_emails`. `valid` rows form the main CSV. Role addresses (`info@`, `office@`, `contact@`) stay in the main file on a local list, since the owner often reads them. `valid_catch_all` goes to a separate file sent at no more than 10% of daily volume. `unknown` waits 72 hours for one retry. `invalid` and `disposable` are removed and added to the blocklist.

### 9. Export and report

Write the CSV with the columns in Output Format, a catch-all file, a phone-only file if requested, and the report from `templates/output-template.md`. Run `scripts/check-output.py`.

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
| Validation | `validate_emails` | $0.0072 per email |
| Owner mobile, if asked and lawful | `find_mobiles` | $0.25 per number found, free if not found |

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
| validate_emails after dedupe and suppression | 734 emails | $0.0072 | $5.28 |
| Total | | | $8.86 |

The ceiling shown before the scrapes was $3.17 (Maps) + $0.59 (Yelp) + $5.83 (validation of up to 810 emails) = $9.59, over $5, so it waited for a yes. The Website Finder ceiling ($1.30 for 26 domains) was shown and approved after the scrapes, once the domain count was known. Cost per send-ready business in the example: $8.86 / 561 = $0.016.

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

1. `local-[category]-[area]-[date].csv`: valid emails only, with the business columns from `references/list-quality-standard.md` section 2b: `business_name`, `business_name_key`, `category`, `website`, `domain`, `email`, `email_status`, `email_validated_at`, `is_role`, `phone`, `contact_name`, `contact_title`, `street`, `city`, `state`, `postal_code`, `country`, `rating`, `reviews`, `sub_area`, `source`, `source_detail`, `pulled_at`, `segment`.
2. `local-[category]-[area]-[date]-catch-all.csv` and, if requested, `-phone-only.csv` for businesses with a phone and no website.
3. The report from `templates/output-template.md`: search definition, geography split with counts, count check, source results, cleaning funnel, validation, cost, schema, sample rows, next steps.

## Quality Check

- [ ] Count calls A to D ran and appear in the report before any pull or scrape.
- [ ] Geography table lists every sub-area with its count; the counts sum to the total.
- [ ] Scrapes ran only in sub-areas flagged as gaps, each with a stated cap and ceiling.
- [ ] Every row in the main file has a website, a domain (or a noted platform host), an email with `email_status = valid`, and a phone in E.164.
- [ ] Funnel adds up stage by stage; every drop has a reason.
- [ ] No duplicate phone, domain-plus-location or email in the main file; the chain policy is stated.
- [ ] Validation buckets sum to the number validated; catch-all rows are in their own file.
- [ ] `check_wallet` ran and paid steps over $5 had a go-ahead.
- [ ] `scripts/check-output.py report.md` prints PASS.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| One Maps search for a whole metro | Results are capped per search; suburbs go missing | Split into sub-cities; split again when a run hits its cap |
| Scraping before counting the database | Pays for rows already included in the plan | Database first, scrapes only for gaps |
| Raising `maxCrawledPlacesPerSearch` to 500 on 4 terms | Ceiling of 2,000 places, $19.80, mostly duplicates | Cap at 40-60 per term and split the area instead |
| Keeping Facebook pages as websites | No domain to search or validate against | Blank the domain for platform hosts; keep the URL |
| Deduping only on name | "Smile Dental" exists in five suburbs | Keys in order: domain, phone, name key plus postal code |
| Dropping `info@` addresses | On local lists the owner often reads them | Keep role addresses on local lists; validate them |
| Sending catch-all rows with the valid file | Small-business hosting often accepts all mail, then bounces | Separate file, 10% of daily volume |
| Texting the mobile numbers from `contact_mobile` | Marketing texts to mobiles need prior express written consent under the TCPA | Email, or manual calls after a Do Not Call scrub |

## Execution Artifacts

| File | Open it when |
|-|-|
| `references/framework-notes.md` | You need the source behind a rule or the routing table. |
| `references/metro-split-and-geo-recipes.md` | Splitting a metro or state, building map boxes, deciding where to scrape, cursor paging and dedupe for local rows. |
| `references/local-category-recipes.md` | Keywords, exclusions, Website Finder titles and Yelp or Angi terms for 30 verticals. |
| `references/list-quality-standard.md` | Business columns, normalization, dedupe keys, validation buckets (shared). |
| `references/deliverability-primer.md` | Catch-all cap and bounce stop lines (shared). |
| `references/outbound-compliance-primer.md` | CAN-SPAM, TCPA and country rules (shared). |
| `references/scrapercity-agent-patterns.md` | Wallet checks, polling, retries (shared). |
| `references/scrapercity-catalog.md` | Prices and parameters (shared). |
| `references/scrapercity-platform.md` | Plans and database rules (shared). |
| `templates/output-template.md` | Writing the report. |
| `examples/worked-example.md` | A finished list of dentists in the Austin metro. |
| `scripts/check-output.py` | Final gate: `python3 scripts/check-output.py report.md`. |

## Related Skills

- `tam-builder` to size every business in the market first.
- `scrapercity-local-business-database` for every database parameter.
- `cold-email-list` to carry this CSV into a sequencer with copy columns.
- `email-list-cleaner` to re-validate the list before a later re-launch.
- `decision-maker-finder` for named managers at multi-location groups.
- `mobile-appender` for owner mobiles with the compliance checks.
- `cold-email-copywriting` for the first email to one sub-segment.
