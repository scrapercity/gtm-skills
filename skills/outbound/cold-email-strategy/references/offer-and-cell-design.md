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
| Ask | What is the smallest next step? | "Book a 45 minute demo" | "Want the template we used?" or "Worth 10 minutes?" |

Offer sentence: "We help [niche] get [result] in [timeframe] by [mechanism]."

### Offer strength score

Score each line 0 or 1. Ship at 5 or 6. Rework under 5.

| Check | 1 point when |
|-|-|
| Number | The result has a number and a unit |
| Same niche | The proof client matches the cell's business type |
| Time | A timeframe is stated |
| Mechanism | A reader can picture what you did |
| Low ask | The ask takes under 15 minutes or is a resource |
| Risk | Something lowers risk: a free sample, a pilot, a result-based fee |

### Offer types by what you have

| What you have | Offer type | Example ask |
|-|-|-|
| A measured client result in the same niche | Case-study offer | "Want to see what we changed?" |
| A result in an adjacent niche | Borrowed proof plus diagnostic | "Should I run the same check on your store?" |
| No clients yet | Free work or audit offer (Berman describes free work as a way to build a first case study) | "Can I send a 2 minute video audit of your booking page?" |
| A data asset | Sample offer | "Want 25 sample leads for your territory?" |
| Partnership with a known brand | Borrowed credibility (Berman suggests borrowing case studies through partners) | "We built this with [partner] for [client]; worth a look?" |

Never invent a result, a client, a partner or a percentage. If the proof is not real, use the audit or sample offer.

## 2. Contact thesis worksheet

Template: "[Buyer title] at [segment] will reply because [observable fact or trigger, with field name] makes [problem] costly now, and [proof] shows we fix it. Falsified if [threshold]."

| Part | Must be | Example |
|-|-|-|
| Buyer title | One title or a tight title family | Practice owner or office manager |
| Segment | Reproducible with filters | Dentists, Texas, 20 to 150 reviews, has website |
| Observable fact | A field in the list, not a guess | `reviews_count` under 60 while top 3 local competitors exceed 150 |
| Problem | What the fact costs | New patients pick the practice with more reviews |
| Proof | Real client result | Round Rock practice went from 41 to 160 reviews in 5 months |
| Falsifier | A number that ends the cell | Under 0.5 positive replies per 100 delivered after 300 delivered |

### Trigger freshness windows

Elias's window of dissatisfaction closes. Use these as defaults and record the date each trigger was observed.

| Trigger | Source | Use within |
|-|-|-|
| New app or platform on a store | `scrape_store_leads` with `apps` or `platform` | 90 days of detection |
| Technology in use (stable) | `scrape_builtwith` | No expiry; treat as fit, not trigger |
| Few reviews for a category | `query_local_business_database` with `maxReviews` | Recheck each pull |
| Low rating | `maxRating` | Recheck each pull |
| Distressed property | `scrape_distress_list` | 30 days |
| Business listed for sale | `scrape_bizbuysell` | While listed |
| Hiring for a role you support | Outside ScraperCity (job boards) | 30 days |

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

For 800 domains with an assumed 45% find rate: 360 contacts x $0.0499 = $17.96, plus $4.99 = $22.95.

### F. Apollo.io saved search (when the user already has one)

`scrape_apollo` with the Filters 1.0 `url` and `count` between 500 and 50,000. $0.0039 per lead: 5,000 leads = $19.50. Runs take hours to several days; register a webhook at app.scrapercity.com/dashboard/webhooks or poll at most hourly.

## 4. Enrichment and validation cost per 1,000 contacts

| Step | Tool | Rate | Cost per 1,000 |
|-|-|-|-|
| Find missing emails (assume 50% found) | `find_emails` | $0.05 per email found | $25.00 |
| Validate every address | `validate_emails` | $0.0072 per email | $7.20 |
| Mobile numbers for phone touches (assume 30% found) | `find_mobiles` | $0.25 per number found | $75.00 |

Find rates vary by segment; these are planning assumptions, not ScraperCity accuracy claims. Email Finder and Mobile Finder charge only when they find something.

## 5. Cell card (copy into the plan)

| Field | Value |
|-|-|
| Cell id | A |
| Segment filters | (tool + parameters) |
| Exclusions | Customers, open deals, prior unsubscribes, Canada |
| Buyer title | |
| Offer sentence | |
| Trigger and freshness | |
| Proof line | |
| Framework | 3C / problem-first / PAS / trigger / three-sentence |
| Count (from `limit: 1`) | |
| Validated estimate | |
| Cost | |

## Sources

- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://alexberman.com/cold-email-fewer-sends-higher-reply-rates
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.insidesales.com/leveraging-trigger-events/
- https://scrapercity.com/pricing
- https://www.npmjs.com/package/scrapercity
