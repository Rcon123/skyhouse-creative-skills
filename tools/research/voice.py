#!/usr/bin/env python3
"""Customer-voice + search-demand collector (Phase 3 + 4 of the research system).

Usage:
  python3 tools/research/voice.py <offer-slug> --config offers/<slug>/research/voice-config.json

Config: {"reddit_queries": [...], "subreddits": [...], "trustpilot": ["domain.com"],
         "suggest_seeds": [...]}
Raw pulls land in offers/<slug>/research/data/*.jsonl (the local queryable store).
A ranked summary prints to stdout.
"""
import json, os, re, sys, time, urllib.parse, urllib.request, collections

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 research"}


def get(url, retries=3, timeout=45):
    req = urllib.request.Request(url, headers=UA)
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:
            if i == retries - 1:
                print(f"  FAIL {url[:90]} {e}", file=sys.stderr)
                return None
            time.sleep(2 + 2 * i)


def jl(path, rows):
    with open(path, "a") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


REDLIB = "https://safereddit.com"  # reddit.com + old.reddit block scripts; redlib mirrors do not


def reddit_search(q, limit=100):
    """NOTE: reddit.com and old.reddit.com return 403 to scripts and reddit.com is
    blocked in the Browser pane. Use a redlib mirror. If the mirror throws a JS
    challenge, drive it through the Browser pane instead (preview_start + get_page_text)."""
    url = f"{REDLIB}/search.json?q={urllib.parse.quote(q)}&limit={limit}&sort=top&t=all"
    raw = get(url)
    if not raw:
        return []
    try:
        d = json.loads(raw)
    except Exception:
        return []
    out = []
    for c in d.get("data", {}).get("children", []):
        p = c.get("data", {})
        out.append({"src": "reddit", "q": q, "sub": p.get("subreddit"),
                    "title": p.get("title"), "text": (p.get("selftext") or "")[:3000],
                    "score": p.get("score"), "comments": p.get("num_comments"),
                    "url": "https://reddit.com" + (p.get("permalink") or "")})
    return out


def reddit_top_comments(permalink, limit=40):
    raw = get(f"https://old.reddit.com{permalink}.json?limit={limit}&sort=top")
    if not raw:
        return []
    try:
        d = json.loads(raw)
        thread = d[1]["data"]["children"]
    except Exception:
        return []
    out = []
    for c in thread:
        p = c.get("data", {})
        body = p.get("body")
        if body and len(body) > 40:
            out.append({"src": "reddit-comment", "permalink": permalink,
                        "text": body[:2000], "score": p.get("score")})
    return out


# AMAZON + BBB + TRUSTPILOT: all block scripts (503/403). All three DO work through the
# Browser pane: preview_start({url}) then get_page_text. Amazon search URL pattern:
#   https://www.amazon.com/s?k=<query>          (listings, prices, review counts, velocity)
#   https://www.amazon.com/product-reviews/<ASIN>/?filterByStar=critical   (the objections)
# Verified working 2026-08-03. Drive these from the browser, not from this script.


def trustpilot(domain, pages=3):
    out = []
    for pg in range(1, pages + 1):
        raw = get(f"https://www.trustpilot.com/review/{domain}?page={pg}")
        if not raw:
            break
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', raw, re.S)
        if not m:
            break
        try:
            d = json.loads(m.group(1))
            revs = d["props"]["pageProps"]["reviews"]
        except Exception:
            break
        for r in revs:
            out.append({"src": "trustpilot", "domain": domain,
                        "stars": r.get("rating"), "title": r.get("title"),
                        "text": (r.get("text") or "")[:2000],
                        "date": (r.get("dates") or {}).get("publishedDate")})
        if len(revs) < 20:
            break
    return out


def suggest(seed):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(seed)}"
    raw = get(url)
    if not raw:
        return []
    try:
        return json.loads(raw)[1]
    except Exception:
        return []


def suggest_sweep(seed):
    results = {}
    for suffix in [""] + [f" {c}" for c in "abcdefghijklmnopqrstuvwxyz"]:
        for s in suggest(seed + suffix):
            results[s] = True
        time.sleep(0.15)
    return list(results)


def main():
    slug = sys.argv[1]
    cfgpath = sys.argv[sys.argv.index("--config") + 1]
    cfg = json.load(open(cfgpath))
    ddir = f"offers/{slug}/research/data"
    os.makedirs(ddir, exist_ok=True)

    posts = []
    for q in cfg.get("reddit_queries", []):
        r = reddit_search(q)
        posts += r
        print(f"reddit '{q}': {len(r)} posts")
        time.sleep(1)
    # dedupe, keep engagement-ranked
    seen = {}
    for p in posts:
        seen[p["url"]] = p
    posts = sorted(seen.values(), key=lambda x: -(x.get("score") or 0))
    jl(f"{ddir}/reddit-posts.jsonl", posts)

    comments = []
    for p in posts[:25]:
        perma = p["url"].replace("https://reddit.com", "")
        c = reddit_top_comments(perma)
        comments += c
        time.sleep(1)
    jl(f"{ddir}/reddit-comments.jsonl", comments)
    print(f"reddit comments pulled: {len(comments)}")

    for dom in cfg.get("trustpilot", []):
        tp = trustpilot(dom)
        jl(f"{ddir}/trustpilot.jsonl", tp)
        print(f"trustpilot {dom}: {len(tp)} reviews")

    demand = {}
    for seed in cfg.get("suggest_seeds", []):
        s = suggest_sweep(seed)
        demand[seed] = s
        print(f"suggest '{seed}': {len(s)} queries")
    json.dump(demand, open(f"{ddir}/search-demand.json", "w"), indent=1)

    # ranked phrase summary off everything pulled
    STOP = set("the a an and or but if of to in for on with is are was were be been it its this that these those i my me we our you your they their he she his her at as from by not no so just have has had do does did can could would should will".split())
    freq = collections.Counter()
    corpus = [p.get("title", "") + " " + p.get("text", "") for p in posts]
    corpus += [c["text"] for c in comments]
    for t in corpus:
        words = re.findall(r"[a-z']+", t.lower())
        for n in (2, 3):
            for i in range(len(words) - n + 1):
                g = words[i:i + n]
                if g[0] in STOP or g[-1] in STOP:
                    continue
                freq[" ".join(g)] += 1
    print("\nTOP PHRASES (customer voice, ranked by frequency):")
    for ph, c in freq.most_common(40):
        if c >= 4:
            print(f"{c:5d}  {ph}")


if __name__ == "__main__":
    main()
