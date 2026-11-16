#!/usr/bin/env python3
"""Amazon competitor + review miner (source 2.5 of the research brief spec).

From Amazon we want, per Jason: who the competitors actually are, what other
searches come up, prices/ratings/velocity, and the most-helpful reviews
(especially the negatives, which is where the differentiation angle hides).

Usage:
  python3 tools/research/amazon.py <slug> "liver detox supplement" "fatty liver supplement" ...

Amazon 503s a bare request but serves fine with full browser headers.
Raw output -> offers/<slug>/research/data/amazon-*.jsonl
"""
import json, os, re, sys, time, urllib.parse, urllib.request, html, collections

H = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none",
    "Sec-Fetch-Dest": "document", "Upgrade-Insecure-Requests": "1",
}


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=H)
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    import gzip
                    raw = gzip.decompress(raw)
                return raw.decode("utf-8", "ignore")
        except Exception as e:
            if i == tries - 1:
                print(f"  fail {url[:70]} {e}", file=sys.stderr)
                return None
            time.sleep(3 + 3 * i)


def clean(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s or "")).strip()


def search(term):
    """Listings: who is actually selling into this term."""
    u = "https://www.amazon.com/s?k=" + urllib.parse.quote(term)
    h = get(u)
    if not h:
        return [], []
    out = []
    # Amazon wraps each result in data-component-type="s-search-result".
    # Splitting on data-asin alone gets the boundaries wrong and loses every metric.
    cards = re.split(r'(?=<div[^>]*data-component-type="s-search-result")', h)[1:]
    for c in cards:
        asin = re.search(r'data-asin="([A-Z0-9]{10})"', c)
        title = re.search(r'<h2[^>]*>(?:.*?)<span[^>]*>([^<]{15,300})</span>', c, re.S)
        if not asin or not title:
            continue
        price = re.search(r'<span class="a-price-whole">([\d,]+)', c)
        frac = re.search(r'<span class="a-price-fraction">(\d+)', c)
        rating = re.search(r'([\d.]+) out of 5 stars', c)
        nrev = re.search(r'aria-label="([\d,]+)"[^>]*>\s*<span[^>]*a-size-base', c) or \
               re.search(r's-underline-text[^>]*>\(?([\d,]+)\)?<', c) or \
               re.search(r'"ratingCount"\s*:\s*"?([\d,]+)', c)
        sold = re.search(r'([\d.KM,]+\+?) bought in past month', c)
        out.append({
            "src": "amazon-listing", "term": term, "asin": asin.group(1),
            "title": clean(title.group(1))[:180],
            "price": (price.group(1).replace(",", "") + "." + (frac.group(1) if frac else "00")) if price else None,
            "rating": rating.group(1) if rating else None,
            "reviews": nrev.group(1).replace(",", "") if nrev else None,
            "sold_past_month": sold.group(1) if sold else None,
            "url": "https://www.amazon.com/dp/" + asin.group(1),
        })
    rel = set()
    for m in re.finditer(r'<span class="a-size-base a-color-base">([a-z0-9 \-\']{6,50})</span>', h):
        rel.add(html.unescape(m.group(1)).strip())
    for m in re.finditer(r'data-csa-c-item-id="[^"]*"[^>]*>\s*<[^>]*>\s*([a-z0-9 \-\']{6,50})\s*<', h):
        rel.add(html.unescape(m.group(1)).strip())
    return out, sorted(rel)


def reviews(asin, critical=None):
    """Top reviews off the PRODUCT page.

    Amazon now 302s /product-reviews/ to a login wall, and changed the review
    markup: data-hook is reviewTitle / reviewTextContainer / helpful-vote-statement.
    The /dp/ page still carries the most-helpful reviews unauthenticated.
    """
    h = get(f"https://www.amazon.com/dp/{asin}")
    if not h:
        return []
    out = []
    blocks = re.split(r'(?=data-hook="review" class="a-section aok-relative")', h)[1:]
    for c in blocks:
        c = c[:9000]
        title = re.search(r'data-hook="reviewTitle"[^>]*>(.*?)(?:<span|</a>)', c, re.S)
        star = re.search(r'([\d.]+) out of 5 stars', c)
        helpf = re.search(r'helpful-vote-statement"[^>]*>\s*([\d,]+|One) (?:person|people)', c)
        who = re.search(r'a-profile-name">([^<]{2,40})<', c)
        tj = c.find('reviewTextContainer')
        body = None
        if tj > 0:
            seg = c[tj:tj + 3000]
            seg = re.sub(r'Brief content visible.*?brief content\.', ' ', seg, flags=re.S)
            body = clean(seg)
        if not body or len(body) < 40:
            continue
        st = float(star.group(1)) if star else None
        out.append({"src": "amazon-review", "asin": asin,
                    "stars": st,
                    "kind": "critical" if (st or 5) <= 3 else "positive",
                    "who": who.group(1) if who else None,
                    "title": clean(title.group(1))[:150] if title else None,
                    "text": body[:1500],
                    "helpful": int((helpf.group(1).replace(",", "") if helpf and helpf.group(1) != "One" else "1")) if helpf else 0})
    return out


def main():
    slug = sys.argv[1]
    terms = sys.argv[2:]
    d = f"offers/{slug}/research/data"
    os.makedirs(d, exist_ok=True)
    listings, related = [], set()
    for t in terms:
        L, R = search(t)
        listings += L
        related.update(R)
        print(f"'{t}': {len(L)} listings")
        time.sleep(2)
    with open(f"{d}/amazon-listings.jsonl", "w") as f:
        for r in listings:
            f.write(json.dumps(r) + "\n")
    json.dump(sorted(related), open(f"{d}/amazon-related-searches.json", "w"), indent=1)

    # rank the shelf: who actually owns this category
    byasin = {}
    for r in listings:
        byasin.setdefault(r["asin"], r)
    def _v(x):
        v=(x.get("sold_past_month") or "0").replace("+","").replace(",","")
        mult=1000 if v.endswith("K") else (1000000 if v.endswith("M") else 1)
        try: return float(v.rstrip("KM"))*mult
        except: return 0.0
    ranked = sorted(byasin.values(), key=lambda r: (-_v(r), -int(r["reviews"] or 0)))
    print("\n=== THE SHELF (who the competitors actually are) ===")
    for r in ranked[:14]:
        print(f"  {(r['reviews'] or '?'):>7s} rev  {(r['rating'] or '?'):>4s}*  "
              f"${(r['price'] or '?'):>7s}  {(r['sold_past_month'] or '-'):>6s}/mo  {r['title'][:60]}")

    # reviews on the top sellers
    allrev = []
    for r in ranked[:8]:
        rv = reviews(r["asin"])
        for x in rv:
            x["product"] = r["title"][:70]
        allrev += rv
        time.sleep(2)
    with open(f"{d}/amazon-reviews.jsonl", "w") as f:
        for r in allrev:
            f.write(json.dumps(r) + "\n")
    print(f"\nreviews pulled: {len(allrev)}")
    print(f"related searches captured: {len(related)}")
    neg = sorted([r for r in allrev if r["kind"] == "critical"], key=lambda r: -r["helpful"])
    pos = sorted([r for r in allrev if r["kind"] == "positive"], key=lambda r: -r["helpful"])
    print("\n=== MOST-HELPFUL NEGATIVES (where the angle hides) ===")
    for r in neg[:8]:
        print(f"  [{r['helpful']:>4} helpful | {r['stars']}*] {r['title']}")
        print(f"      {r['text'][:220]}")
    print("\n=== MOST-HELPFUL POSITIVES (what they credit) ===")
    for r in pos[:6]:
        print(f"  [{r['helpful']:>4} helpful | {r['stars']}*] {r['title']}")
        print(f"      {r['text'][:200]}")


if __name__ == "__main__":
    main()
