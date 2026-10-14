# Signal Catalog

Every signal ScraperCity data can show (S1 to S13), plus the signals that start outside ScraperCity (S14 to S28: website visits, job changes, funding, hiring, new leaders, earnings and filings, product launches, events, social engagement, G2 category intent, webinar and content engagement) and the negative signals that lower a score, with the exact pull or feed, how to detect the change, what date to attach, what goes wrong, and the angle for the first line. No published study gives half-lives, max ages, base points or touch windows for these signals, so the program sets each one in its Signal Catalog and re-fits it from its own meeting rate by age bucket (`references/scoring-and-freshness.md` section 7). Where a source gives a timing fact (UserGems' first 90 days for new executives, the Form D and 8-K filing windows), it is noted under the signal. Who to contact, the touch plan and a full first email for each outside signal: `references/signal-plays.md`.

Column names: Local Business Database rows carry `title`, `category_name`, `phone`, `website`, `total_score`, `reviews_count`, `postal_code` and the `contact_*` fields. For scrapers (Maps, Yelp, Store Leads, BizBuySell, Distress List, Zillow Agents, Tech Stack Search), read the header row of the downloaded CSV before mapping; column names can change between versions.

## Summary

| # | Signal | Tool | Change detected | Date anchor |
|-|-|-|-|-|
| S1 | New local listing | `query_local_business_database`, `scrape_maps`, `scrape_yelp` | Record absent last pull, present now, reviews at or under the program's new-listing cap | First-seen pull date |
| S2 | Review velocity | `scrape_maps`, `scrape_yelp`, `query_local_business_database` | `reviews_count` up by a threshold between pulls | Pull date of the jump |
| S3 | Rating drop | Same as S2 | `total_score` down 0.2 or more between pulls | Pull date of the drop |
| S4 | Review stall | Same as S2 | No new reviews over the program's window while local peers gained | Pull date |
| S5 | Technology adopted | `scrape_builtwith` | Domain absent from last week's list, present now | First-seen pull date |
| S6 | Technology removed | `scrape_builtwith` | Domain present last week, absent now, still absent next week | Second consecutive absent pull |
| S7 | Store app installed | `scrape_store_leads` with `apps` | Domain newly matches the `apps` filter | First-seen pull date |
| S8 | Traffic band crossed | `scrape_store_leads` | Estimated monthly visits moved across a band edge between monthly pulls | Pull date |
| S9 | Platform or plan change | `scrape_store_leads` (`platform`, `planExclude`) | Domain appears under a new platform or leaves an excluded plan tier | Pull date |
| S10 | Business listed for sale | `scrape_bizbuysell` | Listing URL not in last pull | First-seen pull date |
| S11 | Pre-foreclosure or auction | `scrape_distress_list` | Property address not in last pull, or distress type changed | First-seen pull date; auction date when the row has one |
| S12 | Agent new to a market | `scrape_zillow_agents` | Agent profile not in last month's pull for the location | First-seen pull date |
| S13 | New-to-account record | `query_lead_database`, `query_local_business_database`, Ecommerce Database | Returned with `excludeDelivered=true` | Pull date |

Base points feed the signal strength part of the score. Stacking and the optional cap for a signal that should not reach tier A alone: `references/scoring-and-freshness.md` section 1.

## S1. New local listing

- **Pull:** weekly `query_local_business_database` with `keyword`, `location` and `maxReviews` set to the program's new-listing cap. Add `excludeDelivered: true` to receive only records the account does not have. For markets the database covers thinly, run `scrape_maps` with the same keyword and city and filter reviews in the CSV.
- **Detect:** key not in the snapshot and reviews at or under the cap. Diff key: E.164 `phone`, then `business_name_key` plus `postal_code` (see `references/list-quality-standard.md` 3f).
- **False positives:** an old business that moved, rebranded or added a second location; a listing that was missing from your earlier pull because of a filter change. Check the website footer year or "opening soon" text for tier A.
- **Angle:** new businesses need customers and reviews before anything else. "Saw Lakeview Pediatric Dentistry show up on Google Maps in the last couple of weeks with 3 reviews."
- **Do not say:** "Congratulations on opening" unless the site or listing says it opened.

## S2. Review velocity

- **Pull:** keep a watched set (the ICP universe) and re-pull it. `scrape_yelp` with `directUrls` re-checks known businesses at $0.0099 each; `scrape_maps` re-runs the search. A Local Business Database re-pull of owned records is free but check that values change first (SKILL.md, ScraperCity Implementation).
- **Detect:** reviews gained since last pull at or above the threshold the program sets (an absolute count, a share of the previous count, or both).
- **False positives:** review-gating campaigns, a merged listing, a burst of fake reviews. Look at the rating at the same time: velocity plus a rating dip is a different story than velocity plus 5.0.
- **Angle:** growth creates capacity strain. "Hill Country Plumbing added 46 reviews in the last month, more than any plumber in Austin we track."

## S3. Rating drop

- **Detect:** `total_score` down by at least the drop the program sets since last pull. Google shows one decimal, so the smallest visible move is 0.1.
- **False positives:** one review on a small base moves the average a lot. Set a minimum review count for this signal.
- **Angle:** reputation repair, without blame. "Noticed Iron Yard's Google rating moved from 4.8 to 4.5 this month. Is that a few bad weeks or something you're working on?"
- **Do not say:** "Your customers are unhappy", or quote a negative review back. Both state a cause the data does not show, and the reply turns into a defense of the business instead of a talk about the fix.

## S4. Review stall

- **Detect:** zero new reviews over the window the program sets while the median competitor in the same category and city kept gaining.
- **Angle:** review requests.

## S5. Technology adopted

- **Pull:** weekly `scrape_builtwith` with `technology` (one technology per run, $4.99). Output is a domain list.
- **Detect:** domain in this week's list and absent from last week's. Intersect with the ICP universe (Store Leads or Lead Database companies) before scoring; a raw Tech Stack Search list covers every site using the technology.
- **False positives:** detection lag (the site added it months ago and was just crawled), agencies and theme demos, staging domains. Exclude domains on `myshopify.com` subdomains and known agency domains.
- **Angle:** onboarding help or the next tool in the stack. "Saw Northpaw started running Klaviyo in the last few weeks. The first 90 days are when flows get built or don't."

## S6. Technology removed

- **Detect:** domain on last week's list and absent on this week's; confirm on the next pull or by hand before acting.
- **Check by hand:** load the site and look for the script or the vendor's badge before any tier A touch.
- **Angle:** displacement window. "Looks like Fernway moved off HubSpot recently. What are you running marketing email on now?" Ask, do not assert.

## S7. Store app installed

- **Pull:** `scrape_store_leads` with `platform: "shopify"`, `apps` (Shopify only), `countryCode`, visit bands and `totalLeads`; page with `offset` and `nextOffset`. Every pull bills $0.0039 per row returned, including repeats, so keep `apps` pulls narrow or use Tech Stack Search for the same app when it is detectable there.
- **Detect:** domain newly matches. If the universe filter also changed (a visits band), the domain may have crossed the band instead; check S8 first.
- **Angle:** the job the app creates. Recharge creates subscription churn work; a reviews app creates review request flows.

## S8. Traffic band crossed

- **Pull:** monthly Store Leads universe with no visits filter inside your size range, or with a wider band than you sell to. Compare estimated monthly visits per domain between months.
- **Detect:** crossed one of the program's visit band edges upward (growth) or fell by the share the program sets (decline).
- **False positives:** estimates move with methodology; confirm a crossing on the next monthly pull before a tier A touch.
- **Angle (growth):** "Northpaw's traffic looks to have roughly doubled since summer." Use "looks to" because the figure is an estimate.

## S9. Platform or plan change

- **Detect:** domain appears under `platform: "shopify"` that was under another platform last pull, or leaves a tier excluded with `planExclude` (for example "Shopify Plus").
- **Angle:** migration clean-up, apps to rebuild, redirects and SEO checks.

## S10. Business listed for sale

- **Pull:** weekly `scrape_bizbuysell` with saved search URLs per category and region in `startUrls`, `maxItems`, and the same `datasetName` every week so dedupe across runs works.
- **Detect:** listing URL not in the snapshot.
- **Who to contact:** the listing broker (broker contacts come with the listing) or, for buyers, the seller through the broker. Listings often leave out the business name and the broker screens buyers, so a note to the owner directly gets forwarded to the broker or goes unanswered.
- **Angle by offer:** buyer: "We have a buyer for HVAC service businesses in the $1M to $3M revenue range in Maricopa County." Lender: "Is the buyer for the Mesa listing lined up on financing yet?" Services: valuation, transition, bookkeeping clean-up.

## S11. Pre-foreclosure or auction

- **Pull:** weekly `scrape_distress_list` with `search` (city and state or ZIP), `distressTypes: ["preForeclosure", "auction"]`, `maxItems` up to 500 per run. Split a large market into ZIP runs.
- **Detect:** address not in the snapshot, or `distressTypes` changed (pre-foreclosure to auction raises urgency).
- **Contact data:** `scrape_property_lookup` with `includeOwnerContact: true` ($0.25 per property) or `find_people` by address ($0.0199 per result).
- **Angle:** an offer tied to the auction date. "I buy houses in Seminole Heights and saw the property at 4410 W Linda Ln may be heading to auction. If selling before then would help, I can make a cash offer this week."

## S12. Agent new to a market

- **Pull:** monthly `scrape_zillow_agents` with `location`, optional `specialty` and `language`, `searchLimit` up to 500.
- **Detect:** agent profile not in last month's pull for that location. Could mean newly licensed, moved brokerages, or newly listed on Zillow.
- **Angle:** setup work. "Looks like you recently started showing up for Scottsdale on Zillow. Are you building your own listing photos and CRM from scratch, or bringing them from your last market?"

## S13. New-to-account records

- **Pull:** daily `query_lead_database` or `query_local_business_database` with the ICP filters, `excludeDelivered: true`, `page: 1` or the `after` cursor. Ecommerce Database through REST with the same flag.
- **Meaning:** records the account has never received. Useful as a fresh-contact feed and a dedupe guarantee. It carries no dated event about the prospect.
- **Angle:** none from the flag itself; use the record's fit and any other live signal. Score it low on its own.

## Signals that start outside ScraperCity (S14 to S28)

Website visits, funding rounds, job posts, filings, product launches, events, social engagement, G2 intent and webinar attendance are events ScraperCity tools do not show. They come from a free public feed (EDGAR, a company's job board API, a newsroom page) or from a tool the user pays for. Import the event, set `source = other:<feed or vendor>` on the queue row, and score it with the same formula as S1 to S13. ScraperCity's part starts at the account: finding the buyer, validating the email, finding a mobile, and for S24 pulling the competitor's install base. Three people-change signals (S16, S20, S21) can also be found inside ScraperCity by re-pulling known people or watched accounts from the Lead Database; those rows carry `query_lead_database` as the source.

Vendor and feed facts in this section were checked on each vendor's or publisher's own pages on 2026-10-13. Half-life, max age, base points and touch window are set per signal in the program, as for S1 to S13.

| # | Signal | Detection (pages checked 2026-10-13) | Diff key | Date anchor |
|-|-|-|-|-|
| S14 | Identified person viewed a high-intent page (pricing, demo, comparison, integration docs) | RB2B, Vector, Warmly | Work email or LinkedIn URL + company domain + page group + visit date | Visit timestamp |
| S15 | Company-level visit (account resolved, person unknown) | RB2B company-level ID, Vector IP-to-company fallback | Company domain + ISO week | First visit of the week |
| S16 | Champion or past buyer started at a new company | `query_lead_database` re-pull by `socialUrl` for CRM champions; Sales Navigator saved-lead alerts; UserGems | LinkedIn URL + new company domain | Start date at the new company, else detection date |
| S17 | Funding round announced | Crunchbase (funding rounds, API); the company's own press release | Company domain + round type + announced date | Announcement date |
| S18 | Job post for a role your offer supports or replaces | Greenhouse, Lever and Ashby public job board APIs; the careers page; UserGems | Company domain + normalized job title + posting URL | Posting date, else first-seen pull date |
| S19 | Public social engagement on a topic or competitor post | Octolens, F5Bot (Reddit and Hacker News only), Warmly; Trigify shuts down 2026-10-22 | LinkedIn URL or post URL | Engagement date |
| S20 | New leader at a watched account (VP, head or C-level in the function you sell to) | `query_lead_database` monthly re-pull of watched domains; 8-K Item 5.02 on EDGAR for public companies; Sales Navigator account pages | Person LinkedIn URL + company domain | First-seen pull date, or the filing date |
| S21 | Champion or buyer left a customer account | `query_lead_database` re-pull by `socialUrl` for customer contacts; UserGems "departures from customers" | LinkedIn URL + old company domain | Detection date |
| S22 | Form D filed (private raise, no press needed) | EDGAR full-text search, `forms=D` | CIK + accession number | Filing date |
| S23 | Earnings release or annual or quarterly filing (public company) | EDGAR full-text search for 8-K Item 2.02, 10-K and 10-Q on watched CIKs; the investor relations page for the call | CIK + form + period | Filing date |
| S24 | Competitor change (launch, price change, sunset, acquisition) | Page monitor (changedetection.io) on the competitor's pricing, changelog and status pages; Octolens mentions; press wire feeds. Install base: `scrape_builtwith` for the competitor's technology | Competitor + change URL; then install-base domain | Date the change went live |
| S25 | Target account launched a product, market or location | Page monitor on the account's newsroom or changelog; GlobeNewswire subject feeds; the account's Product Hunt page | Company domain + launch URL | Launch date |
| S26 | Account exhibits, sponsors or speaks at an event | The event's exhibitor, sponsor and agenda pages; your own event's registration list | Company domain + event + role (exhibitor, sponsor, speaker, attendee) | Event start date (age counts from 0 before the event) |
| S27 | Third-party category intent | G2 Buyer Intent (your profile, pricing, category, alternatives, compare and competitor pages) | Company domain + signal type + week | G2 "last seen" date |
| S28 | Webinar or content engagement | Your webinar platform's registrant and attendee export; your marketing automation for gated downloads | Work email + asset + date | Attendance or download date |

In the program's Signal Catalog table, put `other source: <feed or vendor>` in the Tool column for these rows, or `query_lead_database` for a job change or new leader found by a Lead Database re-pull. `scripts/check-output.py` fails a funding, hiring, filing, launch, event, visit or social signal that lacks the label, and a job change or new leader row that has neither the label nor `query_lead_database`.

### Website visitor coverage (S14, S15)

RB2B's FAQ calls its person-level identity "a US-only technology with a US-only database". Vector's FAQ says it is "geofenced to the U.S." and may show only company-level data for EU visitors. Warmly's homepage states no geographic limit; confirm coverage in your contract. Treat S14 as unavailable for non-US traffic (vendor pages, checked 2026-10-13).

Whether the first line should name the visit is untested here. RB2B's own guide for past customers (May 2026) shows sample messages that open with the visit. Split S14 rows between a visit line and a fit-based line and keep the one with more positive replies.

### S14. Identified person viewed a high-intent page

- **Import:** the vendor's push to Slack, a CRM or a webhook into the same n8n workflow as the ScraperCity pulls (RB2B lists Slack, Teams and CRM destinations on its site). Keep page path, timestamp, person and company.
- **Page weights:** the program weights page groups (pricing, demo or trial, comparison, integration docs, case study, product, blog) and drops careers, login and support pages. It sets the weight at which S14 fires for an identified person and the points per week at which S15 fires for a company domain, then checks those settings against meeting rate.
- **Confirm the person:** run `query_lead_database` with `socialUrl` set to the vendor's LinkedIn URL. Same company domain as the visit: confirmed, score as S14. A different company: the profile is stale, so score the visit as S15 for the visiting domain. No record: send email only after `validate_emails` returns `valid`.
- **Enrich with ScraperCity:** `validate_emails` on the vendor's email ($0.0072), `query_lead_database` with `companyDomain` to confirm title and company size (included on Growth), `find_mobiles` with the LinkedIn URL for a tier A call ($0.25 per number found).
- **False positives:** your own staff, candidates reading the careers page, students, competitors researching pricing. Drop company domains on the exclusion list (`references/scoring-and-freshness.md` section 5a) and the careers path before scoring.
- **Angle:** a public fact about the company plus a question, or the visit line if your split test favors it. "Saw Ledgerline opened a Denver office in August. Who owns lead routing for the new team?"
- **Vendor pilot:** log identified visitors per 1,000 sessions, the share that pass fit, a hand check of a sample of matches against LinkedIn (right person, right company), cost per fit-passing identification and meetings booked. Keep the vendor when its cost per meeting is at or under your static-list cost per meeting.

### S15. Company-level visit

- **Detect:** one company domain reaches the program's weekly page-weight threshold (S14).
- **Enrich:** `query_lead_database` with `companyDomain` and the buyer `title`, `limit: 10`; `scrape_website_finder` with `domains` and `jobTitle` when the database has no one in the role ($0.0499 per contact found).
- **Angle:** the same fit-based first line as an account with no visit; the visit raises priority.

### S16. Champion or past buyer started at a new company

- **Detect inside ScraperCity:** every quarter, run `query_lead_database` with `socialUrl` for each CRM contact marked customer, champion or closed-won, and compare the returned `company_domain` with the CRM company. A difference is a job change (the `crm-enricher` skill flags it `JOB_CHANGE`). The database refresh schedule is not published, so test it first: take people you know moved recently and count how many the Lead Database shows at the new company. If it misses most of them, use Sales Navigator saved-lead alerts (LinkedIn's page says saved leads trigger alerts when they change jobs) or a vendor feed for S16.
- **Detect from a vendor:** the job-change feed for the same CRM contacts.
- **Qualify:** the new company passes fit and the exclusion list. Seniority sets the channel: VP and above get a personal note from the rep who knew them plus a call; managers and individual contributors go to the S16 campaign.
- **Enrich:** `find_emails` with first name, last name and the new domain ($0.05 per email found), then `validate_emails`.
- **Timing:** UserGems' signals page says new executives re-evaluate the stack within their first 90 days (vendor claim), so an S20 row, or an S16 row where the person moved into a leadership seat, stays live for 90 days from the start date. Split a batch between an early and a later first touch inside that window and keep the better day.
- **CRM:** create the contact at the new company with `source = job_change`, mark the old contact as left, and raise S21 on the old account if it is a customer.
- **Angle:** the person announced the new job in public, so naming it is fine. Bridge from what they did with you before: "Congrats on the new role at Fernway. Are you rebuilding the email program there, or inheriting one?"

### S17. Funding round announced

- **Detect:** a round dated within the max age at a company in the ICP universe. Match on domain; a company name alone is too loose.
- **Stack:** a funding row scores higher when a second signal is live on the account, such as an S18 post on the team you serve or an S20 leader hire in your buyer's function.
- **Enrich:** `query_lead_database` with `companyDomain` and titles for the budget owner: the CEO at a small company, otherwise the leader of the function the round is for.
- **False positives:** debt facilities and grants listed as rounds, announcements months after the close. Use the announced date. Save "this week" for announcements under 7 days old; otherwise say "recent round".
- **Angle:** what the round could fund in your category, asked as a question so you do not assert their plan. Name the use of funds from their own announcement when it gives one. "Saw the Series A news. Is outbound hiring part of the plan for the next two quarters?"

### S18. Job post for a role your offer supports or replaces

- **Detect:** pull the company's public job board on a schedule and diff it. Greenhouse: `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs`, no authentication for GET; the list carries `updated_at`, and the single-job call carries `first_published`. Ashby: `GET https://api.ashbyhq.com/posting-api/job-board/{JOB_BOARD_NAME}` with `publishedAt` per job. Lever: `GET https://api.lever.co/v0/postings/{site}`; its docs list no date field, so date the post by first sight. The token or site name is the last part of the careers URL (boards.greenhouse.io/..., jobs.ashbyhq.com/..., jobs.lever.co/...).
- **Read the role:**

| Role pattern | What it tells you | Contact |
|-|-|-|
| A leader for the function you sell to (VP, head) | A new owner arrives within months and sets the stack | CEO or hiring manager now; the new leader as S20 once hired |
| A builder role (operations, enablement, admin of the system you replace) | Process and tooling get rebuilt | The function leader |
| Several open roles of one title | Capacity strain on that team | The team's manager |
| A title reposted after it closed | Backfill or churn in the seat | The function leader, with a retention or ramp angle |

- **Backfill check:** run `query_lead_database` with `companyDomain` and the posted `title`. Someone already holds that title at the domain: treat the post as a backfill or an added seat, not a first hire, and drop the "new function" angle.
- **Re-check:** the post must still be open at scoring time. Re-load the URL before a tier A touch; a closed post drops to 0 strength.
- **Enrich:** `query_lead_database` with `companyDomain` and the hiring manager's title.
- **Angle:** the work the hire will do in the first 90 days, quoted from the job description. "Saw you're hiring two SDRs in Austin. Who builds their lists before they start?"

### S19. Public social engagement

Trigify announced on its own site that its team is joining HubSpot and that the standalone platform, integrations and API stop at 11:59pm BST on 22 October 2026, with no account migration. Export saved searches and engagement history before that date, and build S19 on a different tool.

| Tool (checked 2026-10-13) | Sources | Delivery | Price shown |
|-|-|-|-|
| Octolens | 15 sources including LinkedIn, X, Reddit, Hacker News, GitHub, YouTube, newsletters and reviews | Slack, email, webhooks, API, MCP server | Pro $159 a month billed annually (15,000 mentions, 10 keywords); 7-day trial |
| F5Bot | Reddit, Hacker News, Lobsters | Email on the free plan; Slack and JSON feeds on Gold | Free; Silver $9.99 and Gold $49.99 a month |
| Warmly | Lists social activity among its signals | Its own workflows | Quote |

- **Keywords:** phrases, never single words. Competitor name plus a pain or switch word ("alternative to", "price increase", "cancel"), recommendation requests in your category ("recommend a tool for", "what do you use for"), and the problem in buyer words. Add negative keywords for job posts, giveaways and your own brand. Drop any keyword whose alerts rarely land on a person at a fit account; the program sets the share it keeps.
- **Detect:** a comment or reaction on a post about the problem you solve, or on a competitor's post, by a person at an ICP account. Urgency by engagement type: `references/repeat-pull-recipes.md` section 8.
- **Enrich:** `query_lead_database` with `socialUrl` set to the person's LinkedIn URL (included on Growth), then `validate_emails`.
- **Angle:** the topic of the post. A person's own public post can be named; a reaction on someone else's post should not be, because the reply becomes about how you saw it.

### S20. New leader at a watched account

- **Detect inside ScraperCity:** once a month, run `query_lead_database` on the watched domains (`companyDomain` takes several, comma separated) with `seniority: ["vp", "c_suite"]` or the leader `title`, and the `department` you sell to. A LinkedIn URL that was not in last month's result for that domain, with a leader title, is S20. Run the same refresh test as S16 before trusting it.
- **Public companies:** EDGAR full-text search with `ciks` and `forms=8-K`; an 8-K whose `items` include `5.02` covers departures and appointments of certain officers (investor.gov lists Item 5.02 by that name). Filed within four business days of the event.
- **Other sources:** Sales Navigator account pages show decision makers who joined or left a saved account.
- **Angle:** the first 90 days. UserGems' signals page says new executives re-evaluate the stack within their first 90 days (vendor claim). "Saw you joined Corvane as VP Revenue in September. What are you keeping from the current outbound setup, and what are you replacing?"

### S21. Champion or buyer left a customer account

- **Detect:** the S16 re-pull run on customer contacts, or a vendor's departures feed.
- **Route:** this row goes to the account owner, not to an outbound campaign (customers sit on the exclusion list).
- **Find the replacement:** `query_lead_database` with the customer's `companyDomain` and the departed person's `title` or `department` plus `seniority`. Then `validate_emails`.
- **Touch:** the account owner writes to the replacement with what the account has done with you so far (usage, results, open items) and offers a 20-minute handover.

### S22. Form D filed

- **Detect:** EDGAR full-text search returns JSON with no key: `https://efts.sec.gov/LATEST/search-index?forms=D&dateRange=custom&startdt=2026-10-05&enddt=2026-10-11&locationCodes=TX`. Each hit's `_source` carries `display_names`, `file_date`, `biz_states`, `biz_locations`, `ciks` and `adsh`. Send a User-Agent with your company name and a contact email, and stay at or under 10 requests a second (SEC webmaster FAQ). The form is due within 15 days after the first sale in the offering, so it can show a raise that has no press release yet. Volume is high and mostly funds: a national query for 2026-10-01 to 2026-10-09 returned 2,054 Form D filings, and the first page was angel fund series. Always filter by state and drop funds before matching. The API returns 100 hits per call; page with `&from=100`, `&from=200` and so on.
- **Drop:** names that read as funds, series, SPVs or single-property LLCs. Then open the filing and read Item 4 (Industry Group: drop pooled investment funds and real estate), Item 7 (Type of Filing: an amendment is not a new raise), Item 13 (Offering and Sales Amounts) and Item 3 (Related Persons: the executives and directors by name).
- **Match to a domain:** Form D has no website field. Run `query_lead_database` with `companyName` and `companyState`, and confirm the domain by hand for tier A rows. Related Persons names go to `find_emails` with that domain.
- **Angle:** the stage, without citing the filing, since the company may not have announced. "Are you adding sales headcount at Brightline this half, or building pipeline for the team you have first?"

### S23. Earnings release or annual or quarterly filing

- **Detect:** EDGAR full-text search with `ciks` set to the watched companies and `forms=8-K,10-K,10-Q`. An 8-K whose `items` include `2.02` (Results of Operations and Financial Condition) is the earnings release; the call is on the investor relations page the same day or the next.
- **Read, in this order:** Item 1A Risk Factors (investor.gov describes them as generally ordered by importance), Item 7 MD&A (management's view of results and changes), then the analyst questions on the call. A topic two or more analysts asked about is under pressure.
- **Plan against actual:** put the priorities in the 10-K's Item 7 next to the latest 10-Q's MD&A. A priority that slipped a quarter, or a cost line that grew faster than revenue, is a problem in progress, which beats a risk listed in the abstract.
- **Extract with a model, then check:** paste Item 1A and Item 7 into a model and ask for every sentence that names a priority, an investment, a headcount plan or a risk touching your category, quoted word for word with its item number. Open the filing and confirm each quote word for word before it goes in an email, because models sometimes return a paraphrase inside quotation marks.
- **Who:** the executive who owns the initiative the filing names, found with `query_lead_database` (`companyDomain`, `title`). Directors get the operational version of the same point.
- **Private accounts:** read the filings of their two largest public competitors for industry pressure, and never present those facts as the private company's own.
- **Angle:** management's own phrase, with where it came from. "Your Q3 MD&A said the priority is lowering cost to serve in the mid-market segment. Is self-serve onboarding part of that plan, or is it all headcount?"

### S24. Competitor change

- **Detect:** a page monitor on each competitor's pricing page, changelog, status page and end-of-life docs. changedetection.io is open source (Apache-2.0), self-hosts with Docker, and sends to Slack, email or a webhook. Add the competitor's name plus "price increase", "sunset", "acquired" to your mention monitor (S19 tools), and a press wire feed for mergers and acquisitions.
- **Build the install base:** one Tech Stack Search run (`scrape_builtwith`, $4.99) for the competitor's technology returns every domain detected using it. Intersect with your ICP universe and the exclusion list. These domains carry S24 with the change date as the anchor.
- **Open deals:** the account owner sends the champion a three-line note the same day: what changed, what it means for their project, one question. Product marketing updates the comparison talk track.
- **Angle:** neutral and specific; ask, do not attack. "Saw Relaywise moved its API to the Enterprise tier on October 1. Is that changing your plan for the integration work this quarter?"

### S25. Target account launched a product, market or location

- **Detect:** a page monitor on the account's newsroom, blog feed or changelog; GlobeNewswire offers RSS by industry and subject (no keyword or company feeds), so filter titles for watched names in n8n. Product Hunt's API needs a token and its docs restrict commercial use without permission, so check a watched account's Product Hunt page by hand.
- **Who:** the launch owner (product marketing, product, or the new market's general manager) via `query_lead_database` with `companyDomain` and `title`.
- **Angle:** the work the launch creates for your function. "Saw Brightline launched the payroll add-on on October 6. Who is building the onboarding emails for the first 1,000 customers?"

### S26. Account exhibits, sponsors or speaks at an event

- **Detect:** copy the exhibitor, sponsor and speaker lists from the event's pages into a sheet (company, role, booth or session) as soon as they are published. For your own event, the registration list. Map names to domains, then run `query_lead_database` with `companyDomain` (several at once) and the buyer `title`; `scrape_website_finder` for domains with no match.
- **Timing:** age counts from 0 before the event. Pre-event emails to attendees and speakers ask for a named time and place at the show; exhibitors get the post-show ask below. Post-event emails go first to people you met, then to exhibitors you did not meet. The program sets the pre-event start date and the post-event max age.
- **Angle by role:** exhibitor: how the booth conversations will turn into pipeline; speaker: one question about their talk; attendee you met: the conversation; not attending: a theme from the agenda.
- **Exhibitors are working:** booth staff are selling to their own prospects, and shows such as NAMM bar non-exhibitors from soliciting exhibitors in aisles or booths (NAMM Show suitcasing policy, checked 2026-10-13). When the exhibitor's sales team is your buyer, the pre-event email goes to the sales leader not on booth duty and asks for a meeting in the week after the show; a visit to the booth is offered as an optional drop-by.
- **Return per event:** cost per meeting = (event cost + travel + outreach spend) / meetings held. Compare it with the cost per meeting of your static-list campaigns before booking next year's booth.

### S27. Third-party category intent

- **Detect:** G2 Buyer Intent reports company-level activity when a buyer views your G2 profile, pricing, category, alternatives or compare pages, or a competitor's pricing, profile or compare page in a shared category (`competitive/` signals in the Detail CSV). Each company carries a buying stage (Awareness, Consideration, Decision), an activity level updated daily, headquarters, last seen date and the products compared. Delivery: CSV export (one row per company or per signal), scheduled email alerts to up to 20 addresses, and integrations. Which signals arrive depends on your G2 plan (G2 documentation, checked 2026-10-13).
- **Score:** weight compare, alternatives and competitive signals above category views; the program sets the points. G2 names no person, so S27 scores at the account and the contact comes from the Lead Database by domain and buyer title.
- **Angle:** never mention G2 or the research. Use a fit fact or another live signal; the intent only raises priority, as with S15.

### S28. Webinar or content engagement

- **Detect:** your webinar platform's registrant and attendee export and your marketing automation's form fills, pulled daily or pushed by webhook into the same workflow. Attended, registered and did not attend, and downloaded are three separate rows with their own points.
- **Who:** the person who engaged if the title fits; otherwise the buyer at that domain, as for a visitor below the buyer (S14).
- **Angle:** the topic of the session or asset, named, because the person gave you their email for it. One question about the problem the session covered.

## Negative signals

Events that make a near-term purchase less likely. Each one subtracts points from the score and pauses outreach to the account for a number of days; the program sets both and re-fits them like base points. Every Scoring Model carries at least one negative row.

| Negative signal | Detection | Effect to set in the program |
|-|-|-|
| Layoffs in the last quarter | layoffs.fyi (tracks tech startup layoffs, free with attribution), press, the company's own announcement | Minus points; pause days |
| Hiring freeze in the buyer's team | The S18 job board diff: every posting for the team closed and none reopened since the program's look-back | Minus points; pause days; S17 and S18 on the account stop scoring |
| Competitor just signed | The competitor's press release or case study naming the account; a job post that lists the competitor as a new tool | Minus points; pause until the renewal window the program sets |
| Sponsor left | The champion or buyer left the account (S21 at a prospect) | Minus points until the replacement is found |
| Store or site traffic fell out of the ICP band | The monthly universe pull | Minus points; pause until the next pull |

## Sources

- https://www.insidesales.com/leveraging-trigger-events/
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://scrapercity.com/llm-info
- https://www.npmjs.com/package/scrapercity
- https://www.rb2b.com/
- https://www.vector.co/websiteid
- https://learn.vector.co/articles/5062232408-faq-help-center
- https://www.warmly.ai/
- https://www.usergems.com/
- https://www.crunchbase.com/
- https://www.trigify.io/
- https://octolens.com/
- https://f5bot.com/
- https://developers.greenhouse.io/job-board.html
- https://developers.ashbyhq.com/docs/public-job-posting-api
- https://github.com/lever/postings-api
- https://www.usergems.com/product/signals
- https://business.linkedin.com/sales-solutions/sales-navigator/how-to-use-linkedin-sales-navigator
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://www.sec.gov/about/webmaster-frequently-asked-questions
- https://www.sec.gov/resources-small-businesses/exempt-offerings/filing-form-d-notice
- https://www.sec.gov/files/formd.pdf
- https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read-8
- https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/how-read
- https://github.com/dgtlmoon/changedetection.io
- https://www.globenewswire.com/rss/list
- https://api.producthunt.com/v2/docs
- https://www.rb2b.com/learn/how-to-re-engage-past-customers-who-visit-your-website-again
- https://documentation.g2.com/docs/buyer-intent
- https://www.namm.org/thenammshow/info/SuitcasingUnauthorizedSolicitation
- https://layoffs.fyi/
