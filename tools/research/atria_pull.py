#!/usr/bin/env python3
"""Atria brand-library + semantic-search puller.

Usage:
  python3 tools/research/atria_pull.py --out <dir> --brand ID:name [--brand ...] \
      [--query "text":slug ...] [--cap 12000]

Writes <out>/atria-<slug>-<YYYY-MM-DD>.jsonl. Key from .env (ATRIA_API_KEY).
Notes baked in from prior runs: use order=most_active for deep history; the
search endpoint honours `query=`, never `keyword=`.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request
from datetime import date

BASE = "https://api.tryatria.com"

def key():
    k = os.environ.get("ATRIA_API_KEY")
    if k: return k
    for line in open(os.path.join(os.path.dirname(__file__), "..", "..", ".env"), encoding="utf8"):
        if line.startswith("ATRIA_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("no ATRIA_API_KEY")

K = key()

def get(url, tries=4):
    req = urllib.request.Request(url, headers={"X-API-Key": K, "User-Agent": "skyhouse-research"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf8", "ignore"))
        except Exception as e:
            if i == tries - 1:
                print(f"  FAIL {url[:110]} :: {e}", file=sys.stderr); return None
            time.sleep(3 + 3 * i)

def page(path, params, cap):
    out, cursor, n = [], None, 0
    while len(out) < cap:
        p = dict(params); p["page_size"] = 50
        if cursor: p["cursor"] = cursor
        d = get(f"{BASE}{path}?" + urllib.parse.urlencode(p))
        if not d: break
        data = d.get("data") or {}
        ads = data.get("items") or []
        if not ads: break
        out.extend(ads)
        cursor = data.get("cursor")
        n += 1
        if not cursor: break
        if n % 20 == 0:
            print(f"    ...{len(out)}", flush=True)
        time.sleep(0.15)
    return out[:cap]

def write(outdir, slug, ads):
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, f"atria-{slug}-{date.today().isoformat()}.jsonl")
    with open(p, "w", encoding="utf8") as f:
        for a in ads:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
    print(f"  wrote {len(ads):6d} -> {os.path.basename(p)}", flush=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--brand", action="append", default=[])
    ap.add_argument("--query", action="append", default=[])
    ap.add_argument("--cap", type=int, default=12000)
    a = ap.parse_args()
    for b in a.brand:
        bid, name = b.split(":", 1)
        print(f"brand {name} ({bid})", flush=True)
        # 2026-10-29: /brand-library/{id}/ads returns 404 ("no matching open API"). Brand libraries now
        # come through the search endpoint filtered by brand_id. No order param on this route.
        ads = page("/open/v1/ad-library/search", {"brand_id": bid}, a.cap)
        write(a.out, name, ads)
    for q in a.query:
        text, slug = q.rsplit(":", 1)
        print(f"query {text!r}", flush=True)
        ads = page("/open/v1/ad-library/search", {"query": text}, min(a.cap, 1000))
        hit = sum(1 for x in ads if text.split()[0].lower() in json.dumps(x).lower())
        print(f"    sanity: {hit}/{len(ads)} contain '{text.split()[0]}'", flush=True)
        write(a.out, f"q-{slug}", ads)
