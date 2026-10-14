# Metro Split and Geo Recipes

How to turn an area into searchable pieces, where to spend on scrapes, how to page the database, and how to dedupe local rows from several sources. Parameter names come from the `query_local_business_database`, `scrape_maps` and `scrape_yelp` schemas in the published package; prices from `references/scrapercity-catalog.md`.

## 1. Split rules

| Area the user names | Database `location` | Scrape inputs |
|-|-|-|
| One small city (under about 100,000 people) | `["Kyle TX"]` | One `locationQuery` per run |
| A metro | Every sub-city in one array (section 2) | One run per sub-city that is a gap |
| A large city core | The city name, then `box` per quadrant if a call returns 503 | A Google Maps search link per box passed as `url`, or ZIP codes as `locationQuery` |
| A state | `["Texas"]`, or its metros as separate calls when counts are huge | Cities by population, one run each, only where gaps show |
| A list of ZIP codes | The ZIPs as strings, up to 2,000 entries | One `locationQuery` per ZIP; `zipCodes` array for `scrape_angi` |
| A radius around an address | A `box` around the point (section 3) | A Google Maps search link centered on the point |

Always add the state to a city name. "San Marcos" is in Texas and in California; "Aurora" is in Colorado and Illinois. Read `searched_as.places` after the first call: every entry should show `read_as`, and any `not_found` gets a new spelling or a ZIP code.

## 2. Sub-city lists for 15 metros

Pass every sub-city in one `location` array for the database; scrape only the sub-cities the coverage table flags.

| Metro | Sub-cities |
|-|-|
| Austin, TX | Austin, Round Rock, Cedar Park, Georgetown, Pflugerville, Leander, Kyle, Buda, San Marcos, Lakeway, Hutto, Manor, Bee Cave, Dripping Springs |
| Houston, TX | Houston, Pasadena, Pearland, Sugar Land, The Woodlands, Katy, Spring, Humble, League City, Baytown, Missouri City, Conroe, Cypress, Friendswood, Tomball |
| Dallas-Fort Worth, TX | Dallas, Fort Worth, Arlington, Plano, Irving, Garland, Frisco, McKinney, Grand Prairie, Denton, Mesquite, Carrollton, Richardson, Lewisville, Allen, Flower Mound, Mansfield, Grapevine, Southlake |
| Phoenix, AZ | Phoenix, Mesa, Chandler, Scottsdale, Gilbert, Glendale, Tempe, Peoria, Surprise, Goodyear, Avondale, Buckeye, Queen Creek, Cave Creek |
| Atlanta, GA | Atlanta, Sandy Springs, Roswell, Alpharetta, Marietta, Smyrna, Johns Creek, Dunwoody, Decatur, Kennesaw, Lawrenceville, Duluth, Peachtree City, Brookhaven |
| Denver, CO | Denver, Aurora, Lakewood, Thornton, Arvada, Westminster, Centennial, Highlands Ranch, Littleton, Broomfield, Castle Rock, Parker, Englewood, Golden |
| South Florida | Miami, Miami Beach, Hialeah, Coral Gables, Doral, Kendall, Homestead, Fort Lauderdale, Hollywood, Pembroke Pines, Coral Springs, Boca Raton, Delray Beach, West Palm Beach, Jupiter |
| Chicago, IL | Chicago, Naperville, Aurora, Joliet, Evanston, Schaumburg, Oak Park, Arlington Heights, Skokie, Orland Park, Wheaton, Downers Grove, Oak Brook, Elgin, Waukegan |
| Los Angeles County, CA | Los Angeles, Long Beach, Glendale, Pasadena, Santa Monica, Burbank, Torrance, Santa Clarita, Pomona, West Covina, Inglewood, Downey, Beverly Hills, Culver City, El Monte |
| New York City area | Manhattan, Brooklyn, Queens, Bronx, Staten Island, Yonkers, White Plains, New Rochelle, Hempstead, Huntington, Jersey City, Newark, Hoboken |
| Seattle, WA | Seattle, Bellevue, Tacoma, Kent, Everett, Renton, Redmond, Kirkland, Federal Way, Auburn, Lynnwood, Bothell, Issaquah, Sammamish |
| Tampa Bay, FL | Tampa, St. Petersburg, Clearwater, Brandon, Largo, Wesley Chapel, Riverview, Lutz, Palm Harbor, Dunedin, Lakeland, Bradenton, Sarasota |
| Charlotte, NC | Charlotte, Concord, Gastonia, Huntersville, Matthews, Mooresville, Cornelius, Mint Hill, Indian Trail, Rock Hill SC, Fort Mill SC |
| Nashville, TN | Nashville, Franklin, Murfreesboro, Brentwood, Hendersonville, Gallatin, Smyrna, Mount Juliet, Lebanon, Spring Hill, Clarksville |
| San Diego, CA | San Diego, Chula Vista, Oceanside, Escondido, Carlsbad, El Cajon, Vista, San Marcos, Encinitas, La Mesa, Santee, Poway, National City |

For metros not listed, take the county list for the metro from the Census Bureau's metropolitan statistical area definitions, then list the incorporated places in each county.

New York boroughs: pass "Brooklyn NY" style names to the database and read `searched_as`; if a borough is read as a county, keep it, since the area is the same.

## 3. Map boxes

`query_local_business_database` accepts `box` as `minLat,minLng,maxLat,maxLng` and returns only businesses inside it; an unreadable box returns 400. The tool's own example is `30.1,-97.9,30.5,-97.5`, which covers central Austin.

Size: one degree of latitude is about 111 km; one degree of longitude is about 111 km times the cosine of the latitude (about 96 km at Austin's 30 degrees north). The example box is about 44 km tall and 38 km wide.

Quadrant split of the example box:

| Box | `box` value |
|-|-|
| Southwest | `30.1,-97.9,30.3,-97.7` |
| Southeast | `30.1,-97.7,30.3,-97.5` |
| Northwest | `30.3,-97.9,30.5,-97.7` |
| Northeast | `30.3,-97.7,30.5,-97.5` |

Grid generator for an n x n split:

```python
def grid(min_lat, min_lng, max_lat, max_lng, n):
    dlat, dlng = (max_lat - min_lat) / n, (max_lng - min_lng) / n
    for i in range(n):
        for j in range(n):
            yield f"{min_lat + i*dlat:.4f},{min_lng + j*dlng:.4f},{min_lat + (i+1)*dlat:.4f},{min_lng + (j+1)*dlng:.4f}"
```

Radius around an address: a box with half-width r km is latitude plus or minus r / 111 and longitude plus or minus r / (111 x cos(latitude)). A 10 km radius around downtown Austin (30.267, -97.743) gives `30.177,-97.847,30.357,-97.639`.

For Maps scrapes over a box, open Google Maps on that area, search the category, and pass the link as `url`. With no place in the search words, the map area the link shows is searched; the response's `search_translation` says what ran.

## 4. Where to scrape

Build the coverage table from per-sub-area count calls (A: all, C: with website and email), then:

| Signal | Action | Ceiling formula |
|-|-|-|
| Coverage C / A is under the gap line the user sets against the metro average | `scrape_maps` for that sub-area, 2-3 terms, cap 60 or less per term (Google's text search maximum) | terms x cap x $0.0099 |
| A count far under the CBP establishment count for the county | `scrape_maps` across the county's cities | cities x terms x cap x $0.0099 |
| Vertical with dense Yelp listings (restaurants, beauty, auto, home services) | `scrape_yelp` for the weakest 1-3 sub-areas | terms x locations x `searchLimit` x $0.0099 |
| Home services with an Angi slug | `scrape_angi` with `zipCodes` for the gap ZIPs | `maxItems` x $0.0099 |
| A Maps term returns exactly at its cap | Split that sub-area into ZIP codes and rerun the term | Same per ZIP |
| The sub-area's outside-list or database count is already above the per-term cap | Run Maps by ZIP there from the start, using the ZIPs on the outside list's location addresses | ZIPs x terms x cap x $0.0099 |
| Coverage is fine everywhere | No scrape | $0 |

Before paying for a Maps run, read the `local_business_database` block a Maps start response can return: it reports how many businesses for the same search are already in the database and not yet in the account, with the call that returns them. Pull those first and cancel the scrape if they cover the gap.

Scrape output columns differ by tool and version. Read each CSV's header row and map columns to the business schema before merging; record any missing field (for example no email column) in the report.

## 5. Paging the database

| Need | Parameters |
|-|-|
| Count only | `limit: 1`; read `pagination.total` |
| All rows of a search | `limit: 100`, `after: "0"`, then `pagination.next_after` until null |
| Only businesses the account does not have yet | add `excludeDelivered: true`, keep `after` paging |
| Long location lists | `POST /api/v1/database/local-businesses` with a JSON body |
| More than 100,000 new businesses | Split across days by state or metro; only new records count toward the daily allowance |

Every record returned is saved to the account; fetching one the account already has is free. A refresh with `excludeDelivered: true` returns only businesses added since the last pull.

## 6. Dedupe across sources

Keys from `references/list-quality-standard.md` section 4a for local businesses, tried in order:

| Order | Key | Catches |
|-|-|-|
| 1 | Registrable `domain` | The same business listed on Maps and in the database |
| 2 | `phone` in E.164 | Listings with different names for the same office ("Smile Dental" vs "Smile Dental of Austin") |
| 3 | `business_name_key` plus `postal_code` | Listings with no website and different phone formats |
| 4 | `business_name_key` plus `street` | Two suites in one building |

Chain and group policy, decided with the user before the merge:

| Policy | Key 1 | Use when |
|-|-|-|
| One row per location | `phone` | Each location buys on its own (franchise owners, multi-location contractors) |
| One row per brand | `domain` | One office manager or owner buys for every location |
| Always | Collapse rows sharing one email to one row | Emailing one inbox twice reads as spam |

Survivorship when rows merge: valid email beats any other status; non-empty beats empty; source precedence for a field is user CRM, then Website Finder or Email Finder, then the Local Business Database, then Maps, Yelp and Angi; newer `pulled_at` wins ties. `source` joins every contributor with a pipe (`local_db|maps`).

## 7. Recipe library

| # | Job | Database call | Gap fill |
|-|-|-|-|
| 1 | One vertical in one metro | keyword set, sub-city list, `hasWebsite`, `hasEmail` | Maps in flagged sub-cities |
| 2 | Statewide list | `location: ["Florida"]`, keyword set, `hasEmail` | Maps in the 10 largest cities only where coverage lags |
| 3 | Owner-named list | Recipe 1 plus `hasContact: true` | Website Finder with "Owner" on rows with a website and no contact |
| 4 | High-rated only | add `minRating: 4.5`, `minReviews: 50` | None; scrapes return all ratings, filter after |
| 5 | Newer or smaller businesses | `maxReviews: 20` | Maps with a cap of 60, since new listings sit low in results |
| 6 | Exclude chains | `notCategory` for franchise categories, then the independence screen in `coverage-segments-and-handoff.md` section 1c (chain line set by the user) | None |
| 7 | Radius campaign around one office | `box` from section 3 | Maps with a Google Maps link of the same area as `url` |
| 8 | ZIP list from a client's service area | `location` as the ZIP list | `scrape_angi` with `zipCodes` for home services |
| 9 | New-business refresh | Recipe 1 plus `excludeDelivered: true` | None |
| 10 | A saved Google Maps search | `url` set to the search link; read `search_translation` | Same link to `scrape_maps` as `url` if gaps remain |

## Sources

- ScraperCity MCP tool schemas (`query_local_business_database`, `scrape_maps`, `scrape_yelp`, `scrape_angi`): https://www.npmjs.com/package/scrapercity
- ScraperCity CLI repository: https://github.com/scrapercity/scrapercity-cli
- Google Maps Platform, Text Search (New): https://developers.google.com/maps/documentation/places/web-service/text-search
- US Census Bureau, Metropolitan and micropolitan delineation files: https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html
- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- Public Suffix List: https://publicsuffix.org/
