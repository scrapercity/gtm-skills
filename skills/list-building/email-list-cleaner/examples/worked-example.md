# Email List Cleaning Report: 2023-2024 event and webinar contacts

_Illustrative example. Companies, people, counts and run results are invented to show the format. Prices are ScraperCity catalog prices._

Prepared 2026-10-13 for Fieldnote Analytics (fieldnoteanalytics.example), a B2B reporting tool for operations teams, ahead of a cold re-engagement campaign in Instantly. Intended use: cold email. List type: named B2B contacts. Wallet before run: $212.40. Addresses below use the reserved `.example` domain.

## List Profile

| Item | Value |
|-|-|
| File and email column | `events_master_export.xlsx`, column `Email Address` (a second column `Alt Email` was empty on every row) |
| Raw rows | 12,400 |
| Source | Webinar registrations 2024 (6,288 rows), trade-show badge scans 2023 (4,710 rows), partner co-marketing list 2024 (1,402 rows) |
| Last mailed | August 2025, a newsletter to the webinar segment only |
| Last validated | Never |
| Previous bounce rate | 4.6% on the August 2025 newsletter (Instantly report) |
| Risk tier (A, B or C) | C: last mailed 14 months ago, never validated, includes badge scans |
| Suppression files supplied | Instantly unsubscribe and bounce exports, HubSpot customer domains, competitor domain list |

## Cleaning Funnel

| Stage | Rows | Change | Reason |
|-|-|-|-|
| Raw rows | 12,400 | 0 | Starting point |
| After splitting multi-address cells | 12,431 | +31 | 31 cells held two addresses separated by a semicolon; each became its own row |
| After removing blank emails | 12,219 | -212 | Badge scans with no email captured |
| After syntax repair | 12,158 | -61 | Unrepairable: missing domain, spaces inside the local part, two @ signs |
| After dedupe | 10,770 | -1,388 | Same person registered for several webinars; 97 of these were Gmail dot or case variants |
| After suppression | 10,368 | -402 | 188 unsubscribed, 131 past hard bounces, 6 spam complaints, 64 customer domains, 13 competitor domains |
| After network-role removal (sent to validator) | 10,351 | -17 | abuse@, postmaster@, noc@ and security@ addresses (RFC 2142) |

Syntax fixes applied and kept: 143, logged in `fix_applied`. Examples: `mailto:` prefix stripped (58), display names removed from `Dana Ruiz <dana.ruiz@ledgerline.example>` (41), trailing period removed (19), `gmial.com` to `gmail.com` (14), `hotmial.com` to `hotmail.com` (6), zero-width spaces removed (5). No corporate domain was rewritten.

## Validation Results

| Status | Count | Share | Routed to |
|-|-|-|-|
| valid | 7,214 | 69.7% | send_ready.csv, except 236 role and 341 personal addresses routed to role_review.csv |
| valid_catch_all | 1,302 | 12.6% | catch_all.csv, held out of cold campaigns (tier C) |
| unknown | 418 | 4.0% | hold_unknown.csv, one retry on 2026-10-16 |
| invalid | 1,329 | 12.8% | removed.csv and the Instantly blocklist |
| disposable | 88 | 0.9% | removed.csv and the Instantly blocklist |
| Total validated | 10,351 | 100% | One run |

Billed count from the run: `emailCount` 10,351 on run `3f9c27ab`, equal to the unique count sent; estimated cost in the start response $17.49.

Invalid rate by source: webinar registrations 8.1% (498 of 6,120 validated), badge scans 21.0% (641 of 3,050), partner list 16.1% (190 of 1,181). Badge scans and the partner list run at two to two and a half times the webinar list's invalid rate; neither should be reused without a fresh pull.

## Output Files

| File | Rows | Contents |
|-|-|-|
| send_ready.csv | 6,637 | `valid` only, sorted high, medium, low `email_quality`, non-role, company addresses |
| role_review.csv | 577 | 236 valid role addresses (info@, sales@, marketing@) and 341 valid personal Gmail or Outlook addresses on rows with a company domain |
| catch_all.csv | 1,302 | `valid_catch_all`, 214 of them behind a security gateway (`gateway = true`) |
| hold_unknown.csv | 418 | `unknown`, retry date set |
| removed.csv | 3,497 | 212 no_email, 61 syntax, 1,388 duplicate, 188 unsubscribed, 131 bounced, 6 complained, 64 customer, 13 competitor, 17 network_role, 1,329 invalid, 88 disposable |
| Total | 12,431 | Raw 12,400 rows plus 31 split rows; every row ends up in one file |

## Suppression Additions

| Addition | Count | Where it goes |
|-|-|-|
| invalid addresses | 1,329 | Instantly workspace blocklist, CRM email status set to invalid |
| disposable addresses | 88 | Instantly workspace blocklist |
| network-role addresses | 17 | Instantly workspace blocklist |
| Total new blocklist rows | 1,434 | `suppression_additions.csv`, one column, imported on 2026-10-13 |

## Cost Estimate

| Item | Units | Unit price | Cost |
|-|-|-|-|
| Email Validator | 10,351 | $0.00169 | $17.49 |
| Email Finder replacements for 40 invalid VIP contacts | 20 found (20 misses free) | $0.05 | $1.00 |
| Total paid usage | | | $18.49 |

Scheduled, not yet billed: unknown retry of 418 addresses on 2026-10-16, $0.71. Wallet after run: $193.91.

Approval: the user approved the $17.49 validation estimate and the $2.00 replacement ceiling in chat on 2026-10-13, after seeing the funnel down to 10,351 unique addresses.

## Re-validation Schedule

| File or rows | Next validation date | Rule |
|-|-|-|
| hold_unknown.csv | 2026-10-16 | One retry on the date Fieldnote set; still unknown goes to removed.csv as unknown_twice (tier C) |
| send_ready.csv rows not mailed yet | 2026-11-10 | Re-validate anything not sent within four weeks of validation |
| role_review.csv | 2026-10-20 | User decides which role and personal rows to keep; kept rows are mailed by 2026-11-10 or re-validated |
| catch_all.csv | 2026-11-10 | Not for cold email on a tier C list; re-validate before any ads or phone use after this date |
| CRM email status for this segment | 2027-01-13 | Re-validate before the Q1 HubSpot campaign Fieldnote has planned for that date |

## Next Steps

1. Load a 664-row test batch from the top of `send_ready.csv` (10% of the file, the size Fieldnote chose) into a new Instantly campaign with cross-campaign duplicate checking on; continue to the remaining 5,973 only if hard bounces stay under 2% after 200 sends.
2. Import the 1,434 blocklist rows before the campaign starts, and import the 20 replacement addresses from `replacements.csv` only after they pass the same suppression check.
3. Retire the badge-scan and partner sources; rebuild those segments from fresh Lead Database pulls on the same titles and company sizes, validated with the Email Validator before import.
4. Write `email_status` and `email_validated_at` back to HubSpot for all 10,351 validated contacts, and enroll the campaign only from an active segment filtered on valid status validated within the last four weeks.
