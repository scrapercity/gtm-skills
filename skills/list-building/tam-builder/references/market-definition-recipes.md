# Market Definition Recipes

24 markets, each with a one-sentence definition, the NAICS code for the Census benchmark, and starting filters for each ScraperCity source. Change the geography and size words to fit the user. Every database body below is a count call (`limit: 1`); switch to `limit: 100` with `after` to pull.

## How to read a recipe

- **Local DB** is `query_local_business_database`. `keyword` and `location` work the way a Google Maps search does; `category` matches category labels and a word also finds categories containing it.
- **Lead DB** is `query_lead_database` with one leader title per company, used as a company proxy.
- **Maps** is `scrape_maps`. Use the same keywords as `searchStringsArray`.
- **Other** names Yelp (`scrape_yelp`), Angi (`scrape_angi`, slug from the catalog list), Store Leads (`scrape_store_leads`) or Tech Stack Search (`scrape_builtwith`).
- NAICS codes are 2022 NAICS. A code is a benchmark only; it rarely matches the sales market exactly.

## Home and building services

### 1. HVAC contractors

- Definition: residential and light commercial heating and air conditioning contractors, excluding supply houses and manufacturers.
- NAICS: 238220 Plumbing, Heating, and Air-Conditioning Contractors.
- Local DB: `{"keyword": ["hvac contractor", "air conditioning contractor", "heating contractor"], "location": ["Texas"], "notCategory": ["HVAC supply store", "Appliance store"], "limit": 1}`
- Lead DB: `{"title": "Owner, President, CEO, Founder, General Manager", "keywords": ["hvac"], "companyState": ["Texas"], "limit": 1}`
- Other: `scrape_angi` with `keyword: "hvac"` and `zipCodes` for gap ZIPs.

### 2. Plumbers

- Definition: plumbing contractors serving homes and small commercial buildings.
- NAICS: 238220.
- Local DB: `{"keyword": ["plumber", "plumbing contractor", "drain cleaning"], "location": ["Florida"], "notCategory": ["Plumbing supply store"], "limit": 1}`
- Other: `scrape_angi` with `keyword: "plumbing"`.

### 3. Roofing contractors

- Definition: residential and commercial roofing installers and repairers.
- NAICS: 238160 Roofing Contractors.
- Local DB: `{"keyword": ["roofing contractor", "roofer", "roof repair"], "location": ["Georgia"], "notCategory": ["Roofing supply store"], "limit": 1}`
- Other: `scrape_angi` with `keyword: "roofing"`.

### 4. Electricians

- NAICS: 238210 Electrical Contractors and Other Wiring Installation Contractors.
- Local DB: `{"keyword": ["electrician", "electrical contractor"], "location": ["Arizona"], "notCategory": ["Electrical supply store", "Lighting store"], "limit": 1}`
- Other: `scrape_angi` with `keyword: "electrical"`.

### 5. Landscaping and lawn care

- NAICS: 561730 Landscaping Services.
- Local DB: `{"keyword": ["landscaper", "landscaping", "lawn care service"], "location": ["North Carolina"], "notCategory": ["Garden center", "Plant nursery"], "limit": 1}`
- Other: `scrape_angi` with `keyword: "landscaping"` or `"lawn-and-yard-work"`.

### 6. Pest control

- NAICS: 561710 Exterminating and Pest Control Services.
- Local DB: `{"keyword": ["pest control service", "exterminator", "termite control"], "location": ["California"], "limit": 1}`
- Other: `scrape_angi` with `keyword: "pest-control"`.

### 7. Residential remodelers

- NAICS: 236118 Residential Remodelers.
- Local DB: `{"keyword": ["remodeling contractor", "kitchen remodeler", "bathroom remodeler"], "location": ["Illinois"], "notCategory": ["Kitchen supply store", "Home improvement store"], "limit": 1}`
- Other: `scrape_angi` with `keyword: "kitchen-and-bath-remodeling"`.

### 8. Commercial cleaning and janitorial

- NAICS: 561720 Janitorial Services.
- Local DB: `{"keyword": ["commercial cleaning service", "janitorial service", "office cleaning"], "location": ["Ohio"], "notCategory": ["House cleaning service", "Dry cleaner"], "limit": 1}`
- Lead DB: `{"title": "Owner, President, CEO, Founder", "keywords": ["janitorial", "commercial cleaning"], "companyState": ["Ohio"], "limit": 1}`

## Health and personal care

### 9. Dental practices

- NAICS: 621210 Offices of Dentists.
- Local DB: `{"category": ["Dentist", "Dental clinic", "Cosmetic dentist", "Pediatric dentist"], "location": ["Austin TX", "Round Rock TX"], "limit": 1}`
- Lead DB: `{"title": "Owner, Dentist, DDS, DMD, Practice Owner", "keywords": ["dental"], "companyCity": "Austin", "limit": 1}`

### 10. Chiropractors

- NAICS: 621310 Offices of Chiropractors.
- Local DB: `{"category": ["Chiropractor"], "location": ["Colorado"], "limit": 1}`

### 11. Optometrists

- NAICS: 621320 Offices of Optometrists.
- Local DB: `{"category": ["Optometrist", "Eye care center"], "location": ["Washington"], "notCategory": ["Optician"], "limit": 1}`

### 12. Veterinary clinics

- NAICS: 541940 Veterinary Services.
- Local DB: `{"category": ["Veterinarian", "Animal hospital", "Emergency veterinarian service"], "location": ["Pennsylvania"], "limit": 1}`

### 13. Med spas

- NAICS: no clean match; part of 812199 Other Personal Care Services and 621111 Offices of Physicians. Skip the CBP benchmark.
- Local DB: `{"keyword": ["med spa", "medical spa", "botox"], "location": ["Florida"], "notCategory": ["Day spa", "Nail salon"], "limit": 1}`

### 14. Gyms and fitness studios

- NAICS: 713940 Fitness and Recreational Sports Centers.
- Local DB: `{"category": ["Gym", "Fitness center", "Yoga studio", "Pilates studio"], "location": ["New York"], "limit": 1}`
- Other: `scrape_yelp` with `searchTerms: ["gym", "boutique fitness"]`.

### 15. Home health agencies

- NAICS: 621610 Home Health Care Services.
- Local DB: `{"keyword": ["home health care service", "home care agency"], "location": ["Michigan"], "limit": 1}`
- Lead DB: `{"title": "Owner, Administrator, Executive Director, CEO", "keywords": ["home health", "home care"], "companyState": ["Michigan"], "limit": 1}`

## Professional services

### 16. Law firms

- NAICS: 541110 Offices of Lawyers.
- Local DB: `{"category": ["Law firm", "Attorney", "Personal injury attorney", "Family law attorney"], "location": ["New Jersey"], "limit": 1}`
- Lead DB: `{"title": "Managing Partner, Founding Partner, Owner, Principal Attorney", "keywords": ["law firm"], "companyState": ["New Jersey"], "limit": 1}`

### 17. CPA firms

- NAICS: 541211 Offices of Certified Public Accountants.
- Local DB: `{"category": ["Accountant", "Certified public accountant", "Tax preparation service"], "location": ["Virginia"], "limit": 1}`
- Lead DB: `{"title": "Managing Partner, Partner, Owner, CPA", "keywords": ["accounting", "cpa"], "companyState": ["Virginia"], "limit": 1}`

### 18. Insurance agencies

- NAICS: 524210 Insurance Agencies and Brokerages.
- Local DB: `{"category": ["Insurance agency"], "location": ["Tennessee"], "limit": 1}`

### 19. Real estate brokerages

- NAICS: 531210 Offices of Real Estate Agents and Brokers.
- Local DB: `{"category": ["Real estate agency"], "location": ["Arizona"], "limit": 1}`
- Other: `scrape_zillow_agents` for individual agents ($0.029 per agent), which is a people market, not an account market.

### 20. IT managed service providers

- NAICS: 541512 Computer Systems Design Services (MSPs also file under 541519 and 541513).
- Lead DB: `{"title": "Owner, Founder, CEO, President", "keywords": ["managed services", "msp", "it services"], "minEmployees": 2, "maxEmployees": 200, "companyCountry": ["United States"], "limit": 1}`
- Local DB: `{"keyword": ["it services", "computer support", "managed it services"], "location": ["United States"], "limit": 1}`

### 21. Marketing agencies

- NAICS: 541810 Advertising Agencies and 541613 Marketing Consulting Services.
- Lead DB: `{"title": "Owner, Founder, CEO, Managing Director", "keywords": ["marketing agency", "digital marketing"], "minEmployees": 2, "maxEmployees": 100, "companyCountry": ["United States"], "limit": 1}`

## Software, commerce and logistics

### 22. B2B SaaS companies

- NAICS: 513210 Software Publishers.
- Lead DB: `{"title": "CEO, Founder, Co-Founder", "keywords": ["saas"], "minEmployees": 10, "maxEmployees": 500, "companyCountry": ["United States"], "limit": 1}`
- Other: Tech Stack Search for a technology-defined slice, for example `{"technology": "HubSpot"}` at $4.99 per technology, then intersect domains.

### 23. Shopify stores in a category

- NAICS: none fits; skip the CBP benchmark.
- Store Leads: `{"platform": "shopify", "countryCode": "US", "category": "pet supplies", "emails": true, "totalLeads": 100, "offset": 0}` as a $0.39 probe, then the full pull with `offset` paging. Use `minEstimatedMonthlyVisits` or `minEstimatedMonthlySales` to cut hobby stores server-side so they are never billed.
- Other: Ecommerce Database by REST `GET /api/v1/database/ecommerce` on Growth and Scale.

### 24. Trucking carriers

- NAICS: 484121 General Freight Trucking, Long-Distance, Truckload.
- Lead DB: `{"title": "Owner, President, CEO, Director of Operations", "keywords": ["trucking", "freight"], "minEmployees": 5, "maxEmployees": 500, "companyCountry": ["United States"], "limit": 1}`
- Local DB: `{"keyword": ["trucking company"], "location": ["Texas"], "notCategory": ["Truck rental agency", "Truck repair shop"], "limit": 1}`

## Size and quality filters that apply across recipes

| Goal | Local DB parameter | Lead DB parameter |
|-|-|-|
| Established businesses only | `minReviews: 20` | `minEmployees: 5` |
| Exclude struggling businesses | `minRating: 3.5` | none |
| Small, fixable-reputation businesses (reputation services) | `maxRating: 3.9`, `minReviews: 10` | none |
| Has a website (needed for email) | `hasWebsite: true` | `hasEmail: true` |
| Has a named owner or manager | `hasContact: true` | title set |
| A map rectangle (one county or service area) | `box: "minLat,minLng,maxLat,maxLng"` | `city` list |
| Only records not pulled before | `excludeDelivered: true` | `excludeDelivered: true` |

Use quality filters for SAM, not TAM. TAM counts every business in the definition; SAM applies the filters that describe who the team can serve.

## Sources

- US Census Bureau, NAICS: https://www.census.gov/naics/
- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- ScraperCity MCP tool schemas for `query_local_business_database` and `query_lead_database`: https://www.npmjs.com/package/scrapercity
- ScraperCity catalog (Angi slugs, Store Leads filters, prices): references/scrapercity-catalog.md
