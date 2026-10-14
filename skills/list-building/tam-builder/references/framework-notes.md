# Framework Notes: TAM Builder

## Routing table

| You are about to | Open |
|-|-|
| Write the market definition and filters for each source | `market-definition-recipes.md` |
| Decide where to run Maps, split a metro, estimate coverage, run the dedupe passes | `coverage-and-dedupe-playbook.md` |
| Import a licensing file, association directory, exhibitor list, Inc. 5000, G2, Crunchbase, job board or GitHub list | `coverage-and-dedupe-playbook.md` section 9 |
| Tier accounts by how many sources hold them, write the source-overlap and source-yield reports | `coverage-and-dedupe-playbook.md` sections 10 to 12 |
| Score accounts, cut Tier 1 to 3 by capacity, set spend ceilings, backtest, apply tier movers, run the quarter-end read | `account-scoring-and-tiers.md` |
| Count a bank, credit union, nonprofit, federal contractor, public company or school market | `market-definition-recipes.md`, Public registries |
| Pick sources and an outside list by vertical | `market-definition-recipes.md`, Sources by vertical |
| Map columns, normalize names and domains, pick a surviving record | `references/list-quality-standard.md` (shared) |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |
| Check database access and the daily allowance | `references/scrapercity-platform.md` (shared) |

## Sources and what each contributes

### US Census Bureau: County Business Patterns, Nonemployer Statistics and NAICS

County Business Patterns is an annual Census series of establishment counts, employment and payroll by industry and geography; the latest data year is 2023, released June 26, 2025 (checked 2026-10-13). Nonemployer Statistics counts businesses with no paid employees; its latest data year is 2024. NAICS is the industry code system both use. The Census API now asks for a free key; data.census.gov needs none. Three uses here:

1. Benchmark. Pull the establishment count for the market's NAICS code and state from data.census.gov. If the deduped file is far below it, coverage is low; far above, the definition is too loose or includes non-employer businesses.
2. Gap targeting. CBP county counts show where establishments cluster, which tells you which metros deserve Maps gap fill.
3. Owner-only markets. When the definition includes one-person shops, CBP plus NES bounds the market; most nonemployer businesses have no website, so expect the file to sit far below that sum.

Limits to state in every report: CBP excludes businesses without paid staff; it lags by about two years; a NAICS code rarely matches a sales market one to one (238220 mixes plumbers and HVAC contractors).

### Lincoln-Petersen and Chapman estimators

Capture-recapture comes from wildlife biology. Mark n1 animals, later catch n2, count m that were marked; total population is about n1 x n2 / m. Chapman's version, (n1 + 1)(n2 + 1) / (m + 1) - 1, reduces bias for small samples. Two independent data sources covering one metro play the role of the two catches; the overlap after dedupe is m.

Assumptions that do not hold perfectly for business data: a closed population (businesses open and close), equal catchability (both sources favor businesses with websites and reviews), independence (sources may share upstream signals). Because catchability is unequal in the same direction, the population estimate is a floor and the coverage share is a ceiling. Report it as a range check next to a registry match.

### April Dunford, best-fit segment

Dunford's positioning work defines the target market as the segment that cares most about the product's differentiated value. Applied here: a TAM for "small businesses" is useless; a TAM for "HVAC contractors in Texas with 3+ trucks" is plannable. Size the best-fit segment first and widen only on request.

### Public Suffix List

The registrable domain (one label plus the public suffix) is the most stable company key across sources. The Public Suffix List is the reference for where the suffix ends (`co.uk`, `com.au`). Platform hosts (facebook.com, business.site, linktr.ee) are not company domains and get blanked before dedupe.

### License files and other outside lists

A state license file is the nearest thing to a census for a licensed trade, and it does not depend on a website or reviews. Texas TDLR, for example, publishes CSV license files with business name, address, ZIP, phone and expiration date. Matching it against the file gives a second coverage figure that does not share the online-presence bias of capture-recapture. Exhibitor lists, Inc. 5000, G2 categories, Crunchbase, job boards and GitHub organizations each cover a slice; they raise confidence on the accounts they confirm and add accounts only after a fit check. The found-in-N labels (3 or more sources High, 2 Medium, 1 Low) name the count; a hand check of Low and High accounts on the user's file shows what each level means.

### Public registers for regulated and registered markets

Banks (FDIC BankFind API, no key; 4,220 active insured institutions in the 2026-10-09 index), credit unions (NCUA quarterly Call Report files, latest June 2026), nonprofits (IRS EO BMF extract, 1,964,958 records posted 2026-09-08), federal contractors (SAM.gov Entity and Extract APIs with a free key), public companies (EDGAR by SIC code) and schools (NCES Common Core of Data) each have a register that lists every member. For those markets the register replaces CBP as the benchmark and replaces capture-recapture as the coverage check: coverage is matched rows divided by register rows.

### Win-rate lift, capacity tiers and the spend ceiling

Scoring uses lift (win rate with a trait divided by the overall win rate) converted to points as 10 x log2(lift), capped at plus or minus 10, and only on columns filled on at least the share of SAM rows the user sets. The log keeps a 2x lift and a 0.5x lift symmetric (plus and minus 10). Tiers are cut by how many accounts each rep can work at each depth, using Alex Berman's segment, account and person personalization levels for Tiers 3, 2 and 1. David Skok's guidance that acquisition cost should be recovered within 12 months sets the spend ceiling per worked account when the user supplies ACV, margin and win rates: first-year gross profit times the win rate per worked account. A mover lifts an account for one send cycle, the 30 to 60 days Alex Berman puts between cycles (alexberman.com TAM breakdown, October 2026). No published source sets the fill minimum or the backtest bar, so each is the user's setting and the report records it; a backtest concentration at or below 1.0x means the score is no better than chance.

### TAM, SAM, SOM

Standard market-sizing layers. This skill computes them bottom-up from counted accounts times annual contract value, which is checkable, rather than top-down from industry revenue reports. SOM is always an assumption the user states; the skill does not invent a capture rate.

## What this skill does not do

- It does not pull contacts for every account. TAM files are company-level. Use `decision-maker-finder` on Tier 1 and Tier 2.
- It does not track intent or events. A trigger from `signal-triggered-outbound` lifts an account one tier; it never replaces fit.
- It does not validate emails. If the user wants to email the TAM, run `cold-email-list` on the chosen slice.

## Sources

- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- US Census Bureau, NAICS: https://www.census.gov/naics/
- data.census.gov: https://data.census.gov/
- Montana State University, WILD 502 notes on closed-population abundance (Lincoln-Petersen, Chapman): https://www.montana.edu/rotella/documents/502/Closed.pdf
- April Dunford, A quickstart guide to positioning: https://www.aprildunford.com/post/a-quickstart-guide-to-positioning
- Public Suffix List: https://publicsuffix.org/
- Texas Department of Licensing and Regulation, license data files: https://www.tdlr.texas.gov/LicenseSearch/licfile.asp
- US Census Bureau, County Business Patterns datasets (2023 data year, June 2025): https://www.census.gov/programs-surveys/cbp/data/datasets.html
- US Census Bureau, Nonemployer Statistics: https://www.census.gov/programs-surveys/nonemployer-statistics.html
- CMS, NPPES downloadable files: https://download.cms.gov/nppes/NPI_Files.html
- David Skok, SaaS Metrics 2.0: https://www.forentrepreneurs.com/saas-metrics-2/
- Alex Berman, Cold email templates: https://alexberman.com/cold-email-templates
- FDIC, BankFind Suite API: https://api.fdic.gov/banks/institutions
- NCUA, Call report quarterly data: https://ncua.gov/analysis/credit-union-corporate-call-report-data/quarterly-data
- IRS, EO BMF extract: https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf
- GSA, SAM.gov Entity Management API: https://open.gsa.gov/api/entity-api/
- NCES, Common Core of Data files: https://nces.ed.gov/ccd/files.asp
- Alex Berman, Map your market, skip the follow-ups (one email per person per cycle, 30 to 60 days between cycles, October 2026): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
