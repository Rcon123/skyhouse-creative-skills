# How AI-UGC makers get the voice to sound like a real person on a phone
Research run 2026-11-04. 23 sources read in full (listed per section). Most are tool-vendor or agency blogs, not creator posts. X posts would not open (402 paywall), so no X thread is quoted. Anything not confirmed by a source read in full is marked **unverified**.

## One-screen summary (the stack most people use, in order)

1. **Script for the mouth first.** Short lines, 2.5 to 3 words per second for talking-head UGC (Spark UGC, 2026-10-31). Kling: no more than about 15 words per 5 s shot or the audio model "squeezes" the speech and it sounds robotic (VIDEOAI.ME).
2. **Voice: ElevenLabs is still the default, and v4 is now the realism leader.** Eleven v4 launched 2026-09-28, $0.08 per 1K chars on fal. It sits #1 on the Artificial Analysis blind TTS arena (ELO 1334, checked 2026-11-03), ahead of Qwen-Audio 3.1, Cartesia Sonic 3.6, Gemini 3.8 Flash TTS and Fish Drama 3. MiniMax Speech 2.8 and OpenAI TTS are not in the top 20. Hume: no ranking found.
3. **Two ways to get picture plus voice:**
   - **A. Video model talks natively, then you swap the voice.** Seedance 2.5 (or Kling 3.0, Omni Flash) does the mouth. You export its audio as a scratch track and run it through ElevenLabs speech-to-speech (Voice Changer), then lay it back on. The lips hold because they follow rhythm, not timbre (Mirrorize, 2026-07-20; seedance.tv, 2026-09-20).
   - **B. Audio first, then drive the face.** Make the final voice, then animate a still with Kling Avatar v2 Pro, OmniHuman 1.5/2.0, HeyGen Avatar IV or InfiniteTalk. Or re-mouth existing footage with Sync 3 / lipsync-2-pro / LatentSync.
4. **Reference audio on video models does not keep your file.** Seedance 2.5 lip-syncs to reference audio but re-renders it. Its output is a new recording with an added ambience bed, re-timed, pitch about 5% up, in 32 kHz AAC (openstory issue #1551, 2026-09-11; Segmind, 2026-08-08). That is the likely source of the dulled, slightly band-limited sound. **The fix people use: mux the original voice file back over the picture** and treat the model's audio as a scratch track.
5. **Post: light touch.** Tighten pauses to about 0.35 s but keep room tone under the cuts. Room-tone bed around -50 to -60 dB so gaps are never digital silence. Add a breath before opening lines. Normalize last to -14 LUFS / -1 dBTP (Turntake, 2026-10-10). Heavy EQ, compression or noise removal makes it sound MORE fake. ElevenLabs "remove background noise" strips breaths and leaves "metallic tails" (seedance.tv).
6. **Phone look:** prompt "clear phone-mic voice with light room tone, no background music" (Atlas Cloud, crediting creator @beechinour, 2026-08-12). Never put "phone" or "reverb" in an ElevenLabs Voice Design prompt; ElevenLabs says those words hurt quality. Do the phone color in post. No source gives a tested iPhone EQ curve (**unverified**).

---

## Q1. Which voice tools, and what sounds real vs AI

**Blind-test ranking (Artificial Analysis TTS arena, via Teamday, updated 2026-11-03)**
https://www.teamday.ai/blog/best-ai-voice-models-2026

| Rank | Model | ELO | Price |
|---|---|---|---|
| 1 | ElevenLabs Eleven v4 | 1334 | $0.08 / 1K chars |
| 2 | Eleven v4 Turbo | 1331 | $0.04 / 1K chars |
| 3 | Alibaba Qwen-Audio-3.1-TTS-Plus | 1301 | ~$19.30 / 1M chars |
| 4 | Cartesia Sonic 3.6 | 1293 | plans from $5/mo |
| 5 | Google Gemini 3.8 Flash TTS | 1282 | $0.50 in / $9 out per 1M tokens |
| 6 | Fish Audio Drama 3 | 1272 | open weights; ~$15 / 1M chars API |
| 18 | ElevenLabs v3 Conversational | 1212 | $0.04 / 1K chars |
| not top 20 | MiniMax Speech 2.8 HD / Turbo | n/a | $100 / $60 per 1M chars |
| not top 20 | OpenAI tts-1, tts-1-hd, gpt-4o-mini-tts | n/a | $15 / $30 per 1M chars; per token |

- Quote (Teamday): "In September we wrote that ElevenLabs no longer won blind votes; v4 reverses that." Also: the arena "measures short clips, not your brand voice."
- Hume Octave, Resemble, OpenAI gpt-realtime: no UGC-maker usage or ranking found. **Unverified** for UGC.

**Eleven v4 (Novoads, Mauricio Valdivia, 2026-09-29)**
https://novoads.ai/en/blog/eleven-v4
- Launched 2026-09-28 with v4 Turbo. ElevenLabs calls it "our most emotive text-to-speech model yet." It claims about 75% of listeners preferred v4 in blind tests (ElevenLabs' own figure).
- About 4 cents per 30 s take on v4. Instant clones from 10 s of audio. **Clones made before v4 need retraining.**
- SSML break tags are off; pauses are written as `[pause]`.

**What creators use in practice**
- **ElevenLabs as the voice layer** shows up in nearly every UGC pipeline read: n8n GPT-4o + ElevenLabs + WaveSpeed template, Segmind Kling 3.0 + ElevenLabs template, Mirrorize, seedance.tv, Atlas Cloud. MakeUGC reportedly uses ElevenLabs natively; Arcads' engine is disputed. Both are **unverified** (secondhand comparison sites).
- **Video-model native voices** (Nikhil Sharma, DTC paid social, updated 2026-10-17, https://nikhil.pro/ai-ugc-ads-seedance-veo-chatgpt/): his pipeline uses no TTS at all. Seedance 2.5, Veo 3.1 and Kling make "synchronized dialogue and ambient sound in the same pass." He reruns Kling for Spanish. Prices: Seedance 2.5 ~$0.10/s at 480p and ~$0.23/s at 720p (BytePlus ModelArk); Veo 3.1 Fast $0.15/s, Standard $0.40/s; Kling 3.0 Pro ~$0.10 to 0.14/s.
- **Native voice weaknesses:**
  - Seedance 2.5 "infers a voice for the character" and gave an unprompted British accent. "American" fixed it; "American English" did not. "Voice consistency remains unpredictable." (MindStudio, 2026-08-06, https://www.mindstudio.ai/blog/seedance-2-5-review-guide)
  - Gemini Omni Flash: "the lips faithfully follow the broken audio"; about 15% of takes stutter; you can't supply a voice (Maxfusion, Ori Silver, July 2026, https://maxfusion.ai/blog/ai-video-models-lip-sync-2026).
  - Kling 3.0 dialogue goes "robotic, compressed, or out of sync" when the line is too long for the shot (VIDEOAI.ME, Paul Grisel, 2026-04-12, https://videoai.me/blog/kling-ai-troubleshooting).

**What reads as AI (ScreenWeaver, Frank Houbre, 2026-08-24)**
https://www.screenweaver.ai/blog/ai-voices-lip-sync-film
- Five tells: flat emphasis, no breaths, no room acoustics, dialogue at a constant level, sync close but not locked. "Silence between lines is the loudest tell there is."
- Their fix is to make 4 to 8 takes per important line and splice the best parts.

**ElevenLabs tag behavior (Superscale, Emily Schubert, 2025-09-02, older)**
https://superscale.ai/learn/sound-effects-emotions/
- Action tags work. Their examples are [Whispering] and [Strong British accent]. Emotion adjectives ([Sad], [Friendly]) are "underperforming." CAPS for emphasis "works very well."

## Q2. Audio-first workflow and lip-sync / avatar tools

**Two live patterns**
1. **Video first, voice swap after** (Mirrorize "Master Lip Sync: Seedance 2.0 + ElevenLabs", Higginswerx, 2026-07-20, https://mirrorize.ai/learn/the-best-lipsync-workflow-right-now-seedance-2-0-elevenlabs).
   - Prompt "dialogue only, no music, no background sound." Direct pace, breath and emphasis, because they drive mouth shapes.
   - Export the Seedance audio and run it through ElevenLabs speech-to-speech, then put it back. Quote: "as long as the new voice track follows the same rhythm, the lipsync holds."
   - Treat the Seedance voice as a scratch track.
2. **Audio first** (diyai HeyGen + ElevenLabs guide). Approve the script, make the final ElevenLabs narration, then upload it to the avatar tool. They call audio-first "the safer order."

**Tool ratings (none independent; all vendor-adjacent)**
- **Maxfusion (Ori Silver, Jul/Nov 2026)**
  - "Cheap model, regenerate. Expensive model, repair." "If the mouth is wrong, the ad is dead."
  - Best fixer: Sync 3 (120 s cap, expensive). Workhorse fixers: Sync 2 Pro (needs visible speaking motion, struggles with still frames and hard angles) and VEED Lipsync.
  - Audio-driven: RIZZ is "the most realistic audio-driven model on the market right now" (**unverified**, single source). OmniHuman 1.5 degrades around 10 to 11 s.
  - Generators: Kling 3.0 Pro sync falls apart after about 8 s. Seedance 2.0 "corrupts words." Veo 3.1 mouth looks unnatural (8 s cap). Sora 2 Pro API shuts 2026-09-24.
- **Fuser (tests 2026-09-28, verified 2026-10-23)**, https://fuser.studio/articles/best-ai-lip-sync-tools
  - Audio fidelity: HeyGen Avatar IV returned the line exactly. LatentSync matched apart from encoding. MiniMax H3 mixed in extra workshop sound. Seedance 2.5 "produced a new recording."
  - Seedance 2.5 "refused our photoreal face."
  - HeyGen adds its own gestures and smiles and costs about 20x LatentSync per second.
  - LatentSync cut the last word (5.76 s output for a 6.3 s line). Padding the audio with silence fixed it.
  - MiniMax H3 reference audio must be 2 to 15 s.
- **each::labs (Eftal Yurtseven, 2026-10-22)**, https://www.eachlabs.ai/blog/best-ai-lip-sync-models-2026
  - "no single winner"; pick by footage.
  - OmniHuman 2.0 takes 4 to 300 s audio: "Give it an expressive voice, because the audio is the real prompt."
  - Kling Avatar v2 has Standard (iterate) and Pro (final) tiers, and the prompt is for "behaviour, not identity."
  - Sync lipsync-2-pro has `sync_mode` (cut_off, loop, bounce, silence, remap); Sync 3 drops it.
- **invideo (2026-08-06)**, https://invideo.io/blog/ai-lipsync-models/
  - Premium lip-sync about $0.05 to 0.07 per output second; volume tier roughly 10x cheaper.
  - Kling Lipsync caps source video at 2 to 10 s.
  - VEED Fabric: "emotion in the audio carries into the face."
- **Other secondhand claims:**
  - Kling Avatar is the most stable on long clips with no face drift, and ranks first on quality per dollar (ClipIA).
  - InfiniteTalk (MeiGen, open source) stays drift-free past a minute but renders slowly; v1.5 swapped Wav2Vec2 for Whisper-Large.
  - Hedra Character-3 is best for stylized characters and weaker on side profiles.
  - HeyGen Avatar IV/V costs 20 credits/min, about 7x standard.
  - All of the above is **unverified** beyond the listicles.
- **Volcengine video-to-video lip-sync:** no source found. **Unverified.**

**Gotchas collected**
- Close-up, low-motion shots hold the voice; wide action shots don't (Wireflow, Michael Aubry, 2026-08-25, https://www.wireflow.ai/blog/real-voice-seedance-2-5). The same close-up reference came back near-verbatim in 3 of 3 runs; a wide action shot with wind and engine came back recomposed in 0 of 3.
- Wireflow's generate-then-replace test with a clone plus "worldizing" was "comically bad." A reviewer said it sounded "like he's in a room recording with the motorcycle attached as a different source." Quote: "Layering is not blending."
- "An instant voice clone is not your voice." A professional clone needs 30+ minutes of clean speech (Wireflow).
- Mute video references (`ffmpeg -i ref.mp4 -an`) so old speech doesn't bleed in (Wireflow).
- Mouth shapes shrink when the face turns away (Fuser, LatentSync). Check B/P/M closures frame by frame; if you can't lock it, early sync beats late (ScreenWeaver).

## Q3. Reference audio mode: does it keep quality?

**Seedance 2.5: lip-syncs, but re-renders the voice.** openstory issue #1551 (Tom Beckenham, opened 2026-09-09, closed 2026-09-11): https://github.com/openstory-so/openstory/issues/1551
- Model `dreamina-seedance-2-5-260628` on BytePlus Ark.
- Reference audio IS used as the dialogue. Whisper transcripts came back verbatim, with phrase boundaries within 0.1 to 0.3 s of the reference. The mouth closed during a 1 s pause.
- Quote: the returned audio "is a re-render, not the supplied file."
  - It adds an ambience bed (about -51 dBFS in a pause where the reference sat at -85 dBFS).
  - Timing is re-timed non-uniformly.
  - Mean pitch (f0) is about 5% above the reference.
- `generate_audio` defaults to true whenever reference audio is present. `generate_audio: false` returns a silent MP4 where the character still moves its mouth. Muxing your file over it "might work" (**unverified**).
- `first_frame` cannot be combined with reference audio: "first/last frame content cannot be mixed with reference media content." Photoreal reference faces were rejected (`InputImageSensitiveContentDetected.PrivacyInformation`).

**Seedance 2.5 output audio spec:** "stereo AAC, 16 bit, at 32 kHz" (Segmind, Rohit Rao, 2026-08-08, https://blog.segmind.com/seedance-2-5-review-five-real-world-use-cases-and-exactly-what-each-one-costs/). Below the 48 kHz standard. "Dialogue holds for social and review work, but it is not a substitute for a proper dub."
- My read: a 32 kHz AAC re-render with an added noise bed matches the "dulled / phone-call" complaint. No source names the complaint in those words. **Unverified as cause.**

**Wireflow (2026-08-25):** audio references "guide tone, timbre, pacing... They do not preserve your recording."

**seedance.tv (Emma Chen, 2026-09-04)**, https://www.seedance.tv/blog/how-to-keep-voices-consistent-in-seedance-2-5
- Reference should be 8 to 15 s of natural speech, quiet room, steady mic distance, no music, no reverb.
- "Do not splice several takes merely to make the sample longer."
- "A voice can be the same person yet seem different because the next clip is louder, wetter, or noisier."

**Kling 3.0 voice binding**
- Official guide: voice from a recording of at least 3 s; FAQ says 5 to 30 s, single speaker, clean, moderate speed, neutral emotion.
- Video input plus native audio is "Not Supported Yet." 4K mode doesn't take voice inputs.
- The API field name `element_input_audio_urls` is not documented in anything found. **Unverified.**
- No creator complaint of muffled bound voices found. **Unverified.**

**The fix people use:** keep the model's audio as a scratch track and lay the clean voice back on.
- If the voice was made first, mux your file in: `ffmpeg -i clip.mp4 -i voice.wav -map 0:v -map 1:a -c:v copy -shortest out.mp4`. This is a general ffmpeg pattern; test it.
- If the model's voice came first, run it through ElevenLabs speech-to-speech.
- Align on the first clear consonant. "Do not time-stretch the entire take immediately." Split at breaths or closed-mouth frames (seedance.tv, 2026-09-20, https://www.seedance.tv/blog/elevenlabs-voice-changer-video-tutorial).

## Q4. Post-processing

- **Turntake (2026-10-10)**, https://turntake.app/learn/elevenlabs-ad-voiceover
  - Make 2 takes. Speech-to-text each against the script and keep the one with the fewest deviations.
  - Tighten pauses in the trim to about 0.35 s and keep room tone. "Raw silence removal clips soft consonants and leaves seams."
  - Normalize LAST to -14 LUFS, -1 dBTP. Music bed around -31.5 LUFS.
- **seedance.tv voice changer guide (2026-09-20):** after the swap, "restore the mix": room tone, breaths where they help, separate music and effects.
  - ElevenLabs "remove background noise" is no substitute for a clean source. Check it for missing breaths and "metallic tails."
  - Avoid repeated lossy exports; check the sample rate before aligning.
  - Check on phone speakers, because harsh consonants show up there.
- **Room tone level:** -50 to -60 dB bed under the voice (several AI-voice guides, low authority; test by ear).
- **EQ:** some guides cut 2 to 4 kHz harshness slightly. Others warn heavy EQ, compression or reverb makes synthetic voice sound more artificial. No UGC creator settings found. **Unverified.**
- **Adobe Podcast Enhance Speech:** fixes "muffled, reverberated... tinny" speech; the free tier is 30 min / 500 MB. It reconstructs audio with AI, so it can produce odd results and makes speech sound studio-clean, the opposite of phone UGC. No UGC maker found using it on AI voices. **Unverified.**
- **Auphonic, iZotope RX, Resemble Enhance:** no AI-UGC usage found. **Unverified.**

## Q5. Pace and getting it to talk fast with no gaps

- **Targets (Spark UGC, Chris Bristow, updated 2026-10-31)**, https://www.sparkugc.com/resources/ad-script-length-words-per-second
  - Natural read 2.5 w/s (150 wpm); energetic 3 w/s (180 wpm).
  - UGC feed ads: 2.5 is the floor and 3 is the target. Talking-head lines at 3; demo lines at 2.5.
  - Past 80 words in 30 s, "the pauses disappear." Keep the beat before the CTA: "That beat is where the viewer decides."
- **Other benchmarks:**
  - Commercial reads run 160 to 180 wpm (granary.digital).
  - seedance.tv prompts a pace of "about 135 words per minute."
  - Turntake measured Eleven v4 at about 100 words in 40 s (150 wpm) on number-heavy English.
- **ElevenLabs controls:**
  - Speed is 0.7 to 1.2 in the app; REST API 0.25 to 4.0 on v2/v3. **Speed is NOT supported on v4.** Style is not supported on v4. v4 uses only stability and similarity_boost (ElevenLabs skills repo, https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md).
  - On v3/v4 there are no SSML `<break>` tags. Use punctuation, line breaks, `[pause]` (ElevenLabs best practices, https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices). Ellipses ADD pauses, so cut them for a no-gap read.
  - Voice Design pacing words: "Speaking quickly", "at a fast pace", "fast-paced"; casual: "Relaxed and conversational pacing", "like he's talking to a friend" (https://elevenlabs.io/docs/eleven-creative/voices/voice-design).
  - Pacing follows the source voice: "use longer, continuous samples to avoid pacing issues" (best practices). Pick a fast-talking voice or clone rather than forcing speed.
- **On the video models:** fit the words to the shot. Kling: about 15 words per 5 s, 25 per 10 s, or under 12 per 5 s to avoid frozen lips (VIDEOAI.ME). Also add "unnatural voice, robotic speech, audio distortion" to the negative prompt.
- **Gaps are mostly cut in the edit, not the prompt.** Atlas Cloud says: "Cut the dead air at the top before the energy kicks in" and tighten every pause.
  - Hook starts "mid-sentence, as if we joined late"; CTA lands as "an afterthought"; keep "one pause mid-thought."
- Filler words ("um"): no source shows they raise realism. **Unverified.**

## Q6. Matching the voice to the iPhone look

- **Atlas Cloud / @beechinour (2026-08-12)**, https://www.atlascloud.ai/blog/tips/how-to-make-ai-ugc-ads
  - Seedance 2.5 audio prompt: "clear phone-mic voice with light room tone, no background music." Audio: "room tone, one ambient sound event. No music."
  - Visual: "ultra realistic iphone front camera selfie", "handheld front camera selfie perspective, chest-up framing, natural micro shakes, 9:16."
  - Quote: "Seedance renders a bad script as beautifully as a good one."
  - Prices quoted (promo ended early Sep 2026): Seedance 2.0 Mini about $0.039/s, Fast about $0.072/s.
- **ElevenLabs Voice Design docs:** "phone", "reverb", "echo", "tape" "can negatively affect output quality."
  - For a deliberately lo-fi sound they suggest "Sounds like a voicemail", "Low-fidelity audio." Those push toward a voicemail sound, not an iPhone selfie mic, so do it in post.
- **Wireflow (2026-08-25):** "Record lines first: phone, outdoors, energy up, three takes per line." Their best results came from a real phone recording used as the reference with close-ups, not from EQ'ing a studio voice into a scene.
- **Mic distance and room:** match room tone, mic distance, loudness and ambience between clips, or cuts give it away (seedance.tv 2026-09-04). Match reverb to the visible room (ScreenWeaver).
- **Breaths:** add before opening lines and after heavy ones (ScreenWeaver). ElevenLabs tags `[exhales]`, `[sighs]` exist (best practices).
- **Mouth clicks:** no source on adding them. **Unverified.**
- **Not found:** a tested EQ curve for "sounds like an iPhone front mic" (**unverified**). General knowledge, untested here: iPhone voice memos are close, slightly bright, with light room and no studio low end. Treat that as a hypothesis to A/B, not a finding.

## Sources read in full
Wireflow (Aubry, 2026-08-25) · openstory #1551 (2026-09-11) · seedance.tv voice consistency (2026-09-04) · seedance.tv voice changer (2026-09-20) · Maxfusion (Silver, Jul 2026) · Superscale (2025-09-02) · invideo lipsync (2026-08-06) · Novoads Eleven v4 (2026-09-29) · ElevenLabs TTS best practices · ElevenLabs Voice Design docs · ElevenLabs skills voice-settings.md · Atlas Cloud / @beechinour (2026-08-12) · Nikhil Sharma (upd. 2026-10-17) · ugcvids (2026-07-04) · Segmind Seedance 2.5 review (2026-08-08) · Teamday TTS arena (upd. 2026-11-03) · MindStudio Seedance 2.5 (2026-08-06) · ScreenWeaver (2026-08-24) · Spark UGC (upd. 2026-10-31) · each::labs (2026-10-22) · Mirrorize (2026-07-20) · Fuser (tested 2026-09-28) · Turntake (2026-10-10) · VIDEOAI.ME Kling troubleshooting (2026-04-12)
