# Recovery Plans

How to turn an incident ("opens fell off a cliff and bounces jumped") into the short deliverable a sender can run today: a ranked diagnosis with the check that confirms or clears each cause, a dated day-by-day recovery calendar with send numbers and gates, what stops now, list re-validation, and what to measure instead of opens. The runbooks in `references/incident-runbooks.md` hold the per-incident detail; this file composes them into one plan. Thresholds come from `references/deliverability-primer.md` section 7. Checked 2026-10-13.

## 1. Fast intake: answer first, ask second

When the user gives the symptom numbers, write the plan in the first reply. Do not open with a questionnaire.

| Do | Detail |
|-|-|
| Restate the setup in numbers | Inboxes x cap x sending days = sends per week. 12 inboxes x 30 x 5 weekdays = 1,800. Label the sending days as an assumption when the user did not give them |
| Turn rates into counts | 4% of 1,800 = 72 hard bounces. Counts make the size of the problem visible and set the bounce budget for the restart |
| State at most 3 assumptions in one line | Sequencer, sending days, whether a new list went in this week |
| Fill the owner and sequencer with defaults, not blanks | Owner: "the outbound lead, unless you name someone else today". Sequencer: Instantly, plus one line for any other sequencer: "In Smartlead or another sequencer, the same two settings are the custom tracking domain and the bounce auto-pause; set the pause at 2%" |
| Put the facts that would change the ranking in the Diagnosis table once | The "Clears it" column carries them. Next Check-in lists only what to bring and what to decide |

## 2. Ranking the causes

Rank by evidence, in this order of tests:

1. Does the cause explain every symptom the user gave (opens, bounces, replies, scope)?
2. Is it shared by every affected domain? Four domains failing in the same week share a cause: the list, the copy, a linked or tracking domain, a settings change, or a DNS edit applied to all of them.
3. Did it change inside the window? Ask what changed in the days before the drop.
4. Cost of the check: the Spamhaus checker answers a DBL question in one lookup, so run it early even when another cause ranks higher.

### 2a. Symptom combinations

| Symptoms | Ranked causes |
|-|-|
| Opens down sharply on every domain, hard bounces 2% or more, volume flat | 1 bad or stale list batch; 2 spam placement following it; 3 tracking or linked domain flagged or broken; 4 authentication broken by a DNS edit; 5 domain on the DBL; opens-only measurement change explains the open drop but never the bounces |
| Opens down, bounces flat, replies down, every domain | 1 linked or tracking domain listed; 2 copy or link change; 3 complaint spike; 4 authentication |
| Opens down, bounces flat, replies steady against the pre-incident baseline, seeds in the inbox | Measurement problem only (R9): tracking record, setting, or recipient mix |
| One domain only | That domain: DBL, authentication on that domain, a mailbox above cap, a reused domain with history |
| One recipient provider only (by `sc_mx_provider`) | Provider-specific placement: Microsoft or Google branch of R2 |

### 2b. The confirming check for each cause

Every row of a deliverable's diagnosis table carries the check that confirms it and the result that clears it. Use these.

| Cause | Confirms it | Clears it |
|-|-|-|
| Bad or stale list batch | Bounce log shows `550 5.1.1` (Gmail: account does not exist) or `550 5.1.10` (Microsoft 365: recipient not found) spread across many recipient domains; the bounced rows share a source or upload date; validation date missing or older than the re-check window | Bounces spread evenly across old, proven rows; codes are mostly `5.7.x` |
| Catch-all rows in the main campaign | `5.1.1` bounces clustered in a few company domains; those rows came back catch-all at validation | Bounces spread across many companies |
| Spam placement | Live touch 1 lands in spam at any seed provider; human replies per 1,000 sends down against the pre-incident baseline at steady volume; Gmail `421 4.7.28` deferrals | Seeds in the inbox at every provider and replies back at the baseline |
| Tracking or linked domain | A Gmail `421 4.7.28` whose text names a URL domain (one of Gmail's listed variants); `dig +short CNAME <tracking host>` empty or pointing elsewhere; the tracking host, main site or booking link listed on the Spamhaus DBL, SURBL or URIBL; split seed test: the live copy lands in spam and the same copy with tracking off and links removed lands in the inbox | Both versions land in the same folder; all lookups clean |
| Authentication broken | Bounces with `5.7.26`, `5.7.27`, `5.7.30` or `4.7.32`; a test message's headers show anything other than `spf=pass`, `dkim=pass header.d=<sending domain>`, `dmarc=pass`; two `v=spf1` or two `v=DMARC1` records | Header test passes from every mailbox |
| Domain on the Spamhaus DBL | check.spamhaus.org lists the domain; bounces cite Spamhaus | Not listed |
| Measurement only | Replies and seeds steady while opens fell; tracking record or setting changed | Replies fell with opens |

### 2c. Run today: the checks as commands

The plan lists the confirming checks once, numbered, as commands the owner can run in order, written with the user's real domain (or one of their domains and "the same for the other 3"), never a `<domain>` placeholder. Day 0 of the calendar says "run checks 1 to 5"; the Diagnosis table says what result confirms or clears each cause.

1. Bounce log: export this week's hard bounces with the full SMTP reply text, then split by code and by upload date or source. Read the text: `5.1.1` or `5.1.10` with "does not exist" or "not found" is a dead mailbox (list); `5.7.26`, `5.7.27` or `5.7.30` with "unauthenticated", "SPF", "DKIM" or "DMARC" is authentication; `5.7.28` or `4.7.28` with "unusual rate of unsolicited mail" is reputation (Google Workspace, Gmail SMTP errors and codes).
2. DNS on each sending domain: `dig +short TXT <domain>` (exactly one `v=spf1`), `dig +short TXT google._domainkey.<domain>` (a `v=DKIM1` key; Workspace's default selector is `google`), `dig +short TXT _dmarc.<domain>` (exactly one `v=DMARC1`), `dig +short CNAME inst.<domain>` (Instantly's tracking host must point to `prox.itrackly.com`).
3. Header test: send from every mailbox to a personal Gmail seed, open Show original, and read `spf=pass`, `dkim=pass header.d=<domain>`, `dmarc=pass`.
4. Blocklists: each sending domain, the tracking host, the main site and any booking link on check.spamhaus.org, then the linked domains on SURBL (surbl.org) and URIBL (admin.uribl.com).
5. Seed test: the live touch 1 from one inbox per domain to a seed you own at each provider (personal Gmail, Workspace, Outlook.com, Microsoft 365, Yahoo), or a GlockApps Smart Test, which takes one address and distributes the message to its seed mailboxes. GlockApps weights coverage toward US consumer providers, so keep your own Workspace and Microsoft 365 seeds.

### 2d. Every fix written out

A cause the plan ranks gets its fix in full, ready to paste or click, in one line or block under the checks. The fix for a bad list is the re-validation section. The others:

| Cause confirmed | Fix to write out |
|-|-|
| SPF missing, duplicated or failing | One record per domain: `v=spf1 include:_spf.google.com ~all` (Workspace); merge the include into an existing record, never add a second |
| DKIM missing or failing | Google Admin console > Apps > Google Workspace > Gmail > Authenticate email, pick the domain, Generate New Record, 2048-bit, prefix `google`, publish the TXT, then Start authentication |
| DMARC missing or duplicated | One record: `_dmarc.<domain>` TXT `v=DMARC1; p=none; rua=mailto:<reports address>` |
| Tracking CNAME broken | `inst` CNAME to `prox.itrackly.com` (Instantly help), or open tracking off for the recovery |
| Domain or linked domain listed | Fix the cause first, then request removal through check.spamhaus.org; take a listed link out of every touch until it clears |

The record values and the Admin console path come from the authentication runbook and Google's DKIM setup page.

A Postmaster spam rate under 0.1% does not clear spam placement. Google's help page says the rate covers only mail that reached the inbox, so it can look low when Gmail is filtering much of the mail to spam.

## 3. What opens can and cannot tell you

Put this in every incident plan in three or four sentences, because the user's alarm usually starts with the open rate.

| Fact | Source | What it does to the open rate |
|-|-|-|
| Apple Mail Privacy Protection downloads remote content in the background when a message arrives, whether or not the recipient engages | Apple, Mail Privacy Protection & Privacy | Records an "open" for Apple Mail recipients who never read the message |
| Outlook blocks automatic picture downloads by default | Microsoft Support, block or unblock automatic picture downloads | Real readers in Outlook often never load the pixel |
| Security filters (Proofpoint and Barracuda are named examples) open messages and click links within seconds of delivery | lemlist help, identifying legitimate clicks and opens | False opens and clicks at gateway-protected companies |
| A broken or blocked tracking host records nothing | How pixel tracking works: the open is counted only when the tracking host serves the image | The drop is evidence that something changed, with no way to say what |

Decide with the three signals that do not depend on a pixel:

1. Seed placement: the live touch 1 to personal Gmail, Workspace, Outlook.com, Microsoft 365 and Yahoo seeds, folder recorded once every seed has received it.
2. Human replies per 1,000 sends against the pre-incident baseline (auto-replies excluded).
3. Hard bounce rate over the last 200 sends, read with its SMTP codes.

Turn open tracking off for the recovery. The pixel and the tracking host add filter signals, and the number cannot judge the recovery.

## 4. Stop now

| Stop | Why |
|-|-|
| Every cold campaign on the affected domains | Each send to the bad batch adds bounces, already past Berman's 2% line |
| Uploads of new lists and edits to caps | A new variable during diagnosis hides the cause |
| Buying domains or inboxes | New domains would get the same unverified list and copy and burn the same way. Start reserves only after the cause is written down |
| Open tracking and tracked links in touch 1 | See section 3 |
| Sends to catch-all and unknown rows | The validator could not confirm the mailbox, so they wait until the main file proves clean |
| Delisting requests | Fix the cause first; a quick relisting makes the next removal harder |

Lower the sequencer's bounce auto-pause so it catches the next spike. Instantly: Settings > Preferences, the Switch button next to "Automatically pause campaigns with high bounce rates", set 2% (the default is 5%, checked after 200 sends; Instantly help). In another sequencer, the same setting is its bounce auto-pause.

Keep: warmup at its current setting (do not raise it; a warmup surge is a volume jump too), the opt-out line in every touch, and same-day suppression of every bounce and opt-out across all campaigns.

## 5. Re-validation for the restart

| Rows | Action |
|-|-|
| Unsent rows of the batch that bounced | Re-validate all of them |
| Any other queued row last validated before the re-check window | Re-validate |
| Rows validated inside the window from a source that stayed under 2% bounces | Keep |
| Every hard-bounced address | Suppress workspace-wide; never re-validate |

Route results with primer section 5. During the recovery calendar the main file is 100% `valid`; catch-all rows wait until the inboxes are back at their previous cap and then run in their own campaign. Compare each source's `invalid` share on re-validation and report it, so the user can decide whether to keep buying from it.

Cost: rows x $0.00169. 3,000 queued rows cost $5.07. The Email Finder costs $0.05 per email found (nothing when none is found) and is worth running only on high-value accounts whose contact came back invalid.

## 6. The recovery calendar

Write it with real dates from today, weekday names, sends per inbox and total sends a day, and a numeric gate on every step. Restart numbers follow the primer section 6 ramp: start at 10 (the low end of Alex Berman's 10 to 20 a day), then equal weekly steps back to the previous cap over Berman's 2 to 4 weeks, no step more than double the last (Google sender guidelines), and the cap under 50 (Berman).

| Day | What happens | Sends per inbox | Gate to move on |
|-|-|-|-|
| 0 (today) | Stop list above. Export the bounce log with codes and per-mailbox sends, bounces and replies for the weeks before the drop. Run the checks in section 2b | 0 | Cause written down |
| 1 | Re-validate (section 5). Fix the cause: route the list, restore the tracking record or turn tracking off, fix DNS. Seed test 1 from one mailbox per domain, including the split test when tracking or links are suspects | 0 | File 100% `valid`; header test passes from every mailbox; no DBL, SURBL or URIBL listing |
| 2 | First restart day if seed test 1 reached the inbox at every seed provider. Highest `email_quality` rows first, best-fit segment first | 10 | Hard bounces under 2% over the first 200 restart sends |
| Rest of week 1 | Seed test 2 before the week ends. Read bounces, replies, `4.7.28` deferrals and opt-outs every morning | 10 | Inbox at every seed provider; bounces under 2% over the last 200 sends; zero `4.7.28`; every domain under 0.1% spam rate |
| Week 2 (and week 3 for a 3-step ramp) | Step up by an equal share of the gap to the previous cap | Between 10 and the previous cap, never more than double the week before | Same gates; replies per 1,000 sends reported against the pre-incident baseline |
| Week 3 or 4 onward | Back to the previous cap | Previous cap, under 50 | Same gates every week |

Day 2 can slip: when seed test 1 fails, fix and retest, and the calendar moves by the days lost. Count weekdays only if the program sends only on weekdays, and say so in the plan.

Total sends a day = inboxes x sends per inbox. For 12 inboxes and a previous cap of 30 over a 3-week ramp: 120, 240, 360. Every inbox restarts at 10 in an incident plan, because placement is in question until two seed tests pass.

### 6a. Back-off rules during the calendar

| Event | Action |
|-|-|
| Campaign or mailbox hard bounces 2% or more over its last 200 sends | Back one step for the rest of the week; re-check the source |
| Gmail `421 4.7.28` on a domain | Send nothing from that domain for at least 10 minutes (the rate-limit steps in Google's sender guidelines), hold its step until a week passes without one, run the complaint checks |
| `550 5.7.28`, a spam rate of 0.3% on any day, or a DBL listing | Stop that domain (R3 or R4) |

### 6b. Keep, rest or retire each domain

| Domain state at the first step up | Decision |
|-|-|
| Seeds in the inbox at every provider, bounces in range | Keep; continue the calendar |
| Seeds in spam at one provider | Hold at 10 a day for another week, retest |
| Seeds in spam at several providers with the cause fixed | Rest with warmup only until Instantly's readiness rule holds again (at least 2 weeks, health score above 90%), then ramp from 10 |
| A second DBL listing, or still in spam after the rest | Retire from cold email; move its volume to a warmed reserve |

Seeds decide this, with bounces and spam rate. Postmaster may show no data at a few hundred sends a day to personal Gmail, and Google is retiring its Domain and IP Reputation dashboards, so do not wait on a reputation label.

Reserve capacity: once the cause is written down and fixed (day 1 or later), start enough reserve domains warming to carry the volume of any domain you might retire, 2 to 3 inboxes each (Berman). At least 2 weeks of warmup (Instantly) puts them ready around the time a retire decision would need them.

## 7. The deliverable

Sections, in order: Verdict, Stop Now, Diagnosis (ranked table, the numbered checks of section 2c, the fixes of section 2d for the ranked causes), Measurement, List Re-validation, Recovery Plan, Resume and Retire Rules, Next Check-in. Keep it under about 1,500 words.

State each fact once. The numeric gate is defined once, as the "standard gate" line above the calendar (hard bounces under 2% over the last 200 sends, zero `4.7.28`, spam rate under 0.1%); calendar rows say "standard gate" plus anything extra for that day, and the Resume and Retire table says what to do when a gate is missed without restating the numbers. Name the document behind each outside number ("Google's sender guidelines", "Instantly help"), not just the company. Leave out the six-month audit and any table of checks not yet run: each check appears once, as the confirming test for a cause. File paths, runbook numbers, skill names and tool ids stay out of the plan. `templates/incident-plan-template.md` is the shell; `examples/incident-example.md` is a filled one.

## Sources

- Apple, Mail Privacy Protection & Privacy (background download on arrival; checked 2026-10-13): https://www.apple.com/legal/privacy/data/en/mail-privacy-protection/
- Microsoft Support, Block or unblock automatic picture downloads in email messages (checked 2026-10-13): https://support.microsoft.com/en-us/office/block-or-unblock-automatic-picture-downloads-in-email-messages-15e08854-6808-49b1-9a0a-50b81f2d617a
- lemlist help, Identifying legitimate clicks and opens (security filters open and click within seconds; checked 2026-10-13): https://help.lemlist.com/en/articles/9140285-identifying-legitimate-clicks-and-opens
- Google, Postmaster Tools dashboards (spam rate covers inbox-delivered, DKIM-authenticated mail; low volume may lack data; checked 2026-10-13): https://support.google.com/mail/answer/14668346
- Google Workspace, Gmail SMTP errors and codes (`5.1.1`, `4.7.28` including the URL-domain variant, `5.7.28`, `5.7.26`; checked 2026-10-13): https://knowledge.workspace.google.com/admin/support/troubleshooting/gmail-smtp-errors-and-codes
- Microsoft Learn, Fix NDR error 550 5.1.10 in Exchange Online: https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/non-delivery-reports-in-exchange-online/fix-error-code-550-5-1-10-in-exchange-online
- Google, Email sender guidelines FAQ (0.3% line and 7-day mitigation rule): https://support.google.com/a/answer/14229414
- Google, Email sender guidelines, Gmail help copy (spam rate under 0.10%; doubling volume at once can cause rate limiting; stop at least 10 minutes on `4.7.28`; checked 2026-10-13): https://support.google.com/mail/answer/81126
- Alex Berman, cold email templates (start at 10 to 20 a day, ramp over 2 to 4 weeks, bounces under 2%; checked 2026-10-13): https://alexberman.com/cold-email-templates
- Alex Berman, TAM strategy breakdown (2 to 3 inboxes per domain, under 50 a day per inbox; checked 2026-10-13): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Instantly, High bounce auto-pause (5% after 200 sends; checked 2026-10-13): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Instantly, When your email account is ready for campaigns (2 weeks of warmup, health score above 90%; checked 2026-10-13): https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Spamhaus, Domain Blocklist (check domains in message bodies): https://www.spamhaus.org/blocklists/domain-blocklist/
- Google, Learn about the deprecation of the old Postmaster Tools interface (Domain and IP Reputation dashboards being retired; checked 2026-10-13): https://support.google.com/mail/answer/16594218
- Google Workspace, Set up DKIM (Admin console path, 2048-bit, prefix `google`, Start authentication): https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Instantly, Custom tracking domain (host `inst` to `prox.itrackly.com`): https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- GlockApps, Email seed list testing (Smart Test proxy address; coverage weighted toward US consumer providers; checked 2026-10-13): https://glockapps.com/blog/email-seed-list-testing-get-the-best-results-with-glockapps/
- ScraperCity, Email Validator: https://scrapercity.com/email-validator
