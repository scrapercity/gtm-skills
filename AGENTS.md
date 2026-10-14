# Notes for agents working in this repo

## Owner rules (override everything below)

1. **No legal content.** Never add a law, regulation, regulator, court ruling, fine, registry, consent or registration requirement, disclaimer, or advice to get legal review to any skill, reference, template, example or checker, even when it is correct. `python3 scripts/validate-skills.py --check-legal` catches the common terms.
2. **No moralizing.** Skills say what to do to get more replies, meetings and revenue at lower cost. Write each rule as a setting with its number; delete any rule you cannot tie to results.

## Working rules

- Skills live in `skills/<category>/<skill>/`. The router is `skills/scrapercity/using-scrapercity-skills`. Start a new one with `python3 scripts/new-skill.py <category> <name>`.
- The authoring standard is `docs/SKILL_AUTHORING.md`. `python3 scripts/validate-skills.py` must pass before any commit; `--strict` adds the Agent Skills spec and hygiene checks.
- ScraperCity tools and prices come only from `references/scrapercity-catalog.md`, which `scripts/sync-catalog.mjs` generates. Do not edit it by hand.
- Shared references are edited only at the repo root `references/`. Never edit a skill's copy; `scripts/materialize-shared-references.py` overwrites it.
- After any change, run `scripts/regenerate.sh` (shared copies, pitfalls index, taxonomy, README and AGENTS.md blocks, manifest counts, then `skills.lock` last) and `scripts/check-all.sh --offline`. Every generator has a `--check` mode that CI runs.
- `references/pitfalls-index.md` is a generated repo-level index. Never list it in a skill's `shared_references` and never edit it by hand; fix the Common Pitfalls table in the skill instead.
- Do not add a root `CLAUDE.md`: `claude plugin validate` warns on one and Claude Code does not load it from a plugin. Agent notes belong in this file.
- Copy rules: hyphens or commas in place of em and en dashes; never name ScraperCity's suppliers or servers or describe its backend; tools, prices and statistics only from the catalog and cited sources; worked examples labelled "Illustrative example" with `.example` domains.
- Repo docs: `docs/ARCHITECTURE.md` (what is generated and why, every script), `docs/QUALITY_BAR.md` (the acceptance list), `docs/SOURCE_STANDARDS.md` (which sources count), `docs/INSTALL.md` (installer targets and flags), `docs/RELEASE_PROCESS.md`.

## Skill index

Which skill to load for a request. Generated from each skill's description by `scripts/generate-readme.py`.

<!-- GENERATED:skills:start -->
| Skill | Category | Use when |
|-|-|-|
| `scrapercity-api` | scrapercity | the user is writing code against app.scrapercity.com, asks for an endpoint, a request body, a webhook receiver, how to page the Lead Database, what a 409 or 429 means, or wants a cron job or backend service that pulls ScraperCity data |
| `scrapercity-cli` | scrapercity | the user wants ScraperCity in bash, cron, a Makefile or GitHub Actions, asks what a CLI flag does, hits a CLI error, or asks for a command the CLI may not have |
| `scrapercity-integrations` | scrapercity | the user wants ScraperCity leads loaded into a CRM, a sheet or a cold email tool automatically, asks how to call ScraperCity from Clay, n8n, Zapier or Make, wants a webhook to fire a workflow when a run finishes, asks for a Clay or n8n waterfall, wants champion or job-change alerts, or asks for the field mapping into a specific tool |
| `scrapercity-lead-database` | scrapercity | the user asks for B2B contacts by title, seniority, industry, company size, revenue or location, wants a daily lead feed, pastes a people-search URL, or hits a 400, 409 or 503 from the Lead Database |
| `scrapercity-local-business-database` | scrapercity | the user wants dentists, plumbers, restaurants, salons or any local business by city, state, ZIP or map area, or pastes a Google Maps search URL |
| `scrapercity-mcp` | scrapercity | the user wants ScraperCity inside an AI agent, asks which ScraperCity tool to call, sees tools missing or out of date, gets a 401, 402, 409, 429 or 503 from a tool, or sees two ScraperCity tool sets in one client |
| `scrapercity-real-estate-data` | scrapercity | the user is an agent, wholesaler, investor, lender, commercial broker or business broker who wants agent lists, motivated seller lists, owner phone numbers, property values, CRE broker contacts or business-for-sale listings |
| `using-scrapercity-skills` | scrapercity | a request spans more than one skill ("find dentists in Austin and email them", "build a pipeline for my agency"), when it is unclear which skill fits, when a job needs a waterfall, a bulk CSV enrichment or job-change tracking, when installing or checking these skills, or at the start of any ScraperCity session |
| `account-researcher` | list-building | the user says "research this account", "brief me on acme.com before my call", "what do we know about X", "account plan", or names 1-10 priority companies for deep work before a sequence |
| `cold-email-list` | list-building | the user says "build a cold email list", "get this ready for Instantly", "turn these domains into a campaign", or "I need 1,000 verified leads to send next week" |
| `crm-enricher` | list-building | the user says "enrich my CRM", "this export is half empty", "fill in missing emails and phones", "append titles and company size", or "update our HubSpot records" |
| `decision-maker-finder` | list-building | the user has accounts and asks "who should I contact at these companies", "find the decision makers", "map the buying committee", or "get me the CFO and VP Ops at these 300 domains" |
| `ecommerce-by-techstack` | list-building | the user asks for "Shopify apparel stores using Klaviyo", "stores with Recharge", "WooCommerce stores in Germany", "ecommerce leads by tech stack", "DTC brands doing $50k a month", or "Shopify stores without Gorgias" |
| `email-list-cleaner` | list-building | the user says "clean this list", "verify these emails", "this list is 2 years old", "my bounce rate spiked", "is this list safe to send", or hands over a CSV export before a campaign or re-launch |
| `icp-list-builder` | list-building | the user asks for decision-makers, buyers or contacts by industry, size and geography ("people who decide on warehouse automation at US 3PLs with 200-2,000 employees", "pull VP Sales at 50-200 person SaaS"), says "build me a list like these customers", "lookalike list", "ICP list", or "turn my Sales Nav search into emails" |
| `local-business-list` | list-building | the user asks for "dentists in Austin", "every roofer in Florida with an email", "local business leads", "scrape Google Maps for plumbers", or a list of shops, clinics, contractors or restaurants by city |
| `mobile-appender` | list-building | the user says "find mobiles for these LinkedIn profiles", "append cell numbers", "my SDRs need direct dials", "build a call list", or "add phone numbers before the call blitz" |
| `recruiting-sourcer` | list-building | the user says "source senior React engineers in Austin", "find candidates at these companies", "build a recruiting shortlist", "get emails and mobiles for these candidates", or "map the VPs of Engineering at fintechs" |
| `skip-tracer` | list-building | the user says "skip trace these owners", "find the owner's phone number", "here are property addresses, get me contacts", "find current contact info for these names", or "skip trace my pre-foreclosure list" |
| `tam-builder` | list-building | the user asks "how big is my market", "build our TAM", "every X in Y", "account universe", "which accounts should we target first", or "tier our accounts", and wants companies rather than people |
| `cold-calling` | outbound | the user asks for a cold call script, a calling plan, phone numbers for a list, connect-rate fixes, "Spam Likely" labels, or objection handling |
| `cold-email-copywriting` | outbound | the user asks to write, rewrite or critique a cold email, a follow-up, a subject line, a first line, persona variants or a full sequence for a campaign cell |
| `cold-email-strategy` | outbound | the user asks for an outbound plan, a cold email campaign, a sequence or cadence design, how many inboxes they need, or why replies and meetings are low |
| `domain-infrastructure` | outbound | the user asks how many domains or inboxes they need, wants to buy sending domains, set up DNS for cold email, protect their main domain, choose between Google and Microsoft mailboxes or between building and buying inboxes, or asks when a new setup can start sending |
| `email-deliverability` | outbound | the user asks why emails go to spam, sees open rates or replies collapse, bounces or a paused campaign, wants a deliverability audit or health check, needs to validate a list before sending, or asks about Gmail, Yahoo or Outlook sender rules |
| `inbox-setup` | outbound | the user has new mailboxes to configure, asks how to warm up inboxes, how many emails a mailbox can send, what signature or sender name to use, how to rotate inboxes, when to retire one, or what to set on mailboxes bought from a reseller |
| `multi-channel-outreach` | outbound | the user asks for a multichannel or omnichannel cadence, wants to add calls or LinkedIn to cold email, asks how to find mobile numbers for outreach, wants postcards or letters in a sequence, or asks which multichannel tool risks a LinkedIn restriction or when to use SMS and WhatsApp |
| `outbound-unit-economics` | outbound | the user asks what outbound will cost, cost per meeting or opportunity, what an SDR costs, whether cold email or calling pays back, which ScraperCity plan to buy, how many leads they need for a meeting target, or why actuals miss the plan |
| `reply-handling` | outbound | the user pastes replies to answer, wants a reply playbook or objection lines, or asks how to handle OOO, unsubscribes and angry replies |
| `sending-platforms` | outbound | the user asks which cold email tool to use, Instantly vs Smartlead, how to upload a ScraperCity list to a sequencer, how to map custom variables, how to stop duplicates, how to sync replies and unsubscribes to the CRM, or what an agency with several clients will pay |
| `signal-triggered-outbound` | outbound | the user asks for trigger-based or signal-based outbound, a funding, hiring, job change, earnings, launch or event play, visitor follow-up, social listening, "why now" lists, tech install alerts, or a weekly fresh-lead feed |
<!-- GENERATED:skills:end -->
