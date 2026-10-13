# Cold Email Campaign Plan: Review Software for Texas Dental Practices

Prepared: 2026-10-12. Owner: Head of Growth, BrightChair Reviews (a fictional review-request SaaS used for this example). Sending platform: Instantly.

## Campaign Summary

| Field | Value |
|-|-|
| Goal | 15 meetings held by 2027-01-15 |
| Product and average deal value | Text-based review requests for dental practices, $299 per location per month, about $3,600 first-year value |
| Cells | 3 (A: well rated, few reviews; B: low rated; C: multi-location dental groups) |
| Validated contacts | 2,592 |
| Touches per contact | 4 over 12 business days |
| Sending window | 2026-10-19 to 2026-12-18 (43 weekdays after skipping Thanksgiving and the day after), 8am to 11am recipient time |
| ScraperCity cash cost | $149.00 (the Growth plan month; $50.63 of usage is drawn from its $159 of credits) |

## Offer

Offer sentence: We help 3 to 6 chair dental practices in Texas get from under 60 Google reviews to over 150 in 5 months by texting a review link to every patient within an hour of their visit.

| Check | Value |
|-|-|
| Proof source (client, date, metric) | Round Rock practice, May to September 2026, Google Business Profile review count 41 to 163 |
| Ask | Cells A and B: "Want the text we send?" Cell C: "Worth 15 minutes to compare locations?" |
| Risk reducer | 30 day pilot on one location, cancel any time |
| Offer strength score (0 to 6) | 6 |

## Campaign Cells

| Cell | Segment | Buyer | Offer | Trigger | Framework | Validated contacts |
|-|-|-|-|-|-|-|
| A | Dentists in TX, rating 4.5 or higher, 20 to 80 reviews, has website | Practice owner or office manager | Review texts after each visit, pilot | Strong rating, low review count vs local leaders | 3C | 1,310 |
| B | Dentists in TX, rating 4.0 or lower, 20 to 150 reviews, has website | Practice owner | Same offer, framed as lifting the average | Rating at or below 4.0 | Problem-first question | 930 |
| C | Dental groups, 20 to 500 employees, US HQ in TX | Director or VP of Operations | Per-location review dashboard, pilot on 2 sites | Fit only (multi-location) | PAS | 352 |

## Contact Thesis

| Cell | Thesis | Evidence field | Falsified if |
|-|-|-|-|
| A | Owners with a 4.5+ rating but under 80 reviews lose new patients to practices with 150+, and our Round Rock result shows the count can triple in 5 months | `total_score`, `reviews_count` | Under 0.5 positive replies per 100 delivered after 300 delivered |
| B | Owners at 4.0 or below know the rating hurts bookings; more recent happy-patient reviews lift the average fastest | `total_score`, `reviews_count` | Same threshold, or over 30% of replies angry |
| C | Operations leaders at groups need every location on one review process; a pilot on 2 sites is a low-risk test | `title`, `employees_count`, `company_industry` | Under 1 positive reply per 100 delivered after 200 delivered |

## List Sources and Cost

| Cell | Tool | Parameters | Raw count | Unit price | Cost |
|-|-|-|-|-|-|
| A | `query_local_business_database` | category ["Dentist"], state "TX", minRating 4.5, minReviews 20, maxReviews 80, hasWebsite true, hasEmail true, excludeDelivered true | 1,560 | included on Growth | $0.00 |
| B | `query_local_business_database` | category ["Dentist"], state "TX", maxRating 4.0, minReviews 20, maxReviews 150, hasWebsite true, hasEmail true, excludeDelivered true | 1,120 | included on Growth | $0.00 |
| C | `query_lead_database` | title "Director of Operations, VP Operations, COO", industry ["hospital & health care"], keywords ["dental"], companyState ["Texas"], minEmployees 20, maxEmployees 500, hasEmail true | 420 | included on Growth | $0.00 |
| A and B | `find_emails` | 900 named dentists whose listing shows only a generic inbox, first_name, last_name, domain | 495 found (55% planning assumption) | $0.05 per email found | $24.75 |
| All | `validate_emails` | 3,100 database addresses plus 495 found | 3,595 | $0.0072 | $25.88 |

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Growth plan, one month | 1 | $149.00 | $149.00 |
| Email Finder | 495 found | $0.05 | $24.75 |
| Email Validator | 3,595 | $0.0072 | $25.88 |
| Total cash (usage $50.63 drawn from the $159 plan credits) | | | $149.00 |

The $50.63 of enrichment and validation is covered by the $159 of monthly credits on Growth. The count and this table were shown to the owner, who approved the paid steps on 2026-10-12 after `check_wallet` showed a $212.40 balance.

Validation result: 2,951 valid, 372 catch-all held, 272 invalid removed. After keeping one address per business (the named dentist when valid, else the practice inbox), sendable contacts are 1,310 (A), 930 (B) and 352 (C). The 372 catch-all addresses sit in a hold cell capped at 36 sends a day (10% of capacity).

## Touch Map

| Touch | Day | Cell | Job | Thread | Branch |
|-|-|-|-|-|-|
| 1 | 0 | All | Open: review count or rating fact, Round Rock proof, one question | New | Reply: stop all touches for that practice and classify in reply-handling |
| 2 | 3 | All | Proof: second result (a Katy practice from 3.8 to 4.4 stars in 4 months) | Same | Reply: stop; out of office: pause to return date plus 1 day |
| 3 | 7 | A, B | Resource: offer the exact text message template | Same | Reply: stop; wrong person: capture referral and run find_emails on the named person |
| 3 | 7 | C | Angle: location-by-location comparison | Same | Reply: stop; referral: route to the named regional manager |
| 4 | 12 | All | Breakup: close the file or name the right person | Same | Reply: stop; no reply: suppress 60 days, then eligible for a new offer |

Branches on every touch: hard bounce suppresses the address and pauses the cell if bounces pass 2%; unsubscribe or "remove me" suppresses across every campaign within 2 days; spam complaint suppresses and cuts the domain's volume by half; a positive reply stops touches for every contact at that practice.

## Volume and Capacity

| Input | Value |
|-|-|
| Validated contacts (V) | 2,592 |
| Touches (T) | 4 |
| Warmed inboxes (I) | 12 (4 domains x 3 inboxes, warmed since 2026-09-14) |
| Sends per inbox per day (S) | 30 |
| Total sends (V x T) | 10,368 |
| Daily capacity (I x S) | 360 per day |
| Sending days | 10,368 / 360 = 28.8, rounded to 29 |
| New contacts started per day | 360 / 4 = 90 |

Week 1 runs at 15 sends per inbox per day (180 total) while bounce and complaint data comes in, then steps to 30. With the slower first week, the last contacts start around sending day 31 and finish touch 4 about 9 sending days later, on day 40 of the 43 available. Meeting capacity: two account executives with 10 first-call slots a week each, well above the 3 to 4 meetings a week this plan targets.

## Test Plan

| Test | Cell | Variable | Variant A | Variant B | Per variant | Decision metric | Stop rule |
|-|-|-|-|-|-|-|-|
| 1 | A | Ask | "Worth 10 minutes?" | "Want the text we send?" | 200 delivered | Positive replies per 100 delivered | Winner at 2x and 5+ positive replies; tie after 300 each |
| 2 | B | First line | Rating stated with competitor counts | Rating stated alone | 200 delivered | Positive replies per 100 delivered | Same; kill cell B under 0.5 per 100 after 300 |
| 3 | C | Offer | Pilot on 2 locations | Free review gap report for all locations | 150 delivered | Positive replies per 100 delivered | Read result at 150 each; cell too small for a second test |

## Measurement Funnel

| Stage | Floor | Target | Expected count at target |
|-|-|-|-|
| Contacts sent touch 1 | 2,592 | 2,592 | 2,592 |
| Delivered (bounce under 2%, target 1%) | 2,540 | 2,566 | 2,566 |
| All replies | 2% | 4% | 103 |
| Positive replies per 100 delivered | 0.5 | 1.5 | 38 |
| Positive reply to meeting booked | 40% | 50% | 19 |
| Meetings held | 70% | 80% | 15 |
| Opportunities (pilot started) | 25% | 40% | 6 |

Opens are logged for deliverability diagnosis only and never decide a test. ScraperCity data cost per meeting held at target: $149.00 / 15 = $9.93.

## Compliance and Suppression

| Item | Rule | Law or policy |
|-|-|-|
| Sender identity and subject | Real name and BrightChair domain in From; subjects describe the email | CAN-SPAM (FTC) |
| Postal address | BrightChair's registered office address in every touch | CAN-SPAM (FTC) |
| Opt-out | "Reply 'no thanks' and I won't email again" in every touch, plus one-click unsubscribe header | CAN-SPAM; Google and Yahoo sender rules |
| Opt-out timing | Processed same day, never later than 2 days | Yahoo (2 days), CAN-SPAM (10 business days) |
| Authentication | SPF, DKIM, DMARC p=none with alignment on all 4 domains | Google, Yahoo, Microsoft Outlook sender rules |
| Spam rate | Pause a domain at 0.1% in Postmaster Tools | Google sender guidelines |
| Geography | Texas practices only; no Canadian or EU addresses | CASL and GDPR avoided by scope |
| Suppression list | Current customers, open deals, prior unsubscribes loaded before launch | Internal policy, CAN-SPAM |

## Handoff

| To | What they receive |
|-|-|
| cold-email-copywriting | Offer sentence, three cell cards, proof lines (Round Rock, Katy), merge fields `contact_first_name`, `title`, `city`, `total_score`, `reviews_count`, touch jobs |
| reply-handling | Touch map branches, 2 business hour SLA for positive replies, referral capture with find_emails |
| sending-platforms | 3 campaigns plus a catch-all hold campaign in Instantly, 12 inboxes, 30 per day ceiling, stop on reply at company level |
| email-deliverability | Bounce pause at 2%, spam pause at 0.1%, weekly Postmaster review |
| outbound-unit-economics | Funnel targets and the $149.00 data cost for cost-per-meeting tracking |
