---
name: cold-email-strategy
description: >-
  Plans a cold email campaign from list to booked meeting: campaign cells (one
  segment, one offer, one trigger), offer design, contact thesis, a touch map with
  branches, a volume and inbox capacity plan, a test plan, and a measurement funnel
  judged on positive replies and meetings. Maps every cell to a ScraperCity list
  source with validation and a cost estimate. Use when the user asks for an outbound
  plan, a cold email campaign, a sequence or cadence design, how many inboxes they
  need, or why replies and meetings are low.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [cold-email, campaign-strategy, sequences, offer-design, outbound, capacity-planning]
  related_skills: [cold-email-copywriting, reply-handling, multi-channel-outreach, email-deliverability, domain-infrastructure, inbox-setup, sending-platforms, signal-triggered-outbound, outbound-unit-economics, icp-list-builder, local-business-list, ecommerce-by-techstack, email-list-cleaner]
  frameworks:
    - "Alex Berman - 30/30/50 targeting, offer and deliverability split"
    - "Alex Berman - offer built from a measured client result"
    - "Alex Berman - segment testing in 100 email batches"
    - "Craig Elias - Trigger Event Selling and the window of dissatisfaction"
    - "Google - Email sender guidelines (2024)"
    - "Yahoo - Sender best practices (2024)"
    - "Microsoft Outlook - high-volume sender requirements (May 2025)"
    - "FTC - CAN-SPAM Act compliance guide"
    - "CRTC - Canada's Anti-Spam Legislation (CASL)"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, cold-email-frameworks.md, alex-berman-cold-email.md, deliverability-primer.md, outbound-compliance-primer.md, list-quality-standard.md]
---

# Cold Email Strategy

## Overview

This skill produces a campaign plan that a copywriter, a list builder and a sending platform can execute without guessing. The plan names each campaign cell (one segment, one offer, one trigger), the contact thesis for that cell, a touch map where every touch has a purpose and a branch, the inbox capacity the volume needs, the test that will run, and the funnel that decides whether the campaign scales. Every cell is tied to a ScraperCity list source with a validated-contact count and a dollar cost.

The mistake it prevents: writing emails first and hoping the list fits. Alex Berman's site splits cold email results into 30% targeting, 30% offer and 50% deliverability. Copy is downstream of all three, so this plan settles them before `cold-email-copywriting` writes a word.

## When to Use

- "Plan an outbound campaign to [segment]", "build me a cold email strategy", "design a sequence".
- "How many inboxes do I need to email 6,000 people a month?"
- "Replies are under 1%, what is wrong?" (run the diagnosis branch in Workflow step 9).
- Splitting one broad list into testable cells, or deciding between a short sequence and a once-per-cycle mailing.
- Before any paid ScraperCity pull meant for cold email, so the pull matches a cell.

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Writing the actual emails, subject lines, merge fields | `cold-email-copywriting` |
| Classifying and answering replies | `reply-handling` |
| Adding calls, LinkedIn and direct mail around email | `multi-channel-outreach` |
| Domains, DNS, SPF, DKIM, DMARC | `domain-infrastructure` |
| Mailbox setup and warmup | `inbox-setup` |
| Bounce and spam diagnosis | `email-deliverability` |
| Cost per meeting and payback | `outbound-unit-economics` |
| Building the list itself | `icp-list-builder`, `local-business-list`, `ecommerce-by-techstack` |

## Prerequisites

Collect these, or mark each one `unknown` in the plan and carry it as a risk:

1. What is sold, the price or average deal value, and one measured client result (number, timeframe, client type).
2. Who buys: industry or business category, size band, geography, buyer title.
3. Exclusions: current customers, open opportunities, competitors, prior unsubscribes, countries you will not email.
4. Sending setup: number of warmed inboxes, domains, platform (Instantly, Smartlead, Lemlist, EmailBison, ManyReach), current bounce and complaint rates.
5. ScraperCity plan (Starter, Growth or Scale) and wallet balance. The two databases need Growth or higher.
6. Meeting capacity: how many first calls the team can take per week.

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, alexberman.com (30/30/50) | Fix targeting, offer and deliverability before copy. The plan has a section for each. |
| Alex Berman, "Cold Email Doesn't Fail, Your Offer Does" | An offer is one sentence with a niche, a measured result and a mechanism. The list is built after the offer. |
| Alex Berman, Lean B2B interview | Test a segment with about 100 emails; score segments by reply enthusiasm, ease of closing, ability to pay and problem severity; check market size first (his first market of about 3,300 companies ran out in about two months). |
| Alex Berman, follow-up guide and TAM breakdown | 4 to 6 follow-ups over 2 to 3 weeks for small markets, or one touch per 30 to 60 day cycle for very large ones. |
| Craig Elias, Trigger Event Selling | A dated trigger explains "why now"; the first vendor to reach a buyer in the window of dissatisfaction wins most often. |
| Google, Yahoo and Microsoft sender rules | SPF, DKIM and DMARC with alignment for bulk senders; Gmail spam rate under 0.1%, never 0.3%; one-click unsubscribe for marketing mail. |
| FTC CAN-SPAM guide | Truthful headers and subjects, a postal address, an opt-out honored within 10 business days, and no B2B exemption. |
| CRTC CASL guidance | Canadian recipients need consent; a published business address gives implied consent only for role-relevant messages. |
| Hunter, State of Cold Email 2025; Instantly 2026 benchmarks | Average replies of 3.4% to 4.1%; smaller, targeted campaigns reply higher; about 58% of replies come from the first email. Starting hypotheses only. |

Full digests: `references/alex-berman-cold-email.md` and `references/cold-email-frameworks.md`. Routing between them: `references/framework-notes.md`.

## Workflow

### 1. Write the offer sentence

Fill: "We help [niche] get [result with a number] in [timeframe] by [mechanism]." Use a real client result. If any bracket is vague, stop and work the offer with `references/offer-and-cell-design.md` before planning volume. Record the proof source (client, date, metric).

### 2. Split the market into campaign cells

A cell is one segment x one offer x one trigger (or "no trigger, fit only"). Split whenever the buyer title, the business type, the size band, the trigger or the offer changes. Two to four cells per campaign is the working range; more cells means smaller samples per cell.

For each cell record: segment filters, exclusions, offer, trigger with its freshness window, proof line, buyer title, and the list source (step 4).

### 3. State the contact thesis per cell

One sentence: "[Buyer] at [segment] will reply because [trigger or observable fact] makes [problem] costly now, and [proof] shows we fix it." Add what would prove the thesis wrong (for example "fewer than 2 positive replies per 100 delivered after 300 sends").

### 4. Map each cell to a ScraperCity source and size it

Use the source table in ScraperCity Implementation. Run a free count first (a database call with `limit: 1` returns `pagination.total`), then estimate the validated yield and the cost. Show the user the count and the cost and get a go-ahead before any pull over about $5. If a cell has fewer than 300 reachable contacts, merge it with a neighbor or accept that it will only support one test.

### 5. Build the touch map with branches

Default for markets under 50,000 contacts: 4 email touches over about 14 days, each with a distinct job.

| Touch | Day | Job | Branch on reply |
|-|-|-|-|
| 1 | 0 | Trigger or observation, proof, one question | Stop sequence, route to `reply-handling` |
| 2 | 3 | Same thread, new proof point or case study | Stop, route |
| 3 | 7 | Different angle or problem question | Stop, route |
| 4 | 12 to 14 | Breakup: close the file or point to the right person | Stop; referral goes to referral capture |

Every touch also branches on bounce (suppress, check list source), unsubscribe (suppress across every campaign), out of office (pause until return date) and wrong person (referral capture). For markets over 50,000 contacts with deal values under $5,000, use one touch per 30 to 60 day cycle with fresh copy instead (decision table in `references/campaign-architecture-playbook.md`).

### 6. Plan volume and inbox capacity

Compute, and show the arithmetic in the plan:

- Total sends = validated contacts x touches per contact.
- Daily capacity = warmed inboxes x sends per inbox per day.
- Days to complete = total sends / daily capacity.
- New contacts started per day = daily capacity / touches.

Planning default: 30 sends per warmed inbox per day, 2 to 3 inboxes per domain. Berman's beginner setup keeps inboxes under 50 a day with 3 to 5 domains and 2 to 4 weeks of warmup; another page on his site suggests about 15 per inbox. Start at the low end on new domains and raise only while bounces stay under 2% and spam complaints under 0.1%. Hand domain and inbox counts to `domain-infrastructure` and `inbox-setup`.

### 7. Write the test plan

One variable per test, inside one cell. Minimum 100 delivered per variant, 200 when the expected positive reply rate is under 2%. Decision metric: positive replies per 100 delivered. Guardrails: bounce rate, spam complaint rate, unsubscribe rate. Stop rules and test order (offer, then segment, then first line, then subject) are in `references/campaign-architecture-playbook.md`.

### 8. Define the measurement funnel

Stages: sourced, validated, sent, delivered, replied, positive replies, meetings booked, meetings held, opportunities. Opens are a diagnostic only: Apple Mail Privacy Protection preloads tracking pixels and logs opens that never happened, and open tracking adds a tracking domain to every email. Set a target and a floor for each stage from the dated benchmarks, then replace them with your own numbers after the first 500 delivered.

### 9. Diagnose an underperforming campaign

Run in order, and stop at the first failure:

1. Bounce rate over 2% or spam complaints over 0.1%: deliverability. Re-validate, pause, route to `email-deliverability`.
2. Delivered fine, almost no replies of any kind: offer or segment. Rebuild the offer sentence and re-score the cell.
3. Replies mostly "not interested": targeting. Change the segment or the buyer title.
4. Positive replies without meetings: reply speed or the ask. Check the SLA in `reply-handling`.
5. Meetings without deals: sales process, outside this skill.

### 10. Hand off

Send each cell to `cold-email-copywriting` with: offer sentence, thesis, trigger field names, proof line, touch map and the merge fields available from the list source. Send the routing table to `reply-handling`. Confirm the platform setup with `sending-platforms`.

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
| Every address before sending | `validate_emails` | `emails` | $0.0072 per email |

### Count first, then pull

```text
check_wallet
query_local_business_database  category=["Dentist"] state="TX" city="Houston" minReviews=20 hasEmail=true limit=1
  -> read pagination.total for the cell size, no charge for a count
query_local_business_database  same filters, limit=100, excludeDelivered=true, after="0"
  -> page with pagination.next_after until null
validate_emails  emails=[...every address in the cell...]
```

CLI equivalents: `npx scrapercity db-local`, `npx scrapercity db-leads`, `npx scrapercity store-leads`, `npx scrapercity email-validate`. REST: `POST /api/v1/database/local-businesses`, `POST /api/v1/scrape/email-validator`.

### Worked cost estimate (three cells, Texas dental review software)

| Line | Count | Unit price | Cost |
|-|-|-|-|
| Growth plan (Local Business Database, Lead Database) | 1 month | $149.00 | $149.00 |
| Local Business Database, cells A and B, `hasEmail: true` | 2,680 businesses | included | $0.00 |
| Lead Database, cell C (DSO operations leaders), `hasEmail: true` | 420 contacts | included | $0.00 |
| `find_emails` for named dentists whose listing shows only info@, 900 lookups, 55% found (planning assumption) | 495 found | $0.05 | $24.75 |
| `validate_emails` on every address (3,100 + 495) | 3,595 emails | $0.0072 | $25.88 |
| Total cash (usage $50.63 drawn from the $159 plan credits) | | | $149.00 |

Growth includes $159 in monthly credits per `references/scrapercity-platform.md`, so the $50.63 of enrichment and validation is covered by credits. Present this table, then wait for approval before the paid steps.

### Validation gate

Send only `valid` results. Hold `catch-all` and `unknown` addresses in a separate low-volume cell capped at 10% of daily sends, and drop them if that cell's bounce rate passes 2%. Full rules: `references/list-quality-standard.md`.

## Output Format

The user receives one Markdown plan built from `templates/output-template.md`, with these `##` sections in order: Campaign Summary, Offer, Campaign Cells, Contact Thesis, List Sources and Cost, Touch Map, Volume and Capacity, Test Plan, Measurement Funnel, Compliance and Suppression, Handoff. Tables, not prose, for cells, sources, touches, capacity and the funnel. Every number in the capacity section shows its inputs.

## Quality Check

Run `python3 scripts/check-output.py plan.md`. It checks headings, placeholders, length and table rows, plus these skill rules:

- Every campaign cell row has a segment, an offer and a trigger (or "fit only").
- Every touch row has a branch.
- The cost section contains a dollar total.
- The measurement funnel names positive replies and meetings, and the test plan never uses opens as its decision metric.

Also confirm by reading:

- The offer sentence has a number, a niche and a timeframe from a real client.
- Each cell has at least 300 validated contacts, or the plan says it supports one test only.
- Daily sends stay inside inbox capacity, and the ramp starts low on new domains.
- Every touch includes an opt-out and the sender's postal address (CAN-SPAM).
- Canadian contacts are excluded or have a documented CASL basis.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| One campaign for "SaaS companies" | Mixed buyers need different offers; results average out and teach nothing | Split by title, size and trigger into cells |
| Offer is a service list | Nothing in it gives a stranger a reason to reply | Rewrite as niche + measured result + mechanism |
| Sizing by gut | A 1,200 contact cell supports one or two tests, then runs dry | Count with `limit: 1` before planning volume |
| Skipping validation on database pulls | Bounces over 2% damage domain reputation for every cell | `validate_emails` on everything, $7.20 per 1,000 |
| Judging tests on opens | Apple MPP inflates opens; tracking pixels add a spam signal | Decide on positive replies per 100 delivered |
| Five follow-ups to a 300,000 contact market | Burns the audience and raises unsubscribes after touch 3 | One touch per 30 to 60 day cycle, fresh copy |
| Emailing three people at one company the same day | Can get the sender blocked company wide | CEO first, next level down after 1 to 2 weeks |
| Scaling a winner straight to 5x | New volume on new inboxes trips spam filters | Raise sends per inbox in steps while guardrails hold |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Choosing which authority or reference file to open for a decision |
| `references/campaign-architecture-playbook.md` | Building cells, picking sequence vs cycle mailing, capacity tables, test order and stop rules |
| `references/offer-and-cell-design.md` | Writing the offer sentence, the contact thesis, and ScraperCity filter recipes per segment type |
| `templates/output-template.md` | Starting the plan; copy it and fill every field |
| `examples/worked-example.md` | Seeing a complete plan for Texas dental practices with real prices |
| `scripts/check-output.py` | Validating a finished plan before handing it off |
| `references/cold-email-frameworks.md` | Picking the email framework per cell (shared) |
| `references/alex-berman-cold-email.md` | Checking exactly what Alex Berman teaches and where (shared) |
| `references/scrapercity-catalog.md` | Tool ids, parameters and per-result prices (shared) |
| `references/scrapercity-platform.md` | Plans, database allowances, integrations (shared) |
| `references/deliverability-primer.md` | Sender requirements and warmup (shared) |
| `references/outbound-compliance-primer.md` | CAN-SPAM, CASL, PECR and GDPR detail (shared) |
| `references/list-quality-standard.md` | Validation statuses and catch-all handling (shared) |

## Related Skills

- `cold-email-copywriting` writes the emails for each cell.
- `reply-handling` takes over every reply the touch map routes.
- `multi-channel-outreach` adds phone, LinkedIn and mail around the email touches.
- `domain-infrastructure`, `inbox-setup` and `email-deliverability` deliver the capacity this plan assumes.
- `sending-platforms` loads the cells into Instantly, Smartlead, Lemlist, EmailBison or ManyReach.
- `signal-triggered-outbound` supplies trigger-based cells.
- `outbound-unit-economics` turns the funnel into cost per meeting.
- `icp-list-builder`, `local-business-list`, `ecommerce-by-techstack` and `email-list-cleaner` build and clean the lists.
