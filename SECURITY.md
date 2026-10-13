# Security

Skills in this repo contain Markdown and small Python checker scripts. The checkers use only the Python standard library and make no network calls. The repo-level tooling (`scripts/sync-catalog.mjs`) reads the public npm registry.

- Never commit an API key. Skills read `SCRAPERCITY_API_KEY` from the environment or the CLI's `~/.scrapercityrc`.
- Verify an install against `skills.lock`: `python3 scripts/generate-lock.py --verify ~/.claude/skills`.
- Report a vulnerability privately to support@scrapercity.com rather than in a public issue.
