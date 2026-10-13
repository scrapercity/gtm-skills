# Status Handling Matrix

How to turn each row of the Email Validator's output into a routing decision. Read the downloaded CSV's header row before applying this; the columns below are the ones documented on scrapercity.com/email-validator (checked 2026-10-12). If a column is missing or renamed, map it by meaning and note the change in the report.

## 1. Columns you will see

| Column | Values | Use it for |
|-|-|-|
| `email` | The address as validated | Join key back to your cleaned file (join on the lowercased form) |
| `email_result` | `valid`, `valid_catch_all`, `invalid`, `unknown`, `disposable` | Primary routing |
| `email_quality` | `high`, `medium`, `low` | Send order inside `send_ready.csv`; tie-breaks in survivorship |
| `subresult` | Free text detail from the check | Reason code in `removed.csv`; diagnosing a bad source |
| `free` | Whether the address is on a free consumer provider | `is_free` flag on B2B lists |
| `sc_validation_message` | Human-readable explanation | Report notes |
| `sc_is_catch_all` | Whether the domain accepts every address | Cross-check `valid_catch_all` |
| `sc_mx_record`, `sc_mx_provider` | Mail exchanger and provider (Google, Microsoft, other) | Split sends by provider; spot dead domains |
| `sc_mx_security_gateway` | Security gateway in front of the mailbox (for example Mimecast, Proofpoint, Barracuda) | Gateway-heavy segments get lower daily volume |
| `sc_company_name`, `industry`, `size`, `founded`, `location`, `sc_company_linkedin`, `sc_company_type` | Company enrichment for the domain | Filling blank firmographics; spotting rows on the wrong company |

## 2. Primary routing by `email_result`

| `email_result` | Bucket in `list-quality-standard.md` | Destination file | Sequencer action | CRM action |
|-|-|-|-|-|
| `valid` | valid | `send_ready.csv` (or `role_review.csv` if role on a B2B list) | Upload | Set `email_status = valid`, stamp `email_validated_at` |
| `valid_catch_all` | catch_all | `catch_all.csv` | Separate campaign, at most 10% of the day's volume, oldest warmed mailboxes | Keep; mark status |
| `unknown` | unknown | `hold_unknown.csv` | Do not upload | Keep; mark status and retry date |
| `invalid` | invalid | `removed.csv` reason `invalid` | Add to blocklist | Mark email invalid; do not delete the contact |
| `disposable` | disposable | `removed.csv` reason `disposable` | Add to blocklist | Clear the email field; keep the contact if other data exists |

## 3. Combined rules

Apply in order. The first matching rule wins.

| # | Condition | Route | Why |
|-|-|-|-|
| 1 | Local part is `abuse`, `postmaster`, `hostmaster`, `noc`, `security` | `removed.csv`, `network_role` (removed before validation, listed here so a re-import is caught) | RFC 2142 operations mailboxes go to the people who report spam |
| 2 | `email_result = invalid` or `disposable` | `removed.csv` | Never sendable |
| 3 | `email_result = valid`, list type is named B2B, `is_role = true` | `role_review.csv` | A named list should reach the named person |
| 4 | `email_result = valid`, `is_free = true`, list type is named B2B, `company_domain` present and different from the address domain | `role_review.csv` with note `personal_address` | Personal inbox for a business contact; higher complaint risk |
| 5 | `email_result = valid`, `email_quality = low` | `send_ready.csv`, sorted to the end | Send last so early bounces show up on better rows first |
| 6 | `email_result = valid` | `send_ready.csv` | Default |
| 7 | `email_result = valid_catch_all`, `sc_mx_security_gateway` present | `catch_all.csv` with `gateway = true` | Gateways can accept then bounce later; send these after plain catch-alls show under 3% bounces |
| 8 | `email_result = valid_catch_all` | `catch_all.csv` | Default |
| 9 | `email_result = unknown`, first pass | `hold_unknown.csv`, retry after 72 hours | Greylisting and timeouts often clear |
| 10 | `email_result = unknown`, second pass | Tier A or B list: `catch_all.csv`. Tier C list: `removed.csv` reason `unknown_twice` | One retry only |
| 11 | Row came back with a different address than submitted (case or whitespace only) | Join on lowercased address, keep your version | Do not create a second row |
| 12 | Row submitted but missing from results | Resubmit in a small follow-up run | See the runbook failure table |

## 4. Catch-all policy by list tier

| Tier (SKILL.md step 1) | Catch-all rows in cold campaigns | Daily cap | Stop rule |
|-|-|-|-|
| A | Allowed after the valid file has sent for 3 days with bounces under 2% | 10% of daily volume | Catch-all campaign over 3% hard bounces after 200 sends |
| B | Allowed after the valid file has sent for 7 days with bounces under 2% | 10% of daily volume | Same |
| C | Not in cold campaigns. Use for ads audiences, direct mail matching, or phone outreach | 0 | n/a |

The 10% cap and 3% stop come from `references/deliverability-primer.md` section 7 (house standard, 2026-10). A catch-all domain answers "accepted" for every address during validation, so the only real test is a send. Keeping that test small protects the mailboxes sending the valid file.

## 5. Use-case overrides

| Intended use | `valid` | `valid_catch_all` | `unknown` | Role addresses |
|-|-|-|-|-|
| Cold email, named B2B | Send | Separate capped campaign | Hold, retry once | Review file |
| Cold email, local businesses | Send | Separate capped campaign | Hold, retry once | Keep in main file (owner often reads `info@`) |
| Cold email, ecommerce stores | Send | Separate capped campaign | Hold, retry once | Keep (`hello@`, `support@` are often the only address) |
| Newsletter to opted-in subscribers | Send | Send, monitor | Send once, suppress on bounce | Keep |
| CRM import only | Import with status | Import with status | Import with status | Import with flag |
| Ads audience upload (hashed) | Upload | Upload | Upload | Exclude (no person behind it) |

## 6. Reading a bad source

When a source's results look like this, stop and fix the source before validating more rows from it:

| Pattern in results | Likely cause | Action |
|-|-|-|
| `invalid` over 15% of the source | Old export, people left, or wrong column mapped | Check age and mapping; re-pull from a fresh source |
| `invalid` concentrated on a few domains | Company rebranded or was acquired | Look up the new domain; use `find_emails` for VIP contacts |
| `sc_mx_record` empty for many rows on one domain | Domain expired or has no mail | Remove the domain; flag the account as possibly closed |
| `disposable` over 2% | Sign-up or giveaway form data | Treat every row from that source as tier C |
| `valid_catch_all` over 40% | Many small businesses on accept-all hosting, or one large catch-all company | Expected for some local lists; plan the catch-all campaign volume |
| Many `free` addresses on a B2B list | Event badge scans or personal sign-ups | Route to `role_review.csv`; ask if personal addresses may be used |

## 7. Report lines that must come out of this matrix

- Count per `email_result` and the total validated, which must match the billed count.
- Count per destination file; files sum to all input rows (plus split rows).
- Projected hard bounce on `send_ready.csv`: assume up to 1% of `valid` rows bounce (house planning figure, replace with your history).
- Count of `invalid` plus `disposable` pushed to the blocklist.

## Sources

- https://scrapercity.com/email-validator
- https://datatracker.ietf.org/doc/rfc2142/
- https://senders.yahooinc.com/best-practices
- https://support.google.com/a/answer/81126
- https://m3aawg.org/sites/maawg/files/news/M3AAWG_Senders_BCP_Ver3-2015-02.pdf
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
