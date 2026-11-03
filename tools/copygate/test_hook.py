#!/usr/bin/env python3
"""Runs the ship hook against known commands. python3 tools/copygate/test_hook.py  (expect: every line says as expected)"""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
CASES = [  # (command, expect_block)  dreaming 2026-11-02: ship block removed 10-30, hook_pre_ship exits 0, so every case expects allow
    ("tools/landers/deploy.sh offers/prodenta/landers/top5-toxins prodenta-info.americanhealthjournal.org prodenta-top5 info.americanhealthjournal.org", False),
    ('npx wrangler r2 object put "landers-prod/x/y/advertorial.html" --file=offers/prodenta/landers/top5-toxins/advertorial.html --remote', False),
    ('npx wrangler r2 object put "landers-prod/x/y/image1.jpg" --file=offers/prodenta/landers/top5-toxins/image1c.jpg --remote', False),
    ("python3 offers/prodenta/handoff/update_doc.py 1eVKl_tI offers/prodenta/ads/squeeze-story-FINAL.md", False),
    ("python3 offers/prodenta/handoff/ship_iteration.py --go", False),
    ("python3 offers/prodenta/handoff/ship_iteration.py --dry", False),
    ("COPYGATE=offers/prodenta/ads/squeeze-story-FINAL.md python3 offers/prodenta/handoff/ship_iteration.py --go", False),
    ("npx exodus drive get-doc 1abc", False),
    ('npx exodus drive batch-update 1abc --requests "[]"', False),
    ('curl -X POST https://api.clickup.com/api/v2/list/123/task -d "{}"', False),
    ("grep -n crust offers/prodenta/landers/top5-toxins/advertorial.html", False),
    ("ls offers/prodenta/handoff/", False),
    ("cd offers/prodenta && python3 handoff/add_picks.py", False),
]
ok = True
for cmd, expect in CASES:
    r = subprocess.run([sys.executable, str(HERE / "hook_pre_ship.py")], input=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}),
                       capture_output=True, text=True)
    blocked = r.returncode == 2
    crashed = "crashed" in r.stdout
    good = (blocked == expect) and not crashed
    ok &= good
    why = (r.stderr.strip().splitlines()[1:2] or [""])[0][:110] if blocked else ("CRASH " + r.stdout[:120] if crashed else "allowed")
    print(("ok  " if good else "BAD ") + ("BLOCK" if blocked else "allow") + f"  {cmd[:70]}\n      {why}")

# Stop hook (reply length). dreaming 2026-11-02: (last user message, assistant reply, expect_block, text the reason must hold)
import tempfile, os
LONG = " ".join(["word"] * 140)
HOOKS = "\n".join(f"{i}. Hook line number {i} about the dog's teeth" for i in range(1, 7))
STOP_CASES = [
    ("what did that fix", "- " + LONG, True, "cut"),                                      # plain status over 130: block, ask for a cut
    ("what did that fix", "- a\n- b\n- c\n- d\n- e", True, "top-level bullets"),       # 5 bullets: names the bullet fault
    ("what did that fix", "- a\n  - https://x.y/1\n  - https://x.y/2\n- b\n- c", False, ""),  # nested URLs are not bullets (1b)
    ("show me the hooks", "Here they are.\n" + HOOKS + "\nPick by number.", False, ""),   # show me: the list is the deliverable (1a)
    ("I don't see any hooks", "Here are the six, in the chat.\n" + HOOKS, False, ""),      # I don't see: same (1a)
    ("ok", "Here is the script.\n```\n" + LONG + "\n```\nSay go.", False, ""),         # fenced block never counts (1b)
    ("reexplain that", LONG, False, ""),                                                   # depth word (1c)
    ("does that make sense to you?", LONG, False, ""),                                     # depth word (1c)
    ("say it dead simple", LONG, False, ""),                                               # depth word (1c)
    ("what did you just do", LONG, False, ""),                                             # depth word (1c)
    ("what did that fix", "Intro line.\n" + HOOKS + "\n" + LONG, True, "not counted"),     # mostly list but the prose is still long: block, says the list was kept
]
for user, asst, expect, must in STOP_CASES:
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w") as f:
        f.write(json.dumps({"type": "user", "message": {"role": "user", "content": user}}) + "\n")
        f.write(json.dumps({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": asst}]}}) + "\n")
    r = subprocess.run([sys.executable, str(HERE / "hook_stop_reply.py")], input=json.dumps({"transcript_path": path}),
                       capture_output=True, text=True)
    os.unlink(path)
    out = r.stdout.strip()
    blocked = '"block"' in out
    good = blocked == expect and (not must or must in out) and r.returncode == 0
    ok &= good
    print(("ok  " if good else "BAD ") + ("BLOCK" if blocked else "allow") + f"  user={user[:28]!r}\n      {out[:150]}")
print("ALL AS EXPECTED" if ok else "FAILURES ABOVE")
sys.exit(0 if ok else 1)
