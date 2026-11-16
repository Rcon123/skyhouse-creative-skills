---
name: strategist-research-brief
description: The research-brief engine of the Strategist pack — the full SkyHouse 35-step research process (client assets, offer breakdown, real-people scrapes, search terms, ad spying, synthesis, ongoing refresh) for one offer, producing extensive PER-SOURCE docs plus the one BRIEF.md that hands off to the creative brief. Invoke when the user addresses the strategist about the research brief, e.g. "strategist, research brief for akka", "strategist, run the big dig on <offer>", "strategist, start the research process", "strategist, refresh <offer>" (the ongoing spy loop), /strategist-research-brief, or when the strategist hub routes here. Distinct from strategist-research (single-purpose Atria competitor pulls — this skill USES it for stage 5) and from strategist-netnew (the downstream creative-brief filler this feeds). The process is Ryan's, approved and evolving: strategist-references/research-checklist.md holds the canonical rules (43 as of 2026-08-11); when Ryan changes the process mid-run, update the checklist and this skill in the same session. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). If the user says "exodus", this skill is not for them.
---

# Strategist Research Brief: the big dig, done so it's worth Ryan's time

You run the SkyHouse research process for one offer. The canonical rules are the 35 steps in `strategist-references/research-checklist.md` — read it EVERY run, follow it exactly, no step skipped silently. The how (phases, source tricks, runbook) is `strategist-references/research-system.md` — read it every run too. This file adds the operator layer: modes, file contract, extensiveness bars, and gates.

**The stakes:** this brief decides what the agency spends money testing. Thin research = wasted spend = burned offers. If a section would come back with one or two findings, that section is not done — dig further, widen the search, try the next source trick. Never pad with filler to look extensive; depth means more REAL findings, each carrying its receipt.

## Two modes

- **New offer** (e.g. Akka): the full 35 steps, stages 1–6. Day one is the big dig.
- **Existing offer**: compressed. Stages 1–2 pull from what the agency already holds (we ARE the ad account — its breakdown belongs to this skill, not to Matt); stages 3–4 run only where thin; the weight goes to stage 5 spying + our own RedTrack/Meta data. Ryan's line: for existing offers, research is mostly spying.
- **Refresh** ("strategist, refresh <offer>"): the every-1-2-weeks report — what's NEW, what's SCALING (copy-count movers), what DIED. Comes to Ryan; nobody sits in Atria clicking around.

## The file contract (Ryan's hard rule: per-source docs, extensive)

Every source lives in its OWN doc under `offers/<slug>/research/`. The brief is a synthesis that POINTS at them; nothing lives only in the brief.

```
offers/<slug>/research/
  00-client-assets.md     stage 1: inventory of what the client gave + what's still missing
  01a-offer-brief.md      stage 2: the Offer Brief Bot output (one file per bot, Ryan's preference 2026-08-11)
  01b-reverse-brief.md    stage 2: the Reverse Brief / Sales Letter Analysis output
  01c-buyer-brief.md      stage 2: the Build a Buyer ELITE output; Ryan's gut take (verbatim) leads stage 2,
                          biggest pain + biggest buyer named
  02-amazon.md            stage 3: brand AND competitors; also: who the competitors are,
                          what else people search
  03-trustpilot.md        stage 3
  04-bbb.md               stage 3 (competitor complaint patterns)
  05-reddit.md            stage 3: search the pain, not the product
  06-x-twitter.md         stage 3: the followed accounts, scraped
  07-search-terms.md      stage 4: short + long tail, hooks in their words
  08-ad-spy.md            stage 5: Atria — patterns, gaps, kill ledger, funnel-type tags
  08-ad-spy-visual.html   stage 5: the visual board — grid centerpiece, contact sheets, hook walls,
                          beat maps; takeaway + selection logic on every element
  swipes/                 contact sheets + reference stills (labeled with copy counts)
  teardowns/              video transcripts (full + opening-15s) and frame sheets
  data/                   every raw pull (jsonl/json/html) — searchable forever
  BRIEF.md                stage 6: the synthesis, one doc per offer (the long receipt)
offers/<slug>/RESEARCH-BRIEF.html   stage 6, THE deliverable Ryan reads (standard since 2026-10-29): one page,
                          built to strategist-references/research-brief-page.md, copied from the OsteoShield exemplar
```

## Extensiveness bars (what "done" means per source doc)

These are floors, not targets. If a source can't reach the floor, the doc says exactly what was searched and why it came back thin — visibly, at the top. Never silently thin.

- **Verbatim language, counted.** Every people-source doc (02–06) ends in two ranked tables: pains ranked by how often they repeat (with counts), and exact recurring phrases (with counts). Tons of people saying the same thing = it goes big in the copy. Aim for 40+ distinct verbatim quotes per major source before ranking; file sound bites by avatar.
- **A quote only stays if it gives us an ad, a hook, or an objection to answer.** Tag each kept quote with which one it is. Everything else stays in `data/`, not the doc.
- **Two quotes are not a fact.** Nothing is called a pattern in ANY doc without repetition; state the count.
- **Brand AND competitors, every source.** Competitor complaints are gold — that's where the unique mechanism hides. Each people-doc has an explicit competitor-complaints section.
- **Amazon** additionally maps the competitor set (who they are, "customers also bought" trail) and what else people search. Sort by units-sold velocity, not review count.
- **Reddit**: multiple subreddits (check for banned/renamed subs — see the access notes), pain searches not product searches, scraped not scrolled.
- **Search terms**: the a–z autocomplete sweep per seed term (~250 queries/seed) minimum; group into the demand map: what language searchers use, which questions repeat.
- **Ad spy (stage 5)**: run it through the `strategist-research` skill's Atria patterns. The brand's own library FIRST (`order=most_active`, deep history), then every real competitor, then the adjacent market that shares the buyer. Patterns AND gaps, kill ledger included, copies × longevity as the money signal. **Tag every ad with its funnel destination — only learn from ads going to the same kind of page as ours.** Watch the actual creative before claiming anything about it.
- **Stage 5 runs at the dissection standard (Ryan, 2026-08-11: "a way better breakdown, and visuals").** Text-only ad spy is a FAILED stage 5. Required, per the Mars Men / Primal Viking standard in `strategist-research` Jobs 1, 2b, 2d and its graded Output spec:
  1. **Contact sheets for the top clusters of every real player** (PIL grids from `images[0].url` / `videos[0].preview_image_url`, labeled with copy counts), saved to `research/swipes/`. Preview stills are only frame one: for the biggest videos, pull inner frames with ffmpeg at ~15/45/80%.
  2. **Transcripts of the winners** (ffmpeg + whisper-cli, filed in `research/teardowns/`). Reuse existing teardowns before making new ones.
  3. **Classify from what you SEE, then marry format to concept** (who is on camera, the conceit, which format carries which concept). A finding like "cholesterol = doctor face, weight = UGC face" is invisible to text alone.
  4. **The visual page**: alongside 08-ad-spy.md, deliver `08-ad-spy-visual.html` in the graded whiteboard style (marker-font look, sticky notes, the concept x proof grid as the centerpiece, real ad images embedded, plain-English labels, self-contained base64 images so it renders anywhere). The board up top is the two-minute read; deeper sections below it are welcome. Report-not-prescribe and plain language apply to the page too.
  5. **Takeaway on everything (Ryan, 2026-08-11).** Every image, sheet, grid row, and video pick on the page carries a one-line LEARNING (what this shows), and the page states its selection logic: why these clusters and not others, where the concept list came from, what was considered and left out. A takeaway is a learning, never an instruction. "Why am I seeing this?" is a failed element.
  6. **Comprehensiveness bar (the Mars Men / Primal Viking standard).** The visual page includes: share-of-testing splits (what % of their actives goes to which promise/avatar/awareness), a hook wall (top hooks with the why-it-works per hook), beat maps of the transcribed winners (what is said and shown, minute by minute), and format married to concept. Thin pages get rejected.
  7. **Video hooks come from inside the video (Ryan, 2026-08-11, repeat rule).** On video ads the headline/ad text matter much less; the video sells. Mine video hooks by clipping the first 10-15 seconds of the top video clusters (`ffmpeg -t 15`), transcribing them (whisper-cli), and pairing each with its opening frame. Mine static hooks from headline/ad text/image text. The hook wall splits by source and labels every hook VIDEO-OPEN or STATIC-TEXT. Presenting headline text as a video ad's "hook" is a failed element.

## Gates (hard stops, in order)

1. **Ryan watches the VSL first, like a stranger.** Ask for his gut take BEFORE any AI breakdown is written. Do not proceed to stage 2 without it (if he explicitly waives it, record the waiver in 00-client-assets.md). His verbatim take is preserved, never merged into the AI's read.
2. **Missing client assets don't block, but they're logged** in 00-client-assets.md as open asks (angles already tested + how they did, call-center logs, support tickets, existing research).
3. **BRIEF.md rules** (checklist steps 23–31): most common avatars; outcomes / concepts / angles kept separate (three different things — never call an outcome an angle); patterns AND gaps; **every line says why it matters — no why, no line**; our own data included, not just competitors; ends with the ranked angle list — safe bets / medium plays / big swings — marked **INTERNAL ONLY, the client never sees it**.
4. **The page (Ryan, 2026-10-29: "so good, save it and do it for all of them").** Stage 6 is not done until
   `offers/<slug>/RESEARCH-BRIEF.html` exists, built section by section to `strategist-references/research-brief-page.md`
   (the OsteoShield page is the exemplar: buyer, VSL reverse, market, gaps, every ranking with a Learning line,
   client flags, plus the keyword bank and the ranked Ideas section). A BRIEF.md with no page is a failed stage 6.
5. **Handoff**: the finished BRIEF.md feeds the creative brief (`strategist-netnew`). Everything after that is the testing process, its own doc — not this skill's job.

## Tools and access (don't rediscover, read the notes)

**Stage 2 runs on the Genesis bot prompts** in `strategist-references/genesis-bots/` (copied from Ryan's Luke Mario Bot Copy Files, 01.13.26 versions): `Ad - Offer Brief Bot` for the offer brief, `Avatar - Build a Buyer ELITE` for the buyer brief, `Ideation - Reverse Brief 1` (the Sales Letter Analyst) to reverse-engineer the VSL's persuasion structure. Follow each prompt's own process — these are Luke's proven frameworks, don't freestyle the breakdowns. The full bot library lives in `~/Downloads/Luke Mario Bot Copy Files/` if another bot is needed.

`strategist-references/research-system.md` bottom section = verified source-access notes (Amazon headers trick, Reddit mirrors, Trustpilot AND BBB via Browser pane, autocomplete free tier). Standing rule: a source needing the browser is a build item for Paolo, not a reason to skip it. Local tools: `tools/research/voice.py`, `tools/research/amazon.py`, Atria key + RedTrack key in `.env` (RedTrack = Jason's key; Facebook only, never Google). Keys pending with Jason: AdSpy (only source with likes/comments), AdBeat Enterprise (~$8k/yr, in Jason's email), SERP API. Also on the wishlist from the Aug 10 call: TikTok/IG spy tools (Matt has a couple), SpyHero (Robbie's tool — Calvin can ask), and burner TikTok/IG accounts following category pages.

## Adaptive clause (this process is a living thing)

Ryan said it plainly: working process, things will change, keep it adaptive. So:
- `strategist-references/research-checklist.md` is the single source of truth for the RULES. The PDF artifact and this skill mirror it.
- When Ryan tweaks the process mid-run ("actually, also pull X", "drop that section"), apply it immediately AND fold it into the checklist + this skill in the same session, with a dated line in the change log below. Never let the docs drift from how the process actually runs.
- When a new key lands (AdSpy, AdBeat, SERP) or a source access method changes, update research-system.md's runbook + access notes.

## Writing rules (Ryan, 2026-08-11, hard rules)

- **The funnel-stage filter.** Before any finding goes in a doc, ask: does this help write the ad or the lander? For VSL offers the ad and lander are product-blind, so the reader does not know a product exists. Pains, symptoms, fears, beliefs, myths, failed-solution categories, curiosity gaps, and exact language: useful. Price, subscriptions, billing, shipping, brand complaints, anything a person only meets after the video: cut it. If one post-product fact truly must be recorded, it goes in a single clearly labeled client-side note at the bottom, never mixed into findings.
- **Stage 2 runs the bot prompts faithfully.** The offer brief, buyer brief, and reverse-engineer outputs follow the Genesis bots' own output templates section by section (the templates are inside the prompt files in `strategist-references/genesis-bots/`). Not a summary in their spirit. The actual structure, with verbatim quotes where the bot asks for them.

- **Report, don't prescribe.** A research doc states what was found, the count, and why it is worth attention. It NEVER converts an observation into a creative directive. No "ads should," no "copy must," no "we need to." Seeing a pattern on Amazon does not prove it works on Facebook. If a finding sparks an idea, pose it as a question for Ryan or leave it out. The angle playbook at the end of BRIEF.md ranks angles as options with their evidence; it does not order anyone to run them.
- **4th-5th grade reading level, max. Always.** Short sentences. Common words. One idea per sentence. Keep every number and fact; drop the fancy wrapping. This applies to every doc this skill writes and every chat message about them.
- **Clarity beats brevity (Ryan, 2026-08-19, from his 2026-08-18 style prompt).** The rule above keeps the words simple. This rule stops simple from turning into confusing, which is the exact thing Ryan got fed up with. Never compress an explanation so far that he has to work out what it means. Write clear, natural, complete sentences, not fragments or telegraph-speak. Name the exact thing every time: the exact file, the exact ad, the exact number, never "this" or "it" or "the data." Explain cause and effect out loud: what is happening, why it is happening, and what happens next. Translate anything technical into normal English, and spell out every acronym the first time it shows up in a doc. Before a doc or a chat message goes out, reread it and ask: is the meaning obvious on the first read, is there enough context, is the cause explained, is the next step stated. Fix it before sending. Checklist rule 44.


## Hook work: the current system only

For any hook on any offer, the live system is  +  +  (grep it by the market's symptom words AND the format tag, then read 5-10 matching hooks in full). The Obsidian vault at ~/Documents/Obsidian Vault/wiki/ and the  skill with its Self-Review Gauntlet are RETIRED (confirmed by Ryan 2026-08-11). Do not use the gauntlet, the 18-word cap, or the doctor/story split from it.

## Change log

- 2026-08-11: skill created from the SkyHouse Research Brief v1 PDF + Aug 3 checklist + Aug 10 call (per-source docs mandate, extensiveness bars, existing-offer mode, ad-account breakdown lives here not with Matt).
- 2026-08-11 (same day, after the first full Akka run): four rules added from Ryan's review. (1) Report, don't prescribe. (2) Plain language, 4th-5th grade max. (3) The funnel-stage filter: only pre-product findings survive on VSL offers. (4) Stage 2 follows the Genesis bot templates faithfully, one file per bot (01a/01b/01c). Checklist steps 36-40 record the same rules. Gut-take waivers now recorded in 00-client-assets.md. First proven output: offers/akka/research/ (12 docs).
- 2026-08-19: clarity-beats-brevity rule added to the writing rules (checklist rule 44), from Ryan's 2026-08-18 communication style prompt. Plain words stay, but simplicity must never come from cutting context or chopping sentences.
- 2026-08-11 (evening): stage 5 raised to the dissection standard after three review rounds on the Akka visual page. Added: contact sheets + inner frames + transcripts as requirements, the visual board deliverable (08-ad-spy-visual.html), takeaway + selection logic on every element ("why am I seeing this?" = failed), the comprehensiveness bar (share-of-testing, hook wall, beat maps, format x concept), and video hooks mined from inside the videos (first 10-15s transcribed + opening frame; headlines are not video hooks). Checklist rules 41-43. BBB access solved via Browser pane. Proven output: offers/akka/research/08-ad-spy-visual.html v3.

- 2026-10-29: the one-page RESEARCH-BRIEF.html becomes the required stage-6 deliverable for every offer, after Ryan on the OsteoShield page: "so good that I want you to save it and do it for all of them moving forward... more in-depth, more fire, with genius little ideas." Spec: strategist-references/research-brief-page.md (adds the keyword bank and the ranked Ideas section). Checklist rule 45.

## COLD-READ JUDGE (built 2026-10-27; ship block removed 2026-10-30; read cap and scope 2026-11-02)

SUPERSEDED 10-30: the "COLD-READ GATE (NOT optional, enforced by hooks)" block that stood here. Ryan, 10-30: "Get rid of
this thing that stops you from doing it because it's just wasting my time." The judge stays as a tool. (dreaming 2026-11-02, sessions 10-30_6aaa8a1e, 10-26_601f85f7, 10-28_fe5dc0fa, 11-02_0af56953)

1. **The reader is never the writer.** Before NEW copy reaches Ryan, run `python3 tools/copygate/coldread.py judge <file>`
   (add `--from "MASTHEAD:"` or `--section "<heading>"` so builder notes above the copy are not read). It prints the
   brief: spawn ONE fresh Agent (general-purpose, sonnet) with `tools/copygate/READER-PROMPT.md`; it runs `coldread.py
   text`, reads once as a stranger, and writes `coldread.py stamp <file> --reader subagent --json @<verdict>`. You never
   write a stamp for your own copy. Say once per session in the reply: the headless stranger is logged out and
   `claude login` in a terminal restores it. Never run `claude login` yourself.
2. **One read, one fix pass, at most one re-read.** Then ship with the remaining flags listed as notes at the top of the
   deliverable. Never a third read: every fresh reader finds a different line.
3. **Never run it on** unchanged copy, a CSS or image swap, a team brief, ClickUp task text, locked hooks or held-reveal
   headlines. Those fail every reader by design. A flag on a line Ryan locked is his call, not a fix.
4. **Their words, not ours.** Every mechanism word comes from `offers/<slug>/LANGUAGE.md` `## Their words`; a word you
   invent goes on `## Never`, not on the page.
5. **The judge is a tool, never a gate.** Nothing waits on a stamp: deploys, Doc pushes, handoffs and ClickUp go when he
   says go. ~~Nothing ships unstamped~~ (removed 10-30; `hook_pre_ship.py` exits 0).
6. **The mechanical floor runs itself** after every Write/Edit to `offers/<slug>/{ads,advertorials,landers,videos}/`.
   Fix dashes, banned words and long sentences before the judge, not after.

Tool and rules: `tools/copygate/README.md`.

Research addition: the synthesis step fills `offers/<slug>/LANGUAGE.md` (`## Their words`) from the VSL, the client's top ads and the real-people scrapes, verbatim phrases only.
