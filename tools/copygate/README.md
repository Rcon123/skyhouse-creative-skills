# copygate: the cold-read judge (a tool, never a gate)

Built 2026-10-27, the morning after the ProDenta / Pup Labs escalation (offers/prodenta/CLIENT-ESCALATION-2026-10-26.md).
A page went live after 17 graded versions with a sentence a stranger could not parse and a hero a stranger reads as a
dead dog. Every review graded angle, reveal and punch. Nobody read it once, cold. This tool makes that read cheap.

**10-30, Ryan: "Get rid of this thing that stops you from doing it because it's just wasting my time."** The ship block
is gone. Nothing waits on a stamp: deploys, Doc pushes, handoffs and ClickUp go when he says go. The judge is a read you
run on new copy and report as notes. (dreaming 2026-11-02, sessions 10-30_6aaa8a1e, 11-02_0af56953)

## What runs by itself (hooks in .claude/settings.json)

| When | What | Blocks? |
|---|---|---|
| After every Write/Edit to `offers/<slug>/{ads,advertorials,landers,videos}/**.{md,html,txt}` | `hook_post_write.py` runs the mechanical check and prints it to Claude: dashes, banned words (LANGUAGE.md "Never"), sentences over 18 (warn) / 25 (fail) words, paragraphs over ~3 phone lines, reading grade (warn over 6). | No (the write already happened) |
| ~~Before every Bash command that ships copy~~ | ~~`hook_pre_ship.py` required a valid PASS stamp~~ **Removed 2026-10-30 at Ryan's order.** The script exits 0 at the top and is no longer in settings.json. | No |

Notes files (README, BATCH, PLAN, STUDY, CONCEPTS, `_*`) are not copy and are skipped.

## The judge

```bash
python3 tools/copygate/coldread.py judge offers/<slug>/landers/<x>/advertorial.html
python3 tools/copygate/coldread.py judge offers/<slug>/ads/<file>.md --from "MASTHEAD:"
```

A fresh reader with zero context reads the copy once with `READER-PROMPT.md`: a 58-year-old on a phone. It returns every
sentence it had to re-read, every unclear referent, every line that is not how a person talks, every mechanism word that
is not the brand's own (from `offers/<slug>/LANGUAGE.md`), and whether any image description reads as a dead animal.
Verdict PASS only when the mechanical check has no FAIL and the reader flagged nothing. Writes `<file>.coldread.json`.

**The read cap (dreaming 2026-11-02, sessions 10-26_601f85f7, 10-26_d2b8fcfa, 10-28_fe5dc0fa; 5 to 16 reads per file,
85K to 105K tokens each, "This has been running for over an hour"):**
- One read on new copy. Fix the flags. At most one re-read. Then ship with the remaining flags listed as notes.
- Never a third read. Every fresh reader finds a different line; past two reads it grades taste, not clarity.
- Never run it on unchanged copy, a CSS or image swap, a team brief, ClickUp task text, locked hooks or held-reveal headlines.
- A flag on a line Ryan locked is a note for him, not a fix.

**Who reads (5c, dreaming 2026-11-02):** the DEFAULT reader is a fresh in-session Agent. `judge` prints the mechanical check
and the brief for that Agent and exits 4; the Agent runs `coldread.py text <file>`, reads once, and writes its verdict with
`coldread.py stamp <file> --reader subagent --json @verdict.json`. The stamp records `reader: subagent`.
The true stranger (`judge --headless`, a separate `claude -p` with no session) has been logged out since 10-27. Say once per
session in the reply: the headless stranger is logged out and `claude login` in a terminal restores it. Never run
`claude login` yourself, never make him do it to ship.

**Scope (5d, dreaming 2026-11-02):** the check, the reader text and the stamp hash cover the copy only. `--from "MASTHEAD:"`
starts at that line (builder notes above it are skipped); `--section "<heading>"` takes one markdown section. By default a
line that is only a `[bracketed builder tag]` is skipped, inline `[tags]` are stripped, and the footer disclaimer block
(`<footer>`, "These statements have not been evaluated", "Copyright") is skipped; `--keep-tags` / `--keep-footer` turn that
off. The stamp stores the scope and a hash of the scoped text, so a note added above the copy, a CSS change or an image
swap does not stale it (`status` says "copy section unchanged"). A reader image `problem` that begins with "none" is no flag.

Ryan's override, from his own terminal only (refuses without a TTY): `coldread.py approve <file> --note "why"`. Since 10-30
nothing needs it to ship; it exists so a locked line can carry a PASS stamp on his word.

Other commands: `check <file>` (mechanical only), `status <file>`, `text <file>` (what the reader sees). All take the scope flags.
Tests for the ship hook and the reply-length stop hook: `python3 tools/copygate/test_hook.py` (the ship-hook block cases expect blocks that were removed 2026-10-30; the stop-hook cases are current, dreaming 2026-11-02).

## What the judge cannot grade (structural blind spots)

These fail every fresh reader by design. Report them as "reader flag, by design", never rewrite them to satisfy the reader:
- **Locked hooks and locked control lines.** Ryan locked them; a stranger's stumble is his call, not a fix.
- **Held-reveal headlines and Top 5 teasers.** The reader cannot know what the page holds back on purpose; "I could not tell what the trick is" is the point.
- **Ad-voice lines** ("sounds like a salesman", "too exact a number"). The prompt says not to flag these and readers still do; 9 of 16 flags on the ProDenta squeeze round 4 were this.
- **Reader variance.** The same body passed one reader and failed the next on the same day (ProDenta v16, 10-27). Two reads is the budget, not a target of zero flags.

## LANGUAGE.md (per offer)

```
## Their words
- tartar
- "so rotten even a professional cleaning couldn't help"
## Never
- crust (our word, not theirs)
```
The check fails on any `## Never` entry. The judge gets `## Their words` and flags mechanism words that are not on it.
`tools/copygate/NEVER.md` holds cross-offer bans.

## Rules for the writer (in every copy skill as "COLD-READ JUDGE")

1. The reader is never the writer. 2. The flags go at the top of the deliverable as notes. 3. Their words, not ours.
4. One version per round, one read, one fix pass, at most one re-read. 5. The judge is a tool, never a gate (10-30).
6. Fix the mechanical floor first. ~~5. Nothing ships unstamped.~~ (superseded 10-30)

## What it cannot see

Copy pasted straight into a Google Doc or ClickUp from chat (no file, no stamp), uploads from the Cloudflare
dashboard, and Exodus/Genesis runs whose output never touches a local file. Rule for those: pull the text into
`offers/<slug>/ads/<name>.md` first and judge it. Ryan's own phone read before launch is the last line.

## Skill-first check (PreToolUse, added 2026-11-03)

`hook_skill_first.py` refuses a Write/Edit to `offers/<slug>/{ads,advertorials,landers,videos,images}/*.{md,html,txt}` until
this session's transcript shows the lane's SKILL.md was read (Read, Bash cat, the Skill tool, or a `/slash` invoke). Ryan's
reason: text rules only work if the file gets read; this makes the read mechanical. Fails open on anything unclear (no
transcript, unknown lane, any error). Notes, READMEs, TASK/CONCEPT/BRIEF files, `_folders` and non-text files are never gated.
Lane map is the `LANES` list at the top. Tests: `python3 tools/copygate/test_skill_first.py` (24 cases).
Dry run over past sessions: `python3 -I tools/copygate/hook_skill_first.py --audit --days 7` (11-03: 108 of 250 copy writes in 7 days
happened without the skill read).
