# Scoring and Freshness

How a signal becomes a number, how that number decays, which tier it falls in, and how each tier is worked. No published study gives score weights, decay rates or tier cut-offs for these signals, so every weight, base point value, half-life, max age and cut-off is a setting the program writes into its Scoring Model and Signal Catalog, then re-fits from its own meeting rate by age bucket (section 7). The formulas below are arithmetic; the numbers in the examples are one program's settings, not defaults.

## 1. Score formula

```
score = max(0, fit + signal_strength + reachability - negative_points)   (0 to 100)

fit             = 0 to F    (ICP match, table 2; the program sets F)
signal_strength = min(S, top_decayed_value + bonus x extra_live_signals)
top_decayed_value = max over live signals of base_points x 0.5 ** (age_days / half_life_days)
reachability    = 0 to R    (table 3; the program sets R)
negative_points = sum of live negative signals (layoffs, hiring freeze, competitor signed; the program sets each)
age_days        = today - signal_date
F + S + R       = 100
```

A signal past its max age scores 0 for strength and leaves the queue. A negative signal also pauses the account for the days the program sets; signals that fire during the pause are logged and scored when it ends (signal catalog, Negative signals). Before an event (S26), age is 0. A program can also cap a signal type's strength on its own (for example a Form D, where the filings run mostly to funds; see the catalog) so that it reaches tier A only once a second signal is live: the cap is any value at or below (A cut-off - F - R - 1).

## 2. Fit points

The program lists its criteria and points; the maximum is F.

| Criterion | Points |
|-|-|
| Category, platform or industry is a core ICP value | Set in the program |
| Category is adjacent (sells, but slower) | Set in the program |
| Geography inside the served area | Set in the program |
| Size band inside the sweet spot (employees, reviews, visits) | Set in the program |
| Not a chain or franchise location (local offers) | Set in the program |

## 3. Reachability points

The program lists its criteria and points; the maximum is R.

| Data on the record | Points |
|-|-|
| Named decision maker | Set in the program |
| Email with `email_status = valid` | Set in the program |
| Email `catch_all` | Set in the program, below `valid` |
| Mobile number on file | Set in the program |
| Business phone only | Set in the program |
| Website domain | Set in the program |

Reachability is scored after cheap enrichment (Lead Database by domain, which is included on Growth) and before paid enrichment, so paid lookups go to records already near a tier line.

## 4. Decay lookup

Share of base points left at each age, computed as 0.5 ** (age / half-life). Use it to check a program's settings by hand.

| Half-life (days) | Day 0 | Day 7 | Day 14 | Day 30 | Day 60 | Day 90 |
|-|-|-|-|-|-|-|
| 14 | 1.00 | 0.71 | 0.50 | 0.23 | 0.05 | 0.01 |
| 30 | 1.00 | 0.85 | 0.72 | 0.50 | 0.25 | 0.12 |
| 45 | 1.00 | 0.90 | 0.81 | 0.63 | 0.40 | 0.25 |
| 60 | 1.00 | 0.92 | 0.85 | 0.71 | 0.50 | 0.35 |
| 90 | 1.00 | 0.95 | 0.90 | 0.79 | 0.63 | 0.50 |

Half-lives measured in days, by hours since the event (for signals delivered by webhook, such as S14 and S19):

| Half-life (days) | 1 hour | 4 hours | 24 hours | 48 hours | 72 hours | 7 days |
|-|-|-|-|-|-|-|
| 2 | 0.99 | 0.94 | 0.71 | 0.50 | 0.35 | 0.09 |
| 3 | 0.99 | 0.96 | 0.79 | 0.63 | 0.50 | 0.20 |
| 7 | 1.00 | 0.98 | 0.91 | 0.82 | 0.74 | 0.50 |

Compute age in fractional days for these signals (hours / 24).

Worked example with one program's settings (S5 base 35, half-life 45, fit 35, reachability 15, tier A at 70): a Klaviyo detection found 7 days ago scores 35 x 0.5 ** (7 / 45) = 31.4 strength, total 81.4, tier A. The same record at 60 days scores 35 x 0.5 ** (60 / 45) = 13.9 strength, total 63.9, tier B.

## 5. Tiers and channels

The program sets the A and B cut-offs and the touch window per tier and writes them in its Scoring Model and Routing table.

| Tier | Enrichment allowed | First touch | Follow-up |
|-|-|-|-|
| A | Lead Database, Website Finder, Email Finder, validation, Mobile Finder | Call and email the same day | Instantly's spacing (March 2026): first follow-up 2 to 3 days later, later ones 4 to 7 days apart, 4 to 7 emails over 14 to 21 days; signal named in touch 1 |
| B | Lead Database, Website Finder, Email Finder, validation | Email in the signal campaign | Same spacing |
| C | None | None | Re-score each pull; drop at max age |

Speed: Craig Elias (InsideSales, 2013) says the first viable vendor in the window of dissatisfaction wins far more often, citing a 74% close ratio attributed to Forrester. No source gives a day or minute count for these signals. Set each tier's touch window, then log days (or minutes, for webhook signals) from detection to first touch and compare meeting rate across those buckets.

Routing rules:

- Tier A creates a CRM task for a named owner and a notification (Slack, email) from the workflow. When the owner misses the SLA, the workflow reassigns the task or moves it to the next day's batch; the program writes which.
- An identified visitor or registrant below the buyer (rep, SDR, coordinator) is routed to the buyer at that domain with the fit-based email, which does not mention the visit.
- An account in an active sequence, a customer, or an open opportunity is logged with the signal and not contacted; the account owner sees the signal.
- An account contacted from any signal inside the cool-down (section 6) is not re-enrolled. New signals on it are added to the CRM record for the next cycle.
- Stop the sequence on any reply; anyone who asks to be removed comes off every list the same day.

## 5a. Exclusion tier (X)

Exclusion runs before scoring, so an excluded account skips scoring, enrichment spend and alerts. Excluded accounts get tier X, a reason and a log row. Every signal program lists its exclusion classes and counts in an `## Exclusions` section; `scripts/check-output.py` fails a program that leaves out competitors, vendors, partners or agencies.

| Class | Who | Match rule | List source | Why exclude |
|-|-|-|-|-|
| Competitors | Companies selling the same offer | Registrable domain on the competitor list; also flag company names containing a competitor's brand | Sales leadership, win/loss notes, G2 or Capterra category pages for your category | Their visits, tech adoption and hiring signal research on you, so a pitch wastes the touch |
| Vendors | Companies you buy from (tools, data, payroll, office) | Domain on the AP vendor list | Finance or the accounting system's vendor export | A vendor's reps browse your pricing to renew or upsell, so they never buy |
| Partners | Referral, reseller, integration and co-sell partners | Domain on the partner list | Partnerships owner, partner portal export | Partner accounts are worked through the partner manager |
| Agencies | Marketing, dev and lead generation agencies, theme and app builders | Domain on the agency list, or category or name containing agency, studio, digital, marketing, consulting (flag for review, do not auto-drop) | Partner directories of the tools you track, plus the review flag | Agencies install tracked technology on demo and client stores (S5 false positives) and visit pricing pages for clients |
| Customers and open opportunities | Current accounts and live deals | Domain in the CRM with lifecycle customer or an open deal | CRM export, refreshed each cycle | The account owner works them; the signal is logged on the record |
| Do not contact | Opted-out companies and accounts leadership has closed | Domain on the do-not-contact list | Leadership | Permanent |

Order of checks for every candidate row: exclusion list, then opt-outs and suppression, then the cool-down, then scoring.

## 6. Freshness rules

| Rule | Value | Basis |
|-|-|-|
| Baseline pull | Produces no signals | Everything looks new on day one |
| Wording of time | "In the last week" for weekly pulls, "this month" for monthly | The pull date bounds the event, it does not date it |
| Max age | Per signal in the program's catalog, at least as long as the half-life | The checker enforces max age at least the half-life |
| Re-verify before a tier A touch | Tech removal (S6), rating drop (S3), distress status (S11) | Load the site or listing; these revert |
| Stacking | The strongest live signal counts in full; each further one adds the program's bonus, up to S | Set in the program |
| Cool-down | One signal-triggered sequence per account per 90 days | Instantly (March 2026) advises pausing two to three months before re-engaging a contact |

## 7. Measure and re-fit

Log per contact: `signal_id`, `signal_date`, `age_at_first_touch`, `score`, `tier`, then reply, positive reply, meeting.

| Check | After | Action |
|-|-|-|
| Meeting rate by signal vs a static list from the same ICP and weeks | The contact count the program sets per signal | Retire a signal that does not beat the static list |
| Meeting rate by age bucket | Same sample | Cut max age where older buckets convert like the static list; lengthen the half-life where they do not decay |
| Tier A meeting rate vs tier B | Same sample per tier | If A does not beat B, re-weight fit against signal strength |
| Touch-window hit rate for tier A | Weekly | Misses mean too much tier A volume per owner: raise the cut-off or add an owner |

Without a static baseline yet, compare with published averages: Hunter reports a 3% average reply rate for sales outreach sequences (4.5% across all uses, 31 million emails sent in 2025), and Instantly 3.43% across all sequences (2026 benchmark report).

## 8. Queue record

| Field | Example |
|-|-|
| `account_key` | northpaw.example |
| `signal_id` | S5 |
| `signal_label` | Klaviyo adopted |
| `source` | `scrape_builtwith`, or `other:rb2b` for an outside signal |
| `signal_date` | 2026-10-12 |
| `source_run` | techstack-klaviyo-20261012, runId first 8 characters |
| `age_days` | 7 |
| `fit` | 35 |
| `signal_strength` | 31.4 |
| `reachability` | 15 |
| `negative_points` | 0 |
| `paused_until` | Blank, or the date a negative signal's pause ends |
| `score` | 81.4 |
| `tier` | A (X when excluded) |
| `exclusion_reason` | Blank, or competitor, vendor, partner, agency, customer, do_not_contact |
| `owner` | Dana R. |
| `action` | Call founder, email touch 1 |
| `due_by` | 2026-10-21 |

## Sources

- https://www.insidesales.com/leveraging-trigger-events/
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://scrapercity.com/llm-info
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://hunter.io/the-state-of-cold-email
