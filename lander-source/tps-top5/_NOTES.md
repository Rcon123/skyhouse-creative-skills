# Notes — TPS Top 5 lander source

## Saved landers

- **TPS Top 5 - Prostate Flush (final, zip22 2026-07-21).html** — TPS prostate offer. Men's Health Journal-styled VSL bridge advertorial. H1: `NBA Doctor Reveals: The (30-Sec) "Prostate Flush" Giving Men Their Sex Lives Back`. Short pre-sell: story lead → "Real Men. Real Results." testimonial block → "Watch The Video Below" CTA. Sticky CTA bar, countdown timer, fake-comments section, "related articles" thumbnails (related-1..6.jpg), Sponsored/advertorial disclosure line. Every click-out goes to the video.
- **Prostate Advertorial VSL - 3 Mistakes (final, zip21 2026-07-18).html** — TPS prostate offer. Men's Health Journal-styled listicle/graded advertorial into the VSL. H1: `3 Prostate Mistakes You NEED to Fix NOW to Avoid Surgery (Here's How...)`. Structure: 3 mistakes → "The Top 5 Prostate Fixes of 2026, Graded Worst to Best" → "So What's the #1 Prostate Fix of 2026?" (reveal withheld, click to video) → testimonials → Watch Video CTA. Sticky CTA + countdown + comments.
- **Top 5 Skincare Advertorial (final, zip20 2026-07-15).html** — Top 5 Skincare offer. American Beauty Journal-styled long listicle. H1: `Your Face Has TWO Kinds of Wrinkles, Most Skincare Brands Only Target One`. Structure: two-wrinkle-types mechanism → doctor authority ("Why I Tell My Patients to Throw Most Skincare in the Trash") → before/after proof ("Real Women, Real Faces, Just Weeks Apart") → graded countdown through Cerave / Pond's / Neutrogena / Olay → "Who Took the #1 Spot?" reveal → testimonials. Note the earlier sibling (zips 15/19) was branded "American Health Journal"; the final flipped to "American Beauty Journal."

Shared page pattern across all three: fake-publication masthead, Sponsored/advertorial disclosure, hold-the-reveal #1 spot, graded/ranked list device, testimonial wall, countdown urgency, sticky Watch-Video CTA, Facebook-style comments block.

## Preference signals (from feedback_transcript.txt — Ryan x Brandon Ham call, June 16, on the Ancestral Organs listicle)

These are strategy-call takeaways Ryan accepted, not verbatim formatting rules:

- Lead with claims, bury the ingredient. The organs angle up top killed CTR: "maybe the organs is too on the nose and they just don't care" / "make the claims up front and save the organs for the back end." Ryan agreed and moved the claim block to the top of the listicle.
- Benefit order for the men's listicle, agreed on the call: **age first ("feel like you did at 30"), then fat loss / belly fat ("Fat loss just crushes for everything"), then testosterone/TRT ("your testosterone levels skyrocket, TRT, don't need it"), then energy, libido last.**
- Two-direction testing rule: one on-the-nose version ("go direct to top five organ supplements") and one blind claim-heavy version that sinks the unique mechanism late (Marsmen style: "lead with claims and go claim heavy and then support it").
- Headline: big claim over attack, keep "giving men the T-level drive and energy of their 20s," but rename the product reference — "instead of capsule full of organs... Ancient T-booster."
- Aggressive comparison angle approved as a test: "ditching or switching TRT" ("comparing to drugs always crushes. It's just super risky").
- Disqualify-the-alternative lead "crushes all the time"; other proven lead types listed: big benefit, root cause, history/stat, story-based.
- Advertorial QA method Ryan uses with Claude: bullet-point the advertorial line by line and skim the logic chain ("is the copy good... the logic chain is there").
- Build swipes/lists instead of demanding net-new concepts every time; net-new pressure "is probably slowing down output like crazy."
- Sales-letter structure variants to rotate: doctor-educates, personal-story POV of meeting the doctor, top-3-mistakes lead with less disqualify, UMP-heavy no-doctor variant.

Note: the other transcripts named in the project (cloudflare_transcript, cf_transcript*, transcript17, vsl_script, vsl_skin) were not retrievable this session; more formatting-specific rules likely live there.

## Deployment conventions

- **Tracking:** every CTA/click-out uses the RedTrack placeholder `https://trk.skatrk02.com/click` (34 occurrences across the 3 saved landers).
- **Cloudflare upload bundle:** each deploy zip is `upload/advertorial.html` + flat numbered images `image1.jpg ... imageN.jpg` (plus `related-N.jpg` for the related-articles block, `hero-video.mp4`/`.webm` when a video header is used). All asset refs in the HTML are relative to the same directory.
- **Image naming:** sequential `imageN.jpg`, no descriptive names; related-article thumbs `related-N.jpg`.
- **Versioning:** each downloaded zip is a full replacement bundle; highest `TPS Top 5 (N).zip` number = newest deploy for whichever lander was being worked on that day (the zip series interleaves the three families).
- One stray external asset in the skincare lander: author profile pic hotlinked from `d9hhrg4mnvzow.cloudfront.net/read.americanhealthjournal.org/...` (an Unbounce/CDN asset of the swiped source) — worth localizing on redeploy. Testimonial avatars in the 3 Mistakes lander hotlink `randomuser.me`.
