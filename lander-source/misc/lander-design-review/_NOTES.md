# Notes — Lander design review (Organ Top 5, finished export)

**What it is:** the FINISHED, deploy-shaped version of the Organ Supplement Brands Top 5 lander — the completed counterpart of the draft in `organ-top5/from-zip/`. H1: "These Top 5 Organ Supplement Brands are Making Men Over 40 Feel Like They Did in Their 20s" (title tag matches). Same Lora/Lato editorial styling as the draft.

**Page style:** top-5 listicle advertorial for men 40+ (brand roundup with a #1 pick), fully self-contained: the draft's hotlinked competitor CDN images and `{{ ctaUrl }}` / `{{ reviewerName }}` template vars are resolved here into local `imageN.jpg` files and live CTA links.

**CTA / tracking:**
- 9 CTA links, all → `https://trk.skatrk02.com/click` (bare click URL, no params — same click domain as ProtaFlo and LANDING 1).
- Microsoft Clarity bootstrap present but with the literal placeholder project id `"CLARITY_PROJECT_ID"` — not functional as-is; needs a real id before deploy.
- No fbq/gtag pixel.

**Deploy conventions:** `cloudflare-export/` flat folder, `advertorial.html` + generic sequential `imageN.jpg`, everything pre-compressed under ~110 KB — the house Cloudflare Pages drag-and-drop shape.

**Draft → final delta worth knowing:** draft (32 KB dc.html + dc-runtime support.js + React) vs final (self-contained static advertorial.html, no support.js, no template vars).
