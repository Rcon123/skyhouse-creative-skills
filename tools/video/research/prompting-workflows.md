# AI Video Ad Prompting and Workflows

Research date: 2026-10-04. Lane: everything except lip-sync models (prompting, consistency, shot design, editing, pipelines).
Target: direct-response video ads, 9:16, 30 seconds to 3 minutes, older health and beauty buyers, generated through Kie.ai, assembled with ffmpeg + Python.

## 0. Read this first

### How to read the labels

- **(V)** verified: the page was fetched and read during this research. The fetch tool returns a summary of the page, so re-check any exact parameter name or string against the live page before hardcoding it.
- **(S)** seen in search results only. The page was not opened.
- **(MR)** my read: my own inference or recommendation, not a sourced fact.

### About the example prompts

Every example prompt in this file is written fresh for a health and beauty direct-response use case, using the syntax each source documents. They are not copied from the sources. Under each model there is a "real examples live here" list that links to the pages holding the original prompts. This was a deliberate choice to stay clear of reproducing other people's text, and it is the one place this file departs from the brief.

### What changed since the brief was written (verify before building)

1. **Sora 2 is gone.** The consumer app closed 2026-04-26 and the API was switched off 2026-09-24 with no replacement model listed. (V) https://invideo.io/blog/sora-ai-video-generator/ and (S) https://pasqualepillitteri.it/en/news/18764/openai-sora2-api-dismessa-en. The Kie docs index read on 2026-10-04 has no Sora entry at all. (V) https://docs.kie.ai/llms.txt. Do not build a Sora route. No Sora characters or cameos.
2. **There is no Veo 4.** Veo 3.1 is still Google's Veo flagship. Google's 2026 video launch was a separate family, **Gemini Omni** (Omni Flash in May 2026, Omni 1.1 Flash on 2026-08-27). (V) https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides and (S) https://videogen.io/best-ai-video-models
3. **Kling:** 3.0 (February 2026), 3.0 Omni (also called O3), and V3 Turbo are live. Kling 4.0 was not released as of 2026-09-27. (V) https://wavespeed.ai/blog/ai-comparisons/kling-4-0-vs-veo-3-1-vs-seedance-2-5/
4. **Seedance:** 2.5 is live on Kie with 4 to 30 second clips. 2.0, 2.0 Fast and 2.0 Mini are also listed. (V) https://docs.kie.ai/market/bytedance/seedance-2-5.md
5. **Wan:** 3.0 (public beta 2026-08-06) and 3.0 Video Prime (a high-speed variant) are on Kie, alongside 2.7. (V) https://docs.kie.ai/market/wan/3-0-video.md and (S) https://datanorth.ai/news/alibaba-launches-wan3-0-video-model
6. **Image models on Kie:** Nano Banana 2, Nano Banana 2 Lite, Nano Banana Pro, Seedream 5.0 Pro / Flash / Lite, GPT Image 2 and 2.5, Qwen3, Flux-2. (V) https://docs.kie.ai/llms.txt
7. **Also on Kie:** Grok Imagine Video 1.5 Preview, MiniMax H3, HappyHorse 1.1, PixVerse V6, OmniHuman 1.5, InfiniteTalk, Kling AI Avatar, Runway Aleph, Topaz video upscale, ElevenLabs TTS and dialogue. (V) https://docs.kie.ai/llms.txt

### Kie model map (from the Kie request schemas, read 2026-10-04)

| Model | Kie model id seen in schema | Clip length | Resolution | Reference inputs | Prompt cap | Notes |
|---|---|---|---|---|---|---|
| Veo 3.1 | `veo-3-1` (docs also name `veo3_fast`, `veo3_lite` tiers) | 4, 6, 8 s | 720p, 1080p, 4k | 1 or 2 images as first / last frame, or 1 to 3 reference images | not stated | Reference mode (`REFERENCE_2_VIDEO`) only on Fast and Lite, and only at 8 s. Extend via `veo/extend` with the original `task_id`. 1080P renders cannot be extended. |
| Kling 3.0 | `kling-3.0/video` | 3 to 15 s | std 720p, pro 1080p, 4K | first and last frame in `image_urls`, up to 3 `kling_elements` (2 to 4 images each, optional voice audio 5 to 30 s) | 500 chars per shot in multi-shot | `multi_shots` with up to 5 shots, each 1 to 12 s. `sound` boolean. Element tag costs 37 chars. |
| Kling 3.0 Omni | reference-to-video endpoint | 3 to 15 s | 720p, 1080p, 4k | up to 7 reference images | 3,072 chars | Up to 6 custom shots. `audio` boolean. |
| Seedance 2.5 | `bytedance/seedance-2-5` | 4 to 30 s, or -1 for auto | 480p, 720p, 1080p | first / last frame OR up to 30 images + 10 videos + 10 audio (not both) | 30,000 chars | `generate_audio`, `return_last_frame`. |
| Seedance 2.0 | `bytedance-seedance-2` page | 4 to 15 s | 480p, 720p (higher tiers mentioned) | up to 9 images | see doc | Cheaper. Fast and Mini tiers exist. |
| Wan 3.0 | `wan/3-0-video`, `wan/3-0-video-prime` | 2 to 30 s, or -1 | 480P, 720P, 1080P | first / last frame OR up to 10 images + 5 videos + 5 audio | 20,000 chars | Refs named Image1, Video1, Audio1 in the prompt. `audio` default true. `seed`. |
| Gemini Omni | `gemini-omni-video`, Omni 1.1 Flash endpoint | 4, 6, 8, 10 s | 720p, 1080p, 4k | up to 7 images, or first / last frame, plus `character_ids` and `audio_ids` | 20,000 chars | Characters are created once with a portrait + optional body image and reused by id. |
| Grok Imagine Video 1.5 Preview | `grok-imagine-video-1-5-preview` | 1 to 15 s | 480p default, 720p, 1080p | up to 7 images (1 at 1080p) | 4,096 chars | Image-led. |
| Nano Banana 2 | `nano-banana-2` | image | 1K, 2K, 4K | up to 14 input images | 20,000 chars | 9:16 supported. |
| Nano Banana Pro | `nano-banana-pro` | image | 1K, 2K, 4K | up to 8 input images on Kie | 10,000 chars | |
| Seedream 5.0 Pro edit | `seedream/5-pro-image-to-image` | image | basic 1K, high 2K | up to 10 input images | 5,000 chars | |
| Topaz video upscale | `topaz/video-upscale` | n/a | 1x, 2x, 4x | video up to 50 MB | n/a | |

Sources: (V) the `.md` pages under https://docs.kie.ai/market/ and https://docs.kie.ai/veo3-api/generate-veo-3-video.md

Three schema facts that shape the whole skill:

- **No negative prompt field** on the Kie schemas for Veo 3.1, Kling 3.0, Seedance 2.0 / 2.5, Wan 3.0, Gemini Omni or Grok. Only the Wan 2.7 endpoints expose one. Every exclusion has to be written into the prompt text. (V) Kie schemas above.
- **First-frame mode and reference mode are mutually exclusive** on Seedance 2.5, Wan 3.0 and Gemini Omni. You pick one per clip. Kling 3.0 is the exception: it takes a start frame and elements together. (V) Kie schemas above.
- **Prices move.** Snapshot from August 2026: Veo 3.1 Fast about $0.30 to $0.40 per 8 s clip, Veo 3.1 Quality about $1.28, Kling 3.0 std about $0.07 per second, Seedance 2.0 about $0.057 per second on Kie. (V) https://www.bitdoze.com/kie-ai-video-generation/. Check https://kie.ai/pricing before budgeting.

---

## 1. Per-model prompt anatomy that works now

### 1.0 Rules that hold for every model

- **Write a shot brief, not a keyword list.** Every current guide says the same thing: full sentences that read like directions to a camera operator. (V) https://fal.ai/learn/tools/how-to-use-kling-3-0-pro, (V) https://fal.ai/learn/tools/seedance-2-0-prompting-guide, (V) https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n
- **One action per clip.** Break a sequence (walk to door, open it, walk through) into separate clips. Lead with the shot type. (V) https://runway.com/resources/ai-video-prompting-guide
- **Describe motion as countable beats** (four steps, pause, turn in the last second), not vague verbs. (V) https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide
- **Separate subject motion from camera motion** into different sentences. (V) https://runware.ai/docs/models/bytedance-seedance-2-5/guides/prompting
- **Always name the audio.** If audio is unspecified, models add music on their own. Say what you want to hear and say no music. (V) https://aivideosensei.com/prompts/veo-3-prompt-library, (V) https://fal.ai/learn/tools/seedance-2-0-prompting-guide
- **Image-to-video prompts describe what changes, not what is in the picture.** Re-describing the person invites face drift. (V) https://dxbuilder.io/blog/how-to-create-realistic-phone-footage-ai-ugc-230926, (V) https://kling.ai/quickstart/image-to-video-guide
- **Positive phrasing for camera behavior.** Runway warns that naming an unwanted thing (camera shake) can summon it. Say smooth, locked camera. Keep hard exclusions for text, subtitles and music, where every other guide says explicit negation works. (V) https://runway.com/resources/ai-video-prompting-guide
- **Prompt length (MR, from mixed sources):** 60 to 120 words for a single shot. One published agent skill uses 50 to 90 words and reports prompts above 280 words start contradicting themselves. (V) https://github.com/0xadvait/ai-video-skill. Long structured prompts (300 to 400 words) are only for 15 to 30 second multi-beat Seedance or Wan generations. (V) https://blog.segmind.com/we-made-a-30-second-micro-drama-in-one-seedance-2-5-generation-full-test-output/

### 1.1 Veo 3.1

**Official structure:** Cinematography + Subject + Action + Context + Style and Ambiance. (V) https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1

**Audio syntax (official):** dialogue attributed to a speaker, sound effects prefixed `SFX:`, background prefixed `Ambient noise:`. (V) same Google page.

**Timestamp prompting (official):** `[00:00-00:02] ...` blocks, one shot per block, each with its own camera, subject and action. Google's own example runs four 2-second blocks in one 8 second clip. (V) same Google page.

**Negatives (official):** describe the absence inside the scene description, not a bare ban list. (V) same Google page.

**Dialogue rules that creators report:**

- Google's guide puts lines in quotation marks. Creators report that quotes and apostrophes raise the odds of burned-in subtitles, and that a plain colon form (She says: line with no quotes) is cleaner. Rewrite contractions (do not, not don't). (V) https://www.veo3ai.io/blog/veo-3-remove-subtitles-captions-fix-2026
- Put the spoken line first in the prompt, then the visual description. One creator reported ten subtitle-free generations in a row after moving speech to the top. (V) same page.
- Add an inline ban right after the line: (no subtitles, no captions, no on-screen text). (V) same page.
- Keep speech to about 15 words or fewer per 8 second clip. For UGC, 6 to 10 words per line. One idea per line. (V) https://www.veo3gen.app/blog/veo-31-dialogue-sfx-prompts-that-actually-sync-a-creator-workflow-for-clean-mout and (V) https://aivideosensei.com/prompts/veo-3-prompt-library
- Pacing markers creators use: `[beat]`, `[0.3s pause]`, `[1.0s pause]`. Keep SFX in the pauses, not on the words. Keep the camera simple while someone speaks. (V) veo3gen.app page above.
- Two speakers: label by appearance and position (the woman on the left in the red jacket), strict turn taking, and split long exchanges across clips. (V) veo3ai.io page above.

**Best at:** talking to camera with synced speech from a plain prompt, photoreal close-ups, skin and light, timed SFX. (V) https://invideo.io/blog/ai-micro-drama-model-routing/, (V) https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/

**Worst at:** 8 second ceiling, hallucinated subtitles, a different voice on every generation, drift when extended, and policy rejections on image inputs that look like minors or prominent people (Kie returns 422 for those). (V) https://docs.kie.ai/veo3-api/generate-veo-3-video-callbacks.md via helper agent, (S) https://www.technologyreview.com/2025/07/15/1120156/googles-generative-video-model-veo-3-has-a-subtitles-problem/

**Skeleton (MR, built on the sourced rules):**

```
[Speaker tag] says: [6 to 15 words, no quotes, no apostrophes].
(no subtitles, no captions, no on-screen text)

Visual: [shot type and camera], [who, one or two fixed identifiers], [one action], [where], [light].
Look: [capture medium and texture].
Audio: [voice quality and accent], [room tone], [one or two SFX in the pauses]. No music.
```

**Example (written for this project):**

```
She says: I almost did not try this. My mornings used to start with my knees.
(no subtitles, no captions, no on-screen text)

Visual: Handheld selfie video on a front phone camera at arm's length, slightly above eye level. A 64 year old woman with short gray hair and reading glasses pushed up on her head sits at her kitchen table. She talks straight to the lens, blinks, small head movements, one hand resting on a coffee mug. Window light from the left, a warm lamp behind her. Light handheld sway, no zoom, no cuts.
Look: plain phone footage, deep focus, real skin with pores and fine lines, slight sensor noise.
Audio: her voice only, warm, a little tired, American accent, quiet kitchen room tone, refrigerator hum. No music.
```

**Real examples live here:** https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1 (official timestamp, first/last frame and ingredients examples), https://aivideosensei.com/prompts/veo-3-prompt-library (tested ad templates), https://www.veo3ai.io/blog/veo-3-remove-subtitles-captions-fix-2026 (subtitle-free formula)

### 1.2 Kling 3.0 and Kling 3.0 Omni

**Structure:** Scene, Characters, Action, Camera, Audio and Style. 2 to 5 short sentences per shot, each sentence carrying one element. Short punchy sentences parse better than long compound ones. (V) https://fal.ai/learn/tools/how-to-use-kling-3-0-pro, (S) https://www.imagine.art/insights/kling-3-0-prompt-guide

**Image-to-video (official):** Subject + Movement, then Background + Movement. Keep language simple. Movements that break physics or stray far from the image trigger unwanted camera cuts. (V) https://kling.ai/quickstart/image-to-video-guide

**Multi-shot:** on Kie, set `multi_shots: true` and pass `multi_prompt` as an array of `{prompt, duration}`. Up to 5 shots, 1 to 12 s each, 15 s total, 500 characters per shot. Only a first frame is supported in multi-shot. Sound defaults on. (V) https://docs.kie.ai/market/kling/kling-3-0.md. fal documents six shots on its own endpoint. (V) https://blog.fal.ai/kling-3-0-prompting-guide/

**Dialogue syntax (fal's Kling guide):**

- Introduce each speaker once with a bracket label and description: `[Character A: description]`.
- Each line: `[Label, tone descriptor]: "line"`.
- Describe the action first, then give the line to the character who did it.
- Use linking words such as Immediately, or a bare Pause, to control turn timing.
- Never swap to pronouns or synonyms once a label is set.
(V) https://blog.fal.ai/kling-3-0-prompting-guide/

**Elements (consistency):** on Kie, `kling_elements` holds up to 3 elements per task, each with a name, a description and 2 to 4 images, optionally a 5 to 30 s voice sample. Reference them in the prompt as `@element_name`. (V) https://docs.kie.ai/market/kling/kling-3-0.md

**V3 vs Omni (official):** V3 is prompt-led (text, image, start and end frames, three or more characters, custom multi-shot). Omni is reference-led (multi-image reference, element reference, video element reference, element voice control). Choose Omni when a recurring face, product and voice must hold across many clips. (V) https://kling.ai/blog/kling-v3-vs-o3-comparison-guide

**Best at:** multi-shot dialogue where it cuts between angles inside one generation, cheap realistic people, start and end frame control, reusable characters. (V) https://invideo.io/blog/ai-micro-drama-model-routing/, (V) https://www.mindstudio.ai/blog/seedance-kling-minimax-video-model-comparison

**Worst at:** lettering on products distorts slightly, fine details such as jewelry and scars wander, identity softens the longer one clip runs, complex physics. (V) mindstudio page above, (V) https://www.atlascloud.ai/blog/guides/how-to-use-kling-3.0-for-character-consistency, (V) https://kling.ai/quickstart/image-to-video-guide

**Skeleton (MR):**

```
Shot N (Xs): [shot type]. [@element or labeled character] [one action]. [Camera: one move or locked]. [Light]. [Sound cue].
[Label, tone]: "short line"
```

**Example multi_prompt (written for this project, each under 500 chars):**

```
1 (4s): Medium shot, a bright bathroom, morning. @maria stands at the mirror and touches the skin under her eye with one finger. Camera locked. Soft window light. Quiet room tone, a tap dripping.
2 (5s): Close-up on @maria in the mirror. She turns to the camera.
   [Maria, low and honest]: "Nobody told me it could look like this at sixty."
   Camera slow push-in. No music.
3 (3s): Insert, macro. @maria's hand sets a small white jar on the sink edge. Camera locked. A soft clink on the tile.
```

**Real examples live here:** https://blog.fal.ai/kling-3-0-prompting-guide/ (six full dialogue scenes), https://fal.ai/learn/tools/how-to-use-kling-3-0-pro, https://kling.ai/quickstart/image-to-video-guide

### 1.3 Seedance 2.5 (and 2.0)

**Official formula (BytePlus, as reported by guides that cite it):** Subject + action or event + scene and environment + visual style + camera movement or cut + audio. (V) https://kylon.io/blog/seedance-2-5-prompt-guide-2026, (V) https://morphic.com/resources/how-to/seedance-2-5-guide. The official page exists at https://docs.byteplus.com/en/docs/ModelArk/2607689 but its body did not load for this research.

**Reference syntax:** `@Image 1`, `@Video 1`, `@Audio 1`, numbered in upload order. Give each reference a job and an exclusion, for example: @Image 1 defines her face, hair and green cardigan, do not use its background. One reference, one subject. BytePlus recommends 1 to 8 image subjects for stability even though 30 are accepted. (V) https://rendley.com/blog/how-to-prompt-seedance-2-5, (V) kylon page above.

**Timing syntax:** three accepted forms: continuous intervals (0-3s, 3-7s), a single time point (at the 2 second mark), or relative timing (after 3 seconds). Intervals must be continuous with no gaps. Timestamps budget time, they are not frame-accurate edit points. (V) rendley page, (V) morphic page.

**Stage structure for long takes:** each stage states one primary event and a visible end state. This out-performed free-form description in a public 30 second test. (V) https://blog.segmind.com/we-made-a-30-second-micro-drama-in-one-seedance-2-5-generation-full-test-output/

**Dialogue syntax, with a conflict to know about:**

- Lines in double quotes trigger lip-synced speech. (V) https://fal.ai/learn/tools/seedance-2-5-workflows
- The plain official form is: Dialogue (speaker description): "line". (V) rendley page.
- Some guides teach a bracket system (parentheses for music, angle brackets for SFX, curly braces for dialogue). (V) kylon and morphic pages. Another guide states the official BytePlus guide documents no such bracket language. (V) rendley page. **(MR)** use the plain form and quotes. Do not depend on brackets.
- Name the language and accent before the line. Tag every line with the speaker's name. (V) morphic page, (V) segmind page.

**Official negatives that work:** No subtitles. No BGM, only ambient and action sounds. No audio. (V) https://runware.ai/docs/models/bytedance-seedance-2-5/guides/prompting, (V) rendley page.

**Multi-shot:** use cut to cues or a labeled shot list with hard cuts. The model also cuts on its own (wide to close) if you do not forbid it. (V) https://fal.ai/learn/tools/seedance-2-0-prompting-guide, (S) https://youmind.com/ar/landing/x-viral-articles/seedance-2-5-ai-drama-guide

**Best at:** holding characters, products and on-product text across shots, long single generations with native audio, reference-driven work. In one September 2026 head-to-head it gave the cleanest, most consistent results and rendered the brand name most accurately. (V) https://www.mindstudio.ai/blog/seedance-kling-minimax-video-model-comparison

**Worst at:**

- Cost: $1.60 to $3.23 per clip in that same test against $0.20 to $0.60 for Kling 3.0. (V) mindstudio page.
- A plastic, over-smooth skin look, called out for Seedance 2.0 in particular. (V) https://invideo.io/faq/why-does-ai-generated-video-look-plasticky-and-how-do/
- All-or-nothing long takes: one bad beat in a 30 second clip means paying for the full regeneration. Latency for the same request ranged from 135 to 458 seconds, so set timeouts above 600 seconds. (V) segmind page.
- A face filter: Seedance 2.0 rejects reference images with detectable real human faces. AI-generated portraits are a documented path. (V) https://www.mindstudio.ai/blog/seedance-2-0-content-restrictions-workarounds, (S) https://seedance2.so/ms/blog/seedance-2-real-face-workaround. **(MR)** photoreal AI faces can still trip it, so keep a fallback model.
- Resolution conflict: fal, Runware and the segmind test describe a 720p ceiling. The Kie schema lists 1080p. Test on Kie before relying on it. (V) fal workflows page, (V) Kie schema.

**Skeleton (MR):**

```
[Format line: Vertical 9:16, capture style, one continuous shot or N shots with hard cuts.]
@Image 1 defines [identity + wardrobe]. Do not use its background.
@Image 2 defines [location]. @Image 3 defines [product, label exact].
0-4s: [initial state]. [primary event]. End state: [what is visible].
4-8s: [primary event]. End state: [what is visible].
Dialogue (NAME, voice description, accent): "short line"
Audio: [room tone, named sounds]. No BGM. No subtitles. No on-screen text.
```

**Example (written for this project):**

```
Vertical 9:16, plain phone footage, one continuous handheld shot, no cuts.
@Image 1 defines CAROL: her face, silver bob and blue cardigan. Do not use its background.
@Image 2 defines the location: a small sunlit kitchen. Keep the layout and the yellow curtains.
@Image 3 defines the product: a white supplement bottle. Keep the label exactly as shown.
0-3s: CAROL stands at the counter holding the bottle at chest height and looks at the lens. End state: bottle label faces the camera.
3-8s: CAROL sets the bottle down and taps the lid twice with one finger. End state: both hands flat on the counter.
Dialogue (CAROL, warm, slightly dry, Midwestern American English): "My daughter sent me this. I rolled my eyes."
Audio: her voice, quiet kitchen room tone, the bottle touching the counter. No BGM. No subtitles. No on-screen text.
```

**Real examples live here:** https://higgsfield.ai/blog/seedance-2-5-prompting-guide (full labeled-section prompts including a UGC one), https://blog.segmind.com/we-made-a-30-second-micro-drama-in-one-seedance-2-5-generation-full-test-output/ (the full 30 second prompt and settings), https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts (2,000+ community prompts, 2,078 stars on 2026-10-04), https://youmind.com/video-prompts/raw-ugc-smartphone-selfie-style-7530 (a UGC selfie recipe)

### 1.4 Wan 3.0

**Alibaba's official formulas (as tested and reported):**

- Basic: Entity + Scene + Motion
- Advanced: Entity + Scene + Motion + Aesthetic control + Stylization
- Image-to-video: Motion + Camera movement
- Sound: Entity + Scene + Motion + Sound description
- Multi-shot: Overall description + Shot number + Timestamp + Shot content
- Reference-to-video: Reference identifier + Action + Scene + Lines + Background music

(V) https://blog.segmind.com/wan-3-prompt-guide-alibabas-official-formulas-tested/

**Tested behavior:**

- Timestamps work. Cuts landed within about a frame of `[0-3s]`, `[3-6s]`, `[6-10s]` boundaries. (V) segmind Wan page.
- Without camera direction it edits on its own. A four word prompt produced five shots in five seconds. Always state the shot plan. (V) same page.
- Budget about 2.5 seconds of speech per 5 second clip. Two short sentences fit. (V) same page.
- `prompt_extend` is on by default in Alibaba's API and rewrites your prompt. Turn it off for detailed prompts. The Kie schema read for this research does not expose that switch, so on Kie assume the rewrite may happen. (V) segmind page, (V) Kie schema.
- Audio is on by default. (V) Kie schema.
- References are addressed as Image1, Video1, Audio1 in upload order. (V) https://docs.kie.ai/market/wan/3-0-video.md

**Best at:** 30 second single-pass clips, cheap per second ($0.05 at 480P to $0.20 at 1080P on Alibaba's own pricing), honoring timed cuts, reference consistency. (V) segmind Wan page, (V) https://morphic.com/resources/models/wan-3-0

**Worst at:** audio texture and in-frame text are the stated weak points, no 4K, 4 to 5 minute latency per job, drift risk on long takes. (V) morphic page, (V) https://www.cometapi.com/what-is-wan-3-0/, (V) segmind Wan page.

**Skeleton (MR, in the official multi-shot formula):**

```
Overall: [place, look, light, one consistent character description]. 
Shot 1 [0-3s]: [shot type], [action].
Shot 2 [3-6s]: [shot type], [action].
Shot 3 [6-10s]: [shot type], [action].
[Named ambient sounds]. No music.
```

**Example (written for this project):**

```
Overall: a quiet suburban kitchen at breakfast, photoreal phone footage look, soft daylight, the same woman throughout: early seventies, white ponytail, lavender robe.
Shot 1 [0-3s]: close-up, her hands twist the lid off a small amber jar.
Shot 2 [3-6s]: medium close-up, she lifts a spoon of golden powder and stirs it into a glass of water.
Shot 3 [6-10s]: slow push in on her face as she takes one sip and nods once.
Lid click, spoon on glass, faint birds outside. No music. No subtitles.
```

**Real examples live here:** https://blog.segmind.com/wan-3-prompt-guide-alibabas-official-formulas-tested/, https://morphic.com/resources/models/wan-3-0

### 1.5 Gemini Omni (Omni Flash, Omni 1.1 Flash)

**Structure:** shot framing and motion, style, light, location, action, in 3 to 4 sentences. Lead with the camera, because the opening phrase sets the grammar for the rest. Skip what is physically obvious. (V) https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides/prompting

**Critical default:** it cuts between shots unless told not to. Add in a single unbroken scene, or no scene cuts. (V) same page.

**Audio:** three patterns: named foley listed item by item, a layered ambience bed, and quoted dialogue with an accent given before the line. Add no music and no dialogue to switch off defaults. (V) same page.

**Editing:** it is built for conversational edits. Generate a clean base shot, then ask for one change at a time and say what must stay. (V) https://www.atlabs.ai/blog/ultimate-gemini-omni-flash-prompting-guide-2026

**On Kie:** 4, 6, 8 or 10 second clips, up to 4k, up to 7 reference images, first and last frame mode, plus reusable characters: create a character once from a portrait and an optional body image, optionally attach audio ids for voice traits, then pass `character_ids`. (V) https://docs.kie.ai/market/gemini-omni-video.md, (V) https://docs.kie.ai/market/gemini-omni-character.md

**Best at:** stylized work and bound first-to-last-frame clips. A published claymation ad skill runs every clip as a 4 second Omni Flash generation between two stills. (V) https://github.com/mikefutia/claymation-ads-claude-skill. It also topped the Artificial Analysis arena at a fraction of flagship cost per one ranking. (S) https://videogen.io/best-ai-video-models

**Worst at:** 10 second cap, drift on big scene changes and fast camera moves. (V) atlabs page above.

**Skeleton (MR):**

```
[Camera: shot type and one move], in a single unbroken scene. [Style]. [Light]. [Location]. [Subject does one action].
Audio: [named foley], [ambience]. In a [accent] accent: "line". No music.
```

**Real examples live here:** https://runware.ai/docs/models/google-gemini-omni-flash-1-1/guides/prompting, https://github.com/cnemri/awesome-gemini-omni, https://github.com/AtlasCloudAI/awesome-gemini-omni-prompts

### 1.6 Grok Imagine Video 1.5 Preview

- Treat it as an image-to-video tool. One guide states the 1.5 Preview API page says it does not support text-to-video. The Kie doc page describes the endpoint as text-to-video while also taking up to 7 images. Test before trusting text-only. (V) https://pixverse.ai/en/blog/grok-imagine-video-generation-capabilities-2026, (V) https://docs.kie.ai/market/grok-imagine/1-5-preview.md
- It entered the Artificial Analysis image-to-video arena in first place at launch (2026-05-31). (S) https://pixverse.ai/fr/blog/grok-imagine-video-generation-capabilities-2026
- Prompt with five parts: the subject that must stay readable, the motion, the camera, the environment, and protective constraints (keep the label, no text overlays). (V) pixverse page.
- Weak point for ads: product shape changes and labels that look readable but are wrong. Check every product frame. (V) pixverse page.
- **(MR)** useful as a cheap second opinion for b-roll from a start frame. Not a first choice for dialogue.

### 1.7 Sora 2 and Sora 2 Pro (retired)

Not available. The OpenAI cookbook structure is still a good universal template and transfers to every model above: a prose scene paragraph, then a Cinematography block (camera, lens, lighting, mood), an Actions list with one beat per bullet, a Dialogue block with labeled speakers, and a Background Sound line. It also recommends three to five named palette colors and countable motion beats. (V) https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide

### 1.8 JSON vs prose

- Neither Google nor OpenAI documents a JSON prompt schema. Both recommend natural language. JSON works only because the model reads tidy JSON as text. (S) https://www.datallmlab.com/blog/json-prompts-for-ai-video.html
- A side-by-side test of the same Veo 3 prompt as JSON and as structured text found near-identical output, with differences inside normal run-to-run variation. Duration, fps and resolution written inside JSON do nothing; those are API settings. (V) https://vc.ru/ai/2630266-json-promting-mify-i-realnost
- The real benefit is completeness and reuse: a schema forces you to fill every slot. (V) https://aivideosensei.com/prompts/veo-3-prompt-library
- **(MR)** keep the shot spec as structured data inside the skill (YAML or JSON per shot), then render it to prose in each model's own syntax. Never send raw JSON to the model.

### 1.9 Timestamp and multi-shot prompting, compared

| Model | Syntax | Notes | Source |
|---|---|---|---|
| Veo 3.1 | `[00:00-00:02]` blocks | Official. Up to four beats in 8 s. | (V) Google Cloud guide |
| Seedance 2.0 | `[0s]`, `[3s]`, `[6s]` markers | 2 to 3 markers for 5 s, 3 to 4 for 10 s. One camera position, one action, one atmosphere detail per marker. | (V) https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video |
| Seedance 2.5 | continuous intervals `0-3s` | Too little in a window and it improvises, too much and it drops a beat. | (V) Runware Seedance guide |
| Wan 3.0 | `Shot 1 [0-3s]:` | Cuts land within about a frame. | (V) segmind Wan guide |
| Kling 3.0 | separate `multi_prompt` items with durations | No timestamps in text. 500 chars per shot. | (V) Kie schema |
| Gemini Omni | no timestamps needed | Say single unbroken scene, or describe the cuts. | (V) Runware Omni guide |

**(MR)** for ads, generate one shot per clip by default. Use in-clip multi-shot only for dialogue exchanges (Kling) and for long single-location scenes (Seedance, Wan). Separate clips can be re-rolled one at a time. A 30 second generation cannot.

### 1.10 Stopping hallucinated captions, subtitles, logos and music

1. **Captions and subtitles.** Veo: colon dialogue with no quotes or apostrophes, speech first, inline ban. (V) veo3ai.io page. Seedance: No subtitles is an official control. (V) Runware Seedance guide. Everything else: write No subtitles, no on-screen text in the audio or constraint line.
2. **Leave headroom.** Compose with empty space in the bottom fifth so a bad clip can be saved by cropping 12 to 18 percent or by covering it with your own caption. (V) veo3ai.io page.
3. **Do not re-roll the same prompt.** If text appears, change the prompt before spending again. (V) veo3ai.io page.
4. **Music.** Say No music or No BGM in every audio line. (V) Runware Omni and Seedance guides. **(MR)** for voiceover-driven b-roll, turn audio off entirely (`sound: false` on Kling, `generate_audio: false` on Seedance, `audio: false` on Wan) and build the sound bed yourself.
5. **Logos and product text.** Generated on-screen text is still unreliable everywhere, so prices and headlines go on in post. (V) apogee page. Attach the real product photo as a reference on every frame that shows the product. (V) claymation skill repo.
6. **Wrong words.** Avoid quoting any word you do not want rendered as text. Keep brand names out of the visual description unless the label must show.
7. **Catch it in QA.** Run a text check on sampled frames of every clip (see section 7). **(MR)**

### 1.11 Model routing at a glance (MR, built from the sources above)

| Job | First choice | Why | Fallback |
|---|---|---|---|
| Talking to camera, speech generated in the clip | Veo 3.1 | best speech from a simple prompt | Seedance 2.5 with references, Kling 3.0 |
| Recurring character across many shots | Kling 3.0 with elements + start frame | only model taking both at once on Kie, cheap | Seedance 2.5 reference mode, Omni character ids |
| Product in hand, label must read | Seedance 2.5 reference mode | best text and product fidelity | Kling 3.0 with a product element |
| Two-person dialogue with cuts | Kling 3.0 multi-shot | cuts between angles natively | Seedance 2.5 staged prompt |
| Silent b-roll inserts from a start frame | Kling 3.0 std or Wan 3.0 | cost | Grok Imagine 1.5 |
| Stylized (claymation, storybook, 3D) | Gemini Omni first / last frame | bound start and end stills | Veo 3.1, Kling 3.0 |
| 15 to 30 s single-location scene | Seedance 2.5 or Wan 3.0 | long native takes | split into clips |

---

## 2. The UGC selfie realism recipe

### 2.1 Core idea

Brands buying AI UGC want something that looks like a real person filmed it on a phone, a little imperfect. Glossy perfection reads as a fake sponsored post. The fix is to prompt for small-sensor phone physics and real skin, and to ban the cinematic vocabulary. (V) https://dxbuilder.io/blog/how-to-create-realistic-phone-footage-ai-ugc-230926

### 2.2 The recipe

1. **Start from a still, never from text.** Generate a photoreal seed frame first, then animate it. Skipping the frame stage is the most cited cause of bad output. (V) dxbuilder page, (V) https://www.pigeondigital.com/insight/ai-ugc-ads-stack-claude-nano-banana-seedance-2026
2. **Seed frame prompt carries the realism.** Write the capture device, the framing, the skin and the mess into the image prompt.
3. **Motion prompt carries only motion.** Talking, breathing, small hand tremor, eye contact. Do not describe the person again. (V) dxbuilder page.
4. **Render native 9:16.** Never render 16:9 and crop. (V) dxbuilder page, (V) https://aiworkflows.tools/workflows/short-drama
5. **Lock one accent line** (for example American accent, conversational tone) into every scene prompt. Accent drift between scenes is a common failure. (V) https://ugccopilot.ai/blog/seedance-2-ugc-ad-workflow-tutorial-2026/
6. **Expect waste.** Plan for 30 to 40 percent of clips to need regeneration, and 3 to 10 attempts per keeper on hard shots. (V) ugccopilot page, (V) apogee page.

### 2.3 Phrases that push toward phone footage

Use in the seed frame prompt (ideas drawn from the sources, reworded):

- front phone camera at arm's length, slightly above eye level, slight wide-angle distortion
- phone front camera selfie framing (one guide credits this phrase with flattening depth of field and tightening the crop the way a real selfie does) (V) ugccopilot page
- 24mm phone lens, deep focus, background readable (V) dxbuilder page
- visible pores, fine lines, slight shine on nose and forehead, small asymmetries, flyaway hair (V) https://youmind.com/video-prompts/raw-ugc-smartphone-selfie-style-7530
- mixed light: daylight from a window plus a warm household lamp (V) dxbuilder page
- casual, slightly tilted framing, lived-in room, ordinary clutter
- slight sensor noise, plain true-to-life color

Use in the motion prompt:

- handheld micro-jitter, natural breathing, blinks, a half-beat-late reaction (V) dxbuilder page, (V) https://higgsfield.ai/blog/seedance-2-5-prompting-guide
- understated delivery, not performing, voice a little self-conscious (V) higgsfield page
- fixed selfie framing for the whole clip (V) higgsfield page

### 2.4 Phrases to ban

- 8K, hyperrealistic, award-winning cinematography, cinematic
- studio lighting, volumetric light, any render-engine name
- 85mm portrait lens, shallow depth of field, bokeh
- flawless skin, airbrushed, saturated color

(V) dxbuilder page. The Seedance UGC recipe adds a long explicit list of skin-retouching bans in its negative section. (V) youmind page.

### 2.5 Seed frame and motion prompt patterns (written for this project)

Seed frame (image model):

```
Raw phone selfie photo taken on a front camera at arm's length, slightly above eye level, slight wide-angle distortion. A 67 year old woman with shoulder-length gray hair, no makeup, reading glasses on a cord, sits in a worn armchair by a window. Daylight from the window on one side of her face, a warm table lamp behind her. Real skin: pores, fine lines, age spots on the hands, slight shine on the forehead. She holds nothing and looks into the lens with a small tired smile. Lived-in living room behind her in focus: crocheted blanket, framed family photos, a TV remote. Plain true-to-life phone color, slight sensor noise. Vertical 9:16. No text, no logos.
```

Motion (video model, start frame attached):

```
She talks to the camera in a calm, unhurried way, small nods, natural blinks, her free hand lifts once and settles back on the armrest. The phone has light handheld sway. Framing stays the same for the whole clip. No cuts, no zoom.
She says: [line].
Audio: her voice, quiet living room tone, a clock ticking. No music. No subtitles, no on-screen text.
```

### 2.6 Common tells of AI video and how creators remove them

| Tell | Cause | Fix at generation | Fix in post |
|---|---|---|---|
| Waxy, smoothed skin | models smooth fine texture and over-sharpen edges (V) invideo plasticky FAQ | put pores, lines and shine in the seed frame; pick an image model that keeps imperfections | upscale with denoise low and skin smoothing off, light blur, then grain (V) https://invideo.io/blog/ai-video-post-production-pipeline/ (S) |
| Perfect lighting | cinematic vocabulary | mixed color temperature, window plus lamp (V) dxbuilder | grade toward a real phone clip |
| Dead eyes, no blinks | long takes with no direction | ask for blinks, glances, a late reaction; keep talking clips 4 to 8 s | cut away to b-roll before it shows |
| Motorized camera | default camera drift | ask for handheld micro-jitter, or lock the camera | add slight shake |
| Drifting or melting hands | complex hand tasks | one simple hand action, hands at rest, product already in hand in the start frame; POV hand shots need extra re-rolls (V) apogee | cut the shot shorter, punch in |
| Morphing background | long clips, big camera moves | short clips, locked camera, a location reference image | use a punch-in to hide edges |
| Gibberish text | models cannot hold lettering | keep signage out of frame, attach the real product photo | add all text in post |
| Robotic or changing voice | each generation invents a new voice; voice is called the single biggest tell (V) skaleit | one locked voice source for all clips | replace or convert audio to one voice (S) https://hackernoon.com/how-to-keep-an-ai-voice-consistent-across-every-video-clip |
| Unrequested mid-clip action | model drift (one agency saw an actor start doing core exercises in a skincare ad) (V) pigeondigital | one action, stated end state | watch every clip fully before approving |
| Background people frozen | default extras | ask for background people who move naturally (V) higgsfield | crop them out |

### 2.7 Post tricks: grain, softness, compression, shake

Order that creators report: upscale first, then a light blur, then grain, then grade. Never add sharpening. (V) https://invideo.io/faq/why-does-ai-generated-video-look-plasticky-and-how-do/. A related invideo page gives amounts: grain at 2 to 3 percent (or a 20 to 40 percent overlay) and a 0.3 to 0.8 px Gaussian softening, on the reasoning that AI frames have no sensor noise or optical softness. (V) https://invideo.io/faq/does-adding-film-grain-and-blur-to-ai-generated-video/

ffmpeg starting points **(MR, untested values)**:

```
# subtle temporal grain + slight softening
-vf "gblur=sigma=0.5,noise=alls=6:allf=t"

# slight handheld drift on a locked clip: crop a little, wander the crop window, scale back
-vf "crop=iw-24:ih-24:12+8*sin(2*PI*t*0.6):12+6*sin(2*PI*t*0.8+1),scale=1080:1920:flags=lanczos"

# phone-style compression pass before the final encode
-c:v libx264 -crf 27 -preset veryfast
```

The ffmpeg `noise` filter takes strength 0 to 100; 20 is heavy. (V) https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Video/noise.html

### 2.8 Where AI UGC wins and loses (paid results)

- An agency running this stack for Shopify clients reports that single standalone AI testimonials flop, while AI clips cut into human-paced mashups with product shots and screen recordings convert. On a homewares account the AI batch cost about a tenth and CPA landed within 10 percent of human creators. On a trust-dependent skincare account AI CPAs were about 40 percent worse and were pulled. The article flags its own numbers as illustrative. (V) https://www.pigeondigital.com/insight/ai-ugc-ads-stack-claude-nano-banana-seedance-2026
- Another agency reports roughly $0.13 per ad in credits and up to 5x ROAS on Meta, using Nano Banana Pro stills animated by Kling motion control from real reference clips. (V) https://skaleit.agency/blog/ai-ugc-ads-cheap-realistic-meta-ads-method/
- Real cost math: sticker price times 5 to 10 generations per keeper times about 10 creatives per winner. (V) apogee page.
- About 74 percent of middle-aged and senior Americans report little to no trust in AI-generated health information. (S) https://www.rainforgrowth.com/insights-updates/rethinking-senior-healthcare-marketing. **(MR)** for this audience the realism bar is higher and an obvious AI look costs more than it does with younger buyers.

---

## 3. Character and scene consistency across many clips

### 3.1 The workflow that holds up (start-frame-first)

Every published pipeline that works uses the same skeleton: one locked portrait, a start frame per shot built from that portrait, then image-to-video per shot.

1. **Master portrait.** Generate one photoreal image of the character. This file is canonical. Never regenerate it mid-project. A real bug report shows the actor changing across clips until the project stored one portrait and attached it as the first reference on every clip and every re-roll. (V) https://github.com/infoworksdomain-blip/PostmindStudio/pull/103
2. **Reference pack.** From the master, make: a clean front view, a three-quarter view, a profile, a full body, and one or two expression variants. Add a back view only if a shot shows it. If a new scene reveals a side the reference never showed, the model guesses. (V) https://runware.ai/docs/models/google-nano-banana-2/guides/character-consistency
3. **Location plate.** One image of the empty room per location. Reuse it as a reference in every start frame for that location.
4. **Product reference.** The real product photo, not a generated one, attached to every frame that shows the product. (V) https://github.com/mikefutia/claymation-ads-claude-skill, (V) pigeondigital page.
5. **Start frame per shot.** Use an edit model (Nano Banana 2, Nano Banana Pro or Seedream 5.0 Pro) with the references attached. State what stays and what changes.
6. **Pick stills before paying for video.** Render 2 or 3 start-frame candidates and choose. Previewing start frames before the full render cut regenerations by about 40 percent in one pipeline. Another generates candidates in parallel and lets a vision model choose. (V) https://dev.to/humzakt/ugc-pipeline-script-first-ai-video-generation-1o8c, (V) https://github.com/HKUDS/ViMax
7. **Animate each shot from its start frame** with a motion-only prompt.
8. **Re-anchor, do not chain blindly.** Each clip goes back to the original references. See 3.5.

### 3.2 Exact prompt patterns for the image edit step (written for this project)

The patterns follow three documented rules: begin with the same subject from the reference image, name the features to keep, and describe only what is new (V) Runware Nano Banana 2 guide; tell the model to keep facial features exactly the same as Image 1 (V) https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n; and state both the change and the elements that must stay fixed, with no vague pronouns (S) https://evolink.ai/blog/seedream-prompt-guide-best-practices-2026.

**Master portrait (text to image):** use the seed frame pattern in 2.5.

**Angle variant:**

```
Image 1 is the reference. The same woman from Image 1, same room, same clothes, same hair. Keep her facial features exactly the same as Image 1. Change only the camera position: a three-quarter view from her left at chest height, about two meters away. Same window light and lamp. Phone photo look, deep focus. Vertical 9:16.
```

**Expression variant:**

```
The same woman from Image 1 in the same position and framing. Keep her face, glasses, hair and cardigan identical. Change only her expression: eyebrows raised, mouth slightly open, as if she just read something surprising. Do not change the light or the background.
```

**New location with the same person:**

```
Image 1 defines the woman (identity, hair, glasses, blue cardigan). Image 2 defines the location (this exact bathroom: white tile, oval mirror, green towel). Place the woman from Image 1 standing at the sink in the room from Image 2, medium shot from the doorway. Keep her facial features exactly the same as Image 1. Keep the room layout and objects exactly as in Image 2. Light comes from the frosted window in Image 2. Phone photo look. Vertical 9:16.
```

**Product in hand:**

```
Image 1 defines the woman. Image 2 is the real product photo. The same woman from Image 1, same room and clothes, now holds the bottle from Image 2 in her right hand at chest height with the front label facing the camera. Keep the bottle shape, cap color and label exactly as in Image 2. All five fingers visible and relaxed. Do not change her face, the light or the background.
```

**End frame for a first-to-last-frame clip:** edit the start frame, do not generate a fresh image. Two independently generated stills disagree on room details and the video model has to reconcile them. (V) https://fal.ai/learn/tools/seedance-2-5-workflows

```
Same image as Image 1, same framing, same light, same room. Change only this: the glass on the table is now empty and her hand rests flat beside it.
```

**Storyboard grid shortcut:** ask Nano Banana Pro for a nine-panel grid of film stills that tell the scene while preserving identity, then ask it to extract a panel by row and column, upscale, and use panels as start frames. Fast, but panels are low resolution and must be upscaled. (V) https://videohighlight.com/v/7RIN1pLJjH4

**Rules for the edit step:**

- Edit, do not re-roll. Ask for one change at a time on a good image. (V) https://www.atlabs.ai/blog/master-professional-ai-asset-creation-google’s-10-golden-rules-for-nano-banana-pro, (V) dev.to/googleai page.
- Do not re-describe features the reference already shows. Spend the prompt on what is new. (V) Runware Nano Banana 2 guide.
- Name small distinguishing details (the glasses cord, the cardigan color) so they survive. (V) same guide.
- Reference limits: Nano Banana Pro supports up to 14 references with 6 at high fidelity per Google's guide; Kie's Nano Banana Pro endpoint accepts 8 inputs and Nano Banana 2 accepts 14. (V) dev.to/googleai page, (V) Kie schemas.
- Fix the source sheet when something is wrong. Do not keep re-rolling shots built on a flawed reference. (V) https://invideo.io/faq/how-do-you-fix-character-drift-when-chaining-ai-video/

### 3.3 Each model's consistency mechanism

| Model | Mechanism | Limits and gotchas | Source |
|---|---|---|---|
| Veo 3.1 | first frame (and last frame), or reference images (Google calls this ingredients) | On Kie, reference mode is Fast and Lite only, 8 s only, 1 to 3 images. First-frame mode works on all tiers. | (V) Kie Veo doc, (V) Google Cloud guide |
| Kling 3.0 | elements (`@name`) plus a start frame | 3 elements per task, 2 to 4 images each. Use front and side views, even neutral light, plain background, one outfit per sheet. | (V) Kie Kling doc, (V) atlascloud consistency guide |
| Kling 3.0 Omni | multi-image and video element reference, element voice | up to 7 reference images | (V) Kie Omni doc, (V) kling.ai comparison |
| Seedance 2.5 | `@Image N` references with stated roles | reference mode excludes first-frame mode; 1 to 8 subjects recommended; real-face filter | (V) Kie doc, (V) rendley |
| Wan 3.0 | Image1, Video1 references | reference mode excludes first-frame mode; label every reference in the prompt | (V) Kie doc, (V) morphic |
| Gemini Omni | `character_ids` built from portrait + body image, optional voice audio | each character uses 1 or 2 of 7 slots; excludes first-frame mode | (V) Kie docs |
| Sora 2 characters / cameos | retired | n/a | (V) invideo Sora page |

**Two prompt rules that look like they conflict, and how to reconcile them (MR):**

- With a start frame attached, describe motion only. Re-describing the actor causes face morphing. (V) dxbuilder page.
- With reference mode and no start frame, paste one identical character descriptor block into every prompt and change only the scene line. Even small paraphrases cause drift. (V) atlascloud consistency guide, (V) https://alejandrodinsmore.substack.com/p/deep-dive-veo-3-i-spent-400-testing

### 3.4 Keeping wardrobe, props and room fixed

- One signature outfit per character sheet. (V) atlascloud guide.
- Write the continuity list out in concrete nouns: identity, clothing, props, room position, light direction. Vague instructions to stay consistent do nothing. (V) kylon page.
- Make a new reference sheet whenever costume or props change on purpose. (V) invideo drift FAQ.
- Start each new location with a wide establishing shot and use it as the spatial anchor for the tighter shots. (V) invideo micro-drama routing page.
- Repeat the outfit and hair descriptors in every continuation prompt when using the same anchor image for many 8 second clips. (V) https://www.stork.ai/blog/pt/this-ai-creates-perfect-60-second-ads

### 3.5 Last-frame chaining and extend

- **Why it drifts:** each extension feeds the model a frame it invented, and the small errors compound into color shift, identity change and contrast loss. Chained clips anchor to the previous clip, not to your character, so by the third or fourth clip the errors have stacked. (V) https://hackernoon.com/how-to-extend-an-ai-generated-video-clip-past-its-length-limit-without-the-drift, (V) invideo drift FAQ.
- **Cap extensions at two.** Use extend only for static or low-motion shots. Generate fresh for dialogue, lip-sync, pans and handheld. A short static insert is cheaper and safer than a third extension. (V) hackernoon page.
- **Export the last frame at full resolution** from the delivered file, never from a compressed preview. (V) hackernoon page. Seedance 2.5 on Kie can return it directly with `return_last_frame`. (V) Kie doc.
- **Chain with references, not with the last frame alone.** Re-attach the character and location references on every segment so it re-anchors to the source. (V) invideo drift FAQ.
- **Trim the join.** On Seedance extend, the first two frames of the new clip are often bad; cut in from frame three. A small curve and hue correction at the join is standard. (S) https://invideo.io/faq/why-do-the-first-frames-of-an-ai-extended-video-clip/
- **Veo on Kie:** extend takes the original `task_id` and a prompt, and 1080P renders cannot be extended. (V) https://docs.kie.ai/veo3-api/extend-video.md
- **(MR)** for ads, cuts are free and expected. Prefer a new angle from a new start frame over any extension. Use last-frame chaining only when a single continuous action has to run past the clip limit.

### 3.6 Color matching between clips

- Normalize color in post as a standard step, alongside fixed reference frames and identical descriptor text. (S) https://www.futureflowai.in/post/how-to-make-a-cinematic-ai-short-film-in-2026-the-complete-workflow
- scikit-image has a one-line histogram transfer: `match_histograms(image, reference, channel_axis=-1)`. (V) https://scikit-image.org/docs/stable/auto_examples/color_exposure/plot_histogram_matching.html
- **(MR)** matching every frame separately flickers. Compute one transfer per clip from its first frame against a hero frame for that scene, bake it into a `.cube` LUT, and apply with ffmpeg `lut3d`. Then run one shared grade and one shared grain pass over the whole timeline so clips from different models sit together. Both `lut3d` and scikit-image 0.24 are present on this machine (checked 2026-10-04).

---

## 4. Shot design and intentionality

### 4.1 From script to shot list

1. **Voice first.** Generate the voiceover before any clip, measure each line, and size each shot from measured audio. Cuts then land on the narration with no timing fixes. (V) claymation skill repo, (V) humzakt pipeline post.
2. **Split the script into beats.** One sentence or one claim per beat. One published pipeline has the LLM split scripts into 8 second scenes to match Veo. (V) https://n8n.io/workflows/14316-ads-factory-generate-unlimited-length-ugc-ai-video-pipeline/
3. **Mark each line** as one of: a claim that needs a visual, a place where the face matters, a dense stretch that needs a breather, or a change of place or time. (V) https://storyflow.so/blog/how-to-plan-b-roll
4. **Write each shot as an actionable line:** subject, framing, moving or locked, duration, and the job it does for the script. A line like detail, hands on the jar, locked, 3 s, shows the daily habit claim is usable. A line like kitchen b-roll is not. (V) storyflow page.
5. **One idea per shot, and the visual must show the exact words.** If the line names a noun, the noun is on screen while it is said. **(MR)** this is the single biggest difference between intentional and confusing AI ads.
6. **Keep the face for emotional lines.** Do not cut away when the speaker's face carries the moment. (V) storyflow page.
7. **Never reuse the same shot twice.** It signals a shortage. (V) storyflow page.

**Shot spec the skill should carry per shot (MR):**

```yaml
- id: s07
  script_line: "I stopped dreading the stairs."
  vo_seconds: 2.4
  type: b-roll            # a-roll | b-roll | insert | macro | diagram | text-card
  shows: "her slippered feet climbing carpeted stairs at an easy pace"
  job: illustrate          # illustrate | cover | breathe | establish | hook | proof
  framing: "low angle from the bottom step, locked"
  start_state: "left foot on step two"
  end_state: "both feet out of frame at the top"
  camera: locked
  duration: 3
  refs: [char_master, loc_hallway]
  model: kling-3.0
  audio: none
```

### 4.2 Shot length and cadence

- Finished-edit shots typically run 2 to 5 seconds. (V) storyflow page.
- Cuts every 2 to 3 seconds keep attention in short-form. (V) https://segwise.ai/blog/anatomy-top-performing-video-ad-frame-by-frame
- Talking clips: one sentence, 3 to 6 seconds of speech per 8 second generation, then trim. (S) veo3gen.app via search summary, (V) veo3gen.app dialogue page.
- Shorter generated clips (3 to 6 s) hold consistency better than long ones. (V) fal Kling 3.0 Pro guide.
- UGC script pace: about 74 to 84 words per 30 seconds, roughly 2.5 to 2.8 words per second. (S) https://ugccopilot.ai/ugc-scripts/
- Trim 0.3 to 0.5 seconds of dead air off the head and tail of each talking clip. (V) ugccopilot tutorial.
- **(MR)** for buyers over 60: 2 to 4 second shots in the first 15 seconds, 4 to 6 seconds after, and a visual change on every new claim. No source found gives cadence data for this age group.

### 4.3 When to use which shot type (MR, grounded in the sources)

| Type | Use when | AI risk | Notes |
|---|---|---|---|
| A-roll (talking to camera) | first-person claims, emotion, trust | lip-sync, voice drift | direct address converts 33 percent better than voiceover only per one data roundup (V) segwise |
| B-roll (scene illustrates the line) | every concrete noun or action in the script | low, no face needed | stills to animate to assemble is the standard flow (V) apogee |
| Insert / macro | product, texture, hands, a single object | hands, label text | attach real product photo |
| POV hands | usage demo | hands are the weak point; budget extra re-rolls (V) apogee | no face means no lip-sync |
| Diagram / animation | mechanism, how it works | text gibberish | render shapes only, add labels in post |
| Text card | numbers, offers, prices | none if done in post | never ask the model to write it |

### 4.4 Camera vocabulary that models obey

Shot sizes: wide, medium, medium close-up, close-up, extreme close-up, macro, over-the-shoulder, two-shot, POV, low angle, high angle, top-down.

Moves: locked-off (static), slow push-in (dolly in), pull-back (dolly out), pan left or right, tilt up or down, tracking shot alongside, orbit or arc, crane up or down, handheld, rack focus, whip pan.

Sources: (V) Google Cloud Veo guide, (V) Runway prompting guide, (V) Runware Seedance guide, (V) fal Kling 3.0 Pro guide.

Rules:

- One camera move per clip. Stacking several directions gives chaotic results. (V) Runway guide.
- If you say nothing, Kling stays static or drifts slightly, Wan and Omni start cutting. Always state locked camera, or one move, and no cuts. (V) fal Kling guide, (V) segmind Wan guide, (V) Runware Omni guide.
- Replace vague words (dynamic, cinematic) with the named move. (V) https://higgsfield.ai/blog/generating-with-seedance-2-0

### 4.5 What makes motion look deliberate

1. One action per clip. (V) Runway guide.
2. State the start state and the end state. The end state gives a reviewer something to check. (V) kylon page, (V) segmind micro-drama test.
3. Camera locked unless the move has a reason (reveal, follow, emphasis). **(MR)**
4. Physics-safe actions. Bouncing balls, throws and complex trajectories still fail. (V) Kling image-to-video guide.
5. Hands do simple things: hold, set down, tap, point. Put the object in the hand in the start frame. **(MR)**, supported by (V) apogee.
6. Give the model a consequence to render (steam rises, the lid clicks) so it has concrete physics to resolve. (V) fal Seedance 2.0 guide.
7. Minimal movement while speaking; actions happen on the beats between phrases. (V) veo3gen.app dialogue page.
8. Subtle motion beats aggressive motion when animating stills. (S) https://claudemarket.ai/skills/gracelungu/nano-banana-kling-ad-workflow

### 4.6 First-frame and hook rules for paid social

- Viewers decide in about 1.7 seconds on Meta. (S) search summary of https://vidico.com/news/facebook-video-ad-best-practices-that-actually-work-2026/
- Meta's first-half 2026 average hook rate was 25.44 percent across 88,329 sales ads. Aim for 30 percent or more on Meta and 40 percent or more on TikTok. (V) https://billo.app/blog/hook-rate-to-hold-rate
- Put the first visual jolt inside 1.5 seconds, ideally at 0.8 to 1.2 seconds. Use one or two strong interrupts, not a barrage. (V) https://inceptly-agency.beehiiv.com/p/pattern-interrupts-simple-video-tricks-that-stop-the-scroll
- Open on motion in the first second. Product or subject already moving beats an establishing shot. (V) https://vidpros.com/facebook-video-ads/
- The first frame has to work as a still image, because a share of viewers never unmute. (S) search summary of https://selzee.com/blog/advertising-hooks-examples
- 63 percent of top-performing auction ads use text in the first frame, and 63 percent of top TikTok ads deliver the core message in 3 seconds. (V) segwise page (citing Keevx), (V) billo page.
- Show the value by second 7. (V) vidpros page.
- Absurd AI hooks pull views, not buyers. Test them as a hook grafted onto a selling body. (V) apogee page.
- **(MR)** for the skill: generate the hook shot as its own clip, check that frame 1 is already a strong image with motion under way (trim the first 4 to 8 frames if the model eases in), and add the hook text in post inside the safe zone.

---

## 5. Formats winning in paid social with AI video, and how each is made

Costs below are from the apogee roundup unless noted. (V) https://www.apogee.ad/en/blog/crea-publicitaire-ia-concepts-meta-ads/

| Format | Stack people use | Why that stack | Gotchas |
|---|---|---|---|
| AI UGC selfie testimonial | Nano Banana still, then Veo 3.1 (speech in clip) or Seedance / Kling with references; or avatar tools (Arcads, Creatify) | Veo gives synced speech from a prompt; reference models hold the face over many clips | Lip-sync decides everything. Voice changes per clip. Standalone AI testimonials underperform mashups (V) pigeondigital. Legal: see 5.1. |
| Podcast clip / interview | Veo 3.1 for multi-speaker, Kling 3.0 multi-shot; or two silent clips plus a lip-sync pass | native two-person dialogue | Set must look like a real podcast: real mics, proper two-shot. A bedroom with an unplugged mic does not work (V) https://www.niceads.uk/p/how-to-make-fake-podcast-ads-that-actually-work. Budget 5 to 10 attempts. Masked or anonymous guest removes the lip-sync problem (MR). |
| Street interview | Veo 3.1 for tight shots; 3 to 5 passer-by clips plus cutaways | handheld chaos is a pattern interrupt plus social proof | Label speakers by look and position. Keep answers to one line. Needs several clips to feel real. (V) apogee, (V) https://rpn.beehiiv.com/p/how-to-go-viral-with-veo-3 |
| Doctor or expert to camera (yapper) | Portrait still, then lip-sync avatar lane (other researcher), or Veo 3.1 clips | long monologue needs audio-driven lip-sync, not 8 s speech clips | Highest legal risk. Fake AI doctors are under press, platform and state attorney general scrutiny (S) https://www.emarketer.com/content/ai-doctor-fakes-wellness-influencers-fuel-health-scam-ads-on-social-media, (S) https://illinoisattorneygeneral.gov/news/story/attorney-general-raoul-calls-on-meta-to-remove-misleading-ai-weight-loss-ads. No invented credentials or diplomas. |
| Photoreal mini-drama with dialogue | Veo for emotional close-ups, Kling for two-person exchanges, Seedance reference mode for the recurring lead; or one Seedance 2.5 take | each model is routed to the shot it is best at (V) https://invideo.io/blog/ai-micro-drama-model-routing/ | Keep dialogue to 1 or 2 lines per generation and under 12 words per line. Start each scene with a wide shot as the anchor. A 30 s Seedance 2.5 take cost about $7.12 and any flaw means a full redo (V) segmind. |
| Storybook / illustrated narration | Style-locked stills (Nano Banana, GPT Image), subtle image-to-video (Kling, Omni first / last frame), ElevenLabs narration | stills carry the style; motion is only blinking, breathing, drifting elements | Lock the style with one style reference image attached to every still. Voiceover drives timing. No lip-sync needed. (V) claymation skill, (S) https://lilys.ai/hi/notes/nano-banana-20260204/cinematic-ai-nano-banana-veo |
| Pixar-style 3D characters, talking objects, organs, foods | Veo 3.1 for 8 s speech clips, Seedance for longer episodes, Kling for mouth detail; or still + lip-sync | stylized faces forgive lip-sync errors | Prompt = character + distinctive features + emotion or action + setting + style. Keep the character description identical across clips. (V) https://online.hitpaw.com/learn/ai-fruit-video-prompts.html, (S) https://vmake.ai/blog/ai-fruit |
| POV vlog | Veo 3.1 with the same character block in every prompt, selfie-stick framing | style word first (selfie vlog style), then detail | Identical description every clip; small wording changes break the look. (V) https://alejandrodinsmore.substack.com/p/deep-dive-veo-3-i-spent-400-testing |
| AI baby or animal podcast | One still (podcast set, headphones, mic, lips slightly parted), a recorded or TTS voice track, then an audio-driven lip-sync tool | image + audio in, talking video out; three steps | The voice is the joke, so record or convert a real adult read. Lip-sync lane belongs to the other researcher. Note Veo on Kie may reject or mute content that looks like minors. (V) https://cholyai.beehiiv.com/p/how-to-create-viral-ai-baby-podcast-videos-step-by-step-guide-26b6, (S) https://ai-for-real-life.beehiiv.com/p/how-to-make-ai-talking-baby-videos |
| ASMR / cut-open | Veo 3.1, Kling, or Seedance with native audio | sound generated in sync with the picture is the whole point | Macro, shallow depth, plain background, one hand, one knife, two clean cuts. Image-to-video is hit and miss; physics can fail. (V) https://techtactician.com/how-to-make-veo-3-asmr-fruit-cutting-videos-prompts-included |
| News-report style | Veo 3.1 generated set, or avatar tool, with all graphics added in post | the newscast frame is a strong pattern interrupt | Generate the desk with empty screens and no lower third, then add your own graphics. Keep it clearly parody, not a real outlet, to stay inside ad policy. (V) apogee |
| Old footage / 1950s style | Veo 3.1, Seedance, Wan, Kling with medium terms in the prompt, plus a film-damage pass in post | models respond to capture-medium language | Name the stock and the damage: 16mm, faded warm color, heavy grain, gate weave, scratches. Keep period details concrete. (S) https://youmind.com/video-prompts/vintage-16mm-archive-film-montage-6037, (S) https://www.media.io/ai-prompts/vintage-video-prompts.html |

More format notes from the same roundup: faceless voiceover ads (AI b-roll + ElevenLabs) are the most scalable at $2 to $8 per finished 30 seconds; a short VSL of 60 to 90 seconds is an assembly job because models return 6 to 15 seconds per call ($15 to $40 in generation); fake podcast runs $12 to $15 in generation per 30 second edit. (V) apogee.

### 5.1 Compliance gotcha that touches every people format (outside my lane, but it kills ad accounts)

- The FTC's 2024 rule on fake reviews and testimonials covers AI-generated testimonials. A synthetic person presented as a real satisfied customer can be an illegal fake endorsement even when the ad is labeled as AI. (S) https://www.makeinfluence.com/en/academy/ai-generated-synthetic-ugc-ads-when-a-brand-uses-an-ai-actor-instead-of-a-real-creator
- Meta's AI Info label targets photoreal AI people and fully AI scenes. Account-risk mistakes named by one policy guide: presenting a synthetic person as a real named customer, fabricated testimonials, unsupported health claims, and skipping disclosure when the tool does not embed provenance metadata. (V) https://www.cinerads.com/blog/ai-ugc-facebook-ad-policy
- Sources disagree on how strict disclosure is for ordinary commercial ads. One says no disclosure is required for regular commercial ads as of August 2026 (V) apogee; another says undisclosed AI content caused 14 percent of ad rejections in early 2026 (S) https://storrito.com/resources/meta-rejects-14-percent-of-ads-for-undisclosed-ai-content/. Check Meta's current policy page before launch.
- Generated after images in skincare, weight loss and health sit close to Meta's policy line. (V) apogee.

---

## 6. Editing and finishing

Most of this section was gathered by a helper agent that fetched each source. Commands marked (MR) were composed from documented options and are not copied from a source.

### 6.0 Blocker on this machine (checked 2026-10-04)

The installed ffmpeg (8.1.1 at `/opt/homebrew/bin/ffmpeg`) has **no `subtitles`, `ass` or `drawtext` filter**. It does have `loudnorm`, `sidechaincompress`, `acrossfade`, `xfade`, `lut3d`, `noise`, `gblur`, `unsharp`, `eq`, `colorbalance` and `minterpolate`. Homebrew's core `ffmpeg` formula no longer lists libass; the keg-only `ffmpeg-full` formula does. `ffmpeg-full` is not installed here. (V) local check, (V) https://formulae.brew.sh/formula/ffmpeg, (V) https://formulae.brew.sh/formula/ffmpeg-full

Options: `brew install ffmpeg-full` and call it by full path, or render captions outside ffmpeg (pycaps or Remotion), or draw caption frames in Python and overlay them. **(MR)** install ffmpeg-full; it is the smallest change.

### 6.1 Cut cadence

See 4.2 and 4.6. Add: TikTok and Reels viewers are mostly sound-on now (Meta says over 75 percent of Reels views are sound on), so audio quality counts as much as captions. (V) https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads/. Among seniors, four in ten prefer browsing without sound. (S) rainforgrowth page. Build for both.

### 6.2 Captions that convert

- 2 to 3 words per screen is the common default with one emphasis word per frame; 1 word is for hype; 6 or more behaves like full sentences. The only lift figure for word-by-word (about 15 percent) comes from vendor claims and is low confidence. (V) https://blitzcutai.com/blog/word-by-word-captions-vs-full-sentence-captions
- Viewers are 80 percent more likely to finish a video with captions (Verizon / Publicis 2019, n = 5,616, cited in the same article). (V) same page.
- Size: 60 to 75 px at 1080x1920 is standard, 75 to 95 px for high energy, 100 px a hard max. Vendor consensus, no study. (V) https://blitzcutai.com/blog/best-caption-size-tiktok-2026
- Font: bold weight 700 to 900 with a tall x-height. (V) https://openclip.app/guides/caption-font-guide. White text with a 5 to 8 px black outline, Montserrat Bold for direct response. (S) https://blitzcutai.com/blog/best-caption-fonts-tiktok
- Captions should lead the spoken word by 0.3 to 0.5 seconds and sit in the lower-middle of the frame, not the bottom. Hook text is far larger than body captions. (V) vidpros page.
- Keep dialogue lines under 12 words so captions stay readable. (V) aiworkflows short-drama page.
- **(MR) spec for buyers over 60:** 84 to 96 px, 2 to 3 words per page, white with a 6 px black stroke, one yellow emphasis word, each page on screen at least 0.8 seconds, placed around y = 1100 of 1920. No source gives caption specs for this age group.

### 6.3 Generating captions programmatically

**Word timings:**

- You already have the script, so force-align instead of transcribing. stable-ts `align()` aligns known text and can export ASS with highlight colors. (V) https://github.com/jianfch/stable-ts
- ElevenLabs: `POST /v1/forced-alignment` with a file and text returns words with start and end. The TTS `with-timestamps` endpoint returns character-level timings alongside the audio; you assemble words yourself. (V) https://elevenlabs.io/docs/api-reference/forced-alignment/create, (V) https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps
- faster-whisper: `model.transcribe(path, word_timestamps=True)` then read `segment.words` (each has `start`, `end`, `word`). (V) https://github.com/SYSTRAN/faster-whisper
- WhisperX: wav2vec2 forced alignment, CLI flag `--highlight_words True`. (V) https://github.com/m-bain/whisperX

**ASS karaoke facts:** `\k<centiseconds>` switches a word from secondary to primary color instantly, `\kf` sweeps it, colors are `&HBBGGRR&`. `\k` never switches a word back, so only the active word is highlighted needs one Dialogue event per word. (V) https://aegisub.org/docs/latest/ass_tags/

**Style and events (MR, built on the Aegisub spec, PlayRes 1080x1920):**

```
Style: Cap,Montserrat ExtraBold,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,5,120,120,0,1
Dialogue: 0,0:00:01.20,0:00:01.62,Cap,,0,0,0,,{\pos(540,1100)}{\1c&H00FFFF&}MY{\r} KNEES FELT
Dialogue: 0,0:00:01.62,0:00:01.95,Cap,,0,0,0,,{\pos(540,1100)}MY {\1c&H00FFFF&}KNEES{\r} FELT
```

**Burn-in (MR, needs a libass build):**

```
/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -i in.mp4 -vf "subtitles=caps.ass:fontsdir=./fonts" -c:a copy out.mp4
```

The `subtitles` filter requires `--enable-libass` and accepts `fontsdir` and `force_style`. (V) https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Video/subtitles.html

**Alternatives that avoid libass:**

- Remotion: `createTikTokStyleCaptions({captions, combineTokensWithinMilliseconds: 1200})` returns pages of tokens with `fromMs` and `toMs`. A lower value gives fewer words per page. (V) https://www.remotion.dev/docs/captions/create-tiktok-style-captions
- pycaps: Whisper plus CSS styling (a `.word-being-narrated` class) rendered through Playwright. `pycaps render --input my_video.mp4 --template minimalist`. (V) https://github.com/francozanardi/pycaps

### 6.4 Sound design and loudness

- TikTok and Reels publish no exact loudness spec. -14 to -16 LUFS is the safe range; YouTube normalizes to -14 LUFS at -1 dBTP. (V) https://openclip.app/learn/audio-normalization. Editors commonly target -14 LUFS with -1.0 to -1.5 dBTP for both. (S) https://opus.pro/blog/best-loudness-normalizers
- **(MR) master target:** -14 LUFS integrated, -1.5 dBTP, 48 kHz stereo AAC.
- loudnorm defaults are I = -24, LRA = 7, TP = -2. Linear mode needs the measured values from a first pass. Dynamic mode upsamples to 192 kHz, so add `-ar 48000`. (V) https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Audio/loudnorm.html

Two-pass loudnorm (pattern from the cited guide, with the target swapped to -14):

```
ffmpeg -i in.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | tail -12
ffmpeg -i in.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<..>:measured_TP=<..>:measured_LRA=<..>:measured_thresh=<..>:offset=<..>:linear=true" -ar 48000 -c:v copy out.mp4
```

(V) https://dev.to/javidjamae/ffmpeg-loudnorm-filter-ebu-r128-loudness-normalization-guide-15d4

- **Music under voice:** duck 6 to 12 dB with attack 30 to 80 ms and release 250 to 700 ms. (S) https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video. A broadcast study figure puts music 16 to 23 LU under speech. (S) https://salford-repository.worktribe.com/OutputFile/1486952. **(MR)** for listeners over 60, keep the bed 18 to 20 dB under the voice.
- **Ducking in ffmpeg:** `sidechaincompress` defaults are threshold 0.125, ratio 2, attack 20 ms, release 250 ms. (V) https://ayosec.github.io/ffmpeg-filters-docs/7.1/Filters/Audio/sidechaincompress.html

```
# (MR) music ducked by the voiceover
ffmpeg -i music.wav -i vo.wav -filter_complex "[1:a]asplit=2[sc][mix];[0:a][sc]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=400[duck];[duck][mix]amix=inputs=2:duration=longest:normalize=0" out.wav
```

- **Build order and hierarchy:** ambience bed first, foley on visible beats, music last. Priority is dialogue, then foley, then ambience, then music. (V) https://hackernoon.com/ai-video-comes-out-silent-here-is-the-sound-design-workflow-i-run-on-every-shot
- **Room tone (MR):** lay one continuous room-tone bed under the whole timeline at about -45 to -50 dBFS. It hides the audio seams between clips that were generated separately. Crossfade clip audio by about 0.25 seconds at joins (`acrossfade` is available locally).
- **One voice (MR):** generate the full voiceover as one file from one voice, or convert every native clip voice to one target voice, before mixing. See the voice row in 2.6.

### 6.5 Color and grain unification

See 2.7 and 3.6. Order: per-clip color match to the scene's hero frame, upscale, light soften, one shared grain layer over the entire timeline, one shared grade. The shared grain layer is what makes clips from different models read as one camera. **(MR)**, supported by (V) invideo grain FAQ.

### 6.6 Upscaling and frame rate

- AI clips usually arrive at 720p or 1080p. SeedVR2 is strong on soft AI output; per-frame image upscalers such as Real-ESRGAN flicker in motion. (V) https://upsampler.com/blog/upscale-ai-generated-video-sora-veo-kling-wan-2026
- Topaz has diffusion upscalers aimed at AI video, including one meant to reduce the plastic look. (S) https://invideo.io/blog/topaz-video-enhancement-models/. Topaz video upscale is on Kie at 1x, 2x and 4x with a 50 MB input limit. (V) https://docs.kie.ai/market/topaz/video-upscale.md
- Keep upscaler denoise low (about 15 to 30 on a 0 to 100 scale) and turn skin smoothing off. (S) invideo post-production pipeline page.
- Models differ in frame rate: Seedance 2.5 is 24 fps, Wan 3.0 about 30 fps. (V) fal Seedance 2.5 workflows page, (V) cometapi Wan page. Reels want at least 30 fps. (S) https://help.instagram.com/1038071743007909. Meta's ads guide only requires a fixed frame rate. (V) Meta ads guide below.
- **(MR)** render at the highest native resolution you can afford (1080p), upscale 720p clips once before grain, and conform the whole timeline to 30 fps with plain `fps=30`. Use motion interpolation only on shots where pans visibly judder; it warps across cuts.

### 6.7 Export specs and safe zones

- **Meta Reels ads:** MP4 or MOV, 9:16, H.264, square pixels, fixed frame rate, progressive scan, stereo AAC at 128 kbps or more, max 4 GB. The recommended resolution is now 1440x2560. Captions optional but recommended. (V) https://www.facebook.com/business/ads-guide/update/video/instagram-reels
- **Meta safe zone:** keep the top 14 percent, the bottom 35 percent and 6 percent on each side clear of text and logos. At 1080x1920 that is about 269 px top, 672 px bottom, 65 px each side. Stories and Reels have shared one safe zone since March 2026. (V) same Meta page, (V) https://billo.app/blog/meta-ads-safe-zones
- Ads that violated the Reels safe zone averaged 28 percent lower CTR. (S) https://blog.adobe.com/en/publish/2024/11/04/unlock-potential-reels-best-practices-for-creative-success-using-adobe-creative-cloud
- **TikTok in-feed (non-Spark):** 9:16 at 540x960 or more, mp4 / mov / mpeg / 3gp / avi, up to 10 minutes, 500 MB or less, 516 kbps or more. Safe zone depends on caption length and ships as templates. (V) https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads?lang=en. A third-party reading of those templates: top 240, bottom 660, left 120, right 120 px, plus 300 px on the right below y = 840. (V) https://adkit.so/tools/safe-zones/tiktok
- **(MR) one caption box that clears both platforms at 1080x1920:** x from 120 to 780, y from 270 to 1245.

Export command **(MR)**:

```
ffmpeg -i master.mov -vf "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p" \
  -c:v libx264 -profile:v high -level 4.2 -preset slow -crf 18 -maxrate 12M -bufsize 24M -g 60 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart out.mp4
```

Open question: Meta now recommends 1440x2560. **(MR)** 1080x1920 remains fine because source clips are 1080p at best; exporting larger only upsamples.

---

## 7. End-to-end pipelines people have published

Headline: no one has published a fully automatic vision-model re-roll loop with thresholds for ads. The closest are a Google research system, one skill that scores clips but never re-rolls on its own, and human approval gates before the expensive step.

### 7.1 n8n templates

| Template | Steps | Models | Lessons |
|---|---|---|---|
| Ads Factory | Sheet row with script, character and setting; agent writes selfie prompt; start image; vision model describes it; LLM splits script into 8 s scenes; each scene to Veo; poll; merge | Kie Nano Banana, Kie Veo 3, Claude Opus, fal ffmpeg | retries with a 5 s delay; no QA step (V) https://n8n.io/workflows/14316-ads-factory-generate-unlimited-length-ugc-ai-video-pipeline/ |
| Viral video (Dr. Firas) | Telegram photo + idea; vision analysis; UGC image prompt; image; structured Veo prompt; one 8 s 9:16 clip; publish | Nano Banana 2 Pro, Veo 3.1, fal, Blotato | single clip, no stitch, no QA (V) https://n8n.io/workflows/11204-create-ai-viral-videos-using-nanobanana-2-pro-and-veo31-and-publish-via-blotato/ |
| UGC from product images | Gemini improves the image; Claude writes script; Veo 3 Fast renders | Gemini 2.5 Flash, Claude Sonnet 4, Kie Veo 3 Fast | add delays for rate limits; lengthen waits for timeouts; scripts must respect the physical limits of the source image (V) https://n8n.io/workflows/8927-generate-ugc-videos-from-product-images-with-gemini-and-veo3/ |
| Sheets + Nano Banana Pro + Veo 3.1 | sheet-driven UGC | Nano Banana Pro, Veo 3.1 | (S) https://n8n.io/workflows/12752-generate-ugc-style-ai-videos-with-google-sheets-nanobanana-pro-and-veo-31/ |
| 60 second ad (Zubair Trabzada, via a write-up) | one base image of person with product; repeated 8 s Veo clips each anchored to that same image with a running summary and repeated outfit and hair descriptors; ffmpeg concat | Nano Banana Pro, Veo 3.1, fal | $1 to $7 per ad; says nothing about voice consistency or lip-sync (V) https://www.stork.ai/blog/pt/this-ai-creates-perfect-60-second-ads |

**(MR)** every template is the same skeleton: one anchor image, N clips of 8 seconds, concat. None has a visual QA step and none builds captions. That is the gap the skill should fill.

### 7.2 GitHub repos and skills

- **mikefutia/claymation-ads-claude-skill** (closest analog). Brief, then script and cast, then a style lock and one master image per character, then scene keyframes that reference the masters and the previous still, then voiceover, then clips generated between pairs of stills on Gemini Omni Flash (4 s, 720p), then ffmpeg stitch. Five approval gates with rising spend (free, free, about $0.30, about $0.60, about $5.70). $6 to $8 and about 30 minutes for a 10 to 11 scene ad. Project state is saved so one clip can be repaired and re-stitched for free. (V) https://github.com/mikefutia/claymation-ads-claude-skill
- **0xadvait/ai-video-skill.** Seven stages: still, prompt, generate, QC and learn, voiceover, assemble, finish. Auto-routing: audio references or two or more image references go to Seedance 2.0; single-image jobs go to Wan 2.7; classifier-flagged jobs fall back to Kling 3.0 Omni; a plain talking head goes to OmniHuman 1.5. Dialogue lines are held to 4 to 10 words. It keeps a `LESSONS.md` that every run reads first. (V) https://github.com/0xadvait/ai-video-skill
- **HKUDS/ViMax.** Idea, script and novel to video. Generates keyframe candidates in parallel and has a vision-capable model select one. Tracks reference images, first frames and camera continuity. (V) https://github.com/HKUDS/ViMax
- **krusemediallc/video-editor-agent.** QA on the rendered MP4: contact sheets, loudness checks, seam checks, optional Gemini watch-and-listen. Its rule, in its own words: "verify pixels and dB, not intentions". It also refuses to label a skipped check as a pass. (V) https://github.com/krusemediallc/video-editor-agent
- **digitalsamba/claude-code-video-toolkit.** Remotion + ffmpeg with phase state in a project file and a human scene review. The author calls full autonomy a lofty ideal. (V) https://github.com/digitalsamba/claude-code-video-toolkit
- **Kie's own agent skills.** `kie-models` searches the live model list, loads the model's input fields, uploads files, submits, polls and downloads. It is a single-task runner with no storyboard, consistency, QA or assembly layer. Its habit of reading the live schema before each call is worth copying. (V) https://docs.kie.ai/ai-agent/overview.md, (V) https://docs.kie.ai/ai-agent/what-can-do.md
- Prompt libraries: https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts, https://github.com/ofoxai/awesome-ai-video-prompts (Seedance 2.5, Hailuo 3, Wan 3.0 cases), https://github.com/cnemri/awesome-gemini-omni. (V) repo listings via GitHub search, contents only sampled.

### 7.3 QA and review loops

- **VISTA (Google research).** Per iteration it generates about 30 Veo 3 videos, picks winners by pairwise tournament judged by Gemini 2.5 Flash (comparisons run in both orders to cancel position bias, critique written before the pick), scores on visual fidelity, physical commonsense, text-video alignment, audio-video alignment and engagement, then a separate agent rewrites the prompt. Humans preferred its output 66.4 percent of the time. About 0.7M tokens per iteration. (V) https://arxiv.org/html/2510.15831
- **Character.ai talk on evaluating video.** Evaluate at three points: start frames, each clip before assembly, the full sequence. Pairwise comparison beat absolute scores. Their first judge rewarded visual gloss (it praised camera work on static images). Score the specific axes you care about. (V) https://www.ai.engineer/talks/b_PmGocP4rc-evaling-video-slop
- **ai-video-skill QC.** Extracts a contact sheet plus sampled frames, has the model score 1 to 5 on prompt fidelity, subject consistency, camera and motion, audio match and overall, and appends a one-line lesson to `LESSONS.md`. It does not regenerate unless asked. Its failure list is a ready rubric: hand drift, glyph-soup text, fast-motion warping, unrequested cuts, plastic skin, face flicker, and silent failures (a 200 response with an empty result). (V) https://github.com/0xadvait/ai-video-skill
- **Gemini video understanding.** Samples at 1 fps by default with a custom fps option and clip offsets; about 258 tokens per frame plus 32 tokens per second of audio; inline upload under 100 MB. Fast action loses detail at 1 fps. (V) https://ai.google.dev/gemini-api/docs/video-understanding
- **Benchmarks worth knowing:** VideoScore2 (visual quality, text alignment, physical consistency) and VBench-2.0 (18 dimensions including human fidelity). (S) https://arxiv.org/pdf/2509.22799, (S) https://arxiv.org/html/2503.21755v2

### 7.4 Recommended QA loop for the skill (MR)

1. **Stills gate (cheap).** 2 or 3 start-frame candidates per shot. A vision model compares them pairwise against the master portrait and the shot spec. Pass or fail on named axes: identity match, hands, stray text, wardrobe and props, composition inside the caption safe zone.
2. **Clip gate.** For each clip build a contact sheet (first, middle, last, plus 2 fps frames across speech). Checks, each pass or fail:
   - identity against the master portrait
   - hands and object contact
   - burned-in text or subtitles on any frame
   - unrequested cuts (ffmpeg scene-change detection)
   - action reached the stated end state
   - spoken line matches the script (transcribe the clip audio and compare)
   - music present when none was asked for
   - empty or truncated file
3. **Retry policy.** At most 2 re-rolls per clip. Change the prompt using the named failure before each retry. Third attempt goes to the fallback model for that shot type.
4. **Assembly gate.** Loudness, seam frames, caption box inside the safe zone, total duration against the voiceover.
5. **Cost control.** Draft at low resolution where the model allows (480p is roughly 2.25x cheaper on Seedance 2.5 per the segmind test) and render finals at 1080p only after the stills and the script timing pass.
6. **State.** Save every asset and its spec per shot so one clip can be repaired and the stitch re-run for free.
7. **Memory.** Append one cause-and-effect lesson per failed clip to a lessons file that is read at the start of every run.

### 7.5 Kie API facts and pitfalls

- Create: `POST https://api.kie.ai/api/v1/jobs/createTask`. Poll: `GET /api/v1/jobs/recordInfo?taskId=`. States: `waiting`, `queuing`, `generating`, `success`, `fail`. Results arrive in `resultJson` only on success; failures carry `failCode` and `failMsg`. (V) https://docs.kie.ai/market/quickstart.md, (V) https://docs.kie.ai/market/common/get-task-detail.md
- Veo 3.1 uses its own endpoints under the veo3-api section, not the Market createTask route. (V) https://docs.kie.ai/veo3-api/generate-veo-3-video.md
- Rate limit: 20 new generation requests per 10 seconds per account, 100+ concurrent tasks, HTTP 429 beyond that. A 200 only means the task was created. (V) https://docs.kie.ai/1973359m0.md
- Polling: start at 2 to 3 seconds, back off, stop after 10 to 15 minutes. (V) task-detail page. A 30 second Seedance 2.5 job took up to 458 seconds elsewhere, so allow at least 600. (V) segmind page.
- **Retention conflict:** one page says generated media is stored 14 days, another says result URLs typically expire after 24 hours. Download every result the moment it succeeds. (V) getting-started and task-detail pages.
- **Upload expiry conflict:** the file upload page gives 24 hours in one place and 3 days in another; the response includes `expiresAt`. Re-upload references for any re-roll a day later. (V) https://docs.kie.ai/file-upload-api/quickstart.md
- Veo errors: 400 for flagged prompt or unsafe image, 422 for requests rejected over minors or prominent people, 501 generation failed, 455 maintenance, 402 no credits. (V) https://docs.kie.ai/veo3-api/generate-veo-3-video-callbacks.md
- Callbacks need a public server that answers within 15 seconds. A local CLI skill should poll. (V) https://docs.kie.ai/common-api/webhook-verification.md, (MR)
- Not documented: whether credits are refunded on failed generations.

---

## 8. Rules that matter most (top 25, ranked by impact)

| # | Rule | Source |
|---|---|---|
| 1 | Build every shot from a start frame made from one locked master portrait. Never text-to-video a recurring character. | (V) dxbuilder, (V) pigeondigital, (V) PostmindStudio PR #103 |
| 2 | One action per clip, with a stated start state and end state. | (V) Runway guide, (V) kylon, (V) segmind micro-drama |
| 3 | Generate the voiceover first and size every shot from measured audio. | (V) claymation skill, (V) humzakt post |
| 4 | Every shot shows the exact thing the words name. Write each shot as subject, framing, movement, duration and job. | (V) storyflow, (MR) |
| 5 | In image-to-video prompts describe only motion, camera and sound. Do not re-describe the person. | (V) dxbuilder, (V) Kling i2v guide |
| 6 | Gate at the cheapest stage: pick from 2 or 3 start-frame candidates before paying for video. | (V) humzakt post (about 40 percent fewer regenerations), (V) ViMax |
| 7 | Keep dialogue short: about 15 words or fewer per 8 second clip, one idea per line, 6 to 10 words for UGC. | (V) veo3gen.app, (V) aivideosensei |
| 8 | Name the audio in every prompt and say no music. Turn audio off for voiceover b-roll. | (V) aivideosensei, (V) fal Seedance guide, (V) Runware Omni guide |
| 9 | Kill subtitles at the prompt: no quotes or apostrophes around Veo dialogue, speech first, inline ban; No subtitles on Seedance. Leave bottom headroom. | (V) veo3ai.io, (V) Runware Seedance guide |
| 10 | Use one voice source for the whole ad. Native clip voices change every generation. | (S) hackernoon voice article, (V) skaleit |
| 11 | Prompt for phone physics and real skin, and ban cinematic words (8K, cinematic, studio light, 85mm, bokeh). | (V) dxbuilder, (V) youmind UGC recipe |
| 12 | Attach the real product photo to every frame that shows the product. Put all text, prices and headlines on in post. | (V) claymation skill, (V) apogee |
| 13 | Do not chain by last frame more than twice. Re-anchor every clip to the original references and prefer a cut to a new angle. | (V) hackernoon extend article, (V) invideo drift FAQ |
| 14 | Re-roll with a changed prompt, never the same prompt. Cap retries and fall back to another model. | (V) veo3ai.io, (V) ai-video-skill |
| 15 | State the camera explicitly: locked or one named move, and no cuts. Unstated cameras drift or start editing. | (V) fal Kling guide, (V) segmind Wan guide, (V) Runware Omni guide |
| 16 | Route by shot type: Veo for speech close-ups, Kling for multi-shot dialogue and cheap b-roll, Seedance for recurring characters and product text. | (V) invideo micro-drama routing, (V) mindstudio comparison |
| 17 | Assign every reference image a role and an exclusion (identity only, ignore its background). One reference, one subject. | (V) kylon, (V) rendley |
| 18 | With reference mode and no start frame, reuse one identical character descriptor block word for word. | (V) atlascloud Kling guide, (V) Dinsmore Veo deep dive |
| 19 | Finish in this order: color match per clip, upscale, light soften, one shared grain layer, one shared grade. Never sharpen. | (V) invideo plasticky FAQ, (V) invideo grain FAQ |
| 20 | First frame works as a still, motion starts inside the first second, first jolt before 1.5 seconds, value shown by second 7. | (V) inceptly, (V) vidpros, (V) segwise |
| 21 | Keep all text inside the safe zone: clear the top 14 percent, bottom 35 percent and 6 percent sides on Meta. | (V) Meta ads guide |
| 22 | Captions: 2 to 3 words per page, bold, high contrast, one highlight word, lower-middle of frame. Larger for older buyers. | (V) blitzcutai, (V) vidpros, (MR) |
| 23 | Master to -14 LUFS and -1.5 dBTP with two-pass loudnorm; duck music under voice; lay room tone under every seam. | (V) openclip, (V) loudnorm docs, (MR) |
| 24 | QA with named pass or fail axes, compare pairwise, and check the rendered file, not the plan. | (V) Character.ai talk, (V) VISTA, (V) video-editor-agent |
| 25 | Save per-shot state and keep a lessons file read at the start of every run. Download Kie results immediately. | (V) claymation skill, (V) ai-video-skill, (V) Kie docs |

---

## 9. Open conflicts and gaps

- **Reddit was not reachable.** The search tool cannot access reddit.com, so r/aivideo, r/VEO3, r/KlingAI_Videos, r/FacebookAds and r/dropshipping threads were not read. Community findings here come from blogs, newsletters, GitHub and vendor guides that summarize them.
- **YouTube tutorials** were only seen through written summaries.
- **Seedance 2.5 audio brackets:** guides disagree on whether bracket types route music, SFX and dialogue. Use plain labeled lines and quotes until tested.
- **Seedance 2.5 max resolution:** third-party hosts say 720p; Kie's schema lists 1080p.
- **Grok Imagine 1.5 text-to-video:** sources disagree. Treat as image-led.
- **Veo dialogue punctuation:** Google's guide uses quotation marks; creators report fewer subtitles without them. Test both on Kie.
- **Meta AI disclosure for ordinary commercial ads:** sources disagree. Check the live policy.
- **No source** gives cut cadence, caption size or pacing data specific to buyers over 60. Those recommendations are marked (MR).
- **Official pages that did not load:** the BytePlus Seedance 2.5 prompt guide body, Kling's own prompt syntax blog post, Google's Vertex video prompt guide body. Their content is represented through guides that cite them.
- **Kie model ids** in section 0 come from schema examples. Read the live schema before each call, as Kie's own agent skill does.
- **Not researched here:** lip-sync models (InfiniteTalk, Kling AI Avatar, OmniHuman), covered by the other researcher.
