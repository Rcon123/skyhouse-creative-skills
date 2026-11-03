#!/usr/bin/env python3
"""Kie.ai client for the one-shot video pipeline.

Stdlib + curl only, so it runs under any python3. Every call is appended to a
JSONL log (model, input, task id, state, credits spent, seconds) so a project
is a record of what was tried.

  from kie import Kie
  k = Kie(log="project/kie_log.jsonl")
  url = k.upload("frame.png")                 # cached by file hash for 20h
  res = k.run("kling/ai-avatar-pro", {...}, dest="clips/s01.mp4")

CLI:
  python3 kie.py credits
  python3 kie.py upload FILE
  python3 kie.py info TASK_ID
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(HERE, "..", ".."))
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
UA = "Mozilla/5.0"
UPLOAD_TTL = 20 * 3600          # Kie keeps uploads at least 24h; re-upload after 20h
CREDIT_USD = 0.005


def _env():
    env = dict(os.environ)
    path = os.path.join(WORKSPACE, ".env")
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env.setdefault(k, v.strip().strip('"').strip("'"))
    return env


class KieError(RuntimeError):
    pass


class Kie:
    def __init__(self, log=None, cache=None):
        self.key = _env().get("KIE_API_KEY")
        if not self.key:
            raise KieError("KIE_API_KEY not found in .env")
        self.log_path = log
        self.cache_path = cache or os.path.join(HERE, ".upload_cache.json")

    # ---------- low level ----------
    def _req(self, url, body=None, timeout=120):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, headers={
            "Authorization": f"Bearer {self.key}", "Content-Type": "application/json",
            "User-Agent": UA})
        for attempt in range(5):
            try:
                return json.load(urllib.request.urlopen(req, timeout=timeout))
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code >= 500:
                    time.sleep(3 * (attempt + 1))
                    continue
                raise KieError(f"HTTP {e.code}: {e.read()[:300]!r}")
            except (urllib.error.URLError, TimeoutError):
                time.sleep(3 * (attempt + 1))
        raise KieError(f"request failed after retries: {url}")

    def _log(self, row):
        if not self.log_path:
            return
        os.makedirs(os.path.dirname(os.path.abspath(self.log_path)), exist_ok=True)
        row["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a") as fh:
            fh.write(json.dumps(row) + "\n")

    def credits(self):
        return self._req(f"{API}/chat/credit").get("data")

    # ---------- files ----------
    def upload(self, path, folder="video-pipeline"):
        """Upload a local file, return a URL Kie models accept. Cached by content hash."""
        # The stream endpoint drops files of about 5 MB and up. Big stills go up as JPEG.
        if os.path.getsize(path) > 4_000_000 and path.lower().endswith((".png", ".webp", ".jpg", ".jpeg")):
            small = os.path.splitext(path)[0] + "_up.jpg"
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", path, "-q:v", "3", small], check=True, stdin=subprocess.DEVNULL)
            path = small
        h = hashlib.sha1(open(path, "rb").read()).hexdigest()
        cache = {}
        if os.path.exists(self.cache_path):
            try:
                cache = json.load(open(self.cache_path))
            except ValueError:
                cache = {}
        hit = cache.get(h)
        if hit and time.time() - hit["t"] < UPLOAD_TTL:
            return hit["url"]
        name = f"{h[:12]}{os.path.splitext(path)[1].lower()}"
        url, out = None, ""
        for attempt in range(4):            # the upload host drops a request now and then; retry before giving up
            out = subprocess.run(
                ["curl", "-s", "-m", "300", "-X", "POST", UPLOAD, "-A", UA,
                 "-H", f"Authorization: Bearer {self.key}",
                 "-F", f"file=@{path}", "-F", f"uploadPath={folder}", "-F", f"fileName={name}"],
                capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout
            try:
                d = json.loads(out).get("data") or {}
                url = d.get("downloadUrl") or d.get("fileUrl")
            except ValueError:
                url = None
            if url:
                break
            time.sleep(2 + 2 * attempt)
        if not url:
            raise KieError(f"upload failed after retries: {out[:300]}")
        cache[h] = {"url": url, "t": time.time(), "file": os.path.basename(path)}
        json.dump(cache, open(self.cache_path, "w"), indent=1)
        return url

    @staticmethod
    def download(url, dest):
        os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
        subprocess.run(["curl", "-s", "-L", "-m", "600", "-A", UA, "-o", dest, url], check=True, stdin=subprocess.DEVNULL)
        if not os.path.exists(dest) or os.path.getsize(dest) < 200:
            raise KieError(f"download came back empty: {url}")
        return dest

    # ---------- tasks ----------
    def create(self, model, inp):
        d = self._req(f"{API}/jobs/createTask", {"model": model, "input": inp})
        tid = (d.get("data") or {}).get("taskId")
        if not tid:
            self._log({"model": model, "input": inp, "state": "rejected", "msg": d.get("msg"), "code": d.get("code")})
            raise KieError(f"{model} rejected: {d.get('code')} {d.get('msg')}")
        return tid

    def info(self, tid):
        return self._req(f"{API}/jobs/recordInfo?taskId={tid}", timeout=60).get("data") or {}

    def wait(self, tid, timeout=1500, every=8):
        t0 = time.time()
        while time.time() - t0 < timeout:
            d = self.info(tid)
            st = d.get("state")
            if st == "success":
                res = json.loads(d.get("resultJson") or "{}")
                urls = res.get("resultUrls") or []
                if not urls and isinstance(res.get("data"), list):      # Suno returns a list of takes
                    urls = [x.get("audio_url") for x in res["data"] if x.get("audio_url")]
                return {"state": "success", "urls": urls, "result": res, "raw": d}
            if st == "fail":
                return {"state": "fail", "msg": d.get("failMsg"), "code": d.get("failCode"), "raw": d}
            time.sleep(every)
            every = min(every + 2, 20)
        return {"state": "timeout", "raw": {}}

    def run(self, model, inp, dest=None, timeout=1500, tag=None, task_id=None, on_submit=None):
        """Create (or resume task_id), wait, download. Returns dict with state, files, urls, result.

        The task id is logged and handed to on_submit the moment Kie accepts the job, because
        Kie charges at submit: a run that dies while waiting can pick the same task back up
        instead of paying twice."""
        t0 = time.time()
        tid = task_id or self.create(model, inp)
        if not task_id:
            self._log({"tag": tag, "model": model, "taskId": tid, "state": "submitted"})
            if on_submit:
                on_submit(tid)
        out = self.wait(tid, timeout=timeout)
        out["taskId"] = tid
        out["files"] = []
        if out["state"] == "success" and dest:
            urls = out["urls"]
            for i, u in enumerate(urls):
                base, ext = os.path.splitext(dest)
                path = dest if i == 0 else f"{base}_{i}{ext}"
                out["files"].append(self.download(u, path))
        raw = out.get("raw") or {}
        self._log({"tag": tag, "model": model, "input": inp, "taskId": tid, "state": out["state"],
                   "msg": out.get("msg"), "files": out["files"], "resumed": bool(task_id),
                   "credits": raw.get("creditsConsumed", raw.get("consumeCredits")),
                   "seconds": round(time.time() - t0, 1)})
        return out


if __name__ == "__main__":
    k = Kie()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "credits"
    if cmd == "credits":
        c = k.credits()
        print(f"{c} credits (about ${float(c) * CREDIT_USD:.2f})")
    elif cmd == "upload":
        print(k.upload(sys.argv[2]))
    elif cmd == "info":
        print(json.dumps(k.info(sys.argv[2]), indent=2))
