# X deep dive: what named accounts say about ultra-realistic AI UGC video ads (Aug 1 to Nov 4, 2026)

Pulled 2026-11-04.

## How this was pulled (source notes)

- **Main source:** the FxTwitter public API (`api.fxtwitter.com/2/profile/<handle>/statuses`, paginated by cursor) for each account's own timeline from 2026-08-01 to 2026-11-04, plus `api.fxtwitter.com/i/status/<id>` for single posts, threads and X Articles. The article bodies came from the `article.content` field. All quotes below are copied from that API output. Every link is the original x.com post URL the API returned.
- **Did not work:** xcancel.com (service suspended), nitter.net (offline), Claude in Chrome (extension not connected). The `cdn.syndication.twimg.com` endpoints worked but returned only top posts, mostly from 2025, and cut long posts off at 280 characters, so they were used only to cross-check.
- **Coverage gaps:** the FxTwitter profile timeline skips some posts. For example, 3 of @pounddz's August posts (Omni 1.1, the male voice post and the voice thread) only showed up because other posts quoted them, so I fetched them one by one. @neverfilmed's timeline stopped paging at 2026-09-25, so anything older from that account is missing. Each section lists the posts I actually saw.
- **Images inside articles:** prompts posted as images inside X Articles (0xROAS's 10-01 character-sheet prompt and video prompt, his 09-02 Gemini prompt) show only as `[media]` in the API. That text is marked unverified unless the same prompt also appears as plain text in a post.
- **Self-reported numbers:** everything below (cost, spend, CPA, ROAS, hours) is what the account says about its own results. None of it is independently verified.

---

## 1. @0xROAS ("0x ROAS", runs "the anti-slop AI UGC system" community on Whop)

**What he uses (as of Oct to Nov 2026)**
- **Image (characters, props, character sheets):** "GPT Images 2.5" (since 09-08; before that "gpt 2.0"). He builds the character with ChatGPT using his "chatgpt image reference method".
- **Video:** Seedance 2.5 on Kie.ai is the main engine since 08-01. He has also posted with "Wan 3.0" (09-03), "omni flash" (08-10), Sora 2 (old work) and an unnamed "really cool model very few people talk about" (09-30).
- **Voice:** whatever Seedance generates natively. He works from a reference voice ("better audio reference method", 08-31). No separate TTS is named. His one fix is phonetic spelling.
- **Lip sync:** Seedance native. He says it got better with his 08-23/08-31 "cracked" method.
- **Agent and editor:** "GPT-6 Astra" and "GPT-6 Sol" in September, "Claude Opus 5.5" from late October ("video is fully edited with OPUS 5.5"). He also uses Claude Code skills and a "grok bot + t3 code" ads agent.
- **Breakdown and analysis:** Gemini ("gemini 3.7 flash" in AI Studio, thinking set to high).
- **Upscaler:** none named. Unverified.
- **Course:** "AI UGC V3" in August, renamed "0X System", then launched as "V6" around 09-07 (the "AI UGC V6 System"). "my course is literally $148/m" (10-18). He says the price will 3x or 4x. Codes: "50koff" (09-03), "1YEAR" for 50% off (11-02). Whop links: whop.com/ai-marketing-mafia/the-anti-slop-ai-ugc-system. Note: Franky Shaw also calls his framework "v6". They are two different products.

**Verbatim, with dates and links**

- 2026-08-01: "Seedance 2.5 + AI UGC = $$$ ... my first take at seedance 2.5 AI UGC, it's crazy good but also it's crazy expensive hahah. this cost me ~$20" https://x.com/0xROAS/status/2083564974530568399
- 2026-08-10, on voice and lip sync (the key quote): "seedance 2.5 is really good at making extremely realistic videos that you can literally not tell that they're ai. but for some reason i don't really like the lipsync part ... here's what i would use seedance 2.5 for in ecom/aff ads: - hooks - brolls - complex animations ... if you combine seedance 2.5 + omni flash you can get some pretty good ads." https://x.com/0xROAS/status/2086797500644552825
- 2026-08-14, the full street-interview method: "i deconstructed the whole video w/ gemini - i generate all characters and props w/ gpt 2.0 - i uploaded all the references to seedance 2.5 - i uploaded the prompt gemini gave me - that's it ... it took me less than 15 mins" https://x.com/0xROAS/status/2088292533465923678
- 2026-08-20, voice and accent problem plus the fix: "infinite AI podcasts using my SD2.5 framework ... total cost per min around $13 ... if the reference voice doens't have a good accent it will have issues pronouncing words (like my accent) the fix is to make phonetic words like: Carbohydrate = kar-boh-HY-drayt ... this took me around 10-15 mins" https://x.com/0xROAS/status/2090408321744249001
- 2026-08-20, X Article "here's how to clone videos w/ Seedance 2.5 (full breakdown)" (the reference-video swap method, 2-person podcast version): "Step 1: go to Seedance 2.5 on kie ai ... Step 2: download your base video ... upload it to Seedance 2.5 as Video1. this video will act as the editing master. Seedance will use its camera framing, movement, actions, gestures, timing, lip movements, shot transitions, and event order." His ChatGPT step for new faces: "help me clone this image, i need a prompt with image reference, where i will upload an image of left host, and image of right host. this will be the main shot of the podcast. image1 will be the total reference, image2 diff left host, image3 diff right host". The exact swap prompt, quoted in full:
  > 【Editing Goal】 Edit Video1, replacing the speaker on the left with the person in Image1 and the speaker on the right with the person in Image2.
  > 【Role of the Source Video】 Video1 is the sole editing master and governs the scene, camera framing, movement, action trajectories, shot transitions, and event order.
  > 【Role of the Target Material】 Image1 is used for the facial features, hairstyle, and wardrobe of the left speaker; do not adopt its background or lighting. Image2 is used for the facial features, hairstyle, and wardrobe of the right speaker; do not adopt its background or lighting.
  > 【Edit Objects and Scope】 Modify only the appearance, facial identity, and clothing of the two seated speakers. Except for the objects explicitly modified above, all other visible characters, props, and background elements in Video1 remain unchanged and are not to be replaced or removed.
  > 【Timeline Inheritance】 Each replacement subject inherits the timing, gestures, head positions, and lip movements of the original speaker they replace. All other character actions, camera movement, shot changes, and event order remain as in Video1.

  His note on it: "The most important line is that Video1 is the sole editing master." Post: https://x.com/0xROAS/status/2090502241195098291 (article id 2090492304628842498)
- 2026-08-23, the "cracked" post (a post, not an article; I found no X Article from him dated 08-23): "i've finally cracked seedance 2.5 and 2.0 launching soon. - cut credit costs by 30-40% (no yearly plan) - use better audio reference mode - use better lipsync - better physics" https://x.com/0xROAS/status/2091584303977173425 . Reposted 08-31 with "clear lipsync" and "smaller % of mistakes in video": https://x.com/0xROAS/status/2094482045128814828 . The method itself is behind the paywall. Unverified.
- 2026-08-25, singing ads: "do not generate images, clips literally - chorus confuses AI on what to generate - image-to-video works better ... this cut our ai singing ads production time to less than 1 hour for a 5-6 min video" https://x.com/0xROAS/status/2092269277583716750
- 2026-08-26 and 08-27: "this video is 100% AI... it cost me <$4 per 1 min" https://x.com/0xROAS/status/2092751815880167935 ; "this cost me around $2 - same character - same voice - same movement" https://x.com/0xROAS/status/2093011174619000981 ; "me and @hookrate_ have finally cracked AI UGC with seedance 2.5 ... perimeno girlies are about to be cooked on fb" https://x.com/0xROAS/status/2093019203049501128
- 2026-09-03: "GPT-6 Astra + Wan 3.0 = Crazy AI UGC ... it cost me <$3.8 per 1 min" https://x.com/0xROAS/status/2095555851796795673
- 2026-09-04: "seedance 2.5 not bad for <$6 per 30s" https://x.com/0xROAS/status/2095943235654803926
- 2026-09-07: "V6 + GPT Astra + Seedance 2.5 = $$$ ... V6 is live and updates are being added right as models come out" https://x.com/0xROAS/status/2096932305994396061
- 2026-09-08 and 09-09: "GPT Images 2.5 is literally crazy for realistic images" https://x.com/0xROAS/status/2097401017260179603 ; "here's how GPT Images 2.5 + Seedance 2.5 looks like" (723 likes, 304K views, his biggest post in the window) https://x.com/0xROAS/status/2097672201486872745
- 2026-09-21: "this fully edited video cots me around $50 in kie credits ... a 10 min pixar ad fully automated" https://x.com/0xROAS/status/2102110304281006280
- 2026-09-27, the short swap prompt: "Replace the character in Video1 with the character in Image1" https://x.com/0xROAS/status/2104303018099503270
- 2026-09-29, the single-person swap prompt, quoted in full (968 likes): "Reference Image1 for the character only. Replace the old man in Video1 with the character in Image1, make sure to keep everything else the same. also make sure the color grading is correct and matches the original video." https://x.com/0xROAS/status/2104994366804857003
- 2026-09-30, on an unnamed model: "pros: - really good lipsync - feels natural - looks natural ... cons: - voice issues - sometimes location mixes up" https://x.com/0xROAS/status/2105393532211196125 (the model is not named. Unverified.)
- 2026-10-01, X Article "here's how to make viral videos with Seedance 2.5" (577 likes, 147K views): "Kie ai is just the one that doesn't trap you in a yearly plan ... You're not generating a video from scratch. You're stealing the thing that already got the views ... Image1 is only the character. Nothing else ... use this prompt for character sheet with gpt 2.5: [image] ... The most important line is 'keep everything else the same.' ... 'Reference Image1 for the character only' stops it from pulling the background, lighting, or composition out of your character image. The color grading line stops it from washing the clip". https://x.com/0xROAS/status/2105719128954950142 (article id 2105716458177318912). The character-sheet prompt is posted as an image. Unverified.
- 2026-10-09: "GPT-6 Astra + Seedance 2.5 = Crazy AI UGC ... it cost me <$8 per 1 min" https://x.com/0xROAS/status/2108617328086917231
- 2026-10-13: "here's how GPT Images 2.5 + Seedance 2.5 + motion ref looks like" https://x.com/0xROAS/status/2110019777301446774
- 2026-10-20: "this video is 100% AI. it cost me less than $4 ... i did it in ~10 mins MANUALLY" https://x.com/0xROAS/status/2112581074589045136
- 2026-10-22: "21 AI Drama ads in less than a day. 160+ min of generated and edited content fully by ai ... analyze top 15 drama ads in us - create stories ... create storyboard - generate videos - stitch videos, cut pauses, captions" https://x.com/0xROAS/status/2113071163576390030
- 2026-10-26, motion-transfer prompt: "Apply the source video1 motion to the character in the reference image1, keeping their clothing, the framing and the timing." https://x.com/0xROAS/status/2114868123358662997
- 2026-10-27: "most of the skills in the space are way too bloated ... build the agent based on your style and your videos from scratch" https://x.com/0xROAS/status/2115125953626083666
- 2026-10-30: "generate and fully edit 444 min of ads in the last 7 days" https://x.com/0xROAS/status/2115957174589378735
- 2026-11-03: "1v10 format ... this was done in less than 20 mins with AI ... video is fully edited with OPUS 5.5." https://x.com/0xROAS/status/2117639164669653110

**Numbers he quotes:** <$1 to ~$2 per short UGC clip; <$4 per minute (08-26, 10-20); <$3.8/min with Wan 3.0; <$6 per 30 s and <$8/min with Seedance 2.5; ~$13/min for podcasts; ~$20 for his first Seedance 2.5 UGC; ~$50 for a 10-minute Pixar ad; 10 to 20 minutes per video; "$1B+ in ad spend" through his workflows (bio). He never posts a CPA.

**What changed since August:** at the start of August, Seedance 2.5 was "crazy expensive" and its lip sync was weak, so he used it for hooks and b-roll and Omni flash for talking. From late August he says a reference-audio method makes Seedance 2.5 his all-in-one engine. September brought the reference-video swap (Video1 as the "editing master") and GPT Images 2.5 for faces. October moved to agent editing (GPT-6 Astra, then Opus 5.5) and to drama, Pixar and "1v10" formats over plain UGC.

---

## 2. @pounddz ("Pounds", organic and affiliate AI content)

**What he uses**
- **Image:** "NBP" (Nano Banana Pro), starting from a Pinterest photo.
- **Video:** Omni 1.1 (Gemini Omni 1.1 Flash) is his default for talking heads, animation and organic. Seedance 2.5 (on Higgsfield) for 30-second one-shots and b-roll.
- **Voice:** model-native. He says voice is "the only bottle neck". He credits a "voice trick" to @Mho_23. The trick itself is not published. Unverified.
- **Upscaler:** Topaz. **Editor:** CapCut. **Scripting:** Claude, using his own Claude skill.
- **Research and generation:** solid.tech, Higgsfield.

**Verbatim, with dates and links**
- 2026-07-31 (context just before the window): "Seedance 2.5 + Claude is going to change the game for organic content >Generate 30 second videos in ONE SHOT! >Realism that's unmatched to any other software >50 references per generation" https://x.com/pounddz/status/2083242433748377909
- 2026-08-22: "I just cracked how to do male AI UGC which for a long time has been super difficult to make seem 100% realistic for some reason mens voices always came out sounding so AI" https://x.com/pounddz/status/2091177759468847505 ; then "I recorded my full AI UGC workflow ... If you want it + my Claude skill I use for scripting RT + reply" https://x.com/pounddz/status/2091184482774548561 (behind a DM. Unverified.)
- 2026-08-24, on voice: "Voices / personality in AI UGC is the only bottle neck in making the AI look real And IMO this Flux 3 voices still sound bad Only a handful of people are able to make the voices sound really good" https://x.com/pounddz/status/2091875953672650977 ; "Btw shout out @Mho_23 for showing me the voice trick before he showed anyone else" https://x.com/pounddz/status/2091876222686908635
- 2026-08-27: "Seedance 2.5 is very good for one shotting 30 second clips then extending it with B roll But for >Animation >Over 30 second yappers >Organic content (because of price) Omni wins every single time especially now 1.1 came out" https://x.com/pounddz/status/2093056483608949142
- 2026-08-31 (436 likes, 43.7K views): "Stop using Seedance 2.5 and use Omni 1.1... NOW! >10x Cheaper >10x Faster generation timess >No need to redo the whole video if one thing is wrong >Looks insanely realistic >Voice / body movement is perfect" https://x.com/pounddz/status/2094419914962411699
- 2026-09-01, his exact pipeline: "Upscaling your AI videos can make them look 10x better ... New workflow is: - Pinterest > NBP image - NBP image > Omni - Omni > Topaz - Topaz > Capcut. I most likely won't upscale every single creative still though." https://x.com/pounddz/status/2094792391056085201
- 2026-09-30: "PICK ONE OF THESE FORMATS: >Old VHS drama >Pixar >Hyper realistic drama ... generate the videos in Seedance 2.5" https://x.com/pounddz/status/2105374662427316249
- 2026-10-01: "I didn't just learn a workflow I learned how to: >Direct >Edit >Script >Story tell >D.R market >Colour grade" https://x.com/pounddz/status/2105707169479786947

**Numbers:** "made this AI UGC video in no joke 30 minuets (not including generation time)" (04-09, before the window); "$5k from 500k views" (08-15, about older work); "$38,166 this year from my Whop side hustle" (09-02). No CPA, no per-clip cost.

**What changed since August:** in late July he backed Seedance 2.5 on Higgsfield. By 08-31 he switched talking heads and organic to Omni 1.1 for cost and speed, kept Seedance for 30-second one-shots, and added Topaz upscaling. After that he posted mostly about distribution and business, not stack.

---

## 3. @frankyecom (Franky Shaw, sells the "v5.x / v6" framework, futrgroup.ca)

**What he uses**
- **Models:** he does not name an image, video, voice, lip-sync or upscale model in any post in the window. Unverified.
- **Scripts:** DeepSeek ("unrestricted towards hyper aggressive psychology hacks"), AIDA.
- **Research:** WinningHunter MCP.
- **Course:** "v5.3" (animated framework, 08-15), "v6" announced 08-08 ("Scripting that holds attention, Cinematic b-roll, AI video mastery, Editing for retention & story"). Price on his site per a web search: $47. Not checked by me. Unverified.

**Verbatim, with dates and links**
- 2026-08-08: "Introducing v6 ... While everyone's chasing the newest AI model to sell another guide, I spent my time building a system brands can use to train creative teams." https://x.com/frankyecom/status/2086144216984330597
- 2026-08-19: "Brands can now use the same animated character across every single ad. Same face. Same personality. Same voice. Different concepts every week." https://x.com/frankyecom/status/2090098711988781202
- 2026-09-05: "I also use DeepSeek a lot for scripts since it's unrestricted towards hyper aggressive psychology hacks. Where GPT or Claude set 'ethical' limits." https://x.com/frankyecom/status/2096280638806429835
- 2026-09-15 (873 likes): "We keep trying to make UGC look more 'authentic' when the bigger problem is that the format itself has become predictable. The future isn't making UGC look more authentic.... It's making the ad interesting enough that people forget it's an ad." https://x.com/frankyecom/status/2099949616049631312
- 2026-09-16 (6.6M views, the most viral post in this whole set): "Drama ads aren't just for women ... If you can get someone to watch 30, 45, 60+ seconds instead of 2 seconds, you're creating dramatically more opportunity for Meta to learn" https://x.com/frankyecom/status/2100331741948813730
- 2026-10-04: "Entertainment value is basically the currency you use to earn product attention ... Cheap CPMs. Strong CPAs. Way more scale." https://x.com/frankyecom/status/2106833649970684195
- 2026-10-06: "you can usually tell within 3 seconds when somebody knows AI tools but has never actually studied good creative… the casting is way off, the script is wack, and everything looks muddy." https://x.com/frankyecom/status/2107552431533949012
- 2026-10-14, on realism (his only realism-method post): "the acting coming out of my v6 framework is some of the most realistic i've seen in AI video. the micro expressions, subtle reactions, natural pauses and little mannerisms ... i spend just as much time thinking about how a character should react to a line as i do writing the line itself." https://x.com/frankyecom/status/2110512070546362827
- Before the window, for price context: "$7 in tokens ... In 30 minutes you have an ad like this" (04-14) https://x.com/frankyecom/status/2044097830269124948 ; "an ad like this for under $10. From concept to launch in an hour" (04-13) https://x.com/frankyecom/status/2043812722094014471

**Numbers:** no CPA figures, only "Cheap CPMs. Strong CPAs." Spend is not stated.

**What changed since August:** he moved from "AI UGC" (v5.1 in April) to drama, "dramady" and entertainment-first ads. On realism he now talks about acting direction (reactions, pauses), not models. Reference swaps: nothing posted.

---

## 4. @neverfilmed (account seen from 2026-09-25 only)

**What he uses**
- **Video:** Seedance 2.5 (on Higgsfield) and Omni 1.1 Flash (on Google Flow, free tier credits). Native audio from both: "the voice, the music, all the animation straight from the model".
- **Prompt writer:** Claude Opus 5.5, after it reads Seedance's prompting docs.
- **Separate voice, lip-sync tool or upscaler:** none named.

**Verbatim, with dates and links**
- 2026-10-12: "Omni 1.1 Flash is f*cking insane for AI animation ads it's fast, FREE, actually smooth, and way better at following detailed prompts the character stays consistent & the expressions really land" https://x.com/neverfilmed/status/2109680434632368641
- 2026-10-20, head to head: "Seedance 2.5 (1080p, 30fps) $14 for the 3 clips (480 credits on Higgsfield) ~4 min per clip and it still got the goli product wrong. Omni 1.1 Flash (720p, 24fps) $0 for the 3 clips (45 credits on Google Flow) ~1 minute per clip ... gotta give it to seedance for the better voices though. no reference image on either" https://x.com/neverfilmed/status/2112639565681005006 ; repeated at 720p on 10-22: "$7 for the 3 clips (210 credits on Higgsfield) ~5 min per clip ... I gotta give it to seedance for better voiceover" https://x.com/neverfilmed/status/2113344152012239004
- 2026-10-21: "this whole 28 second spot came out of Seedance 2.5 3 prompts, 3 clips, stitched into one story. the voice, the music, all the animation straight from the model. no juggling 5 different apps" https://x.com/neverfilmed/status/2112951190019543252
- 2026-10-23, full Pixar prompt (excerpt; the full prompt is in the post): "CHARACTER: Hazel [paste LOCKED CHARACTER BLOCK] ... ACTION (one continuous 10-second shot) ... VOICEOVER — OFF-SCREEN narration only (Hazel's voice), first person. Hazel does NOT speak; mouth stays closed. VOICE: a warm, playful 20s American woman ... AUDIO: no music. Only subtle SFX ... IMPORTANT: Hazel does NOT talk or lip-sync — mouth closed and still" https://x.com/neverfilmed/status/2113547141289296082
- 2026-10-28: "the hard part is keeping the exact same girl and her voice across every scene thats what most people cant crack ... how the voice stays identical the whole way through" (workflow sent by DM. Unverified.) https://x.com/neverfilmed/status/2115519190060916751
- 2026-11-02, street-interview reference method: "create your character >find a real street interview on tiktok you like >open Seedance 2.5 >drop in your character image and the interview clip >paste in your prompt ... I use claude Opus 5.5. first i have it read how Seedance 2.5 is actually meant to be prompted, then i tell it: use the interview clip as the reference so it picks up the real camera shake, the way people react to a mic in their face, the natural expressions use the character image as the person then just describe the scene" https://x.com/neverfilmed/status/2117338063034528213

**Numbers:** $7 to $14 for 3 Seedance clips against $0 for Omni; 1 to 10 minutes per clip; "a few dollars in credits" for a Pixar ad.

**What changed:** Omni 1.1 Flash replaced Seedance for cheap animation in October. Seedance came back in November for realistic street interviews, driven by a reference clip.

---

## 5. @Whiskeyatx (agency owner, affiliate background)

**What he uses (from his 10-28 X Article, the most concrete stack in this whole file)**
- **Talking head:** "Wan or Omni". **Voice:** ElevenLabs (paid plan). **B-roll:** Kling through Kie. **Refresh old winners:** Seedance 2.5.
- **Editor:** Claude + FFmpeg (winner); Claude + DaVinci Resolve Studio (gives a real timeline); Palmier Pro (rejected).
- **Upscaler:** none named.

**Verbatim, with dates and links**
- 2026-09-22, swapping old winners into Seedance: "One of the things that helped us do the 1m day last week. Refresh your old videos with seedance 2.5 You know that video that crushed last year? …but the video kinda looked AI? Redo it." https://x.com/Whiskeyatx/status/2102361310893949140
- 2026-09-20: "We took a client to 1M yesterday, One offer, and… Profitably on Day 1 revenue." https://x.com/Whiskeyatx/status/2101710031091831144
- 2026-08-19: "initiate checkout costs for a VSL offer We generally need to be below $35" https://x.com/Whiskeyatx/status/2090055263650787832
- 2026-10-28, X Article "Editing comparison: Claude + FFmpeg vs Claude + DaVinci vs Palmier":
  - "Claude + FFmpeg ... Output: 5 versions, 9:16, about 3:42 each. Production: about 2 h 35 by Claude ... Human time: about 30 min of review. No hand edit. Review rounds: 3 ... Cost: $18.14 in Kie credits (about $4.9 per minute of finished video), plus the ElevenLabs plan. Main issue: audio/video drift from about 2:04, caused by clips a few frames short. Fixed in v4, and the script now checks frame counts before assembling."
  - "Claude + DaVinci Resolve ... Claude time: 4 h 44 ... 48 min was lost to provider failures ... Human time: about 2 h 14 ... Review rounds: 5. Cost: $33.2 in Kie credits (about $7.7 per minute of finished video). Main issues: pauses cut too tight, talking-head repeats not caught, hooks needed judgment by ear"
  - "Our talking-head and voice steps (Wan or Omni, ElevenLabs) stay outside it ... the Kling B-roll on Claude + FFmpeg cost $8.40 for about 2 min through Kie."
  - "Our bottlenecks are generation, talking head, and review"
  - https://x.com/Whiskeyatx/status/2115565599346593935 (article id 2115564311510712320)

**What changed:** in August he posted about structure and media buying. From late September, Seedance 2.5 refreshes of old winners; in October, an agent editing stack priced per finished minute.

---

## 6. @Salifsibane16 (agency, DTC supplements)

**What he uses:** he names no image, video, voice or lip-sync model in the window. He names Suno for song ads. Unverified for everything else.

**Verbatim, with dates and links**
- 2026-08-05: "Meta ... groups creatives by entity id Same background + same talent + same first 3 sec + same framing = ONE ad ... Net-new = new creator, new location, new angle, or a big visual swing Minimum 2 major visual changes per asset" https://x.com/Salifsibane16/status/2084992199033282953
- 2026-08-19: "Iterations with highest success rate: 1 - Swap avatar 2 - Swap format" https://x.com/Salifsibane16/status/2090181761225412799
- 2026-08-25: "$40k spent, winners found in first batch What's working: Statics, pixar-style animations, doctor puppet explainers What didn't hit: claymations, 3D medical animations" https://x.com/Salifsibane16/status/2092326140887416956
- 2026-09-08: "Suno AI song ads ... One is already at $3k/day in spend and scaling" https://x.com/Salifsibane16/status/2097399745887051821
- 2026-10-08, formats with $50k to $100k+ spend in the last 30 days: "Suno songs - AI skeleton animations - Product-focused AI videos - Fake AI founder ads - LF native statics - AI drama stories (new banger) - Partnership ads - Authority figure AI ads" https://x.com/Salifsibane16/status/2108286310251200514
- 2026-10-09, on realism: "Already past $10k/day and scaling Quick tip: start making better AI avatars I don't mean just how real the person looks Hand gestures, movements, pauses, every small detail matters..." https://x.com/Salifsibane16/status/2108603406634152246
- 2026-10-19, compliance: "We made an AI avatar concept based on a real creator ... Client asked us to turn off due to compliance We managed to find the REAL creator and remake the same exact video w him ... yesterday $3.4k spend 2.3 ROAS" https://x.com/Salifsibane16/status/2112317874412859446
- 2026-10-20: "East vs West expert debate with AI avatars Skeptical doctor challenges a traditional healer" https://x.com/Salifsibane16/status/2112634963417792964

---

## 7. @LachezarVoynov (LJV Media, says it oversees "$25M in monthly Meta spend")

**What he uses**
- **Image:** Nano Banana. **Video:** Kling 3.0 (image to video), all models through Kie.ai in his own internal tool. He left Higgsfield.
- **Voice:** ElevenLabs. **Music:** Suno, both built into the tool.
- **Editor:** a custom AI editor built in Claude Code, with Frame.io comments turned into revision prompts and Slack linked to Claude Code for bug fixes.
- **Upscaler and lip-sync tool:** none named.

**Verbatim, with dates and links**
- 2026-09-16, hiring: "Must-haves: - Taste - Experience with Higgsfield" https://x.com/LachezarVoynov/status/2100147206632202577
- 2026-09-22: "These guys are running 30-60min AI ads. Guess they are spending $1k-$2k per ad on Higgsfield ... I thought our agency was spending a lot at 20k/mo for AI video generation" https://x.com/LachezarVoynov/status/2102468111832105225
- 2026-09-24: "People 50+ can't really tell the difference between a UGC and an AI UGC - I have clients spending $1m+/mo on AI UGC and are scaling hard" https://x.com/LachezarVoynov/status/2103119511448949150
- 2026-10-08 (509 likes): "Last month we spent $35,000 on it [Higgsfield] ... Used http://Kie.ai to connect all available image & video generation models to our tool ... another 10% discount with the max allowed top-up on Kie should bring the cost down by ~40%" https://x.com/LachezarVoynov/status/2108263460005875769
- 2026-10-09: "1. An AI creative director broke down the whole storyline of the brief into multiple (100+) coherent scenes 2. Each scene was generated with Nano Banana using a custom prompt 3. Each Nano Banana image was then animated using Kling 3.0 4. The song was created using Suno ... 6. The edit went through 4 revision rounds" https://x.com/LachezarVoynov/status/2108585587494019562
- 2026-10-12: "I've also integrated ElevenLabs & Suno into our tool" https://x.com/LachezarVoynov/status/2109705155666919488
- 2026-10-14: "45s avg playtime on a 2:40-minute ad ... We only introduce the product 2 minutes after the ad had started" https://x.com/LachezarVoynov/status/2110397254985023946
- 2026-10-27: "spent two weeks and over $5,000 building & testing an AI editor ... Scene generation is hooked up to our Higgsfield alternative (using http://KIE.AI), which saves us about $20k/month on video generation" https://x.com/LachezarVoynov/status/2115123558967857628
- 2026-10-29, the honest-cost post: "I've already spent $6k on Claude tokens so far this month just on AI Editing and it's nowhere near being perfect ... video generation (i've done this through http://KIE.AI) which for a ~10min suno song costs $150 - $300 in video gen credits + 2-3 hours for the whole thing including the failed generations ... this whole process takes 6-8 hours" https://x.com/LachezarVoynov/status/2115848163311419620
- 2026-10-29: "you can't fully automate editing with AI yet ... the solution is a human editor + AI editor working together" https://x.com/LachezarVoynov/status/2115831742619607387

**What changed:** he went from Higgsfield (Aug and Sep hiring requirement, $35k/month) to Kie.ai through an internal tool (October), and from human editors to a hybrid AI editor. His ads are Suno songs and "AI movies" more than talking-head UGC.

---

## 8. @runtraffic (Brendan, YouTube and Google affiliate agency)

- No AI video stack named in the window. Unverified. Posts are about media buying (a "GrokBot" agent on Google Ads, Everflow and Sheets), "16x9 SONG Ads" for Mood.com (09-02, https://x.com/runtraffic/status/2095141119340515401), and "$20K/day ... Great time to smash AI ads on YouTube" (10-29, https://x.com/runtraffic/status/2115825695603790256). His TrimRX AI ad post is from before the window.

## 9. @chrisrudy

- Only 3 posts in the window, none naming a stack: "Vox style AI ads are ripping right now" (09-23, https://x.com/chrisrudy/status/2102692476478009747); "My team makes the greatest AI ads" (09-22); hiring copywriters with "experience writing high performing AI video scripts" (10-30, https://x.com/chrisrudy/status/2116122307299348520). The last stack he named was in April (statics: "Nano Banana Pro - Adobe Photoshop - Claude for prompts"). Unverified for video.

## 10. @godofprompt

- 606 posts in the window, almost none about AI UGC video. The closest is a GPT-Image 2.5 reference-role prompt list (09-09): "Multi-reference merge: image 1 = identity. image 2 = clothing. image 3 = environment. image 4 = composition. use each image only for its assigned role." and "Lock the master: this image is the approved master. treat every visible attribute as locked unless I explicitly name it." https://x.com/godofprompt/status/2097520160424993007 . Also: "MiniMax H3 just dropped" (08-08), "10 minute editorial explainer videos with Higgsfield" (08-09). No UGC workflow, no prices.

---

## 11. Viral "how I made this AI UGC" breakdowns (late Sep to Nov 2026)

**@hanifproduktif, X Article "How to create the most realistic AI UGC content", 2026-09-29, 84 likes, 52.8K views** https://x.com/hanifproduktif/status/2104805403699880246 . This is a few days before October, but it is the most detailed realism breakdown in the window.
- Stack: "Google Flow on Google AI Pro, $19.99 a month. Nano Banana Pro for the face, Omni 1.1 Flash for 8-second clips ... Seedance 2.5 for 20 to 30 second one-takes ... ElevenLabs if you want a voice you control instead of the video model's."
- Face: "Use Nano Banana Pro, not Nano Banana 2 or GPT Image 2: the newer models clean the skin too much ... Never fix a face in rounds of edits, because every edit feathers pixels". The character prompt starts: "A single unedited still frame from a vertical 9:16 iPhone front-camera video ... Skin: visible pores, peach fuzz, fine lines under the eyes, slight shine on the nose, uneven skin tone, a naturally asymmetrical face. Do not retouch, smooth the skin, add a beauty filter".
- Omni prompt shape: "SCENE: ... LINE: She says: '...' RULES: One continuous take, no jump cuts, no camera movement, no text on screen, confident pace, natural pauses". Also: "Capitals are intonation. Omni stresses the word you capitalise"; "Durations are 4, 6, 8 or 10 seconds only".
- Voice and lip sync: "The voice comes first. For the hair dryer video I recorded the lines in ElevenLabs v4, then gave that audio to Seedance as the voice to lip-sync. Higgsfield drops audio uploads, so I put the voice track on a plain black video, uploaded it as Video 1, and told the prompt that Video 1 is an audio-only reference: lip-sync to it, ignore its picture. Seedance matched the recording word for word."
- Seedance pacing: "Budget 2.5 to 3 spoken words per second and leave the last second or two silent."
- Cost: "Hook video, 8 seconds, 2 takes, Omni 1.1 Flash 720p: 24 credits ... A full three-clip video is 72 credits, $1.44." Seedance: "60 credits for 20 seconds at 480p, three renders to get the clean one."
- Limits: "Every Omni avatar has the same teeth. Keep the mouth small in frame."

**@OriSilver, X Article "How To Save On Credits When Making AI Ads (based on 15,557 generations)", 2026-10-11, 8.5K views** https://x.com/OriSilver/status/2109300864477282331
- "Gemini Omni Flash is the default for AI UGC. It's cheaper than Seedance, it gives extremely realistic people (if you use the correct reference), and it stays consistent with speech ... Seedance 2.5 or 2.0 is the realistic backup ... it's the most expensive."
- Reference frame: "Don't generate the reference from scratch with Nano Banana Pro or GPT Image 2.5. Use a real one: find a real video on TikTok or Pinterest, take a frame from it, and replace the person with your avatar."
- Voice: "copy the same voice description word for word into every prompt so it doesn't drift"; "Don't use Kling 3.0 for podcasts. Its lip sync is very bad"; "some teams used Veo 3.1 for podcasts, but that model is being deprecated at the end of the month"; claymation voiceover: "Use ElevenLabs V4 or V3 with emotion tags ... Slice the voiceover and attach each slice as the audio reference".
- He works for Maxfusion AI, so the article also sells that platform.

**@codyschneider, 2026-10-22, 7.5K views** https://x.com/codyschneider/status/2113390013136142366
- "seedance 2.5 makes a better talking head for under $5 an ad ... 2. clone a voice once with fal minimax and make the ad read mp3 first 3. pass the avatar photo + the mp3 to seedance 2.5 at 480p so it lip syncs to audio you already approved 4. run whisper on the output and check every word against the script 5. any misspoken word gets spliced back in from the mp3 ... 6. resize to 1080 with ffmpeg + light grain. skip the ai upscaler, it makes her face look plastic". This post promotes graphed.com.

**Related comparison quoted by @pounddz:** @adswithcami, 2026-08-23, 54K views: "Flux 3 voice is unreal Video 1 is Flux 3. Video 2 is Seedance 2.5. Video 3 is google omni" https://x.com/adswithcami/status/2091458195705213394 (pounddz replied that Flux 3 voices "still sound bad").

No Oct or Nov breakdown above ~50K views turned up beyond these. @frankyecom's 09-16 drama post (6.6M views) is the most viral post in the set, but it is about the format, not a how-to.

---

## What they all agree on

- **Seedance 2.5 is the realism default.** Every account that names a video model (0xROAS, pounddz, neverfilmed, Whiskeyatx, hanif, OriSilver, Cody) uses Seedance 2.5 for the most realistic people. Its weak points are price and, early on, lip sync.
- **Omni 1.1 Flash is the cheap talking-head engine.** pounddz ("10x Cheaper"), neverfilmed ("$0 ... 45 credits on Google Flow"), Whiskeyatx ("Wan or Omni"), hanif and OriSilver ("the default for AI UGC") all use it. 0xROAS paired "seedance 2.5 + omni flash" in August.
- **Voice is the weak link.** pounddz calls it "the only bottle neck", 0xROAS lists "voice issues" and accent problems, and neverfilmed and OriSilver both warn about voice drift between clips.
- **The voice fix is to lock the audio first.** Make or clone the voice first (ElevenLabs v4, fal minimax), then feed it to Seedance as an audio reference, or copy the same voice description word for word into every prompt. 0xROAS's "better audio reference method" points the same way, but he keeps the details paywalled.
- **Start from a real video or a real frame.** 0xROAS (Video1 as "the sole editing master"), neverfilmed (a real TikTok street interview), OriSilver (a real frame, not a generated one), the Seedance refresh of old winners (Whiskeyatx) and the higgsfield CLI flow pounddz quoted all copy real footage and swap in their own person. Each reference gets one job ("Reference Image1 for the character only").
- **Build the character once and reuse it.** Everyone makes a character sheet or face image first (GPT Images 2.5 or Nano Banana Pro) and attaches it to every clip.
- **Kie.ai beats Higgsfield on cost.** 0xROAS, LachezarVoynov ($35k/month on Higgsfield, then Kie at ~40% cheaper) and Whiskeyatx all bill generation through Kie. Higgsfield shows up mainly for its free and unlimited promotions.
- **Claude now edits the ads.** 0xROAS (Opus 5.5), Whiskeyatx (Claude + FFmpeg), Lachezar (a custom tool in Claude Code) and neverfilmed (Opus 5.5 writes the prompts) all do it. Cost runs about $4.9 to $7.7 per finished minute in Kie credits, plus human review.
- **Formats have moved past plain UGC.** Drama, Pixar, Suno songs, street interviews and podcasts are what they say is spending. Franky, 0xROAS, Lachezar and Salif all post this.

## Where they disagree

- **Seedance 2.5 or Omni for talking heads.** pounddz and neverfilmed say Omni is cheaper, faster and good enough (neverfilmed: Seedance "still got the goli product wrong"). 0xROAS, hanif and Cody say Seedance 2.5 one-takes look more real, and neverfilmed admits Seedance has "the better voices".
- **Native voice or a separate TTS.** 0xROAS and neverfilmed keep the model's own voice. hanif (ElevenLabs v4), Cody (fal minimax clone), Whiskeyatx and Lachezar (ElevenLabs) make the voice first.
- **Upscaling.** pounddz: Topaz makes it "10x better". Cody: "skip the ai upscaler, it makes her face look plastic", just ffmpeg resize plus grain.
- **Which image model makes faces.** 0xROAS: GPT Images 2.5. hanif: Nano Banana Pro, because "the newer models clean the skin too much". OriSilver: neither; use a real frame and swap the person.
- **Kling.** Lachezar animates everything with Kling 3.0 and Whiskeyatx uses it for b-roll. OriSilver says its lip sync is "very bad" for talking.
- **Full automation.** 0xROAS: "444 min of ads in the last 7 days", "21 AI Drama ads in less than a day". Lachezar: "most of what you read on X about AI Video Editing is cap", 6 to 8 hours and $150 to $300 per 10-minute ad, a human still needed. Whiskeyatx sits in between: 30 minutes of human review for 5 versions.
- **Where realism comes from.** Tool people (0xROAS, hanif) say prompts and references. Franky and Salif say acting and direction ("micro expressions, subtle reactions, natural pauses"; "Hand gestures, movements, pauses"), and Franky says the bigger problem is that the UGC format is predictable, not that it looks fake.
- **Cost per minute.** It ranges from "<$4 per 1 min" (0xROAS) and $1.44 for a 3-clip Omni video (hanif) to $13/min (0xROAS podcasts) and $15 to $30/min (Lachezar's Suno ads). The cheap numbers leave out failed takes and human time. Lachezar and Whiskeyatx count both.
