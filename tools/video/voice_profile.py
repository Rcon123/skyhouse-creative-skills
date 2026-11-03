#!/usr/bin/env python3
"""Acoustic profile of a voice track, so a generated voice can be compared with real footage.

I cannot listen, so this measures the things that make a clean text-to-speech read stand out
from a person filmed on a phone: how quiet the gaps are, how much room is on the voice, how
wide the band is, how much the pitch and pace move.

  tools/video/.venv/bin/python tools/video/voice_profile.py FILE [FILE ...] [--json out.json]

Numbers are for comparing files to each other, not absolute truth. Music under a voice
inflates the noise floor and the reverb estimate.
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 32000


def load(path):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR),
                    "-c:a", "pcm_s16le", tmp], check=True, stdin=subprocess.DEVNULL)
    sr, a = wavfile.read(tmp)
    os.unlink(tmp)
    return a.astype(np.float64) / 32768.0


def frames_db(a, win=0.02):
    n = int(SR * win)
    m = len(a) // n
    f = a[:m * n].reshape(m, n)
    return 20 * np.log10(np.sqrt((f ** 2).mean(1)) + 1e-9)


def f0_track(a):
    hop, win = int(SR * 0.01), int(SR * 0.04)
    lo, hi = SR // 400, SR // 60
    out = []
    for i in range(0, len(a) - win, hop):
        f = a[i:i + win]
        if np.sqrt((f ** 2).mean()) < 0.01:
            out.append(np.nan)
            continue
        f = f - f.mean()
        ac = signal.correlate(f, f, mode="full", method="fft")[win - 1:]
        k = lo + int(np.argmax(ac[lo:hi]))
        out.append(SR / k if ac[k] > 0.45 * ac[0] else np.nan)
    return np.array(out)


def profile(path):
    a = load(path)
    db = frames_db(a)
    speech_level = np.percentile(db, 90)
    floor = np.percentile(db, 5)
    speech = db > speech_level - 30
    # pauses: runs of non-speech between speech
    runs, start = [], None
    for i, s in enumerate(list(~speech) + [False]):
        if s and start is None:
            start = i
        elif not s and start is not None:
            runs.append((i - start) * 0.02)
            start = None
    pauses = [r for r in runs[1:-1] if r >= 0.12] if len(runs) > 2 else []
    # decay after speech stops: how many dB the level falls in the first 100 ms of each pause (room = slow fall)
    drops = []
    for i in range(1, len(db) - 6):
        if speech[i - 1] and not speech[i] and not speech[i:i + 6].any():
            drops.append(db[i - 1] - db[i + 4])
    # spectrum
    f, pxx = signal.welch(a, SR, nperseg=4096)
    tot = pxx.sum()
    cum = np.cumsum(pxx) / tot
    rolloff = float(f[np.searchsorted(cum, 0.95)])
    hf = float(10 * np.log10(pxx[f > 7000].sum() / tot + 1e-12))
    lf = float(10 * np.log10(pxx[f < 120].sum() / tot + 1e-12))
    f0 = f0_track(a)
    v = f0[~np.isnan(f0)]
    semis = 12 * np.log2(v / np.median(v)) if len(v) > 20 else np.array([0.0])
    return {
        "file": os.path.basename(path),
        "seconds": round(len(a) / SR, 1),
        "noise_floor_below_speech_db": round(float(speech_level - floor), 1),   # big = dead silent gaps (studio or TTS)
        "decay_db_in_100ms": round(float(np.median(drops)), 1) if drops else None,  # big = dry, small = room on the voice
        "rolloff95_hz": round(rolloff),
        "energy_above_7k_db": round(hf, 1),
        "energy_below_120_db": round(lf, 1),
        "f0_median_hz": round(float(np.median(v)), 0) if len(v) else None,
        "f0_spread_semitones": round(float(np.percentile(semis, 90) - np.percentile(semis, 10)), 1),
        "pause_share": round(float((~speech).mean()), 2),
        "pause_median_s": round(float(np.median(pauses)), 2) if pauses else None,
        "pause_sd_s": round(float(np.std(pauses)), 2) if pauses else None,
        "crest_db": round(float(20 * np.log10(np.abs(a).max() / (np.sqrt((a ** 2).mean()) + 1e-9))), 1),
    }


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    rows = [profile(p) for p in args]
    keys = [k for k in rows[0] if k != "file"]
    print("file".ljust(34) + " ".join(k[:13].rjust(14) for k in keys))
    for r in rows:
        print(r["file"][:33].ljust(34) + " ".join(str(r[k]).rjust(14) for k in keys))
    if "--json" in sys.argv:
        json.dump(rows, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
