# Framework Notes: scrapercity-cli

Which sources shape this skill, what each one contributes, and which file to open for what.

## Sources and what they contribute

| Source | Type | What it contributes | Where it shows up |
|---|---|---|---|
| `scrapercity` 1.0.17 `bin/cli.mjs` | Vendor code, primary | The 27 commands, every flag, defaults (`maps` 500, `apollo` 1,000, `store-leads` 1,000, `yelp` 10, `angi` 100, `zillow-agents` 10, `bizbuysell` 100, `poll` 15 s and 1 h), printed output, exit codes, parser quirks | SKILL.md, `references/command-reference.md`, `references/gaps-and-quirks.md` |
| `scrapercity` 1.0.17 `lib/client.mjs` | Vendor code, primary | Key lookup (env var, then `~/.scrapercityrc`), owner-only rc file, endpoint per command, GET to POST switch past 6,000 characters for database queries, download default `{runId}.csv` | Command reference, troubleshooting |
| Request capture with a stubbed network (2026-10-13) | Test | The exact JSON each command sends, which exposed the positional-argument quirks | `references/gaps-and-quirks.md` |
| `references/scrapercity-catalog.md` | Generated from the package | Every price and input schema; the official 1.0.17 command list | Cost lines, gaps table |
| `references/scrapercity-agent-patterns.md` | Shared operating rules | Wallet first, count first, a go-ahead before every paid run, polling cadence, errors, safe retry, CSV naming | Workflow, scripts |
| `references/scrapercity-platform.md` | Vendor facts | Plans, database access from Growth, 100 records per request, `excludeDelivered`, `after`, daily allowance | Daily-pull design |
| scrapercity.com/api-docs | Vendor docs | 100 requests a minute per key, 10 concurrent scrapes, results kept 48 hours, allowance resets at midnight UTC | Loops, cron timing |
| npm docs (`npx`) | Tool docs | `--package`, `-y`, version pinning with `name@version` | Script header |
| POSIX `crontab` and Shell Command Language (The Open Group) | Standard | Five-field schedule, minimal job environment, `set -e` behavior | Cron pattern |
| GNU Bash manual | Tool docs | Command substitution does not inherit `set -e` unless `inherit_errexit` is set | `start_run` and `pull_db` error handling |
| util-linux `flock` | Tool docs | Non-blocking lock so a slow run does not overlap the next | Cron pattern |
| curl and jq manuals | Tool docs | `--fail-with-body`, `-G --data-urlencode`, `jq -c`, `@csv` | REST loop |
| GitHub Actions docs | Platform docs | `schedule` in UTC, 5-minute minimum, default branch only, delays under load, 60-day disable in public repos, encrypted secrets | CI pattern |
| AWS Architecture Blog, exponential backoff and jitter | Engineering reference | Retry spacing for 429 and 503 | Error handling (via agent patterns) |

## Routing table

| You need to | Open |
|---|---|
| The syntax, flags, defaults or output of one command | `references/command-reference.md` |
| A loop, poll-and-download, cron job, CSV pipe or CI workflow | `references/scripting-patterns.md` |
| A command or flag the CLI lacks, or a flag combination that misbehaves | `references/gaps-and-quirks.md` |
| A price or input field | `references/scrapercity-catalog.md` |
| Wallet, approval, polling and retry rules | `references/scrapercity-agent-patterns.md` |
| Plan access and daily allowances | `references/scrapercity-platform.md` |
| The deliverable | `templates/output-template.md`, then `scripts/check-output.py` |
| A finished example | `examples/worked-example.md` |

## Decisions this skill makes, and why

| Decision | Reason |
|---|---|
| Pin `scrapercity@1.0.17` in every scheduled job | A new release can change flags or output lines a script parses |
| `npx -y` in scripts | No interactive install prompt in cron or CI |
| Key from the environment in CI and cron; `login` only on a personal machine | Keeps the key out of files that get copied around |
| REST for database rows, CLI for counts and starts | The CLI prints 3 rows per page; the REST response has all of them |
| `--after 0` every day with `--exclude-delivered` | Starts from the beginning and returns only records the account does not have, without skipping |
| `poll --interval 30` or slower | The default 15 s is 240 status calls an hour against a 100 per minute limit shared with everything else on the key |
| Webhook for Apollo, never `poll` | `poll` gives up after one hour; Apollo runs take hours to days |
| An explicit return-on-failure after every substitution inside functions | Bash does not apply `set -e` there |

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://docs.npmjs.com/cli/v10/commands/npx
- https://pubs.opengroup.org/onlinepubs/9799919799/utilities/crontab.html
- https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
- https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
- https://man7.org/linux/man-pages/man1/flock.1.html
- https://curl.se/docs/manpage.html
- https://jqlang.org/manual/
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
- https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
