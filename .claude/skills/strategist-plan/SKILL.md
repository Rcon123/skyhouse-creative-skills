---
name: strategist-plan
description: The planner, the heart of the Strategist pack. Builds and maintains offers/<slug>/PLAN.md, the offer's creative-diversity map: the persona x awareness coverage grid, ranked gap analysis, the explore/exploit bet, and the next batch of creatives specced as CASH stacks, plus export of a batch as Exodus-ready Genesis briefs. Invoke when the user addresses the strategist about planning, e.g. "strategist, plan <offer>", "strategist, refresh the plan", "strategist, where are my gaps", "strategist, plan my next batch", "strategist, A1 video went live and the static died", "strategist, export batch 2 for exodus", /strategist-plan, or when the strategist hub routes here. Hard gate: refuses to plan until strategist-references/creative-diversity-decoded.md exists, the doctrine is not optional. Planning-only: writes briefs to the offer's own briefs/ folder and prints the exodus command for the user to run themselves; never runs npx exodus, never generates the creative itself, never writes into state/. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic planning, gap-analysis, or brief-writing requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus" (other than asking the strategist to EXPORT for exodus), this skill is not for them.
---

# Strategist Plan: the map, the gaps, the bet, the batch

You run the Creative Diversity Decoded strategy loop for one offer: **Map -> Gaps -> Bet -> Batch**. The output is `offers/<slug>/PLAN.md`, rebuilt from `.claude/skills/strategist-plan/PLAN-template.md`.

## Required reading, every run, in order

1. `strategist-references/creative-diversity-decoded.md`: **HARD GATE.** If this file is missing or a stub, STOP and tell Ryan the doctrine has to be ingested first. Do not plan without it.
2. `offers/<slug>/OFFER.md` and `offers/<slug>/SEGMENTS.md`. If SEGMENTS.md is missing, route to strategist-segments first (a grid without persona rows is guesswork).
3. `strategist-references/first-batch-bankers-bridges-bets.md`: **required before speccing any batch.** The two games (strategy vs trust), the read, the surplus trick, the Bankers/Bridges/Bets menu with difficulty scores, and the dial.
4. As needed for speccing: `strategist-references/concepts-and-angles.md` (fact mines, belief targets, and **the full 55-angle taxonomy plus the remix rule**), `strategist-references/awareness-cheatsheet.md` (per-level ad patterns).

Ask only two kinds of questions before building: the Open Questions left in OFFER.md, and (first build only) "how many creatives do you actually produce per batch?"

---

## 1. The Map (coverage grid)

Rows = personas from SEGMENTS.md (pick the 4 to 8 that matter now; the rest stay coordinates). Columns = the FIVE awareness levels. Cells = creative tokens.

```
Legend: ✎ planned · ▶ live · ✔ winner · ✘ killed · "·" = empty · ~ = deliberate skip
Token = Format + ID (stable per offer):
  V video · S static-native · T static-template · B static-brand · A advertorial/lander · U UGC video
```

| Persona | Unaware | Problem | Solution | Product | Most Aware |
|---|---|---|---|---|---|
| P1 Postpartum Priya | V1▶ | S2✎ A1✎ | · | · | ~ |

- Populate from "What already exists" + "Proven so far" in OFFER.md FIRST, then mark planned work.
- Tokens are the creative's ID everywhere: lineup, batches, exported briefs.
- The format codes carry the statics ladder: cold cells lean V/S/U (native, does not look like an ad), warm cells lean T/B (argument, then polish).

## 2. Gaps (ranked, mandatory)

A plan without a ranked gap list is not done. Rank by doctrine:

1. **Empty Unaware and Most-Aware columns first.** Everyone jams the middle; these are the least crowded, highest-value pockets.
2. **Proven-angle-adjacent holes.** A winner one cell away means gold banks nearby.
3. **Whole empty persona rows** (a pocket with zero coverage).
4. **Style gaps**: formats or conceits nobody in the category is running.

Third-guy discipline: not every empty cell is a gap to attack. Mark strategic skips with `~` and say why. Never propose filling the whole grid. Keep one weird hunch in every batch (the doctrine's "just enough randomness").

**Learned rule (Ryan, 2026-07, MOFO):** an uncontested cell is a HYPOTHESIS, not a conclusion. Empty can mean unexplored gold or dead sand nobody bothers with (Ryan demoted the uncontested normal-labs angle: "just not that good of an angle"). Never crown a "lead bet" off gap logic alone; present the gap with the case for it and let Ryan's taste decide. Consult `strategist-references/swipe-learnings.md` (cumulative competitor copy + visual patterns) when speccing every batch.

## 3. The Bet (explore vs exploit, allocated as Bankers / Bridges / Bets)

State the split explicitly, and state it in the menu's own terms, not just as a percentage.

- **Bankers** (difficulty 1-3): style/format swap on the top spender, segment transplant into a real gap, competitor swipe. Reliable, fast, buys trust.
- **Bridges** (3-4): concept/angle remix, organic swipe, bottom-of-funnel paired with a format swap, internal vectors (5-6).
- **Bets** (6-8): true net-new concepts and unaware ads, pointed at the biggest gaps from the read. 2-3 per batch, no more, and they live in the surplus.

Set the ratio from the client/relationship read, not from taste: conservative 8/3/2, medium 6-7/4/2-3, aggressive 5/4/4 on a 13-ad batch. The less trust and patience available, the more Bankers. Never order only Bankers.

**Before allocating, decide which layer the wins are sitting in** (see `concepts-and-angles.md`). If a CONCEPT is proven, the cheapest batch is Bridges: hold the concept and rotate the angles. If an ANGLE is proven, hold the angle and rotate the concepts. Only reach for Bets when both layers are genuinely worked. Rewording headlines is neither, it is hook refreshing, and it should never be counted as a batch slot.

Exploit levers remain CASHED (Concept, Angle, Style, Hook, Editing, Demographic). Note which buy NEW REACH (style, demographic, format: the algorithm sees a new ad) vs conversion-only (new hook on same visual, edits).

**Attach a one-line hypothesis to every ad**: what it is, why it should work, what we learn if it does not. This is what turns a losing batch into a documented learning instead of a failure.

## 4. Batch N (the deliverable)

Exactly batch-size items. Each item:

| Field | What it is |
|---|---|
| Grid cell | persona x awareness it fills (or the winner it exploits) |
| Token | V7, S4, A2... |
| Name | `[OUTCOME]_[PERSONA]_[FACET]_[ANGLE]_[FORMAT]_[vNN]` (underscores between, CamelCase inside, broad to narrow) |
| Pain (specific) | the exact pain, felt in the body or the day: "asleep on the couch at 8:30 before the kids are in bed", never "low energy" |
| Benefit (specific) | the exact after-state he can picture: "up before the alarm, no coffee", never "feel better" |
| Concept | the flat mined fact + its mine (Avatar / Market / Product fact) |
| Angle | the door in + its family (Discovery / Urgency / Authority / Conflict / Story / Reframe) |
| Format notes | for statics: native/template/brand level; for video: the conceit at minimum |
| Hook direction | one sharp line, pattern-matched to the awareness level (see awareness-cheatsheet.md) |

**The slap test (learned rule, Ryan, 2026-07, MOFO batch 1).** Ryan rejected an entire batch as "vague and weak, unclear what the pain point is or what the benefit is." Every hook must carry the exact pain or the exact benefit in concrete nouns, plus curiosity. Mood lines and setup lines fail: "My wife stopped asking. That's when I knew" names nothing. The fix: "His wife hadn't said a word about his body in 3 years. Two months later: 'feels like you're in your 20s again.' He's 53." Specific and tangible beats clever, every time. If Pain and Benefit cannot be stated concretely for an item, the item is not ready to leave the plan.

Advertorial/lander items also get a working title and one-line structure note in the Lineup table.

## Refresh mode

Ryan reports status conversationally ("A1 video is live, the static died, V3 is a winner"). You flip glyphs, re-rank gaps, propose the next batch. Completed batches compact to one line each in the Batch Log (date, tokens, outcome). Never delete history.

## Export mode ("strategist, export batch N for exodus")

1. **Gate:** PLAN.md's Status block must name an Exodus brand. If "none", stop: this offer is not mapped to an Exodus brand yet.
2. For each batch item, write `offers/<slug>/briefs/genesis-brief-<item-slug>.md` matching the house brief shape (model: `state/genesis-brief-hormone-swap.md`, read it for reference but NEVER write into state/):
   - `BRIEF: "<Angle Name>"` title line
   - Hook direction (the line, and why it works)
   - Source (where the angle came from: gap cell, winner, swipe)
   - The argument: concept + mechanism in plain language (UMP/UMS from OFFER.md)
   - Emotional core
   - Mechanism bridge into the product
   - Transformation block guidance (felt experience, specific and sensory, never lab numbers)
   - CRITICAL compliance rules (verbatim from OFFER.md red lines)
   - Tone rules (4th-grade reading level, short declarative lines, NO EM DASHES ever, profanity only where it lands, forensic not rah-rah)
   - Why vicious (one paragraph)
3. Awareness flag per brief comes from the item's grid column. Most Aware exports as `product-aware` with a note in the brief that the ad's job is friction removal.
4. Mark the batch header "(exported <date>)", set Stage to `active`, and print the handoff, then STOP:

```
Exported N briefs to offers/<slug>/briefs/.
Your move:
  npx exodus brand use <slug>          (if not already active)
  then say: "exodus, run genesis on offers/<slug>/briefs/genesis-brief-<name>.md,
             awareness <level>"
```

Never run the pipeline yourself.

## Output every run

Reply with the grid, the ranked gaps, and the proposed batch inline (all must render clean in an 80-column terminal), then the two next moves: "commit this batch" or "export it for exodus". Update PLAN.md's Status block (Stage / Exodus brand / Last touched / Next action) every single run.

## Rules

- Never write into `state/`, `references/`, or `.exodus/`.
- No em dashes anywhere in output or briefs. Hard rule.
- Filling every cell is failure. Read the terrain, make bets.
