# Cold Email Frameworks

Original summaries of the cold email frameworks this repo relies on. Each one lists where it comes from, when to use it, when to skip it, and a short example built on real ScraperCity fields. Every example body stays under 90 words, the cap `cold-email-copywriting` enforces. Benchmarks are starting hypotheses with a source and a date.

Field names used in the examples come from ScraperCity outputs: Local Business Database rows carry `title`, `category_name`, `city`, `total_score` (Google rating), `reviews_count`, `website` and `contact_first_name`; Lead Database rows carry `title`, `company_size`, `employees_count`, `company_annual_revenue`, `company_industry` and `company_city`; Store Leads filters cover platform, apps and technologies. Output fields are documented in the package's AGENT_DOCS.txt (https://github.com/scrapercity/scrapercity-cli/blob/main/AGENT_DOCS.txt); tool inputs are in `references/scrapercity-catalog.md`.

## Constraints every framework sits inside

| Constraint | Rule | Source |
|-|-|-|
| Truthful headers and subject | From, Reply-To and subject must not mislead | FTC CAN-SPAM guide |
| Postal address and opt-out | Every commercial email carries a valid postal address and a working opt-out, honored within 10 business days; no B2B exemption | FTC CAN-SPAM guide |
| Authentication | SPF, DKIM and a DMARC record (p=none or stricter) with From alignment for bulk senders | Google sender guidelines, Yahoo sender best practices, Microsoft Outlook (enforced May 5, 2025) |
| Complaint rate | Gmail: stay under 0.1%, never reach 0.3%. Yahoo: under 0.3% | Google, Yahoo |
| Canada | CASL needs consent; implied consent from a published business address only when the message is relevant to the role; unsubscribe within 10 business days | CRTC CASL FAQ |
| UK corporate subscribers | Companies can be emailed without prior consent under PECR; sole traders and some partnerships need consent | ICO PECR guidance |

These limits shape copy: no deceptive "Re:" subject lines, no hidden sender, an opt-out line in every touch, and personalization that does not read as surveillance.

## Framework index

| # | Framework | Primary authority | Best for | Skip when |
|-|-|-|-|-|
| 1 | Targeting-first (30/30/50) | Alex Berman | Deciding what to fix first | Never skip; it frames the others |
| 2 | 3C: Compliment, Case Study, Call to Action | Alex Berman | Agencies and services with a client result | You have no comparable result yet |
| 3 | Offer-led email | Alex Berman | Any campaign with a measurable outcome to sell | The offer is still a service description |
| 4 | Problem-first question | Josh Braun (as summarized by 11x), Berman's "Direct Question" template | Buyers who do not yet know they have the problem | The data cannot support a problem guess |
| 5 | PAS adapted for cold email | Direct response copywriting tradition (Copyblogger) | Problems with a visible, costly symptom | The symptom would insult the reader |
| 6 | AIDA compressed | E. St. Elmo Lewis model (EBSCO) | Longer consideration buys, follow-up arcs | First touch to a busy executive |
| 7 | Three-sentence short email | Berman length rules, Hunter word-count data | High volume, mobile reading | Complex offers that need one proof line more |
| 8 | Trigger-based relevance | Craig Elias, Trigger Event Selling | Funding, hiring, new location, new tech | The trigger is stale or invented |
| 9 | Cycle mailing vs sequence | Alex Berman | Very large or very small markets | Mid-size markets with a fixed quarter |

## 1. Targeting-first (30/30/50)

**What it says.** Berman's site splits cold email results into 30% targeting, 30% offer and 50% deliverability. Copy is not one of the three. A roundup on his site argues that choosing a better buyer (a manufacturer with 15+ employees instead of a startup) changed deal size more than any rewrite.

**When to use.** At the start of every campaign, and whenever replies drop. Fix in this order: is mail landing, is the list the right buyer, is the offer specific. Only then rewrite copy.

**ScraperCity example.** A web agency's replies are 0.4%. Before touching copy, re-pull the list with `query_local_business_database` using `category: ["Dentist"]`, `city: "Austin"`, `state: "TX"`, `minReviews: 40`, `hasWebsite: true`, `hasContact: true`. Practices with 40+ reviews and a website are established enough to pay for a redesign. Then run `validate_emails` on every address before the next send.

**Sources.** https://alexberman.com, https://alexberman.com/cold-email-buyer-selection-beats-copywriting

## 2. 3C: Compliment, Case Study, Call to Action

**What it says.** Berman's 3C framework: open with a sincere, specific compliment, follow with a relevant case study and its result, close with a simple ask. The Lean B2B interview gives the same three lines in that order.

**When to use.** Service businesses with one result from a similar client. The compliment must come from data you can see (rating, review count, store category), not flattery.

**When to skip.** No comparable client result yet. Use the problem-first question instead.

**ScraperCity example** (fields: `contact_first_name`, `title`, `total_score`, `reviews_count`, `city`):

> Subject: Question about Lakeline Family Dental
>
> Hi Maria, 4.9 stars across 212 reviews is rare for a Cedar Park practice.
>
> We rebuilt the site for a 3-chair practice in Round Rock with similar reviews. New patient form fills went from 9 to 26 a month in 60 days.
>
> Worth a 10 minute look at what we changed?

(51 words in the body. The case study must be real; never invent one.)

**Sources.** https://alexberman.com, https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/, https://devrims.com/blog/alex-berman-techtalk-interview-005/

## 3. Offer-led email

**What it says.** Berman's article "Cold Email Doesn't Fail, Your Offer Does" says the offer is what earns a reply. Build it from a measured client outcome, as one sentence: niche, result, mechanism. Build the list after the offer. Adding one line of documented proof to an existing campaign is reported on that page to lift replies sharply (self-reported).

**When to use.** Always, as the core of the email. The other frameworks are wrappers around an offer.

**Offer test.** Fill this sentence with real numbers: "We help [niche] get [result with number] in [time] by [mechanism]." If any bracket stays vague, the offer is not ready.

**ScraperCity example** (Store Leads fields: platform, apps, estimated monthly visits):

> Subject: Klaviyo flows at Northpaw
>
> Hi Dana, saw Northpaw runs Shopify with Klaviyo installed.
>
> We build post-purchase flows for pet stores in the 20k to 60k monthly visit range. Our last one, a treats brand, added $11,400 in repeat revenue in its first 45 days.
>
> Want the flow map we used?

(46 words in the body.)

**Sources.** https://alexberman.com/cold-email-doesn-t-fail-your-offer-does

## 4. Problem-first question

**What it says.** Lead with a neutral question about a problem the reader may have, with no pitch. The 11x summary of Josh Braun's method describes curiosity questions that let the prospect reflect instead of defend, low-pressure closes such as asking whether something is worth exploring, and emails under 80 words. Berman's templates page includes a "Direct Question" template that asks whether the prospect currently does a specific thing.

**When to use.** The buyer may not know the problem exists, and your data hints at it (a low rating, a missing app, a small review count against local competitors).

**When to skip.** You cannot point at evidence. A guessed problem reads as presumptuous.

**ScraperCity example** (fields: `total_score`, `reviews_count`, `category_name`, `city`):

> Subject: reviews at Hill Country Plumbing
>
> Hi Tom, Hill Country Plumbing sits at 3.9 stars on 31 reviews. The three plumbers ranked above you in Austin each have 150+.
>
> Do you ask customers for a review after each job today, or is it left to chance?

(40 words in the body.)

**Sources.** https://www.11x.ai/guides/josh-braun-cold-outreach-method, https://alexberman.com/cold-email-templates

## 5. PAS adapted for cold email

**What it says.** Problem, Agitate, Solve: name a problem, make its cost concrete, then offer the fix. Copyblogger's Demian Farnworth describes it as a direct response formula (2014). Berman's templates page includes a "Problem-Agitate" template that asks about the problem, describes its consequence, cites a similar result and offers to show how.

**Cold email adaptation.** Keep "agitate" to one factual line with a number. Drama gets marked as spam by people. Replace "solve" with a proof line and a question.

**When to use.** The problem has a visible symptom in the data and a cost you can state.

**ScraperCity example** (Lead Database fields: `title`, `employees_count`, `company_industry`):

> Subject: SDR ramp at Corvane
>
> Hi Priya, Corvane is hiring 4 SDRs this quarter at 120 employees.
>
> New reps usually spend their first month building lists by hand, which is about $6,000 of salary per rep before a single meeting.
>
> We hand each new SDR a validated, segmented list on day one. One fintech client cut ramp from 7 weeks to 3.
>
> Open to seeing a sample list for your ICP?

(66 words in the body.)

**Sources.** https://copyblogger.com/problem-agitate-solve/, https://alexberman.com/cold-email-templates

## 6. AIDA compressed

**What it says.** Attention, Interest, Desire, Action. EBSCO credits E. St. Elmo Lewis with the earliest version around 1898. In a 60 word email each stage is one clause: the subject and first line earn attention, one fact earns interest, one result builds desire, one question asks for action.

**When to use.** Better as a sequence arc than a single email: touch 1 attention plus interest, touch 2 desire (case study), touch 3 action (direct ask), touch 4 breakup.

**ScraperCity example** (Maps and Local Business Database fields, gym owner):

> Subject: Iron Yard's 4.8
>
> Hi Luis, Iron Yard has a 4.8 on 380 reviews, the highest of any gym in Tempe we looked at.
>
> We run trial-pass ads for gyms with ratings like yours. A Mesa gym booked 64 trials in March from $1,900 of spend.
>
> Should I send the ad set?

(48 words in the body.)

**Sources.** https://ebsco.com/research-starters/marketing/aida-model

## 7. Three-sentence short email

**What it says.** One line on them, one line of proof, one question. Berman's pages recommend under 75 words, about four lines under 70 words, and an opener of one or two sentences. Hunter's analysis of 34 million cold emails sent through Hunter Sequences (2022 to 2024, published April 2024) found 20 to 39 word emails had the highest average reply rate at 4.5%, while noting the differences between length bands were small.

**When to use.** Default for first touches and for follow-ups. Most of the campaigns in this repo should start here.

**ScraperCity example** (Tech Stack Search output: a domain list for one technology):

> Subject: Question about Fernway
>
> Hi Chris, Fernway's site still runs on Magento 1.
>
> We moved two outdoor gear stores to Shopify in under 6 weeks without losing search rankings.
>
> Worth a quick call to see if that timeline fits you?

(36 words in the body.)

**Sources.** https://alexberman.com/cold-email-templates, https://alexberman.com/cold-email-buyer-selection-beats-copywriting, https://hunter.io/blog/cold-email-word-count

## 8. Trigger-based relevance

**What it says.** Craig Elias, creator of Trigger Event Selling, describes a "window of dissatisfaction" when a buyer is unhappy but has not started looking, and argues that being the first vendor to reach them in that window wins most often (his article cites a 74% close rate attributed to Forrester). Triggers include a new decision maker, a large new contract and a competitor's launch. A roundup on Berman's site reports trigger-based lists replying far above bought lists (self-reported figures).

**When to use.** Whenever a dated event explains "why now". Put the trigger in the first line and make sure the offer connects to it.

**Trigger sources in ScraperCity.**

| Trigger | Tool | Field or filter |
|-|-|-|
| New store on a platform, new app installed | `scrape_store_leads` | `platform`, `apps`, `technologies` |
| Running a specific technology | `scrape_builtwith` | `technology` (domain list) |
| New or newly listed local business, few reviews | `query_local_business_database` | `maxReviews`, `category` |
| Distressed property owner | `scrape_distress_list` | `distressTypes` |
| Business listed for sale | `scrape_bizbuysell` | listing URL |

**When to skip.** The trigger is older than its half-life (a funding round from last year) or you cannot verify it. Never invent a trigger.

**ScraperCity example** (`scrape_store_leads` with `apps: "Recharge"`):

> Subject: Recharge churn at Lumen Tea
>
> Hi Ava, noticed Lumen Tea added Recharge subscriptions.
>
> Most of the subscription churn we see in tea and coffee happens in month two. For one Shopify roaster we cut it from 31% to 19% with a single skip-a-month email.
>
> Want the email?

(42 words in the body. The 31% to 19% figure must be your real result.)

**Sources.** https://www.insidesales.com/leveraging-trigger-events/, https://alexberman.com/cold-email-buyer-selection-beats-copywriting

## 9. Cycle mailing vs sequence

**What it says.** Berman's follow-up guide plans 4 to 6 follow-ups over 2 to 3 weeks, each adding something new. A separate breakdown on his site describes mapping every reachable buyer in the market and contacting each person once per cycle, every 30 to 60 days, with fresh copy. Instantly's 2026 benchmark post reports about 58% of replies arriving on the first email; Hunter's 2025 report finds campaigns with follow-ups average 4.9% replies against 3% without, and that unsubscribes rise after the third follow-up.

**Decision rule.**

| Market size (validated contacts) | Average deal value | Use |
|-|-|-|
| Under 5,000 | Over $10,000 | 4 to 5 touch sequence, then account-level CEO-down rotation |
| 5,000 to 50,000 | Any | 3 to 4 touch sequence, re-mail non-responders after 60 days with a new angle |
| Over 50,000 | Under $5,000 | One touch per cycle, new copy every 30 to 60 days |

**Sources.** https://alexberman.com/cold-email-follow-up, https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown, https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/, https://hunter.io/the-state-of-cold-email-2025

## Choosing a framework

| Situation | First touch | Follow-up arc |
|-|-|-|
| Local business with strong rating, you have a similar client | 3C | Case study, then question, then breakup |
| Local business with weak rating or few reviews | Problem-first question | PAS, then offer, then breakup |
| Ecommerce store with a trigger (new app, platform) | Trigger plus offer | Proof, then alternative angle, then breakup |
| B2B title at a company that is hiring for the role you serve | PAS | Case study, then referral ask |
| Large market, low deal value | Three-sentence short email | None in cycle, re-mail in 30 to 60 days |

## Benchmarks to test against (dated, not promises)

| Metric | Figure | Source and date |
|-|-|-|
| Average reply rate | 3.43% | Instantly 2026 benchmark report, cited in Instantly's March 2026 post |
| Average reply rate | 4.1% across 11M emails | Hunter, State of Cold Email 2025 |
| Reply rate by size | 5.8% for campaigns of 50 or fewer recipients, 2.1% for 1,000+ | Hunter, State of Cold Email 2025 |
| First email share of replies | About 58% | Instantly, March 2026 |
| Open rates | Unreliable: Apple Mail Privacy Protection preloads images, logging opens that never happened | Postmark, 2021 (updated 2022) |

## Sources

- https://alexberman.com
- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://devrims.com/blog/alex-berman-techtalk-interview-005/
- https://www.11x.ai/guides/josh-braun-cold-outreach-method
- https://copyblogger.com/problem-agitate-solve/
- https://ebsco.com/research-starters/marketing/aida-model
- https://www.insidesales.com/leveraging-trigger-events/
- https://hunter.io/blog/cold-email-word-count
- https://hunter.io/the-state-of-cold-email-2025
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://dmarcreport.com/blog/microsoft-outlook-dmarc-requirements-may-2025/
- https://crtc.gc.ca/eng/com500/faq500.htm
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/
