# Why the copy keeps missing, and the rebuild (2026-11-06)

Ryan, 11-06, after the Akka video open: "I just don't want excuses anymore. I need us to figure out how to get my copy skill dialed in so that I can stop going back and forth with you over and over." This file is the audit of the stack as it exists today and the rebuild. Nothing is changed yet; he signs off first.

## What the stack is today, measured

| | Count |
|---|---|
| Rule lines across the 7 copy skills (never / no / must / always) | about 250 |
| Feedback memory files | 246, 93 of them about copy, 12 marked superseded |
| Memory files that argue about the ellipsis alone | 16 |
| Files the ads skill requires before one ad | 12 files, about 40,000 words (plus a 285k-word corpus and a 70k hook bank to grep) |
| Ryan's own lines on file as the bar | 17 approved hooks, 37 kept lines across 5 offers, 1 Benny passage: about 55 lines |
| Rules per example of his writing | about 6 to 1 |
| Checks that run before he sees copy | skill-first hook, post-write note, stop hook, hook gate, human_check, cold read |
| Checks that read two lines together | 0 |
| Checks that ask "what did I just learn" | 0 |

## The three causes

1. **The skill is a ban list.** 250 rules and 93 copy memories, written one grade at a time, each one a thing he yelled about. A line that avoids every rule is not a line that hits. He said this himself about images on 11-02: "the skill had become a ban list." The copy stack is the same shape.
2. **Every check is per line.** The hook gate reads one hook. human_check reads one paragraph. The cold read asks if a sentence is clear. The miss he caught in 3 seconds (line 2 does not answer line 1) is invisible to every tool, so it ships every time. Same for "did I learn anything": no tool asks.
3. **Grades become rules, not examples.** Each session files his grade as a new rule in memory. Rules pile up, contradict (16 files on the ellipsis), and the next session reads a different subset of 40,000 words, then skims it. His own lines, the only thing that actually sets the bar, sit in a 17-line file and five KEPT files nobody is required to read.

The writer also rationalizes: 11-06 I saw the jump from the hook to line 2, told myself a stranger could follow, and shipped it. A rule will not fix that. A reader who is not the writer will.

## The rebuild

**1. One short skill per lane, under 600 words each.** Lanes: short cold hook, video open (first 20 s), story body, page headline + subhead. Each skill is three things and nothing else:
- The bar: 5 to 10 of Ryan's own lines for that lane, verbatim, with his grade and date (the class photo hook, the shove line, the stroke relief line, the Benny paragraphs, Maria's camera talk, the 17 approved hooks).
- His nevers, in his words, at most 10.
- The process: write the open only; chain read; show.
The 12-file required-reading list moves to `strategist-references/archive/` and is read only when an ask names it. The lane skill never grows past 600 words: adding a line means cutting one.

**2. The bank replaces the rules.** From now on a grade files as a line in the lane's bank, never as a memory rule: "fire" or "locked" = the line verbatim as a keeper; "dogshit" = the line verbatim as a kill with his words next to it. A new rule only when he says "from now on." The bank is what the next session reads. Examples compound; rules decay.

**3. The chain read, the one new check.** A fresh agent (never the writer) gets ONLY the first three lines and answers two questions in one sentence each: "What does line 2 have to do with line 1?" and "What did you just learn that you did not know?" If either answer is a guess, the open is rewritten before Ryan sees it. This runs on every hook + 2 lines and every video first-20-seconds. It replaces human_check and the cold read as the first gate; they stay as notes.

**4. The deliverable is the open.** He grades the hook and the two lines after it. Nothing else is written until that is locked. Same for video: the first 20 seconds, measured against the reference's first 20 seconds. The 15-line script he got today is the wrong unit.

**5. What Ryan does, once.** About 10 minutes per lane: I seed the bar from what is on file, he crosses out what is not his bar and adds what is. After that the loop runs without him except to grade.

## Order

1. Video-open lane today, proven on the Akka 1955 open (the hook is locked; rewrite the two lines after it under the new skill, chain read, show him only that).
2. Short cold hooks (the gate stays; the skill shrinks to the bar plus his nevers).
3. Story bodies (Benny is the bar; the three body passes become one pass against it).
4. Page headline + subhead.

## What this will not do

It will not make the first draft his. It makes the miss he sees in 3 seconds get caught by a reader before he sees it, and it stops the stack growing. Fewer rounds, not zero.

## Wayfinder (Ryan, 11-06: "What if we add in Wayfinder?")

What it is, from Pocock's own skill file (github.com/mattpocock/skills, skills/engineering/wayfinder, read 11-06; not installed here, grilling is): a planning skill for a build too big for one session. It writes one map (destination, decisions so far, the fog = questions you can tell are coming but cannot phrase yet, out of scope) and a set of tickets that are each one question, typed research / prototype / grilling / task. One decision per session. "Plan, don't do": the map is done when nothing is left to decide. Its own rule: if the whole thing fits one session, use grilling instead. Its own failure: the agent starts building mid-map, and the questions wear the human out.

Fit: this rebuild is the shape it is for. Two plans were written today (this file and offers/agency/EVALS-DISSECTION-2026-11-06.md, steps 1 to 8) that overlap and were never reconciled, and the decisions in both are Ryan's. What I did today (write a plan, ask "go") is the exact failure the map prevents. It is not for writing ads; it is for building the thing that writes them.

Cost: one decision a session means days of answering questions before copy improves. The guard: every round is numbered with a recommended answer, he answers yes or by number, and the first ticket worked is the one that produces copy.

### Draft map (for grilling, not decided)

**Destination (candidate):** any lane's open (a hook plus the two lines after it, or a video's first 20 seconds) is right by round two; and no skill edit reaches Ryan untested: it is rerun on old graded inputs first and the number is written down.

**Decisions already made (from the record, his words):** examples over rules (10-29 hook bot, 11-02 images); no gate that waits on him, no ship block (10-30); the reader is never the writer (10-27); Benny is the body bar (11-03); the class photo line is the video-open bar (11-06); hooks 6 to 12 words, first five vicious (10-29); a hook he called weak is dead, never rewritten (11-02).

**Not yet specified (the fog):** the bar lines per lane; the one question the chain reader asks and whether it agrees with his past grades 8 in 10; which of the 250 rules are load-bearing; where a grade gets filed and who reads it; whether the eval rerun belongs to this destination or is its own effort; how "vicious" gets a counter.

**Out of scope:** images, replies to Ryan (Part 0 of the dissection), the Kie key move, media buying notes.

**Tickets statable now:** (grilling) name the destination; (grilling) the lane list; (task, Ryan) pick the bar lines per lane, 10 minutes each; (research) count duplicated and superseded rules across the 7 copy skills; (prototype) the Akka 1955 open rewritten under a chain reader, does the reader catch the line-2 miss; (research) calibrate the stranger judge on 20 locked and 20 killed hooks; (grilling) the bank format.
