# Mobile and Contact Compliance

What to check before requesting mobile numbers with `find_mobiles`, and before emailing, calling or texting decision makers in the US, Canada, the UK and the EU. This file is an operating checklist with sources. It is not legal advice; anyone running a calling or texting program at scale should have counsel review it. Full country rules for email sit in `references/outbound-compliance-primer.md`.

## 1. Decision table before any Mobile Finder run

| Question | If yes | If no |
|-|-|-|
| Did the user ask for mobiles? | Continue | Do not run `find_mobiles` |
| Will a person dial each number by hand, one call at a time? | Continue to the next question | Stop: autodialed or prerecorded marketing calls to mobiles need prior express written consent (section 2) |
| Will anyone send marketing texts to these numbers? | Stop unless the user holds prior express written consent for texts; texts count as calls under the TCPA | Continue |
| Are any recipients in Canada, the UK or the EU? | Apply sections 4 to 6 for those rows | Continue |
| Is there an internal do-not-call list? | Scrub against it | Create one before the first call; it is required for exempt callers in Canada and expected everywhere else |
| Will the numbers be scrubbed against the National Do Not Call Registry? | Continue | Scrub first: a mobile may be a personal phone, and the FCC's do-not-call rules apply to wireless numbers |

Record the answers in the report's Mobile Numbers table (`Stated use`, `Compliance check`). The checker fails a report that delivers mobiles without them.

## 2. United States: TCPA

| Rule | What it says | Source |
|-|-|-|
| Autodialer and prerecorded calls to mobiles | Calls using an automatic telephone dialing system or an artificial or prerecorded voice to a wireless number need the called party's prior express consent; for telemarketing, prior express written consent. The rule has no business-to-business exception. | 47 CFR 64.1200(a)(1)(iii) and (a)(2) |
| Texts | The FCC treats text messages as calls for these rules | FCC TCPA orders; 47 CFR 64.1200 |
| One-to-one consent rule | The FCC's December 2023 rule limiting consent to one seller was vacated by the Eleventh Circuit on 24 January 2025 (Insurance Marketing Coalition v. FCC). The 2012 prior express written consent requirement still stands. | Kelley Drye summary of the decision |
| Do Not Call on wireless numbers | The company-specific and national do-not-call rules in 64.1200(c) and (d) apply to telephone solicitations to wireless numbers | 47 CFR 64.1200(e) |
| Calling hours | No telephone solicitation to a residential subscriber before 8 a.m. or after 9 p.m. at the called party's location | 47 CFR 64.1200(c)(1) |
| Internal do-not-call list | Callers keep a list of people who asked not to be called and honor it | 47 CFR 64.1200(d) |
| Reassigned numbers | The FCC Reassigned Numbers Database (reassigned.us, live 1 November 2021) shows whether a number was disconnected after a date. Checking it is the basis of the safe harbor for callers relying on consent. | FCC Reassigned Numbers Database page |

### FTC Telemarketing Sales Rule

The TSR leaves most business-to-business calls outside its scope, with an exception for calls selling nondurable office or cleaning supplies. The TSR exemption does not touch the TCPA's mobile rules above. A mobile number on a B2B list can be the person's personal phone, so treat it as a consumer line for consent and do-not-call purposes.

### State telephone solicitation laws

| State | Rule worth knowing | Source |
|-|-|-|
| Florida (FTSA, Fla. Stat. 501.059) | Automated sales calls or texts need prior express written consent. Calls or texts to a Florida area code are presumed to reach a Florida resident. The 2023 amendment narrowed the autodialer definition to selection and dialing, and added a 15-day notice-and-cure for texts. | Goodwin summary of HB 761 (June 2023) |
| Oklahoma (OTSA, effective 1 November 2022) | Automated sales calls need prior express written consent; no sales calls between 8 p.m. and 8 a.m.; at most three calls in 24 hours on the same subject | Manatt summary |

Other states have their own statutes. When a calling program targets a state with one, check it before the first dial.

### Working rules for this skill

1. Mobile Finder output is for manual, one-to-one dialing by a rep.
2. No autodialer, predictive dialer, prerecorded voicemail drop or marketing text to these numbers without documented prior express written consent.
3. Scrub against the National Do Not Call Registry and the internal list before each call block, and record the scrub date on each row.
4. Call between 8 a.m. and 8 p.m. recipient local time. That satisfies the federal 8 to 9 window and Oklahoma's 8 p.m. cutoff.
5. Honor a stop request on the call: add the number to the internal list the same day.

## 3. United States: email

CAN-SPAM covers B2B commercial email with no exemption. Every message identifies the sender, uses honest headers and subject lines, includes a valid physical postal address, and offers a working opt-out honored within 10 business days (FTC compliance guide). Suppress every opt-out across all campaigns, not only the one it came from.

## 4. Canada

| Channel | Rule | Source |
|-|-|-|
| Email and texts | CASL treats both as commercial electronic messages. They need consent. Implied consent can come from a conspicuously published business address when the message relates to the person's role and the publication does not refuse unsolicited messages. Unsubscribe requests are processed within 10 business days. | CRTC CASL FAQ |
| Telemarketing calls to businesses | The National Do Not Call List Rules do not apply to calls to businesses | National DNCL exemptions page |
| Internal list | Exempt callers still keep an internal do-not-call list, add a request within 14 days, keep it for three years, and identify themselves at the start of the call | Same |

For Canadian rows, record where the address or number was published (`source_detail`) so implied consent can be shown.

## 5. United Kingdom

| Channel | Rule | Source |
|-|-|-|
| Email and texts to corporate subscribers (companies, LLPs, Scottish partnerships, some government bodies) | PECR's consent rule does not apply. Identify yourself and give a valid opt-out address. | ICO business-to-business marketing guidance |
| Email and texts to sole traders and some partnerships | Treated as individual subscribers: specific consent or the soft opt-in is required. When unsure, the ICO says to treat the recipient as an individual. | Same |
| Live calls to businesses | Screen against both the TPS and the CTPS plus your own do-not-call list; calling a registered number needs that business's consent. Display your number and identify yourself. | Same |
| UK GDPR | Named business contacts are personal data. Choose a lawful basis (usually legitimate interests with the three-part test), give privacy information within one month when the data came from another source, and honor objections to direct marketing. | Same |

A mobile number tied to a named UK person is personal data even when found from a work email. Mobile Finder results for UK rows should be used for live calls only after TPS and CTPS screening.

## 6. European Union

GDPR applies to named business contacts. Document a legitimate interest assessment, give the Article 14 notice (information to the person within one month when the data was not obtained from them), and record the source. National e-privacy laws set the rules for B2B email and calls and differ by member state; check the target country before contacting anyone there. When the rules are unclear, email only and skip mobiles for EU rows.

## 7. Storage and handling

| Rule | Why |
|-|-|
| `mobile` and `phone` stay in separate columns | A business main line carries different rules from a personal mobile |
| Record `mobile_found_at`, `dnc_scrubbed_at` and `mobile_use` per row | Shows when and why the number was obtained and checked |
| Never upload mobiles to a dialer or SMS tool without a consent field | Prevents an autodialer campaign from picking them up |
| Delete or stop using a number when a person objects | Required by the internal-list rules above and by UK and EU objection rights |
| Re-scrub before each new call block | Registrations and reassignments change |

## 8. Questions to ask the user before a mobile run

1. Who will call, and with what tool? (A dialer with autodial features changes the answer.)
2. Will anyone text these numbers? With what consent?
3. Which countries are the recipients in?
4. Do you have an internal do-not-call list, and where does it live?
5. Who scrubs against the National Do Not Call Registry, and how often?

If the answers do not support manual one-to-one calls, skip `find_mobiles` and save the $0.25 per number.

## Sources

- 47 CFR 64.1200, Delivery restrictions (TCPA rules): https://www.law.cornell.edu/cfr/text/47/64.1200
- eCFR, 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- Kelley Drye, Eleventh Circuit vacates TCPA 1:1 consent rule (January 2025): https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/eleventh-circuit-vacates-tcpa-11-consent-rule
- FCC, Reassigned Numbers Database: https://www.fcc.gov/reassigned-numbers-database
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- Goodwin, Florida amends mini-TCPA (June 2023): https://www.goodwinlaw.com/en/insights/publications/2023/06/alerts-otherindustries-dpc-florida-amends-mini-tcpa
- Manatt, Oklahoma's mini-TCPA takes effect: https://www.manatt.com/insights/newsletters/tcpa-connect/oklahomas-mini-tcpa-takes-effect
- CRTC, CASL frequently asked questions: https://crtc.gc.ca/eng/com500/faq500.htm
- National Do Not Call List, Exemptions: https://lnnte-dncl.gc.ca/en/Organization/Exemptions
- ICO, Business-to-business marketing: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/
- GDPR Article 14: https://gdpr-info.eu/art-14-gdpr/
