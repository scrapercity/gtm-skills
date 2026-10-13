# Outbound Compliance Primer

The law-by-channel reference for every outbound skill in this repo: cold email, cold calls, texts, voicemail, direct mail, and the people-search and public-records data that feed them. It covers CAN-SPAM, the TCPA and Do Not Call rules, state telemarketing laws, CASL and the Canadian telemarketing rules, PECR and UK GDPR, the EU GDPR and ePrivacy Directive, the FCRA's limits on people-search and criminal-records data, and state privacy laws at a high level.

**This is not legal advice.** It is an operating summary of primary sources, checked on 2026-10-13. Laws, regulator guidance and court rulings change. A program that calls consumers, texts anyone, sends into the EU, or uses public-records data for anything beyond prospecting needs review by a lawyer licensed where you and your recipients are.

Skills that load this file: `cold-calling`, `signal-triggered-outbound`, `multi-channel-outreach`, `reply-handling`, `cold-email-strategy`, `mobile-appender`, `skip-tracer`, `scrapercity-real-estate-data`, `scrapercity-local-business-database`, and the list-building skills.

## 1. Decision table by channel and country

Read the row for the channel, then the column for where the recipient is. "Allowed" means allowed when every condition in the cell holds. When a cell says counsel, do not launch until a lawyer has signed off.

| Channel | United States | Canada | United Kingdom | European Union |
|-|-|-|-|-|
| Cold email to a business address | Allowed under CAN-SPAM: true headers and subject, ad identification, postal address, working opt-out honored within 10 business days. No B2B exemption. | Needs consent. Implied consent can come from a conspicuously published address with no "no unsolicited messages" statement, when the message fits the person's role. Identify sender, unsubscribe within 10 business days. | Corporate subscribers (companies, LLPs, government bodies): allowed without prior consent under PECR; identify yourself and give an opt-out. Sole traders and some partnerships: consent or soft opt-in only. UK GDPR applies to named work addresses: document legitimate interests. | GDPR applies to named work addresses: legitimate interests assessment, Article 14 notice, absolute right to object. Whether B2B email needs prior consent depends on each member state's ePrivacy law. Counsel per country. |
| Live, hand-dialed call to a business line | Generally allowed. The FTC's Telemarketing Sales Rule exempts most B2B calls (not retail sales of nondurable office or cleaning supplies). Keep a company Do Not Call list and identify yourself. | Calls to business numbers are exempt from the National DNCL rules; the Telemarketing Rules still apply (hours, identification, internal list honored within 14 days). | Allowed unless the number is on TPS or CTPS or the business objected. Screen both registers and your own list. | Varies by country. Treat as counsel-only. |
| Live, hand-dialed call to a mobile or residential number | Scrub the National DNC Registry (copy no older than 31 days) and your internal list; 8am to 9pm federal window, tighter in several states; identify caller and company. Treat sole-proprietor mobiles as consumer numbers. | National DNCL applies to residential and mobile numbers; Telemarketing Rules hours (weekdays 9am to 9:30pm, weekends 10am to 6pm). | TPS screening required; sole traders register on TPS. | Counsel per country. |
| Autodialed, prerecorded, ringless voicemail or AI-voice call | Prior express consent for wireless numbers; prior express written consent when the call is telemarketing. The FCC ruled in February 2024 that AI-generated voices are "artificial" voices under the TCPA. Do not use for cold outreach. | Automatic dialing-announcing devices need express consent for sales calls. Do not use cold. | Automated marketing calls need consent that specifically covers automated calls. Do not use cold. | Do not use cold. |
| Text message (SMS, MMS) | Treated as a call under the TCPA and under Florida, Oklahoma, Maryland and Texas law. Do not send cold texts. | CASL treats a text as a commercial electronic message: consent required. | PECR: texts to individuals need consent or soft opt-in. | Consent in practice. |
| Direct mail to a business address | No federal consent rule. Truthful claims, honor removal requests. | Allowed; PIPEDA governs personal information use. | Allowed; UK GDPR legitimate interests and an objection route. | Allowed with GDPR basis and notice. |
| Direct mail to a residence (property owners, skip-traced addresses) | Allowed with care: no deceptive official-looking pieces; mortgage assistance offers fall under Regulation O. | Allowed; PIPEDA. | UK GDPR legitimate interests; honor objections. | GDPR basis and notice. |

House defaults that sit on top of the law: suppress every opt-out from every channel within 1 business day; no cold texts anywhere; no automated or AI voice on cold calls anywhere; EU sends only after counsel approves the country list.

## 2. United States: commercial email (CAN-SPAM)

Source: FTC, CAN-SPAM Act: A Compliance Guide for Business.

| Requirement | What it means in a cold email program |
|-|-|
| No false or misleading header information | From name, From address, Reply-To and routing identify the real sender. No spoofed domains. |
| No deceptive subject lines | No "Re:" or "Fwd:" on a first touch. Subject reflects the content. |
| Identify the message as an ad | Clear and conspicuous; the FTC allows flexibility in how. |
| Tell recipients where you are | A valid physical postal address: street address, a registered USPS box, or a private mailbox registered under USPS rules. |
| Tell recipients how to opt out | A clear way to opt out of future email. Must work for at least 30 days after the send. |
| Honor opt-outs promptly | Within 10 business days. No fee, no login, nothing beyond a reply or one page visit. Never sell or transfer the address. |
| Monitor what others do for you | The company whose product is promoted and the company that sends are both liable. |

The FTC guide says the law makes no exception for business-to-business email. Each separate email in violation can cost up to $53,088 (16 CFR 1.98, amount in force since January 2025).

Mailbox provider rules (Google, Yahoo, Microsoft) sit on top of the law and are covered in `references/deliverability-primer.md`.

## 3. United States: calls and texts (TCPA, FCC rules, Do Not Call, TSR)

### 3a. The rules that apply to a cold calling program

| Rule | Source | Requirement |
|-|-|-|
| Autodialer and artificial or prerecorded voice to wireless numbers | 47 U.S.C. 227(b); 47 CFR 64.1200(a)(1)(iii) | Prior express consent, except emergencies. For telemarketing, prior express written consent (64.1200(a)(2)). |
| AI-generated voices | FCC Declaratory Ruling FCC 24-17, CG Docket 23-362, adopted 2 Feb 2024, released 8 Feb 2024 | AI technologies that generate human voices, including voice cloning, are "artificial" voices under the TCPA. Consent rules above apply. Artificial voice messages must identify the caller at the start; telemarketing ones must offer an opt-out. |
| Calling hours | 47 CFR 64.1200(c)(1) | No telephone solicitation to a residential subscriber before 8am or after 9pm, called party's local time. |
| National Do Not Call Registry | 47 CFR 64.1200(c)(2) | No telephone solicitation to a residential number on the registry. Safe harbor needs written procedures, trained staff, an internal list, and a registry copy obtained no more than 31 days before the call. |
| Wireless numbers | 47 CFR 64.1200(e) | The DNC and company-specific list rules in (c) and (d) apply to wireless numbers as the FCC's 2003 order describes. |
| Company-specific Do Not Call list | 47 CFR 64.1200(d) | Written policy available on demand; trained staff; record a do-not-call request and honor it within 10 business days; keep it 5 years; give the caller's name, the company name and a contact number or address. |
| Revocation of consent | 47 CFR 64.1200(a)(10) | Revocation by any reasonable means, honored within 10 business days. |
| Abandoned calls | 47 CFR 64.1200(a)(7) | No more than 3% of live-answered telemarketing calls abandoned per campaign per 30 days; a call is abandoned if no live rep within 2 seconds of the greeting. A reason never to run a predictive dialer on cold lists. |
| B2B exemption (FTC) | Telemarketing Sales Rule, 16 CFR 310.6(b)(7) | Calls between a telemarketer and a business to induce a purchase are exempt from most of the TSR, including its Do Not Call provisions, except retail sales of nondurable office or cleaning supplies. Misrepresentation bans still apply. |
| Statutory damages (private suits) | 47 U.S.C. 227(b)(3), (c)(5) | $500 per violation under (b)(3); actual loss or up to $500 per violation under (c)(5), whichever is greater. Either can be trebled to $1,500 if willful or knowing. Class actions multiply this by every call. |
| FTC civil penalty | 16 CFR 1.98 | Up to $53,088 per violation of the TSR. |
| Registry access fee | FTC, August 2026 release | FY2027 (from 1 October 2026): $85 per area code, $43 for an area code added in the second half of the year, first five area codes free, $23,425 maximum. The FTC resets fees each October. |

### 3b. B2B versus consumer: how this repo decides

The FCC's DNC rule protects residential subscribers, and the FTC's TSR exempts most business calls. The gray zone is a business owner's mobile, which is also a personal phone. House rule:

| Number | Source in ScraperCity | Treat as | Gate |
|-|-|-|-|
| Main business line from a listing | `phone` in Local Business Database, Google Maps or Yelp results | Business | Internal DNC list, calling hours, caller ID |
| Company or direct dial for a named employee | Lead Database phone fields | Business, unless the number is wireless | Same, plus a line type check |
| Mobile for a named person | `find_mobiles` (`mobile_number`), `contact_mobile` in the Local Business Database | Consumer (residential) | National DNC scrub within 31 days, internal list, calling hours, state rules, live hand dial only |
| Residential owner phone | `find_people`, `scrape_property_lookup` with `includeOwnerContact` | Consumer | Same as mobile, plus Regulation O if the offer is mortgage relief |

### 3c. Autodialer definition and court deference

- The Supreme Court held in Facebook v. Duguid (April 2021) that equipment is an autodialer under the TCPA only if it can store or produce numbers using a random or sequential number generator. Several state laws define "automated system" more broadly (section 4).
- In McLaughlin Chiropractic v. McKesson (June 2025), the Court held that district courts in TCPA enforcement suits are not bound by the FCC's interpretations and must apply ordinary statutory interpretation. Expect court-by-court variation; it does not loosen any rule above.
- A click-to-call or one-line power dialer started by a rep is the conservative choice. Parallel and predictive dialers, ringless voicemail drops and AI voice agents stay off cold lists.

## 4. United States: state telemarketing laws (mini-TCPAs)

State laws add hours, call caps and broader autodialer definitions. Many give consumers a private right of action. Check every state on the list before a campaign; the rows below are verified examples and leave other states out.

| State | Law | Hours | Frequency cap | Automated system rule | Private action |
|-|-|-|-|-|-|
| Florida | Fla. Stat. 501.059 (Telephone Solicitation Act) and 501.616 | 8am to 8pm called party's time zone (501.616(6)) | Max 3 commercial solicitation calls per person per 24 hours on the same subject, from any number (501.616(6)) | Prior express written consent for sales calls using an automated system for selecting or dialing numbers or a recorded message (501.059(8)); texts and voicemail transmissions count | $500 or actual damages, up to 3x if willful (501.059(10)) |
| Oklahoma | Telephone Solicitation Act of 2022 (HB 3168), effective 1 Nov 2022 | 8am to 8pm | Max 3 calls per 24 hours on the same subject | Prior express written consent for automated selection or dialing | $500 or actual damages, up to 3x |
| Maryland | Stop the Spam Calls Act (2023 ch. 413), effective 1 Jan 2024 | No calls between 8pm and 8am | Max 3 calls per 24 hours on the same subject | Prior express written consent for automated selection or dialing; no altered voice to disguise the caller | A violation is an unfair, abusive or deceptive trade practice under the Maryland Consumer Protection Act |
| Texas | Bus. & Com. Code 301.051; SB 140 (2025), effective 1 Sep 2025 | 9am to 9pm; Sunday noon to 9pm (Texas State Law Library summary of 301.051) | | SB 140 brings text messages into Chapter 302 "telephone call" coverage | SB 140 makes violations of the Texas no-call chapter enforceable through the DTPA, including private suits |

House rule that satisfies every row: call 9am to 8pm recipient local time, Monday to Friday; at most 2 dials per number per day and never 3 in 24 hours; no automated selection or dialing on mobiles; no texts.

## 5. Canada

| Topic | Rule | Source |
|-|-|-|
| What CASL covers | Any commercial electronic message (email, text, social DM) with a purpose of encouraging commercial activity. Needs consent, sender identification and an unsubscribe mechanism. | CRTC CASL FAQ |
| Implied consent by publication | Recipient conspicuously published the address, did not say they refuse unsolicited messages, and the message relates to their business role or duties. | CRTC CASL FAQ |
| B2B exemption | Only when the two organizations already have a relationship and the message concerns the recipient organization's activities. One person-level contact does not create a relationship. | CRTC CASL FAQ |
| Unsubscribe | Processed without delay, no later than 10 business days. | CRTC CASL FAQ |
| Penalties | Up to $1 million per violation for individuals and $10 million for businesses. | CRTC CASL FAQ |
| Voice calls | CASL does not cover live or automated telemarketing calls; the Unsolicited Telecommunications Rules do. | CRTC CASL FAQ |
| National DNCL | Calls to business numbers are exempt from the DNCL rules but covered by the Telemarketing Rules and ADAD Rules. Exempt callers keep an internal do-not-call list and honor additions within 14 days. Calling hours: weekdays 9am to 9:30pm, weekends 10am to 6pm. | CRTC National DNCL exemptions page |

Keep proof of where each Canadian address was published (URL and date) in the lead record, since implied consent depends on it.

## 6. United Kingdom: PECR and UK GDPR

| Topic | Rule | Source |
|-|-|-|
| Email and text to corporate subscribers | Allowed without prior consent: companies, Scottish partnerships, LLPs, government bodies. Do not conceal identity; give a valid address for opt-outs; keep a do-not-email list and screen new lists against it. | ICO guide to PECR, electronic mail marketing |
| Email and text to individual subscribers | Sole traders and some partnerships count as individuals: specific consent or soft opt-in only. | Same |
| Live calls | Allowed to numbers not on TPS or CTPS and not previously objected; screen both registers plus your own list. Claims management calls have stricter rules. | ICO guide to PECR, telephone marketing |
| Automated calls | Only with consent that covers automated calls specifically. | Same |
| Lawful basis for named contacts | UK GDPR applies to personal data such as jane.smith@company.co.uk. Legitimate interests needs a purpose test, a necessity test and a balancing test. The UK GDPR, as amended by the Data (Use and Access) Act 2025, states that direct marketing may be a legitimate interest; the ICO says this is not automatic. | ICO legitimate interests guidance (updated March 2026) |
| Right to object | Absolute for direct marketing. Stop on objection, tell people about the right, make it free and easy. | Same |
| PECR overrides | Where PECR needs consent, legitimate interests cannot replace it. | Same |
| Data (Use and Access) Act 2025 | The ICO reported on 19 June 2026 that all data protection provisions are in force, and it has published new guidance on direct marketing by electronic mail. Check the ICO page before each new UK program. | ICO DUAA page |

## 7. European Union: GDPR and ePrivacy

| Topic | Rule | Source |
|-|-|-|
| Lawful basis | Article 6(1)(f) legitimate interests; Recital 47 says direct marketing may be regarded as a legitimate interest. Document a legitimate interests assessment per campaign. | GDPR (Regulation 2016/679) |
| Notice when data was not collected from the person | Article 14: tell the person who you are, the purpose, the basis, the source of the data and their rights, at the latest at the first communication or within one month. A short notice and link in the first email is the usual way. | GDPR Article 14 |
| Right to object | Article 21(2) and (3): absolute for direct marketing; stop processing for that purpose. | GDPR Article 21 |
| Electronic marketing consent | ePrivacy Directive Article 13 requires prior consent for email marketing to natural persons and leaves protection of legal persons to member states. National laws differ on B2B email; some require opt-in even for work addresses. | Directive 2002/58/EC |
| Fines | Up to EUR 20 million or 4% of worldwide annual turnover for the highest tier. | GDPR Article 83 |

## 8. FCRA: permissible purpose limits on people-search and criminal-records data

ScraperCity tools that return public-record or people data: People Finder and skip tracing (`find_people`), Property Lookup (`scrape_property_lookup`), Criminal Records (`search_criminal_records`) and Mobile Finder (`find_mobiles`).

| Use | Allowed in this repo | Why |
|-|-|-|
| Finding an owner's contact details to offer a product or service | Yes, as prospecting, subject to TCPA, DNC and state rules | Marketing contact is not an eligibility decision |
| Researching a prospect company or its principals before outreach | Yes | Same |
| Screening a job applicant, tenant, borrower or insurance applicant | No | 15 U.S.C. 1681b lists the permissible purposes for consumer reports (credit, employment, insurance, licensing, legitimate business need tied to a consumer-initiated transaction). Those uses need a consumer reporting agency that follows the FCRA, plus notices, consent and adverse action steps. |
| Deciding whether to sell to or extend terms to a consumer based on a criminal record | No | Same |

The FTC's September 2023 action against TruthFinder and Instant Checkmate ($5.8 million proposed penalty) said people-search sites operated as consumer reporting agencies despite disclaimers, because they marketed background reports for employment and tenant screening. The lesson for a user: the label on the data source does not decide the law; the use does. ScraperCity's terms make the user responsible for a lawful basis (see `references/scrapercity-platform.md`).

## 9. US state privacy laws, high level

| Topic | What to know | Source |
|-|-|-|
| California CCPA as amended by CPRA | Since 1 January 2023 the temporary exemptions for employee and business-to-business personal information have expired, so a California professional's name, work email and phone are personal information. Rights include know, delete, correct and opt out of sale or sharing. Applies to businesses over the statute's thresholds. | Cal. Civ. Code 1798.145; California Privacy Protection Agency |
| California data brokers (Delete Act) | Registered data brokers had to register through DROP in January 2026 and must process DROP deletion requests from 1 August 2026, checking at least every 45 days. A user who resells or brokers lists may be a data broker. | CPPA data broker page |
| Other comprehensive state laws | Several states define "consumer" to exclude people acting in a commercial or employment context. Virginia's law is an example. B2B prospecting data often falls outside those laws; consumer data (homeowners, mobiles used personally) does not. | Va. Code 59.1-575 |
| Practical rule | Keep the source and pull date on every record, honor deletion and opt-out requests across every tool within the law's deadline, and do not resell lists without counsel. | This repo |

## 10. Real estate and distress outreach

Distress List (`scrape_distress_list`) returns pre-foreclosure, foreclosure, auction and bank-owned properties; owners are consumers.

- Phone and text: the consumer rules in sections 3 and 4 apply in full. Scrub DNC, hand dial, no texts.
- Offers to help a homeowner avoid foreclosure or modify a mortgage are mortgage assistance relief services under Regulation O (12 CFR part 1015), which bans advance fees and requires disclosures. Many states add foreclosure consultant or equity purchaser laws. Investor "we buy houses" offers still need truthful, non-threatening copy.
- Never imply you are the lender, a government program or a court.

## 11. Records to keep

| Record | Why | Keep for |
|-|-|-|
| Source and pull date per lead (`source`, `source_detail`, `pulled_at`) | Article 14 notices, CASL implied consent proof, deletion requests | Life of the record |
| DNC registry download date and the scrub result per number | TCPA safe harbor needs a copy no older than 31 days | 5 years (match the company DNC retention rule) |
| Company DNC requests with date received and date honored | 47 CFR 64.1200(d) | 5 years |
| Email opt-outs with date received and date suppressed | CAN-SPAM, CASL, PECR | As long as you send |
| Legitimate interests assessment per UK or EU campaign | UK GDPR, GDPR | Life of the campaign plus your retention policy |
| Dialer settings (manual, one line) | Autodialer defense | Life of the program |

## Sources

- FTC, CAN-SPAM Act: A Compliance Guide for Business: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FTC civil penalty amounts, 16 CFR 1.98: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-A/part-1/subpart-L/section-1.98
- Telemarketing Sales Rule exemptions, 16 CFR 310.6: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.6
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- FTC, 2027 telemarketer fees to access the National Do Not Call Registry (Aug 2026): https://www.ftc.gov/news-events/news/press-releases/2026/08/ftc-announces-2027-telemarketer-fees-access-national-do-not-call-registry
- TCPA, 47 U.S.C. 227: https://www.law.cornell.edu/uscode/text/47/227
- FCC rules, 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FCC Declaratory Ruling FCC 24-17 on AI-generated voices: https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf
- FCC news release on AI-generated voices: https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal
- Facebook, Inc. v. Duguid (2021): https://www.supremecourt.gov/opinions/20pdf/19-511_p86b.pdf
- McLaughlin Chiropractic Associates v. McKesson Corp., docket 23-1226: https://www.supremecourt.gov/docket/docketfiles/html/public/23-1226.html
- Florida Statutes 501.059: http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.059.html
- Florida Statutes 501.616: http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.616.html
- Oklahoma HB 3168 (2022), enrolled: https://oklegislature.gov/cf_pdf/2021-22%20ENR/hB/HB3168%20ENR.PDF
- Maryland 2023 Laws ch. 413 (SB 90): https://mgaleg.maryland.gov/2023RS/chapters_noln/Ch_413_sb0090E.pdf
- Texas SB 140 (2025) bill analysis: https://capitol.texas.gov/tlodocs/89R/analysis/html/SB00140F.htm
- Texas State Law Library, How late can telemarketers call (Bus. & Com. Code 301.051): https://sll.texas.gov/faqs/how-late-can-telemarketers-call
- Texas Business and Commerce Code chapter 301: https://statutes.capitol.texas.gov/SOTWDocs/BC/htm/BC.301.htm
- CRTC, CASL frequently asked questions: https://crtc.gc.ca/eng/com500/faq500.htm
- CRTC, National DNCL exemptions: https://crtc.gc.ca/eng/phone/telemarketing/exempt.htm
- ICO, Guide to PECR, electronic mail marketing: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/
- ICO, Guide to PECR, telephone marketing: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/telephone-marketing/
- ICO, When can we rely on legitimate interests: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/legitimate-interests/when-can-we-rely-on-legitimate-interests/
- ICO, The Data (Use and Access) Act 2025, what it means for organisations: https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-what-does-it-mean-for-organisations/
- GDPR, Regulation (EU) 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- ePrivacy Directive 2002/58/EC: https://eur-lex.europa.eu/eli/dir/2002/58/oj
- FCRA permissible purposes, 15 U.S.C. 1681b: https://www.law.cornell.edu/uscode/text/15/1681b
- FTC, TruthFinder and Instant Checkmate (Sep 2023): https://www.ftc.gov/news-events/news/press-releases/2023/09/ftc-says-truthfinder-instant-checkmate-deceived-users-about-background-report-accuracy-violated-fcra
- California Civil Code 1798.145: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.145
- California Privacy Protection Agency, data brokers and DROP: https://cppa.ca.gov/data_brokers/
- Virginia Code 59.1-575 definitions: https://law.lis.virginia.gov/vacode/title59.1/chapter53/section59.1-575/
- Regulation O, Mortgage Assistance Relief Services, 12 CFR part 1015: https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- ScraperCity terms: https://scrapercity.com/terms
