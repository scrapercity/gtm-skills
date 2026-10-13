# Local Business Category Recipes

Ready searches for 56 verticals. Each row gives the `keyword` array to start with, an optional `category` array to tighten it, the `notCategory` exclusions that remove common neighbors, and the filter flags that fit the usual offer.

How to use a row:

1. Send `keyword` plus your `location` with `limit: 1`.
2. Read `searched_as.keywords[].categories`. If neighbors show up, add the row's `notCategory`.
3. If the count is too broad, switch to the row's `category` array.

Category names follow Google Business Profile wording. A category word also finds categories that contain it, so `["Dentist"]` is broad and `["Pediatric dentist"]` is narrow. Confirm the exact spelling against `searched_as` before a big pull.

## Health and wellness

| # | Vertical | keyword | category (to tighten) | notCategory | Flags |
|---|---|---|---|---|---|
| 1 | General dentists | `["dentist"]` | `["Dentist"]` | `["Dental laboratory","Dental supply store"]` | `hasEmail` |
| 2 | Orthodontists | `["orthodontist"]` | `["Orthodontist"]` | `["Dental laboratory"]` | `hasEmail` |
| 3 | Pediatric dentists | `["pediatric dentist"]` | `["Pediatric dentist"]` | | `hasEmail` |
| 4 | Chiropractors | `["chiropractor"]` | `["Chiropractor"]` | | `hasEmail`, `hasContact` |
| 5 | Physical therapy clinics | `["physical therapy"]` | `["Physical therapy clinic","Physical therapist"]` | `["Hospital"]` | `hasEmail` |
| 6 | Med spas | `["med spa","medical spa"]` | `["Medical spa"]` | `["Day spa","Nail salon"]` | `hasEmail`, `hasWebsite` |
| 7 | Optometrists | `["optometrist","eye doctor"]` | `["Optometrist"]` | `["Optician"]` | `hasEmail` |
| 8 | Veterinarians | `["veterinarian","animal hospital"]` | `["Veterinarian","Animal hospital"]` | `["Pet store","Pet groomer"]` | `hasEmail` |
| 9 | Dermatologists | `["dermatologist"]` | `["Dermatologist"]` | `["Hospital"]` | `hasEmail` |
| 10 | Mental health practices | `["therapist","counseling"]` | `["Psychotherapist","Counselor","Psychologist"]` | `["Hospital"]` | `hasEmail` |
| 11 | Pharmacies (independent) | `["pharmacy"]` | `["Pharmacy"]` | `["Hospital"]` | `hasPhone`; exclude chains with `title` review |
| 12 | Home health agencies | `["home health care"]` | `["Home health care service"]` | `["Hospital","Nursing home"]` | `hasEmail` |
| 13 | Gyms and fitness studios | `["gym","fitness studio"]` | `["Gym","Fitness center"]` | `["Sporting goods store"]` | `hasEmail`, `hasWebsite` |
| 14 | Yoga and pilates studios | `["yoga studio","pilates studio"]` | `["Yoga studio","Pilates studio"]` | | `hasEmail` |

## Home services

| # | Vertical | keyword | category (to tighten) | notCategory | Flags |
|---|---|---|---|---|---|
| 15 | Plumbers | `["plumber"]` | `["Plumber"]` | `["Plumbing supply store"]` | `hasPhone`, `hasWebsite` |
| 16 | HVAC | `["hvac contractor","air conditioning contractor"]` | `["HVAC contractor","Air conditioning contractor","Heating contractor"]` | `["Air conditioning store","Appliance store"]` | `hasPhone` |
| 17 | Electricians | `["electrician"]` | `["Electrician"]` | `["Electrical supply store","Lighting store"]` | `hasPhone` |
| 18 | Roofers | `["roofing contractor"]` | `["Roofing contractor"]` | `["Roofing supply store"]` | `hasPhone`, `hasWebsite` |
| 19 | General contractors | `["general contractor"]` | `["General contractor"]` | `["Building materials store"]` | `hasEmail` |
| 20 | Landscapers | `["landscaper","lawn care"]` | `["Landscaper","Lawn care service"]` | `["Garden center","Plant nursery"]` | `hasPhone` |
| 21 | Pest control | `["pest control"]` | `["Pest control service"]` | | `hasPhone` |
| 22 | House cleaning | `["house cleaning","maid service"]` | `["House cleaning service","Janitorial service"]` | `["Dry cleaner","Laundromat"]` | `hasPhone` |
| 23 | Pool services | `["pool cleaning","pool contractor"]` | `["Pool cleaning service","Swimming pool contractor"]` | `["Public swimming pool","Swimming pool supply store"]` | `hasPhone` |
| 24 | Garage door companies | `["garage door"]` | `["Garage door supplier"]` | | `hasPhone` |
| 25 | Painters | `["painter","painting contractor"]` | `["Painter","Painting"]` | `["Art gallery","Paint store"]` | `hasPhone` |
| 26 | Solar installers | `["solar installer","solar energy"]` | `["Solar energy contractor"]` | `["Solar energy equipment supplier"]` | `hasEmail` |
| 27 | Movers | `["moving company","movers"]` | `["Mover","Moving company"]` | `["Truck rental agency","Self-storage facility"]` | `hasPhone` |
| 28 | Locksmiths | `["locksmith"]` | `["Locksmith"]` | `["Hardware store"]` | `hasPhone` |
| 29 | Water damage restoration | `["water damage restoration"]` | `["Water damage restoration service"]` | | `hasPhone` |

## Auto

| # | Vertical | keyword | category (to tighten) | notCategory | Flags |
|---|---|---|---|---|---|
| 30 | Auto repair shops | `["auto repair"]` | `["Auto repair shop","Mechanic"]` | `["Auto parts store","Car dealer"]` | `hasPhone` |
| 31 | Auto body shops | `["auto body shop","collision repair"]` | `["Auto body shop"]` | `["Car wash"]` | `hasPhone` |
| 32 | Used car dealers | `["used car dealer"]` | `["Used car dealer"]` | `["Car rental agency"]` | `hasEmail` |
| 33 | Car washes and detailing | `["car wash","auto detailing"]` | `["Car wash","Car detailing service"]` | `["Gas station"]` | `hasPhone` |
| 34 | Tire shops | `["tire shop"]` | `["Tire shop"]` | | `hasPhone` |
| 35 | Towing | `["towing service"]` | `["Towing service"]` | | `hasPhone` |

## Food and hospitality

| # | Vertical | keyword | category (to tighten) | notCategory | Flags |
|---|---|---|---|---|---|
| 36 | Independent restaurants | `["restaurant"]` | specific cuisine, e.g. `["Thai restaurant","Italian restaurant"]` | `["Fast food restaurant"]` | `hasEmail`, `maxReviews: 1500` to skip chains |
| 37 | Coffee shops | `["coffee shop","cafe"]` | `["Coffee shop","Cafe"]` | `["Coffee store"]` | `hasEmail` |
| 38 | Bakeries | `["bakery"]` | `["Bakery"]` | `["Grocery store"]` | `hasEmail` |
| 39 | Bars and breweries | `["brewery","bar"]` | `["Brewery","Bar","Brewpub"]` | `["Liquor store"]` | `hasEmail` |
| 40 | Caterers | `["caterer","catering"]` | `["Caterer"]` | | `hasEmail` |
| 41 | Boutique hotels | `["boutique hotel","inn"]` | `["Hotel","Inn","Bed & breakfast"]` | `["Motel"]` | `hasEmail`, `hasWebsite` |
| 42 | Event venues | `["event venue","wedding venue"]` | `["Event venue","Wedding venue","Banquet hall"]` | | `hasEmail` |

## Professional services

| # | Vertical | keyword | category (to tighten) | notCategory | Flags |
|---|---|---|---|---|---|
| 43 | Law firms (personal injury) | `["personal injury attorney"]` | `["Personal injury attorney"]` | `["Courthouse"]` | `hasEmail`, `hasContact` |
| 44 | Law firms (family) | `["family law attorney","divorce lawyer"]` | `["Family law attorney","Divorce lawyer"]` | | `hasEmail` |
| 45 | Accountants and CPAs | `["accountant","cpa"]` | `["Accountant","Certified public accountant","Tax preparation service"]` | | `hasEmail`, `hasContact` |
| 46 | Insurance agencies | `["insurance agency"]` | `["Insurance agency"]` | | `hasEmail`, `hasContact` |
| 47 | Financial advisors | `["financial advisor","financial planner"]` | `["Financial planner","Financial consultant"]` | `["Bank","ATM"]` | `hasEmail` |
| 48 | Real estate brokerages | `["real estate agency"]` | `["Real estate agency"]` | `["Real estate developer"]` | `hasEmail`; for agents, see `scrapercity-real-estate-data` |
| 49 | Marketing agencies (local) | `["marketing agency"]` | `["Marketing agency","Advertising agency"]` | `["Print shop"]` | `hasEmail`, `hasWebsite` |
| 50 | IT services and MSPs | `["it services","managed it"]` | `["Computer support and services","IT services"]` | `["Computer store","Cell phone store"]` | `hasEmail` |
| 51 | Staffing agencies | `["staffing agency"]` | `["Employment agency","Temp agency"]` | | `hasEmail` |

## Retail, beauty and education

| # | Vertical | keyword | category (to tighten) | notCategory | Flags |
|---|---|---|---|---|---|
| 52 | Hair salons | `["hair salon"]` | `["Hair salon","Beauty salon"]` | `["Beauty supply store","Barber supply store"]` | `hasPhone` |
| 53 | Barbershops | `["barber shop"]` | `["Barber shop"]` | `["Barber supply store"]` | `hasPhone` |
| 54 | Nail salons | `["nail salon"]` | `["Nail salon"]` | | `hasPhone` |
| 55 | Daycares and preschools | `["daycare","preschool"]` | `["Day care center","Preschool"]` | `["Elementary school"]` | `hasEmail` |
| 56 | Tutoring centers | `["tutoring"]` | `["Tutoring service"]` | | `hasEmail` |
| 57 | Florists | `["florist"]` | `["Florist"]` | `["Garden center"]` | `hasEmail` |
| 58 | Jewelry stores (independent) | `["jewelry store"]` | `["Jewelry store"]` | `["Pawn shop"]` | `hasEmail`, `maxReviews: 800` |
| 59 | Pet groomers | `["pet groomer","dog grooming"]` | `["Pet groomer"]` | `["Pet store","Veterinarian"]` | `hasPhone` |

## Filtering out chains and franchises

The database has no franchise flag. Three ways to cut chain locations:

| Method | How |
|---|---|
| Brand names | Pull a `limit: 100` sample, list the repeated names, re-run and drop rows whose `title` matches them in your post-processing. `title` is an include filter, so remove brands after the pull |
| Review ceiling | Big chains pile up reviews per location. `maxReviews: 800` to `1500` trims many of them; test on the sample first |
| Website domain | Group rows by `website` domain; a domain on 10+ rows is a chain |

## Picking flags by offer

| Offer | Flags |
|---|---|
| Cold email | `hasEmail: true` |
| Cold calling | `hasPhone: true` (check DNC and TCPA rules for mobiles) |
| Website, SEO, ads services | `hasWebsite: true` for redesign offers, or no flag and filter rows without `website` for "you have no website" offers |
| Personalized email to the owner | `hasContact: true` |
| Review management | `maxRating: 4.2` or `maxReviews: 30` |

## Sources

- https://support.google.com/business/answer/3038177
- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://www.brightlocal.com/research/local-consumer-review-survey/
