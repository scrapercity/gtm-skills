# Line Library

Original lines for cold email, grouped by the ScraperCity field that feeds them. Merge tags use Instantly-style syntax with fallbacks (`{{tag | fallback}}`); convert for your platform with `references/personalization-and-merge-fields.md`. Every result, percentage and client in brackets must be replaced with a real one. Never ship an invented proof line.

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
7. You have the reviews most {{category | businesses}} in {{city}} would pay for.
8. With {{rating}} stars, you are the kind of {{category | business}} we like to work with.

### Strong rating, low review count (4.5+ stars, under 80 reviews)

9. {{business_name}} has a {{rating}} rating but {{reviews_count}} reviews, while the top three {{category | practices}} in {{city}} each have 150 or more.
10. Your rating beats most of {{city}}, but searchers see the review count first.
11. {{rating}} stars from {{reviews_count}} reviews says patients love you and few of them are asked.
12. You are {{reviews_count}} reviews in, with a {{rating}} average. The next 100 are the easy part.

### Low rating (total_score 4.0 or lower)

13. Noticed {{business_name}} sits at {{rating}} stars on Google.
14. At {{rating}} stars, {{business_name}} drops below the 4.0 filter some searchers use.
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
26. Most {{title | sales leaders}} at {{employees_count}} person companies own both pipeline and hiring.
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
39. {{store_name}} is still on {{platform}}, which most {{category | stores}} your size have left.
40. Noticed {{store_name}} moved to {{platform | Shopify}}.

### Installed apps (Shopify)

41. Noticed {{store_name}} added {{app | Recharge}}.
42. You have {{app | Klaviyo}} installed but the site shows no pop-up or welcome offer.
43. {{store_name}} runs {{app | Judge.me}} for reviews, so you already care about social proof.
44. Saw {{app}} on {{store_name}}. Most stores we work with replace it in the first year.
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

Replace every bracket with a real client result.

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
67. Worth a look?
68. Open to seeing how it worked?
69. Want me to run the same check on {{business_name | your site}}?
70. Is this on your list for this quarter?

Meeting asks:

71. Worth 10 minutes next week?
72. Open to a 15 minute call Tuesday or Wednesday?
73. Would a short call to compare numbers be useful?
74. Can I show you the before and after on a quick call?

Problem-first questions (Braun-style neutral):

75. How are you getting new reviews today?
76. Is month two churn something you track?
77. Who builds the lead lists for new reps right now?
78. Is that something you are trying to change, or is it fine for now?
79. How do you handle {{problem}} today?

Referral asks:

80. Are you the right person for this, or is it someone on your team?
81. Who handles {{problem_area}} at {{company_name}}?

## 7. Follow-up openers (touches 2 and 3, same thread)

Each one adds something new.

82. One more result that fits {{business_name}}: [result].
83. Different angle: [second problem the same buyer has].
84. A [client type] asked the same question last month. Here is what we found: [finding].
85. I put together the [asset] for {{category | businesses}} in {{city}}. Want it?
86. Quick add: this works without changing your [current tool].
87. Not sure the first note reached the right person, so here is the short version: [offer in one line].
88. If timing is the issue, when should I check back?

## 8. Breakup lines (last touch)

89. I will close your file for now. If [problem] comes up later, reply here and I will pick it up.
90. Should I stop here, or is there a better person to send this to?
91. Last note from me on this. Want me to check back in [month]?
92. Looks like this is not a priority right now. Should I close it out?
93. If this belongs to someone else at {{company_name}}, who should I ask?

## 9. Sign-offs

94. Thanks, {{sender_first_name}}
95. {{sender_first_name}}, [Company]
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
| Synergy, leverage, solutions, revolutionary | Vague words that look like marketing copy | The specific outcome |

## 11. Assembled examples (all under 90 words)

Local, strong rating, 3C (51 words):

```text
Hi {{first_name | there}},

{{business_name}} has {{rating}} stars across {{reviews_count}} reviews, near the top for dentists in {{city}}.

We built the new patient page for a 3-chair practice in Round Rock with similar reviews. Form fills went from 9 to 26 a month in 60 days.

Worth a look at what we changed?
```

Ecommerce trigger (40 words):

```text
Hi {{first_name | there}},

Noticed {{store_name}} added Recharge.

For one coffee subscription store, a single skip-a-month email cut month two cancellations from 31% to 19%.

Want the email we used?
```

B2B PAS (55 words):

```text
Hi {{first_name | there}},

Most sales leaders at {{employees_count}} person companies have reps building their own lists in the first month.

That is about four weeks of salary before a single meeting. One fintech client cut new rep ramp from 7 weeks to 3 by handing each rep a validated list on day one.

Open to seeing a sample for your territory?
```

## Sources

- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.11x.ai/guides/josh-braun-cold-outreach-method
- https://www.insidesales.com/leveraging-trigger-events/
- https://hunter.io/blog/cold-email-word-count
