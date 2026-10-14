# Reply Triage: Ledgerline Vet Clinic Campaign, Tuesday October 13

Illustrative example: Ledgerline, every clinic and every person below are fictional, and the domains end in .example. Sender: Sam, Central time, 8am to 5pm. The user asked for drafts, routing and SLAs.

Brief facts the drafts use: $450 a month per clinic, month-to-month; books closed and a P&L delivered by the 10th of each month; works with QuickBooks Online; clinics can hand over only the month-end close; a two-vet clinic in Boise cut the owner's bookkeeping time from 6 hours to under 1 hour a week (the clinic agreed to be described by city). Platform not named, so settings give Instantly and Smartlead paths.

## Reply Triage

| # | Reply | Class | Send | Within | CRM status | Suppress |
|-|-|-|-|-|-|-|
| 1 | Dr. Amy Chen, Ridgeview Animal Clinic, Denver: "Sure, Thursday at 2 works." | Interested: accepted time | Draft 1, plus the invite in Mountain time | 5 minutes | Meeting booked; deal at "Meeting scheduled" | No |
| 2 | Mark Ellis, Harbor Vet, Tampa: "What does this cost?" | Interested: price question | Draft 2 | 5 minutes | Interested; deal at "Engaged" | No |
| 3 | Tom Becker, Becker Veterinary: "Not me. Talk to Dana Ruiz, she runs our office and does the books." | Referral: named | Draft 3 to Tom; draft 3b to Dana as a new thread, address from ScraperCity Email Finder (Dana Ruiz, beckervet.example) | 2 to 4 business hours | Tom: Referred, sequence stopped. Dana: new contact, referrer Tom Becker | No |
| 4 | Linda Park, Park Pet Hospital: "$450 a month is too expensive for a clinic our size." | Objection: too expensive | Draft 4 | 2 to 4 business hours | Objection: budget | No |
| 5 | Raj Patel, Northside Vet: "Our practice software already does accounting." | Objection: our software does it | Draft 5 | 2 to 4 business hours | Objection: bundled tool | No |
| 6 | Jill Moreno, Mesa Animal Care: "My office manager does our books, we're fine." | Objection: in-house | Draft 6 | 2 to 4 business hours | Objection: in-house | No |
| 7 | Greg Holt, Holt Veterinary: "This is spam. Take me off your list or I'm reporting you." | Hostile: complaint opt-out | Removal line (draft 7), sent by Sam | Suppressed now; line the same day | Do not contact | Yes, address, every tool, permanent |
| 8 | Auto-reply from Karen Wu, Lakeside Vet: "Out of office until Monday, October 26." | Automatic: out of office | No reply | Paused now | Paused; resume Tuesday, October 27 | No |

## Drafts

### 1. Amy Chen, accepted time

```text
Thursday, October 15 at 2:00pm Mountain works. The invite is on its way to this address; forward it to anyone else from Ridgeview who should join.

Sam
```

### 2. Mark Ellis, price question

```text
Fair question. It depends mainly on how many clinics Harbor Vet runs, so it varies. I can walk you through the options in 15 minutes: does Wednesday at 3pm or Thursday at 10am Eastern work?

Sam
```

### 3. Tom Becker, referral thanks

```text
Thanks Tom, that helps. I'll reach out to Dana and mention you sent me.

Sam
```

### 3b. Dana Ruiz, referred (new thread)

```text
Subject: Tom suggested I reach out

Hi Dana, Tom said you run the office at Becker Veterinary and keep the books. When that work waits until the last appointment is done, the month closes late. We close clinic books by the 10th, and a Boise clinic's owner went from 6 hours a week on books to under 1. Would Tuesday at 10am or Wednesday at 2pm Pacific work for 15 minutes?

Sam Ortiz
Client lead, Ledgerline
```

### 4. Linda Park, too expensive

```text
Fair. The Boise clinic owner was spending 6 hours a week on the books before us. If your number is closer to 1, we're not worth it. If it's closer to 6, 15 minutes Thursday at 11am Central would show you the trade.

Sam
```

### 5. Raj Patel, our software does it

```text
Makes sense, your software records the invoices. With us, a person reconciles everything and closes the month by the 10th, in QuickBooks Online. If your software already gets you a closed month on time, you're set.

Sam
```

### 6. Jill Moreno, in-house

```text
Good, then someone already knows your numbers. Some clinics keep that person on bills and payroll and hand us only the month-end close, so the P&L lands by the 10th. If yours has it covered, I'll leave it there.

Sam
```

### 7. Greg Holt, hostile opt-out

```text
Sorry for the unwanted email. I found your address in a business contact database, and I've removed it so you won't hear from us again.
```

## Routing and SLAs

| Class | Owner | Escalate to | Automation |
|-|-|-|-|
| Interested: accepted time, price question (1, 2) | Sam | AE alerted on arrival when the clinic runs more than one location | Partial: label and phone alert; Sam sends |
| Referral (3) | Sam | None | Partial: the address lookup runs on its own; Sam sends the thanks and approves Dana's email |
| Objection (4, 5, 6) | Sam | None | Never sends alone |
| Hostile (7) | Sam | Sales manager, same day | Never sends; may only suppress |
| Out of office (8) | Sequencer | None | Auto |

- Stop on reply for every contact at the clinic. Instantly: Campaign, Settings, Advanced settings, "Stop sending emails on reply" and "Stop Campaign for Company on Reply" on. Smartlead: Campaign Settings, "Company Level Auto-Pause" ticked.
- Out of office pauses to Tuesday, October 27. Instantly: Sending rules, "Stop on auto-reply" off, and Settings, Preferences, AI Automations, "Automatically tag lead status in replies" on. Smartlead: General, AI categorization with Out-of-Office selected, then "Automatically restart ai-categorized OOO when lead returns".
- Greg on one suppression list. Instantly: Settings, Blocklist. Smartlead: Settings, Global Block List. CRM: Do not contact field.
- Hostile words (spam, report, reported, junk, block, abuse, unsolicited, lawyer, attorney, sue) send the reply to Sam with automatic sending off, as a keyword rule in the reply webhook or CRM workflow.

## Open Items

- The brief has no multi-clinic pricing. Confirm Harbor Vet's number before Mark's call.
- Dana's times are Pacific, from Becker Veterinary's Spokane address on the lead record.
- Confirm: the AE for multi-location clinics and the sales manager for hostile replies.
