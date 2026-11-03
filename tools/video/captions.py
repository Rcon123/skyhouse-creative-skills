#!/usr/bin/env python3
"""Captions for the one-shot video pipeline.

The local ffmpeg has no subtitles/ass/drawtext filter, so captions are drawn
with Pillow and piped into ffmpeg as a transparent band that is overlaid on the
picture. Words and timing come from the voice step (script words, whisper
timing), so captions are word-perfect and land on the spoken word.

Plan options (all optional), under "captions":
  enabled      true
  max_words    3           words per page
  max_chars    16          characters per page before a new page starts
  size         88          px at 1080x1920 (84 to 96 reads well for buyers over 60)
  y            1150        center line of the caption block (keep under 1248: Meta's bottom 35% is UI)
  upper        true
  color        "#FFFFFF"
  highlight    "#FFE600"   the word being spoken
  stroke       8
  weight       "ExtraBold"
  replace      {"twenty twenty six": "2026"}   spoken phrase -> how it should display

"hook_text": {"text": "...", "start": 0, "end": 4.5, "y": 300, "size": 64}
  white rounded box, black text, top of frame (inside the safe zone).
"""
import os
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
FONT = os.path.join(HERE, "fonts", "Montserrat-VF.ttf")
FALLBACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def _font(size, weight="ExtraBold"):
    try:
        f = ImageFont.truetype(FONT, size)
        f.set_variation_by_name(weight)
        return f
    except Exception:
        return ImageFont.truetype(FALLBACK, size)


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))


def _apply_replace(words, replace):
    if not replace:
        return words
    out, i = [], 0
    keys = sorted(((k.split(), v) for k, v in replace.items()), key=lambda kv: -len(kv[0]))
    while i < len(words):
        hit = False
        for ks, v in keys:
            n = len(ks)
            if [_norm(w["w"]) for w in words[i:i + n]] == [_norm(k) for k in ks]:
                tail = re.search(r"[.,?!]+$", words[i + n - 1]["w"])
                out.append({**words[i], "w": v + (tail.group(0) if tail else ""), "e": words[i + n - 1]["e"]})
                i += n
                hit = True
                break
        if not hit:
            out.append(dict(words[i]))
            i += 1
    return out


def pages(words, conf):
    max_words, max_chars = conf.get("max_words", 3), conf.get("max_chars", 16)
    words = _apply_replace(words, conf.get("replace"))
    out, cur = [], []
    for w in words:
        kept = re.sub(r"(?<!\d),|,(?!\d)", "", w["w"].replace("\u2019", "'"))         # a comma survives only inside a number: "$2,000"
        shown = re.sub(r"[^\w' $%&\-,]", "", kept).strip()   # keep spaces: "over 60" stays two words on screen
        if not shown:
            continue
        item = {"t": shown.upper() if conf.get("upper", True) else shown, "s": w["s"], "e": w["e"],
                "stop": bool(re.search(r"[.?!]$", w["w"])), "soft": bool(re.search(r"[,;:]$", w["w"]))}
        if cur:
            chars = sum(len(x["t"]) for x in cur) + len(cur) + len(item["t"])
            brk = (len(cur) >= max_words or chars > max_chars or cur[-1]["stop"]
                   or (cur[-1]["soft"] and len(cur) >= 2) or item["s"] - cur[-1]["e"] > 0.45)
            if brk:
                out.append(cur)
                cur = []
        cur.append(item)
    if cur:
        out.append(cur)
    res = []
    for i, p in enumerate(out):
        start = max(0.0, p[0]["s"] - 0.04)
        end = p[-1]["e"] + 0.30
        if i + 1 < len(out):
            end = min(end, out[i + 1][0]["s"] - 0.04)
        res.append({"words": p, "start": start, "end": max(end, start + 0.2)})
    return res


def _layout(draw, font, texts, max_w):
    """Split a page into one or two centered lines."""
    space = draw.textlength(" ", font=font)
    widths = [draw.textlength(t, font=font) for t in texts]
    total = sum(widths) + space * (len(texts) - 1)
    if total <= max_w or len(texts) == 1:
        return [list(range(len(texts)))], widths, space
    best, split = None, 1
    for k in range(1, len(texts)):
        a = sum(widths[:k]) + space * (k - 1)
        b = sum(widths[k:]) + space * (len(texts) - k - 1)
        if best is None or max(a, b) < best:
            best, split = max(a, b), k
    return [list(range(split)), list(range(split, len(texts)))], widths, space


def render_band(page, active, conf, band_h):
    size, stroke = conf.get("size", 88), conf.get("stroke", 8)
    font = _font(size, conf.get("weight", "ExtraBold"))
    img = Image.new("RGBA", (W, band_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    texts = [w["t"] for w in page["words"]]
    lines, widths, space = _layout(d, font, texts, W - 160)
    line_h = int(size * 1.16)
    y = (band_h - line_h * len(lines)) // 2
    for line in lines:
        lw = sum(widths[i] for i in line) + space * (len(line) - 1)
        x = (W - lw) / 2
        for i in line:
            fill = conf.get("highlight", "#FFE600") if i == active else conf.get("color", "#FFFFFF")
            d.text((x, y), texts[i], font=font, fill=fill, stroke_width=stroke, stroke_fill="#000000")
            x += widths[i] + space
        y += line_h
    return img


def render_hook(conf, dest):
    size = conf.get("size", 62)
    font = _font(size, "Bold")
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    words, lines, cur = conf["text"].split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) > W - 220 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    line_h = int(size * 1.28)
    y = conf.get("y", 300)
    pad = 26
    for ln in lines:
        tw = d.textlength(ln, font=font)
        x = (W - tw) / 2
        d.rounded_rectangle([x - pad, y - 8, x + tw + pad, y + line_h], radius=18, fill=(255, 255, 255, 245))
        d.text((x, y + 2), ln, font=font, fill="#111111")
        y += line_h + 6
    img.save(dest)
    return dest


def burn(pr, picture, audio, final, total_frames, vf_tail, enc):
    plan = pr.plan
    conf = plan.get("captions") or {}
    hook = plan.get("hook_text")
    use_caps = conf.get("enabled", True)
    size = conf.get("size", 88)
    band_h = int(size * 1.16 * 2 + 48) // 2 * 2
    band_y = int(conf.get("y", 1150) - band_h / 2)
    pgs = pages(pr.state["words"], conf) if use_caps else []

    ins = ["-i", picture, "-i", audio]
    filt, last, idx = [], "[0:v]", 2
    if use_caps:
        ins += ["-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{band_h}", "-r", str(FPS), "-i", "-"]
        filt.append(f"{last}[{idx}:v]overlay=0:{band_y}:format=auto[c]")
        last, idx = "[c]", idx + 1
    if hook:
        hp = render_hook(hook, pr.p("build/hook.png"))
        ins += ["-loop", "1", "-i", hp]
        t0, t1 = hook.get("start", 0), hook.get("end") or total_frames / FPS
        filt.append(f"{last}[{idx}:v]overlay=0:0:enable='between(t,{t0},{t1})':shortest=0[h]")
        last, idx = "[h]", idx + 1
    tail = ",".join(vf_tail) if vf_tail else "null"
    filt.append(f"{last}{tail},format=yuv420p[v]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filt),
           "-map", "[v]", "-map", "1:a", "-frames:v", str(total_frames), *enc, final]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE if use_caps else None)
    if use_caps:
        blank = Image.new("RGBA", (W, band_h), (0, 0, 0, 0)).tobytes()
        skip = pr.state.get("caption_skip") or []      # footage that carries its own burned-in captions
        cache, pi = {}, 0
        for f in range(total_frames):
            t = f / FPS
            while pi < len(pgs) and t >= pgs[pi]["end"]:
                pi += 1
            if any(a <= t < b for a, b in skip):
                proc.stdin.write(blank)
            elif pi < len(pgs) and pgs[pi]["start"] <= t:
                ws = pgs[pi]["words"]
                active = max([i for i, w in enumerate(ws) if w["s"] <= t + 0.02] or [0])
                key = (pi, active)
                if key not in cache:
                    cache.clear() if len(cache) > 6 else None
                    cache[key] = render_band(pgs[pi], active, conf, band_h).tobytes()
                proc.stdin.write(cache[key])
            else:
                proc.stdin.write(blank)
        proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("captions: ffmpeg failed")
    return final
