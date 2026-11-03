# Kie.ai API reference for the talking-character video ad pipeline

Pulled live on 2026-10-04. Scope: everything on Kie that helps turn an ad script into a finished talking-character video with Python + ffmpeg.

## How to use this file

- Sections 0 to 7 are the curated reference (read these).
- Appendix A is the per-model spec, machine-extracted from the OpenAPI block of each docs page: every parameter, allowed values, limits, and the exact request JSON from the doc. Grep it by model id, for example `grep -n '#### `kling/ai-avatar-pro`' kie-api.md`.
- Appendix B is the full Kie price list for video, music, and image models, pulled from the same endpoint the pricing page uses.
- Appendix C is the list of things that are NOT on Kie today.

### Sources

| Tag | Source | Notes |
|---|---|---|
| [doc] | https://docs.kie.ai (index https://docs.kie.ai/llms.txt, 536 pages, each has a `.md` variant) | `llms-full.txt` returns 404. All English pages were pulled as raw markdown and parsed, not summarized. |
| [old-doc] | https://docs.kie.ai/old-model/llms.txt | Legacy dedicated endpoints (Veo, Runway, Suno, 4o Image, Flux Kontext) now live here. |
| [live] | `GET https://api.kie.ai/api/v1/models` with the API key | Returned 218 models on 2026-10-04. This is the best truth for "can I call this model id". |
| [price] | `POST https://api.kie.ai/client/v1/model-pricing/page` (public, no key) | 524 price rows. This is what https://kie.ai/pricing renders. |
| [site] | https://kie.ai/<model page> embedded page data | Per-model `pricingDesc`, playground form limits, FAQ text. Marketing copy, so weaker than [doc]. |
| [inferred] | My reasoning from the above | Marked every time. Verify before relying on it. |

"Not documented" means no doc page, price row, or site page states it. No generation task was created and no credits were spent to build this file, so result shapes that the docs do not show are flagged as unverified.

---

## 0. Read this first (what changed and what will bite)

1. **Everything is on the unified task API now.** The current docs describe Veo 3.1, Runway, Suno, 4o Image, and Flux Kontext as `model` values on `POST /api/v1/jobs/createTask` (`veo-3-1`, `veo/extend`, `veo/get-1080p-video`, `veo/get-4k-video`, `runway`, `runway/extend-ai-video`, `ai-music-api/generate`, `4o-image-api`, `flux1-kontext`). Each of those pages opens with a warning that links to the old version under `https://docs.kie.ai/old-model/...`. The old dedicated endpoints (`/api/v1/veo/generate`, `/api/v1/veo/record-info`, and so on) are still documented there. [doc] [old-doc]
2. **Sora 2 is gone.** No Sora page in the docs index (the old slugs return 404), zero Sora rows in the price list, no Sora id in the live model list, and https://kie.ai/sora-2 is a 404. Leftovers that still mention it: a stale card on the Market quickstart page, the `progress` field note in Get Task Details, and stale ids in the playground list. Do not build on Sora 2, storyboard, characters/cameo, or the watermark remover. [doc] [live] [price]
3. **ElevenLabs on Kie is TTS only.** Live ids: `elevenlabs/text-to-speech-turbo-2-5`, `elevenlabs/text-to-speech-multilingual-v2`, `elevenlabs/text-to-dialogue-v3`. Speech-to-text and sound effects have no doc page (404), no price row, and are not in the live list. `elevenlabs/audio-isolation` still has a doc page but is NOT in the live list and has no price row. There is no voice changer and no voice cloning. [doc] [live] [price]
4. **Word timestamps are a risk.** Both ElevenLabs TTS models take `timestamps` (boolean, "Whether to return timestamps for each word in the generated speech"). The docs do not show where the timestamps come back (the documented result is `{"resultUrls":[...]}`). Spend one cheap TTS call (about 1 credit) to look at the raw `resultJson` before designing captions around it. Fallback that needs no Kie model: run whisper locally on the returned mp3. [doc] [inferred]
5. **InfiniteTalk is capped at 15 seconds per task on Kie** even though the model itself is "infinite length". Kling AI Avatar is the long-form option: the doc says audio up to 5 minutes. [doc] [site]
6. **New audio inputs on general video models.** `wan/2-7-image-to-video` takes `driving_audio_url`. `wan/2-7-text-to-video` takes `audio_url`. `bytedance/seedance-2`, `-2-fast`, `-2-mini`, `-2-5`, `wan/3-0-video`, `wan/3-0-video-prime`, and `minimax-h3/reference-to-video` take `reference_audio_urls`. `kling-3.0/video` and `kling-3.0-omni/*` take a per-character voice clip (`element_input_audio_urls`, 5 to 30 s). `wan/2-7-r2v` takes `reference_voice` (1 to 10 s). See section 3.3.
7. **Veo 3.1 tier selection is not documented in the new docs.** The new page only shows `"model": "veo-3-1"` and never says how to pick Fast, Quality, or Lite, though the prose and prices name all three. The legacy endpoint uses `model` = `veo3` (Quality), `veo3_fast`, `veo3_lite`. Until Kie documents it, the safe path for Veo is the legacy `/api/v1/veo/generate` endpoint. [doc] [old-doc]
8. **Retention statements conflict.** Generated media: "stored for 14 days" (Getting Started) versus "Generated content URLs typically expire after 24 hours" (Get Task Details). Uploaded files: "deleted after 24h" (page banners) versus "deleted after 3 days" (feature lists on the same pages). Treat both as 24 hours: download results as soon as the task succeeds and re-upload inputs per run. [doc]
9. **Price labels lag the docs.** The price list still labels Kling AI Avatar and InfiniteTalk as "up to 15 seconds" and links the avatar rows to old ids (`kling/v1-avatar-standard`, `kling/ai-avatar-v1-pro`). Those old ids are not in the live list. Use `kling/ai-avatar-standard` and `kling/ai-avatar-pro`. [price] [live]
10. **1 credit = $0.005. Verified.** The price rows hold that ratio (6 credits = $0.03, 16 credits = $0.08, 250 credits = $1.25), apart from a few obvious typos in Kie's own table (for example one Grok row lists 8 credits as $0.004). The pricing copy also says higher top-up tiers add a 10% credit bonus, which lowers the effective price about 10%. [price] [site]
11. **Kie ships an official agent skill.** `npx skills add https://kie.ai` installs `kie-models`, which reads the live model list, uploads inputs, submits, polls, and saves. It was not installed or downloaded for this research. The live list endpoint in the Sources table was found by probing and is not in the docs. [doc] [live]

---

## 1. Core mechanics

### 1.1 Auth and headers [doc]

```http
Authorization: Bearer <KIE_API_KEY>
Content-Type: application/json
```

Base URL `https://api.kie.ai`. Missing or bad key, verified live: `{"code":401,"msg":"Unauthorized – Authentication failed. Please check that your Authorization and Content-Type headers are correctly set."}`

Key management at https://kie.ai/api-key supports per-key hourly, daily, and total credit caps plus an IP whitelist. Task history with credit use: https://kie.ai/logs.

### 1.2 Create a task [doc]

`POST https://api.kie.ai/api/v1/jobs/createTask`

```json
{
  "model": "kling/ai-avatar-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": { "...model specific fields...": "..." }
}
```

- `model` (string, required): exact id from Appendix A.
- `callBackUrl` (string, optional): Kie POSTs the final status here.
- `input` (object): model-specific. Field naming is not consistent across models (`image_url` vs `image_urls` vs `input_urls` vs `image_input` vs `first_frame_url`), so copy the names from Appendix A every time.
- Many fal-backed models also accept `input.nsfw_checker` (boolean, "Defaults to false").

Success response (HTTP 200 only means the task was created):

```json
{"code":200,"msg":"success","data":{"taskId":"task_kling_1765186008504"}}
```

ElevenLabs examples also return a `recordId`: `{"code":200,"msg":"success","data":{"taskId":"task_elevenlabs_1765185518880","recordId":"elevenlabs_1765185518880"}}`.

### 1.3 Poll a task [doc]

`GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=<taskId>`

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "taskId": "task_12345678",
    "model": "grok-imagine/text-to-image",
    "state": "success",
    "param": "{\"model\":\"grok-imagine/text-to-image\",\"callBackUrl\":\"https://your-domain.com/api/callback\",\"input\":{\"prompt\":\"Cinematic portrait...\",\"aspect_ratio\":\"3:2\"}}",
    "resultJson": "{\"resultUrls\":[\"https://example.com/generated-content.jpg\"]}",
    "failCode": "",
    "failMsg": "",
    "costTime": 15000,
    "completeTime": 1698765432000,
    "createTime": 1698765400000,
    "updateTime": 1698765432000,
    "progress": 45,
    "creditsConsumed": 50
  }
}
```

(The doc's own example shows `"code": 505` at the top, which is a typo in the doc. Real success is 200.)

- `state`: `waiting` (queued), `queuing` (in the processing queue), `generating`, `success`, `fail`.
- `resultJson` is a JSON **string**, present only on success. Shapes:
  - media: `{"resultUrls":["..."]}`
  - Seedance 2 / 2 Fast with `return_last_frame`: `{"resultUrls":[],"firstFrameUrl":[],"lastFrameUrl":[]}`
  - text output: `{"resultObject":{...}}`, for example OmniHuman subject detection `{"resultObject":{"mask_urls":["url1","url2"]}}` (those URLs live 1 hour) and human identification `{"resultObject":{"subject_status":1}}`.
- `param` is a JSON string of the original request. `costTime` is milliseconds. Timestamps are Unix milliseconds.
- `creditsConsumed`: actual credits charged. Log this per task for cost tracking.
- `progress` (0 to 100): doc says "Only returned when model is sora2 or sora2 pro", so treat it as absent.
- Unknown task id, verified live: `{"code":422,"msg":"recordInfo is null","data":null}`.
- Doc best practice: start polling at 2 to 3 second intervals and back off, stop after 10 to 15 minutes, "Download results immediately". For Veo 1080p/4K upgrades the docs suggest 20 to 30 s+ intervals.

### 1.4 Callbacks [doc]

Kie POSTs JSON to `callBackUrl` when the task ends:

```json
{
  "code": 200,
  "msg": "Playground task completed successfully.",
  "data": {
    "taskId": "task_example_video_webhook_001",
    "model": "kling/ai-avatar-pro",
    "state": "success",
    "param": "{...original request as a JSON string...}",
    "resultJson": "{\"resultUrls\":[\"https://example.com/generated-video.mp4\"]}",
    "failCode": null,
    "failMsg": null,
    "costTime": 0, "completeTime": 0, "createTime": 0, "updateTime": 0,
    "creditsConsumed": 0
  }
}
```

- `code` is `200` on success and `501` on failure. `msg` is `Playground task completed successfully.` or `Playground task failed.`. `state` is `success` or `fail`. On failure `resultJson` is null and `failCode` / `failMsg` are set.
- Optional signature check (https://docs.kie.ai/common-api/webhook-verification): turn on a `webhookHmacKey` at https://kie.ai/settings. Kie then sends `X-Webhook-Timestamp` (Unix seconds) and `X-Webhook-Signature` = `base64(HMAC-SHA256(taskId + "." + timestamp, webhookHmacKey))`.
- A local Python pipeline has no public URL, so polling is the practical route. [inferred]

### 1.5 Response codes [doc]

| Code | Meaning |
|---|---|
| 200 | Success (task created, or query OK) |
| 400 | Bad request (for example missing `taskId`) |
| 401 | Unauthorized |
| 402 | Insufficient credits |
| 404 | Not found |
| 408 | Upstream service issue, no result for over 10 minutes |
| 422 | Validation error (also returned for an unknown task id) |
| 429 | Rate limited |
| 433 | Sub-key usage exceeded its limit |
| 455 | Maintenance |
| 500 | Server error |
| 501 | Generation failed |
| 505 | Feature disabled |

Per-task failures show up as `state: "fail"` with `failCode` and `failMsg`. The list of possible `failCode` values is not documented.

### 1.6 Limits and retention [doc]

- "Up to 20 new generation requests per 10 seconds", "typically allows 100+ concurrent running tasks", applied per account. Over the limit returns HTTP 429 and "Rejected requests will not enter the queue", so retry with backoff.
- Generated media: 14 days per Getting Started, 24 hours per Get Task Details. Log records: 2 months.
- Result URLs are served from Kie temp hosts (`tempfile.aiquickdraw.com`, `file.aiquickdraw.com`, `tempfile.redpandaai.co`). The house script downloads them with a browser User-Agent (`-A "Mozilla/5.0"`), keep doing that.
- "All generation tasks on KIE are asynchronous."
- Stability: Kie states its "overall stability may be slightly lower than official providers". Build retries.

### 1.7 Other common endpoints

| Endpoint | Purpose | Notes |
|---|---|---|
| `GET /api/v1/chat/credit` | Credit balance | Returns `{"code":200,"msg":"success","data":<number>}`. Verified live. [doc] |
| `POST /api/v1/common/download-url` | Turn a Kie result URL into a temporary direct download link | Body `{"url":"<kie file url>"}`. Link valid 20 minutes. Kie URLs only, others get 422. [doc] |
| `GET /api/v1/models` | Live list of callable model ids with `taskType`, `provider`, `pricingDesc` | Needs the key. Not in the docs. No per-model parameter schema here. [live] |
| `POST /client/v1/model-pricing/page` | Full price list | Public. Body `{"pageNum":1,"pageSize":100}`, optional `interfaceType` (`image`, `video`, `music`, `chat`) and `modelDescription` search. [price] |
| `GET /api/v1/playground/model-paths` | Playground model ids | Public. Contains stale ids (Sora, old avatars, ElevenLabs STT). Do not trust it for availability. [live] |

### 1.8 Legacy dedicated endpoints versus the unified API

| Family | Legacy endpoints [old-doc] | Unified `model` ids [doc] | Differences that matter |
|---|---|---|---|
| Veo 3.1 | `POST /api/v1/veo/generate`, `GET /api/v1/veo/record-info?taskId=`, `GET /api/v1/veo/get-1080p-video?taskId=&index=`, `POST /api/v1/veo/get-4k-video`, `POST /api/v1/veo/extend` | `veo-3-1`, `veo/get-1080p-video`, `veo/get-4k-video`, `veo/extend` | Legacy params are top-level and mostly camelCase (`imageUrls`, `generationType`, `enableTranslation`; `aspect_ratio` stays snake_case), and legacy `model` picks the tier. Unified params sit in `input` as snake_case (`image_urls`, `generation_type`, `enable_translation`). Legacy status is `successFlag` (0 generating, 1 success, 2 failed, 3 generation failed) with results in `data.response.resultUrls`. Unified field naming is uneven: the `veo/get-1080p-video` doc uses `input.taskId` (its playground form on kie.ai uses `task_id`), while `veo/get-4k-video` and `veo/extend` use `input.task_id`. Tier hint [site]: the playground form for `veo/extend` has a `model` field with options `fast`, `quality`, `lite` (default `fast`). The doc pages do not list that field, so treat it as unconfirmed. |
| Runway | `POST /api/v1/runway/generate`, `GET /api/v1/runway/record-detail`, `POST /api/v1/runway/extend` | `runway`, `runway/extend-ai-video` | No audio. |
| Runway Aleph | `POST /api/v1/aleph/generate`, `GET /api/v1/aleph/record-info` | `runway/gen4-aleph` in the doc, but that id is NOT in the live list | Use the legacy endpoint if you need Aleph. |
| Suno | `POST /api/v1/generate`, `GET /api/v1/generate/record-info`, `POST /api/v1/generate/sounds`, `POST /api/v1/generate/get-timestamped-lyrics` | `ai-music-api/generate`, `ai-music-api/sounds`, `ai-music-api/timeStamped-lyrics`, and the rest of `ai-music-api/*` | Unified version takes `input.model` = `V6`, `V6_MINI`, `V6_WILD` (older versions are marked discontinued). |
| 4o Image | `POST /api/v1/gpt4o-image/generate`, `GET /api/v1/gpt4o-image/record-info` | `4o-image-api` | |
| Flux Kontext | `POST /api/v1/flux/kontext/generate`, `GET /api/v1/flux/kontext/record-info` | `flux1-kontext` | |
| Gemini Omni voices and characters | none | `POST /api/v1/omni/audio/create`, `POST /api/v1/omni/character/create` | These two are their own endpoints, not createTask. They return ids used by the Gemini Omni video models. |

Whether the unified ids for Veo, Runway, and Suno behave exactly like the legacy endpoints is not verified here (no task was run).

### 1.9 House call pattern

`/Users/ryanconnolly/SkyHouse Exodus/offers/reactivate/images/lander-salt-longform/kie.py` already implements `post()` (createTask), `info()` (recordInfo), `upload()` (base64 upload to `kieai.redpandaai.co`), and `wait()` (poll every 12 s, read `json.loads(d["resultJson"])["resultUrls"][0]`, download with a browser User-Agent). Two things to change for video work:

- `upload()` hardcodes the `data:image/png;base64,` prefix. For mp3, wav, and mp4 use the stream upload in section 2.
- `wait()` saves everything as `.png` and stops at 900 s. Video tasks need a longer timeout and the right extension.

---

## 2. File upload API (local file to a URL Kie models accept)

Docs: https://docs.kie.ai/file-upload-api/quickstart

- **Base URL: `https://kieai.redpandaai.co`** per the quickstart and every code sample. (The OpenAPI blocks list `https://api.kie.ai` as the server. The house script already uses `kieai.redpandaai.co` and it works.) Same Bearer key.
- Uploads are free.
- Retention: banners say files are "automatically deleted after 24h". Feature lists on the same pages say "after 3 days". The quickstart also says "File URLs remain valid for 24 hours". Plan on 24 hours.
- Same `uploadPath` + `fileName` overwrites the old file, "changes may not take effect immediately due to caching". Use unique file names per run.

| Method | Endpoint | Body | Limits |
|---|---|---|---|
| Stream (best for mp3, wav, mp4, big png) | `POST /api/file-stream-upload` | `multipart/form-data`: `file` (binary, required), `uploadPath` (required, no leading or trailing slash), `fileName` (optional) | "Recommended for large files (>10MB)". Hard max not documented. |
| Base64 | `POST /api/file-base64-upload` | JSON: `base64Data` (required, raw base64 or a `data:<mime>;base64,...` URL), `uploadPath` (required), `fileName` (optional) | "Recommended ≤10MB". Payload grows 33%. |
| From URL | `POST /api/file-url-upload` | JSON: `fileUrl` (required, http or https), `uploadPath` (required), `fileName` (optional) | 30 second download timeout, "Recommended maximum file size is 100MB". |

Stream upload example from the doc:

```bash
curl -X POST https://kieai.redpandaai.co/api/file-stream-upload \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@/path/to/your-file.jpg" \
  -F "uploadPath=images/user-uploads" \
  -F "fileName=custom-name.jpg"
```

Response (endpoint pages):

```json
{"success":true,"code":200,"msg":"File uploaded successfully","data":{"fileName":"uploaded-image.png","filePath":"images/user-uploads/uploaded-image.png","downloadUrl":"https://tempfile.redpandaai.co/xxx/images/user-uploads/uploaded-image.png","fileSize":154832,"mimeType":"image/png","uploadedAt":"2025-01-01T12:00:00.000Z"}}
```

Pass `data.downloadUrl` to models. The quickstart shows a different response shape (`fileId`, `fileUrl`, `downloadUrl`, `expiresAt`). The house script reads `data.downloadUrl`, which exists in both. Upload status codes: 200, 400, 401, 405, 500.

Each model has its own input size cap (for example 10MB for most audio inputs). That cap is the real limit, not the upload API.

---

## 3. Audio-driven talking and lip-sync models (most important)

The live list tags exactly four models as "Lip Sync" (`kling/ai-avatar-standard`, `kling/ai-avatar-pro`, `infinitalk/from-audio`, `volcengine/video-to-video-lip-sync`) plus `wan/2-2-a14b-speech-to-video-turbo` as "Speech to Video". OmniHuman 1.5 is tagged "Image to Video" but is the same kind of model.

### 3.1 Ranked options (my read of the docs, nothing was rendered)

| Rank | Model id | Input | Max audio per task | Output | Credits per second | $ per second | $ for 30 s of speech |
|---|---|---|---|---|---|---|---|
| 1 | `kling/ai-avatar-pro` | 1 image + audio + prompt | 5 minutes [doc] | 1080p, 48 fps [site] | 16 | 0.08 | 2.40 |
| 1b | `kling/ai-avatar-standard` | same | 5 minutes [doc] | 720p [site] | 8 | 0.04 | 1.20 |
| 2 | `omnihuman-1-5` | 1 image + audio, optional mask and prompt | under 60 s, "recommended 15 seconds or less" [doc] | 1080p or 720p | 27 | 0.135 | 4.05 (one task is allowed, two 15 s tasks follow the doc's advice) |
| 3 | `infinitalk/from-audio` | 1 image + audio + prompt | 15 s on Kie [site] | 480p or 720p | 3 (480p), 12 (720p) | 0.015, 0.06 | 0.45 or 1.80 (2 tasks) |
| 4 | `wan/2-7-image-to-video` with `driving_audio_url` | first frame + audio + prompt | clip length 2 to 15 s [doc] | 720p or 1080p | 16 (720p), 24 (1080p) | 0.08, 0.12 | 2.40 or 3.60 (2 tasks) |
| 5 | `volcengine/video-to-video-lip-sync` | existing video + audio | not documented | mp4, 25 fps, source resolution up to 1080p | 8 | 0.04 | 1.20 |
| 6 | `wan/2-2-a14b-speech-to-video-turbo` | 1 image + audio + prompt | 40 to 120 frames, about 2.5 to 7.5 s at the default 16 fps [inferred] | 480p, 580p, 720p | 12, 18, 24 | 0.06, 0.09, 0.12 | 1.80 to 3.60 (4 or more tasks) |

Why this order:

- **Kling AI Avatar** is the only one documented for long audio (5 minutes), so a 30 to 60 s ad read can be one task with no stitching, and Pro is the only 1080p option that is cheap per second. The site calls the current model "Kling AI Avatar 2.0" and says it handles speech and singing, non-photoreal characters, and improved hand motion.
- **OmniHuman 1.5** has the most control (mask to pick which subject speaks, people, pets, and anime are named in the doc, a prompt for behavior, fast mode, seed) and outputs 1080p, but the doc warns of quality loss past 15 s and it costs the most.
- **InfiniteTalk** is the budget pick at 480p. The 15 s cap means a chunk-and-stitch loop.
- **Wan 2.7 I2V with driving audio** gives prompt-directed motion, camera, and 1080p, but the audio field is documented with one line ("Driving audio URL."), so lip-sync quality and audio-length handling are unknowns to test.
- **Volcengine lip sync** is a re-dub tool: generate any talking clip (for example Veo or Kling with native audio), then force its mouth to your ElevenLabs track. Lite mode is for a single frontal speaker.
- **Wan 2.2 S2V** is short, low-res, and pricey per second.

### 3.2 Per-model facts (full params and request JSON in Appendix A.3)

**`kling/ai-avatar-standard`, `kling/ai-avatar-pro`** (https://docs.kie.ai/market/kling/ai-avatar-pro)
- `image_url` (required): jpeg or png, max 10MB.
- `audio_url` (required): mpeg, wav, x-wav, aac, mp4, ogg. "audio size is limited to 100M, and the duration cannot exceed 5 minutes".
- `prompt` (required, max 5000 chars). The doc example sends `""`.
- No resolution, aspect ratio, duration, or seed parameter. Resolution comes from the model tier. Aspect ratio behavior is not documented (most likely follows the input image [inferred]). Output length is not documented (most likely follows the audio [inferred]).
- Quirk: price rows and site pricing text say "up to 15 seconds per generation" while the doc and the site FAQ say 5 minutes. Test one 30 s clip before trusting the long path.

```json
{
  "model": "kling/ai-avatar-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "image_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/175792685809077e8h8k3.png",
    "audio_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1757925802302srqfkcqh.mp3",
    "prompt": ""
  }
}
```

**`omnihuman-1-5`** (https://docs.kie.ai/market/omnihuman-1-5)
- `image_url` (required): jpeg, png, webp, max 10MB. "Supports any aspect ratio with subjects including people, pets, anime".
- `audio_url` (required): "Duration must be less than 60 seconds (recommended 15 seconds or less; exceeding this will cause quality degradation)". Max 10MB.
- `mask_url` (array, up to 5): from `omnihuman-1-5/subject-detection`, picks which subject speaks.
- `prompt` (optional): Chinese, English, Japanese, Korean, Spanish, Indonesian. Schema `maxLength` is 300, the text says "Recommended 300 characters or less. Maximum length: 1000".
- `output_resolution`: `"720"` or `"1080"` (default `"1080"`). `pe_fast_mode` (boolean, default false). `seed` (default -1).
- Helpers: `omnihuman-1-5/subject-detection` (image up to 5MB, returns `mask_urls`, valid 1 hour) and `omnihuman-1-5/human-identification` (returns `subject_status` 0 or 1). Their price is not listed.

```json
{
  "model": "omnihuman-1-5",
  "input": {
    "image_url": "https://your-domain.com/image/portrait.png",
    "mask_url": ["https://your-domain.com/image/mask.png"],
    "audio_url": "https://your-domain.com/audio/speech.mp3",
    "prompt": "A person speaking naturally with gentle expressions.",
    "output_resolution": "1080",
    "pe_fast_mode": false,
    "seed": -1
  },
  "callBackUrl": "https://your-domain.com/api/callback"
}
```

**`infinitalk/from-audio`** (https://docs.kie.ai/market/infinitalk/from-audio)
- `image_url` (required): jpeg, png, webp, max 10MB. "If the input image does not match the chosen aspect ratio, it is resized and center cropped." There is no aspect ratio parameter, so the crop rule is unclear. Feed an image already at the target ratio.
- `audio_url` (required): max 10MB. The playground form adds "Audio duration must not exceed 15 seconds." and the site FAQ says "InfiniteTalk on kie.ai supports video generation up to 15 seconds per task."
- `prompt` (required, max 5000). `resolution`: `480p` (default) or `720p`. `seed`: 10000 to 1000000.
- `infinitalk/from-text` shows in the playground id list only. It is not in the docs or the live list.

**`wan/2-7-image-to-video`** (https://docs.kie.ai/market/wan/2-7-image-to-video)
- Modes: first frame (`first_frame_url`), first and last frame (`last_frame_url`), continuation (`first_clip_url`).
- `driving_audio_url`: "Driving audio URL." Playground form accepts mpeg, wav, aac, mp4, ogg up to 50MB. Nothing else is stated.
- `prompt` (required, max 5000), `negative_prompt` (max 500), `resolution` `720p` or `1080p` (default `1080p`), `duration` 2 to 15 (default 5), `prompt_extend` (default true), `watermark` (default false), `seed`.
- `wan/2-7-text-to-video` has `audio_url` ("Optional custom audio URL") plus `ratio` (`16:9`, `9:16`, `1:1`, `4:3`, `3:4`).

**`volcengine/video-to-video-lip-sync`** (https://docs.kie.ai/market/volcengine/video-to-video-lip-sync)
- `mode` (required): `lite` ("single-person frontal videos. Faster processing") or `basic` ("single-person complex scenes. Supports scene segmentation and speaker identification").
- `video_url` (required): 360p to 1080p (above is compressed to 1080p, below 360p is rejected), MOV, MP4, HDR, H.264 recommended, max 500MB, 1 to 30 Mbps, 24 to 60 fps.
- `audio_url` (required): "Target pure vocal audio", max 10MB.
- `separate_vocal` (default false), `open_scenedet` (basic only, default false), `align_audio` (lite, default true: loop the video when audio is longer), `align_audio_reverse` (lite, default false: loop in reverse), `templ_start_seconds` (lite, default 0).
- Output: "MP4 format at 25 fps. The final output duration follows the audio duration: if the source video is longer than the audio, it will be trimmed; if the source video is shorter than the audio, it will be looped."

**`wan/2-2-a14b-speech-to-video-turbo`** (https://docs.kie.ai/market/wan/2-2-a14b-speech-to-video-turbo)
- `prompt`, `image_url` (max 10MB), `audio_url` (mp3, wav, ogg, m4a, flac, aac, wma, max 10MB) required.
- `num_frames` 40 to 120 step 4 (default 80), `frames_per_second` 4 to 60 (default 16), `resolution` `480p` (default), `580p`, `720p`, `negative_prompt`, `seed`, `num_inference_steps` 2 to 40 (default 27), `guidance_scale` 1 to 10 (default 3.5), `shift` 1 to 10 (default 5).
- Clip length is frames divided by fps. Max audio duration is not documented.

### 3.3 Models that take audio as a reference (not a strict lip-sync driver)

These generate their own video and use your audio as voice or timing guidance. The docs do not promise frame-accurate sync to the file.

| Model id | Audio field | Audio limits [doc] | Notes |
|---|---|---|---|
| `bytedance/seedance-2-5` | `reference_audio_urls` (up to 10) | wav or mp3, each 2 to 30 s, 15MB each, total 30 s | Cannot be combined with `first_frame_url` / `last_frame_url`. Use `reference_image_urls` for the character instead. Output 4 to 30 s. |
| `bytedance/seedance-2`, `-2-fast`, `-2-mini` | `reference_audio_urls` (up to 3) | wav or mp3, each 2 to 15 s, total 15 s, 15MB each | Same exclusivity rule. Output 4 to 15 s. |
| `wan/3-0-video`, `wan/3-0-video-prime` | `reference_audio_urls` (up to 5) | wav or mp3, each 1 to 15 s, total 15 s, 15MB | Refer to it in the prompt as `Audio1`. Cannot be combined with first or last frame. |
| `minimax-h3/reference-to-video` | `reference_audio_urls` (up to 3) | wav or mp3, each 2 to 15 s, total 15 s, 15MB | "Input audio: Free." |
| `wan/2-7-r2v` | `reference_voice` | wav or mp3, 1 to 10 s, 15MB | Voice timbre only. |
| `kling-3.0/video`, `kling-3.0-omni/*` | `kling_elements[].element_input_audio_urls` / `elements[].element_input_audio_urls` | 5 to 30 s | Voice for a named character element. |
| `gemini-omni-video`, `google/gemini-omni-flash-1-1` | `audio_ids` (up to 3) | ids from `POST /api/v1/omni/audio/create` | That endpoint builds a voice from a preset voice id plus a text description. It does not accept an audio file. |

### 3.4 Asked about but not on Kie

Hedra, Sync (lipsync), VEED Fabric, a Kling video lip-sync model, Wan 2.5 or 2.6 audio-file input (the current Wan 2.5 and 2.6 docs have no audio parameter), `bytedance/omni-human` (old id), `kling/v1-avatar-standard`, `kling/ai-avatar-v1-pro`, `kling/v1-tts`. Topaz on Kie is upscaling only. Details in Appendix C.

---

## 4. Native-audio video models (video and speech generated together)

"Speech from prompt" below is [site] marketing unless marked [doc]. The docs mostly expose a single audio on/off switch and do not describe dialogue syntax. Kling 2.6 is the exception: its doc examples show the dialogue prompt format (`[Character, tone] says: "line"`).

| Family | Model ids | Modes | Duration | Resolution | Aspect | Audio switch | Speech from prompt | Audio file input | Multi-shot | Reference images | Price |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Veo 3.1 | `veo-3-1` (+ `veo/extend`, `veo/get-1080p-video`, `veo/get-4k-video`); legacy `veo3`, `veo3_fast`, `veo3_lite` | t2v, i2v (1 image, or first + last), reference-to-video (1 to 3 images, Fast and Lite only, 8 s only) | 4, 6, 8 s | 720p, 1080p, 4k | 16:9, 9:16, Auto | none, always on ("All videos ship with background audio by default") | yes [site] | no | no | 1 to 3 in `REFERENCE_2_VIDEO` | per video: Lite 30 / 35 / 150, Fast 60 / 65 / 180, Quality 250 / 255 / 370 credits (720p / 1080p / 4K). Extend 30 / 60 / 250. 1080p fetch 5. 4K fetch 120. |
| Kling 3.0 | `kling-3.0/video` | t2v, i2v, first + last frame | 3 to 15 s | `std` 720p, `pro` 1080p, `4K` | 16:9, 9:16, 1:1 (auto from image) | `sound` | yes, multi-character dialogue [site] | voice clip per element (5 to 30 s) | yes, `multi_shots` + `multi_prompt`, up to 5 shots, 1 to 12 s each, 500 chars each | `kling_elements`: up to 3 elements, 2 to 4 images each, or 1 video of 3 to 8 s | per second: std 14 (no audio) / 20 (audio), pro 18 / 27, 4K 67 |
| Kling 3.0 Turbo | `kling/v3-turbo-text-to-video`, `kling/v3-turbo-image-to-video` | t2v, i2v | 3 to 15 s | 720p, 1080p | t2v: 1:1, 9:16, 16:9 | none documented | doc example prompt contains spoken lines, site says dialogue | no | prompt-driven [site] | 1 start image | per second: 18 (720p), 22.5 (1080p) |
| Kling 3.0 Omni | `kling-3.0-omni/text-to-video`, `/image-to-video`, `/reference-to-video`, `/transformation` | t2v, i2v, first + last, reference, video transform | 3 to 15 s | 720p, 1080p, 4k | 16:9, 9:16, 1:1, auto | `audio` (must be false when a reference video is supplied) | not stated | voice clip per element | yes, `customize_multi_shots` + `multi_prompt` up to 6 shots, or `prefer_multi_shots` | up to 7 images, elements with 2 to 4 images each | per second: 720p 14 / 18 with audio, 1080p 18 / 23, 4K 67. With video input 20 / 27 / 67. [live] |
| Kling 2.6 | `kling-2.6/text-to-video`, `kling-2.6/image-to-video` | t2v, i2v (1 image) | 5 or 10 s | not selectable ("HD" [site]) | t2v: 1:1, 16:9, 9:16 | `sound` (required) | yes, doc example shows dialogue lines | no | no | 1 | per video: 55 (5 s) / 110 (10 s) silent, 110 / 220 with audio |
| Seedance 2.5 | `bytedance/seedance-2-5` | t2v, first frame, first + last, multimodal reference | 4 to 30 s, or -1 auto | 480p, 720p, 1080p | 1:1, 4:3, 3:4, 16:9, 9:16, 21:9, adaptive | `generate_audio` (default true) | yes [site, for Seedance 2.0] | `reference_audio_urls` | prompt-driven | up to 30 images, 10 videos, 10 audio clips | per second: 480p 28, 720p 63, 1080p 158 (with video input 17 / 38 / 95, billed on input + output seconds) |
| Seedance 2.0 | `bytedance/seedance-2`, `bytedance/seedance-2-fast`, `bytedance/seedance-2-mini` | same | 4 to 15 s, or -1 | 2: 480p to 4k. Fast and Mini: 480p, 720p | same | `generate_audio` (default true) | yes, "lip-sync" [site] | `reference_audio_urls` | prompt-driven | up to 9 images, 3 videos, 3 audio clips | per second, no video input: 2: 19 / 41 / 102 / 208 (480p / 720p / 1080p / 4K). Fast: 11.7 / 24.8. Mini: 3.8 / 8.2 |
| Seedance 1.5 Pro | `bytedance/seedance-1.5-pro` | t2v, i2v with 0 to 2 images | 4 to 12 s | 480p, 720p, 1080p | 1:1, 4:3, 3:4, 16:9, 9:16, 21:9 | `generate_audio` (default false) | yes [site] | no | no | 0 to 2 (`input_urls`) | per second: 480p 1.75 / 3.5 with audio, 720p 3.5 / 7, 1080p 7.5 / 15 |
| Wan 3.0 | `wan/3-0-video`, `wan/3-0-video-prime` | t2v, first frame, first + last, all-purpose reference, file-to-video, link-to-video | 2 to 30 s, or -1 | 480P, 720P, 1080P (uppercase) | adaptive, 16:9, 4:3, 1:1, 3:4, 9:16 | `audio` (default true) | yes [site] | `reference_audio_urls` | prompt-driven | up to 10 images, 5 videos, 5 audio clips | per second: standard 8 / 16 / 32, Prime 12.2 / 25.2 / 50.4. Billed on input video + output seconds. |
| Wan 2.7 | `wan/2-7-text-to-video`, `wan/2-7-image-to-video`, `wan/2-7-r2v`, `wan/2-7-videoedit` | t2v, i2v, first + last, continuation, reference, edit | 2 to 15 s (r2v and edit 2 to 10) | 720p, 1080p | 16:9, 9:16, 1:1, 4:3, 3:4 | none (videoedit has `audio_setting`) | not stated in the doc | `audio_url` (t2v), `driving_audio_url` (i2v), `reference_voice` (r2v) | no | r2v: up to 5 images + videos | per second: 16 (720p), 24 (1080p) |
| Wan 2.6 | `wan/2-6-text-to-video`, `wan/2-6-image-to-video`, `wan/2-6-video-to-video` | t2v, i2v, v2v | 5, 10, 15 s (v2v 5, 10) | 720p, 1080p | not a parameter | none | "native audio, and accurate lip sync" [site] | no | `multi_shots` (boolean) | 1 image, or up to 3 videos | per video 720p: 70 / 140 / 210. 1080p: 104.5 / 209.5 / 315 |
| Wan 2.5 | `wan/2-5-text-to-video`, `wan/2-5-image-to-video` | t2v, i2v | 5 or 10 s | 720p, 1080p | t2v: 16:9, 9:16, 1:1 | none | "dialogue, ambient sound, and background music" [site] | no | no | 1 | 720p 60 / 120, 1080p 100 / 200 per video |
| Grok Imagine | `grok-imagine/text-to-video`, `grok-imagine/image-to-video`, `grok-imagine/extend`, `grok-imagine/upscale`, `grok-imagine-video-1-5-preview` | t2v, i2v, extend, upscale | 6 to 30 s (1.5 preview: 1 to 15 s) | 480p, 720p, 1080p | 2:3, 3:2, 1:1, 16:9, 9:16 | none | yes for 1.5 [site] | no | no | up to 7 images | per second: 2.4 / 4.5 / 8 |
| Gemini Omni | `google/gemini-omni-flash-1-1`, `gemini-omni-video` | t2v, reference images, video clips, first + last frame (Flash 1.1) | 4, 6, 8, 10 s | 720p, 1080p, 4k (Flash adds 360p) | 16:9, 9:16 | none | not stated | `audio_ids` (preset voices), `character_ids` | no | 7-unit quota: image 1 unit, video 2 units | per video 720p / 1080p: 63 / 84 / 105 / 126 for 4 / 6 / 8 / 10 s. 4K: 147 / 168 / 189 / 210 |
| MiniMax H3 (Hailuo 03) | `minimax-h3/text-to-video`, `/image-to-video`, `/reference-to-video` | t2v, first or last frame, reference | 4 to 15 s | 768P, 2K | 21:9, 16:9, 4:3, 1:1, 3:4, 9:16, adaptive | none | "native stereo audio ... dialogue" [site] | `reference_audio_urls` | prompt-driven [site] | up to 9 images, 3 videos, 3 audio clips | per second: 8 (768P), 13 (2K) |
| PixVerse V6 | `pixverse-v6/text-to-video`, `/image-to-video`, `/transition`, `/extend`, `/reference-to-video` | t2v, i2v, first + last, extend, fusion | 1 to 15 s | 360p, 540p, 720p, 1080p | 8 ratios | `generate_audio_switch` | example prompt has dialogue [site] | no | `generate_multi_clip_switch` | up to 7 named references | per second 720p: 7.2 / 9.6 with audio. 1080p: 14.4 / 18.4 |
| HappyHorse 1.1 | `happyhorse-1-1/text-to-video`, `/image-to-video`, `/reference-to-video` | t2v, i2v, reference | 3 to 15 s | 720p, 1080p | 9 ratios | none | not stated | no | no | up to 9 | per second: 22.5 / 29 |
| Hailuo 2.3 | `hailuo/2-3-image-to-video-pro`, `-standard` | i2v | 6 or 10 s (no 10 s at 1080P) | 768P, 1080P | from image | none | no audio stated | no | no | 1 | per video 30 to 90 |
| Runway | `runway`, `runway/extend-ai-video` | t2v, i2v, extend | 5 or 10 s | 720p, 1080p (5 s only) | 5 ratios | none | no | no | no | 1 | 12 or 30 per video |
| Sora 2 | removed | | | | | | | | | | |

Notes:

- Veo 3.1 extend: "Can only extend videos generated through the Veo3.1 API" and "Videos generated in 1080P cannot be extended." 1080p fetch takes about 1 to 3 minutes, 4K about 5 to 10 minutes and returns 422 while processing.
- Veo reference-to-video is Fast and Lite only, 8 s only.
- Seedance "with video input" prices look lower but are billed on input + output seconds.
- Seedance 2.x takes `asset://{assetId}` values as well as URLs. The asset create and query doc pages return 404, so that flow is not documented.
- The Seedance 2.0 Fast and Mini pricing text says a limited-time discount ends 2026-10-07 06:00 UTC. Recheck prices after that date.
- For the one-character talking ad, the native-audio route means the model invents the voice. A consistent brand voice needs either the section 3 route (ElevenLabs audio, then lip-sync) or a model with a voice reference input (section 3.3).

---

## 5. Text to speech, audio, and music

### 5.1 ElevenLabs on Kie

| Model id | What | Price | Text limit |
|---|---|---|---|
| `elevenlabs/text-to-speech-turbo-2-5` | Single-voice TTS | 6 credits per 1,000 characters ($0.03) | 5000 chars |
| `elevenlabs/text-to-speech-multilingual-v2` | Single-voice TTS | 12 credits per 1,000 characters ($0.06) | 5000 chars |
| `elevenlabs/text-to-dialogue-v3` | Eleven v3, multi-speaker dialogue | 14 credits per 1,000 characters ($0.07) | 5000 chars across all lines |
| `elevenlabs/audio-isolation` | Voice isolation | no price row | NOT in the live model list |

TTS parameters (both TTS models, [doc]):

- `text` (required, max 5000).
- `voice`: one of the 67 preset voice ids in 5.2. Default `EkK5I93UQWFDigLMpZcX` (James). Optional on Turbo 2.5, marked required on Multilingual v2. The doc text says "Can be a preset voice name (e.g. Rachel, Adam) or a voice ID" and its request example sends `"voice": "Rachel"`, but the schema enum lists ids only and neither Rachel nor Adam is in it. Send ids.
- `stability` 0 to 1 (default 0.5), `similarity_boost` 0 to 1 (default 0.75), `style` 0 to 1 (default 0), `speed` 0.7 to 1.2 (default 1).
- `timestamps` (boolean): "Whether to return timestamps for each word in the generated speech". Return shape not documented.
- `previous_text`, `next_text` (max 5000 each): continuity across chunks. Use these when a script is split into several TTS calls.
- `language_code` (ISO 639-1): "Currently only Turbo v2.5 and Flash v2.5 support language enforcement. For other models, an error will be returned if language code is provided." So leave it out on Multilingual v2.
- Output: audio URL(s) in `resultUrls` (mp3 in the site sample). Output format and sample rate options are not documented.

```json
{
  "model": "elevenlabs/text-to-speech-turbo-2-5",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "text": "Unlock powerful API with Kie.ai! Affordable, scalable APl integration, free trial playground, and secure, reliable performance.",
    "voice": "Rachel",
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0,
    "speed": 1,
    "timestamps": false,
    "previous_text": "",
    "next_text": "",
    "language_code": ""
  }
}
```

(That is the doc's example verbatim. Replace `"Rachel"` with an id from 5.2.)

Dialogue v3 parameters: `dialogue` (required array of `{text, voice}`, same 67 voice ids, all `text` combined max 5000 chars), `stability` (only `0`, `0.5`, or `1`, default 0.5), `language_code` (enum of 74 codes, omit for auto detect). The playground default text uses v3 audio tags such as `[excitedly]`. No `timestamps`, `speed`, `style`, or `similarity_boost` on v3.

```json
{
  "model": "elevenlabs/text-to-dialogue-v3",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "dialogue": [
      {"text": "I have a pen, I have an apple, ah, Apple pen~", "voice": "EkK5I93UQWFDigLMpZcX"},
      {"text": "a happy dog", "voice": "Z3R5wn05IrDiVCyEkUrK"},
      {"text": "a happy cat", "voice": "NNl6r8mD7vthiJatiJt1"}
    ],
    "stability": 0.5
  }
}
```

Custom or cloned voices: not possible through the documented API. The voice field is a closed list of 67 ids. No voice-clone, voice-design, or voice-changer model exists in the docs or the live list. (A line of site marketing copy mentions cloning "via ElevenLabs API key", which is not a Kie API feature.) Whether an arbitrary ElevenLabs voice id outside the list is accepted is not documented.

Not available on Kie today: ElevenLabs speech-to-text (Scribe), sound effects, voice changer. `openai/whisper-speech-to-text` appears only in the stale playground list.

### 5.2 ElevenLabs voice ids (all 67, identical for the three models)

Preview any voice at `https://static.aiquickdraw.com/elevenlabs/voice/<voice_id>.mp3`.

| voice id | name and description (verbatim from docs) |
|---|---|
| `EkK5I93UQWFDigLMpZcX` | James - Husky, Engaging and Bold |
| `Z3R5wn05IrDiVCyEkUrK` | Arabella - Mysterious and Emotive |
| `NNl6r8mD7vthiJatiJt1` | Bradford - Expressive and Articulate |
| `YOq2y2Up4RgXP2HyXjE5` | Xavier - Dominating, Metallic Announcer |
| `B8gJV1IhpuegLxdpXFOE` | Kuon - Cheerful, Clear and Steady |
| `2zRM7PkgwBPiau2jvVXc` | Monika Sogam - Deep and Natural |
| `1SM7GgM6IMuvQlz2BwM3` | Mark - Casual, Relaxed and Light |
| `5l5f8iK3YPeGga21rQIX` | Adeline - Feminine and Conversational |
| `scOwDtmlUjD3prqpp97I` | Sam - Support Agent |
| `NOpBlnGInO9m6vDvFkFC` | Spuds Oxley - Wise and Approachable |
| `BZgkqPqms7Kj9ulSkVzn` | Eve - Authentic, Energetic and Happy |
| `wo6udizrrtpIxWGp2qJk` | Northern Terry |
| `gU0LNdkMOQCOrPrwtbee` | British Football Announcer |
| `DGzg6RaUqxGRTHSBjfgF` | Brock - Commanding and Loud Sergeant |
| `x70vRnQBMBu4FAYhjJbO` | Nathan - Virtual Radio Host |
| `Sm1seazb4gs7RSlUVw7c` | Anika - Animated, Friendly and Engaging |
| `P1bg08DkjqiVEzOn76yG` | Viraj - Rich and Soft |
| `qDuRKMlYmrm8trt5QyBn` | Taksh - Calm, Serious and Smooth |
| `qXpMhyvQqiRxWQs4qSSB` | Horatius - Energetic Character Voice |
| `TX3LPaxmHKxFdv7VOQHJ` | Liam - Energetic, Social Media Creator |
| `N2lVS1w4EtoT3dr4eOWO` | Callum - Husky Trickster |
| `FGY2WhTYpPnrIDTdsKH5` | Laura - Enthusiast, Quirky Attitude |
| `kPzsL2i3teMYv0FxEYQ6` | Brittney - Social Media Voice - Fun, Youthful & Informative |
| `UgBBYS2sOqTuMpoF3BR0` | Mark - Natural Conversations |
| `hpp4J3VqNfWAUOO0d1Us` | Bella - Professional, Bright, Warm |
| `nPczCjzI2devNBz1zQrb` | Brian - Deep, Resonant and Comforting |
| `uYXf8XasLslADfZ2MB4u` | Hope - Bubbly, Gossipy and Girly |
| `gs0tAILXbY5DNrJrsM6F` | Jeff - Classy, Resonating and Strong |
| `DTKMou8ccj1ZaWGBiotd` | Jamahal - Young, Vibrant, and Natural |
| `vBKc2FfBKJfcZNyEt1n6` | Finn - Youthful, Eager and Energetic |
| `DYkrAHD8iwork3YSUBbs` | Tom - Conversations & Books |
| `56AoDkrOh6qfVPDXZ7Pt` | Cassidy - Crisp, Direct and Clear |
| `eR40ATw9ArzDf9h3v7t7` | Addison 2.0 - Australian Audiobook & Podcast |
| `g6xIsTj2HwM6VR4iXFCw` | Jessica Anne Bogart - Chatty and Friendly |
| `lcMyyd2HUfFzxdCaC4Ta` | Lucy - Fresh & Casual |
| `6aDn1KB0hjpdcocrUkmq` | Tiffany - Natural and Welcoming |
| `Sq93GQT4X1lKDXsQcixO` | Felix - Warm, Positive & Contemporary RP |
| `flHkNRp1BlvT73UL6gyz` | Jessica Anne Bogart - Eloquent Villain |
| `9yzdeviXkFddZ4Oz8Mok` | Lutz - Chuckling, Giggly and Cheerful |
| `pPdl9cQBQq4p6mRkZy2Z` | Emma - Adorable and Upbeat |
| `zYcjlYFOd3taleS0gkk3` | Edward - Loud, Confident and Cocky |
| `nzeAacJi50IvxcyDnMXa` | Marshal - Friendly, Funny Professor |
| `ruirxsoakN0GWmGNIo04` | John Morgan - Gritty, Rugged Cowboy |
| `TC0Zp7WVFzhA8zpTlRqV` | Aria - Sultry Villain |
| `ljo9gAlSqKOvF6D8sOsX` | Viking Bjorn - Epic Medieval Raider |
| `PPzYpIqttlTYA83688JI` | Pirate Marshal |
| `8JVbfL6oEdmuxKn5DK2C` | Johnny Kid - Serious and Calm Narrator |
| `iCrDUkL56s3C8sCRl7wb` | Hope - Poetic, Romantic and Captivating |
| `wJqPPQ618aTW29mptyoc` | Ana Rita - Smooth, Expressive and Bright |
| `EiNlNiXeDU1pqqOPrYMO` | John Doe - Deep |
| `4YYIPFl9wE5c4L2eu2Gb` | Burt Reynolds™ - Deep, Smooth and Clear |
| `6F5Zhi321D3Oq7v1oNT4` | Hank - Deep and Engaging Narrator |
| `YXpFCvM1S3JbWEJhoskW` | Wyatt - Wise Rustic Cowboy |
| `LG95yZDEHg6fCZdQjLqj` | Phil - Explosive, Passionate Announcer |
| `CeNX9CMwmxDxUF5Q2Inm` | Johnny Dynamite - Vintage Radio DJ |
| `aD6riP1btT197c6dACmy` | Rachel M - Pro British Radio Presenter |
| `mtrellq69YZsNwzUSyXh` | Rex Thunder - Deep N Tough |
| `dHd5gvgSOzSfduK4CvEg` | Ed - Late Night Announcer |
| `eVItLK1UvXctxuaRV2Oq` | Jean - Alluring and Playful Femme Fatale |
| `esy0r39YPLQjOczyOib8` | Britney - Calm and Calculative Villain |
| `Tsns2HvNFKfGiNjllgqo` | Sven - Emotional and Nice |
| `1U02n4nD6AdIZ9CjF053` | Viraj - Smooth and Gentle |
| `AeRdCCKzvd23BpJoofzx` | Nathaniel - Engaging, British and Calm |
| `LruHrtVF6PSyGItzMNHS` | Benjamin - Deep, Warm, Calming |
| `1wGbFxmAM3Fgw63G1zZJ` | Allison - Calm, Soothing and Meditative |
| `hqfrgApggtO1785R4Fsn` | Theodore HQ - Serene and Grounded |
| `MJ0RnG71ty4LH3dvNfSd` | Leon - Soothing and Grounded |

### 5.3 Gemini TTS on Kie (alternative voices, style direction in plain words)

| Model id | Price (credits per 1M tokens) | Notes |
|---|---|---|
| `google/gemini-3-8-flash-tts` | input 70, audio output 1,260 (limited-time price until 2026-12-31) | 70 voices, per-line `style` text, inline tags like `<laugh>` |
| `google/gemini-3-8-flash-lite-tts` | input 70, audio output 840 (same limited-time note) | same schema; the doc's request example omits `voice_name` |
| `google/gemini-3-1-flash-tts` | input 140, audio output 2,800 | required `voice_name` (30 voices), `scene`, `sample_context`, per-speaker `audio_profile`, `accent` (required), `style`, `pace`; bracket tags like `[whispers]`. The doc's request example omits `voice_name` even though the schema marks it required. |
| `google/gemini-2-5-pro-tts` | input 140, audio output 2,800 | same schema as 3.1 Flash TTS |

Shape: `input.speakers[]` (`speaker_id` must be `"Speaker N"`), `input.dialogue_turns[]` (`speaker_id`, `text` max 10000, and `style` on 3.8), `input.temperature` 0 to 2. Output sample on the site is a wav. No timestamps. Tokens per second of audio is not documented, so cost per minute is unknown until tested. Full voice lists and examples are in Appendix A.5.

### 5.4 Suno (music bed, sound effects)

All Suno functions are `ai-music-api/*` models on createTask in the current docs (legacy `/api/v1/generate` family in the old docs).

| Model id | Use | Price |
|---|---|---|
| `ai-music-api/generate` | Song or instrumental. `input.model` = `V6`, `V6_MINI`, `V6_WILD`. `custom_mode`, `instrumental`, `prompt`, `style`, `title`, `lyrics`, `duration` 10 to 360 s (custom mode), `vocal_gender`, `persona_id`. | 12 credits per request ($0.06) |
| `ai-music-api/sounds` | Sound effect or loop from a prompt (max 500 chars), `sound_loop`, `sound_tempo`, `sound_key` | 2.5 credits ($0.0125) |
| `ai-music-api/timeStamped-lyrics` | Word-level timing for a Suno track (`task_id`, `audio_id`) | 0.5 credits |
| `ai-music-api/separate-vocals` | Stem split | 10 (vocal + instrumental), 20 (named stem), 50 (multi-stem) |
| `ai-music-api/extend`, `upload-and-cover-audio`, `upload-and-extend-audio`, `add-vocals`, `add-instrumental`, `mashup` | Edits | 12 credits each |
| `ai-music-api/convert-to-wav-format` | WAV export | 0.4 credits |
| `ai-music-api/create-voice`, `validation-phrase`, `regenerate-phrase`, `check-voice`, `generate-voice` | Suno custom singing voice flow | free where a price is shown |

`ai-music-api/timeStamped-lyrics` only works on Suno task ids. It is not a general transcription tool. The workspace `song-ads` skill already covers the Suno song-ad prompt side.

---

## 6. Image models for character sheets and start frames

Prices are per output image. Full params in Appendix A.6.

| Model id | Reference images | Aspect ratios | Resolution | Credits ($) | Notes |
|---|---|---|---|---|---|
| `nano-banana-pro` | `image_input`, up to 8 | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, auto | `1K`, `2K`, `4K` | 18 (1K or 2K), 24 (4K) ($0.09, $0.12) | t2i and i2i in one id. Prompt max 10000. |
| `nano-banana-2` | `image_input`, up to 14 | adds 1:4, 4:1, 1:8, 8:1 | `1K`, `2K`, `4K` | 8, 12, 18 ($0.04, $0.06, $0.09) | Prompt max 20000. |
| `nano-banana-2-lite` | `image_urls`, up to 10 | same as Nano Banana 2 | 1K | 4 ($0.02) | |
| `google/nano-banana-edit` | `image_urls`, up to 10 (required) | 11 options incl. auto | not selectable | 4 ($0.02) | Use `aspect_ratio`; `image_size` is the deprecated name. |
| `google/nano-banana` | none (t2i) | same | not selectable | 4 ($0.02) | |
| `gpt-image-2-image-to-image` | `input_urls`, up to 16 | auto plus 15 ratios | `1K`, `2K`, `4K` | 6, 10, 16 ($0.03, $0.05, $0.08) | Already the house default. `background` transparent only at 1K. 1:1 cannot be 4K. |
| `gpt-image-2-text-to-image` | none | same | same | same | |
| `gpt-image-2-5-flare-*`, `gpt-image-2-5-sunburst-*` (`-text-to-image`, `-image-to-image`) | `input_urls`, up to 16 | auto plus 12 ratios | `1K`, `2K`, `4K` | 6, 10, 16 | Two GPT Image 2.5 variants. The docs do not explain the difference. |
| `gpt-image/1.5-image-to-image`, `gpt-image/1.5-text-to-image` | `input_urls`, up to 16 | 1:1, 2:3, 3:2 | by `quality` | medium 4, high 22 | |
| `seedream/4.5-edit` | `image_urls`, up to 14 | 1:1, 4:3, 3:4, 16:9, 9:16, 2:3, 3:2, 21:9 | `quality` basic = 2K, high = 4K | 6.5 ($0.0325) | |
| `seedream/5-pro-image-to-image` | `image_urls`, up to 10 | same 8 | basic = 1K, high = 2K | 7 (1K), 14 (2K), plus 0.5 per input image after the first | Also `seedream/5-pro-layer-decomposition`. |
| `seedream/5-lite-image-to-image` | `image_urls`, up to 14 | same 8 | basic 2K, high 3K, ultra 4K | 5.5 | |
| `seedream/5-flash-image-to-image` | see appendix | | 1K, 1.5K, 2K | 3.24 | |
| `flux-2/pro-image-to-image`, `flux-2/flex-image-to-image` | `input_urls`, 1 to 8 | 7 ratios plus auto | `1K`, `2K` | Pro 5 / 7, Flex 14 / 24 | |
| `ideogram/character` (+ `-edit`, `-remix`) | `reference_image_urls`, 1 image only | `image_size` presets | preset | Turbo 12, Balanced 18, Quality 24 | Purpose-built for character consistency. |
| `qwen2/image-edit` | `image_url`, 1 | 8 ratios | not selectable | 5.6 | Prompt max 800. |
| `qwen3/pro-image-to-image`, `qwen3/image-to-image` | see appendix | | 1K, 2K | Pro 6.4 / 12, standard 4.8, plus 0.5 per input image | |
| `wan/2-7-image-pro`, `wan/2-7-image` | `input_urls`, up to 9 | 8 ratios | `1K`, `2K`, `4K` | Pro 12, standard 4.8 | Sequential mode makes up to 12 related images in one call. |
| `z-image` | none | 1:1, 4:3, 3:4, 16:9, 9:16 | not selectable | 0.8 ($0.004) | Cheapest t2i. Prompt max 1000. |
| `grok-imagine-image-2-0/image-edit`, `/text-to-image` | see appendix | | | 4 | |
| `4o-image-api`, `flux1-kontext` | up to 5 / 1 | 1:1, 3:2, 2:3 / 6 ratios | | 6 / 5 (Pro) or 10 (Max) | Older, now unified ids. |

Field-name trap: the reference-image field is `image_input` (Nano Banana Pro and 2), `image_urls` (Nano Banana Edit and Lite, Seedream), `input_urls` (GPT Image, Flux 2, Wan 2.7 Image), `reference_image_urls` (Ideogram), `image_url` (Qwen 2 edit).

For a character sheet plus matching 9:16 start frames, the documented fits are `nano-banana-pro` or `nano-banana-2` (many references, explicit 9:16, up to 4K) and `gpt-image-2-image-to-image` (16 references). No quality comparison was run.

---

## 7. Utility and finishing

| Model id | Use | Key params | Price |
|---|---|---|---|
| `topaz/video-upscale` | Upscale a finished clip | `video_url` (mp4, mov, mkv; playground cap 50MB), `upscale_factor` `"1"`, `"2"`, `"4"` | 8 credits per second (1x, 2x), 14 per second (4x) |
| `topaz/image-upscale` | Upscale a still | `image_url`, `upscale_factor` | 10 (up to 2K), 20 (4K) |
| `recraft/crisp-upscale` | Cheap image upscale | `image` | 0.5 |
| `recraft/remove-background` | Cut out a character | `image` (png, jpg, webp, max 5MB, max 16MP) | 1 |
| `grok-imagine/upscale` | Upscale a Grok video by task id only | `task_id`, `resolution` | 10 to 30 per upscale |
| `veo/get-1080p-video`, `veo/get-4k-video` | Upgrade a Veo task | task id, `index` | 5, 120 |
| `wan/2-2-animate-move`, `wan/2-2-animate-replace` | Drive a character image with a performance video, or replace the actor in a video | `video_url`, `image_url`, `resolution` 480p / 580p / 720p | 6 / 9.5 / 12.5 per second, up to 30 s per job [site] |
| `kling-3.0/motion-control`, `kling-2.6/motion-control` | Transfer motion from a 3 to 30 s video onto a character image | `input_urls` (1 image), `video_urls` (1 video), `mode`, `character_orientation`, `background_source` (3.0) | 3.0: 20 (720p) / 27 (1080p) per second. 2.6: 11 / 18 |
| `kling-3.0-omni/transformation` | Prompt-edit a 3 to 15.5 s video | `video_urls`, optional `image_urls`, `elements` | 20 / 27 / 67 per second |
| `wan/2-7-videoedit` | Prompt-edit a 2 to 10 s video, keep or regenerate audio (`audio_setting`) | `video_url`, `reference_image` | 16 / 24 per second |
| `happyhorse/video-edit` | Prompt-edit a video | see appendix | 28 / 48 per second on input + output seconds |
| `wan/2-6-video-to-video` | Restyle up to 3 videos | `video_urls` | 70 to 209.5 per video |
| Runway Aleph | Video-to-video edit | legacy `POST /api/v1/aleph/generate` | 110 per video. Unified id `runway/gen4-aleph` is not in the live list. |
| `volcengine/video-to-video-lip-sync` | Re-sync mouth to a new audio track | section 3 | 8 per second |
| `ai-music-api/separate-vocals` | Split voice from music | | 10 to 50 |
| `POST /api/v1/common/download-url` | Direct download link for a Kie file | | free |

Luma Modify and Kling O1 are not available (Appendix C). Captions, cuts, stitching, loudness, and audio muxing stay in ffmpeg.

---

## 8. Open questions to settle with one cheap paid test each

Nothing below could be answered without spending credits. Each is one small task.

1. **TTS timestamps shape.** Run `elevenlabs/text-to-speech-turbo-2-5` on one sentence with `"timestamps": true` and print the raw `resultJson`. Decide captions after seeing it. (About 1 credit.)
2. **Voice names.** Same call with `"voice": "Rachel"` to see whether names outside the 67-id list are accepted.
3. **Kling AI Avatar long audio.** One `kling/ai-avatar-standard` task with a 25 to 30 s mp3 (about 240 credits, $1.20) to confirm the 5 minute doc claim over the "up to 15 seconds" price label, and to see output aspect ratio and fps.
4. **Veo tier on the unified id.** One `veo-3-1` task, then read `creditsConsumed` (30 = Lite, 60 = Fast, 250 = Quality at 720p). Or skip the question and use legacy `/api/v1/veo/generate` with `model: "veo3_fast"`.
5. **Wan 2.7 `driving_audio_url`.** One 5 s 720p task (80 credits) with a speech mp3 to see whether it is true lip-sync and what happens when audio is longer than `duration`.
6. **Upload retention.** Check whether an uploaded file URL still resolves after 24 hours.

---

## Appendix A. Per-model parameter specs (machine-extracted from docs.kie.ai)

How to read: each block is one doc page. Parameter lines are `name` (type, REQUIRED if required, enum, default, limits): description from the doc. The `input.` prefix is dropped, so every parameter goes inside `input` unless the endpoint line is not createTask. `callBackUrl` (optional) is accepted on every createTask model and is omitted from the lists. Blocks titled LEGACY are the old dedicated endpoints: their parameters are top-level JSON fields, not wrapped in `input`. Descriptions longer than the cap end with "[truncated, see doc]". Request examples are the doc's own JSON with long strings shortened (marked with …). "same fields as" entries were produced by diffing the two schemas.

### A.1 Core and utility endpoints

#### Get Task Details
- Doc: https://docs.kie.ai/market/common/get-task-detail
- Endpoint: `GET https://api.kie.ai/api/v1/jobs/recordInfo`
- Doc prose:

  > Query the status and results of any task created in the Market models. This is a unified query interface that works with all models under the Market category.
  > 
  > ### Supported Models
  > This endpoint works with all Market models including:
  > - **Seedream**: seedream, seedream-v4-text-to-image, etc.
  > - **Grok Imagine**: text-to-image, image-to-video, text-to-video, upscale
  > - **Kling**: text-to-video, image-to-video models
  > - **ElevenLabs**: Audio processing models
  > - **Claude**: Language models
  > - **And any future models added to the Market**
  > 
  > ### Task States
  > - **waiting**: Task is queued and waiting to be processed
  > - **queuing**: Task is in the processing queue
  > - **generating**: Task is currently being processed
  > - **success**: Task completed successfully
  > - **fail**: Task failed
  > 
  > ### Best Practices
  > - **Use callbacks for production**: Include `callBackUrl` when creating tasks to avoid polling
  > - **Implement exponential backoff**: Start with 2-3 second intervals, increase gradually
  > - **Handle timeouts**: Stop polling after 10-15 minutes
  > - **Download results immediately**: Generated content URLs typically expire after 24 hours

- Query params:
  - query `taskId` req=true type=string enum=null default=null ex=["task_12345678"] :: The unique task identifier returned when you created the task.
- 200 response example: `{"code":505,"msg":"success","data":{"taskId":"task_12345678","model":"grok-imagine/text-to-image","state":"success","param":"{\"model\":\"grok-imagine/text-to-image\",\"callBackUrl\":\"https://your-domain.com/api/callback\",\"input\":{\"prompt\":\"Cinematic portrait...\",\"aspect_ratio\":\"3:2\"}}","resultJson":"{\"resultUrls\":[\"https://example.com/generated-content.jpg\"]}","failCode":"","failMsg":"","costTime":15`

#### Get Remaining Credits
- Doc: https://docs.kie.ai/common-api/get-account-credits
- Endpoint: `GET https://api.kie.ai/api/v1/chat/credit`
- Doc prose:

  > :::tip[]
  >   Get the current credit balance available in your account.
  > :::
  > 
  > ### Usage Guide
  > 
  > * Use this interface to check your current credit balance
  > * Monitor usage to ensure sufficient credits to continue using services
  > * Plan credit replenishment based on usage patterns
  > 
  > ### Developer Notes
  > 
  > * All generation services require credit balance
  > * Service access will be restricted when credits are exhausted
  > * Credit consumption is based on specific services and usage volume

- 200 response example: `{"code":200,"msg":"success","data":100}`

#### Get Download URL for Generated Files
- Doc: https://docs.kie.ai/common-api/download-url
- Endpoint: `POST https://api.kie.ai/api/v1/common/download-url`
- Doc prose:

  > # Get Download Link for Generated Files
  > 
  > :::tip[]
  >   Convert generated file URLs into downloadable temporary links. Only supports files generated by kie.ai services.
  > :::
  > 
  > ### Features
  > 
  > * Convert kie.ai generated file URLs into downloadable links
  > * Supports all file types generated by the kie.ai platform (images, videos, audio, etc.)
  > * Temporary download links are valid for 20 minutes
  > * Secure access to generated content
  > * Protected by API Key authentication
  > 
  > ### Important Notes
  > 
  > :::warning[]
  > Only supports file URLs generated by kie.ai services. External file URLs will return a 422 validation error.
  > :::
  > 
  > :::tip[]
  > Downloadable links expire after 20 minutes. Please ensure you download or cache content within this timeframe.
  > :::

- Params:
  - `url` (string, REQUIRED): Image URL (Required)
- Request example from the doc:

```json
"{\n  \"url\": \"https://tempfile.aiquickdraw.com/path/to/image.jpg\" // 图片url（必填）\n}"
```
- 200 response example: `{"code":200,"msg":"success","data":"https://tempfile.1f6cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbd98"}`

#### Base64 File Upload
- Doc: https://docs.kie.ai/file-upload-api/upload-file-base-64
- Endpoint: `POST https://api.kie.ai/api/file-base64-upload`
- Doc prose:

  > :::info[]
  >   Uploaded files are temporary and will be automatically deleted after 24h
  > :::
  > 
  > ### Features
  > 
  > * Supports Base64 encoded data and data URL formats
  > * Automatically identifies MIME types and file extensions
  > * Supports custom filenames or auto-generation (identical filenames will overwrite old files, potential caching delays may occur)
  > * Returns complete file information and download links
  > * Protected by API Key authentication
  > * Uploaded files are temporary and will be automatically deleted after 3 days
  > 
  > ### Supported Formats
  > 
  > * **Plain Base64 strings**: `iVBORw0KGgoAAAANSUhEUgAA...`
  > * **Data URL format**: `data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...`
  > 
  > ### Usage Recommendations
  > 
  > * Recommended for small files such as images
  > * Large files (>10MB) should use the File Stream Upload API
  > * Base64 encoding increases data transmission volume by approximately 33%

- Params:
  - `base64Data` (string, REQUIRED): Base64 encoded file data. Supports pure Base64 strings or data URL format
  - `uploadPath` (string, REQUIRED): File upload path, without leading or trailing slashes
  - `fileName` (string): File name (optional), including file extension. If not provided, a random file name will be generated. If the same file name is uploaded again, the old file will be overwritten, but changes may not take effect immediately due to caching
- Request example from the doc [[with_data_url] Using data URL format]:

```json
{
  "base64Data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
  "uploadPath": "images/base64",
  "fileName": "test-image.png"
}
```
- Request example from the doc [[with_pure_base64] Using pure Base64 string]:

```json
{
  "base64Data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
  "uploadPath": "documents/uploads"
}
```
- 200 response example: `{"success":true,"code":200,"msg":"File uploaded successfully","data":{"fileName":"uploaded-image.png","filePath":"images/user-uploads/uploaded-image.png","downloadUrl":"https://tempfile.redpandaai.co/xxx/images/user-uploads/uploaded-image.png","fileSize":154832,"mimeType":"image/png","uploadedAt":"2025-01-01T12:00:00.000Z"}}`

#### File Stream Upload
- Doc: https://docs.kie.ai/file-upload-api/upload-file-stream
- Endpoint: `POST https://api.kie.ai/api/file-stream-upload` (multipart/form-data)
- Doc prose:

  > :::info[]
  >   Uploaded files are temporary and will be automatically deleted after 24h
  > :::
  > 
  > ### Features
  > 
  > * Supports binary stream upload for multiple file types
  > * Suitable for large file uploads with high transmission efficiency
  > * Automatically identifies MIME types
  > * Supports custom filenames or auto-generation (identical filenames will overwrite old files, potential caching delays may occur)
  > * Returns complete file information and download links
  > * Protected by API Key authentication
  > * Uploaded files are temporary and will be automatically deleted after 3 days
  > 
  > ### Usage Recommendations
  > 
  > * Recommended for large files (>10MB)
  > * Supports multiple formats: images, videos, documents, etc.
  > * Approximately 33% more efficient for transmission compared to Base64 format
  > 
  > ### Example Command
  > 
  > ```bash  theme={null}
  > curl -X POST https://kieai.redpandaai.co/api/file-stream-upload \
  >   -H "Authorization: Bearer YOUR_API_KEY" \
  >   -F "file=@/path/to/your-file.jpg" \
  >   -F "uploadPath=images/user-uploads" \
  >   -F "fileName=custom-name.jpg"
  > ```

- Params:
  - `file` (string, REQUIRED, format=binary): File to upload (binary data)
  - `uploadPath` (string, REQUIRED): File upload path, without leading or trailing slashes
  - `fileName` (string): File name (optional), including file extension. If not provided, a random file name will be generated. If the same file name is uploaded again, the old file will be overwritten, but changes may not take effect immediately due to caching
- 200 response example: `{"success":true,"code":200,"msg":"File uploaded successfully","data":{"fileName":"uploaded-image.png","filePath":"images/user-uploads/uploaded-image.png","downloadUrl":"https://tempfile.redpandaai.co/xxx/images/user-uploads/uploaded-image.png","fileSize":154832,"mimeType":"image/png","uploadedAt":"2025-01-01T12:00:00.000Z"}}`

#### URL File Upload
- Doc: https://docs.kie.ai/file-upload-api/upload-file-url
- Endpoint: `POST https://api.kie.ai/api/file-url-upload`
- Doc prose:

  > :::info[]
  >   Uploaded files are temporary and will be automatically deleted after 24h
  > :::
  > 
  > ### Features
  > 
  > * Supports HTTP and HTTPS file links
  > * Automatically downloads remote files and uploads them
  > * Automatically extracts filenames from URLs or uses custom filenames (identical filenames will overwrite old files, potential caching delays may occur)
  > * Automatically identifies MIME types
  > * Returns complete file information and download links
  > * Protected by API Key authentication
  > * Uploaded files are temporary and will be automatically deleted after 3 days
  > 
  > ### Supported Protocols
  > 
  > * **HTTP**: `http://example.com/file.jpg`
  > * **HTTPS**: `https://example.com/file.jpg`
  > 
  > ### Use Cases
  > 
  > * Migrating files from other services
  > * Batch downloading and storing web resources
  > * Backing up remote files
  > * Caching external resources
  > 
  > ### Important Notes
  > 
  > * Ensure the provided URL is publicly accessible
  > * Download timeout is 30 seconds
  > * Recommended maximum file size is 100MB

- Params:
  - `fileUrl` (string, REQUIRED, format=uri): File download URL, must be a valid HTTP or HTTPS address
  - `uploadPath` (string, REQUIRED): File upload path, without leading or trailing slashes
  - `fileName` (string): File name (optional), including file extension. If not provided, a random file name will be generated. If the same file name is uploaded again, the old file will be overwritten, but changes may not take effect immediately due to caching
- Request example from the doc [[image_from_url] Download image from URL]:

```json
{
  "fileUrl": "https://example.com/images/sample.jpg",
  "uploadPath": "images/downloaded",
  "fileName": "my-downloaded-image.jpg"
}
```
- Request example from the doc [[document_from_url] Download document from URL]:

```json
{
  "fileUrl": "https://example.com/docs/manual.pdf",
  "uploadPath": "documents/manuals"
}
```
- 200 response example: `{"success":true,"code":200,"msg":"File uploaded successfully","data":{"fileName":"uploaded-image.png","filePath":"images/user-uploads/uploaded-image.png","downloadUrl":"https://tempfile.redpandaai.co/xxx/images/user-uploads/uploaded-image.png","fileSize":154832,"mimeType":"image/png","uploadedAt":"2025-01-01T12:00:00.000Z"}}`


### A.3 Audio-driven talking / lip-sync models

#### `kling/ai-avatar-pro` (Kling AI Avatar Pro)
- Doc: https://docs.kie.ai/market/kling/ai-avatar-pro
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `image_url` (string, REQUIRED): The URL of the image to use as your avatar (File URL after upload, not file content; Accepted types: image/jpeg, image/png; Max size: 10.0MB)
  - `audio_url` (string, REQUIRED): The URL of the audio file (must be the URL of the uploaded file, not the file content; supported formats: audio/mpeg, audio/wav, audio/x-wav, audio/aac, audio/mp4, audio/ogg; audio size is limited to 100M, and the duration cannot exceed 5 minutes)
  - `prompt` (string, REQUIRED, maxLength=5000): The prompt to use for the video generation (Max length: 5000 characters)
- Request example from the doc:

```json
{
  "model": "kling/ai-avatar-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "image_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/175792685809077e8h8k3.png",
    "audio_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1757925802302srqfkcqh.mp3",
    "prompt": ""
  }
}
```

#### `kling/ai-avatar-standard` (Kling AI Avatar Standard)
- Doc: https://docs.kie.ai/market/kling/ai-avatar-standard
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `kling/ai-avatar-pro` (no field differences in the docs).

#### `infinitalk/from-audio` (Infinitalk - From Audio)
- Doc: https://docs.kie.ai/market/infinitalk/from-audio
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > Content generation using infinitalk/from-audio

- Params:
  - `image_url` (string, REQUIRED): URL of the input image. If the input image does not match the chosen aspect ratio, it is resized and center cropped. (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `audio_url` (string, REQUIRED): The URL of the audio file. (File URL after upload, not file content; Accepted types: audio/mpeg, audio/wav, audio/x-wav, audio/aac, audio/mp4, audio/ogg; Max size: 10.0MB)
  - `prompt` (string, REQUIRED, maxLength=5000): The text prompt to guide video generation. (Max length: 5000 characters)
  - `resolution` (string, enum=["480p","720p"], default="480p"): Resolution of the video to generate. Must be either 480p or 720p.
  - `seed` (number): Random seed for reproducibility. Valid range is 10000 to 1000000.
- Request example from the doc:

```json
{
  "model": "infinitalk/from-audio",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "image_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1757329269873ggqj2hz3.png",
    "audio_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1757329255705mmqwrnri.mp3",
    "prompt": "A young woman with long dark hair talking on a podcast.",
    "resolution": "480p"
  }
}
```

#### `omnihuman-1-5` (Omnihuman 1.5)
- Doc: https://docs.kie.ai/market/omnihuman-1-5
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Use this endpoint to create a new audio-driven portrait animation task. Upload a portrait image and an audio file, and the model will generate a video of the subject speaking or moving in sync with the audio.

- Params:
  - `image_url` (string, REQUIRED, format=uri): Portrait image URL. Supports any aspect ratio with subjects including people, pets, anime, etc. Accepted file types: image/jpeg, image/png, image/webp. Max file size: 10MB.
  - `mask_url` (array, maxItems=5): Optional mask image URL(s). To have a specific subject in the image speak, use 'Subject Detection' to get the corresponding mask image and pass it as input. Accepted file types: image/jpeg, image/png, image/webp. Max file size: 10MB. Multiple file upload is supported, up to 5 files.
  - `audio_url` (string, REQUIRED, format=uri): Audio URL. Duration must be less than 60 seconds (recommended 15 seconds or less; exceeding this will cause quality degradation). Accepted file types: audio/mpeg, audio/wav, audio/x-wav, audio/aac, audio/ogg, audio/mp4. Max file size: 10MB.
  - `prompt` (string, maxLength=300): Optional prompt text. Limited to Chinese, English, Japanese, Korean, Spanish, and Indonesian. Recommended 300 characters or less. Maximum length: 1000 characters.
  - `output_resolution` (string, enum=["720","1080"], default="1080"): Output video resolution. - `720`: 720P - `1080`: 1080P (default)
  - `pe_fast_mode` (boolean, default=false): Fast mode. Sacrifices some quality to speed up generation. Default value: `false`.
  - `seed` (integer, default=-1): Random seed. Default is `-1` (random). When using the same positive integer and keeping all other parameters identical, the result will be highly consistent.
- Request example from the doc:

```json
{
  "model": "omnihuman-1-5",
  "input": {
    "image_url": "https://your-domain.com/image/portrait.png",
    "mask_url": [
      "https://your-domain.com/image/mask.png"
    ],
    "audio_url": "https://your-domain.com/audio/speech.mp3",
    "prompt": "A person speaking naturally with gentle expressions.",
    "output_resolution": "1080",
    "pe_fast_mode": false,
    "seed": -1
  },
  "callBackUrl": "https://your-domain.com/api/callback"
}
```

#### `omnihuman-1-5/subject-detection` (OmniHuman 1.5 Subject Detection)
- Doc: https://docs.kie.ai/market/omnihuman-1-5/subject-detection
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Use this endpoint to create a new subject detection task. Upload a portrait image and the model will detect subjects in the image, supporting up to 5 subjects.

- Params:
  - `image_url` (string, REQUIRED, format=uri): Portrait image URL. Supports detection of up to 5 subjects in the image. Accepted file types: image/jpeg, image/png, image/jpg. Max file size: 5MB.
- Request example from the doc:

```json
{
  "model": "omnihuman-1-5/subject-detection",
  "input": {
    "image_url": "https://your-domain.com/image/portrait.png"
  },
  "callBackUrl": "https://your-domain.com/api/callback"
}
```

#### `omnihuman-1-5/human-identification` (Omnihuman 1.5 Human Identification)
- Doc: https://docs.kie.ai/market/omnihuman-1-5/human-identification
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Calling this interface creates a new task for recognizing human portraits, human-like figures, or anthropomorphic subjects. Upload a portrait image, and the model will detect and identify the human subjects in the image.

- Params:
  - `image_url` (string, REQUIRED, format=uri): Portrait image URL. Requirements: JPG/PNG/JPEG format, less than 5MB, resolution under 4096x4096. Recommended: single person facing forward, with the face occupying a large proportion of the image. Accepted file types: image/jpeg, image/png, image/jpg. Max file size: 5MB.
- Request example from the doc:

```json
{
  "model": "omnihuman-1-5/human-identification",
  "input": {
    "image_url": "https://your-domain.com/image/portrait.png"
  },
  "callBackUrl": "https://your-domain.com/api/callback"
}
```

#### `volcengine/video-to-video-lip-sync` (Volcengine video to video lip sync)
- Doc: https://docs.kie.ai/market/volcengine/video-to-video-lip-sync
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Use this endpoint to create a new video-to-video lip sync task. Upload a video and an audio file, and the model will drive the video lip movements to match the target audio.
  > 
  > ## Output Specifications
  > 
  > The generated video is returned in MP4 format at 25 fps. The final output duration follows the audio duration: if the source video is longer than the audio, it will be trimmed; if the source video is shorter than the audio, it will be looped.

- Params:
  - `mode` (string, REQUIRED, enum=["lite","basic"]): Service mode for lip-sync generation. - `lite`: For single-person frontal videos. Faster processing. - `basic`: For single-person complex scenes. Supports scene segmentation and speaker identification.
  - `video_url` (string, REQUIRED, format=uri): Video URL. Supported resolution: 360p–1080p. Videos above 1080p will be compressed to 1080p, while videos below 360p are not supported. Supported formats: MOV, MP4, HDR. Recommended codec: H.264. Other formats/codecs may be transcoded. Max file size: 500 MB. Bitrate: 1–30 Mbps. Frame rate: 24–60 fps.
  - `audio_url` (string, REQUIRED, format=uri): Target pure vocal audio URL; used to drive video lip movements. Accepted file types: audio/mpeg, audio/wav, audio/x-wav, audio/aac, audio/mp4, audio/ogg. Max file size: 10MB.
  - `separate_vocal` (boolean, default=false): Enable vocal separation to suppress background noise. Default value: `false`.
  - `open_scenedet` (boolean, default=false): Whether to enable scene segmentation and speaker identification. Supported only in Basic mode. Default value: `false`.
  - `align_audio` (boolean, default=true): Supported in Lite mode. Whether to loop the video when the audio is longer than the video. Default value: `true`.
  - `align_audio_reverse` (boolean, default=false): Supported in Lite mode. Whether to loop the video in reverse (backward). Requires `align_audio` to be set to `true`. Default value: `false`.
  - `templ_start_seconds` (number, default=0): Supported in Lite mode. Start time of the template video, in seconds. Default value: `0`.
- Request example from the doc:

```json
{
  "model": "volcengine/video-to-video-lip-sync",
  "input": {
    "mode": "lite",
    "video_url": "https://your-domain.com/video/example.mp4",
    "audio_url": "https://your-domain.com/audio/speech.mp3",
    "separate_vocal": false,
    "open_scenedet": false,
    "align_audio": true,
    "align_audio_reverse": false,
    "templ_start_seconds": 0
  },
  "callBackUrl": "https://your-domain.com/api/callback"
}
```

#### `wan/2-2-a14b-speech-to-video-turbo` (Wan - 2.2 A14B Speech to Video Turbo)
- Doc: https://docs.kie.ai/market/wan/2-2-a14b-speech-to-video-turbo
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > Generate videos using Wan's advanced AI model

- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): The text prompt used for video generation (Max length: 5000 characters)
  - `image_url` (string, REQUIRED): URL of the input image. If the input image does not match the chosen aspect ratio, it is resized and center cropped (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `audio_url` (string, REQUIRED): The URL of the audio file (File URL after upload, not file content; Accepted types: audio/mp3, audio/wav, audio/ogg, audio/m4a, audio/flac, audio/aac, audio/x-ms-wma, audio/mpeg; Max size: 10.0MB)
  - `num_frames` (number, default=80, minimum=40, maximum=120): Number of frames to generate. Must be between 40 to 120, (must be multiple of 4) (Min: 40, Max: 120, Step: 4) (step: 4)
  - `frames_per_second` (number, default=16, minimum=4, maximum=60): Frames per second of the generated video. Must be between 4 to 60. When using interpolation and adjust_fps_for_interpolation is set to true (default true,) the final FPS will be multiplied by the number of interpolated frames plus one. For example, if the generated frames per second is 16 and the number of interpolated frames is 1, the final frames per second will be 32. If adjust_fps_for_interpolation is set to false, this value will be used as-is (Min: 4, Max: 60, Step: 1) (step: 1)
  - `resolution` (string, enum=["480p","580p","720p"], default="480p"): Resolution of the generated video (480p, 580p, or 720p)
  - `negative_prompt` (string, maxLength=500): Negative prompt for video generation (Max length: 500 characters)
  - `seed` (integer): Random seed for reproducibility. If None, a random seed is chosen
  - `num_inference_steps` (number, default=27, minimum=2, maximum=40): Number of inference steps for sampling. Higher values give better quality but take longer (Min: 2, Max: 40, Step: 1) (step: 1)
  - `guidance_scale` (number, default=3.5, minimum=1, maximum=10): Classifier-free guidance scale. Higher values give better adherence to the prompt but may decrease quality (Min: 1, Max: 10, Step: 0.1) (step: 0.1)
  - `shift` (number, default=5, minimum=1, maximum=10): Shift value for the video. Must be between 1.0 and 10.0 (Min: 1, Max: 10, Step: 0.1) (step: 0.1)
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
{
  "model": "wan/2-2-a14b-speech-to-video-turbo",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "The lady is talking",
    "image_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1756797663082u4pjmcrq.png",
    "audio_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/17567977044127d1emlmc.mp3",
    "num_frames": 80,
    "frames_per_second": 16,
    "resolution": "480p",
    "negative_prompt": "",
    "num_inference_steps": 27,
    "guidance_scale": 3.5,
    "shift": 5
  }
}
```

#### `wan/2-7-image-to-video` (Wan 2.7 - Image to Video)
- Doc: https://docs.kie.ai/market/wan/2-7-image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Use this endpoint to create a new image-to-video generation task.
  > 
  > This model supports the following three generation modes:
  > 
  > - First-frame-to-video: provide `first_frame_url` only
  > - First-and-last-frame-to-video: provide both `first_frame_url` and `last_frame_url`
  > - Video continuation: provide `first_clip_url`

- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Positive prompt. Maximum length: 5000 characters.
  - `negative_prompt` (string, maxLength=500): Negative prompt. Maximum length: 500 characters.
  - `first_frame_url` (string, format=uri): First frame image URL.
  - `last_frame_url` (string, format=uri): Last frame image URL.
  - `first_clip_url` (string, format=uri): First clip video URL, used for video continuation.
  - `driving_audio_url` (string, format=uri): Driving audio URL.
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Video resolution. - `720p`: 720p - `1080p`: 1080p
  - `duration` (integer, default=5, minimum=2, maximum=15): Total output video duration in seconds. - Minimum: `2` - Maximum: `15` - Default: `5`
  - `prompt_extend` (boolean, default=true): Whether to enable intelligent prompt rewriting. Default value: `true`.
  - `watermark` (boolean, default=false): Whether to add an AI-generated watermark. Default value: `false`.
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed. - Minimum: `0` - Maximum: `2147483647`
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc [[1] First and last frame to video]:

```json
{
  "model": "wan/2-7-image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "A white cat stands on a windowsill in warm afternoon light. The camera slowly pushes in as the cat blinks softly and turns to look outside.",
    "negative_prompt": "blurry, flicker, low quality, distorted",
    "first_frame_url": "https://your-domain.com/assets/first-frame.png",
    "last_frame_url": "https://your-domain.com/assets/last-frame.png",
    "resolution": "1080p",
    "duration": 5,
    "prompt_extend": true,
    "watermark": false,
    "seed": 123456
  }
}
```
- Request example from the doc [[2] First frame to video]:

```json
{
  "model": "wan/2-7-image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "A white cat stands on a windowsill in warm afternoon light. The camera slowly pushes in as the cat blinks softly and turns to look outside.",
    "negative_prompt": "blurry, flicker, low quality, distorted",
    "first_frame_url": "https://your-domain.com/assets/first-frame.png",
    "driving_audio_url": "https://your-domain.com/assets/driving-audio.mp3",
    "resolution": "1080p",
    "duration": 5,
    "prompt_extend": true,
    "watermark": false,
    "seed": 123456
  }
}
```

#### `wan/2-7-text-to-video` (Wan 2.7 - Text to Video)
- Doc: https://docs.kie.ai/market/wan/2-7-text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Use this endpoint to create a new text-to-video generation task.

- Params:
  - `prompt` (string, REQUIRED, minLength=1, maxLength=5000): Positive prompt. Minimum length: 1 character. Maximum length: 5000 characters.
  - `negative_prompt` (string, maxLength=500): Negative prompt. Maximum length: 500 characters.
  - `audio_url` (string, format=uri): Optional custom audio URL.
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Video resolution. - `720p`: 720p - `1080p`: 1080p
  - `ratio` (string, enum=["16:9","9:16","1:1","4:3","3:4"], default="16:9"): Video aspect ratio. - `16:9`: Landscape - `9:16`: Portrait - `1:1`: Square - `4:3`: Landscape 4:3 - `3:4`: Portrait 3:4
  - `duration` (integer, default=5, minimum=2, maximum=15): Video duration in seconds. - Minimum: `2` - Maximum: `15` - Default: `5`
  - `prompt_extend` (boolean, default=true): Whether to enable intelligent prompt rewriting. Default value: `true`.
  - `watermark` (boolean, default=false): Whether to add an AI-generated watermark. Default value: `false`.
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed. - Minimum: `0` - Maximum: `2147483647`
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
{
  "model": "wan/2-7-text-to-video",
  "input": {
    "prompt": "A futuristic city street at night, neon reflections shimmering on the wet ground. The camera slowly pushes forward as a silver hover car glides in from the left. Giant holographic billboards flicker in the distance, creating a cinematic atmosphere.",
    "negative_prompt": "blurry, low quality, flicker, distorted characters",
    "audio_url": "https://your-domain.com/audio/custom-track.mp3",
    "resolution": "1080p",
    "ratio": "16:9",
    "duration": 5,
    "prompt_extend": true,
    "watermark": false,
    "seed": 123456
  },
  "callBackUrl": "https://your-domain.com/api/callback"
}
```

#### `wan/2-7-r2v` (Wan 2.7 - Reference to Video)
- Doc: https://docs.kie.ai/market/wan/2-7-r2v
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Use this endpoint to create a new reference-to-video generation task.

- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Text prompt. Required. Describes the desired elements and visual features in the generated video. Supports Chinese and English. Maximum length: 5000 characters.
  - `negative_prompt` (string, maxLength=500): Optional negative prompt describing what should not appear in the video. Supports Chinese and English. Maximum length: 500 characters.
  - `reference_image` (array, maxItems=5): Array of reference image URLs. At least one of `reference_image` or `reference_video` must be provided. The total number of images and videos cannot exceed 5.
  - `reference_video` (array, maxItems=5): Array of reference video URLs. At least one of `reference_image` or `reference_video` must be provided. The total number of images and videos cannot exceed 5.
  - `first_frame` (string, format=uri): First frame image URL. At most one image can be provided. If supplied, `aspect_ratio` is ignored and the output uses a ratio close to the first frame image.
  - `reference_voice` (string, format=uri): Audio URL used to specify the voice timbre of the subject in the reference material. Rules: - If `reference_video` contains audio and `reference_voice` is not provided, the original video audio is used by default - If both `reference_video` and `reference_voice` are provided, `reference_voice` takes priority Audio limits: - Formats: `wav`, `mp3` - Duration: `1` to `10` seconds - File size: up to `15MB`
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Output video resolution tier. Available values: `720p`, `1080p`. Default value: `1080p`.
  - `aspect_ratio` (string, enum=["16:9","9:16","1:1","4:3","3:4"], default="16:9"): Output video aspect ratio. Effective logic: - If `first_frame` is not provided: the video is generated using the specified `aspect_ratio` - If `first_frame` is provided: `aspect_ratio` is ignored and the output uses a ratio close to the first frame image
  - `duration` (integer, default=5, minimum=2, maximum=10): Output video duration in seconds. Valid range is an integer from `2` to `10`. Default value: `5`.
  - `prompt_extend` (boolean, default=true): Whether to enable prompt rewriting. When enabled, the model expands the input prompt. This usually works better for short prompts but increases processing time.
  - `watermark` (boolean, default=false): Whether to add a watermark. The watermark is placed in the lower-right corner of the video with the fixed text "AI generated".
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed. Range: `0-2147483647`. If omitted, the system generates one automatically.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
{
  "model": "wan/2-7-r2v",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Image 1 is eating, while video 1 and image 2 are singing beside it.",
    "negative_prompt": "low resolution, errors, worst quality, low quality, malformed, extra fingers, bad proportions",
    "reference_image": [
      "https://example.com/demo/ref-image-1.png",
      "https://example.com/demo/ref-image-2.png"
    ],
    "reference_video": [
      "https://example.com/demo/ref-video-1.mp4"
    ],
    "first_frame": "https://example.com/demo/first-frame.png",
    "reference_voice": "https://example.com/demo/reference-voice.mp3",
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "duration": 5,
    "prompt_extend": true,
    "watermark": false,
    "seed": 0
  }
}
```


### A.4 Native-audio and general video models

**Veo 3.1, current docs (unified createTask):**

#### `veo-3-1` (Generate Veo3.1 Video)
- Doc: https://docs.kie.ai/veo3-api/generate-veo-3-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > :::warning
  > This is the new version of the API documentation; for the old version of the API, please see [https://docs.kie.ai/old-model/veo3-api/generate-veo-3-video](https://docs.kie.ai/old-model/veo3-api/generate-veo-3-video).
  > :::
  > ### Veo 3.1 Generation API
  > 
  > Our **Veo 3.1 Generation API** is more than a direct wrapper around Google's baseline. It layers extensive optimisation and reliability tooling on top of the official models, giving you greater flexibility and markedly higher success rates — **25% of the official Google pricing** (see [kie.ai/pricing](https://kie.ai/pricing) for full details).
  > 
  > | Capability | Details |
  > | :------------------- | :------ |
  > | **Models** | • **Veo 3.1 Quality** — flagship model, highest fidelity• **Veo 3.1 Fast** — cost-efficient variant that still delivers strong visual results• **Veo 3.1 Lite** — most cost-effective model for high-volume generation |
  > | **Tasks** | • **Text → Video**• **Image → Video** (single reference frame or first and last frames)• **Material → Video** (based on material images) |
  > | **Generation Modes** | • **TEXT\_2\_VIDEO** — Text-to-video: using text prompts only• **FIRST\_AND\_LAST\_FRAMES\_2\_VIDEO** — First and last frames to video: generate transition videos using one or two images• **REFERENCE\_2\_VIDEO** — Material-to-video: based on material images (**Fast model** and **Lite model**, supports **16:9 & 9:16**) |
  > | **Aspect Ratios** | Supports both native **16:9** and **9:16** outputs. **Auto** mode lets the system decide aspect ratio based on input materials and internal strategy (for production control, we recommend explicitly setting `aspect_ratio`). |
  > | **Output Quality** | Both **16:9** and **9:16** support **1080P** and **4K** outputs. **4K requires extra credits** (approximately **2× the credits of generating a Fast mode video**)|
  > | **Audio Track** | All videos ship with background audio by default. In rare cases, upstream may suppress audio when the scene is deemed sensitive (e.g. minors). |
  > 
  > ### Why our Veo 3.1 API is different
  > 
  > 1. **True vertical video** – Native Veo 3.1 supports **9:16** output, delivering authentic vertical videos without the need for re-framing or manual editing.
  > 2. **Global language reach** – Our flow supports multilingual prompts by default (no extra configuration required).
  > 3. **Significant cost savings** – Our rates are 25% of Google's direct API pricing.

- Params:
  - `prompt` (string, REQUIRED): Text prompt describing the desired video content. Required for all generation modes. - Should be detailed and specific in describing video content - Can include actions, scenes, style and other information - For image-to-video, describe how you want the image to come alive
  - `image_urls` (array): Image URL list (used in image-to-video mode). Supports 1 or 2 images: - **1 image**: The generated video will unfold around this image, with the image content presented dynamically - **2 images**: The first image serves as the video's first frame, and the second image serves as the video's last frame, with the video transitioning between them - Must be valid image URLs - Images must be accessible to the API server.
  - `generation_type` (string, enum=["TEXT_2_VIDEO","FIRST_AND_LAST_FRAMES_2_VIDEO","REFERENCE_2_VIDEO"]): Video generation mode (optional). Specifies different video generation approaches: - **TEXT_2_VIDEO**: Text-to-video - Generate videos using only text prompts - **FIRST_AND_LAST_FRAMES_2_VIDEO**: First and last frames to video - Flexible image-to-video generation mode - 1 image: Generate video based on the provided image - 2 images: First image as first frame, second image as last frame, generating transition video - **REFERENCE_2_VIDEO**: Reference-to-video - Generate videos based on reference images, requires 1-3 images in imageUrls (minimum 1, maximum 3) **Important Notes**: - REFERENCE_2_VIDEO mode currently supports the veo3_fast and veo3_lite models. - If not specified, the system will automatically determine the generation mode based on whether imageUrls are provided
  - `aspect_ratio` (string, enum=["16:9","9:16","Auto"], default="16:9"): Video aspect ratio. Specifies the dimension ratio of the generated video. Available options: - 16:9: Landscape video format. - 9:16: Portrait video format, suitable for mobile short videos - Auto: In auto mode, the video will be automatically center-cropped based on whether your uploaded image is closer to 16:9 or 9:16. Default value is 16:9.
  - `enable_fallback` (boolean, default=false): Deprecated Enable fallback functionality. When set to true, if the official Veo3.1 video generation service is unavailable or encounters exceptions, the system will automatically switch to a backup model for video generation to ensure task continuity and reliability. Default value is false. - When fallback is enabled, backup model will be used for the following errors: - public error minor upload - Your prompt was flagged by Website as violating content policies - public error prominent people upload - Fallback mode requires 16:9 aspect ratio and uses 1080p resolution by default - **Note**: Videos generated through fallback mode cannot be accessed via the Get 1080P Video endpoint - **Credit Consumption**: Successful fallback has different credit consumption, please see https://kie.ai/pricing for pricing details **Note: This parameter is deprecated. Please remove this parameter from your …[truncated, see doc]
  - `enable_translation` (boolean, default=false): Enable prompt translation to English. When set to true, the system will automatically translate prompts to English before video generation for better generation results. Default value is true. - true: Enable translation, prompts will be automatically translated to English - false: Disable translation, use original prompts directly for generation
  - `watermark` (string): Watermark text. - Optional parameter - If provided, a watermark will be added to the generated video
  - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): Controls the pixel dimensions of the generated image. Higher resolution results in greater clarity and detail, while lower resolution allows for faster generation.
  - `duration` (integer, enum=[4,6,8], default=8): The duration of the generated video, in seconds. Optional values are 4, 6, 8. **Important Note**: - The REFERENCE_2_VIDEO mode currently only supports a duration of 8 seconds.
- Request example from the doc:

```json
{
  "model": "veo-3-1",
  "callBackUrl": "http://your-callback-url.com/complete",
  "input": {
    "prompt": "A dog playing in a park",
    "image_urls": [
      "http://example.com/image1.jpg",
      "http://example.com/image2.jpg"
    ],
    "watermark": "MyBrand",
    "aspect_ratio": "16:9",
    "enable_fallback": false,
    "enable_translation": true,
    "generation_type": "REFERENCE_2_VIDEO"
  }
}
```

#### `veo/extend` (Extend Veo3.1 Video)
- Doc: https://docs.kie.ai/veo3-api/extend-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `task_id` (string, REQUIRED): The task ID of the original video generation. Must be a valid task ID returned by the video generation API. Note: Videos generated in 1080P cannot be extended.
  - `prompt` (string, REQUIRED): A text prompt describing the content of the extended video. It should detail how you want the video to be extended, including actions, scene changes, styles, etc.
  - `seeds` (integer, minimum=10000, maximum=99999): A random seed parameter that controls the randomness of the generated content. Range: 10000-99999. The same seed will generate similar video content, while different seeds will generate different video content. If not specified, the system will automatically assign a random seed.
  - `watermark` (string): Watermark text (optional). If provided, a watermark will be added to the generated video.
- Request example from the doc:

```json
{
  "model": "veo/extend",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "task_id": "veo_task_abcdef123456",
    "prompt": "The dog continues running through the park, jumping over obstacles and playing with other dogs",
    "seeds": 12345,
    "watermark": "MyBrand"
  }
}
```

#### `veo/get-1080p-video` (Get 1080P Video)
- Doc: https://docs.kie.ai/veo3-api/get-veo-3-1080-p-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `taskId` (string, REQUIRED): taskId
  - `index` (string): video index
- Request example from the doc:

```json
{
  "model": "veo/get-1080p-video",
  "callBackUrl": "https://acceptable-nectarine.us/",
  "input": {
    "taskId": "46",
    "index": 0
  }
}
```
- 200 response example: `{"code":200,"msg":"success","data":{"resultUrl":"https://tempfile.aiquickdraw.com/p/42f4f8facbb040c0ade87c27cb2d5e58_1749711595.mp4"}}`

#### `veo/get-4k-video` (Get 4K Video)
- Doc: https://docs.kie.ai/veo3-api/get-veo-3-4k-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `task_id` (string, REQUIRED): Task ID
  - `index` (integer, default=0): video index
- Request example from the doc:

```json
{
  "model": "veo/get-4k-video",
  "callBackUrl": "http://your-callback-url.com/4k-callback",
  "input": {
    "task_id": "veo_task_abcdef123456",
    "index": 0
  }
}
```
- 200 response example: `{"code":200,"msg":"success","data":{"taskId":"veo_task_abcdef123456","resultUrls":null,"imageUrls":null}}`

**Veo 3.1, legacy dedicated endpoints (docs moved to https://docs.kie.ai/old-model/...):**

#### LEGACY: Generate Veo3.1 Video
- Doc: https://docs.kie.ai/old-model/veo3-api/generate-veo-3-video
- Endpoint: `POST https://api.kie.ai/api/v1/veo/generate`
- Params (top-level JSON body, no `input` wrapper):
  - `prompt` (string, REQUIRED): Text prompt describing the desired video content. Required for all generation modes. - Should be detailed and specific in describing video content - Can include actions, scenes, style and other information - For image-to-video, describe how you want the image to come alive
  - `imageUrls` (array): Image URL list (used in image-to-video mode). Supports 1 or 2 images: - **1 image**: The generated video will unfold around this image, with the image content presented dynamically - **2 images**: The first image serves as the video's first frame, and the second image serves as the video's last frame, with the video transitioning between them - Must be valid image URLs - Images must be accessible to the API server.
  - `model` (string, enum=["veo3","veo3_fast","veo3_lite"], default="veo3_fast"): Select the model type to use. - veo3: Veo 3.1 Quality, supports both text-to-video and image-to-video generation - veo3_fast: Veo3.1 Fast generation model, supports both text-to-video、image-to-video and materials-to-video generation - veo3_lite: Veo3.1 Lite generation model, supports both text-to-video、image-to-video and materials-to-video generation
  - `generationType` (string, enum=["TEXT_2_VIDEO","FIRST_AND_LAST_FRAMES_2_VIDEO","REFERENCE_2_VIDEO"]): Video generation mode (optional). Specifies different video generation approaches: - **TEXT_2_VIDEO**: Text-to-video - Generate videos using only text prompts - **FIRST_AND_LAST_FRAMES_2_VIDEO**: First and last frames to video - Flexible image-to-video generation mode - 1 image: Generate video based on the provided image - 2 images: First image as first frame, second image as last frame, generating transition video - **REFERENCE_2_VIDEO**: Reference-to-video - Generate videos based on reference images, requires 1-3 …[truncated, see doc]
  - `aspect_ratio` (string, enum=["16:9","9:16","Auto"], default="16:9"): Video aspect ratio. Specifies the dimension ratio of the generated video. Available options: - 16:9: Landscape video format. - 9:16: Portrait video format, suitable for mobile short videos - Auto: In auto mode, the video will be automatically center-cropped based on whether your uploaded image is closer to 16:9 or 9:16. Default value is 16:9.
  - `enableFallback` (boolean, default=false): Deprecated Enable fallback functionality. When set to true, if the official Veo3.1 video generation service is unavailable or encounters exceptions, the system will automatically switch to a backup model for video generation to ensure task continuity and reliability. Default value is false. - When fallback is enabled, backup model will be used for the following errors: - public error minor upload - Your prompt was flagged by Website as violating content policies - public error prominent people upload - Fallback mod …[truncated, see doc]
  - `enableTranslation` (boolean, default=false): Enable prompt translation to English. When set to true, the system will automatically translate prompts to English before video generation for better generation results. Default value is true. - true: Enable translation, prompts will be automatically translated to English - false: Disable translation, use original prompts directly for generation
  - `watermark` (string): Watermark text. - Optional parameter - If provided, a watermark will be added to the generated video
  - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): Controls the pixel dimensions of the generated image. Higher resolution results in greater clarity and detail, while lower resolution allows for faster generation.
  - `duration` (integer, enum=[4,6,8], default=8): The duration of the generated video, in seconds. Optional values are 4, 6, 8. **Important Note**: - The REFERENCE_2_VIDEO mode currently only supports a duration of 8 seconds.
- Request example from the doc:

```json
{
  "prompt": "A dog playing in a park",
  "imageUrls": [
    "http://example.com/image1.jpg",
    "http://example.com/image2.jpg"
  ],
  "model": "veo3_fast",
  "watermark": "MyBrand",
  "callBackUrl": "http://your-callback-url.com/complete",
  "aspect_ratio": "16:9",
  "enableFallback": false,
  "enableTranslation": true,
  "generationType": "REFERENCE_2_VIDEO"
}
```

#### LEGACY: Get Veo3.1 Video Details
- Doc: https://docs.kie.ai/old-model/veo3-api/get-veo-3-video-details
- Endpoint: `GET https://api.kie.ai/api/v1/veo/record-info`
- Query params:
  - query `taskId` req=true type=string enum=null default=null ex="veo_task_abcdef123456" :: Task ID
- 200 response example: `{"code":200,"msg":"success","data":{"taskId":"veo_task_abcdef123456","paramJson":"{\"prompt\":\"A futuristic city with flying cars at sunset.\",\"waterMark\":\"KieAI\"}","completeTime":"2025-06-06 10:30:00","response":{"taskId":"veo_task_abcdef123456","resultUrls":["http://example.com/video1.mp4"],"originUrls":["http://example.com/original_video1.mp4"],"fullResultUrls":["http://example.com/full_result.mp4"],"resolution":"1080p"},"successFlag":1,"errorCode":null,"errorMessage":"","createTime":"2025-06-06 10:25:00","fallbackFlag":false}}`

#### LEGACY: Get 1080P Video
- Doc: https://docs.kie.ai/old-model/veo3-api/get-veo-3-1080-p-video
- Endpoint: `GET https://api.kie.ai/api/v1/veo/get-1080p-video`
- Query params:
  - query `taskId` req=true type=string enum=null default=null ex="veo_task_abcdef123456" :: Task ID
  - query `index` req=false type=integer enum=null default=null ex=0 :: video index
- 200 response example: `{"code":200,"msg":"success","data":{"resultUrl":"https://tempfile.aiquickdraw.com/p/42f4f8facbb040c0ade87c27cb2d5e58_1749711595.mp4"}}`

#### LEGACY: Get 4K Video
- Doc: https://docs.kie.ai/old-model/veo3-api/get-veo-3-4k-video
- Endpoint: `POST https://api.kie.ai/api/v1/veo/get-4k-video`
- Params (top-level JSON body, no `input` wrapper):
  - `taskId` (string, REQUIRED): Task ID
  - `index` (integer, default=0): video index
- Request example from the doc:

```json
{
  "taskId": "veo_task_abcdef123456",
  "index": 0,
  "callBackUrl": "http://your-callback-url.com/4k-callback"
}
```
- 200 response example: `{"code":200,"msg":"success","data":{"taskId":"veo_task_abcdef123456","resultUrls":null,"imageUrls":null}}`

#### LEGACY: Extend Veo3.1 Video
- Doc: https://docs.kie.ai/old-model/veo3-api/extend-video
- Endpoint: `POST https://api.kie.ai/api/v1/veo/extend`
- Params (top-level JSON body, no `input` wrapper):
  - `taskId` (string, REQUIRED): Task ID of the original video generation. Must be a valid taskId returned from the video generation interface. Note: Videos generated after 1080P generation cannot be extended.
  - `prompt` (string, REQUIRED): Text prompt describing the extended video content. Should detail how you want the video to be extended, including actions, scene changes, style, etc.
  - `seeds` (integer, minimum=10000, maximum=99999): Random seed parameter for controlling the randomness of generated content. Range: 10000-99999. Same seeds will generate similar video content, different seeds will generate different video content. If not specified, the system will automatically assign random seeds.
  - `model` (string, enum=["fast","quality","lite"], default="fast"): Model type for video extension (optional). Defaults to `fast` if not specified. - **fast**: Fast generation mode - **quality**: High quality generation mode - **lite**: Most cost-effective generation mode
  - `watermark` (string): Watermark text (optional). If provided, a watermark will be added to the generated video.
- Request example from the doc:

```json
{
  "taskId": "veo_task_abcdef123456",
  "prompt": "The dog continues running through the park, jumping over obstacles and playing with other dogs",
  "seeds": 12345,
  "watermark": "MyBrand",
  "callBackUrl": "https://your-callback-url.com/veo-extend-callback",
  "model": "fast"
}
```

**Kling:**

#### `kling-3.0/video` (Kling 3.0)
- Doc: https://docs.kie.ai/market/kling/kling-3-0
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > Generate high-quality videos with advanced multi-shot capabilities and element references using Kling 3.0 AI 
  > 
  > ## Overview
  > 
  > Kling 3.0 is an advanced video generation model that supports both single-shot and multi-shot video creation with element references. It offers two generation modes (standard and pro) with different resolution options, and supports sound effects for enhanced video output.
  > 
  > ## Key Features
  > 
  > - **Multiple Generation Modes**: Choose between `std` (standard resolution), `pro` (higher resolution), and `4K` (ultra-high resolution) modes
  > - **Multi-Shot Support**: Create videos with multiple shots, each with its own prompt and duration
  > - **Element Reference**: Use the `@element_name` syntax to reference image/video/audio elements within prompts
  > - **Sound Effects**: Optional sound effects to enhance video output
  > - **Flexible Aspect Ratios**: Support for 16:9, 9:16, and 1:1 aspect ratios
  > - **Configurable Duration**: Video duration from 3 to 15 seconds
  > 
  > ## Resolution Mappings
  > 
  > The resolution depends on both the `mode` and `aspect_ratio` parameters:
  > 
  > <Tabs groupId="mode">
  > <TabItem value="std" label="Standard Mode (std)">
  > 
  > | Aspect Ratio | Resolution |
  > |--------------|------------|
  > | 16:9         | 1280×720   |
  > | 9:16         | 720×1280   |
  > | 1:1          | 720×720    |
  > 
  > </TabItem>
  > <TabItem value="pro" label="Pro Mode (pro)">
  > 
  > | Aspect Ratio | Resolution |
  > |--------------|------------|
  > | 16:9         | 1920×1080  |
  > | 9:16         | 1080×1920  |
  > | 1:1          | 1080×1080  |
  > 
  > </TabItem>
  > <TabItem value="4K" label="4K Mode (4K)">
  > 
  > | Aspect Ratio | Resolution |
  > |--------------|------------|
  > | 16:9         | 3840×2160  |
  > | 9:16         | 2160×3840  |
  > | 1:1          | 2160×2160  |
  > 
  > </TabItem>
  > </Tabs>
  > 
  > :::info[]
  > 4K mode provides higher resolution output but may take longer to generate and consume more credits.
  > :::
  > 
  > ## Single-Shot vs Multi-Shot Mode
  > 
  > ### Single-Shot Mode (`multi_shots: false`)
  > - Uses the main `prompt` field for video generation
  > - Supports first and last frame images via `image_urls`
  > - Sound effects are optional
  > 
  > ### Multi-Shot Mode (`multi_shots: true`)
  > - Uses `multi_prompt` array to define multiple shots
  > - Each shot has its own prompt and duration (1-12 seconds)
  > - Only supports first frame image (via `image_urls[0]`)
  > - Sound effects default to enabled
  > - The maximum number of characters per shot is 500
  > 
  > ## Aspect Ratio Auto-Adaptation
  > 
  > When you provide `image_urls` (first and/or last frame images), the `aspect_ratio` parameter becomes optional. The system will automatically adapt the aspect ratio based on the uploaded images, so you don't need to specify it manually.
  > 
  > :::tip[]
  > If you upload reference images, you can omit the `aspect_ratio` parameter and let the system automatically match the aspect ratio of your images.
  > :::
  > 
  > ## Element References
  > 
  > You can reference element in your prompts using the `@element_name` syntax. Define elements in the `kling_elements` array:
  > 
  > - **Image Elements**: 2-4 image URLs (JPG/PNG, max 10MB each)
  > - **Video Elements**: Up to 1 video URL (MP4/MOV format, the video duration must be at least 3 seconds, and the effective segment length should be between 3 and 8 seconds)
  > - **Audio Reference**: Up to 1 audio URL (audio duration must be between 5 and 30 seconds)
  > 
  > :::tip[]
  > Use descriptive element na
  > …[doc prose truncated, see doc]

- Params:
  - `prompt` (string, REQUIRED): Video generation prompt. Takes effect when multi_shots is false.
  - `image_urls` (array): First and last frame image URLs. Required when elements are referenced in the prompt (using @element_name syntax). When multi_shots is false: if length is 2, index 0 is the first frame and index 1 is the last frame; if length is 1, the array item serves as the first frame. When multi_shots is true: only the first frame is supported.
  - `sound` (boolean, REQUIRED, default=false): Whether to enable sound effects. true enables sound effects, false disables them. When multi_shots is true, this field defaults to true.
  - `duration` (string, REQUIRED, enum=["3","4","5","6","7","8","9","10","11","12","13","14","15"], default="5"): Total video duration in seconds. Integer value, range: 3 to 15.
  - `aspect_ratio` (string, REQUIRED, enum=["16:9","9:16","1:1"], default="16:9"): Video aspect ratio. Options: 16:9, 9:16, 1:1. When image_urls(first and last frame images) is provided, this parameter is optional and the aspect ratio will be automatically adapted based on the uploaded images.
  - `mode` (string, REQUIRED, enum=["std","pro","4K"], default="pro"): Generation mode. std has standard resolution, pro has higher resolution, 4K has 4K resolution. Resolution mapping: - **std mode**: 16:9 (1280×720), 9:16 (720×1280), 1:1 (720×720) - **pro mode**: 16:9 (1920×1080), 9:16 (1080×1920), 1:1 (1080×1080) - **4K mode**: 16:9 (3840×2160), 9:16 (2160×3840), 1:1 (2160×2160)
  - `multi_shots` (boolean, REQUIRED, default=false): Whether to use multi-shot mode. true enables multi-shot mode, false enables single-shot mode.
  - `multi_prompt` (array, REQUIRED): Shot prompts. Takes effect when multi_shots is true. Used to describe the text and duration of each shot. Supports up to 5 shots. Each shot duration is 1-12 seconds. If you need to use elements, add them after the prompt.
  - `multi_prompt[].prompt` (string, REQUIRED, maxLength=500): Prompt text for this shot, a maximum of 500 characters per shot. Each @element will occupy 37 characters.
  - `multi_prompt[].duration` (integer, REQUIRED, minimum=1, maximum=12): Duration of this shot in seconds. Range: 1-12.
  - `kling_elements` (array, maxItems=3): Referenced elements. Detailed information about elements referenced in the prompt. A single task can reference a maximum of three elements.
  - `kling_elements[].name` (string, REQUIRED): Element name, used in prompt with @ prefix (e.g., @element_dog)
  - `kling_elements[].description` (string, REQUIRED): Element description
  - `kling_elements[].element_input_urls` (array, REQUIRED): Image URLs for the element. 2-4 URLs required. Accepted formats: JPG, PNG. Maximum file size: 10MB per image.
  - `kling_elements[].element_input_audio_urls` (array): Optional. List of audio material URLs for characters. The audio duration must be between 5 and 30 seconds.
  - `kling_elements[].start_time` (integer): Start time for video character material capture (in milliseconds). Only effective when uploading videos through element_input_urls. If not uploaded, it defaults to 0.
  - `kling_elements[].end_time` (integer): End time for video character material capture (in milliseconds). Only effective when uploading videos through element_input_urls. Must be greater than start_time, and the difference between end_time and start_time must be within 3000 to 8000 milliseconds.
- Request example from the doc:

```json
{
  "model": "kling-3.0/video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "In a bright rehearsal room, sunlight streams through the window @element_dog",
    "image_urls": [
      "https://static.aiquickdraw.com/tools/example/1764851002741_i0lEiI8I.png"
    ],
    "sound": true,
    "duration": "5",
    "aspect_ratio": "16:9",
    "mode": "pro",
    "multi_shots": false,
    "multi_prompt": [
      {
        "prompt": "a happy dog in running @element_cat",
        "duration": 3
      },
      {
        "prompt": "a happy dog play with a cat @element_dog",
        "duration": 2
      }
    ],
    "kling_elements": [
      {
        "name": "element_dog",
        "description": "dog",
        "element_input_urls": [
          "https://tempfileb.aiquickdraw.com/kieai/market/1770361808044_4RfUUJrI.jpeg",
          "https://tempfileb.aiquickdraw.com/kieai/market/1770361848336_ABQqRHBi.png"
        ],
        "element_input_audio_urls": [
          "https://your-cdn.com/wjeoiajfosijfoi.mp3"
        ]
      },
      {
        "name": "element_cat",
        "description": "cat",
        "element_input_urls": [
          "https://your-cdn.com/element_image.mp4"
        ],
        "element_input_audio_urls": [
          "https://your-cdn.com/wjeoiajfosijfoi.mp3"
        ],
        "start_time": 0,
        "end_time": 8000
      }
    ]
  }
}
```

#### `kling/v3-turbo-text-to-video` (Kling - V3 Turbo Text to Video)
- Doc: https://docs.kie.ai/market/kling/v3-turbo-text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=2500, examples=["Outdoor terrace of a European villa, by a dining table with a blue and white checkered tablecloth, a young white woman in a blue and white striped short-sleeve shirt and khaki shorts, with a brown belt, sits barefoot, opposite a young white man in a white T-shirt.The camera zooms in, the woman swirls the juice in a glass, her eyes looking at the distant woods, and says, \"These trees will turn yellow in a month, won't they?\"Close-up of the man, he lowers his head and says, \"But they'll be green again next summer.\"Then the woman turns her head, smiles at the man opposite, and says, \"Are you always this optimistic? Or just about summer?\"Then the man lifts his head, looks at the woman an...(trunc)): The text description of the video you want to generate (Max length: 2500 characters)
  - `duration` (string, REQUIRED, default="5"): The duration of the generated video in seconds Optional duration: 3s - 15s
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","9:16","16:9"], default="16:9"): The aspect ratio of the generated video frame
  - `resolution` (string, REQUIRED, enum=["720p","1080p"], default="720p"): Resolution of the generated video (720p or 1080p)
- Request example from the doc:

```json
{
  "model": "kling/v3-turbo-text-to-video",
  "input": {
    "prompt": "Outdoor terrace of a European villa, by a dining table with a blue and white checkered tablecloth, a young white woman in a blue and white striped short-sleeve shirt and khaki shorts, with a brown belt, sits barefoot, opposite a young white man in a white T-shirt.\n\nThe camera zooms in, the woman swirls the juice in a glass, her eyes looking at the distant woods, and says, \"These trees will turn yellow in a month, won't they?\"\n\nClose-up of the man, he lowers his head and says, \"But they'll be green again next summer.\"\n\nThen the woman turns her head, smiles at the man opposite, and says, \"Are you always this optimistic? Or just about summer?\"\n\nThen the man lifts his head, l…",
    "duration": "5",
    "aspect_ratio": "16:9",
    "resolution": "720p"
  }
}
```

#### `kling/v3-turbo-image-to-video` (Kling - V3 Turbo Image to Video)
- Doc: https://docs.kie.ai/market/kling/v3-turbo-image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=2500, examples=["Outdoor terrace of a European villa, by a dining table with a blue and white checkered tablecloth, a young white woman in a blue and white striped short-sleeve shirt and khaki shorts, with a brown belt, sits barefoot, opposite a young white man in a white T-shirt.The camera zooms in, the woman swirls the juice in a glass, her eyes looking at the distant woods, and says, \"These trees will turn yellow in a month, won't they?\"Close-up of the man, he lowers his head and says, \"But they'll be green again next summer.\"Then the woman turns her head, smiles at the man opposite, and says, \"Are you always this optimistic? Or just about summer?\"Then the man lifts his head, looks at the woman an...(trunc)): The text prompt describing the video to generate (Max length: 2500 characters)
  - `image_urls` (array, REQUIRED): URL of the image to be used for the video (File URL after upload, not file content; Accepted types: image/jpeg, image/png; Max size: 10.0MB)
  - `duration` (string, REQUIRED, default="5"): The duration of the generated video in seconds Optional duration: 3s - 15s
  - `resolution` (string, REQUIRED, enum=["720p","1080p"], default="720p"): Resolution of the generated video (720p or 1080p)
- Request example from the doc:

```json
{
  "model": "kling/v3-turbo-image-to-video",
  "input": {
    "image_urls": [
      "https://static.aiquickdraw.com/tools/example/1770688028208_jxcvxCQm.png"
    ],
    "prompt": "Outdoor terrace of a European villa, by a dining table with a blue and white checkered tablecloth, a young white woman in a blue and white striped short-sleeve shirt and khaki shorts, with a brown belt, sits barefoot, opposite a young white man in a white T-shirt.\n\nThe camera zooms in, the woman swirls the juice in a glass, her eyes looking at the distant woods, and says, \"These trees will turn yellow in a month, won't they?\"\n\nClose-up of the man, he lowers his head and says, \"But they'll be green again next summer.\"\n\nThen the woman turns her head, smiles at the man opposite, and says, \"Are you always this optimistic? Or just about summer?\"\n\nThen the man lifts his head, l…",
    "duration": "5",
    "resolution": "720p"
  }
}
```

#### `kling-2.6/text-to-video` (Kling 2.6 Text to Video)
- Doc: https://docs.kie.ai/market/kling/text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=1000): Text prompt for video generation (maximum length: 1000 characters)
  - `sound` (boolean, REQUIRED): This parameter specifies whether the generated video contains sound (boolean: true/false)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","16:9","9:16"], default="1:1"): This parameter defines the video aspect ratio
  - `duration` (string, REQUIRED, enum=["5","10"], default="5"): Video duration (unit: seconds)
- Request example from the doc:

```json
{
  "model": "kling-2.6/text-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Scene: A fashion live-streaming sales setting, with clothes hanging on racks and the host's figure reflected in a full-length mirror. Lines: [African female host] turns around to showcase the hoodie's cut. [African female host, in a cheerful tone] says: \"360-degree flawless tailoring, slimming and versatile.\" She then [African female host] leans closer to the camera. [African female host, in a lively tone] says: \"Double-sided fleece fabric, $30 off immediately when you order now.\"",
    "sound": false,
    "aspect_ratio": "1:1",
    "duration": "5"
  }
}
```

#### `kling-2.6/image-to-video` (Kling 2.6 Image to Video)
- Doc: https://docs.kie.ai/market/kling/image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=1000): Text prompt for video generation (maximum length: 1000 characters)
  - `image_urls` (array, REQUIRED, maxItems=1): Image URLs for video generation. (Uploaded file URLs, not file content; supported types: image/jpeg, image/png; maximum file size: 10.0MB)
  - `sound` (boolean, REQUIRED): This parameter specifies whether the generated video contains sound (boolean: true/false)
  - `duration` (string, REQUIRED, enum=["5","10"], default="5"): Video duration (unit: seconds)
- Request example from the doc:

```json
{
  "model": "kling-2.6/image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "In a bright rehearsal room, sunlight streams through the windows, and a standing microphone is placed in the center of the room. [Campus band female lead singer] stands in front of the microphone with her eyes closed, and other members stand around her. [Campus band female lead singer, singing loudly] Lead vocal: \"I will do my best to heal you, with all my heart and soul...\" The background is a cappella harmonies, and the camera slowly pans around the band members.",
    "image_urls": [
      "https://static.aiquickdraw.com/tools/example/1764851002741_i0lEiI8I.png"
    ],
    "sound": false,
    "duration": "5"
  }
}
```

#### `kling-3.0-omni/text-to-video` (Kling 3.0 Omni Text to Video)
- Doc: https://docs.kie.ai/market/kling/v3-omni-text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=1, maxLength=3072): Text description of the video. It must not be empty after leading and trailing whitespace is removed, and must not exceed 3,072 characters.
  - `customize_multi_shots` (boolean, default=true): Whether to enable multi-shot mode. Explicitly specifying this value is recommended. `true` enables multiple shots; `false` uses a single shot.
  - `prefer_multi_shots` (boolean): Whether to enable intelligent shot planning. This field is mutually exclusive with `customize_multi_shots`. Both fields may be `false`, but they cannot both be `true`.
  - `multi_prompt` (array, default=[], maxItems=6): List of custom shots. When `customize_multi_shots` is `true`, this field is required, must not be empty, and supports up to 6 shots. When `customize_multi_shots` is `false`, it must be an empty array or omitted.
  - `multi_prompt[].prompt` (string, REQUIRED, minLength=1, maxLength=512): Video description for the current shot. Maximum length: 512 characters.
  - `multi_prompt[].duration` (integer, REQUIRED, minimum=1, maximum=15): Duration of the current shot in seconds. The supported range is 1 to 15 seconds.
  - `elements` (array, default=[]): List of one-time subject assets. The default is an empty array. When using only multi-image subjects, up to 7 subjects can be uploaded. When using only video character subjects, the number of video character subjects must not exce …[truncated, see doc]
  - `elements[].name` (string, REQUIRED, minLength=1): Subject name. It must be unique within the same request and can be referenced in the `prompt` field using `@name`.
  - `elements[].description` (string, REQUIRED, minLength=1): Text description of the subject asset.
  - `elements[].element_input_urls` (array, REQUIRED, minItems=1, maxItems=4): List of image URLs for a multi-image subject (provide 2 to 4 images), or a video URL for a video character subject (provide exactly 1 video). Images and videos cannot be mixed. HTTP, HTTPS, and OSS URLs are supported.
  - `elements[].element_input_audio_urls` (array, default=[]): Optional list of subject audio asset URLs. HTTP, HTTPS, and OSS URLs are supported.
  - `audio` (boolean, default=false): Whether to add audio to the generated video. `true` enables audio; `false` disables audio.
  - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): Resolution of the generated video. Available values are `720p` (outputs a 720p video), `1080p` (outputs a 1080p video), and `4k` (outputs a 4K video).
  - `aspect_ratio` (string, enum=["16:9","9:16","1:1"], default="16:9"): Aspect ratio of the generated video. Supported values are `16:9`, `9:16`, and `1:1`.
  - `duration` (integer, enum=[3,4,5,6,7,8,9,10,11,12,13,14,15], default=5, minimum=3, maximum=15): Total video duration in seconds. The supported range is 3 to 15 seconds, and the default is 5 seconds.

#### `kling-3.0-omni/image-to-video` (Kling 3.0 Omni  Image To Video)
- Doc: https://docs.kie.ai/market/kling/v3-omni-image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - **oneOf variant 0 (Single First Frame):**
    - `prompt` (string, REQUIRED, maxLength=3072): Video description. It must not be empty after leading and trailing whitespace is removed. Maximum length: 3,072 characters.
    - `image_urls` (array, REQUIRED, minItems=1, maxItems=1): Array of first-frame image URLs. Exactly 1 image is required. HTTP, HTTPS, and OSS URLs are supported. Images must be in JPG, JPEG, or PNG format; each file must not exceed 50 MB; both width and height must be at least 300 px; and …[truncated, see doc]
    - `duration` (integer, enum=[3,4,5,6,7,8,9,10,11,12,13,14,15], default=5, minimum=3, maximum=15): Total video duration in seconds. Optional; the default is 5 seconds. Supports integer values from 3 to 15.
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): Video resolution. `720p` outputs a 720p video, `1080p` outputs a 1080p video, and `4k` outputs a 4K video.
    - `aspect_ratio` (string, enum=["16:9","9:16","1:1","auto"], default="auto"): Video aspect ratio. `16:9`, `9:16`, and `1:1` can be selected only when custom multi-shot mode is enabled through `customize_multi_shots`; otherwise, use `auto`.
    - `audio` (boolean): Whether to enable audio. Passing this value explicitly is recommended. `true` enables audio; `false` disables audio.
    - `customize_multi_shots` (boolean): Whether to enable multiple shots. Passing this value explicitly is recommended.
    - `prefer_multi_shots` (boolean): Whether to enable intelligent shot planning. This field is mutually exclusive with `customize_multi_shots`.
    - `multi_prompt` (array, minItems=1, maxItems=6): List of custom shots. When `customize_multi_shots=true`, this field is required and may contain up to 6 shots. When `customize_multi_shots=false`, it must be an empty array or omitted.
    - `multi_prompt[].duration` (integer, REQUIRED, minimum=1, maximum=15): Duration of the current shot in seconds. Supports 1 to 15 seconds.
    - `multi_prompt[].prompt` (string, REQUIRED, minLength=1, maxLength=512): Video description for the current shot. Maximum length: 512 characters.
    - `elements` (array, default=[], maxItems=3): List of one-time subject assets. The default is an empty array, with up to 3 subjects. The subject is automatically identified as a multi-image subject or video character subject based on `element_input_urls`.
    - `elements[].name` (string, REQUIRED): Subject name. It must be unique within the same request and can be referenced in the prompt using `@name`.
    - `elements[].description` (string, REQUIRED): Subject description.
    - `elements[].element_input_urls` (array, REQUIRED, minItems=1, maxItems=4): For a multi-image subject, provide 2 to 4 images. For a video character subject, provide exactly 1 video. Images and videos cannot be mixed. HTTP, HTTPS, and OSS URLs are supported.
    - `elements[].element_input_audio_urls` (array, default=[]): Optional list of subject reference audio URLs. It may be omitted or passed as an empty array. If the audio duration can be determined, it must be between 5 and 30 seconds.
    - `elements[].start_time` (integer, default=0, minimum=0): Start time for trimming the video character subject, in milliseconds. The default is 0. This applies only when a video is provided in `element_input_urls`.
    - `elements[].end_time` (integer, default=8000, minimum=3000): End time for trimming the video character subject, in milliseconds. The default is 8,000. It must be greater than `start_time`, and the trimmed duration must be between 3,000 and 8,000 milliseconds.
  - **oneOf variant 1 (First and Last Frames):**
    - `prompt` (string, REQUIRED, maxLength=3072)
    - `image_urls` (array, REQUIRED, minItems=2, maxItems=2)
    - `duration` (integer, enum=[3,4,5,6,7,8,9,10,11,12,13,14,15], default=5, minimum=3, maximum=15)
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p")
    - `aspect_ratio` (string, enum=["16:9","9:16","1:1","auto"], default="auto")
    - `audio` (boolean)
    - `customize_multi_shots` (boolean, default=false)
    - `prefer_multi_shots` (boolean)
    - `multi_prompt` (array, minItems=1, maxItems=6)
    - `elements` (array, default=[], maxItems=3)

#### `kling-3.0-omni/reference-to-video` (Kling 3.0 Omni Reference To Video)
- Doc: https://docs.kie.ai/market/kling/v3-omni-reference-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - **oneOf variant 0 (No Video Input):**
    - `prompt` (string, REQUIRED, minLength=1, maxLength=3072): Video description. It must not be empty after leading and trailing whitespace is removed. Maximum length: 3,072 characters.
    - `image_urls` (array, REQUIRED, maxItems=7): Array of reference image URLs. The maximum number of images depends on the number and types of reference subjects. When there is no reference video and only multi-image subjects are used, the combined number of reference images an …[truncated, see doc]
    - `duration` (integer, enum=[3,4,5,6,7,8,9,10,11,12,13,14,15], default=5, minimum=3, maximum=15): Total video duration in seconds. Optional; the default is 5 seconds. Supports integer values from 3 to 15.
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): Video resolution. `720p` outputs a 720p video, `1080p` outputs a 1080p video, and `4k` outputs a 4K video.
    - `aspect_ratio` (string, enum=["16:9","9:16","1:1"], default="16:9"): When no video is provided, `16:9`, `9:16`, and `1:1` are supported.
    - `audio` (boolean): Whether to enable audio. When no video is provided, both `true` and `false` are supported.
    - `customize_multi_shots` (boolean): Whether to enable multiple shots. Both `true` and `false` are supported.
    - `prefer_multi_shots` (boolean): Whether to enable intelligent shot planning. This field is mutually exclusive with `customize_multi_shots`.
    - `multi_prompt` (array, minItems=1, maxItems=6): List of custom shots. When `customize_multi_shots=true`, this field is required, must not be empty, and may contain up to 6 shots. When `customize_multi_shots=false`, it must be an empty array or omitted.
    - `multi_prompt[].prompt` (string, REQUIRED, minLength=1, maxLength=512): Video description for the current shot. Maximum length: 512 characters.
    - `multi_prompt[].duration` (integer, REQUIRED, minimum=1, maximum=15): Duration of the current shot in seconds.
    - `elements` (array, default=[]): List of one-time subject assets. The default is an empty array. The number of subjects is jointly limited by the reference images, reference video, and subject types. When there is no reference video and only multi-image subjects …[truncated, see doc]
    - `elements[].name` (string, REQUIRED): Subject name. It must be unique within the same request and can be referenced in the prompt using `@name`.
    - `elements[].description` (string, REQUIRED): Subject description.
    - `elements[].element_input_urls` (array, REQUIRED, minItems=1, maxItems=4): URLs of the subject image or video assets. Provide 1 to 4 URLs.
    - `elements[].element_input_audio_urls` (array, default=[]): Optional list of subject reference audio URLs. If the duration can be determined, it must be between 5 and 30 seconds.
    - `elements[].start_time` (integer, default=0): Start time for trimming the video character subject, in milliseconds. The default is 0.
    - `elements[].end_time` (integer, default=8000): End time for trimming the video character subject, in milliseconds. The default is 8,000.
  - **oneOf variant 1 (Video Input Only):**
    - `prompt` (string, REQUIRED, minLength=1, maxLength=3072)
    - `video_urls` (array, REQUIRED, minItems=1, maxItems=1)
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p")
    - `aspect_ratio` (string, REQUIRED, enum=["auto"], default="auto")
    - `audio` (boolean, REQUIRED)
    - `elements` (array, default=[])
  - **oneOf variant 2 (Video with Images):**
    - `prompt` (string, REQUIRED, minLength=1, maxLength=3072)
    - `image_urls` (array, REQUIRED, maxItems=4)
    - `video_urls` (array, REQUIRED, minItems=1, maxItems=1)
    - `duration` (integer, enum=[3,4,5,6,7,8,9,10,11,12,13,14,15], default=5, minimum=3, maximum=15)
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p")
    - `aspect_ratio` (string, enum=["16:9","9:16","1:1"], default="16:9")
    - `audio` (boolean, REQUIRED)
    - `elements` (array, default=[])

#### `kling-3.0-omni/transformation` (Kling 3.0 Omni Transformation)
- Doc: https://docs.kie.ai/market/kling/v3-omni-transformation
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - **oneOf variant 0 (Video Input Only):**
    - `prompt` (string, REQUIRED, minLength=1, maxLength=3072): Video description. It must not be empty after leading and trailing whitespace is removed. Maximum length: 3,072 characters.
    - `video_urls` (array, REQUIRED, minItems=1, maxItems=1): Array of video URLs. Exactly 1 video is required. HTTP, HTTPS, and OSS URLs are supported. Videos must be in MP4 or MOV format; each file must not exceed 200 MB; duration must be between 3 and 15.5 seconds; width and height must e …[truncated, see doc]
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): Video resolution. `720p` outputs a 720p video, `1080p` outputs a 1080p video, and `4k` outputs a 4K video.
    - `aspect_ratio` (string, enum=["auto"], default="auto"): Video aspect ratio. Only `auto` can be used with video-only input.
    - `audio` (boolean, enum=[false,true]): Whether to enable audio.
    - `elements` (array, default=[]): List of one-time subject assets. The default is an empty array. When using only multi-image subjects, up to 7 subjects can be uploaded. When using only video character subjects, the number of video character subjects must not exce …[truncated, see doc]
    - `elements[].name` (string, REQUIRED, minLength=1): Subject name. It must be unique within the same request and can be referenced in the `prompt` field using `@name`.
    - `elements[].description` (string, REQUIRED, minLength=1): Text description of the subject asset.
    - `elements[].element_input_urls` (array, REQUIRED, minItems=1, maxItems=4): List of image URLs for a multi-image subject (provide 2 to 4 images), or a video URL for a video character subject (provide exactly 1 video). Images and videos cannot be mixed. HTTP, HTTPS, and OSS URLs are supported.
    - `elements[].element_input_audio_urls` (array, default=[]): Optional list of subject audio asset URLs. HTTP, HTTPS, and OSS URLs are supported.
  - **oneOf variant 1 (Video with Images):**
    - `prompt` (string, REQUIRED, minLength=1, maxLength=3072)
    - `image_urls` (array, REQUIRED, maxItems=4)
    - `video_urls` (array, REQUIRED, minItems=1, maxItems=1)
    - `duration` (string)
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p")
    - `aspect_ratio` (string, enum=["16:9","9:16","1:1"], default="16:9")
    - `audio` (boolean, enum=[false,true])
    - `elements` (array, default=[])
  - **fields listed outside the variants in the doc schema:**
    - `prompt` (string, minLength=1, maxLength=3072): Video description. It must not be empty after leading and trailing whitespace is removed. Maximum length: 3,072 characters.
    - `video_urls` (array, minItems=1, maxItems=1): Array of video URLs. Exactly 1 video is required. HTTP, HTTPS, and OSS URLs are supported. Videos must be in MP4 or MOV format; each file must not exceed 200 MB; duration must be between 3 and 15.5 seconds; width and height must e …[truncated, see doc]
    - `image_urls` (array, maxItems=4): Array of image URLs. The maximum number of images depends on the number and types of reference subjects. When using only multi-image subjects, the combined number of reference images and multi-image subjects must not exceed 4. Vid …[truncated, see doc]
    - `duration` (string): Video duration. This field may be configured when using a video with images.
    - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): Video resolution. `720p` outputs a 720p video, `1080p` outputs a 1080p video, and `4k` outputs a 4K video.
    - `aspect_ratio` (string, enum=["16:9","9:16","1:1","auto"], default="16:9"): Video aspect ratio. Only `auto` can be used with video-only input. When using a video with images, `16:9`, `9:16`, and `1:1` are supported; `auto` is not supported.
    - `audio` (boolean, enum=[false,true]): Whether to enable audio.
    - `elements` (array, default=[]): List of one-time subject assets. The default is an empty array. When using only multi-image subjects, up to 7 subjects can be uploaded. When using only video character subjects, the number of video character subjects must not exce …[truncated, see doc]
    - `elements[].name` (string, REQUIRED, minLength=1): Subject name. It must be unique within the same request and can be referenced in the `prompt` field using `@name`.
    - `elements[].description` (string, REQUIRED, minLength=1): Text description of the subject asset.
    - `elements[].element_input_urls` (array, REQUIRED, minItems=1, maxItems=4): List of image URLs for a multi-image subject (provide 2 to 4 images), or a video URL for a video character subject (provide exactly 1 video). Images and videos cannot be mixed. HTTP, HTTPS, and OSS URLs are supported.
    - `elements[].element_input_audio_urls` (array, default=[]): Optional list of subject audio asset URLs. HTTP, HTTPS, and OSS URLs are supported.

**Seedance (ByteDance):**

#### `bytedance/seedance-2-5` (Bytedance Seedance 2.5)
- Doc: https://docs.kie.ai/market/bytedance/seedance-2-5
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, maxLength=30000): The text prompt used to generate the video.. ( Max length: 30000 characters)
  - `first_frame_url` (string): First frame image url or asset://{assetId} (for example: asset://asset-20260404242101-76djj) Cannot be used simultaneously with reference_image_urls, reference_video_urls, or reference_audio_urls.
  - `last_frame_url` (string): End frame image url or asset://{assetId} (for example: asset://asset-20260404242101-76djj) last_frame_url cannot be passed alone; first_frame_url must be provided together with it.
  - `reference_image_urls` (array, maxItems=30): Enter a list of image URLs or asset://{assetId} (for example: asset://asset-20260404242101-76djj). Single image requirements: Format: jpeg, png, webp, bmp, tiff, gif. Aspect ratio (width/height): (0.4, 2.5) Width and height (px): (300, 6000) Size: Single image less than 30 MB. Maximum number of files: The sum of the number of frames at the beginning and end must not exceed 30. Mutually exclusive with the first/last-frame scenario;
  - `reference_video_urls` (array, maxItems=10): Enter a list of video URLs or asset://{assetId} (for example: asset://asset-20260404242101-76djj) . Single video requirements: Video format: mp4, mov. Resolution: 480p, 720p Dimensions: Aspect ratio (width/height): [0.4, 2.5] Width/height (px): [300, 6000] Total pixels: [640×640=409600, 834×1112=927408], i.e., the product of width and height must meet the range requirement of [409600, 927408]. Size: Single video not exceeding 200 MB. Frame rate (FPS): [24, 60] Single video duration: [2, 30] seconds; Mutually exclusive with the first/last-frame scenario; Total duration of reference videos must not exceed 30 seconds.
  - `reference_audio_urls` (array, maxItems=10): Enter a list of audio URLs or asset://{assetId} (for example: asset://asset-20260404242101-76djj) . Single audio requirements: Format: wav, mp3 Size: Single audio file size not exceeding 15 MB. Single audio duration: [2, 30] seconds; Mutually exclusive with the first/last-frame scenario; Total duration of reference videos must not exceed 30 seconds.
  - `return_last_frame` (boolean, default=false): Whether to return the last frame of the video. When draft=true, this parameter cannot be set to true.
  - `generate_audio` (boolean, default=true): Whether to generate audio for the video. - **true**: Generate with audio (higher cost) - **false**: Generate without audio Note: Enabling audio will increase the generation cost
  - `resolution` (string, enum=["480p","720p","1080p"], default="720p"): Video resolution - 480p for faster generation, 720p for balance.
  - `aspect_ratio` (string, enum=["1:1","4:3","3:4","16:9","9:16","21:9","adaptive"], default="adaptive"): Video aspect ratio configuration.
  - `duration` (integer, default=5): Video duration in 4-30 seconds. Special values -1: Pass -1 for automatic duration selection — the model picks a suitable duration itself (for video-editing tasks, it matches the input video's length; for other task types, it selects within the valid range), instead of you specifying an exact value.
  - `output_format` (string, enum=["mp4","mov"], default="mp4"): Video output format.
  - `web_search` (boolean): Enable online search.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
"{\n    \"model\": \"bytedance/seedance-2-5\",\n    \"callBackUrl\": \"https://your-domain.com/api/callback\",\n    \"input\": {\n        \"prompt\": \"A serene beach at sunset with waves gently crashing on the shore, palm trees swaying in the breeze, and seagulls flying across the orange sky\",\n        \"reference_ima…"
```

#### `bytedance/seedance-2` (Bytedance Seedance 2.0)
- Doc: https://docs.kie.ai/market/bytedance/seedance-2
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, minLength=3, maxLength=20000): The text prompt used to generate the video. Required field. (Min length: 3, Max length: 20000 characters)
  - `first_frame_url` (string): First frame image url or asset://{assetId} (for example: asset://asset-20260404242101-76djj)
  - `last_frame_url` (string): End frame image url or asset://{assetId} (for example: asset://asset-20260404242101-76djj)
  - `reference_image_urls` (array, maxItems=9): Enter a list of image URLs or asset://{assetId} (for example: asset://asset-20260404242101-76djj). Single image requirements: Format: jpeg, png, webp, bmp, tiff, gif. Aspect ratio (width/height): (0.4, 2.5) Width and height (px): (300, 6000) Size: Single image less than 30 MB. Maximum number of files: The sum of the number of frames at the beginning and end must not exceed 9..
  - `reference_video_urls` (array, maxItems=3): Enter a list of video URLs or asset://{assetId} (for example: asset://asset-20260404242101-76djj) . Single video requirements: Video format: mp4, mov. Resolution: 480p, 720p Duration: Single video duration [2, 15] s, maximum 3 reference videos, total duration of all videos not exceeding 15 seconds. Dimensions: Aspect ratio (width/height): [0.4, 2.5] Width/height (px): [300, 6000] Total pixels: [640×640=409600, 834×1112=927408], i.e., the product of width and height must meet the range requirement of [409600, 927408]. Size: Single video not exceeding 50 MB. Frame rate (FPS): [24, 60]
  - `reference_audio_urls` (array, maxItems=3): Enter a list of audio URLs or asset://{assetId} (for example: asset://asset-20260404242101-76djj) . Single audio requirements: Format: wav, mp3 Duration: Single audio duration [2, 15] s, maximum 3 reference audios, total duration of all audios not exceeding 15 s. Size: Single audio file size not exceeding 15 MB.
  - `return_last_frame` (boolean, default=false): Whether to return the last frame of the video as an image.
  - `generate_audio` (boolean, default=true): Whether to generate audio for the video. - **true**: Generate with audio - **false**: Generate without audio
  - `resolution` (string, enum=["480p","720p","1080p","4k"], default="720p"): Video resolution - 480p for faster generation, 720p for balance, 1080p for High-quality video, 4K Ultra-High Definition, delivering perfect visual details.
  - `aspect_ratio` (string, enum=["1:1","4:3","3:4","16:9","9:16","21:9","adaptive"], default="16:9"): Video aspect ratio configuration. Required field.
  - `duration` (integer, default=5): Video duration in 4-15 seconds or -1.
  - `web_search` (boolean): Use online search
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
{
  "model": "bytedance/seedance-2",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "A serene beach at sunset with waves gently crashing on the shore, palm trees swaying in the breeze, and seagulls flying across the orange sky",
    "first_frame_url": "https://templateb.aiquickdraw.com/custom-page/akr/section-images/example2.png",
    "last_frame_url": "https://templateb.aiquickdraw.com/custom-page/akr/section-images/example3.png",
    "reference_image_urls": [
      "https://templateb.aiquickdraw.com/custom-page/akr/section-images/example1.png"
    ],
    "reference_video_urls": [
      "https://templateb.aiquickdraw.com/custom-page/akr/section-images/example1.mp4"
    ],
    "reference_audio_urls": [
      "https://templateb.aiquickdraw.com/custom-page/akr/section-images/example1.mp3"
    ],
    "return_last_frame": false,
    "generate_audio": false,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "duration": 15,
    "web_search": false
  }
}
```

#### `bytedance/seedance-2-fast` (Bytedance Seedance 2.0 Fast)
- Doc: https://docs.kie.ai/market/bytedance/seedance-2-fast
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `bytedance/seedance-2` except: `resolution` is (string, enum=["480p","720p"], default="720p") instead of (string, enum=["480p","720p","1080p","4k"], default="720p").

#### `bytedance/seedance-2-mini` (Bytedance Seedance 2.0 Mini)
- Doc: https://docs.kie.ai/market/bytedance/seedance-2-mini
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `bytedance/seedance-2` except: `resolution` is (string, enum=["480p","720p"], default="720p") instead of (string, enum=["480p","720p","1080p","4k"], default="720p"); lacks `return_last_frame`.

#### `bytedance/seedance-1.5-pro` (Bytedance Seedance 1.5 Pro)
- Doc: https://docs.kie.ai/market/bytedance/seedance-1-5-pro
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ::: note[]
  > **Audio Generation**: Enabling the `generate_audio` feature will increase the generation cost. Use it when audio is essential for your video content.
  > :::

- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=20000): The text prompt used to generate the video. Required field. (Min length: 3, Max length: 20000 characters)
  - `input_urls` (array, maxItems=2): URLs of input images for image-to-video generation. Optional field. - Accepts 0-2 images - If not provided, the model will perform text-to-video generation - File URLs after upload, not file content - Accepted types: image/jpeg, image/png, image/webp - Max size per image: 10.0MB
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","21:9"], default="1:1"): Video aspect ratio configuration. Required field.
  - `resolution` (string, enum=["480p","720p","1080p"], default="720p"): Video resolution - 480p for faster generation, 720p for balance, 1080p for higher quality
  - `duration` (number, REQUIRED): Duration of the video in seconds,Optional range 4-12 s
  - `fixed_lens` (boolean, default=false): Seedance adds dynamic camera movement. Enable this feature to lock the camera for stable, static shots. - **true**: Lock camera for static shots - **false**: Allow dynamic camera movement
  - `generate_audio` (boolean, default=false): Whether to generate audio for the video. - **true**: Generate with audio (higher cost) - **false**: Generate without audio Note: Enabling audio will increase the generation cost
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
{
  "model": "bytedance/seedance-1.5-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "A serene beach at sunset with waves gently crashing on the shore, palm trees swaying in the breeze, and seagulls flying across the orange sky",
    "input_urls": [
      "https://file.aiquickdraw.com/custom-page/akr/section-images/example1.png"
    ],
    "aspect_ratio": "1:1",
    "resolution": "720p",
    "duration": 8,
    "fixed_lens": false,
    "generate_audio": false,
    "nsfw_checker": false
  }
}
```

**Wan (Alibaba):**

#### `wan/3-0-video` (Wan 3.0 - Video)
- Doc: https://docs.kie.ai/market/wan/3-0-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > Generate video through Wan 3.0. The standard model uses the parameter "model=wan/3-0-video".

- Params:
  - `prompt` (string, maxLength=20000): Text prompt, supporting both Chinese and English. Up to 20,000 characters; excess characters will be truncated automatically. Required for text-to-video generation; for other modes, it is recommended to provide it together with media. In reference mode, use Image1/Video1/Audio1 to reference the provided media.
  - `first_frame_url` (object): URL of the first-frame image. Up to 1 image, used strictly as the first frame of the video. Used for first-frame-to-video / first-and-last-frame-to-video generation. Cannot be provided together with `reference_*_urls`. Formats: JPEG/JPG, PNG (transparency not supported), BMP, WEBP; each side [240, 8000] px; aspect ratio ≤ 8:1; ≤ 20MB.
  - `last_frame_url` (object): URL of the first-frame image. Up to 1 image, used strictly as the first frame of the video. Used for first-frame-to-video / first-and-last-frame-to-video generation. Cannot be provided together with `reference_*_urls`. Formats: JPEG/JPG, PNG (transparency not supported), BMP, WEBP; each side [240, 8000] px; aspect ratio ≤ 8:1; ≤ 20MB.
  - `reference_image_urls` (array, maxItems=10): Reference images for the all-purpose reference mode, with up to 10 images. Correspond to Image1, Image2, … in the prompt according to array order. Specifications are the same as `first_frame_url`. Cannot be provided together with the first-frame/last-frame parameters.
  - `reference_image_urls[]` (object): URL of the first-frame image. Up to 1 image, used strictly as the first frame of the video. Used for first-frame-to-video / first-and-last-frame-to-video generation. Cannot be provided together with `reference_*_urls`. Formats: JPEG/JPG, PNG (transparency not supported), BMP, WEBP; each side [240, 8000] px; aspect ratio ≤ 8:1; ≤ 20MB.
  - `reference_video_urls` (array, maxItems=5): Reference videos for the all-purpose reference mode, with up to 5 clips. Each clip must be 1–15 seconds, with a total duration ≤ 15 seconds. Correspond to Video1, Video2, … according to array order. Formats: mp4, mov; each side [240, 4096] px; aspect ratio ≤ 8:1; each file ≤ 100MB. There is an additional constraint on the output side: the input video duration + `duration` must not exceed 30 seconds.
  - `reference_video_urls[]` (object): URL of the first-frame image. Up to 1 image, used strictly as the first frame of the video. Used for first-frame-to-video / first-and-last-frame-to-video generation. Cannot be provided together with `reference_*_urls`. Formats: JPEG/JPG, PNG (transparency not supported), BMP, WEBP; each side [240, 8000] px; aspect ratio ≤ 8:1; ≤ 20MB.
  - `reference_audio_urls` (array, maxItems=5): Reference audio for the all-purpose reference mode, with up to 5 clips. Each clip must be 1–15 seconds, with a total duration ≤ 15 seconds. Correspond to Audio1, Audio2, … according to array order. Formats: wav, mp3; ≤ 15MB. Audio should not be used alone as the only media input; pairing it with an image or video is still recommended.
  - `reference_audio_urls[]` (object): URL of the first-frame image. Up to 1 image, used strictly as the first frame of the video. Used for first-frame-to-video / first-and-last-frame-to-video generation. Cannot be provided together with `reference_*_urls`. Formats: JPEG/JPG, PNG (transparency not supported), BMP, WEBP; each side [240, 8000] px; aspect ratio ≤ 8:1; ≤ 20MB.
  - `reference_file_urls` (array, maxItems=1): File-to-video generation. Up to 1 file. Cannot be provided together with `reference_link_urls`, or with the first-frame/last-frame parameters. Formats: docx/doc/xlsx/xls/pptx/ppt/pdf/txt/key/pages/numbers/md; ≤ 100MB; pdf/docx/ppt/key/pages, etc. ≤ 50 pages.
  - `reference_file_urls[]` (object): URL of the first-frame image. Up to 1 image, used strictly as the first frame of the video. Used for first-frame-to-video / first-and-last-frame-to-video generation. Cannot be provided together with `reference_*_urls`. Formats: JPEG/JPG, PNG (transparency not supported), BMP, WEBP; each side [240, 8000] px; aspect ratio ≤ 8:1; ≤ 20MB.
  - `reference_link_urls` (array, maxItems=1): Link-to-video generation. Up to 1 publicly accessible webpage that does not require login. Cannot be provided together with `reference_file_urls`, or with the first-frame/last-frame parameters.
  - `reference_link_urls[]` (object): URL of the first-frame image. Up to 1 image, used strictly as the first frame of the video. Used for first-frame-to-video / first-and-last-frame-to-video generation. Cannot be provided together with `reference_*_urls`. Formats: JPEG/JPG, PNG (transparency not supported), BMP, WEBP; each side [240, 8000] px; aspect ratio ≤ 8:1; ≤ 20MB.
  - `resolution` (string, enum=["480P","720P","1080P"], default="1080P"): Output resolution. Default: **1080P**.
  - `aspect_ratio` (string, enum=["adaptive","16:9","4:3","1:1","3:4","9:16"], default="adaptive"): Output aspect ratio. `adaptive` (default) automatically selects the ratio based on the input media and intent.
  - `duration` (integer, default=5): Output video duration in seconds. Default: 5. Without video input, the range is [2, 30]. With reference videos: input video duration + output duration ≤ 30. Pass `-1` to use an intelligent duration determined by the model.
  - `audio` (boolean, default=true): Whether the output video includes an audio track. Default: true.
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed used to reproduce results. If omitted, a random seed will be used.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc [[1] Text to Video]:

```json
{
  "model": "wan/3-0-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Under the moonlight, a little cat is running on the roof. In the distance, the neon lights are flashing, giving a cinematic feel. The camera movement is smooth.",
    "resolution": "480P",
    "aspect_ratio": "adaptive",
    "duration": 5,
    "audio": true
  }
}
```
- Request example from the doc [[2] First frame to Video]:

```json
{
  "model": "wan/3-0-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "The graffiti teenager emerged from the concrete wall, rapping under the night-time railway bridge, with a cinematic atmosphere.",
    "first_frame_url": "https://example.com/first-frame.png",
    "resolution": "720P",
    "aspect_ratio": "adaptive",
    "duration": 5,
    "audio": true
  }
}
```

#### `wan/3-0-video-prime` (Wan 3.0 - Video Prime)
- Doc: https://docs.kie.ai/market/wan/3-0-video-prime
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `wan/3-0-video` (no field differences in the docs).

#### `wan/2-7-videoedit` (Wan 2.7 - Video Edit)
- Doc: https://docs.kie.ai/market/wan/2-7-videoedit
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, maxLength=5000): Optional text prompt describing the expected elements and visual features in the generated video. Supports Chinese and English. Maximum length: 5000 characters.
  - `negative_prompt` (string, maxLength=500): Optional negative prompt describing content that should not appear in the video. Supports Chinese and English. Maximum length: 500 characters.
  - `video_url` (string, REQUIRED, format=uri): URL of the source video to edit. Required. Only one video is supported. - Formats: `mp4`, `mov` - Duration: `2` to `10` seconds - Resolution: width and height range `[240,4096]` pixels - Aspect ratio: `1:8` to `8:1` - File size: up to `100M …[truncated, see doc]
  - `reference_image` (string, format=uri): Optional reference image URL for character, clothing, or style guidance. - Formats: `JPEG`, `JPG`, `PNG` (no alpha channel), `BMP`, `WEBP` - Resolution: width and height range `[240,8000]` pixels - Aspect ratio: `1:8` to `8:1` - Supports pu …[truncated, see doc]
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Output video resolution tier. `1080p` costs more than `720p`. Default value: `1080p`. - `720p`: 720p - `1080p`: 1080p
  - `aspect_ratio` (string, enum=["16:9","9:16","1:1","4:3","3:4"]): Output video aspect ratio. - If omitted: the output uses an aspect ratio close to the input video - If provided: the output uses the specified aspect ratio - Available values: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`
  - `duration` (integer, default=0, minimum=0, maximum=10): Output video duration in seconds. - Default `0` means using the full input video duration without truncation - If a value is provided, the output is clipped from second `0` to the specified length - Valid values are `0` or any integer in `[ …[truncated, see doc]
  - `audio_setting` (string, enum=["auto","origin"], default="auto"): Video audio setting. - `auto`: default, the model decides whether to regenerate audio based on the `prompt` - `origin`: force keeping the original input video audio
  - `prompt_extend` (boolean, default=true): Whether to enable prompt rewriting. When enabled, the model expands the input prompt. This usually works better for short prompts but increases processing time.
  - `watermark` (boolean, default=false): Whether to add a watermark. The watermark is placed in the lower-right corner of the video with the fixed text "AI generated".
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed. Range: `0-2147483647`. If omitted, the system generates one automatically.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filte …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "wan/2-7-videoedit",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Change the character's outfit and add the hat shown in the reference image.",
    "negative_prompt": "low resolution, errors, worst quality, low quality, malformed, extra fingers, bad proportions",
    "video_url": "https://example.com/demo/video.mp4",
    "reference_image": "https://example.com/demo/reference.png",
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "duration": 0,
    "audio_setting": "auto",
    "prompt_extend": true,
    "watermark": false,
    "seed": 0
  }
}
```

#### `wan/2-6-text-to-video` (Wan 2.6 - Text to Video)
- Doc: https://docs.kie.ai/market/wan/2-6-text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Text prompts for video generation. Supports both Chinese and English, with a minimum of 1 characters and a maximum of 5,000 characters. (Max length: 5000 characters)
  - `duration` (string, enum=["5","10","15"], default="5"): The duration of the generated video in seconds
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Video resolution tier
  - `multi_shots` (boolean, default=false): The multi shots parameter controls the shot composition style during AI video generation, determining whether the generated video is a single continuous shot or multiple shots with transitions.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filte …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "wan/2-6-text-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "In a hyperrealistic ASMR video, a hand uses a knitted knife to slowly slice a burger made entirely of knitted wool. The …",
    "duration": "5",
    "resolution": "1080p",
    "multi_shots": false,
    "nsfw_checker": false
  }
}
```

#### `wan/2-6-image-to-video` (Wan 2.6 - Image to Video)
- Doc: https://docs.kie.ai/market/wan/2-6-image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Text prompts for video generation. Supports both Chinese and English, with a minimum of 2 characters and a maximum of 5,000 characters. (Max length: 5000 characters)
  - `image_urls` (array, REQUIRED, maxItems=1): Upload an image file to use as input for the API (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB),All images must be at least 256x256px.
  - `duration` (string, enum=["5","10","15"], default="5"): The duration of the generated video in seconds
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Video resolution tier
  - `multi_shots` (boolean, default=false): The multi shots parameter controls the shot composition style during AI video generation, determining whether the generated video is a single continuous shot or multiple shots with transitions.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filte …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "wan/2-6-image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Anthopmopric fox singing a Christmas song at the rubbish dump in the rain.",
    "image_urls": [
      "https://static.aiquickdraw.com/tools/example/1765957673717_awiBAidD.webp"
    ],
    "duration": "5",
    "resolution": "1080p",
    "multi_shots": false,
    "nsfw_checker": false
  }
}
```

#### `wan/2-6-video-to-video` (Wan 2.6 - Video to Video)
- Doc: https://docs.kie.ai/market/wan/2-6-video-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Text prompts for video generation. Supports both Chinese and English, with a minimum of 2 characters and a maximum of 5,000 characters. (Max length: 5000 characters)
  - `video_urls` (array, REQUIRED, maxItems=3): The URL of the image used to generate video (File URL after upload, not file content; Accepted types: video/mp4, video/quicktime, video/x-matroska; Max size: 10.0MB)
  - `duration` (string, enum=["5","10"], default="5"): The duration of the generated video in seconds
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Video resolution tier
  - `multi_shots` (boolean, default=false): The multi shots parameter controls the shot composition style during AI video generation, determining whether the generated video is a single continuous shot or multiple shots with transitions.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filte …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "wan/2-6-video-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "The video drinks milk tea while doing some improvised dance moves to the music.",
    "video_urls": [
      "https://static.aiquickdraw.com/tools/example/1765957777782_cNJpvhRx.mp4"
    ],
    "duration": "5",
    "resolution": "1080p",
    "multi_shots": false,
    "nsfw_checker": false
  }
}
```

#### `wan/2-5-text-to-video` (Wan 2.5 - Text to Video)
- Doc: https://docs.kie.ai/market/wan/2-5-text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=800): The text prompt for video generation. Supports Chinese and English. Maximum length: 800 characters.
  - `duration` (string, REQUIRED, enum=["5","10"]): The duration of the generated video in seconds. - `5`: 5 seconds - `10`: 10 seconds
  - `aspect_ratio` (string, enum=["16:9","9:16","1:1"]): The aspect ratio of the generated video. - `16:9`: Landscape - `9:16`: Portrait - `1:1`: Square
  - `resolution` (string, enum=["720p","1080p"]): Video resolution tier. - `720p`: 720p - `1080p`: 1080p
  - `negative_prompt` (string, maxLength=500): Negative prompt used to describe content to avoid. Maximum length: 500 characters.
  - `enable_prompt_expansion` (boolean): Whether to enable prompt rewriting using LLM. Improves results for short prompts but increases processing time. - Boolean value: `true` / `false`
  - `seed` (integer): Random seed for reproducibility. If omitted, a random seed is chosen.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filte …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "wan/2-5-text-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "A dimly lit jazz bar at night, wooden tables glowing under warm pendant lights. Patrons sip drinks and chat quietly whil…",
    "duration": "5",
    "aspect_ratio": "16:9",
    "resolution": "1080p",
    "negative_prompt": "blurry, flicker, low quality, distorted people, camera shake",
    "enable_prompt_expansion": true,
    "seed": 123456,
    "nsfw_checker": false
  }
}
```

#### `wan/2-5-image-to-video` (Wan 2.5 - Image to Video)
- Doc: https://docs.kie.ai/market/wan/2-5-image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=800): The text prompt describing the desired video motion. Maximum length: 800 characters.
  - `image_url` (string, REQUIRED, format=uri): URL of the image to use as the first frame. Must be publicly accessible. - Please provide the URL of the uploaded file, not raw file content - Accepted types: `image/jpeg`, `image/png`, `image/webp` - Max size: 10.0MB
  - `duration` (string, REQUIRED, enum=["5","10"]): The duration of the generated video in seconds. - `5`: 5 seconds - `10`: 10 seconds
  - `resolution` (string, enum=["720p","1080p"]): Video resolution. Valid values: `720p`, `1080p`.
  - `negative_prompt` (string, maxLength=500): Negative prompt used to describe content to avoid. Maximum length: 500 characters.
  - `enable_prompt_expansion` (boolean): Whether to enable prompt rewriting using LLM. - Boolean value: `true` / `false`
  - `seed` (integer): Random seed for reproducibility. If omitted, a random seed is chosen.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filte …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "wan/2-5-image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "The same woman from the reference image looks directly into the camera, takes a breath, then smiles brightly and speaks …",
    "image_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1758796480945qb63zxq8.webp",
    "duration": "5",
    "resolution": "1080p",
    "negative_prompt": "blurry, flicker, camera shake, distorted face, low quality",
    "enable_prompt_expansion": true,
    "seed": 123456,
    "nsfw_checker": false
  }
}
```

**Grok Imagine:**

#### `grok-imagine/text-to-video` (Grok Imagine Text to Video)
- Doc: https://docs.kie.ai/market/grok-imagine/text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED): Text prompt describing the desired video motion. Required field. - Should be detailed and specific about the desired visual motion - Describe movement, action sequences, camera work, and timing - Include details about subjects, environments, and motion dynamic …[truncated, see doc]
  - `aspect_ratio` (string, enum=["2:3","3:2","1:1","16:9","9:16"], default="2:3"): Specifies the width-to-height ratio of the generated video. Controls the aspect ratio of the output. - **2:3**: Portrait orientation (vertical) - **3:2**: Landscape orientation (horizontal) - **1:1**: Square format - **16:9**: Wide screen format - **9:16**: Ta …[truncated, see doc]
  - `mode` (string, enum=["fun","normal","spicy"], default="normal"): Specifies the generation mode affecting the style and intensity of motion. - **fun**: More creative and playful interpretation - **normal**: Balanced approach with good motion quality - **spicy**: More dynamic and intense motion effects Default: normal
  - `duration` (number): The duration of the generated video (in seconds) (6-30). (Minimum: 6, Maximum: 30, Step: 1)
  - `resolution` (string, enum=["480p","720p","1080p"], default="480p"): The resolution of the generated video.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "grok-imagine/text-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "A couple of doors open to the right one by one randomly and stay open, to show the inside, each is either a living room,…",
    "aspect_ratio": "2:3",
    "mode": "normal",
    "duration": "6",
    "resolution": "480p"
  }
}
```

#### `grok-imagine/image-to-video` (Grok Imagine Image to Video)
- Doc: https://docs.kie.ai/market/grok-imagine/image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `image_urls` (array, maxItems=7): Provide an external image URL as a reference for video generation. Up to 7 images are supported. Do not use it simultaneously with task_id. In your prompt, reference an uploaded image by typing @image(n) followed by a space (for example: @image1 a sunset over …[truncated, see doc]
  - `task_id` (string, maxLength=100): Task ID from a previously generated Grok image. Use with index to select a specific image. Do not use with image_urls. - Use task ID from grok-imagine/text-to-image generations - Supports all modes including Spicy - Maximum length: 100 characters
  - `index` (integer, default=0, minimum=0, maximum=5): When using task_id, specify which image to use (Grok generates 6 images per task). Only works with task_id. - 0-based index (0-5) - Ignored if image_urls is provided - Default: 0
  - `prompt` (string): Text prompt describing the desired video motion. Optional field. - Should be detailed and specific about the desired visual motion - Describe movement, action sequences, camera work, and timing - Include details about subjects, environments, and motion dynamic …[truncated, see doc]
  - `mode` (string, enum=["fun","normal","spicy"], default="normal"): Specifies the generation mode affecting the style and intensity of motion. Note: Spicy mode is not available for external image inputs. - **fun**: More creative and playful interpretation - **normal**: Balanced approach with good motion quality - **spicy**: Mo …[truncated, see doc]
  - `duration` (string): The duration of the generated video (in seconds) (6-30). (Minimum: 6, Maximum: 30, Step: 1)
  - `resolution` (string, enum=["480p","720p","1080p"], default="480p"): The resolution of the generated video.
  - `aspect_ratio` (string, enum=["2:3","3:2","1:1","16:9","9:16"], default="16:9"): Image ratio selection only applies to multi-image generation mode. In single-image mode, the video width and height are referenced to the image width and height.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "grok-imagine/image-to-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "task_id": "task_grok_12345678",
    "image_urls": [
      "https://file.aiquickdraw.com/custom-page/akr/section-images/1762247692373tw5di116.png"
    ],
    "prompt": "POV hand comes into frame handing the girl a cup of take away coffee, the girl steps out of the screen looking tired, th…",
    "mode": "normal",
    "duration": "6",
    "resolution": "480p",
    "aspect_ratio": "16:9"
  }
}
```

#### `grok-imagine-video-1-5-preview` (Grok Imagine Video 1.5 Preview)
- Doc: https://docs.kie.ai/market/grok-imagine/1-5-preview
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, maxLength=4096): Prompt for video generation. Maximum length: 4096 characters.
  - `image_urls` (array, maxItems=7): Upload image files to be used as API input. Supported file types: image/jpeg, image/png, image/webp, image/jpg. Maximum file size: 20MB. Supports multi-file upload, up to 7 file.Only one is supported when the resolution is 1080p.
  - `aspect_ratio` (string, enum=["1:1","16:9","9:16","3:2","2:3","auto"], default="auto"): The aspect ratio of the video. This parameter is invalid if it is a single image.
  - `resolution` (string, enum=["480p","720p","1080p"], default="480p"): Resolution for video generation.
  - `duration` (integer, default=8, minimum=1, maximum=15): Video duration in seconds. Range: [1, 15]. Default: 8. Minimum: 1. Maximum: 15. Step: 1.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are …[truncated, see doc]
- Request example from the doc [[default] Example request]:

```json
{
  "model": "grok-imagine-video-1-5-preview",
  "input": {
    "prompt": "Describe the scene you want to generate.",
    "image_urls": [
      "https://your-domain.com/image/example.png"
    ],
    "aspect_ratio": "16:9",
    "resolution": "480p",
    "duration": 8
  },
  "callBackUrl": "https://your-domain.com/api/callback"
}
```

#### `grok-imagine/extend` (Grok Imagine - Video Extend)
- Doc: https://docs.kie.ai/market/grok-imagine/extend
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `task_id` (string, REQUIRED, maxLength=100): Task ID from a previously successful video generation task. Required field. - Must be from a Kie AI video generation model (e.g., grok-imagine/text-to-video) - The original video generation must have completed successfully - Only Kie AI–generated task IDs are …[truncated, see doc]
  - `prompt` (string, REQUIRED): Text instructions describing the required movement of the video. Required field. - Provide a detailed description of how you would like the video to expand and continue. - You can specify camera movements, scene changes, object actions, etc. - The more specifi …[truncated, see doc]
  - `extend_at` (number, REQUIRED, default=2, minimum=2): The starting position of the video extension. Optional field.
  - `extend_times` (number, REQUIRED): Duration of video extension (in seconds). Required field. - `6`: Expand 6 seconds of video content - `10`: Expand 10 seconds of video content - The longer the extension duration, the longer the time required for generation - Select the appropriate duration bas …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "grok-imagine/extend",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "task_id": "task_grok_12345678",
    "prompt": "",
    "extend_at": 2,
    "extend_times": "6"
  }
}
```

#### `grok-imagine/upscale` (Grok Imagine - Video Upscale)
- Doc: https://docs.kie.ai/market/grok-imagine/upscale
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `task_id` (string, REQUIRED, maxLength=100): Task ID from a previously successful video generation task. Required field. - Must be from a Kie AI video generation model (e.g., grok-imagine/text-to-video) - The original video generation must have completed successfully - Only Kie AI–generated task IDs are …[truncated, see doc]
  - `resolution` (string, enum=["720p","1080p"], default="720p"): Video generation resolution.
- Request example from the doc:

```json
{
  "model": "grok-imagine/upscale",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "task_id": "task_grok_12345678"
  }
}
```

**Gemini Omni (Google):**

#### `google/gemini-omni-flash-1-1` (Gemini Omni 1.1 Flash)
- Doc: https://docs.kie.ai/market/google/gemini-omni-flash-1-1
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## Create Task
  > 
  > Use this endpoint to create a new multimodal video generation task.
  > 
  > **Total Quota Overview:**
  > The system utilizes a quota-based system for content uploads. The total available capacity is **7 units**. Different parameters consume different amounts of this quota. Please ensure the sum of all consumed units does not exceed 7.
  > 
  > **Quota Consumption Rules:**
  > 1.  **Images (`image_urls`)**: Each image consumes **1 unit**.
  > 2.  **Videos (`video_list`)**: Each video consumes **2 units**.
  >     *   *Note: Maximum of 1 video per request.*
  > 3.  **Character IDs (`character_ids`)**: Each ID consumes **1 unit**.
  >     *   *Note: Maximum of 3 character IDs per request.*
  > 
  > **Constraint Formula:**
  > `(Number of Images) + (Number of Videos × 2) + (Number of Character IDs) ≤ 7`
  > 
  > **Example Scenarios:**
  > *   If 1 video (2 units) and 3 Character IDs (3 units) are uploaded, you can upload a maximum of 2 additional images.
  > *   If no video or Character IDs are provided, you can upload up to 7 images.
  > 
  > ** Special Attention (First frame limit prompt) : **
  > When you upload the first frame image (' first_frame_url 'is not empty) to specify the starting image, to avoid material conflicts,
  > The parameters' image_urls' (images), 'video_list' (videos), 'character_ids' (character ids), and' audio_ids' (audio) will not be passable.
  > If you need to mix and use multimodal materials, please do not upload the first frame of the image.

- Params:
  - `prompt` (string, REQUIRED, maxLength=20000): The video prompt, used to describe the visual content, style, cinematography, or character actions of the target video.
  - `image_urls` (array): An array of image URLs. Multiple reference images can be uploaded to provide references for characters, scenes, styles, or storyboards. Image limitations: - Each file must not exceed `20MB` - Use publicly accessible image URLs - Maximum of 7 images - Note: This field is mutually exclusive with the first-frame image (`first_frame_url`) and cannot be provided at the same time.
  - `first_frame_url` (string, format=uri): The URL of the first-frame image. Used to specify the starting frame of the generated video. Note: This field is mutually exclusive with `image_urls`, `audio_ids`, `video_list`, and `character_ids` and cannot be provided at the same time.
  - `last_frame_url` (string, format=uri): The URL of the last-frame image. Used to specify the ending frame of the generated video. Note: The last-frame image cannot be used alone and must be provided together with the first-frame image (`first_frame_url`).
  - `audio_ids` (array): An array of audio IDs generated by the `gemini-omni-audio` interface. Used to provide narration, dialogue, background music, or sound references for the video. Up to 3 items. Note: This field is mutually exclusive with the first-frame image (`first_frame_url`) and cannot be provided at the same time.
  - `video_list` (array): An array of video clips. Each element describes a video asset that can be used for generation and its trimming time range. Video limitations: - Each file must not exceed `100MB` - Video duration must not exceed `30s` - `ends` should be greater than `start` - The difference between the end and start times must not exceed `10s` - Maximum of 1 item, occupying two image slots - Note: This field is mutually exclusive with the first-frame image (`first_frame_url`) and cannot be provided at the same time.
  - `video_list[].url` (string, REQUIRED, format=uri): The video URL. Each video file must not exceed `100MB`, and the video duration must not exceed `30s`.
  - `video_list[].start` (number, REQUIRED, minimum=0): The start time, in seconds.
  - `video_list[].ends` (number, REQUIRED, minimum=0): The end time, in seconds. It should be greater than `start`. The difference between the end and start times must not exceed 10 seconds.
  - `character_ids` (array): An array of character IDs generated by the `gemini-omni-character` interface. Used to provide character appearance, identity, or person references for the video. Each character_id occupies 1 image slot; the basic maximum is 7. If `video_list` is provided at the same time, `video_list` occupies 2 image slots, and a maximum of 3 character_ids can be provided. Note: This field is mutually exclusive with the first-frame image (`first_frame_url`) and cannot be provided at the same time.If the incoming character_id is a …[truncated, see doc]
  - `duration` (string, REQUIRED, enum=["4","6","8","10"]): The duration of the generated video, in seconds. Valid values are 4, 6, 8, and 10. This parameter only takes effect when there is no video input. If video input is used, the output duration is determined by the model, and the `duration` parameter will be ignored. Note: When video input is provided, the output duration is automatically determined by the model. In this case, the `duration` parameter will not take effect.
  - `aspect_ratio` (string, enum=["16:9","9:16"]): The aspect ratio of the generated video. `16:9` is landscape, and `9:16` is portrait.
  - `seed` (integer): The random seed. Valid range: [0, 2147483647]. If not specified, the system will automatically generate a seed. A fixed seed can improve result reproducibility, but because the model itself is stochastic, results may still vary.
  - `resolution` (string, enum=["360p","720p","1080p","4k"], default="720p"): The resolution of the generated video. Valid values are 360p, 720p, 1080p, and 4k.
- Request example from the doc:

```json
{
  "model": "google/gemini-omni-flash-1-1",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Create a futuristic night city short film with a slow push-in shot as the character walks out from a neon-lit street.",
    "image_urls": [
      "https://example.com/assets/scene-1.png",
      "https://example.com/assets/scene-2.png"
    ],
    "audio_ids": [
      "audio_01hx8p0demo"
    ],
    "video_list": [
      {
        "url": "https://example.com/assets/source-video.mp4",
        "start": 0,
        "ends": 10
      }
    ],
    "duration": "4"
  }
}
```

#### `gemini-omni-video` (Gemini Omni Video)
- Doc: https://docs.kie.ai/market/gemini-omni-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=20000): Video prompt used to describe the target content, style, camera language, or character actions in the generated video.
  - `image_urls` (array): Array of image URLs. You can provide one or more reference images for characters, scenes, styles, or storyboard guidance. Image limits: - Each file must be no larger than `20MB` - Use publicly accessible image URLs - Max 7 images
  - `audio_ids` (array): Array of audio IDs generated by the `gemini-omni-audio` endpoint. Useful for narration, dialogue, music, or audio guidance in the generated video. Max 3 items.
  - `video_list` (array): Array of video clips. Each item defines a source video and the trim range to use during generation. Video limits: - Each file must be no larger than `100MB` - Video duration must not exceed `30s` - `ends` should be greater than `start` - The difference between the end time and the start time must not exceed `10s`. - Max 1 items. Equal 2 images
  - `video_list[].url` (string, REQUIRED, format=uri): Video URL. Each source video file must be no larger than `100MB` and no longer than `30s`.
  - `video_list[].start` (number, REQUIRED, minimum=0): Start time in seconds.
  - `video_list[].ends` (number, REQUIRED, minimum=0): End time in seconds. It should be greater than `start`.The difference between the end time and the start time must not exceed 10s
  - `character_ids` (array): An array of character IDs generated by the `gemini-omni-character` API. Used to provide character appearance, identity, or person references for the video. Each character_id uses 1 image slot. The base limit is 7 image slots; if video_list is also provided, video_list uses 2 image slots, so character_ids can contain up to 3 IDs. If the incoming character_id is a dual-image set [portrait + body], it will occupy two sl …[truncated, see doc]
  - `duration` (string, REQUIRED, enum=["4","6","8","10"]): The duration of the generated video in seconds. Available values are 4, 6, 8, and 10. When video input is provided, the output duration is determined by the model automatically. This duration parameter will not take effect.Note: when video input is provided, the output duration is determined by the model automatically. This duration parameter will not take effect.
  - `aspect_ratio` (string, enum=["16:9","9:16"]): The aspect ratio of the generated video. `16:9` is landscape, and `9:16` is portrait.
  - `seed` (integer): Random seed. Range: [0, 2147483647]. If not specified, the system generates a seed automatically. Fixing the seed can improve reproducibility, but results may still vary due to the model’s stochasticity.
  - `resolution` (string, enum=["720p","1080p","4k"], default="720p"): The resolution of the generated video. Available values are 720p, 1080p, and 4k.
- Request example from the doc:

```json
{
  "model": "gemini-omni-video",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Create a futuristic night city short film with a slow push-in shot as the character walks out from a neon-lit street.",
    "image_urls": [
      "https://example.com/assets/scene-1.png",
      "https://example.com/assets/scene-2.png"
    ],
    "audio_ids": [
      "audio_01hx8p0demo"
    ],
    "video_list": [
      {
        "url": "https://example.com/assets/source-video.mp4",
        "start": 0,
        "ends": 10
      }
    ],
    "duration": "4"
  }
}
```

#### Gemini Omni Audio
- Doc: https://docs.kie.ai/market/gemini-omni-audio
- Endpoint: `POST https://api.kie.ai/api/v1/omni/audio/create`
- Params:
  - `audio_id` (string, REQUIRED): Enum voice ID, used to select a preset voice character. achernar - female, soft, high pitch achird - male, friendly, mid pitch algenib - male, raspy, low pitch algieba - male, easygoing, mid-low pitch alnilam - male, steady, mid-low pitch aoede - female, brisk, mid pitch autonoe - female, bright, mid pitch callirrhoe - female, easygoing, mid pitch charon - male, intellectual, low pitch despina - female, smooth, mid p …[truncated, see doc]
  - `name` (string, REQUIRED): Voice name. Maximum length: `210` characters.
  - `voice_description` (string): Voice characteristic description used to define timbre, style, speaking rate, emotion, and other traits. Maximum length: `20000` characters.
  - `example_dialogue` (string): Example dialogue, such as "Hello, I am Adam". Maximum length: `120` characters.
- Request example from the doc:

```json
{
  "audio_id": "achernar",
  "name": "achernar Narrator",
  "voice_description": "A calm, clear, and friendly male voice suitable for tech explainers and daily conversation.",
  "example_dialogue": "Hello, I am achernar"
}
```
- 200 response example: `{"code":0,"msg":"success","data":{"kieAudioId":"a8f1c2d3e4f5...","name":"gentle female voice"}}`

#### Gemini Omni Character
- Doc: https://docs.kie.ai/market/gemini-omni-character
- Endpoint: `POST https://api.kie.ai/api/v1/omni/character/create`
- Params:
  - `descriptions` (string, REQUIRED): Character description used to define the appearance, identity, style, clothing, or personality of the character.
  - `image_urls` (array, REQUIRED, minItems=1, maxItems=2): Array of character reference image URLs. Up to 2 images are supported. Index 0 is the portrait image, and index 1 is the body image. The body image is optional, but if provided, the portrait image must be present at index 0. Image limits: - Each image must be no larger than `20MB` - Use a publicly accessible image URL
  - `audio_ids` (array): Array of audio IDs generated by the `gemini-omni-audio` endpoint. These can be used to provide voice traits, tone, or persona guidance for the character.
  - `character_name` (string): Character name
- Request example from the doc:

```json
{
  "description": "A young female character with short silver hair and a futuristic utility jacket, calm, agile, and strongly cyberpunk in style.",
  "image_urls": [
    "https://example.com/assets/character-reference.png"
  ],
  "audio_ids": [
    "audio_01hx8p0demo"
  ],
  "character_name": "Jenny"
}
```
- 200 response example: `{"code":200,"msg":"success","data":{"characterId":"b09dbf56...","characterName":"cute character","imageUrl":"https://xx.com/profile.png","bodyImageUrl":"https://xx.com/body.png"}}`

**MiniMax H3 / Hailuo:**

#### `minimax-h3/text-to-video` (MiniMax H3 Text-to-Video)
- Doc: https://docs.kie.ai/market/minimax-h3/text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=1, maxLength=7000): Video generation prompt, length is between 1 and 7000 characters.
  - `aspect_ratio` (string, REQUIRED, enum=["21:9","16:9","4:3","1:1","3:4","9:16"]): Video aspect ratio. Required for text-to-video, adaptive is not supported.
  - `duration` (integer, REQUIRED, enum=[4,5,6,7,8,9,10,11,12,13,14,15], default=6, minimum=4, maximum=15): Generated video duration, supports integer values from 4 to 15 seconds.
  - `resolution` (string, enum=["768P","2K"], default="2K"): Video resolution.

#### `minimax-h3/image-to-video` (MiniMax H3 Image-to-Video)
- Doc: https://docs.kie.ai/market/minimax-h3/image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=1, maxLength=7000): Video generation prompt, length is between 1 and 7000 characters.
  - `first_frame_url` (string, format=uri): First frame image URL. Note: Either first_frame_url or last_frame_url must be provided. Supports HTTP, HTTPS, and OSS addresses; supports JPG, JPEG, PNG, WEBP, HEIC, HEIF formats; single image size not exceeding 30 MB, image side length between 256 and 5760 pixels, aspect ratio between 0.4 and 2.5.
  - `last_frame_url` (string, format=uri): Last frame image URL. Note: Either first_frame_url or last_frame_url must be provided. Image restrictions are the same as first_frame_url.
  - `duration` (integer, REQUIRED, enum=[4,5,6,7,8,9,10,11,12,13,14,15], default=6, minimum=4, maximum=15): Generated video duration, supporting integer values from 4 to 15 seconds.
  - `resolution` (string, enum=["768P","2K"], default="2K"): Video resolution.

#### `minimax-h3/reference-to-video` (MiniMax H3 Reference-to-Video)
- Doc: https://docs.kie.ai/market/minimax-h3/reference-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - **anyOf variant 0:**
    - `reference_image_urls` (string, REQUIRED)
  - **anyOf variant 1:**
    - `reference_video_urls` (string, REQUIRED)
  - **fields listed outside the variants in the doc schema:**
    - `prompt` (string, REQUIRED, minLength=1, maxLength=7000): Video generation prompt, length is between 1 and 7000 characters.
    - `reference_image_urls` (array, maxItems=9): Array of reference image URLs. Supports up to 9 images. Supports HTTP, HTTPS, and OSS addresses; supported image formats include JPG, JPEG, PNG, WEBP, HEIC, and HEIF; a single image size cannot exceed 30 MB; the side length of the image must be between 256 and 5760 pixels, and the aspect ratio must be between 0.4 and 2.5.
    - `reference_video_urls` (array, maxItems=3): Array of reference video URLs. Supports up to 3 videos. Supports MP4, MOV; video encoding supports H.264, H.265, audio encoding supports AAC, MP3; a single file size cannot exceed 50 MB; the duration of a single segment is 2 to 15 seconds, and the total duration of all reference videos cannot exceed 15 seconds; the video side length must be between 256 and 5760 pixels, the aspect ratio must be between 0.4 and 2.5, and the frame rate must be between 23.976 and 60.
    - `reference_audio_urls` (array, maxItems=3): Array of reference audio URLs. Supports up to 3 audios. Supports WAV, MP3; a single file size cannot exceed 15 MB; the duration of a single segment is 2 to 15 seconds, and the total duration of all reference audios cannot exceed 15 seconds. reference_audio cannot be used alone, it must be accompanied by reference_image or reference_video.
    - `aspect_ratio` (string, enum=["adaptive","21:9","16:9","4:3","1:1","3:4","9:16"], default="adaptive"): Video aspect ratio. The default is adaptive, or a specific ratio can be specified.
    - `duration` (integer, REQUIRED, enum=[4,5,6,7,8,9,10,11,12,13,14,15], default=6, minimum=4, maximum=15): The duration of the generated video, supporting integer values from 4 to 15 seconds.
    - `resolution` (string, enum=["768P","2K"], default="2K"): Video resolution.

#### `hailuo/2-3-image-to-video-pro` (Hailuo 2.3 Pro Image to Video)
- Doc: https://docs.kie.ai/market/hailuo/2-3-image-to-video-pro
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Text prompt describing the desired video animation (Max length: 5000 characters)
  - `image_url` (string, REQUIRED): Input image to animate (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `duration` (string, enum=["6","10"], default="6"): The duration of the video in seconds. 10 seconds videos are not supported for 1080p resolution.
  - `resolution` (string, enum=["768P","1080P"], default="768P"): The resolution of the generated video.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
{
  "model": "hailuo/2-3-image-to-video-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "A graceful geisha performs a traditional Japanese dance indoors. She wears a luxurious red kimono with golden floral emb…",
    "image_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1761736831884xl56xfiw.webp",
    "duration": "6",
    "resolution": "768P"
  }
}
```

#### `hailuo/2-3-image-to-video-standard` (Hailuo 2.3 Standard Image to Video)
- Doc: https://docs.kie.ai/market/hailuo/2-3-image-to-video-standard
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `hailuo/2-3-image-to-video-pro` (no field differences in the docs).

**PixVerse V6:**

#### `pixverse-v6/text-to-video` (PixVerse V6 Text-to-Video)
- Doc: https://docs.kie.ai/market/pixverse/text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): Generate prompt, cannot be empty, length is limited to 3-5000 characters.
  - `aspect_ratio` (string, REQUIRED, enum=["16:9","4:3","1:1","3:4","9:16","2:3","3:2","21:9"], default="16:9"): Output video aspect ratio. This parameter is supported in text-to-video and Fusion multi-reference image-to-video modes.
  - `quality` (string, REQUIRED, enum=["360p","540p","720p","1080p"], default="720p"): Output video resolution. Supports 360p, 540p, 720p, and 1080p.
  - `duration` (integer, REQUIRED, default=5, minimum=1, maximum=15): Output video duration in seconds. PixVerse V6 supports 1–15 seconds.
  - `generate_audio_switch` (boolean, default=false): Whether to generate audio synchronized with the video content.
  - `generate_multi_clip_switch` (boolean, default=false): Whether to generate a multi-clip video.
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed, value range is 0–2147483647. Using the same parameters and seed helps improve result reproducibility.

#### `pixverse-v6/image-to-video` (PixVerse V6 Image-to-Video)
- Doc: https://docs.kie.ai/market/pixverse/image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): Generate prompt, cannot be empty, length is limited to 3-5000 characters.
  - `image_urls` (array, REQUIRED): Image URLs, supports up to 2 images, single image size not exceeding 20 MB. Supports HTTP, HTTPS, and OSS addresses. Supported image formats include JPG, JPEG, PNG, and WebP.
  - `quality` (string, REQUIRED, enum=["360p","540p","720p","1080p"], default="720p"): Output video resolution. Supports 360p, 540p, 720p, and 1080p.
  - `duration` (integer, REQUIRED, default=5, minimum=1, maximum=15): Generated video duration in seconds, ranging from 1 to 15. Required when template_id is not passed; if template_id is passed, the video duration is fixed by the selected template, please do not pass t …[truncated, see doc]
  - `generate_audio_switch` (boolean, default=false): Whether to generate audio synchronized with the video content.
  - `generate_multi_clip_switch` (boolean, default=false): Whether to generate a multi-clip video.
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed, value range is 0-2147483647. Using the same parameters and seed helps improve result reproducibility.
  - `template_id` (string, enum=[50 values, see doc]): Used to select a PixVerse video effect template. Please pass in the corresponding template_id. Once a template_id is provided, the video duration is fixed by the selected template, so duration cannot …[truncated, see doc]

#### `pixverse-v6/transition` (PixVerse V6 First & Last Frame Transition)
- Doc: https://docs.kie.ai/market/pixverse/transition
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): Generate prompt, cannot be empty, length is limited to 3-5000 characters.
  - `first_frame_image_url` (string, REQUIRED, format=uri): First frame image URL. Supports HTTP, HTTPS, and OSS addresses; supported image formats include JPG, JPEG, PNG, and WebP; the size of a single image file must not exceed 20 MB
  - `last_frame_image_url` (string, REQUIRED, format=uri): Last frame image URL. Supports HTTP, HTTPS, and OSS addresses; supported image formats include JPG, JPEG, PNG, and WebP; the size of a single image file must not exceed 20 MB
  - `quality` (string, REQUIRED, enum=["360p","540p","720p","1080p"], default="720p"): Output video resolution. Supports 360p, 540p, 720p, and 1080p.
  - `duration` (integer, REQUIRED, default=5, minimum=1, maximum=15): Output video duration in seconds. PixVerse V6 supports 1–15 seconds.
  - `generate_audio_switch` (boolean, default=false): Whether to generate audio synchronized with the video content.
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed, value range is 0–2147483647. Using the same parameters and seed helps improve result reproducibility.

#### `pixverse-v6/extend` (PixVerse V6 Video Extension)
- Doc: https://docs.kie.ai/market/pixverse/extend
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - **anyOf variant 0 (TaskId):**
    - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): Generate prompt, cannot be empty, length is limited to 3-5000 characters.
    - `duration` (integer, REQUIRED, minimum=1, maximum=15): Generated video duration in seconds. Current validation range is 1-15.
    - `quality` (string, REQUIRED, enum=["360p","540p","720p","1080p"]): Resolution.
    - `generate_audio_switch` (boolean): Whether to generate audio.
    - `seed` (integer, minimum=0, maximum=2147483647): Random seed, optional. Range 0-2147483647.
    - `taskId` (string, REQUIRED): The taskId of the parent video task to be extended. The parent task must belong to the current user, be undeleted, and have a status of success. KIE does not accept official source_video_id/video_id. …[truncated, see doc]
  - **anyOf variant 1 (Video):**
    - `prompt` (string, REQUIRED, minLength=3, maxLength=5000)
    - `duration` (integer, REQUIRED, minimum=1, maximum=15)
    - `quality` (string, REQUIRED, enum=["360p","540p","720p","1080p"])
    - `generate_audio_switch` (boolean)
    - `seed` (integer, minimum=0, maximum=2147483647)
    - `video_url` (string, REQUIRED)

#### `pixverse-v6/reference-to-video` (PixVerse V6 Fusion / Reference-to-Video)
- Doc: https://docs.kie.ai/market/pixverse/reference-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): Generate prompt, cannot be empty, length is limited to 3-5000 characters.
  - `image_references` (array, REQUIRED, minItems=1, maxItems=7): Fusion multi-reference image list. `ref_name` must be unique within the same list. You can reference the reference object in the prompt via `@ref_name`.
  - `image_references[].image_url` (string, REQUIRED, format=uri): Reference image URL.
  - `image_references[].type` (string, enum=["subject","background"], default="subject"): Reference image type. `subject` means subject, `background` means background.
  - `image_references[].ref_name` (string, minLength=1, maxLength=30): Reference image name, maximum 30 characters. Can be referenced in the prompt using `@name`.
  - `aspect_ratio` (string, REQUIRED, enum=["16:9","4:3","1:1","3:4","9:16","2:3","3:2","21:9"], default="16:9"): Output video aspect ratio. Supported in text-to-video and Fusion multi-reference image to video modes.
  - `quality` (string, REQUIRED, enum=["360p","540p","720p","1080p"], default="720p"): Output video resolution. Supports 360p, 540p, 720p, and 1080p.
  - `duration` (integer, REQUIRED, default=5, minimum=1, maximum=15): Output video duration, in seconds.
  - `generate_audio_switch` (boolean, default=false): Whether to generate audio synchronized with the video content.
  - `seed` (integer, minimum=0, maximum=2147483647): Random seed, value range is 0-2147483647. Using the same parameters and seed helps improve the reproducibility of the results.

**HappyHorse (Alibaba):**

#### `happyhorse-1-1/text-to-video` (HappyHorse-1-1 text-to-video)
- Doc: https://docs.kie.ai/market/happyhorse-1-1/text-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, default="", maxLength=4999): Text description of the video to generate. Supports any language. Maximum 5,000 non-Chinese characters or 2,500 Chinese
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Output video resolution. Options: 720p; 1080p
  - `aspect_ratio` (string, enum=["16:9","9:16","1:1","4:3","3:4","4:5","5:4","9:21","21:9"], default="16:9"): Output video aspect ratio. Options: 16:9; 9:16; 1:1; 4:3; 3:4; 4:5; 5:4; 9:21; 21:9
  - `duration` (number, default=5, minimum=3, maximum=15): Output video duration in seconds.

#### `happyhorse-1-1/image-to-video` (HappyHorse-1-1 image-to-video)
- Doc: https://docs.kie.ai/market/happyhorse-1-1/image-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, default="", maxLength=5000): Describes the video content to generate. Supports any language. Maximum: 5,000 non-Chinese characters or 2,500 Chinese
  - `image_urls` (array, REQUIRED, default=[""], maxItems=1): The URL of the first frame image. Image constraints: 1. Formats: JPEG, JPG, PNG, WEBP. 2. Resolution: Width and height must both be at least 300 pixels. 3. Aspect ratio: Between 1:2.5 and 2.5:1. 4. Fi …[truncated, see doc]
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): The resolution of the generated video. Options: 720p; 1080p
  - `duration` (number, default=5, minimum=3, maximum=15): The duration of the generated video, in seconds. The value must be an integer in the range [3, 15]. Default: 5

#### `happyhorse-1-1/reference-to-video` (HappyHorse-1-1 reference-to-video)
- Doc: https://docs.kie.ai/market/happyhorse-1-1/reference-to-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, default="", maxLength=5000): A description of the desired elements and visual style for the generated video. Input in any language is supported. The length is limited to 5,000 non-Chinese characters or 2,500 Chinese characters. C …[truncated, see doc]
  - `reference_image` (array, REQUIRED, default=[], maxItems=9): The URL of a reference image. Image requirements: 1. Formats: JPEG, JPG, PNG, WEBP. 2. Resolution: The shortest side must be at least 400 pixels. A clear image with a resolution of 720P or higher is r …[truncated, see doc]
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): The resolution tier of the generated video. Options: 720p; 1080p
  - `aspect_ratio` (string, enum=["16:9","9:16","3:4","4:3","4:5","5:4","1:1","9:21","21:9"], default="16:9"): The aspect ratio of the generated video. Options: 16:9; 9:16; 3:4; 4:3; 4:5; 5:4; 1:1; 9:21; 21:9
  - `duration` (number, default=5, minimum=3, maximum=15): The duration of the generated video, in seconds. Value range: An integer from 3 to 15.

#### `happyhorse/video-edit` (HappyHorse - video-edit)
- Doc: https://docs.kie.ai/market/happyhorse/video-edit
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Required edit instruction describing the intended change (e.g., style transfer / local replacement). Max 5,000 non‑Chinese characters or 2,500 Chinese characters; extra content is truncated.
  - `video_url` (string, REQUIRED): Input video URL list. Exactly one video is required. Video requirements: Format: MP4, MOV (H.264 encoding recommended). Duration: 3–60 seconds. Resolution: the longer side must not exceed 2,160 px; th …[truncated, see doc]
  - `reference_image ` (array, minItems=0, maxItems=5): Optional reference image URL list (0–5). Image requirements: Format: JPEG, JPG, PNG, WEBP. Resolution: both width and height must be at least 300 px. Aspect ratio: 1:2.5–2.5:1. File size: up to 10 MB.
  - `resolution` (string, enum=["720p","1080p"], default="1080p"): Output video resolution. Valid values: 720P, 1080P (default).
  - `audio_setting` (string, enum=["auto","origin"], default="auto"): Audio handling strategy for the output video.
  - `seed` (integer, default=0, minimum=0, maximum=2147483647): Random seed for reproducibility (if supported).

**Runway (current docs, unified createTask):**

#### `runway` (Generate AI Video)
- Doc: https://docs.kie.ai/runway-api/generate-ai-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED): Descriptive text that guides the AI video generation. Be specific about subject, action, style, and setting. When used with an image, describes how to animate or modify the image content. Maximum length is 1800 characters.
  - `image_url` (string): Optional reference image URL to base the video on. When provided, the AI will create a video animating or extending this image.
  - `duration` (number, REQUIRED): Video duration, optional values are 5 or 10. If 10-second video is selected, 1080p resolution cannot be used
  - `quality` (string, REQUIRED): Video resolution, optional values are 720p or 1080p. If 1080p is selected, 10-second video cannot be generated
  - `aspect_ratio` (string, enum=["16:9","4:3","1:1","3:4","9:16"]): Video aspect ratio parameter. **Required parameter for text-to-video generation requests. This parameter is invalid when image_url is passed, and the aspect ratio will ultimately be determined by the provided image.**
  - `watermark` (string): Video watermark text content. An empty string indicates no watermark, while a non-empty string will display the specified text as a watermark in the bottom right corner of the video.
- Request example from the doc:

```json
{
  "model": "runway",
  "callBackUrl": "https://api.example.com/callback",
  "input": {
    "prompt": "A fluffy orange cat dancing energetically in a colorful room with disco lights",
    "image_url": "https://example.com/cat-image.jpg",
    "duration": "5",
    "quality": "720p",
    "aspect_ratio": "9:16",
    "watermark": "kie.ai"
  }
}
```

#### `runway/extend-ai-video` (Extend AI Video)
- Doc: https://docs.kie.ai/runway-api/extend-ai-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `task_id` (string, REQUIRED): Unique identifier of the original video generation task. Must be a valid task ID from a previously generated video.
  - `prompt` (string, REQUIRED): Descriptive text that guides the continuation of the video. Explain what actions, movements, or developments should happen next. Be specific but maintain consistency with the original video content.
  - `quality` (string, REQUIRED): Video resolution, optional values are 720p or 1080p.
  - `watermark` (string): Video watermark text content. An empty string indicates no watermark, while a non-empty string will display the specified text as a watermark in the bottom right corner of the video.
- Request example from the doc:

```json
{
  "model": "runway/extend-ai-video",
  "callBackUrl": "https://api.example.com/callback",
  "input": {
    "task_id": "ee603959-debb-48d1-98c4-a6d1c717eba6",
    "prompt": "The cat continues dancing with more energy and excitement, spinning around with colorful light effects intensifying",
    "quality": "720p",
    "watermark": "kie.ai"
  }
}
```

#### `runway/gen4-aleph` (Generate Aleph Video)
- Doc: https://docs.kie.ai/runway-api/generate-aleph-video
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- WARNING: this model id is NOT in the live `GET /api/v1/models` list pulled 2026-10-04 (documented but possibly not callable).
- Params:
  - `prompt` (string, REQUIRED): Descriptive text that guides the AI video generation. Be specific about subject, action, style, and setting. Describes how to animate or modify the reference image content.
  - `video_url` (string, REQUIRED): Reference video URL to base the video-to-video generation on. The AI will transform and enhance this video according to the prompt.
  - `watermark` (string): Optional watermark text content. An empty string indicates no watermark, while a non-empty string will display the specified text as a watermark in the video.
  - `upload_cn` (boolean, default=false): Upload method selection. Default value is false (S3/R2), set to true for Alibaba Cloud OSS upload, set to false for overseas R2 server upload.
  - `aspect_ratio` (string, enum=["16:9","9:16","4:3","3:4","1:1","21:9"]): Video aspect ratio.
  - `seed` (integer): Random seed. Set for reproducible generation.
  - `reference_image` (string, format=uri): Reference image URL to influence the style or content of the output.
- Request example from the doc:

```json
{
  "model": "runway/gen4-aleph",
  "callBackUrl": "https://api.example.com/callback",
  "input": {
    "prompt": "A majestic eagle soaring through mountain clouds at sunset with cinematic camera movement",
    "video_url": "https://example.com/input-video.mp4",
    "watermark": "kie.ai",
    "upload_cn": false,
    "aspect_ratio": "16:9",
    "seed": 123456,
    "reference_image": "https://example.com/reference.jpg"
  }
}
```


### A.5 Text to speech, audio, music

#### `elevenlabs/text-to-speech-turbo-2-5`
- Doc: https://docs.kie.ai/market/elevenlabs/text-to-speech-turbo-2-5
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `text` (string, REQUIRED, maxLength=5000): The text to convert to speech (Max length: 5000 characters)
  - `voice` (string, enum=[67 voice ids, see section 5.2 table], default="EkK5I93UQWFDigLMpZcX"): The voice to use for speech generation. Can be a preset voice name (e.g. Rachel, Adam) or a voice ID. You can preview a voice by opening https://static.aiquickdraw.com/elevenlabs/voice/<voice_id>.mp3 in your browser (replace <voice_id> with the actual voice ID). For example: https://static.aiquickdraw.com/elevenlabs/voice/N2lVS1w4EtoT3dr4eOWO.mp3 Available voices: see section 5.2 table.
  - `stability` (number, default=0.5, minimum=0, maximum=1): Voice stability (0-1) (Min: 0, Max: 1, Step: 0.01) (step: 0.01)
  - `similarity_boost` (number, default=0.75, minimum=0, maximum=1): Similarity boost (0-1) (Min: 0, Max: 1, Step: 0.01) (step: 0.01)
  - `style` (number, default=0, minimum=0, maximum=1): Style exaggeration (0-1) (Min: 0, Max: 1, Step: 0.01) (step: 0.01)
  - `speed` (number, default=1, minimum=0.7, maximum=1.2): Speech speed (0.7-1.2). Values below 1.0 slow down the speech, above 1.0 speed it up. Extreme values may affect quality. (Min: 0.7, Max: 1.2, Step: 0.01) (step: 0.01)
  - `timestamps` (boolean): Whether to return timestamps for each word in the generated speech (Boolean value (true/false))
  - `previous_text` (string, maxLength=5000): The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation. (Max length: 5000 characters)
  - `next_text` (string, maxLength=5000): The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation. (Max length: 5000 characters)
  - `language_code` (string, maxLength=500): Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 and Flash v2.5 support language enforcement. For other models, an error will be returned if language code is provided. (Max length: 500 characters)
- Request example from the doc:

```json
{
  "model": "elevenlabs/text-to-speech-turbo-2-5",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "text": "Unlock powerful API with Kie.ai! Affordable, scalable APl integration, free trial playground, and secure, reliable performance.",
    "voice": "Rachel",
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0,
    "speed": 1,
    "timestamps": false,
    "previous_text": "",
    "next_text": "",
    "language_code": ""
  }
}
```

#### `elevenlabs/text-to-speech-multilingual-v2` (elevenlabs/text-to-speech-multilingual-v2)
- Doc: https://docs.kie.ai/market/elevenlabs/text-to-speech-multilingual-v2
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `elevenlabs/text-to-speech-turbo-2-5` except: `voice` is (string, REQUIRED, enum=[long list], default="EkK5I93UQWFDigLMpZcX") instead of (string, enum=[long list], default="EkK5I93UQWFDigLMpZcX").

#### `elevenlabs/text-to-dialogue-v3`
- Doc: https://docs.kie.ai/market/elevenlabs/text-to-dialogue-v3
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `dialogue` (array, REQUIRED): Array of dialogue items. Each item contains text and voice. The total character count of all text fields combined must not exceed 5000 characters.
  - `dialogue[].text` (string, REQUIRED): The dialogue text content. All text fields in the dialogue array combined must not exceed 5000 characters.
  - `dialogue[].voice` (string, REQUIRED, enum=[67 voice ids, see section 5.2 table], default="EkK5I93UQWFDigLMpZcX"): The voice to use for speech generation. Can be a preset voice name (e.g. Rachel, Adam) or a voice ID. You can preview a voice by opening https://static.aiquickdraw.com/elevenlabs/voice/<voice_id>.mp3 in your browser (replace <voice_id> with the actual voice ID). For example: https://static.aiquickdraw.com/elevenlabs/voice/N2lVS1w4EtoT3dr4eOWO.mp3 Available voices: see section 5.2 table.
  - `stability` (number, enum=[0,0.5,1], default=0.5): Voice stability parameter. Must be one of the following values: 0.0, 0.5, or 1.0
  - `language_code` (string, enum=["af","ar","hy","as","az","be","bn","bs","bg","ca","ceb","ny","hr","cs","da","nl","en","et","fil","fi","fr","gl","ka","de","el","gu","ha","he","hi","hu","is","id","ga","it","ja","jv","kn","kk","ky","ko","lv","ln","lt","lb","mk","ms","ml","zh","mr","ne","no","ps","fa","pl","pt","pa","ro","ru","sr","sd","sk","sl","so","es","sw","sv","ta","te","th","tr","uk","ur","vi","cy"]): Language code for the speech. Default is empty string or omit the parameter for automatic language detection.
- Request example from the doc:

```json
{
  "model": "elevenlabs/text-to-dialogue-v3",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "dialogue": [
      {
        "text": "I have a pen, I have an apple, ah, Apple pen~",
        "voice": "EkK5I93UQWFDigLMpZcX"
      },
      {
        "text": "a happy dog",
        "voice": "Z3R5wn05IrDiVCyEkUrK"
      },
      {
        "text": "a happy cat",
        "voice": "NNl6r8mD7vthiJatiJt1"
      }
    ],
    "stability": 0.5
  }
}
```

#### `elevenlabs/audio-isolation`
- Doc: https://docs.kie.ai/market/elevenlabs/audio-isolation
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- WARNING: this model id is NOT in the live `GET /api/v1/models` list pulled 2026-10-04 (documented but possibly not callable).
- Params:
  - `audio_url` (string, REQUIRED): URL of the audio file to isolate voice from (File URL after upload, not file content; Accepted types: audio/mpeg, audio/wav, audio/x-wav, audio/aac, audio/mp4, audio/ogg; Max size: 10.0MB)
- Request example from the doc:

```json
{
  "model": "elevenlabs/audio-isolation",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "audio_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1756964657418ljw1jbzr.mp3"
  }
}
```

#### `google/gemini-3-8-flash-tts` (Gemini 3.8 Flash Text to speech)
- Doc: https://docs.kie.ai/market/google/gemini-3-8-flash-tts
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `temperature` (number, default=1, minimum=0, maximum=2): Sampling temperature, e.g., 1
  - `speakers` (array, REQUIRED): List of speaker configurations
  - `speakers[].speaker_id` (string, REQUIRED): Speaker identifier, e.g., "Speaker 1" or "Speaker 2". Must be in "Speaker N" format. When two people are speaking, you can turn on the `filler_words` switch.
  - `speakers[].voice_name` (string, enum=[70 values, see doc], default="Fola"): Voice name. Default `Fola`. 70 voices grouped by use case: - Tutor: Bodi, Lumi, Sadaltager, Sola, Sulafat, Varo, Zephyr - Commercial Voiceover: Koda, Kore, Nika, Tavi, Zeno - Instructional: Algenib, Despina, Erinome, Kira, Ludo, Mako, Rasalgethi, Rina - Podcast: Alnilam, Brio, Jori, Laomedeia, Rami, Veda - Storyteller: Achird, Enzo, Riko, Sami, Zali, Zubenelgenubi - Digital Assistant: Algieba, Aoede, Autonoe, Callirrhoe, Enceladus, Gero, Iapetus, Neno, Olin, Tari, Umbriel - Call Center: Achernar, Charon, Daro, Fola, Hali, Milo, Puck - Concierge: Arlo, Cleo, Fenrir, Finn, Leda, Lora, Orus - Tech Support: Enya, Jett, Knox, Nyla, Sadachbia, Vindemiatrix - Professional: Cruz, Elio, Gacrux, Pulcherrima, Schedar, Tova, Zuri
  - `filler_words` (boolean, default=false): Whether to insert filler words in two-speaker dialogue. Off by default (omit this field); when enabled, the request includes `"filler_words": true`. Only takes effect when `speakers` has two speakers (e.g. Speaker 1 and Speaker 2).
  - `dialogue_turns` (array, REQUIRED): List of dialogue turns, output in sequential order
  - `dialogue_turns[].speaker_id` (string, REQUIRED): Corresponding speaker identifier, e.g., "Speaker 1"
  - `dialogue_turns[].text` (string, REQUIRED, maxLength=10000): The speaker's line. May include tone tags wrapped in English angle brackets. Example: Hello there. &lt;laugh&gt; That works. Official insertable tags: &lt;argh&gt;, &lt;breath&gt;, &lt;cackle&gt;, &lt;cheer&gt;, &lt;chuckle&gt;, &lt;chuckles&gt;, &lt;cough&gt;, &lt;cry&gt;, &lt;exhales&gt;, &lt;gasp&gt;, &lt;giggle&gt;, &lt;groan&gt;, &lt;growl&gt;, &lt;grr&gt;, &lt;grunt&gt;, &lt;heavy breath&gt;, &lt;hiss&gt;, &lt;laugh&gt;, &lt;laughter&gt;, &lt;long pause&gt;, &lt;moan&gt;, &lt;pant&gt;, &lt;pff&gt;, &lt;phew&gt;, &lt;scream&gt;, &lt;short pause&gt;, &lt;shout&gt;, &lt;shriek&gt;, &lt;sigh&gt;, &lt;sighs&gt;, &lt;sneeze&gt;, &lt;snicker&gt;, &lt;snort&gt;, &lt;sob&gt;, &lt;throat-clearing&gt;, &lt;tsk&gt;, &lt;whimper&gt;, &lt;whispering&gt;, &lt;whispers&gt;, &lt;yawn&gt;.
  - `dialogue_turns[].style` (string): Per-turn speaking style, 3.8 only. Freely describe tone, emotion, and pace; different lines from the same speaker can differ. Example: Speak like a tired night-shift radio host, slow and dry.
- Request example from the doc:

```json
{
  "model": "google/gemini-3-8-flash-tts",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "temperature": 1,
    "speakers": [
      {
        "speaker_id": "Speaker 1",
        "voice_name": "Fola"
      },
      {
        "speaker_id": "Speaker 2",
        "voice_name": "Zephyr"
      }
    ],
    "dialogue_turns": [
      {
        "speaker_id": "Speaker 1",
        "style": "Speak like a tired night-shift radio host, slow and dry.",
        "text": "Hello there. <laugh> That works."
      },
      {
        "speaker_id": "Speaker 2",
        "style": "Bright and curious, slightly faster.",
        "text": "Wait, did you hear that? <gasp> I think it actually worked."
      }
    ]
  }
}
```
- 200 response example: `"{\n    \"code\": 200,\n    \"msg\": \"success\",\n    \"data\": {\n        \"taskId\": \"task_1765185282276\",\n    }\n}"`

#### `google/gemini-3-8-flash-lite-tts` (Gemini 3.8 Flash Lite Text to speech)
- Doc: https://docs.kie.ai/market/google/gemini-3-8-flash-lite-tts
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `google/gemini-3-8-flash-tts` (no field differences in the docs).

#### `google/gemini-3-1-flash-tts` (Gemini 3.1 Flash Text to speech)
- Doc: https://docs.kie.ai/market/google/gemini-3-1-flash-tts
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `temperature` (number, default=1, minimum=0, maximum=2): Sampling temperature, e.g., 1
  - `scene` (string, default=""): Scene description, e.g., "A quiet, warm room with a fireplace crackling softly."
  - `sample_context` (string, default=""): Sample context/overall tone, e.g., "Audiobook style narration. Tone is gentle and inviting."
  - `speakers` (array, REQUIRED): List of speaker configurations
  - `speakers[].speaker_id` (string, REQUIRED): Speaker identifier, e.g., "Speaker 1" or "Speaker 2";Must be 「Speaker N」format
  - `speakers[].voice_name` (string, REQUIRED, enum=["Achernar","Achird","Algenib","Algieba","Alnilam","Aoede","Autonoe","Callirrhoe","Charon","Despina","Enceladus","Erinome","Fenrir","Gacrux","Iapetus","Kore","Laomedeia","Leda","Orus","Puck","Pulcherrima","Rasalgethi","Sadachbia","Sadaltager","Schedar","Sulafat","Umbriel","Vindemiatrix","Zephyr","Zubenelgenubi"]): Voice name, e.g., "Zephyr", "Fenrir", "Puck"
  - `speakers[].audio_profile` (string): Audio profile description, e.g., "A warm and soothing narrator" or "A stern and weary gatekeeper"
  - `speakers[].accent` (string, REQUIRED, enum=["Neutral","American (Gen)","American (Valley)","American (South)","British (RP)","British (Brixton)","Transatlantic","Australian"]): Accent, e.g., "British (RP)" or "American (Gen)"
  - `speakers[].style` (string, enum=["Vocal Smile","Newscaster","Whisper","Empathetic","Promo/Hype","Deadpan"]): Emotional style, e.g., "Gentle" or "Deadpan"
  - `speakers[].pace` (string, enum=["Natural","Rapid Fire","The Drift","Staccato"]): Pace, e.g., "Slow" or "Natural"
  - `dialogue_turns` (array, REQUIRED): List of dialogue turns, output in sequential order
  - `dialogue_turns[].speaker_id` (string, REQUIRED): Corresponding speaker identifier, e.g., "Speaker 1"
  - `dialogue_turns[].text` (string, REQUIRED, maxLength=10000): The text spoken by the speaker, which may contain tone tags, e.g., "Once upon a time, in a quiet valley hidden away..."
- Request example from the doc:

```json
{
  "model": "google/gemini-3-1-flash-tts",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "temperature": 1,
    "scene": "A dark, crumbling dungeon...",
    "sample_context": "Fantasy RPG style...",
    "speakers": [
      {
        "speaker_id": "Speaker 1",
        "voice_name": "Fenrir",
        "audio_profile": "A stern and weary gatekeeper",
        "accent": "British (RP)",
        "style": "Deadpan",
        "pace": "Natural"
      },
      {
        "speaker_id": "Speaker 2",
        "voice_name": "Puck",
        "audio_profile": "A determined and courageous traveler seeking answers.",
        "accent": "American (Gen)",
        "style": "Empathetic",
        "pace": "Staccato"
      }
    ],
    "dialogue_turns": [
      {
        "speaker_id": "Speaker 1",
        "text": "[shouting] Halt, traveler! The northern pass is sealed by order of the council."
      },
      {
        "speaker_id": "Speaker 2",
        "text": "[determination] I carry a message for the elder. Step aside, or I will force my way through."
      },
      {
        "speaker_id": "Speaker 1",
        "text": "[caution] No one passes. [pensive] The elder is... he's no longer receiving visitors."
      },
      {
        "speaker_id": "Speaker 2",
        "text": "It's too late. [whispers] The shadow... it reached him first. [urgency] You need to leave. [shouting] Now."
      }
    ]
  }
}
```
- 200 response example: `"{\n    \"code\": 200,\n    \"msg\": \"success\",\n    \"data\": {\n        \"taskId\": \"task_1765185282276\",\n    }\n}"`

#### `google/gemini-2-5-pro-tts` (Gemini 2.5 Pro Text to Speech)
- Doc: https://docs.kie.ai/google/gemini-2-5-pro-tts
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `google/gemini-3-1-flash-tts` (no field differences in the docs).

#### `ai-music-api/generate` (Generate Music)
- Doc: https://docs.kie.ai/suno-api/generate-music
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string): A description of the desired audio content. Optional. - Custom mode (`custom_mode=true`): When provided, the prompt is used strictly as lyrics and sung in the generated track. Character limits by model: - V4: Maximum 3000 characters - V4_5, V4_5PLUS, V4_5ALL, …[truncated, see doc]
  - `style` (string): Music style specification for the generated audio. - Character limits by model: - **V4** (Discontinued): Maximum 200 characters - **V4_5 and V4_5PLUS** (Discontinued): Maximum 1000 characters - **V4_5ALL** (Discontinued): Maximum 1000 characters - **V5_5 and V …[truncated, see doc]
  - `title` (string): Title for the generated music track. - Required in Custom Mode (`custom_mode: true`). - Max length: 80 characters. - Will be displayed in player interfaces and filenames.
  - `custom_mode` (boolean, REQUIRED): Determines whether advanced parameter customization is enabled. - If `true`: Allows detailed control - If `false`: Simplified mode
  - `instrumental` (boolean, REQUIRED): Determines whether the audio should be instrumental (no lyrics). - In Custom Mode (`custom_mode: true`): - If `true`: Only `style` and `title` are required. - If `false`: `style`, `title`, and `prompt` are required (`prompt` is used as the exact lyrics). - In …[truncated, see doc]
  - `model` (string, REQUIRED, enum=["V4","V4_5","V4_5PLUS","V4_5ALL","V5","V5_5","V6","V6_MINI","V6_WILD"], default="V6"): The AI model version to use for generation. - Required for all requests. - Available options: - **`V6_WILD`**: Pushes creative boundaries for bolder, more distinctive musical expression. - **`V6_MINI`**: Lightweight and fast, balancing quality and speed for ef …[truncated, see doc]
  - `negative_tags` (string): Music styles or traits to exclude from the generated audio. Optional. Use to avoid specific styles.
  - `vocal_gender` (string, enum=["m","f"]): Vocal gender preference. Optional. Use `m` for male and `f` for female. This parameter is only effective when `custom_mode` is true. In practice, it only increases probability and cannot guarantee male/female voice instructions are followed.
  - `style_weight` (number, minimum=0, maximum=1): Only available when Custom Mode (`custom_mode: true`) is enabled. Strength of adherence to the specified style. Optional. Range 0–1, up to 2 decimal places.
  - `weirdness_constraint` (number, minimum=0, maximum=1): Only available when Custom Mode (`custom_mode: true`) is enabled. Controls experimental/creative deviation. Optional. Range 0–1, up to 2 decimal places.
  - `audio_weight` (number, minimum=0, maximum=1): Only available when Custom Mode (`custom_mode: true`) is enabled. Relative weight of audio features. Optional. Range 0–1, up to 2 decimal places. - `audio_weight` is not supported when there are no vocals
  - `persona_id` (string): Persona ID or Voice ID to apply to the generated music. Optional. Use this to apply a specific persona style to your music generation. To generate a Persona ID, use the [Generate Persona](https://docs.kie.ai/suno-api/generate-persona) endpoint to create a pers …[truncated, see doc]
  - `persona_model` (string, enum=["style_persona","voice_persona"]): Persona model. Only available for V5 (Discontinued), V5.5 (Discontinued), V6, V6_MINI, and V6_WILD.
  - `duration` (number, default=20, minimum=10, maximum=360): Audio duration. Optional; only valid when `custom_mode` is true and the model is V5_5 (Discontinued), V6, V6_MINI, or V6_WILD.
  - `image_urls` (array, maxItems=5): Image references. Only effective when `custom_mode=false`. - Optional - Up to 5 images; each image must not exceed 10 MB - Supported formats: `jpeg`, `png`, `webp`, and `bmp`
  - `variety` (number, default=1, minimum=0, maximum=4): Only available when Custom Mode (`custom_mode: true`) is enabled. Controls the diversity and stylistic variation of generated results. Optional. Range 0–4, integer, default 1. - **`0`**: off (exact style) — fully off, strictly the same style - **`1`**: normal …[truncated, see doc]
  - `lyrics` (string): Lyrics for the generated audio. Optional. - V6: Maximum 5000 characters. - When `custom_mode=true`, `lyrics` is used as lyrics first; if `lyrics` is not provided, `prompt` is used as lyrics. - When `custom_mode=false`, `lyrics` is used as a lyrics attachment a …[truncated, see doc]
  - `audio_urls` (array): Audio references. Only effective when `custom_mode=false`. - Optional - Audio duration must be between 6 seconds and 30 minutes; each audio file must not exceed 500 MB
  - `video_urls` (array, maxItems=1): Video references. Only effective when `custom_mode=false`. - Optional - Up to 1 video file; each file must not exceed 100 MB, duration must not exceed 241 seconds, with no minimum duration - Supported formats: mp4, mov, and webm
- Request example from the doc:

```json
{
  "model": "ai-music-api/generate",
  "callBackUrl": "https://api.example.com/callback",
  "input": {
    "prompt": "A calm and relaxing piano track with soft melodies",
    "custom_mode": true,
    "instrumental": true,
    "model": "V4",
    "style": "Classical",
    "title": "Peaceful Piano Meditation",
    "negative_tags": "Heavy Metal, Upbeat Drums",
    "vocal_gender": "m",
    "style_weight": 0.65,
    "weirdness_constraint": 0.65,
    "audio_weight": 0.65,
    "persona_id": "persona_123",
    "persona_model": "style_persona",
    "duration": 20
  }
}
```

#### `ai-music-api/sounds` (Generate sounds)
- Doc: https://docs.kie.ai/suno-api/generate-sounds
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED): Sound task type limit: 500 characters
  - `model` (string, REQUIRED, enum=["V5","V5_5","V6","V6_WILD","V6_MINI"]): Model Name - **`V6_WILD`**: Pushes creative boundaries for bolder, more distinctive musical expression. - **`V6_MINI`**: Lightweight and fast, balancing quality and speed for effortless creation. - **`V6`**: Greater musical expression with more natural vocals …[truncated, see doc]
  - `sound_loop` (boolean, default=false): Is it a cycle?
  - `sound_tempo` (integer, default=null, minimum=1, maximum=300): Do not broadcast.
  - `sound_key` (string, enum=["Cm","C#m","Dm","D#m","Em","Fm","F#m","Gm","G#m","Am","A#m","Bm","C","C#","D","D#","E","F","F#","G","G#","A","A#","B"], default="Any")
  - `grab_lyrics` (boolean, default=false): Whether to capture the lyrics subtitles Will the interface be called after completion to obtain the lyrics subtitles?
- Request example from the doc:

```json
{
  "model": "ai-music-api/sounds",
  "callBackUrl": "https://api.example.com/callback",
  "input": {
    "prompt": "sint",
    "model": "V5",
    "sound_loop": true,
    "sound_tempo": 166,
    "sound_key": "D#m",
    "grab_lyrics": true
  }
}
```
- 200 response example: `{"code":422,"msg":"success","data":{"taskId":"task38695****935u9043u"}}`

#### `ai-music-api/timeStamped-lyrics` (Get Timestamped Lyrics)
- Doc: https://docs.kie.ai/suno-api/get-timestamped-lyrics
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `task_id` (string, REQUIRED): Unique identifier of the music generation task. This should be a task_id returned from either the "Generate Music" or "Extend Music" endpoints.
  - `audio_id` (string, REQUIRED): Unique identifier of the specific audio track for which to retrieve lyrics. This ID is returned in the callBackUrl data after music generation completes.
- Request example from the doc:

```json
{
  "model": "ai-music-api/timeStamped-lyrics",
  "callBackUrl": "https://api.example.com/callback",
  "input": {
    "task_id": "5c79****be8e",
    "audio_id": "e231****-****-****-****-****8cadc7dc"
  }
}
```
- 200 response example: `{"code":200,"msg":"success","data":{"alignedWords":[{"word":"[Verse]\nWaggin'","success":true,"startS":1.36,"endS":1.79,"palign":0}],"waveformData":[0,1,0.5,0.75],"hootCer":0.3803191489361702,"isStreamed":false}}`


### A.6 Image models (character sheets, start frames)

#### `google/nano-banana` (Google - Nano Banana)
- Doc: https://docs.kie.ai/market/google/nano-banana
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): The prompt for image generation (Max length: 5000 characters)
  - `output_format` (string, enum=["png","jpeg"], default="png"): Output format for the images
  - `aspect_ratio` (string, enum=["1:1","9:16","16:9","3:4","4:3","3:2","2:3","5:4","4:5","21:9","auto"], default="1:1"): Radio description
  - `image_size` (string, enum=["1:1","9:16","16:9","3:4","4:3","3:2","2:3","5:4","4:5","21:9","auto"], default="1:1"): The aspect ratio of the generated image (this parameter has been replaced by aspect_ratio; please use the latest aspect_ratio parameter).
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `google/nano-banana-edit` (Google - Nano Banana Edit)
- Doc: https://docs.kie.ai/market/google/nano-banana-edit
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): The prompt for image editing (Max length: 5000 characters)
  - `image_urls` (array, REQUIRED, maxItems=10): List of URLs of input images for editing,up to 10 images. (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `output_format` (string, enum=["png","jpeg"], default="png"): Output format for the images
  - `aspect_ratio` (string, enum=["1:1","9:16","16:9","3:4","4:3","3:2","2:3","5:4","4:5","21:9","auto"], default="1:1"): Radio description
  - `image_size` (string, enum=["1:1","9:16","16:9","3:4","4:3","3:2","2:3","5:4","4:5","21:9","auto"], default="1:1"): The aspect ratio of the generated image (this parameter has been replaced by aspect_ratio; please use the latest aspect_ratio parameter).
- Request example from the doc:

```json
{
  "model": "google/nano-banana-edit",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "turn this photo into a character figure. Behind it, place a box with the character’s image printed on it, and a computer showing the Blender…",
    "image_urls": [
      "https://file.aiquickdraw.com/custom-page/akr/section-images/1756223420389w8xa2jfe.png"
    ],
    "output_format": "png",
    "aspect_ratio": "1:1"
  }
}
```

#### `nano-banana-pro` (Google - Nano Banana Pro)
- Doc: https://docs.kie.ai/market/google/pro-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=10000): A text description of the image you want to generate (Max length: 10000 characters)
  - `image_input` (array, maxItems=8): Input images to transform or use as reference (supports up to 8 images) (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 30.0MB)
  - `aspect_ratio` (string, enum=["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9","auto"], default="1:1"): Aspect ratio of the generated image
  - `resolution` (string, enum=["1K","2K","4K"], default="1K"): Resolution of the generated image
  - `output_format` (string, enum=["png","jpg"], default="png"): Format of the output image
- Request example from the doc:

```json
{
  "model": "nano-banana-pro",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Comic poster: cool banana hero in shades leaps from sci-fi pad. Six panels: 1) 4K mountain landscape, 2) banana holds page of long multiling…",
    "image_input": [],
    "aspect_ratio": "1:1",
    "resolution": "1K",
    "output_format": "png"
  }
}
```

#### `nano-banana-2` (Google - Nano Banana 2)
- Doc: https://docs.kie.ai/market/google/nanobanana2
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=20000): A text description of the image you want to generate (Max length: 20000 characters)
  - `image_input` (array, maxItems=14): Input images to transform or use as reference (supports up to 14 images) (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 30.0MB)
  - `aspect_ratio` (string, enum=["1:1","2:3","3:2","1:4","4:1","3:4","4:3","4:5","5:4","1:8","8:1","9:16","16:9","21:9","auto"], default="auto"): Aspect ratio of the generated image
  - `resolution` (string, enum=["1K","2K","4K"], default="1K"): Resolution of the generated image
  - `output_format` (string, enum=["png","jpg"], default="jpg"): Format of the output image
- Request example from the doc:

```json
{
  "model": "nano-banana-2",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Comic poster: cool banana hero in shades leaps from sci-fi pad. Six panels: 1) 4K mountain landscape, 2) banana holds page of long multiling…",
    "image_input": [],
    "aspect_ratio": "auto",
    "resolution": "1K",
    "output_format": "png"
  }
}
```

#### `nano-banana-2-lite` (Google - Nano Banana 2 Lite)
- Doc: https://docs.kie.ai/market/google/nano-banana-2-lite
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `image_urls` (array, default=[], maxItems=10): Input image URL array. Optional parameter. Set to an empty array or omit it for pure text-to-image generation. Supports up to 10 images. - Please provide uploaded file URLs, not raw file content - Accepted types: `image/jpeg`, `im …[truncated, see doc]
  - `prompt` (string, REQUIRED, maxLength=20000): Text prompt used to generate the image. Required. Maximum length: 20000 characters.
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9","auto"], default="auto"): Generated image aspect ratio. Default value: `auto`. Use `auto` to let the system choose the aspect ratio automatically.

#### `seedream/4.5-text-to-image` (Seedream4.5 - Text to Image)
- Doc: https://docs.kie.ai/market/seedream/4-5-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=3000): A text description of the image you want to generate (Max length: 3000 characters)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","2:3","3:2","21:9"], default="1:1"): Width-height ratio of the image, determining its visual form.
  - `quality` (string, REQUIRED, enum=["basic","high"], default="basic"): Basic outputs 2K images, while High outputs 4K images.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `seedream/4.5-edit` (Seedream4.5 - Edit)
- Doc: https://docs.kie.ai/market/seedream/4-5-edit
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=3000): A text description of the image you want to generate (Max length: 3000 characters)
  - `image_urls` (array, REQUIRED, maxItems=14): Upload an image file to use as input for the API (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 30.0MB)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","2:3","3:2","21:9"], default="1:1"): Width-height ratio of the image, determining its visual form.
  - `quality` (string, REQUIRED, enum=["basic","high"], default="basic"): Basic outputs 2K images, while High outputs 4K images.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]
- Request example from the doc:

```json
{
  "model": "seedream/4.5-edit",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "Keep the model's pose and the flowing shape of the liquid dress unchanged. Change the clothing material from silver metal to completely tran…",
    "image_urls": [
      "https://static.aiquickdraw.com/tools/example/1764851484363_ScV1s2aq.webp"
    ],
    "aspect_ratio": "1:1",
    "quality": "basic",
    "nsfw_checker": true
  }
}
```

#### `seedream/5-pro-text-to-image` (Seedream5.0 Pro - Text to Image)
- Doc: https://docs.kie.ai/market/seedream/5-pro-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): A text description of the image you want to generate (Max length: 3-5000 characters)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","2:3","3:2","21:9"], default="1:1"): Width-height ratio of the image, determining its visual form.
  - `quality` (string, REQUIRED, enum=["basic","high"], default="basic"): Basic outputs 1K images, while High outputs 2K images.
  - `output_format` (string, enum=["png","jpeg"], default="png"): Format of the output image
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `seedream/5-pro-image-to-image` (Seedream5.0 Pro - Image to Image)
- Doc: https://docs.kie.ai/market/seedream/5-pro-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): A text description of the image you want to generate (Max length: 3-5000 characters)
  - `image_urls` (array, REQUIRED, maxItems=10): Upload an image file to use as input for the API (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 30.0MB)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","2:3","3:2","21:9"], default="1:1"): Width-height ratio of the image, determining its visual form.
  - `quality` (string, REQUIRED, enum=["basic","high"], default="basic"): Basic outputs 1K images, while High outputs 2K images.
  - `output_format` (string, enum=["png","jpeg"], default="png"): Format of the output image
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `seedream/5-lite-text-to-image` (Seedream5.0 Lite - Text to Image)
- Doc: https://docs.kie.ai/market/seedream/5-lite-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=3000): A text description of the image you want to generate (Max length: 3-3000 characters)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","2:3","3:2","21:9"], default="1:1"): Width-height ratio of the image, determining its visual form.
  - `quality` (string, REQUIRED, enum=["basic","high","ultra"], default="basic"): Basic outputs 2K images, while High outputs 3K images, and Ultra outputs 4K images.
  - `output_format` (string, enum=["png","jpeg"], default="png"): Format of the output image
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `seedream/5-lite-image-to-image` (Seedream5.0 Lite - Image to Image)
- Doc: https://docs.kie.ai/market/seedream-5-lite-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=3000): A text description of the image you want to generate (Max length: 3-3000 characters)
  - `image_urls` (array, REQUIRED, maxItems=14): Upload an image file to use as input for the API (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 30.0MB)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","2:3","3:2","21:9"], default="1:1"): Width-height ratio of the image, determining its visual form.
  - `quality` (string, REQUIRED, enum=["basic","high","ultra"], default="basic"): Basic outputs 2K images, while High outputs 3K images, and Ultra outputs 4K images.
  - `output_format` (string, enum=["png","jpeg"], default="png"): Format of the output image
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `seedream/5-flash-image-to-image` (Seedream5.0 Flash - Image to Image)
- Doc: https://docs.kie.ai/market/seedream/5-flash-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=3, maxLength=5000): A text description of the image you want to generate (Max length: 3-5000 characters)
  - `image_urls` (array, REQUIRED, maxItems=10): Upload an image file to use as input for the API (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 30.0MB)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","2:3","3:2","21:9"], default="1:1"): Width-height ratio of the image, determining its visual form.
  - `size` (string, enum=["1K","1.5K","2K"], default="1K"): Resolution level of the output image.
  - `output_format` (string, enum=["png","jpeg"], default="png"): Format of the output image
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `gpt-image-2-text-to-image` (GPT Image-2 - Text to Image)
- Doc: https://docs.kie.ai/market/gpt/gpt-image-2-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=1, maxLength=20000): Text prompt. Required, maximum 20,000 characters.
  - `aspect_ratio` (string, enum=["auto","1:1","3:2","2:3","4:3","3:4","5:4","4:5","16:9","9:16","2:1","1:2","3:1","1:3","21:9","9:21"]): The aspect ratio of the generated image is set to auto by default. Note: for 2K resolution, the following aspect ratios are not supported: 5:4, 4:5, 3:1, 1:3, and 9:21. for 4K resolution, the following aspect ratios are not suppor …[truncated, see doc]
  - `resolution` (string, enum=["1K","2K","4K"]): Image resolution: Note: Images with a 1:1 aspect ratio cannot be converted to 4K images. Images with the aspect ratio set to "auto" or without a specified aspect ratio parameter will only be converted to 1K images; otherwise, the …[truncated, see doc]
  - `background` (string, enum=["transparent","opaque","auto"]): Image background Note: This parameter is only supported when the resolution is 1K.

#### `gpt-image-2-image-to-image` (GPT Image 2 - Image To Image)
- Doc: https://docs.kie.ai/market/gpt/gpt-image-2-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED): Text prompts, up to 20,000 characters.
  - `input_urls` (array, REQUIRED, maxItems=16): Array of input image URLs.
  - `aspect_ratio` (string, enum=["auto","1:1","3:2","2:3","4:3","3:4","5:4","4:5","16:9","9:16","2:1","1:2","3:1","1:3","21:9","9:21"]): The aspect ratio of the generated image is set to auto by default. Note: for 2K resolution, the following aspect ratios are not supported: 5:4, 4:5, 3:1, 1:3, and 9:21. for 4K resolution, the following aspect ratios are not suppor …[truncated, see doc]
  - `resolution` (string, enum=["1K","2K","4K"]): Image resolution: Note: Images with a 1:1 aspect ratio cannot be converted to 4K images. Images with the aspect ratio set to "auto" or without a specified aspect ratio parameter will only be converted to 1K images; otherwise, the …[truncated, see doc]
  - `background` (string, enum=["transparent","opaque","auto"]): Image background Note: This parameter is only supported when the resolution is 1K.
- Request example from the doc:

```json
{
  "model": "gpt-image-2-image-to-image",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "take a photo with Sam Altman in the conference room",
    "input_urls": [
      "https://static.aiquickdraw.com/tools/example/1776782793756_wrogXTdd.png"
    ],
    "aspect_ratio": "auto"
  }
}
```

#### `gpt-image-2-5-flare-text-to-image` (GPT Image 2.5 Flare - Text to Image)
- Doc: https://docs.kie.ai/market/gpt/gpt-image-2-5-flare-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, minLength=1, maxLength=20000): Text prompt. Required, maximum 20,000 characters.
  - `aspect_ratio` (string, enum=["auto","1:1","3:2","2:3","4:3","3:4","16:9","9:16","21:9","27:16","16:27","9:8","8:9"]): The aspect ratio of the generated image is set to auto by default. The 27:16, 16:27, 9:8 and 8:9 aspect ratios support 1K only. 2K and 4K are available for other aspect ratios.
  - `resolution` (string, enum=["1K","2K","4K"]): Image resolution
  - `background` (string, enum=["transparent","opaque","auto"]): Image background

#### `gpt-image-2-5-flare-image-to-image` (GPT Image 2.5 Flare - Image To Image)
- Doc: https://docs.kie.ai/market/gpt/gpt-image-2-5-flare-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED): Text prompts, up to 20,000 characters.
  - `input_urls` (array, REQUIRED, maxItems=16): Array of input image URLs.
  - `aspect_ratio` (string, enum=["auto","1:1","3:2","2:3","4:3","3:4","16:9","9:16","21:9","27:16","16:27","9:8","8:9"]): The aspect ratio of the generated image is set to auto by default. The 27:16, 16:27, 9:8 and 8:9 aspect ratios support 1K only. 2K and 4K are available for other aspect ratios.
  - `resolution` (string, enum=["1K","2K","4K"]): Image resolution
  - `background` (string, enum=["transparent","opaque","auto"]): Image background

#### `gpt-image/1.5-image-to-image` (GPT Image-1.5 - Image to Image)
- Doc: https://docs.kie.ai/market/gpt-image/1-5-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `input_urls` (array, REQUIRED, maxItems=16): Upload an image file to use as input for the API (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `prompt` (string, REQUIRED): A text description of the image you want to generate
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","2:3","3:2"], default="3:2"): Width-height ratio of the image, determining its visual form.
  - `quality` (string, REQUIRED, enum=["medium","high"], default="medium"): Quality: medium=balanced, high=slow/detailed.

#### `flux-2/pro-text-to-image` (Flux-2 - Pro Text to Image)
- Doc: https://docs.kie.ai/market/flux2/pro-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Must be between 3 and 5000 characters. (Max length: 5000 characters)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","3:2","2:3"], default="1:1"): Aspect ratio for the generated image. Select 'auto' to match the first input image ratio (requires input image).
  - `resolution` (string, REQUIRED, enum=["1K","2K"], default="1K"): Output image resolution.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `flux-2/pro-image-to-image` (Flux-2 - Pro Image to Image)
- Doc: https://docs.kie.ai/market/flux2/pro-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `input_urls` (array, REQUIRED, maxItems=8): Input reference images (1-8 images). (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `prompt` (string, REQUIRED, maxLength=5000): Must be between 3 and 5000 characters. (Max length: 5000 characters)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16","3:2","2:3","auto"], default="1:1"): Aspect ratio for the generated image. Select 'auto' to match the first input image ratio (requires input image).
  - `resolution` (string, REQUIRED, enum=["1K","2K"], default="1K"): Output image resolution.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `qwen2/image-edit` (Qwen2 - Image Edit)
- Doc: https://docs.kie.ai/market/qwen2/image-edit
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=800): The prompt to generate the image with (Max length: 800 characters)
  - `image_url` (string, REQUIRED): The URL of the image to edit. (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `image_size` (string, enum=["1:1","2:3","3:2","3:4","4:3","9:16","16:9","21:9"], default="16:9"): The size of the generated image. Default value: 16:9
  - `seed` (integer): The same seed and the same prompt given to the same version of the model will output the same image every time.
  - `output_format` (string, enum=["jpeg","png"], default="png"): The format of the generated image. Default value: "png"
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `qwen3/pro-image-to-image` (Qwen3 Pro Image to Image)
- Doc: https://docs.kie.ai/market/qwen3-pro/image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `image_urls` (array, REQUIRED, minItems=1, maxItems=3): Input image URL array. Upload images and provide their URLs rather than the file content. Supports up to 3 images. Supported file types: `image/jpeg`, `image/png`, `image/webp`, `image/bmp`, and `image/gif`,`image/tiff`. Maximum f …[truncated, see doc]
  - `prompt` (string, REQUIRED, minLength=0, maxLength=5000): The positive prompt that describes the image content, style, and composition you want to generate or edit. Both Chinese and English are supported.
  - `resolution` (string, enum=["1K","2K"], default="1K"): The output image resolution.
  - `image_size` (string, enum=["1:1","3:2","2:3","4:3","3:4","16:9","9:16","21:9"], default="16:9"): The output image size.
  - `output_format` (string, enum=["png","jpeg"], default="png"): The generated image format.
  - `prompt_extend` (boolean, default=true): Whether to enable intelligent prompt rewriting. Default: true (recommended). When enabled, the model optimizes the positive prompt, which significantly improves results for simple descriptions.
  - `nsfw_checker` (boolean, default=false): Whether to enable content filtering. Optional. Defaults to false. When set to false, content filtering is disabled and all results are returned directly by the model. Note: Content filtering cannot guarantee that all inappropriate …[truncated, see doc]
  - `negative_prompt` (string, minLength=0, maxLength=5000): The negative prompt that describes content you do not want to appear in the image.
  - `seed` (integer, default=1, minimum=0, maximum=2147483647): The random seed. Value range: [0, 2147483647]. A fixed seed helps maintain relatively stable results.

#### `ideogram/character` (Ideogram - Character)
- Doc: https://docs.kie.ai/market/ideogram/character
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): The prompt to fill the masked part of the image. (Max length: 5000 characters)
  - `reference_image_urls` (array, REQUIRED): A set of images to use as character references. Currently only 1 image is supported, rest will be ignored. (maximum total size 10MB across all character references). The images should be in JPEG, PNG or WebP format (File URL after …[truncated, see doc]
  - `rendering_speed` (string, enum=["TURBO","BALANCED","QUALITY"], default="BALANCED"): The rendering speed to use. Default value: "BALANCED"
  - `style` (string, enum=["AUTO","REALISTIC","FICTION"], default="AUTO"): The style type to generate with. Cannot be used with style_codes. Default value: "AUTO"
  - `expand_prompt` (boolean): Determine if MagicPrompt should be used in generating the request or not. Default value: true (Boolean value (true/false))
  - `num_images` (string, enum=["1","2","3","4"], default="1"): Select description
  - `image_size` (string, enum=["square","square_hd","portrait_4_3","portrait_16_9","landscape_4_3","landscape_16_9"], default="square_hd"): The resolution of the generated image Default value: square_hd
  - `seed` (integer): Seed for the random number generator
  - `negative_prompt` (string, maxLength=5000): Description of what to exclude from an image. Descriptions in the prompt take precedence to descriptions in the negative prompt. Default value: "" (Max length: 5000 characters)

#### `wan/2-7-image-pro` (Wan 2.7 Image Pro)
- Doc: https://docs.kie.ai/market/wan/2-7-image-pro
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=5000): Prompt for image generation or editing. This field supports both Chinese and English, with a maximum length of 5000 characters as per Alibaba Cloud documentation.
  - `input_urls` (array, maxItems=9): (Optional) Array of input image URLs. The current project uses `input_urls` as a wrapper field.
  - `aspect_ratio` (string, enum=["1:1","16:9","4:3","21:9","3:4","9:16","8:1","1:8"]): (Optional) Output aspect ratio when no image input is provided.
  - `enable_sequential` (boolean, default=false): Whether to enable sequential/group image mode. Default is false.
  - `n` (integer): Number of images to generate. Range is 1-4 when `enable_sequential=false` (default: 4); range is 1-12 when `enable_sequential=true` (default: 12).
  - `resolution` (string, enum=["1K","2K","4K"], default="2K"): Output resolution. The current project uses `resolution` as a wrapper field corresponding to the underlying resolution parameter.(4K generation is available only for text-to-image in Standard Mode)
  - `thinking_mode` (boolean, default=false): Whether to enable thinking mode. Only available when `enable_sequential=false` and `input_urls` is empty; the frontend will automatically disable it in other cases.
  - `color_palette` (array, minItems=3, maxItems=10): (Optional) Custom color theme. Only available when `enable_sequential=false`. Requires 3-10 colors, 8 recommended.
  - `color_palette[].hex` (string, REQUIRED): HEX color value.
  - `color_palette[].ratio` (string, REQUIRED): Color proportion, format must be xx.xx%.
  - `bbox_list` (array): (Optional) Interactive editing bounding box areas. The outer list length should match `input_urls`; maximum 2 boxes per image; single box format is `[x1, y1, x2, y2]`.
  - `bbox_list[]` (array, maxItems=2)
  - `bbox_list[][]` (array, minItems=4, maxItems=4)
  - `watermark` (boolean, default=false): Whether to add watermark.
  - `seed` (integer, default=0, minimum=0, maximum=2147483647): Random seed, range 0-2147483647.
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `z-image` (Z-Image)
- Doc: https://docs.kie.ai/market/z-image/z-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED, maxLength=1000): A text description of the image you want to generate (Max length: 1000 characters)
  - `aspect_ratio` (string, REQUIRED, enum=["1:1","4:3","3:4","16:9","9:16"], default="1:1"): Aspect ratio for the generated image. Select 'auto' to match the first input image ratio (requires input image).
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything ca …[truncated, see doc]

#### `4o-image-api` (Generate 4o Image)
- Doc: https://docs.kie.ai/4o-image-api/generate-4-o-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string): (Optional) Text prompt that conveys the creative idea you want the 4o model to render. Required if neither `files_url` nor `file_url` is supplied. At least one of `prompt` or `files_url` must be provided.
  - `files_url` (array): (Optional) Up to 5 publicly reachable image URLs to serve as reference or source material. Use this when you want to edit or build upon an existing picture. If you don’t have reliable hosting, upload your images first via our File …[truncated, see doc]
  - `size` (string, REQUIRED, enum=["1:1","3:2","2:3"]): (Required) Aspect ratio of the generated image. Must be one of the listed values.
  - `file_url` (string, format=uri): (Optional, Deprecated) File URL, such as an image URL. If file_url is provided, 4o image may create based on this image. This parameter will be deprecated in the future, please use files_url instead.

#### `flux1-kontext` (Generate or Edit Image)
- Doc: https://docs.kie.ai/flux-kontext-api/generate-or-edit-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `prompt` (string, REQUIRED): Text prompt describing the desired image or edit. Required for both generation and editing modes. - Should be detailed and specific - For image editing, describe the desired changes - For image generation, describe the complete sc …[truncated, see doc]
  - `enable_translation` (boolean): Whether to enable automatic translation feature. - Since prompt only supports English, when this parameter is true, the system will automatically translate non-English prompts to English - If your prompt is already in English, you …[truncated, see doc]
  - `upload_cn` (boolean): (Optional) Specifies the server region for image upload. Set to true to use servers in China, false to use non-China servers. Choose based on your geographical location for optimal upload speeds.
  - `input_image` (string, format=uri): URL of the input image for editing mode. Required when editing an existing image. - Must be a valid image URL - Image must be accessible to the API server
  - `aspect_ratio` (string, enum=["21:9","16:9","4:3","1:1","3:4","9:16"], default="16:9"): Output image aspect ratio. You Applicable in both text-to-image generation and image editing modes. For **text-to-image generation** , the output image will follow the specified aspect ratio. For **image editing** , if aspectRatio …[truncated, see doc]
  - `output_format` (string, enum=["jpeg","png"], default="jpeg"): Output image format.
  - `prompt_upsampling` (boolean, default=false): - If true, performs upsampling on the prompt - May increase processing time
  - `safety_tolerance` (integer, enum=[0,1,2,3,4,5,6], default=2): **For Image Generation Mode:** Moderation level for inputs and outputs. Value ranges from 0 (most strict) to 6 (more permissive). **For Image Editing Mode:** Moderation level for inputs and outputs. Value ranges from 0 (most stric …[truncated, see doc]
  - `watermark` (string): Watermark identifier to add to the generated image. - Optional - If provided, a watermark will be added to the output image

#### `gpt-image-2-5-sunburst-image-to-image` (GPT Image 2.5 Sunburst - Image To Image)
- Doc: https://docs.kie.ai/market/gpt/gpt-image-2-5-sunburst-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `gpt-image-2-5-flare-image-to-image` (no field differences in the docs).

#### `gpt-image-2-5-sunburst-text-to-image` (GPT Image 2.5 Sunburst - Text to Image)
- Doc: https://docs.kie.ai/market/gpt/gpt-image-2-5-sunburst-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `gpt-image-2-5-flare-text-to-image` (no field differences in the docs).

#### `flux-2/flex-image-to-image` (Flux-2 - Image to Image)
- Doc: https://docs.kie.ai/market/flux2/flex-image-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `flux-2/pro-image-to-image` (no field differences in the docs).

#### `flux-2/flex-text-to-image` (Flux-2 - Text to Image)
- Doc: https://docs.kie.ai/market/flux2/flex-text-to-image
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `flux-2/pro-text-to-image` (no field differences in the docs).

#### `ideogram/character-edit` (Ideogram - Character Edit)
- Doc: https://docs.kie.ai/market/ideogram/character-edit
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `ideogram/character` except: lacks `image_size`; adds `image_url` (string | REQUIRED); adds `mask_url` (string | REQUIRED); lacks `negative_prompt`.

#### `ideogram/character-remix` (Ideogram - Character Remix)
- Doc: https://docs.kie.ai/market/ideogram/character-remix
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `ideogram/character` except: adds `image_url` (string | REQUIRED); adds `image_urls` (array); `negative_prompt` is (string, maxLength=500) instead of (string, maxLength=5000); `prompt` is (string, REQUIRED, maxLength=5000, examples=["A fisheye lens selfie photograph taken at night on an urban street. The image is circular with a black border and shows a person wearing dark sunglasses and a black jacket, holding a silver digital camera up to capture the reflection. The background shows a row of shuttered storefronts with red neon lighting visible in the upper portion. The street is empty and dark, with street lights creating a warm glow along the sidewalk. The fisheye effect creates a curved, distorted perspective that bends the straight lines of the street and buildings. The lighting is predominantly red and dark, creating a moody urban atmosphere. The person's reflection shows long dark hair and is positioned in the c...(trunc)) instead of (string, REQUIRED, maxLength=5000); adds `reference_mask_urls` (string); adds `strength` (number | default=0.8 | minimum=0.1 | maximum=1).


### A.7 Utility and finishing models

#### `topaz/video-upscale` (Topaz - Video Upscale)
- Doc: https://docs.kie.ai/market/topaz/video-upscale
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `video_url` (string, REQUIRED): URL of the video to upscale (File URL after upload, not file content; Accepted types: video/mp4, video/quicktime, video/x-matroska; Max size: 50.0MB)
  - `upscale_factor` (string, enum=["1","2","4"], default="2"): Factor to upscale the video by (e.g. 2.0 doubles width and height)
- Request example from the doc:

```json
{
  "model": "topaz/video-upscale",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "video_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1758166466095hvbwkrpw.mp4",
    "upscale_factor": "2"
  }
}
```

#### `topaz/image-upscale` (Topaz - Image Upscale)
- Doc: https://docs.kie.ai/market/topaz/image-upscale
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `image_url` (string, REQUIRED): Url of the image to be upscaled (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `upscale_factor` (string, REQUIRED, enum=["1","2","4"], default="2"): Factor to upscale the video by (e.g. 2.0 doubles width and height)
- Request example from the doc:

```json
{
  "model": "topaz/image-upscale",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "image_url": "https://static.aiquickdraw.com/tools/example/1762752805607_mErUj1KR.png",
    "upscale_factor": "2"
  }
}
```

#### `recraft/remove-background` (Recraft - Remove Background)
- Doc: https://docs.kie.ai/market/recraft/remove-background
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `image` (string, REQUIRED): Image to remove background from. Supported formats: PNG, JPG, WEBP. Max 5MB, max 16MP, max dimension 4096px, min dimension 256px. (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 5.0MB)
- Request example from the doc:

```json
{
  "model": "recraft/remove-background",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "image": "https://file.aiquickdraw.com/custom-page/akr/section-images/1757057285447k9qcbki1.webp"
  }
}
```

#### `recraft/crisp-upscale` (Recraft - Crisp Upscale)
- Doc: https://docs.kie.ai/market/recraft/crisp-upscale
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `image` (string, REQUIRED): Image to upscale (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
- Request example from the doc:

```json
{
  "model": "recraft/crisp-upscale",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "image": "https://file.aiquickdraw.com/custom-page/akr/section-images/1757169577325ijj8vwvt.jpg"
  }
}
```

#### `wan/2-2-animate-move` (Wan - Animate Move)
- Doc: https://docs.kie.ai/market/wan/2-2-animate-move
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Params:
  - `video_url` (string, REQUIRED): URL of the input video. (File URL after upload, not file content; Accepted types: video/mp4, video/quicktime, video/x-matroska; Max size: 10.0MB)
  - `image_url` (string, REQUIRED): URL of the input image. If the input image does not match the chosen aspect ratio, it is resized and center cropped. (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB)
  - `resolution` (string, enum=["480p","580p","720p"], default="480p"): Resolution of the generated video (480p, 580p, or 720p).
  - `nsfw_checker` (boolean): Defaults to false. You can set it to false based on your needs. If set to false, our content filtering will be disabled, and all results will be returned directly by the model itself. Note: There is no guarantee that everything can be filtered out; if you are not satisfied with the results, you will need to make your own arrangements.
- Request example from the doc:

```json
{
  "model": "wan/2-2-animate-move",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "video_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/17586254974931y2hottk.mp4",
    "image_url": "https://file.aiquickdraw.com/custom-page/akr/section-images/1758625466310wpehpbnf.png",
    "resolution": "480p",
    "nsfw_checker": false
  }
}
```

#### `wan/2-2-animate-replace` (Wan - Animate Replace)
- Doc: https://docs.kie.ai/market/wan/2-2-animate-replace
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Schema: same fields as `wan/2-2-animate-move` (no field differences in the docs).

#### `kling-3.0/motion-control` (Kling-3.0 motion-control)
- Doc: https://docs.kie.ai/market/kling/motion-control-v3
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## File Upload Requirements
  > 
  > Before using the Motion Control API, you need to upload your image and video files:
  > 
  > <Steps>
  > <Step title="Upload Reference Image">
  >   Use the File Upload API to upload your reference image showing the subject.
  > 
  >   
  > 
  >   **Requirements:**
  >   - **File Type**: JPEG, PNG, or JPG format
  >   - **Max File Size**: 10MB per file, size needs to be greater than 340px, aspect ratio 2:5 to 5:2.
  >   - **Content**: Clear image showing the subject's head, shoulders, and torso
  > </Step>
  > 
  > <Step title="Upload Motion Video">
  >   Upload a video that defines the motion pattern you want to apply.
  > 
  >   **Requirements:**
  >   - **File Type**: MP4, or QuickTime format
  >   - **Duration**: Between 3-30 seconds
  > …[doc prose truncated, see doc]

- Params:
  - `prompt` (string): (Optional) Text prompt words, used to guide the generation of animation content. Can be empty or 0 - 2500 characters long.
  - `input_urls` (array, REQUIRED): (Required) Include a URL of an image
  - `video_urls` (array, REQUIRED): (Required) Include a video URL
  - `mode` (string): (Optional) Video Quality Mode. std: Standard Mode (720p). pro: Professional Mode (1080p)
  - `character_orientation` (string): (Optional) Reference source for character orientation. video: Refer to video (recommended); image: Refer to image. Default value: video
  - `background_source` (string): (Optional) Background source. input_video: Use video background; input_image: Use image background. Default value: input_video
- Request example from the doc:

```json
{
  "model": "kling-3.0/motion-control",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "The cartoon character is dancing.",
    "input_urls": [
      "https://static.aiquickdraw.com/tools/example/1767694885407_pObJoMcy.png"
    ],
    "video_urls": [
      "https://static.aiquickdraw.com/tools/example/1767525918769_QyvTNib2.mp4"
    ],
    "mode": "720p",
    "character_orientation": "image",
    "background_source": "input_video"
  }
}
```

#### `kling-2.6/motion-control` (Kling 2.6 motion-control)
- Doc: https://docs.kie.ai/market/kling/motion-control
- Endpoint: `POST https://api.kie.ai/api/v1/jobs/createTask`
- Doc prose:

  > ## File Upload Requirements
  > 
  > Before using the Motion Control API, you need to upload your image and video files:
  > 
  > <Steps>
  > <Step title="Upload Reference Image">
  >   Use the File Upload API to upload your reference image showing the subject.
  > 
  >   
  > 
  >   **Requirements:**
  >   - **File Type**: JPEG, PNG, or JPG format
  >   - **Max File Size**: 10MB per file
  >   - **Content**: Clear image showing the subject's head, shoulders, and torso
  > </Step>
  > 
  > <Step title="Upload Motion Video">
  >   Upload a video that defines the motion pattern you want to apply.
  > 
  >   **Requirements:**
  >   - **File Type**: MP4 or QuickTime format
  >   - **Duration**: Between 3-30 seconds per video
  >   - **Max File Size**: 100MB per file
  >   - **Content**
  > …[doc prose truncated, see doc]

- Params:
  - `prompt` (string, maxLength=2500): A text description of the desired output. Maximum length is 2500 characters. (Max length: 2500 characters)
  - `input_urls` (array, REQUIRED, maxItems=1): An array containing a single image URL. The photo must clearly show the subject's head, shoulders, and torso. (File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/jpg; Max size: 10.0MB,size needs to be greater than 300px, aspect ratio 2:5 to 5:2.)
  - `video_urls` (array, REQUIRED, maxItems=1): An array containing a single video URL. The duration must be between 3 to 30 seconds, and the video must clearly show the subject's head, shoulders, and torso. (File URL after upload, not file content; Accepted types: video/mp4, video/quicktime; Max size: 100.0MB)
  - `character_orientation` (string, REQUIRED, enum=["image","video"], default="video"): Generate the orientation of the characters in the video. 'image': same orientation as the person in the picture (max 10s video). 'video': consistent with the orientation of the characters in the video (max 30s video).
  - `mode` (string, REQUIRED, enum=["720p","1080p"], default="720p"): Output resolution mode. Use 'std' for 720p or 'pro' for 1080p.
- Request example from the doc:

```json
{
  "model": "kling-2.6/motion-control",
  "callBackUrl": "https://your-domain.com/api/callback",
  "input": {
    "prompt": "The cartoon character is dancing.",
    "input_urls": [
      "https://static.aiquickdraw.com/tools/example/1767694885407_pObJoMcy.png"
    ],
    "video_urls": [
      "https://static.aiquickdraw.com/tools/example/1767525918769_QyvTNib2.mp4"
    ],
    "mode": "720p",
    "character_orientation": "image"
  }
}
```


---

## Appendix B. Kie price list (video, music, image), pulled 2026-10-04

Source: `POST https://api.kie.ai/client/v1/model-pricing/page`. Labels are Kie's own, typos included. 1 credit = $0.005. Chat model rows are left out.

**image / Alibaba**

- Qwen image 3.0 Pro, input, 1K: 0.5 credits per image ($0.0025)
- Qwen image 3.0 Pro, input, 2K: 0.5 credits per image ($0.0025)
- Qwen image 3.0 Pro, output, 1K: 6.4 credits per image ($0.032)
- Qwen image 3.0 Pro, output, 2K: 12 credits per image ($0.06)
- Qwen image 3.0 Pro, text to image, 1K: 6.4 credits per image ($0.032)
- Qwen image 3.0 Pro, text to image, 2K: 12 credits per image ($0.06)
- Qwen image 3.0, input, 1K: 0.5 credits per image ($0.0025)
- Qwen image 3.0, input, 2K: 0.5 credits per image ($0.0025)
- Qwen image 3.0, output, 1K: 4.8 credits per image ($0.024)
- Qwen image 3.0, output, 2K: 4.8 credits per image ($0.024)
- Qwen image 3.0, text to image, 1K: 4.8 credits per image ($0.024)
- Qwen image 3.0, text to image, 2K: 4.8 credits per image ($0.024)
- Qwen-Image-2.1, image to image, 1K: 4 credits per image ($0.02)
- Qwen-Image-2.1, image to image, 2K: 8 credits per image ($0.04)
- Qwen-Image-2.1, text to image, 1K: 4 credits per image ($0.02)
- Qwen-Image-2.1, text to image, 2K: 8 credits per image ($0.04)

**image / Black Forest Labs**

- Black Forest Labs Flux 2 Flex, image to image, 1.0s-1K: 14.0 credits per image ($0.07)
- Black Forest Labs Flux 2 Flex, image to image, 1.0s-2K: 24.0 credits per image ($0.12)
- Black Forest Labs Flux 2 Flex, text to image, 1.0s-1K: 14 credits per image ($0.07)
- Black Forest Labs Flux 2 Flex, text to image, 1.0s-2K: 24 credits per image ($0.12)
- Black Forest Labs flux-2 pro, image to image, 1.0s-1K: 5.0 credits per image ($0.025)
- Black Forest Labs flux-2 pro, image to image, 1.0s-2K: 7.0 credits per image ($0.035)
- Black Forest Labs flux-2 pro, text-to-image, 1.0s-1K: 5.0 credits per image ($0.025)
- Black Forest Labs flux-2 pro, text-to-image, 1.0s-2K: 7.0 credits per image ($0.035)
- Black Forest Labs flux1-kontext, text-to-image, Max: 10.0 credits per image ($0.05)
- Black Forest Labs flux1-kontext, text-to-image, Pro: 5.0 credits per image ($0.025)

**image / ByteDance**

- seedream 4.5, image-to-image: 6.5 credits per image ($0.0325)
- seedream 4.5, text-to-image: 6.5 credits per image ($0.0325)
- seedream 5 Flash, Image to image , 1K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, Image to image, 1.5K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, Image to image, 2K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, Text to image , 1K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, Text to image, 1.5K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, Text to image, 2K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, layer-decomposition, 1.5K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, layer-decomposition, 1K: 3.24 credits per image ($0.0162)
- seedream 5 Flash, layer-decomposition, 2K: 3.24 credits per image ($0.0162)
- seedream 5 Pro, Layer Decomposition, 1.5K: 7 credits per image ($0.035)
- seedream 5 Pro, Layer Decomposition, 1K: 7 credits per image ($0.035)
- seedream 5 Pro, Layer Decomposition, 2K: 14 credits  ($0.07)
- seedream 5 Pro, image-to-image, 1K: 7 credits per image ($0.035)
- seedream 5 Pro, image-to-image, 2K: 14 credits per image ($0.07)
- seedream 5 Pro, input image, First image free: 0.5 credits per image ($0.0025)
- seedream 5 Pro, text-to-image, 1K: 7 credits per image ($0.035)
- seedream 5 Pro, text-to-image, 2K: 14 credits per image ($0.07)
- seedream 5.0 Lite, image-to-image: 5.5 credits per image ($0.0275)
- seedream 5.0 Lite, text-to-image: 5.5 credits per image ($0.0275)

**image / Google**

- Google nano banana 2, 1K: 8 credits per image ($0.04)
- Google nano banana 2, 2K: 12 credits per image ($0.06)
- Google nano banana 2, 4K: 18 credits per image ($0.09)
- Google nano banana edit, image-to-image: 4.0 credits per image ($0.02)
- Google nano banana pro, 1/2K: 18.0 credits per image ($0.09)
- Google nano banana pro, 4K: 24.0 credits per image ($0.12)
- Google nano banana, text-to-image: 4.0 credits per image ($0.02)
- google imagen4, text-to-image, Fast: 4.0 credits per request ($0.02)
- google imagen4, text-to-image, Ultra: 12.0 credits per image ($0.06)
- google imagen4, text-to-image, default: 8.0 credits per request ($0.04)
- nano-banana-2-lite, 1k: 4 credits per image ($0.02)

**image / Grok**

- grok-imagine, image-to-image: 4 credits per generation ($0.02)
- grok-imagine, text-to-image: 4.0 credits per 2 images ($0.02)
- grok-imagine, text-to-image(quality): 5 credits per generation ($0.025)
- grok-imagine-image-2-0, Image Edit: 4 credits per image ($0.02)
- grok-imagine-image-2-0, Text to Image: 4 credits per image ($0.02)

**image / Ideogram**

- Ideogram V3 Reframe, image to image, Balanced: 7.0 credits per image ($0.035)
- Ideogram V3 Reframe, image to image, Quality: 10.0 credits per image ($0.05)
- Ideogram V3 Reframe, image to image, Turbo: 3.5 credits per image ($0.0175)
- ideogram character, image-to-image, BALANCED: 18.0 credits per image ($0.09)
- ideogram character, image-to-image, QUALITY: 24.0 credits per image ($0.12)
- ideogram character, image-to-image, TURBO: 12.0 credits per image ($0.06)
- ideogram character-edit, image-to-image, BALANCED: 18.0 credits per image ($0.09)
- ideogram character-edit, image-to-image, QUALITY: 24.0 credits per image ($0.12)
- ideogram character-edit, image-to-image, TURBO: 12.0 credits per image ($0.06)
- ideogram character-remix, image-to-image, BALANCED: 18.0 credits per image ($0.09)
- ideogram character-remix, image-to-image, QUALITY: 24.0 credits per image ($0.12)
- ideogram character-remix, image-to-image, TURBO: 12.0 credits per image ($0.06)
- ideogram v3,  text-to-image, BALANCED: 7.0 credits per image ($0.035)
- ideogram v3,  text-to-image, QUALITY: 10.0 credits per image ($0.05)
- ideogram v3,  text-to-image, TURBO: 3.5 credits per image ($0.0175)
- ideogram v3-edit, image-to-image, BALANCED: 7.0 credits per image ($0.035)
- ideogram v3-edit, image-to-image, QUALITY: 10.0 credits per image ($0.05)
- ideogram v3-edit, image-to-image, TURBO: 3.5 credits per image ($0.0175)
- ideogram v3-remix, image-to-image, BALANCED: 7.0 credits per image ($0.035)
- ideogram v3-remix, image-to-image, QUALITY: 10.0 credits per image ($0.05)
- ideogram v3-remix, image-to-image, TURBO: 3.5 credits per image ($0.0175)

**image / OpenAI**

- gpt image 1.5, image-to-image, high: 22.0 credits per image ($0.11)
- gpt image 1.5, image-to-image, medium: 4.0 credits per image ($0.02)
- gpt image 1.5, text-to-image, high: 22.0 credits per image ($0.11)
- gpt image 1.5, text-to-image, medium: 4.0 credits per image ($0.02)
- gpt image 2, image-to-image, 1k: 6 credits per image ($0.03)
- gpt image 2, image-to-image, 2k: 10 credits per image ($0.05)
- gpt image 2, image-to-image, 4k: 16 credits per image ($0.08)
- gpt image 2, text-to-image, 1k: 6 credits per image ($0.03)
- gpt image 2, text-to-image, 2k: 10 credits per image ($0.05)
- gpt image 2, text-to-image, 4k: 16 credits per image ($0.08)
- gpt-image-2-5-flare, image-to-image, 1K: 6 credits per image ($0.03)
- gpt-image-2-5-flare, image-to-image, 2K: 10 credits per image ($0.05)
- gpt-image-2-5-flare, image-to-image, 4K: 16 credits per image ($0.08)
- gpt-image-2-5-flare, text-to-image, 1K: 6 credits per image ($0.03)
- gpt-image-2-5-flare, text-to-image, 2K: 10 credits per image ($0.05)
- gpt-image-2-5-flare, text-to-image, 4K: 16 credits per image ($0.08)
- gpt-image-2-5-sunburst, image-to-image, 1K: 6 credits per image ($0.03)
- gpt-image-2-5-sunburst, image-to-image, 2K: 10 credits per image ($0.05)
- gpt-image-2-5-sunburst, image-to-image, 4K: 16 credits per image ($0.08)
- gpt-image-2-5-sunburst, text-to-image, 1K: 6 credits per image ($0.03)
- gpt-image-2-5-sunburst, text-to-image, 2K: 10 credits per image ($0.05)
- gpt-image-2-5-sunburst, text-to-image, 4K: 16 credits per image ($0.08)

**image / OpenAI 4o**

- OpenAI 4o image, text-to-image: 6.0 credits per image ($0.03)

**image / Qwen**

- Qwen Image , text-to-image: 4.0 credits per megapixel ($0.02)
- Qwen Image, image-to-image: 4.0 credits per megapixel ($0.02)
- Qwen image-edit, image-to-image: 5.0 credits per megapixel ($0.03)
- Qwen z-image, text-to-image, 1.0s: 0.8 credits per image ($0.004)
- Qwen2 - Image edit, image-to-image: 5.6 credits per image ($0.028)
- Qwen2 - Image edit, text-to-image: 5.6 credits per image ($0.028)

**image / Recraft**

- Recraft Crisp Upscale, image to image: 0.5 credits per image ($0.0025)
- Recraft Remove Background , image to image: 1.0 credits per image ($0.005)

**image / Topaz**

- Topaz Image Upscaler, image-upscale, 2K: 10.0 credits per image ($0.05)
- Topaz Image Upscaler, image-upscale, 4K: 20.0 credits per image ($0.1)

**image / Wan**

- wan 2.7 image: 4.8 credits per image ($0.024)
- wan 2.7 image pro: 12 credits per image ($0.06)

**music / Elevenlabs**

- Elevenlabs Text to Speech, multilingual v2: 12.0 credits per 1000 characters ($0.06)
- Elevenlabs Text to Speech, turbo 2.5: 6.0 credits per 1000 characters ($0.03)
- Elevenlabs V3 , Text to dialogue: 14 credits per 1000 characters ($0.07)

**music / Google**

- Gemini 2.5 Pro TTS, Text to Speech, Audio Output: 2800 credits per million tokens ($14)
- Gemini 2.5 Pro TTS, Text to Speech, Input: 140 credits per million tokens ($0.7)
- Gemini 3.1 Flash TTS, Text to Speech, Audio Output: 2800 credits per million tokens ($14)
- Gemini 3.1 Flash TTS, Text to Speech, input: 140 credits per million tokens ($0.7)
- Gemini 3.8 Flash TTS, Text to Speech, Audio Output: 1260 credits per million tokens ($6.30)
- Gemini 3.8 Flash TTS, Text to Speech, Input: 70 credits per million tokens ($0.35)
- Gemini 3.8 Flash-Lite TTS, Text to Speech, Audio Output: 840 credits per million tokens ($4.20)
- Gemini 3.8 Flash-Lite TTS, Text to speech, Input: 70 credits per million tokens ($0.35)

**music / Suno**

- Suno, Advanced Split: 20 credits per request ($0.1)
- Suno, Boost Music Style Boost: 0.4 credits per request ($0.002)
- Suno, Cover Generate: 0 credits per request ($0)
- Suno, Extend Music: 12.0 credits per request ($0.06)
- Suno, Generate Lyrics: 0.4 credits per request ($0.002)
- Suno, Generate Midi From Audio: 0 credits per request ($0)
- Suno, Generate Music: 12.0 credits per request ($0.06)
- Suno, Generate Persona: 0 credits per request ($0)
- Suno, Generate sounds: 2.5 credits per request ($0.0125)
- Suno, Mashup: 12 credits per request ($0.06)
- Suno, Multi-Stem Separation, without stemName: 50 credits per request ($0.25)
- Suno, Replace Music Section: 5 credits per request ($0.025)
- Suno, TimeStamped Lyrics: 0.5 credits per request ($0.0025)
- Suno, Vocal  Separate: 10 credits per request ($0.05)
- Suno, add-instrumental: 12.0 credits per request ($0.06)
- Suno, add-vocals: 12.0 credits per request ($0.06)
- Suno, convert-to-wav-format: 0.4 credits per request ($0.002)
- Suno, create-music-video: 2.0 credits per request ($0.01)
- Suno, upload-and-cover-audio: 12.0 credits per request ($0.06)
- Suno, upload-and-extend-audio: 12.0 credits per request ($0.06)

**video / Alibaba**

- HappyHorse-1.0, image-to-video, 1080p: 48 credits per second ($0.24)
- HappyHorse-1.0, image-to-video, 720p: 28 credits per second ($0.14)
- HappyHorse-1.0, reference-to-video, 1080p: 48 credits per second ($0.24)
- HappyHorse-1.0, reference-to-video, 720p: 28 credits per second ($0.14)
- HappyHorse-1.0, text-to-video, 1080p: 48 credits per second ($0.24)
- HappyHorse-1.0, text-to-video, 720p: 28 credits per second ($0.14)
- HappyHorse-1.0, video-edit, 1080p: 48 credits per second ($0.24)
- HappyHorse-1.0, video-edit, 720p: 28 credits per second ($0.14)
- HappyHorse-1.1, image-to-video, 1080p: 29 credits per second ($0.145)
- HappyHorse-1.1, image-to-video, 720p: 22.5 credits per second ($0.1125)
- HappyHorse-1.1, reference-to-video, 1080p: 29 credits per second ($0.145)
- HappyHorse-1.1, reference-to-video, 720p: 22.5 credits per second ($0.1125)
- HappyHorse-1.1, text-to-video, 1080p: 29 credits per second ($0.145)
- HappyHorse-1.1, text-to-video, 720p: 22.5 credits per second ($0.1125)

**video / ByteDance**

- bytedance/seedance-1.5-pro, with audio-1080p: 15 credits per second ($0.075)
- bytedance/seedance-1.5-pro, with audio-480p: 3.5 credits per second ($0.0175)
- bytedance/seedance-1.5-pro, with audio-720p: 7 credits per second ($0.035)
- bytedance/seedance-1.5-pro, without audio-1080p: 7.5 credits per second ($0.0375)
- bytedance/seedance-1.5-pro, without audio-480p: 1.75 credits per second ($0.00875)
- bytedance/seedance-1.5-pro, without audio-720p: 3.5 credits per second ($0.0175)
- bytedance/seedance-2 fast, 480p no video input: 11.7 credits per second ($0.059)
- bytedance/seedance-2 fast, 480p with video input: 6.8 credits per second ($0.034)
- bytedance/seedance-2 fast, 720p no video input: 24.8 credits per second ($0.124)
- bytedance/seedance-2 fast, 720p with video input: 15 credits per second ($0.075)
- bytedance/seedance-2, 1080p no video input: 102 credits per second ($0.51)
- bytedance/seedance-2, 1080p with video input: 62 credits per second ($0.31)
- bytedance/seedance-2, 480p no video input: 19 credits per second ($0.095)
- bytedance/seedance-2, 480p with video input: 11.5 credits per second ($0.057)
- bytedance/seedance-2, 4K no video input: 208 credits per second ($1.04)
- bytedance/seedance-2, 4K with video input: 128 credits per second ($0.64)
- bytedance/seedance-2, 720p no video input: 41 credits per second ($0.205)
- bytedance/seedance-2, 720p with video input: 25 credits per second ($0.125)
- bytedance/seedance-2-5, 1080p no video: 158 credits per second ($0.79)
- bytedance/seedance-2-5, 1080p with video: 95 credits per second ($0.475)
- bytedance/seedance-2-5, 480p no video: 28 credits per second ($0.140)
- bytedance/seedance-2-5, 480p with video: 17 credits per second ($0.085)
- bytedance/seedance-2-5, 720p no video: 63 credits per second ($0.315)
- bytedance/seedance-2-5, 720p with video: 38 credits per second ($0.190)
- bytedance/seedance-2-mini, 480P no video: 3.8 credits per second ($0.019)
- bytedance/seedance-2-mini, 480P with video: 2.4 credits per second ($0.012)
- bytedance/seedance-2-mini, 720P no video: 8.2 credits per second ($0.041)
- bytedance/seedance-2-mini, 720P with video: 5 credits per second ($0.025)
- omnihuman-1-5, lip sync: 27 credits per second ($0.135)
- volcengine , lip sync: 8 credits per second ($0.04)

**video / Google**

- Google veo 3.1, Extend, Fast: 60 credits per video ($0.30)
- Google veo 3.1, Extend, Lite: 30 credits per vedio ($0.15)
- Google veo 3.1, Extend, Quality: 250 credits per video ($1.25)
- Google veo 3.1, Get 1080P Video: 5 credits per video ($0.025)
- Google veo 3.1, Get 4K Video: 120.0 credits per video ($0.6)
- Google veo 3.1, image-to-video, Fast-1080p: 65 credits per video ($0.325)
- Google veo 3.1, image-to-video, Fast-4K: 180 credits per video ($0.90)
- Google veo 3.1, image-to-video, Fast-720p: 60 credits per video ($0.30)
- Google veo 3.1, image-to-video, Lite-1080p: 35 credits per video ($0.175)
- Google veo 3.1, image-to-video, Lite-4K: 150 credits per video ($0.75)
- Google veo 3.1, image-to-video, Lite-720p: 30 credits per video ($0.15)
- Google veo 3.1, image-to-video, Quality-1080p: 255 credits per video ($1.275)
- Google veo 3.1, image-to-video, Quality-4K: 370 credits per video ($1.85)
- Google veo 3.1, image-to-video, Quality-720p: 250 credits per video ($1.25)
- Google veo 3.1, reference-to-video, Fast-1080p: 65 credits per video ($0.325)
- Google veo 3.1, reference-to-video, Fast-4k: 180 credits per video ($0.9)
- Google veo 3.1, reference-to-video, Fast-720p: 60.0 credits per video ($0.3)
- Google veo 3.1, reference-to-video, Lite-1080p: 35 credits per video ($0.175)
- Google veo 3.1, reference-to-video, Lite-4k: 150 credits per video ($0.75)
- Google veo 3.1, reference-to-video, Lite-720p: 30 credits per video ($0.15)
- Google veo 3.1, text-to-video, Fast-1080p: 65 credits per video ($0,325)
- Google veo 3.1, text-to-video, Fast-4K: 180 credits per video ($0.90)
- Google veo 3.1, text-to-video, Fast-720p: 60 credits per video ($0.30)
- Google veo 3.1, text-to-video, Lite-1080p: 35 credits per video ($0.175)
- Google veo 3.1, text-to-video, Lite-4K: 150 credits per video ($0.75)
- Google veo 3.1, text-to-video, Lite-720p: 30 credits per video ($0.15)
- Google veo 3.1, text-to-video, Quality-1080p: 255 credits per video ($1.275)
- Google veo 3.1, text-to-video, Quality-4K: 380 credits per video ($1.85)
- Google veo 3.1, text-to-video, Quality-720p: 250 credits per video ($1.25)
- gemini-omni-video, video, 1080p with video input: 168 credits per video ($0.84)
- gemini-omni-video, video, 10s 1080p no video input: 126 credits per video ($0.63)
- gemini-omni-video, video, 10s 4k no video input: 210 credits per video ($1.05)
- gemini-omni-video, video, 10s 720p no video input: 126 credits per vedio ($0.63)
- gemini-omni-video, video, 4k with video input: 252 credits per video ($1.26)
- gemini-omni-video, video, 4s 1080p no video input: 63 credits per video ($0.315)
- gemini-omni-video, video, 4s 4k no video input: 147 credits per video ($0.735)
- gemini-omni-video, video, 4s 720p no video input: 63 credits per vedio ($0.315)
- gemini-omni-video, video, 6s 1080p no video input: 84 credits per video ($0.42)
- gemini-omni-video, video, 6s 4k no video input: 168 credits per video ($0.84)
- gemini-omni-video, video, 6s 720p no video input: 84 credits per vedio ($0.42)
- gemini-omni-video, video, 720p with video input: 168 credits per video ($0.84)
- gemini-omni-video, video, 8s 1080p no video input: 105 credits per video ($0.525)
- gemini-omni-video, video, 8s 4k no video input: 189 credits per video ($0.945)
- gemini-omni-video, video, 8s 720p no video input: 105 credits per vedio ($0.525)
- google/gemini-omni-flash-1-1, video, 1080p with video input: 168 credits per video ($0.84)
- google/gemini-omni-flash-1-1, video, 10s 1080p no video input: 126 credits per video ($0.63)
- google/gemini-omni-flash-1-1, video, 10s 360p no video input: 126 credits per video ($0.63)
- google/gemini-omni-flash-1-1, video, 10s 4k no video input: 210 credits per video ($1.05)
- google/gemini-omni-flash-1-1, video, 10s 720p no video input: 126 credits per video ($0.63)
- google/gemini-omni-flash-1-1, video, 360p with video input: 168 credits per video ($0.84)
- google/gemini-omni-flash-1-1, video, 4k with video input: 252 credits per video ($1.26)
- google/gemini-omni-flash-1-1, video, 4s 1080p no video input: 63 credits per video ($0.315)
- google/gemini-omni-flash-1-1, video, 4s 360p no video input: 63 credits per video ($0.315)
- google/gemini-omni-flash-1-1, video, 4s 4k no video input: 147 credits per video ($0.735)
- google/gemini-omni-flash-1-1, video, 4s 720p no video input: 63 credits per video ($0.315)
- google/gemini-omni-flash-1-1, video, 6s 1080p no video input: 84 credits per video ($0.42)
- google/gemini-omni-flash-1-1, video, 6s 360p no video input: 84 credits per video ($0.42)
- google/gemini-omni-flash-1-1, video, 6s 4k no video input: 168 credits per video ($0.84)
- google/gemini-omni-flash-1-1, video, 6s 720p no video input: 84 credits per video ($0.42)
- google/gemini-omni-flash-1-1, video, 720p with video input: 168 credits per video ($0.84)
- google/gemini-omni-flash-1-1, video, 8s 1080p no video input: 105 credits per video ($0.525)
- google/gemini-omni-flash-1-1, video, 8s 360p no video input: 105 credits per video ($0.525)
- google/gemini-omni-flash-1-1, video, 8s 4k no video input: 189 credits per video ($0.945)
- google/gemini-omni-flash-1-1, video, 8s 720p no video input: 105 credits per video ($0.525)

**video / Grok**

- grok-imagine, image-to-video, 1080p: 8 credits per second ($0.004)
- grok-imagine, image-to-video, 480p: 2.4 credits per second ($0.012)
- grok-imagine, image-to-video, 720p: 4.5 credits per second ($0.0225)
- grok-imagine, text-to-video, 1080p: 8 credits per second ($0.04)
- grok-imagine, text-to-video, 480p: 2.4 credits per second ($0.012)
- grok-imagine, text-to-video, 720p: 4.5 credits per second ($0.0225)
- grok-imagine, upscale, 360p→720p: 10.0 credits per upscale ($0.05)
- grok-imagine, upscale, 480P → 1080P: 30 credits per upscale ($0.15)
- grok-imagine, upscale, 720P → 1080P: 20 credits per upscale ($0.10)
- grok-imagine-video-1-5-preview, image-to-video, 480p: 2.4 credits per second ($0.012)
- grok-imagine-video-1-5-preview, image-to-video, 720p: 4.5 credits per second ($0.0225)
- grok-imagine/extend, 10s 480p: 24 credits  ($0.12)
- grok-imagine/extend, 10s 720p: 45 credits  ($0.225)
- grok-imagine/extend, 6s 480p: 14.4 credits  ($0.072)
- grok-imagine/extend, 6s 720p: 27 credits  ($0.135)

**video / Hailuo**

- MiniMax H3, image input, 768p, 2k: 4 credits per image ($0.02)
- MiniMax H3, image to video, 2K: 13 credits per second ($0.065)
- MiniMax H3, image to video, 768p: 8 credits per second ($0.04)
- MiniMax H3, reference to video, 2K: 13 credits per second ($0.065)
- MiniMax H3, reference to video, 768p: 8 credits per second ($0.04)
- MiniMax H3, text to video, 2K: 13 credits per second ($0.065)
- MiniMax H3, text to video, 768p: 8 credits per second ($0.04)
- MiniMax H3, video input, 2k: 13 credits per second ($0.065)
- MiniMax H3, video input, 768p: 8 credits per second ($0.04)
- hailuo 2.3, image-to-video, Pro-10.0s-768p: 90.0 credits per video ($0.45)
- hailuo 2.3, image-to-video, Pro-6.0s-1080p: 80.0 credits per video ($0.4)
- hailuo 2.3, image-to-video, Pro-6.0s-768p: 45.0 credits per video ($0.225)
- hailuo 2.3, image-to-video, Standard-10.0s-768p: 50.0 credits per video ($0.25)
- hailuo 2.3, image-to-video, Standard-6.0s-1080p: 50.0 credits per video ($0.25)
- hailuo 2.3, image-to-video, Standard-6.0s-768p: 30.0 credits per video ($0.15)

**video / Kling**

- Kling 2.1, image-to-video, Master-10.0s: 320.0 credits per video ($1.6)
- Kling 2.1, image-to-video, Master-5.0s: 160.0 credits per video ($0.8)
- Kling 2.1, text-to-video, Master-10.0s: 320.0 credits per video ($1.6)
- Kling 2.1, text-to-video, Master-5.0s: 160.0 credits per video ($0.8)
- Kling 2.1, video-generation, Pro-10.0s: 100.0 credits per video ($0.5)
- Kling 2.1, video-generation, Pro-5.0s: 50.0 credits per video ($0.25)
- Kling 2.1, video-generation, Standard-10.0s: 50.0 credits per video ($0.25)
- Kling 2.1, video-generation, Standard-5.0s: 25.0 credits per video ($0.125)
- Kling 3.0, video, with audio-1080P: 27 credits per second ($0.135)
- Kling 3.0, video, with audio-4K: 67 credits per second ($0.335)
- Kling 3.0, video, with audio-720P: 20 credits per second ($0.1)
- Kling 3.0, video, without audio-1080P: 18 credits per second ($0.09)
- Kling 3.0, video, without audio-4K: 67 credits per second ($0.335)
- Kling 3.0, video, without audio-720P: 14 credits per second ($0.07)
- Kling AI Avtar , lip sync, Pro-up to 15 secondss-1080p: 16.0 credits per second ($0.08)
- Kling AI Avtar , lip sync, Standard-up to 15 secondss-720p: 8.0 credits per second ($0.04)
- kling 2.5 turbo , image-to-video, Turbo Pro-10.0s: 84.0 credits per video ($0.42)
- kling 2.5 turbo , image-to-video, Turbo Pro-5.0s: 42.0 credits per video ($0.21)
- kling 2.5 turbo , text-to-video, Turbo Pro-10.0s: 84.0 credits per video ($0.42)
- kling 2.5 turbo , text-to-video, Turbo Pro-5.0s: 42.0 credits per video ($0.21)
- kling 2.6 motion control, video to video, 1080P: 18 credits per second ($0.09)
- kling 2.6 motion control, video-to-video, 720P: 11 credits per second ($0.055)
- kling 2.6, image-to-video, with audio-10.0s: 220.0 credits per video ($1.1)
- kling 2.6, image-to-video, with audio-5.0s: 110.0 credits per video ($0.55)
- kling 2.6, image-to-video, without audio-10.0s: 110.0 credits per video ($0.55)
- kling 2.6, image-to-video, without audio-5.0s: 55.0 credits per video ($0.275)
- kling 2.6, text-to-video, with audio-10.0s: 220.0 credits per video ($1.1)
- kling 2.6, text-to-video, with audio-5.0s: 110.0 credits per video ($0.55)
- kling 2.6, text-to-video, without audio-10.0s: 110.0 credits per video ($0.55)
- kling 2.6, text-to-video, without audio-5.0s: 55.0 credits per video ($0.275)
- kling 3.0 motion control, video-to-video, 1080P: 27 credits per second ($0.135)
- kling 3.0 motion control, video-to-video, 720P: 20 credits per second ($0.1)
- kling 3.0 turbo, image-to-video, 1080P: 22.5 credits per second ($0.1125)
- kling 3.0 turbo, image-to-video, 720P: 18 credits per second ($0.09)
- kling 3.0 turbo, text-to-video, 1080P: 22.5 credits per second ($0.1125)
- kling 3.0 turbo, text-to-video, 720P: 18 credits per second ($0.09)

**video / Other**

- MeiGen-AI InfiniteTalk, lip sync, up to 15 secondss-480p: 3.0 credits per second ($0.015)
- MeiGen-AI InfiniteTalk, lip sync, up to 15 secondss-720p: 12.0 credits per second ($0.06)
- hailuo 02, image-to-video, Pro-6.0s-1080p: 57.0 credits per video ($0.285)
- hailuo 02, image-to-video, Standard-10.0s-512p: 20.0 credits per video ($0.1)
- hailuo 02, image-to-video, Standard-10.0s-768p: 50.0 credits per video ($0.25)
- hailuo 02, image-to-video, Standard-6.0s-512p: 12.0 credits per video ($0.06)
- hailuo 02, text-to-video, Pro-6.0s-1080p: 57.0 credits per video ($0.285)
- hailuo 02, text-to-video, Standard-10.0s-768p: 50.0 credits per video ($0.25)
- hailuo 02, text-to-video, Standard-6.0s-768p: 30.0 credits per video ($0.15)

**video / Pixverse**

- pixverse-v6, Extend, 1080p(no aiduo): 14.4 credits per second ($0.072)
- pixverse-v6, Extend, 1080p(with aiduo): 18.4 credits per second ($0.092)
- pixverse-v6, Extend, 360p(no aiduo): 4 credits per second ($0.020)
- pixverse-v6, Extend, 360p(with aiduo): 5.6 credits per second ($0.028)
- pixverse-v6, Extend, 540p(no aiduo): 5.6 credits per second ($0.028)
- pixverse-v6, Extend, 540p(with aiduo): 7.2 credits per second ($0.028)
- pixverse-v6, Extend, 720p(no aiduo): 7.2 credits per second ($0.036)
- pixverse-v6, Extend, 720p(with aiduo): 9.6 credits per second ($0.048)
- pixverse-v6, Reference To Video, 1080p(no audio): 16.2 credits per second ($0.081)
- pixverse-v6, Reference To Video, 1080p(with audio): 20.7 credits per second ($0.1035)
- pixverse-v6, Reference To Video, 360p(no audio): 4.5 credits per second ($0.0225)
- pixverse-v6, Reference To Video, 360p(with audio): 6.3 credits per second ($0.0315)
- pixverse-v6, Reference To Video, 540p(no audio): 6.3 credits per second ($0.0315)
- pixverse-v6, Reference To Video, 540p(with audio): 8.1 credits per second ($0.0405)
- pixverse-v6, Reference To Video, 720p(no audio): 8.1 credits per second ($0.0405)
- pixverse-v6, Reference To Video, 720p(with audio): 10.8 credits per second ($0.054)
- pixverse-v6, Text /Image to Video, 1080p (no audio): 14.4 credits per second ($0.072)
- pixverse-v6, Text /Image to Video, 1080p (with audio): 18.4 credits per second ($0.092)
- pixverse-v6, Text /Image to Video, 360p (with audio): 5.6 credits per second ($0.028)
- pixverse-v6, Text /Image to Video, 360p（no audio）: 4 credits per second ($0.02)
- pixverse-v6, Text /Image to Video, 540p (no audio): 5.6 credits per second ($0.028)
- pixverse-v6, Text /Image to Video, 540p (with audio): 7.2 credits per second ($0.036)
- pixverse-v6, Text /Image to Video, 720p (no audio): 7.2 credits per second ($0.036)
- pixverse-v6, Text /Image to Video, 720p (with audio): 9.6 credits per second ($0.048)

**video / Runway**

- Runway Aleph: 110.0 credits per video ($0.55)
- Runway, image-to-video, 10.0s-720p: 30.0 credits per video ($0.15)
- Runway, image-to-video, 5.0s-1080p: 30.0 credits per video ($0.15)
- Runway, image-to-video, 5.0s-720p: 12.0 credits per video ($0.06)
- Runway, text-to-video, 10.0s-720p: 30.0 credits per video ($0.15)
- Runway, text-to-video, 5.0s-1080p: 30.0 credits per video ($0.15)
- Runway, text-to-video, 5.0s-720p: 12.0 credits per video ($0.06)

**video / Topaz**

- Topaz Video Upscaler, upscale factor 1x/2x: 8.0 credits per second ($0.04)
- Topaz Video Upscaler, upscale factor 4x: 14 credits per second ($0.07)

**video / Wan**

- Wan 2.2 A14B Turbo API Speech to Video, 480p: 12.0 credits per second ($0.06)
- Wan 2.2 A14B Turbo API Speech to Video, 580p: 18.0 credits per second ($0.09)
- Wan 2.2 A14B Turbo API Speech to Video, 720p: 24.0 credits per second ($0.12)
- wan 2.2 Animate, 2.2 Animate Move, 1.0s-480p: 6.0 credits per second ($0.03)
- wan 2.2 Animate, 2.2 Animate Move, 1.0s-580p: 9.5 credits per second ($0.0475)
- wan 2.2 Animate, 2.2 Animate Move, 1.0s-720p: 12.5 credits per second ($0.0625)
- wan 2.2 Animate, 2.2 Animate Replace, 1.0s-480p: 6 credits per second ($0.03)
- wan 2.2 Animate, 2.2 Animate Replace, 1.0s-580p: 9.5 credits per second ($0.0475)
- wan 2.2 Animate, 2.2 Animate Replace, 1.0s-720p: 12.5 credits per second ($0.0625)
- wan 2.2,  text-to-video, 5.0s-480p: 40.0 credits per video ($0.2)
- wan 2.2,  text-to-video, 5.0s-580p: 60.0 credits per video ($0.3)
- wan 2.2,  text-to-video, 5.0s-720p: 80.0 credits per video ($0.4)
- wan 2.2, image-to-video, 5.0s-480p: 40 credits per video ($0.2)
- wan 2.2, image-to-video, 5.0s-580p: 60.0 credits per video ($0.3)
- wan 2.2, image-to-video, 5.0s-720p: 80.0 credits per video ($0.4)
- wan 2.5, image-to-video, default-10.0s-1080p: 200.0 credits per video ($1.0)
- wan 2.5, image-to-video, default-10.0s-720p: 120.0 credits per video ($0.6)
- wan 2.5, image-to-video, default-5.0s-1080p: 100.0 credits per video ($0.5)
- wan 2.5, image-to-video, default-5.0s-720p: 60.0 credits per video ($0.3)
- wan 2.5, text-to-video, default-10.0s-1080p: 200.0 credits per video ($1.0)
- wan 2.5, text-to-video, default-10.0s-720p: 120.0 credits per video ($0.6)
- wan 2.5, text-to-video, default-5.0s-1080p: 100.0 credits per video ($0.5)
- wan 2.5, text-to-video, default-5.0s-720p: 60.0 credits per video ($0.3)
- wan 2.6, image-to-video, 10.0s-1080p: 209.5 credits per video ($1.0475)
- wan 2.6, image-to-video, 10.0s-720p: 140.0 credits per video ($0.7)
- wan 2.6, image-to-video, 15.0s-1080p: 315.0 credits per video ($1.575)
- wan 2.6, image-to-video, 15.0s-720p: 210.0 credits per video ($1.05)
- wan 2.6, image-to-video, 5.0s-1080p: 104.5 credits per video ($0.5225)
- wan 2.6, image-to-video, 5.0s-720p: 70.0 credits per video ($0.35)
- wan 2.6, text to video, 10.0s-1080p: 209.5 credits per video ($1.0475)
- wan 2.6, text to video, 10.0s-720p: 140.0 credits per video ($0.7)
- wan 2.6, text to video, 15.0s-1080p: 315.0 credits per video ($1.575)
- wan 2.6, text to video, 15.0s-720p: 210.0 credits per video ($1.05)
- wan 2.6, text to video, 5.0s-1080p: 104.5 credits per video ($0.5225)
- wan 2.6, text to video, 5.0s-720p: 70.0 credits per video ($0.35)
- wan 2.6, video-to-video, 10.0s-1080p: 209.5 credits per video ($1.0475)
- wan 2.6, video-to-video, 10.0s-720p: 140.0 credits per video ($0.7)
- wan 2.6, video-to-video, 5.0s-1080p: 104.5 credits per video ($0.5225)
- wan 2.6, video-to-video, 5.0s-720p: 70.0 credits per video ($0.35)
- wan 2.7 video, image-to-video, 1080p: 24 credits per second ($0.12)
- wan 2.7 video, image-to-video, 720p: 16 credits per second ($0.08)
- wan 2.7 video, r2v, 1080p: 24 credits per second ($0.12)
- wan 2.7 video, r2v, 720p: 16 credits per second ($0.08)
- wan 2.7 video, text-to-video, 1080p: 24 credits per second ($0.12)
- wan 2.7 video, text-to-video, 720p: 16 credits per second ($0.08)
- wan 2.7 video, videoedit, 1080p: 24 credits per second ($0.12)
- wan 2.7 video, videoedit, 720p: 16 credits per second ($0.08)
- wan 3.0 video, 1080p, video: 32 credits per second ($0.16)
- wan 3.0 video, 480p, video: 8 credits per second ($0.04)
- wan 3.0 video, 720p, video: 16 credits per second ($0.09)
- wan3.0 video prime, 1080p, video: 50.4 credits per second ($0.252)
- wan3.0 video prime, 480p, video: 12.2 credits per second ($0.0612)
- wan3.0 video prime, 720p, video: 25.2 credits per second ($0.126)

---

## Appendix C. Not on Kie as of 2026-10-04

"Live" = `GET /api/v1/models`. "Price" = the public price list. "Playground list" = `GET /api/v1/playground/model-paths`, which holds stale ids.

| Item | Evidence | Status |
|---|---|---|
| Sora 2 family: `sora-2-text-to-video`, `sora-2-image-to-video`, `sora-2-pro-text-to-video`, `sora-2-pro-image-to-video`, `sora-2-pro-storyboard`, `sora-2-characters`, `sora-2-characters-pro`, `sora-watermark-remover`, `sora2-remix`, `sora-2-*-stable` | Doc slugs under `/market/sora2/` return 404. Not in live. No price rows. https://kie.ai/sora-2 is 404. Ids remain only in the playground list. | Removed |
| `elevenlabs/speech-to-text`, `elevenlabs/sound-effect-v2` | Doc slugs return 404. Not in live. No price rows. Playground list only. | Removed |
| `elevenlabs/audio-isolation` | Doc page exists (Appendix A.5). Not in live. No price row. | Documented, probably not callable |
| ElevenLabs voice changer, voice cloning, voice design | No doc page, live id, or price row | Never listed |
| `openai/whisper-speech-to-text` | Playground list only | Not available |
| `kling/v1-avatar-standard`, `kling/ai-avatar-v1-pro`, `kling/v1-tts` | Playground list only. The price rows for Kling AI Avatar still link to the two v1 avatar ids. | Superseded by `kling/ai-avatar-standard` and `kling/ai-avatar-pro` |
| `infinitalk/from-text` | Playground list only | Not available |
| `bytedance/omni-human` | Playground list only | Superseded by `omnihuman-1-5` |
| `kling-o1/*` (Kling O1 image and video reference and edit) | Playground list only. https://kie.ai/kling-o1 is 404. | Superseded by `kling-3.0-omni/*` |
| `luma-dream-machine/modify`, `luma-dream-machine/ray-2-flash-reframe` | Playground list only. https://kie.ai/luma-modify is 404. | Not available |
| `runway/gen4-aleph` | Doc page and a price row (110 credits) exist. Not in live. | Use legacy `POST /api/v1/aleph/generate` |
| `wan/2-6-flash-image-to-video`, `wan/2-6-flash-video-to-video` | Doc pages exist. Not in live. | Probably not callable |
| `ideogram/v3-reframe`, `kie/image-refiner`, `nano-banana-upscale` | Playground list only (reframe also has price rows, its page is 404) | Not available |
| Hedra, Sync lipsync, VEED Fabric, HeyGen, a Kling video lip-sync model, Topaz products other than image and video upscale | No doc page, live id, price row, or playground id | Never listed |
| Seedance asset endpoints (`market/bytedance/create-asset`, `query-asset`) for `asset://` ids | Doc slugs return 404 | Not documented |
| `GET /api/v1/veo/record-info` style detail pages in the current docs | Moved to `/old-model/` | Legacy docs only |

In the live list but without their own createTask doc page: `gemini-omni-audio` and `gemini-omni-character` (they use the dedicated `/api/v1/omni/...` endpoints), `qwen2/text-to-image`.
