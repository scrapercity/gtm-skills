# Mailbox Setup Runbook

Per-mailbox setup, in order, for Google Workspace and Microsoft 365 mailboxes that will send cold email through a sequencer. Click paths were current on 2026-10-12; admin consoles move menus often, so search the console for the setting name if a path has changed.

## 1. Sender identity

| Rule | Why | Source |
|-|-|-|
| Every mailbox belongs to a real employee or contractor who agreed in writing to send under their name | CAN-SPAM requires From, Reply-To and routing information that identifies the person or business who sent the message | FTC CAN-SPAM compliance guide |
| The person can answer a reply in their own words or hands it to a named teammate | Replies are the point of cold email | House standard |
| One person may own mailboxes on several domains | Spreads volume without inventing people | House standard |
| A person who leaves the company: mailboxes paused the same day, replies routed to their manager, mailboxes renamed only after 30 days of no sends | Avoids sending under the name of someone who no longer works there | House standard |
| Never use a name or photo of someone who did not agree | Misleading header information; also a right-of-publicity problem | FTC; local law |

Ownership ratio: up to 9 mailboxes per person (3 domains x 3 formats) is workable when a sequencer's unified inbox gathers replies. More than that and the person cannot keep up with replies on a good day.

## 2. Address and display name

Address formats, rotated so no domain has two mailboxes with the same local part pattern for one person:

| Format | Example | Use |
|-|-|-|
| `first@` | `dana@getacme.com` | First choice |
| `first.last@` | `dana.ortiz@tryacme.com` | Second |
| `firstl@` | `danao@acmehq.com` | Third |
| `first_last@` | `dana_ortiz@meetacme.com` | Fourth |

Avoid: `sales@`, `info@`, `outreach@`, `team@`, numbered addresses (`dana2@`). Role-looking senders read as bulk mail.

Display name: `Dana Ortiz`. Not `Dana from Acme`, not `Dana Ortiz | Acme`, not `Acme Sales`. Set it in the Workspace user profile (Admin console > Directory > Users > user > User information) or Microsoft 365 (Admin center > Users > Active users > user > Display name), and again in the sequencer's sender name field if it has one.

## 3. Signature

Plain text. The sequencer usually holds the signature (Instantly, Smartlead, Lemlist and others let you set a per-account signature); set it there, and match it in Gmail or Outlook for manual replies.

Template (US commercial email):

```text
Dana Ortiz
Head of Partnerships, Acme
1200 Main St, Suite 400, Austin, TX 78701
Not the right person? Reply "no thanks" and I won't follow up.
```

| Element | Rule | Source |
|-|-|-|
| Name and title | Real, matching LinkedIn | House standard |
| Company | Brand name as on the main site | House standard |
| Postal address | Valid street address, registered PO box or private mailbox; required in commercial email | FTC CAN-SPAM |
| Opt-out line | Clear way to stop further mail; honor within 10 business days by law, 24 hours by house standard | FTC CAN-SPAM; `references/deliverability-primer.md` |
| Links | Zero in step 1 if link tracking is on; otherwise at most one plain link to the main site | House standard |
| Images, logos, social icons | None | Images add load and spam signals; plain text matches person-to-person mail |
| Legal disclaimers | Only if counsel requires them | Long footers read as bulk mail |

Canada (CASL), the EU and UK (GDPR, PECR) add identification and consent rules. Open `references/outbound-compliance-primer.md` before sending to those countries.

## 4. Profile photo and account security

| Step | Google Workspace | Microsoft 365 |
|-|-|-|
| Photo | User signs in > Google Account > Personal info > Profile picture, or admin uploads in Directory > Users | Admin center > Users > Active users > user > Change photo |
| 2-Step Verification | Admin console > Security > Authentication > 2-Step Verification, enforce for the cold email organizational unit | Entra admin center > Security defaults or Conditional Access MFA |
| Recovery email | An ops-controlled address on the main domain, never a rep's personal Gmail | Same |
| Password | Unique, stored in the team password manager | Same |
| Sequencer connection | OAuth "Sign in with Google" in the sequencer | OAuth "Sign in with Microsoft"; if a tool needs SMTP AUTH, enable it per mailbox (Admin center > user > Mail > Manage email apps > Authenticated SMTP) |
| Organizational unit | Put cold mailboxes in their own OU so policies differ from staff mailboxes | Use a separate tenant or a separate group with its own outbound policy |

Photo: a real headshot of the owner. Gmail shows the Google account photo to recipients in many views; Outlook shows the Microsoft 365 photo to recipients in the same organization and sometimes outside it.

## 5. Reply routing options

| Option | How | Pros | Cons | Pick when |
|-|-|-|-|-|
| A. Unified inbox only | Replies land in the sending mailbox; the sequencer's unified inbox shows all mailboxes | Sequencer sees every reply and stops sequences; labels sync to webhooks | Rep must open the sequencer | Default |
| B. Unified inbox plus forwarding copies | Gmail filter on the sending mailbox: from `-me`, has words `Re:` or a sequencer label, forward to the rep's main-domain address | Rep sees replies in their normal inbox | Forwarded mail carries the cold domain into the main tenant; answering from the main inbox breaks the thread | Rep refuses to use a second tool |
| C. Reply-To on the main domain | Reply-To header set to `dana@acme.com` | Replies arrive in the main inbox | Every cold email names the main domain in headers; sequencer may miss replies | Not recommended |
| D. Delegation | Rep added as a delegate to each sending mailbox | Rep answers from the right address in Gmail | Many mailboxes to switch between | Small teams with 3 to 6 mailboxes |

Google Workspace forwarding needs the admin to allow automatic forwarding (Admin console > Apps > Google Workspace > Gmail > End User Access > Automatic forwarding). Auto-forwarded messages do not count toward the 2,000 a day sending limit, and each account can hold up to 40 forwarding filters.

Answer from the sending mailbox. A reply from a different address than the prospect wrote to looks odd and splits the thread.

## 6. Mailbox setup checklist (one row per mailbox)

- [ ] Owner named, consent recorded
- [ ] Address format assigned, display name set
- [ ] Photo uploaded
- [ ] 2-Step Verification on, recovery email set, password stored
- [ ] Placed in the cold email OU or group
- [ ] Header test passed (SPF, DKIM, DMARC pass) from `domain-infrastructure`
- [ ] Connected to the sequencer by OAuth
- [ ] Signature set in the sequencer and the mail client
- [ ] Tracking domain set (if tracking is on)
- [ ] Warmup on with the settings in `warmup-and-ramp.md`
- [ ] Daily campaign limit 0, first cold send date written in the roster
- [ ] Reply routing option chosen and tested with a reply from an outside address
- [ ] Added to a rotation group

## 7. Reply monitoring

| Item | House standard |
|-|-|
| Owner | One named person per rotation group, with a backup |
| Check times | At least 10:00 and 15:00 recipient-local on sending days |
| Positive reply SLA | Human answer within 4 business hours |
| Out-of-office | Sequencer pauses and resumes after the return date if it supports it |
| Unsubscribe or "remove me" | Added to the workspace blocklist the same day |
| Angry reply or legal threat | Blocklist, apologize once, escalate to the ops lead |
| Wrong person with a referral | Thank, ask permission, start a new thread to the referral |

Hand categories and templates to `reply-handling`.

## Sources

- FTC, CAN-SPAM Act: A Compliance Guide for Business: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- Google Workspace, Gmail sending limits (auto-forward counts and filter limits): https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace
- Google Workspace, Set up DKIM: https://knowledge.workspace.google.com/admin/security/set-up-dkim
- Microsoft, Exchange Online limits: https://learn.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- Instantly, Account and campaign limits: https://help.instantly.ai/en/articles/6248612-account-and-campaign-limits
- Alex Berman, custom tracking domains and Gmail: https://alexberman.com/custom-tracking-domain-gmail
