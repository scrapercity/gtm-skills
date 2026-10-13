# Count and Paging Runbook

How to count before pulling, how to page large pulls with cursors, and what to do when a call fails. Applies to `query_lead_database` and, with the parameter names swapped, `query_local_business_database`.

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

Expected losses between the raw pull and the send-ready file, as planning defaults (house standard, 2026-10; replace with your own numbers after two lists):

| Stage | Planning loss |
|-|-:|
| Normalization drops (no name, broken email syntax) | 1-3% |
| Dedupe within the pull | 1-5% |
| Suppression (customers, past sends, unsubscribes) | 0-15%, depends on how much of the market you have already worked |
| Per-domain cap of 3 | 2-10% for mid-market, more for enterprise |
| Validation: not valid (invalid, catch-all, unknown) | 10-25% |

Rule of thumb: rows to pull = target send-ready rows divided by 0.75, rounded up to the next 100. For 1,500 send-ready rows pull 2,000.

## 3. Widen or tighten

Change one filter per recount so you know which one moved the number.

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

Use `after` for any pull above 100 rows. Cursor paging returns records after a given id, so new records added between calls do not shift what you get.

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
- With `excludeDelivered: true`, use `after` or keep `page: 1`. Page numbers move as records become delivered.
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
| 429 | Rate limit | Wait 30 seconds, retry once. Scale has higher rate limits. |
| 503 | The search ran too long | Add a location, a size band or fewer titles; split the query; retry. |
| `pagination.total` = 0 with a filter you expected to work | Label mismatch | Remove filters one at a time; prefer `keywords` over `industry`. |
| `search_translation.not_supported` lists a filter | The pasted URL used a filter the database cannot apply | Re-express it with native parameters or accept the wider result and say so. |
| Rows returned with titles outside the family | Partial matching | Add the offending words to `notTitle`, recount. |
| Same people as last month's list | No suppression and no `excludeDelivered` | Add `excludeDelivered: true` and apply the past-sends suppression list. |

## 7. Validation run handling

`validate_emails` is a run, not an instant response:

1. Submit up to a few thousand emails per call. Note the `runId`.
2. Poll `check_run_status` every 30-60 seconds; status moves from RUNNING to SUCCEEDED, FAILED or CANCELLED.
3. On SUCCEEDED, `download_results` with an `outputPath` inside the working folder.
4. On FAILED, check `list_runs` for the error, resubmit once. A 409 means the same submission is already running; reuse it.
5. Read the CSV header, map raw results into the buckets in `references/list-quality-standard.md` section 5, and keep the raw value in `email_status_raw`.

## 8. Sanity checks before you call it done

- Pulled rows equals the sum of page sizes saved to disk.
- No two rows share an email after dedupe.
- Validation buckets add up to the number submitted.
- The funnel in the report starts at `pagination.total` and ends at the send-ready count, with a reason on every drop.

## Sources

- ScraperCity platform facts (paging, `excludeDelivered`, daily allowances, 503 handling): references/scrapercity-platform.md
- ScraperCity catalog (error codes, run lifecycle, validator price): references/scrapercity-catalog.md
- ScraperCity CLI source (`db-leads` output and cursor hint): https://github.com/scrapercity/scrapercity-cli
- Yahoo Sender Hub, remove invalid recipients promptly: https://senders.yahooinc.com/best-practices/
