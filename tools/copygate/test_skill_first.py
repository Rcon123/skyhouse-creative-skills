#!/usr/bin/env python3
"""Tests for hook_skill_first.py: fake transcripts, one case per line. Run: python3 tools/copygate/test_skill_first.py"""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hook_skill_first as H

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
def asst(name, inp): return json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]}})
def user(txt): return json.dumps({"type": "user", "message": {"content": txt}})

def tr(lines):
    f = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False); f.write("\n".join(lines) + "\n"); f.close(); return f.name

CASES = [
    ("ads write, nothing read -> block", [], f"{ROOT}/offers/akka/ads/story-v1.md", True),
    ("ads write after Read of strategist-ads -> allow", [asst("Read", {"file_path": f"{ROOT}/.claude/skills/strategist-ads/SKILL.md"})], f"{ROOT}/offers/akka/ads/story-v1.md", False),
    ("ads write after Skill tool -> allow", [asst("Skill", {"skill": "strategist-longform"})], f"{ROOT}/offers/akka/ads/story-v1.md", False),
    ("ads write after /slash invoke -> allow", [user("<command-name>/strategist-ads</command-name>")], f"{ROOT}/offers/akka/ads/story-v1.md", False),
    ("ads write after bash cat of skill -> allow", [asst("Bash", {"command": f"cat '{ROOT}/.claude/skills/strategist-ads/SKILL.md'"})], f"{ROOT}/offers/akka/ads/story-v1.md", False),
    ("bash that only MENTIONS the skill path (ls) -> block", [asst("Bash", {"command": f"ls -la {ROOT}/.claude/skills/strategist-ads/SKILL.md"})], f"{ROOT}/offers/akka/ads/story-v1.md", True),
    ("bash sed -n of the skill -> allow", [asst("Bash", {"command": f"cd x; sed -n 1,200p \"{ROOT}/.claude/skills/strategist-ads/SKILL.md\""})], f"{ROOT}/offers/akka/ads/story-v1.md", False),
    ("ads write after WRONG skill (images) -> block", [asst("Skill", {"skill": "strategist-images"})], f"{ROOT}/offers/akka/ads/story-v1.md", True),
    ("hooks file needs hook-writer, ads skill not enough -> block", [asst("Skill", {"skill": "strategist-ads"})], f"{ROOT}/offers/akka/ads/hooks/round-2.md", True),
    ("hooks file after hook-writer -> allow", [asst("Skill", {"skill": "hook-writer"})], f"{ROOT}/offers/akka/ads/hooks/round-2.md", False),
    ("lander html after strategist-lander -> allow", [asst("Read", {"file_path": f"{ROOT}/.claude/skills/strategist-lander/SKILL.md"})], f"{ROOT}/offers/tps/landers/top5/advertorial.html", False),
    ("lander html, nothing read -> block", [], f"{ROOT}/offers/tps/landers/top5/advertorial.html", True),
    ("video script after oneshot-video -> allow", [asst("Skill", {"skill": "oneshot-video"})], f"{ROOT}/offers/prodenta/videos/three-signs/SCRIPT-v1.md", False),
    ("images preflight.md, nothing read -> block", [], f"{ROOT}/offers/olavita/images/r11/preflight.md", True),
    ("images preflight after strategist-images -> allow", [asst("Skill", {"skill": "strategist-images"})], f"{ROOT}/offers/olavita/images/r11/preflight.md", False),
    ("skill name mentioned only in CLAUDE.md text (user msg) -> still block", [user("see .claude/skills/oneshot-video/SKILL.md for details")], f"{ROOT}/offers/prodenta/videos/x/SCRIPT.md", True),
    # never gated
    ("README in ads -> allow", [], f"{ROOT}/offers/akka/ads/README.md", False),
    ("_project-state -> allow", [], f"{ROOT}/offers/akka/_project-state.md", False),
    ("TASK.md in landers -> allow", [], f"{ROOT}/offers/tps/landers/plain-black/TASK.md", False),
    ("CONCEPT.md in videos -> allow", [], f"{ROOT}/offers/reactivate/videos/salt/CONCEPT.md", False),
    ("_picker html under images -> allow", [], f"{ROOT}/offers/olavita/images/_picker/picker.html", False),
    ("jpg in images -> allow", [], f"{ROOT}/offers/olavita/images/r11/01.jpg", False),
    ("research file -> allow", [], f"{ROOT}/offers/akka/research/BRIEF.md", False),
    ("file outside offers -> allow", [], f"{ROOT}/tools/copygate/x.md", False),
    ("memory file -> allow", [], "/Users/ryanconnolly/.claude/projects/x/memory/feedback_y.md", False),
    ("missing transcript -> allow (fail open)", None, f"{ROOT}/offers/akka/ads/story-v1.md", False),
]

bad = 0
for name, lines, fp, expect_block in CASES:
    path = tr(lines) if lines is not None else "/nonexistent/transcript.jsonl"
    got = H.decide(fp, path) is not None
    ok = got == expect_block
    bad += not ok
    print(("ok  " if ok else "FAIL") + "  " + name)
print("\nALL AS EXPECTED" if not bad else f"\n{bad} FAILED")
sys.exit(1 if bad else 0)
