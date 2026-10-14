# Support

## Where to go

| You need | Go to |
|-|-|
| Help with your ScraperCity account, billing, an API key or a failed run | support@scrapercity.com |
| To report a wrong price, sender rule, feature or statistic in a skill | A "Wrong or stale fact" issue on this repo, with the file, the line and a source |
| To report a bug in `install.sh`, a checker or a validator | A "Bug" issue on this repo, with the command you ran and its full output |
| To suggest a better skill, reference or checker | An "Improvement" issue |
| To propose a new skill | A "Skill request" issue |
| To report a security problem | support@scrapercity.com, privately. See [SECURITY.md](SECURITY.md). |

Remove API keys and personal data from anything you paste into an issue. Issues are public.

## Before you open an issue

- Install problems: read [docs/INSTALL.md](docs/INSTALL.md) and run `./install.sh --dry-run` with the same flags to see the folders it would write. `./install.sh --list-targets` prints every target's folders.
- An installed skill behaves differently from the repo: run `python3 scripts/generate-lock.py --verify <skills folder>` from a clone at the same release and include the MISMATCH lines.
- A skill output fails its checker: run `python3 skills/<category>/<skill>/scripts/check-output.py <your file>` and include the FAIL lines.
- Prices: compare against `references/scrapercity-catalog.md` in the latest release before reporting. That file is generated from the published `scrapercity` npm package.
- A check fails on your clone: run `scripts/check-all.sh --offline` and paste its output.

## What the skills cover, and what they leave out

The skills cover what gets more replies, meetings and revenue at lower cost: lists, data, sending setup, copy, calls, replies and the numbers. Two owner rules shape what you will not find in them, and an issue asking to add either is closed:

- **No legal content.** No laws, regulators, registries, consent or registration requirements, disclaimers or advice to get legal review.
- **No moralizing.** No rules justified as good behavior. Each rule is a setting tied to results.
