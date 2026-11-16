# Format Invention Doctrine (v1, 2026-08-24)

The playbook behind `strategist-formats`. How to read the format market, why formats die on a clock, and the five moves that produce formats nobody has run yet. Everything numbered here that is not backed by the Graveyard Study is marked PROVISIONAL until Ryan grades it.

---

## 1. What a format actually is

A format is not "Pixar song video." That is a costume. Every format is two layers:

- **The mechanism**: the psychological reason a human stops scrolling and keeps watching. Mechanisms are old and nearly immortal. Authority in a white coat has printed money since the 1950s. Eavesdropping on a private confession worked in 1920s advertorials and works in UGC today.
- **The costume**: what is literally on screen. The costume is what everyone copies, and the costume is what dies.

Write every format's DNA on one line:

```
COSTUME (what's on screen) / MECHANISM (why it stops the scroll) / TRUST VECTOR (why it's believed) / CAMOUFLAGE (what non-ad content it imitates) / CLONE COST (how hard to copy)
```

Example: Pixar song ads = animated-movie musical number / incongruity (childhood art form selling a supplement, brain has no ad filter for it) / borrowed nostalgia / imitates a movie clip your feed already shows you / clone cost LOW, which is exactly why the window is short.

**The one-sentence law: costumes die, mechanisms don't.** When a format saturates, the mechanism inside it is still alive and looking for a new costume. That is the single biggest source of "new" formats.

## 2. Why formats die on a clock

Attention is a novelty market. The first time a feed shows you a Pixar song ad, your brain cannot classify it as an ad, so you watch. Every exposure after that trains your ad filter. Once the filter is trained, the format's stop-rate falls for every brand running it at once, including the originator.

So a format's death clock starts the day it starts getting cloned, and it ticks faster the cheaper the costume is to copy. The Graveyard Study gives the base rates for individual creatives (38% dead in 7 days, statics live a median 24 days at scale, video 56). Formats live longer than single creatives because iterations refresh them, but the shape is the same: a ramp, a crowd, a cliff.

The strategic consequence: **the edge is not owning a format, it is owning a conveyor.** Ship a format while feeds cannot classify it, ride it, and have the next one ready before the cliff. Never fall in love with a costume.

## 3. The lifecycle stages

Stage every observed format with real evidence: first-seen date across the corpus, how many distinct brands run it, how fast new brands are picking it up, and whether scaled clusters are getting killed.

| Stage | Read | What we do |
|---|---|---|
| **Emerging** | 1 to 4 brands, first seen inside ~60 days, copies growing | The only stage worth entering late. Move now or skip |
| **Rising** | 5 to 12 brands, adoption accelerating | Enter only with a twist that resets the ad filter |
| **Peaking** | Everyone's testing it, big accounts iterating hard | Do not enter. This is where "crushing right now" usually lives, and it means ~90 days left |
| **Saturated** | Adoption flat, scaled clusters getting killed | Harvest the mechanism, abandon the costume |
| **Dead** | Kill ledger material | Free intel: the mechanism is now unclaimed again |

Brand-count thresholds are PROVISIONAL until a few runs calibrate them against this market. The stage read matters more than the label: the question is always "is the ad filter trained yet."

**Evidence rules carried over from research doctrine:** no impressions exist in Atria, so copies = spend proxy and run length = performance proxy. Cluster before counting. Use `order=most_active` for history. Every stage call carries its counts.

## 4. Where new formats have always come from

Check history and the sources are boringly consistent. There are only four, plus a wildcard:

1. **Tech unlocks.** A capability gets cheap, and for a short window ads made with it are unclassifiable. Phone cameras made UGC. Suno plus video gen made Pixar songs. This is the most important source right now because unlocks are landing every few months.
2. **Imports.** A content format that already holds attention organically somewhere else gets used as an ad conceit for the first time. Whiteboard explainers came from YouTube education. Street interviews came from man-on-the-street TV. Podcast-clip ads came from podcast clips. The feed already trained people to watch these; the ad version inherits that training.
3. **Recostumes.** An immortal mechanism gets a fresh costume. The white-coat authority mechanism has been recostumed continuously for 70 years (TV doctor, blog doctor, TikTok doctor, AI doctor). Recostuming is what the market does naturally, slowly. Doing it deliberately and early is the edge.
4. **Collisions.** Two proven elements that have never crossed. The decompose pass surfaces these as empty cells: "in this market, cholesterol is always a doctor face and weight is always a UGC face, nobody has ever crossed them." Crossing a proven pair is cheap because both halves are pre-proven.
5. **Wildcard: inversions.** Take the saturated format's signature element and flip something load-bearing (the AI-perfect ad made deliberately broken, the silent version of a loud format). Riskiest move, use sparingly, only when the flip has its own standalone logic.

## 5. The five invention moves (the generator)

Run all five every time. Generate wide (15 to 25 candidates), then let the gauntlet in section 6 kill most of them. Order them by reliability:

**Move 1: Recostume a dying winner.** Take every format staged Peaking or Saturated. Extract its mechanism. List 5 costumes from the import-watch list (in LEDGER.md) that could carry that mechanism. The Pixar-song mechanism (beloved non-ad art form + earworm + incongruity) does not need Pixar: it can wear any art form with trained-in affection that video gen can now fake.

**Move 2: Import an unclaimed attention format.** Walk the import-watch list in LEDGER.md: content formats that provably hold attention organically and have no ad version in this market yet. For each, ask what the DR health version looks like where the format's OWN rules force the ad story through (a bodycam clip has rules; a courtroom has rules; obeying the borrowed format's rules IS the camouflage).

**Move 3: Tech-unlock scan.** List what became cheap in the last 6 months that was impossible or expensive before. For each capability, ask: what format does this unlock that literally could not exist before, and what does it make so cheap that being FIRST matters more than being good. Pixar songs were sitting in plain sight for months between the capability landing and the first crusher. That gap is the hunting ground.

**Move 4: Collision from the grid.** From the decompose pass, build the costume x mechanism grid for this market. Occupied cells are paid-for proof. Empty cells where both the row and the column are independently proven are pre-validated ideas nobody has assembled.

**Move 5: Inversion.** One or two per run, max. Only when the flipped version has its own reason to stop the scroll, stated without referencing the original.

## 6. The gauntlet (kill order)

Kill candidates in this order, cheapest test first. A run that pitches more than 8 survivors did not kill hard enough.

1. **The reskin check.** If the candidate is a trending format with a palette swap, kill it. Each survivor needs standalone logic: it must be explainable, and exciting, to someone who has never seen the trend it came from. (Ryan's no-formula-cloning rule.)
1b. **The fire check (Ryan, 2026-08-24: "should be fucking insane fire").** Would a stranger screenshot this because they have never seen anything like it in a feed? The menu leads with formats that are visually arresting on sight, the way the first Pixar song ad was. Quiet-and-cheap formats can ride along, but they never headline, and a menu with no jaw-dropper in the top three is a failed run.
1c. **The one-second test on the DEMO (Ryan, 2026-08-24, after grading the first demo sheet "i feel a bit confused").** The twist must be visible inside the frame itself: a stranger must get what is insane about it in one second with zero explanation. A tasteful production still of the format's world (a host at an easel, a man in a hallway) fails; the impossible thing must be ON SCREEN (the canyon IS a liver). If a demo needs a paragraph, the format either gets a better demo or dies.
1d. **The buyer in the frame (Ryan, 2026-08-24, the round-2 grading law).** Graded live: sports-replay-of-getting-out-of-the-recliner = "great"; organ-as-canyon, villain-as-perfume, villain-as-creature = "confusing and not sure how they relate to any of our offers." The winner was the only frame containing the BUYER living a REAL moment from their actual life. The law: a format is a spectacular TREATMENT wrapped around a recognizable life moment (the chair, the stairs, the 3am walk, the mirror). Metaphor formats that replace the person with a symbol of the mechanism force decoding, and decoding kills. Simple and direct beats clever, here too.
1e. **No fake broadcast credibility (Ryan, 2026-08-24, from FB rejection experience).** Facebook rejects ads that borrow news-media credibility: fake newscasts, weathermen, breaking-news framing, anchor desks. Kill on sight, no matter how good. Entertainment-TV surfaces (game shows, variety stages, sports replay, courtroom shows) are a different lane and still allowed, but watch any format that could read as impersonating real media.
2. **The mechanism check.** Name the scroll-stop mechanism in one sentence. If the sentence is "it's new and weird," kill it. Novelty is the window, never the engine. The mechanism must be one with receipts, ours or the market's, with counts.
3. **The untested check.** Search Atria before claiming untested: semantic `query=` with 3+ phrasings of the concept, active AND inactive, and eyeball the top hits. Finding a small prior test is not a kill: it changes the pitch from "never done" to "done once by X, here's why it underperformed or never scaled." Never say "nobody has ever done this" without the searches to show. (Lookback rule.)
   PROVISIONAL (run 1, 2026-08-24): copy-text search cannot see VISUAL formats; ad copy never names its own costume, and on this run `/ad-library/search` returned the same generic pool for every conceptual query (hit rate ~0%, sanity check failed). Always run the hit-rate sanity check; when search fails or the format is purely visual, the evidence base is absence across the run's eyes-on sample, and the claim must be worded "not seen in a sample of N ads," never "never done."
4. **The destination check.** Our offers are product-blind VSL funnels. If the format only works product-aware (unboxings, price reveals, us-vs-them charts), it is dead for us regardless of how good it is. The format must be able to sell a click into a video with no bottle, brand, or price on screen.
5. **The audience check.** Default buyer is 65+. A format that only lands on feed-native 25-year-olds fails unless the run was explicitly for another market. Note: 65+ audiences GREW UP on TV formats (game shows, soap operas, news bulletins, infomercials, radio). Imports from old TV are often stronger for this buyer than imports from TikTok culture.
6. **The feasibility check.** Producible this week with tools on hand (Kie for statics, Suno via the song-ads skill, ffmpeg, video gen, one editor task) or it is a nice idea for someone else.
7. **The moat check.** Estimate clone cost. Trivially clonable formats die fastest; that is not a kill, but it sets the window estimate and the urgency in the pitch.

## 7. The deliverable: a format menu, not ad ideas (Ryan, 2026-08-24, run 1 correction)

Run 1 delivered scripted ad pitches (specific hooks, captions, a courtroom story about snoring). Ryan rejected the altitude: that is angle and concept work, and it belongs to other skills. **A format is only the surface an ad is poured into: the medium plus the look plus the delivery conceit.** "Pixar-style song video." "Whiteboard drawing image." "Judge-show clip." Any topic, any angle, any offer can be poured into any of them.

So the deliverable is a **format menu**: one line per format, ranked, nothing else.

```
N. [Format name] (video or image): what the surface looks like in one sentence. Where it's proven (receipt), and whether it's unseen in our market or already emerging.
```

Hard scope line: no hooks, no scripts, no captions, no personas, no story beats, no offer assignments. If a line only works for one topic, it is not a format, it is a concept wearing a costume, and it gets cut. Turning a chosen format into an actual ad is downstream work (strategist-netnew, strategist-ads, song-ads, strategist-images).

## 8. Standing constraints (inherited, non-negotiable)

- No em dashes anywhere. Plain language in chat, always: say "why people stop scrolling," not "attention mechanism," when talking to Ryan.
- Hooks and on-screen text inside any pitched format still obey hook-laws.md. A new format does not suspend the hook rules.
- Check the agency's tested-dead list and LEDGER.md's killed section before pitching. Re-pitching something Ryan killed burns trust.
- This doctrine file holds the method. Observed formats, stage calls, pitches and their fates live in `formats/LEDGER.md`. Run reports live in `formats/`. One home per fact.
- New rules discovered mid-run get added here marked PROVISIONAL until Ryan grades the wording.
