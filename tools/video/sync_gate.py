#!/usr/bin/env python3
"""Lip-sync gate for one talking clip.

Scores a video against the audio that was supposed to drive it and prints a
JSON verdict. Three stages:

  0. container: clip length vs audio length (ffprobe)
  1. mouth signal: MediaPipe lip gap vs audio loudness (flapping in silence,
     frozen in speech, gross lag)
  2. SyncNet: AV offset in frames at 25 fps + confidence

Usage:
  .venv/bin/python sync_gate.py CLIP.mp4 [--audio DRY_CHUNK.wav] [--json OUT.json]

Run with the venv python in tools/video/.venv (needs torch + mediapipe).
Always score against the DRY voice chunk, never a mix with music.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
SYNCNET_DIR = os.path.join(HERE, "vendor", "syncnet_python")
SYNCNET_WEIGHTS = os.path.join(SYNCNET_DIR, "data", "syncnet_v2.model")
FACE_MODEL = os.path.join(HERE, "vendor", "models", "face_landmarker.task")

FPS = 25          # SyncNet is trained at 25 fps video
SR = 16000        # and 16 kHz audio
VSHIFT = 15       # search window, frames

# Gate thresholds, calibrated on the 2026-10-05 bake-off (9 clips, 5 engines: every good
# clip scored confidence 7.4 to 8.6, offsets -3 to 0). Offset sign, verified by shifting
# audio on a known clip: POSITIVE = sound arrives before the mouth moves, NEGATIVE = mouth
# leads the sound. Real speech has the mouth leading by about a frame, and viewers notice
# early sound (45 ms) long before late sound (125 ms), so the pass window is lopsided.
CONF_FAIL = 3.0
CONF_PASS = 5.0
OFFSET_MIN = -3   # frames at 25 fps, mouth leading
OFFSET_MAX = 1    # sound leading
OFFSET_TARGET = -1
OFFSET_FIXABLE = 7  # a clean constant offset this size is slid out at assembly


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, stdin=subprocess.DEVNULL)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-print_format", "json",
               "-show_format", "-show_streams", path]).stdout
    info = json.loads(out)
    res = {"duration": float(info["format"].get("duration", 0))}
    for s in info["streams"]:
        if s["codec_type"] == "video" and "video" not in res:
            num, den = s.get("avg_frame_rate", "0/1").split("/")
            res["video"] = {
                "w": s["width"], "h": s["height"],
                "fps": (float(num) / float(den)) if float(den) else 0.0,
                "duration": float(s.get("duration", res["duration"])),
                "start": float(s.get("start_time", 0) or 0),
            }
        if s["codec_type"] == "audio" and "audio" not in res:
            res["audio"] = {
                "duration": float(s.get("duration", res["duration"])),
                "start": float(s.get("start_time", 0) or 0),
            }
    return res


def read_frames(path, max_h=540):
    """Decode to 25 fps BGR frames, downscaled so the long work stays fast."""
    info = probe(path)["video"]
    scale = min(1.0, max_h / info["h"])
    w = int(info["w"] * scale) // 2 * 2
    h = int(info["h"] * scale) // 2 * 2
    proc = subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={FPS}:start_time=0,scale={w}:{h}",
         "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
        stdout=subprocess.PIPE, stdin=subprocess.DEVNULL)
    frames = []
    size = w * h * 3
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size:
            break
        frames.append(np.frombuffer(buf, np.uint8).reshape(h, w, 3))
    proc.wait()
    return frames


def read_audio(path):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-vn", "-ac", "1",
         "-af", "aresample=async=1:first_pts=0",   # keep any container start offset as real silence
         "-ar", str(SR), "-acodec", "pcm_s16le", tmp])
    sr, audio = wavfile.read(tmp)
    os.unlink(tmp)
    return audio


def face_track(frames):
    """Per frame: face box (cx, cy, half-size) and a normalized lip gap."""
    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision

    opts = vision.FaceLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=FACE_MODEL,
                                           delegate=mp_python.BaseOptions.Delegate.CPU),
        running_mode=vision.RunningMode.VIDEO, num_faces=1,
        min_face_detection_confidence=0.3, min_face_presence_confidence=0.3)
    boxes, gaps = [], []
    with vision.FaceLandmarker.create_from_options(opts) as lm:
        for i, f in enumerate(frames):
            h, w = f.shape[:2]
            img = mp.Image(image_format=mp.ImageFormat.SRGB,
                           data=cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            r = lm.detect_for_video(img, int(i * 1000 / FPS))
            if not r.face_landmarks:
                boxes.append(None)
                gaps.append(np.nan)
                continue
            pts = np.array([(p.x * w, p.y * h) for p in r.face_landmarks[0]])
            x0, y0 = pts.min(0)
            x1, y1 = pts.max(0)
            boxes.append(((x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) / 2))
            eye = np.linalg.norm(pts[33] - pts[263]) + 1e-6
            gaps.append(float(np.linalg.norm(pts[13] - pts[14]) / eye))
    return boxes, np.array(gaps)


def fill_boxes(boxes):
    """Hold the nearest detection through short dropouts, then median-smooth."""
    idx = [i for i, b in enumerate(boxes) if b is not None]
    if not idx:
        return None
    arr = np.zeros((len(boxes), 3))
    for i in range(len(boxes)):
        j = min(idx, key=lambda k: abs(k - i))
        arr[i] = boxes[j]
    k = 13 if len(boxes) >= 13 else (len(boxes) // 2 * 2 - 1 or 1)
    for c in range(3):
        arr[:, c] = signal.medfilt(arr[:, c], kernel_size=k)
    return arr


def crop_faces(frames, arr, cs=0.40):
    """Same crop geometry as syncnet_python/run_pipeline.py crop_video."""
    out = []
    for f, (mx, my, bs) in zip(frames, arr):
        bsi = int(bs * (1 + 2 * cs))
        pad = np.pad(f, ((bsi, bsi), (bsi, bsi), (0, 0)), "constant", constant_values=110)
        my2, mx2 = my + bsi, mx + bsi
        face = pad[int(my2 - bs):int(my2 + bs * (1 + 2 * cs)),
                   int(mx2 - bs * (1 + cs)):int(mx2 + bs * (1 + cs))]
        out.append(cv2.resize(face, (224, 224)))
    return out


def syncnet(faces, audio, batch=20):
    import torch
    import python_speech_features
    sys.path.insert(0, SYNCNET_DIR)
    from SyncNetModel import S

    net = S(num_layers_in_fc_layers=1024)
    state = torch.load(SYNCNET_WEIGHTS, map_location="cpu", weights_only=True)
    own = net.state_dict()
    for name, param in state.items():
        own[name].copy_(param)
    net.eval()

    im = np.stack(faces, axis=3)                       # H W C T
    im = np.transpose(np.expand_dims(im, 0), (0, 3, 4, 1, 2))  # 1 C T H W
    imtv = torch.from_numpy(im.astype(np.float32))

    mfcc = python_speech_features.mfcc(audio, SR)      # T x 13 at 100 Hz
    cct = torch.from_numpy(mfcc.T[None, None].astype(np.float32))

    n = min(len(faces), len(audio) // 640)
    last = n - 5
    if last < 20:
        return None
    im_feat, cc_feat = [], []
    with torch.no_grad():
        for i in range(0, last, batch):
            rng = range(i, min(last, i + batch))
            im_in = torch.cat([imtv[:, :, v:v + 5] for v in rng], 0)
            cc_in = torch.cat([cct[:, :, :, v * 4:v * 4 + 20] for v in rng], 0)
            im_feat.append(net.forward_lip(im_in))
            cc_feat.append(net.forward_aud(cc_in))
    im_feat, cc_feat = torch.cat(im_feat), torch.cat(cc_feat)

    win = VSHIFT * 2 + 1
    cc_pad = torch.nn.functional.pad(cc_feat, (0, 0, VSHIFT, VSHIFT))
    dists = [torch.nn.functional.pairwise_distance(
        im_feat[[i]].repeat(win, 1), cc_pad[i:i + win]) for i in range(len(im_feat))]
    mdist = torch.mean(torch.stack(dists, 1), 1)
    minval, minidx = torch.min(mdist, 0)
    return {
        "offset_frames": int(VSHIFT - minidx),
        "confidence": round(float(torch.median(mdist) - minval), 3),
        "min_dist": round(float(minval), 3),
    }


def mouth_checks(gaps, audio):
    """Cheap checks from lip gap vs loudness. Lag here is coarse; SyncNet is the gate."""
    hop = SR // FPS
    n = min(len(gaps), len(audio) // hop)
    if n < 20:
        return {}
    a = audio[:n * hop].astype(np.float64).reshape(n, hop)
    rms = np.sqrt((a ** 2).mean(1)) + 1e-9
    db = 20 * np.log10(rms / (np.abs(audio).max() + 1e-9))
    speech = db > -35
    g = gaps[:n].copy()
    seen = ~np.isnan(g)
    if seen.sum() < 10:
        return {"face_ratio": round(float(seen.mean()), 3)}
    g[~seen] = np.nanmedian(g)
    base = np.percentile(g, 10)
    move = np.abs(np.diff(g, prepend=g[0]))

    def runs(mask, min_len):
        out, start = [], None
        for i, m in enumerate(list(mask) + [False]):
            if m and start is None:
                start = i
            elif not m and start is not None:
                if i - start >= min_len:
                    out.append((start, i))
                start = None
        return out

    # mouth WORKING during a silence of 0.4s or more. An open, resting mouth in a pause is
    # normal; chewing through the pause is not. Compare movement to movement during speech.
    speech_move = move[speech].mean() if speech.any() else 0.0
    flap = 0.0
    sil = runs(~speech, int(0.4 * FPS))
    for s, e in sil:
        seg = move[s + 4:e - 4]
        if len(seg) >= 3 and speech_move > 0 and seg.mean() > 0.7 * speech_move and seg.mean() > 0.006:
            flap += (e - s) / FPS
    # mouth still while speech runs 0.6s or more
    frozen = 0.0
    for s, e in runs(speech, int(0.6 * FPS)):
        if move[s:e].mean() < 0.004:
            frozen += (e - s) / FPS

    env = (rms - rms.mean()) / (rms.std() + 1e-9)
    gz = (g - g.mean()) / (g.std() + 1e-9)
    lags = range(-10, 11)
    cc = [float(np.mean(env[max(0, -l):n - max(0, l)] * gz[max(0, l):n - max(0, -l)])) for l in lags]
    best = int(np.argmax(cc))
    return {
        "face_ratio": round(float(seen.mean()), 3),
        "speech_ratio": round(float(speech.mean()), 3),
        "flap_in_silence_s": round(flap, 2),
        "frozen_in_speech_s": round(frozen, 2),
        "env_corr": round(cc[best], 3),
        "env_lag_frames": int(list(lags)[best]),
        "gap_range": round(float(np.percentile(g, 95) - base), 3),
    }


def gate(clip, audio_path=None):
    res = {"clip": clip, "audio": audio_path or "(clip audio)"}
    p = probe(clip)
    res["video"] = p.get("video")
    audio = read_audio(audio_path or clip)
    res["audio_duration"] = round(len(audio) / SR, 3)
    res["length_diff_s"] = round(p["video"]["duration"] - res["audio_duration"], 3)

    frames = read_frames(clip)
    boxes, gaps = face_track(frames)
    res["mouth"] = mouth_checks(gaps, audio)
    arr = fill_boxes(boxes)
    reasons = []
    if arr is None or res["mouth"].get("face_ratio", 0) < 0.6:
        res["verdict"] = "NO_FACE"
        res["reasons"] = ["face found in under 60% of frames; cannot score, do not treat as a pass"]
        return res
    res["face_px"] = int(arr[:, 2].mean() * 2 * probe(clip)["video"]["h"] / frames[0].shape[0])
    fh, fw = frames[0].shape[:2]
    res["face_center"] = [round(float(np.median(arr[:, 0])) / fw, 3), round(float(np.median(arr[:, 1])) / fh, 3)]
    res["syncnet"] = syncnet(crop_faces(frames, arr), audio)

    s = res["syncnet"]
    m = res["mouth"]
    verdict = "PASS"
    if s is None:
        verdict = "REVIEW"
        reasons.append("clip too short for SyncNet")
    else:
        off = s["offset_frames"]
        if s["confidence"] < CONF_FAIL:
            verdict = "FAIL"
            reasons.append(f"SyncNet confidence {s['confidence']} under {CONF_FAIL}: the mouth does not follow the audio")
        elif s["confidence"] < CONF_PASS:
            verdict = "REVIEW"
            reasons.append(f"SyncNet confidence {s['confidence']} between {CONF_FAIL} and {CONF_PASS}")
        if not (OFFSET_MIN <= off <= OFFSET_MAX) and verdict != "FAIL":
            if s["confidence"] >= CONF_PASS and abs(off) <= OFFSET_FIXABLE:
                verdict = "PASS_SHIFT" if verdict == "PASS" else verdict
                reasons.append(f"constant offset of {off} frames, slid out at assembly")
            else:
                verdict = "FAIL"
                reasons.append(f"AV offset {off} frames at 25 fps")
        res["shift_frames"] = (off - OFFSET_TARGET) if (s["confidence"] >= CONF_PASS and abs(off) <= OFFSET_FIXABLE
                                                         and not (OFFSET_TARGET - 1 <= off <= 0)) else 0
    if m.get("frozen_in_speech_s", 0) >= 1.0:
        verdict = "FAIL"
        reasons.append(f"mouth still for {m['frozen_in_speech_s']}s of speech")
    if m.get("flap_in_silence_s", 0) >= 1.0 and verdict == "PASS":
        verdict = "REVIEW"
        reasons.append(f"mouth moving for {m['flap_in_silence_s']}s of silence")
    if res["length_diff_s"] < -0.15:      # longer is fine (some engines round up); shorter cuts the last word
        verdict = "FAIL"
        reasons.append(f"clip is {-res['length_diff_s']}s shorter than its audio: the end of the line is cut off")
    res["verdict"] = verdict
    res["reasons"] = reasons
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("--audio", help="dry voice chunk that drove the clip (default: the clip's own audio)")
    ap.add_argument("--json", help="write the result here")
    a = ap.parse_args()
    out = gate(a.clip, a.audio)
    text = json.dumps(out, indent=2)
    if a.json:
        with open(a.json, "w") as fh:
            fh.write(text)
    print(text)
