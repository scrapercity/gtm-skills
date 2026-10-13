# Real Estate Outreach Compliance Guide

High-level rules for using ScraperCity real estate and owner data in outreach. This is a summary of public sources to help plan a compliant workflow. It is not legal advice. Laws change; confirm with a local attorney before launching, especially for wholesaling and foreclosure outreach.

## 1. The four-question gate

Answer these in every plan, before any owner data is pulled:

| Question | If the answer is... | Then |
|---|---|---|
| What channel? | Mail | No federal DNC rule. Accurate, non-deceptive content |
| | Email | CAN-SPAM: accurate headers, honest subject, postal address, opt-out honored within 10 business days |
| | Live manual call | TSR and FCC rules: DNC scrub every 31 days, 8 a.m. to 9 p.m. local time, internal do-not-call list, caller ID |
| | Autodialed, prerecorded or AI-voice call, or text | TCPA: prior express consent for wireless numbers (written consent for telemarketing). No consent, no send |
| Who is the recipient? | A homeowner or individual | Consumer rules above apply in full |
| | An agent, broker or business at its business line | Most B2B calls are exempt from the TSR's DNC provisions; CAN-SPAM still applies to email. Personal mobiles used for business are still wireless numbers under the TCPA |
| What state? | IL, OK, PA, OH, SC (see section 4) or CA for owners in foreclosure | Apply the state rule |
| What is the data used for? | Prospecting, marketing, research | Allowed under the user's own lawful basis |
| | Tenant screening, lending decisions, hiring, insurance | Stop. FCRA. Use a consumer reporting agency |

## 2. Federal rules for calls and texts

| Rule | Source | What it requires |
|---|---|---|
| Consent for automated calls to wireless numbers | 47 U.S.C. 227(b)(1)(A)(iii) | Prior express consent for autodialed or artificial or prerecorded voice calls to cell numbers |
| Prior express written consent for telemarketing robocalls | FCC rules, 47 CFR 64.1200 | A signed written agreement with a clear disclosure that the person authorizes automated or prerecorded telemarketing and that signing is not a condition of purchase |
| Calling hours | 47 CFR 64.1200(c)(1) | No telephone solicitation before 8 a.m. or after 9 p.m. at the called party's location |
| National Do Not Call Registry | 47 CFR 64.1200(c)(2); FTC TSR | Do not solicit registered residential numbers; scrub at least every 31 days |
| Established business relationship | FTC TSR | 18 months after the last purchase or transaction, 3 months after an inquiry. A skip-traced owner has no relationship with you |
| Texts | 47 CFR 64.1200 | Several provisions define a call or solicitation to include a text message; plan texts under the same consent rules |
| Private damages | 47 U.S.C. 227(b)(3), (c)(5) | $500 per violation under (b)(3); actual loss or up to $500 per violation under (c)(5), whichever is greater; up to triple if willful or knowing; DNC suits after more than one violating call in 12 months |
| FTC civil penalties | FTC TSR | Up to $53,088 per violation |

Operating rules for owner lists built with `find_people` or `scrape_property_lookup`:

1. Flag every number as wireless or landline before calling.
2. Scrub against the National DNC Registry and any state DNC list; keep the scrub date.
3. Manual dial only, live voice only, unless prior express written consent is on file.
4. No texts without consent.
5. Keep an internal do-not-call list and honor every request immediately.
6. Call inside 8 a.m. to 9 p.m. in the owner's time zone; state rules can be tighter.

## 3. State call and text rules (examples)

| State | Rule | Effect |
|---|---|---|
| Florida | Florida Telephone Solicitation Act, Fla. Stat. 501.059, amended 2023 | Consent rules for automated calls and texts; after a recipient replies STOP to texts, the sender has 15 days before a suit is allowed |
| Other states | Many states keep their own DNC lists and calling-hour rules | Check the state attorney general's telemarketing page before calling |

## 4. State wholesaling and equity purchase rules

| State | Law | Summary | Plan action |
|---|---|---|---|
| Illinois | Real Estate License Act of 2000, as amended | Buying, selling or offering real estate contracts on two or more occasions in any 12-month period is a pattern of business that needs a broker license | One unlicensed wholesale deal a year at most; otherwise work through a licensed broker |
| Oklahoma | Predatory Real Estate Wholesaler Prohibition Act, effective November 1, 2021 | Wholesalers need a real estate license and follow the license code | License required before marketing contracts |
| Pennsylvania | Act 52 of 2024 | Wholesalers treated as brokers or salespersons; contracts must state it is a wholesale transaction, that the seller may consult an attorney or appraiser, and that the seller may cancel until midnight of the 30th day after signing or conveyance; refunds within 10 business days | License, disclosure language, cancellation window in the contract |
| Ohio | Senate Bill 155, effective March 2, 2026 | Wholesaler disclosure form before contract: identifies the wholesaler, says it does not represent the owner, explains assignment for profit and possible below-market price; without it, the owner can cancel before closing | Use the disclosure form; enforcement under the Consumer Sales Practices Act |
| South Carolina | Real Estate Commission guidance on S.C. Code 40-57 | Marketing the underlying property (photos, address, descriptions) for compensation is brokerage and needs a license; disclaimers do not cure it | Market the contract position only within the narrow statutory exception, or get licensed |
| California | Civil Code 1695 (Home Equity Sales Contracts) | Buying a residence in foreclosure from the owner: written contract rules and a right to cancel until midnight of the fifth business day after signing, or 8 a.m. on the sale date if earlier | Build the cancellation window into the timeline and contract |

States change these rules often. For any state missing from this table, check the state real estate commission and attorney general before marketing contracts.

## 5. Foreclosure-rescue offers: Regulation O

CFPB Regulation O (12 CFR 1015) covers anyone offering to arrange mortgage assistance relief, such as stopping a foreclosure, modifying a loan or negotiating a short sale on the owner's behalf.

| Requirement | Summary |
|---|---|
| Advance fees | Banned. A fee is allowed only after the owner signs the lender's written agreement with the relief |
| Disclosures | Communications must state that the company has no government affiliation and that neither the government nor the lender approved its service |
| Stop-paying warning | Any message suggesting the owner stop paying must include the Regulation O warning about losing the home and credit damage |

Plan rule: scripts to pre-foreclosure owners make a purchase offer or a listing offer. They do not promise to stop the foreclosure or fix the loan unless the user operates as a compliant relief provider.

## 6. FCRA boundary

| Use | Allowed with these tools? |
|---|---|
| Finding an owner to make a purchase offer | Yes, as prospecting |
| Finding agents or brokers to market a service | Yes |
| Screening a rental applicant | No. Use a consumer reporting agency; FCRA permissible purpose and adverse action notices apply |
| Deciding whether to lend to a borrower | No. Same reason |
| Hiring or insurance decisions | No |

ScraperCity's terms make the user responsible for a lawful basis and legal review; `references/scrapercity-platform.md` records that these results are prospecting data only.

## 7. Email to owners and agents

CAN-SPAM applies to commercial email with no B2B exemption: accurate From and routing information, a subject that reflects the content, an ad disclosure, a valid postal address, an opt-out mechanism, and opt-outs honored within 10 business days. Penalties reach $53,088 per email. Validate emails with `validate_emails` ($0.0072 each) before sending to protect the domain.

## 8. Compliance check table for a plan

Every plan includes a table like this, one row per channel:

| Channel | Recipients | Law | Action |
|---|---|---|---|
| Direct mail | Pre-foreclosure owners | Regulation O (content), state wholesaling law | Purchase offer only; state disclosures in any contract |
| Manual calls | Owners with numbers that pass the DNC scrub | TCPA, TSR, 47 CFR 64.1200 | Scrub every 31 days, 8 a.m. to 9 p.m. local, live voice, internal DNC list |
| Email | Agents | CAN-SPAM | Postal address, opt-out, 10-business-day removal |

## Sources

- https://www.law.cornell.edu/uscode/text/47/227
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://www.fcc.gov/general/telemarketing-and-robocalls
- https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr
- https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://www.ftc.gov/business-guidance/resources/using-consumer-reports-what-landlords-need-know
- https://www.ecfr.gov/current/title-12/chapter-X/part-1015
- https://rejournals.com/real-estate-wholesaling-in-illinois-an-investment-strategy-under-scrutiny/
- https://oklahoma.gov/orec/resources/blog/wholesale-act.html
- https://www.barley.com/act-52-imposes-new-regulations-on-real-estate-wholesaling-in-pennsylvania/
- https://www.ohiorealtors.org/blog/2306/real-estate-wholesaling-legislation-takes-effect/
- https://www.llr.sc.gov/re/News/Wholesaling-Assignment-of-Contracts-Guidance.pdf
- https://california.public.law/codes/civil_code_section_1695.4
- https://www.mcguirewoods.com/client-resources/alerts/2023/5/pro-business-amendments-to-floridas-mini-tcpa-now-in-effect
