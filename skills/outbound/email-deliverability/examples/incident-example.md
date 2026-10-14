# Deliverability Recovery Plan: Harborview Payroll

Illustrative example (fictional company; domains use `.example`). Prepared Tuesday 2026-11-10 for Lena Ortiz (sales ops), who can pause any domain without sign-off. Setup: 8 Google Workspace inboxes on 4 domains at 30 a day, weekdays only, so 240 sends a day and 1,200 a week. Assumed: Instantly as the sequencer, a 2,400-row list from a new source loaded on 2026-11-02, about 2,900 rows still queued. In Smartlead or another sequencer, the same two settings are the custom tracking domain and the bounce auto-pause. Results of the checks below are pending.

## Verdict

Open rate fell from 48% to 7% and hard bounces reached 4.5%, about 54 of last week's 1,200 sends, on all 4 domains at once. Volume did not change, so the cause is something every domain shares, and the likeliest one is the new list: 4.5% is more than double Alex Berman's 2% hard-bounce line, and that many dead addresses also pushes mail toward spam, which is how an open collapse looks. Stop all cold sends today and re-validate everything queued. The earliest restart is Thursday 2026-11-12 at 10 a day per inbox, only if Wednesday's seed test reaches the inbox at every seed provider. Decision for you: approve about $20.88 of re-validation.

## Stop Now

- Today, 2026-11-10: pause every cold campaign on all 4 domains.
- Add the 54 hard-bounced addresses to the workspace-wide blocklist, so no campaign mails them again.
- Quarantine the 2026-11-02 batch's unsent rows and freeze list uploads and cap changes until the cause is written down.
- Buy no new domains or inboxes this week. They would get the same unverified list and copy and burn the same way.
- Turn open tracking off and remove links from touch 1 for the recovery.
- Lower the bounce auto-pause to 2%: Instantly > Settings > Preferences, the Switch button next to "Automatically pause campaigns with high bounce rates". Its default of 5%, checked after 200 sends (Instantly help), never fired at 4.5%.
- Keep: warmup at its current setting (do not raise it), the opt-out line in every touch, and same-day suppression of every opt-out.

## Diagnosis

| Rank | Likely cause | Why it fits your numbers | Confirm with | Clears it |
|-|-|-|-|-|
| 1 | Bad or stale rows in the new batch | Bounces jumped the week a new source went in, on every domain | Check 1 shows mostly `550 5.1.1` (Gmail) or `550 5.1.10` (Microsoft 365) across many recipient domains, on rows from the 2026-11-02 upload | Bounces spread across older rows, or mostly `5.7.x` codes |
| 2 | Spam placement following the bounce hit | Opens fell 85% on all domains in the same week | Check 5 lands in spam at any provider; human replies per 1,000 sends down against the 4 weeks before the drop | Seeds in the inbox at every provider and replies back at that baseline |
| 3 | Tracking host or a linked domain flagged | All 4 domains share the tracking host and the main-site link | Check 2 shows the `inst` CNAME missing or wrong; check 4 lists a linked domain; the live copy lands in spam and the same copy without tracking or links lands in the inbox | Both seed versions land in the same folder and every lookup is clean |
| 4 | Authentication broken by a DNS edit | Would hit every domain the same day | Check 1 shows `5.7.26`, `5.7.27` or `5.7.30`; check 2 or 3 fails | Check 3 passes on all 8 inboxes |

Run today, in order:

1. Export last week's hard bounces from Instantly with the full reply text, split by code and upload date. "Does not exist" or "not found" means a dead mailbox; "unauthenticated", "SPF", "DKIM" or "DMARC" means authentication; "unusual rate of unsolicited mail" means reputation.
2. On each sending domain, shown for getharborview.example: `dig +short TXT getharborview.example` (one `v=spf1`), `dig +short TXT google._domainkey.getharborview.example` (a `v=DKIM1` key), `dig +short TXT _dmarc.getharborview.example` (one `v=DMARC1`), `dig +short CNAME inst.getharborview.example` (must return `prox.itrackly.com`).
3. Send from each of the 8 inboxes to a personal Gmail seed, open Show original, and look for `spf=pass`, `dkim=pass` and `dmarc=pass`.
4. Look up the 4 sending domains, harborviewpayroll.example and the booking link's domain on check.spamhaus.org, then the linked domains on SURBL and URIBL.
5. Seed test on Wednesday: live touch 1 from one inbox per domain to a GlockApps Smart Test address, plus a Workspace and a Microsoft 365 seed account you own (GlockApps weights its coverage toward US consumer providers).

Fix when confirmed:

- SPF: one record per domain, `v=spf1 include:_spf.google.com ~all`; merge into an existing record, never add a second.
- DKIM: Google Admin console > Apps > Google Workspace > Gmail > Authenticate email, pick the domain, Generate New Record, 2048-bit, prefix `google`, publish the TXT, then Start authentication.
- DMARC: `_dmarc.getharborview.example` TXT `v=DMARC1; p=none; rua=mailto:dmarc@harborviewpayroll.example`.
- Tracking: `inst` CNAME to `prox.itrackly.com` (Instantly help), or leave open tracking off.
- Listing: fix the cause, then request removal on check.spamhaus.org; take a listed link out of every touch until it clears.

## Measurement

The 48% was never a clean number. Apple Mail downloads images when a message arrives whether or not anyone reads it, Outlook blocks images by default, and security filters at Proofpoint or Barracuda customers open messages within seconds of delivery. Judge the incident and the recovery by seed placement, human replies per 1,000 sends against the 4 weeks before the drop, and hard bounces with their codes. At 60 sends a day per domain Postmaster may show no data, and a low spam rate there counts only mail that reached the inbox, so seeds decide.

## List Re-validation

Re-validate all queued rows with ScraperCity's Email Validator: about 1,700 unsent rows from the new batch and about 1,200 older rows last validated before your 30-day re-check window, 2,900 x $0.0072 = $20.88. Valid rows go to the restart file, highest quality first. Catch-all rows wait until the inboxes are back at 30 a day on 2026-11-30 and then run in their own campaign. Unknown rows are re-checked once. Invalid and disposable rows go to the blocklist. Bring the new source's invalid share to Wednesday's check-in.

## Recovery Plan

Day numbers count sending days (weekdays). The ramp starts at the low end of Alex Berman's 10 to 20 a day for new domains, returns over his 2 to 4 weeks, and never doubles in one step (Google's sender guidelines).

Standard gate: hard bounces under 2% over the last 200 sends (Alex Berman's line, Instantly's 200-send window), zero `4.7.28` deferrals, every domain under 0.1% spam rate (Google's sender guidelines).

| Date | Day | Action | Sends per inbox | Total sends a day | Gate to move on |
|-|-|-|-|-|-|
| Tue 2026-11-10 | 0 | Stop list above; run checks 1 to 4 | 0 | 0 | Cause written down |
| Wed 2026-11-11 | 1 | Re-validate; apply the fix; seed test 1 (check 5), plus the no-tracking version if cause 3 is open | 0 | 0 | File 100% valid; check 3 passes on all 8 inboxes; no listing |
| Thu 2026-11-12 | 2 | Restart if seed test 1 reached the inbox at every provider; best-fit rows first | 10 | 80 | Under 4 hard bounces in the first 200 restart sends |
| Fri 2026-11-13 | 3 | Seed test 2; read bounces, replies, deferrals and opt-outs every morning from here | 10 | 80 | Standard gate; seeds in the inbox at every provider |
| Mon 2026-11-16 to Fri 2026-11-20 | 4 to 8 | Hold; keep, rest or retire each domain on Fri 2026-11-20 | 10 | 80 | Standard gate for 5 days |
| Mon 2026-11-23 to Fri 2026-11-27 | 9 to 13 | First of two equal steps back to 30 | 20 | 160 | Standard gate; replies per 1,000 sends against the pre-drop baseline |
| Mon 2026-11-30 onward | 14+ | Back to the previous cap of 30, under Berman's 50; catch-all campaign may start | 30 | 240 | Standard gate every week |

## Resume and Retire Rules

| If | Then |
|-|-|
| Seed test 1 fails | Fix and retest; every later date moves by the days lost |
| A campaign or inbox misses the bounce gate | Back one step for the rest of the week and re-check that row source |
| Gmail `421 4.7.28` on a domain | Send nothing from it for at least 10 minutes (Google's sender guidelines), then hold its step until a full week passes without one |
| `550 5.7.28`, a 0.3% spam rate on any day, or a Spamhaus listing | Stop that domain; at 0.3% Google's sender guidelines FAQ restores mitigation only after 7 consecutive days below it |
| Seeds in spam at several providers on 2026-11-20 with the cause fixed | Rest the domain with warmup only until Instantly's readiness rule holds again (at least 2 weeks, health score above 90%), then restart at 10 |
| Still in spam after the rest, or listed a second time | Retire it from cold email and move its 60 a day to a reserve domain started warming once the cause was fixed |

## Next Check-in

Wednesday 2026-11-11, 10:00 ET, with Lena Ortiz. Bring the results of checks 1 to 4, replies per 1,000 sends for the last 4 weeks, the re-validation counts by result and source, and seed test 1. Pending: approval of the $20.88 re-validation and whether to keep buying from the new source.
