#!/usr/bin/env python3
"""Ask the listener (Gemini 3.1 Pro on Kie) a free question about a stretch of audio. The builder cannot hear;
this is the ear for anything the gates do not measure (music, ambience, intelligibility, a glitch).

  tools/video/.venv/bin/python tools/video/listen.py FILE "question" [--start S] [--seconds N]
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice_judge
from kie import Kie

def listen(path, question, start=None, seconds=30, runs=1):
    k = voice_judge._k or Kie(); voice_judge._k = k
    wav = voice_judge._clip(path, start, seconds)
    try:
        url = k.upload(wav)
    finally:
        os.unlink(wav)
    body = {"model": voice_judge.MODEL, "stream": False, "messages": [{"role": "user", "content": [
        {"type": "text", "text": "Listen carefully to this audio clip. " + question + " Answer in plain prose, under 120 words, with timestamps in seconds from the start of the clip where relevant."},
        {"type": "image_url", "image_url": {"url": url}}]}]}
    for attempt in range(3):
        try:
            d = k._req(f"https://api.kie.ai/{voice_judge.MODEL}/v1/chat/completions", body, timeout=180)
            return d["choices"][0]["message"]["content"].strip()
        except Exception as e:
            err = str(e)[:160]; time.sleep(4)
    return "ERROR " + err

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    start = float(sys.argv[sys.argv.index("--start") + 1]) if "--start" in sys.argv else None
    secs = int(sys.argv[sys.argv.index("--seconds") + 1]) if "--seconds" in sys.argv else 30
    print(listen(a[0], a[1], start, secs))
