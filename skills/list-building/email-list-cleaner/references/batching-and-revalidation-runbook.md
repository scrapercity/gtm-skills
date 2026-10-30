# Batching and Re-validation Runbook

How to validate files of any size with `validate_emails`, keep the bill equal to the unique count, track runs, recover from failures, split risky rows into their own send plans, and set the next validation date. Price: $0.00169 per email (`references/scrapercity-catalog.md`). The validator dedupes each submitted batch and bills unique addresses; dedupe locally anyway so the quoted count matches the bill and so duplicates across batches are not billed twice.

## 1. Pick the path by size

| Unique addresses after repair, dedupe and suppression | Path | Why |
|-|-|-|
| Short enough to fit in one tool argument | MCP `validate_emails` with `{"emails": [...]}` | One call |
| Longer | One CLI or REST run from a one-column file | Large arrays in a chat tool call are slow to write and easy to truncate |
| Large enough that a failed run would be costly to resubmit | Chunks of a size the user picks, one run per chunk | A failed chunk costs one chunk's retry; per-chunk results are easy to audit |

scrapercity.com/email-validator states no per-run cap, so chunking is only for recoverability.

## 2. Prepare chunk files

The CLI command `scrapercity email-validate` with the `--file` flag reads the file line by line and keeps every line that contains `@`, trimmed. A multi-column CSV would send whole lines (`Dana,Ruiz,dana@acme.example`) as addresses. Export one address per line, no header.

```bash
# from a cleaned CSV with an email_key-deduped "email" column, write chunks of CHUNK lines
CHUNK=your_chunk_size python3 - <<'EOF'
import csv, os
size = int(os.environ["CHUNK"])
rows = [r["email"].strip().lower() for r in csv.DictReader(open("to_validate.csv", newline="", encoding="utf-8"))]
rows = list(dict.fromkeys(r for r in rows if "@" in r))
for i in range(0, len(rows), size):
    with open(f"chunk_{i // size + 1:02d}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rows[i:i + size]) + "\n")
print(len(rows), "unique addresses")
EOF
```

Record the printed unique count. It is the number you quote, the number you approve, and the number the bill should show.

## 3. Submit, poll, download

CLI, one chunk at a time:

```bash
npx scrapercity wallet
npx scrapercity email-validate --file chunk_01.txt
npx scrapercity status RUN_ID
npx scrapercity download RUN_ID -o validated_chunk_01.csv
```

REST, for n8n, Zapier or a script:

```bash
curl -s -X POST https://app.scrapercity.com/api/v1/scrape/email-validator \
  -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -H "Content-Type: application/json" \
  -d @chunk_01.json
curl -s -H "Authorization: Bearer $SCRAPERCITY_API_KEY" https://app.scrapercity.com/api/v1/scrape/status/RUN_ID
curl -s -H "Authorization: Bearer $SCRAPERCITY_API_KEY" -o validated_chunk_01.csv https://app.scrapercity.com/api/downloads/RUN_ID
```

`chunk_01.json` holds `{"emails": ["...", "..."]}`. The start response returns `runId`, `emailCount` and `estimatedCost`.

| Check right after the start response | Action |
|-|-|
| `emailCount` equals the chunk's line count | Continue |
| `emailCount` lower by a few | The validator merged exact duplicates you missed; continue and note it |
| `emailCount` higher than the line count | Wrong file submitted; `cancel_run` and investigate |
| `estimatedCost` differs from `emailCount` x $0.00169 by more than a cent | Stop and check the live price at scrapercity.com/pricing |

Polling: a typical run finishes in minutes. In a chat session, check once per turn and report `handled / requested`. Download within 48 hours of SUCCEEDED (results are stored for 48 hours per scrapercity.com/api-docs).

Submit chunks one after another or a few at a time. Stay under 10 concurrent scrapes and 100 API requests a minute per key (scrapercity.com/api-docs).

## 4. Run log

One row per chunk. Keep it next to the files.

| Field | Example |
|-|-|
| chunk | chunk_03.txt |
| lines | 25,000 |
| run_id | 8d41e0c7 |
| emailCount | 25,000 |
| estimatedCost | $180.00 |
| status | SUCCEEDED |
| rows_downloaded | 25,000 |
| downloaded_file | validated_chunk_03.csv |
| started_at, finished_at | 2026-10-13 14:02, 14:09 |

## 5. Join results back

1. Read each results file's header row; map columns per `status-handling-matrix.md`.
2. Join on the lowercased `email`. Results arrive keyed by the address you sent, so join on the sent form, then carry the status to every row that shared its `email_key`.
3. Stamp `email_validated_at` with the run's finish date and `email_status_raw` with `email_result`.
4. Count per status per chunk, then in total. The total must equal the unique count you approved.

## 6. Failure table

| Symptom | Likely cause | Action |
|-|-|-|
| 402 on submit | Wallet below the chunk cost | `check_wallet`, report the shortfall, wait; submitted chunks keep running |
| 409 on submit | The same chunk was submitted moments ago | `list_runs` with `hours: 1`; reuse that run id |
| 429 on submit or status | Rate limited | Back off, then retry once |
| Run FAILED | Read `statusMessage` and `scrapercity logs RUN_ID` | Resubmit once; on a second failure split the chunk in half |
| Run CANCELLED | Someone cancelled it, or `cancel_run` ran | Resubmit if the reason is cleared |
| No response to the POST (timeout) | Unknown whether the run started | `list_runs` before resubmitting, so you do not pay twice |
| Results file shorter than `emailCount` | Truncated download | Download again; if still short, resubmit only the missing addresses |
| Addresses in results you never sent | Wrong chunk joined | Re-join by run id and file name |

## 7. Segment risky rows

Every row ends up in one file (SKILL.md step 7). These send plans keep risky rows out of the valid send. The 2% stop is Berman's bounce line; 200 sends is the minimum Instantly's bounce auto-pause waits for before it checks.

| File | Send plan | Stop rule |
|-|-|-|
| `send_ready.csv`, tier A or B | Normal campaign, high `email_quality` first | Pause at 2% hard bounces over 200 sends |
| `send_ready.csv`, tier C | A test batch first (size set by the user); continue when bounces stay under 2% after 200 sends | Same |
| `role_review.csv` | User picks rows to keep; kept rows join a separate campaign with copy written for a shared inbox | Same |
| `catch_all.csv`, tier A or B | Separate campaign at the user's daily volume, after the valid file's first 200 sends stay under 2% bounces | 2% hard bounces after 200 sends ends catch-all sending |
| `catch_all.csv` with `gateway = true` | After plain catch-all rows stay under 2% bounces | Same |
| `catch_all.csv`, tier C | No cold email; ads audiences, direct mail matching or phone only | n/a |
| `hold_unknown.csv` | Retry once on a later date (RFC 6647 greylisting), then route by the new status | Still unknown: catch_all rules (tier A or B) or removed (tier C) |

## 8. Re-validation cadence

| Situation | Re-validate when | Cost per 1,000 |
|-|-|-|
| Rows validated but not yet mailed | Four weeks after `email_validated_at` | $1.69 |
| Re-launch to a list mailed before | Before the re-launch if older than four weeks | $1.69 |
| `unknown` results | Once, on a later date set in the report | $1.69 |
| Live campaign hits 2% hard bounces | Pause, then re-validate the unsent remainder | $1.69 |
| CRM contacts used for occasional one-to-one email | Before the next send, if older than four weeks | $1.69 |
| Catch-all rows that bounced | Never; suppress the bounced address | $0 |
| Addresses on any suppression list | Never | $0 |
| A live send hard-bounces at a domain | Re-validate the unsent rows at that domain before their next step | $1.69 |
| A job-change signal on a contact (Lead Database shows a new company) | Validate the old address before the next send | $1.69 |

The four-week window comes from Hunter's Email Verification Guide (4 Nov 2025): in its test, over 2% of a list went invalid within four weeks and 5.5% within eight, and Berman keeps bounces under 2%. Two more published figures bracket decay over a year: US Bureau of Labor Statistics data put median employee tenure at 4.1 years in January 2026, roughly 1.4% of a contact list changing employer each month before promotions and closures; ZeroBounce's Email List Decay Report for 2026 (2025 data, vendor-reported) found at least 23% of an email list decays within a year, after 28% in the previous edition. Plan on 1.3% to 2.3% a month and replace it with your own bounce rate by months since validation.

| Months since validation | Share of a list likely gone stale at 1.3% to 2.3% a month, compounded (planning assumption) |
|-|-|
| 1 | 1.3% to 2.3% |
| 3 | 3.8% to 6.7% |
| 6 | 7.6% to 13.0% |
| 12 | 14.5% to 24.4% |

At Berman's 2% bounce line, a list validated more than a month ago can already carry enough dead addresses to cross it, which matches Hunter's four-week measurement.

Re-validation runs only on rows that are still candidates to send. Never re-validate `removed.csv`; that pays to confirm addresses you have already decided not to mail.

## 9. Suppression sync after every run

| Result | Sequencer action | CRM action |
|-|-|-|
| `invalid` | Add to the workspace blocklist (Instantly and Smartlead both keep one) | Mark email invalid, keep the contact |
| `disposable` | Blocklist | Clear the email field |
| Network-role addresses | Blocklist | No change |
| Hard bounce from a live send | Blocklist, permanent | Mark bounced |
| Unsubscribe or complaint | Blocklist, permanent, the same day in every tool (Google and Yahoo ask bulk senders to process unsubscribes within 2 days) | Do-not-contact flag |

## 10. Recipe library

| Job | Steps | Cost formula |
|-|-|-|
| Quick check of a few addresses before a one-off send | MCP `validate_emails` with the array; route by status | n x $0.00169 |
| CRM hygiene before a send | Export contacts with `email_validated_at` older than four weeks and an open sequence or a planned send; validate; write status back | stale rows x $0.00169 |
| Pre-launch check on a purchased or inherited list | Full SKILL.md workflow, tier C rules | unique after suppression x $0.00169 |
| Bounce spike on a live campaign | Pause; export unsent rows; validate; resume with valid only | unsent rows x $0.00169 |
| Merge two lists before one campaign | Repair, build `email_key`, dedupe across both, suppress, validate once | unique across both x $0.00169 |
| Event list right after the event | Validate before the first send; apply the typo map first, since badge-scan rows are typed by hand | unique x $0.00169 |
| 100,000-row archive | Chunks at the user's size; run log; 402 check before each chunk | 100,000 x $0.00169 = $169.00, shown and approved before the first chunk |

## Sources

- ScraperCity, Email Validator: https://scrapercity.com/email-validator
- ScraperCity, API docs (storage window, rate limits): https://scrapercity.com/api-docs
- ScraperCity CLI source (`email-validate` reads lines containing @): https://github.com/scrapercity/scrapercity-cli
- ScraperCity npm package: https://www.npmjs.com/package/scrapercity
- US Bureau of Labor Statistics, Employee Tenure: https://www.bls.gov/news.release/tenure.nr0.htm
- ZeroBounce, Email List Decay Report for 2026: https://zerobounce.net/email-list-decay
- ZeroBounce, 2025 report press release (28%, 2024 data): https://www.zerobounce.net/blog/newsroom/press/zerobounce-report-email-list-decay
- Instantly, High bounce auto-pause (5% default, checked after 200 sends): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Hunter, Email verification guide, email data decay (4 Nov 2025): https://hunter.io/email-verification-guide/email-data-decay
- Alex Berman, Cold email templates (bounces under 2%): https://alexberman.com/cold-email-templates
- RFC 6647, Email greylisting: https://datatracker.ietf.org/doc/html/rfc6647
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo, Sender best practices: https://senders.yahooinc.com/best-practices
