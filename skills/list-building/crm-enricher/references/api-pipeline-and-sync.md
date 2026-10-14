# API Pipeline and CRM Sync

How to run enrichment on a schedule or on CRM events: triggers, which calls answer at once and which return a run, safe re-runs, error states, a reference lookup script, new-contact creation without duplicates, one writer per field, the send-gate view, monitoring, and the refresh schedule that keeps data from decaying. Pick the operating mode first with the build-vs-buy table in `SKILL.md`; this file covers the light-build and API-first modes.

## 1. Triggers

| Trigger | What runs | Scope | How |
|-|-|-|-|
| Record created (form fill, list import, reply synced from the sequencer) | Lead Database by `socialUrl` or by the email's domain; `validate_emails` on a new address | That record | CRM webhook to n8n, Zapier or Pipedream, then REST |
| Stage moves to SQL or opportunity | `find_mobiles` for the contact and the other contacts on the deal | That deal | Same webhook path |
| Weekly batch | Blanks in in-scope fields; validation for contacts entering a sequence next week whose `email_validated_at` is older than 90 days | Segment | CLI or REST script on cron |
| Job-change sweep, on the cadence the user sets | Lead Database by `socialUrl` for contacts on open opportunities and for customer champions | Named list | REST script |
| Title and company refresh, on the cadence the user sets | Title and company for active accounts; company fields (written only on a size-band change) | Active accounts | REST script |
| Before every sequence enrollment | The send gate in section 8 | Enrollment list | CRM view |

A champion who moves to a new company is a warm lead there; the sweep finds them at $0 wallet on Growth and Scale.

## 2. Calls that answer at once versus calls that return a run

| Call | Behavior | Fits |
|-|-|-|
| `GET` or `POST /api/v1/database/leads` | Returns `data` and `pagination` in the same response | A per-row HTTP step: Clay HTTP API column, n8n HTTP Request node, Zapier Webhooks step |
| `POST /api/v1/scrape/email-finder`, `/mobile-finder`, `/website-finder`, `/email-validator` | Returns a `runId`; then `GET /api/v1/scrape/status/{runId}` until `SUCCEEDED`, then `GET /api/downloads/{runId}` for the CSV | A batch step: collect the day's rows, start one run, poll or wait for the webhook, download, join back |

Never start one scraper run per CRM row. One run per row spends a request, a run slot and a CSV per record and trips the 10 concurrent scrapes and 100 requests a minute limits (`references/scrapercity-agent-patterns.md` rule 11). In n8n, batch with a schedule trigger, then a Wait node between start and status.

## 3. Safe re-runs

| Risk | Control |
|-|-|
| A crash halfway through a database loop | Cache every response on disk keyed by the query (domain or URL). A restart reads the cache. Fetching a record the account already holds is free and does not count toward the daily allowance |
| A scraper start that timed out | Do not resubmit blind. `list_runs` for the last hour, look for the same inputs, resubmit only if none exists |
| The same webhook delivered twice | Key the work on `runId`; confirm `SUCCEEDED` with the status call before downloading. ScraperCity documents no webhook signature, so the status call is the confirmation |
| The same write applied twice | Every row carries `enrich_run_id`. Before writing a field, skip it when the CRM already shows this run id and the same value |
| A create that already exists | Section 6 |

## 4. Error states

A failed lookup and an empty lookup are different results and get different codes, so a 429 storm never looks like a list with no data.

| Code | Meaning | `enrich_status` | Next attempt |
|-|-|-|-|
| `NOT_FOUND` | The call succeeded and returned no candidate | `not_found` | 90 days |
| `LOOKUP_ERROR` | 429 after retries, 503 after narrowing, network error, or a run that ended `FAILED` | `error` | Next run, from the retry file |
| `RETRY_EXHAUSTED` | `LOOKUP_ERROR` on 3 consecutive runs | `error` | A person checks the input (bad domain, dead site) |

Retry file: `crm-retry-[date].csv` with `crm_record_id`, step, error code and attempt count. Each run reads it first.

## 5. Reference script: Lead Database by domain

Standard library only. Reads one domain per line, pages up to 5 pages per domain, caches responses, paces calls under 100 a minute, backs off on 429 and 503, and writes failures to the retry file instead of dropping them.

```python
#!/usr/bin/env python3
"""Lead Database people lookups by company domain: disk cache, pacing, retries, error file.

Usage: SCRAPERCITY_API_KEY=... python3 lead_db_by_domain.py domains.txt
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://app.scrapercity.com/api/v1/database/leads"
KEY = os.environ["SCRAPERCITY_API_KEY"]
CACHE = Path("lead_db_cache")
MAX_PAGES = 5      # per domain; large companies go to find_emails instead
PACE = 0.7         # seconds between calls, under 100 requests a minute


def get(params, tries=5):
    for attempt in range(tries):
        url = API + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as err:
            if err.code not in (429, 503) or attempt == tries - 1:
                raise
            if err.code == 503:
                params = {**params, "limit": 25}   # narrow the search, then retry
            time.sleep(30 if err.code == 429 else min(60, 2 ** (attempt + 1)))
        except urllib.error.URLError:
            if attempt == tries - 1:
                raise
            time.sleep(min(60, 2 ** (attempt + 1)))


def people_at(domain):
    cached = CACHE / f"{domain}.json"
    if cached.exists():
        return json.loads(cached.read_text(encoding="utf-8"))
    rows, after = [], "0"
    for _ in range(MAX_PAGES):
        body = get({"companyDomain": domain, "limit": 100, "after": after})
        rows += body.get("data", [])
        after = (body.get("pagination") or {}).get("next_after")
        time.sleep(PACE)
        if not after:
            break
    cached.write_text(json.dumps(rows), encoding="utf-8")
    return rows


def main(path):
    CACHE.mkdir(exist_ok=True)
    domains = [d.strip().lower() for d in open(path, encoding="utf-8") if d.strip()]
    with open("crm-retry.csv", "a", encoding="utf-8") as retry:
        for domain in dict.fromkeys(domains):
            try:
                print(f"{domain}\t{len(people_at(domain))} people")
            except Exception as err:   # LOOKUP_ERROR: retried next run, never NOT_FOUND
                retry.write(f"{domain},lead_db,{getattr(err, 'code', type(err).__name__)}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: lead_db_by_domain.py domains.txt")
    main(sys.argv[1])
```

The response shape (`data`, `pagination.next_after`) is the one documented in the package's `AGENT_DOCS.txt`. Match CRM names against the cached rows with the rules in `field-precedence-and-overwrite-rules.md` section 4. To save daily allowance on large companies, stop paging a domain as soon as every CRM person at it is matched.

### Compact version for the report

The report's How to Run It section carries this shorter version, so a team without this file can run the pull. Same endpoint, paging, cache, pacing and retry file; no 429 back-off, so rerun it to pick up the retry file.

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

For LinkedIn URL lookups, send `socialUrl` with `limit` 5 in place of `companyDomain`. The paid steps run from the CLI after `npx scrapercity login`, one run per file, then `npx scrapercity poll RUN_ID` and `npx scrapercity download RUN_ID`:

| Step | Command | File format (from the CLI source) |
|-|-|-|
| Email Validator | `npx scrapercity email-validate --file emails.txt` | Every line containing `@` is sent; one address per line |
| Email Finder | `npx scrapercity email-find --file contacts.csv` | Header row containing "first"; columns by position: first name, last name, domain, company name; splits on every comma, so strip commas inside fields |
| Mobile Finder | `npx scrapercity mobile-find --file mobile_inputs.txt` | Every non-empty line is an input, so no header; one LinkedIn URL or email per line. Version 1.0.17 also sends the file name as one input, a free miss |
| Website Finder | `npx scrapercity website-finder --file domains.txt` | One domain per line. Version 1.0.17 also sends the file name, and any `--title` value, as domains; when a title is needed, send `domains` and `jobTitle` through REST |

## 6. New contacts without duplicates

Job-change contacts at a new company and buyers found at account-only companies are creates, not updates. They go in their own file:

1. Dedupe each new row against the full CRM export, not only the rows in scope, on lowercased email, then normalized LinkedIn URL, then first name + last name + domain. A match becomes an update to that record or is dropped.
2. Import in create-only mode where the CRM offers it: HubSpot's create-only import mode, Salesforce Data Import Wizard "Add new records". In Pipedrive and HighLevel, which match on their own keys during import, keep the email column in the file so an existing contact is matched instead of duplicated.
3. Tag the creates with the same `enrich_run_id` so a rollback can find them.

## 7. One writer per field group

When two tools write the same field, each sync overwrites the other and the value flips back and forth. Give every field group one writer:

| Field group | Writer | Everyone else |
|-|-|-|
| `enrich_*` audit fields, `email_status`, `email_validated_at`, `uses_<technology>` | The enrichment job | Read |
| Email, phone, mobile, title, company fields | The rep when non-empty; the enrichment job fills blanks under the field rule sheet | Sequencer reads only |
| Sequence status, last contacted, replies | The sequencer's CRM sync | Enrichment reads only |
| Owner, lifecycle stage, lead status, deal fields | Reps and CRM automation | Nobody else |
| Unsubscribe and do-not-contact flags | Whichever tool receives the request, written the same day | Every tool reads before acting |

If the sequencer's CRM integration also maps email, title or company back into the CRM, switch those mappings off or to fill-blank-only.

## 8. Send-gate and data-health views

Send gate, used as the only source for sequence enrollment: `email_status` is valid, `email_validated_at` is within the last 90 days (ZeroBounce recommends verifying at least once per quarter), no unsubscribe or do-not-contact flag is set, and no `JOB_CHANGE` flag (the person has left that address).

Catch-all lane: `email_status` is catch_all. It opens once the main campaign's first 200 sends bounce under 2% and pauses past 2%: Alex Berman keeps bounces under 2%, and Instantly's bounce auto-pause runs its check once a campaign has sent 200 emails.

| CRM | Build it as |
|-|-|
| HubSpot | An active segment (HubSpot now calls lists "segments") on those three property filters |
| Salesforce | A list view or report; in SOQL `WHERE Email_Status__c = 'valid' AND Email_Validated_At__c = LAST_N_DAYS:90` |
| Pipedrive | A saved filter on the custom fields |
| HighLevel | A smart list on the custom fields |

Data-health view, read per segment on each refresh: share of contacts with a valid email validated in the last 90 days; share with a title; share with a title older than the title freshness window; job changes flagged since the last sweep; staged rows waiting longer than the review time the user sets; month-to-date enrichment spend against the cap.

## 9. Monitoring for scheduled and API-first runs

| Metric | Source | Act when |
|-|-|-|
| Fill rate per field per run | Fill Results | Drops against the previous run: check inputs and column mapping |
| Cost per incremental fill per step | Run log | Above the field value in the rule sheet: move the step later or drop it (`waterfall-and-cost-control.md` section 4) |
| `LOOKUP_ERROR` share | Retry file | Rises run over run: slow the pacing or narrow queries |
| 429 responses | Script log | Repeated on most runs: raise `PACE` |
| CRM write failures | Import results or API responses | Any |
| Duplicates created | New records matching an existing email or LinkedIn URL | Any; fix the section 6 dedupe |
| Review queue age | Staged rows | Older than the review time the user sets: remind the account owner |
| Month-to-date spend | Run log | Reaches the monthly cap: pause scheduled paid steps |

## 10. Refresh schedule and decay

Two published figures bracket how fast contact data goes stale:

- US Bureau of Labor Statistics: median employee tenure 4.1 years (January 2026). Spread evenly, about 1.4% of contacts change employer each month, roughly 15% a year, before promotions and closures.
- ZeroBounce Email List Decay Report for 2026 (2025 data): at least 23% of an email list decays within a year; the previous edition reported at least 28% (2024 data). Vendor-reported, across its customers' lists.

Planning assumption: 15% to 28% of a contact list a year, 1.3% to 2.3% a month. Measure your own: the share of re-checked titles that changed, and hard bounces by months since validation.

| Segment | Check | Cadence | Cost |
|-|-|-|-|
| Contacts entering a sequence | `validate_emails` if `email_validated_at` is older than 90 days | Before each send | $7.20 per 1,000 validated |
| Open opportunities and customer champions | Lead Database `socialUrl` job-change sweep | User sets; expected changes per sweep = contacts x 1.3% to 2.3% x months since the last one | $0 wallet on Growth and Scale |
| Active accounts | Title and company refresh; company fields written only on a size-band change | User sets the title and size freshness windows | $0 wallet on Growth and Scale |
| Accounts tied to a technology trigger | Tech Stack Search per technology | Before each campaign that uses it | $4.99 per technology |
| Everyone else | No paid check until the record enters a sequence or a call list | On use | $0 |

At the planning range, 2,000 contacts on open opportunities produce about 26 to 46 job changes a month (2,000 x 1.3% to 2.3%). If the sweep flags far more, check the match rules before acting on them.

After each refresh, record the share of re-checked values that changed per field, and set the next window from it.

## Sources

- ScraperCity npm package 1.0.17, `AGENT_DOCS.txt` (database response shape, scraper start, status and download): https://www.npmjs.com/package/scrapercity
- ScraperCity, API docs (rate limits, result storage): https://scrapercity.com/api-docs
- ScraperCity agent patterns (safe retry, webhooks, keys): references/scrapercity-agent-patterns.md
- HubSpot, Create segments (previously called lists): https://knowledge.hubspot.com/lists/create-active-or-static-lists
- HubSpot, Import records for a single object (import modes): https://knowledge.hubspot.com/import-and-export/import-records-for-a-single-object
- Salesforce, Import data with the Data Import Wizard: https://help.salesforce.com/s/articleView?id=sf.import_with_data_import_wizard.htm&type=5
- Salesforce, SOQL date literals (`LAST_N_DAYS:n`): https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_dateformats.htm
- US Bureau of Labor Statistics, Employee Tenure (January 2026): https://www.bls.gov/news.release/tenure.nr0.htm
- ZeroBounce, How often should I verify my email list: https://zerobounce.net/docs/frequently-asked-questions/account/how-often-should-I-verify-my-email-list
- ZeroBounce, Email List Decay Report for 2026: https://zerobounce.net/email-list-decay
- ZeroBounce, 2025 report press release (28% figure, 2024 data): https://www.zerobounce.net/blog/newsroom/press/zerobounce-report-email-list-decay
- Alex Berman, Cold email templates (keep bounces under 2%): https://alexberman.com/cold-email-templates
- Instantly, High bounce auto-pause (check runs after 200 sends): https://help.instantly.ai/en/articles/9823139-high-bounce-auto-pause-feature
- ScraperCity CLI source (`--file` parsing per command): https://github.com/scrapercity/scrapercity-cli
- AWS Architecture Blog, Exponential backoff and jitter: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
