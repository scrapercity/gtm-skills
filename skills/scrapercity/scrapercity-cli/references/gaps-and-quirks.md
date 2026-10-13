# Gaps and Quirks: scrapercity CLI 1.0.17

What the CLI does not have, and flag combinations that do something other than what they look like. Each item was checked against `bin/cli.mjs` and `lib/client.mjs` in 1.0.17, and each quirk was reproduced on 2026-10-13 by capturing the request the CLI sends with the network stubbed out. A later release may fix any of them; re-check with `npm view scrapercity version` and the changelog before relying on a workaround.

## Commands the CLI does not have

| Need | In 1.0.17 | Use instead |
|---|---|---|
| Property details, value and owner contact | No `property-lookup` command (`Unknown command`) | MCP `scrape_property_lookup`, or `POST /api/v1/scrape/property-lookup` with `{"addresses": [...], "includeOwnerContact": true}`. $0.15 per property, $0.25 with owner contact |
| Ecommerce Database | No command (the library has a function, the CLI does not expose it) | `GET /api/v1/database/ecommerce` with the same `excludeDelivered` and `after` pattern |
| Webhook setup | None | app.scrapercity.com/dashboard/webhooks |
| Apollo endpoint status | None | `GET /api/v1/apollo-status` |
| Machine-readable output | No `--json`; every command prints text | Parse the stable lines (`Run ID:`, `Status:`, `Balance:`, `Next page: --after`), or call REST and use `jq` |
| Full database rows | `db-leads` and `db-local` print 3 rows per page | REST loop in `references/scripting-patterns.md` |
| A poll timeout other than 1 hour | Fixed | The `wait_run` status loop in `references/scripting-patterns.md` |
| Buying credits | None | Dashboard |
| A YouTube email scraper | Not a command or a tool in 1.0.17, even though an older README lists one | No equivalent in the current catalog |

## Tool parameters the CLI cannot send

| Command | Parameters in the catalog that have no flag | Use instead |
|---|---|---|
| `maps` | More than one search term per run, `url` (Google Maps link), `customGeolocation` | MCP `scrape_maps` or REST |
| `store-leads` | `offset`, `state`, `twitter`, `pinterest`, `planExclude`, `resumeFromLead`, the visits, sales and employee bounds (`minEstimatedMonthlyVisits` and the rest) | MCP `scrape_store_leads` or REST. Without `offset`, repeat runs with the same filters return the same first page |
| `website-finder` | `autoValidateEmails`, `autoFindMobiles`; a reliable `jobTitle` (see quirks) | MCP `scrape_website_finder` or REST |
| `airbnb` | `maxPages`, `onlyProHosts`, `onlyUniqueEmails`, `bulk` mode | MCP `scrape_airbnb` or REST |
| `bizbuysell` | `datasetName`; a working `--limit` (see quirks) | MCP `scrape_bizbuysell` or REST |
| `db-leads` | `socialUrl` | REST or MCP `query_lead_database` |
| `email-find` | The catalog's `find_emails` schema lists only `contacts`. The CLI also sends `autoValidateEmails` and `autoFindMobiles` from `--validate` and `--mobiles`; the catalog does not document them for this tool | Every email found is already validated per the catalog. For mobiles, run `mobile-find` on the found emails so the $0.25 per number is explicit |

## Parser quirks, reproduced

In several commands the CLI collects positional arguments before it removes flags, so a flag's value can land in the positional list.

| You type | What is sent | Workaround |
|---|---|---|
| `website-finder acme.com --title CEO` | `domains: ["acme.com", "CEO"]`, `jobTitle: "CEO"` | No safe CLI form with a title; `jobTitle` is required by the catalog. Use MCP or REST |
| `website-finder --file d.txt --title CEO` | `domains: ["d.txt", "CEO", ...file lines]` | Same: MCP or REST |
| `scrapercity builtwith Shopify --name shopify-us` | `technology: "Shopify shopify-us"` | `scrapercity builtwith Shopify` with no other flags; the run is still billed $4.99 for the one technology |
| `bizbuysell URL --limit 50` | `startUrls: [URL, "50"]` | Omit `--limit` (default `maxItems` 100, ceiling $0.99), or MCP or REST |
| `mobile-find --file inputs.txt` | `inputs: ["inputs.txt", ...lines]` | The file name finds nothing, and Mobile Finder bills only numbers found. For a clean input list: `xargs npx -y scrapercity@1.0.17 mobile-find < inputs.txt` (xargs may split a very long list into several runs) |
| `criminal John Smith --state CA` | `name: "John Smith CA"` | Always `criminal --name "John Smith" --state CA` |
| `distress-list --max 50 "Tampa, FL"` | `search: "50"` | Market first: `distress-list "Tampa, FL" --max 50` |
| `apollo --count 2000 URL` | `url: "--count"`, which is not a search URL | URL first: `apollo URL --count 2000` |
| `yelp -q plumbers -l "Denver, CO"` | `locations: ["Denver", "CO"]` | `-l "Denver CO"`; use commas only between places |
| `airbnb --city "Lisbon, Portugal"` | `city: ["Lisbon", "Portugal"]`; the tool expects "City, Country" (Europe only) | MCP or REST. The built-in help example ("Miami, FL") is outside the Europe-only coverage in the catalog |
| `airbnb --city ... --limit 50` | `maxResults: 50`; the catalog schema documents `maxPages`, not `maxResults` | Do not rely on it as a cost cap; test small through MCP with `maxPages` |
| `maps --limit` (no value) | `maxCrawledPlacesPerSearch: 1` | Always give a value |
| `db-leads ... --limit=100` | The flag is ignored; server default page size applies | `--limit 100` |

Commands that are safe in any order: `maps`, `yelp` (apart from the comma split), `angi`, `zillow-agents`, `store-leads`, `people-find`, `email-find`, `email-validate`, `db-leads`, `db-local`, `wallet`, `runs`, `status`, `poll`, `download`, `cancel`, `logs`.

## Output quirks

| Output | Behavior | Handle it |
|---|---|---|
| `runs` | Run ids cut to 12 characters | Keep the full id from the start output |
| `runs` cost column | Computed as rows handled times the run's per-row price | Cross-check against the catalog for free-if-not-found tools |
| `db-leads` and `db-local` first line | A total of 0 prints as `?` | Treat `?` as 0 |
| `status` | `Download:` line only when the server returned an output URL | Download only when `Status: SUCCEEDED` |
| `poll` | Prints progress on one line with carriage returns | In logs, read the final `✓ Done: N leads` line |
| Errors | `✗ ` plus message; the HTTP code is printed only when the server sent no message | Branch on message text |
| `download` errors | `Download failed: HTTP N` without the server's message | Run `status` and `logs` to see why; results are kept 48 hours |

## Stale documentation to ignore

The README and SKILL.md inside the CLI repository include a price table and plan list that do not match the current catalog (for example older per-email and per-place prices), a YouTube email entry, and a `--print-skill` option that the 1.0.17 MCP binary does not handle. Use `references/scrapercity-catalog.md` for prices and this skill for commands.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://github.com/scrapercity/scrapercity-cli
- https://scrapercity.com/api-docs
- https://scrapercity.com/pricing
- https://www.gnu.org/software/findutils/manual/html_node/find_html/Invoking-xargs.html
