# Source Standards

Every fact in a skill that a reader could act on (a sender rule, a protocol detail, a price, a feature, a benchmark) needs a source a reviewer can open and check. This page scores sources from 0 to 5 and sets the minimum score for each kind of fact.

## Owner rules for sources

- **No legal content.** Statutes, regulations, regulator guidance, court rulings and law firm alerts are not sources in this repo, and the facts they support stay out of skills, even when correct. A rule a skill keeps for results (one-click unsubscribe, a spam-rate ceiling) cites the mailbox provider or the RFC that sets it.
- **No moralizing.** A source supports a setting and its number. Do not cite a source to argue that a rule is right; cite it for what happens to replies, placement, pickups or cost when the setting is crossed.

## Strength rubric

| Score | Source | Examples |
|-|-|-|
| 5 | The body that runs the system or writes the standard, in its own words | A mailbox provider's sender documentation (Google, Yahoo, Microsoft), Postmaster Tools and SNDS help pages, an RFC or other published standard, `references/scrapercity-catalog.md` for ScraperCity tools and prices |
| 4 | The vendor's own current documentation for its own product, or a named operator's own published work for their own method | A sequencer's pricing page or help center, an official changelog, an API reference, Alex Berman's own videos and posts for his frameworks |
| 3 | A dated study that states its method and sample size | A call-analytics firm's analysis of a stated number of calls, an industry survey that publishes its sample and questions |
| 2 | Reputable secondary reporting on a level 4 or 5 source | Trade press. Use it to find and date the primary, then cite the primary. |
| 1 | A claim with no method behind it | A vendor's marketing benchmark with no sample, a single practitioner's anecdote, an undated blog post |
| 0 | Not a source | See the last section |

## Minimum score by kind of fact

| Fact | Minimum | Also required |
|-|-|-|
| Mailbox provider sender rules, DNS and email protocols, caller ID and numbering standards | 5 | The provider's page or the RFC or standard number |
| ScraperCity tool, parameter, price, plan or limit | 5 | Taken from the generated catalog or `references/scrapercity-platform.md`, never typed from memory |
| Third-party product feature, price, limit or plan | 4 | The date the page was read, because these change often |
| A named person's method or framework | 4 | Their own published work, not a summary of it |
| Benchmark (reply rate, connect rate, hit rate, conversion) | 3 | Labelled as a planning assumption, with the source's date and sample, and a pilot step that measures the user's own rate |
| Background or context that changes no decision | 2 | Prefer to cut it |

A score 1 source may appear only as an explicitly labelled hypothesis next to a stronger source, and never as the basis for a gate or a price.

## How to cite

- End each reference file with `## Sources`, one bullet per source, publisher and title before the URL: `- Google, Email sender guidelines: https://support.google.com/a/answer/81126`.
- Name the frameworks a skill rests on in `metadata.frameworks` with a year: `"Google - Email sender guidelines (2024)"`.
- Date third-party facts in the text where they are used: "Plan prices as listed on the vendor's pricing page, read 2026-10-13."
- Quote under 15 words, at most once per source. Paraphrase the rest and link it.
- Label numbers a person or vendor reports about themselves as self-reported, and research from a company that sells the tool it measures as vendor research. `references/experts.md` shows the format.

## Keeping sources current

- The weekly CI run fails when the ScraperCity catalog no longer matches the npm package.
- Third-party prices and features older than 12 months are re-read before a minor release. Update the date even when the fact is unchanged.
- A reader who finds a wrong fact opens a "Wrong or stale fact" issue with the file, the line and a source that meets this page.

## What does not count as a source

- Legal texts and commentary on them (owner rule 1, above).
- Output from an AI model, including this repo's own agents.
- Another file in this repo. A skill cannot cite itself or a sibling skill as evidence; cite what that file cites.
- Search result snippets, link previews, and summaries of a page the author did not open.
- Forum threads, social media posts and comment sections.
- Wikipedia as the final citation. Follow it to the source it cites.
- A page that makes the claim without saying where it came from, when the claim is a number.
- A vendor's statements about another vendor's product.
- A screenshot with no URL, a dead link, or an archived copy with no capture date.
- "Common knowledge" or memory of how a tool used to work.
- Paywalled material a maintainer has not read.
