# Title Expansion Library

Ready `title` and `notTitle` strings for common role families. The Lead Database `title` filter takes comma-separated terms and matches each one partially, so a short term catches many phrasings; `notTitle` removes titles containing any listed term. Treat every set as a draft: count with `limit: 1`, read a sample of rows, and adjust.

## 1. How to build a family

1. Core noun: the word every version of the title shares (Engineer, Developer, Account Executive, Controller).
2. Specialty words: how people name the specialty (React, Frontend, Front End, Front-End, UI, Web).
3. Spelling variants: hyphens, spaces, abbreviations (Front-End, Front End, FE; Sr, Senior; Mgr, Manager).
4. Level: use `seniority` where possible instead of putting Senior or Staff in `title`, because many senior people do not write the level in their title.
5. Drag-ins: titles that contain your terms but are not the role (React Native for web React, Engineering Manager for an individual contributor role, Recruiter for anything). These go in `notTitle`.
6. Always exclude: Intern, Student, Instructor, Teacher, Bootcamp, Former, Retired, Volunteer, Freelance and Contract when the role is full-time.

Glen Cathey's point about narrow exact phrases applies directly: one exact title misses qualified people who write their title another way.

## 2. Engineering families

| Role | `title` | `notTitle` | `seniority` / `department` |
|-|-|-|-|
| Frontend or React engineer (IC) | React, Frontend, Front End, Front-End, UI Engineer, JavaScript Engineer, Web Engineer | Native, Mobile, iOS, Android, Manager, Director, Head of, VP, Recruiter, Designer, QA, Intern, Instructor | senior (probe); engineering |
| React Native or mobile engineer | React Native, Mobile Engineer, iOS, Android, Mobile Developer | Manager, Director, Recruiter, QA, Intern | engineering |
| Backend engineer | Backend, Back End, Back-End, Server, API Engineer, Platform Engineer, Java Engineer, Go Engineer, Python Engineer | Frontend, Manager, Director, Recruiter, Intern, Data Scientist | engineering |
| Full-stack engineer | Full Stack, Full-Stack, Fullstack, Software Engineer | Manager, Director, Recruiter, Intern, Test, QA | engineering |
| Data engineer | Data Engineer, Analytics Engineer, ETL, Data Platform, Big Data | Manager, Director, Recruiter, Intern, Data Entry, Data Analyst | engineering |
| Data scientist or ML engineer | Data Scientist, Machine Learning, ML Engineer, Applied Scientist, AI Engineer | Manager, Director, Recruiter, Intern, Instructor, Sales | engineering |
| DevOps or SRE | DevOps, Site Reliability, SRE, Platform Engineer, Infrastructure Engineer, Cloud Engineer | Manager, Director, Recruiter, Intern, Sales, Support | engineering |
| Security engineer | Security Engineer, Application Security, AppSec, Cloud Security, Product Security, Detection Engineer | Manager, Director, Guard, Officer, Recruiter, Sales, Intern | engineering |
| QA or test engineer | QA, Quality Assurance, Test Engineer, SDET, Automation Engineer | Manager, Director, Recruiter, Intern, Quality Control, Food | engineering |
| Engineering manager | Engineering Manager, Manager Software, Software Development Manager, Head of Engineering | Product Manager, Project Manager, Program Manager, Recruiter | engineering |
| VP or head of engineering | VP Engineering, Vice President of Engineering, VP of Engineering, Head of Engineering, CTO, Chief Technology Officer | Sales Engineering, Solutions Engineering, Assistant, Recruiter | vp, c_suite, director; engineering |

## 3. Product and design

| Role | `title` | `notTitle` |
|-|-|-|
| Product manager | Product Manager, Product Owner, Group Product Manager, Senior PM | Project Manager, Program Manager, Product Marketing, Production, Recruiter, Intern |
| Product designer | Product Designer, UX Designer, UI/UX, Interaction Designer, Experience Designer | Graphic, Interior, Fashion, Instructional, Recruiter, Intern |
| Head of product | VP Product, Vice President of Product, Head of Product, Chief Product Officer, CPO | Marketing, Production, Assistant, Recruiter |

## 4. Go-to-market

| Role | `title` | `notTitle` |
|-|-|-|
| Account executive | Account Executive, Enterprise Account Executive, Sales Executive, Account Manager | Assistant, Coordinator, Development Representative, SDR, BDR, Director, VP, Recruiter, Intern |
| SDR or BDR | Sales Development, Business Development Representative, SDR, BDR | Manager, Director, VP, Recruiter |
| Sales leader | VP Sales, Vice President of Sales, Head of Sales, Chief Revenue Officer, CRO, Sales Director | Assistant, Operations, Enablement, Engineer, Recruiter |
| Customer success manager | Customer Success Manager, CSM, Client Success, Account Manager | Director, VP, Support Specialist, Recruiter, Intern |
| Demand generation | Demand Generation, Growth Marketing, Performance Marketing, Marketing Manager | Director, VP, Coordinator, Intern, Recruiter |
| Marketing leader | VP Marketing, Head of Marketing, CMO, Chief Marketing Officer, Marketing Director | Assistant, Coordinator, Recruiter, Intern |
| GTM engineer (builds enrichment, routing and outbound automation) | GTM Engineer, Go-To-Market Engineer, Growth Engineer, Revenue Engineer, Marketing Automation Engineer, Outbound Engineer | Sales Engineer, Solutions Engineer, Software Engineer, Recruiter, Intern |
| Revenue operations (owns CRM policy, forecast, routing rules) | Revenue Operations, RevOps, Sales Operations, Sales Ops, GTM Operations, Marketing Operations, CRM Manager | Engineer, Recruiter, Assistant, Coordinator, Intern |
| Sales or solutions engineer (technical win on deals) | Sales Engineer, Solutions Engineer, Solutions Consultant, Pre-Sales, Presales | Software Engineer, Recruiter, Intern, Field Service |

The three titles above overlap in the market: a "Growth Engineer" can be a product engineer and a "Solutions Engineer" can be post-sales. Read a sample of rows from each family and move drag-ins to `notTitle` before pulling.

### Fields the data cannot filter for GTM roles

Quota attainment, deal size, sales motion (inbound, outbound, product-led) and ramp history are not in any database. Write them in the role brief under "Screened by a human" and ask them on the first call: the last four quarters' quota and attainment, average deal size, cycle length, and how much pipeline the rep sourced.

## 5. Finance, people and operations

| Role | `title` | `notTitle` |
|-|-|-|
| Controller | Controller, Financial Controller, Assistant Controller, Accounting Manager | Air Traffic, Game, Flight, Recruiter, Intern |
| FP&A | FP&A, Financial Planning, Financial Analyst, Finance Manager | Intern, Recruiter, Advisor, Sales |
| CFO | CFO, Chief Financial Officer, VP Finance, Head of Finance | Assistant, Recruiter |
| HR business partner | HR Business Partner, HRBP, People Partner | Recruiter, Coordinator, Intern |
| Recruiter (when hiring recruiters) | Recruiter, Talent Acquisition, Sourcer, Talent Partner | Intern, Coordinator |
| Operations manager | Operations Manager, Ops Manager, Business Operations | Sales Operations, Revenue Operations, Intern, Recruiter |

## 6. Seniority and department values

The `query_lead_database` tool documents seniority examples `vp`, `director` and `c_suite`, and department examples `sales` and `engineering`. The shared quality standard uses this seniority vocabulary: owner, founder, c_suite, partner, vp, head, director, manager, senior, entry. Before using any value not documented by the tool, run the search with `limit: 1`, open the returned row, and confirm the seniority or department field shows the value you expect. If a value returns 0, drop it and use title terms instead.

| Level in the brief | First try | Fallback |
|-|-|-|
| Junior | `seniority: ["entry"]` (probe) | `notTitle` adds Senior, Staff, Lead, Principal |
| Mid-level | No seniority filter | `notTitle` adds Senior, Staff, Principal, Junior |
| Senior | `seniority: ["senior"]` (probe) | `title` terms with Senior, Sr, Staff, Lead |
| Staff, principal | `title` adds Staff, Principal, Lead | none |
| Manager | `seniority: ["manager"]` (probe) | `title` adds Manager |
| Director | `seniority: ["director"]` | none |
| VP | `seniority: ["vp"]` | none |
| C-level | `seniority: ["c_suite"]` | none |

## 7. Location patterns

| Need | Filters |
|-|-|
| One metro | `city` (comma-separated for several cities), `state`, `country` |
| A state | `state`, `country` |
| Remote within a time zone | `state` list for that zone, `country` |
| Company based in a region, person anywhere | `companyCountry`, `companyState`, `companyCity` |

Person filters (`country`, `state`, `city`) describe where the person sits; company filters (`companyCountry` and siblings) describe headquarters. Recruiting usually needs the person filters.

## Sources

- Glen Cathey, Boolean Black Belt: https://booleanblackbelt.com/
- Glen Cathey, LinkedIn Recruiter search result discrepancies explored: https://booleanblackbelt.com/2014/10/linkedin-recruiter-search-result-discrepancies-explored/
- ScraperCity CLI and MCP source (Lead Database filter descriptions): https://github.com/scrapercity/scrapercity-cli
- ScraperCity list quality standard (seniority vocabulary): references/list-quality-standard.md
