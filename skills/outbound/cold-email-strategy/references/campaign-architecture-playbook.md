# Campaign Architecture Playbook

Decision tables for turning one market into campaign cells, choosing the touch pattern, sizing inbox capacity, and running tests that produce a decision. Every number here is sourced, arithmetic, or an input the user supplies; replace assumed rates with measured ones at the first read.

## 1. Cell splitting rules

Start from recent won deals: write down what was true of each buyer when they bought (business type, size, title, the event that made it urgent, what they used before). The first cell is the slice that repeats most often in that list. Jordan Crawford's Pain-Qualified Segment idea runs the same direction: build the list from the situation past buyers were in. With no won deals yet, the first cell is the segment where your one measured result came from.

Split a list into separate cells when any of these change. Keep them together when only cosmetic fields change (first name, city name in the same metro).

| Variable | Split? | Reason |
|-|-|-|
| Buyer title or function (owner vs office manager; VP Sales vs RevOps) | Yes | Different problem, different proof |
| Business type (dentist vs orthodontist; Shopify apparel vs Shopify supplements) | Yes | Proof must come from the same type |
| Size band (1 to 10 vs 50 to 200 employees; under 20k vs over 100k monthly visits) | Yes | Ability to pay and buying process differ |
| Trigger (new app installed, low rating, hiring, none) | Yes | First line and "why now" differ |
| Offer or price point | Yes | You cannot attribute results otherwise |
| City within one country and segment | No | Merge field only |
| Rating band inside a local category | Yes if the angle differs (praise vs fix) | 3C for the high band, problem-first for the low band |

### Personalization depth per cell

Berman's templates page describes three depths: segment (role, industry, size), account (news, funding, hiring, a change) and person (a post, a talk), and suggests matching depth to the buyer. Depth costs research time per contact, so the deal value sets how deep a cell can afford to go; the user sets the cutoffs from what an hour of research is worth.

| Depth | What the first line uses |
|-|-|
| Segment (lowest deal values) | A list field (rating, review count, platform, app) |
| Account | A dated trigger or a computed fact about the company |
| Person (highest deal values, inside an account-based plan, section 8) | Something the person said or did, checked by hand |

### Cell count

A cell is worth splitting out only if it holds its read size: two variants at 100 to 200 or more delivered each (Berman's templates page), so 200 to 400 or more validated contacts. Capacity sets how many launch at once. Sending days to a read = read size / new contacts per day, and parallel cells share the new contacts. At 3 touches per contact, 30 sends per inbox (Instantly) and a 400-contact read:

| Warmed inboxes at 30 a day | Sends a day | New contacts a day (3 touches) | Sending days to 400 in one cell | Sending days to 400 in each of two cells |
|-|-|-|-|-|
| 3 | 90 | 30 | 14 | 27 |
| 4 | 120 | 40 | 10 | 20 |
| 6 | 180 | 60 | 7 | 14 |
| 12 | 360 | 120 | 4 | 7 |

Launch the cells that reach their read by the read date the plan sets; queue the rest. A queued cell launches on a date in the plan: when the first cell has its read or when new inboxes finish warmup, whichever comes first.

## 2. Touches per contact, and sequence vs cycle mailing

### How many touches

Hunter's State of Email Outreach 2026 (31 million emails sent by Hunter users in 2025) found that three messages produced about twice the replies of one (6.8% against 3.3%), and that three was the best balance in the 2025 data, after four had peaked the year before. Instantly's 2026 benchmarks put about 58% of replies on the first email.

| Situation | Touches | Why |
|-|-|-|
| Default, and whenever validated contacts are waiting for a first touch | 3 | Each extra touch costs new contacts: at 90 sends a day, 3 touches start 30 contacts a day and 4 start 22 |
| No validated contacts left to start and no new market approved, so inboxes would sit idle | Add a fourth touch, a breakup, for contacts still in sequence | The extra touch uses capacity that would otherwise go unused |
| Account-based, high deal value | 3 emails plus calls (section 8) | Nilsson's three email arc |

### Sequence or cycle

Berman's TAM breakdown says cycle mailing works when the market or the deal is large enough and sets no cutoff. The capacity test: a 60-day cycle holds about 42 sending days (Hunter's 21 a month), so cycle mailing fills the inboxes only when validated contacts are at or above daily capacity x 42.

| Situation | Pattern | Touches | Re-mail rule |
|-|-|-|-|
| A short list of high-value accounts with several buyers each | Account-based sequence, CEO first then next level after 1 to 2 weeks (Berman) | 3 to 4 per person | Rest 60 days, then a new angle |
| Validated contacts under daily capacity x 42 | Standard sequence | 3 (a fourth only when no new contacts are waiting) | Rest 60 days, then a new offer or trigger |
| Validated contacts at or above daily capacity x 42 | Cycle mailing, one touch per person per cycle | 1 per cycle | Rest 60 days between cycle emails, fresh copy each cycle |

### The rest rule (one rule for every pattern)

| Rule | Value |
|-|-|
| Rest after a sequence ends with no reply | 60 days before any new touch |
| Rest between cycle emails | 60 days (the top of Berman's 30 to 60 day range, so cycle mailing and sequences share one number) |
| Re-enrollment | Only with a new angle: a new offer, trigger or proof line |
| Before re-enrolling | Re-validate before every send cycle (Berman's TAM breakdown) |

Write the same 60 into the touch map, the hygiene section and the sequencer settings. A plan that says 60 in one place and 90 in another gives the sequencer two answers.

Sources: Berman's follow-up guide (4 to 6 follow-ups over 2 to 3 weeks, 3 to 5 days apart); a TAM breakdown on his site (one touch per 30 to 60 day cycle); Hunter 2026 (three messages); Hunter 2025 (unsubscribes rise after the third follow-up); Instantly 2026 (about 58% of replies from email 1).

## 3. Touch jobs, routing and channels

Every touch has one job. If two touches share a job, cut one.

| Job | What the touch carries | Good after |
|-|-|-|
| Open | Trigger or observation, one proof line, one question | Nothing (first touch) |
| Proof | A second, different result or a short case study | Open |
| Angle | A different problem the same buyer has | Proof |
| Referral | Ask who owns this if not them | Angle |
| Breakup | Offer to close the file; easy yes or no | Any |
| Resource | Offer a specific asset (flow map, audit, sample list) instead of a call | Open or Proof |

### Default touch map (days are business days after touch 1)

| Touch | Day | Thread | Job | Branch |
|-|-|-|-|-|
| 1 | 0 | New | Open | Reply: stop all touches at that company, route per the table below |
| 2 | 3 | Same | Proof | Reply: stop; out of office: pause to return date |
| 3 | 6 | Same | Angle or Resource, ending with an easy out | Reply: stop; no reply: rest 60 days, then eligible only with a new angle |
| 4 (only when no new contacts are waiting) | 10 | Same | Breakup | Same as touch 3; touch 3 then drops the easy out |

### Reply routing (every plan carries this table with names)

| Event | Action | Owner | SLA | State after |
|-|-|-|-|-|
| Positive reply | Answer with two specific times or a booking link and ask for nothing else; documents or access come after the call is booked; stop touches for everyone at that company | The person who takes first calls, with phone reply alerts; the backup covers set hours | Within 5 minutes in business hours (Berman's follow-up guide; his templates page allows 2 to 4 hours as the outer limit) | Meeting pending |
| Asks for info or price | Two or three sentences, one case study, a proposed time; no PDF. Berman's follow-up guide keeps pricing out of email; a flat price the user gives is stated, since "it depends" would be untrue | Same | Same as a positive reply | Meeting pending |
| Not now, with a date | Thank them, log the date, ask nothing else | Campaign owner | Set by the owner | Rest until the date, then a new angle |
| Not interested | Acknowledge, ask once whether it is timing or fit, tag the reason (Berman's follow-up guide) | Campaign owner | Set by the owner | Rest 60 days |
| Uses a competitor | Ask what made them choose that vendor; position the offer as a complement (Berman's follow-up guide) | Campaign owner | Set by the owner | Rest 60 days, then a new angle |
| Wrong person or referral | Thank them; add the named person as a new contact after validation, first line names the referrer | Campaign owner or SDR | Set by the owner | New contact in the same cell |
| Unsubscribe or "remove me" | Add to the one suppression list, across every campaign, domain and tool | Whoever reads it first | Same day, never past 2 days (Yahoo) | Permanent suppression |
| Hard bounce | Suppress; pause the cell if bounces pass 2% (Berman) | Sending platform, checked by the deliverability owner daily | Automatic | Permanent suppression |
| Out of office with a return date | Pause until the business day after the return date | Campaign owner or SDR | 1 business day | Paused |
| Closed, sold or joined a group | Suppress and tag; the tag becomes an exclusion filter at the next pull | Campaign owner or SDR | 1 business day | Permanent suppression |

### Other channels

Email is the default channel here. Add a channel only when the data for it exists and someone owns it:

| Channel | Use when | Role | Owner skill |
|-|-|-|-|
| Main-line phone call (section 9) | Local or small businesses with a listed main number | Find the right person and their email; one question | `cold-calling` |
| LinkedIn profile view and connection request without a pitch | B2B titles, and the sender has an active profile | Name recognition before touch 2 | `multi-channel-outreach` |
| Direct mail | An account-based plan with a verified business address | Pattern break for high-value accounts | `multi-channel-outreach` |

Each channel gets copy written for it; pasting the email into a LinkedIn note reads as automation.

## 4. Capacity, goal and runway

Inputs: validated contacts (V), touches per contact (T), warmed inboxes (I), sends per inbox per day (S, 30 per Instantly's recommended limit), 21 sending days a month (Hunter).

- Total sends = V x T
- Daily capacity = I x S
- New contacts started per day = (I x S) / T
- New contacts per month = new contacts per day x 21
- Sending days to start everyone = V / new contacts per day
- Runway in months = V / new contacts per month

### Back-solve the goal (show this in every plan)

Meetings held per month = new contacts per month x (1 - bounce rate) x positive replies per 100 delivered / 100 x booked rate x held rate.

The rates are the user's own floor and target (SKILL.md Prerequisite 9); no published source sets them. Per warmed inbox at 30 a day and 3 touches, 210 new contacts start a month. Meetings per inbox = 210 x (1 - bounce rate) x positive per 100 / 100 x booked rate x held rate.

Inboxes needed for a goal = goal meetings per month / meetings per inbox per month at target, rounded up. A plan shows the target and floor results and says what happens when results sit at the floor (more inboxes, a stronger offer or a longer timeline). When target output is under the goal, the plan names the shortfall and the fix with a date. Replace assumed rates with measured ones at the first read.

### Inbox table at 30 sends per inbox per day, 3 touches

| New contacts per month | Sends per month | Sends per day (21 days) | Inboxes needed | Domains at 2 to 3 inboxes each |
|-|-|-|-|-|
| 630 | 1,890 | 90 | 3 | 1 to 2 |
| 1,000 | 3,000 | 143 | 5 | 2 to 3 |
| 2,500 | 7,500 | 357 | 12 | 4 to 6 |
| 5,000 | 15,000 | 714 | 24 | 8 to 12 |

Round up. Cold mail goes from secondary sending domains, never the company's main domain (Berman's beginner setup warns against sending from the primary domain). With every inbox on one domain, one complaint spike stops all sending; Berman's beginner setup spreads inboxes over 3 to 5 domains, and Hunter keeps fewer than five accounts per domain.

### Ramp

| Stage of a new inbox | Sends per inbox per day | Source |
|-|-|-|
| Warmup, 2 to 4 weeks | 10 to 20 warmup emails, no cold sends | Berman's templates page and beginner setup |
| First cold sends | 15 a day for an inbox new to cold campaigns, then Instantly's Campaign Slow Ramp adding 2 a day, so 30 on the 9th sending day | Hunter (2023, 15 or fewer for new senders); Instantly help center |
| Steady state | 30 | Instantly's recommended limit per account |
| Ceiling | Under 50 | Berman; Hunter calls 50 safe for warmed accounts |

Scaling a winner: raise sends with Slow Ramp (2 more a day) only while bounces stay under 2% (Berman), Gmail spam stays under 0.1% (Google), and a seed test shows inbox placement at Gmail and Outlook. Stop under 50 per inbox. Past that, add inboxes and domains.

Send window: the days and hours the plan sets, scheduled in the recipient's time zone. Send time is a late test, after offer, segment and first line.

### Sequencer settings (Instantly option names)

The plan lists one platform's settings with values. Option names below are from Instantly's help center articles on campaign options, account limits and high bounce auto-pause (checked 2026-10-13); for another platform, use its own names for the same jobs.

| Instantly option | Value in the plan | Why |
|-|-|-|
| Accounts to use | The inboxes for this cell's campaign | One cell per campaign keeps reads clean |
| Schedule & Limits | Days, send window, time zone, daily limit (15 on the first sending day for inboxes new to cold sends, 30 at steady state) | Instantly recommends 30 campaign emails per account per day |
| Campaign Slow Ramp | On until the inbox reaches its limit | Adds 2 campaign emails a day |
| Stop sending emails on reply | On | Stop rule on reply (Berman's follow-up guide) |
| Stop Campaign for Company on Reply | On | Marks every other lead at that company completed |
| Insert Unsubscribe Link Header | On | One-click unsubscribe header (Google and Yahoo sender rules) |
| Open tracking, Link tracking | Off | Opens are unreliable since Apple Mail Privacy Protection; decisions use replies |
| Send first email as text-only | On | Plain first email |
| High bounce auto-pause | On, threshold lowered from the 5% default to 2% | Instantly checks after 200 sends; 2% is Berman's bounce ceiling |
| Auto optimize A/Z testing | Off | The read uses positive replies tagged by hand, one variable at a time |
| Custom fields | Merge tags, sequence count, rest-until date | The rest rule and the counter live in the platform |

### New sending domain: name, inboxes, records

| Item | Rule | Source |
|-|-|-|
| Domain name | The brand with get, try, hq or team; `.com` or the market's country TLD; no hyphens or digits (`getacme.com`, `acmehq.com`) | Instantly and Smartlead secondary-domain articles |
| Inbox addresses | `first@` or `first.last@` of real team members, two different people per domain; no role addresses | Puzzle Inbox, cold email inbox naming conventions (May 18, 2026) |
| MX (Google Workspace) | `smtp.google.com`, priority 1 | Google Workspace, set up MX records |
| SPF | TXT at `@`: `v=spf1 include:_spf.google.com ~all` | Google Workspace, set up SPF |
| DKIM | TXT at `google._domainkey`: the 2048-bit key generated in the Admin console, then Start authentication | Google Workspace, set up DKIM |
| DMARC | TXT at `_dmarc`: `v=DMARC1; p=none; rua=mailto:dmarc@<main domain>`, plus `*._report._dmarc.<main domain>` TXT `v=DMARC1` on the main domain so reports arrive | RFC 7489 section 7.1; Google's recommended DMARC rollout |

Full record sets, Microsoft 365 values and verification commands: the `domain-infrastructure` skill's DNS records checklist.

### Sending stack cost lines

| Line | How the plan prices it | Source |
|-|-|-|
| Sequencer | Instantly Growth $47 a month billed monthly ($37.60 billed yearly): 1,000 uploaded contacts and 5,000 emails a month. Hypergrowth $97 ($77.60 yearly): 25,000 uploaded contacts. Pick the tier from the contacts the plan uploads | Instantly pricing page, checked 2026-10-13 |
| Inbox seats | Seats x the user's seat price | The user's invoice or the provider's pricing page, dated |
| Domains | Domains x the user's registrar price, per month | The user's invoice |
| ScraperCity | Growth $149 a month includes $159 of monthly credits for pay-per-result tools | `references/scrapercity-platform.md` |

Sources: Berman's beginner setup (3 to 5 domains, 2 to 3 inboxes per domain, 2 to 4 weeks warmup, under 50 per inbox per day, never the primary domain); his templates page (10 to 20 a day on new domains over 2 to 4 weeks, bounces under 2%); Hunter's outreach ops guide (15 a day or fewer for new senders, 50 safe for warmed accounts, under five accounts per domain); Instantly's account limits article (30 a day, Slow Ramp); Google's spam rate thresholds.

### Meeting capacity check

Positive replies the team can answer inside the SLA must exceed positive replies at target. If the plan produces more than the team can answer within Berman's 5 minutes in business hours, name a second responder before adding volume.

## 5. Funnel targets (starting hypotheses)

| Stage | Floor | Target | Source and date |
|-|-|-|-|
| Bounce rate | under 2% | under 1% | Berman templates page; Google bulk sender guidance on list hygiene |
| Spam complaint rate (Gmail) | under 0.3% | under 0.1% | Google, 2024 |
| Reply rate, all replies | 3.43% | 4.5% | Instantly 2026 average (3.43%), Hunter 2026 average sequence reply rate (4.5%) |
| Positive replies per 100 delivered | User's floor | User's target | User's own data, or a stated assumption replaced at the first read |
| Positive reply to meeting booked | User's floor | User's target | Same |
| Meeting booked to held | User's floor | User's target | Same |

Opens are reported but never used for a decision. Apple Mail Privacy Protection preloads images and logs opens that did not happen (Postmark, 2021, updated 2022).

## 6. Test order and stop rules

Test in this order, one variable at a time, inside one cell:

| Order | Variable | Why this order |
|-|-|-|
| 1 | Offer (result, mechanism, ask type) | 30% of results per Berman; deliverability (50%) is fixed before any test |
| 2 | Segment (title, size band, trigger) | Same weight as offer; a bad segment hides a good offer |
| 3 | First line (trigger vs observation vs compliment) | Changes relevance |
| 4 | Ask (call vs resource vs referral) | Affects how easy it is to reply |
| 5 | Subject line | Smallest lever once opens are unreliable |

| Rule | Value |
|-|-|
| Minimum per variant | 100 to 200 or more delivered (Berman's templates page) |
| Decision metric | Positive replies per 100 delivered |
| Read date | The day the last contact in the variant finishes the final touch; put it in the plan as a date |
| Call a winner | The two-proportion test below once volume allows; before that, the leader is a direction |
| Kill a cell | Under the break-even positive rate (SKILL.md gate) once its read size is delivered, with bounces under 2% |
| Pause everything | Bounces over 2% on any cell (Berman), a Gmail spam rate at 0.3% (Google), or a sending domain listed on a major blocklist |

### Small volume: directional reads, not significance

The minimums above give a direction, not a statistically significant result. To tell 1.5% positive replies from 3% at 95% confidence and 80% power, a two-proportion test needs about 1,530 delivered per variant. Worked: pooled rate 2.25%; (1.96 x sqrt(2 x 0.0225 x 0.9775) + 0.84 x sqrt(0.015 x 0.985 + 0.03 x 0.97))^2 / 0.015^2 = about 1,530. At 30 new contacts a day (3 inboxes, 3 touches), two variants of 1,530 take about 102 sending days (3,060 / 30).

Until each variant passes the size the test needs, judge by the break-even rate, reply reasons tagged by hand, and one change at a time, and label the read directional. An A/B split inside one live cell still runs at low volume; each variant is read as a direction, and the test is a single variable (usually the ask or the offer).

Berman's Lean B2B interview describes reworking an approach when 20 emails produce fewer than about 4 strongly positive replies in an early market test; use that only as a fast signal for very small, high-value markets.

## 7. Diagnosis tree

| Symptom | Likely cause | Check | Fix |
|-|-|-|-|
| Bounces over 2% | Unvalidated or stale list | Validation status mix | Re-validate; drop catch-all from main cell |
| Sends go out, near zero replies of any kind | Mail in spam, or offer gives no reason | Seed test placement, then offer sentence | Fix placement first; then rewrite the offer |
| Many replies, mostly "not interested" | Wrong segment or title | Reply reasons by cell | Change segment or buyer title |
| "We already have someone" | Market buys; offer not differentiated | Count of vendor objections | Sharpen the mechanism; position as complement |
| Positive replies, few meetings | Slow response or heavy ask | Median reply time | Answer within 5 minutes in business hours (Berman's follow-up guide); offer two times and ask for nothing else |
| Meetings, no deals | Sales process or price | Call notes | Outside this skill |

## 8. Account-based sales development (Lars Nilsson)

Lars Nilsson and his team at Cloudera built Account-Based Sales Development (ABSD). He walked through it at SaaStr Annual 2016 (video and transcript on saastr.com) and later ran global sales development at Snowflake (SaaStr podcast 612). A 2020 SalesSource post he co-wrote with Travis Henry adds persona planning and spreads multichannel outreach over two to four weeks. The unit of work is one target company, not a list of companies.

### When ABSD replaces the default cells

| Condition | ABSD | Default cells (sections 1 to 6) |
|-|-|-|
| Named target accounts | A short named list, each worth an account executive's multi-meeting cycle | A segment of many accounts |
| People involved in the purchase | 3 or more across departments | 1 or 2 |
| Who takes the meeting | An account executive who will run a multi-meeting cycle | The sender or a closer on the first call |
| List source | Account domains, then people by title | Segment filters |

### What Nilsson described, and how to run it now

| Element | Nilsson, SaaStr Annual 2016 | Running it today |
|-|-|-|
| Many personas per account | Pick 5 to 10 titles across departments and levels, from C-level to individual contributors, at one company. Send in batches of 50 to 250 people at that company rather than everyone at once. | Pull people per title with `scrape_website_finder` (one `jobTitle` per request across the account domains) or `query_lead_database` by title. Stagger in batches per company, as Nilsson did; Berman warns that emailing several people at one company at once can get the sender blocked company wide. |
| Short arc | Three emails. Email 1 is a vertical hook (an industry news item or use case). Email 2, about two and a half to three days later, layers in three more use cases from the same industry. Email 3 is a short "Hail Mary" with almost no content, which he said drew strong replies. SDRs then tracked replies for about seven to nine days. | Same three jobs inside the 100 word cap: one use case per line, two or three lines in email 2. The last try is one or two sentences ending in a question. |
| Call the openers | When replies were low, SDRs called the people who opened; they did little with people who did nothing. | Opens are unreliable since Apple Mail Privacy Protection (2021). Call non-repliers at accounts where another persona replied or someone clicked, using `cold-calling`. |
| Use-case library | Subject matter experts wrote 10 to 15 use cases per vertical in a shared doc that grew weekly; SDRs picked the hook from it. | Keep the library table below per vertical. A use case without a named or anonymized customer result stays out of email 1. |
| Net-new vs known contacts | Each campaign ran twice: once to people who had opted in (webinar, trade show, a click) and once to sourced people who had never interacted. Replies were similar; meetings set were much higher from the never-interacted group, and he said he did not know why. | Keep them as separate cells with separate copy. Known CRM contacts get a reference to the past touchpoint; net-new contacts get the vertical hook. Suppress current customers and open deals from both. |

### Use-case library (one per vertical, 10 to 15 rows)

| # | Vertical | Use case in one line | Persona it fits | Proof (client, metric, date) | Owner |
|-|-|-|-|-|-|
| 1 | (vertical) | (what the customer did with the product) | (title) | (measured result) | (subject matter expert) |

### Cloudera figures (point in time, SaaStr Annual 2016, not benchmarks)

| Figure | As stated in 2016 |
|-|-|
| Email baseline before ABSD (marketing automation sends) | 5% to 8% opens, 2% to 3% replies |
| First ABSD sequence | About 70% opens and 30% replies across three emails |
| SDR team | Grew from 6 inherited SDRs to 45, with a plan for up to 65; 65 to 70 inside-sales staff across three centers |
| Target accounts | About 3,000 |

These numbers come from one company in 2016, before Apple Mail Privacy Protection inflated opens and before Google and Yahoo's 2024 bulk sender rules. Use them to explain the method, never as a target for a plan.

### ABSD cost example (40 enterprise accounts, 6 titles)

| Step | Count | Unit price | Cost |
|-|-|-|-|
| `scrape_website_finder`, 40 domains x 6 titles, 60% of requests find one contact (planning assumption) | 144 contacts found | $0.0499 | $7.19 |
| `validate_emails` on every found address | 144 | $0.0072 | $1.04 |
| `find_mobiles` for the call step, 30% found (planning assumption) | 43 numbers | $0.25 | $10.75 |
| Total | | | $18.98 |

Call `check_wallet` first and show the user this table before the pull.

## 9. Phone touch on the main line

For local businesses and small companies whose listing carries a main business number (`phone` from the Local Business Database or Google Maps), in every cell that has the number, not only the trigger cell. Dials a day equal new contacts a day; a roundup on Berman's site describes email opening the door and about two hours of calling a day. One attempt between email touches 2 and 3, a second attempt only if the first reached a gatekeeper who named a better time.

| Touch | Day | Channel | Job | Branch |
|-|-|-|-|-|
| Call | 4 or 5 | Main business line | Confirm the right person and their email; one question if they pick up | Gatekeeper: get the name and email, no pitch. Decision maker: ask the touch 1 question. Voicemail: none on attempt 1. "Not interested": the one suppression list, and stop the emails. "Send info": reply in the email thread inside the positive-reply SLA |

Script (short, to the first question):

1. "Hi, this is [caller] at [company]."
2. "I sent [owner] a short note [day] about [result in one phrase]."
3. "Is [owner] the right person for that, or is it someone else?"
4. If the decision maker: "Quick one: [touch 1 question]?"

Rules: the listed main business line; a "not interested" goes on the same suppression list as email. Full scripts, objections and call logging belong to `cold-calling`.

## 10. Launch calendar

Every plan ends with dated tasks and a named owner per task. Count back from the launch date in business days (T-5 is five business days before touch 1).

| When | Task | Done when |
|-|-|-|
| T-5 | Load suppression lists: customers, open deals, prior unsubscribes, competitors, excluded countries | The sending platform blocks a test address from each list |
| T-4 | Pull, dedupe and validate the first cell; hold catch-all and unknown | Validation counts recorded in the plan |
| T-3 | Hand-write 10 first lines from rows in the list | 10 lines in the prompt file |
| T-2 | Generate an AI dry run and read every line; preview random rows in the platform to check every merge field and fallback | Zero blank or wrong merge fields in the previews |
| T-1 | Enter the sequencer settings; send each touch to seed inboxes at Gmail and Outlook; confirm SPF, DKIM and DMARC pass in the headers and the opt-out works | Every seed arrives in the inbox |
| Day 0 | Launch the first cell | First sends logged |
| Days 1 to 5 | Daily check of bounces, complaints and replies against the pause rules | Logged daily |
| Read date | Read the cell or the test (section 6) | Decision written in the plan |
| 1st of each month | Not-yet-reached tracker and runway update | Date each cell runs dry |

## Sources

- https://alexberman.com
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://thetransactionpod.com/episodes/inverting-your-go-to-market-strategy-thinking-with-jordan-crawford-ep-55/transcript
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://hunter.io/the-state-of-cold-email-2025
- https://hunter.io/the-state-of-cold-email (State of Email Outreach 2026, checked 2026-10-13)
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://hunter.io/cold-email-guide/outreach-ops (Hunter, Set Up Your Outreach Ops for Scale, December 29, 2023)
- https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits (Instantly, account and campaign limits, checked 2026-10-13)
- https://help.instantly.ai/en/articles/6222396-campaign-options (Instantly, campaign options, checked 2026-10-13)
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature (Instantly, high bounce auto-pause: on by default at 5% after 200 sends, threshold adjustable, checked 2026-10-13)
- https://instantly.ai/pricing (Instantly pricing: Growth and Hypergrowth prices and limits, checked 2026-10-13)
- https://alexberman.com/manual-outbound-beats-ai-cold-email (about two hours of calling a day)
- https://help.instantly.ai/en/articles/6502027-scale-your-cold-email-campaigns-with-secondary-sending-domains-the-strategy-how-to-implement-it (secondary domain naming)
- https://helpcenter.smartlead.ai/en/articles/147-all-you-need-to-know-about-secondary-sending-domains-for-cold-email-campaigns (no numbers or hyphens)
- https://puzzleinbox.com/blog/cold-email-inbox-naming-conventions (inbox naming, May 18, 2026)
- https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace
- https://knowledge.workspace.google.com/admin/security/set-up-spf
- https://knowledge.workspace.google.com/admin/security/set-up-dkim
- https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- https://www.saastr.com/lars-nilsson-vp-global-inside-sales-cloudera-targeting-the-big-guys-account-based-sales-development-video-transcript/
- https://www.saastr.com/how-to-manage-100-sdrs-across-4-continents-with-snowflake-vp-global-sales-development-lars-nilsson-pod-612-video/
- https://salessource.com/blog/the-ultimate-absd-tech-stack/
