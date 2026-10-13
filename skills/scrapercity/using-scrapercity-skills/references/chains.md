# End-to-End Chains

Nine playbooks. Each lists the skills in order, the file each one hands to the next, and a worked ScraperCity cost. Prices come from `references/scrapercity-catalog.md`. Hit rates for Email Finder, Mobile Finder and Website Finder are not published, so every chain marks them as planning assumptions; replace them with a measured rate from a 20 to 50 row pilot before a large run.

## 1. Local businesses by email (Growth plan)

Example: 1,500 dentists in Austin and Houston with a website and an email.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `local-business-list` | `dentists_tx_sendready.csv` with rating, reviews, city, website, validated email |
| 2 | `cold-email-strategy` | Campaign cell and touch map (rating band decides the angle) |
| 3 | `cold-email-copywriting` | Four-touch sequence using `total_score`, `reviews_count`, `city` |
| 4 | `sending-platforms` | Import mapping and suppression list |
| 5 | `reply-handling` | Reply rules and SLAs |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `query_local_business_database` | 1,500 | included | $0.00 |
| `scrape_maps` (gap fill) | 300 | $0.0099 | $2.97 |
| `validate_emails` | 1,800 | $0.0072 | $12.96 |
| **Total** | | | **$15.93** |

## 2. B2B contacts by title and company size

Example: VP or Head of Sales at US software companies with 50 to 200 employees, 3,000 contacts with an email.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `icp-list-builder` | Filter spec and count, then `vp_sales_us_saas.csv` |
| 2 | `cold-email-list` | Send-ready file, at most 2 contacts per company |
| 3 | `cold-email-strategy` | Cells split by company size band |
| 4 | `cold-email-copywriting` | Sequence |
| 5 | `outbound-unit-economics` | Cost per meeting at the measured reply rate |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `query_lead_database` (`hasEmail: true`) | 3,000 | included | $0.00 |
| `validate_emails` | 3,000 | $0.0072 | $21.60 |
| **Total** | | | **$21.60** |

## 3. Named accounts

Example: 200 target domains; the database covers 140 of them; 500 contacts end up in the sequence.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `decision-maker-finder` | Buying roles per account with verified emails |
| 2 | `account-researcher` | One-page briefs for the top 20 accounts |
| 3 | `multi-channel-outreach` | Email plus LinkedIn plan per account tier |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `query_lead_database` by `companyDomain` | 140 domains | included | $0.00 |
| `scrape_website_finder` (60 uncovered domains, 1 contact found each, assumption) | 60 | $0.0499 | $2.99 |
| `find_emails` (100 contacts without email, 60% found, assumption) | 60 | $0.05 | $3.00 |
| `validate_emails` | 500 | $0.0072 | $3.60 |
| **Total** | | | **$9.59** |

## 4. Online stores by platform and app

Example: 2,000 US Shopify apparel stores with the Klaviyo app and an email.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `ecommerce-by-techstack` | Store list tiered by estimated monthly sales |
| 2 | `cold-email-copywriting` | Angle per tier, naming the platform and app |
| 3 | `signal-triggered-outbound` | Monthly re-pull to catch stores that add or drop the app |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `scrape_store_leads` | 2,000 | $0.0039 | $7.80 |
| `validate_emails` | 2,000 | $0.0072 | $14.40 |
| **Total** | | | **$22.20** |

## 5. Distressed property owners

Example: a wholesaler wants 500 pre-foreclosure properties in one metro and the owners' contact details.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `scrapercity-real-estate-data` | Distress list with addresses and distress type |
| 2 | `skip-tracer` | Owner phones and emails with a match score |
| 3 | `multi-channel-outreach` | Mail first, then calls that passed the DNC gate |
| 4 | `cold-calling` | Script and call blocks |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `scrape_distress_list` | 500 | $0.05 | $25.00 |
| `find_people` (one result per search, assumption) | 500 | $0.0199 | $9.95 |
| **Total** | | | **$34.95** |

Gate: People Finder output is for outreach only, never a tenant, credit or employment decision (FCRA). Every number is scrubbed against the National DNC Registry and state lists before a dial.

## 6. Recruiting

Example: 400 senior backend engineers in Austin, excluding the hiring company, with mobiles for the top 50.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `recruiting-sourcer` | Candidate shortlist with tiers |
| 2 | `mobile-appender` | Mobiles for A-tier only |
| 3 | `cold-email-copywriting` | Candidate outreach (role, team, why them) |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `query_lead_database` | 400 | included | $0.00 |
| `find_mobiles` (50 inputs, 40% found, assumption) | 20 | $0.25 | $5.00 |
| `validate_emails` | 400 | $0.0072 | $2.88 |
| **Total** | | | **$7.88** |

## 7. CRM hygiene

Example: a 5,000-contact HubSpot export, 1,200 rows missing an email.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `crm-enricher` | Filled fields with audit columns, never overwriting owner-entered data |
| 2 | `email-list-cleaner` | Send-ready, catch-all, hold and removed files |
| 3 | `scrapercity-integrations` | Write-back mapping for HubSpot |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `find_emails` (1,200 inputs, 55% found, assumption) | 660 | $0.05 | $33.00 |
| `validate_emails` | 5,000 | $0.0072 | $36.00 |
| **Total** | | | **$69.00** |

## 8. Owner call program

Example: 800 local business owners with a named contact; SDRs want mobiles.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `local-business-list` (`hasContact: true`) | Owners with name, business phone and email |
| 2 | `mobile-appender` | Mobiles in E.164 with DNC status |
| 3 | `cold-calling` | Call blocks, opener, objection bank |

| Tool | Units | Unit price | Cost |
|-|-:|-:|-:|
| `query_local_business_database` | 800 | included | $0.00 |
| `find_mobiles` (800 inputs, 40% found, assumption) | 320 | $0.25 | $80.00 |
| **Total** | | | **$80.00** |

Call the business line first when no mobile is found. It costs nothing extra and carries less TCPA risk than a wireless number.

## 9. Daily feed of new businesses

Example: 50 new roofing contractors a day across Texas, emailed within 48 hours.

| Order | Skill | Hands on |
|-:|-|-|
| 1 | `signal-triggered-outbound` | Signal definition and freshness rule |
| 2 | `scrapercity-cli` | Cron job with `db-local` and `excludeDelivered` |
| 3 | `cold-email-copywriting` | "New listing" angle |
| 4 | `sending-platforms` | Daily API push into the sequencer |

| Tool | Units per month (22 sending days) | Unit price | Cost per month |
|-|-:|-:|-:|
| `query_local_business_database` (`excludeDelivered: true`) | 1,100 | included | $0.00 |
| `validate_emails` | 1,100 | $0.0072 | $7.92 |
| **Total** | | | **$7.92** |

## Plan choice across chains

Starter ($49 a month, $49 of credits) has no database access, so chains 1, 2, 3, 6, 8 and 9 fall back to scrapers. Chain 1 on Starter: 1,800 Maps businesses x $0.0099 = $17.82, plus $12.96 validation, $30.78 in all. Growth ($149 a month) carries $159 of credits and includes the databases. When a user runs more than one of the database chains a month, Growth is usually cheaper per record; `outbound-unit-economics` has the break-even table.

## Sources

- https://scrapercity.com/pricing
- https://www.npmjs.com/package/scrapercity
- https://www.ftc.gov/legal-library/browse/statutes/fair-credit-reporting-act
- https://www.donotcall.gov
