# Framework Notes: Local Business List

Which sources shape this skill, what each one contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Choose keywords, exclusions and the Website Finder title for a vertical | `local-category-recipes.md` |
| Split a metro, a state or a dense city core | `metro-split-and-geo-recipes.md` sections 1-3 |
| Decide which sub-areas get a Maps or Yelp scrape | `metro-split-and-geo-recipes.md` section 4 |
| Page the database, dedupe scrape rows against it, handle chains | `metro-split-and-geo-recipes.md` sections 5-6 |
| Name columns, normalize phones, ZIPs and domains | `references/list-quality-standard.md` sections 2b and 3 (shared) |
| Route catch-all rows and set bounce stop lines | `references/deliverability-primer.md` (shared) |
| Check coverage against the NPI Registry or a state license file | `coverage-segments-and-handoff.md` section 1 |
| Name the owner, or screen out chains and DSOs | `coverage-segments-and-handoff.md` sections 1b and 1c |
| Tag segments, set up call outcomes, map sequencer and dialer columns | `coverage-segments-and-handoff.md` sections 2 to 4 |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### US Census Bureau, County Business Patterns

CBP publishes annual establishment counts by NAICS industry code for every county. It gives an outside number to compare against: if the database and scrapes together find far fewer dental offices (NAICS 621210) in a county than CBP reports, coverage there is low and a scrape or a ZIP-level split is due. CBP counts establishments with paid employees, so sole proprietors without staff are missing from it; treat it as a rough benchmark, not a ceiling. CBP data lags by about two years.

### Google Maps Platform, Places Text Search

Google's developer documentation states that Text Search returns a maximum of 60 results across all pages for one query, a limit Google says may change. Any single search over a large area therefore returns a slice. This skill works without the exact number: it splits areas into sub-cities or boxes, caps `maxCrawledPlacesPerSearch`, and splits further whenever a run returns at its cap.

### CMS NPI Registry and state licensing boards

The NPI Registry API returns organization (type 2) providers by taxonomy, city and state, with the legal organization name, the authorized official and title, the practice location address and phone, 200 records per page and at most 1,200 per query because `skip` stops at 1,000 (tested 2026-10-13); CMS also publishes a monthly full file and a weekly incremental file. Florida's DBPR publishes its construction licensee file as a CSV with license class, county code and original licensure date. Applied rules: match these lists against the pool per sub-area to measure coverage, scrape where coverage is under the target the user sets, and tag licenses issued inside the window the user sets `new_license`.

### State entity registries and group announcements

Arizona's Corporation Commission eCorp search takes an entity name or a principal name, so the legal name on an NPI record leads to the people behind the entity. Colorado's register files no officers or managers (Topograph's Colorado documentation), so the step depends on the state. Groups that support practices can leave the practice name in place: Heartland Dental lists newly supported offices under their own names in its monthly growth spotlight, and Becker's Dental Review (Oct 2025) described a practice that "operates as Chiquita Dental Care and is supported by" Heartland. Applied rule: the independence screen uses group lists and homepage text, not location counts alone.

### Mailbox providers: Google, Yahoo, Microsoft

Google's sender guidelines (February 2024) set a spam rate ceiling of 0.3% with a target under 0.1%; Yahoo asks senders to remove invalid recipients; Microsoft's May 2025 rules for high-volume senders list removing invalid addresses as expected practice. Small-business domains often sit on hosting that accepts all mail, so the catch-all share on local lists runs high; the catch-all file runs as its own campaign and pauses at 2% hard bounces over 200 sends, per `references/deliverability-primer.md` (Alex Berman's 2% line, Instantly's 200-send window).

### Alex Berman, niche first

In his Lean B2B interview Berman describes testing about 100 cold emails per segment and scoring segments before committing, and his offer article argues that the list should be built after the offer, around one niche and one result. Applied here: the CSV covers every business in the category and area, and the next step always names one sub-segment (a sub-city, practices with a named contact, a rating band) for the first send.

## Settings the user supplies

| Setting | Used for |
|-|-|
| Gap line against the metro average email coverage | Which sub-cities get a Maps scrape |
| Coverage target against the NPI or license list | Whether a sub-area needs more spend |
| Maps cap per term, 60 or less | Google's 60-result maximum per text search bounds it |
| Segment cutoffs (rating, review count, license age) | Situation tags |
| Chain line (locations per brand that make it a chain) | Independence screen |
| QA sample size and pass line per check | The hand check before handoff |
| Specialists or sub-types in or out | Scope; the default keeps them, tagged |
| Cool-off window for past contacts and `not_interested` | Suppression |

## Sources

- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- CMS, NPPES NPI Registry API: https://npiregistry.cms.hhs.gov/api-page
- CMS, NPPES downloadable files: https://download.cms.gov/nppes/NPI_Files.html
- Florida DBPR, Construction Industry public records: https://www2.myfloridalicense.com/construction-industry/public-records/
- Arizona Corporation Commission, eCorp entity search: https://ecorp.azcc.gov/EntitySearch/Index
- Topograph, Colorado business register: https://docs.topograph.co/essentials/us-colorado
- Heartland Dental, Monthly Growth Spotlight, December 2025: https://blog.heartland.com/heartland-dental-monthly-growth-spotlight-december-2025
- Becker's Dental Review, Oct 7 2025: https://www.beckersdental.com/dso-dpms/florida-dental-practice-leased-to-heartland-sells-for-3m/
- Google Maps Platform, Text Search (New): https://developers.google.com/maps/documentation/places/web-service/text-search
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Lean B2B, Alex Berman on B2B market segments: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- Alex Berman, Cold email doesn't fail, your offer does: https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
