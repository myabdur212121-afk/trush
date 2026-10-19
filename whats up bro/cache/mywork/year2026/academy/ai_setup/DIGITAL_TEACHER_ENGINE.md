# DIGITAL TEACHER ENGINE — কারিগরি সংযোগ-নির্দেশিকা
### (MASTER_ROADMAP-এর সঙ্গী ফাইল: roadmap বলে "কী" বানাতে হবে, এই ফাইল বলে ভেতরে ভেতরে "কীভাবে" সব জোড়া লাগে)

---

## ০. ইঞ্জিনটা এক নজরে

```
ব্যবহারকারীর ইনপুট (বইয়ের ছবি/টেক্সট)
        │
        ▼
[১] পাঠ-বিশ্লেষণ ──────► central lesson data (এক উৎস)
        │                        │
        ▼                        ▼
[২] Narration script      [৪] প্রশ্ন-ইঞ্জিন (রিসার্চ→যাচাই→ব্যাংক)
        │                        │
        ▼                        ▼
[৩] অডিও-ভিডিও ইঞ্জিন      [৫] Practice Website (inline data)
   (TTS→duration→scene→          │
    render→mux→concat)           ▼
        │                  [৬] Hub Website
        ▼                        │
     QC লুপ ◄────────────────────┘
        │
        ▼
   ফাইনাল ডেলিভারি + ব্যবহারকারীর অনুমোদন
```

মূলনীতি: **সব উপাদান একটাই কেন্দ্রীয় তথ্য থেকে জন্মায়** — ভিডিওর বোর্ড, ওয়েবসাইটের প্রশ্ন, রিভিশন তালিকা সব `data/lesson.json` থেকে; তাহলে ভিডিও আর ওয়েবসাইটে তথ্যের গরমিল হয় না।

---

## ১. Central Lesson Data — ইঞ্জিনের হৃৎপিণ্ড

প্রতিটি অধ্যায়ের জন্য প্রথমেই `lesson_<নাম>/data/lesson.json` বানাবে:

```
meta        : নাম, লেখক, ধরন, বই/পৃষ্ঠা
author_bio  : লেখক-পরিচিতির প্রতিটি তথ্য (exam_note সহ)
theme       : surface (আপাত অর্থ) + real (আসল বক্তব্য) + key_device
chunks[]    : id, title, মূল টেক্সট (হুবহু), explanation, important[]
vocabulary  : বইয়ের টীকা + অতিরিক্ত কঠিন শব্দ (আলাদা রাখবে)
important_lines[] : লাইন + কেন + স্তর (সাধারণ/গুরুত্বপূর্ণ/অতি)
book_exercises    : বইয়ের নিজের প্রশ্ন (এগুলো "existing" ট্যাগ পাবে)
mcq_concept_map / cq_concept_map : কোন অংশ থেকে কী প্রশ্ন সম্ভব
```

নিয়ম: video-script, বোর্ডের লেখা, প্রশ্নব্যাংক — সব এই ফাইল থেকে টানবে; নতুন তথ্য পেলে আগে এখানে লিখবে, তারপর ব্যবহার করবে।

---

## ২. ব্যবহারকারীর কাছ থেকে তথ্য নেওয়ার প্রোটোকল

**শুরুতেই যা চাইবে:**
1. বইয়ের পৃষ্ঠার **স্পষ্ট ছবি** (মূল পাঠ + লেখক-পরিচিতি + শব্দার্থ/টীকা + বইয়ের প্রশ্ন — সবগুলো পৃষ্ঠা)
2. শ্রেণি/পরীক্ষা (SSC/HSC/অন্য) — ব্যাখ্যার ভাষা ও প্রশ্নের কাঠিন্য এতে ঠিক হয়
3. কতটুকু চাই — শুধু ভিডিও? শুধু প্রশ্ন? পুরো প্যাকেজ?

**কাজ থামিয়ে জিজ্ঞেস করবে যখন:**
- ছবির কোনো শব্দ zoom করেও পড়া যাচ্ছে না (কখনো অনুমান নয়)
- ডিজাইন/কাঠামোতে নতুন কিছু করতে যাচ্ছ → **mockup frame render করে দেখাও → "হ্যাঁ" পেলে full production**
- কোনো ফাইল মুছতে হবে (সাইজ-হিসাব দেখিয়ে অনুমতি নেবে)
- এক পর্ব শেষ → দেখিয়ে অনুমোদন নিয়ে পরের পর্ব (ব্যবহারকারী "টানা করো" বললে ভিন্ন কথা)

**ফিডব্যাক প্রোটোকল:** ব্যবহারকারীর সংশোধন এলে (ক) আগে নিজের ভাষায় বোঝাটা লিখবে, (খ) দরকারে নমুনা দেখাবে, (গ) সম্মতি পেলে প্রয়োগ করবে — পুরনো ভুল প্যাটার্নটা roadmap/engine ফাইলে আপডেট করে রাখবে যাতে পরে আর না হয়।

---

## ৩. অডিও-ভিডিও ইঞ্জিন (audio-first bonding — এটাই sync-এর রহস্য)

**ধাপ ধরে ধরে:**
```
১. প্রতিটি scene-এর narration লিখবে
     - Reading scene: মূল টেক্সট হুবহু (সাধু ভাষা অটুট) + ২-৪ সেকেন্ডের lead-in
     - Board scene : শিক্ষকের ব্যাখ্যার ভাষা (roadmap §২.৬)
     - TTS-এ সংখ্যা কথায় (১৮৮০→আঠারোশো আশি), ইংরেজি বাংলা উচ্চারণে
২. TTS দিয়ে সব clip বানাবে  [সীমা: ~১০ clip/টার্ন, ≤১৫০০ অক্ষর/clip;
     fail-এর retry-ও গোনা হয় → তাই পর্ব = ৮–১০ scene]
     এক কোর্সে সব scene-এ একটাই voice_id।
৩. ffprobe দিয়ে প্রতিটি clip-এর duration মাপবে:
     ffprobe -v error -show_entries format=duration -of csv=p=0 file.mp3
৪. Scene class-এ T = duration + ~0.9 সেকেন্ড।
৫. Scene-এর ভেতরে টাইমলাইন চালাবে helper দিয়ে:
     self.el (elapsed) ট্র্যাক; p(anim, rt)=play+el বাড়াও; upto(t)=t পর্যন্ত wait
     → narration-এর নির্দিষ্ট সেকেন্ডে নির্দিষ্ট জিনিস পর্দায় আসে।
৬. Reading bar sync: প্যারাগ্রাফ-ইঞ্জিন প্রতিটি লাইনের bounding box জানে;
     লাইন-i-এর সময় = মোট পড়ার সময় × (লাইনের অক্ষর ÷ মোট অক্ষর);
     bar/highlight Transform দিয়ে লাইন-বাই-লাইন নামে (rt≈0.25)।
৭. Render (দ্রুত): manim render -ql --disable_caching file.py SceneName
৮. Mux (apad অপরিহার্য — নইলে concat-এ অডিও পিছিয়ে যায়):
     d=$(ffprobe ... scene.mp4)
     ffmpeg -i scene.mp4 -i scene.mp3 -c:v copy -af apad -t "$d" \
            -c:a aac -b:a 128k -ar 44100 out.mp4
৯. Concat (একই কোডেক বলে -c copy যথেষ্ট):
     ffmpeg -f concat -safe 0 -i list.txt -c copy part.mp4
     পর্বগুলো জুড়ে FULL: একই কমান্ডে part1+2+3 → FULL_CLASS.mp4
```

**Justified প্যারাগ্রাফ-ইঞ্জিন (LaTeX নয়):** শব্দপ্রতি `Text()` mobject → width মাপা → greedy wrap → শেষ লাইন ছাড়া gap=(width−শব্দগুলোর মোট width)÷(শব্দসংখ্যা−1) → প্রতি লাইন আলাদা VGroup। space-width = `Text("অ অ").width − Text("অঅ").width`। পাতা ৬.৯×৭.৫ unit, টেক্সট width ৬.২, ফন্ট ১৪.৫–১৯; বেশি লম্বা হলে auto `scale_to_fit_height`।

**QC লুপ:** প্রতিটি ঘন scene render-এর পর শেষ frame বের করে দেখবে
(`ffmpeg -sseof -1 -i s.mp4 -frames:v 1 f.png`) — টেক্সট কাটা/overlap থাকলে spacing/size কমিয়ে **শুধু সেই scene** re-render; পুরো পর্ব নয়। Mux-এর পর কাঁচা `manim/media/` সঙ্গে সঙ্গে মুছবে (storage)।

**ভুল-সংশোধন নীতি:** কোনো scene-এ কনটেন্ট-ভুল ধরা পড়লে → সংশ্লিষ্ট audio ঠিক আছে কি দেখো → দরকারে ওই এক clip নতুন করে → ওই এক scene re-render+mux → পর্ব আবার concat। কখনোই গোটা ক্লাস নতুন করে বানাবে না।

---

## ৪. প্রশ্ন-ইঞ্জিন (research → verify → bank → site)

```
১. lesson.json-এর concept_map থেকে টপিক-তালিকা
২. অনলাইন রিসার্চ: "<গল্পের নাম> MCQ / সৃজনশীল / জ্ঞানমূলক প্রশ্ন" —
   একাধিক শিক্ষা-সাইট cross-check (courstika, sohagschool জাতীয়)
৩. যাচাই: প্রতিটি প্রশ্নের উত্তর মূল পাঠের সঙ্গে মেলাও;
   না মিললে বাদ; সন্দেহ থাকলে ব্যবহারকারীকে জানাও
৪. ট্যাগ: existing (বই) / adapted (সাইটের নামসহ) / AI_generated
৫. ব্যাংক (JS):
   mcqBank[]  {q, uddipok?, options[4], answer(0-3), explain, source}
   shortBank[]{q, a(এক-অনুচ্ছেদ), source}          ← মান ২
   cqBank[]   {uddipok, source, subs[[প্রশ্ন,উত্তর]×৪]} ← ক১ খ২ গ৩ ঘ৪
   PAPER      {mcq:[৩০টি index], short:[৫টি], cq:index}
৬. Validate (deploy-এর আগে বাধ্যতামূলক) — node দিয়ে:
   new Function(js+';return {mcqBank,...}')() →
   দৈর্ঘ্য, options=4, answer 0-3, explain আছে, PAPER index বৈধ — সব চেক
৭. Inline: questions.js-কে index.html-এর <script>-এ ঢুকিয়ে দাও
   (এক ফাইল = প্রিভিউ ও ডাউনলোড দুটোই কাজ করে); python-এ replace করবে
```
উত্তর-ফরম্যাটের বিস্তারিত মান: MASTER_ROADMAP §৪.১ — সেটাই চূড়ান্ত।

---

## ৫. ফাইল-কাঠামো (এই কনভেনশনেই চলবে)

```
/ (root)
├── index.html                  ← Hub: ভিডিও প্লেয়ার + practice লিংক
├── MASTER_ROADMAP_AI_Teacher.md
├── DIGITAL_TEACHER_ENGINE.md   ← এই ফাইল
├── practice_site/index.html    ← প্রশ্নব্যাংক inline
└── lesson_<নাম>/
    ├── source/    (বইয়ের ছবি — source of truth, মুছবে না)
    ├── data/      (lesson.json, বিশ্লেষণ)
    ├── audio/     (pN_XX_নাম.mp3 — পর্ব_সিরিয়াল_কাজ)
    ├── manim/     (part1.py, part2.py, ... — production code)
    └── video/     (partN/ পর্ব-ফাইনাল + FULL_CLASS.mp4)
```

Server: `python3 -m http.server 8000 --bind 0.0.0.0 --directory /home/user`
(root থেকে — যাতে hub, practice, ভিডিও সব relative লিংকে চলে)।

**GitHub-এ রাখা/পুনর্নির্মাণ:** ওয়েব-আপলোডে ফাইলপ্রতি ~২৫MB সীমা → FULL_CLASS (৩৮MB) বাদ দিয়ে part1/2/3 আলাদা আপলোড করলেই চলবে; FULL পরে ১ কমান্ডে আবার তৈরি হয়:
```
printf "file 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\n" > l.txt
ffmpeg -f concat -safe 0 -i l.txt -c copy FULL_CLASS.mp4
```
কোড (.py) + audio + data থাকলে যেকোনো scene/পর্ব সম্পূর্ণ রিবিল্ডযোগ্য।

---

## ৬. Environment checklist (sandbox নতুন হলে সব ইনস্টল হারায় — প্রতিবার চেক)

```
which ffmpeg               || sudo apt-get install -y ffmpeg fonts-noto
python3 -c "import manim"  || pip install manim
fc-list | grep "Noto Serif Bengali"    # ফন্ট নিশ্চিত
which node                 # প্রশ্নব্যাংক validate-এর জন্য
```
Workspace ফাইল থাকে, install করা জিনিস থাকে না — এটা মাথায় রেখে টার্ন সাজাবে।
Storage-সীমা ~128MB: বড় কাজের আগে `du -sh` দেখে হিসাব; মোছার আগে অনুমতি।

---

## ৭. নতুন অধ্যায় যোগের সংক্ষিপ্ত চেকলিস্ট (পুরো ইঞ্জিন এক পাতায়)

```
□ ছবি নাও → পুরো পড়ো → ঝাপসা অংশ crop-zoom যাচাই
□ data/lesson.json বানাও → ব্যবহারকারীকে বিশ্লেষণ দেখাও
□ পর্ব-ভাগ ঠিক করো (৮-১০ scene/পর্ব) → অনুমোদন নাও
□ প্রতি পর্ব: narration → TTS → duration → partN.py → render → QC frame
  → mux(apad) → কাঁচা render মুছো → concat → দেখাও
□ সব পর্ব শেষে FULL concat
□ প্রশ্ন-ইঞ্জিন: রিসার্চ → যাচাই → ব্যাংক (§৪.১ ফরম্যাট) → validate → inline
□ Hub-এ নতুন lesson-কার্ড + ভিডিও-বাটন যোগ
□ শেষ আত্মপরীক্ষা: ভিডিও-ওয়েবসাইট একই তথ্য? সব উত্তরে ব্যাখ্যা?
  source-ট্যাগ আছে? শিক্ষার্থী ভিডিও শেষে practice-এ যেতে পারবে?
```
