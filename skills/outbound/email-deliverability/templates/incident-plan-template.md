# Deliverability Recovery Plan: [fill company or program]

Prepared [fill date, weekday] for [fill owner with authority to pause any domain, default: the outbound lead, unless you name someone else today]. Setup: [fill inboxes] inboxes on [fill domains] domains at [fill cap] a day, [fill sends per week] sends a week. Assumed: [fill up to 3 assumptions in one line, sequencer default Instantly]. [fill: one line naming the same two settings in any other sequencer: custom tracking domain and bounce auto-pause]

## Verdict

[fill: 3 to 5 sentences. Most likely cause and why these numbers point to it, what stops today, the earliest restart date and the gate that decides it, and the one decision the user must make]

## Stop Now

- [fill: pause, with today's date]
- [fill: suppress bounced addresses everywhere]
- [fill: quarantine the batch, no new uploads or cap changes]
- [fill: no new domains or inboxes until the cause is written down]
- [fill: open tracking off]
- [fill: bounce auto-pause lowered to 2%, with the menu path]
- Keep: [fill: warmup at its current setting, the opt-out line, same-day suppression of opt-outs]

## Diagnosis

| Rank | Likely cause | Why it fits your numbers | Confirm with | Clears it |
|-|-|-|-|-|
| 1 | [fill] | [fill] | [fill] | [fill] |
| 2 | [fill] | [fill] | [fill] | [fill] |
| 3 | [fill] | [fill] | [fill] | [fill] |

Run today, in order:

1. [fill: bounce log export, and how to read the code and text]
2. [fill: dig commands for SPF, DKIM, DMARC and the tracking CNAME]
3. [fill: header test]
4. [fill: blocklist lookups for sending and linked domains]
5. [fill: seed test with its named tool or seed accounts]

Fix when confirmed: [fill: each ranked cause's fix written out: SPF and DMARC records ready to paste, the Admin console DKIM path, the tracking CNAME]

## Measurement

[fill: why the open rate cannot decide this (Apple Mail Privacy Protection, Outlook image blocking, security filters) and the three signals that decide it: seed placement, human replies per 1,000 sends, hard bounces with codes]

## List Re-validation

[fill: which rows get re-validated, the count, the cost at $0.00169 per email, how each result is routed, and each source's invalid share]

## Recovery Plan

Standard gate: [fill: hard bounces under 2% over the last 200 sends, zero 4.7.28, spam rate under 0.1%, each with its source, stated once]

| Date | Day | Action | Sends per inbox | Total sends a day | Gate to move on |
|-|-|-|-|-|-|
| [fill] | [fill] | [fill] | [fill] | [fill] | [fill] |

## Resume and Retire Rules

| If | Then |
|-|-|
| [fill: standard gate missed, without restating its numbers] | [fill] |
| [fill: keep, rest or retire, decided by seeds and bounces] | [fill] |

## Next Check-in

[fill: date and time, the numbers to bring, decisions pending; no second list of what would change the ranking]
