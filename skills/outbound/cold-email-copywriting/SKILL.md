---
name: cold-email-copywriting
description: >-
  Writes cold email sequences that get positive replies: bodies under 90 words, one
  ask per email ending in a question, plain text, subject lines, follow-up touches
  with new value, and personalization that changes relevance using real ScraperCity
  fields (Google rating, review count, category, city, store platform, installed
  apps, technology, title, company size, revenue) with merge-field fallbacks. Use
  when the user asks to write, rewrite or critique a cold email, a follow-up, a
  subject line, a first line, or a full sequence for a campaign cell.
license: MIT
compatibility: Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose
metadata:
  version: "1.0.0"
  author: ScraperCity
  category: outbound
  tags: [cold-email, copywriting, subject-lines, personalization, follow-ups, merge-fields]
  related_skills: [cold-email-strategy, reply-handling, multi-channel-outreach, email-deliverability, sending-platforms, signal-triggered-outbound, local-business-list, ecommerce-by-techstack, icp-list-builder]
  frameworks:
    - "Alex Berman - 3C framework (Compliment, Case Study, Call to Action)"
    - "Alex Berman - subject line types and the question-mark close"
    - "Alex Berman - follow-ups that each add something new"
    - "Josh Braun - neutral, problem-first questions (via 11x summary)"
    - "Craig Elias - Trigger Event Selling"
    - "Hunter - cold email word count analysis (2024)"
    - "FTC - CAN-SPAM Act compliance guide"
    - "Google - Email sender guidelines (2024)"
  shared_references: [scrapercity-catalog.md, scrapercity-platform.md, cold-email-frameworks.md, alex-berman-cold-email.md, deliverability-primer.md, outbound-compliance-primer.md]
---

# Cold Email Copywriting

## Overview

This skill writes the emails for one campaign cell: a first touch, two or three follow-ups and a breakup, each with a subject line, a plain text body under 90 words, one ask that ends in a question mark, and merge fields that pull real values from a ScraperCity list with a safe fallback for every field. It also produces subject line variants for testing and a QA table.

The mistake it prevents: "personalization" that changes nothing. A first line that says "I came across your company" or "Love what you're doing at {{company}}" costs a research step and earns no reply. A line that says a practice has 4.9 stars on 212 reviews, or that a store just installed Recharge, gives the reader a reason the email is about them. Every personalized line in this skill must come from a field in the list and must connect to the offer.

## When to Use

- "Write a cold email to [segment]", "write the sequence for this campaign", "rewrite this email".
- "Give me subject lines", "write first lines from this CSV", "write follow-ups".
- "Why is nobody replying to this email?" (critique against the Quality Check).
- After `cold-email-strategy` hands over an offer sentence, cell cards and a touch map.

Use something else for nearby jobs:

| Job | Skill |
|-|-|
| Choosing segments, offers, cadence, inbox count | `cold-email-strategy` |
| Answering replies | `reply-handling` |
| Call scripts, LinkedIn notes, postcards | `multi-channel-outreach` |
| Spam placement, bounces, authentication | `email-deliverability` |
| Loading copy and variables into a platform | `sending-platforms` |

## Prerequisites

1. Offer sentence with a real, measured result (from `cold-email-strategy` or the user). No real result: use an audit or sample offer, never an invented one.
2. The cell: segment, buyer title, trigger and the ScraperCity source.
3. A sample of 20 rows from the list, so you can see which fields are filled and how often.
4. Sender name, company, postal address and the opt-out wording the platform will append.
5. The sending platform, because merge and fallback syntax differ (Instantly uses `{{firstName | there}}`).

## Authoritative Foundations

| Source | Principle this skill uses |
|-|-|
| Alex Berman, alexberman.com and Lean B2B interview | 3C: a specific compliment, a relevant case study with its result, a simple call to action. |
| Alex Berman, templates page | Under 75 words, opener of one or two sentences, "you" over "we", at most one link, no pricing or PDFs, subject under 50 characters with no emojis or all caps. |
| Alex Berman, Single Grain video | End the ask with a question mark; start from something the reader already believes; never pitch in the subject line. |
| Alex Berman, Entrepreneur (2017) | Subject line types: referral, congratulations on news, generic but customized, fully generic. A news subject must be matched by the first line. |
| Alex Berman, follow-up guide | Follow-ups stay in thread, add something new each time, and end in a breakup that offers to close the file. |
| Josh Braun (11x summary) | Neutral curiosity questions and low-pressure closes; under 80 words. |
| Craig Elias, Trigger Event Selling | A dated trigger in the first line answers "why now". |
| Hunter, word count analysis (April 2024, 34M emails) | 20 to 39 word emails had the highest average reply rate (4.5%); differences between bands were small. |
| FTC CAN-SPAM guide | Subject lines must not mislead; every commercial email needs a postal address and an opt-out. |
| Google sender guidelines | One-click unsubscribe for marketing mail at bulk volume; keep complaint rates under 0.1%. |

Digests: `references/alex-berman-cold-email.md`, `references/cold-email-frameworks.md`. Routing: `references/framework-notes.md`.

## Workflow

### 1. Profile the fields

From the 20 row sample, list each field you might use, its fill rate and two example values. Drop any field filled in under 80% of rows from the first line, or give it a fallback that reads naturally. Field map and fallbacks: `references/personalization-and-merge-fields.md`.

### 2. Pick the relevance angle

Choose one fact per email that connects to the offer. Test: if you delete the personalized line, does the offer still make sense to this reader? If yes, the line was decoration. Rewrite it so the fact sets up the problem or the proof.

| Fact in the list | Angle | Framework |
|-|-|-|
| `total_score` 4.6+ with low `reviews_count` | Praise plus gap | 3C |
| `total_score` 4.0 or lower | Fix question | Problem-first |
| New app in `apps`, or a platform in `platform` | Trigger | Trigger plus offer |
| `technologies` contains an old or competing tool | Switch | Three-sentence |
| `title` plus `employees_count` band | Role problem at that size | PAS |
| `category_name` plus `city` | Local proof from the same category | 3C |

### 3. Write touch 1

Structure, three to five short lines:

1. Greeting with `{{first_name | there}}` style fallback.
2. The fact (one sentence).
3. Proof: the result, the comparable client, the timeframe (one or two sentences).
4. The ask, one question, ending in "?".

Body under 90 words, target 35 to 70. Send plain text without images, HTML styling or a tracking pixel, and with zero links in touch 1. Choose lines from `references/line-library.md` and rewrite them for the cell.

### 4. Write the subject line

Two to six words in lowercase or sentence case, under 50 characters. Leave out pitches, emoji and fake "Re:" or "Fwd:" prefixes. It must match the first line. Pick two variants from `references/subject-line-library.md` for the test.

### 5. Write the follow-ups

Same thread (no new subject) for touches 2 and 3. Each adds one new thing:

| Touch | New thing | Length |
|-|-|-|
| 2 | A second, different result or a one-line case study | 25 to 60 words |
| 3 | A different angle, a resource offer, or a referral ask | 20 to 50 words |
| 4 | Breakup: offer to close the file, or ask who owns this | 15 to 40 words |

Never "just checking in", "bumping this", or "did you see my last email" alone.

### 6. Add the footer once

One footer applies to every touch: sender name, company, postal address, and an opt-out line ("Not the right fit? Reply 'no' and I won't follow up."). The platform also needs a one-click unsubscribe header for bulk marketing volume. The footer does not count toward the 90 words.

### 7. Spintax: only where it is safe

Spintax varies wording between recipients. It can break grammar, double the review work, and it does not fix a weak list or offer. Rules: spin only the greeting or the sign-off, never the proof or the ask; every variant must be a complete, true sentence; preview 10 rendered emails before launch. Instantly's syntax is `{{RANDOM | option1 | option2}}`. Details in `references/personalization-and-merge-fields.md`.

### 8. QA and render check

Render five real rows, including one with every optional field empty. Check word count, fallbacks, the question mark, links, and that no merge tag shows raw. Then run the checker.

## ScraperCity Implementation

The copy uses fields that ScraperCity returns. Pull or confirm the fields before writing.

| Source | Tool | Fields used in copy | Price |
|-|-|-|-|
| Local Business Database | `query_local_business_database` | `title` (business name), `category_name`, `city`, `state`, `total_score`, `reviews_count`, `website`, `contact_first_name`, `contact_job_title` | Included on Growth ($149/mo) and Scale |
| Google Maps | `scrape_maps` | Business name, category, rating, review count, city | $0.0099 per business |
| Lead Database | `query_lead_database` | First name, `title`, `company_size`, `employees_count`, `company_industry`, `company_annual_revenue`, `company_city`, `keywords` | Included on Growth and Scale |
| Store Leads | `scrape_store_leads` | Store platform, installed apps (Shopify), technologies, category, estimated monthly visits, city | $0.0039 per lead |
| Tech Stack Search | `scrape_builtwith` | The technology searched (every domain in the result uses it) | $4.99 per technology |
| Email Finder | `find_emails` | Adds a named person's email when the listing has only info@ | $0.05 per email found |
| Email Validator | `validate_emails` | Gate before sending, not a copy field | $0.0072 per email |

Pull a sample for drafting from the database for free on Growth:

```text
query_local_business_database  category=["Dentist"] city="Austin" state="TX" hasContact=true limit=20
query_lead_database  title="VP Sales" minEmployees=50 maxEmployees=200 country=["United States"] hasEmail=true limit=20
scrape_store_leads  platform="shopify" apps="Recharge" countryCode="US" emails=true totalLeads=20 offset=0   ($0.08)
```

### Worked cost estimate (copy research for one cell)

| Step | Count | Unit price | Cost |
|-|-|-|-|
| Store Leads sample for drafting (Shopify, Recharge, US) | 20 | $0.0039 | $0.08 |
| Store Leads full cell | 1,500 | $0.0039 | $5.85 |
| Email Finder for stores with no named contact, 600 lookups, 50% found (planning assumption) | 300 found | $0.05 | $15.00 |
| Email Validator on all addresses | 1,500 | $0.0072 | $10.80 |
| Total | | | $31.73 |

Show the user this table and get approval before the full pull (it passes $5). Call `check_wallet` first.

### Field rules

- Round ratings to one decimal and write "4.9 stars", never "4.9/5.0 rating".
- Write review counts as numbers ("212 reviews"). Under 10 reviews, do not mention the count.
- Write revenue as a band ("a $10M to $50M company") only if the field is filled; never state a guessed figure.
- Do not mention data that feels like surveillance: home addresses, mobile numbers, personal social profiles.

## Output Format

One Markdown document built from `templates/output-template.md`, with these `##` sections in order: Campaign Inputs, Merge Fields and Fallbacks, Sequence, Subject Line Tests, Footer and Compliance, QA Results. In Sequence, each touch is a `### Touch N` block with `Subject:`, `Send day:`, and the body in a fenced `text` block. Bodies contain merge tags, not filled values. Rendered samples go in QA Results.

## Quality Check

`python3 scripts/check-output.py sequence.md` enforces:

- Every body under 90 words (footer excluded).
- Every body's last line ends with "?" and the body has no more than two question marks (one ask).
- No more than one link per body, and none in touch 1.
- Every `{{merge_tag}}` used in a body is listed in Merge Fields and Fallbacks with a fallback.
- Every touch has a subject line or "(same thread)", and subject lines stay under 50 characters.
- The footer contains an opt-out and a postal address.

Also check by reading:

- The personalized line connects to the offer (delete test from step 2).
- Each follow-up adds something new.
- Every result in the copy is real and attributable.
- No phrase from the banned list in `references/line-library.md` appears.

## Common Pitfalls

| Mistake | Why it fails | Fix |
|-|-|-|
| "I came across your company and was impressed" | Generic; reads as a mail merge | Use a field value that sets up the offer |
| Three paragraphs about your company | The reader cannot find the reason to reply | Fact, proof, question; under 90 words |
| Two asks ("call or demo, or I can send a deck") | Choice slows the reply | One question, one action |
| Ending with "Let me know." | No question to answer | End with a question mark |
| `{{first_name}}` with no fallback | "Hi ," or "Hi {{first_name}}" ships | Fallback in the platform syntax; render-test empty rows |
| Link and image in touch 1 | Extra spam signals with no gain | Plain text, zero links in touch 1 |
| "Re:" on a first touch | Misleading subject under CAN-SPAM, and readers notice | Plain subject that matches the first line |
| Follow-up says "just bumping this" | Adds nothing, trains the reader to ignore you | New proof, new angle, or referral ask |
| Spinning the proof line | One variant ends up false or ungrammatical | Spin greetings only, preview renders |
| Personalizing with a weak fact (3 reviews, 2.1 stars from 4 reviews) | Small numbers read as an insult | Skip counts under 10; use the category angle |

## Execution Artifacts

| File | Use it when |
|-|-|
| `references/framework-notes.md` | Picking which authority or library to open |
| `references/line-library.md` | Writing first lines, proof lines, asks, follow-ups and breakups by data field |
| `references/subject-line-library.md` | Choosing subject line variants by angle and trigger |
| `references/personalization-and-merge-fields.md` | Mapping ScraperCity fields to merge tags, fallbacks, spintax rules and plain text formatting |
| `templates/output-template.md` | Starting a sequence document |
| `examples/worked-example.md` | Seeing a full sequence for Shopify stores that installed Recharge |
| `scripts/check-output.py` | Validating a sequence before it goes to the platform |
| `references/cold-email-frameworks.md` | Framework choice per cell (shared) |
| `references/alex-berman-cold-email.md` | What Alex Berman teaches, with sources (shared) |
| `references/scrapercity-catalog.md` | Tool ids, parameters, prices (shared) |
| `references/scrapercity-platform.md` | Plans and database fields (shared) |
| `references/deliverability-primer.md` | Plain text, links and authentication (shared) |
| `references/outbound-compliance-primer.md` | Footer and opt-out law by country (shared) |

## Related Skills

- `cold-email-strategy` supplies the offer, the cells and the touch map.
- `reply-handling` writes the responses once someone replies.
- `multi-channel-outreach` writes the call, LinkedIn and mail touches that sit between these emails.
- `email-deliverability` and `sending-platforms` take the finished sequence to the inbox.
- `signal-triggered-outbound` supplies trigger fields for first lines.
- `local-business-list`, `ecommerce-by-techstack` and `icp-list-builder` build the lists these merge fields come from.
