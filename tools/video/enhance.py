#!/usr/bin/env python3
"""Speech enhancement with DeepFilterNet3: strip music and background from a voice track, keep the speaker.
Used when a separated voice stem still carries the song (demucs puts a sung music track with the vocals).
  tools/video/.venv/bin/python tools/video/enhance.py IN.wav OUT.wav [--atten 100]
"""
import sys, types, dataclasses
# torchaudio >= 2.2 dropped torchaudio.backend.common; DeepFilterNet only wants the AudioMetaData record from it.
try:
    import torchaudio.backend.common  # noqa: F401
except Exception:
    import torchaudio
    m = types.ModuleType("torchaudio.backend.common")
    @dataclasses.dataclass
    class AudioMetaData:
        sample_rate: int = 0; num_frames: int = 0; num_channels: int = 0; bits_per_sample: int = 0; encoding: str = ""
    m.AudioMetaData = AudioMetaData
    sys.modules["torchaudio.backend.common"] = m
    if not hasattr(torchaudio, "backend"):
        torchaudio.backend = types.ModuleType("torchaudio.backend")
    torchaudio.backend.common = m
from df.enhance import enhance, init_df
import numpy as np, subprocess, tempfile, os, torch, soundfile as sf

def run(src, dst, atten=100.0):
    model, df_state, _ = init_df(log_level="ERROR")
    sr = df_state.sr()
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-ac", "1", "-ar", str(sr), "-c:a", "pcm_f32le", tmp], check=True, stdin=subprocess.DEVNULL)
    a, _ = sf.read(tmp, dtype="float32", always_2d=True); os.unlink(tmp)
    audio = torch.from_numpy(a.T.copy())                       # [channels, samples]
    out = enhance(model, df_state, audio, atten_lim_db=atten)
    sf.write(dst, out.squeeze(0).cpu().numpy(), sr, subtype="PCM_16")
    return dst

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    atten = float(sys.argv[sys.argv.index("--atten") + 1]) if "--atten" in sys.argv else 100.0
    print(run(a[0], a[1], atten))
