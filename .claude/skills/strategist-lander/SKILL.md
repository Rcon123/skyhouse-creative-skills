---
name: strategist-lander
description: The page builder AND the lander doctrine of the Strategist pack (rewritten 2026-11-02 around vicious copy and vicious images, with Ryan's own pages as the models and every graded lesson folded in). Takes finished advertorial copy (offers/<slug>/advertorials/<angle>-copy.md) and builds the actual deploy-ready static HTML lander plus its Kie-rendered images, in Ryan's house lander system learned from every lander he has shipped. Output is offers/<slug>/landers/<angle>/ containing advertorial.html and sequential imageN.jpg, ready to drag into Cloudflare Pages. Invoke when the user addresses the strategist about building, making, or assembling a lander or advertorial PAGE (not the copy), e.g. "strategist, build the lander", "strategist, turn this advertorial into a page", "strategist, make the akka lander", /strategist-lander, or when the strategist hub routes here. For the COPY, that is strategist-advertorial; this skill builds the page from copy that already exists. Always finishes by handing the page to strategist-lander-qa in a FRESH agent. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic web-page, HTML, or landing-page-building requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus", this skill is not for them.
---
# Strategist Lander: the page a stranger clicks, built the way Ryan builds it

You build and ship landers: the short Top 5, the long-form Top 5, the VSL bridge editorial, the squeeze, the story page. Copy, images, build, checks, deploy. The mechanics (deploy, hosts, cache, gate, the cold reader) are in Part 5 and do not change. Parts 1 to 4 are the doctrine, rewritten 2026-11-02 after the Akka cholesterol long-form went through five rounds of the same mistakes. Ryan, that day: "Does our lander skill need work, like a lot of work, or are we not using it?" Both. "The major issue is the viciousness of the copy and the images."

The bar, in his words: "the thing that sets us apart is that not only do we create the most incredible copy, but the most incredible images and the most incredible ideas out of anyone... there should be no room for mediocrity." "Stop being such a pussy." "Vicious while following the market research and what works for the client, all three." "Shorter forces you to be WAY more vicious." And when a page misses: "we could do so much better."

Read this whole file before any lander work. Then read the model page for the shape (Part 1) and the live control if there is one. A page built from memory of "how we do it" is how every repeated mistake in this file happened.

## HOW TO READ THIS FILE

**Hard rules.** These are never bent:
- On a VSL offer the page is blind: no product name, bottle, price, discount, guarantee, ingredient pitch; every CTA asks for a watch.
- The #1 on a Top 5 is never revealed on the page. The click is the reveal.
- Every CTA is the bare RedTrack link copied from the LIVE control (`curl` it), never from a local file.
- No em dashes, no entities for them. No `text-wrap:balance` on an H1 or H2.
- On a twin of a live page the control's copy stays word for word; the control's slots stay filled with the same kind of thing.
- Before the first review deploy of NEW copy: the gate (`deploy.sh` runs it), one cold read (the judge is a tool, never a gate; at most two reads), a fresh QA agent, your own phone-width look. A CSS, image or one-line fix redeploys without a reread. You never grade your own page. (dreaming 2026-11-02, sessions 10-30_6aaa8a1e, 10-26_601f85f7, 10-28_fe5dc0fa, 11-02_0af56953)
- Deploy only through `tools/landers/deploy.sh`. Changed images get new filenames, and every preview link he gets carries `?v=N`.
- Nothing to ClickUp, Dropbox, a Doc or the buyers before Ryan grades. A preview deploy for his review is fine.
- Every mechanism word comes from the offer's `LANGUAGE.md`. A word you invent goes on the Never list, not the page.

**Taste.** Everything else here is what has worked and what has died, written down so the judgment is his and not a fresh guess. It is how to look at a page, not a fence. When the best idea for this page sits outside it, make it and say why.

## PART 1. WHAT A 10/10 LANDER LOOKS LIKE (his pages are the models; outline them before you write)

Run `python3 tools/landers/outline.py <model.html> <live control.html>` first. It prints words per block, every H1/H2, image and button in order. Size the page to what it prints. Ryan, three times in two months: "go study our long form pages", "go study my landers again", "I just don't think you quite encapsulated it." Every one of those was a page built without opening his files.

**Regular Top 5 (short).** The headline IS the Top 5 ("The 5 'Healthy' Foods Trapping Cholesterol in Your Blood"). Under it ONE deck line about #1, hyperlinked to the #1 block; never an AND/PLUS stack. A hook opener, never "My name is Dr. X". A lead of about 150 to 220 words that names the five more than once. No second image in the lead. Five entries counting down, each a real brand in a hand or on a counter, 3 to 4 lines each. "What is the #1 ..." with the video thumbnail full width and the control's own Watch button. Comments. Disclaimer below the footer. Models: `offers/akka/landers/top5-liver-foods-chol/advertorial.html` (live, the top Akka lander), the OsteoShield Top 5 Toxins page. Rules note: memory `feedback_regular_top5_page_shape`.

**Long-form Top 5.** The H1 is the big idea or the mechanism, one thought ("Your Face Has TWO Kinds of Wrinkles, Most Skincare Brands Only Target One"). The Top 5 becomes the AND line under it and the list's own subhead deep in the page ("The Top 5 Prostate Fixes of 2026, Graded Worst to Best"). PLUS only when it earns its line. Lead 200 to 280 words. Then 3 to 5 sections of 90 to 150 words, each with one image and one claim subhead of 8 to 11 words. ONE proof block mid-page. Then the list (5 to 2), the #1 hold with the thumbnail and button, comments, the button again. 730 to 1,600 words all in. No video block under the lead, no bridge paragraph, no sub-lines on buttons the control does not have. Models: `lander-source/tps-top5/Top 5 Skincare Longform - Plain Article.html` (1,512 words), `Prostate Advertorial VSL - 3 Mistakes (final, zip21 2026-07-18).html`, and the graded Akka twin `offers/akka/landers/top5-liver-foods-lf-1955/advertorial.html` (1,569 words: control lead, three sections, proof, ranking section, list). When the long-form iterates a live page, the control's words stay and the new writing is an insert of about 400 to 500 words.

**VSL bridge editorial.** Five sections of 110 to 215 words, two Watch buttons, 900 to 1,050 words. Model: `lander-source/tps-top5/Prostate Advertorial v4.html`.

**Squeeze.** 150 to 350 words, the H1 stands alone (no stack), no subheads at classic length, the fix held unnamed, a benefit montage in concrete pictures, "In this short video..." then the button, "Real People. Real Results." and comments. The full shape: `strategist-references/swipe-learnings.md`, SQUEEZE PAGE FORMAT. A squeeze that teaches the mechanism in flat prose is "boring".

**Story lander.** First person, RJV density: 1 to 2 sentence beats, bold / italic / yellow highlight rotated so almost every beat has a landing point, one-line paragraphs legal. Model: `offers/tps/landers/top5-story-insider/advertorial.html`.

Which shape is Ryan's call, made before the copy. If it is not stated, ask in one line; building the wrong shape wastes the run (and "regular top 5" never means the long control with less copy).

## PART 2. THE LAWS

### 00. VICIOUS, HIS WORD FOR WHAT IS MISSING (2026-11-02: "the major issue is the viciousness of the copy and the images")
In copy, vicious is the ugliest TRUE thing the research says she is afraid of, said in the plain words she says herself, aimed at her or at the villain, first try, with no soft option beside it. "Default to the hardest true version, first try, every time. Plain words. Real nouns. No apology." The villain is a person when the research has one (her doctor who says "very common at your age", the pill for life, the cardiologist who never checked her liver). More of her research words in one line that still reads as English is more vicious ("tons of keywords, super vicious"). What vicious is NOT: insults, cleverness, metaphors, literary intensity, a mechanism nickname she has to decode, a hedge, a disclaimer, "may / might / some people". A subhead or line that needs a second read is not vicious however hard it hits; it is dead (law 0).

In images, vicious is her ugliest true fear shown flat in her own house, or the villain done violence: the 14-slot pill organizer like her mother's, the commode by the bed, her pills in the toilet, the statin bottle burning at her breakfast table, her hand flipping off the doctor, the doctor with his head in his hands over her lab sheet. One wrong or impossible thing in a picture she already knows, read in one second. What it is NOT: a still object on a table with a note on it ("very boring image, doesn't do anything for me"), a format costume (crayon, vintage ad, receipt, whiteboard as the idea), staged drama, a face acting, a prop in a hand, a clean full-resolution render ("super AI and fake, too staged, the paper looks fake").

### 0. Dead simple or dead
If a line, a subhead or an image is confusing, not relatable, not crystal clear or not specific, it is dead, however vicious. "Confusing as fuck" has killed more subheads than politeness ever has. Every referent named. No device she has to decode ("Refill", "ALT", "the exit" before the page has said what the exit is). Every line a 58-year-old on a phone can repeat back in one plain sentence after one read.

### 1. The skim test (his rule "to remember at all times")
A skimmer reads the H1, the deck lines, then every subhead in order, and nothing else. That chain alone must tell the whole story with zero confusion. Every referent in a subhead is defined by the H1 or an EARLIER subhead, never by body copy. Each subhead is one sentence, 8 to 11 words, a complete claim naming the real things (the statin, the liver, the cholesterol), carrying the pain or the villain, in her words. Never a scene ("Strangers kept asking me what was wrong"), never a side concept, never two sentences, never long ("this is really long for a sub headline, and also very boring"). Before anything else, write the chain in one place and read it aloud cold.

### 2. Readable on a phone, which means beats, not fragments
No paragraph over two or three phone lines. One idea per line. Whole spoken sentences with their connectives, the way a person talks; never chopped fragments to hit a grade score ("writing like a fucking robot"), never five-sentence paragraphs ("massive, unreadable"). "Chunky" is his word for both a long paragraph and a mechanism stacked three ideas deep. Bold is a skim beat, one per screen, the claim the skimmer acts on, never a mechanism clause; "all the black bolding lines is horrible". Italic whispers. Yellow highlight on 2 to 3 payoff lines a page, only where the skin has it. Blue underlined links exactly where the control has them. Photos full width, no frames. Byline on one line. Nameplate small, fonts plain.

### 3. The headline
One sentence. His shapes (swipe-learnings HEADLINE FORMULAS): authority stunned + nickname + parenthetical; symptom question + fix; authority command; enemy betrayal; dual benefit AND; spectacle; contradiction; the winning ad text in quotes. Devices: ONE quoted word, ONE caps word, a number or time, a parenthetical; credibility opens ("Top NYC Gut Doctor:"); the reveal is never spent after a colon; the first three or four words carry it. Plain English: no nickname she must decode, no abbreviation, no "it" without a noun. Long-form: the big idea in the H1, the Top 5 in the AND line. When he asks for headline options he means DIFFERENT shapes, ten or more, in one file he can open, not ten variants of one idea ("I asked for different headline options, and I didn't get them").

### 4. The deck
Regular Top 5: one line about #1, hyperlinked. Long-form: AND carries the Top 5; PLUS only if it adds a second real promise. Short. Never promise a thing the next page does not deliver ("why would we mention a 30-second morning ritual?").

### 5. The lead
A hook opener about the phenomenon ("What the hell changed?"), the big claim early, the five named more than once on a Top 5, benefit before mechanism. On a twin, the control's lead stays word for word; you may split it one idea per line, nothing else. "You don't need to rewrite the copy that's already on the lander."

### 6. Congruent with the funnel
The ad sells the page; the page sells the click to the video; the video sells the bottle. The page delivers the ad's promise in the ad's words. Every mechanism line comes from the VSL (the read in `research/`) or the winning ad texts, and the page never promises a thing the video does not pay off. Never "just cut these foods and it's fixed"; it "starts with five foods". The reader is at the awareness level the ad brought her to, never product-aware on a VSL offer. Before writing, read `OFFER.md`, `LANGUAGE.md` and the VSL read; after writing, check every tease against them.

### 7. Every section has an image, and the image does something
A section with no photo is a wall. Each slot is ONE line of this page made visible as one wrong or impossible thing happening, in a picture she already recognises, with the subject plainly visible and nothing else competing. Before the first prompt, write per slot: the page line it is, what a stranger says she sees in one second (five words; more than five means not simple yet), and which register from the offer's live strip (`landers/*/image1.jpg` and `image2.jpg`) it sits in. The full craft is `.claude/skills/strategist-images/SKILL.md`; these are the lander-specific points:
- The hero is one page line as one impossible real thing, crisp, no feed-candid blur; match the live hero strip's register. Give options on one sheet before placing a hero or thumbnail when he asks for options; otherwise render round 1 and let him grade.
- Section images: real phone photos of real things (gpt-image-2 with a phone-photo tail), the pan caked in yellow wax labeled TRAPPING CHOLESTEROL, the statin bottle on fire at her table. Never a still object with a note. Labels that ARE the proof are not "text".
- People only through the realism stack: z-image flash candid, degraded like a 2014 phone photo, crooked, cluttered, eyes into the lens; the change as an image-to-image edit of the same frame; never a text-to-image face, never a clean render, never a prop in the hand. Hero slots stay crisp.
- Handwriting must be ugly: uneven, crooked, smudged, cramped at the edge, or move the line to a paper sign. Clean marker reads AI ("this handwriting's too good").
- Backgrounds matter: a hospital hallway behind a doctor got "I'm not a fan of the background"; a plain wall passed.
- A section image never repeats the hero's device. Every slot the same 3:2 height.
- Hand-built UI (portal, text thread, notes app) is HTML flattened with headless Chrome, never AI. Use it for ad statics; on a lander it is not social proof (law 8).
- Real people with names (the doctor) use the real approved headshot, never a generated face.

### 8. Proof: what a real person would actually show, stating the claim in words on the frame
Social proof only reads when the picture itself says the claim: the same face twice when the result is visible (skin, weight, a jaw), one real photo with her own line across it when the result is a number nobody can see (cholesterol: "263 to 192 in 12 weeks. I never took the statin."), or someone reacting to her. Each proof carries one line a stranger reads in one second, in her words, with the thing named and the win in it. What died on the Akka long-form in one week, each one graded by him: printed lab sheets taped to a fridge ("horrible, fake, not social proof"), a prescription bottle in the trash ("no one would show this"), a lab sheet with red pen ("okay, very very AI"), portal and pharmacy screenshots (not pictures of people), people holding printed sheets ("super AI, too staged, the paper looks fake"), then/now face pairs with date labels for an invisible result ("I don't even understand what I'm looking at"). The before/after pair (law 12 in the image skill) is for visible results only, through `pairs.py`, both halves degraded, different world in each half. Captions under proof photos 20px with a 17px name; quotes 15 to 30 words that name the thing and end on a win she would brag about ("off the statin, eggs every morning, my legs don't ache at night"). Comments: short, named, the thing she clicked for named, a big life win, one reply that links the video; never a phrase lifted from the VSL because it is "true to the source".

### 9. The hold and the close
Count down 5 to 2, hold #1: "What Is the #1 ...?" with a lowercase is and a specific hold. The close names the discovery and the payoff in plain nouns (the #1 food, the 30-second thing, the number dropping on the next blood test) and a reason to do it now; bullets benefit first, every noun named, no teases copied from the video's own bullets. The thumbnail full width with a play button, the control's own button, the comments, the button again. The CTA copy is laid out exactly as the doc has it; drift at the buttons is the pilot's failure mode.

### 10. Twins, format tests, re-angles
A twin of a live page keeps every slot the control has (strip, eyebrow, H1, deck, byline, hero, lead, sections, reveal, comments) filled with the same kind of thing; only the words and the picture inside change. A format test keeps the idea, the look and the copy and changes only the delivery. A re-angle swaps the frame lines (the subject of the H1, 2 to 3 woven sentences), never bolts on clauses. When he says he loves the copy but it is long, cut lines; never re-voice the ones that stay.

### 11. One review surface, one version per round
He grades one clean place: the live preview link and one image sheet in chat. No side files, no extra rounds he did not ask for ("look at all this crap I have to look at"). A note from him fixes the flagged line, then you re-read the whole piece once, then show it. The judge runs again only on changed copy and only if it has run once before (two reads is the cap, 11-02). "I like this / I still want to keep that" locks that element verbatim.

## PART 3. BUILDING A PAGE: THE PREFLIGHT, IN WRITING, BEFORE ANY SECTION EXISTS

1. **Shape** from Ryan (Part 1). Not stated: ask in one line.
2. **Outline** his model page and the live control with `tools/landers/outline.py`. Write the target: words per block, section count, subhead length, where proof sits.
3. **Read** `OFFER.md` (funnel type, red lines), `LANGUAGE.md` (their words, never list), the VSL read in `research/`, the winning ad texts the traffic arrives on, the live control's hrefs (`curl`).
4. **Write the skim chain**: H1, deck lines, every H2, in one block. Read it aloud as a stranger. Fix it before a single section is written.
5. **List every image slot**: hero, each section, proof, thumbnail. Per slot: the page line, the five-word read, the register from the live strip, the kind of proof the offer allows (law 8).
6. **Write the copy** in beats (law 2). Run the mechanical check; a paragraph over three phone lines is a fail.
7. **Build** from the control or model block by block. Keep the control's words. Any CSS insert matches the FULL selector (`h2.sec em{`, not `.sec em{`; the substring match silently un-styled a whole block once).
8. **Render** round 1 immediately, in the background, while the HTML builds. Pick as him. Place under new filenames whenever a published page's images change.
9. **Check**: the gate, one cold read on new copy (flags as notes at the top of the deliverable; flags on locked control lines are his call; at most one re-read; never on a CSS or image swap), a fresh QA agent, your own look at phone width (the pane's mobile preset or Playwright at 390; never headless Chrome, which clamps to 500px) with every image confirmed loaded.
10. **Deploy** through the gate, verify the live page and every image, hand him the link (with `?v=N`) and the image sheet in chat. Every image swap gets a new file name.
11. **His notes**: pull the Loom transcript AND the frames; pin every "this" to a frame before changing anything; apply every note; then screenshot the served page at phone width and check each note against it before replying; log the grade in this file (Part 4) the same day.

## PART 4. READING HIS GRADES (what each word means, and what the next round does)

- "chunky" / "could be more readable": paragraphs past two phone lines or three ideas in one sentence. Cut to beats, same words.
- "confusing as fuck" / "I don't know what that means": a device or an undefined referent in a subhead or line. Say the plain thing.
- "too long" (a subhead, a deck): cut words, not the idea; 8 to 11 words.
- "boring image" / "doesn't do anything for me": a still object. Make something happen to her or to the villain.
- "fake" / "staged" / "super AI": a clean render, a prop in a hand, perfect paper, a posed person. Realism stack, degrade, no props.
- "doesn't make any sense" / "I don't understand what I'm looking at": the picture needs decoding. The claim goes in words on the frame, or the picture shows the visible result.
- "not social proof" / "no one would show this": not what a real person would post. Law 8.
- "handwriting's too good": ugly it up or move it to paper. "not a fan of the background": plain wall.
- "go study my landers" / "didn't encapsulate it": wrong shape. Outline his files, rebuild the skeleton.
- "I didn't get the options": give ten or more DIFFERENT shapes, in one file, not variants of one idea.
- "vicious" / "weak" / "pussy" / "vanilla": law 00. The harder true fact in plainer words; her fear flat in her house.
- "random" / "not related to the story": not a line from this page. Quote the line, then render it.
- "why would we mention X": the page promises something the next page does not deliver. Cut it.
- "I like this" / "keep that": locked verbatim. Change nothing around it that makes it read differently.
- "we could do so much better": the whole round was inside the lines and still ordinary. Start from the page's own line and her own fear, not from the last round.

# PART 5. MECHANICS (unchanged; every line below was paid for live)

## RYAN'S 3 GOLDEN RULES (told to every lander build, from the Fernando process call)

1. **Mobile-optimized.** 95% of the traffic is mobile on paid. Build mobile first and check at 390px before anything else.
2. **Page speed and quality maxed out.** Compressed jpgs under ~110KB, hero preloaded with `fetchpriority="high"`, everything below the fold `loading="lazy"`, fonts preconnected. Ryan: "if you don't tell it that, your landing page CTR drops like crazy."
3. **Proper tracking links.** Every CTA points at the RedTrack link, bare, no query params: `https://trk.skatrk02.com/click`.

Plus: **bold for the scanners** (only the important phrases, never random bolding), **italic to whisper**, and leave the Microsoft Clarity hook in place for heatmaps.

## Deployment conventions (match these exactly)

- One flat folder: `offers/<slug>/landers/<angle>/`
- One `advertorial.html`
- Images named `image1.jpg`, `image2.jpg`, ... in page order
- Nothing referenced outside the folder except Google Fonts
- No hotlinks to competitor CDNs or avatar services. Every asset is local.
- Optional `_headers` for Cloudflare cache policy (assets immutable 1 year, HTML 5 minutes)

## Format is decided BEFORE the copy, not by you

The page type is Ryan's call and it gets made in `strategist-advertorial` at step zero (squeeze / top five / long-form top five / editorial / listicle / comparison). If you are handed copy whose format is ambiguous, ask rather than guess. Building the wrong page type wastes the whole run.

## Format library (pick by the copy's shape, from Ryan's shipped landers)

- **Fake-publication editorial advertorial** — masthead, sponsored bar, dateline, byline, big serif headline, hero, flowing sections with Archivo subheads. The workhorse. Models: `lander-source/tps-top5/Protaflo Advertorial Longform.html`, `Prostate Advertorial v4.html`.
- **Top 5 listicle** — masthead, breadcrumb, ranked entries counting down, hold-the-reveal #1 box, comment section, sidebar. Model: `lander-source/misc/lander-design-review/`.
- **10-reasons listicle** — countdown bar, sticky CTA, numbered reasons with a photo each, FAQ accordion, scroll-reveal. Model: `lander-source/mofo/10-reasons-mofo.html`.
- **VSL bridge editorial** — cards with image slots, mid-page and final watch CTAs. Model: `Prostate Advertorial v4.html`.
- **Comparison page** — cloned competitor structure. Model: `lander-source/page-replication/`.

## Build sequence

1. **Read the copy and mark the image slots.** The copy doc carries `[IMAGE SLOT n: ...]` descriptions written for the designer. Those are your render briefs.
2. **Fire the Kie renders first**, in the background, so they cook while you build the HTML. Mechanics live in `.claude/skills/strategist-images/formats.md` (gpt-image via the 4o-image endpoint, poll, download). **NEVER nano-banana-pro.** Landscape for in-page slots (the endpoint takes 3:2, not 16:9). Compress each result to jpg under ~110KB with `sips` (note: recompressing an already-compressed jpg at similar quality does nothing; resample down AND drop quality).
   - **Lander images are AD images (Ryan, graded 2026-08-05, squeeze pilot).** The full strategist-images doctrine applies: holy-shit bar, clarity bar, one focal point, LOUD.
   - **SUPERSEDED by Part 2, law 7 (2026-11-02): the live Akka pages and every keep since September are phone-real photos of real things, and the format library is a wardrobe, not the idea. Kept for history:** **RENDER THROUGH THE FORMAT LIBRARY, NEVER FREEFORM PHOTOREAL (Ryan, graded harder 2026-08-05: "fake stock-photo dog shits").** Use the exact approved prompt blocks in `.claude/skills/strategist-images/formats.md` (watercolor, drawing/KO-journal, neon, crayon, claymation, diorama; timestamp-candid is the ONLY photoreal that ever passed). Format block + scene + tail, horizontal for landers. Freeform "cinematic photorealistic" prompting is what produces the stock-photo look and is banned. Quiet conceptual renders (a subtle glowing organ on black) fail exactly like quiet ad images fail. Ryan's shipped register, from his own TPS deploys: the HERO is a bold illustrated action scene of the mechanism literally happening with dramatic energy VFX; the VIDEO THUMB is a busy VSL-style collage (2-3 curiosity elements: mechanism visualized viscerally, a time device like a stopwatch, the payoff) that looks like a real video.
   - **Squeeze video-thumb treatment (his .thumb pattern):** thumb image wrapped in the RedTrack anchor, bottom dark gradient, play affordance, and a yellow pill badge with red play circle + "WATCH VIDEO" in thick caps. Compose badge, doctor photo, and any text as HTML/CSS overlays, never baked into the AI render — crisp text guaranteed, and the real face stays real.
   - No captions or slogans baked into lander images; labels that are the proof, marker on a real object, and her own line as a caption bar (law 8) are allowed.
   - Every image stages a moment the copy actually says. No invented adjacent drama.
   - Real people (a named doctor) use their real approved headshot, never a generated face. The offer's own funnel pages are the source for the real headshot.
3. **Assemble the HTML** from the format model plus the copy, block by block. Keep the copy word-for-word; you are laying it out, not rewriting it.
4. **Verify in the browser pane**: 390px first, then desktop. Check console and network.
5. **Hand off to QA**: spawn a FRESH agent running `strategist-lander-qa`. You do not grade your own page.
6. **Apply the QA fix list surgically.** Keep every unflagged line word-for-word. Re-render only the flagged images.
7. **Present to Ryan**: the mobile screenshot, the desktop screenshot, and the folder path. Never make him dig.

## The two failure modes this builder actually has (graded, pilot run 1, 2026-08-05)

1. **Drift at the CTA blocks.** Every unapproved line in the pilot was in a button, a sub-line, or a CTA headline. Lay out the CTA copy exactly as the doc specifies, or back-port your change into the doc in the same pass so the two never disagree.
2. **Silently dropping a slot that needs a real asset.** The pilot dropped the doctor-headshot slot because it could not be AI-generated. Never quietly skip a slot. Leave a commented placeholder naming the missing asset, and report it as a blocker.

Also graded in: **check CTA button text against its position on the page.** A button that names a person placed before that person is introduced is a referent violation, which is the error class Ryan grades hardest. And **paragraph length is the builder's job too**: if the copy doc hands you a 9-line phone paragraph, break it and fix the doc.

## Rules

- The copy is approved. Do not improve it, trim it, or reword it while laying it out. If a line genuinely cannot be laid out, raise it, do not silently change it.
- No em dashes anywhere, including HTML entities.
- On a VSL offer the page is blind: no brand, bottle, price, discount, guarantee, benefit bullets, comparison table, or product testimonials, and every CTA asks for a watch. This is a funnel rule, not a style preference.
- Never write into `state/`, `references/`, or `.exodus/`. Never run `npx exodus`.
- Update the offer's PLAN.md lineup when a lander ships.
- New graded lessons from each build session get appended to this skill and to `lander-source/_CATALOG.md`.


## DEPLOY (wired live 2026-08-05, Ozempic Face lander)

Ryan's landers are served from the Cloudflare R2 bucket `landers-prod` (account `ad6991edae13144d309c95ac258213c7`, creds in `.env`: CLOUDFLARE_API_TOKEN with Pages Edit + Workers R2 Storage Edit, CLOUDFLARE_ACCOUNT_ID).

Structure (CORRECTED 2026-09-01, StoryInsider deploy): the top-level folder is NOT the bare public
hostname. It is `<lander-slug>-<hostname>` (e.g. `hero-tps-news.americanbeautyjournal.org/`), and a
Worker called `landers-router` (bound to LANDERS_BUCKET=landers-prod + KV LANDER_SCRIPTS) maps the
public hostname (`news.americanbeautyjournal.org`) onto that folder. One subfolder per VARIANT:
`landers-prod/<slug-hostname>/<VariantName>/advertorial.html + image1..N.jpg`. Peer TPS variants:
Plain, OzempicFace, LF-Feminine, TPS-SelectWrinkles, twowrinkles1-3, StoryInsider. Uploading to a
bare-hostname folder serves NOTHING; check the bucket root listing for the real folder name first.
The page is live at `https://<public-hostname>/<VariantName>/advertorial.html` immediately after
upload, no DNS step needed for hostnames already routed (news.americanbeautyjournal.org is).

Deploy after QA passes:
```bash
export CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=...
npx wrangler r2 object put "landers-prod/<host>/<Variant>/advertorial.html" --file=advertorial.html --content-type="text/html" --remote
# then each imageN.jpg with --content-type="image/jpeg"
```
Verify with `GET /accounts/<acct>/r2/buckets/landers-prod/objects?prefix=<host>/<Variant>/`.

NOTE — THE LIVE URL MAPPING (learned the hard way 2026-09-01, Akka LF deploy): the bucket FOLDER names (ancestral-mofo-info.americanlivingjournal.com/...) are NOT the live hostnames. The live site is https://info.americanlivingjournal.com/<Variant>/advertorial.html and it serves the bucket's ancestral-mofo-info.americanlivingjournal.com/<Variant>/ keys through serving plumbing not visible to this workspace's scoped token (no zone perms). So: UPLOADING TO THE BUCKET *IS* THE LIVE DEPLOY. Verify by fetching https://info.americanlivingjournal.com/<Variant>/advertorial.html directly, and pull the destination URL for any live campaign from RedTrack landings (REDTRACK_API_KEY in .env) rather than guessing from folder names. Do NOT stand up Pages projects as stopgaps; the live domain works.

## GRADED IN (Ryan, 2026-09-01, TPS story lander): STORY COPY GETS THE RJV TYPOGRAPHIC DENSITY

Ryan's grade against the RJV control: our page was "harder to read, not many bolds/highlights where they should be, more chunky and longer." The readable register, taken from the RJV story lander:

- Paragraphs are 1-2 sentence beats. A paragraph with two scenes in it gets split.
- Rotate FOUR emphasis treatments through the copy so almost every beat has one landing point: **bold** (names on intro, slap phrases), *italic* (whisper/aside lines), underline (mechanism claims), and yellow highlight (2-3 payoff lines per page, no more).
- The plain-design skin kills `.hl` backgrounds to bare bold on purpose; for story variants add a `.mark` class AFTER the plain-skin override block so the yellow survives (see top5-story-insider).
- One-word or one-phrase standalone paragraphs are legal and good ("She laughed at me.").

## CACHE LESSON (2026-09-01, Akka LF lander, graded live by Ryan: "i still see the wrist band")

The `_headers` convention gives every asset `max-age=31536000, immutable`. That means REDEPLOYING CHANGED IMAGES TO THE SAME FILENAMES leaves every prior visitor (including Ryan) staring at the old images: the browser never re-asks. Any time an already-published page's images change, RENAME THE FILE (`image2.jpg` -> `image2b.jpg`) and update the HTML references. A `?v=2` query bump was tried first and Ryan still saw the old image (the stale cached HTML references the unversioned name, so the query never reaches the browser until the HTML cache expires); a new filename is the only fix that cannot be defeated by a stale page. Hand Ryan the per-deploy hash URL (https://<hash>.<project>.pages.dev, printed by wrangler) for instant verification: a hostname his browser has never cached. Fresh variant folders don't have this problem; same-URL iteration always does.


## IMAGE SWAPS AND LOOM NOTES (8c, dreaming 2026-11-02, sessions 10-28_21a10a66, 10-27_476ca5f9, 10-27_d3faba13)

Ryan, three times in one session: "No, you didn't make the changes. I immediately looked at it." He was looking at the cached old picture. And after a Loom: "No, that fucking thing on the side is still there." The note was reported done and was not done on the served page.
- Every image swap gets a new file name (`image2.jpg` -> `image2b.jpg`), never the same name re-uploaded.
- Every preview link he gets carries `?v=N`, N up by one per deploy, so his browser fetches fresh HTML.
- After a Loom: apply the notes, deploy, then screenshot the SERVED page (the live URL, not the local file) at phone width and check each note against that screenshot before replying. The reply lists each note with "done, seen on the live page" or "not done".

## PHONE-WIDTH SCREENSHOTS (9h, dreaming 2026-11-02, sessions 11-02_322d89c5, 10-27_d3faba13)

Headless Chrome clamps window width to 500px: a `--window-size=390,...` capture is silently rendered wider and right-clipped, so it is not a phone shot. For a true 390px look use the browser pane's mobile preset or Playwright at 390 (`page.set_viewport_size({"width": 390, "height": 844})`). Treat a narrow headless capture as an approximation only.

## HOST RULE (2026-09-10, TestoGreens Top 5 Testo deploy): DO NOT PASTE THE REDTRACK unilpclick.js TAG ON info.seniorvitalitymagazine.com

The `landers-router` Worker injects `https://trk.skatrk02.com/unilpclick.js?...` into every page it serves for this hostname (check any live page's source vs the R2 object: the live copy has the tag, the stored file does not). A page that also carries the tag in its own HTML loads the script twice and throws `Identifier 'referrer' has already been declared`. Ship the page with only the Clarity tag; leave RedTrack to the router. Verify after upload with `curl <live url> | grep -c unilpclick` (expect 1).


## HOST RULE (2026-09-18, REA Beauty Cell squeeze): info.themodernamerican.org INJECTS CLARITY TOO

On this host the `landers-router` Worker injects both the Clarity tag and RedTrack unilpclick.js. Ship the stored HTML with NO tracking tags at all (the stored salt-squeeze file has none). Verify live with `curl <url> | grep -o 'clarity.ms/tag' | wc -l` (expect 1); `grep -c` counts lines and reads 1 on minified HTML even when the tag is doubled.


## GRADED IN (Ryan, two Looms 2026-09-22, REA salt long-form)

- Subheads never wrap short: no `text-wrap:balance`, no narrow max-width on h2. Every subhead (section, proof, comments) is CENTERED and the proof title is as big as the section subheads.
- Body text uses the whole column. A `max-width:64ch` on paragraphs left "all this white space on the right"; drop it inside the 840px main.
- No underline emphasis ("looks really f***ed with these gaps"). Rotate bold and yellow highlight only.
- Quote captions under before/afters are 20px with a 17px name; 17px was "so small I can barely see these".
- A strong line the copy hammers (the 89/86 line) goes in the control's callout-box style, not just bold.
- Section image "options": Ryan wants 4-5 alternates per slot on a contact sheet, more curiosity than the literal copy illustration; he picked in-photo writing (sticky notes, a taped note) over the plain photo every time.
- No Watch Video button inside a proof block; proof photos from the control go back under the thumbnail + button where the original had them.
- Testimonial words must fit the 65+ reader: "my boyfriend" at 68 read weird; "my husband".
- Read a Loom with the frames, not just the transcript (memory: loom-transcript-and-frames).

## HARD RULE (2026-09-22, REA salt long-form, $94 at 0% lander CTR): CTA HREFS COME FROM THE LIVE PAGE
Before building a variant, `curl -s <live control url> | grep -o 'href="https://[^"]*"' | sort | uniq -c` and copy those hrefs exactly. The local folder can be stale (the salt-squeeze local copy still had the direct EF link a month after the live page moved to the bare RedTrack link). House CTA is `https://trk.skatrk02.com/click`, bare; the offer is on the RedTrack stream. After deploy, open the live page with `?rtkcid=test` and confirm every href rewrites to `trk.skatrk02.com/click?clickid=test`; if it does not, the page is not tracking and must not take traffic.

## DEPLOY ONLY THROUGH THE GATE (2026-09-22, Ryan: "we create landers literally every day. this can NOT happen again")
Never call wrangler by hand. Deploy with `tools/landers/deploy.sh <local folder> <bucket host folder> <variant> <public host>`. It runs `tools/landers/gate.py` first and refuses to upload if any `<a href>` is not the bare `https://trk.skatrk02.com/click`, if a tracking tag is baked in, if a dash is present, or if a referenced image is missing or over 110KB. After upload it re-runs the gate on the LIVE page and checks every image returns 200. Then open the live URL with `?rtkcid=test` in the browser and confirm every href rewrites to `click?clickid=test`. A page that fails any step does not take traffic.

## NOTE (2026-10-06, REA experiment squeeze): THE ?rtkcid=test REWRITE IS NOT VISIBLE ON LOAD ANY MORE
Opened the new page AND the live tracked control (salt-squeeze-tabloid) with `?rtkcid=test` in Chrome: both show the bare `https://trk.skatrk02.com/click` hrefs, unilpclick.js present once, no rewrite on load. The built-in browser pane blocks unilpclick.js outright (ERR_BLOCKED_BY_CLIENT), so never run this check there. Working test until RedTrack's script is re-read: the new page must match the live control byte for byte on hrefs and tag counts (gate --live does this).


## FIX (2026-10-13, OsteoShield termites staging): deploy.sh and gate.py now cover EVERY referenced local image
Both scripts matched only `src="image*"`, so a page with avatar1..12.jpg (comment faces) deployed with twelve 404s and the live gate still passed. They now match any local `src="*.jpg|jpeg|png|webp"`. Name comment faces whatever you like, but after any deploy, curl one non-image* asset on the live host to confirm it is 200. Also: the session's auto mode refuses deploy.sh as a production deploy; Ryan runs the command himself from the terminal, so hand him the exact line.

## HOST NOTE (2026-10-22, OsteoShield one-thing-lf deploy): info.americanhealthjournal.org now injects TWO unilpclick tags
Someone added a second RedTrack default-campaign tag to the router for this host on 10-22 (defaultcampaignid 6ada46ad = "IGNORE - BOTS - Skin - NutraHero - Unattributed Traffic (10.22.26)", cookiedomain info.americanhealthjournal.org) next to the old SCR one. Every live page on the host, controls included, now serves unilpclick x2 and Clarity x1, so `gate.py --live` with the fixed "expect 1" fails a correct page. Fix shipped: `gate.py <live.html> --live --control <live control url>` and `CONTROL=<url> tools/landers/deploy.sh ...` compare the new page's tag counts with the control's. The rule is unchanged: the new page matches the live control exactly; the stored HTML still carries no tags. Flag a doubled tag to Ryan/Calvin rather than "fixing" it in the page.

## COLD-READ JUDGE (built 2026-10-27; ship block removed 2026-10-30; read cap and scope 2026-11-02)

SUPERSEDED 10-30: the "COLD-READ GATE (NOT optional, enforced by hooks)" block that stood here. Ryan, 10-30: "Get rid of
this thing that stops you from doing it because it's just wasting my time." The judge stays as a tool. (dreaming 2026-11-02, sessions 10-30_6aaa8a1e, 10-26_601f85f7, 10-28_fe5dc0fa, 11-02_0af56953)

1. **The reader is never the writer.** Before NEW copy reaches Ryan, run `python3 tools/copygate/coldread.py judge <file>`
   (add `--from "MASTHEAD:"` or `--section "<heading>"` so builder notes above the copy are not read). It prints the
   brief: spawn ONE fresh Agent (general-purpose, sonnet) with `tools/copygate/READER-PROMPT.md`; it runs `coldread.py
   text`, reads once as a stranger, and writes `coldread.py stamp <file> --reader subagent --json @<verdict>`. You never
   write a stamp for your own copy. Say once per session in the reply: the headless stranger is logged out and
   `claude login` in a terminal restores it. Never run `claude login` yourself.
2. **One read, one fix pass, at most one re-read.** Then ship with the remaining flags listed as notes at the top of the
   deliverable. Never a third read: every fresh reader finds a different line.
3. **Never run it on** unchanged copy, a CSS or image swap, a team brief, ClickUp task text, locked hooks or held-reveal
   headlines. Those fail every reader by design. A flag on a line Ryan locked is his call, not a fix.
4. **Their words, not ours.** Every mechanism word comes from `offers/<slug>/LANGUAGE.md` `## Their words`; a word you
   invent goes on `## Never`, not on the page.
5. **The judge is a tool, never a gate.** Nothing waits on a stamp: deploys, Doc pushes, handoffs and ClickUp go when he
   says go. ~~Nothing ships unstamped~~ (removed 10-30; `hook_pre_ship.py` exits 0).
6. **The mechanical floor runs itself** after every Write/Edit to `offers/<slug>/{ads,advertorials,landers,videos}/`.
   Fix dashes, banned words and long sentences before the judge, not after.

Tool and rules: `tools/copygate/README.md`.
