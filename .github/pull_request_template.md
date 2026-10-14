## What changed

## Owner rules

- [ ] **No legal content.** No law, regulation, regulator, fine, registry, consent or registration requirement, disclaimer or advice to get legal review was added to any skill. `python3 scripts/validate-skills.py --check-legal` shows no new lines for the skills I touched.
- [ ] **No moralizing.** Every rule I added is a setting tied to replies, meetings, revenue or cost, with its number. No "reason" columns, brand, respect or safety framing.

## Checks

- [ ] `scripts/regenerate.sh` ran, so `README.md`, `AGENTS.md`, `references/pitfalls-index.md`, `taxonomy.csv`, the manifests and `skills.lock` are current
- [ ] `scripts/check-all.sh` passes (or `--offline`, with the catalog check left to CI)
- [ ] Prices and tools come from `references/scrapercity-catalog.md`
- [ ] Shared references edited only at the repo root
- [ ] New facts cite a primary source that meets `docs/SOURCE_STANDARDS.md`
- [ ] Worked examples are labelled "Illustrative example" and use `.example` domains
- [ ] For a changed checker: I ran one broken deliverable through it and it failed
