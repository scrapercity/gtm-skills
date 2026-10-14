# Deliverability Health Report: [fill company]

Period [fill start date] to [fill end date]. Prepared [fill date] by [fill owner].

## Summary

[fill: one paragraph with domains in scope, how many are green, yellow and red, open incidents, list validation results, and what the user must decide]

## Scope

| Item | Value |
|-|-|
| Main domain (never sends cold email) | [fill] |
| Sending domains | [fill] |
| Mailboxes | [fill] |
| Sequencer | [fill] |
| Cold sends in period | [fill] |
| Dedicated IPs | [fill] |
| Pause authority (one owner, plus backup) | [fill] |
| Backup capacity (warmed reserves, sends a day) | [fill] |

Not checked: [fill one line naming each check not run and why, or none]

## Authentication and Unsubscribe

| Domain | SPF | DKIM | DMARC | Alignment | Unsubscribe header | Postmaster compliance |
|-|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

Records to publish: [fill exact SPF, DKIM and DMARC values and the Admin console path for any failing check, or none]

## List Validation

| Bucket | Count | Action |
|-|-|-|
| valid | [fill] | [fill] |
| valid_catch_all | [fill] | [fill] |
| unknown | [fill] | [fill] |
| invalid | [fill] | [fill] |
| disposable | [fill] | [fill] |
| Total | [fill] | [fill] |

Cost: [fill]

## Placement Tests

| Domain | Gmail | Workspace | Outlook.com | Microsoft 365 | Yahoo | Result |
|-|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

## Domain Health

| Domain | Mailboxes | Sends (period) | Hard bounce % | Spam rate (Postmaster) | Human replies | Status | Action |
|-|-|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

## Blocklist Checks

| Domain | Role | Spamhaus DBL | SURBL | URIBL | Checked |
|-|-|-|-|-|-|
| [fill sending domain] | [fill] | [fill] | [fill] | [fill] | [fill] |
| [fill linked domain: tracking host, main site, booking link] | [fill] | [fill] | [fill] | [fill] | [fill] |

## Incidents and Actions

| Opened | Type | Scope | Trigger | Action | Owner | Resume condition | Status |
|-|-|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

## Stop Rules

| Rule | Threshold | Source | Fired this period | Action taken |
|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] |

## Six-Month Audit

Last full audit [fill date]. Next due [fill date].

| Check | Run on | Result | Action | Next due |
|-|-|-|-|-|
| DNS records vs plan | [fill] | [fill] | [fill] | [fill] |
| DKIM key rotation | [fill] | [fill] | [fill] | [fill] |
| DMARC rua review, unknown senders | [fill] | [fill] | [fill] | [fill] |
| Placement test, Google, Microsoft, Yahoo | [fill] | [fill] | [fill] | [fill] |
| Caps vs volume | [fill] | [fill] | [fill] | [fill] |

## Next Review

[fill: date, checks to repeat, decisions pending]
