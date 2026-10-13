# Contributing

Pull requests are welcome: new skills, better references, fixes to facts that have gone stale.

## Before you open a pull request

1. Read [docs/SKILL_AUTHORING.md](docs/SKILL_AUTHORING.md). It sets the folder layout, frontmatter, section order, checker contract and copy rules.
2. Take ScraperCity tools, parameters and prices only from `references/scrapercity-catalog.md`. If the product changed, run `node scripts/sync-catalog.mjs` instead of editing prices by hand.
3. Edit shared references only in the repo-root `references/` folder, then run `python3 scripts/materialize-shared-references.py`.
4. Cite primary sources (regulators, mailbox providers, RFCs, vendor docs, the named operator's own work) and date vendor facts.
5. Run everything CI runs:

```bash
python3 scripts/validate-skills.py
node scripts/sync-catalog.mjs --check
python3 scripts/materialize-shared-references.py --check
python3 scripts/generate-readme.py
python3 scripts/generate-lock.py
```

## Adding a skill

- Create `skills/<category>/<name>/` with `SKILL.md`, `references/framework-notes.md`, at least one deeper reference, `templates/output-template.md`, `examples/worked-example.md` and `scripts/check-output.py`.
- The checker must fail the template and pass the worked example.
- Add the skill to the routing matrix in `skills/scrapercity/using-scrapercity-skills/references/routing-matrix.md` and to the `SKILLS` set in that skill's checker.

## Reporting a wrong fact

Open an issue with the file, the line, what it says, what is true, and a link to the source.
