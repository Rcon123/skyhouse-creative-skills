# QA: the gates, how to read them, what to do on a miss

The rule from the best published video-agent work: verify pixels and decibels, not intentions. A step is not done because the command exited. It is done when the sheet has been looked at and the numbers are in range. A check that was skipped is reported as skipped, never as a pass.

## Gate 1. Frames (before any video spend)

Open `qa/frames_sheet.jpg`. For each frame:

| Check | Fail looks like | Fix |
|---|---|---|
| Identity | a different woman from the master | redo that frame (`frames --only <id>`); if the master is wrong, redo the master and everything built on it |
| Mouth | open, teeth showing, or covered by a hand, mug, bottle, hair | re-edit: "lips closed", move the prop "well below her chin" |
| Framing | face tiny, profile, cut off at the forehead, face in the bottom half | re-edit with "head and shoulders, face in the upper half, front view" |
| Hands | six fingers, melted grip | re-edit: "all five fingers visible and relaxed", or hide the hand |
| Text | any lettering, logo, watermark | re-edit: "plain, no readable labels and no logos" |
| Look | glossy, blurred background, studio light on a UGC ad | restate the phone-photo style contract |
| Match | photo pairs that are different rooms, B-roll rooms that do not belong | make the second by editing the first |
| Caption zone | the key thing sits at y 1040 to 1260 where captions go | reframe higher |

Redo only the bad frames: `frames <project> --only id1,id2`. Two tries per frame, then change the prompt's approach rather than rolling the same words a third time.

## Gate 2. Lip sync on every talking clip (automatic)

`gate` runs `tools/video/sync_gate.py` on each talking clip against the dry audio chunk that drove it. Three stages:

0. **Container.** A clip shorter than its audio has cut the end of the line. Fail.
1. **Mouth signal** (MediaPipe face landmarks). Mouth still through a second of speech = fail (a frozen face). Mouth working through a second of silence = review. Face found in under 60% of frames = `NO_FACE`.
2. **SyncNet** (the standard research scorer, running locally on CPU, about 6 seconds a clip). Returns the audio-video offset in frames at 25 fps and a confidence.

Reading the numbers (calibrated on this workspace's own bake-off):

| Confidence | Meaning |
|---|---|
| 7 to 9 | real-footage level. Every good clip in the bake-off landed here. |
| 5 to 7 | pass |
| 3 to 5 | REVIEW: look at the sheet, usually a small or turned face |
| under 3 | FAIL: the mouth is not following the audio |

| Offset | Meaning |
|---|---|
| -3 to +1 | in sync. Negative = mouth leads the sound, which is how real speech looks. |
| outside that, confidence 5+, within 7 frames | `PASS_SHIFT`: a clean constant offset. The assembler slides the clip by the measured frames. No reroll, no cost. Stylized faces usually land here. |
| anything else | FAIL |

Verdicts: `PASS`, `PASS_SHIFT` and `REVIEW` go forward. `FAIL` rerolls automatically: once on the same engine with a new seed, then on the fallback engine, then it stops and reports. `NO_FACE` is never a pass: it means the scorer could not see a face (stylized object, mask, profile, face too small). Judge those clips by eye on the sheet and say so in the report.

SyncNet confidence is not a beauty score. It catches offsets and dead mouths. It does not rank two good takes, and it cannot see a melted hand. That is what gate 3 is for.

## Gate 2b. Native voice clips (automatic, inside the `native` step)

Each generated line is checked three ways before it is kept:

| Check | Tool | Pass | On a miss |
|---|---|---|---|
| Said the exact words | whisper on the clip, matched to the script | 90% or more of the script words, no extra words | reroll; if the line ran to the end of the clip, the reroll gets two more seconds |
| Same voice as the anchor | `voice_match.py` (ECAPA speaker embedding) | similarity 0.5 or more (same voice measured 0.81, other voices 0.09 to 0.48) | reroll |
| Mouth follows | `sync_gate.py` against the clip's own audio | as gate 2 | reroll |

Two rerolls, then the id is listed under NEEDS WORK with its last take kept. The numbers for every line are in `state.json` under `native`.

**The voice itself** is scored by `voice_judge.py` in the `check` step (three stretches of the finished track, 1 to 10). It agreed with Ryan on the voice he rejected (2) and scored his real winners 10. It is wrong sometimes (one real studio interview scored 2). A score under 6 on the finished track is a reason to recast before sending; a score of 9 is not proof. Ryan's ear is the gate.

## Gate 3. Clips by eye

Open `qa/clips_sheet.jpg` (six frames per clip, rows in id order). For each row:

| Check | Fail looks like | Fix |
|---|---|---|
| Identity holds across the six frames | face drifts, ages, changes hair | reroll; if it repeats, the start frame is the problem |
| Hands and props | bottle melts, extra fingers, object appears or vanishes | reroll with a simpler action, or change the start frame so the hand does less |
| The action happened | B-roll frozen, or the stated end state never arrives | rewrite the motion prompt as one concrete event, reroll |
| Burned-in text | subtitles, gibberish captions, a watermark | reroll with the prompt changed (never the same prompt); or crop with `zoom` if it is at an edge |
| Unrequested cuts or zooms | the framing jumps between frames 3 and 4 | add "single continuous shot, no cuts, no zoom", reroll |
| B-roll mouths | a person in B-roll visibly talking | add "lips closed", remove any speech word from the prompt, reroll |
| Skin | plastic, smoothed, glowing | switch that beat's engine (`--engine`), or accept on a stylized format |

Reroll one clip: `clips <project> --only b05` (add `--engine kling-avatar-pro` to switch engine), then `gate <project> --only b05`. Old takes are kept as `clips/<id>.prevNNN.mp4`. Cap: two rerolls per clip, changing one thing each time, then cover the problem with a cutaway or cut the beat differently. Log what fixed it in `lessons.md`.

## Gate 4. The finished file

`check` runs on `final.mp4` itself:

- **Sync on the export.** Every talking stretch of 2.2 seconds or more is cut out of the final and rescored against the master voice. This catches assembly mistakes (a wrong in-point, a frame-rate slip), which is where good clips usually get broken.
- **Transcript.** Whisper hears the export and the words are compared with the script. Under 95% means audio was cut or doubled.
- **Loudness.** Should read about -14 LUFS.
- **Filmstrip.** `qa/final_filmstrip.jpg` has one frame per segment in order, labelled with its time and source. Read it against the script: does each picture show what the words say at that moment, do captions sit clear of faces and inside the safe zone, is any shot repeated.
- **Cost.** Credits and dollars for the whole project from `kie_log.jsonl`.

`qa/final_report.json` holds all of it. The report to Ryan quotes these numbers; it does not say "looks good".

## When something outside the gates goes wrong

- **A Kie model returns "internal error" on every call:** that model is down. Switch engine (`--engine`), note it, move on. Failed calls cost nothing.
- **"blocked by safety review":** Google models reject some photoreal faces and some health wording. Switch that shot to a Wan engine.
- **A run dies while waiting:** rerun the same step. Task ids are saved in `state.json` the moment Kie accepts a job, and the rerun picks the same tasks up instead of paying again. Do not kill a `clips` run because it looks quiet: Wan takes about a minute a clip, Kling Avatar five.
- **Whisper heard under 90% of the script:** listen for a skipped line before spending on video. Usually a number written in digits or a made-up product name.
- **Upload fails with an empty response:** the file is 5 MB or more. The client converts big stills to JPEG on its own; for audio, send WAV chunks (they are under 2 MB).

## The gate's own test

`sync_gate.py` was checked three ways before it was trusted: it reproduces the published reference numbers for SyncNet's own sample clip (offset 3, confidence 9.9 to 10.0); shifting that clip's audio by three frames moves the reported offset by exactly three; and a real talking clip from each engine scores in the range the research literature reports for real footage. Rerun those if torch or mediapipe is ever upgraded (`mediapipe==0.10.21` is pinned on purpose: 1.0.1 crashes on this Mac).
