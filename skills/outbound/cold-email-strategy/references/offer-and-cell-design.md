# Offer and Cell Design

Worksheets for the offer sentence and the contact thesis, plus ScraperCity filter recipes for the cell types this repo sees most. Every recipe uses parameters from `references/scrapercity-catalog.md` and the database schemas in `references/scrapercity-platform.md`.

## 1. Offer worksheet

Alex Berman's offer article: build from a measured client outcome, pick the most dramatic repeatable result, state it as one sentence with a niche, a result and a mechanism, then build the list.

| Field | Question | Bad | Good |
|-|-|-|-|
| Niche | Who exactly had the result? | "Businesses" | "3 to 6 chair dental practices in Texas suburbs" |
| Result | What number changed, from what to what? | "More patients" | "New patient form fills from 9 to 26 a month" |
| Timeframe | How long did it take? | "Fast" | "60 days" |
| Mechanism | What did you do, in five words? | "Our proven system" | "Review requests sent by text after each visit" |
| Proof source | Client, date, metric owner | "Trust us" | "Round Rock practice, March 2026, their booking software export" |
| Current alternative | What does the buyer do about this today? (April Dunford starts positioning here: the alternative, not your product) | "Nothing" | "Front desk asks happy patients in person, about 2 reviews a month" |
| Pain in their words | How did 3 won customers describe the problem before buying? (call notes, reviews, emails) | "Reputation management challenges" | "Patients love us but can't find us on Google" |
| Objection pre-answered | Why would a good-fit buyer ignore this? Answer it inside the offer | (left out) | "Too busy to set up" answered by "we load your patient list for you in one call" |
| Ask | What is the smallest next step? | "Book a 45 minute demo" | "Want the template we used?" or "Open to 10 minutes?" |

Offer sentence: "We help [niche] get [result] in [timeframe] by [mechanism]."

The mechanism has to beat the current alternative in a way the reader can picture. "We already have someone for that" in replies means the market buys (Berman, Lean B2B interview); sharpen the mechanism against that alternative instead of changing the segment.

### Offer strength score

Score each line 0 or 1. Each line scored 0 is a fix to make before launch.

| Check | 1 point when |
|-|-|
| Number | The result has a number and a unit |
| Same niche | The proof client matches the cell's business type |
| Time | A timeframe is stated |
| Mechanism | A reader can picture what you did |
| Low ask | The ask is a short call or a resource |
| Risk | Something lowers risk: a free sample, a pilot, a result-based fee |

### Offer types by what you have

| What you have | Offer type | Example ask |
|-|-|-|
| A measured client result in the same niche | Case-study offer | "Want to see what we changed?" |
| A result in an adjacent niche | Borrowed proof plus diagnostic | "Should I run the same check on your store?" |
| No clients yet, or no measured result in this niche | Free work or audit offer (Berman describes free work as a way to build a first case study): a scoped review that returns a few written findings | "Can I send a 2 minute video audit of your booking page?" / "Want me to look at last month's P&L and send back what I'd fix?" |
| A data asset | Sample offer | "Want 25 sample leads for your territory?" |
| Partnership with a known brand | Borrowed credibility (Berman suggests borrowing case studies through partners) | "We built this with [partner] for [client]; want to see it?" |

Never invent a result, a client, a partner or a percentage. If you have no measured proof, use the audit or sample offer.

## 2. Contact thesis worksheet

Template: "[Buyer title] at [segment] will reply because [observable fact or trigger, with field name] makes [problem] costly now, and [proof] shows we fix it. Falsified if [threshold]."

| Part | Must be | Example |
|-|-|-|
| Buyer title | One title or a tight title family | Practice owner or office manager |
| Segment | Reproducible with filters | Dentists, Texas, 20 to 150 reviews, has website |
| Observable fact | A field in the list | `reviews_count` under 60 while top 3 local competitors exceed 150 |
| Problem | What the fact costs | New patients pick the practice with more reviews |
| Proof | Measured client result | Round Rock practice went from 41 to 160 reviews in 5 months |
| Falsifier | A number that ends the cell | Under the break-even positive rate once the read size is delivered |

### Trigger freshness windows

Elias's window of dissatisfaction closes, and he gives no length in days. Record the date each trigger was observed, set each window in the plan as a stated assumption, and compare reply rates by trigger age at the first read.

| Trigger | Source | Freshness check |
|-|-|-|
| New app or platform on a store | `scrape_store_leads` with `apps` or `platform` | Detected between two pulls; the window the plan sets |
| Technology in use (stable) | `scrape_builtwith` | No expiry; treat as a fit criterion |
| Few reviews for a category | `query_local_business_database` with `maxReviews` | Recheck each pull |
| Low rating | `maxRating` | Recheck each pull |
| Distressed property | `scrape_distress_list` | Recheck each pull |
| Business listed for sale | `scrape_bizbuysell` | While listed |
| Hiring for a role you support | Outside ScraperCity (job boards, careers pages) | The window the plan sets from the posting date, and still live when re-opened before touch 1 (section 7) |

## 3. Filter recipes by cell type

### A. Local services owner (Local Business Database, Growth plan)

```json
{
  "tool": "query_local_business_database",
  "category": ["Dentist"],
  "state": "TX",
  "location": ["Houston TX", "Austin TX", "San Antonio TX", "Dallas TX"],
  "minReviews": 20,
  "maxReviews": 150,
  "hasWebsite": true,
  "hasEmail": true,
  "excludeDelivered": true,
  "limit": 100,
  "after": "0"
}
```

Returned fields to carry into copy: `title` (business name), `category_name`, `city`, `total_score`, `reviews_count`, `website`, `contact_first_name`, `contact_job_title`, `contact_email`. Add `hasContact: true` to keep only businesses with a named contact.

Split into rating cells: `minRating: 4.6` for a praise angle (3C framework), `maxRating: 4.0` for a fix angle (problem-first).

### B. Local services, fresh pull (Google Maps)

```json
{
  "tool": "scrape_maps",
  "searchStringsArray": ["roofing contractor"],
  "locationQuery": "Phoenix, AZ",
  "maxCrawledPlacesPerSearch": 500
}
```

$0.0099 per business. 500 businesses = $4.95. Use when the database count for the category and city is thin or you need today's listings.

### C. B2B title by company size (Lead Database, Growth plan)

```json
{
  "tool": "query_lead_database",
  "title": "VP Sales, Head of Sales, Director of Sales",
  "seniority": ["vp", "director"],
  "industry": ["computer software"],
  "country": ["United States"],
  "minEmployees": 50,
  "maxEmployees": 200,
  "hasEmail": true,
  "notTitle": "assistant, intern",
  "excludeDelivered": true,
  "limit": 100,
  "after": "0"
}
```

Fields for copy: `title`, `company_size`, `employees_count`, `company_industry`, `company_annual_revenue`, `company_city`, `keywords`. If the call returns 503, narrow it (add a state, cut a title) and retry.

### D. Ecommerce by platform and app (Store Leads)

```json
{
  "tool": "scrape_store_leads",
  "platform": "shopify",
  "apps": "Klaviyo",
  "category": "apparel",
  "countryCode": "US",
  "minEstimatedMonthlyVisits": 20000,
  "maxEstimatedMonthlyVisits": 200000,
  "emails": true,
  "planExclude": ["Shopify Plus"],
  "totalLeads": 1000,
  "offset": 0
}
```

$0.0039 per lead. 1,000 leads = $3.90. Page with `offset` 0, 1000, 2000 or the returned `nextOffset`.

### E. Technology users (Tech Stack Search, then people)

1. `scrape_builtwith` with `technology: "Magento"`: $4.99 for the technology, returns a domain list.
2. `scrape_website_finder` with `domains` from step 1, `jobTitle: "Founder"`, `autoValidateEmails: true`: $0.0499 per contact found.

For 800 domains at a 45% find rate (assumed for this example): 360 contacts x $0.0499 = $17.96, plus $4.99 = $22.95.

### F. Apollo.io saved search (when the user already has one)

`scrape_apollo` with the Filters 1.0 `url` and `count` between 500 and 50,000. $0.0039 per lead: 5,000 leads = $19.50. Runs usually take 15 to 30 minutes; register a webhook at app.scrapercity.com/dashboard/webhooks or poll every few minutes.

## 4. Enrichment and validation cost per 1,000 contacts

| Step | Tool | Rate | Cost per 1,000 |
|-|-|-|-|
| Find missing emails (50% found, assumed for this example) | `find_emails` | $0.05 per email found | $25.00 |
| Validate every address | `validate_emails` | $0.00169 per email | $1.69 |
| Mobile numbers for phone touches (30% found, assumed for this example) | `find_mobiles` | $0.25 per number found | $75.00 |

Find rates vary by segment; replace these example rates with the measured rate from your first run. They make no claim about ScraperCity accuracy. Email Finder and Mobile Finder charge only when they find something.

## 5. Cell card (copy into the plan)

| Field | Value |
|-|-|
| Cell id | A |
| Segment filters | (tool + parameters) |
| Exclusions | Customers, open deals, prior unsubscribes, excluded regions |
| Buyer title | |
| Offer sentence | |
| Trigger and freshness | |
| Proof line | |
| Framework | 3C / problem-first / PAS / trigger / three-sentence |
| Count (from `limit: 1`) | |
| Validated estimate | |
| Cost | |

## 6. First-line templates by trigger

A trigger is only usable when the first line can state it as a fact from a dated column. Most "new" and "change" triggers need two pulls of the same filters a few weeks apart: the trigger is the difference. Keep both pull dates in the sheet. Tags are shown without fallbacks; add one per tag in `cold-email-copywriting`.

Set each row's window in the plan from the observed date (section 2).

| Trigger | Source | ScraperCity? | How to detect | First-line template |
|-|-|-|-|-|
| New local listing | `query_local_business_database` or `scrape_maps` ($0.0099 per business) | Yes | Business present in this month's pull and absent last month; a very low `reviews_count` supports it | Saw {{business_name}} is new on Google Maps in {{city}}. |
| Review change | Same pull repeated; `scrape_yelp` ($0.0099 per result) for Yelp | Yes | `reviews_count` or `total_score` differs from the prior pull | {{business_name}} added {{review_delta}} Google reviews since {{prior_month}}. |
| New technology | `scrape_builtwith` ($4.99 per technology) | Yes | Domain in this month's list and not last month's | Saw {{company_name}} added {{technology}} to the site. |
| Store platform or app change | `scrape_store_leads` with `platform` or `apps` ($0.0039 per lead) | Yes | Store appears under the new platform or app filter versus the prior pull | Noticed {{store_name}} moved to {{platform}}. / Saw {{store_name}} added {{app}}. |
| Business for sale | `scrape_bizbuysell` with a search `startUrls` ($0.0099 per listing) | Yes | Listing present; write to the broker contact on the listing | Saw the {{category}} listing in {{city}} you are representing. |
| Pre-foreclosure | `scrape_distress_list` with `distressTypes: ["preForeclosure"]` ($0.05 per property) | Yes | Distress type on the property record; owner via `find_people` | {{street_address}} came up in our search for {{city}} homes we would buy as-is. |
| Leadership or job change | LinkedIn, press releases, a job-change alert tool | No | Start date in the new role | Congrats on the move to {{title}} at {{company_name}}. |
| Hiring | Company careers page, job boards | No | Open role posted for the function you serve | Saw {{company_name}} is hiring {{open_roles}} {{role}} roles. |
| Funding | Company press release, SEC Form D filings, funding databases | No | Announcement date | Congrats on the {{round}} in {{funding_month}}. |

Rules for these lines:

- Business-for-sale listings are often anonymous. Write to the broker named on the listing.
- Rating drops get neutral wording: state the current rating, never "your rating fell".
- State the fact and stop. A fit field never becomes evidence of a problem: "{{review_count}} reviews says {{practice_name}} is busy, so the books run behind" guesses at a cause the row cannot show, reads as mail-merge, and gets cut. A fit-only row opens with the problem in won customers' words (section 1, pain line) or a dated trigger from this table.
- A trigger from a non-ScraperCity source needs its URL and date in a column, so the line can be checked before it sends.
- Change triggers are only as fresh as the time between pulls, so the pull interval has to be shorter than the window the plan sets.

## 7. Job postings as a trigger

ScraperCity does not supply job postings. Collect them from the company's careers page or a job board, and treat them as a dated trigger column next to the ScraperCity row.

| Step | Rule |
|-|-|
| Pick roles | Only roles your offer helps with: a "Dental Front Desk Coordinator" opening for a scheduling or review tool; an "Email Marketing Manager" opening for a retention agency |
| Store | Columns `job_title`, `job_url`, `job_posted_date`, `job_checked_date`. A row missing the URL or the date gets the fit-only line |
| Freshness | Inside the window the plan sets, counted from `job_posted_date` to the send date. Re-open the URL before touch 1; a closed posting drops the trigger line |
| Fallback | A dropped trigger sends the cell's fit-only first line; the contact stays in the cell |
| First line | State the role and leave the reason out: "Saw {{company_name}} is hiring a {{job_title}}." A line like "Saw you are struggling to keep staff" guesses at motive and gets cut |
| Counting | Each posting triggers once. A repost of the same role inside the window is the same trigger |
| Join key | Company domain from the posting URL or the careers page, matched to `company_domain` or `website` in the ScraperCity row |

A job posting names the company, not the buyer. Find the buyer with the cell's normal source (`query_lead_database` by title and domain, or `find_emails` for a named owner), then validate.

## Sources

- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://stfo.io/podcast/april-dunford-product-positioning (April Dunford, episode 82, June 3, 2019: step one is the competitive alternatives)
- https://alexberman.com/cold-email-fewer-sends-higher-reply-rates
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.insidesales.com/leveraging-trigger-events/
- https://scrapercity.com/pricing
- https://www.npmjs.com/package/scrapercity
- https://www.sec.gov/resources-small-businesses/exempt-offerings/filing-form-d-notice
