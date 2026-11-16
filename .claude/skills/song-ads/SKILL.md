---
name: song-ads
description: Convert a finished ad into a Suno-ready song ad with the fewest possible changes to the original copy. Invoke whenever Ryan says "song ad", "suno", "jingle", "sing this ad", "make this a song", "turn this ad into a song", or pastes ad copy and asks for a musical or sung version in any phrasing. Also invoke for tweaks to an existing song ad ("make the chorus hit harder", "different genre", "shorten the second verse"). This skill claims ALL song/music-ad requests in this workspace. It does not write ads from scratch; it adapts finished ad copy Ryan supplies (if no ad is given, ask for one or point to strategist-ads first).
---

# Song Ads: finished ad copy → Suno-ready song, minimal edits

## The job

Ryan hands you a finished ad. You hand back a paste-ready Suno package (style prompt + tagged lyrics) where the ad is sung, sounds genuinely good, and stays as close to the original copy as humanly possible.

The doctrine, learned across a full grading session (see Graded-in lessons in songcraft.md):

1. **The ad's own sentences ARE the lyric, and the ad's structure IS the song's structure.** Work through the ad top to bottom, splitting its sentences into singable one-breath lines. No beat may appear earlier in the song than the ad reveals it; the ad's reveal order is engineered and the song must not leak the solution, mechanism, or payoff ahead of its slot. Do not compose new lines. Every lyric line must be traceable to a specific ad sentence; a line Ryan cannot find in his ad reads as fabrication and kills trust, even if it restates a real claim.
2. **The hook is untouchable.** Verse 1 is the ad's opening hook, as close to verbatim as physically possible, moving FAST. Never pad it with dialogue, setup, or rhyme-service lines. Grab speed beats rhyme in the hook; the rhymes can start in verse 2.
3. **Rhyme is harvested, never imported.** Take rhymes the ad's own words hand you (line/time, York/work), use tiny connective adds of a word or two on Ryan's own sentence when they land one, and accept an unrhymed passage over an invented line every single time. Spoken delivery covers the passages that will not rhyme.
4. **An edit must earn its place by making the line sing better.** A lateral reword (same meaning, no musical gain) is the worst available move; it loses fidelity and buys nothing. Verbatim or genuinely better, never in between.

## Required reading, every time

1. `references/songcraft.md` in this skill folder: the minimal-edit hierarchy, rhyme and prosody rules, section mapping, compression rules. This is where the "master songwriter" lives. Not optional.
2. `references/suno-formatting.md`: current Suno tags, style-field rules, limits, and the exact delivery format.

## Process

1. **Read the ad and mark the beats.** Hook scene, problem/emotion, failed solutions, trusted-source discovery, skepticism, mechanism, transformation timeline, social payoff, CTA. These map to song sections (mapping table in songcraft.md).
2. **Pick the genre from the avatar, not from taste.** The narrator of the ad is the singer. A 55-year-old woman telling a wedding story is a country-pop storytelling ballad with a warm female vocal, not a synth track. Default is decided for Ryan with one alternate offered; never block on this question.
3. **Build the chorus first.** Distill the ad's core transformation or mechanism hook into 2-4 lines using the ad's own words. The chorus is the one place light rewriting is allowed, because it repeats 3x and carries the song. First line of the chorus gets the most melodic weight, so the money phrase goes there.
4. **Convert the verses using the minimal-edit hierarchy** (songcraft.md). Spoken-word and conversational delivery are your best friends: they let original ad lines survive verbatim, unrhymed.
5. **Compress by cutting whole beats, never by paraphrasing beats.** A song holds 200-300 words; most ads run longer. A beat kept verbatim plus a beat cut cleanly is more faithful than two beats reworded.
6. **Format for Suno** per suno-formatting.md and deliver in the exact package format there: style prompt, exclude field, paste-ready lyrics, then a change log listing every deviation from the original ad and why. The change log is how Ryan vetoes edits fast.
7. **Iterate surgically.** Ryan grades in chat. Touch only the flagged lines; do not re-roll the whole lyric because one line got flagged.

## Voice rules (inherited, non-negotiable)

- **No em dashes. Anywhere.** Lyrics, style prompts, change logs, chat.
- Simple direct language. One thought per line. If a lyric line needs decoding, it fails.
- The story logic must hold when sung: the cure arrives via a credible source, skepticism stays in, claims stay believable. Cutting the skepticism beat to save words is a red flag; it is load-bearing.
- Strip emojis. They do not sing.
- Compliance red lines from the source ad carry over verbatim; never let a rhyme push a claim past what the ad said.

## Self-improvement

When Ryan grades a song ad and a lesson generalizes (a rhyme move that flopped, a genre call he corrected, a beat he never wants cut), append it to `references/songcraft.md` under "Graded-in lessons" in the same session. This skill gets sharper every time it runs.
