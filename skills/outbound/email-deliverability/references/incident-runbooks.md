# Incident Runbooks

Step-by-step responses to the deliverability incidents a cold email program hits: bounce spikes, spam folder placement, complaint spikes, blocklisted domains or IPs, provider rejections and mailbox suspensions. Each runbook has a trigger, a first-hour containment step, a diagnosis table, the fix, and the condition for resuming. Thresholds come from `references/deliverability-primer.md` section 7. SMTP codes come from the Google sender guidelines FAQ and Microsoft's documentation, checked 2026-10-13.

## How to use

1. Match the symptom to a runbook with the triage table.
2. Contain first: stop the damage before diagnosing.
3. Log every incident in the health report's Incidents and Actions table with date, trigger, owner and status.
4. Resume only when the resume condition holds, then re-ramp per `inbox-setup` (`references/warmup-and-ramp.md` section 7 in that skill).

## Triage

| Symptom | Runbook |
|-|-|
| Sequencer auto-paused a campaign; hard bounces at 2% or more | R1 Bounce spike |
| Seed tests land in spam; reply rate fell by half with steady volume | R2 Spam folder placement |
| Postmaster spam rate at 0.1% or more; Yahoo CFL reports; prospects reply "spam" | R3 Complaint spike |
| Domain appears on the Spamhaus DBL | R4 Blocklisted domain |
| Dedicated IP on Barracuda, SpamCop, Spamhaus or Microsoft's banned list | R5 Blocklisted IP |
| Bounces with Google `4.7.2x`, `4.7.3x`, `5.7.2x` codes or Microsoft `5.7.515` | R6 Authentication rejection |
| Google `4.7.28` or other rate-limit deferrals | R7 Rate limiting |
| Provider disabled sending, or the sequencer shows the account disconnected | R8 Mailbox suspended |

## R1. Bounce spike

**Trigger:** hard bounces at 2% or more on a campaign over its last 200 sends, 3% or more on one mailbox, or a sequencer auto-pause. Instantly's default auto-pause fires above 5% after 200 sends; set yours lower where the platform allows.

**First hour:**

1. Pause the campaign (or confirm the auto-pause). Leave warmup on.
2. Export the bounce log with SMTP codes.
3. Stop any other campaign fed by the same list batch.

**Diagnosis:**

| Bounce code pattern | Likely cause | Check |
|-|-|-|
| `550 5.1.1` user unknown, spread across many domains | Stale or unvalidated rows | `email_validated_at` older than 30 days, or rows that skipped validation |
| `550 5.1.1` concentrated in a few company domains | Catch-all domains that reject later | `sc_is_catch_all` on the bounced rows |
| `5.7.x` policy or authentication codes | Not a list problem | Go to R6 |
| `4.x.x` deferrals counted as bounces | Rate limits or greylisting | Go to R7; check how the sequencer classifies soft bounces |
| Bounces from one mailbox only | That mailbox or its domain | Postmaster for the domain; seed test from that mailbox |

**Fix:**

1. Re-validate every unsent row of the batch with `validate_emails` ($0.0072 per email) and drop anything not `valid`.
2. Add every bounced address to the workspace blocklist.
3. If catch-alls drove it, suppress the bouncing company domains and cut the catch-all share to 5% for 2 weeks.
4. If one source produced over 15% invalid on re-validation, stop using that source (list quality standard section 5).

**Resume when:** the re-validated file is 100% `valid`. Restart the paused mailboxes at ramp row 1 (10 a day) if they crossed 3%; otherwise at their previous cap.

## R2. Spam folder placement

**Trigger:** seed tests in spam at 2 or more providers, every Microsoft seed in junk, or reply rate down 50% week over week at steady volume and list quality.

**First hour:**

1. Cut the affected domains' cold volume by 50%. Do not add new domains or mailboxes to compensate.
2. Run a second seed test from a different mailbox on the same domain to see if it is mailbox or domain level.

**Diagnosis:**

| Check | Finding | Fix |
|-|-|-|
| Headers on the seed | SPF, DKIM or DMARC not passing or not aligned | R6 |
| Tracking | Open pixel or tracked links on | Turn off open tracking; remove links from touch 1 |
| Copy | Same template across all mailboxes for weeks; link shorteners; attachments; image signature | New copy from `cold-email-copywriting`, plain text |
| Volume pattern | Burst sending, gaps under 2 minutes, cap raised in the last week | Return to the previous cap; 3 to 6 minute gaps |
| Postmaster | Spam rate at 0.1% or more | R3 |
| Blocklists | Domain on the DBL | R4 |
| Warmup | Warmup turned off when campaigns started | Turn back on at 10 a day |
| Microsoft only | All Microsoft seeds in junk, Gmail fine | Check for `5.7.515`-style policy messages; verify DMARC alignment; run Microsoft seeds after each change |

**Resume when:** two seed tests 48 hours apart land in the inbox at 4 of 5 providers. Then raise volume back in two weekly steps.

## R3. Complaint spike

**Trigger:** Postmaster spam rate at 0.1% or more for 2 days, any day at 0.3%, Yahoo CFL reports, or 2 or more "this is spam" replies in a week from one domain's sends.

**First hour:**

1. At 0.1% for 2 days: cut that domain's volume 50%.
2. At 0.3%: stop the domain. Google says a bulk sender at 0.3% or more is ineligible for mitigation until it stays below 0.3% for 7 consecutive days.
3. Suppress every complainer at email and company-domain level.

**Diagnosis:**

| Check | Why |
|-|-|
| Which segment and which touch drew complaints | A wrong-fit segment complains; so does a fourth follow-up to people who never engaged |
| Opt-out line present and working | People mark spam when they cannot see how to stop mail |
| Contacts per company | More than 3 contacts at one company in a campaign reads as a blast |
| Personal Gmail share of the list | Consumer addresses complain more and feed Postmaster directly |

**Fix:** narrow the segment, drop the last touch for that segment, put the opt-out line in the first two lines of touch 3 and later, and remove personal-domain addresses from B2B campaigns.

**Resume when:** 7 consecutive days under 0.1% at the reduced volume, then return to full volume.

## R4. Blocklisted domain (Spamhaus DBL)

**Trigger:** check.spamhaus.org shows a sending domain listed, or bounces cite Spamhaus.

1. Stop every mailbox on the domain the same hour. Keep warmup off while listed.
2. Check the other sending domains; a listing often means the pattern (copy, list source, volume) affects them too.
3. Find the cause: list source with traps or old addresses, complaint spike, a sudden volume jump, or a batch of new domains spun up at once (Spamhaus treats rapidly rotating many domains as snowshoeing).
4. Fix the cause before requesting removal. Spamhaus delisting is free and only through the checker.
5. After removal, rest the domain 14 days, then a full ramp from day 1.
6. A second listing after removal: retire the domain per `inbox-setup` rotation rules. Keep it registered and redirecting for 12 months.

## R5. Blocklisted IP (dedicated or private IP senders)

Applies when you send through dedicated or private IPs (for example EmailBison dedicated IPs or ManyReach private IPs). Workspace and Microsoft 365 mailboxes use the provider's IPs; for them, go to R4 for your domain.

| List | Signal | Removal |
|-|-|-|
| Microsoft 365 banned IP | NDR `550 5.7.606-649 Access denied, banned sending IP` | sender.office.com delist portal, one IP and one email per request; Microsoft says up to 24 hours or longer |
| Microsoft banned sender | NDR `5.7.511 Access denied, banned sender` | Forward the full NDR to delist@microsoft.com; Microsoft says it will respond within 48 hours |
| Barracuda BRBL | Barracuda lookup | Removal request with a valid explanation, typically processed within 12 hours |
| SpamCop | SpamCop lookup | Automatic after 24 hours with no new reports |
| Spamhaus IP lists | check.spamhaus.org | Through the checker after fixing the cause |

Ask the platform to rotate the IP only after the cause is fixed. ManyReach's pricing page lists free blacklisted IP swapping on its private IP add-on (checked 2026-10-13).

## R6. Authentication rejection

**Trigger:** bounces or deferrals with these codes.

| Provider | Code | Meaning | Fix |
|-|-|-|-|
| Google | `4.7.27` / `5.7.27` | SPF did not pass | One SPF record with the provider include; under 10 lookups |
| Google | `4.7.30` / `5.7.30` | DKIM did not pass | DKIM published and signing turned on for that domain |
| Google | `4.7.31` | No DMARC record or no policy | Publish `v=DMARC1; p=none; rua=mailto:...` |
| Google | `4.7.32` | From domain not aligned with SPF or DKIM | Sign with the From domain's own DKIM key |
| Google | `4.7.23` / `5.7.25` | PTR missing or not matching | Dedicated IP senders only: fix reverse DNS with the IP owner |
| Google | `4.7.29` / `5.7.29` | No TLS | Sequencer or SMTP relay must use TLS |
| Microsoft (Outlook.com consumer) | `550; 5.7.515` | Domain does not meet the required authentication level | SPF pass, DKIM pass, DMARC at least `p=none` aligned |

Google lists the 4.x.x codes as rate limited and the 5.x.x codes as blocked (sender guidelines FAQ). From November 2025 Google ramps up enforcement with temporary and permanent rejections, and new domains follow an accelerated timetable. Stop the affected domain until the header test passes on every mailbox.

## R7. Rate limiting

**Trigger:** deferrals such as Google `4.7.28`, or Yahoo closing connections without an error.

1. Google says to pause at least 10 minutes after `4.7.28`; the sequencer's retry should handle it.
2. Check for bursts: gap under 2 minutes, more than 15 sends an hour per mailbox, or a cap raised by more than 10 a day in the last week.
3. Spread the schedule and return to the previous cap.
4. Yahoo limits messages per connection and closes it without an error code; Yahoo says to reconnect. No action unless deferrals keep growing.

## R8. Mailbox suspended or disconnected

| Signal | Action |
|-|-|
| Sequencer shows "account error" or disconnected (Instantly `account_error` webhook, Smartlead `EMAIL_ACCOUNT_DISCONNECTED`, EmailBison "Email Account Disconnected") | Reconnect by OAuth; if it fails, check the admin console |
| Google Workspace: user suspended for suspicious activity or sending limits | Admin restores the user; read the admin alert; cut that mailbox to ramp row 1 |
| Microsoft 365: user restricted from sending | Admin center restricted users list; release after fixing; cut to ramp row 1 |
| Second suspension in 60 days | Retire the mailbox (`inbox-setup` rotation rules) |

In-flight leads of a suspended mailbox wait up to 7 days for it to return; after that, end their sequence instead of switching senders mid-thread.

## Incident log fields

| Field | Example |
|-|-|
| Date and time opened | 2026-12-01 10:40 CT |
| Runbook | R1 Bounce spike |
| Scope | Campaign "B - MT/PT", mailboxes marcus.bell@ and elenar@ on useledgerline.com |
| Trigger value | 3.4% hard bounces over last 200 sends |
| Containment | Campaign paused 10:45 |
| Cause | Batch validated 45 days before send |
| Fix | 640 unsent rows re-validated, 41 invalid removed |
| Resume condition | File 100% valid; mailboxes restart at 10 a day |
| Closed | 2026-12-03 |

## Sources

- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Email sender guidelines FAQ (SMTP codes, enforcement timeline): https://support.google.com/a/answer/14229414
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders (Apr 2025): https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Mailgun, Microsoft sender requirements summary: https://www.mailgun.com/blog/deliverability/microsoft-sender-requirements/
- Microsoft, Use the delist portal to unblock yourself: https://learn.microsoft.com/en-us/defender-office-365/external-senders-use-the-delist-portal-to-unblock-yourself
- Spamhaus, Domain Blocklist: https://www.spamhaus.org/blocklists/domain-blocklist/
- Barracuda Central, Removal request: https://www.barracudacentral.org/rbl/removal-request
- SpamCop, How long do listings last: https://www.spamcop.net/fom-serve/cache/298.html
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Instantly, Webhook events: https://developer.instantly.ai/webhook-events
- Smartlead, Webhook events: https://api.smartlead.ai/api-reference/webhooks/events
- EmailBison, When are webhooks triggered: https://docs.emailbison.com/webhooks/when-are-webhooks-triggered
- ManyReach, Pricing: https://manyreach.com/pricing
