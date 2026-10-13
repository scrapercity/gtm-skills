# Framework Notes: Email List Cleaner

Which named sources shape this skill, what each one contributes, and which file to open for which job.

## Sources and what each contributes

| Source | Date | What it contributes | Where it shows up |
|-|-|-|-|
| Google, Email sender guidelines | Requirements from 1 Feb 2024 | Spam rate in Postmaster Tools kept below 0.3%, target below 0.1%. Bulk senders (over 5,000 a day to Gmail) need SPF, DKIM, DMARC and one-click unsubscribe. A dirty list raises bounces and complaints together. | SKILL.md Foundations; projection thresholds |
| Yahoo Sender Hub, Best practices | Feb 2024 | Remove invalid recipients promptly; track bounces and inactive recipients; honor unsubscribes within 2 days. | Suppression additions; removed.csv |
| Microsoft, Outlook high-volume sender requirements | Effective 5 May 2025 | For senders over 5,000 a day to Outlook.com, Hotmail.com and Live.com: SPF, DKIM, DMARC; keep the list clean by removing invalid contacts and monitor bounces. | Foundations; why invalids are blocklisted |
| M3AAWG Sender Best Common Practices v3 (Feb 2015) | 2015 | Remove addresses that bounce consecutively at least two times over two weeks or more; treat "no such user" as permanent; not mailing a list for a year or more marks it as dirty. Recommends a permission pass for implied-consent addresses. | Risk tiers; bounce suppression rule |
| IETF RFC 2142, Mailbox names for common services | May 1997 | Defines business role mailboxes (info, marketing, sales, support) and network-operations mailboxes (abuse, noc, security) plus service names (postmaster, hostmaster, webmaster). | Role flag; network-role removal |
| FTC, CAN-SPAM Act compliance guide | Current page | Honor opt-outs within 10 business days; keep the opt-out working 30 days after a send; never sell or transfer an opted-out address. | Suppression step; never re-import removed rows |
| CRTC, CASL FAQ | Current page | Unsubscribe processed within 10 business days; conspicuous-publication implied consent requires role relevance. | Canada rows in the compliance note |
| Instantly help center, High bounce auto-pause | 2024 | Campaigns pause when the bounce rate exceeds 5% (default, adjustable). | Projection target sits well under it |
| Smartlead help center, bounce auto protection | Current page | User-set bounce threshold pauses the campaign. | Same |
| ScraperCity Email Validator page | Checked 2026-10-12 | Five results (valid, valid_catch_all, invalid, unknown, disposable), quality rating high, medium or low, `sc_` enrichment columns including MX provider and security gateway. 99%+ accuracy per scrapercity.com. | Status matrix |
| ScraperCity catalog (npm package 1.0.17) | Generated | `validate_emails` at $0.0072 per email; `find_emails` at $0.05 per email found, free if not found; run lifecycle and error codes. | Every cost line |

## Routing table

| You are doing this | Open |
|-|-|
| Deciding what a validator result means and which file the row goes to | `status-handling-matrix.md` |
| Combining `email_result` with `email_quality`, `free`, role and gateway flags | `status-handling-matrix.md`, section "Combined rules" |
| Fixing malformed addresses, splitting cells, typo domains | `syntax-repair-and-role-rules.md` |
| Deciding whether `info@` or `sales@` stays | `syntax-repair-and-role-rules.md`, role table |
| Planning a file over 1,000 rows, chunking, tracking run ids | `batching-and-revalidation-runbook.md` |
| A run failed, was cancelled, or returned fewer rows than sent | `batching-and-revalidation-runbook.md`, failure table |
| Setting the next validation date | `batching-and-revalidation-runbook.md`, cadence table |
| Column names, dedupe keys, acceptance thresholds | `references/list-quality-standard.md` (shared) |
| Catch-all volume cap, bounce stop lines, monitoring | `references/deliverability-primer.md` (shared) |
| Opt-out law by country | `references/outbound-compliance-primer.md` (shared) |
| Prices and parameters | `references/scrapercity-catalog.md` (shared) |

## How the sources fit together

Mailbox providers (Google, Yahoo, Microsoft) set the outcome a cleaned list must protect: low complaints and few bounces. M3AAWG and RFC 2142 supply the hygiene rules a list operator applies: suppress repeat bouncers, avoid operations mailboxes. CAN-SPAM and CASL set the floor on suppression: a cleaned list must never resurrect an opt-out. ScraperCity's validator supplies the per-address evidence, and the house standards in `list-quality-standard.md` turn that evidence into routing decisions with numbers attached.

Benchmarks quoted in this skill (the 5% Instantly default, the 2% house bounce target, the 15% invalid-rate source alarm) are starting hypotheses dated 2026-10. Replace them with your own bounce data per list age once you have three or more campaigns of history.

## Sources

- https://support.google.com/a/answer/81126
- https://senders.yahooinc.com/best-practices
- https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- https://m3aawg.org/sites/maawg/files/news/M3AAWG_Senders_BCP_Ver3-2015-02.pdf
- https://datatracker.ietf.org/doc/rfc2142/
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://crtc.gc.ca/eng/com500/faq500.htm
- https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- https://scrapercity.com/email-validator
