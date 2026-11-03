#!/usr/bin/env python3
"""hook-writer judge: a stranger reads each gate survivor once, cold. No login, no background process.

  python3 tools/hooks/judge.py prompt <hooks.md>                 writes <hooks.md>.judge-prompt.md for a FRESH in-session agent
  python3 tools/hooks/judge.py stamp  <hooks.md> --json <out>    turns that agent's JSON array into <hooks.md>.hookjudge.json
  python3 tools/hooks/judge.py headless <hooks.md>               old route: one `claude -p` call per hook (needs a CLI login)
  python3 tools/hooks/judge.py nojudge  <hooks.md>               judge OFF (Ryan 10-29): stamps every gate survivor PASS

The writer never answers the questions itself. The agent that reads the prompt has no other context.
Exit: 0 stamp written and something survived, 1 stamp written and nothing survived, 2 structure error, 4 reader unavailable.
"""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(WS / "tools" / "copygate"))
import gate  # noqa: E402

PROMPT = HERE / "READER-PROMPT.md"


def prompt_path(path):
    return Path(str(path) + ".judge-prompt.md")


def out_path(path):
    return Path(str(path) + ".judge-out.json")


def questions(judge_rules, start=3):
    qs, shape, n = [], {"n": 1, "repeat": "<one plain sentence or empty>", "stop": True}, start
    for r in judge_rules:
        s = r["spec"]
        if s.get("primitive") == "score_vs_examples":
            qs.append(f"{n}. {r['id']}: {s['question']} Answer with a whole number from 1 to 10.")
            shape[r["id"]] = 10
        else:
            qs.append(f"{n}. {r['id']}: {s['question']} Answer with exactly one of: " + ", ".join(s["answers"]) + ".")
            shape[r["id"]] = s["answers"][0]
        n += 1
    shape["why"] = "<one plain line>"
    return "\n".join(qs), n, shape


def gate_or_die(path):
    text = Path(path).read_text()
    try:
        res = gate.check(text, path)
    except gate.GateError as e:
        print("gate: " + str(e), file=sys.stderr); sys.exit(2)
    if res["set_fails"]:
        for s in res["set_fails"]:
            print("gate: " + s, file=sys.stderr)
        print("fix the file first; the judge does not read a short set", file=sys.stderr); sys.exit(2)
    return res


def write_prompt(path):
    res = gate_or_die(path)
    reader = res["header"]["reader"]
    alive = [h for h in res["hooks"] if not h["fails"]]
    qs, last, shape = questions(res["judge_rules"])
    lines = "\n".join(f"{h['n']}. {h['text']}" for h in alive)
    examples = ""
    for r in res["judge_rules"]:
        if r["spec"].get("primitive") == "score_vs_examples":
            ex = (WS / r["spec"]["examples"]).read_text()
            ex_lines = [l.strip() for l in ex.split("\n") if l.strip() and l.strip()[0].isdigit()]
            examples = ("===== LINES THAT ARE A 10 (Ryan's approved hooks; the bar) =====\n" + "\n".join(ex_lines) +
                        "\n\nThese are from other products. Judge only how hard each one hits, not the topic.\n\n")
    body = (
        f"You are {reader}. You are scrolling Facebook on your phone. You are not a copywriter, not a moderator, "
        "not a reviewer. You are one person seeing one line at a time.\n\n"
        f"Below are {len(alive)} lines. Each one is the FIRST line of a different post sliding past your thumb. "
        "Take them one at a time. Forget the one before. Do not compare them, rank them, or look for a theme; "
        "each is the only line you see at that moment. Swearing, ugly words and hard claims are normal on your feed; "
        "do not judge taste or manners. Judge only what the line does to you.\n\n"
        "For EACH line answer:\n"
        "1. repeat: Say back what the line is telling you, in your own words, one short plain sentence. If you honestly cannot tell what it means, answer \"\".\n"
        "2. stop: Would your thumb stop so you could read the next line? true or false. Not whether you like it. Whether you stop.\n"
        f"{qs}\n{last}. why: One plain line on what made you stop or keep scrolling.\n\n"
        + examples +
        "===== THE LINES =====\n" + lines + "\n\n"
        f"Write your answer as a JSON array, one object per line, keyed by its number, to the file {out_path(path)} "
        "(use your Write tool), and reply with nothing else. Exact shape of each object:\n"
        + json.dumps(shape, ensure_ascii=False) + "\n"
    )
    prompt_path(path).write_text(body)
    print(f"prompt: {prompt_path(path)}")
    print(f"{len(alive)} lines for the reader. Spawn ONE fresh agent (general-purpose, sonnet) whose whole prompt is that file's "
          f"contents. It writes {out_path(path)}. Then: python3 tools/hooks/judge.py stamp {path} --json {out_path(path)}")
    return 0


def verdict(j, judge_rules):
    killed = []
    if not str(j.get("repeat", "")).strip():
        killed.append("J-repeat")
    if not j.get("stop"):
        killed.append("J-stop")
    for r in judge_rules:
        s = r["spec"]
        if s.get("primitive") == "score_vs_examples":
            try:
                score = int(str(j.get(r["id"], "")).strip())
            except ValueError:
                score = 0
            if score < s["min"]:
                killed.append(f"{r['id']}<{s['min']}")
            continue
        a = str(j.get(r["id"], "")).strip().lower()
        allowed = [x.lower() for x in s["answers"]]
        if a == s["fail_when"].lower() or a not in allowed:
            killed.append(r["id"])
    return ("FAIL" if killed else "PASS"), killed


def write_stamp(path, res, answers, reader_kind, seconds=0):
    """answers: {n: judge-json or None}"""
    jr = res["judge_rules"]
    out_hooks = []
    for h in res["hooks"]:
        row = {"n": h["n"], "text": h["text"], "star": h["star"], "category": h.get("category"), "gate": h["fails"],
               "judge": None, "killed_by": list(h["fails"]), "verdict": "FAIL" if h["fails"] else None}
        if not h["fails"] and not jr:
            row["verdict"] = "PASS"  # no active judge rules (Ryan 10-29: the judge is off); the gate decides
        elif not h["fails"]:
            j = answers.get(h["n"])
            if not isinstance(j, dict):
                row["verdict"] = "ERROR"; row["judge"] = {"error": "no answer from the reader"}
            else:
                v, killed = verdict(j, jr)
                row["judge"] = j; row["verdict"] = v; row["killed_by"] = killed
        out_hooks.append(row)
    stamp = {"file": str(Path(path).resolve()), "sha256": gate.sha(path), "rules_sha": res["rules_sha"],
             "lane": res["header"]["lane"], "header": res["header"], "reader": res["header"]["reader"],
             "model": reader_kind, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "seconds": seconds,
             "set_spec": (res["set_spec"] or (None, {}))[1], "cat_spec": (res.get("cat_spec") or (None, None))[1],
             "set_fails": res["set_fails"], "hooks": out_hooks}
    gate.stamp_path(path).write_text(json.dumps(stamp, indent=1, ensure_ascii=False))
    alive = [r for r in out_hooks if not r["gate"]]
    survived = sum(1 for r in alive if r["verdict"] == "PASS")
    errors = sum(1 for r in alive if r["verdict"] == "ERROR")
    print(f"judge: {len(alive)} read, {survived} passed, {len(alive) - survived - errors} killed, {errors} unanswered")
    print(f"stamp: {gate.stamp_path(path)}")
    return 0 if survived else 1


def stamp_cmd(path, argv):
    res = gate_or_die(path)
    src = argv[argv.index("--json") + 1] if "--json" in argv else str(out_path(path))
    raw = Path(src).read_text() if Path(src).exists() else src
    try:
        arr = json.loads(raw)
    except Exception:
        import re
        m = re.search(r"\[.*\]", raw, re.S)
        if not m:
            print("stamp: the reader's output is not a JSON array", file=sys.stderr); return 4
        arr = json.loads(m.group(0))
    answers = {}
    for j in arr:
        try:
            answers[int(j.get("n"))] = j
        except Exception:
            continue
    return write_stamp(path, res, answers, "in-session agent")


def headless_cmd(path, argv):
    from coldread import headless, parse_json, MODEL
    res = gate_or_die(path)
    alive = [h for h in res["hooks"] if not h["fails"]]
    qs, last, shape = questions(res["judge_rules"])
    shape.pop("n", None)
    base = PROMPT.read_text().replace("{READER}", res["header"]["reader"]).replace("{QUESTIONS}", qs) \
        .replace("{LAST}", str(last)).replace("{SHAPE}", json.dumps(shape, ensure_ascii=False))
    workers = int(argv[argv.index("--workers") + 1]) if "--workers" in argv else 4

    def ask(h):
        p = base.replace("{HOOK}", h["text"].replace('"', "'"))
        for _ in range(2):
            out, err = headless(p, timeout=240)
            if err and ("unavailable" in err or "not found" in err or "not logged in" in err):
                return None, "FATAL " + err
            if out:
                try:
                    j = parse_json(out); j["n"] = h["n"]; return j, None
                except Exception as e:
                    err = f"bad JSON: {e}"
        return None, err

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(ask, alive))
    fatal = [e for _, e in results if e and e.startswith("FATAL")]
    if fatal:
        print(fatal[0][6:], file=sys.stderr)
        print("no stamp. Use the no-login route: python3 tools/hooks/judge.py prompt " + path, file=sys.stderr); return 4
    answers = {h["n"]: j for h, (j, _) in zip(alive, results)}
    return write_stamp(path, res, answers, "headless " + MODEL, round(time.time() - t0))


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    cmd, path = argv[0], argv[1]
    if cmd == "prompt":
        return write_prompt(path)
    if cmd == "stamp":
        return stamp_cmd(path, argv[2:])
    if cmd == "nojudge":
        res = gate_or_die(path)
        if res["judge_rules"]:
            print("nojudge: judge rules are still active in the lane json; retire them first", file=sys.stderr); return 2
        return write_stamp(path, res, {}, "gate only, judge off (Ryan 10-29)")
    if cmd == "headless":
        return headless_cmd(path, argv[2:])
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
