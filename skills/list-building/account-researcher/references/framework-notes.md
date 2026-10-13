# Framework Notes: Account Researcher

Which named sources shape this skill, what each one contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Pull the snapshot, count teams, find people at the domain | `research-playbook.md` sections 1-3 |
| Decide whether a technology is worth $4.99 to check | `tech-stack-decision-guide.md` section 1 |
| Find a free signal for a technology before paying | `tech-stack-decision-guide.md` section 3 |
| Collect and sort trigger events | `research-playbook.md` section 4 |
| Read a public company's filings | `research-playbook.md` section 5 |
| Write talking points and the contact plan | `research-playbook.md` sections 6-7 |
| Pick roles for the product category | The role map in the `decision-maker-finder` skill |
| Name columns and validation buckets | `references/list-quality-standard.md` (shared) |
| Quote a price or a parameter | `references/scrapercity-catalog.md` (shared) |
| Check Berman's personalization levels and sequencing advice | `references/alex-berman-cold-email.md` (shared) |

## Sources and what each contributes

### Gartner, buying groups

Gartner's B2B buying research describes buying groups of roughly 6 to 10 decision makers for a complex purchase, each gathering information on their own. Applied here: the brief names 3-4 of them with a role each, so the rep knows who else will be in the room and who to approach next.

### MEDDIC

Created at PTC in 1996 by Dick Dunkel with Jack Napoli under John McMahon. The letters are Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain and Champion. A pre-call brief can fill three of them from outside evidence: Economic Buyer (the person who signs), Champion (the person who feels the problem and will push), and a first guess at Identify Pain. Metrics, Decision Criteria and Decision Process come from the call itself, so the brief lists them as open questions.

### Craig Elias, trigger events

Elias (CustomerThink, July 2008; *SHiFT!*, with Tibor Shanto) describes three buying modes: status quo, the window of dissatisfaction, and searching for alternatives. Trigger events move a buyer into the window, and he groups them as bad experiences, transitions (new legislation, changed management priorities, a new buyer) and awareness. He argues that reaching a buyer in the window leads to more sales and shorter cycles than reaching one already comparing vendors. Applied here: every Why Now signal is typed with one of the three categories, and transitions (a new executive, a new team, a rebuild posted as a job) get the most weight in the contact plan.

### US SEC, EDGAR

EDGAR full-text search covers filings since 2001. For a public company the 10-K business section and risk factors describe priorities and problems in the company's own words, and Form 8-K Item 5.02 reports departures and appointments of certain officers. Applied here: for public accounts, filings outrank press coverage as evidence.

### Alex Berman, personalization levels

His templates page (alexberman.com/cold-email-templates) describes three levels of personalization: segment (role, industry, size), account (news, funding, hiring, leadership change) and person (a post, podcast or talk), matched to how valuable the buyer is. His Single Grain video and the Lean B2B interview add the account sequencing rule used in the contact plan: start at the top, move down a level after one to two weeks without a reply, and do not email several people at one company at once. Details in `references/alex-berman-cold-email.md`.

### ScraperCity tool behavior

From the published package (version 1.0.17): Tech Stack Search takes one `technology` and returns the domains detected using it at $4.99 per technology; Website Finder takes one `jobTitle` per request; Email Finder results are validated at lookup; the Email Validator returns `sc_mx_provider` and `sc_mx_security_gateway`, which reveal the mail platform and any security gateway for $0.0072.

## What this skill does not use

- People Finder (`find_people`) and other public-record tools. A sales brief covers people in their work role; consumer public records are out of scope (see `references/scrapercity-platform.md`, compliance boundaries).
- Intent data feeds. Signals here come from sources a rep can open and cite.

## Sources

- Gartner, The B2B buying journey: https://www.gartner.com/en/sales/insights/b2b-buying-journey
- MEDDICC, Who created MEDDIC: https://meddicc.com/resources/who-created-meddic
- Craig Elias, What's the BIG deal about trigger events (CustomerThink, 2008): https://customerthink.com/whats_big_deal_about_trigger_events/
- SEC, EDGAR full-text search: https://www.sec.gov/edgar/search/
- SEC, Form 8-K instructions (Item 5.02): https://www.sec.gov/files/form8-k.pdf
- Alex Berman, Cold email templates: https://alexberman.com/cold-email-templates
- ScraperCity npm package: https://www.npmjs.com/package/scrapercity
