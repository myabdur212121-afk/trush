# Binomial Theorem — সংখ্যাগুলো আসলে কোথা থেকে আসে?

বাংলা narration সহ ~৩৩ মিনিটের Manim ভিডিও project।

## Folder

```
binomial_theorem/
├── 03_polished_by_claude.md   # মূল narration স্ক্রিপ্ট (anim hint সহ)
├── project/                   # ভিডিওর কোড
│   ├── common.py              # রং, ফন্ট, Narrated mixin, chapter title helper
│   ├── part1.py … part4.py    # Part1–Part4 scene (Intro / Combination / Binomial / Pascal + Summary + outro)
│   ├── narration/             # ৫৮টা বলার-রূপ টেক্সট (TTS-এ হুবহু এটাই ব্যবহার হয়েছে)
│   ├── audio/                 # ৫৮টা narration mp3 + intro/title/outro music + pause ফাইল
│   ├── build_all.sh           # পুরো pipeline: ৪ part render → জোড়া → output/*.mp4
│   ├── make_music.py, pauses.sh, tools/grid.py
├── practice/
│   ├── index.html             # মোবাইলে স্ক্রিপ্ট পড়ার ওয়েবসাইট (অফলাইন, ফন্ট embedded)
│   ├── build.py
│   └── pdf/                   # প্রিন্টের PDF (XeLaTeX · Noto Serif Bengali + CMU Serif)
│       ├── Narration_Script.pdf / .tex
│       └── build_pdf.py
└── scripts/
    ├── setup_manim.sh         # apt (TeX, cairo, pango, ffmpeg) + manim + ফন্ট
    └── font.sh                # Noto Serif Bengali + CMU Serif install
```

## Render

```bash
bash scripts/setup_manim.sh          # একবার
cd project && bash build_all.sh      # -qm = 720p30; final: -qh / 1080p60
```

- Manim Community v0.21.0 · background `#0B1736` · ফন্ট: বাংলা Noto Serif Bengali, English CMU Serif
- লোগো/চ্যানেলের নাম: `common.py` → `LOGO_FILE`, `CHANNEL_NAME`

> ⚠️ কিছু স্ক্রিপ্টে path `/home/user/...` ধরে লেখা (`scripts/setup_manim.sh`, `practice/build.py`, `practice/pdf/build_pdf.py`)।
> অন্য জায়গায় চালালে ওই path বদলে নিন।

রেন্ডার করা ভিডিও (`project/output/`) repo-তে রাখা হয়নি — কোড থেকে আবার বানানো যায়।
