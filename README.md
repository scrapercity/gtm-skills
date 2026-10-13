# ScraperCity GTM Skills

Agent skills for go-to-market work, built on [ScraperCity](https://scrapercity.com) data. **31 skills** that take an agent from "who should we sell to" to a validated list, a sending setup that stays out of spam, copy, calls, replies and the numbers behind it.

Every skill ships a `SKILL.md`, deep references, an output template, a worked example, and a checker script that fails an unfinished deliverable. Every ScraperCity tool, parameter and price comes from a catalog generated from the published [`scrapercity`](https://www.npmjs.com/package/scrapercity) npm package, so the skills cannot drift from what the product exposes and charges.

Works in Claude Code, Claude Desktop, Codex, GitHub Copilot, Cursor, Gemini CLI, Windsurf, Cline, OpenCode, Goose and any other runtime that reads the [Agent Skills](https://agentskills.io/specification) format.

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
./install.sh --dry-run                       # show what would be copied, write nothing
./install.sh                                 # all skills into ~/.claude/skills
./install.sh --scope project                 # into ./.claude/skills of the current project
./install.sh --category list-building        # one category
./install.sh --skill local-business-list     # one skill
./install.sh --dest ~/.codex/skills          # any agent's skills folder
```

Existing skill folders are skipped unless you pass `--force`. Skills contain small Python checker scripts, so read them before installing, as with any skill.

### By hand

Copy any folder under `skills/<category>/` into your agent's skills directory. Each skill carries its own copy of every shared reference it uses, so a single folder works on its own.

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

Load **`using-scrapercity-skills`** first. It reads the request, picks the skills and their order, chooses the cheapest data path (a database your plan includes before a paid scrape), prices the job from the catalog, and sets the wallet, count and compliance gates before anything is spent.

| You want | Skills, in order |
|-|-|
| Local businesses by email | `local-business-list`, `cold-email-strategy`, `cold-email-copywriting`, `sending-platforms` |
| B2B contacts like your best customers | `icp-list-builder`, `cold-email-list`, `cold-email-copywriting` |
| Buyers at named accounts | `decision-maker-finder`, `account-researcher`, `multi-channel-outreach` |
| A cold email setup from zero | `domain-infrastructure`, `inbox-setup`, `email-deliverability`, `sending-platforms` |
| A calling program | a list skill, `mobile-appender`, `cold-calling` |
| Property owners | `scrapercity-real-estate-data`, `skip-tracer`, `multi-channel-outreach` |
| Cost per meeting | `outbound-unit-economics` |

## Catalog

<!-- GENERATED:catalog:start -->
### ScraperCity platform (8)

| Skill | What it does |
|-|-|
| [scrapercity-api](skills/scrapercity/scrapercity-api/SKILL.md) | Builds integrations on the ScraperCity REST API: Bearer auth, every scraper start endpoint, the RUNNING to SUCCEEDED status lifecycle, CSV downloads, webhooks for Apollo and long runs, database paging with the after cursor, POST bodies for long filters, and a retry policy that never starts a paid run twice. |
| [scrapercity-cli](skills/scrapercity/scrapercity-cli/SKILL.md) | Runs ScraperCity from a terminal with the scrapercity CLI (npm package scrapercity 1.0.17): login and key handling, all 27 commands and their flags, start-poll-download in shell scripts, daily cron pulls of only new records with db-leads and db-local using excludeDelivered and after cursors, CSV piping, and CI jobs. |
| [scrapercity-integrations](skills/scrapercity/scrapercity-integrations/SKILL.md) | Connects ScraperCity to Clay (HTTP API column), n8n (HTTP Request node and Webhook trigger), Zapier (Webhooks by Zapier), Make, Pipedream, Google Sheets, Airtable, HubSpot, Pipedrive, GoHighLevel, Instantly, Smartlead, Lemlist, EmailBison and ManyReach. |
| [scrapercity-lead-database](skills/scrapercity/scrapercity-lead-database/SKILL.md) | Plans and runs pulls from the ScraperCity B2B Lead Database: filter specs, count checks, people-search URL translation, cursor paging, daily pulls of only new leads, and the choice between the database and the Apollo Scraper. |
| [scrapercity-local-business-database](skills/scrapercity/scrapercity-local-business-database/SKILL.md) | Plans and runs pulls from the ScraperCity Local Business Database: Google Maps style keyword and location searches, category and rating filters, map box tiling for metros, named-contact pulls, daily feeds of new businesses, and when to fall back to the Google Maps, Yelp or Angi scrapers. |
| [scrapercity-mcp](skills/scrapercity/scrapercity-mcp/SKILL.md) | Installs, verifies and operates the ScraperCity MCP server (npm package scrapercity, binary scrapercity-mcp) in Claude Code, Claude Desktop, Cursor, Windsurf, Cline, Gemini CLI and GitHub Copilot, then runs its 25 tools under the agent rules: wallet first, count before pull, start-poll-download, Apollo by webhook. |
| [scrapercity-real-estate-data](skills/scrapercity/scrapercity-real-estate-data/SKILL.md) | Plans and runs ScraperCity real estate pulls: Zillow agent lists, property lookups with owner contact, distressed property lists (pre-foreclosure, foreclosure, auction, bank-owned), Crexi commercial listings, BizBuySell businesses for sale, and People Finder for owner contact. |
| [using-scrapercity-skills](skills/scrapercity/using-scrapercity-skills/SKILL.md) | Routes any lead generation, list building or outbound request to the right ScraperCity skills in the right order, picks the cheapest tool path, prices it from the live catalog, and sets the wallet, count and compliance gates before anything is spent. |

### List building (12)

| Skill | What it does |
|-|-|
| [account-researcher](skills/list-building/account-researcher/SKILL.md) | Builds a one-page brief on a target company and its key people before outreach or a call: firmographics and team counts from the Lead Database, the 3-4 people who own the decision with verified emails, the technologies that change the pitch (checked with Tech Stack Search only when they do), dated trigger events, and talking points that each cite a source. |
| [cold-email-list](skills/list-building/cold-email-list/SKILL.md) | Takes target domains or an ICP and produces a send-ready CSV for a cold email sequencer. |
| [crm-enricher](skills/list-building/crm-enricher/SKILL.md) | Fills missing emails, mobiles, job titles and company fields in a HubSpot, Pipedrive, GoHighLevel or Salesforce export using ScraperCity Lead Database lookups (by companyDomain, companyName or socialUrl), Email Finder, Mobile Finder and Website Finder. |
| [decision-maker-finder](skills/list-building/decision-maker-finder/SKILL.md) | Finds the people who own a buying decision at a given list of companies or domains, maps each to a buying role (economic buyer, owner, champion, technical evaluator), and returns verified work emails and, on request, mobile numbers. |
| [ecommerce-by-techstack](skills/list-building/ecommerce-by-techstack/SKILL.md) | Builds a list of online stores filtered by platform, category, installed Shopify apps, technologies, location, social presence and estimated traffic, sales or headcount bands with ScraperCity Store Leads ($0.0039 per lead, band filters applied server-side), intersects or excludes a second technology with Tech Stack Search ($4.99 per technology), keeps only stores with an email, validates them, tiers them by size and exports a CSV. |
| [email-list-cleaner](skills/list-building/email-list-cleaner/SKILL.md) | Cleans an old or inherited email list before anyone sends to it: repairs syntax, dedupes, applies suppression, flags role and free-provider addresses, validates every unique address with ScraperCity's Email Validator, and splits the result into send-ready, catch-all, hold and removed files with a reason on every dropped row. |
| [icp-list-builder](skills/list-building/icp-list-builder/SKILL.md) | Turns 3-5 example customers into Lead Database filters, shows the match count before pulling, pages the results with after cursors, normalizes, dedupes, suppresses and validates every email, and delivers a CSV of send-ready contacts with a funnel that accounts for every dropped row. |
| [local-business-list](skills/list-building/local-business-list/SKILL.md) | Builds a send-ready list of local businesses for a category and area. |
| [mobile-appender](skills/list-building/mobile-appender/SKILL.md) | Turns LinkedIn profile URLs or work emails into a dialer-ready calling list with ScraperCity Mobile Finder ($0.25 per number found, nothing when none is found). |
| [recruiting-sourcer](skills/list-building/recruiting-sourcer/SKILL.md) | Sources candidates by role, seniority, location and target companies from the ScraperCity Lead Database (title, notTitle, seniority, department, companyName, companyDomain and location filters) or from an Apollo people-search URL (scrape_apollo, 500 to 50,000 leads at $0.0039 each, delivered over hours to days through a webhook), removes people at the hiring company and do-not-poach accounts, ranks the shortlist, then adds verified emails (find_emails, validate_emails) and mobiles for the top tier (find_mobiles), with outreach rules for candidates. |
| [skip-tracer](skills/list-building/skip-tracer/SKILL.md) | Turns names, phone numbers, emails or property addresses into current phones, emails and addresses with ScraperCity People Finder ($0.0199 per result; a search with 0 matches is billed as 1 result) and Property Lookup ($0.15 per property, plus $0.10 for owner contact), with Distress List as a lead feed. |
| [tam-builder](skills/list-building/tam-builder/SKILL.md) | Builds a total addressable market file: defines the market, counts it in the Lead Database and Local Business Database, pulls every account with cursor paging, fills coverage gaps with Google Maps or Store Leads scrapes, dedupes by domain then normalized business name keeping the most complete record, and delivers one company-level CSV with a source column, a coverage estimate and TAM/SAM/SOM in accounts and dollars. |

### Outbound (11)

| Skill | What it does |
|-|-|
| [cold-calling](skills/outbound/cold-calling/SKILL.md) | Builds a B2B or local-business cold calling program: a call list from ScraperCity phone fields and find_mobiles, a per-number DNC and TCPA gate (B2B vs consumer lines, wireless numbers, AI-voice ban, state calling hours), call blocks with a dials-to-meetings funnel, an opener-reason-question-ask script, an objection bank, voicemail and gatekeeper scripts, and CRM logging. |
| [cold-email-copywriting](skills/outbound/cold-email-copywriting/SKILL.md) | Writes cold email sequences that get positive replies: bodies under 90 words, one ask per email ending in a question, plain text, subject lines, follow-up touches with new value, and personalization that changes relevance using real ScraperCity fields (Google rating, review count, category, city, store platform, installed apps, technology, title, company size, revenue) with merge-field fallbacks. |
| [cold-email-strategy](skills/outbound/cold-email-strategy/SKILL.md) | Plans a cold email campaign from list to booked meeting: campaign cells (one segment, one offer, one trigger), offer design, contact thesis, a touch map with branches, a volume and inbox capacity plan, a test plan, and a measurement funnel judged on positive replies and meetings. |
| [domain-infrastructure](skills/outbound/domain-infrastructure/SKILL.md) | Plans and specifies the sending infrastructure for cold email: how many secondary domains and mailboxes a volume target needs, what to name them, where to register them, how they redirect to the main site, the exact SPF, DKIM, DMARC (with rua), MX, tracking-domain and optional BIMI records, and whether to run Google Workspace, Microsoft 365 or another mailbox provider. |
| [email-deliverability](skills/outbound/email-deliverability/SKILL.md) | Keeps a running cold email program in the inbox: a pre-send gate (authentication, one-click unsubscribe, list validation with ScraperCity's Email Validator and a rule for every result, catch-all handling), weekly monitoring with seed tests, Google Postmaster Tools, Yahoo CFL, Microsoft SNDS and blocklist checks, an incident runbook for bounce spikes, spam folder placement, complaint spikes and blocklisted domains, and hard stop rules tied to the Google, Yahoo and Microsoft sender requirements. |
| [inbox-setup](skills/outbound/inbox-setup/SKILL.md) | Sets up each cold email mailbox after the domains exist: sender identity tied to a real person, address format, display name, signature with opt-out and postal address, profile photo, reply routing and forwarding, warmup settings and a day-by-day ramp, sending windows, daily caps, reply monitoring, inbox rotation and retirement. |
| [multi-channel-outreach](skills/outbound/multi-channel-outreach/SKILL.md) | Builds outbound sequences that combine cold email with phone calls (mobile numbers from ScraperCity's Mobile Finder), manual LinkedIn touches and direct mail to business or property addresses. |
| [outbound-unit-economics](skills/outbound/outbound-unit-economics/SKILL.md) | Builds the unit economics of an outbound program: cost per lead, verified email, mobile, conversation, meeting and deal, using ScraperCity catalog prices and plan credits (Starter $49 with $49 credits, Growth $149 with $159, Scale $649 with $800) plus the user's own inbox, domain, sequencer and people costs. |
| [reply-handling](skills/outbound/reply-handling/SKILL.md) | Classifies and answers cold email replies: interested, referral, objections (price, timing, competitor, no need, send info), not now, unsubscribe, out of office, bounce, wrong person and angry. |
| [sending-platforms](skills/outbound/sending-platforms/SKILL.md) | Chooses and configures the sequencer for cold email: Instantly, Smartlead, Lemlist, EmailBison, ManyReach, HubSpot sequences or Apollo sequences, with every feature and price taken from the vendor's own page and dated. |
| [signal-triggered-outbound](skills/outbound/signal-triggered-outbound/SKILL.md) | Builds outbound that fires on dated events ScraperCity data can show: a new Google Maps or Yelp listing with few reviews, rating or review-count changes across repeat pulls, a domain newly found on a technology via Tech Stack Search, a store's platform, apps or traffic band from Store Leads, a business listed on BizBuySell, a pre-foreclosure or auction from the Distress List, agents new to a Zillow market, and daily new records with excludeDelivered. |
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

Checkers use only the Python standard library. Each one fails the unfilled template and passes the worked example, and each adds checks specific to its skill: email bodies under 90 words, units times price equals cost, every phone row cleared against Do Not Call, every touch with a branch, and so on.

<!-- GENERATED:inventory:start -->
| Inventory | Count |
|-|-:|
| Skills | 31 |
| Categories | 3 |
| Skill-owned reference files | 117 |
| Shared reference files (repo root, copied into each skill that uses them) | 8 |
| Output templates | 31 |
| Worked examples | 31 |
| Deliverable checkers | 31 |
| Total packaged files | 392 |
| Lines of Markdown (shared references counted once) | 30,741 |
<!-- GENERATED:inventory:end -->

## How the content is kept honest

- **Prices and tools are generated.** `scripts/sync-catalog.mjs` reads the published npm package and writes `references/scrapercity-catalog.md`. CI fails when the committed catalog drifts from the package.
- **Named sources.** Regulations come from the regulator (FTC, FCC, CRTC, ICO), sender rules from the mailbox providers (Google, Yahoo, Microsoft), protocols from the RFCs, and vendor features from the vendor's own docs, each dated. Every reference file ends with its sources.
- **Benchmarks are hypotheses.** Hit rates, reply rates and connect rates are labelled as planning assumptions with a source and a date, and the skills tell the agent to measure its own rate with a small pilot before a large run.
- **Compliance is a gate.** Email steps carry CAN-SPAM (and CASL, PECR or GDPR where they apply). Phone steps carry TCPA and Do Not Call. People search, property and records tools are for prospecting and research only, never for employment, tenant, credit or insurance decisions under the FCRA. Nothing here is legal advice.
- **Integrity.** `skills.lock` holds a SHA-256 for every packaged file.

## Validate

```bash
python3 scripts/validate-skills.py                     # structure, sources, copy rules, every checker
node scripts/sync-catalog.mjs --check                  # catalog matches the npm package
python3 scripts/materialize-shared-references.py --check
python3 scripts/generate-readme.py --check
python3 scripts/generate-lock.py --check
```

Requires Python 3.9+ with PyYAML, and Node 18+ for the catalog sync.

## Related

- [scrapercity.com/skills](https://scrapercity.com/skills): short versions of 12 list-building skills. The list-building category here holds the full versions.
- [scrapercity/scrapercity-cli](https://github.com/scrapercity/scrapercity-cli): the MCP server and CLI the skills call.
- [ScraperCity API docs](https://scrapercity.com/api-docs).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/SKILL_AUTHORING.md](docs/SKILL_AUTHORING.md). Every pull request runs the validators above.

## License

[MIT](LICENSE)
