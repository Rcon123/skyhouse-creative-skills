# Notes — ProtaFlo prostate advertorial (deploy bundle)

**What it is:** the ProtaFlo prostate offer's pre-VSL advertorial, complete and deploy-ready.
Title/H1: "Board-Certified Surgeon Who Treated NBA Players: The Hidden 'Fungal' Colony Swelling Men's Prostates", masthead styled as "Men's Health Journal".

**Page style:** fake-editorial advertorial (authority-figure story, Oswald + Source Serif 4 typography), selling the click into the VSL — consistent with the VSL-funnel rule: no product name/bottle/price on the page, CTA is "Watch The Full Presentation".

**CTA / tracking:**
- All 3 CTAs → `https://trk.skatrk02.com/click` (bare click URL, no query params — RedTrack-style click domain; campaign resolution happens server-side).
- No Microsoft Clarity, no fbq/gtag pixel in the HTML.

**Deploy conventions:**
- Flat Cloudflare Pages bundle: one `a.html` (page name = `a`, so path is `/a.html`) + `assets/` webp images.
- `_headers` sets Cache-Control: `assets/*` immutable 1 year (versioning via filename), `*.html` max-age 300 must-revalidate ("copy changes go live within ~5 min").
- All images pre-converted to webp, largest 96 KB — deliberately light page.
