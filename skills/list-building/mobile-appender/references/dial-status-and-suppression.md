# Dial Status and Suppression

How each appended mobile gets its `dial_status`, how the suppression check runs, and how removal requests are handled while the campaign runs. Run section 1 before the pilot and sections 2 and 3 after the append.

## 1. Call plan

Record these answers in the report's Call Plan table before spending anything:

| Question | Why it changes the run |
|-|-|
| How will numbers be dialed? Manual, click-to-call or power dialer | A power dialer that skips non-mobile lines needs a line-type lookup on every number; click-to-call reps can mark wrong lines as they go |
| Which suppression list is used, and how many rows does it hold? | Suppressed people are removed before the pilot, so they never cost a lookup |
| Which countries are in the list? | Sets the E.164 country code and the time zones |
| Will line-type lookups run on every number? | Decides whether `line_type` is filled or `unchecked` |
| Where do the numbers go after delivery? | Dialer, CRM mobile field, or both; the CRM field should only receive `line_type = mobile` rows |

## 2. Suppression check

One suppression list holds every person who asked not to be contacted, from every tool: the dialer, the sequencer, the CRM and reply inboxes. Keeping one list means a removal logged in email also stops the calls.

Run the checks in this order:

1. Before the pilot: match input emails and LinkedIn URLs against the suppression list and drop matches. This saves the $0.25 a hit would cost.
2. After the append: match every found number in E.164 against the suppression list. Any hit is `hold_suppressed`, permanently.
3. Record the check in the run log: date, list version, counts removed. Write the date to `suppression_checked_at`.

## 3. Dial status assignment

```text
if number or person on suppression list         -> hold_suppressed
elif number shared by 2+ people                 -> hold_shared_number
elif plan needs mobile and line_type not mobile -> hold_line_type
else                                            -> callable
```

| `dial_status` | What the team does with it |
|-|-|
| `callable` | Load into the dialer with `tz` mapped |
| `hold_suppressed` | Never dialed; stays in the hold file so it is not re-appended |
| `hold_line_type` | A rep reviews; desk direct dials move to the `phone` column |
| `hold_shared_number` | Move to the company `phone` column; it is a main line or reception |

## 4. Shared numbers

A number found on two or more people is a main line or a reception desk. Hold every copy, and if one copy matches the company's published main line, move it to `phone`. Counting shared numbers per company also shows which accounts need a decision-maker search before calling.

## 5. Time zones and call windows

- Take the time zone from the person's city and state or country and store it as an IANA zone such as `America/Chicago`. A mobile area code shows where the number was issued, not where the person lives now.
- When the person's location is missing, use the company HQ and mark `tz_source = company_hq`.
- The call window is a team setting in the prospect's local time. Set it from the team's own connect data: after the first week of dials, compare connect rate by local hour and move the window to the best hours.

## 6. Removal requests during the campaign

- Add anyone who asks not to be called to the suppression list the same day, and sync it to every tool: dialer, sequencer, CRM.
- Stop every other sequence step for that person at the same time.
- Keep suppressed rows in the hold file so a later append run skips them before it bills.

## 7. Call plan table for the report

Illustrative rows:

| Question | Answer | Action |
|-|-|-|
| Dialing method | Click-to-call, one call at a time | Line-type lookup on every number so reps only see mobiles |
| Suppression list | Unified list, 1,240 rows | Matched before the pilot and after the append |
| Countries | United States | `+1` country code; `tz` from person city and state |
| Line-type lookups | Every found number | `hold_line_type` for landline, VoIP and unknown |
| Destination | Sales engagement tool and CRM mobile field | Only `line_type = mobile` rows go to the CRM field |

## Sources

- Twilio, Lookup Line Type Intelligence: https://www.twilio.com/docs/lookup/v2-api/line-type-intelligence
- IANA Time Zone Database: https://www.iana.org/time-zones
- ScraperCity tool catalog (Mobile Finder price): references/scrapercity-catalog.md
