#!/usr/bin/env python3
"""PreToolUse hook (Bash): no copy ships without a valid cold-read PASS stamp.

Ship = any of:
  lander deploy      tools/landers/deploy.sh <dir> ...            -> <dir>/advertorial.html
                     deploy_r2.sh <dir> ...                       -> every *.html in <dir>
                     wrangler r2 object put ... --file=<x>.html   -> <x>.html
  doc push           npx exodus drive create-doc | batch-update   -> copy files named in the command, else COPYGATE=<file>
  handoff scripts    offers/<slug>/handoff/*.py, update_doc.py, make_docs*.py, refresh_docx.py, ship*.py, add_picks.py
                                                                  -> .md/.txt/.html args under offers/, else COPYGATE=<file>
  ClickUp task       api.clickup.com ... POST / task              -> COPYGATE=<file>

Rule (Ryan 10-26, "it has to apply automatically so it can't slip through the cracks"): a ship command whose copy
cannot be identified is BLOCKED with the fix spelled out, not allowed with a warning. A --dry / --dry-run command,
or one that only reads (echo, cat, grep, head, sed -n ...), is never touched. Any hook crash = allow + warning.
"""
import json, os, re, shlex, subprocess, sys
# 2026-10-30, Ryan: "Get rid of this thing that stops you from doing it because it's just wasting my time."
# The ship block is OFF. The judge (coldread.py judge) still exists as a tool to run when asked; nothing is blocked.
import sys as _s; _s.exit(0)
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent.parent
COLD = HERE / "coldread.py"
NOT_RUN = {"echo", "printf", "cat", "grep", "rg", "sed", "awk", "less", "head", "tail", "man", "which", "type", "ls", "wc", "diff", "#", "open"}
SHIP_MARK = re.compile(r"tools/landers/deploy\.sh|deploy_r2\.sh|\br2\s+object\s+put\b|exodus\s+drive\s+(create-doc|batch-update)|"
                       r"/handoff/[^\s;&|]+\.py|\b(update_doc|make_docs[^\s]*|refresh_docx|ship[^\s/]*|add_picks)\.py|api\.clickup\.com", re.I)
COPY_EXT = (".md", ".txt", ".html", ".htm")
WARN = []


def out_allow():
    if WARN:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "copygate: " + " ".join(WARN)}}))
    return 0


def block(msg):
    print("copygate BLOCKED this command.\n" + msg + "\nDo not work around the gate with another tool or command. "
          "Run the judge, fix every flag (or have Ryan run `approve` himself), then ship.", file=sys.stderr)
    return 2


HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?\n\s*\1\s*(?=\n|$)", re.S)


def segments(cmd):
    cmd = HEREDOC.sub(" HEREDOC_BODY", cmd)        # a heredoc body is data (a script, a doc), not a command
    try:
        lex = shlex.shlex(cmd.replace("\n", " ; "), posix=True, punctuation_chars=";&|")
        lex.whitespace_split = True
        toks = list(lex)
    except ValueError:
        return None
    segs, cur = [], []
    for t in toks:
        if t in {"&&", "||", ";", "|", "&", ";;", "|&"}:
            segs.append(cur); cur = []
        else:
            cur.append(t)
    segs.append(cur)
    return [s for s in segs if s]


def resolve(p):
    q = Path(os.path.expanduser(p))
    if not q.is_absolute():
        q = WS / q
    return q


def copy_files_for(seg, env_copy):
    """Returns (files, reason_if_none). files = list of Path the stamp must cover."""
    words = [w for w in seg if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", w)]
    envs = {w.split("=", 1)[0]: w.split("=", 1)[1] for w in seg if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", w)}
    gate = envs.get("COPYGATE") or env_copy
    text = " ".join(seg)
    files = []
    # lander deploy
    if any(w.endswith("tools/landers/deploy.sh") or w.endswith("/deploy.sh") for w in words):
        i = next(k for k, w in enumerate(words) if w.endswith("deploy.sh"))
        rest = [w for w in words[i + 1:] if not w.startswith("-")]
        if not rest or "$" in rest[0]:
            return [], "write the lander folder as a literal path (not a variable) so the gate can find advertorial.html"
        d = resolve(rest[0])
        if d.is_dir():
            if "deploy_r2.sh" in words[i]:
                files = sorted(d.glob("*.html"))
            else:
                files = [d / "advertorial.html"]
        elif d.suffix.lower() in COPY_EXT:
            files = [d]
        else:
            return [], f"lander folder not found: {rest[0]}"
    elif re.search(r"\br2\s+object\s+put\b", text, re.I):
        m = re.search(r"--file[= ]+[\"']?([^\s\"']+)", text)
        if not m:
            return [], "name the uploaded file with --file=<path> so the gate can read it"
        f = resolve(m.group(1))
        if f.suffix.lower() in (".html", ".htm"):
            files = [f]
        else:
            return None, ""            # an image or asset upload: not copy
    else:
        for w in words:
            if w.lower().endswith(COPY_EXT) and ("offers/" in w or "/offers/" in w):
                files.append(resolve(w))
        if not files and gate:
            if "$" in gate:
                return [], "COPYGATE must be a literal path"
            files = [resolve(gate)]
        if not files:
            return [], ("say which copy this ships: prefix the command with COPYGATE=<path to the ad/advertorial/script file> "
                        "(the file whose words end up in the doc, task or page)")
    return files, ""


def check_stamps(files):
    bad = []
    for f in files:
        if not f.exists():
            bad.append(f"{f}: file not found"); continue
        r = subprocess.run([sys.executable, str(COLD), "status", str(f)], capture_output=True, text=True, timeout=20)
        if r.returncode != 0:
            why = (r.stdout.strip().splitlines() or ["no stamp"])[-1].strip()
            bad.append(f"{f.relative_to(WS) if str(f).startswith(str(WS)) else f}: {why}")
    return bad


def decide(cmd):
    if not SHIP_MARK.search(HEREDOC.sub(" ", cmd)):
        return 0, ""
    segs = segments(cmd)
    if segs is None:
        return 2, "the command could not be parsed; write it as one plain line."
    env_copy = os.environ.get("COPYGATE", "").strip() or None
    carried = None
    for sg in segs:
        envs = [w for w in sg if w.startswith("COPYGATE=")]
        words = [w for w in sg if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", w)]
        if envs and not words:
            carried = envs[0].split("=", 1)[1]; continue
        if not words or words[0].lower() in NOT_RUN or words[0] == "export":
            continue
        if not SHIP_MARK.search(" ".join(sg)):
            continue
        if re.search(r"api\.clickup\.com", " ".join(sg), re.I) and not re.search(
                r"(-X|--request)\s*(POST|PUT|DELETE)|--data|--json|(^|\s)-d\s|--upload-file|(^|\s)-F\s", " ".join(sg), re.I):
            continue                                         # ClickUp GET: a read, never a ship
        if any(w in ("--dry", "--dry-run", "--dryrun") for w in sg):
            continue
        if re.search(r"exodus\s+drive", " ".join(sg), re.I) and not re.search(r"create-doc|batch-update", " ".join(sg)):
            continue                                         # get-doc / list-files / status: reads
        files, why = copy_files_for(sg, carried or env_copy)
        if files is None:
            continue
        if not files:
            return 2, why
        bad = check_stamps(files)
        if bad:
            fixes = "\n".join(f"  python3 tools/copygate/coldread.py judge \"{f}\"" for f in files)
            return 2, ("No valid cold-read PASS stamp for:\n  " + "\n  ".join(bad) +
                       "\nRun the fresh reader on each file, fix every flag, then re-run the ship command:\n" + fixes)
    return 0, ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command")
    if not isinstance(cmd, str):
        return 0
    code, msg = decide(cmd)
    return block(msg) if code == 2 else out_allow()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException as e:
        WARN.append(f"the copy gate hook crashed ({type(e).__name__}); this command was NOT checked. Tell Ryan.")
        sys.exit(out_allow())
