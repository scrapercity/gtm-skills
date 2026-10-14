---
name: cold-email-copywriting
description: >-
  Writes cold email sequences that get positive replies: bodies under 100 words
  with one ask, that say who is writing and name the segment (city, building
  class, category, platform), carry the strongest proof in email 1 and a
  concrete offer worth replying for, answer the buyer's first objection
  head-on, and give every follow-up a new reason to reply. Adds persona variants
  and signal variants gated on a verified list field, a subject line plus an A/B
  alternative for every email, and merge fields from ScraperCity data (Google
  rating, review count, category, city, store platform, installed apps,
  technology, title, company size, revenue) with fallbacks. Use when the user asks
  to write, rewrite or critique a cold email, a follow-up, a subject line, a first
  line, persona variants or a full sequence for a campaign cell.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.1.0"
  author: ScraperCity
  category: outbound
  tags:
    - cold-email
    - copywriting
    - subject-lines
    - personalization
    - follow-ups
    - merge-fields
    - objections
    - persona-variants
  related_skills:
    - cold-email-strategy
    - reply-handling
    - multi-channel-outreach
    - email-deliverability
    - sending-platforms
    - signal-triggered-outbound
    - local-business-list
    - ecommerce-by-techstack
    - icp-list-builder
  frameworks:
    - "Alex Berman - 3C framework (Compliment, Case Study, Call to Action)"
    - "Alex Berman - subject line types and the question-mark close"
    - "Alex Berman - follow-ups that each add something new"
    - "Josh Braun - neutral, problem-first questions (via 11x summary)"
    - "Craig Elias - Trigger Event Selling"
    - "Leslie Venetz - 1-10-100 rule and Earn the Right (2026)"
    - "Jason Bay - reason, problem, proof, ask (Gong blog, 2025)"
    - "Eric Nowoslawski - offers that answer why someone would not reply (GTM Engineer, 2025)"
    - "Eric Nowoslawski - Creative Ideas campaign (via alexberman.com, 2026)"
    - "Jordan Crawford - Permissionless Value Proposition (2025)"
    - "Eugene Schwartz - Breakthrough Advertising awareness levels (1966)"
    - "Hunter - cold email word count analysis (2024)"
    - "Google - Email sender guidelines (2024)"
    - "Yahoo - Sender best practices (2024)"
  shared_references:
    - scrapercity-catalog.md
    - scrapercity-platform.md
    - cold-email-frameworks.md
    - alex-berman-cold-email.md
    - deliverability-primer.md
---

# Cold Email Copywriting

## Overview

This skill writes the emails for one campaign cell: a first touch, two or three follow-ups and a breakup, each with its own subject line and one A/B alternative, a plain text body under 100 words and one ask, the only question mark in the email. Touch 1 opens with a statement (the proof, or a moment in the reader's week), says who is writing and names every segment marker the user gave, and carries the strongest proof the user has. The sequence puts a concrete offer on the table that the reader keeps either way, answers the buyer's first objection in its own touch, and gives every follow-up a new reason to reply. Persona and signal variants of touch 1 go to the rows their gate selects.

The mistakes it prevents: two questions competing in touch 1, a follow-up that restates touch 1 from another side, a result stretched into a promise the brief never made, and "personalization" that changes nothing. Every personalized line comes from a field in the list and connects to the offer.

## When to Use

- "Write a cold email to [segment]", "write the sequence for this campaign", "rewrite this email".
- "Give me subject lines", "write first lines from this CSV", "write follow-ups", "write a version for directors".
- "Why am I getting no replies to this email?" (audit mode).
- After `cold-email-strategy` hands over an offer sentence, cell cards and a touch map.

| Nearby job | Skill |
|-|-|
| Choosing segments, offers, cadence, inbox count | `cold-email-strategy` |
| Answering replies | `reply-handling` |
| Call scripts, LinkedIn notes, postcards | `multi-channel-outreach` |
| Spam placement, bounces, authentication | `email-deliverability` |
| Loading copy and variables into a platform | `sending-platforms` |
| Finding and dating trigger events | `signal-triggered-outbound` |

## Prerequisites

1. Offer sentence with a measured result (from `cold-email-strategy` or the user). With no measured result, lead with the reply offer and a question, never an invented result.
2. The cell: segment, buyer titles, trigger and the ScraperCity source.
3. A sample of rows from the list, to see which fields are filled and how often.
4. Sender first name, full name, company and the opt-out wording the platform will append. Unknown: use `{{sender_first_name}}`, `{{sender_name}}` and `{{sender_company}}`, never "[Sender name]".
5. The sending platform, because merge and fallback syntax differ (Instantly uses `{{firstName | there}}`).

Ask for anything missing in one message. If the user cannot answer, write with what you have and list the gap once in Confirm Before Launch.

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, alexberman.com and Lean B2B interview | 3C: a specific compliment, a relevant case study with its result, a simple call to action. |
| Alex Berman, templates page | Under 75 words, opener of one or two sentences, "you" over "we", at most one link, no pricing or PDFs, subject under 50 characters with no emojis or all caps. |
| Alex Berman, Single Grain video | End the ask with a question mark; start from something the reader already believes; never pitch in the subject line. |
| Alex Berman, Entrepreneur (2017) | Four subject line types; a news subject must be matched by the first line. |
| Alex Berman, follow-up guide | Follow-ups stay in thread, add something new each time, and end in a breakup that offers to close the file. |
| Josh Braun (11x summary) | Neutral curiosity questions and low-pressure closes; under 80 words. |
| Craig Elias, Trigger Event Selling | A dated trigger in the first line answers "why now"; never invent one. |
| Leslie Venetz, 1-10-100 post (September 2026) | One low-effort ask; the first ten words (subject plus preview) lead with relevance; under 100 words; openings built on "I", "we" and "our" read as seller-first. |
| Jason Bay, Gong blog (July 2025, 28M+ emails) | Reason, problem in the buyer's words, peer proof, one ask; 100 words or fewer; pitching cut replies by up to 57%. |
| Eric Nowoslawski, GTM Engineer podcast notes (July 2025) | Build offers strong enough that prospects would pay for the call; every offer answers why someone would not reply; remove risk. His reputation campaign quoted each business's own negative reviews and reported 1 positive reply per 70 emails (self-reported). |
| Eric Nowoslawski, via alexberman.com (March 2026) | Creative Ideas: ideas tied to real capabilities, an off-limits list, hand-written examples before any AI output. |
| Jordan Crawford, The Transaction ep. 55 (May 2025) | A PVP is useful on its own; the bar is a message people would pay to receive; AI rewords data and invents nothing. |
| lemlist help center (March 2026) | One campaign per ICP, written in that prospect's own language. |
| Eugene Schwartz, Breakthrough Advertising (1966) | The opener depends on what the reader already knows. |
| Hunter, word count analysis (April 2024, 34M emails) | 20 to 39 word emails had the highest average reply rate (4.5%); differences between bands were small. |
| Google and Yahoo sender rules | One-click unsubscribe at bulk volume, unsubscribes processed within 2 days, complaints under 0.1% and never 0.3%. |

Digests: `references/alex-berman-cold-email.md`, `references/cold-email-frameworks.md`. Routing: `references/framework-notes.md`.

## Workflow

### 1. Profile the fields

From the row sample, list each field you might use, its fill rate and two example values, in the worksheet's Fill Rates table (the worksheet is your working file, `<sequence>-worksheet.md`; the client never sees it). Keep a field that is often empty out of the first line, or give it a fallback that reads naturally (`references/personalization-and-merge-fields.md`).

### 2. Speak their language and name their slice

List the words this segment uses about its own work, the words they'd say to a colleague, in the "Their words" row (lemlist: write in the prospect's own language). Use them across the sequence. Pull them from the brief, the list's category and title fields and the user's notes; ask the user when unsure. Starter lists by segment: `references/line-library.md` section 15.

Then list the segment markers: every term the user used for the slice (city, building class, category, platform, size band). Touch 1 and every variant name all of them in the body; dropping "Class B" from "Class B office buildings in Denver" loses the user's own targeting. "Class B buildings in Denver" tells a property manager the email was written for them; "properties like yours" tells them nothing. A marker must be true for every row: gate on the list field, or use a merge tag with a fallback. Say it about the slice you serve or the proof ("we clean Class B office buildings in Denver"), never as a label on the reader's own property: "your Class B building" reads as a rank.

Write the rest in plain operator voice: contractions, short sentences, no marketing adjectives. A timely touch ("before the holiday orders start") is welcome when it's true for the send date.

### 3. Pick the relevance angle

Place the cell on Schwartz's awareness scale from list evidence (`references/cold-email-frameworks.md` section 15). No evidence means unaware: lead with a fact or the problem, never the product. Set proof and ask by seniority (`references/line-library.md` section 12).

Choose one fact per email that connects to the offer. Delete test: if you remove the personalized line and the offer still makes the same sense to this reader, the line was decoration. Fact-to-angle table: `references/line-library.md` sections 1 to 4.

### 4. Set the reply offer and the objection

Reply offer: one concrete thing the reader gets for replying and keeps whether or not they buy. Nowoslawski's bar: good enough that they would pay for it. It passes when it is specific to the segment (a walkthrough of one building after the night crew leaves, with a written punch list), takes the reader little time, carries no catch, and the user confirms a delivery date. The row says when they get it ("punch list within N business days of the walkthrough", N from the user). If the brief has no offer or no delivery time, write a specific one in the row starting "Proposed:" and list it once under Confirm Before Launch. Never send an offer the user has not confirmed. Every ask in the sequence and in the Test Plan offers only what this row or the facts list: "want to hear what changed?" needs a brief that says what changed.

Likely objection: the first reason this buyer won't reply, in their words ("tenants always complain", "we already have a cleaning company", "Recharge already has skip"). Nowoslawski: the offer has to answer why someone would not respond. Write it in the "Likely objection" row with the fact from the brief that answers it. If the brief has no answering fact, ask for one. Objections by persona: `references/line-library.md` section 13.

### 5. Write touch 1

Short lines, in this order, with one question mark per email (Venetz: one low-effort ask; a second question leaves the reader unsure which to answer):

1. Greeting with a `{{first_name | there}}` style fallback.
2. A statement opener: the proof, the list fact when the angle is a trigger, or a moment in the reader's week stated as a condition ("If the first you hear about a missed restroom is a tenant email, the night crew has already had a full shift to fix it."). Never a claim about the segment the brief does not make ("Most Class B managers...").
3. Who is writing and what they do, naming every segment marker ("We do nightly janitorial for Class B office buildings in Denver."), then the strongest proof: result, comparable client, timeframe. A reader who stops after touch 1 never sees touch 2.
4. One ask ending in "?": the reply offer, or a one-line question ask ("Want the email we used?").
5. Sign-off: the sender's first name, or `{{sender_first_name}}`. Every touch and variant ends this way; the footer adds the full name and company.

Hook test. A question ask about the reader's week (in a follow-up, or as touch 1's ask when there is no reply offer) passes all three:

| Test | Fails when |
|-|-|
| Answers vary by reader | Every reader gives the same answer, so the email has told them nothing ("Who hears about a dirty lobby first: you or your cleaning company?" Everyone says "me.") |
| A reader who needs the offer gives the gap answer | The honest answer of a good-fit reader does not point at the problem the proof fixes |
| No answer embarrasses | One option reads as failure; offer two normal-sounding answers, one of them the gap |

| Avoid | Use |
|-|-|
| Is tenant satisfaction something you track? (survey) | Where do most of your cleaning complaints come from right now: restrooms, trash, or the common areas? |
| Who hears about a complaint first: you or your vendor? (obvious) | After a move-out, how many days before the unit's ready to show? |
| Do you have a review process? (yes/no) | When a patient leaves happy, who asks for the review: the front desk, the dentist, or whoever remembers? |

More by segment: `references/line-library.md` section 15. Body under 100 words (Jason Bay, Gong blog, 2025); aim under 75 (Berman's templates page). Hunter's 2024 data found 20 to 39 word emails replied best, by a small margin. Plain text, no images, HTML styling, tracking pixel or links in touch 1.

### 6. Write the subject lines

Every touch gets `Subject:` and `Subject B:`. A few words (the Lean B2B interview says three to four), lowercase or sentence case, under 50 characters (Berman), no pitch, emoji or fake "Re:" or "Fwd:", matching the first line. Pick from `references/subject-line-library.md`. `Subject:` is the default: it carries no merge tag whose fill rate is assumed or low on the sample (a "your building" fallback in most inboxes says nothing). Test the tagged version as `Subject B:`. Each touch also gets a `Thread:` line. Berman's follow-up guide keeps the first three or four touches in one thread: touch 1 new; touches 2 to 4 reply to touch 1 and keep "Re:" plus touch 1's A and B subjects. A touch that opens a new thread gets its own subjects. "Re:" appears only on a touch that replies in an existing thread.

### 7. Write the follow-ups

Every touch gets a row in the worksheet's Touch Map (Type, Adds) naming the new reason to reply: a new fact, the objection answered, the reply offer, a route to the right person. If you cannot fill it with something touch 1 did not say, cut the touch. Days follow Berman's follow-up guide (3 to 5 days apart; his example schedule starts day 0, 3, 7, 11), or the strategy plan's cadence. The Sequence opens with one sending line: weekdays, business hours in the recipient's time zone (Mountain for Denver), under 50 sends per inbox per day (Berman's beginner setup, alexberman.com TAM breakdown) unless the strategy plan sets the cap, the send days and the threading:

| Touch | Day | Type | Adds |
|-|-|-|-|
| 2 | 3 | Objection pre-handle | Names the likely objection in the reader's words, answers it with a fact from the brief, adds a second result |
| 3 | 7 | Value ask | The reply offer, if touch 1 used a question ask; otherwise a different problem with its own fact |
| 4 | 11 | Breakup with referral ask | Who owns this, an easy close of the file, and touch 1's proof in one line if touch 3 did not restate it |

Berman's follow-up guide lists a case study with numbers as one thing a follow-up can add: restate touch 1's proof in one line in touch 3 or the breakup, so a reader who skimmed touch 1 still sees the number. A reframe (cost instead of time, tenant instead of owner) counts only when it brings a fact the reader has not seen. Other types and lines: `references/line-library.md` section 14. Mark a no-ask touch with Type "value-add (no ask)" in the Touch Map: no question mark, never touch 1, one per sequence at most. Never "just checking in" or "bumping this". After the breakup, this cell stops mailing the contact; any re-mail belongs to the strategy plan.

### 8. Write the variants

Variants replace touch 1 for the rows their gate selects; follow-ups stay shared.

- Persona variant: whenever the cell holds more than one buyer type (portfolio director vs site property manager, founder vs head of ecommerce, owner vs office manager). Same proof, different stake: a portfolio director answers for consistency across buildings and owner reporting; a site manager answers for tomorrow's walkthrough and today's tenant emails. Gate on the title field.
- Signal variant: only when a list field on the contact's own row verifies the signal (an installed app, a technology, a listing date, a rating inside the cell's low band) and measures the problem the offer fixes. A rating fits a reviews offer; for a cleaning offer, an office building's Google reviews are about parking, leasing and tenants, and quoting a low score to its manager reads as a jab. A field from a second pull needs its match step (which column joins it to the contact) in Confirm Before Launch, or the variant goes. Name the field in backticks in `Gate:` and say what the other rows get. With no such field, write one persona variant and no signal variant. Gates by field: `references/personalization-and-merge-fields.md` section 9.

### 9. Use only facts from the brief

Every claim in a body (number, client, result, how the client got it) appears in the worksheet's "Facts from the brief" row or comes from a list field. Three ways an inference creeps in, all banned:

| Inference | Example | Fix |
|-|-|-|
| Added color | "same tenants", "the only thing that changed" | Cut it, or ask the user |
| Result projected onto the reader | Client's cleaning tickets fell 60%, written as "half as many cleaning emails in your inbox" | State the client's result as the client's |
| Word ratios | "half", "twice", "a third" not in the brief | Use the brief's own numbers |

### 10. Add the footer once

Two lines: sender full name and company, and an opt-out line ("Not the right fit? Reply 'no' and I won't follow up."). Nothing else in the deliverable's footer. As platform settings (not printed): one-click unsubscribe header at bulk volume (Google, Yahoo), and every unsubscribe on one suppression list the same day, across every tool. The footer does not count toward the 100 words.

### 11. Spintax and AI-written lines

Spin only the greeting or sign-off, never the proof or the ask; preview renders before launch (Instantly: `{{RANDOM | option1 | option2}}`). For a line that needs more than a merge tag, hand-write about 10 rows (Nowoslawski's count, via alexberman.com), build the prompt from them plus capability and off-limits lists, generate a dry run, read every line, then run the cell. The model only restates values in the row. Details: `references/personalization-and-merge-fields.md` sections 5 and 8.

### 12. QA and render check

Render sample rows including one with every optional field empty (one line in the worksheet), read each email on a phone screen, run the hook test on every question ask, then run the checker on the sequence; it reads the worksheet beside it.

## ScraperCity Implementation

The copy uses fields ScraperCity returns. Pull or confirm them before writing.

| Source | Tool | Fields used in copy | Price |
|-|-|-|-|
| Local Business Database | `query_local_business_database` | `title` (business name), `category_name`, `city`, `state`, `total_score`, `reviews_count`, `website`, `contact_first_name`, `contact_job_title` | Included on Growth ($149/mo) and Scale |
| Google Maps | `scrape_maps` | Business name, category, rating, review count, reviews, city | $0.0099 per business |
| Lead Database | `query_lead_database` | First name, `title`, `company_size`, `employees_count`, `company_industry`, `company_annual_revenue`, `company_city`, `keywords` | Included on Growth and Scale |
| Store Leads | `scrape_store_leads` | Store platform, installed apps (Shopify), technologies, category, estimated monthly visits, city | $0.0039 per lead |
| Tech Stack Search | `scrape_builtwith` | The technology searched (every domain in the result uses it) | $4.99 per technology |
| Email Finder | `find_emails` | A named person's email when the listing has only info@ | $0.05 per email found |
| Email Validator | `validate_emails` | Pre-send gate only | $0.0072 per email |

Draft samples:

```text
query_local_business_database  category=["Property management company"] city="Denver" state="CO" hasContact=true limit=20
query_lead_database  title="VP Sales" minEmployees=50 maxEmployees=200 country=["United States"] hasEmail=true limit=20
scrape_store_leads  platform="shopify" apps="Recharge" countryCode="US" emails=true totalLeads=20 offset=0   ($0.08)
```

### Worked cost estimate (copy research for one cell)

| Step | Count | Unit price | Cost |
|-|-|-|-|
| Store Leads sample for drafting (Shopify, Recharge, US) | 20 | $0.0039 | $0.08 |
| Store Leads full cell | 1,500 | $0.0039 | $5.85 |
| Email Finder for stores with no named contact, 600 lookups, 50% found (assumed for this example) | 300 found | $0.05 | $15.00 |
| Email Validator on all addresses | 1,500 | $0.0072 | $10.80 |
| Total | | | $31.73 |

Show the user this table and get approval before the full pull. Call `check_wallet` first.

### Field rules

- Ratings to one decimal: "4.9 stars", never "4.9/5.0 rating". Review counts as numbers; below the cell's `minReviews` filter, skip the count.
- Revenue as a band only when the field is filled; never a guessed figure.
- Leave home addresses, mobile numbers and personal social profiles out of the copy.

## Output Format

Two files. The sequence (from `templates/output-template.md`) is what the client reads; the worksheet (`templates/output-template-worksheet.md`, saved as `<sequence>-worksheet.md`) holds Campaign Inputs, Fill Rates and the Touch Map for the checker and stays with you.

The sequence, answer first: title, one line (date, platform), then these `##` sections in order: Copy Audit (audit mode only), Sequence, Variants, Footer, Merge Fields and Fallbacks, Test Plan, Confirm Before Launch.

- Sequence: one sending line (step 7), then each touch as a `### Touch N` block with `Thread:`, `Subject:`, `Subject B:`, `Send day:` and the body in a fenced `text` block (merge tags, not filled values) ending with the ask and the sign-off. No Type, Adds, framework or word-count lines.
- Variants: each `### Variant N: name` block has `Kind:` (persona or signal), `For:`, `Gate:`, `Subject:` and a fenced body.
- Footer: the two footer lines in a fenced block.
- Merge Fields: one line naming the tag notation (the user's platform, or `{{tag | fallback}}` with "set each fallback in your tool"), then Tag, List column, Fallback. Fill rates and the empty-row render stay in the worksheet.
- Test Plan: one row per test in run order (split, at least 100 delivered per arm, from Berman's 100 to 200+ per variation on his templates page, metric), then a `Decide:` line: act when one arm's positive replies beat the other's by at least 2 x the square root of both counts added together (a two-proportion check at about 95% confidence, from the arms' own counts); otherwise keep sending. Every alternative ask offers only what the brief backs.
- Confirm Before Launch: each open question once (the proposed offer and its delivery time, a missing fact, a match step, sender details), or "Nothing open." Nothing here repeats the header.

Worksheet rows: Mode, Offer sentence, Segment and buyer, Segment markers, Their words, Facts from the brief, Reply offer (with when they get it), Likely objection, Timing, List source (filters in plain words; a database named only if the user named it).

Mode `write` leaves out Copy Audit. Mode `audit` (the user pasted an email) requires `### Original` (fenced, with its subject), a line-level table (Line, Issue, Rule broken, Fix) with at least 3 rows, a count line for words and pronouns, and `### Rewrite`, which becomes touch 1. `examples/worked-example.md` and `examples/worked-example-worksheet.md` show one.

Economy: the client reads emails and the decisions they must confirm, nothing else. Leave out the brief echoed back, QA columns, framework and author names (state a cadence or rule as a choice, or link the page), line-by-line rationales, list-building tool plans, tool ids, cost tables (unless asked), sender-rule tables, and this skill's file paths. No bracketed blanks in copy or footer: a merge tag, or a Confirm Before Launch item.

## Quality Check

`python3 scripts/check-output.py sequence.md` (reads `sequence-worksheet.md` beside it) enforces:

- Every body under 100 words with exactly one question mark, the ask, followed by a sign-off line; no link in touch 1 or any variant, one at most elsewhere.
- Every number and word ratio ("half", "twice", "a third") in a body appears in the worksheet's Campaign Inputs. Call lengths are exempt.
- Touch 1 and every variant name every segment marker, show the proof or a marker in the first two sentences, and never write "your" + a marker.
- Every touch has a unique, non-bump Adds row in the Touch Map; one Type contains "objection"; touch 1's proof number reappears in a later touch.
- At least one variant; each has Kind, For, Gate and Subject; a signal variant's Gate names a list field in backticks.
- Subjects under 50 characters; `Subject B:` on every touch; reply touches keep "Re:" plus the parent's subjects; default subjects carry no tag with an assumed or low fill rate.
- Every merge tag has a fallback and a Fill Rates row; no body opens with I, we, our or my (Venetz flags seller-first openings).
- Sequence (or Copy Audit) comes first under a one-line header; the sending line names a time zone and a per-inbox cap; Test Plan has 100+ per arm and a Decide line; Reply offer states a delivery time and a proposed offer appears in Confirm Before Launch.
- The client's document has no Campaign Inputs, Fill Rates, Touch Map, Type or Adds lines, fill-rate or render notes, footer table, bracketed blanks, unlinked author or guide names, legal content, file paths or tool ids.

Earn the Right gate before anything sends (Venetz, 1-10-100 post):

| Gate | Pass when |
|-|-|
| 1 ask | One low-effort question, or the reply offer |
| 10 words | Subject plus preview name something about the reader, with no pleasantry or self-introduction |
| 100 words | Under 100 |
| Phone read | No scrolling to reach the ask |

Read for what the checker cannot see:

- Every question ask about the reader's week passes the hook test; the gap answer is the one the proof fixes.
- The reply offer is concrete, kept either way, and confirmed by the user (or marked proposed).
- The objection touch names the objection in the buyer's words and answers it with a fact, not reassurance.
- Each touch's Adds row is true of its body: a reader of touch 2 learns something touch 1 did not say.
- Results are stated as the client's results; nothing is projected onto the reader.
- Persona variants differ in stake, not only in length; signal variants say nothing the gated field does not show.
- No phrase from the banned list in `references/line-library.md` section 10.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| Question with an obvious answer ("you or your cleaning company?") | Every reader answers "me" and learns nothing | Hook test: answers vary, the gap answer points at the proof |
| Survey-style question ("Is churn something you track?") | Reads like a form; yes or no ends the thought | Ask about a moment in their week (when, how, what, who) |
| Touch 2 restates touch 1 from another side | No new reason to reply, so it trains the reader to skip | The Touch Map's Adds names a new fact, the objection answered, or the offer |
| Result projected onto the reader ("half as many complaint emails for you") | A promise the brief never made; one checked claim sinks the email | Client's result in the brief's own numbers |
| "Properties like yours" | Generic; the reader can't tell it was written for them | Name the segment marker: "Class B buildings in Denver" |
| Ask with nothing to gain ("open to a chat?") | Replying costs time and earns nothing | A reply offer they keep either way, confirmed by the user |
| Ignoring the objection every buyer has ("tenants always complain") | The silent objection kills the reply | One touch names it in their words and answers it with a fact |
| One email for director and site manager | Different stakes; one of them reads it as off-target | Persona variant gated on title |
| "Congrats on the new building" with no field showing it | An unverified trigger reads as a mail merge when wrong | Signal variant gated on a list field; other rows get touch 1 |
| `{{first_name}}` with no fallback | "Hi ," ships | Fallback in platform syntax; render an empty row |
| Link and image in touch 1 | Spam signals with no gain | Plain text, zero links |
| "Re:" on a first touch | The subject claims a thread the reader never had | "Re:" only on a real in-thread reply |
| Best result saved for touch 2 | Readers who stop at touch 1 never see it | Strongest proof in touch 1 |
| AI line states a fact not in the row | One wrong "congrats on the funding" costs the cell its credibility | Claims only from list fields; read the dry run first |
| QA tables and rationale in the deliverable | Padding the client scrolls past | Emails plus the decisions to confirm; checks run, not printed |
| "your Class B building" | Labels the reader's property with a rank | Name the slice you serve: "we clean Class B office buildings in Denver" |
| Proof only in touch 1 | A reader who skimmed it never sees the number | One line restating it in touch 3 or the breakup |
| Default subject built on a low-fill tag | Most inboxes get "night crew at your building" | Tag-free subject as default, tagged one as Subject B |
| "[Sender name]" or an unsigned body | A blank ships, and "we" has no name | Sign-off in every body; sender merge tags in the footer |
| Sender-rule table or "Berman's guide" in the deliverable | Unlinked claims the client cannot check | State the cadence as a choice; settings go to the platform, not the doc |
| Opening question plus an offer question in touch 1 | The reader can't tell which to answer | Statement opener; the ask is the only question |
| "Office buildings in Denver" when the user said Class B | Drops the user's own targeting | Every segment marker in touch 1 and each variant |
| Rating signal for an offer the reviews are not about | Reads as a jab and measures nothing the offer fixes | Gate only on a field that measures the problem, on the contact's row |
| Brief echoed back, Type/Adds lines, fill-rate column | Process material between the client and the emails | Keep them in the worksheet |
| "200 per arm" with no decision rule | Two to six replies per arm can't pick a winner | Decide line from the arms' own counts; keep sending until it clears |
| "Weekday mornings" | No time zone or cap to set in the platform | Business hours in the recipient's time zone, under 50 per inbox per day |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Picking which authority or library to open; where sources disagree |
| `references/line-library.md` | First lines by field (1 to 4), proof lines, asks, breakups, banned lines (10), voice by seniority (12), objection pre-handles (13), follow-up types (14), opening questions and segment words (15), a full property management sequence with variants (16) |
| `references/subject-line-library.md` | Subject variants by angle, trigger and persona (section 10) |
| `references/personalization-and-merge-fields.md` | Field map, fallbacks, spintax, plain text, AI-written lines (section 8), signal gates for variants (section 9) |
| `templates/output-template.md` | Starting a sequence document |
| `templates/output-template-worksheet.md` | Starting the worksheet the checker reads (inputs, fill rates, touch map) |
| `examples/worked-example.md` | An audit of a weak email, the rebuilt sequence with objection touch, and persona and signal variants (Illustrative example) |
| `examples/worked-example-worksheet.md` | The worksheet behind that example |
| `scripts/check-output.py` | Validating a sequence before it goes to the platform |
| `references/cold-email-frameworks.md` | Framework choice per cell, awareness levels (shared) |
| `references/alex-berman-cold-email.md` | What Alex Berman teaches, with sources (shared) |
| `references/scrapercity-catalog.md` | Tool ids, parameters, prices (shared) |
| `references/scrapercity-platform.md` | Plans and database fields (shared) |
| `references/deliverability-primer.md` | Plain text, links and authentication (shared) |

## Related Skills

- `cold-email-strategy` supplies the offer, the cells and the touch map.
- `reply-handling` writes the responses once someone replies.
- `multi-channel-outreach` writes the call, LinkedIn and mail touches between these emails.
- `email-deliverability` and `sending-platforms` take the finished sequence to the inbox.
- `signal-triggered-outbound` supplies dated trigger fields for signal variants.
- `local-business-list`, `ecommerce-by-techstack` and `icp-list-builder` build the lists these merge fields come from.
