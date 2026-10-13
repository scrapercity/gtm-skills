# Notes for agents working in this repo

- Skills live in `skills/<category>/<skill>/`. The router is `skills/scrapercity/using-scrapercity-skills`.
- The authoring standard is `docs/SKILL_AUTHORING.md`. `python3 scripts/validate-skills.py` must pass before any commit.
- ScraperCity tools and prices come only from `references/scrapercity-catalog.md`, which `scripts/sync-catalog.mjs` generates. Do not edit it by hand.
- Shared references are edited only at the repo root `references/`; run `python3 scripts/materialize-shared-references.py` afterwards.
- Regenerate `README.md` and `skills.lock` with `scripts/generate-readme.py` and `scripts/generate-lock.py` after any change to a skill.
- Copy rules: no em or en dashes, no vendor or infrastructure names describing how ScraperCity works, no invented tools, prices or statistics.
