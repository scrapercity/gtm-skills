# Cold Email Sequence: Shopify Subscription Stores Using Recharge

Illustrative example. Written: 2026-10-12. Platform: Instantly. Sender: Lena Ortiz, Retention Lab (a fictional retention email agency).

## Copy Audit

### Original

```text
Hi {{first_name}},

I hope this email finds you well! My name is Lena and I'm the founder of Retention Lab, a full-service retention agency. We help ecommerce brands grow with email, SMS, popups, loyalty programs and more. We have worked with over 50 brands and our clients love us.

I'd love to set up a 30 minute call to walk you through our services and show you how we can help {{store_name}} grow revenue. Here is our case study deck: retentionlab.example/deck

Let me know what time works for you!

Lena
```

Subject on the original: "Re: Partnership opportunity".

| Line | Issue | Rule broken | Fix |
|-|-|-|-|
| Re: Partnership opportunity | Fake reply prefix and a pitch in the subject | No pitch in the subject; "Re:" only on a real reply | "second charge at {{store_name}}" |
| Hi {{first_name}}, | No fallback; 3 of 20 sample rows rendered "Hi ," | Every merge tag needs a fallback | {{first_name \| there}} |
| I hope this email finds you well! | The preview spends its first ten words on a pleasantry | The first ten words (subject plus preview) lead with relevance | Open with the client's top cancel reason, a fact the reader recognizes |
| My name is Lena and I'm the founder of Retention Lab | Seller-first opening | Open with the reader, not I, we or our | Start with their subscribers; the sender appears in the signature only |
| We help ecommerce brands grow with email, SMS, popups, loyalty programs and more. | A service list with no result, in vendor words, for no segment | Name the niche, a measured result and how it was reached | The strongest result, in their words, for Recharge stores: month two cancellations 31% to 19% in 45 days |
| We have worked with over 50 brands and our clients love us. | Unverifiable claim | Proof must be measured and attributable | A same-category client with a number |
| I'd love to set up a 30 minute call to walk you through our services | Heavy ask from a stranger, nothing worth replying for | One low-effort ask, with something worth replying for | "Want a copy of that email to adapt for your subscribers?" |
| Here is our case study deck: retentionlab.example/deck | Link in touch 1 | Zero links in touch 1 | Remove; offer the email itself |
| Let me know what time works for you! | Assumes the meeting and ends without a question | Last line ends in a question mark | Merged into the new ask |

Original: 90 words, 12 I/we/our words vs 5 you/your references, 1 link in touch 1, 0 question marks.

### Rewrite

```text
Hi {{first_name | there}},

For a coffee brand on Shopify and Recharge, the top reason subscribers gave for cancelling before the second charge was "too much coffee."

We help Shopify subscription brands on Recharge keep subscribers past that charge. One skip-a-month email, sent three days before it, cut this brand's month two cancellations from 31% to 19% in 45 days.

Want a copy of that email to adapt for your subscribers?

Lena
```

Rewrite: 70 words, 1 I/we/our word vs 1 you/your reference, 0 links, one question. It is touch 1 below.

## Sequence

Sending: weekdays during business hours in each store's local time zone, under 50 sends per inbox per day, on days 0, 3, 7 and 11. Touches 2 to 4 reply in touch 1's thread.

### Touch 1

Thread: new
Subject: second charge at {{store_name | your store}}
Subject B: skip or cancel?
Send day: 0

```text
Hi {{first_name | there}},

For a coffee brand on Shopify and Recharge, the top reason subscribers gave for cancelling before the second charge was "too much coffee."

We help Shopify subscription brands on Recharge keep subscribers past that charge. One skip-a-month email, sent three days before it, cut this brand's month two cancellations from 31% to 19% in 45 days.

Want a copy of that email to adapt for your subscribers?

Lena
```

### Touch 2

Thread: reply to touch 1
Subject: Re: second charge at {{store_name | your store}}
Subject B: Re: skip or cancel?
Send day: 3

```text
Hi {{first_name | there}},

Recharge already lets subscribers skip in the portal, so this may sound covered. The coffee store had portal skip too. The email put that option in their inbox three days before the charge.

A tea store added the same email in June and kept 41 more subscribers that first month.

Want both versions side by side?

Lena
```

### Touch 3

Thread: reply to touch 1
Subject: Re: second charge at {{store_name | your store}}
Subject B: Re: skip or cancel?
Send day: 7

```text
Hi {{first_name | there}},

Different idea, before the holiday orders start. I'll go through the emails {{store_name | your store}} sends between the first box and the second charge and send you a written list of gaps within 3 business days.

It's free, and the list is yours to keep either way.

Want me to take a look?

Lena
```

### Touch 4

Thread: reply to touch 1
Subject: Re: second charge at {{store_name | your store}}
Subject B: Re: skip or cancel?
Send day: 11

```text
Hi {{first_name | there}},

Closing the file on this for now. If month two cancellations become a priority for {{store_name | your store}}, the coffee brand's email (31% to 19% in 45 days) is still yours to adapt.

Is someone else on your team the right person for retention?

Lena
```

## Variants

Each variant replaces touch 1 for the rows its gate selects. Touches 2 to 4 stay the same.

### Variant 1: founders

Kind: persona
For: Founders and owners who run the store themselves and read fast: proof first, no setup line
Gate: rows where the contact title contains Founder, Owner or CEO; every other row gets touch 1
Subject: month two at {{store_name | your store}}

```text
Hi {{first_name | there}},

A coffee brand on Shopify and Recharge was losing 31% of subscribers in month two. One skip-a-month email, sent three days before the second charge, cut that to 19% in 45 days.

Want the email to adapt for {{store_name | your store}}?

Lena
```

### Variant 2: Klaviyo stores

Kind: signal
For: Stores whose installed apps show they already send email from Klaviyo, the tool the coffee client used
Gate: only rows where `apps` lists Klaviyo; rows without it get touch 1
Subject: Recharge and Klaviyo at {{store_name | your store}}

```text
Hi {{first_name | there}},

{{store_name | Your store}} runs Recharge and Klaviyo on Shopify, the same setup as a coffee brand we worked with in April.

Their skip-a-month email, sent from Klaviyo three days before the second charge, cut month two cancellations from 31% to 19% in 45 days.

Want it as a Klaviyo draft for your subscribers?

Lena
```

## Footer

```text
Lena Ortiz, Retention Lab
Not a fit? Reply "no" and I won't follow up.
```

## Merge Fields and Fallbacks

Tags use Instantly's `{{tag | fallback}}` form.

| Tag | List column | Fallback |
|-|-|-|
| first_name | Contact first name | there |
| store_name | Store name, ".com" stripped | your store |

## Test Plan

| Test | Split | Per variant | Decide on |
|-|-|-|-|
| 1. Touch 1 ask | "Want a copy of that email" vs "Open to 10 minutes this week?" | 200 delivered | Positive replies per 100 delivered |
| 2. Touch 1 subject | Subject vs Subject B as written | 200 delivered | Positive replies per 100 delivered |

Decide: once both arms reach 200 delivered, keep the arm whose positive replies beat the other's by at least 2 x the square root of both arms' positive replies added together (12 vs 4: a gap of 8, and 2 x the square root of 16 is 8, so keep the 12). A smaller gap is noise: keep sending both. Run one test at a time, in this order.

## Confirm Before Launch

Nothing open.
