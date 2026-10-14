# Governance

## Who maintains the repo

ScraperCity maintains this repo. The ScraperCity team has write access to `main`, reviews contributions, cuts releases and decides what merges. Outside contributors propose changes through issues and pull requests. Reach the maintainers at support@scrapercity.com.

## Owner rules

The repo owner set two rules on October 13, 2026. They override every other line in this repo, and a maintainer rejects a change that breaks either one:

1. **No legal content.** No law, regulation, regulator, court ruling, fine, registry, consent or registration requirement, disclaimer, or advice to get legal review in any skill, even when correct.
2. **No moralizing.** Skills say what to do to get more replies, meetings and revenue at lower cost. Every rule is a setting tied to results, with its number; a rule that cannot be tied to results is deleted.

## How a change gets in

Every change, from a maintainer or a contributor, meets the same five conditions before it reaches `main`:

1. **The checks pass.** `scripts/check-all.sh` passes locally, and the `validate` workflow (the same checks plus a full install of every target on Linux and macOS) is green. A red run does not merge.
2. **The owner rules hold.** `python3 scripts/validate-skills.py --check-legal` prints no legal-term lines for the changed skills, and the reviewer reads the diff for moralizing.
3. **Facts have a primary source.** A new or changed sender rule, price, feature or benchmark cites a source that meets [docs/SOURCE_STANDARDS.md](docs/SOURCE_STANDARDS.md). ScraperCity tools and prices come from the generated catalog and are never typed by hand.
4. **A maintainer reviews it** against [docs/QUALITY_BAR.md](docs/QUALITY_BAR.md), reads any changed checker script, and runs a broken deliverable through it.
5. **Generated files are current.** `scripts/regenerate.sh` ran in the same change.

## How decisions are made

Maintainers decide in the pull request or issue thread. When two readings conflict, the one with the stronger source wins. When the sources are equal, the reading that books more meetings in a measured test wins; until a test exists, the maintainer picks one, labels it a planning assumption, and says in the thread what result would change it. A rejected proposal gets a reason in the thread.

## Wrong facts

A wrong fact is fixed before new features. Open a "Wrong or stale fact" issue with the file, the line and a source. A confirmed wrong price or tool id ships as a patch release, as described in [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md).

## Changes to this document

Changes to governance go through a pull request like any other change.
