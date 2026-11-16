# Suno formatting: tags, style field, limits, delivery format

Current as of Suno v5+ (July 2026). If a render sounds wrong, check the mistakes list at the bottom before rewriting lyrics.

## The two fields

**Style field** (Custom Mode): genre, tempo, instrumentation, vocal quality, mood, production texture. 2-7 short descriptors; beyond ~7 they compete and the mix goes muddy. Example: "Emotional country pop ballad, mid tempo, warm mature female vocal, conversational verses, soaring heartfelt chorus, acoustic guitar, light strings, modern radio production".

**Exclude field** (Advanced Options): what you do NOT want. Negative instructions inside the Style field ("no drums") are unreliable; the Exclude field is the reliable path. Typical for song ads: "autotune, EDM, rap" (unless rap is the pick).

**Lyrics field**: the tagged lyric. Meta tags in square brackets on their OWN line are arrangement directives and are not sung.

## Tags that work

Structure: `[Intro]` `[Verse 1]` `[Verse 2]` `[Pre-Chorus]` `[Chorus]` `[Hook]` `[Bridge]` `[Outro]` `[End]`

- Number the verses: numbering signals "different melody each verse."
- Repeat the chorus with IDENTICAL text each time: identical text signals "same big melody."
- Always close with `[End]` or Suno may trail on.

Delivery: `[Female Vocal]` `[Male Vocal]` `[Spoken Word]` `[Whisper]` `[Harmony]` `[Backing Vocals]` `[Ad-lib]`

Parameterized tags give per-section control and are the best dynamics tool:
`[Verse 1: conversational, acoustic guitar only]`
`[Chorus: full band, soaring vocals]`
`[Outro: spoken, music fading]`
Keep modifiers to 2-3 per tag.

Parenthetical vocal cues on their own line or inline, 1-3 words max: `(softly)` `(building)` `(spoken)` `(belted)`. Full sentences in parentheses confuse the model.

## Formatting rules

- Tag on its own line, lyric lines below it. `[Chorus] lyric here` on one line fails.
- Single line break between lines in a section; blank line between sections.
- 4-8 words per line, one breath per line.
- 200-300 words total for a 3-4 minute song. Hard ceiling 5,000 characters, but rushing and clipped sections show up past ~3,000; stay well under.
- Physically repeat the chorus text every time it appears. `(x2)` notation is unreliable.
- No emojis, no stage-direction prose ("she opens her purse"), no unrecognized novelty tags.

## Delivery format (every song-ad package uses this exact shape)

```
## Style prompt
<paste-ready style field>
Alternate: <one different genre direction, one line>

## Exclude
<paste-ready exclude field>

## Lyrics
<paste-ready tagged lyric block>

## What changed
- <original ad line> → <lyric line>: <one-line reason>
- (one bullet per deviation; verbatim lines are not listed)

## Cut beats
- <beats dropped for length, so Ryan can demand any back>
```

## Common mistakes

1. No meta tags at all: Suno guesses structure and guesses wrong.
2. Chorus text varying between repeats: kills the melodic repetition.
3. Style field over 7 descriptors: muddy output.
4. "No X" in Style instead of the Exclude field.
5. Missing `[End]`.
6. Long parentheticals and stage directions sung out loud by accident.
7. Cramming the whole ad in: past ~300 words the vocal rushes and sections get clipped.

## Spoken-front story songs (added 2026-09-28)

A render came back fully spoken when the style field said "spoken word verses" and about half the lyric was tagged spoken. Rules:
- Never put spoken, narration, conversational or talking in the STYLE field. The style field applies to the whole track and overrides section tags. Say "sung female vocals" there instead.
- Put the spoken instruction only in section tags: a bare `[Spoken Word]` block per spoken section on the front, `[Outro: spoken word, music fading]` at the end.
- Keep the spoken share near a quarter and never past a third. If the story needs a long spoken front, start singing one beat earlier rather than adding spoken tags.
- Mark the first sung section explicitly (`[Verse 1: sung, soft melody]` plus a `(sung)` cue on its own line) and declare `[Female Vocal]` at the top.
- Sung lines 4 to 8 words; long prose lines get read, short lines get sung.
