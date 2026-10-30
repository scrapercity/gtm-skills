# Candidate Shortlist Report: Senior React engineers, Austin, TX

Illustrative example. Prepared 2026-10-13 for Northpoint Talent, a technical recruiting agency. Client: Ledgerline, a payments software company hiring three senior frontend engineers. Plan: Growth ($149/mo). Wallet before run: $121.60. People and companies are fictional and use the reserved `.example` domain; numbers use the 555-01XX range; counts are illustrative.

## Role Brief

| Item | Value |
|-|-|
| Role as written | Senior Frontend Engineer (React, TypeScript), hybrid 2 days a week in Austin |
| Seniority | Senior individual contributor; not managers |
| Location | Person in Austin, TX metro |
| Pay band | $165,000 to $195,000 base plus equity |
| Selling points | Owns the merchant dashboard end to end; weekly releases with no on-call rotation |
| Target companies | 25 Austin fintech and SaaS companies with React web products: 9 ahead (Series C and later payments companies), 6 competitors, 4 alumni (the VP of Engineering's last two employers and two of the tech lead's), 6 adjacent (finance SaaS selling to the same merchants) |
| Company traits | Fintech or SaaS keywords, 50 to 2,000 employees |
| Screened by a human, not filtered | TypeScript depth, payments domain, work authorization, current compensation |
| Excluded employer domains | ledgerline.example, ledgerlinepay.example (client and its payments subsidiary) |
| Do-not-poach accounts | tallyhq.example, brightfold.example, cobaltcare.example, meridianapps.example (current agency clients) |

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

A first 20-row read found 3 React Native and mobile titles; Mobile, iOS and Android were added to notTitle and the market-wide pull re-run.

QA sample (20 random rows after the final pull): title fit 19 of 20, level fit 19 of 20, location 20 of 20, profile confirmed 5 of 5.

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
| Lead Database counts and pulls | 814 rows | Included in Growth | $0.00 |
| Email Validator on Lead Database emails | 251 emails | $0.00169 | $0.42 |
| Email Finder for A and B without an email | 69 lookups, 41 found | $0.05 per email found | $2.05 |
| Mobile Finder for A tier | 84 inputs, 29 found | $0.25 per number found | $7.25 |
| Total | | | $9.72 |

User go-ahead: agency lead approved the $24.87 ceiling in chat on 2026-10-13. Skipping the Apollo run saved at least the 500-lead minimum ($1.95) and a wait of one to several days.

## Shortlist Sample

| Name | Title | Company domain | Location | Tier | Fit | email_status | Mobile |
|-|-|-|-|-|-|-|-|
| Maya Chen | Senior Frontend Engineer | tallyworks.example | Austin, TX | A | core+level+target | valid | +15125550131 |
| Andre Silva | Senior UI Engineer | pinecrestpay.example | Austin, TX | A | core+level+target | valid | +15125550176 |
| Grace Obi | Senior Web Engineer | orbitfin.example | Round Rock, TX | A | core+level+target | valid | none found |
| Tomas Reyes | Senior JavaScript Engineer | cedarloop.example | Austin, TX | B | core+level | valid | not run |
| Hana Ito | Senior Frontend Engineer | quillpoint.example | Austin, TX | B | core+level | catch_all | not run |
| Priya Nair | Senior Full Stack Engineer | pinecrestpay.example | Austin, TX | B | adjacent+level+target | valid | not run |

## Outreach Plan

| Step | Channel | Timing | Rule |
|-|-|-|-|
| 1 | Email from the recruiter | Day 1, Sunday to Thursday | Under 400 characters: one line on the candidate's work, the role, the pay band, one selling point, a 15-minute ask |
| 2 | Call to A-tier mobiles | Day 2 | Recruiter dials; the opener references the email |
| 3 | LinkedIn connection note | Day 3, the recruiter's choice | Short, references the email |
| 4 | Email follow-up | Day 8 | New detail: team size, interview steps; LinkedIn's data puts 90% of replies within a week, so this goes out once that week has passed |
| 5 | Final email | Day 14, the recruiter's choice | Closes the loop and asks for a referral; anyone who opts out goes on the agency suppression list the same day |

## Message Drafts

The recruiter replaces the first line per candidate with one specific detail from their profile or their company's product; `{{first_name}}` and `{{company}}` are sequencer fields.

### Email 1, day 1 (289 characters before merge fields fill)

> Hi {{first_name}}, your frontend work at {{company}} is why I'm writing. An Austin payments software company is hiring senior React engineers to own its merchant dashboard: TypeScript, hybrid two days a week, $165k to $195k base plus equity, no on-call. Open to a 15-minute call this week?

### Email 3, day 14 (189 characters before merge fields fill)

> {{first_name}}, I'll stop here. If someone you've worked with would want this role ($165k to $195k, hybrid Austin), I'd be glad to hear their name. If timing changes for you, reply anytime.

## Next Steps

1. Import the 320 shortlisted candidates into Greenhouse as prospects in the role's pool, stage sourced, with source "ScraperCity, target companies" (tagged ahead, competitor, alumni or adjacent) or "ScraperCity, market-wide", so replies and hires count per search. Load the 255 with valid emails into the sequence in two waves, A tier first; alumni candidates get a first line naming the shared employer.
2. Hold the 22 catch-all candidates for LinkedIn outreach; re-validate the 5 unknown emails before the second wave.
3. Recruiter calls the 29 A-tier mobiles in week one.
4. Tag every reply interested, not now, not looking, wrong fit, referred or opt out. After the first wave, the title term drawing the most wrong fit replies moves to notTitle, and the target reason with the lowest reply rate gets a smaller share of the next recount (new people only).
5. Re-check title and employer for anyone not contacted by 2026-12-12, the agency's chosen wait; record how many had moved to set the next search's wait.
