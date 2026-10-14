# Syntax Repair and Role Rules

How to repair malformed addresses before validation, which repairs are safe, how to build the dedupe key, and how to flag role, network-operations and free-provider addresses. Everything here runs locally before `validate_emails`, so none of it costs money. Every change is logged in `fix_applied` so a reviewer can undo it.

## 1. Repair order

Run the steps in this order. Each step works on the output of the one before.

| # | Step | Example in | Example out | Safe to automate? |
|-|-|-|-|-|
| 1 | Decode the file as UTF-8; re-read as Windows-1252 if bytes fail | `JosÃ©@` | `José@` (then flagged at step 11) | Yes |
| 2 | Trim whitespace, tabs, line breaks | `  dana@acme.example ` | `dana@acme.example` | Yes |
| 3 | Remove zero-width and non-breaking spaces (U+200B, U+200C, U+200D, U+FEFF, U+00A0) | `dana@acme.example` with a hidden U+200B | `dana@acme.example` | Yes |
| 4 | Strip `mailto:` and URL query strings | `mailto:dana@acme.example?subject=Hi` | `dana@acme.example` | Yes |
| 5 | Pull the address out of a display name | `"Dana Ruiz" <dana@acme.example>` | `dana@acme.example` | Yes |
| 6 | Split multi-address cells on `;` `,` `/` or whitespace | `a@x.example; b@x.example` | two rows | Yes, copy every other column to both rows |
| 7 | Strip surrounding quotes, brackets and trailing punctuation | `(dana@acme.example).` | `dana@acme.example` | Yes |
| 8 | Replace obfuscation | `dana [at] acme [dot] example` | `dana@acme.example` | Yes, only for the exact `[at]` and `[dot]` forms |
| 9 | Lowercase the domain part | `dana@ACME.example` | `dana@acme.example` | Yes |
| 10 | Fix known consumer-domain typos (section 3) | `sam@gmial.com` | `sam@gmail.com` | Yes, only from the map |
| 11 | Check the structure rules (section 2); failures go to `removed.csv` with reason `syntax` | `dana@@acme.example` | removed | Yes |
| 12 | Build `email_key` for dedupe (section 4) | `Dana.Ruiz+events@Gmail.com` | `danaruiz@gmail.com` | Yes |

Never auto-fix a corporate domain. `acme.co` may be the company's own domain, and `acme-inc.com` may be a second brand. When a corporate domain looks wrong, leave it and let the validator answer.

## 2. Structure rules

An address passes local syntax when all of these hold. They follow RFC 5321 and RFC 5322 for the forms that show up on B2B lists; quoted local parts and IP-literal domains are legal but never appear on a prospect list, so this skill removes them.

| Rule | Limit | Source |
|-|-|-|
| Exactly one `@` | | RFC 5322 addr-spec |
| Local part length | 1 to 64 octets | RFC 5321 section 4.5.3.1.1 |
| Domain length | 255 octets maximum, each label 63 maximum | RFC 5321 section 4.5.3.1.2, RFC 1035 |
| Whole address | 254 characters maximum in practice | RFC 5321 path limit of 256 including the angle brackets |
| Local part characters | Letters, digits, dots and the RFC 5322 atext symbols (the character class in the pattern below) | RFC 5322 dot-atom |
| Dots in the local part | Only between other characters, one at a time | RFC 5322 dot-atom |
| Domain | At least one dot, labels of letters, digits and hyphens, no label starting or ending with a hyphen, a top-level label with at least one letter | RFC 1035, RFC 5321 |
| No spaces anywhere | | RFC 5322 |

Practical pattern for the check (after the repairs above):

```text
^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$
```

Apply it to the lowercased address. Pair it with the length checks; a regex alone does not enforce the 64-octet local part.

### Non-ASCII addresses

| Case | Action |
|-|-|
| Non-ASCII domain (`müller.example`) | Convert the domain to its ASCII punycode form for validation and keep the original in `email_raw` |
| Non-ASCII local part (`josé@acme.example`) | Valid under RFC 6531 (SMTPUTF8), but many sending tools reject it. Route to `role_review.csv` with note `utf8_local_part` |
| Mojibake (`JosÃ©`) | Fix the file encoding first (step 1); if it persists, remove with reason `syntax` |

## 3. Consumer-domain typo map

Fix only these domains, only when the full domain matches exactly. Every fix writes `fix_applied = typo:<from>-><to>`.

| Typo | Fix |
|-|-|
| gmial.com, gmal.com, gmaill.com, gamil.com, gnail.com, gmail.co, gmail.cm, gmail.con, gmail.om, gmai.com | gmail.com |
| hotmial.com, hotmal.com, hotmai.com, hotmail.co, hotmail.con, homail.com | hotmail.com |
| yaho.com, yahooo.com, yahoo.co, yahoo.con, yhoo.com | yahoo.com |
| outlok.com, outllok.com, outlook.co, outlook.con | outlook.com |
| iclod.com, icloud.co, icoud.com | icloud.com |
| aol.co, aol.con | aol.com |
| comcast.com | comcast.net (only when the source is a US consumer sign-up) |

Do not fix `.co` to `.com` on any other domain. `.co` is a live country-code domain used by many companies.

## 4. Dedupe key

| Address type | `email_key` rule | Example |
|-|-|-|
| Consumer Gmail (`gmail.com`, `googlemail.com`) | Lowercase; drop every dot in the local part; drop `+` and everything after it; map `googlemail.com` to `gmail.com` | `Dana.Ruiz+events@Googlemail.com` to `danaruiz@gmail.com` |
| Every other domain | Lowercase the full address; keep dots and `+tags` | `Dana.Ruiz+events@Acme.example` to `dana.ruiz+events@acme.example` |

Google documents that dots do not change delivery for Gmail addresses. Corporate servers (including Google Workspace domains) may treat dots and tags as meaningful, so the collapse applies only to the two consumer domains. Send to the address as the person gave it; the key is only for matching.

When two rows share a key, keep one using `references/list-quality-standard.md` section 4b (valid status first, then non-empty fields, then source precedence, then newest), and log the dropped row in `removed.csv` with reason `duplicate` and `duplicate_of` set to the kept row's id.

## 5. Role and network-operations addresses

RFC 2142 (May 1997) defines standard mailbox names in three groups. This skill treats them differently.

| Group | Local parts | Action on every list type |
|-|-|-|
| Network operations | abuse, noc, security | Remove before validation, reason `network_role`, add to the blocklist. These mailboxes reach the people who file spam reports. |
| Support services | postmaster, hostmaster, usenet, news, webmaster, www, uucp, ftp | Remove postmaster and hostmaster with reason `network_role`; flag the rest `is_role = true` |
| Business | info, marketing, sales, support | Flag `is_role = true` |

Extended role list (not in RFC 2142, common on B2B lists): admin, office, contact, hello, team, help, billing, accounts, accounting, ar, ap, invoices, careers, jobs, hr, recruiting, press, media, pr, legal, compliance, privacy, orders, enquiries, inquiries, reception, frontdesk, appointments, bookings, reservations, service, customerservice, noreply, no-reply, donotreply, mailer-daemon, newsletter, events, partners, founders.

Never send to `noreply`, `no-reply`, `donotreply` or `mailer-daemon`: remove with reason `syntax` (they are not mailboxes a person reads).

### Role policy by list type

| List type | `is_role = true` rows | Why |
|-|-|-|
| Named B2B contacts (cold email) | `role_review.csv` | A named list should reach the named person, not a shared inbox |
| Local businesses (dentists, roofers) | Keep in the main flow | The owner often reads `info@` or `office@` |
| Ecommerce stores | Keep in the main flow | `hello@` and `support@` are often the only published address |
| Newsletter to opted-in subscribers | Keep | The subscriber asked for the mail |
| CRM import | Keep with the flag | Status is information, not a send decision |
| Ads audience upload | Exclude | No person behind the address |

## 6. Free-provider addresses

Set `is_free = true` when the domain is on this list or the validator's `free` column is true. The validator column wins when they disagree.

gmail.com, googlemail.com, yahoo.com, ymail.com, rocketmail.com, outlook.com, hotmail.com, live.com, msn.com, aol.com, icloud.com, me.com, mac.com, proton.me, protonmail.com, gmx.com, gmx.de, web.de, mail.com, zoho.com, yandex.com, yandex.ru, qq.com, 163.com, 126.com, comcast.net, att.net, sbcglobal.net, verizon.net, cox.net, charter.net, btinternet.com, sky.com, orange.fr, free.fr, libero.it.

| List type | `is_free = true` | Rule |
|-|-|-|
| Named B2B, the row has a company domain that differs | `role_review.csv` with note `personal_address` | A personal inbox, not the business address the list targets; the user decides whether to use it |
| Named B2B, sole proprietor or no company domain | Keep | The business runs on that address |
| Local business list | Keep | Many small businesses publish a Gmail address |
| Ecommerce stores | Keep | Same |

## 7. Disposable addresses

The validator returns `disposable` for temporary inbox providers. A local pre-filter saves the validation charge for the obvious ones: mailinator.com, guerrillamail.com, 10minutemail.com, temp-mail.org, yopmail.com, trashmail.com, sharklasers.com, getnada.com, dispostable.com. Remove matches with reason `disposable` and add them to the blocklist. Disposable rows clustered in one source mark it as a sign-up or giveaway form; treat its rows as tier C.

## 8. Reason codes for removed.csv

| Code | Meaning |
|-|-|
| `no_email` | Blank email cell |
| `syntax` | Failed section 2 after repair, or a no-reply mailbox |
| `duplicate` | Same `email_key` as a kept row |
| `unsubscribed`, `bounced`, `complained` | Matched a sequencer suppression export |
| `customer`, `open_opportunity`, `competitor`, `do_not_contact` | Matched a CRM or user-maintained domain list |
| `network_role` | abuse, noc, security, postmaster, hostmaster |
| `invalid`, `disposable` | Validator result |
| `unknown_twice` | Still `unknown` after the one retry on a tier C list |

## Sources

- RFC 5321, Simple Mail Transfer Protocol: https://datatracker.ietf.org/doc/html/rfc5321
- RFC 5322, Internet Message Format: https://datatracker.ietf.org/doc/html/rfc5322
- RFC 1035, Domain names, implementation and specification: https://datatracker.ietf.org/doc/html/rfc1035
- RFC 6531, SMTP extension for internationalized email: https://datatracker.ietf.org/doc/html/rfc6531
- RFC 2142, Mailbox names for common services, roles and functions: https://datatracker.ietf.org/doc/rfc2142/
- Google, Dots do not matter in Gmail addresses: https://support.google.com/mail/answer/7436150
- ScraperCity, Email Validator: https://scrapercity.com/email-validator
- Unicode, Format characters (zero-width space U+200B): https://www.unicode.org/charts/PDF/U2000.pdf
