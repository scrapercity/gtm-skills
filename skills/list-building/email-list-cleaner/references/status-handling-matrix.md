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
| `sc_mx_security_gateway` | Security gateway in front of the mailbox (for example Mimecast, Proofpoint, Barracuda) | Catch-all send order (gateway rows last) |
| `sc_company_name`, `industry`, `size`, `founded`, `location`, `sc_company_linkedin`, `sc_company_type` | Company enrichment for the domain | Filling blank firmographics; spotting rows on the wrong company |

## 2. Primary routing by `email_result`

| `email_result` | Bucket in `list-quality-standard.md` | Destination file | Sequencer action | CRM action |
|-|-|-|-|-|
| `valid` | valid | `send_ready.csv` (or `role_review.csv` if role on a B2B list) | Upload | Set `email_status = valid`, stamp `email_validated_at` |
| `valid_catch_all` | catch_all | `catch_all.csv` | Separate campaign at the user's daily volume, stopped past 2% bounces | Keep; mark status |
| `unknown` | unknown | `hold_unknown.csv` | Do not upload | Keep; mark status and retry date |
| `invalid` | invalid | `removed.csv` reason `invalid` | Add to blocklist | Mark email invalid; do not delete the contact |
| `disposable` | disposable | `removed.csv` reason `disposable` | Add to blocklist | Clear the email field; keep the contact if other data exists |

## 3. Combined rules

Apply in order. The first matching rule wins.

| # | Condition | Route | Why |
|-|-|-|-|
| 1 | Local part is `abuse`, `postmaster`, `hostmaster`, `noc`, `security` | `removed.csv`, `network_role` (removed before validation, listed here so a re-import is caught) | RFC 2142 operations mailboxes reach the people who handle abuse reports, not buyers |
| 2 | `email_result = invalid` or `disposable` | `removed.csv` | Never sendable |
| 3 | `email_result = valid`, list type is named B2B, `is_role = true` | `role_review.csv` | A named list should reach the named person |
| 4 | `email_result = valid`, `is_free = true`, list type is named B2B, `company_domain` present and different from the address domain | `role_review.csv` with note `personal_address` | Personal inbox for a business contact; the user decides whether to use it |
| 5 | `email_result = valid`, `email_quality = low` | `send_ready.csv`, sorted to the end | Send last so early bounces show up on better rows first |
| 6 | `email_result = valid` | `send_ready.csv` | Default |
| 7 | `email_result = valid_catch_all`, `sc_mx_security_gateway` present | `catch_all.csv` with `gateway = true` | Gateways can accept then bounce later; send these after plain catch-alls stay under 2% bounces |
| 8 | `email_result = valid_catch_all` | `catch_all.csv`, ordered per section 4a | Default |
| 9 | `email_result = unknown`, first pass | `hold_unknown.csv`, retry once on a later date | Greylisting servers reject a first attempt and accept a later retry (RFC 6647) |
| 10 | `email_result = unknown`, second pass | Tier A or B list: `catch_all.csv`. Tier C list: `removed.csv` reason `unknown_twice` | One retry only |
| 11 | Row came back with a different address than submitted (case or whitespace only) | Join on lowercased address, keep your version | Do not create a second row |
| 12 | Row submitted but missing from results | Resubmit in a small follow-up run | See the runbook failure table |

## 4. Catch-all policy by list tier

| Tier (SKILL.md step 1) | Catch-all rows in cold campaigns | Daily volume | Stop rule |
|-|-|-|-|
| A | Allowed once the valid file's first 200 sends stay under 2% bounces | The user's number | Catch-all campaign over 2% hard bounces after 200 sends |
| B | Same | The user's number | Same |
| C | Not in cold campaigns. Use for ads audiences, direct mail matching, or phone outreach | 0 | n/a |

The 2% stop is Berman's bounce line; 200 sends is the minimum Instantly's bounce auto-pause waits for before it checks. A catch-all domain answers "accepted" for every address during validation, so the only test is a send.

## 4a. Catch-all send order

A catch-all domain accepts every address at validation, so the file has to be ordered by other evidence. Sort each `catch_all.csv` row by this evidence, in order, and send the strongest rows first; the first 200 catch-all sends decide whether the rest go out (2% hard-bounce stop above).

1. The person is confirmed at the company since the list was built (a Lead Database match, a reply, a meeting).
2. The local part matches the format of other known addresses at the same domain (`first.last`, `flast`, `first`), taken from Lead Database rows or past replies.
3. `email_quality` high, then medium.
4. No `sc_mx_security_gateway` value.

Rows with none of this evidence wait until the stronger rows have sent 200 with under 2% hard bounces. When any catch-all address at a domain hard-bounces, pause the other unsent catch-all rows at that domain: the server that accepted every address at validation is rejecting at delivery.

The format check ranks rows. It never creates an address: a pattern-built address is not a found address and is not sent.

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

| What the results show | Likely cause | Action |
|-|-|-|
| `invalid` share far above the other sources in the same file | Old export, people left, or wrong column mapped | Check age and mapping; re-pull from a fresh source |
| `invalid` concentrated on a few domains | Company rebranded or was acquired | Look up the new domain; use `find_emails` for VIP contacts |
| `sc_mx_record` empty for many rows on one domain | Domain expired or has no mail | Remove the domain; flag the account as possibly closed |
| `disposable` rows clustered in one source | Sign-up or giveaway form data | Treat every row from that source as tier C |
| A large `valid_catch_all` share | Many small businesses on accept-all hosting, or one large catch-all company | Expected for some local lists; plan the catch-all campaign volume |
| Many `free` addresses on a B2B list | Event badge scans or personal sign-ups | Route to `role_review.csv`; ask if personal addresses may be used |

## 7. Report lines that must come out of this matrix

- Count per `email_result` and the total validated, which must match the billed count.
- Count per destination file; files sum to all input rows (plus split rows).
- Projected hard bounce on `send_ready.csv`: the user's bounce rate on valid rows from their last send, or "no history; measured on the first 200 sends" when there is none.
- Count of `invalid` plus `disposable` pushed to the blocklist.

## Sources

- https://scrapercity.com/email-validator
- https://datatracker.ietf.org/doc/rfc2142/
- https://senders.yahooinc.com/best-practices
- https://support.google.com/a/answer/81126
- https://m3aawg.org/sites/maawg/files/news/M3AAWG_Senders_BCP_Ver3-2015-02.pdf
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://datatracker.ietf.org/doc/html/rfc6647
- https://alexberman.com/cold-email-templates
