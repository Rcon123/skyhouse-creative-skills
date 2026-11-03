# Craft rules

What separates an intentional AI video from a confusing one. Each rule has a reason so you can judge the edge cases. Sources: the 2026-10-05 bake-off and demo build in this workspace (TESTED), the people Ryan follows on X (`tools/video/research/x-notes.md`), and two research reads with links for every claim (`tools/video/research/lipsync-sota.md`, `tools/video/research/prompting-workflows.md`).

## 1. Why lip sync used to fail, and the one rule that fixes it

The mouth has to be generated from the exact audio the viewer will hear. Every bad-sync video breaks that rule somewhere: a silent clip with a moving mouth and a voiceover laid on top, a clip retimed to fit a voice, a clip's own voice swapped for another read.

So the voice is recorded first, once, for the whole script. Each talking shot is generated from its own slice of that recording. The recording is the only voice track in the final. Nothing is ever stretched, sped up or re-voiced after the picture exists. TESTED: nine clips across five engines all scored at real-footage level this way.

Corollaries:

- Never speed or slow a clip to fit audio. Trim or hold a frame instead.
- Never put speech words (talk, says, speaking, conversation) in a B-roll prompt. Mouths start flapping with no audio behind them.
- A person seen in B-roll while the voiceover runs has lips closed, and the prompt says so.
- Upscale after lip sync, never before, and recheck the mouth after.

## 2. The voice (decided before the picture, judged by Ryan's ear)

Graded 2026-10-05: a text-to-speech read with a style prompt is "horrible, super fake". The fix that tested out:

- **Let the video model speak.** The voices that pass as real are generated with the picture (native audio), not read by a TTS engine and laid on. Give the model a VOICE paragraph and the exact line. The pattern, from the prompts Ryan's X follows publish:
  - who she is and where: "A woman of 66 with a Midwestern American accent, recording a selfie video for her friends at home."
  - texture: "A lived-in, slightly husky mid-low voice with a little rasp on the low notes."
  - delivery: "Chatty and continuous, half laughing, with audible breath, uneven pauses and slightly swallowed word endings."
  - mic and room: "Close to the phone mic, with the natural sound of a real house around her."
  - the line that matters most: "She sounds like a person talking, not a person reading. One take."
  - then `SPOKEN DIALOGUE, EXACTLY: "..."`.
- **Cast once, lock it.** One clip becomes the voice anchor; its audio goes in as the voice reference for every other line. Measured: 0.81 speaker similarity on a new line, against 0.09 to 0.48 for unrelated voices. A picked anchor is reused for that character across videos.
- **Seat it in the room.** A generated voice is too clean. `voice_fx.py` adds a small room, a phone's band limit and a noise floor without touching timing. It moved a native voice from 2 to 9 and 10 with the listening judge.
- **Match the winners, by the numbers.** Measured on Ryan's own winning yappers (`voice_profile.py`): 160 to 195 words a minute, under 16% of the time in pauses, pauses around 0.2 s, women's pitch 180 to 220 Hz moving about 10 semitones, the gaps between words only 21 to 32 dB under the speech, most energy under 3 kHz. The voice he rejected: 152 Hz, a third of its length in silence, pauses of half a second, gaps 60 dB down. Never direct a voice to slow down or leave silences.
- **The voice gate (ProDenta client, 2026-10-28: "sounded really bad").** The client's winners measured 15 to 21 semitones of pitch movement, 7 to 15% pauses, low end -17 to -22 dB, and a noise floor CLEANER than ours. Our three builds: 8 to 9 semitones, 21 to 25% pauses, low end -34 dB. Monotone, pausey and thin is what "sounds AI". Before any voice ships, run `voice_profile.py` on the track beside the reference: pause share under 16%, pitch spread over 12 semitones, low end within 6 dB of the reference. A voice that fails is recast or redirected ("pitch moving a lot, excited to share, no pauses"), never fixed by seating it in a room (that adds noise, not life).
- **Words are checked, not trusted.** A native model can change or drop a word. Every clip is transcribed and compared with the script; under 90% is rerolled.
- Spell numbers, years, prices and acronyms as words in `text`; `captions.replace` sets how they display.
- **Delivery marks only.** Ellipses, commas and tags may be added to steer a read. Fillers and restarts ("um", "I mean") sound human and change graded words, so they need Ryan's say-so each time.
- If Ryan supplies a recorded read (his own or anyone's with permission), that is the best voice source there is: real timing, real breath. It drives the picture in TTS mode as `voice/master.wav`.

Corollaries that hold in either mode: never speed or slow a clip to fit audio, never put speech words in a B-roll prompt, a person seen in B-roll has lips closed.

## 3. Start frames (cheap, so decide everything here)

A frame costs 5 cents and a few seconds. A bad clip costs a dollar and minutes. Every decision about look, wardrobe, room and framing is made on stills.

**The master.** One portrait per character, generated once, never regenerated mid-project. Every other frame of that person is an edit of the master, so the face holds. TESTED: one master held through a kitchen, a table, and two bathroom mirror selfies at different body weights.

**Talking frames must have:**

- face frontal or a slight angle (under 30 degrees), head and shoulders, face in the upper half of the frame
- lips closed, relaxed, a hint of expression (visible teeth in the still cause teeth flicker)
- nothing over the mouth or chin: no hands, mugs, mics, hair, bottles
- even light on the face, no backlight
- props already in the hands if the beat uses them (the model moves a bottle it can see far better than it invents one)

**Edit prompts** (the pattern that held identity):

```
Image 1 is the reference. The same woman from Image 1, same clothes and hair.
Keep her facial features exactly the same as Image 1.
Change only [the one thing]. [Where things sit.] Lips closed, looking into the lens.
```

Say what stays and what changes. One change per edit. Do not re-describe her face. For a photo pair (before and after), make the second by editing the first: "Recreate the exact same photo... Change only her body and expression."

**Realism for UGC-style frames.** Ask for a plain iPhone photo: deep focus, no background blur, flat natural indoor light, real skin with pores, lines and age spots, slightly imperfect framing, an ordinary lived-in room. Ban the words that summon the AI look: cinematic, 8K, studio lighting, bokeh, 85mm, flawless. Ryan's rule for statics applies here too: if it looks like it cost money, it dies.

**The AI look is the premise and the set, not the texture (ProDenta client, 2026-10-28: "looked AI").** Measured against the client's winners, sharpness and grain were identical; what differed was everything else. Rules:
- No premise, no costume. The presenter is an owner in her own clothes on her own couch. No white coats, no scrubs, no kids as doctors, no glass dogs or 3D tooth renders. Mechanism pictures are the client's kind: a thumb on real teeth, a clock, a gloved hand.
- The room is somebody's, not a set. Name the clutter in the prompt: the arm of a brown couch with a fleece throw, a lamp, a side table with a remote and a mug, a TV off to the side, a dog bed. Window light from one side, slightly under-exposed. Never the bright white designer kitchen.
- The dog is old when the script says old: grey muzzle, reddish tear stains, scruffy uneven fur, a little matted around the mouth. A groomed show dog with brown teeth is a toy.
- Muted colour: saturation 0.2 to 0.3 measured on the frame (theirs), never 0.4 (ours). Keep saturation down in the finish.
- Captions on a twin of a client ad take the client's shape: one short mixed-case line, medium weight, white on a soft dark pill, bottom third inside the safe zone; the hook card is a black bar in heavy caps with one yellow word. The teal top-band style stays for formats Ryan graded it on.
- Cut rate 24+ a minute in the first minute (theirs 22 to 33, our best 21).

**The style contract.** One paragraph of look language in `style_contract`, pasted onto every frame prompt word for word, so every frame pulls toward the same camera. For stylized formats it names the medium exactly ("3D animated feature film still, soft rounded stylized characters, subsurface skin, warm key light").

**No text in generated images.** Prices, headlines, article screens, labels that must read: add them in post or keep them unreadable. Generated lettering is gibberish often enough to burn a take.

**Real products.** Attach the real product photo as a ref on every frame that shows the product. Never let the model invent the pack. (Does not apply to product-blind funnels, where no product shows at all.)

## 4. Shot design (what makes it look intentional)

**Every shot shows the exact thing the words name.** If the line says salad, the salad is on screen while she says salad. This is the single biggest difference between an intentional ad and a random one. Write each cutaway by quoting the words it covers (`on`), then showing that noun.

**One idea per shot. One action per clip.** "She sets the bottle down" works. "She sets the bottle down, turns, and walks to the window" collapses. Give a start state and an end state when the action matters.

**Camera: say it every time.** "Locked-off camera, single continuous shot, no cuts" unless a move has a reason. An unstated camera drifts or starts editing on its own. If it moves, one named move: slow push-in, pan left, tilt up.

**Motion prompts describe only what changes.** With a start frame attached, do not describe the person again; that invites the face to drift. Under 80 words. Positive phrasing ("stable picture, lips closed"), because negatives get ignored or summon the thing.

**Kill frozen shots.** Something has to happen in a B-roll clip: a hand slides the plate, the screen lights up, steam rises. A camera drifting over a still scene reads as a slideshow.

**Hands do simple things.** Hold, set down, tap, slide, pick up. Put the object in the hand in the start frame.

**Keep the face for the lines that carry feeling.** Cut away on nouns and facts. Stay on her for the confession, the turn, the ask.

**Never reuse a shot.**

**Stills are shots too.** A photo the script points at (before and after, the class picture) is a `still` with a slow push-in toward the part she is talking about. Free, and more believable than animating it.

## 5. Seams (every talking shot restarts the head pose)

Two talking clips cut back to back on the same framing look like a glitch. Hide every seam one of three ways:

1. **Punch-in.** Same frame, alternate `zoom` 1.0 and 1.14. Reads as a deliberate jump cut, the native grammar of talking-head ads.
2. **Another framing or setting.** Counter, then table. Two or three settings per ad keeps it alive.
3. **A cutaway or B-roll beat over the join.**

`validate` warns when two neighbours share frame and zoom.

Beat length: 8 to 30 words. Short enough that one bad take is cheap to redo, long enough to score (the sync gate needs about two seconds).

## 6. Pacing for paid social

- The first frame has to work as a still and motion starts inside the first second. Open on the thing in her hands, not on a neutral face.
- A visual change every 2 to 4 seconds in the first 15 seconds (cutaway, punch-in, photo), then every 4 to 6.
- Before and after inside the first 12 seconds when the script has one (Ryan's yapper shape).
- Ryan's yappers run 60 to 90 seconds. Drama scenes run 2 to 3 minutes with many cuts.

## 7. Captions and sound

- Captions: 2 to 3 words a page, bold, white with a black outline, the spoken word highlighted, 84 to 96 px for buyers over 60, centered around y 1150. **THE META SAFE ZONE (Ryan, 2026-10-22, every video): all text, cards, stamps and CTAs inside the 950 x 979 box from y 269 to y 1248, x 65 to 1015 (14% top, 35% bottom, 6% sides), and clear of the bottom-right engagement rail (x > 940 when y > 1050). Feed crops to 4:5 and 1:1 from the centre, so the box survives every placement. `tools/video/safe_zone.py` holds the numbers and `validate` refuses captions or hook cards outside it.**
- The mix: voice on top, quiet room tone under everything so the cuts do not sound like cuts, optional music ducked under the voice, final at -14 LUFS.
- Sound is on for most Reels viewers and off for four in ten seniors. Build for both: the captions carry the whole script.

## 8. Formats and what changes for each

| Format | Picture plan | Notes |
|---|---|---|
| **Yapper** (one person to camera) | talking beats in 2 or 3 settings, cutaways on the nouns, stills for photos | The demo. Phone look, punch-ins, 60 to 90 s. |
| **Doctor or expert to camera** | same as yapper, prop in hand from frame one | Check claims against the offer's compliance lines before rendering. |
| **Drama scene** (two people, no narrator) | every line is a talking beat on a single of whoever speaks; reaction shots are silent B-roll of the listener, lips closed | Set `"talk_engine": "kling-avatar-pro"` (Wan misses on faces that look off camera). Build the room once as a wide scene image, then make each single as an edit of it so the kitchen and the eyelines match. Never two faces talking in one generated shot. Coverage in singles is how film does it and it removes the wrong-speaker problem. One establishing two-shot as B-roll. Ryan's drama rules: nobody talks to camera, premise in the first sentence, real props. |
| **Podcast or interview** | two singles with mics below the chin, a wide as B-roll. Kling Avatar Pro for the same reason as drama. | Masked or anonymous guests need no lip sync at all: one chair shot plus cutaways. |
| **Pixar-style or talking character** | same pipeline, stylized master frames | Tested: sync holds on stylized faces. Keep a human-like face with a clear mouth. Objects with faces (a liver, a bottle) are untested; expect the gate to return NO_FACE and judge those by eye. |
| **Storybook or narrated** (voice over pictures, nobody on camera) | every beat is B-roll or stills | No lip sync to get wrong. Cheapest format per second. |

What the people Ryan follows are saying (October 2026): drama ads built as entertainment first are the top spenders (frankyecom), Pixar-style animation is in a gold rush and nobody cares that it is AI (pounddz), and a cheap one-shot yapper is the right way to test a script before full production (Whiskeyatx).

## 9. What the pipeline will not fix

- A weak script. The tool renders the words it is given.
- A wrong face. If the master is not her, stop and redo the master; do not reroll clips built on it.
- Real people. Never generate a real person's face or voice, and never a doctor who exists.
- Brand logos. Generic props unless Ryan supplies the real asset and asks for it.
