# Contributing

Pull requests are welcome: new skills, better references, fixes to facts that have gone stale, and tooling.

## Owner rules

Two rules from the repo owner (October 13, 2026) come before everything else on this page:

1. **No legal content.** Skills name no law, regulation, regulator, court ruling, fine, registry, consent or registration requirement, carry no disclaimers, and never send the reader to get legal review. Leave it out even when it is correct. A pull request that adds any of it is sent back.
2. **No moralizing.** A skill says what to do to get more replies, meetings and revenue at lower cost. Write each rule as a setting with its number (stop the sequence on reply; keep spam complaints under Google's 0.3%). Delete any rule you cannot tie to results, and leave out framing about the brand, respecting prospects, not annoying people or safety.

[docs/SKILL_AUTHORING.md](docs/SKILL_AUTHORING.md#owner-rules) has the full wording and examples.

## Before you open a pull request

1. Read [docs/SKILL_AUTHORING.md](docs/SKILL_AUTHORING.md). It sets the folder layout, frontmatter, section order, checker contract and copy rules. [docs/QUALITY_BAR.md](docs/QUALITY_BAR.md) is the acceptance list a reviewer uses, and [docs/SOURCE_STANDARDS.md](docs/SOURCE_STANDARDS.md) says which sources count.
2. Take ScraperCity tools, parameters and prices only from `references/scrapercity-catalog.md`. If the product changed, run `node scripts/sync-catalog.mjs` instead of editing prices by hand.
3. Edit shared references only in the repo-root `references/` folder.
4. Cite primary sources (mailbox providers, RFCs, vendor docs, the named operator's own work) and date vendor facts.
5. Regenerate, then run everything CI runs:

```bash
scripts/regenerate.sh
scripts/check-all.sh --offline       # drop --offline to include the npm catalog check
```

Turn on the pre-commit hook once per clone so a commit never carries a stale generated file, a dash, a restricted name or a secret:

```bash
git config core.hooksPath .githooks
```

## Adding a skill

```bash
python3 scripts/new-skill.py <category> <name>
```

That writes `SKILL.md` with every section in order, `references/framework-notes.md`, `templates/output-template.md`, `examples/worked-example.md` and a `scripts/check-output.py` that already meets the checker contract, all marked `[fill]`. Then:

- Fill every `[fill]` and add at least one deeper reference.
- The checker must fail the template and pass the worked example.
- Add the skill to the routing matrix in `skills/scrapercity/using-scrapercity-skills/references/routing-matrix.md`, to the `SKILLS` set in that skill's checker, and to a bundle in `install.sh` if it belongs in one.
- Run `python3 scripts/validate-skills.py <category>/<name> --strict --check-legal` until it passes.

## Reporting a wrong fact

Open a "Wrong or stale fact" issue with the file, the line, what it says, what is true, and a link to the source.

## License

Contributions are accepted under the repo's [MIT license](LICENSE). Quote outside material under 15 words with a link, paraphrase the rest, and do not add files you lack the rights to share.
