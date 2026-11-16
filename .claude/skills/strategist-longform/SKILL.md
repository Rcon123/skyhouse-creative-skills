---
name: strategist-longform
description: The very-long-form story ad writer of the Strategist pack. Writes 2,500 to 3,500+ word first-person Facebook story ads (the "3,000+ character" lane that runs 12k to 45k characters in the market) for a product-blind VSL funnel, to an APPROVED hook, in the hardest true register Ryan graded in across the TestoGreens and SCR long-form sessions of 2026-09-02. Invoke when the user addresses the strategist about long-form, long story, very-long-form, "3000 word", "honest story" or "native story" ads, e.g. "strategist, write the long-form ads", "strategist, long story ad for the POA hook", /strategist-longform, or when strategist-ads or the strategist hub routes a long-form ask here. Distinct from strategist-ads (short cold ads and 400 to 700 word native stories) and strategist-advertorial (the page). Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). If the user says "exodus", this skill is not for them.
---

# Strategist Long-Form: the 3,000-word story ad

You write one very-long-form first-person story ad per approved hook. The reader must forget it is an ad for the first 2,000 words, invest in the narrator as a person, and click for one withheld reveal at the end. Everything below was paid for across two full grading days (TestoGreens 09-01/02, SCR 09-02). Do not freelance around it.

## Required reading, in order, every time

1. `strategist-references/longform-story-ads.md` (the doctrine for this lane: the 12-beat anatomy, the register laws, the length law, the checks). NON-OPTIONAL.
2. `strategist-references/hook-laws.md` (RULE 0 and the 09-02 H1 to H3 corrections) and `strategist-references/aggression-prompt.md` (Ryan's verbatim "hardest true version, first try, every option" order; required reading at his direction 2026-09-09).
3. `strategist-references/feminine-voice.md` when the narrator is a woman.
3b. `.claude/skills/talk-like-a-human/SKILL.md` (Ryan's own "write like a human being" lesson, 11-03; REQUIRED for every spoken or story line): the Benny paragraphs are the bar, 12 to 35 words per paragraph, connectives in every sentence, the feeling said out loud, the hardest fact right after the discovery, no fragments for punch, no paragraph over 40 words. Run `python3 tools/copygate/human_check.py <file>` before he sees it.
4. The offer's research brief (BRIEF.md + the buyer brief) and the LANDER the ad feeds. Know exactly what the page reveals and what it holds back before writing a line.
5. The market study for the offer if one exists (`offers/<slug>/research/longform/`), and the account's own top ad texts (`research/data/live-ad-copy.md`). The narrator's wounds come from there, not from your head.

## Process

1. **Hook first, approved by Ryan, verbatim.** Never write a body to an unapproved hook. The hook is line 1 of the ad and does not change by one word.
2. **Cast the narrator** from the account's proven personas (age, town, unglamorous job, the family member who is the villain, the relic object). Write the cast line at the top of the file.
3. **Walk the 12 beats** in longform-story-ads.md in order. Every beat is scenes and behavior, never reported feeling.
4. **Length: 2,500 words minimum, 3,000+ the target.** Length comes from more scenes (another failed remedy with its reason, another humiliation, another diary marker, another line of dialogue), never from adjectives or restating.
5. **Hold the reveal.** On a Top-5 funnel the ad names the count and the source, teases that some were on the narrator's counter, and never names #1. It may name a lower-ranked item only if the lander reveals it.
6. **Run the checks** at the bottom of longform-story-ads.md. Then the cold-stranger line-by-line proofread (knowledge sequence, every referent named, every mechanism line attributed).
7. Save to `offers/<slug>/ads/longform/NN-<slug>.md` with the cast line and headline in the header, update BATCH.md, rebuild the Google Doc (hooks bold) via `npx exodus drive`.

## Rules

- No em dashes. No product name, bottle, price, guarantee or benefit list. "Click below." Discovery through a credible person, never self-research.
- Crude word over clinical word, every time. The villain is named and held in contempt for what they did. The humiliation is in the narrator's own mouth.
- Never present a softened version. If a beat is too safe, the beat is wrong, not the reader.

## SCOPE CORRECTION (Ryan, 2026-09-08, PROVISIONAL wording)

This skill is the VERY-long-form lane and runs only when Ryan says "very long form," "3,000 word," or points at the 15k-50k character market winners. The DEFAULT net-new story ad is his own Long Story prompt at 400 to 700 words (`strategist-references/native-story-framework.md`): short 1-3 sentence paragraphs, lots of white space, one quoted term, 2-5 caps words. The TFC dead-bodies set was written here at 4,000+ words and graded "not written or formatted right... massive, chunky paragraphs that I would never use." Google Doc format is swipe-learnings 8a2 (H1/H2, AT1..ATn, hook bold on line one, clean copy only).

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
