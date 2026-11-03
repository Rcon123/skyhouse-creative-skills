#!/usr/bin/env python3
"""copygate: the cold-read judge for copy that leaves this workspace. A tool, never a gate (Ryan, 10-30).

Built 2026-10-27 after the ProDenta escalation (a sentence a stranger could not parse and a surgery-table
hero went live after 17 graded versions; nobody read the page cold). The ship block was removed 10-30 at
Ryan's order ("get rid of this thing that stops you"). Two layers remain:

  check   <file>            mechanical floor: dashes, banned words (LANGUAGE.md "Never"), long sentences,
                            long paragraphs, reading grade. Runs automatically after every Write/Edit.
  judge   <file>            the cold read. DEFAULT (since 2026-11-02): prints the mechanical check and the brief
                            for a FRESH in-session Agent that reads the copy once as a stranger and writes the
                            verdict with `stamp`. Exit 4 = "spawn the reader now". `--headless` instead runs a
                            separate `claude -p` process (the true stranger); it needs `claude login` in a
                            terminal and has been logged out since 10-27.
  stamp   <file> --reader subagent --json <verdict json>
                            the fresh reader's verdict, written by the READER, never by the writer.
  status  <file>            is the stamp valid (PASS, copy unchanged since the read)?
  approve <file> --note ... Ryan's override from his own terminal (refuses without a TTY).
  text    <file>            print the extracted visible text (what the reader sees).

Scope (2026-11-02, dreaming pass): the check, the reader text and the stamp hash cover the COPY only.
  --from "MASTHEAD:"        copy starts at the first line containing this marker (builder notes above it are skipped)
  --section "<heading>"     copy is the markdown section under this heading (md) or from that line down (html)
  By default lines that are only a [bracketed builder tag] are skipped, inline [tags] are stripped, and the
  footer disclaimer block is skipped. --keep-tags / --keep-footer turn that off.
  The stamp records the scope and a hash of the scoped text, so a note added above the copy does not stale it.

Read cap (Ryan, 10-26 to 11-02): one read on new copy, fix the flags, at most one re-read, then ship with the
rest as notes. Never a third read. Never on unchanged copy, a CSS or image swap, briefs, task text, locked hooks
or held-reveal headlines.

Exit codes: 0 pass, 1 fail (flags), 3 stamp missing/stale, 4 reader not run here (spawn the Agent), 2 usage.
"""
import hashlib, html as htmlmod, json, os, re, subprocess, sys, time, glob
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent.parent
PROMPT = HERE / "READER-PROMPT.md"
MAX_WORDS_FAIL = 25
MAX_WORDS_WARN = 18
MAX_PARA_CHARS = 260          # about three phone lines at 390px
GRADE_WARN = 6.0
MODEL = os.environ.get("COPYGATE_MODEL", "sonnet")

NOTE_LABELS = re.compile(r"^(Images?|Lander|Cast|Source|Sources|Note|Notes|Ryan|File|DB|Doc|ClickUp|Status|Hooks? locked|Headlines? LOCKED)\b[^:]{0,40}:", re.I)
LABEL = re.compile(r"^(H\d+|AT\d+|HL\d+|HOOK\s*\d*|HEADLINE\s*\d*|BODY|P\.?S\.?)\s*:\s*", re.I)
TAG_LINE = re.compile(r"^(\[[^\]]*\]\s*)+$")                 # a line that is only [builder tags]
TAG_INLINE = re.compile(r"\[[^\]\n]*\](?!\()")               # [tag] but not a markdown link [text](url)
DISCLAIMER = re.compile(r"^\W*(these statements have not been evaluated|this (site|website|page) is not (a )?part of|"
                        r"results (may|can|will) vary|disclaimer\b|copyright\b|©|all rights reserved|marketing disclosure|"
                        r"advertorial\s*$|this is an advertisement|terms (of|and) |privacy policy|the information (on|provided|in) this)", re.I)


def scope_of(args):
    """Scope options from parsed CLI args (or a stamp's recorded scope)."""
    return {"from": args.get("--from") or None, "section": args.get("--section") or None,
            "tags": "--keep-tags" not in args, "footer": "--keep-footer" not in args}


DEFAULT_SCOPE = scope_of({})


# ---------- text extraction ----------
def _apply_scope(lines, scope, md=False):
    """Trim a list of visible lines to the copy section. `lines` are already stripped, empty lines kept for md."""
    scope = scope or DEFAULT_SCOPE
    start, end = 0, len(lines)
    if scope.get("from"):
        m = scope["from"].lower()
        for i, l in enumerate(lines):
            if m in l.lower():
                start = i
                lines = list(lines)
                lines[i] = re.sub(re.escape(scope["from"]), "", l, count=1, flags=re.I).strip()
                break
    elif scope.get("section"):
        want = re.sub(r"^#+\s*", "", scope["section"]).strip().lower()
        for i, l in enumerate(lines):
            bare = re.sub(r"^#+\s*", "", l).strip().lower()
            if bare and (bare == want or want in bare):
                start = i + 1
                if md:
                    level = len(l) - len(l.lstrip("#")) if l.startswith("#") else 0
                    for k in range(i + 1, len(lines)):
                        lk = lines[k]
                        if lk.startswith("#") and (len(lk) - len(lk.lstrip("#"))) <= max(level, 1):
                            end = k
                            break
                break
    out = []
    for l in lines[start:end]:
        if scope.get("tags", True):
            if TAG_LINE.match(l):
                continue
            l = re.sub(r"\s{2,}", " ", TAG_INLINE.sub("", l)).strip()
        if scope.get("footer", True) and DISCLAIMER.match(l):
            continue
        out.append(l)
    return out


def extract(path, scope=None):
    """Returns (text, alts). text = what a reader sees, one block per line. alts = image descriptions in page order."""
    scope = scope or DEFAULT_SCOPE
    raw = Path(path).read_text(errors="ignore")
    if path.lower().endswith((".html", ".htm")):
        s = re.sub(r"<(script|style|noscript)\b.*?</\1>", " ", raw, flags=re.S | re.I)
        s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
        if scope.get("footer", True):
            s = re.sub(r"<footer\b.*?</footer>", " ", s, flags=re.S | re.I)
            s = re.sub(r"<(div|p|section|small)\b[^>]*\b(class|id)=\"[^\"]*disclaim[^\"]*\"[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
        alts = [htmlmod.unescape(a) for a in re.findall(r"<img\b[^>]*\balt=\"([^\"]*)\"", s, flags=re.I)]
        s = re.sub(r"<\s*(br|/p|/div|/h[1-6]|/li|/blockquote|/figcaption|/tr|/section|/article|/header|/footer|p|div|h[1-6]|li)\b[^>]*>", "\n", s, flags=re.I)
        s = re.sub(r"<[^>]+>", "", s)
        s = htmlmod.unescape(s)
        lines = [re.sub(r"[ \t ]+", " ", l).strip() for l in s.split("\n")]
        lines = _apply_scope([l for l in lines if l], scope)
        return "\n".join(l for l in lines if l), alts
    lines = _apply_scope([l.strip() for l in raw.split("\n")], scope, md=True)
    out = []
    for t in lines:
        if not t or t.startswith(("#", ">", "<!--", "|", "```")) or NOTE_LABELS.match(t):
            continue
        t = LABEL.sub("", t)
        t = re.sub(r"\*\*|__|^\s*[-*]\s+", "", t)
        if t:
            out.append(t)
    return "\n".join(out), []


def sentences(text):
    out = []
    for line in text.split("\n"):
        parts = re.split(r"(?<=[.!?])\s+(?=[\"'(\[A-Z0-9#$])|(?<=\.\.\.)\s+", line)
        out += [p.strip() for p in parts if p and p.strip()]
    return out


# ---------- readability ----------
def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def fk_grade(sents):
    words = [w for s in sents for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", s)]
    if not words or not sents:
        return 0.0
    syl = sum(syllables(w) for w in words)
    return round(0.39 * len(words) / len(sents) + 11.8 * syl / len(words) - 15.59, 1)


# ---------- language bank ----------
def offer_of(path):
    p = Path(path).resolve()
    try:
        rel = p.relative_to(WS / "offers")
        return rel.parts[0]
    except Exception:
        return None


def language(path):
    """{'their': [...], 'never': [...]} from offers/<slug>/LANGUAGE.md (+ tools/copygate/NEVER.md)."""
    their, never = [], []

    def read(fp):
        if not fp.exists():
            return
        sec = None
        for l in fp.read_text(errors="ignore").split("\n"):
            t = l.strip()
            if t.lower().startswith("## their"):
                sec = "their"; continue
            if t.lower().startswith("## never"):
                sec = "never"; continue
            if t.startswith("## "):
                sec = None; continue
            if sec and t.startswith(("-", "*")):
                item = t.lstrip("-* ").strip()
                item = re.sub(r"\s*\([^)]*\)\s*$", "", item).strip().strip('"“”')
                if item:
                    (their if sec == "their" else never).append(item)
    read(HERE / "NEVER.md")
    slug = offer_of(path)
    if slug:
        read(WS / "offers" / slug / "LANGUAGE.md")
    return {"their": their, "never": never, "offer": slug}


# ---------- mechanical check ----------
QUALIFIER_SLICE = re.compile(r"^\W*if\s+(your\s+(vet|doctor|dentist|dr\.?)|you\s+take|you(?:'ve| have)\s+been\s+told)\b", re.I)
CHOPPY_RUN = 3          # this many short sentences in a row reads as choppy
CHOPPY_WORDS = 6        # a sentence under this many words counts as short


def style_warns(text, sents):
    """Warns only, never fails (dreaming 2026-11-02, sessions 10-30_d8dfe031, 10-30_c21efef8, 10-29_ccab9cfb, 10-26_601f85f7).
    (1) a qualifier line that starts 'If your vet / If your doctor / If you take / If you've been told' names a slice of
    the audience; Ryan's rule is to qualify to the widest true group. (2) three or more sentences under 6 words in a row
    read as choppy; the band is 8 to 22 words, mostly 12 to 18."""
    out = []
    for line in text.split("\n"):
        if QUALIFIER_SLICE.match(line.strip()):
            out.append(f"qualifier names a slice; widest true group? \"{line.strip()[:80]}\"")
    run = []
    for s in sents + [""]:
        if s and len(s.split()) < CHOPPY_WORDS:
            run.append(s)
            continue
        if len(run) >= CHOPPY_RUN:
            out.append(f"{len(run)} sentences under {CHOPPY_WORDS} words in a row (choppy; aim 8 to 22 words, mostly 12 to 18): \"{' '.join(run)[:110]}\"")
        run = []
    return out


def check(path, scope=None):
    scope = scope or DEFAULT_SCOPE
    text, alts = extract(path, scope)
    sents = sentences(text)
    lang = language(path)
    fails, warns = [], []
    if re.search(r"[—–]|&mdash;|&ndash;|&#8212;|&#8211;", text + "\n" + "\n".join(alts)):
        fails.append("em/en dash present")
    for nv in lang["never"]:
        pat = r"\b" + re.escape(nv) + r"\b" if re.match(r"^\w", nv) else re.escape(nv)
        hits = re.findall(pat, text, flags=re.I)
        if hits:
            fails.append(f"banned word for this offer: \"{nv}\" ({len(hits)}x). See offers/{lang['offer']}/LANGUAGE.md")
    for s in sents:
        n = len(s.split())
        if n > MAX_WORDS_FAIL:
            fails.append(f"{n}-word sentence: \"{s[:110]}…\"")
        elif n > MAX_WORDS_WARN:
            warns.append(f"{n}-word sentence: \"{s[:110]}…\"")
    for line in text.split("\n"):
        if len(line) > MAX_PARA_CHARS:
            warns.append(f"paragraph over ~3 phone lines ({len(line)} chars): \"{line[:80]}…\"")
    warns += style_warns(text, sents)
    grade = fk_grade(sents)
    if grade > GRADE_WARN:
        warns.append(f"reading grade {grade} (aim under {GRADE_WARN:.0f})")
    return {"file": str(path), "sentences": len(sents), "words": sum(len(s.split()) for s in sents),
            "grade": grade, "fails": fails, "warns": warns, "alts": alts, "language": lang, "scope": scope,
            "text_sha256": hashlib.sha256(text.encode()).hexdigest()}


def scope_line(scope):
    bits = []
    if scope.get("from"):
        bits.append(f"from \"{scope['from']}\"")
    if scope.get("section"):
        bits.append(f"section \"{scope['section']}\"")
    if scope.get("tags", True):
        bits.append("[tags] skipped")
    if scope.get("footer", True):
        bits.append("footer skipped")
    return ", ".join(bits) or "whole file"


def print_check(r):
    print(f"copygate check: {r['file']}  (scope: {scope_line(r['scope'])})")
    print(f"  {r['sentences']} sentences, {r['words']} words, reading grade {r['grade']}")
    for f in r["fails"]:
        print("  FAIL:", f)
    for w in r["warns"]:
        print("  warn:", w)
    if not r["fails"] and not r["warns"]:
        print("  clean on the mechanical floor")
    print("  mechanical", "FAIL" if r["fails"] else "ok", "(the fresh-reader judge is the real read; it is a tool, never a block)")


# ---------- stamp ----------
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stamp_path(path):
    return Path(str(path) + ".coldread.json")


def read_stamp(path):
    sp = stamp_path(path)
    if not sp.exists():
        return None, "no stamp"
    try:
        st = json.loads(sp.read_text())
    except Exception:
        return None, "stamp unreadable"
    if st.get("sha256") != sha(path):
        # 11-02: a note above the copy, a CSS change or an image swap does not stale the read; only the copy does.
        same_copy = False
        if st.get("text_sha256"):
            try:
                same_copy = check(path, st.get("scope") or DEFAULT_SCOPE)["text_sha256"] == st["text_sha256"]
            except Exception:
                same_copy = False
        if not same_copy:
            return st, "stale (copy changed since the cold read)"
        if st.get("verdict") != "PASS":
            return st, "verdict FAIL"
        return st, "valid (file changed, copy section unchanged)"
    if st.get("verdict") != "PASS":
        return st, "verdict FAIL"
    return st, "valid"


def write_stamp(path, verdict, reader, model, checkres, judge, note=""):
    st = {"file": str(Path(path).resolve()), "sha256": sha(path), "text_sha256": checkres.get("text_sha256"),
          "scope": checkres.get("scope", DEFAULT_SCOPE), "verdict": verdict, "reader": reader, "model": model,
          "time": time.strftime("%Y-%m-%d %H:%M:%S"), "grade": checkres["grade"], "mechanical_fails": checkres["fails"],
          "mechanical_warns": checkres["warns"], "judge": judge, "note": note}
    stamp_path(path).write_text(json.dumps(st, indent=1, ensure_ascii=False))
    return st


# ---------- the fresh reader ----------
def find_claude():
    cands = [os.environ.get("COPYGATE_CLAUDE", "")]
    cands += sorted(glob.glob(os.path.expanduser("~/Library/Application Support/Claude/claude-code/*/*/claude.app/Contents/MacOS/claude")), reverse=True)
    cands += ["/opt/homebrew/bin/claude", "/usr/local/bin/claude", os.path.expanduser("~/.local/bin/claude")]
    for c in cands:
        if c and os.access(c, os.X_OK):
            return c
    return None


def build_prompt(path, text, alts, lang):
    p = [PROMPT.read_text(), "\n\n===== THE PAGE (read once, top to bottom) =====\n", text]
    if alts:
        p.append("\n\n===== IMAGE DESCRIPTIONS, in page order (the first is above the fold) =====\n" + "\n".join(f"- {a}" for a in alts))
    if lang["their"]:
        p.append("\n\n===== THE BRAND'S OWN WORDS (how they say it) =====\n" + "\n".join(f"- {w}" for w in lang["their"]))
    p.append("\n\nReturn the JSON object only.")
    return "".join(p)


def parse_json(s):
    m = re.search(r"\{.*\}", s, flags=re.S)
    if not m:
        raise ValueError("no JSON in reader output")
    return json.loads(m.group(0))


def headless(prompt, timeout=600):
    exe = find_claude()
    if not exe:
        return None, "claude CLI not found"
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        r = subprocess.run([exe, "-p", "--model", MODEL, "--output-format", "json", "--no-session-persistence",
                            "--max-thinking-tokens", "2048",
                            "--disallowedTools", "Bash,Edit,Write,Read,Glob,Grep,WebFetch,WebSearch,Agent,Task"],
                           input=prompt, capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None, f"reader timed out after {timeout}s"
    out = r.stdout.strip()
    try:
        d = json.loads(out)
        res = d.get("result", "")
        if d.get("is_error") or "Failed to authenticate" in str(res) or "OAuth" in str(res):
            return None, f"headless reader unavailable: {str(res)[:160]}"
        return res, None
    except Exception:
        if "authenticate" in out or "OAuth" in out or "authenticate" in r.stderr:
            return None, "headless reader unavailable: claude CLI is not logged in (run `claude login` in a terminal)"
        return (out or None), (None if out else f"empty reader output (exit {r.returncode}): {r.stderr[:160]}")


def image_ok(problem):
    """11-02: a reader 'problem' that begins with 'none' ('none, a normal kitchen') is no flag."""
    p = (problem or "none").strip().lower()
    return p == "" or p.startswith("none") or p == "no" or re.match(r"^no[ ,.;:]", p) is not None


def verdict_from(judge, checkres):
    flagged = bool(judge.get("reread")) or any(not image_ok(i.get("problem")) for i in judge.get("images", []))
    return "FAIL" if (flagged or checkres["fails"]) else "PASS"


def print_judge(st):
    j = st["judge"]
    print(f"copygate judge: {st['file']}  (scope: {scope_line(st.get('scope') or DEFAULT_SCOPE)})")
    print(f"  reader: {st['reader']} ({st['model']}), reading grade {st['grade']}")
    for f in st["mechanical_fails"]:
        print("  FAIL (mechanical):", f)
    for x in j.get("reread", []):
        print(f"  RE-READ: \"{x.get('text','')}\"\n           {x.get('why','')}")
    for x in j.get("not_their_words", []):
        print(f"  NOT THEIR WORDS: \"{x.get('text','')}\" {('(' + x.get('why','') + ')') if x.get('why') else ''}")
    for x in j.get("images", []):
        if not image_ok(x.get("problem")):
            print(f"  IMAGE: \"{x.get('alt','')[:90]}\" -> {x.get('problem')}")
    if j.get("summary"):
        print("  reader's summary:", j["summary"])
    print(f"  VERDICT: {st['verdict']}  (stamp: {stamp_path(st['file']).name})")
    print("  This is a note for Ryan, never a block. One fix pass, at most one re-read, then ship (README: The judge).")


def scope_flags(scope):
    f = []
    if scope.get("from"):
        f.append(f"--from \"{scope['from']}\"")
    if scope.get("section"):
        f.append(f"--section \"{scope['section']}\"")
    if not scope.get("tags", True):
        f.append("--keep-tags")
    if not scope.get("footer", True):
        f.append("--keep-footer")
    return (" " + " ".join(f)) if f else ""


def print_subagent_brief(path, scope, why=""):
    sf = scope_flags(scope)
    if why:
        print(f"  judge: {why}")
    print("  No stamp written here. Spawn ONE fresh Agent (general-purpose, sonnet) with the full text of tools/copygate/READER-PROMPT.md")
    print(f"  as its instructions. It runs: python3 tools/copygate/coldread.py text \"{path}\"{sf}   reads it ONCE as a stranger, writes")
    print(f"  its JSON verdict to a file, then runs: python3 tools/copygate/coldread.py stamp \"{path}\"{sf} --reader subagent --json @<verdict file>")
    print("  Say once per session in the reply to Ryan: the headless stranger (`claude -p`) is logged out; `claude login` in a terminal")
    print("  restores the true stranger (then use `judge --headless`). Do not run claude login yourself.")
    print("  Read cap: this read, fix the flags, at most one re-read, then ship with remaining flags as notes. Never a third read.")


def judge(path, args):
    scope = scope_of(args)
    checkres = check(path, scope)
    if "--headless" not in args:
        # 11-02 default: the in-session fresh Agent is the reader. The headless CLI has been logged out since 10-27
        # and every judge call spent a turn finding that out.
        print_check(checkres)
        print_subagent_brief(path, scope)
        return 4
    text, alts = extract(path, scope)
    prompt = build_prompt(path, text, alts, checkres["language"])
    res, err = None, None
    for _ in range(2):
        res, err = headless(prompt)
        if err:
            break
        try:
            j = parse_json(res)
            break
        except Exception as e:
            err = f"reader output was not JSON ({e})"
            j = None
    if err:
        print_check(checkres)
        print_subagent_brief(path, scope, why=err)
        return 4
    v = verdict_from(j, checkres)
    st = write_stamp(path, v, "headless", MODEL, checkres, j)
    print_judge(st)
    return 0 if v == "PASS" else 1


def stamp_cmd(path, args):
    reader = args.get("--reader", "subagent")
    if reader not in ("subagent",):
        print("stamp: --reader must be subagent (headless stamps come from `judge --headless`, Ryan's from `approve`)"); return 2
    raw = args.get("--json")
    if not raw:
        print("stamp: --json '<verdict json>' required"); return 2
    if raw.startswith("@"):
        raw = Path(raw[1:]).read_text()
    j = parse_json(raw)
    checkres = check(path, scope_of(args))
    v = verdict_from(j, checkres)
    st = write_stamp(path, v, "subagent", args.get("--model", "in-session agent"), checkres, j)
    print_judge(st)
    return 0 if v == "PASS" else 1


def approve(path, args):
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("approve: refuses to run without a terminal. This is Ryan's override, typed by Ryan, never by an agent."); return 2
    note = args.get("--note", "")
    if not note:
        print("approve: --note \"why this is fine as written\" required"); return 2
    checkres = check(path, scope_of(args))
    st, why = read_stamp(path)
    prev = st.get("judge") if st else {}
    write_stamp(path, "PASS", "ryan", "override", checkres, prev or {}, note=note)
    print(f"approved by Ryan: {path}\n  note: {note}")
    return 0


def status(path):
    st, why = read_stamp(path)
    print(f"copygate status: {path}\n  {why}" + (f" (reader {st.get('reader')}, {st.get('time')})" if st else ""))
    return 0 if why.startswith("valid") else 3


def parse_args(argv):
    args = {}
    k = 0
    while k < len(argv):
        if argv[k].startswith("--"):
            args[argv[k]] = argv[k + 1] if k + 1 < len(argv) and not argv[k + 1].startswith("--") else "1"
            k += 2 if (k + 1 < len(argv) and not argv[k + 1].startswith("--")) else 1
        else:
            k += 1
    return args


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    cmd, path = argv[0], argv[1]
    if not Path(path).exists():
        print(f"no such file: {path}"); return 2
    args = parse_args(argv[2:])
    scope = scope_of(args)
    if cmd == "check":
        r = check(path, scope); print_check(r); return 1 if r["fails"] else 0
    if cmd == "text":
        t, alts = extract(path, scope); print(t); [print("[image]", a) for a in alts]; return 0
    if cmd == "judge":
        return judge(path, args)
    if cmd == "stamp":
        return stamp_cmd(path, args)
    if cmd == "approve":
        return approve(path, args)
    if cmd == "status":
        return status(path)
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
