# Signal Catalog

Every signal ScraperCity data can show, with the exact pull, how to detect the change, what date to attach, how fast it decays, what goes wrong, and the angle for the first line. Half-lives and max ages are house starting points (dated 2026-10) with no measured data behind them; shorten or lengthen them from your own conversion data by age bucket (`references/scoring-and-freshness.md` section 7).

Column names: Local Business Database rows carry `title`, `category_name`, `phone`, `website`, `total_score`, `reviews_count`, `postal_code` and the `contact_*` fields. For scrapers (Maps, Yelp, Store Leads, BizBuySell, Distress List, Zillow Agents, Tech Stack Search), read the header row of the downloaded CSV before mapping; column names can change between versions.

## Summary

| # | Signal | Tool | Change detected | Date anchor | Half-life (days) | Max age (days) | Base points |
|-|-|-|-|-|-|-|-|
| S1 | New local listing | `query_local_business_database`, `scrape_maps`, `scrape_yelp` | Record absent last pull, present now, reviews 5 or fewer | First-seen pull date | 30 | 60 | 35 |
| S2 | Review velocity | `scrape_maps`, `scrape_yelp`, `query_local_business_database` | `reviews_count` up by a threshold between pulls | Pull date of the jump | 21 | 45 | 25 |
| S3 | Rating drop | Same as S2 | `total_score` down 0.2 or more between pulls | Pull date of the drop | 21 | 45 | 30 |
| S4 | Review stall | Same as S2 | No new reviews in 60 days while local peers gained | Pull date | 30 | 90 | 15 |
| S5 | Technology adopted | `scrape_builtwith` | Domain absent from last week's list, present now | First-seen pull date | 45 | 90 | 35 |
| S6 | Technology removed | `scrape_builtwith` | Domain present last week, absent now, still absent next week | Second consecutive absent pull | 30 | 60 | 30 |
| S7 | Store app installed | `scrape_store_leads` with `apps` | Domain newly matches the `apps` filter | First-seen pull date | 45 | 90 | 35 |
| S8 | Traffic band crossed | `scrape_store_leads` | Estimated monthly visits moved across a band edge between monthly pulls | Pull date | 60 | 120 | 20 |
| S9 | Platform or plan change | `scrape_store_leads` (`platform`, `planExclude`) | Domain appears under a new platform or leaves an excluded plan tier | Pull date | 45 | 90 | 30 |
| S10 | Business listed for sale | `scrape_bizbuysell` | Listing URL not in last pull | First-seen pull date | 30 | 90 | 35 |
| S11 | Pre-foreclosure or auction | `scrape_distress_list` | Property address not in last pull, or distress type changed | First-seen pull date; auction date when the row has one | 14 | 45 | 40 |
| S12 | Agent new to a market | `scrape_zillow_agents` | Agent profile not in last month's pull for the location | First-seen pull date | 45 | 90 | 20 |
| S13 | New-to-account record | `query_lead_database`, `query_local_business_database`, Ecommerce Database | Returned with `excludeDelivered=true` | Pull date | 60 | 120 | 10 |

Base points feed the signal strength part of the score (0 to 40). A record with two live signals takes the higher decayed value plus 5, capped at 40.

## S1. New local listing

- **Pull:** weekly `query_local_business_database` with `keyword`, `location` and `maxReviews: 5`. Add `excludeDelivered: true` to receive only records the account does not have. For markets the database covers thinly, run `scrape_maps` with the same keyword and city and filter reviews in the CSV.
- **Detect:** key not in the snapshot and reviews 5 or fewer. Diff key: E.164 `phone`, then `business_name_key` plus `postal_code` (see `references/list-quality-standard.md` 3f).
- **False positives:** an old business that moved, rebranded or added a second location; a listing that was missing from your earlier pull because of a filter change. Check the website footer year or "opening soon" text for tier A.
- **Angle:** new businesses need customers and reviews before anything else. "Saw Lakeview Pediatric Dentistry show up on Google Maps in the last couple of weeks with 3 reviews."
- **Do not say:** "Congratulations on opening" unless the site or listing says it opened.

## S2. Review velocity

- **Pull:** keep a watched set (the ICP universe) and re-pull it. `scrape_yelp` with `directUrls` re-checks known businesses at $0.0099 each; `scrape_maps` re-runs the search. A Local Business Database re-pull of owned records is free but check that values change first (SKILL.md, ScraperCity Implementation).
- **Detect:** reviews gained since last pull at or above max(10, 25% of the previous count) within 30 days.
- **False positives:** review-gating campaigns, a merged listing, a burst of fake reviews. Look at the rating at the same time: velocity plus a rating dip is a different story than velocity plus 5.0.
- **Angle:** growth creates capacity strain. "Hill Country Plumbing added 46 reviews in the last month, more than any plumber in Austin we track."

## S3. Rating drop

- **Detect:** `total_score` down 0.2 or more since last pull. Google shows one decimal, so 0.2 is two display steps.
- **False positives:** one review on a small base (a business with 12 reviews moves 0.2 on one bad review). Require at least 20 reviews.
- **Angle:** reputation repair, without blame. "Noticed Iron Yard's Google rating moved from 4.8 to 4.5 this month. Is that a few bad weeks or something you're working on?"
- **Do not say:** "Your customers are unhappy" or quote a negative review back to them.

## S4. Review stall

- **Detect:** zero new reviews over 60 days while the median competitor in the same category and city gained 5 or more.
- **Angle:** review requests. Lowest urgency, longest half-life.

## S5. Technology adopted

- **Pull:** weekly `scrape_builtwith` with `technology` (one technology per run, $4.99). Output is a domain list.
- **Detect:** domain in this week's list and absent from last week's. Intersect with the ICP universe (Store Leads or Lead Database companies) before scoring; a raw Tech Stack Search list covers every site using the technology.
- **False positives:** detection lag (the site added it months ago and was just crawled), agencies and theme demos, staging domains. Exclude domains on `myshopify.com` subdomains and known agency domains.
- **Angle:** onboarding help or the next tool in the stack. "Saw Northpaw started running Klaviyo in the last few weeks. The first 90 days are when flows get built or don't."

## S6. Technology removed

- **Detect:** domain on last week's list, absent on this week's and the following week's. One absence is not enough; detection gaps happen.
- **Check by hand:** load the site and look for the script or the vendor's badge before any tier A touch.
- **Angle:** displacement window. "Looks like Fernway moved off HubSpot recently. What are you running marketing email on now?" Ask, do not assert.

## S7. Store app installed

- **Pull:** `scrape_store_leads` with `platform: "shopify"`, `apps` (Shopify only), `countryCode`, visit bands and `totalLeads`; page with `offset` and `nextOffset`. Every pull bills $0.0039 per row returned, including repeats, so keep `apps` pulls narrow or use Tech Stack Search for the same app when it is detectable there.
- **Detect:** domain newly matches. If the universe filter also changed (a visits band), the domain may have crossed the band instead; check S8 first.
- **Angle:** the job the app creates. Recharge creates subscription churn work; a reviews app creates review request flows.

## S8. Traffic band crossed

- **Pull:** monthly Store Leads universe with no visits filter inside your size range, or with a wider band than you sell to. Compare estimated monthly visits per domain between months.
- **Detect:** crossed 50,000 or 100,000 estimated monthly visits upward (growth) or fell 30% or more (decline).
- **False positives:** estimates move with methodology; treat a single month as weak. Require two consecutive months for tier A.
- **Angle (growth):** "Northpaw's traffic looks to have roughly doubled since summer." Use "looks to" because the figure is an estimate.

## S9. Platform or plan change

- **Detect:** domain appears under `platform: "shopify"` that was under another platform last pull, or leaves a tier excluded with `planExclude` (for example "Shopify Plus").
- **Angle:** migration clean-up, apps to rebuild, redirects and SEO checks.

## S10. Business listed for sale

- **Pull:** weekly `scrape_bizbuysell` with saved search URLs per category and region in `startUrls`, `maxItems`, and the same `datasetName` every week so dedupe across runs works.
- **Detect:** listing URL not in the snapshot.
- **Who to contact:** the listing broker (broker contacts come with the listing) or, for buyers, the seller through the broker. Do not try to go around the broker to the owner.
- **Angle by offer:** buyer: "We have a buyer for HVAC service businesses in the $1M to $3M revenue range in Maricopa County." Lender: "Is the buyer for the Mesa listing lined up on financing yet?" Services: valuation, transition, bookkeeping clean-up.

## S11. Pre-foreclosure or auction

- **Pull:** weekly `scrape_distress_list` with `search` (city and state or ZIP), `distressTypes: ["preForeclosure", "auction"]`, `maxItems` up to 500 per run. Split a large market into ZIP runs.
- **Detect:** address not in the snapshot, or `distressTypes` changed (pre-foreclosure to auction raises urgency).
- **Owners are consumers.** Phone: National DNC scrub, internal list, hand dial, 9am to 8pm local, no texts. Mail: plain, respectful, no official-looking envelopes, no implied lender or government affiliation. Any offer to help avoid foreclosure is a mortgage assistance relief service under Regulation O (12 CFR 1015): no advance fees. State foreclosure consultant and equity purchaser laws apply. See `references/outbound-compliance-primer.md` section 10.
- **Contact data:** `scrape_property_lookup` with `includeOwnerContact: true` ($0.25 per property) or `find_people` by address ($0.0199 per result). Prospecting only, never an eligibility decision (FCRA).
- **Angle:** offer options and keep pressure out. "I buy houses in Seminole Heights and saw the property at 4410 W Linda Ln may be heading to auction. If selling before then would help, I can make a cash offer this week."

## S12. Agent new to a market

- **Pull:** monthly `scrape_zillow_agents` with `location`, optional `specialty` and `language`, `searchLimit` up to 500.
- **Detect:** agent profile not in last month's pull for that location. Could mean newly licensed, moved brokerages, or newly listed on Zillow.
- **Angle:** setup work. "Looks like you recently started showing up for Scottsdale on Zillow. Are you building your own listing photos and CRM from scratch, or bringing them from your last market?"

## S13. New-to-account records

- **Pull:** daily `query_lead_database` or `query_local_business_database` with the ICP filters, `excludeDelivered: true`, `page: 1` or the `after` cursor. Ecommerce Database through REST with the same flag.
- **Meaning:** records the account has never received. Useful as a fresh-contact feed and a dedupe guarantee. It carries no dated event about the prospect.
- **Angle:** none from the flag itself; use the record's fit and any other live signal. Score it low on its own.

## Signals outside these tools

| Event | Reason | If the user has it |
|-|-|-|
| Funding rounds | No ScraperCity tool returns funding events | Import from the user's source, label `source = other:<name>` in the queue |
| Job postings and hiring | Same | Same |
| Leadership changes and new hires | Same; the Lead Database has no job-change field | Same |
| Website visits and intent data | Same | Same |
| Press, awards, expansions | Same | Same |

## Sources

- https://www.insidesales.com/leveraging-trigger-events/
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://scrapercity.com/llm-info
- https://www.npmjs.com/package/scrapercity
