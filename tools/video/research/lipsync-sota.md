# Lip sync state of the art for one-shot AI video ads

Research date: 2026-10-04. Scope: talking-character direct-response ads, vertical, 30s to 3min, generated on Kie.ai, assembled locally with ffmpeg and Python.

How to read this file:

- **VERIFIED** = a source says it and the page was fetched in this session (by me or by a research sub-agent I briefed). The URL follows the claim.
- **VENDOR** = the source sells one of the things being compared. Treat as a lead, not a verdict.
- **READ** = my own inference. No source says it directly.
- Reddit blocked direct fetch. Reddit threads below were read through an archive (PullPush) by a sub-agent, so treat them as secondhand.
- Kie facts come from Kie's own docs index (https://docs.kie.ai/llms.txt), the per-model doc pages, and the model landing pages, all pulled today.

---

## 0. Bottom line

**The hypothesis is half right. Here is the corrected version.**

Lip sync does not fail because audio and video were made separately. It fails when the mouth pixels were not generated from the exact final audio. Three setups meet that test and all three can sync:

1. Audio-driven avatar models (image + audio in). Audio is made first, separately, and it works.
2. Native joint generation (Veo, Kling, Seedance, Gemini Omni).
3. Post-hoc re-render of the mouth (Sync, Volcengine). This is literally marrying after, and pros use it daily to repair expensive footage. (VENDOR: https://maxfusion.ai/blog/ai-video-models-lip-sync-2026)

What actually reads as bad lip sync, in rough order of how often it shows up in sources:

1. Silent image-to-video with a moving mouth, voiceover laid on top. Never synced to begin with.
2. Drift or decay inside a long clip (Kling 3.0 past about 8s, OmniHuman 1.5 past about 10s, InfiniteTalk color shift past 1 min).
3. Mouth realism: rubbery lips, teeth flicker, lips not closing on p, b, m. Timing is right but it still reads fake.
4. Dirty driving audio: music bed, reverb, compression.
5. Face too small, turned, or covered.
6. Assembly damage: frame-rate conforms, `-shortest`, clips returned at the wrong length, per-clip audio used instead of the master.
7. Native-audio word corruption, stutter, wrong speaker, invented subtitles.
8. B-roll characters mouthing while the voiceover runs.

**Which architecture wins for this skill: audio-first.** (READ, reasons in section 8.) One ElevenLabs voice track is the master clock. Each talking shot is driven from its own sentence-bounded chunk. B-roll and captions are timed off word timestamps that exist before any video is rendered. Every clip can be scored against known audio and rerolled alone.

**Native audio is still the better tool for one job:** a short realistic UGC hook (one 6 to 8 second line) where whole-body realism matters more than voice identity. People buying media at volume lean native plus a repair layer for realistic UGC. (VENDOR: maxfusion link above; https://ugcvids.ai/blog/kling-3-vs-veo-3-1-for-ugc-ads)

**A third option now exists on Kie and should be tested:** general video models that take a driving audio file. Wan 2.7 image-to-video accepts `first_frame_url` plus `driving_audio_url` for 2 to 15 seconds at up to 1080p. That keeps the audio-first spine but gives full scene motion instead of a talking portrait. (VERIFIED: https://docs.kie.ai/market/wan/2-7-image-to-video.md)

**Top 2 picks for talking shots on Kie:**

1. `kling/ai-avatar-pro` (Kling AI Avatar 2.0 Pro). Best lip articulation in the independent comparisons found, 1080p at 48 fps, handles cartoon, animal and stylized characters, $0.08/s.
2. `infinitalk/from-audio` at 720p. Most natural head and body motion, cheapest ($0.06/s at 720p, $0.015/s at 480p), 15s cap per call on Kie.

---

## 1. Audio-driven talking-video models, ranked

Ranking is my READ from the sources cited in each row. No neutral benchmark covers all of them. Most comparison posts are written by resellers.

| Rank | Model | Lip accuracy | Motion and expression | Max length | Resolution, fps | Stylized / cartoon / 3D | Multi-speaker | Price | On Kie |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Kling AI Avatar 2.0 Pro | Most accurate in two side-by-side tests | Stiff, limited range, one repeated hand move | 5 min per Kie API doc (see conflict below) | 1080p, 48 fps | Yes: humans, animals, cartoons, stylized | No | $0.08/s Kie, $0.115/s fal | Yes |
| 2 | InfiniteTalk | Good, lags on some phonemes | Best: nods, tilts, shoulders, finer expression | 15s per call on Kie. Open source holds about 1 min before color shift | 480p or 720p, 25 fps | Not documented. Test it | Yes in open source (separate weights). Not exposed on Kie | $0.015/s 480p, $0.06/s 720p on Kie | Yes |
| 3 | OmniHuman 1.5 | Good early, decays | Full body, gestures can overreach | Under 60s, Kie recommends 15s or less | 720p or 1080p | Yes: people, pets, anime | Yes, pick the speaker with a mask (up to 5) | $0.135/s Kie, $0.16/s fal | Yes |
| 4 | HeyGen Avatar V / IV | Very strong on real humans (self-reported LSE-C 8.97 for V) | V has native gaze variation, IV adds gestures | V stable at 4 min in one review | 1080p | IV supports human, anime, animal. V needs a 15s selfie video | Not checked | About $0.067/s for V | No |
| 5 | Hedra Character-3 | Mixed: weakest of three in a 2025 test, praised for expression | Dynamic, can over-act | 10 min | 540p to 1080p | Best fit for mascots, clay, illustration | Not checked | $0.05/s at 720p | No |
| 6 | VEED Fabric 1.0 | Tuned for UGC talking heads | Emotion in audio carries to face | 60s | 480p or 720p | Not documented | No | $0.08/s 480p, $0.15/s 720p | No |
| 7 | Wan 2.2 S2V | Finicky | 16 fps, weak long-term consistency | 120 frames on Kie (7.5s at 16 fps) | 480p to 720p | Not documented | No | $0.06 to $0.12/s Kie | Yes |
| n/a | Creatify Aurora, Mirage Avatar X, LTX-2.3 audio-to-video, MultiTalk, RIZZ | Not evaluated here | | | | | | | No |

Sources for the table:

- Kling vs OmniHuman, neutral speech and emotion tests, Kling ahead on articulation: https://piapi.ai/blogs/omnihuman-1-5-vs-kling-ai-avatar (VENDOR, reseller of both, March 2026)
- Kling vs Hedra vs InfiniteTalk, same image and audio, Kling most accurate, InfiniteTalk most motion, Hedra off: https://videomaker.me/blog-kling-ai-avatar-vs-hedra-vs-infinitetalk-best-ai-avatar-tool-54935 (Sept 2025, so it tested Kling Avatar v1)
- InfiniteTalk vs Kling vs OmniHuman, lip order OmniHuman then Kling then InfiniteTalk, motion order InfiniteTalk first, Kling stiff: https://wavespeed.ai/blog/posts/the-2026-ai-digital-human-crown/ (VENDOR, hosts InfiniteTalk, Dec 2025)
- OmniHuman 1.5 decays by second 10 to 11: https://maxfusion.ai/blog/ai-video-models-lip-sync-2026 (VENDOR, sells a competing avatar model). Kie's own doc says quality degrades past 15s: https://docs.kie.ai/market/omnihuman-1-5.md
- Kling Avatar 2.0 specs, stylized support, 1080p 48 fps: https://kie.ai/kling-ai-avatar and https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/pro
- Kling Avatar input rules (face 60 to 70 percent of frame, 512px minimum, 5 to 30 second clips work best, long audio goes stiff): https://fal.ai/learn/devs/kling-avatar-v2-developer-guide
- InfiniteTalk base model, 1 minute limit, color shift, audio CFG 3 to 5: https://github.com/MeiGen-AI/InfiniteTalk
- OmniHuman limits on fal (60s at 720p, 30s at 1080p, $0.16/s): https://fal.ai/learn/devs/omnihuman-15-user-guide
- HeyGen Avatar V numbers: https://theplanettools.ai/blog/heygen-avatar-v-tested-hands-on-review-2026 (the LSE-C figure is HeyGen's own; the per-second price came from a search summary and is not pinned to a page)
- Hedra and HeyGen prices and stylized fit: https://novoads.ai/en/blog/hedra-vs-heygen (Sept 2026)
- Fabric specs and price: https://fal.ai/models/fal-ai/veed/fabric and https://invideo.io/blog/ai-lipsync-models/
- VEED's own shootout (claims Kling shows more floating-mouth artifacts, Hedra over-smiles): https://www.veed.io/learn/best-lipsync-api (VENDOR)
- Wan S2V finicky, 16 fps: https://reddit.sentinel-team.org/posts/1rwtez2/snapshots/2026-03-20T17%3A36%3A49.07391Z and https://comfyui-wiki.com/en/tutorial/advanced/video/wan2.2/wan2-2-s2v
- Current avatar model list on fal (shows HeyGen Avatar V, Mirage Avatar X, Creatify Aurora, Sync v3): https://fal.ai/explore/best-avatar-models

**Non-frontal faces.** Every avatar vendor says front or slight three-quarter only. Kling's lip sync guide puts the limit at about 30 degrees off center. Profiles fail. (VERIFIED: https://www.hedra.com/blog/ai-lip-sync-video-guide, https://www.atlascloud.ai/blog/guides/kling-ai-lip-sync). HeyGen Avatar V claims multi-angle stability (review link above). Sync-3 is the only tool that claims profiles and over-shoulder shots. (https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality)

**Elderly faces.** No source found for any model. READ: the model invents teeth and smooths skin, so use a closed-mouth start frame, keep the face large, and check plosives at quarter speed. This matters for 65+ offers, so put an elderly face in the first bake-off.

**Stylized characters.** Kling Avatar 2.0, OmniHuman 1.5 and Hedra claim support. Sync says models trained on real faces can produce mouth artifacts on AI and 3D characters. (https://support.sync.so/articles/4535262132-why-is-my-ai-avatar-generation-showing-poor-lip-sync-and-robotic-movement)

### What Kie actually hosts (verified today)

| Kie model id | What it is | Limits from Kie docs | Kie price |
|---|---|---|---|
| `kling/ai-avatar-pro` | Kling AI Avatar 2.0, 1080p | image jpeg/png up to 10MB, audio up to 100MB and 5 min, prompt field required (can be empty), 5,000 chars | $0.08/s |
| `kling/ai-avatar-standard` | Same, 720p | Same | $0.04/s |
| `infinitalk/from-audio` | InfiniteTalk image + audio | audio up to 10MB, 480p or 720p, prompt required, seed 10000 to 1000000. Landing page: audio must not exceed 15s | $0.015/s 480p, $0.06/s 720p |
| `omnihuman-1-5` | OmniHuman 1.5 | audio under 60s (15s or less recommended), 720 or 1080, `mask_url` to choose the speaker, prompt up to 300 chars, fast mode | $0.135/s |
| `wan/2-2-a14b-speech-to-video-turbo` | Wan 2.2 S2V | 40 to 120 frames, default 16 fps, 480p/580p/720p | $0.06 to $0.12/s |
| `wan/2-7-image-to-video` | General video model with `driving_audio_url` | first frame + driving audio, 2 to 15s, 720p or 1080p | $0.08/s 720p, $0.12/s 1080p |
| `volcengine/video-to-video-lip-sync` | Post-hoc redub | lite = single person frontal, basic = complex scenes. Video 360p to 1080p, 24 to 60 fps. Audio must be pure vocal | $0.04/s |
| `elevenlabs/text-to-speech-multilingual-v2` | TTS | 5,000 chars, `timestamps: true` returns word timestamps, `previous_text` and `next_text`, speed 0.7 to 1.2 | $0.06 per 1,000 chars |
| `elevenlabs/text-to-dialogue-v3` | Eleven v3 | stability setting, no timestamps flag | see page |
| `elevenlabs/audio-isolation` | Voice isolation | | see page |

Doc pages: https://docs.kie.ai/market/kling/ai-avatar-pro.md, https://docs.kie.ai/market/infinitalk/from-audio.md, https://docs.kie.ai/market/omnihuman-1-5.md, https://docs.kie.ai/market/wan/2-2-a14b-speech-to-video-turbo.md, https://docs.kie.ai/market/volcengine/video-to-video-lip-sync.md, https://docs.kie.ai/market/elevenlabs/text-to-speech-multilingual-v2.md, https://docs.kie.ai/market/elevenlabs/text-to-dialogue-v3.md. Prices: https://kie.ai/kling-ai-avatar, https://kie.ai/infinitalk, https://kie.ai/omnihuman-1-5, https://kie.ai/wan-speech-to-video-turbo, https://kie.ai/wan-2-7-video, https://kie.ai/volcengine-video-to-video-lip-sync, https://kie.ai/elevenlabs-tts.

**Not on Kie** (absent from the docs index today): Hedra, HeyGen, VEED Fabric, Sync, Creatify Aurora, LatentSync, MuseTalk, a standalone Kling Lip Sync endpoint, a PixVerse lip sync endpoint. Sora 2 is gone everywhere: the API was shut off 2026-09-24. (https://invideo.io/blog/sora-ai-video-generator/)

**Conflict to settle with one test.** Kie's Kling avatar API doc and playground say audio up to 5 minutes. The pricing blurb on the same landing page says up to 15 seconds per generation. A third-party Kie cheat sheet also lists 5 minutes (https://github.com/ARosentiehl24/kie-avatar-studio, docs/API_KIE.md). Send one 30s audio file before designing around either number. It does not change the plan much, because short chunks are better anyway.

---

## 2. Native-audio models

| Model | Clip length | Lip sync on dialogue | Voice control | On Kie |
|---|---|---|---|---|
| Veo 3.1 | 4, 6 or 8s | Timing acceptable. One ad-account source calls the mouth rubbery with wrong shapes on plosives. Google lists short speech as still in development. Better in medium shots than close-ups | None. No voice persistence between clips | Yes |
| Kling 3.0 | 3 to 15s | Strong under 8s, drifts past second 8 in one test. Others call it the best talking pick | Voice binding: attach 5 to 30s of audio to a character element | Yes |
| Kling 4.0 | Up to 30s | Claims better lip sync, stereo audio, voice reference. Announced 2026-09-30, too new for independent tests | Voice reference | Landing page live, no API doc or price in the docs index yet |
| Seedance 2.0 | 4 to 15s | Sync strong, but words get mangled | Up to 3 reference audio clips, 2 to 15s each | Yes |
| Seedance 2.5 | 4 to 30s | Same family. Keep first tests to one speaker, one short sentence | Up to 10 reference audio clips, 2 to 30s each. Cannot combine with a first frame | Yes, expensive |
| Gemini Omni Flash 1.1 | 4, 6, 8 or 10s, 720p base | Excellent on clean takes, about 15 percent of takes stutter. Holds to about 6 to 7s with one speaker | Reusable `audio_ids` (30 preset voices) and `character_ids`. Cannot combine with a first frame | Yes |
| Wan 3.0 | 2 to 30s | Not independently tested here | Up to 5 reference audio clips, total 15s or less | Yes |
| Wan 2.7 i2v | 2 to 15s | Lips follow your uploaded audio | Your own audio drives it | Yes |
| Sora 2 | n/a | Was the best native lip sync | n/a | Shut down 2026-09-24 |
| Grok Imagine | Up to 15s | Poor | None | Yes, skip for talking |

Sources: per-model failure notes from https://maxfusion.ai/blog/ai-video-models-lip-sync-2026 (VENDOR, July 2026). Veo limits and Google's own caveat: https://prompt-architects.com/blog/101-veo-dialogue-prompts and https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1. Kling 3.0 as talking pick: https://ugcvids.ai/blog/kling-3-vs-veo-3-1-for-ugc-ads. Kling 4.0: https://kie.ai/kling-4-0 and https://kling.ai/blog/kling40-kling-visual-realism-creative-control-introducing-storytelling (second link appeared in search, not opened). Gemini Omni 6 to 7s ceiling: https://invideo.io/faq/what-is-gemini-omni-flash-and-what-can-it-do/ (appeared in search, not opened). Kie parameter facts: https://docs.kie.ai/market/kling/kling-3-0.md, https://docs.kie.ai/market/bytedance/seedance-2.md, https://docs.kie.ai/market/bytedance/seedance-2-5.md, https://docs.kie.ai/market/google/gemini-omni-flash-1-1.md, https://docs.kie.ai/market/gemini-omni-audio.md, https://docs.kie.ai/market/wan/3-0-video.md, https://docs.kie.ai/veo3-api/generate-veo-3-video.md.

**Words per clip.**

- READ: plan on about 2.5 words per second, minus half a second of air at each end. That is 16 to 20 words for an 8s Veo clip and 30 to 35 for a 15s Kling clip. A search summary across Veo guides gave 16 to 22 words for 8s, which matches, but I could not pin it to one page. Normal ad read speed is about 144 to 150 words per minute. (pace figure: https://lazykiwi.ai/blog/ai-lip-sync)
- One Veo creator guide targets 6 to 10 words per line for UGC reads, one idea per line. (https://www.veo3gen.app/blog/veo-31-dialogue-sfx-prompts-that-actually-sync-a-creator-workflow-for-clean-mout)
- One guide prints 60 to 80 words for 8 seconds. That is not possible at a natural pace. Ignore it. (https://prompt-architects.com/blog/101-veo-dialogue-prompts)
- Overwritten lines get rushed or cut off at the end. (same Veo guides)

**Dialogue syntax that works.**

- Google's official form: a description of the speaker, then says, then the line in quotation marks. Put the delivery note before the line. SFX and ambient noise get their own labeled lines. (Google Cloud link above)
- Community fix for burned-in subtitles: use a colon before the line and no quotation marks, put dialogue early in the prompt, and add no subtitles, no captions, no on-screen text. (https://www.veo3ai.io/blog/veo-3-remove-subtitles-captions-fix-2026, read by sub-agent)
- These two conflict. READ: use the colon form on Veo when subtitles appear, and accept that no prompt wording is a guarantee. One guide says exactly that and tells you to reroll. (https://www.glbgpt.com/hub/how-to-make-characters-speak-in-veo-3-1-the-ultimate-guide-to-dialogue-audio-lip-sync/)
- Attach the line to a visual description of the speaker, not a name. One speaker per clip. Keep the whole prompt under Veo's 1,024-token input limit or the dialogue at the end gets dropped. (prompt-architects link)
- Kling native audio form: who, then tone and language in brackets, then the line. More than two speakers gets voices assigned to the wrong person. (https://www.atlascloud.ai/blog/guides/kling-2-6-review, appeared in search, not opened)

**Keeping one voice and one character across clips.**

1. Kling 3.0 element with bound voice audio (5 to 30s sample). (Kie doc above; https://kling.ai/blog/kling-3-subject-binding-character-consistency appeared in search)
2. Reference audio on Seedance 2.0 / 2.5, Wan 3.0, Kling 4.0. Unverified whether the output plays your audio exactly or regenerates a similar voice. Search summaries suggest Seedance treats it as a guide.
3. Gemini Omni: create an audio id and a character id once, reuse both.
4. Voice-changer pass: stitch the native clips, run ElevenLabs speech-to-speech over the joined audio so one voice covers all clips. One open-source pipeline does this and claims timing holds within about 0.01s. (https://github.com/TheMattBerman/scrollclaw, assemble/references/audio-orchestration.md)
5. Character: same approved start frame or reference image every clip. Veo starts from a first frame, which is why faces and packaging hold. (ugcvids link)

**Known failure modes** (all from the sources above): invented subtitles, wrong speaker talking, line cut off, rushed speech, word corruption (Seedance), stutter (Gemini Omni), drift past 8s (Kling 3.0), new voice every clip (Veo), sound effects masking the line.

---

## 3. Post-hoc lip sync and dubbing models

| Model | Face render | Limits | Price | Notes | On Kie |
|---|---|---|---|---|---|
| Sync sync-3 | 4K native | 120s per job in one source | $0.107 to $0.133/s | Whole shot at once, handles profiles, occlusion, close-ups | No (fal has it) |
| Sync lipsync-2-pro | 512px + super-resolution | Split past 2 min | $0.067 to $0.083/s | Keeps teeth, beards. Struggles with still frames, profiles, occlusion | No |
| Sync lipsync-2 | 512px | | $0.04 to $0.05/s | Same weaknesses | No |
| Sync react-1 | | 15s hard cap | $0.133 to $0.167/s | Re-directs expression and head motion, not only lips | No |
| Volcengine video-to-video | Not stated | Video 360p to 1080p, 24 to 60 fps | $0.04/s | The only repair tool on Kie. Untested in any source I found | Yes |
| Kling Lip Sync | | Sources disagree: source video 2 to 10s vs 60s | about $0.07 to $0.095/s elsewhere | Frontal within about 30 degrees | Not as its own endpoint |
| PixVerse Lipsync | | 60s, 1920px | | Voice clone built in | No |
| HeyGen Lipsync Precision, VEED Lipsync v2 | | | about $0.05 to $0.07/s | Redub tools | No |
| LatentSync 1.6 (open) | 512px | 18GB VRAM | free | Best open redub, still soft, needs upscale after | No |
| MuseTalk 1.5 (open) | 256px | 8GB VRAM | free | Fast, loses beard and lip detail at 1080p | No |

Sources: https://sync.so/docs/models/lipsync, https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality, https://maxfusion.ai/blog/ai-video-models-lip-sync-2026, https://invideo.io/blog/ai-lipsync-models/, https://www.atlascloud.ai/blog/guides/kling-ai-lip-sync, https://news.creeta.com/en/open-source-lip-sync-models-2026/, https://github.com/bytedance/LatentSync, https://github.com/TMElyralab/MuseTalk.

**When a pro reaches for these** (VENDOR, maxfusion):

- Rule of thumb: cheap generation broke, reroll. Expensive generation broke, keep the picture, make clean audio, repair.
- Fixable: word corruption, sync drift, a few missed words, language swaps.
- Not fixable: bad mouth texture and realism in the source, image decay.
- Workhorse tier for plain front-facing footage, top tier (sync-3) for angles, occlusion, close-ups.

**Quality ceiling and artifacts:**

- Most redub models render the face at 512px, so close-ups go soft. Upscale after. (Sync docs; creeta link)
- They need a clear, frontal, unobstructed lower face. Hands, mics, hair over the mouth break them. (Sync docs)
- Source footage that is frozen or idle works worse than footage where the person already appears to talk. (https://support.sync.so/articles/7391977257-sync-support-faq, appeared in search, not opened)
- Sync says anime is unsupported and 3D gives poor results. (sub-agent read of https://sync.so/docs/compatibility-and-tips/media-content-tips)

READ for this skill: a repair layer is a fallback, not the spine. If a native hook shot is used and a word is wrong, run the Volcengine endpoint with the master voice chunk before rerolling an expensive clip. Test Volcengine once before relying on it.

---

## 4. Craft rules that make lip sync land

Tags: V = verified with source, R = my read.

### Start frame

1. V. Front-facing or slight angle only. (https://www.hedra.com/blog/ai-lip-sync-video-guide)
2. V. Face fills 60 to 70 percent of the frame for the generation, minimum 512px source. Simple background. (https://fal.ai/learn/devs/kling-avatar-v2-developer-guide)
3. V. Mouth closed, calm expression. Visible teeth in the still cause teeth flicker. (https://lazykiwi.ai/blog/ai-lip-sync)
4. V, with a conflict. One vendor says a light natural expression beats a blank passport face. READ: closed mouth, relaxed, slight warmth. (https://higgsfield.ai/blog/make-ai-lipsync-videos)
5. V. Nothing over the mouth or chin: hands, mics, mugs, hair, big glasses. (https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality)
6. V. Even light, no backlight, no hard shadows. (same)
7. R. Wide and full-body shots are B-roll, not dialogue. Lip detail falls with face pixel count. If a wide talking shot is needed, OmniHuman is the one built for it, and keep it under 10s.
8. R. For punch-ins, generate the tighter frame as its own start image, do not rely on cropping a 720p clip.

### Audio prep

9. V. Drive the avatar with the dry voice only. Add music and SFX in the final mix. (Sync docs; https://www.seedance.tv/fr/blog/seedance-2-5-lip-sync-issues)
10. V. WAV 16-bit PCM or MP3 at 128 kbps or more. No mouth movement usually means an encoding problem. (https://fal.ai/learn/devs/omnihuman-15-user-guide)
11. V for Seedance guides, R as a general default: mono, 44.1 or 48 kHz, peaks around minus 6 to minus 3 dBFS, no clipping. No avatar vendor publishes a LUFS target. (seedance.tv link; https://crepal.ai/blog/aivideo/blog-seedance-2-0-lip-sync-voiceover-fix/)
12. V. Pad about half a second of silence at the head and tail of each chunk. One model returned a 5.76s clip for a 6.3s line and cut the last word until padded. (https://lazykiwi.ai/blog/ai-lip-sync; https://fuser.studio/articles/best-ai-lip-sync-tools, read by sub-agent)
13. V. End every chunk on a full stop. Cut where a listener would hear a pause. (lazykiwi link; https://creatide.ai/blog/ai-lip-sync-audio-preparation-fix-timing-before-generation, read by sub-agent)
14. V. Leave natural pauses of 150 to 400 ms between phrases. Models use them as anchors. (crepal link)
15. V. Pace near 144 words per minute. Fast speech, slurred contractions, shouting and sobbing all cut accuracy or add 100 to 200 ms lag. (lazykiwi; crepal)
16. V. A flat voice gives a flat face. A calmer voice fixes jaw over-motion. Emotion in the audio is what moves the face. (higgsfield link; lazykiwi link)
17. V. Spell numbers as words, and scrub product names, acronyms, dollar amounts and dates first. Those are where sync and pronunciation break. (lazykiwi; https://www.yarnit.app/blog/the-2-ugc-ad-how-to-build-a-talking-head-video-workflow-with-ai, read by sub-agent)

### Chunk length

18. V. Many short clips beat one long one. Practitioners run 3 to 10s per beat and regenerate only the bad beat. Teeth go wrong at second 4 or the voice drifts at second 12 and a 30s roll is wasted. (Reddit r/AI_UGC_Marketing via archive: https://www.reddit.com/r/AI_UGC_Marketing/comments/1vrhw56/how_do_yall_take_care_of_ai_generated_creatives/p4dkkb5/)
19. V. Per-model ceilings: Kling Avatar best at 5 to 30s and goes stiff on long audio. OmniHuman 15s or less. InfiniteTalk 15s on Kie. Gesture loops and expression cycling show up past 30s on every tool. (fal Kling guide; Kie OmniHuman doc; https://kie.ai/infinitalk; higgsfield link)
20. R. Sweet spot for this skill: 5 to 12s chunks, one to three sentences, never over 14s.

### Editing

21. V. Put B-roll or a scene change between separately generated talking clips. It hides lighting and color shifts. (Reddit r/FacebookAds via archive: https://www.reddit.com/r/FacebookAds/comments/1ud430i/how_to_make_ai_creatives_that_actually_convert_my/)
22. V. Change the avatar's setting 2 to 3 times per ad. (same thread)
23. Low trust (automated Reddit bot account): hold a talking shot 2.5 to 4s, then hard cut with a 110 percent punch-in or J-cut. Never alternate two avatar models on one face. READ: both match common editing practice, so adopt them, but they are not evidence.
24. V. Output frame rates differ by model: InfiniteTalk 25, Kling Avatar Pro 48, Wan S2V 16. One user got desync by treating 24 fps footage as 30. (https://www.runcomfy.com/models/community/infinite-talk/image-to-video; https://kie.ai/kling-ai-avatar; comfyui-wiki link)
25. R. Run ffprobe on every clip. Conform by dropping or duplicating frames (ffmpeg `fps` filter). Never retime, never speed the voice with `atempo`.
26. V. Do not use `-shortest`. One pipeline lost 3 frames to it. Set the frame count and check it. (https://github.com/guyow/video-studio, PROJECT-SUMMARY.md)
27. R. The master voiceover is the only voice track in the final. Throw away each clip's own audio. Place each clip at its chunk's start time on the master timeline. Reject any clip whose length is off by more than one frame from its audio chunk.
28. V. 30 ms audio fades at every cut. (https://github.com/browser-use/video-use)
29. V. Re-encode generated clips with dense keyframes before compositing, or frames freeze under overlays. (https://github.com/hadimouter/ai-talking-head-pipeline)
30. V. Upscale after lip sync, not before. Upscalers invent teeth and eyes. (Reddit r/comfyui and r/vfx via archive, low volume of evidence). R: recheck p, b, m after any upscale or frame interpolation.
31. V. Add room tone and light grain or one LUT across all clips so they sit in the same world. A studio-clean voice in a bedroom scene reads fake. (r/FacebookAds thread; bot-sourced for the room tone point)

### Prompts

32. V. Keep avatar prompts short: emotion, gesture, eye contact. Extra words add noise. (https://wavespeed.ai/blog/ai-guides/infinitetalk-api-guide/, read by sub-agent; https://kling.ai/pt/quickstart/kling-ai-avatar-2-user-guide, read by sub-agent)
33. V. If the character over-acts, write a prompt that restrains movement. Matters for health claims that should not look like parody. (novoads link)
34. V. For B-roll, leave out talking, speaking, conversation. Negatives can backfire, so write the positive: sits silently, lips closed. (https://apipass.dev/blogs/how-to-solve-veo-3-keep-generating-unwanted-dialogue, read by sub-agent)
35. R. Turn sound off on every B-roll generation that offers the switch (Kling `sound: false`, Seedance `generate_audio: false`, Wan `audio: false`). It is cheaper and removes the urge to mouth words.
36. V. Naming a device in the prompt can make a phone appear in the shot. (r/FacebookAds thread)

### ElevenLabs

37. V. Current lineup: Eleven v4 (10,000 chars), v3 (5,000), Multilingual v2 (10,000 direct), Flash v2.5. Kie hosts only Multilingual v2, Turbo 2.5 and the v3 dialogue endpoint, with a 5,000 char cap on v2. (https://elevenlabs.io/docs/overview/models; Kie docs)
38. V. If the script fits one request, generate once and cut it. A 3 minute ad is about 450 words or 2,700 characters, so it fits. (R on the arithmetic)
39. V. v3 stability: Creative is expressive but can hallucinate, Natural is balanced, Robust is stable and ignores tags. Low stability drifts fastest across a batch. Tags only land if the voice already has that delivery in it. (https://elevenlabs.io/docs/best-practices/prompting, read by sub-agent; https://hackernoon.com/how-to-keep-an-ai-voice-consistent-across-every-video-clip)
40. V. Request stitching (`previous_request_ids`) is for chunked generation and does not work on v3. (https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching, read by sub-agent)
41. V. Test a voice on 2 minutes or more of script to catch pacing drift before committing. (yarnit link)

### The one check to learn

42. V. Watch p, b and m at quarter speed. If the lips close on those, the rest of the clip is usually fine. (https://lazykiwi.ai/blog/ai-lip-sync)

---

## 5. Making B-roll and animation match the words

**Word timestamps, best to worst for this pipeline:**

1. Kie `elevenlabs/text-to-speech-multilingual-v2` with `timestamps: true`. Word times come back with the audio, from the engine that made it. No alignment step. (VERIFIED in Kie doc. Output shape not tested.)
2. ElevenLabs direct: the with-timestamps endpoint returns character-level start and end times, and the Forced Alignment API aligns known text to any audio and returns words plus a loss score. Needs an ElevenLabs key, not Kie. (https://elevenlabs.io/docs/api-reference/streaming-with-timestamps and https://elevenlabs.io/docs/api-reference/forced-alignment/create.md, read by sub-agent)
3. WhisperX forced alignment. Accurate to under 100 ms, but it cannot align tokens like years and prices written in digits. `pip install whisperx` (3.8.6, needs Python 3.10 or newer; this Mac's system Python is 3.9.6). (https://github.com/m-bain/whisperX)
4. whisper.cpp. Already installed here at /opt/homebrew/bin/whisper-cli. Word-level output exists, quality depends on model size. One repo found small.en drifts 100 to 300 ms when music is mixed in and medium.en holds. (https://github.com/krusemediallc/claude-code-ai-ad-builder-kie-ai, shared/skills/caption-video/prompting/guide.md)
5. stable-ts (https://github.com/jianfch/stable-ts) and mlx-whisper are also on PyPI. Not evaluated.

Use option 1, and keep whisper-cli as the fallback and as a check that the audio says what the script says.

**Shot planning from the script:**

- Split the script into sections of 5 to 10s that never cut a sentence. (https://github.com/matt-j-penny/vox-style-video)
- R: tag each sentence as talking shot, B-roll over voice, or cutaway. One visual per claim or noun. The picture of the thing lands when the word is said, with the cut 2 to 3 frames early.
- Generate B-roll from a frame pulled out of the talking clip so the room and character match. (https://github.com/TheMattBerman/scrollclaw)
- Trim each B-roll clip to its words. No dead air. (krusemedia repo, claymation-ad guide)
- Any text that must be correct (prices, product names) goes on in post, never in the generation prompt. (vox-style-video repo)

**Cut cadence:**

- Hook inside the first 3 seconds. Draft 5 to 10 hooks per concept. (https://sync.so/blog/ai-ugc, read by sub-agent)
- B-roll clips of 1 to 3s. Scene change every 2 to 3s in UGC-style ads. (https://influee.co/gb/blog/raw-ugc-to-ads, read by sub-agent)
- R: for a 30s to 3min DR ad, alternate 3 to 6s of face with 1 to 3s of B-roll, and never show two back-to-back talking clips from different generations without a cutaway or a punch-in between them.

**Captions:**

- Take timing from the timestamps but burn the script's own words. Match with difflib so captions stay word-perfect even when a transcriber mishears. (https://github.com/digitalsamba/claude-code-video-toolkit, gen_captions.py)
- Word-by-word highlight, bold sans, white with black stroke. Sources say 3 to 7 words per line. Open-source ad tools use 2-word uppercase chunks or a grouper capped at 22 characters and 5 words that breaks on a 0.55s gap. (https://www.opus.pro/blog/tiktok-caption-subtitle-best-practices, read by sub-agent; video-use repo; krusemedia repo)
- Safe zone on 1080x1920: x 60 to 960, y 210 to 1480. Keep text out of the bottom quarter and top 15 percent. (scrollclaw repo, assemble/references/green-zone.md; https://reap.video/blog/short-form-video-safe-zones, read by sub-agent)
- Show each caption at the word start, no lead-in. (krusemedia repo)
- **Local blocker, verified on this Mac today:** the installed Homebrew ffmpeg 8.1.1 has no `subtitles`, `ass` or `drawtext` filter. Caption burn-in needs another route: render caption frames with Pillow and overlay them, render captions over a key color and `chromakey` them on (the krusemedia approach, and `chromakey` is present here), use HyperFrames or Remotion, or install an ffmpeg build with libass.

---

## 6. Local lip-sync QA on an M-series Mac

No GPU farm needed. Nothing here has published Mac timings, so benchmark on one clip first.

### Recommended gate, in order

**Stage 0. Container check with ffprobe.** Milliseconds.

- Compare video and audio stream `start_time` and `duration`.
- Compare clip duration with its audio chunk duration. Fail if off by more than one frame.
- Threshold on the audio-minus-video difference. MP4 start times are often nonzero for harmless reasons. (https://trac.ffmpeg.org/ticket/424)

**Stage 1. MediaPipe mouth signal + Silero VAD.** Cheap, CPU.

- Per frame: lip gap from Face Landmarker, normalized by eye distance, or the `jawOpen` blendshape.
- Check A: mouth moving during silences of 300 ms or more. Catches flapping.
- Check B: mouth still during speech. Catches frozen faces and failed generations.
- Check C: cross-correlate lip gap with the audio RMS envelope, read the lag at the peak. Catches gross offsets of several frames.
- Check D (optional): at each p, b, m from the word timestamps, the lip gap should be near zero. This is the automated version of the quarter-speed plosive check. Deepfake research uses the same idea. (https://openaccess.thecvf.com/content_CVPRW_2020/html/w39/Agarwal_Detecting_Deep-Fake_Videos_From_Phoneme-Viseme_Mismatches_CVPRW_2020_paper.html)
- Install: `pip install mediapipe silero-vad`. MediaPipe 1.0.1 ships a macOS arm64 wheel (checked on PyPI today). The old `mp.solutions.face_mesh` API is gone, use the Tasks API `FaceLandmarker` in video mode with blendshapes on. (https://github.com/google-ai-edge/mediapipe/issues/6192; https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/python; https://github.com/snakers4/silero-vad)
- Prior art: THEval scores lip sync with exactly this lip-gap vs RMS idea and got a 0.404 rank correlation with human ratings. (https://arxiv.org/html/2511.04520v1) No maintained repo does the cross-correlation step, so that part is ours to write.

**Stage 2. SyncNet. The primary gate.**

- It is the only tool found that returns an offset in frames plus a confidence, and it runs on CPU.
- Original: https://github.com/joonson/syncnet_python. Outputs AV offset, min dist, confidence. Updated April 2026 with a CPU conda env (Python 3.10, torch 2.5.1). No MPS path. It resamples to 25 fps and 16 kHz itself. Defaults: tracks under 100 frames (4s) are dropped, faces under 100px are dropped, search window plus or minus 15 frames.
- pip route: `pip install syncnet-python` (0.2.2, Python 3.9+, https://github.com/nawta/SyncNet_py313). Small project. You download the two weight files yourself. The PyPI package named plain `syncnet` is unrelated.
- Built for AI talking characters: https://github.com/congwei1230/MoChaBench has a SyncNetPipeline with weights bundled and CPU support.
- LatentSync's eval script uses the same classic SyncNet with a 50-frame minimum track: https://github.com/bytedance/LatentSync (eval/eval_sync_conf.py).

### Thresholds

- In sync = offset within plus or minus 1 frame at 25 fps. (https://arxiv.org/pdf/2204.02090)
- Viewers detect audio early by 45 ms and audio late by 125 ms. One frame at 25 fps is 40 ms, so two frames early is already visible. (ITU-R BT.1359, quoted in https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf)
- Confidence on real video: about 7 to 8 (LRS2 7.8, LRS3 7.6, LRW 6.9). (https://arxiv.org/pdf/2008.10010)
- Confidence on AI talking-character models in MoChaBench: 6.3 for the best, 4.7 to 4.9 for mid, 1.7 for poor.
- LatentSync throws out training clips below 3.
- **Starting gate (READ, calibrate on 20 of our own good and bad clips):** fail if confidence is under 3 or the offset is 2 frames or more. Review if confidence is 3 to 5. Pass at 5 or more with offset 0 or 1.
- Check the sign convention once: shift a good clip's audio by 3 frames with ffmpeg and confirm the reported offset moves by 3.

### Gotchas

- **SyncNet confidence is not perceived quality.** THEval found LSE-C and LSE-D do not track human ratings, and a codec change alone moved scores by up to 1.2. Another study found only the offset output moderately useful. Use it to catch offsets and gross failures, not to rank takes. (https://arxiv.org/html/2511.04520v1; https://arxiv.org/pdf/2403.06421)
- **Score against the dry voice chunk**, never the final mix with music. (MoChaBench docs)
- **Stylized, 3D and elderly faces.** The face detectors are trained on real human faces. No failure-rate data exists. Treat no face track found as its own result, never as a pass, and log what share of frames had a face.
- **Short clips.** Anything under about 4s is silently skipped by default settings. Lower the minimum track or score the chunk before it is trimmed.
- **Scene cuts split tracks.** Score each talking clip before assembly, then spot-check the final.
- **Envelope method limits.** Mouth opening and loudness are only loosely tied, mouth movement leads the sound by 100 to 300 ms in natural speech, and m, b, p make sound with closed lips. A correct clip will not peak at zero lag. Calibrate a baseline lag on known-good clips and flag deviation. (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2700967/)
- **Skipped on purpose:** Synchformer (https://github.com/v-iashin/Synchformer) classifies offset in 0.2s steps, too coarse, GPU only. TalkNet-ASD and Light-ASD give speaking or not speaking, not an offset, and are hardcoded to CUDA. VocaLiST is non-commercial. No SyncNet ONNX or CoreML port was found.

---

## 7. Existing repos and skills

Nothing found does the whole job (script in, 30s to 3min talking-character ad out, audio-first, on Kie). The parts exist. All links below were opened by a sub-agent through the GitHub API and I confirmed each URL resolves.

**1. krusemediallc/claude-code-ai-ad-builder-kie-ai** (33 stars, July 2026, MIT)
https://github.com/krusemediallc/claude-code-ai-ad-builder-kie-ai

- Pipeline: still image (Nano Banana 2 or GPT Image 2), user approves, image-to-video with native audio on Veo 3.1, Seedance 2 or Sora 2. Pixar and claymation recipes add per-beat ElevenLabs voice, ffmpeg stitch, captions.
- Steal: the no-dead-space trim rule (ffprobe each voice file, trim the clip to voice length + 0.5s, never `atempo`). The mix recipe (voice 100 percent, clip audio 28 percent, music 10 percent, placed with `adelay`). The caption guide. Cost estimate before every call. Image QA capped at 2 retries. A JSONL call log. Model strings in one file.
- Kie notes it records: poll about every 30s, rate limit 20 requests per 10s.
- Short: native audio only, 8 to 15s clips, voice drifts between clips, no avatar models, user approves at many steps. It also says Kie has no file upload, which is wrong.

**2. ARosentiehl24/kie-avatar-studio** (1 star, Sept 2026, no license, Spanish)
https://github.com/ARosentiehl24/kie-avatar-studio

- Pipeline: Kie only, audio-first. Upload image, make ElevenLabs voice through Kie, wait, call `kling/ai-avatar-pro` with image and audio, download.
- Steal: docs/API_KIE.md is the best Kie cheat sheet found. Voice settings go flat inside `input`. `language_code` returns 422 on multilingual-v2. No voice-list endpoint. Avatar limits it lists: audio 5 min and 100MB, image 10MB.
- Short: no captions, no final stitch, no license. Read it, do not copy code.

**3. TheMattBerman/scrollclaw** (71 stars, March 2026, MIT)
https://github.com/TheMattBerman/scrollclaw

- Pipeline: persona research, script, first frame, Sora 2 or Kling 3 talking clips with native voice on fal, Kling B-roll, ffmpeg assembly, grain, captions last, scoring gate.
- Steal: the one-voice trick (stitch clips, run speech-to-speech over the joined audio, drop B-roll in as video only). B-roll generated from a frame of the talking clip. A vision-model score with a hard fail on a weak hook. A post-stitch QA script. Text safe zones.
- Short: 15 to 30s only, fal and Replicate, not Kie.

**4. digitalsamba/claude-code-video-toolkit** (2,164 stars, Oct 2026, MIT)
https://github.com/digitalsamba/claude-code-video-toolkit

- Pipeline: scenes.json, voice per scene, captions, build. Voice length sets scene length. Has a portrait + audio talking-head tool on a self-hosted model.
- Steal: caption alignment that burns the script's words with Whisper's timing. Per-project phase tracking file.
- Short: explainer tool, self-hosted models, no ad format, no Kie.

**5. guyow/video-studio** (1 star, Aug 2026, no license)
https://github.com/guyow/video-studio

- Pipeline: transcribe a winning ad, rewrite the script to fit footage length at a measured words-per-second, voice clone, lip-sync redub, word-timed captions.
- Steal: `-shortest` ban and frame-count check. Cut video at speech end before lip sync. Lip sync fails on frames with no face, such as end cards. Every repair is a new take, never an overwrite. Caption fallback to segment timing when word alignment crashes.
- Short: redubs real footage, does not generate characters.

**6. matt-j-penny/vox-style-video** (30 stars, July 2026, no license)
https://github.com/matt-j-penny/vox-style-video

- Pipeline: audio-first on Kie. Script, voice, word-level transcript, 5 to 10s sections that never cut a sentence, each scene starts from the previous scene's last frame, stitch.
- Steal: the sectioning rules and the rule that exact text goes on in post.
- Short: narrated collage, no talking character.

**7. hadimouter/ai-talking-head-pipeline** (0 stars, Sept 2026, MIT)
https://github.com/hadimouter/ai-talking-head-pipeline

- Pipeline: portrait + audio into Hedra Character-3, then captions.
- Steal: re-encode with dense keyframes (`-g 25 -keyint_min 25`) before compositing.

**8. browser-use/video-use** (28,051 stars, Oct 2026, MIT)
https://github.com/browser-use/video-use

- An editing skill for existing footage.
- Steal: the self-check loop. Render a filmstrip plus waveform image at every cut on the finished file, look at it, fix, re-render, max 3 passes. 30 ms audio fades at cuts.

**Caption and Kie helpers:**

- https://github.com/heygen-com/hyperframes (56,824 stars): caption skills, 35 styles, local transcription.
- https://github.com/remotion-dev/skills (4,841 stars): Remotion caption skill with local Whisper.
- https://github.com/thanhthuduc99/edit-short-skill: karaoke captions plus a QA report for black frames, freezes and audio offset, voice at minus 16 LUFS.
- https://github.com/elibarnett/kie-mcp: Kie model registry with costs, lists OmniHuman 1.5, Kling AI Avatar, Infinitalk and the lip-sync redub.
- https://github.com/mrdainami/kie-mcp and https://github.com/Cripacx/mediagen: generic Kie wrappers.
- Kie File Upload API: https://docs.kie.ai/file-upload-api/quickstart. Uploads are temporary. The page gives two retention figures (3 days and 24 hours), so download results right away.

**My read of the gap.** Nobody chains one continuous voice, sentence-bounded chunks, an audio-driven avatar per chunk on Kie, B-roll over the same audio, and an automatic sync gate. Repos 2 and 6 are closest and both stop short.

---

## 8. Recommended architecture for a one-shot pipeline on Kie

### Why audio-first wins here (READ)

1. **One voice for up to 3 minutes.** Native models give a new voice per clip unless you add binding, references or a voice-changer pass. A single TTS call removes the problem.
2. **Timing is known before any video is rendered.** Shot plan, B-roll cues and captions come from the same word timestamps.
3. **Each shot is small and checkable.** A 5 to 12s chunk either passes the gate or gets rerolled alone. No user in the loop.
4. **No word corruption.** The words are in the audio file. Native models still mangle or drop words.
5. **Cost.** Kling Avatar Pro is $0.08/s on Kie. Seedance 2.5 at 720p with no video input is $0.315/s. Kling 3.0 Pro with audio is $0.135/s. (https://kie.ai/seedance-2-5, https://kie.ai/kling-3-0)
6. **Stylized characters.** Kling Avatar 2.0 is documented for cartoons and animals.

What audio-first gives up: avatar models move less than native models. Hands, props and walking are weak. That is what B-roll, cutaways and the optional Wan 2.7 shots are for.

### Pipeline

1. **Script to shot plan.** Split into sentences. Tag each as TALK, BROLL or CUTAWAY. Scrub numbers, prices, acronyms and product names into spoken form.
2. **Master voiceover.** One call to `elevenlabs/text-to-speech-multilingual-v2` with `timestamps: true`. Under 5,000 characters, so no stitching. If v3 emotion tags are wanted, use the v3 dialogue endpoint and align with whisper-cli. Normalize, keep it dry, save as 48 kHz mono WAV.
3. **Chunk.** Cut at sentence ends on the silence midpoint. 5 to 12s per chunk. Add about 0.3 to 0.5s of silence at head and tail of each chunk file, and record the pad so it can be trimmed back off.
4. **Start frames.** One approved master character image. Derive 2 to 3 framings and 2 to 3 settings from it with an image edit model. Closed mouth, frontal, face large, even light.
5. **Talking shots.** Upload image and chunk, call `kling/ai-avatar-pro` with a short prompt (emotion, gesture, eye contact). Submit all chunks in parallel inside the rate limit. Poll every 30s. Download at once.
6. **Gate each clip.** Stage 0, 1, 2 from section 6 against the dry chunk. On fail: reroll once, then switch to `infinitalk/from-audio` at 720p, then cover that sentence with B-roll.
7. **B-roll.** Generate with sound off and no speech words in the prompt. Time each clip to its words from the timestamps. Use a frame from a talking clip as the first frame when the scene should match.
8. **Assemble.** Conform every clip to one frame rate (30 fps) with frame drop or duplicate. Trim the pads. Place each talking clip at its chunk's start time. Lay B-roll as video only. The master voiceover is the single voice track. Alternate framings or cut away at every chunk seam. 30 ms fades at cuts. Music and room tone under. Loudness normalize the final.
9. **Captions.** Script words, timestamp timing, safe zone, rendered by a route that works on this Mac (see section 5).
10. **Final check.** Re-run SyncNet on each talking span of the export. Render a filmstrip at each cut and look at it. Max 3 fix passes.

### Top 2 model picks for talking shots

1. **`kling/ai-avatar-pro`.** Most accurate articulation in the comparisons found. 1080p 48 fps so no upscale step. Documented for stylized characters. $0.08/s. Its weakness is stiffness, which short chunks, varied framings and B-roll hide.
2. **`infinitalk/from-audio` at 720p.** Best natural head and body motion. $0.06/s. Use as fallback and for shots that need a livelier performer. Needs chunks of 15s or less and likely an upscale.

Also test: `wan/2-7-image-to-video` with driving audio for shots that need hands, props or movement. `omnihuman-1-5` for wide or two-character shots under 10s.

### Rough cost for a 60s ad (READ, from Kie list prices)

- 40s of talking on Kling Avatar Pro: $3.20. With a 30 percent reroll rate: about $4.20.
- Voice: about 900 characters, about $0.05.
- B-roll: 20s. On Wan 2.7 at 720p about $1.60. On Veo 3.1 Fast, three 8s clips, about $0.90.
- Total: about $6 to $7 before images.

### Main risks

1. **The Kie Kling avatar length limit is unclear** (15s vs 5 min). Chunking at 12s sidesteps it.
2. **Seams.** Every chunk restarts head pose and gesture. Without a cutaway or reframe at each seam it looks like a glitch.
3. **Stiff avatar.** Kling Avatar may read as presenter, not UGC. If realism of the person is the point, a native hook shot or Wan 2.7 driving audio may be needed.
4. **The gate can be wrong.** SyncNet does not match human judgment and may not find stylized or elderly faces. Calibrate on our own clips and keep the plosive check.
5. **Elderly and Pixar-style faces are untested everywhere.** No source covers them.
6. **Frame-rate mismatch.** 48, 25 and 16 fps sources on one timeline. Conform by frame drop only.
7. **Kie timestamp output is undocumented in shape.** Confirm what comes back before building on it.
8. **Kie file links expire.** Download immediately.
9. **Captions cannot be burned with the ffmpeg on this Mac.** Pick the route up front.
10. **The market moves monthly.** Kling 4.0 (30s clips, voice reference) landed four days ago and is not yet in Kie's API docs. Keep model ids in one config file.

### First test to run (about $10)

One 10s voice chunk, three start frames (realistic adult, elderly, Pixar-style), through four models: `kling/ai-avatar-pro`, `infinitalk/from-audio` 720p, `omnihuman-1-5`, `wan/2-7-image-to-video` with driving audio. Score all twelve with the gate, watch p, b, m at quarter speed, and send one 30s chunk to Kling Avatar to settle the length question. That bake-off replaces most of the uncertainty in sections 1 and 8.

---

## Sources that carry the most weight

- Kie docs index and model pages (primary, fetched today): https://docs.kie.ai/llms.txt
- Sync Labs docs on input quality: https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality
- InfiniteTalk repo: https://github.com/MeiGen-AI/InfiniteTalk
- fal developer guides: https://fal.ai/learn/devs/kling-avatar-v2-developer-guide and https://fal.ai/learn/devs/omnihuman-15-user-guide
- Google's Veo 3.1 prompting guide: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Ad-account model comparison (vendor): https://maxfusion.ai/blog/ai-video-models-lip-sync-2026
- Redub model roster (vendor): https://invideo.io/blog/ai-lipsync-models/
- Lip sync craft guide: https://lazykiwi.ai/blog/ai-lip-sync
- SyncNet: https://github.com/joonson/syncnet_python
- THEval (why SyncNet scores are not quality): https://arxiv.org/html/2511.04520v1
- ElevenLabs models: https://elevenlabs.io/docs/overview/models

## What was not found

- A neutral benchmark across current avatar models.
- Any guidance on elderly faces.
- A vendor LUFS or sample-rate spec for avatar inputs.
- Evidence on whether Seedance and Wan 3.0 play reference audio exactly or regenerate it.
- Independent tests of Kling 4.0, Wan 2.7 driving audio, or Kie's Volcengine lip sync.
- Mac timings for SyncNet or MediaPipe.
