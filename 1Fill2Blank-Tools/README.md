# 1Fill2Blank Audio–Video Tools

Factorial ভিডিও বানানোর সময় তৈরি করা music, voice–video sync এবং mixing
পদ্ধতিটা এখানে গুছিয়ে রাখা হলো—যাতে পরের ভিডিওতে আবার শুরু থেকে আবিষ্কার
করতে না হয়।

এই package-এর মূল ধারণা তিনটি:

1. **Music code দিয়ে তৈরি** — কোনো download করা বা copyrighted track নয়।
2. **Voice sync scene-এর ভেতর থেকে মাপা** — অনুমান করে timing বসানো নয়;
   Manim নিজে প্রতিটি অংশের শুরু সময় (`marks`) লিখে দেয়।
3. **Music নিজে থেকে voice-এর নিচে নামে** — FFmpeg sidechain ducking;
   কথা থামলে বা logo চললে music ধীরে ধীরে আবার সামনে আসে।

## Folder মানচিত্র

```text
1Fill2Blank-Tools/
├── README.md                  ← তুমি এখানে
├── docs/bn/                   ← বাংলায় বিস্তারিত ব্যাখ্যা
├── tools/
│   ├── make_music.py          ← background/intro/outro music generator
│   ├── manim_sync.py          ← Manim scene-এর mark()/pad() helper
│   ├── compute_pads.py        ← voice অনুযায়ী দরকারি hold হিসাব করে
│   └── mix_voice_music.py     ← voice বসানো + ducking + final MP4
├── music/
│   ├── background/            ← Factorial-এ ব্যবহৃত পুরো background track
│   ├── intro/                 ← ভবিষ্যতের জন্য তৈরি 8s intro
│   └── outro/                 ← ভবিষ্যতের জন্য তৈরি 12s outro
├── templates/                 ← নতুন ভিডিওর জন্য copy করে ভরার ফাইল
├── examples/factorial/        ← শেষ হওয়া Factorial ভিডিওর হুবহু উদাহরণ
└── mobile/                    ← মোবাইল/Termux থেকে নিরাপদে GitHub upload
```

## কোনটা এখানে বানানো, কোনটা বাইরের জিনিস?

| জিনিস | উৎস | এই package-এ কী আছে |
|---|---|---|
| Music generator, pad calculator, mixer, sync patch | Factorial production-এর সময় এই workspace-এ লেখা | reusable রূপ `tools/`-এ; হুবহু original রূপ `examples/factorial/production-scripts-original/`-এ |
| Manim Community (ManimCE), LaTeX, FFmpeg/ffprobe, Python, NumPy | বাইরের open-source software | binary copy রাখা হয়নি; আলাদা install করতে হয় |
| Manim/fonts installer (`manimce.sh`, `font.sh`, `latex_slim.sh`) | তোমার নিজের `manim-sandbox-setup` repo | duplicate করা হয়নি; ওই repo থেকেই ব্যবহার হবে |
| Manim scene ও logo | তোমার `1Fill2Blank` repo | Factorial production scene-এর copy উদাহরণে আছে |
| Bengali voice clip গুলো | এখানে বেছে নেওয়া voice দিয়ে তৈরি | তৈরি clip গুলো আছে; voice তৈরির কোনো local code এখানে নেই—নিজের রেকর্ড করা বা অন্য TTS clip একই নামে রাখলেই বাকি tools চলবে |

## পুরো workflow এক নজরে

```text
script কে segment-এ ভাগ করা
        ↓
প্রতিটি segment-এর voice clip (S01.mp3, S02.mp3, ...)
        ↓
Manim pass 1: কোনো pad ছাড়া render → marks_pass1.json
        ↓
compute_pads.py: কোন দৃশ্যে কত সেকেন্ড বাড়তি hold লাগবে → pad.json
        ↓
Manim pass 2: pad সহ final render → marks_final.json + silent video
        ↓
make_music.py: ঠিক video-র দৈর্ঘ্যের music
        ↓
mix_voice_music.py: mark ধরে voice বসানো → music ducking → loudnorm → final MP4
        ↓
QC: duration, overlap, loudness, silence, কয়েকটা frame
```

## দ্রুত শুরু (নতুন ভিডিও)

নতুন project-এর জন্য একটি কাজের folder বানিয়ে template দুটো copy করো:

```bash
mkdir -p work/my-video/audio
cp templates/project_plan.json work/my-video/
cp templates/narration_segments.json work/my-video/
```

তারপর মূল command গুলো এই আকারে চলবে (path নিজের project অনুযায়ী বদলাবে):

```bash
# ১) pass 1-এর timing দেখে pad হিসাব
python tools/compute_pads.py work/my-video/marks_pass1.json work/my-video/audio work/my-video/pad.json \
  --plan work/my-video/project_plan.json

# ২) pass 2 render-এর পর, ঠিক video-র দৈর্ঘ্যের music
python tools/make_music.py 221.633 work/my-video/background.wav

# ৩) voice + ducked music + final MP4
python tools/mix_voice_music.py \
  --video work/my-video/silent_1080p.mp4 \
  --marks work/my-video/marks_final.json \
  --audio-dir work/my-video/audio \
  --music work/my-video/background.wav \
  --output work/my-video/final.mp4 \
  --plan work/my-video/project_plan.json
```

Manim scene-এ `mark()`/`pad()` কীভাবে বসাতে হয় তা আছে
[`docs/bn/02-voice-video-sync.md`](docs/bn/02-voice-video-sync.md)-এ।

## মোবাইল ব্যবহারকারীর জন্য সবচেয়ে গুরুত্বপূর্ণ কথা

- এই folder টা এই workspace-এই থাকল; পরের ভিডিওর সময় আমাকে বললেই
  আমি এই tools দিয়েই কাজ শুরু করতে পারব—তোমাকে PC লাগবে না।
- স্থায়ী backup হিসেবে GitHub-এ রাখতে চাইলে
  [`docs/bn/04-mobile-github-upload.md`](docs/bn/04-mobile-github-upload.md)
  অনুসরণ করো। সেখানে Termux-এর একটা তৈরি script আছে
  (`mobile/termux_push.sh`); token তোমার ফোনেই থাকবে।
- **Token কখনো chat-এ পাঠাবে না**, repo URL-এর ভেতরে বসাবে না, কোনো
  file-এ লিখে commit করবে না। এই package ব্যবহারের জন্য আমাকে token
  দেওয়ার কোনো দরকার নেই।

## বাংলায় বিস্তারিত

- [Music কীভাবে তৈরি হলো](docs/bn/01-music-system.md)
- [Voice আর video কীভাবে sync হলো](docs/bn/02-voice-video-sync.md)
- [Voice এলে music নিজে থেকে কমে কীভাবে (ducking)](docs/bn/03-ducking-and-mixing.md)
- [মোবাইল থেকে GitHub-এ তোলা](docs/bn/04-mobile-github-upload.md)
- [পরের ভিডিওর checklist ও তৈরি prompt](docs/bn/05-future-video-checklist.md)
- [Factorial উদাহরণ](examples/factorial/README_BN.md)

## Factorial-এ যাচাই হওয়া ফল

- Silent animation: 02:48.7 → voice অনুযায়ী hold যোগ করে final **03:41.6**
- Voice মোট 03:13.9; মোট pad **+53.0s**; প্রতিটি clip পরের অংশ শুরুর আগেই শেষ
- Final: 1920×1080, 30fps, **-15.8 LUFS**, true peak -1.2 dBFS
- এই reusable tools দিয়ে Factorial mix আবার বানিয়ে পরীক্ষা করা হয়েছে;
  ফল একই loudness (-15.8 LUFS) এসেছে।
