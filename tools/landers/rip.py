"""Rip a live client lander into a static house page.

python3 tools/landers/rip.py <url> <outdir> [--cta-match substr ...] [--keep-root selector-id]

What it does:
- fetches the page, deletes every <script>, <noscript>, <iframe> and inline on* handler
  (their GTM, pixels, funnel JS, Shopify kit, Klaviyo, Judge.me, TikTok)
- downloads every image (src, data-src, srcset, inline style url()) into <outdir>/images/ and rewrites the reference
- downloads external stylesheets into <outdir>/css/ and makes the url() references inside them absolute
- CTA rule: an <a> whose href contains any --cta-match substring, or any element that carried
  onclick="linkMethod(event)" / class fk-post-button (Checkout Champ funnels), becomes an <a href=CLICK>
- every other href becomes "#", so no click leaks to the client's site
- writes <outdir>/advertorial.html and <outdir>/RIP-NOTES.md
Stored HTML carries no tracking tags; the landers-router Worker injects Clarity + unilpclick on serve.
"""
import re, sys, os, hashlib, urllib.request, urllib.parse, time

CLICK = "https://trk.skatrk02.com/click"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif")

def fetch(u, binary=False):
    d = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    return d if binary else d.decode("utf8", "ignore")

def absolutize(u, base):
    u = u.strip().replace("&amp;", "&")
    if u.startswith("data:") or u.startswith("#") or not u: return u
    if u.startswith("//"): return "https:" + u
    return urllib.parse.urljoin(base, u)

class Store:
    def __init__(self, out):
        self.out = out; self.seen = {}; self.failed = []
    def image(self, u, base):
        a = absolutize(u, base)
        if not a or a.startswith("data:") or a.startswith("#"): return u
        if a in self.seen: return self.seen[a]
        path = urllib.parse.urlparse(a).path
        ext = os.path.splitext(path)[1].lower()
        if ext not in IMG_EXT: ext = ".jpg"
        name = "images/%s_%s%s" % (len(self.seen) + 1, hashlib.md5(a.encode()).hexdigest()[:6], ext)
        try:
            d = fetch(a, True)
            if d[:4] == b"RIFF" and ext != ".webp": name = name[:-len(ext)] + ".webp"
            elif d[:3] == b"\xff\xd8\xff" and ext not in (".jpg", ".jpeg"): name = name[:-len(ext)] + ".jpg"
            elif d[:8] == b"\x89PNG\r\n\x1a\n" and ext != ".png": name = name[:-len(ext)] + ".png"
            open(os.path.join(self.out, name), "wb").write(d)
            self.seen[a] = name
            return name
        except Exception as e:
            self.failed.append((a, str(e)[:80])); self.seen[a] = a; return a
    def css(self, u, base):
        a = absolutize(u, base)
        try:
            c = fetch(a)
        except Exception as e:
            self.failed.append((a, str(e)[:80])); return u
        c = re.sub(r"url\((['\"]?)([^'\")]+)\1\)", lambda m: "url(%s%s%s)" % (m.group(1), absolutize(m.group(2), a), m.group(1)), c)
        c = re.sub(r"@import\s+(['\"])([^'\"]+)\1", lambda m: "@import %s%s%s" % (m.group(1), absolutize(m.group(2), a), m.group(1)), c)
        name = "css/%s_%s.css" % (len(os.listdir(os.path.join(self.out, "css"))) + 1, hashlib.md5(a.encode()).hexdigest()[:6])
        open(os.path.join(self.out, name), "w").write(c)
        return name

def main():
    args = sys.argv[1:]
    url, out = args[0], args[1]
    cta_match = [args[i + 1] for i, a in enumerate(args) if a == "--cta-match"]
    os.makedirs(os.path.join(out, "images"), exist_ok=True); os.makedirs(os.path.join(out, "css"), exist_ok=True)
    st = Store(out)
    s = fetch(url); n_in = len(s)

    # mark funnel CTAs before the handlers are stripped
    s = re.sub(r'<(a|button|div|span)\b([^>]*)onclick="linkMethod\(event\)"', r'<\1 data-rip-cta="1"\2', s)
    s = re.sub(r'<button\b([^>]*class="[^"]*fk-post-button[^"]*")', r'<button data-rip-cta="1"\1', s)

    for tag in ("script", "noscript", "iframe", "template"):
        s = re.sub(r"<%s\b[^>]*>.*?</%s>" % (tag, tag), "", s, flags=re.S | re.I)
    s = re.sub(r"<link[^>]+rel=\"(?:preload|prefetch|preconnect|dns-prefetch|modulepreload|canonical|alternate)\"[^>]*>", "", s, flags=re.I)
    s = re.sub(r'\son[a-z]+="[^"]*"', "", s)
    s = re.sub(r"<meta[^>]+(?:property|name)=\"(?:og:|twitter:|facebook|fb:|google-site)[^\"]*\"[^>]*>", "", s, flags=re.I)
    s = re.sub(r"[—–]", "-", s).replace("&mdash;", "-").replace("&ndash;", "-")

    # stylesheets
    def css_sub(m):
        return m.group(0).replace(m.group(1), st.css(m.group(1), url))
    s = re.sub(r'<link[^>]+rel="stylesheet"[^>]*href="([^"]+)"[^>]*>', css_sub, s, flags=re.I)
    s = re.sub(r'<link[^>]+href="([^"]+)"[^>]*rel="stylesheet"[^>]*>', css_sub, s, flags=re.I)

    # images
    def attr_sub(m):
        return '%s="%s"' % (m.group(1), st.image(m.group(2), url))
    s = re.sub(r'\b(src|data-src|data-lazy-src|data-original|poster|data-bg|data-background)="([^"]+)"', attr_sub, s)
    def srcset_sub(m):
        parts = []
        for p in m.group(2).split(","):
            bits = p.strip().split()
            if not bits: continue
            parts.append(" ".join([st.image(bits[0], url)] + bits[1:]))
        return '%s="%s"' % (m.group(1), ", ".join(parts))
    s = re.sub(r'\b(srcset|data-srcset)="([^"]+)"', srcset_sub, s)
    s = re.sub(r"url\((['\"]?)([^'\")]+)\1\)", lambda m: "url(%s%s%s)" % (m.group(1), st.image(m.group(2), url) if not m.group(2).startswith("data:") else m.group(2), m.group(1)), s)
    # lazy loaders: promote data-src to src when src is a placeholder
    s = re.sub(r'<img\b([^>]*?)\ssrc="(?:data:[^"]*|[^"]*(?:blank|placeholder|lazy|spacer)[^"]*)"([^>]*?)\sdata-src="([^"]+)"', r'<img\1 src="\3"\2 data-src="\3"', s)
    s = re.sub(r'<img\b([^>]*?)\sdata-src="([^"]+)"([^>]*?)\ssrc="(?:data:[^"]*|[^"]*(?:blank|placeholder|lazy|spacer)[^"]*)"', r'<img\1 data-src="\2"\3 src="\2"', s)

    # links
    def href_sub(m):
        tag_open, href = m.group(1), m.group(2)
        is_cta = 'data-rip-cta="1"' in tag_open or any(c in href for c in cta_match)
        return tag_open + 'href="%s"' % (CLICK if is_cta else "#")
    s = re.sub(r'(<a\b[^>]*?)href="([^"]*)"', href_sub, s)
    # funnel buttons/divs/spans with the CTA marker become anchors
    s = re.sub(r'<(button|div|span)\b([^>]*data-rip-cta="1"[^>]*)>(.*?)</\1>',
               lambda m: '<a href="%s" %s>%s</a>' % (CLICK, m.group(2).replace('href=""', ''), m.group(3)), s, flags=re.S)
    s = s.replace('data-rip-cta="1"', "")
    s = re.sub(r'<a\b([^>]*)\shref=""', r'<a\1 href="#"', s)

    open(os.path.join(out, "advertorial.html"), "w").write(s)
    sizes = sorted(((os.path.getsize(os.path.join(out, v)), v) for v in set(st.seen.values()) if v.startswith("images/") and os.path.exists(os.path.join(out, v))), reverse=True)
    ctas = s.count('href="%s"' % CLICK)
    with open(os.path.join(out, "RIP-NOTES.md"), "w") as f:
        f.write("# Rip notes\n\nSource: %s\nFetched: %s\nBytes in: %d, out: %d\nImages: %d (failed %d)\nCSS files: %d\nCTA links to RedTrack: %d\n\n" % (
            url, time.strftime("%Y-%m-%d %H:%M"), n_in, len(s), len([v for v in st.seen.values() if v.startswith("images/")]), len(st.failed), len(os.listdir(os.path.join(out, "css"))), ctas))
        f.write("## Biggest images\n" + "".join("- %dKB %s\n" % (b // 1024, v) for b, v in sizes[:15]))
        if st.failed: f.write("\n## Failed downloads\n" + "".join("- %s (%s)\n" % x for x in st.failed))
    print("wrote %s/advertorial.html  images %d  css %d  ctas %d  failed %d" % (out, len(sizes), len(os.listdir(os.path.join(out, "css"))), ctas, len(st.failed)))

if __name__ == "__main__":
    main()
