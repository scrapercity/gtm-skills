---
name: scrapercity-local-business-database
description: >-
  Plans and runs pulls from the ScraperCity Local Business Database: Google
  Maps style keyword and location searches, category and rating filters, map
  box tiling for metros, named-contact pulls, daily feeds of new businesses,
  and when to fall back to the Google Maps, Yelp or Angi scrapers. Produces a
  local pull plan with filters, counts, segments by rating and reviews, and a
  cost table. Use when the user wants dentists, plumbers, restaurants, salons
  or any local business by city, state, ZIP or map area, or pastes a Google
  Maps search URL.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: scrapercity
  tags:
    - local-business
    - google-maps
    - smb
    - local-leads
    - database
    - mcp
  related_skills:
    - using-scrapercity-skills
    - scrapercity-mcp
    - scrapercity-cli
    - scrapercity-api
    - local-business-list
    - scrapercity-lead-database
    - email-list-cleaner
    - cold-email-list
    - cold-calling
  frameworks:
    - "ScraperCity - Local Business Database API reference (scrapercity npm package 1.0.17)"
    - "Google Business Profile - category guidelines"
    - "BrightLocal - Local Consumer Review Survey 2026"
    - "USGS - distance covered by a degree of latitude and longitude"
    - "Google - Email sender guidelines (2024)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - list-quality-standard.md
    - scrapercity-agent-patterns.md
---

# ScraperCity Local Business Database

## Overview

This skill turns "get me every [type of business] in [place]" into a Local Business Database search that matches the right businesses, a count check, a paging plan inside the 100,000 new businesses a day allowance, and segments by rating and review count so each segment gets a message that fits its situation.

The database is included with the Growth plan ($149/mo) and up. Every business returned is saved to the account. Only new businesses count toward the daily allowance; fetching one the account already has is free. Many records carry a named contact (first name, last name, job title, email, mobile).

The mistakes it prevents:

- Paying $0.0099 per business for a `scrape_maps` run when the database returns the same search in seconds at no extra cost.
- Sending one generic email to a 4.9-star clinic with 800 reviews and a 3.1-star clinic with 9 reviews.
- A 503 on "restaurants in Texas" because the search was never narrowed by city, category or map box.
- Reading an empty result as "no market" when `searched_as` shows the place was not found, or the `lead_database` block shows 100+ people for the same search.

## When to Use

- "Find every dentist in Austin with an email."
- "Pull HVAC companies across Dallas-Fort Worth with under 50 reviews."
- "I have this Google Maps search URL, get me the businesses."
- "Give me med spas in Florida with a named owner."
- "Set up a daily feed of new roofers in Colorado."
- "Should I use the database or the Google Maps scraper?"

Use a different skill for nearby jobs:

| Job | Skill |
|---|---|
| Strategy for a local list (offer, ICP, channels) | `local-business-list` |
| B2B roles at companies of any type | `scrapercity-lead-database` |
| Cleaning and validating the emails after the pull | `email-list-cleaner` |
| Phone outreach to the businesses | `cold-calling` |
| Real estate agents, properties, owners | `scrapercity-real-estate-data` |

## Prerequisites

- Growth or Scale plan (run `check_wallet` and read `plan.name`). On Starter, use `scrape_maps`, `scrape_yelp` or `scrape_angi`.
- What the businesses do, in the words a person would type into Google Maps.
- Where: cities, states, postal codes, countries, or a map box.
- Contact needs: email, phone, website, named contact.
- Volume and cadence: one-off or daily.

## Authoritative Foundations

| Source | What it contributes |
|---|---|
| ScraperCity Local Business Database API (npm `scrapercity` 1.0.17) | Every filter, `searched_as`, the `lead_database` fallback block, `search_translation`, paging, POST for long requests, error branches, returned fields |
| `references/scrapercity-catalog.md` | Prices for the scrapers and enrichment around the database: `scrape_maps` $0.0099 per business, `scrape_yelp` $0.0099 per result, `scrape_angi` $0.0099 per listing, `validate_emails` $0.00169 per email, `find_emails` $0.05 per email found |
| Google Business Profile category guidelines | A business picks the most specific category that says what it is. Search the specific category first ("Pediatric dentist"), then the broad word ("dentist") |
| BrightLocal Local Consumer Review Survey 2026 | 68% of consumers will only use a business with 4+ stars, 31% only 4.5+, 47% will not use one with fewer than 20 reviews, 74% look for reviews written in the last three months. Basis for the rating and review segments |
| USGS | One degree of latitude is about 69 miles; one degree of longitude is about 54.6 miles at 38 degrees north. Converts a map box from degrees to miles |
| Google Email sender guidelines | Mail to these businesses lands in the same Gmail and Workspace inboxes as any other: one-click unsubscribe on bulk mail, removals within 48 hours, spam rate under 0.1% |

Routing and detail: `references/framework-notes.md`.

## Workflow

### 1. Confirm access, pick the tool

Run `check_wallet`. Then choose:

| Situation | Tool |
|---|---|
| Growth or Scale, any keyword and place | `query_local_business_database` first |
| Starter plan | `scrape_maps` ($0.0099 per business, minutes) |
| Database count is low for a place you know is dense, or the user needs today's listings | `scrape_maps` for that place; its response can include a `local_business_database` block with matches you can pull now |
| User wants Yelp reviews or Yelp-only businesses | `scrape_yelp` ($0.0099 per result) |
| Home services with Angi verification | `scrape_angi` ($0.0099 per listing, `keyword` from the Angi slug list) |

### 2. Write the search the way a person types it into Google Maps

- `keyword`: what the businesses do or are called, as an array: `["dentist"]`, `["thai restaurant", "sushi"]`. Matches business names and categories, any keyword.
- `location`: as an array, up to 2,000 places, any match: `["Austin TX", "Round Rock TX", "78701"]`. Cities, states, countries or postal codes.
- A place inside a keyword ("plumbers in Austin TX") is used as the location when `location` is empty.
- On the CLI, `--location` separates places with semicolons (`"Houston, TX; Austin, TX"`) because a place has its own commas.

Read `searched_as` in the response. `keywords[].categories` shows which categories each keyword matched; `matches_nothing: true` means no business name or category has it, so rephrase. `places[].read_as` shows how each place was read; `not_found` means drop or respell it.

### 3. Add filters

Filters narrow the keyword and location search. Full list in `references/filter-semantics.md`:

- `category` (array, a word also finds categories that contain it: "restaurant" finds "Mexican restaurant"), `notCategory` (array).
- `country` (two-letter codes: `["US"]`), `state` (string, commas for several, "TX" works), `city` (partial match), `postalCode`, `box`.
- `query` (business names and descriptions), `title` (business name, comma list, partial match).
- `minRating`, `maxRating` (1-5), `minReviews`, `maxReviews`.
- `hasEmail`, `hasPhone`, `hasWebsite`, `hasContact` (a named contact person).

### 4. Count check

Send the search with `limit: 1`. Read `pagination.total`, `searched_as`, and the one row.

| Result | Action |
|---|---|
| total 0 and a `lead_database` block | The Lead Database has 100+ people for this search (keywords read as job title or company keywords). Offer that route via `scrapercity-lead-database`, using `lead_database.filters` |
| total 0, a place `not_found` | Fix the place spelling or use `postalCode` or `box` |
| total 0, a keyword `matches_nothing` | Rephrase to the category a business would choose ("HVAC contractor", not "AC guys") |
| 1-100,000 | Pull. Show the count and the day count |
| over 100,000 | Split by state, city list or map box |

A 503 means the search ran too long. Add a category, a city, a state or a postal code, or tile with `box` (step 6).

### 5. Segment by rating and reviews

Run one count per segment so the message can match it. Bands from the BrightLocal 2026 lines (4.0 stars, 4.5 stars, 20 reviews):

| Segment | Filters | Line it sits on |
|---|---|---|
| Leaders | `minRating: 4.5`, `minReviews: 20` | Above the 4.5-star line 31% of consumers apply |
| Solid | `minRating: 4.0`, `maxRating: 4.4`, `minReviews: 20` | Between the 4.0 and 4.5 lines |
| Thin reviews | `minRating: 4.0`, `maxReviews: 19` | Under the 20-review line 47% of consumers use |
| At risk | `maxRating: 3.9`, `minReviews: 1` | Below the 4-star line 68% of consumers apply |
| No reviews | `maxReviews: 0` | No rating yet |

The five bands do not overlap; dedupe on business id anyway before sending. Opening angles per offer are in `references/segmentation-and-tiling.md`.

### 6. Tile big metros with `box`

`box` is `"minLat,minLng,maxLat,maxLng"`. For a dense category in a big metro, split the metro into equal tiles, count each with `limit: 1`, and split any tile that returns 503 into four (half the step). The USGS figures convert a step in degrees to miles (0.25 degrees is about 17 by 14 miles at 38 degrees north). A box that cannot be read returns 400. Tiling recipe and a stdlib tile generator are in `references/segmentation-and-tiling.md`.

### 7. Pull with the cursor

`limit: 100`, `after: "0"`, then `pagination.next_after` until null. For a feed of only new businesses, add `excludeDelivered: true` and keep `page` at 1 or use `after`. Long `location` lists or a long `url` go as `POST /api/v1/database/local-businesses` with a JSON body (query strings past about 16KB are refused).

### 8. QA and hand off

Check a random sample of rows (the size is your call; the example checks 20): category fits, address inside the place, rating and reviews inside the segment band, email or phone present as required. When misses share a pattern, add a `notCategory` or tighten the place before the bulk pull. Send emails to `validate_emails` before any campaign. For businesses without a named contact, run `find_emails` only where you have a person's name and the website domain.

## ScraperCity Implementation

### MCP

```json
{
  "keyword": ["dentist"],
  "location": ["Austin TX", "Round Rock TX", "Cedar Park TX", "Pflugerville TX"],
  "notCategory": ["Dental laboratory", "Dental supply store"],
  "hasEmail": true,
  "minRating": 4.0,
  "limit": 1
}
```

### CLI

```bash
npx scrapercity db-local --keyword "dentist" \
  --location "Austin, TX; Round Rock, TX; Cedar Park, TX; Pflugerville, TX" \
  --not-category "Dental laboratory" --has-email --min-rating 4 --limit 1
```

The CLI prints the total, the next cursor, how each place was read, keywords that match nothing, and the Lead Database fallback when the search finds nothing.

### REST

```bash
curl -s -G "https://app.scrapercity.com/api/v1/database/local-businesses" \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
  --data-urlencode "keyword=dentist" \
  --data-urlencode "location=Austin, TX" --data-urlencode "location=Round Rock, TX" \
  --data-urlencode "hasEmail=true" --data-urlencode "limit=100" --data-urlencode "after=0"
```

Repeat a key for several values. A Google Maps search URL goes in `url`; its keyword and place become the search, other parameters override, and the response adds `search_translation` (`applied`, `approximated`, `not_supported`). A URL with nothing usable returns 400.

### Returned fields

`title`, `category_name`, `address`, `city`, `state`, `postal_code`, `country_code`, `phone`, `website`, `emails`, `total_score` (the rating), `reviews_count`, `lat`, `lng`, and when there is a named contact: `contact_first_name`, `contact_last_name`, `contact_job_title`, `contact_email`, `contact_mobile`. The response also carries `pagination`, `rate_limit`, and when relevant `search_translation`, `searched_as`, `lead_database`.

### Database or scraper

| Factor | Local Business Database | `scrape_maps` | `scrape_yelp` | `scrape_angi` |
|---|---|---|---|---|
| Price | Included with Growth and up | $0.0099 per business | $0.0099 per result | $0.0099 per listing |
| Speed | Seconds | Minutes | Minutes | Minutes |
| Named contact fields | Yes, for many | No | No | No |
| Rating and review filters | Yes, server side | No | No | No |
| Best for | Default for any search | A live search on the Starter plan, or areas the database covers thinly | Yelp reviews | Home services |

### Worked cost estimate

Dentists in the Austin metro, `hasEmail: true`. Count check returns 1,146. 412 have a named contact.

| Line | Units | Unit price | Cost |
|---|---:|---:|---:|
| Local Business Database pull (12 calls of up to 100) | 1,146 | included in Growth | $0.00 |
| `validate_emails` (1,146 businesses, 1,388 emails) | 1,388 | $0.00169 | $2.35 |
| `find_emails` for owners named on 300 websites without a contact, ceiling if every lookup finds one | 300 | $0.05 | $15.00 |
| **Total paid, ceiling** | | | **$17.35** |

Email Finder bills only emails found, so the actual line is found emails x $0.05. The same 1,146 businesses through `scrape_maps` would cost 1,146 x $0.0099 = $11.35 before enrichment, without rating filters or named contacts. Show this table and get a go-ahead before any paid step.

## Output Format

A local pull plan in Markdown from `templates/output-template.md`:

1. **Request Summary**: business type, places, contact needs, plan.
2. **Search Spec**: parameter, value, reason.
3. **Count Check**: total, `searched_as` notes, fallback block if any.
4. **Segments**: one row per rating and review segment with filters and count.
5. **Pull Plan**: paging, excludeDelivered, tiles, days.
6. **Cost Estimate**: $ table with total.
7. **Sample QA** and **Next Steps**.

Check it with `python3 scripts/check-output.py plan.md`.

- Each fact once; every call and script written out in full (no `"..."` values, no loop described in a comment); no counts or results marked assumed. If nothing has run, say so once at the top.
- What the reader receives is the deliverable only: no internal file paths, reference section numbers or runbook IDs; another skill is named only in a handoff line that tells the user what to run next; no tables of checks that were not run (one "Not checked:" line instead); and no repeated identical rows where one template plus a list will do.

## Quality Check

- Every search row uses a parameter that exists in `query_local_business_database`.
- `country` values are two-letter codes.
- Every `box` reads as four numbers with min below max.
- A count from a `limit: 1` call is shown before the bulk pull.
- Every segment states its rating band and review band, and the segments are deduped.
- `excludeDelivered` is never paired with `page` above 1.
- The cost table uses catalog prices, and paid spend is approved first.
- Sample QA reports on-target rows as "N / M", and any shared miss pattern is fixed in the search.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|---|---|---|
| `country: ["United States"]` | Country takes two-letter codes on this database | `["US"]` |
| Keyword in slang ("AC guys") | `matches_nothing` in `searched_as` | Use the category a business picks: "HVAC contractor", "Air conditioning contractor" |
| "restaurants" statewide | 503, and one message for 40,000 kinds of restaurant | Split by cuisine `category`, by city, or tile with `box` |
| Comma-separated `--location` on the CLI | "Austin, TX" splits wrong | Use semicolons between places |
| Treating `category: ["restaurant"]` as exact | A word also finds categories that contain it, so "restaurant" pulls "Fast food restaurant" too | Add `notCategory: ["Fast food restaurant"]`, or list the specific categories you want |
| Running `scrape_maps` before checking the database | Pays $0.0099 per business for rows already included | Count in the database first |
| Ignoring `lead_database` on an empty search | Misses 100+ people the Lead Database has | Offer the Lead Database route with its filters |
| One message for every rating | A 4.9-star leader and a 3.2-star shop need different openers | Segment with `minRating`/`maxRating` and review bands |

## Execution Artifacts

| File | Use it when |
|---|---|
| `references/framework-notes.md` | You need the source behind a rule or the right reference to open. |
| `references/filter-semantics.md` | You need exact parameter behavior, `searched_as`, `lead_database`, or the field list. |
| `references/category-recipes.md` | You need a ready keyword, category and exclusion set for a vertical (50+ verticals). |
| `references/segmentation-and-tiling.md` | You need rating and review segments, message angles, or map box tiles for a metro. |
| `templates/output-template.md` | Start every local pull plan here. |
| `examples/worked-example.md` | A complete plan for dentists in the Austin metro. |
| `scripts/check-output.py` | Run on the finished plan before sending it. |
| `references/scrapercity-catalog.md` | Prices for scrapers and enrichment. |
| `references/scrapercity-platform.md` | Plans, allowance and paging rules. |
| `references/list-quality-standard.md` | Acceptance bar for the final list. |
| `references/scrapercity-agent-patterns.md` | Wallet checks and confirmation before spend. |

## Related Skills

- `local-business-list`: the strategy layer for local lists.
- `scrapercity-lead-database`: when the `lead_database` fallback appears, or the target is a role.
- `scrapercity-mcp`, `scrapercity-cli`, `scrapercity-api`: access paths.
- `email-list-cleaner`, `cold-email-list`: validation and the send-ready file.
- `cold-calling`: phone outreach to the businesses.
- `using-scrapercity-skills`: router.
