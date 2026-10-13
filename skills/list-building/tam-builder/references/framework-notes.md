# Framework Notes: TAM Builder

## Routing table

| You are about to | Open |
|-|-|
| Write the market definition and filters for each source | `market-definition-recipes.md` |
| Decide where to run Maps, split a metro, estimate coverage, run the dedupe passes | `coverage-and-dedupe-playbook.md` |
| Map columns, normalize names and domains, pick a surviving record | `references/list-quality-standard.md` (shared) |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |
| Check database access and the daily allowance | `references/scrapercity-platform.md` (shared) |

## Sources and what each contributes

### US Census Bureau: County Business Patterns and NAICS

County Business Patterns is an annual Census series of establishment counts, employment and payroll by industry and geography; at the time of writing the latest data year is 2023. NAICS is the industry code system CBP uses. Two uses here:

1. Benchmark. Pull the establishment count for the market's NAICS code and state from data.census.gov. If the deduped file is far below it, coverage is low; far above, the definition is too loose or includes non-employer businesses.
2. Gap targeting. CBP county counts show where establishments cluster, which tells you which metros deserve Maps gap fill.

Limits to state in every report: CBP counts establishments with paid employees, so sole proprietors without staff are excluded; it lags by about two years; a NAICS code rarely matches a sales market one to one (238220 mixes plumbers and HVAC contractors).

### Lincoln-Petersen and Chapman estimators

Capture-recapture comes from wildlife biology. Mark n1 animals, later catch n2, count m that were marked; total population is about n1 x n2 / m. Chapman's version, (n1 + 1)(n2 + 1) / (m + 1) - 1, reduces bias for small samples. Two independent data sources covering one metro play the role of the two catches; the overlap after dedupe is m.

Assumptions that do not hold perfectly for business data: a closed population (businesses open and close), equal catchability (both sources favor businesses with websites and reviews), independence (sources may share upstream signals). Because catchability is unequal in the same direction, the estimate is a floor, and real coverage is lower than the estimate implies. Report it as a range check, not a census.

### April Dunford, best-fit segment

Dunford's positioning work defines the target market as the segment that cares most about the product's differentiated value. Applied here: a TAM for "small businesses" is useless; a TAM for "HVAC contractors in Texas with 3+ trucks" is plannable. Size the best-fit segment first and widen only on request.

### Public Suffix List

The registrable domain (one label plus the public suffix) is the most stable company key across sources. The Public Suffix List is the reference for where the suffix ends (`co.uk`, `com.au`). Platform hosts (facebook.com, business.site, linktr.ee) are not company domains and get blanked before dedupe.

### TAM, SAM, SOM

Standard market-sizing layers. This skill computes them bottom-up from counted accounts times annual contract value, which is checkable, rather than top-down from industry revenue reports. SOM is always an assumption the user states; the skill does not invent a capture rate.

## What this skill does not do

- It does not pull contacts for every account. TAM files are company-level. Use `decision-maker-finder` on a slice.
- It does not validate emails. If the user wants to email the TAM, run `cold-email-list` on the chosen slice.

## Sources

- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- US Census Bureau, NAICS: https://www.census.gov/naics/
- data.census.gov: https://data.census.gov/
- Montana State University, WILD 502 notes on closed-population abundance (Lincoln-Petersen, Chapman): https://www.montana.edu/rotella/documents/502/Closed.pdf
- April Dunford, A quickstart guide to positioning: https://www.aprildunford.com/post/a-quickstart-guide-to-positioning
- Public Suffix List: https://publicsuffix.org/
