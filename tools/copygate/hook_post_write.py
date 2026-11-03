#!/usr/bin/env python3
"""PostToolUse hook (Write|Edit|MultiEdit): after any copy file is written, run the mechanical cold-read check and
put the result in front of Claude. Copy files = offers/<slug>/{ads,advertorials,landers,videos}/**.{md,html,txt},
excluding notes (README, BATCH, PLAN, STUDY, CONCEPTS, names starting with _ ) and stamps.
Never blocks (the write already happened); nothing blocks since 10-30. Any error = silent."""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COPY = re.compile(r"/offers/[^/]+/(ads|advertorials|landers|videos)/.*\.(md|html|htm|txt)$", re.I)
HOOKS = re.compile(r"/offers/[^/]+/ads/hooks/", re.I)  # 10-29: hook-writer files have their own gate (tools/hooks)
SKIP = re.compile(r"(^|/)(_[^/]*|README[^/]*|BATCH[^/]*|PLAN[^/]*|STUDY[^/]*|CONCEPTS[^/]*|NOTES?[^/]*|HOOKS?-RANKED[^/]*|.*\.coldread\.json)$", re.I)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = (data.get("tool_input") or {}).get("file_path") or ""
    if not fp or not COPY.search(fp) or SKIP.search(fp) or HOOKS.search(fp) or not Path(fp).exists():
        return 0
    try:
        r = subprocess.run([sys.executable, str(HERE / "coldread.py"), "check", fp], capture_output=True, text=True, timeout=25)
        report = (r.stdout or "").strip()
    except Exception:
        return 0
    st = Path(fp + ".coldread.json")
    # dreaming 2026-11-02: the ship block was removed 10-30; this is a note, never a gate. One read on new copy, two max.
    tail = ("\nNote: this file changed since its last cold read. If the copy is new, one stranger read before the first "
            "review deploy: python3 tools/copygate/coldread.py judge \"%s\"  (flags go in the delivery as notes; two reads max; "
            "a CSS, image or one-line fix never waits on a reread)." % fp) if st.exists() else (
            "\nNote: no cold read yet. If the copy is new, one stranger read before the first review deploy: "
            "python3 tools/copygate/coldread.py judge \"%s\"  (flags as notes, two reads max)." % fp)
    msg = "[copygate] " + report + tail
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException:
        sys.exit(0)
