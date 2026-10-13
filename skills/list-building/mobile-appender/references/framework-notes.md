# Framework Notes: Mobile Appender

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Decide whether the list may be autodialed, texted, or only hand-dialed | `tcpa-dnc-gate.md` sections 1 and 2 |
| Scrub against internal, national and state lists | `tcpa-dnc-gate.md` section 3 |
| Handle Canadian or UK numbers | `tcpa-dnc-gate.md` section 5 |
| Normalize LinkedIn URLs and emails before the append | `phone-normalization-and-line-type.md` section 1 |
| Convert found numbers to E.164 and check line type | `phone-normalization-and-line-type.md` sections 2 to 4 |
| Run the pilot and build the cost scenarios | `cost-and-hit-rate-model.md` |
| Check shared calling and email rules | `references/outbound-compliance-primer.md` (shared) |
| Quote a price | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### Telephone Consumer Protection Act, 47 U.S.C. 227

The statute bars calls to wireless numbers using an automatic telephone dialing system or an artificial or prerecorded voice without the called party's prior express consent, with exceptions for emergencies. It gives a private right of action for $500 per violation or actual loss, and courts may triple damages for willful or knowing violations. Applied rule: no appended mobile goes into an automated or prerecorded campaign without a consent record.

### FCC rules, 47 CFR 64.1200

The rules add the detail used in the gate:

- Prior express written consent is a signed written agreement that names the number and discloses that signing is not a condition of purchase. Required for telemarketing robocalls to wireless numbers.
- Telephone solicitations to residential subscribers are barred before 8 a.m. and after 9 p.m. at the called party's location.
- Telemarketers keep an internal do-not-call list, honor requests within a reasonable time not over 10 business days, and keep requests for 5 years.
- The DNC rules cover wireless numbers.
- A caller is not liable for an automated voice call to a number ported from wireline to wireless within the previous 15 days, if the number is not already on the national or company list.
- Paragraph (m) gives a safe harbor for calls to reassigned numbers when the caller checked the Reassigned Numbers Database and got a wrong "no" answer.

### FTC Telemarketing Sales Rule

The FTC's DNC Q&A says most calls to a business intended to sell to that business are exempt, that sellers must sync with the Registry at least every 31 days, and that data for up to five area codes is free. Penalties are adjusted for inflation; the 2025 figure of $53,088 per violation stayed in place for 2026 per the FTC's September 2026 notice. Applied rule: scrub every 31 days even for B2B lists, because the FCC rule and state law are separate from the TSR exemption.

### Court decisions

- Facebook v. Duguid (US Supreme Court, April 1, 2021): an autodialer must have the capacity to store or produce numbers using a random or sequential number generator. Many dialers fall outside that definition, but the prerecorded and artificial voice prohibitions do not depend on equipment.
- Chennette v. Porch.com (9th Cir., October 12, 2022): registered cell phones used for both personal and business purposes are presumptively residential; the caller bears the burden to show primarily business use.
- Insurance Marketing Coalition v. FCC (11th Cir., January 24, 2025): vacated the FCC's one-to-one consent requirement and the "logically and topically associated" requirement.
- McLaughlin Chiropractic v. McKesson (US Supreme Court, June 20, 2025): district courts are not bound by the FCC's interpretation of the TCPA in enforcement suits and must interpret the statute themselves. Applied rule: FCC guidance is a floor, not a shield; keep the conservative defaults.

### FCC actions on consent and AI voice

- February 2024 declaratory ruling: AI-generated voices are "artificial" voices under the TCPA.
- Revocation of consent rules effective April 11, 2025: consumers may revoke consent by any reasonable means; callers honor revocations within 10 business days; replying STOP to a text is a per se reasonable method.

### FCC Reassigned Numbers Database

Live since November 2021. A caller submits a number and a date it last knew the number belonged to the intended person; the database answers whether the number was disconnected (and so possibly reassigned) since then. Used here only for numbers with consent on file.

### ITU-T E.164 and number portability

E.164 numbers are at most 15 digits after the plus sign. Because numbers can be ported between carriers and between wireline and wireless service, the prefix of a US or Canadian number cannot prove the line is a mobile. Applied rule: line type comes from a carrier lookup, not from the area code or exchange.

### CRTC and ICO

- Canada: the National DNCL Rules do not apply to telemarketing calls to businesses, but telemarketers must still keep an internal do-not-call list, add a person within 14 days of a request and keep them on it for 3 years.
- UK: live marketing calls are screened against the TPS (individuals, sole traders, some partnerships) and the CTPS (companies, LLPs, government bodies); automated recorded calls need specific consent.

## What this skill does not do

- Decide whether a specific dialer is an autodialer. That is a legal question for the user's counsel.
- Buy Registry access or carrier lookups. The user holds those accounts.
- Append phones for consumers. That runs through `skip-tracer`.

## Sources

- 47 U.S.C. 227: https://www.law.cornell.edu/uscode/text/47/227
- 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FTC, Q&A for telemarketers and sellers about DNC provisions in the TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- FTC, 2026 civil penalty notice: https://public-inspection.federalregister.gov/2026-18853.pdf
- Facebook, Inc. v. Duguid: https://www.law.cornell.edu/supremecourt/text/19-511
- Chennette v. Porch.com (summary): https://olshanlaw.com/Advertising-Law-Blog/ninth-circuit-issues-pro-plaintiff-ruling-in-do-not
- Insurance Marketing Coalition v. FCC (summary): https://www.reedsmith.com/our-insights/blogs/technology-law-dispatch/102k2uj/eleventh-circuit-vacates-fcc-one-to-one-consent-rule/
- McLaughlin Chiropractic v. McKesson (summary): https://www.faegredrinker.com/en/insights/publications/2025/6/supreme-court-decides-mclaughlin-chiropractic-associates-v-mckesson-corp
- FCC AI voice ruling (summary): https://cooley.com/news/insight/2024/2024-02-15-fcc-ai-generated-robocalls-illegal-under-the-tcpa
- FCC revocation rules effective date (summary): https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/fcc-sets-effective-date-for-tcpa-reasonable-consent-revocation-rules
- Reassigned Numbers Database: https://www.reassigned.us/
- CRTC National DNCL exemptions: https://lnnte-dncl.gc.ca/en/Organization/Exemptions
- ICO, Telephone marketing under PECR: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/telephone-marketing/
- ITU-T E.164 (Twilio glossary summary): https://www.twilio.com/docs/glossary/what-e164
