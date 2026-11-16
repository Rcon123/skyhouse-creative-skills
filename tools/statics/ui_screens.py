#!/usr/bin/env python3
"""Hand-built phone screens (HTML -> headless Chrome, 1080x1080), because AI cannot fake OS chrome.
notes(out, title, lines)  : iPhone Notes entry.
portal(out, sender, subject, body, when) : patient-portal message (MyChart-style, unbranded)."""
import html, subprocess, os

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def _shot(doc, out):
    out = os.path.abspath(out); hp = out + ".html"; open(hp, "w").write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1080,1080", f"--screenshot={out}", f"file://{hp}"], capture_output=True)
    os.remove(hp); return out


def notes(out, title, lines, when="Today at 1:12 AM"):
    li = "".join(f"<p>{html.escape(l)}</p>" for l in lines)
    doc = f"""<!doctype html><meta charset=utf-8><style>
body{{margin:0;width:1080px;height:1080px;background:#fff;font-family:-apple-system,'SF Pro Text',Helvetica,Arial;overflow:hidden}}
.sb{{height:70px;display:flex;justify-content:space-between;align-items:center;padding:0 48px;font-size:34px;font-weight:600}}
.nav{{height:90px;display:flex;justify-content:space-between;align-items:center;padding:0 36px;color:#e0a800;font-size:40px}}
.d{{text-align:center;color:#8e8e93;font-size:28px;margin:8px 0 26px}}
.b{{padding:0 56px}} h1{{font-size:72px;margin:0 0 30px;font-weight:700}} p{{font-size:54px;line-height:1.3;margin:0 0 16px}}
</style><div class=sb><span>1:12</span><span style='font-size:30px'>5G&nbsp;&nbsp;86%</span></div>
<div class=nav><span>‹ Notes</span><span>⋯&nbsp;&nbsp;Done</span></div><div class=d>{html.escape(when)}</div>
<div class=b><h1>{html.escape(title)}</h1>{li}</div>"""
    return _shot(doc, out)


def portal(out, sender, subject, body, when="May 15, 2026 · 7:42 AM"):
    doc = f"""<!doctype html><meta charset=utf-8><style>
body{{margin:0;width:1080px;height:1080px;background:#f3f5f8;font-family:-apple-system,Helvetica,Arial;overflow:hidden}}
.top{{background:#1d5c96;color:#fff;padding:34px 44px 28px;font-size:40px;font-weight:600}}
.top small{{display:block;font-size:28px;font-weight:400;opacity:.85;margin-top:6px}}
.card{{background:#fff;margin:36px 36px;border-radius:22px;padding:40px 44px;box-shadow:0 2px 6px rgba(0,0,0,.08)}}
.f{{display:flex;align-items:center;gap:22px}}.av{{width:96px;height:96px;border-radius:50%;background:#c9d6e3;flex:none;display:flex;align-items:center;justify-content:center;font-size:40px;color:#1d5c96;font-weight:700}}
.n{{font-size:38px;font-weight:700}}.w{{font-size:28px;color:#6b7785}}.s{{font-size:34px;color:#334;margin:34px 0 18px;font-weight:600}}
.m{{font-size:96px;font-weight:800;color:#13233a;margin:30px 0 10px}}.r{{font-size:30px;color:#6b7785}}
.btn{{margin-top:40px;background:#1d5c96;color:#fff;border-radius:14px;text-align:center;padding:26px;font-size:34px;font-weight:600}}
</style><div class=top>Messages<small>Inbox · 1 new</small></div>
<div class=card><div class=f><div class=av>MD</div><div><div class=n>{html.escape(sender)}</div><div class=w>{html.escape(when)}</div></div></div>
<div class=s>{html.escape(subject)}</div><div class=m>{html.escape(body)}</div><div class=r>Comprehensive metabolic panel, collected May 13, 2026</div>
<div class=btn>View lab results</div></div>"""
    return _shot(doc, out)
