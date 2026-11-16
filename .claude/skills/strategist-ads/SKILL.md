---
name: strategist-ads
description: The ad copywriter of the Strategist pack. Writes Facebook/Meta ad copy (hooks + primary text) for an offer's angles, usually feeding an advertorial or lander, in Ryan's own voice learned from his full Drive corpus. Invoke when the user addresses the strategist about writing ads, e.g. "strategist, write ads for the sex drive angle", "strategist, more ads like AT1", "strategist, ads for batch 2", /strategist-ads, or when the strategist hub routes here. The required reading is NOT optional; every rule in it was paid for across a full live grading session. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic copywriting requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus", this skill is not for them.
---

# Strategist Ads: hooks + primary text, in Ryan's voice

## Required reading, in order, EVERY time

1. `strategist-references/ryan-voice.md`: his voice DNA and format taxonomy. Pick the FORMAT first (cold ad = curiosity bomb selling the click, product unnamed; retargeting AT = named product; etc.). Then grep `strategist-references/source/ryan-copy-corpus/FULL-CORPUS.md` (608 of his docs) for the offer/format at hand and read 3-5 of his real examples IN FULL before writing a word. THE COUNT IS A HARD GATE, not a suggestion: one example produced ads Ryan graded "really bad" plus a diffable lift (2026-08-05). Always include `Fire-Hooks-Swipe-File.md` (in the corpus, grep for it): it is the hook register bank and every hook gets checked against its patterns. In the delivery message, NAME the corpus docs read this session so Ryan can audit the inputs.
2. `strategist-references/hook-laws.md`: his Hook Laws, verbatim. The bar is "holy shit." RULE 0 (DEAD SIMPLE OR DEAD, added 2026-08-25) outranks everything including voltage; its three kill tests (cold stranger, real behavior, plain words) run on every line as the FINAL pass, after amplification.
2a. `strategist-references/amplification-craft.md` (PROVISIONAL, adopted 2026-08-25 from Luke's Hook Forge kit): the amplification protocol — ineffective gate, climb-the-fact, name-the-crime, bar test, loop gate, calibration lines. Runs AFTER drafting, BEFORE the Rule 0 kill pass. If output is politer, vaguer, or more resolved than its calibration lines, go around again.
2c. `strategist-references/aggression-prompt.md` (Ryan's verbatim standing order; wired in as required reading at his direction 2026-09-09): read before drafting a single hook. "Hardest true version, first try, every option." Every option at full strength, no safe one beside the real one, no hedging or caveats. He would rather dial a hook back than ramp it up.
2b. `strategist-references/hook-bank.md`: 729 verbatim hooks from scaled ads, tagged by format (advertorial_longform / video / static_short / static_onimage). Too big to read whole: grep it for the market's symptom words AND the target format tag, then read 5-10 matching hooks IN FULL before drafting. Use them as pattern fuel (hook-laws #22: steal the principle, never the words).
3. `strategist-references/swipe-learnings.md`: process rules (surgical iteration, formulas-not-sentences, angle diversity, protect the lander's reveal), ad format rules (montage mandatory, BBQ-test mechanism, two lengths), and competitor intel.
4. `strategist-references/native-story-framework.md`: Ryan's own long-form "native story" prompt (400-700w organic-post ads: hook formulas, trusted source + skepticism, progressive timeline, interpersonal drama, soft P.S. CTA). REQUIRED whenever the ask is a long story ad; pair it with the living-proof character hook formula in swipe-learnings.
4b. `strategist-references/feminine-voice.md` (PROVISIONAL pointer, added 2026-08-20, Ryan has not graded this wording): REQUIRED whenever the narrator is a woman. The kitchen-table test, the emotion engine (every line slaps), scripted tells, the 8 voice patterns / 7 anti-patterns, mobile ellipsis pacing, and the Dr. Hoffman 23-beat structure. This is the upgraded version of the feminine-voice memory file from the home workspace.
4c. `.claude/skills/talk-like-a-human/SKILL.md` (Ryan's own "write like a human being" lesson, 11-03; REQUIRED for every spoken or story line): the Benny paragraphs are the bar, 12 to 35 words per paragraph, connectives in every sentence, the feeling said out loud, the hardest fact right after the discovery, no fragments for punch, no paragraph over 40 words. Run `python3 tools/copygate/human_check.py <file>` before he sees it.
5. The offer's OFFER.md (mechanism, compliance red lines) and the LANDER the ads feed.

Reference outputs: `offers/mofo/inputs/ryan-example-ads.md` (his winning MOFO ads) and `offers/mofo/ads/sexdrive-ads.md` v12+ (the first set written post-corpus).

## Where the time goes (Ryan approved the rule 2026-09-09; wording PROVISIONAL)

Hooks are 80 to 90 percent of the work. The body follows the hook. Ryan to Jet, 2026-08-26: "hooks matter 80%... if you have a boring dog hook and you're using AI, what's going to happen with the body?" and "you should be spending basically 80% to 90% of your time on the hooks. And then the body should basically write itself." To Ary, 2026-09-02: "put most of your focus on the hooks and the images. In the body... that should be, like, your last worry."

He grades the concept, the hooks and the images. He barely reads the body (2026-09-03: "I'm not really reading the body copy at all. The thing that takes the most time is hooks").

So: get the hooks approved FIRST. Hooks get the rounds. Never write a body under an unlocked hook. Once the hooks are locked, write the body in one pass, then run the line-by-line cold-stranger proofread, and deliver.

## Process

0. When Ryan pastes or links material (a research block, a ranking, a Loom, a swipe URL, a transcript), the first line of the next reply names it and the three things from it that drive the build. If that line cannot be written from his material alone, read it again before writing anything. (Ryan 10-29: "Did you even read what I just sent you?"; dreaming 2026-11-02, sessions 10-29_cd58bf7d, 11-01_7edc0272)
1. Confirm the angle, the destination lander, and what the lander holds back (its reveal). Ads sell the click; the lander educates and reveals.
2. Write cold ads and retargeting ATs as separate formats. Never mix registers. For STATIC cold ads there are exactly two registers: first-person story or doctor ad (Ryan, 2026-08-05). Model only on static corpus docs; video-script docs (UGC/video/Cartoon titles, stage-direction beats, "look at this photo" reveals) are off-limits as models for statics.
3. Every set: different angle door per ad, hooks passing the Hook Laws, transformation montage in anything longer than a teaser, and a click tease with something specific waiting.
4. Deliver in chat for grading. Iterate SURGICALLY on flags only. On approval: save to `offers/<slug>/ads/<angle>-ads.md` and push a Google Doc (Drive MCP) if asked.
5. New graded-in lessons append to `strategist-references/swipe-learnings.md` (process/format) or `ryan-voice.md` (voice), never both.


## AFTER THE HOOK IS LOCKED: the three body passes (Ryan, 2026-10-29; REQUIRED)

Write the body once, then run `strategist-references/body-polish-passes-2026-10-29.md` in order: (1) the crystal-clear rewrite, (2) the storyteller rewrite, (3) the phone format from Ryan's own example, (4) the every-word pass: keywords, vicious, intentional, the slide. Each is a full rewrite, not an edit, and returns only the copy. For a doctor ad, the shapes and the body skeleton are in `strategist-references/doctor-ads-study-2026-10-29.md` (read it before writing, not after). Then the cold read. Ryan sees the copy only after all four.

**The target band for every body pass (dreaming 2026-11-02, sessions 10-27_a6556288, 10-29_ccab9cfb, 10-30_c21efef8, 10-30_7b2411ff, 10-26_601f85f7):** sentences 8 to 22 words, most of them 12 to 18, with the spoken connectives in them (and, so, because, but). Paragraphs 1 to 2 sentences. "Chunky" means the paragraphs; "choppy" means runs of sentences under 6 words. A rewrite that moves the median sentence outside the band either way is wrong, not a fix: four sessions swung from 35-word sentences to fragments and back. The copygate check warns on both ends; read the warns before the judge.

## HEADLINES (Meta HL field): a measured ceiling, before you see them (dreaming 2026-11-02, sessions 10-29_ccab9cfb, 10-30_d8dfe031)

Ryan, 10-29: "All these headlines are so fucking long. Are you sure you're using my headline skill?" His ran 7 to 9 words; mine ran 15 to 22.

1. Before any headline round, open `strategist-references/swipe-learnings.md` HEADLINE FORMULAS and the offer's research brief keyword bank (`offers/<slug>/RESEARCH-BRIEF.html`, the nouns she types ranked by count). Name both files in the reply before the first headline.
2. 7 to 12 words. Count them before Ryan sees them; a 13-word headline does not go in the reply.
3. The first 3 words carry a top-counted keyword from that bank. The first 5 words read alone still sell the crowd.
4. One device per headline (one quoted word, or one authority, or one number). Never two.
5. One option is always the live control's shape with the new angle's words poured in.
6. A headline is not a hook: no first person, no story line, never written from the ad's own lines. It is 0f and 0f2 below, cut to this length.

## THE VICIOUS GATE (from Ryan's "Polite to VICIOUS" teardown deck, ~/Desktop/Ad Feedback Deck/. Run BEFORE the checklist. This is the grading engine; the checklist is just compliance.)

Ryan's six patterns, from his own live teardowns. Every hook and body gets torn down against them the way he would do it, in his voice ("Not vicious enough. Doesn't slap. First words have to hit faster."):

1. **VICIOUS BEATS POLITE.** Hooks slap, not whisper. His revisions from the deck: "My kids are the reason my legs look disgusting." / "My ex-husband told me my legs look like cottage cheese left out in the sun." / "My dermatologist said my dark spots were permanent... now I'm laughing in her face." / "My knees were so bad I couldn't get up off the toilet without holding the wall." The ugly thing gets said in the ugliest true words the buyer herself uses. Humiliation named out loud, vindication with teeth. If a hook is comfortable to read at a dinner party, it's polite, and it's dead.
2. **REALISM BEATS POLISH.** Raw beats staged, in copy too: real numbers, real places, minor imperfections, spoken rhythm.
3. **RULE OF ONE.** One pain point per ad. Never stack sagging + wrinkles + hollow + lines; pick THE one and drive it through everything.
4. **NO DISCONNECT.** What the hook promises is what the body pays and what the image shows.
5. **QUALIFY FAST.** Specific in the first 5 words.
6. **MATCH AUDIENCE TO CLAIM.** Older claim, older woman; the narrator's age, words, and world match the buyer exactly.

**The kill ratio:** draft 15+ hooks minimum, tear each one down against the six patterns, deliver only the survivors (6-8). If a hook survives untouched, it wasn't torn down hard enough. Never deliver the first draft of anything.

## Pre-delivery checklist (run on EVERY ad before it hits chat; each line was a paid-for grade)

0. Hook is a PRESENT-TENSE AFTERMATH: the transformation already happened and the world is reacting ("People keep asking if my Grandson is my BABY", "Look at my face now"), or the reader's own symptom is said to their face ("You stand at the toilet for two minutes..."). A hook that sets up a story without paying anything ("...my sister finally said the thing nobody else would") is a movie trailer, not a hook, and it is DEAD. Graded 2026-08-05.
0b. CAUSAL CHAIN LIVES INSIDE THE HOOK (Ryan, 2026-08-05, round 2): every logical link the reader needs must be STATED, never inferred. "A woman at church asked if I was dying... I'd lost 52 pounds" failed because the middle link (my face got gaunt) lived in my head: reader asks "what does 52 lbs have to do with dying?" Fixed shape: "I lost 52 pounds... and my face got so GAUNT a woman at church asked my husband if I was dying." Cause -> visible effect -> reaction, all on the page. Run this check on every hook: can a stranger trace every step without guessing?
0c. FAILED SOLUTIONS = THE MOST COMMON REMEDIES for this exact symptom, ranked by how many buyers actually try them (Ryan, 2026-08-05: "collagen powder in the coffee is very random"; same law as the MOFO zinc-pills grade in ryan-voice.md). Ask "what are the top 3 things a buyer with THIS symptom tries first" and use those, in her words.
0c2. WORD PROVENANCE: emotional words in hooks come from the buyer's OWN FIRST-PERSON speech, never from a professional describing the buyer (Ryan caught "gaunt", which came from a dermatologist quoting patients; the women themselves wrote "deflated", "hollowed out", "sunken"). When citing customer language, check WHO said it into the record.
0d. NAME EVERY REFERENT CONCRETELY, even in hooks: "cream list" graded vague. It's "a dermatologist's Top 5 list" or "the #1 cream on a dermatologist's list", never a compressed noun mash a stranger can't picture.
0e. COMPRESS HOOKS to the shortest version that keeps qualify + causal chain + scene (Ryan, 2026-08-05: 21 words graded "too long"). When the drug/product name already implies the backstory, drop secondary numbers ("I lost 52 pounds on Ozempic and..." -> "Ozempic made my face so HOLLOW..."). Target: under ~15 words; his all-time winners run 6-12.
0e0. THE REVERSAL IS A SCENE, NEVER A CLAIM (Ryan, 2026-08-05: "I erased every bit of it" graded "just a direct claim... vague"). The transformation half of a hook must be a SPECIFIC VISIBLE REACTION someone has to her (hairdresser swears she got a facelift, sister demands the surgeon's name, med spa girl chases her into the parking lot, stranger thinks her grandson is her son, makeup counter girl guesses 48 when she's 61). "I fixed it / I erased it" is an autopsy of the fix; the reaction is the proof AND the curiosity.
0e0b. GLP-1 WORDING MIX (Ryan, 2026-08-05 + market data; REPEATED VIOLATION 2026-08-05, structural fix): by 2026 tirzepatide (Zepbound/Mounjaro) leads new weight-loss scripts, so many buyers are NOT on Ozempic, and the brand word can flag/spike CPMs. THE STRUCTURAL RULE: the PRIMARY/default text of every deliverable uses generic wording ("the weight loss shots", "GLP-1", "GLP-1 face"); "Ozempic" appears only in explicitly DESIGNATED tester ads (about 2 per batch), named as such in the file. Never present an all-Ozempic lineup; the failure mode is labeling Ozempic "version A" and then always presenting the A set.
0e0c. MOBILE PARAGRAPH GATE (Ryan, 2026-08-05: "most of our traffic is on mobile... break it up"): the discovery beat (trusted source + article + skip-to-#1) keeps getting written as one 4-line block; it must be broken into one-thought lines like everything else. Check EVERY paragraph at phone width; anything over ~2 short lines splits.
0e1. EVERY HOOK TEASES THE TRANSFORMATION (Ryan, 2026-08-05: a bank of pure pain-aftermath hooks graded "kind of weak... none of them tease transformations"). The fire shape is pain + reversal in ONE line, his Menopause doc DNA: "Menopause gave me these deep wrinkles in six months. Then I erased them." The wound alone is an autopsy; the erasure is the click. Also: name the angle's actual DAMAGE in aging words (aged 10 years, wrinkles, sagging jawline, hollow cheeks) — for TPS the hook is about AGING and the cream that reverses it, not adjacent social awkwardness. And NEVER open with credentials ("I'm a dermatologist" graded "really dumb and weak"; hook-laws #6 says the same) — lead with the shocking claim, credential later if at all.
0e2. NO SUBCULTURE DECODING in hooks (Ryan, 2026-08-05: "my church put me on the prayer list" graded "the most confusing thing I've ever heard"). If the hook's payoff only lands for someone inside a subculture (church prayer chains, niche rituals), it fails the 4th-grader rule no matter how vivid it is. The scene must explain itself to any stranger.
0e3. THE SAY-IT-OUT-LOUD TEST on every body line (Ryan, 2026-08-05: "Then the world started noticing" flagged as not how a woman talks). Narrator transitions, punchy copywriter fragments ("Correct. I'm not."), and speechwriter closes all fail. The reference register is his Hotter body: "I'm just standing there thinking is this actually happening right now."
0e4. THE SOLUTION NEVER GETS A PRICE (Ryan, 2026-08-05: "$40 fix sounds like an ad... I don't like giving away prices"). Failed solutions and villain quotes carry the price tags ($3,200 filler, $200 counter cream); the winning brand is only ever "costs almost nothing" (his corpus device) or a relative comparison. Never a dollar figure on the fix, in hooks or bodies.
0f. HEADLINES (Meta HL field) ARE ANGLE-SPECIFIC, never generic offer lines (Ryan, 2026-08-05: generic locked line "not related to this angle"; slogan-shaped "Losing Weight Shouldn't Age Your Face" graded "really bad"). Write them in his proven H1 formula: [authority/retailer anchor or scarcity] + (This) + ONE quoted keyword naming the angle's phenomenon ("Dermatologists Stunned by (This) 'Ozempic Face' Eraser", "Target Can't Keep (This) Menopause 'Wrinkle' Eraser in Stock"). The angle's name appears IN the headline. 0f2. FIRST 4-5 WORDS CARRY THE SOCIAL PROOF (Ryan, 2026-08-12; PROVISIONAL — wording not yet graded by Ryan, treat as strong guidance not law): mobile truncates headlines, so words 1-5 should be a complete social-proof thought on their own ("Target Shoppers Are Buying (This)...", "Dermatologists Stunned by New..."). The proof anchor (retailer/authority/crowd + mass action) goes first; avoid opening on (This)/The/New/product name. But vary the anchor — Target-first every time reads formulaic; crowds (women over 60, retired nurses, Facebook groups) and threatened gatekeepers (injectors, estheticians) are anchors too. WORD VOLTAGE: one visceral reaction word beats a mushy verb phrase ("Stunned" > "keep getting asked", Ryan 2026-08-12). TPS data: front-loaded proof $259k at $92 blended CPA vs late-proof $69k at $101. Truncation test: read only the first 5 words out loud; they should already sell the crowd.
1. Hook names the exact problem (the words the buyer uses, e.g. "man boobs") inside the first 5 words, plus curiosity. No decoding, no paradox puzzles.
2. Hook passes believability: claims in could-be-real range, one humble checkable detail beats stacked brags.
3. No-VSL funnel = product NAMED, but only in the back half: after struggle + discovery, with the product's weirdness as the skepticism beat. Never in the opening.
4. Every story beat survives "would this actually happen / would he actually say that."
5. No paragraph over 3 short lines. One thought per line.
6. Native stories follow strategist-references/native-story-framework.md structure exactly (situation, failed solutions, trusted-source discovery, skepticism, short-para mechanism, progressive timeline, drama, soft P.S.).
7. No em dashes. Simple direct language, zero jargon.

## Rules

- Compliance from OFFER.md. No em dashes anywhere. Plain-text deliverables.
- Never write into `state/`, `references/`, or `.exodus/`. Never run `npx exodus`.

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
