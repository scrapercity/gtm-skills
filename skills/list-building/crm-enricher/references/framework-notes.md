# Framework Notes: CRM Enricher

Which sources shape this skill, what each contributes, and which file to open for which job.

## Routing table

| You are about to | Open |
|-|-|
| Profile an export and count identifiers | `SKILL.md` step 1, then `enrichment-runbook.md` section 1 |
| Decide what may overwrite what | `field-precedence-and-overwrite-rules.md` |
| Score a Lead Database match, spot a job change | `field-precedence-and-overwrite-rules.md` sections 4 and 5 |
| Pick import mode and map columns for a CRM | `crm-import-mapping.md` |
| Batch lookups, page the database, loop over REST, pilot a hit rate | `enrichment-runbook.md` |
| Write a reason code for an unfilled field | `enrichment-runbook.md` section 6 |
| Write the report's How to Run It | `api-pipeline-and-sync.md` section 5, compact version |
| Order lookups per field, cap spend per row and per month, cut a weak step, pick a plan | `waterfall-and-cost-control.md` |
| Add technographic flags | `waterfall-and-cost-control.md` section 6 |
| Schedule enrichment on CRM events, re-run safely, monitor, set the refresh cadence | `api-pipeline-and-sync.md` |
| Build the send-gate view or create new contacts without duplicates | `api-pipeline-and-sync.md` sections 6 and 8 |
| Normalize names, emails, phones, domains | `references/list-quality-standard.md` section 3 (shared) |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |

## Sources and what each contributes

### DAMA UK data quality dimensions

The UK Government Data Quality Hub recommends six dimensions drawn from DAMA UK: accuracy, completeness, uniqueness, consistency, timeliness and validity. This skill reports against four of them:

| Dimension | How the report measures it |
|-|-|
| Completeness | Fill rate per field, before and after |
| Validity | E.164 phones, `email_status` buckets, domains that resolve to the registrable domain |
| Timeliness | `enriched_at`, `email_validated_at` (90 days for the send gate), and the title freshness window from the rule sheet |
| Uniqueness | Duplicate CRM records flagged `DUPLICATE_IN_CRM` (not merged by this skill) |

Accuracy and consistency are protected by the overwrite policies: the skill does not claim a database value is more accurate than a value a rep entered, so it stages conflicts for review instead of guessing.

### CRM vendors' import documentation

Each CRM decides how a row in your file finds an existing record and whether a blank cell erases data. These rules drive the write-back design:

- HubSpot: Record ID overrides every other identifier; contacts otherwise match on email and companies on Company Domain Name; modes are create and update, create new only, update existing only; each mapped property has a "Don't overwrite" checkbox.
- Pipedrive: a person merges with an existing person when the name is recognized and organization, phone or email also matches, and the import adds new data to the record; organizations merge on address; the merge step can be bypassed.
- HighLevel (GoHighLevel): Update or Create and Update; match order Contact ID, then email, then phone; a "Don't update Empty Values" checkbox; phones should have spaces, dashes and letters removed.
- Salesforce: the Data Import Wizard can add, update, or add and update, matching on Salesforce ID, name or email; for accounts it fills only empty fields unless "Overwrite existing account values" is ticked, and blank imported values do not erase data. Data Loader's "Insert null values" setting writes blanks as nulls and overwrites existing data on update. REST upsert by external ID updates one match, creates on no match, and fails with HTTP 300 on multiple matches.

Applied rule: update-only imports keyed on the CRM record ID, untouched columns removed from the file, and "don't overwrite" or "don't update empty values" switched on wherever the CRM offers it.

### ZeroBounce, verification frequency and list decay

ZeroBounce's FAQ tells senders to verify an email list at least once per quarter. Its Email List Decay Report for 2026 (2025 data) found at least 23% of an email list decays within a year. Applied rule: the send gate admits only emails validated in the last 90 days, and the refresh schedule re-validates anything older before a send.

### US Bureau of Labor Statistics, Employee Tenure (January 2026)

Median employee tenure was 4.1 years. Spread evenly, about 1.4% of contacts change employer each month. Applied rule: together with the ZeroBounce figure this brackets a planning decay of 1.3% to 2.3% a month, which sets the expected job-change count per sweep. Measure the team's own rate on each refresh and replace the planning range.

### Alex Berman and Instantly, the bounce line for the catch-all lane

Alex Berman's cold email templates page says to keep the bounce rate under 2%. Instantly's high bounce auto-pause runs its check once a campaign has sent at least 200 emails (default pause at 5%, adjustable). Applied rule: catch-all addresses wait in their own lane until the main campaign's first 200 sends bounce under 2%, and the lane pauses past 2%. The report names both sources on the line that uses the numbers.

### Lead Database seniority and department

The platform file lists title, seniority and department on every Lead Database person record. Applied rule: high matches fill `seniority` and `department`, and the mobile scope is filtered on them to the levels and departments the user says reps will dial.

### Suppression flags

Rows with an unsubscribe, opt-out or DND flag are skipped and flagged `SUPPRESSED`. Enrichment never refills an email a person asked you to stop using, because a refilled address re-enters sequences and drives spam complaints, which Google's sender guidelines tie to inbox placement.

### Alex Berman, narrow and current lists

Alex Berman's companies have booked 500k+ meetings. His site tells senders to verify every email before sending and aim for 95%+ valid, and to build the list after the offer for one tight niche. Applied here as a cost rule: enrich the segment reps will work next (open opportunities, target accounts) before the long tail, and spend mobile dollars only where a rep will dial.

## What this skill does not do

- Merge duplicate CRM records. Flag them and use the CRM's merge tool so activity history moves with the record.
- Infer emails from a naming pattern without verification. Email Finder results are validated at lookup time per its tool description; guessed patterns are not.
- Change owner, lifecycle stage, lead status, subscription status or opt-out fields.

## Sources

- UK Government Data Quality Hub, Meet the data quality dimensions (2021): https://www.gov.uk/government/news/meet-the-data-quality-dimensions
- HubSpot, Import records for a single object: https://knowledge.hubspot.com/import-and-export/import-records-for-a-single-object
- Pipedrive, How to avoid duplicates during an import: https://support.pipedrive.com/en/article/how-to-avoid-duplicates-during-an-import
- HighLevel, Importing contacts using a CSV file: https://help.gohighlevel.com/support/solutions/articles/155000004432-importing-contacts
- Salesforce, Import data with the Data Import Wizard: https://help.salesforce.com/s/articleView?id=sf.import_with_data_import_wizard.htm&type=5
- Salesforce, Import cheat sheet (matching and overwrite rules): https://resources.docs.salesforce.com/206/latest/en-us/sfdc/pdf/salesforce_import_cheatsheet.pdf
- Salesforce, Data Loader settings: https://developer.salesforce.com/docs/atlas.en-us.dataLoader.meta/dataLoader/configuring_the_data_loader.htm
- Salesforce, Upsert a record using an external ID: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api/dome_upsert.htm
- ZeroBounce, How often should I verify my email list: https://zerobounce.net/docs/frequently-asked-questions/account/how-often-should-I-verify-my-email-list
- ZeroBounce, Email List Decay Report for 2026: https://zerobounce.net/email-list-decay
- US Bureau of Labor Statistics, Employee Tenure (January 2026): https://www.bls.gov/news.release/tenure.nr0.htm
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Alex Berman, Cold email templates (keep bounces under 2%): https://alexberman.com/cold-email-templates
- Instantly, High bounce auto-pause feature: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Alex Berman, B2B lead generation: https://alexberman.com/b2b-lead-generation
