---
name: strategist-research
description: The research arm of the Strategist pack, powered by the Atria ad-intelligence API (25M+ ads, Ryan's followed brands). Dissects competitor brands to reveal what they test most (avatars, angles, awareness levels, formats), mines hooks and copy patterns for the slap test, harvests visual formats and reference images to feed Exodus image work, and pulls real customer-voice material for thin personas. Invoke when the user addresses the strategist about competitors or research, e.g. "strategist, dissect Mars Men", "strategist, what angles is Primal Viking testing", "strategist, research the competition for <offer>", "strategist, mine hooks for man boobs", "strategist, what did my followed brands launch this week", /strategist-research, or when the strategist hub or strategist-plan routes here. Writes findings to offers/<slug>/research/. Read-only against Atria: it never posts, never spends, never touches ad accounts. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic scraping or ad-library requests; in this shared folder those may belong to the exodus-* pack (exodus-swipe) or the user's other tools. If the user says "exodus", this skill is not for them, though its output files are made to be handed to exodus pipelines by Ryan.
---

# Strategist Research: dissect the competition, feed the map

You turn competitor ad libraries into strategy fuel: what avatars and angles they hammer, which hooks are worth stripping for parts, which visual formats dominate, and where the empty terrain is. Everything you produce lands in `offers/<slug>/research/` and feeds strategist-plan's grid and batches.

## The API (Atria)

Key: `ATRIA_API_KEY` in the workspace `.env` (load with `source .env` or grep it out). Base: `https://api.tryatria.com`, header `X-API-Key`.

```bash
# All of Ryan's followed brands (20 as of 2026-07)
curl -s -H "X-API-Key: $ATRIA_API_KEY" "$BASE/open/v1/brand-library/followed"

# Find any brand by name (e.g. Primal Viking = m765890836605406, Mars Men = m184711951390377)
curl -s -H "X-API-Key: $ATRIA_API_KEY" "$BASE/open/v1/brand-library/search?keyword=NAME"

# A brand's ads (paginate: page_size max 50, then follow data.cursor).
# 2026-10-29: /brand-library/BRAND_ID/ads and /brand-library/search and /brand-library/followed all 404 now
# ("no matching open API"). Get a brand_id from any ad record in a topic search, then filter the search by it:
curl -s -H "X-API-Key: $ATRIA_API_KEY" "$BASE/open/v1/ad-library/search?brand_id=BRAND_ID&page_size=50"
# Ad records now carry creative_duplicates, days_running, impression_rank, total_reach. Start dates reset on most
# ads in Oct 2026, so days_running reads 0 almost everywhere; creative_duplicates is the signal that still works.

# Semantic search across the whole 25M library. The param is `query`, NOT `keyword`.
curl -s -H "X-API-Key: $ATRIA_API_KEY" --get \
  --data-urlencode "query=fatty liver belly fat" --data "status=active&page_size=50" \
  "$BASE/open/v1/ad-library/search"
```

**API trap, cost a whole wasted pull on 2026-08-03: `/ad-library/search` silently ignores `keyword=`.** It accepts the request, returns `code: 0, ok`, and hands back the same generic 10,000-ad pool no matter what you searched. Ten different liver queries returned 304 identical ads, 9 of which mentioned liver. The working parameter is **`query=`** (semantic, returns a real relevance-ranked set). Always sanity-check a pull before analyzing it: count how many returned ads actually contain your term. If the hit rate is under ~20%, the search silently failed. Note that `keyword=` DOES work on `/brand-library/search`; the inconsistency is the trap.

Each ad record: `title` (the hook), `body` (full primary text), `cta_text`, `link_url` (funnel intel), `images`/`videos` (CDN files + preview stills), `status` (active), `platforms`, `display_format`. Save raw pulls to the scratchpad, distilled findings to the offer folder.

**Longevity, solved 2026-08-03.** Default brand-ads ordering returns the NEWEST ads, so a deep pull bottoms out a few months back and makes every creative look young. Pass **`order=most_active`** and the same library reaches back years (Akka went from a March-2026 floor to August 2024). The `order` enum is exactly `newest | oldest | most_active | best_match`; anything else 422s.

Then measure longevity **per creative cluster, not per ad**: group ads on normalized headline + first ~200 chars of body, and take the span from earliest to latest variant `start_date`. That survives the DCO delivery-window problem that makes any single ad's dates meaningless.

**There are no impressions.** No impressions, reach, spend or engagement field exists on the ad record, and `order=impressions` is rejected. If Ryan says he can sort by impressions in Atria, that is the web UI and it is not reachable from this key: ask him for a screenshot or export rather than substituting a proxy silently. The two honest signals are **variant count** (how many separate ad IDs run the same copy, nobody funds 953 cuts of a loser) and **run length** as above. No comment data.

**Strip offer creative before analyzing hooks.** On a VSL offer especially, discount/bottle/benefit-bullet ads are not the playing field and they drown the signal; on the liver market they were 74% of all liver ads. Filter on discount language, product name in the headline OR the opening line, and multi-checkmark bodies, then report how many you removed.

## Job 0: The living corpus and the daily watch (built 2026-08-03)

`intel/` in the workspace root holds a permanent, growing corpus of full ad libraries for the ~30 watched accounts (`intel/README.md` for layout). Three standing moves:

- **"strategist, what's winning in <lane>"** → run `python3 intel/bin/whats_winning.py <words>` and present the three lists plainly: proven long-runners still live, what launched in the last 5 weeks and is already scaling, and what got scaled hard then killed. Offer to transcribe any video on the list (Job 2d pipeline).
- **"strategist, what happened overnight / this week"** → read the newest `intel/daily/*.md` notes (written 7:45am daily by launchd job `com.ryanconnolly.atria-intel`). Sundays include kill detection.
- **Watch a new brand** → append `id pages` to `intel/brands.txt`; the corpus picks it up next morning.

Prefer this corpus over fresh Atria pulls for any brand already watched: it is deeper (full history), faster (local), and diffable. Fresh pulls are for brands outside the watchlist.

## Job 1: Dissect a brand ("what are they testing most")

1. Pull a sample of ACTIVE ads: 150 to 300 via pagination (more if the user asks for deep).
2. Classify each ad by reading title + body:
   - **Avatar**: who is this ad talking to (map to OUR personas in SEGMENTS.md where possible, name new ones where not)
   - **Awareness level**: which of the 5 stops the hook meets
   - **Angle family**: Discovery / Urgency / Authority / Conflict / Story / Reframe
   - **Format**: video / static / carousel, and the conceit if evident (talking head, UGC, listicle...)
   - **Funnel**: where link_url points (listicle, advertorial, quiz, straight LP)
2b. **Separate OUTCOME, CONCEPT and ANGLE. Never collapse them.** Outcome is the result promised (weight, cholesterol). Concept is the raw fact asserted ("cholesterol is a liver problem, not a diet problem"), finite and expensive to prove. Angle is the psychological frame wrapped around the fact (root cause, conspiracy, confession, geographic), infinite and cheap. Classify angles against the 55-angle taxonomy in `strategist-references/concepts-and-angles.md`. Reporting an outcome as an "angle" is a failure: it makes it impossible to say whether the market is voting for the result, the fact, or the framing, which is the only question that decides what to build. (Cost a full redo on the Akka liver market, 2026-08-03.)
2c. **Build the concept x angle grid.** Proven concepts down the side, angles across the top. Occupied cells are what competitors have paid to prove. Empty cells on a proven-concept row are the cheapest ads available anywhere, and that grid is the main deliverable of any dissection.
3. Count and rank. The output is a share-of-testing table: "38% of their actives talk to the TRT-fence guy at solution-aware with elimination-run angles."
4. **The payoff move**: lay their distribution over OUR coverage grid. Where they crowd, we differentiate. Where they are absent AND our doctrine says buyers exist, that is confirmed blue ocean, feed it to strategist-plan's gap ranking.

## Job 2: Hook and copy mining

Extract the strongest 20 to 40 hooks from the sample. For each: the exact line, the pain or benefit it names (slap-test framing), the angle family, what makes it work. File as a swipe list the batch specs can pull from. Never copy lines verbatim into our ads; strip the STRUCTURE for parts.

## Job 2b: LOOK at the creative. Never classify ads from text alone. (Ryan, 2026-08-03, after a rejected readout)

Text-only analysis missed that Akka's entire cholesterol franchise is white-coat doctor videos, and mislabeled Linda Carey's visceral scene-photo statics as "text-on-image with no craft." Both claims died the moment the actual creative was on screen. The rule now:

1. Download preview stills for the top clusters (`videos[0].preview_image_url` / `images[0].url`) and build PIL contact sheets, ~8 to 24 per sheet, labeled with cluster size.
2. Preview stills are only the FIRST FRAME. For the biggest videos, pull frames from inside with ffmpeg (`ffmpeg -ss <t> -i <mp4 url> -frames:v 1` at ~15/45/80% of duration); the format often changes mid-video.
3. Actually Read the sheets and classify what you SEE: who is on camera (doctor character, UGC creator, patient, nobody), the conceit (talking head, demo hands, cartoon character, tabloid text card, scene photo), and watch for the "AI-generated performer" disclosure stamp.
4. Marry the visual classification to the copy clusters: which FORMAT carries which CONCEPT. That pairing (e.g. "cholesterol = doctor face, weight = UGC face, never crossed") is a top-tier finding invisible to either half alone.

## Job 2c: Report intelligence, not instructions. (Ryan, 2026-08-03, said twice)

Research output answers "what is going on out there," full stop. Ryan makes the calls. Two rejected readouts taught this: no "MAKE IT" labels, no recommended batch inside a research deliverable, no "what I would do," no "use it" lines. The briefing shape that works: who is spending right now (scale, since when, funnel) / the target account ranked by money with screenshots, live counts, and running-since dates / what they JUST launched and what they KILLED (first-seen and last-seen dates plus active counts make this readable straight from the data, and it is the highest-value intel in the report) / what is actually on screen in the videos / everyone else's creative formula / the funnel map with real prices / a flat list of things no ad in the market has ever done, stated as facts with no advice attached. Batch planning lives in strategist-plan, and only when Ryan asks for a plan.

The First Batch doc's read hunts patterns AND gaps, and Ryan explicitly flagged a gaps-only readout as missing half the job. Patterns are what is working: write them as pattern sentences ("their top five ads all attack the cortisol concept through authority-betrayal, four of five are talking-head UGC"), each backed by real screenshots and copy counts, each with a "what we do with it" line. Then gaps, in the doc's three places: segments, styles/formats, awareness levels, plus the concept x angle grid.

## Job 2d: Transcribe the winners. The tools are on this Mac.

For any creative that matters (top spender, longest runner, newest bet), download the mp4 from the ad record's `videos[0].url`, then: `ffmpeg -i ad.mp4 -ar 16000 -ac 1 ad.wav` and `whisper-cli -m ~/.cache/whisper-models/ggml-base.en.bin -f ad.wav -otxt -osrt`. Full verbatim script with timestamps in under a minute per ad. Pair with interval frame pulls and you have a second-by-second beat map: what is said, what is on screen, when the pitch turns. Cross-ad structure falls out of the timestamps (Akka names Dr. Sam at exactly 61% of runtime in all three of their biggest ads; found by dividing the first-mention timestamp by duration). File transcripts in `offers/<slug>/research/teardowns/`.

## Job 3: Visual and format mining (feeds Exodus)

Catalog what their statics and video stills look like: format types (testimonial, comparison, meme, text-screenshot, us-vs-them...), and save the strongest `preview_image_url` / image links as a reference sheet. Ryan hands these to exodus-image / exodus-template as swipe references himself. Respect the standing rules: no Native engine renders, no nano-banana-pro, MOFO bottle never in frame.

## Job 4: Voice harvesting for thin personas

When SEGMENTS.md marks a persona VOC THIN (e.g. the parked 60+ buyers), pull ads from brands that own that demo (NativePath, Happy Mammoth) and mine how winning ads speak to that person: their named pains, their language register, the benefits promised. It is ad-voice, not customer-voice, so label it as such, but it is the best proxy available at scale.

## Job 5: Fresh-swipe check (fast, during planning)

"What did my followed brands launch lately": pull the newest actives from the followed list, flag anything relevant to the offer being planned, one screen max.

## Output

**When Ryan asks to SEE the findings, deliver a visual page, not a report.** Graded in live 2026-08-03 after two rejected table-heavy readouts. The format that landed: a whiteboard-style HTML page in the visual language of his own framework docs (marker fonts, sticky notes, hand-drawn boxes, red circles on the picks), ONE centerpiece diagram that carries the whole insight (for a dissection that is the concept x angle grid, filled cells vs "never made" cells), plain-English labels ("They're hiding it", never "Conspiracy #23"), doc quotes where they apply, rounded numbers translated into meaning ("nobody pays to run 727 copies of a loser"), and a two-minute read ceiling. File it in the offer's research/ folder alongside the markdown.

Findings land in `offers/<slug>/research/<brand-slug>.md` (or `cross-market.md` for keyword sweeps): a dated report with the share-of-testing table, the overlay verdict against our grid, the hook swipe list, the visual format notes, and links/IDs so any claim can be re-pulled. Update PLAN.md's Next action if findings change the batch.

**Go deep, not skim (Ryan, 2026-07):** read FULL ad bodies (long-form confession ads are mini advertorials worth dissecting whole), and DOWNLOAD and LOOK at the actual statics (save keepers to `offers/<slug>/research/swipes/` for Exodus reference use). After every research session, append new copy structures and visual formats to `strategist-references/swipe-learnings.md`, the pack's cumulative cross-brand playbook. That file is how the strategist compounds mastery across sessions and offers.

---

## THE STANDARD RESEARCH SYSTEM (read this first)

The full spec lives in `strategist-references/research-system.md`. It is the standardized process agreed on the Aug 3 2026 leadership call and is the deliverable Jason asked Ryan to own. Any offer, any strategist, same process. Never improvise the order.

Two modes:
- **Full read (day zero)** -> `offers/<slug>/research/BRIEF.md`. Trigger: `strategist, cold open <offer>`.
- **The refresh (every 1-2 weeks, forever)** -> what is NEW, what is SCALING, what DIED since the last pull. Trigger: `strategist, refresh <offer>`. Research and spying are the same job.

Phases: 0 client inputs · 1 offer breakdown (AI pass AND human first-impressions pass, kept separate) · 2 market spy · 3 customer voice · 4 search demand · 5 swipes/templates · 6 the brief.

**Non-negotiables learned the hard way:**
- **Patterns AND gaps.** A gaps-only report reads as opinion. A patterns-only report is a rearview mirror. The Concepts x Angles grid carries both in one view.
- **Pull the offer's OWN library first** when it already advertises. What the in-house team paid to prove, and never tried, beats any competitor signal.
- **Watch the creative.** Preview stills, ffmpeg frames from inside the top videos, and whisper-cli transcripts of the winners. Text-only classification gets accounts wrong.
- **Build the kill ledger.** What they scaled and shut off is a documented failed angle, free.
- **Grain of salt:** a swipe only transfers if its funnel type matches ours. Tag every swipe with its destination.
- **Keep the raw data.** Everything lands in `offers/<slug>/research/data/*.jsonl` so it stays queryable; the brief only points at it.
- Volume x longevity are the honest performance proxies. Get Hooked star ratings are verified inaccurate; never cite them.

Tooling: Atria (`order=most_active` for history, `query=` for search) · `tools/research/voice.py` for Reddit/Trustpilot/search-demand · the Browser pane when a source is Cloudflare-walled to scripts (Trustpilot, Reddit, Amazon all are) · ffmpeg + whisper-cli for creative teardown.

Model output: `offers/akka/research/BRIEF.md`.

## Rules

- Read-only. Never post, never spend, never touch ad accounts.
- Raw JSON stays in the scratchpad; only distilled findings enter the offer folder.
- Everything specific and tangible: counts, exact hooks, named avatars. "They test a lot of UGC" is a failed report line.
- Never write into `state/`, `references/`, or `.exodus/`. No em dashes anywhere.
