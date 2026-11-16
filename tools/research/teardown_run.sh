#!/bin/bash
# Download top video clusters, transcribe the opening 15s (the real video hook)
# and the full audio, and pull inner frames at 15/45/80%.
# Usage: teardown_run.sh <data-dir> <out-dir> <swipes-dir> [max]
set -u
DATA="$1"; OUT="$2"; SW="$3"; MAX="${4:-8}"
MODEL="$HOME/.cache/whisper-models/ggml-base.en.bin"
mkdir -p "$OUT" "$SW" /tmp/td
python3 - "$DATA/_top_videos.json" "$MAX" <<'PY' > /tmp/td/list.tsv
import json,sys
rows=json.load(open(sys.argv[1]))[:int(sys.argv[2])]
for r in rows:
    print("\t".join([r["slug"], str(r["copies"]), str(r["live"]), r["url"], r.get("prev") or "", str(r["dur"])]))
PY
while IFS=$'\t' read -r slug copies live url prev dur; do
  [ -z "$url" ] && continue
  base="${copies}cp-${slug}"
  mp4="/tmp/td/$base.mp4"
  if [ -f "$OUT/HOOK-$base.txt" ]; then echo "=== $base (already done) ==="; continue; fi
  echo "=== $base (${dur}s, $live live) ==="
  curl -s -L --max-time 180 -o "$mp4" "$url" || { echo "  download failed"; continue; }
  sz=$(stat -f%z "$mp4" 2>/dev/null || echo 0)
  [ "$sz" -lt 10000 ] && { echo "  too small ($sz)"; continue; }
  # opening 15 seconds = the video hook
  ffmpeg -nostdin -loglevel error -y -i "$mp4" -t 15 -ar 16000 -ac 1 "/tmp/td/$base-open.wav" 2>/dev/null
  # full audio
  ffmpeg -nostdin -loglevel error -y -i "$mp4" -ar 16000 -ac 1 "/tmp/td/$base-full.wav" 2>/dev/null
  if [ -f "/tmp/td/$base-open.wav" ]; then
    whisper-cli -m "$MODEL" -f "/tmp/td/$base-open.wav" -nt -np 2>/dev/null \
      | tr -s ' \n' ' ' > "$OUT/HOOK-$base.txt"
    echo "  hook: $(head -c 150 "$OUT/HOOK-$base.txt")"
  fi
  if [ -f "/tmp/td/$base-full.wav" ]; then
    whisper-cli -m "$MODEL" -f "/tmp/td/$base-full.wav" -nt -np 2>/dev/null \
      > "$OUT/FULL-$base.txt"
    echo "  full: $(wc -w < "$OUT/FULL-$base.txt") words"
  fi
  # inner frames at 15/45/80%
  for pct in 15 45 80; do
    t=$(python3 -c "print(max(1,round($dur*$pct/100,1)))")
    ffmpeg -nostdin -loglevel error -y -ss "$t" -i "$mp4" -frames:v 1 -vf scale=360:-1 \
      "/tmp/td/$base-f$pct.jpg" 2>/dev/null
  done
  if ls /tmp/td/$base-f*.jpg >/dev/null 2>&1; then
    ffmpeg -nostdin -loglevel error -y -pattern_type glob -i "/tmp/td/$base-f*.jpg" \
      -filter_complex tile=3x1 "$SW/frames-$base.jpg" 2>/dev/null && echo "  frames -> frames-$base.jpg"
  fi
  rm -f "$mp4" "/tmp/td/$base-open.wav" "/tmp/td/$base-full.wav"
done < /tmp/td/list.tsv
echo "DONE"
