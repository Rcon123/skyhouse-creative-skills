# plan.json format

One file drives the whole build. Write it once from the script, then every step reads it. A working example is `offers/akka/videos/1955-coke-yapper-demo/plan.json`.

```json
{
  "title": "Akka 1955 yapper",
  "format": "yapper",
  "talk_engine": "wan27-audio",
  "broll_engine": "wan27",
  "style_contract": "one paragraph pasted onto every frame prompt",
  "voice": { ... },
  "captions": { ... },
  "hook_text": { ... },
  "music": { ... },
  "finish": { ... },
  "frames": { "<frame id>": { ... } },
  "beats": [ { ... } ]
}
```

## beats (the script, in order)

The script is split into beats. A beat is one to three sentences that share one picture plan. The spoken words of all beats, in order, are the whole voiceover. Nothing is spoken that is not in a beat, and no beat's words are ever changed by the pipeline.

**A talking beat** (the speaker is on camera, lip-synced):

```json
{"id": "b04", "visual": "talk", "speaker": "carol", "frame": "carol_master", "zoom": 1.0,
 "text": "My friend Joan has been a nurse for thirty years, and a few months ago she watched me order a salad...",
 "performance": "Talks like she is telling a friend a story, a small eye roll near the end.",
 "cutaways": [
   {"id": "c04a", "on": "Joan has been a nurse for thirty years", "frame": "joan_lunch",
    "motion": "The woman slowly shakes her head once, lips closed. Locked-off camera, single continuous shot, no cuts."}
 ]}
```

| Field | Meaning |
|---|---|
| `id` | unique, used for file names and `--only` |
| `text` | the exact spoken words. Spell numbers, years and prices as words. |
| `speaker` | key into `voice.speakers`. Optional when there is one speaker. |
| `style` | optional voice direction for this beat only (overrides the speaker's style) |
| `frame` | start frame id. Face frontal, mouth closed, nothing over the chin. |
| `zoom` | 1.0 or a punch-in such as 1.14. Applied at assembly, centered on the face the gate found. |
| `performance` | one sentence of acting direction. What she does, not what she looks like. |
| `engine` | optional override of `talk_engine` |
| `cutaways` | B-roll laid over part of this beat while the voice continues |
| `allow_jump` | true silences the same-frame-same-zoom warning |

Limits: 5 words minimum (shorter cannot be sync-scored), 40 words maximum, and the recorded beat must come in at 14.3 seconds or less. Aim for 8 to 30 words.

**A cutaway** covers the words in `on` (exact words from this beat's text, any length). It starts 0.08 s before the first word and ends 0.25 s after the last. `lead`, `tail` and `dur` override that. A cutaway with no `on` covers the head of the beat for `dur` seconds (default 2). Cutaways shorter than 0.6 s are dropped; a sliver of face under 0.5 s between two cutaways is given to the cutaway.

**A B-roll beat** (the voice continues, the speaker is not on camera):

```json
{"id": "b02", "visual": "broll",
 "text": "So this is me four months ago, and look at that belly hanging over my jeans...",
 "shots": [
   {"id": "s02", "frame": "before_photo", "still": true, "push": [1.0, 1.18], "focus": [0.5, 0.62]}
 ]}
```

Several shots split the beat. A shot with `on` starts at that phrase; shots without `on` share the remaining time evenly.

**Shot and cutaway fields:**

| Field | Meaning |
|---|---|
| `frame` | start frame id |
| `motion` | what moves, in one or two sentences, plus the camera. Never the word talk, speak or say. |
| `still` | true = no video render. The frame is shown with a slow push-in. For photos the script shows. |
| `push` | `[from, to]` zoom for a still, default `[1.0, 1.10]` |
| `focus` | `[x, y]` 0 to 1, where a still's push-in heads. Default `[0.5, 0.45]`. |
| `engine` | optional override of `broll_engine` |
| `zoom`, `start` | punch-in, and seconds to skip at the head of the clip |

## source footage (real clips inside a generated cut)

Added 2026-10-16 for the TPS VID636 kid-narrator test (keep an existing ad, replace one speaker). Any talk beat, shot or cutaway may carry a `source` block instead of a frame; the segment is cut from the footage into `clips/<id>.mp4` once (`source` step, also run by `native` and `clips`) and treated like any other clip after that.

```json
{"id": "b10", "visual": "talk", "speaker": "grandma",
 "source": {"file": "/abs/path/VID636.mp4", "t0": 24.05, "t1": 28.50, "keep_captions": true},
 "text": "Oh my God, stop. This is so embarrassing."}
```

| Field | Meaning |
|---|---|
| `file`, `t0`, `t1` | the footage and the segment, seconds. On a talk beat the segment's own audio is the line; cut it tight to that speaker's words (word times from whisper or a Scribe transcript) so no neighbour's word rides along. |
| `audio`, `audio_offset` | optional separate audio (a stem) replacing the footage audio; `audio_offset` is the footage time where that file starts. |
| `crop` | `[x, y, w, h]` fractions, applied before the 9:16 fit. Costs resolution; a 2x crop of 720p is visibly soft. |
| `keep_captions` | the footage has captions burned in and they match the words: ours are not drawn over that segment (`state.caption_skip`). |

- A speaker heard only in footage is declared `"real": true` under `voice.speakers`: no voice is cast, no anchor, no similarity check. Source beats are measured (words, sync) for the record and never rerolled; a word mismatch there means the cut points are wrong.
- Source beats may exceed 40 words: one beat per uninterrupted stretch, split only where the other speaker interjects. Trimming happens at the beat edges, so a split inside continuous speech can clip a word.
- Generated lines next to real audio: set `voice.fx` to `"none"` and give the generated speaker its own room and level, `speakers.<name>.fx` (a `voice_fx` preset, `native-offmic` for someone a few feet from a lav clipped on the other person) and `speakers.<name>.gain_db`. Measure the footage first (`voice_profile.py` on a stretch of each speaker) and match rolloff and noise floor, not taste.
- A silent listener under a real line is an ordinary cutaway (`on` = the whole line) from a generated frame with lips closed: two faces never talk in one shot, and the listener's reaction is the coverage.
- Footage with burned captions is only usable under its own words. Under new words the old captions show; use a generated shot instead.

## frames

```json
"frames": {
  "carol_master": {"prompt": "A 66 year old American woman, a retired teacher: ... lips closed ..."},
  "carol_table":  {"refs": ["carol_master"], "prompt": "Image 1 is the reference. The same woman from Image 1 ... Change only ..."},
  "after_photo":  {"refs": ["before_photo", "carol_master"], "prompt": "Image 1 is a bathroom mirror selfie. Recreate the exact same photo ... Change only ..."}
}
```

- No `refs` = a new image from text. With `refs` = an edit: refs are other frame ids or file paths (a real product photo, a reference still), and they are Image 1, Image 2 in the order listed.
- Frames render in dependency order, so an edit never starts before its source exists.
- `style_contract` is appended to every prompt unless the frame sets `"no_style": true`.
- Optional: `"model": "nano-banana-2"`, `"resolution": "1K" | "2K" | "4K"` (default 2K).
- Every frame is 9:16. "No text, no captions, no logos, no watermark" is added automatically.

## voice

**Native (default): the video model speaks each line.**

```json
"voice": {
  "mode": "native",
  "engine": "seedance2-mini",
  "fx": "native-kitchen",
  "min_similarity": 0.5,
  "speakers": {
    "carol": {
      "frame": "carol_selfie",
      "anchor": "voice/anchor_carol.wav",
      "anchor_beat": "b05",
      "voice": "A woman of 66 with a Midwestern American accent, recording a selfie video for her friends at home. A lived-in, slightly husky mid-low voice ... She sounds like a person talking, not a person reading. One take."
    }
  }
}
```

| Field | Meaning |
|---|---|
| `engine` | `seedance2-mini` (default), `seedance2-fast`, `seedance2`, `seedance25`, `wan3`, `minimax-h3`, `kling3`, `veo-lite`, `veo-fast`. A beat can override with `voice_engine`. |
| `fx` | room seating for the finished voice: `native-kitchen` (default), `native-room`, `light`, `none` |
| `speakers.<name>.voice` | the VOICE paragraph (see craft-rules section 2) |
| `speakers.<name>.frame` | the face to generate from when the line plays over B-roll |
| `speakers.<name>.anchor` | a voice clip Ryan already picked (2 to 13 s wav). If absent, the step casts one on `anchor_beat` (default: the longest talking beat up to 26 words) and saves it as `voice/anchor_<name>.wav`. |
| `min_similarity` | voice-match floor for a line to be kept |
| `second_ear` | `true` runs a Gemini verbatim transcript (repeats kept) on every take and on every line of the finished track in `check`. Whisper cannot hear a doubled word ("put put"); Gemini can. On for any strict word-exact build. |
| `respell` | `{"jowls": "jaowls"}`: swaps the spelling in the generation prompt only. Script, captions and audits keep the real word. The fix for a word Seedance 2 mini mispronounces; `pronounce` hints in the prompt did nothing there. Per beat too (`beats[].respell`). |
| `phoneme_gate` | `{"jowls": ["aʊ"]}`: fails any take whose word window lacks that phoneme (`phonemes.py`, wav2vec2 espeak). Transcribers write the right word for a mispronounced one; this hears it. Budget about 4 takes per gated word. |
| `aliases` | `{"Fosamax": ["phosmank", "fosomax"], "Prolia": ["proia"]}`: transcriber spellings that count as the script word in every word check (whisper, strict audit, second ear). Whisper cannot spell drug and brand names, so a line with "Fosamax" fails the letter-exact match forever without this. A heard token also maps when it is at least 60% similar to a listed script word. Added 2026-10-16 (OsteoShield yapper test). |
| `tempo` | voice-only formats only (speaker never shown): pitch-preserving speed-up of the finished track, 1.10 to 1.15. Refuses to run when any beat shows the speaker talking. |
| `min_wps` | do not set on Seedance: a pace floor made reads slower (the model fills a longer clip). Use `takes` instead. |

`pronounce` (plan or beat level) adds a pronunciation hint to the prompt; it worked nowhere yet. Prefer `respell`.

Run order: `validate`, `frames`, `native`, `takes`, `clips`, `gate`, `assemble`, `check`. `takes` promotes the best take per beat across all rerolls: exact words (whisper plus second ear), not cut off, then the fastest read. Run it after any `native --only` reroll, then `native` once more with no `--only` to rebuild the voice track. A beat may set `lead_in` / `tail_out` (seconds kept before the first word and after the last, defaults 0.10 and 0.18) to tighten or loosen the pace between lines.

**TTS: one voiceover drives every shot** (use when Ryan asks for it or supplies a recorded read).

```json
"voice": {
  "mode": "tts", "provider": "gemini", "model": "google/gemini-3-8-flash-tts", "fx": "kitchen-phone", "tempo": 1.0,
  "speakers": {"carol": {"voice_name": "Sulafat", "style": "A 66 year old Midwestern woman venting to her friends ... on a roll, barely pausing ..."}}
}
```

- Run order: `validate`, `voice`, `frames`, `clips`, `gate`, `assemble`, `check`. `talk_engine` picks the audio-driven picture engine (see models.md).
- To use a recorded read: save it as `voice/master.wav` before the `voice` step is ever run and run `voice` (it will find the file, align the words and cut the chunks without generating anything).
- Two speakers fit in one call. More than two are split into runs automatically.
- Inline tags work inside `text` on Gemini 3.8: `<sigh>`, `<laugh>`, `<short pause>`, `<breath>` and more. Tags are not spoken and are not captioned.
- ElevenLabs alternative: `"provider": "elevenlabs"`, speakers take `voice_id`. Down on Kie as of 2026-10-05.
- All 68 Gemini voices on one page, with pitch and pace measured: `tools/video/voices/index.html`.

## captions, hook_text, music, finish

```json
"captions": {"enabled": true, "size": 88, "y": 1150, "max_words": 3, "max_chars": 16,
             "upper": true, "highlight": "#FFE600", "replace": {"twenty twenty six": "2026"}},
"hook_text": {"text": "Nurse of 30 years told me to stop eating salads", "start": 0, "end": 5, "y": 300, "size": 62},
"music": {"file": "music/bed.mp3", "db": -24},
"finish": {"grain": 4, "room_tone_db": -52}
```

- Captions use the script's own words with whisper's timing, so they are word-perfect. `replace` changes how a spoken phrase is displayed.
- Keep `y` at 1248 or less: the bottom 35% of a Reels or Stories ad sits under the app's buttons.
- `hook_text` is a white box with black text at the top of the frame. Use it only when the script calls for an on-screen hook.
- Music is optional. It is ducked under the voice automatically. With no music the mix is voice plus quiet room tone.
- The final is normalized to -14 LUFS.

## Files a project ends up with

```
plan.json            the plan
state.json           word timings, beat cut points, clip and gate status, the cut list
kie_log.jsonl        every paid call: model, input, credits, seconds
voice/master.wav     the one voice track        voice/chunks/<beat>.wav   what drove each talking shot
frames/<id>.png      start frames               clips/<id>.mp4            raw renders (old takes kept as .prevNNN.mp4)
qa/frames_sheet.jpg  look before paying for video
qa/clips_sheet.jpg   six frames per clip        qa/<beat>.gate.json       lip-sync score per talking clip
qa/final_filmstrip.jpg, qa/final_report.json    the finished file, checked
final.mp4            1080x1920, 30 fps, H.264, AAC, captions burned in
```
