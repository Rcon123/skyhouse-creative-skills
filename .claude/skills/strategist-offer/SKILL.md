---
name: strategist-offer
description: Intake for the Strategist pack, add a new offer to offers/ or update an existing one with new material. Invoke when the user addresses the strategist and wants an offer created or its inputs changed, e.g. "strategist, add a new offer", "strategist, new offer, here's the buyer brief and VSL", "strategist, update <offer>, here's the new advertorial", /strategist-offer, or when the strategist hub routes here. Takes whatever the user has (buyer brief, VSL script, advertorials, landers, links, notes), files the raw material verbatim under offers/<slug>/inputs/, distills it into OFFER.md, and stubs PLAN.md so the planner can pick up. Never blocks on missing inputs, it records gaps as open questions and moves on. Planning-only pack: never generates creative, never runs npx exodus. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic "save this brief" / "organize my offer docs" requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus", this skill is not for them.
---

# Strategist Offer: intake

Get the offer's raw material filed and distilled with the minimum of questions. One conversation, one folder, done.

---

## New offer flow

1. **One-shot ask.** In a single message, ask for:
   - The offer's name.
   - "Paste or point me at whatever you have: buyer brief, VSL script, any advertorials or landers, links (ad library, sales page, competitors). Give me what exists, skip the rest."
   - Does this offer map to an Exodus brand? (slug or "none"; run `npx exodus brand list` read-only ONLY if the user is unsure)
   - Compliance red lines, if they are not evident from the material.
2. **File raw material verbatim** into `offers/<slug>/inputs/`, one file per artifact: `buyer-brief.md`, `vsl-script.md`, `advertorial-1.md`, `advertorial-2.md`, `links.md`, `notes.md`. Never edit or summarize inside `inputs/`.
3. **Distill OFFER.md** from the template at `.claude/skills/strategist-offer/OFFER-template.md`. Distill means compress and organize, never copy-paste dumps. Pay special attention to:
   - The mechanism section: capture the UMP (problem behind the problem) and UMS (unique solution mechanism) in plain language (see `strategist-references/concepts-and-angles.md`).
   - Compliance red lines: what can NEVER be claimed. These flow into every exported brief later.
   - Proven angles: anything already known to work seeds the grid's winner cells.
4. **Stub PLAN.md** with only the Status block: Stage `intake`, Exodus brand, today's date, Next action "map segments (strategist-segments), then plan".
5. **Hand off.** Close with: offer is in, say "strategist, map segments for <name>" when ready (or go straight to "strategist, plan <name>" if segments already exist).

Missing inputs never block. Log them under Open Questions in OFFER.md and move on.

## Update flow

When the user brings new or revised material for an existing offer:
1. Append the new artifact to `inputs/` (new numbered file; never overwrite raw history).
2. Re-distill only the affected OFFER.md sections.
3. Flip PLAN.md's Next action to "refresh plan, inputs changed" and update Last touched.

## Rules

- Slug: kebab-case of the offer name (e.g. "Prostate Flush" -> `prostate-flush`).
- Never write into `state/`, `references/`, or `.exodus/`.
- No em dashes anywhere in output. Hard rule.

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

Offer-setup addition: `offers/<slug>/LANGUAGE.md` is created with OFFER.md, seeded from the VSL transcript and the client's top ads (`## Their words`), and `## Never` starts empty. No ad or page is written for an offer without it.
