# Mailbox Setup Runbook

Per-mailbox setup, in order, for Google Workspace and Microsoft 365 mailboxes that will send cold email through a sequencer. Click paths were current on 2026-10-12; admin consoles move menus often, so search the console for the setting name if a path has changed.

## 1. Sender identity

| Rule | Why |
|-|-|
| Every mailbox has a named owner on the team who reads its replies, or hands them to a named teammate | Unread replies are lost meetings |
| One person may own mailboxes on several domains | Spreads volume across domains |
| A person who leaves the company: mailboxes paused the same day, replies routed to their manager | Replies keep an owner |

How many mailboxes one person can own is set by how fast they answer replies in the sequencer's unified inbox; measure reply wait time and move mailboxes when it grows.

## 2. Address and display name

Address formats, rotated so no domain has two mailboxes with the same local part pattern for one person:

| Format | Example | Use |
|-|-|-|
| `first@` | `dana@getacme.com` | First choice |
| `first.last@` | `dana.ortiz@tryacme.com` | Second |
| `firstl@` | `danao@acmehq.com` | Third |
| `first_last@` | `dana_ortiz@meetacme.com` | Fourth |

Display name: the owner's name, `Dana Ortiz`. Set it in the Workspace user profile (Admin console > Directory > Users > user > User information) or Microsoft 365 (Admin center > Users > Active users > user > Display name), and again in the sequencer's sender name field if it has one.

## 3. Signature

Plain text. The sequencer usually holds the signature (Instantly, Smartlead, Lemlist and others let you set a per-account signature); set it there, and match it in Gmail or Outlook for manual replies.

Template:

```text
Dana Ortiz
Head of Partnerships, Acme
Not the right person? Reply "no thanks" and I won't follow up.
```

| Element | Rule | Source |
|-|-|-|
| Name, title, company | The owner's own name and title, the brand name as on the main site | |
| Opt-out line | Clear way to stop further mail, honored the same day, inside Yahoo's 2-day and Google's 48-hour unsubscribe processing; complaints count toward Google's 0.3% spam-rate ceiling | Google and Yahoo sender requirements (`references/deliverability-primer.md`) |
| Links | None in step 1 if link tracking is on; otherwise at most one plain link to the main site | Click tracking wraps every link in a redirect (Alex Berman, May 2026) |

## 4. Profile photo and account security

| Step | Google Workspace | Microsoft 365 |
|-|-|-|
| Photo | User signs in > Google Account > Personal info > Profile picture, or admin uploads in Directory > Users | Admin center > Users > Active users > user > Change photo |
| 2-Step Verification | Admin console > Security > Authentication > 2-Step Verification, enforce for the cold email organizational unit | Entra admin center > Security defaults or Conditional Access MFA |
| Recovery email | An ops-controlled address on the main domain, never a rep's personal Gmail | Same |
| Password | Unique, stored in the team password manager | Same |
| Sequencer connection | OAuth "Sign in with Google" in the sequencer; no app passwords needed | OAuth "Sign in with Microsoft". Basic auth for SMTP AUTH is unchanged through December 2026, then off by default for existing tenants and unavailable for tenants created after December 2026 (Message Center MC786329). Enable SMTP AUTH per mailbox only for a tool that cannot use OAuth (Admin center > user > Mail > Manage email apps > Authenticated SMTP) |
| Organizational unit or policy | Put cold mailboxes in their own OU so policies differ from staff mailboxes | Separate tenant from staff mail, plus an outbound spam policy for the cold mailboxes: 20 external recipients an hour (the top of Apollo's 10 to 20), 50 a day (Alex Berman's per-inbox ceiling), restrict until the following day, automatic forwarding Off (Defender portal > Anti-spam > Create policy > Outbound) |
| Tenant quota | Not applicable | Before each ramp step, mailboxes in the tenant x (cold cap + warmup) stays under the tenant's external recipient quota at its age (`warmup-and-ramp.md` section 2) |

Photo: the owner's own headshot, if the team uses one.

## 4a. DNS records and Postmaster Tools

The deliverable lists every record with its exact value. Values checked on 2026-10-13 on the provider pages in Sources.

| Record | Google Workspace | Microsoft 365 |
|-|-|-|
| MX | `smtp.google.com`, priority 1 | The value shown in Admin center > Settings > Domains > DNS records |
| SPF (TXT on @) | `v=spf1 include:_spf.google.com ~all` | `v=spf1 include:spf.protection.outlook.com -all` |
| DKIM | TXT at `google._domainkey` (default selector `google`), 2048-bit; the key appears 24 to 72 hours after Gmail is turned on (Admin console > Apps > Google Workspace > Gmail > Authenticate email) | CNAMEs `selector1._domainkey` and `selector2._domainkey`, targets copied from Defender > Email authentication settings > DKIM |
| DMARC (TXT on `_dmarc`) | Start at `v=DMARC1; p=none; rua=mailto:<report address>` (Google's set-up page starts at `p=none`) | Same |

Postmaster Tools: add each sending domain at postmaster.google.com, publish the TXT or CNAME record it shows, then click Verify. It shows no data until the domain is verified, and data can be missing on low-volume days. Schedule this as a dated step whenever the spam rate is a gate.

## 5. Reply routing options

| Option | How | Pros | Cons | Pick when |
|-|-|-|-|-|
| A. Unified inbox only | Replies arrive in the sending mailbox; the sequencer's unified inbox shows all mailboxes | Sequencer sees every reply and stops sequences; labels sync to webhooks | Rep must open the sequencer | Default |
| B. Unified inbox plus forwarding copies | Gmail filter on the sending mailbox: from `-me`, has words `Re:` or a sequencer label, forward to the rep's main-domain address | Rep sees replies in their normal inbox | Forwarded mail carries the cold domain into the main tenant; answering from the main inbox breaks the thread | Rep refuses to use a second tool |
| C. Reply-To on the main domain | Reply-To header set to `dana@acme.com` | Replies arrive in the main inbox | Every cold email names the main domain in headers; the sequencer never sees those replies, so stop-on-reply fails | Not used |
| D. Delegation | Rep added as a delegate to each sending mailbox | Rep answers from the right address in Gmail | Many mailboxes to switch between | Small teams with few mailboxes |

Google Workspace forwarding needs the admin to allow automatic forwarding (Admin console > Apps > Google Workspace > Gmail > End User Access > Automatic forwarding). Auto-forwarded messages do not count toward the 2,000 a day sending limit, and each account can hold up to 40 forwarding filters.

Answer from the sending mailbox. A reply from a different address than the prospect wrote to looks odd and splits the thread.

## 6. Mailbox setup checklist (one row per mailbox)

- [ ] Owner named
- [ ] Address format assigned, display name set
- [ ] Photo uploaded
- [ ] 2-Step Verification on, recovery email set, password stored
- [ ] Placed in the cold email OU or group
- [ ] Header test passed (SPF, DKIM, DMARC pass) from `domain-infrastructure`
- [ ] Connected to the sequencer by OAuth
- [ ] Microsoft only: in the cold outbound spam policy; tenant quota checked for this ramp step
- [ ] Signature set in the sequencer and the mail client
- [ ] Tracking domain set (if tracking is on), with the sequencer's documented host: Instantly CNAME `inst` to `prox.itrackly.com`, DNS-only
- [ ] Warmup on with the settings in `warmup-and-ramp.md`
- [ ] Daily campaign limit 0, first cold send date written in the roster
- [ ] Reply routing option chosen and tested with a reply from an outside address
- [ ] Added to a rotation group

## 7. Reply monitoring

| Item | Setting |
|-|-|
| Owner | One named person per rotation group, with a backup |
| Check times | Set by the team; write them in the roster |
| Positive reply response time | A target the team sets, measured from the reply's timestamp to the first human answer |
| Out-of-office | Sequencer pauses and resumes after the return date if it supports it |
| Unsubscribe, "remove me" or a hostile reply | Added to the workspace blocklist the same day, across every tool |
| Wrong person with a referral | Start a new thread to the referral |

Hand categories and templates to `reply-handling`.

## 8. Mailboxes bought from a reseller

When a vendor provisions the mailboxes in its own Google Workspace or Microsoft 365 account, some roster settings are yours and some are not. Get the answers below in writing before the roster is final.

| Setting | Usually yours | Usually the vendor's | Ask |
|-|-|-|-|
| Display name, signature, sequencer warmup and caps | Yes | | |
| Address format and the person behind it | Yes, when you order | | Can addresses be renamed after delivery? |
| Profile photo | Sometimes, by signing in to the mailbox | Admin upload | Can we sign in to each mailbox directly? |
| 2-Step Verification, recovery email, password | | Admin account | Who can reset the password, and who is notified? |
| DKIM key, outbound policy, tenant quota | | Yes | Which tenant holds us, and how many other customers share it? |
| Reply export when you leave | | Yes | Can we export every mailbox's mail on cancellation? |

Export replies from the sequencer before any cancellation, keep the domains in your own registrar account, and run resold mailboxes on the same caps and ramp as your own. Warmup dates start when the mailbox passes its header test, never from the order date.

## Sources

- Google Workspace, Gmail sending limits (auto-forward counts and filter limits): https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace
- Google Workspace, Set up DKIM (selector `google`, 2048-bit, 24 to 72 hours after Gmail is on): https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Google Workspace, Set up MX records (`smtp.google.com`, priority 1; checked 2026-10-13): https://knowledge.workspace.google.com/admin/domains/set-up-mx-records-for-google-workspace
- Google Workspace, Set up SPF (`v=spf1 include:_spf.google.com ~all`; checked 2026-10-13): https://knowledge.workspace.google.com/admin/security/set-up-spf
- Google Workspace, Set up DMARC (start at `p=none` with a `rua` address; checked 2026-10-13): https://knowledge.workspace.google.com/admin/security/set-up-dmarc
- Google, Set up Postmaster Tools (verify by TXT or CNAME; checked 2026-10-13): https://support.google.com/a/answer/9981691
- Microsoft, Set up SPF for Microsoft 365 (checked 2026-10-13): https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure
- Microsoft, Set up DKIM for Microsoft 365 (selector1 and selector2 CNAMEs; checked 2026-10-13): https://learn.microsoft.com/en-us/defender-office-365/email-authentication-dkim-configure
- Microsoft, Exchange Online limits: https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- Instantly, Account and campaign limits: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Alex Berman, custom tracking domains and Gmail (May 11, 2026): https://alexberman.com/custom-tracking-domain-gmail
- Apollo, Email sending limits (10 to 20 an hour): https://knowledge.apollo.io/hc/en-us/articles/4409233349005-Email-Sending-Limits
- Alex Berman, TAM strategy breakdown (under 50 a day per inbox): https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Instantly, Custom tracking domain (host `inst`, checked 2026-10-13): https://help.instantly.ai/en/articles/6984188-custom-tracking-domain
- Microsoft 365 Message Center MC786329, Basic auth for SMTP AUTH (mirror, checked 2026-10-13): https://mc.merill.net/message/MC786329
- Microsoft, Configure outbound spam policies (checked 2026-10-13): https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-policies-configure
