# THE RESEARCH SYSTEM

> The standardized research process for any offer, new or running. Distilled from the Aug 3 2026 leadership call (Ryan, Jason, Fernando, Calvin, Matt) plus what the Akka run proved out. This document is the spec Jason asked for: the outline that can be handed to Paolo, run by any strategist, and shared with a client. The strategist pack runs it via `strategist, cold open <offer>` (first pass) and `strategist, refresh <offer>` (the ongoing loop).

The one-line version: **research = the full read at day zero, then spying forever.** Both are research. The first produces THE RESEARCH BRIEF. The second produces a biweekly refresh that comes to you, so nobody has to go live inside Atria.

---

## PHASE 0 - What we collect before touching anything

From the client (goes in the onboarding pre-survey; if they refuse, note Jason's line: "you don't want us to be successful"):

1. The funnel assets: VSL script, landers, advertorials, TSL, PDP, every live URL.
2. **Every angle they have already tested and what happened.** The playbook conversation runs in reverse too: "here are the 27 things we want to test, which have you tried?" puts ownership back on the client.
3. Ad account access (or exports): what worked, what died, CPCs, CPMs. This becomes its own brief. **The breakdown itself lives inside this research process, not with Matt** (Jason, Aug 10 call: it's the easiest thing to scrape — "what are your winning ads, give them to me").
4. Call center logs and customer support tickets.
5. Any research they already have.

## PHASE 1 - The offer breakdown

Two passes, never merged:
- **The AI pass:** feed the VSL/lander through the breakdown bots -> OFFER BRIEF (what the product is, price ladder, mechanism, claims, guarantee, compliance red lines) and the reverse-engineered structure (what the VSL argues, in order, and which loops it opens and never pays off; unpaid loops are free ad leads).
- **The human pass (Fernando's rule):** watch the VSL as if you are a brand-new stranger. Write down first impressions before the AI's read biases you. What slapped, what dragged, what you did not believe.

## PHASE 2 - The market spy (Atria API, the key in `.env`)

This is the pattern-and-gap read. Both halves matter: **patterns are what the market has paid to prove; gaps are what nobody has claimed.** Never deliver one without the other.

1. **The offer's own library first.** If the brand already advertises, its own account outranks every competitor signal: it shows what the in-house team paid to prove and what they never tried. Pull deep with `order=most_active` (reaches years back; default ordering only shows the newest window).
2. **Every competitor scaling in the category.** Semantic search (`query=`, never `keyword=`, which is silently broken), then pull each real player's full library.
3. **Adjacent markets that share the buyer.** Jason: "what are the top diabetes ads? Diabetes is only weight loss, which is the same thing liver is too." Pull the adjacent category the offer's promise actually lives in.
4. Per creative cluster (dedupe by copy, count the copies): **concepts tested, angles tested, copies per creative, live count, first-to-last run span, format (video/static), funnel destination.** Copies x longevity is the money signal; nobody runs 900 cuts of a loser for 18 months.
5. **The kill ledger.** What they tested at scale and shut off is as much signal as what they scaled. Dead creative = a documented failed angle, free of charge.
6. **Watch the actual creative.** Pull preview stills AND ffmpeg frames from inside the top videos; transcribe the winners (whisper-cli). Classify formats (podcast clip, kitchen demo, talking doctor, cartoon character, gross-hands b-roll...). Text-only analysis misclassifies accounts; the Akka "doctor video" turned out to be a first-person cartoon liver.
7. **The grain-of-salt rule:** a winning creative only transfers if its funnel type matches ours. Native-style statics feeding an advertorial prove nothing about a VSL gate. Tag every swipe with its destination type.
8. Tools of record: Atria API (primary). AdSpy for likes/comments when the key lands (Jason has the API). Get Hooked MCP exists but **never trust its star rankings** (verified inaccurate against our own data). **AdBeat Enterprise** pending (~$8k/yr, sitting in Jason's email to-do folder; heavy on native ads). Facebook Ads Library as the free fallback. Wishlist from the Aug 10 call: TikTok/IG spy tools (Matt has a couple), SpyHero (Robbie's tool, Calvin can ask for API access), burner TikTok/IG accounts following a ton of category pages, and feature specs for Flavio's scraper (Ryan + Fernando own the feature list — what to pull out of the data lake: what ran, what worked, what didn't).

## PHASE 3 - Customer voice (the people research)

Scrape real people, for the brand AND its competitors. Competitor complaints are where the unique mechanism hides (Native Path collagen won on Vital Proteins' shrunken-packaging complaints).

- Amazon reviews: the product's category equivalents and every named competitor. Note which competitor products the "customers also bought" trail exposes.
- Trustpilot: the brand, the competitors.
- BBB: the competitors (complaint patterns).
- Reddit: the condition subreddits and the "struggling with X" searches. Scraped, not manual (Calvin's time sink).
- The X/Twitter follow list: scrape the followed accounts instead of scrolling the feed.
- **Ranked, not sampled:** the output is pain points and phrases ranked by frequency ("1,000 people made the same comment -> that goes big on the lander"), plus verbatim sound bites filed by avatar.
- **Everything raw goes into the store** (`offers/<slug>/research/data/*.jsonl`, our local Supabase): re-queryable forever, never rely on the summary doc alone.

## PHASE 4 - Search demand (what people actually Google)

SERP/keyword pull for the condition, the mechanism, the product class, the competitors. Short and long tail. Free tier: Google autocomplete expansion off seed terms (a-z suffix sweep); paid tier when the SERP API lands. Output: the demand map, what language real searchers use, which questions repeat.

## PHASE 5 - Swipes and templates

Matt's STORMING frame: a standing source checklist (Swipes, Templates, and the rest) so nobody free-styles where they look. Swipe files live with destination-type tags (grain-of-salt rule). Winners get stripped for structure, never copied.

## PHASE 6 - Synthesis: THE RESEARCH BRIEF

One document per offer, `offers/<slug>/research/BRIEF.md`. Sections, in order:

1. **The offer** (from Phase 1, with the human first-impressions kept separate)
2. **The market map**: who is really in the category vs borrowing it, with receipts
3. **Patterns**: what the market has paid to prove (concepts, angles, formats, faces, funnel shapes, with counts and run spans)
4. **The kill ledger**: what was tested at scale and shut off
5. **Customer voice**: ranked pains, ranked phrases, sound bites by avatar, competitor complaint openings
6. **Search demand**: the demand map
7. **Avatars, ranked**: the macro pain and macro avatar first (Jason: that is always step one), then the pockets
8. **Concepts x angles map**: patterns and gaps on one grid, concepts as rows, angle families as columns, filled cells carry the market's receipts, empty cells are unclaimed
9. **THE ANGLE PLAYBOOK**: the client-shareable list (the "27 things"), every angle tagged Banker / Bridge / Bet, sized 70/30 iterations to net-new. This is the piece that justifies the 90-day term: "this is what 90 days of testing walks through."
10. **Feeds**: what goes to the copy brief (Fernando's input spec) and only then to the creative brief. Statics before video. For statics: image, then hook, then body, in that order of importance. For video: visual hook + copy hook.

## THE REFRESH (research never ends)

Every 1-2 weeks per live offer, delivered as a report (not a dashboard visit): what is NEW since last pull (new creatives, new competitors, new angles), what is SCALING (copy-count movers), what DIED. Plus the swipe-feed pull (X follows, organic). The refresh is how "research" and "spying" become the same job. Idea file: a daily-email version once the scraper graduates (Jason's "more than a scraper" vision, sits with Sam/Apollo).

## Operating rules

- Patterns AND gaps, always both. A gaps-only report reads as opinion; a patterns-only report is a rearview mirror.
- Raw data is never thrown away. Summaries point at the store.
- Any claim about a video that nobody watched is a guess. Watch the creative.
- Volume and longevity are the only honest performance proxies in spy tools; star ratings are not.
- The brief is shareable with the client. If they hand it to their internal team, their team should have built it anyway.
- Juniors start in research (90 days) and iterate winners daily while they learn taste.

## Runbook (what actually executes, today)

| Step | Tool | Status |
|---|---|---|
| Atria pulls (brand, category, adjacent, most_active, kill ledger) | `pull.py` pattern + Atria key in `.env` | live, proven on Akka |
| Creative viewing | ffmpeg frames + contact sheets + whisper-cli transcripts | live, proven on Akka |
| Customer voice | `tools/research/voice.py` (Reddit JSON, Trustpilot, autocomplete) | live |
| Amazon / BBB | fetch with fallback, else manual paste | best-effort |
| AdSpy comments, AdBee, SERP API | keys with Jason | stubbed until keys land |
| Raw store | `offers/<slug>/research/data/*.jsonl` | live |
| The brief | `offers/<slug>/research/BRIEF.md` | template = Akka's |

---

## Source access notes (verified 2026-08-03, hand these to Paolo)

Every people-research source blocks naive scripts differently. What actually works:

| Source | Status | How |
|---|---|---|
| **Atria API** | works | `order=most_active` for history, `query=` for search (`keyword=` is silently ignored) |
| **Amazon listings** | works | 503s on a bare request; serves fine with full Safari headers (UA + Accept + Accept-Language + Sec-Fetch-*). Split cards on `data-component-type="s-search-result"`, not on `data-asin`. **Sort by units-sold-last-month, not review count** — velocity is the real signal and many listings hide review counts. |
| **Amazon reviews** | works, changed | `/product-reviews/` now 302s to a login wall. The `/dp/` page still carries most-helpful reviews unauthenticated. New markup: `data-hook="reviewTitle"`, `reviewTextContainer`, `helpful-vote-statement`. Strip the container class prefix and the "Read more / Report" chrome from the extracted text. |
| **Amazon related searches** | mostly dead | Amazon stopped rendering the related-search rail server-side. Use the Google autocomplete a-z sweep instead; it returns ~250 queries per seed. |
| **Google autocomplete** | works | plain GET, no headers needed. The a-z suffix sweep is the cheapest demand map we have. |
| **Trustpilot** | browser only | 403s to scripts. Works through the Browser pane (`preview_start` + `get_page_text`). |
| **Reddit** | mirror or browser | reddit.com and old.reddit.com 403 scripts, and reddit.com is blocked in the Browser pane. Use a redlib mirror (safereddit.com). Mirrors throw a JS challenge to curl, so drive them through the Browser pane. Check whether the obvious sub is banned: r/FattyLiver is banned, r/FattyLiverNAFLD (27.2k) is the real one. |
| **BBB** | browser only (solved 2026-08-11) | Search results render client-side; scripts get an empty shell. Works through the Browser pane: `bbb.org/search?find_country=USA&find_text=<name>` then get_page_text. Still a Paolo build item for headless automation. |
| **AdSpy / SERP API** | keys pending | Jason holds both. AdSpy is the only source in the stack with likes and comments. |

**Standing rule:** whenever a source needs the browser rather than a script, that is a build item for Paolo, not a reason to skip the source.
