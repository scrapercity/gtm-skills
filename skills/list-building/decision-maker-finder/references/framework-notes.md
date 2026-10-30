# Framework Notes: Decision Maker Finder

## Routing table

| You are about to | Open |
|-|-|
| Decide which roles to contact and which to map at each account | `buying-role-map.md` |
| Batch domains, rank candidates, choose the next tool for an empty slot, handle failures | `waterfall-runbook.md` |
| Request mobile numbers, plan a call block, read call dispositions | `mobile-and-phone-handling.md` |
| Name columns, normalize, bucket validation results, apply the shared suppression list | `references/list-quality-standard.md` (shared) |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### Gartner: buying groups

Gartner's B2B Buying Report, built on its 2022 B2B buyer survey, puts the average enterprise buying group at five to 11 stakeholders representing about five business functions. Applied here: an outbound list contacts the number of them the user sets, chosen on purpose and sent in order; when procurement, IT security or finance joined the user's past deals of this size, the skill names them in a committee file the AE uses after the first meeting.

### MEDDIC

MEDDIC was created at PTC in 1996 by Dick Dunkel, working with Jack Napoli under John McMahon. The letters stand for Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain and Champion. Two of them shape the slots:

- Economic Buyer: the person who can approve the spend. In outbound, this is slot 1. For most mid-market software and services, it sits at VP level in the department that owns the budget.
- Champion: the person who feels the pain daily and will push for the change. In outbound, this is slot 2, usually a director or manager who will run the tool.

Decision Process is where the committee file earns its keep: the procurement and security names in it are the people the Decision Process will route the deal through. The other letters belong in discovery calls, not in list building.

### Alex Berman: account sequencing

Alex Berman's companies have booked 500,000+ meetings. His published guidance on emailing several people at one company (Single Grain video, Lean B2B interview): start with the most senior relevant person, move down a level after one to two weeks without a reply, and do not email several people at the same company at once, since that can get you blocked company wide. His cold email templates page adds: test one variable at a time. Applied here: slot order is send order, the report hands the sequencer one slot at a time, and the role audit changes the title or the copy, never both.

### Committee size: user inputs

No published source ties a contact count or a committee to a contract value band, so SKILL.md step 2 takes both from the user: contacts per account, and which roles joined their last deals of this size. The role audit threshold and review count in step 9 are also set by the user before launch.

### List quality standard

Validation buckets, per-domain caps, the shared suppression list, the `source` vocabulary and the delivery funnel come from `references/list-quality-standard.md`, shared across list-building skills.

## Tool ordering logic

The waterfall runs from included-in-plan to most expensive per hit:

| Order | Tool | Billing | Why this position |
|-|-|-|-|
| 1 | `query_lead_database` | Included in Growth and Scale | Free per lead within the daily allowance; returns titles, seniority and emails together; also maps committee roles at no wallet cost. |
| 2 | `scrape_website_finder` | $0.0499 per contact found | Searches a domain for a title; only billed on hits. |
| 3 | `find_emails` | $0.05 per email found | Turns a known name into an email; validated at lookup. |
| 4 | `validate_emails` | $0.00169 per email | Required before sending anything not validated at lookup. |
| 5 | `find_mobiles` | $0.25 per number found | Highest cost; optional; only for a planned call block. |
| Side path | `scrape_apollo` | $0.0039 per lead, 500 minimum | For large accounts the database missed; slow (hours to days). Try the same URL in the Lead Database `url` parameter first. |

## Sources

- Gartner, B2B Buying Report: https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- MEDDICC, Who created MEDDIC: https://meddicc.com/resources/who-created-meddic
- Alex Berman, Single Grain video on cold emails: https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- Alex Berman, Cold email templates (test one variable at a time): https://alexberman.com/cold-email-templates
- Lean B2B, Alex Berman on B2B market segments: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- ScraperCity npm package (tool schemas and prices): https://www.npmjs.com/package/scrapercity
