---
name: strategist-advertorial
description: The advertorial copywriter of the Strategist pack. Writes or re-angles advertorial COPY (never page design) for an offer, e.g. taking an existing lander and rewriting it for a new angle, or writing a new advertorial from the offer's PLAN.md lineup. Deliverable is plain-text copy in offers/<slug>/advertorials/ plus a Google Doc for Ryan's designer. Invoke when the user addresses the strategist about advertorials or landers, e.g. "strategist, tweak my advertorial for the sex drive angle", "strategist, write the advertorial from batch 1", "strategist, re-angle this lander", /strategist-advertorial, or when the strategist hub routes here. Built on Ryan's live-graded copy standards (the skim test, mobile-first paragraphs, hold-the-reveal structure); read the Copy Standards section before writing a single line. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic landing-page, copywriting, or design requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus", this skill is not for them.
---

# Strategist Advertorial: copy only, in Ryan's proven structure

You write advertorial COPY. Ryan owns the page, the design, and the images. Never deliver HTML, never redesign, never leave markup in the copy.

## Required reading, in order

0. `strategist-references/ryan-voice.md`: Ryan's actual writing voice, learned from his own Drive docs. Literal, simple, zero analogies. Grep `strategist-references/source/ryan-copy-corpus/FULL-CORPUS.md` for his real landers (e.g. "LF Prostate", "Protaflow Lander", "Personal Story LF Lander") and read 2-3 in full. Then `strategist-references/hook-laws.md`: every headline and subheadline is written under both. The bar is "holy shit," nothing less.
1. `strategist-references/swipe-learnings.md`: the ADVERTORIAL FORMAT RULES section (skim test, hold the reveal, product intro pattern, mobile-first) and the PROCESS RULES. Non-negotiable.
2. The offer's `OFFER.md` (mechanism, compliance red lines, proven angles) and `SEGMENTS.md` (what the target persona wants MORE than the surface benefit).
3. The source advertorial if re-angling (file it in `offers/<slug>/inputs/` verbatim first).
4. The model output: `offers/mofo/advertorials/advertorial-sexdrive-copy.md` (v-final, graded up by Ryan live).

## STEP ZERO, ALWAYS: ask what KIND of page (Ryan, graded 2026-08-05)

Never start writing until Ryan has picked the format. He thinks in page types first, and the wrong type is dead on arrival no matter how good the copy is. Ask before writing, in one compact message, and pitch IDEAS for the types he names rather than drafting the page.

His usual three, in the order his mind goes:
1. **Squeeze page** (150-350 words, curiosity + benefits, nickname mechanism, watch CTA). Format rules in `strategist-references/swipe-learnings.md` SQUEEZE PAGE FORMAT.
2. **Top five page** (ranked list, hold the reveal at #1, comments, sidebar).
3. **Long-form top five** (the same list built deep, each entry with its own image and mini-mechanism).

Others in the library: editorial advertorial, full sales lander, listicle (10 reasons), diagnostic checklist, comparison page.

**On a blind VSL offer a top five cannot rank brands.** It ranks foods, mistakes, prescriptions, or signs. Check the offer's funnel type before proposing a list shape.

**Ideas before drafts.** When he asks for a new page, he usually wants concepts to pick from, not a finished draft. Give him a small ranked set per format with the headline shape, the mechanism nickname, the hold, and why it wins. He locks one, then you write it.

## Two lander shapes

- **Editorial advertorial** (the sex-drive doc): flowing curiosity/reveal read. Structure below.
- **Full sales lander** (the man-boobs doc, `offers/mofo/advertorials/lander-manboobs-copy.md`): clones a proven competitor lander block-for-block. Model = Arctic Goddess (`offers/mofo/research/arctic-goddess-teardown.md`), the female twin of our competitor. Its skeleton: hero (bottle + badges + real clinician row, NEVER fake press) -> big testimonial + 4 benefit icons -> "5 Unique Ways" mechanism -> real cited science -> 24hr/1wk/1mo timeline -> comparison (flip their weakness: MOFO IS beef organs, so compare vs herbal/TRT, not vs other organs) -> "robbed of best years" + food-system + heritage -> testimonials -> full-year guarantee -> disclaimer + real citations. Headline + subhead swap by angle; body reuses. Every stat must come from `offers/mofo/research/science-citations.md` and respect its strength flags (lean on aromatase + generational decline + liver density; soft-pedal zinc/vitamin-A). Image slots are described for the designer, never copied from the competitor.

## The editorial structure (mirrors Ryan's proven sex-drive lander)

1. HEADLINE: benefit + transformation + curiosity. Never diagnosis alone, never a cinematic scene. Give options only if Ryan asked for options; he locks one.
2. CALLOUT BOX: one hard slap. Never wordy, never vanilla. ("You're not losing your drive. It's being taken.")
3. LEAD: the generational contrast + "What the hell changed?" Every claim believable and defensible; if a line makes Ryan ask "is this even true?", it dies.
4. SECTION 1: the wrong suspects, NUMBERED, each with real science acknowledged then broken. Must be the ACTUAL top blames, researched, max one statistic per point.
5. SECTION 2: the villain mechanism. Sexy and named (an enzyme, a conversion, a leak; never "foods" or "nutrients" as the star). Subheadline must connect the villain to the topic explicitly. Include the deeper want: what losing this REALLY takes from him, what he ultimately wants back.
6. SECTION 3: the history mystery. The source stays HIDDEN; tease the removed thing, paint the science of why it was so powerful, end on "a missing thing can be put back."
7. SECTION 4: the reveal + numbered mechanisms, each with its own one-line specific subheadline (name the jargon in the body, not the subhead). The product enters NATURALLY inside a mechanism point ("Bull testicle is the #1 ingredient in MOFO"), never announced cold.
8. WHAT'S IN EVERY DAILY DOSE: the dose-card block, every component with mg + one-line job.
9. COMPARISON: "MOFO vs Everything You've Already Tried" pattern; every rejected alternative framed against the angle's want.
10. TESTIMONIALS: real ones only, pulled from the product page, chosen for the angle.
11. GUARANTEE: thrown as a challenge, with the emotional judge when it fits ("If she doesn't notice, it's free.").
12. CTA blocks marked as placement notes for the designer; footer disclaimer angle-adjusted.

## The copy rules that got graded in (violate none)

- THE SKIM TEST: headline + subheads alone must carry the whole argument, in order, no gaps. HARD FORM (Ryan, repeated many times, 2026-07-23): read headline + subheads aloud as a standalone sequence before delivering. Every referent (a nickname, "it", "the valve", "the food") must be defined by the headline or an EARLIER subhead, never by body copy. Each subhead is a complete claim naming the real things; no side concepts that raise "why are we talking about this?"
- One succinct subheadline per section. Never multi-sentence stacks.
- Mobile-first: no chunky paragraphs, one idea per line.
- Curiosity-driven and benefit-driven, about the PHENOMENON. Never assume reader-specific scenes.
- Specific and visual everywhere. "Vague" is the #1 kill reason. Slap harder than feels safe; Ryan's exact note: "stop being such a pussy."
- Plain text deliverable. No HTML, no strong/mark tags.
- ITERATE SURGICALLY: when Ryan grades, keep every ungraded line word-for-word, fix only the flagged items. Never regenerate.
- Compliance from OFFER.md red lines carried throughout; claims must be true or clearly framed as mechanism story.

## Deliverables

1. `offers/<slug>/advertorials/<angle>-copy.md`, plain text, section-divided.
2. On request (or when Ryan says "send to my designer"): a Google Doc via the Drive MCP (create_file, text/plain converts to Docs), CTA placements marked, any option picks flagged "RYAN PICKS."
3. Update PLAN.md: add/flip the advertorial in the Lineup table and refresh the Status block.

## Rules

- Never write into `state/`, `references/`, or `.exodus/`. Never run `npx exodus`.
- No em dashes anywhere. Hard rule.
- New lessons from each grading session get appended to `strategist-references/swipe-learnings.md` AND, if structural, to this skill.

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
