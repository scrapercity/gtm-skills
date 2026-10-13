# Dialing Compliance Gate

The per-number check every phone record passes before it reaches a dialer. It turns `references/outbound-compliance-primer.md` into steps a rep or a script can run. Not legal advice: a program that calls consumers at volume, or calls outside the US, gets a lawyer's review first.

## 1. Classify the number

| Field from ScraperCity | Typical line | Default class | Why |
|-|-|-|-|
| `phone` on a Local Business Database, Google Maps or Yelp record | Business main line, but often the owner's cell for small trades | Business if a line type lookup says landline or VoIP; consumer if wireless | Sole proprietors list personal mobiles as the business number |
| Lead Database phone fields | Company switchboard or direct dial | Business, unless wireless | A wireless direct dial may be a personal phone |
| `contact_mobile` (Local Business Database named contact) | Mobile | Consumer | Wireless numbers fall under 47 CFR 64.1200(e) |
| `mobile_number` from `find_mobiles` | Mobile | Consumer | Same |
| Owner phone from `find_people` or `scrape_property_lookup` | Residential or mobile | Consumer | Homeowners are consumers |
| Store Leads phone (`phones: true`) | Store support line or owner cell | Line type lookup decides | Small stores often use a personal number |

Line type lookup: use your dialer's carrier or line type check, or a carrier lookup API. ScraperCity does not return line type, so this cost is a user input.

## 2. Gate steps

Run in order. Stop at the first Drop.

| Step | Question | Yes | No | Rule |
|-|-|-|-|-|
| 1 | Will any call to this list use an autodialer, a prerecorded or artificial voice, an AI voice agent, or a ringless voicemail drop? | Drop that method for every number on the list | Go to 2 | 47 U.S.C. 227(b); 47 CFR 64.1200(a)(1)(iii) and (a)(2); FCC 24-17 |
| 2 | Is the number on the company DNC list, or did the contact opt out on any channel? | Drop | Go to 3 | 47 CFR 64.1200(d); internal policy |
| 3 | Is the number consumer class (section 1)? | Go to 4 | Go to 5 | 47 CFR 64.1200(c), (e) |
| 4 | Is it on the National DNC Registry, checked against a copy pulled within the last 31 days? | Drop, unless counsel confirms the call is B2B and exempt | Go to 5 | 47 CFR 64.1200(c)(2); TSR 16 CFR 310.6(b)(7) |
| 5 | Is it on a state no-call list for a state that keeps one (for example Texas)? | Drop | Go to 6 | State law |
| 6 | Is it 9am to 8pm, Monday to Friday, in the recipient's time zone? | Go to 7 | Reschedule | 47 CFR 64.1200(c)(1); Tex. Bus. & Com. Code 301.051; Fla. Stat. 501.616(6) |
| 7 | Fewer than 3 calls to this number about this offer in the last 24 hours, and fewer than 6 attempts total? | Go to 8 | Reschedule or stop | Fla. Stat. 501.616(6); Oklahoma HB 3168; Maryland 2023 ch. 413; house cap |
| 8 | Is the recipient in Canada, the UK or the EU? | Apply section 4 | Call | CRTC; ICO PECR; GDPR |

Record the result per number (section 6).

## 3. State hours and caps

The federal window is 8am to 9pm. These states are tighter. The house window, 9am to 8pm weekdays, satisfies all of them.

| State | Window | Cap | Note | Source |
|-|-|-|-|-|
| Texas | 9am to 9pm; Sunday noon to 9pm | | Texas keeps its own no-call list; SB 140 (2025) made violations of the no-call chapter suable under the DTPA and brought texts into Chapter 302 | Tex. Bus. & Com. Code 301.051 (Texas State Law Library); SB 140 analysis |
| Florida | 8am to 8pm | 3 calls per 24 hours per person on the same subject, any number | Automated selection or dialing needs prior express written consent; texts and voicemail transmissions count | Fla. Stat. 501.616(6), 501.059 |
| Oklahoma | 8am to 8pm | 3 per 24 hours | Effective 1 Nov 2022; $500 per violation, up to 3x | HB 3168 (2022) |
| Maryland | No calls 8pm to 8am | 3 per 24 hours | Effective 1 Jan 2024; no altered voice to disguise the caller | 2023 ch. 413 |
| All other states | Federal 8am to 9pm unless the state sets tighter | | Check each state on the list before launch | 47 CFR 64.1200(c)(1) |

Time zone: use the number's area code only as a fallback. Prefer the business address (`city`, `state`, `postal_code`) or the contact's location. Area codes travel with ported mobiles.

## 4. Outside the US

| Country | Business line | Mobile or residential | Source |
|-|-|-|-|
| Canada | Exempt from National DNCL rules; Telemarketing Rules still apply; internal list honored within 14 days | Scrub the National DNCL | CRTC |
| Canada hours | Weekdays 9am to 9:30pm, weekends 10am to 6pm | Same | CRTC |
| United Kingdom | Screen TPS and CTPS and your own list | Screen TPS | ICO PECR telephone marketing |
| European Union | Counsel per country | Counsel per country | GDPR, national law |

## 5. Dialer settings

| Setting | Required value | Why |
|-|-|-|
| Dial mode | Manual or click-to-call, one line per rep | Keeps calls rep-initiated and live |
| Parallel or predictive dialing | Off | Autodialer risk and the 3% abandoned-call limit (47 CFR 64.1200(a)(7)) |
| Voicemail drop (prerecorded) | Off on cold lists | Prerecorded message to a wireless number needs consent |
| AI voice agent or voice cloning | Off on cold lists | FCC 24-17 |
| Caller ID | A real, callable number that rings to the rep or a monitored line | Company DNC rule requires a contact number; callbacks book meetings |
| Local presence (area code matching) | Only numbers you own and answer | Callbacks must reach you |
| Call recording | Follow two-party consent states: announce recording or turn it off | State wiretap laws differ; check with counsel |
| DNC sync | Dialer reads the company DNC list before every dial | Same-day suppression |

## 6. Gate record per number

| Field | Example |
|-|-|
| `phone_e164` | +12145550182 |
| `number_source` | local_db `phone` |
| `line_type` | wireless |
| `number_class` | consumer |
| `national_dnc_checked_at` | 2026-10-12 (registry copy dated 2026-10-01) |
| `national_dnc_result` | clear |
| `state_dnc_result` | clear (Texas) |
| `company_dnc_result` | clear |
| `recipient_tz` | America/Chicago |
| `window_local` | 09:00 to 20:00 Mon to Fri |
| `attempts_24h` | 0 |
| `attempts_total` | 1 |
| `gate_result` | pass |

## 7. When a contact says stop

1. Say you will remove them and end the call.
2. Add the number (and the email, if known) to the company DNC list the same day; the rule allows up to 10 business days, the house standard is same day.
3. Keep the entry 5 years (47 CFR 64.1200(d)(6)).
4. Stop every channel for that person: email, LinkedIn, mail.

## Sources

- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf
- https://www.law.cornell.edu/uscode/text/47/227
- https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310/section-310.6
- https://sll.texas.gov/faqs/how-late-can-telemarketers-call
- https://capitol.texas.gov/tlodocs/89R/analysis/html/SB00140F.htm
- http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.616.html
- http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.059.html
- https://oklegislature.gov/cf_pdf/2021-22%20ENR/hB/HB3168%20ENR.PDF
- https://mgaleg.maryland.gov/2023RS/chapters_noln/Ch_413_sb0090E.pdf
- https://crtc.gc.ca/eng/phone/telemarketing/exempt.htm
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/telephone-marketing/
- https://www.ftc.gov/news-events/news/press-releases/2026/08/ftc-announces-2027-telemarketer-fees-access-national-do-not-call-registry
