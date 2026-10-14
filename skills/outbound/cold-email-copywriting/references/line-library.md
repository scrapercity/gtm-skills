# Line Library

Original lines for cold email, grouped by the ScraperCity field that feeds them. Merge tags use Instantly-style syntax with fallbacks (`{{tag | fallback}}`); convert for your platform with `references/personalization-and-merge-fields.md`. Every result, percentage and client in brackets must be replaced with your own. Never ship an invented proof line.

How to use: pick one first line, one proof line and one ask. Read the three together. If the first line does not set up the proof, pick another.

## 1. Local business first lines (Local Business Database, Google Maps, Yelp)

Fields: `title` (business name), `category_name`, `city`, `total_score`, `reviews_count`, `website`, `contact_first_name`.

### Strong rating (total_score 4.6+)

1. {{business_name}} has {{rating}} stars across {{reviews_count}} reviews, which puts you near the top for {{category | your category}} in {{city}}.
2. {{rating}} stars on {{reviews_count}} reviews is rare for a {{category | practice}} your size.
3. Your patients clearly like you: {{rating}} stars and {{reviews_count}} reviews on Google.
4. Read a few of your {{reviews_count}} reviews. Several mention the front desk by name.
5. {{business_name}} is one of the few {{category | shops}} in {{city}} above {{rating}} stars.
6. A {{rating}} rating usually means the work is good and the marketing is the bottleneck.
7. You have the kind of reviews other {{category | businesses}} in {{city}} would pay for.
8. With {{rating}} stars, you are the kind of {{category | business}} we like to work with.

### Strong rating, low review count (4.5+ stars, under 80 reviews)

9. {{business_name}} has a {{rating}} rating but {{reviews_count}} reviews, while the top three {{category | practices}} in {{city}} each have 150 or more.
10. Your rating is high for {{city}}, but searchers see the review count first.
11. {{rating}} stars from {{reviews_count}} reviews says patients love you and you could be asking more of them.
12. You are {{reviews_count}} reviews in, with a {{rating}} average. The next 100 are the easy part.

### Low rating (total_score 4.0 or lower)

13. Noticed {{business_name}} sits at {{rating}} stars on Google.
14. At {{rating}} stars on {{reviews_count}} reviews, {{business_name}} sits just under 4.0 on Google.
15. Most of your recent reviews look positive, but the {{rating}} average still carries the older ones.
16. Is the {{rating}} rating something you are working on this year?
17. A few unhappy reviews from years ago are holding {{business_name}} at {{rating}}.

### Category and city

18. We work with {{category | businesses}} around {{city}}, and {{business_name}} came up in our search.
19. Saw {{business_name}} while mapping {{category | businesses}} in {{city}}.
20. Most {{category | owners}} we talk to in {{city}} say the slow months are January and August.
21. Quick one for a {{category | business}} owner in {{city}}.

### Website present or missing

22. Your site is the first thing a {{city}} customer sees after your {{rating}} star listing.
23. Pulled up {{website}} on my phone. The booking button sits below the fold.
24. {{business_name}} has a strong listing but no website linked to it.

## 2. B2B first lines (Lead Database, Apollo Scraper)

Fields: `first_name`, `title`, `company_name`, `company_size`, `employees_count`, `company_industry`, `company_annual_revenue`, `company_city`, `keywords`.

### Title plus company size

25. As {{title | the sales lead}} at a {{employees_count | growing}} person {{industry | company}}, you are probably still hiring reps.
26. {{title | Sales leaders}} at {{employees_count}} person companies usually own both pipeline and hiring.
27. At {{company_name}}'s size, list building usually falls to the reps themselves.
28. Teams around {{employees_count}} people tend to outgrow spreadsheets before they buy a data tool.
29. You run {{department | sales}} at {{company_name}}, so this is either yours or you know whose it is.

### Industry and keywords

30. Saw {{company_name}} sells to {{keyword | your market}}.
31. {{industry | Your industry}} buyers rarely answer a generic pitch, so I will keep this specific.
32. We work with {{industry | software}} companies in the {{employees_count}} employee range.
33. Noticed {{company_name}} is headquartered in {{company_city | your city}}, where three of our clients are.

### Revenue band (only when filled)

34. Companies in the {{revenue_band}} range usually hit this problem when the second sales team starts.
35. At {{revenue_band}} in revenue, a one point gain in close rate pays for most tools.

### CEO first, then down (account-level sequencing)

36. Sending this to you first since you would know who owns {{problem_area}} at {{company_name}}.
37. Wrote to {{ceo_first_name}} last week; you looked like the person who owns this day to day.

## 3. Ecommerce first lines (Store Leads)

Fields: platform, `apps` (Shopify), `technologies`, `category`, estimated monthly visits, `city`, `country_code`.

### Platform

38. Saw {{store_name}} runs on {{platform | Shopify}}.
39. {{store_name}} is still on {{platform}}, which many {{category | stores}} your size have left.
40. {{store_name}} sells on {{platform | Shopify}} with {{app | Klaviyo}} installed.

### Installed apps (Shopify)

41. Noticed {{store_name}} runs {{app | Recharge}}. (Say "added" or "just installed" only when a dated column shows when.)
42. You have {{app | Klaviyo}} installed but the site shows no pop-up or welcome offer.
43. {{store_name}} runs {{app | Judge.me}} for reviews, so you already care about social proof.
44. Saw {{app}} on {{store_name}}. [Client] replaced it in [time] and [measured result].
45. With {{app | Recharge}} live, month two churn is usually the number to watch.

### Technologies

46. {{store_name}} uses {{technology}}, which is the setup we migrate most often.
47. Your checkout still loads {{technology}}.

### Traffic band and category

48. {{store_name}} looks like it gets steady traffic for a {{category | store}} brand.
49. Stores in {{category}} with your traffic tend to lose the most to cart abandonment.
50. Most {{category | apparel}} stores we see at your size have one email flow running.

## 4. Technology users (Tech Stack Search plus Website Finder)

Every domain in a `scrape_builtwith` result uses the technology searched.

51. Saw {{company_name}} runs {{technology}}.
52. Teams on {{technology}} usually ask us about {{adjacent_problem}} first.
53. {{company_name}} is one of a small set of {{industry | companies}} still on {{technology}}.
54. You built {{company_name}} on {{technology}}, which makes this a 2 week project for us.

## 5. Proof lines

Replace every bracket with a measured client result.

55. We did this for a [client type] in [nearby city]: [metric] went from [before] to [after] in [time].
56. A [size] [category] we work with went from [before] to [after] [metric] in [time].
57. Our last [category] client added [result] in the first [time].
58. [Client type] in [city] used the same setup and booked [number] [outcome] in [month].
59. For a [category] store at your traffic, this added [dollar figure] in [time].
60. One [title] at a [size] [industry] company cut [metric] from [before] to [after].
61. We have done this for [number] [category] businesses in [state], the latest in [month].
62. A [client type] with a similar rating went from [before] to [after] stars in [time].
63. It took [client] [time] and about [hours] of their staff time.
64. The [client type] in [city] paid for it in [time] from [outcome].

## 6. Asks (one per email, always a question)

Low effort:

65. Want the template we used?
66. Should I send the [asset]?
67. Want to take a look?
68. Open to seeing how it worked?
69. Want me to run the same check on {{business_name | your site}}?
70. Is this on your list for this quarter?

Meeting asks:

71. Open to 10 minutes next week?
72. Open to a 15 minute call Tuesday or Wednesday?
73. Would a short call to compare numbers be useful?
74. Can I show you the before and after on a quick call?

Problem-first questions (Braun-style neutral):

75. How are you getting new reviews today?
76. When a subscriber cancels before the second charge, what reason do they give you most?
77. Who builds the lead lists for new reps right now?
78. Is that something you are trying to change, or is it fine for now?
79. How do you handle {{problem}} today?

Referral asks:

80. Are you the right person for this, or is it someone on your team?
81. Who handles {{problem_area}} at {{company_name}}?

## 7. Follow-up openers (touches 2 and 3)

Write the touch's `Adds:` line first, then pick an opener that delivers it.

82. One more result that fits {{business_name}}: [result].
83. Different angle: [second problem the same buyer has].
84. A [client type] asked the same question last month. We found [finding].
85. I put together the [asset] for {{category | businesses}} in {{city}}. Want it?
86. Quick add: this works without changing your [current tool].
87. If retention sits with someone else at {{company_name | your team}}, who should I send the [asset] to?
88. If timing is the issue, when should I check back?

## 8. Breakup lines (last touch)

89. I will close your file for now. If [problem] comes up later, reply here and I will pick it up.
90. Should I stop here, or is there a better person to send this to?
91. Last note from me on this. Want me to check back in [month]?
92. Looks like this is not a priority right now. Should I close it out?
93. If this belongs to someone else at {{company_name}}, who should I ask?

## 9. Sign-offs

94. Thanks, {{sender_first_name}}
95. {{sender_first_name}}, {{sender_company}}
96. Cheers, {{sender_first_name}}

Keep the signature to name, company and one line, without logo images, banners or social icons.

## 10. Banned lines and why

| Line | Problem | Replace with |
|-|-|-|
| I hope this email finds you well | Filler before the point | Start with the fact |
| I came across your company | Says nothing specific | A field value |
| I wanted to reach out | Describes the email instead of saying something | Delete |
| We are the leading provider of | Claim without proof, about you | Proof line about a client |
| Just checking in / bumping this up | Adds nothing | Follow-up opener with new value |
| Let me know your thoughts. | No question to answer | One question ending in ? |
| Do you have 30 minutes for a demo? | Heavy ask from a stranger | 10 to 15 minutes, or a resource |
| Re: on a first email | Misleading subject | Plain subject |
| As per my last email | Reads as irritated | A new angle |
| Synergy, leverage, solutions, revolutionary, best-in-class, robust, seamless, innovative | Vague words that look like marketing copy | The specific outcome |
| Properties like yours / businesses like yours | Generic; the reader can't tell the email is about their slice | The segment marker: "Class B buildings in Denver" |
| Half as many [problems] for you | Projects a client result onto the reader | The client's result in the brief's numbers |

## 11. Assembled examples (all under 100 words)

Local, strong rating, 3C (51 words):

```text
Hi {{first_name | there}},

{{business_name}} has {{rating}} stars across {{reviews_count}} reviews, near the top for dentists in {{city}}.

We built the new patient page for a 3-chair practice in Round Rock with similar reviews. Form fills went from 9 to 26 a month in 60 days.

Want to see what we changed?
```

Ecommerce trigger (40 words):

```text
Hi {{first_name | there}},

Noticed {{store_name}} runs Recharge.

For one coffee subscription store, a single skip-a-month email cut month two cancellations from 31% to 19%.

Want the email we used?
```

B2B experience question plus proof (50 words):

```text
Hi {{first_name | there}},

When a new rep starts, how long before they're working their own list: a week, or closer to a month?

One fintech client cut new rep ramp from 7 weeks to 3 by handing each rep a validated list on day one.

Open to seeing a sample for your territory?
```

## 12. Voice by seniority

No source cited here sets body length by seniority; every level stays under 100 words. The columns below are starting points to test inside a cell.

| Level | What they care about | Proof that works | Ask that fits | Sample first line |
|-|-|-|-|-|
| VP or C-level | A number they report upward: pipeline, revenue, churn, cost | A named peer company and one result | "Who owns this?" or 10 minutes | Teams at {{company_name}}'s size usually see ramp time show up in the quarterly number. |
| Director | This quarter's plan, team output, the budget they control | Same size peer, timeline, effort required | 15 minute comparison or a sample | Directors running {{department}} at {{employees_count}} people usually own both the plan and the tools. |
| Manager | The team's weekly workload, hitting targets, tools the team uses | How it works in their current tool | A template or a short walkthrough | Your reps probably build their own lists before they make a call. |
| Individual contributor | Their own time, tasks they dislike, looking good to their manager | The task removed and the hours saved | A resource, no meeting | Building territory lists by hand usually eats the first week of a quarter. |
| Local business owner | Cash this month, a full schedule, their reputation in town | A nearby business in the same category | A resource or a yes or no question | {{business_name}} has {{rating}} stars, the first number a {{city}} customer sees on Maps. |

Rules that hold at every level: one problem, one proof, one ask; at senior levels the proof names a peer. When the cell mixes levels, split it (`cold-email-strategy` cell rules).


## 13. Persona objection pre-handles

A pre-handle answers the objection this persona raises first, before they raise it. Name the objection in the buyer's words, agree with the true part, then answer with a fact from the brief, never with reassurance ("we're different"). Nowoslawski's rule for offers is the test: the email has to answer why this person would not reply. Use it in touch 2 by default. Replace every bracket with your own facts.

| Persona | Likely objection | Pre-handle line |
|-|-|-|
| Practice or shop owner | "We already ask for reviews" | Asking at the front desk is common; the change that worked for [client] was a text sent within an hour of the visit. |
| Practice or shop owner | "No time to set it up" | Setup took [client]'s front desk about [minutes] minutes; we handle the rest. |
| Ecommerce founder | "We have an agency for that" | This runs inside the account you already have, and your agency keeps everything else. |
| Ecommerce founder | "We already use [app]" | It works with {{app}}, so nothing gets replaced. |
| VP Sales | "We have a data vendor" | [client] kept their vendor and uses us for the segments it misses, such as [segment]. |
| RevOps or sales ops | "Integration work" | It arrives as a CSV or directly in {{crm}}, with no new tool for reps to learn. |
| Director of Operations | "No budget this quarter" | The pilot covers [locations] locations for [days] days and can be cancelled any time. |
| Manager or IC | "Someone else decides that" | If this sits with [title], would you point me to them? |
| Agency owner | "Cold email does not work for us" | The campaigns that failed for [client type] usually had a list problem before a copy problem. |
| Site property manager (janitorial seller) | "Tenants always complain" | Some complaints never stop; the part you can change is who spots a cleaning miss first. At [client building], [measured result]. |
| Site property manager (janitorial seller) | "We already have a cleaning company" | Keep them for now; the walkthrough shows what they miss, in writing, so you can raise it with them either way. |
| Portfolio director | "Each site manager picks their own vendors" | [Client] kept site managers' choices and added one weekly report across [number] buildings. |
| Owner or director | "Cheaper is fine for Class B" | [Client] pays [price change] and logged [result] fewer tenant requests; the brief must carry both numbers. |

Assembled pre-handle follow-up (53 words):

```text
Hi {{first_name | there}},

You may already have an agency running Klaviyo for {{store_name | your store}}.

The reorder flow we build sits inside your existing account, and your agency keeps everything else. Two of our [category] clients run it that way today.

Would it help if I sent the flow map to whoever manages Klaviyo for you?
```

## 14. Follow-up types

Each follow-up has one type and one `Adds:` line: the new reason to reply that touch brings (a new fact, the objection answered, the reply offer, a route to the right person). Pick the type, write the `Adds:` line, then the body. If the `Adds:` line repeats an earlier touch, cut the touch.

| Type | Job | Best position | Ask |
|-|-|-|-|
| Proof | A second, different result | Touch 2 | Low-effort question |
| Angle | A different problem the same buyer has | Touch 3 | Problem-first question |
| Value-add resource with no ask | Give something useful and ask for nothing | Touch 2 or 3, after a direct ask in touch 1 | None; the body has no question mark |
| Objection pre-handle | Answer the persona's usual objection (section 13) | Touch 2 or 3 | Low-effort question |
| Reframe | The same problem from another side (cost instead of time, tenant instead of owner), carrying a fact the reader has not seen yet. A reframe without a new fact is a bump: cut it | Touch 3 | Problem-first question |
| Referral | Ask who owns the problem | Touch 3 or 4 | "Who handles this?" |
| Breakup | Offer to close the file | Last touch | Yes or no question |

Mark a no-ask touch with `Type: value-add (no ask)` in the sequence document. The checker then requires zero question marks in that body instead of a closing question. Use at most one no-ask touch per sequence, and never as touch 1.

Value-add resource with no ask (62 words):

```text
Hi {{first_name | there}},

No ask in this one. Here is the timing data from our dental clients this year.

Review texts sent within an hour of the visit got [x]% of patients to post a review. Sent the next day, [y]%. After three days, almost none.

If your team asks by hand, the one hour window is the part to copy.
```

Reframe (43 words):

```text
Hi {{first_name | there}},

Another way to look at reviews: they are what a new patient compares when two practices are the same distance away.

{{business_name | Your practice}} has {{rating}} stars on {{reviews_count}} reviews.

Want to see how that compares with the five closest practices to you?
```

## 15. Opening questions and segment words

Touch 1 opens with a question the reader answers in their head from their own week. Each one below names a specific moment and passes the hook test in `SKILL.md` step 5: answers vary by reader, a good-fit reader's honest answer is the gap the proof fixes, and no option embarrasses. They state no facts about the reader, so they can't be wrong.

| # | Segment | Opening question | The gap answer |
|-|-|-|-|
| 97 | Property management (cleaning seller) | When the night crew finishes, how do you find out what they missed: a walkthrough, or the first tenant email? | The first tenant email |
| 98 | Property management (turnover seller) | After a move-out, how many days before the unit's ready to show? | More than the reader would like |
| 99 | Dental practice | When a patient leaves happy, who asks for the review: the front desk, the dentist, or whoever remembers? | Whoever remembers |
| 100 | SaaS sales team | When a new rep starts, how long before they're working their own list: a week, or closer to a month? | Closer to a month |
| 101 | HVAC or home services | When the phone rings after 5pm, who picks it up: you, an answering service, or voicemail? | Voicemail |
| 102 | Shopify subscription brand | When a subscriber cancels before the second charge, what reason do they give you most? | Any reason the skip email can answer |
| 103 | Restaurant group | When a server calls out on a Friday, who finds the cover: the GM or the server? | The GM |
| 104 | Accounting firm | When a client sends receipts in a shoebox in March, who on your team sorts them? | A senior person |

Questions that fail:

| Fails | Why | Rewrite |
|-|-|-|
| When a tenant complaint comes in, who hears first: you or your cleaning company? | Every manager answers "me"; nothing learned | #97 |
| Is tenant satisfaction something you track? | Survey; yes or no ends the thought | #97 |
| Do you have a process for reviews? | Asks the reader to defend a choice | #99 |
| Are you happy with your current vendor? | Invites a reflexive "yes" | Ask how they find out what the vendor missed |

Their words, starter lists (confirm with the user before relying on them):

| Segment | Their words |
|-|-|
| Property management | night crew, walkthrough, punch list, work order, tenant request, common areas, make-ready, turnover, lease renewal |
| Dental practice | hygiene schedule, recall, chair time, front desk, new patients, no-shows, treatment plan |
| Shopify subscription brand | subscribers, second charge, skip, swap, cancel flow, renewal, box |
| SaaS sales team | ramp, territory, pipeline, quota, book of business, SDR, discovery call |
| HVAC or home services | dispatch, service call, tune-up, maintenance plan, after-hours, tech in the truck |

## 16. Assembled sequence: janitorial company to Denver Class B property managers

Illustrative example. Front Range Night Clean is a fictional janitorial company; the Aurora and Lakewood clients and every number below are invented for illustration. Use results and an offer from your own brief.

Brief facts this sequence may use: a 140,000 sq ft Class B office building in Aurora, CO (client's work order log, 2025): tenant cleaning requests fell from 22 a month to 7 in 60 days after a night supervisor began walking every floor with a signed checklist; the supervisor photographs each restroom and common area and sends the property manager a report by 6 a.m. A Lakewood owner with three Class B buildings gets one weekly cleaning report for all three in place of three vendor email threads. Reply offer (proposed, confirm before launch): a free after-hours walkthrough of one building with a written punch list within 48 hours, the manager's to keep. Likely objection: "Tenants always complain." Segment markers: Denver, Class B.

Touch 1 (site property manager, day 1, new thread). Subject: after the night crew leaves. Subject B: night crew at {{building_name | your building}} (tagged subject goes to B while the building name fill rate is unmeasured). Adds: the Aurora result and the walkthrough offer.

```text
Hi {{first_name | there}},

If the first you hear about a missed restroom is a tenant email, the night crew has already had a full shift to fix it.

Front Range Night Clean does nightly janitorial for Class B office buildings in Denver. At a Class B building in Aurora, a supervisor now walks every floor nightly with a signed checklist, and tenant cleaning requests fell from 22 a month to 7 in 60 days.

Want a free after-hours walkthrough of {{building_name | your building}}, with a written punch list you keep either way?
```

Touch 2 (objection, day 4, reply to touch 1). Adds: answers "tenants always complain" with the 6 a.m. photo report.

```text
Hi {{first_name | there}},

Tenants will always find something to complain about. The part you can change is who spots a cleaning miss first.

At the Aurora building, the night supervisor photographs each restroom and common area and sends the property manager a report by 6 a.m., before tenants arrive.

Want a sample report?
```

Touch 3 (new angle, day 9, new thread). Subject: one report for every building. Subject B: cleaning across your buildings. Adds: the Lakewood portfolio fact.

```text
Hi {{first_name | there}},

Different angle, for Denver managers with more than one building.

A Lakewood owner with three Class B buildings now gets one weekly cleaning report for all three, in place of three vendor email threads.

Would one report across your buildings help, or do you run them one at a time?
```

Touch 4 (breakup, day 16, reply to touch 3). Adds: referral route.

```text
Hi {{first_name | there}},

I'll close the file here. If cleaning comes up at {{building_name | your building}}, a reply reopens it.

Is someone else on your team the right person for vendor contracts?
```

Persona variant, portfolio director (gate: title contains Director, VP, Regional or Portfolio; every other row gets touch 1). Subject: cleaning across {{company_name | your portfolio}}. The stake moves from tomorrow's walkthrough to comparing buildings.

```text
Hi {{first_name | there}},

A Lakewood owner with three Class B buildings in the Denver area gets one weekly cleaning report for all three, in place of three vendor email threads.

At one Aurora building, tenant cleaning requests fell from 22 a month to 7 in 60 days.

Want a free after-hours walkthrough of one building, so you can see the report format?
```

No signal variant: no list field shows cleaning at a specific building. A building listing's Google rating is mostly about parking, leasing and the tenants' own businesses, so it measures nothing the offer fixes, and quoting a low score to the manager reads as a jab.

What this sequence avoids: two questions in touch 1, a touch 2 that restates touch 1, and any line such as "half as many cleaning emails for you" that turns the Aurora result into a promise.

## Sources

- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.11x.ai/guides/josh-braun-cold-outreach-method
- https://www.insidesales.com/leveraging-trigger-events/
- https://hunter.io/blog/cold-email-word-count
- https://leslievenetz.substack.com/p/1-10-100-b2b-cold-email
- https://www.gong.io/blog/does-cold-email-even-work-any-more-heres-what-the-data-says
- https://thegtmengineer.substack.com/p/the-winning-cold-outbound-formula
