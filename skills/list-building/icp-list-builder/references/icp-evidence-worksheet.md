# ICP Evidence Worksheet

How to turn customer evidence into Lead Database filters and exclusions: which accounts to study, what to record, the rule that turns a shared trait into a filter, the lift check that replaces that rule once the user has enough closed deals, and the situation-based segments the database cannot express on its own.

## 1. Pick the evidence accounts

| Group | How many | Pick by | Becomes |
|-|-|-|-|
| Best-fit customers | 3-5, up to 10 | Closed fastest, renewed or expanded, would take a reference call | Filters (`title`, `keywords`, employee band, geography) |
| Lost on fit, or churned soon after buying | 2-5 | Lost because the product did not fit, not because of price or timing | Exclusions (`notKeywords`, `notIndustry`, `notTitle`, a tighter employee band) |
| Biggest logo | 0 | Leave it out unless it also qualifies as best-fit | Nothing |

Ask the user for the reason each lost or churned account left. A trait seen on the accounts lost on fit and on no best-fit customer becomes an exclusion once the user approves it.

## 2. Worksheet

One row per evidence account. Fill the company columns from `query_lead_database` with `companyDomain` and `limit: 5` (included in the Growth plan); ask the user for the deal columns.

| Column | Example | Where it comes from |
|-|-|-|
| `domain` | ledgerline.example | User |
| `outcome` | won, lost, churned | User or CRM |
| `days_to_close` | 9 | CRM |
| `retained_12m` | yes | CRM |
| `employees` | 85 | `employees_count` on the returned row |
| `industry_label` | Computer Software | `company_industry` as the database spells it |
| `keywords` | saas, b2b, fintech | `keywords` |
| `hq_country`, `hq_state` | United States, TX | `company_country`, `company_state` |
| `signer_title` | VP Sales | User |
| `user_title` | Sales Manager | User |
| `trigger_at_purchase` | New CRO hired that quarter | User, sales notes |
| `deal_source` | Outbound, referral, inbound | CRM |

Copy the database's own spelling of the industry label into the worksheet. A label typed from memory is the most common cause of a zero count.

## 3. From traits to filters

| Trait | Becomes a filter when | Filter |
|-|-|-|
| Employee count | Every best-fit example falls inside one span | `minEmployees` and `maxEmployees`: the examples' min and max, widened to the nearest band edge (10, 50, 200, 500, 1,000, 5,000) |
| Industry label | Every best-fit example shares the exact label | `industry`; otherwise skip it and use `keywords` |
| Keywords | A tag appears on every best-fit example and describes the business model | `keywords`, 2-4 tags |
| Revenue | The seller prices by revenue tier | `revenueMin`, `revenueMax`; revenue is sparser than headcount, so count with and without |
| Person country | The seller can only sell or support in some countries | `country` |
| HQ country or state | Territories are assigned by HQ | `companyCountry`, `companyState` |
| Signer title | Always | A title family from `title-synonyms-and-exclusions.md` |
| Lost or churned trait | Accounts lost on fit have it, no best-fit example has it, and the user approves | `notKeywords`, `notIndustry`, `notTitle` or a band edge |

A trait on only some best-fit examples goes to the user to decide. One unusual customer never sets a filter.

### Losses that are not fit losses

Sort every lost deal by reason before it touches the exclusions. Only fit losses exclude.

| Loss reason | Becomes | Example |
|-|-|-|
| Product did not fit the business | Exclusion (no best-fit example has the trait; the user approves) | Staffing firms with recruiter desks, not a sales team |
| Lost to one named competitor | Its own segment with its own copy angle, never an exclusion | Repeated losses to the same competitor among companies on one platform: build that slice with Tech Stack Search and hand `cold-email-copywriting` a displacement angle |
| Price | Nothing; check the employee band against the spend ceiling in `tam-builder` | |
| Timing, no budget this year | Re-contact list dated to the timing the prospect gave | |
| Went dark | Nothing; not evidence | |

### The "why now" column

For each best-fit customer, ask the user one question and write the answer in `trigger_at_purchase`: what changed at the account just before it bought? More than one best-fit account with the same answer (a new sales leader, a second office, a platform switch) is a situation segment for section 6: build it as its own slice so the first line of the email can name the event.

## 4. The lift check (a CRM export of closed deals)

With a CRM export of closed deals (won plus lost), compare win rates instead of counting examples. For each trait:

```text
win_rate_with_trait = won deals with the trait / all closed deals with the trait
lift                = win_rate_with_trait / overall win rate
```

Lift above 1 means deals with the trait close more often than average; below 1, less often. The user sets three numbers and the report records them: the lift at or above which a trait becomes a filter, the lift at or below which it becomes an exclusion, and the fewest deals a trait needs before either decision.

| Lift | Deals with the trait | Decision |
|-|-|-|
| At or above the user's filter lift | At or above the user's minimum | Filter on it |
| At or below the user's exclusion lift | At or above the user's minimum | Exclude it |
| Between the two | Any | Leave it out of the filters |
| Any | Under the user's minimum | Too few deals to decide; leave it out |

Worked numbers (illustrative): 120 closed deals, 40 won, so the overall win rate is 33.3%. The user's settings in this example: filter at 1.3, exclude at 0.5, at least 10 deals per trait.

| Trait | Closed deals with it | Won | Win rate | Lift | Decision |
|-|-:|-:|-:|-:|-|
| Uses HubSpot | 30 | 18 | 60.0% | 1.80 | Filter, through Tech Stack Search domains (section 6) |
| 50-200 employees | 70 | 32 | 45.7% | 1.37 | Filter |
| Agency business model | 15 | 1 | 6.7% | 0.20 | Exclude with `notKeywords` |
| Texas HQ | 12 | 5 | 41.7% | 1.25 | Leave out |
| Series B funding | 6 | 4 | 66.7% | 2.00 | Too few deals |

The lift check picks filters for one list. Weighting traits into a score and splitting an account universe into tiers belongs to `tam-builder`, which reuses the same lift numbers.

## 5. Company size changes the list, not only the filter

| Size band | Slot 1 title | Contacts per domain | Notes for the pull |
|-|-|-|-|
| 1-10 employees | Owner, Founder | The owner | Add `minEmployees: 2` to drop one-person side projects; role inboxes are common, so expect more catch-all results |
| 11-50 | Founder, CEO, or the one department head | One or two | The department head is often the founder; check for one person filling two slots |
| 51-1,000 | VP of the department that owns the budget | Up to the user's cap | The standard case for the title families |
| 1,001+ | VP or SVP of the business unit, with a region in the title | Up to the user's cap per business unit | Add the region or unit to `title` ("VP Operations North America") or filter by `state` |

## 6. Situation segments the database cannot express alone

Some best-fit segments are defined by an event or a technology at the account: a new leader, a hiring push, a platform in use. The Lead Database has no filter for these; pair it with the tool that does.

| Situation | Lead Database alone? | Execute with |
|-|-|-|
| Runs a given technology (CRM, ecommerce platform, help desk) | No; `keywords` sometimes names a platform, weakly | Tech Stack Search (`scrape_builtwith`, $4.99 per technology), then the returned domains in `companyDomain` batches |
| Shopify or WooCommerce store with a given app or traffic band | No | `scrape_store_leads` with `apps`, `technologies`, `minEstimatedMonthlyVisits` ($0.0039 per lead) |
| New leader in the buyer's seat in the last 90 days | No | A Sales Navigator "Changed jobs" saved search, then `socialUrl` lookups (`sales-navigator-filter-map.md`), or `signal-triggered-outbound` |
| Hiring for the role the product serves | No | `signal-triggered-outbound` |
| HQ in one state, people anywhere | Yes | `companyState` |
| Local business with a low rating | No (people database) | `local-business-list` with `maxRating` |

## 7. The ICP statement

Write one sentence the user can approve before any pull:

```text
[Title family] at [keywords or industry] companies with [employee band] employees in [geography],
excluding [anti-ICP traits], [optional situation].
```

Example: "VP Sales and CRO at B2B SaaS companies with 50-200 employees in the United States, excluding agencies and staffing firms."

## 8. Keep the worksheet alive

- Each quarter, add the quarter's won and lost deals and rerun the lift table.
- After each campaign, read replies by title family as described in the list quality standard's QA section. Referral replies name the right title; add it to the family before the next pull.
- When a filter's lift falls under the user's filter lift on fresh deals, drop it from the next list.

## Sources

- April Dunford, A quickstart guide to positioning (best-fit customers as the starting point): https://www.aprildunford.com/post/a-quickstart-guide-to-positioning
- Gartner, B2B Buying Report (buying groups of five to 11 stakeholders across five functions, 2022 survey): https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- ScraperCity MCP tool schema for `query_lead_database` (`companyDomain`, `socialUrl`, `keywords`, `revenueMin`): https://www.npmjs.com/package/scrapercity
- ScraperCity catalog (Tech Stack Search and Store Leads prices): references/scrapercity-catalog.md
