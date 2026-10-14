# Dialer Setup and Caller ID

How to set up numbers, the dialer and caller ID so more prospects pick up and call back.

## 1. Type every number

| Field from ScraperCity | Typical line | Type it as | Why it changes the plan |
|-|-|-|-|
| `phone` on a Local Business Database, Google Maps or Yelp record | Business main line, often the owner's cell for small trades | Main line, or mobile when the dialer's line type lookup says wireless | A wireless "main line" may be the owner's cell: dial it with the owner-mobile group |
| Lead Database phone fields | Switchboard or direct dial | Direct dial or switchboard | Switchboards route to voicemail or a gatekeeper; budget more attempts |
| `contact_mobile` (Local Business Database named contact) | Mobile | Owner mobile | Berman: mobiles connect far more often than main lines; dial first |
| `mobile_number` from `find_mobiles` | Mobile | Contact mobile | Same |
| Store Leads phone (`phones: true`) | Store support line or owner cell | Line type lookup decides | Support lines reach staff, not the owner |

Line type lookup: use the dialer's carrier or line type check. ScraperCity does not return line type, so its cost is a user input.

Dial order: owner or contact mobile, then direct dial, then main line; Berman's page says moving from switchboard to mobile can double the connect rate. Inside each group, records with a fresh trigger or a past connect go first, the way Reisert works Priority before Working (`references/call-blocks-and-metrics.md` section 4b).

## 2. Dial mode

| Mode | Use it for | Trade-off |
|-|-|-|
| Click-to-call, one line | Tier A accounts, mid-market titles | Fewest conversations per hour; the rep hears every pickup from the first word |
| One-line power dialer | Most SDR lists | Removes dialing time between calls without a pickup delay |
| Parallel dialer, several lines | Large local business lists where conversations per hour decide the result | A short delay at pickup costs some openers, and more dials per hour need more numbers to stay under the per-number cap below |

## 3. Dialer settings

| Setting | Value |
|-|-|
| Voicemail | Rep-left and specific to the record (V1 to V3 in the script library); a pre-recorded drop only on parallel lists, recorded per segment |
| Caller ID | Local numbers you own that ring back to the rep or a monitored line; callbacks book meetings |
| Dials per number | The plan's own cap, at or under the 75 calls per day per number that Readymode recommends (June 2, 2025), spread across the blocks. It is Readymode's recommendation in a blog post, not a limit of any dialer; enter the plan's cap in the named dialer's per-number setting |
| Numbers per rep | Planned dials per day / 75, rounded up, plus one registered backup; Readymode says to hold enough numbers to spread volume evenly |
| Removed numbers | The dialer reads the CRM's removed-numbers field before every dial; anyone who said "don't call" or "remove me" comes off every list the same day |
| Window | The sourced windows in `references/call-blocks-and-metrics.md` section 4 (Berman: 9 to 11am blocks, 4 to 5pm pickups, avoid 12 to 2pm); for local owners, the hours the front desk gives you (section 5) |
| Testing windows | Two windows per segment, the same sample size each; keep the one with the higher connect rate |
| Attempts per number | One a day per person at most (Kixie, June 2023), up to 5 over about two weeks (Berman); Cognism and WHAM found 93% of conversations by attempt 3 |
| Time zone | From the business address (`city`, `state`, `postal_code`), area code only as a fallback, since ported mobiles keep their old area code |

## 4. Caller ID reputation

Pickups collapse when the prospect's screen shows "Spam Likely" under your number. The labels come from carrier-side call analytics. Per Hiya (August 2023), the engines behind the three large US wireless carriers are Hiya (AT&T), TNS (Verizon) and First Orion (T-Mobile).

### 4a. Attestation

Carriers sign each call with an attestation level defined in the ATIS-1000074 standard:

| Level | Meaning | What to ask your dialer or carrier |
|-|-|-|
| A, full | Provider knows the customer and has verified the customer may use the calling number | Target for every outbound number |
| B, partial | Provider knows the customer but has not verified the number | Prove ownership of the number to the provider |
| C, gateway | Provider only knows where the call entered its network | Do not cold call through this route |

Attestation does not stop an analytics engine from labeling a number that behaves like spam (Hiya, 2023).

### 4b. Register, monitor, limit

| Step | Action | Source |
|-|-|-|
| Register | Submit every outbound number to the Free Caller Registry (freecallerregistry.com, run by First Orion, Hiya and TNS). It is free; you give business name and address, website, a contact with a verified email, call purpose and monthly volume, then up to 20 numbers or an upload file | freecallerregistry.com, checked 2026-10-13 |
| Expect no guarantee | Registration informs the engines; labels return if calling behavior looks like spam, and Hiya says re-registering numbers is not a fix | Hiya blog, August 2023 |
| Monitor | Test calls from each outbound number to an AT&T, a Verizon and a T-Mobile phone you control, on a schedule the plan sets; record what each screen shows. Track connect rate per number per day, since a sudden drop on one number is the first sign of a label | Readymode (June 2025) on monitoring caller ID reputation |
| Volume per number | At or under 75 calls a day, as Readymode recommends | Readymode, June 2025 |

### 4c. Fix the cause before swapping numbers

1. The engines label on calling behavior and user feedback (Hiya, 2023); new numbers dialing the same list the same way pick up the same label within days.
2. Callbacks from earlier voicemails go to the old number, so a swap loses the meetings those callbacks would book.

Label runbook:

| Step | Action |
|-|-|
| 1 | Stop dialing from the labeled number; finish the block on the backup |
| 2 | Find the cause: dials per number per day, calls outside the window, repeat calls to one person, very short calls |
| 3 | File a dispute with the analytics provider for each carrier showing the label |
| 4 | If calls are blocked outright, open a ticket with the dialer or carrier's blocking support contact |
| 5 | Resume on the original number at lower volume once test calls show no label |

## 5. Ready-to-dial record per number

| Field | Example |
|-|-|
| `phone_e164` | +12145550182 |
| `number_source` | local_db `phone` |
| `line_type` | wireless |
| `number_type` | owner mobile |
| `removed_checked_at` | 2026-10-16 |
| `recipient_tz` | America/Chicago |
| `window_local` | 09:00 to 11:00 and 16:00 to 17:00 Tue to Thu |
| `attempts_24h` | 0 |
| `attempts_total` | 1 |
| `ready_to_dial` | yes |

## Sources

- https://www.freecallerregistry.com/
- https://blog.hiya.com/dont-pay-a-vendor-to-register-your-phone-numbers-across-carriers-use-free-caller-registry
- https://www.cognism.com/cold-calling-report-2025
- https://belkins.io/blog/cold-calling-benchmarks
- https://readymode.com/avoid-being-flagged-as-spam-in-outbound-calls
- https://www.kixie.com/sales-blog/how-to-avoid-showing-up-as-scam-likely-in-outbound-sales/
- https://alexberman.com/cold-calling-techniques
