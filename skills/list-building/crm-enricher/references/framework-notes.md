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
| Normalize names, emails, phones, domains | `references/list-quality-standard.md` section 3 (shared) |
| Quote a price or parameter | `references/scrapercity-catalog.md` (shared) |
| Check calling and email rules before records feed outreach | `references/outbound-compliance-primer.md` (shared) |

## Sources and what each contributes

### DAMA UK data quality dimensions

The UK Government Data Quality Hub recommends six dimensions drawn from DAMA UK: accuracy, completeness, uniqueness, consistency, timeliness and validity. This skill reports against four of them:

| Dimension | How the report measures it |
|-|-|
| Completeness | Fill rate per field, before and after |
| Validity | E.164 phones, `email_status` buckets, domains that resolve to the registrable domain |
| Timeliness | `enriched_at`, `email_validated_at`, and a 90-day freshness window on titles |
| Uniqueness | Duplicate CRM records flagged `DUPLICATE_IN_CRM` (not merged by this skill) |

Accuracy and consistency are protected by the overwrite policies: the skill does not claim a database value is more accurate than a value a rep entered, so it stages conflicts for review instead of guessing.

### CRM vendors' import documentation

Each CRM decides how a row in your file finds an existing record and whether a blank cell erases data. These rules drive the write-back design:

- HubSpot: Record ID overrides every other identifier; contacts otherwise match on email and companies on Company Domain Name; modes are create and update, create new only, update existing only; each mapped property has a "Don't overwrite" checkbox.
- Pipedrive: a person merges with an existing person when the name is recognized and organization, phone or email also matches, and the import adds new data to the record; organizations merge on address; the merge step can be bypassed.
- HighLevel (GoHighLevel): Update or Create and Update; match order Contact ID, then email, then phone; a "Don't update Empty Values" checkbox; phones should have spaces, dashes and letters removed.
- Salesforce: the Data Import Wizard can add, update, or add and update, matching on Salesforce ID, name or email; for accounts it fills only empty fields unless "Overwrite existing account values" is ticked, and blank imported values do not erase data. Data Loader's "Insert null values" setting writes blanks as nulls and overwrites existing data on update. REST upsert by external ID updates one match, creates on no match, and fails with HTTP 300 on multiple matches.

Applied rule: update-only imports keyed on the CRM record ID, untouched columns removed from the file, and "don't overwrite" or "don't update empty values" switched on wherever the CRM offers it.

### GDPR Articles 5 and 14

Article 5(1)(d) requires personal data to be accurate and, where necessary, kept up to date, which supports replacing an email proven invalid. Article 14 covers data obtained from someone other than the person: the controller tells the person, among other items, the source of the data, within a reasonable period and at the latest within one month, or at the first communication if the data is used to contact them. Applied rule: for EU and UK records, the write-back file sets `enrich_source` per field so the user can answer the source question, and the report reminds the user that the first outreach email to an enriched EU contact needs the Article 14 information.

### TCPA and 47 CFR 64.1200

A mobile number written into a CRM is a wireless number. Autodialed or prerecorded calls and texts to it need prior express consent, and telemarketing robocalls need prior express written consent. Applied rule: found mobiles go only into the mobile field, in E.164, with `enrich_source = mobile_finder`, so a dialer or texting tool can exclude them from automated campaigns. The full calling gate lives in `mobile-appender`.

### FTC CAN-SPAM guide

There is no business-to-business exemption, and opt-outs are honored within 10 business days. Applied rule: rows with an unsubscribe, opt-out or DND flag are skipped and flagged `SUPPRESSED`; enrichment never refills an email a person asked you to stop using.

### Alex Berman, narrow and current lists

Alex Berman's companies have booked 500k+ meetings. His site tells senders to verify every email before sending and aim for 95%+ valid, and to build the list after the offer for one tight niche. Applied here as a cost rule: enrich the segment that will be worked this quarter (open opportunities, target accounts) before the long tail, and spend mobile dollars only where a rep will dial.

## What this skill does not do

- Merge duplicate CRM records. Flag them and use the CRM's merge tool so activity history moves with the record.
- Infer emails from a naming pattern without verification. Email Finder results are validated at lookup time per its tool description; guessed patterns are not.
- Change owner, lifecycle stage, lead status, consent or opt-out fields.

## Sources

- UK Government Data Quality Hub, Meet the data quality dimensions (2021): https://www.gov.uk/government/news/meet-the-data-quality-dimensions
- HubSpot, Import records for a single object: https://knowledge.hubspot.com/import-and-export/import-records-for-a-single-object
- Pipedrive, How to avoid duplicates during an import: https://support.pipedrive.com/en/article/how-to-avoid-duplicates-during-an-import
- HighLevel, Importing contacts using a CSV file: https://help.gohighlevel.com/support/solutions/articles/155000004432-importing-contacts
- Salesforce, Import data with the Data Import Wizard: https://help.salesforce.com/s/articleView?id=sf.import_with_data_import_wizard.htm&type=5
- Salesforce, Import cheat sheet (matching and overwrite rules): https://resources.docs.salesforce.com/206/latest/en-us/sfdc/pdf/salesforce_import_cheatsheet.pdf
- Salesforce, Data Loader settings: https://developer.salesforce.com/docs/atlas.en-us.dataLoader.meta/dataLoader/configuring_the_data_loader.htm
- Salesforce, Upsert a record using an external ID: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api/dome_upsert.htm
- GDPR Article 14: https://gdpr-info.eu/art-14-gdpr/
- GDPR Article 5: https://gdpr-info.eu/art-5-gdpr/
- 47 CFR 64.1200: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
- FTC, CAN-SPAM Act compliance guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- Alex Berman, B2B lead generation: https://alexberman.com/b2b-lead-generation
