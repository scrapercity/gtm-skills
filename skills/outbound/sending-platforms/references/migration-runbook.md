# Sequencer Migration Runbook

How to move cold email from one sequencer to another without mailing anyone twice, losing an unsubscribe, or throwing away mailbox history. Vendor export paths were read from each help center on 2026-10-13. Each threshold names its source; windows no source fixes are the user's settings.

Use this runbook only when the user has named the tool they send from today. With no named tool, there is nothing to migrate: the plan leaves out its Migration Plan section and the new tool's first send follows the plan's Test Plan.

The principle: reputation lives with the domains and mailboxes, not with the tool. A migration moves the same mailboxes to a new tool and leaves every prospect's sequence on the tool that started it.

## 1. Pre-commitment trial (before any annual plan or live campaign moves)

Prove the new tool on a domain you can afford to lose before it touches the warmed mailboxes.

| Step | What | Pass when |
|-|-|-|
| 1 | Pick a test domain: a reserve from `domain-infrastructure`, or one new domain with 2 to 3 mailboxes (Alex Berman's inboxes per domain) | The domain has never sent cold email from the old tool |
| 2 | Connect only those mailboxes to the new tool; warmup on in the new tool for at least 2 weeks, settings from `inbox-setup` (`warmup-and-ramp.md` section 4) | Health score above 90% after at least 2 weeks (Instantly's readiness rule) or the tool's equivalent |
| 3 | Seed placement test from the new tool: live touch 1 copy, seeds at Gmail, Google Workspace, Outlook.com, Microsoft 365 and Yahoo (`email-deliverability` monitoring section 3) | Inbox at every seed provider on two tests run on different days |
| 4 | Import a small sample of the live list with the planned column map into a paused campaign | Row count reconciles; previews render with no raw `{{` and no "Hi ,"; block list honored |
| 5 | Fire a test reply, a test unsubscribe and a test bounce through the webhooks | The CRM updates once per event; the unsubscribe reaches every block list |
| 6 | Read the raw headers of a test message | `List-Unsubscribe` present; `dkim=pass` for the sending domain |
| 7 | Decide | All six pass: migrate. Any fail: fix and repeat that step, or stop and stay on the old tool |

Trial length: at least 2 weeks of warmup (Instantly) plus the days the two seed tests and the webhook tests take. Pay monthly during the trial; annual billing waits until the migration is complete. After the trial the test domain joins the reserve pool.

## 2. Inventory and export from the old tool

Export everything before changing anything. Write each file's row count in the migration log.

| Item | Why | Instantly (help center, 2026-10-13) | Woodpecker (help center, 2026-10-13) | Mailshake (docs, 2026-10-13) |
|-|-|-|-|-|
| All leads or prospects with status | Who is mid-sequence, finished, replied, bounced | Leads > All Leads, select all, Row actions > Download selected (CSV) | Prospects, select, More actions > export; filter by status (Sent, Opened, Bounced, Responded, Active) first | Campaigns, select up to 20, Export > Prospects, Download CSV |
| Block list and unsubscribes | Never mail an opt-out again | Settings > Blocklist, select all, Download CSV | Company settings > Safety, select, Export to CSV | Prospects > Unsubscribes > Export |
| Sequences and copy | Rebuild in the new tool | No CSV export; Campaign API endpoint or a campaign share link | Not exportable: copy steps by hand | Copy steps by hand |
| Replies | Context for open conversations | No bulk export in the interface; Email API endpoint | Not exportable as CSV; replies remain in the mailbox | Read in the mailbox |
| Email accounts list | Which mailboxes to reconnect | Email Accounts, select, Download CSV | Read from the account settings screen | Read from the account settings screen |
| Webhooks and integrations | Rebuild in the new tool | Settings > Integrations | Integration settings | Integration settings |
| Custom tracking domain | Re-point in step 6 | Host and target per account (Instantly uses host `inst`, target `prox.itrackly.com`) | Read from settings | Read from settings |

Replies stay in the mailboxes themselves, which is one more reason to keep the same mailboxes.

## 3. Let mid-sequence prospects finish on the old tool

| Rule | How |
|-|-|
| Cutover date T | From T, no new prospect enters the old tool |
| Prospects already mid-sequence | Finish on the old tool. Moving them would restart the sequence or break the thread, because follow-ups must come from the mailbox and thread that sent step 1 |
| Finish date | T + the longest remaining sequence length. A 3-step sequence over 10 days means the old tool runs about 2 weeks after T |
| Suppress in the new tool | Upload every old-tool prospect (active, finished, replied, bounced, unsubscribed) to the new tool's block list or skip list before the first import, so no prospect gets a second first touch |
| Cooling period | Finished, non-replying prospects stay out of the new tool for the user's re-contact gap (Alex Berman waits 30 to 60 days between cycles) before any re-engagement campaign |

## 4. Rebuild the sequences

1. Copy each step's subject and body from the old tool, one campaign at a time.
2. Translate merge tags to the new tool's syntax (`references/csv-mapping-and-import.md` section 2) and rename CSV headers to match.
3. Re-enter schedules, time zones, per-mailbox and campaign limits, stop on reply, open tracking off, link tracking off unless a verified tracking domain exists, and the unsubscribe header setting.
4. Preview renders for each campaign, including rows that use fallbacks.
5. Leave every new campaign paused until step 7.

## 5. Reconnect the same mailboxes

| Rule | Why |
|-|-|
| Connect the existing, warmed mailboxes by OAuth; create no new mailboxes for the migration | The history Google, Microsoft and the blocklists see belongs to the domain and mailbox |
| One warmup pool at a time: turn warmup on in the new tool and off in the old tool on the same day | Two pools double the warmup volume and the daily count |
| Split the daily cap during the overlap: old-tool limit + new-tool limit for each mailbox stays at or under its `inbox-setup` cap | Two tools do not see each other's sends |
| Keep display names, signatures and photos unchanged | The recipient's thread looks the same |

## 6. Re-point the tracking CNAME

Open and link tracking go through a custom tracking host on each sending domain. The CNAME points at one tool's tracking server.

1. Set a cut-off date after the old tool's last send; links in mail already delivered resolve through the old host until then.
2. If the old and new hosts share a name, re-point on the cut-off date.
3. If the names differ (for example the new tool's `inst` host for Instantly), add the new CNAME now, DNS-only (gray cloud on Cloudflare), verify it in the new tool, and remove the old one on the cut-off date.
4. Never leave a tracking host pointing at a tool you no longer pay for: links in delivered mail stop working for the reader, and so does any unsubscribe link that rides on the same host.

## 7. Run in parallel

| Day | Old tool | New tool |
|-|-|-|
| T | No new prospects; mid-sequence prospects continue at the split cap | First campaign starts at the split cap, after a seed test |
| T to finish date | Finishes sequences | Ramps to the split cap; compare bounce rate per mailbox, positive replies per 1,000 sends and seed placement against the same mailboxes' numbers on the old tool before T |
| Finish date | 0 active prospects | Full cap from the next day |

Stop the migration and send new prospects back through the old tool if, during the overlap, the new tool's hard bounces pass 2% over 200 sends (Alex Berman's line, Instantly's window) or a seed test shows spam at any provider. Investigate before trying again.

## 8. Decommission the old tool

- [ ] 0 active prospects in every old-tool campaign
- [ ] Final export of prospects with status, unsubscribes and bounces, merged into the new tool's block list and the CRM
- [ ] Webhooks and integrations in the old tool turned off
- [ ] Every mailbox disconnected from the old tool, and its OAuth grant revoked in the Google or Microsoft account security settings
- [ ] Old tracking CNAMEs removed on the cut-off date
- [ ] Plan cancelled at the next billing date; invoices downloaded
- [ ] Export archive kept

## 9. Timeline template

| Date | Step |
|-|-|
| T minus the trial length | Trial starts on the test domain |
| After the second seed test | Trial decision |
| Before T | Exports, suppression upload, sequence rebuild |
| Day before T | Mailboxes connected to the new tool, warmup switched over, caps split |
| Day 0 (T) | New campaigns start; old tool takes no new prospects |
| T + longest remaining sequence | Old tool at 0 active prospects |
| Finish + 1 | New tool at full cap; decommission checklist |
| Cut-off date | Old tracking CNAMEs removed |

## Sources

- Instantly, How to export data from your Instantly account: https://help.instantly.ai/en/articles/13924078-how-to-export-data-from-your-instantly-account
- Instantly, Custom tracking domain: https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Instantly, High bounce auto-pause (200-send window): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Alex Berman, TAM strategy breakdown (2 to 3 inboxes per domain; 30 to 60 days between cycles; checked 2026-10-13): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Alex Berman, cold email templates (bounces under 2%): https://alexberman.com/cold-email-templates
- Woodpecker, Exporting data from Woodpecker: https://woodpecker.co/help-center/en/articles/5241827-exporting-data-from-woodpecker
- Mailshake, How do I export my prospects or campaign results: https://docs.mailshake.com/article/119-how-do-i-export-my-campaign-results
- Mailshake, Can I export my unsubscribe list: https://docs.mailshake.com/article/309-how-can-i-export-my-unsubscribe-list
