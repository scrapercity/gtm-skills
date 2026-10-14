# Framework Notes: Cold Email Copywriting

Which named sources shape this skill and which file to open for each writing decision.

## Authorities

| Authority | What it contributes | Used in | Evidence type |
|-|-|-|-|
| Alex Berman, alexberman.com FAQ | 3C framework: compliment, case study, call to action | Touch 1 structure | Operator teaching |
| Alex Berman, Lean B2B interview | Same 3C order; tailor each email to the industry; short subjects of a few words | Touch 1, subjects | Interview |
| Alex Berman, templates page | Under 75 words, opener of one or two sentences, "you" over "we", one link max, no pricing or PDFs, subjects under 50 characters, three personalization levels | Length rule, link rule, field choice | Operator teaching, mixed benchmarks |
| Alex Berman, Single Grain video | Close on a question mark; begin with something the reader already believes; neutral subjects such as "Question about [company]" | Ask rule, subjects | Video |
| Alex Berman, Entrepreneur 2017 | Four subject line types; news subjects must match the first line; generic-but-customized for 500+ sends | Subject library | Bylined article |
| Alex Berman, follow-up guide | In-thread follow-ups that each add something new; breakup that offers to close the file | Follow-up rules | Operator teaching |
| Alex Berman, offer article | Proof line from a measured client result | Proof lines | Operator teaching |
| Josh Braun (11x summary) | Neutral curiosity questions, low-pressure closes, under 80 words | Problem-first lines, asks | Secondary summary of his method |
| Craig Elias | Trigger events and the window of dissatisfaction | Trigger first lines | Practitioner framework |
| Leslie Venetz, via Jeff Bajorek's newsletter (February 2025) | Remove "I, we, our" phrases from outreach; no word ratio is given | Seller-first opening check | Interview summary |
| Leslie Venetz, 1-10-100 post (September 2026) | One ask, relevance in the first ten words, under 100 words; seller-first openings; tied to "Earn the Right" | Earn the Right gate, opening check | Practitioner newsletter |
| Jason Bay, Gong blog (July 2025) | Reason, problem, peer proof, ask; 100 words or fewer; pitching cut replies by up to 57% | B2B touch 1, seniority voice | Practitioner post on a vendor dataset |
| Eric Nowoslawski, GTM Engineer podcast notes (July 2025) | Offers worth paying for; every offer answers why someone would not respond; remove risk; per-row negative reviews in a reputation campaign (1 positive reply per 70, self-reported) | Reply offer, objection touch, signal gates | Podcast episode notes |
| Eric Nowoslawski, via alexberman.com (March 2026) | Creative Ideas; hand-written examples first; constrained AI output | AI lines at scale, Creative Ideas cells | Operator video, summarized by Berman |
| Jordan Crawford, The Transaction ep. 55 (May 2025) | PQS and PVP; pay-to-receive bar; AI invents nothing | Claims-only-from-fields rule, PVP lines | Podcast transcript, his own words |
| lemlist help center (March 2026) | Problem-first PAS, resource asks, separate campaign per ICP | Problem-first touches | Vendor guidance |
| Eugene Schwartz, Breakthrough Advertising (1966) | Awareness level sets the opener | Workflow step 3 | Book, via secondary summaries |
| Hunter word count analysis, April 2024 | 20 to 39 words had the highest average reply rate (4.5%) in 34M emails; small differences | Length target | Vendor dataset |
| Instantly help center | `{{RANDOM | a | b}}` spintax and `{{firstName | there}}` fallbacks | Merge syntax | Vendor documentation |
| Google sender guidelines; Yahoo sender best practices | One-click unsubscribe at bulk volume, unsubscribes processed within 2 days, complaint thresholds | Footer and headers | Mailbox provider policy |
| Postmark on Apple MPP | Open tracking is unreliable | No tracking pixel advice | Vendor explainer |

## Routing

| Decision | Open |
|-|-|
| Which framework fits this cell | `references/cold-email-frameworks.md` |
| Exact wording of a first line for a data field | `references/line-library.md` sections 1 to 4 |
| Proof lines, asks, follow-ups, breakups | `references/line-library.md` sections 5 to 9 |
| Subject lines by angle | `references/subject-line-library.md` |
| Which ScraperCity field feeds which tag, and its fallback | `references/personalization-and-merge-fields.md` |
| Spintax, plain text, links, signatures | `references/personalization-and-merge-fields.md` |
| AI-written lines: rollout, prompt template, dry-run review | `references/personalization-and-merge-fields.md` section 8 |
| Length and proof by seniority | `references/line-library.md` section 12 |
| Opening question from the reader's experience, hook test failures, their words by segment | `references/line-library.md` section 15 |
| A full sequence with objection touch, persona and signal variants | `references/line-library.md` section 16 |
| Which list field can gate a signal variant | `references/personalization-and-merge-fields.md` section 9 |
| Objection pre-handles by persona | `references/line-library.md` section 13 |
| Follow-up type (no-ask resource, pre-handle, reframe) | `references/line-library.md` section 14 |
| Persona-specific subject lines | `references/subject-line-library.md` section 10 |
| Creative Ideas, BAB, PQS and PVP, awareness levels | `references/cold-email-frameworks.md` sections 10 to 15 |
| What Berman said, with the URL | `references/alex-berman-cold-email.md` |
| Tool prices for sample pulls | `references/scrapercity-catalog.md` |

## Rules this skill sets where sources differ

| Topic | Range in sources | Rule here |
|-|-|-|
| Body length | Under 70, 75, 80 or 100 words | Hard cap under 100 (Jason Bay, Venetz); aim under 75 (Berman's templates page) |
| Links | One max (Berman) | Zero in touch 1, one max after |
| Subject length | Under 50 characters (Berman), "three to four words" (Lean B2B) | A few words, under 50 characters |
| You/your vs I/we/our | Venetz flags seller-first openings, lemlist flags too many "I" statements; neither sets a number | No body opens with I/we/our/my; no word ratio is enforced |
| Three ideas as bullets vs one idea plus P.S. | Nowoslawski runs three bullets; Berman prefers one plus P.S.; Venetz advises against bullets | Start with one idea plus P.S.; test the bullets against it |
| Asking for a meeting in touch 1 | Berman's 3C ends on a call ask; a roundup on alexberman.com argues for opening a conversation first | Test it: variant A asks for 10 minutes, variant B offers a resource |
| Touch 1 opener | Berman: start from something the reader already believes; Braun: neutral questions; no source tests whether the answer varies | A question about a moment in the reader's week (Braun's neutral question, on something the reader already believes, per Berman) that passes the hook test, then the strongest proof (Berman's 3C puts the case study in the first email) |
| Where the best proof goes | Berman's 3C puts the case study in the first email | Strongest proof in touch 1; touch 2 gets a different result |
| Follow-up gaps | Berman's follow-up guide: 3 to 5 days apart, example schedule day 0, 3, 7, 11, 16, 23 | Day 0, 3, 7, 11 for four touches, unless the strategy plan sets a cadence |
| Subjects on follow-ups | Berman keeps the first three or four touches in one thread | Every touch gets a subject and an alternative; touches 2 to 4 reply in touch 1's thread and keep "Re:" plus its subjects |
| Reply offer when the brief has none | Nowoslawski: offers worth paying for; Berman: a measured result | Propose one in Campaign Inputs, marked for the user to confirm; never send an unconfirmed offer |
| Where the objection goes | Nowoslawski: the offer answers why someone would not respond | Touch 2 by default, named in the buyer's words and answered with a fact |
| Persona coverage | Seniority guidance varies by source | A persona variant of touch 1 whenever the cell holds more than one buyer type; follow-ups shared |
| Named persuasion frameworks in the deliverable | Many copy guides label each email AIDA, PAS or Cialdini principles | Use them to choose; never print the labels for the client |
