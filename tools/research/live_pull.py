#!/usr/bin/env python3
"""Pull an offer's LIVE picture: RedTrack campaigns/landers/offer URLs + Meta active creative.

Usage: python3 tools/research/live_pull.py <TAG> <slug> [step]
  step: rt | meta | all   (default all)
"""
import json,sys,os,urllib.parse,urllib.request,datetime,time,re
WS="/Users/ryanconnolly/SkyHouse Exodus"
env={}
for line in open(f"{WS}/.env"):
    line=line.strip()
    if line and not line.startswith("#") and "=" in line: k,v=line.split("=",1); env[k]=v
RT=env["REDTRACK_API_KEY"]; TOK=env["META_ACCESS_TOKEN"]
TAG=sys.argv[1]; SLUG=sys.argv[2]; STEP=sys.argv[3] if len(sys.argv)>3 else "all"
OUT=f"{WS}/offers/{SLUG}/research"; os.makedirs(f"{OUT}/data",exist_ok=True)
os.makedirs(f"{OUT}/swipes/live",exist_ok=True); os.makedirs(f"{OUT}/teardowns",exist_ok=True)
today=datetime.date.today(); since=today-datetime.timedelta(days=7)

def rtget(**p):
    p["api_key"]=RT
    url="https://api.redtrack.io/report?"+urllib.parse.urlencode(p)
    for a in range(4):
        try:
            with urllib.request.urlopen(url,timeout=300) as r: return json.load(r)
        except Exception as e: time.sleep(8)
    return []
def rtlist(ep):
    out=[];page=1
    while True:
        u=f"https://api.redtrack.io/{ep}?"+urllib.parse.urlencode({"api_key":RT,"per":500,"page":page})
        try:
            with urllib.request.urlopen(u,timeout=180) as r: d=json.load(r)
        except Exception: break
        rows=d if isinstance(d,list) else d.get("items") or []
        out+=rows
        if len(rows)<500: break
        page+=1
        if page>20: break
    return out
def fb(url):
    for a in range(6):
        try:
            with urllib.request.urlopen(url,timeout=300) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if a==5: return {"ERR":e.read().decode()[:200]}
            time.sleep(8*(a+1))
        except Exception: time.sleep(8*(a+1))
    return {"ERR":"retries"}
def fbpage(path,**p):
    p["access_token"]=TOK
    url=f"https://graph.facebook.com/v21.0/{path}?"+urllib.parse.urlencode(p)
    out=[]
    while url:
        d=fb(url)
        if "ERR" in d: print("  meta err",d["ERR"][:150]); break
        out+=d.get("data",[])
        url=(d.get("paging") or {}).get("next")
    return out
R=lambda r: r.get("total_revenue") or 0

if STEP in ("rt","all"):
    print(f"== RedTrack live pull for {TAG} ({since} to {today})")
    rows=[];page=1
    while True:
        b=rtget(group="campaign",date_from=str(since),date_to=str(today),per=500,page=page,timezone="America/New_York")
        b=b if isinstance(b,list) else b.get("items") or []
        rows+=b
        if len(b)<500: break
        page+=1
    h=[r for r in rows if TAG in (r.get("campaign") or "") and (r.get("cost") or 0)>0]
    h.sort(key=lambda r:-(r["cost"]))
    c=sum(r["cost"] for r in h); rv=sum(R(r) for r in h)
    print(f"   live campaigns: {len(h)}   spend ${c:,.0f}   revenue ${rv:,.0f}   ROAS {rv/c if c else 0:.2f}")
    for r in h[:25]: print(f"     ${r['cost']:>8,.0f}  {R(r)/r['cost'] if r['cost'] else 0:>5.2f}  {r['campaign']}")
    json.dump(h,open(f"{OUT}/data/rt-live-7d.json","w"),indent=1)
    # landers
    d=rtget(group="campaign,landing",date_from=str(since),date_to=str(today),per=1000,page=1,timezone="America/New_York")
    d=d if isinstance(d,list) else d.get("items") or []
    hl=[r for r in d if TAG in (r.get("campaign") or "") and (r.get("cost") or 0)>0]
    from collections import defaultdict
    agg=defaultdict(lambda:[0,0,0])
    for r in hl:
        k=r.get("landing") or "?"; a=agg[k]; a[0]+=r["cost"]; a[1]+=R(r); a[2]+=r.get("conversions") or 0
    print("   LIVE LANDERS:")
    for k,(cc,rr,cv) in sorted(agg.items(),key=lambda x:-x[1][0]):
        print(f"     ${cc:>8,.0f}  {rr/cc if cc else 0:>5.2f}  {cv:>4.0f} conv   {k}")
    json.dump(hl,open(f"{OUT}/data/rt-live-landers-7d.json","w"),indent=1)
    # offer + landing url catalog
    offs=rtlist("offers"); lands=rtlist("landings")
    mo=[o for o in offs if TAG in (o.get("title") or "")]
    ml=[l for l in lands if TAG.lower() in ((l.get("title") or "")+" "+(l.get("url") or "")).lower()]
    print("   OFFER URLS (the destination / VSL):")
    for o in mo: print(f"     [{o.get('status')}] {o.get('title')}\n         {o.get('url')}")
    json.dump({"offers":mo,"landings":ml},open(f"{OUT}/data/rt-catalog.json","w"),indent=1)
    print(f"   landing records in tracker: {len(ml)}")
    # fb ad ids
    d=rtget(group="campaign,sub1",date_from=str(since),date_to=str(today),per=1000,page=1,timezone="America/New_York")
    d=d if isinstance(d,list) else d.get("items") or []
    ids=[r for r in d if TAG in (r.get("campaign") or "") and (r.get("cost") or 0)>0]
    ids.sort(key=lambda r:-(r["cost"]))
    json.dump(ids,open(f"{OUT}/data/rt-live-adids.json","w"),indent=1)
    if ids:
        top=ids[0]["sub1"]
        info=fb(f"https://graph.facebook.com/v21.0/{top}?"+urllib.parse.urlencode({"fields":"account_id,name,campaign{name}","access_token":TOK}))
        print(f"   META ACCOUNT: act_{info.get('account_id')}   (via ad {top})")
        json.dump(info,open(f"{OUT}/data/meta-account-probe.json","w"),indent=1)

if STEP in ("meta","all"):
    probe=json.load(open(f"{OUT}/data/meta-account-probe.json"))
    ACT="act_"+str(probe.get("account_id"))
    print(f"\n== Meta live creative pull for {ACT}")
    fields=("id,name,status,effective_status,created_time,adset{name,id},campaign{name,id,objective},"
            "creative{id,name,title,body,link_url,call_to_action_type,image_url,thumbnail_url,video_id,"
            "object_story_spec,asset_feed_spec,effective_object_story_id}")
    ads=fbpage(f"{ACT}/ads",fields=fields,limit=200,effective_status=json.dumps(["ACTIVE"]))
    print("   active ads:",len(ads))
    json.dump(ads,open(f"{OUT}/data/meta-active-ads.json","w"),indent=1)
    from collections import Counter,defaultdict
    camps=Counter((a.get("campaign") or {}).get("name","?") for a in ads)
    print("   active campaigns:")
    for c,n in camps.most_common(12): print(f"     {n:>4} ads  {c}")
    ins=fbpage(f"{ACT}/insights",level="ad",
        fields="ad_id,ad_name,adset_name,campaign_name,spend,impressions,clicks,ctr,cpm,actions,action_values",
        time_range=json.dumps({"since":str(since),"until":str(today)}),limit=200)
    json.dump(ins,open(f"{OUT}/data/meta-insights-7d.json","w"),indent=1)
    print(f"   insight rows {len(ins)}   spend ${sum(float(r.get('spend') or 0) for r in ins):,.0f}")
    def num(r,keys,kind="actions"):
        for a in (r.get(kind) or []):
            if a.get("action_type") in keys: return float(a.get("value") or 0)
        return 0.0
    P={"purchase","omni_purchase","offsite_conversion.fb_pixel_purchase"}
    agg=defaultdict(lambda:{"spend":0,"imp":0,"clicks":0,"purch":0,"val":0})
    for r in ins:
        a=agg[r.get("ad_name") or "?"]
        a["spend"]+=float(r.get("spend") or 0); a["imp"]+=float(r.get("impressions") or 0)
        a["clicks"]+=float(r.get("clicks") or 0); a["purch"]+=num(r,P); a["val"]+=num(r,P,"action_values")
    byname={}
    for a in ads:
        if a.get("name") in agg and a["name"] not in byname: byname[a["name"]]=a
    det={}
    for n,v in sorted(agg.items(),key=lambda x:-x[1]["spend"]):
        a=byname.get(n); c=(a or {}).get("creative") or {}
        oss=c.get("object_story_spec") or {}; afs=c.get("asset_feed_spec") or {}
        titles=[t.get("text") for t in (afs.get("titles") or [])]
        bodies=[b.get("text") for b in (afs.get("bodies") or [])]
        vids=[x.get("video_id") for x in (afs.get("videos") or [])]
        imgs=[x.get("url") or x.get("image_url") for x in (afs.get("images") or [])]
        link=oss.get("link_data") or {}; vd=oss.get("video_data") or {}
        det[n]={"spend7d":round(v["spend"]),"roas_meta":round(v["val"]/v["spend"],2) if v["spend"] else 0,
          "purchases":v["purch"],"impressions":v["imp"],
          "ctr":round(100*v["clicks"]/v["imp"],2) if v["imp"] else 0,
          "headline":c.get("title") or link.get("name") or vd.get("title") or (titles[0] if titles else None),
          "headlines_all":titles or None,
          "body":c.get("body") or link.get("message") or vd.get("message") or (bodies[0] if bodies else None),
          "video_id":c.get("video_id") or vd.get("video_id") or (vids[0] if vids else None),
          "image_url":c.get("image_url") or link.get("picture") or (imgs[0] if imgs else None),
          "thumbnail_url":c.get("thumbnail_url"),"link_url":c.get("link_url") or link.get("link"),
          "cta":c.get("call_to_action_type") or (link.get("call_to_action") or {}).get("type"),
          "post_id":c.get("effective_object_story_id"),"ad_id":(a or {}).get("id")}
    json.dump(det,open(f"{OUT}/data/live-creative-detail.json","w"),indent=1)
    tot=sum(v["spend7d"] for v in det.values())
    nv=sum(1 for v in det.values() if v.get("video_id"))
    print(f"   DISTINCT LIVE CREATIVES: {len(det)}  (videos {nv}, images {len(det)-nv})  total ${tot:,.0f}")
    print(f"   {'SPEND':>8} {'CTR%':>6} {'PUR':>4}  NAME | HEADLINE")
    for n,v in list(det.items())[:20]:
        print(f"   {v['spend7d']:>8,} {v['ctr']:>6.2f} {v['purchases']:>4.0f}  {n[:40]:<40} | {str(v['headline'])[:60]}")
