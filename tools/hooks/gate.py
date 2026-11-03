#!/usr/bin/env python3
"""hook-writer gate: the mechanical half of Ryan's hook rules.

Rules live in tools/hooks/rules/<lane>.json as data. This script reads them; it never contains a rule.

  python3 tools/hooks/gate.py check  <hooks.md> [--json]   per-hook PASS/FAIL against the check rules
  python3 tools/hooks/gate.py report <hooks.md>            the Ryan-facing output: plain numbered hooks, star kept (needs a fresh judge stamp);
                                                           the counts line goes to <hooks.md>.report.txt, never the chat
  python3 tools/hooks/gate.py status <hooks.md>            0 fresh PASS stamp, 1 nothing survived, 3 missing/stale
  python3 tools/hooks/gate.py keep   <hooks.md> 3 5        append hooks 3 and 5 to offers/<slug>/ads/hooks/KEPT.md

Hooks file:
  ---
  offer: cloud9
  lane: short-cold
  round: 1
  angle: labs
  reader: woman, 62, wine every night, ALT flagged last month
  sources: none           (or full paths from the workspace root, semicolon separated: offers/<slug>/LANGUAGE.md; offers/<slug>/OFFER.md)
  ---
  ## Heartbreaking       (optional category line; required when the lane has a 'categories' rule)
  1. * Hook text          (* = the writer's holy-shit pick)
  2. Hook text

Exit codes: 0 ok, 1 fails, 2 structure or rules error, 3 stamp missing or stale.
"""
import hashlib, json, re, sys, time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent.parent
RULES_DIR = HERE / "rules"
sys.path.insert(0, str(WS / "tools" / "copygate"))
try:
    from coldread import language as _language
except Exception:  # copygate missing: no Never list, still runs
    _language = None

HEADER_FIELDS = ["offer", "lane", "round", "angle", "reader", "sources"]
FORBIDDEN_SOURCES = re.compile(r"strategist-ads|hook-laws|hook-bank|hook-bot|poe|memory|check_hooks", re.I)
SOURCES_FORMAT = ("\n  expected: sources: offers/<slug>/LANGUAGE.md; offers/<slug>/OFFER.md"
                  "\n  (full paths from the workspace root, semicolon separated, no prose, no parentheses, or exactly 'none')"
                  "  (dreaming 2026-11-02, sessions 10-29_9bbc526f, 10-29_37715be0, 10-30_b1ae4676)")
HOOK_LINE = re.compile(r"^\s*(\d+)[.)]\s*(\*?)\s*(.*\S)\s*$")
CATEGORY_LINE = re.compile(r"^\s*##\s+(.+?)\s*$")
ABBREV = re.compile(r"\b(Dr|Mr|Mrs|Ms|St|vs|Jr|Sr|a\.m|p\.m|No)$", re.I)


class GateError(Exception):
    pass


# ---------- parsing ----------

def parse(text):
    """-> (header dict, [{n, star, text}])"""
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        raise GateError("missing --- header block (offer, lane, round, angle, reader, sources)")
    header = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            header[k.strip().lower()] = v.strip()
    missing = [f for f in HEADER_FIELDS if not header.get(f)]
    if missing:
        raise GateError("header missing: " + ", ".join(missing))
    src = header["sources"]
    if src.lower() != "none":
        if FORBIDDEN_SOURCES.search(src):
            raise GateError("sources names a file this skill may not read: " + src + SOURCES_FORMAT)
        for s in re.split(r"[;,\s]+", src):
            if s and not s.startswith("offers/"):
                raise GateError("sources must be 'none' or paths under offers/, got: " + s + SOURCES_FORMAT)
    hooks = []
    category = None
    for line in m.group(2).split("\n"):
        cm = CATEGORY_LINE.match(line)
        if cm:
            category = cm.group(1).strip()
            continue
        mm = HOOK_LINE.match(line)
        if not mm:
            continue
        t = mm.group(3).strip()
        star = bool(mm.group(2))
        if t.endswith("*"):
            star, t = True, t[:-1].rstrip()
        hooks.append({"n": int(mm.group(1)), "star": star, "text": t, "category": category})
    if not hooks:
        raise GateError("no numbered hooks found (write them as '1. Hook text')")
    return header, hooks


def load_rules(lane):
    fp = RULES_DIR / f"{lane}.json"
    if not fp.exists():
        raise GateError(f"no rules file for lane '{lane}' (expected {fp})")
    d = json.loads(fp.read_text())
    return d, hashlib.sha256(fp.read_bytes()).hexdigest()


def rules_of(rules, kind):
    return [r for r in rules["rules"] if r.get("type") == kind and r.get("status", "active") == "active"]


# ---------- primitives ----------

def word_count(t):
    return len([w for w in t.split() if re.search(r"[A-Za-z0-9]", w)])


def mid_sentence_break(t):
    """True if a . ! or ? ends a sentence before the last word (ellipses and abbreviations excluded)."""
    for m in re.finditer(r"(?<!\.)[.!?](?!\.)(?=[\"'”’)]*\s+\S)", t):
        before = t[:m.start()]
        if m.group(0) == "." and ABBREV.search(before):
            continue
        return True
    return False


def core_words(offer):
    """## Core words section of offers/<slug>/LANGUAGE.md -> list of words/phrases (comma-split)."""
    fp = WS / "offers" / offer / "LANGUAGE.md"
    if not fp.exists():
        return []
    out, sec = [], False
    for l in fp.read_text(errors="ignore").split("\n"):
        t = l.strip()
        if t.lower().startswith("## core"):
            sec = True; continue
        if t.startswith("## "):
            sec = False; continue
        if sec and t.startswith(("-", "*")):
            for w in re.split(r"\s*,\s*", t.lstrip("-* ").strip()):
                w = re.sub(r"\s*\([^)]*\)", "", w).strip().strip('"“”')
                if w:
                    out.append(w)
    return out


def norm_hook(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()


def earlier_rounds(header):
    """{normalized text, first-five-words key} from every earlier round of this angle (offers/<slug>/ads/hooks/<angle>-r<M>.md, M < round)."""
    exact, openers = set(), set()
    try:
        cur = int(header.get("round", "0"))
    except ValueError:
        return exact, openers
    d = WS / "offers" / header["offer"] / "ads" / "hooks"
    if not d.exists():
        return exact, openers
    for fp in d.glob(f"{header['angle']}-r*.md"):
        m = re.search(r"-r(\d+)\.md$", fp.name)
        if not m or int(m.group(1)) >= cur:
            continue
        try:
            _, hooks = parse(fp.read_text(errors="ignore"))
        except GateError:
            continue
        for h in hooks:
            n = norm_hook(h["text"])
            exact.add(n)
            openers.add(" ".join(n.split()[:5]))
    return exact, openers


def carried_over(header, hooks):
    """Hooks that repeat an earlier round of this angle: same line, or the same first five words (a template).
    Ryan 10-28_66850cc4: 'you keep doing the same hooks over and over again, trying to improve them instead of just doing new hooks.'
    Ryan 10-29_ccab9cfb: 'Why are you doing vet stunned every single time?' (dreaming 2026-11-02)"""
    exact, openers = earlier_rounds(header)
    out = []
    for h in hooks:
        n = norm_hook(h["text"])
        if n in exact:
            out.append((h, "same line as an earlier round"))
        elif len(n.split()) >= 5 and " ".join(n.split()[:5]) in openers:
            out.append((h, "same first five words as an earlier round (a template)"))
    return out


def require_patterns(spec, offer):
    if spec.get("from") == "language.core":
        words = core_words(offer)
        if not words:
            raise GateError(f"rule needs '## Core words' in offers/{offer}/LANGUAGE.md (what the offer is about)")
        return [re.compile(r"\b" + re.escape(w) + r"\b", re.I) for w in words]
    return [re.compile(spec["regex"], re.I)]


def forbid_patterns(spec, lang):
    pats = []
    if spec.get("regex"):
        pats.append((re.compile(spec["regex"], re.I), "dash"))
    if spec.get("from") == "language.never" and lang:
        for item in lang.get("never", []):
            # LANGUAGE.md lists several words per line ("hangover, hangover cure, hangover pill"); each one is banned
            for w in re.split(r"\s*,\s*", item):
                w = re.sub(r"\s*\([^)]*\)", "", w).strip().strip('"“”')
                if w and len(w.split()) <= 4:
                    pats.append((re.compile(r"\b" + re.escape(w) + r"\b", re.I), w))
    return pats


# ---------- check ----------

def check(text, path=None):
    header, hooks = parse(text)
    rules, rules_sha = load_rules(header["lane"])
    lang = None
    if _language:
        try:  # always keyed on the header's offer, so fixtures outside offers/ still get the Never list
            lang = _language(str(WS / "offers" / header["offer"] / "LANGUAGE.md"))
        except Exception:
            lang = None
    checks = rules_of(rules, "check")
    set_spec = None
    set_max = []
    cat_spec = None
    for r in checks:
        spec = r["spec"]
        prim = spec["primitive"]
        if prim == "set":
            set_spec = (r["id"], spec)
            continue
        if prim == "set_max":
            set_max.append((r["id"], spec))
            continue
        if prim == "new_lines":
            for h, why in carried_over(header, hooks):
                h.setdefault("fails", []); h.setdefault("notes", [])
                h["fails"].append(r["id"]); h["notes"].append(f"{r['id']}: {why}")
            continue
        if prim == "categories":
            if not any(h.get("category") for h in hooks):
                continue  # an unbatched file (no '## Category' lines) is not gated by this rule; the report says so
            cat_spec = (r["id"], spec)
            names = {n.lower(): n for n in spec["names"]}
            for h in hooks:
                h.setdefault("fails", []); h.setdefault("notes", [])
                c = (h.get("category") or "").lower()
                if c in names:
                    h["category"] = names[c]
                else:
                    h["fails"].append(r["id"])
                    h["notes"].append(f"{r['id']}: " + (f"category '{h['category']}' is not one of {', '.join(spec['names'])}" if h.get("category") else "no '## Category' line above it"))
            continue
        pats = forbid_patterns(spec, lang) if prim == "forbid" else None
        reqs = require_patterns(spec, header["offer"]) if prim == "require" else None
        for h in hooks:
            h.setdefault("fails", [])
            h.setdefault("notes", [])
            t = h["text"]
            if prim == "words":
                n = word_count(t)
                if n < spec.get("min", 0) or n > spec.get("max", 10 ** 6):
                    h["fails"].append(r["id"]); h["notes"].append(f"{r['id']}: {n} words")
            elif prim == "one_sentence":
                if mid_sentence_break(t):
                    h["fails"].append(r["id"]); h["notes"].append(f"{r['id']}: sentence break mid-hook")
            elif prim == "forbid":
                for pat, label in pats:
                    if pat.search(t):
                        h["fails"].append(r["id"]); h["notes"].append(f"{r['id']}: '{label}'")
                        break
            elif prim == "require":
                if not any(p.search(t) for p in reqs):
                    h["fails"].append(r["id"]); h["notes"].append(f"{r['id']}: no {spec.get('what', 'required word')}")
            else:
                raise GateError(f"rule {r['id']} uses unknown primitive '{prim}'")
    for h in hooks:
        h.setdefault("fails", []); h.setdefault("notes", [])
    set_fails, set_warns = [], []
    if set_spec:
        sid, spec = set_spec
        if len(hooks) < spec.get("min_drafted", 0):
            set_fails.append(f"{sid}: {len(hooks)} drafted, rule says draft {spec['min_drafted']}+")
    if cat_spec:
        sid, spec = cat_spec
        per = Counter(h.get("category") for h in hooks)
        short = [f"{n} {per.get(n, 0)}" for n in spec["names"] if per.get(n, 0) < spec["per_category"]]
        if short:
            set_fails.append(f"{sid}: rule says {spec['per_category']} per category, short: " + ", ".join(short))
    for sid, spec in set_max:
        pat = re.compile(spec["regex"], re.I)
        n = sum(1 for h in hooks if pat.search(h["text"]))
        allowed = -(-len(hooks) * spec["max_per_10"] // 10)  # ceil
        if n > allowed:
            set_fails.append(f"{sid}: {n} of {len(hooks)} {spec.get('what', 'match')}, rule allows {spec['max_per_10']} in 10 ({allowed} here)")
    return {"header": header, "hooks": hooks, "rules_sha": rules_sha, "set_spec": set_spec, "cat_spec": cat_spec,
            "carried": len(carried_over(header, hooks)),
            "set_fails": set_fails, "set_warns": set_warns, "judge_rules": rules_of(rules, "judge"),
            "taste_rules": rules_of(rules, "taste")}


def print_check(res):
    for h in res["hooks"]:
        if h["fails"]:
            print(f"{h['n']}. FAIL {' '.join(h['fails'])}   ({'; '.join(h['notes'])})")
        else:
            print(f"{h['n']}. PASS")
    for s in res["set_fails"]:
        print("SET FAIL " + s)
    alive = sum(1 for h in res["hooks"] if not h["fails"])
    print(f"gate: {len(res['hooks'])} drafted, {alive} pass, {len(res['hooks']) - alive} killed")


# ---------- stamp ----------

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stamp_path(path):
    return Path(str(path) + ".hookjudge.json")


def read_stamp(path):
    sp = stamp_path(path)
    if not sp.exists():
        return None, "no stamp (run judge.py)"
    try:
        st = json.loads(sp.read_text())
    except Exception:
        return None, "stamp unreadable"
    if st.get("sha256") != sha(path):
        return st, "stale: the hooks file changed since the judge read it (run judge.py again)"
    try:
        _, rs = load_rules(st.get("lane", ""))
    except GateError as e:
        return st, str(e)
    if st.get("rules_sha") != rs:
        return st, "stale: the rules changed since the judge read it (run judge.py again)"
    return st, None


def status(path):
    st, why = read_stamp(path)
    if why:
        print(why); return 3
    if not any(h.get("verdict") == "PASS" for h in st.get("hooks", [])):
        print("stamp ok, nothing survived"); return 1
    print("fresh PASS stamp"); return 0


# ---------- report ----------

def survivors(st):
    alive = [h for h in st["hooks"] if h.get("verdict") == "PASS"]
    return sorted(alive, key=lambda h: (not h.get("star"), h["n"]))


def report(path):
    st, why = read_stamp(path)
    if why:
        print(why, file=sys.stderr); return 3
    hd = st["header"]
    gate_kills = Counter(); judge_kills = Counter(); errors = 0
    for h in st["hooks"]:
        if h.get("verdict") == "ERROR":
            errors += 1
        for k in h.get("gate", []):
            gate_kills[k] += 1
        if not h.get("gate"):
            for k in h.get("killed_by", []):
                judge_kills[k] += 1
    g_n = sum(1 for h in st["hooks"] if h.get("gate"))
    j_n = sum(1 for h in st["hooks"] if not h.get("gate") and h.get("verdict") == "FAIL")
    alive = survivors(st)
    max_shown = (st.get("set_spec") or {}).get("max_shown", 10)
    min_stars = (st.get("set_spec") or {}).get("min_stars", 0)
    cat = st.get("cat_spec") or None
    if cat:  # SC-11: batched by category, per_category shown in each, in the rule's order
        order = {n: i for i, n in enumerate(cat["names"])}
        alive = sorted(alive, key=lambda h: (order.get(h.get("category"), 99), not h.get("star"), h["n"]))
        max_shown = cat["per_category"] * len(cat["names"])
    # set_max rules cap what is SHOWN too (e.g. at most 3 of 10 with an ellipsis); the rest stay in the file
    caps = []
    has_cat_rule = False
    try:
        rules, _ = load_rules(st.get("lane", ""))
        caps = [(re.compile(r["spec"]["regex"], re.I), r["spec"]["max_per_10"]) for r in rules_of(rules, "check")
                if r["spec"].get("primitive") == "set_max"]
        has_cat_rule = any(r["spec"].get("primitive") == "categories" for r in rules_of(rules, "check"))
    except GateError:
        pass
    shown, counts = [], [0] * len(caps)
    per_cat = Counter()
    for h in alive:
        if len(shown) >= max_shown:
            break
        if cat and per_cat[h.get("category")] >= cat["per_category"]:
            continue
        hit = [i for i, (pat, _) in enumerate(caps) if pat.search(h["text"])]
        if any(counts[i] >= caps[i][1] * max_shown // 10 for i in hit):
            continue
        for i in hit:
            counts[i] += 1
        per_cat[h.get("category")] += 1
        shown.append(h)

    def fmt(c):
        return ", ".join(f"{k} x{v}" for k, v in c.most_common()) or "none"

    line = (f"{hd['offer']} / {hd['lane']} / r{hd['round']} {hd['angle']}: {len(st['hooks'])} drafted, "
            f"{g_n} killed by gate ({fmt(gate_kills)}), {j_n} killed by judge ({fmt(judge_kills)}), "
            f"{len(shown)} shown. * = holy shit.")
    extras = []
    if has_cat_rule and not cat:
        extras.append("unbatched: no '## Category' lines (SC-11 wants 5 per category)")
    if len(alive) > len(shown):
        extras.append(f"+{len(alive) - len(shown)} more passed, in the file")
    stars = sum(1 for h in shown if h.get("star"))
    if min_stars and stars < min_stars:
        extras.append(f"only {stars} starred, rule wants {min_stars}")
    if errors:
        extras.append(f"{errors} not judged (reader error)")
    if st.get("set_fails"):
        extras.append("; ".join(st["set_fails"]))
    if extras:
        line += " (" + "; ".join(extras) + ")"
    # counts go in the file, not the chat (Ryan 10-30_016dc322: "the formatting here is all weird"; dreaming 2026-11-02).
    # The reply is the plain numbered list below, star kept. judge.py is also run from the hooks file, so recount carry-over here.
    try:
        _, cur_hooks = parse(Path(path).read_text(errors="ignore"))
        carried = len(carried_over(hd, cur_hooks))
    except Exception:
        carried = st.get("carried", "?")
    counts_path = Path(str(path) + ".report.txt")
    counts_path.write_text(line + f"\n{carried} carried over from earlier rounds of this angle (0 is the rule).\n")
    last_cat = None
    for h in shown:
        if cat and h.get("category") != last_cat:
            last_cat = h.get("category")
            print(f"## {last_cat}")
        print(f"{h['n']}. {'* ' if h.get('star') else ''}{h['text']}")
    return 0 if shown else 1


# ---------- keep ----------

def keep(path, nums):
    text = Path(path).read_text()
    header, hooks = parse(text)
    by_n = {h["n"]: h for h in hooks}
    kept = WS / "offers" / header["offer"] / "ads" / "hooks" / "KEPT.md"
    kept.parent.mkdir(parents=True, exist_ok=True)
    if not kept.exists():
        kept.write_text(f"# {header['offer']}: hooks Ryan kept (never gated, the writer's examples for this offer)\n\n")
    day = time.strftime("%Y-%m-%d")
    out = []
    for n in nums:
        if n not in by_n:
            print(f"no hook #{n} in {path}", file=sys.stderr); return 2
        c = f" ({by_n[n]['category']})" if by_n[n].get("category") else ""
        out.append(f"- [{header['lane']}] {day} {header['angle']}-r{header['round']} #{n}{c}: {by_n[n]['text']}")
    with open(kept, "a") as f:
        f.write("\n".join(out) + "\n")
    print(f"kept {len(out)} -> {kept.relative_to(WS)}")
    return 0


# ---------- main ----------

def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    cmd, args = argv[0], argv[1:]
    try:
        if cmd == "check":
            path = args[0]
            res = check(Path(path).read_text(), path)
            if "--json" in args:
                print(json.dumps(res, indent=1))
            else:
                print_check(res)
            bad = any(h["fails"] for h in res["hooks"]) or res["set_fails"]
            return 1 if bad else 0
        if cmd == "report":
            return report(args[0])
        if cmd == "status":
            return status(args[0])
        if cmd == "keep":
            return keep(args[0], [int(x) for x in args[1:]])
    except GateError as e:
        print("gate: " + str(e), file=sys.stderr); return 2
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
