# CRM Enrichment Report: HubSpot contacts, US mid-market payroll prospects

Prepared 2026-10-13 for Northbeam Payroll, which sells payroll software to US companies with 20 to 500 employees. CRM: HubSpot, contacts and companies. Plan: Growth ($149/mo). Wallet before run: $184.20. Run ID: crm-enrich-20261013-hubspot. Company and person names are fictional and use the reserved `.example` domain.

## Input Profile

| Measure | Count |
|-|-|
| Records exported | 2,438 contacts, plus 60 companies with no associated contact |
| Suppressed (opt-out, unsubscribe, DND), skipped | 38 |
| Records in scope | 2,400 |
| Missing email | 640 |
| Existing emails | 1,760 |
| Missing job title | 410 |
| Missing mobile, in scope (SQL and opportunity stages) | 520 |
| Missing mobile, out of scope (other stages) | 1,660 |
| Missing company size | 900 rows across 610 company domains |
| Missing industry | 780 rows |
| Duplicate CRM records flagged | 26 |

Identifier counts across the 640 missing-email rows: 61 with a LinkedIn URL and no company domain, 498 with first name, last name and domain, 52 with a company name but no domain, 29 with none of these.

## Field Rules

| Field | Precedence | Policy | Approved by |
|-|-|-|-|
| email | CRM, find_emails, Lead Database after validation | fill_blank_only | RevOps lead, 2026-10-12 |
| email (invalid) | find_emails replacement, old value kept in prior_email | replace_if_invalid | RevOps lead, 2026-10-12 |
| job_title (blank) | CRM, Lead Database on a high match | fill_blank_only | RevOps lead, 2026-10-12 |
| job_title (different) | CRM wins; database value to enriched_title | stage_for_review | RevOps lead, 2026-10-12 |
| mobile | CRM, find_mobiles | fill_blank_only | RevOps lead, 2026-10-12 |
| company_name | CRM wins; job changes staged | stage_for_review | RevOps lead, 2026-10-12 |
| industry, number of employees | CRM, Lead Database company fields | fill_blank_only | RevOps lead, 2026-10-12 |
| contact owner, lifecycle stage, lead status | CRM only | never_overwrite | RevOps lead, 2026-10-12 |
| second phone | Lead Database phone when CRM phone differs | append_new | RevOps lead, 2026-10-12 |

## Routing Plan

| Gap | Identifier class | Rows | First call | Paid fallback |
|-|-|-|-|-|
| Email missing | LinkedIn URL, no domain | 61 | query_lead_database socialUrl | find_emails once the domain is known |
| Email missing | first + last + domain | 498 | query_lead_database companyDomain, match names locally | find_emails |
| Email missing | name + company name only | 52 | query_lead_database companyName | find_emails with domain if resolved, else company_name |
| Email missing | no domain, company or URL | 29 | none | flag NO_DOMAIN |
| Email invalid | first + last + domain | 97 | none | find_emails |
| Title missing | domain | 372 | query_lead_database companyDomain | none |
| Title missing | LinkedIn URL only | 22 | query_lead_database socialUrl | none |
| Title missing | nothing usable | 16 | none | flag NO_IDENTIFIER |
| Company size and industry | company domain | 610 domains | query_lead_database companyDomain, limit 1 | none |
| Mobile, in scope | LinkedIn URL (300) or email (190) | 490 | none | find_mobiles |
| Mobile, in scope | neither | 30 | none | flag NO_IDENTIFIER |
| Account-only companies | company domain | 60 | query_lead_database companyDomain plus People titles | scrape_website_finder, jobTitle Head of People |

## Cost Estimate

| Line | Units | Unit price | Ceiling | Actual |
|-|-|-|-|-|
| query_lead_database | 1,490 calls (83 socialUrl, 685 people-at-domain incl. 74 extra pages, 52 companyName, 610 company reads, 60 account-only) | Included in Growth | $0.00 | $0.00 |
| validate_emails, existing plus Lead Database emails | 1,978 emails | $0.0072 | $14.24 | $14.24 |
| find_emails | 480 lookups, 290 found | $0.05 per email found | $24.00 | $14.50 |
| find_mobiles | 490 inputs, 147 found | $0.25 per number found | $122.50 | $36.75 |
| scrape_website_finder | 38 domains, 27 contacts found | $0.0499 per contact found | $1.90 | $1.35 |
| validate_emails, new account contacts | 49 emails | $0.0072 | $0.35 | $0.35 |
| Total | | | $162.99 | $67.19 |

User go-ahead: RevOps lead approved the $162.99 ceiling in chat on 2026-10-12 after a 50-row pilot (Email Finder 29 of 50 hits, Mobile Finder 15 of 50). The Lead Database returned 41,870 rows across two days, under the 100,000 a day allowance.

## Fill Results

| Field | Missing before | Filled | Staged | Unfilled | Filled by |
|-|-|-|-|-|-|
| email | 640 | 430 | 0 | 210 | Lead Database 211 (validated valid or catch_all), find_emails 219 |
| job_title | 410 | 266 | 38 | 106 | Lead Database high matches 266; medium matches staged |
| mobile (in scope) | 520 | 147 | 0 | 373 | find_mobiles |
| number of employees | 900 | 812 | 0 | 88 | Lead Database company read |
| industry | 780 | 702 | 0 | 78 | Lead Database company read |
| new contact at account-only company | 60 | 47 | 0 | 13 | Lead Database 22, scrape_website_finder 25 valid or catch_all |

Invalid existing emails: 103 found by validation. 71 replaced through find_emails (old value in prior_email), 32 kept with email_status invalid and flagged EMAIL_INVALID.

Email status after the run, existing plus Lead Database emails (1,978 validated): valid 1,677, catch_all 149, unknown 36, invalid 110, disposable 6.

## Match Confidence

| Tier | Count | Action |
|-|-|-|
| high | 520 | Written per field policy |
| medium | 62 | Staged to review file, nothing written |
| low | 39 | Nothing written, flagged AMBIGUOUS_MATCH |
| none | 332 | Nothing written, flagged NOT_FOUND |
| Total attempted | 953 | Lead Database person lookups (socialUrl and people-at-domain) |

Of the 520 high matches, 9 socialUrl matches listed a different company than HubSpot. Flagged JOB_CHANGE; company and email untouched.

## Write-back Mapping

| Enricher column | CRM field | Import setting |
|-|-|-|
| crm_record_id | Record ID | Identifier; update existing only |
| email | Email | Don't overwrite ticked in the fill file; unticked only in the 71-row replacement file |
| job_title | Job Title | Don't overwrite ticked |
| mobile | Mobile Phone Number | Don't overwrite ticked; E.164 |
| phone_2 | Custom property Phone 2 | Append only; Don't overwrite ticked |
| linkedin_url | Custom property LinkedIn Profile URL | Don't overwrite ticked |
| industry | Company Industry via companies file | Mapped to dropdown; 41 unmapped values to Industry (enriched) |
| employees | Company Number of Employees via companies file | Don't overwrite ticked |
| enrich_* audit columns | Custom properties, group Enrichment | Always written |

## Audit Columns

| Column | Example | Rule |
|-|-|-|
| enrich_run_id | crm-enrich-20261013-hubspot | Same on every touched row |
| enriched_at | 2026-10-13 | Date of write-back |
| enrich_fields_changed | email;job_title | Only fields written, not staged |
| enrich_source | email=email_finder;job_title=lead_db | One source per written field |
| enrich_confidence | high | Tier of the person match |
| enrich_status | filled | filled, staged, kept_existing, not_found, skipped_rule, suppressed |
| enrich_flags | JOB_CHANGE;TITLE_CONFLICT | Every reason code for the row |
| prior_email | m.ruiz@oldco.example | Set only when replace_if_invalid fired |
| email_status | valid | Validator bucket |
| email_validated_at | 2026-10-13 | Date of validation or Email Finder lookup |

## Unfilled Flags

| Reason code | Count | Field | Next action |
|-|-|-|-|
| NOT_FOUND | 181 | email | Retry in 90 days |
| NO_DOMAIN | 29 | email | Rep adds company |
| AMBIGUOUS_MATCH | 21 | job_title | Rep picks from review file |
| NOT_FOUND | 69 | job_title | Retry in 90 days |
| NO_IDENTIFIER | 16 | job_title | Research by hand |
| NOT_FOUND | 343 | mobile | No action; no charge was made |
| NO_IDENTIFIER | 30 | mobile | Add LinkedIn URL |
| NOT_FOUND | 62 domains, 88 rows | employees | Rep fills from website |
| NOT_FOUND | 78 | industry | Rep fills |
| EMAIL_INVALID | 32 | email | Do not email; call or LinkedIn |
| JOB_CHANGE | 9 | company | New contact at new company, replacement at old account |
| TITLE_CONFLICT | 57 | job_title | Rep accepts or rejects staged title |
| DUPLICATE_IN_CRM | 26 | record | Merge in HubSpot |

## Sample Rows

| crm_record_id | Field | Prior value | New value | Source | Confidence | Status |
|-|-|-|-|-|-|-|
| 51203 | email | (blank) | dana.okafor@ledgerline.example | lead_db, validated valid | high | filled |
| 51877 | email | m.ruiz@ledgerline.example (invalid) | maria.ruiz@ledgerline.example | email_finder | high | filled |
| 52410 | job_title | (blank) | Director of People Operations | lead_db | high | filled |
| 53022 | job_title | (blank) | HR Manager | lead_db, nickname match Bob to Robert | medium | staged |
| 53318 | mobile | (blank) | +15125550142 | mobile_finder | high | filled |
| 54001 | company_name | Shipwise | Quotient Labs (in enriched_company) | lead_db socialUrl | high | staged |

## Next Steps

1. Import the 10-row test file update-only, open records 51203, 51877 and 53318, confirm owner fields unchanged, then import the remaining 2,390 rows.
2. Send the review file (62 medium matches, 57 title conflicts, 9 job changes) to the two AEs who own those accounts; re-import accepted values on 2026-10-20.
3. Create new contacts for the 9 job changes at their new companies and find replacements at the old accounts with the Lead Database by companyDomain.
4. Route the 147 new mobiles through the mobile-appender TCPA and DNC gate before any dialer campaign.
5. Re-validate catch_all and unknown emails before the next sequence; re-run title and size enrichment on 2027-01-13.
