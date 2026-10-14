# Account Scoring and Tiers

How to turn the deduped account file into a ranked, tiered target list: hard exclusions first, a fit score built only from columns the file fills, weights from win-rate lift when closed deals exist, tier sizes set by team capacity, a spend ceiling per account from first-year gross profit when the user supplies the deal inputs, and a backtest on current customers before anyone works the list.

Run it when the user asks which accounts to work first, wants Tier 1 to 3, an ABM target list or territory assignments. A user who only asked how big the market is gets the TAM report without this section.

## 1. Hard exclusions before any score

These rows never get a score; they leave the scored set with a reason, so a high fit score cannot carry them back in.

| Exclusion | Typical rule | Where it comes from |
|-|-|-|
| Outside the serviceable area | Metro or country the team cannot sell or support | `in_sam = false` |
| Wrong business type | Supply houses, manufacturers, agencies, resellers in a contractor TAM | Category review, `notCategory`, `notKeywords` |
| Too small to pay back | Below the size where the ACV can be recovered (section 6) | Employee or review floor |
| Customers and open opportunities | Domain match to the CRM | Suppression files |
| Competitors and partners | Domain list from the user | Suppression files |
| Lost on fit in the last 12 months | Domain match to closed-lost with a fit reason | CRM export |
| Missing a technology the product requires | A Shopify app and a store on another platform; a Salesforce add-on and no Salesforce | Tech Stack Search domain list (one run per technology) |
| Locked into a technology the product replaces, on a contract the user knows renews later | Signed a multi-year deal with a competitor this year | CRM notes, closed-lost reason; re-check at the renewal date |

## 2. Score only what the file fills

A trait filled for some rows and blank for others rewards data-rich accounts and punishes the rest. Report the fill rate of every candidate column and score a column only when it is filled on at least the share of SAM rows the user sets; report the others as "not scored, coverage N%".

| Attribute | Column | Local business market | B2B market |
|-|-|-|-|
| Size | `employees`, or `reviews` as a local proxy | Reviews band | Employee band |
| Business type match | `category`, `keywords` | Core category vs adjacent | Core keyword vs adjacent |
| Quality | `rating` | Rating band | Rarely available |
| Technology | Tech Stack Search hit | Booking or POS platform | CRM, platform, cloud |
| Existence confidence | `confidence` (found-in-N) | High, Medium, Low | High, Medium, Low |
| Reachability | `website`, named contact | Website present, named owner | Domain present |

## 3. Weights

### With closed deals joined to the file by domain

Compute lift per attribute value as in the ICP evidence worksheet (win rate with the value divided by the overall win rate). Convert to points:

```text
points = round(10 * log2(lift)), capped at +10 and -10
values seen on fewer closed deals than the user's minimum score 0
account fit score = sum of points across scored attributes
```

Worked numbers (illustrative, a field-service app selling to HVAC contractors; 112 closed deals, 38 won, overall win rate 33.9%; the user's minimum is 10 deals per value):

| Attribute value | Deals | Won | Win rate | Lift | Points |
|-|-:|-:|-:|-:|-:|
| 50+ Google reviews | 48 | 25 | 52.1% | 1.54 | 6 |
| Rating 4.0 or higher | 81 | 31 | 38.3% | 1.13 | 2 |
| Confidence High (found in 3+ sources) | 40 | 19 | 47.5% | 1.40 | 5 |
| Named owner on file | 66 | 27 | 40.9% | 1.21 | 3 |
| Fewer than 10 reviews | 22 | 2 | 9.1% | 0.27 | -10 (capped from -19) |
| Uses a competing dispatch app | 8 | 1 | 12.5% | 0.37 | 0 (under 10 deals) |

Check one row: 25 / 48 = 52.1%; 52.1 / 33.9 = 1.54; log2(1.54) = 0.62; 10 x 0.62 rounds to 6.

### Without closed deals

Score each attribute 0, 5 or 10 from the best-fit customer traits (10 = matches the best-fit examples, 5 = adjacent, 0 = neither), label every weight "assumption, no deal data", and recalibrate with lift once each value has the user's minimum of closed deals.

## 4. Fit decides the tier; timing, engagement and access move it

Fit is structural and changes slowly; the three movers below change weekly. Keeping them out of the score keeps the score stable and testable, and lets a mover expire.

| Mover | Examples | Where it comes from | Effect |
|-|-|-|-|
| Dated trigger | New owner or leader in the buyer's seat, hiring for the role the product serves, a new location, a technology change | `signal-triggered-outbound`, a Sales Navigator alert or Buyer intent spotlight | Up one tier for the next send cycle |
| First-party engagement | A recent pricing or demo page visit, webinar attended, replied to an earlier sequence, demo booked and missed | The user's CRM or marketing automation export, joined by domain | Up one tier for the next send cycle |
| Access | A champion at a current customer now works here (job change), a colleague connected through TeamLink, a closed-lost on timing whose stated timing has arrived | CRM; a Sales Navigator lead list of customer champions filtered by Changed jobs; the With TeamLink intro filter | Up one tier for the next send cycle; the warm path goes into the contact plan as Day 1 |

An account with two movers at once goes up one tier, not two. No mover lifts an account past a hard exclusion. The lift lasts one send cycle; Alex Berman sends one email per person per cycle and spaces cycles 30 to 60 days apart (alexberman.com TAM breakdown, October 2026). Check the one-tier step in the quarter-end read (section 8).

## 5. Tier sizes come from capacity

Cut tiers by how many accounts the team can work at each depth, then check the score cutoffs that produces. A Tier 1 of 600 accounts for two reps means none of them gets Tier 1 treatment.

| Tier | Work per account | Size rule | Example: 4 AEs, 2 SDRs |
|-|-|-|-|
| 1 | Account brief, named contacts up to the user's cap, email plus manual calls, person-level personalization | AEs x accounts each researches and works per quarter | 4 x 30 = 120 |
| 2 | Fewer contacts than Tier 1, account-level personalization (trigger, news, hiring) | SDRs x new accounts a week x 13 weeks | 2 x 46 x 13 = 1,196, rounded to 1,200 |
| 3 | 1 contact, segment-level copy | Rest of SAM at or above the score floor | Remainder |
| Not worked | Nurture or nothing | Below the score floor | Remainder |

The three personalization depths follow Alex Berman's segment, account and person levels; the capacity numbers per rep are the user's. Without them, cut tiers by score and write one Capacity line asking for AE and SDR headcount; never invent a team size.

## 6. Spend ceiling per account

Only when the user supplies ACV, gross margin and win rates per tier (measured in the CRM, or the user's own figures). Write them on one "Deal inputs (from you):" line under the tier table. Without them, leave the column out: a ceiling built on assumed win rates is a budget nobody asked for.

David Skok's SaaS metrics put healthy businesses at recovering acquisition cost within 12 months, often 5 to 7. Turn that into a ceiling per worked account:

```text
first-year gross profit per customer = ACV x gross margin
ceiling per worked account           = first-year gross profit x accounts won per account worked in that tier
```

Example: ACV $3,600, gross margin 80%, first-year gross profit $2,880. If the user's CRM shows 1 in 20 worked Tier 1 accounts becoming a customer, the most the team can spend per Tier 1 account, data, tools and rep time included, is $2,880 / 20 = $144. At 1 in 200 for Tier 3 it is $14.40, which rules out manual research for Tier 3 and sets the size floor in section 1: an account whose expected win rate cannot carry the cheapest tier's cost is excluded.

## 7. Backtest on customers before handing over the list

Score current customers as if they were prospects (they are in the file before suppression). Compare where they land with where SAM lands.

```text
concentration = (share of customers in Tier 1 and 2) / (share of SAM in Tier 1 and 2)
```

Example: Tier 1 and 2 hold 1,320 of 6,940 SAM accounts (19.0%) and 31 of 46 customers (67.4%); concentration = 67.4 / 19.0 = 3.5. At or below 1.0 the score does not separate buyers from non-buyers (Tier 1 and 2 hold no larger share of customers than of SAM); the user may set a higher bar. Below the bar: drop the weakest attribute, re-weight, rerun. Write the result in the report as one "Backtest:" line.

## 8. Refresh

| Event | Action |
|-|-|
| Monthly TAM refresh | Re-score new and changed accounts |
| Quarter start | Re-cut tier sizes to current capacity; promote and demote |
| Trigger found | Up one tier for the next send cycle |
| No reply after the number of full sequences the user sets | Down one tier for the period the user sets |
| Each new batch of closed deals | Recompute lift and points |
| Quarter end | Meetings booked per 100 accounts worked, by tier. Tier 1 at or below Tier 2, or Tier 2 at or below Tier 3, means the score ranks the wrong accounts: drop the weakest attribute and re-run the backtest |
| Accounts moved up by a mover | Compare their meetings per 100 with the tier they joined; a mover type that books no better than the tier below loses its lift next quarter |

Change one thing per quarter (a weight, a tier size or a mover), so the next read shows which change moved the meeting rate.

## 9. Report section

```markdown
## Account Tiers

| Tier | Rule | Accounts | Motion | Contacts per account | Spend ceiling per account |
|-|-|-|-|-|-|
| 1 | Score 15+ and top 120 by score | 120 | ... | 3 | $144 |

Capacity: ...
Backtest: ...
```

Tier accounts sum to the SAM account count in the TAM table. The checker enforces that sum and the two lines. The Spend ceiling column appears only with a "Deal inputs (from you):" line; without one, drop the column.

## Sources

- David Skok, SaaS Metrics 2.0 (LTV to CAC above 3, CAC recovered within 12 months): https://www.forentrepreneurs.com/saas-metrics-2/
- Alex Berman, Cold email templates (segment, account and person personalization levels): https://alexberman.com/cold-email-templates
- Gartner, B2B Buying Report (buying groups of five to 11 people, behind the per-account contact cap): https://emt.gartnerweb.com/ngw/globalassets/en/sales-service/documents/trends/gartner-b2b-buying-report.pdf
- Alex Berman, Map your market, skip the follow-ups (one email per person per cycle, 30 to 60 days between cycles, October 2026): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
