---
name: strategist-netnew
description: The agency creative-brief filler of the Strategist pack. Ryan leads the agency-side creative strategy team; he dictates the idea for a net-new (or iteration) and this skill shapes it into a paste-ready brief for the form at brief.skyhouse.ai. It does NOT do research by default — the research brief is a separate upstream process; this skill only pulls data when Ryan explicitly asks for help finding angles or proof. Invoke when the user addresses the strategist about an agency creative brief, e.g. "strategist, brief this up for testo: [idea]", "strategist, net new for SCR", "strategist, turn this into a brief", /strategist-netnew, or when the strategist hub routes here. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never runs npx exodus, never touches ad accounts, never submits the form. If the user says "exodus", this skill is not for them.
---

# Strategist Net-New: Ryan talks, the brief comes out formed

One job: take Ryan's idea and turn it into a filled creative brief matching Fernando's form at **https://brief.skyhouse.ai/**, field for field. Ryan pastes and submits it himself.

**Do not research unless asked.** The research brief is a whole separate process — `strategist-research-brief`, which produces `offers/<slug>/research/` (per-source docs + BRIEF.md). It runs upstream, on its own cadence. If the offer has a BRIEF.md, read it for persona/proof/receipts instead of deriving anything; if it doesn't, Ryan brings the idea and you bring the formatting and a quality check.

## Required reading before any hook goes in a brief (Ryan, 2026-09-09)

`strategist-references/aggression-prompt.md` (his verbatim "hardest true version, first try, every option" order) and `strategist-references/hook-laws.md`. Hooks are the part of the brief he grades hardest; they get the rounds.

## The default flow

1. **Listen.** Ryan brain-dumps the idea — voice-note style, messy is fine. Don't interrupt with questions the dump already answers.
2. **Shape it** into the form using `.claude/skills/strategist-netnew/BRIEF-template.md` (mirrors the form field for field; the form is WIP — if they drift, re-read the form and update the template).
3. **Fill the gaps from what he said**, not from research. If a required field is genuinely missing (persona, proof, lander call, confidence), ask in one short batch — don't go pull data to answer it yourself.
4. **Quality-check** against the hard rules below. Flag anything that would get kicked back (no proof, a five on confidence, product-aware creative on a VSL funnel).
5. **Deliver**: save to `offers/<slug>/briefs/` (create the folder stub if needed), print the brief in chat for Ryan's review, then FILL THE LIVE FORM IN RYAN'S REAL CHROME (claude-in-chrome tools, not the in-app Browser pane) so he can see it, review it, and click Submit himself. HARD RULE (Ryan, 2026-08-25): briefs are always done in his Chrome; Claude never submits. Form-filling notes from the first live run: the form is React (use native value setters + input/change events), all three order types start ON (toggle off what you don't need and re-check the "Your order:" line), hook inputs appear only after the AT count is set, target fields by placeholder never by index (re-renders shift indices), pasting a link in Reference + Enter creates a chip (check for duplicates), and verify every section visually by screenshot before handing off.

What happens after submit (context, not your job): Fernando's translator feeds the bots -> copy variants -> creative team via Leah's ClickUp automation -> back to Ryan for approval -> live. Assets back in 1 business day.

## Help mode — only when Ryan asks

"What should I run for X?", "find me proof for this", "what's died on this offer before?" — then and only then, pull:

```bash
python3 tools/perf/pull_redtrack.py --days 7   --filter <CODE> --out <scratchpad>/rt-<code>-7d
python3 tools/perf/pull_redtrack.py --days 365 --filter <CODE> --out <scratchpad>/rt-<code>-365d
```

Facebook only — exclude anything matching GG / Google / GDN. **7 days = what's live. 365 days = what's been tried.** Never claim "never tested / doesn't exist" from the short window (hard rule after the Testo lander miss, 2026-08-10 — squeezes and top-5s had been tested and killed months back). Campaign names carry launch dates (MM.DD.YY). Check alternate names before any "doesn't exist" call: client name vs offer name (Enclave = client, Akka = offer).

If `offers/<slug>/` has research or a PLAN, read that first. When the ask is angles FROM THE VSL (the foods lander / Coke vs Pepsi kind of find), run `strategist-references/vsl-gem-mining.md` (PROVISIONAL) on the full VSL script, and read the offer's latest `research/VSL-GEMS-*.md` first so nothing gets re-pitched. For competitor questions, route to `strategist-research` (Atria). When ranking angle candidates for Ryan, use Bankers / Bridges / Bets and tag each with its nearest form angle family so the override is a one-word pick.

## Offer names (RedTrack code ↔ form dropdown)

| RedTrack | Brief form | Note (2026-08-10) |
|---|---|---|
| TPS | Wrinkle-TPS | Scaled, net-news stocked |
| SCR | Age-SCR | Healthy |
| RJV | Hair-RJV | Healthy |
| TestoGreens | Testosterone-TestoGreens | CRITICAL, limited runway |
| SlimSculpt | Cellulite-SlimSculpt | Struggling |
| TFC | Skin-TFC | Maintenance, no new ads |
| DermaBright | DarkSpots-BRT | Maintenance, no new ads |
| ReActivate | Skin-ReActivate | Tiny relaunch spend |
| Akka | (not in form yet) | Client = Enclave. Research brief first |

Statuses drift — the week plan in `offers/agency/WEEK-*.md` is the living view.

## The 2026-08-11 redesign (Ryan + Fernando call, recap in Gmail from fathom.video that day)

The form now follows Creative Diversity Decoded's own order: **Outcome → Sub-outcome → Facets → Persona**. That means a plan built on that framework (see `strategist-plan`, and `offers/<slug>/PLAN-VISUAL.html` for the Akka model) maps into the brief field for field, with no translation step. Changes:

- **New required fields**: Outcome (the primary goal, e.g. "Longevity"), Sub-outcome (the specific tangible result, e.g. "Stay out of a nursing home"), Facets (the beliefs and past experiences she carries, e.g. "Keto didn't work", "My metabolism is broken").
- **New optional fields**: Angle (a specific strategic approach), Hooks (pre-written copy to steer the AI; must pass `hook-laws.md` and be checked against `hook-bank.md`), Budget justification (optional for senior strategists).
- **Renames**: the old "Style" field is now **Format**, and Format is free text so custom formats work ("Whiteboard video", "Scene photo + confession caption").
- **Lander notes** accepts a Loom link for detailed instructions.
- **Ryan's workflow**: he dictates the idea as a voice note, this skill shapes it into the fields, he pastes and submits. Write every value in speakable plain sentences.
- Fernando is shipping these changes to the live form; until then the live page shows the old fields. Fill the new template regardless and paste field by field.

## Form facts that shape the output

- The brief is an **order + idea + proof, not copy**. Production writes all ad text, headlines, scripts. Exact hooks Ryan insists on go in Special notes only.
- **Proof is a hard gate** — one ad receipt + market receipts, or it gets kicked back. Iterations cite the parent's numbers.
- **Confidence 1–10, "don't bring fives"** — the why must point at the proof.
- **Lander always present** ("landers are the retainer, there is no none"): existing, or new with style Top 5 / Long form / Editorial / Listicle / Product + the promise.
- At least one **reference artifact** (link or file, not a description).
- Awareness defaults to problem aware.
- Only optional field: **angle family override** (Vindication, Guilt, Future warning, Cautionary tale, David vs Goliath, Permission granting, Peer comparison, Wrong question, Conspiracy). Skip = production picks.

## Hard rules (check every brief)

- **No em dashes.** Anywhere. Ever.
- **VSL funnels get NO product-aware creative.** Every ad sells the click into the video: no brand name, bottle, price, offer, guarantee, benefit bullets. Unaware / problem-aware / solution-aware only.
- **Simple direct beats clever.** One thought per line. No jargon in the brain dump either — the translator feeds bots, not poets.
- **Substantiation must be named** in the concept dump or the AI invents it. Cure logic arrives via a credible source, never lazy self-research.
- **Lander congruence is a hypothesis, not a default** — matching lander language to the ad angle has lost in testing (TPS GLP-1 wrinkles).
- Google never enters a read. Bid-cap context before any scaling claim.

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
