# Framework Notes: Cold Email List

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Size the list from mailboxes and sequence length | `pipeline-runbook.md` section 1 |
| Pick a sourcing path (domains, ICP, URL, CRM export, local) | `pipeline-runbook.md` section 2 |
| Fill empty domains and missing emails | `pipeline-runbook.md` section 3 |
| Dedupe, suppress, cap per company, split waves | `pipeline-runbook.md` sections 4-6 |
| Choose personalization columns | `pipeline-runbook.md` section 7 |
| Map headers for Instantly, Smartlead, Lemlist or EmailBison | `sequencer-import-specs.md` sections 1-3 |
| Set upload options and run the launch checklist | `sequencer-import-specs.md` sections 4-6 |
| Column names, normalization, validation buckets | `references/list-quality-standard.md` (shared) |
| Mailbox provider sender rules | `references/deliverability-primer.md` (shared) |
| Berman's targeting, testing and sequencing guidance | `references/alex-berman-cold-email.md` (shared) |
| Prices and parameters | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### Alex Berman

| Teaching (paraphrased) | Source | Applied here |
|-|-|-|
| Results split 30% targeting, 30% offer, 50% deliverability | alexberman.com | The list owns targeting and protects deliverability: validation, caps, capacity sizing |
| Build the list after the offer; a broad list built first produces generic messaging | alexberman.com, offer article | Step 1 requires the offer and segment before any pull |
| Test about 100 emails per segment, then score segments | Lean B2B interview | Large lists ship in waves; the first wave can be one segment |
| Verify every email; keep bounces under 2% | alexberman.com, cold email templates page | 100% `valid` in the send file |
| Start at the top, move down a level after one to two weeks; do not email several people at a company at once, since that can get you blocked company wide | Single Grain video, Lean B2B interview | Per-company cap the user sets and wave files by contact order |
| Beginner setup: 2 to 3 inboxes per domain, 2 to 4 weeks of warmup, under 50 emails per inbox per day | alexberman.com TAM breakdown | Capacity sizing stays under 50 a day per mailbox; launch checklist warmup |
| Contact each person once per cycle; start a new cycle every 30 to 60 days | alexberman.com TAM breakdown | Reference point for the user's re-contact window |

### Mailbox providers

- Google, Email sender guidelines (requirements from 1 February 2024): spam rate under 0.3%, target under 0.1%; bulk senders authenticate with SPF, DKIM and DMARC and offer one-click unsubscribe, processed within 2 days.
- Yahoo Sender Hub: remove invalid recipients promptly, keep spam rate under 0.3%.
- Microsoft, Outlook high-volume sender requirements (5 May 2025): SPF, DKIM and DMARC for domains sending over 5,000 a day to consumer Outlook domains; list hygiene expected.

Applied: nothing reaches the send file without a `valid` result, and the launch checklist confirms an unsubscribe in every step with removals processed the same day (Google and Yahoo ask bulk senders for one-click unsubscribe processed within 2 days).

### Hunter, email data decay

Hunter's Email Verification Guide (4 November 2025) recommends verifying a list shortly before the campaign. In its test, over 2% of a list went invalid within four weeks and 5.5% within eight. Applied: rows validated more than four weeks before their send date are re-validated, since four weeks of decay alone can reach Berman's 2% bounce line.

### Sequencer import documentation

| Platform | Facts used | Source |
|-|-|-|
| Instantly | Email column is mandatory; headers in the first row, unique, 20 characters or fewer, starting with a capital letter; UTF-8; at most 50 variables per upload; duplicate check across campaigns and lists on by default; optional verification at upload | Instantly help center, upload leads with a CSV |
| Instantly | Recommends 30 campaign emails per account per day; bounce auto-pause at 5% by default, adjustable, checked once a campaign has sent 200 | Instantly help center, account and campaign limits; high bounce auto-pause |
| Smartlead | Auto-maps Name, Email and Location; other columns become custom variables, up to 40 per lead; blank cells mean the value does not appear; import options for the global block list, unsubscribes, bounced leads and leads in other campaigns | Smartlead help center, map CSV columns |
| Lemlist | `email` required and unique; standard names `firstname`, `lastname`, `companyName`, `companyDomain`, `linkedinUrl`, `phone`, `icebreaker` auto-map; custom variable names without spaces; UTF-8 CSV | Lemlist help center, import leads from a CSV |
| EmailBison | Custom variables are created per workspace and mapped during CSV header mapping; examples use `first_name`, `last_name`, `email` | EmailBison docs, custom variables |

### M3AAWG Sender Best Common Practices

Version 3 (February 2015) recommends removing addresses after repeated bounces and treats a list not mailed for a year or more as a dirty list. Applied: bounce suppression, and a full clean with `email-list-cleaner` for CRM exports not mailed in a year.

## Settings and where each number comes from

| Setting | Value | Source |
|-|-|-|
| Sends per mailbox per day | 30 default, always under 50 | Instantly account and campaign limits; Berman TAM breakdown |
| Pull size | Target send-ready rows / the user's measured yield | User input |
| Contacts per company | The user's number, one per wave | User input; Berman for the order |
| Validation age at send | Four weeks or less | Hunter decay test (Nov 2025) against Berman's 2% bounce line |
| Catch-all campaign volume | The user's number, paused past 2% bounces | User input; Berman for the 2% |
| Re-contact window | The user's number | User input; Berman's cycle model runs 30 to 60 days |

## Sources

- https://alexberman.com
- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- https://support.google.com/a/answer/81126
- https://senders.yahooinc.com/best-practices/
- https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- https://hunter.io/email-verification-guide/email-data-decay
- https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://help.instantly.ai/en/articles/6254215-how-to-upload-leads-with-a-csv-file
- https://helpcenter.smartlead.ai/en/articles/409-how-to-map-csv-columns-in-smartlead-campaigns
- https://help.lemlist.com/en/articles/4515109-how-to-import-leads-from-a-csv-file
- https://docs.emailbison.com/leads/custom-variables.md
- https://m3aawg.org/sites/maawg/files/news/M3AAWG_Senders_BCP_Ver3-2015-02.pdf
