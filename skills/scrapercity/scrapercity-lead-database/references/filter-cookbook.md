# Lead Database Filter Cookbook

44 ready filter sets for `query_lead_database`. Each recipe is a JSON body you can send as MCP arguments or as a REST POST body. Run every recipe first with `"limit": 1` to read `pagination.total`, then pull with `"limit": 100, "after": "0"`.

Conventions used below:

- Seniority values used are the three confirmed in the ScraperCity source (`vp`, `director`, `c_suite`). Other values need a probe first (see `references/filter-semantics.md`).
- Industry strings other than `computer software` are shown as `keywords`, which match whole words in company tags and need no exact industry spelling. Swap to `industry` once you have confirmed the spelling from `company_industry` on a sample row.
- `hasEmail: true` is on for every email campaign recipe. Remove it for a count of the full market.

## A. Sales and revenue leaders

**1. VP Sales, US SaaS, 50-200 employees**
```json
{"title":"VP Sales, VP of Sales, Vice President Sales, Vice President of Sales, Head of Sales","notTitle":"Assistant, Intern, Operations, Enablement","companyCountry":["United States"],"keywords":["saas"],"minEmployees":50,"maxEmployees":200,"hasEmail":true}
```

**2. CRO and VP Revenue, US B2B software, 201-1,000**
```json
{"title":"Chief Revenue Officer, CRO, VP Revenue, Vice President of Revenue","industry":["computer software"],"companyCountry":["United States"],"minEmployees":201,"maxEmployees":1000,"hasEmail":true}
```

**3. Sales Directors, UK companies over 10 staff (drops one-person firms that have no sales team)**
```json
{"title":"Sales Director, Director of Sales, Head of Sales","notTitle":"Assistant","companyCountry":["United Kingdom"],"minEmployees":10,"hasEmail":true}
```

**4. Founders doing their own selling, seed stage SaaS, 2-20 staff**
```json
{"title":"Founder, Co-Founder, CEO","keywords":["saas"],"companyCountry":["United States","Canada"],"minEmployees":2,"maxEmployees":20,"hasEmail":true}
```

**5. Sales Enablement leaders**
```json
{"title":"Sales Enablement, Revenue Enablement","notTitle":"Coordinator, Intern, Specialist","companyCountry":["United States"],"minEmployees":200,"hasEmail":true}
```

**6. RevOps and Sales Ops leaders**
```json
{"title":"Revenue Operations, RevOps, Sales Operations","seniority":["vp","director"],"companyCountry":["United States"],"minEmployees":100,"hasEmail":true}
```

**7. SDR and BDR managers (buyers of outbound tools)**
```json
{"title":"SDR Manager, BDR Manager, Head of Sales Development, Director of Sales Development","companyCountry":["United States"],"minEmployees":50,"hasEmail":true}
```

**8. Sales leaders by department instead of title**
```json
{"department":["sales"],"seniority":["vp","director"],"companyCountry":["United States"],"minEmployees":50,"maxEmployees":500,"hasEmail":true}
```

## B. Marketing

**9. CMOs at mid-market B2B**
```json
{"title":"CMO, Chief Marketing Officer","companyCountry":["United States"],"minEmployees":200,"maxEmployees":2000,"notKeywords":["agency"],"hasEmail":true}
```

**10. Demand gen leaders**
```json
{"title":"Demand Generation, Demand Gen, Growth Marketing","seniority":["vp","director"],"keywords":["saas","b2b"],"hasEmail":true}
```

**11. Heads of Marketing at small ecommerce brands**
```json
{"title":"Head of Marketing, Marketing Director, Director of Marketing, Ecommerce Manager","keywords":["ecommerce","dtc"],"minEmployees":5,"maxEmployees":100,"hasEmail":true}
```

**12. Marketing agency owners (selling to agencies)**
```json
{"title":"Founder, Owner, CEO, Managing Director","keywords":["marketing agency","digital agency"],"notTitle":"Product Owner","minEmployees":2,"maxEmployees":50,"hasEmail":true}
```

**13. Content and SEO leads**
```json
{"title":"Head of Content, Content Director, SEO Manager, Head of SEO","notTitle":"Intern, Assistant","companyCountry":["United States"],"minEmployees":50,"hasEmail":true}
```

## C. Finance

**14. CFOs at $10M-$100M revenue companies, US HQ**
```json
{"title":"CFO, Chief Financial Officer","companyCountry":["United States"],"revenueMin":10000000,"revenueMax":100000000,"hasEmail":true}
```

**15. Controllers and VP Finance at 100-500 staff**
```json
{"title":"Controller, VP Finance, Vice President of Finance, Director of Finance","notTitle":"Assistant, Intern, Analyst","minEmployees":100,"maxEmployees":500,"companyCountry":["United States"],"hasEmail":true}
```

**16. Finance leaders in Texas-headquartered companies**
```json
{"title":"CFO, Controller, VP Finance","companyState":["Texas"],"minEmployees":50,"hasEmail":true}
```

**17. Accounts payable owners (AP automation)**
```json
{"title":"Accounts Payable Manager, AP Manager, Director of Accounts Payable","minEmployees":200,"companyCountry":["United States"],"hasEmail":true}
```

## D. Engineering, IT and security

**18. CTOs at software companies, 20-200 staff**
```json
{"title":"CTO, Chief Technology Officer","industry":["computer software"],"minEmployees":20,"maxEmployees":200,"hasEmail":true}
```

**19. VP Engineering by department**
```json
{"department":["engineering"],"seniority":["vp"],"companyCountry":["United States"],"minEmployees":100,"hasEmail":true}
```

**20. CISOs and security leaders at regulated firms**
```json
{"title":"CISO, Chief Information Security Officer, VP Security, Head of Security, Director of Information Security","keywords":["fintech","healthcare","insurance"],"minEmployees":200,"hasEmail":true}
```

**21. IT Directors at mid-size non-tech companies**
```json
{"title":"IT Director, Director of IT, Head of IT, IT Manager","notKeywords":["saas","software"],"minEmployees":100,"maxEmployees":1000,"companyCountry":["United States"],"hasEmail":true}
```

**22. Data and analytics leaders**
```json
{"title":"Head of Data, VP Data, Director of Analytics, Chief Data Officer","minEmployees":200,"hasEmail":true}
```

**23. DevOps and platform leads**
```json
{"title":"Head of DevOps, Director of Platform, VP Infrastructure, Director of Infrastructure","keywords":["saas"],"minEmployees":50,"hasEmail":true}
```

## E. People and operations

**24. HR leaders at 200-2,000 staff**
```json
{"title":"CHRO, VP People, Head of People, VP Human Resources, HR Director","minEmployees":200,"maxEmployees":2000,"companyCountry":["United States"],"hasEmail":true}
```

**25. Talent acquisition leaders (recruiting tools)**
```json
{"title":"Head of Talent, Director of Talent Acquisition, VP Talent, Recruiting Manager","notTitle":"Coordinator, Intern","minEmployees":100,"hasEmail":true}
```

**26. COOs at 50-500 staff**
```json
{"title":"COO, Chief Operating Officer, VP Operations","notTitle":"Assistant","minEmployees":50,"maxEmployees":500,"companyCountry":["United States"],"hasEmail":true}
```

**27. Procurement leaders**
```json
{"title":"Procurement, Purchasing Director, Head of Procurement, VP Procurement","notTitle":"Assistant, Coordinator, Buyer","minEmployees":500,"hasEmail":true}
```

**28. Office and facilities managers (office services)**
```json
{"title":"Office Manager, Facilities Manager, Workplace Manager","city":"New York, Brooklyn","minEmployees":20,"hasEmail":true}
```

## F. Executives by size and stage

**29. CEOs of small businesses, 10-50 staff, US HQ**
```json
{"title":"CEO, President, Owner, Founder","notTitle":"Product Owner, Vice President","companyCountry":["United States"],"minEmployees":10,"maxEmployees":50,"hasEmail":true}
```

**30. C-suite at $50M+ revenue**
```json
{"seniority":["c_suite"],"revenueMin":50000000,"companyCountry":["United States"],"hasEmail":true}
```

**31. Managing Directors in DACH**
```json
{"title":"Managing Director, Geschaftsfuhrer, CEO","companyCountry":["Germany","Austria","Switzerland"],"minEmployees":20,"hasEmail":true}
```

**32. Founders at fintech startups**
```json
{"title":"Founder, Co-Founder","keywords":["fintech"],"minEmployees":5,"maxEmployees":100,"hasEmail":true}
```

## G. Vertical plays

**33. Healthcare practice administrators**
```json
{"title":"Practice Administrator, Practice Manager, Office Administrator","keywords":["healthcare","medical practice"],"hasEmail":true}
```

**34. Logistics and supply chain leaders**
```json
{"title":"VP Supply Chain, Director of Logistics, Head of Supply Chain, Logistics Manager","keywords":["logistics","3pl","freight"],"minEmployees":50,"hasEmail":true}
```

**35. Construction company owners and estimators**
```json
{"title":"Owner, President, Estimator, Project Manager","notTitle":"Product Owner, Assistant","keywords":["construction","general contractor"],"minEmployees":10,"maxEmployees":200,"companyCountry":["United States"],"hasEmail":true}
```

**36. Manufacturing plant and ops leaders**
```json
{"title":"Plant Manager, VP Manufacturing, Director of Operations, Operations Manager","keywords":["manufacturing"],"minEmployees":50,"hasEmail":true}
```

**37. Law firm partners**
```json
{"title":"Managing Partner, Partner","notTitle":"Partner Manager, Partnerships","keywords":["law firm","legal services"],"hasEmail":true}
```

**38. Real estate brokerage leaders**
```json
{"title":"Broker, Managing Broker, Team Lead, Broker Owner","keywords":["real estate"],"companyCountry":["United States"],"hasEmail":true}
```

**39. Ecommerce operators, Shopify-tagged companies**
```json
{"title":"Founder, CEO, Head of Ecommerce, Director of Ecommerce","keywords":["shopify","ecommerce"],"minEmployees":2,"maxEmployees":200,"hasEmail":true}
```

## H. Account-based and lookups

**40. Everyone senior at a list of target domains**
```json
{"companyDomain":"acme.com, globex.com, initech.com","seniority":["vp","director","c_suite"],"hasEmail":true}
```

**41. One named company, sales and marketing only**
```json
{"companyName":"Acme Corporation","title":"Sales, Marketing","notTitle":"Intern, Assistant","hasEmail":true}
```

**42. Find a person from a social profile URL (also the job-change re-check)**
```json
{"socialUrl":"https://www.linkedin.com/in/example-profile","limit":1}
```
Compare the company on the record with the one in the CRM. A different company is a job-change candidate to confirm on the public profile; an empty result says nothing about whether they left. Re-fetching a lead the account already has is free. The monthly routine for a whole watch list is the job-change recipe in the `scrapercity-integrations` skill.

**43. People-search URL with an override**
```json
{"url":"<paste the people-search URL>","hasEmail":true,"limit":1}
```
Replace the angle-bracket text with the user's URL before sending. Read `search_translation` and report it.

**44. Daily new-lead feed for one segment**
```json
{"title":"VP Sales, Head of Sales","companyCountry":["United States"],"keywords":["saas"],"minEmployees":50,"maxEmployees":200,"hasEmail":true,"excludeDelivered":true,"after":"0","limit":100}
```
Loop on `pagination.next_after` until null or the day's target.

## I. Exclusion patterns to add to any recipe

| Goal | Add |
|---|---|
| Drop assistants and junior staff | `"notTitle":"Assistant, Intern, Coordinator, Associate"` |
| Drop agencies and consultancies from software pulls | `"notKeywords":["agency","consulting","staffing"]` |
| Drop non-profits and government | `"notIndustry":["government administration","nonprofit organization management"]` after confirming spelling, or `"notKeywords":["nonprofit","government"]` |
| Drop "Product Owner" from owner pulls | `"notTitle":"Product Owner"` |
| Drop partnership managers from partner pulls | `"notTitle":"Partner Manager, Partnerships, Channel Partner"` |
| Cut one-person firms and sole traders | `"minEmployees":10` |

## J. Splitting a big market into daily segments

When a recipe returns more than 100,000, split it so each segment fits one day and one message:

| Split by | Example |
|---|---|
| Company HQ state | `companyState: ["California"]`, then `["Texas"]`, then `["New York"]` |
| Size band | 11-50, 51-200, 201-1,000 |
| Seniority | `["c_suite"]` then `["vp"]` then `["director"]` |
| Title family | Sales titles, then RevOps titles |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://docs.apollo.io/reference/people-api-search
