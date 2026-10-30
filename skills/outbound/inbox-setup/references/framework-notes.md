# Framework Notes: Inbox Setup

Which sources shape this skill, what each one contributes, where the skill relaxes or tightens a source, and which file to open for which question. Facts were checked on 2026-10-12 and re-checked on 2026-10-13.

## Sources and what they contribute

| Source | Type | Contribution to this skill | Where it shows up |
|-|-|-|-|
| Google Email sender guidelines (support.google.com/a/answer/81126), FAQ (/14229414) and Top 10 Gmail sender issues (/mail/answer/15256272) | Mailbox provider rule | Raise volume slowly and avoid spikes; keep spam rate below 0.1% and never at 0.3%; daily increases of 25% to 100% are common after a deferral; honor unsubscribes within 48 hours | Ramp shape, pause triggers |
| Yahoo Sender Hub best practices | Mailbox provider rule | Spam rate under 0.3%; process unsubscribes within 2 days; remove invalid addresses promptly | Retirement triggers, list feed |
| M3AAWG Sender Best Common Practices v4.0 (Aug 2026) | Industry body | Start low, ramp over about six weeks, spread sends through the day; flags volume jumps as a monitoring signal; does not recommend artificial warming | Ramp length, pacing, the caveat on pool warmup |
| Instantly help center (warmup settings, readiness, account limits, slow ramp, bounce auto-pause) | Sequencer doc | Ready after 2 weeks of warmup and a health score above 90%, 3 weeks for AirMail accounts; new-account warmup defaults (+1 a day, limit 10, reply rate 30%); 30 campaign emails a day per account; slow ramp from 2 a day, +2 a day, 30 on day 15; campaigns auto-pause at 5% bounces after 200 sends | Warmup settings table, the 14- and 21-day paths, the ramp, the cap of 30, the bounce pause line |
| Instantly Inbox Placement (feature and one-time tests) | Sequencer doc | Placement tests at Gmail and Microsoft, two free one-time tests, under Email Accounts > Deliverability Tests | The go-live placement gate and the Rest return test |
| Google Workspace DNS and Postmaster Tools help (MX, SPF, DKIM, DMARC, Postmaster set-up) and Microsoft Learn (SPF, DKIM) | Mailbox provider doc | Exact record values; DKIM 24 to 72 hours after Gmail is on; DMARC starts at `p=none`; Postmaster Tools needs a verified domain | DNS record table, setup schedule |
| Smartlead help center (warmup, daily ramp up) | Sequencer doc | Warmup of 10 to 20 a day while campaigns run, reply rate 20 to 30%; enable daily ramp up when warmup starts | Smartlead settings table |
| Apollo knowledge base (sending limits) | Sequencer doc | 50 to 100 a day per mailbox, 10 to 20 an hour, 60 to 300 seconds apart; ramp-up uses the lower of two limits | Hourly cap and gap between sends |
| HubSpot knowledge base (sales email send limits) | Sequencer doc | Sequences: 500 a day per Professional seat, 1,000 per Enterprise seat; no warmup feature | HubSpot row in the per-sequencer table |
| Google Workspace and Microsoft 365 admin docs | Mailbox provider doc | Workspace 2,000 messages per user per day (500 on trial); Exchange Online 10,000 recipients a day and 30 messages a minute; auto-forward rules | Why provider limits never bind; forwarding option |
| Spamhaus Domain Blocklist | Blocklist operator | Unknown reputations begin as poor; snowshoeing is a technique using many domains and IPs that change often, and domains acting like it get treated like it | Keep retired domains registered; replace one for one after the cause is found |
| Alex Berman (alexberman.com) | Operator | Warm up 2 to 4 weeks; start new domains at 10 to 20 a day; under 50 a day per inbox; 2 to 3 inboxes per domain; bounces above 2% hurt and above 5% are critical; click tracking wraps every link in a redirect | Ramp start, ceiling of 50, bounce lines, signature links |
| Growth Engine X (coldoutbound.com) | Operator | Backup domains always warming; 1,500 a day of capacity for a 1,000 goal | Reserves |
| Microsoft 365 Message Center MC1454397 and MC786329 | Vendor notice | New tenants get 10% of the external recipient quota for 30 days and 25% to day 60, trials 500 a day; Basic SMTP AUTH off by default after December 2026 | Standard path for new tenants, tenant quota check, OAuth connection |
| Microsoft Learn, Configure outbound spam policies | Vendor doc | Per-user hourly and daily recipient limits, restriction on breach, forwarding control | Microsoft account settings row |
| ScraperCity catalog and platform files | Tool facts | `validate_emails` at $0.00169 per email; Lead Database included on Growth with 100,000 new leads a day | List feed sized to the ramp |

## Where sources differ

| Topic | Sources | This skill uses |
|-|-|-|
| Daily cap | Instantly: 30. Alex Berman: under 50. Smartlead: max 50. Apollo: 50 to 100 | 30, ceiling 50 |
| Opt-out speed | Google 48 hours; Yahoo 2 days | The same day, which meets both |
| Warmup length | Instantly 2 weeks minimum, 3 for AirMail accounts; Alex Berman 2 to 4 weeks; M3AAWG about 6 weeks for permission mail | 21 days standard, 14 days as the soft-start floor, then Instantly's slow ramp to 30 on sending day 15 |
| Ramp start | Alex Berman: 10 to 20 a day. Instantly slow ramp: 2 on day 1 | Instantly's slow ramp, which passes 10 on sending day 5 |
| Reply-To | Sequencers allow any Reply-To | No Reply-To elsewhere, so replies reach the sequencer and stop the sequence |

## What this skill does not claim

- No source publishes an inbox placement rate for a given ramp. The ramp is a starting schedule to test against bounce, complaint and reply data.
- Sending days and hours, reply check times, the reply response target, the reserve share and the pass line for any raise above 30 are user inputs; no source cited here publishes them for cold email.
- Pool warmup is a sequencer feature that M3AAWG does not recommend. The skill uses it for early history and judges mailbox health by prospect replies.

## Routing table

| Question | Open |
|-|-|
| Who can be the sender, and what name and address format? | `references/mailbox-setup-runbook.md` sections 1 and 2 |
| What goes in the signature? | `references/mailbox-setup-runbook.md` section 3 |
| Photo, 2-Step Verification, OAuth connection | `references/mailbox-setup-runbook.md` section 4 |
| Where do replies go? | `references/mailbox-setup-runbook.md` sections 5 and 7 |
| Exact DNS record values, Postmaster Tools set-up | `references/mailbox-setup-runbook.md` section 4a |
| What warmup settings do I enter in my sequencer? | `references/warmup-and-ramp.md` section 4 |
| When does a mailbox move to the next cap? | `references/warmup-and-ramp.md` sections 2 and 6 |
| Can I raise this mailbox above 30 a day? | `references/warmup-and-ramp.md` section 8 |
| Can a burned mailbox be brought back? | `references/warmup-and-ramp.md` section 9 |
| Standard path or soft start? Microsoft tenant quota? | `references/warmup-and-ramp.md` section 2 |
| What can we set on mailboxes a reseller built? | `references/mailbox-setup-runbook.md` section 8 |
| Sending window and pacing | `references/warmup-and-ramp.md` section 5 |
| How are mailboxes grouped per campaign? | `references/rotation-and-retirement.md` sections 1 and 2 |
| When do I pause, rest or retire a mailbox? | `references/rotation-and-retirement.md` sections 3 and 4 |
| How many reserves, and when to buy more? | `references/rotation-and-retirement.md` section 5 |
| Provider rules and standing thresholds | `references/deliverability-primer.md` |
| Price of validation | `references/scrapercity-catalog.md` |

## Sources

- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://www.m3aawg.org/sites/default/files/doc_files/m3aawg-sender-best-common-practices-aug-27-2026.pdf
- https://help.instantly.ai/en/articles/7988514-warmup-settings
- https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- https://helpcenter.smartlead.ai/en/articles/52-how-to-enable-ai-email-account-warm-ups
- https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- https://knowledge.hubspot.com/connected-email/sales-email-send-limits
- https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace
- https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- https://www.spamhaus.org/blocklists/domain-blocklist/
- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://mc.merill.net/message/MC1454397
- https://mc.merill.net/message/MC786329
- https://help.instantly.ai/en/articles/10056946-campaign-slow-ramp-system
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://support.google.com/mail/answer/15256272
- https://alexberman.com/custom-tracking-domain-gmail
- https://coldoutbound.com/
- https://help.instantly.ai/articles/10147177-inbox-placement-feature
- https://help.instantly.ai/en/articles/10258203-inbox-placement-one-time-tests
- https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace
- https://knowledge.workspace.google.com/admin/security/set-up-spf
- https://knowledge.workspace.google.com/admin/security/set-up-dkim
- https://knowledge.workspace.google.com/admin/security/set-up-dmarc
- https://support.google.com/a/answer/9981691
- https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure
- https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
- https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-policies-configure
