#!/usr/bin/env python3
"""Is this the same voice? Speaker-embedding similarity between audio or video files.

Uses SpeechBrain's ECAPA speaker-verification model (trained on VoxCeleb). Cosine similarity:
about 0.6 and up reads as the same speaker, 0.3 to 0.6 is doubtful, under 0.3 is a different
voice. Calibrate on your own clips: the same generated voice across two clips scored 0.7 to 0.8
here, different models scored 0.1 to 0.4.

  tools/video/.venv/bin/python tools/video/voice_match.py ANCHOR FILE [FILE ...]
"""
import os
import subprocess
import sys
import tempfile

import numpy as np

_model = None


def _load():
    global _model
    if _model is None:
        import torch  # noqa: F401
        from speechbrain.inference.speaker import EncoderClassifier
        cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor", "models", "ecapa")
        _model = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir=cache,
                                                run_opts={"device": "cpu"})
    return _model


def embed(path):
    import torch
    from scipy.io import wavfile
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", tmp], check=True, stdin=subprocess.DEVNULL)
    sr, a = wavfile.read(tmp)
    os.unlink(tmp)
    x = torch.from_numpy(a.astype(np.float32) / 32768.0).unsqueeze(0)
    with torch.no_grad():
        e = _load().encode_batch(x).squeeze().numpy()
    return e / (np.linalg.norm(e) + 1e-9)


def similarity(a, b):
    return float(np.dot(embed(a), embed(b)))


if __name__ == "__main__":
    anchor = embed(sys.argv[1])
    for f in sys.argv[2:]:
        print(f"{float(np.dot(anchor, embed(f))):.3f}  {os.path.basename(f)}")
