#!/usr/bin/env python3
"""human_check.py <file> [--from TEXT]

Measures spoken copy against Ryan's Benny shape (.claude/skills/talk-like-a-human/SKILL.md):
one idea per paragraph, 12 to 35 words, sentences that run together with connectives,
no fragments stacked for punch, no paragraph over 40 words, no three short sentences in a row.

Prints one line per paragraph (words, sentences, connectives) and a FLAGS list. Never blocks.
Skips markdown headings, front matter, and lines that are only a label like **CARD**.
--from TEXT starts reading at the first line containing TEXT (skip a file header).
"""
import re
import sys

CONNECTIVES = re.compile(r"\b(because|so|though|and|but|or|which|when|while|since|until|even though|anything like that)\b", re.I)
FEELING = re.compile(r"\b(thank god|ashamed|terrified|scared|sick|cried|cry|honestly|craziest|can't believe|couldn't believe|worst|relief|happy|heart ?broke|never)\b", re.I)


def paragraphs(text):
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in block.splitlines()]
        lines = [l for l in lines if l and not l.startswith("#") and not l.startswith("---")]
        lines = [l for l in lines if not re.fullmatch(r"\*\*[^*]+\*\*.*", l) or len(l) > 80]
        lines = [re.sub(r"^\*\*[^*]+\*\*\s*", "", l) for l in lines]
        lines = [re.sub(r"^\([^)]*\)\s*", "", l) for l in lines]
        lines = [l for l in lines if l and not l.lower().startswith(("click path", "swipe:", "source", "names none"))]
        if lines:
            out.append(" ".join(lines))
    return out


def sentences(p):
    parts = re.split(r"(?<=[.!?])\s+", p.strip())
    return [s for s in parts if s]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8").read()
    if "--from" in sys.argv:
        key = sys.argv[sys.argv.index("--from") + 1]
        i = text.find(key)
        if i >= 0:
            text = text[i:]
    flags = []
    paras = paragraphs(text)
    short_run = 0
    for n, p in enumerate(paras, 1):
        words = len(p.split())
        sents = sentences(p)
        conn = len(CONNECTIVES.findall(p))
        feel = bool(FEELING.search(p))
        print(f"P{n:02d}  {words:3d} words  {len(sents)} sent  {conn} connectives  {'feeling' if feel else ''}")
        if words > 40:
            flags.append(f"P{n}: {words} words, over 40 (chunky). Split the idea or cut.")
        if words < 8 and not feel:
            flags.append(f"P{n}: {words} words with no feeling in it (fragment for punch). Say the whole thought.")
        if words >= 12 and conn == 0:
            flags.append(f"P{n}: no connective (because/so/though/and). Reads written, not spoken.")
        if len(sents) >= 3:
            flags.append(f"P{n}: {len(sents)} sentences in one paragraph. One idea per paragraph.")
        if re.match(r"^(This|That|He|She)\b", p) and n > 1:
            flags.append(f"P{n}: opens on a pronoun. Name the thing.")
        for s in sents:
            if len(s.split()) < 6:
                short_run += 1
                if short_run >= 3:
                    flags.append(f"P{n}: three short sentences in a row ('{s}'). Choppy.")
            else:
                short_run = 0
    print()
    if flags:
        print("FLAGS")
        for f in flags:
            print(" -", f)
    else:
        print("No flags. Now read it aloud and put it next to the Benny paragraphs.")


if __name__ == "__main__":
    main()
