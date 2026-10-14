# Local Category Recipes

Search inputs for 30 local verticals: the `keyword` set for `query_local_business_database` and Google Maps, `notCategory` exclusions, the `jobTitle` to send to `scrape_website_finder` when a row has a website and no email, the Yelp search term, and the Angi slug where one exists. Category labels in `notCategory` are written the way Google Maps names categories; confirm each with a `limit: 1` count and read `searched_as` before relying on it, since a label that matches nothing silently excludes nothing.

## How to use a recipe

1. Copy the keyword set into `keyword` (database) and the first 2-3 terms into `searchStringsArray` (Maps).
2. Add `notCategory` and the area from `metro-split-and-geo-recipes.md`.
3. Run the four count calls (all, `hasWebsite`, `hasEmail`, `hasContact`).
4. For rows with a website and no email, run Website Finder with the recipe's title; run a second title only on the misses.
5. Apply the vertical's notes before sending.

## Health and wellness

| # | Vertical | `keyword` | `notCategory` | Website Finder `jobTitle` | Yelp term | Notes |
|-|-|-|-|-|-|-|
| 1 | Dentists | dentist, dental clinic, cosmetic dentist, pediatric dentist | Dental laboratory, Dental supply store, Dental school | Office Manager | dentist | Group practices share inboxes; collapse on email. DSO-supported offices can keep the practice name: run the independence screen. Specialists stay in, tagged by NPI taxonomy, unless the user excludes them |
| 2 | Orthodontists | orthodontist | Dental laboratory | Practice Manager | orthodontist | Many locations under one owner; one row per brand |
| 3 | Chiropractors | chiropractor, chiropractic clinic | Massage therapist | Owner | chiropractor | Owner usually the doctor; "Dr." in salutation |
| 4 | Physical therapy | physical therapy clinic, physical therapist | Hospital | Clinic Director | physical therapy | Hospital-owned clinics buy centrally; exclude |
| 5 | Med spas | med spa, medical spa, botox, laser hair removal | Day spa, Nail salon | Owner | med spa | Owner often a nurse practitioner or physician |
| 6 | Optometrists | optometrist, eye care center | Optician, Eyewear store | Office Manager | optometrist | Retail chain optical counters inflate counts |
| 7 | Veterinarians | veterinarian, animal hospital, veterinary clinic | Pet store, Pet groomer | Practice Manager | veterinarian | Corporate-owned groups common; run the independence screen |
| 8 | Dermatology | dermatologist, dermatology clinic | Beauty salon | Practice Administrator | dermatologist | Large groups buy centrally |
| 9 | Counseling and therapy practices | counselor, therapist, mental health clinic | Hospital | Clinical Director | therapist | Many solo practitioners on Gmail; keep `is_free` rows |

## Home services

| # | Vertical | `keyword` | `notCategory` | Website Finder `jobTitle` | Angi slug | Notes |
|-|-|-|-|-|-|-|
| 10 | Plumbers | plumber, plumbing service, drain cleaning | Plumbing supply store | Owner | plumbing | Owner-operators answer `info@` |
| 11 | HVAC | hvac contractor, air conditioning contractor, heating contractor | HVAC supply store, Appliance store | Owner | hvac | Seasonal: email in shoulder months |
| 12 | Roofers | roofing contractor, roofer | Roofing supply store | Owner | roofing | Storm-chasing firms change domains; re-validate before each send |
| 13 | Electricians | electrician, electrical contractor | Electrical supply store, Lighting store | Owner | electrical | Commercial and residential mix; split by keyword |
| 14 | Landscapers | landscaper, landscaping service, lawn care service | Garden center, Nursery | Owner | landscaping | Many Gmail addresses; keep them |
| 15 | Pest control | pest control service, exterminator | Hardware store | General Manager | pest-control | National franchises; one row per location |
| 16 | House cleaning | house cleaning service, maid service, janitorial service | Dry cleaner, Laundromat | Owner | house-cleaning | Commercial janitorial is a separate segment |
| 17 | Garage doors | garage door supplier, garage door repair | Hardware store | Owner | garage-doors | Lead-gen sites list fake locations; drop domains seen 10+ times |
| 18 | Pool service | pool cleaning service, pool contractor | Swimming pool supply store | Owner | pool-and-spa-service | Sun Belt metros only |
| 19 | Solar installers | solar energy company, solar panel installer | Electrical supply store | Owner | solar-panels | High churn; validate within 7 days of sending |
| 20 | Tree service | tree service, arborist | Garden center | Owner | tree-service | Phone-first businesses; email coverage runs low |
| 21 | Remodelers | remodeler, kitchen remodeler, bathroom remodeler, general contractor | Home improvement store, Kitchen supply store | Owner | kitchen-and-bath-remodeling | Mix of owner-builders and design firms |

## Professional services

| # | Vertical | `keyword` | `notCategory` | Website Finder `jobTitle` | Yelp term | Notes |
|-|-|-|-|-|-|-|
| 22 | Personal injury law firms | personal injury attorney, accident lawyer | Legal services, Notary public | Managing Partner | personal injury lawyer | One row per firm |
| 23 | Accountants and CPA firms | accountant, cpa, tax preparation service | Bookkeeping service (if excluded) | Managing Partner | accountant | Avoid February to April 15 for cold email |
| 24 | Insurance agencies | insurance agency, insurance agent | Insurance company | Agency Owner | insurance agent | Captive agents cannot buy many products; filter by brand names in titles |
| 25 | Real estate brokerages | real estate agency, real estate broker | Property management company | Broker Owner | real estate agent | For individual agents use `scrape_zillow_agents` instead |
| 26 | Financial advisors | financial planner, financial advisor, wealth management | Bank, Credit union | Principal | financial advisor | One row per brand |

## Hospitality, retail and auto

| # | Vertical | `keyword` | `notCategory` | Website Finder `jobTitle` | Yelp term | Notes |
|-|-|-|-|-|-|-|
| 27 | Independent restaurants | restaurant plus the cuisine (thai restaurant, steakhouse) | Fast food restaurant, Meal delivery | General Manager | restaurants | Yelp coverage is dense; use it as the second source |
| 28 | Gyms and fitness studios | gym, fitness center, yoga studio, pilates studio, crossfit gym | Sporting goods store | Owner | gyms | Franchise studios buy through corporate; one row per brand |
| 29 | Salons and barbershops | hair salon, barber shop, beauty salon | Beauty supply store | Owner | hair salons | Booking-platform pages are not websites; blank those domains |
| 30 | Auto repair shops | auto repair shop, mechanic, auto body shop | Auto parts store, Car dealer | Owner | auto repair | Dealer service departments buy through the dealership |

## Contact title ladder for Website Finder

Website Finder takes one `jobTitle` per request. Run the first title on every domain without an email; run the second only on the misses.

| Business type | First title | Second title |
|-|-|-|
| Owner-operated trades and studios | Owner | President |
| Medical and dental practices | Office Manager | Practice Manager |
| Multi-provider clinics | Practice Administrator | Clinic Director |
| Restaurants and hospitality | General Manager | Owner |
| Law, accounting and advisory firms | Managing Partner | Office Manager |
| Franchise locations | General Manager | Franchise Owner |

Ceiling per run: domains x $0.0499. A 26-domain run is at most $1.30.

## Exclusion add-ons

| Situation | Add |
|-|-|
| Only established businesses | `minReviews: 25` |
| Only well-rated businesses (reputation offers, premium services) | `minRating: 4.3` |
| Businesses with weak reviews (reputation management offers) | `maxRating: 3.9`, `minReviews: 10` |
| Only businesses with a named contact | `hasContact: true` |
| Phone-first campaign | `hasPhone: true`, drop the email requirement, run mobiles through mobile-appender's line-type and suppression checks |
| Exclude one brand name | `title` cannot exclude; drop rows by `business_name_key` after the pull |

## Copy notes by vertical type

| Type | Note for the list owner |
|-|-|
| Clinicians (dentists, chiropractors, optometrists, veterinarians) | Store `credentials` and use "Dr." only when the listing or website shows it |
| Trades | First names are common in business names ("Mike's Plumbing"); do not guess a first name from it |
| Restaurants | Avoid sending during lunch and dinner service; mid-afternoon local time |
| Professional firms | One partner per firm; never email every partner at once |

## Sources

- ScraperCity MCP tool schemas (`query_local_business_database`, `scrape_maps`, `scrape_yelp`, `scrape_angi` slugs, `scrape_website_finder`): https://www.npmjs.com/package/scrapercity
- ScraperCity CLI repository: https://github.com/scrapercity/scrapercity-cli
- Google Business Profile Help, Guidelines for representing your business (category selection): https://support.google.com/business/answer/3038177
- US Census Bureau, NAICS codes: https://www.census.gov/naics/
