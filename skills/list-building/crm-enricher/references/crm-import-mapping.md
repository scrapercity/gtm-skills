# CRM Import Mapping and Settings

How to export, map, and re-import enriched records for HubSpot, Pipedrive, GoHighLevel (HighLevel) and Salesforce without creating duplicates or erasing data. Vendor behavior below was read from each vendor's help pages in October 2026; CRMs change their import screens, so run the 10-row test import every time.

## 1. Universal rules

1. Export with the record ID. Every CRM puts a system ID on each record; it is the only identifier that cannot collide.
2. Re-import in update-only mode keyed on that ID.
3. Put only the columns you are writing in the file, plus the ID. A column you do not intend to change is a column that can blank or overwrite something.
4. Never leave a blank cell in a column you are writing. Split the file per field group if needed (an email file, a title file) so every cell has a value.
5. Create the audit fields in the CRM before the import (section 6).
6. Phones in E.164 (`+15125550142`). Some CRMs reformat on display; storing E.164 keeps dialers and dedupe consistent.
7. Import 10 rows, open 3 records, confirm owner-entered fields did not change and the audit fields are filled, then import the rest.
8. Keep the untouched original export. It is the rollback file.
9. New contacts (job changes at a new company, buyers found at account-only companies) go in a separate create file, deduped against the full CRM export first (`api-pipeline-and-sync.md` section 6).
10. One writer per field group. If the sequencer's CRM sync also writes email, title or company, switch that mapping off or to fill-blank-only (`api-pipeline-and-sync.md` section 7).

## 2. HubSpot

| Setting | Value for an enrichment write-back | Why |
|-|-|-|
| Import type | One file, one object (contacts or companies) | Keeps mapping simple |
| Mode | Update existing only | A row with no match is ignored instead of creating a record |
| Identifier | Record ID column | Per HubSpot, Record ID overrides any other unique identifier in the file |
| Fallback identifier | Email (contacts), Company Domain Name (companies) | Only when the export lacks Record ID; companies accept the domain up to the top-level domain |
| Don't overwrite | Tick for every property with policy `fill_blank_only` | Prevents existing values from being replaced |
| Unmapped columns | "Don't import data in unmapped columns" | Stops stray columns creating properties |

Column map (contacts):

| Enricher column | HubSpot property label |
|-|-|
| `crm_record_id` | Record ID |
| `email` | Email |
| `first_name`, `last_name` | First Name, Last Name |
| `job_title` | Job Title |
| `phone` | Phone Number |
| `mobile` | Mobile Phone Number |
| `company_name` | Company Name |
| `website` | Website URL |
| `person_city`, `person_state`, `person_country` | City, State/Region, Country/Region |
| `linkedin_url` | Custom property, single-line text (create "LinkedIn Profile URL") |
| Audit columns | Custom properties in a group named "Enrichment" |

Company fields (industry, number of employees, annual revenue) belong on the company object in HubSpot. Write them in a separate companies file keyed on the company Record ID, with Industry, Number of Employees and Annual Revenue mapped. HubSpot's Industry property is a dropdown; map the Lead Database industry to an allowed option or write it to a custom text property such as "Industry (enriched)".

`replace_if_invalid` emails: HubSpot matches contacts by email when Record ID is absent, so an email change must go through the Record ID column. Untick Don't overwrite for Email in that file only.

## 3. Pipedrive

| Setting | Value | Why |
|-|-|-|
| Object | People file and organizations file separately | Different match logic |
| Duplicate handling for people | Leave merging on, and include the person ID column if your import screen offers it | Pipedrive merges a person when the name is recognized and organization, phone or email matches, and adds new data to the existing record |
| Duplicate handling for organizations | Include the organization address only if unchanged | Organizations merge on address; a changed address creates a second organization |
| Test | 10 rows, then open each merged record | Pipedrive's article does not state whether a merge replaces an existing single-value field, so verify on the test rows |

Column map (people):

| Enricher column | Pipedrive person field |
|-|-|
| `crm_record_id` | ID (from the export) |
| `first_name`, `last_name` | First name, Last name (or Name) |
| `email` | Email, label Work |
| `phone` | Phone, label Work |
| `mobile` | Phone, label Mobile |
| `company_name` | Organization |
| `job_title` | Job title if your account has it; otherwise a custom text field |
| `linkedin_url` | Custom text field |
| Audit columns | Custom fields |

Pipedrive stores several emails and phones per person. A `append_new` value (second phone) fits naturally as another Phone entry with its own label. Never import a mobile under the Work label.

## 4. GoHighLevel (HighLevel)

| Setting | Value | Why |
|-|-|-|
| Import option | Update | Create and Update would add contacts for unmatched rows |
| Matching | Contact ID column present | HighLevel looks up Contact ID, then email, then phone |
| Don't update Empty Values | Ticked | Stops blank cells overwriting existing data |
| Tags | Add `enriched-YYYYMMDD` | Lets you build a smart list of touched contacts and reverse it |
| Phones | Digits with country code, no spaces, dashes or letters | HighLevel asks for spaces, dashes and letters removed |

Column map:

| Enricher column | HighLevel field |
|-|-|
| `crm_record_id` | Contact ID |
| `first_name`, `last_name` | First Name, Last Name |
| `email` | Email |
| `phone` or `mobile` | Phone (one standard phone field; put the second number in a custom field) |
| `company_name` | Company Name |
| `website` | Website |
| `job_title`, `linkedin_url` | Custom fields |
| Audit columns | Custom fields in an "Enrichment" folder |

HighLevel has one standard phone field and texting runs from it. Decide with the user which number goes there. If the CRM phone is a main line and a mobile was found, keep the main line in Phone, write the mobile to a custom "Mobile" field, and point any texting campaign at the field the user picks.

## 5. Salesforce

### Data Import Wizard (up to 50,000 records per import per Salesforce's import cheat sheet)

| Setting | Value | Why |
|-|-|-|
| Object | Contacts and accounts, or leads | Person accounts are not imported by the wizard |
| Operation | Update existing records | Add and update creates records for unmatched rows |
| Match by | Salesforce ID | IDs are exact; name matching ignores case and punctuation and treats "HP" and "Hewlett Packard" as different |
| Overwrite existing account values | Off for `fill_blank_only` fields | With it off, the wizard fills only empty account fields; with it on, blanks in the file still do not erase data |
| Trigger workflow rules and processes | Off for the test import | Avoids assignment rules or emails firing on 2,000 updates |

### Data Loader and API

| Setting | Value | Why |
|-|-|-|
| Operation | Update by ID, or Upsert by an external ID field | Upsert creates on no match, updates on one, and the REST API returns HTTP 300 on multiple matches without writing |
| Insert null values | Off | When on, blank mapped values write null and overwrite existing data on update |
| Batch size | Leave the default unless the org hits limits | Bulk API allows up to 10,000 per batch, SOAP API 200 |

Column map:

| Enricher column | Contact API name | Lead API name | Account API name |
|-|-|-|-|
| `crm_record_id` | Id | Id | Id |
| `first_name`, `last_name` | FirstName, LastName | FirstName, LastName | |
| `email` | Email | Email | |
| `job_title` | Title | Title | |
| `phone` | Phone | Phone | Phone |
| `mobile` | MobilePhone | MobilePhone | |
| `company_name` | (via AccountId) | Company | Name |
| `website` | | Website | Website |
| `industry` | | Industry | Industry |
| `employees` | | NumberOfEmployees | NumberOfEmployees |
| `annual_revenue` | | AnnualRevenue | AnnualRevenue |
| Person location | MailingCity, MailingState, MailingCountry | City, State, Country | |
| HQ location | | | BillingCity, BillingState, BillingCountry |
| Audit columns | Custom fields ending in `__c` | Custom fields ending in `__c` | Custom fields ending in `__c` |

Industry is a picklist on Lead and Account. Map values to the org's picklist or write to a custom text field.

## 6. Audit fields to create first

| Field | Type | Example |
|-|-|-|
| `enrich_run_id` | Text | `crm-enrich-20261013-hubspot` |
| `enriched_at` | Date | `2026-10-13` |
| `enrich_fields_changed` | Text | `email;job_title` |
| `enrich_source` | Text | `email=email_finder;job_title=lead_db` |
| `enrich_confidence` | Picklist: high, medium, low, none | `high` |
| `enrich_status` | Picklist: filled, staged, kept_existing, not_found, skipped_rule, suppressed | `filled` |
| `enrich_flags` | Text | `JOB_CHANGE;TITLE_CONFLICT` |
| `prior_email`, `prior_phone` | Text | Value before replacement |
| `email_status` | Picklist: valid, catch_all, unknown, invalid, disposable | `valid` |
| `email_validated_at` | Date | `2026-10-13` |

## 7. Rollback

1. Filter the CRM on `enrich_run_id` (or the HighLevel tag).
2. For replaced values, re-import `prior_email` and `prior_phone` into the main fields, keyed on record ID, update-only.
3. For filled-blank values, re-import the original export's columns with the CRM's "update empty values" or "insert null" option switched on for that one file. This is the only time blanks should be written.

## Sources

- HubSpot, Import records for a single object: https://knowledge.hubspot.com/import-and-export/import-records-for-a-single-object
- Pipedrive, How to avoid duplicates during an import: https://support.pipedrive.com/en/article/how-to-avoid-duplicates-during-an-import
- Pipedrive, Importing data with spreadsheets: https://support.pipedrive.com/hc/en/articles/208039595-How-can-I-import-data-into-Pipedrive-with-spreadsheets-
- HighLevel, Importing contacts using a CSV file: https://help.gohighlevel.com/support/solutions/articles/155000004432-importing-contacts
- Salesforce, Import data with the Data Import Wizard: https://help.salesforce.com/s/articleView?id=sf.import_with_data_import_wizard.htm&type=5
- Salesforce, Import cheat sheet: https://resources.docs.salesforce.com/206/latest/en-us/sfdc/pdf/salesforce_import_cheatsheet.pdf
- Salesforce, Data Loader settings: https://developer.salesforce.com/docs/atlas.en-us.dataLoader.meta/dataLoader/configuring_the_data_loader.htm
- Salesforce, Upsert using an external ID: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api/dome_upsert.htm
