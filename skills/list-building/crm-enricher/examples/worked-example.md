# CRM Enrichment Report: HubSpot contacts, US mid-market payroll prospects

_Illustrative example. Companies, people, counts and run results are invented to show the format; companies use the reserved `.example` domain. Prices are ScraperCity catalog prices._

Run completed 2026-10-13 for Tallyroll (tallyroll.example), which sells payroll software to US companies with 20 to 500 employees; counts are actual. CRM: HubSpot, contacts and companies. Plan: Growth ($149/mo).

## Summary

| Question | Answer |
|-|-|
| What happens | Every existing email validated; blank emails filled from the Lead Database, then Email Finder; titles, seniority and company fields refreshed and job changes caught; mobiles added for Director-and-above Finance, HR and People contacts on open deals; written back update-only with an audit trail |
| Fields after the run | Email, Email Status (new), Email Validated At (new), Job Title, Seniority (new), Department (new), Mobile Phone Number (buyers on open deals), LinkedIn Profile URL, Industry, Number of Employees |
| Campaign-ready emails | 2,080 valid (2,028 existing contacts, 52 new contacts), plus 168 catch-all addresses for a separate lane |
| Cost | $56.81 of credits against a $119.56 ceiling, inside Growth's $159 monthly credit, so cash is the $149 plan; $0.03 per campaign-ready email, $0.26 per dial-ready mobile (96 numbers) |
| Time | Lookups ran in one day; the AEs return the review file by 2026-10-20 |
| Approvals needed | Review file decisions from the two AEs by 2026-10-20 |

## Input Profile

| Measure | Count |
|-|-|
| Records exported | 2,459 contacts, plus 60 companies with no contact |
| Suppressed or test records, skipped | 59 (38 opted out or unsubscribed, 12 test records, 9 Tallyroll employees) |
| Records in scope | 2,400 |
| Missing email | 640; the other 1,760 had never been validated |
| Missing job title | 410 |
| Mobile scope (accounts, seniority, departments) | 680 contacts on SQL and opportunity deals; 340 are Director and above in Finance, HR or People after the title refresh; 30 already had a mobile, so 310 missing |
| Missing company size or industry | 900 rows missing size across 610 domains; 780 missing industry |
| Duplicate CRM records flagged | 26, left for HubSpot's merge tool |

## Field Rules

| Field | Precedence | Policy |
|-|-|-|
| email (blank) | HubSpot; Lead Database email once validated valid; Email Finder | fill_blank_only |
| email (validated invalid) | Email Finder replacement; old address kept in prior_email | replace_if_invalid |
| email (catch-all result for a blank) | Written to enriched_email for review, not to Email | stage_for_review |
| job_title (blank) | HubSpot; Lead Database on a high match | fill_blank_only |
| job_title (different from the database) | HubSpot wins; database title to enriched_title | stage_for_review |
| seniority, department (new properties) | Lead Database on a high match | fill_blank_only |
| company_name (different: job change) | HubSpot wins; new company to the review file | stage_for_review |
| mobile | HubSpot; Mobile Finder for the mobile scope above | fill_blank_only |
| industry, number of employees | HubSpot; Lead Database company fields; Email Validator company columns | fill_blank_only |
| number of employees, different size band | HubSpot wins; new band staged for the account owner | stage_for_review |
| second phone | Lead Database phone when the HubSpot phone differs | append_new |
| contact owner, lifecycle stage, lead status, subscription and opt-out properties | HubSpot only | never_overwrite |

Approval: Priya Natarajan (RevOps lead) approved the sheet and the $119.56 ceiling on 2026-10-12, after the pilots below.

## Routing Plan

| Gap | Identifier class | Rows | First step (included) | Paid fallback |
|-|-|-|-|-|
| Email missing | LinkedIn URL, no domain | 61 | Lead Database by LinkedIn URL, then Email Validator | Email Finder once the match gives a domain |
| Email missing | first + last + domain | 498 | Lead Database people at the domain, name matched locally, then Email Validator | Email Finder |
| Email missing | name + company name | 52 | Lead Database by company name to resolve the domain | Email Finder with the domain, else the company name |
| Email missing | nothing usable | 29 | None | Flag NO_DOMAIN |
| Every existing email | any | 1,760 | Email Validator (also returns company name, industry and size for the domain) | None |
| Email invalid | name + domain, person still at the company | 98 | None | Email Finder replacement |
| Email Finder misses | company name on record | 120 | None | Email Finder again with the company name in place of the website domain |
| Title, seniority, department | LinkedIn URL, email or name + domain | 1,640 | Lead Database person lookup | None |
| Company size and industry | company domain | 610 domains | Lead Database company fields, one record per domain | Email Validator company columns |
| Mobile | LinkedIn URL (190) or work email only (100) | 290 | None | Mobile Finder; a second pass with the work email for URL misses |
| Mobile | neither identifier | 20 | None | Flag NO_IDENTIFIER |
| Job changers at the new company | new domain from the Lead Database | 9 | Lead Database email from the LinkedIn URL match, validated | Email Finder for the 3 without a valid one |
| Account-only companies | company domain | 60 | Lead Database by domain with a Finance or People title | Website Finder, title Head of People, for the 38 the database missed |

Match tiers: high 1,120, medium 96, low 54, none 370, of 1,640 attempted. High matches are written per the field rules, medium matches are staged, low and none write nothing. Nine LinkedIn URL matches list a different company than HubSpot: those people changed jobs.

## Cost Estimate

| Line | Units | Unit price | Actual | Ceiling |
|-|-|-|-|-|
| Lead Database | 2,162 calls (380 by LinkedIn URL, 1,060 people-at-domain including extra pages, 52 by company name, 610 company reads, 60 account-only) | Included in Growth | $0.00 | $0.00 |
| Email Validator | 2,112 emails (1,760 existing, 267 Lead Database emails, 36 unknown retries, 49 new account contacts) | $0.0072 | $15.21 | $15.21 |
| Email Finder, pass 1 | 479 lookups (378 blanks, 98 invalid replacements, 3 job changers), 292 found | $0.05 per email found | $14.60 | $23.95 |
| Email Finder, pass 2 (company name retry) | 120 lookups, 18 found | $0.05 per email found | $0.90 | $6.00 |
| Mobile Finder, pass 1 (URL, else work email) | 290 inputs, 87 found | $0.25 per number found | $21.75 | $72.50 |
| Mobile Finder, pass 2 (work email, URL misses only) | 95 inputs, 12 found | $0.25 per number found | $3.00 | $0.00 extra: only pass-1 misses enter |
| Website Finder | 38 domains, 27 contacts found | $0.0499 per contact found | $1.35 | $1.90 |
| Total | | | $56.81 | $119.56 |

Pilots before the go-ahead: Email Finder found 29 of 50, Mobile Finder 15 of 50. Email Finder and Mobile Finder bill only on a hit, so the ceiling is every lookup hitting.

## Fill Results

| Field | Missing before | Filled | Staged | Unfilled | Filled by |
|-|-|-|-|-|-|
| job_title (blank) | 410 | 266 | 38 | 106 | Lead Database high matches; medium matches staged |
| seniority and department (rows looked up) | 1,640 | 1,120 | 96 | 424 | Lead Database high matches; medium matches staged |
| mobile (scope above) | 310 | 99 | 0 | 211 | Mobile Finder pass 1 87, pass 2 12 |
| number of employees | 900 | 812 | 0 | 88 | Lead Database 760, Email Validator company columns 52 |
| industry | 780 | 702 | 0 | 78 | Lead Database 660, Email Validator company columns 42 |
| contact at an account-only company | 60 | 47 | 0 | 13 | Lead Database 22, Website Finder 25 (2 of its 27 failed validation) |

## Email Position After the Run

| Group | Before | After |
|-|-:|-:|
| Valid, validated 2026-10-13, person still at the company (main campaign) | 0 known | 2,028 |
| Catch-all (separate lane, see Refresh Schedule) | 0 known | 165 |
| Old address still valid, person moved (never emailed at the old company) | 0 known | 5 |
| Invalid, no replacement (kept with Email Status invalid) | unknown | 32 |
| No email | 640 | 170 |
| New contacts in the create file (8 job changers at their new company, 44 account-only buyers) | 0 | 52 valid, 3 catch-all |

Valid is 1,494 existing addresses that validated, 20 unknowns that validated on retry, 71 invalid addresses replaced and 448 blanks filled (Lead Database 211, Email Finder 219, then 18 on the company-name retry), less the 5 movers.

## Write-back Mapping

Contacts and companies are separate imports keyed on Record ID, update existing only, with "Don't import data in unmapped columns" selected; untouched columns are left out of the file so nothing is blanked.

| Column | CRM field | Import setting |
|-|-|-|
| crm_record_id | Record ID (contact) | Identifier; update existing only |
| email | Email | Don't overwrite ticked in the fill file; unticked only in the 71-row replacement file |
| email_status, email_validated_at | New properties Email Status (dropdown) and Email Validated At (date) | Always written |
| job_title | Job Title | Don't overwrite ticked |
| seniority, department | New properties Seniority and Department | Don't overwrite ticked |
| mobile | Mobile Phone Number | Don't overwrite ticked; E.164; never Phone Number |
| phone_2 | New property Phone 2 | Don't overwrite ticked |
| linkedin_url | LinkedIn Profile URL | Don't overwrite ticked |
| industry, employees | Industry and Number of Employees, companies file keyed on company Record ID | Don't overwrite ticked; 41 industry values outside the dropdown go to Industry (enriched) |
| enriched_title, enriched_company, enriched_email | New properties, group Enrichment | Review file only; accepted values re-imported |
| enrich_run_id (crm-enrich-20261013-hubspot), enriched_at, enrich_fields_changed, enrich_source, enrich_confidence, enrich_status, enrich_flags, prior_email | New properties, group Enrichment | Always written; enrich_run_id is the rollback filter |

The 55 new contacts go in a third file, create-only mode, deduped against the full 2,459-row export on email, LinkedIn URL, then name plus domain (0 matches).

## Unfilled Flags

| Reason code | Count | Field | Next action |
|-|-|-|-|
| NO_DOMAIN | 29 | email | Rep adds the company website; the row reruns on the next refresh |
| EMAIL_INVALID | 32 | email | Not emailed; rep calls or connects on LinkedIn |
| DOMAIN_NO_MAIL | 7 domains, 11 contacts | email | Account owner checks whether the company closed or was acquired; a new domain goes back through the Lead Database |
| TITLE_CONFLICT | 57 | job_title | AE accepts or rejects the staged title |
| AMBIGUOUS_MATCH | 21 | job_title | AE picks the right person from the review file |
| SIZE_BAND_CHANGE | 34 | employees | Account owner accepts or rejects the new band |
| JOB_CHANGE | 9 | company | Replacement contact at the old account (Next Steps) |
| DUPLICATE_IN_CRM | 26 | record | Merge in HubSpot before the campaign |

Not checked: funding, hiring, intent and SIC or NAICS codes; no tool in the plan returns them.

## How to Run It

The Lead Database pull was 2,162 calls returning 41,870 rows, under the 100,000 new leads a day allowance; at the API's 100 requests a minute it needs at least 22 minutes, so it runs as a script. Set `SCRAPERCITY_API_KEY`, put one domain per line in `domains.txt`, and run `python3 lead_db_lookup.py domains.txt`:

```python
import json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

API = "https://app.scrapercity.com/api/v1/database/leads"
HDR = {"Authorization": "Bearer " + os.environ["SCRAPERCITY_API_KEY"]}
cache = Path("lead_db_cache"); cache.mkdir(exist_ok=True)
for domain in dict.fromkeys(l.strip().lower() for l in open(sys.argv[1]) if l.strip()):
    out = cache / f"{domain}.json"
    if out.exists():                       # a restart skips finished domains
        continue
    rows, after = [], "0"
    try:
        for _ in range(5):                 # at most 5 pages of 100 per domain
            q = urllib.parse.urlencode({"companyDomain": domain, "limit": 100, "after": after})
            req = urllib.request.Request(f"{API}?{q}", headers=HDR)
            with urllib.request.urlopen(req, timeout=60) as r:
                body = json.load(r)
            rows += body.get("data", [])
            after = (body.get("pagination") or {}).get("next_after")
            time.sleep(0.7)                # stays under 100 requests a minute
            if not after:
                break
        out.write_text(json.dumps(rows))
    except Exception as err:               # retried next run, never counted as not found
        with open("retry.csv", "a") as f:
            f.write(f"{domain},{getattr(err, 'code', type(err).__name__)}\n")
```

For the LinkedIn URL lookups, send `socialUrl` with `limit` 5 in place of `companyDomain`. The paid steps run from the command line after `npx scrapercity login`:

```text
npx scrapercity email-validate --file emails.txt       # one address per line
npx scrapercity email-find --file contacts.csv         # header first_name,last_name,domain,company_name; no commas inside a field
npx scrapercity mobile-find --file mobile_inputs.txt   # one LinkedIn URL or email per line, no header
npx scrapercity poll RUN_ID                            # each command prints its RUN_ID
npx scrapercity download RUN_ID
```

Website Finder needs the job title with the domain list, so it runs through REST: `POST https://app.scrapercity.com/api/v1/scrape/website-finder` with the same Bearer header and a body of `domains` and `jobTitle` ("Head of People"); poll and download it the same way.

## Refresh Schedule

| Segment | Check | Next date | Cadence | Owner | Cost |
|-|-|-|-|-|-|
| Send gate | HubSpot active segment: Email Status valid, Email Validated At within 90 days (ZeroBounce: verify at least once a quarter), no opt-out or JOB_CHANGE flag; sequences enroll only from it | 2026-10-14 | Built once | Priya Natarajan | $0.00 |
| Catch-all lane (168 addresses) | Separate campaign once the main campaign's first 200 sends bounce under 2% (Berman's bounce line; Instantly runs its bounce check after 200 sends); paused past 2% | 2026-10-21 | Once | Priya Natarajan | $0.00 |
| Contacts entering a later sequence | Email Validator on rows last validated more than 90 days before the send | 2027-01-11 | Before each send | Priya Natarajan | $7.20 per 1,000 |
| 680 SQL and opportunity contacts | Lead Database job-change sweep by LinkedIn URL; about 9 to 16 changes a month at a planning decay of 1.3% to 2.3% a month (BLS median tenure 4.1 years, January 2026; ZeroBounce 2026 decay report, at least 23% a year) | 2026-11-13 | Monthly, Tallyroll's choice | Priya Natarajan | $0.00 on Growth |
| 610 active account domains | Title and company refresh; employees written only on a size-band change | 2027-01-13 | Quarterly, Tallyroll's choice | Priya Natarajan | $0.00 on Growth |
| Mobiles reps mark wrong | Mobile Finder for those people only | 2026-11-16 | On rep flags | Sales manager | $0.25 per number found |

## Next Steps

1. 2026-10-14, Priya: import 10 rows update-only, open records 51203, 51877 and 53318 to confirm owner and stage fields did not change and the audit properties are filled, then import the other 2,390 rows. The original export is the rollback file.
2. 2026-10-14, Priya: build the send-gate segment and enroll its 2,028 contacts in the main campaign.
3. 2026-10-15, Priya: import the 55-row create file in create-only mode; enroll the 8 job changers in the main campaign as their own "new role" segment and the 44 account-only buyers with the rest; the 3 catch-all creates join the catch-all lane.
4. 2026-10-16, sales manager: before the 99 mobiles load into the dialer, hold any number found on two or more contacts (3 held), drop numbers already in a Phone Number field, and remove anyone on the suppression list; if the dialer is a power dialer, keep only numbers the team's carrier lookup returns as mobile. 96 numbers load.
5. 2026-10-20, the two AEs: work the review file (96 medium matches, 57 title conflicts, 34 size-band changes, 9 job changes); Priya re-imports accepted values update-only the same day.
6. 2026-10-20, the two AEs: find a replacement contact at each of the 9 accounts the job changers left, from the Lead Database people at that domain with the departed person's title.
