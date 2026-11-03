"""OUR caption system (approved direction 2026-10-22, from overlays/ours.py on the baby-doctor take):
clean, straight, readable, never on a character, inside the Meta safe box (safe_zone.py).

Usage: captions_ours.py <project> [--in final_nocap.mp4] [--out final.mp4] [--hook "LINE|LINE|LINE"] [--hook-end 4.6]

Placement: the caption page goes in the TOP band of the safe box (y 291..560) when no tracked face is there at the page's
start, middle and end; otherwise the BOTTOM band of the box (ending above 1248); if both are blocked the top band is used
and the clash is listed in qa/captions_report.json. Faces are tracked with the gate's MediaPipe landmarker, 3 faces, 2/s.
Type: Montserrat Black, white, one teal accent on the key words, a small teal SIGN n label when a sign starts.
No pills, no tilt, no stamps, no hard band: a soft dark gradient for contrast.
"""
import json, os, sys, subprocess, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import safe_zone as SZ
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
MONT = os.path.join(HERE, "fonts", "Montserrat-VF.ttf")
WHITE, TEAL, INK = (255, 255, 255), (0, 220, 190), (10, 12, 16)
KEY = {"rotting", "hiding", "breath", "germs", "yellow", "brown", "red", "pink", "bloodstream", "heart", "kidneys", "thirty",
       "gone", "cement", "toothbrush", "softens", "dead", "bleeding", "fourteen", "white", "vet", "cleaned", "five", "one",
       "article", "below", "kitchen", "tonight", "tomorrow", "harder", "click", "cleaning", "crust", "falling", "stain"}
TOP0, TOP1 = SZ.Y0 + 22, 560
BOT0, BOT1 = 1040, SZ.Y1 - 6


def mont(size, var="Black"):
    f = ImageFont.truetype(MONT, size)
    f.set_variation_by_name(var)
    return f


def track_faces(video, fps=2.0):
    import cv2, numpy as np, mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision
    model = os.path.join(HERE, "vendor", "models", "face_landmarker.task")
    opts = vision.FaceLandmarkerOptions(base_options=mp_python.BaseOptions(model_asset_path=model, delegate=mp_python.BaseOptions.Delegate.CPU),
                                        running_mode=vision.RunningMode.VIDEO, num_faces=3,
                                        min_face_detection_confidence=0.3, min_face_presence_confidence=0.3)
    cap = cv2.VideoCapture(video)
    vfps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, int(round(vfps / fps)))
    out = []
    with vision.FaceLandmarker.create_from_options(opts) as lm:
        for i in range(0, n, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ok, f = cap.read()
            if not ok:
                break
            h, w = f.shape[:2]
            sx, sy = W / w, H / h
            img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            r = lm.detect_for_video(img, int(i * 1000 / vfps))
            faces = []
            for lmks in (r.face_landmarks or []):
                pts = np.array([(p.x * w * sx, p.y * h * sy) for p in lmks])
                x0, y0 = pts.min(0); x1, y1 = pts.max(0)
                faces.append([int(x0), int(y0), int(x1), int(y1)])
            out.append({"t": round(i / vfps, 3), "faces": faces})
    cap.release()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--in", dest="src", default="final_nocap.mp4")
    ap.add_argument("--out", default="final.mp4")
    ap.add_argument("--hook", default="")
    ap.add_argument("--hook-end", type=float, default=0.0)
    ap.add_argument("--words", type=int, default=3)
    ap.add_argument("--hook-size", type=int, default=80)
    a = ap.parse_args()
    P = os.path.abspath(a.project)
    src = os.path.join(P, a.src)
    out = os.path.join(P, a.out)
    st = json.load(open(os.path.join(P, "state.json")))
    words = st["words"]
    os.makedirs(os.path.join(P, "qa"), exist_ok=True)
    os.makedirs(os.path.join(P, "build", "cap"), exist_ok=True)
    faces_path = os.path.join(P, "qa", "faces_final.json")
    if os.path.exists(faces_path) and os.path.getmtime(faces_path) > os.path.getmtime(src):
        FACES = json.load(open(faces_path))
    else:
        FACES = track_faces(src)
        json.dump(FACES, open(faces_path, "w"))

    def faces_at(t):
        return min(FACES, key=lambda o: abs(o["t"] - t))["faces"] if FACES else []

    def clash(box, t0, t1):
        x0, y0, x1, y1 = box
        hits = []
        for t in (t0, (t0 + t1) / 2, t1 - 0.05):
            for fx0, fy0, fx1, fy1 in faces_at(t):
                if x0 < fx1 and x1 > fx0 and y0 < fy1 and y1 > fy0:
                    hits.append([round(t, 2), fx0, fy0, fx1, fy1])
        return hits

    def gradient_top():
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        for y in range(0, TOP1 + 60):
            a_ = 150 if y < SZ.Y0 else int(150 * max(0.0, 1 - (y - SZ.Y0) / (TOP1 + 60 - SZ.Y0)))
            d.line([(0, y), (W, y)], fill=(0, 0, 0, a_))
        return g

    def gradient_bot():
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        for y in range(BOT0 - 80, H):
            a_ = int(150 * min(1.0, (y - (BOT0 - 80)) / 120))
            d.line([(0, y), (W, y)], fill=(0, 0, 0, a_))
        return g

    def soft_text(im, xy, t, f, fill):
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0] + 3, xy[1] + 5), t, font=f, fill=(0, 0, 0, 170))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
        ImageDraw.Draw(im).text(xy, t, font=f, fill=fill)

    def fit(d, toks, size, maxw=900, var="Black"):
        f = mont(size, var)
        while True:
            ws = [d.textlength(t, font=f) for t in toks]; sp = d.textlength(" ", font=f)
            if sum(ws) + sp * (len(toks) - 1) <= maxw or f.size <= 44:
                return f, ws, sp
            f = mont(f.size - 4, var)

    def clean(w): return w["w"].strip(".,?!;:\"")

    def pages(n):
        out_, cur = [], []
        for w in words:
            if a.hook_end and w["s"] < a.hook_end:
                continue
            cur.append(w)
            if len(cur) >= n or w["w"].rstrip().endswith((".", "?", "!")):
                out_.append(cur); cur = []
        if cur:
            out_.append(cur)
        res = []
        for i, pg in enumerate(out_):
            s = pg[0]["s"] - 0.04
            e = out_[i + 1][0]["s"] - 0.04 if i + 1 < len(out_) else pg[-1]["e"] + 0.4
            res.append((pg, max(0.0, s), e))
        return res

    ovs, report = [], {"clashes": [], "bottom_pages": 0, "pages": 0}
    if a.hook:
        im = gradient_top(); d = ImageDraw.Draw(im); y = SZ.Y0 + 4   # the hook card starts at the very top of the safe box
        lines = a.hook.split("|")
        for i, t in enumerate(lines):
            f, ws, sp = fit(d, [t], a.hook_size, maxw=930)
            soft_text(im, ((W - ws[0]) / 2, y), t, f, TEAL if i == 1 else WHITE); y += int(f.size * 1.05)
        hits = clash((SZ.X0, SZ.Y0 + 4, SZ.X1, y), 0.0, a.hook_end)
        if hits:
            # the face sits in the top band during the hook: draw the card in the bottom band of the box instead
            im = gradient_bot(); d = ImageDraw.Draw(im)
            fs = [fit(d, [t], a.hook_size, maxw=930)[0] for t in lines]
            block = sum(int(f.size * 1.05) for f in fs); y = BOT1 - block
            y0 = y
            for i, (t, f) in enumerate(zip(lines, fs)):
                tw = d.textlength(t, font=f)
                soft_text(im, ((W - tw) / 2, y), t, f, TEAL if i == 1 else WHITE); y += int(f.size * 1.05)
            hits_b = clash((SZ.X0, y0, SZ.X1, BOT1), 0.0, a.hook_end)
            if hits_b:
                report["clashes"].append({"what": "hook", "top": hits, "bottom": hits_b})
            else:
                report["hook_slot"] = "bottom"
        p = os.path.join(P, "build", "cap", "hook.png"); im.save(p); ovs.append((p, 0.0, a.hook_end))
    label = None
    for i, (pg, s, e) in enumerate(pages(a.words)):
        toks = [clean(w) for w in pg]
        if toks and toks[0].lower() == "sign" and len(toks) > 1:
            label = "SIGN " + {"one": "1", "two": "2", "three": "3"}.get(toks[1].lower(), "")
        if toks and toks[0].lower() in ("and", "here's", "add", "that", "once", "by", "the", "number", "so", "but"):
            if toks[0].lower() in ("and", "here's", "once", "by", "number", "so", "but", "that"):
                label = None
        d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        f, ws, sp = fit(d0, toks, 78)
        tw = sum(ws) + sp * (len(toks) - 1)
        lab_h = 78 if label else 0
        box_top = (SZ.X0, TOP0, SZ.X1, TOP0 + lab_h + f.size * 1.2)
        slot = "top"
        hits = clash(box_top, s, e)
        if hits:
            y_b = BOT1 - f.size * 1.2
            box_bot = (SZ.X0, y_b, SZ.X1, BOT1)
            hits_b = clash(box_bot, s, e)
            if not hits_b:
                slot = "bottom"
            else:
                report["clashes"].append({"page": " ".join(toks), "t": [round(s, 2), round(e, 2)], "top": hits, "bottom": hits_b})
        if slot == "top":
            im = gradient_top(); d = ImageDraw.Draw(im); y = TOP0
            if label:
                fl = mont(40, "ExtraBold"); lw = d.textlength(label, font=fl)
                d.rounded_rectangle([SZ.X0 + 10, y, SZ.X0 + 10 + lw + 36, y + 58], radius=12, fill=TEAL)
                d.text((SZ.X0 + 28, y + 8), label, font=fl, fill=INK); y += 78
        else:
            im = gradient_bot(); d = ImageDraw.Draw(im); y = BOT1 - f.size * 1.2; report["bottom_pages"] += 1
        x = (W - tw) / 2
        for t, wd, w in zip(toks, ws, pg):
            soft_text(im, (x, y), t, f, TEAL if clean(w).lower() in KEY else WHITE); x += wd + sp
        p = os.path.join(P, "build", "cap", f"p{i:03d}.png"); im.save(p); ovs.append((p, s, e)); report["pages"] += 1
    inputs, chain, cur, idx = ["-i", src], [], "[0:v]", 1
    for k, (p, s, e) in enumerate(ovs):
        inputs += ["-i", p]
        chain.append(f"{cur}[{k + 1}:v]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'[v{idx}]"); cur = f"[v{idx}]"; idx += 1
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(chain), "-map", cur, "-map", "0:a",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
                   check=True, stdin=subprocess.DEVNULL)
    json.dump(report, open(os.path.join(P, "qa", "captions_report.json"), "w"), indent=1)
    print(f"captions: {report['pages']} pages, {report['bottom_pages']} in the bottom slot, {len(report['clashes'])} clashes -> {out}")


if __name__ == "__main__":
    main()
