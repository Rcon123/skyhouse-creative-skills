"""Cut dead air out of an assembled cut without re-rendering anything.

Ryan 2026-11-04 on the first full video: "weird pauses from her that are super unnatural." Measured: 32 pauses over
0.45 s, 27.6 s of silence in 183 s (15%; the client's winners sit at 4 to 7%). Native takes pad the head and tail of
every line and breathe inside it; the assembler keeps all of it.

This pass works on the ASSEMBLED, UNCAPTIONED final.mp4 (voice, bed and picture already mixed) plus state.json's word
timings: every stretch of silence in the voice track longer than --max (default 0.45 s) is cut down to --keep (0.22 s),
picture and audio together. Under a cutaway the cut is invisible; on her face it is a jump cut, the native grammar of
a yapper. Word timings are shifted the same way and written back to state.json (the originals are kept under
"words_untightened") so the caption pass lands on the words. Re-run `assemble` to get the untightened cut back.

Usage: tighten.py <project> [--in final.mp4] [--out final_tight.mp4] [--max 0.45] [--keep 0.22] [--floor -45]
"""
import sys, os, json, argparse, subprocess, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("project")
ap.add_argument("--in", dest="src", default="final.mp4")
ap.add_argument("--out", default="final_tight.mp4")
ap.add_argument("--max", type=float, default=0.45)
ap.add_argument("--keep", type=float, default=0.22)
ap.add_argument("--floor", type=float, default=-45.0)
a = ap.parse_args()
P = os.path.abspath(a.project)
src, out = os.path.join(P, a.src), os.path.join(P, a.out)
st = json.load(open(os.path.join(P, "state.json")))
words = st.get("words_untightened") or st["words"]
voice = os.path.join(P, "voice", "master.wav")

# 1. silences in the voice track (the mixed file has the bed under it; the voice track is what the viewer waits on)
tmp = "/tmp/_tighten_voice.wav"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", voice, "-ac", "1", "-ar", "16000", tmp], check=True, stdin=subprocess.DEVNULL)
w = wave.open(tmp); sig = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768; sr = 16000
hop = int(0.02 * sr)
rms = np.array([20 * np.log10(np.sqrt(np.mean(sig[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(sig) - hop, hop)])
total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                             capture_output=True, text=True).stdout.strip())
sil = rms < a.floor
cuts = []  # (start, end) of silence to REMOVE, keeping `keep` seconds split around the middle
i = 0
while i < len(sil):
    if sil[i]:
        j = i
        while j < len(sil) and sil[j]:
            j += 1
        s0, s1 = i * 0.02, j * 0.02
        d = s1 - s0
        if d > a.max and s0 > 0.3 and s1 < total - 0.3:
            # keep `keep` s: a little before the cut and a little after, so neither word is clipped
            pad = a.keep / 2
            cuts.append((round(s0 + pad, 3), round(s1 - pad, 3)))
        i = j
    else:
        i += 1
removed = sum(e - s for s, e in cuts)
print(f"tighten: {len(cuts)} pauses over {a.max}s, removing {removed:.1f}s of {total:.1f}s")

# 2. keep intervals
keeps, t = [], 0.0
for s, e in cuts:
    if s > t:
        keeps.append((t, s))
    t = e
if t < total:
    keeps.append((t, total))

# 3. cut picture and sound together with select/aselect (frame-accurate on the decoded stream)
vexpr = "+".join(f"between(t,{s:.3f},{e:.3f})" for s, e in keeps)
filt = f"[0:v]select='{vexpr}',setpts=N/FRAME_RATE/TB[v];[0:a]aselect='{vexpr}',asetpts=N/SR/TB[a]"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-filter_complex", filt, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", out], check=True, stdin=subprocess.DEVNULL)

# 4. shift word timings: new_t = t - (removed time before t); a word inside a removed span snaps to the cut point
def shift(x):
    rem = 0.0
    for s, e in cuts:
        if e <= x:
            rem += e - s
        elif s < x < e:
            rem += x - s
    return round(x - rem, 3)
new_words = [{**wd, "s": shift(wd["s"]), "e": max(shift(wd["s"]) + 0.05, shift(wd["e"]))} for wd in words]
st["words_untightened"] = words
st["words"] = new_words
st["tighten"] = {"src": a.src, "out": a.out, "cuts": cuts, "removed": round(removed, 2), "max": a.max, "keep": a.keep}
json.dump(st, open(os.path.join(P, "state.json"), "w"), indent=1)
newdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                              capture_output=True, text=True).stdout.strip())
print(f"tighten: wrote {out} ({newdur:.1f}s); words shifted in state.json (originals under words_untightened)")
