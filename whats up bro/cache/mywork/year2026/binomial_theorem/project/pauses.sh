#!/usr/bin/env bash
# usage: bash pauses.sh audio/p2_*.mp3  -> prints duration + pauses (>=0.3s) per clip
for f in "$@"; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "== $(basename $f) $d"
  ffmpeg -hide_banner -i "$f" -af silencedetect=noise=-35dB:d=0.3 -f null - 2>&1 \
   | grep -o 'silence_\(start\|end\): [0-9.]*' | paste - - \
   | awk '{printf "  %.2f-%.2f (%.2f)\n",$2,$4,$4-$2}'
done
