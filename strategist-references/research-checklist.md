# SKYHOUSE RESEARCH BRIEF — THE PROCESS

Research only. What happens after (creative briefs, testing) lives in its own doc.
(Approved by Ryan 2026-08-03. Source: the Aug 3 leadership call + Ryan's direct edits. Presentation: the "SkyHouse Research Brief" artifact / v1 PDF.)
(LIVING DOC — this is the canonical rules list. Process changes land here first, dated inline. Operator layer: `.claude/skills/strategist-research-brief/SKILL.md`. Last reconciled with the Aug 10 call: 2026-08-11.)

## STEP 1 — GET EVERY ASSET FROM THE CLIENT

1. The VSL, all pages, all links.
2. Every angle they already tested and how it did.
3. Their ad account. The breakdown lives in this research process (moved from Matt — Jason, Aug 10 call): what worked, what died, CPCs, CPMs.
4. Call center logs and support tickets.
5. Any research they already have.

## STEP 2 — BREAK DOWN THE OFFER

6. Watch the VSL yourself first, like a stranger. Write your gut take before AI tells you anything.
7. Then have AI break it down into the offer brief: what the product is, what it costs, how it works.
8. And the buyer brief: who buys it, what hurts, what they say, what they already tried, what stops them from buying.
9. Name the biggest pain and the biggest buyer. Everything aims at that.

## STEP 3 — READ REAL PEOPLE

10. Scrape Amazon, Trustpilot, and BBB. The brand AND the competitors.
11. From Amazon also grab: who the competitors are, and what else people search.
12. Reddit: search the pain, not the product. Pull the insights that actually help us write ads. Scrape it, don't scroll it.
13. Scrape the X accounts we follow.
14. Pull the exact words people use. Count how often each pain repeats. If tons of people say the same thing, it goes big in the copy.
15. Competitor complaints are gold. That's where the unique mechanism hides.
16. A quote only stays if it gives us an ad, a hook, or an objection to answer.
17. Two quotes are not a fact. A pattern has to repeat before we act on it.

## STEP 4 — SEE WHAT PEOPLE GOOGLE

18. Pull search terms, short and long tail. Write hooks in their words.

## STEP 5 — SPY ON THE ADS

19. Give the AI the VSL and the Atria API key. It finds every competitor and everything scaling for this offer right now.
20. It breaks the whole market down: best concepts, best angles, what's tested the most, what's been running the longest.
21. Look at the brand's own ads first: what they scaled, what they killed.
22. Check where every ad sends people. ONLY learn from ads that go to the same kind of page as ours. An ad built to sell on a product page is playing a different game than an ad built to get a VSL view.

## STEP 6 — THE RESEARCH BRIEF (one doc per offer)

23. Everything above goes into one brief.
24. The most common avatars.
25. Keep outcomes, concepts, and angles separate. Three different things.
26. Show patterns AND gaps: what's proven, and what nobody has tried.
27. Every line says why it matters. No why, no line.
28. Use our own data too, not just competitors.
29. It ends with the list of angles we're going to test, ranked: safe bets, medium plays, big swings. INTERNAL ONLY. The client never sees it.
30. Save every raw pull (reviews, ads, comments) in one folder we can search later. The brief points to it, so nothing lives only in the doc.
31. The finished brief hands off to the creative brief. Everything after that is the testing process, its own doc.

## STEP 7 — RESEARCH NEVER STOPS

32. Day one is the big dig. After that, spying IS research. Same job.
33. Every week or two a report comes TO us: what's new, what's scaling, what died. Nobody sits in Atria clicking around.
34. Later, a daily email version. The scraper becomes more than a scraper (Sam and Apollo build that).
35. New strategists live in research for their first 90 days and iterate winners while they learn.

## STEP 8 — WRITING RULES (added 2026-08-11, from the Akka v2 run)

36. Report, don't prescribe. A research doc states the fact, the count, and why it is worth attention. Never "ads should" or "copy must." Directives come from Ryan only. If a finding sparks an idea, write it as a question for Ryan.
37. Plain language. 4th-5th grade reading level, max, in every doc and every chat message about them. Short sentences. Common words. Keep the numbers, drop the fancy wrapping.
38. The funnel-stage filter. A finding only earns its place if it helps write the ad or the lander. On a VSL offer those are product-blind, so anything a buyer only meets after the video (price, subscriptions, billing, shipping, brand complaints) gets cut. One labeled client-side note at the bottom is the only exception.
39. Stage 2 runs the three Genesis bots faithfully, following each prompt's own output template, with verbatim quotes where the bot asks for them. One file per bot: 01a-offer-brief, 01b-reverse-brief, 01c-buyer-brief.
40. No em dashes anywhere, and quotes are data: never edit a customer quote, even to fix these rules.
41. Ad spying is done at the dissection standard, with visuals (added 2026-08-11). Text-only ad spy is a failed pass. Contact sheets of the top clusters for every real player, frames pulled from inside the biggest videos, transcripts of the winners, format married to concept (who is on camera carrying which idea), and a one-page visual with the concept-by-angle grid as the centerpiece. The Atria key drives it, same as the Mars Men and Primal Viking dissections.
42. Everything shown carries its takeaway and its why (added 2026-08-11). Every image, sheet, grid row, and video pick states the learning it holds and why it was chosen over the alternatives. If a concept list or angle list is shown, say where it came from and what else was considered. "Why am I seeing this?" is a failed element. A takeaway is a learning, not an instruction; rule 36 still holds.
43. Video hooks come from inside the video (added 2026-08-11). On video ads, the ad text and headline matter much less; the video sells. So video hooks are mined from the first 10-15 seconds of the actual video (transcribed) plus the opening frame. Static hooks are mined from the headline and ad text. Every hook wall labels which source each hook came from, and never presents headline text as "the hook" of a video ad.
44. Clarity beats brevity (added 2026-08-19, from Ryan's 2026-08-18 style prompt). Rule 37 keeps the words simple. This rule stops simple from turning into confusing. Never compress an explanation so far that Ryan has to work out what it means. Write clear, natural, complete sentences, not fragments or telegraph-speak. Name the exact thing every time (the exact file, the exact ad, the exact number), never "this" or "it" or "the data." Explain cause and effect out loud: what is happening, why it is happening, and what happens next. Translate anything technical into normal English, and spell out every acronym the first time it appears in a doc. A slightly longer sentence that lands on the first read always beats a short one he has to decode.
45. The research ends in one page (added 2026-10-29, from Ryan on the OsteoShield page: "so good, save it and do it for all of them, more in-depth, more fire, with genius little ideas"). Every offer gets `offers/<slug>/RESEARCH-BRIEF.html`, built to `strategist-references/research-brief-page.md`: the buyer, the VSL reverse-engineered, the market, the gaps table, every ranking from the data with a Learning line under it, flags for the client, a keyword bank of the nouns she types ranked by count, and ten or more one-line Ideas each carrying the number that makes it true. The per-source docs stay the receipts; the page is what Ryan reads. Rules 36 to 44 apply on the page.
