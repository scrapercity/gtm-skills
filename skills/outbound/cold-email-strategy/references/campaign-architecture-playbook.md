# Campaign Architecture Playbook

Decision tables for turning one market into campaign cells, choosing the touch pattern, sizing inbox capacity, and running tests that produce a decision. Numbers here are planning defaults and dated benchmarks; replace them with your own after the first 500 delivered emails.

## 1. Cell splitting rules

Split a list into separate cells when any of these change. Keep them together when only cosmetic fields change (first name, city name in the same metro).

| Variable | Split? | Reason |
|-|-|-|
| Buyer title or function (owner vs office manager; VP Sales vs RevOps) | Yes | Different problem, different proof |
| Business type (dentist vs orthodontist; Shopify apparel vs Shopify supplements) | Yes | Proof must come from the same type |
| Size band (1 to 10 vs 50 to 200 employees; under 20k vs over 100k monthly visits) | Yes | Ability to pay and buying process differ |
| Trigger (new app installed, low rating, hiring, none) | Yes | First line and "why now" differ |
| Offer or price point | Yes | You cannot attribute results otherwise |
| Country | Yes when the law differs (US, Canada, UK, EU) | CAN-SPAM, CASL, PECR and GDPR need different handling |
| City within one country and segment | No | Merge field only |
| Rating band inside a local category | Yes if the angle differs (praise vs fix) | 3C for 4.6+, problem-first under 4.0 |

### Cell count by list size

| Validated contacts available | Cells | Why |
|-|-|-|
| Under 600 | 1 | Two cells of 300 cannot both reach 200 delivered per variant |
| 600 to 2,000 | 2 | Each cell supports one A/B test |
| 2,000 to 10,000 | 2 to 4 | Room for a segment test and an offer test |
| Over 10,000 | 3 to 6 | Add cells only if each keeps 1,500+ contacts |

## 2. Sequence vs cycle mailing

| Market size (validated) | Deal value | Pattern | Touches | Re-mail rule |
|-|-|-|-|-|
| Under 2,000 | Over $10,000 | Account-based sequence, CEO first then next level after 1 to 2 weeks | 4 to 5 per person | New angle after 90 days |
| 2,000 to 50,000 | Any | Standard sequence | 4 | Non-responders re-enter after 60 days with a new offer or trigger |
| Over 50,000 | Under $5,000 | Cycle mailing, one touch per person per cycle | 1 per cycle | Every 30 to 60 days, fresh copy each cycle |
| Over 50,000 | Over $5,000 | Short sequence | 2 to 3 | Re-mail after 60 days |

Sources: Berman's follow-up guide (4 to 6 follow-ups over 2 to 3 weeks); a TAM breakdown on his site (one touch per 30 to 60 day cycle); Hunter 2025 (follow-up campaigns average 4.9% replies vs 3% without, unsubscribes rise after touch 3); Instantly 2026 (about 58% of replies from the first email).

## 3. Touch jobs

Every touch has one job. If two touches share a job, cut one.

| Job | What the touch carries | Good after |
|-|-|-|
| Open | Trigger or observation, one proof line, one question | Nothing (first touch) |
| Proof | A second, different result or a short case study | Open |
| Angle | A different problem the same buyer has | Proof |
| Referral | Ask who owns this if not them | Angle |
| Breakup | Offer to close the file; easy yes or no | Any |
| Resource | Offer a specific asset (flow map, audit, sample list) instead of a call | Open or Proof |

### Default 4 touch map

| Touch | Day | Thread | Job | Branch |
|-|-|-|-|-|
| 1 | 0 | New | Open | Reply: stop all touches, classify in `reply-handling` |
| 2 | 3 | Same | Proof | Reply: stop; OOO: pause to return date |
| 3 | 7 | Same | Angle or Resource | Reply: stop; wrong person: referral capture |
| 4 | 12 to 14 | Same | Breakup | Reply: stop; no reply: suppress 60 days then re-mail eligible |

Branches that apply on every touch:

| Event | Action |
|-|-|
| Hard bounce | Suppress the address permanently; if the cell's bounce rate passes 2%, pause the cell and re-validate |
| Unsubscribe or "remove me" | Suppress across every campaign and domain within 2 days (Yahoo) and never later than 10 business days (CAN-SPAM) |
| Spam complaint | Suppress; if the domain's Gmail spam rate nears 0.1%, cut volume |
| Positive reply | Stop the sequence for everyone at that company |
| Auto reply with a return date | Pause until the return date plus 1 business day |

## 4. Capacity planning

Inputs: validated contacts (V), touches per contact (T), warmed inboxes (I), sends per inbox per day (S), sending days per week (5).

- Total sends = V x T
- Daily capacity = I x S
- Sending days needed = (V x T) / (I x S)
- New contacts started per day = (I x S) / T, once the pipeline is full

### Inbox table at 30 sends per inbox per day, 4 touches

| Contacts per month (new) | Sends per month | Sends per day (21 days) | Inboxes needed | Domains at 3 inboxes each |
|-|-|-|-|-|
| 1,000 | 4,000 | 191 | 7 | 3 |
| 2,500 | 10,000 | 477 | 16 | 6 |
| 5,000 | 20,000 | 953 | 32 | 11 |
| 10,000 | 40,000 | 1,905 | 64 | 22 |

Round up. Add 20% spare inboxes so one burned domain does not stall the campaign.

### Ramp

| Week of a new inbox | Sends per inbox per day | Condition to move up |
|-|-|-|
| 1 to 2 | Warmup only | Warmup tool shows inbox placement, no bounces |
| 3 | 10 to 15 | Bounce under 2%, no complaint spike |
| 4 | 20 | Same |
| 5 and later | 30 (ceiling 50) | Gmail spam rate under 0.1% in Postmaster Tools |

Sources: Berman's beginner setup (3 to 5 domains, 2 to 3 inboxes per domain, 2 to 4 weeks warmup, under 50 per inbox per day); his templates page (10 to 20 a day on new domains over 2 to 4 weeks, bounces under 2%); Google's spam rate thresholds.

### Meeting capacity check

Positive replies needed per week = meetings the team can take / show-to-meeting conversion. If the plan produces more positive replies than the team can answer inside the SLA, cut volume. Reply speed decays faster than list freshness.

## 5. Funnel targets (starting hypotheses)

| Stage | Floor | Target | Source and date |
|-|-|-|-|
| Bounce rate | under 2% | under 1% | Berman templates page; Google bulk sender guidance on list hygiene |
| Spam complaint rate (Gmail) | under 0.3% | under 0.1% | Google, 2024 |
| Reply rate, all replies | 2% | 4% | Instantly 2026 (3.43%), Hunter 2025 (4.1%) |
| Positive replies per 100 delivered | 0.5 | 1.5 | Planning default; replace after 500 delivered |
| Positive reply to meeting booked | 40% | 60% | Planning default |
| Meeting booked to held | 70% | 85% | Planning default |

Opens are reported but never used for a decision. Apple Mail Privacy Protection preloads images and logs opens that did not happen (Postmark, 2021, updated 2022).

## 6. Test order and stop rules

Test in this order, one variable at a time, inside one cell:

| Order | Variable | Why this order |
|-|-|-|
| 1 | Offer (result, mechanism, ask type) | 30% of results per Berman, and the biggest lever after deliverability |
| 2 | Segment (title, size band, trigger) | Same weight as offer; a bad segment hides a good offer |
| 3 | First line (trigger vs observation vs compliment) | Changes relevance |
| 4 | Ask (call vs resource vs referral) | Changes reply friction |
| 5 | Subject line | Smallest lever once opens are noisy |

| Rule | Value |
|-|-|
| Minimum per variant | 100 delivered; 200 when expected positive replies are under 2% |
| Decision metric | Positive replies per 100 delivered |
| Call a winner | Leader has at least 2x the positive replies of the other variant and at least 5 positive replies |
| Call a tie | Neither condition after 300 delivered per variant; keep the cheaper or simpler variant |
| Kill a cell | Under 0.5 positive replies per 100 delivered after 300 delivered, with bounces under 2% |
| Pause everything | Bounces over 3% on any cell, or a Gmail spam rate at 0.3% |

Berman's Lean B2B interview describes reworking an approach when 20 emails produce fewer than about 4 strongly positive replies in an early market test; use that as a fast signal for very small, high-value markets, not as a general threshold.

## 7. Diagnosis tree

| Symptom | Likely cause | Check | Fix |
|-|-|-|-|
| Bounces over 2% | Unvalidated or stale list | Validation status mix | Re-validate; drop catch-all from main cell |
| Sends go out, near zero replies of any kind | Mail in spam, or offer gives no reason | Seed test placement, then offer sentence | Fix placement first; then rewrite the offer |
| Many replies, mostly "not interested" | Wrong segment or title | Reply reasons by cell | Change segment or buyer title |
| "We already have someone" | Market buys; offer not differentiated | Count of vendor objections | Sharpen the mechanism; position as complement |
| Positive replies, few meetings | Slow response or heavy ask | Median reply time | Answer inside 2 business hours; offer two times |
| Meetings, no deals | Sales process or price | Call notes | Outside this skill |

## Sources

- https://alexberman.com
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://hunter.io/the-state-of-cold-email-2025
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
