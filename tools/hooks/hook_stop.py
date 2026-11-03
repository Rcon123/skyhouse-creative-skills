#!/usr/bin/env python3
"""Stop hook: a hooks file written this turn must carry a fresh PASS stamp before the reply goes out.

Scans the transcript from Ryan's last message: every Write/Edit/MultiEdit to offers/<slug>/ads/hooks/<angle>-r<N>.md,
and every Bash command naming one, is a hooks file. If any of them has no stamp, a stale stamp, or nothing survived,
the reply is sent back once with the two commands to run. stop_hook_active guards the loop. Any error = allow.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent.parent
sys.path.insert(0, str(HERE))
# the hooks file itself, never its side files (.hookjudge.json, .judge-out.json, .report.txt), so a Bash write of a side
# file does not count as writing the round (dreaming 2026-11-02, sessions 10-29_a90bed16, 10-29_9bbc526f)
HOOKFILE = re.compile(r"[^\s\"'=]*offers/[^/\s\"']+/ads/hooks/[^/\s\"']+-r\d+\.md(?![\w.-])")


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0
    path = data.get("transcript_path")
    if not path:
        return 0
    files = []
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            m = e.get("message") or {}
            role = m.get("role") or e.get("type")
            c = m.get("content")
            if role == "user" and not e.get("isMeta"):
                t = c if isinstance(c, str) else " ".join(b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text")
                if t.strip() and not t.strip().startswith(("<", "[")):
                    files = []  # a new human message starts a new turn
                continue
            if role != "assistant" or not isinstance(c, list):
                continue
            for b in c:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                inp = b.get("input") or {}
                name = b.get("name", "")
                if name in ("Write", "Edit", "MultiEdit"):
                    # only a file actually written this turn; a round only mentioned or read never counts
                    fp = str(inp.get("file_path", ""))
                    if HOOKFILE.search(fp) and HOOKFILE.search(fp).end() == len(fp):
                        files.append(fp)
                elif name == "Bash":
                    # only a command that WRITES a hooks file counts (cat > file, tee file); a check or a read of an old round does not
                    cmd = str(inp.get("command", ""))
                    files += [m.group(1) for m in re.finditer(r"(?:>\s*|\btee\s+(?:-a\s+)?)[\"']?(" + HOOKFILE.pattern + ")", cmd)]
    if not files:
        return 0
    import gate
    bad = []
    seen = set()
    for fp in files:
        p = Path(fp)
        if not p.is_absolute():
            p = WS / fp
        p = p.resolve()
        if p in seen or not p.exists():
            continue
        seen.add(p)
        fp = str(p.relative_to(WS)) if str(p).startswith(str(WS)) else str(p)
        st, why = gate.read_stamp(p)
        if why:
            bad.append((fp, why)); continue
        if not any(h.get("verdict") == "PASS" for h in st.get("hooks", [])):
            bad.append((fp, "stamp ok, nothing survived; draft again"))
    if not bad:
        return 0
    lines = [f"- {fp}: {why}" for fp, why in bad]
    print(json.dumps({"decision": "block", "reason":
        "hook-writer: a hooks file went out without a fresh PASS stamp.\n" + "\n".join(lines) +
        "\nFinish the loop BEFORE writing the reply, every round: `python3 tools/hooks/judge.py nojudge <file>` (the judge is OFF since 10-29; "
        "this writes the stamp) then `python3 tools/hooks/gate.py report <file>`. The report (plain numbered hooks) is your whole reply; "
        "the counts are in <file>.report.txt, not the chat. Never ask Ryan to log in to anything."}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException:
        sys.exit(0)
