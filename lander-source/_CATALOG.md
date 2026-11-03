# Lander Source Catalog

Extracted 2026-08-05 from Ryan's Claude Design account + local Downloads deploy zips. This folder is the raw material for the lander design systems, the `strategist-lander` builder, and the QA skill (plan: `../LANDERS.md`). Per-folder `_MANIFEST.md` / `_NOTES.md` files have detail.

## Claude Design account map (fetch anything on demand via the DesignSync tool, main session only — subagents cannot reach it)

| Project | projectId | Contents |
|---|---|---|
| TPS Top 5 | 4e8e3d5a-20cf-4d28-86c3-7c1824578e80 | THE workhorse. ~33 lander HTML files across 4 offers (TPS=Total Package Serum skincare, Protaflo prostate, ancestral organs, prostate flush), all transcripts, all deploy bundles |
| Page replication request | 7ee7ece8-8eea-45cf-a859-029432b998f5 | MOFO advertorial + comparison pages, replicated from the Menerals comparison page (source saved here) |
| MOFO | db4d0a15-c68f-4434-8a59-75b96cadc796 | 10-reasons-mofo listicle with a fully organized numbered image set (img-01..22, reason-01..09, webp/svg) |
| Organ Supplement Brands Top Five | 66ce85ae-549a-42c7-98cf-c839b57bc9f6 | Men's Health Journal-style Top 5 listicle (.dc.html with {{ ctaUrl }} template vars) |
| ProtaFlo | 10bf2f10-7b83-49e0-bf13-48f6516cf72b | chat only, no files |
| Untitled | 657bd12d-5072-4078-9b18-e3a6d59bac81 | chat only, no files |
| TPS Top 5 Healthline | 38493b8f-d49e-4a14-8cd7-28f8f155ab31 | chat only, no files (Healthline lander lives in the TPS project) |
| Madi | 28dfc4ba-068d-4207-bb99-881140813af2 | logo design project (HiH mark), not a lander |
| Spiritual Gift Course Design System | 0425b968-8172-4289-9f0f-9632219e0a46 | Anima design system — structural template for per-brand systems |

Still in Claude Design, NOT yet local (fetch when needed): 10/8 Reasons Ancestral Organs, Ancestors Advertorial, Top 5 Prostate Advertorial, Prostate Advertorial - Top 5 Toxins, Prostate Advertorial VSL (base) + 3 Mistakes v3, and the 8 Top 5 Skincare variants (Health Magazine / Feminine / Age Quiz / Plain Article / Problem Quiz / Video Hero v2 / Longform / Advertorial v2).

## What's local

- `tps-top5/` — feedback_transcript.txt (June 16 Brandon Ham lander-review call), cf_transcript_4.txt (May 27 Fernando call = the Claude Design lander process), Protaflo + skincare VSL scripts, TPS Top 5 v4 Plain (canonical), Prostate Advertorial v4 (editorial VSL-bridge with image-slot placeholder tags), Protaflo Advertorial Longform (live RedTrack links), 3 zip finals, _DEPLOY-HISTORY.md (23 deploy zips May 20 → Jul 21)
- `page-replication/` — MOFO Advertorial.dc.html, MOFO Comparison.dc.html (+ mobile preview wrapper), advertorial.html (Cloudflare version), source21-menerals-comparison.html (the competitor page that was cloned), upload-primal-viking-homepage.html (truncated at 256KB)
- `mofo/` — 10-reasons-mofo.html, from-zip-manboobs/ (36 AI renders for the man-boobs angle, 2 treatments: handheld-phone-photo real + flat 2D illustration)
- `organ-top5/` — from-zip/ draft (.dc.html + support.js)
- `protaflo/` — from-zip/ deploy-ready advertorial + webp assets + Cloudflare `_headers`
- `misc/landing1/` — MOFO first-person testimonial advertorial (bottle on page, 8 CTAs, IMAGE-MANIFEST.txt)
- `misc/lander-design-review/` — finished Organ Top 5 cloudflare-export (19 compressed jpgs, 9 CTAs)

## The house lander system (distilled from transcripts + shipped HTML)

**Ryan's 3 golden rules (told to Claude Design at the start of every template, from the May 27 Fernando call):**
1. Mobile-optimized. "95% of my people on this are gonna be mobile on paid traffic."
2. Page speed and quality maxed out: compressed images (PNG → JPG under ~110KB), lazy loading below the fold, preconnect/preload. "If you don't tell it that, your landing page CTR drops like crazy."
3. Proper tracking links: RedTrack.

Plus from the call notes: bold the really important points for scanners ("use bold for the scanners, only important phrases, use italic when you're trying to whisper" — no random bolding), and connect Microsoft Clarity for heatmaps.

**Deployment conventions (consistent across every shipped lander):**
- CTA link: `https://trk.skatrk02.com/click`, bare, no query params, campaign resolved in RedTrack
- Bundle: one flat Cloudflare Pages folder, one `advertorial.html`, sequential `image1.jpg...imageN.jpg` pre-compressed
- Cloudflare Pages URL pattern: folder name + html name are the path; two-step: page → RedTrack → offer
- Clarity bootstrap present but unarmed (empty project ID) — an armed Clarity ID is an open item
- `_headers` cache policy (assets immutable 1yr, HTML 5-min) seen once (ProtaFlo) — worth standardizing

**Format library observed:** fake-publication advertorial (Men's Health Journal / Men's Health Bulletin / Primal Journal / American Beauty Journal masthead), Top 5 listicle with hold-the-reveal #1, 10-reasons listicle (modern: countdown, sticky CTA, FAQ accordions, scroll-reveal), editorial VSL-bridge (cards + Watch CTA, image slots described as placeholder tags for renders), comparison page (cloned from Menerals), first-person testimonial advertorial, Healthline-style clean medical.

**Testing doctrine (Ryan, May 27):** test format first, then headline/lead/image. New iterations change only headline + intro on a proven template. Even splits (e.g. 4-way 25/25/25/25).

**Preference signals from the June 16 Brandon call (graded onto the organ listicle):** lead with claims and bury the ingredient ("save the organs for the back end"); benefit order age → fat loss → TRT-alternative → energy → libido last; always test an on-the-nose version and a blind claim-heavy version; big-claim headline with renamed product ("Ancient T-booster" not "capsule full of organs"); disqualify-the-alternative leads crush; QA an advertorial by bullet-pointing its logic chain.

## 2026-09-01 — TPS story lander (top5-story-insider): readability grade
Ryan graded our story variant against the RJV control: too chunky, too few bolds/highlights. Fix that shipped: split paragraphs to 1-2 sentence beats and rotate bold / italic / underline / yellow-highlight treatments (highlights limited to 2-3 payoff lines). The plain skin strips `.hl` to bold, so story variants define `.mark` after the override block to get RJV-style yellow. Model: offers/tps/landers/top5-story-insider/advertorial.html.

**Cache-busting rule (2026-09-01, Akka LF build):** assets ship immutable/1yr, so same-filename image swaps on a live page MUST bump `?v=N` in the HTML references, or prior visitors keep the old images forever.
