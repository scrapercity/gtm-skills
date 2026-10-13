# Framework Notes: Decision Maker Finder

## Routing table

| You are about to | Open |
|-|-|
| Decide which roles to search at each account | `buying-role-map.md` |
| Batch domains, rank candidates, choose the next tool for an empty slot, handle failures | `waterfall-runbook.md` |
| Request mobile numbers, or contact people outside the US | `mobile-and-contact-compliance.md` |
| Name columns, normalize, bucket validation results | `references/list-quality-standard.md` (shared) |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |
| Check country-specific rules in full | `references/outbound-compliance-primer.md` (shared) |

## Sources and what each contributes

### Gartner: buying groups

Gartner's B2B buying research describes the typical buying group for a complex solution as 6 to 10 decision makers, each arriving with information gathered on their own. Applied here: an outbound list reaches 2-3 of them, chosen on purpose. Mapping all 6 to 10 belongs to account-based selling after a reply, so this skill stops at 3.

### MEDDIC

MEDDIC was created at PTC in 1996 by Dick Dunkel, working with Jack Napoli under John McMahon. The letters stand for Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain and Champion. Two of them shape the slots in this skill:

- Economic Buyer: the person who can approve the spend. In outbound, this is slot 1. For most mid-market software and services, it sits at VP level in the department that owns the budget.
- Champion: the person who feels the pain daily and will push for the change. In outbound, this is slot 2, usually a director or manager who will run the tool.

The other letters belong in discovery calls, not in list building.

### FCC and the TCPA

47 CFR 64.1200(a)(1)(iii) bars autodialed or artificial or prerecorded voice calls to cell numbers without prior express consent, and the rule has no business-to-business carve-out. Applied here: Mobile Finder results are for manual, one-to-one calls by a person, or for texts only with consent. The mobile compliance reference spells out the decision.

### FTC: CAN-SPAM and the Telemarketing Sales Rule

CAN-SPAM covers B2B email with no exemption. The Telemarketing Sales Rule exempts most business-to-business calls from the National Do Not Call Registry, with exceptions such as retail sales of nondurable office or cleaning supplies. The TSR exemption does not override the TCPA's mobile autodialer rule.

### List quality standard

Validation buckets, per-domain caps, the `source` vocabulary and the delivery funnel come from `references/list-quality-standard.md`, shared across list-building skills.

## Tool ordering logic

The waterfall runs from included-in-plan to most expensive per hit:

| Order | Tool | Billing | Why this position |
|-|-|-|-|
| 1 | `query_lead_database` | Included in Growth and Scale | Free per lead within the daily allowance; returns titles, seniority and emails together. |
| 2 | `scrape_website_finder` | $0.0499 per contact found | Searches a domain for a title; only billed on hits. |
| 3 | `find_emails` | $0.05 per email found | Turns a known name into an email; validated at lookup. |
| 4 | `validate_emails` | $0.0072 per email | Required before sending anything not validated at lookup. |
| 5 | `find_mobiles` | $0.25 per number found | Highest cost; optional; compliance rules apply. |
| Side path | `scrape_apollo` | $0.0039 per lead, 500 minimum | For large accounts the database missed; slow (hours to days). |

## Sources

- Gartner, The B2B buying journey: https://www.gartner.com/en/sales/insights/b2b-buying-journey
- MEDDICC, Who created MEDDIC: https://meddicc.com/resources/who-created-meddic
- 47 CFR 64.1200 (TCPA rules): https://www.law.cornell.edu/cfr/text/47/64.1200
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
