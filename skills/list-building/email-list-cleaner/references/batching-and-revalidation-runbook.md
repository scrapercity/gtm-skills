# Batching and Re-validation Runbook

How to validate files of any size with `validate_emails`, keep the bill equal to the unique count, track runs, recover from failures, split risky rows into their own send plans, and set the next validation date. Price: $0.0072 per email (`references/scrapercity-catalog.md`). The validator dedupes each submitted batch and bills unique addresses; dedupe locally anyway so the quoted count matches the bill and so duplicates across batches are not billed twice.

## 1. Pick the path by size

| Unique addresses after repair, dedupe and suppression | Path | Why |
|-|-|-|
| Up to about 1,000 | MCP `validate_emails` with `{"emails": [...]}` | One call, the array fits in a tool argument |
| 1,000 to 25,000 | One CLI or REST run from a one-column file | Large arrays in a chat tool call are slow to write and easy to truncate |
| Over 25,000 | Chunks of 25,000 (house batch size), one run per chunk | A failed chunk costs one 25,000-row retry; per-chunk results are easy to audit |

scrapercity.com/email-validator states no per-run cap. The 25,000 chunk size is a house operating choice for recoverability, dated 2026-10; raise it if your runs finish without trouble.

## 2. Prepare chunk files

The CLI command `scrapercity email-validate` with the `--file` flag reads the file line by line and keeps every line that contains `@`, trimmed. A multi-column CSV would send whole lines (`Dana,Ruiz,dana@acme.example`) as addresses. Export one address per line, no header.

```bash
# from a cleaned CSV with an email_key-deduped "email" column, write 25,000-line chunks
python3 - <<'EOF'
import csv
rows = [r["email"].strip().lower() for r in csv.DictReader(open("to_validate.csv", newline="", encoding="utf-8"))]
rows = list(dict.fromkeys(r for r in rows if "@" in r))
for i in range(0, len(rows), 25000):
    with open(f"chunk_{i // 25000 + 1:02d}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rows[i:i + 25000]) + "\n")
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
| `estimatedCost` differs from `emailCount` x $0.0072 by more than a cent | Stop and check the live price at scrapercity.com/pricing |

Polling: first check after 30 seconds, then every 30 to 60 seconds; validation runs finish in minutes. In a chat session, check once per turn and report `handled / requested`. Download within 48 hours of SUCCEEDED (results are stored for 48 hours per scrapercity.com/api-docs).

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
| 429 on submit or status | Rate limited | Wait 30 seconds, retry once |
| Run FAILED | Read `statusMessage` and `scrapercity logs RUN_ID` | Resubmit once; on a second failure split the chunk in half |
| Run CANCELLED | Someone cancelled it, or `cancel_run` ran | Resubmit if the reason is cleared |
| No response to the POST (timeout) | Unknown whether the run started | `list_runs` before resubmitting, so you do not pay twice |
| Results file shorter than `emailCount` | Truncated download | Download again; if still short, resubmit only the missing addresses |
| Addresses in results you never sent | Wrong chunk joined | Re-join by run id and file name |

## 7. Segment risky rows

Every row lands in one file (SKILL.md step 7). These send plans keep risky rows from contaminating the valid send. Thresholds are house standards from `references/deliverability-primer.md` section 7, dated 2026-10.

| File | Send plan | Stop rule |
|-|-|-|
| `send_ready.csv`, tier A or B | Normal campaign, high `email_quality` first | Pause at 2% hard bounces over 200 sends |
| `send_ready.csv`, tier C | First 10% of rows only; continue when bounces stay under 2% after 200 sends | Same |
| `role_review.csv` | User picks rows to keep; kept rows join a separate campaign with copy written for a shared inbox | Same |
| `catch_all.csv`, tier A or B | Separate campaign, at most 10% of daily volume, from the oldest warmed mailboxes, after the valid file shows bounces under 2% | 3% hard bounces after 200 sends ends catch-all sending |
| `catch_all.csv` with `gateway = true` | After plain catch-all rows show under 3% bounces | Same |
| `catch_all.csv`, tier C | No cold email; ads audiences, direct mail matching or phone only | n/a |
| `hold_unknown.csv` | Retry once after 72 hours, then route by the new status | Still unknown: catch_all rules (tier A or B) or removed (tier C) |

Daily volume worked example: 6 mailboxes x 30 cold sends a day = 180 sends. The catch-all cap is 10% of that, 18 catch-all sends a day.

## 8. Re-validation cadence

| Situation | Re-validate when | Cost per 1,000 |
|-|-|-|
| Rows validated but not yet mailed | 30 days after `email_validated_at` | $7.20 |
| Re-launch to a list mailed before | Before the re-launch if older than 30 days | $7.20 |
| `unknown` results | Once, 72 hours after the first run | $7.20 |
| Live campaign hits 2% hard bounces | Pause, then re-validate the unsent remainder | $7.20 |
| CRM contacts used for occasional one-to-one email | Quarterly | $7.20 |
| Catch-all rows that bounced | Never; suppress the bounced address | $0 |
| Addresses on any suppression list | Never | $0 |

The 30-day window is a house standard. US Bureau of Labor Statistics data put median employee tenure at 4.1 years in January 2026; spread evenly that is roughly 1.4% of a contact list changing employer each month, before promotions and closures. Measure your own bounce rate by list age and adjust.

Re-validation runs only on rows that are still candidates to send. Never re-validate `removed.csv`; that pays to confirm addresses you have already decided not to mail.

## 9. Suppression sync after every run

| Result | Sequencer action | CRM action |
|-|-|-|
| `invalid` | Add to the workspace blocklist (Instantly and Smartlead both keep one) | Mark email invalid, keep the contact |
| `disposable` | Blocklist | Clear the email field |
| Network-role addresses | Blocklist | No change |
| Hard bounce from a live send | Blocklist, permanent | Mark bounced |
| Unsubscribe or complaint | Blocklist, permanent, within 24 hours (house standard; CAN-SPAM allows 10 business days) | Opt-out flag |

## 10. Recipe library

| Job | Steps | Cost formula |
|-|-|-|
| Quick check of fewer than 50 addresses before a one-off send | MCP `validate_emails` with the array; route by status | n x $0.0072 |
| Monthly CRM hygiene | Export contacts with `email_validated_at` older than 90 days and an open sequence or a planned send; validate; write status back | stale rows x $0.0072 |
| Pre-launch check on a purchased or inherited list | Full SKILL.md workflow, tier C rules | unique after suppression x $0.0072 |
| Bounce spike on a live campaign | Pause; export unsent rows; validate; resume with valid only | unsent rows x $0.0072 |
| Merge two lists before one campaign | Repair, build `email_key`, dedupe across both, suppress, validate once | unique across both x $0.0072 |
| Event list right after the event | Validate within 7 days; badge-scan rows carry more typos, so apply the typo map first | unique x $0.0072 |
| 100,000-row archive | Four chunks of 25,000; run log; 402 check before each chunk | 100,000 x $0.0072 = $720.00, shown and approved before the first chunk |

## Sources

- ScraperCity, Email Validator: https://scrapercity.com/email-validator
- ScraperCity, API docs (storage window, rate limits): https://scrapercity.com/api-docs
- ScraperCity CLI source (`email-validate` reads lines containing @): https://github.com/scrapercity/scrapercity-cli
- ScraperCity npm package: https://www.npmjs.com/package/scrapercity
- US Bureau of Labor Statistics, Employee Tenure: https://www.bls.gov/news.release/tenure.nr0.htm
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
