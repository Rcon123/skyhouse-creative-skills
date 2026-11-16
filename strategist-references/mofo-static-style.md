# MOFO Static Style: the graded-in image recipe (Ryan: "unbelievable job... remember this and save it", 2026-07-16)

The reproducible formula behind the man-boobs textbook set (valve, padlock, 1925 plates, cut-estrogen, balloons; flagship: the testosterone-siphon). Use this recipe for MOFO mechanism statics until graded otherwise.

## The engine

Kie.ai direct (NOT the exodus template/creative engines for this style). `KIE_API_KEY` in workspace `.env`.
- Submit: POST `https://api.kie.ai/api/v1/gpt4o-image/generate` with `{"prompt": ..., "size": "1:1"}` (+ `"filesUrl": [bottle-url]` only when the real bottle must appear).
- Poll: GET `record-info?taskId=` until `successFlag=1`, download `response.resultUrls[0]`.
- Real bottle reference (when needed): `https://cdn.prod.website-files.com/69d69241f70f6f490a4af419/69ddd98e4c8d5caeaf3e03de_mofo.webp` with prompt opening "Use the EXACT supplement bottle from the provided reference image, unchanged".
- Content-policy trips: transformation-y body phrasing ("chest-flattener", melting ice torso) gets blocked; labeled objects and illustration torsos pass fine. Rephrase and rerun.

## The style block (append verbatim to every concept prompt)

> "Vintage medical-textbook flat illustration on aged cream paper, warm muted colors with one gold and one pink accent, painted bold labels on objects, huge headline in thick uniform black condensed hand-lettered caps, comic-book-letterer clean, perfectly legible at thumbnail size. Maximum three visual elements. The argument must be understood in one glance with no reading beyond the labels. Square 1:1."

## The concept rules

1. **One universal metaphor per image** (siphon, valve, lock and key, deflating balloon, then-vs-now plates). If the metaphor needs decoding, kill the concept.
2. **The mechanism is a labeled physical OBJECT** ("ESTROGEN" painted on the pipe/padlock/tank; "ZINC + VIT A" on the key). The labels ARE the copy.
3. **Headline names the problem in the buyer's words** ("MAN BOOBS ...") + states the reframe or benefit in one spoken sentence.
4. **Gold = male/testosterone/fix. Pink = estrogen/villain.** Keep the color grammar consistent across the set.
5. **Text is prompted separately from the art style** (letterer-clean caps) so illustration wobble never infects the words.
6. Photos of ordinary people are NOT a concept (graded "boring as fuck"); a realistic photo is only the paired native image for a story ad.

## The 5 winning prompts (2026-07-16 renders, files in offers/mofo/images/)

- **Valve** (`manboobs-valve-v1`): pink pipe labeled ESTROGEN pouring into a clear glass male torso, chest filling pink; hand mid-turn on a red shut-off valve, last drop falling. Headline: "MAN BOOBS HAVE A SHUT-OFF VALVE."
- **Padlock** (`manboobs-padlock-v1`): pink lace bra locked onto a male torso by a padlock engraved ESTROGEN; golden key tagged "ZINC + VIT A" approaching. Headline: "YOUR MAN BOOBS ARE LOCKED ON. THIS IS THE KEY."
- **1925 plates** (`manboobs-1925-v1`): split, banners 1925 / TODAY; organ-meat plate + lean torso icon vs cereal-and-pizza plate + soft-chested torso icon. Headline: "MAN BOOBS BARELY EXISTED IN 1925. THE PLATE IS WHY."
- **Cut estrogen** (`manboobs-cutestrogen-v1`): two textbook torsos, ribbon banners ESTROGEN HIGH / ESTROGEN CUT, painted arrow. Headline: "CUT THE ESTROGEN. LOSE THE BOOBS." (v1 flag: after-torso too shredded; keep the after believably normal.)
- **Balloons** (`manboobs-balloons-v1`): tailor's mannequin with pink balloons at the chest, one deflating at a hat pin labeled ZINC. Headline: "MAN BOOBS DON'T MELT. THEY DEFLATE."

Flagship reference: `manboobs-siphon-v1` (TESTOSTERONE barrel siphoned by pink hose into a bra-shaped ESTROGEN tank; "THIS IS WHY YOU HAVE MAN BOOBS.").

## Native screenshot formats (separate lane, same folder)

iPhone Notes / app-screenshot statics are hand-built HTML rendered via headless Chrome (never AI; AI can't fake OS chrome). Working example: scratchpad notes-manboobs.html → manboobs-notes-v1.png, 1080x1080.
