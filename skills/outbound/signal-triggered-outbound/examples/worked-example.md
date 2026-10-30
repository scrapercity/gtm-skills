# Signal Program: Tidewater Retention, Shopify Stores Adopting or Leaving Klaviyo

Illustrative example: Tidewater Retention and every store below are fictional, and store domains use the reserved `.example` suffix.

Offer: Klaviyo email and SMS flows for Shopify stores, $3,500 setup plus $1,800 a month. ICP: US Shopify stores with 20,000 to 150,000 estimated monthly visits and a public email, in apparel, pets, food and beverage, and home goods. Buyer: founder or head of ecommerce. Stack: ScraperCity Growth plan ($149 a month, $159 in credits), n8n on a small server, Postgres for snapshots, HubSpot for tasks, Instantly for tier B, Slack #signals for tier A. Half-lives, points, cut-offs and windows below are Tidewater's starting settings, re-fit from its own meeting rate after four cycles.

## Signal Catalog

| Signal | Source | Detection rule | Date anchor | Half-life (days) | Max age (days) | Base points | Touch within |
|-|-|-|-|-|-|-|-|
| S5 Klaviyo adopted | Tech Stack Search for Klaviyo, intersected with the Store Leads universe | Domain in this week's Klaviyo list, absent last week, inside the ICP universe | First-seen pull date | 45 | 90 | 35 | 2 business days |
| S6 Klaviyo removed | Tech Stack Search for Klaviyo, intersected with the universe | On the list two weeks ago, absent on the last two weekly pulls, and a site check finds no Klaviyo script | Second consecutive absent pull | 30 | 60 | 30 | 2 business days after the site check |
| S8 Traffic band crossed | Store Leads monthly universe | Estimated monthly visits crossed 50,000 upward between two monthly pulls | Universe pull date | 60 | 120 | 20 | 5 business days |

Not used: funding and job posts (S17, S18), untested for this ICP and next quarter's test; website visitor ID (S14), since Tidewater has no visitor tool; new-to-account Ecommerce Database records, which carry no event.

## Scoring Model

| Component | Rule | Points |
|-|-|-|
| Fit: category | Apparel, pets, food and beverage, home goods 15; beauty or outdoor 7 | 0 to 15 |
| Fit: visits band | 30,000 to 100,000 visits 10; 20,000 to 30,000 or 100,000 to 150,000 visits 5 | 0 to 10 |
| Fit: geography | US store with a US address 10 | 0 to 10 |
| Fit: plan | Not on Shopify Plus 5 | 0 to 5 |
| Signal strength | Base points x 0.5 ^ (age / half-life); a second live signal adds 5; cap 40 | 0 to 40 |
| Reachability | Named founder or ecommerce lead 6, valid email 6, mobile on file 5, website 3 | 0 to 20 |
| Negative: retention agency in place | Agency credit in the store footer, or the store named in a competing agency's case study, seen on the site check; pause 180 days | -30 |
| Negative: traffic fell | Visits dropped below 20,000 in the monthly universe; pause 30 days, until the next universe pull | -20 |
| Tiers | A 70 and up, B 40 to 69, C under 40 | 0 to 100 |

Example: northpaw.example, Klaviyo first seen 7 days ago: fit 35 + strength 35 x 0.5 ^ (7 / 45) = 31.4 + reachability 15 = 81.4, tier A.

## Exclusions

Checked before scoring; excluded accounts get no score, enrichment or alert.

| Class | Match rule | List source |
|-|-|-|
| Competitors | Domain on the list of 41 retention and email agencies; brand-name matches flagged for review | Founder's list plus the Klaviyo partner directory |
| Vendors | Domain on the vendor list | Accounting system export |
| Partners | Domain on the co-sell and referral list | Partnerships sheet |
| Agencies | Domain on the non-competing agency list, or a store name containing studio, theme or agency, reviewed by hand (theme demo stores add Klaviyo for client builds) | Shopify theme and app partner pages |
| Customers and open opportunities | HubSpot lifecycle customer or an open deal; the signal is logged on the record for the owner | HubSpot export each cycle |
| Do not contact | Domain on the do-not-contact list | Founder |

## Routing and SLAs

| Tier | First touch | SLA | Owner | Missed SLA |
|-|-|-|-|-|
| A | Call and email the same day | 2 business days from detection | Account executive, HubSpot task plus Slack alert | Workflow moves the task to the founder the next morning |
| B | Email 1 of the signal campaign | 5 business days | SDR, Instantly | Workflow adds the account to the next day's batch |
| C | None | Re-score each pull; drop at max age | Workflow | None |

| Signal | First contact | Second thread (after email 2, no reply) |
|-|-|-|
| S5 | Founder | Marketing or ecommerce manager |
| S6 | Founder | Head of ecommerce |
| S8 | Head of ecommerce, else founder | Founder |

Each campaign: 4 emails over 14 days, inside Instantly's March 2026 guidance of 4 to 7 emails over 14 to 21 days, the first follow-up 3 days after email 1; tier A adds a call on day 1. Stop on any reply. One signal sequence per store per 90 days, after Instantly's advice to pause two to three months before re-engaging.

## First Emails

Claims to confirm: the two-week rebuild time (S6) and each proof result come from Tidewater's delivery records; everything else restates the offer above.

### S5 Klaviyo adopted

Angle: new Klaviyo account, flows not yet built; offer the flow map.

> Subject: Klaviyo flows at {{company}}
>
> Hi {{first_name}}, saw {{company}} started running Klaviyo in the last {{weeks_since_detected}} weeks.
>
> Which flows are live so far: welcome, browse abandon, reorder? We build those three for {{category}} stores at your traffic; {{proof_result}}.
>
> Want the flow map we used?

Fields: {{first_name}} and {{company}} from the Lead Database contact; {{weeks_since_detected}} = weeks since the first Klaviyo pull that showed the domain (2); {{category}} from the Store Leads category column (pet supplies); {{proof_result}} from Tidewater's client results sheet ("a treats brand added $11,400 in repeat revenue in its first 45 days").

### S6 Klaviyo removed

Angle: platform switch; ask what they run now, do not assert.

> Subject: email and SMS at {{company}}
>
> Hi {{first_name}}, looks like {{company}} moved off Klaviyo in the last {{weeks_since_removed}} weeks.
>
> Did the welcome, abandon and reorder flows come across to the new platform, or are they being rebuilt? We rebuild them in two weeks and use your old flow revenue as the number to beat.
>
> What are you running email and SMS on now?

Fields: {{first_name}} and {{company}} from the Lead Database contact; {{weeks_since_removed}} = weeks since the last pull that showed Klaviyo (3).

### S8 Traffic band crossed

Angle: traffic grew; ask whether post-purchase flows grew with it. Visits are estimates, so "looks to".

> Subject: repeat orders at {{company}}
>
> Hi {{first_name}}, {{company}}'s traffic looks to have passed {{visits_band}} visits a month since {{prior_pull_month}}.
>
> Are your post-purchase flows keeping pace with the new traffic? We build them for {{category}} stores in your range; {{proof_result}}.
>
> Worth a look at what we would add first?

Fields: {{visits_band}} = the band edge crossed in Store Leads estimated monthly visits (50,000); {{prior_pull_month}} = month of the earlier universe pull (September); {{category}} from the Store Leads category column (apparel); {{proof_result}} from Tidewater's client results sheet ("one apparel store added 9% to repeat revenue in a quarter"); {{first_name}} and {{company}} from the Lead Database contact.

## Pulls and Cost

| Pull | Source, in plain words | Frequency | Cost per run | Cost per 4 weeks |
|-|-|-|-|-|
| ICP universe | Store Leads: US Shopify stores, 20,000 to 150,000 monthly visits, with an email, not on Shopify Plus (9,800 stores) | Monthly, 1st at 07:00 CT | $38.22 | $38.22 |
| Klaviyo detections | Tech Stack Search: every domain running Klaviyo | Weekly, Monday 06:15 CT | $4.99 | $19.96 |
| Buyers | Lead Database: founder, CEO and ecommerce titles at tier A and B domains (29 a week, estimate) | Weekly after scoring | $0.00, included in Growth | $0.00 |
| Founders the database lacks | Website Finder on the remaining domains (7 found a week, estimate) | Weekly after scoring | $0.35 | $1.40 |
| Email check | Email Validator on contacts not checked in 30 days (36 a week) | Weekly | $0.06 | $0.24 |
| Mobiles | Mobile Finder for tier A founders (4 found a week) | Weekly | $1.00 | $4.00 |
| Total | | | | $63.82 of the $159 Growth credits |

## Launch Plan

| Week of | Step | Owner |
|-|-|-|
| 2026-10-13 | Approve the $63.82 spend; run a 100-store universe test ($0.39) and confirm the visits filter applied | Founder |
| 2026-10-19 | Baseline: full universe and first Klaviyo pull stored; no alerts from the baseline | Ops lead |
| 2026-10-26 | First cycle: diff, score and route; tier A calls and tier B campaigns start | Ops lead and account executive |
| 2026-11-23 | Review four cycles: meetings per 100 contacts by signal and age bucket against the static Shopify campaign; re-fit half-lives and cut-offs | Founder |
