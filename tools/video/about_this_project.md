# tools/video: the one-shot video pipeline

Code behind the `oneshot-video` skill (`.claude/skills/oneshot-video/SKILL.md`). Script and plan in, lip-synced captioned `final.mp4` out, on the Kie API with local ffmpeg.

## Files

| Path | What it is |
|---|---|
| `oneshot.py` | the pipeline: validate, voice, native, takes, frames, clips, gate, assemble, check, status, source (real footage cut into clips). Engine names and model ids live at the top (`TALK_ENGINES`, `BROLL_ENGINES`). |
| `kie.py` | Kie client: upload (JPEG conversion for big stills, 20 h cache), create, resume, wait, download, JSONL cost log |
| `sync_gate.py` | lip-sync scorer for one clip: ffprobe length check, MediaPipe mouth checks, SyncNet offset and confidence |
| `captions.py` | word-highlight captions drawn with Pillow and overlaid (the local ffmpeg has no subtitle or drawtext filter) |
| `voice_fx.py` | seats a clean generated voice in a room (convolution room, band limit, noise floor), timing untouched |
| `voice_judge.py` | listening judge: Gemini 3.1 Pro on Kie rates a clip 1 to 10, real recording vs TTS. Calibration in the docstring. |
| `voice_match.py` | same-voice check: ECAPA speaker embedding similarity between clips |
| `phonemes.py` | phoneme recognizer (wav2vec2 espeak) behind `voice.phoneme_gate`: hears a mispronounced word that whisper and Gemini transcribe as correct. Calibrated on macOS `say`. |
| `edit_review.py` | the editor's pass on a finished cut: floor continuity per segment, motion spikes per generated clip, the shot map. Runs before every hand-off (SKILL.md 6b). |
| `listen.py` | the ear: Gemini on Kie with a free question about a stretch of audio (music present? intelligible? one song or two?). Coarse: confirms a thing exists, cannot tune a level. |
| `enhance.py` | DeepFilterNet3 speech enhancement (shims the torchaudio I/O the package expects). Strips a song from under a voice when demucs cannot (`--atten 20` kept grandma usable on VID636; 100 made her robotic). |
| `voice_profile.py` | acoustic profile (pace, pauses, pitch, noise floor, room decay, band) to compare a voice with real footage |
| `voicelab/` | casting reels. `kid_r1/` = the 7-year-old casting (2026-10-16, five VOICE paragraphs on one line, `cast.py`). Round 2 voice work: `r1/` shootout clips and blind reels, `shootout_r1.py`, `reel.py`, `judge/` calibration clips, `native_mech_test/` |
| `voices.py` | voice board: one line in every Gemini TTS voice, pitch and pace measured, `voices/index.html` to listen |
| `voices/` | 68 voice samples + `voices.json` |
| `fonts/` | Montserrat (OFL) for captions and sheets |
| `.venv/` | Python 3.11 env: torch, mediapipe 0.10.21 (pinned, 1.0.1 crashes here), opencv, pillow, scipy |
| `vendor/syncnet_python/` | Joon Son Chung's SyncNet (MIT) + weights from Oxford VGG |
| `vendor/models/face_landmarker.task` | Google MediaPipe face landmarker |
| `bakeoff/` | the 2026-10-05 engine test: start frames, audio chunk, clips, scores, `run.py` to rerun it |
| `research/` | `lipsync-sota.md`, `prompting-workflows.md`, `kie-api.md` (full catalog and prices), `x-notes.md` (Ryan's X follows), `voice-realism.md` (voice sources, Kie voice routes, delivery marks, kitchen post chain, machine realism judges), `kie-docs-raw/` |
| `_scratch/` | throwaway test files, safe to delete |

## Run

```
tools/video/.venv/bin/python tools/video/oneshot.py validate <project>
tools/video/.venv/bin/python tools/video/oneshot.py frames|native|clips|gate|assemble|check <project> [--only id,id] [--force] [--engine name]   # voice instead of native in TTS mode
python3 tools/video/kie.py credits
```

Projects (plan.json + everything generated) live with their offer: `offers/<offer>/videos/<name>/`.

## Transcription (dreaming 2026-11-02, sessions 11-01_688ed675, 11-01_9949d507)

Whisper on this Mac is `/opt/homebrew/bin/whisper-cli` (whisper.cpp 1.8.4, Homebrew). `mlx_whisper`, `whisper-cpp` and `whisper` are not installed; do not probe for them. `tools/video/.venv` exists and is the Python env for everything else here.

## Rebuilding the env

```
/opt/homebrew/bin/python3.11 -m venv tools/video/.venv
tools/video/.venv/bin/pip install "mediapipe==0.10.21" opencv-python-headless pillow requests scipy soundfile python_speech_features torch torchvision torchaudio speechbrain
```
SyncNet weights: `vendor/syncnet_python/download_model.sh` lists the two URLs (only `syncnet_v2.model` is needed; faces are found with MediaPipe, not S3FD).
