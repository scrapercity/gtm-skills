# Cold Email Frameworks

Original summaries of the cold email frameworks this repo relies on. Each one lists where it comes from, when to use it, when to skip it, and a short example built on ScraperCity fields. Every example body stays under 100 words, the cap `cold-email-copywriting` enforces (Jason Bay's "100 words or fewer", Gong blog, July 2025). Benchmarks are starting hypotheses with a source and a date.

Field names used in the examples come from ScraperCity outputs: Local Business Database rows carry `title`, `category_name`, `city`, `total_score` (Google rating), `reviews_count`, `website` and `contact_first_name`; Lead Database rows carry `title`, `company_size`, `employees_count`, `company_annual_revenue`, `company_industry` and `company_city`; Store Leads filters cover platform, apps and technologies. Output fields are documented in the package's AGENT_DOCS.txt (https://github.com/scrapercity/scrapercity-cli/blob/main/AGENT_DOCS.txt); tool inputs are in `references/scrapercity-catalog.md`.

## Constraints every framework sits inside

| Constraint | Rule | Source |
|-|-|-|
| Authentication | SPF, DKIM and a DMARC record (p=none or stricter) with From alignment for bulk senders | Google sender guidelines, Yahoo sender best practices, Microsoft Outlook (enforced May 5, 2025) |
| Complaint rate | Gmail: stay under 0.1%, never reach 0.3%. Yahoo: under 0.3% | Google, Yahoo |
| Unsubscribe | One-click unsubscribe for bulk senders; unsubscribes honored within 2 days | Google sender guidelines, Yahoo sender best practices |

These limits shape copy: plain text from an authenticated sending domain, an opt-out line in every touch, and complaint rates watched per domain.

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
| 10 | Creative Ideas campaign | Eric Nowoslawski (as broken down on alexberman.com) | Agencies and services with several deliverables; large lists where hand research does not scale | You cannot list what you deliver, or nobody will review the AI output |
| 11 | BAB: Before, After, Bridge | Copywriting tradition (GMass guide) | Offers that produce a gain the reader can picture | Products that only prevent a loss (insurance, security) |
| 12 | Reason, Problem, Proof, Ask | Jason Bay (Outbound Squad), Gong blog 2025 | B2B titles where a peer customer is the strongest proof | You have no customer in the reader's industry |
| 13 | PQS and PVP | Jordan Crawford (Blueprint) | Segments where public data shows tension you can compute | The data points are guesses, or the message would not survive the pay-to-receive test |
| 14 | Problem-first PAS (lemlist) | lemlist copywriting guidance | One pain per ICP, written in the prospect's words | The pain is vague or generic to every company |
| 15 | Awareness levels | Eugene Schwartz, Breakthrough Advertising (1966) | Choosing a problem-led vs solution-led opener | Never skip; run it before picking 2 to 14 |

## 1. Targeting-first (30/30/50)

**What it says.** Berman's site splits cold email results into 30% targeting, 30% offer and 50% deliverability. Copy is not one of the three. A roundup on his site argues that choosing a better buyer (a manufacturer with 15+ employees instead of a startup) changed deal size more than any rewrite.

**When to use.** At the start of every campaign, and whenever replies drop. Fix in this order: is mail reaching the inbox, is the list the right buyer, is the offer specific. Only then rewrite copy.

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
> Want a 10 minute look at what we changed?

(51 words in the body. The case study must be true; never invent one.)

**Sources.** https://alexberman.com, https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/, https://devrims.com/blog/alex-berman-techtalk-interview-005/

## 3. Offer-led email

**What it says.** Berman's article "Cold Email Doesn't Fail, Your Offer Does" says the offer is what earns a reply. Build it from a measured client outcome, as one sentence: niche, result, mechanism. Build the list after the offer. Adding one line of documented proof to an existing campaign is reported on that page to lift replies sharply (self-reported).

**When to use.** Always, as the core of the email. The other frameworks are wrappers around an offer.

**Offer test.** Fill this sentence with measured numbers: "We help [niche] get [result with number] in [time] by [mechanism]." If any bracket stays vague, the offer is not ready.

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

**What it says.** Lead with a neutral question about a problem the reader may have, with no pitch. The 11x summary of Josh Braun's method describes curiosity questions that let the prospect reflect instead of defend, low-pressure closes such as asking whether the prospect wants to explore an idea, and emails under 80 words. Berman's templates page includes a "Direct Question" template that asks whether the prospect currently does a specific thing.

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

**Cold email adaptation.** Keep "agitate" to one factual line with a number. Readers mark drama as spam. Replace "solve" with a proof line and a question.

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
> Want a quick call to see if that timeline fits you?

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

(42 words in the body. The 31% to 19% figure must be your own measured result.)

**Sources.** https://www.insidesales.com/leveraging-trigger-events/, https://alexberman.com/cold-email-buyer-selection-beats-copywriting

## 9. Cycle mailing vs sequence

**What it says.** Berman's follow-up guide plans 4 to 6 follow-ups over 2 to 3 weeks, each adding something new. A separate breakdown on his site describes mapping every reachable buyer in the market and contacting each person once per cycle, every 30 to 60 days, with fresh copy. Instantly's 2026 benchmark post reports about 58% of replies arriving on the first email. Hunter's State of Email Outreach 2026 (31 million emails sent in 2025) found three messages roughly doubled replies against one (6.8% vs 3.3%) and called three the best balance; its 2025 report found unsubscribes rising after the third follow-up.

**Decision rule.** The TAM breakdown says cycle mailing works when the market or the deal is large enough, and sets no cutoff. The campaign playbook in `cold-email-strategy` turns that into a capacity test.

| Situation | Use |
|-|-|
| A short list of high-value accounts with several buyers each | 3 to 4 touch sequence, CEO first, next level down after one to two weeks (Berman) |
| One email per person per 60-day cycle would leave inboxes idle | 3 touch sequence (a fourth only when no new contacts are waiting to start); rest non-responders 60 days, then a new angle |
| One email per person per 60-day cycle fills the daily sends | One touch per cycle, fresh copy, 60 days between cycles |

**Sources.** https://alexberman.com/cold-email-follow-up, https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown, https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/, https://hunter.io/the-state-of-cold-email-2025, https://hunter.io/the-state-of-cold-email

## 10. Creative Ideas campaign

**What it says.** Eric Nowoslawski of Growth Engine X built this campaign while running outbound for Instantly. Alex Berman broke down two of his videos on alexberman.com in March 2026. The email opens with one line about the prospect, offers three ideas for how the sender could help that specific business, adds a one-line value prop and asks one question. An LLM writes the ideas per row from the prospect's company description. The rules Berman's pages attribute to Nowoslawski: tie every idea to something the business sells, write the example emails by hand (about 10, across different audience types), list the idea areas that are off-limits, and keep the long system prompt identical across rows so cached-input pricing applies. His warning case: on a software agency campaign the model proposed builds the client could not deliver, so strong replies turned into deals nobody could fulfil. The phrase his breakdown uses for the fix is "constrain the creativity".

**Reported result (self-reported, undated, published March 2026).** In a split test for Instantly, the creative ideas variant needed 85 contacts per opportunity, against 175 for a two-sentence direct email and 341 for case-study matching. Fewer contacts per opportunity is better. Treat it as a hypothesis to test in your own cell.

**Build it.**

| Step | Rule |
|-|-|
| 1. Capability list | Write the things you deliver today, each with one proof point. Every idea in every email must map to one row. |
| 2. Off-limits list | Name what the model may never propose (table below). Put it in the system prompt. |
| 3. Row inputs | Company description from the prospect's site plus ScraperCity fields. The model may only cite facts present in those inputs. |
| 4. Hand-write 10 | Write 10 finished emails yourself for real rows of different types. They become the few-shot examples. |
| 5. Review | Read the dry-run outputs before anything sends (`cold-email-copywriting`, `references/personalization-and-merge-fields.md` section 8). |
| 6. Format | Test three ideas against one idea plus a P.S. idea in the same cell. |

**Off-limits list (starter, edit per client).**

| Off-limits | Why |
|-|-|
| Services or features not on the capability list | Wins replies you cannot fulfil |
| Numbers about the prospect's revenue, margins or traffic not in the inputs | Invented facts; reads as a guess when wrong |
| Guarantees, prices, discounts | Commits the sender to terms in a cold email |
| Medical, tax or financial advice | Outside the offer |
| Naming the prospect's competitors or customers | Can be wrong |
| Ideas that need the prospect to change platform, unless migration is a capability | The reader hears "start over" |

**Format choice.** Berman's March 13, 2026 breakdown prefers the shorter variant: one idea in the body and a second idea in a P.S. Leslie Venetz advises against bullets in cold email because they read like a brochure (her 1-10-100 post, September 2026). Start with the one-idea plus P.S. version and test the three-idea list against it.

**ScraperCity example, three ideas** (`scrape_store_leads` with `platform: "shopify"`, `apps: "Klaviyo"`, `category: "pet supplies"`; fields used: store name, platform, app, category; sender builds Klaviyo flows):

> Subject: 3 ideas for Northpaw
>
> Hi Dana, Northpaw sells dog treats on Shopify and already runs Klaviyo.
>
> Three flows we could build inside your Klaviyo account:
>
> 1. A reorder reminder timed to when a bag usually runs out.
> 2. A win-back email for buyers who never placed a second order.
> 3. A day 10 email asking for a photo review.
>
> A treats brand we work with added $11,400 in repeat revenue from the first one in 45 days.
>
> Want the reorder email as a draft?

(80 words in the body.)

**One idea plus P.S. variant** (same row):

> Hi Dana, Northpaw sells dog treats on Shopify and already runs Klaviyo.
>
> A reorder reminder timed to when a bag runs out is usually the fastest repeat-revenue win for a treats store. We would build it inside your Klaviyo account in a week.
>
> P.S. If reorders are covered, would a win-back email for buyers who never ordered twice be more useful?

(61 words in the body. The P.S. carries the only question, so the email still has one ask.)

**Sources.** https://alexberman.com/cold-email-automation-clay-creative-ideas-breakdown, https://alexberman.com/creative-ideas-campaign-cold-email-infrastructure, https://leslievenetz.substack.com/p/1-10-100-b2b-cold-email

## 11. BAB: Before, After, Bridge

**What it says.** Three steps: the reader's situation today (Before), the situation once the problem is solved (After), and how you get them there (Bridge), followed by one ask. GMass's guide (Sam Greenspan, February 2023, updated February 2026) gives no origin for the formula. It recommends a researched Before, an After the reader can picture, a Bridge that leads with one proof point, and limiting BAB to offers that create a gain. Products that only prevent a loss fit PAS better.

**Cold email adaptation.** One sentence per step. The Before must come from a list field. The After must be a result you have measured for a client, stated as that client's result, never as a promise to the reader.

**ScraperCity example** (`query_local_business_database` with `category: ["HVAC contractor"]`, `city: "Mesa"`, `state: "AZ"`, `minRating: 4.5`, `maxReviews: 60`; fields `title`, `total_score`, `reviews_count`, `city`):

> Subject: reviews at Comfort Air
>
> Hi Mark, Comfort Air has 4.7 stars on 38 reviews. The three HVAC shops ranked above you in Mesa each have 250 or more.
>
> A Gilbert shop with the same rating went from 52 to 190 reviews in five months.
>
> The difference was a text with the review link, sent when the tech closes the ticket.
>
> Want the text they send?

(61 words in the body.)

**Sources.** https://www.gmass.co/blog/before-after-bridge-copywriting/

## 12. Reason, Problem, Proof, Ask (Jason Bay)

**What it says.** Jason Bay runs Outbound Squad. His July 2025 post on the Gong blog draws on more than 28 million cold emails analyzed in Gong. His example email follows this order: a relevant reason for writing, one problem in the buyer's own words, specific proof from similar customers, and one clear ask. He sets the length at "100 words or fewer", in three or four sentences. The same post reports that pitching cut reply rates by up to 57% and that buzzwords and numbers in subject lines cut opens. Some summaries call this shape pain, value, proof. The order above follows his post.

**When to use.** B2B titles from the Lead Database where you can name a customer in the same industry or size band.

**When to skip.** No peer proof. Use PQS and PVP or a problem-first question instead.

**ScraperCity example** (`query_lead_database` with `title: "Head of Revenue Operations"`, `industry: ["computer software"]`, `minEmployees: 100`, `maxEmployees: 500`; fields `title`, `employees_count`, `company_industry`):

> Subject: territory lists at Corvane
>
> Hi Priya, RevOps leads at software companies around 300 people tell us territory planning eats the first two weeks of every quarter.
>
> The time goes to cleaning account lists by hand before reps can work them.
>
> Two of our customers at that size, both in HR software, now start the quarter with validated lists on day one.
>
> Want to compare how you build yours?

(64 words in the body.)

**Sources.** https://www.gong.io/blog/does-cold-email-even-work-any-more-heres-what-the-data-says

## 13. PQS and PVP (Jordan Crawford)

**What it says.** Jordan Crawford, founder of Blueprint, described both terms on The Transaction podcast (episode 55, May 16, 2025). A Pain-Qualified Segment (PQS) is a list defined by two to five data points that together imply tension at the account, with a timing element. He keeps the heuristics simple and argues that the list is the message: if you know why a company is on the list, you know what to say. A Permissionless Value Proposition (PVP) is a message that is useful to the recipient on its own, before your product comes up. His bar for a PVP is "a message that people will pay to receive". In his process the data work comes first and the AI only rewords it, so the model invents nothing.

**Pay-to-receive test.** Before a PVP ships, answer all four with yes:

| Question | Fails when |
|-|-|
| Is every fact computed from data about this account? | It restates their own website or a generic statistic |
| Would they have to spend time or money to get this themselves? | They can see it in one search |
| Can they act on it without buying from you? | The value depends on a call with you |
| Would a peer at a similar company want the same analysis for their own account? | It only makes sense as a pitch |

**ScraperCity PQS example.** Data points from one `query_local_business_database` pull of every dentist in Plano, TX: `total_score` 4.6 or higher, `reviews_count` under 60, and a computed gap against the five highest-review practices in the same city. Rating plus a review gap means good care that searchers cannot see.

**ScraperCity PVP example:**

> Subject: Plano dentist review counts
>
> Hi Dr. Lee, we pulled all 41 dental practices in Plano from Google.
>
> Lakeside Smiles ranks 4th of 41 by rating and 33rd by review count. The five practices with the most reviews average 212; you have 47.
>
> Want the full ranked list of the 41?

(46 words in the body. Every number comes from the pull; recompute before each send.)

**Sources.** https://thetransactionpod.com/episodes/inverting-your-go-to-market-strategy-thinking-with-jordan-crawford-ep-55/transcript

## 14. Problem-first PAS (lemlist)

**What it says.** lemlist's copywriting guidance in its help center (lemCoach article, March 5, 2026) opens with one specific pain the prospect deals with daily, in their own language. It then puts a cost on the pain (time, money or missed opportunities), describes the fix in one or two sentences, and closes with a value-based yes or no question. The ask is often a resource instead of a meeting. The article keeps emails under about 125 words, recommends a separate campaign per ICP, warns against flattery such as website compliments and against invented urgency, and sums up the standard as "Write emails you would reply to." lemlist's blog post on pain points adds that too many first-person statements turn the email toward the sender.

**Cold email adaptation.** This repo caps bodies under 100 words (Jason Bay), stricter than lemlist's 125. Write the pain from a list field when one exists.

**ScraperCity example** (`scrape_store_leads` with `platform: "woocommerce"`, `category: "apparel"`, `minEstimatedMonthlyVisits: 20000`; fields: store name, platform, traffic band):

> Subject: WooCommerce updates at Linen Row
>
> Hi Sam, apparel stores on WooCommerce at Linen Row's traffic tell us plugin updates break checkout two or three times a year.
>
> Each break costs a day of sales before anyone notices.
>
> We run update testing on a staging copy every week, so checkout breaks there first.
>
> Want the checklist we test against?

(53 words in the body.)

**Sources.** https://help.lemlist.com/en/articles/13941977-lemcoach-how-to-write-cold-emails-that-get-replies-pas-framework, https://lemlist.com/blog/how-to-use-prospects-pain-points-for-more-replies

## 15. Awareness levels (Eugene Schwartz)

**What it says.** In *Breakthrough Advertising* (1966) Eugene Schwartz argues that the opening of any ad depends on how much the prospect already knows. Summaries of the book describe five states, often labelled unaware, problem aware, solution aware, product aware and most aware. A prospect who already wants the product needs only the offer. A prospect who feels the need but knows no solution needs the need named and the product shown as the answer. A prospect who does not see the need at all needs an opening they recognize about their own situation, with no product in it.

**Cold email use.** A list built on fit alone sits at unaware or problem aware, so a product-first opener has nothing to attach to. Pick the opener from evidence in the list:

| Awareness | Evidence in the list | Opener | Framework |
|-|-|-|-|
| Unaware | Fit only, no trigger | An observation or a computed fact about them | PVP, problem-first question |
| Problem aware | Low rating, low review count, hiring for the problem role | Name the problem and its cost | PAS, BAB, lemlist problem-first |
| Solution aware | A competing tool in `apps` or `technologies` | Name the approach they already use, then the difference | Trigger plus offer, three-sentence |
| Product aware | Past reply, demo or trial in your CRM | Offer and proof | Offer-led, 3C |
| Most aware | Asked for pricing or a proposal | The offer and a date | Direct ask, outside cold email |

Rule: if the evidence column is empty, treat the row as unaware and lead with the problem or a fact, never with the product.

**Sources.** https://shortform.com/pdf/breakthrough-advertising-pdf-eugene-m-schwartz, https://nanoglobals.com/recommended/breakthrough-advertising-review/ (secondary summaries; the 1966 book is not online)

## Choosing a framework

| Situation | First touch | Follow-up arc |
|-|-|-|
| Local business with strong rating, you have a similar client | 3C | Case study, then question, then breakup |
| Local business with weak rating or few reviews | Problem-first question | PAS, then offer, then breakup |
| Ecommerce store with a trigger (new app, platform) | Trigger plus offer | Proof, then alternative angle, then breakup |
| B2B title at a company that is hiring for the role you serve | PAS | Case study, then referral ask |
| Large market, low deal value | Three-sentence short email | None in cycle; next cycle email after 60 days with fresh copy |
| Agency or service with several deliverables, list too large to research by hand | Creative Ideas, one idea plus P.S. | Second idea, then case study, then breakup |
| Public data lets you compute a gap or rank for each account | PVP built on a PQS | A second computed fact, then referral ask |
| B2B title, you have a customer in the same industry | Reason, Problem, Proof, Ask | Different problem, then resource with no ask, then breakup |
| Gain you can picture (more reviews, more repeat orders) | BAB | Proof, then reframe, then breakup |

Run section 15 first: the awareness level sets whether the first line names a problem, a fact or the product.

## Benchmarks to test against (dated, not promises)

| Metric | Figure | Source and date |
|-|-|-|
| Average reply rate | 3.43% | Instantly 2026 benchmark report, cited in Instantly's March 2026 post |
| Average sequence reply rate | 4.5% across 31M emails sent in 2025 | Hunter, State of Email Outreach 2026 |
| Reply rate by size | 6.2% for sequences of 21 to 50 recipients, 2.4% for over 500 | Hunter, State of Email Outreach 2026 |
| Messages per sequence | Three messages: 6.8% replies vs 3.3% for one | Hunter, State of Email Outreach 2026 |
| Average reply rate (prior year) | 4.1% across 11M emails | Hunter, State of Cold Email 2025 |
| First email share of replies | About 58% | Instantly, March 2026 |
| Open rates | Unreliable: Apple Mail Privacy Protection preloads images, logging opens that never happened | Postmark, 2021 (updated 2022) |
| Creative Ideas vs other campaign types | 85 contacts per opportunity, against 175 (two-sentence direct) and 341 (case-study matching) | Nowoslawski split test for Instantly, self-reported, undated, published on alexberman.com March 2026 |
| Effect of pitching | Pitching cut reply rates by up to 57% | Jason Bay, Gong blog, July 2025 (28M+ emails in Gong) |
| Body length | Under 100 words; 25 to 100 practical range | Jason Bay (Gong, 2025); Leslie Venetz (1-10-100 post, September 2026) |

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
- https://hunter.io/the-state-of-cold-email
- https://instantly.ai/blog/email-sequence-benchmarks-2026-whats-a-good-open-rate-reply-rate-and-cost-per-meeting/
- https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
- https://support.google.com/a/answer/14229414
- https://senders.yahooinc.com/best-practices/
- https://dmarcreport.com/blog/microsoft-outlook-dmarc-requirements-may-2025/
- https://alexberman.com/cold-email-automation-clay-creative-ideas-breakdown
- https://alexberman.com/creative-ideas-campaign-cold-email-infrastructure
- https://leslievenetz.substack.com/p/1-10-100-b2b-cold-email
- https://www.gmass.co/blog/before-after-bridge-copywriting/
- https://www.gong.io/blog/does-cold-email-even-work-any-more-heres-what-the-data-says
- https://thetransactionpod.com/episodes/inverting-your-go-to-market-strategy-thinking-with-jordan-crawford-ep-55/transcript
- https://help.lemlist.com/en/articles/13941977-lemcoach-how-to-write-cold-emails-that-get-replies-pas-framework
- https://lemlist.com/blog/how-to-use-prospects-pain-points-for-more-replies
- https://shortform.com/pdf/breakthrough-advertising-pdf-eugene-m-schwartz
- https://nanoglobals.com/recommended/breakthrough-advertising-review/
