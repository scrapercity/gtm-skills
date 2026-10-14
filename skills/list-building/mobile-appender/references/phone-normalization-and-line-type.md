# Phone Normalization and Line Type

How to prepare inputs for `find_mobiles`, and how to turn its output into numbers a dialer can trust.

## 1. Input normalization

### LinkedIn URLs

| Raw input | Action | Normalized |
|-|-|-|
| `http://linkedin.com/in/Priya-Natarajan/` | Lowercase, https, www, strip trailing slash | `https://www.linkedin.com/in/priya-natarajan` |
| `https://www.linkedin.com/in/priya-natarajan?originalSubdomain=uk` | Strip query string | `https://www.linkedin.com/in/priya-natarajan` |
| `https://uk.linkedin.com/in/priya-natarajan` | Country subdomain to www | `https://www.linkedin.com/in/priya-natarajan` |
| `https://www.linkedin.com/in/priya-natarajan/en` | Strip locale suffix | `https://www.linkedin.com/in/priya-natarajan` |
| `https://www.linkedin.com/in/priya-natarajan/details/experience/` | Strip sub-pages | `https://www.linkedin.com/in/priya-natarajan` |
| `https://www.linkedin.com/company/coastal-health` | Company page, not a person | Drop, reason `NOT_A_PERSON` |
| `https://www.linkedin.com/sales/lead/ACwAA...` | Sales Navigator link, not a public profile | Drop, reason `SALES_NAV_LINK`; ask for the public URL |
| `https://www.linkedin.com/pub/...` | Legacy public URL | Keep as given; flag for manual check if no hit |

Percent-encoded slugs (non-Latin names) stay encoded. Do not decode them.

### Emails

1. Trim, lowercase, strip `mailto:`.
2. Reject syntax failures.
3. Freemail addresses (gmail.com, outlook.com, yahoo.com and so on) are personal emails. Mobile Finder's catalog description names work email addresses; send a freemail only when no LinkedIn URL or work email exists, and mark the row `input_quality = personal_email`.
4. Role addresses (info@, sales@) do not identify a person. Drop with reason `ROLE_ADDRESS`.

### One input per person

Build a person key (`linkedin_url`, else `email`). If a person has both, send the URL in the first run and keep the email for a second run on URL misses only. Deduplicate on the person key before the pilot.

## 2. Output to E.164

E.164: a plus sign, the country code, then the national significant number, 15 digits at most.

| Country | Country code | National number rule | Example raw | E.164 |
|-|-|-|-|-|
| US, Canada | 1 | 10 digits; area code and exchange each start 2 to 9 | `(512) 555-0142` | `+15125550142` |
| United Kingdom | 44 | Drop the trunk 0; mobiles are in the 07 range, which also holds 070 personal numbers | `07700 900123` | `+447700900123` |
| Australia | 61 | Drop the trunk 0; mobiles start 4 after the code | `0412 345 678` | `+61412345678` |
| Germany | 49 | Drop the trunk 0; mobile prefixes start 15, 16 or 17 | `0151 23456789` | `+4915123456789` |
| India | 91 | 10-digit mobile starting 6 to 9 | `98765 43210` | `+919876543210` |

Steps:

1. Split extensions (`x`, `ext`, `#`) into `phone_ext`. A mobile with an extension is a desk line; flag `hold_line_type`.
2. Strip everything except digits and a leading plus.
3. Add the country code from the person's country when the number lacks one. If the country is unknown and the number is not already in plus format, do not guess: flag `COUNTRY_UNKNOWN`.
4. Validate length and the US rule (area code and exchange not starting with 0 or 1). Failures are blanked and flagged `BAD_FORMAT`.
5. Store as text. Spreadsheets strip the plus sign and turn long numbers into scientific notation.

Regex used by the checker: `^\+[1-9]\d{7,14}$`.

## 3. Line type

### Why the number alone is not enough

Numbers move between switches and carriers, so the prefix is no longer an effective way to determine line type (Service Objects, September 10, 2015). An exchange once assigned to a mobile carrier can now hold a landline, and the reverse. A lookup is the only way to know.

### Lookup output to `line_type`

A carrier lookup such as Twilio Lookup Line Type Intelligence returns values like these. Map them:

| Lookup value | `line_type` | Dial-plan effect |
|-|-|-|
| mobile | mobile | Callable |
| landline | landline | Hold if the plan is a mobile-only list |
| fixedVoip | voip_fixed | Desk phone through a business VoIP service; often a direct dial; hold for review |
| nonFixedVoip | voip_nonfixed | Google Voice style number; can be personal; review by hand |
| tollFree, premium, sharedCost, uan | other | Drop from a mobile list |
| voicemail, pager | other | Drop |
| personal | other | Review by hand |
| unknown | unknown | Hold if the plan needs true mobiles |

Canadian numbers may need separate approval in some lookup services; when the lookup errors, keep `line_type = unknown`.

### When to pay for a lookup

| Plan | Lookup needed? |
|-|-|
| Click-to-call, small list | Optional; reps will learn the line type on the first call |
| Power dialer that should only ring mobiles | Yes, every number |
| Writing numbers back into a CRM mobile field | Recommended, so the field means what it says |

## 4. Shared and suspicious numbers

| Signal | What it usually is | Status |
|-|-|-|
| Same number on two or more people | Office main line or reception | `hold_shared_number` |
| Same number as the company's published main line | Switchboard | Move to `phone`, not `mobile` |
| Number differs from the CRM mobile for the same person | Newer number, or a wrong match | Keep both; ask the rep which works |
| 555-01XX in US numbers | Reserved fictional range | Drop |

## 5. Time zones

Use the person's city and state (or country) to set `tz` as an IANA zone such as `America/Chicago`. Fall back to the company HQ only when the person's location is missing, and mark `tz_source = company_hq`. Do not infer from the mobile's area code.

## 6. Output columns

| Column | Example | Rule |
|-|-|-|
| `mobile` | `+15125550142` | E.164 text |
| `input_used` | `linkedin_url` | Which identifier found it |
| `line_type` | `mobile` | Section 3 values or `unchecked` |
| `suppressed` | `no` | `yes`, `no`, `unchecked` |
| `suppression_checked_at` | `2026-10-13` | ISO date |
| `tz` | `America/Chicago` | IANA zone |
| `dial_status` | `callable` | Vocabulary in `dial-status-and-suppression.md` section 3 |
| `source` | `mobile_finder` | Controlled vocabulary |

## Sources

- Twilio, What is E.164: https://www.twilio.com/docs/glossary/what-e164
- Twilio, Lookup Line Type Intelligence: https://www.twilio.com/docs/lookup/v2-api/line-type-intelligence
- Service Objects, The Benefits and Uses of Local Number Portability (2015-09-10): https://www.serviceobjects.com/blog/the-benefits-and-uses-of-local-number-portability/
- Ofcom, Numbering (070 personal numbering guidance): https://www.ofcom.org.uk/phones-and-broadband/phone-numbers/numbering
- North American Numbering Plan Administrator: https://www.nationalnanpa.com/
- IANA Time Zone Database: https://www.iana.org/time-zones
