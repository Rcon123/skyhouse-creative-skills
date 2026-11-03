#!/usr/bin/env python3
"""PreToolUse hook (Write|Edit|MultiEdit): no draft before the lane's skill is read.

Ryan, 2026-11-03, after the dreaming pass: text rules only work if the file gets read, so this makes the read mechanical.
Writing a copy file under offers/<slug>/{ads,advertorials,landers,videos,images}/ is refused unless this session's
transcript shows the lane's SKILL.md was read (Read tool, a Bash cat/sed of it, the Skill tool, or a /slash invoke).

Fails OPEN: no transcript, unknown lane, any error -> allow. It only blocks the one clear case.
Dry run over past sessions:  python3 hook_skill_first.py --audit --days 7
"""
import json, os, re, sys, glob, time

LANES = [
    # (path regex, [accepted skill names]) first match wins
    (re.compile(r"/offers/[^/]+/ads/hooks/", re.I), ["hook-writer"]),
    (re.compile(r"/offers/[^/]+/ads/", re.I), ["strategist-ads", "strategist-longform", "hook-writer", "write-video-script"]),
    (re.compile(r"/offers/[^/]+/advertorials/", re.I), ["strategist-advertorial", "strategist-advertorial-pdp", "strategist-lander", "strategist-longform"]),
    (re.compile(r"/offers/[^/]+/landers/", re.I), ["strategist-lander", "strategist-lander-qa", "strategist-advertorial", "lander-deploy"]),
    (re.compile(r"/offers/[^/]+/videos/", re.I), ["oneshot-video", "write-video-script", "strategist-ads", "strategist-longform", "song-ads"]),
    (re.compile(r"/offers/[^/]+/images/", re.I), ["strategist-images", "exodus-image", "exodus-creative", "exodus-template"]),
]
GATED_EXT = re.compile(r"\.(md|html|htm|txt)$", re.I)
SKIP = re.compile(r"(^|/)(_[^/]*|README[^/]*|BATCH[^/]*|PLAN[^/]*|STUDY[^/]*|CONCEPTS?[^/]*|NOTES?[^/]*|TASK[^/]*|BRIEF[^/]*|HOOKS?-RANKED[^/]*|about_this_project\.md|LAUNCH\.md|.*[-_]input[-_.][^/]*|.*\.coldread\.json|.*\.report\.txt)$", re.I)
SKIP_DIR = re.compile(r"/_[^/]*/", re.I)  # anything under a _folder (pickers, scratch, examples)
SKILL_ROOTS = ("/.claude/skills/", "/skills/user/", "/skills/")


def lane_for(fp):
    if not fp or not GATED_EXT.search(fp) or SKIP.search(fp) or SKIP_DIR.search(fp.split("/offers/")[-1]):
        return None
    for rx, names in LANES:
        if rx.search(fp):
            return names
    return None


BASH_READ = re.compile(r"(?:^|[;&|(]\s*)(?:cat|sed|head|tail|less|more|bat)\b[^;&|\n]*?/skills/(?:user/)?([\w-]+)/SKILL\.md", re.M)


def _skill_from_path(p):
    m = re.search(r"/skills/(?:user/)?([^/]+)/SKILL\.md", p or "")
    return m.group(1) if m else None


def skills_read(transcript_path):
    """Set of skill names this transcript shows as read/invoked. Prefilter lines by bytes, then parse only those."""
    out = set()
    keys = (b"SKILL.md", b'"Skill"', b"command-name")
    with open(transcript_path, "rb") as fh:
        for raw in fh:
            if not any(k in raw for k in keys):
                continue
            try:
                d = json.loads(raw)
            except Exception:
                continue
            m = d.get("message") or {}
            c = m.get("content")
            if d.get("type") == "user" and isinstance(c, str):
                for s in re.findall(r"<command-name>/?([\w-]+)</command-name>", c):
                    out.add(s)
                continue
            if d.get("type") != "assistant" or not isinstance(c, list):
                continue
            for b in c:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                name, inp = b.get("name"), b.get("input") or {}
                if name == "Skill":
                    s = str(inp.get("skill", "")).split(":")[-1]
                    if s:
                        out.add(s)
                elif name == "Read":
                    s = _skill_from_path(inp.get("file_path", ""))
                    if s:
                        out.add(s)
                elif name == "Bash":
                    out.update(BASH_READ.findall(str(inp.get("command", ""))))
    return out


def decide(fp, transcript_path):
    """Return None (allow) or the block message."""
    names = lane_for(fp)
    if not names:
        return None
    if not transcript_path or not os.path.exists(transcript_path):
        return None
    have = skills_read(transcript_path)
    if have & set(names):
        return None
    return ("[skill-first] Not yet: this session has not read the lane's skill. Read .claude/skills/%s/SKILL.md in full "
            "(any of: %s), name it in your next reply, then write %s." % (names[0], ", ".join(names), os.path.basename(fp)))


def audit(days):
    root = os.path.expanduser("~/.claude/projects/-Users-ryanconnolly-SkyHouse-Exodus")
    cutoff = time.time() - days * 86400
    blocked = allowed = 0
    rows = []
    for f in sorted(glob.glob(os.path.join(root, "*.jsonl")), key=os.path.getmtime):
        if os.path.getmtime(f) < cutoff:
            continue
        have = set()
        keys = (b"SKILL.md", b'"Skill"', b"command-name", b'"Write"', b'"Edit"', b'"MultiEdit"')
        first_block = None
        n_b = n_a = 0
        with open(f, "rb") as fh:
            for raw in fh:
                if not any(k in raw for k in keys):
                    continue
                try:
                    d = json.loads(raw)
                except Exception:
                    continue
                m = d.get("message") or {}
                c = m.get("content")
                if d.get("type") == "user" and isinstance(c, str):
                    have.update(re.findall(r"<command-name>/?([\w-]+)</command-name>", c))
                    continue
                if d.get("type") != "assistant" or not isinstance(c, list):
                    continue
                for b in c:
                    if not isinstance(b, dict) or b.get("type") != "tool_use":
                        continue
                    name, inp = b.get("name"), b.get("input") or {}
                    if name == "Skill":
                        have.add(str(inp.get("skill", "")).split(":")[-1])
                    elif name == "Read":
                        s = _skill_from_path(inp.get("file_path", ""))
                        if s:
                            have.add(s)
                    elif name == "Bash":
                        have.update(BASH_READ.findall(str(inp.get("command", ""))))
                    elif name in ("Write", "Edit", "MultiEdit"):
                        names = lane_for(inp.get("file_path", ""))
                        if not names:
                            continue
                        if have & set(names):
                            n_a += 1
                        else:
                            n_b += 1
                            first_block = first_block or inp.get("file_path", "")
        if n_a or n_b:
            rows.append((os.path.basename(f)[:8], n_a, n_b, first_block))
            allowed += n_a
            blocked += n_b
    for sid, a, bl, fb in rows:
        print(f"{sid}  allowed {a:3d}  would-block {bl:3d}  {('first: ' + fb.split('/offers/')[-1]) if fb else ''}")
    print(f"\n{len(rows)} sessions with copy writes in {days} days: {allowed} writes after a skill read, {blocked} without one.")


def main():
    if "--audit" in sys.argv:
        days = float(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 7
        audit(days)
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    fp = (data.get("tool_input") or {}).get("file_path") or ""
    msg = decide(fp, data.get("transcript_path"))
    if msg is None:
        return 0
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        code = main()
    except Exception:
        code = 0  # any error = allow
    sys.exit(code)
