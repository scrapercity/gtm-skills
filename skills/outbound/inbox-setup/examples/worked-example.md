# Mailbox Roster and Ramp: Fernhill Analytics

Illustrative example: Fernhill Analytics is fictional and every domain uses `.example`. Prepared 2026-10-15 from the sending plan dated 2026-10-13.

## Summary

Path: standard 21-day warmup, chosen over the soft start because the Microsoft tenant would be 20 days old on the soft-start date, inside its 10% quota window. 12 active and 6 reserve mailboxes, owned by three people, warm together from Monday 2026-10-19 and connect to Instantly by OAuth.

| Item | Value |
|-|-|
| Main domain (never sends cold email) | fernhill.example |
| Sequencer | Instantly Hypergrowth ($97 a month) |
| Active mailboxes | 12 on 4 domains (6 Google, 6 Microsoft) |
| Reserve mailboxes | 6 on 2 domains (3 Google, 3 Microsoft) |
| Warmup path | Standard, 21 days |
| First cold send | 2026-11-09 |
| Full volume date | 2026-11-27 |
| Steady-state cold sends a day | 360 (120 new prospects a day on a 3-step sequence) |

## Sender Identities

| Person | Title | Mailboxes owned | Reply backup |
|-|-|-|-|
| Dana Ortiz | Head of Sales | 6 (one per domain) | Lena Park |
| Sam Whitaker | Account Executive | 6 (one per domain) | Dana Ortiz |
| Lena Park | Account Executive | 6 (one per domain) | Sam Whitaker |

Address formats rotate by domain so no person repeats a pattern on neighboring domains: `first@`, `first.last@`, `firstl@`. Every display name is the owner's full name.

## Mailbox Roster

| Mailbox | Owner | Provider | Role | Group | Wave |
|-|-|-|-|-|-|
| dana@getfernhill.example | Dana Ortiz | Google Workspace | Active | A | Wave 1 |
| sam.whitaker@getfernhill.example | Sam Whitaker | Google Workspace | Active | A | Wave 1 |
| lenap@getfernhill.example | Lena Park | Google Workspace | Active | A | Wave 1 |
| dana.ortiz@tryfernhill.example | Dana Ortiz | Google Workspace | Active | A | Wave 1 |
| samw@tryfernhill.example | Sam Whitaker | Google Workspace | Active | A | Wave 1 |
| lena@tryfernhill.example | Lena Park | Google Workspace | Active | A | Wave 1 |
| danao@fernhillhq.example | Dana Ortiz | Google Workspace | Reserve | Reserve | Reserve |
| sam@fernhillhq.example | Sam Whitaker | Google Workspace | Reserve | Reserve | Reserve |
| lena.park@fernhillhq.example | Lena Park | Google Workspace | Reserve | Reserve | Reserve |
| dana@meetfernhill.example | Dana Ortiz | Microsoft 365 | Active | A | Wave 1 |
| sam.whitaker@meetfernhill.example | Sam Whitaker | Microsoft 365 | Active | A | Wave 1 |
| lenap@meetfernhill.example | Lena Park | Microsoft 365 | Active | A | Wave 1 |
| dana.ortiz@fernhillapp.example | Dana Ortiz | Microsoft 365 | Active | A | Wave 1 |
| samw@fernhillapp.example | Sam Whitaker | Microsoft 365 | Active | A | Wave 1 |
| lena@fernhillapp.example | Lena Park | Microsoft 365 | Active | A | Wave 1 |
| danao@usefernhill.example | Dana Ortiz | Microsoft 365 | Reserve | Reserve | Reserve |
| sam@usefernhill.example | Sam Whitaker | Microsoft 365 | Reserve | Reserve | Reserve |
| lena.park@usefernhill.example | Lena Park | Microsoft 365 | Reserve | Reserve | Reserve |

Group A runs two Instantly campaigns on the same 12 mailboxes, East (Eastern and Central prospects) and West (Mountain and Pacific); each account's daily limit caps the mailbox across both.

## Account Settings

| Setting | Google Workspace (one account, 9 users) | Microsoft 365 (one tenant, 9 users, created 2026-10-13) |
|-|-|-|
| Sign-in security | 2-Step Verification enforced on the "Cold email" organizational unit | MFA through security defaults |
| Sequencer connection | Instantly, Sign in with Google (OAuth); no app passwords | Instantly, Sign in with Microsoft (OAuth); SMTP AUTH left off, since Basic SMTP AUTH turns off by default after December 2026 |
| Volume guard | Instantly account daily limit and Campaign Slow Ramp | Outbound spam policy "Cold email" on all 9 users: 20 external recipients an hour (top of the 10 to 20 in Apollo, Email Sending Limits), 50 a day (Alex Berman's per-inbox ceiling), restrict until the following day, automatic forwarding Off; plus the Instantly account limit |
| Tenant-wide limit | None to plan for: paid Business Starter Flexible since 2026-10-13, no trial | External recipient quota by tenant age: 1,182 a day through 2026-11-12, 2,957 through 2026-12-12, 11,828 after (9 licenses) |
| Photo and recovery | Each owner's headshot; recovery email it-ops@fernhill.example | Headshot uploaded in the admin center; same recovery address |

DNS records on each sending domain (the main domain is untouched):

| Record | Google domains (getfernhill, tryfernhill, fernhillhq) | Microsoft domains (meetfernhill, fernhillapp, usefernhill) |
|-|-|-|
| MX | `smtp.google.com`, priority 1 | The value in Microsoft 365 admin center > Settings > Domains > DNS records |
| SPF (TXT on @) | `v=spf1 include:_spf.google.com ~all` | `v=spf1 include:spf.protection.outlook.com -all` |
| DKIM | TXT at `google._domainkey`, 2048-bit key generated in Admin console > Apps > Gmail > Authenticate email | CNAMEs `selector1._domainkey` and `selector2._domainkey`, targets copied from Defender > Email authentication settings > DKIM |
| DMARC (TXT on `_dmarc`) | `v=DMARC1; p=none; rua=mailto:dmarc@fernhill.example` | Same |
| Tracking | CNAME `inst` to `prox.itrackly.com` (unused while tracking is off) | Same |

## Signature Block

```text
Dana Ortiz
Head of Sales, Fernhill Analytics
Not the right person? Reply "no thanks" and I won't follow up.
```

Sam Whitaker and Lena Park use the same block with their own name and title ("Account Executive, Fernhill Analytics"). Set in: Instantly per-account signature for all 18 accounts, and matched in Gmail and Outlook on the web for manual replies. Plain text, no logo, no links.

## Warmup and Ramp Schedule

| Wave | Mailboxes | Warmup start | First cold send | Cold cap at full volume |
|-|-|-|-|-|
| Wave 1 | 12 active (getfernhill, tryfernhill, meetfernhill, fernhillapp) | 2026-10-19 | 2026-11-09 | 30 |
| Reserve | 6 reserve (fernhillhq, usefernhill) | 2026-10-19 | None until promoted | 0 |

| Dates | Row | Cold cap per mailbox | Warmup per day | Campaign daily limit | Gate to move on |
|-|-|-|-|-|-|
| 2026-10-19 to 2026-11-08 | Warmup only | 0 | 1 rising to 10 | 0 | On 2026-11-06: health score above 90% (Instantly readiness guide); header test shows spf=pass, dkim=pass, dmarc=pass; placement test lands in the inbox at Gmail and Microsoft |
| 2026-11-09 to 2026-11-13 | Slow ramp week 1 | 2 rising to 10 | 10 | 24 rising to 120 | Hard bounces under 2% (Alex Berman); spam rate under 0.1% where Postmaster Tools shows data (Google) |
| 2026-11-16 to 2026-11-20 | Slow ramp week 2 | 12 rising to 20 | 10 | 144 rising to 240 | Same |
| 2026-11-23 to 2026-11-27 | Slow ramp week 3 | 22 rising to 30 | 10 | 264 rising to 360 | Same |
| 2026-11-30 onward | Full volume | 30 | 10 | 360 (East 210, West 150) | Any raise above 30 runs as a test with its pass line written first, never above 50 |

The ramp is Instantly's Campaign Slow Ramp: 2 campaign emails on the first sending day, 2 more each sending day, 30 on the 15th, Monday to Friday.

| Date | Step | Done when |
|-|-|-|
| 2026-10-15 to 2026-10-16 | DNS records above on all 6 domains; 18 users created with photos, 2-Step Verification or MFA, recovery address | Every user signs in |
| 2026-10-16 | Register and verify all 6 domains in Google Postmaster Tools (TXT record) | Each domain shows Verified |
| 2026-10-19 | Header test from each domain; all 18 accounts connected to Instantly by OAuth; warmup on for all 18 | `dkim=pass` on every domain; Instantly shows warmup running |
| 2026-11-04 to 2026-11-05 | Pull and validate the week 1 list; load only `valid` rows into the East and West campaigns | Campaigns saved, not launched |
| 2026-11-06 | Gate check per mailbox; one Instantly Inbox Placement one-time test (Email Accounts > Deliverability Tests; two free tests per workspace) with touch 1 from one mailbox per domain | Passing mailboxes get daily campaign limit 30 with Slow Ramp on; a domain in spam at Gmail or Microsoft holds at 0 and is retested a week later |
| 2026-11-09 | First cold send, 2 per mailbox, 09:00 in each campaign's time zone | First replies in Unibox |

Tenant quota check: Microsoft tenant, 9 licenses, standard quota 500 x 9^0.7 + 9,500 = 11,828 external recipients a day. In slow ramp week 1 (inside the 10% window, 1,182 a day): at most 6 active x (10 cold + 10 warmup) + 3 reserve x 10 warmup = 150 a day, 12.7%. At full volume from 2026-11-27 (25% window, 2,957 a day): 6 x 40 + 3 x 10 = 270 a day, 9.1%. Both stay under the quota; the Exchange admin center's tenant outbound external recipients report is read every Monday.

Warmup settings entered in Instantly for all 18 accounts: warmup on, increase per day 1, daily warmup limit 10, reply rate 30% (Instantly's suggested values for new accounts), Disable slow warmup: off, weekdays only off. Account daily campaign limit 0 until 2026-11-09, then 30 with Campaign Slow Ramp on. Minimum wait time 3 minutes.

## Sending Rules

| Rule | Value | Source |
|-|-|-|
| Days | Monday to Friday | Fernhill's choice |
| Hours | 08:00 to 17:00 recipient local time. East runs 09:00 to 17:00 America/New_York, so Central recipients get mail 08:00 to 16:00. West runs 09:00 to 17:00 America/Denver, so Pacific recipients get mail 08:00 to 16:00 | Fernhill's choice |
| Gap between sends | Random 3 to 5 minutes per mailbox | Inside 60 to 300 seconds (Apollo, Email Sending Limits) |
| Max per hour per mailbox | 15 | Inside 10 to 20 an hour (Apollo, Email Sending Limits) |
| Max per day per mailbox | Ramp row, 30 at full volume, ceiling 50 | Instantly (30 per account); alexberman.com (under 50) |
| Time zone handling | Prospects split by company state into East and West before upload | Fernhill's choice |
| Tracking | Opens off, clicks off | Alex Berman: Apple Mail Privacy Protection distorts opens, and click tracking wraps every link in a redirect |

## Reply Monitoring

| Item | Value |
|-|-|
| Owner per rotation group | Group A: Dana Ortiz, backup Lena Park |
| Check times | 10:00 and 15:00 Central on sending days, plus 09:00 Monday for weekend replies (Fernhill's choice) |
| Positive reply response target | Fernhill's target: a human answer within 4 business hours, from the mailbox that received the reply; measured every Friday from Instantly reply timestamps |
| Opt-out handling | Any "no thanks", "remove me" or unsubscribe goes to the Instantly blocklist the same day; a domain-level block if the person asks for the company |
| Routing | Instantly Unibox for all 18 mailboxes. Sam Whitaker also gets copies of replies from his 3 Google mailboxes through a Gmail filter; his Microsoft mailboxes have forwarding off by policy, so he answers those in Unibox |

## Rotation and Retirement

| Action | Trigger | Steps | Back in service |
|-|-|-|-|
| Re-validate | Hard bounces 2% to 5% on a campaign after 200 sends (Alex Berman's warning zone) | Pause the campaign, re-validate its remaining rows, drop everything not valid | When the re-validated file is loaded |
| Pause | Hard bounces over 5% after 200 sends (Alex Berman's critical line; Instantly's default auto-pause); spam rate 0.3% on the domain (Google); provider sending disabled | Account daily campaign limit to 0, warmup stays on, log date and cause, promote a reserve mailbox on the same provider | Cause fixed and list re-validated; the slow ramp resumes from its last limit |
| Rest | Spam rate over 0.1% on the domain (Google's line) | All 3 mailboxes on the domain to cap 0 for 14 days (Fernhill's choice), warmup on | After the rest and an Instantly Inbox Placement test that reaches the inbox at Gmail and Microsoft |
| Retire | Domain relisted on the Spamhaus DBL after removal; a provider suspension that does not lift; owner leaves the company | Remove from Instantly, cancel the Google seat at the next Flexible billing date (Microsoft seats stay in warmup until the annual renewal), keep the domain registered and redirecting, export replies before deleting users | Not reused for cold email |

A mailbox with a health score under 90% (Instantly readiness guide) holds its cold cap until it recovers. Reserves on hand: 2 warmed domains (6 mailboxes, one domain per provider), 50% of the 4 active domains, the ratio Growth Engine X publishes. Reorder point: when a reserve is promoted, buy and set up one domain on the same provider that week (22 to 24 days to ready on the standard path).
