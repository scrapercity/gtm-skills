# Sequencer Import Specs

How to shape the send-ready CSV for Instantly, Smartlead, Lemlist and EmailBison, which upload settings to choose, and the launch checklist. Facts below come from each platform's help center or docs, checked 2026-10-13; platforms change their importers, so re-read the linked page when an upload fails.

## 1. Platform rules

| Rule | Instantly | Smartlead | Lemlist | EmailBison |
|-|-|-|-|-|
| Required column | Email, mapped at upload | Email (each row maps to a lead email) | `email`, unique per lead | `email` |
| Header rules | First row; unique; 20 characters or fewer; start with a capital letter | Columns mapped at upload; unused ones set to Ignore | First row; standard names auto-map; custom names without spaces | Mapped at upload; custom variables created in the mapping step |
| Variable limit | 50 variables per upload | 40 custom variables per lead | Unlimited custom variables | Not stated |
| Encoding | UTF-8 ("CSV UTF-8" in Excel) | Properly formatted CSV | UTF-8; plain CSV, not `.xlsx` | Not stated |
| Duplicate handling | "Check for duplicates across all campaigns/lists", on by default | Option to skip leads already in another campaign | "Manage duplicates" step for the campaign or team | Not stated |
| Block and unsubscribe lists | Workspace blocklist | Options to import or skip leads on the global block list, unsubscribe list and bounced list | Not covered in the import guide | Not covered |
| Verification at upload | Optional, billed in Instantly credits | Not covered | Enrichment at import can be billed | Not covered |
| Blank cells | Not covered | The value does not appear in the email | Not covered | Not covered |

Rows marked "not covered" or "not stated" mean the cited page does not say; test with a small file before a full upload.

## 2. Header map

Rename columns from the master file (`pipeline-runbook.md` section 8) to these headers. The Instantly column also satisfies the 20-character, capital-letter, no-space rule, so it works as a safe default for Smartlead and EmailBison.

| Master column | Instantly | Smartlead | Lemlist | EmailBison |
|-|-|-|-|-|
| `email` | Email | Email | email | email |
| `first_name` | FirstName | first_name | firstname | first_name |
| `last_name` | LastName | last_name | lastname | last_name |
| `company_name` | CompanyName | company_name | companyName | company |
| `company_domain` | Website | website | companyDomain | website |
| `title` | Title | title | jobTitle | title |
| `company_city` | City | city | city | city |
| `industry` | Industry | industry | industry | industry |
| `case_study` | CaseStudy | case_study | caseStudy | case_study |
| `trigger` | Trigger | trigger | trigger | trigger |
| `first_line` | FirstLine | first_line | icebreaker | first_line |
| `linkedin_url` | LinkedIn | linkedin_url | linkedinUrl | linkedin_url |
| `company_contact_order` | ContactOrder | contact_order | contactOrder | contact_order |

Documented standard names: Lemlist auto-maps `email`, `firstname`, `lastname`, `companyName`, `companyDomain`, `linkedinUrl`, `phone`, `picture` and `icebreaker`; EmailBison's examples use `first_name`, `last_name` and `email`; Instantly lists First Name, Last Name and Company Name as predefined fields. Every other name in the map becomes a custom variable created at upload.

The variable written in the copy must match the mapped name exactly (Smartlead notes that placeholders like `{{first_name}}` must match the names mapped at import). Write the copy after the header map is fixed.

Columns that stay in the master file only: `email_status`, `email_validated_at`, `source`, `source_detail`, `pulled_at`, `segment`, `wave`. Map them to "Do Not Import" or "Ignore", or drop them from the import projection.

## 3. File preparation

| Step | Rule |
|-|-|
| Encoding | Save as UTF-8 so accented names survive |
| Header row | One row, without blank columns or merged cells |
| Booleans | Remove true and false columns from the import file (Instantly asks for this) |
| Whitespace | Trim every cell |
| Phone numbers and ZIPs | Keep as text; never open the CSV by double-clicking in a spreadsheet app |
| One file per campaign and wave | `send-ready-[segment]-[date]-wave1.csv`, `-wave2.csv`, `-catch-all.csv` |
| Row check | Count rows after export and compare with the master file's send-ready count |

Python export that keeps text intact:

```python
import csv
cols = [("email", "Email"), ("first_name", "FirstName"), ("last_name", "LastName"),
        ("company_name", "CompanyName"), ("title", "Title"), ("company_city", "City"),
        ("case_study", "CaseStudy"), ("company_domain", "Website"), ("company_contact_order", "ContactOrder")]
with open("master.csv", newline="", encoding="utf-8") as f, open("wave1.csv", "w", newline="", encoding="utf-8") as g:
    w = csv.writer(g)
    w.writerow([h for _, h in cols])
    for r in csv.DictReader(f):
        if r["email_status"] == "valid" and r["company_contact_order"] == "1":
            w.writerow([r[c].strip() for c, _ in cols])
```

## 4. Upload settings

| Setting | Choice | Why |
|-|-|-|
| Duplicate check across campaigns | On | Keeps one person in one campaign |
| Skip leads on block, unsubscribe and bounce lists (Smartlead options) | Skip | Suppression must hold inside the platform too |
| Verification at upload | Off when every row was validated with `validate_emails` within four weeks | Avoids paying twice; turn it on for older rows (Hunter's 2025 test: over 2% of a list invalid after four weeks) |
| Daily limit per mailbox | 30 | Instantly recommends 30 campaign emails per account per day; Berman keeps inboxes under 50 |
| Bounce auto-pause | On, threshold set to 2% | Instantly's default pauses at 5% once a campaign has sent 200 and the threshold is adjustable; Berman keeps bounces under 2% |
| Catch-all file | Separate campaign at the user's daily volume | Catch-all addresses accept at validation and can bounce on send |
| Send window | Recipient's business hours | Time zone from `person_state` or `company_state` |

## 5. Blocklist import

Before the leads: import the invalid and disposable addresses from validation, past hard bounces, unsubscribes and complaint addresses into the workspace blocklist. Instantly and Smartlead both keep one. Re-import after each new validation run.

## 6. Launch checklist

| # | Check | Pass when |
|-|-|-|
| 1 | Authentication | SPF, DKIM and DMARC pass on a test message from each sending domain |
| 2 | Warmup | Each mailbox has at least 2 weeks of warmup before its first cold send (Instantly; Berman says 2 to 4 weeks) |
| 3 | Daily limit | Set in the platform, under 50 per mailbox |
| 4 | Bounce auto-pause | On |
| 5 | Blocklist | Imported before the leads |
| 6 | Duplicate check | On at upload |
| 7 | Unsubscribe | Unsubscribe in every step; removals added to the blocklist the same day (Google and Yahoo bulk-sender rules: one-click unsubscribe, processed within 2 days) |
| 8 | Validation age | Every row validated within four weeks of its send date, or a re-validation date set |
| 9 | Catch-all | Separate campaign at the user's daily volume |
| 10 | Waves | Wave 1 holds only `company_contact_order = 1` |
| 11 | Variables | Every variable in the copy is filled on every row or has a fallback |
| 12 | Test send | One test lead per variant renders without empty variables |

## Sources

- Instantly, How to upload leads with a CSV file: https://help.instantly.ai/en/articles/6254215-how-to-upload-leads-with-a-csv-file
- Instantly, High bounce auto-pause: https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- Instantly, When your email account is ready for campaigns: https://help.instantly.ai/en/articles/13938078-when-your-email-account-is-ready-for-campaigns
- Smartlead, How to map CSV columns in Smartlead campaigns: https://helpcenter.smartlead.ai/en/articles/409-how-to-map-csv-columns-in-smartlead-campaigns
- Lemlist, How to import leads from a CSV file: https://help.lemlist.com/en/articles/4515109-how-to-import-leads-from-a-csv-file
- EmailBison, Custom variables: https://docs.emailbison.com/leads/custom-variables.md
- Instantly, Account and campaign limits: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Google, Email sender guidelines: https://support.google.com/a/answer/81126
- Yahoo, Sender best practices: https://senders.yahooinc.com/best-practices/
- Hunter, Email verification guide, email data decay (4 Nov 2025): https://hunter.io/email-verification-guide/email-data-decay
- Alex Berman, Cold email templates (bounces under 2%): https://alexberman.com/cold-email-templates
