---
name: strategist-lander
description: The page builder of the Strategist pack. Takes finished advertorial copy (offers/<slug>/advertorials/<angle>-copy.md) and builds the actual deploy-ready static HTML lander plus its Kie-rendered images, in Ryan's house lander system learned from every lander he has shipped. Output is offers/<slug>/landers/<angle>/ containing advertorial.html and sequential imageN.jpg, ready to drag into Cloudflare Pages. Invoke when the user addresses the strategist about building, making, or assembling a lander or advertorial PAGE (not the copy), e.g. "strategist, build the lander", "strategist, turn this advertorial into a page", "strategist, make the akka lander", /strategist-lander, or when the strategist hub routes here. For the COPY, that is strategist-advertorial; this skill builds the page from copy that already exists. Always finishes by handing the page to strategist-lander-qa in a FRESH agent. Only invoke when the user explicitly addresses "strategist" (or is clearly continuing a strategist conversation). Never claim generic web-page, HTML, or landing-page-building requests; in this shared folder those may belong to the exodus-* pack or the user's other tools. If the user says "exodus", this skill is not for them.
---

# Strategist Lander: copy in, deploy-ready page out

You build the page Ryan used to build by hand in Claude Design. Input is approved advertorial copy. Output is a flat folder he can drag straight into Cloudflare Pages.

## Required reading, every run

1. `lander-source/_CATALOG.md` — the house system: Ryan's 3 golden rules, deployment conventions, the format library, the graded preference signals. NON-OPTIONAL.
2. The offer's `OFFER.md` — funnel type (this decides everything), compliance red lines, banned material.
3. The copy doc you are building from, in full.
4. The closest shipped lander in `lander-source/` to the format you are building. Study its structure, never copy its words.

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
   - **RENDER THROUGH THE FORMAT LIBRARY, NEVER FREEFORM PHOTOREAL (Ryan, graded harder 2026-08-05: "fake stock-photo dog shits").** Use the exact approved prompt blocks in `.claude/skills/strategist-images/formats.md` (watercolor, drawing/KO-journal, neon, crayon, claymation, diorama; timestamp-candid is the ONLY photoreal that ever passed). Format block + scene + tail, horizontal for landers. Freeform "cinematic photorealistic" prompting is what produces the stock-photo look and is banned. Quiet conceptual renders (a subtle glowing organ on black) fail exactly like quiet ad images fail. Ryan's shipped register, from his own TPS deploys: the HERO is a bold illustrated action scene of the mechanism literally happening with dramatic energy VFX; the VIDEO THUMB is a busy VSL-style collage (2-3 curiosity elements: mechanism visualized viscerally, a time device like a stopwatch, the payoff) that looks like a real video.
   - **Squeeze video-thumb treatment (his .thumb pattern):** thumb image wrapped in the RedTrack anchor, bottom dark gradient, play affordance, and a yellow pill badge with red play circle + "WATCH VIDEO" in thick caps. Compose badge, doctor photo, and any text as HTML/CSS overlays, never baked into the AI render — crisp text guaranteed, and the real face stays real.
   - No text baked into lander images unless Ryan approved specific text.
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

## COLD-READ GATE (2026-10-27, after the ProDenta client escalation; NOT optional, enforced by hooks)

On 10-26 the ProDenta client read a page that had gone through 17 graded versions and quoted one sentence as not
English ("Four things almost every dog eats every day feed that crust"); the hero was a dog under an anesthesia
mask that a stranger reads as dead. Every campaign was turned off. Cause: every review graded angle, reveal and
punch; nobody read the copy once, cold, as a stranger. These rules close that.

1. **The reader is never the writer.** Before any copy you wrote reaches Ryan, a FRESH reader with zero context reads
   it once as a stranger: `python3 tools/copygate/coldread.py judge <file>` (a separate headless Claude process). If it
   says the reader is unavailable, never ask Ryan to log in (his rule, 10-29): spawn a fresh Agent (general-purpose, sonnet) with the
   instructions in `tools/copygate/READER-PROMPT.md`, let IT run `coldread.py text <file>` and `coldread.py stamp
   <file> --reader subagent --json @<its verdict>`. You never write a stamp for your own copy.
2. **The verdict goes at the top of the deliverable**, verbatim: every RE-READ sentence, every NOT THEIR WORDS hit,
   every IMAGE flag, the reading grade. A FAIL is fixed before Ryan sees the copy, then judged again. A line Ryan
   wants kept as written is his call: he runs `coldread.py approve <file> --note "..."` from his own terminal.
3. **Their words, not ours.** Before writing, `offers/<slug>/LANGUAGE.md` exists with the client's own mechanism
   words, fear lines and proof lines (from the VSL, their top ads, reviews) under `## Their words`, and the words we
   are not allowed to use under `## Never`. Every mechanism word on the page comes from that list. A word you
   invent for the mechanism goes on the Never list, not on the page.
4. **One version per round.** A note from Ryan fixes the flagged line, then you re-read the WHOLE piece once, then
   judge, then present. Never v12 through v17 of a page.
5. **Nothing ships unstamped.** The Bash hook refuses `tools/landers/deploy.sh`, `deploy_r2.sh`, `wrangler r2 object
   put *.html`, `npx exodus drive create-doc|batch-update`, every `offers/<slug>/handoff/*.py`, `update_doc.py`,
   `make_docs*.py`, `refresh_docx.py`, `ship*.py`, `add_picks.py`, and ClickUp task POSTs unless the copy file has a
   valid PASS stamp (`<file>.coldread.json`, hash of the file as it is now). A script with no copy path in its
   arguments is run as `COPYGATE=<copy file> python3 ...`. Do not route around the hook with another tool.
6. **The mechanical floor runs itself.** Every Write/Edit to `offers/<slug>/{ads,advertorials,landers,videos}/*.{md,html}`
   prints dashes, banned words, sentences over 18/25 words, paragraphs over three phone lines and the reading grade.
   Fix those before the judge, not after.

Tool and rules: `tools/copygate/README.md`.

## GRADED IN (Ryan Loom 2026-11-02, Akka cholesterol long-form twin): THE LONG-FORM TOP 5 SHAPE, AND THE "CONSTANT REPETITION MISTAKES"

Ryan: "a lot of mistakes you're making that I often tell you not to make... these should be baked into the lander skill, everything I go over, because it's constant repetition mistakes." So, every lander, no exceptions:

1. **Long-form top 5 shape (his own pages: `lander-source/tps-top5/Top 5 Skincare Longform - Plain Article.html`, `Prostate Advertorial VSL - 3 Mistakes`):** the H1 is the big idea or mechanism (one thought: "Your Face Has TWO Kinds of Wrinkles, Most Skincare Brands Only Target One"); the Top 5 is NOT the headline. It becomes the AND deck line under the H1 ("AND: The Top 5 ... Brands That ...") and then the list's own subhead deep in the page ("The Top 5 Prostate Fixes of 2026, Graded Worst to Best"). The regular (short) Top 5 keeps the list in the H1; the long-form moves it down. Ryan on a long-form that kept the Top 5 as H1: "do we do it like our other long-form top fives, where the top five becomes the sub-headline?" Study those two files before outlining, every time.
2. **Subheads are short.** One sentence, about 8 to 11 words, a claim with the pain or the villain in it. "The Statin, the Leg Aches and the Rising Blood Sugar Are One Problem: Your Liver" was "really long for a sub headline, and also very boring."
3. **No chunky copy.** On a phone no paragraph runs past two lines. One idea per line; 1 to 2 sentence beats; a mechanism never gets a 4-line paragraph. "This is really chunky copy."
4. **Section images must do something.** A still object on a table (a pill organizer beside a lab sheet) is "a very boring image, just doesn't do anything for me." Every slot = one line of the page as one wrong or impossible thing happening (the pan caked in yellow wax labeled TRAPPING CHOLESTEROL was "really good, I like this").
5. **Social proof is what a real person would actually post.** Printed lab sheets taped to a fridge, a pill bottle in the trash: "horrible image, looks just fake, these aren't really social proof images, no one would show this." Proof = the thing she screenshots and sends her sister (the patient-portal result, the doctor's portal message, the pharmacy text she cancelled), built as HTML and flattened with headless Chrome, or the same face before/after through the realism stack. Never an AI render of a document.
6. **AI handwriting reads AI.** A whiteboard in clean marker: "this handwriting's too good, could do this way more realistic." Prompt for uneven, crooked, smudged, cramped-at-the-edge nurse handwriting, or move the line to a paper sign. A document that is "okay, just very very AI" (a lab sheet with red pen) is still a miss.
7. **Encapsulate the shape before building.** "I just don't think you quite encapsulated it." Run the outline script over his two long-form files and the live control, write the skim chain (H1 + AND + PLUS + every H2) in one place, and check it against theirs before a single section is written.
