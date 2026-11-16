#!/usr/bin/env python3
"""Intake-form alignment check: gather the client's intake lines for an offer,
scan launch copy for red-line words, and stamp the report files.

The judgment (ALIGNED / PARTIAL / MISMATCH / NOT IN INTAKE per element) is made
by Claude in the intake-check skill. This script only does the mechanical part:

  python3 tools/intake/intake_check.py prodenta                 # print the intake bundle
  python3 tools/intake/intake_check.py prodenta --new squeeze-top5
                                                               # + create the launch spec from the template
  python3 tools/intake/intake_check.py prodenta --scan offers/prodenta/ads/*.md offers/prodenta/landers/*/advertorial.html
                                                               # + red-line word scan with context
  python3 tools/intake/intake_check.py prodenta --out /path/bundle.md

Sources, in order (each one that exists is included, missing ones are listed):
  offers/<slug>/inputs/intake-survey*.txt          the client's own words (raw docx/pdf text)
  offers/<slug>/inputs/*onboarding*.txt            technical onboarding (pages, tracking)
  offers/<slug>/research/00-client-assets.md       the "what the client told us" + funnel + congruence sections
  offers/<slug>/research/01b-reverse-brief.md      the VSL/page lead (first table) + every "mismatch" line
  offers/<slug>/OFFER.md                           compliance / red-line sections
  offers/<slug>/LAUNCH.md                          launch profile (page, audience)
Stdlib only.
"""
import argparse
import datetime as dt
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL = os.path.join(ROOT, ".claude", "skills", "intake-check")

# Words that are a red line on nearly every offer. OFFER.md / the intake add offer-specific ones.
DEFAULT_WORDS = [
    r"\bcures?\b", r"\bcured\b", r"\breverses?\b", r"\breversal\b", r"\bheals?\b",
    r"\btreat(s|ed|ing)? (the |your |his |her |their )?(disease|condition|liver|gum|infection|illness|arthritis)",
    r"\bclinically proven\b", r"\bguarantee[ds]?\b", r"\bFDA[- ]approved\b", r"\bDr\.? [A-Z][a-z]+",
    r"\bpermission\b", r"\bdrink more\b", r"\bcapsules?\b",
]


def offer_dir(slug):
    d = os.path.join(ROOT, "offers", slug)
    if not os.path.isdir(d):
        sys.exit(f"no offer folder: {d}")
    return d


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def sections(md, *needles):
    """Return the markdown sections (## or ###) whose heading contains any needle, case-insensitive."""
    out, keep, buf, head = [], False, [], ""
    for line in md.splitlines():
        if re.match(r"^#{2,3} ", line):
            if keep and buf:
                out.append("\n".join(buf))
            head = line
            keep = any(n.lower() in line.lower() for n in needles)
            buf = [line] if keep else []
        elif keep:
            buf.append(line)
    if keep and buf:
        out.append("\n".join(buf))
    return out


def strip_html(path):
    t = read(path)
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    return "\n".join(l.strip() for l in t.splitlines() if l.strip())


def bundle(slug):
    d = offer_dir(slug)
    parts, missing = [], []

    intake = sorted(glob.glob(os.path.join(d, "inputs", "intake-survey*.txt")))
    if intake:
        for p in intake:
            parts.append(f"# SOURCE: {os.path.relpath(p, ROOT)} (the client's own words, raw)\n\n" + read(p))
    else:
        missing.append("inputs/intake-survey*.txt (no raw intake text; ask where the live form lives)")

    onboarding = sorted(glob.glob(os.path.join(d, "inputs", "*onboarding*.txt")))
    for p in onboarding:
        parts.append(f"# SOURCE: {os.path.relpath(p, ROOT)} (technical onboarding)\n\n" + read(p)[:6000])

    ca = os.path.join(d, "research", "00-client-assets.md")
    if os.path.exists(ca):
        secs = sections(read(ca), "client told us", "funnel", "congruence", "contradict", "open asks", "rules")
        if secs:
            parts.append(f"# SOURCE: {os.path.relpath(ca, ROOT)} (distilled intake + funnel)\n\n" + "\n\n".join(secs))
        else:
            parts.append(f"# SOURCE: {os.path.relpath(ca, ROOT)} (no matching sections; first 4000 chars)\n\n" + read(ca)[:4000])
    else:
        missing.append("research/00-client-assets.md")

    rb = os.path.join(d, "research", "01b-reverse-brief.md")
    if os.path.exists(rb):
        md = read(rb)
        head = md[:3500]
        mism = [l for l in md.splitlines() if re.search(r"mismatch|never says|not in the vsl|flop", l, re.I)]
        parts.append(f"# SOURCE: {os.path.relpath(rb, ROOT)} (what the funnel's own page/VSL leads with)\n\n"
                     + head + "\n\n## Lines flagged mismatch / never says / flop\n" + "\n".join(mism[:40]))
    else:
        missing.append("research/01b-reverse-brief.md (no VSL/page reverse brief; funnel lead unchecked)")

    off = os.path.join(d, "OFFER.md")
    if os.path.exists(off):
        secs = sections(read(off), "compliance", "red line", "never", "rules", "funnel", "avatar", "who")
        parts.append(f"# SOURCE: OFFER.md\n\n" + ("\n\n".join(secs) if secs else read(off)[:3000]))
    else:
        missing.append("OFFER.md (optional)")

    la = os.path.join(d, "LAUNCH.md")
    if os.path.exists(la):
        parts.append("# SOURCE: LAUNCH.md\n\n" + read(la)[:3000])

    header = f"# INTAKE BUNDLE: {slug} ({dt.date.today().isoformat()})\n"
    if missing:
        header += "\nMISSING SOURCES:\n" + "\n".join(f"- {m}" for m in missing) + "\n"
    return header + "\n\n---\n\n".join(parts)


def scan(paths, words):
    """Red-line word scan with one line of context per hit. HTML is stripped to text first."""
    rx = re.compile("|".join(words), re.I)
    out = []
    for p in paths:
        text = strip_html(p) if p.lower().endswith((".html", ".htm")) else read(p)
        hits = []
        for i, line in enumerate(text.splitlines(), 1):
            for m in rx.finditer(line):
                hits.append(f"  L{i} [{m.group(0)}] {line.strip()[:150]}")
        out.append(f"## {os.path.relpath(p, ROOT)}: {len(hits)} hit(s)\n" + ("\n".join(hits) if hits else "  none"))
    return "\n\n".join(out)


def new_launch(slug, name):
    d = os.path.join(offer_dir(slug), "intake-checks")
    os.makedirs(d, exist_ok=True)
    stamp = dt.date.today().isoformat()
    launch = os.path.join(d, f"{stamp}-{name}.launch.md")
    report = os.path.join(d, f"{stamp}-{name}.md")
    if not os.path.exists(launch):
        t = read(os.path.join(SKILL, "LAUNCH-template.md"))
        t = t.replace("<slug>", slug).replace("<name>", name).replace("<date>", stamp)
        with open(launch, "w", encoding="utf-8") as f:
            f.write(t)
    return launch, report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--new", metavar="NAME", help="create offers/<slug>/intake-checks/<date>-NAME.launch.md from the template")
    ap.add_argument("--scan", nargs="*", metavar="PATH", help="launch copy / landers to scan for red-line words")
    ap.add_argument("--words", nargs="*", help="extra regexes for the scan (offer-specific red lines)")
    ap.add_argument("--out", help="write the bundle here instead of stdout")
    a = ap.parse_args()

    text = bundle(a.slug)
    if a.scan:
        text += "\n\n---\n\n# RED-LINE WORD SCAN\n\n" + scan(a.scan, DEFAULT_WORDS + (a.words or []))
    if a.new:
        launch, report = new_launch(a.slug, a.new)
        text += f"\n\n---\n\nLAUNCH SPEC: {os.path.relpath(launch, ROOT)}\nREPORT GOES TO: {os.path.relpath(report, ROOT)}\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {a.out} ({len(text):,} chars)")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
