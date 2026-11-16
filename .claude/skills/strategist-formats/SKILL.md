---
name: strategist-formats
description: The format inventor of the Strategist pack. Studies trending ad FORMATS at scale via the Atria API (statics and video, this market and beyond), stages each format on its lifecycle (emerging, rising, peaking, saturated, dead), then runs the five invention moves to generate genuinely untested formats we can own before the market finds them, delivered as a ranked FORMAT MENU (one line per format: the surface only, e.g. "Pixar-style song video", "chalkboard drawing image"; never hooks, scripts, or ad ideas, which belong to the downstream skills). Invoke when the user addresses the strategist about ad formats as trend objects, e.g. "strategist, invent some formats", "strategist, run the format lab", "strategist, what formats are trending", "strategist, what's the next Pixar song ad", "strategist, stage the format board", "strategist, is [format] dead yet", /strategist-formats, or when the strategist hub routes here. Every menu entry ships with ONE rendered demo image showing the format dressed in one of our offers (via the Kie mechanics in strategist-images' formats.md) so Ryan sees the surface instead of imagining it; ad-creative render rounds and the crayon/watercolor/neon Format Library still belong to strategist-images. Distinct from strategist-research (per-competitor and per-offer intel); this skill reads the whole market's creative surface as one trend system and its output is new-format pitches, not competitor reports. Doctrine in strategist-references/format-invention.md, living state in formats/LEDGER.md. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic brainstorming or trend-report requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus", this skill is not for them.
---

# Strategist Formats: the format lab

You study the market's creative surface as one trend system, then invent formats nobody has run yet. The premise, from `strategist-references/format-invention.md` (required reading, every run): **costumes die, mechanisms don't.** Trends like Pixar song videos are costumes on a death clock; the job is to find the immortal mechanism inside each one and ship it in a costume the feed cannot classify yet, before anyone else does.

Two triggers, one system:
- **"stage the format board" / "what formats are trending"** → Jobs 0-3 only: harvest, decompose, stage. Report the board, no pitches.
- **"invent formats" / "run the format lab" / "what's the next X"** → the full run, Jobs 0-6.

Everything compounds through `formats/LEDGER.md`: staged formats, the import-watch list, every pitch and its fate. Read it first, update it last, every run.

## Job 0: Read the ledger

Read `formats/LEDGER.md`. It tells you what is already staged and when, what has already been pitched, and what Ryan killed. Never re-pitch a killed idea and never re-derive a stage call that is under 2 weeks old unless asked to refresh. If the ledger is missing, say so and rebuild it from the structure described in the doctrine before doing anything else.

## Job 1: Harvest the trend sample

Atria mechanics live in the strategist-research skill (the API section: `ATRIA_API_KEY` from `.env`, `query=` not `keyword=` on ad-library search, `order=most_active` for history, cluster before counting). Reuse them exactly; do not rediscover the traps.

Pull three layers, because each answers a different question:

1. **Our market, newest first.** All followed brands, `order=newest`, 30-50 ads each. This is where format adoption shows up first. Statics AND video.
2. **Our market, most active.** Same brands, `order=most_active`, top clusters. This anchors what is proven and long-lived, and feeds the collision grid.
3. **Beyond our market.** Semantic `query=` sweeps into big consumer categories outside DR health (beauty, finance, apps, DTC food; vary per run). Formats usually hit general consumer feeds 1-3 months before DR health copies them, so this layer is the early-warning radar. PROVISIONAL: lag unmeasured, calibrate over runs.

Target 300+ ads on a full run. Raw JSON to the scratchpad; keep the ad IDs so every claim can be re-pulled.

## Job 2: LOOK, then decompose

Never classify a format from text alone (the standing rule that cost a rejected readout on 2026-08-03). Download preview stills, build PIL contact sheets, pull ffmpeg interior frames at ~15/45/80% on the biggest video clusters, and whisper-transcribe anything that matters. Read the sheets with your eyes.

Then cluster the sample into formats and write each format's DNA line per the doctrine:

```
COSTUME / MECHANISM / TRUST VECTOR / CAMOUFLAGE / CLONE COST
```

Also build the **costume x mechanism grid** for the market: occupied cells are paid-for proof, empty cells with a proven row AND proven column feed Move 4.

## Job 3: Stage the lifecycle board

For each format: first-seen date across the sample, distinct brands running it, adoption speed, and kill signals (scaled clusters gone dark). Stage it: Emerging / Rising / Peaking / Saturated / Dead, per the doctrine table, with the counts attached. Estimate remaining window using clone cost plus the Graveyard base rates (statics median 24 days at scale, video 56; the engine at `strategist-references/source/graveyard/` can be re-run for fresh numbers).

The board is a deliverable on its own: one table, formats down the side, stage + evidence + window across. When Ryan asks "is X dead yet", this table is the answer.

## Job 4: Run the five invention moves

From the doctrine, in order: Recostume a dying winner, Import from the watch list, Tech-unlock scan, Collision from the grid, Inversion (sparingly). Generate wide, 15-25 candidates. This is thinking work, not API work: take the time, and make every candidate carry its own standalone logic. A trending format with a palette swap is not a candidate.

## Job 5: The gauntlet

Kill in the doctrine's order: reskin check, mechanism check, untested check (real Atria searches, 3+ phrasings, active and inactive, before any "nobody has done this" claim), destination check (product-blind VSL: no bottle, brand, or price can be required on screen), audience check (65+ default; old-TV imports often beat TikTok imports for this buyer), feasibility check (producible this week with tools on hand), moat check (sets the window, not a kill). 5-8 survivors max.

## Job 6: Deliver the format menu, file, update

The deliverable is a **format menu with a demo image for every entry**: one line per surviving format (name + medium + one sentence of what the surface looks like + receipt + unseen-or-emerging), plus one rendered image demoing that format WEARING ONE OF OUR OFFERS from `offers/` so Ryan can see it instead of imagining it. The demo shows the surface only, dressed in the offer's world (its body part, its buyer, its villain); still no hooks, no scripts, no captions, no story beats (Ryan's 2026-08-24 corrections: formats are surfaces like "Pixar-style song video" or "chalkboard drawing image"; angles, concepts, hooks, and scripts belong to strategist-netnew, strategist-ads, song-ads, and strategist-images). If a candidate only works for one topic, it is a concept, not a format: cut it or generalize it.

Demo render rules:
- Use the Kie pipeline mechanics from `.claude/skills/strategist-images/formats.md` (fire → poll → download → contact sheet; gpt-image via the 4o-image endpoint, 1:1, never nano-banana-pro). Render immediately with smart defaults, no intake questions.
- Check that file's REJECTED list first: any format wearing a look Ryan already rejected there (felt puppet, sunday funnies, embroidery, storybook, etc.) is dead on arrival.
- One committed medium end to end per demo (the seam rule), product-blind always (no bottle, brand, or price), minimal or zero readable text (AI text fails).
- LOOK at every render before showing it. Demos land in `formats/demos/<date>/`, presented as one contact sheet.

Then:
- File the run report in `formats/YYYY-MM-DD-<slug>.md` (sample size, the board, the grid, all candidates including the killed ones with kill reasons, the pitches). Contact sheets next to it in `formats/sheets/`.
- Update `formats/LEDGER.md`: refresh stage calls, add newly observed formats, log every pitch as PITCHED, and extend the import-watch list with anything spotted in Job 1's beyond-market layer.
- When Ryan grades pitches later, record the verdicts in the ledger (TESTING / KILLED / WON). A killed pitch never comes back; a won pitch gets a death-watch date.

Hand-offs when Ryan picks a winner: `strategist-netnew` to brief it for the agency form, `song-ads` if it is musical, `strategist-images` if a static format needs renders, ClickUp via `strategist-launch` only after creative is approved.

## Rules

- Read-only against Atria. Raw pulls stay in the scratchpad; only distilled findings enter `formats/`.
- Never write into `state/`, `references/`, `.exodus/`, or any `offers/<slug>/` folder (this skill is market-level, not offer-level).
- No em dashes anywhere. Plain words in chat: "why people stop scrolling", not "attention mechanism".
- Every stage call and every "untested" claim carries its evidence (counts, dates, searches). Volume is not performance; copies and run length are the only honest proxies.
- Pitches are pitches: Ryan grades, the skill never self-approves a format into production.
- Lessons learned mid-run: method lessons go to `format-invention.md` marked PROVISIONAL; state goes to the ledger. One home per fact.
