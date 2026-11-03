# SkyHouse creative skills

Ryan's Claude Code skills for ad creative: one-shot video, static images, landers and cold hooks. Each lives in `.claude/skills/<name>/SKILL.md` and is the whole method; read it before running anything.

## The four skills

| Skill | Say | What it does | Needs |
|---|---|---|---|
| `oneshot-video` | "one-shot this video" | script in, lip-synced captioned `final.mp4` out on Kie | `tools/video/`, python env below, ffmpeg, whisper.cpp |
| `strategist-images` | "strategist, make images for this ad" | ad statics, lander heroes, thumbnails, before/after pairs on Kie (gpt-image-2, z-image); `formats.md` is the graded format library | `tools/statics/`, `strategist-references/winning-statics-study.md` |
| `strategist-lander` + `strategist-lander-qa` | "strategist, build the lander" / "QA this lander" | finished advertorial copy to a deploy-ready static HTML page in the house system, then a fresh-agent inspection; `tools/landers/deploy.sh` pushes to Cloudflare R2 behind a gate | `lander-source/` (Ryan's shipped pages), `strategist-references/swipe-learnings.md`, wrangler + Cloudflare keys in `.env` |
| `hook-writer` | "hooks for <offer>" | short cold Facebook hooks under five rules in `tools/hooks/rules/short-cold.json`, each passed through a mechanical gate and a stranger judge (headless `claude`, needs `claude login`) | `tools/hooks/`, `offers/_examples/short-cold-approved.md` |

`tools/copygate/` is the cold-read judge the lander and ad lanes call (`python3 tools/copygate/coldread.py judge <file>`), plus three Claude Code hooks. `.claude/settings.example.json` wires them (skill-first gate on copy writes, cold-read note after writes, hook-writer judge stamp on stop); copy it to `.claude/settings.json` if you want the same guardrails.

## One-shot video

Turns a finished script into a captioned, lip-synced AI video ad (`final.mp4`) on the Kie API with local ffmpeg. The video model speaks every line in one locked voice, every clip is machine-checked for exact words, same voice and lip sync, misses are rerolled, and a listening judge scores the voice.

## What is in here (video)

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
