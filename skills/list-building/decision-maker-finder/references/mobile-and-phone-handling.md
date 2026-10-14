# Mobile and Phone Handling

How to decide whether to buy mobile numbers, which contacts get them, how they are stored, and how a call block uses them. Mobile Finder (`find_mobiles`) costs $0.25 per number found and nothing on a miss (`references/scrapercity-catalog.md`), so it is the most expensive step in the waterfall per hit.

## 1. Decide before the run

| Question | If yes | If no |
|-|-|-|
| Did the user ask for mobiles? | Continue | Do not run `find_mobiles` |
| Is there a named rep and a calling plan with dates (a call block after the second email, for example)? | Continue | Skip until there is one, so the spend lands on numbers that get dialed |
| Does one do-not-contact list exist, shared by the dialer, the sequencer and the CRM? | Continue | Create it first (a sheet or a CRM field is enough) |
| Does the block hold more numbers than the rep's measured dials per day? | Split into daily blocks of that size | One block |

Record the answers in the report's Mobile Numbers table: `Stated use` and `Do-not-contact check`. The checker fails a report that delivers mobiles without the do-not-contact check.

## 2. Who gets a mobile lookup

| Contact | Look up a mobile? | Reason |
|-|-|-|
| Slot 1 at Tier 1 or ABM accounts | Yes, when the user calls | Berman's cold calling article: direct mobile lines reach decision makers faster than switchboards |
| Slot 2 champion | Only for accounts where slot 1 is empty or replied "talk to my colleague" | Keeps spend on the people a rep will call this month |
| Slot 3 evaluator | No | Evaluators join after a meeting is booked |
| Contacts with only a catch-all or unknown email | Yes for Tier 1 accounts | A phone touch confirms the person still works there |
| Owners of the smallest companies (the map's 1-10 employee row) | Use the business phone from the Local Business Database or the website first | The owner often answers the main line |

Inputs: a valid work email or a profile URL per contact. `find_mobiles` detects which one it got. Send the slot's top contacts only.

## 3. Storage

| Rule | Reason |
|-|-|
| `mobile` and `phone` stay in separate columns | A switchboard and a person's own phone are different channels; mixing them sends a rep's personal call to a reception desk or the reverse |
| Store E.164 (`+14155550142`) | Dialers and CRMs match on it; formatting differences create duplicate contacts |
| Record `mobile_found_at` and `mobile_use` per row | Shows when the number was bought and for which block |
| Keep a `do_not_contact` flag on the contact, synced from the one list | The flag travels with the contact into every tool |

## 4. Running the call block

1. Before the block, remove every number on the do-not-contact list and every contact who replied "remove me" or "not interested" by email.
2. Call in the recipient's own time zone (person state or country from the list). Berman's cold calling article names Tuesday through Thursday as the strongest days.
3. Log a disposition for every call: voicemail, wrong number, or for a connected call one of meeting booked, interested (follow-up set), not now (date to call back), wrong person, referred (name the person and title), not interested, asked not to be called.
4. "Asked not to be called": add to the do-not-contact list the same day, in every tool.
5. Wrong number: blank the `mobile` field and mark `mobile_status = wrong_number`, so nobody pays to call it again.

## 5. Reading the block

At the connected-call count the user set before the block, sort dispositions by title family. A family over the user's wrong-person threshold means the role map picked the wrong title for this product; change the slot titles before the next pull. Referred answers name the right title; add it to the slot's title list. A high not-now share with a low wrong-person share means the list is right and the timing is not: keep the titles, add the callback dates to the CRM, and move trigger-based accounts to the front of the next block. Change one thing per block (titles, script or call window; Berman: test one variable at a time), so the next review shows which change worked.

| Metric | Formula | Use |
|-|-|-|
| Find rate | numbers found / inputs sent | Expected cost of the next run: inputs x find rate x $0.25 |
| Wrong-number rate | wrong numbers / dials | Compare across batches; a batch far above the others gets its source emails re-checked before more dials |
| Connect rate | connected calls / dials | Compare across title families before buying more numbers |
| Wrong-person share | wrong person and referred / connected | Role map check (above) |

## 6. Cost planning

```text
ceiling  = inputs x $0.25
expected = inputs x test find rate x $0.25   (run a test batch first to measure the find rate)
```

For 244 slot 1 contacts the ceiling is $61.00. Show the ceiling and the expected cost, then wait for a yes.

## Sources

- ScraperCity catalog (`find_mobiles` price and inputs): references/scrapercity-catalog.md
- ScraperCity MCP tool schema for `find_mobiles` (profile URLs or work emails, auto-detected): https://www.npmjs.com/package/scrapercity
- ITU-T Recommendation E.164 summary (number format): https://www.twilio.com/docs/glossary/what-e164
- Alex Berman, Cold calling techniques (direct mobile lines, strongest days): https://alexberman.com/cold-calling-techniques
- Alex Berman, Cold email templates (test one variable at a time): https://alexberman.com/cold-email-templates
