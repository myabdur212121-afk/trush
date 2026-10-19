#!/usr/bin/env bash
# full rebuild: setup -> outro music -> 720p render of all parts -> concat -> compress -> clean
cd ~/project
mkdir -p output
which manim >/dev/null 2>&1 || bash ~/scripts/setup_manim.sh > /tmp/setup.log 2>&1
echo "SETUP done: $(which manim)"
# 5 s outro sting cut from the intro music (fade in 0.6 s, fade out over the last 2 s)
ffmpeg -v error -y -i audio/music_intro.wav -t 5 -af "afade=t=in:d=0.6,afade=t=out:st=3:d=2" audio/music_outro.wav
for p in 1 2 3 4; do
  manim -qm --disable_caching part$p.py Part$p > /tmp/r$p.log 2>&1; echo "PART$p EXIT=$?"
  rm -rf media/videos/part$p/720p30/partial_movie_files
done
ls media/videos/part*/720p30/Part*.mp4 | sed "s/^/file '$(pwd | sed 's/\//\\\//g')\//; s/$/'/" > /tmp/list.txt
ffmpeg -v error -y -f concat -safe 0 -i /tmp/list.txt -c copy /tmp/joined.mp4
echo "CONCAT EXIT=$?"
D=$(ffprobe -v error -select_streams v -show_entries stream=duration -of csv=p=0 /tmp/joined.mp4)
ffmpeg -v error -y -i /tmp/joined.mp4 -c:v copy -af apad -c:a aac -b:a 192k -t "$D" -movflags +faststart \
  output/Binomial_Theorem_full_720p.mp4
echo "FINAL EXIT=$? duration=$D"
if [ -s output/Binomial_Theorem_full_720p.mp4 ]; then
  rm -f /tmp/joined.mp4
  rm -rf media __pycache__ ~/fonts
else
  echo "FINAL FILE MISSING - keeping media/ and /tmp/joined.mp4"
fi
ls -la output
echo ALLDONE
