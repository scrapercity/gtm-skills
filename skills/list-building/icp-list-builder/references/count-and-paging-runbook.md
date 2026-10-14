# Count and Paging Runbook

How to count before pulling, how to page large pulls with cursors, what to do when a call fails, how to size a market from Census firm data, and how to handle size-band edges. Applies to `query_lead_database` and, with the parameter names swapped, `query_local_business_database`.

## 1. The count call

Send the full filter set with `limit: 1`. The response carries a `pagination` object; the CLI prints it as "N total leads, page P of T" and, when more rows exist, the cursor to continue from. Fields used here:

| Field | Meaning |
|-|-|
| `pagination.total` | Records matching the filters |
| `pagination.page`, `pagination.totalPages` | Page position when paging by `page` |
| `pagination.next_after` | Cursor for the next batch; null when there are no more rows |
| `search_translation` | Present when you passed `url`: filters applied, approximated, not supported |

A count call returns one record, and every record returned is saved to the account. One record per count call is negligible against the 100,000 daily allowance.

## 2. Sizing the pull

Rows are lost between the raw pull and the send-ready file at each stage below. Record the loss per stage on every list, and size the next pull from the measured yield (send-ready rows divided by pulled rows on the last comparable list).

| Stage | What drives the loss |
|-|-|
| Normalization drops | Rows with no name or broken email syntax |
| Dedupe within the pull | The same person under two title variants |
| Suppression (customers, past sends, unsubscribes) | How much of the market the user has already worked |
| Per-domain cap | The user's cap and the company size band; larger companies lose more |
| Validation: not valid (invalid, catch-all, unknown) | Source age and how many catch-all domains the segment has |

Rows to pull = target send-ready rows divided by the measured yield, rounded up to the next 100 (one page). At a 75% yield, 1,500 send-ready rows means pulling 2,000. With no earlier list to measure, pull page by page and stop when the send-ready count reaches the target.

## 3. Widen or tighten

Change one filter per recount so you know which one changed the count.

Widening order (count too low):

1. Add title synonyms from `title-synonyms-and-exclusions.md`.
2. Swap `title` for `seniority` plus `department`.
3. Widen headcount one band on each side.
4. Drop the least important keyword.
5. Remove `industry` and keep `keywords`.
6. Add neighboring countries the seller can serve.
7. Remove `hasEmail` only if the plan is to find emails with `find_emails` ($0.05 per email found).

Tightening order (count too high):

1. Add `seniority`.
2. Narrow headcount.
3. Add a business-model keyword (saas, b2b, marketplace).
4. Add `notKeywords` for segments the seller does not serve.
5. Split by `state` or `companyState` and run one region at a time.
6. Add `revenueMin` or `revenueMax` if the seller prices by revenue.

## 4. Cursor paging

Use `after` for any pull above 100 rows. Cursor paging returns records after a given id, so new records added between calls do not change what you get.

```text
filters = {...}                 # identical on every call
after = "0"
pulled = []
while len(pulled) < planned_rows:
    r = query_lead_database({**filters, "limit": 100, "after": after})
    pulled.extend(r["data"])
    after = r["pagination"].get("next_after")
    if not after:
        break
save pulled to raw file, with source = lead_db and source_detail = fingerprint(filters)
```

REST, the same loop with curl:

```bash
curl -s -H "Authorization: Bearer $SCRAPERCITY_API_KEY" \
  "https://app.scrapercity.com/api/v1/database/leads?title=VP%20Sales&minEmployees=50&maxEmployees=200&country=United%20States&hasEmail=true&limit=100&after=0"
# read pagination.next_after from the JSON and send it as after on the next call
```

The CLI command `db-leads` prints the next cursor after each page.

Rules:

- Never change filters mid-loop. A changed filter with an old cursor gives an undefined slice.
- With `excludeDelivered: true`, use `after` or keep `page: 1`. Page numbers change as records become delivered.
- Save each page to disk as it arrives. If the run stops, restart from the last saved `next_after`.

## 5. Daily allowance planning

The Lead Database allows 100,000 new leads a day on Growth and Scale. Records the account already has do not count again.

| Planned new rows | Days needed | Note |
|-:|-:|-|
| 2,000 | 1 | Typical campaign list |
| 25,000 | 1 | 250 calls of 100 |
| 100,000 | 1 | Uses the full day |
| 250,000 | 3 | Split by region or size band, one slice per day |

For recurring pulls (a weekly fresh list), run the same filters with `excludeDelivered: true` and `after: "0"` each time. You receive only people the account has not seen.

## 6. Errors and fixes

| Symptom | Cause | Fix |
|-|-|-|
| 401 | Key missing or wrong | Ask for `SCRAPERCITY_API_KEY`; do not retry. |
| 402 | Wallet too low for a paid step | `check_wallet`, report the shortfall. Database pulls count against the daily allowance; validation and finder steps draw on the wallet. |
| 403 | Plan without database access, account cancelled, or a charge processing | Tell the user; the Lead Database needs Growth or Scale. |
| 429 | Rate limit | Back off, then retry once. Scale has higher rate limits. |
| 503 | The search ran too long | Add a location, a size band or fewer titles; split the query; retry. |
| `pagination.total` = 0 with a filter you expected to work | Label mismatch | Remove filters one at a time; prefer `keywords` over `industry`. |
| `search_translation.not_supported` lists a filter | The pasted URL used a filter the database cannot apply | Re-express it with native parameters or accept the wider result and say so. |
| Rows returned with titles outside the family | Partial matching | Add the offending words to `notTitle`, recount. |
| Same people as last month's list | No suppression and no `excludeDelivered` | Add `excludeDelivered: true` and apply the past-sends suppression list. |

## 7. Validation run handling

`validate_emails` is a run, not an instant response:

1. Submit up to a few thousand emails per call. Note the `runId`.
2. Poll `check_run_status` until the status moves from RUNNING to SUCCEEDED, FAILED or CANCELLED.
3. On SUCCEEDED, `download_results` with an `outputPath` inside the working folder.
4. On FAILED, check `list_runs` for the error, resubmit once. A 409 means the same submission is already running; reuse it.
5. Read the CSV header, map raw results into the buckets in `references/list-quality-standard.md` section 5, and keep the raw value in `email_status_raw`.

## 8. Sanity checks before you call it done

- Pulled rows equals the sum of page sizes saved to disk.
- No two rows share an email after dedupe.
- Validation buckets add up to the number submitted.
- The funnel in the report starts at `pagination.total` and ends at the send-ready count, with a reason on every drop.

## 9. Company counts from Census firm data

The Census Bureau's Statistics of U.S. Businesses (SUSB) counts US firms by industry (NAICS) and enterprise employment size. Use it two ways: as the company count in a plan report when no ScraperCity call can run, and as the benchmark for the deduped database count in a run report.

1. Download the "U.S. & states, NAICS, detailed employment sizes" table from the SUSB 2022 tables page (2022 data, released April 2025).
2. Keep State `00` (United States) and the NAICS codes of the segment.
3. Sum the Firms column over the enterprise size classes that cover the band. Classes run 200-299, 300-399, 400-499, 500-749, 750-999, 1,000-1,499, 1,500-1,999, 2,000-2,499, 2,500-4,999, 5,000+. When the user's band edge falls inside a class, use the nearest class edge and say which.
4. A firm is counted in every industry where it has an establishment, and its size class counts all of the firm's employees. A sum across several NAICS codes is therefore a ceiling, and the employment counts include hourly staff.
5. The size classes give tier sizes by band before any pull (for example 200-499 versus 500-1,999).

Firm counts, 200-1,999 employees, SUSB 2022:

| NAICS | Industry | 200-499 | 500-1,999 | 200-1,999 |
|-|-|-:|-:|-:|
| 311 | Food Manufacturing | 660 | 435 | 1,095 |
| 3121 | Beverage Manufacturing | 77 | 56 | 133 |
| 493 | Warehousing and Storage | 557 | 602 | 1,159 |
| 484 | Truck Transportation | 561 | 387 | 948 |
| 488510 | Freight Transportation Arrangement (brokers, forwarders) | 155 | 130 | 285 |
| 5112 | Software Publishers | 277 | 232 | 509 |
| 42 | Wholesale Trade | 3,192 | 2,016 | 5,208 |

People in a plan report: firms x 5 to 11, the buying-group size in Gartner's B2B Buying Report (2022 survey). It bounds the people who decide, not the people the database holds with an email; the step-4 counts measure that.

## 10. Band edges in hourly-workforce industries

Employee counts in B2B data read low for firms whose staff are mostly hourly: Pew Research Center (January 2024) found 10% of US adults with a high school education or less use LinkedIn, against 53% of college graduates. Warehousing, manufacturing, retail, healthcare delivery, construction and hospitality firms in the user's band can show up below its floor.

1. Count the band just below the floor as its own query, same filters (for a 200 floor, 100-199).
2. During the site check, read the headcount the company states on its site, in a press release or in a job posting.
3. A below-floor company joins when that stated headcount is inside the band; one with no stated figure stays out. A company inside the band whose stated headcount is above the ceiling leaves.
4. Record the figure and its URL in `company_employees` and the site-check column, so the tier uses the corrected size.

## Sources

- ScraperCity platform facts (paging, `excludeDelivered`, daily allowances, 503 handling): references/scrapercity-platform.md
- ScraperCity catalog (error codes, run lifecycle, validator price): references/scrapercity-catalog.md
- ScraperCity CLI source (`db-leads` output and cursor hint): https://github.com/scrapercity/scrapercity-cli
- Yahoo Sender Hub, remove invalid recipients promptly: https://senders.yahooinc.com/best-practices/
- US Census Bureau, 2022 SUSB annual data tables (detailed employment sizes, released April 2025): https://www.census.gov/data/tables/2022/econ/susb/2022-susb-annual.html
- US Census Bureau, SUSB detailed employment sizes file used for the table above: https://www2.census.gov/programs-surveys/susb/tables/2022/us_state_naics_detailedsizes_2022.xlsx
- Pew Research Center, Americans' Social Media Use (January 31, 2024; LinkedIn use by education): https://www.pewresearch.org/internet/2024/01/31/americans-social-media-use/
- Gartner, B2B Buying Report (buying groups of five to 11): https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
