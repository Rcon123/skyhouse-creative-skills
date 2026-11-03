"""Zapply-style typography pass (measured from Zapply m2130474244574046, ref/STUDY.md 2026-10-21).

Run after `oneshot.py assemble` on a project whose plan has captions.enabled false and an "overlay" block:

  "overlay": {
    "hook":  {"beat": "b01", "pills": [["3 WARNING SIGNS", "red"], ["Your dog's teeth", "white"], ["ARE ROTTING", "red"]]},
    "signs": [{"beat": "b02", "label": "SIGN #1:", "text": "The back teeth have gone brown."}, ...],
    "body":  [{"beat": "b06", "label": null}, {"beat": "b07", "label": "DAY 1"}, ...]
  }

- hook: three stacked pills (red / white / red), centred at 62% of frame height, held for the beat.
- signs: a red pill with the label at 56% height and the full sentence under it in white with a shadow, held for the beat
  while the pictures change under it.
- body: the spoken words two at a time in white condensed heavy caps with a shadow at 66% height, from the state's
  word timings (script words, never the transcriber's), with an optional white pill label (DAY 1) above.
Writes final_signs.mp4 next to final.mp4. Picture and audio are never re-timed.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.abspath(sys.argv[1])
W, H = 1080, 1920
IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
SANS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Montserrat-VF.ttf")
RED, WHITE, BLACK, NAVY = (226, 28, 28), (255, 255, 255), (0, 0, 0), (26, 36, 84)
OV = os.path.join(HERE, "build", "ov"); os.makedirs(OV, exist_ok=True)

plan = json.load(open(os.path.join(HERE, "plan.json")))
state = json.load(open(os.path.join(HERE, "state.json")))
words = state["words"]
conf = plan.get("overlay") or {}
replace = (plan.get("captions") or {}).get("replace") or {}


def font(path, size, var=None):
    f = ImageFont.truetype(path, size)
    if var:
        try:
            f.set_variation_by_name(var)
        except Exception:
            pass
    return f


def span(beat):
    ws = [w for w in words if w["beat"] == beat]
    return ws[0]["s"], ws[-1]["e"]


def shadow_text(d, xy, text, f, fill, shadow=(0, 0, 0, 200), off=4):
    x, y = xy
    for dx, dy in ((off, off), (off, 0), (0, off)):
        d.text((x + dx, y + dy), text, font=f, fill=shadow)
    d.text((x, y), text, font=f, fill=fill)


def pill_img(d, text, f, cy, bg, fg, pad_x=34, pad_y=14, radius=18):
    tw = d.textlength(text, font=f)
    th = f.size * 1.15
    x0, y0 = (W - tw) / 2 - pad_x, cy - th / 2 - pad_y
    d.rounded_rectangle([x0, y0, x0 + tw + pad_x * 2, y0 + th + pad_y * 2], radius=radius, fill=bg)
    d.text(((W - tw) / 2, y0 + pad_y), text, font=f, fill=fg)
    return th + pad_y * 2


def hook_card(pills, name):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fb = font(SANS, 58, "ExtraBold"); fr = font(SANS, 50, "Medium")
    y = int(H * 0.62) - 110
    for text, style in pills:
        if style == "red":
            h = pill_img(d, text, fb, y, RED, WHITE)
        else:
            h = pill_img(d, text, fr, y, WHITE, BLACK)
        y += int(h) + 10
    p = os.path.join(OV, name + ".png"); im.save(p); return p


def sign_card(label, text, name):
    """The reference's sign: a red pill 'SIGN #1:' centred at 56% height, the sentence under it in white bold with a black outline."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fl = font(SANS, 66, "ExtraBold"); ft = font(SANS, 50, "Bold")
    cy = int(H * 0.56)
    h = pill_img(d, label, fl, cy, RED, WHITE, pad_x=40, pad_y=14, radius=18)
    lines, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=ft) > 860 and cur:
            lines.append(cur); cur = wd
        else:
            cur = t
    if cur: lines.append(cur)
    y = cy + int(h / 2) + 14
    for ln in lines:
        tw = d.textlength(ln, font=ft)
        d.text(((W - tw) / 2, y), ln, font=ft, fill=WHITE, stroke_width=5, stroke_fill=BLACK)
        y += 60
    p = os.path.join(OV, name + ".png"); im.save(p); return p


def body_page(text, label, name):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fi = ImageFont.truetype(IMPACT, 74)
    cy = int(H * 0.66)
    if label:
        fl = font(SANS, 54, "ExtraBold")
        pill_img(d, label, fl, cy - 90, WHITE, NAVY, pad_x=30, pad_y=10, radius=16)
    tw = d.textlength(text, font=fi)
    shadow_text(d, ((W - tw) / 2, cy), text, fi, WHITE, off=5)
    p = os.path.join(OV, name + ".png"); im.save(p); return p


def display(w):
    t = w
    for k, v in replace.items():
        if t.lower() == k.lower():
            t = v
    return t.upper()


overlays = []  # (png, start, end)
hk = conf.get("hook")
if hk:
    s, e = span(hk["beat"])
    overlays.append((hook_card(hk["pills"], "hook"), s, e + 0.25))
for i, sg in enumerate(conf.get("signs", [])):
    s, e = span(sg["beat"])
    overlays.append((sign_card(sg["label"], sg["text"], f"sign{i}"), s, e + 0.25))
n = 0
for bd in conf.get("body", []):
    ws = [w for w in words if w["beat"] == bd["beat"]]
    per = int(bd.get("words", 2))
    for i in range(0, len(ws), per):
        page = ws[i:i + per]
        text = " ".join(display(w["w"].strip(".,?!")) for w in page)
        nxt = ws[i + per]["s"] if i + per < len(ws) else page[-1]["e"] + 0.2
        overlays.append((body_page(text, bd.get("label"), f"body{n:03d}"), page[0]["s"], nxt))
        n += 1

src = os.path.join(HERE, "final.mp4"); out = os.path.join(HERE, "final_signs.mp4")
inputs, chain, cur, idx = ["-i", src], [], "[0:v]", 1
for k, (p, s, e) in enumerate(overlays):
    inputs += ["-i", p]
    chain.append(f"{cur}[{k + 1}:v]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'[v{idx}]"); cur = f"[v{idx}]"; idx += 1
cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(chain), "-map", cur, "-map", "0:a",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)
print("wrote", out, "overlays", len(overlays))
