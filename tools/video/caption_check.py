"""Do the burned captions land on the words? Transcribe the finished file's audio fresh with whisper and compare every
script word's caption time (state.json words, the timings the caption pass used) with the time whisper hears that word
in the export. Reports the words that are off by more than --tol seconds and the beats they cluster in.

Ryan 2026-11-04: "a bunch of errors with the captions." The captions show the script's words at whisper's timing from each
clip; after assembly, tightening or speed changes, a word can be drawn early or late. This measures it.

Usage: caption_check.py <project> [--in final_tight.mp4] [--tol 0.4] [--speed 1.0]
"""
import sys, os, json, argparse, subprocess, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oneshot

ap = argparse.ArgumentParser()
ap.add_argument("project")
ap.add_argument("--in", dest="src", default="final_tight.mp4")
ap.add_argument("--tol", type=float, default=0.4)
ap.add_argument("--speed", type=float, default=1.0, help="if the file was sped up after the captions were timed")
ap.add_argument("--fix", action="store_true", help="write the export's own word times back to state.json (matched words exact, the rest interpolated) so the caption pass lands on the sound")
a = ap.parse_args()
P = os.path.abspath(a.project)
src = os.path.join(P, a.src)
st = json.load(open(os.path.join(P, "state.json")))
words = st["words"]
wav = os.path.join(P, "qa", "caption_check.wav")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav], check=True, stdin=subprocess.DEVNULL)
heard = oneshot.whisper_words(wav)
A = [oneshot.norm(w["w"]) for w in words]
B = [oneshot.norm(w["w"]) for w in heard]
sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
off, matched = [], 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        continue
    for k in range(i2 - i1):
        sw, hw = words[i1 + k], heard[j1 + k]
        cap_t = sw["s"] / a.speed
        d = cap_t - hw["s"]
        matched += 1
        if abs(d) > a.tol:
            off.append((round(hw["s"], 2), sw["w"], round(d, 2)))
print(f"caption check: {matched} of {len(words)} script words matched in the export; {len(off)} drawn more than {a.tol}s off")
for t, w, d in off[:60]:
    print(f"  {t:7.2f}s  {w:18s} caption {'early' if d < 0 else 'late'} by {abs(d):.2f}s")
json.dump({"matched": matched, "total": len(words), "off": off}, open(os.path.join(P, "qa", "caption_check.json"), "w"), indent=1)
if a.fix:
    fixed = [dict(w) for w in words]
    known = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                known[i1 + k] = (heard[j1 + k]["s"] * a.speed, heard[j1 + k]["e"] * a.speed)
    idx = sorted(known)
    for i in range(len(fixed)):
        if i in known:
            fixed[i]["s"], fixed[i]["e"] = round(known[i][0], 3), round(known[i][1], 3)
    # interpolate the unmatched words between their nearest matched neighbours, in order
    i = 0
    while i < len(fixed):
        if i in known:
            i += 1; continue
        j = i
        while j < len(fixed) and j not in known:
            j += 1
        left = known[i - 1][1] if i - 1 in known else fixed[i]["s"]
        right = known[j][0] if j in known else fixed[j - 1]["e"]
        n = j - i; span = max(right - left, 0.12 * n)
        for k in range(n):
            fixed[i + k]["s"] = round(left + span * k / n, 3); fixed[i + k]["e"] = round(left + span * (k + 1) / n - 0.02, 3)
        i = j
    st["words_before_retime"] = words
    st["words"] = fixed
    json.dump(st, open(os.path.join(P, "state.json"), "w"), indent=1)
    print(f"caption fix: {len(known)} words timed from the export, {len(fixed) - len(known)} interpolated; state.json words updated")
