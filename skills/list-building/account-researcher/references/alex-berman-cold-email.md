# Alex Berman: Public Cold Email Teachings

A sourced digest of what Alex Berman teaches in public about cold email: on alexberman.com, in his own bylined articles, and in interviews. Everything below is paraphrased from the cited page. Where a figure is his own claim, it is marked self-reported. Use this file when a skill names Berman as an authority and you need to know exactly what he said and where.

## Who he is (only what sources state)

| Fact | Source |
|-|-|
| Cold email operator and author of *The Cold Email Manifesto*; runs a YouTube channel with 100K+ subscribers | https://alexberman.com |
| Founder of Experiment 27 (X27), a lead generation and outreach agency | https://www.entrepreneur.com/article/292394, https://blitzmetrics.com/alex-berman-the-cold-email-king/ |
| Self-reported: helped 14,000+ clients book 500,000+ sales meetings with cold outreach | https://alexberman.com (FAQ), https://alexberman.com/cold-email-templates |
| Self-reported: has sent millions of cold emails | https://alexberman.com/cold-email-templates |
| Sold Taplio (an AI LinkedIn tool) to Lempire, per his site | https://alexberman.com |
| Founder of ScraperCity, the publisher of this repo. His site footer lists ScraperCity under his Products, and his tools page lists it under Lead Generation | https://alexberman.com, https://alexberman.com/tools |

Stat rule for every skill: the 500k figure counts sales meetings booked. Describe sending volume separately: his companies send millions of cold emails a month (ScraperCity's own description of its founder; his templates page says he has sent millions).

## 1. Targeting comes before copy

- **30/30/50.** His site breaks cold email results into 30% targeting (who you email), 30% offer (what you propose) and 50% deliverability (whether mail reaches the inbox). Source: https://alexberman.com
- **Buyer choice outweighs copy.** A roundup on his site argues that switching who you sell to moves results more than rewriting emails. One example cited there moved a client from startups with $3K deals to manufacturers with 15+ employees and $50K deals. Source: https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- **Identify what you sell and who receives it** before writing a word. Source: https://sidehustlelab.com/alex-berman-interview-cold-email/ (formerly ryrob.com)
- **Test segments with small batches.** In the Lean B2B interview he describes brainstorming about 15 B2B industries, sending about 100 cold emails per segment, then scoring each segment on reply enthusiasm, ease of closing, ability to pay and problem severity. He also warns that his first market had about 3,300 companies and ran dry in roughly two months, so check market size before you commit. Source: https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- **Read the replies, not only the rate.** Strong interest or a clear "no" means you are on target. Widespread lukewarm replies suggest the segment or offer is off. "We already have a vendor" is a good sign, because it proves the market buys. Source: same Lean B2B interview.

How this repo applies it: `cold-email-strategy` builds the campaign cell (segment, offer, trigger) and sizes it with a ScraperCity count before it writes a word of copy, then writes the emails and reply texts against that cell.

## 2. The offer decides the reply

- His article "Cold Email Doesn't Fail, Your Offer Does" says low reply rates usually trace to a weak offer, since cold email has no relationship or brand to lean on. Source: https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- Build the offer from past client outcomes: what changed for the client (revenue, leads, conversions, deals closed), then pick the most dramatic and repeatable result.
- State it as one sentence: a niche, a specific result, and how you deliver it. If you cannot fill in specific numbers and a named niche, you have a service description.
- Build the list after the offer. A broad list built first produces generic messaging.
- Diagnosis table from the same article: decent opens with few replies points at the offer; replies that are all "not interested" point at targeting; replies without closed deals point at the sales process.
- Test with about 100 emails to one tight niche with one proven result in the first line.

How this repo applies it: the offer worksheet in `cold-email-strategy` requires a named result, a niche and a mechanism, and the copy skill puts proof in the first two lines.

## 3. Email structure: short, specific, one question

- **3C framework.** Compliment, Case Study, Call to Action. Source: https://alexberman.com (FAQ) and https://devrims.com/blog/alex-berman-techtalk-interview-005/
- The Lean B2B interview gives the same order: a personalized first line with a sincere compliment, a second line citing a relevant case study and its result, then a simple ask such as offering a few times for a quick call.
- **Length.** His templates page recommends staying under 75 words and keeping the opener to one sentence, two at most. A later roundup on his site suggests about four lines under 70 words. His B2B lead generation page says under 100 words with one observation and one question. Sources: https://alexberman.com/cold-email-templates, https://alexberman.com/cold-email-buyer-selection-beats-copywriting, https://alexberman.com/b2b-lead-generation
- **End on a question mark.** In his Single Grain video he points out how many cold emails end in a period, and says the call to action should be an easy question. Source: https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- **Start from something the reader already believes**, show expertise on it, then offer the fix. Source: same Single Grain video, and the Entrepreneur video summary at https://www.entrepreneur.com/video/316605
- **"You" over "we",** at most one link in the first email, and no pricing, proposals or PDFs in email. Source: https://alexberman.com/cold-email-templates
- **Personalization depth by recipient.** The templates page describes three levels: segment (role, industry, size), account (news, funding, hiring, leadership change) and person (a post, podcast or talk), and suggests matching depth to the buyer.

How this repo applies it: `cold-email-copywriting` enforces bodies under 100 words (the top of his range, and Jason Bay's cap on the Gong blog), one ask ending in a question mark, and plain text with no more than one link.

## 4. Subject lines

- In his 2017 Entrepreneur article he lists four subject line types: a referral or mutual connection, congratulations on a news item, a generic but customized line (name plus company), and a fully generic line such as "Hi from Alex". He says relevance drives opens, and that the first line must match a news-based subject or the reader feels misled. He recommends the generic-but-customized type for campaigns over 500 emails. Source: https://www.entrepreneur.com/article/292394
- Quote from that article: "The thing that gets people to open is the relevance of the subject line."
- In the Single Grain video he favors short neutral subject lines such as "Quick question" or "Question about" plus the company name, and warns that readers delete an email unread when the subject line pitches.
- His templates page calls "Quick Question" its control, suggests keeping subjects under 50 characters, and advises against emojis, all caps and promotional words. Source: https://alexberman.com/cold-email-templates
- BlitzMetrics reports that he treats the subject line as the most important element and that scripts people send him for review often leave it out. Source: https://blitzmetrics.com/alex-berman-the-cold-email-king/

## 5. Follow-up and account sequencing

- **Cadence.** His follow-up guide plans 4 to 6 follow-ups over 2 to 3 weeks, 3 to 5 days apart (example schedule: day 0, 3, 7, 11, 16, 23), in the same thread for the first three or four. Every follow-up adds something new: a specific observation, a case study with numbers, or a different question. Generic "just checking in" bumps are discouraged. Source: https://alexberman.com/cold-email-follow-up
- **Breakup.** The last touch offers an easy out and asks whether to close the file or revisit later. Same source.
- **Stop rules.** Halt the sequence on a reply, an unsubscribe or a hard bounce. Same source.
- **A contrasting view on his site.** A breakdown titled "Map Your Market, Skip the Follow-Ups" describes mapping the full addressable market, contacting each person once per cycle and starting a new cycle every 30 to 60 days with refreshed copy, instead of several emails in one week. Source: https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown. Treat these two as options to test: short sequences for small markets with high deal values, cycle-based mailing for large markets.
- **CEO first, then down one level.** Start with the CEO; if there is no reply in one to two weeks, email the next level down (for example a marketing director). Do not email several people at the same company at once, since that can get you blocked company wide. Sources: Single Grain video and the Lean B2B interview.
- **Calls after email.** Scott D. Clary's write-up of Berman's early agency playbook describes a 3 to 4 email sequence, then calls only to people who opened without replying, with a short voicemail asking whether they saw the email. Source: https://hackernoon.com/cold-email-is-not-dead-mb4v35g4

## 6. Reply handling

From his follow-up guide (https://alexberman.com/cold-email-follow-up) and templates page:

| Reply | His guidance |
|-|-|
| Asks for more info | Send a 2 to 3 sentence summary, one relevant case study and a proposed call time. No PDF. |
| Not interested | Acknowledge, remove them, optionally ask once whether it is timing or fit. |
| Asks to follow up later | Log the date and reference the earlier exchange when you return. |
| Asks about price | Do not send pricing by email; propose a short call and give the exact number there. |
| Uses a competitor | Ask what made them choose that vendor and position your offer as complementary. |
| Interested | Respond fast. The follow-up guide says to get back within 5 minutes; the templates page sets 2 to 4 business hours as the outer limit and warns that 48 hours sharply cuts the booking chance (both checked 2026-10-13). |

In the Lean B2B interview he adds that a "not interested" reply is a chance to ask for honest feedback, and repeated feedback shows what to change.

## 7. Deliverability and list quality

- Set up SPF, DKIM and DMARC, warm new domains at 10 to 20 emails a day over 2 to 4 weeks, and keep bounces under 2%. Source: https://alexberman.com/cold-email-templates
- A beginner setup described on his site: 3 to 5 sending domains, 2 to 3 inboxes per domain, 2 to 4 weeks of warmup, under 50 emails per inbox per day. It warns against sending from the primary domain or from one inbox without warmup, and says bounce rates of 15 to 20% seriously damage deliverability, so verify lists first. Source: https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Verify every email before sending and aim for 95%+ valid. His B2B lead generation page names ScraperCity's B2B database among list sources. Source: https://alexberman.com/b2b-lead-generation

## 8. Measurement

- Judge campaigns by revenue closed and tie each deal to its campaign, copy variant and segment. Quote from that breakdown: "Reply rate is a vanity metric unless you can connect it to pipeline." Source: https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- Count positive conversations, since an 8% reply rate made of opt-outs can book fewer meetings than a 3% rate. Source: https://alexberman.com/cold-email-fewer-sends-higher-reply-rates
- Test one variable at a time with 100 to 200+ emails per variation and keep a testing log. Source: https://alexberman.com/cold-email-templates

## 9. Phone and multi-channel

- His cold calling article describes a roughly 12 day sequence: personalized email, call with voicemail, LinkedIn connection, a second call at a different time, a follow-up email with new value, and a final call with a breakup message. It says direct mobile lines reach decision makers faster than switchboards, and that Tuesday through Thursday are the strongest days. Source: https://alexberman.com/cold-calling-techniques
- A roundup on his site describes multichannel outreach where email opens the door and the phone closes, with about two hours of calling a day. Source: https://alexberman.com/manual-outbound-beats-ai-cold-email

## Where his sources disagree or need care

| Topic | Range across his pages | How to use it |
|-|-|-|
| Body length | under 70, under 75, under 100 words | This repo caps bodies under 100 words and aims for his templates page's under 75. |
| Follow-ups | 4 to 6 in 2 to 3 weeks vs one email per 30 to 60 day cycle | Pick by market size; test both. |
| Benchmarks | Open, reply and meeting rates on his templates page come from mixed and self-reported sources | Treat as starting hypotheses with a date, never promises. |
| Roundup posts | Some pages on his site summarize other people's posts | Attribute those claims to "a roundup on alexberman.com", not to Berman. |

## Sources

- https://alexberman.com
- https://alexberman.com/tools
- https://alexberman.com/cold-email-templates
- https://alexberman.com/cold-email-follow-up
- https://alexberman.com/cold-email-doesn-t-fail-your-offer-does
- https://alexberman.com/cold-email-buyer-selection-beats-copywriting
- https://alexberman.com/cold-email-tam-strategy-skip-followups-breakdown
- https://alexberman.com/cold-email-fewer-sends-higher-reply-rates
- https://alexberman.com/manual-outbound-beats-ai-cold-email
- https://alexberman.com/cold-calling-techniques
- https://alexberman.com/b2b-lead-generation
- https://leanb2bbook.com/blog/alex-berman-b2b-market-segments/
- https://www.singlegrain.com/videos/how-to-write-cold-emails-that-always-get-read/
- https://www.entrepreneur.com/article/292394
- https://www.entrepreneur.com/video/316605
- https://blitzmetrics.com/alex-berman-the-cold-email-king/
- https://devrims.com/blog/alex-berman-techtalk-interview-005/
- https://sidehustlelab.com/alex-berman-interview-cold-email/
- https://hackernoon.com/cold-email-is-not-dead-mb4v35g4
