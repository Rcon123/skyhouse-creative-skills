# SkyHouse one-shot video

Ryan's Claude Code skill that turns a finished script into a captioned, lip-synced AI video ad (`final.mp4`) on the Kie API with local ffmpeg. The video model speaks every line in one locked voice, every clip is machine-checked for exact words, same voice and lip sync, misses are rerolled, and a listening judge scores the voice.

## What is in here

| Path | What |
|---|---|
| `.claude/skills/oneshot-video/SKILL.md` | the skill Claude Code loads. Read it first; it is the whole method. |
| `.claude/skills/oneshot-video/references/` | lessons from past builds, craft rules, plan.json format, QA gates, model notes |
| `tools/video/` | the python pipeline. Start at `tools/video/about_this_project.md` for a file by file map. |
| `tools/video/research/` | the deep research: lip sync state of the art, prompting, the Kie catalog and prices, voice realism |
| `strategist-references/feminine-voice.md` | required reading before any line a woman speaks is planned |
| `offers/akka/videos/*/plan.json` | two working example plans the skill points at |

Left out on purpose: the python venv (1.7G), casting reels, the engine bakeoff and scratch files. Rebuild the env below.

## Setup

1. Drop this folder into a Claude Code project (or copy `.claude/skills/oneshot-video`, `tools/video` and `strategist-references` into yours). Paths in the skill are relative to the project root.
2. `cp .env.example .env` and put your Kie key in it.
3. Install ffmpeg and whisper.cpp: `brew install ffmpeg whisper-cpp` (the scripts call `/opt/homebrew/bin/whisper-cli`).
4. Python env (3.11):

```
/opt/homebrew/bin/python3.11 -m venv tools/video/.venv
tools/video/.venv/bin/pip install "mediapipe==0.10.21" opencv-python-headless pillow requests scipy soundfile python_speech_features torch torchvision torchaudio speechbrain
```

mediapipe is pinned; 1.0.1 crashed on macOS. SyncNet weights ship in `tools/video/vendor/syncnet_python/data/`. The ECAPA speaker model downloads itself from speechbrain on first run.

5. Check the key: `python3 tools/video/kie.py credits`

## Run

In Claude Code say "one-shot this video" with a script, or `/oneshot-video`. By hand:

```
tools/video/.venv/bin/python tools/video/oneshot.py validate <project>
tools/video/.venv/bin/python tools/video/oneshot.py frames|native|clips|gate|assemble|check <project>
```

A project is a folder with a `plan.json` (format in `references/plan-format.md`). Paid steps refuse to run until the swipe reference has been studied (`ref/STUDY.md`); that gate is deliberate.
