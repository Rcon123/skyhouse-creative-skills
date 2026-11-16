#!/usr/bin/env python3
"""Cluster Atria pulls by ad text and print the seven ranked market boards.

Usage: python3 tools/research/spy_boards.py <data-dir> [--ours "Brand Name"] [--now YYYY-MM-DD]

Boards: outcomes, sub-outcomes, personas, concepts, angles, awareness, formats.
Copies = duplicate ads sharing normalised body text. Repetition is the signal;
run duration is not (Jason, Aug 20 call). Discount/catalog ads are stripped first.
"""
import argparse, glob, json, os, re, sys
from collections import defaultdict
from datetime import datetime, timezone

def norm(s):
    s = (s or "").lower()
    s = re.sub(r"http\S+", " ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def parse(d):
    if not d: return None
    try:
        dt = datetime.fromisoformat(str(d).replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None

OFFERY = re.compile(r"\b(\d{1,2}% ?off|free gift|free shipping|buy \d|bogo|\bsale\b|discount|subscribe|coupon|limited time|risk free|money back)\b", re.I)

def rx(*p): return re.compile("|".join(p), re.I)

OUTCOME = [
 ("Lose the belly / body fat",      rx(r"belly", r"\bfat\b", r"dad bod", r"love handles", r"lose weight")),
 ("Raise testosterone / vitality",  rx(r"testosterone", r"\blow t\b", r"\bt levels", r"virility", r"masculin")),
 ("Sexual performance / desire",    rx(r"\blibido", r"sex drive", r"erection", r"morning wood", r"bedroom", r"desire")),
 ("Energy / stop being tired",      rx(r"energy", r"fatigue", r"tired", r"exhaust", r"stamina", r"drained")),
 ("Muscle / strength",              rx(r"muscle", r"strength", r"\bgains\b", r"definition")),
 ("Look / man boobs / appearance",  rx(r"man boobs", r"moobs", r"chest fat", r"gyneco", r"physique")),
 ("Mind / mood / focus",            rx(r"brain fog", r"focus", r"\bmood\b", r"irritab", r"motivation", r"confidence")),
]
SUB = [
 ("Beer belly gone",                rx(r"beer belly")),
 ("Man boobs gone",                 rx(r"man boobs", r"moobs", r"chest fat")),
 ("Morning wood back",              rx(r"morning wood")),
 ("Wife / partner wants him again", rx(r"\bwife\b", r"\bhusband\b", r"\bmarriage\b", r"her again")),
 ("Dad bod reversed",               rx(r"dad bod")),
 ("Off TRT / no needles",           rx(r"\btrt\b", r"needles", r"injections")),
 ("Keep up with kids/grandkids",    rx(r"grandkid", r"grandchild", r"grandfather", r"my son", r"play with")),
]
PERSONA = [
 ("Man 60+",                    rx(r"\b6[0-9] year", r"\b7[0-9] year", r"\bover 6[05]\b", r"\bover 70\b")),
 ("Man 50s",                    rx(r"\b5[0-9] year", r"\bover 50\b", r"\bin his 50s")),
 ("Man 40s",                    rx(r"\b4[0-9] year", r"\bover 40\b", r"\bin his 40s")),
 ("The wife / woman narrating", rx(r"\bmy husband\b", r"\bhis wife\b", r"\bwives\b")),
 ("Doctor / medical authority", rx(r"\bdoctor\b", r"\bdr\.", r"physician", r"endocrinolog", r"surgeon")),
 ("Everyday guy / UGC",         rx(r"\bi tried\b", r"\bi started\b", r"\bmy story\b", r"i was skeptical")),
]
CONCEPT = [
 ("Common foods turn T into estrogen",  rx(r"common foods", r"these foods", r"feminizing food", r"\b5 foods", r"five foods", r"foods.{0,25}estrogen", r"avoid these")),
 ("Aromatase enzyme steals your T",     rx(r"aromatase", r"enzyme.{0,30}(testosterone|estrogen)", r"converts? .{0,15}testosterone")),
 ("Excess estrogen is the real problem",rx(r"excess estrogen", r"estrogen (overload|dominan|levels)", r"more estrogen", r"estrocontrol", r"estrogen blocker")),
 ("Cortisol / stress made you soft",    rx(r"cortisol", r"stress hormone")),
 ("Reindeer / arctic organs",           rx(r"reindeer", r"arctic (herb|organ)")),
 ("Beef organs are the answer",         rx(r"beef organ", r"beef testicle", r"organ complex")),
 ("Water retention / bloat, not fat",   rx(r"excess water", r"water retention", r"bloat", r"puffy")),
 ("Doctor's 'normal' is wrong",         rx(r"normal for your age", r"doctor said.{0,30}normal", r"came back normal")),
 ("TRT is a trap / dependency",         rx(r"\btrt\b.{0,40}(trap|depend|shut down|forever)", r"no needles", r"without trt")),
 ("Diet and exercise can't fix this",   rx(r"diet (and|&) exercise", r"nothing worked", r"did everything right", r"tried everything")),
 ("Tongkat / herb ingredient",          rx(r"tongkat", r"fadogia", r"ashwagandha", r"boron", r"shilajit")),
 ("A hidden gene / switch",             rx(r"\bgene\b", r"\bswitch\b")),
]
ANGLE = [
 ("Doctor dismissed him",         rx(r"doctor (said|told|laughed|dismissed)", r"normal for your age", r"came back normal")),
 ("Tried everything / failed",    rx(r"nothing worked", r"tried everything", r"did everything right", r"diet (and|&) exercise")),
 ("Personal transformation",      rx(r"\bi (lost|dropped|went from)\b", r"\bmy story\b", r"weeks later", r"before and after")),
 ("Warning / cautionary tale",    rx(r"\bwarning\b", r"stop (eating|taking)", r"\bavoid\b", r"never eat", r"dangerous")),
 ("Conspiracy / hidden",          rx(r"they don'?t want", r"\bhidden\b", r"big pharma", r"suppress", r"banned")),
 ("Comparison / which one",       rx(r"\bvs\b", r"compare", r"which one", r"i tested both")),
 ("Quiz / diagnostic",            rx(r"\bquiz\b", r"which type", r"find out if")),
 ("Countdown / list",             rx(r"\b\d+ reasons\b", r"\btop \d+\b", r"\b\d+ foods\b", r"number \d")),
 ("Wife / spouse POV",            rx(r"\bmy husband\b", r"wives love", r"\bhis wife\b")),
]
AWARE = [
 ("Product aware (names product/offer)", rx(r"\bbuy\b", r"\border\b", r"capsul", r"supplement", r"\bbottle\b", r"formula", r"\bgumm", r"\bstack\b")),
 ("Solution aware (names a fix type)",   rx(r"t.?booster", r"\btrt\b", r"blocker", r"protocol", r"treatment")),
 ("Problem aware (symptom led)",         rx(r"belly", r"tired", r"libido", r"man boobs", r"brain fog", r"low t", r"energy")),
]

def build(datadir, ours, now):
    rows, seen = [], {}
    for f in glob.glob(os.path.join(datadir, "atria-*.jsonl")):
        for line in open(f, encoding="utf8"):
            line = line.strip()
            if not line: continue
            try: r = json.loads(line)
            except Exception: continue
            if r.get("id"): seen[r["id"]] = r
    rows = list(seen.values())
    cl = defaultdict(list)
    for r in rows:
        k = norm(r.get("body") or "") or ("T:" + norm(r.get("title") or ""))
        if len(k) >= 25: cl[k].append(r)
    out = []
    for k, ads in cl.items():
        st = [parse(a.get("start_date")) for a in ads]; st = [s for s in st if s]
        if not st: continue
        brands = sorted({a.get("brand_name") for a in ads if a.get("brand_name")})
        sample = max(ads, key=lambda a: len(a.get("body") or ""))
        out.append({"copies": len(ads), "live": sum(1 for a in ads if a.get("status") == "active"),
                    "brands": brands, "recent56": sum(1 for s in st if (now - s).days <= 56),
                    "first": min(st).date().isoformat(), "last": max(st).date().isoformat(),
                    "title": sample.get("title") or "", "body": (sample.get("body") or "")[:900],
                    "url": (sample.get("link_url") or "").lower(),
                    "formats": {a.get("display_format") or "?": 1 for a in ads}})
    return rows, out

def board(name, table, sel, ed, top=12):
    agg = defaultdict(lambda: {"copies":0,"live":0,"brands":set(),"recent":0})
    for c in ed:
        if not sel(c): continue
        t = (c["title"] + " " + c["body"]).lower()
        for lab, p in table:
            if p.search(t):
                a = agg[lab]; a["copies"] += c["copies"]; a["live"] += c["live"]
                a["brands"] |= set(c["brands"]); a["recent"] += c["recent56"]
    print(f"\n### {name}")
    print(f'{"":40s} {"copies":>7s} {"live":>6s} {"br":>3s} {"new8wk":>7s}  trend')
    for lab, a in sorted(agg.items(), key=lambda x: -x[1]["copies"])[:top]:
        sh = a["recent"]/a["copies"] if a["copies"] else 0
        tr = "RISING" if sh >= .35 else ("fading" if sh <= .05 else "steady")
        print(f'{lab[:40]:40s} {a["copies"]:7d} {a["live"]:6d} {len(a["brands"]):3d} {a["recent"]:7d}  {tr}')

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("datadir"); ap.add_argument("--ours", default="Live Anabolic")
    ap.add_argument("--now", default="2026-08-21")
    a = ap.parse_args()
    now = datetime.fromisoformat(a.now).replace(tzinfo=timezone.utc)
    rows, cl = build(a.datadir, a.ours, now)
    ed = [c for c in cl if not OFFERY.search(c["title"] + " " + c["body"])]
    print(f"ads {len(rows)}  clusters {len(cl)}  editorial {len(ed)}  "
          f"copies {sum(c['copies'] for c in cl)} -> editorial {sum(c['copies'] for c in ed)}")
    OURS = {a.ours}
    mkt = lambda c: not (set(c["brands"]) & OURS)
    our = lambda c: bool(set(c["brands"]) & OURS)
    print("\n" + "="*74); print("MARKET (real competitors)"); print("="*74)
    for n, t in [("TOP OUTCOMES",OUTCOME),("TOP SUB-OUTCOMES",SUB),("TOP PERSONAS",PERSONA),
                 ("TOP CONCEPTS",CONCEPT),("TOP ANGLES",ANGLE),("TOP AWARENESS",AWARE)]:
        board(n, t, mkt, ed)
    print("\n" + "="*74); print(f"OURS ({a.ours}, the client's in-house account)"); print("="*74)
    for n, t in [("TOP CONCEPTS",CONCEPT),("TOP ANGLES",ANGLE),("TOP PERSONAS",PERSONA)]:
        board(n, t, our, ed)
    json.dump(ed, open(os.path.join(a.datadir, "_clusters.json"), "w"), indent=1)
