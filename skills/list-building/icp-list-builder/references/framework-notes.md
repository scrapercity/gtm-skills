# Framework Notes: ICP List Builder

Which sources shape this skill, what each one contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Turn example customers and lost deals into filters and exclusions | `icp-evidence-worksheet.md` |
| Run the lift check on a CRM export of closed deals | `icp-evidence-worksheet.md` section 4 |
| Start from a vertical recipe | `icp-filter-recipes.md` |
| Translate a Sales Navigator search, or turn Sales Navigator signals into emails | `sales-navigator-filter-map.md` |
| Write the `title` and `notTitle` strings, or split the buying group into role families | `title-synonyms-and-exclusions.md` |
| Decide whether a count is too big or too small, page the results, handle a 503 | `count-and-paging-runbook.md` |
| Count companies with no call available, benchmark a database count, or handle size-band edges | `count-and-paging-runbook.md` sections 9 and 10 |
| See the format of a run report or a plan report | `examples/worked-example.md`, `examples/plan-example.md` |
| Name columns, normalize, dedupe, bucket validation results, score the fit sample | `references/list-quality-standard.md` (shared) |
| Quote a price or a parameter | `references/scrapercity-catalog.md` (shared) |
| Check plan access or the daily allowance | `references/scrapercity-platform.md` (shared) |

## Sources and what each contributes

### April Dunford, best-fit customers

Dunford's positioning method starts from the customers who understood the product quickly, bought it and got strong value, then asks what those accounts share. This skill applies the same method to list building: the example customers are best-fit accounts, and only traits they all share become filters. One unusual customer never sets a filter. The skill adds the mirror image Dunford's method implies: accounts that bought and left, or were lost on fit, supply the exclusions.

Applied rule: ask for the 3-5 customers who closed fastest and renewed or expanded, not the biggest logos, plus 2-5 that were lost on fit or churned soon after buying.

### Gartner, buying groups

Gartner's B2B Buying Report, built on its 2022 B2B buyer survey, puts the average enterprise buying group at five to 11 stakeholders from about five business functions. An outbound list reaches a few of them on purpose: the budget owner, the day-to-day owner, and a user lead or technical evaluator.

Applied rules: one query per role family; contacts per account fall by tier and never exceed the group; in a plan report, firms x 5-11 bounds the people who decide. At small companies one person often holds two roles.

### Alex Berman, narrow lists

Alex Berman's companies have booked 500k+ meetings. A secondhand account of his early agency work describes a campaign aimed at about 50 universities that resembled one case study, which led to meetings at Yale, UCLA and Ohio State. The principle used here: the closer the list is to the case study the email cites, the better it converts, so a smaller tight list beats a large loose one. In a Lean B2B interview (December 2020) he describes testing each niche with about 100 emails before going further.

Applied rules: when the count is many times the target, tighten instead of pulling the top N; release a new list as a 100-contact test cell first. His TAM breakdown (alexberman.com, October 2026) sends one email per person per cycle and spaces cycles 30 to 60 days apart, the default re-contact window when the user has none.

### Win-rate lift

When the user has a CRM export of closed deals, counting how many examples share a trait wastes the evidence. Lift compares the win rate of deals with a trait to the overall win rate; above 1 the trait wins more often than average. No published source sets the cutoffs, so the user sets the filter lift, the exclusion lift and the minimum deals per trait, and the report records them.

### US Census Bureau, Statistics of U.S. Businesses

SUSB counts US firms by NAICS industry and enterprise employment size, from 200-299 employees up through 1,500-1,999 and beyond (2022 data, released April 2025). Its employment counts include hourly staff, and a firm is counted in every industry where it has an establishment.

Applied rule: a plan report takes its company count from SUSB, as a ceiling when it sums several industries; a run report shows SUSB next to the deduped database count.

### Pew Research Center, LinkedIn use by education

Pew's January 2024 report on Americans' social media use found 10% of US adults with a high school education or less use LinkedIn, against 53% of college graduates (survey May to September 2023).

Applied rule: in industries with mostly hourly staff, the band below the floor is counted and companies join when their own site states an in-band headcount.

### Eypasch, Lefering, Kum and Troidl, BMJ 1995

When an event never occurs in n checks (n over 30), the upper 95% confidence limit on its rate is about 3/n.

Applied rule: the fit sample is sized as n = 3 / the misfit ceiling; 60 rows with no misses caps misfits under 5%.

### LinkedIn Sales Navigator

Sales Navigator is where many reps build searches. Its title, seniority, function, geography, headcount and industry filters map onto Lead Database parameters; its spotlights (changed jobs in the last 90 days, posted in the last 30 days, following your company) have no database equivalent and work as weekly timing signals. Prices from LinkedIn's compare-plans page, checked 2026-10-13: Core $99.99 a month, Advanced $179.99 a month per seat.

Applied rule: Sales Navigator decides when, the Lead Database supplies the validated contact data, joined by `socialUrl`.

### Mailbox providers: Google, Yahoo, Microsoft

- Google (bulk sender rules announced October 2023, enforced from February 2024): senders above 5,000 messages a day to Gmail authenticate, offer one-click unsubscribe, honor unsubscribes within 48 hours and keep spam rate under 0.1%, never reaching 0.3% (Google sender FAQ, checked 2026-10-13).
- Yahoo Sender Hub: remove invalid recipients promptly, monitor bounces, keep spam rate below 0.3%.
- Microsoft Outlook (enforced May 5, 2025 for senders over 5,000 a day): SPF, DKIM and DMARC required; list hygiene and removing invalid addresses listed among the practices it expects.

Applied rule: nothing reaches the main CSV without `validate_emails` returning valid, and every pull is checked against one suppression list shared by every sending tool.

### Sequencer bounce guards

Instantly pauses a campaign whose bounce rate exceeds 5% after 200 sends by default. Smartlead lets the user set a pause threshold. Alex Berman's templates page says to keep bounces under 2%. Applied rule: the list targets a projected bounce rate under 2%.

### Bureau of Labor Statistics, tenure

Median employee tenure was 4.1 years in January 2026, and ZeroBounce's 2025 Email List Decay Report (2024 data) found email databases degrade by at least 28% a year. Applied rule: a contact list ages; re-validate before every send.

## What this skill does not do

- Event-driven lists (funding, hiring, job changes across a market). Use `signal-triggered-outbound`.
- Weighted lift scores across a whole account universe, TAM/SAM/SOM and spend ceilings. `tam-builder` does that; this skill tiers the accounts it pulls by columns every account has.
- Message writing per segment or per Sales Navigator signal. Use `cold-email-copywriting` or `multi-channel-outreach`.

## Sources

- April Dunford, A quickstart guide to positioning: https://www.aprildunford.com/post/a-quickstart-guide-to-positioning
- Gartner, B2B Buying Report: https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- Hackernoon, Cold Email is not Dead (Scott D. Clary on Alex Berman): https://hackernoon.com/cold-email-is-not-dead-mb4v35g4
- LinkedIn, Sales Navigator compare plans: https://business.linkedin.com/sales-solutions/compare-plans
- Google, Gmail sender requirements announcement: https://blog.google/products/gmail/gmail-security-authentication-spam-protection/
- Google, Email sender guidelines FAQ: https://support.google.com/a/answer/14229414
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook high-volume sender requirements: https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Smartlead, High bounce rate auto protection: https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- BLS, Employee Tenure news release: https://www.bls.gov/news.release/tenure.nr0.htm
- ZeroBounce, Email List Decay Report (February 2025): https://www.zerobounce.net/blog/newsroom/press/zerobounce-report-email-list-decay
- Alex Berman, Cold email templates (bounces under 2%): https://alexberman.com/cold-email-templates
- Alex Berman, Map your market, skip the follow-ups (30 to 60 day cycles): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Lean B2B, Alex Berman on evaluating B2B market segments with cold email (December 2020): https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- US Census Bureau, 2022 SUSB annual data tables: https://www.census.gov/data/tables/2022/econ/susb/2022-susb-annual.html
- Pew Research Center, Americans' Social Media Use (January 31, 2024): https://www.pewresearch.org/internet/2024/01/31/americans-social-media-use/
- Eypasch E, Lefering R, Kum CK, Troidl H. Probability of adverse events that have not yet occurred: a statistical reminder. BMJ 1995;311:619: https://www.bmj.com/content/311/7005/619
