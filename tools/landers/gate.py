"""Lander gate. python3 gate.py advertorial.html [--live]. Exit 1 on any failure."""
import re,sys,os
p=sys.argv[1]; live='--live' in sys.argv; s=open(p,errors='ignore').read(); bad=[]
hrefs=[h for h in re.findall(r'<a[^>]+href="([^"]+)"',s) if not h.startswith(('https://fonts.g','#','mailto'))]
for h in hrefs:
    if h!='https://trk.skatrk02.com/click': bad.append(f'CTA href is not the bare RedTrack link: {h}')
if not hrefs: bad.append('no CTA links found')
if re.search(r'[—–]|&mdash;|&ndash;',s): bad.append('em/en dash present')
if not live:
    if 'clarity.ms' in s or 'unilpclick' in s: bad.append('tracking tag baked into stored HTML (router injects both on this host)')
    for f in sorted(set(re.findall(r'src="([^"/:]+\.(?:jpg|jpeg|png|webp))"',s))):
        fp=os.path.join(os.path.dirname(p) or '.',f)
        if not os.path.exists(fp): bad.append(f'missing image file {f}')
        elif os.path.getsize(fp)>115000: bad.append(f'{f} is {os.path.getsize(fp)//1024}KB (over 110KB)')
else:
    # Expected injected-tag counts: 1 each by default, or whatever the live CONTROL page carries when
    # --control <url> is given (10-22: the router on info.americanhealthjournal.org started injecting a
    # second unilpclick tag on every page, so a fixed 1 fails pages that match their control exactly).
    exp_c,exp_u=1,1
    if '--control' in sys.argv:
        import urllib.request
        cu=sys.argv[sys.argv.index('--control')+1]
        try:
            c=urllib.request.urlopen(urllib.request.Request(cu,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read().decode('utf8','ignore')
            exp_c,exp_u=c.count('clarity.ms/tag'),c.count('unilpclick'); print(f'control {cu}: clarity {exp_c}, unilpclick {exp_u}')
        except Exception as e: bad.append(f'could not fetch control {cu}: {e}')
    if s.count('clarity.ms/tag')!=exp_c: bad.append(f"clarity tag count {s.count('clarity.ms/tag')} (expect {exp_c})")
    if s.count('unilpclick')!=exp_u: bad.append(f"unilpclick count {s.count('unilpclick')} (expect {exp_u})")
for b in bad: print('FAIL:',b)
print('GATE PASS' if not bad else f'{len(bad)} failure(s)'); sys.exit(1 if bad else 0)
