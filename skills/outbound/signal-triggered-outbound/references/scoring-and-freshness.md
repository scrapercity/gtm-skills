# Scoring and Freshness

How a signal becomes a number, how that number decays, which tier it lands in, and how fast each tier must be worked. All weights, half-lives and thresholds are house starting points dated 2026-10. Re-fit them after 200 contacts per signal (section 6).

## 1. Score formula

```
score = fit + signal_strength + reachability            (0 to 100)

fit             = 0 to 40   (ICP match, table 2)
signal_strength = min(40, base_points x 0.5 ** (age_days / half_life_days) [+5 if a second live signal])
reachability    = 0 to 20   (table 3)
age_days        = today - signal_date
```

A signal past its max age scores 0 for strength and leaves the queue.

## 2. Fit points

| Criterion | Points |
|-|-|
| Category, platform or industry is a core ICP value | 15 |
| Category is adjacent (sells, but slower) | 7 |
| Geography inside the served area | 10 |
| Size band inside the sweet spot (employees, reviews, visits) | 10 |
| Size band at the edge | 5 |
| Not a chain or franchise location (local offers) | 5 |
| Maximum | 40 |

## 3. Reachability points

| Data on the record | Points |
|-|-|
| Named decision maker | 6 |
| Email with `email_status = valid` | 6 |
| Email `catch_all` | 3 |
| Mobile that passed the dialing gate | 5 |
| Business phone only | 2 |
| Website domain | 3 |
| Maximum | 20 |

Reachability is scored after cheap enrichment (Lead Database by domain, which is included on Growth) and before paid enrichment, so paid lookups go to records already near a tier line.

## 4. Decay table

Share of base points left at each age. Computed as 0.5 ** (age / half-life).

| Half-life (days) | Day 0 | Day 7 | Day 14 | Day 30 | Day 60 | Day 90 |
|-|-|-|-|-|-|-|
| 14 | 1.00 | 0.71 | 0.50 | 0.23 | 0.05 | 0.01 |
| 30 | 1.00 | 0.85 | 0.72 | 0.50 | 0.25 | 0.12 |
| 45 | 1.00 | 0.90 | 0.81 | 0.63 | 0.40 | 0.25 |
| 60 | 1.00 | 0.92 | 0.85 | 0.71 | 0.50 | 0.35 |
| 90 | 1.00 | 0.95 | 0.90 | 0.79 | 0.63 | 0.50 |

Worked example: a new Klaviyo detection (S5, base 35, half-life 45) found 7 days ago scores 35 x 0.5 ** (7 / 45) = 31.4 strength. With fit 35 and reachability 15 the total is 81.4: tier A. The same record at 60 days scores 35 x 0.5 ** (60 / 45) = 13.9 strength, total 63.9: tier B.

## 5. Tiers, SLAs and channels

| Tier | Score | Enrichment allowed | First touch | SLA from detection | Follow-up |
|-|-|-|-|-|-|
| A | 70 to 100 | Lead Database, Website Finder, Email Finder, validation, Mobile Finder | Call (if the gate passes) and email the same day | 2 business days | 4 touches over 10 business days, signal named in touch 1 and 3 |
| B | 40 to 69 | Lead Database, Website Finder, Email Finder, validation | Email in the signal campaign | 5 business days | 3 touches over 2 weeks |
| C | 0 to 39 | None | None | None | Re-score each pull; drop at max age |

Routing rules:

- Tier A creates a CRM task for a named owner and a notification (Slack, email) from the workflow.
- An account in an active sequence, a customer, or an open opportunity is logged with the signal and not contacted; the account owner sees the signal.
- An account contacted from any signal in the last 90 days is not re-enrolled (cool-down). New signals on it are added to the CRM record for the next cycle.
- Any opt-out from any channel suppresses all signal campaigns for that contact.

## 6. Freshness rules

| Rule | Value | Why |
|-|-|-|
| Baseline pull | Produces no signals | Everything looks new on day one |
| Wording of time | "In the last week" for weekly pulls, "this month" for monthly | The pull date bounds the event, it does not date it |
| Max age | Per signal in the catalog; default 2x half-life | Old events read as research |
| Re-verify before tier A touch | Tech removal (S6), rating drop (S3), distress status (S11) | These revert or carry false positives |
| Double-count protection | One signal per account per pull counts at full value; a second adds 5 | Prevents a busy account from swamping the queue |
| Cool-down | 90 days between signal-triggered sequences per account | Keeps the program from feeling like surveillance |

## 7. Measure and re-fit

Log per contact: `signal_id`, `signal_date`, `age_at_first_touch`, `score`, `tier`, then reply, positive reply, meeting.

| Check | After | Action |
|-|-|-|
| Meeting rate by signal vs a static list from the same ICP | 200 contacts per signal | Retire a signal that does not beat the static list |
| Meeting rate by age bucket (0 to 7, 8 to 30, 31+ days) | 200 contacts per signal | If 31+ converts like the static list, cut max age to 30 |
| Tier A meeting rate vs tier B | 100 contacts per tier | If A is not at least 1.5x B, re-weight fit vs signal |
| SLA hit rate for tier A | Weekly | Under 90%: reduce tier A volume or add an owner |

## 8. Queue record

| Field | Example |
|-|-|
| `account_key` | northpaw.example |
| `signal_id` | S5 |
| `signal_label` | Klaviyo adopted |
| `signal_date` | 2026-10-12 |
| `source_run` | techstack-klaviyo-20261012, runId first 8 characters |
| `age_days` | 7 |
| `fit` | 35 |
| `signal_strength` | 31.4 |
| `reachability` | 15 |
| `score` | 81.4 |
| `tier` | A |
| `owner` | Dana R. |
| `action` | Call founder, email touch 1 |
| `due_by` | 2026-10-21 |

## Sources

- https://www.insidesales.com/leveraging-trigger-events/
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://scrapercity.com/llm-info
