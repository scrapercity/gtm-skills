# Identifier Strategy and Match Banding

How to pick the search for each row, how many results to pay for, and how to decide whether a returned person is the right one.

## 1. Identifier ladder

Search the strongest identifier a row has. Weaker identifiers are used to band the match, not to search.

| Rank | Identifier | Why it is strong or weak | Search with |
|-|-|-|-|
| 1 | Full street address with ZIP, plus the expected name | The address narrows to a household; the name confirms the person | `street_citystatezip`, band with the name |
| 2 | Phone number | A number belongs to one subscriber at a time | `phone_number` |
| 3 | Personal email | A personal inbox belongs to one person | `email` |
| 4 | Full address with ZIP, no name | Returns people tied to the address: owners, tenants, relatives, former residents | `scrape_property_lookup` with owner contact when the owner is needed; else `street_citystatezip` capped at the probable band |
| 5 | Name plus last known address | The person may have moved | `street_citystatezip` with the old address first; `name` search if they are gone |
| 6 | Name plus city and state | Common names collide | `name` at the user's `max_results` setting, band on city and state |
| 7 | Name only | Many candidates | Do not search; find a second identifier first |

The catalog lists `name`, `email`, `phone_number` and `street_citystatezip` as separate arrays. It does not document pairing values across arrays into one search, so treat each entry as its own search.

## 2. Setting `max_results`

People Finder bills $0.0199 per result, and a search with 0 matches is billed as 1 result. Every search costs at least $0.0199; a search that returns 3 people costs $0.0597.

| Search type | `max_results` | Reason |
|-|-|-|
| Address, phone, email | 1 | The identifier points to one household or subscriber, and every extra result is billed |
| Name with city and state | The user's setting (the example uses 3) | The number of same-name candidates the user will pay to compare |
| Rescue name search after a weak address match | Same setting | Same |

Ceiling formula: `searches x max(max_results, 1) x $0.0199`.

## 3. Banding by evidence

Compare each returned candidate with what the input already knows, using only fields present in the downloaded CSV header. Keep the candidate with the strongest evidence per input row and write the evidence to `match_evidence`.

### Evidence types

| Token | What agrees | Notes |
|-|-|-|
| `name` | Expected first and last name, or last name plus a nickname or initial (Bob for Robert, J. for James) | Normalize case, accents and suffixes (Jr, Sr, III) first |
| `surname` | Last name only, or one part of a hyphenated or maiden name | Spouse, relative or a married name |
| `address` | Result's current address equals the input address | After USPS normalization, unit included |
| `city` | Same city and state, different street | Moved locally |
| `contact` | An input phone or email other than the one searched appears in the result | Corroboration from a second identifier |
| `owner_record` | Property Lookup returned a person as owner of record for the input address | The property record names the owner |

### Evidence to band

| Evidence | Band |
|-|-|
| `name+address`, `name+contact`, `name+address+contact`, `owner_record` | `confirmed` |
| `name+city`, `surname+address`, `address_only` (no expected name for the row) | `probable` |
| `name_only`, `surname+city`, `tie` (two candidates with the same evidence), `entity` (LLC, trust or bank owner) | `weak` |
| `none`, `deceased` | `no_match` |

A row with no expected name can reach `probable` at best from People Finder; the call opens with an identity check. Property Lookup with owner contact is the path to `confirmed` for those rows.

### Bands

| Band | Outreach |
|-|-|
| `confirmed` | Calls, mail, email if validated |
| `probable` | Calls opening with "Am I speaking with the owner of 2217 Elmwood?", mail |
| `weak` | Mail only |
| `no_match` | Rescue search, Property Lookup, or mail to "Current Owner" |

The QA sample in `skip-trace-runbook.md` section 9 tests this table against the owner of record. When missed rows share an evidence type, that type moves down one band for the rest of the file.

## 4. Rescue rules

| Row after the first pass | Rescue | Stop when |
|-|-|-|
| A1 weak or no match | `name` search at the user's setting, banded with the city and state | Best candidate reaches probable, or after one rescue |
| N1 person moved (address search found other people) | `name` search at the user's setting | Same |
| A2 address, owner unknown | `scrape_property_lookup` with `includeOwnerContact: true` | Owner name returned |
| P or E no match | No rescue; the identifier is stale | Drop or mail |

The plan budgets one rescue per row. A second pass is another billed search; price it before adding it.

## 5. Owner types and special cases

| Situation | How to spot it | Action |
|-|-|-|
| LLC, corporation | Owner name contains LLC, INC, CORP, LP, LLP | Do not search as a person. Look up the registered agent and managers in the state business registry; mail the entity's address |
| Trust | Owner name contains TRUST, TR, TRUSTEE | Search the named trustee as a person if listed; else mail |
| Bank or lender (REO) | Lender name as owner, or `bankOwned` distress type | Drop from homeowner outreach; contact the listing agent |
| Estate or deceased owner | Deceased flag, probate filing, "ESTATE OF" | Mail the estate; call only the personal representative named in probate |
| Multi-unit property | Unit numbers on the address, several unrelated people returned | Property Lookup with owner contact; the residents returned may be tenants |
| Absentee owner | Owner mailing address differs from the property | Search the mailing address, band with the owner name |
| Co-owners | Two names on the record | Search both; keep both if both reach probable or better |

## 6. Ranking phones inside a row, and phones shared across rows

A matched person often comes back with several numbers, and reps dial `phone_1` first. Order the numbers by the recency field the CSV header holds (marked current or most recently seen first). Line type order is set from your own results: after the first call block, compute connect rate by line type (mobile, landline, VoIP or unknown) and sort ties by the type that connected most. Ties after that break on the number that also appears in the input file. The output keeps `phone_1` to `phone_3`.

A phone that appears on two or more unrelated matched owners in one batch is a shared line (a property manager, an office, a relative who co-signs). Mark it `shared_line` in `flags` and move it to the end of every row's order; never use it as the only callable phone for a row.

## 7. Owners with several properties

Group the matched rows by `matched_name` plus the best phone or mailing address. An owner who appears on two or more input properties is a portfolio owner:

| Rule | Action |
|-|-|
| 2 or more properties under one matched owner | Flag `PORTFOLIO` on every row; one call covers all of them, opened with the full address list |
| Same owner, different mailing addresses | Keep the mailing address seen most often; send one letter listing every property |
| Portfolio owner weak on one property and confirmed on another | Use the confirmed match for all rows |

Portfolio owners go to the top of the call queue: one conversation covers several properties.

## 8. Address normalization quick rules (USPS Publication 28)

| Raw | Standard |
|-|-|
| Avenue, Ave. | AVE |
| Lane | LN |
| Drive | DR |
| Street | ST |
| Road | RD |
| Boulevard | BLVD |
| North, South, East, West (directional) | N, S, E, W |
| Apartment, Suite, Unit, # | APT, STE, UNIT |
| State names | Two-letter codes |
| ZIP | 5 digits as text, ZIP+4 optional |

Format for `street_citystatezip`: `2217 Elmwood Ave, Columbus, OH 43211`. Keep unit numbers; without one, a search on a multi-unit building can return residents of every unit.

## Sources

- ScraperCity tool catalog (People Finder inputs and billing): references/scrapercity-catalog.md
- USPS Publication 28, Postal Addressing Standards: https://pe.usps.com/text/pub28/welcome.htm
- USPS Publication 28, Appendix C1 street suffix abbreviations: https://pe.usps.com/text/pub28/28apc_002.htm
- Franklin County Auditor, Ohio (owner of record): https://auditor.franklincountyohio.gov/home
