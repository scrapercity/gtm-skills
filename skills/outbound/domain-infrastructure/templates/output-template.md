# Sending Infrastructure Plan: [fill company]

Prepared [fill plan date] (Day 0) for [fill team or client]. Prices checked [fill date]. [fill only if any value is a stand-in: one sentence saying values marked ASSUMED are replaced at the first checklist row]

## Summary

[fill: at most 160 words, answer first: which path meets the requested date and the slip in days for the others (no calendar dates), domains and mailboxes, provider split, build path, monthly total, the wide build's extra cost, the other volume reading in one clause]

## Inputs

| Input | Value | Source |
|-|-|-|
| Main domain | [fill] | [fill] |
| Volume as requested, and the reading used | [fill] | [fill] |
| Steps per sequence | [fill] | [fill] |
| Sending days per month | [fill] | [fill] |
| Mailboxes per domain | [fill 2 or 3, the user's choice] | [fill] |
| Reserve share of domains | [fill] | [fill] |
| Tenant size | [fill] | [fill] |
| Senders | [fill the team members whose names go on the mailboxes] | [fill] |
| Wide-build cap | [fill a number from Alex Berman's 10 to 20 a day for new domains] | [fill] |
| Sequencer | [fill] | [fill] |
| Existing sending domains | [fill] | [fill] |

## Capacity Plan

| Line | Formula | Result |
|-|-|-|
| Daily sends at steady state | [fill] | [fill] |
| Cap per mailbox | [fill] | [fill] |
| Active mailboxes | [fill] | [fill] |
| Mailboxes per domain (2 versus 3) | [fill both layouts: domains, mailboxes, monthly cost, share paused by one domain incident] | [fill] |
| Active domains | [fill] | [fill] |
| Reserve domains | [fill] | [fill] |
| Total domains | [fill] | [fill] |
| Total mailboxes | [fill] | [fill] |
| Wide build | [fill ceil(daily sends / wide cap), 2 per domain, provider split] | [fill mailboxes, domains, tenants] |

## Mailbox Provider Decision

Recipient mix: Google [fill]%, Microsoft [fill]%, other [fill]% (source: [fill sample size and when it was taken]).

| Option | Monthly cost | Fit | Reason |
|-|-|-|-|
| Google Workspace only | [fill] | [fill] | [fill] |
| Microsoft 365 only | [fill] | [fill] | [fill] |
| Google and Microsoft from day one | [fill] | [fill] | [fill] |
| Resold inboxes | [fill] | [fill] | [fill] |

Decision: [fill]

Build path: [fill own tenants or resold inboxes, what the choice costs and what it keeps or gives up]

Tenants: [fill tenants, users per tenant, mailboxes one tenant problem would pause]

## Sending Domains and Mailboxes

| Domain | Role | Provider and tenant | Mailboxes |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill first@ and first.last@ of two different people] |

All domains: [fill registrar, registration date, redirect target, nameservers, DNSSEC On or Off, renewal date and auto-renew]

## Tenant Settings

| Provider | Setting | Value | Why |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

## DNS Record Template

[fill provider] block, filled in for [fill example domain]. Applies to: [fill the other domains on this provider, by count].

| Provider | Record | Type | Host | Value | Differs per domain |
|-|-|-|-|-|-|
| [fill] | Verification | TXT | [fill] | [fill] | [fill] |
| [fill] | MX | MX | [fill] | [fill] | [fill] |
| [fill] | SPF | TXT | [fill] | [fill] | [fill] |
| [fill] | DKIM | TXT | [fill] | [fill] | [fill] |
| [fill] | DMARC | TXT | [fill] | [fill] | [fill] |
| [fill] | Postmaster | TXT | [fill] | [fill] | [fill] |
| [fill] | Tracking | CNAME | [fill] | [fill] | [fill] |
| [fill] | Redirect | [fill] | [fill] | [fill] | [fill] |

Main domain changes: [fill the one wildcard report authorization record, or none if a report service receives rua]

How the records get written: [fill dashboard, or the API with the dry-run and live steps]

```bash
[fill the script when records go in by API: the loop over the domain file that writes every row of each provider block]
```

## Launch Timeline

Requested: [fill date and volume]

Warmup settings, every mailbox: [fill increase a day, daily warmup limit, reply rate, one value each; campaign limit 0 until the first cold day]

Ramp: [fill per-mailbox steps and when each raise happens]

| Path | Warmup start | First cold send | Full volume | Against the request |
|-|-|-|-|-|
| Standard (21 days) | [fill] | [fill] | [fill] | [fill] |
| Soft start (14 days) | [fill] | [fill] | [fill] | [fill] |
| Wide build, [fill mailboxes] mailboxes at [fill wide cap] | [fill] | [fill] | [fill] | [fill] |

Recommendation: [fill]

## Monitoring

Setup: [fill Postmaster Tools on every domain, the SNDS note, tenant quota reports, seed list, blocklist checks]

| Signal | Where | Act at | Stop at |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

## Cost Estimate

| Item | Numbers | Monthly |
|-|-|-|
| [fill mailboxes, domains and sequencer rows only] | [fill] | [fill] |
| Total | [fill] | [fill] |

Wide build instead: [fill its monthly total and the difference]

Not in the total: [fill list validation or other costs outside the infrastructure, one line, or delete]

## Launch Risks and Scaling Triggers

Domain age: [fill one sentence, no dates: warmup days and when the cap is reached]

Blast radius: [fill one sentence: what one domain or tenant problem pauses]

| Trigger | Action |
|-|-|
| [fill] | [fill] |
| [fill] | [fill] |
| [fill] | [fill] |

## Launch Checklist

| Step | Owner | Date | Done when |
|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] |

## Sources

- [fill one line per vendor or source whose number the plan uses, with its URL]
