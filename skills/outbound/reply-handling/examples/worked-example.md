# Reply Handling Playbook: Texas Dental Review Campaign

Campaign: BrightChair Reviews, three cells of Texas dental practices and dental groups (2,592 contacts, 4 touches). Platform: Instantly. CRM: HubSpot. Reply owner: Priya Shah, SDR, 8am to 6pm Central, with a backup rep for 12pm to 1pm. Escalation: Marcus Lee (account executive), Dana Cole (solutions engineer), Jen Ortiz (sales manager). Target accounts: every dental group in cell C (352 contacts at groups with 20 to 500 employees). Illustrative example: BrightChair, the practices and every person named here are fictional.

Facts from the brief, the only claims the drafts may use: $299 a month per location, cancel any time; a 30 day pilot at one location is available; works with Dentrix, and the review text goes out from the appointment checkout so the front desk changes nothing; a Round Rock practice went from 41 to 163 Google reviews in five months by texting a review link after each visit (the practice agreed to be described by city).

## Inbox Setup

| Setting | Value |
|-|-|
| Stop on reply | On, at company (domain) level: Campaign, Settings, Advanced settings, "Stop sending emails on reply" and "Stop Campaign for Company on Reply" on |
| Stop on auto-reply | Off (Advanced settings, Sending rules), so OOO leads pause until the return date and resume |
| Automatic status tagging | Instantly AI Custom Reply Labels on; automatic actions limited per Automation Boundaries, every other label reviewed by Priya before a reply goes out |
| Global blocklist | Instantly Settings, Blocklist (addresses and whole domains), synced to HubSpot "Do not contact" by a Zapier zap |
| Alerts | Push notification to Priya's phone for Interested, price questions and accepted times; target-account Interested also pages Marcus |
| Open and click tracking | Off |
| Booking link | 15 minute event, Tuesday to Thursday, 9am to 4pm Central |

## Reply Taxonomy

| Class | Example wording | Detect | Response id |
|-|-|-|-|
| Interested: meeting | "Sure, send me a time" | Agreement plus scheduling words | R1 |
| Interested: meeting accepted | "Thursday at 11 works" | An accepted time or calendar acceptance | R3 |
| Interested: price question | "How much is it?" | Price words with no objection | R6 |
| Interested: question | "Does it work with Dentrix?" | Product question, no objection | R8 |
| Referral: named | "Talk to Sarah Kim, our office manager" | Named person | R10, then referral sequence R11 |
| Referral: role only | "Our office manager handles that" | Role, no name | R12 |
| Objection: not interested | "Not interested, thanks" | A plain no | R25 |
| Objection: no need | "We get plenty of reviews" | Problem denied | R13 |
| Objection: competitor | "We use Birdeye and we're happy" | Vendor named | R14 |
| Objection: price | "No budget this year" | Money words with a no | R15 |
| Objection: too expensive | "$299 a location is too much" | Price heard, pushback | R34 |
| Objection: our software does it | "Our practice software already sends review requests" | Bundled feature named | R35 |
| Objection: in-house | "Our front desk asks every patient at checkout" | Staff do it by hand | R27 |
| Not now | "Try us after the new year" | Future date | R19 |
| Wrong person | "I'm the hygienist, not the owner" | Role mismatch, no name | R22 |
| Unsubscribe | "Remove me" | Opt-out words | None |
| Hostile | "This is spam, I'm reporting you", "my attorney", "how did you get this email?" | A trigger word from Automation Boundaries | R26 by a person, or none; threats and data requests forwarded |
| Out of office | "Out until October 26" | Auto-Submitted header or OOO subject | None, pause |
| Bounce | "User unknown" notice from the mail server | Delivery failure report | None, suppress |

## Response Library

Every draft below sends as written. Times are examples from Priya's calendar; she swaps in her open slots.

### R1 Interested: meeting

```text
Great, thanks {{first_name|there}}. Does Tuesday at 10:30am or Wednesday at 2pm Central work for 15 minutes? I'll send the invite to this address with a video link.
```

### R3 Interested: meeting accepted

```text
Thursday, October 15 at 11:00am Central works. The invite is on its way to this address; forward it to anyone else from {{company|the practice}} who should join.
```

### R6 Interested: price question

```text
Fair question. It depends mainly on how many locations {{company|the practice}} runs, so it varies. I can walk you through the options in 15 minutes: does Thursday at 11am or Friday at 1pm Central work?
```

### R8 Interested: product question

```text
Yes, it works with Dentrix. The review text goes out from the appointment checkout, so your front desk doesn't change anything. Want me to show you on a 15 minute call Wednesday at 2pm Central?
```

### R10 Referral: thank the referrer

```text
Thanks {{first_name|there}}, that helps. I'll reach out and mention you sent me.
```

### R11 Referral: first email to the referred person

```text
Subject: {{referrer_first_name|Your colleague}} suggested I reach out

Hi {{first_name|there}}, {{referrer_first_name|your colleague}} said you run the front office, so patient reviews land on your desk. When a patient agrees at checkout and then forgets, the review never gets written. A Round Rock practice went from 41 to 163 Google reviews in five months with a text after each visit, and it works with Dentrix. Would Tuesday at 10am or Wednesday at 2pm Central work for 15 minutes?
```

### R12 Referral: role only

```text
Thanks {{first_name|there}}. What's the best way to reach your office manager?
```

### R25 Objection: not interested

```text
Understood, thanks for letting me know. I won't follow up.
```

### R13 Objection: no need

```text
Fair enough, thanks for the quick reply. I'll close this out and won't follow up.
```

### R14 Objection: competitor

```text
Makes sense, and if Birdeye is working I won't try to talk you out of it. If patients who say yes at checkout and then forget ever start costing you reviews, reply here and I'll show you how we handle them.
```

### R15 Objection: price

```text
Understood. Would a 30 day pilot at one location help you test it first? If not, no problem, I'll leave it there.
```

### R34 Objection: too expensive

```text
Fair. If $299 a month is close to what the reviews bring in, it isn't worth it, and I'd rather you know that now. The 30 day pilot at one location is the cheap way to find out. Want to try that first?
```

### R35 Objection: our software does it

```text
Makes sense if your software already asks. Ours goes out from the Dentrix checkout by text, so the front desk changes nothing. If yours is already getting you steady reviews, you're set.
```

### R27 Objection: in-house

```text
Good, then your front desk already asks. The text after each visit is for patients who say yes at checkout and forget by the parking lot. If asking in person is working, I'll leave it there.
```

### R19 Not now

```text
Thanks {{first_name|there}}. I'll follow up the week of January 11 and won't email before then.
```

### R22 Wrong person

```text
Thanks {{first_name|there}}, sorry for the misfire. Who handles patient reviews at {{company|the practice}}?
```

### R26 Hostile

```text
Sorry for the unwanted email. I found your practice's address in a business contact database, and I've removed it so you won't hear from us again.
```

## SLAs

| Class | First response | Owner | Escalate to |
|-|-|-|-|
| Interested: meeting | 5 minutes in business hours, every account tier | Priya | Target account or VP+ (group owner, COO, VP Operations): Marcus within 15 minutes; others: Priya books within 5 minutes |
| Interested: meeting accepted | 5 minutes: R3 plus the invite | Priya | Marcus added to the invite within 15 minutes for target accounts |
| Interested: price question | 5 minutes in business hours, every account tier: R6 offers the walkthrough | Priya | Marcus within 15 minutes if they ask for a quote or group terms |
| Interested: question | 5 minutes, answered from the brief or with a holding reply | Priya | Dana within 4 business hours for a technical or integration question the brief does not answer |
| Referral: named | Thank the referrer within 2 to 4 business hours; referral enrolled when the Email Finder returns | Priya, then automation | Marcus within 4 business hours if the referred person is VP+ at a target account |
| Referral: role only | 2 to 4 business hours | Priya | None |
| Objection: not interested | 2 to 4 business hours, R25 only | Priya | None |
| Objection (no need, competitor, price) | 2 to 4 business hours | Priya | Jen within 4 business hours for competitor or procurement objections at target accounts |
| Not now | 2 to 4 business hours | Priya | None |
| Wrong person | 2 to 4 business hours | Priya | None |
| Unsubscribe, polite | No reply; suppressed the same day | Automation, Priya checks at 5pm | Jen if any entry is not suppressed the same day |
| Hostile: complaint or profanity | Removal line (R26), sent by Priya, or no reply if the message is abusive; suppressed the same day | Priya | Jen within 4 business hours |
| Hostile: threat or data request | No reply; suppressed the same day | Priya forwards | Jen, who owns threats, within 4 business hours |
| Out of office | No reply; paused to the return date | Automation | None |
| Bounce | No reply; suppressed immediately | Automation | Deliverability owner if a cell passes 2% bounces |

Hot replies that arrive after 6pm are answered first thing the next business day. Escalation times are BrightChair's own settings.

## CRM State Map

| Class | Lead status | Sequence action | Suppress | Deal |
|-|-|-|-|-|
| Interested: meeting | Interested | Stop for every contact at the practice | No | Create, "Meeting requested" |
| Interested: meeting accepted | Meeting booked | Stopped | No | Stage "Meeting scheduled" |
| Interested: price question | Interested | Stop at practice | No | Create, "Engaged" |
| Interested: question | Interested | Stop at practice | No | None until a meeting is set |
| Referral: named | Referred | Stop for referrer | No | Note referrer on the new contact |
| Referral: role only | Referred | Stop for referrer | No | None |
| Objection: not interested | Not interested | Stop | No, permanent; only if they write in first | None |
| Objection: no need | Not interested | Stop | No, permanent; only if they write in first | None |
| Objection: competitor | Competitor: Birdeye or other | Stop; nurture, first touch 6 weeks after the reply, then every 4 to 6 weeks (Berman's nurture cadence), or the renewal date if they gave one | No | None |
| Objection: price | Objection: budget | Stop | No, re-engage in January | None |
| Not now | Nurture until stated date | Stop; HubSpot task on the date | No | None |
| Wrong person | Wrong person | Stop | No | None |
| Unsubscribe | Do not contact | Stop everywhere | Yes, address, permanent | None |
| Hostile | Do not contact | Stop everywhere | Yes, address, permanent; domain if they speak for the practice | None |
| Out of office | Paused | Pause to resume date | No | None |
| Bounce (hard) | Bounced | Stop | Yes, address, permanent | None |

## Suppression Rules

| Event | Scope | Deadline | Reason |
|-|-|-|-|
| Unsubscribe link or "remove me" | Address, every campaign and tool | Same day (Yahoo and Google sender rules allow 2 days at most) | A second email after "remove me" is the one that gets reported as spam |
| "Take our practice off" | Domain | Same day | They spoke for the practice; an email to a colleague next week is the same second email |
| Hostile reply | Address; domain if they speak for the practice | Same day | Keeps Gmail-reported spam under 0.1% |
| Spam complaint | Address | Same day | Google sender guidelines: spam rate under 0.1%, never 0.3% |
| Hard bounce | Address | Immediate | Keeps bounces under 2%, the line past which inbox placement drops |
| Bounce blaming spam, policy or reputation | Sending domain paused, contact kept | Same day | The address is fine; the domain's reputation is the problem |
| Two or three mailbox-full bounces in a row | Address, permanent | After the second or third | Treated as a hard bounce; repeated soft bounces drag the cell's bounce rate up |
| Not interested | Address, every sequence from this sender, permanent | Same day | Keeps the "I won't follow up" promise in R25 |

Every suppression is logged in a Google Sheet with email, scope, reason, message id, received time, suppressed time, tools updated and operator, so the lag is visible.

## Auto-Reply Detection

| Signal | Class | Action |
|-|-|-|
| `Auto-Submitted: auto-replied` or `auto-generated` header | Automatic | No reply (RFC 3834) |
| Delivery failure report saying "user unknown" or "does not exist" | Hard bounce | Suppress |
| Delivery failure saying "mailbox full" or "try again later" | Soft bounce | Platform retries; suppress after two or three in a row |
| Delivery failure blaming spam, policy or reputation | Reputation block | Pause the sending domain, alert the deliverability owner |
| Subject "Automatic reply", "Out of Office", "Respuesta automática" | Out of office | Parse date, pause |
| "back on Monday, October 26" | Out of office with date | Resume October 26 |
| "on maternity leave" with no date | Out of office, long | Pause 60 days (BrightChair's setting) |
| "no longer with the practice" | Left company | Suppress address; look up the replacement |
| "Thank you for contacting us, a team member will respond" | Automatic help desk | Suppress address from outbound |

## Automation Boundaries

AI labelling tool: Instantly AI Custom Reply Labels, with "Automatically tag lead status in replies" on and "Update existing lead labels with AI" off. Instantly shows no confidence score, so a Zapier step sends each reply to BrightChair's own classifier prompt, which returns a class and a confidence. The threshold, queue times and sample size below are BrightChair's settings. Confidence threshold: automation acts alone only when the class is on the auto list and a header rule matched or the classifier reports 0.90 or higher. Human-review queue: a HubSpot view of replies below 0.90, on the never list, or where Instantly's label and the classifier disagree; Priya clears it every business hour, and items older than 2 business hours alert Jen. Weekly misclassification sample: every Monday Jen relabels 50 auto-handled replies from the prior week without seeing the AI label; over 5% wrong in a class turns automation off for that class.

Hostile trigger words (whole word, reply body only, any class): spam, report, reported, junk, blacklist, block, abuse, harass, unsolicited, "how did you get this email"; lawyer, attorney, sue, cease and desist; "delete my data", "what data do you have"; any profanity. A match routes the reply to Priya's queue with automatic sending off for that lead, even when the same reply also says "remove me". Automation may suppress the address; only a person sends anything.

| Class | Automation | Allowed action | Condition |
|-|-|-|-|
| Out of office | Auto | Pause to the return date; 7 days if no date | Auto-Submitted header or OOO subject, or 0.90+ |
| Bounce (hard) | Auto | Suppress address | Delivery failure report naming an unknown user |
| Help desk auto-ack | Auto | Suppress address from outbound | Auto-Submitted header or ticket phrase |
| Unsubscribe, polite | Auto | Suppress in Instantly and HubSpot; no reply | Opt-out words at 0.90+ and no hostile trigger word; below that, suppress and queue |
| Referral: named | Partial | Email lookup runs; Priya sends R10 and approves R11 | Any confidence |
| Not now | Partial | Status and dated task set; Priya sends R19 | 0.90+ |
| Interested, non-target practice | Partial | Label, phone alert, AI draft of R1, R3 or R6; Priya checks it against the brief and sends within 5 minutes | Any confidence |
| Interested, target account | Never | Human only; Priya replies within 5 minutes, Marcus within 15 | Always |
| Hostile | Never | Suppress automatically; Priya decides R26 or no reply; threats to Jen | Any hostile trigger word |
| Other or unclear | Never | Human queue | Always |
| Reputation block | Never | Pause sending domain, alert the deliverability owner | Always |

## Referral Capture

| Step | Tool or action | Detail |
|-|-|-|
| 1 | Parse the reply | First name, last name, practice domain from the referrer's address |
| 2 | ScraperCity Email Finder | Daily batch of named referrals: first name, last name, domain; found addresses come back validated |
| 3 | ScraperCity Lead Database | Role-only referrals: the practice domain plus the title "Office Manager" |
| 4 | Thank the referrer | R10, and stop the referrer's sequence |
| 5 | Enroll | New thread from the referral campaign in Instantly: R11, subject naming the referrer, nothing forwarded |

At this campaign's volume the lookups cost under $2 a month, so they run without a separate approval.

Example from week one: Dr. Nguyen replied "Talk to Sarah Kim, she runs the front office." The lookup returned a validated address for Sarah at Lakeline Family Dental. She received R11 the next morning, with "Dr. Nguyen suggested I reach out" as the subject, and booked a call for Thursday.

## Weekly Review

| Metric | Threshold | Action if breached |
|-|-|-|
| Median time to first response, hot replies | Over 5 minutes in business hours | Add backup coverage; check alert settings |
| Not interested share in a cell | Most human replies in the cell say "not interested" | Targeting is off: pull the cell and rework the segment before more sends |
| Competitor objections | Many "we already use Birdeye" replies | The market buys: sharpen the offer and add a comparison line to touch 2 |
| Unsubscribes | Over 0.5% of prospects in a cell | Follow-ups are too aggressive or not relevant: cut a touch or rewrite it |
| Spam complaints | Approaching 0.1% in Google Postmaster Tools | Pause the cell, review list source and copy |
| Bounce rate per cell | Over 2% | Pause the cell, re-validate the list, alert the deliverability owner |
| Suppression lag | Any entry not suppressed the same day | Fix the sync; audit the week's unsubscribes |
| Referral enrollment lag | A named referral not enrolled after its lookup returned | Check the daily lookup batch ran |
