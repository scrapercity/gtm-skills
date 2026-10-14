# Warmup and Ramp Schedules

How a new mailbox goes from zero to its full cold email cap, with the settings to enter in each sequencer and the gates between steps. Vendor defaults were read from each help center on 2026-10-12 and 2026-10-13. Every number below names its source; the rest are inputs the user sets.

## 1. What warmup is and what it is for

A new mailbox on a new domain has no sending history. Spamhaus says unknown domain reputations start as poor by default. Warmup builds history at low volume before cold sends begin.

Two kinds:

| Kind | How it works | Strength | Limit |
|-|-|-|-|
| Pool warmup (sequencer feature) | The sequencer exchanges messages between your mailbox and other participating mailboxes, opens them, replies to a share, and pulls them out of spam | Automatic, starts on day 1, gives volume to a mailbox with no contacts | M3AAWG's Sender BCP v4.0 does not recommend artificial warming. Pool engagement is not prospect engagement. |
| Manual warmup | The owner sends one-to-one mail from the new mailbox to colleagues, partners, customers who expect it | Engagement from people who know the sender | Slow, needs a person every day |

Pool warmup goes on the day the mailbox passes its header test. Cold sends start on day 22 on the standard path and no earlier than day 15 on the soft start.

## 2. The ramp per mailbox: standard and soft start

Two paths. The user picks one per wave.

| Path | Warmup before cold mail | Source |
|-|-|-|
| Standard | 21 days | Instantly gives its own AirMail accounts 3 weeks of warmup; Alex Berman warms for 2 to 4 weeks |
| Soft start | 14 days, never shorter | Instantly's minimum of 2 weeks; gates below |

Cold sends then follow Instantly's Campaign Slow Ramp: 2 campaign emails on the first day, 2 more each day, 30 on day 15. The ramp remembers its last limit when sending stops, so this file counts sending days.

| Period | Cold a day per mailbox | Pool warmup a day | Gate to move on |
|-|-|-|-|
| Warmup days 1 to 14 | 0 | Ramps 1 to 10 (+1 a day, Instantly's suggested values); soft start raises the limit to 20 at the mid-warmup check if every account is above 90% (top of Smartlead's 10 to 20 while campaigns run) | Health score above 90% (Instantly readiness guide); header test passes SPF, DKIM, DMARC |
| Warmup days 15 to 21 | 0 on the standard path; soft start begins its sending day 1 | 10 (20 on the soft start) | Before the first cold send on either path: an inbox placement test lands in the inbox at Gmail and Microsoft (Instantly Inbox Placement, two free one-time tests). Soft start also: a send file of `valid` addresses only. A domain that misses a gate stays on the standard dates |
| Sending days 1 to 14 | 2 on day 1, +2 each sending day (28 on day 14) | 10 | Hard bounces under 2% (Alex Berman); spam rate under 0.1% where Postmaster Tools shows data (Google) |
| Sending day 15 onward | 30 (Instantly's recommended campaign emails per account a day) | 10 | A raise above 30 only through the escalation test in section 8, never above 50 (Alex Berman) |

A gate that fails holds the mailbox at its current cap until the cause is found and fixed. A mailbox that keeps failing goes to `email-deliverability` for diagnosis.

Alex Berman starts new domains at 10 to 20 a day; the slow ramp starts lower and passes 10 on sending day 5. Google's Gmail sender guidance, written for resuming after a deferral, calls daily increases of 25% to 100% common; the slow ramp's largest daily step is 100% (2 to 4) and every later step is smaller.

### Waves

Mailboxes that start warmup on the same day form a wave and share one row of dates in the roster, so the roster does not repeat four dates on every line. A mailbox that fails a gate leaves its wave and gets its own dates in a note under the wave table.

### Microsoft 365 tenant quota during the ramp

Microsoft caps each tenant's external recipients a day at 500 x (purchased email licenses ^ 0.7) + 9,500, cut to 10% for a tenant's first 30 days and 25% to day 60 (Message Center MC1454397; trial tenants 500). Warmup mail to other participants counts. Check before each ramp step:

```text
tenant_daily_use = mailboxes_in_tenant x (cold cap + warmup a day)
pass if tenant_daily_use is under the tenant's quota at its age on that date
```

Over the quota, Microsoft blocks external mail until the 24-hour window clears. Worked: a 9-license tenant has a standard quota of 500 x 9^0.7 + 9,500 = 11,828, so 1,182 a day in its first 30 days. At 30 cold plus 10 warmup, 9 mailboxes use 360 a day, 30% of the cut quota. A 25-mailbox high-density tenant at 10 cold plus 10 warmup uses 500 a day against a cut quota of 500 x 25^0.7 + 9,500 = 14,259, so 1,425: 35%; with warmup raised to 40 a day it would use 1,250, 88%, and one more mailbox or a busy day puts it over.

## 3. Sources for the numbers

| Number | Source |
|-|-|
| 14-day minimum warmup, 21-day standard | Instantly: account ready after at least 2 weeks of warmup and a health score above 90%, 3 weeks for AirMail accounts (checked 2026-10-13) |
| Slow ramp: 2 on day 1, +2 a day, 30 on day 15 | Instantly, Campaign slow ramp (checked 2026-10-13) |
| 30 campaign emails a day per account | Instantly, Account and campaign limits, for non-AirMail accounts |
| New-tenant quota of 10% then 25% | Microsoft 365 Message Center MC1454397, rollout mid-September to end of November 2026 |
| Warmup +1 a day to a limit of 10, reply rate 30% | Instantly suggested values for newly created accounts |
| Keep warmup at 10 to 20 a day while campaigns run, reply rate 20 to 30% | Smartlead help center |
| 10 to 20 a day at the start, 2 to 4 weeks | alexberman.com, cold email templates page |
| Under 50 a day per inbox | alexberman.com, TAM strategy breakdown |
| Bounces above 2% hurt reputation; above 5% critical | alexberman.com, custom tracking domain guide (May 11, 2026) |
| 50 to 100 a day, 10 to 20 an hour, 60 to 300 seconds apart | Apollo knowledge base |
| Spam rate below 0.1%; daily increases of 25% to 100% are common | Google, Top 10 Gmail sender issues |
| About six weeks average warm-up | M3AAWG Sender BCP v4.0, written for permission mail |

## 4. Settings to enter, per sequencer

### Instantly (checked 2026-10-13)

| Setting | Where | Value for a new mailbox | Value once cold sends start |
|-|-|-|-|
| Warmup | Email Accounts > account > Warmup | On | On |
| Increase per day | Warmup settings | 1 | 1 |
| Daily warmup limit | Warmup settings | 10 | 10 |
| Reply rate % | Warmup settings | 30 | 30 |
| Disable slow warmup | Warmup settings | Off. Instantly: only for already-warmed accounts, never for new ones. Write the setting by this exact name in the roster, never "slow warmup on" | Off |
| Weekdays only | Warmup settings | Team choice | Team choice |
| Warm custom tracking domain | Warmup settings | On if tracking domain is set | On |
| Daily Campaign limit | Account > Settings | 0 until the wave's first cold send (day 22 standard, day 15 soft start) | 30, or the user's cap up to 50 |
| Minimum wait time | Account > Settings | Default 1 minute | Inside Apollo's 60 to 300 seconds |
| Campaign Slow Ramp | Campaign > Options | n/a | On: 2 on the first day, +2 a day until the account limit |
| Campaign daily limit | Campaign > Schedule & Limits | n/a | Active mailboxes x 30 (Instantly's formula) |

### Smartlead (checked 2026-10-12)

| Setting | Value |
|-|-|
| Warmup on, Total daily emails | 10 to 20 while campaigns run |
| Daily Ramp up | On for a fresh domain, enabled at the same time warmup starts (enabling later does not work as intended) |
| Reply Rate | 20 to 30% |
| Per-account max emails per day | 0 until the wave's first cold send, then the same 2-a-day ramp entered by hand, to 30 |
| Time gap between emails | Inside Apollo's 60 to 300 seconds |

### Lemlist, EmailBison, ManyReach, Apollo, HubSpot

Lemlist (lemwarm is included on paid plans per its pricing page), EmailBison ("smart warm-up" on its pricing page) and ManyReach (warmup included on the Business plan) each run their own warmup. Enter the same ramp into each tool's per-mailbox daily limit. Apollo has a per-mailbox ramp-up feature and uses the lower of the ramp-up limit and your configured limit. HubSpot sequences have no warmup; connect mailboxes that are already warmed elsewhere and cap HubSpot per user (Professional seats 500 sequence emails a day, Enterprise 1,000, both far above 30).

## 5. Sending window and pacing

| Rule | Value | Source |
|-|-|-|
| Days and hours | The user's choice, set in the recipient's local time | User |
| Gap between sends from one mailbox | Random, 60 to 300 seconds | Apollo knowledge base |
| Max per hour per mailbox | 10 to 20 | Apollo knowledge base |
| Max per day per mailbox | Ramp row, 30 at full volume, ceiling 50 | Instantly; Alex Berman |
| Time zone split | One campaign per time zone group, or the sequencer's per-lead time zone setting | Keeps the chosen window in each recipient's local time |

Capacity check: a 9-hour window at an average 3-minute gap allows about 180 sends per mailbox; a cap of 30 uses a sixth of it, so sends spread through the day.

## 6. Ramp calendar example (warmup starts Monday 2026-10-19, Monday-to-Friday sending)

| Date range | Standard: cold cap | Soft start: cold cap | Warmup |
|-|-|-|-|
| 2026-10-19 to 2026-11-01 | 0 | 0 | 1 rising to 10 |
| 2026-11-02 to 2026-11-06 | 0 | 2 rising to 10 | 10 |
| 2026-11-09 to 2026-11-13 | 2 rising to 10 | 12 rising to 20 | 10 |
| 2026-11-16 to 2026-11-20 | 12 rising to 20 | 22 rising to 30 (30 on 2026-11-20) | 10 |
| 2026-11-23 to 2026-11-27 | 22 rising to 30 (30 on 2026-11-27) | 30 | 10 |
| 2026-11-30 onward | 30 | 30 | 10 |

## 7. Re-warming a paused mailbox

Re-warming is for a mailbox whose cause was found and fixed. Warmup stays on during a pause. When the mailbox returns, Instantly's slow ramp resumes from the last limit it used; the user decides whether to restart lower. A mailbox that meets the burned test in section 9 is retired, not re-warmed.

## 8. Volume escalation test (any raise above 30)

Instantly recommends 30; Alex Berman's ceiling is 50. A raise between them is a test the user defines before it runs:

| Step | What | Pass line |
|-|-|-|
| 1. Baseline | Positive replies per 1,000 sends and hard bounces for the mailboxes being raised, over a period the user sets | Recorded |
| 2. Placement test before | Seed test from one of the mailboxes, live touch 1 copy, protocol in `email-deliverability` | Recorded by provider |
| 3. Raise | One step up per mailbox, campaign daily limit raised to match; Google warns against sudden spikes such as doubling | Bounces stay under 2% (Alex Berman) |
| 4. Placement test after | Same seeds, same copy | No provider moved from inbox to spam |
| 5. Reply check | Positive replies per 1,000 sends over the same number of sends as the baseline | The user's pass line, written before the raise |
| 6. Decide | All passed: keep the new cap. Any step failed: return to the previous cap the same day | Logged in the roster |

Positive replies, not total replies: an increase in "remove me" replies after a raise counts against it. Small samples are noisy; with too few sends to compare, keep the current cap.

## 9. Burned mailboxes are not reliably recoverable: retire and replace

The provider and blocklist pages cited here describe no recovery path that returns a burned sending identity to its old placement on a schedule you can plan around. The nearest is Google's FAQ: a bulk sender over 0.3% spam rate gets no mitigation until it has 7 consecutive days under that line. Plan as if a burned mailbox stays burned.

Burned test (any one):

| Signal | Threshold |
|-|-|
| Placement | Still in spam at seed providers after the `email-deliverability` spam-folder runbook fixed list, copy and authentication |
| Blocklist | The domain is relisted on the Spamhaus DBL after a removal |
| Provider | A suspension that the provider does not lift |

What to do:

1. Set the mailbox's campaign limit to 0 the same day. In-flight leads follow the lead pinning rule in `references/rotation-and-retirement.md` section 2.
2. Promote a warmed reserve from the same rotation group's reserve list. Do not move the burned mailbox's leads to a brand-new mailbox mid-thread.
3. Retire with the steps in `references/rotation-and-retirement.md` section 4: seat cancelled at the next billing date, domain kept registered and redirecting.
4. Order one replacement domain once the burn's cause is found. Replace one for one. A new batch every time a domain burns carries the same cause onto fresh domains, and spreading volume across many fresh domains to stay ahead of filters is what Spamhaus calls snowshoeing.
5. Write the cause in the roster. A burn without a found cause means the next mailbox burns the same way.

A reserve mailbox already in warmup is ready the day it is promoted; a new one on a new domain needs setup plus 21 days of warmup on the standard path.

## Sources

- Instantly, Warmup settings (suggested 10 and 30% for new accounts; "Disable slow warmup" only for already-warmed accounts; checked 2026-10-13): https://help.instantly.ai/en/articles/7988514-warmup-settings
- Instantly, Inbox Placement feature (Gmail and Microsoft; two free one-time tests; checked 2026-10-13): https://help.instantly.ai/articles/10147177-inbox-placement-feature
- Instantly, Inbox Placement one-time tests (Email Accounts > Deliverability Tests; checked 2026-10-13): https://help.instantly.ai/en/articles/10258203-inbox-placement-one-time-tests
- Instantly, How to change the warmup settings: https://help.instantly.ai/en/articles/9214348-how-to-change-the-warmup-settings
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, Account and campaign limits: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Instantly, Campaign slow ramp (checked 2026-10-13): https://help.instantly.ai/en/articles/10056946-campaign-slow-ramp-system
- Smartlead, How to enable email account warm ups: https://helpcenter.smartlead.ai/en/articles/52-how-to-enable-ai-email-account-warm-ups
- Smartlead, Daily ramp up: https://helpcenter.smartlead.ai/en/articles/164-understanding-the-daily-ramp-up-feature-in-smartlead-s-email-warm-up
- Apollo, Configure email sending limits: https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- HubSpot, Sales email send limits: https://knowledge.hubspot.com/connected-email/sales-email-send-limits
- Lemlist, Pricing: https://www.lemlist.com/pricing
- EmailBison, Pricing: https://emailbison.com/pricing
- ManyReach, Pricing: https://manyreach.com/pricing
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Top 10 Gmail sender issues (spam rate below 0.1%, common daily increase of 25% to 100%; checked 2026-10-13): https://support.google.com/mail/answer/15256272
- M3AAWG, Sender Best Common Practices v4.0: https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
- Spamhaus, Domain Blocklist: https://www.spamhaus.org/blocklists/domain-blocklist/
- Alex Berman, cold email templates: https://alexberman.com/cold-email-templates
- Alex Berman, TAM strategy breakdown: https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Alex Berman, custom tracking domains and Gmail (bounce lines, May 11, 2026): https://alexberman.com/custom-tracking-domain-gmail
- Google, Email sender guidelines FAQ (spam rate mitigation): https://support.google.com/a/answer/14229414
- Microsoft 365 Message Center MC1454397, TERRL quotas for new, trial and education tenants (mirror, checked 2026-10-13): https://mc.merill.net/message/MC1454397
