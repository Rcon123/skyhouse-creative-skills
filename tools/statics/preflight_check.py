#!/usr/bin/env python3
"""Preflight gate for image rounds (dreaming 2026-11-02, sessions 10-28_3ca8ae6d, 10-28_85e5fbe2, 10-29_ccab9cfb, 10-30_016dc322).

kie.render() calls check() before the first POST and refuses to fire without a passing preflight.md.
Run by hand:  python3 tools/statics/preflight_check.py <round folder>

The round folder (or its parent, when the outdir is raw/) must hold preflight.md with three sections:

  ## Files read
  - .claude/skills/strategist-images/SKILL.md (47562 bytes)      one line per file, path + size
  - .claude/skills/strategist-images/formats.md (46096 bytes)

  ## Format blocks
  - lf07a-pill-box: none                                           one line per frame: name: <format block> or none
  - lf12-whiteboard: whiteboard prop                               the block name is a ### heading in formats.md

  ## Ryan's notes
  1. "I liked the idea of this, so I want you to think about why I liked this, but I want you to do more shit than just this." (10-28 17:16)
  2. "..."                                                         every note from THIS campaign, verbatim, numbered
  Check: frame A keeps note 1 by ...; note 2 by ...                 round 2+ only: one line, the round against all the notes

Rules enforced:
  1. All three sections present. Files read names SKILL.md and formats.md with sizes.
  2. Every format block named is a heading in formats.md (approved sections, not REJECTED).
  3. A format block used in a prior round of the same campaign is refused until the library is exhausted
     (prior rounds = sibling folders <campaign>-r*/preflight.md or <campaign>/r*/preflight.md).
  4. Round 2 and later: the notes section holds at least one numbered quote and a "Check:" line.
"""
import os, re, sys, glob

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FORMATS_MD = f"{WS}/.claude/skills/strategist-images/formats.md"
ROUND_RE = re.compile(r"^(.*?)-?r(\d+)$")


def library_formats(path=FORMATS_MD):
    """Approved ### headings in formats.md, lowercased, with the parenthetical stripped. Stops at REJECTED/CANDIDATES."""
    names = set()
    skip = False
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            skip = bool(re.match(r"## (REJECTED|CANDIDATES)", line))
            continue
        if skip or not line.startswith("### "):
            continue
        name = re.sub(r"\s*\(.*$", "", line[4:]).strip()
        name = re.sub(r"^Format:\s*", "", name, flags=re.I)
        if name:
            names.add(name.lower())
    return names


def round_folder(outdir):
    outdir = os.path.abspath(outdir.rstrip("/"))
    if os.path.exists(os.path.join(outdir, "preflight.md")):
        return outdir
    parent = os.path.dirname(outdir)
    if os.path.exists(os.path.join(parent, "preflight.md")) and not ROUND_RE.match(os.path.basename(outdir)):
        return parent
    return outdir


def siblings(folder):
    """Prior rounds' preflight.md files for the same campaign, and this round's number (1 when unknown)."""
    base = os.path.basename(folder)
    parent = os.path.dirname(folder)
    m = ROUND_RE.match(base)
    if not m:
        return [], 1
    stem, n = m.group(1), int(m.group(2))
    if stem:
        pat = os.path.join(parent, f"{stem}-r*", "preflight.md")
    else:
        pat = os.path.join(parent, "r*", "preflight.md")
    out = []
    for p in glob.glob(pat):
        mm = ROUND_RE.match(os.path.basename(os.path.dirname(p)))
        if mm and int(mm.group(2)) < n:
            out.append(p)
    return sorted(out), n


def sections(text):
    """{heading lowercased: body} for every '## ' heading."""
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip().lower()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def find_section(secs, *keys):
    for k, v in secs.items():
        if all(key in k for key in keys):
            return v
    return None


def formats_in(body):
    """Format block names from '- frame: block' lines; 'none' is skipped."""
    found = []
    for line in body.splitlines():
        m = re.match(r"^\s*[-*]\s*[^:]+:\s*(.+?)\s*$", line)
        if not m:
            continue
        f = re.sub(r"\s*\(.*$", "", m.group(1)).strip().lower()
        if f and f not in ("none", "no format", "photo", "real photo", "-"):
            found.append(f)
    return found


def check(outdir, formats_md=FORMATS_MD):
    """Returns (ok, [messages]). ok=False means do not fire."""
    folder = round_folder(outdir)
    pf = os.path.join(folder, "preflight.md")
    msgs = []
    if not os.path.exists(pf):
        return False, [f"no preflight.md in {folder}. Write it (Files read / Format blocks / Ryan's notes) before the first POST."]
    text = open(pf, encoding="utf-8").read()
    secs = sections(text)
    files = find_section(secs, "files")
    blocks = find_section(secs, "format")
    notes = find_section(secs, "note")
    if files is None: msgs.append("preflight.md has no '## Files read' section.")
    if blocks is None: msgs.append("preflight.md has no '## Format blocks' section.")
    if notes is None: msgs.append("preflight.md has no '## Ryan's notes' section.")
    if msgs:
        return False, msgs

    # 1. files read, with sizes
    for need in ("SKILL.md", "formats.md"):
        if not re.search(re.escape(need) + r".*\d+\s*(bytes|b|kb|k|chars)", files, re.I):
            msgs.append(f"Files read: {need} is not listed with its size (read it, then write the path and size).")

    # 2. format blocks exist in the library
    lib = library_formats(formats_md)
    used_here = formats_in(blocks)
    if not re.search(r"^\s*[-*]\s*[^:]+:", blocks, re.M):
        msgs.append("Format blocks: no per-frame lines ('- frame: block' or '- frame: none').")
    for f in used_here:
        if f not in lib:
            msgs.append(f"Format blocks: '{f}' is not a ### heading in formats.md (use the block's name verbatim, or 'none').")

    # 3. no format already used in a prior round of this campaign, until the library is exhausted
    prior, n = siblings(folder)
    used_before = {}
    for p in prior:
        for f in formats_in(find_section(sections(open(p, encoding="utf-8").read()), "format") or ""):
            used_before.setdefault(f, os.path.basename(os.path.dirname(p)))
    exhausted = lib and lib <= set(used_before)
    for f in used_here:
        if f in used_before and not exhausted:
            msgs.append(f"Format blocks: '{f}' already used in {used_before[f]} of this campaign. A block used in a prior round is repetition; pick one not yet used ({len(lib) - len(set(used_before) & lib)} left).")

    # 4. round 2+: notes numbered verbatim and a one-line check
    if n > 1 or prior:
        if not re.search(r"^\s*1[.)]\s+\S", notes, re.M):
            msgs.append("Ryan's notes: round 2+ needs every note from this campaign, numbered, in his words.")
        if not re.search(r"^\s*check\s*:", notes, re.M | re.I):
            msgs.append("Ryan's notes: round 2+ needs one 'Check:' line holding this round against all the notes.")
    elif not notes.strip():
        msgs.append("Ryan's notes: write 'none yet' on round 1, never leave it blank.")

    return (not msgs), msgs or [f"preflight ok: {pf}"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    ok, out = check(sys.argv[1])
    print("\n".join(("OK " if ok else "REFUSED ") + m for m in out))
    sys.exit(0 if ok else 1)
