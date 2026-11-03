#!/usr/bin/env python3
"""Phoneme check for single words in a native-voice clip.

Transcribers (whisper, Gemini) write the script word they expect even when the voice model
mispronounces it: "jowls" read as "joles" still comes back as "jowls". A phoneme recognizer
(wav2vec2 fine-tuned on espeak phonemes) reports the sounds that were actually made, so a
plan can demand a vowel:

    "voice": {"phoneme_gate": {"jowls": ["aʊ"]}}

Every listed word in a take must contain every listed phoneme in its window, or the take fails.
Calibration on macOS `say` (2026-10-16): "jowls" -> dʒ aʊ z, "bowls" -> b oʊ s, "jaws" -> dʒ a s.

    python3 phonemes.py CLIP.mp4 START END      # phonemes in a window
"""
import json
import os
import subprocess
import sys
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "facebook/wav2vec2-lv-60-espeak-cv-ft"
_model = None


def _load():
    global _model
    if _model is None:
        import torch  # noqa: F401
        from transformers import Wav2Vec2ForCTC, Wav2Vec2FeatureExtractor
        from huggingface_hub import hf_hub_download
        fe = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
        m = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME).eval()
        vocab = json.load(open(hf_hub_download(MODEL_NAME, "vocab.json")))
        _model = (fe, m, {v: k for k, v in vocab.items()})
    return _model


def phonemes(path, t0, t1):
    """Phoneme string heard between t0 and t1 seconds of an audio or video file."""
    import numpy as np
    import torch
    fe, m, inv = _load()
    tmp = os.path.join("/tmp", f"_ph_{os.getpid()}.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{max(0.0, t0):.3f}", "-t", f"{max(0.05, t1 - t0):.3f}",
                    "-i", path, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp], check=True, stdin=subprocess.DEVNULL)
    with wave.open(tmp) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    os.unlink(tmp)
    if len(x) < 1600:
        return ""
    with torch.no_grad():
        ids = torch.argmax(m(**fe(x, sampling_rate=16000, return_tensors="pt")).logits, -1)[0].tolist()
    out, prev = [], None
    for i in ids:
        if i != prev and i != 0:
            out.append(inv.get(i, "?"))
        prev = i
    return " ".join(t for t in out if t not in ("<pad>", "<s>", "</s>", "<unk>", "|"))


def gate(wav, words, rules, pad=0.15):
    """words: whisper words [{w, s, e}]. rules: {"jowls": ["aʊ"]}. Returns {"faults": [...], "heard": {...}, "ok"}."""
    import re
    faults, heard = [], {}
    for w in words:
        key = re.sub(r"[^a-z']", "", w["w"].lower())
        for word, need in rules.items():
            if key != word.lower():
                continue
            ph = phonemes(wav, w["s"] - pad, w["e"] + pad)
            heard[f"{word}@{w['s']:.2f}"] = ph
            toks = ph.split()
            missing = [n for n in need if n not in toks]
            if missing:
                faults.append(f"'{word}' said without {'/'.join(missing)} (heard: {ph})")
    return {"faults": faults, "heard": heard, "ok": not faults}


if __name__ == "__main__":
    print(phonemes(sys.argv[1], float(sys.argv[2]), float(sys.argv[3])))
