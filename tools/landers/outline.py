#!/usr/bin/env python3
# Outline a lander: words per block, every H1/H2, image and button in page order. Run it over Ryan's model page and the live control BEFORE writing a page, and size to them.
# usage: python3 tools/landers/outline.py <one or more .html files>
import re,html,sys
for f in sys.argv[1:]:
    s=open(f,errors='ignore').read()
    s=re.sub(r'<script.*?</script>|<style.*?</style>|<head>.*?</head>','',s,flags=re.S)
    toks=re.split(r'(<h1[^>]*>.*?</h1>|<h2[^>]*>.*?</h2>|<img[^>]*>|<a[^>]*class="[^"]*btn[^"]*"[^>]*>.*?</a>)',s,flags=re.S)
    print('#####',f.split('/')[-1]); total=0; buf=''
    def flush():
        global buf,total
        t=html.unescape(re.sub(r'<[^>]+>',' ',buf)); w=len(t.split()); total+=w
        if w>5: print(f'      [{w} words]')
        buf=''
    for t in toks:
        if t.startswith('<h1') or t.startswith('<h2'):
            flush(); txt=html.unescape(re.sub(r'<[^>]+>','',t)).strip(); txt=re.sub(r'\s+',' ',txt); print(('H1 ' if t.startswith('<h1') else 'H2 ')+txt[:110])
        elif t.startswith('<img'):
            flush(); m=re.search(r'src="([^"]*)"',t); print('   IMG',m.group(1)[:50] if m else '')
        elif t.startswith('<a'):
            flush(); print('   BTN',re.sub(r'<[^>]+>','',t).strip()[:40])
        else: buf+=t
    flush(); print('   TOTAL',total,'words\n')
