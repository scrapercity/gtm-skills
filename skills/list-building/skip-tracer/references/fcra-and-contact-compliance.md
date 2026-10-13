# FCRA Boundary and Contact Compliance

The rules that decide whether a skip trace may run and how its results may be used. A planning summary of public sources, not legal advice. The user's counsel decides close calls.

## 1. Purpose gate

| Purpose | Allowed with this skill? | Why |
|-|-|-|
| Find a property owner to make a purchase or listing offer | Yes | Prospecting |
| Reconnect with a past customer of the user's own business | Yes | Contact data for an existing relationship |
| Locate a debtor's current address or phone (collector or creditor) | Yes, under Regulation F location rules | Location, not eligibility |
| Find heirs or the personal representative of an estate for a property purchase | Yes | Prospecting; contact the representative named in probate |
| Serve legal process, locate a witness | Yes, by or for the law firm | Location |
| Decide whether to rent to an applicant | No | FCRA: tenant screening needs a consumer report from a CRA |
| Decide whether to hire, promote or retain someone | No | FCRA employment purpose |
| Decide whether to lend, extend credit, or set terms | No | FCRA credit purpose |
| Decide insurance eligibility or price | No | FCRA insurance purpose |
| Find a person who cut off contact with the user personally | No | No business purpose; safety risk |
| Resell the results as "background checks" | No | That is the business model the FTC treated as a CRA in Spokeo and Instant Checkmate |

Write the purpose in one sentence in the report. If the purpose changes later (a landlord who prospected owners now wants to screen a tenant), the data does not follow it.

## 2. Why the FCRA line sits where it does

- A consumer report is information from a consumer reporting agency bearing on a person's creditworthiness, character, general reputation, personal characteristics or mode of living, used or expected to be used for eligibility for credit, insurance, employment or other purposes the statute lists.
- Users of consumer reports need a permissible purpose, must certify it, and must send adverse action notices when a report contributes to a denial.
- The FTC treated people-search sites as consumer reporting agencies when they marketed reports for screening (Spokeo, 2012) or supplied them to users without a permissible purpose (Instant Checkmate and TruthFinder, 2023).
- `references/scrapercity-platform.md` records that ScraperCity's public-records results are treated in this repo as prospecting and research data only, never as the basis for an employment, tenant, credit or insurance decision.

Operating rules:

1. The report's first section names the purpose and states the results are not used for tenant, employment, credit or insurance decisions.
2. Results are not stored in a screening system, an applicant file or an HR record.
3. The word "background check" never appears in the deliverable.

## 3. Calls and texts to homeowners and consumers

| Rule | Source | Operating standard |
|-|-|-|
| Autodialed, artificial or prerecorded voice calls to wireless numbers need consent | 47 U.S.C. 227(b) | Manual live calls only unless written consent is on file |
| AI-generated voices count as artificial | FCC declaratory ruling, February 2024 | No AI voice agents on skip-traced numbers without consent |
| Texts are treated as calls for these rules | 47 CFR 64.1200 | No texts without consent |
| No solicitation before 8 a.m. or after 9 p.m. local | 47 CFR 64.1200(c)(1) | Dialer windows by the owner's time zone |
| National DNC Registry | FTC TSR; 47 CFR 64.1200(c)(2) | Scrub within 31 days of calling; remove Registry numbers |
| Established business relationship | FTC TSR | A skip-traced owner has none; the exemption does not apply |
| Internal do-not-call list | 47 CFR 64.1200(d) | Add requests the same day; the ceiling is 10 business days; keep 5 years |
| Revocation by any reasonable means | FCC rules effective April 11, 2025 | Treat "stop calling" in any form as final |
| Damages | 47 U.S.C. 227(b)(3), (c)(5) | $500 per violation under (b)(3); actual loss or up to $500 under (c)(5), whichever is greater; up to triple if willful |
| State mini-TCPA laws | For example Florida's Telephone Solicitation Act | Check the owner's state before any automated contact |

## 4. Debt collectors and creditors: Regulation F location communications

When a collector contacts anyone other than the consumer to find the consumer (12 CFR 1006.10):

| Must | Must not |
|-|-|
| Give the individual's name and say they are confirming or correcting location information | Say the consumer owes a debt |
| Name the employer only if asked | Use postcards |
| Contact each third party once, unless asked to call back or the earlier answer was wrong or incomplete | Put debt language or symbols on envelopes |
| Stop third-party contacts once they know the consumer has an attorney for the debt (and can find the attorney), unless the attorney does not respond | |

Location script for collectors:

```text
"Hi, this is Jordan Lee. I'm trying to confirm contact information for Maria Ortiz. Is this a good number to reach her?"
(If asked who you work for, name the employer. Say nothing about a debt.)
```

## 5. Pre-foreclosure and distressed owners

- Regulation O (12 CFR 1015): offers to stop a foreclosure, modify a loan or negotiate with the lender for the owner are mortgage assistance relief services. No advance fees; required disclosures. A purchase offer is outside it; a "we can save your home" pitch is inside it.
- State wholesaling statutes (for example Ohio SB 155, effective March 2, 2026, requiring a wholesaler disclosure form) and equity-purchase statutes (California Civil Code 1695) change the contract and the script. See the `scrapercity-real-estate-data` skill's `references/compliance-guide.md`.
- Script rule: lead with who you are and that you buy houses; no implication of a government or lender affiliation.

## 6. Email to individuals

Commercial email to a homeowner's personal address still follows CAN-SPAM: accurate headers, honest subject, a postal address, a working opt-out honored within 10 business days. Validate before sending (`validate_emails`, $0.0072 each). In Canada (CASL) and the EU and UK (GDPR, PECR), emailing an individual for marketing generally needs consent; skip-traced emails for those countries go to mail instead.

## 7. Data handling

| Practice | Rule |
|-|-|
| Retention | Keep results only as long as the campaign needs them; delete no-match and weak rows after the mail drop |
| Access | Limit the file to the people working the campaign |
| Sharing | Do not resell or share results with third parties |
| Opt-outs | A person who asks not to be contacted goes on the internal do-not-call and do-not-mail list across every future skip trace |
| Accuracy | Record `match_score` and `matched_by` so a wrong-person complaint can be traced and suppressed |

## 8. Compliance table for the report

One row per channel or decision, each naming its law:

| Item | Answer | Law | Action |
|-|-|-|-|
| Purpose | Purchase offers to owners in pre-foreclosure | FCRA, 15 U.S.C. 1681b | Not used for tenant, employment, credit or insurance decisions |
| Calls | Manual live calls | TCPA, 47 U.S.C. 227(b) | No autodialer, prerecorded or AI voice, no texts |
| DNC | Registry and internal list | FTC TSR; 47 CFR 64.1200(c), (d) | Scrub within 31 days; remove matches |
| Calling hours | Owner local time | 47 CFR 64.1200(c)(1) | 8 a.m. to 9 p.m. |
| Offer content | Purchase only | Regulation O, 12 CFR 1015 | No foreclosure rescue claims |
| State | Ohio | Ohio SB 155 | Wholesaler disclosure form before any contract |

## Sources

- FTC, Fair Credit Reporting Act: https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act
- 15 U.S.C. 1681a and 1681b: https://www.law.cornell.edu/uscode/text/15/1681b
- FTC, Using consumer reports: what landlords need to know: https://www.ftc.gov/business-guidance/resources/using-consumer-reports-what-landlords-need-know
- FTC Spokeo settlement (summary): https://www.hunton.com/privacy-and-cybersecurity-law-blog/ftc-fines-data-broker-800000-alleged-fcra-violations
- FTC Instant Checkmate and TruthFinder settlement (summary): https://www.consumerfinancemonitor.com/2023/09/15/ftc-settles-with-background-report-companies-for-fcra-violations-and-deceptive-acts/
- CFPB Regulation F, 1006.10: https://www.consumerfinance.gov/rules-policy/regulations/1006/10/
- 47 U.S.C. 227: https://www.law.cornell.edu/uscode/text/47/227
- 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FCC AI voice ruling (summary): https://cooley.com/news/insight/2024/2024-02-15-fcc-ai-generated-robocalls-illegal-under-the-tcpa
- FCC revocation rules (summary): https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/fcc-sets-effective-date-for-tcpa-reasonable-consent-revocation-rules
- FTC, Q&A about DNC provisions of the TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- CFPB Regulation O: https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- Ohio REALTORS on wholesaling legislation: https://www.ohiorealtors.org/blog/2306/real-estate-wholesaling-legislation-takes-effect/
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
