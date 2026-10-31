# ScraperCity GTM Skills

[![validate](https://github.com/scrapercity/gtm-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/scrapercity/gtm-skills/actions/workflows/validate.yml) [![skills](https://img.shields.io/badge/skills-31-2b6cb0)](#catalog) [![release](https://img.shields.io/github/v/release/scrapercity/gtm-skills)](https://github.com/scrapercity/gtm-skills/releases) [![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-555)](https://agentskills.io/specification) [![license: MIT](https://img.shields.io/badge/license-MIT-black)](LICENSE)

Agent skills for go-to-market work, built on [ScraperCity](https://scrapercity.com) data. **31 skills** that take an agent from "who should we sell to" to a validated list, a sending setup that stays out of spam, copy, calls, replies and the numbers behind it.

Every skill ships a `SKILL.md`, deep references, an output template, a worked example, and a checker script that fails an unfinished deliverable. Every ScraperCity tool, parameter and price comes from a catalog generated from the published [`scrapercity`](https://www.npmjs.com/package/scrapercity) npm package, so the skills match what the product exposes and charges.

Works in Claude Code, the Claude apps, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, goose, Hermes Agent and any other runtime that reads the [Agent Skills](https://agentskills.io/specification) format.

## Why these skills

An agent asked for a lead list or a cold email plan has to get prices, list hygiene, sending limits and copy right, and a wrong guess costs money or a sending domain. These skills give it the specifics: tool names and prices from a catalog generated from the ScraperCity package, a cost estimate before any paid pull, sender settings with the thresholds mailbox providers publish, sendable copy, and a checker script that fails a deliverable until it is finished. Methods come from the operators who published them, and benchmarks carry a date and a sample size.

**Authorities:** the operators, mailbox providers and standards bodies the skills draw on are profiled in [references/experts.md](references/experts.md); the table under [Authorities](#authorities) counts how many skills cite each.

## Install

### Claude Code plugin

```text
/plugin marketplace add scrapercity/gtm-skills
/plugin install gtm-skills@scrapercity
```

Skills load as `gtm-skills:<name>`, for example `gtm-skills:cold-email-strategy`.

### Installer script

```bash
git clone https://github.com/scrapercity/gtm-skills.git
cd gtm-skills
./install.sh                                  # in a terminal: pick agents, scope and skills, then confirm
./install.sh --target cursor --dry-run        # show the plan, write nothing
./install.sh --target all --yes               # 11 targets: Claude Code, Codex, Copilot, Cursor, Gemini CLI, OpenCode, Windsurf, goose, Cline, Hermes, .agents
./install.sh --target codex --scope project   # into ./.agents/skills of the current project
./install.sh --bundle email-from-zero         # a named bundle (./install.sh --list-bundles)
./install.sh --search caller                  # find skills by keyword
./install.sh --target all --update            # after git pull: replace only the skills that changed
./install.sh --dest ~/my-agent/skills         # any other agent's skills folder
```

Existing skill folders are skipped unless you pass `--update` or `--force`; `--uninstall` removes skills. After writing, the installer checks every folder against `skills.lock` and prints `Verified:` per folder. [docs/INSTALL.md](docs/INSTALL.md) lists every flag and bundle, each agent's user and project skills folder with the documentation page it comes from, and `gh skill install` usage. Skills contain small Python checker scripts, so read them before installing, as with any skill.

### Claude apps

```bash
./install.sh --zip ~/Downloads/gtm-skills     # one zip per skill, the skill folder at the zip root
```

Upload each zip in the Claude app's skills settings and turn it on. [docs/INSTALL.md](docs/INSTALL.md#claude-apps-claudeai-and-claude-desktop) has the plan requirements and the description-length note.

### GitHub CLI or by hand

`gh skill install scrapercity/gtm-skills <skill> --agent <agent>` works with GitHub CLI 2.90.0 and later. Or copy any folder under `skills/<category>/` into your agent's skills directory. Each skill carries its own copy of every shared reference it uses, so a single folder works on its own.

## Connect ScraperCity

The skills call ScraperCity through the MCP server, the CLI or the REST API. Get an API key at [app.scrapercity.com](https://app.scrapercity.com), then add the MCP server.

Claude Code:

```bash
claude mcp add scrapercity --scope user --env SCRAPERCITY_API_KEY=your_key -- npx -y --package scrapercity scrapercity-mcp
```

Claude Desktop, Cursor and other JSON-configured clients:

```json
{
  "mcpServers": {
    "scrapercity": {
      "command": "npx",
      "args": ["-y", "--package", "scrapercity", "scrapercity-mcp"],
      "env": { "SCRAPERCITY_API_KEY": "your_key" }
    }
  }
}
```

The `scrapercity-mcp` skill has the setup for every client and a troubleshooting guide. New accounts start with a $5 credit.

## Start here

Load **`using-scrapercity-skills`** first. It reads the request, picks the skills and their order, chooses the cheapest data path (a database your plan includes before a paid scrape), prices the job from the catalog, and sets the wallet and count checks before anything is spent.

| You want | Skills, in order | Install with |
|-|-|-|
| Local businesses by email | `local-business-list`, `cold-email-strategy`, `cold-email-copywriting`, `reply-handling` | `--bundle local-outbound` |
| B2B contacts like your best customers | `icp-list-builder`, `cold-email-list`, `cold-email-strategy`, `cold-email-copywriting`, `reply-handling` | `--bundle b2b-outbound` |
| Buyers at named accounts | `account-researcher`, `decision-maker-finder`, `signal-triggered-outbound`, `multi-channel-outreach` | `--bundle account-based` |
| A cold email setup from zero | `domain-infrastructure`, `inbox-setup`, `email-deliverability`, `sending-platforms` | `--bundle email-from-zero` |
| A calling program | a list skill, `mobile-appender`, `cold-calling` | `--bundle calling` |
| Property owners | `scrapercity-real-estate-data`, `skip-tracer`, `mobile-appender`, `multi-channel-outreach` | `--bundle property-owners` |
| Cost per meeting | `outbound-unit-economics` | `--skill outbound-unit-economics` |

## Catalog

<!-- GENERATED:catalog:start -->
### ScraperCity platform (8)

| Skill | What it does |
|-|-|
| [scrapercity-api](skills/scrapercity/scrapercity-api/SKILL.md) | Builds integrations on the ScraperCity REST API: Bearer auth, every scraper start endpoint, the RUNNING to SUCCEEDED status lifecycle, CSV downloads, webhooks for Apollo and long runs, database paging with the after cursor, POST bodies for long filters, a retry policy that never starts a paid run twice, and a staged bulk pipeline for enriching an existing CSV or CRM export with a batch ledger and result routing. |
| [scrapercity-cli](skills/scrapercity/scrapercity-cli/SKILL.md) | Runs ScraperCity from a terminal with the scrapercity CLI (npm package scrapercity 1.0.17): login and key handling, all 27 commands and their flags, start-poll-download in shell scripts, daily cron pulls of only new records with db-leads and db-local using excludeDelivered and after cursors, CSV piping, and CI jobs. |
| [scrapercity-integrations](skills/scrapercity/scrapercity-integrations/SKILL.md) | Connects ScraperCity to Clay (HTTP API column), n8n (HTTP Request node and Webhook trigger), Zapier (Webhooks by Zapier), Make, Pipedream, Google Sheets, Airtable, HubSpot, Salesforce, Attio, Pipedrive, GoHighLevel, Instantly, Smartlead, Lemlist, EmailBison and ManyReach, including enrichment waterfalls ordered by cost per found record, real-time form enrichment and job-change tracking by Lead Database re-pulls. |
| [scrapercity-lead-database](skills/scrapercity/scrapercity-lead-database/SKILL.md) | Plans and runs pulls from the ScraperCity B2B Lead Database: filter specs, count checks, people-search URL translation, cursor paging, daily pulls of only new leads, and the choice between the database and the Apollo Scraper. |
| [scrapercity-local-business-database](skills/scrapercity/scrapercity-local-business-database/SKILL.md) | Plans and runs pulls from the ScraperCity Local Business Database: Google Maps style keyword and location searches, category and rating filters, map box tiling for metros, named-contact pulls, daily feeds of new businesses, and when to fall back to the Google Maps, Yelp or Angi scrapers. |
| [scrapercity-mcp](skills/scrapercity/scrapercity-mcp/SKILL.md) | Installs, verifies and operates the ScraperCity MCP server (npm package scrapercity, binary scrapercity-mcp) in Claude Code, Claude Desktop, Codex, Cursor, Windsurf, Cline, Gemini CLI, GitHub Copilot, OpenCode, Goose, Zed, Hermes Agent and Perplexity (plus the ChatGPT custom GPT path), sets which tools ask before running, then runs its 25 tools under the agent rules: wallet first, count before pull, start-poll-download, Apollo by webhook, a miss is unknown. |
| [scrapercity-real-estate-data](skills/scrapercity/scrapercity-real-estate-data/SKILL.md) | Plans and runs ScraperCity real estate pulls: Zillow agent lists, property lookups with owner contact, distressed property lists (pre-foreclosure, foreclosure, auction, bank-owned), Crexi commercial listings, BizBuySell businesses for sale, and People Finder for owner contact. |
| [using-scrapercity-skills](skills/scrapercity/using-scrapercity-skills/SKILL.md) | Routes any lead generation, list building or outbound request to the right ScraperCity skills in the right order, picks the cheapest tool path, prices it from the live catalog, and sets the wallet, count, suppression, quality and deliverability gates before anything is spent or sent. |

### List building (12)

| Skill | What it does |
|-|-|
| [account-researcher](skills/list-building/account-researcher/SKILL.md) | Builds a one-page brief on a target company and its key people before outreach or a call: firmographics and team counts from the Lead Database, the people who own the decision with verified emails, the technologies that change the pitch (checked with Tech Stack Search only when they do), dated trigger events, and talking points that each cite a source. |
| [cold-email-list](skills/list-building/cold-email-list/SKILL.md) | Takes target domains or an ICP and produces a send-ready CSV for a cold email sequencer. |
| [crm-enricher](skills/list-building/crm-enricher/SKILL.md) | Fills missing emails, mobiles, job titles and company fields in a HubSpot, Pipedrive, GoHighLevel or Salesforce export using ScraperCity Lead Database lookups (by companyDomain, companyName or socialUrl), Email Finder, Mobile Finder and Website Finder, with one cost-ordered ladder per field and Tech Stack Search flags for technographics. |
| [decision-maker-finder](skills/list-building/decision-maker-finder/SKILL.md) | Finds the people who own a buying decision at a given list of companies or domains, maps each to a buying role (economic buyer, champion, technical evaluator), sizes the committee to the deal, and returns verified work emails and, on request, mobile numbers for reps who call. |
| [ecommerce-by-techstack](skills/list-building/ecommerce-by-techstack/SKILL.md) | Builds a list of online stores filtered by platform, category, installed Shopify apps, technologies, location, social presence and estimated traffic, sales or headcount bands with ScraperCity Store Leads ($0.0039 per lead, band filters applied server-side), intersects or excludes a second technology with Tech Stack Search ($4.99 per technology), keeps only stores with an email, validates them, tiers them by size and exports a CSV. |
| [email-list-cleaner](skills/list-building/email-list-cleaner/SKILL.md) | Cleans an old or inherited email list before anyone sends to it: repairs syntax, dedupes, applies suppression, flags role and free-provider addresses, validates every unique address with ScraperCity's Email Validator, and splits the result into send-ready, catch-all, hold and removed files with a reason on every dropped row. |
| [icp-list-builder](skills/list-building/icp-list-builder/SKILL.md) | Builds a list of the people who decide on a purchase at companies that fit an ICP, and answers how many companies and contacts exist, how to tier them, what it costs and how to get verified emails. |
| [local-business-list](skills/list-building/local-business-list/SKILL.md) | Builds a send-ready list of local businesses for a category and area. |
| [mobile-appender](skills/list-building/mobile-appender/SKILL.md) | Turns LinkedIn profile URLs or work emails into a dialer-ready calling list with ScraperCity Mobile Finder ($0.25 per number found, nothing when none is found). |
| [recruiting-sourcer](skills/list-building/recruiting-sourcer/SKILL.md) | Sources candidates by role, seniority, location and target companies from the ScraperCity Lead Database (title, notTitle, seniority, department, companyName, companyDomain and location filters) or from an Apollo people-search URL (scrape_apollo, 500 to 50,000 leads at $0.0039 each, usually delivered in 15 to 30 minutes through a webhook), removes people at the hiring company and do-not-poach accounts, tiers the shortlist, then adds verified emails (find_emails, validate_emails) and mobiles for the top tier (find_mobiles), with first messages for candidates. |
| [skip-tracer](skills/list-building/skip-tracer/SKILL.md) | Turns names, phone numbers, emails or property addresses into current phones, emails and addresses with ScraperCity People Finder ($0.0199 per result; a search with 0 matches is billed as 1 result) and Property Lookup ($0.15 per property, plus $0.10 for owner contact), with Distress List as a lead feed. |
| [tam-builder](skills/list-building/tam-builder/SKILL.md) | Builds a company-level market file: every account in a defined market, counted, pulled, deduped across sources and outside lists, with a coverage estimate, TAM/SAM/SOM in accounts and dollars, and on request a fit score and Tier 1 to 3 cut to team capacity. |

### Outbound (11)

| Skill | What it does |
|-|-|
| [cold-calling](skills/outbound/cold-calling/SKILL.md) | Builds a B2B or local-business cold calling program: a call list from ScraperCity phone fields and find_mobiles, dial order by number type, dialer and caller ID setup that keeps pickups high, call blocks with a dials-to-meetings funnel, an opener-reason-question-ask script, an objection bank, voicemail and gatekeeper scripts, and CRM logging. |
| [cold-email-copywriting](skills/outbound/cold-email-copywriting/SKILL.md) | Writes cold email sequences that get positive replies: bodies under 100 words with one ask, that say who is writing and name the segment (city, building class, category, platform), carry the strongest proof in email 1 and a concrete offer worth replying for, answer the buyer's first objection head-on, and give every follow-up a new reason to reply. |
| [cold-email-strategy](skills/outbound/cold-email-strategy/SKILL.md) | Plans a cold email campaign from list to booked meeting: campaign cells (one segment, one offer, one trigger), a concrete offer, a touch map with every email and reply written out, exact sequencer settings with a ramp, inbox capacity back-solved from the meeting goal, all-in cost per meeting, a dated test plan, owners and a 90-day launch calendar. |
| [domain-infrastructure](skills/outbound/domain-infrastructure/SKILL.md) | Plans and specifies the sending infrastructure for cold email: how many secondary domains and mailboxes a volume target needs, 2 or 3 per domain, Google Workspace and Microsoft 365 split by the measured recipient mix, your own tenants or resold inboxes, tenant settings, domain names, the exact SPF, DKIM, DMARC (with rua), MX, tracking and Postmaster records, warmup settings, dated launch paths including a wide build that meets the requested date, monitoring thresholds and a cost estimate. |
| [email-deliverability](skills/outbound/email-deliverability/SKILL.md) | Keeps a running cold email program in the inbox: a pre-send gate (authentication, one-click unsubscribe, list validation with ScraperCity's Email Validator and a rule for every result, catch-all handling), weekly monitoring with seed tests, Google Postmaster Tools, Yahoo CFL, Microsoft SNDS and blocklist checks, an incident runbook for bounce spikes, spam folder placement, complaint spikes and blocklisted domains, and hard stop rules tied to the Google, Yahoo and Microsoft sender requirements. |
| [inbox-setup](skills/outbound/inbox-setup/SKILL.md) | Sets up each cold email mailbox after the domains exist: sender identity tied to a person on the team, address format, display name, plain-text signature with an opt-out line, profile photo, account security, Google Workspace and Microsoft 365 connection settings, reply routing, warmup on a 21-day standard path or a 14-day soft start, sending windows, daily caps, tenant quota checks, reply monitoring, rotation and retirement. |
| [multi-channel-outreach](skills/outbound/multi-channel-outreach/SKILL.md) | Builds outbound sequences that combine cold email with phone calls (mobile numbers from ScraperCity's Mobile Finder), manual LinkedIn touches and direct mail to business or property addresses. |
| [outbound-unit-economics](skills/outbound/outbound-unit-economics/SKILL.md) | Builds the unit economics of an outbound program: cost per lead, verified email, mobile, conversation, meeting, opportunity and deal, using ScraperCity catalog prices and plan credits (Starter $49 with $49 credits, Growth $149 with $159, Scale $649 with $800), a dated tool stack, a loaded SDR cost and AE time per meeting. |
| [reply-handling](skills/outbound/reply-handling/SKILL.md) | Classifies and answers cold email replies: interested, price questions, referrals, objections (too expensive, competitor, our system already does it, in-house, no need), not now, unsubscribe, hostile, out of office and bounce. |
| [sending-platforms](skills/outbound/sending-platforms/SKILL.md) | Chooses and configures the sequencer for cold email: Instantly, Smartlead, Lemlist, EmailBison, ManyReach, HubSpot sequences or Apollo sequences, with every feature and price taken from the vendor's own page and dated. |
| [signal-triggered-outbound](skills/outbound/signal-triggered-outbound/SKILL.md) | Builds outbound that fires on dated events: new local listings, review and rating changes, tech installs and removals (Tech Stack Search), store apps and traffic bands, businesses for sale, pre-foreclosures, agents new to a market and new-to-account records from ScraperCity pulls; plus website visitors, job changes, new leaders, funding and Form D filings, job posts, earnings and SEC filings, competitor and account launches, events, webinars, third-party category intent and social engagement from public feeds or the user's tools. |
<!-- GENERATED:catalog:end -->

## What every skill ships

```text
skills/<category>/<skill>/
├── SKILL.md                     # loaded when the skill triggers
├── references/                  # framework notes, playbooks, recipe libraries, runbooks
├── templates/output-template.md # the deliverable shell
├── examples/worked-example.md   # a complete deliverable with real catalog prices
└── scripts/check-output.py      # PASS or FAIL on a finished deliverable
```

Run a checker on any deliverable:

```bash
python3 skills/list-building/local-business-list/scripts/check-output.py my-list-report.md
```

Checkers use only the Python standard library. Each one fails the unfilled template and passes the worked example, and each adds checks specific to its skill: email bodies under 90 words, units times price equals cost, every touch with a branch, and so on.

<!-- GENERATED:inventory:start -->
| Inventory | Count |
|-|-:|
| Skills | 31 |
| Categories | 3 |
| Skill-owned reference files | 132 |
| Shared reference files (repo root, copied into each skill that uses them) | 9 |
| Output templates | 35 |
| Worked examples | 38 |
| Deliverable checkers | 32 |
| Common Pitfalls rows (references/pitfalls-index.md) | 457 |
| Total packaged files | 400 |
| Lines of Markdown (shared references counted once) | 41,993 |
<!-- GENERATED:inventory:end -->

## Authorities

How many skills name each authority from [references/experts.md](references/experts.md) in their `metadata.frameworks`.

<!-- GENERATED:authorities:start -->
| Authority | Skills that name them in `frameworks` |
|-|-:|
| Alex Berman | 21 |
| Google | 17 |
| Yahoo | 14 |
| Instantly | 11 |
| Microsoft | 9 |
| Hunter | 7 |
| Craig Elias | 4 |
| M3AAWG | 4 |
| Ryan Reisert | 4 |
| April Dunford | 3 |
| Jordan Crawford | 3 |
| Gong Labs | 2 |
| Ronen Pessar | 2 |
| Spamhaus | 2 |
| Armand Farrokh and Nick Cegelski | 1 |
| Belkins | 1 |
| Cognism | 1 |
| Eric Nowoslawski | 1 |
| Jason Bay | 1 |
| Jeb Blount | 1 |
| Joey Gilkey | 1 |
| Josh Braun | 1 |
| Lars Nilsson | 1 |
| Leslie Venetz | 1 |
| Tom Slocum | 1 |
<!-- GENERATED:authorities:end -->

## How the content is kept honest

- **Prices and tools are generated.** `scripts/sync-catalog.mjs` reads the published npm package and writes `references/scrapercity-catalog.md`. CI fails when the committed catalog no longer matches the package's tools, prices or CLI commands, and a weekly scheduled run catches a release that changed them. A release that changes only the version number leaves the catalog as it is.
- **Named sources.** Sender rules come from the mailbox providers (Google, Yahoo, Microsoft), protocols from the RFCs, vendor features from the vendor's own docs, and methods from the operator's own published work, each dated. Every reference file ends with its sources.
- **Benchmarks are hypotheses.** Hit rates, reply rates and connect rates are labelled as planning assumptions with a source and a date, and the skills tell the agent to measure its own rate with a small pilot before a large run.
- **Rules are settings.** Every rule in a skill is a setting tied to replies, meetings, revenue or cost, with its number.
- **Integrity.** `skills.lock` holds a SHA-256, size and kind for every packaged file, and the installer verifies what it writes. [docs/INTEGRITY.md](docs/INTEGRITY.md) covers what a match proves.
- **No telemetry: static files and local scripts only.** Checkers use the Python standard library and stay offline. The one repo script that reads the network is the catalog sync, against the public npm registry.

## Validate

```bash
scripts/check-all.sh                 # every check CI runs, in CI order
scripts/check-all.sh --offline       # without the npm catalog check
scripts/check-all.sh --strict        # adds the Agent Skills spec and hygiene checks
scripts/regenerate.sh                # rewrite every generated file after a change
```

`check-all.sh` runs the skill validator, `check-repo.py`, the shared-reference, index, README and lock checks, the catalog check, shellcheck and `claude plugin validate --strict`, and reports any tool it could not find as skipped. Requires Python 3.9+ with PyYAML, and Node 18+ for the catalog sync.

## Docs

- [docs/INSTALL.md](docs/INSTALL.md): installer flags, bundles, every agent's skills folder with its source, Claude app zips, `gh skill install`.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): repo layout, which files are generated, every script, shared-reference copies, catalog sync, the lock.
- [docs/SKILL_AUTHORING.md](docs/SKILL_AUTHORING.md): the owner rules and how to write a skill.
- [docs/QUALITY_BAR.md](docs/QUALITY_BAR.md): what every skill must contain and the checker contract.
- [docs/SOURCE_STANDARDS.md](docs/SOURCE_STANDARDS.md): the 0 to 5 source rubric and what does not count as a source.
- [docs/INTEGRITY.md](docs/INTEGRITY.md): what `skills.lock` proves and what it does not.
- [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md): checks, version bumps, tags and semver rules.
- [docs/REPO_TOPICS.md](docs/REPO_TOPICS.md): the GitHub topics and the command that sets them.
- [references/pitfalls-index.md](references/pitfalls-index.md) and [taxonomy.csv](taxonomy.csv): every Common Pitfalls row in one file, and one row per skill with its version, description, links, frameworks, tools and prices.
- [references/glossary.md](references/glossary.md): deliverability, data, phone and program terms with their primary sources.
- [AGENTS.md](AGENTS.md), [GOVERNANCE.md](GOVERNANCE.md), [SUPPORT.md](SUPPORT.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), [SECURITY.md](SECURITY.md), [CITATION.cff](CITATION.cff), [CHANGELOG.md](CHANGELOG.md).

## Related

- [scrapercity.com/skills](https://scrapercity.com/skills): short versions of 12 list-building skills. The list-building category here holds the full versions.
- [scrapercity/scrapercity-cli](https://github.com/scrapercity/scrapercity-cli): the MCP server and CLI the skills call.
- [ScraperCity API docs](https://scrapercity.com/api-docs).

## Contributing

Two owner rules come first for every contribution:

- **No legal content.** No laws, regulations, regulators, fines, registries, consent or registration requirements, disclaimers or advice to get legal review in any skill, even when correct.
- **No moralizing.** A skill says what to do to get more replies, meetings and revenue at lower cost; every rule is a setting tied to results.

Then see [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/SKILL_AUTHORING.md](docs/SKILL_AUTHORING.md). `python3 scripts/new-skill.py <category> <name>` scaffolds a new skill. Every pull request runs the checks above.

## License

[MIT](LICENSE)
