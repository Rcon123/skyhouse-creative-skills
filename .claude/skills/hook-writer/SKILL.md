---
name: hook-writer
description: Writes short cold Facebook ad hooks (the first line of a cold static or short ad) for one offer, gated by Ryan's five rules and a stranger judge. Invoke when Ryan says "hooks for <offer>", "write hooks", "more hooks", "hook round 2", "next round of hooks", or /hook-writer. Hooks only, no body copy, no research, no images. Story openers, yapper lines and headlines are other lanes, not built yet; say so if asked.
---

# hook-writer: short cold hooks, five rules, one gate

**Read only these.** `offers/<slug>/LANGUAGE.md`, the first 60 lines of `offers/<slug>/OFFER.md`, `offers/<slug>/ads/hooks/KEPT.md` (if it exists), `offers/_examples/short-cold-approved.md`, `tools/hooks/rules/short-cold.json`. Nothing else.
**Never open:** strategist-ads, hook-laws.md, hook-bank.md, any hook-bot or poe file, tools/check_hooks.py, memory notes about hooks. The gate rejects a file that cites them.

## The rules (the json is the law; this is the summary)
1. 6 to 12 words, 15 max.
2. One sentence. An ellipsis may join two beats. Never a period in the middle.
3. The first five words grab, super vicious: an ugly, physical or shocking thing, said the way she says it. A doctor, a test, a number or a setup in the first five words is a fail.
4. (retired 10-29) A hook may start with the good news. Six of the approved examples do: a refusal and an impossible result.
5. Draft 25 or more. Show 8 to 10. Star at least 2 as holy shit.
6. At most 3 of 10 with an ellipsis. The rest are plain sentences.
7. (retired 10-29, Ryan: 'get rid of the judge, it's breaking things') No stranger read. Write to the approved examples' bar yourself: a shocking act or an ugly noun she would never say out loud, a twist, something at stake. A relatable complaint is a 5.
8. (10-29) A hook never opens on the authority: no 43-year Vet, no Vet, no Doctor, no Dr. in the first words. The expert may speak later in the line.
10. (10-30, testing) Pack the line with the market's keywords (the drug, the body part, the fear, the price) as long as it still reads as one spoken line; capitalize the ones that pop.
9. (10-29) Plain spoken sentences. No clipped comma-splice fragments to fit the count; if it does not fit, cut the idea, not the grammar. Write the idea the way the doctor would say it out loud.
11. (10-30) Categories (Heartbreaking, Miracle, Betrayal, Unfair, Gross, Shame; 5 each) ONLY when Ryan asks for hook ideas with no angle given. When he hands you the idea, one flat list on that idea, no categories (Ryan: 'otherwise it becomes too confusing').
12. (11-02) A hook Ryan called weak is dead, never rewritten. The next round is 100 percent new lines. Liked = locked verbatim in KEPT.md, never a template: "vet stunned" twelve times (10-29) and "the vets keep asking who cleaned them" (10-27) were the same miss. The gate (SC-12) kills a line that repeats an earlier round of the angle, or opens on the same five words; the counts file says how many carried over and the rule is 0. (dreaming 2026-11-02, sessions 10-28_66850cc4, 10-29_ccab9cfb)
No em dashes. No words from the offer's Never list.

The approved examples are the standard. Before drafting, name what each one does (the taboo act, the impossible link, the ugly noun, the stake) and do THAT for this offer. Never their words. Name the thing she is ashamed of; a hook that avoids her shame is polite, and polite is dead.

## The loop
1. Need: offer slug, angle, who the reader is (one sentence). Ask once if missing, then go.
2. Write `offers/<slug>/ads/hooks/<angle>-r<N>.md` (N = next round for that angle):
```
---
offer: cloud9
lane: short-cold
round: 1
angle: labs
reader: woman, 62, wine every night, ALT flagged last month
sources: none
---
1. * Hook text
2. Hook text
```
25 or more. `*` marks a holy-shit pick. Use the Write tool, whole file.
The `sources:` line is exactly one of these two shapes, nothing else (the gate rejects prose, parentheses, bare file names; dreaming 2026-11-02, sessions 10-29_9bbc526f, 10-29_37715be0, 10-30_b1ae4676):
```
sources: none
sources: offers/<slug>/LANGUAGE.md; offers/<slug>/OFFER.md; offers/<slug>/research/BRIEF.md
```
Full paths from the workspace root, semicolon separated, only files under `offers/`.
3. BEFORE writing one word of the reply, every round, no exceptions: `python3 tools/hooks/judge.py nojudge <file>` (the judge is OFF since 10-29; this writes the stamp. If the judge is ever back on: `judge.py prompt`, a fresh agent, `judge.py stamp`), then `python3 tools/hooks/gate.py report <file>`. No login, no agent, no waiting on Ryan. Three of five Stop-hook fires were a reply written before this step (dreaming 2026-11-02, sessions 10-29_9bbc526f, 10-29_9970f3d2, 10-29_a90bed16).
4. Your whole reply is the report output, pasted as is: a plain numbered list of hooks with the `*` kept, no code fence, no header line. The counts ("32 drafted, 7 killed...") live in `<file>.report.txt`, never in the chat (Ryan 10-30_016dc322: "the formatting here is all weird"). Nothing before the list, nothing after it.
5. Ryan grades. "keep 3 and 5": run `python3 tools/hooks/gate.py keep <file> 3 5`. "Too long" or "boring": fix this round, new file r<N+1>. "From now on X": add it to `tools/hooks/rules/short-cold.json` in his exact words as a `check` or `judge` rule, show him the entry, the next round is gated by it.

Never paste hooks the gate killed. When Ryan approves a hook and asks for 'more options of it', rewrite that sentence 5 to 10 ways in chat; that is not a new round.
