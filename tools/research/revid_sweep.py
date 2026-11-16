#!/usr/bin/env python3
"""
Revid viral-TikTok sweep. Revid (revid.ai/tiktok-video-finder) keeps an index of
~2.4M viral TikToks with transcripts, play counts, an AI "setting" tag and a copy
of every mp4 on its own CDN. Its search is a POST to /api/tiktok-search; this
script runs a list of keywords through it, filters by plays, dedupes, saves the
rows, downloads covers and (optionally) the mp4s.

Usage:
  python3 tools/research/revid_sweep.py <out_folder> --keywords kw1,kw2,... [--min-plays 100000]
         [--days 365] [--sort diggCount:desc|createTime:desc|""] [--setting Virtual] [--videos]
  python3 tools/research/revid_sweep.py <out_folder> --keyword-file words.txt ...

Rate limit: the anonymous endpoint says "You used this feature too much" after a
burst; the script backs off and retries. A logged-in Revid session lifts it: set
REVID_COOKIE="<cookie header>" to send it.

Rows: {id,url,author,text,desc,views,likes,shares,comments,secs,created,cover,video,setting,perspective,origin,query}
"""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://www.revid.ai/api/tiktok-search"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def search(keywords, min_plays=0, days=365, sort="diggCount:desc", setting=None, perspective=None):
    now = int(time.time())
    filters = ["nbChar > 10", "lang = 'en'", f"createTime >= {now - days * 86400} AND createTime <= {now}"]
    if setting:
        filters.append(f"setting = '{setting}'")
    if perspective:
        filters.append(f"perspective = '{perspective}'")
    if min_plays:
        filters.append(f"playCount > {int(min_plays)}")
    body = {"keywords": keywords, "filtersFast": filters, "extraParams": {"sort": sort}}
    headers = {"Content-Type": "application/json", "User-Agent": UA, "Origin": "https://www.revid.ai",
               "Referer": "https://www.revid.ai/tiktok-video-finder"}
    if os.environ.get("REVID_COOKIE"):
        headers["Cookie"] = os.environ["REVID_COOKIE"]
    req = urllib.request.Request(API, data=json.dumps(body).encode(), headers=headers)
    wait = 20
    for attempt in range(8):
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        if d.get("videos") is not None:
            return d["videos"]
        if "too much" in (d.get("error") or ""):
            print(f"  rate-limited, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
            wait = min(wait * 2, 180)
            continue
        raise RuntimeError(d.get("error") or str(d)[:200])
    raise RuntimeError("rate limit did not lift")


def norm(v, query):
    return {
        "id": str(v.get("id")), "url": v.get("url"), "author": v.get("username"), "nick": v.get("userNickname"),
        "text": (v.get("text") or "")[:600], "desc": (v.get("desc") or "")[:300],
        "views": int(v.get("playCount") or 0), "likes": int(v.get("diggCount") or 0),
        "shares": int(v.get("shareCount") or 0), "comments": int(v.get("commentCount") or 0),
        "secs": v.get("durationInSeconds"),
        "created": datetime.fromtimestamp(int(v.get("createTime") or 0), tz=timezone.utc).strftime("%Y-%m-%d"),
        "cover": v.get("imagePreview"), "video": v.get("urlUploaded"),
        "setting": v.get("setting"), "perspective": v.get("perspective"), "origin": v.get("visualOrigin"),
        "ctype": v.get("contentType"), "query": query,
    }


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main(argv):
    folder = argv[0].rstrip("/")
    args = argv[1:]
    get = lambda k, d=None: args[args.index(k) + 1] if k in args else d
    kws = []
    if get("--keywords"):
        kws += [k.strip() for k in get("--keywords").split(",") if k.strip()]
    if get("--keyword-file"):
        kws += [l.strip() for l in open(get("--keyword-file")) if l.strip() and not l.startswith("#")]
    min_plays = int(get("--min-plays", 100000))
    days = int(get("--days", 365))
    sort = get("--sort", "diggCount:desc")
    setting = get("--setting")
    want_videos = "--videos" in args
    os.makedirs(os.path.join(folder, "covers"), exist_ok=True)
    seen_path = os.path.join(folder, "..", "revid-seen.json")
    try:
        seen = set(json.load(open(seen_path)))
    except Exception:  # noqa: BLE001
        seen = set()
    rows = {}
    for i, kw in enumerate(kws, 1):
        try:
            vids = search(kw, min_plays, days, sort, setting)
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(kws)}] {kw!r} failed: {e}", file=sys.stderr)
            continue
        new = 0
        for v in vids:
            r = norm(v, kw)
            if r["id"] in seen or r["id"] in rows:
                continue
            rows[r["id"]] = r
            new += 1
        print(f"[{i}/{len(kws)}] {kw!r}: {len(vids)} hits, {new} new", flush=True)
        time.sleep(2.5)
    out = sorted(rows.values(), key=lambda r: -r["views"])
    for n, r in enumerate(out, 1):
        r["n"] = n
        r["thumb"] = os.path.join(folder, "covers", f"{n:03d}_{r['id']}.png")
        if r["cover"] and not os.path.exists(r["thumb"]):
            try:
                open(r["thumb"], "wb").write(fetch(r["cover"]))
            except Exception as e:  # noqa: BLE001
                print(f"[cover] {r['id']}: {e}", file=sys.stderr)
        if want_videos and r["video"]:
            mp4 = os.path.join(folder, "videos", f"{n:03d}_{r['id']}.mp4")
            os.makedirs(os.path.dirname(mp4), exist_ok=True)
            if not os.path.exists(mp4):
                try:
                    open(mp4, "wb").write(fetch(r["video"]))
                except Exception as e:  # noqa: BLE001
                    print(f"[video] {r['id']}: {e}", file=sys.stderr)
    json.dump(out, open(os.path.join(folder, "candidates.json"), "w"), indent=1)
    json.dump(sorted(seen | set(rows)), open(seen_path, "w"))
    print(f"{len(out)} new rows -> {folder}/candidates.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
