# Personalization and Merge Fields

How to turn ScraperCity output columns into merge tags that render correctly for every row, including rows with empty fields. Also covers spintax and plain text formatting.

## 1. Personalization levels

Alex Berman's templates page describes three levels; this table maps each to ScraperCity fields.

| Level | What it uses | ScraperCity fields | Cost to produce | Use for |
|-|-|-|-|-|
| Segment | Shared role, industry or size | `category_name`, `company_industry`, `employees_count`, platform | Free with the pull | Every email |
| Account | Facts about this business | `total_score`, `reviews_count`, `apps`, `technologies`, `city`, `website` | Free with the pull | First line in most cells |
| Person | Something this person said or did | Not in ScraperCity data; manual research | 3 to 10 minutes per contact | High value accounts only |

The relevance test: the personalized fact must make the offer more believable or more urgent for this reader. A fact that could be deleted without changing the email is decoration.

## 2. Field map and fallbacks

Normalize columns into these tags before upload. Each fallback must read naturally in the sentence it sits in. If no fallback reads naturally, write a second version of the line and route empty rows to it with a condition (section 4).

### Local Business Database and Google Maps

| Tag | Source column | Clean-up | Fallback |
|-|-|-|-|
| `first_name` | `contact_first_name` | Title case; drop if it is a business word ("Office", "Info") | `there` |
| `business_name` | `title` | Strip "LLC", "Inc", "PLLC", "DDS" and trailing location suffixes | `your practice` / `your shop` |
| `category` | `category_name` | Lowercase, singular ("dentist") | `business` |
| `city` | `city` | Title case | `your area` |
| `rating` | `total_score` | One decimal | route to non-rating line |
| `reviews_count` | `reviews_count` | Integer; blank if under 10 | route to non-count line |
| `website` | `website` | Bare domain, no https:// | omit the line |
| `job_title` | `contact_job_title` | Title case | omit |

### Lead Database and Apollo Scraper

| Tag | Source column | Clean-up | Fallback |
|-|-|-|-|
| `first_name` | first name | Title case | `there` |
| `company_name` | company name | Strip legal suffixes | `your team` |
| `title` | `title` | Shorten ("Vice President of Sales" to "VP Sales") | `your role` |
| `employees_count` | `employees_count` | Round to a band word: "40", "about 120", "200+" | route to non-size line |
| `industry` | `company_industry` | Lowercase, plain words ("software" not "computer software") | `your industry` |
| `revenue_band` | `company_annual_revenue` | Band only: "$10M to $50M" | omit the line |
| `company_city` | `company_city` | Title case | omit |
| `keyword` | `keywords` | First relevant tag only | omit |

### Store Leads

| Tag | Source column | Clean-up | Fallback |
|-|-|-|-|
| `store_name` | store name | Strip ".com" and "Store" duplicates | `your store` |
| `platform` | platform | Proper case ("Shopify", "WooCommerce") | `your platform` |
| `app` | installed apps | One app that matches the offer, not the list | route to platform line |
| `technology` | technologies | One relevant technology | omit |
| `category` | category | Lowercase plural ("apparel stores") | `stores` |

### Tech Stack Search

`scrape_builtwith` returns domains using one technology. Set `technology` as a static value for every row in the cell and find people with `scrape_website_finder` (`domains`, `jobTitle`, `autoValidateEmails: true`).

## 3. Platform merge syntax

| Platform | Variable | Fallback | Notes |
|-|-|-|-|
| Instantly | `{{firstName}}` | `{{firstName | there}}`; chained `{{firstName | lastName | there}}` | Case-sensitive, must match CSV headers |
| Smartlead | `{{first_name}}` | Set a default per variable in the campaign | Check the docs for the current syntax |
| Lemlist | `{{firstName}}` | Fallback set in the variable settings | Same |
| EmailBison, ManyReach | Platform variables | Platform fallback or pre-filled CSV column | Same |

Safest pattern for any platform: fill fallbacks in the CSV before upload, so no row has an empty cell. Example: if `contact_first_name` is empty, write "there" into the `first_name` column.

## 4. Routing empty fields with conditions

Instantly supports Liquid-style conditions (`{% if variable == "value" %} ... {% endif %}`), and its help center notes matching is case-sensitive. A simpler and more portable method: split rows by field presence into separate campaigns or variants.

| Rows where | Variant | First line |
|-|-|-|
| `rating` 4.6+ and `reviews_count` 10+ | A | Praise plus count |
| `rating` 4.0 or lower and `reviews_count` 10+ | B | Rating question |
| `reviews_count` under 10 or blank | C | Category and city line |

## 5. Spintax caution

| Rule | Reason |
|-|-|
| Spin only greetings, sign-offs and connector words | Proof and asks must be identical so the test measures one thing |
| Every option is a full, true sentence | Random combinations otherwise produce broken grammar |
| Two or three options per spin, no nesting | Nesting multiplies variants you cannot review |
| Preview 10 rendered emails before launch | Instantly's help center recommends previewing spintax renders |
| Never use spintax to hide the same email sent at high volume from one inbox | It does not fix list quality, volume or complaints; mailbox providers read reputation and complaints |

Instantly syntax: `{{RANDOM | Hi | Hello}} {{firstName | there}},`. Its help center notes that omitting `RANDOM` can skip the first option.

## 6. Plain text formatting

| Element | Rule |
|-|-|
| Format | Plain text, or HTML that renders as plain text, without images, colors or bold |
| Links | None in touch 1; one maximum after, written as a bare domain |
| Tracking | Open tracking off (Apple MPP inflates opens and the pixel adds a tracking domain); click tracking off unless a custom tracking domain is set |
| Line breaks | One idea per line, blank line between |
| Signature | Name, company, one line; no images |
| Attachments | Never on a cold first touch |
| Footer | Sender name, company, postal address, opt-out line (CAN-SPAM); one-click unsubscribe header for bulk marketing volume (Google, Yahoo) |

## 7. Render QA checklist

| Check | Pass when |
|-|-|
| Empty-field row | Renders with fallbacks and no raw `{{` |
| Long business name | Line still reads; subject under 50 characters |
| Rating format | "4.9 stars", not "4.90" or "4.9/5" |
| Count under 10 | Count line not used |
| Names in caps ("JOHN") | Normalized to "John" |
| Business-word names ("Office", "Front Desk") | Replaced with fallback |
| Word count | Under 90 for every touch body |
| Last line | Ends with "?" |

## Sources

- https://alexberman.com/cold-email-templates
- https://help.instantly.ai/articles/6384663-how-to-use-spintax
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
