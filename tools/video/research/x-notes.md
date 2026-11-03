# X research notes (Ryan's follows, pulled 2026-10-04/05)

Source: x.com search with `filter:follows` while logged in as @RyanJ_Connolly. Everything here is what those accounts SAID, not verified fact, until a test in this workspace confirms it.

## Who matters (from Ryan's follows)
- @0xROAS: AI UGC ads community ("V6" course). Posts exact stacks. Uses Kie.
- @pounddz: AI UGC + AI animation ads, freelance $300 to $500 per ad. Omni + Seedance + NBP + Claude.
- @frankyecom (Franky Shaw): at the front of AI animation / drama ads. Ryan swiped his DMV ad for TPS "Who Is He".
- @LachezarVoynov: lists of AI video ad formats with Foreplay links.
- @Whiskeyatx, @Salifsibane16, @runtraffic, @chrisrudy, @godofprompt, @gregisenberg.

## Model landscape as they describe it (Aug to Oct 2026)
- Seedance 2.5 (ByteDance, Aug 2026): "nano banana moment of AI video". Takes video + image references. Ultra realism, camera control. On Kie. Expensive (<$6 per 30s per 0xROAS 09-04). 0xROAS 08-10: "for some reason i don't really like the lipsync part"; best for hooks, B-roll, complex animation, commercial and Netflix-doc styles. 08-23: "better audio reference mode", "better lipsync" in his cracked method.
- Google Omni ("omni flash", Omni 1.1 late Aug 2026): pounddz: "Omni cooks seedance for AI UGC any day of the week. Cheaper and better." Wins for animation, yappers over 30 seconds, organic content.
- "GPT 2.5" / "GPT Astra" / "ChatGPT Images 2": image models used for character sheets and iPhone-real stills.
- Nano Banana Pro (NBP) / Nano Banana 2 for start frames.
- Older stack (Dec 2025 to Mar 2026) for talking heads: NBP image + voice (MiniMax audio or ElevenLabs clone) + InfiniteTalk or Hedra avatar ($0.04/s) lipsync. This is the audio-first route.
- Upscale: pounddz 09-01 workflow = Pinterest > NBP image > Omni > Topaz > CapCut. Upscaled looked much better.

## Tactics quoted
- 0xROAS Seedance 2.5 video-reference swap (10-01 article): upload a real viral video as Video1 (the "editing master": framing, movement, gestures, timing, lip movements, cuts), character image as Image1. Prompt: "Reference Image1 for the character only. Replace the old man in Video1 with the character in Image1, make sure to keep everything else the same. also make sure the color grading is correct and matches the original video." Every reference has one clearly defined job.
- 0xROAS Seedance 2.0 (06-11 article): reference video max 15s. Custom dialogue variant: "Using video1 as the source video, replace the main character/person in the video with the character shown in img1. character says \"enter script\"". Still prefix for realism: "Create me a photorealistic iphone image with no background blur of a [...]".
- 0xROAS 09-28: AI drama ads = take a winning ad, turn it into a 2 to 3 minute story, catchy hook (Resilia style), multiple cuts per video.
- 0xROAS 09-21: a 10 minute Pixar-style ad fully automated cost about $50 in Kie credits.
- 0xROAS 09-30: an unnamed "really cool model very few people talk about" with really good lipsync; cons: voice issues, location sometimes mixes up.
- pounddz yapper formula (07-14): 1 shocking statement, 2 text hook that complements it, 3 an achievement that backs the topic, 4 a simple visible roadmap, 5 an original name for the method.
- Whiskeyatx 09-18: do not go full production first; one-shot a 2 minute yapper to test the script and angle.
- Salifsibane16 04-29: his best AI editor spends 10 to 15 hours per full video. (That is the gap a one-shot skill closes.)
- frankyecom 04-22: influencer UGC style with no lip sync (voiceover over footage) works in any language.

## Round 2 (same night)
- Gemini Omni Flash = Google model (July 2026), lives in Google Flow, "like $1 per 1 min of video" (0xROAS 07-16). Omni 1.1 Flash late Aug. Used as a video EDITOR (clone a video, swap character/product), not like Veo 3. neverfilmed 10-04: "fast, cheap, actually realistic, way better at following detailed prompts". pounddz: people fail yappers on Seedance, Omni is cheaper/better/faster for yapper content. The script makes the video good, not the AI.
- 0xROAS Omni trick: Flow rejects prompts that edit speech; he screenshots the prompt text and says "Read this image". (Flow UI hack, not relevant to API use.)
- 0xROAS 09-21/22: "10 min ad in one prompt fully edited with astra 6" (GPT-6 Astra/Sol as the agent harness), about $50 Kie credits for a 10 min Pixar ad; automated yapper under $1 (09-24); drama ad fully automated "has some mistakes" (09-23). So fully agent-driven video on Kie is already being done by him; quality bar on his automated output still has visible mistakes.
- pounddz character prompts (10-02 article): full-body studio portrait prompt format (85mm f/8, grey seamless, visible pores, etc.), EDIT prompts that say keep everything identical except X, then a CHARACTER SHEET: one wide image, top row five full-body views (front, 3/4 front, side, 3/4 back, back), bottom row three close-ups, with one detailed CHARACTER paragraph that must match in every panel, "clean thin white dividing lines, no text, no labels". Base negative prompt list included.
- frankyecom thesis (09-20 to 10-04): make the ad the show. Entertainment first, product written into the story; drama ads work for men too; drama ads are top spenders, wording matters for review. Classic UGC hook > problem > solution > CTA is getting predictable.
- LachezarVoynov 14 AI video ad formats on Meta (Foreplay links in the post): skits, whistleblower, celebrity, drama, founder-led, yapper, timeline, authority figure, street interviews, character arguments, warehouse, musicals, Suno songs, mini-movie.

## Other people's Claude Code video skills (leads to study)
- Sabrina_Ramonov 08-18: free `/generate` Claude skill (built from a RoboNuggets guide) that generates through Kie, picks the cheapest model that can do the job, quotes cost and waits for approval, presets; about $0.75 per 10s clip. Kie only charges on success. Fallbacks fal.ai, WaveSpeed.
- mikefutia 09-03: "ad multiplier" Claude Code skill: point at a winning ad + one photo; it watches the ad, pulls the shot table, cut timestamps, camera moves, lighting; shows a lock list (what it holds, what it changes); writes the prompt scoped to shots and timestamps; quotes cost; renders on Seedance 2.5; writes the ORIGINAL AUDIO back over the result. mikefutia.com/ad-multiplier-claude-skill-lm/
- EXM7777 07-28: Claude Code as a film studio, six stages: 1 extract a style contract from real cinema, 2 frames at volume with characters and locations locked, 3 the agent writes every shot prompt, 4 motion + "the grammar that kills frozen shots", 5 subagent fleet generating in parallel, 6 score, montage from a text file, 4K master. "you own taste, the agent owns throughput". Shot loop: generate, watch, change ONE variable, regenerate. Log every generation.
- RaphaelAubryy 09-28: github.com/howseen-ai/claude-motion-design. Motion graphics as code: one pure function seek(t) paints the frame for time t, headless Chromium screenshots every frame, ffmpeg stitches. 4 stills reviewed before any full render. Beat map: every scene starts on a beat. Never trust an automatic beat grid. Useful for caption/graphic overlays.
- tivollem 08-24 (French): AI content is bad because the process lets the model make every decision. One exact format first. Put stops where fixes are free: concept, then script, then start images, and only then video. "A bad sentence is free to fix. A bad generated video is not."

## EXM7777 film-studio rules (07-28 article, read in full)
- Style contract: pick 5 to 10 real shots with the feeling, have a vision model name lens feel, lighting direction and source, palette, grain, contrast, blocking, atmosphere, era; lock ONE paragraph and paste it word for word into every image and video prompt. "cinematic" alone means nothing; pairs land: "motivated warm lighting, 35mm grain, shallow depth of field, lifted blacks".
- Frames before motion, always. Explore at the still layer (cents, seconds). Animate only the winner.
- Reference sheets: front, three-quarter, profile CROPPED SEPARATELY, "because grids confuse the video models into reading panels as different people". Separate sheet per wardrobe/state change. (Conflicts with pounddz's one-wide-grid sheet: test which the model in use prefers.)
- Objects hold emotion better than faces (faces drift, objects lock). One impossible thing in one normal place stops a scroll. Give the character a cost.
- Shot prompts in ONE locked template, same order every time: scene context, references, blocking, camera, lighting, audio, style locks. Consistency comes from repeated reference images and repeated language, never seeds.
- One verb per shot. Five small actions beat one adjective ("blank stare, slow blink, sips coffee, looks up" vs "he looks confused"). Subject movement and camera movement in separate sentences. Text-only prompts 120 to 280 words; image-to-video prompts under 80 words (past that the text fights the image and the character drifts). Constraints positive ("stable picture, sharp clarity"), negatives get ignored.
- Motion grammar that kills frozen shots: (1) a named camera move, (2) an in-scene EVENT that happens during the clip, (3) explicit "no frozen figures". "slow dolly in, cinematic" = a still that drifts; "slow dolly in as the sail tears loose and the crew scrambles to catch it" = film.
- Isolated 3 to 5 second shots; a minute = 12 to 16 shots. Identity drift shows past 30s of continuous scene.
- Chain shots: last frame of shot N is the reference frame of shot N+1. Time-code beats inside one generation: [0-4s] wide static, [4-8s] push in, etc.
- Fleet: respect concurrency caps, 3 to 4 candidates per shot, change ONE variable per pass, log every generation (prompt, model, result, kept/killed).
- Montage as code: the cut is a text file, one line per clip (name, seconds to keep, audio flag), ffmpeg renders it. Mute per-clip audio where it fights the score. Upscale ONCE at the end on the finished cut. 720p while exploring, 1080p keepers.
- Last pass: any clip where you'd check your phone gets deleted.
