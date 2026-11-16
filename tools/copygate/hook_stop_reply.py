#!/usr/bin/env python3
"""Stop hook: measures every reply to Ryan against the plain-reply rules. Never blocks.

Ryan 10-27: "STOP these confusing, long responses I can't stand it anymore."
Ryan 11-06: "I don't know what you're saying, literally every single time you respond to me." Counted that day: 252 of 568
sessions since June had him say he could not understand the reply; 44% of the 2,976 replies in the prior 7 days broke one
of these rules. The old version of this hook only logged length misses and skipped any message with a word like "hooks" or
"copy" in it, which was nearly every message he sends.

What it does now: after every reply, it runs the six checks below and appends one line (pass or fail, with the flags) to
tools/copygate/reply-eval.jsonl. `python3 tools/copygate/reply_eval.py today` turns that into the daily number in
REPLY-EVAL.md. It never blocks (Ryan 11-04: "I don't want to have to see the same thing twice"). Any error = allow.

The six checks (Ryan's own rules, dreaming 2026-11-02 proposals 1d, 4a, 4b, 4d):
  long        prose over 100 words (fenced blocks, URLs and the thing he asked to see are not counted)
  bullets     more than 3 top-level bullets
  toolname    a tool, script, file or path name in the reply (he cannot see those things)
  number      a number he did not ask for
  preamble    the first line is about what I am doing, not the answer
  grade       reads above 4th grade (Ryan 11-06: "talking like a third grader and keeping things simple")

Exempt: when the turn wrote an ad/advertorial/lander/video file (the reply IS the copy) and when Ryan asked for depth with one
of a few words (diagnose, deep dive, walk me through, full read, explain, in detail, report, write-up, breakdown). Nothing else.
"""
import json, re, sys, os, datetime

LIMIT_WORDS = 100
LIMIT_BULLETS = 3
COPYFILE = re.compile(r"/offers/[^/]+/(ads|advertorials|landers|videos)/", re.I)
# 11-06: the skip list is only the words that really mean "go long"
DEPTH = re.compile(r"\b(diagnos\w*|deep dive|walk me( through)?|full read|explain|in detail|long(er)? (version|form|read)|write[- ]?up|report|breakdown)\b", re.I)
# when Ryan asked to SEE the thing, the thing is the reply; only the prose around it is counted
SHOW = re.compile(r"\b(show (me|it)|let me see|see it|in the chat|paste|list them|i don'?t see)\b", re.I)
FENCE = re.compile(r"```.*?```", re.S)
URL = re.compile(r"https?://\S+|www\.\S+", re.I)
DELIVERABLE_LINE = re.compile(r"^\s*(\d+[.)]\s|>\s?|[\"“])")
# a tool, script, file or path: things on my screen, never on his
TOOLNAME = re.compile(
    r"(\b[\w-]+\.(py|md|html|json|jsonl|txt|csv|yaml|yml|sh)\b"
    r"|(?<![\w/])(tools|offers|strategist-references|\.claude|~)/[\w./-]+"
    r"|\b(subagent|sub-agent|stop hook|pretooluse|posttooluse|regex|npx exodus|curl|jsonl|frontmatter|stdout|preflight\.md|the gate|the judge|coldread|gate\.py|judge\.py|kie\.py|pairs\.py|hook_\w+)\b)",
    re.I)
# a number: 2+ digits, a percent, a decimal, or a dollar figure
NUMBER = re.compile(r"\$\s?\d|\b\d+(\.\d+)?\s?%|\b\d+\.\d+\b|\b\d{2,}\b")
# dates and clock times are not the numbers he means ("Nov 13", "11-13", "2026-11-06", "3:14")
DATE_OR_TIME = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[-/]\d{1,2}\b|\b\d{1,2}:\d{2}\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.? \d{1,2}\b|\b\d{1,2} (jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\b|\b(19|20)\d{2}\b", re.I)
# Ryan asked for a number if his message has a digit or one of these words
ASKED_NUMBER = re.compile(r"\d|how (many|much|long)|number|count|percent|cost|price|words|seconds|minutes|score|rate|stats?|numbers?", re.I)
# the first line is about what I am doing, not the answer
PREAMBLE = re.compile(
    r"^\s*(i'?ll\b|i'?m going|i am going|let me\b|before (i|we)\b|first,|now i\b|here'?s what i\b|quick(ly)?\b|reading\b|checking\b|pulling\b|building\b|working on\b|got it[.,]|okay,? so\b|ok,? so\b|starting\b|looking (at|into)\b|i (just |already )?(read|pulled|checked|ran|looked)\b|i have (read|pulled|checked)\b|you'?re right[.,] (i|it)\b)",
    re.I)


def split_prose(text, show_asked):
    """(prose, deliverable_lines, total_lines). Fenced blocks and URLs never count. When Ryan asked to see the thing, or
    the reply is mostly a list / fenced block / quoted copy, numbered and quoted lines are the deliverable and drop out."""
    fenced_lines = sum(m.group(0).count("\n") + 1 for m in FENCE.finditer(text))
    body = FENCE.sub("", text)
    body = URL.sub("", body)
    lines = [l for l in body.split("\n") if l.strip()]
    deliv = [l for l in lines if DELIVERABLE_LINE.match(l)]
    total = len(lines) + fenced_lines
    mostly = total > 0 and (len(deliv) + fenced_lines) * 2 >= total
    if show_asked or mostly:
        prose = [l for l in lines if not DELIVERABLE_LINE.match(l)]
    else:
        prose = lines
    return "\n".join(prose), len(deliv), total


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def grade(text):
    """Flesch-Kincaid grade of the prose. Ryan 11-06: talk like a third grader. Rule: 4 or under."""
    sents = [x for x in re.split(r"(?<=[.!?])\s+|\n+", text) if re.search(r"[A-Za-z]", x)]
    words = [w for x in sents for w in re.findall(r"[A-Za-z][A-Za-z'\u2019-]*", x)]
    if not words or not sents:
        return 0.0
    syl = sum(syllables(w) for w in words)
    return round(0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59, 1)


LIMIT_GRADE = 4.0


def check_reply(last_user, reply):
    """Run the five checks. Returns a dict with words, bullets, flags (list of names) and the evidence per flag."""
    prose, deliv, total = split_prose(reply, bool(SHOW.search(last_user or "")))
    words = len(re.findall(r"\S+", prose))
    bullets = len(re.findall(r"^[-*]\s", prose, flags=re.M))
    flags, why = [], {}
    if words > LIMIT_WORDS:
        flags.append("long"); why["long"] = f"{words} words of prose, rule is {LIMIT_WORDS}"
    if bullets > LIMIT_BULLETS:
        flags.append("bullets"); why["bullets"] = f"{bullets} top-level bullets, rule is {LIMIT_BULLETS}"
    m = TOOLNAME.search(prose)
    if m:
        flags.append("toolname"); why["toolname"] = m.group(0)
    if not ASKED_NUMBER.search(last_user or ""):
        m = NUMBER.search(DATE_OR_TIME.sub(" ", prose))
        if m:
            flags.append("number"); why["number"] = m.group(0)
    g = grade(re.sub(r"[*_`#>-]", " ", prose))
    if g > LIMIT_GRADE and words >= 12:
        flags.append("grade"); why["grade"] = f"reads at grade {g}, rule is {LIMIT_GRADE:g}"
    first = next((l for l in reply.split("\n") if l.strip()), "")
    first = re.sub(r"^[\s#*>-]+", "", first)
    if PREAMBLE.match(first):
        flags.append("preamble"); why["preamble"] = first[:60]
    return {"words": words, "bullets": bullets, "deliverable_lines": deliv, "flags": flags, "why": why}


def texts(msg):
    c = msg.get("content")
    if isinstance(c, str):
        return [c]
    return [b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text"]


def last_turn(path):
    """(last_user, last_assistant_text, wrote_copy) from a transcript file."""
    last_user, last_asst, wrote_copy = "", "", False
    with open(path, errors="ignore") as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            m = e.get("message") or {}
            role = m.get("role") or e.get("type")
            if role == "user" and not e.get("isMeta"):
                t = " ".join(texts(m)).strip()
                t = re.sub(r"</?pasted_content[^>]*>", "", t).strip()
                if t and not t.startswith(("<", "[", "The user hasn't heard from you", "Stop hook feedback", "Your reply is")):
                    last_user, last_asst, wrote_copy = t, "", False
            elif role == "assistant":
                t = " ".join(texts(m)).strip()
                if t:
                    last_asst = t
                for b in (m.get("content") or []):
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in ("Write", "Edit", "MultiEdit"):
                        if COPYFILE.search(str((b.get("input") or {}).get("file_path", ""))):
                            wrote_copy = True
    return last_user, last_asst, wrote_copy


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0
    path = data.get("transcript_path")
    if not path:
        return 0
    last_user, last_asst, wrote_copy = last_turn(path)
    if not last_asst:
        return 0
    exempt = None
    if wrote_copy:
        exempt = "wrote_copy"
    elif DEPTH.search(last_user or ""):
        exempt = "depth_asked"
    r = check_reply(last_user, last_asst)
    log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reply-eval.jsonl")
    with open(log, "a") as f:
        f.write(json.dumps({"at": datetime.datetime.now().isoformat(timespec="seconds"), "session": data.get("session_id"),
                            "exempt": exempt, "words": r["words"], "bullets": r["bullets"],
                            "flags": [] if exempt else r["flags"], "why": {} if exempt else r["why"],
                            "asked": (last_user or "")[:80]}) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException:
        sys.exit(0)
