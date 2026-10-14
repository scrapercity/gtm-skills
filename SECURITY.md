# Security

## What runs

- **Skills** contain Markdown and one small Python checker each. The checkers use only the Python standard library, read only the file they are given, and make no network calls. Read `scripts/check-output.py` in a skill before you run it, as with any code.
- **Repo tooling** (`install.sh`, `scripts/`) runs only when you call it. The one script that reads the network is `scripts/sync-catalog.mjs`, which downloads the public `scrapercity` npm package. `generate-lock.py` asks the local `git` for the current commit and nothing else.
- **No telemetry.** Nothing in this repo reports usage anywhere.

## Keys

- Never commit an API key. Skills read `SCRAPERCITY_API_KEY` from the environment or the CLI's `~/.scrapercityrc`; examples use placeholders such as `your_key`.
- `scripts/check-repo.py`, the pre-commit hook and CI fail on anything shaped like a private key, a cloud, GitHub, Slack, Google, payment or model API key, or a literal ScraperCity key, without printing the value.
- If a key was committed, treat it as exposed: stop using it and ask support@scrapercity.com to revoke it. Deleting the file does not remove it from git history or forks.

## Verify what you installed

```bash
python3 scripts/generate-lock.py --verify ~/.claude/skills
```

Use a clone checked out at the release you installed. [docs/INTEGRITY.md](docs/INTEGRITY.md) explains what a match proves and what it does not.

## Supported versions

Fixes land on `main` and ship in the next release. Install from the latest release tag.

## Report a vulnerability

Email support@scrapercity.com with "Security" in the subject, the affected file or command, the release or commit, and the smallest reproduction you have. Do not open a public issue, and do not include live keys or personal data.
