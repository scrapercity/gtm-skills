# Cold Email Sequence: Shopify Subscription Stores Using Recharge

Cell: US Shopify stores in food and beverage with Recharge installed, 10,000 to 150,000 estimated monthly visits. Platform: Instantly. Written: 2026-10-12.

Sender: Lena Ortiz, Retention Lab (a fictional retention email agency used for this example).

## Campaign Inputs

| Field | Value |
|-|-|
| Offer sentence | We help Shopify subscription brands in food and beverage cut month two cancellations by a third in 45 days with a skip-a-month email sent before the second charge. |
| Segment and buyer | Founders and ecommerce leads at US Shopify food and beverage stores, 10,000 to 150,000 monthly visits |
| Trigger or relevance fact | Recharge installed (subscription revenue at stake); store category |
| Proof line source | Coffee subscription client, April to May 2026, Recharge cancellation report: month two cancellations 31% to 19% |
| List source and tool | `scrape_store_leads` with platform "shopify", apps "Recharge", category "food & drink", countryCode "US", minEstimatedMonthlyVisits 10000, maxEstimatedMonthlyVisits 150000, emails true, totalLeads 1500 |
| Framework | Trigger plus offer (touch 1), proof (touch 2), resource (touch 3), breakup (touch 4) |

Cost of the list, shown to the user and approved after `check_wallet`: 1,500 leads x $0.0039 = $5.85; `find_emails` on 600 stores with no named contact, 300 found x $0.05 = $15.00; `validate_emails` on 1,500 addresses x $0.0072 = $10.80. Total $31.65.

## Merge Fields and Fallbacks

| Tag | Source field | Fill rate in sample | Fallback |
|-|-|-|-|
| first_name | Contact first name from Store Leads or Email Finder | 17 of 20 | there |
| store_name | Store name, ".com" stripped | 20 of 20 | your store |
| category | Store category, lowercased ("coffee", "tea", "snacks") | 19 of 20 | subscription |

## Sequence

### Touch 1

Subject: Recharge churn at {{store_name | your store}}
Send day: 0

```text
Hi {{first_name | there}},

Noticed {{store_name | your store}} runs subscriptions on Recharge.

For a coffee brand on the same setup, one skip-a-month email sent three days before the second charge cut month two cancellations from 31% to 19% in 45 days.

Want the email we used?
```

### Touch 2

Subject: (same thread)
Send day: 3

```text
Hi {{first_name | there}},

One more data point. A tea subscription store tried the same email in June. Skips went up, cancellations went down, and they kept 41 more subscribers in the first month.

Should I send both versions so you can compare?
```

### Touch 3

Subject: (same thread)
Send day: 7

```text
Hi {{first_name | there}},

Different angle: most {{category | subscription}} brands we look at send nothing between the first order and the second charge.

I mapped the four emails that fill that window, with send times. It fits on one page and needs no call.

Want me to send it over?
```

### Touch 4

Subject: (same thread)
Send day: 12

```text
Hi {{first_name | there}},

I will close this out for now. If month two churn comes up later, reply here and I will pick it back up.

Or is someone else at {{store_name | your store}} the right person for retention?
```

## Subject Line Tests

| Test | Variant A | Variant B | Per variant | Decide on |
|-|-|-|-|-|
| 1 | Recharge churn at {{store_name}} | Question about {{store_name}} | 200 delivered | Positive replies per 100 delivered |
| 2 | Winner of test 1 | month two at {{store_name}} | 200 delivered | Positive replies per 100 delivered |

Test 1 runs only after the ask test (touch 1 "Want the email we used?" against "Worth 10 minutes this week?") settles, per the strategy plan's test order.

## Footer and Compliance

```text
Lena Ortiz, Retention Lab
2100 Example Avenue, Suite 400, Austin, TX 78701
Not a fit? Reply "no" and I won't follow up.
```

| Requirement | How it is met | Law or policy |
|-|-|-|
| Accurate From and subject | Real sender name and Retention Lab domain; subjects describe the email | CAN-SPAM (FTC) |
| Postal address | Office address in every touch | CAN-SPAM (FTC) |
| Opt-out | Reply-based opt-out in the footer plus Instantly's one-click unsubscribe header | CAN-SPAM; Google and Yahoo sender rules |
| Opt-out processing | Same day via Instantly blocklist; legal limit 10 business days, Yahoo asks for 2 days | CAN-SPAM; Yahoo |
| Geography | US stores only (countryCode "US"); no Canadian stores, so CASL does not apply | CASL scope |
| Tracking | Open and click tracking off | Google sender guidelines (complaint risk); Apple MPP makes opens unreliable |

## QA Results

| Touch | Words | Ends with question | Links | Fallback render ok |
|-|-|-|-|-|
| 1 | 42 | Yes | 0 | Yes, row with empty first_name rendered "Hi there," |
| 2 | 41 | Yes | 0 | Yes |
| 3 | 47 | Yes | 0 | Yes, empty category rendered "most subscription brands" |
| 4 | 36 | Yes | 0 | Yes, empty store_name rendered "at your store" |

Rendered sample (row: first_name "Dana", store_name "Northpaw Coffee", category "coffee"), touch 1:

```text
Hi Dana,

Noticed Northpaw Coffee runs subscriptions on Recharge.

For a coffee brand on the same setup, one skip-a-month email sent three days before the second charge cut month two cancellations from 31% to 19% in 45 days.

Want the email we used?
```

Why each line is there: the Recharge fact explains why a retention email is relevant now; the proof uses the same category and the same app; the ask offers an asset instead of a meeting, which is the variant under test. Every number comes from the client's Recharge report named in Campaign Inputs.
