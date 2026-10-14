# Using ScraperCity Skills - Framework Notes

Which sources shape the router, what each one contributes, and which file to open for which question.

## Sources and what they contribute

| Source | Contribution | Where it shows up |
|-|-|-|
| ScraperCity tool catalog, generated from the `scrapercity` npm package 1.0.17 | Tool ids, endpoints, input schemas and per-result prices | Step 3 (cheapest path), step 4 (pricing), the checker's price table |
| scrapercity.com/pricing and scrapercity.com/llm-info | Plan tiers ($49, $149, $649), monthly credits, which plans include the databases | Prerequisites, the Starter vs Growth comparison |
| ScraperCity Lead Database and Local Business Database API docs (AGENT_DOCS in the npm package) | 100,000 new records a day, free re-fetch of records already delivered, `excludeDelivered`, `after` cursors | Step 3, the repeat-pull chains |
| Agent Skills specification, agentskills.io | Progressive disclosure: load a skill's body only when its step starts | Step 6 (handoff) and the "load every skill up front" pitfall |
| Alex Berman, alexberman.com | Targeting and offer carry most of the result, so the chain fixes list and offer before copy | Chain order in `references/chains.md` |
| Google, Email sender guidelines and FAQ | One-click unsubscribe for bulk mail, unsubscribes processed within 48 hours, spam rate under 0.1% and never 0.3% or higher | Suppression and deliverability gates |
| Yahoo, Sender Hub best practices | A working list-unsubscribe header with one-click support, unsubscribes honored within 2 days, spam rate below 0.3% | Suppression gate |
| `scrapercity-api` bulk pipeline, `scrapercity-integrations` waterfall and job-change recipes | Stage order for existing files, cost-per-found ordering, `socialUrl` re-pulls | Chains 10 and 11, routing rows |
| `docs/INSTALL.md` in this repo | Installer flags, bundles, agent folders, the Claude Code plugin | Install section |

## Routing table

| Question | Open |
|-|-|
| Which skill handles this phrase? | `references/routing-matrix.md` |
| What order do the skills run in for a full program? | `references/chains.md` |
| What does a tool cost, and what inputs does it take? | `references/scrapercity-catalog.md` |
| Does this plan tier include the databases? | `references/scrapercity-platform.md` |
| How do I poll, page, retry and handle errors? | `references/scrapercity-agent-patterns.md` |
| Is this list ready to send? | `references/list-quality-standard.md` |
| What should the deliverable look like? | `templates/output-template.md`, then `examples/worked-example.md` |
| Is my routing plan complete? | `scripts/check-output.py` |

## Routing principles

1. **Outcome first.** Route on what the user wants to happen (meetings, a market count, a clean CRM), not on the tool they named.
2. **Included before paid.** A database the plan includes beats any per-result scraper for the same records.
3. **Pay-on-find before pay-per-search.** Email Finder and Mobile Finder charge only on a hit, so they come before People Finder, which bills a 0-match search as 1 result.
4. **List and offer before words.** Copy, sequences and call scripts wait for the list and the offer.
5. **Gate before spend, gate before send.** Wallet and count before any paid pull; suppression and validation before any send or dial.
6. **One skill in context at a time.** Finish a skill's deliverable and its check, then load the next.
7. **One owner per deliverable.** Exactly one skill owns the final file or plan; every other skill feeds it an input or checks it.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/pricing
- https://scrapercity.com/llm-info
- https://scrapercity.com/skills
- https://agentskills.io/specification
- https://alexberman.com
- https://support.google.com/a/answer/81126
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
