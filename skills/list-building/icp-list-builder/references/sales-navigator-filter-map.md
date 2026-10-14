# Sales Navigator to Lead Database Filter Map

For a user who works in LinkedIn Sales Navigator and wants the same people with verified emails, or wants Sales Navigator's timing signals to decide who gets emailed this week. Sales Navigator facts below were checked on 2026-10-13: plan prices and the alert and intent features on LinkedIn's compare-plans page, spotlight and core filter names in LinkedIn's Sales Navigator community, and the filter groups (Buyer intent, Best path in, Recent updates, Workflow) as listed in an August 2026 filter walkthrough. Other filter names are as labeled in the Sales Navigator search panel; LinkedIn renames filters from time to time, so read the names in the user's own search before mapping.

| Plan (LinkedIn, per seat) | Monthly | Annual |
|-|-:|-:|
| Sales Navigator Core | $99.99 | $959.88 |
| Sales Navigator Advanced | $179.99 | $1,679.88 |

## 1. Lead filters

| Sales Navigator lead filter | Lead Database parameter | How to map it |
|-|-|-|
| Current job title (Boolean) | `title`, `notTitle` | Terms joined by OR go in `title` as a comma list; terms after NOT go in `notTitle`. There is no AND: express it with `seniority` or `department`, or run two counts |
| Seniority level | `seniority` | The tool documents `vp`, `director`, `c_suite`; test any other value with a `limit: 1` call and read the rows |
| Function | `department` | The tool documents `sales`, `engineering`; test others the same way |
| Geography (where the person is) | `country`, `state`, `city` | Full country names ("United States"); US, USA, UK and UAE also work |
| Company headquarters | `companyCountry`, `companyState`, `companyCity` | Keep person geography and HQ geography apart; mixing them is the usual cause of a count that disagrees |
| Current company | `companyDomain` (preferred) or `companyName` | Domains match better than names |
| Company headcount | `minEmployees`, `maxEmployees` | Sales Navigator uses bands; use the band edges (11-50 becomes 11 and 50) |
| Industry | `industry` or `keywords` | Labels differ between the two products. Count with `industry`, then with `keywords` only, and keep the one whose sample rows fit |
| Keywords | `keywords` | Not equivalent: Sales Navigator searches profile text, the Lead Database matches company tags. Rewrite profile keywords as title words or company tags |
| Past company, Past job title, School, Groups, Years of experience, Years in current company, Years in current position, Profile language, First or last name | None | Keep these in Sales Navigator. If one of them defines the segment (tenure windows, an alumni play), run Workflow B |
| Recent updates: Changed jobs (last 90 days), Posted on LinkedIn, Mentioned in news | None; timing signals | Workflow B, one saved search each |
| Buyer intent: Following your company, Viewed your profile recently | None; timing signals | Workflow B; these two get the first send each week |
| Best path in: Connection, Connections of, Past colleague, Shared experiences, With TeamLink intro | None | Warm paths. Record them in the account brief (`account-researcher`), not in a bulk list |
| Workflow: Lead lists (include or exclude), People in CRM, People you interacted with, Saved leads and accounts, Persona | Suppression files and `excludeDelivered: true` | Export the CRM and past lists as suppression; `excludeDelivered` skips people this account already pulled. A saved Persona is a title, function and seniority bundle: unpack it into `title`, `department`, `seniority` |
| Account lists (include) | `companyDomain`, batches of 25 | The usual ABM case: the account list lives in Sales Navigator, the people come from the Lead Database by domain. Run `decision-maker-finder` for slots per account |

## 2. Account filters

| Sales Navigator account filter | ScraperCity equivalent |
|-|-|
| Company headcount, Annual revenue, Headquarters location | `minEmployees`, `maxEmployees`, `revenueMin`, `revenueMax`, `companyCountry`, `companyState` |
| Industry | `industry` or `keywords`, as above |
| Technologies used | Tech Stack Search (`scrape_builtwith`, $4.99 per technology); feed the returned domains to `companyDomain` in batches of 25 |
| Company or department headcount growth | None. Proxy: compare a department's `limit: 1` count at the domain this month against last month's saved count |
| Funding events, senior leadership changes, hiring, Job opportunities | None in the databases; `signal-triggered-outbound` builds lists from these events |
| Buyer intent (account spotlight) | None. Treat as a timing signal: move the account up one tier for the window the user sets (`tam-builder` scoring) and run Workflow B on its buyers |
| Account lists, Saved accounts, Companies in CRM | `companyDomain` batches for inclusion; suppression files for exclusion |

Sales Navigator has no CSV export button. Advanced Plus syncs saved leads to Salesforce, HubSpot or Dynamics; on Core and Advanced, the profile URLs come from the lead list by hand. Either way the emails come from the Lead Database by `socialUrl` (Workflow B).

## 3. Workflow A: rebuild a Sales Navigator search to get emails

1. Copy the search URL and list every filter in it.
2. Try the URL in the Lead Database: `{"url": "<the search URL>", "hasEmail": true, "limit": 1}`. The tool takes a people-search URL and returns `search_translation` with the filters it applied, approximated or could not support. Whether a given Sales Navigator URL is read at all shows up there; do not assume it.
3. Re-express everything listed under `not_supported` with native parameters from section 1.
4. Compare the two counts. Lead Database total well under the Sales Navigator count: remove one filter at a time to find the one spelled differently. Well over it: a filter was dropped or `keywords` is reading broader than profile keywords did; read a page of rows.
5. Pull, dedupe, suppress, validate and cap exactly as SKILL.md steps 4 to 7.

## 4. Workflow B: Sales Navigator signals, Lead Database emails

Use Sales Navigator for timing and the Lead Database for the contact data.

1. In Sales Navigator, save one search per signal on top of the ICP filters (for example ICP plus "Changed jobs in the last 90 days", ICP plus "Posted on LinkedIn in the last 30 days", ICP plus "Following your company") and turn on alerts.
2. Each week, collect the profile URLs of the new matches.
3. For each URL, call `query_lead_database` with `socialUrl` set to the profile URL and `limit: 1`. A match returns the person with company fields and, often, an email (included in the Growth plan).
4. No match, or no email: send first name, last name and company domain to `find_emails` ($0.05 per email found, free when not found).
5. Validate every email that did not come from Email Finder with `validate_emails` ($0.0072 each).
6. Mobiles only for people a rep will call by hand: `find_mobiles` accepts the profile URL ($0.25 per number found, free when not found).
7. Set `segment` to the signal and week (`job-change-2026-w42`) so the copy can name the trigger.

The saved searches to build on top of the ICP filters, and how each one is worked:

| Saved search (ICP filters plus) | `segment` prefix | Send order in the week | Note for the copy skill |
|-|-|-|-|
| Viewed your profile recently | `viewed-profile` | First | They looked at the sender; a short note, no long pitch |
| Following your company | `follows-co` | First | Already know the brand |
| Changed jobs (last 90 days) | `job-change` | Second | New in seat; first 90 days priorities |
| Years in current company under 1 year | `new-in-company` | Second | Overlaps with job change; dedupe on `socialUrl` before the lookup |
| Posted on LinkedIn (recent) | `posted` | Third | Read the post; reference it only if it is about the problem |
| Mentioned in news | `in-news` | Third | Cite the article |

Measure each saved search on its own: replies and meetings per 100 sent by `segment` prefix, starting once each has about 100 sends (the test size Alex Berman uses for a niche). Drop the saved searches that book the fewest meetings per 100 once the user has enough sends to compare them. Comment, connection-request and DM steps on LinkedIn belong to `multi-channel-outreach`.

Weekly cost ceiling for 60 new signal matches (illustrative; the match rate is a planning assumption, measure your own):

| Item | Units | Unit price | Ceiling |
|-|-:|-:|-:|
| `socialUrl` lookups | 60 | Included in Growth | $0.00 |
| Validation of the 45 database emails (assumed 75% match) | 45 | $0.0072 | $0.32 |
| Email Finder on the other 15 | 15 | $0.05 if found | $0.75 |
| Total ceiling | | | $1.07 |

## 5. Which tool does which job

| Job | Use | Reason |
|-|-|-|
| Timing signals (job change, recent post, follows your company) | Sales Navigator | The Lead Database has no activity fields |
| Warm paths (TeamLink, Connections of) | Sales Navigator | Relationship data |
| Counting a segment before spending | Lead Database | `pagination.total` from a `limit: 1` call |
| 2,000 contacts with validated emails | Lead Database | 100 rows per call, cursor paging, emails returned, 100,000 new leads a day on Growth |
| Technology-defined accounts | Tech Stack Search | One run returns every detected domain |
| What to say to each signal | `cold-email-copywriting` or `multi-channel-outreach` | Copy is outside this skill |

## 6. Mapping mistakes

| Mistake | Effect | Fix |
|-|-|-|
| Treating Sales Navigator keywords as Lead Database keywords | Counts differ widely | Profile words become title words; company words become tags |
| Person geography in `companyCountry` | US companies' overseas staff, or the reverse | `country` is the person, `companyCountry` is HQ |
| Using "Owner" or "Partner" seniority without testing | Zero rows or the wrong layer | `limit: 1` test, read rows, fall back to titles |
| Rebuilding a signal search as a static list | Last month's job changers go stale | Workflow B each week |

## Sources

- LinkedIn, Sales Navigator compare plans (prices checked 2026-10-13): https://business.linkedin.com/sales-solutions/compare-plans
- LinkedIn Sales Navigator community, Best Practice 3: find the right buyers (spotlight filter names, Boolean in title, saved search alerts, May 2023): https://scommunity.linkedin.com/competitions-challenges-40/best-practice-3-find-the-right-buyers-community-challenge-learn-to-become-a-top-seller-with-sales-navigator-in-9-weeks-4598
- SalesRobot, Sales Navigator filters (filter groups including Buyer intent and Workflow, published 2026-08-21): https://salesrobot.co/blogs/sales-navigator-filters
- Cleverly, Export leads from Sales Navigator (no CSV export button; Advanced Plus CRM sync, May 2026): https://www.cleverly.co/blog/export-leads-from-linkedin-sales-navigator
- ScraperCity MCP tool schema for `query_lead_database` (`url`, `socialUrl`, `search_translation`): https://www.npmjs.com/package/scrapercity
- Lean B2B, Alex Berman on evaluating B2B market segments with cold email (about 100 emails per niche, December 2020): https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- ScraperCity catalog (Email Finder, Mobile Finder, Email Validator and Tech Stack Search prices): references/scrapercity-catalog.md
