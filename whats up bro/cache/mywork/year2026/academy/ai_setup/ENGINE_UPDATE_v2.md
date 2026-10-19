# DIGITAL TEACHER ENGINE — আপডেট v2 (পল্লিসাহিত্য প্রজেক্ট থেকে শেখা)
### এই ফাইলটা DIGITAL_TEACHER_ENGINE.md এর সম্পূরক — পুরনো নিয়ম বাতিল নয়, বরং নতুন অভিজ্ঞতায় পরিমার্জিত।
### পরবর্তী AI: প্রথমে এই পুরো ফাইল পড়ে নাও, তারপর কাজ শুরু করো।

---

## ০. সবচেয়ে গুরুত্বপূর্ণ পরিবর্তন — হাইব্রিড ইঞ্জিন (LaTeX + Text() মিশ্রণ)

আগে পুরো ভিডিও `Text()` (Manim বিল্ট-ইন) দিয়ে বানানো হতো, ম্যানুয়াল word-wrap কোড দিয়ে (`nirio_bangali_part1.mp4` রেফারেন্স)। এখন আমরা শিখেছি **দুই জায়গায় দুই ইঞ্জিন লাগে**:

| জায়গা | ইঞ্জিন | কারণ |
|---|---|---|
| বইয়ের পাতার মূল টেক্সট (reading section) | **LaTeX** (XeLaTeX + polyglossia bengali) | নিখুঁত justify, স্বাভাবিক flowing প্যারাগ্রাফ — Text() দিয়ে হাতে-করা word-wrap কখনোই এত ভালো justify দেয় না |
| স্যারের বোর্ড (explanation section) | **Text()/bn()** (আগের মতোই) | vrow (শব্দ→অর্থ তীরচিহ্ন), redline (লাল সতর্কবার্তা), qbox/qpanel (প্রশ্ন-বক্স) — এগুলো ছোট ছোট UI উপাদান, LaTeX দরকার নেই |

**ভুল যেটা প্রথমে করেছিলাম:** পুরো অনুচ্ছেদকে বাক্যে ভেঙে প্রতিটা বাক্য আলাদা LaTeX ব্লক বানিয়ে `arrange(DOWN)` করেছিলাম — এতে ছোট বাক্য জোর করে জাস্টিফাই হয়ে অস্বাভাবিক ফাঁকা জায়গা তৈরি হয়, লিস্টের মতো দেখায়, প্যারাগ্রাফের মতো লাগে না।

**সঠিক পদ্ধতি:** পুরো অনুচ্ছেদ **একটাই flowing LaTeX minipage ব্লক** হিসেবে রেন্ডার করা (`\begin{minipage}...\end{minipage}`, `\justifying`) — বাক্য যেখানে শেষ হয় সেখান থেকেই পরের বাক্য একই লাইনে চলতে থাকে, ঠিক আসল বইয়ের মতো। রিডিং-বার সিঙ্কের জন্য LaTeX রেন্ডার হয়ে যাওয়া glyph-গুলোকে তাদের **প্রকৃত y-অবস্থান (রেন্ডার-লাইন)** অনুযায়ী ক্লাস্টার করে "লাইন" বানানো হয় — বাক্য-ভিত্তিক নয়, প্রকৃত-লাইন-ভিত্তিক।

---

## ১. নতুন কনটেন্ট প্যাটার্ন — সেগমেন্ট রিডিং + বিস্তারিত আলোচনা + প্রশ্ন-ট্যাগ

আগে: পুরো অনুচ্ছেদ একবারে পড়া → একটাই আলোচনা সিন।

**নতুন (এখন থেকে সবসময় এভাবে):**
1. প্রতিটা অনুচ্ছেদকে **২-৩টা সেগমেন্টে** ভাগ করা (লাইন-সংখ্যা অনুযায়ী প্রায় সমান ভাগ)
2. প্রতিটা সেগমেন্ট → **আলাদা সিনে**: প্রথমে reading-bar দিয়ে ওই সেগমেন্টের লাইনগুলো হাইলাইট করে পড়া, তারপর সেই একই সিনে বোর্ডে **বিস্তারিত আলোচনা** (নিজের ভাষায় সহজ করে গল্প/বিষয় বুঝিয়ে বলা, শুধু ২-৩ শব্দের পয়েন্ট না)
3. যে সেগমেন্ট নিয়ে কাজ চলছে সেটার opacity=1, বাকি পুরো অনুচ্ছেদ (আগের/পরের সেগমেন্ট) opacity≈0.4 (আবছা) — চোখ ফোকাসড থাকে
4. একই পাতায় একাধিক অনুচ্ছেদ (chunk) থাকলে, বর্তমানে যেটা নিয়ে কাজ চলছে না সেটাও পুরোপুরি আবছা

**প্রশ্ন-ট্যাগ (নতুন উপাদান, `qpanel`/`qtag`):** প্রতিটা আলোচনায় বোর্ডে রঙিন ব্যাজ দিয়ে প্রশ্নের ধরন দেখাতে হবে —
- 🔵 **MCQ** (নীল ব্যাজ)
- 🟢 **সংক্ষিপ্ত** (সবুজ ব্যাজ)
- 🟣 **সৃজনশীল (ক-খ-গ-ঘ)** (বেগুনি ব্যাজ)

প্রতি সেগমেন্টের আলোচনায় ২-৩টা সম্ভাব্য প্রশ্ন এই ট্যাগসহ দেখানো, যাতে ছাত্র বুঝতে পারে এই অংশ থেকে কী ধরনের প্রশ্ন পরীক্ষায় আসতে পারে।

---

## ২. কোড আর্কিটেকচার — `engine.py` পুনর্ব্যবহারযোগ্য মডিউল

পুরো লজিক একটা `engine.py`-তে রাখা, প্রতিটা পর্বের `partN.py` শুধু `from engine import *` করে টেক্সট ও সিন-স্পেসিফিক জিনিস লেখে। এতে সব পর্বে consistent ইঞ্জিন থাকে, বাগ ফিক্স একবার করলে সব জায়গায় কাজ করে।

মূল ফাংশন:
- `bn(text, size, color, weight)` — Text() wrapper
- `bn_wrap(text, size, ..., max_w)` — লম্বা বাক্য শব্দ-ভিত্তিক wrap করে VGroup বানায় (bn() এর width ছাড়ালে wrap দরকার, নাহলে বোর্ডের বাইরে চলে যায়)
- `vrow(a, b)`, `redline(t)`, `qbox(lines)`, `qpanel(items)`, `qtag(kind)` — বোর্ড UI উপাদান
- `latex_paragraph(text, size, leading)` — flowing LaTeX প্যারাগ্রাফ মোবজেক্ট + cluster করার জন্য line-height রিটার্ন করে
- `cluster_into_lines(mobj, line_h_units)` — glyph-গুলোকে y-position দিয়ে প্রকৃত লাইনে ভাগ করে (**অবশ্যই চূড়ান্ত scale+position বসানোর পরে ডাকতে হবে**, নাহলে y-স্থানাঙ্ক ভুল হবে)
- `book_page(head, sub, section, paragraphs[], sizes[], page_label)` — সম্পূর্ণ পাতা বানায়, একাধিক অনুচ্ছেদ সাপোর্ট করে
- `segment_ranges(n_lines, n_segments)`, `dim_except(lines, keep_start, keep_end)` — সেগমেন্ট-ভিত্তিক dimming হেল্পার
- `segment_scene_factory(page_kwargs_fn, n_segments, seg_index, read_dur, discuss_dur, discuss_builder)` — একটা সম্পূর্ণ read+discuss scene ক্লাস **ডায়নামিকভাবে** তৈরি করে

---

## ৩. বাগ-ফিক্স যা মনে রাখতেই হবে (সময় বাঁচাতে)

1. **ইংরেজি শব্দ LaTeX পাতায় লিখলে বক্স (□□□) দেখায়** — কারণ `Noto Serif Bengali` ফন্টে লাতিন glyph নেই এবং polyglossia bengali তা সঠিক ফন্টে সুইচ করে না এমনিই। সমাধান: preamble-এ `\newfontfamily\latinfont{Noto Serif}` যোগ করে, ইংরেজি অংশ `{\latinfont টেক্সট}` (curly-brace group syntax) দিয়ে wrap করা। **সাবধান:** `\latinfont{টেক্সট}` (কমান্ড-আর্গুমেন্ট সিনট্যাক্স) কাজ করে না, খালি কালো স্ক্রিন দেয়! শুধু `{\latinfont টেক্সট}` (group সিনট্যাক্স) কাজ করে। হেল্পার ফাংশন: `latin(text)` রিটার্ন করে `r"{\latinfont %s}" % text`।

2. **Bengali hyphenation ভুলভাবে শব্দ ভেঙে ফেলে** (যেমন "পেয়া-রা", "বসিরহাট" ভেঙে যাওয়া) — polyglossia bengali document শুরু হওয়ার সময় নিজের hyphenation প্যারামিটার সেট করে দেয়, তাই preamble-এ সরাসরি `\righthyphenmin=62` লিখলে কাজ করে না। সমাধান: `\AtBeginDocument{...}` দিয়ে wrap করতে হবে, এবং শুধু hyphenmin না, `\hyphenpenalty=10000\exhyphenpenalty=10000\tolerance=9999\emergencystretch=3em` সবগুলো একসাথে লাগবে হাইফেনেশন পুরোপুরি বন্ধ করতে।

3. **Dynamic ভাবে তৈরি Scene class manim CLI চিনতে পারে না** (ভুল scene রেন্ডার হয়, বা "not in the script" এরর) — `segment_scene_factory()`-এর মতো ফাংশন থেকে রিটার্ন হওয়া ক্লাসের `__name__`, `__qualname__`, **এবং `__module__`** — তিনটাই ম্যানুয়ালি সেট করতে হবে (`Klass.__module__ = __name__` কলিং ফাইলে)। শুধু `__name__` বদলালে যথেষ্ট না — manim-এর module scanner `__module__` চেক করে ক্লাসটা এই ফাইলে define হয়েছে কিনা, নাহলে স্কিপ করে দেয়।

4. **LaTeX-এর `scale_to_fit_width`/অন্য স্কেলিং প্রয়োগের পরেই** `cluster_into_lines()` ডাকতে হবে, তার আগে না — কারণ scale/move করলে mobject-এর world-coordinate y-value বদলে যায়, আগে ক্লাস্টার করলে ভুল লাইন-গ্রুপিং হবে।

5. **Text() দিয়ে বানানো লম্বা এক-লাইন বোর্ড টেক্সট বোর্ডের বাইরে চলে যায়** — `scale_to_fit_width()` ব্যবহার করলে ফন্ট ছোট-বড় হয়ে অসামঞ্জস্যপূর্ণ দেখায়। সঠিক সমাধান: `bn_wrap()` দিয়ে multi-line VGroup বানানো (word-by-word wrap, ঠিক প্যারাগ্রাফের মতো)।

---

## ৪. রেন্ডার ওয়ার্কফ্লো (নতুন নিয়ম)

```
প্রতিটা পর্বের জন্য:
১. narration লিখো, TTS জেনারেট করো (≤১০ ক্লিপ/টার্ন সীমা — বেশি লাগলে একাধিক টার্নে ভাগ করো)
২. ffprobe দিয়ে প্রতিটা ক্লিপের duration মাপো
৩. partN.py লেখো/আপডেট করো (duration অনুযায়ী read_dur/discuss_dur বসাও)
৪. manim -ql --disable_caching দিয়ে DRAFT রেন্ডার করো (দ্রুত, ভুল থাকলে সস্তায় ধরা পড়ে)
৫. QC: ffmpeg দিয়ে মাঝের/শেষের ফ্রেম বের করে ছবি হিসেবে দেখো (read_file দিয়ে) — layout/overlap/hyphenation/ইংরেজি-বক্স চেক
৬. ভুল থাকলে ঠিক করে আবার -ql রেন্ডার (রিপিট ৪-৫)
৭. -ql সিনগুলো mux (audio+video) করে concat করে draft প্রিভিউ বানাও, ইউজারকে/নিজেকে verify করাও
৮. সব ঠিক থাকলে manim -qh দিয়ে সব সিন আবার রেন্ডার করো (1080p60, প্রোডাকশন কোয়ালিটি)
৯. -qh সিনগুলো mux+concat করে ফাইনাল partN_final.mp4 বানাও
১০. draft(-ql) ভিডিও, raw manim/media ফোল্ডার, intermediate mux ফাইল — সব মুছে workspace পরিষ্কার করো
    (শুধু partN_final.mp4 + সোর্স .py/audio রাখো)
১১. সব পর্ব শেষ হলে: ffmpeg concat দিয়ে ১ কমান্ডে FULL_CLASS.mp4 বানানো যায়, কিন্তু এটা ডিফল্টে workspace-এ
    না রাখাই ভালো (ইউজার বলেছে ছোট পর্বই বেশি গুরুত্বপূর্ণ) — দরকার হলেই বানাও, কাজ শেষে আবার মুছে দাও।
```

**mux কমান্ড টেমপ্লেট (audio ছোট হলে একাধিক ক্লিপ concat করে নিতে হয়):**
```bash
# একাধিক TTS ক্লিপ (read+discuss) জোড়া দেওয়া:
printf "file 'audio/xx_read.mp3'\nfile 'audio/xx_discuss.mp3'\n" > /tmp/a.txt
ffmpeg -y -f concat -safe 0 -i /tmp/a.txt -c copy /tmp/a.mp3

# video+audio mux (apad জরুরি, নইলে concat-এ অডিও পিছিয়ে যায়):
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 scene.mp4)
ffmpeg -y -i scene.mp4 -i audio.mp3 -c:v copy -af apad -t "$d" -c:a aac -b:a 128k -ar 44100 out.mp4

# concat (same codec, তাই -c copy যথেষ্ট):
printf "file 'S01.mp4'\nfile 'S02.mp4'\n..." > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy part_final.mp4
```

---

## ৫. মাল্টি-টার্ন / দীর্ঘ কাজ চালানোর নিয়ম

- TTS-এ **টার্নপ্রতি সর্বোচ্চ ১০ ক্লিপ** সীমা — বড় পর্ব (৯টা chunk, ৪-৫ পর্ব) এক টার্নে শেষ হয় না।
- ইউজার যদি "টানা করো / decide yourself / no question" জাতীয় নির্দেশ দেয়, তাহলে **প্রতিটা টার্নের শেষে progress ফাইলে (`data/PROGRESS.md`)** — কোন পর্ব কতটুকু হয়েছে, বাকি narration script (হুবহু টেক্সট, পরের টার্নে কপি-পেস্ট করে TTS কল করার জন্য), duration যা মাপা হয়েছে, পরের ধাপ কী — সব বিস্তারিত লিখে রাখা, যাতে পরের টার্নে (বা sandbox রিসেট হয়ে গেলে) তক্ষুনি চালিয়ে যাওয়া যায় প্রশ্ন ছাড়াই।
- **sandbox প্রতি সেশনে রিসেট হতে পারে** — ffmpeg, texlive-xetex, manim, fonts-noto সব প্রতিবার নতুন করে `apt-get install`/`pip install` করা লাগতে পারে। কাজ শুরুর আগে `which ffmpeg xelatex; python3 -c "import manim"` দিয়ে চেক করে নেওয়া, না থাকলে ইনস্টল করা।
- ওয়ার্কস্পেস ফাইল (workspace snapshot) persist থাকে, কিন্তু installed packages/processes থাকে না — এটা মাথায় রেখে টার্ন সাজানো।

---

## ৬. এই প্রজেক্টের ফাইল-কাঠামো (রেফারেন্স)

```
lesson_pollisahitya/
├── source/              (বইয়ের ৬টা মূল স্ক্রিনশট — মুছবে না)
├── data/
│   ├── lesson.json      (কেন্দ্রীয় বিশ্লেষণ: author_bio, chunks[9], vocabulary, book_exercises)
│   └── PROGRESS.md       (মাল্টি-টার্ন কাজের ট্র্যাকার)
├── audio/               (s01-s54+ .mp3, নাম কনভেনশন: sNN_<chunk>_<read|discuss>.mp3)
├── manim/
│   ├── engine.py        (পুনর্ব্যবহারযোগ্য ইঞ্জিন — এইটা সব পর্বে import হয়)
│   └── partN.py         (প্রতি পর্বের সিন-ক্লাস + মূল টেক্সট)
└── video/
    └── partN/partN_final.mp4   (শুধু ফাইনাল -qh mux+concat ভিডিও রাখা হয়, draft/raw রাখা হয় না)
```

---

## ৭. সংক্ষিপ্ত চেকলিস্ট (নতুন অধ্যায়ে কাজ শুরুর আগে)

```
□ environment চেক/ইনস্টল (ffmpeg, texlive-xetex, manim, fonts-noto-extra, poppler-utils)
□ বইয়ের ছবি বিশ্লেষণ করে lesson.json বানাও (chunk-ভিত্তিক, প্রতিটার text/explanation/important)
□ ইউজারকে বিশ্লেষণ দেখাও, অনুমতি নাও
□ পর্ব-ভাগ ঠিক করো (প্রতি পর্বে ২-৩টা chunk, প্রতি chunk ২-৩ সেগমেন্টে)
□ প্রতি পর্ব: TTS script লেখো (read+discuss প্রতি সেগমেন্টে) → generate_speech (≤১০/টার্ন)
   → ffprobe duration → engine.py দিয়ে partN.py লেখো/আপডেট করো
   → -ql রেন্ডার → QC ফ্রেম দেখো → ঠিক করো → mux+concat draft verify
   → -qh রেন্ডার → mux+concat ফাইনাল → draft/raw মুছে ফেলো
□ প্রতি টার্নের শেষে PROGRESS.md আপডেট করো (script, duration, next step সহ)
□ সব পর্ব শেষে চাইলে FULL concat বানাও (persist না করে, দরকার হলে regenerate করার কমান্ড লিখে রাখো)
```
