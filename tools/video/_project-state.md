# tools/video state

**Last updated:** 2026-10-18 (TPS VID636 kid narrator shipped as a test: VID852, ClickUp 17th71z6ym2)

## Where it stands

- 2026-10-18: kid narrator shipped as v7 (`offers/tps/videos/grandma-kid-narrator/kid-v3/final_v7.mp4`, DB VID852, ClickUp 17th71z6ym2). Seven versions over two nights; Ryan's grades drove the pipeline additions below and three standing rules: never process a voice he picked raw, never put captions on a mouth (assembly guards it), never substitute the control's music on a twin. New tools: `edit_review.py`, `listen.py`, `enhance.py` (DeepFilterNet, torchaudio shim), `plan.bed` / `plan.sfx` / `music.duck`. Music on a twin remains the unsolved part without the editor's music file.

- 2026-10-16 evening, TPS VID636 kid narrator (`offers/tps/videos/grandma-kid-narrator/kid-v1/`): Ryan's test is to keep a shipped ad and swap one speaker. New in the pipeline: `source` on beats/shots cuts real footage into clips (`source` step, run by `native` and `clips`), `"real": true` speakers are never cast, `keep_captions` skips our captions over footage that has its own, per-speaker `fx` and `gain_db` seat a generated voice next to real audio (`native-offmic` preset from measuring Emma off-mic), and `takes` now checks voice similarity and the sync gate per take (it had promoted a wrong-voice take). Kid voice cast by blind reel (`voicelab/kid_r1/`), Ryan picked C; anchor in `voices/picked/kid_7yo_girl__seedance2mini_C.wav`. Child frames and lines rendered with no policy block. Short lines (under 8 words) read slow on Seedance's 4 s minimum clip; budget 3 to 4 takes each. Editors' Dropbox project folders (Evgenii's VID636 reframe) held clean before photos, per-line audio and a Scribe transcript: search there before designing frames for any existing ad.
  Later the same night, after Ryan graded v1 and v2 down: assembly punches in automatically when a face would sit under the caption band (every kid line had failed export sync for that reason); `voice.strict_sync` makes REVIEW a reroll for on-screen lines; `plan.sfx` places one-shot sounds on cut points (the original's whooshes on photo transitions); `music.duck`/`music.offset`; `tools/video/edit_review.py` is the editor's pass (floor continuity per segment, motion spikes per generated clip, shot map) and SKILL.md 6b makes it mandatory before a hand-off. Demucs is installed in the venv (`python -m demucs`); on VID636 it showed there was no music bed, only whooshes and room floor. Rule from Ryan tonight: good shape, not perfect, mind the money.

- 2026-10-15: first graded full build. TPS Two Wrinkles (voice-only demo on a glossy bust): v1 "really great start" with three tweaks; v2 delivered (faster read via best-take selection + tempo 1.15, jowl-grab open, top-five wording). Hook variants H2 to H6 build from the shared clips. Same day, Ryan's last note (every word said right, no word said twice): whisper could not hear doubled words ("face face", "put put"), Gemini verbatim could, every run. Added `voice.second_ear` (Gemini repeat check on every take and on every line of the finished track in `check`), measured speech start/end for the master cut (whisper's last-word time was clipping "Gone" and "apart"), a tail-noise fault, compound and contraction spellings in the audit, and the no-repeat line in the native prompt. All six versions rebuilt from exact-word takes (b05 took 16 takes, b11 13). 10-16 round 3 from Ryan's notes: head cut at the neck on a black base (the chest had read as a standing woman), every transform shot rubs before it changes, and "jowls" fixed with `voice.respell` + `voice.phoneme_gate` (`phonemes.py`, wav2vec2 espeak) because whisper and Gemini cannot hear a mispronounced word. Six finals rebuilt and sent, v2 at $35.91 all in; Ryan: "Awesome". Shipped 10-16: DB VID828 (v1) + VID829-834 (round 3), ClickUp 17th71z6w23, Google Doc 1AZJkjGCI6MoMGOSt8o4wqv-7jyEbgXYYV4QjhXJKKm4 (2 HL + 2 AT + script). Scratch test project `offers/tps/videos/face-build/_jowl-test/`. Projects in `offers/tps/videos/face-build/two-wrinkles-v2*`. New steps: `takes` (best take across rerolls), `voice.tempo` (voice-only formats), `pronounce` hints, number-aware word check, Suno music via `ai-music-api/generate`.

- Ryan graded the first two tests 5 of 10 on 2026-10-05: "voices horrible, super fake", "not even real Coke bottles", wants 10 of 10.
- Round 2 rebuilt the voice layer. Default is now native voice (the video model speaks, one voice locked by reference audio), room seating, and three machine checks per line (words, voice match, sync) plus a Gemini listening judge.
- Proven so far: two native lines end to end in `voicelab/native_mech_test/final.mp4` (words 100%, voice match 0.81, sync pass, judge 10). NOT yet run: a full-length native build. Kie balance is about 130 credits; the full Akka v2 plan estimates 2,700 to 3,500.
- Waiting on Ryan's ear: blind reels `voicelab/r1/voice_shootout_r1.mp4` (A to J) and `voicelab/r1/voice_shootout_r1b.mp4` (his winner VID251, then the lead candidate on two lines, then Kling).
- Ready to run on top-up: `offers/akka/videos/1955-coke-yapper-v2/` (full 554-word script, Ryan's picked Carol images, real Coke bottles from IMG92, native voice). The candidate voice anchor sits at `voice/anchor_carol.candidate.wav`; rename it to `anchor_carol.wav` if he picks that voice, or cast a new one.

## Decisions (and why)

- Native voice over TTS. Reason: Ryan's grade, the listening judge (TTS 2 to 3, native 9 to 10 once seated), and what his X follows do.
- Default native engine Seedance 2 mini + `native-kitchen` room chain. Reason: cheapest, exact words, sync 7.9 to 10.3, voice lock measured at 0.81. Kling 3.0 is the alternate (best untouched voice, 2.4x price).
- Voice casting is Ryan's call, by blind reel. A picked anchor is reused per character.
- Search the offer for PICKED images and their NOTES.md before designing frames. Real branded objects from real reference photos.
- Still true from round 1: Wan 2.7 + driving audio at 720p for TTS-mode talking shots, Kling Avatar Pro fallback and first choice for drama singles; dialogue in singles.

## Open, in order of value

1. Ryan's pick from the two reels (or "none": then cast again with new voice paragraphs, Kling voice lock, or an ElevenLabs key).
2. Top up Kie, then run Akka v2 end to end: the first full-length native build. Expect to learn about voice drift over 22 lines and room-tone seams between clips.
3. Kling 3.0 voice lock test (element + voice clip), about 160 credits.
4. If he wants the very top voice route: ElevenLabs direct key (v4 designed voice, or Voice Changer over a human read). Not on Kie.
5. Native voice for drama: two anchors, singles, off-axis faces. Untested.
6. 1080p, music bed, Pixar full ad, talking objects: unchanged from round 1.
