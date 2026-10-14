# Glossary

Short definitions for the deliverability, data, phone and program terms used across this repo. Standards and mailbox-provider rules link to the primary source; repo terms point to the skill or reference that defines them in full. Checked 2026-10-13.

## Email authentication and deliverability

| Term | Meaning | Primary source |
|-|-|-|
| SPF | Sender Policy Framework. A TXT record listing the servers allowed to send for the envelope (Return-Path) domain; more than 10 DNS-querying terms returns `permerror`. | https://www.rfc-editor.org/rfc/rfc7208 |
| DKIM | DomainKeys Identified Mail. The sending server signs the message with a private key; the public key sits at `<selector>._domainkey.<domain>`. | https://www.rfc-editor.org/rfc/rfc6376 |
| DMARC | Policy at `_dmarc.<domain>` that passes when SPF or DKIM passes and aligns with the From domain, and tells receivers what to do on failure. RFC 7489 was obsoleted by RFC 9989 in May 2026. | https://www.rfc-editor.org/rfc/rfc9989.html, https://www.rfc-editor.org/rfc/rfc7489 |
| Alignment | The visible From domain matches the domain that passed SPF (Return-Path) or DKIM (`d=`). Relaxed mode accepts the same organizational domain. Google and Yahoo require it for bulk senders. | https://www.rfc-editor.org/rfc/rfc7489#section-3.1 |
| One-click unsubscribe | `List-Unsubscribe` with an HTTPS URL plus `List-Unsubscribe-Post: List-Unsubscribe=One-Click`, so the mailbox provider can unsubscribe the user with one POST. Google and Yahoo ask bulk senders for it and process it within 2 days. | https://www.rfc-editor.org/rfc/rfc8058 |
| MX record | The DNS record naming the servers that accept mail for a domain. A domain with no MX (and no address record to fall back on) cannot receive mail, so validators mark its addresses invalid. | https://www.rfc-editor.org/rfc/rfc5321#section-5 |
| BIMI | Brand Indicators for Message Identification: a DNS record that points to a logo for supporting inboxes to show. It needs DMARC at `p=quarantine` or `p=reject` with `pct=100`; `p=none` is not accepted. Optional for cold email domains. | https://bimigroup.org/implementation-guide/ |
| Spam rate | In Google Postmaster Tools, the percent of DKIM-authenticated mail delivered to engaged recipients' inboxes that those recipients mark as spam. Google asks bulk senders to stay under 0.3% and target under 0.1%. Mail filtered straight to spam is not in the count, so a low rate never proves inbox placement. | https://support.google.com/mail/answer/14668346, https://support.google.com/mail/answer/81126 |
| Hard and soft bounce | A permanent rejection (SMTP reply code 5xx, such as enhanced status 5.1.1 for an unknown mailbox) versus a temporary one (4xx, retried by the sender). Hard-bounced addresses go to the suppression list after one bounce. | https://www.rfc-editor.org/rfc/rfc5321#section-4.2.1, https://www.rfc-editor.org/rfc/rfc3463 |
| Blocklist (DNSBL) | A DNS-queried list of IPs or domains with poor reputation that receiving servers check before accepting mail. Spamhaus DBL lists domains only. | https://www.rfc-editor.org/rfc/rfc5782, https://www.spamhaus.org/blocklists/domain-blocklist/ |
| SNDS | Microsoft Smart Network Data Services: per-IP data on mail sent to Outlook.com, Hotmail and Live addresses, including complaint rates and trap hits, for senders who control the IPs. | https://sendersupport.olc.protection.outlook.com/snds/ |
| Yahoo CFL | Yahoo Complaint Feedback Loop: an ARF report to the enrolled sender each time a Yahoo user marks its mail as spam. Domain-based and requires DKIM signing. | https://senders.yahooinc.com/complaint-feedback-loop/ |
| Catch-all | A domain that accepts mail for any address, so a validator cannot confirm the mailbox exists. Bucket `catch_all`; sent only from a separate, capped campaign. | `references/list-quality-standard.md` section 5 |
| Role address | A mailbox for a function or team, such as `info@`, `sales@` or `support@`. RFC 2142 defines the common names. Flagged `is_role = true`. | https://www.rfc-editor.org/rfc/rfc2142 |
| Seed test | Sending a campaign to a panel of test inboxes across providers to see inbox, promotions or spam placement before and during a campaign. | `email-deliverability` |
| Warmup | A gradual ramp of a new mailbox's daily volume, with a day-by-day schedule, before it carries full campaign traffic. | `inbox-setup` |
| Secondary sending domain | A domain registered for cold email that redirects to the main site, so the main domain's reputation stays out of cold traffic. | `domain-infrastructure` |
| Custom tracking domain | A CNAME the sequencer uses for open and click tracking instead of its shared tracking host. | `domain-infrastructure` |

## Lists and data

| Term | Meaning | Where defined |
|-|-|-|
| ICP | Ideal customer profile: the firmographic, technographic and behavioral filters that describe the accounts most likely to buy, built from the user's best customers. | `icp-list-builder` |
| Firmographics | Company attributes used as filters: industry, headcount, revenue, location, age. | `icp-list-builder`, `scrapercity-lead-database` |
| Technographics | The technologies a company runs, read from its site; in ScraperCity, Tech Stack Search (`scrape_builtwith`) and the store fields in Store Leads. | `ecommerce-by-techstack` |
| Validation status | The bucket each email lands in after validation: `valid`, `catch_all`, `unknown`, `invalid` or `disposable`, each with its own send rule. | `references/list-quality-standard.md` section 5 |
| Suppression list | One list of unsubscribes, bounces, complaints and do-not-contact requests that every tool reads before every send and call block, matched on email, then domain, then business name key. | `references/list-quality-standard.md` section 7 |
| Dedupe key | The fields tried in order to find the same record twice. People: email, LinkedIn URL, name plus company domain, name plus business name key. Companies: domain, then business name key plus state. Local businesses: domain, phone, business name key plus postal code, business name key plus street. | `references/list-quality-standard.md` section 4 |
| Waterfall | Enrichment order from the included-in-plan source to the most expensive per hit, where each step runs only on the gaps the previous step left (Lead Database, then Website Finder, Email Finder, validation, Mobile Finder). | `decision-maker-finder`, `crm-enricher` |
| TAM, SAM, SOM | Total addressable market (every account in the market definition x ACV), serviceable addressable market (accounts the team can serve), serviceable obtainable market (the 12-month share the user commits to, stated as an assumption). Counted bottom-up from accounts. | `tam-builder` |
| PQS | Pain-Qualified Segment. Jordan Crawford's term for prospects identified by a specific, data-detectable problem they have now. | https://www.blueprintgtm.com/ |
| PVP | Permissionless Value Prop. Crawford's term for a message so specific and valuable the prospect would pay to receive it, leading with the data. | https://www.blueprintgtm.com/ |

## Phone

| Term | Meaning | Primary source |
|-|-|-|
| E.164 | The ITU-T international numbering plan format: `+`, country code, national number, 15 digits at most. Every phone in this repo is stored this way. | https://www.itu.int/rec/T-REC-E.164/en |
| STIR/SHAKEN attestation | The originating carrier signs the caller ID with an attestation level: A (it knows the customer and the customer may use the number), B (it knows the customer, not the number) or C (it only passed the call along). | https://www.rfc-editor.org/rfc/rfc8588, https://www.rfc-editor.org/rfc/rfc8224 |
| Line type | Mobile, landline or VoIP, read before a call block because it changes pickup rates and the dial order. | `cold-calling`, `mobile-appender` |
| Spam label | A carrier or handset warning such as "Spam Likely" shown with an incoming call. Pickups drop once a number carries one; `cold-calling` has the fix. | `cold-calling` |
| Connect rate | Connects divided by dials. Conversations per connect and meetings per conversation are tracked as separate rates. | `cold-calling` |

## Program design terms used in this repo

| Term | Meaning | Where defined |
|-|-|-|
| Positive reply rate | Positive replies per 100 delivered emails. Campaigns are judged on it and on meetings booked. | `cold-email-strategy` |
| Cost per meeting | Total program cost for a period (data, inboxes, domains, sequencer, people) divided by meetings, reported per meeting booked and per meeting held. | `outbound-unit-economics` |
| Show rate | Meetings held divided by meetings booked. | `cold-calling`, `outbound-unit-economics` |
| Campaign cell | One segment, one offer and one trigger (or "fit only"). The unit a campaign plan is built, sized and tested in. | `cold-email-strategy` |
| Contact thesis | One sentence per cell on why this buyer will reply now, plus the result that would prove it wrong (for example fewer than 2 positive replies per 100 delivered after 300 sends). | `cold-email-strategy` step 3 |
| Half-life | Days after which a signal's score falls to half its base points: strength = base x 0.5 ^ (age in days / half-life). Each program sets its own half-lives and re-fits them from its conversion data. | `signal-triggered-outbound`, `references/scoring-and-freshness.md` |
| Planning assumption | A benchmark from a dated, sourced study used to size a plan until a pilot measures the user's own rate. | `cold-email-strategy`, `cold-calling` |

## ScraperCity API terms

| Term | Meaning | Where defined |
|-|-|-|
| Start, poll, download | Every scraper run: a POST returns a `runId`, the status call reports `RUNNING` until `SUCCEEDED`, `FAILED` or `CANCELLED`, then the CSV downloads. Apollo runs use a webhook instead of polling. | `references/scrapercity-catalog.md` |
| `check_wallet` | The MCP tool that returns balance, plan and billing date; called before any paid run. | `references/scrapercity-catalog.md` |
| `excludeDelivered` | Database parameter. `true` returns only records this account has never received, for daily or weekly incremental pulls. It flags records new to your account and says nothing about when a business opened. | `references/scrapercity-platform.md` |
| `after` cursor | Database paging: send `after=0`, then each response's `pagination.next_after` until it is null, up to 100 records per request. | `references/scrapercity-platform.md` |

## Sources

- https://www.rfc-editor.org/rfc/rfc7208
- https://www.rfc-editor.org/rfc/rfc6376
- https://www.rfc-editor.org/rfc/rfc7489
- https://www.rfc-editor.org/rfc/rfc9989.html
- https://www.rfc-editor.org/rfc/rfc8058
- https://www.rfc-editor.org/rfc/rfc5321
- https://www.rfc-editor.org/rfc/rfc3463
- https://www.rfc-editor.org/rfc/rfc5782
- https://www.rfc-editor.org/rfc/rfc2142
- https://www.rfc-editor.org/rfc/rfc8224
- https://www.rfc-editor.org/rfc/rfc8588
- https://bimigroup.org/implementation-guide/
- https://support.google.com/mail/answer/14668346
- https://support.google.com/mail/answer/81126
- https://sendersupport.olc.protection.outlook.com/snds/
- https://senders.yahooinc.com/complaint-feedback-loop/
- https://www.spamhaus.org/blocklists/domain-blocklist/
- https://www.itu.int/rec/T-REC-E.164/en
- https://www.blueprintgtm.com/
