# Models and engines (tested, not assumed)

Everything here was rendered and scored in this workspace on 2026-10-05 unless a line says otherwise. Raw clips, scores and the runner live in `tools/video/bakeoff/`. The wider catalog (218 live Kie models, every parameter, every price) is in `tools/video/research/kie-api.md`. The market moves monthly, so when a new model lands, rerun the bake-off before changing a default (see the last section).

## The bake-off

One 8.2 second voice chunk (Gemini TTS), three start frames (woman 66 at a kitchen table, man 72 in a truck, Pixar-style grandmother), same prompt, scored by `tools/video/sync_gate.py` against the dry voice chunk. SyncNet confidence on real filmed speech is about 7 to 8. Offset is in frames at 25 fps; negative means the mouth leads the sound, which is how real speech looks.

| Engine (Kie model) | Face | Output | Offset | Confidence | Credits | Seconds to render |
|---|---|---|---|---|---|---|
| Wan 2.7 + driving audio (`wan/2-7-image-to-video`) | woman | 718x1280, 30 fps | -1 | 7.45 | 144 | 63 |
| Wan 2.7 + driving audio | man | 718x1280 | 0 | 8.46 | 144 | 63 |
| Wan 2.7 + driving audio | Pixar | 718x1280 | -3 | 7.59 | 144 | 62 |
| Kling AI Avatar Pro (`kling/ai-avatar-pro`) | woman | 1072x1920, 30 fps | -1 | 7.91 | 128 | 324 |
| Kling AI Avatar Pro | man | 1072x1920 | -1 | 8.57 | 128 | 323 |
| Kling AI Avatar Pro | Pixar | 1072x1920 | -2 | 7.52 | 128 | 344 |
| Kling AI Avatar Standard (`kling/ai-avatar-standard`) | woman | 720x1280 | -1 | 7.63 | 64 | 263 |
| OmniHuman 1.5 (`omnihuman-1-5`) | woman | 1088x1920, 25 fps | -2 | 7.37 | 216 | 345 |
| Veo 3.1 Lite, native voice (legacy `veo3_lite`) | woman | 720x1280, 24 fps | -1 | 8.17 | 30 | 77 |
| InfiniteTalk (`infinitalk/from-audio`) | all | failed: Kie returned internal error on every call that night | | | 0 | |
| Gemini Omni Flash 1.1, native voice, photoreal first frame | woman | blocked by Google safety review | | | 0 | |

What that means:

1. **Every engine that generates the mouth from the audio syncs at real-footage level.** Lip sync is solved by the architecture (the picture is made from the final audio), not by picking a magic model.
2. **Wan 2.7 with `driving_audio_url` is the default talking engine for anyone talking to the lens.** It is a full video model, not a talking-portrait model, so the person can hold props, shrug and gesture while the mouth follows the audio. In a side-by-side crop of the same moment it kept real skin (pores, lines, freckles) where Kling Avatar Pro smoothed the face. It renders in about a minute.
3. **Kling AI Avatar Pro is the fallback, and the first choice for drama singles.** It passed sync on every take all night (7 of 7), in true 1080p, with a softer face, and it takes five minutes. The gate switches a beat to it the first time Wan misses.
4. **OmniHuman 1.5 is not worth its price here.** Most expensive, softer, and it reframed the shot on its own.
5. **Veo 3.1 Lite with its own voice is the cheap draft route** (30 credits, 15 cents, for 8 seconds, said the line word for word, no subtitles). Its voice changes on every clip, so it is for a one-clip hook or a throwaway script test, never for a multi-clip ad.
6. **Stylized faces work** on both Wan and Kling. They come out with the mouth 2 to 3 frames early; the gate measures that and the assembler slides the clip, so it costs nothing.
7. **Google's safety review can block photoreal faces as a first frame** on Gemini Omni. Keep Omni for stylized work and for B-roll without a recognizable face.

## Engine names in plan.json

Talking beats (`talk_engine`, or `engine` on one beat):

| Name | Model | Notes | Price |
|---|---|---|---|
| `wan27-audio` | `wan/2-7-image-to-video` at 720p | the default | 16 credits/s ($0.08) |
| `wan27-audio-1080` | same at 1080p | do not use for talking: 3 of 3 takes ignored the audio (see below) | 24 credits/s |
| `kling-avatar-pro` | `kling/ai-avatar-pro` | automatic fallback, true 1080p, softer face | about 16 credits/s |
| `kling-avatar-std` | `kling/ai-avatar-standard` | 720p | about 8 credits/s |
| `omnihuman` | `omnihuman-1-5` | wide or full-body talking shots only | 27 credits/s |
| `infinitalk` | `infinitalk/from-audio` | 15 s cap, was down on test night | 12 credits/s at 720p |

**Wan 2.7 follows the audio when the face looks into the lens, and mostly does not when it looks away.** Counting every 720p take from build night: 8 of 9 to-camera takes (yapper, selfie, expert) passed the gate. Drama singles, where the person looks at someone just off camera in evening light, passed on 1 of 5 takes; Kling Avatar Pro passed on the same frames and audio (confidence 6.1 to 6.9). So: Wan for anyone talking to the lens, Kling Avatar Pro for scenes shot in singles. `validate` warns if a drama plan is set to Wan.

**Wan 2.7 only follows the audio at 720p.** On the demo build, three 1080p takes (two with an acting prompt, one with a neutral prompt, same frame and audio that pass at 720p) all scored confidence about 1: the mouth moved but not to the words. At 720p, 8 of 9 to-camera takes passed. The gate caught every one of these and repaired them without help. The 720p picture is scaled to 1080x1920 at assembly; in a 1:1 crop it still shows more real skin than Kling's native 1080p.

Wan bills whole seconds and tops out at 15, so a talking beat must be 14.3 seconds or less including padding. The voice step prints an error if one is longer.

B-roll (`broll_engine`, or `engine` on one shot). Audio is always thrown away:

| Name | Model | Notes | Price |
|---|---|---|---|
| `wan27-720` / `wan27` | `wan/2-7-image-to-video` at 720p / 1080p | 720p is the default; obeys a locked camera, 2 to 15 s | 16 / 24 credits/s |
| `veo-lite` / `veo-fast` | legacy Veo endpoint | 8 s clips, cheapest per clip | 30 / 60 credits per clip |
| `omni-flash` | `google/gemini-omni-flash-1-1` | best for stylized, may block photoreal faces | 63 to 126 credits per clip |

A shot marked `"still": true` costs nothing to animate: the assembler pushes in on the frame itself. Use it for photos the script shows (before and after, a class picture, a receipt).

Images: `gpt-image-2-text-to-image` for new frames and `gpt-image-2-image-to-image` for edits from a reference, 9:16 at 2K, 10 credits each. It held one woman's face across a kitchen, a table and two bathroom mirror selfies in the demo. `nano-banana-2` (12 credits at 2K, up to 14 references) is the alternate: set `"model": "nano-banana-2"` on a frame.

Voice in TTS mode: `google/gemini-3-8-flash-tts` (about 1 credit per 20 seconds). 70 voices, plain-English style direction per line, two voices per call. Ryan graded it "super fake"; the default is now the video model's own voice (next section). ElevenLabs on Kie (`elevenlabs/text-to-speech-multilingual-v2`) returned internal errors on every call on test night; the code path exists (`"provider": "elevenlabs"`) for when it is back. Word timings come from local whisper either way.

## Voice shootout (2026-10-05, after Ryan graded the TTS voice "super fake")

One line from the Akka script, one start frame, each video model speaking it with its own generated voice. Files in `tools/video/voicelab/r1/`. Judge = `voice_judge.py`, 1 to 10, two runs. Sync = SyncNet confidence against the clip's own audio.

| Engine (name in plan) | Said the exact line | Sync | Judge, untouched | Judge, after room seating | Credits for 8 s | Voice lock |
|---|---|---|---|---|---|---|
| Kling 3.0 std (`kling3`) | yes | 4.3 (review) | 10, 10 | not needed | 160 | per-character voice clip, untested here |
| Seedance 2 mini (`seedance2-mini`) | yes | 7.9 | 2, 2 | 10, 9 | 66 | reference audio, tested: 0.81 similarity on a new line, sync 10.3 |
| Seedance 2.5 at 480p (`seedance25`) | yes | 8.5 | not run | not run | 224 | reference audio |
| Wan 3.0 (`wan3`) | yes | 8.8 | 2, 2 | 2, 1 | 128 | reference audio |
| Veo 3.1 Lite / Fast (`veo-lite`, `veo-fast`) | yes | 5.3 / 6.7 | 2, 9 (Lite) | not run | 30 / 60 | none: new voice every clip |
| MiniMax H3 (`minimax-h3`) | yes | 6.6 | not run | not run | 64 | reference audio |
| Gemini 3.8 TTS, the old voice | n/a | n/a | 2 | 3, 2 | 1 | preset |
| Ryan's winners VID251, VID212 (the bar) | | | 10, 10 | | | |

**Ryan's ear (2026-10-05, blind): Seedance 2 mini seated with `native-kitchen` sounds real, on both lines. Kling 3.0 native does not, despite the judge's 10.** Default native engine: `seedance2-mini` with `fx: native-kitchen`: his pick, and also the cheapest, with exact words, strong sync and a proven voice lock. Do not use `kling3` for voice. The picked voice anchor is `tools/video/voices/picked/carol_66_midwest__seedance2mini.wav`.

Not on Kie, worth a key if Ryan wants them: ElevenLabs v4 with a designed voice, and ElevenLabs Voice Changer over a human read (the research's top-rated route, `tools/video/research/voice-realism.md`). ElevenLabs on Kie was still returning errors 18 hours in.

## Kie facts that bit during the build

- Uploads of 5 MB and up die with an empty response. `kie.py` converts big stills to JPEG before upload.
- `recordInfo` returns `creditsConsumed`; every call is logged with it in the project's `kie_log.jsonl`.
- Failed generations cost 0 credits (seen on ElevenLabs, InfiniteTalk and Omni).
- Result links expire (24 hours to be safe). The client downloads the moment a task succeeds.
- Rate limit is 20 new tasks per 10 seconds. The pipeline runs 6 at a time.
- 1 credit = $0.005.

## Rerunning the bake-off when a new model ships

`tools/video/bakeoff/run.py` is the runner: add a job line for the new model, run it, then score each clip with `tools/video/.venv/bin/python tools/video/sync_gate.py CLIP --audio tools/video/bakeoff/chunk.wav`. A new default has to beat Wan 2.7 on three things: confidence 7 or better on all three faces, skin that survives a 1:1 crop, and price per second.
