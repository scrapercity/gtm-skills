# Candidate Outreach Compliance

Rules for contacting sourced candidates and for how they are filtered and ranked. A planning summary of public sources, not legal advice. Employment counsel decides close calls, especially across borders.

## 1. Email to candidates

| Rule | Source | Operating standard |
|-|-|-|
| CAN-SPAM covers messages whose primary purpose is commercial advertisement or promotion | FTC CAN-SPAM guide | A one-to-one job approach may fall outside "commercial", but agencies often mix in their own services. Apply CAN-SPAM mechanics to every candidate email: accurate From and subject, the sender's postal address, a working opt-out honored within 10 business days |
| Talent acquisition teams email candidates under these laws | PeopleScout compliance note | Same mechanics |
| CASL covers commercial electronic messages to recipients in Canada and generally needs consent | CRTC CASL FAQ | Treat Canadian candidate email as subject to CASL until counsel says otherwise. Implied consent from a conspicuously published business address applies only when the message relates to the recipient's business role and the address was not published with a "no unsolicited messages" statement; record where the address was published |
| PECR and GDPR for UK and EU candidates | ICO; GDPR | Named business emails are personal data. Document a legitimate interest assessment; follow Article 14 (section 4) |

Copy rules that keep candidate email on the right side of these rules and of the inbox providers:

1. Say who you are, who you recruit for (or that the client is confidential), and why this person.
2. One clear opt-out line ("Reply 'no thanks' and I won't contact you about roles again").
3. Send from a recruiter's domain that passes SPF, DKIM and DMARC; candidate inboxes are on Google Workspace and Microsoft 365 like any other.
4. Do not email a candidate's work address about leaving their employer with a subject line that would embarrass them if a colleague saw it.

## 2. Calls and texts to candidate mobiles

| Rule | Source | Operating standard |
|-|-|-|
| Autodialed, artificial or prerecorded voice calls to wireless numbers need prior express consent | 47 U.S.C. 227(b) | Recruiters dial by hand |
| AI-generated voices count as artificial voices | FCC declaratory ruling, February 2024 | No AI voice agents calling candidates without consent |
| Texts are treated as calls under these rules | 47 CFR 64.1200 | No platform or bulk texts without consent; a single manual text after a call the candidate agreed to is the outer limit |
| DNC rules center on telephone solicitations (encouraging purchases of goods, services or property) | 47 CFR 64.1200 definitions | A pure job call may fall outside the Registry rules; still keep an internal do-not-contact list and honor every request |
| Calling hours | 47 CFR 64.1200(c)(1) applies to solicitations | Use 8 a.m. to 9 p.m. local as the operating window anyway |
| Revocation by any reasonable means | FCC rules effective April 11, 2025 | "Stop texting me" or "don't call" ends contact on that channel |
| UK live calls | ICO PECR telephone marketing | Recruiting calls are not marketing calls in most cases; if the call also markets the agency's services, TPS and CTPS screening applies |

## 3. Fair filtering and ranking

| Rule | Source | Operating standard |
|-|-|-|
| No job ad or recruiting method that shows a preference or discourages applicants by race, color, religion, sex, national origin, age 40 and up, disability or genetic information | EEOC prohibited practices; Title VII; ADEA | Filters are job-related only: title, level, company, location, company traits |
| Word-of-mouth-only recruiting can be discriminatory when it reproduces a homogeneous workforce | EEOC prohibited practices | Combine target-company searches with market-wide searches; do not source only from the hiring team's former employers |
| Age proxies | ADEA; EEOC example of "recent college graduates" in ads | No graduation-year filters, no "years since degree", no "digital native" language |
| Automated tools that substantially assist hiring decisions in New York City need a bias audit within one year before use and at least 10 days' notice to candidates | NYC Local Law 144, enforced from July 5, 2023 | This skill's rubric is a manual sort reviewed by a recruiter. Automated scoring used to screen NYC candidates needs a Local Law 144 review first |
| Diversity sourcing | EEOC | Widen where you look (more companies, more cities, more title phrasings). Never filter on a protected trait or a proxy for one |

## 4. GDPR Article 14 for candidates in the EU and UK

When personal data is obtained from a source other than the candidate, the controller provides, among other items: its identity and contact details, the purposes and legal basis, the legitimate interests pursued, the categories of data, the source of the data and whether it came from publicly accessible sources, the retention period, and the candidate's rights (access, erasure, objection) and right to complain to a supervisory authority. Timing: within a reasonable period and at the latest within one month, or at the first communication if the data is used to contact the person.

First-email line for EU and UK candidates:

```text
I found your work details through a B2B contact database. I keep them only to discuss this role, delete them after 6 months if we don't speak, and you can ask me to delete them now. Privacy notice: link.
```

Article 14(5)(b) allows an exception where informing each person would require disproportionate effort, but a recruiter who is about to email the candidate cannot rely on it.

## 5. The FCRA line

| Activity | Status |
|-|-|
| Finding work emails and mobiles to contact candidates | Sourcing; outside the FCRA when not used to evaluate eligibility |
| Ranking by title, level, company and location for a recruiter's call list | Sourcing |
| Searching People Finder, Property Lookup or Criminal Records about a candidate | Background screening; FCRA employment purpose. Not in this skill |
| A background check before an offer | Use a consumer reporting agency, with the candidate's written authorization and the FCRA disclosure and adverse action steps |

The FTC treated Spokeo as a consumer reporting agency in 2012 because it marketed people profiles to HR and recruiting for screening ($800,000 civil penalty). The lesson for recruiters: the use decides. Keep sourcing data out of the evaluation file.

## 6. Agency-specific obligations

| Topic | Rule |
|-|-|
| Non-solicitation clauses with clients | Exclude current clients' domains from every search unless the contract allows it |
| Confidential searches | Do not name the client in the first message if the client asked for confidentiality |
| Candidate ownership disputes | Record `pulled_at`, `source` and first-contact date so the agency can show when it sourced the person |
| Retention | Delete long-list data for people never contacted after the search closes; keep opt-outs permanently |

## 7. Compliance table template for the report

| Item | Answer | Law or rule | Action |
|-|-|-|-|
| Email to US candidates | Work emails | CAN-SPAM | Sender identity, postal address, opt-out within 10 business days |
| Calls | Recruiters dial by hand | TCPA, 47 U.S.C. 227(b) | No autodialer, prerecorded or AI voice |
| Texts | None without consent | TCPA, 47 CFR 64.1200 | Manual follow-up text only after a call the candidate agreed to |
| Filters and ranking | Title, level, company, location | EEOC guidance; ADEA | No age or other protected-trait proxies |
| Automated screening | Manual rubric | NYC Local Law 144 | No automated scoring for NYC roles without an audit |
| Background data | Not collected | FCRA | No People Finder or Criminal Records on candidates |

## Sources

- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- PeopleScout, Compliance corner: CAN-SPAM, CASL and more: https://www.peoplescout.com/insights/compliance-corner-can-spam-casl/
- CRTC, CASL frequently asked questions: https://crtc.gc.ca/eng/com500/faq500.htm
- ICO, Telephone marketing under PECR: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/telephone-marketing/
- GDPR Article 14: https://gdpr-info.eu/art-14-gdpr/
- 47 U.S.C. 227: https://www.law.cornell.edu/uscode/text/47/227
- 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FCC AI voice ruling (summary): https://cooley.com/news/insight/2024/2024-02-15-fcc-ai-generated-robocalls-illegal-under-the-tcpa
- FCC revocation rules (summary): https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/fcc-sets-effective-date-for-tcpa-reasonable-consent-revocation-rules
- EEOC, Prohibited employment policies and practices: https://www.eeoc.gov/prohibited-employment-policiespractices
- NYC Local Law 144 final rules (summary): https://perkinscoie.com/en/news-insights/nyc-adopts-final-rules-for-law-governing-automated-employment-decision-tools.html
- FTC Spokeo settlement (summary): https://www.hunton.com/privacy-and-cybersecurity-law-blog/ftc-fines-data-broker-800000-alleged-fcra-violations
- FTC, Background checks: what employers need to know: https://www.ftc.gov/business-guidance/resources/background-checks-what-employers-need-know
