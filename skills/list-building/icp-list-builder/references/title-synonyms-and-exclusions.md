# Title Synonyms and `notTitle` Exclusions

`query_lead_database` matches `title` as a partial, comma-separated list, and `notTitle` drops any row whose title contains one of its terms. Partial matching is generous: "VP Sales" also matches "Assistant to the VP Sales" and "Former VP Sales". So every title family below comes in pairs: the synonyms to include and the exclusions that strip false positives.

Paste the `title` line into `title` and the `notTitle` line into `notTitle`. Keep each string under about 600 characters; for longer lists the CLI and REST API switch to a POST body automatically, and the MCP tool accepts the same parameters.

## How to test a title family

1. Count with the `title` only.
2. Count again with `notTitle` added. The drop is the false positives you removed.
3. Pull a page of rows and read the titles. Add the word behind each wrong title to `notTitle` and repeat.
4. Seniority can do part of the job. `"seniority": ["vp", "c_suite"]` with `"department": ["sales"]` often replaces a long title list. The tool documents `vp`, `director`, `c_suite` for seniority and `sales`, `engineering` for department; test any other value with a count call first.

## Buying-group families

Gartner's B2B Buying Report (2022 survey) puts buying groups at five to 11 people from about five functions. Build one query per family below, so each family's title list and `notTitle` stay separate, and dedupe people across families afterwards (a "COO and VP Operations" matches two families).

| Family | Role in the deal | `title` pattern | `notTitle` guards |
|-|-|-|-|
| Economic buyer | Signs or approves the spend | CEO, Chief Executive Officer, President, Owner, Co-Owner, Founder, Co-Founder, Managing Partner, COO, Chief Operating Officer, CFO, Chief Financial Officer | vice, assistant, executive assistant, coordinator, product owner, process owner, former, retired, board, investor, advisor, division, regional, sales |
| Day-to-day owner | Owns the process or site the product changes | The operating leader of that function: VP Operations, Director of Operations, Plant Manager, VP Warehouse Operations, VP Distribution, VP Fulfillment, General Manager | assistant, intern, former, sales, coordinator, supervisor, analyst, specialist |
| Technical evaluator | Specs and runs the project | Director of Engineering, Industrial Engineering, Automation, Continuous Improvement, Operational Excellence, Solutions Design, Maintenance, Reliability | assistant, intern, former, technician, mechanic, sales engineer, software, coordinator, analyst |
| IT and systems | Signs off on integration with their systems | CIO, Chief Information Officer, CTO, VP IT, Director of IT, Director of Systems, Director of Applications | help desk, support, technician, desktop, analyst, intern, former |

Why the guards:

- "President" matches inside "Vice President", so "vice" goes in the economic-buyer `notTitle`; Vice Presidents are covered by the other families.
- "COO" matches inside "Coordinator".
- "Owner" matches "Product Owner" and "Process Owner".
- Owner, Founder and Managing Partner stay in the economic-buyer family at every size: family-owned and founder-led companies use them for the person who signs, and a CEO-only list misses those companies.
- "CTO" at a company that also sells software returns its product engineers; read the first 100 rows of the IT family and drop CTO if they appear.

The tool documents `vp`, `director` and `c_suite` as seniority values. Owner and founder titles go in `title`; test any other seniority value with a `limit: 1` count first.

## Universal exclusions

Add these to every family unless the user is selling to them:

```text
assistant, intern, former, retired, emeritus, student, volunteer, advisor, advisory, board member, investor, freelance, consultant to, executive assistant, ea to, office of the
```

Watch "consultant": it removes buyers at consulting firms. Leave it out when the target is a services firm.

## Sales and revenue

| Level | `title` |
|-|-|
| C-level | Chief Revenue Officer, CRO, Chief Sales Officer, CSO, Chief Commercial Officer, CCO |
| VP | VP Sales, VP of Sales, Vice President of Sales, Vice President Sales, SVP Sales, EVP Sales, VP Revenue, VP Business Development, VP Commercial |
| Head | Head of Sales, Head of Revenue, Head of Growth, Head of Business Development |
| Director | Director of Sales, Sales Director, Regional Sales Director, Director of Business Development |
| Small company | Founder, Co-Founder, CEO, Owner, President, Managing Director |

`notTitle` for sales leaders:

```text
assistant, intern, former, retired, advisor, board, sales engineer, solutions engineer, sales enablement, sales operations, inside sales representative, account executive, sdr, bdr, sales associate, sales coordinator, sales support
```

Note: "CSO" also means Chief Security Officer and Chief Sustainability Officer. Drop it from `title` if the count jumps and the sample shows security or sustainability roles.

## Sales operations and RevOps

```text
title: Revenue Operations, RevOps, Sales Operations, Sales Ops, GTM Operations, Go-to-Market Operations, Director of Revenue Operations, VP Revenue Operations, Head of Revenue Operations, Sales Systems, CRM Manager, Salesforce Administrator
notTitle: assistant, intern, former, coordinator, analyst i, associate, specialist i
```

## Marketing

```text
title: CMO, Chief Marketing Officer, VP Marketing, VP of Marketing, Vice President of Marketing, Head of Marketing, Head of Growth, Head of Demand Generation, Director of Marketing, Marketing Director, Director of Demand Generation, VP Growth
notTitle: assistant, intern, former, coordinator, social media, content writer, graphic designer, marketing associate, brand ambassador
```

Narrower sub-families:

| Sub-family | `title` |
|-|-|
| Demand gen | Demand Generation, Growth Marketing, Performance Marketing, Paid Acquisition |
| Product marketing | Product Marketing, PMM, Head of Product Marketing, Director of Product Marketing |
| Content and brand | Head of Content, Content Director, Brand Director, Head of Brand |
| Marketing ops | Marketing Operations, Marketing Ops, Marketing Technology, MarTech |

## Engineering and IT

```text
title: CTO, Chief Technology Officer, VP Engineering, VP of Engineering, Vice President of Engineering, Head of Engineering, Director of Engineering, Engineering Director, SVP Engineering
notTitle: assistant, intern, former, sales engineer, solutions engineer, field engineer, support engineer, engineer i, engineer ii, technician, student
```

```text
title: CIO, Chief Information Officer, VP IT, VP Information Technology, Director of IT, IT Director, Head of IT, IT Manager, Director of Information Systems
notTitle: assistant, intern, former, help desk, technician, support specialist, desktop support
```

Security:

```text
title: CISO, Chief Information Security Officer, Chief Security Officer, VP Security, VP Information Security, Head of Security, Director of Security, Director of Information Security, Security Director
notTitle: assistant, intern, former, physical security, security guard, security officer i, loss prevention, campus security, guard
```

Data:

```text
title: Chief Data Officer, CDO, VP Data, Head of Data, Director of Data, Director of Analytics, Head of Analytics, VP Analytics, Data Engineering Manager
notTitle: assistant, intern, former, data entry, analyst i, student
```

## Product

```text
title: CPO, Chief Product Officer, VP Product, VP of Product, Head of Product, Director of Product, Director of Product Management, Group Product Manager
notTitle: assistant, intern, former, product marketing, product designer, product specialist, production
```

"production" is in `notTitle` because "Product" partially matches "Production Manager".

## Customer success and support

```text
title: Chief Customer Officer, CCO, VP Customer Success, Head of Customer Success, Director of Customer Success, VP Customer Experience, Head of Customer Experience, VP Support, Director of Support
notTitle: assistant, intern, former, representative, associate, specialist, agent, coordinator
```

## Finance

```text
title: CFO, Chief Financial Officer, VP Finance, VP of Finance, Head of Finance, Controller, Financial Controller, Director of Finance, Finance Director, Corporate Controller
notTitle: assistant, intern, former, accounts payable, accounts receivable, clerk, bookkeeper, staff accountant, analyst i
```

## Operations

```text
title: COO, Chief Operating Officer, VP Operations, VP of Operations, Head of Operations, Director of Operations, Operations Director, General Manager
notTitle: assistant, intern, former, operations coordinator, operations associate, operator, technician, supervisor
```

## People and HR

```text
title: CHRO, Chief People Officer, Chief Human Resources Officer, VP People, VP Human Resources, VP HR, Head of People, Head of HR, Director of Human Resources, HR Director, Director of People
notTitle: assistant, intern, former, coordinator, generalist, recruiter, sourcer, hr associate, payroll clerk
```

Talent acquisition:

```text
title: Head of Talent Acquisition, VP Talent Acquisition, Director of Talent Acquisition, Director of Recruiting, Head of Recruiting, VP Talent
notTitle: assistant, intern, former, coordinator, sourcer, recruiter i
```

## Procurement and supply chain

```text
title: Chief Procurement Officer, CPO, VP Procurement, VP Purchasing, Director of Procurement, Head of Procurement, Director of Purchasing, VP Supply Chain, Director of Supply Chain, Head of Supply Chain
notTitle: assistant, intern, former, buyer i, clerk, coordinator, expediter, analyst i
```

"CPO" collides with Chief Product Officer. Use it in only one family per query.

## Legal

```text
title: General Counsel, Chief Legal Officer, CLO, Deputy General Counsel, VP Legal, Head of Legal, Legal Director
notTitle: assistant, paralegal, intern, former, legal secretary, clerk
```

## Owners of small businesses and practices

```text
title: Owner, Co-Owner, Founder, Co-Founder, President, CEO, Principal, Managing Partner, Managing Member, Proprietor
notTitle: assistant, former, intern, student, franchise consultant, advisor, investor, board
```

"Owner" partially matches "Product Owner" and "Process Owner". Add `product owner, process owner, business owner liaison` to `notTitle` when the list targets software firms.

Practice-specific owners:

| Practice | `title` |
|-|-|
| Dental | Owner, Dentist, DDS, DMD, Practice Owner, Practice Administrator, Office Manager |
| Medical | Owner, Physician Owner, Medical Director, Practice Administrator, Practice Manager |
| Veterinary | Owner, Veterinarian, DVM, Practice Manager, Hospital Administrator |
| Law | Managing Partner, Founding Partner, Principal Attorney, Firm Administrator |
| Accounting | Managing Partner, Partner, Owner, CPA |

For practices where the database has few named owners, switch to `local-business-list` and the Local Business Database with `hasContact: true`.

## Non-English title forms

| Language | Executive | Sales head | Operations or plant |
|-|-|-|-|
| German | Geschäftsführer, Vorstand, Inhaber | Vertriebsleiter, Leiter Vertrieb | Werksleiter, Leiter Produktion |
| French | Directeur Général, PDG, Gérant | Directeur Commercial | Directeur des Opérations, Directeur d'Usine |
| Spanish | Director General, Gerente General, Consejero Delegado | Director Comercial, Director de Ventas | Director de Operaciones, Jefe de Planta |
| Dutch | Algemeen Directeur, Eigenaar | Commercieel Directeur, Salesdirecteur | Operationeel Directeur, Fabrieksmanager |
| Portuguese | Diretor Geral, CEO, Sócio | Diretor Comercial, Diretor de Vendas | Diretor de Operações |

Mix English and local forms in one `title` string; many people in these markets use English titles.

## Titles that look senior and are not buyers

| Title | Why to exclude by default |
|-|-|
| Chief of Staff | Influences, rarely signs; include only for CEO-office tools. |
| Executive Assistant to the CEO | Gatekeeper; matches "CEO" partial search. |
| VP (at banks) | Bank VP is often a mid-level title. For banks, use SVP, EVP, Managing Director. |
| Partner (at large consultancies and Big 4) | Thousands per firm; target practice leads by name instead. |
| Director (at agencies) | Often a client-facing account title; check with a 25-row sample. |
| Founder (of a side project) | Sole founders of one-person companies; add `minEmployees: 2`. |

## Sources

- ScraperCity MCP tool schema for `query_lead_database` (`title`, `notTitle`, `seniority`, `department` descriptions): https://www.npmjs.com/package/scrapercity
- ScraperCity CLI source (POST fallback for long queries): https://github.com/scrapercity/scrapercity-cli
- Gartner, B2B Buying Report (buying group size): https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- US Bureau of Labor Statistics, Standard Occupational Classification (management occupation groups): https://www.bls.gov/soc/
