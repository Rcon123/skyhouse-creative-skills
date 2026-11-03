# tools/hooks: the hook-writer gate (built 2026-10-29)

One lane so far: `short-cold`. Rules are data in `rules/short-cold.json`, in Ryan's words. The skill is `.claude/skills/hook-writer/SKILL.md`. The approved examples are `offers/_examples/short-cold-approved.md`.

## Pieces
- `gate.py` mechanical checks (`check`), the Ryan-facing output (`report`: plain numbered hooks with the star, nothing else; the counts line and the carried-over count go to `<file>.report.txt`, never the chat), stamp freshness (`status`), keeps (`keep`).
- `judge.py prompt <file>` writes `<file>.judge-prompt.md`; a FRESH in-session agent (general-purpose, sonnet) reads it as the persona in the file's `reader:` line and writes `<file>.judge-out.json`; `judge.py stamp <file>` turns that into `<file>.hookjudge.json`. No login, no background process (Ryan, 10-29: nothing may wait on him). `judge.py headless <file>` is the old one-call-per-hook route through the CLI, kept for when a login exists.
- `hook_stop.py` Stop hook (wired in `.claude/settings.json`): a hooks file actually written this turn (Write/Edit, or a Bash `>`/`tee` to the `.md` itself, never a side file or a file only read) with no fresh PASS stamp sends the reply back once. Tightened 2026-11-02.
- `READER-PROMPT.md` the stranger's questions. `{READER}`, `{HOOK}`, `{QUESTIONS}` are filled from the file and the rules.
- `test_gate.py` + `fixtures/` one hook per check rule that must die. Run `python3 tools/hooks/test_gate.py` after any change.

## The loop order (every round, before the reply)
1. Write `offers/<slug>/ads/hooks/<angle>-r<N>.md`. The `sources:` line is `none` or full paths from the workspace root under `offers/`, semicolon separated, no prose (the gate prints the expected shape when it rejects one).
2. `python3 tools/hooks/judge.py nojudge <file>` (judge OFF since 10-29; writes the stamp. Judge on: `judge.py prompt`, fresh agent, `judge.py stamp`).
3. `python3 tools/hooks/gate.py report <file>`. Its stdout is the whole reply. Never write the reply first and run these after; that is what fired the Stop hook 3 times in 5 (dreaming 2026-11-02, sessions 10-29_9bbc526f, 10-29_9970f3d2, 10-29_a90bed16).

## Rule types
- `check`: a primitive decides. Primitives today: `words` (min, max), `one_sentence`, `forbid` (regex, or `from: language.never`), `require` (`from: language.core`), `set` (min_drafted, max_shown, min_stars), `set_max` (regex, max_per_10), `categories`, `new_lines` (added 2026-11-02: kills a hook that repeats an earlier round of the same angle, same line or same first five words; a weak hook is dead, never rewritten).
- `judge`: a question the stranger answers about one line, with `answers` and `fail_when`.
- `taste`: text only, shown to the writer, never gates.
A rule nobody can check mechanically becomes a judge question, never a silent skip. A new primitive is a code change; a new rule is not.

## Adding a rule
Only with Ryan's yes, in his words. Append to the lane's json with a new id, `said`, `date`, `type`, `spec`. Every stamp goes stale (the rules hash changed), so the next round is judged under the new rule.

## Adding a lane
New `rules/<lane>.json`, a `lane:` value in the hooks file. The reader persona still comes from the file. No code.

## What it cannot see
Hooks pasted into chat from memory, or into a Google Doc, never touch a hooks file and never get judged. The Stop hook only catches files written under `offers/<slug>/ads/hooks/`.
