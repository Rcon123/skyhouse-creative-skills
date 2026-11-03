#!/bin/zsh
# House lander deploy gate. Usage: tools/landers/deploy.sh <local folder> <bucket prefix host-folder> <variant> <public host>
# e.g. tools/landers/deploy.sh offers/reactivate/landers/salt-longform reactivate-info.themodernamerican.org salt-longform info.themodernamerican.org
# 10-15: image globs now include relative subfolders (images/x.webp); the old [^"/:] pattern silently skipped them and the live check passed vacuously.
# Refuses to upload unless every CTA is the bare RedTrack click link, no tracking tags are baked in, no dashes, every referenced image exists.
set -e
DIR="$1"; HOSTDIR="$2"; VARIANT="$3"; PUB="$4"
[[ -z "$DIR" || -z "$HOSTDIR" || -z "$VARIANT" || -z "$PUB" ]] && { echo "usage: deploy.sh <dir> <bucket host folder> <variant> <public host>"; exit 2 }
WS="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$WS/$DIR" || exit 2
python3 "$WS/tools/landers/gate.py" advertorial.html || { echo "GATE FAILED. Nothing uploaded."; exit 1 }
export $(grep -E '^(CLOUDFLARE_API_TOKEN|CLOUDFLARE_ACCOUNT_ID)=' "$WS/.env" | xargs)
P="landers-prod/$HOSTDIR/$VARIANT"
for f in advertorial.html _headers; do [[ -f $f ]] || continue; ct=text/html; [[ $f == _headers ]] && ct=text/plain
  npx wrangler r2 object put "$P/$f" --file=$f --content-type="$ct" --remote 2>&1 | tail -1; done
for f in $(grep -o 'src="[^":]*\.\(jpg\|jpeg\|png\|webp\)"' advertorial.html | sed 's/src="//;s/"//;s#^\./##' | grep -v '^/' | sort -u); do
  ct=image/jpeg; [[ $f == *.webp ]] && ct=image/webp; [[ $f == *.png ]] && ct=image/png
  npx wrangler r2 object put "$P/$f" --file=$f --content-type="$ct" --remote 2>&1 | tail -1; done
sleep 4
U="https://$PUB/$VARIANT/advertorial.html"
curl -s "$U" -o /tmp/_live.html -w "live page %{http_code}\n"
ctl=(); [[ -n "$CONTROL" ]] && ctl=(--control "$CONTROL")
python3 "$WS/tools/landers/gate.py" /tmp/_live.html --live "${ctl[@]}" || { echo "LIVE PAGE FAILED THE GATE: $U (set CONTROL=<live control url> to compare tag counts with the control instead of 1)"; exit 1 }
for f in $(grep -o 'src="[^":]*\.\(jpg\|jpeg\|png\|webp\)"' /tmp/_live.html | sed 's/src="//;s/"//;s#^\./##' | grep -v '^/' | sort -u); do
  c=$(curl -s -o /dev/null -w "%{http_code}" "https://$PUB/$VARIANT/$f"); [[ $c == 200 ]] || { echo "IMAGE $f -> $c"; exit 1 }; done
echo "DEPLOYED AND VERIFIED: $U"
echo "Last step (manual, browser): open $U?rtkcid=test and confirm every href reads trk.skatrk02.com/click?clickid=test"
