# Identifier Strategy and Match Scoring

How to pick the search for each row, how many results to pay for, and how to decide whether a returned person is the right one.

## 1. Identifier ladder

Search the strongest identifier a row has. Weaker identifiers are used to score, not to search.

| Rank | Identifier | Why it is strong or weak | Search with |
|-|-|-|-|
| 1 | Full street address with ZIP, plus the expected name | The address narrows to a household; the name confirms the person | `street_citystatezip`, score with the name |
| 2 | Phone number | Usually one current subscriber | `phone_number` |
| 3 | Personal email | Usually one person | `email` |
| 4 | Full address with ZIP, no name | Returns people tied to the address: owners, tenants, relatives, former residents | `scrape_property_lookup` with owner contact when the owner is needed; else `street_citystatezip` capped at the probable band |
| 5 | Name plus last known address | The person may have moved | `street_citystatezip` with the old address first; `name` search if they are gone |
| 6 | Name plus city and state | Common names collide | `name` with `max_results: 3`, score on city and state |
| 7 | Name only | Many candidates | Do not search; find a second identifier first |

The catalog lists `name`, `email`, `phone_number` and `street_citystatezip` as separate arrays. It does not document pairing values across arrays into one search, so treat each entry as its own search.

## 2. Setting `max_results`

People Finder bills $0.0199 per result, and a search with 0 matches is billed as 1 result. Every search costs at least $0.0199; a search that returns 3 people costs $0.0597.

| Search type | `max_results` | Reason |
|-|-|-|
| Address, phone, email | 1 | The first result is the best candidate; more results add cost and rarely change the answer |
| Name with city and state | 3 | Enough to see a collision and score it |
| Rescue name search after a weak address match | 3 | Same |
| Common surname in a large metro (Smith, Garcia, Nguyen, Johnson) | 5 only for high-value rows | Otherwise mail only |

Ceiling formula: `searches x max(max_results, 1) x $0.0199`.

## 3. Scoring rubric

Score each returned candidate against what the input already knows. Keep the best-scoring candidate per input row.

### Points

| Evidence | Points | Notes |
|-|-|-|
| Exact first and last name match to the expected person | 40 | Normalize case, accents, suffixes (Jr, Sr, III) |
| Last name plus nickname or initial (Bob for Robert, J. for James) | 30 | Use the nickname table in `crm-enricher` or a standard list |
| Last name only | 15 | Spouse or relative at the same address |
| Hyphenated or maiden name matches one part | 25 | Marriage name changes |
| Current address equals the input address | 25 | After USPS normalization, unit included |
| Same city and state, different street | 10 | Moved locally |
| Input phone or email appears in the result | 20 | Strong corroboration |
| A phone or address in the result is marked current or recent | 10 | Only if the CSV has such a field |
| Age or life-status fields consistent with the input, no deceased flag | 5 | Only if present |

### Rescaling when fields are missing

Score only with fields present in the downloaded CSV header and only with what the input knows:

```text
points_available = sum of the points for evidence types that can be checked for this row
score = round(points_earned / points_available x 100)
```

Example: an A1 address row with an owner name, where the CSV has name and address fields but no recency or age: available = 40 + 25 + 20 = 85. A result with an exact name and the same address earns 65, so the score is 76 (probable). If the owner's phone from the county filing also appears, 85 / 85 = 100 (confirmed).

### Caps

| Situation | Cap |
|-|-|
| No expected name for the row | 79 (probable at best); the call opens with an identity check |
| Result has a deceased flag | 39 (no match for outreach); route to the estate |
| Two candidates within 10 points of each other | 59 (weak); mail only until resolved |

### Bands

| Band | Score | Outreach allowed |
|-|-|-|
| `confirmed` | 80 to 100 | Manual calls after DNC scrub, mail, email if validated |
| `probable` | 60 to 79 | Manual calls opening with "Am I speaking with the owner of 2217 Elmwood?", mail |
| `weak` | 40 to 59 | Mail only |
| `no_match` | 0 to 39 | Rescue search, Property Lookup, or drop |

## 4. Rescue rules

| Row after the first pass | Rescue | Stop when |
|-|-|-|
| A1 weak or no match | `name` search with `max_results: 3`, score with the city and state | Best candidate reaches probable, or after one rescue |
| N1 person moved (address search found other people) | `name` search, `max_results: 3` | Same |
| A2 address, owner unknown | `scrape_property_lookup` with `includeOwnerContact: true` | Owner name returned |
| P or E no match | No rescue; the identifier is stale | Drop or mail |

Never run more than one rescue per row. A row that fails twice costs more than it is worth.

## 5. Owner types and special cases

| Situation | How to spot it | Action |
|-|-|-|
| LLC, corporation | Owner name contains LLC, INC, CORP, LP, LLP | Do not search as a person. Look up the registered agent and managers in the state business registry; mail the entity's address |
| Trust | Owner name contains TRUST, TR, TRUSTEE | Search the named trustee as a person if listed; else mail |
| Bank or lender (REO) | Lender name as owner, or `bankOwned` distress type | Drop from homeowner outreach; contact the listing agent |
| Estate or deceased owner | Deceased flag, probate filing, "ESTATE OF" | Mail the estate; call only the personal representative named in probate |
| Multi-unit property | Unit numbers on the address, several unrelated people returned | Property Lookup with owner contact; residents are likely tenants |
| Absentee owner | Owner mailing address differs from the property | Search the mailing address, score with the owner name |
| Co-owners | Two names on the record | Search both; keep both if both score probable or better |

## 6. Address normalization quick rules (USPS Publication 28)

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

Format for `street_citystatezip`: `2217 Elmwood Ave, Columbus, OH 43211`. Keep unit numbers; a missing unit on a multi-unit building returns every resident.

## Sources

- ScraperCity tool catalog (People Finder inputs and billing): references/scrapercity-catalog.md
- USPS Publication 28, Postal Addressing Standards: https://pe.usps.com/text/pub28/welcome.htm
- USPS Publication 28, Appendix C1 street suffix abbreviations: https://pe.usps.com/text/pub28/28apc_002.htm
- ScraperCity skills page (strongest identifier first): https://scrapercity.com/skills
