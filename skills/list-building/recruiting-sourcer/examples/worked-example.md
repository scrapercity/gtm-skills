# Candidate Shortlist Report: Senior React engineers, Austin, TX

Prepared 2026-10-13 for Northpoint Talent, a technical recruiting agency. Client: Ledgerline, a payments software company hiring three senior frontend engineers. Plan: Growth ($149/mo). Wallet before run: $121.60. People and companies are fictional and use the reserved `.example` domain; numbers use the 555-01XX range; counts are illustrative.

## Role Brief

| Item | Value |
|-|-|
| Role as written | Senior Frontend Engineer (React, TypeScript), hybrid 2 days a week in Austin |
| Seniority | Senior individual contributor; not managers |
| Location | Person in Austin, TX metro |
| Target companies | 25 Austin fintech and SaaS companies with React web products (poach list from the client) |
| Company traits | Fintech or SaaS keywords, 50 to 2,000 employees |
| Screened by a human, not filtered | TypeScript depth, payments domain, work authorization, compensation |
| Excluded employer domains | ledgerline.example, ledgerlinepay.example (client and its payments subsidiary) |
| Do-not-poach accounts | tallyhq.example, brightfold.example, cobaltcare.example, meridianapps.example (agency clients under non-solicit) |

## Search Strings

| Parameter | Value | Why |
|-|-|-|
| title | React, Frontend, Front End, Front-End, UI Engineer, JavaScript Engineer, Web Engineer | Frontend family; partial match catches level prefixes |
| notTitle | Native, Mobile, iOS, Android, Manager, Director, Head of, VP, Recruiter, Designer, QA, Intern, Instructor, Contract | Removes mobile, management, design and recruiter drag-ins |
| seniority | senior | Probed with limit 1; returned rows showed senior in the seniority field |
| department | engineering | Documented value |
| companyDomain | 25 poach-list domains in 3 batches | Target-company search |
| city, state, country | Austin; Texas; United States | Person location for the market-wide search |
| keywords | fintech, saas | Market-wide company traits |
| minEmployees, maxEmployees | 50, 2,000 | Product companies with a frontend team |

## Count Check

| Search | pagination.total | Decision |
|-|-|-|
| Target companies, 3 batches of up to 10 domains | 214 | Pull all |
| Market-wide, Austin, senior, fintech or saas | 1,140 | Pull 600, about twice the shortlist need |
| Client's Apollo URL passed as url | 690 | search_translation applied titles and location, approximated seniority; Lead Database covers it, so no Apollo run |

QA on a 20-row sample found 3 React Native and mobile titles; Mobile, iOS and Android were added to notTitle and the market-wide pull re-run.

## Sourcing Funnel

| Stage | Rows | Dropped | Reason |
|-|-|-|-|
| Pulled across both searches | 814 | 0 | 214 target-company and 600 market-wide |
| After dedupe | 718 | 96 | Same person in both searches |
| After removing the hiring company | 695 | 23 | Current Ledgerline and Ledgerline Pay employees |
| After removing do-not-poach accounts | 654 | 41 | Four current agency clients |
| After re-pull with the updated notTitle | 616 | 38 | Mobile and React Native titles |
| Shortlist, A and B tiers | 320 | 296 | C tier moved to the long list without paid enrichment |

## Contact Coverage

| Measure | Count |
|-|-|
| Shortlisted candidates (A and B) | 320 |
| Valid email from the Lead Database | 214 |
| Valid email from Email Finder | 41 |
| Catch-all email, held | 22 |
| No usable email | 43 |
| A-tier candidates | 84 |
| A-tier mobiles found | 29 |

Lead Database emails validated: 251 (214 valid, 22 catch_all, 5 unknown, 10 invalid). Email Finder ran on 69 shortlisted candidates without a usable email and found 41.

## Cost Estimate

| Line | Units | Unit price | Cost |
|-|-|-|-|
| query_lead_database counts and pulls | 814 rows | Included in Growth | $0.00 |
| validate_emails on Lead Database emails | 251 emails | $0.0072 | $1.81 |
| find_emails for A and B without an email | 69 lookups, 41 found | $0.05 per email found | $2.05 |
| find_mobiles for A tier | 84 inputs, 29 found | $0.25 per number found | $7.25 |
| Total | | | $11.11 |

User go-ahead: agency lead approved the $26.26 ceiling in chat on 2026-10-13. Skipping the Apollo run saved at least the 500-lead minimum ($1.95) and a wait of one to several days.

## Compliance Check

| Item | Answer | Law or rule | Action |
|-|-|-|-|
| Email to US candidates | Work emails, one recruiter domain | CAN-SPAM | Sender identity, agency postal address, opt-out honored within 10 business days |
| Calls | Recruiter dials A-tier mobiles by hand | TCPA, 47 U.S.C. 227(b) | No autodialer, prerecorded or AI voice |
| Texts | None without consent | TCPA, 47 CFR 64.1200 | One manual text only after a call the candidate agreed to |
| Filters and ranking | Title, seniority, company, location | EEOC guidance; ADEA | No graduation year or other age or protected-trait proxies |
| Automated screening | Manual rubric reviewed by the recruiter | NYC Local Law 144 | Not an automated tool; role is in Austin |
| Background data | None collected | FCRA | No People Finder or Criminal Records on candidates |
| Poaching | Four clients excluded | Client contract non-solicitation clauses | Domains on the do-not-poach list for every search |

## Shortlist Sample

| Name | Title | Company domain | Location | Tier | Rank score | email_status | Mobile |
|-|-|-|-|-|-|-|-|
| Maya Chen | Senior Frontend Engineer | tallyworks.example | Austin, TX | A | 100 | valid | +15125550131 |
| Andre Silva | Staff UI Engineer | pinecrestpay.example | Austin, TX | A | 90 | valid | +15125550176 |
| Grace Obi | Senior Software Engineer, Web | orbitfin.example | Round Rock, TX | A | 85 | valid | none found |
| Tomas Reyes | Senior JavaScript Engineer | cedarloop.example | Austin, TX | B | 70 | valid | not run |
| Hana Ito | Frontend Engineer | quillpoint.example | Austin, TX | B | 65 | catch_all | not run |

## Outreach Plan

| Step | Channel | Timing | Rule |
|-|-|-|-|
| 1 | Email from the recruiter | Day 1, weekday morning | Names the role, the client type (payments software), the hybrid schedule and the pay band; opt-out line |
| 2 | Manual call to A-tier mobiles | Day 2 | 8 a.m. to 9 p.m. local; no voicemail drops by software |
| 3 | LinkedIn connection note | Day 3 | Short, references the email |
| 4 | Email follow-up | Day 6 | New detail: team size, stack, interview steps |
| 5 | Final email | Day 12 | Closes the loop; anyone who opts out goes on the agency suppression list |

## Next Steps

1. Load the 255 candidates with valid emails into the recruiter's sequence in two waves (A tier first).
2. Hold the 22 catch-all candidates for LinkedIn outreach; re-validate the 5 unknown emails after 72 hours.
3. Recruiter calls the 29 A-tier mobiles in week one.
4. Report replies and screens to the client weekly; recount the market-wide search with excludeDelivered set to true in 30 days for new people.
5. Delete long-list rows for people never contacted when the search closes.
