#!/usr/bin/env python3
"""
Weird AI video finder: pull weird / AI-made videos from places that are NOT
ad-spy tools (X, TikTok, Instagram via Apify; r/aivideo via the safereddit
mirror; YouTube search HTML), build a numbered contact sheet, and leave the
"can this become an ad" judgment to the weekly Claude task that looks at it.

Subcommands:
  apify  <folder> [--days 7] [--per 40]
         X + TikTok + Instagram pulls through Apify (token = the one in
         ~/scripts/winners-audit.py). Writes <folder>/candidates.json,
         <folder>/covers/, <folder>/sheet.jpg, <folder>/CANDIDATES.md.
         Skips anything already in offers/_weird-videos/seen.json.
         Refuses to run when the Apify account is at its monthly cap.
  board  <folder>
         Same sheet + BOARD.md from a reddit posts.json (see docstring in
         cmd_board). Reddit rows come from the safereddit mirror in the
         built-in browser because reddit.com 403s curl.
  youtube [--period week|month] [--out FILE.json]
         YouTube search sorted by views. Noisy; secondary.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SEEN = os.path.join(ROOT, "offers", "_weird-videos", "seen.json")

# ---------------------------------------------------------------- helpers

def fetch(url, timeout=30, data=None, headers=None):
    if "api.apify.com/v2/key-value-stores/" in url and "token=" not in url:
        url += ("&" if "?" in url else "?") + "token=" + apify_token()
    h = {"User-Agent": UA, "Accept-Language": "en-US"}
    h.update(headers or {})
    req = urllib.request.Request(url, headers=h, data=data, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def load_seen():
    try:
        return set(json.load(open(SEEN)))
    except Exception:  # noqa: BLE001
        return set()


def save_seen(ids):
    os.makedirs(os.path.dirname(SEEN), exist_ok=True)
    json.dump(sorted(ids), open(SEEN, "w"))


def num(x):
    try:
        return int(x or 0)
    except Exception:  # noqa: BLE001
        return 0


def make_sheet(rows, folder, img_key, cap_lines, name="sheet.jpg", cols=5):
    """rows need ['n'] and rows[img_key] = local image path. cap_lines(row) -> (line1, line2)."""
    from PIL import Image, ImageDraw, ImageFont
    cw, ch, pad, cap = 384, 384, 8, 44
    nrows = (len(rows) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + pad) + pad, max(1, nrows) * (ch + cap + pad) + pad), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
        big = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except Exception:  # noqa: BLE001
        font = big = ImageFont.load_default()
    for r in rows:
        i = r["n"] - 1
        x = pad + (i % cols) * (cw + pad)
        y = pad + (i // cols) * (ch + cap + pad)
        try:
            im = Image.open(r[img_key]).convert("RGB")
            im.thumbnail((cw, ch))
            sheet.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))
        except Exception:  # noqa: BLE001
            draw.rectangle([x, y, x + cw, y + ch], outline=(80, 80, 80))
        draw.rectangle([x, y, x + 44, y + 28], fill=(230, 60, 60))
        draw.text((x + 6, y + 3), str(r["n"]), fill="white", font=big)
        l1, l2 = cap_lines(r)
        draw.text((x, y + ch + 4), l1[:50], fill=(200, 200, 200), font=font)
        draw.text((x, y + ch + 23), l2[:50], fill="white", font=font)
    p = os.path.join(folder, name)
    sheet.save(p, quality=88)
    return p


# ---------------------------------------------------------------- apify

def apify_token():
    src = os.path.expanduser("~/scripts/winners-audit.py")
    m = re.search(r'APIFY_TOKEN\s*=\s*"([^"]+)"', open(src).read())
    return m.group(1)


def apify_call(token, actor, inp, timeout=600):
    url = f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?token={token}"
    out = json.loads(fetch(url, timeout=timeout, data=json.dumps(inp).encode(),
                           headers={"Content-Type": "application/json"}))
    if isinstance(out, dict) and out.get("error"):
        raise RuntimeError(out["error"].get("message"))
    return out


def apify_capped(token):
    d = json.loads(fetch(f"https://api.apify.com/v2/users/me/limits?token={token}"))["data"]
    cap, used = d["limits"]["maxMonthlyUsageUsd"], d["current"]["monthlyUsageUsd"]
    return used >= cap - 0.25, cap, used


# What we search for. Tool names are the hashtag the makers use themselves.
X_QUERIES = [
    '("ai video" OR seedance OR veo OR kling OR sora) (grandma OR "old lady" OR face OR skin OR wrinkles OR hair OR bald OR skeleton OR bones OR belly OR "dog teeth" OR dentist) filter:videos min_faves:500 -filter:replies lang:en',
    '("ai video" OR seedance OR veo OR kling) (claymation OR "stop motion" OR puppet OR musical OR "soap opera" OR storybook OR "70s commercial" OR "80s commercial") filter:videos min_faves:300 -filter:replies lang:en',
]
TIKTOK_QUERIES = ["ai face melting", "ai face stretch", "ai wrinkles", "ai grandma funny", "ai old lady transformation", "ai aging",
                  "ai skin peel", "ai botox", "ai hair growing", "ai bald head", "ai skeleton", "ai bones x-ray", "ai belly fat",
                  "ai dog teeth", "ai dog dentist", "ai old man funny", "ai claymation", "ai stop motion ad", "ai musical song story",
                  "ai puppet show", "ai storybook narrated", "ai old tv commercial", "ai soap opera",
                  "ai miniature world", "ai tiny people", "ai giant hands", "ai diorama", "ai puppet", "ai asmr satisfying",
                  "ai living food", "ai mukbang weird", "ai hydraulic press", "ai x-ray vision", "ai found footage", "ai game show"]
# creators Ryan liked (2026-10-22): their newest popular posts come in every week
TIKTOK_PROFILES = ["floredelune.ai", "helpinghands0101", "amara__voss", "fore.auggie", "artificial.world08", "kookoai", "aidreamcode", "predmet_ai"]
TIKTOK_TAGS = ["aigrandma", "aiclaymation", "aistopmotion", "aiskeleton", "aiface"]
IG_TAGS = ["aigrandma", "aiclaymation", "claymation", "aiskeleton", "aiface", "aiold", "aidog"]


def pull_x(token, days, per):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = []
    for q in X_QUERIES:
        try:
            res = apify_call(token, "kaitoeasyapi~twitter-x-data-tweet-scraper-pay-per-result-cheapest",
                             {"twitterContent": f"{q} since:{since}", "maxItems": per, "queryType": "Top", "lang": "en"})
        except Exception as e:  # noqa: BLE001
            print(f"[x] failed: {e}", file=sys.stderr)
            continue
        for t in res:
            if not isinstance(t, dict) or "text" not in t:
                continue
            media = t.get("extendedEntities", {}).get("media") or t.get("media") or []
            vid = next((m for m in media if isinstance(m, dict) and m.get("type") in ("video", "animated_gif")), None)
            if not vid:
                continue
            a = t.get("author") or {}
            rows.append({
                "src": "x", "id": "x_" + str(t.get("id")), "url": t.get("url") or t.get("twitterUrl"),
                "author": a.get("userName"), "text": (t.get("text") or "")[:300],
                "likes": num(t.get("likeCount")), "views": num(t.get("viewCount")),
                "cover": vid.get("media_url_https") or vid.get("mediaUrl"), "posted": (t.get("createdAt") or "")[:16],
                "video": next((v.get("url") for v in (vid.get("video_info", {}).get("variants") or []) if v.get("content_type") == "video/mp4"), None),
            })
    return rows


def pull_tiktok(token, days, per):
    rows = []
    date_filter = "PAST_WEEK" if days <= 7 else "PAST_MONTH"
    jobs = [{"searchQueries": TIKTOK_QUERIES, "searchSection": "/video", "videoSearchSorting": "MOST_LIKED",
             "videoSearchDateFilter": date_filter, "resultsPerPage": per // 2},
            {"hashtags": TIKTOK_TAGS, "resultsPerPage": per // 2},
            {"profiles": TIKTOK_PROFILES, "profileSorting": "latest", "resultsPerPage": 8}]
    for inp in jobs:
        inp.update({"shouldDownloadVideos": True, "shouldDownloadCovers": False, "proxyCountryCode": "US"})
        try:
            res = apify_call(token, "clockworks~tiktok-scraper", inp, timeout=420)
        except Exception as e:  # noqa: BLE001
            print(f"[tiktok] failed: {e}", file=sys.stderr)
            continue
        for v in res:
            if not isinstance(v, dict) or not v.get("id"):
                continue
            rows.append({
                "src": "tiktok", "id": "tt_" + str(v["id"]), "url": v.get("webVideoUrl"),
                "author": (v.get("authorMeta") or {}).get("name"), "text": (v.get("text") or "")[:300],
                "likes": num(v.get("diggCount")), "views": num(v.get("playCount")),
                "cover": (v.get("videoMeta") or {}).get("coverUrl"),
                "posted": (v.get("createTimeISO") or "")[:16],
                "video": (v.get("mediaUrls") or [None])[0],
                # clockworks writes a machine description of what happens in the clip: the filter reads this first
                "desc": ((v.get("videoMeta") or {}).get("aiVideoDescription") or "")[:700],
                "summary": ((v.get("videoMeta") or {}).get("aiVideoSummary") or "")[:300],
            })
    return rows


def pull_instagram(token, days, per):
    rows = []
    try:
        res = apify_call(token, "apify~instagram-hashtag-scraper",
                         {"hashtags": IG_TAGS, "resultsType": "reels", "resultsLimit": per // 2}, timeout=420)
    except Exception as e:  # noqa: BLE001
        print(f"[ig] failed: {e}", file=sys.stderr)
        return rows
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for p in res:
        if not isinstance(p, dict) or not p.get("id"):
            continue
        ts = p.get("timestamp") or ""
        try:
            if ts and datetime.fromisoformat(ts.replace("Z", "+00:00")) < cutoff:
                continue
        except Exception:  # noqa: BLE001
            pass
        rows.append({
            "src": "instagram", "id": "ig_" + str(p["id"]), "url": p.get("url"),
            "author": p.get("ownerUsername"), "text": (p.get("caption") or "")[:300],
            "likes": num(p.get("likesCount")), "views": num(p.get("videoPlayCount") or p.get("videoViewCount")),
            "cover": p.get("displayUrl"), "posted": ts[:16], "video": p.get("videoUrl"),
        })
    return rows


def cmd_apify(args):
    folder = args[0].rstrip("/")
    days = int(args[args.index("--days") + 1]) if "--days" in args else 7
    per = int(args[args.index("--per") + 1]) if "--per" in args else 40
    token = apify_token()
    capped, cap, used = apify_capped(token)
    print(f"apify plan cap ${cap}/mo, used ${used:.2f}")
    if capped:
        sys.exit("Apify account is at its monthly cap. Upgrade the plan at apify.com (Settings > Billing) or wait for the cycle reset.")
    os.makedirs(folder, exist_ok=True)
    seen = load_seen()
    rows = []
    for fn in (pull_x, pull_tiktok, pull_instagram):
        got = fn(token, days, per)
        print(f"{fn.__name__}: {len(got)}")
        rows += got
    byid = {}
    for r in rows:
        if r["id"] in seen or not r.get("cover"):
            continue
        if r["id"] not in byid or r["likes"] > byid[r["id"]]["likes"]:
            byid[r["id"]] = r
    # virality floor: Ryan wants viral + unique, so drop anything under 50k views (or 2.5k likes where views are hidden)
    rows = [r for r in byid.values() if (r["views"] or 0) >= 50000 or (not r["views"] and r["likes"] >= 2500)]
    rows = sorted(rows, key=lambda r: -(r["views"] or r["likes"] * 20))
    covers = os.path.join(folder, "covers")
    os.makedirs(covers, exist_ok=True)
    for i, r in enumerate(rows, 1):
        r["n"] = i
        r["thumb"] = os.path.join(covers, f"{i:02d}_{r['id']}.jpg")
        if not os.path.exists(r["thumb"]):
            try:
                open(r["thumb"], "wb").write(fetch(r["cover"]))
            except Exception as e:  # noqa: BLE001
                print(f"[cover] {r['id']} failed: {e}", file=sys.stderr)
            time.sleep(0.1)
    json.dump(rows, open(os.path.join(folder, "candidates.json"), "w"), indent=1)
    sheet = make_sheet(rows, folder, "thumb",
                       lambda r: (f"{r['src']}  {r['views']:,} views  {r['likes']:,} likes", f"@{r['author']}  {r['text'][:40]}"))
    lines = [f"# Weird AI video candidates, {os.path.basename(folder)} (last {days} days, X + TikTok + Instagram)", "",
             "Numbers match sheet.jpg. Unfiltered: the weekly task picks the ones that can become an ad.", ""]
    for r in rows:
        lines.append(f"{r['n']:>2}. [{r['src']}] @{r['author']}  {r['views']:,} views, {r['likes']:,} likes, {r['posted']}  "
                     f"{r['text'][:120].replace(chr(10), ' ')}  {r['url']}")
    open(os.path.join(folder, "CANDIDATES.md"), "w").write("\n".join(lines))
    save_seen(seen | {r["id"] for r in rows})
    print(f"{len(rows)} new candidates, sheet {sheet}")


def cmd_strips(args):
    """strips <folder> [--top 25] [--only 3,17,42]: download clips, 8-frame strip each, stacked into strips/strips-pN.jpg"""
    import subprocess
    from PIL import Image, ImageDraw, ImageFont
    folder = args[0].rstrip("/")
    rows = json.load(open(os.path.join(folder, "candidates.json")))
    top = int(args[args.index("--top") + 1]) if "--top" in args else 25
    only = [int(x) for x in args[args.index("--only") + 1].split(",")] if "--only" in args else None
    pick = [r for r in rows if (only and r["n"] in only) or (not only and r["n"] <= top)]
    D = os.path.join(folder, "strips")
    os.makedirs(D, exist_ok=True)
    done = []
    for r in pick:
        out = os.path.join(D, f"{r['n']}.jpg")
        if os.path.exists(out):
            done.append(r); continue
        if not r.get("video"):
            continue
        mp4 = os.path.join(D, f"{r['n']}.mp4")
        try:
            open(mp4, "wb").write(fetch(r["video"], timeout=120))
        except Exception as e:  # noqa: BLE001
            print(f"[strip] {r['n']} download failed: {e}", file=sys.stderr); continue
        if os.path.getsize(mp4) < 50000:
            continue
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                                   capture_output=True, text=True).stdout.strip() or 0)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-vf", f"fps={8 / max(dur, 1):.4f},scale=240:-1,tile=8x1",
                        "-frames:v", "1", out], check=False)
        os.remove(mp4)
        if os.path.exists(out):
            done.append(r)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    for page in range(0, len(done), 10):
        chunk = done[page:page + 10]
        ims = [(r, Image.open(os.path.join(D, f"{r['n']}.jpg"))) for r in chunk]
        W = max(im.width for _, im in ims); H = sum(im.height + 30 for _, im in ims)
        sheet = Image.new("RGB", (W, H), (18, 18, 18)); y = 0; d = ImageDraw.Draw(sheet)
        for r, im in ims:
            d.text((4, y + 4), f"#{r['n']}  {r['src']}  @{r['author']}  {r['views']:,} views  {(r['text'] or '')[:70]}", fill="white", font=font)
            y += 30; sheet.paste(im, (0, y)); y += im.height
        sheet.save(os.path.join(D, f"strips-p{page // 10 + 1}.jpg"), quality=85)
    print(f"{len(done)} strips, pages: {(len(done) + 9) // 10} in {D}")


# ---------------------------------------------------------------- youtube

SP = {"week": "CAMSBAgDEAE%3D", "month": "CAMSBAgEEAE%3D"}
YT_QUERIES = ["ai commercial seedance", "ai generated commercial", "fake ad ai video", "ai video weird",
              "ai ad veo", "kling ai ad", "ai video transformation before after", "ai short film seedance"]


def yt_search(q, period):
    html = fetch("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=" + SP[period]).decode("utf-8", "replace")
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        return []
    out = []

    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                out.append(o["videoRenderer"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(json.loads(m.group(1)))
    rows = []
    for v in out:
        runs = lambda k: "".join(r.get("text", "") for r in (v.get(k) or {}).get("runs", []))
        rows.append({"id": v.get("videoId"), "title": runs("title"), "channel": runs("ownerText"),
                     "views": (v.get("viewCountText") or {}).get("simpleText", ""),
                     "published": (v.get("publishedTimeText") or {}).get("simpleText", ""),
                     "length": (v.get("lengthText") or {}).get("simpleText", ""),
                     "url": "https://youtu.be/" + str(v.get("videoId")), "query": q})
    return rows


def views_int(s):
    m = re.search(r"([\d,.]+)\s*([KM]?)", s or "")
    if not m:
        return 0
    return int(float(m.group(1).replace(",", "")) * {"K": 1e3, "M": 1e6, "": 1}[m.group(2)])


def cmd_youtube(args):
    period = args[args.index("--period") + 1] if "--period" in args else "week"
    out = args[args.index("--out") + 1] if "--out" in args else None
    seen = {}
    for q in YT_QUERIES:
        try:
            for r in yt_search(q, period):
                if r["id"] and r["id"] not in seen:
                    seen[r["id"]] = r
        except Exception as e:  # noqa: BLE001
            print(f"[yt] {q!r} failed: {e}", file=sys.stderr)
    rows = sorted(seen.values(), key=lambda r: -views_int(r["views"]))
    for r in rows[:60]:
        print(f"{r['views']:>16} | {r['published']:>7} | {r['length']:>6} | {r['channel'][:22]:<22} | {r['title'][:70]:<70} | {r['url']}")
    if out:
        json.dump(rows, open(out, "w"), indent=1)


# ---------------------------------------------------------------- reddit board

def cmd_board(args):
    """posts.json rows: {id,title,flair,score,comments,created,author,poster,src};
    poster = the external-preview.redd.it path+query (safereddit serves it under /preview/external-pre/)."""
    folder = args[0].rstrip("/")
    posts = json.load(open(os.path.join(folder, "posts.json")))
    byid = {}
    for p in posts:
        if p["id"] not in byid or p["score"] > byid[p["id"]]["score"]:
            byid[p["id"]] = p
    posts = sorted(byid.values(), key=lambda p: -p["score"])
    thumbs = os.path.join(folder, "thumbs")
    os.makedirs(thumbs, exist_ok=True)
    for i, p in enumerate(posts, 1):
        p["n"] = i
        p["thumb"] = os.path.join(thumbs, f"{i:02d}_{p['id']}.jpg")
        if not os.path.exists(p["thumb"]):
            try:
                open(p["thumb"], "wb").write(fetch("https://external-preview.redd.it/" + p["poster"]))
            except Exception as e:  # noqa: BLE001
                print(f"[thumb] {p['id']} failed: {e}", file=sys.stderr)
    sheet = make_sheet(posts, folder, "thumb", lambda p: (f"{p['score']:,} up  {p['flair'][:34]}", p["title"][:46]))
    lines = [f"# Weird AI video board, r/aivideo, pulled {os.path.basename(folder)}", "",
             "Numbers match sheet.jpg. Score = reddit upvotes. The safereddit mirror plays the video without an account.", ""]
    groups = [("TV AD (fake product)", lambda p: "TV AD" in p["flair"]),
              ("CRAZY / MINDBLOWING", lambda p: "CRAZY" in p["flair"]),
              ("Everything else", lambda p: True)]
    done = set()
    for name, test in groups:
        sel = [p for p in posts if p["id"] not in done and test(p)]
        if not sel:
            continue
        lines += [f"## {name}", ""]
        for p in sel:
            done.add(p["id"])
            lines.append(f"{p['n']:>2}. **{p['title']}**  {p['score']:,} up, {p['comments']} comments, {p['created']}, u/{p['author']}, {p['flair']}  "
                         f"[reddit](https://www.reddit.com/r/aivideo/comments/{p['id']}/) [mirror](https://safereddit.com/r/aivideo/comments/{p['id']}/)")
        lines.append("")
    open(os.path.join(folder, "BOARD.md"), "w").write("\n".join(lines))
    print(f"{len(posts)} posts, sheet {sheet}")


if __name__ == "__main__":
    cmds = {"apify": cmd_apify, "strips": cmd_strips, "youtube": cmd_youtube, "board": cmd_board}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    cmds[sys.argv[1]](sys.argv[2:])
