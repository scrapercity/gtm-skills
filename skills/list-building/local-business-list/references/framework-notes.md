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
| Check CAN-SPAM, TCPA and country rules | `references/outbound-compliance-primer.md` (shared) |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### US Census Bureau, County Business Patterns

CBP publishes annual establishment counts by NAICS industry code for every county. It gives an outside number to compare against: if the database and scrapes together find far fewer dental offices (NAICS 621210) in a county than CBP reports, coverage there is low and a scrape or a ZIP-level split is due. CBP counts establishments with paid employees, so sole proprietors without staff are missing from it; treat it as a rough benchmark, not a ceiling. CBP data lags by about two years.

### Google Maps Platform, Places Text Search

Google's developer documentation states that Text Search returns a maximum of 60 results across all pages for one query, a limit Google says may change. Any single search over a large area therefore returns a slice. This skill works without the exact number: it splits areas into sub-cities or boxes, caps `maxCrawledPlacesPerSearch`, and splits further whenever a run returns at its cap.

### FTC, CAN-SPAM

The FTC guide says CAN-SPAM makes no exception for business-to-business email. Local business email needs honest headers and subject lines, a valid physical postal address, a clear opt-out, and opt-outs honored within 10 business days.

### FCC, TCPA

The Local Business Database can return `contact_mobile` for named contacts. Marketing texts and autodialed or prerecorded calls to mobiles need prior express written consent under 47 CFR 64.1200. Mobiles on this list are for manual calls after a Do Not Call scrub, or are left unused.

### Mailbox providers: Google, Yahoo, Microsoft

Google's sender guidelines (February 2024) set a spam rate ceiling of 0.3% with a target under 0.1%; Yahoo asks senders to remove invalid recipients; Microsoft's May 2025 rules for high-volume senders list removing invalid addresses as expected practice. Small-business domains often sit on hosting that accepts all mail, so the catch-all share on local lists runs high; the catch-all file and its 10% daily cap come from `references/deliverability-primer.md`.

### Alex Berman, niche first

In his Lean B2B interview Berman describes testing about 100 cold emails per segment and scoring segments before committing, and his offer article argues that the list should be built after the offer, around one niche and one result. Applied here: the CSV covers every business in the category and area, and the next step always names one sub-segment (a sub-city, practices with a named contact, a rating band) for the first send.

## House standards used in this skill (2026-10)

| Standard | Value | Replace when |
|-|-|-|
| Gap threshold for scraping a sub-area | Email coverage 5+ points under the metro average | You have coverage data from three metros |
| Maps cap per term on the first pass | 40 | Runs routinely finish under the cap |
| Role addresses on local lists | Kept | Bounce or complaint data says otherwise for a vertical |
| Catch-all share of daily volume | 10% or less | Per `deliverability-primer.md` |

## Sources

- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- Google Maps Platform, Text Search (New): https://developers.google.com/maps/documentation/places/web-service/text-search
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- 47 CFR 64.1200: https://www.law.cornell.edu/cfr/text/47/64.1200
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Lean B2B, Alex Berman on B2B market segments: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- Alex Berman, Cold email doesn't fail, your offer does: https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
