# Notes — LANDING 1 (MOFO testimonial advertorial)

**What it is:** a MOFO advertorial, first-person testimonial style. H1 opens: "I Went from Exhausted and Soft to ..." (Archivo/Mulish typography). `<title>` is just "Ancestral Supplements" — an off-brand/leftover page title worth fixing before any redeploy. Product imagery per IMAGE-MANIFEST is MOFO: `bottle-mofo.png` (image20) plus a `bottle-generic.png` comparison bottle, `ic-*` benefit icons (morningwood, fat, energy, brain, blood, testo, bicep, body, rose), and ~17 uploaded testimonial/story photos.

**Page style:** long-form testimonial advertorial (story → benefits icon row → product reveal with bottle + comparison → proof photos). Not a listicle; the bottle appears on-page, so this is a direct product-page-style advertorial, not a VSL pre-frame.

**CTA / tracking:**
- 8 CTA links, all → `https://trk.skatrk02.com/click` (bare click URL, no params — same RedTrack-style click domain as the ProtaFlo and Organ Top 5 landers).
- Microsoft Clarity bootstrap is present but disabled: `CLARITY_ID=""` (empty placeholder guarded by an early-return). Would need a real project id to activate.
- No fbq/gtag pixel.

**Deploy conventions:** `cloudflare-export/` flat folder, `advertorial.html` + generic `imageN.*` names, with `IMAGE-MANIFEST.txt` as the rename map back to design sources — the same export shape as the TPS Top 5 bundles (`upload/advertorial.html` + `imageN.jpg`).
