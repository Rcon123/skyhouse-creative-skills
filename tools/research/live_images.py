#!/usr/bin/env python3
"""Download live ad images for an offer and build labelled contact sheets."""
import json,os,re,sys,urllib.request
from PIL import Image,ImageDraw,ImageFont
WS="/Users/ryanconnolly/SkyHouse Exodus"; SLUG=sys.argv[1]
OUT=f"{WS}/offers/{SLUG}/research"
det=json.load(open(f"{OUT}/data/live-creative-detail.json"))
os.makedirs(f"{OUT}/swipes/live",exist_ok=True)
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
ok=0;fail=0
for n,v in det.items():
    url=v.get("image_url") or v.get("thumbnail_url")
    if not url: continue
    slug=re.sub(r"[^A-Za-z0-9]+","_",n).strip("_")[:70]
    fn=f"{OUT}/swipes/live/{v['spend7d']:07d}_{slug}.jpg"
    if os.path.exists(fn): ok+=1; continue
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60) as r: open(fn,"wb").write(r.read())
        ok+=1
    except Exception: fail+=1
print(f"{SLUG}: downloaded {ok}, failed {fail}")
files=sorted([f for f in os.listdir(f"{OUT}/swipes/live") if f.endswith(".jpg")],key=lambda p:-int(p[:7]))
# drop tiny video thumbnails from sheets
big=[]
for f in files:
    try:
        if Image.open(f"{OUT}/swipes/live/{f}").size[0]>=300: big.append(f)
    except Exception: pass
try: font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf",20)
except: font=ImageFont.load_default()
def sheet(fs,out,cols=4,cell=430):
    if not fs: return
    rows=(len(fs)+cols-1)//cols; lab=54
    sh=Image.new("RGB",(cols*cell,rows*(cell+lab)),(18,18,20)); d=ImageDraw.Draw(sh)
    for i,f in enumerate(fs):
        im=Image.open(f"{OUT}/swipes/live/{f}").convert("RGB"); im.thumbnail((cell-12,cell-12))
        x=(i%cols)*cell+(cell-im.width)//2; y=(i//cols)*(cell+lab)+6
        sh.paste(im,(x,y))
        ty=(i//cols)*(cell+lab)+cell-4
        d.text(((i%cols)*cell+8,ty),f"${int(f[:7]):,}",fill=(255,214,0),font=font)
        d.text(((i%cols)*cell+8,ty+24),f[8:].replace(".jpg","")[:44],fill=(200,200,205),font=font)
    sh.save(out,quality=86); print("  ",os.path.basename(out),sh.size,f"({len(fs)} images)")
sheet(big[:12],f"{OUT}/swipes/{SLUG}-live-top12.jpg")
if len(big)>12: sheet(big[12:32],f"{OUT}/swipes/{SLUG}-live-next20.jpg")
if len(big)>32: sheet(big[32:60],f"{OUT}/swipes/{SLUG}-live-tail.jpg")
print(f"  usable images (>=300px): {len(big)} of {len(files)}")
