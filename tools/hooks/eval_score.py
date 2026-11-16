#!/usr/bin/env python3
"""eval_score.py <run_dir> [--label TEXT]: score a hook-writer eval run and add one row to tools/hooks/EVAL.md.

A run dir holds one hooks file per offer (written by a fresh agent under the skill, round 99, never in offers/).
For every hook: the gate's own check rules (gate.py check --json) plus the checks lifted from Ryan's most repeated notes:
  disease    a disease word (Ryan 10-06: "We absolutely cannot say cancer")
  stat       a percent or a study claim (no stats in hooks)
  narrows    the line opens by shrinking who it is for ("If your vet...", "If you take...")
  kept       repeats the first five words of a hook Ryan already locked in offers/<slug>/ads/hooks/KEPT.md
  dash       an em dash
A hook passes when the gate passes it and none of these fire. The number is passes / hooks shown, per offer and in total.
The stranger read (did you read it twice) is a separate step: judge_eval.py, when it exists.
"""
import sys, os, re, json, subprocess, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
EVAL_MD = os.path.join(HERE, "EVAL.md")
DISEASE = re.compile(r"\b(cancer|tumou?r|obes\w*|diabet\w*|dementia|alzheimer\w*|disease|diseased)\b", re.I)
STAT = re.compile(r"\d+(\.\d+)?\s?%|\bstud(y|ies)\b|\bpercent\b|\bresearch(ers)? (show|found|say)", re.I)
NARROWS = re.compile(r"^\s*(if (your|you|you're|he|she|they)\b|for (women|men|anyone|those) (who|over)\b|women over\b|men over\b)", re.I)
DASH = re.compile(r"—|–| -- ")
EXTRA = ["disease", "stat", "narrows", "kept", "dash"]


def first5(t):
    return " ".join(re.findall(r"[a-z']+", t.lower())[:5])


def kept_firsts(slug):
    p = os.path.join(WS, "offers", slug, "ads", "hooks", "KEPT.md")
    out = set()
    if os.path.exists(p):
        for l in open(p):
            m = re.search(r"#\d+:\s*(.+)$", l)
            if m:
                out.add(first5(m.group(1)))
    return out


def score_file(path):
    r = subprocess.run([sys.executable, os.path.join(HERE, "gate.py"), "check", path, "--json"], capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
    except Exception:
        return {"error": (r.stdout + r.stderr).strip()[:300], "hooks": []}
    slug = (data.get("header") or {}).get("offer") or os.path.basename(path)[:-3]
    kept = kept_firsts(slug)
    rows = []
    for h in data.get("hooks", []):
        t = h.get("text", "")
        extra = []
        if DISEASE.search(t): extra.append("disease")
        if STAT.search(t): extra.append("stat")
        if NARROWS.search(t): extra.append("narrows")
        if first5(t) in kept: extra.append("kept")
        if DASH.search(t): extra.append("dash")
        rows.append({"n": h.get("n"), "star": h.get("star"), "text": t, "gate_fails": h.get("fails", []), "extra": extra,
                     "pass": not h.get("fails") and not extra})
    return {"offer": slug, "hooks": rows}


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 1
    run = argv[1]
    label = argv[argv.index("--label") + 1] if "--label" in argv else os.path.basename(run.rstrip("/"))
    files = sorted(glob.glob(os.path.join(run, "*.md")))
    total = passed = 0
    per_offer, fail_counts = [], {}
    detail = []
    for f in files:
        s = score_file(f)
        if "error" in s:
            per_offer.append(f"{os.path.basename(f)}: ERROR {s['error']}"); continue
        n = len(s["hooks"]); p = sum(1 for h in s["hooks"] if h["pass"])
        total += n; passed += p
        per_offer.append(f"{s['offer']} {p}/{n}")
        for h in s["hooks"]:
            for k in h["gate_fails"] + h["extra"]:
                fail_counts[k] = fail_counts.get(k, 0) + 1
            if not h["pass"]:
                detail.append(f"  {s['offer']} #{h['n']}: {', '.join(h['gate_fails'] + h['extra'])}  | {h['text']}")
    pct = 100 * passed // max(total, 1)
    row = f"| {datetime.date.today().isoformat()} | {label} | **{passed}/{total} ({pct}%)** | {' · '.join(per_offer)} | " + \
          ", ".join(f"{k} {v}" for k, v in sorted(fail_counts.items(), key=lambda x: -x[1])) + " |"
    header = ("# hook-writer eval\n\nOne row per run. `pass` = the gate passed the hook and none of the extra checks fired "
              "(see `eval_score.py`). Rerun the same five inputs after every skill edit; keep the edit only if the number moves "
              "and nothing else got worse.\n\n| date | run | pass | per offer | what failed |\n|---|---|---|---|---|\n")
    old = open(EVAL_MD).read() if os.path.exists(EVAL_MD) else header
    if not old.startswith("# hook-writer eval"):
        old = header
    open(EVAL_MD, "w").write(old.rstrip("\n") + "\n" + row + "\n")
    json.dump({"run": run, "rows": per_offer, "passed": passed, "total": total, "fails": fail_counts},
              open(os.path.join(run, "score.json"), "w"), indent=1)
    print(row)
    print("\n".join(detail))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
