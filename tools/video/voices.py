#!/usr/bin/env python3
"""Voice sampler: one short line in every Gemini TTS voice, on one page you can listen to.

  tools/video/.venv/bin/python tools/video/voices.py            # all 70 voices, about 25 credits
  tools/video/.venv/bin/python tools/video/voices.py Gacrux Sulafat Charon
  tools/video/.venv/bin/python tools/video/voices.py --style "A tired 70 year old man, slow, gravelly"

Writes tools/video/voices/<voice>.mp3 and tools/video/voices/index.html.
Pitch is measured so the page can sort lower voices from higher ones (the docs do not
say which voices read as men or women).
"""
import json
import os
import subprocess
import sys
import threading
import time

import numpy as np
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kie import Kie  # noqa: E402

OUT = os.path.join(HERE, "voices")
GROUPS = {
    "Tutor": "Bodi Lumi Sadaltager Sola Sulafat Varo Zephyr",
    "Commercial voiceover": "Koda Kore Nika Tavi Zeno",
    "Instructional": "Algenib Despina Erinome Kira Ludo Mako Rasalgethi Rina",
    "Podcast": "Alnilam Brio Jori Laomedeia Rami Veda",
    "Storyteller": "Achird Enzo Riko Sami Zali Zubenelgenubi",
    "Digital assistant": "Algieba Aoede Autonoe Callirrhoe Enceladus Gero Iapetus Neno Olin Tari Umbriel",
    "Call center": "Achernar Charon Daro Fola Hali Milo Puck",
    "Concierge": "Arlo Cleo Fenrir Finn Leda Lora Orus",
    "Tech support": "Enya Jett Knox Nyla Sadachbia Vindemiatrix",
    "Professional": "Cruz Elio Gacrux Pulcherrima Schedar Tova Zuri",
}
LINE = ("My friend Joan has been a nurse for thirty years. She looked at my lunch and said, "
        "you need to stop with the salads. And I thought, what is she talking about?")
STYLE = ("Someone in their sixties telling a friend a true story. Warm and conversational. "
         "Speaks slowly and calmly and leaves a beat of silence between sentences. Not an announcer.")


def pitch_hz(path):
    tmp = path + ".tmp.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", path, "-ar", "16000", "-ac", "1", tmp], check=True)
    sr, a = wavfile.read(tmp)
    os.remove(tmp)
    a = a.astype(np.float64)
    hop, win, vals = 400, 800, []
    for i in range(0, len(a) - win, hop):
        f = a[i:i + win]
        if np.sqrt((f ** 2).mean()) < 400:
            continue
        f = f - f.mean()
        ac = np.correlate(f, f, "full")[win - 1:]
        lo, hi = sr // 350, sr // 70
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.35 * ac[0]:
            vals.append(sr / k)
    return float(np.median(vals)) if vals else 0.0, len(a) / sr


def main():
    args = sys.argv[1:]
    style = STYLE
    if "--style" in args:
        i = args.index("--style")
        style = args[i + 1]
        args = args[:i] + args[i + 2:]
    group_of = {v: g for g, vs in GROUPS.items() for v in vs.split()}
    voices = args or sorted(group_of)
    os.makedirs(OUT, exist_ok=True)
    k = Kie(log=os.path.join(OUT, "kie_log.jsonl"))
    rows, lock, sem = {}, threading.Lock(), threading.Semaphore(6)

    def go(v):
        with sem:
            wav = os.path.join(OUT, f"{v}.wav")
            mp3 = os.path.join(OUT, f"{v}.mp3")
            try:
                if not os.path.exists(mp3):
                    out = k.run("google/gemini-3-8-flash-tts", {
                        "temperature": 1, "speakers": [{"speaker_id": "Speaker 1", "voice_name": v}],
                        "dialogue_turns": [{"speaker_id": "Speaker 1", "style": style, "text": LINE}]}, dest=wav, tag=f"voice-sample:{v}", timeout=300)
                    if out["state"] != "success":
                        print(v, "failed", out.get("msg"), flush=True)
                        return
                    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", wav, "-b:a", "128k", mp3], check=True)
                    os.remove(wav)
                hz, dur = pitch_hz(mp3)
                with lock:
                    rows[v] = {"voice": v, "group": group_of.get(v, ""), "hz": round(hz), "wpm": round(len(LINE.split()) / dur * 60)}
                print(v, rows[v], flush=True)
            except Exception as e:
                print(v, "ERROR", str(e)[:160], flush=True)

    ts = [threading.Thread(target=go, args=(v,)) for v in voices]
    for t in ts:
        t.start()
        time.sleep(0.5)
    for t in ts:
        t.join()
    old = {}
    meta = os.path.join(OUT, "voices.json")
    if os.path.exists(meta):
        old = {r["voice"]: r for r in json.load(open(meta))}
    old.update(rows)
    data = sorted(old.values(), key=lambda r: r["hz"])
    json.dump(data, open(meta, "w"), indent=1)
    trs = "\n".join(
        f"<tr><td><b>{r['voice']}</b></td><td>{'lower' if r['hz'] < 150 else 'higher'} ({r['hz']} Hz)</td><td>{r['wpm']}</td>"
        f"<td>{r['group']}</td><td><audio controls preload='none' src='{r['voice']}.mp3'></audio></td></tr>" for r in data)
    html = f"""<!doctype html><meta charset="utf-8"><title>Voice board</title>
<style>body{{font:16px -apple-system,sans-serif;margin:32px;max-width:980px}}td,th{{padding:6px 14px;border-bottom:1px solid #ddd;text-align:left}}audio{{height:32px}}</style>
<h1>Voice board (Gemini 3.8 Flash TTS on Kie)</h1>
<p>Same line, same direction, every voice. Sorted low pitch to high. Put the name you like in plan.json under voice.speakers.&lt;name&gt;.voice_name.</p>
<p><i>Line:</i> {LINE}<br><i>Direction:</i> {style}</p>
<table><tr><th>Voice</th><th>Pitch</th><th>Words/min</th><th>Kie group</th><th>Listen</th></tr>
{trs}</table>"""
    open(os.path.join(OUT, "index.html"), "w").write(html)
    print(f"{len(data)} voices on {os.path.join(OUT, 'index.html')}")


if __name__ == "__main__":
    main()
