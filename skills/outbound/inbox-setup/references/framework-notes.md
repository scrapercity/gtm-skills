# Framework Notes: Inbox Setup

Which sources shape this skill, what each one contributes, where the skill relaxes or tightens a source, and which file to open for which question. Facts were checked on 2026-10-12 and 2026-10-13.

## Sources and what they contribute

| Source | Type | Contribution to this skill | Where it shows up |
|-|-|-|-|
| FTC, CAN-SPAM Act compliance guide | US regulator | Header information (From, Reply-To, routing) must identify the sender; a valid postal address; a clear opt-out honored within 10 business days; no B2B exception | Real-person rule, signature template, opt-out line |
| Google Email sender guidelines (support.google.com/a/answer/81126) and FAQ (/14229414) | Mailbox provider rule | Raise volume slowly and avoid spikes; keep spam rate under 0.1% and never at 0.3%; honor unsubscribes within 48 hours | Ramp shape, pause triggers |
| Yahoo Sender Hub best practices | Mailbox provider rule | Spam rate under 0.3%; process unsubscribes within 2 days; remove invalid addresses promptly | Retirement triggers, list feed |
| M3AAWG Sender Best Common Practices v4.0 (Aug 2026) | Industry body | Start low, ramp over about six weeks, spread sends through the day; flags volume jumps as a monitoring signal; does not recommend artificial warming | Ramp length, pacing, the caveat on pool warmup |
| Instantly help center (warmup settings, readiness, account limits, slow ramp) | Sequencer doc | Ready after 2 weeks of warmup and a health score above 90%; new-account warmup defaults (+1 a day, limit 10, reply rate 30%); 30 campaign emails a day per account recommended | Warmup settings table, the 14-day gate, the cap of 30 |
| Smartlead help center (warmup, daily ramp up) | Sequencer doc | Warmup of 10 to 20 a day while campaigns run, reply rate 20 to 30%; enable daily ramp up when warmup starts | Smartlead settings table |
| Apollo knowledge base (sending limits) | Sequencer doc | 50 to 100 a day per mailbox, 10 to 20 an hour, 60 to 300 seconds apart; ramp-up uses the lower of two limits | Hourly cap and gap, compared against stricter house numbers |
| HubSpot knowledge base (sales email send limits) | Sequencer doc | Sequences: 500 a day per Professional seat, 1,000 per Enterprise seat; no warmup feature | HubSpot row in the per-sequencer table |
| Google Workspace and Microsoft 365 admin docs | Mailbox provider doc | Workspace 2,000 messages per user per day (500 on trial); Exchange Online 10,000 recipients a day and 30 messages a minute; auto-forward rules | Why provider limits never bind; forwarding option |
| Spamhaus Domain Blocklist | Blocklist operator | New domains start with poor reputation; rotating many domains fast is treated as snowshoeing | Keep retired domains registered; do not churn domains |
| Alex Berman (alexberman.com) | Operator | Warm up 2 to 4 weeks; start new domains at 10 to 20 a day; under 50 a day per inbox; 2 to 3 inboxes per domain | Ramp start, ceiling of 50 |
| ScraperCity catalog and platform files | Tool facts | `validate_emails` at $0.0072 per email; Lead Database included on Growth with 100,000 new leads a day | List feed sized to the ramp |

## Where this skill is stricter than a source

| Topic | Source says | This skill uses | Why |
|-|-|-|-|
| Daily cap | Apollo: 50 to 100 per mailbox | 30, ceiling 50 | Cold email draws more complaints than the mail Apollo's figure was written for; a cap of 30 keeps one mailbox's bad day small |
| Opt-out speed | CAN-SPAM 10 business days; Google 48 hours; Yahoo 2 days | Same day, 24 hours at most | Faster than every rule at once, so one process covers all three |
| Warmup length | Instantly 2 weeks; M3AAWG about 6 weeks | 14 days warmup, then a 4-week cold ramp to 30 | Cold volume reaches 30 a mailbox around day 29, inside M3AAWG's six-week shape |
| Reply-To | CAN-SPAM only requires it to identify the sender | No Reply-To on the main domain | Keeps the cold domain and the main domain apart in headers |

## What this skill does not claim

- No source publishes an inbox placement rate for a given ramp. The ramp is a starting schedule to test against bounce, complaint and reply data.
- Pool warmup is a sequencer feature that M3AAWG does not recommend. The skill uses it for early history and treats real prospect replies as the signal that counts.
- Profile photos are a trust signal for the prospect who opens the email. No mailbox provider documents them as a filtering input.

## Routing table

| Question | Open |
|-|-|
| Who can be the sender, and what name and address format? | `references/mailbox-setup-runbook.md` sections 1 and 2 |
| What goes in the signature? | `references/mailbox-setup-runbook.md` section 3 |
| Photo, 2-Step Verification, OAuth connection | `references/mailbox-setup-runbook.md` section 4 |
| Where do replies go? | `references/mailbox-setup-runbook.md` sections 5 and 7 |
| What warmup settings do I enter in my sequencer? | `references/warmup-and-ramp.md` section 4 |
| When does a mailbox move to the next cap? | `references/warmup-and-ramp.md` sections 2 and 6 |
| Sending window and pacing | `references/warmup-and-ramp.md` section 5 |
| How are mailboxes grouped per campaign? | `references/rotation-and-retirement.md` sections 1 and 2 |
| When do I pause, rest or retire a mailbox? | `references/rotation-and-retirement.md` sections 3 and 4 |
| How many reserves, and when to buy more? | `references/rotation-and-retirement.md` section 5 |
| Provider rules and standing thresholds | `references/deliverability-primer.md` |
| Opt-out law by country | `references/outbound-compliance-primer.md` |
| Price of validation | `references/scrapercity-catalog.md` |

## Sources

- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
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
