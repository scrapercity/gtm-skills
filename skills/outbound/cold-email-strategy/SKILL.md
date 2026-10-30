---
name: cold-email-strategy
description: >-
  Plans a cold email campaign from list to booked meeting: campaign cells (one
  segment, one offer, one trigger), a concrete offer, a touch map with every
  email and reply written out, exact sequencer settings with a ramp, inbox
  capacity back-solved from the meeting goal, all-in cost per meeting, a dated
  test plan, owners and a 90-day launch calendar. Maps every cell to a
  ScraperCity list source with validation and a cost estimate. Use when the user asks for an outbound plan, a cold email
  campaign, a sequence or cadence design, how many inboxes they need, or why
  replies and meetings are low.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.3.0"
  author: ScraperCity
  category: outbound
  tags:
    - cold-email
    - campaign-strategy
    - sequences
    - offer-design
    - outbound
    - capacity-planning
  related_skills:
    - cold-email-copywriting
    - reply-handling
    - multi-channel-outreach
    - cold-calling
    - email-deliverability
    - domain-infrastructure
    - inbox-setup
    - sending-platforms
    - signal-triggered-outbound
    - outbound-unit-economics
    - icp-list-builder
    - local-business-list
    - ecommerce-by-techstack
    - email-list-cleaner
  frameworks:
    - "Alex Berman - 30/30/50 targeting, offer and deliverability split"
    - "Alex Berman - offer built from a measured client result"
    - "Alex Berman - segment testing in 100 email batches"
    - "April Dunford - positioning starts from the competitive alternative"
    - "Jordan Crawford - Pain-Qualified Segments built from past buyers"
    - "Craig Elias - Trigger Event Selling and the window of dissatisfaction"
    - "Lars Nilsson - Account-Based Sales Development (SaaStr Annual 2016)"
    - "Hunter - State of Email Outreach 2026"
    - "Hunter - Set Up Your Outreach Ops for Scale (2023)"
    - "Instantly - account and campaign limits (30 campaign emails per account per day)"
    - "Instantly - campaign options and high bounce auto-pause"
    - "Google - Email sender guidelines (2024)"
    - "Yahoo - Sender best practices (2024)"
    - "Microsoft Outlook - high-volume sender requirements (May 2025)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - cold-email-frameworks.md
    - alex-berman-cold-email.md
    - deliverability-primer.md
    - list-quality-standard.md
---

# Cold Email Strategy

## Overview

This skill produces a campaign plan a small team can launch on a named date with nothing else to write: each campaign cell (one segment, one offer, one trigger), the offer and the alternative it beats, the contact thesis, a touch map with every email, call opener and reply written out, the sequencer's exact settings with a ramp, the inbox capacity the meeting goal needs, how long the list lasts, the all-in cost per meeting, the dated tests, and who does what by when inside the first 90 days. Every cell is tied to a ScraperCity list source with a validated-contact count and a dollar cost.

The mistakes it prevents: writing emails first and hoping the list fits, promising a meeting goal the inboxes cannot reach, and handing the user a plan that still needs copy, settings or another planning step before it can send. Alex Berman's site splits cold email results into 30% targeting, 30% offer and 50% deliverability. This plan settles those three first, then writes the copy against them.

## When to Use

- "Plan an outbound campaign to [segment]", "build me a cold email strategy", "design a sequence".
- "How many inboxes do I need to book 8 meetings a month?" or "to email 6,000 people a month?"
- "Replies are under 1%, what is wrong?" (the diagnosis branch, step 10).
- Splitting one broad list into testable cells, or choosing a short sequence vs once-per-cycle mailing.
- Before any paid ScraperCity pull meant for cold email, so the pull matches a cell.
- "Can we email these people again?" (the rest rule, step 11).

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Rewriting or critiquing existing emails, persona variants beyond one plan | `cold-email-copywriting` |
| Classifying and answering replies in depth | `reply-handling` |
| Calls, LinkedIn and direct mail around email | `multi-channel-outreach`, `cold-calling` |
| Domains, DNS, mailboxes, warmup | `domain-infrastructure`, `inbox-setup` |
| Bounce and spam diagnosis | `email-deliverability` |
| Full cost per meeting and payback model | `outbound-unit-economics` |
| Building the list itself | `icp-list-builder`, `local-business-list`, `ecommerce-by-techstack` |

## Prerequisites

Collect these, or mark each one unknown in the plan's Assumptions section and carry it as a risk:

1. What is sold, the price or first-year deal value, whether the price is one flat figure, and one measured client result (number, timeframe, client type).
2. What the buyer does about the problem today (the current alternative), and how won customers described the problem.
3. Who buys: industry or business category, size band, geography, buyer title. Recent won deals, if any.
4. Exclusions: current customers, open opportunities, competitors, prior unsubscribes, countries you will not email.
5. Sending setup: warmed inboxes, how many domains they sit on, how long each has warmed and whether it has sent cold campaigns, the sequencer and data source already paid for, current bounce and complaint rates, and what each seat, domain and plan costs. With no platform named, the plan picks one (Instantly, whose limits, option names and plan prices are sourced below), adds one line for a team already on another tool, and dates the confirmation in the calendar.
6. The goal: meetings booked or held per month, and from what date.
7. Meeting capacity: first-call slots per week, and the names behind each role (owner, backup, caller). With no names, the plan assigns each role to a job title the user has and lists the name mapping as one open question.
8. Close rate from a held meeting, and the most the user will pay to win a customer (CAC ceiling).
9. Funnel rates from the user's past campaigns, as a floor and a target: positive replies per 100 delivered, positive reply to meeting booked, booked to held. With no history, the user states the rates the plan uses; the plan lists them as assumptions and replaces them with measured rates at the first read.
10. ScraperCity plan (Starter, Growth or Scale) and wallet balance. The databases need Growth or higher.
11. Dated deadlines in the buyer's year (a filing date, a renewal, a year-end close), if the user knows any: one touch can name the nearest one, and a "not now" reply gets a re-contact task on that date.

Run this gate before planning cells. It compares the break-even rate with the user's own rates, so it has no fixed cutoff.

| Gate | Check | Go | Test only | No-go |
|-|-|-|-|-|
| Unit economics | Break-even positive replies per 100 delivered = 100 x monthly campaign cost / (delivered per month x booked rate x held rate x win rate x CAC ceiling), at the floor booked and held rates | At or under the floor positive rate | Between the floor and target positive rates: one cell, no extra cash on data until it reads | Above the target rate: raise the deal value, narrow to a higher-value cell, or pick another channel |

Several buyers across departments at each target account: plan account-based sales development (playbook section 8) instead of segment cells.

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, alexberman.com (30/30/50) | Fix targeting, offer and deliverability before copy. |
| Alex Berman, "Cold Email Doesn't Fail, Your Offer Does" | An offer is one sentence with a niche, a measured result and a mechanism; the list is built after the offer. |
| Alex Berman, Lean B2B interview | Test a segment with about 100 emails; "we already have a vendor" proves the market buys; check market size first (his first market of about 3,300 companies ran dry in about two months). |
| Alex Berman, follow-up guide and TAM breakdown | Follow-ups 3 to 5 days apart, each adding something new; one touch per 30 to 60 day cycle for very large markets; 2 to 3 inboxes per domain, under 50 sends per inbox a day, never the primary domain. This skill fixes the rest at 60 days for every pattern. |
| April Dunford (podcast episode 82, 2019) | Positioning starts from what the buyer would use instead of you. The offer worksheet starts there. |
| Jordan Crawford, The Transaction episode 55 (2025) | Build segments from the situation past buyers were in; the list is the message. |
| Craig Elias, Trigger Event Selling | A dated trigger explains "why now"; the first vendor in the window of dissatisfaction wins most often. |
| Lars Nilsson, SaaStr Annual 2016 (Cloudera ABSD) | For high-value accounts: 5 to 10 personas per company, a three email arc, a library of 10 to 15 use cases per vertical, calls to engaged non-repliers. |
| Hunter, State of Email Outreach 2026; Instantly 2026 benchmarks | Three messages roughly doubled replies against one (6.8% vs 3.3%); average sequence reply 4.5% (Hunter) and 3.43% (Instantly); about 58% of replies come from email 1. Starting hypotheses only. |
| Hunter, Set Up Your Outreach Ops for Scale (December 29, 2023) | 50 a day is safe for warmed accounts; new senders start at 15 or fewer; fewer than five accounts per domain; 21 sending days a month. |
| Instantly help center, account and campaign limits (checked 2026-10-13) | 30 campaign emails per account per day; Campaign Slow Ramp adds 2 a day until the account reaches its limit. |
| Instantly help center, campaign options and high bounce auto-pause (checked 2026-10-13) | Option names the plan sets (Schedule & Limits, Stop sending emails on reply, Stop Campaign for Company on Reply, Insert Unsubscribe Link Header, Send first email as text-only); bounce auto-pause is on by default at 5% after 200 sends and its threshold can be changed. |
| Alex Berman, templates page, follow-up guide, B2B lead generation page, Single Grain video | Bodies under 75 words (templates page) and never over 100 (B2B lead generation page); end on one easy question (Single Grain); subjects under 50 characters, bounces under 2%, new domains starting at 10 to 20 a day (templates page); interested replies answered within 5 minutes, no pricing sent by email, a competitor user asked what made them choose it (follow-up guide). |
| Instantly pricing page (checked 2026-10-13) | Growth $47 a month billed monthly (1,000 uploaded contacts, 5,000 emails a month); Hypergrowth $97 (25,000 uploaded contacts). The plan picks the tier from its contact count. |
| Google, Yahoo and Microsoft sender rules | SPF, DKIM and DMARC with alignment; Gmail spam rate under 0.1%, never 0.3%; one-click unsubscribe; Yahoo honors unsubscribes within 2 days. |

Full digests: `references/alex-berman-cold-email.md` and `references/cold-email-frameworks.md`. Routing between them: `references/framework-notes.md`.

## Workflow

### 1. Write the offer

Fill: "We help [niche] get [result with a number] in [timeframe] by [mechanism]." Use a measured client result and record its source (client, date, metric). Then add three lines from `references/offer-and-cell-design.md` section 1: the current alternative the mechanism beats, the pain in won customers' words, and the objection the offer answers (for example "too busy to set up" answered by "we do the setup in one call"). If any bracket is vague, stop and work the offer before planning volume. Score it 0 to 6 and fix each missing point before launch. With no measured result in the niche yet, the ask becomes a free scoped review that returns a few written findings (Berman describes free work as the way to build a first case study; `references/offer-and-cell-design.md` section 1), and the plan asks the user for the first result by a date.

### 2. Split the market into campaign cells

Start from recent won deals: the first cell is the situation that repeats most often. A cell is one segment x one offer x one trigger (or "fit only"). Split whenever the buyer title, business type, size band, trigger or offer changes. A cell with a dated trigger (a posting, a new listing) launches on the first launch date, sharing the inboxes with the fit-only cell, because the trigger goes stale while it waits in a queue. Exclude accounts that buy centrally (groups sharing one domain, franchise or parent-owned locations). Look for a dated trigger before settling for fit only: when the offer takes over work a person does (bookkeeping, scheduling, prospecting), a job posting for that role is a dated trigger (Elias's window of dissatisfaction) and gets its own cell, collected from job boards with the posting URL and date per row (step 5). Record per cell: filters, exclusions, offer, trigger with its freshness window, proof line, buyer title, personalization depth (segment, account or person, set by deal value) and the list source (step 4).

**Small capacity: launch fewer cells.** A cell teaches nothing until its read size is delivered (step 8). Sending days to a read = read size / new contacts per day per cell. Launch only the cells that reach their read by the read date and queue the rest with a launch date. Three inboxes give 90 sends a day; at 3 touches that starts 30 new contacts a day, so one cell reaches 200 delivered in about 7 sending days, while three cells in parallel take three times as long. A queued cell launches when the first cell has its read or when new inboxes finish warmup.

**Scope: the first 90 days.** The plan details at most 3 cells, all launching inside a 90-day calendar. Cells for later (the next state, the next size band) get one "Next cells" line with the date the owner picks them; the user asked for this campaign, not next year's.

### 3. State the contact thesis per cell

One sentence: "[Buyer] at [segment] will reply because [trigger or observable fact] makes [problem] costly now, and [proof] shows we fix it." Add the list field that carries the fact and how fresh it must be. What proves the thesis wrong is the cell read row in the Test Plan; it is not repeated here.

### 4. Map each cell to a ScraperCity source and size it

Use the source table in ScraperCity Implementation. Run a free count first (a database call with `limit: 1` returns `pagination.total`), then estimate the validated yield and the cost. Show the user the count and the cost and get a go-ahead before any paid pull. Pull only the cells that launch first; count the queued ones. A cell too small to reach its read size merges with a neighbor or supports one test only. The plan names the product and its filters in plain words (Local Business Database: Dentist, Texas, 50 to 400 reviews, has email) and dates the prices once ("ScraperCity price list, checked [date]", from `references/scrapercity-platform.md`). It never prints tool calls; counts that were not run are listed once under Assumptions and the count becomes a calendar row.

### 5. Build the touch map and the reply routing table

Default: 3 email touches on business days 0, 3 and 6, each with a distinct job (open, proof, angle or resource with an easy out). Hunter's 2026 data found three messages the best balance; a fourth touch costs new contacts while any are waiting, so add a breakup touch only when no validated contacts are left to start. Every touch branches on reply (stop touches for everyone at that company), bounce, unsubscribe, out of office and wrong person. When one email per person per 60-day cycle would fill the daily sends (validated contacts at or above daily capacity x 42 sending days), use one touch per 60-day cycle instead; for a short list of high-value accounts with several buyers each, use the account-based arc (playbook sections 2 and 8). Pick each cell's first line from `references/offer-and-cell-design.md` section 6. A first line states a fact from the row and stops: a trigger ("Saw {{practice_name}} is hiring an office manager"), a field ("{{rating}} stars from {{review_count}} reviews") or, for a fit-only row, the problem in won customers' words. It never infers a problem from a fit field: "{{review_count}} reviews says you are busy, so your books run behind" is a guess and gets cut.

The plan carries a reply routing table: event, the reply text in quotes, named owner, SLA and the state after (playbook section 3). Positive replies get an answer within 5 minutes in business hours (Berman's follow-up guide), from the person who takes first calls, with reply alerts on that person's and the backup's phones; unsubscribes are suppressed across every campaign and tool the same day. Add rows for out of office (paused to the return date) and for closed, sold or joined a group (suppressed, and the tag becomes a list filter).

**Job postings as a trigger** (not a ScraperCity source): store the posting URL and date; inside the freshness window the plan sets and still live when re-opened before touch 1, or the contact gets the fit-only line (`references/offer-and-cell-design.md` section 7).

**Phone touch on the main line.** For local and small businesses with a listed main number, every cell gets one call between touches 2 and 3 to confirm the right person and their email, sized as dials a day = new contacts a day (Berman's site describes email opening the door and about two hours of calling a day). Leave a cell out only when its rows carry no number, and say so. A "not interested" on the phone also stops the emails and goes on the one suppression list. Script and branches: playbook section 9; dialer setup: `cold-calling`.

### 6. Write every message the plan mentions

The plan is the copy. Write in full, in an Email Copy section: every email touch per cell (subject line, then the body as quoted lines), the opt-out line once, each test variant (in full, or as the one changed line when only one line changes), the call opener, and the reply text for every routing row a person answers. A touch shared by several cells is written once and labelled with its cells. Copy rules, from `references/alex-berman-cold-email.md` sections 3 and 4:

- Body under 75 words, never over 100; plain text, at most one link, no price.
- The first line follows step 5; the second line is the proof (client type, number, timeframe); the email ends on one easy question.
- Subject under 50 characters, no pitch; follow-ups stay in the same thread.
- Merge tags only for fields the list carries; the 10 hand-written lines (step 12) are the examples any AI-written first lines follow.

Write the signature block out. Reply texts follow Berman's follow-up guide: two times or a booking link for a positive reply, asking for nothing else (documents, reports and access come after the call is booked); two or three sentences, one result and a proposed time for info or price. Berman's guide keeps pricing out of email; when the user's price is one flat figure, the price reply states it, since "it depends" would be untrue. Every link merge tag ({{booking_link}}) names its tool and gets a calendar row that sets it up; one question ("timing or fit?") for not interested; "what made you choose them?" for a competitor, positioning the offer as a complement.

### 7. Back-solve capacity from the goal, then set the ramp and the sequencer

Show every line with its inputs (playbook section 4):

- Daily capacity = warmed inboxes x sends per inbox per day (plan at Instantly's 30).
- Ramp: inboxes that have not sent cold campaigns start at 15 a day (Hunter's figure for new senders) and climb 2 a day with Instantly's Campaign Slow Ramp, reaching 30 on the 9th sending day. Read dates and runway count from the ramp, not from full volume.
- New contacts per day = daily capacity / touches; per month = x 21 sending days (Hunter's month).
- Meetings held per month = new contacts per month x (1 - bounce rate) x positive replies per 100 delivered / 100 x booked rate x held rate, at the target and floor rates from Prerequisite 9.
- Compare with the goal on the user's current inboxes first, then with each option that adds capacity (a second domain, its monthly cost). The Answer row leads with what today's setup delivers. When output falls short, name the shortfall and the fix with a date: more inboxes on a second domain (2 to 4 weeks of warmup first), a stronger offer, or a later goal date.
- Runway: validated contacts / new contacts per day, as the date each cell runs dry, and the date to pick the next cells.
- All-in monthly cost (ScraperCity plan plus the user's sending stack) and cost per meeting held at target and at floor, stated once in Campaign Summary.

One warmed inbox at 30 a day and 3 touches starts 210 new contacts a month; multiply by the rates for meetings per inbox. Cold mail goes from secondary domains, never the main company domain: Berman's beginner setup uses 3 to 5 sending domains with 2 to 3 inboxes each, and Hunter's outreach ops guide keeps fewer than five per domain. New domains and inboxes are calendar rows in this plan (register, authenticate, warm 2 to 4 weeks), not a separate step, and the plan gives the domain name (the brand with get, try or hq, `.com`, no hyphens or digits), the inbox addresses (first@ or first.last@ of real team members) and the record values (playbook section 4).

Cost lines are itemized: ScraperCity plan (Growth is $149 a month and includes $159 of monthly credits for pay-per-result tools), each pay-per-result tool, the sequencer tier chosen by uploaded contacts and monthly sends, inbox seats x the user's seat price, and domains x the user's registrar price. A price comes from a dated pricing page or the user's invoice.

Sequencer settings: one platform, one table, with the platform's own option names (Instantly's are in playbook section 4): accounts per campaign, schedule window and daily limit, the ramp, stop on reply, company-level stop on reply, unsubscribe header, open and link tracking off, first email as text only, bounce auto-pause lowered to the plan's 2% pause line, the test split, custom fields for merge tags, sequence count and rest-until date, and the no-send dates. Each option name links to its help-center page under Sources, and the ramp row carries a by-hand fallback (raise the daily limit by hand 2 a day) in case a label differs in the account.

### 8. Write the test plan

One variable per test, inside one cell, with a read date. 100 to 200 or more delivered per variant (Berman's templates page). Decision metric: positive replies per 100 delivered. Test order (offer, segment, first line, ask, subject) and stop rules: playbook section 6.

These samples give a direction, not significance: telling 1.5% from 3% at 95% confidence and 80% power takes about 1,530 delivered per variant, about 102 sending days at 30 new contacts a day. When volume is below that, say so in the plan and judge by the break-even rate (a cell under it once its read size is delivered stops), reply reasons tagged by hand, and one change at a time.

### 9. Write one funnel table

The goal back-solve and the measurement funnel are the same table, written once in Volume and Funnel: contacts started, delivered, all replies, positive replies, meetings booked, meetings held, customers won, each with a floor rate, a target rate and the monthly count at each, then a Goal row and a Result row ("Goal met" or "Shortfall of N"). Cite the all-reply band once under it (Instantly 2026, Hunter 2026). Opens are a diagnostic only: Apple Mail Privacy Protection preloads tracking pixels and logs opens that never happened. Replace assumed rates with measured ones at the first read.

### 10. Diagnose an underperforming campaign

Run in order and stop at the first failure:

1. Bounces over 2% or spam complaints over 0.1%: deliverability. Re-validate and pause; `email-deliverability` covers the full diagnosis.
2. Delivered fine, almost no replies of any kind: offer or segment. Rebuild the offer and re-score the cell.
3. Replies mostly "not interested": targeting. Change the segment or the buyer title.
4. Positive replies without meetings: reply speed or the ask. Check the routing SLA.
5. Meetings without deals: sales process, outside this skill.

### 11. Run list hygiene between campaigns

One rest rule everywhere in the plan, the touch map and the sequencer:

- **Rest 60 days.** A contact who finishes a sequence without replying rests 60 days before any new touch. Cycle mailing uses the same 60 days between cycle emails.
- **New angle only.** Re-enrollment needs a new offer, trigger or proof line.

Hygiene jobs: a not-yet-reached tracker on the 1st of each month (validated contacts not yet sent touch 1 per cell, and the date each runs dry); dedupe local businesses on website domain and normalized phone as well as email; dedupe B2B on email, then company domain for stop-on-reply; a per-contact sequence counter and rest-until date; re-validate before every send cycle, as Berman's TAM breakdown does (`references/list-quality-standard.md`).

### 12. Name owners and write the launch calendar

| Role | Duty |
|-|-|
| Campaign owner | Runs the plan, reads the weekly funnel, restarts a paused send |
| Backup | Covers the owner's absence with the same rights |
| May pause sending | Named people who pause any campaign without asking when bounces pass 2% (Berman) or Gmail spam reaches 0.1% (Google). Only the owner or backup restarts |

Owners are people the user named, or job titles the user has with the name mapping as one open question; never a blank Name column.

Personalization: the person who knows the buyer best hand-writes the first 10 personalized lines from rows in the list (Nowoslawski writes about 10 examples, per alexberman.com); those become the AI prompt examples, and the same person reviews a dry run of AI-written lines before the cell sends.

Launch calendar, covering the first 90 days: a dated row with one owner for each task in playbook section 10: suppression lists loaded, first cell pulled and validated, 10 lines written, the AI dry run and merge-field previews checked, sequencer settings entered, seed test at Gmail and Outlook, launch at the ramp's first-day limit, daily checks in week 1, each read date, the monthly tracker, the queued cell launch dates and the date the owner picks the next cells.

### 13. Record assumptions once

List every number that is a planning assumption or the user's own figure (funnel rates, find rates, stack cost, close rate) and the date measured data replaces it, plus open questions with an owner. This list is the only place assumptions are named: tables carry no "(assumed)" tags, and the intro carries at most one "Not checked:" line for anything not run. The plan ends here, with no handoff to other steps: everything the team needs to send is already in it.

## ScraperCity Implementation

Prices come from `references/scrapercity-catalog.md`; plan facts from `references/scrapercity-platform.md`. Call `check_wallet` before any paid run.

### Cell to source map

| Cell type | Source tool | Key parameters | Cost |
|-|-|-|-|
| B2B title at company size, revenue or industry | `query_lead_database` | `title`, `seniority`, `industry`, `minEmployees`, `maxEmployees`, `revenueMin`, `revenueMax`, `country`, `hasEmail: true`, `excludeDelivered: true` | Included on Growth ($149/mo) and Scale, 100,000 new leads a day |
| Same, from a saved Apollo.io search | `scrape_apollo` | `url` (Filters 1.0), `count` 500 to 50,000 | $0.0039 per lead; runs take hours to days, use a webhook |
| Local business by category and city | `query_local_business_database` | `keyword` or `category`, `location` or `city` and `state`, `minRating`, `maxRating`, `minReviews`, `maxReviews`, `hasEmail`, `hasContact` | Included on Growth and Scale, 100,000 new businesses a day |
| Local business, fresh from Maps | `scrape_maps` | `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch` | $0.0099 per business |
| Ecommerce store by platform, app or traffic | `scrape_store_leads` | `platform`, `apps`, `technologies`, `category`, `countryCode`, `minEstimatedMonthlyVisits`, `emails: true`, `totalLeads`, `offset` | $0.0039 per lead |
| Companies using a technology | `scrape_builtwith` then `scrape_website_finder` | `technology`; then `domains`, `jobTitle`, `autoValidateEmails: true` | $4.99 per technology, then $0.0499 per contact found |
| Named person, no email | `find_emails` | `contacts: [{first_name, last_name, domain}]` | $0.05 per email found, free if not found |
| Every address before sending | `validate_emails` | `emails` | $0.00169 per email |

### Count first, then pull

```text
check_wallet
query_local_business_database  category=["Dentist"] state="TX" minRating=4.5 minReviews=20 maxReviews=80 hasEmail=true limit=1
  -> read pagination.total for the cell size, no charge for a count
query_local_business_database  same filters, limit=100, excludeDelivered=true, after="0"
  -> page with pagination.next_after until null
validate_emails  emails=[...every address in the launch cell...]
```

These calls are for you to run. The plan reports their results in plain words (product, filters, count, cost) and never prints the calls; a count you could not run becomes one Assumptions line and a calendar row.

CLI equivalents: `npx scrapercity db-local`, `npx scrapercity db-leads`, `npx scrapercity store-leads`, `npx scrapercity email-validate`. REST: `POST /api/v1/database/local-businesses`, `POST /api/v1/scrape/email-validator`.

### Worked cost estimate (Texas dental review software, one cell first)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Growth plan (Local Business Database, Lead Database) | 1 month | $149.00 | $149.00 |
| Local Business Database: cell A pulled, cell B counted | 1,560 pulled | included | $0.00 |
| Email Finder for cell A dentists whose listing shows only a generic inbox, 520 lookups, 55% found (planning assumption) | 286 found | $0.05 | $14.30 |
| Email Validator on cell A (1,560 + 286) | 1,846 | $0.00169 | $3.12 |
| Total cash (usage $17.42 drawn from the $159 plan credits) | | | $149.00 |

Cell B adds $12.70 of finder and validation usage when it is pulled (380 lookups, 209 found, 1,329 validated), still inside the monthly credits. Present this table, then wait for approval before the paid steps.

### Validation gate

Send only `valid` results. Hold `catch-all` and `unknown` addresses in a separate low-volume campaign, and drop them if its bounce rate passes 2% (Berman). Full rules: `references/list-quality-standard.md`.

## Output Format

The user receives one Markdown plan built from `templates/output-template.md`. Under the title: one line with the date, the owner, the one sending platform, the launch date and, only if something was not run, one "Not checked:" sentence. Then these `##` sections in order: Campaign Summary, Offer, Campaign Cells, Contact Thesis, List Sources and Cost, Touch Map, Email Copy, Sequencer Settings, Volume and Funnel, Test Plan, List and Sender Rules, Owners and Controls, Launch Calendar, Assumptions and Open Questions, Sources.

- **Answer first, in one sentence.** Campaign Summary opens with an Answer row of 45 words or fewer: what the user's current inboxes deliver against the goal, and the option (with its monthly cost) that closes any gap. Then the `Unit economics go/no-go` row (Go, Test or No-go and the break-even figure, 35 words or fewer; the formula sits under the funnel), launch and read dates, and the all-in cost with cost per meeting held. The offer score stays internal.
- **Sendable today.** Email Copy holds the signature block (`Signature:`), every email touch in full (a `Subject:` line, then the body as `>` lines), the opt-out line once, every test variant, and the call opener. The routing table's Action column holds the reply text in quotes. Sequencer Settings lists one platform's options with values, ramp included. Nothing is handed to another step.
- **Each fact once.** One funnel table in Volume and Funnel carries the goal back-solve (floor and target rates, monthly counts on the current inboxes and with each capacity option, Goal and Result rows); cost per meeting appears only in Campaign Summary; a cell's falsifier is its Test Plan read row; assumptions appear only in their list, with no "(assumed)" tags in tables.
- **Inside the request.** At most 3 cells, all launching inside a 90-day Launch Calendar; later cells get one "Next cells" line.
- **Sources stay short.** A benchmark, limit or threshold carries its source once, in parentheses, by publisher and page title (Instantly help center, account and campaign limits; Hunter, Set Up Your Outreach Ops for Scale, 2023; alexberman.com templates page). Plain settings (stop on reply, one suppression list) go without a source. Drop the Source column, trainer and framework names, and any outside limit looser than the plan's own setting. Prices carry one dated line. A closing Sources section lists each outside source once with its URL, so every number and option name can be checked.
- **The reader gets the plan only.** ScraperCity product names (Local Business Database, Email Finder, Email Validator), never tool ids or code blocks; no internal file paths, skill names, reference section numbers, framework lists, self-grading checklists or handoff tables.
- Every test and every launch task has a date (YYYY-MM-DD) and an owner. Every rest or re-enrollment period uses the same number of days.

## Quality Check

Run `python3 scripts/check-output.py plan.md`. It checks headings (no duplicates), placeholders, length and table rows, plus these skill rules:

- No legal content, code blocks, tool ids, skill ids, trainer or framework names, Handoff or Quality Check sections, offer score row or looser outside limit ("allows 2 days"); at most one "Not checked" line, at the top; at most 2 "(assumed)" tags.
- The Answer row is one sentence of 45 words or fewer; the go/no-go row is 35 words or fewer.
- A cell with a dated trigger launches on the first launch date; the call touch covers every cell.
- The positive reply asks for a time only and its SLA is in minutes; Email Copy writes out the signature; a link merge tag has a calendar row that sets it up.
- Sequencer Settings has a line for a team on another sequencer and a by-hand ramp fallback; the cost table itemizes seats instead of a "sending stack" lump; a registered domain comes with its v=spf1 and v=DMARC1 values; Sources lists URLs.
- The offer sentence carries a number; at most 3 cells, each with a segment, an offer and a trigger (or "fit only").
- Every touch row has a branch; every routing row has an owner and an SLA, and rows a person answers carry the reply text in quotes.
- Email Copy has at least one email per email touch, each with a body under 100 words ending on a question, and states the opt-out line.
- Sequencer Settings has 6 or more rows covering the daily limit, the ramp, stop on reply, the unsubscribe header and the bounce auto-pause.
- The cost section has a dollar total and a dated price line; no test decides on opens; every test has a read date.
- The go/no-go row starts with Go, Test or No-go and carries the break-even number.
- Volume and Funnel has capacity inputs, a Ramp row, a 'Cells launched at once' row, and one funnel table with positive replies, meetings held, a Goal row and "goal met" or a shortfall.
- One rest period across the plan; List and Sender Rules covers the tracker, the new angle rule, unsubscribe, the suppression list and authentication, with no Source column.
- Owners and Controls names owner, backup and pausers, the 10 hand-written lines and the AI review.
- Every Launch Calendar row has a date and an owner, and the calendar spans at most 92 days; Assumptions and Open Questions is not empty.

Also confirm by reading:

- Every number in the plan is sourced, the user's own figure, or listed as a planning assumption.
- The goal arithmetic, ramp, read dates, runway dates and funnel counts agree with each other.
- Each launched cell can reach its read size, or the plan says it supports one test only.
- Every first line states a fact from the row; none infers a problem from a fit field.
- New inboxes warm 2 to 4 weeks before cold sends, cold mail never uses the main domain, and inboxes spread across several sending domains.
- Every email carries the opt-out line and the one-click unsubscribe header, and unsubscribes are processed across every tool the same day.
- A job posting trigger carries its URL and date.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| A goal with no capacity check | Three inboxes at 30 a day start 630 contacts a month, whatever the goal says | Back-solve inboxes from the goal; name the shortfall and its dated fix |
| One campaign for "SaaS companies" | Mixed buyers need different offers; results average out and teach nothing | Split by title, size and trigger into cells |
| Offer is a service list | A stranger gets no reason to reply | Niche + measured result + mechanism, against the current alternative |
| Sizing by gut | A 1,200 contact cell runs dry in two months at 30 new contacts a day | Count with `limit: 1`; put the run-dry date in the plan |
| Skipping validation on database pulls | Bounces over Berman's 2% ceiling damage domain reputation for every cell | Validate everything, $1.69 per 1,000 |
| Judging tests on opens | Apple MPP inflates opens; tracking pixels add a spam signal | Decide on positive replies per 100 delivered |
| A fourth and fifth touch while contacts wait | Each extra touch costs new contacts at fixed capacity | 3 touches; a breakup only when no new contacts are waiting |
| Five follow-ups to a 300,000 contact market | Burns the audience; unsubscribes rise after touch 3 | One touch per 60-day cycle, fresh copy |
| All inboxes on one domain, or the main domain | One complaint spike stops all sending, or hurts the company's own mail | Secondary domains only, 3 to 5 of them with 2 to 3 inboxes each (Berman) |
| Emailing three people at one company the same day | Can get the sender blocked company wide | CEO first, next level down after 1 to 2 weeks |
| Scaling a winner straight to 5x | New volume on new inboxes trips spam filters | Instantly's Slow Ramp, 2 more a day up to 30 per inbox, while bounces and spam stay under the pause lines |
| Three cells on three inboxes | Each cell takes three times as long to reach its read | Launch only the cells that reach their read size by the read date |
| Calling a winner from 200 per variant | Two or three replies of chance pick the winner | Label it directional; decide on floors and reply reasons |
| A plan with no dates or owners | Tasks slip and reads never happen | Launch calendar with a date and an owner per row |
| No enterprise exit ramp | A deal with several buyers closes through an account executive's multi-meeting cycle | Use email to open the account (ABSD), then hand to the account executive's plan |
| 60 days in the touch map and 90 in hygiene | The sequencer gets two answers | One rest rule, copied everywhere |
| A first line that infers a problem from a fit field ("200 reviews says your books run behind") | The reader sees a mail-merge guess and the claim is often wrong | State the fact and stop; use a dated trigger (a job posting for the role the offer replaces) or the problem in won customers' words |
| Full daily volume on day 1 from inboxes new to cold sends | Every cell rides on one or two domains; an early reputation hit stops all sending | Start at 15 per inbox and climb 2 a day to 30; count read dates from the ramp |
| Copy, replies or settings left to "the next step" | The team cannot send on the launch date | Write every email, variant, reply and setting into the plan |
| "Instantly recommended; Smartlead, Lemlist or others also work" | The operator still has to choose and translate settings | One platform, its option names, its values |
| The trigger cell queued behind the fit-only cell | A posting or new listing goes stale while it waits | Launch it on day one, sharing the inboxes |
| Positive reply that asks for documents before the call, or a 2-hour SLA | Each extra step and hour loses bookings | Ask for a time only; answer within 5 minutes in business hours |
| "Sending stack $110" as one line | The user cannot check it or see which part to cut | Sequencer tier, seats x price, domains x price, each dated |
| A calendar and cells running a year out | Weight the user did not ask for; later cells change after the first reads anyway | 90-day calendar, at most 3 cells, one "Next cells" line |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference file to open for a decision |
| `references/campaign-architecture-playbook.md` | Cells from won deals, touch count and cycle mailing, reply routing, capacity and goal back-solve, test rules, account-based sales development (section 8), the phone touch (section 9) and the launch calendar (section 10) |
| `references/offer-and-cell-design.md` | The offer worksheet with alternative and objection rows, the contact thesis, ScraperCity filter recipes, trigger first lines (section 6) and job postings (section 7) |
| `templates/output-template.md` | Starting the plan; copy it and fill every field |
| `examples/worked-example.md` | A complete plan for Texas dental practices on 3 inboxes growing to 6: full copy, reply texts, Instantly settings, the ramp and current prices |
| `scripts/check-output.py` | Validating a finished plan before handing it off |
| `references/cold-email-frameworks.md` | Picking the email framework per cell (shared) |
| `references/alex-berman-cold-email.md` | Checking exactly what Alex Berman teaches and where (shared) |
| `references/scrapercity-catalog.md` | Tool ids, parameters and per-result prices (shared) |
| `references/scrapercity-platform.md` | Plans, database allowances, integrations (shared) |
| `references/deliverability-primer.md` | Sender requirements and warmup (shared) |
| `references/list-quality-standard.md` | Validation statuses and catch-all handling (shared) |

## Related Skills

- `cold-email-copywriting` rewrites, critiques or extends the copy beyond what one plan needs.
- `reply-handling` takes over every reply the routing table sends it.
- `multi-channel-outreach` and `cold-calling` add phone, LinkedIn and mail around the email touches.
- `domain-infrastructure`, `inbox-setup` and `email-deliverability` deliver the capacity this plan assumes.
- `sending-platforms` loads the cells into Instantly, Smartlead, Lemlist, EmailBison or ManyReach.
- `signal-triggered-outbound` supplies trigger-based cells.
- `outbound-unit-economics` turns the funnel into a full payback model.
- `icp-list-builder`, `local-business-list`, `ecommerce-by-techstack` and `email-list-cleaner` build and clean the lists.
