# Incident Runbooks

Step-by-step responses to the deliverability incidents a cold email program hits: bounce spikes, spam folder placement, complaint spikes, blocklisted domains or IPs, provider rejections and mailbox suspensions. Each runbook has a trigger, a first-hour containment step, a diagnosis table, the fix, and the condition for resuming. Thresholds come from `references/deliverability-primer.md` section 7. SMTP codes come from the Google sender guidelines FAQ and Microsoft's documentation, checked 2026-10-13.

## How to use

1. Match the symptom to a runbook with the triage table. If only opens moved, start with R9. When several symptoms arrive together (opens collapsing plus a bounce spike across every domain), rank the causes and write the dated plan with `references/recovery-plans.md`; the runbooks below supply each step.
2. Contain first: stop the damage before diagnosing.
3. Log every incident in the health report's Incidents and Actions table with date, incident type, trigger, owner and status. The report names the type ("Bounce spike"), never the runbook number.
4. Resume only when the resume condition holds, then re-ramp per `inbox-setup` (`references/warmup-and-ramp.md` section 7 in that skill).

## Incident command

| Rule | Detail |
|-|-|
| One owner | One named person can pause any domain, mailbox or campaign without approval. The health report's Scope table names them, plus a backup for their days off |
| Backup capacity | Every report lists the warmed reserve domains, their mailboxes and the sends a day they can take. A paused domain's volume moves to a reserve the same day, or waits |
| No buying mid-incident | Never buy replacement domains while the cause is unknown. New domains need at least 2 weeks of warmup anyway (Instantly's readiness rule), and they inherit the list, copy or volume pattern that caused the incident and burn the same way. Buy only after the cause is written down and fixed |
| Written resume condition | Set before the fix starts; the owner signs off when it holds |

## Triage

| Symptom | Runbook |
|-|-|
| Sequencer auto-paused a campaign; hard bounces at 2% or more | R1 Bounce spike |
| Seed tests go to spam; replies per 1,000 sends fell against the baseline with steady volume | R2 Spam folder placement |
| Postmaster spam rate at 0.1% or more; Yahoo CFL reports; prospects reply "spam" | R3 Complaint spike |
| Domain appears on the Spamhaus DBL | R4 Blocklisted domain |
| Dedicated IP on Barracuda, SpamCop, Spamhaus or Microsoft's banned list | R5 Blocklisted IP |
| Bounces with Google `4.7.2x`, `4.7.3x`, `5.7.2x` codes or Microsoft `5.7.515` | R6 Authentication rejection |
| Google `421 4.7.28` (Gmail detected an unusual rate of unsolicited mail) or `550 5.7.28` | R7 Gmail reputation deferral |
| Yahoo closing connections, other rate-limit deferrals | R7 Rate limiting |
| Open rate fell; replies per 1,000 sends, bounces and seeds unchanged | R9 Measurement problem only |
| Provider disabled sending, or the sequencer shows the account disconnected | R8 Mailbox suspended |

## R1. Bounce spike

**Trigger:** hard bounces at 2% or more on a campaign or a mailbox over its last 200 sends (Berman's line, Instantly's window), or a sequencer auto-pause. Instantly's default auto-pause fires above 5% after 200 sends; set it to 2% at Settings > Preferences, the Switch button next to "Automatically pause campaigns with high bounce rates" (Instantly help). Other sequencers: the same bounce auto-pause setting, at 2%.

**Contain:**

1. Pause the campaign (or confirm the auto-pause). Leave warmup on.
2. Export the bounce log with SMTP codes.
3. Stop any other campaign fed by the same list batch.

**Diagnosis:**

| Bounce code pattern | Likely cause | Check |
|-|-|-|
| `550 5.1.1` user unknown, spread across many domains | Stale or unvalidated rows | `email_validated_at` older than the re-check window, or rows that skipped validation |
| `550 5.1.1` concentrated in a few company domains | Catch-all domains that reject later | `sc_is_catch_all` on the bounced rows |
| `5.7.x` policy or authentication codes | Not a list problem | Go to R6 |
| `4.x.x` deferrals counted as bounces | Rate limits or greylisting | Go to R7; check how the sequencer classifies soft bounces |
| Bounces from one mailbox only | That mailbox or its domain | Postmaster for the domain; seed test from that mailbox |

**Fix:**

1. Re-validate every unsent row of the batch with `validate_emails` ($0.00169 per email) and drop anything not `valid`.
2. Add every bounced address to the workspace blocklist.
3. If catch-alls drove it, suppress the bouncing company domains and keep the catch-all campaign paused until the main campaign is back under 2%.
4. Report each source's `invalid` share on re-validation, so the user can drop the worst source.
5. Soft bounces: read their codes for `4.7.28` and other rate limits before the next send (R7).

**Resume when:** the re-validated file is 100% `valid`. Restart the paused mailboxes at 10 a day and ramp back per primer section 6.

## R2. Spam folder placement

**Trigger:** seed tests in spam at any provider, or replies per 1,000 sends down against the baseline at steady volume and list quality.

**Contain:**

1. Lower the affected domains' cold volume. Do not add new domains or mailboxes to compensate.
2. Run a second seed test from a different mailbox on the same domain to see if it is mailbox or domain level.

**Diagnosis:**

| Check | Finding | Fix |
|-|-|-|
| Headers on the seed | SPF, DKIM or DMARC not passing or not aligned | R6 |
| Tracking | Open pixel or tracked links on | Turn off open tracking; remove links from touch 1 |
| Copy | Same template across all mailboxes for weeks; link shorteners; attachments; image signature | New copy from `cold-email-copywriting`, plain text |
| Volume pattern | Burst sending, or a cap raised to more than double at once (Google: doubling volume suddenly can cause rate limiting or reputation drops) | Return to the previous cap; spread sends across the window (gap = window minutes / cap) |
| Postmaster | Spam rate at 0.1% or more | R3 |
| Blocklists | Sending domain on the DBL, or a linked domain (tracking host, main site, booking link) on the DBL, SURBL or URIBL | R4; for a linked domain, remove the link from every touch until it is delisted |
| Warmup | Warmup turned off when campaigns started | Turn it back on (Instantly's new-account default is a daily warmup limit of 10) |
| Microsoft only | All Microsoft seeds in junk, Gmail fine | Check for `5.7.515`-style policy messages; verify DMARC alignment; run Microsoft seeds after each change |

**Resume when:** two seed tests reach the inbox at every provider. Then raise volume back in weekly steps, none more than double the last (Google).

## R3. Complaint spike

**Trigger:** Postmaster spam rate at 0.1% or more on any day (Google's target), any day at 0.3%, Yahoo CFL reports, or "this is spam" replies from one domain's sends.

**Contain:**

1. At 0.1% or more: lower that domain's volume.
2. At 0.3%: stop the domain. Google says a bulk sender at 0.3% or more is ineligible for mitigation until it stays below 0.3% for 7 consecutive days.
3. Suppress every complainer at email and company-domain level.

**Diagnosis:**

| Check | Why |
|-|-|
| Which segment and which touch drew complaints | The fix targets that segment or touch |
| Opt-out line and unsubscribe header present and working | Google and Yahoo require an easy unsubscribe from bulk senders |
| Personal Gmail share of the list | Personal Gmail traffic is what Postmaster's spam rate measures; mail to Workspace accounts is outside Google's sender guidelines |

**Fix:** narrow the segment or drop the touch that drew the complaints, and remove personal-domain addresses from B2B campaigns.

**Resume when:** 7 consecutive days under 0.1% at the reduced volume (Google's target, over the 7-day window Google uses for mitigation), then return to full volume in weekly steps.

## R4. Blocklisted domain (Spamhaus DBL)

**Trigger:** check.spamhaus.org shows a sending domain listed, or bounces cite Spamhaus.

1. Stop every mailbox on the domain. Keep warmup off while listed.
2. Check the other sending domains; a listing often means the same cause (copy, list source, volume) affects them too.
3. Find the cause: list source with traps or old addresses, complaint spike, a sudden volume jump, a listed link or tracking domain in the body, or a batch of new domains spun up at once. Spamhaus describes snowshoeing as a technique using many domains and IPs that change often, and says domains that act that way get treated that way.
4. Fix the cause before requesting removal. Spamhaus delisting is free and only through the checker.
5. After removal, re-warm until Instantly's readiness rule holds (at least 2 weeks, health score above 90%), then the full primer section 6 ramp.
6. A second listing after removal: retire the domain per `inbox-setup` rotation rules.

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

**Recovery records (copy, then replace the domain).** A Google Workspace sending domain `getacme.com` with reports going to the main domain `acme.com`:

```text
getacme.com.                  TXT  "v=spf1 include:_spf.google.com ~all"
google._domainkey.getacme.com. TXT  "v=DKIM1; k=rsa; p=<2048-bit key from Admin console>"
_dmarc.getacme.com.           TXT  "v=DMARC1; p=none; rua=mailto:dmarc@acme.com"
*._report._dmarc.acme.com.    TXT  "v=DMARC1"          (once, on the main domain)
```

One DKIM selector per signer: Workspace or Microsoft 365 signs mail sent through the mailbox, and a sequencer that sends through its own servers signs with its own selector, so each key rotates without breaking the other.

Microsoft 365: SPF `v=spf1 include:spf.protection.outlook.com -all`, DKIM as two CNAMEs (`selector1._domainkey`, `selector2._domainkey`) copied from the Defender portal, the same DMARC record.

Google DKIM key: Admin console > Apps > Google Workspace > Gmail > Authenticate email, pick the domain, Generate New Record, key length 2048 (Google recommends it when the DNS host supports it; 1024 otherwise), selector prefix `google`. Publish the TXT, wait for it to resolve, then click Start authentication; the status reads "Authenticating email with DKIM" when it works. Keep one SPF record per domain: merge the include into the existing record, never add a second. Over 10 lookups: remove includes for tools that no longer send, before any SPF flattening; a flattened record lists today's provider IPs and fails without warning when the provider changes them.

## R7. Gmail reputation deferral and rate limiting

**Trigger:** Google `421 4.7.28` or `550 5.7.28`, or Yahoo closing connections without an error.

Gmail's error reference gives `4.7.28` texts such as "an unusual rate of unsolicited email originating from your IP Netblock" and lists `550 5.7.28` as the blocked form of the same finding. Treat `4.7.28` as a reputation warning about unsolicited mail. The sequencer's retry delivers the deferred message later; the reputation problem stays.

1. Send nothing from the domain for at least 10 minutes (the rate-limit steps in Google's sender guidelines, not the SMTP error page), then lower that domain's volume.
2. Run the R3 checks: Postmaster spam rate, "spam" replies, the segment and touch that drew them, personal Gmail share of the list.
3. Check for bursts: sends bunched instead of spread across the window, or a cap raised to more than double at once (Google). Spread the schedule and return to the previous cap.
4. Any `5.7.28`: stop the domain and run R3 in full.
5. Yahoo limits messages per connection and closes it without an error code; Yahoo says to reconnect. No action unless deferrals keep growing.

**Resume when:** a week with no `4.7.28` on the domain and its spam rate under 0.1% (Google), then back to full volume in weekly steps, none more than double the last.

## R8. Mailbox suspended or disconnected

| Signal | Action |
|-|-|
| Sequencer shows "account error" or disconnected (Instantly `account_error` webhook, Smartlead `EMAIL_ACCOUNT_DISCONNECTED`, EmailBison "Email Account Disconnected") | Reconnect by OAuth; if it fails, check the admin console |
| Google Workspace: user suspended for suspicious activity or sending limits | Admin restores the user; read the admin alert; restart that mailbox at 10 a day (primer section 6) |
| Microsoft 365: user restricted from sending | Admin center restricted users list; release after fixing; restart at 10 a day |
| A second suspension after the fix | Retire the mailbox (`inbox-setup` rotation rules) |

In-flight leads of a suspended mailbox wait for it to return; if it is retired, end their sequence instead of switching senders mid-thread.

## R9. Measurement problem only

**Trigger:** open rate down while human replies per 1,000 sends hold at the pre-incident baseline, bounces stay under 2% and seeds still reach the inbox.

Placement held and only the open counter moved. Do not cut volume, pause domains or buy anything.

| Check | Finding | Fix |
|-|-|-|
| Tracking CNAME | `dig +short CNAME inst.<domain>` empty or pointing elsewhere (Instantly needs exactly `inst` to `prox.itrackly.com`); a Cloudflare record switched to proxied | Restore the record, DNS-only; re-run the sequencer's check |
| Sequencer setting | Open tracking switched off or moved to a different tracking domain in a campaign edit | Restore, or accept and stop reporting opens |
| Recipient mix | More Apple Mail users (MPP loads remote content for them) or a gateway that fetches every image | Report opens by `sc_mx_provider` and gateway, or drop opens from the report |
| Link tracking | Clicks fell with opens because a gateway rewrites or strips tracked links | Judge by replies; remove links from touch 1 |

**Close when:** the tracking record and setting are confirmed, and the report says opens are excluded or corrected. Replies remain the health signal.

## Incident log fields

| Field | Example |
|-|-|
| Date and time opened | 2026-12-01 10:40 CT |
| Incident type | Bounce spike |
| Scope | Campaign "B - MT/PT", mailboxes marcus@ and elena.ruiz@ on useledgerline.com |
| Trigger value | 3.4% hard bounces over last 200 sends |
| Containment | Campaign paused 10:45 |
| Cause | Batch validated 45 days before send |
| Fix | 640 unsent rows re-validated, 41 invalid removed |
| Resume condition | File 100% valid; mailboxes restart at 10 a day |
| Closed | 2026-12-03 |

## Sources

- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Google, Email sender guidelines, Gmail help copy (spam rate under 0.10%; doubling volume suddenly; stop 10 minutes on `4.7.28`; checked 2026-10-13): https://support.google.com/mail/answer/81126
- Instantly, When your email account is ready for campaigns (2 weeks of warmup, health score above 90%; checked 2026-10-13): https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, Warmup settings (new-account daily warmup limit 10): https://help.instantly.ai/en/articles/7988514-warmup-settings
- Alex Berman, cold email templates (bounces under 2%; start at 10 to 20 a day): https://alexberman.com/cold-email-templates
- Google, Email sender guidelines FAQ (SMTP codes, enforcement timeline): https://support.google.com/a/answer/14229414
- Google Workspace, Gmail SMTP errors and codes (4.7.28 and 5.7.28 texts, checked 2026-10-13): https://knowledge.workspace.google.com/admin/support/troubleshooting/gmail-smtp-errors-and-codes
- Google Workspace, Set up DKIM (Admin console path, 2048-bit, Start authentication; checked 2026-10-13): https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Spamhaus, Domain Blocklist (snowshoeing; reputations begin as poor; checked 2026-10-13): https://www.spamhaus.org/blocklists/domain-blocklist/
- Spamhaus, Two month "snowshoe" trek results (2009): https://www.spamhaus.org/news/article/650/
- Instantly, Custom tracking domain (host `inst`): https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook requirements for high-volume senders (Apr 2025): https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- Mailgun, Microsoft sender requirements summary: https://www.mailgun.com/blog/deliverability/microsoft-sender-requirements/
- Microsoft, Use the delist portal to unblock yourself: https://learn.microsoft.com/en-us/defender-office-365/external-senders-use-the-delist-portal-to-unblock-yourself
- Barracuda Central, Removal request: https://www.barracudacentral.org/rbl/removal-request
- SpamCop, How long do listings last: https://www.spamcop.net/fom-serve/cache/298.html
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Instantly, Webhook events: https://developer.instantly.ai/webhook-events
- Smartlead, Webhook events: https://api.smartlead.ai/api-reference/webhooks/events
- EmailBison, When are webhooks triggered: https://docs.emailbison.com/webhooks/when-are-webhooks-triggered
- ManyReach, Pricing: https://manyreach.com/pricing
