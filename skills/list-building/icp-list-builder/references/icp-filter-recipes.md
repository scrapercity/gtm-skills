# ICP Filter Recipes for `query_lead_database`

37 starting filter sets, grouped by the seller's market. Each recipe is a JSON body for `query_lead_database` with `limit: 1` (the count call). Change `limit` to 100 and add `after` for the pull.

## How to use these recipes

1. Pick the recipe whose buyer and segment are closest to the user's example customers.
2. Replace the employee band, keywords and geography with the traits from SKILL.md step 1.
3. Run the count. If it returns 0, remove `industry` first: industry labels in the database may be spelled differently from the ones written here. `keywords` is the more forgiving filter.
4. Read the returned rows before pulling. Tighten `notTitle` or `notKeywords` with the words behind any off-target row.

Title strings are partial match and comma separated. `notTitle` excludes any title containing one of its terms. Full synonym and exclusion sets live in `title-synonyms-and-exclusions.md`.

Parameter types (from the tool schema): `title`, `notTitle`, `city`, `companyName`, `companyDomain`, `companyCity` are strings. `industry`, `country`, `state`, `seniority`, `department`, `keywords`, `companyCountry`, `companyState`, `notKeywords`, `notIndustry` are arrays. `minEmployees`, `maxEmployees`, `revenueMin`, `revenueMax`, `limit`, `page` are numbers. `after` is a string.

## A. Selling to software companies

### A1. Sales leaders at growth-stage SaaS (sales tools, enablement, data)

```json
{"title": "VP Sales, Vice President of Sales, VP of Sales, Head of Sales, Chief Revenue Officer, CRO, SVP Sales",
 "notTitle": "assistant, intern, former, retired, advisor, board, engineer, enablement, operations, inside sales rep",
 "keywords": ["saas", "b2b"], "minEmployees": 50, "maxEmployees": 200,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### A2. Founders at seed and Series A SaaS (agencies, dev shops, fractional execs)

```json
{"title": "Founder, Co-Founder, CEO, Chief Executive Officer",
 "notTitle": "assistant, former, advisor, investor, board, emeritus",
 "keywords": ["saas", "software"], "minEmployees": 5, "maxEmployees": 50,
 "country": ["United States", "Canada"], "hasEmail": true, "limit": 1}
```

### A3. RevOps owners (CRM consultants, data tools)

```json
{"title": "Revenue Operations, RevOps, Sales Operations, Head of Sales Ops, Director of Revenue Operations",
 "notTitle": "assistant, intern, analyst, coordinator, former",
 "keywords": ["saas"], "minEmployees": 100, "maxEmployees": 1000,
 "seniority": ["director", "vp"], "country": ["United States"], "hasEmail": true, "limit": 1}
```

### A4. Engineering leaders at mid-size software firms (dev tools, cloud cost, QA)

```json
{"title": "VP Engineering, Vice President of Engineering, Head of Engineering, CTO, Chief Technology Officer, Director of Engineering",
 "notTitle": "assistant, intern, former, sales engineer, solutions engineer, field",
 "department": ["engineering"], "keywords": ["software", "saas"],
 "minEmployees": 50, "maxEmployees": 500, "country": ["United States"], "hasEmail": true, "limit": 1}
```

### A5. Security leaders (security services, compliance automation)

```json
{"title": "CISO, Chief Information Security Officer, VP Security, Head of Security, Director of Information Security",
 "notTitle": "assistant, intern, former, physical security, guard, loss prevention",
 "keywords": ["saas", "fintech", "healthtech"], "minEmployees": 200, "maxEmployees": 2000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### A6. Marketing leaders at B2B SaaS (content, paid media, ABM)

```json
{"title": "VP Marketing, Vice President of Marketing, Head of Marketing, CMO, Chief Marketing Officer, Head of Demand Generation, Director of Demand Generation",
 "notTitle": "assistant, intern, coordinator, former, product marketing manager, social media",
 "keywords": ["saas", "b2b"], "minEmployees": 30, "maxEmployees": 300,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### A7. Customer success leaders (CS platforms, onboarding services)

```json
{"title": "VP Customer Success, Head of Customer Success, Chief Customer Officer, Director of Customer Success",
 "notTitle": "assistant, intern, former, manager of support, representative, associate",
 "keywords": ["saas"], "minEmployees": 100, "maxEmployees": 1000,
 "country": ["United States", "United Kingdom"], "hasEmail": true, "limit": 1}
```

### A8. Product leaders (research tools, analytics, design agencies)

```json
{"title": "VP Product, Head of Product, Chief Product Officer, CPO, Director of Product",
 "notTitle": "assistant, intern, former, product marketing, product designer, owner of",
 "keywords": ["saas", "software"], "minEmployees": 50, "maxEmployees": 500,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

## B. Selling to professional services

### B1. Marketing agency owners (white-label services, lead gen, software)

```json
{"title": "Founder, Owner, CEO, Managing Director, Principal, President",
 "notTitle": "assistant, former, advisor, freelance, student",
 "keywords": ["marketing agency", "digital marketing", "advertising"],
 "minEmployees": 5, "maxEmployees": 50, "country": ["United States"], "hasEmail": true, "limit": 1}
```

### B2. Accounting firm partners (practice software, outsourced bookkeeping)

```json
{"title": "Managing Partner, Partner, Owner, Founder, CPA, Principal",
 "notTitle": "assistant, intern, former, associate, staff accountant, student",
 "keywords": ["accounting", "cpa", "tax"], "minEmployees": 5, "maxEmployees": 100,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### B3. Law firm managing partners (legal tech, intake services)

```json
{"title": "Managing Partner, Founding Partner, Owner, Principal Attorney, Firm Administrator",
 "notTitle": "assistant, paralegal, intern, former, associate, clerk",
 "keywords": ["law firm", "legal services"], "minEmployees": 5, "maxEmployees": 100,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### B4. IT managed service providers (MSP tools, distribution)

```json
{"title": "Owner, Founder, CEO, President, Managing Director, CTO",
 "notTitle": "assistant, former, technician, help desk, student",
 "keywords": ["managed services", "msp", "it services"], "minEmployees": 5, "maxEmployees": 200,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### B5. Staffing and recruiting firm owners (job boards, ATS, sourcing data)

```json
{"title": "Owner, Founder, CEO, President, Managing Director, VP Recruiting",
 "notTitle": "assistant, intern, former, recruiter, coordinator, sourcer",
 "keywords": ["staffing", "recruiting"], "minEmployees": 10, "maxEmployees": 200,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### B6. Management consulting partners (research, proposal tools)

```json
{"title": "Partner, Managing Partner, Principal, Founder, Managing Director",
 "notTitle": "assistant, intern, former, associate, analyst",
 "keywords": ["consulting", "management consulting"], "minEmployees": 10, "maxEmployees": 500,
 "country": ["United States", "United Kingdom"], "hasEmail": true, "limit": 1}
```

### B7. Architecture and engineering firm principals (BIM, project software)

```json
{"title": "Principal, Partner, Owner, President, Managing Principal, Founder",
 "notTitle": "assistant, intern, former, drafter, designer i, student",
 "keywords": ["architecture", "engineering services"], "minEmployees": 10, "maxEmployees": 250,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

## C. Selling to healthcare and life sciences

### C1. Multi-location dental and medical group operators (DSO services, RCM)

```json
{"title": "CEO, COO, Chief Operating Officer, VP Operations, Director of Operations, Practice Administrator",
 "notTitle": "assistant, intern, former, dental assistant, hygienist, receptionist",
 "keywords": ["dental", "medical group", "healthcare services"], "minEmployees": 50, "maxEmployees": 1000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### C2. Hospital and health system IT (interoperability, security)

```json
{"title": "CIO, Chief Information Officer, VP Information Technology, Director of IT, CMIO, Chief Medical Information Officer",
 "notTitle": "assistant, intern, former, technician, analyst, help desk",
 "keywords": ["hospital", "health system"], "minEmployees": 500,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### C3. Biotech and pharma clinical operations (CRO services, trial software)

```json
{"title": "VP Clinical Operations, Head of Clinical Operations, Director of Clinical Operations, Chief Medical Officer",
 "notTitle": "assistant, intern, former, associate, coordinator, CRA",
 "keywords": ["biotech", "pharmaceutical", "clinical trials"], "minEmployees": 20, "maxEmployees": 1000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### C4. Home health and senior care owners (staffing, scheduling software)

```json
{"title": "Owner, Administrator, Executive Director, CEO, Director of Operations",
 "notTitle": "assistant, nurse aide, caregiver, former, intern",
 "keywords": ["home health", "senior living", "home care"], "minEmployees": 20, "maxEmployees": 500,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

## D. Selling to commerce, consumer and manufacturing

### D1. Ecommerce brand founders (agencies, fulfillment, retention tools)

```json
{"title": "Founder, Co-Founder, CEO, Owner, Head of Ecommerce, Director of Ecommerce",
 "notTitle": "assistant, intern, former, advisor, investor",
 "keywords": ["ecommerce", "dtc", "consumer goods"], "minEmployees": 5, "maxEmployees": 200,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

For store-level filters (platform, installed apps, monthly visits) use `ecommerce-by-techstack` with `scrape_store_leads` instead.

### D2. Manufacturing plant and operations leaders (automation, MRO, safety)

```json
{"title": "VP Operations, Plant Manager, Director of Manufacturing, COO, VP Manufacturing, General Manager",
 "notTitle": "assistant, intern, former, supervisor, technician, operator",
 "keywords": ["manufacturing", "industrial"], "minEmployees": 100, "maxEmployees": 2000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### D3. Procurement in manufacturing (sourcing platforms, freight)

```json
{"title": "VP Procurement, Director of Procurement, Head of Purchasing, Chief Procurement Officer, Director of Supply Chain",
 "notTitle": "assistant, intern, former, buyer i, clerk, coordinator",
 "keywords": ["manufacturing"], "minEmployees": 200, "maxEmployees": 5000,
 "country": ["United States", "Canada", "Mexico"], "hasEmail": true, "limit": 1}
```

### D4. Logistics and 3PL operators (TMS, freight audit)

```json
{"title": "CEO, President, VP Operations, COO, Director of Logistics, Owner",
 "notTitle": "assistant, intern, former, dispatcher, driver, coordinator",
 "keywords": ["logistics", "3pl", "freight", "trucking"], "minEmployees": 20, "maxEmployees": 1000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### D5. Warehouse, 3PL and fulfillment operators (automation, robotics, WMS)

One count per buying-group family (`title-synonyms-and-exclusions.md`); this is the day-to-day owner family. Brokers and forwarders run no warehouses, so they leave through `notKeywords` and the site check.

```json
{"title": "VP Operations, VP Warehouse Operations, VP Distribution, VP Fulfillment, VP Contract Logistics, Director of Operations, Director of Warehouse Operations, Director of Distribution, Director of Fulfillment, General Manager",
 "notTitle": "assistant, intern, former, sales, business development, account, transportation, fleet, brokerage, freight, coordinator, supervisor, analyst",
 "keywords": ["3pl", "third party logistics", "contract logistics", "warehousing", "fulfillment", "distribution center", "cold storage"],
 "notKeywords": ["freight brokerage", "freight forwarding", "customs brokerage", "moving", "courier", "staffing", "saas"],
 "minEmployees": 200, "maxEmployees": 2000,
 "companyCountry": ["United States"], "hasEmail": true, "limit": 1}
```

Count `notKeywords` terms one at a time: hybrid 3PLs that also broker freight can lose rows to "freight brokerage"; if a term removes warehouse operators, drop it and let the site check decide. Benchmark: Census SUSB 2022 counts 1,159 Warehousing and Storage (NAICS 493) firms with 200-1,999 employees (`count-and-paging-runbook.md` section 9).

### D6. Restaurant groups (POS, procurement, staffing)

```json
{"title": "Owner, CEO, COO, Director of Operations, VP Operations, Managing Partner",
 "notTitle": "assistant, server, host, line cook, former, intern",
 "keywords": ["restaurant group", "hospitality"], "minEmployees": 50, "maxEmployees": 2000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

## E. Selling to finance, real estate and construction

### E1. Finance leaders at mid-market companies (FP&A software, fractional CFO)

```json
{"title": "CFO, Chief Financial Officer, VP Finance, Head of Finance, Controller, Director of Finance",
 "notTitle": "assistant, intern, former, accountant i, clerk, analyst",
 "minEmployees": 100, "maxEmployees": 1000, "revenueMin": 10000000, "revenueMax": 250000000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### E2. Community bank and credit union executives (core banking, compliance)

```json
{"title": "President, CEO, Chief Lending Officer, CFO, Chief Operating Officer, Chief Risk Officer",
 "notTitle": "assistant, teller, former, intern, branch associate",
 "keywords": ["community bank", "credit union", "banking"], "minEmployees": 50, "maxEmployees": 1000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### E3. Commercial real estate brokerage leaders (CRM, lead lists)

```json
{"title": "Managing Director, Principal, Broker, Owner, President, Managing Broker",
 "notTitle": "assistant, intern, former, coordinator, analyst",
 "keywords": ["commercial real estate"], "minEmployees": 5, "maxEmployees": 200,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

For agent-level lists use `scrape_zillow_agents` or the real estate skills.

### E4. General contractors and construction executives (estimating, safety)

```json
{"title": "Owner, President, CEO, VP Operations, Director of Preconstruction, Chief Estimator",
 "notTitle": "assistant, intern, former, laborer, apprentice, foreman",
 "keywords": ["general contractor", "construction"], "minEmployees": 20, "maxEmployees": 500,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### E5. Insurance agency principals (agency management systems, lead gen)

```json
{"title": "Owner, Principal, Agency Owner, President, CEO",
 "notTitle": "assistant, csr, customer service, former, intern, producer i",
 "keywords": ["insurance agency"], "minEmployees": 5, "maxEmployees": 100,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

## F. Selling to HR, education, nonprofit and public-adjacent buyers

### F1. HR leaders at mid-size employers (benefits, HRIS, recruiting)

```json
{"title": "VP People, Head of People, CHRO, Chief People Officer, VP Human Resources, Director of Human Resources",
 "notTitle": "assistant, intern, coordinator, generalist, recruiter, former",
 "department": ["hr"], "minEmployees": 200, "maxEmployees": 2000,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

`department: ["hr"]` is not one of the two examples in the tool description. Confirm with a count call; if it returns 0, drop it and rely on titles.

### F2. Talent acquisition leaders (sourcing tools, RPO)

```json
{"title": "Head of Talent Acquisition, VP Talent, Director of Talent Acquisition, Director of Recruiting",
 "notTitle": "assistant, intern, coordinator, sourcer, former",
 "minEmployees": 500, "maxEmployees": 5000, "country": ["United States"], "hasEmail": true, "limit": 1}
```

### F3. Higher education IT and enrollment (EdTech, CRM)

```json
{"title": "CIO, Chief Information Officer, VP Enrollment Management, Dean of Admissions, Director of Admissions, Provost",
 "notTitle": "assistant, student, intern, former, coordinator, professor",
 "keywords": ["higher education", "university", "college"], "minEmployees": 200,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

### F4. Nonprofit executive directors (donor CRM, fundraising services)

```json
{"title": "Executive Director, CEO, President, Director of Development, Chief Development Officer",
 "notTitle": "assistant, volunteer, intern, former, board member, coordinator",
 "keywords": ["nonprofit", "foundation", "charity"], "minEmployees": 10, "maxEmployees": 500,
 "country": ["United States"], "hasEmail": true, "limit": 1}
```

## G. International variants

### G1. UK SaaS sales leaders

Copy A1 and set `"country": ["United Kingdom"]`. UK titles lean on "Sales Director" and "Commercial Director" where US firms say "VP Sales"; add both to `title`, and add "Managing Director" for companies under 50 employees.

### G2. DACH industrial buyers

Copy D2 and set `"companyCountry": ["Germany", "Austria", "Switzerland"]`. Add German title forms to `title`: Geschäftsführer, Leiter Produktion, Werksleiter, Einkaufsleiter. Write the email in German for German-language titles; English titles at the same company usually read English.

### G3. Canada, any recipe

Add `"country": ["Canada"]`. For Quebec, add French title forms (Directeur des ventes, Vice-président des ventes, Directeur commercial) and set `state` to Quebec in a separate count, so French-language copy goes only to that slice. Keep `source_detail` on every row so the origin of each address can be shown on request.

## Exclusion add-ons that apply to most recipes

| Situation | Add |
|-|-|
| Seller cannot serve agencies or resellers | `"notKeywords": ["agency", "marketing agency", "reseller"]` |
| Seller cannot serve staffing firms | `"notKeywords": ["staffing", "recruiting"]` |
| Exclude government and education | `"notIndustry": ["government administration", "higher education", "primary/secondary education"]` (confirm labels with a count) |
| Exclude very large enterprises | `"maxEmployees": 5000` |
| Only people with a direct phone for a call block | `"hasPhone": true` |
| Only new people since the last pull | `"excludeDelivered": true` with `after` paging |
| Headquartered in one state, person anywhere | `"companyState": ["Texas"]` |
| Person in one metro | `"city": "Austin, Round Rock, Cedar Park"` |

## Using a saved people-search URL

If the user already has a people search in a tool such as Apollo.io, pass it as `url`. Its filters become the query and any parameter you also pass overrides the matching one. Read `search_translation` in the response: it lists filters applied, approximated, or not supported. Re-add anything not supported with native parameters before pulling.

```json
{"url": "https://app.apollo.io/#/people?personTitles[]=vp%20sales&organizationNumEmployeesRanges[]=51,200", "hasEmail": true, "limit": 1}
```

## Sources

- ScraperCity MCP tool schema for `query_lead_database` (scrapercity npm package): https://www.npmjs.com/package/scrapercity
- ScraperCity CLI repository: https://github.com/scrapercity/scrapercity-cli
- April Dunford, A quickstart guide to positioning: https://www.aprildunford.com/post/a-quickstart-guide-to-positioning
- US Census Bureau, 2022 SUSB annual data tables (NAICS 493 firm count by size): https://www.census.gov/data/tables/2022/econ/susb/2022-susb-annual.html
