# my_work

**উদ্দেশ্য:** personal Manim **work-saving + exam hall**।
Rough/দৈনন্দিন কাজ এখানে বছর-ধরে জমা থাকে; project pass করলে main repo-তে graduate হয়।
আর packaging থাকায় Colab-এ যেকোনো project এক লাইনে import করা যায়।

```
write  →  test (Colab)  →  passes  →  main repo
```

## Structure

```
my_work/
├── pyproject.toml        # repo-কে pip-installable বানায় (include = ["year2026*"])
├── README.md             # এই instruction + overview
└── year2026/             # 🧊 বছরের archive (read-only history)
    ├── __init__.py
    ├── INDEX.md          # ← বছরের সূচিপত্র (প্রতি project-এ update)
    ├── buffon_needles/   🚧
    ├── line_intersection/ ✅
    └── bbox_shift/       ✅
```

**প্রতি project folder-এ same pattern:**
- `__init__.py` — package marker (এক লাইন: `"""package"""`)
- `<lib>.py` — জিনিসপত্র (import-যোগ্য, render ছাড়াও চলে)
- `scene_construct.py` — `def construct` অংশ
- `notes.md` — ৩ লাইন: কী চেয়েছিলাম / কী হলো / status

## Colab one-liner (ব্যবহার)

```python
!apt-get install -y -qq ffmpeg libcairo2-dev libpango1.0-dev texlive-latex-extra \
    fonts-noto-core fonts-noto-extra fonts-beng-extra
!pip install -q git+https://github.com/myabdur2121-cpu/my_work.git
from year2026.buffon_needles.paper_lib import *
import year2026.buffon_needles.scene_construct as sc
!manim -ql {sc.__file__} BuffonNeedlesScene
```

## Instructions / নিয়ম

### নতুন project
1. Folder বানান: `year2026/<project_name>/` + ভিতরে `__init__.py`
2. Lib আর scene আলাদা file-এ; `notes.md`-এ ৩ লাইন
3. **`year2026/INDEX.md`-এ এক লাইন যোগ করুন**
4. Colab-এ install করে test করুন

### নতুন বছর
1. নতুন folder `year2027/` + `__init__.py` + নতুন `INDEX.md`
2. `pyproject.toml`-এর `include`-এ `"year2027*"` যোগ

### File খোঁজা
- Repo page-এ keyboard-এ `t` চাপুন → নাম লিখুন → file সামনে (folder ঘোরার দরকার নেই)

### Status
🚧 exam / ✅ passed / ❌ abandoned

### Long-term নিয়ম
- পুরনো বছর **read-only** — edit নয়, শুধু নতুন বছর যোগ
- Month path-এ নয় (কখনো দরকার হলে নতুন project-এ `m09_` prefix)
- Graduate = main repo-তে copy; এখানে status ✅

## বছরের সূচিপত্র

→ [year2026/INDEX.md](year2026/INDEX.md)
