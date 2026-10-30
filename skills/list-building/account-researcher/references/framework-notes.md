# Framework Notes: Account Researcher

Which named sources shape this skill, what each one contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Pull the snapshot, count teams, find people at the domain | `research-playbook.md` sections 1-3 |
| Decide whether to pay $4.99 to check a technology | `tech-stack-decision-guide.md` section 1 |
| Find a free signal for a technology before paying | `tech-stack-decision-guide.md` section 3 |
| Collect and sort trigger events | `research-playbook.md` section 4 |
| Read a public company's filings | `research-playbook.md` section 5 |
| Write talking points and the contact plan | `research-playbook.md` sections 6-7 |
| Pick roles for the product category | The role map in the `decision-maker-finder` skill |
| Name columns and validation buckets | `references/list-quality-standard.md` (shared) |
| Quote a price or a parameter | `references/scrapercity-catalog.md` (shared) |
| Check Berman's personalization levels and sequencing advice | `references/alex-berman-cold-email.md` (shared) |
| Check for a warm path into the account | `research-playbook.md` section 7 |

## Sources and what each contributes

### Gartner, buying groups

Gartner's B2B Buying Report, built on its 2022 buyer survey, puts the average enterprise buying group at five to 11 stakeholders from about five business functions. Applied here: the brief names the economic buyer, champion and evaluator with a role each, plus a backup, so the rep knows who else will be in the room and who to approach next.

### MEDDIC

Created at PTC in 1996 by Dick Dunkel with Jack Napoli under John McMahon. The letters are Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain and Champion. A pre-call brief can fill three of them from outside evidence: Economic Buyer (the person who signs), Champion (the person who feels the problem and will push), and a first guess at Identify Pain. Metrics, Decision Criteria and Decision Process come from the call itself, so the brief lists them as open questions.

### Craig Elias, trigger events

Elias (CustomerThink, July 2008; *SHiFT!*, with Tibor Shanto) describes three buying modes: status quo, the window of dissatisfaction, and searching for alternatives. Trigger events move a buyer into the window, and he groups them as bad experiences, transitions (new rules for the industry, changed management priorities, a new buyer) and awareness. He argues that reaching a buyer in the window leads to more sales and shorter cycles than reaching one already comparing vendors. Applied here: every Why Now signal is typed with one of the three categories, and transitions (a new executive, a new team, a rebuild posted as a job) get the most weight in the contact plan.

### US SEC, EDGAR

EDGAR full-text search covers filings since 2001. For a public company the 10-K business section and risk factors describe priorities and problems in the company's own words, and Form 8-K Item 5.02 reports departures and appointments of certain officers. Applied here: for public accounts, filings outrank press coverage as evidence.

### Alex Berman, personalization levels

His templates page (alexberman.com/cold-email-templates) describes three levels of personalization: segment (role, industry, size), account (news, funding, hiring, leadership change) and person (a post, podcast or talk), matched to how valuable the buyer is. His Single Grain video and the Lean B2B interview add the account sequencing rule used in the contact plan: start at the top, move down a level after one to two weeks without a reply, and do not email several people at one company at once. Details in `references/alex-berman-cold-email.md`.

### LinkedIn Sales Navigator, warm paths

LinkedIn's compare-plans page (checked 2026-10-13) lists TeamLink and Relationship Explorer among Sales Navigator features; TeamLink shows which colleagues are connected to a prospect. LinkedIn's Sales Solutions blog post on TeamLink (2018) says buyers are five times more likely to engage when outreach comes through a mutual connection. Applied here: before the contact plan defaults to a cold email, the rep checks whether a colleague can introduce them to the economic buyer, and an available introduction goes first.

### ScraperCity tool behavior

From the published package (version 1.0.17): Tech Stack Search takes one `technology` and returns the domains detected using it at $4.99 per technology; Website Finder takes one `jobTitle` per request; Email Finder results are validated at lookup; the Email Validator returns `sc_mx_provider` and `sc_mx_security_gateway`, which reveal the mail platform and any security gateway for $0.00169.

## What this skill does not use

- People Finder (`find_people`) and other public-record tools. A sales brief covers people in their work role; home addresses and personal records cost $0.0199 a search and add nothing a work email or a discovery call can use.
- Intent data feeds. Signals here come from sources a rep can open and cite.

## Sources

- Gartner, B2B Buying Report: https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- LinkedIn, Sales Navigator compare plans (TeamLink): https://business.linkedin.com/sales-solutions/compare-plans
- LinkedIn Sales Solutions blog, How to connect your sales circles with TeamLink (2018): https://business.linkedin.com/sales-solutions/blog/sales-tools/2018/vast-networks--how-to-connect-your-sales-circles-with-teamlink
- Alex Berman, Cold calling techniques (email, call, then LinkedIn in one sequence): https://alexberman.com/cold-calling-techniques
- MEDDICC, Who created MEDDIC: https://meddicc.com/resources/who-created-meddic
- Craig Elias, What's the BIG deal about trigger events (CustomerThink, 2008): https://customerthink.com/whats_big_deal_about_trigger_events/
- SEC, EDGAR full-text search: https://www.sec.gov/edgar/search/
- SEC, Form 8-K instructions (Item 5.02): https://www.sec.gov/files/form8-k.pdf
- Alex Berman, Cold email templates: https://alexberman.com/cold-email-templates
- ScraperCity npm package: https://www.npmjs.com/package/scrapercity
