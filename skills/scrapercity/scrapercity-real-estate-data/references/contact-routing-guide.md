# Contact Routing Guide: Owners, Agents and Brokers

How to turn ScraperCity real estate results into outreach that reaches the right person, keeps the sending domain and phone numbers delivering, and stops when someone asks it to. Every rule below carries its operating reason. Where no published number exists, the rule names the outcome data that sets it.

## 1. Who is on the list decides the channel order

| Recipient | Where the contact came from | Channel order | Why |
|---|---|---|---|
| Homeowner in pre-foreclosure, foreclosure or auction | `scrape_distress_list` address, then `find_people` or `scrape_property_lookup` with owner contact | Mail, then manual calls to confirmed matches, then email to confirmed matches | Mail reaches every property address, including owners with no phone or email found; calls and emails go only where the match is confirmed (section 2) |
| Agent | `scrape_zillow_agents` profile | Email, then calls to the listed number | Agents publish these details on their profiles |
| Commercial or business broker | `scrape_crexi`, `scrape_bizbuysell` broker fields | Email and calls to the firm line | Dedupe brokers across listings first: one broker holds many listings, so one message can cover them all |
| Owner of a commercial property | `scrape_property_lookup` on the address | Mail to the owner entity first | Commercial owners are often LLCs; the person behind the LLC is unconfirmed until a reply |
| Asset manager for bank-owned property | Distress List `bankOwned` rows | The lender's REO contact, not the former owner | The lender is the seller of an REO property |

## 2. Match confidence for People Finder and owner contact

A People Finder search by address returns the person the data links to that address. That is not always the current owner.

| Class | Test | Use |
|---|---|---|
| Confirmed | Returned address equals the property address after normalization, and the returned name matches the owner name on the distress or lookup record | Mail, calls and email |
| Probable | Address matches, owner name unknown or a partial match (same surname) | Mail and one call; drop on "wrong person" |
| Unconfirmed | Address differs, or several people returned for one address | Mail to the property address only |

Normalize both addresses the same way before comparing: USPS abbreviations (St, Ave, Blvd), unit designators, ZIP to five digits (USPS Publication 28). Keep the class in a `match_class` column so every call list can be filtered on it.

## 3. One suppression list across every tool

| Column | Example |
|---|---|
| `contact_value` | Lowercase email, or phone in E.164 |
| `property_address` | Normalized, when the request was tied to a property |
| `reason` | unsubscribed, asked not to be contacted, wrong number, wrong person, hard bounce, spam complaint, sold, deceased |
| `source_channel` | mail reply, call, email reply, sender unsubscribe |
| `added_at` | UTC date |

Rules:

- Add a "stop" or "remove me" request the same day, in whatever channel it came, and sync the list into every dialer, sender and mail house before the next block or drop. A list kept in one tool lets another tool reach the same person again.
- A wrong-number or wrong-person reply suppresses that number or address for that property only, so the correct owner can still be reached by mail.
- Re-pulls (monthly distress lists, new lookups) are deduped against this list before any spend on contact data.

## 4. Message content

Offer what the user does: a purchase, a listing or a valuation, with the valuation range from Property Lookup when the letter quotes one. Say who is writing in the first lines of every letter, call and email.

## 5. Email to owners and agents

| Rule | Value | Source |
|---|---|---|
| Validate before sending | `validate_emails`, $0.0072 each | Catalog |
| One-click unsubscribe header on bulk mail, unsubscribes processed within 2 days | Required for bulk senders | Google Email sender guidelines; Yahoo Sender Hub |
| Spam complaint rate | Under 0.1%, never 0.3% or higher | Google sender guidelines FAQ |
| Personal addresses from People Finder | A separate campaign | Its bounce and complaint rates are read on their own, apart from agent and broker email |
| Hard bounces on a send | Pause above 2% | Hunter, Cold Email Guide (October 2023): bounces should not exceed 2% of emails sent |

## 6. Calls

| Rule | Reason |
|---|---|
| Manual dial, a live person, confirmed and probable matches only | Each call reaches the person it was meant for, and a wrong-number reply is caught on the first try |
| Check the suppression list before every call block | Lists change daily; a block built on Monday may hold Tuesday's "stop" |
| Record an outcome per attempt (connected, voicemail, wrong number, stop, callback) | The outcomes drive suppression and the next block |
| Cap attempts per number at the attempt after which your outcome data shows no further connects | Attempts past that point spend dialer time without connects |
| Check caller ID numbers for spam labels; swap a labeled number | Pickups collapse once a number is labeled |
| Move call blocks to the hours with the best connect rate in your own outcome data | Connect rates vary by market and owner type; your data beats a guess |

## 7. Reply triage

| Reply contains | Route |
|---|---|
| "stop", "remove", "not interested, don't contact me" | Suppress (section 3), confirm once, no further contact |
| "wrong number", "I don't own that" | Suppress that number for that property; keep mailing the property |
| Any threat or complaint | Suppress across every channel and hand it to a person on the team the same day |
| A question or a price | A person on the team answers it |

## 8. Contact Hygiene table for a plan

Every plan carries one row per channel:

| Channel | Recipients | Rule | Operating reason |
|---|---|---|---|
| Direct mail | All owners in the buy box | Purchase offer; suppression list applied before each drop | Reaches every address, including owners with no phone or email found |
| Manual calls | Confirmed and probable matches | Suppression list checked before each block; attempts capped from outcome data; outcomes logged | Dials reach the owner; labeled caller IDs swapped |
| Email | Agents, confirmed owner matches | Validated; one-click unsubscribe; removals within 2 days | Inbox placement and complaint rate |

## Sources

- https://pe.usps.com/text/pub28/welcome.htm
- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- Hunter, Cold Email Guide, Email bounce rate (October 10, 2023): https://hunter.io/cold-email-guide/email-bounce-rate
- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/pricing
