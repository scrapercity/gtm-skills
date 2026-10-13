# Warmup and Ramp Schedules

How a new mailbox goes from zero to its full cold email cap, with the settings to enter in each sequencer and the gates between steps. Vendor defaults were read from each help center on 2026-10-12. House numbers are ScraperCity operating defaults to test against your own data.

## 1. What warmup is and what it is for

A new mailbox on a new domain has no sending history. Spamhaus says unknown domain reputations start as poor by default. Warmup builds history at low volume before cold sends begin.

Two kinds:

| Kind | How it works | Strength | Limit |
|-|-|-|-|
| Pool warmup (sequencer feature) | The sequencer exchanges messages between your mailbox and other participating mailboxes, opens them, replies to a share, and pulls them out of spam | Automatic, starts on day 1, gives volume to a mailbox with no contacts | M3AAWG's Sender BCP v4.0 does not recommend artificial warming. Pool engagement is not prospect engagement. |
| Manual warmup | The owner sends real one-to-one mail from the new mailbox to colleagues, partners, customers who expect it | Real engagement | Slow, needs a person every day |

House standard: pool warmup on from day 1, plus 5 to 10 real messages from the owner in week 1 (reply to a vendor, send a calendar invite to a colleague). Cold sends start no earlier than day 15.

## 2. The house ramp (per mailbox)

| Days since warmup started | Pool warmup a day | Cold sends a day | Gate to move to the next row |
|-|-|-|-|
| 1 to 14 | Ramps 1 to 10 (+1 a day) | 0 | Sequencer health score above 90% over 7 days (Instantly's readiness rule); header test passes SPF, DKIM, DMARC |
| 15 to 21 | 10 | 10 | Hard bounces under 2% across the mailbox's cold sends; no complaint on the domain in Postmaster Tools if data shows |
| 22 to 28 | 10 | 20 | Same, plus at least 1 human reply across the domain's mailboxes |
| 29 to 42 | 10 | 30 | Same |
| 43 onward | 10 | 30, up to 50 | Raise by 5 a week only after 14 days with bounces under 1%, complaints under 0.1%, reply rate steady |

A gate that fails holds the mailbox on its current row for another 7 days. Two failed gates in a row send the mailbox to `email-deliverability` for diagnosis.

Weekly ramp increase is 100% (10 to 20) once and 50% (20 to 30) once. M3AAWG flags volume jumps above 40% as a monitoring signal for permission mail; the cold ramp starts from such small numbers that the absolute jump is 10 messages a day.

## 3. Sources for the numbers

| Number | Source |
|-|-|
| 14-day minimum warmup | Instantly: account ready after at least 2 weeks of warmup and a health score above 90% (3 weeks for AirMail accounts) |
| Warmup +1 a day to a limit of 10, reply rate 30% | Instantly suggested values for newly created accounts |
| Keep warmup at 10 to 20 a day while campaigns run, reply rate 20 to 30% | Smartlead help center |
| 10 to 20 a day at the start, 2 to 4 weeks | alexberman.com, cold email templates page |
| Under 50 a day per inbox | alexberman.com, TAM strategy breakdown |
| 30 campaign emails a day per account | Instantly's account and campaign limits article recommends 30 for non-AirMail accounts |
| 50 to 100 a day, 10 to 20 an hour, 60 to 300 seconds apart | Apollo knowledge base (looser than this repo) |
| About six weeks average warm-up | M3AAWG Sender BCP v4.0, written for permission mail |
| Avoid sudden spikes such as doubling volume | Google Email sender guidelines |

## 4. Settings to enter, per sequencer

### Instantly (checked 2026-10-12)

| Setting | Where | Value for a new mailbox | Value once cold sends start |
|-|-|-|-|
| Warmup | Email Accounts > account > Warmup | On | On |
| Increase per day | Warmup settings | 1 | 1 |
| Daily warmup limit | Warmup settings | 10 | 10 |
| Reply rate % | Warmup settings | 30 | 30 |
| Disable slow warmup | Warmup settings | Off (only for already-warmed accounts) | Off |
| Weekdays only | Warmup settings | Off for the first 14 days (house standard: daily history), then team choice | Team choice |
| Warm custom tracking domain | Warmup settings | On if tracking domain is set | On |
| Daily Campaign limit | Account > Settings | 0 until day 15 | 10, 20, 30 by ramp row |
| Minimum wait time | Account > Settings | Default 1 minute | 3 minutes (house standard) |
| Campaign Slow Ramp | Campaign > Options | n/a | On: Instantly adds 2 campaign emails a day until the account limit |
| Campaign daily limit | Campaign > Schedule & Limits | n/a | Active mailboxes x current per-mailbox cap |

### Smartlead (checked 2026-10-12)

| Setting | Value |
|-|-|
| Warmup on, Total daily emails | 10 to 20 while campaigns run |
| Daily Ramp up | On for a fresh domain, enabled at the same time warmup starts (enabling later does not work as intended) |
| Reply Rate | 20 to 30% |
| Per-account max emails per day | 0 until day 15, then by ramp row |
| Time gap between emails | 3 to 6 minutes (house standard) |

### Lemlist, EmailBison, ManyReach, Apollo, HubSpot

Lemlist (lemwarm is included on paid plans per its pricing page), EmailBison ("smart warm-up" on its pricing page) and ManyReach (warmup included on the Business plan) each run their own warmup. Enter the house ramp numbers into each tool's per-mailbox daily limit. Apollo has a per-mailbox ramp-up feature and uses the lower of the ramp-up limit and your configured limit. HubSpot sequences have no warmup; connect mailboxes that are already warmed elsewhere and cap HubSpot per user (Professional seats 500 sequence emails a day, Enterprise 1,000, both far above this repo's caps).

## 5. Sending window and pacing

| Rule | Value (house standard) | Reason |
|-|-|-|
| Days | Monday to Friday | B2B buyers read work mail on workdays |
| Hours | 8:00 to 17:00 recipient local time | Mail arrives during the working day |
| Gap between sends from one mailbox | Random 2 to 6 minutes | Avoids bursts; Apollo recommends 60 to 300 seconds |
| Max per hour per mailbox | 15 | Apollo recommends 10 to 20 an hour |
| Max per day per mailbox | Ramp row, ceiling 50 | Section 2 |
| Time zone split | One campaign per time zone group, or the sequencer's per-lead time zone setting | Keeps the window honest across US zones |

Capacity check: a 9-hour window at an average 4-minute gap allows about 135 sends per mailbox; a cap of 30 uses under a quarter of it, so sends spread through the day without crowding the morning.

## 6. Ramp calendar example (mailbox created Thursday 2026-10-15)

| Date range | Row | Cold cap | Warmup |
|-|-|-|-|
| 2026-10-15 to 2026-10-28 | Warmup only | 0 | 1 rising to 10 |
| 2026-10-29 to 2026-11-04 | Ramp 1 | 10 | 10 |
| 2026-11-05 to 2026-11-11 | Ramp 2 | 20 | 10 |
| 2026-11-12 to 2026-11-25 | Ramp 3 | 30 | 10 |
| 2026-11-26 onward | Steady | 30, review for 35 on 2026-12-10 | 10 |

## 7. Re-warming a paused mailbox

| Pause length | Restart at |
|-|-|
| Under 7 days, paused for a list problem | Previous cap |
| 7 to 30 days | Ramp row 1 (10 a day), warmup stayed on |
| Over 30 days or after a blocklisting or provider suspension | Full ramp from day 1, after `email-deliverability` clears it |

## Sources

- Instantly, Warmup settings: https://help.instantly.ai/en/articles/7988514-warmup-settings
- Instantly, How to change the warmup settings: https://help.instantly.ai/en/articles/9214348-how-to-change-the-warmup-settings
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, Account and campaign limits: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Smartlead, How to enable email account warm ups: https://helpcenter.smartlead.ai/en/articles/52-how-to-enable-ai-email-account-warm-ups
- Smartlead, Daily ramp up: https://helpcenter.smartlead.ai/en/articles/164-understanding-the-daily-ramp-up-feature-in-smartlead-s-email-warm-up
- Apollo, Configure email sending limits: https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- HubSpot, Sales email send limits: https://knowledge.hubspot.com/connected-email/sales-email-send-limits
- Lemlist, Pricing: https://www.lemlist.com/pricing
- EmailBison, Pricing: https://emailbison.com/pricing
- ManyReach, Pricing: https://manyreach.com/pricing
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- M3AAWG, Sender Best Common Practices v4.0: https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
- Spamhaus, Domain Blocklist: https://www.spamhaus.org/blocklists/domain-blocklist/
- Alex Berman, cold email templates: https://alexberman.com/cold-email-templates
- Alex Berman, TAM strategy breakdown: https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
