# Buying Role Map

For 22 product categories: who holds the budget (slot 1, economic buyer), who owns the problem day to day (slot 2, champion or owner), and who evaluates (slot 3, optional). Each slot lists a `title` string and `seniority` for `query_lead_database`, and one `jobTitle` for `scrape_website_finder`, which takes one title per request.

## How to read the map

- `seniority` values documented in the tool: `vp`, `director`, `c_suite`. Other values (`manager`, `owner`, `founder`, `head`, `senior`) may exist; test with a `limit: 1` call before relying on them.
- Company size changes which titles fill each slot. Use the size adjustments at the end.
- Add the universal `notTitle` set to every call: `assistant, intern, former, retired, advisor, board, investor`.

## Sales, marketing and revenue products

### 1. Sales engagement, dialers, sales coaching

| Slot | Role | `title` | `seniority` | Website Finder `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | VP Sales, Chief Revenue Officer, CRO, SVP Sales, Head of Sales | vp, c_suite | VP Sales |
| 2 | Champion | Director of Sales, Sales Director, Director of Sales Development, Head of SDR | director | Director of Sales |
| 3 | Evaluator | Sales Operations, Revenue Operations, RevOps | director | Revenue Operations |

### 2. CRM and revenue data

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CRO, VP Sales, VP Revenue Operations | vp, c_suite | Chief Revenue Officer |
| 2 | Champion | Director of Revenue Operations, Head of Sales Operations, Sales Operations Manager | director | Revenue Operations |
| 3 | Evaluator | Salesforce Administrator, CRM Manager | | Salesforce Administrator |

### 3. Marketing automation, ads, SEO and content services

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CMO, VP Marketing, Head of Marketing, VP Growth | vp, c_suite | VP Marketing |
| 2 | Champion | Director of Demand Generation, Head of Growth, Director of Marketing | director | Director of Demand Generation |
| 3 | Evaluator | Marketing Operations, Marketing Ops Manager | | Marketing Operations |

### 4. Customer success and support platforms

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | Chief Customer Officer, VP Customer Success, VP Support | vp, c_suite | VP Customer Success |
| 2 | Champion | Director of Customer Success, Head of Support, Director of Customer Experience | director | Director of Customer Success |
| 3 | Evaluator | Support Operations, CS Operations | | Customer Success Operations |

## Technology and data products

### 5. Developer tools and cloud infrastructure

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CTO, VP Engineering, SVP Engineering | vp, c_suite | VP Engineering |
| 2 | Champion | Director of Engineering, Head of Platform, Head of DevOps, Engineering Manager | director | Director of Engineering |
| 3 | Evaluator | Staff Engineer, Principal Engineer, DevOps Lead | | Principal Engineer |

### 6. Security

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CISO, Chief Information Security Officer, VP Security | vp, c_suite | CISO |
| 2 | Champion | Director of Security, Security Engineering Manager, Head of Security Operations | director | Director of Information Security |
| 3 | Evaluator | Security Architect, Security Engineer | | Security Architect |

Under 200 employees there is often no CISO; slot 1 becomes CTO or VP IT.

### 7. IT services, MSP, hardware

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CIO, VP IT, Director of IT | vp, c_suite, director | IT Director |
| 2 | Champion | IT Manager, Systems Administrator Manager, Infrastructure Manager | | IT Manager |

### 8. Data and analytics platforms

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | Chief Data Officer, VP Data, VP Analytics, CTO | vp, c_suite | VP Data |
| 2 | Champion | Head of Data, Director of Analytics, Data Engineering Manager | director | Director of Analytics |

## Finance, legal and people products

### 9. FP&A, accounting software, fractional CFO

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CFO, Chief Financial Officer, VP Finance | vp, c_suite | CFO |
| 2 | Champion | Controller, Director of FP&A, Director of Finance | director | Controller |

### 10. Payments, AP automation, spend management

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CFO, VP Finance | vp, c_suite | CFO |
| 2 | Champion | Controller, Accounts Payable Manager, Director of Accounting | director | Controller |

### 11. Legal tech and contract management

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | General Counsel, Chief Legal Officer | c_suite, vp | General Counsel |
| 2 | Champion | Deputy General Counsel, Legal Operations Director, Head of Legal Operations | director | Legal Operations |

### 12. HRIS, payroll, benefits

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CHRO, Chief People Officer, VP People, VP Human Resources | vp, c_suite | VP Human Resources |
| 2 | Champion | Director of HR, HR Operations Manager, Director of Total Rewards | director | Director of Human Resources |
| 3 | Evaluator | Payroll Manager, HRIS Manager | | HRIS Manager |

### 13. Recruiting tools and staffing services

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | VP Talent Acquisition, CHRO, VP People | vp, c_suite | VP Talent Acquisition |
| 2 | Champion | Director of Talent Acquisition, Head of Recruiting | director | Director of Talent Acquisition |

## Operations and industry products

### 14. Field service, scheduling, dispatch

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | Owner, President, COO, VP Operations | c_suite, vp | Owner |
| 2 | Champion | Operations Manager, Service Manager, Dispatch Manager, General Manager | | Operations Manager |

### 15. Manufacturing, MRO, automation, safety

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | VP Operations, COO, VP Manufacturing | vp, c_suite | VP Operations |
| 2 | Champion | Plant Manager, Director of Manufacturing, Maintenance Manager, EHS Manager | director | Plant Manager |
| 3 | Evaluator | Continuous Improvement Manager, Process Engineer | | Continuous Improvement Manager |

### 16. Procurement, sourcing, freight

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | Chief Procurement Officer, VP Procurement, VP Supply Chain | vp, c_suite | VP Supply Chain |
| 2 | Champion | Director of Procurement, Purchasing Manager, Logistics Manager | director | Director of Procurement |

### 17. Food and beverage manufacturing (packaging, ingredients, food safety)

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | VP Operations, COO, VP Supply Chain | vp, c_suite | VP Operations |
| 2 | Champion | Plant Manager, Director of Food Safety, Director of Quality, QA Manager | director | Director of Quality |

### 18. Healthcare providers (RCM, patient engagement, staffing)

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | CEO, CFO, COO, Administrator | c_suite | Administrator |
| 2 | Champion | Director of Revenue Cycle, Practice Manager, Director of Patient Access | director | Practice Manager |

### 19. Hospitality and restaurant groups

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | Owner, CEO, COO, VP Operations | c_suite, vp | Director of Operations |
| 2 | Champion | Director of Operations, General Manager, Area Manager | director | General Manager |

### 20. Construction (estimating, project software, equipment)

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | President, Owner, VP Operations | c_suite, vp | President |
| 2 | Champion | Director of Preconstruction, Chief Estimator, Project Executive | director | Chief Estimator |

### 21. Ecommerce brands (agencies, retention, fulfillment)

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | Founder, CEO, Head of Ecommerce | c_suite | Founder |
| 2 | Champion | Director of Ecommerce, Head of Growth, Retention Marketing Manager | director | Director of Ecommerce |

### 22. Professional services firms (law, accounting, consulting)

| Slot | Role | `title` | `seniority` | `jobTitle` |
|-|-|-|-|-|
| 1 | Economic buyer | Managing Partner, Founding Partner, Owner | c_suite | Managing Partner |
| 2 | Champion | Firm Administrator, Director of Operations, COO | director | Firm Administrator |

## Size adjustments

| Company size | Slot 1 | Slot 2 | Slot 3 |
|-|-|-|-|
| 1-10 employees | Owner or founder | Usually none; skip | Skip |
| 11-50 | Founder, CEO, or the one department head | Department head if separate from slot 1 | Skip |
| 51-500 | VP of the owning department | Director or manager who runs the process | Optional |
| 501-5,000 | VP or SVP | Director | Manager or evaluator |
| 5,000+ | SVP or division head | Director in the right business unit | Evaluator |

Industry can change the committee too. Ask the user which reviewers (information security, vendor risk) joined their past deals in the account's industry, and map those names from the committee table below.

For companies over 5,000 employees, add the business unit or region to `title` ("VP Operations North America") or filter by `state` to find the person who owns the account's territory.

## Committee roles to map, not email

When the user says these roles joined their past deals of this size, map them by name from the same Lead Database pass and keep them in the committee file.

| Role | Joins when | `title` |
|-|-|-|
| Procurement | Contract and vendor setup | Procurement, Purchasing, Sourcing, Vendor Management |
| IT security review | Any product that touches company data or logins | Information Security, IT Security, Security Architect, GRC |
| Finance | Spend above the department's own approval limit | Controller, Finance Director, FP&A |
| IT owner of the systems | The product integrates with existing systems | IT Director, Enterprise Applications, Systems Manager |
| End-user lead | Rollout and adoption | The category's slot 2 manager titles at other sites or regions |

## Ranking candidates within a slot

When the database returns several people for one slot at a domain:

1. Title family exact match beats partial ("VP Operations" over "VP Operations Excellence").
2. Higher seniority within the slot wins.
3. Email present beats missing.
4. Person location in the company's HQ country beats elsewhere.
5. If still tied, keep both as primary and backup; send to primary only.

## Sources

- Gartner, B2B Buying Report: https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- MEDDICC, Who created MEDDIC: https://meddicc.com/resources/who-created-meddic
- ScraperCity MCP tool schemas for `query_lead_database` and `scrape_website_finder`: https://www.npmjs.com/package/scrapercity
