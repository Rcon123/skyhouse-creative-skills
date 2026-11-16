# Video Ad Script + Creative Brief Writer

Turn an offer + an audio/script direction into a scene-by-scene shot list ready to hand to a video editor. Works for cartoon ads (Pixar 3D, hand-drawn), live action, talking-head, slideshow VSL openings, music-driven, or silent-with-text.

Audio source varies. Sometimes it's a song. More often it's a VO script, narration over visuals, on-camera dialogue, or text-on-screen with music underneath. The process is the same: sync each beat of the audio (or the on-screen text) to a specific scene.

This file captures the process Ryan and I built hand-in-hand. The rules came from real iteration on real ads — don't shortcut them.

---

## WHEN TO USE

- Ryan provides a song/lyrics/VO and an offer, wants a shot list
- Ryan wants a creative brief for a video editor
- Adapting a reference video style to a new offer

## STEP 1 — INPUTS YOU NEED

Confirm before you start. If any are missing, ask.

1. **The audio/script** — VO script, narration, song lyrics, on-camera dialogue, or just the captions if there's no audio. Confirm what kind it is.
2. **The offer** — what's being sold, the price, the CTA destination
3. **Target audience** — age range, gender, primary pain/desire
4. **Style direction** — Pixar 3D, hand-drawn, live action, motion graphics. Reference an existing aesthetic if possible (Klaus, Up, RYZE Mushroom Coffee, etc.)
5. **Reference video (if any)** — if Ryan shares one, study it carefully. If it's a video file, use ffmpeg to extract a frame grid (`ffmpeg -i input.mp4 -vf "fps=1/4" frame_%03d.jpg`) and Read the frames.
6. **Hook angle** — problem-led shock vs benefit-led aspirational. Match the audio's energy (or the offer's positioning if no audio).

## STEP 2 — STUDY THE REFERENCE (IF PROVIDED)

If Ryan gives a reference video, extract frames and analyze:
- Aesthetic (Pixar 3D? Hand-drawn? Live action?)
- Pacing (how many distinct shots per minute)
- Character consistency (one mascot? Multiple?)
- Hook structure (what's the opening?)
- Where does it pivot from benefit to problem (or vice versa)
- Caption/text style
- Product/brand integration

Don't guess at the style — get the actual frames in front of you.

## STEP 3 — CORE PRINCIPLES (non-negotiable)

### 3.1 FIRE HOOK in the first 3 seconds

The single most important rule. The hook must:

- **Be SINGLE-FRAME readable.** No sequence to decode. If the viewer needs to watch a character do A, then B, then C to understand the hook, you've lost them.
- **Be INSTANTLY clear about the topic.** GLP-1 ad? GLP-1 vial visible. Weight loss? Body transformation visible. Pharmacy bill? Bill visible with the number on it.
- **GRAB BY THE THROAT.** Two flavors:
  - **Shock hook** (problem-led ads): A specific visceral moment of pain/dread. Examples: woman in pajamas sitting on the curb with a $1,247 GLP-1 bill in her hand. Specific number visible on the paper.
  - **Aspirational/visual-joke hook** (benefit-led ads): A specific transformation moment that's instantly readable. Examples: woman holding her old jeans with the waistband sliding past her hips (Pixar physics — they're way too big).
- **Pair with the first beat** of the audio/script. Visual + audio land together. If there's no audio, the on-screen text or caption is the "first beat."

What does NOT grab:
- Static character smiling at camera (charm, not throat-grab)
- Walking sequences that need time to unfold
- Confrontational text over a still character (feels like a billboard, not an ad)
- Surreal jokes that need interpretation (giant vial on a flatbed truck — confusing)
- Eye contact alone (no motion = scroll past)
- Pretty/aspirational lifestyle without a specific WTF moment

### 3.2 Every Shot SLAPS

No mid scenes. Every shot needs ONE of these:

- Visual gag (Pixar physics, cartoon comedy)
- Emotional punch (tears, husband stare, granddaughter awe)
- Shock reveal (price slam, transformation, number drop)

Failure mode: "Linda doing thing" with no specific punch. Examples that don't slap:
- Linda holding a vial and breathing (quiet, no payoff)
- Linda walking past a pantry (mid)
- Linda buttoning jeans in a mirror (small)
- Linda scrolling her phone (passive)

Upgrade each mid moment with a specific visual hit:
- Vial held to sunrise light like a Disney "I have decided" moment
- Pantry walk-past replaced with food emojis swarming her head and dissolving
- Jeans button moment combined with scale drop + ring spinning loose into a montage

### 3.3 Visual MUST match the audio/script beat

If the VO says "she takes her first shot," the visual shows her taking the shot, not her at the beach. Disconnect = viewer confusion.

Exception: a strong HOOK can show the end-state during the opening line (e.g., transformed body during "if a woman takes her first shot..."). The audio rewinds the journey, the visual previews the win.

If there's no audio, the on-screen text/caption serves as the beat — the visual must match what the text is saying at that moment.

### 3.4 Editor feasibility — keep it buildable

Avoid:
- Sentient objects unless the joke is universal (cake chasing a woman = confusing; food emojis as flies = readable, well-established trope)
- Tidal waves of clothes flying out of closets (complex animation)
- Magical jeans buttoning themselves up her legs (unclear what's happening)
- Surreal scale jokes that need cartoon physics to read (giant vial on a flatbed truck)
- Wedding rings landing in wine glasses with perfect dings (specific staging that confuses)

Prefer:
- Standard motion graphics tropes (text slams, stamps, hearts/likes flying off phones, swarms of small icons around a character's head)
- Clear character actions (waving "no thanks," buttoning easy, lifting a child)
- Cinematic wide shots for payoff moments (beach sunset)
- Numbers slammed full-frame for price reveals

### 3.5 Match audience to character

50+ ad → 56-year-old character. 30-something ad → 32-year-old character. Older the audience, older the avatar (within reason). Same applies to lifestyle scenes — 50+ women dance at daughter's weddings, play with grandkids, drink wine on porches. 30+ women drink matcha at brunch. Get the lifestyle right.

### 3.6 Single mascot character throughout

The viewer locks onto one face. Don't switch protagonists mid-ad. If you need other characters (husband, friend, grandkid), they orbit the main mascot.

## STEP 4 — DRAFT THE HOOK FIRST

Before shotlisting the body, write 3-5 hook options. Each one a single-frame description.

Examples that worked:
- "Linda at her mailbox in pajamas. Rips open the GLP-1 bill on the curb. $1,247 visible on the paper. Knees buckle. She sits down on the curb, stunned." (shock)
- "Linda in her bedroom in her old jeans. The waistband is sliding past her hips because they're way too big. She's clutching them with both hands, laughing." (aspirational visual joke)

Get Ryan's pick. Build the rest of the shot list around the chosen hook's energy.

## STEP 5 — BUILD THE SHOT LIST

Match each beat of the audio/script to a scene. Group related beats into single sustained moments rather than micro-cutting.

For each shot:
- **Shot number + name + timecode**
- **Visual description** (clear, single read, editor-feasible)
- **Audio pairing** in italics (lyric / VO line / on-screen text)

Target pacing: roughly 4-5 seconds per shot. For a 90-second video, 13-18 shots is the right zone (the RYZE Mushroom Coffee reference clocks ~23 shots in 97 seconds, fast cuts). Talking-head ads can hold longer shots — adjust to format.

## STEP 6 — AUDIT EVERY SHOT

Before delivery, audit each shot against three filters:

1. **Does it SLAP?** Visual gag, emotional punch, or shock reveal? If not, redesign.
2. **Is it INSTANTLY readable?** No inference needed. If a viewer needs more than 1-2 seconds to understand what's happening, simplify.
3. **Can an editor BUILD this?** Avoid sentient objects, complex physics, magical animation. Stick to standard tropes the editor will recognize.

If a shot fails any filter, redesign or cut.

## STEP 7 — DELIVER

Format for the editor:

```
# [AD TITLE] — SHOT LIST

**Style:** [animation/aesthetic]. Vertical 9:16. [Lighting note].
**Character:** [Name, age, look]. Same character every shot.

---

**SHOT 1 — [NAME] (0:00–0:0X)**
[Visual description.]
*Audio: "..."* (or *VO:* / *Caption:* / *Lyric:* as appropriate)

**SHOT 2 — [NAME] (0:0X–0:XX)**
[Visual description.]
*Audio: "..."*

[etc.]
```

End with a brief note flagging anything the editor might need clarification on (custom characters, signature shots, etc.).

---

## PROVEN STRUCTURES

### Structure A — Problem-led / Cost-trap

Use when the audio/script narrates a problem or trap (e.g., the GLP-1 debt anthem).

1. **SHOCK HOOK** — visceral problem moment (e.g., woman with $1,247 bill on the curb)
2. **Trap beats** — each lyric about the cost matches a specific cost-trap visual (vial in car costing more than the car, can't afford to take her dose, dress no longer zips)
3. **Solution reveal** — phone glow + ranking + $119 slam
4. **Through-line callback** — earlier "trap" object now resolved (dress zips again)
5. **Cinematic payoff** — wide shot of transformation (beach sunset)
6. **CTA slam**

### Structure B — Benefit-led / RYZE-style

Use when the audio/script lists benefits in sequence (the GLP-1 benefit anthem mirroring RYZE Mushroom Coffee, or any VO that walks through a transformation over time).

1. **ASPIRATIONAL HOOK** — visual joke or transformation evidence (old jeans falling off)
2. **Benefit beats per lyric** — each lyric matches one specific lifestyle moment (smaller plate, walks past dessert, grandkid spin, husband stare)
3. **"Now here's the problem" pivot** — single visual establishing the cost trap (three pharmacy clerks handing huge bills)
4. **Solution reveal** — ranking + price slam + guarantee stamps
5. **Cinematic payoff + CTA slam**

---

## COMMON FAILURE PATTERNS

Run-down of what to avoid (each one caught in real iterations):

- **Sequence hooks** — anything requiring 3+ seconds to read. Static images with motion in second 1.
- **Generic character smiling** — charm, not throat-grab. Need specific WTF moment.
- **Confrontational text-over-still** — feels like a billboard, not an ad. Pair text with a hot visual.
- **Sentient food / objects** (cake chasing) — confusing without setup. Use established tropes (food emojis around head, money flying out of purse).
- **Disconnect between visual and lyric** — if the lyric is about cost, don't show the beach payoff yet.
- **Showing syringes** — use vials. Syringes feel medical/clinical/scary.
- **"Click at top"** — always "click below" (where the CTA actually is).
- **Quiet introspective moments** without emotional payload (Linda holding a vial breathing) — every shot needs a hit.
- **Mismatched audience** — slim 30-year-old character in a 50+ ad.
- **Over-decorated graphics** ($99 banner exploding into fee-tag swarm) — confuses. Use simple text slams.
- **Tidal-wave-of-clothes / flying-jeans** — too magical, breaks suspension.
- **"30 day" specific guarantee terms** — say "money back" without committing to specific days (Ryan's offers vary).
- **Husband-coffee-mug-shatter hook** — requires sequence to read. Mid as opener.
- **Wedding-ring-into-wine-glass-with-ding** — too staged, distracts from the point.

## COPY GATE FOR SPOKEN-DIALOGUE SCRIPTS (PROVISIONAL, 2026-08-24, from the TPS call-in session — Ryan grades wording)

When the script is spoken copy (call-in show, podcast, interview, talking head), the shot-list rules above are not enough. Before drafting a single line, read:
1. `strategist-references/hook-laws.md` (incl. cumulative-feedback protocol) — hooks qualify in the first words, name the body part, never tease the article, spoken-discovery voice.
2. The Fire Video Ad Scripts prompt in `strategist-references/ryan-fire-prompts-2026-08-18.md` — 5 hooks + 1 body format, voice checklist, Top 5 structure, social proof density.
3. `strategist-references/feminine-voice.md` for any female speaker — kitchen-table test, every line carries a hit, clarity gates (every referent named, number one named three times).
4. `.claude/skills/talk-like-a-human/SKILL.md` (Ryan's own "write like a human being" lesson, 11-03; REQUIRED for every spoken or story line): the Benny paragraphs are the bar, 12 to 35 words per paragraph, connectives in every sentence, the feeling said out loud, the hardest fact right after the discovery, no fragments for punch, no paragraph over 40 words. Run `python3 tools/copygate/human_check.py <file>` before he sees it.

Failures this gate exists to prevent (all graded in one session): mechanism explained early or at length (max 1-3 lines, late, riding inside a feeling); social proof replaced by science; vague referents ("numbers are down", "the full ranking" — of what? for whom?); polite radio-drama dialogue instead of a real woman talking; CTA without the what + what's-in-it-for-me spelled out.

---

## STEP 8 — RECURSIVE IMPROVEMENT

After each ad, update this file with new learnings:
- New failure patterns encountered (add to "Common Failure Patterns")
- New successful visual moves (add to proven structures or principles)
- New editor feasibility constraints (add to 3.4)
- New audience/lifestyle insights (add to 3.5)

The rules get richer with each run. Don't restart from scratch — build on what worked.
