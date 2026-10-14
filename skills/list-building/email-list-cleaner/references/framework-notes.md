# Framework Notes: Email List Cleaner

Which named sources shape this skill, what each one contributes, and which file to open for which job.

## Sources and what each contributes

| Source | Date | What it contributes | Where it shows up |
|-|-|-|-|
| Google, Email sender guidelines | Requirements from 1 Feb 2024 | Spam rate in Postmaster Tools kept below 0.3%, target below 0.1%. Bulk senders (over 5,000 a day to Gmail) need SPF, DKIM, DMARC and one-click unsubscribe processed within 2 days. A dirty list raises bounces and complaints together. | SKILL.md Foundations |
| Yahoo Sender Hub, Best practices | Feb 2024 | Remove invalid recipients promptly; track bounces and inactive recipients; honor unsubscribes within 2 days. | Suppression additions; removed.csv |
| Microsoft, Outlook high-volume sender requirements | Effective 5 May 2025 | For senders over 5,000 a day to Outlook.com, Hotmail.com and Live.com: SPF, DKIM, DMARC; list hygiene that removes invalid contacts, and bounce monitoring. | Foundations; why invalids are blocklisted |
| M3AAWG Sender Best Common Practices v3 (Feb 2015) | 2015 | Remove addresses that bounce consecutively at least two times over two weeks or more; treat "no such user" as permanent; not mailing a list for a year or more marks it as dirty. | Risk tiers; bounce suppression rule |
| IETF RFC 2142, Mailbox names for common services | May 1997 | Defines business role mailboxes (info, marketing, sales, support) and network-operations mailboxes (abuse, noc, security) plus service names (postmaster, hostmaster, webmaster). | Role flag; network-role removal |
| IETF RFC 6647, Email greylisting | June 2012 | Greylisting servers temporarily reject a first delivery attempt and accept a later retry. | One later retry for `unknown` results |
| Hunter, Email verification guide: email data decay | 4 Nov 2025 | Verify shortly before a campaign. In Hunter's test, over 2% of a list went invalid within four weeks and 5.5% within eight. | Four-week re-validation window; tier A |
| Alex Berman, Cold email templates | Current page | Verify every email before sending; keep bounces under 2%. | Bounce stop line on every send plan |
| Instantly help center, High bounce auto-pause | Current page | Campaigns pause when the bounce rate exceeds 5% (default, adjustable); the check runs once a campaign has sent at least 200 emails. | Auto-pause setting; 200 sends as the first read on a test batch |
| Smartlead help center, bounce auto protection | Current page | User-set bounce threshold pauses the campaign. | Same |
| US Bureau of Labor Statistics, Employee Tenure | January 2026 data | Median employee tenure of 4.1 years. | Decay planning table |
| ZeroBounce, Email List Decay Report | 2026 edition (2025 data, vendor-reported) | At least 23% of an email list decays within a year (28% in the previous edition). | Decay planning table |
| ScraperCity Email Validator page | Checked 2026-10-12 | Five results (valid, valid_catch_all, invalid, unknown, disposable), quality rating high, medium or low, `sc_` enrichment columns including MX provider and security gateway. 99%+ accuracy per scrapercity.com. | Status matrix |
| ScraperCity catalog (npm package 1.0.17) | Generated | `validate_emails` at $0.0072 per email; `find_emails` at $0.05 per email found, free if not found; run lifecycle and error codes. | Every cost line |

## Routing table

| You are doing this | Open |
|-|-|
| Deciding what a validator result means and which file the row goes to | `status-handling-matrix.md` |
| Combining `email_result` with `email_quality`, `free`, role and gateway flags | `status-handling-matrix.md`, section "Combined rules" |
| Fixing malformed addresses, splitting cells, typo domains | `syntax-repair-and-role-rules.md` |
| Deciding whether `info@` or `sales@` stays | `syntax-repair-and-role-rules.md`, role table |
| Planning a large file, chunking, tracking run ids | `batching-and-revalidation-runbook.md` |
| A run failed, was cancelled, or returned fewer rows than sent | `batching-and-revalidation-runbook.md`, failure table |
| Setting the next validation date | `batching-and-revalidation-runbook.md`, cadence table |
| Column names, dedupe keys | `references/list-quality-standard.md` (shared) |
| Mailbox provider sender rules, bounce monitoring | `references/deliverability-primer.md` (shared) |
| Prices and parameters | `references/scrapercity-catalog.md` (shared) |

## How the sources fit together

Mailbox providers (Google, Yahoo, Microsoft) set the outcome a cleaned list must protect: low complaints and few bounces. M3AAWG and RFC 2142 supply the hygiene rules a list operator applies: suppress repeat bouncers, avoid operations mailboxes. Hunter's decay test sets how long a validation result stays usable, and Berman's 2% sets where a send stops. ScraperCity's validator supplies the per-address evidence.

Numbers the sources do not give are user inputs: the size of a tier C test batch, the daily volume of a catch-all campaign, the chunk size for very large files, and the date of the single `unknown` retry. Replace the decay planning range with your own bounce rate by months since validation once you have campaign history.

## Sources

- https://support.google.com/a/answer/81126
- https://senders.yahooinc.com/best-practices
- https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- https://m3aawg.org/sites/maawg/files/news/M3AAWG_Senders_BCP_Ver3-2015-02.pdf
- https://datatracker.ietf.org/doc/rfc2142/
- https://datatracker.ietf.org/doc/html/rfc6647
- https://hunter.io/email-verification-guide/email-data-decay
- https://alexberman.com/cold-email-templates
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- https://www.bls.gov/news.release/tenure.nr0.htm
- https://zerobounce.net/email-list-decay
- https://scrapercity.com/email-validator
