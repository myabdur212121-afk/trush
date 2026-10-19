# DIGITAL TEACHER ENGINE — আপডেট v3 (উমর ফারুক কবিতা প্রজেক্ট থেকে শেখা)
### এই ফাইলটা DIGITAL_TEACHER_ENGINE.md ও ENGINE_UPDATE_v2.md-এর সম্পূরক — পুরনো নিয়ম বাতিল নয়, নতুন অভিজ্ঞতায় পরিমার্জিত
### পরবর্তী AI: DIGITAL_TEACHER_ENGINE.md → ENGINE_UPDATE_v2.md → এই ফাইল (ENGINE_UPDATE_v3.md) — এই ক্রমে পড়ে তারপর কাজ শুরু করো

---

## ০. এই প্রজেক্টে কী বানানো হয়েছে (নতুন রেফারেন্স স্ট্যান্ডার্ড)

- **পাঠ:** "উমর ফারুক" (কাজী নজরুল ইসলাম, জিঞ্জীর কাব্য) — বাংলা সাহিত্য, ৯ম-১০ম শ্রেণি
- **ইনপুট:** ৬ স্ক্রিনশট + **ভেক্টরাইজড PDF** (ব্যবহারকারী দিয়েছে — তাই OCR লাগেনি; §৫ দেখো)
- **ডেলিভারি:** ৩ পর্ব · ৩২ সিন · মোট ২৫:৫২ · 1080p60 · **৫৭ TTS ক্লিপ** (পুরো কোর্সে একটাই voice_id)
- **পর্ব-কাঠামো (কবিতার জন্য নতুন):**

| পর্ব | বিষয় | সিন |
|---|---|---|
| ১ | ইন্ট্রো · কবি-পরিচিতি (২) · পাঠ-পরিচিতি (৩) · স্তবক ১ (৩ সেগমেন্ট) · রিক্যাপ | ১০ |
| ২ | ইন্ট্রো · স্তবক ২ (২) · স্তবক ৩ (৩) · স্তবক ৪ (৩) · রিক্যাপ | ১০ |
| ৩ | ইন্ট্রো · স্তবক ৫ (২) · স্তবক ৬ (৩) · স্তবক ৭ (২) · স্তবক ৮ (২) · **শব্দার্থ-রিভিউ** · **ফাইনাল রিভিশন** | ১২ |

- ফাইল-কাঠামো v2 §৬-এর মতোই: `lesson_<নাম>/{source, data(lesson.json+PROGRESS+narration_P*.md), audio, manim, video}`

---

## ১. সবচেয়ে গুরুত্বপূর্ণ নতুন প্যাটার্ন — কবিতা (poem) কনটেন্ট

গদ্য = flowing justified প্যারাগ্রাফ (v2), কিন্তু **কবিতা = লাইন-বাই-লাইন**:

- মূল টেক্সটে `\n` দিয়ে পংক্তি আলাদা রাখবে (স্ট্রিং-এ `"...মসজিদে।\nপ্রিয়-হারা..."`)
- `book_page(..., kinds=["poem"])` → নতুন `poem_block()` দিয়ে LaTeX রেন্ডার হয়
  (প্রতি পংক্তিতে `\\[3pt]`, `\noindent`, justify নেই)
- reading-bar প্রতিটি **কবিতার পংক্তিতে** নামে; স্তবককে ২-৩ সেগমেন্টে ভাগ (পংক্তি-সীমা)
- কবিতার পাতায় পৃষ্ঠা-নম্বর, স্তবক-শিরোনাম (section) আগের মতোই
- শব্দার্থ-তালিকাও `kinds=["poem"]`-এ সুন্দর বসে (১৮ লাইন পর্যন্ত পাতা-ফিট পরীক্ষিত)
- উদাহরণ: `example_file4.py` (উমর ফারুক পর্ব ৩) — C5–C8, VOCAB, কাস্টম সিন S11/S12

---

## ২. cluster_into_lines() — ক্রিটিকাল বাগ ও নতুন অ্যালগরিদম

**বাগ:** পুরনো max-gap পদ্ধতি ভুল লাইন-ভাগ করত যখন লাইন-গ্যাপ ≈ লাইনের ভেতরের glyph-গ্যাপ।
স্তবক ৭-তে ৮ পংক্তি → ৪ ক্লাস্টার → `read_lines`-এ IndexError-এ রেন্ডার ক্র্যাশ।

**নতুন সমাধান — histogram পিক + adaptive merge:**
- সব glyph-এর y-সেন্টার থেকে histogram → প্রতিটি লাইনের বেসলাইন একটা করে **পিক**
- রেফ/মাত্রার ভাসমান ছোট পিক (বেসলাইনের সামান্য উপরে) **adaptive merge**-এ মূল লাইনে জোড়া লাগে
- যেকোনো ফন্ট-সাইজ/স্কেলে স্ব-ক্যালিব্রেটিং — line_h_units আর্গুমেন্ট আর লাগে না

**যাচাই (আবশ্যক নিয়ম):** যেকোনো নতুন লেআউটে রেন্ডারের পরে
`print(len(lines))` == কবিতার পংক্তি-সংখ্যা — মিলছে কি না দেখবেই (C1=22 ✓ C2=8 ✓ C3=18 ✓
C4=18 ✓ C5=6 ✓ C6=16 ✓ C7=8 ✓ C8=8 ✓ VOCAB=18 ✓)। QC-র আগে এটা না মিললে রেন্ডারই বাতিল।

> ⚠️ এই ফিক্সের কারণে **আগের রেন্ডার করা পর্বগুলোও নতুন করে রেন্ডার করতে হয়** —
> ইঞ্জিন বদলালে সব পর্ব re-render + re-mux + re-concat করবে, পুরনো ভিডিও রাখবে না।

---

## ৩. রিডিং-টাইমিং টিউনিং (audio-first sync-এর সূক্ষ্ম টিউন)

- এই TTS ইঞ্জিনের ক্লিপে **লিড-সাইলেন্স নেই** (০.০s-এই কথা শুরু) → পড়া শুরু ০.৬s,
  scene fade-in rt=0.6 (আগের ১.০s বসালে বার-হাইলাইট পিছিয়ে যায়)
- factory scene: `T = read_dur + discuss_dur + 1.6`; কাস্টম সিনে `T = audio + ~0.9–1.0`
- **Sync pixel-ভেরিফিকেশন:** 1080p ফ্রেমে highlight (#f5e6b8) ও bar (#9b6239)-এর
  pixel-কাউন্ট — পড়ার সময় দুইটাই থাকবে, আলোচনায় থাকবে না (numpy দিয়ে গুনে দেখো)

---

## ৪. seg_ranges — narration-অনুযায়ী কাস্টম সেগমেন্ট-ভাগ

`segment_scene_factory(..., seg_ranges=[(0,7),(7,14),(14,22)])` — নতুন অপশন।
সমান ভাগ নয়; **TTS রেকর্ডিং যত পংক্তি পড়েছে ঠিক সেই সীমা** দেবে
(যেমন স্তবক ১-এর ২২ পংক্তি → ৭+৭+৮)। না দিলে আগের সমান-ভাগ নিয়মই চলে।

---

## ৫. Source of Truth — ভেক্টরাইজড PDF (নতুন নিয়ম)

ব্যবহারকারী PDF দিলে OCR বাদ, কিন্তু PDF-রেন্ডারারের নিজস্ব ফাঁদ আছে:

1. **শব্দ ভাঙে:** "তু মি", "জাহা ততোর" (=তোরে), "মহম্মদ" — pdftotext -layout + pymupdf raw layer দুইটাই দেখো
2. **চন্দ্রবিন্দু/বিশেষ বর্ণ হারায়:** জাঁহা→জাহা, চীরধারী→চিরধারী, নান্দী→নন্দী, উদ্ধত→উদ্যত
3. **সমাধান-ধারা:** সন্দেহজনক শব্দের লাইন স্ক্রিনশট থেকে hi-res crop+zoom করে OCR →
   তারপর প্রকাশিত ক্যানোনিকাল টেক্সট ২-৩ ওয়েব-সাইটে cross-check (banglarkobita, ebanglalibrary ইত্যাদি)
4. **ব্যবহারকারীকে ভিন্ন-শব্দের তালিকা দেখিয়ে অনুমোদন নাও** — এই প্রজেক্টে ৫টা
   (জাঁহা, উদ্ধত, চীরধারী, নান্দী, রোদ্রদগ্ধ) — ব্যবহারকারী "ঠিক আছে" বলার পরই production

---

## ৬. TTS content-filter retry (নতুন অভিজ্ঞতা)

- কবিতার লাইনে কখনো কখনো ফিল্টার আটকায় ("মানব-প্রেমিক! আজিকে তোমারে স্মরি" → ২ বার fail)
- **শব্দ বদলাবে না**, শুধু বিরামচিহ্ন/হাইফেন বদলাও: "মানব-প্রেমিক! আজিকে" → "মানব প্রেমিক, আজিকে" — পাস হয়
- স্ক্রিনের বইয়ের টেক্সট অটুট থাকে; TTS-এ শুধু উচ্চারণ-ছন্দ সামান্য বদলায়
- ⚠️ fail-ও টার্নের ১০-ক্লিপ সীমায় গণনা হয় — তাই fail হলে একবারই retry করো, বেশি হলে পরের টার্নে

---

## ৭. Sandbox রিসেট — প্রতি টার্নের প্রথম কাজ

- রিসেটে ফাইল থাকে, প্যাকেজ থাকে না — প্রতিবার প্রথমেই চেক:

```bash
which ffmpeg xelatex tesseract     # নেই তো apt install: ffmpeg texlive-xetex texlive-latex-extra
                                   #   texlive-latex-recommended fonts-noto-core fonts-noto-extra
                                   #   tesseract-ocr tesseract-ocr-ben
python3 -c "import manim"          # নেই তো pip install manim
fc-list | grep -c "Noto Serif Bengali"   # বাংলা ফন্ট নিশ্চিত
```

- **মাঝপথে tesseract হারালে QC-র OCR ফাঁকা আসে — ভিডিও দোষ নয়!** ফ্রেমের pixel-stat দেখে
  নিশ্চিত হয়ে tesseract আবার ইনস্টল করো
- প্রতি টার্নের শেষে `data/PROGRESS.md` আপডেট — কোন ক্লিপ বাকি, duration তালিকা,
  পরের ধাপ, রিজেনারেট-কমান্ড — সব লিখে রাখো (v2 §৫)

---

## ৮. GitHub আপলোড — ২৫MB সীমা ও স্প্লিট নিয়ম

- web upload-এ ফাইলপ্রতি ~25MB; বড় হলে **স্তবক/সিন-সীমানায়** স্প্লিট করো (মাঝপথে কাটবে না)
- স্প্লিট রেন্ডার-কমান্ড (re-encode — concat ফাইলে -ss কাট নিরাপদ):

```bash
# অংশ ১ (শুরু থেকে 317.25s):   অংশ ২ (317.25s থেকে শেষ):
ffmpeg -y -i part2_final.mp4 -t 317.25 -c:v libx264 -crf 18 -preset veryfast \
       -pix_fmt yuv420p -c:a aac -b:a 128k -ar 44100 part2a_final.mp4
ffmpeg -y -ss 317.25 -i part2_final.mp4 -c:v libx264 -crf 18 -preset veryfast \
       -pix_fmt yuv420p -c:a aac -b:a 128k -ar 44100 part2b_final.mp4
```

- **বাউন্ডারি QC:** কাট-পয়েন্টের শেষ/প্রথম ফ্রেম OCR (শেষ ফ্রেম = আগের স্তবকের আলোচনা,
  প্রথম ফ্রেম = পরের স্তবকের পাতা) + একাধিক পয়েন্টে volumedetect
- এই প্রজেক্টের ফল: part1 22.2MB ✓ · part2a 15.0 ✓ · part2b 9.5 ✓ · part3a 17.0 ✓ · part3b 8.8 ✓
- FULL_CLASS (84MB) web-এ যায় না — মোবাইল-ডাউনলোড/ড্রাইভে দাও; স্প্লিটগুলো জোড়া দিলেই FULL:

```bash
printf "file 'part1_final.mp4'\nfile 'part2a_final.mp4'\nfile 'part2b_final.mp4'\nfile 'part3a_final.mp4'\nfile 'part3b_final.mp4'\n" > l.txt
ffmpeg -y -f concat -safe 0 -i l.txt -c copy FULL_CLASS.mp4
```

---

## ৯. QC টুলকিট (সব এক জায়গায়)

```bash
# শেষ ফ্রেম / মাঝের ফ্রেম → OCR (480p-তে ফেল করলে 2x আপস্কেল):
ffmpeg -y -sseof -1 -i scene.mp4 -frames:v 1 f.png
tesseract f.png stdout -l ben --psm 6
# A/V sync (শুরু/মাঝ/শেষ পয়েন্টে):
ffmpeg -ss 100 -t 3 -i out.mp4 -af volumedetect -f null - 2>&1 | grep mean_volume
# reading-bar pixel চেক (python): highlight(245,230,184)±12 ও bar(155,98,57)±18 কাউন্ট
```

---

## ১০. engine.py-তে যা যা বদলেছে (example_engine_file2.py থেকে)

| জায়গা | পরিবর্তন |
|---|---|
| `poem_block()` | **নতুন** — কবিতার লাইন-বাই-লাইন LaTeX ব্লক |
| `book_page(..., kinds=)` | **নতুন প্যারামিটার** — "prose"/"poem" |
| `cluster_into_lines()` | **সম্পূর্ণ নতুন** — histogram পিক + adaptive merge (লাইন-গ্যাপ≈ইন-লাইন গ্যাপেও নির্ভুল) |
| `segment_scene_factory(..., seg_ranges=)` | **নতুন অপশন** — narration-অনুযায়ী পংক্তি-ভাগ |
| read শুরু | ১.০s → **০.৬s** (TTS-এ লিড-সাইলেন্স নেই) |
| fade-in rt | ০.৮ → **০.৬** |

সর্বশেষ engine সবসময় প্রজেক্টের `manim/engine.py`-তে; নতুন প্রজেক্ট শুরুতে সেটাই কপি করবে।
(এই ai_setup ফোল্ডারে `example_engine_file3.py` নামে কপি দেওয়া আছে।)

---

## ১১. নতুন অধ্যায়ের চেকলিস্ট (কবিতা-সংস্করণ)

```
□ PDF/স্ক্রিনশট → টেক্সট নিষ্কাশন (PDF হলে pdftotext + raw layer; সন্দেহে hi-res OCR + ওয়েব-ক্রসচেক)
□ ভিন্ন-শব্দের তালিকা ব্যবহারকারীকে দেখাও → অনুমোদন নাও
□ data/lesson.json (chunks = স্তবক-ভিত্তিক, text-এ \n দিয়ে পংক্তি; vocab; বইয়ের প্রশ্ন)
□ পর্ব-ভাগ ঠিক করো (স্তবক ধরে; শেষ পর্বে শব্দার্থ-রিভিউ + ফাইনাল রিভিশন)
□ environment চেক (§৭) → PROGRESS.md শুরু
□ প্রতি পর্ব: narration লিখো → TTS (≤১০/টার্ন, fail রিপাংচুয়েট) → ffprobe
   → partN.py (kinds=["poem"], seg_ranges) → -ql রেন্ডার
   → print(len(lines)) == পংক্তি-সংখ্যা যাচাই (§২) → QC ফ্রেম OCR
   → -qh রেন্ডার → mux(apad) → concat → partN_final.mp4
□ সব পর্ব শেষ: FULL concat (চাইলে) · GitHub-এ >25MB হলে স্প্লিট (§৮)
□ প্রতি টার্নের শেষে PROGRESS.md আপডেট
```

---

## ১২. ভুল-সংশোধন নীতি (এই প্রজেক্টের অভিজ্ঞতা থেকে এক লাইনে)

ইঞ্জিনে বাগ → এক জায়গায় ফিক্স → **সব প্রভাবিত পর্ব নতুন করে রেন্ডার** (পুরনো ভিডিও রাখবে না);
একটি মাত্র সিনে কনটেন্ট-ভুল → শুধু সেই ক্লিপ/সিন (MASTER_ROADMAP §৫.৫ আগের মতোই)।
------------------------------------
"""
# -*- coding: utf-8 -*-
"""পল্লিসাহিত্য — সাধারণ ইঞ্জিন মডিউল (সব পর্বে পুনর্ব্যবহৃত হবে)
- পাতার মূল টেক্সট (reading) = LaTeX (XeLaTeX+polyglossia bengali) flowing paragraph
- বোর্ড আলোচনা (explanation) = Manim Text()/bn() — vrow, redline, qbox, qpanel (MCQ/Short/CQ ব্যাজ)
- প্রতিটি অনুচ্ছেদ ২-৩ সেগমেন্টে ভেঙে read(lines)+discuss(board) চক্র; অন্য অংশ আবছা (opacity~0.4)
"""
import re
from manim import *

INK = "#24231f"; DESK = "#d7d0c3"; PAGE = "#faf6ec"; MUTED = "#6d685e"
ACCENT = "#274c3d"; ACCENT2 = "#9b6239"; LINEC = "#b8ad9a"; HL = "#f5e6b8"
RED = "#a33d2e"; GREEN = "#2e6b45"; BLUE = "#2b5f8a"; PURPLE = "#6a3d8f"
SERIF = "Noto Serif Bengali"


# ================================================================== বোর্ড টেক্সট ইঞ্জিন (Text())
def bn(s, size=24, color=INK, weight=NORMAL):
    return Text(s, font=SERIF, font_size=size, color=color, weight=weight)


def bn_wrap(s, size=16, color=INK, weight=NORMAL, max_w=6.1, line_buff=0.08):
    """লম্বা বাক্যকে শব্দ-ভিত্তিক wrap করে একাধিক লাইনের VGroup বানায়।"""
    words = s.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        test = bn(trial, size, color, weight)
        if test.width > max_w and cur:
            lines.append(bn(cur, size, color, weight))
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(bn(cur, size, color, weight))
    return VGroup(*lines).arrange(DOWN, buff=line_buff, aligned_edge=LEFT)


def vrow(a, b, size=21, max_w=6.0):
    left = bn_wrap(a, size, ACCENT2, MEDIUM, max_w=max_w * 0.42)
    arrow = bn("→", int(size * 0.85), MUTED)
    right = bn_wrap(b, size, GREEN, MEDIUM, max_w=max_w * 0.48)
    return VGroup(left, arrow, right).arrange(RIGHT, buff=0.18)


def redline(t, size=19, max_w=6.1):
    return bn_wrap(t, size, RED, MEDIUM, max_w=max_w)


def qbox(lines, w=6.15, title="প্রশ্ন-পয়েন্ট:"):
    title_m = bn(title, 18, ACCENT, BOLD)
    items = [bn_wrap(l, 15.5, INK, max_w=w - 0.5) for l in lines]
    g = VGroup(title_m, *items).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    bg = RoundedRectangle(corner_radius=0.08, width=w, height=g.height + 0.4,
                           fill_color=HL, fill_opacity=1, stroke_color=ACCENT2, stroke_width=1.4)
    g.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.22)
    return VGroup(bg, g)


def board_title():
    t = bn("স্যারের বোর্ড", 23, ACCENT, BOLD)
    sep = Line(ORIGIN, RIGHT * 6.0, stroke_color=INK, stroke_width=1.5)
    g = VGroup(t, sep).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    g.to_edge(RIGHT, buff=0.45).align_to([0, 3.45, 0], UP)
    return g


# ------- প্রশ্ন-ধরন ব্যাজ (MCQ / Short / CQ) -------
TAG_COLORS = {"MCQ": BLUE, "SHORT": GREEN, "CQ": PURPLE}
TAG_LABELS = {"MCQ": "MCQ", "SHORT": "সংক্ষিপ্ত", "CQ": "সৃজনশীল (ক-খ-গ-ঘ)"}


def qtag(kind):
    color = TAG_COLORS.get(kind, MUTED)
    label = TAG_LABELS.get(kind, kind)
    t = bn(label, 14, WHITE, BOLD)
    bg = RoundedRectangle(corner_radius=0.06, width=t.width + 0.28, height=t.height + 0.16,
                           fill_color=color, fill_opacity=1, stroke_width=0)
    t.move_to(bg)
    return VGroup(bg, t)


def qline(tag_kind, text, size=15.5, w=5.5):
    tg = qtag(tag_kind)
    txt = bn_wrap(text, size, INK, max_w=w)
    row = VGroup(tg, txt).arrange(RIGHT, buff=0.15, aligned_edge=UP)
    return row


def qpanel(items, w=6.15, title="সম্ভাব্য প্রশ্ন:"):
    """items: list of (tag_kind, text)।"""
    title_m = bn(title, 18, ACCENT, BOLD)
    rows = [qline(k, t, w=w - 1.7) for k, t in items]
    g = VGroup(title_m, *rows).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    bg = RoundedRectangle(corner_radius=0.08, width=w, height=g.height + 0.4,
                           fill_color=HL, fill_opacity=1, stroke_color=ACCENT2, stroke_width=1.4)
    g.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.22)
    return VGroup(bg, g)


# ================================================================== পাতার মূল টেক্সট ইঞ্জিন (LaTeX)
BENGALI_PREAMBLE = r"""
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{bengali}
\setmainfont{Noto Serif Bengali}[
  UprightFont = *-Regular,
  BoldFont = *-Bold,
]
\newfontfamily\latinfont{Noto Serif}
\usepackage{xcolor}
\usepackage{ragged2e}
\setlength{\parindent}{0pt}
\AtBeginDocument{%
  \righthyphenmin=62\lefthyphenmin=62
  \hyphenpenalty=10000\exhyphenpenalty=10000
  \tolerance=9999\emergencystretch=3em
}
"""


def latin(text):
    """ইংরেজি/লাতিন অংশকে সঠিক ফন্টে রেন্ডার করতে wrap করে (polyglossia bengali-তে glyph miss হয়)।"""
    return r"{\latinfont %s}" % text


bn_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    documentclass="\\documentclass[preview]{standalone}",
    preamble=BENGALI_PREAMBLE,
)

MINIPAGE_IN = 6.2
UNITS_PER_IN = 3.6
TARGET_TEXT_W = 6.2
FIXED_SCALE = TARGET_TEXT_W / (MINIPAGE_IN * UNITS_PER_IN)


def tex_raw(latex_body, scale=FIXED_SCALE, color=INK):
    t = Tex(latex_body, tex_template=bn_template, color=color)
    t.scale(scale)
    return t


def latex_inline(text, size=15, color=INK, bold=False):
    inner = r"\textbf{%s}" % text if bold else text
    latex = r"\fontsize{%s}{%s}\selectfont %s" % (size, size * 1.3, inner)
    return tex_raw(latex, color=color)


def latex_paragraph(text, size=14, leading=21, color=INK, width_in=MINIPAGE_IN):
    """পুরো অনুচ্ছেদ একটাই flowing LaTeX ব্লক (স্বাভাবিক প্যারাগ্রাফ, বাক্য জোর করে ভাঙা হয় না)।"""
    latex = (r"\begin{minipage}{%sin}\fontsize{%s}{%s}\selectfont\justifying %s\end{minipage}"
              % (width_in, size, leading, text))
    mobj = tex_raw(latex, color=color)
    line_h_units = (leading / 72.27) * FIXED_SCALE
    return mobj, line_h_units


def poem_block(text, size=13, leading=None, color=INK, width_in=MINIPAGE_IN):
    """কবিতার স্তবক — লাইন-বাই-লাইন রেন্ডার (justified prose নয়)।
    text-এ \n দিয়ে কবিতার পংক্তি আলাদা থাকবে; প্রতিটি পংক্তি নিজের লাইনে বসে,
    reading-bar-এর জন্য cluster_into_lines() পংক্তি-ভিত্তিক লাইন দেয়।"""
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if leading is None:
        leading = size * 1.4
    body = r"\\[3pt] ".join(lines)
    latex = (r"\begin{minipage}{%sin}\fontsize{%s}{%s}\selectfont\noindent %s\end{minipage}"
              % (width_in, size, leading, body))
    mobj = tex_raw(latex, color=color)
    line_h_units = (leading / 72.27) * FIXED_SCALE
    return mobj, line_h_units


def cluster_into_lines(mobj, line_h_units=None):
    """glyph-গুলোকে রেন্ডার-লাইন অনুযায়ী ভাগ করে — histogram পিক + adaptive merge।
    রেফ/মাত্রার ভাসমান পিক (বেসলাইনের সামান্য উপরে) মূল লাইনে জোড়া লাগে; লাইন-স্পেসিং
    যেকোনো স্কেলে নিজে মেপে নেয়।"""
    fam = [m for m in mobj.family_members_with_points() if m.get_num_points() > 0]
    if not fam:
        return [mobj]
    ys = np.array([float(m.get_center()[1]) for m in fam])
    ymin, ymax = float(ys.min()), float(ys.max())
    span = max(ymax - ymin, 0.5)
    bin_w = max(span / 300, 0.008)
    bins = np.arange(ymin - bin_w, ymax + 2 * bin_w, bin_w)
    hist, edges = np.histogram(ys, bins=bins)
    hist = np.convolve(hist.astype(float), [1, 1, 1], mode="same")
    min_sep = max(span / 60, 0.06)
    peak_min = max(2, hist.max() * 0.06)
    peaks = []  # (y, weight)
    for i in range(1, len(hist) - 1):
        if hist[i] >= hist[i - 1] and hist[i] > hist[i + 1] and hist[i] >= peak_min:
            y = (edges[i] + edges[i + 1]) / 2
            if peaks and y - peaks[-1][0] < min_sep:
                if hist[i] > peaks[-1][1]:
                    peaks[-1] = (y, hist[i])
            else:
                peaks.append((y, hist[i]))
    if not peaks:
        return [VGroup(*fam)]
    # adaptive merge: পিক-স্পেসিং দুই ক্লাস্টারে (ভাসমান-পিক বনাম সত্যিকারের লাইন) ভাগ
    sps = [b[0] - a[0] for a, b in zip(peaks, peaks[1:])]
    if len(sps) > 1:
        ss = sorted(sps)
        jump = max(((b - a), (a + b) / 2) for a, b in zip(ss, ss[1:]))
        merge_t = jump[1] if jump[0] > 0.02 else None
        if merge_t is not None:
            merged = [peaks[0]]
            for p in peaks[1:]:
                if p[0] - merged[-1][0] < merge_t:
                    if p[1] > merged[-1][1]:
                        merged[-1] = p
                else:
                    merged.append(p)
            peaks = merged
    peak_ys = [p[0] for p in peaks]
    buckets = {i: [] for i in range(len(peak_ys))}
    for m in fam:
        y = float(m.get_center()[1])
        j = int(np.argmin([abs(y - p) for p in peak_ys]))
        buckets[j].append(m)
    out = [VGroup(*buckets[i]) for i in sorted(buckets) if buckets[i]]
    out.sort(key=lambda g: g.get_center()[1], reverse=True)  # উপর থেকে নিচে
    return out


# ================================================================== পাতার লেআউট
PAGE_W = 6.9; PAGE_H = 7.5; TEXT_W = 6.2


def book_page(head_title, sub_title, section, paragraphs, sizes, page_label, kinds=None):
    """kinds: প্রতি প্যারাগ্রাফের ধরন — None/'prose' = flowing justified (latex_paragraph),
    'poem' = লাইন-বাই-লাইন (poem_block)।"""
    page = RoundedRectangle(corner_radius=0.05, width=PAGE_W, height=PAGE_H,
                             fill_color=PAGE, fill_opacity=1, stroke_color=LINEC, stroke_width=2)
    page.to_edge(LEFT, buff=0.25).set_y(0)

    head = latex_inline(head_title, size=24, color=ACCENT, bold=True)
    sub = latex_inline(sub_title, size=15, color=MUTED)
    headg = VGroup(head, sub).arrange(DOWN, buff=0.05)
    sec = latex_inline(section, size=18, color=ACCENT2, bold=True) if section else None

    para_mobjs = []
    line_heights = []
    parts = [headg]
    if sec:
        parts.append(sec)
    kinds = kinds or ["prose"] * len(paragraphs)
    for text, size, kind in zip(paragraphs, sizes, kinds):
        if kind == "poem":
            pg, lh = poem_block(text, size=size)
        else:
            pg, lh = latex_paragraph(text, size=size, leading=size * 1.5)
        para_mobjs.append(pg)
        line_heights.append(lh)
        parts.append(pg)

    body = VGroup(*parts).arrange(DOWN, buff=0.24)
    for pg in para_mobjs:
        pg.align_to(body, LEFT)
    if sec:
        sec.align_to(body, LEFT)
    scale_factor_w = TEXT_W / body.width
    body.scale(scale_factor_w)
    max_h = PAGE_H - 1.0
    scale_factor_h = 1.0
    if body.height > max_h:
        scale_factor_h = max_h / body.height
        body.scale(scale_factor_h)
    total_scale = scale_factor_w * scale_factor_h
    body.move_to(page).align_to(page, UP).shift(DOWN * 0.25)

    para_data = []
    for pg, lh in zip(para_mobjs, line_heights):
        final_lh = lh * total_scale
        lines = cluster_into_lines(pg, final_lh)
        para_data.append((pg, lines))

    no = latex_inline(page_label, size=12, color=MUTED).move_to(page.get_bottom() + UP * 0.2)

    page_group = VGroup(page, body, no)
    return page_group, para_data


def segment_ranges(n_lines, n_segments):
    """n_lines-কে n_segments ভাগে (প্রায়) সমান ভাগ করে [(start,end), ...] রিটার্ন করে।"""
    n_segments = max(1, min(n_segments, n_lines))
    base = n_lines // n_segments
    rem = n_lines % n_segments
    ranges = []
    start = 0
    for i in range(n_segments):
        size = base + (1 if i < rem else 0)
        end = start + size
        ranges.append((start, end))
        start = end
    return ranges


def dim_except(lines, keep_start, keep_end, keep_opacity=1.0, dim_opacity=0.4):
    anims = []
    for i, ln in enumerate(lines):
        target = keep_opacity if keep_start <= i < keep_end else dim_opacity
        anims.append(ln.animate.set_opacity(target))
    return anims


# ================================================================== Scene বেস
class BaseScene(Scene):
    T = 30.0

    def construct(self):
        self.camera.background_color = DESK
        self.el = 0.0
        self.body()
        pad = self.T - self.el
        if pad > 0:
            self.wait(pad)

    def p(self, *a, rt=0.7):
        self.play(*a, run_time=rt)
        self.el += rt

    def w(self, t):
        if t > 0:
            self.wait(t)
            self.el += t

    def upto(self, t):
        self.w(t - self.el)

    def read_lines(self, blocks, t_start, t_end):
        weights = [max(len(b.family_members_with_points()), 1) for b in blocks]
        total = sum(weights) or 1
        span = t_end - t_start
        cur = blocks[0]
        hl = SurroundingRectangle(cur, fill_color=HL, fill_opacity=0.55, stroke_width=0, buff=0.04)
        bar = Rectangle(width=cur.width + 0.1, height=0.04, fill_color=ACCENT2, fill_opacity=1, stroke_width=0)
        bar.next_to(cur, DOWN, buff=0.02)
        self.upto(t_start)
        self.p(FadeIn(hl), FadeIn(bar), rt=0.3)
        self.bring_to_back(hl)
        t = t_start
        for i, b in enumerate(blocks):
            dur = span * weights[i] / total
            t += dur
            if i < len(blocks) - 1:
                nxt = blocks[i + 1]
                nhl = SurroundingRectangle(nxt, fill_color=HL, fill_opacity=0.55, stroke_width=0, buff=0.04)
                nbar = Rectangle(width=nxt.width + 0.1, height=0.04, fill_color=ACCENT2, fill_opacity=1, stroke_width=0)
                nbar.next_to(nxt, DOWN, buff=0.02)
                self.upto(t - 0.2)
                self.p(Transform(hl, nhl), Transform(bar, nbar), rt=0.2)
                self.bring_to_back(hl)
        self.upto(t_end)
        self.p(FadeOut(hl), FadeOut(bar), rt=0.4)


def segment_scene_factory(page_kwargs_fn, n_segments, seg_index, read_dur, discuss_dur,
                           discuss_builder, seg_ranges=None):
    """একটি generic segment scene ক্লাস তৈরি করে।
    page_kwargs_fn: () -> dict (book_page আর্গুমেন্ট) — প্রতিবার নতুন mobject বানাতে function হিসেবে
    discuss_builder: () -> VGroup (বোর্ডের কন্টেন্ট, নিজেই arrange করা)
    seg_ranges: [(start,end), ...] — narration-এর সাথে মিলিয়ে কাস্টম লাইন-ভাগ (ডিফল্ট সমান ভাগ)
    """
    total_t = read_dur + discuss_dur + 1.6

    class _Seg(BaseScene):
        T = total_t

        def body(self):
            page_group, para_data = book_page(**page_kwargs_fn())
            _, lines = para_data[0]
            ranges = seg_ranges or segment_ranges(len(lines), n_segments)
            s0, s1 = ranges[seg_index]
            bt = board_title()
            self.p(FadeIn(page_group, shift=RIGHT * 0.2), FadeIn(bt), rt=0.6)
            if seg_index > 0:
                for i, ln in enumerate(lines):
                    if i < s0:
                        ln.set_opacity(0.4)
            self.upto(0.6)
            self.read_lines(lines[s0:s1], 0.6, 0.6 + read_dur)
            self.p(*dim_except(lines, s0, s1), rt=0.5)

            board_content = discuss_builder()
            board_content.next_to(bt, DOWN, buff=0.32).align_to(bt, LEFT)
            for m in board_content:
                if hasattr(m, "width") and m.width > 6.25:
                    m.scale_to_fit_width(6.25)

            t0 = self.el
            n_items = len(board_content)
            remain = self.T - 0.5 - t0
            per = max(remain / max(n_items, 1), 0.3)
            t = t0
            for m in board_content:
                self.upto(t)
                self.p(FadeIn(m, shift=UP * 0.1), rt=min(0.6, per * 0.6))
                t += per
            self.upto(self.T - 0.4)

    return _Seg

---------------------------
