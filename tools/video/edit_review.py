#!/usr/bin/env python3
"""Editor's review of a finished cut: things a viewer notices that the clip gates do not measure.

  tools/video/.venv/bin/python tools/video/edit_review.py <project> [--ref original.mp4]

1. Floor continuity: the floor under the speech per segment (quietest 10% of 50 ms windows). A dry generated line next
   to footage with room in it reads as a bed dropping out at the cut (TPS kid v2, 2026-10-16).
2. Motion spikes: per clip in the cut, mean absolute frame difference per second; a generated shot that jumps or
   bounces shows as a spike against the clip's own median.
3. Shot map: the cut's segments next to the plan's beats, so the timeline can be read against the original's.
Prints a report; exit code 1 when something needs a look.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from scipy import signal
from scipy.io import wavfile

def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout

def floor_per_segment(path, segs, sr=16000):
    """The floor under the speech in each segment: the quietest 10% of 50 ms windows, broadband. A segment whose floor
    sits far under the others is a generated line with no room in it next to footage that has one (the thing a viewer
    hears as a bed or ambience dropping out at the cut). Voice level does not move this number much; a band measure did."""
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-c:a", "pcm_s16le", tmp])
    _, a = wavfile.read(tmp); os.unlink(tmp)
    a = a.astype(np.float64) / 32768.0
    hop = int(sr * 0.05)
    out = {}
    for s_ in segs:
        x = a[int((s_["t0"] + 0.15) * sr):int((s_["t1"] - 0.15) * sr)]
        n = len(x) // hop
        if n < 6:
            continue
        r = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) for i in range(n)])
        out[s_["src"]] = float(np.percentile(20 * np.log10(r + 1e-9), 10))
    return out

def motion_per_second(path):
    out = sh(["ffmpeg", "-hide_banner", "-i", path, "-vf", "scale=96:-1,format=gray,tblend=all_mode=difference,fps=4,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"])
    vals = [float(l.split("=")[-1]) for l in subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vf", "scale=96:-1,format=gray,tblend=all_mode=difference,fps=4,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"], capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr.splitlines() if "YAVG" in l]
    return np.array(vals)

def main():
    pr = sys.argv[1]
    plan = json.load(open(os.path.join(pr, "plan.json"))); st = json.load(open(os.path.join(pr, "state.json")))
    final = os.path.join(pr, "final.mp4")
    flags = []
    # 1. floor continuity across the cut
    fl = floor_per_segment(final, st.get("segments", []))
    med = np.median(list(fl.values())) if fl else 0.0
    low = {k: v for k, v in fl.items() if v < med - 6}
    print(f"floor under speech: median {med:.1f} dB; " + (f"{len(low)} segment(s) more than 6 dB under it: " + ", ".join(f"{k} {v:.1f}" for k, v in low.items()) if low else "every segment within 6 dB"))
    for k, v in low.items():
        flags.append(f"{k}: floor {v:.1f} dB vs median {med:.1f} (a dry generated line next to footage with room in it)")
    # 2. motion spikes per generated clip in the cut
    for s in st.get("segments", []):
        if s["kind"] == "broll" and os.path.exists(os.path.join(pr, "clips", s["src"] + ".mp4")) and st.get("clips", {}).get(s["src"], {}).get("engine") != "source":
            m = motion_per_second(os.path.join(pr, "clips", s["src"] + ".mp4"))
            if len(m) > 2 and m.max() > max(3.0, 2.5 * np.median(m)):
                flags.append(f"{s['src']}: motion spike {m.max():.1f} vs median {np.median(m):.1f} (a jump, a bounce or a whip)")
    # 3. shot map
    print("\nshot map (export time, segment, beat text):")
    for s in st.get("segments", []):
        b = next(x for x in plan["beats"] if x["id"] == s["beat"])
        kind = "FOOTAGE" if st.get("clips", {}).get(s["src"], {}).get("engine") == "source" else ("still" if s["kind"] == "broll" and any(sh_.get("still") for bb in plan["beats"] for sh_ in bb.get("shots", []) + bb.get("cutaways", []) if sh_["id"] == s["src"]) else s["kind"])
        print(f"  {s['t0']:6.1f}-{s['t1']:6.1f} {kind:7} {s['src']:5} {b.get('speaker', ''):8} {b['text'][:60]}")
    print("\n" + ("NEEDS A LOOK:\n  " + "\n  ".join(flags) if flags else "editor review: nothing flagged"))
    sys.exit(1 if flags else 0)

if __name__ == "__main__":
    main()
