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
| `reviews_count` | `reviews_count` | Integer; blank if below the cell's `minReviews` | route to non-count line |
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
| `app` | installed apps | One app that matches the offer, instead of the full list | route to platform line |
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
| `reviews_count` below the cell's `minReviews`, or blank | C | Category and city line |

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
| Footer | Sender name, company, opt-out line; one-click unsubscribe header for bulk volume (Google, Yahoo) |

## 7. Render QA checklist

| Check | Pass when |
|-|-|
| Empty-field row | Renders with fallbacks and no raw `{{` |
| Long business name | Line still reads; subject under 50 characters |
| Rating format | "4.9 stars", not "4.90" or "4.9/5" |
| Count below the cell's `minReviews` | Count line not used |
| Names in caps ("JOHN") | Normalized to "John" |
| Business-word names ("Office", "Front Desk") | Replaced with fallback |
| Word count | Under 100 for every touch body |
| Last line | Ends with "?" |

## 8. AI-written lines at scale

Use an LLM (in Clay, n8n, a spreadsheet formula or a script) to write one line per row when the line depends on more than a merge tag: a creative idea, a computed gap, a first line from a company description. Nowoslawski's process, as broken down on alexberman.com in March 2026, writes the examples by hand first and fixes weak output by adding examples instead of rewriting the prompt. This section turns that into a gate.

### Rollout steps

| Step | What you do | Pass to move on |
|-|-|-|
| 1. Hand-write | Write the line yourself for about 10 real rows (Nowoslawski's count), covering each variant (strong rating, low rating, missing field, different category) | Each line passes the delete test (section 1) and uses only fields in that row |
| 2. Build the prompt | Paste those lines as examples, plus the constraints block below and the capability and off-limits lists | The prompt reproduces your hand-written lines on the same rows |
| 3. Dry run | Generate for a batch of new rows and hold the upload | Output saved next to its input row |
| 4. Human review | Read every dry-run line against the review table below | Every failure type fixed by adding an example or a constraint (Nowoslawski fixes weak output with examples), then rerun the batch |
| 5. Automate | Generate for the full cell; spot-check rows from the run | Any invented fact stops the run and returns to step 4 |

### Claims only from list fields

The model may restate, round or compare values that are in the row. It may never add a fact. If a line needs a fact that is not in the row (a funding round, a hire, a product launch), pull it into a column first with its source and date, or drop the line.

| Allowed | Not allowed |
|-|-|
| "4.8 stars on 212 reviews" when `total_score` is 4.8 and `reviews_count` is 212 | "your busiest season" with no seasonal field |
| "runs Klaviyo" when the app is in the `apps` column | "your Klaviyo flows are underperforming" |
| "around 120 people" from `employees_count` 118 | "after your Series B" with no funding column |
| A rank computed across the same pull ("33rd of 41 by review count") | A rank against data you did not pull |

### Prompt template

```text
SYSTEM (identical for every row, so cached-input pricing applies):
You write one line for a cold email from [sender company] to [segment].
We deliver only these things: [capability 1], [capability 2], [capability 3].
Never propose, mention or imply: [off-limits list].
Use only facts present in the ROW block. If the field you need is empty,
return the fallback line exactly: "[fallback line]".
Line rules: one sentence, under 25 words, no greeting, no question,
no exclamation mark, no adjectives about the reader ("amazing", "impressive").
Return only the line.

EXAMPLES (hand-written, about 10):
ROW: business_name=Lakeline Family Dental; category=dentist; city=Cedar Park;
rating=4.9; reviews_count=212
LINE: 4.9 stars across 212 reviews is rare for a Cedar Park practice.
ROW: business_name=Hill Country Plumbing; category=plumber; city=Austin;
rating=3.9; reviews_count=31
LINE: Hill Country Plumbing sits at 3.9 stars on 31 reviews.
[add more, at least one with an empty field]

USER (varies per row):
ROW: [field=value; field=value; ...]
```

Brackets are filled once per campaign. Keep temperature low, and log the model name and prompt version with every output column so you can trace a bad line.

### Review table for the dry run

| Check | Fail example | Fix |
|-|-|-|
| Every fact traces to a field in the row | Mentions "your new location" with no location field | Add constraint; add a counterexample |
| Idea is on the capability list | Proposes a mobile app for an email agency | Tighten the capability list wording |
| Nothing from the off-limits list | Quotes a price | Add the term to off-limits |
| Fallback used when the field is empty | Invents a rating | Add an empty-field example |
| Reads like a person wrote it | "I was impressed by your impressive growth" | Add a plain example; ban the adjective |
| Fits the template sentence | Long line pushes the body past 100 words | Lower the word cap in the prompt |

### Fields in prompts

Send the model only the fields the line needs; every extra field is one more fact it can misplace.

## 9. Signal gates for variants

A signal variant replaces touch 1 only for rows where a list field shows the signal. Every other row gets the default touch 1. The line states what the field shows and nothing more: a rating is a rating, not proof that tenants complain about cleaning. Use a field only when it measures the problem the offer fixes, on the contact's own row: a rating fits a reviews or patient-experience offer for the business that owns the listing, not a cleaning offer to an office building's manager, whose listing reviews are about parking, leasing and tenants. A field from a second pull needs a match step (the column that joins it to the contact) before it can gate anything.

| Signal | Field and source | Gate (from the cell's filters) | Line it allows | Line it does not allow |
|-|-|-|-|-|
| Low rating with enough reviews | `total_score`, `reviews_count` (Local Business Database, Google Maps) | Inside the cell's low rating band, with at least its `minReviews` | "{{business_name}} has 3.8 stars on 46 Google reviews." | "Your reviews say the lobby is dirty" (review text not checked) |
| Strong rating, few reviews | `total_score`, `reviews_count` | Inside the cell's high rating band and under its `maxReviews` | "4.8 stars on 31 reviews" | "Patients love you" |
| Installed app | `apps` (Store Leads) | Lists the named app | "runs Recharge and Klaviyo" | "just installed Recharge" (no install date) |
| Platform | platform (Store Leads) | Equals the platform | "sells on WooCommerce" | "is moving off WooCommerce" |
| Technology | Tech Stack Search result | Domain is in the result for that technology | "runs Magento 1" | "is struggling with Magento" |
| Title | `title` (Lead Database, Local Business Database contact title) | Contains the persona keywords | Persona variant, different stake | A claim about their plans |
| Company size | `employees_count` | Inside the band | "a team around 120 people" | "growing fast" |
| Dated event (funding, hire, new location, sale) | Not a ScraperCity row field; needs a column with source URL and date (`signal-triggered-outbound`) | Dated inside the window the strategy plan sets | "congrats on the Aurora location" | Any event with no source and date |

Rules:

- Write the gate in the deliverable as the field in backticks, the threshold, and what other rows get: "only rows where `apps` lists Klaviyo; rows without it get touch 1".
- Split gated rows into their own campaign or variant before upload (section 4), and render one gated and one ungated row.
- Eric Nowoslawski's reputation campaign is the model: it targeted businesses in a rating band and quoted each one's own negative reviews, which only works because the reviews were pulled per row (GTM Engineer podcast notes, July 2025).

## Sources

- https://alexberman.com/cold-email-templates
- https://help.instantly.ai/articles/6384663-how-to-use-spintax
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://alexberman.com/cold-email-automation-clay-creative-ideas-breakdown
- https://alexberman.com/creative-ideas-campaign-cold-email-infrastructure
- https://thetransactionpod.com/episodes/inverting-your-go-to-market-strategy-thinking-with-jordan-crawford-ep-55/transcript
- https://thegtmengineer.substack.com/p/the-winning-cold-outbound-formula
