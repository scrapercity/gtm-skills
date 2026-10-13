# Framework Notes: ICP List Builder

Which sources shape this skill, what each one contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Turn example customers into filters | `SKILL.md` step 1, then `icp-filter-recipes.md` |
| Write the `title` and `notTitle` strings | `title-synonyms-and-exclusions.md` |
| Decide whether a count is too big or too small, page the results, handle a 503 | `count-and-paging-runbook.md` |
| Name columns, normalize, dedupe, bucket validation results | `references/list-quality-standard.md` (shared) |
| Quote a price or a parameter | `references/scrapercity-catalog.md` (shared) |
| Check plan access or the daily allowance | `references/scrapercity-platform.md` (shared) |
| Check country rules before sending | `references/outbound-compliance-primer.md` (shared) |

## Sources and what each contributes

### April Dunford, best-fit customers

Dunford's positioning method starts from the customers who understood the product quickly, bought it and got strong value, then asks what those accounts share. This skill applies the same move to list building: the example customers are best-fit accounts, and only traits shared by 3 or more of them become filters. One unusual customer never sets a filter.

Applied rule: ask the user for the 3-5 customers who closed fastest and renewed or expanded, not the biggest logos.

### Gartner, buying groups

Gartner's B2B buying research describes a typical buying group for a complex solution as 6 to 10 decision makers. For list building that means one title per account under-covers the decision. The skill pulls up to 3 roles per account (economic buyer, day-to-day owner, and a user lead or technical evaluator) and caps there to keep complaint risk down.

Applied rule: the per-domain cap is 3, chosen by seniority then title closeness.

### Alex Berman, narrow lists

Alex Berman's companies have booked 500k+ meetings. A secondhand account of his early agency work describes a campaign aimed at about 50 universities that resembled one case study, which led to meetings at Yale, UCLA and Ohio State. The principle used here: the closer the list is to the case study the email cites, the better it converts, so a smaller tight list beats a large loose one.

Applied rule: when the count is more than 10x the target, tighten instead of pulling the top N.

### Mailbox providers: Google, Yahoo, Microsoft

- Google (bulk sender rules announced October 2023, enforced from February 2024): senders above 5,000 messages a day to Gmail must authenticate, offer one-click unsubscribe processed within two days, and stay under a spam rate threshold. Google's guidance targets under 0.1% and never reaching 0.3%.
- Yahoo Sender Hub: remove invalid recipients promptly, monitor bounces, keep spam rate below 0.3%.
- Microsoft Outlook (enforced May 5, 2025 for senders over 5,000 a day): SPF, DKIM and DMARC required; list hygiene and removing invalid addresses listed among the practices it expects.

Applied rule: nothing reaches the main CSV without `validate_emails` returning valid within 30 days.

### FTC, CAN-SPAM

The FTC guide states the law has no exception for business-to-business email and that opt-outs must be honored within 10 business days. Applied rule: suppression runs before validation and before delivery, and the report states which suppression files were applied.

### Sequencer bounce guards

Instantly pauses a campaign whose bounce rate exceeds 5% after 200 sends by default. Smartlead lets the user set a pause threshold. Applied rule: the list targets a projected bounce rate under 2%, well clear of those pause lines.

### Bureau of Labor Statistics, tenure

Median employee tenure was 4.1 years in January 2026. Applied rule: a contact list ages; re-validate before any send more than 30 days after `email_validated_at`.

## What this skill does not use

- Intent data or website visitor tracking. Use `signal-triggered-outbound` for event-driven lists.
- Scoring models. The ICP here is a filter set, not a weighted score; scoring belongs after the list exists.

## Sources

- April Dunford, A quickstart guide to positioning: https://www.aprildunford.com/post/a-quickstart-guide-to-positioning
- Gartner, The B2B buying journey: https://www.gartner.com/en/sales/insights/b2b-buying-journey
- Hackernoon, Cold Email is not Dead (Scott D. Clary on Alex Berman): https://hackernoon.com/cold-email-is-not-dead-mb4v35g4
- Google, Gmail sender requirements announcement: https://blog.google/products/gmail/gmail-security-authentication-spam-protection/
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo Sender Hub, Best practices: https://senders.yahooinc.com/best-practices/
- Microsoft, Outlook high-volume sender requirements: https://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Smartlead, High bounce rate auto protection: https://helpcenter.smartlead.ai/en/articles/274-what-is-high-bounce-rate-auto-protection-in-smartlead
- BLS, Employee Tenure news release: https://www.bls.gov/news.release/tenure.nr0.htm
