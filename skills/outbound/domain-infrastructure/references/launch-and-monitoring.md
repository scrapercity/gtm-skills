# Launch Timing and Monitoring

Two parts of a sending plan that decide whether a team trusts it: the date of the first cold email, written honestly, and the monitoring that tells the team a domain is in trouble before replies stop. Facts were checked on 2026-10-13 against the sources at the end.

## 1. Why new infrastructure cannot start on the day it is bought

| Fact | Source |
|-|-|
| Unknown domain reputations start as poor; only time and clean sending improve them | Spamhaus Domain Blocklist page |
| An account is ready for campaigns after at least 2 weeks of warmup and a health score above 90%; Instantly's own AirMail accounts need 3 weeks | Instantly help center, checked 2026-10-13 |
| New domains: "Start with 10-20 emails per day and ramp up over 2-4 weeks" | alexberman.com, cold email templates, checked 2026-10-13 |
| Warmup settings for newly created accounts: increase per day 1, daily warmup limit 10, reply rate 30; "Stick to 10 warmup emails per day for new accounts" | Instantly help center, warmup settings and how warmup works, checked 2026-10-13 |
| About six weeks is an average warm-up period for permission mail | M3AAWG Sender BCP v4.0 (Aug 2026) |
| New Microsoft 365 tenants get 10% of the standard Tenant External Recipient Rate Limit for their first 30 days and 25% for days 31 to 60; trial tenants drop to 500 external recipients a day. Rollout runs mid-September to end of November 2026 | Microsoft 365 Message Center MC1454397 (updated 2026-09-29) |
| Google Workspace trial accounts are capped at 500 messages a day per user, and paid limits can take up to 75 days to rise after the account has paid $100 | Google Workspace, Gmail sending limits |

## 2. Three launch paths

Every plan shows the standard and soft-start paths; when the standard path reaches the target after the requested date it also shows the wide build, and the user picks on day 0. Day 0 is the plan date. Warmup starts the day the header test passes (Google's DKIM key appears 24 to 72 hours after Gmail is turned on, so usually day 2).

Warmup settings for every mailbox, one value each (Instantly's suggested values for new accounts): increase 1 a day, daily warmup limit 10, reply rate 30%, left on at those values once cold mail starts. Campaign daily limit 0 until the first cold day.

Cold ramp: 10 a mailbox on sending days 1 to 5, 20 on days 6 to 10, the cap (30, Instantly) from day 11. The start is the low end of Alex Berman's 10 to 20 for new domains and the cap is reached in 2 weeks, the short end of his 2 to 4. Every mailbox, reserves included, sends during the ramp; reserves go back to warmup only once the active mailboxes are at the cap. A raise waits for the weekly review to pass (section 6).

| Path | Warmup before cold mail | Cold sends per mailbox | Source |
|-|-|-|-|
| Standard | 21 days | The ramp above | 3 weeks is Instantly's warmup for its own new AirMail accounts and sits inside Alex Berman's 2 to 4 weeks |
| Soft start | 14 days, never shorter | The ramp above, 7 days earlier | Instantly's minimum of 2 weeks, the low end of Alex Berman's range; every mailbox shows an Instantly health score above 90% (Instantly's readiness rule), the header test passes, and the send file holds only `valid` addresses |
| Wide build | 21 days, or 14 on the soft start | `wide_cap` from the first cold day, no ramp | `wide_cap` is a number from Alex Berman's 10 to 20 for new domains; mailboxes = ceil(daily sends / wide_cap), with no reserve domains because every mailbox can rise to 30 to cover a paused domain |

A Microsoft 365 tenant runs on 10% of its standard quota for its first 30 days, warmup mail included, so a tenant created on day 0 is still in that window on the first cold day of every path. Check mailboxes x (cold cap + 10 warmup) per tenant against it.

What the soft start costs: one week less history before prospects see the mail. A mailbox that misses its gate on the soft path stays on warmup only and joins on the standard dates.

## 3. Writing the dates

```text
warmup_start        = day the header test passes for the last mailbox in the wave
first_cold_standard = warmup_start + 21 days
first_cold_soft     = warmup_start + 14 days
full_volume         = sending day 11, counting the first cold send as day 1
wide_full_volume    = the wide build's first cold day
slip_days           = full_volume - requested date   (write it when above 0)
```

Worked (plan date Tuesday 2026-10-13 = Day 0, request "1,500 a day starting in 3 weeks", so 2026-11-03; 60 mailboxes of which 50 active; wide build 100 mailboxes at 15; Monday-to-Friday sending):

| Line | Standard | Soft start | Wide build, 21-day warmup |
|-|-|-|-|
| Warmup start | 2026-10-15 | 2026-10-15 | 2026-10-15 |
| Sending day 1, 10 a mailbox on all 60 | 2026-11-05 (600 a day) | 2026-10-29 (600 a day) | 2026-11-05, 15 a mailbox on 100 (1,500 a day) |
| Sending day 6, 20 a mailbox on all 60 | 2026-11-12 (1,200 a day) | 2026-11-05 (1,200 a day) | |
| Sending day 11, 30 a mailbox on the 50 active | 2026-11-19 (1,500 a day) | 2026-11-12 (1,500 a day) | |
| Against the requested 2026-11-03 | First sends 2 days late; 1,500 a day 16 days late | First sends 5 days early; 1,500 a day 9 days late | 1,500 a day 2 days late; on the 14-day warmup, 2026-10-29, 5 days early |

Say in the summary which path meets the date and by how many days the others miss it. Never close the slip by skipping warmup or by moving the volume onto the main domain.

## 4. Vendor lead times

A plan that depends on a vendor delivering mailboxes inside a stated window has a single point of failure the team does not control:

- Put a vendor's delivery time in the plan only after the vendor confirms it in writing for this order size.
- Name the fallback as a Launch Checklist row with its date: "mailboxes connected in the sequencer, or build them in our own tenants that day", and move the first cold send by the days lost.
- Warmup dates start from the day the mailboxes pass the header test, never from the order date.

## 5. Monitoring setup (before the first warmup email)

| Tool | Set up | What it shows | Limits |
|-|-|-|-|
| Google Postmaster Tools | Add every sending domain at postmaster.google.com, copy the verification TXT (or CNAME) into DNS, click Verify; status updates within about 10 minutes. Add the domain that signs DKIM (`d=`), which for Workspace and Microsoft 365 mailboxes is the sending domain itself | Compliance status, spam rate, authentication, encryption, delivery errors, feedback loop; Google's help page also lists IP and domain reputation dashboards | Data covers mail to personal Gmail accounts only, and Google hides days with low volume. A B2B list on Workspace and Microsoft 365 may show little; that is expected, so the plan never relies on it alone |
| Microsoft SNDS | Not set up | Per-IP data for mail to Outlook.com | SNDS works on IP addresses you control. Google Workspace and Microsoft 365 mailboxes send from provider-owned shared IPs, so SNDS does not apply to this build. It applies only to dedicated-IP platforms |
| Microsoft tenant quota (each Microsoft 365 tenant) | Exchange admin center > Reports > Mail flow > Tenant outbound external recipients | External recipients used against the tenant's daily quota, warmup mail included | New tenants run at 10% then 25% of the standard quota (section 1). Over quota, external mail is blocked with `550 5.7.233` |
| Yahoo Complaint Feedback Loop | Enroll each DKIM domain in Yahoo Sender Hub | Complaint reports for Yahoo and AOL recipients | Domain-based |
| Spamhaus checker | check.spamhaus.org for every sending domain and the tracking host, before launch and on each review | Domain Blocklist status | Delisting is free and only through the checker |
| Seed placement test | One message to seed mailboxes at Gmail, Google Workspace, Outlook.com and Microsoft 365, on each review and before any volume raise | Inbox, spam or missing per provider | A sample, not a rate |
| Sequencer account health | Instantly or Smartlead account view, daily | Warmup health score, bounces per account | The sequencer's own measure |

## 6. Thresholds the plan writes in

| Signal | Where | Act | Stop |
|-|-|-|-|
| Spam rate, personal Gmail | Postmaster Tools, per domain | 0.1%: hold that domain's volume and find the cause (Google asks senders to stay below 0.1%) | 0.3%: stop the domain, promote a reserve (Google's ceiling) |
| Hard bounces | Sequencer, per campaign, after 200 sends | 2%: pause the campaign and re-validate the list (Alex Berman: bounces above 2% hurt domain reputation) | 5%: Alex Berman's critical line and Instantly's default campaign auto-pause after 200 sends |
| Blocklist | Spamhaus checker | Any listing: pause the domain, find the cause, request removal | Relisted after removal: retire the domain |
| Seed placement | Seed test | Spam at any provider: check copy, links and authentication before the next raise | |
| Sequencer health score | Sequencer, per account | Under 90%: hold that mailbox's cold sends at its current cap until it is back above 90% (Instantly's readiness line) | |
| Microsoft tenant quota | Exchange admin center report | Before each ramp step: mailboxes x (cold cap + warmup) against the quota at the tenant's age | 100%: external mail blocked until the 24-hour window clears |
| Replies per 1,000 sends, by recipient provider | Sequencer | Compare the Google and Microsoft pods; the user decides any shift of reserves from the measured gap | |

## 7. Review agenda

1. Postmaster spam rate per domain where data shows.
2. Bounces per campaign, sorted high to low.
3. Health scores under 90%.
4. Seed test results by provider.
5. Microsoft tenant quota used, per tenant.
6. Replies per 1,000 sends by recipient provider and by mailbox provider.
7. Reserves on hand; renewal dates coming up.

## Sources

- Spamhaus, Domain Blocklist (checked 2026-10-13): https://www.spamhaus.org/blocklists/domain-blocklist/
- Instantly, When your email account is ready for campaigns (checked 2026-10-13): https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, Warmup settings (increase 1, limit 10, reply rate 30 for new accounts; checked 2026-10-13): https://help.instantly.ai/en/articles/9214350-warmup-settings
- Instantly, How warmup works (10 warmup emails a day for new accounts; checked 2026-10-13): https://help.instantly.ai/en/articles/5975329-how-warm-up-works-and-why-it-s-important
- Instantly, High bounce auto-pause (5% default after 200 sends, checked 2026-10-13): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Alex Berman, cold email templates (new domains start at 10 to 20 a day and ramp up over 2 to 4 weeks; checked 2026-10-13): https://alexberman.com/cold-email-templates
- Alex Berman, custom tracking domains and Gmail (bounces above 2% hurt, above 5% critical; May 11, 2026): https://alexberman.com/custom-tracking-domain-gmail
- Google, Top 10 Gmail sender issues (keep spam rate below 0.1%; checked 2026-10-13): https://support.google.com/mail/answer/15256272
- Google, Email sender guidelines FAQ (0.3% spam rate): https://support.google.com/a/answer/14229414
- M3AAWG, Sender Best Common Practices v4.0: https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
- Microsoft 365 Message Center MC1454397, Updates to TERRL quotas for new, trial and education tenants (mirror, checked 2026-10-13): https://mc.merill.net/message/MC1454397
- Microsoft, Exchange Online limits (TERRL, report location; checked 2026-10-13): https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- Google Workspace, Gmail sending limits (trial cap, $100 threshold, up to 75 days; checked 2026-10-13): https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace
- Google Workspace, Set up DKIM (key available 24 to 72 hours after Gmail is on): https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Google, Postmaster Tools dashboards (checked 2026-10-13): https://support.google.com/mail/answer/14668346
- Google, Set up Postmaster Tools (verify a domain; checked 2026-10-13): https://support.google.com/mail/answer/9981691
- Microsoft, SNDS: https://sendersupport.olc.protection.outlook.com/snds/
- Yahoo Sender Hub, Complaint Feedback Loop: https://senders.yahooinc.com/complaint-feedback-loop/
