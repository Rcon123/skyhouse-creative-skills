#!/usr/bin/env python3
"""Pixelate one rectangle of a clip (the held-back #1 toxin pour in Bone in the Bowl, 2026-11-05).

    pixelate.py <clip.mp4> <x> <y> <w> <h> [--block 28] [--out path]

x y w h are fractions of the frame (0 to 1). The original is kept beside the output as <clip>.raw.mp4 when
--out is omitted, so the pipeline's clips/<id>.mp4 becomes the pixelated one and the raw take is never lost.
Audio is copied untouched (the mouth and the voice are not in the box, so the sync gate still scores the clip).
"""
import argparse, os, shutil, subprocess, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("x", type=float); ap.add_argument("y", type=float)
    ap.add_argument("w", type=float); ap.add_argument("h", type=float)
    ap.add_argument("--block", type=int, default=28, help="pixel block size on the output frame height scale")
    ap.add_argument("--out")
    a = ap.parse_args()
    src = a.clip
    out = a.out
    if not out:
        raw = src[:-4] + ".raw.mp4"
        if not os.path.exists(raw):
            shutil.copy2(src, raw)
        src, out = raw, a.clip
    # probe size
    wh = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                  "-of", "csv=p=0", src]).decode().strip().split(",")
    W, H = int(wh[0]), int(wh[1])
    x, y, w, h = int(a.x * W), int(a.y * H), int(a.w * W), int(a.h * H)
    x -= x % 2; y -= y % 2; w -= w % 2; h -= h % 2
    f = max(2, a.block)
    sw, sh = max(2, w // f), max(2, h // f)
    vf = (f"[0:v]split[base][box];[box]crop={w}:{h}:{x}:{y},scale={sw}:{sh}:flags=area,"
          f"scale={w}:{h}:flags=neighbor[pix];[base][pix]overlay={x}:{y}[v]")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", vf, "-map", "[v]", "-map", "0:a?",
           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", out]
    subprocess.check_call(cmd)
    print(f"pixelated {out}: box x={x} y={y} w={w} h={h} on {W}x{H}, block {f}; raw kept at {src if src != a.clip else out}")


if __name__ == "__main__":
    main()
