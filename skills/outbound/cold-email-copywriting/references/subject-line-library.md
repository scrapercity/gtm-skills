# Subject Line Library

Original subject lines grouped by angle. All are under 50 characters before merge values and avoid emoji, all caps and fake "Re:" or "Fwd:" prefixes. The subject must match the first line of the email: if the subject mentions reviews, the first line is about reviews.

Background from Alex Berman's public work: his 2017 Entrepreneur article lists four types (referral, congratulations on news, generic but customized, fully generic) and says relevance drives opens; his Single Grain video favors short neutral lines such as "Quick question" or "Question about" plus the company name, and warns that readers delete an email unread when the subject pitches; his templates page calls "Quick Question" its control.

Because Apple Mail Privacy Protection inflates opens, judge subject tests on replies, and only after the offer and segment tests are settled.

## 1. Neutral, company-named (default control)

1. Question about {{company_name}}
2. quick question, {{first_name}}
3. {{company_name}}
4. {{company_name}} and {{sender_company}}
5. Hi from {{sender_first_name}}
6. idea for {{company_name}}
7. {{first_name}}, a question
8. about {{business_name}}
9. for {{first_name}} at {{company_name}}
10. {{company_name}} question

## 2. Local business: rating and reviews

11. {{business_name}}'s {{rating}} stars
12. your {{reviews_count}} reviews
13. reviews at {{business_name}}
14. {{rating}} stars in {{city}}
15. Google reviews, {{business_name}}
16. {{business_name}} on Google
17. your rating in {{city}}
18. review count vs {{city}} leaders
19. more reviews for {{business_name}}
20. the {{rating}} average

## 3. Local business: category and city

21. {{category}} in {{city}}
22. {{city}} {{category}} question
23. new patients in {{city}}
24. slow months at {{business_name}}
25. {{business_name}} website
26. booking page at {{business_name}}
27. {{city}} customers
28. for the {{business_name}} team

## 4. Ecommerce: platform, apps, technology

29. {{app}} at {{store_name}}
30. {{store_name}} on {{platform}}
31. Recharge churn at {{store_name}}
32. Klaviyo flows at {{store_name}}
33. {{store_name}}'s checkout
34. leaving {{platform}}?
35. {{technology}} at {{company_name}}
36. {{store_name}} repeat orders
37. month two at {{store_name}}
38. {{store_name}} welcome email
39. cart recovery, {{store_name}}
40. {{category}} stores like yours

## 5. B2B: role and size

41. {{title}} question
42. new rep ramp at {{company_name}}
43. lists for your SDRs
44. {{company_name}} pipeline
45. hiring reps at {{company_name}}
46. {{department}} at {{company_name}}
47. {{employees_count}} person sales team
48. {{company_name}} outbound
49. territory lists, {{first_name}}
50. forecast at {{company_name}}

## 6. Trigger and news (first line must reference the same event)

51. congrats on {{event}}
52. saw {{company_name}} added {{app}}
53. new location in {{city}}
54. {{company_name}}'s move to {{platform}}
55. after the {{event}}
56. {{event}}, {{first_name}}

## 7. Proof-led

57. how a {{city}} {{category}} got 120 reviews
58. 9 to 26 form fills
59. {{category}} result in {{nearby_city}}
60. what worked for a {{category}} store
61. a {{industry}} case in 2 lines

(Proof subjects need a measured result. Fill numbers only from your own client data.)

## 8. Referral and routing

62. right person for {{problem_area}}?
63. who owns {{problem_area}}?
64. {{referrer_first_name}} suggested you
65. {{referrer_first_name}} at {{company_name}}

Use "suggested you" only when the referrer named this person in a reply. Implying a referral that did not happen misleads the reader.

## 9. Follow-ups and breakup

Every touch gets its own subject and one alternative. Berman's follow-up guide keeps the first three or four touches in one thread, so touches 2 to 4 reply in touch 1's thread and keep "Re:" plus touch 1's subject. Write "Re:" only on a touch that is a reply in an existing thread. Subjects for a touch that opens a new thread, or a breakup sent after the sequence:

66. closing the loop, {{first_name}}
67. should I close this out?
68. last one on {{topic}}
69. {{company_name}}, for later

## 10. Persona-specific subject lines

Match the subject to what the persona tracks (`references/line-library.md` section 12). The first line must pick up the same topic. Tags are shown without fallbacks to keep the table readable; add one for each tag per `references/personalization-and-merge-fields.md`.

| # | Persona | Subject | First line should be about |
|-|-|-|-|
| 70 | VP or C-level | {{metric}} at {{company_name}} | The number they report upward |
| 71 | VP or C-level | {{peer_company}} and {{company_name}} | A named peer result (only if the peer agreed to be named) |
| 72 | VP or C-level | who owns {{problem_area}}? | A referral ask, for a top-down first touch |
| 73 | Director | {{department}} plan for next quarter | The quarter plan and the budget they control |
| 74 | Director | {{employees_count}} person {{department}} team | A same-size peer and its timeline |
| 75 | Manager | your team's {{task}} | The weekly workload their team carries |
| 76 | Manager | {{task}} in {{tool}} | How it works in a tool they already use |
| 77 | Individual contributor | {{task}} by hand | The task removed and the hours saved |
| 78 | Individual contributor | template for {{task}} | A free resource, no meeting |
| 79 | Local business owner | slow months at {{business_name}} | Cash flow in their quiet season |
| 80 | Local business owner | {{city}} customers and {{business_name}} | Local reputation, rating or reviews |
| 81 | Ecommerce founder | repeat orders at {{store_name}} | Revenue from customers they already have |
| 82 | Ecommerce founder | {{app}} at {{store_name}} | The installed app and what it leaves on the table |
| 83 | RevOps or sales ops | {{crm}} data at {{company_name}} | Data quality and the time it costs the team |
| 84 | Operations leader, multi-location | {{location_count}} locations, one process | Consistency across sites |
| 85 | Site property manager | night crew at {{building_name}} | What the cleaning crew missed last night |
| 86 | Site property manager | after the night crew leaves | How misses get found before tenants arrive |
| 87 | Portfolio director | cleaning across {{company_name}} | Comparing buildings, one report |
| 88 | Any, segment-named | {{city}} Class B cleaning | The segment marker the first line repeats |

## 11. Subject line rules

| Rule | Why |
|-|-|
| A few words, under 50 characters | Berman's templates page sets the 50 character cap; the Lean B2B interview says three to four words |
| Lowercase or sentence case | Reads like a note from a person |
| No pitch, price, "free", or percentage | Readers delete pitch subjects unread (Berman, Single Grain) |
| Skip emoji, all caps and exclamation marks | Promotional signals |
| Never "Re:" or "Fwd:" on a first touch or any new thread | The subject claims a thread the reader never had; "Re:" belongs only on a real in-thread reply |
| A subject plus one A/B alternative for every touch | Each email can be tested; threaded replies follow the parent's A or B |
| Fallback for every merge tag | "Question about " with an empty name looks broken |
| Matches the first line | A news subject with no news in the body reads as bait (Berman, Entrepreneur) |
| A segment marker in touch 1's subject or first line | The reader sees it was written for their slice (city, class, category) before opening |

## 12. Subject test plan

| Step | Variant A | Variant B | Per variant (Berman: 100 to 200+) | Decide on |
|-|-|-|-|-|
| 1 | Neutral company-named (#1) | Data-specific (#11 or #29) | 200 delivered | Positive replies per 100 delivered |
| 2 | Winner | Proof-led (#57 to #61) | 200 delivered | Same |
| 3 | Winner | Lowercase vs sentence case of the winner | 200 delivered | Same, low priority |

## Sources

- https://www.entrepreneur.com/article/292394
- https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- https://alexberman.com/cold-email-templates
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
