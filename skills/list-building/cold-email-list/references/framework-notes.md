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
| Mailbox limits, catch-all cap, bounce stop lines | `references/deliverability-primer.md` (shared) |
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
| Start at the top, move down a level after one to two weeks; do not email several people at a company at once | Single Grain video, Lean B2B interview | Per-company cap of 3 and wave files by contact order |
| Beginner setup: 2 to 3 inboxes per domain, under 50 emails per inbox per day | alexberman.com TAM breakdown | Capacity sizing uses 30 a day per mailbox, never over 50 |

### Mailbox providers

- Google, Email sender guidelines (requirements from 1 February 2024): spam rate under 0.3%, target under 0.1%; bulk senders authenticate with SPF, DKIM and DMARC.
- Yahoo Sender Hub: remove invalid recipients promptly, keep spam rate under 0.3%.
- Microsoft, Outlook high-volume sender requirements (5 May 2025): SPF, DKIM and DMARC for domains sending over 5,000 a day to consumer Outlook domains; list hygiene expected.

Applied: nothing reaches the send file without a `valid` result from the last 30 days.

### FTC, CAN-SPAM

No exemption for business email; honest From, To and routing information; subject lines that match the content; a physical postal address; a clear opt-out honored within 10 business days. Applied: suppression runs before validation, and the launch checklist confirms the opt-out line and address.

### Sequencer import documentation

| Platform | Facts used | Source |
|-|-|-|
| Instantly | Email column is mandatory; headers in the first row, unique, 20 characters or fewer, starting with a capital letter; UTF-8; at most 50 variables per upload; duplicate check across campaigns and lists on by default; optional verification at upload | Instantly help center, upload leads with a CSV |
| Smartlead | Auto-maps Name, Email and Location; other columns become custom variables, up to 40 per lead; blank cells mean the value does not appear; import options for the global block list, unsubscribes, bounced leads and leads in other campaigns | Smartlead help center, map CSV columns |
| Lemlist | `email` required and unique; standard names `firstname`, `lastname`, `companyName`, `companyDomain`, `linkedinUrl`, `phone`, `icebreaker` auto-map; custom variable names without spaces; UTF-8 CSV | Lemlist help center, import leads from a CSV |
| EmailBison | Custom variables are created per workspace and mapped during CSV header mapping; examples use `first_name`, `last_name`, `email` | EmailBison docs, custom variables |

### M3AAWG Sender Best Common Practices

Version 3 (February 2015) recommends removing addresses after repeated bounces and treats a list not mailed for a year or more as a dirty list. Applied: the 30-day validation window and bounce suppression.

## House standards used here (2026-10)

| Standard | Value |
|-|-|
| Sends per mailbox per day | 30, never over 50 |
| Pull size | Target send-ready rows / 0.75 |
| Contacts per company | 3, one per wave |
| Validation age at send | 30 days or less |
| Catch-all share of daily volume | 10% or less |
| Re-contact window | 90 days since the last cold sequence |

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
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://help.instantly.ai/en/articles/6254215-how-to-upload-leads-with-a-csv-file
- https://helpcenter.smartlead.ai/en/articles/409-how-to-map-csv-columns-in-smartlead-campaigns
- https://help.lemlist.com/en/articles/4515109-how-to-import-leads-from-a-csv-file
- https://docs.emailbison.com/leads/custom-variables.md
- https://m3aawg.org/sites/maawg/files/news/M3AAWG_Senders_BCP_Ver3-2015-02.pdf
