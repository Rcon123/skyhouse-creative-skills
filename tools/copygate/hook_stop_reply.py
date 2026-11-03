#!/usr/bin/env python3
"""Stop hook: Ryan's replies stay short and plain, automatically.

Ryan 10-27: "STOP these confusing, long responses I can't stand it anymore." "I need you to listen to me."
Reads the transcript, takes the last assistant text, and sends it back for a rewrite when it runs over the limit,
unless Ryan asked for depth in his last message (diagnose, deep dive, walk me through, full read, explain, long,
write-up, report). One rewrite pass only (stop_hook_active guards the loop). Any error = allow.
dreaming 2026-11-02 (proposals 1a, 1b, 1c, 1e; ~70 sessions, 250+ fires): the thing Ryan asked to see is never counted,
fenced blocks and URLs never count, only top-level bullets count, and the block names the real fault and asks for a cut.
"""
import json, re, sys

LIMIT_WORDS = 130
LIMIT_BULLETS = 3
COPYFILE = re.compile(r"/offers/[^/]+/(ads|advertorials|landers|videos)/", re.I)
# dreaming 2026-11-02 (1c): re-?explain, walk me, dead simple, fourth grade, make(s) sense, what did you (just) do
DEPTH = re.compile(r"\b(diagnos\w*|deep dive|walk me( through)?|full read|re-?explain|explain|in detail|dead simple|fourth[- ]grade|makes? sense|what did you (just )?do|long(er)? (version|form|read)|write[- ]?up|report|breakdown|script|draft|rewrite|copy|version|hooks?|ads?|headlines?|write|start the|list|examples?|options|numbers|pick|lines?|say|says|saying|body|p\.s\.|paragraphs?|sentences?|words?|stronger|confusing|boring|loom\.com)\b", re.I)
# dreaming 2026-11-02 (1a): when Ryan asked to SEE the thing, the thing is the reply; only the prose around it is counted
# (sessions 10-28_55892592, 10-28_66850cc4, 10-30_c21efef8, 10-26_601f85f7, 10-27_310bc5c8)
SHOW = re.compile(r"\b(show (me|it)|let me see|see it|in the chat|paste|list them|i don'?t see)\b", re.I)
FENCE = re.compile(r"```.*?```", re.S)
URL = re.compile(r"https?://\S+|www\.\S+", re.I)
NUMBERED = re.compile(r"^\s*\d+[.)]\s")
# a line that is the deliverable itself, not prose about it: numbered item, blockquote, or a quoted hook/headline line
DELIVERABLE_LINE = re.compile(r"^\s*(\d+[.)]\s|>\s?|[\"\u201c])")


def split_prose(text, show_asked):
    """Return (prose, deliverable_lines, total_lines). Fenced blocks and URLs never count (1b).
    When Ryan asked to see the thing, or the reply is mostly a list / fenced block / quoted copy,
    numbered and quoted lines are the deliverable and drop out of the count too (1a)."""
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


def texts(msg):
    c = msg.get("content")
    if isinstance(c, str):
        return [c]
    out = []
    for b in c or []:
        if isinstance(b, dict) and b.get("type") == "text":
            out.append(b.get("text", ""))
    return out


def main():
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0
    path = data.get("transcript_path")
    if not path:
        return 0
    last_user, last_asst = "", ""
    wrote_copy = False  # 10-29: when the turn wrote an ad/advertorial/hooks file, the reply IS the copy; never trim it
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
                # text Ryan pasted in arrives wrapped in <pasted_content> tags; it is still his message
                t = re.sub(r"</?pasted_content[^>]*>", "", t).strip()
                # harness nudges and hook feedback are not Ryan's messages; they must not reset what he last asked for
                if t and not t.startswith(("<", "[", "The user hasn't heard from you", "Stop hook feedback", "Your reply is")):
                    last_user = t
                    last_asst = ""
                    wrote_copy = False
            elif role == "assistant":
                t = " ".join(texts(m)).strip()
                if t:
                    last_asst = t
                for b in (m.get("content") or []):
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in ("Write", "Edit", "MultiEdit"):
                        if COPYFILE.search(str((b.get("input") or {}).get("file_path", ""))):
                            wrote_copy = True
    if not last_asst or wrote_copy or DEPTH.search(last_user or ""):
        return 0
    # 10-29: a numbered list Ryan is meant to pick from (hooks, options, rules) is the deliverable; never trim it.
    # dreaming 2026-11-02: that rule now lives in split_prose (the list drops out, the prose around it is still counted).
    prose, deliv, total = split_prose(last_asst, bool(SHOW.search(last_user or "")))
    words = len(re.findall(r"\S+", prose))
    # 1b: only top-level bullets count (no leading whitespace); nested URLs or sub-points are not bullets
    bullets = len(re.findall(r"^[-*]\s", prose, flags=re.M))
    if words <= LIMIT_WORDS and bullets <= LIMIT_BULLETS:
        return 0
    # 1e: name the real fault and ask for a cut, never a rewrite (7 of 14 fires in one batch came back a few words shorter)
    faults = []
    if words > LIMIT_WORDS:
        faults.append(f"the prose is {words} words, the rule is under {LIMIT_WORDS}: cut {max(1, (words - LIMIT_WORDS + 19) // 20)} "
                      "whole sentence(s), usually the reasoning or the caveat, and keep the rest word for word")
    if bullets > LIMIT_BULLETS:
        faults.append(f"{bullets} top-level bullets, the rule is {LIMIT_BULLETS}: drop or merge {bullets - LIMIT_BULLETS}, "
                      "keep the one that says what changed, the one thing he has to do, and what is not done")
    kept = f" The {deliv} numbered or quoted lines are the deliverable and were not counted; keep them exactly." if deliv else ""
    print(json.dumps({"decision": "block", "reason":
        "Your reply is over Ryan's limit. Fault: " + "; ".join(faults) + "." + kept +
        " Do not resend the same text a few words shorter and do not rewrite it. Cut, then stop."}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException:
        sys.exit(0)
