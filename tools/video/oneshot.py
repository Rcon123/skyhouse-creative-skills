#!/usr/bin/env python3
"""oneshot.py: plan.json in, finished talking-character video ad out.

Audio-first pipeline. The voiceover is the master clock:

  voice     one voiceover for the whole script, word timings, one audio chunk per talking beat
  frames    start frames (one locked master per character, every other frame edited from it)
  clips     talking shots generated FROM their audio chunk, silent B-roll from start frames
  gate      lip-sync score on every talking clip (SyncNet + mouth checks), contact sheets
  assemble  cut list from the word timings, conform, captions, mix, export
  check     final file: sync on the export, transcript vs script, filmstrip at every cut

Run with the venv python:
  tools/video/.venv/bin/python tools/video/oneshot.py <step> <project_dir> [--only id,id] [--force]
  steps: validate | voice | frames | clips | gate | assemble | check | all | status

The plan format is documented in .claude/skills/oneshot-video/references/plan-format.md
"""
import argparse
import glob
import difflib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kie import Kie, KieError, API, CREDIT_USD  # noqa: E402

W, H, FPS = 1080, 1920, 30
PAD = 0.30                 # silence added to head and tail of every talking chunk
WHISPER_MODEL = os.path.expanduser("~/.cache/whisper-models/ggml-base.en.bin")
WHISPER_STRICT = os.path.expanduser("~/.cache/whisper-models/ggml-small.en.bin")   # slower, hears words better; used for the strict word check
MAX_PARALLEL = 6

# ---------------------------------------------------------------- engines
# Talking engines take a start frame + the beat's audio chunk.
def _wan_talk(res):
    return lambda img, aud, prompt, dur: ("wan/2-7-image-to-video", {
        "prompt": prompt, "negative_prompt": "subtitles, captions, on-screen text, watermark, cuts, zoom, extra people",
        "first_frame_url": img, "driving_audio_url": aud, "resolution": res,
        "duration": int(min(15, max(2, math.ceil(dur)))), "prompt_extend": False})


TALK_ENGINES = {
    # Wan 2.7 follows the driving audio at 720p (8 of 9 takes passed the gate on 2026-10-05).
    # At 1080p it ignored the audio on 3 of 3 takes, so 1080p is opt-in and expected to fail.
    "wan27-audio": _wan_talk("720p"),
    "wan27-audio-720": _wan_talk("720p"),
    "wan27-audio-1080": _wan_talk("1080p"),
    "kling-avatar-pro": lambda img, aud, prompt, dur: ("kling/ai-avatar-pro", {
        "image_url": img, "audio_url": aud, "prompt": prompt}),
    "kling-avatar-std": lambda img, aud, prompt, dur: ("kling/ai-avatar-standard", {
        "image_url": img, "audio_url": aud, "prompt": prompt}),
    "infinitalk": lambda img, aud, prompt, dur: ("infinitalk/from-audio", {
        "image_url": img, "audio_url": aud, "prompt": prompt, "resolution": "720p"}),
    "omnihuman": lambda img, aud, prompt, dur: ("omnihuman-1-5", {
        "image_url": img, "audio_url": aud, "prompt": prompt[:300], "output_resolution": "1080"}),
}
TALK_FALLBACK = {"wan27-audio": "kling-avatar-pro", "wan27-audio-720": "kling-avatar-pro", "wan27-audio-1080": "wan27-audio",
                 "kling-avatar-pro": "wan27-audio", "kling-avatar-std": "wan27-audio",
                 "infinitalk": "wan27-audio", "omnihuman": "wan27-audio"}

# B-roll engines take a start frame + a motion prompt. Audio is always dropped.
BROLL_ENGINES = {
    "wan27": lambda img, prompt, dur: ("wan/2-7-image-to-video", {
        "prompt": prompt, "negative_prompt": "subtitles, captions, on-screen text, watermark, talking, moving lips",
        "first_frame_url": img, "resolution": "1080p",
        "duration": int(min(15, max(2, math.ceil(dur)))), "prompt_extend": False}),
    "wan27-720": lambda img, prompt, dur: ("wan/2-7-image-to-video", {
        "prompt": prompt, "negative_prompt": "subtitles, captions, on-screen text, watermark, talking, moving lips",
        "first_frame_url": img, "resolution": "720p",
        "duration": int(min(15, max(2, math.ceil(dur)))), "prompt_extend": False}),
    "omni-flash": lambda img, prompt, dur: ("google/gemini-omni-flash-1-1", {
        "prompt": prompt + " In a single unbroken scene, no cuts. No dialogue. No music. No subtitles, no on-screen text.",
        "first_frame_url": img, "duration": str(min(10, max(4, int(math.ceil(dur / 2.0) * 2)))),
        "aspect_ratio": "9:16", "resolution": "1080p"}),
    "veo-lite": "legacy-veo:veo3_lite",
    "veo-fast": "legacy-veo:veo3_fast",
}
# Native-voice engines: the video model speaks the line itself (voice.mode = "native").
# rate = credits per second at the listed resolution, for estimates. ref = takes a voice clip to lock the voice.
NATIVE_ENGINES = {
    "seedance2-mini": {"model": "bytedance/seedance-2-mini", "family": "seedance", "res": "720p", "min": 4, "max": 15, "rate": 8.2, "ref": True},
    "seedance2-fast": {"model": "bytedance/seedance-2-fast", "family": "seedance", "res": "720p", "min": 4, "max": 15, "rate": 24.8, "ref": True},
    "seedance2": {"model": "bytedance/seedance-2", "family": "seedance", "res": "720p", "min": 4, "max": 15, "rate": 41, "ref": True},
    "seedance25": {"model": "bytedance/seedance-2-5", "family": "seedance", "res": "720p", "min": 4, "max": 30, "rate": 63, "ref": True, "adaptive": True},
    "wan3": {"model": "wan/3-0-video", "family": "wan3", "res": "720P", "min": 2, "max": 30, "rate": 16, "ref": True},
    "minimax-h3": {"model": "minimax-h3/image-to-video", "family": "h3", "res": "768P", "min": 4, "max": 15, "rate": 8, "ref": True},
    "kling3": {"model": "kling-3.0/video", "family": "kling", "res": "std", "min": 3, "max": 15, "rate": 20, "ref": False},
    "veo-lite": {"model": "veo3_lite", "family": "veo", "res": "720p", "min": 8, "max": 8, "rate": 3.75, "ref": False},
    "veo-fast": {"model": "veo3_fast", "family": "veo", "res": "720p", "min": 8, "max": 8, "rate": 7.5, "ref": False},
}
IMAGE_T2I = "gpt-image-2-text-to-image"
IMAGE_EDIT = "gpt-image-2-image-to-image"


# ---------------------------------------------------------------- helpers
def sh(cmd, check=True):
    # stdin closed: ffmpeg in a background job otherwise stops waiting on the terminal
    return subprocess.run(cmd, check=check, capture_output=True, text=True, stdin=subprocess.DEVNULL)


def dur_of(path):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout.strip())


def vdur_of(path):
    """Length of the picture (some models return audio a few frames longer than the video)."""
    out = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "csv=p=0", path], check=False).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return dur_of(path)


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "x x twenty thirty forty fifty sixty seventy eighty ninety".split()


def _num_words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else _ONES[n % 10])
    if n < 1000:   # "a hundred" and "one hundred" both become hundred
        return ("" if n // 100 == 1 else _ONES[n // 100]) + "hundred" + ("" if n % 100 == 0 else _num_words(n % 100))
    if n < 10000:
        return ("" if n // 1000 == 1 else _ONES[n // 1000]) + "thousand" + ("" if n % 1000 == 0 else _num_words(n % 1000))
    return str(n)


ALIASES = {}   # script word -> transcriber spellings that count as that word (plan: voice.aliases)


def _alias(tokens, ref):
    """Map transcriber spellings of a brand or odd word onto the script word. "phosmank" for
    "Fosamax" is whisper's spelling, not a mis-said word. Only words listed in plan voice.aliases
    are mapped, and only when the script actually contains that word."""
    if not ALIASES:
        return tokens
    refset = set(ref)
    out = []
    for t in tokens:
        if t in refset:
            out.append(t)
            continue
        hit = t
        for k, al in ALIASES.items():
            if k in refset and (t in al or difflib.SequenceMatcher(None, t, k).ratio() >= 0.6):
                hit = k
                break
        out.append(hit)
    return out


def norm(word):
    """Lowercase letters and digits only, with digits spelled out so whisper's "$190" matches a
    script's "hundred-and-ninety-dollar" and "68" matches "sixty-eight"."""
    w = word.lower().replace("\u2019", "'")
    money = "$" in w
    w = re.sub(r"(\d+)", lambda m: _num_words(int(m.group(1))) if int(m.group(1)) < 10000 else m.group(1), w)
    w = re.sub(r"[^a-z']", "", w)
    w = w.replace("and", "") if money or "hundred" in w else w
    w = w[:-1] if w == "dollars" else w
    return w + ("dollar" if money and not w.endswith("dollar") else "")


def jload(path, default=None):
    if os.path.exists(path):
        return json.load(open(path))
    return default


def jsave(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    json.dump(obj, open(tmp, "w"), indent=1)
    os.replace(tmp, path)


class Project:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.plan = json.load(open(self.p("plan.json")))
        global ALIASES
        ALIASES = {norm(k): [norm(x) for x in v] for k, v in self.plan.get("voice", {}).get("aliases", {}).items()}
        self.state = jload(self.p("state.json"), {})
        self.kie = Kie(log=self.p("kie_log.jsonl"))
        self.lock = threading.Lock()
        for d in ("voice/chunks", "frames", "clips", "qa", "build"):
            os.makedirs(self.p(d), exist_ok=True)

    def p(self, *parts):
        return os.path.join(self.root, *parts)

    def save(self):
        with self.lock:
            jsave(self.p("state.json"), self.state)

    @property
    def beats(self):
        return self.plan["beats"]

    def beat(self, bid):
        return next(b for b in self.beats if b["id"] == bid)

    def talk_beats(self):
        return [b for b in self.beats if b.get("visual", "talk") == "talk"]

    def broll_shots(self):
        """Every silent clip the edit needs: cutaways inside talk beats + shots of b-roll beats."""
        out = []
        for b in self.beats:
            for c in b.get("cutaways", []):
                out.append((b, c))
            if b.get("visual") == "broll":
                for s in b.get("shots", []):
                    out.append((b, s))
        return out

    def source_items(self):
        """Everything cut from real footage instead of rendered: talk beats with `source`, shots and cutaways with `source`."""
        out = [(b, b) for b in self.beats if b.get("source") and b.get("visual", "talk") == "talk"]
        out += [(b, s) for b, s in self.broll_shots() if s.get("source")]
        return out



# ---------------------------------------------------------------- spend gate (added 2026-10-21)
# Ryan, 2026-10-21, after a twin built from sparse frames + a transcript: "you just spent money without
# following my directions. This cannot happen ever again." Every paid step now refuses unless either
#   (a) the project has a measured reference study: ref/STUDY.md with a filled shot map, ref/cuts.txt and
#       at least one ref/strip_*.jpg (made by `oneshot.py study <project>` from ref/*.mp4), or
#   (b) plan.json says {"reference": "none", "reference_none_because": "<why there is no swipe>"}.
# And a narrator / speaker whose voice did not come out of a casting reel Ryan picked from must carry
# voice.speakers.<name>.cast = "<who picked it, when>" so a borrowed anchor is a declared choice, never a shortcut.
def spend_gate(pr, step):
    plan = pr.plan
    probs = []
    ref = plan.get("reference")
    if ref == "none":
        if not str(plan.get("reference_none_because", "")).strip():
            probs.append("plan.reference is 'none' but reference_none_because is empty: say why there is no swipe for this build")
    else:
        study = pr.p("ref", "STUDY.md")
        strips = glob.glob(pr.p("ref", "strip_*.jpg"))
        if not os.path.exists(study) or not strips or not os.path.exists(pr.p("ref", "cuts.txt")):
            probs.append("no measured reference study: put the swipe in ref/<name>.mp4 and run `oneshot.py study <project>`, "
                         "then fill ref/STUDY.md (or set plan.reference = 'none' with reference_none_because)")
        else:
            txt = open(study).read()
            if "TODO" in txt:
                probs.append("ref/STUDY.md still has TODO rows: every planned shot needs the reference shot it mirrors")
            if "## Shot map" not in txt:
                probs.append("ref/STUDY.md has no '## Shot map' section")
    # Ryan, 2026-10-21, second time: "These are just pictures. You didn't even do a video." On a swipe build every shot
    # moves unless the shot itself declares that the reference shot it mirrors is a still ("ref_still": true) and
    # ref/STUDY.md names that shot under a "still" line. A still-with-push-in is never a default on a twin.
    if ref != "none":
        study_txt = open(pr.p("ref", "STUDY.md")).read().lower() if os.path.exists(pr.p("ref", "STUDY.md")) else ""
        for b in plan.get("beats", []):
            for sh in (b.get("shots") or []) + (b.get("cutaways") or []):
                if sh.get("still") and not sh.get("ref_still"):
                    probs.append(f"shot {sh.get('id')} is a still on a swipe build: the reference animates its drawn scenes. "
                                 f"Render it as a clip, or set \"ref_still\": true only if ref/STUDY.md says the mirrored reference shot is a still.")
                elif sh.get("still") and sh.get("ref_still") and sh.get("id", "").lower() not in study_txt:
                    probs.append(f"shot {sh.get('id')} claims ref_still but ref/STUDY.md never names it")
    # Ryan, 2026-10-21, third time on the voice ("muffled, weird background noise"): the mix bed was at -37 dB and the
    # TTS had been run through a compressor/de-esser chain. On a swipe build the bed stays at or under -50 dB.
    if ref != "none" and float((plan.get("finish") or {}).get("room_tone_db", -54)) > -50:
        probs.append("finish.room_tone_db is louder than -50 dB on a swipe build: the reference narrator is dry; a bed that loud is heard as background noise. Set -54 or lower.")
    # Ryan, 2026-10-21: "why is the voice so shitty?" The voice he picked from a reel was sped up 15% and seated in the cut.
    # A reel-picked voice ships raw: no tempo, no fx.
    v = plan.get("voice", {})
    picked = any("reel" in str(sp.get("cast", "")).lower() or "picked" in str(sp.get("cast", "")).lower() for sp in (v.get("speakers") or {}).values())
    if picked:
        if abs(float(v.get("tempo", 1.0)) - 1.0) > 0.005:
            probs.append("voice.tempo is set on a reel-picked voice: Ryan approved the raw take, ship it raw (tempo 1.0). If the pace is wrong, recast faster.")
        if v.get("fx", "native-kitchen") not in ("none",):
            probs.append("voice.fx is set on a reel-picked voice: Ryan approved the raw take, set fx to 'none'.")
    # Ryan, 2026-10-22: the Meta safe zone (950x979 at y 269..1248) for every video. Captions and the hook card must sit inside it.
    try:
        import safe_zone as _sz
        cap = plan.get("captions") or {}
        if cap.get("enabled", True):
            size = int(cap.get("size", 88)); y = int(cap.get("y", 1150))
            # 2026-10-26: the band's width is the caption's real width (max_chars at this size, bold caps ~0.62 em
            # plus padding), centred, so a short caption low in the frame is not refused for a rail it never touches.
            cw = min(_sz.X1 - _sz.X0, int(cap.get("max_chars", 16)) * size * 0.62 + 2 * 40)
            cx0 = max(_sz.X0, 540 - cw / 2); cx1 = min(_sz.X1, 540 + cw / 2)
            for pr_ in _sz.problems(cx0, y - size * 0.7, cx1, y + size * 0.9, "captions"):
                probs.append(pr_ + " (set captions.y so the band ends above 1248)")
        hk = plan.get("hook_text")
        if hk:
            y = int(hk.get("y", 300)); size = int(hk.get("size", 62))
            for pr_ in _sz.problems(_sz.X0, y - size, _sz.X1, y + size * 2.5, "hook_text"):
                probs.append(pr_)
    except Exception as e:
        probs.append(f"safe zone check could not run: {e}")
    if step in ("native", "voice", "all"):
        for name, sp in (plan.get("voice", {}).get("speakers") or {}).items():
            if sp.get("real"):
                continue
            if not str(sp.get("cast", "")).strip():
                probs.append(f"voice.speakers.{name}.cast is empty: name who picked this voice and when "
                             f"(a reel Ryan picked from, or his OK to reuse an anchor). A borrowed anchor without his word is not allowed.")
    if probs:
        print(f"SPEND GATE: {step} refused.")
        for x in probs:
            print("  - " + x)
        raise SystemExit(2)


def step_study(pr):
    """Measure the reference swipe in ref/: 1 fps strips, cut times, caption frames, and a STUDY.md skeleton to fill."""
    import subprocess
    refs = sorted(glob.glob(pr.p("ref", "*.mp4")))
    if not refs:
        raise SystemExit("study: put the reference video in ref/<name>.mp4 first")
    ref = refs[0]
    rd = pr.p("ref")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ref],
                               capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout.strip() or 0)
    for s0 in range(0, int(dur) + 1, 30):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(s0), "-i", ref, "-t", "30", "-vf", "fps=1,scale=180:-1,tile=10x3",
                        "-frames:v", "1", "-y", os.path.join(rd, f"strip_{s0}s.jpg")], stdin=subprocess.DEVNULL)
    out = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", ref, "-vf", "select='gt(scene,0.2)',showinfo", "-f", "null", "-"],
                         capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr
    cuts = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", out)]
    open(os.path.join(rd, "cuts.txt"), "w").write("\n".join(f"{c:.2f}" for c in cuts) + "\n")
    first20 = [c for c in cuts if c <= 20]
    for name, t in (("caption_0s", 0.5), ("caption_5s", 5.0), ("caption_15s", 15.0), ("caption_mid", dur / 2), ("caption_close", max(0.0, dur - 6))):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", ref, "-frames:v", "1", "-y", os.path.join(rd, f"{name}.png")], stdin=subprocess.DEVNULL)
    study = os.path.join(rd, "STUDY.md")
    if not os.path.exists(study):
        rows = "\n".join(f"| {b['id']} / {s.get('id','')} | TODO: reference time + what is on screen | TODO: why ours mirrors it |"
                         for b in pr.beats for s in (b.get("shots") or b.get("cutaways") or [{}]))
        open(study, "w").write(f"""# Reference study: {os.path.basename(ref)}

Length {dur:.1f} s. Cuts: {len(cuts)} total, {len(first20)} in the first 20 s (one every {20/max(1,len(first20)):.1f} s).
Strips: strip_*.jpg (1 fps, 30 s each). Cut times: cuts.txt. Caption frames: caption_*.png (crop one at full size and copy the typography).

## Cuts
First 20 s: {' '.join(f'{c:.1f}' for c in first20)}

## What the first 20 s shows, second by second
TODO: one line per second from strip_0s.jpg (who, where, what is happening TO them, what text is on screen).

## Typography
TODO: title / caption font, weight, colour, pill, position, hold time (from caption_*.png).

## Where the stakes land
TODO: at what second does the viewer first feel the fear, and what picture does it.

## Shot map (every planned shot beside the reference shot it mirrors)
| our beat / shot | reference shot (time, picture) | why it mirrors |
|---|---|---|
{rows}
""")
    print(f"study: {len(cuts)} cuts ({len(first20)} in the first 20 s), strips and caption frames in ref/. Fill ref/STUDY.md (no TODO left) before any paid step.")


# ---------------------------------------------------------------- validate
def validate(pr):
    plan, errs, warns = pr.plan, [], []
    ids = set()
    frames = plan.get("frames", {})
    for b in pr.beats:
        if b["id"] in ids:
            errs.append(f"duplicate beat id {b['id']}")
        ids.add(b["id"])
        words = len(b["text"].split())
        vis = b.get("visual", "talk")
        if vis == "talk":
            if not b.get("source") and b.get("frame") not in frames:
                errs.append(f"{b['id']}: talk beat needs a frame that exists in frames (got {b.get('frame')!r})")
            if words > 40 and b.get("source"):
                pass                                   # real footage: one beat can carry a whole uninterrupted stretch
            elif words > 40:
                errs.append(f"{b['id']}: {words} words is too long for one talking shot (the engine tops out at 15 seconds). Split at a sentence end or a comma pause (aim 8 to 30 words).")
            elif words > 32 and not b.get("source"):
                warns.append(f"{b['id']}: {words} words will run 12 seconds or more. Fine if cutaways cover part of it; otherwise split it.")
            if words < 5 and not b.get("source"):
                warns.append(f"{b['id']}: {words} words is under 2 seconds. Too short to score lip sync. Merge it or cover it with b-roll.")
        elif vis == "broll":
            if not b.get("shots"):
                errs.append(f"{b['id']}: b-roll beat needs shots")
        else:
            errs.append(f"{b['id']}: visual must be talk or broll")
        if re.search(r"\d", b["text"]):
            warns.append(f"{b['id']}: digits in spoken text. Spell numbers, prices and years as words; use caption_replace for how they should display.")
        for c in b.get("cutaways", []) + (b.get("shots", []) if vis == "broll" else []):
            if c["id"] in ids:
                errs.append(f"duplicate id {c['id']}")
            ids.add(c["id"])
            if not c.get("source") and c.get("frame") not in frames:
                errs.append(f"{c['id']}: frame {c.get('frame')!r} not in frames")
            if c.get("on") and norm(c["on"].split()[0]) not in [norm(w) for w in b["text"].split()]:
                errs.append(f"{c['id']}: 'on' phrase {c['on']!r} not found in the beat text")
            if re.search(r"\b(talk|speak|say|says|conversation|dialogue)", c.get("motion", ""), re.I):
                warns.append(f"{c['id']}: speech words in a b-roll motion prompt make mouths flap. Describe the action only.")
    for b, it in pr.source_items():
        src = it["source"]
        f = _source_file(pr, src.get("file"))
        if not f or not os.path.exists(f):
            errs.append(f"{it['id']}: source file {src.get('file')!r} not found")
        if not (isinstance(src.get("t0"), (int, float)) and isinstance(src.get("t1"), (int, float)) and src["t1"] > src["t0"]):
            errs.append(f"{it['id']}: source needs numeric t0 < t1 (seconds in the footage)")
        if src.get("audio") and not os.path.exists(_source_file(pr, src["audio"])):
            errs.append(f"{it['id']}: source audio {src['audio']!r} not found")
    for fid, f in frames.items():
        for r in f.get("refs", []):
            if r not in frames and not os.path.exists(pr.p(r)) and not os.path.exists(r):
                errs.append(f"frame {fid}: ref {r!r} is not a frame id or a file")
    prev = None
    for b in pr.beats:
        if b.get("visual", "talk") == "talk":
            key = (b.get("frame"), b.get("zoom", 1.0))
            if prev == key and not b.get("allow_jump"):
                warns.append(f"{b['id']}: same frame and zoom as the talking beat before it. The seam will read as a glitch. Change the zoom (1.0 vs 1.12), use another framing, or open the beat on a cutaway.")
            prev = key if not (b.get("cutaways") and b["cutaways"][0].get("on") is None) else None
        else:
            prev = None
    eng = plan.get("talk_engine", "wan27-audio")
    if plan.get("format") in ("drama", "podcast", "interview") and eng.startswith("wan"):
        warns.append("format is " + plan["format"] + " but talk_engine is Wan. Wan follows the audio when the face looks into the lens (8 of 9 takes) and misses "
                     "when the person looks at someone off camera (1 of 5 takes). Set \"talk_engine\": \"kling-avatar-pro\" for scenes shot in singles.")
    total_words = sum(len(b["text"].split()) for b in pr.beats)
    print(f"{len(pr.beats)} beats, {total_words} words, about {total_words / 2.6:.0f}s at 155 wpm")
    # rough cost so nobody is surprised: Wan bills whole seconds at 16 credits, frames 10, voice about 5
    broll = sum(1 for _, s in pr.broll_shots() if not s.get("still") and not s.get("source"))
    todo_frames = sum(1 for f in frames if not os.path.exists(_frame_path(pr, f)))
    if _is_native(pr):
        neng = plan["voice"].get("engine", "seedance2-mini")
        talk = sum(_native_duration(neng, len(b["text"].split())) for b in pr.beats if not b.get("source"))   # every generated line, seen or not
        est = int(talk * NATIVE_ENGINES[neng]["rate"]) + broll * 4 * 16 + todo_frames * 10
    else:
        talk = sum(math.ceil(len(b["text"].split()) / 2.6 + 2 * PAD) for b in pr.talk_beats())
        est = talk * 16 + broll * 4 * 16 + todo_frames * 10 + 5
    try:
        have = float(pr.kie.credits())
    except Exception:
        have = None
    print(f"estimate: {talk}s of talking + {broll} b-roll clips + {todo_frames} frames = about {est} credits (${est * CREDIT_USD:.2f}), "
          f"plan on {int(est * 1.3)} with rerolls." + (f" Balance: {have:.0f} credits." if have is not None else ""))
    if have is not None and have < est * 1.3:
        warns.append(f"balance of {have:.0f} credits is under the {int(est * 1.3)} this build may need. Top up Kie or cut the plan before running clips.")
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    if errs:
        sys.exit(1)
    return warns


# ---------------------------------------------------------------- voice
def _tts_gemini(pr, turns, dest):
    """turns: [{speaker, text, style}] with at most two distinct speakers."""
    vconf = pr.plan["voice"]
    spk = []
    for t in turns:
        if t["speaker"] not in spk:
            spk.append(t["speaker"])
    sid = {s: f"Speaker {i + 1}" for i, s in enumerate(spk)}
    inp = {
        "temperature": vconf.get("temperature", 1),
        "speakers": [{"speaker_id": sid[s], "voice_name": vconf["speakers"][s]["voice_name"]} for s in spk],
        "dialogue_turns": [{"speaker_id": sid[t["speaker"]], "text": t["text"],
                            **({"style": t["style"]} if t.get("style") else {})} for t in turns],
    }
    out = pr.kie.run(vconf.get("model", "google/gemini-3-8-flash-tts"), inp, dest=dest, tag="voice")
    if out["state"] != "success":
        raise KieError(f"voice failed: {out.get('msg')}")
    return dest


def _tts_eleven(pr, turns, dest):
    vconf = pr.plan["voice"]
    parts = []
    for i, t in enumerate(turns):
        s = vconf["speakers"][t["speaker"]]
        part = dest.replace(".wav", f"_{i}.mp3")
        out = pr.kie.run(vconf.get("model", "elevenlabs/text-to-speech-multilingual-v2"), {
            "text": t["text"], "voice": s["voice_id"], "stability": s.get("stability", 0.45),
            "similarity_boost": s.get("similarity_boost", 0.75), "style": s.get("style_exaggeration", 0.1),
            "speed": s.get("speed", 1.0),
            "previous_text": turns[i - 1]["text"] if i else "", "next_text": turns[i + 1]["text"] if i + 1 < len(turns) else ""},
            dest=part, tag="voice")
        if out["state"] != "success":
            raise KieError(f"voice failed: {out.get('msg')}")
        parts.append(part)
    _concat_audio(parts, dest, gap=0.25)
    return dest


def _concat_audio(parts, dest, gap=0.3):
    ins, filt = [], []
    for i, p in enumerate(parts):
        ins += ["-i", p]
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,apad=pad_dur={gap if i + 1 < len(parts) else 0}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[o]")
    sh(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filt), "-map", "[o]", "-c:a", "pcm_s16le", dest])


def whisper_words(wav, model=None):
    tmp = wav + ".16k.wav"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-ar", "16000", "-ac", "1", tmp])
    base = wav + ".whisper"
    sh(["whisper-cli", "-m", model or WHISPER_MODEL, "-f", tmp, "-ojf", "-of", base, "-np"])
    data = json.load(open(base + ".json"))
    os.remove(tmp)
    words, cur = [], None
    for seg in data["transcription"]:
        for t in seg.get("tokens", []):
            txt = t["text"]
            if txt.startswith("[_") or not txt.strip():
                continue
            a, b = t["offsets"]["from"] / 1000.0, t["offsets"]["to"] / 1000.0
            if txt.startswith(" ") or cur is None:
                if cur:
                    words.append(cur)
                cur = {"w": txt.strip(), "s": a, "e": b}
            else:
                cur["w"] += txt
                cur["e"] = max(cur["e"], b)
    if cur:
        words.append(cur)
    return [w for w in words if norm(w["w"])]


def _audio_speech_end(wav, frame=0.02, lift_db=12.0):
    """Where the sound actually stops: the last 20 ms frame that sits well above the clip's noise floor.
    Whisper's end time for the last word is unreliable in both directions; this is measured."""
    import wave, struct, math as _m
    try:
        with wave.open(wav) as w:
            sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
            raw = w.readframes(n)
    except Exception:
        return None
    if sw != 2:
        return None
    vals = struct.unpack(f"<{len(raw) // 2}h", raw)
    if ch > 1:
        vals = vals[::ch]
    step = max(1, int(sr * frame))
    rms = []
    for i in range(0, len(vals) - step + 1, step):
        seg = vals[i:i + step]
        rms.append(10 * _m.log10(sum(v * v for v in seg) / step / (32768.0 ** 2) + 1e-12))
    if not rms:
        return None
    floor = sorted(rms)[len(rms) // 10]
    thr = max(floor + lift_db, -45.0)
    last = max([i for i, r in enumerate(rms) if r > thr] or [0])
    return round((last + 1) * frame, 3)


def _audio_speech_start(wav, frame=0.02, lift_db=12.0):
    """First 20 ms frame well above the noise floor (the measured start of the first word)."""
    import wave, struct, math as _m
    try:
        with wave.open(wav) as w:
            sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
            raw = w.readframes(n)
    except Exception:
        return None
    if sw != 2:
        return None
    vals = struct.unpack(f"<{len(raw) // 2}h", raw)
    if ch > 1:
        vals = vals[::ch]
    step = max(1, int(sr * frame))
    rms = []
    for i in range(0, len(vals) - step + 1, step):
        seg = vals[i:i + step]
        rms.append(10 * _m.log10(sum(v * v for v in seg) / step / (32768.0 ** 2) + 1e-12))
    if not rms:
        return None
    floor = sorted(rms)[len(rms) // 10]
    thr = max(floor + lift_db, -45.0)
    first = min([i for i, r in enumerate(rms) if r > thr] or [0])
    return round(first * frame, 3)


def _silences(wav, floor_db=-38, min_len=0.10):
    out = sh(["ffmpeg", "-hide_banner", "-i", wav, "-af", f"silencedetect=noise={floor_db}dB:d={min_len}", "-f", "null", "-"], check=False).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends + [dur_of(wav)] * (len(starts) - len(ends))))


def align(pr, wav):
    """Map every script word to a time. Script words are the truth; whisper only supplies timing."""
    heard = whisper_words(wav)
    script = []
    for b in pr.beats:
        for w in b["text"].split():
            if norm(w):
                script.append({"beat": b["id"], "w": w})
    a = [norm(x["w"]) for x in script]
    h = [norm(x["w"]) for x in heard]
    sm = difflib.SequenceMatcher(None, a, h, autojunk=False)
    matched = 0
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            script[i + k]["s"], script[i + k]["e"] = heard[j + k]["s"], heard[j + k]["e"]
            matched += 1
    total = dur_of(wav)
    # fill words whisper missed by spreading them between their timed neighbours
    i = 0
    while i < len(script):
        if "s" in script[i]:
            i += 1
            continue
        j = i
        while j < len(script) and "s" not in script[j]:
            j += 1
        left = script[i - 1]["e"] if i else 0.0
        right = script[j]["s"] if j < len(script) else total
        step = (right - left) / (j - i + 1)
        for k in range(i, j):
            script[k]["s"] = left + step * (k - i + 0.1)
            script[k]["e"] = left + step * (k - i + 1)
            script[k]["guess"] = True
        i = j
    # whisper stretches a word across the pause after it; pull ends back to where sound stops
    sil = _silences(wav)
    for w in script:
        for s0, s1 in sil:
            if w["s"] + 0.08 < s0 < w["e"]:
                w["e"] = s0 + 0.03
                break
    ratio = matched / max(1, len(script))
    return script, ratio, sil, total


def step_voice(pr, force=False):
    spend_gate(pr, "voice")
    master = pr.p("voice/master.wav")
    if os.path.exists(master) and pr.state.get("words") and not force:
        print("voice: exists (use --force to redo)")
        return
    vconf = pr.plan["voice"]
    provider = vconf.get("provider", "gemini")
    # a recorded read dropped in as voice/master.wav is used as is: aligned and chunked, never regenerated
    recorded = provider == "recorded" or (os.path.exists(master) and not pr.state.get("words") and not force)
    default_speaker = next(iter(vconf["speakers"]))
    turns = []
    for b in pr.beats:
        spk = b.get("speaker", default_speaker)
        style = b.get("style") or vconf["speakers"][spk].get("style")
        if turns and turns[-1]["speaker"] == spk and turns[-1]["style"] == style:
            turns[-1]["text"] += " " + b["text"]
        else:
            turns.append({"speaker": spk, "text": b["text"], "style": style})
    # a TTS call holds at most two voices; split into runs that respect that
    groups, cur = [], []
    for t in turns:
        if len({x["speaker"] for x in cur} | {t["speaker"]}) > 2:
            groups.append(cur)
            cur = []
        cur.append(t)
    groups.append(cur)
    parts = []
    joined = pr.p("voice/joined.wav")
    if recorded:
        if not os.path.exists(master):
            raise SystemExit("voice.provider is recorded: put the read at voice/master.wav first")
        print("voice: using the recorded read at voice/master.wav")
        shutil.copy(master, pr.p("voice/recorded_original.wav"))
        shutil.copy(master, joined)
    else:
        for gi, g in enumerate(groups):
            raw = pr.p(f"voice/raw_{gi}.wav")
            (_tts_gemini if provider == "gemini" else _tts_eleven)(pr, g, raw)
            parts.append(raw)
        _concat_audio(parts, joined, gap=0.35)
    # peak-normalize to -3 dBFS, mono 48k, keep it dry
    vd = sh(["ffmpeg", "-hide_banner", "-i", joined, "-af", "volumedetect", "-f", "null", "-"], check=False).stderr
    peak = float(re.search(r"max_volume: ([-\d.]+) dB", vd).group(1))
    tempo = float(vconf.get("tempo", 1.0))   # 0.9 slows a rushed read by 10% before anything is generated from it
    tfilt = f"atempo={tempo}," if abs(tempo - 1.0) > 0.005 else ""
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", joined, "-af", f"{tfilt}highpass=f=60,volume={-3 - peak:.2f}dB",
        "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", master])

    words, ratio, sil, total = align(pr, master)
    wpm = len(words) / max(1.0, total) * 60
    print(f"voice: {total:.1f}s, {len(words)} words, {wpm:.0f} words a minute, {ratio:.0%} of script words heard by whisper")
    if wpm > 180:
        print("WARN  faster than 180 words a minute. Lip sync and older viewers both do better near 150. Add pace direction to the speaker style (unhurried, clear pauses between sentences) and rerun voice --force.")
    if ratio < 0.9:
        print("WARN  under 90% matched: listen to voice/master.wav, the read may have skipped or changed words. Fix the text or redo with --force.")
    # beat spans and cut points (middle of the pause between beats)
    spans = {}
    for b in pr.beats:
        ws = [w for w in words if w["beat"] == b["id"]]
        spans[b["id"]] = [ws[0]["s"], ws[-1]["e"]]
    order = [b["id"] for b in pr.beats]
    cuts = [0.0]
    for x, y in zip(order, order[1:]):
        lo, hi = spans[x][1], spans[y][0]
        cuts.append(max(lo, min(hi, (lo + hi) / 2)) if hi > lo else lo)
    cuts.append(total)
    beats = {}
    for i, bid in enumerate(order):
        beats[bid] = {"start": round(spans[bid][0], 3), "end": round(spans[bid][1], 3),
                      "cut_in": round(cuts[i], 3), "cut_out": round(cuts[i + 1], 3), "clip_offset": PAD}
    pr.state["words"] = [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in w.items()} for w in words]
    pr.state["beats"] = beats
    pr.state["voice"] = {"duration": round(total, 3), "match": round(ratio, 3)}
    # one padded chunk per talking beat
    for b in pr.talk_beats():
        t = beats[b["id"]]
        d = t["cut_out"] - t["cut_in"]
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", master, "-af",
            f"atrim={t['cut_in']}:{t['cut_out']},asetpts=N/SR/TB,adelay={int(PAD * 1000)}:all=1,apad=pad_dur={PAD}",
            "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", pr.p(f"voice/chunks/{b['id']}.wav")])
        note = ""
        if d > 14.3:
            note = "  ERROR over the 15 second engine limit with padding: split this beat and rerun voice --force"
        elif d > 12.5:
            note = "  WARN long talking beat"
        if d < 2.0:
            note = "  WARN under 2s, cannot be lip-sync scored"
        print(f"  {b['id']}: {t['cut_in']:.2f} to {t['cut_out']:.2f} ({d:.1f}s){note}")
    pr.save()


# ---------------------------------------------------------------- native voice
# voice.mode = "native": the video model generates the voice with the picture. A text-to-speech read
# was graded "super fake" (2026-10-05); the voices that pass as real come out of the video models.
# One clip is cast as the voice anchor, and every other line is generated with that clip's audio as
# a voice reference so one person speaks the whole ad. Each clip is then checked by machine: did it
# say the exact words, is it the same voice, does the mouth follow.
DEFAULT_VOICE_BLOCK = ("A real person talking, not a person reading. Unhurried but continuous, with audible breath, uneven pauses "
                       "and slightly swallowed word endings. Close to the phone mic, with the natural sound of the room around them. One take.")


def _is_native(pr):
    return pr.plan.get("voice", {}).get("mode") == "native"


def _speaker_of(pr, b):
    return b.get("speaker") or next(iter(pr.plan["voice"]["speakers"]))


def _native_frame(pr, b):
    if b.get("frame"):
        return b["frame"]
    spk = _speaker_of(pr, b)
    conf = pr.plan["voice"]["speakers"][spk]
    if conf.get("frame"):
        return conf["frame"]
    for x in pr.talk_beats():           # a line heard over b-roll still needs a face to be generated from
        if _speaker_of(pr, x) == spk:
            return x["frame"]
    raise SystemExit(f"{b['id']}: no frame to generate this speaker from")


def _native_request(pr, b, eng, img, anchor, dur):
    e = NATIVE_ENGINES[eng]
    spk = pr.plan["voice"]["speakers"][_speaker_of(pr, b)]
    voice = spk.get("voice") or spk.get("style") or DEFAULT_VOICE_BLOCK
    perf = b.get("performance") or "Talks straight to the camera, natural and conversational."
    scene = (f"Vertical phone video filmed in one unbroken take, no cuts, no zoom. {perf} Small natural head movements and blinks.")
    tail = "Audio: the voice and quiet room tone only. No music. No subtitles, no captions, no on-screen text."
    line = b["text"]
    # voice.respell / beat.respell: {"jowls": "jowels"} swaps a spelling in the prompt's dialogue line only.
    # The script text, captions and word audits keep the real word.
    for k, v in (pr.plan["voice"].get("respell") or {}).items() | (b.get("respell") or {}).items():
        line = re.sub(rf"\b{re.escape(k)}\b", v, line, flags=re.I)
    pron = b.get("pronounce") or pr.plan.get("pronounce") or {}
    hint = ("\nPronunciation: " + "; ".join(f"{k} is said {v}" for k, v in pron.items()) + "\n") if pron else ""
    body = (f"{scene}\n\nVOICE: {voice}\n\nSPOKEN DIALOGUE, EXACTLY: \"{line}\"{hint}\n"
            "Say every word exactly once, in order, with no stutter, no repeated word and no false start.\n\n"
            f"{tail}")
    fam = e["family"]
    if fam == "seedance":
        if anchor:
            return e["model"], {"prompt": "@Image 1 is the first frame: it defines the person, their clothes and the room, keep all of it. "
                                          "@Audio 1 is this person's voice: keep exactly this voice, accent, pitch and pace.\n" + body,
                                "reference_image_urls": [img], "reference_audio_urls": [anchor], "generate_audio": True,
                                "resolution": e["res"], "aspect_ratio": "9:16", "duration": dur}
        return e["model"], {"prompt": body, "first_frame_url": img, "generate_audio": True, "resolution": e["res"],
                            "aspect_ratio": "adaptive" if e.get("adaptive") else "9:16", "duration": dur}
    if fam == "wan3":
        if anchor:
            return e["model"], {"prompt": "Image1 is the first frame: it defines the person, their clothes and the room, keep all of it. "
                                          "Audio1 is this person's voice: keep exactly this voice, accent, pitch and pace.\n" + body,
                                "reference_image_urls": [img], "reference_audio_urls": [anchor], "resolution": e["res"],
                                "aspect_ratio": "9:16", "duration": dur, "audio": True}
        return e["model"], {"prompt": body, "first_frame_url": img, "resolution": e["res"], "aspect_ratio": "9:16", "duration": dur, "audio": True}
    if fam == "h3":
        if anchor:
            return "minimax-h3/reference-to-video", {"prompt": "The first reference image defines the person, clothes and room. The reference audio is "
                                                     "this person's voice: keep exactly this voice.\n" + body, "reference_image_urls": [img],
                                                     "reference_audio_urls": [anchor], "aspect_ratio": "9:16", "duration": dur, "resolution": e["res"]}
        return e["model"], {"prompt": body, "first_frame_url": img, "duration": dur, "resolution": e["res"]}
    if fam == "kling":
        return e["model"], {"prompt": f"{scene}\n[Speaker: {voice}]\n[Speaker, natural]: \"{line}\"\nQuiet room tone. No music. No subtitles.",
                            "image_urls": [img], "sound": True, "duration": str(dur), "aspect_ratio": "9:16", "mode": e["res"], "multi_shots": False}
    raise SystemExit(f"native engine {eng} has no request builder")


def _native_duration(eng, words, bump=0):
    e = NATIVE_ENGINES[eng]
    # tight on purpose: a clip longer than the line makes the model pad it with repeats or a slow read
    return int(min(e["max"], max(e["min"], math.ceil(words / 2.8 + 0.5) + bump)))


def _spaced_number_words(n):
    """0 to 999,999 as separate words: 2000 -> two thousand, 1200 -> one thousand two hundred, 43 -> forty three."""
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
    tens = "x x twenty thirty forty fifty sixty seventy eighty ninety".split()

    def under1000(k):
        out = []
        if k >= 100:
            out += [ones[k // 100], "hundred"]
            k %= 100
        if k >= 20:
            out.append(tens[k // 10])
            k %= 10
            if k:
                out.append(ones[k])
        elif k or not out:
            out.append(ones[k])
        return out
    if n < 1000:
        return under1000(n)
    return under1000(n // 1000) + ["thousand"] + (under1000(n % 1000) if n % 1000 else [])


def _expand_numbers(heard):
    """Whisper writes "two thousand dollars" as "$2,000" and "eleven" as "11". Scripts spell numbers as words, so a
    heard money or number token is expanded into number words (sharing the token's time span) before matching.
    Without this a correct line scored 85% and was rerolled three times (ProDenta b04, 2026-10-20)."""
    out = []
    for x in heard:
        raw = x["w"].strip(".,?!;:")
        m = re.fullmatch(r"(\$)?(\d[\d,]*)(\.\d+)?", raw)
        if not m or not m.group(2).replace(",", "").isdigit():
            out.append(x)
            continue
        n = int(m.group(2).replace(",", ""))
        words = _spaced_number_words(n) if n < 1000000 else [raw]
        if m.group(1):
            words = words + ["dollars"]
        span = (x["e"] - x["s"]) / max(1, len(words))
        for i, w in enumerate(words):
            out.append({"w": w, "s": x["s"] + span * i, "e": x["s"] + span * (i + 1)})
    return out


def _clip_words(clip, text):
    """Whisper on the clip's own audio, mapped onto the script words. Returns (words, match ratio, speech start, speech end)."""
    wav = clip + ".a.wav"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", clip, "-vn", "-ac", "1", "-ar", "48000", wav])
    heard = _expand_numbers(whisper_words(wav))
    script = [{"w": w} for w in text.split() if norm(w)]
    a, h = [norm(x["w"]) for x in script], [norm(x["w"]) for x in heard]
    h = _alias(h, a)
    sm = difflib.SequenceMatcher(None, a, h, autojunk=False)
    hit = 0
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            script[i + k]["s"], script[i + k]["e"] = heard[j + k]["s"], heard[j + k]["e"]
            hit += 1
    total = dur_of(wav)
    timed = [w for w in script if "s" in w]
    if not timed:
        return script, 0.0, 0.0, total, wav
    i = 0
    while i < len(script):                 # spread untimed words between timed neighbours
        if "s" in script[i]:
            i += 1
            continue
        j = i
        while j < len(script) and "s" not in script[j]:
            j += 1
        left = script[i - 1]["e"] if i else max(0.0, timed[0]["s"] - 0.3)
        right = script[j]["s"] if j < len(script) else min(total, timed[-1]["e"] + 0.3)
        step = (right - left) / (j - i + 1)
        for k in range(i, j):
            script[k]["s"], script[k]["e"], script[k]["guess"] = left + step * (k - i + 0.1), left + step * (k - i + 1), True
        i = j
    sil = _silences(wav)
    for w in script:
        for s0, s1 in sil:
            if w["s"] + 0.08 < s0 < w["e"]:
                w["e"] = s0 + 0.03
                break
    # whisper often ends the LAST word early; extend it to where the sound actually stops
    last = script[-1]
    for s0, s1 in sil:
        if s0 >= last["e"] - 0.08 and s0 - last["e"] < 0.6:
            last["e"] = max(last["e"], s0)
            break
    else:
        last["e"] = min(total, last["e"] + 0.25)
    # score on number-aware tokens so "$400" against "four hundred dollars" is not a miss
    sa, sh_ = _strict_tokens(text.split()), _strict_tokens([x["w"] for x in heard])
    sh_ = _alias(sh_, sa)
    hit2 = sum(n for _, _, n in difflib.SequenceMatcher(None, sa, sh_, autojunk=False).get_matching_blocks())
    extra = max(0, len(sh_) - hit2)         # words the clip said that the script does not have
    ratio = hit2 / max(1, len(sa)) - 0.5 * extra / max(1, len(sa))
    return script, ratio, script[0]["s"], script[-1]["e"], wav


_NUMWORDS = set(_ONES + _TENS[2:] + ["hundred", "thousand", "dollar", "dollars"])


_CONTRACTIONS = {"wanna": ["want", "to"], "gonna": ["going", "to"], "gotta": ["got", "to"], "kinda": ["kind", "of"],
                 "sorta": ["sort", "of"], "outta": ["out", "of"], "lemme": ["let", "me"], "gimme": ["give", "me"],
                 "dunno": ["do", "not", "know"], "cuz": ["because"], "'cause": ["because"], "ya": ["you"]}


def _strict_tokens(words):
    """Tokens for the word audit: hyphens split, digits spelled out as separate words, and the
    filler inside spoken numbers ("a hundred", "hundred and ninety") dropped on both sides, so
    "sixty-eight-year-old's" and whisper's "68-year-old's" compare equal."""
    out = []
    for w in words:
        w = w.lower().replace("\u2019", "'")
        money = "$" in w
        w = re.sub(r"(\d+)", lambda m: " " + " ".join(re.findall(r"[a-z']+", re.sub(r"([a-z])([A-Z])", r"\1 \2", _num_words_spaced(int(m.group(1)))))) + " " if int(m.group(1)) < 10000 else m.group(1), w)
        parts = [re.sub(r"[^a-z']", "", x) for x in re.split(r"[\s\-]+", w)]
        parts = [y for x in parts if x for y in _CONTRACTIONS.get(x, [x])]   # whisper's "wanna" is "want to"
        if money and parts and parts[-1] not in ("dollar", "dollars"):
            parts.append("dollar")
        out += parts
    cleaned = []
    for i, t in enumerate(out):
        if t == "dollars":
            t = "dollar"
        nxt = out[i + 1] if i + 1 < len(out) else ""
        prv = out[i - 1] if i else ""
        if t == "a" and nxt in ("hundred", "thousand"):
            continue
        if t == "and" and prv in _NUMWORDS and nxt in _NUMWORDS:
            continue
        cleaned.append(t)
    return cleaned


def _num_words_spaced(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return ("" if n // 100 == 1 else _ONES[n // 100] + " ") + "hundred" + ("" if n % 100 == 0 else " " + _num_words_spaced(n % 100))
    return ("" if n // 1000 == 1 else _ONES[n // 1000] + " ") + "thousand" + ("" if n % 1000 == 0 else " " + _num_words_spaced(n % 1000))


def _join_compounds(toks, ref):
    """Merge two or three adjacent tokens when their concatenation is a token in ref."""
    refset = set(ref)
    out, i = [], 0
    while i < len(toks):
        hit = False
        for n in (3, 2):
            j = "".join(toks[i:i + n])
            if len(toks[i:i + n]) == n and j in refset and j not in toks[i:i + n]:
                out.append(j)
                i += n
                hit = True
                break
        if not hit:
            out.append(toks[i])
            i += 1
    return out


def second_ear(b, clip, runs=2):
    """Gemini listens to the clip and writes down exactly what it hears. Whisper collapses a stuttered
    or doubled word into one ("face face" -> "face"); Gemini does not. Any run that hears a doubled word
    or phrase the script does not have is a fault. Returns {"faults", "heard", "ok"}."""
    import voice_judge
    a = _strict_tokens(b["text"].split())
    faults, heard = [], []
    for _ in range(runs):
        r = voice_judge.transcribe(clip, 0, 16)
        if "error" in r:
            continue
        txt = re.sub(r"\[.*?\]", " ", str(r.get("verbatim", "")))
        h = _alias(_strict_tokens(txt.split()), a)
        heard.append(" ".join(h))
        for n in (1, 2, 3):
            for i in range(len(h) - 2 * n + 1):
                if h[i:i + n] == h[i + n:i + 2 * n]:
                    ph = " ".join(h[i:i + n])
                    if not any(a[j:j + 2 * n] == h[i:i + 2 * n] for j in range(len(a))):
                        f = f"repeat: {ph} {ph}"
                        if f not in faults:
                            faults.append(f)
    return {"faults": faults, "heard": heard, "ok": not faults}


def strict_word_audit(pr, b, clip):
    """Word-for-word audit of a clip against the script: every inserted word (a stutter, a repeat,
    an ad-lib), every dropped word, and every substituted word that does not look like a transcriber
    spelling of the script word, is a fault. Uses the bigger whisper model when it is installed."""
    wav = clip + ".strict.wav"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", clip, "-vn", "-ac", "1", "-ar", "48000", wav])
    model = WHISPER_STRICT if os.path.exists(WHISPER_STRICT) else WHISPER_MODEL
    heard = whisper_words(wav, model)
    a = _strict_tokens(b["text"].split())
    h = _alias(_strict_tokens([x["w"] for x in heard]), a)
    h = _join_compounds(h, a)        # "skin care" heard for "skincare" is a spelling, not a fault
    a = _join_compounds(a, h)        # and the other way round ("skin care" in the script)
    sm = difflib.SequenceMatcher(None, a, h, autojunk=False)
    faults = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                want, got = a[i1 + k], h[j1 + k]
                if difflib.SequenceMatcher(None, want, got).ratio() < 0.75:
                    faults.append(f"'{want}' heard as '{got}'")
            continue
        if tag in ("insert", "replace") and (j2 - j1) > (i2 - i1):
            faults.append("extra: " + " ".join(h[j1:j2]))
        if tag in ("delete", "replace") and (i2 - i1) > (j2 - j1):
            faults.append("missing: " + " ".join(a[i1:i2]))
    return {"faults": faults, "heard": " ".join(x["w"] for x in heard), "ok": not faults}


def render_native(pr, b, anchor_url=None, bump=0, engine=None):
    bid = b["id"]
    eng = engine or b.get("voice_engine") or pr.plan["voice"].get("engine", "seedance2-mini")
    e = NATIVE_ENGINES[eng]
    img = pr.kie.upload(_frame_path(pr, _native_frame(pr, b)))
    dur = _native_duration(eng, len(b["text"].split()), bump)
    dest = pr.p(f"clips/{bid}.mp4")
    if os.path.exists(dest):
        os.replace(dest, pr.p(f"clips/{bid}.prev{int(time.time())}.mp4"))
    if e["family"] == "veo":
        spk = pr.plan["voice"]["speakers"][_speaker_of(pr, b)]
        prompt = (f"They say: {b['text']} (no subtitles, no captions, no on-screen text)\n"
                  f"Visual: one unbroken phone take, no cuts. {b.get('performance', 'Talks straight to the camera.')}\n"
                  f"Voice: {spk.get('voice') or spk.get('style') or DEFAULT_VOICE_BLOCK}\nAudio: the voice and quiet room tone only. No music.")
        ok = _legacy_veo(pr, e["model"], img, prompt, dest, f"native:{bid}:{eng}", silent=False)
        state = "success" if ok else "fail"
    else:
        model, inp = _native_request(pr, b, eng, img, anchor_url if e["ref"] else None, dur)
        resume, remember = _pending(pr, bid)
        if bump:
            resume = None
        out = pr.kie.run(model, inp, dest=dest, tag=f"native:{bid}:{eng}", timeout=2400, task_id=resume, on_submit=remember)
        state = out["state"]
        if state != "timeout":
            _settled(pr, bid)
        if state != "success":
            print(f"  native {bid} [{eng}]: {state} {out.get('msg') or ''}", flush=True)
    with pr.lock:
        c = pr.state.setdefault("clips", {}).get(bid, {})
        pr.state["clips"][bid] = {"engine": eng, "state": state, "attempts": c.get("attempts", 0) + 1, "seconds": dur}
    pr.save()
    return state == "success"


def _animal_faces(pr):
    """plan "faces": "animal" (dogs, creatures): MediaPipe finds no face, so NO_FACE is judged by eye, not rerolled."""
    return (pr.plan.get("faces") or pr.plan.get("voice", {}).get("faces")) == "animal"


def _animal_sync_ok(pr, g):
    """SyncNet is trained on human mouths and scores a long muzzle near zero even when the jaw works with the words
    (golden retriever, 2026-10-20: confidence 0.5 to 2.7 with the mouth moving through all of speech). For animal faces
    a FAIL is downgraded to by-eye review when the gate's own mouth stage saw the mouth move during speech and
    not flap in silence."""
    if not _animal_faces(pr) or g.get("verdict") != "FAIL":
        return False
    m = g.get("mouth") or {}
    return m.get("frozen_in_speech_s", 9) <= 0.5 and m.get("flap_in_silence_s", 9) <= 1.0 and m.get("speech_ratio", 0) >= 0.35


def _native_qa(pr, b, anchor_path):
    """Words, voice, sync for one native clip. Returns a dict with ok + reasons."""
    import sync_gate
    bid = b["id"]
    clip = pr.p(f"clips/{bid}.mp4")
    words, ratio, s0, s1, wav = _clip_words(clip, b["text"])
    total = min(dur_of(wav), vdur_of(clip))
    res = {"match": round(ratio, 3), "speech": [round(s0, 3), round(s1, 3)], "clip_seconds": round(total, 2), "reasons": []}
    if ratio < 0.9:
        res["reasons"].append(f"said the line only {ratio:.0%} right")
    # a line that reaches the clip's end is cut off unless every word was heard whole and a sliver remains
    a_end = _audio_speech_end(wav)
    if a_end is not None:
        res["audio_end"] = a_end
        if a_end - s1 > 0.5:
            res["reasons"].append(f"sound goes on {a_end - s1:.1f} s after the last word (a repeat, a laugh or a breath the transcriber skipped)")
            res["tail_noise"] = True
    if a_end is not None and total - a_end < 0.08 and ratio < 1.0 or a_end is None and total - s1 < 0.12 and (ratio < 1.0 or total - s1 < 0.03):
        res["reasons"].append("line runs to the very end of the clip (probably cut off)")
        res["cut_off"] = True
    nw = len([w for w in b["text"].split() if norm(w)])
    wps = nw / max(0.3, s1 - s0)
    res["wps"] = round(wps, 2)
    min_wps = float(pr.plan["voice"].get("min_wps", 0))
    if min_wps and wps < min_wps:
        res["reasons"].append(f"too slow: {wps * 60:.0f} words a minute, floor is {min_wps * 60:.0f}")
    if anchor_path and os.path.exists(anchor_path):
        import voice_match
        sim = voice_match.similarity(anchor_path, wav)
        res["voice_sim"] = round(sim, 3)
        if sim < pr.plan["voice"].get("min_similarity", 0.5):
            res["reasons"].append(f"voice similarity {sim:.2f} to the anchor: sounds like someone else")
    if b.get("visual", "talk") == "talk":
        g = sync_gate.gate(clip, None)
        jsave(pr.p(f"qa/{bid}.gate.json"), g)
        sn = g.get("syncnet") or {}
        res["gate"] = {"verdict": g["verdict"], "offset": sn.get("offset_frames"), "conf": sn.get("confidence"), "shift": g.get("shift_frames", 0)}
        if (g["verdict"] == "NO_FACE" and _animal_faces(pr)) or _animal_sync_ok(pr, g):
            res["no_face_by_eye"] = True
            res["gate"]["verdict"] = "ANIMAL_BY_EYE"
        elif g["verdict"] in ("FAIL", "NO_FACE"):
            res["reasons"].append("lip sync " + g["verdict"] + ": " + "; ".join(g.get("reasons") or []))
        elif g["verdict"] == "REVIEW" and pr.plan["voice"].get("strict_sync") and not b.get("source"):
            # an on-screen mouth that moves through a pause reads as bad sync to a viewer (TPS kid v2, 2026-10-16)
            res["reasons"].append("lip sync REVIEW: " + "; ".join(g.get("reasons") or []))
    if pr.plan["voice"].get("strict_words"):
        sw = strict_word_audit(pr, b, clip)
        res["strict"] = sw
        if not sw["ok"]:
            res["reasons"].append("word audit: " + "; ".join(sw["faults"]))
        if pr.plan["voice"].get("second_ear"):
            se = second_ear(b, clip)
            res["second_ear"] = se
            if not se["ok"]:
                res["reasons"].append("second ear: " + "; ".join(se["faults"]))
            sw["ok"] = sw["ok"] and se["ok"]
    rules = pr.plan["voice"].get("phoneme_gate") or {}
    if rules and any(re.sub(r"[^a-z']", "", w["w"].lower()) in rules for w in words):
        import phonemes
        pg = phonemes.gate(wav, words, rules)
        res["phonemes"] = pg
        if not pg["ok"]:
            res["reasons"].append("pronunciation: " + "; ".join(pg["faults"]))
        if "strict" in res:
            res["strict"]["ok"] = res["strict"]["ok"] and pg["ok"]
    if b.get("source"):
        res["notes"], res["reasons"] = res["reasons"], []        # real footage: measured for the record, never rerolled
    res["ok"] = not res["reasons"]
    res["words"] = words
    return res


def _source_file(pr, f):
    if not f:
        return None
    for cand in (f, pr.p(f), os.path.join(os.getcwd(), f)):
        if os.path.exists(cand):
            return os.path.abspath(cand)
    return f


def cut_source_clips(pr, only=None, force=False):
    """Real footage as clips. `source` on a talk beat (its own audio is the line) or on a shot/cutaway (picture only):
       {"file": "path.mp4", "t0": 7.62, "t1": 9.64, "crop": [x, y, w, h] (fractions, optional),
        "audio": "stem.mp3" (optional, replaces the footage audio), "audio_offset": 5.47 (footage time where the stem starts),
        "keep_captions": true (the footage has captions burned in; ours are not drawn over it)}
    The clip is written to clips/<id>.mp4 once and never re-rendered; it is treated like any other clip after that."""
    done = []
    for b, it in pr.source_items():
        sid = it["id"]
        if only and sid not in only:
            continue
        dest = pr.p(f"clips/{sid}.mp4")
        if os.path.exists(dest) and not force:
            continue
        src = it["source"]
        f = _source_file(pr, src["file"])
        t0, t1 = float(src["t0"]), float(src["t1"])
        vf = []
        if src.get("crop"):
            x, y, w, h = src["crop"]
            vf.append(f"crop=iw*{w}:ih*{h}:iw*{x}:ih*{y}")
        vf.append(f"fps={FPS},scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,format=yuv420p")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", f]
        if src.get("audio"):
            off = float(src.get("audio_offset", 0.0))
            cmd += ["-ss", f"{max(0.0, t0 - off):.3f}", "-to", f"{max(0.0, t1 - off):.3f}", "-i", _source_file(pr, src["audio"]), "-map", "0:v:0", "-map", "1:a:0"]
        else:
            cmd += ["-map", "0:v:0", "-map", "0:a?"]
        cmd += ["-vf", ",".join(vf), "-c:v", "libx264", "-preset", "fast", "-crf", "15", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", dest]
        sh(cmd)
        with pr.lock:
            pr.state.setdefault("clips", {})[sid] = {"engine": "source", "state": "success", "file": os.path.relpath(f, pr.root) if f.startswith(pr.root) else f, "t0": t0, "t1": t1}
        done.append(sid)
    if done:
        pr.save()
        print(f"source: cut {len(done)} clip(s) from footage: {', '.join(done)}", flush=True)
    return done


def step_native(pr, only=None, force=False):
    """Voice and talking picture in one pass. Replaces voice + talking clips + gate for voice.mode = native."""
    spend_gate(pr, "native")
    vconf = pr.plan["voice"]
    beats = [b for b in pr.beats if not only or b["id"] in only]
    speakers = []
    for b in pr.beats:
        if _speaker_of(pr, b) not in speakers:
            speakers.append(_speaker_of(pr, b))
    qa = pr.state.setdefault("native", {})
    real = {spk for spk, c in vconf["speakers"].items() if c.get("real")}     # a real person heard in source footage: no voice to cast
    speakers = [s for s in speakers if s not in real]
    cut_source_clips(pr, only, force)
    for b in beats:
        if b.get("source") and (force or not qa.get(b["id"], {}).get("ok")):
            r = _native_qa(pr, b, None)
            qa[b["id"]] = {k: v for k, v in r.items() if k != "words"}
            g = r.get("gate") or {}
            print(f"  {b['id']} (footage): words {r['match']:.0%}, sync {g.get('verdict', '-')} {g.get('conf', '')}"
                  + (f"  notes: {'; '.join(r['notes'])}" if r.get("notes") else ""), flush=True)
    pr.save()

    def anchor_path(spk):
        given = vconf["speakers"][spk].get("anchor")
        return pr.p(given) if given else pr.p(f"voice/anchor_{spk}.wav")

    # 1. cast the voice: the anchor beat is generated from the frame alone, its audio becomes the reference
    for spk in speakers:
        ap = anchor_path(spk)
        if os.path.exists(ap) and not (force and not only):
            continue
        cand = [b for b in pr.talk_beats() if _speaker_of(pr, b) == spk] or [b for b in pr.beats if _speaker_of(pr, b) == spk]
        want = vconf["speakers"][spk].get("anchor_beat")
        ab = next((b for b in cand if b["id"] == want), None) or max(cand, key=lambda b: min(len(b["text"].split()), 26))
        print(f"native: casting {spk}'s voice on beat {ab['id']}", flush=True)
        for attempt in range(3):
            if not render_native(pr, ab, None, bump=attempt):
                continue
            r = _native_qa(pr, ab, None)
            qa[ab["id"]] = {k: v for k, v in r.items() if k != "words"}
            print(f"  anchor {ab['id']}: match {r['match']:.0%} {'; '.join(r['reasons'])}", flush=True)
            if r["ok"]:
                a0, a1 = max(0.0, r["speech"][0] - 0.1), min(r["clip_seconds"], r["speech"][1] + 0.15, r["speech"][0] + 13.5)
                sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a0:.3f}", "-t", f"{a1 - a0:.3f}", "-i", pr.p(f"clips/{ab['id']}.mp4"),
                    "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", ap])
                pr.state.setdefault("anchors", {})[spk] = {"beat": ab["id"], "file": os.path.relpath(ap, pr.root)}
                pr.save()
                break
        if not os.path.exists(ap):
            raise SystemExit(f"native: could not cast a clean anchor for {spk}. Look at clips/{ab['id']}.mp4 and the frame it starts from.")

    # 2. every other line, in parallel, with its speaker's anchor as the voice reference
    anchors = {spk: pr.kie.upload(anchor_path(spk)) for spk in speakers}
    anchor_beats = {v["beat"] for v in pr.state.get("anchors", {}).values()}

    def needs(b):
        if b.get("source") or _speaker_of(pr, b) in real:
            return False
        if b["id"] in anchor_beats and not (only and b["id"] in only):
            return False
        return force or (only and b["id"] in only) or not os.path.exists(pr.p(f"clips/{b['id']}.mp4")) or not qa.get(b["id"], {}).get("ok")

    todo = [b for b in beats if needs(b)]
    for round_no in range(int(pr.plan["voice"].get("max_passes", 3))):     # voice.max_passes: cap the reroll loop (1 = render once, read, then decide)
        if not todo:
            break
        print(f"native: rendering {len(todo)} line(s), pass {round_no + 1}", flush=True)
        bump = {b["id"]: (2 if qa.get(b["id"], {}).get("cut_off") else 0) + round_no for b in todo}
        _parallel(list(range(len(todo))), lambda i: render_native(pr, todo[i], anchors[_speaker_of(pr, todo[i])], bump=bump[todo[i]["id"]] if round_no else 0))
        nxt = []
        for b in todo:
            if not os.path.exists(pr.p(f"clips/{b['id']}.mp4")):
                nxt.append(b)
                continue
            r = _native_qa(pr, b, anchor_path(_speaker_of(pr, b)))
            qa[b["id"]] = {k: v for k, v in r.items() if k != "words"}
            g = r.get("gate") or {}
            print(f"  {b['id']}: words {r['match']:.0%}, voice {r.get('voice_sim', '-')}, {r.get('wps', 0) * 60:.0f} wpm, sync {g.get('verdict', '-')} {g.get('conf', '')}"
                  + (f"  -> REDO: {'; '.join(r['reasons'])}" if not r["ok"] else ""), flush=True)
            if not r["ok"]:
                nxt.append(b)
        pr.save()
        todo = nxt
    if todo:
        print(f"native: NEEDS WORK {[b['id'] for b in todo]} (kept the last take of each). See references/qa.md.")
    if not only:
        build_native_master(pr)
    for b in pr.talk_beats():
        if os.path.exists(pr.p(f"clips/{b['id']}.mp4")):
            clip_sheet(pr, b["id"])


def pick_best_takes(pr, only=None):
    """Every reroll is kept as clips/<id>.prevNNN.mp4. Rescore all takes of each beat and promote the
    best one (exact words, not cut off, then the fastest read). A later take is not always the better one."""
    import glob
    for b in pr.beats:
        bid = b["id"]
        if (only and bid not in only) or b.get("source"):
            continue
        takes = sorted(glob.glob(pr.p(f"clips/{bid}.prev*.mp4"))) + ([pr.p(f"clips/{bid}.mp4")] if os.path.exists(pr.p(f"clips/{bid}.mp4")) else [])
        if not takes:
            continue
        scored = []
        given = pr.plan["voice"]["speakers"].get(_speaker_of(pr, b), {}).get("anchor")
        ap = pr.p(given) if given else pr.p(f"voice/anchor_{_speaker_of(pr, b)}.wav")
        for t in takes:
            r = _native_qa_file(pr, b, t, ap)
            exact = r.get("strict", {}).get("ok", r["match"] >= 0.99)
            scored.append((r["ok"], exact, r["match"] >= 0.9, not r.get("cut_off"), r["match"], r.get("wps", 0), t, r))
        scored.sort(key=lambda x: (x[0], x[1], x[2], x[3], round(x[4], 1), x[5]), reverse=True)
        best = scored[0]
        cur = pr.p(f"clips/{bid}.mp4")
        if best[6] != cur:
            if os.path.exists(cur):          # a failed last render leaves no current clip; the best earlier take still gets promoted
                os.replace(cur, pr.p(f"clips/{bid}.prev{int(time.time())}.mp4"))
            shutil.copy(best[6], cur)
        r = best[7]
        if r.get("gate"):
            import sync_gate
            jsave(pr.p(f"qa/{bid}.gate.json"), sync_gate.gate(cur, None))
        pr.state.setdefault("native", {})[bid] = {k: v for k, v in r.items() if k != "words"}
        print(f"  {bid}: best of {len(takes)} takes: words {r['match']:.0%}, {r.get('wps', 0) * 60:.0f} wpm, voice {r.get('voice_sim', '-')}, sync {(r.get('gate') or {}).get('verdict', '-')}"
              + ("" if r["ok"] else f"  (still: {'; '.join(r['reasons'])})"), flush=True)
    pr.save()


def _native_qa_file(pr, b, clip, anchor_path=None):
    """_native_qa on an arbitrary file (used to compare takes). With an anchor it also checks the voice and,
    on a talking beat, the lip sync, so a take that says the words in the wrong voice is never promoted."""
    words, ratio, s0, s1, wav = _clip_words(clip, b["text"])
    total = min(dur_of(wav), vdur_of(clip))
    nw = len([w for w in b["text"].split() if norm(w)])
    res = {"match": round(ratio, 3), "speech": [round(s0, 3), round(s1, 3)], "clip_seconds": round(total, 2), "reasons": [],
           "wps": round(nw / max(0.3, s1 - s0), 2)}
    if ratio < 0.9:
        res["reasons"].append(f"said the line only {ratio:.0%} right")
    a_end = _audio_speech_end(wav)
    if a_end is not None:
        res["audio_end"] = a_end
        if a_end - s1 > 0.5:
            res["reasons"].append(f"sound goes on {a_end - s1:.1f} s after the last word (a repeat, a laugh or a breath the transcriber skipped)")
            res["tail_noise"] = True
    if a_end is not None and total - a_end < 0.08 and ratio < 1.0 or a_end is None and total - s1 < 0.12 and (ratio < 1.0 or total - s1 < 0.03):
        res["reasons"].append("line runs to the very end of the clip (probably cut off)")
        res["cut_off"] = True
    if pr.plan["voice"].get("strict_words"):
        sw = strict_word_audit(pr, b, clip)
        res["strict"] = sw
        if not sw["ok"]:
            res["reasons"].append("word audit: " + "; ".join(sw["faults"]))
        if pr.plan["voice"].get("second_ear"):
            se = second_ear(b, clip)
            res["second_ear"] = se
            if not se["ok"]:
                res["reasons"].append("second ear: " + "; ".join(se["faults"]))
            sw["ok"] = sw["ok"] and se["ok"]
    rules = pr.plan["voice"].get("phoneme_gate") or {}
    if rules and any(re.sub(r"[^a-z']", "", w["w"].lower()) in rules for w in words):
        import phonemes
        pg = phonemes.gate(wav, words, rules)
        res["phonemes"] = pg
        if not pg["ok"]:
            res["reasons"].append("pronunciation: " + "; ".join(pg["faults"]))
        if "strict" in res:
            res["strict"]["ok"] = res["strict"]["ok"] and pg["ok"]
    if anchor_path and os.path.exists(anchor_path):
        import voice_match
        sim = voice_match.similarity(anchor_path, wav)
        res["voice_sim"] = round(sim, 3)
        if sim < pr.plan["voice"].get("min_similarity", 0.5):
            res["reasons"].append(f"voice similarity {sim:.2f} to the anchor: sounds like someone else")
    if b.get("visual", "talk") == "talk" and not b.get("source"):
        import sync_gate
        g = sync_gate.gate(clip, None)
        sn = g.get("syncnet") or {}
        res["gate"] = {"verdict": g["verdict"], "offset": sn.get("offset_frames"), "conf": sn.get("confidence"), "shift": g.get("shift_frames", 0)}
        if (g["verdict"] == "NO_FACE" and _animal_faces(pr)) or _animal_sync_ok(pr, g):
            res["no_face_by_eye"] = True
            res["gate"]["verdict"] = "ANIMAL_BY_EYE"
        elif g["verdict"] in ("FAIL", "NO_FACE"):
            res["reasons"].append("lip sync " + g["verdict"])
    res["ok"] = not res["reasons"]
    return res


def build_native_master(pr):
    """Cut each clip to its speech, join them in script order: that is the voice track and the timeline."""
    parts, beats, words, t = [], {}, [], 0.0
    gate = pr.state.setdefault("gate", {})
    for b in pr.beats:
        bid = b["id"]
        clip = pr.p(f"clips/{bid}.mp4")
        if not os.path.exists(clip):
            raise SystemExit(f"native: missing clip for {bid}")
        ws, ratio, s0, s1, wav = _clip_words(clip, b["text"])
        total = min(dur_of(wav), vdur_of(clip))
        a_start = _audio_speech_start(wav)
        if a_start is not None and s0 - 0.5 < a_start < s0:
            s0 = a_start
            ws[0]["s"] = min(ws[0]["s"], a_start)
        a0 = max(0.0, s0 - b.get("lead_in", 0.10))
        a_end = _audio_speech_end(wav)
        if a_end is not None and s1 < a_end < s1 + 0.5:
            s1 = a_end
            ws[-1]["e"] = max(ws[-1]["e"], a_end)
        a1 = min(total, s1 + b.get("tail_out", 0.18))
        seg = pr.p(f"voice/chunks/{bid}.wav")
        d = a1 - a0
        spk = pr.plan["voice"]["speakers"].get(_speaker_of(pr, b), {})
        gain = 0.0 if b.get("source") else float(spk.get("gain_db", 0.0))
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a0:.3f}", "-t", f"{d:.3f}", "-i", wav, "-af",
            f"loudnorm=I=-18:TP=-2:LRA=11,afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.03):.3f}:d=0.03,volume={gain}dB",
            "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", seg])
        if spk.get("fx") and not b.get("source"):
            # per-speaker room: a generated voice seated next to real footage audio (voice.fx should then be "none")
            import voice_fx
            voice_fx.apply(seg, seg + ".fx.wav", spk["fx"])
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", seg + ".fx.wav", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", seg])
        d = dur_of(seg)
        beats[bid] = {"start": round(t + (s0 - a0), 3), "end": round(t + (s1 - a0), 3), "cut_in": round(t, 3), "cut_out": round(t + d, 3),
                      "clip_offset": round(a0, 3)}
        for w in ws:
            words.append({"beat": bid, "w": w["w"], "s": round(t + w["s"] - a0, 3), "e": round(t + w["e"] - a0, 3)})
        q = pr.state.get("native", {}).get(bid, {}).get("gate")
        if q:
            gate[bid] = {**q, "engine": pr.state.get("clips", {}).get(bid, {}).get("engine")}
        parts.append(seg)
        t += d
    _concat_audio(parts, pr.p("voice/master.wav"), gap=0)
    # voice.tempo: pitch-preserving speed change of the finished voice track. Only legal when no
    # talking face is on screen (a voice-only demo), because it would break lip sync everywhere else.
    tempo = float(pr.plan["voice"].get("tempo", 1.0))
    if abs(tempo - 1.0) > 0.005:
        if pr.talk_beats():
            raise SystemExit("voice.tempo is only allowed when no beat shows the speaker talking (it would break lip sync)")
        raw = pr.p("voice/master_raw.wav")
        os.replace(pr.p("voice/master.wav"), raw)
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", f"atempo={tempo}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", pr.p("voice/master.wav")])
        for b in beats.values():
            for k2 in ("start", "end", "cut_in", "cut_out"):
                b[k2] = round(b[k2] / tempo, 3)
        for w in words:
            w["s"], w["e"] = round(w["s"] / tempo, 3), round(w["e"] / tempo, 3)
        t = t / tempo
    total = dur_of(pr.p("voice/master.wav"))
    k = total / t if t else 1.0
    pr.state["beats"], pr.state["words"] = beats, words
    pr.state["voice"] = {"duration": round(total, 3), "mode": "native", "match": round(sum(pr.state["native"][b["id"]]["match"] for b in pr.beats if b["id"] in pr.state["native"]) / max(1, len(pr.beats)), 3)}
    pr.save()
    wpm = len(words) / max(1.0, total) * 60
    print(f"native: voice track {total:.1f}s, {wpm:.0f} words a minute, {len(parts)} lines")


# ---------------------------------------------------------------- frames
def _frame_path(pr, fid):
    return pr.p(f"frames/{fid}.png")


def _resolve_ref(pr, r):
    if r in pr.plan.get("frames", {}):
        return _frame_path(pr, r)
    return pr.p(r) if os.path.exists(pr.p(r)) else r


def step_frames(pr, only=None, force=False):
    spend_gate(pr, "frames")
    frames = pr.plan.get("frames", {})
    style = pr.plan.get("style_contract", "")
    todo = [f for f in frames if (not only or f in only) and (force or (only and f in only) or not os.path.exists(_frame_path(pr, f)))]
    done = set(f for f in frames if f not in todo and os.path.exists(_frame_path(pr, f)))
    tail = " Vertical 9:16. No text, no captions, no logos, no watermark."

    def render(fid):
        f = frames[fid]
        refs = [_resolve_ref(pr, r) for r in f.get("refs", [])]
        # allow_logos: Ryan asked for the real packs on screen (2026-11-01, Bone in the Bowl); keep the no-text ban, drop the logo ban
        t = tail.replace("no logos, ", "") if f.get("allow_logos") else tail
        prompt = f["prompt"] + (" " + style if style and not f.get("no_style") else "") + t
        if refs:
            model = f.get("model", IMAGE_EDIT)
            urls = [pr.kie.upload(r) for r in refs]
            key = "input_urls" if model.startswith("gpt-image") else ("image_input" if model.startswith("nano-banana") else "image_urls")
            inp = {"prompt": prompt, key: urls, "aspect_ratio": "9:16", "resolution": f.get("resolution", "2K")}
        else:
            model = f.get("model", IMAGE_T2I)
            inp = {"prompt": prompt, "aspect_ratio": "9:16", "resolution": f.get("resolution", "2K")}
        out = pr.kie.run(model, inp, dest=_frame_path(pr, fid), tag=f"frame:{fid}", timeout=600)
        print(f"  frame {fid}: {out['state']} {out.get('msg') or ''}", flush=True)
        return out["state"] == "success"

    # refs first: render in waves so an edit never starts before its source exists
    while todo:
        wave = [f for f in todo if all((r not in frames) or (r in done) for r in frames[f].get("refs", []))]
        if not wave:
            raise SystemExit(f"frames: circular or missing refs among {todo}")
        _parallel(wave, render)
        for f in wave:
            todo.remove(f)
            if os.path.exists(_frame_path(pr, f)):
                done.add(f)
    sheet(pr, [_frame_path(pr, f) for f in frames if os.path.exists(_frame_path(pr, f))], pr.p("qa/frames_sheet.jpg"), labels=list(frames))
    print("frames: look at qa/frames_sheet.jpg before spending on video")


def _parallel(items, fn):
    sem = threading.Semaphore(MAX_PARALLEL)
    res = {}

    def run(it):
        with sem:
            try:
                res[it] = fn(it)
            except Exception as e:  # keep the other renders going
                res[it] = False
                print(f"  {it}: ERROR {str(e)[:200]}", flush=True)
    ts = [threading.Thread(target=run, args=(it,)) for it in items]
    for t in ts:
        t.start()
        time.sleep(0.6)
    for t in ts:
        t.join()
    return res


def sheet(pr, images, dest, labels=None, cols=4, cell=360):
    """Contact sheet with Pillow (the local ffmpeg has no drawtext)."""
    from PIL import Image, ImageDraw, ImageFont
    if not images:
        return
    font = ImageFont.truetype(os.path.join(HERE, "fonts", "Montserrat-VF.ttf"), 22)
    ch = int(cell * 16 / 9)
    rows = math.ceil(len(images) / cols)
    out = Image.new("RGB", (cols * cell, rows * (ch + 30)), (20, 20, 20))
    d = ImageDraw.Draw(out)
    for i, path in enumerate(images):
        im = Image.open(path).convert("RGB")
        im.thumbnail((cell, ch))
        x, y = (i % cols) * cell, (i // cols) * (ch + 30)
        out.paste(im, (x + (cell - im.width) // 2, y + 30))
        d.text((x + 6, y + 3), (labels[i] if labels else os.path.basename(path))[:34], fill=(255, 255, 255), font=font)
    out.save(dest, quality=88)


# ---------------------------------------------------------------- clips
def _legacy_veo(pr, tier, img_url, prompt, dest, tag, silent=True):
    t0 = time.time()
    d = pr.kie._req(f"{API}/veo/generate", {
        "prompt": prompt + (" No dialogue, nobody speaks. No music. No subtitles, no on-screen text." if silent else ""),
        "imageUrls": [img_url], "model": tier, "aspect_ratio": "9:16",
        "generationType": "FIRST_AND_LAST_FRAMES_2_VIDEO", "enableTranslation": False})
    tid = (d.get("data") or {}).get("taskId")
    if not tid:
        raise KieError(f"veo rejected: {d.get('code')} {d.get('msg')}")
    state, msg = "timeout", None
    while time.time() - t0 < 1500:
        r = pr.kie._req(f"{API}/veo/record-info?taskId={tid}").get("data") or {}
        if r.get("successFlag") == 1:
            pr.kie.download(((r.get("response") or {}).get("resultUrls") or [None])[0], dest)
            state = "success"
            break
        if r.get("successFlag") in (2, 3):
            state, msg = "fail", r.get("errorMessage")
            break
        time.sleep(12)
    pr.kie._log({"tag": tag, "model": tier, "taskId": tid, "state": state, "msg": msg,
                 "credits": {"veo3_lite": 30, "veo3_fast": 60}.get(tier), "seconds": round(time.time() - t0, 1)})
    return state == "success"


def _talk_prompt(pr, b):
    base = b.get("performance") or "Talks straight to the camera in a calm, natural, conversational way."
    return (f"{base} Small natural head movements, occasional blink, shoulders steady. The mouth moves only with the speech. "
            "Locked-off camera, single continuous shot, no cuts, no zoom.")


def _pending(pr, cid):
    """(task id to resume or None, callback that records a fresh task id)."""
    def remember(tid):
        with pr.lock:
            pr.state.setdefault("pending", {})[cid] = tid
        pr.save()
    return pr.state.get("pending", {}).get(cid), remember


def _settled(pr, cid):
    with pr.lock:
        pr.state.get("pending", {}).pop(cid, None)


def render_talk(pr, b, engine=None, attempt=0):
    bid = b["id"]
    engine = engine or b.get("engine") or pr.plan.get("talk_engine", "wan27-audio")
    chunk = pr.p(f"voice/chunks/{bid}.wav")
    img = pr.kie.upload(_frame_path(pr, b["frame"]))
    aud = pr.kie.upload(chunk)
    model, inp = TALK_ENGINES[engine](img, aud, _talk_prompt(pr, b), dur_of(chunk))
    if attempt:
        inp = dict(inp, seed=1000 + attempt * 7919) if "seed" not in inp and "wan" in model else inp
    dest = pr.p(f"clips/{bid}.mp4")
    if os.path.exists(dest):
        os.replace(dest, pr.p(f"clips/{bid}.prev{int(time.time())}.mp4"))   # a repair is a new take, never an overwrite
    resume, remember = _pending(pr, bid)
    if attempt:
        resume = None                       # a reroll is always a new task
    out = pr.kie.run(model, inp, dest=dest, tag=f"talk:{bid}:{engine}", timeout=1800, task_id=resume, on_submit=remember)
    if out["state"] != "timeout":
        _settled(pr, bid)
    with pr.lock:
        pr.state.setdefault("clips", {})[bid] = {"engine": engine, "state": out["state"], "msg": out.get("msg"),
                                                 "attempts": pr.state.get("clips", {}).get(bid, {}).get("attempts", 0) + 1}
    pr.save()
    print(f"  talk {bid} [{engine}]: {out['state']} {out.get('msg') or ''}", flush=True)
    return out["state"] == "success"


def render_broll(pr, b, s, engine=None):
    sid = s["id"]
    engine = engine or s.get("engine") or pr.plan.get("broll_engine", "wan27-720")
    need = pr.state.get("segments_need", {}).get(sid, 4.0)
    img = pr.kie.upload(_frame_path(pr, s["frame"]))
    prompt = s["motion"].rstrip(". ") + ". Nobody speaks, lips stay closed. Stable picture, sharp clarity."
    dest = pr.p(f"clips/{sid}.mp4")
    if os.path.exists(dest):
        os.replace(dest, pr.p(f"clips/{sid}.prev{int(time.time())}.mp4"))
    spec = BROLL_ENGINES[engine]
    if isinstance(spec, str):
        ok = _legacy_veo(pr, spec.split(":")[1], img, prompt, dest, f"broll:{sid}:{engine}")
        state = "success" if ok else "fail"
    else:
        model, inp = spec(img, prompt, need + 0.5)
        resume, remember = _pending(pr, sid)
        out = pr.kie.run(model, inp, dest=dest, tag=f"broll:{sid}:{engine}", timeout=1800, task_id=resume, on_submit=remember)
        state = out["state"]
        if state != "timeout":
            _settled(pr, sid)
    with pr.lock:
        pr.state.setdefault("clips", {})[sid] = {"engine": engine, "state": state}
    pr.save()
    print(f"  broll {sid} [{engine}]: {state}", flush=True)
    return state == "success"


def step_clips(pr, only=None, force=False, engine=None):
    spend_gate(pr, "clips")
    if "beats" not in pr.state:
        raise SystemExit("run voice first")
    plan_segments(pr)   # so b-roll knows how long each shot has to be
    cut_source_clips(pr, only, force)
    jobs = []
    for b in ([] if _is_native(pr) else pr.talk_beats()):   # native mode renders talking clips in the native step
        if (only and b["id"] not in only) or (not only and not force and os.path.exists(pr.p(f"clips/{b['id']}.mp4"))):
            continue
        jobs.append(("talk", b, None))
    for b, s in pr.broll_shots():
        if s.get("still") or s.get("source"):
            continue                        # a still is animated at assembly, footage is cut, no render
        if (only and s["id"] not in only) or (not only and not force and os.path.exists(pr.p(f"clips/{s['id']}.mp4"))):
            continue
        jobs.append(("broll", b, s))
    if not jobs:
        print("clips: nothing to render")
        return
    print(f"clips: rendering {len(jobs)}")
    _parallel(list(range(len(jobs))), lambda i: render_talk(pr, jobs[i][1], engine) if jobs[i][0] == "talk" else render_broll(pr, jobs[i][1], jobs[i][2], engine))


# ---------------------------------------------------------------- gate
def clip_sheet(pr, cid, n=6):
    src = pr.p(f"clips/{cid}.mp4")
    d = dur_of(src)
    dest = pr.p(f"qa/{cid}.sheet.jpg")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", f"fps={n}/{d:.3f},scale=270:-1,tile={n}x1", "-frames:v", "1", dest], check=False)
    return dest


def step_gate(pr, only=None, auto=True):
    import sync_gate
    results = pr.state.setdefault("gate", {})
    for b in pr.talk_beats():
        bid = b["id"]
        clip = pr.p(f"clips/{bid}.mp4")
        if (only and bid not in only) or not os.path.exists(clip):
            continue
        native = _is_native(pr)
        for attempt in range(3):
            r = sync_gate.gate(clip, None if native else pr.p(f"voice/chunks/{bid}.wav"))
            jsave(pr.p(f"qa/{bid}.gate.json"), r)
            s = r.get("syncnet") or {}
            results[bid] = {"verdict": r["verdict"], "offset": s.get("offset_frames"), "conf": s.get("confidence"),
                            "shift": r.get("shift_frames", 0), "reasons": r.get("reasons"), "face_px": r.get("face_px"),
                            "engine": pr.state.get("clips", {}).get(bid, {}).get("engine")}
            print(f"  gate {bid}: {r['verdict']} offset={s.get('offset_frames')} conf={s.get('confidence')} {'; '.join(r.get('reasons') or [])}", flush=True)
            if r["verdict"] in ("PASS", "PASS_SHIFT", "REVIEW") or not auto or attempt == 2 or native:
                break
            # A take that misses usually misses again on the same engine with the same frame and audio
            # (1 of 6 same-engine rerolls passed on build night), so go straight to the fallback,
            # and give the fallback one second try.
            eng = pr.state.get("clips", {}).get(bid, {}).get("engine", "wan27-audio")
            nxt = TALK_FALLBACK.get(eng, "kling-avatar-pro") if attempt == 0 else eng
            print(f"  gate {bid}: rerolling on {nxt}", flush=True)
            if not render_talk(pr, b, nxt, attempt + 1):
                break
        clip_sheet(pr, bid)
        pr.save()
    for b, s in pr.broll_shots():
        if s.get("still") or (only and s["id"] not in only) or not os.path.exists(pr.p(f"clips/{s['id']}.mp4")):
            continue
        clip_sheet(pr, s["id"])
    sheets = sorted(f for f in os.listdir(pr.p("qa")) if f.endswith(".sheet.jpg"))
    from PIL import Image
    ims = [Image.open(pr.p("qa", f)) for f in sheets]
    if ims:
        wmax = max(i.width for i in ims)
        out = Image.new("RGB", (wmax, sum(i.height for i in ims)), (0, 0, 0))
        y = 0
        for i in ims:
            out.paste(i, (0, y))
            y += i.height
        out.save(pr.p("qa/clips_sheet.jpg"), quality=85)
    bad = [k for k, v in results.items() if (v["verdict"] == "FAIL" and not _animal_sync_ok(pr, v)) or (v["verdict"] == "NO_FACE" and not _animal_faces(pr))]
    if _animal_faces(pr):
        print("gate: animal faces: the scorer sees no face, so every talking clip is judged by eye on the sheet.")
    print("gate: " + (f"NEEDS WORK {bad}" if bad else "all talking clips pass") + ". Look at qa/clips_sheet.jpg (rows in id order).")


# ---------------------------------------------------------------- assemble
def _phrase_time(words, bid, phrase, which="s"):
    ws = [w for w in words if w["beat"] == bid]
    target = [norm(x) for x in phrase.split() if norm(x)]
    seq = [norm(w["w"]) for w in ws]
    for i in range(len(seq) - len(target) + 1):
        if seq[i:i + len(target)] == target:
            return ws[i]["s"] if which == "s" else ws[i + len(target) - 1]["e"]
    for i, s in enumerate(seq):             # fall back to the first word
        if s == target[0]:
            return ws[i]["s"] if which == "s" else ws[min(len(ws) - 1, i + len(target) - 1)]["e"]
    return None


def plan_segments(pr):
    """The cut list. Every segment is video only; the master voiceover is the only voice track."""
    words, beats = pr.state["words"], pr.state["beats"]
    segs, need = [], {}
    for b in pr.beats:
        t = beats[b["id"]]
        a, z = t["cut_in"], t["cut_out"]
        if b.get("visual", "talk") == "talk":
            cuts = []
            for c in b.get("cutaways", []):
                if c.get("on"):
                    s = (_phrase_time(words, b["id"], c["on"], "s") or a) - c.get("lead", 0.08)
                    e = (_phrase_time(words, b["id"], c["on"], "e") or z) + c.get("tail", 0.25)
                else:                       # no anchor: cover the head of the beat
                    s, e = a, a + c.get("dur", 2.0)
                if c.get("dur") and c.get("on"):
                    e = s + c["dur"]
                s, e = max(a, s), min(z, e)
                if e - s >= 0.6:
                    cuts.append((s, e, c))
            cuts.sort(key=lambda x: x[0])
            cur = a
            for s, e, c in cuts:
                if s < cur:
                    s = cur
                if s - cur >= 0.5:
                    segs.append({"t0": cur, "t1": s, "kind": "talk", "src": b["id"], "beat": b["id"]})
                elif s > cur:
                    s = cur                 # too short to show the face; give the sliver to the cutaway
                if e - s < 0.6:
                    continue
                segs.append({"t0": s, "t1": e, "kind": "broll", "src": c["id"], "beat": b["id"]})
                need[c["id"]] = e - s
                cur = e
            if z - cur >= 0.5:
                segs.append({"t0": cur, "t1": z, "kind": "talk", "src": b["id"], "beat": b["id"]})
            elif segs and z > cur:
                segs[-1]["t1"] = z
                if segs[-1]["kind"] == "broll":
                    need[segs[-1]["src"]] = segs[-1]["t1"] - segs[-1]["t0"]
        else:
            shots = b["shots"]
            marks = []
            for i, s in enumerate(shots):
                tt = _phrase_time(words, b["id"], s["on"], "s") if s.get("on") else None
                marks.append(tt - 0.08 if tt is not None else None)
            marks[0] = a
            for i in range(1, len(marks)):   # unanchored shots split the remaining time evenly
                if marks[i] is None:
                    nxt = next((m for m in marks[i + 1:] if m is not None), z)
                    gap = [k for k in range(i, len(marks)) if marks[k] is None and all(marks[q] is None for q in range(i, k + 1))]
                    marks[i] = marks[i - 1] + (nxt - marks[i - 1]) / (len(gap) + 1)
            marks.append(z)
            for i, s in enumerate(shots):
                segs.append({"t0": marks[i], "t1": marks[i + 1], "kind": "broll", "src": s["id"], "beat": b["id"]})
                need[s["id"]] = marks[i + 1] - marks[i]
    for s in segs:
        if s["t1"] - s["t0"] > 7.0 and s["kind"] == "broll":
            print(f"WARN  {s['src']} holds one picture for {s['t1'] - s['t0']:.1f}s. Split the beat into two or three shots (use 'on' to start each at its words).")
        if s["t1"] - s["t0"] > 9.0 and s["kind"] == "talk":
            print(f"WARN  {s['src']} stays on one talking shot for {s['t1'] - s['t0']:.1f}s. Add a cutaway on a noun in the line.")
    pr.state["segments"] = [{**s, "t0": round(s["t0"], 3), "t1": round(s["t1"], 3)} for s in segs]
    pr.state["segments_need"] = {k: round(v, 2) for k, v in need.items()}
    pr.save()
    return pr.state["segments"]


def _face_center(pr, bid):
    g = jload(pr.p(f"qa/{bid}.gate.json"), {})
    return g.get("face_center")


def _seg_filter(zoom, face=None):
    """Fill 1080x1920, optional punch-in that keeps the face in frame."""
    z = max(1.0, float(zoom))
    sw, shh = int(round(W * z / 2) * 2), int(round(H * z / 2) * 2)
    cx, cy = (face or (0.5, 0.36))
    x = min(max(0, int(cx * sw - W / 2)), sw - W)
    y = min(max(0, int(cy * shh - H * 0.40)), shh - H)
    return (f"fps={FPS},scale={sw}:{shh}:force_original_aspect_ratio=increase,crop={sw}:{shh},"
            f"crop={W}:{H}:{x}:{y},setsar=1,format=yuv420p")


def step_assemble(pr):
    segs = plan_segments(pr)
    beats, gate = pr.state["beats"], pr.state.get("gate", {})
    build = pr.p("build")
    for f in os.listdir(build):
        if f.startswith("seg_"):
            os.remove(os.path.join(build, f))
    listing = []
    frame_cursor = 0
    for i, s in enumerate(segs):
        n = int(round(s["t1"] * FPS)) - int(round(s["t0"] * FPS))
        if n <= 0:
            continue
        out = os.path.join(build, f"seg_{i:03d}.mp4")
        spec = _find_shot(pr, s["src"]) if s["kind"] == "broll" else {}
        src = _frame_path(pr, spec["frame"]) if spec.get("still") else pr.p(f"clips/{s['src']}.mp4")
        if not os.path.exists(src):
            raise SystemExit(f"assemble: missing clip {s['src']}")
        if spec.get("still"):
            # photo on screen: slow push-in toward a focus point (default: center, a little above middle)
            z0, z1 = spec.get("push", [1.0, 1.10])
            fx, fy = spec.get("focus", [0.5, 0.45])
            vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                  f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}':d=1:s={W}x{H}:fps={FPS},"
                  "setsar=1,format=yuv420p")
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-i", src]
        elif s["kind"] == "talk":
            b = pr.beat(s["beat"])
            g = gate.get(s["beat"], {})
            shift = (g.get("shift") or 0) / 25.0    # frames the gate says to slide the picture (+ = start later in the clip)
            inpoint = max(0.0, beats[s["beat"]].get("clip_offset", PAD) + (s["t0"] - beats[s["beat"]]["cut_in"]) + shift)
            zoom, face = b.get("zoom", 1.0), _face_center(pr, s["beat"])
            caps = pr.plan.get("captions") or {}
            if caps.get("enabled", True) and face and zoom < 1.12:
                # the caption band must never sit on the mouth (TPS kid v1, 2026-10-16: every kid line failed sync on the
                # export because the captions covered her mouth). Mouth is about 0.07 of frame height under the face centre.
                band_top = (caps.get("y", 1150) - caps.get("size", 88) * 1.16 - 24) / H
                if face[1] + 0.07 > band_top - 0.03:
                    zoom = 1.14
                    print(f"  {s['beat']}: face centre at {face[1]:.2f} of frame height would sit under the captions; punching in to 1.14", flush=True)
            vf = _seg_filter(zoom, face) + ",tpad=stop_mode=clone:stop_duration=0.4"
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{inpoint:.3f}", "-i", src]
        else:
            have, want = dur_of(src), n / FPS
            start = spec.get("start", 0.0 if spec.get("source") else (0.15 if have - 0.15 >= want else 0.0))
            vf = _seg_filter(spec.get("zoom", 1.0))
            if have - start < want:          # too short: slow it a little, then hold the last frame
                k = min(1.3, want / max(0.1, have - start))
                vf = f"setpts={k:.4f}*PTS," + vf + f",tpad=stop_mode=clone:stop_duration={want:.2f}"
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.3f}", "-i", src]
        cmd += ["-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "15",
                "-g", str(FPS), "-keyint_min", str(FPS), "-video_track_timescale", "15360", out]
        sh(cmd)
        got = int(sh(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out]).stdout.strip() or 0)
        if got != n:
            raise SystemExit(f"assemble: segment {i} ({s['src']}) has {got} frames, wanted {n}. The source clip is too short.")
        listing.append(out)
        frame_cursor += n
    with open(os.path.join(build, "concat.txt"), "w") as fh:
        for path in listing:
            fh.write(f"file '{path}'\n")
    picture = os.path.join(build, "picture.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(build, "concat.txt"), "-c", "copy", picture])

    audio = _mix(pr, frame_cursor / FPS)
    final = pr.p("final.mp4")
    caps = pr.plan.get("captions", {"enabled": True})
    grade = pr.plan.get("finish", {})
    vf_tail = []
    if grade.get("grain", 4):
        vf_tail.append(f"noise=alls={grade.get('grain', 4)}:allf=t")   # one shared grain layer makes clips from different renders read as one camera
    enc = ["-c:v", "libx264", "-profile:v", "high", "-level", "4.2", "-preset", "slow", "-crf", "20", "-maxrate", "8M", "-bufsize", "16M",
           "-g", str(FPS * 2), "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart"]
    skip = []
    for s in segs:
        spec = pr.beat(s["beat"]) if s["kind"] == "talk" else _find_shot(pr, s["src"])
        if (spec.get("source") or {}).get("keep_captions"):
            skip.append([s["t0"], s["t1"]])
    pr.state["caption_skip"] = skip
    pr.save()
    if caps.get("enabled", True) or pr.plan.get("hook_text"):
        import captions
        captions.burn(pr, picture, audio, final, frame_cursor, vf_tail, enc)
    else:
        vf = ",".join(vf_tail) if vf_tail else "null"
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", picture, "-i", audio, "-vf", vf, *enc, "-shortest", final])
    print(f"assemble: {final} ({dur_of(final):.1f}s, {len(listing)} segments)")


def _find_shot(pr, sid):
    for b, s in pr.broll_shots():
        if s["id"] == sid:
            return s
    return {}


def _mix(pr, total):
    """Voice on top, room tone under every seam, optional music ducked under the voice, -14 LUFS."""
    master = pr.p("voice/master.wav")
    # a generated voice is too clean either way: seat it in the room the picture shows
    fx = pr.plan.get("voice", {}).get("fx", "native-kitchen" if _is_native(pr) else "kitchen-phone")
    if fx and fx != "none":
        import voice_fx
        master = voice_fx.apply(master, pr.p("build/voice_fx.wav"), fx)   # channel only, timing untouched
    out = pr.p("build/mix.wav")
    music = (pr.plan.get("music") or {}).get("file")
    tone_db = (pr.plan.get("finish") or {}).get("room_tone_db", -52)
    ins = ["-i", master, "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anoisesrc=color=brown:sample_rate=48000:amplitude=0.6"]
    filt = [f"[0:a]aresample=48000,apad=whole_dur={total:.3f},atrim=0:{total:.3f},asplit=2[v][sc]",
            f"[1:a]lowpass=f=1800,volume={tone_db}dB[tone]"]
    mixin = "[v][tone]"
    n = 2
    if music:
        mpath = music if os.path.isabs(music) else pr.p(music)
        moff = float(pr.plan["music"].get("offset", 0.0))
        ins += ["-stream_loop", "-1", "-ss", f"{moff:.3f}", "-i", mpath]
        mdb = pr.plan["music"].get("db", -24)
        filt.append(f"[2:a]aresample=48000,atrim=0:{total:.3f},volume={mdb}dB,afade=t=in:d=0.5,afade=t=out:st={max(0, total - 1.5):.2f}:d=1.5[m0]")
        if pr.plan["music"].get("duck", True):
            filt.append("[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=25:release=400[m]")
        else:
            filt.append("[m0]anull[m]")
            filt.append("[sc]anullsink")
        mixin += "[m]"
        n = 3
    else:
        filt.append("[sc]anullsink")
    # plan.bed: the original ad's music stem laid under every stretch of generated picture, each piece anchored so it ENDS
    # at the original-time where the next footage segment picks the music up (footage carries its own music, so no bed there):
    #   {"stem": "music_bed.wav", "db": -3.7, "fade": 0.25,
    #    "stretches": [{"first": "b02", "last": "b03", "end_at_original": 7.55}, ...]}
    bed = pr.plan.get("bed")
    if bed:
        segs = pr.state.get("segments", [])
        stem = bed["stem"] if os.path.isabs(bed["stem"]) else pr.p(bed["stem"])
        stem_len = dur_of(stem)
        for k, stv in enumerate(bed.get("stretches", [])):
            s0 = next((x for x in segs if x["src"] == stv["first"]), None)
            s1 = next((x for x in reversed(segs) if x["src"] == stv["last"]), None)
            if not s0 or not s1:
                print(f"  bed: stretch {stv} not in the cut, skipped", flush=True)
                continue
            d = s1["t1"] - s0["t0"]
            if stv.get("stem_from") is not None:          # an explicit slice (filler from a stronger part of the same track)
                frm = float(stv["stem_from"]); to = min(stem_len, frm + d)
            else:
                to = min(stem_len, float(stv["end_at_original"]))
                frm = max(0.0, to - d)
            fd = float(bed.get("fade", 0.25))
            spath = stv["file"] if stv.get("file") and os.path.isabs(stv["file"]) else (pr.p(stv["file"]) if stv.get("file") else stem)
            if spath != stem:
                to = min(dur_of(spath), frm + d)
            ins += ["-ss", f"{frm:.3f}", "-to", f"{to:.3f}", "-i", spath]
            filt.append(f"[{n}:a]aresample=48000,volume={float(bed.get('db', 0)):.1f}dB,afade=t=in:d={fd:.2f},afade=t=out:st={max(0.0, to - frm - fd):.3f}:d={fd:.2f},"
                        f"adelay={int(s0['t0'] * 1000)}|{int(s0['t0'] * 1000)},apad=whole_dur={total:.3f},atrim=0:{total:.3f}[bed{k}]")
            mixin += f"[bed{k}]"
            n += 1
            print(f"  bed: {stv['first']}..{stv['last']} ({d:.1f}s) <- stem {frm:.2f}-{to:.2f}", flush=True)
    # plan.sfx: one-shot sounds placed on the cut, e.g. the original's whooshes on photo transitions:
    #   [{"file": "sfx/whoosh_in.wav", "at": "s08a", "edge": "start", "db": -6, "lead": 0.2}]  (edge start|end; lead = seconds before the cut the file starts)
    for k, fx_ in enumerate(pr.plan.get("sfx") or []):
        seg = next((x for x in pr.state.get("segments", []) if x["src"] == fx_["at"]), None)
        if not seg:
            print(f"  sfx: no segment {fx_['at']!r} in the cut, skipped", flush=True)
            continue
        at = (seg["t0"] if fx_.get("edge", "start") == "start" else seg["t1"]) - float(fx_.get("lead", 0.0))
        fpath = fx_["file"] if os.path.isabs(fx_["file"]) else pr.p(fx_["file"])
        # optional "from"/"to": a slice of the file (a piece of a music stem laid under one stretch of the cut); "fade": seconds in and out
        if fx_.get("to") is not None:
            ins += ["-ss", f"{float(fx_.get('from', 0.0)):.3f}", "-to", f"{float(fx_['to']):.3f}", "-i", fpath]
        else:
            ins += ["-i", fpath]
        fd = float(fx_.get("fade", 0.0))
        fades = (f",afade=t=in:d={fd:.2f},afade=t=out:st={max(0.0, float(fx_['to']) - float(fx_.get('from', 0.0)) - fd):.3f}:d={fd:.2f}" if fd and fx_.get("to") is not None else "")
        filt.append(f"[{n}:a]aresample=48000,volume={float(fx_.get('db', 0)):.1f}dB{fades},adelay={int(max(0, at) * 1000)}|{int(max(0, at) * 1000)},apad=whole_dur={total:.3f},atrim=0:{total:.3f}[fx{k}]")
        mixin += f"[fx{k}]"
        n += 1
    filt.append(f"{mixin}amix=inputs={n}:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[o]")
    sh(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filt), "-map", "[o]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", out])
    return out


# ---------------------------------------------------------------- final check
def whole_track_audit(pr, wav):
    """Word-for-word audit of the finished voice track: whisper on the dry master against the whole script
    (missing, extra, mispronounced words), then the second ear on each beat's stretch (doubled words).
    Faults here mean a join clipped a word or a take slipped through; fix the take or the cut, then rebuild."""
    full = {"id": "all", "text": " ".join(b["text"] for b in pr.beats)}
    master = pr.p("voice/master.wav")
    src = master if os.path.exists(master) else wav
    sw = strict_word_audit(pr, full, src)
    out = {"faults": list(sw["faults"]), "heard": sw["heard"]}
    print(f"  words (dry track vs script): {'exact' if sw['ok'] else '; '.join(sw['faults'])}")
    if pr.plan["voice"].get("second_ear") and pr.state.get("beats"):
        import voice_judge
        for b in pr.beats:
            bt = pr.state["beats"].get(b["id"])
            if not bt:
                continue
            seg = pr.p(f"build/_ear_{b['id']}.wav")
            t0 = max(0.0, bt["start"] - 0.15)
            sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t0:.3f}", "-t", f"{bt['end'] - t0 + 0.3:.3f}", "-i", src, seg])
            se = second_ear(b, seg)
            if not se["ok"]:
                out["faults"] += [f"{b['id']}: {f}" for f in se["faults"]]
                print(f"  second ear {b['id']}: {'; '.join(se['faults'])}")
            for f in list(out["faults"]):
                m = re.match(r"'([^']+)' heard as '([^']+)'$", f)
                if m and any(m.group(1) in h.split() for h in se["heard"]) and m.group(1) in _strict_tokens(b["text"].split()):
                    out["faults"].remove(f)
                    out.setdefault("notes", []).append(f"{b['id']}: whisper wrote '{m.group(2)}' for '{m.group(1)}', the second ear hears '{m.group(1)}'")
                    print(f"  note {b['id']}: whisper wrote '{m.group(2)}' for '{m.group(1)}'; the second ear hears '{m.group(1)}' (not a fault)")
        if not any(":" in f for f in out["faults"]):
            print("  second ear: no doubled words on any line")
    return out


def step_check(pr):
    import sync_gate
    final = pr.p("final.mp4")
    rep = {"file": final, "duration": round(dur_of(final), 2), "talk": {}}
    master = pr.p("voice/master.wav")
    worst = "PASS"
    for s in pr.state["segments"]:
        if s["kind"] != "talk" or s["t1"] - s["t0"] < 2.2:
            continue
        cut = pr.p("build/_chk.mp4")
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{s['t0']:.3f}", "-t", f"{s['t1'] - s['t0']:.3f}", "-i", final, "-an", "-c:v", "libx264", "-crf", "16", cut])
        aud = pr.p("build/_chk.wav")
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{s['t0']:.3f}", "-t", f"{s['t1'] - s['t0']:.3f}", "-i", master, aud])
        r = sync_gate.gate(cut, aud)
        sn = r.get("syncnet") or {}
        key = f"{s['src']}@{s['t0']:.1f}"
        rep["talk"][key] = {"verdict": r["verdict"], "offset": sn.get("offset_frames"), "conf": sn.get("confidence")}
        print(f"  final sync {key}: {r['verdict']} offset={sn.get('offset_frames')} conf={sn.get('confidence')}")
        if (r["verdict"] == "FAIL" and not _animal_sync_ok(pr, r)) or (r["verdict"] == "NO_FACE" and not _animal_faces(pr)):
            worst = "FAIL"
    # transcript of the export vs the script
    wav = pr.p("build/_final.wav")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vn", "-ac", "1", "-ar", "48000", wav])
    heard = [norm(w["w"]) for w in whisper_words(wav)]
    script = [norm(w) for b in pr.beats for w in b["text"].split() if norm(w)]
    rep["transcript_match"] = round(difflib.SequenceMatcher(None, script, heard, autojunk=False).ratio(), 3)
    if pr.plan["voice"].get("strict_words"):
        rep["words"] = whole_track_audit(pr, wav)
        if rep["words"]["faults"]:
            worst = "WORDS"
    # loudness
    ln = sh(["ffmpeg", "-hide_banner", "-i", final, "-af", "ebur128=peak=true", "-f", "null", "-"], check=False).stderr
    m = re.findall(r"I:\s+([-\d.]+) LUFS", ln)
    rep["lufs"] = float(m[-1]) if m else None
    # filmstrip: the frame before and after every cut, plus one mid frame per segment
    from PIL import Image
    shots = []
    for s in pr.state["segments"]:
        mid = (s["t0"] + s["t1"]) / 2
        fp = pr.p(f"build/_f_{len(shots):03d}.jpg")
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{mid:.3f}", "-i", final, "-frames:v", "1", "-vf", "scale=270:-1", fp], check=False)
        if os.path.exists(fp):
            shots.append((fp, f"{s['t0']:.1f}s {s['src']}"))
    sheet(pr, [x[0] for x in shots], pr.p("qa/final_filmstrip.jpg"), labels=[x[1] for x in shots], cols=6, cell=270)
    # a listening judge on three stretches of the finished voice (report only: it ranks and rejects, it does not certify)
    try:
        import voice_judge
        tot = rep["duration"]
        spots = [max(0.0, tot * f - 5) for f in (0.15, 0.5, 0.85)] if tot > 24 else [0.0]
        js = [voice_judge.score(final, runs=1, start=t, seconds=10) for t in spots]
        vals = [j["score"] for j in js if j["score"] is not None]
        rep["voice_judge"] = {"scores": vals, "tells": [t for j in js for t in j["tells"]][:3], "age": [a for j in js for a in j["age"]]}
        print(f"  voice judge (1 to 10, 10 = sounds like a real recording): {vals}  {rep['voice_judge']['tells'][:1]}")
    except Exception as e:
        rep["voice_judge"] = {"error": str(e)[:200]}
        print("  voice judge: skipped (" + str(e)[:80] + ")")
    cost = 0.0
    for line in (open(pr.p("kie_log.jsonl")) if os.path.exists(pr.p("kie_log.jsonl")) else []):
        try:
            cost += float(json.loads(line).get("credits") or 0)
        except ValueError:
            pass
    rep["credits"] = round(cost, 1)
    rep["usd"] = round(cost * CREDIT_USD, 2)
    rep["verdict"] = worst
    jsave(pr.p("qa/final_report.json"), rep)
    print(f"check: {worst}. {rep['duration']}s, transcript match {rep['transcript_match']:.0%}, {rep['lufs']} LUFS, {rep['credits']} credits (${rep['usd']}).")
    print("       Look at qa/final_filmstrip.jpg (one frame per segment, in order).")


def step_status(pr):
    st = pr.state
    print("voice:", st.get("voice"))
    for b in pr.beats:
        t = st.get("beats", {}).get(b["id"], {})
        g = st.get("gate", {}).get(b["id"], {})
        c = st.get("clips", {}).get(b["id"], {})
        print(f"  {b['id']:8} {b.get('visual', 'talk'):5} {t.get('cut_in', '-')}-{t.get('cut_out', '-')}  clip={c.get('state', '-')} {c.get('engine', '')}  gate={g.get('verdict', '-')} off={g.get('offset', '-')} conf={g.get('conf', '-')}")
    print("credits now:", pr.kie.credits())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["validate", "study", "voice", "native", "takes", "frames", "clips", "gate", "assemble", "check", "all", "status", "source"])
    ap.add_argument("project")
    ap.add_argument("--only", help="comma list of beat, shot or frame ids")
    ap.add_argument("--engine", help="force an engine for this clips run")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-auto", action="store_true", help="gate: score only, do not reroll")
    a = ap.parse_args()
    pr = Project(a.project)
    only = set(a.only.split(",")) if a.only else None
    if a.step == "validate":
        validate(pr)
    elif a.step == "study":
        step_study(pr)
    elif a.step == "voice":
        validate(pr)
        if _is_native(pr):
            raise SystemExit("voice.mode is native: run frames, then native (the video model speaks the lines).")
        step_voice(pr, a.force)
    elif a.step == "native":
        step_native(pr, only, a.force)
    elif a.step == "source":
        cut_source_clips(pr, only, a.force)
    elif a.step == "takes":
        pick_best_takes(pr, only)
        build_native_master(pr)
    elif a.step == "frames":
        step_frames(pr, only, a.force)
    elif a.step == "clips":
        step_clips(pr, only, a.force, a.engine)
    elif a.step == "gate":
        step_gate(pr, only, not a.no_auto)
    elif a.step == "assemble":
        step_assemble(pr)
    elif a.step == "check":
        step_check(pr)
    elif a.step == "status":
        step_status(pr)
    elif a.step == "all":
        validate(pr)
        if _is_native(pr):
            step_frames(pr)
            step_native(pr)
            step_clips(pr)
        else:
            step_voice(pr)
            step_frames(pr)
            step_clips(pr)
            step_gate(pr)
        step_assemble(pr)
        step_check(pr)


if __name__ == "__main__":
    main()
