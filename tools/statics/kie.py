#!/usr/bin/env python3
"""Shared Kie helpers for static ad rounds (2026-10-28).
fire(model, input) -> taskId; wait(taskId) -> url|FAIL; render(frames, outdir) threads them.
Models: gpt-image-2-text-to-image (default statics + baked lettering), gpt-image-2-image-to-image (edits, pairs AFTER),
z-image (real-looking people for pairs BEFORE; prompt < 800 chars; never end a z-image prompt on a bare format word).
Never nano-banana-pro. Realism stack (REA r8 / Cloud9 rule 7) lives in DEG. House pair recipe = pairs.py HEAD/TAIL (copied verbatim).
"""
import os, json, time, base64, subprocess, threading, urllib.request
WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
env = dict(l.strip().split("=", 1) for l in open(f"{WS}/.env") if "=" in l and not l.startswith("#"))
KEY = env["KIE_API_KEY"]
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

DEG = ("Photo taken on a 2014 iPhone from a few feet away, on-camera flash, harsh flash shadow, overexposed highlights, slightly soft focus, "
       "visible JPEG blockiness and colour noise in the shadows, warm yellow indoor colour cast, crooked framing, real household clutter, "
       "no retouching, unposed, not stock, not a portrait. ")
LET = " CRITICAL: the text is lettered clearly and legibly, every word spelled exactly as given, no other text anywhere in the image."
SQ = " Square 1:1, one subject, one focal point, nothing else to look at."
# house pair recipe, verbatim from offers/tps/images/lander-plain-ba/pairs.py
FLASH = ("Amateur snapshot on an old iPhone with the flash on, taken by a family member three feet away, grainy, "
         "real uneven skin, no makeup, unposed, not stock, not a photoshoot. Head and shoulders centered with a "
         "little space above her head, front-on, eyes into the lens, no phone in the picture, hands out of frame. ")
HEAD = ("Use the woman in this photo as the identity reference and make a completely DIFFERENT candid iPhone photograph "
        "of the SAME woman taken about six weeks later: ")
TAIL = (" Same face, same bone structure, same nose, same eye colour, same hair colour, clearly the same woman her age, "
        "but a new photo on a new day: new place, new clothes, new hairstyle, daylight, different framing and angle, do not reuse the room, outfit or pose. "
        "Her skin looks better: the deep lines, sagging and under-eye bags are gone, jawline lifted and defined, neck "
        "smooth, skin firm, so she looks a full twenty years younger, styled, hair done, a little lipstick, smiling, but still a real woman with real pores, a few "
        "faint smile lines and age spots. Real hand-held phone-photo grain, slightly imperfect framing, no retouched or "
        "airbrushed look, NOT brightened, no glow, same old phone, no studio light, no text, no graphics, one single photo.")


def fire(model, inp):
    r = urllib.request.Request("https://api.kie.ai/api/v1/jobs/createTask", data=json.dumps({"model": model, "input": inp}).encode(), headers=H)
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(r, timeout=60))["data"]["taskId"]
        except Exception as e:
            body = getattr(e, "read", lambda: b"")()
            print("POST FAIL", str(e)[:120], body[:200], flush=True); time.sleep(5)
    return None


def wait(tid, limit=720):
    if tid is None: return "FAIL:no task"
    t0 = time.time()
    while time.time() - t0 < limit:
        time.sleep(8)
        try:
            r = urllib.request.Request(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}", headers={"Authorization": f"Bearer {KEY}"})
            d = json.load(urllib.request.urlopen(r, timeout=60))["data"]
        except Exception:
            continue
        if d.get("state") == "success": return json.loads(d["resultJson"])["resultUrls"][0]
        if d.get("state") == "fail": return "FAIL:" + str(d.get("failMsg"))
    return "TIMEOUT"


def grab(url, path):
    if url.startswith("FAIL") or url == "TIMEOUT": print(os.path.basename(path), url, flush=True); return False
    subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", path, url], check=True); print(os.path.basename(path), "ok", flush=True); return True


def upload(path):
    b = base64.b64encode(open(path, "rb").read()).decode(); tmp = path + ".up.json"
    json.dump({"base64Data": "data:image/png;base64," + b, "uploadPath": "images/user", "fileName": os.path.basename(path)}, open(tmp, "w"))
    out = subprocess.run(["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-base64-upload", "-H", f"Authorization: Bearer {KEY}",
                          "-H", "Content-Type: application/json", "-A", "Mozilla/5.0", "--data-binary", f"@{tmp}"], capture_output=True, text=True).stdout
    os.remove(tmp); return json.loads(out).get("data", {}).get("downloadUrl")


def one(name, prompt, outdir, model="gpt-image-2-text-to-image", refs=None, aspect="1:1", retry=1):
    path = f"{outdir}/{name}.png"
    if os.path.exists(path): return
    for _ in range(retry + 1):
        if model == "z-image":
            inp = {"prompt": prompt[:790], "aspect_ratio": aspect, "image_size": "square"}
        elif refs:
            inp = {"prompt": prompt, "input_urls": refs, "aspect_ratio": aspect}
        else:
            inp = {"prompt": prompt, "aspect_ratio": aspect}
        if grab(wait(fire(model, inp)), path): return


def render(frames, outdir, model="gpt-image-2-text-to-image", aspect="1:1"):
    """frames: {name: prompt} or {name: (prompt, model, refs)}
    Refuses to fire without a passing preflight.md in the round folder (preflight_check.py; dreaming 2026-11-02, sessions 10-28_3ca8ae6d, 10-28_85e5fbe2, 10-29_ccab9cfb)."""
    os.makedirs(outdir, exist_ok=True)
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import preflight_check
    ok, msgs = preflight_check.check(outdir)
    if not ok:
        print("RENDER REFUSED, no preflight:\n  " + "\n  ".join(msgs), flush=True); return
    th = []
    for k, v in frames.items():
        p, m, r = (v, model, None) if isinstance(v, str) else (v[0], v[1] or model, v[2] if len(v) > 2 else None)
        th.append(threading.Thread(target=one, args=(k, p, outdir, m, r, aspect)))
    [t.start() for t in th]; [t.join() for t in th]
    print("ALL DONE", flush=True)


def sheet(outdir, title, names=None, cols=4, out="_sheet.png", labels=None):
    """contact sheet via headless Chrome"""
    import glob, html as H2
    outdir = os.path.abspath(outdir)
    files = [f"{outdir}/{n}.png" for n in names] if names else sorted(glob.glob(f"{outdir}/*.png") + glob.glob(f"{outdir}/*.jpg"))
    files = [f for f in files if os.path.exists(f) and "_sheet" not in f]
    cards = "".join(f'<figure><img src="file://{f}"><figcaption>{H2.escape((labels or {}).get(os.path.basename(f)[:-4], os.path.basename(f)[:-4]))}</figcaption></figure>' for f in files)
    rows = -(-len(files) // cols); W = 400 * cols
    doc = f"<!doctype html><meta charset=utf-8><style>body{{margin:0;background:#111;color:#fff;font-family:Helvetica;padding:10px}}h1{{font-size:22px;margin:0 0 10px}}.g{{display:grid;grid-template-columns:repeat({cols},380px);gap:10px}}figure{{margin:0}}img{{width:380px;height:380px;object-fit:cover;display:block}}figcaption{{font-size:15px;padding:4px 0;height:40px}}</style><h1>{H2.escape(title)}</h1><div class=g>{cards}</div>"
    hp = f"{outdir}/_sheet.html"; open(hp, "w").write(doc)
    import tempfile
    ud = tempfile.mkdtemp(prefix="sheetchrome")
    if os.path.exists(f"{outdir}/{out}"): os.remove(f"{outdir}/{out}")
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={ud}",
                    "--force-device-scale-factor=1", f"--window-size={W+40},{rows*440+60}", f"--screenshot={outdir}/{out}", f"file://{hp}"],
                   capture_output=True, timeout=120)
    return f"{outdir}/{out}"


def pair(before_png, after_png, out, left="BEFORE", right="AFTER", bar=None, S=1080):
    """REA treatment: optional black top bar with white Impact line, two halves, white bottom band with labels. No bar by default (ad pairs)."""
    from PIL import Image, ImageDraw, ImageFont
    def font(sz):
        for f in ["/Library/Fonts/Impact.ttf", "/System/Library/Fonts/Supplemental/Impact.ttf", "/System/Library/Fonts/Supplemental/Arial Black.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
            if os.path.exists(f): return ImageFont.truetype(f, sz)
        return ImageFont.load_default()
    topH = 130 if bar else 0; botH = 110; half = S // 2; ih = S - topH - botH
    def fit(im):
        im = im.convert("RGB"); w, h = im.size; tw = int(h * half / ih)
        if tw <= w: im = im.crop(((w - tw) // 2, 0, (w + tw) // 2, h))
        else:
            th = int(w * ih / half); im = im.crop((0, max(0, (h - th) // 3), w, max(0, (h - th) // 3) + th))
        return im.resize((half, ih))
    canvas = Image.new("RGB", (S, S), "white"); d = ImageDraw.Draw(canvas)
    if bar:
        d.rectangle([0, 0, S, topH], fill="black"); sz = 90
        while d.textlength(bar, font=font(sz)) > S - 40 and sz > 30: sz -= 4
        f = font(sz); tw = d.textlength(bar, font=f); d.text(((S - tw) / 2, (topH - sz) / 2 - 6), bar, fill="white", font=f)
    canvas.paste(fit(Image.open(before_png)), (0, topH)); canvas.paste(fit(Image.open(after_png)), (half, topH))
    d.rectangle([half - 3, topH, half + 3, topH + ih], fill="white")
    for txt, x0 in ((left, 0), (right, half)):
        sz = 64
        while d.textlength(txt, font=font(sz)) > half - 30 and sz > 24: sz -= 2
        f = font(sz); tw = d.textlength(txt, font=f); d.text((x0 + (half - tw) / 2, S - botH + 18 + (64 - sz) // 2), txt, fill="black", font=f)
    canvas.save(out, quality=92); return out


def degrade(path, out=None):
    """bake phone-photo degradation into a render (REA r8): downscale, jpeg, noise, warm cast."""
    from PIL import Image, ImageFilter, ImageEnhance
    import random
    im = Image.open(path).convert("RGB"); w, h = im.size
    im = im.resize((int(w * 0.55), int(h * 0.55))).filter(ImageFilter.GaussianBlur(0.6)).resize((w, h))
    px = im.load()
    for _ in range(int(w * h * 0.03)):
        x, y = random.randrange(w), random.randrange(h); r, g, b = px[x, y]; n = random.randint(-18, 18); px[x, y] = (min(255, max(0, r + n)), min(255, max(0, g + n)), min(255, max(0, b + n)))
    r, g, b = im.split(); r = r.point(lambda v: min(255, int(v * 1.05))); b = b.point(lambda v: int(v * 0.93)); im = Image.merge("RGB", (r, g, b))
    im = ImageEnhance.Contrast(im).enhance(1.04)
    out = out or path; im.save(out, "JPEG", quality=58); return out


def _font(sz, bold=True):
    from PIL import ImageFont
    for f in (["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf"] if bold else ["/System/Library/Fonts/Supplemental/Arial.ttf"]) + ["/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def snap(path, line, out=None, y=0.64, sz=44):
    """IMG14 device: translucent black Snapchat-style caption bar across the photo with one white sentence (PIL, real text)."""
    from PIL import Image, ImageDraw
    im = Image.open(path).convert("RGBA"); W, Hh = im.size; f = _font(sz, bold=False)
    d = ImageDraw.Draw(im); words = line.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > W - 80: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur); lh = int(sz * 1.3); bh = lh * len(lines) + 36
    bar = Image.new("RGBA", (W, bh), (0, 0, 0, 165)); im.alpha_composite(bar, (0, int(Hh * y) - bh // 2))
    d = ImageDraw.Draw(im); yy = int(Hh * y) - bh // 2 + 18
    for ln in lines:
        tw = d.textlength(ln, font=f); d.text(((W - tw) / 2, yy), ln, fill="white", font=f); yy += lh
    out = out or path.replace(".png", "-snap.jpg"); im.convert("RGB").save(out, quality=90); return out


def tagpair(left_png, right_png, out, left_tag, right_tag, left_bad=True, S=1080):
    """IMG16 device: two photos side by side, each with a label chip top-left; red X on the bad side, green check on the good side."""
    from PIL import Image, ImageDraw
    half = S // 2
    def fit(im):
        im = im.convert("RGB"); w, h = im.size; tw = h // 2
        if tw <= w: im = im.crop(((w - tw) // 2, 0, (w + tw) // 2, h))
        else: th = w * 2; im = im.crop((0, max(0, (h - th) // 3), w, max(0, (h - th) // 3) + th))
        return im.resize((half, S))
    c = Image.new("RGB", (S, S), "white"); c.paste(fit(Image.open(left_png)), (0, 0)); c.paste(fit(Image.open(right_png)), (half, 0))
    d = ImageDraw.Draw(c); d.rectangle([half - 3, 0, half + 3, S], fill="white"); f = _font(54)
    for tag, x0, bad in ((left_tag, 0, left_bad), (right_tag, half, not left_bad)):
        sz = 54
        while d.textlength(tag, font=_font(sz)) > half - 80 and sz > 22: sz -= 2
        f = _font(sz); tw = d.textlength(tag, font=f); pad = 16
        d.rectangle([x0 + 24, 24, x0 + 24 + tw + 2 * pad, 24 + sz + 2 * pad], fill="white"); d.text((x0 + 24 + pad, 24 + pad - 4), tag, fill="black", font=f)
        if bad:
            fm = _font(150); mw = d.textlength("X", font=fm); d.text((x0 + half - mw - 40, S - 190), "X", fill=(220, 30, 30), font=fm, stroke_width=6, stroke_fill="white")
        else:
            bx, by = x0 + half - 150, S - 150
            pts = [(bx, by + 10), (bx + 38, by + 55), (bx + 110, by - 40)]
            d.line(pts, fill="white", width=34, joint="curve"); d.line(pts, fill=(30, 160, 60), width=20, joint="curve")
    c.save(out, quality=92); return out


def fbpost(out, name, text, photo, comments, when="3h"):
    """hand-built Facebook post screenshot (HTML -> headless Chrome), the IMG20 device."""
    import html as H2
    cm = "".join(f'<div class=c><div class=av></div><div class=b><b>{H2.escape(n)}</b> {H2.escape(t)}</div></div>' for n, t in comments)
    doc = f"""<!doctype html><meta charset=utf-8><style>body{{margin:0;background:#fff;width:1080px;height:1080px;font-family:-apple-system,Helvetica,Arial;overflow:hidden}}
.p{{padding:28px 34px 0}}.h{{display:flex;align-items:center;gap:16px}}.pv{{width:72px;height:72px;border-radius:50%;background:#c9b8a8}}.n{{font-weight:700;font-size:32px}}.t{{color:#65676b;font-size:24px}}
.x{{font-size:34px;line-height:1.3;margin:22px 0 18px}}img{{width:1080px;height:520px;object-fit:cover;display:block}}
.r{{display:flex;justify-content:space-between;padding:14px 34px;color:#65676b;font-size:24px;border-bottom:1px solid #ddd}}
.c{{display:flex;gap:12px;padding:12px 34px 0}}.av{{width:52px;height:52px;border-radius:50%;background:#b8c4d6;flex:none}}.b{{background:#f0f2f5;border-radius:22px;padding:10px 18px;font-size:23px;line-height:1.2}}</style>
<div class=p><div class=h><div class=pv></div><div><div class=n>{H2.escape(name)}</div><div class=t>{when} · 🌎</div></div></div><div class=x>{H2.escape(text)}</div></div>
<img src="file://{photo}"><div class=r><span>👍❤️😮 1.2K</span><span>847 comments · 312 shares</span></div>{cm}"""
    hp = out + ".html"; open(hp, "w").write(doc)
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1080,1080", f"--screenshot={out}", f"file://{hp}"], capture_output=True)
    return out
