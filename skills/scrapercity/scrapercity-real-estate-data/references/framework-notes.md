# Framework Notes: ScraperCity Real Estate Data

Which sources shape this skill, what each contributes, and which file to open for each job.

## Routing table

| You need | Open |
|---|---|
| Inputs, outputs, limits and CLI flags for a tool | `references/tool-reference.md` |
| A plan for a specific persona (agent, wholesaler, investor, lender, CRE broker, business broker) | `references/workflow-playbooks.md` |
| Rules for calling, texting, mailing or emailing owners; FCRA boundary; state wholesaling laws | `references/compliance-guide.md` |
| Catalog prices and schemas | `references/scrapercity-catalog.md` (shared) |
| ScraperCity's own compliance boundary for public-records tools | `references/scrapercity-platform.md` (shared) |
| Cross-skill TCPA, DNC, CAN-SPAM, CASL and GDPR basics | `references/outbound-compliance-primer.md` (shared) |

## Sources and contributions

### ScraperCity tools (primary for behavior and price)

- `references/scrapercity-catalog.md`, generated from npm `scrapercity` 1.0.17, gives the six tools, their inputs and prices: Zillow Agents $0.029 per agent; Property Lookup $0.15 per property plus $0.10 for owner contact; Distress List $0.05 per property; Crexi $0.029 per property; BizBuySell $0.0099 per listing; People Finder $0.0199 per result with zero-match searches billed as one result.
- `bin/cli.mjs` gives the CLI commands `zillow-agents`, `distress-list`, `crexi`, `bizbuysell` and `people-find`, and their flags. The CLI has no property lookup command in this version.
- `AGENT_DOCS.txt` says Property Lookup needs a full address with city, state and ZIP.
- The catalog entry for Crexi lists the three URL forms and the 400 for a map view with no location.
- ScraperCity product pages list the Zillow Agents output fields (name, phone, email, screen name, profile URL, specialties, languages, active listings, recent sales, rating, reviews, license number), the Crexi sample fields (property, address, type, price, square footage, broker name, phone and firm, cap rate, NOI and others) and the BizBuySell sample fields (title, location, price, EBITDA, revenue, cash flow, broker name, phone and firm, year established, employees, reason for selling and others).
- `references/scrapercity-platform.md`: People Finder, skip tracing and Property Lookup return public-record data; the user is responsible for a lawful basis; the skills treat these results as prospecting data only, never for employment, tenant, credit or insurance decisions.

### Telephone Consumer Protection Act, 47 U.S.C. 227 (FCC)

Autodialed or artificial or prerecorded voice calls to wireless numbers need the called party's prior express consent. A private plaintiff can recover the greater of actual loss or $500 per violation, and a court may triple it for willful or knowing violations. Someone who gets more than one call in 12 months in violation of the Do Not Call rules can sue for up to $500 per violation. Contribution: the reason owner mobiles never go into an autodialer or a texting tool without consent.

### 47 CFR 64.1200 (FCC rules)

No telephone solicitation to a residential subscriber before 8 a.m. or after 9 p.m. at the called party's location. Registry numbers are protected until the consumer removes them. Prior express written consent is a signed written agreement with clear disclosure. Several provisions treat text messages as calls. Contribution: calling windows and the consent definition in the compliance gate.

### FTC Telemarketing Sales Rule and the Do Not Call Registry

Lists must be scrubbed against the Registry at least every 31 days. An established business relationship lasts 18 months after the last purchase or transaction, or 3 months after an inquiry. Most calls to businesses are exempt from the DNC provisions. Penalties reach $53,088 per violation. Contribution: scrub cadence, and why Crexi and BizBuySell broker lists route differently from homeowner lists.

### Fair Credit Reporting Act (FTC guidance)

Tenant background checks are consumer reports; using one for a housing decision triggers permissible purpose certification and adverse action notices. Contribution: the hard line that People Finder and Property Lookup results never feed tenant, credit, employment or insurance decisions.

### CFPB Regulation O (12 CFR 1015)

A mortgage assistance relief provider is anyone offering to arrange relief such as stopping a foreclosure or modifying a loan. No fee before the consumer signs the lender's written agreement, and communications must state the company is not affiliated with the government or the lender. Contribution: the script rule that pre-foreclosure outreach makes purchase offers, not foreclosure-rescue promises, unless the user complies with Regulation O.

### State wholesaling and equity purchase laws

- Illinois Real Estate License Act: a pattern of business means two or more deals in any 12-month period, so wholesaling more than one property a year needs a license.
- Oklahoma Predatory Real Estate Wholesaler Prohibition Act: effective November 1, 2021, wholesalers need a real estate license (Oklahoma Real Estate Commission).
- Pennsylvania Act 52 of 2024: wholesalers are treated as brokers or salespersons, contracts need written disclosures, and the seller can cancel until midnight of the 30th day after signing or conveyance, whichever is first.
- Ohio SB 155: effective March 2, 2026, a wholesaler disclosure form before contract; a homeowner who did not get and sign it can cancel before closing.
- South Carolina Real Estate Commission guidance: marketing the underlying property for compensation is brokerage and needs a license.
- California Civil Code 1695.4: an owner selling a residence in foreclosure to an equity purchaser can cancel until midnight of the fifth business day after signing, or 8 a.m. on the sale date if earlier.
- Florida Telephone Solicitation Act (amended 2023): consent rules for automated calls and texts, with a 15-day notice-and-cure window for texts after the recipient replies STOP.

Contribution: the state column in the compliance check. These are summaries, not legal advice; the plan always tells the user to confirm with a local real estate attorney.

## How the sources combine

1. The catalog decides which tool and what it costs.
2. The channel decides which federal rule applies (TCPA and TSR for calls and texts, CAN-SPAM for email).
3. The state decides which wholesaling or equity purchase rule applies.
4. The use decides whether FCRA is in play (if yes, stop).

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/zillow-agents-scraper
- https://scrapercity.com/crexi-scraper
- https://scrapercity.com/bizbuysell-scraper
- https://www.law.cornell.edu/uscode/text/47/227
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr
- https://www.ftc.gov/business-guidance/resources/using-consumer-reports-what-landlords-need-know
- https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- https://oklahoma.gov/orec/resources/blog/wholesale-act.html
- https://www.barley.com/act-52-imposes-new-regulations-on-real-estate-wholesaling-in-pennsylvania/
- https://www.ohiorealtors.org/blog/2306/real-estate-wholesaling-legislation-takes-effect/
- https://www.llr.sc.gov/re/News/Wholesaling-Assignment-of-Contracts-Guidance.pdf
- https://rejournals.com/real-estate-wholesaling-in-illinois-an-investment-strategy-under-scrutiny/
- https://california.public.law/codes/civil_code_section_1695.4
- https://www.mcguirewoods.com/client-resources/alerts/2023/5/pro-business-amendments-to-floridas-mini-tcpa-now-in-effect
