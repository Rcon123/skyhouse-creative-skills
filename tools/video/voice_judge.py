#!/usr/bin/env python3
"""A listening judge, because the builder of these videos cannot hear.

Sends an audio (or video) clip to Gemini 3.1 Pro on Kie and asks one question: real person
recorded on a phone, or AI text-to-speech? One clip per call, so it never compares labels.
About 0.1 credit a call.

Calibration, 2026-10-05 (two runs each unless noted):
  a real Loom recording                      10
  Ryan's winners VID251 and VID212           10, 10
  Kling 3.0 native voice, untouched          10, 10
  Seedance 2 mini native voice, untouched     2, 2   ("sterile, no room tone")
  the same clip after voice_fx native-kitchen 10, 9
  Wan 3.0 native voice, with or without room  2, 2, 2, 1
  Gemini TTS (the voice Ryan called fake)     2      with room: 3, 2
  Veo 3.1 Lite native voice                   2, 9   (unstable)
  a real studio-clean doctor interview        2      (a miss: it punishes clean audio)

Ryan's ear on the same clips: seated Seedance 2 mini = real, Kling 3.0 native = NOT real. So the
judge passed a voice he rejects.

So: it agreed with Ryan on the TTS voice he rejected, it is not fooled by room sound alone, and it
is wrong in both directions. Use it to rank and to reject, score at least twice, and never report a
voice as good on its word alone. Ryan's ear is the final gate.

  tools/video/.venv/bin/python tools/video/voice_judge.py FILE [FILE ...] [--runs 2]
"""
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kie import Kie  # noqa: E402

MODEL = "gemini-3.1-pro"
PROMPT = ("Listen to this short audio clip of a person speaking. You are a forensic audio reviewer for an ad agency. "
          "Decide whether it sounds like a real person recorded on a phone, or like AI text-to-speech. "
          "Judge only by ear: prosody, breath, pacing, room sound, vocal texture, artifacts. "
          "Answer in JSON only: {\"heard\": \"<first 8 words you heard>\", \"real_score\": <1 to 10, 10 = certainly a real recording>, "
          "\"age_guess\": <number>, \"sex_guess\": \"<woman or man>\", \"tells\": \"<under 25 words on what gave it away either way>\"}")
_k = None


def _clip(path, start=None, seconds=10):
    """Mono wav, at most `seconds` long, so each call is cheap and uploads never hit the size limit."""
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.2f}"]
    cmd += ["-t", str(seconds), "-i", path, "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", tmp]
    subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)
    return tmp


def ask(path, start=None, seconds=10):
    global _k
    _k = _k or Kie()
    wav = _clip(path, start, seconds)
    try:
        url = _k.upload(wav)
    finally:
        os.unlink(wav)
    body = {"model": MODEL, "stream": False, "messages": [{"role": "user", "content": [
        {"type": "text", "text": PROMPT}, {"type": "image_url", "image_url": {"url": url}}]}]}
    for attempt in range(3):
        try:
            d = _k._req(f"https://api.kie.ai/{MODEL}/v1/chat/completions", body, timeout=180)
            txt = d["choices"][0]["message"]["content"]
            m = re.search(r"\{.*\}", txt, re.S)
            return json.loads(m.group(0))
        except Exception as e:  # the Gemini proxy times out now and then
            err = str(e)[:160]
            time.sleep(4)
    return {"error": err}


def score(path, runs=2, start=None, seconds=10):
    """Median real_score over a few runs, plus the raw answers. None if the judge could not be reached."""
    out = [ask(path, start, seconds) for _ in range(runs)]
    vals = [r["real_score"] for r in out if isinstance(r.get("real_score"), (int, float))]
    return {"score": statistics.median(vals) if vals else None, "scores": vals,
            "tells": [r.get("tells") for r in out if r.get("tells")], "age": [r.get("age_guess") for r in out if r.get("age_guess")],
            "sex": [r.get("sex_guess") for r in out if r.get("sex_guess")]}


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    runs = int(sys.argv[sys.argv.index("--runs") + 1]) if "--runs" in sys.argv else 2
    a = [x for x in a if not x.isdigit()]
    for f in a:
        r = score(f, runs)
        print(f"{os.path.basename(f)[:40]:42} {r['scores']}  age {r['age']} {r['sex']}  {(r['tells'] or [''])[0]}")


VERBATIM = ("Transcribe this audio clip exactly as spoken, verbatim. Include every repeated word, stutter, false start, "
            "and filler. Mark anything that is not a word (breath, hum, noise, music, mouth sound) in square brackets with its "
            "rough second. Do not correct grammar and do not guess words that are not clearly there. Answer in JSON only: "
            "{\"verbatim\": \"<the transcript>\", \"repeats\": \"<any word said twice in a row, or none>\", "
            "\"nonspeech\": \"<what you heard that is not a word, with seconds, or none>\"}")


def transcribe(path, start=None, seconds=10):
    """A second, independent ear: Gemini listens and writes down exactly what it hears (repeats included)."""
    global _k
    _k = _k or Kie()
    wav = _clip(path, start, seconds)
    try:
        url = _k.upload(wav)
    finally:
        os.unlink(wav)
    body = {"model": MODEL, "stream": False, "messages": [{"role": "user", "content": [
        {"type": "text", "text": VERBATIM}, {"type": "image_url", "image_url": {"url": url}}]}]}
    err = ""
    for attempt in range(3):
        try:
            d = _k._req(f"https://api.kie.ai/{MODEL}/v1/chat/completions", body, timeout=180)
            txt = d["choices"][0]["message"]["content"]
            m = re.search(r"\{.*\}", txt, re.S)
            return json.loads(m.group(0))
        except Exception as e:
            err = str(e)[:160]
            time.sleep(4)
    return {"error": err}
