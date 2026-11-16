#!/usr/bin/env python3
"""reply_eval.py: the daily number for how readable Claude's replies to Ryan are.

  today                 rate for today from reply-eval.jsonl (what the Stop hook logs), appended to REPLY-EVAL.md
  day YYYY-MM-DD        same for one day
  backfill --days N     rebuild the daily numbers for the last N days straight from the session transcripts
                        (so the number exists for days before the hook was logging), appended to REPLY-EVAL.md
  complaints --days N   Leo's test: take the reply right before each time Ryan said he could not understand,
                        run the six checks on it, and compare the flag rate with the base rate. If the checks
                        do not flag the replies he complained about more often than the rest, the checks are wrong.

The checks live in hook_stop_reply.py (check_reply). This file only counts.
"""
import sys, os, re, json, glob, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hook_stop_reply import check_reply, DEPTH, COPYFILE, texts  # noqa: E402

TRANSCRIPTS = os.path.expanduser("~/.claude/projects/-Users-ryanconnolly-SkyHouse-Exodus")
LOG = os.path.join(HERE, "reply-eval.jsonl")
MD = os.path.join(HERE, "REPLY-EVAL.md")
CHECKS = ["long", "bullets", "toolname", "number", "preamble", "grade"]
COMPLAINT = re.compile(r"i don'?t (know|understand) what you('re| are)? (saying|talking)|i don'?t understand|confusing|hieroglyph|plain english|not (really )?speaking english|what do you keep doing|what\?$|dead simple", re.I)


def replies_from_transcripts(days, skip_session=None):
    """Yield (date, session, last_user, reply, exempt) for every end-of-turn reply in the last N days."""
    cut = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).isoformat()
    for f in glob.glob(os.path.join(TRANSCRIPTS, "*.jsonl")):
        sid = os.path.basename(f)[:-6]
        if skip_session and sid.startswith(skip_session):
            continue
        last_user, wrote_copy = "", False
        pending = None  # (date, reply) of an assistant text not yet known to be end-of-turn
        with open(f, errors="ignore") as fh:
            for line in fh:
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                ts = e.get("timestamp") or ""
                m = e.get("message") or {}
                role = m.get("role") or e.get("type")
                if role == "user" and not e.get("isMeta"):
                    c = m.get("content")
                    if isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c):
                        continue
                    t = " ".join(texts(m)).strip()
                    t = re.sub(r"</?pasted_content[^>]*>", "", t).strip()
                    if t and not t.startswith(("<", "[", "The user hasn't heard from you", "Stop hook feedback", "Your reply is")):
                        if pending and pending[0] >= cut:
                            exempt = "wrote_copy" if wrote_copy else ("depth_asked" if DEPTH.search(last_user) else None)
                            yield pending[0][:10], sid, last_user, pending[1], exempt, t
                        pending, wrote_copy, last_user = None, False, t
                elif role == "assistant":
                    t = " ".join(texts(m)).strip()
                    has_tool = any(isinstance(b, dict) and b.get("type") == "tool_use" for b in (m.get("content") or []))
                    for b in (m.get("content") or []):
                        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in ("Write", "Edit", "MultiEdit"):
                            if COPYFILE.search(str((b.get("input") or {}).get("file_path", ""))):
                                wrote_copy = True
                    if t and not has_tool:
                        pending = (ts, t)
                    elif has_tool:
                        pending = None
        if pending and pending[0] >= cut:
            exempt = "wrote_copy" if wrote_copy else ("depth_asked" if DEPTH.search(last_user) else None)
            yield pending[0][:10], sid, last_user, pending[1], exempt, ""


def tally(rows):
    """rows: iterable of (flags list, exempt). Returns dict with n, checked, failed, per-check counts."""
    t = {"n": 0, "checked": 0, "failed": 0, "per": collections.Counter()}
    for flags, exempt in rows:
        t["n"] += 1
        if exempt:
            continue
        t["checked"] += 1
        if flags:
            t["failed"] += 1
        for fl in flags:
            t["per"][fl] += 1
    return t


def line_for(day, t):
    if not t["checked"]:
        return f"| {day} | {t['n']} | 0 | - | " + " | ".join("-" for _ in CHECKS) + " |"
    pct = lambda k: f"{100 * t['per'][k] // t['checked']}%"
    return (f"| {day} | {t['n']} | {t['checked']} | **{100 * t['failed'] // t['checked']}%** | "
            + " | ".join(pct(k) for k in CHECKS) + " |")


HEADER = ("# Reply eval: can Ryan read the reply?\n\n"
          "One line per day. `failed` = replies that broke at least one of the six rules. The rules and why: "
          "`hook_stop_reply.py`. Rebuild a day with `python3 tools/copygate/reply_eval.py day YYYY-MM-DD`.\n\n"
          "| day | replies | checked | failed | long | bullets | toolname | number | preamble | grade |\n"
          "|---|---|---|---|---|---|---|---|---|---|\n")


def write_md(lines_by_day):
    old = {}
    if os.path.exists(MD):
        for l in open(MD):
            m = re.match(r"\| (\d{4}-\d{2}-\d{2}) \|", l)
            if m:
                old[m.group(1)] = l.rstrip("\n")
    old.update(lines_by_day)
    with open(MD, "w") as f:
        f.write(HEADER)
        for day in sorted(old):
            f.write(old[day] + "\n")


def from_log(day):
    rows = []
    if os.path.exists(LOG):
        for l in open(LOG):
            try:
                j = json.loads(l)
            except Exception:
                continue
            if j.get("at", "")[:10] == day:
                rows.append((j.get("flags") or [], j.get("exempt")))
    return tally(rows)


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "today"
    days = int(argv[argv.index("--days") + 1]) if "--days" in argv else 7
    if cmd in ("today", "day"):
        day = argv[2] if cmd == "day" and len(argv) > 2 else datetime.date.today().isoformat()
        t = from_log(day)
        line = line_for(day, t)
        write_md({day: line})
        print(line)
        return 0
    if cmd == "backfill":
        by_day = collections.defaultdict(list)
        for day, sid, user, reply, exempt, _nxt in replies_from_transcripts(days):
            r = check_reply(user, reply)
            by_day[day].append((r["flags"], exempt))
        lines = {d: line_for(d, tally(rows)) for d, rows in by_day.items()}
        write_md(lines)
        print(HEADER.split("\n")[-3])
        for d in sorted(lines):
            print(lines[d])
        return 0
    if cmd == "complaints":
        base, comp = [], []
        examples = []
        for day, sid, user, reply, exempt, nxt in replies_from_transcripts(days):
            if exempt:
                continue
            r = check_reply(user, reply)
            base.append(r["flags"])
            if nxt and COMPLAINT.search(nxt):
                comp.append(r["flags"])
                if len(examples) < 6:
                    examples.append((day, nxt[:70].replace("\n", " "), r["flags"], r["words"]))
        def rate(xs):
            return f"{100 * sum(1 for f in xs if f) // max(len(xs), 1)}% of {len(xs)}"
        print(f"Replies checked in the last {days} days: flagged {rate(base)}")
        print(f"Replies Ryan then said he could not understand: flagged {rate(comp)}")
        per = collections.Counter(fl for f in comp for fl in f)
        print("  which rules those broke:", dict(per))
        print("  the ones the checks missed:", sum(1 for f in comp if not f))
        for d, q, fl, w in examples:
            print(f"  [{d}] he said: {q!r}  flags={fl} words={w}")
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
