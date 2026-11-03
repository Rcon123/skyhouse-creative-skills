# Notes — Organ Top 5 (Claude Design draft)

**What it is:** the working DRAFT of the "Top 5 Organ Supplements" listicle lander — men-40+ organ/beef-organ supplement brand roundup. H1: "Top 5 Organ Supplements ...". This is the draft-stage counterpart of the finished export found in `misc/lander-design-review/` (same lander, same Lora/Lato typography).

**Page style:** top-5 listicle / roundup advertorial. Editorial serif look (Lora headings, Lato body).

**Format:** `.dc.html` is a Claude Design draft file, not a deployable page:
- Template variables still unfilled: `{{ ctaUrl }}` (all CTA hrefs) and `{{ reviewerName }}`.
- `support.js` is a generated dc-runtime bundle (header says "GENERATED from dc-runtime/src/*.ts", expects `window.React`) — design-tool runtime, not shipped tracking.
- Product images are hotlinked from competitor CDNs (shop.heartandsoil.co, vitalproteins.com, try-forge.com, website-files.com) plus local `images/hero-rancher.png` — would need re-hosting before any deploy.

**Tracking:** none. No trk./redtrack/clarity hits. CTA is the `{{ ctaUrl }}` placeholder (in the shipped version this becomes `https://trk.skatrk02.com/click`).

**Other contents:** `screenshots/` are small design-review crops of the page; `uploads/` (skipped, oversized) held the raw hero art and reference screenshots; the skipped PDF is a source doc upload.
