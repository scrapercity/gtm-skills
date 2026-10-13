# Coverage and Dedupe Playbook

How to find gaps, fill them with scrapes, merge sources into one account per real business, and estimate how much of the market the file holds.

## 1. Gap detection

Compute a density per metro or county for the deduped database pull, then compare.

| Signal | Threshold (house standard, 2026-10) | Action |
|-|-|-|
| Accounts per 100,000 residents in a metro below half the state figure | Under 0.5x | Maps gap fill for that metro |
| Database count far below the Census CBP establishment count for the NAICS code in that county | Under 60% | Maps gap fill, then Yelp or Angi for trades |
| Database count above CBP | Over 130% | Definition too loose; check categories in a 50-row sample |
| A Maps probe of 50 places returns over 40% businesses not in the database | Over 40% new | Run the full sub-city split for that metro |
| A Maps probe returns under 10% new | Under 10% new | Stop; the database already covers the metro |

Population per metro comes from the Census; establishment counts by county come from County Business Patterns on data.census.gov.

## 2. Maps run design

`scrape_maps` costs $0.0099 per business returned. `maxCrawledPlacesPerSearch` caps results per search term, so the ceiling for one run is terms x cap. A single search for a big metro misses outer suburbs, so split by sub-city and run 2-4 keyword variants.

| Parameter | Setting |
|-|-|
| `searchStringsArray` | 2-4 variants of the category ("hvac contractor", "air conditioning repair", "heating contractor") |
| `locationQuery` | One sub-city per run ("Pasadena, TX") |
| `maxCrawledPlacesPerSearch` | 50 for suburbs, 100 for core cities |
| `customGeolocation` | Use instead of `locationQuery` for a service-area polygon or bounding box |
| `url` | A Google Maps search link; the run reports `search_translation` |

Before running, the Maps response can include a `local_business_database` block listing matches already in the Local Business Database that the account does not have. Pull those with `query_local_business_database` first; they count against the daily allowance instead of the wallet.

### Sub-city splits for large metros

Use these as starting lists; add suburbs from the metro's county list if a probe shows gaps.

| Metro | Sub-cities to run separately |
|-|-|
| Houston, TX | Houston, Pasadena, Pearland, Sugar Land, Katy, The Woodlands, Spring, Cypress, Baytown, League City, Conroe, Humble |
| Dallas-Fort Worth, TX | Dallas, Fort Worth, Arlington, Plano, Irving, Garland, Frisco, McKinney, Grand Prairie, Denton, Mesquite, Carrollton |
| Austin, TX | Austin, Round Rock, Cedar Park, Georgetown, Pflugerville, Leander, Kyle, San Marcos |
| San Antonio, TX | San Antonio, New Braunfels, Schertz, Boerne, Converse, Live Oak |
| Phoenix, AZ | Phoenix, Mesa, Chandler, Scottsdale, Gilbert, Glendale, Tempe, Peoria, Surprise, Goodyear |
| Atlanta, GA | Atlanta, Marietta, Alpharetta, Roswell, Sandy Springs, Duluth, Lawrenceville, Kennesaw, Decatur, Smyrna |
| Chicago, IL | Chicago, Naperville, Aurora, Joliet, Evanston, Schaumburg, Oak Lawn, Arlington Heights, Elgin, Orland Park |
| Los Angeles, CA | Los Angeles, Long Beach, Glendale, Santa Clarita, Pasadena, Torrance, Burbank, Pomona, West Covina, Downey, Santa Monica, Inglewood |
| New York, NY | Manhattan, Brooklyn, Queens, Bronx, Staten Island, Yonkers, New Rochelle, Hempstead, Jersey City, Newark |
| Miami, FL | Miami, Hialeah, Miami Beach, Coral Gables, Homestead, Fort Lauderdale, Hollywood, Pembroke Pines, Boca Raton, West Palm Beach |
| Denver, CO | Denver, Aurora, Lakewood, Littleton, Arvada, Westminster, Thornton, Centennial, Englewood, Highlands Ranch |
| Seattle, WA | Seattle, Bellevue, Tacoma, Everett, Kent, Renton, Redmond, Kirkland, Federal Way, Auburn |

### Yelp and Angi as second scrapers

| Source | When | Call |
|-|-|-|
| `scrape_yelp` ($0.0099 per result) | Restaurants, salons, fitness, retail, where Yelp coverage is strong | `{"searchTerms": ["hvac"], "locations": ["Pasadena, TX"], "searchLimit": 50}` |
| `scrape_angi` ($0.0099 per listing) | Home services; needs a slug from the catalog list | `{"keyword": "hvac", "zipCodes": ["77502", "77503", "77504"], "maxItems": 200}` |

## 3. Normalization before merge

Apply `references/list-quality-standard.md` section 3 to every source before any comparison. The fields that decide matches:

| Field | Rule |
|-|-|
| `domain` | Registrable domain, lowercase; blank for social or platform hosts |
| `business_name_key` | Lowercase, punctuation stripped, `&` to `and`, legal suffix and leading "the" removed |
| `phone` | E.164 |
| `postal_code` | 5-digit text for US |
| `street` | Lowercase; abbreviations standardized (street to st, avenue to ave, suite to ste) |

## 4. Dedupe passes

Run the passes in order. Each pass only compares rows that did not merge in an earlier pass.

| Pass | Key | Merges | Watch for |
|-|-|-|-|
| 1 | `domain` | Same company across sources | Franchise and multi-location brands share one domain. For local TAMs keep one row per location: within a domain group, merge only rows that also share a phone or a postal code. |
| 2 | `business_name_key + postal_code` | Rows without a domain, same name, same ZIP | Two different "Elite Plumbing" businesses in one ZIP are rare but real; check if phones differ. |
| 3 | `business_name_key + street` | Rows where ZIP was missing or wrong | |
| 4 | `phone` | Name variants ("ABC Heating" vs "ABC Heating and Air") | Shared call centers and answering services; skip phone merges when 5+ rows share one number. |

Fuzzy name matching (edit distance) is optional; if used, require the same postal code and a similarity of at least 0.9, and log every fuzzy merge for review.

## 5. Survivorship

For each merged group:

1. Compute the completeness score from the quality standard: email 3, valid email 2, named contact 2, phone 1, website 1, full street address 1, rating and reviews 1.
2. Keep the highest scoring row as the base. Ties go to the newer `pulled_at`.
3. Fill each empty field on the base from the other rows, using source precedence: `local_db` and `lead_db` > `maps` > `yelp` and `angi` > `store_leads`.
4. Set `source` to every contributing source joined with `|` in precedence order, and `source_detail` to the base row's detail.
5. Keep `merged_from` with the count of rows merged, for audit.

## 6. Coverage estimate

Use two sources that searched the same area independently, for example the Local Business Database and a Maps run for one metro.

```text
n1 = deduped accounts from source A in the metro
n2 = deduped accounts from source B in the same metro
m  = accounts found by both (after the dedupe passes)
Lincoln-Petersen  N = n1 * n2 / m
Chapman           N = (n1 + 1)(n2 + 1) / (m + 1) - 1
Observed          O = n1 + n2 - m
Coverage          O / N
```

Worked numbers: n1 = 1,240, n2 = 980, m = 812. Chapman N = (1,241 x 981) / 813 - 1 = 1,496.4, so about 1,496. Observed O = 1,240 + 980 - 812 = 1,408. Coverage = 1,408 / 1,496 = 94.1%.

Caveats to print with the number:

- Both sources favor businesses with an online presence, so the estimate is a floor. Businesses that are invisible to both sources do not enter either sample.
- Sources are not fully independent.
- Use 1-3 metros as the sample, then apply the coverage rate to the state with caution.

When m is under 30, the estimate is unstable; widen the sample area.

## 7. Funnel and source mix

Report two tables:

1. Funnel: raw rows from all sources, after normalization drops, after each dedupe pass, after exclusions, final accounts. Each row equals the previous minus the dropped count.
2. Source mix: final accounts by primary source value (`local_db`, `local_db|maps`, `maps`, and so on). The rows sum to the final count.

## 8. Refresh

A TAM file ages. Re-run monthly with the same filters and `excludeDelivered: true` on both databases to collect only new records, then run the dedupe passes against the existing file. Mark accounts not seen in two consecutive refreshes as `possibly_closed` rather than deleting them.

## Sources

- Montana State University, WILD 502 closed-population estimators: https://www.montana.edu/rotella/documents/502/Closed.pdf
- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- data.census.gov: https://data.census.gov/
- Public Suffix List: https://publicsuffix.org/
- USPS Publication 28, street suffix abbreviations: https://pe.usps.com/text/pub28/28apc_002.htm
- ScraperCity catalog (Maps, Yelp, Angi parameters and prices): references/scrapercity-catalog.md
