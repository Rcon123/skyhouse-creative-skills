#!/usr/bin/env python3
"""Find the top VIDEO clusters in an Atria pull, list their CDN urls.

Usage: python3 tools/research/teardown.py <data-dir> [--top 14] [--brand NAME]
Prints a ranked table plus a shell-ready list of (slug, url, preview_url).
"""
import argparse, glob, json, os, re
from collections import defaultdict
from datetime import datetime, timezone

def norm(s):
    s=(s or "").lower(); s=re.sub(r"http\S+"," ",s); s=re.sub(r"[^a-z0-9 ]+"," ",s)
    return re.sub(r"\s+"," ",s).strip()

OFFERY = re.compile(r"\b(\d{1,2}% ?off|free gift|free shipping|bogo|\bsale\b|discount|coupon|limited time|money back)\b", re.I)

ap=argparse.ArgumentParser(); ap.add_argument("datadir"); ap.add_argument("--top",type=int,default=14)
a=ap.parse_args()

seen={}
for f in glob.glob(os.path.join(a.datadir,"atria-*.jsonl")):
    for line in open(f,encoding="utf8"):
        line=line.strip()
        if not line: continue
        try: r=json.loads(line)
        except Exception: continue
        if r.get("id"): seen[r["id"]]=r

cl=defaultdict(list)
for r in seen.values():
    k=norm(r.get("body") or "") or ("T:"+norm(r.get("title") or ""))
    if len(k)>=25: cl[k].append(r)

rows=[]
for k,ads in cl.items():
    withvid=[x for x in ads if x.get("videos")]
    if not withvid: continue
    s=max(withvid,key=lambda x:len(x.get("body") or ""))
    v=(s.get("videos") or [{}])[0]
    if not v.get("url"): continue
    title=(s.get("title") or "")[:80]
    if OFFERY.search(title+" "+(s.get("body") or "")): continue
    rows.append({"copies":len(ads),"live":sum(1 for x in ads if x.get("status")=="active"),
        "brand":s.get("brand_name") or "?","title":title,
        "open":(s.get("body") or "").replace("\n"," ")[:100],
        "url":v["url"],"prev":v.get("preview_image_url") or "","dur":round(v.get("duration") or 0,1)})
rows.sort(key=lambda r:-r["copies"])
print(f"video clusters: {len(rows)}\n")
out=[]
for i,r in enumerate(rows[:a.top]):
    slug=re.sub(r'[^a-z0-9]+','-',(r["brand"]+"-"+r["title"]).lower()).strip('-')[:52]
    print(f'{r["copies"]:5d}cp live{r["live"]:5d} {r["dur"]:6.1f}s {r["brand"][:18]:18s} | {r["title"][:60]}')
    out.append({"slug":slug,**r})
json.dump(out, open(os.path.join(a.datadir,"_top_videos.json"),"w"), indent=1)
print(f'\nwrote {len(out)} -> _top_videos.json')
