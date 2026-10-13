# Routing Matrix

Intent to skill. Match the request against the trigger phrases, then read the first tool and the cost driver to price the step. Prices come from `references/scrapercity-catalog.md`; "included" means included with the Growth plan ($149) and up.

## List building

| Intent | Trigger phrases | Skill | First tool | Cost driver |
|-|-|-|-|-|
| Contacts like my best customers | "lookalike", "people like these customers", "build me an ICP list" | `icp-list-builder` | `query_lead_database` with `limit: 1` for the count | Included; $0.0072 per email validated |
| Every company in a market | "TAM", "how many", "every X in Y", "market map" | `tam-builder` | Database counts (lead and local) | Included; Maps or Store Leads for gaps |
| Buyers at named accounts | "who do I talk to at", "decision makers at these domains" | `decision-maker-finder` | `query_lead_database` by `companyDomain` + `seniority` | Included; Website Finder $0.0499 per contact found; Email Finder $0.05 per email found |
| Brief on one account | "research this company", "prep me for a call with" | `account-researcher` | `query_lead_database` by `companyDomain` | Included; Tech Stack Search $4.99 only when the stack changes the pitch |
| Local businesses in an area | "plumbers in Denver", "dentists near", "restaurants in" | `local-business-list` | `query_local_business_database` with `keyword` and `location` | Included; Maps $0.0099 and Yelp $0.0099 for gaps |
| Send-ready cold email list | "list for Instantly", "ready to upload", "emails for my campaign" | `cold-email-list` | Lead Database, then Email Finder for gaps | $0.05 per email found; $0.0072 per validation |
| Clean an existing list | "clean this list", "verify these emails", "bounces are high" | `email-list-cleaner` | `validate_emails` | $0.0072 per unique email |
| Fill gaps in a CRM export | "enrich my CRM", "missing emails", "append titles" | `crm-enricher` | Lead Database lookup by `companyDomain` | Included; Email Finder and Mobile Finder pay on find |
| Mobile numbers for a call list | "mobiles", "cell numbers", "phone numbers for these LinkedIn URLs" | `mobile-appender` | `find_mobiles` | $0.25 per number found |
| Online stores by platform or app | "Shopify stores using", "WooCommerce stores in", "stores doing $X a month" | `ecommerce-by-techstack` | `scrape_store_leads` | $0.0039 per lead; Tech Stack Search $4.99 per technology |
| Current contact for a person or address | "skip trace", "find the owner's phone", "locate" | `skip-tracer` | `find_people` or `scrape_property_lookup` | $0.0199 per result; $0.15 per property (+$0.10 owner contact) |
| Candidates for a role | "source engineers", "recruit", "candidates at" | `recruiting-sourcer` | `query_lead_database` by `title` and `seniority` | Included; Apollo URL $0.0039 per lead |

## Outbound

| Intent | Trigger phrases | Skill | First action | Cost driver |
|-|-|-|-|-|
| Plan a campaign | "outbound plan", "sequence strategy", "why are replies low" | `cold-email-strategy` | Campaign cell: one segment, one offer, one trigger | Inbox capacity |
| Write the emails | "write a cold email", "follow-ups", "subject lines" | `cold-email-copywriting` | Pick the personalization field from the list | None |
| Answer replies | "how do I reply to", "objection", "they said not now" | `reply-handling` | Classify the reply | Email Finder for referrals |
| Mix channels | "email and call", "LinkedIn plus email", "direct mail" | `multi-channel-outreach` | Channel roles and timing | Mobile Finder, postage |
| Domains and DNS | "new domains", "SPF", "DMARC", "how many domains" | `domain-infrastructure` | Volume target to mailbox count | Domains and mailboxes |
| Mailbox setup | "set up inboxes", "warmup", "signatures" | `inbox-setup` | Sender identity per mailbox | Mailbox seats |
| Inbox placement | "spam folder", "blocklisted", "bounce rate", "Postmaster" | `email-deliverability` | Pre-send gate and health check | $0.0072 per validation |
| Choose a sequencer | "Instantly or Smartlead", "import into Lemlist" | `sending-platforms` | Requirements table | Sequencer seats |
| Cold calling | "call script", "SDR call blocks", "cold call local businesses" | `cold-calling` | DNC and TCPA gate | Mobile Finder $0.25 per number found |
| Event-based outreach | "new businesses", "just switched to Shopify", "pre-foreclosure list weekly" | `signal-triggered-outbound` | Define the signal and its repeat pull | Repeat-pull volume |
| Cost and ROI | "cost per meeting", "is outbound worth it", "which plan" | `outbound-unit-economics` | Inputs table | Model only |

## ScraperCity product and access

| Intent | Trigger phrases | Skill |
|-|-|-|
| Install the MCP server | "add ScraperCity to Claude", "MCP not showing", "Cursor setup" | `scrapercity-mcp` |
| Terminal or cron | "CLI", "bash script", "daily cron pull" | `scrapercity-cli` |
| Code against the API | "REST", "webhook", "Python script", "Node" | `scrapercity-api` |
| No-code tools | "Clay", "n8n", "Zapier", "push to HubSpot", "send to Smartlead" | `scrapercity-integrations` |
| Deep Lead Database work | "filter by revenue", "people-search URL", "daily new leads" | `scrapercity-lead-database` |
| Deep Local Business Database work | "map box", "rating filter", "businesses with a named contact" | `scrapercity-local-business-database` |
| Real estate data | "Zillow agents", "pre-foreclosure", "property owner", "Crexi", "BizBuySell" | `scrapercity-real-estate-data` |

## Tie-breakers

| Ambiguity | Decide by | Route |
|-|-|-|
| "Leads" with no type | Does the user sell to companies with staff, or to storefronts? | Companies: `icp-list-builder`. Storefronts: `local-business-list`. |
| "Phone numbers" | Business line or a person's mobile? | Business line: database or Maps phone field. Mobile: `mobile-appender`. |
| "Find the owner" | Of a business or of a property? | Business: `decision-maker-finder` (or `hasContact` in the Local Business Database). Property: `skip-tracer`. |
| "Apollo" | Does the user have an Apollo people-search URL? | Yes: `scrape_apollo` through `scrapercity-lead-database` (compare with the database first). No: Lead Database filters. |
| "Verify" | Emails, or a person's identity? | Emails: `email-list-cleaner`. Identity: `skip-tracer`, with the FCRA boundary stated. |
| Starter plan and a database intent | Growth costs $100 a month more and carries $110 more in credits. Does the database save more than that on this job? | Price both; let the user choose. |
| Background check request for hiring or renting | Purpose is an eligibility decision | Decline that purpose. Public-records tools here are for prospecting and research only. |

## Phrases that need a question first

Ask one question before routing when the request is:

- "Get me leads" with no buyer named. Ask who they sell to.
- "As many as possible" with no budget. Ask for a ceiling, then quote the count.
- A country outside the US with phone or SMS in the plan. Ask which countries, because the gate changes.
- A list for "texting". Ask whether consent exists; without it, route to email or calling with the TCPA gate.

## Sources

- https://www.npmjs.com/package/scrapercity
- https://scrapercity.com/pricing
- https://scrapercity.com/skills
- https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act
- https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-64/subpart-L/section-64.1200
