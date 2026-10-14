# Coverage and Dedupe Playbook

How to find gaps, fill them with scrapes, merge sources into one account per business, and estimate how much of the market the file holds.

## 1. Gap detection

Compute a density per metro or county for the deduped database pull, then compare.

| Signal | Action |
|-|-|
| Accounts per 100,000 residents in a metro well below the state figure | Maps gap fill for that metro, lowest metros first, down to the cutoff the user picks |
| Database count below the Census CBP establishment count for the NAICS code in that county | Maps gap fill, then Yelp or Angi for trades |
| Database count above CBP | Definition too loose; check categories in a sample of rows |
| A Maps probe returns many businesses not in the database | Run the full sub-city split for that metro |
| A Maps probe returns few new businesses | Stop; the database already covers the metro |

The user sets the share of new businesses in a probe that triggers the full split, and the report records it.

Population per metro comes from the Census; establishment counts by county come from County Business Patterns on data.census.gov.

## 2. Maps run design

`scrape_maps` costs $0.0099 per business returned. `maxCrawledPlacesPerSearch` caps results per search term, so the ceiling for one run is terms x cap. A single search for a big metro misses outer suburbs, so split by sub-city and run the category's keyword variants.

| Parameter | Setting |
|-|-|
| `searchStringsArray` | Variants of the category ("hvac contractor", "air conditioning repair", "heating contractor") |
| `locationQuery` | One sub-city per run ("Pasadena, TX") |
| `maxCrawledPlacesPerSearch` | Set from the probe; raise it where a probe returns the full cap |
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
| 2 | `business_name_key + postal_code` | Rows without a domain, same name, same ZIP | Two different "Elite Plumbing" businesses in one ZIP are rare but possible; check if phones differ. |
| 3 | `business_name_key + street` | Rows where ZIP was missing or wrong | |
| 4 | `phone` | Name variants ("ABC Heating" vs "ABC Heating and Air") | Shared call centers and answering services; skip phone merges when one number is shared by rows with different names and addresses. |

Fuzzy name matching (edit distance) is optional; if used, require the same postal code, set the similarity cutoff after reviewing a sample of fuzzy merges with the user, and log every fuzzy merge for review.

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

- Both sources favor businesses with an online presence, so the population estimate is a floor and the coverage share is a ceiling. Businesses invisible to both sources never enter either sample.
- Sources are not fully independent.
- Use 1-3 metros as the sample, then apply the coverage rate to the state with caution.

When m is small, the estimate is unstable; widen the sample area.

## 7. Funnel and source mix

Report two tables:

1. Funnel: raw rows from all sources, after normalization drops, after each dedupe pass, after exclusions, final accounts. Each row equals the previous minus the dropped count.
2. Source mix: final accounts by primary source value (`local_db`, `local_db|maps`, `maps`, and so on). The rows sum to the final count.

## 8. Refresh

A TAM file ages. Re-run at the cadence the user sets with the same filters and `excludeDelivered: true` on both databases to collect only new records, then run the dedupe passes against the existing file. Mark accounts missing from consecutive refreshes (the user sets how many) as `possibly_closed` rather than deleting them.

## 9. Outside-source imports

Lists outside ScraperCity add accounts the databases and scrapers miss, and they confirm accounts the file already holds. None of them is a ScraperCity data source. Tag every imported row with `source = user_upload` (the shared vocabulary in `references/list-quality-standard.md` section 8) and put the list name in `import_sources`, for example `tdlr_ac_2026-10`. Prefer the publisher's own export or API over copying pages by hand: it carries cleaner keys for matching.

Facts in this table were checked on each publisher's own page on 2026-10-13.

| Source | What it gives you | Keys usually present | How to get it | Dedupe key order | Watch for |
|-|-|-|-|-|-|
| Conference sponsors, exhibitors and speaker rosters | Companies paying to reach your buyers; speaker rosters name a person and a company, which go to the Lead Database by `companyDomain` or `socialUrl`. Example: AHR Expo lists 1,900 exhibitors in an online exhibitor search; next show Chicago, 25 to 27 January 2027 | Company name, website, booth, sometimes city | The show's exhibitor directory or sponsor page | Domain, then name key + state | Exhibitors are mostly manufacturers and suppliers. For a contractor TAM they belong on the exclusion or partner list; for a vendor-market TAM they are the market |
| Association directories and licensing boards | Members or licensees in a trade. Example: Texas TDLR publishes CSV license files, including Air Conditioning Contractors, with business name, business address, county, ZIP, phone and license expiration fields per its file format; ACCA links a contractor locator | Business name, address, ZIP, phone; rarely a website | Download the file or search the locator | Phone (E.164), then name key + ZIP, then name key + street | Licensee rows can be individuals; keep rows with a business name. Drop expired licenses. A license list is the closest thing to a census for a licensed trade |
| Inc. 5000 | Privately held, for-profit, independent US companies ranked by three-year revenue growth (2022 to 2025 for the current list) | Company name, rank, story link | The list pages on inc.com | Name key + state, then domain after you find the website | A growth-biased slice. Use it as a segment flag (`inc5000 = true`); it is too narrow to count a market |
| G2 category pages | Software and service vendors in a category, compared by user ratings | Product name, vendor name | Browse the category page | Domain after you resolve the vendor site | These are vendors. Use them for a TAM of software companies, or as the competitor exclusion list |
| Crunchbase | Private company records with funding rounds; offers an API and exports | Name, domain, HQ, funding | Export or API on the user's plan | Domain | Use for funding-stage segments and as a domain resolver |
| Job boards and careers pages | Companies hiring for a role your market needs | Company name, location, job URL | Search by title and location | Name key + city, then domain | Staffing agencies post on behalf of clients. Exclude recruiter domains before matching |
| CMS NPPES NPI file (healthcare) | Every US provider with a National Provider Identifier; Type 2 records are organizations (practices, clinics, agencies). CMS posts a monthly full file (the October 12, 2026 file is about 1.1 GB) plus weekly updates and a deactivation file | Organization name, practice address, phone, taxonomy (specialty) code | Download from the CMS NPPES page | Phone, then name key + ZIP | Large: filter to Type 2 and the target taxonomy codes before matching. Drop NPIs on the deactivation file |
| Public registers (FDIC, NCUA, IRS EO BMF, SAM.gov, EDGAR, NCES) | Every member of a regulated or registered market; details and calls in `market-definition-recipes.md`, Public registries | Name, address, often a website | API or bulk file | Domain, then name key + ZIP | The register is the denominator: report coverage against it rather than against Chapman |
| GitHub organizations | Developer-facing companies. `GET /organizations` lists organizations by creation order, paged only with `since` and up to 100 per page; `GET /orgs/{org}` returns profile fields such as `blog`, `location` and `email` | Org login, `blog` URL, location | GitHub REST API | Domain from `blog` | Many organizations are open-source projects or personal groups. Keep orgs with a company website in `blog` |

### Import procedure

1. Normalize the import to the business schema (section 3): name key, E.164 phone, 5-digit ZIP, registrable domain.
2. Dedupe the import against itself with the same key order.
3. Match it against the TAM file with the passes in section 4: domain first, then phone, then name key + postal code, then name key + street.
4. Classify every import row as `matched` (append the list name to `import_sources` on the TAM row), `new` or `held`.
5. A `new` row joins the TAM only if it fits the market definition, carries a domain or an E.164 phone, and is current (license unexpired, listed this year). Everything else goes to `tam-review-[market]-[date].csv` with a reason.
6. Log one reconciliation row per import: rows after its own dedupe = matched + new + held.

## 10. Found-in-N confidence tiers

`found_in` counts the independent origins that hold an account: each list source in `source` (`local_db`, `lead_db`, `ecom_db`, `apollo`, `maps`, `yelp`, `angi`, `store_leads`, `techstack`, `user_upload` lists counted once each by name in `import_sources`). Enrichment values (`email_finder`, `mobile_finder`, `website_finder`, `people_finder`) do not count, because they found a contact for an account that was already in the file.

| found_in | Confidence label | What it tells you | Action |
|-|-|-|-|
| 3 or more | High | Independent lists agree the business exists and fits | First in sequencing order; safe base for TAM counts in a board deck |
| 2 | Medium | Two lists agree | Normal handling |
| 1 | Low | One list holds it; closed, moved or misclassified businesses sit here more often | Cheap existence check before paid enrichment: website resolves, or a Maps re-probe of a sample; report the Low share next to every TAM number |

The labels name the count; no published rate says how often a Low account is closed or misfit. Check on the user's file: take a sample of Low and High accounts, check by hand whether each business is open and fits, and compare the two hit rates. If they match, the label adds nothing for that market.

## 11. Source-overlap report

A required section of the TAM report (`## Source Overlap`). `scripts/check-output.py` checks that the found-in-N rows sum to the final account count, that each confidence label matches its N, and that each import reconciles.

Template:

```markdown
## Source Overlap

| Found in N sources | Confidence | Accounts | Share of TAM |
|-|-|-|-|
| 1 | Low | [fill] | [fill]% |
| 2 | Medium | [fill] | [fill]% |
| 3 | High | [fill] | [fill]% |
| 4 or more | High | [fill] | [fill]% |

| Outside source | Rows after own dedupe | Dedupe key | Matched to file | New accounts added | Held for review |
|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |
```

Example with illustrative numbers (HVAC contractors in Texas, the same file as `examples/worked-example.md`):

| Found in N sources | Confidence | Accounts | Share of TAM |
|-|-|-|-|
| 1 | Low | 3,184 | 27.4% |
| 2 | Medium | 4,678 | 40.3% |
| 3 | High | 2,900 | 25.0% |
| 4 | High | 820 | 7.1% |
| 5 | High | 40 | 0.3% |

| Outside source | Rows after own dedupe | Dedupe key | Matched to file | New accounts added | Held for review |
|-|-|-|-|-|-|
| TDLR Air Conditioning Contractors license file | 9,412 | Phone, then name key + ZIP | 7,830 | 0 | 1,582 |
| ACCA contractor locator, five metros | 702 | Domain, then phone | 640 | 0 | 62 |

How to read it: 83.2% of active Texas AC contractor licensees (7,830 of 9,412) are already in the file. That is a second coverage check from a registry that lists every active licensee, with or without a website, and it sits below the 94.1% capture-recapture figure, which supports treating the capture-recapture number as an upper bound. The 1,582 unmatched licensees go to the review file and a Maps probe next cycle.

Check the arithmetic: accounts by N sum to 11,622, and sum of N x accounts (3,184 + 9,356 + 8,700 + 3,280 + 200 = 24,720) equals the source memberships (16,250 from ScraperCity sources + 7,830 + 640 import matches).

## 12. Source yield

Write one row per source after the dedupe passes and imports, so the next refresh buys only what adds accounts.

| Column | Rule |
|-|-|
| Accounts contributed | Final accounts whose `source` or `import_sources` includes this source |
| Unique accounts | For ScraperCity sources, the single-source rows in the Source Mix (accounts no other list source found). For an outside list, the new accounts it added |
| Cost | Wallet spend on this source in the run ($0.00 for database pulls inside the plan) |
| Cost per unique account | Cost divided by unique accounts |
| Next refresh | Keep, narrow (fewer metros or terms) or drop |

Decision rule, when the user's deal inputs set a Tier 3 spend ceiling (`account-scoring-and-tiers.md` section 6): keep a paid source when its cost per unique account is below it; narrow it to the metros where it found unique accounts when it is above; drop it when narrowing still leaves it above the ceiling. With no ceiling, report the cost per unique account and ask the user for the keep or drop call. A free registry that adds nothing still earns its place as the coverage check. Unique accounts can never exceed accounts contributed, and the unique counts across all sources equal the single-source rows of the Source Mix plus outside-list rows added as new.

Example (the HVAC file):

| Source | Accounts contributed | Unique accounts | Cost | Cost per unique account | Next refresh |
|-|-|-|-|-|-|
| local_db | 8,965 | 4,980 | $0.00 | $0.000 | Keep |
| lead_db | 4,095 | 1,042 | $0.00 | $0.000 | Keep |
| maps | 3,190 | 1,427 | $35.64 | $0.025 | Keep, limited to the 30 gap sub-cities |
| TDLR license file | 7,830 | 0 | $0.00 | none added | Keep as a coverage check |

## Sources

- Montana State University, WILD 502 closed-population estimators: https://www.montana.edu/rotella/documents/502/Closed.pdf
- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- data.census.gov: https://data.census.gov/
- Public Suffix List: https://publicsuffix.org/
- USPS Publication 28, street suffix abbreviations: https://pe.usps.com/text/pub28/28apc_002.htm
- ScraperCity catalog (Maps, Yelp, Angi parameters and prices): references/scrapercity-catalog.md
- AHR Expo: https://www.ahrexpo.com/
- Texas Department of Licensing and Regulation, license data files: https://www.tdlr.texas.gov/LicenseSearch/licfile.asp
- TDLR license listing file format: https://www.tdlr.texas.gov/dbproduction2/lrformat.txt
- ACCA, Find a Contractor: https://www.acca.org/find-a-contractor
- Inc. 5000: https://www.inc.com/inc5000
- G2 categories: https://www.g2.com/categories
- Crunchbase: https://www.crunchbase.com/
- GitHub REST API, organizations: https://docs.github.com/en/rest/orgs/orgs
- CMS, NPPES downloadable files (monthly, weekly and deactivation files, checked 2026-10-13): https://download.cms.gov/nppes/NPI_Files.html
