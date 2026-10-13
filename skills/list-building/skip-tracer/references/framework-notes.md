# Framework Notes: Skip Tracer

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Decide whether the job may run at all | `fcra-and-contact-compliance.md` sections 1 and 2 |
| Pick the search for each row and set `max_results` | `identifier-strategy-and-match-scoring.md` sections 1 and 2 |
| Score a match and assign a band | `identifier-strategy-and-match-scoring.md` section 3 |
| Handle LLC owners, trusts, banks, deceased owners | `identifier-strategy-and-match-scoring.md` section 5 |
| Price, pilot, batch, chain from Distress List | `skip-trace-runbook.md` |
| Call homeowners, or collect debts | `fcra-and-contact-compliance.md` sections 3 to 5 |
| State wholesaling and foreclosure purchase rules | `scrapercity-real-estate-data` skill, `references/compliance-guide.md` there |
| Quote a price | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### Fair Credit Reporting Act and FTC guidance

The FCRA (15 U.S.C. 1681 and following) governs consumer reports: communications by a consumer reporting agency bearing on a person's credit, character, reputation or characteristics, used or expected to be used to decide eligibility for credit, insurance, employment or other listed purposes. Users of consumer reports need a permissible purpose (15 U.S.C. 1681b) and must give adverse action notices when a report leads to a denial. The FTC's guidance for landlords applies the same rules to tenant screening.

Applied rule: this skill's results are prospecting and contact data. They do not feed rent, hire, lend, insure or credit decisions, and the report says so in its first section.

### FTC enforcement against people-search sites

- Spokeo (June 2012): $800,000 civil penalty. The FTC said Spokeo marketed profiles to human resources, recruiting and background screening companies, which made it a consumer reporting agency, and that it did not verify permissible purpose or report accuracy.
- Instant Checkmate and TruthFinder (September 2023): $5.8 million civil penalty. The FTC alleged the companies operated as consumer reporting agencies without accuracy procedures, provided reports to users without a permissible purpose, and implied criminal records where there was only a traffic ticket.

Applied rule: the way data is used decides whether the FCRA applies. Keep skip-trace output out of screening workflows entirely, and never describe a match as a "background check".

### CFPB Regulation F

12 CFR 1006.10 limits how debt collectors seek location information (a consumer's home address and phone, or place of employment) from third parties: the collector gives an individual name, says it is confirming or correcting location information, and names the employer only if asked. The debt stays unmentioned, postcards and debt language on envelopes are banned, and each third party is generally contacted once. Applied rule: collectors using this skill call third parties only with a location script.

### TCPA, FCC rules and the TSR

- 47 U.S.C. 227: consent for autodialed, artificial or prerecorded voice calls to wireless numbers; $500 per violation in private suits, up to triple if willful.
- 47 CFR 64.1200: calling hours 8 a.m. to 9 p.m. local, internal do-not-call lists (requests honored within 10 business days, kept 5 years), DNC coverage of wireless numbers, prior express written consent defined.
- FTC TSR: sync with the National DNC Registry at least every 31 days; an established business relationship lasts 18 months after a transaction or 3 months after an inquiry, and a skip-traced owner has neither. Penalties up to $53,088 per violation (2025 level, unchanged for 2026).

Applied rule: manual live calls only, Registry numbers removed, no texts without consent.

### CFPB Regulation O

12 CFR 1015 covers mortgage assistance relief services: offers to stop a foreclosure, modify a loan, or negotiate with a lender for the owner. It bans advance fees and requires disclosures. Applied rule: pre-foreclosure outreach makes purchase or listing offers; scripts do not promise to stop the foreclosure.

### USPS Publication 28

The Postal Service's addressing standard (street suffix abbreviations such as AVE, LN, DR; secondary unit designators such as APT, STE, UNIT; two-letter state codes; ZIP or ZIP+4). Applied rule: addresses are normalized to this format before any search, and rows without a ZIP are fixed before they cost money.

### ScraperCity terms and platform facts

`references/scrapercity-platform.md` records that People Finder, skip tracing, Property Lookup and Criminal Records return public-record data, that the user is responsible for a lawful basis and legal review, and that this repo treats results as prospecting and research data only.

## What this skill does not do

- Run Criminal Records searches. A criminal record check for a tenant or hire is an FCRA use; this skill has no reason to call `search_criminal_records`.
- Locate a person for a personal reason (a former partner, a relative who cut contact).
- Decide whether a specific dialer is an autodialer, or whether a state wholesaling statute applies. Counsel decides.

## Sources

- FCRA, 15 U.S.C. 1681 (FTC page with statute text): https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act
- FTC, Using consumer reports: what landlords need to know: https://www.ftc.gov/business-guidance/resources/using-consumer-reports-what-landlords-need-know
- FTC Spokeo settlement (summary): https://www.hunton.com/privacy-and-cybersecurity-law-blog/ftc-fines-data-broker-800000-alleged-fcra-violations
- FTC Instant Checkmate and TruthFinder settlement (summary): https://www.consumerfinancemonitor.com/2023/09/15/ftc-settles-with-background-report-companies-for-fcra-violations-and-deceptive-acts/
- CFPB Regulation F, 1006.10: https://www.consumerfinance.gov/rules-policy/regulations/1006/10/
- 47 U.S.C. 227: https://www.law.cornell.edu/uscode/text/47/227
- 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FTC, Q&A about DNC provisions of the TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- CFPB Regulation O, 12 CFR 1015: https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- USPS Publication 28: https://pe.usps.com/text/pub28/welcome.htm
