# TCPA and DNC Gate

The checks that decide how each appended mobile may be used. Run section 1 before spending anything and sections 3 and 4 after the append. This is a planning aid built from public sources, not legal advice; the user's counsel decides close calls.

## 1. Channel by consent matrix (US)

| How the number will be used | No consent on file | Prior express consent (informational) | Prior express written consent (telemarketing) |
|-|-|-|-|
| Human dials by hand or click-to-call, live voice | Allowed after DNC scrub, inside calling hours | Allowed | Allowed |
| Power or predictive dialer | Hold; counsel decides whether the system is an autodialer under Duguid | Allowed for informational calls | Allowed |
| Prerecorded or artificial voice, including AI voice | Not allowed | Informational only | Allowed |
| Ringless voicemail drop | Treat as prerecorded; not allowed | Informational only | Allowed |
| SMS, manual send | Treat as a call; default not allowed for sales texts | Informational only | Allowed |
| SMS, platform or bulk send | Not allowed | Informational only | Allowed |

"Informational" means no sales or marketing content: an appointment reminder, a delivery update. A recruiting or sales follow-up is not informational for this gate.

What counts as prior express written consent (47 CFR 64.1200(f)(9)): a written agreement, signed (e-signatures valid under state or federal law count), naming the number, authorizing the seller to deliver telemarketing by autodialer or prerecorded voice, with a clear disclosure that signing is not a condition of purchase. A LinkedIn connection, a business card, a webinar sign-up without that disclosure, or a number published on a website is not written consent.

## 2. Recipient and geography matrix

| Recipient | US federal | US state | Canada | UK |
|-|-|-|-|-|
| Business contact, company line | TSR DNC exemption covers most B2B sales calls; FCC rules still apply to automated calls | Some state laws cover business calls; check before automated use | DNCL rules do not apply to calls to businesses; keep an internal list | Screen CTPS (and TPS for sole traders) |
| Business contact, personal or mixed-use mobile | Registered mixed-use mobiles presumed residential in the 9th Circuit (Chennette); scrub and hold registered numbers unless counsel clears | State mini-TCPA laws such as Florida's FTSA cover automated calls and texts | Same as above; respect the internal list | TPS covers individuals and sole traders |
| Consumer | Full DNC, calling hours, consent for automated calls | Full state rules | DNCL applies unless an exemption fits | TPS; consent for automated calls |

## 3. Scrub procedure

Run the checks in this order, cheapest and strictest first.

1. Internal do-not-call list (every number anyone asked you not to call, across all campaigns). Match on E.164. Any hit is `hold_internal_dnc`, permanently.
2. National DNC Registry. The user downloads or queries through their own subscription account; the FTC says data for up to five area codes is free and requires syncing at least every 31 days. Record `dnc_checked_at`.
3. State DNC lists the user subscribes to.
4. For numbers with consent on file only: the FCC Reassigned Numbers Database, using the date of consent as the date the number last belonged to the person. A "yes" (disconnected since) moves the row to hold.
5. Record the scrub in the run log: date, lists, counts removed.

A number not scrubbed within 31 days of the first dial is `hold_dnc` by default, even on a B2B list.

## 4. Dial status assignment

```text
if number on internal list                      -> hold_internal_dnc
elif number shared by 2+ people                 -> hold_shared_number
elif plan needs mobile and line_type not mobile -> hold_line_type
elif on national or state DNC and not cleared   -> hold_dnc
elif not scrubbed within 31 days                -> hold_dnc
elif consent on file and reassigned check ok    -> callable_auto_consented
else                                            -> callable_manual
sms_allowed = yes only when the consent record covers texts
```

"Cleared" means the user's counsel approved calling registered numbers for this B2B campaign and the approval is written in the report.

## 5. Calling hours and time zones

- No telephone solicitation before 8 a.m. or after 9 p.m. in the called party's local time (47 CFR 64.1200(c)(1)). Some states set narrower windows; check the state before a campaign that targets one state heavily.
- Take the time zone from the person's city and state. A mobile area code shows where the number was issued, not where the person lives now.
- When the location is unknown, dial only inside the overlap of the four contiguous US time zones, roughly 11 a.m. to 8 p.m. Eastern, which is 8 a.m. to 5 p.m. Pacific.

## 6. Opt-outs during the campaign

- Honor any "stop calling" request immediately and add it to the internal list; the rule ceiling is 10 business days, the operating standard is the same day.
- For texts, STOP and similar keywords are per se reasonable revocations under the FCC's 2025 rules. One confirmation text within 5 minutes, no marketing, is allowed.
- Keep internal list entries for at least 5 years (US) and 3 years (Canada).

## 7. Compliance gate table for the report

Every report includes one row per question, and each row names its law:

| Question | Answer | Law | Action |
|-|-|-|-|
| Dialing method | Manual click-to-call, live voice | TCPA, 47 U.S.C. 227(b) | No prerecorded or AI voice; no predictive dialer |
| Texts | None planned | TCPA, 47 CFR 64.1200 | `sms_allowed = no` |
| Recipients | IT leaders at hospitals, business role, personal mobiles | TSR B2B exemption; 47 CFR 64.1200(c), (e); Chennette | Scrub; hold Registry hits |
| Calling hours | 8 a.m. to 9 p.m. local | 47 CFR 64.1200(c)(1) | Store `tz` per person |
| Internal list | Maintained in the dialer | 47 CFR 64.1200(d) | Same-day adds; keep 5 years |
| State law | Contacts in Florida | Florida Telephone Solicitation Act | Manual only; no texts |

## Sources

- 47 U.S.C. 227: https://www.law.cornell.edu/uscode/text/47/227
- 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FTC, Q&A about DNC provisions of the TSR: https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0
- FTC, Complying with the Telemarketing Sales Rule: https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule
- Chennette v. Porch.com summary: https://olshanlaw.com/Advertising-Law-Blog/ninth-circuit-issues-pro-plaintiff-ruling-in-do-not
- Florida mini-TCPA amendments: https://www.mcguirewoods.com/client-resources/alerts/2023/5/pro-business-amendments-to-floridas-mini-tcpa-now-in-effect
- FCC revocation of consent rules: https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/fcc-sets-effective-date-for-tcpa-reasonable-consent-revocation-rules
- Reassigned Numbers Database overview: https://tcpaworld.com/2021/11/01/happy-reassigned-number-database-day-the-fccs-new-recycled-number-spotting-database-is-live-heres-how-to-use-it/
- CRTC National DNCL exemptions: https://lnnte-dncl.gc.ca/en/Organization/Exemptions
- ICO telephone marketing: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/telephone-marketing/
