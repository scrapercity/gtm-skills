# Reply Handling Playbook: Texas Dental Review Campaign

Campaign: BrightChair Reviews, three cells of Texas dental practices and dental groups (2,592 contacts, 4 touches). Platform: Instantly. CRM: HubSpot. Reply owner: Marcus Lee, account executive, 8am to 6pm Central, with a backup rep for 12pm to 1pm. BrightChair is a fictional company used for this example.

## Inbox Setup

| Setting | Value |
|-|-|
| Stop on reply | On, at company (domain) level |
| Stop on auto-reply | Off, so OOO leads pause and resume instead of stopping |
| Automatic status tagging | On; every tag reviewed by Marcus before a reply goes out |
| Global blocklist | Instantly workspace blocklist, synced to HubSpot "Do not contact" by a Zapier zap |
| Alerts | Push notification to Marcus's phone for Interested and Meeting booked |
| Open and click tracking | Off |
| Booking link | 15 minute event, Tuesday to Thursday, 9am to 4pm Central |

## Reply Taxonomy

| Class | Example wording | Detect | Response id |
|-|-|-|-|
| Interested: meeting | "Sure, send me a time" | Agreement plus scheduling words | R1 |
| Interested: info | "How much is it?" | Price or material request | R6 |
| Interested: question | "Does it work with Dentrix?" | Product question, no objection | R8 |
| Referral: named | "Talk to Sarah Kim, our office manager" | Named person | R10, then referral sequence R11 |
| Referral: role only | "Our office manager handles that" | Role, no name | R12 |
| Objection: no need | "We get plenty of reviews" | Problem denied | R13 |
| Objection: competitor | "We use Birdeye" | Vendor named | R14 |
| Objection: price | "No budget this year" | Money words | R15 |
| Not now | "Try us after the new year" | Future date | R19 |
| Wrong person | "I'm the hygienist, not the owner" | Role mismatch, no name | R22 |
| Unsubscribe | "Remove me" | Opt-out words | None |
| Angry | "How did you get this email?" | Hostility or data question | R26 then suppress |
| Out of office | "Out until October 27" | Auto-Submitted header or OOO subject | None, pause |
| Bounce | 550 5.1.1 user unknown | Delivery status report | None, suppress |

## Response Library

### R1 Interested: meeting

```text
Great, thanks Dr. Patel. Does Tuesday at 10:30am or Wednesday at 2pm Central work for 15 minutes? I'll send an invite to this address with a video link.
```

### R6 Interested: price question

```text
It depends on the number of locations. Most single-location practices pay $299 a month, cancel any time. Can we take 10 minutes Thursday so I can show you what the first 30 days look like for your practice?
```

### R8 Interested: product question

```text
Yes, it works with Dentrix. The review text goes out from the appointment checkout, and your front desk doesn't change anything in Dentrix. Want me to show you on a 15 minute call?
```

### R10 Referral: thank the referrer

```text
Thanks Dr. Nguyen, I'll reach out to Sarah and mention you sent me. Appreciate it.
```

### R11 Referral: first email to the referred person

```text
Hi Sarah, Dr. Nguyen suggested I reach out about Google reviews. We helped a Round Rock practice go from 41 to 163 reviews in five months by texting a review link after each visit. Worth 15 minutes to see if it fits Lakeline Family Dental?
```

### R12 Referral: role only

```text
Thanks Dr. Ortiz. What's the best way to reach your office manager?
```

### R13 Objection: no need

```text
Fair enough, thanks for saying so. Is that because reviews are already handled at checkout, or because it isn't a priority this year?
```

### R14 Objection: competitor

```text
Makes sense, Birdeye is solid. What made you pick them? A few of our practices switched for the per-location pricing, so if that ever comes up, I'm happy to compare.
```

### R15 Objection: price

```text
Understood. Would a 30 day pilot at one location make sense to test it first, or is this a next-year conversation?
```

### R19 Not now

```text
Thanks, I'll follow up the week of January 12. Is this still the best address?
```

### R22 Wrong person

```text
Thanks, sorry for the misfire. Who handles patient reviews at the practice?
```

### R26 Angry

```text
Sorry for the unwanted email. I found your practice's address in a business contact database, and I've removed it so you won't hear from us again.
```

## SLAs

| Class | First response | Owner |
|-|-|-|
| Interested: meeting | 1 business hour, 2 at most | Marcus |
| Interested: info | 2 business hours | Marcus |
| Interested: question | 2 business hours | Marcus |
| Referral: named | Thank the referrer same business day; referral enrolled within 1 business day | Marcus, then automation |
| Referral: role only | Same business day | Marcus |
| Objection (all types) | Same business day | Marcus |
| Not now | Same business day | Marcus |
| Wrong person | Same business day | Marcus |
| Unsubscribe | No sales reply; suppressed within 1 business day | Automation, Marcus checks at 5pm |
| Angry | No sales reply beyond R26; suppressed within 1 business day | Marcus |
| Out of office | No reply; paused to return date plus 1 business day | Automation |
| Bounce | No reply; suppressed immediately | Automation |

## CRM State Map

| Class | Lead status | Sequence action | Suppress | Deal |
|-|-|-|-|-|
| Interested: meeting | Interested | Stop for every contact at the practice | No | Create, "Meeting requested" |
| Interested: info | Interested | Stop at practice | No | Create, "Engaged" |
| Interested: question | Interested | Stop at practice | No | None until a meeting is set |
| Referral: named | Referred | Stop for referrer | No | Note referrer on the new contact |
| Referral: role only | Referred | Stop for referrer | No | None |
| Objection: no need | Not interested | Stop | No, 180 day hold for this offer | None |
| Objection: competitor | Competitor: Birdeye or other | Stop | No, 180 day hold | None |
| Objection: price | Objection: budget | Stop | No, re-engage in January | None |
| Not now | Nurture until stated date | Stop; HubSpot task on the date | No | None |
| Wrong person | Wrong person | Stop | No | None |
| Unsubscribe | Do not contact | Stop everywhere | Yes, address, permanent | None |
| Angry | Do not contact | Stop everywhere | Yes, address, permanent; domain if they speak for the practice | None |
| Out of office | Paused | Pause to resume date | No | None |
| Bounce (hard) | Bounced | Stop | Yes, address, permanent | None |

## Suppression Rules

| Event | Scope | Deadline | Law or policy |
|-|-|-|-|
| Unsubscribe link or "remove me" | Address, every campaign and tool | 1 business day internal; 2 days Yahoo; 10 business days legal limit | CAN-SPAM (FTC); Yahoo sender requirements |
| "Take our practice off" | Domain | 1 business day | CAN-SPAM (FTC) |
| Spam complaint | Address | Same day | Google sender guidelines (keep under 0.1%) |
| Hard bounce 5.1.x | Address | Immediate | Internal policy, keeps bounces under 2% |
| Reputation block 5.7.1 | Sending domain paused, contact kept | Same day | Google sender guidelines |
| Soft bounce three times | Address, 90 days | After third bounce | Internal policy |
| Not interested | Address, this offer, 180 days | Same day | Internal policy |

Every suppression is logged in a Google Sheet with email, scope, reason, message id, received time, suppressed time, tools updated and operator.

## Auto-Reply Detection

| Signal | Class | Action |
|-|-|-|
| `Auto-Submitted: auto-replied` or `auto-generated` header | Automatic | No reply (RFC 3834) |
| Null return path or `multipart/report; report-type=delivery-status` | Bounce | Read status code |
| 5.1.1, 5.1.10, "user unknown", "does not exist" | Hard bounce | Suppress |
| 4.x.x, "mailbox full" | Soft bounce | Platform retries; suppress after 3 |
| 5.7.1 or "blocked", "policy", "reputation" | Reputation block | Pause domain, route to email-deliverability |
| Subject "Automatic reply", "Out of Office", "Respuesta automática" | Out of office | Parse date, pause |
| "back on Monday, October 27" | Out of office with date | Resume October 28 |
| "on maternity leave" with no date | Out of office, long | Pause 60 days |
| "no longer with the practice" | Left company | Suppress address; Lead Database lookup for replacement |
| "Thank you for contacting us, a team member will respond" | Automatic help desk | Suppress address from outbound |

## Referral Capture

| Step | Tool or action | Detail | Cost |
|-|-|-|-|
| 1 | Parse the reply | First name, last name, practice domain from the referrer's address | $0.00 |
| 2 | `find_emails` | Batch of the week's named referrals: contacts [{first_name, last_name, domain}] | $0.05 per email found, free if not found |
| 3 | `validate_emails` | Every found address before enrolling | $0.0072 per email |
| 4 | `query_lead_database` | Role-only referrals: companyDomain plus title "Office Manager", limit 10 | Included on Growth |
| 5 | Enroll | Referral campaign in Instantly, first line names the referrer (R11) | $0.00 |
| 6 | Thank the referrer | R10, stop the referrer's sequence | $0.00 |

Month one estimate: 24 named referrals, 17 found ($0.85), 17 validated ($0.12), 3 mobiles found for referrals who asked for a call via `find_mobiles` ($0.75), 9 role-only lookups in the Lead Database ($0.00). Total $1.72, under the $5 approval threshold; `check_wallet` runs every Monday.

Example from week one: Dr. Nguyen replied "Talk to Sarah Kim, she runs the front office." `find_emails` with first_name "Sarah", last_name "Kim", domain "lakelinefamilydental.example" returned a validated address for $0.05. Sarah received R11 the next morning and booked a call for Thursday.

## Weekly Review

| Metric | Threshold | Action if breached |
|-|-|-|
| Median time to first response, Interested | Over 2 business hours | Add backup coverage; check alert settings |
| Not interested share in a cell | Over 30% of human replies | Send the cell back to cold-email-strategy for a segment change |
| Competitor objections | Over 20% of human replies | Sharpen the mechanism; add a comparison line to touch 2 |
| Angry replies | Over 5% of human replies, or any spam complaint | Pause the cell, review list source and copy |
| Bounce rate per cell | Over 2% | Pause the cell, re-run validate_emails, route to email-deliverability |
| Suppression lag | Any entry over 2 days | Fix the sync; audit the week's unsubscribes |
| Referral enrollment lag | Over 1 business day | Run find_emails daily instead of weekly |
