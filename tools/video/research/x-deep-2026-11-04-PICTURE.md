# How the AI UGC people get the PICTURE to read as real phone footage (research 2026-11-04)

Scope: picture realism for AI UGC talking-head ads, Aug to Nov 2026. 22 sources read (list at bottom). X posts were read through the fxtwitter API mirror, so X article bodies come back summarized, not verbatim. Anything marked "unverified" is a claim nobody I read showed proof for. Prices in Kie credits use 1 credit = $0.005 (from our own `kie-api.md`, pulled 2026-10-04).

## One-screen summary: the stack most people use, in order

1. **Master = a real winning UGC video.** Download the top TikTok/Reels version of the format, trim it, paint out burned-in captions first (Seedance edit or a subtitle remover), downscale to 720x1280 (Kie only takes 480p/720p reference video).
2. **Character = one iPhone-real still, then a sheet.** GPT Image 2 / 2.5 or Nano Banana Pro/2 (some use Higgsfield Soul for the face). Prompt language: "raw unedited iPhone photo", "no background blur" / "deep depth of field", soft window daylight, visible pores, "no beauty retouching", chest-up 9:16 at eye level. Then a 3-panel sheet (face close-up + front full body + back full body, ONE visible face).
3. **Swap = Seedance 2.5 reference edit** (`reference_video_urls` = master as Video1, `reference_image_urls` = sheet as Image1). 0xROAS prompt, 10-01: "Reference Image1 for the character only. Replace the [old man] in Video1 with the character in Image1, make sure to keep everything else the same. also make sure the color grading is correct and matches the original video." Up to 30 s per run on 2.5. About $5 to $6 per 15 to 17 s swap at 720p.
4. **Cheaper / longer yapper route = Gemini Omni Flash 1.1** (Flow, Higgsfield, Kie): 4 to 10 s clips, each from a start frame (a TikTok screenshot with the person changed in Nano Banana Pro), prompt "extend this video and make her say this ...", several takes per segment, stitched in CapCut. $0.63 to $0.84 per clip on Kie.
5. **Pick takes, fix mouths.** About 2 generated clips per usable clip is the only measured number (Invideo, 103 made, 49 used). Seedance 2.5 fumbles syllables "can't be prompted away" (Maxfusion); Kling 3.0 sync breaks past second 8; Omni Flash stutters about 15% of takes. Sync 3 / Sync 2 Pro is the fix layer.
6. **Finish = CapCut, Topaz LAST.** Captions, product B-roll, cuts on scene changes not mid-sentence, no music for UGC or a quiet bed. Topaz upscale once on the final cut (pounddz: Pinterest > NBP > Omni > Topaz > CapCut). Nobody I read published a grain/grade recipe with numbers; the rule is "match the master's grade, don't add a look".
7. **Time and cost:** about 2 to 3 hours and $73 to $145 per finished ad in Invideo's measured run; a 2 min Seedance swap is about $46 per pass (my arithmetic), so $90 to $140 with 2 to 3 takes per chunk.

Biggest gap in public material: nobody published a measured cut rate, grain amount or grade for AI UGC, and nobody showed a full 2 to 3 min single-character swap with the seams solved. Michael Aubry's "redo from the nearest real cut" is the only seam rule with a reason behind it.

---

## Q1. The video reference swap method

### Seedance 2.5 (the default for swaps)

**0xROAS, "here's how to make viral videos with Seedance 2.5", X article, 2026-10-01** (147k views, 1.5k bookmarks). https://x.com/0xROAS/status/2105719128954950142
- Run it on Kie AI (pay per use; he calls 2.5 "one of the most expensive video models").
- Template: download a viral TikTok/Reels/Shorts video, trim to the supported length, upload as **Video1**. Video1 supplies camera movement, timing, actions, shot order.
- Character: a single-person sheet made in GPT, uploaded as **Image1** = identity only. Sheet layout: three panels, large left portrait with the ONLY visible face, front full-body, back full-body, no facial features in the side panels.
- Prompt (opening and closing lines as quoted): "Reference Image1 for the character only." / "Replace the old man in Video1 with the character in Image1, make sure to keep everything else the same." / "also make sure the color grading is correct and matches the original video."
- Why each line exists (his explanation): the first line stops the model pulling background, lighting or composition from the character image; "keep everything else the same" stops it regenerating the whole scene. Without it: identity drift, background change, clothing change, broken movement.
- Older 2.0 version (his 06-11 article, from our `x-notes.md`): "Using video1 as the source video, replace the main character/person in the video with the character shown in img1. character says \"enter script\"" (custom dialogue variant). 2.0 reference video max 15 s.
- 0xROAS on 2.5 lipsync, 08-10: "for some reason i don't really like the lipsync part"; best for hooks, B-roll, complex animation. 08-23: "better audio reference mode" (from `x-notes.md`, earlier pull).

**Michael Aubry (Wireflow founder), "How to put your own characters in any viral video (Seedance 2.5, the method that finally worked)", X article, 2026-10-02.** https://x.com/michaelaubry/article/2106134433376158000
- Steps: (1) find the most-viewed version of the trend, copy its exact cuts; (2) make ONE still per key beat = the real frame with only the person swapped; (3) one Seedance 2.5 reference edit with the original clip as video ref and the stills as timed keyframes; (4) check output length, compare to the original side by side at 8 fps; (5) if a section fails, redo from the nearest real cut, never patch mid-shot.
- Prompt lines: open with "Character swap edit of @Video1." (length anchor). Keyframes: "Use Images 1 to 6 in order as keyframes at these times: 2.8 s, 5.0 s, 5.8 s, 8.1 s, 10.0 s, 13.5 s." Tells the model to match the original timing and keep the face toward camera unless a still shows otherwise. Leaves action words ("hair toss") OUT of the prompt.
- Stills: about one per second through close-ups where the face matters.
- Cost: a 17 s swap at 720p cost about $5 in model fees; stills cents; retries were the main cost.
- Failure modes: one photo per character made people swap positions mid-clip (fix: one still per beat); describing actions produced exaggerated movement (fix: let stills set poses); re-rendering and splicing a section made the character jump (fix: redo from the nearest original cut); asked for 17.6 s, got 14 s with no warning (fix: anchor length, check every duration).

**Justine Moore (@venturetwins), 2026-09-24** (prompt via YouMind mirror). https://x.com/venturetwins/status/2103169521548976190 , https://youmind.com/video-prompts/character-swap-video-edit-prompt-11249
- Opens: "Edit the entire source video @ Video1. Replace the viewer's FAR RIGHT performer with the man in @ Image1". Then: keep other performers unchanged, name the new wardrobe, photos used ONLY for identity and wardrobe, motion/expressions/gestures/timing/interactions/camera cuts/framing/lighting/background all from the video, preserve the original performance, no new movement or scene elements.

**TECH4SSD, "How to Replace a Video Character Completely with Seedance 2.5", updated 2026-09-18.** https://tech4ssd.com/breakdowns/how-to-replace-a-video-character-completely-with-seedance-25
- Keep from @video1: movement, timing, gestures, camera, framing, environment, lighting, other people. Replace from @image1: face, hair, skin tone, body, clothing, footwear, accessories.
- Prompt skeleton: name a TARGET_ACTOR and lock it across cuts; "Do NOT perform a face swap only."; "The replacement character must perform the same movement at the same moment."; priority order ending with "never show the original actor".
- Failure fixes: source clothes bleed through = restate "@image1 is the wardrobe authority"; original face returns on turns = multi-angle sheet + stronger identity lock; other people get replaced = restate only TARGET_ACTOR maps to @image1. "Fix the specific failure rather than endlessly expanding the prompt."
- 2.5 does up to 30 s per generation.

**Riffkit (vendor, author makes the tool), 2026-10-06.** https://riffkit.ai/blog/seedance-character-swap
- Important audio fact: on Seedance 2.0 the original voice stays; on **2.5 the swapped on-camera lines get a NEW AI voice by default**. "keep the original audio" keeps every voice. Narration (heard, not seen) keeps the original unless asked.
- Their limits: 2.5 single render 30 s; source up to 45 s split at shot cuts; cites BytePlus: 2.5 accepts reference video 4 to 30 s, 2.0 caps video input at 15 s total.
- Kept: shots, cuts, camera, framing, poses, timing, aspect, language, source sound where no voice changes. Their example: "shots, cuts and caption stayed" (so burned-in captions in the master SURVIVE the swap).
- Character photo: two views of the same person on plain background, face close-up left, full body right. A sheet of many small poses "usually fails in close-ups".

**Mike Futia "ad multiplier" Claude Code skill, 2026-09-03** (from `x-notes.md`; the landing page https://mikefutia.com/ad-multiplier-claude-skill-lm/ is a gated download, no detail on page): point at a winning ad + one photo; it pulls the shot table, cut timestamps, camera moves, lighting; shows a lock list (what it holds, what it changes); writes a prompt scoped to shots and timestamps; quotes cost; renders on Seedance 2.5; **writes the ORIGINAL AUDIO back over the result.** That last step is the answer to the 2.5 new-voice problem.

**Kie API facts for `bytedance/seedance-2-5`** (our `kie-api.md`, docs.kie.ai/market/bytedance/seedance-2-5, pulled 2026-10-04):
- `reference_video_urls` max 10, each 2 to 30 s, **total reference video ≤ 30 s**, mp4/mov, **480p or 720p only**, total pixels 409,600 to 927,408 (720x1280 = 921,600 fits; 1080x1920 does NOT), 24 to 60 fps, ≤ 200 MB.
- `reference_image_urls` max 30, `reference_audio_urls` max 10 (2 to 30 s each). All mutually exclusive with `first_frame_url`.
- `duration` 4 to 30, or **-1 = match the input video length for edit tasks**. `generate_audio` default true (costs more). `return_last_frame` available.
- Price: 720p with video input 38 credits/s ($0.19), billed on INPUT + OUTPUT seconds; 480p 17 ($0.085); 1080p 95 ($0.475). No video input: 720p 63 ($0.315).
- So a 15 s master + 15 s output at 720p = 30 x $0.19 = **$5.70 per take** (my arithmetic). Matches Aubry's ~$5 for 17 s and 0xROAS's "<$6 per 30s" (09-04, x-notes). Third-party Seedance 2.5 price pages (apimart, kreatorflow, evolink) list the same $0.14 / $0.315 / $0.79 base rates: https://apimart.ai/blog/seedance-2-5-api-guide-pricing-features-access

### Gemini Omni Flash 1.1 ("clone a video")
- **Google docs** (aistudio.google.com/docs/omni, read 2026-11-04): model id `gemini-omni-1.1-flash`; 360p/720p default/1080p and 4K (both upscaled); 16:9 or 9:16. Uploaded videos for edit/extend must be **≤ 10 s**. Video references: up to 3 clips, each ≤ 3 s, best for likeness, **their audio is ignored**. Extension appends 3 to 10 s, total up to 40 s. Edit prompts are short ("Put a fashionable hat on this person"); Google recommends adding **"Keep everything else the same"** and keeping prompts simple because long ones cause unintended changes. No negative prompts. No voice editing. Editing uploaded video not available in EEA/CH/UK. Recognizable people blocked. SynthID watermark on every output. https://aistudio.google.com/docs/omni
- **Kie price** (kie-api.md): `google/gemini-omni-flash-1-1` with video input 168 credits per video = **$0.84**; 10 s no video input $0.63; 4 s $0.315.
- **EP (@eptwts), 2026-07-23** (paid Higgsfield partnership): whole video is 4 to 8 s clips; each clip starts from a start frame = a TikTok UGC screenshot run through Nano Banana Pro to change the person; prompt begins "extend this video and make her say this" + the line + conditions; expect several generations per segment; compile in CapCut. Reported problems: voices too similar, words bleed between chained clips; suggests frame interpolation for choppy motion. https://x.com/eptwts/status/2080365325988606266
- pounddz (from x-notes, 08 to 10 2026): "Omni cooks seedance for AI UGC any day of the week. Cheaper and better." Omni wins for yappers over 30 s. 0xROAS 07-16: "like $1 per 1 min of video" in Flow. 0xROAS Flow trick: Flow rejects prompts that edit speech, so he screenshots the prompt and says "Read this image" (Flow UI only, unverified on API).

### Kling 3.0 Omni (O3) reference-to-video / transformation (Kie facts)
- `kling-3.0-omni/transformation`: prompt-edit a **3 to 15.5 s** video, `video_urls` + optional `image_urls` + `elements`. 20 / 27 / 67 credits per s (720p / 1080p / 4K) = $0.10 / $0.135 / $0.335 per s.
- `kling-3.0-omni/reference-to-video`: up to 7 images, elements 2 to 4 images each; **`audio` must be false when a reference video is supplied**, so the voice has to be laid back on after. Multi-shot up to 6 shots.
- `kling-3.0/motion-control`: transfer motion from a 3 to 30 s video onto ONE character image; 20 (720p) / 27 (1080p) credits per s. This is the "Kling Motion Transfer" step in several vendor workflows (Atlabs, VidAU).
- Nobody I read published a UGC person-swap test on Kling O3 transformation. Wireflow's roundup says Kling O3 Edit Video, Runway Aleph and Higgsfield Genjutsu all swap OBJECTS with "small shape errors near faces" (vendor, unverified): https://www.wireflow.ai/blog/higgsfield-genjutsu-alternative

### Runway Aleph / Character Swap, Wan 2.7 r2v
- Runway Aleph = video-to-video edit, reference images define the new look, original motion and camera kept, character replacement listed as a use. Runway also has a separate "Character Swap" app that keeps or replaces audio (AlphaSignal summary via search; the article 404'd for me, unverified).
- Wan 2.7 r2v on Kie: up to 5 images + videos total, 2 to 10 s, $0.08/s 720p, `reference_voice` 1 to 10 s; if the reference video has audio and no `reference_voice`, it uses the original audio. No public UGC swap results found.

### Burned-in captions in the master
- Nobody in the creator posts says what they do. Evidence: Riffkit's own example says the caption STAYED through a Seedance swap, so captions in Video1 come through.
- Fix seen in vendor guides: clean the plate first. Atlas Cloud's Seedance 2.5 edit prompt: "remove the burned-in subtitles at the bottom of the frame, keep everything else in the shot exactly as it is." Then swap, then add your own captions in CapCut. https://www.atlascloud.ai/blog/tips/remove-subtitles-from-video
- Caveat (Kenerate): whole-clip AI re-renders shift fine detail; fine for a reference copy, flicker risk on busy backgrounds. A cheaper route that is unverified: crop or mask the caption band before upload.

### Chaining 15 to 30 s limits into a 2 to 3 minute ad
- Seedance 2.5 does 30 s per run, so a 60 s ad = 2 runs (Maxfusion, Atlas). Kie total reference video ≤ 30 s, so chunk the master into ≤ 30 s pieces, ideally cut at the master's own cuts (Riffkit splits at shot cuts; Aubry: redo from the nearest real cut).
- Krea: "Stitched clips let the face, product, or voice drift at each seam." Their fix is single 30 s takes; nothing past 30 s.
- Omni route: chained 4 to 10 s extends, words bleed between clips (EP).
- EXM7777 (07-28, x-notes): last frame of shot N = reference frame of shot N+1; identity drift shows past 30 s of continuous scene.
- Seam hiding that nobody measured but everyone does: cut on a sentence end, cover with B-roll or a jump cut, since UGC already jump-cuts.
- 0xROAS 09-28: drama ads are 2 to 3 min stories with "multiple cuts per video". 09-21: a 10 min Pixar ad fully automated cost about $50 in Kie credits (x-notes).
- Cost of a 2 min Seedance 2.5 swap at 720p: 4 chunks x (30 s in + 30 s out) x $0.19 = **$45.60 per pass**; with 2 to 3 takes per chunk, $90 to $140 (my arithmetic). Omni route: 12 x $0.84 = $10 per pass.

---

## Q2. Start frames: the iPhone photo character and room

**0xROAS "Start Frame Maker" method (via Digital Zoom Studio summary, 2026-10-29).** https://digitalzoomstudio.net/2026/10/how-to-make-realistic-ai-ugc-images-of-people-nobody-else-has/
- Upload a real reference photo to his custom GPT "Start Frame Maker", type "prompt only"; paste into Higgsfield Soul 2.0 / Soul Cinema for the face (9:16, 2K, enhance OFF, batch of 4); then GPT Image 2 image-to-image to move the person into new scenes (High, 2K, 9:16, 4 outputs); "remove overlays" to strip Soul's social icons.
- Five-paragraph prompt: Person (age, hair, skin with "realistic fine lines", eyes, makeup, clothing, jewelry, expression) / Pose (seated, lean, hand mid-gesture, "like a paused testimonial frame") / Framing (vertical 9:16, chest-up, iPhone at eye level, "slight everyday asymmetry") / Setting (lived-in room, named details) / Light + realism (soft window daylight, true colors, sharp focus, NO beauty retouching, NO dramatic grading, NO fake lens effects, NO editorial styling, NO text/logos/overlays). Asks for an "authentic unfiltered UGC snapshot".
- Rule of thumb: "Soul for the selfies, GPT image-to-image to move the person around." Same face held across kitchen, street, car in the author's test.
- Cost: GPT Image 2.5 on Kie $0.05 per 2K image.
- 0xROAS still prefix (06-11, x-notes): "Create me a photorealistic iphone image with no background blur of a [...]".

**KNOX (@knoxtwts), "how you can outproduce entire creative teams with 5 tools", 2026-02-17** (older, still the most specific JSON method). https://x.com/knoxtwts/status/2023749545939624246
- Nano Banana Pro with a JSON prompt. Face: visible pores, natural oiliness, freckles, no smoothing, no beauty filters. Camera: iPhone front camera, digital noise, realistic dynamic range, slight motion softness. "Avoid" list does most of the work: CGI, AI-generated look, plastic skin, studio lighting, beauty filters, perfect symmetry.
- Color: find a Pinterest reference photo, have Gemini extract a JSON of its grade, lighting and composition, paste into NBP.
- Consistency: reuse ONE saved character image across the whole campaign.

**DXBuilder (Filipe Heitor, vendor), 2026-09-23.** https://dxbuilder.io/blog/how-to-create-realistic-phone-footage-ai-ugc-230926
- Seed frame: "Raw unedited smartphone photo taken with an iPhone 16 Pro 24mm main lens, front-facing camera angle." + natural side-window light, visible pores, no airbrushing, 9:16 native.
- Directive table: "shot on 24mm smartphone camera lens" (not 50 to 85 mm); "deep depth of field, sharp background details"; "handheld selfie camera micro-jitters, natural hand movements"; "visible skin pores, subtle facial asymmetries, natural room daylight"; "authentic phone footage grain, unpolished raw recording". Light: 5600K window daylight + 2700K warm lamps.
- Motion prompt rule: never re-describe the person or clothes in the image-to-video prompt (causes face morphing); "The camera stays in authentic selfie POV framing."; only kinetic action (gestures, blinks, head tilts, breathing).
- Tells to avoid: waxy airbrushed skin, 85 mm look with background blur, crane-smooth camera, Hollywood grade, "cinematic 8K" prompts.

**Krea, Seedance 2.5 30 s guide, 2026-08-26.** https://www.krea.ai/blog/seedance-2-5-makes-a-full-30-second-ugc-ad-in-one-shot-2026-guide
- Actor still in Seedream 5 Pro: "photorealistic portrait of a 29 year old woman" in a bright bathroom, filmed like a phone front-camera selfie, bare face, morning window light, no retouching, no studio lighting. "A studio portrait makes the ad look like an ad." Stills at 768x1376.

**pounddz character prompts (10-02 article, from x-notes):** full-body studio portrait (85mm f/8, grey seamless, visible pores) used ONLY to build the sheet; edit prompts "keep everything identical except X"; sheet = one wide image, top row five full-body views (front, 3/4 front, side, 3/4 back, back), bottom row three close-ups, one CHARACTER paragraph repeated, "clean thin white dividing lines, no text, no labels". pounddz sourcing: Pinterest > NBP.

**Face consistency, the methods in use:**
- One locked still or sheet reused everywhere (KNOX, 0xROAS).
- Sheet shape conflict: 0xROAS = 3 panels with ONE visible face; pounddz = 8-panel grid; EXM7777 = front, 3/4, profile CROPPED SEPARATELY because "grids confuse the video models into reading panels as different people"; Riffkit = 2 views, many-pose sheets "usually fail in close-ups". Test on our model; the safest public pattern is few panels, one dominant face.
- Aubry: one still per beat (about 1 per second in close-ups) beats one photo per character.
- Maxfusion on 2.5: "the face holds" with a reference; the 2.0 same-face problem is gone.
- Contested: "no blur" vs "add slight blur". DXBuilder and 0xROAS push deep focus / no background blur; a few vendor guides add handheld blur. Consensus: background sharp, motion handled by jitter in the video prompt, not lens blur in the still.

---

## Q3. Which video models for talking-head realism, and their tells

| Model | Who rates it and why | Known tells |
|---|---|---|
| **Seedance 2.5** (Aug 2026) | Maxfusion: "it one-shots UGC ads I could not tell apart from real phone footage"; "the skin holds, the light behaves like indoor light". MindStudio: more grounded human motion, quality holds full clip. Default for swaps (0xROAS, Aubry, Futia). | "Seedance 2.5 fumbles syllables." (product names, multi-syllable words), can't be prompted away; QA every audio track, keep a problem-word list (Maxfusion). New AI voice on swapped lines by default (Riffkit). Silent truncation (Aubry). 720p ceiling in practice. Expensive. 0xROAS doesn't like its lipsync. |
| **Gemini Omni Flash 1.1** | pounddz: cheaper and better than Seedance for yappers; neverfilmed 10-04: "fast, cheap, actually realistic". Clean takes "excellent" (Maxfusion). | "Around 15% of generations stutter" / repeat syllables (Maxfusion, earlier Omni). Softer motion, backgrounds lose sharpness, hand/finger and hair artifacts in extended action (MindStudio). Voices too similar, words bleed across chained clips (EP). ≤10 s edit input. |
| **Kling 3.0 / 3.0 Omni** | Lip-sync leader at its price (ugcvids); KNOX picks it for dialogue-heavy talking heads (multi-shot). Mike Futia's 02-12 one-prompt UGC workflow. | "past second 8 the audio and the lips lose each other" (Maxfusion). Audio off when a reference video is used (Kie doc). |
| **Veo 3.1** | Realism ceiling for 4 to 8 s hook shots (ugcvids); ingredients mode holds a face (KNOX). | "the mouth region simply doesn't look human"; rubbery motion, wrong plosive shapes (Maxfusion). Expensive. |
| **Sora 2 / 2 Pro** | "The lip sync almost never breaks." (Maxfusion) | Highest per-second price; Maxfusion says it sunsets Sept 24, 2026 (unverified; check before planning on it). |
| **Hailuo 03** | No UGC talking-head reviews found. Hailuo has no native lipsync per Atlas Cloud. | unverified |
| **Wan 2.7 / 3.0** | Cheapest per second on Kie (2.7 $0.08/s 720p). DXBuilder benchmarks Wan at $0.11 to $0.18 per 5 s clip. No realism reviews found. | unverified |
| **Fix layer: Sync 3 / Sync 2 Pro** | Sync 3: "The best lip sync model available, full stop." Sync 2 Pro preserves teeth, beards, skin around the mouth. Rule: "Cheap model, regenerate. Expensive model, repair." (Maxfusion) | Sync 2 Pro struggles with still frames and hard angles. |

Sources: Maxfusion lip-sync test (Ori Silver, byline 2026-07-28, page meta 11-02) https://maxfusion.ai/blog/ai-video-models-lip-sync-2026 ; Maxfusion Seedance 2.5 test ($4,000 of pre-release generations, byline 2026-08-03) https://maxfusion.ai/blog/seedance-2-5-release ; MindStudio (updated 2026-08-03) https://www.mindstudio.ai/blog/seedance-2-5-vs-gemini-omni-flash ; ugcvids (2026-07-04) https://ugcvids.ai/blog/talking-head-ugc-ads-2026

General tells everyone lists (vendor blogs): over-smooth pore-less skin; teeth that change count or fuse; dead/glassy eyes on emphasis words, asymmetric blinks, eye line drifting off the lens; lip sync that starts clean then slips; monotone read; mid-sentence stitch; the 85 mm blurred-background look; Hollywood grade. Animoto stat cited secondhand: viewers who suspected AI named robotic gestures 67%, unnatural voice 55%, flat emotion 51% (unverified).

No head-to-head blind test of Seedance 2.5 vs Omni 1.1 vs Kling 3.0 on the same script exists in public. Run our own.

---

## Q4. Editing and finishing

What is stated (none of it measured against sales):
- **Clip length / cut rate:** DXBuilder: 5 to 8 s scene blocks, about 5 cuts in a 30 s ad. One vendor guide: cuts every 1 to 2 s, under 27 s (unverified). ugcvids: if a model caps at 8 s, cut on scene changes, not mid-sentence. EXM7777: isolated 3 to 5 s shots, a minute = 12 to 16 shots (cinematic, not UGC).
- **Jump cuts:** suggested "quick cuts at syllable boundaries" to hide small sync artifacts (vendor, unverified). Natural fit because real UGC jump-cuts.
- **B-roll:** eptwts: layer product B-roll, screen recordings, on-screen captions and trending music AROUND the raw generation. Common recipe: one or two B-roll cutaways and a product zoom.
- **Audio bed:** Krea: name room tone and "no music", or the model scores it like a commercial. Invideo: 110 to 120 BPM bed for a 25 s ad.
- **Captions:** burn in your own after the swap (CapCut). Check product names and prices against the audio; keep top/bottom safe zones. No style spec published.
- **Grade:** the only creator instruction is 0xROAS's "make sure the color grading is correct and matches the original video" inside the swap prompt; KNOX gets the grade from a Pinterest photo's JSON. Everyone says avoid saturated/Hollywood grades. No numbers.
- **Grain / compression:** DXBuilder: subtle ISO noise and "realistic social compression". Upscaler warning: upscaled grain "will feel painted". No numbers.
- **Topaz:** pounddz 09-01 (x-notes): Pinterest > NBP > Omni > **Topaz** > CapCut, "upscaled looked much better". EXM7777: upscale ONCE at the end on the finished cut; 720p while exploring. Counterpoint (vendor guide): Topaz gain is invisible at phone size, use CapCut enhance. Topaz models: Rhea for static interviews, Iris for faces in compressed footage, Nyx for grain. On Kie: `topaz/video-upscale` 8 credits/s at 1x/2x ($0.04/s), 14 at 4x ($0.07/s). A 2 min ad at 2x = about $4.80 (my arithmetic).
- **Voice normalization (affects how the picture reads):** KNOX runs the script through a random CapCut voice first, then ElevenLabs. Futia's skill writes the master's original audio back over the swap.

---

## Q5. Time per ad and takes per line

- **Invideo, 2026-07-15 (only measured run found):** 4 ads, 108 images + 103 videos generated, 49 clips used (about 2 generated per usable). By format: BTS product 7 of 7; outdoor UGC with interaction 10 of 39 and 8 of 20 (25 to 40%). Per ad: trial-room UGC ~$73 / ~2 h, outdoor UGC ~$130 / ~3 h, localized ~$145 / ~2.5 h; average ~$125 / ~2 h. Two people ship 4 to 5 ads in an 8 h day. "I only spent video credits on locked frames." https://invideo.io/blog/ai-ugc-ads/
- EP: "several generations per segment" (Omni).
- Aubry: retries were the main cost of a ~$5 swap.
- Salifsibane16 (04-29, x-notes): his best AI editor spends 10 to 15 hours per full video.
- 0xROAS: yapper under $0.50 (03-15, https://x.com/0xROAS/status/2033316303629373674), automated yapper under $1 (09-24), 10 min Pixar ad about $50 (09-21); his automated drama ad "has some mistakes".
- Alici.ai (April 2026, vendor): 240+ generations across 14 tools; Mirage 12 of 24 (50%) ad-review-ready without re-prompting.
- Krea render times: 30 s Seedance 2.5 ad took 22 min, 10 s took 13 min (queue-dependent).
- Working planning number: 2 to 3 takes per line on Seedance/Kling, 3+ on Omni (15% stutter), a 2 to 3 min ad = a half day to a day of one person's time. Inference from the above, not measured by any one source.

---

## Q6. Published pipelines

- **0xROAS "AI UGC System" (paid, whop).** No public "V6" doc found; Ryan's x-notes call it the V6 course. Public pieces: Start Frame Maker GPT > Higgsfield Soul > GPT Image 2 i2i (images); Seedance 2.5 swap on Kie (video). Older audio-first stack: Gemini prompt > MiniMax voice > Nano Banana 2 image > InfiniteTalk lipsync. Course listings: https://econolearn.com/the-anti-slop-ai-ugc-system-0x-roas/
- **pounddz:** Pinterest ref > Nano Banana Pro > Omni Flash > Topaz > CapCut. Freelance $300 to $500 per ad (x-notes). His one public post found (https://x.com/pounddz/status/2040011032786038954) only says Seedance 2.0 via Arcads makes it easy.
- **Sabrina Ramonov `/generate` Claude skill, 2026-08-19.** https://www.sabrina.dev/p/this-1-claude-skill-fully-replaces
  1. read the model's recipe file; 2. draft a still on a cheap image model (nano-banana-2; gpt-image-2 when text is in frame); 3. pre-animate QA (1080x1920, no stray text, right subject/POV); 4. quote cost, wait for approval; 5. animate on Kie (default Seedance 1.0 Pro `bytedance/v1-pro-image-to-video`, Lite for budget, 2.5 only on request); 6. check real MP4 dimensions and a frame; 7. log to `generations/ledger.json`. Caps: $10 per session, $50 per month. About $0.70 per 10 s 1080p clip. Faceless content, not talking heads.
- **Mike Futia "ad multiplier" Claude skill (09-03):** winning ad + one photo > shot table, cuts, camera, light > lock list > timestamped prompt > cost quote > Seedance 2.5 > original audio laid back. Gated download.
- **EP / Higgsfield Seedance 2.5 workflow, 2026-08-06 (sponsored):** find a proven TikTok/IG video > send it to Gemini: "break down this video 1:1 so i can recreate it exactly" (timestamped visuals, captions, emphasis, tone, mannerisms) > paste the breakdown as the Seedance prompt at 9:16 720p > add B-roll, screen recordings, captions, music. https://x.com/eptwts/article/2085439131887550534
- **KNOX 5-tool pipeline (02-17):** Claude script > NBP JSON character > CapCut voice normalize + ElevenLabs > Wan lipsync / InfiniteTalk on RunPod > CapCut.
- **Maxfusion prompt structure for 2.5:** one paragraph for character + setting, then timestamped windows (00:00 to 00:04 ...) each pairing the exact spoken line with action, framing and product position. Krea says the same: an untimed prompt says everything in about 12 s then drifts.
- **Invideo agent run:** brand context once > 3 script tones, lock one > anchor frame > multi-angle sheet > storyboard stills > per-shot brief > Seedance 2.0 in batches of 5 with sheet + still as dual refs > vary action and angle per beat > one voiceover mapped to shots > music bed and stitch.
- No public n8n flow for the swap method found.

---

## What this means for our oneshot-video skill (my read, not from sources)
- The swap route needs four things our pipeline may not have yet: a caption-clean step on the master, a downscale to ≤ 720x1280 before upload, `duration: -1` plus a duration check on every output, and an audio decision (2.5 re-voices on-camera lines; either pass our locked voice as `reference_audio_urls` or lay the voice back over after).
- Chunk the master at its own cuts, ≤ 30 s each, and re-render from the nearest real cut on failure.
- Budget: ~$5.70 per 15 s take, plan 2 to 3 takes.

## Sources read in full (22)
1. 0xROAS X article, 2026-10-01: https://x.com/0xROAS/status/2105719128954950142
2. Michael Aubry X article, 2026-10-02: https://x.com/michaelaubry/article/2106134433376158000
3. Justine Moore prompt, 2026-09-24: https://youmind.com/video-prompts/character-swap-video-edit-prompt-11249
4. TECH4SSD, 2026-09-18: https://tech4ssd.com/breakdowns/how-to-replace-a-video-character-completely-with-seedance-25
5. Riffkit, 2026-10-06: https://riffkit.ai/blog/seedance-character-swap
6. Google Omni docs: https://aistudio.google.com/docs/omni
7. EP Omni post, 2026-07-23: https://x.com/eptwts/status/2080365325988606266
8. EP Seedance 2.5 article, 2026-08-06: https://x.com/eptwts/article/2085439131887550534
9. Digital Zoom Studio on 0xROAS images, 2026-10-29: https://digitalzoomstudio.net/2026/10/how-to-make-realistic-ai-ugc-images-of-people-nobody-else-has/
10. Sabrina Ramonov, 2026-08-19: https://www.sabrina.dev/p/this-1-claude-skill-fully-replaces
11. Maxfusion lip-sync test: https://maxfusion.ai/blog/ai-video-models-lip-sync-2026
12. Maxfusion Seedance 2.5 test: https://maxfusion.ai/blog/seedance-2-5-release
13. MindStudio 2.5 vs Omni: https://www.mindstudio.ai/blog/seedance-2-5-vs-gemini-omni-flash
14. Krea 30 s guide, 2026-08-26: https://www.krea.ai/blog/seedance-2-5-makes-a-full-30-second-ugc-ad-in-one-shot-2026-guide
15. DXBuilder, 2026-09-23: https://dxbuilder.io/blog/how-to-create-realistic-phone-footage-ai-ugc-230926
16. Invideo, 2026-07-15: https://invideo.io/blog/ai-ugc-ads/
17. KNOX, 2026-02-17: https://x.com/knoxtwts/status/2023749545939624246
18. Mike Futia Kling post, 2026-02-12: https://x.com/mikefutia/status/2021979641687552419
19. 0xROAS yapper post, 2026-03-15: https://x.com/0xROAS/status/2033316303629373674
20. ugcvids, 2026-07-04: https://ugcvids.ai/blog/talking-head-ugc-ads-2026
21. Kie docs (our pull 2026-10-04): `tools/video/research/kie-api.md`
22. Our earlier X pull from Ryan's follows: `tools/video/research/x-notes.md`
