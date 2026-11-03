#!/usr/bin/env python3
"""Appends SKILL-BLOCK.md (the cold-read gate rules) to every copy-producing skill, once. Re-runnable."""
from pathlib import Path
WS = Path(__file__).resolve().parent.parent.parent
block = (WS / "tools/copygate/SKILL-BLOCK.md").read_text().strip()
skills = ["strategist-ads", "strategist-advertorial", "strategist-advertorial-pdp", "strategist-longform", "strategist-lander",
          "strategist-lander-qa", "strategist-launch", "strategist-netnew", "strategist-offer", "strategist-research-brief",
          "oneshot-video", "exodus-strategist"]
extra = {
    "strategist-lander-qa": "\n\nQA addition: the page's `advertorial.html.coldread.json` must be a valid PASS (run `python3 tools/copygate/coldread.py status <page>`). Missing or stale = VERDICT FAIL, item 0, before the skim test.",
    "strategist-launch": "\n\nLaunch addition: the copy doc is filled from a stamped file only (`COPYGATE=<file>` on every handoff script). The task preview to Ryan shows the stamp line (reader, time, grade).",
    "strategist-offer": "\n\nOffer-setup addition: `offers/<slug>/LANGUAGE.md` is created with OFFER.md, seeded from the VSL transcript and the client's top ads (`## Their words`), and `## Never` starts empty. No ad or page is written for an offer without it.",
    "strategist-research-brief": "\n\nResearch addition: the synthesis step fills `offers/<slug>/LANGUAGE.md` (`## Their words`) from the VSL, the client's top ads and the real-people scrapes, verbatim phrases only.",
    "oneshot-video": "\n\nVideo addition: the SCRIPT file is copy. Judge it before the build (`coldread.py judge offers/<slug>/videos/<name>/SCRIPT*.md`); the video handoff script is gated like every handoff script.",
    "exodus-strategist": "\n\nExodus addition: Genesis output lives in Google Docs, which the hooks cannot see. Before an Exodus run's copy is handed to anyone, pull it to `offers/<slug>/ads/exodus-<runId>.md` (`npx exodus read-doc <runId>`) and judge that file.",
}
for s in skills:
    p = WS / f".claude/skills/{s}/SKILL.md"
    if not p.exists():
        print("MISSING", s); continue
    t = p.read_text()
    if "COLD-READ GATE (2026-10-27" in t:
        print("already", s); continue
    p.write_text(t.rstrip("\n") + "\n\n" + block + extra.get(s, "") + "\n")
    print("added", s, len(p.read_text()), "chars")
