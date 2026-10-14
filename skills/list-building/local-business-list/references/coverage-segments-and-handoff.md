# Coverage Checks, Segments and Handoff

Jobs that sit around the pull itself: proving the list covers the market, naming the owner, screening out group-run locations, cutting it into segments that each have a reason to write, feeding call outcomes back into the list, and handing files to a sequencer or dialer in a shape that sends on day one. Prices come from `references/scrapercity-catalog.md`. Thresholds are set by the user from their own lists.

## 1. Outside lists as a coverage check

The database and the scrapes only show what they hold. An outside list built for another purpose (licensing, billing) gives a count to compare against and a set of businesses the scrapes missed.

| Vertical family | Outside list | How to get it | Match key against the pool | What it adds |
|-|-|-|-|-|
| Dentists, chiropractors, optometrists, physical therapy, dermatology, counseling (veterinarians have no NPI) | CMS NPI Registry, organization records (NPI type 2) | Free API: `https://npiregistry.cms.hhs.gov/api/?version=2.1&enumeration_type=NPI-2&taxonomy_description=Dentist&city=Kyle&state=TX&limit=200`, page with `skip`; statewide jobs use the monthly full download file | Practice location phone (E.164), then `business_name_key` plus ZIP | Practice name, taxonomy, practice location address and phone; no email or website |
| Contractors in states that publish licensee files (roofers, HVAC, electricians, pool, general contractors) | State licensing board download, for example Florida DBPR `CONSTRUCTIONLICENSE_1.csv` | CSV download from the board's public records page | `business_name_key` (from the DBA name when present) plus ZIP | Licensee and DBA name, address, county code, license class, original licensure date, status |
| Any category | US Census County Business Patterns | Census site or API by county and NAICS code | Count only | Establishment count with paid employees, about two years old |

Checked 2026-10-13: an NPI Registry call for organization dentists returns the legal organization name, the authorized official with title (for example "Owner/President"), taxonomy ("Dentist, General Practice"), enumeration date, and a location phone. A page holds at most 200 records and `skip` stops at 1,000 (`skip=1000` and `skip=1200` return the same first record), so one query returns at most 1,200 records. Query one city at a time and split any city that reaches 1,200 by ZIP code. The `city` filter matches any address on the record, so count only records whose LOCATION address is in the sub-area (Denver, CO: 331 records matched the city, 302 had a Denver practice address). The Florida DBPR construction file is a CSV with license class, county code and original licensure date.

When web access is available, run these free counts before the plan goes to the user. A measured outside count is the planning number; a guessed one is not written down.

### Procedure

1. Pull the outside list for the same sub-areas as the geography split.
2. Normalize: phone to E.164, name to `business_name_key`, ZIP to 5 digits as text.
3. Match each outside row to the pool (database plus scrapes) by the keys above.
4. Coverage per sub-area = outside rows matched / outside rows.
5. Act on the result against the coverage target the user sets (no published benchmark exists for it):

| Coverage of the outside list in a sub-area | Action |
|-|-|
| At or above the target | No more spend there |
| Below the target | One Maps run in that sub-area with the top terms, then recheck |
| Still below after that run | Split the sub-area into ZIP codes, Maps per ZIP, then recheck |

6. Rows found only in the outside list have no website or email. Keep them in the phone file, or run a Maps search on the business name and city (a Google Maps search link passed as `url`) to get the website, then Website Finder for the email. Only do this when the user wants every business; it costs a Maps row and a Website Finder lookup per business.

Write the result as one line in the report: "NPI Registry check: 61 of 66 organization dentists in Kyle and Buda matched (92%)."

### Maps by sub-city or by ZIP

`maxCrawledPlacesPerSearch` caps each term, and the terms in one run overlap (the same practice matches "dentist" and "dental clinic"). When a sub-area's outside-list count or database count is above the per-term cap, one run cannot reach every business there: run Maps by ZIP in that sub-area from the start, using the ZIPs on the outside list's location addresses. Below the cap, one run per sub-area, split later only if a term returns at its cap.

## 1b. Owner names

A name goes in `owner_name` only when its source says the person owns the business. Sources in the order they are tried:

| Order | Source | How | What it settles |
|-|-|-|-|
| 1 | State business entity registry, where it lists principals | Search the legal name from the NPI record or license file (for example "BREATHE DENTAL, LLC"). Arizona's Corporation Commission eCorp search takes an entity name or a principal name. Colorado's register lists only the registered agent, so the step is skipped there; a registered agent is never written as the owner | Members, managers or officers of the legal entity |
| 2 | NPI organization record, authorized official | Title or position says Owner, President or Partner, or the credential is DDS or DMD | One named official per organization |
| 3 | Local Business Database contact or Website Finder contact | Title says Owner, President or Dentist-Owner | Name and often the owner's own email |
| 4 | Licensed-individual check (health practices) | NPI Registry, individual records (`enumeration_type=NPI-1`) by first name, last name and state, with the same taxonomy | Confirms the named person holds a license in that field; a principal with no individual record is likely a management company or investor |

Conflict rule: a name from source 1 or 2 that passes check 4 wins. When sources name different people, keep the winner in `owner_name`, put the other in `contact_name` with its title, and set `owner_check = conflict` so the 20-row hand check opens those first. When no source names an owner, `owner_name` stays blank.

One owner, several locations: give every row an `owner_key` (owner name plus legal entity). The email file holds one row per `owner_key` so the owner gets one sequence; the call file keeps one row per location phone.

## 1c. Independence screen (chains, franchises, DSOs)

Run it before any paid enrichment, so no Website Finder or Email Finder spend goes on group-run locations.

| Signal | Source of the signal | Action |
|-|-|-|
| Brand or domain on more locations than the user's chain line | The pull itself | Drop or tag, per the user's decision |
| Brand on the metro's group list | Built at run time: the national groups' location pages for the state, a web search for "[state] dental support organization" (or the vertical's equivalent), plus names the user supplies | Drop or tag |
| The location appears on a group's own list of supported offices | Groups publish acquisitions under the practices' own names: Heartland Dental's December 2025 growth spotlight listed 15 newly supported offices by practice name, Roosevelt Commons Dental Care (AZ) among them | Add each listed name to the screen |
| Homepage text names a group ("supported by", "affiliated with", a group brand) | Becker's Dental Review (Oct 2025) on a Cape Coral practice that "operates as Chiquita Dental Care and is supported by" Heartland Dental: the practice name alone hides the group | Fetch the homepage of each remaining row when web access is available; tag matches for review |
| NPI authorized official holds a corporate title (CEO, CFO, VP, Secretary, Treasurer) or the NPI legal name belongs to a group entity | NPI record | Review before dropping |
| Call outcome `corporate` | The call log (section 3) | Add the brand or parent to the screen; drop its other locations |

A location count alone misses groups that keep the original practice name, so the report names the signals used and the brands found.

## 2. Situation segments

A local list becomes a campaign when each segment has one reason to write. Build segments from fields the pull already holds, so they cost nothing extra.

The rating, review-count and date cutoffs below are settings the user picks for the offer; the values shown are the ones the worked example used.

| Segment tag | Rule | Offer it fits |
|-|-|-|
| `named_contact` | `contact_name` present and the email is a person's address | Any offer; first-name copy; send first |
| `role_inbox` | `is_role = true` | Any offer; copy addressed to the business, not a person |
| `low_rating` | Rating 3.9 or lower with 10 or more reviews | Reputation management, review response, customer service training |
| `few_reviews` | Under 20 reviews | Review generation, local SEO |
| `high_rated_busy` | Rating 4.6 or higher with 200 or more reviews | Capacity offers: scheduling, hiring, second location, financing |
| `new_license` | Original licensure date in the last 12 months (license file match) | Websites, insurance, bookkeeping, equipment, marketing setup |
| `no_website` | Phone and address, no website (phone file only) | Website builds and local listings, by phone or mail |
| `multi_location` | Same domain on 2 or more locations | One-to-many offers; contact the owner or office manager once |

A row can carry two tags (`named_contact;low_rating`). The send order for a first campaign: `named_contact` in the segment that matches the offer, then `role_inbox` in the same segment, then the rest. Every tag's rule and count goes in the report so the next pull can repeat it.

Segment copy names the outcome the offer produces ("more 5-star reviews from the patients you already see") rather than quoting the rating back.

## 3. Call file and call outcomes

The phone file (`-phone-only.csv`, plus the phones on the main file when the user calls) gets one outcome per dial attempt that reached a result:

| Outcome | Meaning | List action |
|-|-|-|
| `owner_reached` | Spoke with the owner or the named contact | Keep; log the result in the CRM |
| `gatekeeper` | Front desk or staff; owner not available | Keep; record the owner's name if given, retry another day |
| `referred` | Given another name or a better number | Add the name to `contact_name`, the number to `phone_alt`, source `call_note` |
| `wrong_number` | Number is not this business | Blank the phone; re-pull the business from Maps by name |
| `closed` | Business closed or number disconnected | Remove from every file; add to suppression |
| `corporate` | Staff say a group, DSO or head office decides | Add the parent to the independence screen (section 1c); drop its other locations |
| `not_interested` | Heard the offer, declined | Suppress for the cool-off window the user sets |
| `remove_request` | Asked not to be contacted | Suppress permanently, every channel, same day |

Compare outcome shares across sub-areas and titles once each has enough reached results for the team to trust the rate:

| Signal | Fix |
|-|-|
| One sub-area's `wrong_number` plus `closed` share is well above the rest of the list | The data there is stale: re-pull that sub-area from Maps and compare `pulled_at` |
| One `contact_title` draws most of the `referred` outcomes | The Website Finder title is wrong for this vertical; move the referred-to title to slot 1 in the title ladder |
| `gatekeeper` is the most common outcome in a segment | Move that segment's call window by the connect rate per local hour, or switch the segment to email first |

## 4. Handoff to the sequencer and the dialer

### Sequencer import

| Sequencer field | Column | Rule |
|-|-|-|
| Email | `email` | Main file only; `email_status = valid` |
| First name | first token of `contact_name` with "Dr." and credentials removed | Blank when there is no named contact; the copy must read correctly with the greeting fallback |
| Greeting fallback | none | Write the opener so a blank first name reads "Hi there" or opens with the business name |
| Company | `business_name` | As listed; trim trailing location tags only if they break the sentence |
| City | `city` | Used in the subject or first line |
| Custom variable 1 | `segment` | Splits campaigns |
| Custom variable 2 | `rating`, `reviews` | For segment copy, not for quoting back |
| Campaign | one per segment and sub-area batch | Catch-all file in its own campaign |

Load `named_contact` rows first. Keep the catch-all file in a separate campaign that starts only after the main file's first 200 sends show hard bounces under 2% (Alex Berman's 2% line, Instantly's 200-send window, as in `references/deliverability-primer.md`).

### Dialer import

| Dialer field | Column |
|-|-|
| Phone | `phone` (E.164) |
| Account name | `business_name` |
| Contact | `contact_name` or blank |
| Local time zone | from `state` and `postal_code` (Arizona stays on Mountain Standard Time all year) |
| Notes | `segment`, `rating`, `reviews` |
| Outcome field | the outcome list in section 3, set up before the first call block |

Call windows are a team setting in each business's local time. Log connect rate by local hour per vertical from the first call blocks and move the window to the hours that connect best.

## 5. Refresh

| Job | Cadence | How |
|-|-|-|
| New businesses in the same search | User sets; before each new campaign at the least | Same database call with `excludeDelivered: true` |
| Re-validate before a new campaign on this list | When `email_validated_at` is older than 90 days (ZeroBounce recommends verifying at least once per quarter) | Email Validator on the rows to be sent |
| Phone, website, open or closed | When the outcome log shows `wrong_number` or `closed` rising in a sub-area | Database re-pull for owned records is free; Maps for scraped rows |
| New license or NPI records | User sets; CMS publishes a weekly incremental NPI file | Weekly NPI incremental file or the license board file; new matches go to `new_license` |

## Sources

- CMS, NPPES NPI Registry API (queried 2026-10-13): https://npiregistry.cms.hhs.gov/api-page
- CMS, NPPES downloadable files (monthly full file, weekly incremental, checked 2026-10-13): https://download.cms.gov/nppes/NPI_Files.html
- Florida DBPR, Construction Industry public records downloads (checked 2026-10-13): https://www2.myfloridalicense.com/construction-industry/public-records/
- CMS, NPPES NPI Registry API paging test (`skip=1000` and `skip=1200` return the same first record, run 2026-10-13): https://npiregistry.cms.hhs.gov/api/
- Arizona Corporation Commission, eCorp entity search (search by entity name, statutory agent or principal name; checked 2026-10-13): https://ecorp.azcc.gov/EntitySearch/Index
- Topograph, Colorado business register documentation (officers and managers are not filed; registered agent only; checked 2026-10-13): https://docs.topograph.co/essentials/us-colorado
- Heartland Dental, Monthly Growth Spotlight, December 2025 (newly supported offices listed by practice name): https://blog.heartland.com/heartland-dental-monthly-growth-spotlight-december-2025
- Becker's Dental Review, "Florida dental practice leased to Heartland sells for $3M", Cameron Cortigiano, Oct 7 2025: https://www.beckersdental.com/dso-dpms/florida-dental-practice-leased-to-heartland-sells-for-3m/
- US Census Bureau, County Business Patterns: https://www.census.gov/programs-surveys/cbp.html
- ZeroBounce, How often should I verify my email list: https://zerobounce.net/docs/frequently-asked-questions/account/how-often-should-I-verify-my-email-list
- Alex Berman, cold email templates (bounces under 2%): https://alexberman.com/cold-email-templates
- Google, Email sender guidelines (bounce and spam rate limits that the catch-all rule protects): https://support.google.com/a/answer/81126
- ScraperCity tool catalog (Maps `url` input, Website Finder price): references/scrapercity-catalog.md
