# Voice realism for the talking-character ad pipeline

Researched 2026-10-05. Scope: how to get a voice that sounds like a real, ordinary American of 66 talking casually to a phone in a kitchen, and how to judge that by machine, since the pipeline builder cannot listen.

No Kie generation task was created and no credits were spent. Nothing in this file was judged by ear. Every realism number is an estimate and is marked as such.

## How to read the labels

| Label | Meaning |
|---|---|
| (V) | I opened the page and read it during this research |
| (H) | A helper agent opened the page during this research and reported it |
| (S) | Seen in a search result summary only. The page was not opened. Treat as a lead |
| (VENDOR) | The vendor's own marketing or docs. Capability claims, not independent tests |
| (MR) | My read. Reasoning from the sources, not a sourced fact |
| [doc] | From the Kie reference `tools/video/research/kie-api.md` (pulled from docs.kie.ai on 2026-10-04) |

Speech length assumption used for prices: 10 minutes of speech is about 10,000 characters (Inworld's own figure is roughly 1,000 characters per minute (S) https://howaiworks.ai/blog/inworld-realtime-tts-2-launch-2026). At the slower pace of a 60+ speaker it is closer to 9,000.

---

## 0. Read this first

1. **The model was not the weak link on paper.** Gemini 3.8 Flash TTS sits at number 4 of 92 on the Artificial Analysis Speech Arena (Elo 1275), level with Cartesia's best model (1278). Only Eleven v4, released one week ago, is clearly ahead. (V) https://artificialanalysis.ai/text-to-speech/leaderboard. So "super fake" is probably not about which engine was used. (MR) The likely causes, in order: a studio-dry voice laid over a kitchen picture, a preset voice from the "Professional" group reading in announcer cadence, even pacing with no breaths or restarts, and generated brown noise instead of a real room.
2. **Arena rank measures the wrong thing for this job.** Arena voters compare two short read sentences and pick the more natural one. (V) https://www.digitalapplied.com/blog/best-text-to-speech-models-september-2026-ranked-priced. Nobody is asked whether it sounds like a specific 66 year old in a kitchen on a phone mic. Use rank to shortlist engines, not to pick the voice. (MR)
3. **The most real voice is a real performance.** Every agency source that names a fix for fake-sounding AI UGC lands on the same thing: a human reads the line casually, and speech-to-speech maps that performance onto the character's voice. (V) https://www.pigeondigital.com/insight/ai-ugc-sounds-fake-speech-to-speech-fix-believable-avatars, (V) https://www.z2adigital.com/blog-content/make-ai-ugc-human. The pipeline is audio-first, so any audio file can drive it. That includes a phone voice memo.
4. **ElevenLabs shipped Eleven v4 on 2026-09-28.** It is now number 1 on the same arena (Elo 1321). It is not on Kie. (V) https://artificialanalysis.ai/text-to-speech/leaderboard, (V) https://elevenlabs.io/v4, [doc].
5. **Kie has no voice cloning, no voice design, and no voice changer.** With only a Kie key the choices are preset TTS voices (Gemini today, ElevenLabs when its endpoint comes back) or video models that generate the voice with the picture. [doc]
6. **No machine score reliably tells "sounds human" from "sounds AI".** Detectors and MOS predictors are weak proxies. The stack in section 6 will reject clearly bad takes and compare candidates against real reference clips. Ryan's ear stays the final gate.

---

## 1. Ranking of current voice options for this job

### 1.1 Leaderboards as of 2026-10-05

Artificial Analysis Speech Arena, top rows read today. Price is their normalized dollars per 1M characters. (V) https://artificialanalysis.ai/text-to-speech/leaderboard

| Rank | Model | Maker | Elo | $ per 1M chars | Released |
|---|---|---|---|---|---|
| 1 | Eleven v4 | ElevenLabs | 1321 | 80.0 | Sept 2026 |
| 2 | Qwen-Audio-3.1-TTS-Plus | Alibaba | 1292 | 19.3 | Sept 2026 |
| 3 | Sonic 3.6 | Cartesia | 1278 | 49.0 | Aug 2026 |
| 4 | Gemini 3.8 Flash TTS | Google | 1275 | 16.5 | Sept 2026 |
| 5 | Qwen-Audio-3.0-TTS-Plus | Alibaba | 1261 | 19.3 | Sept 2026 |
| 6 | Realtime TTS-2 | Inworld | 1251 | 20.8 | Aug 2026 |
| 7 | Simba 3.2 | Speechify | 1242 | 6.6 | Jul 2026 |
| 8 | Gemini 3.8 Flash-Lite TTS | Google | 1242 | 11.0 | Sept 2026 |

Lower rows from a snapshot dated 2026-09-25 (before Eleven v4 landed). (V) https://www.digitalapplied.com/blog/best-text-to-speech-models-september-2026-ranked-priced

| Model | Elo | $ per 1M chars |
|---|---|---|
| Gemini 3.1 Flash TTS | 1202 | 18.31 |
| ElevenLabs v3 Conversational | 1196 | 50 |
| MiniMax Speech 2.8 HD | 1170 | 100 |
| Eleven v3 | 1169 | 100 |
| MiniMax Speech 2.8 Turbo | 1149 | 60 |
| Fish Audio S2.1 Pro | 1140 | 15 |
| Voxtral TTS (Mistral, open weights, non-commercial license) | 1078 | |
| Kokoro 82M (open, Apache 2.0) | 1063 | 0.65 hosted |

Notes:

- The same article says the top three were a statistical tie on 09-25, and that price varies far more than Elo across the top group. (V) same page.
- OpenAI gpt-4o-mini-tts is not on the Artificial Analysis board. A second board (Voice Arena) ranks it 19th. (V) same page.
- The Hugging Face TTS Arena V2 page did not render its table when fetched, and one site that used to mirror its numbers withdrew them on 2026-09-30 and now points readers to Artificial Analysis. (V) https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2, (V) https://offlinetts.com/blog/tts-arena-leaderboard-2026/. I have no current TTS Arena numbers.
- Cartesia claims listeners preferred Sonic 3.6 over Eleven v3 in 92% of US English blind tests. (VENDOR, S) https://cartesia.ai/blog/sonic-3.6/. ElevenLabs claims v4 won about 75% of blind tests against four rivals. (VENDOR via V) digitalapplied page above.

### 1.2 Ranking for this specific job (MR)

The job: a real ordinary American woman of 66, or man of 66, talking casually to a phone camera. Not a narrator. The ranking weighs four things the arenas do not: can it do an OLDER voice, can it do casual uneven delivery, does it take delivery marks without changing words, and can one voice hold for 3 minutes.

| # | Option | Natural on arena | Older voices | Casual delivery, breaths, laughs | 3 minute consistency | Word timestamps | Price for 10 min | API |
|---|---|---|---|---|---|---|---|---|
| 1 | **Human read + ElevenLabs Voice Changer** (speech-to-speech) | n/a, the prosody is human | any library, designed or cloned voice can be the target | all of it comes from the human read; the tool keeps whispers, laughs, cries and emotional cues (VENDOR, V) | one target voice id for every clip | run forced alignment or local whisper | $1.20 ($0.12 per minute) (V) | ElevenLabs direct, also on fal (S) |
| 2 | **Eleven v4** with a Voice Design voice or a library voice | #1, Elo 1321 | yes: library has older American women, and Voice Design takes age, accent, texture and audio quality in the prompt (V) | inline audio tags, natural-language direction, ellipses and caps (V) | 10,000 characters per call, "context stitching", claims no drift on regenerate (VENDOR) | not confirmed for v4. Forced Alignment API exists as a fallback (V) | $0.80 list, $0.22 until Oct 12 (V) | ElevenLabs direct only. Not on Kie |
| 3 | **Gemini 3.8 Flash TTS with a designed voice** (Google key) | #4, Elo 1275 | yes via prompt-based voice design: vocal age and texture are named control axes (S) | per-turn style text plus 40 inline vocal event tags (V) | persistent `voice_...` id, Google advises short turns (V) | none | about $0.14 (V, computed) | Google AI Studio |
| 4 | **Gemini 3.8 Flash TTS preset voices** (what the pipeline uses now) | #4 | weak: one "Mature" female preset (Gacrux), one "Gravelly" male (Algenib) | same tags and style field | same voice name each call | none | about $0.10 on Kie (MR, computed) | **Kie, works today** |
| 5 | **Cartesia Sonic 3.6** | #3, Elo 1278 | 500+ preset voices, clone from about 10 s (S). Older American woman not verified | emotion list plus `[laughter]` in the transcript (S) | not verified | not verified | about $0.49 | Cartesia direct |
| 6 | **Inworld Realtime TTS-2** | #6, Elo 1251 | clone from 5 to 15 s (S). Presets not verified | inline non-verbal markups such as sigh and laugh (S) | not verified | yes, word and character (S) | about $0.21 to $0.25 | Inworld direct, older model on fal |
| 7 | **Hume Octave 2** | not on the AA top list I saw | voice design by prompt; Hume's own guide uses an elderly woman as its example (S) | "acting instructions" per line (S) | not verified | not verified | about $0.75 on the $14 Creator plan (S) | Hume direct |
| 8 | **MiniMax Speech 2.8 HD** | Elo 1170 | Voice Design endpoint: describe a voice, get a reusable `voice_id`. Clone from about 10 s (S) | parses `(laughs)` and `(sighs)` (S) | not verified | not verified | $1.00 | MiniMax direct, fal. Not on Kie |
| 9 | **Eleven v3 (text-to-dialogue)** | Elo 1169, v3 Conversational 1196 | on Kie only the 67 listed presets, none labeled as an older American woman [doc] | the same audio tag family as v4 | 5,000 characters per call | Kie flag exists on the v2-class models, return shape undocumented [doc] | $0.70 on Kie | **Kie, but returning HTTP 500 today** |
| 10 | **Fish Audio S2.1 Pro** | Elo 1140 | clone from a 5 s sample; community voice library (S) | thousands of natural-language tags (VENDOR, S) | not verified | not verified | about $0.15 | Fish direct |
| 11 | **OpenAI gpt-4o-mini-tts** | not on AA; 19th on Voice Arena | no. 11 to 13 fixed voices; custom voices only for approved customers (S) | plain-English `instructions` field | fixed voice | none | about $0.15 (S) | OpenAI |
| 12 | **Qwen-Audio-3.1-TTS-Plus** | #2, Elo 1292 | not verified | not verified | not verified | not verified | about $0.19 | Alibaba. I found nothing on older American voices or US access |
| 13 | **Open source on the Mac** (Chatterbox, Sesame CSM, Dia2, Higgs Audio, IndexTTS-2, VibeVoice, Orpheus, Kokoro, F5-TTS) | best open weights on AA is Fish S2 Pro at 1121; Kokoro 1063 (S, V) | only by cloning a reference clip of a real older speaker | Chatterbox Turbo: `[laugh]`, `[cough]`, `[chuckle]`; Sesame CSM is built around fillers and breaths (S) | varies | none built in | free | local |

Sources for the table, row by row:

- Voice Changer: (V) https://elevenlabs.io/docs/overview/capabilities/voice-changer, price (V) https://elevenlabs.io/pricing/api, fal endpoint `fal-ai/elevenlabs/voice-changer` (S) https://fal.ai/elevenlabs
- Eleven v4: (V) https://elevenlabs.io/v4, (V) https://elevenlabs.io/docs/overview/models, (V) https://elevenlabs.io/docs/best-practices/prompting, (V) https://testingcatalog.com/elevenlabs-launches-eleven-v4-and-v4-turbo-voice-models, (V) https://wavespeed.ai/blog/ai-comparisons/eleven-v4-vs-v3/
- Gemini 3.8: (V) https://ai.google.dev/gemini-api/docs/speech-generation, voice design axes (S) https://www.orcarouter.ai/blog/gemini-3-8-flash-tts-voice-design-and-deploy, price (V) digitalapplied page
- Cartesia: (S) https://cartesia.ai/blog/sonic-3.6/, (S) https://docs.cartesia.ai/build-with-cartesia/sonic-3
- Inworld: (S) https://docs.inworld.ai/tts, (S) https://howaiworks.ai/blog/inworld-realtime-tts-2-launch-2026
- Hume: (S) https://dev.hume.ai/docs/text-to-speech-tts/prompting, (S) https://dev.hume.ai/docs/voice/voice-design, price (S) https://anotherwrapper.com/tools/llm-pricing/speech-models/octave-2
- MiniMax: (S) https://invideo.io/blog/minimax-ai-voice-models/, price (S) https://platform.minimax.io/docs/guides/pricing-paygo.md
- Fish: (S) https://blog.donweb.com/fish-audio-s21-pro-voz-ia-52-millones/, (S) https://openrouter.ai/fish-audio/s2.1-pro-free:free
- OpenAI: (S) https://developers.openai.com/api/docs/guides/text-to-speech, (S) https://costbench.com/software/voice-apis/openai-tts/
- Open source: Chatterbox (V) https://github.com/resemble-ai/chatterbox; Sesame CSM (S) https://openrouter.ai/sesame/csm-1b/apps; roundups (S) https://www.codesota.com/speech/best-open-source, (S) https://findskill.ai/blog/best-open-source-tts-2026/

Why human read + speech-to-speech ranks first (MR): the four tells that agency writers name are a too-clean read, one tempo all the way through, a hook that sounds like ad copy read aloud, and a salesy tone. (V) Pigeon Digital page. All four live in the performance, not the timbre. Speech-to-speech takes the performance from a person and only swaps the timbre. Its limits: the speech-to-speech models are an older generation (`eleven_multilingual_sts_v2`), a segment tops out at 5 minutes, and someone has to read every script. (V) voice changer doc.

Why the top-ranked Qwen model sits low here (MR): high arena rank, but I found no evidence of older American voices, no practitioner using it for ads, and no simple US signup. Untested, not bad.

### 1.3 Named voices and voice-design prompts for older, ordinary voices

**ElevenLabs library voices (need an ElevenLabs key).** Read from ElevenLabs' own library category pages. Descriptions are paraphrased.

| Voice | Voice id | What the listing says | Fit (MR, not heard) |
|---|---|---|---|
| Grandma Rachel, "Wise Southern Senior" | `0rEo3eAjssGDUCXHYENf` | friendly Southern grandma, storyteller | senior and American, but may lean character or storyteller |
| Vivie, "Sincere and Wise" | `H1GhCI6GEKiSXZcwmUkc` | upbeat mature adult, Midwestern to General American, nonfiction and podcasts | closest listed to an ordinary Midwestern woman |
| Jane, "Professional Audiobook Reader" | `RILOU7YmBhvwJGDGjNmP` | narrator in her 50s, General American | narrator cadence risk |
| Grandma Titina | `UOxKeHS7lixzgw35mtAR` | 70 year old woman, relaxed, multilingual storyteller | accent unknown |
| "The Loving Grandmother" | id not shown | woman in her 70s, slight Midwestern accent, soft and slightly gravelly, unhurried | written like a Voice Design prompt; a useful template |

(V) https://elevenlabs.io/voice-library/grandma, (V) https://elevenlabs.io/voice-library/elderly-female-voices, (S) https://elevenlabs.io/voice-library/grandmother. A matching page for men exists and was not opened: (S) https://elevenlabs.io/voice-library/grandpa.

These are library pages, not practitioner picks. I found no practitioner post that names a specific older-woman voice for ads. The one ad-voice roundup I found recommends younger commercial voices (Bella, Antoni). (S) https://aivoicereview.com/blog/best-elevenlabs-voices-2026

**ElevenLabs Voice Design prompt rules.** (V) https://elevenlabs.io/docs/creative-platform/voices/voice-design

- The prompt can carry age, accent, gender, tone and timbre, pacing, emotion, and audio quality.
- Age words that work: "middle-aged", "elderly", "man in his 80s". Timbre words: gravelly, raspy, airy, warm, mellow.
- Accent: say "thick" or "slight", not "strong". Example from the doc: an older woman with a thick Southern accent, sweet and sarcastic.
- Audio quality is a prompt axis. "Perfect audio quality" and "studio-quality" push clean. The doc also lists intentional low quality: "low-fidelity audio", "poor audio quality", "sounds like a voicemail". Quality phrases can reduce accuracy for niche voices.
- Guidance scale: the doc's examples sit at 20 to 40%. Higher follows the prompt harder and can sound worse.
- Preview text should match the character and be a full sentence or paragraph. Each generation returns three candidates.
- Model ids: `eleven_ttv_v3` (voice design), works with v3 and v4. (V) https://elevenlabs.io/docs/overview/models

Prompts written for this project (MR, untested):

```
A woman in her mid 60s from Ohio with a slight Midwestern accent. Ordinary, not a performer.
Warm, a little dry, slightly husky with a light rasp. Relaxed and conversational, talking to
a friend across the kitchen, uneven pace, trails off at the ends of sentences. Good quality.
```

```
A man in his late 60s from western Pennsylvania. Plain, a little gruff, low and slightly
gravelly, tired but good humored. Talks like he is arguing gently with his wife, not
presenting. Natural pace with small pauses. Good quality.
```

Use "good quality", not "perfect audio quality" (MR): the room and phone character get added in post (section 5), and a studio-perfect designed voice pulls toward narrator polish. Do not ask for low fidelity in the voice itself, because the lip-sync driver needs a clean signal.

**Gemini 3.8 Flash TTS.** Preset descriptors from Google's doc: Gacrux "Mature", Algenib "Gravelly", Zubenelgenubi "Casual", Sulafat "Warm", Vindemiatrix "Gentle", Achird "Friendly", Enceladus "Breathy", Umbriel and Callirrhoe "Easy-going". (V) https://ai.google.dev/gemini-api/docs/speech-generation. Kie's Omni voice list adds gender and pitch for 26 of them: gacrux female mature mid pitch, sulafat female warm mid pitch, vindemiatrix female gentle mid pitch, callirrhoe female easygoing mid pitch, algenib male raspy low pitch, enceladus male breathy low pitch, achird male friendly mid pitch. [doc]

Google's direct API also has prompt-based voice design (`POST /v1beta/voices` with `type="prompted"`, returns a persistent `voice_...` id, up to 200 per project) and an extended voice library that can be filtered by gender, pitch, accent and a "Conversational" context. (V) same Google page. Neither is exposed on Kie. [doc]

**Hume Octave.** Its prompting guide pairs a voice prompt about a calm elderly woman with matching text and says the match between description and text matters. (S) https://dev.hume.ai/docs/text-to-speech-tts/prompting

**Casting rule from the sources.** Pick voices with slight imperfections and conversational energy, not the cleanest professional one. (S) https://influencermarketinghub.com/video-advertising/ai-features-ugc-video-quality/. ElevenLabs' own guide says a serious professional voice may not respond to playful tags, and that a delivery already present in the voice's training audio is easier to reproduce. (V) https://elevenlabs.io/docs/best-practices/prompting. (MR) The current wife voice, Gacrux, is in Kie's "Professional" group. That alone may explain part of the narrator feel.

---

## 2. What is reachable through Kie today

### 2.1 Routes that need only a Kie key

| # | Route | Status | Older voice? | Notes |
|---|---|---|---|---|
| K1 | `google/gemini-3-8-flash-tts` (and `-lite`) | **works** | Gacrux (female, mature), Algenib (male, raspy, low). 70 presets, no design, no cloning | Per-turn `style` free text, inline tags such as `<breath>`, `<sigh>`, `<chuckle>`, `<short pause>`, `temperature` 0 to 2. About $0.10 per 10 minutes (MR: $6.30 per 1M audio tokens [doc] times roughly 25 tokens per second, which is implied by Google's $9 per 1M tokens equal to $0.0135 per minute (V) digitalapplied page). Output is 24 kHz mono (V) Google doc |
| K2 | `google/gemini-3-1-flash-tts`, `google/gemini-2-5-pro-tts` | works | same 30 core presets | Different control surface: `scene`, `sample_context`, per-speaker `audio_profile`, required `accent` (`American (Gen)`, `American (South)`, `American (Valley)`), `style` (`Empathetic`, `Deadpan`, `Vocal Smile`...), `pace` (`Natural`, `The Drift`...). Bracket tags. Lower arena rank (1202) but more persona control. Worth one A/B against K1 (MR). About twice the K1 price [doc] |
| K3 | `elevenlabs/text-to-dialogue-v3` | **HTTP 500 for 12+ hours** | no older American woman among the 67 presets by name | Eleven v3 with audio tags. `stability` only 0, 0.5, 1. 5,000 characters. $0.70 per 10 minutes [doc] |
| K4 | `elevenlabs/text-to-speech-multilingual-v2`, `-turbo-2-5` | HTTP 500 | same 67 | `stability`, `similarity_boost`, `style`, `speed` 0.7 to 1.2, `previous_text` and `next_text`, `timestamps`. $0.60 and $0.30 per 10 minutes [doc] |
| K5 | Native audio with a voice reference: `kling-3.0/video` and `kling-3.0-omni/*` (`element_input_audio_urls`, 5 to 30 s) | available per docs, untested here | whatever the reference clip is | The voice is bound to a named character element [doc]. See section 3 |
| K6 | Native audio with reference audio: `bytedance/seedance-2-5` (up to 10 clips, 30 s total), `bytedance/seedance-2*` (3 clips, 15 s), `wan/3-0-video` and `-prime` (5 clips, 15 s), `minimax-h3/reference-to-video` (3 clips, 15 s), `wan/2-7-r2v` (`reference_voice`, 1 to 10 s) | available per docs, untested here | whatever the reference clip is | Reference audio cannot be combined with first or last frame on Seedance and Wan 3.0 [doc] |
| K7 | Gemini Omni voices: `POST /api/v1/omni/audio/create` then `audio_ids` on `gemini-omni-video` or `google/gemini-omni-flash-1-1` | available per docs, untested | preset id (for example `gacrux`, `algenib`) plus a free-text `voice_description` up to 20,000 characters | Does not accept an audio file. It is a described voice on a preset base [doc] |
| K8 | Native audio, no reference: `veo-3-1` | works | described in the prompt only | A new voice every generation. No audio input [doc] |
| K9 | Hybrid: best Gemini TTS take used as the reference clip for K5 or K6 | untested | yes | (MR) The video model re-performs the line in that timbre with room acoustics that match the picture. See 3.4 |

Preview without spending credits: every Kie ElevenLabs preset has a public sample at `https://static.aiquickdraw.com/elevenlabs/voice/<voice_id>.mp3` [doc]. I confirmed one URL returns HTTP 200 audio. Those 67 files can be run through `tools/video/voice_profile.py` and the section 6 stack now, so a shortlist is ready when the endpoint comes back. By name only (MR, not heard), the candidates to profile first are Jessica Anne Bogart "Chatty and Friendly" (`g6xIsTj2HwM6VR4iXFCw`), Tiffany "Natural and Welcoming" (`6aDn1KB0hjpdcocrUkmq`), Monika Sogam "Deep and Natural" (`2zRM7PkgwBPiau2jvVXc`), Adeline "Feminine and Conversational" (`5l5f8iK3YPeGga21rQIX`) for her, and Mark "Natural Conversations" (`UgBBYS2sOqTuMpoF3BR0`), Spuds Oxley "Wise and Approachable" (`NOpBlnGInO9m6vDvFkFC`), Wyatt "Wise Rustic Cowboy" (`YXpFCvM1S3JbWEJhoskW`) for him.

**Not routes to a speaking voice on Kie:**

- Suno `ai-music-api/create-voice` and the persona endpoints build a SINGING voice. The flow needs the user to record a server-issued validation phrase in their own voice, and the doc recommends singing it. The resulting id feeds `ai-music-api/generate` as `persona_id`. It is not text to speech and cannot make a stranger's voice. (V) https://docs.kie.ai/suno-api/suno-voice-generate.md, (V) https://docs.kie.ai/suno-api/suno-voice-validate.md
- No ElevenLabs voice changer, voice design, cloning, speech-to-text or forced alignment. No MiniMax Speech, Fish, Hume, Cartesia or OpenAI TTS. No whisper. [doc] and (V) https://docs.kie.ai/llms.txt

### 2.2 Kie chat models with audio INPUT (for a listening judge)

Verified from the doc pages. Not called, so behavior is unconfirmed.

**OpenAI-style Gemini endpoints.** Paths: `/gemini-2.5-pro/v1/chat/completions`, `/gemini-3-pro/v1/chat/completions`, `/gemini-3.1-pro/v1/chat/completions`, `/gemini-3-7-flash-openai/v1/chat/completions` on `https://api.kie.ai`, Bearer auth. The docs state that images, videos, audio and documents all use the same content part: `type` is always `"image_url"` and only the `url` changes. (V) https://docs.kie.ai/market/gemini/gemini-3-1-pro.md, (V) https://docs.kie.ai/market/gemini/gemini-2-5-pro.md, (V) https://docs.kie.ai/market/gemini/gemini-3-7-flash-openai.md

```
POST https://api.kie.ai/gemini-3.1-pro/v1/chat/completions
Authorization: Bearer <KIE_API_KEY>
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": [
      {"type": "text", "text": "Clip A then clip B, same sentence. Which one sounds more like an unscripted phone recording of a real person? Answer A or B, then one line of evidence."},
      {"type": "image_url", "image_url": {"url": "https://<public-url>/ab_concat.wav"}}
    ]}
  ],
  "stream": false,
  "reasoning_effort": "high"
}
```

Caveats: the same pages carry a feature card that says "text and image inputs", which conflicts with the audio sentence. The response includes `credits_consumed`; per-token prices for chat models are not in the Kie reference. The URL must be public (use the Kie file upload API [doc]). Spend one cheap call to confirm audio is really heard: ask it to transcribe the clip.

**Native-style Gemini endpoints.** `POST https://api.kie.ai/gemini/v1/models/gemini-3-7-flash:streamGenerateContent` (also `gemini-3-6-flash`, `gemini-3-5-flash`). `contents[].parts[]` accepts `text`, `inline_data` (`mime_type` + base64 `data`), and `file_data` (`mime_type` + `file_uri`). The only mime example is `image/jpeg`; audio is not mentioned. The page says to authenticate with the `X-Goog-Api-Key` scheme while the spec's security block is Bearer. (V) https://docs.kie.ai/market/gemini/gemini-3-7-flash.md. (MR) Try `inline_data` with `audio/wav` here if the OpenAI-style route does not hear audio.

GPT pages on Kie (`/codex/v1/responses`) and Claude pages were not found to mention audio input. (V) local grep of https://docs.kie.ai/market/chat/gpt-6-1-sol.md and gpt-5-5.md.

### 2.3 Routes that need another key

Price is for about 10,000 characters or 10 minutes.

| Provider | What it unlocks | About 10 min | Older American woman out of the box? | Where |
|---|---|---|---|---|
| **ElevenLabs direct** | Eleven v4, v3, Voice Design, voice library (17,500+ voices (VENDOR)), Voice Changer, Forced Alignment, Scribe | v4 $0.80 list ($0.22 until 10-12), v3 $0.80, Voice Changer $1.20. Starter plan $6 per month (V) | **Yes.** Library voices in 1.3, or design one | https://elevenlabs.io/pricing/api |
| **Google AI Studio** | Gemini 3.8 Flash TTS with voice design, extended voice library, voice replication (needs a recorded consent statement from the voice owner (V) digitalapplied page) | about $0.14 through 2026-12-31, doubling on 2027-01-01 (V) | Gacrux preset; a designed voice by prompt | https://ai.google.dev/gemini-api/docs/speech-generation |
| **fal.ai** | Resells ElevenLabs v3 (`fal-ai/elevenlabs/tts/eleven-v3`, $0.10 per 1K), voice changer and forced alignment (S), MiniMax Speech 2.8 HD (`fal-ai/minimax/speech-2.8-hd`, $0.10 per 1K), Chatterbox ($0.025 per 1K), Index TTS 2 ($0.002 per second), Qwen3-TTS, Gemini 3.1 Flash TTS. Eleven v4 on fal not confirmed | $0.25 to $1.20 | Only through the ElevenLabs or cloning endpoints. Whether fal passes arbitrary ElevenLabs library voice ids is not verified | (V) https://fal.ai/learn/tools/best-text-to-speech-apis, (S) https://fal.ai/elevenlabs |
| **MiniMax direct** | Speech 2.8 HD and Turbo, Voice Design, rapid cloning ($1.50 per voice) | $1.00 HD, $0.60 Turbo (S) | Not verified. Voice Design can make one | (S) https://platform.minimax.io/docs/guides/pricing-paygo.md |
| **Cartesia** | Sonic 3.6, 500+ voices, instant clone | about $0.49; Pro plan $5 per 100K credits (V) digitalapplied | Not verified | (S) https://cartesia.ai/blog/sonic-3.6/ |
| **Hume** | Octave 2, voice design by prompt, acting instructions, voice conversion | about $0.75; Creator $14 per month (S) | Not as a preset that I verified. Designable | (S) https://hume.ai/text-to-speech |
| **Fish Audio** | S2.1 Pro, 5 s cloning, community voices, a free tier model on OpenRouter | about $0.15 (S) | Not verified | (S) https://fish.audio/ja/blog/s2-1-pro-free-api/ |
| **Inworld** | Realtime TTS-2, cloning, word timestamps | about $0.21 to $0.25 (S) | Not verified | (S) https://docs.inworld.ai/tts |
| **OpenAI** | gpt-4o-mini-tts with `instructions` | about $0.15 (S) | **No.** Fixed younger-sounding presets; custom voices are gated | (S) https://developers.openai.com/api/docs/guides/text-to-speech |
| **Local, no key** | Chatterbox (MIT, `pip install chatterbox-tts`, Python 3.11, runs on MPS) and others | free | Only by cloning a clip of a consenting older speaker | (V) https://github.com/resemble-ai/chatterbox |

Consent note: every cloning route (ElevenLabs instant clone, MiniMax, Fish, Inworld, Chatterbox, Google replication) needs a real person's recording. Use only a person who agreed to it. Library and designed voices avoid the issue.

---

## 3. Native-audio route (voice generated with the picture)

Prompt anatomy for each video model is already in `prompting-workflows.md` sections 1.1 to 1.5. This section covers only the voice.

### 3.1 How real the voices sound, according to practitioners

- An AI UGC tool vendor's Seedance guide says ElevenLabs' best voices are cleaner and more controllable than Seedance's own voice, and that native audio wins on lip-sync precision and speed. It recommends native audio for fast test variants and short UGC, and TTS overdub for premium work or a custom voice. (VENDOR, V) https://ugccopilot.ai/blog/seedance-2-native-audio-generation-guide/
- A comparison article says reviewers rate Kling's audio below Veo 3.1's, that Kling can produce overlapping voices with three or more speakers, and that Veo has no voice-cloning equivalent while Kling Omni can bind a 5 to 30 second sample. It cites no test data of its own. (V) https://invideo.io/blog/kling-3-vs-veo-3-1/
- Roundup sites describe Veo 3.1 dialogue as natural and Kling dialogue as sometimes slightly robotic next to it. (S) https://www.3daistudio.com/blog/best-ai-video-generator-2026
- From Ryan's X follows (`x-notes.md`, their claims, unverified): 0xROAS did not like Seedance 2.5 lip-sync at first and later praised its audio reference mode; he flagged "voice issues" on an unnamed strong lip-sync model. pounddz says Omni beats Seedance for yappers over 30 seconds.
- A changing voice from clip to clip is called the single biggest tell of AI video in the source already cited in `prompting-workflows.md` section 2.6.

(MR) "Cleaner" is not the goal here. The native route's real advantage for this job is that the voice, the room sound and the mouth are generated together, so the acoustics match the kitchen with no post work. Its real cost is identity drift, changed words and timing errors, which the audio-first pipeline was built to avoid. I found no blind test of native voices against TTS for realism.

### 3.2 How to prompt the voice

- Attach the voice description to the line, not floating elsewhere, and put the line in quotes. Veo guides use forms like: a gravelly voice saying "...". (S) https://magichour.ai/blog/how-to-prompt-for-speaking-in-veo-3
- Seedance: the form already in this project, `Dialogue (NAME, voice description, accent): "line"`, plus an audio line. A vendor guide's working audio line asks for ambient room tone, faint kitchen sounds, no music, and a clear conversational voice with single-take phone recording quality. (VENDOR, V) ugccopilot page.
- Seedance 2.5 voice lock, from the seedance.tv guide (third-party site that presents itself as official): keep a fixed "voice identity card" with four audible traits (timbre, vocal age, accent, pace in words per minute), repeat it word for word in every shot, name the speaker, and write "says exactly:" before the quoted line. Conflicting adjectives and extreme emotion cause accent and age shifts. (V) https://www.seedance.tv/blog/how-to-keep-voices-consistent-in-seedance-2-5
- Kling: name the speaker plainly, give the line, add a delivery note (for example "in a relaxed tone", "sighs and says"). Use simple grammar and break long sentences into short lines. (VENDOR, V) https://kling.ai/blog/kling-video-3-omni-native-lip-sync-audio-guide
- State the accent in every prompt. Say "no music" in every prompt. (VENDOR, V) ugccopilot page.

Voice card written for this project (MR, untested):

```
VOICE LOCK, CAROL: woman, 66, Ohio, slight Midwestern accent. Slightly husky, warm, a little
dry. Unhurried, about 150 words per minute, small pauses, ends of sentences drop. Ordinary
person talking to her phone, not performing. Never change accent, pitch range, or vocal age.
```

### 3.3 Keeping ONE voice across 10+ clips

| Method | How | Limits | Source |
|---|---|---|---|
| Kling 3.0 / Omni element voice | Bind a clean single-speaker clip to the character element (`element_input_audio_urls`, 5 to 30 s on Kie), then reference `@name` in every prompt | Kling's own blog says a clip of at least 3 s, or a 3 to 8 s character video, clean with no overlapping voices or loud music | [doc], (VENDOR, V) kling.ai page above |
| Seedance 2.5 / 2.0 reference audio | Same approved reference file on every generation, bound to the speaker in the prompt (`@Audio1` paired with `@Image1`) | It is a style guide, not a clone: tone, pace, accent and register carry, the exact voice does not. One test found mic texture and room echo from the reference leak into the output, and that telling the model to use the reference for speaker identity only and to drop mic distance, echo, hiss and hum reduced it. Best reference: 7 to 15 s, one speaker, dry, steady level, neutral emotion, no splices | (V) https://clipdance.ai/blog/seedance-2-consistent-voice, (V) https://genflick.com/blog/seedance-voice-consistency-audio-reference-2026-05-03, (V) seedance.tv page |
| Seedance black-screen video trick | Convert the audio into a black-screen video and pass it as a video reference, which reportedly makes the output follow the source audio's rhythm more closely than an audio reference | From a search summary of an X article that I could not open (HTTP 402). Unverified | (S) https://x.com/GumVue/article/2066700181161001277 |
| Wan 3.0, MiniMax H3, Wan 2.7 r2v | `reference_audio_urls` (refer to it as `Audio1` in the Wan prompt) or `reference_voice` | Docs only. I found no practitioner test of voice hold on these | [doc] |
| Gemini Omni | Create a voice once from a preset id plus description, attach `audio_ids` to a character, pass `character_ids` | Not a clone of any file | [doc] |
| ElevenLabs Voice Changer over the stitched audio | Generate all clips, cut them in order, export the dialogue track, run it once through Voice Changer with one target voice, lay it back in sync | Needs an ElevenLabs key (not on Kie). 5 minutes per segment. `remove_background_noise=true` strips ambience, so re-lay room tone after. Timing is preserved, so lip-sync holds (MR, from the doc's description) | (S) https://www.tiktok.com/@ai.for.real.life/video/7537477893442538766, (S) https://ai-for-real-life.beehiiv.com/p/the-secret-to-consistent-characters-in-veo-3-and-how-to-fix-the-voices-too, (V) voice changer doc |
| Keep the real audio | Use a real video as the performance reference and write the original audio back over the result | This is what one of the most-followed Claude Code ad skills does. It needs a real source recording | `x-notes.md` (mikefutia ad multiplier, 0xROAS video-reference swap) |

### 3.4 What goes wrong

- **A new voice per generation** on models without a reference (Veo). Accent and tone shift when a scene is extended. (S) TikTok and beehiiv pages above.
- **Rushed or mistimed lines** when the line is too long for the clip. Budgets: about 12 words per 10 s and 20 per 15 s on Seedance (VENDOR, V) ugccopilot page; 15 words or fewer per 8 s on Veo (`prompting-workflows.md` 1.1).
- **Wrong mouth timing** from dense lines or competing actions; two voices merging when the speaker is ambiguous; an extension that sounds like a new person when the reference or room tone changes. (V) seedance.tv page.
- **Changed words.** Native models paraphrase or drop words. No source gave a rate. (MR) Since the script is fixed and graded, every native clip needs a local whisper transcript check against the script before it is kept.
- **Reference contamination.** Phone or noisy references carry their artifacts into every clip. (V) genflick page.
- **Auto music and subtitles.** Covered in `prompting-workflows.md` 1.10.
- **Speech-to-speech cleanup strips the room.** Plan to re-add room tone.

(MR) Where native audio fits this pipeline: short two-person drama lines where acting and in-room sound matter more than exact timing. For a 60 to 180 second single-speaker yapper with a fixed script, audio-first TTS or speech-to-speech stays the safer base. The hybrid K9 (a TTS take as the voice reference for Kling or Seedance) is worth one bake-off clip because it needs only the Kie key.

---

## 4. Script-side and delivery techniques

**Constraint for this project: the script's words are fixed and graded.** Everything in 4.1 changes delivery only. Everything in 4.2 changes or adds words and is labeled NEEDS SCRIPT PERMISSION.

### 4.1 Allowed without changing words

**Punctuation and casing**

- Ellipses add a pause and weight. Capital letters add emphasis. Standard punctuation sets rhythm, and it matters more on v4 than before. (V) https://elevenlabs.io/docs/best-practices/prompting. Caps for emphasis also work on v3 per a UGC tool's guide (VENDOR, V) https://superscale.ai/learn/sound-effects-emotions/ and on Gemini per Google (V) speech-generation doc.
- On Gemini, period-separated fragments come out choppy. Join tagged clauses with commas, use ellipses for a trailing pause and a long dash for a micro-pause mid-thought. This is from a guide written for Gemini 3.1. (V) https://livekit.com/blog/gemini-3.1-flash-tts-prompting-guide. This file uses "..." or a tag in its examples.
- Put a comma before plosive-heavy words to give the model a natural pause point. (S) https://www.michydev.com/elevenlabs-voice-settings/
- Spell numbers and symbols as spoken words ("sixty-six", "forty-two dollars"). The spoken words do not change. ElevenLabs normalizes by default but recommends doing it yourself for phone numbers, currency and dates. (V) ElevenLabs prompting doc.

**Pauses**

- Eleven v3 and v4 do not support SSML break tags. Use tags and punctuation. Tags listed on ElevenLabs pages: `[pause]`, `[short pause]`, `[long pause]`. (V) ElevenLabs prompting doc, (V) https://elevenlabs.io/v4
- Gemini 3.8: `<short pause>`, `<long pause>`. (V) Google doc, [doc]

**Non-verbal tags (they add sounds, not words)**

- ElevenLabs v3 and v4, from the official guide: `[laughs]`, `[chuckles]`, `[sighs]`, `[exhales]`, `[exhales sharply]`, `[inhales deeply]`, `[clears throat]`, `[whispers]`, `[muttering]`, `[snorts]`, `[swallows]`, `[gulps]`, plus state tags such as `[curious]`, `[annoyed]`, `[thoughtful]`, `[surprised]`. (V) ElevenLabs prompting doc.
- A UGC tool vendor's v3 test: action tags (whispering, giggles, pause, sighs, laughs, coughs) land reliably. Emotion tags (sad, sarcastic, friendly, curious, and also exhales in their test) were inconsistent. (VENDOR, V) superscale page. (MR) Prefer action tags and test `[exhales]` before relying on it.
- Tags work best when that delivery is already in the voice. A professional voice may ignore playful tags. (V) ElevenLabs prompting doc.
- Gemini 3.8 on Kie: `<breath>`, `<heavy breath>`, `<exhales>`, `<sigh>`, `<chuckle>`, `<laugh>`, `<throat-clearing>`, `<tsk>`, `<phew>`, `<pff>`, `<gasp>`, `<groan>`, `<snort>`, `<yawn>`, `<whispers>`. [doc]
- Chatterbox Turbo: `[laugh]`, `[cough]`, `[chuckle]`. (V) Chatterbox README.
- MiniMax 2.8: `(laughs)`, `(sighs)`. (S) invideo MiniMax page.
- (MR) Budget: at most one non-verbal per 2 to 3 sentences. A sigh on every line is its own tell. For a 60+ audience keep laughs short.

**Stability, style, speed**

- Eleven v3 has three stability modes: Creative (more expressive, can hallucinate), Natural (balanced, closest to the reference), Robust (most stable, less responsive to tags). (S, summary of ElevenLabs' guide) https://elevenlabs.io/docs/best-practices/prompting, (V) https://hackernoon.com/how-to-keep-an-ai-voice-consistent-across-every-video-clip. On Kie's `text-to-dialogue-v3` that is `stability` 0, 0.5, 1. [doc]. (MR) Use 0.5. Use 0 only for a line that needs a big reaction, and check the words with whisper.
- v2-class models (Multilingual v2, Turbo 2.5), creator-reported settings: stability 30 to 40, similarity 75 to 80, style 15 to 25, speed 0.95 to 1.05. (V) michydev page. An agency post gives stability about 40, lower similarity, style about 10, and speed 1.1 to 1.2. (V) Pigeon Digital page. The two disagree on speed. (MR) For a 66 year old speaker stay at 0.95 to 1.0: conversational rate falls from about 194 words per minute at age 20 to about 169 at 60 (H) https://pmc.ncbi.nlm.nih.gov/articles/PMC2943985.
- High stability (85% and up) with zero style is the usual cause of robotic output. (S) https://neuraplus-ai.github.io/blog/best-settings-for-elevenlabs-ai-voice-quality-improvement-2026.html
- Write down the settings and keep them fixed for a character across the whole ad. Batch all of one character's lines in one session. (V) hackernoon page.

**Chunking and takes**

- One creator generates in about 20 second chunks and joins them, because output degrades past about 30 seconds on some models. (V) michydev page.
- ElevenLabs says v4 handles 10,000 characters in one generation with consistent pacing. (VENDOR, V) elevenlabs.io/v4. An older summary of the v3 guide said prompts over 250 characters are more stable than very short ones. (S)
- Google's advice for Gemini 3.8: split long content into shorter turns instead of writing stronger style prompts, set the persona once in the voice, and do not tell the model to "keep the same timbre". (V) Google doc.
- On Kie's ElevenLabs v2-class models, pass `previous_text` and `next_text` when a script is split, so each chunk is spoken with context. [doc]
- (MR) House rule: generate per beat (2 to 4 sentences, about 150 to 400 characters), not per sentence and not in one pass. Per-sentence calls reset pitch and energy at every sentence start, which is a measurable tell. One pass leaves no room to pick takes. Make 3 to 5 takes per beat (Gemini `temperature` 1.0 to 1.3), score them with section 6, keep the winner, and check every kept take against the script with whisper.

**Direction for Gemini (style prompt)**

- Gemini 3.8 treats `text` as a verbatim transcript. Stage directions inside the text get spoken. All direction goes in the `style` field. (V) Google doc.
- For 3.1 and 2.5 Pro: use the structure Audio Profile, Scene, Director's Notes (style, accent, pace), then the transcript. A concrete scene beats a role label. Do not over-specify. Regional accent detail beats a generic label. (V) https://dev.to/googleai/how-to-prompt-gemini-31s-new-text-to-speech-model-24bb
- Words to avoid in direction (3.1 guide): quiet, flat, monotone, no rush, careful. They produce a monotone, AI-like read. Use positive wording. Never quote words from the transcript inside the direction. (V) LiveKit guide.
- (MR) Announcer cadence comes from three habits: a pitch lift at the start of every sentence, even stress on every content word, and a tidy fall at every period. Direct against all three with a scene, not with adjectives: who she is talking to, what she is doing with her hands, that she is mid-thought.

**Direction for gpt-4o-mini-tts**

- The `instructions` field steers accent, emotional range, intonation, speed and tone. Keep it to a few sentences. (S) https://developers.openai.com/api/docs/guides/text-to-speech. The voices themselves are fixed and none is an older speaker, so this is a poor fit for the job. (MR)

### 4.2 NEEDS SCRIPT PERMISSION (changes or adds words)

- Filler words and restarts ("um", "you know", "I mean", starting a sentence twice). Named as the main missing ingredient by both agency posts, and Google's own best practice for conversational Gemini output is to write the disfluencies into the transcript. (V) Pigeon Digital page, (V) Z2A page, (V) Google doc. Older speakers use more "uh" fillers, so this fits the character. (H) PMC2943985.
- Kie's `filler_words: true` on Gemini 3.8 (two-speaker calls only) lets the model insert fillers by itself. It changes the words. [doc]
- Contractions and spoken respellings ("going to" to "gonna", "I am" to "I'm").
- Rewriting a hook that reads like ad copy so it sounds like an answer to a friend. (V) Pigeon Digital page.
- Backchannels in dialogue: Gemini 3.8 supports a listener's short reaction inside pipes in the other speaker's turn. That adds spoken words. (V) Google doc.

### 4.3 Before and after

The single-speaker sample line comes from this project's own prompt notes (`prompting-workflows.md` 1.3). The two-person lines are invented for illustration. None of it is from a graded script.

**Before (reads like an announcer):**

```
style: "Warm and friendly."
text:  "My daughter sent me this. I rolled my eyes. Then I tried it."
```

**After, Gemini 3.8 on Kie, same words:**

```json
{
  "speaker_id": "Speaker 1",
  "style": "A 66 year old woman from Ohio talking to her phone, which is propped on the kitchen counter while she dries a mug. She is mid-thought and a little amused at herself. Uneven, unhurried pace with small pauses while she finds the words. Her voice drops at the ends of sentences. She is telling one friend, not presenting.",
  "text": "My daughter sent me this... <short pause> I rolled my EYES, <chuckle> then I tried it."
}
```

**After, Eleven v3 or v4, same words:**

```
[exhales] My daughter sent me this... I rolled my EYES. [chuckles] Then I tried it.
```

**NEEDS SCRIPT PERMISSION version:**

```
So my daughter sent me this, and... I rolled my eyes. I did. And then I, um, I tried it.
```

**Two-person kitchen argument, Gemini 3.8, same words, direction only:**

```json
[
  {"speaker_id": "Speaker 2", "style": "Man in his late 60s, half listening, reading the mail at the kitchen table. Low, a little gruff, short on patience. Starts before he has fully decided what to say.", "text": "<sigh> You paid HOW much for that?"},
  {"speaker_id": "Speaker 1", "style": "His wife, 66, at the counter with her back half turned. Quick, dry, a step ahead of him. Not angry, just done with the question.", "text": "Less than your fishing trip, <short pause> so sit down."}
]
```

---

## 5. Post-processing: make a clean TTS voice sound like an iPhone in a kitchen

All commands below were run by a helper agent on this Mac (ffmpeg 8.1.1 from Homebrew) on test speech. Levels and alignment were measured. **Nothing was judged by ear.** (MR) This fixes the "recorded in a studio" tell. It does not fix a flat read.

### 5.1 The rule that protects lip-sync

**Drive the lip-sync model with the DRY voice. Swap in the processed voice at the final mux.** SyncNet-style confidence drops with background noise and Wav2Lip-style models are less accurate on noisy speech. (S) https://towardsdatascience.com/syncnet-paper-easily-explained/, (S) https://arxiv.org/pdf/2012.10852. The chain below adds at most 1 sample of delay, so the processed file lines up with the dry one.

### 5.2 Recommended chain (medium)

Input 0 is the dry TTS file. Input 1 is a room impulse response (IR). Output is WAV, so AAC is encoded only once, at the mux.

```bash
ffmpeg -i voice.wav -i ir.wav -filter_complex "
[1:a]aresample=48000,pan=mono|c0=c0,silenceremove=start_periods=1:start_threshold=-30dB,atrim=end=0.8,afade=t=out:st=0.5:d=0.3[ir];
[0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono,highpass=f=110,equalizer=f=220:t=q:w=0.9:g=-3,volume=volume='1+0.07*sin(2*PI*t/7.3)+0.04*sin(2*PI*t/2.9)':eval=frame,asplit=2[dry][tofir];
[tofir][ir]afir=dry=1:wet=1:irnorm=2[wet];
[dry][wet]amix=inputs=2:weights='1 0.45':normalize=0:duration=first[room];
anoisesrc=color=pink:amplitude=0.012:r=48000:seed=11,highpass=f=80,lowpass=f=6000[n];
[room][n]amix=inputs=2:weights='1 1':normalize=0:duration=first,equalizer=f=3200:t=q:w=1.0:g=2.5,lowpass=f=11000,acompressor=threshold=0.089:ratio=3:attack=12:release=250:knee=4:makeup=1.6,asoftclip=type=tanh:threshold=0.85,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[out]" -map "[out]" -c:a pcm_s16le voice_room.wav

ffmpeg -i lipsynced.mp4 -i voice_room.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -ar 48000 -shortest final.mp4
```

Measured on test speech: -16.3 LUFS, peak -1.5 dBFS, noise in the pauses about 29 dB under active speech, offset against the dry file -4 samples (0.08 ms).

What each step does:

| Step | Purpose |
|---|---|
| IR prep (`silenceremove`, `atrim=end=0.8`, fade) | puts the IR's direct spike at sample 0 so the wet path does not comb-filter against the dry path, and caps the tail at 0.8 s |
| `highpass=f=110` and -3 dB at 220 Hz | removes close-mic chest warmth that would not exist at arm's length. iOS itself applies a high-pass and gain control on the mic (S) https://forum.juce.com/t/disable-agc-and-highpass-filter-on-ios/12812 |
| `volume=...:eval=frame` | about plus or minus 1 dB of slow level drift, like a hand-held or propped phone |
| `afir` with `irnorm=2`, mixed at 0.45 | the room. See the afir notes below |
| pink noise at amplitude 0.012, band-limited | placeholder room tone, mixed BEFORE the compressor so it rises in the pauses the way phone gain control behaves |
| +2.5 dB at 3.2 kHz, `lowpass=f=11000` | phone-mic presence and bandwidth. The 1 to 4 kHz consonant band is left intact |
| `acompressor` 3:1, attack 12 ms, release 250 ms | light phone-style gain control |
| `asoftclip=type=tanh:threshold=0.85` | slight saturation on peaks |
| `loudnorm=I=-16:TP=-1.5` then `aresample=48000` | level. `loudnorm` upsamples internally to 192 kHz, so resample after it (S) https://lists.ffmpeg.org/pipermail/ffmpeg-cvslog/2017-August/108680.html |

House loudness note: `prompting-workflows.md` 6.4 masters the finished ad to -14 LUFS. Keep that as the final master step. The -16 here is the voice stem. Third-party platform targets conflict, from -10 to -16, and Meta publishes no LUFS target (it manages loudness with xHE-AAC metadata on the client). (H) https://engineering.fb.com/2023/04/11/video-engineering/high-quality-audio-xhe-aac-codec-meta/

### 5.3 Light, medium, heavy

| Preset | Wet weight in `amix` | Noise amplitude | Compressor ratio | Lowpass | Measured pause noise under speech | Direct-to-reverb (calculated, synthetic IR) |
|---|---|---|---|---|---|---|
| Light | 0.25 | 0.006 | 2 | 13000 | 37 dB | about +16 dB |
| **Medium** | 0.45 | 0.012 | 3 | 11000 | 29 dB | about +11 dB |
| Heavy | 0.80 | 0.025 | 4 | 9000 | 23 dB | about +8 dB |

(MR) Ship Medium for a 60+ audience. Do not ship Heavy.

### 5.4 afir and other ffmpeg facts verified locally

- `afir`'s `dry` and `wet` are input and output GAINS, not a mix control. A real dry and wet balance needs `asplit` plus `amix`, as above.
- With the default `irnorm=1` the reverb came out about 32 dB under the input, close to inaudible. `irnorm=2` gives roughly unity. `irnorm=-1` applies the raw IR (13 dB hot in the test). `irnorm=0` was unusable.
- `gtype` still parses in 8.1.1 and did nothing. ffmpeg 6.x documents `gtype` and has no `irnorm`, so this command fails on 6.x. (H) https://raw.githubusercontent.com/FFmpeg/FFmpeg/release/6.1/doc/filters.texi, https://raw.githubusercontent.com/FFmpeg/FFmpeg/release/7.1/doc/filters.texi, https://ffmpeg.org/ffmpeg-filters.html
- The IR must be resampled to the voice's rate (the chain does this).
- Delay added, click test at 48 kHz: highpass, lowpass, equalizer, acompressor, aecho, afir, asoftclip, dynaudnorm, speechnorm, loudnorm: 0 to 1 sample. `alimiter`: 5 ms unless `latency=1`. `firequalizer`: 10 ms at its default. AAC round trip through `.m4a`: 0. AAC round trip through a raw ADTS pipe: 21.3 ms (1,024 samples).
- `anoisesrc` level: pink or brown at amplitude 0.01 is about -54 dBFS RMS, 0.02 is about -48, 0.05 is about -40. White is about 9 dB hotter.
- In zsh, `${var}:a` style text inside a filtergraph string can expand as a path modifier. Brace shell variables.

### 5.5 Impulse responses and room tone (free)

| Source | License | Files | Notes |
|---|---|---|---|
| **MIT IR Survey** (Traer and McDermott, 271 real rooms) | CC BY 4.0 per a Hugging Face mirror's license file. The MIT page states no license | Kitchens: `h012_Kitchen_22txts.wav`, `h018_Kitchen_12txts.wav`, `h054_Kitchen_3txts.wav`, `h111_Kitchen_1txts.wav`, `h191_Kitchen_1txts.wav` (names from the mirror listing; the official zip was not opened) | (H) https://mcdermottlab.mit.edu/Reverb/IR_Survey.html, zip https://mcdermottlab.mit.edu/Reverb/IRMAudio/Audio.zip (11.7 MB), mirror https://huggingface.co/datasets/hashdoa/MIT_environmental_impulse_responses. Originals are 32 kHz |
| **Freesound, CC0** | CC0 | "Small House Kitchen" IR, 0.44 s, 48 kHz stereo. "IR - UK kitchen - Balloon pop", 192 kHz mono, 8.4 s (the `atrim` handles it) | (H) https://freesound.org/people/djericmark/sounds/724559/, https://freesound.org/people/Sadiquecat/sounds/867837/ |
| **Freesound room tone, CC0** | CC0 | quiet apartment kitchen with fridge, 25.6 s, 48 kHz | (H) https://freesound.org/people/kyles/sounds/637796/ |
| OpenSLR 28 (RIRS_NOISES) | Apache 2.0 | 1.3 GB, 16 kHz, no kitchens | (H) https://www.openslr.org/28/ |
| Aachen AIR | MIT | meeting room, stairway, corridor | (H) https://www.iks.rwth-aachen.de/en/research/tools-downloads/databases/aachen-impulse-response-database |
| BUT ReverbDB | CC BY 4.0 | offices, hotel room | (H) https://speech.fit.vut.cz/software/but-speech-fit-reverb-database |
| C4DM (Queen Mary) | CC BY-NC-SA | non-commercial, do not use for ads | (S) |

Real room tone instead of generated noise: add `-stream_loop -1 -i roomtone.flac` as input 2 and replace the `anoisesrc` line with `[2:a]aresample=48000,pan=mono|c0=c0,volume=-20dB[n]`. The -20 dB is an untested starting value. Adjust until the pauses sit about 30 dB under speech.

(MR) Prefer real room tone over generated noise, for a measurable reason: Gemini TTS is 24 kHz, so after upsampling there is nothing above 12 kHz. A real phone recording has energy in that top octave. Full-band recorded room tone fills it. Generated brown noise is also spectrally featureless, with no fridge hum (60 and 120 Hz in the US) and no small household sounds.

**Zero-download IR (tested, same levels and alignment):** replace `-i ir.wav` with

```bash
-f lavfi -i "aevalsrc='if(eq(n\,0)\,1\,0)+if(eq(n\,139)\,0.45\,0)+if(eq(n\,254)\,-0.35\,0)+if(eq(n\,389)\,0.3\,0)+if(eq(n\,595)\,0.24\,0)+if(eq(n\,859)\,-0.18\,0)+0.05*(random(0)*2-1)*exp(-6.908*t/0.40)*gt(n\,480)':s=48000:d=0.6"
```

That is a direct spike, five early reflections and a 0.4 s decaying noise tail.

**No-IR fallback with `aecho` only (tested: -16.4 LUFS, 28 dB, 0 lag, output 112 ms longer):**

```bash
ffmpeg -i voice.wav -filter_complex "
[0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono,highpass=f=110,equalizer=f=220:t=q:w=0.9:g=-3,volume=volume='1+0.07*sin(2*PI*t/7.3)+0.04*sin(2*PI*t/2.9)':eval=frame,aecho=1.0:0.85:7|13|19|29|41:0.30|0.24|0.19|0.13|0.09,aecho=1.0:0.95:23|37|53|71:0.16|0.12|0.09|0.06[room];
anoisesrc=color=pink:amplitude=0.012:r=48000:seed=11,highpass=f=80,lowpass=f=6000[n];
[room][n]amix=inputs=2:weights='1 1':normalize=0:duration=first,equalizer=f=3200:t=q:w=1.0:g=2.5,lowpass=f=11000,acompressor=threshold=0.089:ratio=3:attack=12:release=250:knee=4:makeup=1.6,asoftclip=type=tanh:threshold=0.85,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[out]" -map "[out]" -c:a pcm_s16le voice_room.wav
```

`aecho` taps are single echoes, so this gives early reflections with no diffuse tail. The synthesized IR is the better fallback. (MR)

**pyroomacoustics kitchen (not installed here, untested):** a 3.5 x 4.0 x 2.5 m shoebox, `pra.inverse_sabine(0.45, dim)` for the absorption, source and mic 0.6 m apart, `room.compute_rir()`, write `room.rir[0][0]` normalized at 48 kHz. API reference: (H) https://pyroomacoustics.readthedocs.io/en/pypi-release/pyroomacoustics.room.html

### 5.6 What a real iPhone kitchen recording is (for calibration)

- Video mode selects different mics and applies beamforming noise reduction. (H) https://developer.apple.com/library/ios/qa/qa1799/_index.html (old, iPhone 5 era)
- Older iPhone mics were unusable below about 200 Hz. (H) https://www.faberacoustical.com/blog/?p=178
- Furnished kitchens and bedrooms run about 0.1 to 0.4 s RT60. (S) https://arxiv.org/pdf/2509.26140. Real-room reverb decays slowest between 200 and 2,000 Hz. (H) https://pmc.ncbi.nlm.nih.gov/articles/PMC5137703
- A living room is about 40 dBA, a fridge 40 to 43, conversation 55 to 65. (S) https://dbskeptic.com/learn/decibel-chart/
- (MR, calculated) A 3.5 x 4 x 2.5 m kitchen with absorption 0.15 to 0.25 gives RT60 of about 0.57 to 0.34 s by Sabine. Critical distance is then about 0.5 m, so a phone at arm's length really sits near 0 to +3 dB direct-to-reverb, and real speech-to-noise at that distance is roughly 25 to 35 dB. The presets are deliberately drier than reality to protect intelligibility.
- Not found: an authoritative iPhone video AAC bitrate, the stereo default, or the exact video-mode EQ.

**Best calibration (MR):** take one real iPhone clip of someone talking in a kitchen, run `ffprobe`, `ebur128`, `astats` and `voice_profile.py` on it, and tune the chain until the processed TTS matches those numbers. That calibrates without ears.

**The reference method is not ffmpeg.** Playing the voice out of a speaker and re-recording it on a phone in the real room is the film technique called worldizing. (H) https://filmsound.org/terminology/worldizing.htm. A forum thread recommends the same for AI voices, along with cutting below 150 Hz, rolling off above 7 to 8 kHz and room tone near -35 dB. (S) https://www.blackhatworld.com/seo/ai-voices.1841480/. It cannot be automated, but one re-recorded file is the best measurement target for the ffmpeg chain. If Ryan plays a 30 second TTS take from a laptop and records it on his iPhone in his kitchen, the result is both a calibration file and a candidate deliverable. Re-recorded audio is no longer sample-aligned, so align it back to the dry file by cross-correlation before the mux.

### 5.7 Steps that can hurt

- **Lip-sync scoring:** noise and reverb on the driver. Solved by 5.1. Avoid `firequalizer`, uncompensated `alimiter`, and ADTS pipes, which shift timing. Re-check alignment by cross-correlating the processed file against the dry one.
- **Listeners over 60:** age-related hearing loss hits high consonants (s, t, th, f, k) and speech in noise first. (S) https://www.medlink.com/articles/presbycusis. In a classic study, listeners around 72 scored well under young adults in reverberant speech, and young adults were unaffected at 0.4 s. (S, primary not opened: Nabelek and Robinson 1982). (MR) Keep pause noise at least 25 dB under speech, keep the tail under 0.5 s, never cut 1 to 4 kHz, and do not go below `lowpass=9000`.
- **Low-bitrate AAC "generation loss" trick:** skip it. The platform re-encodes anyway and stacking generations costs consonant clarity. If it is ever used on the Heavy preset, round-trip through a `.m4a` file so no delay is added. (MR)
- **Bit crushers, exciters, tremolo:** left out. They add artifacts a phone does not make. (MR)
- **Captions still carry the ad.** A large share of Facebook video is watched muted (85% in a 2016 report). (S) https://digiday.com/media/silent-world-facebook-video/

### 5.8 Evidence that this works

Thin. Two agency posts recommend room tone, breaths and speech-to-speech and give no settings. (V) Z2A page, (V) Pigeon Digital page. The paid plugin equivalent is Audio Ease Speakerphone. (VENDOR, S) https://www.audioease.com/speakerphone/. No A/B data was found showing that room treatment makes AI voices pass as real, and nothing usable from Reddit (blocked to this tool) or X.

---

## 6. Machine judges of realism

All of this section's facts were gathered by a helper agent that opened each source. **Bottom line first: no single score tracks "sounds like a real person". The best-supported setup compares candidates against real reference clips, adds an audio-LLM A/B judge, and calibrates everything against clips Ryan has already passed or failed.**

### 6.1 Synthetic-speech detectors

| Model | License | How to run | Reported numbers |
|---|---|---|---|
| `SpeechAntiSpoofingBenchmarks/DF_Arena_1B_V_1` | "other" | `pipeline("antispoofing", model=..., trust_remote_code=True)`, 16 kHz. Reads only the first 64,600 samples (about 4 s), so window long takes | mean EER 3.66% over 24 sets, 0.91% on In-the-Wild, 17.34% on ASVspoof5 (H) https://huggingface.co/SpeechAntiSpoofingBenchmarks/DF_Arena_1B_V_1 |
| `nii-yamagishilab` AntiDeepfake family (`wav2vec-large-anti-deepfake-nda`, `mms-300m-anti-deepfake`, `xls-r-1b-anti-deepfake`) | CC BY-NC-SA 4.0 | needs `fairseq==0.12.2`, 16 kHz, any length | 2.25% on In-the-Wild, 30.06% on Deepfake-Eval-2024 (H) https://huggingface.co/nii-yamagishilab/wav2vec-large-anti-deepfake-nda |
| `Gustking/wav2vec2-large-xlsr-deepfake-audio-classification` | Apache 2.0 | `pipeline("audio-classification")` | 4.01% EER on an ASVspoof2019 subset (H) https://huggingface.co/Gustking/wav2vec2-large-xlsr-deepfake-audio-classification |
| `MelodyMachine/Deepfake-audio-detection-V2`, `mo-thecreator/Deepfake-audio-detection`, `HyperMoon/wav2vec2-base-960h-finetuned-deepfake` | Apache 2.0 | same | 98 to 99.98% accuracy on small or unnamed sets. In-distribution toys (MR) |
| AASIST (`clovaai/aasist`) | MIT | research code, PyTorch 1.6 era | 0.83% EER on ASVspoof2019 LA (H) https://github.com/clovaai/aasist |
| SSL-AASIST (`TakHemlata/SSL_Anti-spoofing`) | MIT | pins Python 3.7 and a fairseq commit, painful on 3.11 | 0.82% LA, 2.85% DF on ASVspoof 2021 (H) https://github.com/TakHemlata/SSL_Anti-spoofing |

Commercial: Resemble DETECT-3B Omni is API or on-prem only, no public weights (VENDOR, H) https://www.resemble.ai/detect-3b-omni/. The ElevenLabs classifier is a web tool that detects ElevenLabs audio only and says it does not reliably classify Eleven v3 (VENDOR, H) https://elevenlabs.io/ai-speech-classifier. Reality Defender has a Python SDK with 50 free detections a month (VENDOR, H) https://docs.realitydefender.com/sdks/quickstart.

How far to trust them: **low.**

- On real-world 2024 deepfakes, off-the-shelf AASIST scored an AUC of 0.43 (worse than chance), RawNet2 0.53. The best commercial system reached 0.93. (H) https://arxiv.org/html/2503.02857v4
- The best open system averages 13.84% EER across 14 sets, and reverb raises error by half. (H) https://arxiv.org/html/2509.02859v1
- Playing audio through a speaker and re-recording it moves a wav2vec2-AASIST detector from 4.7% to 18.2% EER. (H) https://arxiv.org/abs/2505.14862
- Detectors hold up to noise and are vulnerable to compression, neural codecs most of all. (H) https://arxiv.org/abs/2503.17577
- No detector type generalizes across 2024 to 2025 TTS systems. (H) https://arxiv.org/html/2601.20510v1
- **No study was found that correlates detector score with human naturalness ratings.** In a 2026 study humans caught 71% of fakes while a detector stayed above 94.5%. They are doing different jobs. (H) https://arxiv.org/abs/2605.26136
- Gemini audio carries a SynthID watermark and Chatterbox output carries Resemble's PerTh watermark. (V) digitalapplied page, (V) Chatterbox README. Both are inaudible by design and say nothing about how human the read sounds.

(MR) A detector score is an artifact flag. The kitchen chain will lower "probability fake" without making the performance any more human, so score the DRY take, and use the score only as a tiebreak.

### 6.2 MOS predictors

| Tool | Install | Measures |
|---|---|---|
| UTMOSv2 | `pip install git+https://github.com/sarulab-speech/UTMOSv2.git` (MIT) | naturalness MOS of synthetic speech (H) https://github.com/sarulab-speech/UTMOSv2 |
| UTMOS22 | `torch.hub.load("tarepan/SpeechMOS:v1.2.0","utmos22_strong",trust_repo=True)` (MIT) | same, older, no fairseq (H) https://github.com/tarepan/SpeechMOS |
| NISQA | clone `gabrielmittag/NISQA`; weights CC BY-NC-SA | `nisqa.tar`: quality, noisiness, coloration, discontinuity, loudness. `nisqa_tts.tar`: TTS naturalness (H) https://github.com/gabrielmittag/NISQA |
| DNSMOS | `pip install "torchmetrics[audio]"` | P.808, signal, background, overall (S) https://lightning.ai/docs/torchmetrics/latest/audio/deep_noise_suppression_mean_opinion_score.html |
| torchaudio SQUIM | in torchaudio | objective: STOI, PESQ, SI-SDR estimates. Subjective: MOS. Still listed in the 2.9 docs; 2.9 moved file loading to TorchCodec, so load with soundfile (H) https://docs.pytorch.org/audio/2.9.0/pipelines.html |
| SCOREQ | `pip install scoreq` (MIT) | MOS for natural or synthetic domains (H) https://github.com/alessandroragano/scoreq |
| Distill-MOS | `pip install distillmos` (MIT) | small quality MOS model (H) https://github.com/microsoft/Distill-MOS |
| Audiobox Aesthetics | `pip install audiobox_aesthetics` (CC BY 4.0) | production quality, complexity, enjoyment, usefulness (H) https://github.com/facebookresearch/audiobox-aesthetics |
| VERSA | `pip install git+https://github.com/wavlab-speech/versa.git` (MIT) | wrapper for 90+ metrics (H) https://github.com/wavlab-speech/versa |

What they do not measure: whether it sounds like a real casual person. They reward clean studio audio, so the kitchen chain will LOWER the score while the clip gets more believable. They are also saturated: in one benchmark's human test four TTS systems beat the real recordings, UTMOS and UTMOSv2 fell below 0.4 correlation with humans on in-the-wild speech, NISQA went negative, and DNSMOS averaged 0.25. (H) https://arxiv.org/html/2506.19441v2. UTMOSv2's system-level correlation with humans was 0.118 on modern zero-shot TTS. (H) https://arxiv.org/abs/2603.24430. Existing predictors show low or negative correlation with conversational naturalness. (H) https://arxiv.org/abs/2603.01467

Use: a floor gate to reject glitched takes. Never rank on it.

### 6.3 Distribution comparison against real speech (best fit)

**TTSDS2.** `pip install ttsds` (v2.1.3, MIT, Python 3.10 to 3.12, needs `numpy<2`, ffmpeg and sox). It compares distributions of self-supervised speech features, speaker features, prosody (F0, rate) and ASR features between a set of your clips and a set of real reference clips, scored 0 to 100. It was the only one of 16 metrics above 0.5 Spearman with human ratings in every domain (0.50 to 0.75, average 0.67). (H) https://github.com/ttsds/ttsds, https://arxiv.org/html/2506.19441v2. Limit: it wants 50 to 100 clips per set, so it ranks voices, engines and settings, not single takes.

### 6.4 Prosody and acoustic statistics per take

Libraries (function names from memory, not re-checked this session):

- Pitch, jitter, shimmer, HNR, cepstral peak prominence: `praat-parselmouth` (`snd.to_pitch()`, `parselmouth.praat.call(...)`), `librosa.pyin`, `pyworld.harvest`.
- Standard feature set: `opensmile.Smile(feature_set=opensmile.FeatureSet.eGeMAPSv02)`.
- Pauses: `silero-vad` gaps. Rate and fillers: `faster-whisper` with `word_timestamps=True` (the pipeline already runs whisper).
- Room and noise, blind: `pyannote/brouhaha` gives per-frame SNR and C50 (gated model). (H) https://huggingface.co/pyannote/brouhaha
- Already in the repo: `tools/video/voice_profile.py` measures gap quietness, room on the voice, bandwidth, and pitch and pace movement.

Targets for real older American speakers:

| Measure | Real value | Source |
|---|---|---|
| Median pitch, women in their 60s | about 195 Hz in phone conversations; 175 to 186 Hz postmenopausal in a meta-analysis; 198 Hz for healthy women 66 to 75 in one study. Aim for 170 to 200 Hz (MR) | (H) https://languagelog.ldc.upenn.edu/nll/?p=31786, https://pmc.ncbi.nlm.nih.gov/articles/PMC7426883, https://bibliotekanauki.pl/articles/1397305.pdf |
| Median pitch, men in their 60s | about 115 Hz, 120 Hz in the 70s | (H) Language Log page |
| Speaking rate | about 169 words per minute at 60 in conversation, down from 194 at 20, and falling further after the 60s | (H) https://pmc.ncbi.nlm.nih.gov/articles/PMC2943985, https://www.ldc.upenn.edu/sites/default/files/interspeech2006-towards-integrated-understanding.pdf |
| Fillers | "uh" rate rises with age | (H) PMC2943985 |
| Best age markers | tempo, duration and pause measures were more reliable than jitter and shimmer, where the evidence is mixed | (H) https://www.isca-archive.org/interspeech_2007/bruckl07_interspeech.pdf |

What to compare (MR): F0 median and F0 spread in semitones, words per minute per beat and its variance ACROSS beats, pause length distribution (real speech has a long tail of 0.4 to 1.2 s thinking pauses, a flat TTS read has uniform short ones), sentence-initial pitch reset size, and cepstral peak prominence. Flag any take whose pace variance or pause distribution is far tighter than the reference. That is the metronome the agency post describes.

Free real reference audio: Buckeye (40 Ohio speakers, half over 40, conversational, non-commercial research use) (H) https://www.buckeyecorpus.osu.edu; Santa Barbara Corpus (CC BY-ND) (H) https://linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english; CORAAL (CC BY-NC-SA) (H) https://oraal.uoregon.edu/CORAAL; Common Voice (CC0, age labels, but read speech). These are for measurement only, not for use in ads. (MR) The best reference set is 50 to 100 real phone testimonial clips of women 60 to 75, because they match the channel and the register. The agency's ad library pulls already contain those.

### 6.5 An audio LLM as a listening judge

- AudioJudge (tested on GPT-4o audio and Gemini 1.5 to 2.5 Flash): pairwise beats pointwise scoring, and concatenating the clips into one audio with 4 in-context examples works best. System-level Spearman with human preference reached 0.91 to 0.93. It shows position and verbosity bias and is weak on paralinguistics (speaking-rate judgments: humans 77.8%, model 55.3%). `pip install audiojudge`. (H) https://arxiv.org/html/2507.12705v1, https://github.com/Woodygan/AudioJudge
- Gemini 2.5 Flash and Qwen2-Audio gave negative results as zero-shot TTS evaluators. (H) https://arxiv.org/abs/2604.08562
- Judges trail humans by 32 points on paralinguistic pairs and fail on ties. (H) https://arxiv.org/abs/2606.24648
- One model often picks the same slot regardless of order in concatenated A/B. (H) https://arxiv.org/abs/2607.13477
- Audio LLMs are ineffective at zero-shot deepfake detection. (H) https://arxiv.org/abs/2505.11079
- No evidence was found for the newest Gemini 3.x or GPT realtime models as judges. Everything above is on older models.

Prompt pattern (MR, built from those findings): A/B the candidate against a REAL reference clip in one concatenated file. Run both orders and 3 to 5 repeats and take the majority. Give a rubric of named cues: pause placement, fillers, pitch reset at sentence starts, breath, lengthening at the ends of sentences, room match. Include 4 labeled examples from Ryan's past verdicts. Do not ask "is this AI" and do not ask for a 1 to 5 score. Kie route: section 2.2.

### 6.6 Recommended scoring stack

| # | Component | Runs on | Use | Trust |
|---|---|---|---|---|
| 1 | **Calibration set**: 30 to 50 clips Ryan has passed or failed, plus 50+ real reference clips | n/a | compute each component's rank correlation with his verdicts. Without this the stack is unvalidated | this is what makes the rest worth anything |
| 2 | **TTSDS2** against the real reference set | CPU, own venv (`numpy<2`) | choose engine, voice and settings | moderate. Best evidence available |
| 3 | **Prosody distance per take** (z-scores against the reference: F0 median and spread, words per minute and its variance, pause distribution, filler rate, CPP) | parselmouth + whisper + `voice_profile.py` | reject too-fast, too-flat, no-pause takes | moderate for catching bad takes |
| 4 | **Audio-LLM A/B judge**, both orders, voted | Kie Gemini chat (2.2) or Google direct | coarse ranking of the survivors | moderate for coarse ranking, low for fine prosody |
| 5 | **Detector pair on the DRY take** (`DF_Arena_1B_V_1` plus one nii model, windowed) | CPU; fairseq models in their own venv or skipped | tiebreak only | low |
| 6 | **Channel match on the FINAL mix** (Brouhaha SNR and C50, bandwidth, DNSMOS background) aimed at the reference range, not maximized | CPU | confirm the room sounds like a phone in a kitchen | good for the room, says nothing about the voice |
| 7 | **Floor gate** (UTMOSv2 or SQUIM MOS on the dry take) | CPU | reject glitched or garbled takes | fine as a gate, never as a rank |
| 8 | **Script check**: whisper transcript equals the graded script | already in the pipeline | reject any take with a changed word | high |

Apple Silicon notes (MR, untested here): run everything on CPU first. Expect unsupported MPS ops in wav2vec2-family models, so set `PYTORCH_ENABLE_MPS_FALLBACK=1`. The fairseq-dependent models are the install risk on Python 3.11.

**How far to trust the whole stack:** it will reliably reject clearly bad takes and it will pick better engines, voices and settings on average. It will not reliably pick the best of several good takes, and it cannot certify that a voice sounds real. A wrong-sounding voice can pass every number. Ryan's ear is the final gate, so make his grading cheap: one page with 6 to 8 candidates on the same 20 second passage, plus one real clip mixed in blind.

---

## 7. What AI UGC ad makers do for voice

Sources are thin and mostly vendors. Nothing here is a controlled test.

- **Arcads** (AI actor ad tool): every AI actor runs on ElevenLabs voices through the API. The founder says the two things to nail are the visuals and the voice. Over a billion ad impressions claimed. (VENDOR, V, dated 2025-06-16) https://elevenlabs.io/blog/arcads. A search summary also says Arcads offers speech-to-speech from the user's own recording. (S)
- **HeyGen** connects ElevenLabs voices to its avatars. (VENDOR, S) https://elevenlabs.io/blog/how-heygen-uses-elevenlabs-to-deliver-lifelike-voice-for-ai-video
- **Pose AI** builds ElevenLabs cloning into its UGC flow and argues one cloned voice across all clips is the point. (VENDOR, V) https://pose.ai/blog/ai-ugc-videos-voice-cloning
- **AdGPT / Icon** offer speech-to-speech: record the read, and the tool keeps the pacing and tone in a chosen voice. (S) https://help.icon.com/articles/4136243376-speech-to-speech
- **Pigeon Digital** (agency, Feb 2026): after 40+ AI actor variations underperformed for a skincare brand, their fix is speech-to-speech from a casual human read. Fallback TTS settings: speed 1.1 to 1.2, stability about 40, lower similarity, style about 10. (V) https://www.pigeondigital.com/insight/ai-ugc-sounds-fake-speech-to-speech-fix-believable-avatars
- **Z2A Digital** (agency, Aug 2026): ground the avatar with a real human voice recording as the reference, add breaths, mid-sentence thinking pauses, "uhs and ums", and room tone. Watch for lines cut off mid-sentence. (V) https://www.z2adigital.com/blog-content/make-ai-ugc-human
- **Common published stack**: image model, then a video model, then ElevenLabs for the voiceover, then CapCut. (S) https://adlibrary.com/guides/how-to-create-ai-ugc-ads-that-convert
- **Veo creators**: generate clips with a short voice and accent description, stitch, then run the whole dialogue track through ElevenLabs Voice Changer so every clip has one voice, and add ambient sound after. (S) https://www.tiktok.com/@ai.for.real.life/video/7537477893442538766
- **ElevenLabs settings shared by a short-form creator**: v3, stability 35, similarity 78, style 20, speaker boost on, speed 0.96, a cloned personal voice, 20 second chunks. (V) https://www.michydev.com/elevenlabs-voice-settings/
- **From Ryan's X follows** (`x-notes.md`, their claims): the Dec 2025 to Mar 2026 talking-head stack was a still image, a voice from MiniMax audio or an ElevenLabs clone, then InfiniteTalk or Hedra. The current wave leans on native audio in Omni and Seedance 2.5, and on swapping a character into a REAL viral video while keeping its timing, lip movements and, in one skill, its original audio.

(MR) The pattern across all of it: the realistic end of AI UGC keeps a human somewhere in the voice chain. It is either a cloned real voice, a human read converted by speech-to-speech, or the audio of a real video. Pure text-to-speech with a stock voice is the cheap end and it is the end people complain about.

Compliance, one line: Kie-side and platform rules on AI people and testimonials are covered in `prompting-workflows.md` section 5.1. Cloning any real person's voice needs their consent.

---

## 8. Bottom line: three routes to try first

Realism figures are my estimates on Ryan's 10 point scale. Nothing was heard. Treat them as an ordering, not a promise.

### Route 1. Fix what is already built. Kie key only, today.

- **What:** stay on Gemini 3.8 Flash TTS and change four things. (a) Recast: profile all 70 Kie voices with `voice_profile.py`, shortlist women at 170 to 200 Hz and men near 115 Hz, starting outside Kie's Professional and Commercial Voiceover groups. Test Sulafat (warm), Vindemiatrix (gentle) and Callirrhoe (easygoing) against Gacrux; Algenib (raspy, low), Enceladus (breathy, low) and Achird (friendly) against Zubenelgenubi. These picks come from the descriptor words only. None was heard. (b) Direct with a concrete scene in `style` and delivery marks in `text` (section 4.3), per beat, 3 to 5 takes. (c) Run the section 5 chain with a real kitchen IR and real room tone, driving lip-sync from the dry file. (d) One A/B against `google/gemini-3-1-flash-tts` with `audio_profile`, `scene` and `accent`.
- **Expected realism:** 6 to 7 of 10. The room mismatch and the casting are fixable. A read-aloud cadence will partly remain.
- **Cost:** about $0.10 per 10 minutes of speech, more with multiple takes. Zero new accounts.
- **Needs from Ryan:** a blind listen to a short shootout page. Ideally one real iPhone clip of anyone talking in a kitchen, to calibrate the chain.

### Route 2. ElevenLabs direct. One $6 key unlocks the two strongest options.

- **2a, Eleven v4 with a designed 66 year old voice.** Voice Design prompt from 1.3, three candidates per generation, Ryan picks by ear once, then the voice id is locked for every ad. v4 is number 1 on the arena, takes audio tags, and 10,000 characters per call. Then the same section 5 chain. Word timing from the Forced Alignment API or the existing local whisper.
  - Expected realism: 7.5 to 8.5 of 10.
  - Cost: $0.80 per 10 minutes at list price ($0.22 until 2026-10-12). Starter plan $6 per month.
- **2b, human read plus Voice Changer** for the ads that matter most. Anyone reads the script casually into a phone, word for word. Voice Changer maps the read onto the locked older voice. Segments of up to 5 minutes.
  - Expected realism: 8.5 to 9.5 of 10. It is the only route where the pacing, restarts and breaths are human.
  - Cost: $1.20 per 10 minutes. Costs a human 3 minutes of reading per ad, so it is not fully one-shot.
- **Needs from Ryan:** an ElevenLabs account and API key (https://elevenlabs.io/pricing/api), one voice pick per character, and for 2b a read.

### Route 3. Google AI Studio key: Gemini 3.8 with a designed voice. Then one native-audio bake-off.

- **3a:** the same model the pipeline already uses, but called through Google so prompt-based voice design is available (`POST /v1beta/voices`, `type="prompted"`). Design "woman, 66, Ohio, slightly husky" once, reuse the `voice_...` id. Smallest code change of any new-key route.
  - Expected realism: 7 to 8 of 10.
  - Cost: about $0.14 per 10 minutes through 2026-12-31.
  - Needs from Ryan: a Google AI Studio key and one voice pick.
- **3b, Kie only:** one bake-off clip of the hybrid in 2.1 (K9). Bind the best Route 1 take as the voice on a Kling 3.0 Omni element, or pass it as Seedance 2.5 reference audio, and let the video model speak the line in the room. Check the words with whisper. Worth it mainly for the two-person kitchen argument, where in-room acting matters most. Expect drift and some changed words.

### What I would not do first

- Chase arena rank by swapping engines while keeping a dry mix and a narrator-style preset. The current engine already ranks number 4.
- Trust a detector's "probability real" as the grade. It measures artifacts, and the kitchen chain moves it for the wrong reason.
- Add fillers or restarts without script permission. They are the most-recommended fix in the agency posts, and they change graded words. Ask Ryan for a standing rule on them.

### Open questions this research could not close

1. Whether Eleven v4 supports the `with-timestamps` endpoints. Not confirmed. Forced alignment covers it either way.
2. Whether Kie's Gemini chat endpoints really process audio. The docs say yes in one place and "text and image" in another. One cheap call settles it.
3. Whether fal passes arbitrary ElevenLabs library voice ids, and whether Eleven v4 is on fal yet.
4. Current TTS Arena V2 (Hugging Face) numbers. The page did not render.
5. Any blind human test of native video-model voices against TTS for realism. None found.
6. Reddit was not reachable from the research tools, so Reddit practitioner opinion is missing from this file.
